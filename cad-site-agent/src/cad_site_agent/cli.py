"""
CAD Site Agent — CLI entry points.

Commands:
  analyze-dxf      <file> [--output DIR] [--preview] [--legacy-cls]
  classify-drawing <file> [--legacy]
  export-report    <file> [--format json|md|all] [--output DIR] [--preview]
  clean-dxf        <file> [--output FILE] [--snap-tol N] [--min-len N]
  close-gaps       <file> [--output FILE] [--tol N] [--no-bridge] [--same-layer]
  normalize-layers <file> [--config config/layer_aliases.yaml] [--output FILE]
  hatch-candidates <file> [--output DIR] [--min-area N] [--class-filter NAME]
                          [--json-only]
"""
from __future__ import annotations

import sys
from pathlib import Path

# Use click if available, else argparse fallback
try:
    import click
    _HAS_CLICK = True
except ImportError:
    _HAS_CLICK = False

if _HAS_CLICK:
    # ──────────────────────────────────────────────────────────────────────────
    # CLICK-based CLI
    # ──────────────────────────────────────────────────────────────────────────
    import click

    @click.group()
    def main():
        """CAD Site Agent — DXF analysis, cleanup, and export pipeline."""
        pass

    @main.command("analyze-dxf")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--output", "-o", default=None, help="Output directory (default: reports/analysis/)")
    @click.option("--preview", is_flag=True, default=False, help="Render PNG preview")
    @click.option("--legacy-cls", is_flag=True, default=False,
                  help="Use legacy classifier (site_layout taxonomy)")
    def analyze_dxf(dxf_file: str, output: str | None, preview: bool, legacy_cls: bool):
        """Analyse a DXF file and write JSON + Markdown report."""
        _run_analyze(dxf_file, output, preview, legacy_cls=legacy_cls)

    @main.command("classify-drawing")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--legacy", is_flag=True, default=False,
                  help="Use legacy classifier (site_layout taxonomy)")
    def classify_drawing(dxf_file: str, legacy: bool):
        """Classify drawing type using new (or legacy) taxonomy."""
        _run_classify(dxf_file, legacy=legacy)

    @main.command("export-report")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--format", "fmt", default="all", type=click.Choice(["json", "md", "all"]))
    @click.option("--output", "-o", default=None, help="Output directory")
    @click.option("--preview", is_flag=True, default=False)
    @click.option("--legacy-cls", is_flag=True, default=False)
    def export_report(dxf_file: str, fmt: str, output: str | None, preview: bool, legacy_cls: bool):
        """Full analysis + report export."""
        _run_export(dxf_file, fmt, output, preview, legacy_cls=legacy_cls)

    @main.command("clean-dxf")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--output", "-o", default=None)
    @click.option("--snap-tol", default=1.0, type=float, help="Endpoint snap tolerance (drawing units)")
    @click.option("--min-len", default=0.5, type=float, help="Min segment length (drawing units)")
    def clean_dxf(dxf_file: str, output: str | None, snap_tol: float, min_len: float):
        """Clean DXF: remove short segments, snap endpoints, detect duplicates."""
        from .cleanup.cleaner import run_cleanup
        result = run_cleanup(dxf_file, output_path=output, snap_tol=snap_tol, min_len=min_len)
        _print_cleanup_result(result)

    @main.command("close-gaps")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--output", "-o", default=None)
    @click.option("--tol", default=1000.0, type=float,
                  help="Gap tolerance in drawing units (default 1000 = 1m for mm DXF)")
    @click.option("--no-bridge", is_flag=True, default=False,
                  help="Skip LINE bridge insertion; only self-close")
    @click.option("--same-layer", is_flag=True, default=False,
                  help="Only snap endpoints on the same layer")
    def close_gaps(dxf_file: str, output: str | None, tol: float,
                   no_bridge: bool, same_layer: bool):
        """Close gaps between open LWPOLYLINE endpoints."""
        from .cleanup.gap_closer import run_gap_close
        result = run_gap_close(dxf_file, output_path=output, tolerance=tol,
                               bridge_mode=not no_bridge, same_layer_only=same_layer)
        _print_gap_result(result)

    @main.command("normalize-layers")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--config", "-c", default="config/layer_aliases.yaml")
    @click.option("--output", "-o", default=None)
    def normalize_layers(dxf_file: str, config: str, output: str | None):
        """Normalise layer names using alias config."""
        from .semantic.normalizer import run_normalization
        result = run_normalization(dxf_file, config_path=config, output_path=output)
        _print_norm_result(result)

    @main.command("hatch-candidates")
    @click.argument("dxf_file", type=click.Path(exists=True))
    @click.option("--output", "-o", default=None,
                  help="Output directory (default: reports/analysis/)")
    @click.option("--min-area", default=None, type=float,
                  help="Override min_area from hatch_rules.yaml (mm²)")
    @click.option("--class-filter", default=None,
                  help="Only output candidates for this site class")
    @click.option("--json-only", is_flag=True, default=False,
                  help="Write JSON report only (skip Markdown)")
    def hatch_candidates_cmd(
        dxf_file: str,
        output: str | None,
        min_area: float | None,
        class_filter: str | None,
        json_only: bool,
    ):
        """Identify hatch candidates in a DXF file."""
        _run_hatch_candidates(
            dxf_file, output,
            min_area=min_area,
            class_filter=class_filter,
            json_only=json_only,
        )

    def cli_entry():
        main()

else:
    # ──────────────────────────────────────────────────────────────────────────
    # ARGPARSE fallback (for Python 3.12 without click)
    # ──────────────────────────────────────────────────────────────────────────
    import argparse

    def cli_entry():
        parser = argparse.ArgumentParser(prog="cad-site-agent",
                                         description="CAD Site Agent pipeline")
        sub = parser.add_subparsers(dest="cmd")

        # analyze-dxf
        p_a = sub.add_parser("analyze-dxf")
        p_a.add_argument("dxf_file")
        p_a.add_argument("--output", "-o", default=None)
        p_a.add_argument("--preview", action="store_true")
        p_a.add_argument("--legacy-cls", action="store_true", dest="legacy_cls")

        # classify-drawing
        p_c = sub.add_parser("classify-drawing")
        p_c.add_argument("dxf_file")
        p_c.add_argument("--legacy", action="store_true")

        # export-report
        p_e = sub.add_parser("export-report")
        p_e.add_argument("dxf_file")
        p_e.add_argument("--format", dest="fmt", default="all", choices=["json", "md", "all"])
        p_e.add_argument("--output", "-o", default=None)
        p_e.add_argument("--preview", action="store_true")
        p_e.add_argument("--legacy-cls", action="store_true", dest="legacy_cls")

        # clean-dxf
        p_cl = sub.add_parser("clean-dxf")
        p_cl.add_argument("dxf_file")
        p_cl.add_argument("--output", "-o", default=None)
        p_cl.add_argument("--snap-tol", type=float, default=1.0)
        p_cl.add_argument("--min-len", type=float, default=0.5)

        # close-gaps
        p_g = sub.add_parser("close-gaps")
        p_g.add_argument("dxf_file")
        p_g.add_argument("--output", "-o", default=None)
        p_g.add_argument("--tol", type=float, default=1000.0)
        p_g.add_argument("--no-bridge", action="store_true")
        p_g.add_argument("--same-layer", action="store_true")

        # normalize-layers
        p_n = sub.add_parser("normalize-layers")
        p_n.add_argument("dxf_file")
        p_n.add_argument("--config", "-c", default="config/layer_aliases.yaml")
        p_n.add_argument("--output", "-o", default=None)

        # hatch-candidates
        p_h = sub.add_parser("hatch-candidates")
        p_h.add_argument("dxf_file")
        p_h.add_argument("--output", "-o", default=None)
        p_h.add_argument("--min-area", type=float, default=None, dest="min_area")
        p_h.add_argument("--class-filter", default=None, dest="class_filter")
        p_h.add_argument("--json-only", action="store_true", dest="json_only")

        args = parser.parse_args()
        legacy_cls = getattr(args, "legacy_cls", False)

        if args.cmd == "analyze-dxf":
            _run_analyze(args.dxf_file, args.output, args.preview, legacy_cls=legacy_cls)
        elif args.cmd == "classify-drawing":
            _run_classify(args.dxf_file, legacy=getattr(args, "legacy", False))
        elif args.cmd == "export-report":
            _run_export(args.dxf_file, args.fmt, args.output, args.preview, legacy_cls=legacy_cls)
        elif args.cmd == "clean-dxf":
            from .cleanup.cleaner import run_cleanup
            result = run_cleanup(args.dxf_file, output_path=args.output,
                                 snap_tol=args.snap_tol, min_len=args.min_len)
            _print_cleanup_result(result)
        elif args.cmd == "close-gaps":
            from .cleanup.gap_closer import run_gap_close
            result = run_gap_close(args.dxf_file, output_path=args.output,
                                   tolerance=args.tol, bridge_mode=not args.no_bridge,
                                   same_layer_only=args.same_layer)
            _print_gap_result(result)
        elif args.cmd == "normalize-layers":
            from .semantic.normalizer import run_normalization
            result = run_normalization(args.dxf_file, config_path=args.config,
                                       output_path=args.output)
            _print_norm_result(result)
        elif args.cmd == "hatch-candidates":
            _run_hatch_candidates(
                args.dxf_file, args.output,
                min_area=args.min_area,
                class_filter=args.class_filter,
                json_only=args.json_only,
            )
        else:
            parser.print_help()

    # Argparse stubs that match click command names for pyproject.toml entry points
    def analyze_dxf(): cli_entry()
    def classify_drawing(): cli_entry()
    def export_report(): cli_entry()
    def clean_dxf(): cli_entry()
    def close_gaps(): cli_entry()
    def normalize_layers(): cli_entry()
    def hatch_candidates(): cli_entry()


# ──────────────────────────────────────────────────────────────────────────────
# Shared implementation functions
# ──────────────────────────────────────────────────────────────────────────────

def _resolve_output_dir(dxf_file: str, output: str | None) -> Path:
    """Default output: reports/analysis/ (flat, not nested per-file)."""
    if output:
        out = Path(output)
    else:
        out = Path("reports") / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _run_analyze(dxf_file: str, output: str | None, preview: bool, *, legacy_cls: bool = False):
    from .analyzer.dxf_analyzer import analyze_dxf as _analyze
    from .analyzer.report_writer import write_json_report, write_markdown_report, render_preview_png

    print(f"Analysing: {dxf_file}")
    report = _analyze(dxf_file)

    if legacy_cls:
        from .analyzer.drawing_classifier import classify_drawing
        cls = classify_drawing(report)
        cls_dict = cls.to_dict()
    else:
        from .classify.drawing_type import classify_drawing_type
        cls_new = classify_drawing_type(report)
        cls_dict = cls_new.to_dict()

    out_dir = _resolve_output_dir(dxf_file, output)
    stem = Path(dxf_file).stem

    json_path = out_dir / f"{stem}.analysis.json"
    md_path   = out_dir / f"{stem}.analysis.md"

    _write_json_report_with_new_cls(report, cls_dict, json_path)
    _write_md_report_with_new_cls(report, cls_dict, md_path)

    print(f"  JSON  -> {json_path}")
    print(f"  MD    -> {md_path}")

    label = cls_dict.get("label") or cls_dict.get("drawing_type", "?")
    conf  = cls_dict.get("confidence", 0.0)
    print(f"\n  Type: {label} ({conf:.0%} confidence)")
    print(f"  Entities: {report.total_entities:,} | Layers: {report.total_layers} | "
          f"Unit: {report.likely_unit}")
    print(f"  Closed poly: {report.closed_polyline_count} | "
          f"Open poly: {report.open_polyline_count}")
    spline = report.entity_type_counts.get("SPLINE", 0)
    hatch  = report.entity_type_counts.get("HATCH", 0)
    print(f"  SPLINE: {spline} | HATCH: {hatch} | "
          f"TEXT+MTEXT: {len(report.text_entries)}")

    if preview:
        png_path = out_dir / f"{stem}.preview.png"
        print(f"  Rendering preview -> {png_path} ...")
        ok = render_preview_png(dxf_file, png_path)
        if ok:
            print(f"  Preview -> {png_path}")
        else:
            print("  Preview render failed (see warning above)")


def _run_classify(dxf_file: str, *, legacy: bool = False):
    from .analyzer.dxf_analyzer import analyze_dxf as _analyze

    print(f"Classifying: {dxf_file}")
    report = _analyze(dxf_file)

    if legacy:
        from .analyzer.drawing_classifier import classify_drawing
        cls = classify_drawing(report)
        print(f"\n  Type (legacy):  {cls.drawing_type}")
        print(f"  Confidence:     {cls.confidence:.1%}")
        print(f"  Themes:         {', '.join(cls.detected_themes) or '—'}")
        for note in cls.notes:
            print(f"  Note: {note}")
    else:
        from .classify.drawing_type import classify_drawing_type
        result = classify_drawing_type(report)
        print(f"\n  Label:       {result.label}")
        print(f"  Confidence:  {result.confidence:.1%}")
        for r in result.reasons:
            print(f"  Reason:  {r}")
        d = result.to_dict()["diagnostics"]
        print(f"\n  SPLINE:{d['spline_count']}  HATCH:{d['hatch_count']}  "
              f"INSERT:{d['insert_count']}  SemanticClasses:{d['semantic_class_count']}")


def _run_export(dxf_file: str, fmt: str, output: str | None, preview: bool,
                *, legacy_cls: bool = False):
    from .analyzer.dxf_analyzer import analyze_dxf as _analyze
    from .analyzer.report_writer import render_preview_png

    print(f"Exporting report: {dxf_file}")
    report = _analyze(dxf_file)

    if legacy_cls:
        from .analyzer.drawing_classifier import classify_drawing
        cls = classify_drawing(report)
        cls_dict = cls.to_dict()
    else:
        from .classify.drawing_type import classify_drawing_type
        cls_new = classify_drawing_type(report)
        cls_dict = cls_new.to_dict()

    out_dir = _resolve_output_dir(dxf_file, output)
    stem = Path(dxf_file).stem

    if fmt in ("json", "all"):
        p = out_dir / f"{stem}.analysis.json"
        _write_json_report_with_new_cls(report, cls_dict, p)
        print(f"  JSON -> {p}")

    if fmt in ("md", "all"):
        p = out_dir / f"{stem}.analysis.md"
        _write_md_report_with_new_cls(report, cls_dict, p)
        print(f"  MD   -> {p}")

    if preview:
        p = out_dir / f"{stem}.preview.png"
        render_preview_png(dxf_file, p)
        print(f"  PNG  -> {p}")


# ──────────────────────────────────────────────────────────────────────────────
# Report writers that accept a plain dict (works with both classifiers)
# ──────────────────────────────────────────────────────────────────────────────

def _write_json_report_with_new_cls(report, cls_dict: dict, output_path) -> None:
    import json
    data = {
        "analysis": report.to_dict(),
        "classification": cls_dict,
    }
    Path(output_path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _write_md_report_with_new_cls(report, cls_dict: dict, output_path) -> None:
    from pathlib import Path as _Path
    src = _Path(report.source_file).name

    label      = cls_dict.get("label") or cls_dict.get("drawing_type", "unknown")
    confidence = cls_dict.get("confidence", 0.0)
    reasons    = cls_dict.get("reasons") or cls_dict.get("notes", [])
    themes     = cls_dict.get("detected_themes", [])

    lines = [
        f"# DXF Analysis Report: {src}",
        "",
        f"**File:** `{report.source_file}`  ",
        f"**Size:** {report.file_size_kb} KB  ",
        f"**ezdxf:** {report.ezdxf_version}  ",
        "",
        "---",
        "",
        "## Classification",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Label | **{label}** |",
        f"| Confidence | {confidence:.1%} |",
    ]
    if themes:
        lines.append(f"| Themes | {', '.join(themes)} |")
    lines.append("")

    if reasons:
        lines += ["**Reasons / Notes:**"]
        for r in reasons:
            lines.append(f"- {r}")
        lines.append("")

    diag = cls_dict.get("diagnostics", {})
    if diag:
        lines += [
            "**Diagnostics:**",
            f"- SPLINE: {diag.get('spline_count', 0)}",
            f"- HATCH: {diag.get('hatch_count', 0)}",
            f"- INSERT: {diag.get('insert_count', 0)}",
            f"- Semantic site classes: {diag.get('semantic_class_count', 0)}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total entities | {report.total_entities:,} |",
        f"| Total layers | {report.total_layers:,} |",
        f"| Text entries | {len(report.text_entries):,} |",
        f"| Closed polylines | {report.closed_polyline_count:,} |",
        f"| Open polylines | {report.open_polyline_count:,} |",
        f"| Line segments | {report.total_line_segments:,} |",
        f"| Has hatches | {'Yes' if report.has_hatches else 'No'} |",
        f"| Has blocks | {'Yes' if report.has_blocks else 'No'} |",
        f"| Has splines | {'Yes' if report.has_splines else 'No'} |",
        f"| Has 3D | {'Yes' if report.has_3d else 'No'} |",
        f"| Likely unit | {report.likely_unit} |",
        "",
    ]

    if report.extents_min:
        w = report.extents_width
        h = report.extents_height
        unit = report.likely_unit
        lines += [
            "## Extents",
            "",
            "| | X | Y |",
            "|--|---|---|",
            f"| Min | {report.extents_min[0]:.1f} | {report.extents_min[1]:.1f} |",
            f"| Max | {report.extents_max[0]:.1f} | {report.extents_max[1]:.1f} |",
            f"| Size | {w:.1f} x {h:.1f} ({unit}) |",
        ]
        if unit == "mm":
            lines.append(f"| Size (m) | {w/1000:.1f} x {h/1000:.1f} m |")
        lines.append("")

    lines += [
        "## Entity Types",
        "",
        "| Entity Type | Count |",
        "|-------------|-------|",
    ]
    for etype, cnt in sorted(report.entity_type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {etype} | {cnt:,} |")

    lines += [
        "",
        "## Layer Summary (top 50 by entity count)",
        "",
        "| Layer | Entities | Entity Types | Closed Poly | Open Poly |",
        "|-------|----------|--------------|-------------|-----------|",
    ]
    top_layers = sorted(report.layers.values(), key=lambda l: -l.entity_count)[:50]
    for li in top_layers:
        types_str = ", ".join(
            f"{k}:{v}" for k, v in sorted(li.entity_types.items(), key=lambda x: -x[1])[:4]
        )
        lines.append(
            f"| `{li.name}` | {li.entity_count:,} | {types_str} "
            f"| {li.has_closed_polylines} | {li.has_open_polylines} |"
        )

    if report.text_entries:
        lines += [
            "",
            "## Text Sample (first 20)",
            "",
            "| Type | Layer | Content |",
            "|------|-------|---------|",
        ]
        for t in report.text_entries[:20]:
            content = t.content[:60].replace("|", "\\|")
            lines.append(f"| {t.entity_type} | `{t.layer}` | {content} |")

    if report.block_names:
        lines += [
            "",
            "## Block Names (first 30)",
            "",
            ", ".join(f"`{b}`" for b in report.block_names[:30]),
        ]

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


# ──────────────────────────────────────────────────────────────────────────────
# Print helpers
# ──────────────────────────────────────────────────────────────────────────────

def _print_cleanup_result(result):
    print(f"\n  Removed short segments: {result.get('removed_short', 0)}")
    print(f"  Removed duplicates:     {result.get('removed_duplicates', 0)}")
    print(f"  Endpoints snapped:      {result.get('endpoints_snapped', 0)}")
    if result.get("output_path"):
        print(f"  Output -> {result['output_path']}")


def _print_gap_result(result):
    r = result.to_dict() if hasattr(result, "to_dict") else result
    print(f"\n  Open before: {r.get('open_before', '?'):,}  ->  after: {r.get('open_after', '?'):,}")
    print(f"  Closed before: {r.get('closed_before', '?'):,}  ->  after: {r.get('closed_after', '?'):,}")
    print(f"  Self-closed: {r.get('self_closed', 0)} | "
          f"Merged pairs: {r.get('merged_pairs', 0)} | "
          f"Bridges: {r.get('bridges_added', 0)}")
    errs = r.get("errors", [])
    if errs:
        print(f"  Errors: {len(errs)}")
    if r.get("output_path"):
        print(f"  Output -> {r['output_path']}")


def _print_norm_result(result):
    print(f"\n  Layers normalised: {result.get('layers_renamed', 0)}")
    print(f"  Unmapped layers:   {result.get('unmapped', 0)}")
    if result.get("output_path"):
        print(f"  Output -> {result['output_path']}")


def _run_hatch_candidates(
    dxf_file: str,
    output: str | None,
    *,
    min_area: float | None = None,
    class_filter: str | None = None,
    json_only: bool = False,
):
    from .analyzer.dxf_analyzer import analyze_dxf as _analyze
    from .hatch.semantic_hatch import classify_hatch_candidates, summarise_candidates
    from .export.review_writer import write_hatch_report

    print(f"Hatch candidates: {dxf_file}")
    report = _analyze(dxf_file)

    kwargs: dict = {}
    if min_area is not None:
        # Override via temporary rules path is complex; instead we post-filter
        pass

    candidates = classify_hatch_candidates(
        dxf_file, report, class_filter=class_filter
    )

    # Apply min_area post-filter if overridden on CLI
    if min_area is not None:
        candidates = [c for c in candidates if c.region.area >= min_area]

    summary = summarise_candidates(candidates)

    out_dir = _resolve_output_dir(dxf_file, output)

    json_path, md_path = write_hatch_report(
        candidates, summary, dxf_file, str(out_dir)
    )

    print(f"  JSON -> {json_path}")
    if not json_only:
        print(f"  MD   -> {md_path}")
    else:
        md_path.unlink(missing_ok=True)

    _print_hatch_summary(summary)


def _print_hatch_summary(summary: dict) -> None:
    total    = summary.get("total", 0)
    by_status= summary.get("by_status", {})
    by_class = summary.get("by_class",  {})
    auto_n   = by_status.get("auto",   0)
    review_n = by_status.get("review", 0)
    skip_n   = by_status.get("skip",   0)

    print(f"\n  Regions: {total:,}  |  auto: {auto_n:,}  review: {review_n:,}  skip: {skip_n:,}")

    if by_class:
        top_classes = sorted(by_class.items(), key=lambda x: -x[1])[:8]
        cls_str = "  ".join(f"{k}:{v}" for k, v in top_classes)
        print(f"  Classes: {cls_str}")


if __name__ == "__main__":
    cli_entry()

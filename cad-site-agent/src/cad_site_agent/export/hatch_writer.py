"""
hatch_writer.py — Phase 6A

High-level pipeline: load candidates JSON, filter eligible regions,
write HATCH DXF, produce write reports.

Public API
----------
    WriteReport
    filter_eligible(candidates, *, status_filter, min_confidence,
                    class_filter, material_filter)
        → tuple[list[dict], dict[str, int]]
    run_hatch_write(source_dxf, candidates_json, output_dxf, **kwargs)
        → WriteReport
    write_hatch_write_reports(report, output_dir, stem) → tuple[Path, Path]
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import ezdxf

from .dxf_writer import material_to_layer_name, write_hatch_dxf


# ─── WriteReport ─────────────────────────────────────────────────────────────


@dataclass
class WriteReport:
    """Immutable summary of one hatch-write run."""

    source_dxf:      str
    candidates_json: str
    output_dxf:      str
    generated_at:    str
    total_input:     int
    total_eligible:  int
    total_written:   int
    total_skipped:   int
    skips_by_reason: dict[str, int] = field(default_factory=dict)
    by_material:     dict[str, dict] = field(default_factory=dict)


# ─── filter_eligible ─────────────────────────────────────────────────────────


def filter_eligible(
    candidates: list[dict],
    *,
    status_filter: str = "auto",
    min_confidence: Optional[float] = None,
    class_filter: Optional[str] = None,
    material_filter: Optional[str] = None,
) -> tuple[list[dict], dict[str, int]]:
    """Return (eligible, skips_by_reason) from *candidates*.

    Filter order:
      1. semantic_label.feature_type == "region"
      2. semantic_label.export_role  == "hatch_and_export"
      3. status == status_filter       (default "auto")
      4. semantic_label.material_class is non-empty
      5. confidence >= min_confidence  (if set)
      6. class_guess == class_filter   (if set)
      7. material_class == material_filter (if set)
    """
    eligible: list[dict] = []
    skips: dict[str, int] = {}

    for cand in candidates:
        sem           = cand.get("semantic_label", {})
        feature_type  = sem.get("feature_type", "")
        export_role   = sem.get("export_role", "")
        material_class = sem.get("material_class", "")
        status        = cand.get("status", "")
        confidence    = float(cand.get("confidence", 0.0))
        class_guess   = cand.get("class_guess", "")

        if feature_type != "region":
            skips["not_region"] = skips.get("not_region", 0) + 1
            continue

        if export_role != "hatch_and_export":
            skips["wrong_export_role"] = skips.get("wrong_export_role", 0) + 1
            continue

        if status != status_filter:
            skips["status_not_auto"] = skips.get("status_not_auto", 0) + 1
            continue

        if not material_class:
            skips["no_material_class"] = skips.get("no_material_class", 0) + 1
            continue

        if min_confidence is not None and confidence < min_confidence:
            skips["low_confidence"] = skips.get("low_confidence", 0) + 1
            continue

        if class_filter is not None and class_guess != class_filter:
            skips["class_filtered"] = skips.get("class_filtered", 0) + 1
            continue

        if material_filter is not None and material_class != material_filter:
            skips["material_filtered"] = skips.get("material_filtered", 0) + 1
            continue

        eligible.append(cand)

    return eligible, skips


# ─── run_hatch_write ─────────────────────────────────────────────────────────


def run_hatch_write(
    source_dxf: str,
    candidates_json: str,
    output_dxf: str,
    *,
    status_filter: str = "auto",
    min_confidence: Optional[float] = None,
    class_filter: Optional[str] = None,
    material_filter: Optional[str] = None,
) -> WriteReport:
    """Full pipeline: filter candidates, write HATCH DXF, return WriteReport.

    Safety rules
    ------------
    - Raises FileNotFoundError("Source DXF …")    if source DXF is absent.
    - Raises FileNotFoundError("Candidates JSON …") if JSON is absent.
    - Raises FileExistsError                        if output DXF already exists.
    - Never opens the source DXF for writing.
    - Always creates an output DXF (empty when zero eligible candidates).
    """
    src_path  = Path(source_dxf)
    json_path = Path(candidates_json)
    out_path  = Path(output_dxf)

    if not src_path.exists():
        raise FileNotFoundError(f"Source DXF not found: {source_dxf}")
    if not json_path.exists():
        raise FileNotFoundError(f"Candidates JSON not found: {candidates_json}")
    if out_path.exists():
        raise FileExistsError(f"Output DXF already exists: {output_dxf}")

    payload    = json.loads(json_path.read_text(encoding="utf-8"))
    candidates = payload.get("candidates", [])

    eligible, filter_skips = filter_eligible(
        candidates,
        status_filter=status_filter,
        min_confidence=min_confidence,
        class_filter=class_filter,
        material_filter=material_filter,
    )

    # Build per-material summary before writing
    by_material: dict[str, dict] = {}
    for cand in eligible:
        mat = cand.get("semantic_label", {}).get("material_class", "")
        if mat not in by_material:
            by_material[mat] = {"layer": material_to_layer_name(mat), "eligible": 0}
        by_material[mat]["eligible"] += 1

    # Write DXF (always create output, even when empty)
    all_skips = dict(filter_skips)

    if eligible:
        written, write_skips = write_hatch_dxf(str(src_path), eligible, str(out_path))
        for k, v in write_skips.items():
            all_skips[k] = all_skips.get(k, 0) + v
    else:
        doc = ezdxf.new("R2010")
        doc.saveas(str(out_path))
        written = 0

    total_skipped = len(candidates) - len(eligible)

    return WriteReport(
        source_dxf=str(source_dxf),
        candidates_json=str(candidates_json),
        output_dxf=str(output_dxf),
        generated_at=datetime.now().isoformat(timespec="seconds"),
        total_input=len(candidates),
        total_eligible=len(eligible),
        total_written=written,
        total_skipped=total_skipped,
        skips_by_reason=all_skips,
        by_material=by_material,
    )


# ─── write_hatch_write_reports ───────────────────────────────────────────────


def write_hatch_write_reports(
    report: WriteReport,
    output_dir: str,
    stem: str,
) -> tuple[Path, Path]:
    """Write *report* to ``{stem}.hatch_write.json`` and ``{stem}.hatch_write.md``.

    Returns (json_path, md_path).
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    json_path = out / f"{stem}.hatch_write.json"
    md_path   = out / f"{stem}.hatch_write.md"

    # ── JSON ──────────────────────────────────────────────────────────────
    payload = {
        "meta": {
            "source_dxf":      report.source_dxf,
            "candidates_json": report.candidates_json,
            "output_dxf":      report.output_dxf,
            "generated_at":    report.generated_at,
        },
        "totals": {
            "input":    report.total_input,
            "eligible": report.total_eligible,
            "written":  report.total_written,
            "skipped":  report.total_skipped,
        },
        "skips_by_reason": report.skips_by_reason,
        "by_material":     report.by_material,
    }
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # ── Markdown ──────────────────────────────────────────────────────────
    lines: list[str] = [
        f"# Hatch Write Report — {stem}",
        "",
        f"**Generated:** {report.generated_at}  ",
        f"**Source DXF:** `{report.source_dxf}`  ",
        f"**Candidates JSON:** `{report.candidates_json}`  ",
        f"**Output DXF:** `{report.output_dxf}`",
        "",
        "---",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Input candidates | {report.total_input:,} |",
        f"| Eligible         | {report.total_eligible:,} |",
        f"| Written          | {report.total_written:,} |",
        f"| Skipped          | {report.total_skipped:,} |",
        "",
    ]

    if report.total_written == 0:
        lines += [
            "> **Note:** 0 hatches were written. If candidates were filtered by status,",
            "> re-run with `--status review` to include lower-confidence regions.",
            "",
        ]

    if report.skips_by_reason:
        lines += [
            "---",
            "",
            "## Skips by Reason",
            "",
            "| Reason | Count |",
            "|--------|-------|",
        ]
        for reason, count in sorted(report.skips_by_reason.items()):
            lines.append(f"| {reason} | {count:,} |")
        lines.append("")

    if report.by_material:
        lines += [
            "---",
            "",
            "## By Material Class",
            "",
            "| Material | Layer | Eligible |",
            "|----------|-------|----------|",
        ]
        for mat, info in sorted(report.by_material.items()):
            layer    = info.get("layer", material_to_layer_name(mat))
            eligible = info.get("eligible", 0)
            lines.append(f"| {mat} | {layer} | {eligible:,} |")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

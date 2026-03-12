"""
pipeline.py — Full end-to-end pipeline orchestrator.

Public API
----------
    ProcessReport
    run_process(source_dxf, output_dxf, *, status_filter, min_confidence,
                exclude_noise) -> ProcessReport
"""
from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


# ─── ProcessReport ────────────────────────────────────────────────────────────


@dataclass
class ProcessReport:
    source_dxf:         str
    output_dxf:         str
    generated_at:       str
    candidates_total:   int
    candidates_auto:    int
    candidates_review:  int
    hatches_written:    int
    features_written:   int
    features_removed:   int
    features_skipped:   int
    drawing_type:       str   = "unknown"
    drawing_confidence: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


# ─── run_process ──────────────────────────────────────────────────────────────


def run_process(
    source_dxf: str,
    output_dxf: str,
    *,
    status_filter: str = "auto",
    min_confidence: Optional[float] = None,
    exclude_noise: bool = True,
) -> ProcessReport:
    """Run the full end-to-end pipeline: hatch candidates → hatch DXF → route features DXF.

    Args:
        source_dxf:     Path to the input DXF file.
        output_dxf:     Path for the final output DXF (non-region features).
        status_filter:  Which candidate status to pass to hatch writer ("auto" or "review").
                        "all" is not supported — pass each value explicitly if both are needed.
        min_confidence: Optional minimum confidence threshold for hatch writer.
        exclude_noise:  Whether to suppress noise entities in the routing stage.

    Returns:
        ProcessReport with counts from all stages.

    Raises:
        FileNotFoundError: If source_dxf does not exist.
        FileExistsError:   If output_dxf already exists.
        ValueError:        If status_filter is "all" (not supported by the hatch writer).
    """
    src_path = Path(source_dxf)
    out_path = Path(output_dxf)

    # ── Guard checks ─────────────────────────────────────────────────────────
    if not src_path.exists():
        raise FileNotFoundError(f"Source DXF not found: {source_dxf}")
    if out_path.exists():
        raise FileExistsError(f"Output DXF already exists: {output_dxf}")
    if status_filter == "all":
        raise ValueError(
            "status_filter='all' is not supported; hatch_writer.filter_eligible() "
            "performs strict equality matching. Pass 'auto' or 'review' explicitly."
        )

    out_dir  = out_path.parent
    out_stem = out_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().isoformat(timespec="seconds")

    # ── Stage 1 — hatch candidates ───────────────────────────────────────────
    from .analyzer.dxf_analyzer import analyze_dxf
    from .hatch.semantic_hatch import classify_hatch_candidates, summarise_candidates
    from .export.review_writer import write_hatch_report

    analysis_report = analyze_dxf(str(src_path))
    candidates = classify_hatch_candidates(str(src_path), analysis_report)
    summary    = summarise_candidates(candidates)

    json_path, md_path = write_hatch_report(
        candidates, summary, str(src_path), str(out_dir)
    )

    # Rename JSON (and MD) to use output stem if they differ from source stem
    wanted_json = out_dir / f"{out_stem}.hatch_candidates.json"
    wanted_md   = out_dir / f"{out_stem}.hatch_candidates.md"
    if json_path.resolve() != wanted_json.resolve():
        shutil.move(str(json_path), str(wanted_json))
        if md_path.exists():
            md_path.replace(wanted_md)

    candidates_json = str(wanted_json)

    # Aggregate counts (candidates are HatchCandidate objects)
    n_auto   = sum(1 for c in candidates if c.status == "auto")
    n_review = sum(1 for c in candidates if c.status == "review")

    # ── Stages 2 & 3 — hatch writer + routing (with failure cleanup) ─────────
    # Track all files created by this run so they can be removed on failure.
    _created: list[Path] = [wanted_json, wanted_md]

    hatches_dxf_path = out_dir / f"{out_stem}.hatches.dxf"
    process_json     = out_dir / f"{out_stem}.process.json"
    _created.extend([hatches_dxf_path, process_json, out_path])

    _failed = False
    try:
        # ── Stage 2 — hatch writer ───────────────────────────────────────────
        from .export.hatch_writer import run_hatch_write

        write_report = run_hatch_write(
            source_dxf=str(src_path),
            candidates_json=candidates_json,
            output_dxf=str(hatches_dxf_path),
            status_filter=status_filter,
            min_confidence=min_confidence,
        )

        # ── Stage 3 — route non-region features ─────────────────────────────
        from .export.routing import run_route_features

        routing_report = run_route_features(
            source_dxf=str(src_path),
            candidates_json=candidates_json,
            output_dxf=str(out_path),
            exclude_noise=exclude_noise,
        )

        # ── Write process summary JSON ───────────────────────────────────────
        process_payload = {
            "meta": {
                "source_dxf":   source_dxf,
                "output_dxf":   output_dxf,
                "generated_at": generated_at,
            },
            "totals": {
                "candidates_total":   len(candidates),
                "candidates_auto":    n_auto,
                "candidates_review":  n_review,
                "hatches_written":    write_report.total_written,
                "features_written":   routing_report.total_written,
                "features_removed":   routing_report.total_removed,
                "features_skipped":   routing_report.total_skipped,
            },
        }
        process_json.write_text(
            json.dumps(process_payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    except Exception:
        _failed = True
        raise

    finally:
        if _failed:
            for _p in _created:
                try:
                    if _p.exists():
                        _p.unlink()
                except OSError:
                    pass

    # ── Return ProcessReport ─────────────────────────────────────────────────
    return ProcessReport(
        source_dxf=source_dxf,
        output_dxf=output_dxf,
        generated_at=generated_at,
        candidates_total=len(candidates),
        candidates_auto=n_auto,
        candidates_review=n_review,
        hatches_written=write_report.total_written,
        features_written=routing_report.total_written,
        features_removed=routing_report.total_removed,
        features_skipped=routing_report.total_skipped,
    )

"""
review_writer.py — Phase 4B

Write hatch-candidate results to JSON and Markdown files.

Public API
----------
    write_hatch_report(candidates, summary, dxf_path, output_dir)
        → (json_path, md_path)
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..hatch.semantic_hatch import HatchCandidate


# ─── JSON writer ─────────────────────────────────────────────────────────────


def _build_json_payload(
    candidates: list[HatchCandidate],
    summary: dict[str, Any],
    dxf_path: str,
) -> dict[str, Any]:
    return {
        "meta": {
            "source_file":   str(dxf_path),
            "generated_at":  datetime.now().isoformat(timespec="seconds"),
            "total_regions": summary["total"],
        },
        "summary": summary,
        "candidates": [c.to_dict() for c in candidates],
    }


# ─── Markdown writer ─────────────────────────────────────────────────────────


def _build_markdown(
    candidates: list[HatchCandidate],
    summary: dict[str, Any],
    dxf_path: str,
) -> str:
    stem      = Path(dxf_path).stem
    now       = datetime.now().strftime("%Y-%m-%d %H:%M")
    total     = summary["total"]
    by_status = summary.get("by_status", {})
    by_class  = summary.get("by_class",  {})
    top_layers= summary.get("top_layers",{})

    auto_n   = by_status.get("auto",   0)
    review_n = by_status.get("review", 0)
    skip_n   = by_status.get("skip",   0)

    lines: list[str] = [
        f"# Hatch Candidates — {stem}",
        f"",
        f"**Generated:** {now}  ",
        f"**Source:** `{dxf_path}`",
        f"",
        f"---",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total candidates | {total:,} |",
        f"| Auto (≥ 0.75)    | {auto_n:,} |",
        f"| Review (0.45–0.74) | {review_n:,} |",
        f"| Skip (< 0.45)    | {skip_n:,} |",
        f"",
        f"---",
        f"",
        f"## By Site Class",
        f"",
        f"| Class | Count |",
        f"|-------|-------|",
    ]
    for cls, cnt in sorted(by_class.items(), key=lambda x: -x[1]):
        lines.append(f"| {cls} | {cnt:,} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Top Layers",
        f"",
        f"| Layer | Count |",
        f"|-------|-------|",
    ]
    for lyr, cnt in top_layers.items():
        lines.append(f"| `{lyr}` | {cnt:,} |")

    # ── Auto candidates table (first 50) ──────────────────────────────────
    auto_list = [c for c in candidates if c.status == "auto"]
    if auto_list:
        lines += [
            f"",
            f"---",
            f"",
            f"## Auto Candidates (top {min(50, len(auto_list))} of {len(auto_list)})",
            f"",
            f"| ID | Layer | Class | Hatch | Confidence | Area (mm²) |",
            f"|----|-------|-------|-------|-----------|-----------|",
        ]
        for c in auto_list[:50]:
            r = c.region
            lines.append(
                f"| {r.id} | `{r.source_layer}` | {c.class_guess} "
                f"| {c.hatch_class} | {c.confidence:.2f} | {r.area:,.0f} |"
            )

    # ── Review candidates table (first 50) ───────────────────────────────
    review_list = [c for c in candidates if c.status == "review"]
    if review_list:
        lines += [
            f"",
            f"---",
            f"",
            f"## Review Candidates (top {min(50, len(review_list))} of {len(review_list)})",
            f"",
            f"| ID | Layer | Class | Hatch | Confidence | Reasons |",
            f"|----|-------|-------|-------|-----------|---------|",
        ]
        for c in review_list[:50]:
            r = c.region
            reason_str = "; ".join(c.reasons[:2])
            lines.append(
                f"| {r.id} | `{r.source_layer}` | {c.class_guess} "
                f"| {c.hatch_class} | {c.confidence:.2f} | {reason_str} |"
            )

    lines.append("")
    return "\n".join(lines)


# ─── Public API ─────────────────────────────────────────────────────────────


def write_hatch_report(
    candidates: list[HatchCandidate],
    summary: dict[str, Any],
    dxf_path: str,
    output_dir: str,
) -> tuple[Path, Path]:
    """
    Write hatch candidates to JSON and Markdown files.

    Args:
        candidates:  List of HatchCandidate objects.
        summary:     Dict from summarise_candidates().
        dxf_path:    Source DXF path (used to derive stem).
        output_dir:  Directory to write reports into.

    Returns:
        (json_path, md_path)
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    stem = Path(dxf_path).stem

    json_path = out / f"{stem}.hatch_candidates.json"
    md_path   = out / f"{stem}.hatch_candidates.md"

    payload = _build_json_payload(candidates, summary, dxf_path)
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    md_text = _build_markdown(candidates, summary, dxf_path)
    md_path.write_text(md_text, encoding="utf-8")

    return json_path, md_path

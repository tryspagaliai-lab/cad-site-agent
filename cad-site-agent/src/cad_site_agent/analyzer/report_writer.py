"""
Report Writer — Phase 2.

Generates JSON and Markdown reports from AnalysisReport + DrawingClassification.
Also renders a small layer-coloured PNG preview.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from .dxf_analyzer import AnalysisReport
from .drawing_classifier import DrawingClassification


def write_json_report(
    report: AnalysisReport,
    classification: DrawingClassification,
    output_path: str | Path,
) -> None:
    data = {
        "analysis": report.to_dict(),
        "classification": classification.to_dict(),
    }
    Path(output_path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown_report(
    report: AnalysisReport,
    classification: DrawingClassification,
    output_path: str | Path,
) -> None:
    src = Path(report.source_file).name
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
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Drawing type | **{classification.drawing_type}** |",
        f"| Confidence | {classification.confidence:.1%} |",
        f"| Detected themes | {', '.join(classification.detected_themes) or '—'} |",
        "",
    ]
    if classification.notes:
        lines += ["**Notes:**"]
        for n in classification.notes:
            lines.append(f"- {n}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
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
        scale = 1000 if unit == "mm" else 1
        lines += [
            "## Extents",
            "",
            f"| | X | Y |",
            f"|--|---|---|",
            f"| Min | {report.extents_min[0]:.1f} | {report.extents_min[1]:.1f} |",
            f"| Max | {report.extents_max[0]:.1f} | {report.extents_max[1]:.1f} |",
            f"| Size | {w:.1f} × {h:.1f} ({unit}) |",
        ]
        if unit == "mm":
            lines.append(f"| Size (m) | {w/1000:.1f} × {h/1000:.1f} m |")
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
    top_layers = sorted(
        report.layers.values(), key=lambda l: -l.entity_count
    )[:50]
    for li in top_layers:
        types_str = ", ".join(f"{k}:{v}" for k, v in sorted(li.entity_types.items(), key=lambda x: -x[1])[:4])
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


def render_preview_png(dxf_path: str | Path, output_path: str | Path, max_size: int = 20) -> bool:
    """Render a small layer-coloured PNG preview. Returns True on success."""
    try:
        import ezdxf
        import colorsys
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        from ezdxf.addons.drawing.properties import LayoutProperties

        doc = ezdxf.readfile(str(dxf_path))
        msp = doc.modelspace()

        layers = list(doc.layers)
        n = max(len(layers), 1)

        # Assign unique HSV colours to layers
        layer_colors: dict[str, tuple] = {}
        for i, layer_def in enumerate(layers):
            h = i / n
            r, g, b = colorsys.hsv_to_rgb(h, 0.85, 0.9)
            layer_colors[layer_def.dxf.name] = (r, g, b)

        fig = plt.figure(figsize=(max_size, max_size * 0.75), facecolor="#1a1a1a")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor("#1a1a1a")

        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        lp = LayoutProperties.from_layout(msp)
        lp.set_colors(bg="#1a1a1a")
        Frontend(ctx, out).draw_layout(msp, layout_properties=lp)

        ax.set_aspect("equal")
        ax.axis("off")
        fig.savefig(str(output_path), dpi=100, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        return True
    except Exception as exc:
        print(f"  [preview] Warning: {exc}")
        return False

"""
DXF Analyzer — Phase 2 core module.

Reads a DXF file and produces a structured AnalysisReport with:
  - entity type counts (global + per-layer)
  - layer inventory
  - text / mtext extraction
  - drawing extents
  - hatch, block, polyline, spline presence
  - geometry complexity indicators
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import ezdxf
from ezdxf.math import BoundingBox


@dataclass
class LayerInfo:
    name: str
    color: int = 7          # ACI color index (7 = white/black)
    true_color: int | None = None
    linetype: str = "Continuous"
    entity_count: int = 0
    entity_types: dict[str, int] = field(default_factory=dict)
    has_closed_polylines: int = 0
    has_open_polylines: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "color_aci": self.color,
            "true_color": self.true_color,
            "linetype": self.linetype,
            "entity_count": self.entity_count,
            "entity_types": dict(self.entity_types),
            "has_closed_polylines": self.has_closed_polylines,
            "has_open_polylines": self.has_open_polylines,
        }


@dataclass
class TextEntry:
    entity_type: str   # TEXT or MTEXT
    layer: str
    content: str
    x: float
    y: float
    height: float = 0.0
    rotation: float = 0.0


@dataclass
class AnalysisReport:
    source_file: str
    file_size_kb: int
    ezdxf_version: str

    # Global counts
    total_entities: int = 0
    entity_type_counts: dict[str, int] = field(default_factory=dict)

    # Layers
    total_layers: int = 0
    layers: dict[str, LayerInfo] = field(default_factory=dict)

    # Geometry indicators
    has_hatches: bool = False
    has_blocks: bool = False
    has_splines: bool = False
    has_3d: bool = False
    closed_polyline_count: int = 0
    open_polyline_count: int = 0
    total_line_segments: int = 0

    # Text
    text_entries: list[TextEntry] = field(default_factory=list)

    # Extents (in native drawing units)
    extents_min: tuple[float, float] | None = None
    extents_max: tuple[float, float] | None = None
    extents_width: float = 0.0
    extents_height: float = 0.0

    # Unit estimation
    likely_unit: str = "unknown"   # "mm", "m", "unknown"

    # Block references
    block_names: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "source_file": self.source_file,
            "file_size_kb": self.file_size_kb,
            "ezdxf_version": self.ezdxf_version,
            "total_entities": self.total_entities,
            "entity_type_counts": self.entity_type_counts,
            "total_layers": self.total_layers,
            "layers": {k: v.to_dict() for k, v in self.layers.items()},
            "geometry": {
                "has_hatches": self.has_hatches,
                "has_blocks": self.has_blocks,
                "has_splines": self.has_splines,
                "has_3d": self.has_3d,
                "closed_polyline_count": self.closed_polyline_count,
                "open_polyline_count": self.open_polyline_count,
                "total_line_segments": self.total_line_segments,
            },
            "extents": {
                "min": list(self.extents_min) if self.extents_min else None,
                "max": list(self.extents_max) if self.extents_max else None,
                "width": self.extents_width,
                "height": self.extents_height,
            },
            "likely_unit": self.likely_unit,
            "text_count": len(self.text_entries),
            "text_sample": [
                {"type": t.entity_type, "layer": t.layer, "content": t.content[:80],
                 "x": round(t.x, 3), "y": round(t.y, 3)}
                for t in self.text_entries[:20]
            ],
            "block_names": self.block_names[:50],
        }


def _guess_unit(extents_width: float, extents_height: float) -> str:
    """Heuristic: if max dimension > 10_000, likely mm; if < 1000, likely m."""
    maxdim = max(extents_width, extents_height)
    if maxdim > 10_000:
        return "mm"
    elif maxdim < 1_000:
        return "m"
    return "unknown"


def analyze_dxf(dxf_path: str | Path) -> AnalysisReport:
    """Main entry point — reads a DXF and returns a full AnalysisReport."""
    path = Path(dxf_path)
    if not path.exists():
        raise FileNotFoundError(f"DXF not found: {path}")

    doc = ezdxf.readfile(str(path))
    msp = doc.modelspace()

    report = AnalysisReport(
        source_file=str(path),
        file_size_kb=path.stat().st_size // 1024,
        ezdxf_version=ezdxf.__version__,
    )

    # --- Layer table ---
    for layer_def in doc.layers:
        name = layer_def.dxf.name
        li = LayerInfo(name=name)
        try:
            li.color = layer_def.dxf.color
        except Exception:
            pass
        try:
            tc = layer_def.dxf.get("true_color", None)
            li.true_color = tc
        except Exception:
            pass
        try:
            li.linetype = layer_def.dxf.linetype
        except Exception:
            pass
        report.layers[name] = li

    report.total_layers = len(report.layers)

    # --- Entity scan ---
    bbox = BoundingBox()
    block_names_seen: set[str] = set()

    for entity in msp:
        etype = entity.dxftype()
        report.total_entities += 1
        report.entity_type_counts[etype] = report.entity_type_counts.get(etype, 0) + 1

        # Per-layer stats
        try:
            layer_name = entity.dxf.layer
        except Exception:
            layer_name = "0"

        if layer_name not in report.layers:
            report.layers[layer_name] = LayerInfo(name=layer_name)
        li = report.layers[layer_name]
        li.entity_count += 1
        li.entity_types[etype] = li.entity_types.get(etype, 0) + 1

        # --- Geometry flags ---
        if etype == "HATCH":
            report.has_hatches = True

        elif etype == "SPLINE":
            report.has_splines = True

        elif etype == "INSERT":
            report.has_blocks = True
            try:
                block_names_seen.add(entity.dxf.name)
            except Exception:
                pass

        elif etype in ("LINE", "ARC", "CIRCLE"):
            report.total_line_segments += 1
            _update_bbox_line(entity, etype, bbox)

        elif etype == "LWPOLYLINE":
            pts = list(entity.get_points("xy"))
            n = len(pts)
            if n >= 2:
                report.total_line_segments += n - (0 if entity.closed else 1)
                _update_bbox_points(pts, bbox)
            if entity.closed:
                report.closed_polyline_count += 1
                li.has_closed_polylines += 1
            else:
                report.open_polyline_count += 1
                li.has_open_polylines += 1

        elif etype == "POLYLINE":
            verts = list(entity.vertices)
            n = len(verts)
            if n >= 2:
                report.total_line_segments += n
            try:
                flags = entity.dxf.flags
                if flags & 1:   # closed flag
                    report.closed_polyline_count += 1
                else:
                    report.open_polyline_count += 1
            except Exception:
                report.open_polyline_count += 1

        elif etype in ("TEXT", "MTEXT"):
            _extract_text(entity, etype, report)

        # 3D check
        if not report.has_3d:
            try:
                if hasattr(entity.dxf, "extrusion"):
                    ez = entity.dxf.extrusion
                    if abs(ez.z - 1.0) > 0.01:
                        report.has_3d = True
            except Exception:
                pass

    # --- Extents ---
    if bbox.has_data:
        report.extents_min = (bbox.extmin.x, bbox.extmin.y)
        report.extents_max = (bbox.extmax.x, bbox.extmax.y)
        report.extents_width = bbox.extmax.x - bbox.extmin.x
        report.extents_height = bbox.extmax.y - bbox.extmin.y
        report.likely_unit = _guess_unit(report.extents_width, report.extents_height)

    report.block_names = sorted(block_names_seen)

    return report


def _update_bbox_line(entity, etype: str, bbox: BoundingBox) -> None:
    try:
        if etype == "LINE":
            bbox.extend([entity.dxf.start, entity.dxf.end])
        elif etype == "CIRCLE":
            c = entity.dxf.center
            r = entity.dxf.radius
            bbox.extend([(c.x - r, c.y - r, 0), (c.x + r, c.y + r, 0)])
        elif etype == "ARC":
            c = entity.dxf.center
            r = entity.dxf.radius
            bbox.extend([(c.x - r, c.y - r, 0), (c.x + r, c.y + r, 0)])
    except Exception:
        pass


def _update_bbox_points(pts: list, bbox: BoundingBox) -> None:
    try:
        for x, y in pts:
            bbox.extend([(x, y, 0)])
    except Exception:
        pass


def _extract_text(entity, etype: str, report: AnalysisReport) -> None:
    try:
        layer = entity.dxf.layer
    except Exception:
        layer = "0"
    try:
        if etype == "TEXT":
            content = entity.dxf.text or ""
            ins = entity.dxf.insert
            x, y = ins.x, ins.y
            height = entity.dxf.get("height", 0.0)
            rotation = entity.dxf.get("rotation", 0.0)
        else:  # MTEXT
            content = entity.plain_mtext() if hasattr(entity, "plain_mtext") else (entity.text or "")
            ins = entity.dxf.insert
            x, y = ins.x, ins.y
            height = entity.dxf.get("char_height", 0.0)
            rotation = entity.dxf.get("rotation", 0.0)

        report.text_entries.append(TextEntry(
            entity_type=etype,
            layer=layer,
            content=content.strip(),
            x=x, y=y,
            height=height,
            rotation=rotation,
        ))
    except Exception:
        pass

"""
closed_regions.py — Phase 4B

Extract closed polyline regions from a DXF file.

Each closed LWPOLYLINE (and closed POLYLINE) becomes a ClosedRegion with:
  id, source_layer, handle, area, perimeter, bbox, vertex_count,
  is_closed, source_type
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import ezdxf


# ─── Data class ─────────────────────────────────────────────────────────────


@dataclass
class ClosedRegion:
    """A single closed polyline region extracted from a DXF file."""

    id: int
    source_layer: str
    handle: str
    area: float                              # mm² (absolute value, shoelace)
    perimeter: float                         # mm (chord-length approximation)
    bbox: tuple[float, float, float, float]  # (minx, miny, maxx, maxy)
    vertex_count: int
    is_closed: bool
    source_type: str                         # "LWPOLYLINE" | "POLYLINE"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_layer": self.source_layer,
            "handle": self.handle,
            "area": round(self.area, 2),
            "perimeter": round(self.perimeter, 2),
            "bbox": [round(v, 2) for v in self.bbox],
            "vertex_count": self.vertex_count,
            "is_closed": self.is_closed,
            "source_type": self.source_type,
        }


# ─── Geometry helpers ────────────────────────────────────────────────────────


def _shoelace_area(pts: list[tuple[float, float]]) -> float:
    """Absolute area of a polygon via the shoelace formula."""
    n = len(pts)
    if n < 3:
        return 0.0
    total = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def _chord_perimeter(pts: list[tuple[float, float]]) -> float:
    """Straight-segment perimeter (ignores bulge arcs)."""
    n = len(pts)
    total = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        total += math.hypot(x2 - x1, y2 - y1)
    return total


def _bbox(pts: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


# ─── Per-entity geometry ─────────────────────────────────────────────────────


def _lwpolyline_geometry(
    entity,
) -> Optional[tuple[float, float, tuple, int]]:
    """
    Return (area, perimeter, bbox, vertex_count) for a closed LWPOLYLINE.
    Returns None if the entity has fewer than 3 vertices.
    """
    pts_raw = list(entity.get_points())       # (x, y, sw, ew, bulge)
    if len(pts_raw) < 3:
        return None

    pts = [(float(p[0]), float(p[1])) for p in pts_raw]

    # Use ezdxf's built-in area if available (handles bulge), else shoelace
    try:
        area = abs(entity.area)
    except Exception:
        area = _shoelace_area(pts)

    perimeter = _chord_perimeter(pts)
    box = _bbox(pts)
    return area, perimeter, box, len(pts)


def _polyline_geometry(
    entity,
) -> Optional[tuple[float, float, tuple, int]]:
    """
    Return (area, perimeter, bbox, vertex_count) for a closed 2D POLYLINE.
    Returns None if fewer than 3 vertices.
    """
    pts = []
    for v in entity.vertices:
        try:
            loc = v.dxf.location
            pts.append((float(loc.x), float(loc.y)))
        except Exception:
            continue

    if len(pts) < 3:
        return None

    area = _shoelace_area(pts)
    perimeter = _chord_perimeter(pts)
    box = _bbox(pts)
    return area, perimeter, box, len(pts)


# ─── Public API ─────────────────────────────────────────────────────────────


def extract_closed_regions(
    dxf_path: str,
    min_area: float = 100.0,
    max_vertices: int = 5000,
) -> list[ClosedRegion]:
    """
    Open a DXF file and extract all closed LWPOLYLINE / POLYLINE entities
    from modelspace.

    Args:
        dxf_path:     Path to the DXF file.
        min_area:     Minimum area in drawing units² to include
                      (skips tiny slivers).
        max_vertices: Skip degenerate regions with too many vertices.

    Returns:
        List of ClosedRegion objects, sorted by (source_layer, id).
    """
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    regions: list[ClosedRegion] = []
    region_id = 0

    for entity in msp:
        etype = entity.dxftype()

        if etype == "LWPOLYLINE":
            if not entity.is_closed:
                continue
            geom = _lwpolyline_geometry(entity)
            if geom is None:
                continue
            area, perimeter, box, n = geom
            if area < min_area or n > max_vertices:
                continue
            regions.append(
                ClosedRegion(
                    id=region_id,
                    source_layer=entity.dxf.layer,
                    handle=entity.dxf.handle,
                    area=area,
                    perimeter=perimeter,
                    bbox=box,
                    vertex_count=n,
                    is_closed=True,
                    source_type="LWPOLYLINE",
                )
            )
            region_id += 1

        elif etype == "POLYLINE":
            # Check closed flag (works for 2D mesh-less POLYLINE)
            try:
                closed = entity.is_closed
            except AttributeError:
                try:
                    closed = bool(entity.dxf.flags & 1)
                except Exception:
                    closed = False
            if not closed:
                continue

            geom = _polyline_geometry(entity)
            if geom is None:
                continue
            area, perimeter, box, n = geom
            if area < min_area or n > max_vertices:
                continue
            regions.append(
                ClosedRegion(
                    id=region_id,
                    source_layer=entity.dxf.layer,
                    handle=entity.dxf.handle,
                    area=area,
                    perimeter=perimeter,
                    bbox=box,
                    vertex_count=n,
                    is_closed=True,
                    source_type="POLYLINE",
                )
            )
            region_id += 1

    regions.sort(key=lambda r: (r.source_layer, r.id))
    return regions

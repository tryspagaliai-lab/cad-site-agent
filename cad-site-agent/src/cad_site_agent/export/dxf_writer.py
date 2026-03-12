"""
dxf_writer.py — Phase 6B

Low-level ezdxf helpers: layer naming and hatch geometry writing.

Public API
----------
    material_to_layer_name(material_class) → str
    get_region_points(source_doc, handle, source_type) → list[tuple] | None
    write_hatch_dxf(source_dxf_path, eligible_candidates, output_path,
                    *, stabilize, gap_tolerance, snap_distance,
                       min_area, max_vertices)
        → tuple[int, dict[str, int], int]
"""
from __future__ import annotations

from typing import Optional

import ezdxf

from ..geometry.boundary_tools import stabilize_region


# ─── Layer naming ────────────────────────────────────────────────────────────


def material_to_layer_name(material_class: str) -> str:
    """Map a material class code to its output DXF layer name.

    e.g. MAT_PAVING → HATCH_MAT_PAVING
    """
    return f"HATCH_{material_class}"


# ─── Vertex lookup ───────────────────────────────────────────────────────────


def get_region_points(
    source_doc,
    handle: str,
    source_type: str,
) -> Optional[list[tuple[float, float]]]:
    """Look up a polyline entity by *handle* and return its (x, y) vertices.

    Uses the ezdxf entity database; the entity type is resolved from the
    document rather than from *source_type* (which is kept for documentation).

    Returns None if the handle is not found, the entity type is unsupported,
    or extraction raises an exception.
    """
    entity = source_doc.entitydb.get(handle)
    if entity is None:
        return None

    try:
        dtype = entity.dxftype()
        if dtype == "LWPOLYLINE":
            return [(float(p[0]), float(p[1])) for p in entity.get_points()]
        elif dtype == "POLYLINE":
            return [
                (float(v.dxf.location.x), float(v.dxf.location.y))
                for v in entity.vertices
            ]
        else:
            return None
    except Exception:
        return None


# ─── DXF write ───────────────────────────────────────────────────────────────


def write_hatch_dxf(
    source_dxf_path: str,
    eligible_candidates: list[dict],
    output_path: str,
    *,
    stabilize: bool = True,
    gap_tolerance: float = 10.0,
    snap_distance: float = 1.0,
    min_area: float = 100.0,
    max_vertices: int = 5000,
) -> tuple[int, dict[str, int], int]:
    """Create a new DXF with HATCH entities for each eligible candidate.

    Opens *source_dxf_path* read-only to retrieve vertex coordinates via
    handle lookup.  Never modifies the source file.

    When *stabilize* is True (default), each region's vertex list is passed
    through ``stabilize_region()`` before writing.  Regions that fail
    stabilization are counted in ``skip_reasons`` under a key of the form
    ``"stabilize_rejected_<reason>"``.

    Args:
        source_dxf_path:     Path to the source DXF (read-only).
        eligible_candidates: Pre-filtered list of candidate dicts.
        output_path:         Path for the new output DXF.
        stabilize:           Run boundary stabilization (default True).
        gap_tolerance:       Max closing gap for ``close_small_gaps``.
        snap_distance:       Merge threshold for ``snap_nearby_endpoints``.
        min_area:            Reject regions smaller than this area.
        max_vertices:        Reject regions with more vertices than this.

    Returns:
        (written_count, skip_reasons, repaired_count) where:
          - written_count  — number of HATCH entities written
          - skip_reasons   — maps reason → count for all skipped regions
          - repaired_count — regions whose vertex list changed during stabilization
    """
    source_doc = ezdxf.readfile(str(source_dxf_path))
    out_doc = ezdxf.new("R2010")
    msp = out_doc.modelspace()

    written = 0
    repaired_count = 0
    skip_reasons: dict[str, int] = {}

    for cand in eligible_candidates:
        region = cand.get("region", {})
        handle = region.get("handle", "")
        source_type = region.get("source_type", "LWPOLYLINE")
        material_class = cand.get("semantic_label", {}).get("material_class", "")

        if not material_class:
            skip_reasons["no_material_class"] = skip_reasons.get("no_material_class", 0) + 1
            continue

        pts = get_region_points(source_doc, handle, source_type)
        if pts is None or len(pts) < 3:
            skip_reasons["vertex_lookup_failed"] = (
                skip_reasons.get("vertex_lookup_failed", 0) + 1
            )
            continue

        if stabilize:
            original_pts = pts
            pts, reject_reason = stabilize_region(
                pts,
                gap_tolerance=gap_tolerance,
                snap_distance=snap_distance,
                min_area=min_area,
                max_vertices=max_vertices,
            )
            if pts is None:
                key = f"stabilize_rejected_{reject_reason}"
                skip_reasons[key] = skip_reasons.get(key, 0) + 1
                continue
            if pts != original_pts:
                repaired_count += 1

        layer_name = material_to_layer_name(material_class)

        if layer_name not in out_doc.layers:
            out_doc.layers.add(layer_name)

        try:
            hatch = msp.add_hatch(color=7)
            hatch.dxf.layer = layer_name
            hatch.set_solid_fill()
            hatch.paths.add_polyline_path(pts, is_closed=True)
            written += 1
        except Exception:
            skip_reasons["hatch_error"] = skip_reasons.get("hatch_error", 0) + 1

    out_doc.saveas(str(output_path))
    return written, skip_reasons, repaired_count

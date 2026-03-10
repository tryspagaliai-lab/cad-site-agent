"""
DXF Cleaner — Phase 3 MVP.

Operations:
  1. Remove very short ("garbage") line segments below min_len threshold
  2. Detect duplicate lines (same endpoints, same layer)
  3. Snap polyline/line endpoints within snap_tol of each other
  4. Separate annotation entities from geometry (by layer classification)

Returns a CleanupResult dict + writes cleaned DXF if output_path given.
"""
from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import ezdxf
from scipy.spatial import cKDTree
import numpy as np


def _length_2d(x1, y1, x2, y2) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def run_cleanup(
    dxf_path: str | Path,
    output_path: str | Path | None = None,
    snap_tol: float = 1.0,
    min_len: float = 0.5,
) -> dict[str, Any]:
    """
    Run cleanup pipeline on a DXF file.

    Args:
        dxf_path:    Input DXF path.
        output_path: If given, saves cleaned DXF there.
        snap_tol:    Endpoint snap tolerance in drawing units.
        min_len:     Minimum segment length (units below this → removed).

    Returns:
        Dict with cleanup statistics.
    """
    path = Path(dxf_path)
    doc = ezdxf.readfile(str(path))
    msp = doc.modelspace()

    result: dict[str, Any] = {
        "source": str(path),
        "snap_tol": snap_tol,
        "min_len": min_len,
        "removed_short": 0,
        "removed_duplicates": 0,
        "endpoints_snapped": 0,
        "annotation_entities": 0,
        "geometry_entities": 0,
        "output_path": None,
    }

    # Collect handles to delete
    to_delete: list[str] = []
    seen_lines: set[tuple] = set()

    # ── 1. Gather all LINE endpoints for KD-tree snap ──────────────────────
    all_endpoints: list[tuple[float, float]] = []
    endpoint_entities: list[tuple] = []   # (handle, 'start'|'end', entity)

    for entity in msp:
        etype = entity.dxftype()

        # ── Remove short LINE segments ──
        if etype == "LINE":
            try:
                s = entity.dxf.start
                e = entity.dxf.end
                l = _length_2d(s.x, s.y, e.x, e.y)
            except Exception:
                continue

            if l < min_len:
                to_delete.append(entity.dxf.handle)
                result["removed_short"] += 1
                continue

            # ── Detect duplicate lines ──
            key = _line_key(s.x, s.y, e.x, e.y, entity.dxf.layer)
            if key in seen_lines:
                to_delete.append(entity.dxf.handle)
                result["removed_duplicates"] += 1
                continue
            seen_lines.add(key)

            # Register endpoints for snapping
            all_endpoints.append((s.x, s.y))
            endpoint_entities.append((entity.dxf.handle, "start", entity))
            all_endpoints.append((e.x, e.y))
            endpoint_entities.append((entity.dxf.handle, "end", entity))

    # ── 2. Endpoint snap via KD-tree ──────────────────────────────────────
    if all_endpoints and snap_tol > 0:
        pts = np.array(all_endpoints)
        tree = cKDTree(pts)
        # For each endpoint, find all endpoints within snap_tol
        pairs = tree.query_ball_tree(tree, snap_tol)
        snapped: set[int] = set()
        snap_map: dict[int, tuple[float, float]] = {}

        for i, neighbours in enumerate(pairs):
            if i in snapped:
                continue
            if len(neighbours) <= 1:
                continue
            # Compute centroid of cluster
            cluster_pts = pts[neighbours]
            cx, cy = cluster_pts.mean(axis=0)
            for j in neighbours:
                if j != i:
                    snap_map[j] = (cx, cy)
                    snapped.add(j)

        # Apply snap_map
        for idx, (cx, cy) in snap_map.items():
            handle, end_type, entity = endpoint_entities[idx]
            try:
                if end_type == "start":
                    entity.dxf.start = (cx, cy, 0)
                else:
                    entity.dxf.end = (cx, cy, 0)
                result["endpoints_snapped"] += 1
            except Exception:
                pass

    # ── 3. Delete flagged entities ────────────────────────────────────────
    delete_set = set(to_delete)
    entities_to_remove = [e for e in msp if e.dxf.handle in delete_set]
    for e in entities_to_remove:
        msp.delete_entity(e)

    # ── 4. Count annotation vs geometry ───────────────────────────────────
    ANNOTATION_TYPES = {"TEXT", "MTEXT", "DIMENSION", "LEADER", "ACAD_TABLE"}
    for entity in msp:
        if entity.dxftype() in ANNOTATION_TYPES:
            result["annotation_entities"] += 1
        else:
            result["geometry_entities"] += 1

    # ── 5. Save ───────────────────────────────────────────────────────────
    if output_path:
        out = Path(output_path)
        doc.saveas(str(out))
        result["output_path"] = str(out)
    else:
        stem = path.stem
        auto_out = path.parent / f"{stem}_cleaned.dxf"
        doc.saveas(str(auto_out))
        result["output_path"] = str(auto_out)

    return result


def _line_key(x1, y1, x2, y2, layer: str, precision: int = 2) -> tuple:
    """Normalise a line to a canonical key (order-independent)."""
    p1 = (round(x1, precision), round(y1, precision))
    p2 = (round(x2, precision), round(y2, precision))
    if p1 > p2:
        p1, p2 = p2, p1
    return (layer, p1, p2)

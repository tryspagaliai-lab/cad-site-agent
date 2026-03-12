"""
geometry/boundary_tools.py — Phase 6B

Utility functions for polyline geometry stabilization before hatch writing.

Public API
----------
    detect_almost_closed_polyline(pts, tolerance) → bool
    close_small_gaps(pts, tolerance) → list[tuple]
    snap_nearby_endpoints(pts, snap_distance) → list[tuple]
    merge_fragmented_segments(segments, tolerance) → list[tuple]
    rebuild_closed_polyline(pts) → list[tuple]
    stabilize_region(pts, *, gap_tolerance, snap_distance,
                     min_area, max_vertices)
        → tuple[list[tuple] | None, str | None]
"""
from __future__ import annotations

import math
from typing import Optional


# ─── Internal helpers ────────────────────────────────────────────────────────


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _shoelace_area(pts: list[tuple[float, float]]) -> float:
    """Unsigned area via the Shoelace formula."""
    n = len(pts)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1]
        area -= pts[j][0] * pts[i][1]
    return abs(area) / 2.0


def _is_self_intersecting(pts: list[tuple[float, float]]) -> bool:
    """Brute-force O(n²) self-intersection check using segment crossing.

    Only checks proper crossings (not shared endpoints).
    """
    n = len(pts)
    if n < 4:
        return False

    def _cross(o, a, b) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def _seg_cross(p1, p2, p3, p4) -> bool:
        d1 = _cross(p3, p4, p1)
        d2 = _cross(p3, p4, p2)
        d3 = _cross(p1, p2, p3)
        d4 = _cross(p1, p2, p4)
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        return False

    edges = [(pts[i], pts[(i + 1) % n]) for i in range(n)]
    for i in range(len(edges)):
        for j in range(i + 2, len(edges)):
            # Skip adjacent edges that share an endpoint
            if j == len(edges) - 1 and i == 0:
                continue
            if _seg_cross(edges[i][0], edges[i][1], edges[j][0], edges[j][1]):
                return True
    return False


# ─── Public functions ─────────────────────────────────────────────────────────


def detect_almost_closed_polyline(
    pts: list[tuple[float, float]],
    tolerance: float,
) -> bool:
    """Return True if the polyline has a small closing gap within *tolerance*.

    Returns False if pts has fewer than 3 vertices, if the polyline is already
    closed (first == last vertex), or if the gap exceeds *tolerance*.
    """
    if len(pts) < 3:
        return False
    first, last = pts[0], pts[-1]
    if first == last:
        return False  # already closed, no gap
    return _dist(first, last) <= tolerance


def close_small_gaps(
    pts: list[tuple[float, float]],
    tolerance: float,
) -> list[tuple[float, float]]:
    """Return pts with the closing gap removed if it is within *tolerance*.

    If the gap between the first and last vertex is ≤ *tolerance*, drops the
    last vertex so the caller receives n distinct vertices for a closed polygon.

    Returns pts unchanged if already closed, fewer than 3 points, or the gap
    exceeds *tolerance*.
    """
    if len(pts) < 3:
        return pts
    if pts[0] == pts[-1]:
        return pts  # already closed
    if _dist(pts[0], pts[-1]) <= tolerance:
        return pts[:-1]  # drop last; the polygon closes implicitly
    return pts


def snap_nearby_endpoints(
    pts: list[tuple[float, float]],
    snap_distance: float,
) -> list[tuple[float, float]]:
    """Merge consecutive vertices that are within *snap_distance* of each other.

    Iterates through *pts* and skips any point that is within *snap_distance*
    of the previously kept point.  The first point is always kept.
    """
    if len(pts) < 2:
        return pts
    result: list[tuple[float, float]] = [pts[0]]
    for p in pts[1:]:
        if _dist(result[-1], p) > snap_distance:
            result.append(p)
    return result


def merge_fragmented_segments(
    segments: list[list[tuple[float, float]]],
    tolerance: float,
) -> list[tuple[float, float]]:
    """Chain *segments* into a single ordered vertex list.

    Builds a chain by repeatedly finding the next unchained segment whose
    start or end endpoint is within *tolerance* of the current chain tail.
    Reverses segments when needed to maintain direction.

    If segments cannot be fully chained (disconnected geometry), appends the
    remaining segments in their original order.

    Returns the merged vertex list.
    """
    if not segments:
        return []
    if len(segments) == 1:
        return list(segments[0])

    remaining = [list(s) for s in segments]
    chain = remaining.pop(0)

    while remaining:
        tail = chain[-1]
        found = False
        for i, seg in enumerate(remaining):
            if not seg:
                remaining.pop(i)
                found = True
                break
            if _dist(tail, seg[0]) <= tolerance:
                chain.extend(seg[1:])
                remaining.pop(i)
                found = True
                break
            if _dist(tail, seg[-1]) <= tolerance:
                chain.extend(reversed(seg[:-1]))
                remaining.pop(i)
                found = True
                break
        if not found:
            # Cannot chain further; append remaining in order
            for seg in remaining:
                chain.extend(seg)
            break

    return chain


def rebuild_closed_polyline(
    pts: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """Return a clean closed vertex list without a duplicate closing vertex.

    If the first and last vertices are identical (explicitly closed), drops the
    last vertex.  The caller receives n distinct vertices for a closed polygon.
    """
    if len(pts) >= 2 and pts[0] == pts[-1]:
        return pts[:-1]
    return pts


def stabilize_region(
    pts: list[tuple[float, float]],
    *,
    gap_tolerance: float = 10.0,
    snap_distance: float = 1.0,
    min_area: float = 100.0,
    max_vertices: int = 5000,
) -> tuple[Optional[list[tuple[float, float]]], Optional[str]]:
    """Stabilize a region's vertex list and validate it for hatch writing.

    Stabilization steps (applied in order):
      1. snap_nearby_endpoints  — remove micro-segments
      2. close_small_gaps       — close near-closed gap if within gap_tolerance
      3. rebuild_closed_polyline — strip duplicate closing vertex

    Validation (applied after stabilization):
      - At least 3 vertices
      - Vertex count ≤ max_vertices
      - Area ≥ min_area
      - Not self-intersecting

    Returns:
        (stabilized_pts, None)   — success; pts is the cleaned vertex list
        (None, rejection_reason) — rejected; reason names the failed check
            Possible reasons: "empty", "too_few_vertices", "too_many_vertices",
                              "too_small", "self_intersecting"
    """
    if not pts:
        return None, "empty"

    # --- Stabilization steps ---
    work = list(pts)
    work = snap_nearby_endpoints(work, snap_distance)
    work = close_small_gaps(work, gap_tolerance)
    work = rebuild_closed_polyline(work)

    # --- Validation ---
    if len(work) < 3:
        return None, "too_few_vertices"

    if len(work) > max_vertices:
        return None, "too_many_vertices"

    area = _shoelace_area(work)
    if area < min_area:
        return None, "too_small"

    if _is_self_intersecting(work):
        return None, "self_intersecting"

    return work, None

"""
tests/test_boundary_tools.py — Phase 6B

Unit tests for geometry/boundary_tools.py.

Covers all 6 public functions:
    detect_almost_closed_polyline
    close_small_gaps
    snap_nearby_endpoints
    merge_fragmented_segments
    rebuild_closed_polyline
    stabilize_region
"""
from __future__ import annotations

import pytest

from cad_site_agent.geometry.boundary_tools import (
    close_small_gaps,
    detect_almost_closed_polyline,
    merge_fragmented_segments,
    rebuild_closed_polyline,
    snap_nearby_endpoints,
    stabilize_region,
)


# ─── detect_almost_closed_polyline ───────────────────────────────────────────


class TestDetectAlmostClosedPolyline:
    def test_returns_true_when_gap_within_tolerance(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 9.5)]
        # gap = dist((0,0), (0,9.5)) = 9.5 ≤ 10.0
        assert detect_almost_closed_polyline(pts, tolerance=10.0) is True

    def test_returns_false_when_gap_exactly_at_tolerance(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
        # gap = dist((0,0), (0,10)) = 10.0; condition is <=, so True
        assert detect_almost_closed_polyline(pts, tolerance=10.0) is True

    def test_returns_false_when_gap_exceeds_tolerance(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 15.0)]
        # gap = 15.0 > 10.0
        assert detect_almost_closed_polyline(pts, tolerance=10.0) is False

    def test_returns_false_when_already_closed(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 0.0)]
        assert detect_almost_closed_polyline(pts, tolerance=10.0) is False

    def test_returns_false_for_fewer_than_3_points(self):
        assert detect_almost_closed_polyline([(0.0, 0.0), (1.0, 0.0)], tolerance=100.0) is False

    def test_returns_false_for_empty(self):
        assert detect_almost_closed_polyline([], tolerance=100.0) is False


# ─── close_small_gaps ────────────────────────────────────────────────────────


class TestCloseSmallGaps:
    def test_drops_last_vertex_when_gap_within_tolerance(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 5.0)]
        # gap = 5.0 ≤ 10.0 → drop last
        result = close_small_gaps(pts, tolerance=10.0)
        assert result == [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]

    def test_unchanged_when_gap_exceeds_tolerance(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 20.0)]
        result = close_small_gaps(pts, tolerance=10.0)
        assert result == pts

    def test_unchanged_when_already_closed(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 0.0)]
        result = close_small_gaps(pts, tolerance=100.0)
        assert result == pts

    def test_unchanged_for_fewer_than_3_points(self):
        pts = [(0.0, 0.0), (1.0, 0.0)]
        assert close_small_gaps(pts, tolerance=100.0) == pts

    def test_drops_last_when_gap_exactly_at_tolerance(self):
        pts = [(0.0, 0.0), (5.0, 0.0), (5.0, 5.0), (0.0, 10.0)]
        # gap = 10.0 = tolerance → drop last
        result = close_small_gaps(pts, tolerance=10.0)
        assert result == [(0.0, 0.0), (5.0, 0.0), (5.0, 5.0)]


# ─── snap_nearby_endpoints ───────────────────────────────────────────────────


class TestSnapNearbyEndpoints:
    def test_removes_vertex_within_snap_distance(self):
        pts = [(0.0, 0.0), (0.5, 0.0), (10.0, 0.0)]
        # (0,0) kept; (0.5,0) dist=0.5 ≤ 1.0 → skipped; (10,0) kept
        result = snap_nearby_endpoints(pts, snap_distance=1.0)
        assert result == [(0.0, 0.0), (10.0, 0.0)]

    def test_keeps_vertex_beyond_snap_distance(self):
        pts = [(0.0, 0.0), (2.0, 0.0), (5.0, 0.0)]
        result = snap_nearby_endpoints(pts, snap_distance=1.0)
        assert result == [(0.0, 0.0), (2.0, 0.0), (5.0, 0.0)]

    def test_always_keeps_first_point(self):
        pts = [(0.0, 0.0), (0.1, 0.0), (0.2, 0.0)]
        result = snap_nearby_endpoints(pts, snap_distance=1.0)
        assert result[0] == (0.0, 0.0)

    def test_single_point_unchanged(self):
        pts = [(3.0, 4.0)]
        assert snap_nearby_endpoints(pts, snap_distance=1.0) == pts

    def test_empty_unchanged(self):
        assert snap_nearby_endpoints([], snap_distance=1.0) == []

    def test_multiple_consecutive_snaps(self):
        pts = [(0.0, 0.0), (0.3, 0.0), (0.6, 0.0), (10.0, 0.0)]
        result = snap_nearby_endpoints(pts, snap_distance=1.0)
        # (0,0) kept; (0.3,0) dist=0.3 skipped; (0.6,0) dist from (0,0)=0.6 skipped; (10,0) kept
        assert result == [(0.0, 0.0), (10.0, 0.0)]


# ─── merge_fragmented_segments ───────────────────────────────────────────────


class TestMergeFragmentedSegments:
    def test_chains_two_segments_end_to_start(self):
        seg1 = [(0.0, 0.0), (5.0, 0.0)]
        seg2 = [(5.0, 0.0), (10.0, 0.0)]
        result = merge_fragmented_segments([seg1, seg2], tolerance=0.1)
        assert result == [(0.0, 0.0), (5.0, 0.0), (10.0, 0.0)]

    def test_reverses_segment_when_needed(self):
        seg1 = [(0.0, 0.0), (5.0, 0.0)]
        seg2 = [(10.0, 0.0), (5.0, 0.0)]  # reversed — tail of seg1 matches end of seg2
        result = merge_fragmented_segments([seg1, seg2], tolerance=0.1)
        assert result == [(0.0, 0.0), (5.0, 0.0), (10.0, 0.0)]

    def test_single_segment_returned_as_list(self):
        seg = [(1.0, 2.0), (3.0, 4.0)]
        result = merge_fragmented_segments([seg], tolerance=0.1)
        assert result == [(1.0, 2.0), (3.0, 4.0)]

    def test_empty_input_returns_empty(self):
        assert merge_fragmented_segments([], tolerance=0.1) == []

    def test_disconnected_remainder_appended(self):
        seg1 = [(0.0, 0.0), (1.0, 0.0)]
        seg2 = [(100.0, 0.0), (200.0, 0.0)]  # disconnected
        result = merge_fragmented_segments([seg1, seg2], tolerance=0.1)
        # seg2 cannot be chained, so appended in order
        assert result[:2] == [(0.0, 0.0), (1.0, 0.0)]
        assert (100.0, 0.0) in result
        assert (200.0, 0.0) in result

    def test_chains_three_segments(self):
        seg1 = [(0.0, 0.0), (5.0, 0.0)]
        seg2 = [(5.0, 0.0), (10.0, 0.0)]
        seg3 = [(10.0, 0.0), (15.0, 0.0)]
        result = merge_fragmented_segments([seg1, seg2, seg3], tolerance=0.1)
        assert result == [(0.0, 0.0), (5.0, 0.0), (10.0, 0.0), (15.0, 0.0)]


# ─── rebuild_closed_polyline ─────────────────────────────────────────────────


class TestRebuildClosedPolyline:
    def test_removes_duplicate_closing_vertex(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 0.0)]
        result = rebuild_closed_polyline(pts)
        assert result == [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]

    def test_unchanged_when_not_closed(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (5.0, 15.0)]
        assert rebuild_closed_polyline(pts) == pts

    def test_single_point_unchanged(self):
        pts = [(1.0, 2.0)]
        assert rebuild_closed_polyline(pts) == pts

    def test_empty_unchanged(self):
        assert rebuild_closed_polyline([]) == []

    def test_two_identical_points_stripped(self):
        pts = [(1.0, 1.0), (1.0, 1.0)]
        result = rebuild_closed_polyline(pts)
        assert result == [(1.0, 1.0)]


# ─── stabilize_region ────────────────────────────────────────────────────────


class TestStabilizeRegion:
    def _square(self):
        """100×100 square — valid, area=10000 ≥ min_area=100."""
        return [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]

    def test_valid_square_passes_all_checks(self):
        pts, reason = stabilize_region(self._square())
        assert reason is None
        assert pts is not None
        assert len(pts) == 4

    def test_empty_list_returns_empty_reason(self):
        pts, reason = stabilize_region([])
        assert pts is None
        assert reason == "empty"

    def test_two_points_rejected_too_few_vertices(self):
        pts, reason = stabilize_region([(0.0, 0.0), (1.0, 0.0)])
        assert pts is None
        assert reason == "too_few_vertices"

    def test_tiny_triangle_rejected_too_small(self):
        # Area = 0.5*10*5 = 25 < 100.0 min_area; vertices far enough apart to survive snap
        pts, reason = stabilize_region(
            [(0.0, 0.0), (10.0, 0.0), (10.0, 5.0)],
            min_area=100.0,
        )
        assert pts is None
        assert reason == "too_small"

    def test_too_many_vertices_rejected(self):
        # 5 well-spaced vertices but max_vertices=3
        pts, reason = stabilize_region(
            [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0), (50.0, 150.0)],
            max_vertices=3,
        )
        assert pts is None
        assert reason == "too_many_vertices"

    def test_gap_close_repair_detected(self):
        # Near-closed square: last vertex close to first but not identical
        pts = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 5.0)]
        # gap from (0,5) to (0,0) = 5.0 ≤ gap_tolerance=10.0 → closed
        result, reason = stabilize_region(pts, gap_tolerance=10.0, min_area=100.0)
        assert reason is None
        assert result is not None
        assert len(result) == 3  # last vertex dropped

    def test_self_intersecting_rejected(self):
        # Asymmetric crossed quadrilateral: edges (0,0)→(100,50) and
        # (100,0)→(0,100) cross at (200/3, 100/3).  Shoelace area ≈ 2500 > 1.
        # Gap from (0,100) to (0,0) = 100 > gap_tolerance=10 → not closed.
        pts = [(0.0, 0.0), (100.0, 50.0), (100.0, 0.0), (0.0, 100.0)]
        result, reason = stabilize_region(pts, min_area=1.0)
        assert result is None
        assert reason == "self_intersecting"

    def test_snap_removes_micro_segment(self):
        # Insert a near-duplicate vertex; stabilize should remove it
        pts = [(0.0, 0.0), (0.3, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
        result, reason = stabilize_region(pts, snap_distance=1.0, min_area=100.0)
        assert reason is None
        assert result is not None
        # (0.3, 0) within snap_distance of (0,0) → removed
        assert (0.3, 0.0) not in result

    def test_already_closed_polygon_passes(self):
        # Explicitly closed (first == last); rebuild strips the duplicate
        pts = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 0.0)]
        result, reason = stabilize_region(pts, min_area=100.0)
        assert reason is None
        assert result is not None
        assert result[0] != result[-1]  # no duplicate closing vertex

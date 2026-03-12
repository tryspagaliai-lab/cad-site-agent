# Phase 6B — Boundary / Polyline Stabilization

## Status: COMPLETE ✓

---

## What Was Built

### New module: `geometry/boundary_tools.py`

Six public functions for polyline geometry stabilization:

| Function | Purpose |
|----------|---------|
| `detect_almost_closed_polyline(pts, tolerance)` | Returns True when first↔last gap ≤ tolerance (and not already closed) |
| `close_small_gaps(pts, tolerance)` | Drops last vertex when gap ≤ tolerance, yielding n distinct vertices |
| `snap_nearby_endpoints(pts, snap_distance)` | Removes consecutive vertices within snap_distance of the previous kept vertex |
| `merge_fragmented_segments(segments, tolerance)` | Chains disconnected polyline segments into one vertex list |
| `rebuild_closed_polyline(pts)` | Strips duplicate closing vertex (first == last) |
| `stabilize_region(pts, *, gap_tolerance, snap_distance, min_area, max_vertices)` | Full pipeline: snap → close_gaps → rebuild → validate |

`stabilize_region` returns `(pts, None)` on success (pts may differ from input = repaired)
or `(None, reason)` on rejection, where reason ∈ `{"empty", "too_few_vertices",
"too_many_vertices", "too_small", "self_intersecting"}`.

### Config: `config/tolerances.yaml` — new `boundary:` section

```yaml
boundary:
  polyline_gap_tolerance: 10.0
  snap_distance: 1.0
  min_region_area: 100.0
  max_region_vertex_count: 5000
```

### Modified: `export/dxf_writer.py`

- Imports and calls `stabilize_region()` per eligible candidate
- Skip reasons keyed as `"stabilize_rejected_<reason>"`
- `write_hatch_dxf()` now returns a **3-tuple**: `(written, skip_reasons, repaired_count)`

### Modified: `export/hatch_writer.py`

- `WriteReport` dataclass gains `stabilization_repaired: int = 0` and `stabilization_rejected: int = 0`
- `run_hatch_write()` unpacks 3-tuple, accepts stabilization kwargs, computes both fields
- JSON report gains `"stabilization": {"repaired": N, "rejected": N}`
- MD report gains a **Stabilization** table section

---

## Tests

- **`tests/test_boundary_tools.py`** — 37 tests across 7 classes, all 6 public functions
- Full suite: **161 passed** (0 failed)

---

## Real-file Stabilization Stats (roman_gardens_gapclosed.dxf, `--status review`)

| Metric | Value |
|--------|-------|
| Input candidates | 1,721 |
| Eligible (status=review) | 300 |
| Written | 289 |
| Stabilization repaired | 13 |
| Stabilization rejected | 11 |

Rejection breakdown:
- `stabilize_rejected_self_intersecting`: 10
- `stabilize_rejected_too_few_vertices`: 1

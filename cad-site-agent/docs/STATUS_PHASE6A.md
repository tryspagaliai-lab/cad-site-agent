# Phase 6A — Region Hatch Writer: Status

**Status:** ✅ Complete
**Date:** 2026-03-12

---

## What Was Built

Phase 6A adds the write leg to the hatch pipeline: given a `hatch_candidates.json`
produced by Phase 4B/5, it writes a new DXF file containing solid HATCH entities
for every eligible candidate.  The source DXF is never modified.

### New modules

| Module | Purpose |
|--------|---------|
| `src/cad_site_agent/export/dxf_writer.py` | Low-level ezdxf helpers: `material_to_layer_name()`, `get_region_points()`, `write_hatch_dxf()` |
| `src/cad_site_agent/export/hatch_writer.py` | Pipeline orchestrator: `filter_eligible()`, `run_hatch_write()`, `write_hatch_write_reports()`, `WriteReport` dataclass |

### CLI command

```
write-hatches <SOURCE_DXF> <CANDIDATES_JSON> <OUTPUT_DXF>
              [--status auto|review|skip]
              [--min-confidence N]
              [--class-filter CLASS]
              [--material-filter MAT]
              [--output-dir DIR]
```

Entry-point registered in `pyproject.toml`:
```
write-hatches = "cad_site_agent.cli:write_hatches"
```

### Output artefacts per run

| File | Description |
|------|-------------|
| `<OUTPUT_DXF>` | New DXF with HATCH entities on `HATCH_<material_class>` layers |
| `<stem>.hatch_write.json` | Write report: totals, skips-by-reason, by-material breakdown |
| `<stem>.hatch_write.md` | Human-readable markdown version of the report |

---

## Filter Pipeline

```
candidates list
  └─ feature_type == "region"          → skip: not_region
      └─ export_role == "hatch_and_export"  → skip: wrong_export_role
          └─ status == <status_filter>      → skip: status_not_auto
              └─ material_class non-empty   → skip: no_material_class
                  └─ confidence >= min_conf → skip: low_confidence  (if set)
                      └─ class_guess match  → skip: class_filtered   (if set)
                          └─ material match → skip: material_filtered (if set)
                              └─ ELIGIBLE ✓
```

---

## Real-file Validation

**File:** `E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf`
**Candidates JSON:** `reports/analysis/roman_gardens_gapclosed.hatch_candidates.json`

| Run | `--status` | Input | Eligible | Written |
|-----|-----------|-------|----------|---------|
| default | `auto` | 1,721 | 0 | 0 |
| with flag | `review` | 1,721 | 300 | 300 |

With `--status auto`: 0 candidates qualify because all real candidates have
`status="review"` (confidence 0.65, below the 0.75 auto threshold).  An empty
DXF is still created and the report notes suggest retrying with `--status review`.

With `--status review`: 300 HATCH entities written across `MAT_LAWN`, `MAT_PATH`,
and other material-class layers.

---

## Test Coverage

32 new Phase 6A tests in `tests/test_hatch_writer.py` and `tests/test_dxf_writer.py`:

| Suite | Tests | What it covers |
|-------|-------|---------------|
| `test_dxf_writer.py` | 12 | `material_to_layer_name`, `get_region_points` (LWPOLYLINE/POLYLINE/missing/unsupported), `write_hatch_dxf` (normal, skip bad handle, empty, layer creation, file creation) |
| `test_hatch_writer.py` | 20 | `filter_eligible` (all filter stages, ordering, accumulation), `run_hatch_write` (file guards, zero-candidate empty DXF, report fields, per-material summary), `write_hatch_write_reports` (JSON schema, MD content, zero-written note, skip table, material table) |

All 124 tests pass (32 new + 92 from Phases 2–5).

---

## Safety Guarantees

- `run_hatch_write` raises `FileNotFoundError` if source DXF or candidates JSON missing
- `run_hatch_write` raises `FileExistsError` if output DXF already exists
- Source DXF is always opened read-only via `ezdxf.readfile()`; never saved
- Output DXF is always created (empty if zero eligible candidates)
- Vertex lookup failures (`get_region_points` returns None) are counted in `vertex_lookup_failed` skip reason, not raised

---

## Known Limitations / Next Steps

- All `roman_gardens_gapclosed.dxf` candidates land in `"review"` status (confidence 0.65 < 0.75 auto threshold). The scoring model may benefit from tuning in a future phase.
- Phase 6B will add SVG / PNG / GeoJSON export from the written HATCH DXF.

# Phase 7 — Non-Region Routing MVP: Status

**Status:** ✅ Complete  
**Date:** 2026-03-12  
**Branch:** (main — worktree committed directly; no active feature branch)

---

## Objective

Route non-region DXF entities (linear, marking, symbol, text, noise) from a
source DXF into a semantically layered output DXF. This is the counterpart to
the Phase 6A hatch pipeline, which handles region (HATCH) entities only.

---

## Deliverables

### New modules

| Module | Description |
|--------|-------------|
| `src/cad_site_agent/export/routing.py` | Central routing engine: `classify_layer_name()`, `run_route_features()`, `write_routing_reports()`, `RoutingReport` dataclass, `DEFAULT_ROUTING_HINTS`, `ROLE_TO_GROUP`, `GROUP_TO_PREFIX` |
| `src/cad_site_agent/export/linework_writer.py` | Thin wrapper: `run_linework_write()` — linework-only routing |
| `src/cad_site_agent/export/marking_writer.py` | Thin wrapper: `run_marking_write()` — markings-only routing |
| `src/cad_site_agent/export/symbol_writer.py` | Thin wrapper: `run_symbol_write()` — symbols-only routing |
| `src/cad_site_agent/export/text_writer.py` | Thin wrapper: `run_text_write()` — text-only routing |

### CLI

New `route-features` command added to `src/cad_site_agent/cli.py`:
- Both click and argparse implementations
- Flags: `--include-linework/--no-linework`, `--include-markings/--no-markings`,
  `--include-symbols/--no-symbols`, `--include-text/--no-text`,
  `--exclude-noise/--keep-noise`, `--output-dir`
- Entry-point stub: `route_features` (for future pyproject.toml registration)

### Tests

`tests/test_routing.py` — 41 new tests across 7 classes:

| Class | Tests | Coverage |
|-------|-------|---------|
| `TestDestinationLayer` | 7 | `destination_layer()` pure function |
| `TestConstants` | 3 | `ROLE_TO_GROUP`, `GROUP_TO_PREFIX` correctness |
| `TestClassifyLayerName` | 9 | Layer name matching, case-insensitive, custom hints, unknown |
| `TestRunRouteFeaturesErrors` | 4 | FileNotFoundError, FileExistsError, source not modified |
| `TestRunRouteFeaturesOutput` | 2 | Output always created, returns RoutingReport |
| `TestRunRouteFeaturesRouting` | 9 | Entity routing, noise removal, group disable, dest layers |
| `TestWriteRoutingReports` | 7 | JSON+MD created, correct keys/totals, dest layer section |

### Documentation

- `docs/01_architecture.md` — updated pipeline diagram, module map, new `RoutingReport` data structure, routing constants table, phase roadmap row
- `docs/02_cli.md` — full `route-features` command reference with examples, output layer table, safety guarantees, thin-wrapper API section, `<stem>.routing.json` schema

---

## Routing Logic

Classification is **layer-name-based** using `DEFAULT_ROUTING_HINTS`:

```python
DEFAULT_ROUTING_HINTS = {
    "fence":            ["fence", "fencing", "hoarding"],
    "wall":             ["wall", "retaining"],
    "kerb":             ["kerb", "curb"],
    "drain":            ["drain", "drainage", "gully"],
    "crossing_marking": ["crossing", "hatching", "zebra"],
    "parking_marking":  ["parking_line", "bay_line"],
    "tree":             ["tree", "planting", "shrub"],
    "bollard":          ["bollard"],
    "gate":             ["gate", "barrier"],
    "signage":          ["sign", "signage"],
    "plot_number":      ["plot", "unit_number"],
    "parking_number":   ["parking_number", "bay_number"],
    "annotation":       ["annotation", "note", "label", "text"],
    "noise":            ["titleblock", "title_block", "ref", "revision"],
}
```

Each classified entity is written to `{PREFIX}_{SEMANTIC_CLASS.upper()}` in the output DXF.

---

## Real-File Smoke Test Results

**Source:** `E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf`  
**Runtime:** 2.82 seconds  

| Metric | Value |
|--------|-------|
| Input entities | 34,655 |
| Written | 4,767 |
| Removed (noise) | 6 |
| Skipped (unknown) | 29,882 |

**By destination layer:**

| Layer | Count |
|-------|-------|
| `LINEWORK_DRAIN` | 10 |
| `LINEWORK_FENCE` | 500 |
| `LINEWORK_KERB` | 12 |
| `LINEWORK_WALL` | 537 |
| `MARKING_CROSSING_MARKING` | 5 |
| `SYMBOL_BOLLARD` | 20 |
| `SYMBOL_GATE` | 287 |
| `SYMBOL_SIGNAGE` | 10 |
| `SYMBOL_TREE` | 2,190 |
| `TEXT_ANNOTATION` | 54 |
| `TEXT_PARKING_NUMBER` | 839 |
| `TEXT_PLOT_NUMBER` | 303 |

The 29,882 skipped/unknown entities are primarily the site's closed LWPOLYLINE
region boundaries (the hatch pipeline's domain), which have no matching routing
keyword. This is expected — region entities are intentionally not routed here.

---

## Test Suite

```
202 passed, 7 warnings in 30.28s
```

All 41 new Phase 7 tests pass. All 161 pre-existing tests remain green.
Warnings are cosmetic ezdxf deprecations unrelated to this codebase.

---

## Known Limitations / Next Steps

1. **Unknown entity volume** — 29,882 entities (84%) unmatched. Most are region
   boundary polylines. A future phase could log layer names of unmatched entities
   to help tune `DEFAULT_ROUTING_HINTS` for specific projects.

2. **Taxonomy-based routing** — `classify_layer_name()` currently uses keyword
   dicts only. A future version could invoke `TaxonomyLoader.classify()` on the
   layer name for richer matching (aliases, plural forms, etc.).

3. **Multi-group output** — `run_route_features()` writes a single output DXF
   with all enabled groups. A future batch wrapper could call it once per group
   to produce separate `LINEWORK_*.dxf`, `SYMBOL_*.dxf`, etc. files.

4. **Region entities** — entities whose layer is classified as `region` type are
   currently skipped (they belong to the hatch pipeline). An explicit "region"
   skip counter could be added to `RoutingReport` for clarity.

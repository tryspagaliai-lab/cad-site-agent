# Phase 4A Status Report

**Date:** 2026-03-10
**Phase:** 4A — Project Scaffold + DXF Analyzer MVP
**Status:** ✅ COMPLETE

---

## What Was Created / Modified

### New Files

| File | Purpose |
|------|---------|
| `src/cad_site_agent/classify/__init__.py` | Package init for new classify module |
| `src/cad_site_agent/classify/drawing_type.py` | New 5-type heuristic classifier |
| `config/settings.yaml` | Global project settings (paths, thresholds, classifier) |
| `config/tolerances.yaml` | Gap-close, cleanup, and hatch tolerances |
| `tests/__init__.py` | Test package init |
| `tests/test_classifier.py` | 14 unit tests for the new classifier (all pass) |
| `tests/test_analyzer.py` | 5 integration tests against real DXF files (all pass) |
| `docs/01_architecture.md` | Architecture overview and module map |
| `docs/02_cli.md` | Full CLI reference with examples |

### Modified Files

| File | Change |
|------|--------|
| `pyproject.toml` | Added `close-gaps` entry point |
| `src/cad_site_agent/cli.py` | New classifier integration, `reports/analysis/` output, `--legacy-cls` / `--legacy` flags |

---

## Test Results

```
$ python -m pytest tests/test_classifier.py -v
14 passed in 0.31s

$ python -m pytest tests/test_analyzer.py -v
5 passed in 29.38s
```

All 19 tests pass.

---

## Real DXF Analysis Results

### roman_gardens_gapclosed.dxf (13 MB)
```
Type: rich_site_layout (75% confidence)
Entities: 34,655 | Layers: 180 | Unit: mm
Closed poly: 2346 | Open poly: 2817
SPLINE: 449 | HATCH: 27 | TEXT+MTEXT: 2016

Reasons:
  - HATCH entities present: 27
  - Rich semantic layer vocabulary (19 site classes): asphalt, boundary, building,
    drain, driveway, fence, footpath, grass, ...
  - Many closed polylines: 2346
  - Block inserts (symbols/trees): 223
```

**Assessment:** Correct. This is a rich site layout DXF with semantic layers and polygon regions.

---

### BDW Eastern Counties - DWH & BH Roman Gardens2.dxf
```
Type: rich_site_layout (75% confidence)
Entities: 38,072 | Layers: 180 | Unit: mm
Closed poly: 1475 | Open poly: 7105
SPLINE: 449 | HATCH: 27 | TEXT+MTEXT: 2016
```

**Assessment:** Correct. Same drawing family as Roman Gardens.

---

### ST-23-01S Planning Layout.dxf
```
Type: max_prep (70% confidence)
Entities: 51,164 | Layers: 1008 | Unit: unknown
Closed poly: 1278 | Open poly: 17,265
SPLINE: 0 | HATCH: 0 | TEXT+MTEXT: 8,208

Reasons:
  - 8 layers with 3D/mesh/material keywords
  - 3D geometry detected (non-default extrusion)
```

**Assessment:** Plausible — 1008 layers, 3D geometry, and 0 HATCH all strongly indicate
a 3ds Max / BIM-derived file. However, this file also has 18 semantic site classes
(score: +0.4) which push rich_site_layout to 0.55, but max_prep wins at 0.70.
**Recommended for Phase 4B review** — may benefit from a tie-breaker heuristic.

---

## Output Structure

```
reports/analysis/
├── roman_gardens_gapclosed.analysis.json     ← full structured report
├── roman_gardens_gapclosed.analysis.md       ← markdown summary
├── BDW Eastern Counties - DWH & BH Roman Gardens2.analysis.json
├── BDW Eastern Counties - DWH & BH Roman Gardens2.analysis.md
├── ST-23-01S Planning Layout.analysis.json
└── ST-23-01S Planning Layout.analysis.md
```

JSON structure:
```json
{
  "analysis": { ... full AnalysisReport ... },
  "classification": {
    "label": "rich_site_layout",
    "confidence": 0.75,
    "reasons": [...],
    "diagnostics": { "spline_count": 449, "hatch_count": 27, ... }
  }
}
```

---

## Known Issues / Blockers

1. **Package install broken** — `pip install -e .` fails: `README.md` missing + `hatchling`
   attribute error. Workaround: `PYTHONPATH=src python -m cad_site_agent.cli ...`
   Fix: create `README.md` and pin `hatchling>=1.18`.

2. **Floating-point tie in classifier** — `0.6 + 0.3 = 0.8999...` vs `0.2+0.35+0.25+0.1 = 0.9000...`.
   Impact: minimal (only affects edge-case inputs that are genuinely ambiguous).
   Fix for Phase 4B: add a scoring tiebreaker that favours the category with the fewest
   competing signals (or use `round(score, 6)` before comparison).

3. **Planning Layout: max_prep vs rich_site_layout ambiguity** — file has both 3D signals
   and 18 semantic site classes. Currently classified as `max_prep` (correct given 1008 layers
   and 3D extrusion). May need per-project config override if this is actually a planning layout.

---

## Recommended Next Step (Phase 4B)

**Target file:** `roman_gardens_gapclosed.dxf`
**Recommended action:** Phase 4B — Hatch Generator

The Roman Gardens file has:
- 2346 closed polylines (ready for hatching)
- 19 semantic classes (rich layer vocabulary to drive hatch patterns)
- 27 existing HATCH entities (can use as reference)

Phase 4B goal: for each closed LWPOLYLINE on a known site-class layer, generate
a matching HATCH entity using the canonical pattern from `layer_aliases.yaml`.

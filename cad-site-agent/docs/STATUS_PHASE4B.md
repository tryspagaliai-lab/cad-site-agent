# Phase 4B — Hatch Candidate MVP: Status

**Status:** ✅ Complete
**Date:** 2025-01-01

---

## What Was Built

Phase 4B adds a closed-region extraction and hatch-candidate classification pipeline
to the existing DXF analysis toolchain.

### New Modules

| Module | Description |
|--------|-------------|
| `hatch/closed_regions.py` | Extracts closed LWPOLYLINE / CIRCLE / SPLINE regions from a DXF file as `ClosedRegion` dataclass objects |
| `hatch/confidence.py` | `score_candidate()` — additive scoring model; returns `(confidence, status, reasons)` |
| `hatch/semantic_hatch.py` | `classify_hatch_candidates()` orchestrator — loads rules, matches layers, scores each region |
| `export/review_writer.py` | `write_hatch_report()` — writes `<stem>.hatch_candidates.json` + `.md` |

### New Config

| File | Description |
|------|-------------|
| `config/hatch_rules.yaml` | Scoring weights, confidence thresholds, class→material map, layer hints, area hints |

### New CLI Command

```
PYTHONPATH=src python -m cad_site_agent.cli hatch-candidates <DXF_FILE>
```

See `docs/02_cli.md` for full option reference.

---

## Test Coverage

**Test file:** `tests/test_hatch.py`
**Result:** 34 / 34 passed

| Test class | Tests | Covers |
|------------|-------|--------|
| `TestGeometryHelpers` | 5 | `_shoelace_area`, `_chord_perimeter`, `_bbox` |
| `TestClosedRegion` | 2 | `ClosedRegion.to_dict()` keys and rounding |
| `TestScoreCandidate` | 7 | Scoring model: auto/review/skip, bonuses, penalties, clamping |
| `TestMatchLayer` | 5 | Layer → class keyword matching, case, ambiguity |
| `TestLayerHasHatch` | 4 | Direct hatch check + family-prefix scan |
| `TestMergeHints` | 3 | Keyword merging, dedup, immutability |
| `TestSummariseCandidates` | 2 | Aggregation counters |
| `TestWriteHatchReport` | 5 | JSON/MD file creation, structure, filenames |
| `TestHatchCandidateToDict` | 1 | Serialisation round-trip |

Run with:
```bash
cd /d E:\cad-site-agent
set PYTHONPATH=E:\cad-site-agent\src
C:\Progra~1\Python310\python.exe -m pytest tests/test_hatch.py -v
```

---

## Real-DXF Validation

**Input:** `E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf`

```
Regions extracted: 1,721
  auto   (≥0.75):    0
  review (0.45–0.74): 343
  skip   (<0.45):  1,378
```

**Top site classes:**

| Class | Count |
|-------|-------|
| unknown | 690 |
| garden | 555 |
| path | 281 |
| building | 55 |
| parking | 44 |
| boundary | 40 |
| driveway | 22 |
| planting | 17 |

**Notes:**
- 0 "auto" candidates is expected — `roman_gardens_gapclosed.dxf` has only 27 HATCH
  entities across 180 layers, so few regions earn the `hatch_in_layer_family` (+0.15)
  bonus needed to push a strong-layer-signal (0.45) + area-match (0.20) score past 0.75.
- The high "unknown" count (690) reflects regions on non-semantic layers (e.g. grid,
  reference, survey). These are correctly skipped.

---

## Known Limitations / Next Steps

| Item | Priority | Notes |
|------|----------|-------|
| 0 auto candidates on roman_gardens | P2 | Expected; consider lowering `auto` threshold or adding more `layer_hints` |
| No CIRCLE / ELLIPSE extraction yet | P3 | `closed_regions.py` handles LWPOLYLINE + SPLINE only |
| Phase 5 — Layer Normaliser | P1 | Will feed canonical class names → improve layer matching recall |
| Phase 6 — DXF hatch export | P1 | Write `HATCH` entities back to a new DXF layer |

---

## Scoring Model Reference

Additive, independent signals per candidate:

| Signal | Value | Condition |
|--------|-------|-----------|
| `strong_layer_signal` | +0.45 | Layer name matches a known site class keyword |
| `hatch_in_layer_family` | +0.15 | Layer (or same-prefix family) already contains HATCH entities |
| `shape_heuristic_match` | +0.20 | Region area falls within class-specific expected range |
| `suspicious_size_penalty` | −0.15 | Region area outside expected range for class |
| `ambiguous_overlap_penalty` | −0.20 | Layer name matches keywords of 2+ distinct classes |

Score is clamped to [0.0, 1.0].
Thresholds: **auto ≥ 0.75**, **review ≥ 0.45**, **skip < 0.45**.

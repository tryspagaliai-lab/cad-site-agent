# Phase 5 — Semantic Taxonomy Extension

**Status:** Complete
**Date:** 2026-03-11

## What Was Built

Extended the site-plan semantic model beyond hatch regions. Every `HatchCandidate`
now carries a `SemanticLabel` with four fields that control downstream routing.

## New Files

| File | Purpose |
|------|---------|
| `config/semantic_taxonomy.yaml` | Canonical class taxonomy: 5 feature types, 40+ classes, aliases |
| `config/export_roles.yaml` | 7 export roles + default-by-type mapping |
| `src/cad_site_agent/semantic/taxonomy.py` | `SemanticLabel` dataclass + `TaxonomyLoader` |
| `tests/test_taxonomy.py` | Unit tests for taxonomy module |

## Modified Files

| File | Change |
|------|--------|
| `src/cad_site_agent/hatch/semantic_hatch.py` | Added `semantic_label` field to `HatchCandidate`, wired `TaxonomyLoader` |
| `tests/test_hatch.py` | Updated `TestHatchCandidateToDict`, added `TestClassifyHatchCandidatesTaxonomy` |

## Semantic Model

```
feature_type   semantic_class    export_role         material_class
─────────────  ────────────────  ──────────────────  ──────────────
region         building          hatch_and_export    MAT_BUILDING
region         parking_bay       hatch_and_export    MAT_PARKING
linear         wooden_fence      keep_linework       (empty)
marking        parking_lines     keep_markings       (empty)
symbol         trees             keep_symbols        (empty)
text           labels            keep_text           (empty)
unknown        unknown           review              (empty)
```

## Backward Compatibility

- `HatchCandidate.class_guess` and `.hatch_class` unchanged
- New `semantic_label` field defaults to `SemanticLabel.unknown()` — all
  existing callers that don't pass taxonomy config continue to work
- `classify_hatch_candidates()` falls back to `SemanticLabel.unknown()` if
  taxonomy YAML files are missing

## Next Phase

Phase 6 will use `export_role` to route features:
- `hatch_and_export` → generate DXF HATCH + export region mesh to 3ds Max
- `keep_linework` → export to Illustrator vector layer
- `keep_symbols` → resolve symbol library + place in Illustrator

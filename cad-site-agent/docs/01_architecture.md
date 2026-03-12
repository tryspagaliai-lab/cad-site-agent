# CAD Site Agent — Architecture

## Overview

CAD Site Agent is a Python pipeline that ingests DXF files (site layout drawings),
analyses their geometry and layer structure, classifies their type, extracts
closed regions as hatch candidates, and produces structured JSON + Markdown reports.

```
DXF File
   │
   ├──────────────────────────────────────────────┐
   ▼                                              ▼
[analyzer/dxf_analyzer.py]   ← Phase 2    [hatch/closed_regions.py]  ← Phase 4B
   │  AnalysisReport                              │  list[ClosedRegion]
   ▼                                              │
[classify/drawing_type.py]   ← Phase 4A          ▼
│   OR                                    [hatch/confidence.py]
[analyzer/drawing_classifier.py] (legacy)         │  score per region
   │  DrawingTypeResult                           ▼
   ▼                                     [hatch/semantic_hatch.py]
[cli.py]  write_json + write_md                   │  list[HatchCandidate]
   │                                              ▼
   ▼                                     [export/review_writer.py]
reports/analysis/<stem>.analysis.json             │
reports/analysis/<stem>.analysis.md               ▼
                                         reports/analysis/<stem>.hatch_candidates.json
                                         reports/analysis/<stem>.hatch_candidates.md
                                                  │
                                                  ▼  ← Phase 6A
                                         [export/hatch_writer.py]
                                         [export/dxf_writer.py]
                                                  │  WriteReport
                                                  ▼
                                         <stem>.hatches_<status>.dxf  (new DXF, HATCH entities)
                                         reports/analysis/<stem>.hatch_write.json
                                         reports/analysis/<stem>.hatch_write.md
```

---

## Module Map

```
cad_site_agent/
├── cli.py                      Entry-point dispatcher (click + argparse fallback)
├── analyzer/
│   ├── dxf_analyzer.py         Phase 2: reads DXF, produces AnalysisReport
│   ├── drawing_classifier.py   Legacy classifier (4 types)
│   └── report_writer.py        Legacy JSON/MD writer (PNG preview only kept)
├── classify/
│   └── drawing_type.py         Phase 4A: new 5-type drawing classifier
├── gap_closer/                 Phase 3: gap-close / bridge / snap
├── hatch/
│   ├── __init__.py
│   ├── closed_regions.py       Phase 4B: extract ClosedRegion polys from DXF
│   ├── confidence.py           Phase 4B: score_candidate() → (float, str, reasons)
│   └── semantic_hatch.py       Phase 4B: classify_hatch_candidates() orchestrator
├── export/
│   ├── review_writer.py        Phase 4B: write_hatch_report() → JSON + MD
│   ├── hatch_writer.py         Phase 6A/6B: run_hatch_write() pipeline + WriteReport
│   └── dxf_writer.py           Phase 6B: material_to_layer_name(), write_hatch_dxf()
│                               (stabilize_region integrated; 3-tuple return)
├── geometry/
│   ├── __init__.py
│   └── boundary_tools.py       Phase 6B: polyline stabilization (snap, gap-close,
│                               rebuild, merge, self-intersection check)
├── semantic/
│   ├── normalizer.py           Pre-Phase 5: layer name normalisation helpers
│   └── taxonomy.py             Phase 5: SemanticLabel dataclass + TaxonomyLoader
└── layer_normaliser/           Future phase

config/
├── settings.yaml               Global settings (paths, thresholds)
├── tolerances.yaml             Gap-close, cleanup, and boundary stabilization tolerances
├── layer_aliases.yaml          Layer name → canonical class mapping
├── hatch_rules.yaml            Phase 4B: scoring weights, class→material map, layer hints
├── semantic_taxonomy.yaml      Phase 5: 40+ canonical site classes, 5 feature types, aliases
└── export_roles.yaml           Phase 5: 7 export roles + default-by-type mapping

reports/
└── analysis/                   All output files (flat, <stem>.analysis.{json,md})
```

---

## Core Data Structures

### `AnalysisReport` (`analyzer/dxf_analyzer.py`)

| Field | Type | Description |
|-------|------|-------------|
| `source_file` | str | Absolute path to the DXF |
| `total_entities` | int | Total entity count across all spaces |
| `entity_type_counts` | dict[str, int] | Counts by entity type (LINE, HATCH, etc.) |
| `total_layers` | int | Layer count |
| `layers` | dict[str, LayerInfo] | Per-layer statistics |
| `has_hatches` / `has_splines` / `has_3d` | bool | Presence flags |
| `closed_polyline_count` | int | Closed LWPOLYLINE count |
| `extents_min/max` | tuple[float,float,float] | Drawing bounding box |

### `DrawingTypeResult` (`classify/drawing_type.py`)

| Field | Type | Description |
|-------|------|-------------|
| `label` | str | One of the 5 type labels |
| `confidence` | float | 0.0 – 1.0 heuristic score |
| `reasons` | list[str] | Human-readable evidence |
| `spline_count` / `hatch_count` / `insert_count` | int | Diagnostic counts |
| `semantic_class_count` | int | Unique site-class keywords in layer names |

### `ClosedRegion` (`hatch/closed_regions.py`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Sequential region index |
| `source_layer` | str | DXF layer name of the source entity |
| `handle` | str | DXF entity handle |
| `area` | float | Polygon area in mm² (Shoelace formula) |
| `perimeter` | float | Chord-sum perimeter |
| `bbox` | tuple[float,float,float,float] | (xmin, ymin, xmax, ymax) |
| `vertex_count` | int | Number of vertices |
| `is_closed` | bool | Always True for extracted regions |
| `source_type` | str | e.g. `"LWPOLYLINE"`, `"CIRCLE"` |

### `HatchCandidate` (`hatch/semantic_hatch.py`)

| Field | Type | Description |
|-------|------|-------------|
| `region` | ClosedRegion | The source polygon |
| `class_guess` | str | e.g. `"parking"`, `"building"`, `"unknown"` |
| `hatch_class` | str | e.g. `"MAT_PARKING"`, `"REVIEW_UNKNOWN"` |
| `confidence` | float | 0.0 – 1.0 additive score |
| `status` | str | `"auto"` (≥0.75) \| `"review"` (≥0.45) \| `"skip"` |
| `reasons` | list[str] | Human-readable scoring evidence |
| `semantic_label` | SemanticLabel | Phase 5: feature_type, semantic_class, export_role, material_class |

### `WriteReport` (`export/hatch_writer.py`) — Phase 6A

| Field | Type | Description |
|-------|------|-------------|
| `source_dxf` | str | Path to the source DXF |
| `candidates_json` | str | Path to the input candidates JSON |
| `output_dxf` | str | Path to the written output DXF |
| `generated_at` | str | ISO-8601 timestamp |
| `total_input` | int | Total candidates in JSON |
| `total_eligible` | int | Candidates passing all filters |
| `total_written` | int | HATCH entities successfully written |
| `total_skipped` | int | `total_input - total_eligible` |
| `skips_by_reason` | dict[str, int] | Counts per skip reason (filter stage + write stage) |
| `by_material` | dict[str, dict] | Per-material `{ layer, eligible }` breakdown |

---

## Drawing Type Taxonomy

| Label | Signal | Example files |
|-------|--------|---------------|
| `rich_site_layout` | Many HATCH + semantic layers (parking, grass, boundary…) | Roman Gardens |
| `sparse_linework` | High LINE ratio, no hatch, no semantic layers | Draft / outline DXFs |
| `illustrator_derived` | High SPLINE count or ratio (>5%) | AI / Illustrator exports |
| `max_prep` | Material/mesh/3D layer names OR has_3d geometry | ST-23-01S Planning Layout |
| `unknown` | Score < 0.25 across all categories | Minimal / corrupted files |

Scoring is additive and independent per category. The category with the highest
score above `THRESHOLD = 0.25` wins.

---

## Config Files

### `config/settings.yaml`
```yaml
paths:
  reports_dir: "reports/analysis"
  raw_data_dir: "E:/SHAKESPEARE/RAW_DATA"
analysis:
  max_text_sample: 50
  default_preview: false
classification:
  confidence_threshold: 0.25
  active_classifier: "new"   # "new" or "legacy"
```

### `config/tolerances.yaml`
```yaml
gap_close:
  tolerance: 1000.0    # mm (= 1m) — max gap to close
  bridge_max: 5000.0   # mm — max gap to insert bridge line
cleanup:
  snap_tolerance: 1.0  # mm — node snap distance
  min_segment_length: 0.5
hatch:
  min_area: 100.0      # mm² — skip tiny slivers
  pattern: SOLID
```

### `config/hatch_rules.yaml`
```yaml
thresholds:
  auto:   0.75   # score >= auto   → "auto"   (proceed without review)
  review: 0.45   # score >= review → "review" (human check needed)
scoring:
  strong_layer_signal:       0.45   # layer name matches a known site class
  hatch_in_layer_family:     0.15   # layer already has HATCH entities
  shape_heuristic_match:     0.20   # area fits expected range for class
  suspicious_size_penalty:  -0.15   # area outside expected range
  ambiguous_overlap_penalty: -0.20  # layer matches multiple classes
class_to_material:
  building: MAT_BUILDING
  parking:  MAT_PARKING
  path:     MAT_PATH
  garden:   MAT_LAWN
  driveway: MAT_DRIVEWAY
  unknown:  REVIEW_UNKNOWN
layer_hints:
  building: ["building", "bldg", "struct", "wall"]
  parking:  ["parking", "carpark", "car-park", "bay"]
  path:     ["footpath", "path", "pavement", "paving"]
  garden:   ["garden", "lawn", "turf", "grass"]
  driveway: ["driveway", "asphalt", "tarmac"]
area_hints:           # mm² expected range per class
  parking:  {min: 6000, max: 500000}
  building: {min: 5000, max: 5000000}
  path:     {min: 500,  max: 200000}
```

---

## Phase Roadmap

| Phase | Status | What it adds |
|-------|--------|--------------|
| 0 — Inventory | ✅ Complete | `docs/00_inventory.md`, package discovery |
| 1 — Scaffold | ✅ Complete | `pyproject.toml`, `src/` layout, entry points |
| 2 — Analyzer | ✅ Complete | `dxf_analyzer.py`, `report_writer.py` |
| 3 — Gap Closer | ✅ Complete | `gap_closer/` module |
| 4A — Classifier | ✅ Complete | `classify/drawing_type.py`, new CLI flags |
| 4B — Hatch Gen | ✅ Complete | `hatch/` + `export/`: closed-region scoring + hatch candidate reports |
| 5 — Semantic Taxonomy | ✅ Complete | `semantic/taxonomy.py`: SemanticLabel + TaxonomyLoader; `config/semantic_taxonomy.yaml` + `export_roles.yaml` |
| 6A — Hatch Writer | ✅ Complete | `export/hatch_writer.py` + `export/dxf_writer.py`: filter eligible candidates, write HATCH DXF, WriteReport |
| 6B — Export | 🔜 Future | SVG / PNG / GeoJSON export |

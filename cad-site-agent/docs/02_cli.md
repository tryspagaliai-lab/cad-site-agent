# CAD Site Agent — CLI Reference

## Installation

```bash
# Editable install (requires hatchling + README.md)
pip install -e .

# OR run directly with PYTHONPATH:
PYTHONPATH=src python -m cad_site_agent.cli <command> [args]
```

---

## Commands

### `analyze-dxf`

Analyse a DXF file and write a JSON + Markdown report to `reports/analysis/`.

```
analyze-dxf <DXF_FILE> [--output DIR] [--preview] [--legacy-cls]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output DIR` | `reports/analysis/` | Override output directory |
| `--preview` | off | Render a PNG preview via matplotlib |
| `--legacy-cls` | off | Use old 4-type classifier instead of new 5-type |

**Output files:**
- `<stem>.analysis.json` — full structured report with classification
- `<stem>.analysis.md` — human-readable markdown summary

**Example:**
```bash
PYTHONPATH=src python -m cad_site_agent.cli analyze-dxf \
  "E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf"
```
```
Analysing: E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf
  JSON  -> reports\analysis\roman_gardens_gapclosed.analysis.json
  MD    -> reports\analysis\roman_gardens_gapclosed.analysis.md

  Type: rich_site_layout (75% confidence)
  Entities: 34,655 | Layers: 180 | Unit: mm
  Closed poly: 2346 | Open poly: 2817
  SPLINE: 449 | HATCH: 27 | TEXT+MTEXT: 2016
```

---

### `classify-drawing`

Classify a DXF file's drawing type without writing a full report.

```
classify-drawing <DXF_FILE> [--legacy]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--legacy` | off | Use old 4-type classifier |

**Example:**
```bash
PYTHONPATH=src python -m cad_site_agent.cli classify-drawing \
  "E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf"
```
```
Classifying: E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf

  Label:       rich_site_layout
  Confidence:  75.0%
  Reason:  HATCH entities present: 27
  Reason:  Rich semantic layer vocabulary (19 site classes): asphalt, boundary, ...
  Reason:  Many closed polylines: 2346
  Reason:  Block inserts (symbols/trees): 223

  SPLINE:449  HATCH:27  INSERT:223  SemanticClasses:19
```

---

### `export-report`

Export a previously-generated JSON analysis as JSON, Markdown, or both.

```
export-report <JSON_FILE> [--format json|md|all] [--output DIR] [--preview]
```

---

### `clean-dxf`

Remove duplicate entities, snap near-coincident nodes, and drop micro-segments.

```
clean-dxf <DXF_FILE> [--output FILE] [--snap-tol N] [--min-len N]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output FILE` | `<stem>_cleaned.dxf` | Output DXF path |
| `--snap-tol N` | `1.0` | Snap radius in drawing units |
| `--min-len N` | `0.5` | Minimum segment length |

---

### `close-gaps`

Attempt to close small gaps between line/polyline endpoints.

```
close-gaps <DXF_FILE> [--output FILE] [--tol N] [--no-bridge] [--same-layer]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output FILE` | `<stem>_gapclosed.dxf` | Output DXF path |
| `--tol N` | `1000.0` | Maximum gap to close (drawing units) |
| `--no-bridge` | off | Disable bridge-line insertion |
| `--same-layer` | off | Only close gaps on the same layer |

---

### `hatch-candidates`

Extract closed regions from a DXF file, classify each against site classes, score
confidence, and write a hatch-candidate report to `reports/analysis/`.

```
hatch-candidates <DXF_FILE> [--output DIR] [--rules FILE] [--aliases FILE]
                             [--filter CLASS] [--min-area N] [--max-vertices N]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output DIR` | `reports/analysis/` | Override output directory |
| `--rules FILE` | `config/hatch_rules.yaml` | Scoring rules override |
| `--aliases FILE` | `config/layer_aliases.yaml` | Layer alias hints override |
| `--filter CLASS` | (all) | Only return candidates for this site class |
| `--min-area N` | `100.0` | Minimum region area in mm² |
| `--max-vertices N` | `5000` | Skip regions with more vertices than this |

**Output files:**
- `<stem>.hatch_candidates.json` — full candidate list with scoring details
- `<stem>.hatch_candidates.md`  — human-readable summary tables

**Example:**
```bash
PYTHONPATH=src python -m cad_site_agent.cli hatch-candidates \
  "E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf"
```
```
Hatch candidates: E:/SHAKESPEARE/RAW_DATA/roman_gardens_gapclosed.dxf
  Regions found: 1721
  Auto (≥0.75):   0
  Review (0.45–0.74): 343
  Skip (<0.45):  1378

  JSON -> reports\analysis\roman_gardens_gapclosed.hatch_candidates.json
  MD   -> reports\analysis\roman_gardens_gapclosed.hatch_candidates.md
```

**Status values:**

| Status | Threshold | Meaning |
|--------|-----------|---------|
| `auto` | score ≥ 0.75 | High confidence — can be applied without review |
| `review` | score ≥ 0.45 | Moderate confidence — needs human verification |
| `skip` | score < 0.45 | Low confidence — excluded from output by default |

---

### `normalize-layers`

Map layer names to canonical site classes using `config/layer_aliases.yaml`.

```
normalize-layers <DXF_FILE> [--config FILE] [--output FILE]
```

---

## JSON Report Structure

### `<stem>.analysis.json`

```json
{
  "analysis": {
    "source_file": "...",
    "total_entities": 34655,
    "entity_type_counts": { "LINE": 23094, "HATCH": 27, ... },
    "total_layers": 180,
    "layers": { "CB-P-PARKING": { "entity_count": 44, ... }, ... },
    "has_hatches": true,
    "closed_polyline_count": 2346,
    ...
  },
  "classification": {
    "label": "rich_site_layout",
    "confidence": 0.75,
    "reasons": [...],
    "diagnostics": {
      "spline_count": 449,
      "hatch_count": 27,
      "insert_count": 223,
      "semantic_class_count": 19
    }
  }
}
```

### `<stem>.hatch_candidates.json`

```json
{
  "meta": {
    "source_file": "...",
    "generated_at": "2025-01-01T12:00:00",
    "total_regions": 1721
  },
  "summary": {
    "total": 1721,
    "by_status": { "auto": 0, "review": 343, "skip": 1378 },
    "by_class": { "unknown": 690, "garden": 555, "path": 281, ... },
    "top_layers": { "CB-GRASS": 210, "CB-PATH": 180, ... }
  },
  "candidates": [
    {
      "region": {
        "id": 0, "source_layer": "CB-P-PARKING",
        "area": 48200.0, "perimeter": 920.0,
        "bbox": [100.0, 200.0, 380.0, 330.0],
        "vertex_count": 8, "is_closed": true, "source_type": "LWPOLYLINE"
      },
      "class_guess": "parking",
      "hatch_class": "MAT_PARKING",
      "confidence": 0.65,
      "status": "review",
      "reasons": ["Layer name matches class 'parking'", "Area 48200mm² in expected parking range"]
    }
  ]
}
```

---

## Drawing Type Labels

| Label | Description |
|-------|-------------|
| `rich_site_layout` | Semantic site DXF with hatches, closed regions, many classes |
| `sparse_linework` | Draft DXF: lots of LINE/LWPOLYLINE, few semantics, no hatch |
| `illustrator_derived` | Exported from Illustrator: high SPLINE count |
| `max_prep` | 3ds Max prep/model: material/mesh/3D layer names, 3D geometry |
| `unknown` | Insufficient signal (score < 0.25) |

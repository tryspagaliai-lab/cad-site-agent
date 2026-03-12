# CAD Site Agent

A Python pipeline for processing DXF site layout drawings — classify geometry,
extract closed regions as HATCH entities, and route linework/symbols/text to
semantic output layers.

## Installation

```bash
# Editable install (Python ≥ 3.10, hatchling)
pip install -e .

# Or run without installing (set PYTHONPATH)
set PYTHONPATH=src          # Windows
export PYTHONPATH=src       # Linux/macOS
```

## Quick Start — Single Command

```bash
cad-agent process input.dxf output.dxf
```

This runs the full pipeline and produces four output files alongside `output.dxf`.

## Pipeline Stages

| Stage | Description | Module |
|-------|-------------|--------|
| 1. Hatch Candidates | Extract closed regions, score by area/confidence | `hatch_extractor` |
| 2. Hatch Writer | Write HATCH entities to DXF, stabilise boundaries | `hatch_writer` |
| 3. Route Features | Classify non-region entities, copy to semantic layers | `routing` |

### Output Files

Given `cad-agent process input.dxf output/result.dxf`:

| File | Contents |
|------|----------|
| `output/result.dxf` | Routed linework, markings, symbols, text |
| `output/result.hatches.dxf` | HATCH entities for closed regions |
| `output/result.hatch_candidates.json` | Candidate metadata |
| `output/result.process.json` | Pipeline run summary |

## CLI Reference

### `cad-agent process`

```
cad-agent process SOURCE_DXF OUTPUT_DXF [OPTIONS]

  Run the full end-to-end pipeline.

Options:
  --status [auto|review]  Candidate filter  [default: auto]
  --min-confidence FLOAT  Minimum candidate confidence (0–1)
  --keep-noise            Include noise entities (titleblock, notes, etc.)
  --help                  Show this message and exit.
```

### Individual Commands

| Command | Description |
|---------|-------------|
| `analyze-dxf INPUT` | Full DXF analysis → JSON + Markdown report |
| `classify-drawing INPUT` | Drawing type classification (5 types) |
| `clean-dxf INPUT` | Remove duplicates, snap nodes, micro-segments |
| `close-gaps INPUT` | Bridge small endpoint gaps |
| `normalize-layers INPUT` | Map layer names to canonical semantic classes |
| `hatch-candidates INPUT` | Extract closed regions and score as hatch candidates |
| `write-hatches INPUT CANDIDATES OUTPUT` | Write HATCH DXF from candidate JSON |
| `route-features INPUT CANDIDATES OUTPUT` | Route non-region entities to semantic layers |

## Example

See `examples/roman_gardens/` for a complete walkthrough on a real site layout DXF.

```bash
cd examples/roman_gardens
run.bat           # Windows
bash run.sh       # Linux/macOS
```

## Development

```bash
set PYTHONPATH=src
py -3.10 -m pytest tests/ -v
```

## Phase Status

| Phase | Status | Description |
|-------|--------|-------------|
| 0 — Inventory | ✅ | Package discovery |
| 1 — Scaffold | ✅ | pyproject.toml, src/ layout, entry points |
| 2 — Analyzer | ✅ | DXF geometry and layer analysis |
| 3 — Gap Closer | ✅ | Gap-close / bridge / snap pipeline |
| 4A — Classifier | ✅ | 5-type drawing classifier |
| 4B — Hatch Gen | ✅ | Closed-region extraction and scoring |
| 5 — Layer Norm | ✅ | Canonical class assignment via taxonomy |
| 6 — Hatch Write | ✅ | HATCH DXF writer with boundary stabilisation |
| 7 — Route Features | ✅ | Non-region entity routing to semantic layers |
| 7.5 — v1 Release | ✅ | Single `process` command, example project |

# CAD Site Agent

A Python pipeline for ingesting DXF site layout drawings, analysing geometry and
layer structure, classifying drawing type, extracting closed regions as hatch
candidates, and producing structured JSON + Markdown reports.

## Installation

```bash
# Editable install (requires Python ≥ 3.10 with hatchling)
pip install -e .

# OR run without installing (set PYTHONPATH instead):
set PYTHONPATH=src   # Windows cmd
python -m cad_site_agent.cli <command> [args]
```

## Quick Start

```bash
# Analyse a DXF file
python -m cad_site_agent.cli analyze-dxf "path/to/drawing.dxf"

# Classify drawing type only
python -m cad_site_agent.cli classify-drawing "path/to/drawing.dxf"

# Close gaps in linework
python -m cad_site_agent.cli close-gaps "path/to/drawing.dxf"

# Extract and score hatch candidates
python -m cad_site_agent.cli hatch-candidates "path/to/drawing.dxf"
```

## Commands

| Command | Description |
|---------|-------------|
| `analyze-dxf` | Full DXF analysis → JSON + MD report |
| `classify-drawing` | Drawing type classification (5 types) |
| `export-report` | Re-export a previously generated JSON report |
| `clean-dxf` | Remove duplicates, snap nodes, drop micro-segments |
| `close-gaps` | Close small gaps between line/polyline endpoints |
| `normalize-layers` | Map layer names to canonical site classes |
| `hatch-candidates` | Extract closed regions and score as hatch candidates |

See `docs/02_cli.md` for full option reference.

## Documentation

- `docs/00_inventory.md` — Initial file inventory
- `docs/01_architecture.md` — System architecture and data structures
- `docs/02_cli.md` — CLI command reference
- `docs/STATUS_PHASE4B.md` — Phase 4B (hatch candidates) status and test results

## Development

```bash
# Run tests (requires Python 3.10 with pytest installed)
set PYTHONPATH=src
python -m pytest tests/ -v
```

## Phase Status

| Phase | Status | Description |
|-------|--------|-------------|
| 0 — Inventory | ✅ | Package discovery and inventory |
| 1 — Scaffold | ✅ | pyproject.toml, src/ layout, entry points |
| 2 — Analyzer | ✅ | DXF analysis and report writing |
| 3 — Gap Closer | ✅ | Gap-close / bridge / snap pipeline |
| 4A — Classifier | ✅ | 5-type drawing classifier |
| 4B — Hatch Gen | ✅ | Closed-region extraction and hatch candidate scoring |
| 5 — Layer Norm | 🔜 | Canonical class assignment |
| 6 — Export | 🔜 | SVG / PNG / GeoJSON export |

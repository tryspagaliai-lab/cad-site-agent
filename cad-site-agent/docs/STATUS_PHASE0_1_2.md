# Status Report — Phase 0 + 1 + 2 MVP
**Date:** 2026-03-10

---

## ✅ PHASE 0 — Inventory COMPLETE

### What was found:
- **Python 3.10.11** (default PATH) — heavy env but has all needed libs: ezdxf, shapely, networkx, scipy, numpy, matplotlib, pillow, click, pydantic, PyYAML, trimesh
- **Python 3.12** (clean) — also has key libs + rtree (spatial index), but no click
- **ezdxf 1.4.3** available in both envs — sufficient for all DXF work
- **4 DXF files** in `E:\SHAKESPEARE\RAW_DATA\` (14–90 MB)
- **~30 existing scripts** in `E:\` — analysed and catalogued; best patterns noted for reuse
- **autocad-mcp** installed at `C:\Users\zilva\mcp-servers\autocad-mcp` (v3.0.0)
- **uv 0.10.2** available globally
- **No install needed** for Phases 0–5 MVP

### Deliverables:
- `docs/00_inventory.md` ✅
- `reports/inventory/python_envs.json` ✅
- `reports/inventory/cad_assets.json` ✅
- `reports/inventory/libraries.json` ✅

---

## ✅ PHASE 1 — Project Scaffold COMPLETE

```
E:\cad-site-agent\
├── pyproject.toml
├── config/
│   ├── layer_aliases.yaml     ← 50+ rules, 12 semantic classes
│   └── export_layers.yaml     ← MAX-prep layer schema
├── src/cad_site_agent/
│   ├── cli.py                 ← click + argparse fallback
│   ├── analyzer/
│   │   ├── dxf_analyzer.py    ← AnalysisReport, entity scan, extents
│   │   ├── drawing_classifier.py ← DrawingClassification
│   │   └── report_writer.py   ← JSON + Markdown + PNG preview
│   ├── cleanup/
│   │   └── cleaner.py         ← short seg removal, dup detect, endpoint snap
│   ├── semantic/
│   │   └── normalizer.py      ← YAML rule engine, layer renaming
│   ├── topology/              ← Phase 5 (stub)
│   ├── export/                ← Phase 6 (stub)
│   └── utils/                 ← shared helpers (stub)
├── docs/
│   ├── 00_inventory.md
│   └── STATUS_PHASE0_1_2.md
├── reports/
│   ├── inventory/*.json
│   └── analysis/              ← generated reports
└── scripts/
    ├── analyze_all.py
    └── run_analysis.bat
```

---

## ✅ PHASE 2 — DXF Analyzer MVP COMPLETE

### Analysis results on all 4 DXF files:

| File | Type | Confidence | Entities | Layers | Unit |
|------|------|-----------|---------|--------|------|
| BDW Roman Gardens2 | site_layout | 90% | 38,072 | 180 | mm |
| ST-23-01S Planning Layout | planning_layout | 70% | 51,164 | 1,008 | unknown |
| parking_rotated | site_layout | 90% | 38,072 | 180 | mm |
| parking_hatched | site_layout | 90% | 38,197 | 183 | mm |

### Analyzer detects:
- ✅ Entity type counts (global + per-layer)
- ✅ Layer inventory with linetype/color
- ✅ Text/MTEXT extraction (2016 text entries in Roman Gardens)
- ✅ Extents (bbox from LINE + LWPOLYLINE)
- ✅ Unit heuristic (mm vs m)
- ✅ Hatch, block, spline, 3D presence
- ✅ Closed vs open polyline count (1475 closed, 7105 open in primary file)
- ✅ JSON + Markdown report output

### Key finding — Roman Gardens:
- 1,475 closed polylines (hatchable)
- 7,105 open polylines (need gap-closing in Phase 3)
- 2,016 text entities
- Already has hatches (from add_hatch.py work)

### Key finding — ST-23-01S:
- 1,008 layers — xref-heavy or multi-discipline drawing
- 0 hatches, 17,265 open polylines
- Unit "unknown" (extents too ambiguous to guess)
- Needs separate xref/block analysis pass

---

## ✅ Semantic Layer Normalizer — TESTED

Rule engine working. Test on primary DXF layer names:

| Original | Canonical |
|---------|-----------|
| FCS-GRASS | planting |
| FCS-PATH | path |
| FCS-DRIVEWAY | driveway |
| FCS-BLOCK PAVING-GREY | path |
| FCS-HOGGIN | path |
| BBS-EX-ASPHALT | driveway |
| FCS-PARKING-NO | parking |
| SITE BOUNDARY | boundary |
| TREE PLANTING | planting |
| ROAD KERB | road |
| DIMENSION | annotation |
| NORTH POINT | symbols |
| ZZZMYSTERY-LAYER | unknown |

---

## Risks

| Risk | Severity | Notes |
|------|---------|-------|
| 7,105 open polylines | HIGH | Core problem. Phase 3 cleanup critical. |
| ST-23-01S unit=unknown | MEDIUM | Extents too large/small to auto-detect — manual check needed |
| ST-23-01S 1008 layers | MEDIUM | Likely xrefs. Normalizer will hit many 'unknown' — need rule expansion |
| `dxf_analyzer` bbox misses POLYLINE verts | LOW | POLYLINE (vs LWPOLYLINE) vertices not added to bbox yet |
| preview render slow on 90MB file | LOW | Defer or add sampling |

---

## Next Step — PHASE 3: Cleanup MVP

**Goal:** Gap-close open polylines to make them hatchable.

**Plan:**
1. `cleanup/gap_closer.py` — find open LWPOLYLINE endpoints within tolerance, snap
2. `cleanup/cleaner.py` already has: short segment removal, duplicate detection, KD-tree endpoint snap
3. Test on Roman Gardens: try to close some of the 7,105 open polylines
4. Re-run hatch generation after cleanup

**Suggested tolerance:** 1–5mm (drawing units, so 1000–5000 in file units since mm DXF)

---

## Commands Available

```bash
# From E:\cad-site-agent\
python scripts/analyze_all.py                  # analyse all 4 DXF files
python -m src.cad_site_agent.cli analyze-dxf <file> --preview
python -m src.cad_site_agent.cli classify-drawing <file>
python -m src.cad_site_agent.cli normalize-layers <file>
```

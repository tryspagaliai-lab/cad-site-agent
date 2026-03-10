# CAD Site Agent — Inventory Report
**Generated:** 2026-03-10
**Last updated:** 2026-03-10 (Phase 3 complete)

---

## 1. Python Environments

| ID | Version | Path | Status |
|----|---------|------|--------|
| **py310** | 3.10.11 | `C:\Program Files\Python310\python.exe` | **DEFAULT PATH — RECOMMENDED for running cad-site-agent** |
| **py312** | 3.12.10 | `C:\Users\zilva\AppData\Local\Programs\Python\Python312\python.exe` | Usable — has rtree, missing click |
| **py313** | 3.13.7 | `C:\Python313\python.exe` | Usable — has click + all geo libs, missing rtree |
| py313-choco | 3.13.7 | `C:\ProgramData\chocolatey\bin\python3.13.exe` | Skip — bare install |
| py311 | broken | `E:\SHAKESPEARE_SYSTEM\Python311\python.exe` | **MISSING** — py.exe registered but path gone |
| autocad-mcp venv | 3.13.x | `C:\Users\zilva\mcp-servers\autocad-mcp\.venv` | uv-managed, has ezdxf + mcp |
| 3dsmax-mcp venv | 3.12.x | `C:\Users\zilva\mcp-servers\3dsmax-mcp\.venv` | uv-managed, no DXF libs |
| illustrator-mcp venv | unknown | `C:\Users\zilva\mcp-servers\illustrator-mcp\.venv` | Installed |

**uv:** v0.10.2 — `C:\Program Files\Python310\Scripts\uv.exe` — sees py310, py312, py313

---

## 2. Key Libraries

### TIER 1 — Available Now (all 3 envs unless noted)

| Library | Version | Available In | Phase | Role |
|---------|---------|-------------|-------|------|
| **ezdxf** | 1.4.3 | py310, py312, py313 | ALL | PRIMARY DXF engine — read/write/analyse/hatch/render |
| **shapely** | 2.1.2 | py310, py312, py313 | 5 | Polygon ops, region closure |
| **networkx** | 3.4-3.6 | py310, py312, py313 | 5 | Graph topology for boundary detection |
| **scipy** | 1.15-1.16 | py310, py312, py313 | 3 | `cKDTree` endpoint snapping |
| **numpy** | 2.2.6 | py310, py312, py313 | 3 | Coordinate arrays |
| **pydantic** | 2.12.5 | py310, py312, py313 | ALL | Config models, report schemas |
| **PyYAML** | 6.0.x | py310, py312, py313 | 4 | Layer alias config |
| **matplotlib** | 3.10.x | py310, py312, py313 | 2 | DXF preview PNG |
| **pillow** | 12.0.0 | py310, py312, py313 | 2 | Image post-processing |
| **click** | 8.3.1 | py310, py313 | 1 | CLI — argparse fallback covers py312 |
| **rtree** | 1.4.1 | py312 only | 3 opt | Spatial index for large drawings |

> **Bottom line:** All PHASE 1–5 MVP functionality is unblocked on `py310` as-is. Zero installs needed.

### TIER 2 — Missing but Essential MVP
> **None.** Every phase 1–5 dependency is already installed.

### TIER 3 — Missing but Deferrable

| Package | Missing From | When Needed |
|---------|-------------|-------------|
| `geopandas` | all envs | Phase 6+ — only if geo-referencing / CRS output needed |
| `click` | py312 | Phase 1 — argparse fallback already works |
| `typer`, `rich` | py312 | Optional UX improvement |
| `rtree` | py310, py313 | Phase 3 large-file optimisation — cKDTree sufficient for now |

---

## 3. CAD Scripts (Existing — Not Packaged)

### E:\ root — ad-hoc scripts (16 files)

| Script | Purpose | Keep? |
|--------|---------|-------|
| `rotate_v5_final.py` | Rotate parking texts to bay angle — **BEST VERSION** | Reference |
| `add_hatch.py` | SOLID hatch on closed polys by layer | Reference |
| `render_layers_v3.py` | ezdxf 1.4.x layer-colour render | Reference |
| `check_ezdxf3.py` | API exploration | Archive |
| `analyze_by_color.py` | Find entities by RGB true_color | Reference |
| `diagnose_rects.py` | LWPOLYLINE parking bay analysis | Reference |
| *(others)* | Exploration/debug | Archive |

### E:\SHAKESPEARE\scripts\ — ~60 scripts
- `dxf_parser.py`, `dwg_cleaner.py`, `pdf_to_dxf.py`, `parking_bays.py`
- `ollama_validator.py`, `chromadb_init.py` — AI-assisted validation already explored

**All existing scripts hardcode paths — kept as reference; logic migrated to `E:\cad-site-agent\src\`.**

---

## 4. DXF Data Assets (E:\SHAKESPEARE\RAW_DATA\)

| File | Size | Entities | Layers | Status |
|------|------|----------|--------|--------|
| `BDW Eastern Counties - DWH & BH Roman Gardens2.dxf` | 14.4 MB | 38,072 | 180 | **PRIMARY — analysed** |
| `ST-23-01S Planning Layout.dxf` | 89.8 MB | 51,164 | 1,008 | **Not yet analysed — HIGH PRIORITY** |
| `parking_rotated.dxf` | 13.9 MB | 38,072 | 180 | Derived — parking texts rotated |
| `parking_hatched.dxf` | 13.9 MB | 38,197 | 183 | Derived — hatches added (open polys missed) |
| `roman_gardens_gapclosed.dxf` | ~14 MB | ~34k | 180 | **Phase 3 output** — 6310 -> 2022 open polys |

### Phase 3 Gap Closer Results (Roman Gardens, 1m tolerance)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Open polylines | 6,310 | 2,022 | −68% |
| Closed polylines | 1,434 | 2,305 | +61% |
| Self-closed | — | 559 | — |
| Merged pairs | — | 3,417 | — |

---

## 5. MCP / CAD Tool Integrations

| Tool | Path | Status | DXF Libs |
|------|------|--------|----------|
| **autocad-mcp** v3.0.0 | `mcp-servers/autocad-mcp` | INSTALLED — ezdxf headless works without AutoCAD | ezdxf 1.4.3 |
| **3dsmax-mcp** | `mcp-servers/3dsmax-mcp` | INSTALLED — no DXF libs | — |
| **illustrator-mcp** | `mcp-servers/illustrator-mcp` | INSTALLED | — |
| **TouchDesigner MCP** | `mcp-servers/touchdesigner-mcp-td` | INSTALLED (viz, not CAD) | — |

---

## 6. Local AI (Ollama)

**Ollama running at** `http://localhost:11434`

| Model | Size | Type | Best Use |
|-------|------|------|---------|
| nomic-embed-text | 274 MB | embedding | Layer name vectorisation for semantic matching |
| qwen2.5:1.5b | 986 MB | LLM | Fast layer classification |
| ibm/granite3.3:2b-base | 1.5 GB | LLM | Small reasoning |
| qwen25-vl-3b | 2.4 GB | vision-LLM | Drawing content analysis |
| llama3:8b | 4.7 GB | LLM | Complex instruction following |
| granite3.3:8b | 4.9 GB | LLM | Best local reasoning |
| glm4-9b-chat | 6.3 GB | LLM | Multilingual |
| qwen-image-edit | 13 GB | vision-LLM | Image editing |

**chromadb 1.4.0** also available in py310 — vector DB for layer name embeddings.

**LM Studio:** not installed. **OpenWebUI:** not installed.

---

## 7. Phase Readiness

| Phase | Status | Blocker |
|-------|--------|---------|
| 0 — Inventory | **COMPLETE** | — |
| 1 — Scaffold | **COMPLETE** | — |
| 2 — Analyzer | **COMPLETE** | — |
| 3 — Gap Closer | **COMPLETE** | — |
| 4 — Layer Normalizer | **READY** | Run on gapclosed DXF, expand layer_aliases.yaml |
| 5 — Hatch / Region | **READY** | Depends on Phase 4 closed polys |
| 6 — MAX Export | Not started | 3dsmax-mcp installed, needs design |

---

## 8. Gaps & Risks

| Gap | Risk | Mitigation |
|-----|------|-----------|
| ST-23-01S not analysed | Unknown structure — 1008 layers suspicious | Phase 4 first test |
| 2,022 still-open polys | Hatch will miss them | Phase 5 handles via shapely buffer/union |
| ST-23-01S unit unknown | Gap closer could operate in wrong units | Manual check before running close-gaps |
| py311 broken | py.exe confusion | Ignore — use py310/py312/py313 directly |
| No uv.lock in cad-site-agent | Not reproducible in fresh env | Add if/when project needs isolated venv |

---

## 9. Recommendations

**Run today (zero installs):**
```bash
# From E:\cad-site-agent\
"C:\Program Files\Python310\python.exe" -m src.cad_site_agent.cli normalize-layers \
    "E:\SHAKESPEARE\RAW_DATA\roman_gardens_gapclosed.dxf" \
    --config config/layer_aliases.yaml \
    --output "E:\SHAKESPEARE\RAW_DATA\roman_gardens_normalised.dxf"
```

**Next Phase (4):** Expand `config/layer_aliases.yaml` to cover unknown layers from gapclosed DXF.

**Reuse patterns from existing scripts:**
- `rotate_v5_final.py` → expanding-radius spatial search pattern
- `render_layers_v3.py` → correct ezdxf 1.4.x render API
- `add_hatch.py` → hatch insertion pattern for Phase 5

---

## 10. Project Location

```
E:\cad-site-agent\          # Main structured project
E:\SHAKESPEARE\RAW_DATA\    # DXF source files
E:\SHAKESPEARE\scripts\     # Legacy exploration scripts (~60)
E:\                         # Ad-hoc DXF scripts (~16)
```

*Inventory complete. Next: PHASE 4 — Semantic Layer Normalization.*

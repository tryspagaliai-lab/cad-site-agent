# Status Report — Phase 3: Gap Closer MVP
**Date:** 2026-03-10

---

## PHASE 3 — Gap Closer COMPLETE

### Module: `src/cad_site_agent/cleanup/gap_closer.py`

**Strategy:**
1. Collect all open LWPOLYLINE start/end endpoints into a KD-tree.
2. Find endpoint pairs within `tolerance` distance using `cKDTree.query_pairs()`.
3. For each pair:
   - **Same polyline, start ≈ end** → set `entity.closed = True` (self-close).
   - **Different polylines** → chain-join by appending one poly's vertices to the other,
     handling all 4 orientations (end→start, start→end, end→end rev, start→start rev).
4. Absorbed polylines deleted from modelspace.
5. Short LINE bridges inserted for pairs that fail chain join (disabled by default since 0 needed in test).
6. Save output DXF.

### Test Results — Roman Gardens (BDW Roman Gardens2.dxf)

| Tolerance | Open Before | Open After | Net Closed | Self-closed | Merged |
|-----------|-------------|------------|------------|-------------|--------|
| 100 mm    | 6,310       | 2,860      | +490       | 148         | 2,960  |
| 500 mm    | 6,310       | 2,476      | +605       | 274         | 3,229  |
| **1000 mm** | **6,310** | **2,022**  | **+871**   | **559**     | **3,417** |
| 2000 mm   | 6,310       | 1,353      | +1,401     | 1,155       | 3,556  |
| 5000 mm   | 6,310       | 661        | +1,830     | 1,711       | 3,819  |

**Recommended default: 1000 mm (1 m)**
- Reduces open polys from 6,310 to 2,022 (−68%)
- Closed polys: 1,434 → 2,305 (+871, +61%)
- 0 errors

**Output:** `E:\SHAKESPEARE\RAW_DATA\roman_gardens_gapclosed.dxf`

### CLI Command Added

```bash
# From E:\cad-site-agent\
python -m src.cad_site_agent.cli close-gaps <file> \
    --tol 1000 \         # gap tolerance in drawing units
    --output <out.dxf>   # optional output path
    --no-bridge          # skip LINE bridges (chain-join only)
    --same-layer         # only snap same-layer endpoints
```

---

## Next Step — PHASE 4: Semantic Layer Normalization (full pipeline)

**Goal:** Run normalizer on gap-closed DXF, rename all layers to canonical classes,
write normalised DXF ready for hatch generation.

**Plan:**
1. Run `normalize-layers` on `roman_gardens_gapclosed.dxf`
2. Check mapping coverage — how many layers hit "unknown"?
3. Expand `config/layer_aliases.yaml` rules to cover gaps
4. Write final normalised DXF

**Then Phase 5:** Region/hatch MVP using shapely polygon reconstruction from closed polylines.

---

## Risks Update

| Risk | Severity | Status |
|------|---------|--------|
| 7,105 open polylines | HIGH | RESOLVED — reduced to 2,022 at 1m tolerance |
| 2,022 remaining open | MEDIUM | Phase 5 hatch will handle; closed polys are enough to start |
| ST-23-01S 17,265 open | HIGH | Next target after Roman Gardens pipeline |
| ST-23-01S unit=unknown | MEDIUM | Manual check needed before running gap closer |

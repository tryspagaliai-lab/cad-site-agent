"""
Gap Closer — Phase 3 MVP.

Finds open LWPOLYLINE endpoints within a tolerance and either:
  A) snaps two open endpoints together (extend/trim), or
  B) inserts a short bridging LINE to connect them, or
  C) closes a polyline whose start/end are within tol of each other.

Strategy:
  1. Collect all open LWPOLYLINE start/end points + their entity refs.
  2. Build KD-tree over all endpoints.
  3. For each open endpoint within tol of another endpoint:
       - If the two endpoints belong to the SAME polyline (start≈end) → set closed=True.
       - If they belong to DIFFERENT polylines → merge them (extend first poly, drop second,
         or insert a bridge LINE).
  4. Write results.

All distances are in native drawing units (mm for the Roman Gardens DXF).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import ezdxf
import numpy as np
from scipy.spatial import cKDTree


# ── Types ─────────────────────────────────────────────────────────────────────

@dataclass
class EndpointRef:
    """Reference to one end of an open LWPOLYLINE."""
    entity_handle: str
    which: str          # "start" or "end"
    x: float
    y: float
    layer: str


@dataclass
class GapCloseResult:
    source: str
    tolerance: float
    self_closed: int = 0        # polylines closed by matching own start/end
    merged_pairs: int = 0       # pairs of polys joined end-to-end
    bridges_added: int = 0      # short LINE bridges inserted
    open_before: int = 0
    open_after: int = 0
    closed_before: int = 0
    closed_after: int = 0
    output_path: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "tolerance_units": self.tolerance,
            "open_before": self.open_before,
            "open_after": self.open_after,
            "closed_before": self.closed_before,
            "closed_after": self.closed_after,
            "self_closed": self.self_closed,
            "merged_pairs": self.merged_pairs,
            "bridges_added": self.bridges_added,
            "output_path": self.output_path,
            "errors": self.errors,
        }


# ── Main entry point ──────────────────────────────────────────────────────────

def run_gap_close(
    dxf_path: str | Path,
    output_path: str | Path | None = None,
    tolerance: float = 1000.0,    # 1 m in mm units
    bridge_mode: bool = True,     # insert LINE bridges for non-adjacent pairs
    same_layer_only: bool = False, # only snap endpoints on the same layer
    max_bridge_len: float | None = None,  # reject bridges longer than this
) -> GapCloseResult:
    """
    Close gaps between open LWPOLYLINE endpoints.

    Args:
        dxf_path:        Input DXF.
        output_path:     Output DXF path. Auto-derived if None.
        tolerance:       Max endpoint distance to attempt closure (drawing units).
        bridge_mode:     If True, insert LINE bridge for non-adjacent polys.
                         If False, skip merging — only do self-close.
        same_layer_only: If True, only snap endpoints on matching layers.
        max_bridge_len:  Upper bound on bridge length (prevents cross-drawing snaps).
                         Defaults to tolerance.
    """
    path = Path(dxf_path)
    if not path.exists():
        raise FileNotFoundError(f"DXF not found: {path}")

    if max_bridge_len is None:
        max_bridge_len = tolerance

    doc = ezdxf.readfile(str(path))
    msp = doc.modelspace()

    result = GapCloseResult(source=str(path), tolerance=tolerance)

    # ── 1. Inventory open polylines ───────────────────────────────────────────
    open_polys: dict[str, Any] = {}      # handle -> entity
    endpoints: list[EndpointRef] = []

    for entity in msp:
        if entity.dxftype() != "LWPOLYLINE":
            continue
        try:
            layer = entity.dxf.layer
        except Exception:
            layer = "0"

        pts = list(entity.get_points("xy"))
        if len(pts) < 2:
            continue

        if entity.closed:
            result.closed_before += 1
        else:
            result.open_before += 1
            h = entity.dxf.handle
            open_polys[h] = entity
            sx, sy = pts[0]
            ex, ey = pts[-1]
            endpoints.append(EndpointRef(h, "start", sx, sy, layer))
            endpoints.append(EndpointRef(h, "end",   ex, ey, layer))

    if not endpoints:
        # Nothing to do
        _save(doc, path, output_path, result)
        return result

    # ── 2. Build KD-tree ──────────────────────────────────────────────────────
    coords = np.array([(ep.x, ep.y) for ep in endpoints], dtype=float)
    tree = cKDTree(coords)

    # ── 3. Find pairs ─────────────────────────────────────────────────────────
    processed_handles: set[str] = set()   # handles already merged/closed
    entities_to_delete: set[str] = set()  # handles of polys absorbed into another
    bridges_to_add: list[tuple] = []      # (x1,y1, x2,y2, layer)

    pairs = tree.query_pairs(tolerance)   # set of (i, j) with i<j

    for i, j in sorted(pairs):
        ep_i = endpoints[i]
        ep_j = endpoints[j]

        h_i = ep_i.entity_handle
        h_j = ep_j.entity_handle

        # Skip if either entity already consumed
        if h_i in entities_to_delete or h_j in entities_to_delete:
            continue
        if h_i not in open_polys or h_j not in open_polys:
            continue

        # Layer filter
        if same_layer_only and ep_i.layer != ep_j.layer:
            continue

        # ── Case A: same polyline → self-close ───────────────────────────────
        if h_i == h_j:
            # start ≈ end of same poly
            if {ep_i.which, ep_j.which} == {"start", "end"}:
                dist = _dist(ep_i.x, ep_i.y, ep_j.x, ep_j.y)
                if dist <= tolerance:
                    try:
                        ent = open_polys[h_i]
                        ent.closed = True
                        result.self_closed += 1
                        del open_polys[h_i]
                    except Exception as e:
                        result.errors.append(f"self-close {h_i}: {e}")
            continue

        # ── Case B: different polylines ───────────────────────────────────────
        if not bridge_mode:
            continue

        dist = _dist(ep_i.x, ep_i.y, ep_j.x, ep_j.y)
        if dist > max_bridge_len:
            continue

        ent_i = open_polys[h_i]
        ent_j = open_polys[h_j]

        # Try to merge end-to-start or start-to-end  (chain join)
        joined = _try_chain_join(ent_i, ep_i, ent_j, ep_j, open_polys)
        if joined:
            result.merged_pairs += 1
            # ent_j absorbed into ent_i; remove ent_j from msp
            entities_to_delete.add(h_j)
            del open_polys[h_j]
            # ep_j's layer used for bridge colour if needed
        else:
            # Just insert a tiny bridge LINE
            bridge_layer = ep_i.layer
            bridges_to_add.append((ep_i.x, ep_i.y, ep_j.x, ep_j.y, bridge_layer))
            result.bridges_added += 1

    # ── 4. Apply deletions ────────────────────────────────────────────────────
    if entities_to_delete:
        to_remove = [e for e in msp if e.dxftype() == "LWPOLYLINE"
                     and e.dxf.handle in entities_to_delete]
        for e in to_remove:
            msp.delete_entity(e)

    # ── 5. Add bridge lines ───────────────────────────────────────────────────
    for x1, y1, x2, y2, layer in bridges_to_add:
        try:
            msp.add_line((x1, y1, 0), (x2, y2, 0), dxfattribs={"layer": layer})
        except Exception as e:
            result.errors.append(f"bridge line add: {e}")

    # ── 6. Count result open/closed ───────────────────────────────────────────
    for entity in msp:
        if entity.dxftype() == "LWPOLYLINE":
            if entity.closed:
                result.closed_after += 1
            else:
                result.open_after += 1

    # ── 7. Save ───────────────────────────────────────────────────────────────
    _save(doc, path, output_path, result)
    return result


# ── Helpers ───────────────────────────────────────────────────────────────────

def _dist(x1, y1, x2, y2) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _try_chain_join(
    ent_i, ep_i: EndpointRef,
    ent_j, ep_j: EndpointRef,
    open_polys: dict,
) -> bool:
    """
    Attempt to join two polylines end-to-end by appending ent_j's points
    to ent_i. Returns True if successful.

    Valid chain cases:
      - ep_i.which == "end"   and ep_j.which == "start"  → append j after i
      - ep_i.which == "start" and ep_j.which == "end"    → prepend j before i
    """
    try:
        pts_i = list(ent_i.get_points("xyseb"))  # x,y,start_width,end_width,bulge
        pts_j = list(ent_j.get_points("xyseb"))

        if ep_i.which == "end" and ep_j.which == "start":
            # Append j's points to i (skip j[0] which overlaps i[-1])
            new_pts = pts_i + pts_j[1:]
        elif ep_i.which == "start" and ep_j.which == "end":
            # Prepend j's points to i (skip i[0])
            new_pts = pts_j + pts_i[1:]
        else:
            # end-end or start-start → one must be reversed
            if ep_i.which == "end" and ep_j.which == "end":
                pts_j_rev = list(reversed(pts_j))
                new_pts = pts_i + pts_j_rev[1:]
            else:  # start-start
                pts_j_rev = list(reversed(pts_j))
                new_pts = pts_j_rev + pts_i[1:]

        if len(new_pts) < 2:
            return False

        # Rewrite ent_i with merged points
        ent_i.set_points(new_pts, format="xyseb")

        # Check if now self-closing
        p0 = new_pts[0][:2]
        p_last = new_pts[-1][:2]
        if _dist(p0[0], p0[1], p_last[0], p_last[1]) < 1.0:  # 1 unit = 1mm
            ent_i.closed = True

        return True
    except Exception:
        return False


def _save(doc, path: Path, output_path, result: GapCloseResult) -> None:
    if output_path:
        out = Path(output_path)
    else:
        out = path.parent / f"{path.stem}_gapclosed.dxf"
    doc.saveas(str(out))
    result.output_path = str(out)

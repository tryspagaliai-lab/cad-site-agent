"""
agent_tools.py — read-only helpers behind the MCP server's agent tools.

Patterns adopted from SolidCraft's MCP surface (measure / screenshot /
--allow-path), kept in plain Python so they are testable without MCP:

  resolve_allowed()  — path allowlist (repo root + CAD_AGENT_ALLOW_PATHS)
  measure_dxf()      — per-layer counts, lengths, closed areas, extents
  render_dxf_png()   — PNG of a DXF so the agent can look at its own output

Nothing here mutates a DXF.
"""
from __future__ import annotations

import contextlib
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import ezdxf
from ezdxf import path as ezpath

ALLOW_ENV = "CAD_AGENT_ALLOW_PATHS"

# $INSUNITS code → name (subset that occurs in practice)
_INSUNITS = {
    0: "unitless", 1: "inches", 2: "feet", 4: "mm", 5: "cm", 6: "m", 7: "km",
}

# Entity types whose geometry ezdxf.path.make_path understands
_CURVE_TYPES = {"LINE", "LWPOLYLINE", "POLYLINE", "ARC", "CIRCLE", "ELLIPSE", "SPLINE"}


# ─── Path allowlist ──────────────────────────────────────────────────────────


class PathNotAllowed(ValueError):
    """Raised when a path resolves outside every allowed root."""


def allowed_roots(repo_root: Path) -> list[Path]:
    """Repo root plus every directory listed in $CAD_AGENT_ALLOW_PATHS."""
    roots = [repo_root.resolve()]
    for raw in os.environ.get(ALLOW_ENV, "").split(os.pathsep):
        raw = raw.strip()
        if raw:
            roots.append(Path(raw).expanduser().resolve())
    return roots


def resolve_allowed(path: str, repo_root: Path) -> Path:
    """Resolve *path* (relative → repo root) and require it inside an allowed root.

    Symlinks and '..' are resolved first, so they cannot escape the allowlist.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = repo_root / p
    p = p.resolve()
    roots = allowed_roots(repo_root)
    if any(p == r or p.is_relative_to(r) for r in roots):
        return p
    raise PathNotAllowed(
        f"Path not allowed: {p}\n"
        f"Allowed roots: {[str(r) for r in roots]}\n"
        f"Add a directory with {ALLOW_ENV}=<dir>[{os.pathsep}<dir>...]"
    )


# ─── Measure ─────────────────────────────────────────────────────────────────


def _shoelace(pts: list[tuple[float, float]]) -> float:
    total = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def _is_closed(entity, etype: str) -> bool:
    if etype == "CIRCLE":
        return True
    if etype == "LWPOLYLINE":
        return bool(entity.closed)
    if etype == "POLYLINE":
        return bool(entity.is_closed)
    return False


def measure_dxf(dxf_path: str | Path, layer: str = "", flatten: float = 0.01) -> dict:
    """Measure a DXF's modelspace per layer.

    Returns a dict with drawing units, extents and, per layer: entity counts by
    type, total curve length, number and total area of closed curves, and the
    number of open polylines (a quick gap indicator).

    Lengths/areas are in drawing units; arcs are flattened with max deviation
    *flatten* (drawing units).
    """
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    insunits = int(doc.header.get("$INSUNITS", 0))

    layers: dict[str, dict] = defaultdict(lambda: {
        "counts": defaultdict(int),
        "length": 0.0,
        "closed_count": 0,
        "closed_area": 0.0,
        "open_polylines": 0,
    })
    xmin = ymin = math.inf
    xmax = ymax = -math.inf
    errors = 0

    for e in msp:
        lname = e.dxf.layer
        if layer and lname != layer:
            continue
        etype = e.dxftype()
        rec = layers[lname]
        rec["counts"][etype] += 1
        if etype not in _CURVE_TYPES:
            continue
        try:
            pts = [(v.x, v.y) for v in ezpath.make_path(e).flattening(flatten)]
        except Exception:
            errors += 1
            continue
        if len(pts) < 2:
            continue
        closed = _is_closed(e, etype)
        # Circles and arcs analytically; everything else from the flattened path
        if etype == "CIRCLE":
            r = e.dxf.radius
            seg, area = 2 * math.pi * r, math.pi * r * r
        elif etype == "ARC":
            sweep = (e.dxf.end_angle - e.dxf.start_angle) % 360 or 360
            seg, area = math.radians(sweep) * e.dxf.radius, 0.0
        else:
            seg = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
            if closed and pts[0] != pts[-1]:
                seg += math.dist(pts[-1], pts[0])
            area = _shoelace(pts) if closed else 0.0
        rec["length"] += seg
        if closed:
            rec["closed_count"] += 1
            rec["closed_area"] += area
        elif etype in ("LWPOLYLINE", "POLYLINE"):
            rec["open_polylines"] += 1
        for x, y in pts:
            xmin, ymin = min(xmin, x), min(ymin, y)
            xmax, ymax = max(xmax, x), max(ymax, y)

    out_layers = {
        name: {
            "counts": dict(sorted(rec["counts"].items())),
            "entities": sum(rec["counts"].values()),
            "length": round(rec["length"], 3),
            "closed_count": rec["closed_count"],
            "closed_area": round(rec["closed_area"], 3),
            "open_polylines": rec["open_polylines"],
        }
        for name, rec in sorted(layers.items())
    }
    extents = None
    if xmin <= xmax:
        extents = {
            "min": [round(xmin, 3), round(ymin, 3)],
            "max": [round(xmax, 3), round(ymax, 3)],
            "width": round(xmax - xmin, 3),
            "height": round(ymax - ymin, 3),
        }
    return {
        "file": str(dxf_path),
        "units": _INSUNITS.get(insunits, f"code {insunits}"),
        "layer_filter": layer or None,
        "extents": extents,
        "totals": {
            "entities": sum(v["entities"] for v in out_layers.values()),
            "length": round(sum(v["length"] for v in out_layers.values()), 3),
            "closed_count": sum(v["closed_count"] for v in out_layers.values()),
            "closed_area": round(sum(v["closed_area"] for v in out_layers.values()), 3),
        },
        "layers": out_layers,
        "measure_errors": errors,
    }


# ─── Render ──────────────────────────────────────────────────────────────────


def render_dxf_png(dxf_path: str | Path, png_path: str | Path, size_in: float = 10.0) -> Path:
    """Render a DXF's modelspace to PNG (CPU / matplotlib Agg, headless-safe).

    Reuses the analyzer's layer-coloured preview. Raises RuntimeError on failure.
    """
    import matplotlib
    matplotlib.use("Agg")
    from .analyzer.report_writer import render_preview_png

    png_path = Path(png_path)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    # render_preview_png prints warnings; keep stdout clean for MCP stdio
    with contextlib.redirect_stdout(sys.stderr):
        ok = render_preview_png(dxf_path, png_path, max_size=size_in)
    if not ok:
        raise RuntimeError(f"Render failed for {dxf_path}")
    return png_path

"""
pdf_vector.py — cad-3d P0 stage A: extract vector primitives from a PDF page.

Coordinates are normalised to CAD convention (y up, origin bottom-left of the
page, units = PDF points). Raster-only pages yield an empty page record with a
reason instead of raising.

Public API
----------
    PdfPolyline, PdfText, PdfPageVectors
    extract_pdf_vectors(pdf_path, *, flatten_tolerance=0.5, pages=None)
        -> list[PdfPageVectors]
    pseudo_layer_name(stroke_rgb_hex, width) -> str
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field

TEXT_LAYER = "PDF_TEXT"

# Line-width classes (pt). Upper bounds are inclusive; last class is open-ended.
_WIDTH_CLASS_BOUNDS = [0.35, 0.75, 1.5, 3.0]

# Hard cap on bezier subdivision so a pathological tolerance cannot explode
# vertex counts.
_MAX_BEZIER_STEPS = 64


# ─── Data structures ─────────────────────────────────────────────────────────


@dataclass
class PdfPolyline:
    points: list[tuple[float, float]]
    closed: bool
    layer: str


@dataclass
class PdfText:
    content: str
    bbox: tuple[float, float, float, float]   # (xmin, ymin, xmax, ymax), y up
    layer: str = TEXT_LAYER


@dataclass
class PdfPageVectors:
    page_number: int                          # 1-based
    width: float
    height: float
    polylines: list[PdfPolyline] = field(default_factory=list)
    texts: list[PdfText] = field(default_factory=list)
    skipped_reason: str | None = None         # set when the page has no vectors

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Pseudo-layer naming ─────────────────────────────────────────────────────


def _color_to_hex(color) -> str:
    """Normalise a pdfminer colour value to an RRGGBB hex string.

    Handles None, scalar gray, (gray,), (r,g,b) and (c,m,y,k). Unparseable
    values fall back to black — the layer must stay deterministic, never raise.
    """
    if color is None:
        return "000000"
    if isinstance(color, (int, float)):
        color = (color,)
    try:
        vals = [float(v) for v in color]
    except (TypeError, ValueError):
        return "000000"
    if len(vals) == 1:
        g = vals[0]
        rgb = (g, g, g)
    elif len(vals) == 3:
        rgb = tuple(vals)
    elif len(vals) == 4:
        c, m, y, k = vals
        rgb = ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
    else:
        return "000000"
    clamp = lambda v: max(0, min(255, round(v * 255)))
    return "".join(f"{clamp(v):02X}" for v in rgb)


def _width_class(width) -> int:
    try:
        w = float(width)
    except (TypeError, ValueError):
        w = 1.0
    for i, bound in enumerate(_WIDTH_CLASS_BOUNDS):
        if w <= bound:
            return i
    return len(_WIDTH_CLASS_BOUNDS)


def pseudo_layer_name(stroke_rgb_hex: str, width) -> str:
    """Deterministic pseudo-layer: PDF_C<RRGGBB>_W<class>."""
    return f"PDF_C{stroke_rgb_hex}_W{_width_class(width)}"


def _layer_for(obj: dict) -> str:
    color = obj.get("stroking_color")
    if color is None:
        color = obj.get("non_stroking_color")
    return pseudo_layer_name(_color_to_hex(color), obj.get("linewidth"))


# ─── Path flattening ─────────────────────────────────────────────────────────


def _bezier_points(p0, p1, p2, p3, tolerance: float) -> list[tuple[float, float]]:
    """Sample a cubic bezier into line segments (excluding p0).

    Step count is derived from the control-polygon length so the chord error
    stays in the order of *tolerance*; deterministic for identical input.
    """
    cp_len = (math.dist(p0, p1) + math.dist(p1, p2) + math.dist(p2, p3))
    tol = max(tolerance, 1e-6)
    steps = min(_MAX_BEZIER_STEPS, max(4, math.ceil(cp_len / tol)))
    pts = []
    for i in range(1, steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def _flatten_path(path, tolerance: float) -> list[tuple[list[tuple[float, float]], bool]]:
    """Flatten a pdfplumber path into [(points, closed), ...] subpaths.

    Coordinates stay in pdfplumber's top-down system; the caller converts to
    y-up. Unknown operators end the current subpath (fail-safe, never raise).
    """
    subpaths: list[tuple[list[tuple[float, float]], bool]] = []
    current: list[tuple[float, float]] = []

    def _finish(closed: bool = False):
        nonlocal current
        if len(current) >= 2:
            subpaths.append((current, closed))
        current = []

    for seg in path:
        op = seg[0]
        if op == "m":
            _finish()
            current = [tuple(seg[1])]
        elif op == "l" and current:
            current.append(tuple(seg[1]))
        elif op == "c" and current:
            current.extend(_bezier_points(current[-1], tuple(seg[1]),
                                          tuple(seg[2]), tuple(seg[3]), tolerance))
        elif op == "v" and current:
            p0 = current[-1]
            current.extend(_bezier_points(p0, p0, tuple(seg[1]), tuple(seg[2]), tolerance))
        elif op == "y" and current:
            p1 = tuple(seg[1])
            current.extend(_bezier_points(current[-1], p1, p1, tuple(seg[2]), tolerance))
        elif op == "h":
            _finish(closed=True)
        else:
            _finish()
    _finish()
    return subpaths


# ─── Extraction ──────────────────────────────────────────────────────────────


def _extract_page(page, page_number: int, tolerance: float) -> PdfPageVectors:
    height = float(page.height)
    result = PdfPageVectors(page_number=page_number,
                            width=float(page.width), height=height)

    def _y_up_pts(pts):
        # pdfplumber "pts" are (x, top) — top-down; convert to y-up.
        return [(float(x), height - float(y)) for x, y in pts]

    for obj in page.rects:
        x0, x1 = float(obj["x0"]), float(obj["x1"])
        y0, y1 = height - float(obj["bottom"]), height - float(obj["top"])
        result.polylines.append(PdfPolyline(
            points=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
            closed=True, layer=_layer_for(obj)))

    for obj in list(page.lines) + list(page.curves):
        layer = _layer_for(obj)
        path = obj.get("path")
        if path:
            for pts, closed in _flatten_path(path, tolerance):
                result.polylines.append(PdfPolyline(
                    points=_y_up_pts(pts), closed=closed, layer=layer))
        elif obj.get("pts") and len(obj["pts"]) >= 2:
            result.polylines.append(PdfPolyline(
                points=_y_up_pts(obj["pts"]), closed=False, layer=layer))

    for obj in page.extract_words(use_text_flow=False):
        result.texts.append(PdfText(
            content=obj["text"],
            bbox=(float(obj["x0"]), height - float(obj["bottom"]),
                  float(obj["x1"]), height - float(obj["top"]))))

    if not result.polylines:
        result.skipped_reason = "no_vector_primitives"
    return result


def extract_pdf_vectors(
    pdf_path: str,
    *,
    flatten_tolerance: float = 0.5,
    pages: list[int] | None = None,
) -> list[PdfPageVectors]:
    """Extract vector primitives from *pdf_path*.

    Args:
        pdf_path:          Path to the PDF file.
        flatten_tolerance: Bezier flattening tolerance in PDF points.
        pages:             Optional 1-based page numbers; default all pages.

    Returns:
        One PdfPageVectors per processed page (empty pages carry
        ``skipped_reason`` instead of raising).
    """
    import pdfplumber

    results: list[PdfPageVectors] = []
    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            if pages is not None and idx not in pages:
                continue
            try:
                results.append(_extract_page(page, idx, flatten_tolerance))
            except Exception as exc:                      # fail-safe per page
                results.append(PdfPageVectors(
                    page_number=idx,
                    width=float(getattr(page, "width", 0.0)),
                    height=float(getattr(page, "height", 0.0)),
                    skipped_reason=f"extract_error: {exc}"))
    return results

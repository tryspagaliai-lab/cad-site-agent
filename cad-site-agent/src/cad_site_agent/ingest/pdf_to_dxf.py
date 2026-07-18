"""
pdf_to_dxf.py — cad-3d P0 stage B: write extracted PDF vectors to a DXF file.

The generated DXF uses deterministic pseudo-layers (PDF_C<hex>_W<class>,
PDF_TEXT) so the existing analyzer → classify → hatch → routing pipeline can
consume it unchanged. Mapping pseudo-layers to semantic classes stays a manual
step in config/layer_aliases.yaml (human-in-the-loop).

Public API
----------
    PdfIngestReport
    convert_pdf_to_dxf(pdf_path, output_dxf, *, flatten_tolerance=0.5,
                       pages=None) -> PdfIngestReport
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from .pdf_vector import PdfPageVectors, extract_pdf_vectors

_MIN_TEXT_HEIGHT = 0.1


@dataclass
class PdfIngestReport:
    source_pdf: str
    output_dxf: str
    generated_at: str
    status: str = "ok"                        # "ok" | "empty" | "error"
    pages_total: int = 0
    pages_with_vectors: int = 0
    polylines_written: int = 0
    texts_written: int = 0
    layers_created: list[str] = field(default_factory=list)
    skipped_pages: dict[str, str] = field(default_factory=dict)   # page -> reason
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    def write_json(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                     encoding="utf-8")
        return p


def _write_dxf(pages: list[PdfPageVectors], output_dxf: str) -> tuple[int, int, list[str]]:
    import ezdxf

    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    layers: set[str] = set()
    polylines = texts = 0

    def _layer(name: str) -> str:
        if name not in layers:
            doc.layers.add(name)
            layers.add(name)
        return name

    for page in pages:
        # Multi-page PDFs are laid side by side with a page-width gap so pages
        # never overlap in model space.
        x_off = (page.page_number - 1) * page.width * 2

        for pl in page.polylines:
            pts = [(x + x_off, y) for x, y in pl.points]
            if len(pts) < 2:
                continue
            msp.add_lwpolyline(pts, close=pl.closed,
                               dxfattribs={"layer": _layer(pl.layer)})
            polylines += 1

        for tx in page.texts:
            if not tx.content.strip():
                continue
            xmin, ymin, _, ymax = tx.bbox
            height = max(_MIN_TEXT_HEIGHT, ymax - ymin)
            msp.add_text(tx.content, dxfattribs={
                "layer": _layer(tx.layer),
                "height": height,
                "insert": (xmin + x_off, ymin),
            })
            texts += 1

    doc.saveas(output_dxf)
    return polylines, texts, sorted(layers)


def convert_pdf_to_dxf(
    pdf_path: str,
    output_dxf: str,
    *,
    flatten_tolerance: float = 0.5,
    pages: list[int] | None = None,
) -> PdfIngestReport:
    """Extract vectors from *pdf_path* and write them to *output_dxf*.

    Fail-safe: a raster-only PDF yields status="empty" with no DXF written; an
    unreadable PDF yields status="error". Neither case raises.
    """
    report = PdfIngestReport(
        source_pdf=str(pdf_path),
        output_dxf=str(output_dxf),
        generated_at=datetime.now().isoformat(timespec="seconds"),
    )
    try:
        page_vectors = extract_pdf_vectors(
            pdf_path, flatten_tolerance=flatten_tolerance, pages=pages)
        report.pages_total = len(page_vectors)
        for pv in page_vectors:
            if pv.skipped_reason:
                report.skipped_pages[str(pv.page_number)] = pv.skipped_reason
        with_vectors = [pv for pv in page_vectors if pv.polylines]
        report.pages_with_vectors = len(with_vectors)

        if not with_vectors:
            report.status = "empty"
            return report

        report.polylines_written, report.texts_written, report.layers_created = \
            _write_dxf(with_vectors, output_dxf)
        return report
    except Exception as exc:
        report.status = "error"
        report.error = str(exc)
        return report

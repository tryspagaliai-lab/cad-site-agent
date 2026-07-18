"""test_pdf_ingest.py — cad-3d P0 M1: PDF vector extraction + DXF adapter.

The fixture is a hand-crafted minimal vector PDF (no extra dependencies):
two lines, one polyline, one rect, one cubic bezier and one text string on a
300x200 pt page.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pdfplumber = pytest.importorskip("pdfplumber")

from cad_site_agent.ingest.pdf_vector import (
    TEXT_LAYER,
    extract_pdf_vectors,
    pseudo_layer_name,
)
from cad_site_agent.ingest.pdf_to_dxf import convert_pdf_to_dxf

PAGE_W, PAGE_H = 300, 200

CONTENT_STREAM = b"""1 w 0 0 0 RG
10 10 m 100 10 l S
2 w 0 0 1 RG
20 20 m 20 80 l 60 80 l S
1 w 1 0 0 RG
120 20 60 40 re S
0.5 w 0 0 0 RG
100 100 m 120 140 160 140 180 100 c S
BT /F1 12 Tf 40 160 Td (PARKING) Tj ET
"""


def _build_fixture_pdf() -> bytes:
    """Assemble a minimal valid one-page PDF with a correct xref table."""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
         b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
         % (PAGE_W, PAGE_H)),
        (b"<< /Length %d >>\nstream\n" % len(CONTENT_STREAM)
         + CONTENT_STREAM + b"endstream"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref_at = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1)
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += (b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objects) + 1, xref_at))
    return bytes(out)


@pytest.fixture()
def fixture_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "site_fixture.pdf"
    path.write_bytes(_build_fixture_pdf())
    return path


# ─── extraction ──────────────────────────────────────────────────────────────


def test_extracts_all_primitives(fixture_pdf):
    pages = extract_pdf_vectors(str(fixture_pdf))
    assert len(pages) == 1
    page = pages[0]
    assert page.skipped_reason is None
    assert (page.width, page.height) == (PAGE_W, PAGE_H)
    # 1 line + 1 two-segment polyline + 1 rect + 1 bezier
    assert len(page.polylines) == 4
    assert [t.content for t in page.texts] == ["PARKING"]
    assert page.texts[0].layer == TEXT_LAYER


def test_y_axis_points_up(fixture_pdf):
    """The horizontal line drawn at PDF y=10 must stay near the page BOTTOM."""
    page = extract_pdf_vectors(str(fixture_pdf))[0]
    flat = [p for pl in page.polylines for p in pl.points]
    lows = [pt for pt in flat if abs(pt[1] - 10) < 1e-6]
    assert lows, "expected the y=10 line to remain at y=10 in y-up space"
    # Text drawn near the top of the page (PDF y=160) must have high y.
    assert page.texts[0].bbox[1] > PAGE_H / 2


def test_bezier_is_flattened(fixture_pdf):
    page = extract_pdf_vectors(str(fixture_pdf), flatten_tolerance=0.5)
    curves = [pl for pl in page[0].polylines if len(pl.points) > 5]
    assert curves, "bezier should flatten into more than its 4 control points"
    ys = [y for _, y in curves[0].points]
    # Curve bows upward from y=100; flattened points must enter that bow but
    # never exceed the control-point hull (y=140).
    assert max(ys) > 110
    assert max(ys) <= 140 + 1e-6


def test_pseudo_layers_deterministic(fixture_pdf):
    run1 = extract_pdf_vectors(str(fixture_pdf))[0]
    run2 = extract_pdf_vectors(str(fixture_pdf))[0]
    assert [pl.layer for pl in run1.polylines] == [pl.layer for pl in run2.polylines]
    layers = {pl.layer for pl in run1.polylines}
    # Blue polyline (0 0 1 RG, 2 w) and red rect (1 0 0 RG, 1 w) get distinct
    # colour+width pseudo-layers.
    assert pseudo_layer_name("0000FF", 2) in layers
    assert pseudo_layer_name("FF0000", 1) in layers
    assert len(layers) >= 3


def test_raster_only_pdf_is_failsafe(tmp_path):
    """A PDF with no vector ops must produce an 'empty' report, not a crash."""
    global CONTENT_STREAM
    empty = tmp_path / "raster_like.pdf"
    saved = CONTENT_STREAM
    try:
        # Rebuild the fixture with a content stream containing no path ops.
        globals()["CONTENT_STREAM"] = b"BT /F1 8 Tf 5 5 Td (scan) Tj ET\n"
        empty.write_bytes(_build_fixture_pdf())
    finally:
        globals()["CONTENT_STREAM"] = saved
    report = convert_pdf_to_dxf(str(empty), str(tmp_path / "out.dxf"))
    assert report.status == "empty"
    assert not (tmp_path / "out.dxf").exists()
    assert report.skipped_pages.get("1") == "no_vector_primitives"


# ─── DXF adapter ─────────────────────────────────────────────────────────────


def test_convert_writes_dxf_with_pseudo_layers(fixture_pdf, tmp_path):
    out_dxf = tmp_path / "fixture.pdfvec.dxf"
    report = convert_pdf_to_dxf(str(fixture_pdf), str(out_dxf))
    assert report.status == "ok"
    assert out_dxf.exists()
    assert report.polylines_written == 4
    assert report.texts_written == 1
    assert TEXT_LAYER in report.layers_created

    import ezdxf
    doc = ezdxf.readfile(str(out_dxf))
    layer_names = {layer.dxf.name for layer in doc.layers}
    assert set(report.layers_created) <= layer_names
    msp = doc.modelspace()
    assert len(msp.query("LWPOLYLINE")) == 4
    assert len(msp.query("TEXT")) == 1
    # Rect must arrive closed so the hatch stage can pick it up as a region.
    closed = [e for e in msp.query("LWPOLYLINE") if e.closed]
    assert len(closed) == 1


def test_existing_pipeline_consumes_generated_dxf(fixture_pdf, tmp_path):
    """M1 acceptance: run_process must digest the PDF-derived DXF end-to-end."""
    out_dxf = tmp_path / "fixture.pdfvec.dxf"
    assert convert_pdf_to_dxf(str(fixture_pdf), str(out_dxf)).status == "ok"

    from cad_site_agent.pipeline import run_process
    result = run_process(str(out_dxf), str(tmp_path / "processed.dxf"))
    assert result.candidates_total >= 1          # the closed rect
    # Pseudo-layers carry no semantic aliases yet, so routing legitimately
    # skips them as unknown — the point is that every entity was consumed
    # without an error, not that it was kept.
    consumed = (result.features_written + result.features_removed
                + result.features_skipped)
    assert consumed >= 5                          # 4 polylines + 1 text

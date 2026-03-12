"""
tests/test_hatch_writer.py — Phase 6A

Unit tests for the hatch writer pipeline.

Run with:
    PYTHONPATH=src python -m pytest tests/test_hatch_writer.py -v
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import ezdxf
import pytest

from cad_site_agent.export.dxf_writer import material_to_layer_name, get_region_points
from cad_site_agent.export.hatch_writer import (
    filter_eligible,
    run_hatch_write,
    write_hatch_write_reports,
    WriteReport,
)


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _make_candidate(
    *,
    feature_type: str = "region",
    export_role: str = "hatch_and_export",
    material_class: str = "MAT_PAVING",
    status: str = "auto",
    confidence: float = 0.80,
    class_guess: str = "path",
    handle: str = "ABC1",
    source_type: str = "LWPOLYLINE",
) -> dict:
    return {
        "region": {
            "id": 0,
            "source_layer": "PATHS",
            "handle": handle,
            "area": 50000.0,
            "perimeter": 900.0,
            "bbox": [0.0, 0.0, 200.0, 250.0],
            "vertex_count": 4,
            "is_closed": True,
            "source_type": source_type,
        },
        "class_guess": class_guess,
        "hatch_class": material_class,
        "confidence": confidence,
        "status": status,
        "reasons": [],
        "semantic_label": {
            "feature_type": feature_type,
            "semantic_class": class_guess,
            "export_role": export_role,
            "material_class": material_class,
        },
    }


def _make_source_dxf(tmp_path: Path, handle_pts: dict[str, list[tuple]] | None = None) -> Path:
    """Create a minimal source DXF with LWPOLYLINE entities at known handles."""
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    if handle_pts:
        for pts in handle_pts.values():
            poly = msp.add_lwpolyline(pts, close=True)

    src = tmp_path / "source.dxf"
    doc.saveas(str(src))

    # Re-read to get real handles assigned by ezdxf
    src_doc = ezdxf.readfile(str(src))
    handles = {}
    for entity in src_doc.modelspace():
        if entity.dxftype() == "LWPOLYLINE":
            handles[entity.dxf.handle] = [(float(p[0]), float(p[1])) for p in entity.get_points()]

    return src, src_doc, handles


# ─── material_to_layer_name ───────────────────────────────────────────────────


class TestMaterialToLayerName:
    def test_paving(self):
        assert material_to_layer_name("MAT_PAVING") == "HATCH_MAT_PAVING"

    def test_tarmac(self):
        assert material_to_layer_name("MAT_TARMAC") == "HATCH_MAT_TARMAC"

    def test_grass(self):
        assert material_to_layer_name("MAT_GRASS") == "HATCH_MAT_GRASS"

    def test_building(self):
        assert material_to_layer_name("MAT_BUILDING") == "HATCH_MAT_BUILDING"

    def test_arbitrary(self):
        assert material_to_layer_name("MAT_WATER") == "HATCH_MAT_WATER"

    def test_prefix_always_hatch(self):
        name = material_to_layer_name("MAT_PARKING")
        assert name.startswith("HATCH_")
        assert "PARKING" in name


# ─── get_region_points ────────────────────────────────────────────────────────


class TestGetRegionPoints:
    def test_known_handle_returns_points(self, tmp_path):
        pts_in = [(0, 0), (100, 0), (100, 100), (0, 100)]
        _, src_doc, handles = _make_source_dxf(tmp_path, {"poly": pts_in})
        assert handles, "No polylines in source doc"

        handle = list(handles.keys())[0]
        pts_out = get_region_points(src_doc, handle, "LWPOLYLINE")
        assert pts_out is not None
        assert len(pts_out) == 4

    def test_unknown_handle_returns_none(self, tmp_path):
        _, src_doc, _ = _make_source_dxf(tmp_path)
        result = get_region_points(src_doc, "NONEXISTENT_HANDLE", "LWPOLYLINE")
        assert result is None


# ─── filter_eligible ─────────────────────────────────────────────────────────


class TestFilterEligible:
    def test_happy_path_auto(self):
        cands = [_make_candidate(status="auto", confidence=0.80)]
        eligible, skips = filter_eligible(cands, status_filter="auto")
        assert len(eligible) == 1
        assert not skips

    def test_filters_non_region(self):
        cands = [_make_candidate(feature_type="linear")]
        eligible, skips = filter_eligible(cands)
        assert len(eligible) == 0
        assert skips.get("not_region", 0) == 1

    def test_filters_wrong_export_role(self):
        cands = [_make_candidate(export_role="review")]
        eligible, skips = filter_eligible(cands)
        assert len(eligible) == 0
        assert skips.get("wrong_export_role", 0) == 1

    def test_filters_status_review_when_auto_required(self):
        cands = [_make_candidate(status="review")]
        eligible, skips = filter_eligible(cands, status_filter="auto")
        assert len(eligible) == 0
        assert skips.get("status_not_auto", 0) == 1

    def test_status_review_filter_passes_review(self):
        cands = [_make_candidate(status="review", confidence=0.60)]
        eligible, skips = filter_eligible(cands, status_filter="review")
        assert len(eligible) == 1

    def test_filters_empty_material_class(self):
        cands = [_make_candidate(material_class="")]
        eligible, skips = filter_eligible(cands)
        assert len(eligible) == 0
        assert skips.get("no_material_class", 0) == 1

    def test_filters_low_confidence(self):
        cands = [_make_candidate(confidence=0.50)]
        eligible, skips = filter_eligible(cands, min_confidence=0.75)
        assert len(eligible) == 0
        assert skips.get("low_confidence", 0) == 1

    def test_class_filter(self):
        cands = [
            _make_candidate(class_guess="path"),
            _make_candidate(class_guess="parking"),
        ]
        eligible, skips = filter_eligible(cands, class_filter="path")
        assert len(eligible) == 1
        assert eligible[0]["class_guess"] == "path"
        assert skips.get("class_filtered", 0) == 1

    def test_material_filter(self):
        cands = [
            _make_candidate(material_class="MAT_PAVING"),
            _make_candidate(material_class="MAT_TARMAC"),
        ]
        eligible, skips = filter_eligible(cands, material_filter="MAT_PAVING")
        assert len(eligible) == 1
        assert eligible[0]["semantic_label"]["material_class"] == "MAT_PAVING"

    def test_multiple_candidates_mixed(self):
        cands = [
            _make_candidate(status="auto", confidence=0.85),
            _make_candidate(feature_type="linear"),
            _make_candidate(material_class=""),
            _make_candidate(status="review"),
        ]
        eligible, skips = filter_eligible(cands)
        assert len(eligible) == 1
        assert sum(skips.values()) == 3

    def test_empty_input(self):
        eligible, skips = filter_eligible([])
        assert eligible == []
        assert skips == {}


# ─── run_hatch_write safety rules ────────────────────────────────────────────


class TestRunHatchWriteSafety:
    def test_raises_if_source_not_found(self, tmp_path):
        cands_path = tmp_path / "cands.json"
        cands_path.write_text('{"candidates": []}', encoding="utf-8")
        out = tmp_path / "out.dxf"

        with pytest.raises(FileNotFoundError, match="Source DXF"):
            run_hatch_write(
                str(tmp_path / "missing.dxf"),
                str(cands_path),
                str(out),
            )

    def test_raises_if_candidates_not_found(self, tmp_path):
        src = tmp_path / "source.dxf"
        doc = ezdxf.new("R2010")
        doc.saveas(str(src))
        out = tmp_path / "out.dxf"

        with pytest.raises(FileNotFoundError, match="Candidates JSON"):
            run_hatch_write(str(src), str(tmp_path / "missing.json"), str(out))

    def test_raises_if_output_exists(self, tmp_path):
        src = tmp_path / "source.dxf"
        doc = ezdxf.new("R2010")
        doc.saveas(str(src))

        cands_path = tmp_path / "cands.json"
        cands_path.write_text('{"candidates": []}', encoding="utf-8")

        out = tmp_path / "out.dxf"
        out.write_text("existing")  # pre-create

        with pytest.raises(FileExistsError):
            run_hatch_write(str(src), str(cands_path), str(out))

    def test_never_modifies_source(self, tmp_path):
        src = tmp_path / "source.dxf"
        doc = ezdxf.new("R2010")
        doc.saveas(str(src))
        src_mtime = src.stat().st_mtime

        cands_path = tmp_path / "cands.json"
        cands_path.write_text('{"candidates": []}', encoding="utf-8")
        out = tmp_path / "out.dxf"

        run_hatch_write(str(src), str(cands_path), str(out))

        assert src.stat().st_mtime == src_mtime, "Source DXF was modified!"


# ─── run_hatch_write zero-candidate path ────────────────────────────────────


class TestRunHatchWriteZeroCandidates:
    def test_zero_eligible_still_creates_dxf(self, tmp_path):
        src = tmp_path / "source.dxf"
        doc = ezdxf.new("R2010")
        doc.saveas(str(src))

        # All candidates are review status → filtered out by default auto filter
        cands = [_make_candidate(status="review", confidence=0.65)]
        payload = {"candidates": cands}
        cands_path = tmp_path / "cands.json"
        cands_path.write_text(json.dumps(payload), encoding="utf-8")

        out = tmp_path / "out.dxf"
        report = run_hatch_write(str(src), str(cands_path), str(out))

        assert report.total_input == 1
        assert report.total_eligible == 0
        assert report.total_written == 0
        assert out.exists(), "Output DXF must be created even for zero candidates"

    def test_report_explains_zero_written(self, tmp_path):
        src = tmp_path / "source.dxf"
        doc = ezdxf.new("R2010")
        doc.saveas(str(src))

        cands_path = tmp_path / "cands.json"
        cands_path.write_text('{"candidates": []}', encoding="utf-8")
        out = tmp_path / "out.dxf"

        report = run_hatch_write(str(src), str(cands_path), str(out))

        assert report.total_written == 0
        assert report.total_input == 0


# ─── run_hatch_write with real geometry ─────────────────────────────────────


class TestRunHatchWriteWithGeometry:
    def test_writes_hatch_for_eligible_candidate(self, tmp_path):
        # Build a source DXF with one closed polyline
        src = tmp_path / "source.dxf"
        src_doc = ezdxf.new("R2010")
        msp = src_doc.modelspace()
        pts = [(0, 0), (100, 0), (100, 100), (0, 100)]
        msp.add_lwpolyline(pts, close=True)
        src_doc.saveas(str(src))

        # Read back to get the real handle
        reloaded = ezdxf.readfile(str(src))
        handle = None
        for e in reloaded.modelspace():
            if e.dxftype() == "LWPOLYLINE":
                handle = e.dxf.handle
        assert handle is not None

        # Build candidates JSON using the real handle
        cand = _make_candidate(
            status="auto",
            confidence=0.85,
            material_class="MAT_PAVING",
            handle=handle,
        )
        payload = {"candidates": [cand]}
        cands_path = tmp_path / "cands.json"
        cands_path.write_text(json.dumps(payload), encoding="utf-8")

        out = tmp_path / "out.dxf"
        report = run_hatch_write(str(src), str(cands_path), str(out))

        assert report.total_written == 1
        assert out.exists()

        # Verify the output DXF contains a HATCH on the right layer
        out_doc = ezdxf.readfile(str(out))
        hatches = [e for e in out_doc.modelspace() if e.dxftype() == "HATCH"]
        assert len(hatches) == 1
        assert hatches[0].dxf.layer == "HATCH_MAT_PAVING"

    def test_output_dxf_has_correct_layer(self, tmp_path):
        src = tmp_path / "source.dxf"
        src_doc = ezdxf.new("R2010")
        msp = src_doc.modelspace()
        msp.add_lwpolyline([(0, 0), (50, 0), (50, 50), (0, 50)], close=True)
        src_doc.saveas(str(src))

        reloaded = ezdxf.readfile(str(src))
        handle = None
        for e in reloaded.modelspace():
            if e.dxftype() == "LWPOLYLINE":
                handle = e.dxf.handle

        cand = _make_candidate(
            status="auto", confidence=0.82,
            material_class="MAT_TARMAC", handle=handle,
        )
        cands_path = tmp_path / "cands.json"
        cands_path.write_text(json.dumps({"candidates": [cand]}), encoding="utf-8")

        out = tmp_path / "out.dxf"
        report = run_hatch_write(str(src), str(cands_path), str(out))

        out_doc = ezdxf.readfile(str(out))
        layer_names = [layer.dxf.name for layer in out_doc.layers]
        assert "HATCH_MAT_TARMAC" in layer_names


# ─── write_hatch_write_reports ───────────────────────────────────────────────


class TestWriteHatchWriteReports:
    def _make_report(self, tmp_path) -> WriteReport:
        return WriteReport(
            source_dxf=str(tmp_path / "source.dxf"),
            candidates_json=str(tmp_path / "cands.json"),
            output_dxf=str(tmp_path / "out.dxf"),
            generated_at="2026-03-12T10:00:00",
            total_input=10,
            total_eligible=3,
            total_written=3,
            total_skipped=7,
            skips_by_reason={"status_not_auto": 7},
            by_material={"MAT_PAVING": {"layer": "HATCH_MAT_PAVING", "eligible": 3}},
        )

    def test_json_schema(self, tmp_path):
        report = self._make_report(tmp_path)
        json_path, md_path = write_hatch_write_reports(
            report, str(tmp_path), "myfile"
        )
        assert json_path.exists()
        data = json.loads(json_path.read_text())

        # Required top-level keys
        assert "meta" in data
        assert "totals" in data
        assert "skips_by_reason" in data
        assert "by_material" in data

        # Meta fields
        assert "source_dxf" in data["meta"]
        assert "candidates_json" in data["meta"]
        assert "output_dxf" in data["meta"]
        assert "generated_at" in data["meta"]

        # Totals fields
        assert "input" in data["totals"]
        assert "eligible" in data["totals"]
        assert "written" in data["totals"]
        assert "skipped" in data["totals"]

    def test_json_values(self, tmp_path):
        report = self._make_report(tmp_path)
        json_path, _ = write_hatch_write_reports(report, str(tmp_path), "myfile")
        data = json.loads(json_path.read_text())

        assert data["totals"]["input"] == 10
        assert data["totals"]["eligible"] == 3
        assert data["totals"]["written"] == 3
        assert data["totals"]["skipped"] == 7

    def test_markdown_contains_totals(self, tmp_path):
        report = self._make_report(tmp_path)
        _, md_path = write_hatch_write_reports(report, str(tmp_path), "myfile")
        assert md_path.exists()
        text = md_path.read_text()
        assert "10" in text  # total_input
        assert "HATCH_MAT_PAVING" in text

    def test_markdown_zero_written_note(self, tmp_path):
        report = WriteReport(
            source_dxf="src.dxf", candidates_json="c.json", output_dxf="out.dxf",
            generated_at="2026-01-01T00:00:00",
            total_input=5, total_eligible=0, total_written=0, total_skipped=5,
            skips_by_reason={"status_not_auto": 5},
            by_material={},
        )
        _, md_path = write_hatch_write_reports(report, str(tmp_path), "empty")
        text = md_path.read_text()
        assert "--status review" in text  # guidance for zero-written case

    def test_output_filenames(self, tmp_path):
        report = self._make_report(tmp_path)
        json_path, md_path = write_hatch_write_reports(
            report, str(tmp_path), "roman_gardens_gapclosed"
        )
        assert json_path.name == "roman_gardens_gapclosed.hatch_write.json"
        assert md_path.name == "roman_gardens_gapclosed.hatch_write.md"

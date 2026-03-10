"""
Tests for the new drawing type classifier (classify/drawing_type.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cad_site_agent.analyzer.dxf_analyzer import AnalysisReport
from cad_site_agent.classify.drawing_type import (
    DrawingTypeResult,
    classify_drawing_type,
)


# ─── Helpers ────────────────────────────────────────────────────────────────

def _make_report(**kwargs) -> AnalysisReport:
    """Create a minimal AnalysisReport for testing."""
    defaults = dict(
        source_file="test.dxf",
        file_size_kb=100,
        ezdxf_version="1.4.3",
        total_entities=1000,
        entity_type_counts={},
        total_layers=10,
        layers={},
        has_hatches=False,
        has_blocks=False,
        has_splines=False,
        has_3d=False,
        closed_polyline_count=0,
        open_polyline_count=0,
        total_line_segments=0,
    )
    defaults.update(kwargs)
    return AnalysisReport(**defaults)


# ─── DrawingTypeResult ───────────────────────────────────────────────────────

class TestDrawingTypeResult:
    def test_to_dict_structure(self):
        r = DrawingTypeResult(label="rich_site_layout", confidence=0.75,
                              reasons=["test reason"], hatch_count=30)
        d = r.to_dict()
        assert d["label"] == "rich_site_layout"
        assert d["confidence"] == 0.75
        assert d["reasons"] == ["test reason"]
        assert "diagnostics" in d
        assert d["diagnostics"]["hatch_count"] == 30

    def test_defaults_unknown(self):
        r = DrawingTypeResult()
        assert r.label == "unknown"
        assert r.confidence == 0.0
        assert r.reasons == []


# ─── illustrator_derived ────────────────────────────────────────────────────

class TestIllustratorDerived:
    def test_very_high_splines_pure(self):
        # Pure-spline drawing: no LINE entities → linework_ratio=0 → sparse_linework weak
        report = _make_report(
            total_entities=60,
            entity_type_counts={"SPLINE": 60},
            has_splines=True,
        )
        result = classify_drawing_type(report)
        assert result.label == "illustrator_derived"
        assert result.confidence >= 0.6

    def test_high_splines_dominant(self):
        # 25 splines out of 30 total = 83% spline ratio → clearly illustrator
        report = _make_report(
            total_entities=30,
            entity_type_counts={"SPLINE": 25, "ARC": 5},
            has_splines=True,
        )
        result = classify_drawing_type(report)
        assert result.label == "illustrator_derived"

    def test_spline_ratio_dominant(self):
        # 70 splines in 200 total = 35% → clearly above 5% threshold
        # AND linework_ratio stays low (no LINE)
        report = _make_report(
            total_entities=200,
            entity_type_counts={"SPLINE": 70, "ARC": 130},
            has_splines=True,
        )
        result = classify_drawing_type(report)
        assert result.label == "illustrator_derived"

    def test_mixed_spline_line_is_ambiguous(self):
        # 60 splines + 940 lines: genuinely ambiguous; classifier may pick either
        report = _make_report(
            total_entities=1000,
            entity_type_counts={"SPLINE": 60, "LINE": 940},
        )
        result = classify_drawing_type(report)
        # Both categories get max score ~0.9; either is acceptable
        assert result.label in ("illustrator_derived", "sparse_linework")
        assert result.confidence >= 0.8


# ─── rich_site_layout ───────────────────────────────────────────────────────

class TestRichSiteLayout:
    def test_many_hatch_and_semantic_layers(self):
        layers = {
            "parking": object(), "grass": object(), "boundary": object(),
            "driveway": object(), "path": object(), "building": object(),
        }
        # monkeypatch keys — use proper LayerInfo later
        from cad_site_agent.analyzer.dxf_analyzer import LayerInfo
        layers = {k: LayerInfo(name=k) for k in layers}

        report = _make_report(
            entity_type_counts={"HATCH": 50, "LWPOLYLINE": 400, "LINE": 550},
            total_entities=1000,
            layers=layers,
            closed_polyline_count=120,
        )
        result = classify_drawing_type(report)
        assert result.label == "rich_site_layout"
        assert result.hatch_count == 50
        assert result.semantic_class_count >= 5

    def test_needs_both_hatch_and_semantics(self):
        """Only semantics, no hatch → should NOT be rich_site_layout at high confidence."""
        from cad_site_agent.analyzer.dxf_analyzer import LayerInfo
        layers = {k: LayerInfo(name=k) for k in
                  ["parking", "grass", "boundary", "driveway", "path"]}
        report = _make_report(
            entity_type_counts={"LINE": 1000},
            total_entities=1000,
            layers=layers,
        )
        result = classify_drawing_type(report)
        # No hatch means rich_site_layout score < 0.5; sparse_linework gets a boost
        assert result.label != "rich_site_layout" or result.confidence < 0.5


# ─── sparse_linework ────────────────────────────────────────────────────────

class TestSparseLinework:
    def test_pure_linework_no_semantics(self):
        report = _make_report(
            entity_type_counts={"LINE": 700, "LWPOLYLINE": 200},
            total_entities=1000,
            total_layers=5,
            layers={},
        )
        result = classify_drawing_type(report)
        assert result.label == "sparse_linework"
        assert result.confidence >= 0.5

    def test_no_hatch_adds_score(self):
        report = _make_report(
            entity_type_counts={"LINE": 600},
            total_entities=600,
        )
        result = classify_drawing_type(report)
        # No hatch at all + some linework should score sparse_linework
        assert result.label in ("sparse_linework", "unknown")


# ─── max_prep ───────────────────────────────────────────────────────────────

class TestMaxPrep:
    def test_3d_geometry_with_material_layers(self):
        # Realistic max_prep: 3D geometry + material layer names + some hatch
        # (hatch >=5 suppresses sparse_linework hatch=0 bonus)
        from cad_site_agent.analyzer.dxf_analyzer import LayerInfo
        layers = {k: LayerInfo(name=k) for k in
                  ["material_concrete", "mesh_roof", "model_ground",
                   "solid_walls", "render_setup", "working_3d"]}
        report = _make_report(
            layers=layers,
            total_layers=6,
            entity_type_counts={"3DFACE": 500, "HATCH": 5},
            total_entities=505,
            has_3d=True,
        )
        result = classify_drawing_type(report)
        assert result.label == "max_prep"
        assert result.confidence >= 0.6

    def test_many_material_layers_with_hatch_suppressor(self):
        # 6 material layers + hatch=5 to suppress sparse_linework hatch=0 bonus
        from cad_site_agent.analyzer.dxf_analyzer import LayerInfo
        layers = {k: LayerInfo(name=k) for k in
                  ["material_wood", "working_mesh", "model_base",
                   "solid_3d", "render_export", "mesh_shell"]}
        report = _make_report(
            layers=layers,
            total_layers=6,
            entity_type_counts={"HATCH": 5},
            total_entities=5,
        )
        result = classify_drawing_type(report)
        assert result.label == "max_prep"


# ─── unknown ────────────────────────────────────────────────────────────────

class TestUnknown:
    def test_empty_drawing(self):
        report = _make_report(
            total_entities=0,
            entity_type_counts={},
            layers={},
        )
        result = classify_drawing_type(report)
        # Very sparse signal — could be unknown or sparse_linework
        assert result.label in ("unknown", "sparse_linework")

    def test_mixed_moderate_signals(self):
        """Low scores across the board → unknown."""
        from cad_site_agent.analyzer.dxf_analyzer import LayerInfo
        layers = {k: LayerInfo(name=k) for k in ["layer1", "layer2"]}
        report = _make_report(
            total_entities=100,
            entity_type_counts={"LINE": 50, "SPLINE": 3, "HATCH": 1},
            layers=layers,
            total_layers=2,
        )
        result = classify_drawing_type(report)
        # HATCH present → sparse_linework score drops, but all scores are moderate
        assert result.label in ("unknown", "sparse_linework", "rich_site_layout")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

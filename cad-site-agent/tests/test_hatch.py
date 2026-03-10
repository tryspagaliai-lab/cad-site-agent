"""
tests/test_hatch.py — Phase 4B

Unit + integration tests for the hatch candidate pipeline.

Run with:
    PYTHONPATH=src python -m pytest tests/test_hatch.py -v
"""
from __future__ import annotations

import json
import math
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ─── Imports from the package ───────────────────────────────────────────────
from cad_site_agent.hatch.closed_regions import (
    ClosedRegion,
    _shoelace_area,
    _chord_perimeter,
    _bbox,
)
from cad_site_agent.hatch.confidence import score_candidate
from cad_site_agent.hatch.semantic_hatch import (
    HatchCandidate,
    _match_layer_to_class,
    _layer_has_hatch,
    _merge_hints,
    summarise_candidates,
)
from cad_site_agent.export.review_writer import write_hatch_report


# ─── Fixtures ────────────────────────────────────────────────────────────────

_SCORING = {
    "strong_layer_signal":       0.45,
    "hatch_in_layer_family":     0.15,
    "shape_heuristic_match":     0.20,
    "suspicious_size_penalty":  -0.15,
    "ambiguous_overlap_penalty": -0.20,
}
_THRESHOLDS = {"auto": 0.75, "review": 0.45}
_AREA_HINTS = {
    "parking":  {"min": 6000,  "max": 500_000},
    "building": {"min": 5000,  "max": 5_000_000},
    "path":     {"min": 500,   "max": 200_000},
}

_LAYER_HINTS = {
    "parking":  ["parking", "carpark", "bay"],
    "building": ["building", "bldg", "struct"],
    "path":     ["footpath", "path", "pavement"],
    "garden":   ["grass", "lawn", "garden"],
    "driveway": ["driveway", "asphalt", "tarmac"],
}


def _make_region(
    layer: str = "TEST",
    area: float = 10_000.0,
    region_id: int = 0,
) -> ClosedRegion:
    return ClosedRegion(
        id=region_id,
        source_layer=layer,
        handle="ABC",
        area=area,
        perimeter=400.0,
        bbox=(0.0, 0.0, 100.0, 100.0),
        vertex_count=4,
        is_closed=True,
        source_type="LWPOLYLINE",
    )


def _make_report(layers: dict | None = None):
    """Return a minimal AnalysisReport mock."""
    mock = MagicMock()
    mock.layers = layers or {}
    return mock


# ─── 1. Geometry helpers ─────────────────────────────────────────────────────


class TestGeometryHelpers:
    def test_shoelace_square(self):
        pts = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert _shoelace_area(pts) == pytest.approx(100.0)

    def test_shoelace_triangle(self):
        pts = [(0, 0), (6, 0), (0, 4)]
        assert _shoelace_area(pts) == pytest.approx(12.0)

    def test_shoelace_degenerate_line(self):
        pts = [(0, 0), (5, 5)]
        assert _shoelace_area(pts) == pytest.approx(0.0)

    def test_chord_perimeter_square(self):
        pts = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert _chord_perimeter(pts) == pytest.approx(40.0)

    def test_bbox_basic(self):
        pts = [(1, 2), (5, 0), (3, 7)]
        assert _bbox(pts) == (1, 0, 5, 7)


# ─── 2. ClosedRegion dataclass ───────────────────────────────────────────────


class TestClosedRegion:
    def test_to_dict_keys(self):
        r = _make_region()
        d = r.to_dict()
        expected_keys = {
            "id", "source_layer", "handle", "area", "perimeter",
            "bbox", "vertex_count", "is_closed", "source_type",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_area_rounded(self):
        r = _make_region(area=12345.6789)
        d = r.to_dict()
        assert d["area"] == pytest.approx(12345.68, abs=0.01)


# ─── 3. Confidence scoring ───────────────────────────────────────────────────


class TestScoreCandidate:
    def test_strong_layer_signal_auto(self):
        """Layer match + hatch bonus + area in range → auto (0.45+0.15+0.20=0.80)"""
        region = _make_region(layer="CB-PARKING", area=50_000)
        score, status, reasons = score_candidate(
            region,
            "parking",
            layer_matched=True,
            match_count=1,
            layer_has_hatch=True,
            area_hints=_AREA_HINTS,
            scoring=_SCORING,
            thresholds=_THRESHOLDS,
        )
        assert status == "auto"
        assert score >= 0.75
        assert any("parking" in r for r in reasons)

    def test_hatch_bonus_pushes_higher(self):
        """Layer match + hatch bonus should yield higher score."""
        region = _make_region(area=50_000)
        # score_candidate returns (confidence, status, reasons)
        score_no_hatch, _, _ = score_candidate(
            region, "parking",
            layer_matched=True, match_count=1, layer_has_hatch=False,
            area_hints=_AREA_HINTS, scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        score_with_hatch, _, _ = score_candidate(
            region, "parking",
            layer_matched=True, match_count=1, layer_has_hatch=True,
            area_hints=_AREA_HINTS, scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        assert score_with_hatch > score_no_hatch

    def test_ambiguity_penalty(self):
        """Matching 2 classes should apply penalty."""
        region = _make_region(area=50_000)
        score, status, reasons = score_candidate(
            region, "parking",
            layer_matched=True, match_count=2, layer_has_hatch=False,
            area_hints=_AREA_HINTS, scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        assert any("ambiguous" in r.lower() for r in reasons)

    def test_no_match_unknown_skip(self):
        """No layer match → score stays low → skip"""
        region = _make_region(area=500)
        score, status, reasons = score_candidate(
            region, "unknown",
            layer_matched=False, match_count=0, layer_has_hatch=False,
            area_hints=_AREA_HINTS, scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        assert status == "skip"
        assert score < 0.45

    def test_area_out_of_range_penalty(self):
        """Area outside expected range → suspicious_size_penalty applied."""
        region = _make_region(area=1.0)  # tiny, out of parking range
        score, status, reasons = score_candidate(
            region, "parking",
            layer_matched=True, match_count=1, layer_has_hatch=False,
            area_hints=_AREA_HINTS, scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        assert any("outside" in r for r in reasons)

    def test_score_clamped(self):
        """Score must never exceed 1.0."""
        region = _make_region(area=50_000)
        score, _, _ = score_candidate(
            region, "parking",
            layer_matched=True, match_count=1, layer_has_hatch=True,
            area_hints=_AREA_HINTS, scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        assert 0.0 <= score <= 1.0

    def test_status_review_range(self):
        """Score in [0.45, 0.75) → review."""
        region = _make_region(area=50_000)
        # Only layer signal, no area hints entry → score=0.45
        score, status, _ = score_candidate(
            region, "building",
            layer_matched=True, match_count=1, layer_has_hatch=False,
            area_hints={},  # no area hints for building
            scoring=_SCORING, thresholds=_THRESHOLDS,
        )
        assert status == "review"
        assert score == pytest.approx(0.45)


# ─── 4. Layer matching ───────────────────────────────────────────────────────


class TestMatchLayer:
    def test_exact_keyword_match(self):
        cls, matched, count = _match_layer_to_class("CB-P-PARKING", _LAYER_HINTS)
        assert cls == "parking"
        assert matched is True
        assert count == 1

    def test_case_insensitive(self):
        cls, matched, _ = _match_layer_to_class("BUILDING-OUTLINE", _LAYER_HINTS)
        assert cls == "building"
        assert matched is True

    def test_no_match_returns_unknown(self):
        cls, matched, count = _match_layer_to_class("XREF-SURVEY", _LAYER_HINTS)
        assert cls == "unknown"
        assert matched is False
        assert count == 0

    def test_ambiguous_layer_counts_multiple(self):
        # "asphalt" → driveway, but add "driveway" also matches parking if we set it up
        hints = {
            "driveway": ["driveway", "asphalt"],
            "road":     ["road", "asphalt"],
        }
        cls, matched, count = _match_layer_to_class("CB-ASPHALT", hints)
        assert matched is True
        assert count == 2

    def test_underscore_in_layer_name(self):
        cls, matched, _ = _match_layer_to_class("fcs_path_01", _LAYER_HINTS)
        assert cls == "path"
        assert matched is True


# ─── 5. _layer_has_hatch ─────────────────────────────────────────────────────


class TestLayerHasHatch:
    def _make_layer_info(self, hatch_count: int = 0):
        li = MagicMock()
        li.entity_types = {"LWPOLYLINE": 10, "HATCH": hatch_count}
        return li

    def test_direct_layer_match(self):
        report = _make_report({
            "CB-PARKING": self._make_layer_info(hatch_count=3),
        })
        assert _layer_has_hatch("CB-PARKING", report) is True

    def test_no_hatch(self):
        report = _make_report({
            "CB-PARKING": self._make_layer_info(hatch_count=0),
        })
        assert _layer_has_hatch("CB-PARKING", report) is False

    def test_family_prefix_match(self):
        """CB-PARKING has no hatch but CB-GRASS does → True."""
        report = _make_report({
            "CB-PARKING": self._make_layer_info(0),
            "CB-GRASS":   self._make_layer_info(5),
        })
        assert _layer_has_hatch("CB-PARKING", report) is True

    def test_layer_not_in_report(self):
        report = _make_report({})
        assert _layer_has_hatch("XREF-UNKNOWN", report) is False


# ─── 6. _merge_hints ─────────────────────────────────────────────────────────


class TestMergeHints:
    def test_merge_adds_new_keywords(self):
        base  = {"parking": ["parking"]}
        extra = {"parking": ["car-park"], "road": ["road"]}
        result = _merge_hints(base, extra)
        assert "car-park" in result["parking"]
        assert "road" in result["road"]

    def test_merge_no_duplicates(self):
        base  = {"parking": ["parking", "bay"]}
        extra = {"parking": ["parking"]}  # duplicate
        result = _merge_hints(base, extra)
        assert result["parking"].count("parking") == 1

    def test_merge_does_not_mutate_base(self):
        base  = {"parking": ["parking"]}
        extra = {"parking": ["bay"]}
        _ = _merge_hints(base, extra)
        assert "bay" not in base["parking"]


# ─── 7. summarise_candidates ─────────────────────────────────────────────────


class TestSummariseCandidates:
    def _make_candidate(self, status: str, cls: str, layer: str = "L") -> HatchCandidate:
        return HatchCandidate(
            region=_make_region(layer=layer),
            class_guess=cls,
            hatch_class="MAT_X",
            confidence=0.8,
            status=status,
        )

    def test_counts(self):
        cands = [
            self._make_candidate("auto",   "parking", "L1"),
            self._make_candidate("auto",   "parking", "L1"),
            self._make_candidate("review", "building", "L2"),
            self._make_candidate("skip",   "unknown",  "L3"),
        ]
        summary = summarise_candidates(cands)
        assert summary["total"] == 4
        assert summary["by_status"]["auto"]   == 2
        assert summary["by_status"]["review"] == 1
        assert summary["by_status"]["skip"]   == 1
        assert summary["by_class"]["parking"] == 2

    def test_empty(self):
        summary = summarise_candidates([])
        assert summary["total"] == 0
        assert summary["by_status"] == {}


# ─── 8. write_hatch_report ───────────────────────────────────────────────────


class TestWriteHatchReport:
    def _make_candidates(self, n: int = 3) -> list[HatchCandidate]:
        return [
            HatchCandidate(
                region=_make_region(layer=f"LAYER-{i}", area=10_000 * (i + 1), region_id=i),
                class_guess="parking",
                hatch_class="MAT_PARKING",
                confidence=0.8,
                status="auto",
                reasons=["Layer name matches class 'parking'"],
            )
            for i in range(n)
        ]

    def test_json_file_created(self):
        cands = self._make_candidates(3)
        summary = summarise_candidates(cands)
        with tempfile.TemporaryDirectory() as tmp:
            json_p, md_p = write_hatch_report(
                cands, summary, "test_drawing.dxf", tmp
            )
            assert json_p.exists()
            assert md_p.exists()

    def test_json_structure(self):
        cands = self._make_candidates(2)
        summary = summarise_candidates(cands)
        with tempfile.TemporaryDirectory() as tmp:
            json_p, _ = write_hatch_report(cands, summary, "test.dxf", tmp)
            data = json.loads(json_p.read_text(encoding="utf-8"))
            assert "meta" in data
            assert "summary" in data
            assert "candidates" in data
            assert len(data["candidates"]) == 2

    def test_candidate_dict_keys(self):
        cands = self._make_candidates(1)
        summary = summarise_candidates(cands)
        with tempfile.TemporaryDirectory() as tmp:
            json_p, _ = write_hatch_report(cands, summary, "test.dxf", tmp)
            data = json.loads(json_p.read_text(encoding="utf-8"))
            c = data["candidates"][0]
            assert "region" in c
            assert "class_guess" in c
            assert "hatch_class" in c
            assert "confidence" in c
            assert "status" in c
            assert "reasons" in c

    def test_md_contains_summary_table(self):
        cands = self._make_candidates(2)
        summary = summarise_candidates(cands)
        with tempfile.TemporaryDirectory() as tmp:
            _, md_p = write_hatch_report(cands, summary, "test.dxf", tmp)
            content = md_p.read_text(encoding="utf-8")
            assert "## Summary" in content
            assert "Auto" in content

    def test_output_filenames(self):
        cands = self._make_candidates(1)
        summary = summarise_candidates(cands)
        with tempfile.TemporaryDirectory() as tmp:
            json_p, md_p = write_hatch_report(
                cands, summary, "roman_gardens_gapclosed.dxf", tmp
            )
            assert json_p.name == "roman_gardens_gapclosed.hatch_candidates.json"
            assert md_p.name  == "roman_gardens_gapclosed.hatch_candidates.md"


# ─── 9. HatchCandidate.to_dict ───────────────────────────────────────────────


class TestHatchCandidateToDict:
    def test_to_dict_keys(self):
        c = HatchCandidate(
            region=_make_region(),
            class_guess="parking",
            hatch_class="MAT_PARKING",
            confidence=0.8,
            status="auto",
            reasons=["test"],
        )
        d = c.to_dict()
        assert set(d.keys()) == {
            "region", "class_guess", "hatch_class",
            "confidence", "status", "reasons",
        }
        assert d["class_guess"] == "parking"
        assert d["confidence"] == 0.8

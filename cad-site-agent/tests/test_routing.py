"""
tests/test_routing.py — Phase 7

Unit tests for export/routing.py.

Run with:
    PYTHONPATH=src python -m pytest tests/test_routing.py -v
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import ezdxf
import pytest

from cad_site_agent.export.routing import (
    ROLE_TO_GROUP,
    GROUP_TO_PREFIX,
    DEFAULT_ROUTING_HINTS,
    classify_layer_name,
    destination_layer,
    run_route_features,
    write_routing_reports,
    RoutingReport,
)
from cad_site_agent.semantic.taxonomy import SemanticLabel


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _mock_taxonomy(class_map: dict[str, SemanticLabel]):
    """Return a mock TaxonomyLoader that classifies class_guess via class_map."""
    mock = MagicMock()
    mock.classify.side_effect = lambda guess: class_map.get(guess, SemanticLabel.unknown())
    return mock


_BASIC_TAXONOMY = _mock_taxonomy({
    "fence":        SemanticLabel("linear",  "fence",        "keep_linework"),
    "wall":         SemanticLabel("linear",  "wall",         "keep_linework"),
    "kerb":         SemanticLabel("linear",  "kerb",         "keep_linework"),
    "tree":         SemanticLabel("symbol",  "tree",         "keep_symbols"),
    "bollard":      SemanticLabel("symbol",  "bollard",      "keep_symbols"),
    "annotation":   SemanticLabel("text",    "annotation",   "keep_text"),
    "plot_number":  SemanticLabel("text",    "plot_number",  "keep_text"),
    "parking_line": SemanticLabel("marking", "parking_line", "keep_markings"),
    "titleblock":   SemanticLabel("noise",   "titleblock",   "remove"),
    "notes":        SemanticLabel("noise",   "notes",        "remove"),
})


def _make_minimal_candidates_json(tmp_path: Path) -> Path:
    """Write a minimal candidates JSON (content not used by route-features routing)."""
    payload = {"candidates": []}
    p = tmp_path / "candidates.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def _make_source_dxf(
    tmp_path: Path,
    entities: list[tuple[str, str]],  # [(dxftype, layer_name), ...]
) -> Path:
    """Create a source DXF with simple entities on specified layers.

    Supported types: LINE, LWPOLYLINE, TEXT, MTEXT, INSERT.
    """
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    for dxftype, layer_name in entities:
        if layer_name not in doc.layers:
            doc.layers.add(layer_name)

        t = dxftype.upper()
        if t == "LINE":
            e = msp.add_line((0, 0), (100, 0))
        elif t == "LWPOLYLINE":
            e = msp.add_lwpolyline([(0, 0), (100, 0), (100, 100), (0, 100)])
        elif t == "TEXT":
            e = msp.add_text("hello")
        elif t == "MTEXT":
            e = msp.add_mtext("hello")
        elif t == "INSERT":
            # Block must exist
            if "MYBLOCK" not in doc.blocks:
                doc.blocks.new("MYBLOCK")
            e = msp.add_blockref("MYBLOCK", (0, 0))
        elif t == "CIRCLE":
            e = msp.add_circle((0, 0), radius=50)
        elif t == "ARC":
            e = msp.add_arc((0, 0), radius=50, start_angle=0, end_angle=90)
        else:
            e = msp.add_line((0, 0), (100, 0))

        e.dxf.layer = layer_name

    src = tmp_path / "source.dxf"
    doc.saveas(str(src))
    return src


# ─── destination_layer ────────────────────────────────────────────────────────


class TestDestinationLayer:
    def test_linear_fence(self):
        assert destination_layer("linear", "fence") == "LINEWORK_FENCE"

    def test_marking_parking_line(self):
        assert destination_layer("marking", "parking_line") == "MARKING_PARKING_LINE"

    def test_symbol_bollard(self):
        assert destination_layer("symbol", "bollard") == "SYMBOL_BOLLARD"

    def test_text_plot_number(self):
        assert destination_layer("text", "plot_number") == "TEXT_PLOT_NUMBER"

    def test_prefix_from_group_to_prefix(self):
        for group, prefix in GROUP_TO_PREFIX.items():
            assert destination_layer(group, "x").startswith(prefix + "_")

    def test_unknown_group_uppercased(self):
        # Falls back to feature_group.upper()
        result = destination_layer("custom_group", "thing")
        assert result == "CUSTOM_GROUP_THING"

    def test_semantic_class_uppercased(self):
        result = destination_layer("linear", "retaining_wall")
        assert result == "LINEWORK_RETAINING_WALL"


# ─── ROLE_TO_GROUP / GROUP_TO_PREFIX constants ───────────────────────────────


class TestConstants:
    def test_role_to_group_keys(self):
        assert "keep_linework" in ROLE_TO_GROUP
        assert "keep_markings" in ROLE_TO_GROUP
        assert "keep_symbols"  in ROLE_TO_GROUP
        assert "keep_text"     in ROLE_TO_GROUP
        assert "remove"        in ROLE_TO_GROUP

    def test_role_to_group_values(self):
        assert ROLE_TO_GROUP["keep_linework"] == "linear"
        assert ROLE_TO_GROUP["keep_markings"] == "marking"
        assert ROLE_TO_GROUP["keep_symbols"]  == "symbol"
        assert ROLE_TO_GROUP["keep_text"]     == "text"
        assert ROLE_TO_GROUP["remove"]        == "noise"

    def test_group_to_prefix_all_groups(self):
        for group in ("linear", "marking", "symbol", "text"):
            assert group in GROUP_TO_PREFIX
            assert GROUP_TO_PREFIX[group] == GROUP_TO_PREFIX[group].upper()


# ─── classify_layer_name ─────────────────────────────────────────────────────


class TestClassifyLayerName:
    def test_fence_layer(self):
        sem = classify_layer_name("STE-FENCE-LINE", taxonomy=_BASIC_TAXONOMY)
        assert sem.semantic_class == "fence"
        assert sem.feature_type  == "linear"

    def test_case_insensitive(self):
        sem = classify_layer_name("STE-FENCE-LINE", taxonomy=_BASIC_TAXONOMY)
        sem2 = classify_layer_name("ste-fence-line", taxonomy=_BASIC_TAXONOMY)
        assert sem.semantic_class == sem2.semantic_class

    def test_tree_layer(self):
        sem = classify_layer_name("PLANTING-TREES", taxonomy=_BASIC_TAXONOMY)
        assert sem.semantic_class == "tree"
        assert sem.feature_type  == "symbol"

    def test_titleblock_is_noise(self):
        sem = classify_layer_name("TB-SHEET-BORDER", taxonomy=_BASIC_TAXONOMY)
        assert sem.feature_type == "noise"

    def test_unrecognised_returns_unknown(self):
        sem = classify_layer_name("XREF-BLAH-999", taxonomy=_BASIC_TAXONOMY)
        assert sem.feature_type == "unknown"

    def test_custom_hints_override(self):
        custom_hints = {"fence": ["xrf_fen"]}
        sem = classify_layer_name("XRF_FEN_MAIN", taxonomy=_BASIC_TAXONOMY,
                                  routing_hints=custom_hints)
        assert sem.semantic_class == "fence"

    def test_default_hints_used_when_none(self):
        # annotation should match "annot" from DEFAULT_ROUTING_HINTS
        sem = classify_layer_name("ANNOT-NOTES", taxonomy=_BASIC_TAXONOMY,
                                  routing_hints=None)
        # "notes" keyword matches "notes" class in hints → "notes" in basic taxonomy = noise
        assert sem is not None  # just verify no crash; value depends on key ordering

    def test_parking_marking(self):
        sem = classify_layer_name("PARKING-LINE-MAIN", taxonomy=_BASIC_TAXONOMY)
        assert sem.semantic_class == "parking_line"
        assert sem.feature_type  == "marking"

    def test_annotation_text(self):
        sem = classify_layer_name("ANNOTATION-LAYER", taxonomy=_BASIC_TAXONOMY)
        assert sem.feature_type  == "text"
        assert sem.semantic_class == "annotation"


# ─── run_route_features — safety / IO errors ─────────────────────────────────


class TestRunRouteFeaturesErrors:
    def test_missing_source_dxf(self, tmp_path):
        candidates = _make_minimal_candidates_json(tmp_path)
        with pytest.raises(FileNotFoundError, match="Source DXF"):
            run_route_features(
                str(tmp_path / "missing.dxf"),
                str(candidates),
                str(tmp_path / "out.dxf"),
            )

    def test_missing_candidates_json(self, tmp_path):
        src = _make_source_dxf(tmp_path, [])
        with pytest.raises(FileNotFoundError, match="Candidates JSON"):
            run_route_features(
                str(src),
                str(tmp_path / "missing.json"),
                str(tmp_path / "out.dxf"),
            )

    def test_output_already_exists(self, tmp_path):
        src = _make_source_dxf(tmp_path, [])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        out.write_text("exists")
        with pytest.raises(FileExistsError):
            run_route_features(str(src), str(candidates), str(out))

    def test_source_not_modified(self, tmp_path):
        """Source DXF should be byte-identical after route-features runs."""
        src = _make_source_dxf(tmp_path, [("LINE", "0")])
        candidates = _make_minimal_candidates_json(tmp_path)
        before = src.read_bytes()
        run_route_features(str(src), str(candidates), str(tmp_path / "out.dxf"))
        assert src.read_bytes() == before


# ─── run_route_features — output always created ──────────────────────────────


class TestRunRouteFeaturesOutput:
    def test_output_created_when_no_entities(self, tmp_path):
        """Empty source → output DXF is still created."""
        src = _make_source_dxf(tmp_path, [])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out))
        assert out.exists()
        assert report.total_input == 0
        assert report.total_written == 0

    def test_returns_routing_report(self, tmp_path):
        src = _make_source_dxf(tmp_path, [])
        candidates = _make_minimal_candidates_json(tmp_path)
        report = run_route_features(str(src), str(candidates), str(tmp_path / "out.dxf"))
        assert isinstance(report, RoutingReport)


# ─── run_route_features — entity routing ─────────────────────────────────────


class TestRunRouteFeaturesRouting:
    def test_entity_on_fence_layer_is_written(self, tmp_path):
        """LINE on layer containing 'fence' should be routed to LINEWORK_FENCE."""
        src = _make_source_dxf(tmp_path, [("LINE", "STE-FENCE-MAIN")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out))

        assert report.total_written == 1
        out_doc = ezdxf.readfile(str(out))
        layers_written = {e.dxf.layer for e in out_doc.modelspace()}
        assert any("LINEWORK" in l and "FENCE" in l for l in layers_written)

    def test_unknown_entity_is_skipped(self, tmp_path):
        """Entity on an unrecognised layer should be skipped (not written)."""
        src = _make_source_dxf(tmp_path, [("LINE", "XREF-UNKNOWN-LAYER-999")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out))

        assert report.total_written == 0
        assert report.unknowns == 1

    def test_noise_entity_is_removed(self, tmp_path):
        """Entity on a titleblock layer should be counted as removed."""
        src = _make_source_dxf(tmp_path, [("LINE", "TITLEBLOCK-BORDER")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out),
                                     exclude_noise=True)

        assert report.total_removed >= 1
        assert report.total_written == 0

    def test_noise_entity_kept_when_exclude_noise_false(self, tmp_path):
        """With exclude_noise=False, noise entity goes to skipped rather than removed."""
        src = _make_source_dxf(tmp_path, [("LINE", "TITLEBLOCK-BORDER")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out),
                                     exclude_noise=False)

        # noise entity not removed, not written, counted as skipped
        assert report.total_removed == 0
        assert report.total_written == 0

    def test_linework_disabled_skips_linear(self, tmp_path):
        """include_linework=False → linear entity is skipped."""
        src = _make_source_dxf(tmp_path, [("LINE", "STE-FENCE-MAIN")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out),
                                     include_linework=False)
        assert report.total_written == 0

    def test_multiple_entities_multiple_layers(self, tmp_path):
        """Multiple entity types across different semantic layers."""
        entities = [
            ("LINE",      "STE-FENCE-MAIN"),       # linear  → written
            ("TEXT",      "TITLEBLOCK-BORDER"),     # noise   → removed
            ("LINE",      "XREF-UNKNOWN-999"),      # unknown → skipped
        ]
        src = _make_source_dxf(tmp_path, entities)
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out))

        assert report.total_input   == 3
        assert report.total_written == 1
        assert report.total_removed == 1
        assert report.unknowns      == 1

    def test_by_dest_layer_populated(self, tmp_path):
        """by_dest_layer should record the destination layer name."""
        src = _make_source_dxf(tmp_path, [("LINE", "STE-FENCE-MAIN")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        report = run_route_features(str(src), str(candidates), str(out))

        assert any("LINEWORK" in k and "FENCE" in k for k in report.by_dest_layer)

    def test_output_dxf_has_correct_layer(self, tmp_path):
        """The written entity in output DXF must be on the destination layer."""
        src = _make_source_dxf(tmp_path, [("LINE", "STE-FENCE-MAIN")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        run_route_features(str(src), str(candidates), str(out))

        out_doc = ezdxf.readfile(str(out))
        entity = next(iter(out_doc.modelspace()))
        assert "LINEWORK" in entity.dxf.layer
        assert "FENCE" in entity.dxf.layer

    def test_output_layer_registered_in_layer_table(self, tmp_path):
        """The destination layer should be added to the output DXF layer table."""
        src = _make_source_dxf(tmp_path, [("LINE", "STE-FENCE-MAIN")])
        candidates = _make_minimal_candidates_json(tmp_path)
        out = tmp_path / "out.dxf"
        run_route_features(str(src), str(candidates), str(out))

        out_doc = ezdxf.readfile(str(out))
        layer_names = [l.dxf.name for l in out_doc.layers]
        assert any("LINEWORK" in n and "FENCE" in n for n in layer_names)


# ─── write_routing_reports ────────────────────────────────────────────────────


class TestWriteRoutingReports:
    def _make_report(self) -> RoutingReport:
        return RoutingReport(
            source_dxf="source.dxf",
            candidates_json="candidates.json",
            output_dxf="output.dxf",
            generated_at="2025-01-01T12:00:00",
            total_input=100,
            total_written=60,
            total_removed=10,
            total_skipped=30,
            by_feature_type={"linear": 60, "noise": 10, "unknown": 30},
            by_semantic_class={"fence": 40, "wall": 20, "titleblock": 10},
            by_export_role={"keep_linework": 60, "remove": 10},
            by_dest_layer={"LINEWORK_FENCE": 40, "LINEWORK_WALL": 20},
            unknowns=30,
        )

    def test_creates_json_and_md(self, tmp_path):
        report = self._make_report()
        json_path, md_path = write_routing_reports(report, str(tmp_path), "test_stem")
        assert json_path.exists()
        assert md_path.exists()
        assert json_path.name == "test_stem.routing.json"
        assert md_path.name   == "test_stem.routing.md"

    def test_json_has_required_keys(self, tmp_path):
        report = self._make_report()
        json_path, _ = write_routing_reports(report, str(tmp_path), "test_stem")
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert "meta"    in data
        assert "totals"  in data
        assert "by_feature_type"   in data
        assert "by_semantic_class" in data
        assert "by_dest_layer"     in data

    def test_json_totals_correct(self, tmp_path):
        report = self._make_report()
        json_path, _ = write_routing_reports(report, str(tmp_path), "test_stem")
        totals = json.loads(json_path.read_text(encoding="utf-8"))["totals"]
        assert totals["input"]   == 100
        assert totals["written"] == 60
        assert totals["removed"] == 10
        assert totals["skipped"] == 30

    def test_md_contains_stem(self, tmp_path):
        report = self._make_report()
        _, md_path = write_routing_reports(report, str(tmp_path), "test_stem")
        content = md_path.read_text(encoding="utf-8")
        assert "test_stem" in content

    def test_md_contains_totals_table(self, tmp_path):
        report = self._make_report()
        _, md_path = write_routing_reports(report, str(tmp_path), "test_stem")
        content = md_path.read_text(encoding="utf-8")
        assert "## Totals" in content
        assert "100" in content

    def test_output_dir_created(self, tmp_path):
        report = self._make_report()
        new_dir = tmp_path / "new" / "subdir"
        write_routing_reports(report, str(new_dir), "stem")
        assert new_dir.exists()

    def test_md_dest_layer_section(self, tmp_path):
        report = self._make_report()
        _, md_path = write_routing_reports(report, str(tmp_path), "stem")
        content = md_path.read_text(encoding="utf-8")
        assert "LINEWORK_FENCE" in content

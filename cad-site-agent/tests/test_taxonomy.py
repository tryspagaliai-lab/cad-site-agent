"""
tests/test_taxonomy.py — Phase 5

Unit tests for SemanticLabel (Task 3) and TaxonomyLoader (Task 4).

Run with:
    PYTHONPATH=src python -m pytest tests/test_taxonomy.py -v
"""
from __future__ import annotations

from pathlib import Path

import pytest

# ─── Imports under test ──────────────────────────────────────────────────────
from cad_site_agent.semantic.taxonomy import SemanticLabel, TaxonomyLoader


# ─── 1. SemanticLabel — construction ─────────────────────────────────────────


class TestSemanticLabelConstruction:
    def test_all_fields_stored(self):
        sl = SemanticLabel(
            feature_type="region",
            semantic_class="parking_bay",
            export_role="hatch_and_export",
            material_class="MAT_PARKING",
        )
        assert sl.feature_type  == "region"
        assert sl.semantic_class == "parking_bay"
        assert sl.export_role   == "hatch_and_export"
        assert sl.material_class == "MAT_PARKING"

    def test_material_class_optional_defaults_empty(self):
        """Non-region types carry no material; default is empty string."""
        sl = SemanticLabel(
            feature_type="linear",
            semantic_class="kerb",
            export_role="keep_linework",
        )
        assert sl.material_class == ""

    def test_unknown_factory(self):
        sl = SemanticLabel.unknown()
        assert sl.feature_type  == "unknown"
        assert sl.semantic_class == "unknown"
        assert sl.export_role   == "review"
        assert sl.material_class == ""


# ─── 2. SemanticLabel — to_dict ───────────────────────────────────────────────


class TestSemanticLabelToDict:
    def test_keys_present(self):
        sl = SemanticLabel(
            feature_type="region",
            semantic_class="building",
            export_role="hatch_and_export",
            material_class="MAT_BUILDING",
        )
        d = sl.to_dict()
        assert set(d.keys()) == {
            "feature_type", "semantic_class", "export_role", "material_class"
        }

    def test_values_round_trip(self):
        sl = SemanticLabel(
            feature_type="symbol",
            semantic_class="bollard",
            export_role="keep_symbols",
            material_class="",
        )
        d = sl.to_dict()
        assert d["feature_type"]  == "symbol"
        assert d["semantic_class"] == "bollard"
        assert d["export_role"]   == "keep_symbols"
        assert d["material_class"] == ""

    def test_unknown_to_dict(self):
        d = SemanticLabel.unknown().to_dict()
        assert d["feature_type"]  == "unknown"
        assert d["semantic_class"] == "unknown"
        assert d["export_role"]   == "review"
        assert d["material_class"] == ""


# ─── 3. SemanticLabel — equality ─────────────────────────────────────────────


class TestSemanticLabelEquality:
    def test_equal_instances(self):
        a = SemanticLabel("region", "parking_bay", "hatch_and_export", "MAT_PARKING")
        b = SemanticLabel("region", "parking_bay", "hatch_and_export", "MAT_PARKING")
        assert a == b

    def test_different_class(self):
        a = SemanticLabel("region", "parking_bay", "hatch_and_export", "MAT_PARKING")
        b = SemanticLabel("region", "building",    "hatch_and_export", "MAT_BUILDING")
        assert a != b

    def test_unknown_instances_equal(self):
        assert SemanticLabel.unknown() == SemanticLabel.unknown()


# ─── 4. SemanticLabel — immutability / frozen dataclass ──────────────────────


class TestSemanticLabelImmutability:
    def test_frozen_raises_on_assignment(self):
        sl = SemanticLabel.unknown()
        with pytest.raises((AttributeError, TypeError)):
            sl.feature_type = "region"  # type: ignore[misc]


# ─── TaxonomyLoader fixtures ──────────────────────────────────────────────────

_CONFIG = Path(__file__).resolve().parents[1] / "config"
_TAXONOMY_PATH = _CONFIG / "semantic_taxonomy.yaml"
_ROLES_PATH    = _CONFIG / "export_roles.yaml"


@pytest.fixture
def loader() -> TaxonomyLoader:
    return TaxonomyLoader(_TAXONOMY_PATH, _ROLES_PATH)


# ─── 5. TaxonomyLoader — construction ────────────────────────────────────────


class TestTaxonomyLoaderConstruction:
    def test_loads_without_error(self, loader):
        assert loader is not None

    def test_missing_taxonomy_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            TaxonomyLoader(tmp_path / "missing.yaml", _ROLES_PATH)

    def test_missing_roles_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            TaxonomyLoader(_TAXONOMY_PATH, tmp_path / "missing.yaml")


# ─── 6. TaxonomyLoader.classify — known canonical classes ────────────────────


class TestTaxonomyLoaderClassify:
    def test_region_class(self, loader):
        sl = loader.classify("parking_bay")
        assert sl.feature_type   == "region"
        assert sl.semantic_class  == "parking_bay"
        assert sl.export_role    == "hatch_and_export"
        assert sl.material_class == "MAT_PARKING"

    def test_region_building(self, loader):
        sl = loader.classify("building")
        assert sl.feature_type   == "region"
        assert sl.export_role    == "hatch_and_export"
        assert sl.material_class == "MAT_BUILDING"

    def test_linear_class(self, loader):
        sl = loader.classify("kerb")
        assert sl.feature_type   == "linear"
        assert sl.semantic_class  == "kerb"
        assert sl.export_role    == "keep_linework"
        assert sl.material_class == ""

    def test_marking_class(self, loader):
        sl = loader.classify("parking_line")
        assert sl.feature_type  == "marking"
        assert sl.export_role   == "keep_markings"
        assert sl.material_class == ""

    def test_symbol_bollard(self, loader):
        sl = loader.classify("bollard")
        assert sl.feature_type  == "symbol"
        assert sl.export_role   == "keep_symbols"
        assert sl.material_class == ""

    def test_symbol_gate(self, loader):
        sl = loader.classify("gate")
        assert sl.feature_type  == "symbol"
        assert sl.export_role   == "keep_symbols"

    def test_text_class(self, loader):
        sl = loader.classify("plot_number")
        assert sl.feature_type  == "text"
        assert sl.export_role   == "keep_text"
        assert sl.material_class == ""

    def test_noise_class(self, loader):
        sl = loader.classify("titleblock")
        assert sl.feature_type  == "noise"
        assert sl.export_role   == "remove"
        assert sl.material_class == ""

    def test_unknown_class_returns_unknown(self, loader):
        sl = loader.classify("xref_survey_grid")
        assert sl.feature_type   == "unknown"
        assert sl.semantic_class  == "unknown"
        assert sl.export_role    == "review"
        assert sl.material_class == ""


# ─── 7. TaxonomyLoader.classify — alias resolution ───────────────────────────


class TestTaxonomyLoaderAliases:
    def test_phase4b_parking_alias(self, loader):
        """'parking' (Phase 4B coarse name) → resolves to parking_bay."""
        sl = loader.classify("parking")
        assert sl.semantic_class == "parking_bay"
        assert sl.feature_type   == "region"
        assert sl.export_role    == "hatch_and_export"

    def test_phase4b_garden_alias(self, loader):
        """'garden' → soft_landscape."""
        sl = loader.classify("garden")
        assert sl.semantic_class == "soft_landscape"
        assert sl.feature_type   == "region"

    def test_phase4b_path_alias(self, loader):
        """'path' aliases to 'path' (region polygon), not an edge class."""
        sl = loader.classify("path")
        assert sl.semantic_class == "path"
        assert sl.feature_type   == "region"
        assert sl.export_role    == "hatch_and_export"

    def test_phase4b_building_alias(self, loader):
        """'building' alias → canonical 'building'."""
        sl = loader.classify("building")
        assert sl.semantic_class == "building"
        assert sl.feature_type   == "region"

    def test_boundary_alias_resolves_to_site_boundary(self, loader):
        label = loader.classify("boundary")
        assert label.semantic_class == "site_boundary"
        assert label.feature_type == "region"
        assert label.export_role == "review"
        assert label.material_class == "MAT_BOUNDARY"

    def test_planting_alias_resolves_to_planting_bed(self, loader):
        label = loader.classify("planting")
        assert label.semantic_class == "planting_bed"
        assert label.feature_type == "region"

    def test_road_alias_resolves_to_road_carriageway(self, loader):
        label = loader.classify("road")
        assert label.semantic_class == "road_carriageway"
        assert label.feature_type == "region"
        assert label.export_role == "hatch_and_export"

    def test_site_boundary_direct_lookup_has_material(self, loader):
        """site_boundary must be in the class map with a non-empty material."""
        label = loader.classify("site_boundary")
        assert label.semantic_class == "site_boundary"
        assert label.material_class != ""


# ─── 8. TaxonomyLoader — noise terminal enforcement ──────────────────────────


class TestTaxonomyLoaderNoiseterminal:
    def test_noise_class_always_remove(self, loader):
        """noise classes must always resolve to export_role='remove'."""
        for cls in ("titleblock", "notes", "survey_reference"):
            sl = loader.classify(cls)
            assert sl.export_role == "remove", (
                f"noise class '{cls}' returned export_role='{sl.export_role}', expected 'remove'"
            )

    def test_noise_feature_type_correct(self, loader):
        for cls in ("titleblock", "notes", "survey_reference"):
            sl = loader.classify(cls)
            assert sl.feature_type == "noise"


# ─── 9. TaxonomyLoader — region material coverage ────────────────────────────


class TestTaxonomyLoaderMaterial:
    def test_all_region_classes_have_material(self, loader):
        """Every region class must carry a non-empty material_class."""
        region_classes = [
            "building", "site_boundary", "driveway", "parking_bay", "road_carriageway",
            "patio", "path", "footway", "hard_landscape",
            "soft_landscape", "front_garden", "rear_garden",
            "public_open_space", "planting_bed", "water", "attenuation_basin",
        ]
        for cls in region_classes:
            sl = loader.classify(cls)
            assert sl.feature_type == "region", f"{cls} should be region"
            assert sl.material_class != "", f"{cls} missing material_class"

    def test_non_region_classes_have_no_material(self, loader):
        """Non-region classes must carry empty material_class."""
        non_region = [
            ("kerb",         "linear"),
            ("parking_line", "marking"),
            ("bollard",      "symbol"),
            ("annotation",   "text"),
            ("titleblock",   "noise"),
        ]
        for cls, expected_type in non_region:
            sl = loader.classify(cls)
            assert sl.feature_type == expected_type, f"{cls}: expected {expected_type}"
            assert sl.material_class == "", f"{cls} should have empty material_class"

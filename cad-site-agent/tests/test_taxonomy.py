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
from cad_site_agent.semantic.taxonomy import SemanticLabel


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

"""
taxonomy.py — Phase 5

SemanticLabel  : frozen dataclass carrying the four canonical taxonomy fields.
TaxonomyLoader : loads semantic_taxonomy.yaml + export_roles.yaml, classifies
                 a semantic_class string into a SemanticLabel.

Public API
----------
    SemanticLabel(feature_type, semantic_class, export_role, material_class="")
    SemanticLabel.unknown()            → SemanticLabel for unrecognised input
    SemanticLabel.to_dict()            → dict with four canonical keys

    TaxonomyLoader(taxonomy_path, roles_path)
    TaxonomyLoader.classify(class_guess) → SemanticLabel
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


# ─── SemanticLabel ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SemanticLabel:
    """
    Immutable record of the four canonical taxonomy fields for one site class.

    Attributes
    ----------
    feature_type : str
        Geometric category: region | linear | marking | symbol | text |
        noise | unknown
    semantic_class : str
        Canonical class name from semantic_taxonomy.yaml, e.g. "parking_bay".
    export_role : str
        How this class is handled at export time, e.g. "hatch_and_export".
    material_class : str
        Hatch material code, e.g. "MAT_PARKING".  Empty string for all
        non-region feature types (material is only meaningful for filled areas).
    """

    feature_type:  str
    semantic_class: str
    export_role:   str
    material_class: str = field(default="")

    # ── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def unknown(cls) -> "SemanticLabel":
        """Return the canonical 'no match' sentinel."""
        return cls(
            feature_type="unknown",
            semantic_class="unknown",
            export_role="review",
            material_class="",
        )

    # ── Serialisation ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "feature_type":   self.feature_type,
            "semantic_class":  self.semantic_class,
            "export_role":    self.export_role,
            "material_class": self.material_class,
        }


# ─── TaxonomyLoader ──────────────────────────────────────────────────────────
# (Implemented in Task 4 — stub present so imports do not break.)


class TaxonomyLoader:
    """Loads YAML config and classifies a class_guess → SemanticLabel."""

    def __init__(
        self,
        taxonomy_path: Path,
        roles_path: Path,
    ) -> None:
        raise NotImplementedError("TaxonomyLoader implemented in Task 4")

    def classify(self, class_guess: str) -> SemanticLabel:
        raise NotImplementedError("TaxonomyLoader implemented in Task 4")

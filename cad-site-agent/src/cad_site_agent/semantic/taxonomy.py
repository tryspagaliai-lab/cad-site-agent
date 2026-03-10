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
from typing import Dict

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

# Feature types present as top-level list sections in semantic_taxonomy.yaml.
# The order here is irrelevant; every key is processed identically.
_FEATURE_TYPE_SECTIONS = ("region", "linear", "marking", "symbol", "text", "noise")

# The noise feature_type is terminal: no per-class export_role override is
# allowed to promote a noise class away from "remove".
_NOISE_FEATURE_TYPE = "noise"
_NOISE_EXPORT_ROLE  = "remove"


class TaxonomyLoader:
    """
    Loads semantic_taxonomy.yaml + export_roles.yaml and classifies a
    class_guess string into a SemanticLabel.

    Construction raises FileNotFoundError if either config file is absent.

    classify() resolves Phase 4B aliases (e.g. "parking" → "parking_bay"),
    then looks up the canonical class.  Unknown inputs return
    SemanticLabel.unknown().

    The noise feature_type is enforced as terminal: any noise-class entry
    always returns export_role="remove", regardless of any per-class
    export_role field in the YAML.
    """

    def __init__(
        self,
        taxonomy_path: Path,
        roles_path: Path,
    ) -> None:
        taxonomy_path = Path(taxonomy_path)
        roles_path    = Path(roles_path)

        if not taxonomy_path.exists():
            raise FileNotFoundError(f"Taxonomy file not found: {taxonomy_path}")
        if not roles_path.exists():
            raise FileNotFoundError(f"Roles file not found: {roles_path}")

        with taxonomy_path.open(encoding="utf-8") as fh:
            taxonomy_data: dict = yaml.safe_load(fh)

        with roles_path.open(encoding="utf-8") as fh:
            roles_data: dict = yaml.safe_load(fh)

        # default_by_type: feature_type → default export_role
        self._default_by_type: Dict[str, str] = roles_data.get("default_by_type", {})

        # alias_map: coarse Phase-4B name → canonical label
        self._alias_map: Dict[str, str] = dict(
            taxonomy_data.get("aliases", {}) or {}
        )

        # class_map: canonical label → SemanticLabel
        self._class_map: Dict[str, SemanticLabel] = {}

        for feature_type in _FEATURE_TYPE_SECTIONS:
            entries = taxonomy_data.get(feature_type) or []
            default_role = self._default_by_type.get(feature_type, "review")

            for entry in entries:
                if not isinstance(entry, dict):
                    continue

                label        = str(entry["label"])
                material_cls = str(entry.get("material", "") or "")

                # noise is terminal: ignore any per-class override
                if feature_type == _NOISE_FEATURE_TYPE:
                    export_role = _NOISE_EXPORT_ROLE
                else:
                    export_role = str(entry.get("export_role", "") or "") or default_role

                self._class_map[label] = SemanticLabel(
                    feature_type=feature_type,
                    semantic_class=label,
                    export_role=export_role,
                    material_class=material_cls,
                )

    # ── Public API ───────────────────────────────────────────────────────────

    def classify(self, class_guess: str) -> SemanticLabel:
        """
        Resolve class_guess → SemanticLabel.

        Resolution order:
          1. Apply alias if class_guess is a known Phase-4B coarse name.
          2. Look up the (possibly aliased) name in the class map.
          3. Return SemanticLabel.unknown() if not found.
        """
        canonical = self._alias_map.get(class_guess, class_guess)
        return self._class_map.get(canonical, SemanticLabel.unknown())

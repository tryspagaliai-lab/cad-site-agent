"""
Layer Normaliser — Phase 4 MVP.

Reads config/layer_aliases.yaml and applies rule-based layer name mapping.
Rules are checked in priority order: exact match → prefix → substring → regex.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
import ezdxf


# Canonical semantic classes
SEMANTIC_CLASSES = {
    "building", "driveway", "parking", "path", "road",
    "boundary", "planting", "water", "text", "annotation",
    "symbols", "unknown",
}


@dataclass
class NormalisationResult:
    source: str
    config: str
    layers_found: int
    layers_renamed: int
    unmapped: int
    mapping: dict[str, str]   # original → canonical
    unmapped_layers: list[str]
    output_path: str | None


def _load_aliases(config_path: str | Path) -> dict:
    """Load layer_aliases.yaml and return the parsed dict."""
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(f"Layer alias config not found: {p}")
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _match_layer(layer_name: str, rules: list[dict]) -> str | None:
    """
    Try each rule in priority order. Return canonical class name or None.
    Rule types: exact, prefix, substring, regex.
    """
    name_lower = layer_name.lower()
    for rule in rules:
        rtype = rule.get("type", "substring")
        pattern = rule.get("pattern", "").lower()
        canonical = rule.get("class")

        if rtype == "exact":
            if name_lower == pattern:
                return canonical
        elif rtype == "prefix":
            if name_lower.startswith(pattern):
                return canonical
        elif rtype == "substring":
            if pattern in name_lower:
                return canonical
        elif rtype == "regex":
            try:
                if re.search(pattern, name_lower):
                    return canonical
            except re.error:
                pass
    return None


def run_normalization(
    dxf_path: str | Path,
    config_path: str | Path = "config/layer_aliases.yaml",
    output_path: str | Path | None = None,
    rename_in_dxf: bool = True,
) -> dict[str, Any]:
    """
    Run layer normalisation.

    Args:
        dxf_path:       Input DXF.
        config_path:    Path to layer_aliases.yaml.
        output_path:    Output DXF path. If None, writes to <stem>_normalised.dxf.
        rename_in_dxf:  If True, renames layers in the DXF (sets new name).

    Returns:
        Dict with normalisation statistics.
    """
    path = Path(dxf_path)
    aliases = _load_aliases(config_path)
    rules: list[dict] = aliases.get("rules", [])

    doc = ezdxf.readfile(str(path))
    msp = doc.modelspace()

    mapping: dict[str, str] = {}
    unmapped: list[str] = []
    renamed_count = 0

    for layer_def in doc.layers:
        name = layer_def.dxf.name
        if name in ("0", "Defpoints"):
            continue
        canonical = _match_layer(name, rules)
        if canonical:
            mapping[name] = canonical
        else:
            unmapped.append(name)

    # Apply rename: update entity layer references + layer table
    # NOTE: ezdxf does not support renaming layer definitions directly.
    # Instead we rename all entities referencing the old layer, then add
    # a new layer definition with the canonical name (if not existing).
    if rename_in_dxf:
        for entity in msp:
            try:
                orig = entity.dxf.layer
                if orig in mapping:
                    canonical = mapping[orig]
                    entity.dxf.layer = canonical
            except Exception:
                pass

        # Create canonical layer definitions that don't exist yet
        existing_layers = {l.dxf.name for l in doc.layers}
        for canonical in set(mapping.values()):
            if canonical not in existing_layers:
                doc.layers.new(name=canonical)

        renamed_count = len(mapping)

    result = {
        "source": str(path),
        "config": str(config_path),
        "layers_found": len(list(doc.layers)),
        "layers_renamed": renamed_count,
        "unmapped": len(unmapped),
        "mapping": mapping,
        "unmapped_layers": unmapped,
        "output_path": None,
    }

    out = Path(output_path) if output_path else path.parent / f"{path.stem}_normalised.dxf"
    doc.saveas(str(out))
    result["output_path"] = str(out)

    return result

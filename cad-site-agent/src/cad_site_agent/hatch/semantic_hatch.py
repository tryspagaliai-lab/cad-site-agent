"""
semantic_hatch.py — Phase 4B

Orchestrator: load rules, match each closed region to a site class,
score with the confidence model, and return a list of HatchCandidates.

Public API
----------
    classify_hatch_candidates(dxf_path, report, *, rules_path, aliases_path)
        → list[HatchCandidate]
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from ..analyzer.dxf_analyzer import AnalysisReport
from .closed_regions import ClosedRegion, extract_closed_regions
from .confidence import score_candidate
from ..semantic.taxonomy import SemanticLabel, TaxonomyLoader


# ─── Default paths ──────────────────────────────────────────────────────────

_ROOT = Path(__file__).resolve().parents[3]  # …/cad-site-agent/
_DEFAULT_RULES   = _ROOT / "config" / "hatch_rules.yaml"
_DEFAULT_ALIASES = _ROOT / "config" / "layer_aliases.yaml"


# ─── Data class ─────────────────────────────────────────────────────────────


@dataclass
class HatchCandidate:
    """A single scored hatch candidate for one closed region."""

    region:         ClosedRegion
    class_guess:    str           # e.g. "parking", "building", "unknown"
    hatch_class:    str           # e.g. "MAT_PARKING", "REVIEW_UNKNOWN"
    confidence:     float         # 0.0 – 1.0
    status:         str           # "auto" | "review" | "skip"
    reasons:        list[str]     = field(default_factory=list)
    semantic_label: SemanticLabel = field(default_factory=SemanticLabel.unknown)

    def to_dict(self) -> dict:
        return {
            "region":         self.region.to_dict(),
            "class_guess":    self.class_guess,
            "hatch_class":    self.hatch_class,
            "confidence":     self.confidence,
            "status":         self.status,
            "reasons":        self.reasons,
            "semantic_label": self.semantic_label.to_dict(),
        }


# ─── YAML loaders ────────────────────────────────────────────────────────────


def _load_rules(rules_path: Path) -> dict[str, Any]:
    """Load and return the hatch_rules.yaml dict."""
    with open(rules_path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_alias_hints(aliases_path: Path) -> dict[str, list[str]]:
    """
    Parse layer_aliases.yaml into a supplementary {class: [keyword, ...]} dict.

    We extract the 'pattern' value from substring / prefix rules and group
    them by 'class'. This gives us an extra keyword source alongside the
    layer_hints section of hatch_rules.yaml.
    """
    with open(aliases_path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    hints: dict[str, list[str]] = {}
    rules = raw if isinstance(raw, list) else raw.get("rules", [])
    for rule in rules:
        rtype   = rule.get("type", "substring")
        pattern = rule.get("pattern", "")
        cls     = rule.get("class", "unknown")
        if rtype in ("substring", "prefix") and pattern:
            hints.setdefault(cls, []).append(pattern.lower())
    return hints


# ─── Layer matching ──────────────────────────────────────────────────────────


def _match_layer_to_class(
    layer_name: str,
    layer_hints: dict[str, list[str]],
) -> tuple[str, bool, int]:
    """
    Case-insensitive substring scan of *layer_name* against every keyword
    in *layer_hints*.

    Returns
    -------
    class_guess : str
        The best matching class, or "unknown".
    matched : bool
        True if at least one class matched.
    match_count : int
        Number of distinct classes whose keywords matched (> 1 → ambiguous).
    """
    lower_name = layer_name.lower()
    matched_classes: list[str] = []

    for cls, keywords in layer_hints.items():
        for kw in keywords:
            if kw in lower_name:
                if cls not in matched_classes:
                    matched_classes.append(cls)
                break  # one hit per class is enough

    if not matched_classes:
        return "unknown", False, 0

    # Return the first match as the primary guess (order defined in YAML)
    return matched_classes[0], True, len(matched_classes)


# ─── Layer-family HATCH detection ───────────────────────────────────────────


def _layer_has_hatch(layer_name: str, report: AnalysisReport) -> bool:
    """
    Return True if the region's own layer already contains HATCH entities,
    OR if any layer sharing the same prefix (up to the first '-' or '_')
    contains HATCH entities.
    """
    layer_info = report.layers.get(layer_name)
    if layer_info:
        if layer_info.entity_types.get("HATCH", 0) > 0:
            return True

    # Family prefix scan (e.g. "CB-P-PARKING" → prefix "CB")
    parts = re.split(r"[-_]", layer_name, maxsplit=1)
    if len(parts) > 1:
        prefix = parts[0].lower()
        for lname, linfo in report.layers.items():
            if lname.lower().startswith(prefix):
                if linfo.entity_types.get("HATCH", 0) > 0:
                    return True

    return False


# ─── Merge keyword hints ─────────────────────────────────────────────────────


def _merge_hints(
    base: dict[str, list[str]],
    extra: dict[str, list[str]],
) -> dict[str, list[str]]:
    """
    Merge *extra* keywords into *base* without duplicating entries.
    Returns a new dict.
    """
    merged: dict[str, list[str]] = {k: list(v) for k, v in base.items()}
    for cls, kws in extra.items():
        existing = {kw.lower() for kw in merged.get(cls, [])}
        for kw in kws:
            if kw.lower() not in existing:
                merged.setdefault(cls, []).append(kw)
    return merged


# ─── Public API ─────────────────────────────────────────────────────────────


def classify_hatch_candidates(
    dxf_path: str,
    report: AnalysisReport,
    *,
    rules_path:   Optional[str] = None,
    aliases_path: Optional[str] = None,
    class_filter: Optional[str] = None,
) -> list[HatchCandidate]:
    """
    Extract closed regions from *dxf_path*, classify each against site
    classes, score confidence, and return a list of HatchCandidates.

    Args:
        dxf_path:     Path to the DXF file.
        report:       AnalysisReport from dxf_analyzer (used for HATCH
                      presence per layer).
        rules_path:   Override path to hatch_rules.yaml.
        aliases_path: Override path to layer_aliases.yaml.
        class_filter: If set, only return candidates for this class.

    Returns:
        Sorted list of HatchCandidates by (status priority, confidence desc).
    """
    # ── Load config ───────────────────────────────────────────────────────
    rp = Path(rules_path) if rules_path else _DEFAULT_RULES
    ap = Path(aliases_path) if aliases_path else _DEFAULT_ALIASES

    rules = _load_rules(rp)

    thresholds      = rules.get("thresholds", {})
    scoring         = rules.get("scoring", {})
    region_cfg      = rules.get("region", {})
    class_to_mat    = rules.get("class_to_material", {})
    base_hints      = {k: list(v) for k, v in rules.get("layer_hints", {}).items()}
    area_hints: dict[str, dict[str, float]] = rules.get("area_hints", {})

    # Supplement with aliases if file exists
    if ap.exists():
        alias_hints = _load_alias_hints(ap)
        layer_hints = _merge_hints(base_hints, alias_hints)
    else:
        layer_hints = base_hints

    min_area     = float(region_cfg.get("min_area",     100.0))
    max_vertices = int(region_cfg.get("max_vertices", 5000))

    # ── Extract closed regions ─────────────────────────────────────────────
    regions = extract_closed_regions(
        dxf_path,
        min_area=min_area,
        max_vertices=max_vertices,
    )

    # ── Score each region ──────────────────────────────────────────────────
    candidates: list[HatchCandidate] = []

    for region in regions:
        class_guess, matched, match_count = _match_layer_to_class(
            region.source_layer, layer_hints
        )

        # Apply class filter if requested
        if class_filter and class_guess != class_filter:
            continue

        has_hatch = _layer_has_hatch(region.source_layer, report)

        confidence, status, reasons = score_candidate(
            region,
            class_guess,
            layer_matched=matched,
            match_count=match_count,
            layer_has_hatch=has_hatch,
            area_hints=area_hints,
            scoring=scoring,
            thresholds=thresholds,
        )

        hatch_class = class_to_mat.get(class_guess, "REVIEW_UNKNOWN")

        candidates.append(
            HatchCandidate(
                region=region,
                class_guess=class_guess,
                hatch_class=hatch_class,
                confidence=confidence,
                status=status,
                reasons=reasons,
            )
        )

    # ── Sort: auto first, then review, then skip; within each by confidence ↓
    _status_order = {"auto": 0, "review": 1, "skip": 2}
    candidates.sort(
        key=lambda c: (_status_order.get(c.status, 3), -c.confidence)
    )

    return candidates


# ─── Summary helpers ─────────────────────────────────────────────────────────


def summarise_candidates(candidates: list[HatchCandidate]) -> dict[str, Any]:
    """
    Return a lightweight summary dict (used by CLI + tests).
    """
    from collections import Counter

    by_status:  Counter[str] = Counter()
    by_class:   Counter[str] = Counter()
    by_layer:   Counter[str] = Counter()

    for c in candidates:
        by_status[c.status]             += 1
        by_class[c.class_guess]         += 1
        by_layer[c.region.source_layer] += 1

    return {
        "total":    len(candidates),
        "by_status": dict(by_status),
        "by_class":  dict(by_class.most_common(15)),
        "top_layers": dict(by_layer.most_common(10)),
    }

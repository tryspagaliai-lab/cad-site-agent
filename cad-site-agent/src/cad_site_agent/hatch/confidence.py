"""
confidence.py — Phase 4B

Additive confidence scoring for hatch candidates.

Each signal adds or subtracts a fixed delta (loaded from hatch_rules.yaml).
Final score is clamped to [0.0, 1.0] and mapped to a status:

  score >= thresholds.auto   → "auto"
  score >= thresholds.review → "review"
  else                       → "skip"
"""
from __future__ import annotations

from typing import Any

from .closed_regions import ClosedRegion


# ─── Scoring ────────────────────────────────────────────────────────────────


def score_candidate(
    region: ClosedRegion,
    class_guess: str,
    *,
    layer_matched: bool,
    match_count: int,
    layer_has_hatch: bool,
    area_hints: dict[str, dict[str, float]],
    scoring: dict[str, float],
    thresholds: dict[str, float],
) -> tuple[float, str, list[str]]:
    """
    Compute the confidence score for a single hatch candidate.

    Args:
        region:          The closed region.
        class_guess:     The site class guessed from the layer name.
        layer_matched:   True if the layer name matched any keyword hint.
        match_count:     Number of distinct classes the layer name matched
                         (> 1 means ambiguous).
        layer_has_hatch: True if the region's layer already has HATCH entities.
        area_hints:      Per-class {min, max} area ranges (from hatch_rules.yaml).
        scoring:         Score deltas keyed by signal name.
        thresholds:      {"auto": float, "review": float}.

    Returns:
        (confidence, status, reasons)
    """
    score = 0.0
    reasons: list[str] = []

    # ── Layer name signal ──────────────────────────────────────────────────
    if layer_matched and class_guess != "unknown":
        score += scoring.get("strong_layer_signal", 0.45)
        reasons.append(f"Layer name matches class '{class_guess}'")

        # Bonus: layer family already has HATCHes in the DXF
        if layer_has_hatch:
            score += scoring.get("hatch_in_layer_family", 0.15)
            reasons.append("Layer already contains HATCH entities")

    # ── Ambiguity penalty ─────────────────────────────────────────────────
    if match_count > 1:
        score += scoring.get("ambiguous_overlap_penalty", -0.20)
        reasons.append(
            f"Layer name matched {match_count} classes (ambiguous)"
        )

    # ── Area heuristics ──────────────────────────────────────────────────
    if class_guess in area_hints:
        lo = area_hints[class_guess].get("min", 0.0)
        hi = area_hints[class_guess].get("max", float("inf"))
        if lo <= region.area <= hi:
            score += scoring.get("shape_heuristic_match", 0.20)
            reasons.append(
                f"Area {region.area:,.0f} mm² is within expected range "
                f"for '{class_guess}' [{lo:,.0f}–{hi:,.0f}]"
            )
        else:
            score += scoring.get("suspicious_size_penalty", -0.15)
            reasons.append(
                f"Area {region.area:,.0f} mm² is outside expected range "
                f"for '{class_guess}' [{lo:,.0f}–{hi:,.0f}]"
            )

    # ── Clamp ─────────────────────────────────────────────────────────────
    score = max(0.0, min(1.0, score))

    # ── Status mapping ───────────────────────────────────────────────────
    if score >= thresholds.get("auto", 0.75):
        status = "auto"
    elif score >= thresholds.get("review", 0.45):
        status = "review"
    else:
        status = "skip"

    return round(score, 4), status, reasons

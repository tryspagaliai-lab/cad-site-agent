"""
Drawing Type Classifier — Phase 4A.

New taxonomy (replaces Phase 2 site_layout/planning_layout/detail/schematic):
  rich_site_layout   — semantic site DXF with hatches, closed regions, many classes
  sparse_linework    — draft DXF: lots of LINE/LWPOLYLINE, few semantics, no hatch
  illustrator_derived — exported from Illustrator: high SPLINE count
  max_prep           — 3ds Max prep / model: material/mesh/3d layer names, 3D geometry
  unknown            — insufficient signal to classify

Each result includes: label, confidence (0–1), reasons[]
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..analyzer.dxf_analyzer import AnalysisReport


# ── Semantic layer keyword sets ────────────────────────────────────────────────

SITE_CLASSES = {
    "parking", "driveway", "path", "road", "grass", "planting",
    "boundary", "building", "footpath", "pavement", "paving",
    "hoggin", "asphalt", "grasscrete", "tree", "garden", "lawn",
    "shrub", "kerb", "carriageway", "fence", "water", "pond",
    "swale", "drain", "plot", "curtilage",
}

# Keywords indicating a 3ds Max / mesh-prep / BIM workflow layer
MAX_PREP_KEYWORDS = {
    "material", "working", "mesh", "3d", "model", "prep",
    "maxscript", "bim", "solid", "shell", "surface", "render",
    "export", "ref-plane",
}


# ── Result dataclass ───────────────────────────────────────────────────────────

@dataclass
class DrawingTypeResult:
    label: str = "unknown"           # rich_site_layout | sparse_linework | illustrator_derived | max_prep | unknown
    confidence: float = 0.0          # 0.0–1.0
    reasons: list[str] = field(default_factory=list)

    # Diagnostic counts (filled in by classifier)
    spline_count: int = 0
    hatch_count: int = 0
    insert_count: int = 0
    semantic_class_count: int = 0    # unique site classes detected in layer names

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "confidence": round(self.confidence, 3),
            "reasons": self.reasons,
            "diagnostics": {
                "spline_count": self.spline_count,
                "hatch_count": self.hatch_count,
                "insert_count": self.insert_count,
                "semantic_class_count": self.semantic_class_count,
            },
        }


# ── Semantic layer analysis helper ─────────────────────────────────────────────

def _semantic_class_hits(layer_names: list[str]) -> set[str]:
    """Return site-class keywords found across all layer names."""
    hits: set[str] = set()
    for name in layer_names:
        name_lower = name.lower()
        for kw in SITE_CLASSES:
            if kw in name_lower:
                hits.add(kw)
    return hits


def _max_prep_layer_count(layer_names: list[str]) -> int:
    """Count layers whose names suggest 3ds Max / mesh-prep workflow."""
    count = 0
    for name in layer_names:
        name_lower = name.lower()
        if any(kw in name_lower for kw in MAX_PREP_KEYWORDS):
            count += 1
    return count


# ── Main classifier ────────────────────────────────────────────────────────────

def classify_drawing_type(report: AnalysisReport) -> DrawingTypeResult:
    """
    Classify a DXF using heuristic scoring into one of 5 types.

    Heuristics:
      illustrator_derived: large SPLINE count (>20 or >2% of total)
      rich_site_layout:    many HATCH + many semantic site layer classes (>=3)
      sparse_linework:     no/few hatch + high LINE/LWPOLYLINE ratio + few semantics
      max_prep:            layer names with material/mesh/3d/model/working keywords
      unknown:             insufficient signal
    """
    result = DrawingTypeResult()

    total = max(report.total_entities, 1)
    etypes = report.entity_type_counts

    spline_count = etypes.get("SPLINE", 0)
    hatch_count  = etypes.get("HATCH", 0)
    insert_count = etypes.get("INSERT", 0)
    line_count   = etypes.get("LINE", 0)
    lwpoly_count = etypes.get("LWPOLYLINE", 0)

    result.spline_count  = spline_count
    result.hatch_count   = hatch_count
    result.insert_count  = insert_count

    layer_names = list(report.layers.keys())
    semantic_hits = _semantic_class_hits(layer_names)
    result.semantic_class_count = len(semantic_hits)

    max_layer_count = _max_prep_layer_count(layer_names)

    # ── Score each candidate ───────────────────────────────────────────────────

    scores: dict[str, float] = {
        "illustrator_derived": 0.0,
        "rich_site_layout":    0.0,
        "sparse_linework":     0.0,
        "max_prep":            0.0,
    }
    reasons: dict[str, list[str]] = {k: [] for k in scores}

    # ── illustrator_derived ────────────────────────────────────────────────────
    spline_ratio = spline_count / total
    if spline_count >= 50:
        scores["illustrator_derived"] += 0.6
        reasons["illustrator_derived"].append(f"Very high SPLINE count: {spline_count}")
    elif spline_count >= 20:
        scores["illustrator_derived"] += 0.4
        reasons["illustrator_derived"].append(f"High SPLINE count: {spline_count}")
    elif spline_count >= 5:
        scores["illustrator_derived"] += 0.15
        reasons["illustrator_derived"].append(f"Moderate SPLINE count: {spline_count}")

    if spline_ratio > 0.05:
        scores["illustrator_derived"] += 0.3
        reasons["illustrator_derived"].append(f"SPLINEs are {spline_ratio:.1%} of all entities")
    elif spline_ratio > 0.01:
        scores["illustrator_derived"] += 0.1

    # ── rich_site_layout ───────────────────────────────────────────────────────
    if hatch_count >= 30:
        scores["rich_site_layout"] += 0.35
        reasons["rich_site_layout"].append(f"Many HATCH entities: {hatch_count}")
    elif hatch_count >= 5:
        scores["rich_site_layout"] += 0.2
        reasons["rich_site_layout"].append(f"HATCH entities present: {hatch_count}")

    n_sem = result.semantic_class_count
    if n_sem >= 5:
        scores["rich_site_layout"] += 0.4
        reasons["rich_site_layout"].append(
            f"Rich semantic layer vocabulary ({n_sem} site classes): {', '.join(sorted(semantic_hits)[:8])}")
    elif n_sem >= 3:
        scores["rich_site_layout"] += 0.25
        reasons["rich_site_layout"].append(
            f"Semantic site layers present ({n_sem} classes): {', '.join(sorted(semantic_hits))}")
    elif n_sem >= 1:
        scores["rich_site_layout"] += 0.1

    if report.closed_polyline_count > 100:
        scores["rich_site_layout"] += 0.1
        reasons["rich_site_layout"].append(f"Many closed polylines: {report.closed_polyline_count}")

    if insert_count > 20:
        scores["rich_site_layout"] += 0.05
        reasons["rich_site_layout"].append(f"Block inserts (symbols/trees): {insert_count}")

    # ── sparse_linework ────────────────────────────────────────────────────────
    if hatch_count == 0:
        scores["sparse_linework"] += 0.2
        reasons["sparse_linework"].append("No HATCH entities")
    elif hatch_count < 5:
        scores["sparse_linework"] += 0.08

    linework_ratio = (line_count + lwpoly_count) / total
    if linework_ratio >= 0.7:
        scores["sparse_linework"] += 0.35
        reasons["sparse_linework"].append(f"Line/polyline ratio very high: {linework_ratio:.1%}")
    elif linework_ratio >= 0.5:
        scores["sparse_linework"] += 0.2
        reasons["sparse_linework"].append(f"Line/polyline dominant: {linework_ratio:.1%}")

    if n_sem == 0:
        scores["sparse_linework"] += 0.25
        reasons["sparse_linework"].append("No semantic site-class keywords in layer names")
    elif n_sem <= 1:
        scores["sparse_linework"] += 0.1

    if report.total_layers < 20 and n_sem == 0:
        scores["sparse_linework"] += 0.1
        reasons["sparse_linework"].append(f"Low layer count ({report.total_layers}) with no semantics")

    # ── max_prep ───────────────────────────────────────────────────────────────
    if max_layer_count >= 5:
        scores["max_prep"] += 0.4
        reasons["max_prep"].append(f"{max_layer_count} layers with 3D/mesh/material keywords")
    elif max_layer_count >= 2:
        scores["max_prep"] += 0.2
        reasons["max_prep"].append(f"{max_layer_count} layers with mesh/material keywords")

    if report.has_3d:
        scores["max_prep"] += 0.3
        reasons["max_prep"].append("3D geometry detected (non-default extrusion)")

    # ── Pick best ─────────────────────────────────────────────────────────────
    best_label = max(scores, key=lambda k: scores[k])
    best_score = scores[best_label]

    THRESHOLD = 0.25   # minimum score to commit to a label

    if best_score >= THRESHOLD:
        result.label = best_label
        result.confidence = min(best_score, 1.0)
        result.reasons = reasons[best_label]
    else:
        result.label = "unknown"
        result.confidence = 0.0
        result.reasons = [
            f"Highest score {best_score:.2f} ({best_label}) below threshold {THRESHOLD}",
            f"SPLINE:{spline_count} HATCH:{hatch_count} LINE:{line_count} LWPOLY:{lwpoly_count}",
            f"Semantic site classes: {n_sem}",
        ]

    return result

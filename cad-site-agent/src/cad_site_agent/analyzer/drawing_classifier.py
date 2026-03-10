"""
Drawing Classifier — Phase 2.

Inspects an AnalysisReport and emits a DrawingClassification:
  - drawing_type: site_layout | planning_layout | detail | schematic | unknown
  - confidence: 0.0–1.0
  - detected_themes: list of site element themes found
  - notes: reasoning
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .dxf_analyzer import AnalysisReport


SITE_LAYOUT_KEYWORDS = {
    "parking", "driveway", "path", "road", "grass", "planting",
    "boundary", "building", "footpath", "pavement", "paving",
    "hoggin", "asphalt", "grasscrete", "tree", "garden",
}

PLANNING_KEYWORDS = {
    "planning", "proposed", "existing", "masterplan", "layout",
    "site", "block", "plot", "curtilage",
}

DETAIL_KEYWORDS = {
    "detail", "section", "elevation", "foundation", "kerb",
    "drainage", "threshold", "nosing",
}

ANNOTATION_LAYERS = {"text", "anno", "dim", "note", "label", "tag", "no", "number"}


@dataclass
class DrawingClassification:
    drawing_type: str = "unknown"
    confidence: float = 0.0
    detected_themes: list[str] = field(default_factory=list)
    layer_count: int = 0
    entity_count: int = 0
    text_count: int = 0
    annotation_layer_count: int = 0
    geometry_layer_count: int = 0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "drawing_type": self.drawing_type,
            "confidence": round(self.confidence, 3),
            "detected_themes": self.detected_themes,
            "layer_count": self.layer_count,
            "entity_count": self.entity_count,
            "text_count": self.text_count,
            "annotation_layer_count": self.annotation_layer_count,
            "geometry_layer_count": self.geometry_layer_count,
            "notes": self.notes,
        }


def classify_drawing(report: AnalysisReport) -> DrawingClassification:
    cls = DrawingClassification(
        layer_count=report.total_layers,
        entity_count=report.total_entities,
        text_count=len(report.text_entries),
    )

    all_layers_lower = [name.lower() for name in report.layers.keys()]
    all_text_lower = [t.content.lower() for t in report.text_entries]

    # --- Theme detection ---
    themes_found: set[str] = set()
    for layer_lower in all_layers_lower:
        for kw in SITE_LAYOUT_KEYWORDS:
            if kw in layer_lower:
                themes_found.add(kw)
        for kw in PLANNING_KEYWORDS:
            if kw in layer_lower:
                themes_found.add(kw)
        for kw in DETAIL_KEYWORDS:
            if kw in layer_lower:
                themes_found.add(kw)

    for text_lower in all_text_lower[:200]:
        for kw in SITE_LAYOUT_KEYWORDS | PLANNING_KEYWORDS:
            if kw in text_lower:
                themes_found.add(kw)

    cls.detected_themes = sorted(themes_found)

    # --- Annotation vs geometry layers ---
    for name_lower in all_layers_lower:
        is_anno = any(a in name_lower for a in ANNOTATION_LAYERS)
        if is_anno:
            cls.annotation_layer_count += 1
        else:
            cls.geometry_layer_count += 1

    # --- Classification scoring ---
    site_score = 0.0
    planning_score = 0.0
    detail_score = 0.0

    site_hits = themes_found & SITE_LAYOUT_KEYWORDS
    planning_hits = themes_found & PLANNING_KEYWORDS
    detail_hits = themes_found & DETAIL_KEYWORDS

    site_score += min(len(site_hits) * 0.15, 0.6)
    planning_score += min(len(planning_hits) * 0.15, 0.4)
    detail_score += min(len(detail_hits) * 0.2, 0.5)

    # Large layer count = complex master / planning layout
    if report.total_layers > 500:
        planning_score += 0.3
        cls.notes.append(f"Very high layer count ({report.total_layers}) — likely planning/master layout")
    elif report.total_layers > 50:
        site_score += 0.1

    # Hatch presence typical in site layouts
    if report.has_hatches:
        site_score += 0.1
        cls.notes.append("Hatch entities present — consistent with site layout fill areas")

    # Block inserts = symbols (tree, sign etc)
    if report.has_blocks:
        site_score += 0.05

    # Unit heuristic
    if report.likely_unit == "mm":
        site_score += 0.05
        cls.notes.append("Coordinates likely in mm (typical for architectural/site DXF)")

    best_score = max(site_score, planning_score, detail_score, 0.0)
    if best_score == site_score and site_score > 0.2:
        cls.drawing_type = "site_layout"
        cls.confidence = min(site_score, 1.0)
    elif best_score == planning_score and planning_score > 0.2:
        cls.drawing_type = "planning_layout"
        cls.confidence = min(planning_score, 1.0)
    elif best_score == detail_score and detail_score > 0.2:
        cls.drawing_type = "detail"
        cls.confidence = min(detail_score, 1.0)
    else:
        cls.drawing_type = "unknown"
        cls.confidence = 0.0
        cls.notes.append("Insufficient layer/text keywords to classify confidently")

    if site_hits:
        cls.notes.append(f"Site keywords found: {', '.join(sorted(site_hits))}")
    if planning_hits:
        cls.notes.append(f"Planning keywords found: {', '.join(sorted(planning_hits))}")

    return cls

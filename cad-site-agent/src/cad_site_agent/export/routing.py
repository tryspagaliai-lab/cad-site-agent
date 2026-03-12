"""
routing.py — Phase 7

Non-region entity routing: maps export_role / feature_group to destination
DXF layers, copies linear / marking / symbol / text entities from the source
DXF to an output DXF, and removes noise entities.

Public API
----------
    ROLE_TO_GROUP          : dict[str, str]
    GROUP_TO_PREFIX        : dict[str, str]
    destination_layer(feature_group, semantic_class) -> str
    classify_layer_name(layer_name, *, taxonomy, routing_hints) -> SemanticLabel
    RoutingReport          : dataclass
    run_route_features(source_dxf, candidates_json, output_dxf, **kwargs)
        -> RoutingReport
    write_routing_reports(report, output_dir, stem) -> tuple[Path, Path]
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import ezdxf

from ..semantic.taxonomy import SemanticLabel, TaxonomyLoader


# ─── Constants ───────────────────────────────────────────────────────────────

#: Map export_role → feature_group (only non-region roles are routed here).
ROLE_TO_GROUP: dict[str, str] = {
    "keep_linework": "linear",
    "keep_markings": "marking",
    "keep_symbols":  "symbol",
    "keep_text":     "text",
    "remove":        "noise",
}

#: Map feature_group → output layer prefix.
GROUP_TO_PREFIX: dict[str, str] = {
    "linear":  "LINEWORK",
    "marking": "MARKING",
    "symbol":  "SYMBOL",
    "text":    "TEXT",
}

#: Entity types that belong to each feature_group.
#: Used to filter entities from the source DXF.
_GROUP_ENTITY_TYPES: dict[str, tuple[str, ...]] = {
    "linear":  ("LINE", "LWPOLYLINE", "POLYLINE", "ARC", "SPLINE", "CIRCLE"),
    "marking": ("LINE", "LWPOLYLINE", "POLYLINE", "ARC", "HATCH", "SOLID"),
    "symbol":  ("INSERT", "POINT", "CIRCLE", "ARC"),
    "text":    ("TEXT", "MTEXT", "DIMENSION", "LEADER", "MULTILEADER"),
}

#: Default config paths (relative to project root).
_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_TAXONOMY = _ROOT / "config" / "semantic_taxonomy.yaml"
_DEFAULT_ROLES    = _ROOT / "config" / "export_roles.yaml"

#: Built-in routing keyword hints for non-region semantic classes.
#: Keys are canonical semantic_class labels from the taxonomy;
#: values are lists of case-insensitive substrings to match in layer names.
DEFAULT_ROUTING_HINTS: dict[str, list[str]] = {
    # linear
    "fence":          ["fence", "fencing"],
    "wall":           ["wall", "walling"],
    "kerb":           ["kerb", "curb", "kerbline"],
    "road_edge":      ["road-edge", "road_edge", "rd-edge"],
    "path_edge":      ["path-edge", "path_edge"],
    "hedge":          ["hedge"],
    "drain":          ["drain", "drainage"],
    "retaining_wall": ["retaining", "ret-wall", "ret_wall"],
    # marking
    "parking_line":    ["parking-line", "parking_line", "park-marking", "parkline"],
    "crossing_marking":["crossing", "zebra"],
    "bus_stop_marking":["bus-stop", "bus_stop", "busstop"],
    "road_marking":    ["road-marking", "road_marking", "rdmarking"],
    # symbol
    "tree":     ["tree"],
    "shrub":    ["shrub", "bush"],
    "bollard":  ["bollard"],
    "gate":     ["gate"],
    "lamp_post":["lamp", "lamppost", "lamp-post", "street-light"],
    "signage":  ["sign", "signage"],
    # text
    "annotation":    ["annotation", "annot"],
    "dimension":     ["dim", "dimension"],
    "label":         ["label"],
    "plot_number":   ["plot-no", "plot_no", "plot-number", "plot_number", "plotno"],
    "parking_number":["parking-no", "parking_no", "park-no"],
    "street_name":   ["street-name", "street_name", "streetname", "road-name"],
    # noise
    "titleblock":      ["titleblock", "title-block", "title_block", "tb"],
    "notes":           ["notes", "notation"],
    "survey_reference":["survey-ref", "survey_ref", "surveyref", "survey-control",
                        "control-point"],
}


# ─── Layer name classification ────────────────────────────────────────────────


def classify_layer_name(
    layer_name: str,
    *,
    taxonomy: TaxonomyLoader,
    routing_hints: Optional[dict[str, list[str]]] = None,
) -> SemanticLabel:
    """Match *layer_name* to a SemanticLabel using routing keyword hints.

    Resolution order:
      1. Case-insensitive substring search through *routing_hints*.
         The first match (by dict iteration order) wins.
      2. Look up the matched class_guess in *taxonomy*.
      3. Return SemanticLabel.unknown() if no match.

    Args:
        layer_name:    Raw layer name from the source DXF.
        taxonomy:      Loaded TaxonomyLoader instance.
        routing_hints: Override hints dict; defaults to DEFAULT_ROUTING_HINTS.

    Returns:
        SemanticLabel for the best-matching class, or SemanticLabel.unknown().
    """
    hints = routing_hints if routing_hints is not None else DEFAULT_ROUTING_HINTS
    lower = layer_name.lower()

    for class_guess, keywords in hints.items():
        for kw in keywords:
            if kw.lower() in lower:
                return taxonomy.classify(class_guess)

    return SemanticLabel.unknown()


# ─── Layer naming ────────────────────────────────────────────────────────────


def destination_layer(feature_group: str, semantic_class: str) -> str:
    """Return the output DXF layer name for a routed entity.

    Examples:
        destination_layer("linear", "fence")         → "LINEWORK_FENCE"
        destination_layer("marking", "parking_line") → "MARKING_PARKING_LINE"
        destination_layer("symbol", "bollard")       → "SYMBOL_BOLLARD"
        destination_layer("text", "plot_number")     → "TEXT_PLOT_NUMBER"
    """
    prefix = GROUP_TO_PREFIX.get(feature_group, feature_group.upper())
    suffix = semantic_class.upper()
    return f"{prefix}_{suffix}"


# ─── RoutingReport ────────────────────────────────────────────────────────────


@dataclass
class RoutingReport:
    """Immutable summary of one route-features run."""

    source_dxf:      str
    candidates_json: str
    output_dxf:      str
    generated_at:    str

    total_input:     int       # total entities examined in source DXF
    total_written:   int       # entities copied to output DXF
    total_removed:   int       # noise entities suppressed
    total_skipped:   int       # region / unknown / error entities

    by_feature_type:   dict[str, int] = field(default_factory=dict)
    by_semantic_class: dict[str, int] = field(default_factory=dict)
    by_export_role:    dict[str, int] = field(default_factory=dict)
    by_dest_layer:     dict[str, int] = field(default_factory=dict)
    unknowns:          int = 0


# ─── run_route_features ───────────────────────────────────────────────────────


def run_route_features(
    source_dxf: str,
    candidates_json: str,
    output_dxf: str,
    *,
    include_linework: bool = True,
    include_markings: bool = True,
    include_symbols:  bool = True,
    include_text:     bool = True,
    exclude_noise:    bool = True,
    taxonomy_path:    Optional[str] = None,
    roles_path:       Optional[str] = None,
    routing_hints:    Optional[dict[str, list[str]]] = None,
) -> RoutingReport:
    """Route non-region DXF entities to appropriate output layers.

    Reads every entity from the source DXF modelspace, classifies it by
    layer name via routing_hints + taxonomy, and copies it to the output DXF
    on the appropriate destination layer.

    Safety rules
    ------------
    - Raises FileNotFoundError if source DXF or candidates JSON is absent.
    - Raises FileExistsError if output DXF already exists.
    - Never modifies the source DXF.
    - Always creates an output DXF (empty when no entities are routed).

    Args:
        source_dxf:       Path to source DXF (read-only).
        candidates_json:  Path to hatch_candidates or analysis JSON
                          (used for metadata only; routing is layer-based).
        output_dxf:       Path for the new output DXF.
        include_linework: Copy linear entities (default True).
        include_markings: Copy marking entities (default True).
        include_symbols:  Copy symbol entities (default True).
        include_text:     Copy text entities (default True).
        exclude_noise:    Suppress noise entities (default True).
        taxonomy_path:    Override path to semantic_taxonomy.yaml.
        roles_path:       Override path to export_roles.yaml.
        routing_hints:    Override routing keyword hints dict.

    Returns:
        RoutingReport with counts by feature type, semantic class, and layer.
    """
    src_path  = Path(source_dxf)
    json_path = Path(candidates_json)
    out_path  = Path(output_dxf)

    if not src_path.exists():
        raise FileNotFoundError(f"Source DXF not found: {source_dxf}")
    if not json_path.exists():
        raise FileNotFoundError(f"Candidates JSON not found: {candidates_json}")
    if out_path.exists():
        raise FileExistsError(f"Output DXF already exists: {output_dxf}")

    # Load taxonomy
    tp = Path(taxonomy_path) if taxonomy_path else _DEFAULT_TAXONOMY
    rp = Path(roles_path)    if roles_path    else _DEFAULT_ROLES
    taxonomy = TaxonomyLoader(tp, rp)

    # Determine which groups are enabled
    enabled_groups: set[str] = set()
    if include_linework: enabled_groups.add("linear")
    if include_markings: enabled_groups.add("marking")
    if include_symbols:  enabled_groups.add("symbol")
    if include_text:     enabled_groups.add("text")

    # Open source DXF (read-only)
    source_doc = ezdxf.readfile(str(src_path))
    source_msp = source_doc.modelspace()

    # Create output DXF
    out_doc = ezdxf.new("R2010")
    out_msp = out_doc.modelspace()

    # Counters
    total_input   = 0
    total_written = 0
    total_removed = 0
    total_skipped = 0
    unknowns      = 0

    by_feature_type:   dict[str, int] = {}
    by_semantic_class: dict[str, int] = {}
    by_export_role:    dict[str, int] = {}
    by_dest_layer:     dict[str, int] = {}

    for entity in source_msp:
        total_input += 1
        layer_name = entity.dxf.get("layer", "0")

        sem = classify_layer_name(
            layer_name,
            taxonomy=taxonomy,
            routing_hints=routing_hints,
        )

        feature_type = sem.feature_type
        export_role  = sem.export_role
        sem_class    = sem.semantic_class

        # Count by feature_type / export_role
        by_feature_type[feature_type]   = by_feature_type.get(feature_type, 0) + 1
        by_export_role[export_role]     = by_export_role.get(export_role, 0) + 1

        # Unknown → skip
        if feature_type == "unknown":
            unknowns += 1
            total_skipped += 1
            continue

        # Region → skip (handled by write-hatches pipeline)
        if feature_type == "region":
            total_skipped += 1
            continue

        # Noise → remove if exclude_noise
        if feature_type == "noise":
            if exclude_noise:
                total_removed += 1
                by_semantic_class[sem_class] = (
                    by_semantic_class.get(sem_class, 0) + 1
                )
            else:
                total_skipped += 1
            continue

        # Non-region, non-noise: check if group is enabled
        feature_group = ROLE_TO_GROUP.get(export_role, "")
        if not feature_group or feature_group not in enabled_groups:
            total_skipped += 1
            continue

        # Copy entity to output with destination layer
        dest = destination_layer(feature_group, sem_class)

        try:
            new_entity = entity.copy()
            new_entity.dxf.layer = dest
            out_msp.add_entity(new_entity)

            if dest not in out_doc.layers:
                out_doc.layers.add(dest)

            total_written += 1
            by_semantic_class[sem_class] = by_semantic_class.get(sem_class, 0) + 1
            by_dest_layer[dest]          = by_dest_layer.get(dest, 0) + 1

        except Exception:
            total_skipped += 1

    out_doc.saveas(str(out_path))

    return RoutingReport(
        source_dxf=str(source_dxf),
        candidates_json=str(candidates_json),
        output_dxf=str(output_dxf),
        generated_at=datetime.now().isoformat(timespec="seconds"),
        total_input=total_input,
        total_written=total_written,
        total_removed=total_removed,
        total_skipped=total_skipped,
        by_feature_type=by_feature_type,
        by_semantic_class=by_semantic_class,
        by_export_role=by_export_role,
        by_dest_layer=by_dest_layer,
        unknowns=unknowns,
    )


# ─── write_routing_reports ────────────────────────────────────────────────────


def write_routing_reports(
    report: RoutingReport,
    output_dir: str,
    stem: str,
) -> tuple[Path, Path]:
    """Write *report* to ``{stem}.routing.json`` and ``{stem}.routing.md``.

    Returns (json_path, md_path).
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    json_path = out / f"{stem}.routing.json"
    md_path   = out / f"{stem}.routing.md"

    # ── JSON ──────────────────────────────────────────────────────────────
    payload = {
        "meta": {
            "source_dxf":      report.source_dxf,
            "candidates_json": report.candidates_json,
            "output_dxf":      report.output_dxf,
            "generated_at":    report.generated_at,
        },
        "totals": {
            "input":   report.total_input,
            "written": report.total_written,
            "removed": report.total_removed,
            "skipped": report.total_skipped,
            "unknowns": report.unknowns,
        },
        "by_feature_type":   report.by_feature_type,
        "by_semantic_class": report.by_semantic_class,
        "by_export_role":    report.by_export_role,
        "by_dest_layer":     report.by_dest_layer,
    }
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # ── Markdown ──────────────────────────────────────────────────────────
    lines: list[str] = [
        f"# Routing Report — {stem}",
        "",
        f"**Generated:** {report.generated_at}  ",
        f"**Source DXF:** `{report.source_dxf}`  ",
        f"**Candidates JSON:** `{report.candidates_json}`  ",
        f"**Output DXF:** `{report.output_dxf}`",
        "",
        "---",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Input entities   | {report.total_input:,} |",
        f"| Written          | {report.total_written:,} |",
        f"| Removed (noise)  | {report.total_removed:,} |",
        f"| Skipped          | {report.total_skipped:,} |",
        f"| Unknowns         | {report.unknowns:,} |",
        "",
    ]

    if report.by_feature_type:
        lines += [
            "---",
            "",
            "## By Feature Type",
            "",
            "| Feature Type | Count |",
            "|--------------|-------|",
        ]
        for ft, cnt in sorted(report.by_feature_type.items()):
            lines.append(f"| {ft} | {cnt:,} |")
        lines.append("")

    if report.by_semantic_class:
        lines += [
            "---",
            "",
            "## By Semantic Class",
            "",
            "| Semantic Class | Count |",
            "|----------------|-------|",
        ]
        for sc, cnt in sorted(report.by_semantic_class.items(), key=lambda x: -x[1]):
            lines.append(f"| {sc} | {cnt:,} |")
        lines.append("")

    if report.by_dest_layer:
        lines += [
            "---",
            "",
            "## By Destination Layer",
            "",
            "| Layer | Count |",
            "|-------|-------|",
        ]
        for layer, cnt in sorted(report.by_dest_layer.items()):
            lines.append(f"| `{layer}` | {cnt:,} |")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

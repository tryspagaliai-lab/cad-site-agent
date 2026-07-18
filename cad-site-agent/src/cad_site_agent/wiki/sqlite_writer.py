"""
sqlite_writer.py — cad-3d P0 stage C: pipeline report JSONs → SQLite fact store.

Deterministic (no LLM anywhere): the same input reports produce identical
database content, except the ``ingested_at`` timestamp column. Writes are
transactional; re-ingesting a stem replaces its previous rows.

Input contract per drawing (all in one directory):
    <stem>.analysis.json           required   (analyzer + classification)
    <stem>.hatch_candidates.json   optional   (regions)
    <stem>.routing.json            optional   (feature routing aggregates)

Public API
----------
    WikiDbReport
    ingest_reports(analysis_jsons, db_path) -> WikiDbReport
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ..export.routing import classify_layer_name
from ..semantic.taxonomy import TaxonomyLoader

_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_TAXONOMY = _ROOT / "config" / "semantic_taxonomy.yaml"
_DEFAULT_ROLES    = _ROOT / "config" / "export_roles.yaml"

ANALYSIS_SUFFIX = ".analysis.json"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS drawings (
    id            INTEGER PRIMARY KEY,
    stem          TEXT NOT NULL UNIQUE,
    source_path   TEXT,
    source_format TEXT,
    drawing_type  TEXT,
    confidence    REAL,
    units         TEXT,
    scale_status  TEXT,
    ingested_at   TEXT
);
CREATE TABLE IF NOT EXISTS layers (
    drawing_id     INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    name           TEXT NOT NULL,
    entity_count   INTEGER,
    semantic_class TEXT,
    feature_type   TEXT,
    export_role    TEXT
);
CREATE TABLE IF NOT EXISTS regions (
    drawing_id   INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    region_id    INTEGER,
    source_layer TEXT,
    class_guess  TEXT,
    hatch_class  TEXT,
    confidence   REAL,
    status       TEXT,
    area         REAL,
    perimeter    REAL,
    bbox         TEXT
);
CREATE TABLE IF NOT EXISTS texts (
    drawing_id INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    layer      TEXT,
    content    TEXT,
    x          REAL,
    y          REAL
);
CREATE TABLE IF NOT EXISTS routing (
    drawing_id INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    dimension  TEXT NOT NULL,
    key        TEXT NOT NULL,
    count      INTEGER
);
CREATE TABLE IF NOT EXISTS wiki_nodes (
    drawing_id   INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    path         TEXT,
    generated_at TEXT
);
CREATE TABLE IF NOT EXISTS wiki_links (
    from_drawing_id INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    to_drawing_id   INTEGER NOT NULL REFERENCES drawings(id) ON DELETE CASCADE,
    shared_class    TEXT NOT NULL
);
"""


@dataclass
class WikiDbReport:
    db_path: str
    drawings_ingested: list[str] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)     # stem/path -> reason

    def to_dict(self) -> dict:
        return {"db_path": self.db_path,
                "drawings_ingested": self.drawings_ingested,
                "skipped": self.skipped}


# ─── helpers ─────────────────────────────────────────────────────────────────


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _source_format(source_path: str) -> str:
    if source_path.endswith(".pdfvec.dxf"):
        return "pdf"
    suffix = Path(source_path).suffix.lower().lstrip(".")
    return suffix or "unknown"


def _taxonomy() -> TaxonomyLoader | None:
    try:
        return TaxonomyLoader(_DEFAULT_TAXONOMY, _DEFAULT_ROLES)
    except FileNotFoundError:
        return None


# ─── per-drawing ingest ──────────────────────────────────────────────────────


def _ingest_one(cur: sqlite3.Cursor, analysis_json: Path,
                taxonomy: TaxonomyLoader | None) -> str:
    stem = analysis_json.name.removesuffix(ANALYSIS_SUFFIX)
    data = _load_json(analysis_json)
    if data is None:
        raise ValueError("unreadable analysis json")

    analysis = data.get("analysis", data)
    classification = data.get("classification", {})
    source_path = str(analysis.get("source_file", ""))

    cur.execute("DELETE FROM drawings WHERE stem = ?", (stem,))
    cur.execute(
        "INSERT INTO drawings (stem, source_path, source_format, drawing_type,"
        " confidence, units, scale_status, ingested_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (stem, source_path, _source_format(source_path),
         classification.get("label", "unknown"),
         float(classification.get("confidence", 0.0) or 0.0),
         analysis.get("likely_unit", "unknown"),
         "unknown",
         datetime.now().isoformat(timespec="seconds")))
    drawing_id = cur.lastrowid

    for name in sorted(analysis.get("layers", {})):
        info = analysis["layers"][name]
        if taxonomy is not None:
            label = classify_layer_name(name, taxonomy=taxonomy)
            sem = (label.semantic_class, label.feature_type, label.export_role)
        else:
            sem = ("unknown", "unknown", "unknown")
        cur.execute(
            "INSERT INTO layers VALUES (?, ?, ?, ?, ?, ?)",
            (drawing_id, name, int(info.get("entity_count", 0) or 0), *sem))

    candidates = _load_json(analysis_json.with_name(f"{stem}.hatch_candidates.json"))
    for cand in (candidates or {}).get("candidates", []):
        region = cand.get("region", {})
        cur.execute(
            "INSERT INTO regions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (drawing_id, region.get("id"), region.get("source_layer"),
             cand.get("class_guess"), cand.get("hatch_class"),
             cand.get("confidence"), cand.get("status"),
             region.get("area"), region.get("perimeter"),
             json.dumps(region.get("bbox"))))

    for entry in analysis.get("text_sample", []):
        cur.execute(
            "INSERT INTO texts VALUES (?, ?, ?, ?, ?)",
            (drawing_id, entry.get("layer"), entry.get("content"),
             entry.get("x"), entry.get("y")))

    routing = _load_json(analysis_json.with_name(f"{stem}.routing.json"))
    if routing:
        for dimension in ("by_feature_type", "by_semantic_class", "by_dest_layer"):
            table = routing.get(dimension, {})
            for key in sorted(table):
                cur.execute("INSERT INTO routing VALUES (?, ?, ?, ?)",
                            (drawing_id, dimension, key, int(table[key] or 0)))
    return stem


# ─── public API ──────────────────────────────────────────────────────────────


def ingest_reports(analysis_jsons: list[str], db_path: str) -> WikiDbReport:
    """Ingest each ``<stem>.analysis.json`` (plus optional siblings) into
    the SQLite fact store at *db_path*.

    Fail-safe per drawing: an unreadable report is skipped with a reason and
    rolls back only its own rows; the rest of the batch still commits.
    """
    db = Path(db_path)
    db.parent.mkdir(parents=True, exist_ok=True)
    report = WikiDbReport(db_path=str(db))
    taxonomy = _taxonomy()

    con = sqlite3.connect(db)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(_SCHEMA)
        for raw in analysis_jsons:
            path = Path(raw)
            cur = con.cursor()
            try:
                cur.execute("SAVEPOINT drawing")
                stem = _ingest_one(cur, path, taxonomy)
                cur.execute("RELEASE SAVEPOINT drawing")
                report.drawings_ingested.append(stem)
            except Exception as exc:
                cur.execute("ROLLBACK TO SAVEPOINT drawing")
                report.skipped[str(path)] = str(exc)
        con.commit()
    finally:
        con.close()
    return report

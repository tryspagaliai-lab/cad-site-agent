"""test_wiki.py — cad-3d P0 M2/M3: SQLite fact store + wiki node rendering."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from cad_site_agent.wiki.sqlite_writer import ingest_reports
from cad_site_agent.wiki.wiki_writer import build_wiki


def _write_reports(reports_dir: Path, stem: str, *, class_guess: str,
                   layer: str = "PDF_C000000_W1") -> Path:
    """Write a minimal but schema-faithful report set for one drawing."""
    reports_dir.mkdir(parents=True, exist_ok=True)
    analysis = {
        "analysis": {
            "source_file": f"/data/{stem}.pdfvec.dxf",
            "likely_unit": "mm",
            "layers": {
                layer:      {"entity_count": 3},
                "PDF_TEXT": {"entity_count": 1},
            },
            "text_sample": [
                {"type": "TEXT", "layer": "PDF_TEXT", "content": "PARKING",
                 "x": 40.0, "y": 160.0},
            ],
        },
        "classification": {"label": "sparse_linework", "confidence": 0.55},
    }
    candidates = {
        "candidates": [{
            "region": {"id": 0, "source_layer": layer, "area": 2400.0,
                       "perimeter": 200.0, "bbox": [120, 20, 180, 60]},
            "class_guess": class_guess,
            "hatch_class": f"MAT_{class_guess.upper()}",
            "confidence": 0.6,
            "status": "review",
        }],
    }
    routing = {
        "by_feature_type":   {"linear": 2, "unknown": 3},
        "by_semantic_class": {class_guess: 2},
        "by_dest_layer":     {"LINEWORK_FENCE": 2},
    }
    (reports_dir / f"{stem}.analysis.json").write_text(
        json.dumps(analysis), encoding="utf-8")
    (reports_dir / f"{stem}.hatch_candidates.json").write_text(
        json.dumps(candidates), encoding="utf-8")
    (reports_dir / f"{stem}.routing.json").write_text(
        json.dumps(routing), encoding="utf-8")
    return reports_dir / f"{stem}.analysis.json"


def _dump_rows(db_path: Path) -> list:
    """All fact rows, with nondeterministic timestamp columns excluded."""
    con = sqlite3.connect(db_path)
    try:
        rows = []
        rows += con.execute(
            "SELECT stem, source_path, source_format, drawing_type, confidence,"
            " units, scale_status FROM drawings ORDER BY stem").fetchall()
        for table, order in (("layers", "name"), ("regions", "region_id"),
                             ("texts", "content"), ("routing", "dimension, key")):
            rows += con.execute(
                f"SELECT * FROM {table} ORDER BY drawing_id, {order}").fetchall()
        return rows
    finally:
        con.close()


# ─── M2: sqlite writer ───────────────────────────────────────────────────────


def test_ingest_populates_all_tables(tmp_path):
    a = _write_reports(tmp_path / "reports", "siteA", class_guess="parking")
    report = ingest_reports([str(a)], str(tmp_path / "wiki.sqlite"))
    assert report.drawings_ingested == ["siteA"]
    assert report.skipped == {}

    con = sqlite3.connect(tmp_path / "wiki.sqlite")
    try:
        assert con.execute("SELECT stem, source_format, drawing_type, units"
                           " FROM drawings").fetchone() == \
            ("siteA", "pdf", "sparse_linework", "mm")
        assert con.execute("SELECT COUNT(*) FROM layers").fetchone()[0] == 2
        assert con.execute("SELECT class_guess, status FROM regions").fetchone() == \
            ("parking", "review")
        assert con.execute("SELECT content FROM texts").fetchone() == ("PARKING",)
        assert con.execute("SELECT COUNT(*) FROM routing").fetchone()[0] == 4
    finally:
        con.close()


def test_ingest_is_deterministic_and_replaces(tmp_path):
    a = _write_reports(tmp_path / "reports", "siteA", class_guess="parking")

    db1, db2 = tmp_path / "one.sqlite", tmp_path / "two.sqlite"
    ingest_reports([str(a)], str(db1))
    ingest_reports([str(a)], str(db2))
    assert _dump_rows(db1) == _dump_rows(db2)

    # Re-ingesting the same stem must replace, not duplicate.
    before = _dump_rows(db1)
    ingest_reports([str(a)], str(db1))
    assert _dump_rows(db1) == before


def test_ingest_failsafe_skips_bad_report(tmp_path):
    reports = tmp_path / "reports"
    good = _write_reports(reports, "siteA", class_guess="parking")
    bad = reports / "broken.analysis.json"
    bad.write_text("{not json", encoding="utf-8")

    report = ingest_reports([str(bad), str(good)], str(tmp_path / "wiki.sqlite"))
    assert report.drawings_ingested == ["siteA"]
    assert str(bad) in report.skipped


# ─── M3: wiki nodes + cross-links ────────────────────────────────────────────


def test_wiki_nodes_and_cross_links(tmp_path):
    reports = tmp_path / "reports"
    a = _write_reports(reports, "siteA", class_guess="parking")
    b = _write_reports(reports, "siteB", class_guess="parking")
    db = tmp_path / "wiki.sqlite"
    ingest_reports([str(a), str(b)], str(db))

    result = build_wiki(str(db), str(tmp_path / "wiki"))
    assert len(result.nodes_written) == 2
    assert result.links_created >= 2

    md_a = (tmp_path / "wiki" / "siteA.md").read_text(encoding="utf-8")
    md_b = (tmp_path / "wiki" / "siteB.md").read_text(encoding="utf-8")
    assert "[siteB](siteB.md)" in md_a and "`parking`" in md_a
    assert "[siteA](siteA.md)" in md_b
    assert "# Drawing: siteA" in md_a
    assert "| `PDF_TEXT` | 1 |" in md_a


def test_wiki_output_is_deterministic(tmp_path):
    reports = tmp_path / "reports"
    a = _write_reports(reports, "siteA", class_guess="parking")
    b = _write_reports(reports, "siteB", class_guess="parking")
    db = tmp_path / "wiki.sqlite"
    ingest_reports([str(a), str(b)], str(db))

    build_wiki(str(db), str(tmp_path / "wiki"))
    first = {p.name: p.read_bytes() for p in (tmp_path / "wiki").glob("*.md")}
    build_wiki(str(db), str(tmp_path / "wiki"))
    second = {p.name: p.read_bytes() for p in (tmp_path / "wiki").glob("*.md")}
    assert first == second


def test_no_link_for_unrelated_drawings(tmp_path):
    reports = tmp_path / "reports"
    a = _write_reports(reports, "siteA", class_guess="parking")
    b = _write_reports(reports, "siteB", class_guess="building")
    db = tmp_path / "wiki.sqlite"
    ingest_reports([str(a), str(b)], str(db))

    build_wiki(str(db), str(tmp_path / "wiki"))
    md_a = (tmp_path / "wiki" / "siteA.md").read_text(encoding="utf-8")
    assert "Related drawings" not in md_a

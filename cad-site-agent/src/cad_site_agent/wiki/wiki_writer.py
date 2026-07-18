"""
wiki_writer.py — cad-3d P0 stage D: SQLite fact store → Markdown wiki nodes.

Pure template rendering from database facts (no LLM). The generated Markdown
contains no timestamps, so identical database facts always produce identical
files. Cross-links between drawings are recomputed on every build from shared
semantic classes.

Public API
----------
    WikiBuildReport
    build_wiki(db_path, wiki_dir) -> WikiBuildReport
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

#: Semantic classes that say nothing about drawing content.
_NON_LINKING_CLASSES = {"", "unknown", "none", None}


@dataclass
class WikiBuildReport:
    db_path: str
    wiki_dir: str
    nodes_written: list[str] = field(default_factory=list)
    links_created: int = 0

    def to_dict(self) -> dict:
        return {"db_path": self.db_path, "wiki_dir": self.wiki_dir,
                "nodes_written": self.nodes_written,
                "links_created": self.links_created}


# ─── link computation ────────────────────────────────────────────────────────


def _drawing_classes(con: sqlite3.Connection, drawing_id: int) -> set[str]:
    rows = con.execute(
        "SELECT semantic_class FROM layers WHERE drawing_id = ?"
        " UNION SELECT class_guess FROM regions WHERE drawing_id = ?",
        (drawing_id, drawing_id)).fetchall()
    return {r[0] for r in rows} - _NON_LINKING_CLASSES


def _rebuild_links(con: sqlite3.Connection, drawings: list[tuple[int, str]]) -> int:
    con.execute("DELETE FROM wiki_links")
    classes = {did: _drawing_classes(con, did) for did, _ in drawings}
    created = 0
    for i, (id_a, _) in enumerate(drawings):
        for id_b, _ in drawings[i + 1:]:
            for cls in sorted(classes[id_a] & classes[id_b]):
                con.execute("INSERT INTO wiki_links VALUES (?, ?, ?)", (id_a, id_b, cls))
                con.execute("INSERT INTO wiki_links VALUES (?, ?, ?)", (id_b, id_a, cls))
                created += 2
    return created


# ─── markdown rendering ──────────────────────────────────────────────────────


def _render_node(con: sqlite3.Connection, drawing_id: int, stem: str) -> str:
    d = con.execute(
        "SELECT source_path, source_format, drawing_type, confidence, units,"
        " scale_status, text_count FROM drawings WHERE id = ?",
        (drawing_id,)).fetchone()
    source_path, source_format, dtype, confidence, units, scale_status, text_count = d

    lines = [
        f"# Drawing: {stem}",
        "",
        f"- **Source:** `{source_path}` ({source_format})",
        f"- **Type:** {dtype} (confidence {confidence:.2f})",
        f"- **Units:** {units} | scale: {scale_status}",
        "",
    ]

    layers = con.execute(
        "SELECT name, entity_count, semantic_class, feature_type FROM layers"
        " WHERE drawing_id = ? ORDER BY name", (drawing_id,)).fetchall()
    if layers:
        lines += ["## Layers", "",
                  "| Layer | Entities | Semantic class | Feature type |",
                  "|-------|----------|----------------|--------------|"]
        lines += [f"| `{n}` | {c} | {sc} | {ft} |" for n, c, sc, ft in layers]
        lines.append("")

    regions = con.execute(
        "SELECT status, class_guess, COUNT(*), SUM(area) FROM regions"
        " WHERE drawing_id = ? GROUP BY status, class_guess"
        " ORDER BY status, class_guess", (drawing_id,)).fetchall()
    if regions:
        lines += ["## Regions", "",
                  "| Status | Class | Count | Total area |",
                  "|--------|-------|-------|------------|"]
        lines += [f"| {st} | {cg} | {n} | {area or 0:.1f} |"
                  for st, cg, n, area in regions]
        lines.append("")

    routing = con.execute(
        "SELECT dimension, key, count FROM routing WHERE drawing_id = ?"
        " ORDER BY dimension, key", (drawing_id,)).fetchall()
    if routing:
        lines += ["## Routing", ""]
        lines += [f"- {dim}/{key}: {n}" for dim, key, n in routing]
        lines.append("")

    n_samples = con.execute("SELECT COUNT(*) FROM texts WHERE drawing_id = ?",
                            (drawing_id,)).fetchone()[0]
    # text_count is the analyzer's true total; the texts table holds only its
    # capped sample (20 entries / 80 chars).
    total_texts = text_count if text_count else n_samples
    if total_texts:
        lines += [f"**Text entries:** {total_texts} (sample stored: {n_samples})", ""]

    links = con.execute(
        "SELECT d.stem, l.shared_class FROM wiki_links l"
        " JOIN drawings d ON d.id = l.to_drawing_id"
        " WHERE l.from_drawing_id = ? ORDER BY d.stem, l.shared_class",
        (drawing_id,)).fetchall()
    if links:
        lines += ["## Related drawings", ""]
        lines += [f"- [{other}]({quote(other)}.md) — shared class `{cls}`"
                  for other, cls in links]
        lines.append("")

    return "\n".join(lines)


# ─── public API ──────────────────────────────────────────────────────────────


def build_wiki(db_path: str, wiki_dir: str) -> WikiBuildReport:
    """Render one Markdown node per drawing in the fact store and refresh
    cross-links. Node paths are recorded in ``wiki_nodes``."""
    out_dir = Path(wiki_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = WikiBuildReport(db_path=str(db_path), wiki_dir=str(out_dir))

    con = sqlite3.connect(db_path)
    try:
        drawings = con.execute(
            "SELECT id, stem FROM drawings ORDER BY stem").fetchall()
        report.links_created = _rebuild_links(con, drawings)

        con.execute("DELETE FROM wiki_nodes")
        for drawing_id, stem in drawings:
            node_path = out_dir / f"{stem}.md"
            node_path.write_text(_render_node(con, drawing_id, stem),
                                 encoding="utf-8")
            con.execute("INSERT INTO wiki_nodes VALUES (?, ?, ?)",
                        (drawing_id, str(node_path),
                         datetime.now().isoformat(timespec="seconds")))
            report.nodes_written.append(str(node_path))
        con.commit()
    finally:
        con.close()
    return report

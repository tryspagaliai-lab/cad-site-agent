"""
CAD Site Agent — MCP Server (Repo Bridge A)

Exposes the cad-site-agent pipeline as MCP tools so Claude.ai chat can:
  - list DXF files and reports in the workspace
  - read report contents
  - run analyze, classify, hatch-candidates, and full process commands

Usage (stdio transport, for Claude Desktop / claude.ai MCP):
    python mcp_server.py

claude_desktop_config.json entry:
{
  "mcpServers": {
    "cad-site-agent": {
      "command": "python",
      "args": ["/path/to/cad-site-agent/mcp_server.py"],
      "env": {"PYTHONPATH": "/path/to/cad-site-agent/src"}
    }
  }
}
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── workspace root ─────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.resolve()
SRC_DIR   = REPO_ROOT / "src"

# Ensure src/ is on the path so cad_site_agent imports work
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

mcp = FastMCP("cad-site-agent")


# ── helpers ────────────────────────────────────────────────────────────────────

def _run_cli(*args: str, cwd: Path | None = None) -> str:
    """Run cad-agent CLI and return combined stdout+stderr."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_DIR)
    result = subprocess.run(
        [sys.executable, "-m", "cad_site_agent.cli", *args],
        capture_output=True,
        text=True,
        cwd=str(cwd or REPO_ROOT),
        env=env,
    )
    output = result.stdout
    if result.stderr:
        output += "\n[stderr]\n" + result.stderr
    return output.strip()


def _abs(path: str) -> Path:
    """Resolve a path relative to REPO_ROOT if not absolute."""
    p = Path(path)
    if not p.is_absolute():
        p = REPO_ROOT / p
    return p


# ── tools ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_dxf_files(directory: str = "") -> str:
    """List all DXF files in the workspace (or a sub-directory).

    Args:
        directory: Sub-directory to search (relative to repo root, or absolute).
                   Leave empty to search the whole workspace.
    """
    root = _abs(directory) if directory else REPO_ROOT
    files = sorted(root.rglob("*.dxf"))
    if not files:
        return f"No DXF files found under {root}"
    lines = [f"DXF files under {root}:", ""]
    for f in files:
        try:
            rel = f.relative_to(REPO_ROOT)
        except ValueError:
            rel = f
        size_kb = f.stat().st_size // 1024
        lines.append(f"  {rel}  ({size_kb} KB)")
    return "\n".join(lines)


@mcp.tool()
def list_reports(report_type: str = "all") -> str:
    """List generated analysis reports.

    Args:
        report_type: "json", "md", "all" (default "all").
    """
    report_dir = REPO_ROOT / "reports" / "analysis"
    if not report_dir.exists():
        return f"Report directory not found: {report_dir}"

    patterns: list[str] = []
    if report_type in ("json", "all"):
        patterns.append("*.json")
    if report_type in ("md", "all"):
        patterns.append("*.md")

    files: list[Path] = []
    for pat in patterns:
        files.extend(report_dir.glob(pat))
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    if not files:
        return f"No {report_type} reports found in {report_dir}"

    lines = [f"Reports in {report_dir}:", ""]
    for f in files:
        mtime = f.stat().st_mtime
        size_kb = f.stat().st_size // 1024
        lines.append(f"  {f.name}  ({size_kb} KB)")
    return "\n".join(lines)


@mcp.tool()
def read_report(report_name: str) -> str:
    """Read the content of a named report file.

    Args:
        report_name: File name (e.g. "roman_gardens_analysis.md") or a path
                     relative to the repo root.
    """
    # Try reports/analysis/ first, then repo root, then absolute
    candidates = [
        REPO_ROOT / "reports" / "analysis" / report_name,
        REPO_ROOT / report_name,
        Path(report_name),
    ]
    for p in candidates:
        if p.exists():
            content = p.read_text(encoding="utf-8", errors="replace")
            # Cap at 50 000 chars to keep tool output manageable
            if len(content) > 50_000:
                content = content[:50_000] + "\n\n[... truncated at 50 000 chars ...]"
            return content
    return f"Report not found: {report_name}\nSearched: {[str(c) for c in candidates]}"


@mcp.tool()
def analyze_dxf(dxf_path: str, output_dir: str = "", preview: bool = False) -> str:
    """Analyze a DXF file and produce JSON + Markdown reports.

    Args:
        dxf_path:   Path to the DXF file (relative to repo root or absolute).
        output_dir: Where to write reports (default: reports/analysis/).
        preview:    Also render a PNG preview (slow).
    """
    abs_dxf = _abs(dxf_path)
    if not abs_dxf.exists():
        return f"File not found: {abs_dxf}"

    args = ["analyze-dxf", str(abs_dxf)]
    if output_dir:
        args += ["--output", str(_abs(output_dir))]
    if preview:
        args.append("--preview")

    return _run_cli(*args)


@mcp.tool()
def classify_drawing(dxf_path: str) -> str:
    """Classify the drawing type of a DXF file (5 types: site layout, floor plan, …).

    Args:
        dxf_path: Path to the DXF file.
    """
    abs_dxf = _abs(dxf_path)
    if not abs_dxf.exists():
        return f"File not found: {abs_dxf}"
    return _run_cli("classify-drawing", str(abs_dxf))


@mcp.tool()
def hatch_candidates(
    dxf_path: str,
    output_dir: str = "",
    min_area: float | None = None,
    class_filter: str = "",
) -> str:
    """Extract closed-region hatch candidates from a DXF file.

    Args:
        dxf_path:     Path to the DXF file.
        output_dir:   Output directory for reports.
        min_area:     Minimum region area in mm² (optional override).
        class_filter: Only output candidates for this site class.
    """
    abs_dxf = _abs(dxf_path)
    if not abs_dxf.exists():
        return f"File not found: {abs_dxf}"

    args = ["hatch-candidates", str(abs_dxf)]
    if output_dir:
        args += ["--output", str(_abs(output_dir))]
    if min_area is not None:
        args += ["--min-area", str(min_area)]
    if class_filter:
        args += ["--class-filter", class_filter]

    return _run_cli(*args)


@mcp.tool()
def process_dxf(
    source_dxf: str,
    output_dxf: str,
    status: str = "auto",
    min_confidence: float | None = None,
    keep_noise: bool = False,
) -> str:
    """Run the full end-to-end CAD pipeline on a DXF file.

    Produces:
      <output>.dxf                 — routed linework, markings, symbols, text
      <output>.hatches.dxf         — HATCH entities for closed regions
      <output>.hatch_candidates.json — candidate metadata
      <output>.process.json        — pipeline run summary

    Args:
        source_dxf:     Input DXF path.
        output_dxf:     Output DXF path.
        status:         Candidate filter — "auto" or "review" (default "auto").
        min_confidence: Minimum hatch-candidate confidence 0–1 (optional).
        keep_noise:     Include noise entities such as title blocks (default off).
    """
    abs_src = _abs(source_dxf)
    if not abs_src.exists():
        return f"Source file not found: {abs_src}"

    abs_out = _abs(output_dxf)
    abs_out.parent.mkdir(parents=True, exist_ok=True)

    args = ["process", str(abs_src), str(abs_out), "--status", status]
    if min_confidence is not None:
        args += ["--min-confidence", str(min_confidence)]
    if keep_noise:
        args.append("--keep-noise")

    return _run_cli(*args)


@mcp.tool()
def repo_status() -> str:
    """Return repository info: git log, branch, recent reports, and available DXF files."""
    lines: list[str] = []

    # git info
    for cmd, label in [
        (["git", "rev-parse", "--abbrev-ref", "HEAD"], "Branch"),
        (["git", "log", "--oneline", "-5"], "Recent commits"),
    ]:
        try:
            out = subprocess.check_output(cmd, cwd=str(REPO_ROOT), text=True).strip()
            lines.append(f"### {label}\n{out}\n")
        except Exception as exc:
            lines.append(f"### {label}\n(error: {exc})\n")

    # DXF files
    dxf_files = sorted(REPO_ROOT.rglob("*.dxf"))
    if dxf_files:
        lines.append("### DXF files")
        for f in dxf_files:
            try:
                rel = f.relative_to(REPO_ROOT)
            except ValueError:
                rel = f
            lines.append(f"  {rel}  ({f.stat().st_size // 1024} KB)")
        lines.append("")

    # Latest reports
    report_dir = REPO_ROOT / "reports" / "analysis"
    if report_dir.exists():
        reports = sorted(report_dir.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]
        lines.append("### Latest reports (reports/analysis/)")
        for r in reports:
            lines.append(f"  {r.name}")
        lines.append("")

    return "\n".join(lines) if lines else "No info available."


# ── entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")

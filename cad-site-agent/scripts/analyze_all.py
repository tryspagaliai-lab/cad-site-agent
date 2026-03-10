"""
Quick script: run analysis on all known DXF files and write reports.
Run from E:\cad-site-agent\ as:
  python scripts/analyze_all.py
"""
import sys
sys.path.insert(0, "src")

from pathlib import Path
from cad_site_agent.analyzer.dxf_analyzer import analyze_dxf
from cad_site_agent.analyzer.drawing_classifier import classify_drawing
from cad_site_agent.analyzer.report_writer import write_json_report, write_markdown_report

DXF_FILES = [
    r"E:\SHAKESPEARE\RAW_DATA\BDW Eastern Counties - DWH & BH Roman Gardens2.dxf",
    r"E:\SHAKESPEARE\RAW_DATA\ST-23-01S Planning Layout.dxf",
    r"E:\SHAKESPEARE\RAW_DATA\parking_rotated.dxf",
    r"E:\SHAKESPEARE\RAW_DATA\parking_hatched.dxf",
]

OUT_DIR = Path("reports/analysis")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for dxf in DXF_FILES:
    p = Path(dxf)
    if not p.exists():
        print(f"SKIP (not found): {p.name}")
        continue
    print(f"\nAnalysing: {p.name}")
    report = analyze_dxf(p)
    cls = classify_drawing(report)
    stem = p.stem.replace(" ", "_")
    write_json_report(report, cls, OUT_DIR / f"{stem}_analysis.json")
    write_markdown_report(report, cls, OUT_DIR / f"{stem}_analysis.md")
    print(f"  {cls.drawing_type} ({cls.confidence:.0%}) | "
          f"{report.total_entities:,} ents | {report.total_layers} layers | {report.likely_unit}")
    print(f"  closed={report.closed_polyline_count} open={report.open_polyline_count} hatches={report.has_hatches}")
    print(f"  -> {OUT_DIR / stem}_analysis.[json|md]")

print("\nDone.")

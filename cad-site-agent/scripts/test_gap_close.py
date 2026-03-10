"""
Test gap_closer on Roman Gardens DXF.
Run from E:\\cad-site-agent\\ as:
  python scripts/test_gap_close.py
"""
import sys, json
sys.path.insert(0, "src")

from pathlib import Path
from cad_site_agent.cleanup.gap_closer import run_gap_close

DXF = r"E:\SHAKESPEARE\RAW_DATA\BDW Eastern Counties - DWH & BH Roman Gardens2.dxf"
OUT = r"E:\SHAKESPEARE\RAW_DATA\roman_gardens_gapclosed.dxf"

print("Running gap closer on Roman Gardens...")
print(f"  tolerance = 1000 units (1 m in mm DXF)")
print(f"  bridge_mode = True")
print()

result = run_gap_close(
    dxf_path=DXF,
    output_path=OUT,
    tolerance=1000.0,       # 1 m gap tolerance
    bridge_mode=True,
    same_layer_only=False,
    max_bridge_len=1000.0,
)

print(json.dumps(result.to_dict(), indent=2))
print()
print(f"open  before: {result.open_before:,}  ->  after: {result.open_after:,}")
print(f"closed before: {result.closed_before:,}  ->  after: {result.closed_after:,}")
print(f"self-closed: {result.self_closed}  |  merged pairs: {result.merged_pairs}  |  bridges: {result.bridges_added}")
if result.errors:
    print(f"ERRORS ({len(result.errors)}):")
    for e in result.errors[:20]:
        print(f"  {e}")
print()
print(f"Output: {result.output_path}")

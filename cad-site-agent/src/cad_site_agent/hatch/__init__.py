"""
Hatch candidate pipeline — Phase 4B.

Modules:
  closed_regions  — extract closed LWPOLYLINE / POLYLINE regions from a DXF
  semantic_hatch  — classify each region → site class + material code
  confidence      — score each candidate → auto / review / skip status
"""

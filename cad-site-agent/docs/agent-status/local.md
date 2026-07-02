# Agent status: local (Claude Code LAPTOPE — vienintelė fizinė mašina)

- updated: 2026-07-02T00:30:00Z
- branch: main
- head: (pildyti)
- status: TODO — kai Claude Code bus paleistas laptope: (1) įdiek ODA File
  Converter (žr. docs/ODA_SETUP.md), (2) parsink `C:\Users\zilva\Desktop\H7149
  Osprey Heights` (inventorius: DWG/DXF/PDF), (3) konvertuok DWG→DXF per
  `python scripts/dwg_to_dxf.py "<kelias>" --out ./data/h7149_dxf --recursive`,
  (4) paleisk pipeline (analyze-dxf → classify → clean → close-gaps →
  normalize-layers → hatch → process), (5) surašyk rezultatus čia per
  `./.claude/hooks/agent-status.sh local "..."`.

> Pastaba: ankstesnė rolė vadinosi `desktop` — pervadinta, nes atskiro desktop
> kompiuterio NĖRA. Yra tik laptopas (ir galbūt VPS ateityje).

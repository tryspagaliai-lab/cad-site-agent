#!/usr/bin/env python3
"""
dwg_to_dxf.py — Batch DWG -> DXF konverteris (naudoja ODA File Converter per ezdxf).

SVARBU: reikia įdiegto ODA File Converter (nemokamas):
  https://www.opendesign.com/guestfiles/oda_file_converter
  - Windows: numatytas kelias randamas automatiškai.
  - Linux:   įdiek .deb/AppImage; ezdxf ras per PATH arba nurodyk ODAFC_EXEC.
  - macOS:   ODAFileConverter.app.

Pastaba dėl aplinkos: NUOTOLINĖJE (cloud/web) Claude Code sesijoje ODA įdiegti
negalima (tinklas apribotas, konteineris efemeris). Šį skriptą leisk LAPTOPE
(vienintelė fizinė mašina; ateityje galbūt VPS), kur yra ir failai, ir ODA.

Naudojimas:
  python scripts/dwg_to_dxf.py <input_dir_ar_failas> [--out DIR] [--version ACAD2018] [--recursive]

Grąžina JSON santrauką į stdout (patogu tandemui / logams).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def find_dwgs(src: Path, recursive: bool) -> list[Path]:
    if src.is_file():
        return [src] if src.suffix.lower() == ".dwg" else []
    pattern = "**/*.dwg" if recursive else "*.dwg"
    return sorted(p for p in src.glob(pattern) if p.is_file())


def main() -> int:
    ap = argparse.ArgumentParser(description="Batch DWG -> DXF via ODA File Converter")
    ap.add_argument("input", help="DWG failas arba katalogas")
    ap.add_argument("--out", default=None, help="Output katalogas (default: šalia šaltinio)")
    ap.add_argument("--version", default="ACAD2018", help="DXF versija (default ACAD2018)")
    ap.add_argument("--recursive", action="store_true", help="Ieškoti DWG rekursyviai")
    args = ap.parse_args()

    try:
        from ezdxf.addons import odafc
    except ImportError:
        print(json.dumps({"ok": False, "error": "ezdxf neįdiegtas: pip install -e .[dev]"}))
        return 2

    if not odafc.is_installed():
        print(json.dumps({
            "ok": False,
            "error": "ODA File Converter NĖRA įdiegtas.",
            "fix": "Įdiek iš https://www.opendesign.com/guestfiles/oda_file_converter "
                   "ir leisk šį skriptą LAPTOPE (ne nuotolinėje cloud sesijoje).",
            "platform_hint": {
                "windows": "ODAFileConverter.exe numatytoje vietoje randamas auto",
                "linux": "įdiek .deb/AppImage; nurodyk kelią per ODAFC_EXEC jei reikia",
            },
        }))
        return 3

    src = Path(args.input).expanduser()
    if not src.exists():
        print(json.dumps({"ok": False, "error": f"Nerastas: {src}"}))
        return 4

    dwgs = find_dwgs(src, args.recursive)
    if not dwgs:
        print(json.dumps({"ok": False, "error": f"Jokių .dwg failų: {src}"}))
        return 5

    out_dir = Path(args.out).expanduser() if args.out else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    converted, failed = [], []
    for dwg in dwgs:
        dxf = (out_dir or dwg.parent) / (dwg.stem + ".dxf")
        try:
            odafc.convert(str(dwg), str(dxf), version=args.version, replace=True)
            converted.append({"src": str(dwg), "dxf": str(dxf)})
        except Exception as e:  # odafc gali mesti įvairias klaidas
            failed.append({"src": str(dwg), "error": f"{type(e).__name__}: {e}"})

    print(json.dumps({
        "ok": not failed,
        "oda_exec": odafc.get_unix_exec_path() or odafc.get_win_exec_path(),
        "found": len(dwgs),
        "converted": len(converted),
        "failed": len(failed),
        "outputs": converted,
        "errors": failed,
    }, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
run_pipeline_batch.py — VIENOS KOMANDOS automatizacija visam katalogui.

Kiekvienam rastam brėžiniui automatiškai:
  0. (jei .dwg ir įdiegtas ODA) DWG -> DXF konversija
  1. run_cleanup        — dublikatai, trumpi segmentai, endpoint snap
  2. run_gap_close      — atvirų polilinijų uždarymas
  3. run_normalization  — sluoksnių vardų normalizacija (layer_aliases.yaml)
  4. run_process        — pilnas pipeline: hatch kandidatai -> hatch DXF -> routing

Klaidos izoliuojamos per failą (vienas blogas brėžinys nesustabdo batch'o);
kiekvieno failo rezultatas/klaida rašoma į JSON metadata log (pagal CAD
cleanup taisykles). Gale — bendra JSON santrauka (stdout + reports/batch/).

Naudojimas (laptope):
  python scripts/run_pipeline_batch.py "C:/Users/zilva/Desktop/H7149 Osprey Heights" \
      --out data/h7149 --recursive
  # arba tiesiog: run_h7149.bat

Santrauka automatiškai tinka tandemo (Kimi/MiMo) patikrai — žr.
scripts/tandem_report.py, kuris ją supakuoja į vieną perduodamą paketą.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("batch")


def find_drawings(src: Path, recursive: bool) -> tuple[list[Path], list[Path]]:
    """Grąžina (dxf_files, dwg_files)."""
    if src.is_file():
        s = src.suffix.lower()
        return ([src] if s == ".dxf" else [], [src] if s == ".dwg" else [])
    pat = "**/*" if recursive else "*"
    dxfs = sorted(p for p in src.glob(pat + ".dxf") if p.is_file())
    dwgs = sorted(p for p in src.glob(pat + ".dwg") if p.is_file())
    return dxfs, dwgs


def convert_dwgs(dwgs: list[Path], out_dir: Path) -> tuple[list[Path], list[dict]]:
    """DWG -> DXF per ODA (jei įdiegtas). Grąžina (nauji_dxf, klaidos)."""
    if not dwgs:
        return [], []
    try:
        from ezdxf.addons import odafc
    except ImportError:
        return [], [{"stage": "convert", "error": "ezdxf neįdiegtas"}]
    if not odafc.is_installed():
        return [], [{
            "stage": "convert",
            "error": f"ODA File Converter neįdiegtas — {len(dwgs)} DWG praleisti. "
                     "Žr. docs/ODA_SETUP.md",
            "skipped": [str(p) for p in dwgs],
        }]
    converted, errors = [], []
    conv_dir = out_dir / "converted_dxf"
    conv_dir.mkdir(parents=True, exist_ok=True)
    for dwg in dwgs:
        dxf = conv_dir / (dwg.stem + ".dxf")
        try:
            odafc.convert(str(dwg), str(dxf), version="ACAD2018", replace=True)
            converted.append(dxf)
            log.info("converted %s -> %s", dwg.name, dxf.name)
        except Exception as e:
            errors.append({"stage": "convert", "file": str(dwg),
                           "error": f"{type(e).__name__}: {e}"})
    return converted, errors


def process_one(dxf: Path, out_dir: Path, min_confidence: float | None,
                aliases_cfg: Path) -> dict:
    """Pilna grandinė vienam DXF. Grąžina rezultato dict (ok arba error)."""
    from cad_site_agent.cleanup.cleaner import run_cleanup
    from cad_site_agent.cleanup.gap_closer import run_gap_close
    from cad_site_agent.semantic.normalizer import run_normalization
    from cad_site_agent.pipeline import run_process

    stem = dxf.stem
    work = out_dir / stem
    work.mkdir(parents=True, exist_ok=True)
    result: dict = {"source": str(dxf), "stages": {}}

    cleaned = work / f"{stem}_cleaned.dxf"
    gapped = work / f"{stem}_gapclosed.dxf"
    normal = work / f"{stem}_normalised.dxf"
    final = work / f"{stem}_processed.dxf"

    log.info("[%s] 1/4 cleanup", stem)
    result["stages"]["cleanup"] = run_cleanup(dxf, cleaned)

    log.info("[%s] 2/4 gap close", stem)
    gap = run_gap_close(cleaned, gapped)
    result["stages"]["gap_close"] = getattr(gap, "__dict__", None) or str(gap)

    log.info("[%s] 3/4 normalize layers", stem)
    result["stages"]["normalize"] = run_normalization(
        gapped, config_path=aliases_cfg, output_path=normal)

    log.info("[%s] 4/4 process (hatch + routing)", stem)
    if final.exists():
        final.unlink()  # run_process atsisako perrašyti — batch'e perrašymas OK
    report = run_process(str(normal), str(final), min_confidence=min_confidence)
    result["stages"]["process"] = report.to_dict()
    result["output_dxf"] = str(final)
    result["ok"] = True
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Batch: DWG/DXF -> cleanup -> pipeline")
    ap.add_argument("input", help="Katalogas arba vienas DWG/DXF failas")
    ap.add_argument("--out", default="data/batch_out", help="Output katalogas")
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--min-confidence", type=float, default=None)
    ap.add_argument("--aliases", default=None,
                    help="layer_aliases.yaml kelias (default: config/ šalia paketo)")
    args = ap.parse_args()

    src = Path(args.input).expanduser()
    if not src.exists():
        print(json.dumps({"ok": False, "error": f"Nerastas: {src}"}))
        return 2

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    aliases_cfg = Path(args.aliases) if args.aliases else (
        Path(__file__).resolve().parents[1] / "config" / "layer_aliases.yaml")

    dxfs, dwgs = find_drawings(src, args.recursive)
    converted, conv_errors = convert_dwgs(dwgs, out_dir)
    todo = dxfs + converted

    summary: dict = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input": str(src),
        "found": {"dxf": len(dxfs), "dwg": len(dwgs), "converted": len(converted)},
        "convert_errors": conv_errors,
        "results": [],
        "errors": [],
    }

    for dxf in todo:
        try:
            summary["results"].append(process_one(dxf, out_dir, args.min_confidence,
                                                  aliases_cfg))
        except Exception as e:
            log.error("[%s] FAILED: %s", dxf.stem, e)
            summary["errors"].append({
                "source": str(dxf),
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(limit=3),
            })

    summary["ok"] = not summary["errors"] and not conv_errors
    summary["processed"] = len(summary["results"])
    summary["failed"] = len(summary["errors"])

    # JSON metadata log — nuolatinė vieta tandemo patikrai
    report_path = out_dir / "batch_report.json"
    report_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                           encoding="utf-8")
    log.info("batch report -> %s", report_path)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

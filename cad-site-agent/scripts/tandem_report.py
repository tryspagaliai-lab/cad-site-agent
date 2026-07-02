#!/usr/bin/env python3
"""
tandem_report.py — Kimi/MiMo tandemo paketo generatorius.

Surenka VISĄ aktualią būseną į vieną savarankišką markdown failą, kurį
tiesiog nukopijuoji į Kimi arba MiMo pokalbį kryžminei patikrai:
  - git būsena (šaka, HEAD, paskutiniai commit'ai)
  - visų agentų statusai (docs/agent-status/*.md)
  - atviri TODO iš SESSION_HANDOFF.md
  - paskutinė batch ataskaita (jei nurodyta per --batch)
  - AIŠKI užduotis tikrintojui + laukiamo verdikto formatas

Verdiktą iš Kimi/MiMo įrašai atgal į lentą viena komanda:
  ./.claude/hooks/agent-status.sh kimi "VERDICT: ..."
  ./.claude/hooks/agent-status.sh mimo "VERDICT: ..."

Naudojimas:
  python scripts/tandem_report.py [--batch data/h7149/batch_report.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # cad-site-agent/
REPO = ROOT.parent                                   # git šaknis


def sh(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception as e:
        return f"(nepavyko: {e})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default=None, help="batch_report.json kelias")
    ap.add_argument("--out", default=None, help="Output failas (default: reports/tandem/)")
    args = ap.parse_args()

    now = datetime.now().isoformat(timespec="seconds")
    parts: list[str] = [
        "# TANDEMO PAKETAS — kryžminė patikra (Kimi / MiMo)",
        f"\nSugeneruota: {now}",
        f"Repo: tryspagaliai-lab/cad-site-agent | šaka: {sh(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])} | HEAD: {sh(['git', 'rev-parse', '--short', 'HEAD'])}",
        "\n## UŽDUOTIS TIKRINTOJUI",
        (
            "Tu esi nepriklausomas tikrintojas CAD Site Agent projekte (DXF valymo\n"
            "pipeline: cleanup -> gap close -> layer normalize -> hatch -> routing).\n"
            "Peržiūrėk žemiau pateiktą būseną ir batch rezultatus. Atsakyk TIKSLIAI\n"
            "šiuo formatu:\n\n"
            "```\n"
            "VERDICT: PASS | FAIL | CONCERNS\n"
            "FINDINGS:\n"
            "- <radinys 1: kas negerai/įtartina + kuriame faile/etape>\n"
            "- <radinys 2>\n"
            "RECOMMENDATIONS:\n"
            "- <konkretus veiksmas>\n"
            "```\n\n"
            "Tikrink: (1) ar visų failų 4 etapai įvyko be klaidų; (2) ar hatch\n"
            "kandidatų auto/review santykis protingas; (3) ar features_removed\n"
            "(noise) skaičiai nėra įtartinai dideli; (4) ar sluoksnių normalizacija\n"
            "nepametė svarbių sluoksnių; (5) loginius prieštaravimus ataskaitose."
        ),
        "\n## Paskutiniai commit'ai\n```",
        sh(["git", "log", "--oneline", "-10"]),
        "```",
    ]

    status_dir = ROOT / "docs" / "agent-status"
    if status_dir.is_dir():
        parts.append("\n## Agentų statusai")
        for f in sorted(status_dir.glob("*.md")):
            parts.append(f"\n### {f.stem}\n" + f.read_text(encoding="utf-8").strip())

    handoff = ROOT / "docs" / "SESSION_HANDOFF.md"
    if handoff.exists():
        parts.append("\n## Session handoff (pilnas)\n" +
                     handoff.read_text(encoding="utf-8").strip())

    if args.batch:
        bp = Path(args.batch)
        if bp.exists():
            data = json.loads(bp.read_text(encoding="utf-8"))
            parts.append("\n## Batch ataskaita (pipeline rezultatai)\n```json\n" +
                         json.dumps(data, indent=2, ensure_ascii=False) + "\n```")
        else:
            parts.append(f"\n## Batch ataskaita\n(nerasta: {bp} — batch dar nebuvo leistas)")

    parts.append(
        "\n## KAIP GRĄŽINTI VERDIKTĄ\n"
        "Verdiktą įrašyk į koordinacijos lentą (laptope, repo kataloge):\n"
        "```bash\n"
        "./.claude/hooks/agent-status.sh kimi \"VERDICT: PASS — ...\"\n"
        "./.claude/hooks/agent-status.sh mimo \"VERDICT: CONCERNS — ...\"\n"
        "```\n"
        "Tada kiekviena Claude sesija verdiktus pamatys automatiškai per SessionStart."
    )

    out_dir = Path(args.out).parent if args.out else ROOT / "reports" / "tandem"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else out_dir / f"tandem_package_{now.replace(':', '-')}.md"
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "package": str(out),
                      "chars": out.stat().st_size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    main()

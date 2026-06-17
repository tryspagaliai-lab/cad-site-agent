#!/usr/bin/env python3
"""PreToolUse guard: saugo stabilius sluoksnius nuo netyčinio delete/merge/purge.

Logika (fail-open — niekada nelaužia normalaus darbo):
  stdin : PreToolUse JSON payload (tool_name + tool_input).
  exit 0: leisti (default; jokio destruktyvaus ketinimo, arba taikinys neaiškus).
  exit 2: blokuoti (komanda bando delete/merge/purge STABILŲ sluoksnį iš schemos).

Schema: config/layers.json -> "stable_layers" (generuota iš export_layers.yaml +
semantic_taxonomy.yaml). Kelias keičiamas per CAD_LAYER_SCHEMA env var.

PASTABA dėl semantikos: gardas SAUGO stabilius sluoksnius — t.y. blokuoja jų
naikinimą/jungimą (o ne atvirkščiai). Jei schema nerasta ar sluoksnio neištraukia,
gardas LEIDŽIA (fail-open), kad netrukdytų darbui.
"""
import json, sys, os, re

# Kelias reliatyvus repo šakniai (cwd desktop'e = repo šaknis); turinys po cad-site-agent/
SCHEMA = os.environ.get('CAD_LAYER_SCHEMA', 'cad-site-agent/config/layers.json')

DESTRUCTIVE = ('delete_layer', 'merge_layer', 'purge', 'del_layer', 'remove_layer')


def stable_layers():
    """Grąžina stabilių sluoksnių aibę (lowercase) arba tuščią, jei schema nepasiekiama."""
    try:
        with open(SCHEMA, encoding='utf-8') as f:
            data = json.load(f)
        return {str(x).lower() for x in data.get('stable_layers', [])}
    except (OSError, ValueError):
        return set()  # fail-open: nėra schemos -> neblokuojam


def extract_text(payload):
    """Surenka komandos/argumentų tekstą iš PreToolUse payload (tolerantiška formatui)."""
    ti = payload.get('tool_input', payload)
    if isinstance(ti, dict):
        parts = [str(v) for v in ti.values() if isinstance(v, (str, int, float))]
        return ' '.join(parts) if parts else json.dumps(payload)
    return json.dumps(payload)


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)  # nėra ko tikrinti

    text = extract_text(payload)
    low = text.lower()

    # 1) Ar yra destruktyvus sluoksnio ketinimas?
    if not any(k in low for k in DESTRUCTIVE):
        sys.exit(0)

    # 2) Kurie stabilūs sluoksniai paminėti taikinyje?
    allowed = stable_layers()
    if not allowed:
        sys.exit(0)  # fail-open: be schemos nesprendžiam

    hits = sorted({lyr for lyr in allowed if re.search(r'(?<![\w-])' + re.escape(lyr) + r'(?![\w-])', low)})
    if hits:
        print(
            "BLOCKED: komanda bando delete/merge/purge stabilų(-ius) sluoksnį(-ius): "
            + ", ".join(hits)
            + ". Šie sluoksniai yra schemoje (config/layers.json) ir saugomi. "
            "Jei tikrai reikia — paleisk rankiniu būdu be šio gardo.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()

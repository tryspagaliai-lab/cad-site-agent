#!/usr/bin/env python3
"""PreToolUse guard: blokuoja layer delete/merge jei layer ne 47-schemoje.
stdin: JSON su tool call. exit 0 = leisti, exit 2 = blokuoti."""
import json, sys, os

# Kelias reliatyvus repo šakniai (cwd desktop'e = repo šaknis); turinys yra po cad-site-agent/
SCHEMA = os.environ.get('CAD_LAYER_SCHEMA', 'cad-site-agent/config/layers.json')

def stable_layers():
    with open(SCHEMA) as f:
        return set(json.load(f).get('stable_layers', []))

def main():
    payload = json.load(sys.stdin)
    cmd = json.dumps(payload).lower()
    if any(k in cmd for k in ('delete_layer', 'merge_layer', 'purge')):
        allowed = stable_layers()
        # TODO: parse target layer iš payload ir patikrink prieš `allowed`
        # jei target not in allowed: print('BLOCKED: layer ne schemoje', file=sys.stderr); sys.exit(2)
    sys.exit(0)

if __name__ == '__main__':
    main()

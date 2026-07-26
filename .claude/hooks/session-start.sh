#!/bin/bash
# SessionStart hook — sinchronizuoja repo, įdiegia priklausomybes ir įkelia
# "ką darėm" kontekstą į naują sesiją (desktop / web / bet kuris klientas).
# Visi šalutiniai logai eina į stderr, kad stdout liktų švarus JSON.
set -uo pipefail

PROJ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
APP="$PROJ/cad-site-agent"
HANDOFF="$APP/docs/SESSION_HANDOFF.md"

{
  echo "[session-start] repo: $PROJ"
  cd "$PROJ" 2>/dev/null || { echo "[session-start] no project dir"; }

  # 1) Sinchronizuoti su GitHub (fast-forward; niekada neperrašom lokalių pakeitimų)
  BR="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
  echo "[session-start] branch: $BR — fetch + ff-only pull"
  git fetch origin "$BR" 2>/dev/null || true
  git pull --ff-only origin "$BR" 2>/dev/null || echo "[session-start] pull skipped (no ff or offline)"

  # 2) Priklausomybės — kad testai/pytest veiktų (idempotentiška)
  if command -v python3 >/dev/null 2>&1; then
    echo "[session-start] pip install -e .[dev] (editable + test deps)"
    python3 -m pip install -e "$APP[dev]" >/dev/null 2>&1 || echo "[session-start] pip install skipped (offline/already installed)"
  fi
} 1>&2

# 3) Surinkti kontekstą sesijai: handoff + agentų statusai + paskutiniai commit'ai
RECENT="$(cd "$PROJ" && git log --oneline -8 2>/dev/null || true)"
HANDOFF_TXT=""
[ -f "$HANDOFF" ] && HANDOFF_TXT="$(cat "$HANDOFF")"

# Agentų statusai — TIK ŠVIEŽI (konteksto inžinerija 2026-07-26: pasenęs statusas
# kuria klaidingą sistemos vaizdą ir prieštaraujančias instrukcijas, todėl praleidžiamas).
# Šviežumas matuojamas pagal PASKUTINĮ COMMIT'Ą, ne failo mtime — po švaraus clone visų
# failų mtime vienodas, todėl mtime filtras neveiktų. Fail-open: jei datos nustatyti
# nepavyksta, failas ĮTRAUKIAMAS (geriau perteklius nei prarastas kontekstas).
STATUS_MAX_AGE_DAYS="${STATUS_MAX_AGE_DAYS:-14}"
STATUS_TXT=""
STATUS_SKIPPED=""
STATUS_DIR="$APP/docs/agent-status"
if [ -d "$STATUS_DIR" ]; then
  NOW_TS="$(date +%s)"
  CUTOFF=$(( STATUS_MAX_AGE_DAYS * 86400 ))
  for f in "$STATUS_DIR"/*.md; do
    [ -f "$f" ] || continue
    FTS="$(cd "$PROJ" && git log -1 --format=%ct -- "$f" 2>/dev/null || true)"
    if [ -n "$FTS" ] && [ "$(( NOW_TS - FTS ))" -gt "$CUTOFF" ]; then
      STATUS_SKIPPED="$STATUS_SKIPPED $(basename "$f")($(( (NOW_TS - FTS) / 86400 ))d)"
      continue
    fi
    STATUS_TXT="$STATUS_TXT
--- $(basename "$f") ---
$(cat "$f")
"
  done
  [ -n "$STATUS_SKIPPED" ] && echo "[session-start] praleisti pasenę statusai (>${STATUS_MAX_AGE_DAYS}d):$STATUS_SKIPPED" 1>&2
fi

python3 - "$HANDOFF_TXT" "$RECENT" "$STATUS_TXT" <<'PY'
import json, sys
handoff, recent, status = sys.argv[1], sys.argv[2], sys.argv[3]
ctx = "# Auto-loaded session context (SessionStart hook)\n\n"
if status.strip():
    ctx += "## Agentų koordinacija (kas ką daro)\n" + status + "\n"
if handoff:
    ctx += handoff + "\n\n"
ctx += "## Paskutiniai commit'ai\n" + (recent or "(nėra)") + "\n"
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": ctx
    }
}))
PY

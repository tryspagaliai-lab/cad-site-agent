#!/bin/bash
# Atnaujina agento statusą bendroje koordinacijos lentoje ir push'ina į GitHub.
# Naudojimas: ./.claude/hooks/agent-status.sh <role> "<statuso žinutė>"
#   role: desktop | web | kimi | mimo | <bet koks>
set -uo pipefail

ROLE="${1:-}"
MSG="${2:-}"
if [ -z "$ROLE" ] || [ -z "$MSG" ]; then
  echo "Usage: $0 <role> \"<status message>\"" >&2
  exit 1
fi

PROJ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$PROJ" || { echo "no project dir" >&2; exit 1; }

DIR="cad-site-agent/docs/agent-status"
FILE="$DIR/$ROLE.md"
mkdir -p "$DIR"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
HEAD_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo '?')"
BR="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"

cat > "$FILE" <<EOF
# Agent status: $ROLE

- updated: $TS
- branch: $BR
- head: $HEAD_SHA
- status: $MSG
EOF

# Sinchronizuoti ir push'inti (su pull-rebase retry, jei kitas pastūmė tuo pačiu metu)
git add "$FILE"
if git diff --cached --quiet; then
  echo "[agent-status] no change for $ROLE"
  exit 0
fi
git commit -q -m "agent-status($ROLE): $MSG"

for attempt in 1 2 3; do
  if git push origin "$BR" 2>/dev/null; then
    echo "[agent-status] $ROLE pushed -> $BR ($TS)"
    exit 0
  fi
  echo "[agent-status] push rejected, rebasing (attempt $attempt)" >&2
  git pull --rebase origin "$BR" 2>/dev/null || true
done
echo "[agent-status] PUSH FAILED after retries — statusas commit'intas lokaliai" >&2
exit 1

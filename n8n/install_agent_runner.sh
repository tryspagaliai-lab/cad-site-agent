#!/usr/bin/env bash
# Vienkartinis autonominio VPS agento diegimas.
# Paleisti VPS host'e (root). Naudoja git (ne raw URL), tad šakos vardas su „/" veikia.
set -euo pipefail

REPO=/opt/cad-site-agent
BR=claude/authorize-claude-code-vps-1dcvrv
DST=/usr/local/bin/vps_agent_runner.sh

CLAUDE_BIN="$(command -v claude || true)"
if [ -z "$CLAUDE_BIN" ]; then
  echo "!! 'claude' nerastas PATH'e. Paleisk aplinkoje, kur matomas claude (pvz. po 'source ~/.bashrc')."
  exit 1
fi
echo "==> claude: $CLAUDE_BIN"

echo "==> fetch origin/$BR"
git -C "$REPO" fetch -q origin "$BR"

echo "==> įrašau runner -> $DST"
git -C "$REPO" show "origin/$BR:n8n/vps_agent_runner.sh" \
  | sed "s#__CLAUDE_BIN__#${CLAUDE_BIN}#g" > "$DST"
chmod +x "$DST"

echo "==> cron kas 2 min -> /etc/cron.d/vps-agent"
cat >/etc/cron.d/vps-agent <<EOF
SHELL=/bin/bash
HOME=/root
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
*/2 * * * * root $DST
EOF
chmod 644 /etc/cron.d/vps-agent
service cron reload 2>/dev/null || systemctl restart cron 2>/dev/null || service cron restart 2>/dev/null || true

echo ""
echo "==> OK — autonominis agentas įdiegtas."
echo "    Runner: $DST"
echo "    Cron:   /etc/cron.d/vps-agent (kas 2 min)"
echo "    Log:    /root/agent_runner.log"
echo "    Užduotys: git šaka '$BR', failas 'inbox/TASK.md'."
echo "    Rezultatai: Telegram (@tryspagaliabot) + /root/agent_result_*.txt"

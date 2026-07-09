#!/usr/bin/env bash
# VPS autonominis agentas — git „pašto dėžutė" -> claude -p -> Telegram.
#
# Veikimas: kas kelias minutes (cron) parsisiunčia užduočių šaką, tikrina
# inbox/TASK.md. Jei failo turinys pasikeitė (blob sha) ir nėra „IDLE" —
# paleidžia Claude Code headless režimu (`claude -p`) su ta užduotimi
# repo kataloge, o gautą atsakymą nusiunčia į Telegram (tie patys raktai
# kaip digest'o: /root/ai_digest.env — TELEGRAM_TOKEN, CHAT_ID).
#
# Rezultatas taip pat išsaugomas /root/agent_result_<blob>.txt.
# Diegti per n8n/install_agent_runner.sh (jis įrašo tikrą claude kelią).
set -uo pipefail

REPO=/opt/cad-site-agent
QUEUE=claude/authorize-claude-code-vps-1dcvrv   # užduočių šaka (inbox/TASK.md)
TASKFILE=inbox/TASK.md
STATE=/root/.agent_task_blob
LOG=/root/agent_runner.log
CLAUDE_BIN="__CLAUDE_BIN__"                      # užpildo install skriptas
export HOME=/root

# tik vienas runner vienu metu
exec 9>/root/.agent_runner.lock
flock -n 9 || exit 0

cd "$REPO" 2>/dev/null || exit 1
git fetch -q origin "$QUEUE" 2>>"$LOG" || exit 0

BLOB=$(git rev-parse "origin/$QUEUE:$TASKFILE" 2>/dev/null || echo "")
[ -z "$BLOB" ] && exit 0                          # užduočių failo dar nėra
LAST=$(cat "$STATE" 2>/dev/null || echo "")
[ "$BLOB" = "$LAST" ] && exit 0                    # nieko naujo

TASK=$(git show "origin/$QUEUE:$TASKFILE" 2>/dev/null || echo "")
CLEAN=$(printf '%s' "$TASK" | tr -d '[:space:]')
if [ -z "$CLEAN" ] || [ "$CLEAN" = "IDLE" ]; then
  echo "$BLOB" >"$STATE"                           # tuščia/IDLE — pažymim ir laukiam
  exit 0
fi

send_tg() {
  ( set -a; . /root/ai_digest.env; set +a
    t="${1:0:3900}"                                # Telegram riba ~4096
    curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
      --data-urlencode "chat_id=${CHAT_ID}" \
      --data-urlencode "text=${t}" \
      --data-urlencode "disable_web_page_preview=true" >/dev/null 2>&1 ) || true
}

echo "$(date -Is) RUN blob=$BLOB" >>"$LOG"
send_tg "🤖 VPS agentas: gauta nauja užduotis, vykdau…"

# timeout 15 min — kad pakibęs modelio/tinklo kvietimas ar claude -p niekada nelaikytų lock'o amžinai
OUT=$(cd "$REPO" && IS_SANDBOX=1 timeout -k 30 900 "$CLAUDE_BIN" -p "$TASK" --dangerously-skip-permissions 2>&1)
RC=$?
if [ "$RC" = 124 ] || [ "$RC" = 137 ]; then
  OUT="⏱️ Užduotis NUTRAUKTA po 15 min (timeout) — galimai pakibęs modelio/tinklo kvietimas.
${OUT}"
fi

echo "$(date -Is) DONE rc=$RC" >>"$LOG"
printf '%s\n' "$OUT" >"/root/agent_result_${BLOB:0:12}.txt"
send_tg "$( [ "$RC" = 0 ] && echo '✅' || echo '⚠️' ) VPS agentas baigė (rc=$RC):

${OUT}"

echo "$BLOB" >"$STATE"

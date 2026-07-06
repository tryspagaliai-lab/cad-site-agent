#!/usr/bin/env bash
# AI Research Digest — vieno paleidimo diegimas i VPS n8n.
# Padaro VISKA: sukuria Telegram + Anthropic credentials, irase chat_id,
# importuoja workflow, aktyvuoja ir paleidzia testini vykdyma.
#
# Naudojimas (viena eilute, irasyk savo reiksmes):
#   TELEGRAM_TOKEN='123:ABC' CHAT_ID='123456789' ANTHROPIC_KEY='sk-ant-...' \
#     bash -c "$(curl -fsSL https://raw.githubusercontent.com/tryspagaliai-lab/cad-site-agent/claude/lithuanian-language-question-7al6mx/n8n/vps_install_digest.sh)"
set -euo pipefail

: "${TELEGRAM_TOKEN:?Truksta TELEGRAM_TOKEN (boto tokenas is @BotFather)}"
: "${CHAT_ID:?Truksta CHAT_ID (skaicius is @userinfobot)}"
ANTHROPIC_KEY="${ANTHROPIC_KEY:-}"   # neprivalomas: be jo ataskaita bus be AI santraukos

RAW_BASE="https://raw.githubusercontent.com/tryspagaliai-lab/cad-site-agent/claude/lithuanian-language-question-7al6mx/n8n"
WF_ID="zzAiDigestWf0001"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "==> [1/5] Siunciuosi workflow JSON is GitHub..."
curl -fsSL "$RAW_BASE/ai-research-digest.workflow.json" -o "$TMP/wf.json"
sed -i "s/PAKEISK_I_SAVO_CHAT_ID/${CHAT_ID}/" "$TMP/wf.json"

echo "==> [2/5] Ruosiu credentials..."
if [ -n "$ANTHROPIC_KEY" ]; then
  cat > "$TMP/creds.json" <<EOF
[
  {"id":"zzTgDigestCred01","name":"AI Digest Bot (Telegram)","type":"telegramApi","data":{"accessToken":"${TELEGRAM_TOKEN}"}},
  {"id":"zzAnthropicCr001","name":"Anthropic API (x-api-key)","type":"httpHeaderAuth","data":{"name":"x-api-key","value":"${ANTHROPIC_KEY}"}}
]
EOF
else
  echo "    (ANTHROPIC_KEY neduotas - ataskaita eis be AI santraukos; veliau ji pridesi)"
  sed -i 's/claude-sonnet-5/none/g' "$TMP/wf.json"
  cat > "$TMP/creds.json" <<EOF
[
  {"id":"zzTgDigestCred01","name":"AI Digest Bot (Telegram)","type":"telegramApi","data":{"accessToken":"${TELEGRAM_TOKEN}"}}
]
EOF
fi

if command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}} {{.Image}}' | grep -qi n8n; then
  C="$(docker ps --format '{{.Names}} {{.Image}}' | grep -i n8n | head -1 | cut -d' ' -f1)"
  echo "==> Radau n8n docker konteineri: $C"
  NEXEC=(docker exec -u node "$C")
  docker cp "$TMP/wf.json" "$C:/tmp/zz_wf.json"
  docker cp "$TMP/creds.json" "$C:/tmp/zz_creds.json"
  WF_PATH=/tmp/zz_wf.json; CR_PATH=/tmp/zz_creds.json
elif command -v n8n >/dev/null 2>&1; then
  echo "==> Naudoju vietini n8n CLI (be docker)"
  NEXEC=()
  WF_PATH="$TMP/wf.json"; CR_PATH="$TMP/creds.json"
else
  echo "!! Neradau nei n8n docker konteinerio, nei n8n CLI. Ar cia tikrai n8n VPS?" >&2
  exit 1
fi

echo "==> [3/5] Importuoju credentials ir workflow..."
"${NEXEC[@]}" n8n import:credentials --input="$CR_PATH"
"${NEXEC[@]}" n8n import:workflow --input="$WF_PATH"

echo "==> [4/5] Aktyvuoju workflow (kasdien 08:00)..."
"${NEXEC[@]}" n8n update:workflow --id="$WF_ID" --active=true

echo "==> [5/5] Testinis paleidimas (1-2 min, ziurek Telegram!)..."
"${NEXEC[@]}" n8n execute --id="$WF_ID" >/dev/null 2>&1 \
  && echo "    Testas ivykdytas - patikrink Telegram." \
  || echo "    !! Testinis vykdymas meta klaida (bet workflow idiegtas). Perkrovus n8n suveiks pagal tvarkarasti."

if [ ${#NEXEC[@]} -gt 0 ]; then
  docker exec -u node "$C" rm -f /tmp/zz_wf.json /tmp/zz_creds.json || true
  echo "==> Perkraunu n8n konteineri, kad tvarkarastis isijungtu..."
  docker restart "$C" >/dev/null
else
  systemctl restart n8n 2>/dev/null || pm2 restart n8n 2>/dev/null || echo ">> Perkrauk n8n ranka, kad tvarkarastis isijungtu."
fi

echo ""
echo "==> BAIGTA! Ataskaita ateis kasdien 08:00 (Europe/Vilnius) i tavo Telegram."

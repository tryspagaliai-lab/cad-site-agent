#!/usr/bin/env bash
# Idiegia standalone AI digest tiesiai i serveri (be n8n): env + skriptas + cron 08:00,
# ir PALEIDZIA VIENA KARTA is karto (matai rezultata + Telegram).
set -euo pipefail
: "${TELEGRAM_TOKEN:?Truksta TELEGRAM_TOKEN}"
: "${CHAT_ID:?Truksta CHAT_ID}"
: "${GEMINI_KEY:?Truksta GEMINI_KEY}"

RAW="https://raw.githubusercontent.com/tryspagaliai-lab/cad-site-agent/claude/lithuanian-language-question-7al6mx/n8n/ai_digest.py"

echo "==> Rasau konfigą /root/ai_digest.env..."
cat > /root/ai_digest.env <<EOF
TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
CHAT_ID=${CHAT_ID}
GEMINI_KEY=${GEMINI_KEY}
EOF
chmod 600 /root/ai_digest.env

echo "==> Parsisiunciu skripta /root/ai_digest.py..."
curl -fsSL "$RAW" -o /root/ai_digest.py

echo "==> Isjungiu (klaidinga) n8n digest workflow, kad netrukdytu..."
C=$(docker ps --format '{{.Names}}' | grep -i n8n | head -1 || true)
if [ -n "${C:-}" ]; then
  docker exec -u node "$C" n8n update:workflow --id=zzAiDigestWf0001 --active=false >/dev/null 2>&1 || true
  docker restart "$C" >/dev/null 2>&1 || true
fi

echo "==> Registruoju cron (kasdien 08:00 Europe/Vilnius)..."
cat > /etc/cron.d/ai-digest <<'EOF'
CRON_TZ=Europe/Vilnius
0 8 * * * root bash -c 'set -a; . /root/ai_digest.env; set +a; /usr/bin/python3 /root/ai_digest.py' >> /var/log/ai_digest.log 2>&1
EOF
chmod 644 /etc/cron.d/ai-digest
systemctl restart cron 2>/dev/null || service cron restart 2>/dev/null || true

echo ""
echo "==> TESTAS: paleidziu dabar (ziurek Telegram)..."
set -a; . /root/ai_digest.env; set +a
python3 /root/ai_digest.py

echo ""
echo "==> BAIGTA. Kasdien 08:00 (Vilnius) ataskaita ateis i Telegram automatiskai."

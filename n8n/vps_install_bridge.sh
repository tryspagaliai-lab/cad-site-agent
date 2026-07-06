#!/usr/bin/env bash
# Idiegia "Claude VPS Shell (MCP)" tilta i VPS n8n.
# Po sekmingo paleidimo parodo MCP URL, kuri reikia prijungti prie Claude.
set -euo pipefail

RAW_BASE="https://raw.githubusercontent.com/tryspagaliai-lab/cad-site-agent/claude/lithuanian-language-question-7al6mx/n8n"
MAIN_ID="zzVpsShellMcp01"
MCP_PATH="claude-vps-shell-x7k9q2m4p8w1"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

C="$(docker ps --format '{{.Names}}' | grep -i n8n | head -1)"
[ -z "$C" ] && { echo "!! n8n docker konteineris nerastas"; exit 1; }
echo "==> n8n konteineris: $C"

echo "==> Siunciuosi workflow failus..."
curl -fsSL "$RAW_BASE/claude-vps-shell.sub.json"  -o "$TMP/sub.json"
curl -fsSL "$RAW_BASE/claude-vps-shell.main.json" -o "$TMP/main.json"

docker cp "$TMP/sub.json"  "$C:/tmp/zz_sub.json"
docker cp "$TMP/main.json" "$C:/tmp/zz_main.json"

echo "==> Importuoju..."
docker exec -u node "$C" n8n import:workflow --input=/tmp/zz_sub.json
docker exec -u node "$C" n8n import:workflow --input=/tmp/zz_main.json

echo "==> Aktyvuoju MCP tilta..."
docker exec -u node "$C" n8n update:workflow --id="$MAIN_ID" --active=true

docker exec -u node "$C" rm -f /tmp/zz_sub.json /tmp/zz_main.json || true
echo "==> Perkraunu n8n..."
docker restart "$C" >/dev/null

echo ""
echo "======================================================================"
echo "  BAIGTA. Prijunk sita MCP URL prie Claude (Settings -> Connectors):"
echo ""
echo "     https://n8n.tryspagaliai.com/mcp/${MCP_PATH}"
echo ""
echo "  (Jei domenas kitoks, pakeisk host'a; kelias po /mcp/ - teisingas.)"
echo "======================================================================"

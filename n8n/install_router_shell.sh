#!/usr/bin/env bash
# Prideda run_shell toola prie jau prijungto n8n MCP router'io (n8n_VPS).
# Nekuria naujos jungties. Daro atsargine kopija pries keitima.
set -euo pipefail

RAW="https://raw.githubusercontent.com/tryspagaliai-lab/cad-site-agent/claude/lithuanian-language-question-7al6mx/n8n/patch_router.py"
SUB_ID="zzVpsExecSub001"

C=$(docker ps --format '{{.Names}}' | grep -i n8n | head -1)
[ -z "$C" ] && { echo "!! n8n konteineris nerastas"; exit 1; }
echo "==> n8n konteineris: $C"

echo "==> Eksportuoju visus workflow'us..."
docker exec -u node "$C" n8n export:workflow --all --output=/tmp/zz_all.json
docker cp "$C:/tmp/zz_all.json" /root/zz_all_backup.json
echo "    Atsargine kopija: /root/zz_all_backup.json"

echo "==> Parsisiunciu patch skripta..."
curl -fsSL "$RAW" -o /root/patch_router.py

echo "==> Patch'inu (tik pridedu run_shell)..."
python3 /root/patch_router.py /root/zz_all_backup.json "$SUB_ID"

docker cp /tmp/router_patched.json "$C:/tmp/router_patched.json"
echo "==> Importuoju atnaujinta router'i..."
docker exec -u node "$C" n8n import:workflow --input=/tmp/router_patched.json

RID=$(cat /tmp/router_id.txt)
if [ -n "$RID" ]; then
  docker exec -u node "$C" n8n update:workflow --id="$RID" --active=true >/dev/null 2>&1 || true
fi

echo "==> Perkraunu n8n..."
docker restart "$C" >/dev/null

echo ""
echo "======================================================================"
echo "  BAIGTA. Prie tavo esamo n8n_VPS connector'io pridetas irankis: run_shell"
echo "  Claude aplikacijoje: Settings -> Connectors -> n8n_VPS -> isjunk ir vel"
echo "  ijunk (refresh), kad naujas irankis atsirastu."
echo "  Jei kas nors sugedo: atsargine kopija /root/zz_all_backup.json"
echo "======================================================================"

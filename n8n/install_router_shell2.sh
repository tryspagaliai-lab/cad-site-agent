#!/usr/bin/env bash
# run_shell v2: toolCode (kaip ping) su child_process. Baze - svarus backup router.
set -euo pipefail
RAW="https://raw.githubusercontent.com/tryspagaliai-lab/cad-site-agent/claude/lithuanian-language-question-7al6mx/n8n/patch_router2.py"
C=$(docker ps --format '{{.Names}}' | grep -i n8n | head -1)
[ -z "$C" ] && { echo "!! n8n konteineris nerastas"; exit 1; }

[ -f /root/zz_all_backup.json ] || { echo "!! /root/zz_all_backup.json nerastas (paleisk install_router_shell.sh anksciau)"; exit 1; }

echo "==> Parsisiunciu patch2..."
curl -fsSL "$RAW" -o /root/patch_router2.py
python3 /root/patch_router2.py /root/zz_all_backup.json

docker cp /tmp/router2.json "$C:/tmp/router2.json"
echo "==> Importuoju router su run_shell (toolCode)..."
docker exec -u node "$C" n8n import:workflow --input=/tmp/router2.json

RID=$(cat /tmp/router_id.txt)
echo "==> Publish + aktyvacija (id=$RID)..."
docker exec -u node "$C" n8n update:workflow --id="$RID" --active=true >/dev/null 2>&1 || true
docker exec -u node "$C" n8n publish:workflow --id="$RID" >/dev/null 2>&1 || true

echo "==> Perkraunu n8n..."
docker restart "$C" >/dev/null
echo ""
echo "==> BAIGTA. run_shell (toolCode) turi atsirasti n8n_VPS connector'yje."
echo "    Claude app: Settings -> Connectors -> n8n VPS -> Disconnect, tada prijunk is naujo (arba naujas pokalbis)."

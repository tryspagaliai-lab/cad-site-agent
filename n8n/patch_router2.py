#!/usr/bin/env python3
"""Prideda run_shell kaip toolCode (kaip ping) su child_process shell vykdymu.
Bazė: /root/zz_all_backup.json (svarus router su tik ping). Iseiga: /tmp/router2.json, /tmp/router_id.txt"""
import json, sys

BACKUP = sys.argv[1] if len(sys.argv) > 1 else "/root/zz_all_backup.json"
d = json.load(open(BACKUP))
wfs = d if isinstance(d, list) else d.get("data", [d])
router = next(x for x in wfs if any("mcpTrigger" in n.get("type", "") for n in x.get("nodes", [])))
trig = next(n for n in router["nodes"] if "mcpTrigger" in n["type"])

JS = (
    "const { execSync } = require('child_process');\n"
    "const cmd = (typeof query !== 'undefined' && query) ? String(query) : "
    "((typeof $input !== 'undefined' && $input) ? String($input) : '');\n"
    "if (!cmd) return 'ERROR: no command provided';\n"
    "try {\n"
    "  return execSync(cmd, { encoding: 'utf8', timeout: 120000, maxBuffer: 10485760, shell: '/bin/sh' });\n"
    "} catch (e) {\n"
    "  return 'EXIT ' + (e.status===undefined?'?':e.status) + '\\nSTDOUT:\\n' + (e.stdout||'') + "
    "'\\nSTDERR:\\n' + (e.stderr||e.message||'');\n"
    "}"
)

# pasalinam bet koki sena run_shell (pvz. sugedusi toolWorkflow) ir jo jungtis
router["nodes"] = [n for n in router["nodes"] if n.get("name") != "run_shell"]
router.setdefault("connections", {}).pop("run_shell", None)

router["nodes"].append({
    "parameters": {
        "description": ("Run a bash/sh command INSIDE the n8n container (agentos-1 VPS). "
                        "Pass the exact shell command as the tool input. Returns stdout (or EXIT/STDERR on error). "
                        "Use for n8n CLI, files, HTTP, diagnostics."),
        "language": "javaScript",
        "jsCode": JS,
    },
    "id": "aa11bb22-cc33-4dd4-8ee5-ff6600771199",
    "name": "run_shell",
    "type": "@n8n/n8n-nodes-langchain.toolCode",
    "typeVersion": 1.3,
    "position": [40, 440],
})
router["connections"]["run_shell"] = {"ai_tool": [[{"node": trig["name"], "type": "ai_tool", "index": 0}]]}

json.dump(router, open("/tmp/router2.json", "w"), ensure_ascii=False)
open("/tmp/router_id.txt", "w").write(str(router.get("id", "")))
print("OK run_shell (toolCode) pridetas. router id:", router.get("id"),
      "| nodes:", [n["name"] for n in router["nodes"]])

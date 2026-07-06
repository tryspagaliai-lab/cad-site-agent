#!/usr/bin/env python3
"""Saugiai prideda run_shell (Execute Command sub-workflow) toolą prie esamo n8n MCP router'io.
Naudojimas: python3 patch_router.py <exported_all.json> <sub_workflow_id>
Iseiga: /tmp/router_patched.json ir /tmp/router_id.txt"""
import json, sys

path, subid = sys.argv[1], sys.argv[2]
ROUTER_NAME = "mcp-universal-router-desk"

data = json.load(open(path))
wfs = data if isinstance(data, list) else data.get("data", data if isinstance(data, list) else [data])
if isinstance(wfs, dict):
    wfs = [wfs]

def has_mcp(w):
    return any("mcpTrigger" in n.get("type", "") for n in w.get("nodes", []))

# 1) tikslus vardas; 2) bet koks mcpTrigger workflow, kuris NE musu shell bridge
router = next((w for w in wfs if w.get("name") == ROUTER_NAME), None)
if router is None:
    router = next((w for w in wfs if w.get("id") != "zzVpsShellMcp01" and has_mcp(w)), None)
assert router is not None, "MCP router nerastas eksporte"

trig = next(n for n in router["nodes"] if "mcpTrigger" in n["type"])

if not any(n.get("name") == "run_shell" for n in router["nodes"]):
    pos = trig.get("position", [0, 0])
    router["nodes"].append({
        "parameters": {
            "name": "run_shell",
            "description": ("Run a bash command on the VPS (agentos-1) and return stdout, stderr, "
                            "exitCode. Managing n8n, files, installs, diagnostics."),
            "workflowId": {"__rl": True, "value": subid, "mode": "id"},
            "workflowInputs": {
                "mappingMode": "defineBelow",
                "value": {"command": "={{ $fromAI('command', 'the exact bash command to execute', 'string') }}"},
                "schema": [{"id": "command", "displayName": "command", "required": True, "type": "string",
                            "display": True, "defaultMatch": False, "canBeUsedToMatch": True}],
                "matchingColumns": [], "attemptToConvertTypes": False, "convertFieldsToString": True,
            },
        },
        "id": "dd000001-0001-4001-8001-000000000099",
        "name": "run_shell",
        "type": "@n8n/n8n-nodes-langchain.toolWorkflow",
        "typeVersion": 2,
        "position": [pos[0] + 260, pos[1] + 260],
    })
    router.setdefault("connections", {})
    router["connections"].setdefault("run_shell", {})["ai_tool"] = [[{"node": trig["name"], "type": "ai_tool", "index": 0}]]
    print("run_shell PRIDETAS prie router'io:", router.get("name"))
else:
    print("run_shell jau buvo — praleista")

json.dump(router, open("/tmp/router_patched.json", "w"), ensure_ascii=False)
open("/tmp/router_id.txt", "w").write(str(router.get("id", "")))
print("router id:", router.get("id"), "| mcp trigger node:", trig.get("name"))

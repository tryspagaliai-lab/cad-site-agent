# VPS automatika — AI Research Digest + Claude valdymo tiltas

> Atmintis apie 2026-07-06 sesiją (web, telefonu). Viskas dėliota vien iš telefono.
> **Repo VIEŠAS — jokių tokenų/raktų/slaptažodžių čia. Tik architektūra ir failų vietos.**

## VPS (Hetzner)
- Serveris: **agentos-1**, Hetzner Cloud (projektas „agentos"), Helsinki. IPv4 **77.42.94.63**. Ubuntu 24.04, CX23.
- SSH: `root` + slaptažodis. Slaptažodinis SSH įjungtas per Rescue (`/etc/ssh/sshd_config.d/01a.conf`:
  `PermitRootLogin yes`, `PasswordAuthentication yes`). Prisijungimas iš telefono per **Termius**.
- Root slaptažodį atstatyti: Hetzner Console → agentos-1 → **Rescue → Reset root password** (įsigalioja iškart).
- n8n web: **https://n8n.tryspagaliai.com** (pagr. domenas tryspagaliai.com be DNS; naudojamas subdomenas).

## n8n
- Docker konteineris: **n8n-n8n-1**, n8n **2.28.4**. CLI per `docker exec -u node n8n-n8n-1 n8n ...`.
- MCP router (prijungtas prie Claude kaip connector **n8n_VPS**): „**MCP Universal Router (Desk)**“,
  id `mcprouterdesk001`, MCP trigger node „MCP Server Trigger“. Įrankiai: `ping` (+ pridėtas `run_shell`, žr. žemiau).

## AI Research Digest (VEIKIA)
- **Standalone**, NE per n8n mazgus (n8n variantas buvo nepatikimas → atsisakyta). Kelias: RSS/HF → Gemini → Telegram.
- Serveryje: `/root/ai_digest.py` (skriptas), `/root/ai_digest.env` (raktai, chmod 600, **ne repo**),
  cron `/etc/cron.d/ai-digest` → **kasdien 08:00 Europe/Vilnius** (`CRON_TZ=Europe/Vilnius`).
- LLM: **Google Gemini `gemini-flash-latest`**, `thinkingConfig.thinkingBudget=0` (kitaip visi tokenai eina į
  „mąstymą“ ir tekstas grįžta tuščias — pagrindinė pamoka). **Nemokamas** (free tier), €0. Anthropic buvo išbandytas,
  bet MOKAMAS (atskirai nuo Max) → atsisakyta, raktą rekomenduojama atšaukti.
- Telegram: botas @tryspagaliabot, **chat_id 725037198**. Testas: `surinkta 53 naujienu / issiusta i Telegram`.
- Repo failai: `n8n/ai_digest.py`, `n8n/install_digest_cron.sh` (idempotentiškas diegimas + testas).
- Šaltiniai (19 RSS + HF modeliai): arXiv cs.AI/LG/CL, OpenAI, DeepMind, Google AI, MS Research, MIT, BAIR,
  Import AI, Simon Willison ir kt. Šiuo metu pasenę (praleidžiami): Meta AI (404), Stanford HAI (XML klaida) — pataisyti.

## Claude valdymo tiltas (run_shell) — DALINAI
- Tikslas: kad Claude pats vykdytų komandas VPS'e per MCP, be copy-paste.
- Sub-workflow `zzVpsExecSub001` („vps-exec“): Execute Workflow Trigger → Execute Command → grąžina stdout/stderr.
- `run_shell` tool **PRIDĖTAS** prie router'io `mcprouterdesk001` (addityviai; backup `/root/zz_all_backup.json`).
- **Serverio pusė BAIGTA:** `n8n publish:workflow --id=mcprouterdesk001` + restart atlikta 2026-07-06 —
  `run_shell` publikuotas router'yje. (Reikėjo `publish`, ne `update:workflow --active`.)
- **DIAGNOZĖ (2026-07-06 vakaras):** connector rodo TIK „Ping". Router'io `ping` yra
  **`@n8n/n8n-nodes-langchain.toolCode`** (JS code tool, typeVersion 1.3), `ai_tool → MCP Server Trigger`.
  Mano `run_shell` buvo `toolWorkflow` → šios n8n versijos MCP trigger jo NEIŠVEDĖ. Išvedami tik `toolCode` tipo.
- **SPRĘSTA ✅ (2026-07-06):** `run_shell` padarytas `toolCode` tipo (kaip ping) su `require('child_process').execSync(query)`.
  Konteineryje env JAU buvo `NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs,path` (+ runner atitikmuo), tad shell veikia
  iš karto. Įdiegimas: `n8n/patch_router2.py` + `n8n/install_router_shell2.sh` (bazė = `/root/zz_all_backup.json`).
  Patikrinta naujame Claude pokalbyje: `uname -a && whoami && ls /` → whoami=**node**, veikia.
- **APRIBOJIMAS:** komandos vykdomos **n8n KONTEINERIO viduje** (user `node`), NE host'e. Tinka n8n CLI/failams/HTTP/
  diagnostikai. Host lygio (apt, docker, /root) — reiktų atskiro host agento (dar nepadaryta).
- **Naudojimas:** naujame Claude pokalbyje (šioje app'e, n8n_VPS connector ON) → „paleisk per run_shell: <cmd>“.
  Senoje sesijoje naujas įrankis „karštai" neatsiranda — reikia naujo pokalbio / reconnect.
- Ping = `@n8n/n8n-nodes-langchain.toolCode` typeVersion 1.3, `ai_tool → MCP Server Trigger` (šabloną atkartojom).
  Nepavykęs `toolWorkflow` sub-workflow `zzVpsExecSub001` — nebenaudojamas, galima trinti.
- Atskiras MCP shell bridge (jei prireiktų vietoj router'io): workflow `zzVpsShellMcp01`,
  URL `…/mcp/claude-vps-shell-…` (žr. `n8n/vps_install_bridge.sh`). Reikalauja custom connector (tik per kompiuterį).

## CAD pipeline VPS'e (2026-07-06) ✅
- Projektas nuklonuotas: **`/opt/cad-site-agent`** (git, --depth 1). Vidinis paketas `/opt/cad-site-agent/cad-site-agent`.
- venv: **`/opt/cad-venv`** (python3.12). `pip install -e .` pavyko — ezdxf, shapely, scipy, matplotlib, mcp ir kt.
- `/opt/cad-venv/bin/cad-agent --help` veikia (analyze-dxf, clean-dxf, close-gaps, process, route-features, …).
- **DWG įvestims reiktų ODA File Converter** (host'e dar neįdiegtas; žr. docs/ODA_SETUP.md). DXF veikia iš karto.
- **H7149/Osprey raw duomenų VPS'e NĖRA** — buvo tik laptope. Jei laptopo nebėra → prarasti (tikslinti su vartotoju).

## Claude Code ant VPS ✅ (įdiegta 2026-07-06)
- Node **v22.23.1** (NodeSource), Claude Code **2.1.201** (`npm i -g @anthropic-ai/claude-code`).
- Paleidimas: `cd /opt/cad-site-agent && claude`. Repo šaknis = `/opt/cad-site-agent` (ten `.claude/settings.json`),
  tad SessionStart hook (repo sync + handoff kontekstas) + PreToolUse gardas užsikrauna automatiškai.
- **Auth:** per Max prenumeratą (`/login` → OAuth nuoroda telefone → kodas atgal). BE API mokesčio. **AUTORIZUOTA ✅ (2026-07-06).**

## Superpowers plugin (obra/superpowers)
- Autorius: Jesse Vincent (GitHub **obra**). 14 skills: test-driven-development, systematic-debugging,
  verification-before-completion, brainstorming, writing-plans, executing-plans, dispatching-parallel-agents,
  requesting/receiving-code-review, using-git-worktrees, finishing-a-development-branch,
  subagent-driven-development, writing-skills, using-superpowers.
- Repo šaknies `.claude/settings.json` turi `extraKnownMarketplaces` (obra/superpowers-marketplace) +
  `enabledPlugins` (`superpowers@superpowers-marketplace`) → nauja Claude Code sesija šiame repo pasiūlys
  įdiegti automatiškai (patvirtinti trust dialoge).
- Rankinis diegimas VPS'e (Termius, vienkartinis, galioja visam useriui):
  `claude plugin marketplace add obra/superpowers-marketplace && claude plugin install superpowers@superpowers-marketplace`
  arba Claude Code viduje: `/plugin install superpowers@claude-plugins-official`.

## Saugumo TODO (svarbu)
1. **Atšaukti Anthropic raktą** (console.anthropic.com → API Keys) — nebenaudojamas.
2. **MCP shell path yra viešame repo** (`n8n/vps_install_bridge.sh`) — kas žino URL, gali gauti shell.
   Rekomenduojama: pridėti auth n8n MCP trigger'iui arba pakeisti path'ą (rotacija) ir NEbetalpinti į repo.
3. Telegram boto token buvo persiųstas pokalbyje → **pergeneruoti per @BotFather** (`/revoke`) ir atnaujinti
   `/root/ai_digest.env` + n8n Telegram credential.
4. Įjungti **2FA** Hetzner paskyroje.

## Kaip paleisti/patikrinti digest ranka (Termius)
```bash
set -a; . /root/ai_digest.env; set +a; python3 /root/ai_digest.py   # turi parodyti "issiusta i Telegram"
```

## HERA / „Link Parser" botas (2026-07-07 diagnostika + GitHub auditas)
- **Botas = n8n workflow „Link Parser" (`linkparserwork01`), ACTIVE VPS'e** (docker `n8n-n8n-1`).
  Pollina Telegram (@tryspagaliabot, chat 725037198), failus PRIIMA ir deda į eilę
  `pending-ingest/` konteineryje (store-and-forward). Gyvas kodas — node „Poll & Process";
  backup `/root/zz_all_backup.json`.
- **Worker'is (HERA ingest bridge, port 8799) — TIK laptope** (`tryspagaliai-inspiron-5748`,
  Tailscale `100.68.100.14`). Node'e užkoduota `INGEST_BRIDGE='http://100.68.100.14:8799'`.
  Laptopas offline → failai kaupiasi eilėje (nepradingsta), bet neapdorojami.
- **GitHub auditas (2026-07-07):** ingest-bridge worker'io kodo GitHub'e NĖRA —
  `INGEST_BRIDGE`, `pending-ingest`, `flushPendingJobs`, `8799` = 0 rezultatų visuose repo.
  → tas worker'is egzistuoja **tik laptope** (jei laptopo nebėra — prarastas / atkurti iš n8n node kontrakto).
- **HERA agentų frameworkas** (ne šis failų worker'is) trackinamas repo **`tryspagaliai-lab/agentos-sessions`**:
  `hera_runner`, „HERA Controller", `HERA CheckpointManager (vault mirror)`, `hera-core`, `hera-rebuild-phase1`.
- **SVARBU:** `agentos-sessions` README = *„AgentOS Bridge — async message bus tarp chat-Claude ↔ Claude Code"*.
  Tai reiškia, kad ši sesijoje ad-hoc pastatyta `inbox/`+cron grandinė DUBLIUOJA jau egzistuojančią
  AgentOS Bridge infrastruktūrą — vėliau verta konsoliduoti (naudoti agentos-sessions vietoj cad-site-agent/inbox).
- Variantui B (HERA worker VPS'e) reikia arba (a) laptopo bent kartą — parsinešti worker'io kodą,
  arba (b) atkurti minimalų 8799 HTTP servisą pagal n8n node payload kontraktą (be originalios logikos).
```

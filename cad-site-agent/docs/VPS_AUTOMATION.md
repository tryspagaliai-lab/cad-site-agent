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
- **SPRENDIMAS (nebaigtas):** `run_shell` daryti `toolCode` tipo (kaip ping), bet toolCode sandbox pagal nutylėjimą
  blokuoja `child_process`. Reikia n8n konteineriui env **`NODE_FUNCTION_ALLOW_BUILTIN=*`** (+ recreate), tada
  toolCode gali `require('child_process').execSync(cmd)`. Alternatyva: toolCode → HTTP POST į Webhook workflow su
  Execute Command node (jei nenorim keisti env). Sub-workflow `zzVpsExecSub001` (toolWorkflow) — nepasiteisino, galima trinti.
- Ping node kodas (pavyzdys, kaip apibrėžtas veikiantis tool): grąžina `JSON.stringify({status:'ok',...})`.
- Atskiras MCP shell bridge (jei prireiktų vietoj router'io): workflow `zzVpsShellMcp01`,
  URL `…/mcp/claude-vps-shell-…` (žr. `n8n/vps_install_bridge.sh`). Reikalauja custom connector (tik per kompiuterį).

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

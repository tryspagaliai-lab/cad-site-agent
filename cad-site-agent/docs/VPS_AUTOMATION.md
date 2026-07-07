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

### STATUS 2026-07-07 — HERA ingest worker ATKURTAS VPS'e ✅ (Variantas B (b))
- Laptopo nėra ir nežinia kada bus → worker'is atkurtas iš naujo VPS'e (originalaus kodo GitHub'e nebuvo).
- **Worker:** `/opt/hera-ingest/worker.py` (Python stdlib), systemd `hera-ingest.service` ACTIVE, `0.0.0.0:8799`.
- **Kontraktas** (iš n8n „Poll & Process"): Bearer `INGEST_BRIDGE_TOKEN`; `POST /file?name=X` (octet-stream) → `{ok,dest}`;
  `POST /job` (JSON `{id,channel,kind,payload,chat_id,received_at,prefetched?}`, kind∈file/url/youtube/text/council_decision) → `{ok,id}`; `GET /health`.
- **Vault:** `/opt/hera-vault/ingest/<YYYY-MM-DD>/<id>/payload.json` (+ failas). Kol kas TIK priima+saugo+ack (jokios analizės).
- **Tinklas:** iš n8n konteinerio pasiekiama `http://172.18.0.1:8799` (docker bridge gw; `host.docker.internal` neveikia). ufw: docker subnet → 8799.
- **CUTOVER (2026-07-07):** n8n `INGEST_BRIDGE` 100.68.100.14:8799 (miręs laptopas) → `172.18.0.1:8799`. Workflow „Link Parser" liko ACTIVE.
  Backup: `/root/linkparser_pre_cutover.json` (rollback NEREKOMENDUOJAMAS — senas bridge miręs). Eilė flush'inta: 3 job'ai, photo.jpg atkurtas (validus JPEG).
- **BUG pataisytas:** n8n flush kelyje failą siunčia kaip JSON-Buffer envelope (`{type:Buffer,data:[...]}`); worker `/file` dabar atsuka į raw baitus.
- **LIKO Fazė 2:** tikroji HERA apdorojimo logika (ką daryti su url/youtube/file/text/council_decision — parsingas, vault indeksavimas) — originalo nėra, reikės apibrėžti iš naujo.

### Fazė 2 — reikalavimai (iš vartotojo 2026-07-07) + GitHub auditas
- **Org turi 5 repo:** claudeaios-vault (priv, VAULT — HERA žinių saugykla), agentos-sessions (priv, sesijų archyvas + chat↔CC tiltas, HERA specai/logai),
  cad-site-agent (viešas), cad-cleanup-knowledge (viešas), shakespeare-automation (priv). **Atskiro HERA/`hera-core` repo NĖRA** —
  HERA runtime + ingest worker gyveno lokaliai (laptope) → tikėtina prarasti. Panaudojamo HERA pipeline kodo/speco GitHub'e nerasta (code search visur 0).
- **Vartotojo Fazės 2 reikalavimai:** NE santrauka, o **gilus, pilnas ištraukimas**. Ilgi video/audio **karpomi gabalais**, kiekvienas gabalas apdorojamas,
  rezultatai sujungiami (nesvarbu trukmė/ilgis). Tas pats su image formatais. Po ištraukimo — **HERA agento darbas: atrinkti iš info tai,
  kas tinka SISTEMOS augimui / tobulėjimui / plėtrai** (self-evolving system agents).
- **Kind'ai:** url / youtube / file(image,pdf,audio,video) / text / council_decision.
- **Siūloma architektūra (statoma iš nulio VPS'e):** fetch sluoksnis (readability url; yt-dlp+ffmpeg media) → deep-extract per Gemini (free tier, €0;
  multimodalis: tekstas/vaizdas/audio/video/pdf; ilgi media chunkinami) → pilnas rezultatas į /opt/hera-vault/ → HERA selektorius (antra Gemini/agent pakopa)
  atrenka „naudinga augimui" → kandidatai į augimo eilę. (Vėliau sinchronizuoti į claudeaios-vault, kai bus GitHub write.)
- **Stadijos:** 2a url+text · 2b youtube+audio+video (chunk+transcribe) · 2c image (vision) · 2d HERA selektorius.
- **Statusas 2026-07-07:** branduolys pastatytas — url✅ + image✅ ekstraktoriai duoda full.md; youtube❌ (taisoma),
  hera-processor servisas + HERA selektorius (growth) — taisoma užduotimi `6118390`.

### Strateginė kryptis (vartotojas 2026-07-07)
- **PARSER (HERA ingest) = pagrindinis NAUJŲ GALIMYBIŲ šaltinis.** Vartotojas siunčia turinį (url/video/failai),
  HERA giliai ištraukia + atrenka, kas verta sistemos augimui/plėtrai → self-evolving kilpa. Tai prioritetas.
- **Digest ir Parser = ta pati mašina, priešingos kryptys** (digest stumia naujienas → tu; parser traukia tavo turinį → sistema),
  tas pats botas @tryspagaliabot (chat 725037198) ir tas pats Gemini free variklis.
- **Planas: SUJUNGTI į vieną HERA info-pipeline'ą** — visi šaltiniai (tavo įkelti + digest naujienos) → tas pats gilus ištraukimas →
  HERA selektorius nukreipia: *paviešinti* (Telegram) / *saugoti* (vault) / *pasiūlyti augimui* (growth). Digest tampa dar vienu HERA šaltiniu.
  Daryti PO to, kai Fazė 2 stabili.

### Fazė 3 — BAIGTA ✅ (2026-07-07, task c72acff)
- **ATDP-lite trajektorijos:** `/opt/hera-vault/trajectories/<data>.jsonl` (tipizuoti įrašai, reward laukas atnaujinamas vėliau).
- **Skill-output:** `/opt/hera-vault/skills/<slug>/SKILL.md` — HERA pati gamina įgūdžių juodraščius (pvz. `ai-wargaming-metodika`).
- **Kontrafaktinis pakartojimas:** `/opt/hera-processor/hera_replay.py` — validacijos vartai prieš priimant pakeitimą.

### Fazė 4 — HERA selektoriaus verdiktai iš 6 parsintų video (2026-07-07)
- 🟢 **Multi-SKILL/SAGE/Agentic Proposing (9.5):** skill-tuple `(intent,method,difficulty,tool-hint)` + kaupianti biblioteka + 3-lygių įkėlimas + selektyvi atranka/pruning. (RL/GPU dalis — ne.)
- 🟢 **AutoMem (9.0):** struktūros-optimizavimo outer-loop — meta-LLM peržiūri ATDP trajektorijas → siūlo prompt/skill pataisas → replay validuoja. (LoRA — ne, GPU.)
- 🟢 **AgentOS RIC (8.0):** minimalūs gardai TIK neatšaukiamoms operacijoms (rm -rf/DB drop/force-push/servisų naikinimas); visa kita auto. (S-MMU/CSP multi-agent — atidėta.)
- 🟡 **Parametrinė atmintis / „Frozen Novice" (6.0):** žinoma riba — skill.md=lookup, ne internalizuota; tikras fine-tune reikalauja GPU → ateities kelias.
- ⚪ **AReal/ATDP:** jau Fazėje 3. **Tencent HY3:** atidėta (pigus atsargos modelis, free iki 07-21).
- **Fazė 4 — BAIGTA ✅ (2026-07-07, task a9214ac):**
  - `hera_skills.py` — skill-tuple `(intent,method,difficulty,tool_hint)` + 3-lygių įkėlimas (L1 iter_cards / L2 load_full / L3 load_resources) + `retrieve(task,k)` top-k atranka su pruning (anti lock-in).
  - `hera_optimize.py` (AutoMem #1) — meta-LLM diagnozuoja trajektorijas → siūlo pataisas → `hera_replay.py` validuoja → ACCEPTED į `proposals/approved/` (append-only, GAMYBOS NEKEIČIA — reikia žmogaus promote).
  - `hera_ric.py` — minimalus gardas: blokuoja tik neatšaukiamas katastrofas (rm -rf sist., mkfs/dd, DB drop, force-push, core servisų/vault trynimas); veikia ir kaip PreToolUse, ir kaip API. Blokas → log + Telegram.
  - Self-test: 3 outer-loop pasiūlymai visi replay-PAGERĖJO→ACCEPTED; RIC blokuoja `rm -rf /opt/hera-vault`, praleidžia failo rašymą.
- **⚠️ SVARBU — durabilumas:** VISAS HERA kodas (Fazės 2–4) gyvena TIK VPS'e (`/opt/hera-processor/`, `/opt/hera-ingest/`, kopija `/opt/cad-site-agent/n8n/hera/`). GitHub'e NĖRA (VPS neturi push creds). Rizika = laptopo istorija. Apsaugoti reikia scoped tokeno.
- **⚠️ Patikimumas:** self-improvement sprendimai remiasi Gemini free (flaky, 503) ir subjektyviu LLM verdiktu → `proposals/approved/` laikyti žmogaus-peržiūrimu prieš promote į gamybą (kaip ir pastatyta).

### Fazė 5 — SONA verdiktas + planas (2026-07-07)
- **SONA (Self-Optimizing Neural Architecture) — PRIIMTA dalinai (8.5).** Filosofija „intelektas kilpoje, ne modelyje" = HERA vizija.
- IMAM (be treniravimo): trys laiko kilpos (Loop A per-query / B valandinė klasterizacija+kokybė / C savaitinė konsolidacija), ReasoningBank (kas suveikė → kreipia routing), EWC-lite (svarbos laukas saugo įrodytus skills). Panaudoja jau loginamą `reward` lauką → uždaro kilpą.
- ATIDĖTA (GPU/overkill): LoRA+EWC svorių treniravimas, hiperbolinė (Poincaré) geom., GNN reranking, dinaminis MinCut RuVector. (Embedding-retrieval — nebent lengvas Fazės 4 patobulinimas.)
- **Fazė 5 (statoma, task žemiau):** Loop B (klasterizacija+kokybės balai → silpnų sričių raportas) · Loop C (vault konsolidacija: merge/prune STAGED + concept index) · ReasoningBank (reward-kreipiamas routing) · EWC-lite (importance laukas).
```

# Session Handoff — Rules Modularization

> Šitą failą automatiškai nuskaito SessionStart hook'as ir įkelia į naujos sesijos
> kontekstą (laptopas / web / bet kuris modelis — Kimi, MiMo). Atnaujink jį
> kiekvienos darbo sesijos pabaigoje.

## ⚠️ PIRMENYBĖ — VARTOTOJAS + AUTO-ATMINTIS (2026-07-10)
- **Kas vartotojas:** **AI sistemų dizaineris/orkestruotojas** (diriguoja AI per specs+review; NE rankinis
  koderis; metodas chat-Claude specs → Claude Code vykdo). Fonas: **ArchViz / 3D vizualizacija** (3ds Max/V-Ray,
  ComfyUI, 3D Gaussian Splatting, TouchDesigner) — **NE statybos, niekada nemaišyti.**
  Pilnas asmeninis/strateginis profilis (tikslai, situacija, prioritetai) — TIK privačiame vault'e
  `hera-vault:profile/USER_STRATEGIC_PROFILE.md` (autoritetingas). ⚠️ Šis failas VIEŠAS — jokių asmeninių/
  jautrių detalių čia nerašyti; tik darbinis kontekstas.
- **STANDING RULE — auto-atmintis:** VISADA automatiškai, be atskiro prašymo, persistink į vault kiekvieną naują
  reikšmingą faktą apie vartotoją, tikslus, sprendimus ir sistemos pokyčius. Jam NEREIKIA to prašyti kaskart.
- **Bendravimas:** konkrečiai, be atsiprašymų, be pamokymų kada ilsėtis, be jau žinomo kartojimo. Lietuviškai.
- **Domenas HERA'oje NIEKADA nesiaurinamas** (vartotojo direktyva).

## Būsimų darbų užrašai (neprarasti)
- **Godcoder sandbox (2026-07-11):** iš dev-tools video idėja — leisti sistemai keisti PATS savo kodą
  UŽDAROJE smėlio dėžėje ir testuoti prieš pritaikant. HERA turi outer-loop+replay, bet griežto sandbox NĖRA.
  Vertas, bet RIMTAS (saugumas: sistema keičia savo kodą) — ne skubus, daryti atsargiai su human-gate.
- **HERA naršyklė (2026-07-11, diegiama):** headless Chromium+Playwright VPS'e → HERA gali atsidaryti/naršyti/
  ištraukti/screenshot. Geresnis ingest (JS puslapiai) + žingsnis link „sistema daro darbus". Journey Forge
  (įrašyti vartotojo naršyklės veiksmus→skills) ATIDĖTA — reikia kompiuterio+plėtinio, telefonu neveiks.

## DARBO METODAS — chat-Claude + Claude Code (dual mode)
- **Vartotojo metodas:** chat-Claude = strateginis sluoksnis (vizija, specs, review, kuravimas); Claude Code =
  vykdytojas. Nauja sesija pratęsia BE aiškinimo iš naujo — šitas failas + privatus vault duoda visą kontekstą.
- **Inbox valdymas (kaip užduotys pasiekia VPS):** užduotys rašomos į `inbox/TASK.md` šakoje
  `claude/authorize-claude-code-vps-1dcvrv` → VPS cron runner (kas 2 min, flock, 15-min timeout) → `claude -p`
  vykdo → ataskaita per HERA botą. Darbo eiga: git-worktree add tos šakos → Read TASK.md → Write nauja užduotis
  → commit → push origin → worktree remove/prune. Užduotis: „NEleisk pytest, Telegram trumpai, fail-safe".
- **VISŲ HERA pakeitimų principai (nekintantys):** €0 stack (Gemini free + Groq + GLM, jokio GPU, vienas 4GB VPS);
  fail-safe (klaida → no-op, ne crash); HERA_*=1 jungikliai (default 0); HARD per-LLM timeout 45-60s, NO retry
  (anti rc=124); human-gate VISKAM, NIEKAD auto-merge; git-atšaukiama; domenas NIEKADA nesiaurinamas.
- **Durabilumas:** kodas → PRIVATUS hera-core-backup; vault (skills/growth/profile/proposals/projects) → PRIVATUS
  hera-vault (*/30 sync cron). Viešas cad-site-agent — TIK sanitizuotas operacinis kontekstas.

## BŪSENA 2026-07-11 — savęs-tobulinimas UŽDARYTAS, prasideda pajėgumų plėtra (fazės 6-8)
**GYVA ir įdiegta (visi €0, fail-safe, HERA_*=1, rollback=0):**
- PII valymas (hera_pii); Caveman glaustumas (hera_terse); HERA naršyklė (hera_browser, url fallback JS); LLM-wiki
  grafas+lint (hera_lint, orphan 40→1) + sintezė (hera_synth); botų maršrutas (santrauka→PARSER @tryspagliai_bot
  per PARSER_BOT_TOKEN; HERA botas @tryspagaliai_hera_bot=ataskaitos+per-ingest 🧠 log); sesijų indeksatorius.
- **Savęs-tobulinimo grandinė — VISOS FAZĖS UŽBAIGTOS:**
  1. ✅ Matuoklis (hera_bench, deterministinis, baseline 9/9, NoLiveLLM saugiklis)
  2. ✅ SearXNG €0 paieška (hera_search)
  3. ✅ Research orkestratorius (hera_research: plan→search→fetch→CoVe→synthesize; HARD budget anti-rc124)
  4. ✅ Auto-research vartai GYVI (hera_gate: trigeris→vault-check+research; pass/block/escalate; ACK „🔎 patikrinta")
  5. ✅ Sandbox+savikorekcija: 5a=bubblewrap no-net+worktree izoliacija; 5b=skill-akrecija (hera_accretion);
     5c=siaura bounded savikorekcija (hera_selfedit: whitelist+blacklist, tripwire prieš reward-hacking,
     benchmark-vartai, human-gate, NIEKAD auto-merge). NEGATYVUS testas įrodė tripwire (bypass→REJECT).
- **2 REALŪS human-gate promote ciklai atlikti:** (a) 5b naujas skill `bwrap-agent-isolation` → patvirtintas →
  gyvas; (b) 5c selfedit pataisa tam skill → patvirtinta → gyva; abu benchmark po promote 9/9, jokio rollback.

**KITAS ETAPAS — pajėgumų plėtra (roadmap `hera-vault:docs/ROADMAP.md`, status PROPOSED):**
- **Fazė 6 — Gyvas projektų žurnalas (context retention):** hera_journal.py, `projects/<slug>/STATE.md`
  (NOW/Active/Paused/Next/Decisions/Log/Links), deterministinis branduolys, append-only Log, LLM neprivalomas.
  **⏳ IŠSIŲSTA į inbox 2026-07-11 (commit ce2ea18) — patikrink runner ataskaitą / ar STATE.md sukurtas.**
- **Fazė 7 — Specialist agents + Planning Loop:** Ops/Social/Design agentai; kiekvienas subgoals→draft→
  self-critique (Reflexion-tipo, HARD budget); perpanaudoja council+CoVe; išvestis=draft. Rizika žema-vidutinė.
- **Fazė 8 — Tool Use (AUKŠTA rizika, paskutinė):** Ops=kalendorius+laiškai iš domeno; Social=Instagram publish.
  RĖMAI: default DRAFT/READ-ONLY, human „tvirtinu" prieš siuntimą, recipient/domain allowlist, jokio masinio
  siuntimo, audit log, kredencialai TIK .env. ATVIRI SPRENDIMAI (laukia vartotojo): email provideris
  (SMTP/Zoho/Google), kalendorius (Google/CalDAV), Instagram (reikia IG Business+Meta Graph API+app review — NE
  trivialiai €0), autonomijos lygis (rekomenduojama draft-only startas).

**Produkto vizija (be prekės ženklo — vartotojas pašalino pavadinimą):** autonominis partneris kuris atperka
dėmesį/focus; 3 principai — (1) nuolatinė atmintis+projektų žurnalas, (2) specializuoti agentai su planning loop,
(3) tikri įrankiai/tikri veiksmai. Pilna vizija+profilis: `hera-vault:profile/USER_STRATEGIC_PROFILE.md` (PRIVATU).

**Tyrimų verdiktai:** Godcoder/DGM→per brangu/rizikinga (rink skill-akreciją+siaurą sandbox); €0 stack=SearXNG+
plonas orkestratorius; Shepherd=alfa (statyti savo izoliaciją). **Antigravity:** `agy` v1.1.1 VPS, laukia Google
login. **Atidėta:** Godcoder full self-rewrite, Journey Forge, Codex reviewer (mokamas), router benchmark (5 deferred).

**Atnaujinta:** 2026-07-11
**Rollback SHA (saugus taškas prieš taisykles):** `2fdb3f8`

## Repo struktūros pastaba (svarbu)
- GitHub repo `tryspagaliai-lab/cad-site-agent` turi VISĄ turinį po vienu
  poaplankiu `cad-site-agent/`. Git šaknis yra lygiu aukščiau.
- Claude Code auto-kraunamas `.claude/settings.json` tik iš **repo šaknies**.
  Todėl SessionStart hook'as registruotas šaknyje, o ne `cad-site-agent/.claude/`.

## Kas padaryta (2026-06-16)
Užduotis `rules-modularization-v1` — modulinė rules sistema (MVP slice, tik cad-site-agent).
Merge'inta į `main` (merge commit `7ee7c78`):
- `cad-site-agent/.cursor/rules/cad-cleanup.mdc` — glob-scoped Cursor taisyklė
  (globs: `src/cad_site_agent/**/*.py`, `config/layers.json`).
- `cad-site-agent/src/cad_site_agent/CLAUDE.md` — nested Claude Code scope taisyklės.
- `.claude/hooks/guard_layer_delete.py` (**repo šaknyje**) — PreToolUse layer-delete gardas (STUB).
- `.claude/settings.json` (**repo šaknyje**) — SessionStart + PreToolUse registracijos (auto-kraunasi).
- `.claude/hooks/session-start.sh` (**repo šaknyje**) — repo sync + handoff konteksto įkėlimas.

## Atviri TODO (rytojui)
1. **(DONE 2026-06-17)** `config/layers.json` sukurtas — generuotas iš
   `export_layers.yaml` (12 output sluoksnių) + `semantic_taxonomy.yaml` (43 klasės)
   = **55 stabilūs sluoksniai**. RADINYS: spec'o „47" NEATITINKA realios schemos;
   failas atspindi tikrą schemą (regeneruoti po schemos pakeitimų).
2. **(DONE 2026-06-17)** `guard_layer_delete.py` logika užbaigta — aptinka
   delete/merge/purge, ištraukia taikinio sluoksnį, BLOKUOJA (exit 2) stabilaus
   sluoksnio naikinimą, fail-open jei schema/sluoksnis neaiškus. Ištestuota 5 scenarijais.
3. **Layer „esmės" testavimas** — pagrindinis tikslas: kad sistema suvoktų sluoksnių
   prasmę. Tam skirti `tests/` (test_analyzer, test_classifier, test_taxonomy,
   test_hatch ir kt.). Baseline: **202 passed, 8 skipped** (skip = trūkstami DXF fixture'ai).
4. **(DONE 2026-06-16)** Layer-guard perkeltas į repo šaknies `.claude/` ir
   registruotas šaknies `settings.json` → dabar auto-kraunasi desktop'e.
5. **`agentos-sessions` branduolys (`AGENTS.md`) + `~/.claude/CLAUDE.md`** — ne šios
   sesijos apimtyje (GitHub scope tik cad-site-agent). Padaryti iš laptopo vietoje.

## Aplinkos FAKTAS (2026-07-02, iš vartotojo — įsiminti!)
- Atskirų „desktop" kompiuterių NĖRA. Vienintelė fizinė mašina — **LAPTOPAS su LINUX**
  (NE Windows! Ankstesnė Windows prielaida buvo klaidinga — seni Windows/E:/ keliai pasenę).
  Projektų raw data yra laptope — tikslūs keliai nežinomi, ieškoti per `find ~`. Naudojamas **VPS**.
- Koordinacijos rolė `desktop` pervadinta į `local` (žr. docs/COORDINATION.md).
- Laptopo paleidimas: `bash cad-site-agent/scripts/bootstrap_local.sh` (Linux).

## Testavimo planas
```bash
cd cad-site-agent
python -m pytest tests/ -v        # pilnas rinkinys
python -m pytest tests/test_classifier.py tests/test_taxonomy.py -v  # sluoksnių/klasifikacijos logika
```

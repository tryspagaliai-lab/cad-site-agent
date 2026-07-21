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
- **Fazė 6 — Gyvas projektų žurnalas (context retention): ✅ ĮDIEGTA 2026-07-12** (hera-core-backup commit
  97e915c). hera_journal.py, `projects/<slug>/STATE.md` (NOW/Active/Paused/Next/Decisions/Log/Links),
  deterministinis branduolys (be LLM), append-only Log+Decisions, LLM distill_next neprivalomas (45s timeout).
  HERA_JOURNAL=1 (def 0). Demo „hera-system" projektas gyvas; dispatcher hook_ingest→## Log po kiekvieno ingesto.
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

## BŪSENA 2026-07-18 — faithfulness + eval GYVI; laukia curation backlog
> Ši skiltis PAKEIČIA 07-11 būseną. Nauja sesija: pratęsk nuo čia. Visi €0, fail-safe, anti-rc124, human-gate.

**Naujos GYVOS fazės (po 07-11):**
- **Memora atmintis GYVA** (HERA_MEMORA=1): index (primary_abstraction+cue_anchors) + policy-guided multi-hop retriever.
- **GPU auto-filer GYVAS** (HERA_GPUFILTER=1): GPU/self-hosting turinys auto→future-gpu (FUTURE_GPU.md, `hardware: future-gpu`).
- **Fazė 5d** rejected-edit buferis; **7a planner** (hera_planner, def 0); **7b specialist agents** (hera_agents:
  deterministinis factory router + SocialSpecialist=juodraščiai→proposals/social/, JOKIO postinimo; Ops/Design=stubai
  laukia Fazės 8; def 0, bench 22/22).
- **Fazė 11+11d eval-vartai** (hera_eval: Tier A determ. + Tier B LLM-judge advisory PRIEŠ self-edit promociją;
  **held-out golden split** ref/holdout + **overfitting-flag** ref↑holdout-flat→žmogui; def 0, bench 25/25).
- **Fazė 12/12b/12c faithfulness vartas GYVAS** (HERA_FAITHFULNESS=1): parse↔šaltinis grounding (atomai vs verbatim;
  yt/url source_text 68/68); advisory, `suspect`→HERA botas, NIEKAD neblokuoja; pravalytas md-triukšmas (0.847→0.971;
  bench 14/14). Šakninė pataisa: _PROPER_RE LT-didžiųjų bug'as.
- Naujienų digest dedup PATAISYTAS (seen.jsonl). Search praplėsta: CN/JP/KR labs + TLDR.

**KURAVIMO PRINCIPAS (vartotojas 2026-07-18):** „imam TIK tai, kas stiprina sistemą Į PRIEKĮ — stiprinam sistemą."
Kiekvieną ingestą vertinti pro šį filtrą. Marketingą/dublius/nepatvirtintus žymėti, necituoti. Faithfulness suspect →
atskirti realius neatitikimus nuo vertimo/terminų triukšmo (dažnai suspect = triukšmas, ne haliucinacija).

**cad-3d KRYPTIS (vartotojo ArchViz/3D niša — NE statybos):** FUTURE_GPU.md turi GIFT (MIT/IBM: VLM 2D→CAD-kodas→3D,
near-misses+inference-time budget; GPU→future) + 2D→3D. Plėtros vektorius cad-site-agent'ui (dabar 2D DXF→semantika).
Self-improvement principas (near-misses+biudžetas) IŠORIŠKAI validuotas (GIFT, Forget-Loop, SkillOpt); BET AI2/UW
tyrimas (guardrail 6xlz70) įspėja: harness self-optimizacija overfitting'a → held-out eval + test-time scaling.

**Artifacts KOKYBEI:** naudojami sistemos kokybei kai gerina (NE darbo paieškai). Yra PRIVATUS curation-review
dashboard (staged+prune+faithfulness balai). Vault duomenys PRIVATŪS — nesidalinama.

**⏳ LAUKIA HUMAN-GATE (backlog — naujos sesijos prioritetas):**
- **42 staged prune** (superseded→distiliuoti į skills; C01-C32 saugūs; `gdx0fm`+`lto8bb`=HOLD epistminės vėliavos).
- **~8 staged ingestai:** promote rekom.: Hermes lygiagretūs įrankiai (9.0), H-JEPA/GeoWorld, kognityvinis organiz.,
  Copycat (science-checked); priimti: Claude platforma; MERGE dublį: sistemų-dinamika `zo9qtf`↔MIT; Artifacts=priimti
  +šaltinio vėliava (marketingas). `93ell3` jau=bazinė ref (dublis).
- **🔴 NAUJAS sel 9.0 promote_candidate (07-18): „Statybinių brėžinių apdorojimo efektyvumas su AI"** — TIESIOGIAI
  cad-site-agent drawing-processing domenas; AUKŠČIAUSIAS peržiūros prioritetas (dar neįvertinta).
- Loop B stabilus: 54 skills·68 growth·74 RB; wiki dangling 12 (kyla — verta pravalyti); atviri klausimai 11.

**Atnaujinta:** 2026-07-18

## BŪSENA 2026-07-21 — multi-bot digest (4 temos) GYVAS; vault sync užgrūdintas
> Ši skiltis PAKEIČIA 07-18 būseną. Nauja sesija: pratęsk nuo ČIA (naujausia). Visi €0, fail-safe, anti-rc124, human-gate.

**Multi-bot Telegram digest — 4 TEMINIAI botai GYVI** (kiekvienas = „AI EKSPLOATAVIMO METODAI" savo srityje, NE
bendros naujienos; kiekvienam įrašui 2–3 sakiniai „Kas tai" + „Kur panaudoti", usage pakreiptas į vartotojo kontekstą):
- **AI news** (esamas) — bendri AI leidimai/metodai.
- **Design** — dizaino/vizualizacijos AI įrankiai ir metodai.
- **Ūkininkas / @ARTOJAS_BOT** — žemės ūkio AI (Semantic Scholar backbone; EU+Azijos+Ispanijos/Singapūro/Korėjos tyrimai).
- **@AI_HOWTO_BOT (`aitech` tema)** — praktinis AI how-to (agentai, RAG, tool use, MCP, workflow'ai).
- Architektūra: `ai_digest.py` topic-aware `TOPICS` dict (per-topic feeds/hf_orgs/github_atom/arxiv_cats/filter_kw/
  seen/token/label; per-topic try/except; per-topic seen.jsonl dedup). Cron 08:00 Vilnius.

**Digest v3 — pataisos + praplėtimas:**
- Delivery fix: PILNAS numeruotas sąrašas, split į ≤3800 ženklų žinutes (buvo: Gemini kondensuodavo į TOP-3).
- Noise fix: HF per-org `?author=` release backbone (global createdAt = triukšmas, pašalintas) + `is_noise()` filtras
  (gguf/awq/probe/ppo…); +7 flagship orgs. GitHub `.atom` feed'ai (keyless), Semantic Scholar bulk (keyless),
  arXiv, OpenAlex (nuo 2026-02 reikia FREE key — gated per OPENALEX_KEY), browser User-Agent Cloudflare feed'ams.
- Nauji feed'ai: `aimodels.substack.com/feed` (ai tema), `tldr.tech/api/rss/design` (design tema).

**cad-3d žinių kaupimas (vault, domain cad-3d):**
- **3ds Max MCP serveriai** — cl0nazepamm/loonghao/317431629; DESKTOP-FUTURE (reikia Windows+Max mašinos).
- **AutoCAD MCP serveriai** — U-C4N/autocad-mcp ⭐ = dual-engine, **ezdxf HEADLESS ant Linux → TIESIOGINĖ sinergija su
  cad-site-agent (irgi ezdxf) DABAR, €0, ne desktop-future**; + puran-water/daobataotie/AnCode666.

**Model policy (patvirtinta):** VPS runner pinnintas prie **Sonnet 5** (nebedegina bendros Claude prenumeratos quota);
orchestrator/planner = Fable 5 / Opus 4.8; grunt work = Gemini/Groq/GLM (€0).

**Infra fix (2026-07-21):** `hera_vault_sync.sh` push'ino BE `pull --rebase` → po tiesioginių orchestratoriaus push'ų
VPS vault push'ai kaubdavosi (buvo 40 nepush'intų commit'ų, remote atsiliko nuo 07-20 15:30). SUTVARKYTA: rankinis
rebase+push atkūrė viską į remote, + skriptas užgrūdintas (`git pull --rebase -X theirs` prieš push, su rebase-abort
saugikliu) ir patikrintas gyvai (PUSH OK). Runner „nukritęs" aliarmas buvo klaidingas (cloud konteinerio laikrodis).

**Atnaujinta:** 2026-07-21

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

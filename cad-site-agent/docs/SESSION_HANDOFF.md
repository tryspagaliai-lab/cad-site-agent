# Session Handoff — Rules Modularization

> Šitą failą automatiškai nuskaito SessionStart hook'as ir įkelia į naujos sesijos
> kontekstą (laptopas / web / bet kuris modelis — Kimi, MiMo). Atnaujink jį
> kiekvienos darbo sesijos pabaigoje.

## ⚠️ PIRMENYBĖ — VARTOTOJAS + AUTO-ATMINTIS (2026-07-10)
- **Kas vartotojas:** alias `cs`, London/Lietuva. **AI sistemų dizaineris/orkestruotojas**
  (diriguoja AI per specs+review; NE rankinis koderis; metodas chat-Claude specs → Claude Code vykdo).
  Fonas: **ArchViz / 3D vizualizacija** (3ds Max/V-Ray, ComfyUI, 3D Gaussian Splatting, TouchDesigner) —
  **NE statybos, niekada nemaišyti.** Netekęs darbo, ieško London creative-tech/AI-automation; HERA jam =
  **portfolio darbas + kelias į pajamas.** Pilnas strateginis profilis: privatus vault
  `hera-vault:profile/USER_STRATEGIC_PROFILE.md` (autoritetingas, viršesnis už auto PROFILE.md).
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

## BŪSENA 2026-07-11 (vėlus vakaras) — savęs-tobulinimo + auto-research statyba
**Įdiegta ir GYVA (visi €0, fail-safe, HERA_*=1 jungikliai, rollback=0):**
- PII valymas (hera_pii, Rampart) prieš išorinius modelius; Caveman glaustumas (hera_terse); HERA naršyklė
  (hera_browser, url fallback JS puslapiams); LLM-wiki: nuorodų grafas+lint (hera_lint, orphan 40→1) +
  sintezė→puslapis (hera_synth); botų maršrutas (santrauka→PARSER @tryspagliai_bot per PARSER_BOT_TOKEN;
  HERA botas @tryspagaliai_hera_bot=ataskaitos+per-ingest 🧠 log); sesijų indeksatorius (sessions/index.jsonl).
- **Savęs-tobulinimo/auto-research planas — fazės:**
  1. ✅ Matuoklis (hera_bench, held-out, deterministinis, baseline pass_rate 1.0=9/9, NoLiveLLM saugiklis)
  2. ✅ SearXNG €0 paieška (Docker localhost:8888, JSON, hera_search.py)
  3. ✅ Research orkestratorius (hera_research: plan→search→fetch→CoVe→synthesize; HARD budget/timeout anti-rc124)
  4. ✅ Auto-research saugiklis GYVAS (hera_gate: trigeris promote/high-skill/nesutarimas → vault-check + research;
     decision pass/block/escalate; ACK praturtintas „🔎 patikrinta: supported 0.X"; escalate→OPEN_QUESTIONS)
  5. 🔨 Sandbox (5a=bubblewrap no-net+git-worktree izoliacija BE savęs-keitimo; 5b=skill-kaupimo kilpa;
     5c=siaura prompt/skill savikorekcija). PRIVALOMI saugikliai: no-net sandbox, rašymas tik skills/,
     benchmark-be-regreso vartai, human-gate, git-atšaukiama, RIC guard, tripwires.
**Tyrimų verdiktai (gilios paieškos):** Godcoder/DGM→per brangu/rizikinga, rink skill-akreciją+siaurą sandbox;
Karpathy llm-council=deliberacija (ne verifikacija), LLM-wiki=contradiction-check; €0 stack=SearXNG+plonas
orkestratorius (ne sunkūs karkasai); Shepherd=alfa, tik atšaukiamas pėdsakas (NE reali izoliacija)→statyti savo.
**Antigravity:** `agy` v1.1.1 įdiegtas VPS, laukia vartotojo Google login (`agy` Termius'e) — testui, ne diegimui.
**Nebaigta/atidėta:** Godcoder full self-rewrite (praleista), Journey Forge (atidėta), Codex reviewer (pristabdyta,
mokamas), router LLM benchmark atvejai (5 deferred).

**Atnaujinta:** 2026-06-16
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
  (NE Windows! Ankstesnė Windows prielaida buvo klaidinga — ji kilo iš seno
  užduoties failo su `C:\Users\zilva\...` keliu; tie Windows/E:/ keliai pasenę).
  H7149 Osprey Heights raw data yra laptope — tikslus kelias nežinomas, ieškoti
  per `find ~ -iname "*osprey*"`. Ateityje galimas **VPS**.
- Koordinacijos rolė `desktop` pervadinta į `local` (žr. docs/COORDINATION.md).
- Laptopo paleidimas: `bash cad-site-agent/scripts/bootstrap_local.sh` (Linux).

## Testavimo planas
```bash
cd cad-site-agent
python -m pytest tests/ -v        # pilnas rinkinys
python -m pytest tests/test_classifier.py tests/test_taxonomy.py -v  # sluoksnių/klasifikacijos logika
```

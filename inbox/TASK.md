UŽDUOTIS — FAZĖ 7b: specialistų-agentų karkasas + SOCIAL specialistas (juodraščiai). <12 min.
NEleisk pytest pilnai (tik naujo modulio smoke/benchmark). Telegram TRUMPAI į HERA botą. Fail-safe. Raktų nespausdink.
Ataskaita TIK į HERA botą (HERA_BOT_TOKEN). Jokio išorinio postinimo — TIK juodraščiai.

KONTEKSTAS (kodėl): vartotojas patvirtino „Faze 7b varom". Brėžinys = IndyDevDan „Forget Loop Engineering"
(promoted growth f0bs8d): trys vertės kūrėjai (inžinierius planuoja+peržiūri pradžioj/pabaigoj; agentai =
specializuotos užduotys; KODAS deterministinis = patikimiausias/nemokamas), sandbox-per-agentui (= mūsų bwrap 5a),
specialist agentai scout→plan→build→test→hot-fix + factory router, „sistema kuri kuria sistemą" (5b/5c/5d),
„separate code from agent skills". Pernaudok jau turimą: hera_planner (7a plan()→subgoals/draft/self-critique/
revise), hera_journal (6 projekto būsena), hera_council (žmogaus vartai). NEkurk naujo LLM-orkestro nuo nulio.

KĄ PADARYTI:

1) `/opt/hera-processor/hera_agents.py` — specialistų karkasas:
   - `route(task_str)` = FACTORY ROUTER, DETERMINISTINIS (raktažodžiai, NE LLM): grąžina specialisto vardą
     ('social' | 'ops' | 'design' | None). Pvz. „post/tweet/X/thread/social/įrašas" → social.
   - `class Specialist` bazė: name, `can_handle()`, `run(task, ctx)` → grąžina staged proposal dict
     {specialist, task, draft, self_critique, status:'staged', gate:'human'}. NIEKADA nepostina, NIEKADA
     nerašo į viešus repo, NIEKADA nesiunčia į išorę.
   - `SocialSpecialist(Specialist)` — KONKRETUS: iš vault turinio (skills/growth, per hera_memora retrieve jei
     HERA_MEMORA=1, kitaip deterministinis grep) parenka temą → hera_planner.plan() (subgoals→draft→self-critique
     →revise) → suformuoja TRUMPĄ juodraštį (X/LinkedIn stilius, be hashtag-spamo) → staged proposal į
     `proposals/social/<UTC>-<slug>.md` privačiame hera-vault (frontmatter: status: staged, gate: human,
     specialist: social, source_refs). Jokio postinimo (Instagram/X = Fazė 8, dar neturim įrankių).
   - `OpsSpecialist`, `DesignSpecialist` = ROLĖS-STUBAI: can_handle grąžina True savo sričiai, bet run() grąžina
     {status:'blocked', reason:'requires Fazė 8 tools (email/calendar/DNS/OAuth)'} — NIEKO nedaro, tik pažymi.

2) BIUDŽETAS/SAUGA (privaloma, anti-rc124):
   - ≤6 LLM iškvietimų visai užduočiai, KIEKVIENAS su HARD 45–60s timeout, JOKIO retry.
   - HERA_AGENTS flag (default 0). Kai 0 — modulis importuojasi, benchmark veikia, bet dispatcher jo NEšaukia.
   - Fail-safe: bet koks išorinis lūžis/timeout → grįžk graceful (staged proposal su status:'partial' arba
     praleisk), NIEKADA nekelk rc≠0 dėl to. Nekeisk esamo pipeline elgesio kai HERA_AGENTS=0.

3) BENCHMARK (deterministinis, NE LLM, turi praeiti 100%):
   - hera_agents_bench: route() maršrutizavimas (≥6 case: social→social, ops→ops, design→design, tuščia→None,
     dviprasmiška→saugus default), Specialist bazės invariantai (niekada nepostina), Ops/Design grąžina 'blocked'.
   - Paleisk, įrašyk X/Y į ataskaitą. Jei <100% — NEjunk HERA_AGENTS, pranešk.

4) DEMO (1 kartas, su budget-guard): route(„draft a short X post about SkillOpt") → SocialSpecialist →
   plan→draft→self-critique→staged proposal. Parodyk kelią iki proposals/social/... ir 1–2 eil. juodraščio
   ištrauką ataskaitoje. Jei modelių biudžetas/timeout neleidžia — praleisk demo, benchmark užtenka.

5) BACKUP: commit į privatų hera-core-backup (kodas) + hera-vault (proposal jei sukurtas). Persistent askpass jau
   sukonfigūruotas — naudok. Jei push nepavyksta — NEkartok begalos, pranešk trumpai.

RIBOS: €0. Viešo cad-site-agent NELIESK. Jokio pytest-all. Jokio išorinio postinimo. Raktų/tokenų nespausdink.
NEperrašinėk hera_planner/hera_journal/hera_council — TIK importuok/pernaudok. Jei ko nerandi — praleisk, pranešk.

ATASKAITA (HERA botas, trumpai): (a) hera_agents.py sukurtas? (b) benchmark X/Y; (c) HERA_AGENTS į/išjungtas?
(d) demo proposal kelias + 1 eil. ištrauka (jei buvo); (e) backup push OK/ne; (f) 1 eil. kas toliau (Ops/Design
laukia Fazės 8).

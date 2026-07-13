UŽDUOTIS — FAZĖ 11: eval-vartai prieš self-edit (kokybės regresijos gaudymas). <14 min.
NEleisk pytest pilnai (tik naujo modulio smoke/benchmark). Telegram TRUMPAI į HERA botą. Fail-safe. Raktų nespausdink.
Ataskaita TIK į HERA botą (HERA_BOT_TOKEN). €0. Privatūs repo. Viešo cad-site-agent NELIESK.

KONTEKSTAS (kodėl): giluminė paieška (28 šaltiniai, 22/25 teiginių patvirtinti adversariškai) parinko šitą kaip
#1 sveretą enterprise-link be Fazės 8. Idėja: self-edit (5c/5d) šiandien remiasi TIK human-gate. Pridedam AUTOMATINĮ
kokybės-regresijos vartą PRIEŠ promociją — jei pakeitimas pablogina RAG/ekstrakcijos kokybę, testas krenta pirmiau
nei žmogus spaudžia gate. Tai SUSTIPRINA human-gate, NEpakeičia jo. Deterministinis-core: didžioji dalis vartų —
be LLM (nemokama, greita); LLM-teisėjas tik kaip advisory balas su griežtu biudžetu.

SVARBU DĖL FOOTPRINT (4GB, be GPU): NEnaudok jokio įrankio kuris kelia LOKALŲ modelį (jokio sentence-transformers,
jokio lokalaus NLI/embedding modelio, jokio spaCy dideliam). Metrikoms naudok TIK LLM-teisėją (Gemini/Groq/GLM
taryba per esamą klientą) ARBA deterministinius patikrinimus. DeepEval/promptfoo yra orkestratoriai (be GPU) — jei
imi DeepEval, imk TIK G-Eval / judge-based metrikas, VENK metrikų kurios krauna lokalų embedding modelį. Jei abejoji —
rašyk savo ploną judge-wrapper aplink esamą tarybą, be naujų sunkių priklausomybių.

KĄ PADARYTI:

1) `/opt/hera-processor/hera_eval.py` — dviejų pakopų eval-vartas:
   - GOLDEN SET: mažas `eval/golden_set.jsonl` privačiame hera-vault — 5–8 reprezentatyvūs atvejai
     {query, expected_gist, source_ref}. Jei nėra — sukurk iš esamų skills/growth (deterministiškai, be LLM).
   - PAKOPA A (VISADA, be LLM, nemokama) — deterministiniai regresijos patikrinimai: (i) pipeline grąžina output
     (ne crash), (ii) retrieval grąžina ≥k rezultatų golden query'iams, (iii) output pereina esamą hera_lint/schema,
     (iv) nėra tuščių/NaN laukų. Tai PRIVALOMAS vartas (hard fail → NEpromote).
   - PAKOPA B (BIUDŽETU ribota, LLM-teisėjas) — 3–8 golden atvejai vertinami faithfulness/answer-relevancy per
     tarybą (G-Eval stiliaus, be lokalaus modelio). Grąžina balą 0–1 + baseline slenkstį. Tai ADVISORY (ne hard) —
     balas iškeliamas prie human-gate, kad žmogus matytų regresiją.
   - `run_eval(before, after) -> {tierA_pass: bool, tierB_score: float|None, verdict: 'pass'|'regress'|'inconclusive',
     details}`. Baseline saugomas `eval/baseline.json` vault'e (atnaujinamas TIK po sėkmingo human-gate promote).

2) INTEGRACIJA su self-edit (5c/5d): PRIEŠ staginant promociją — iškviesk hera_eval.run_eval(). 
   - tierA hard-fail → proposal pažymim `eval: FAIL (tierA)`, NEauto-promote, iškeliam prie human-gate raudonai.
   - tierB regress (balas < baseline − delta) → `eval: REGRESS (score X vs base Y)`, iškeliam žmogui, bet NEblokuok
     (advisory). tierA pass + tierB ok → `eval: PASS`.
   - Žmogus visada turi galutinį gate. Eval TIK informuoja/blokuoja auto-kelią, žmogaus sprendimo nepakeičia.

3) BIUDŽETAS/SAUGA (privaloma, anti-rc124):
   - Pakopa B ≤6 LLM iškvietimų visai eval sesijai, KIEKVIENAS HARD 45–60s timeout, JOKIO retry.
   - HERA_EVAL flag (default 0). Kai 0 — self-edit elgiasi kaip dabar (jokio vartų kvietimo), modulis tik importuojasi.
   - Fail-safe: bet koks eval lūžis/timeout → verdict='inconclusive' → NEblokuok promociją, tik pažymėk žmogui.
     NIEKADA nekelk rc≠0 dėl eval. Nekeisk esamo pipeline elgesio kai HERA_EVAL=0.

4) BENCHMARK (deterministinis, NE LLM, turi praeiti 100%):
   - hera_eval_bench: golden_set pasikrauna, Pakopa A logika (pass/fail teisingai), vartų sprendimo lentelė
     (tierA fail→FAIL, tierB regress→REGRESS advisory, ok→PASS), fail-safe (mesta klaida→inconclusive, ne blokas),
     HERA_EVAL=0 → self-edit nepaliestas. Įrašyk X/Y. Jei <100% — NEjunk HERA_EVAL, pranešk.

5) ROADMAP į vault (deterministiškai, be LLM): įrašyk/atnaujink hera-vault `docs/ROADMAP.md` — pridėk skiltį
   „Enterprise sluoksniai (€0, be Fazės 8) — deep-research 2026-07-13":
   Tier1: (11) eval-vartai=promptfoo/DeepEval [ŠI FAZĖ], Presidio PII-redakcija; Tier2: GPTCache semantinis cache
   (pin v0.1.44), LightRAG+GLiNER-Relex graph-RAG; Tier3: Arize Phoenix tracing (RAM rizika 4GB — tik offline batch).
   NE: Langfuse v3 (ClickHouse 8GiB); Infisical→vietoj sops+age. Spraga (nepatvirtinta): SRE-patterns, guardrails,
   prompt-versijos/A-B, CI-CD — atskiram gilinimuisi. (Tik faktai, be raktų.)

6) BACKUP: commit į privatų hera-core-backup (kodas) + hera-vault (golden_set/baseline/ROADMAP). Persistent askpass
   jau sukonfigūruotas. Jei push nepavyksta — NEkartok begalos, pranešk trumpai.

RIBOS: €0. Jokių GPU/lokalių modelių. Jokio pytest-all. Viešo NELIESK. NEperrašinėk hera_selfedit/hera_council/
hera_planner — TIK importuok/integruok. Jei ko nerandi — praleisk, pranešk.

ATASKAITA (HERA botas, trumpai): (a) hera_eval.py sukurtas? (b) golden_set N atvejų; (c) benchmark X/Y;
(d) HERA_EVAL į/išjungtas? (e) integracija su self-edit OK (advisory, human-gate nepakeistas)? (f) ROADMAP.md
atnaujintas? (g) backup push OK/ne; (h) 1 eil. kas toliau (Tier1 Presidio PII).

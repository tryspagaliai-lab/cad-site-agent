UŽDUOTIS — FAZĖ 11d: (A) promote Harness-tyrimo natą kaip forward-guardrail + (B) held-out eval sustiprinimas. <14 min.
NEleisk pytest pilnai (tik hera_eval --bench). Telegram TRUMPAI į HERA botą. Fail-safe. €0. Raktų nespausdink.
Ataskaita TIK į HERA botą. Privatūs repo. Viešo cad-site-agent NELIESK.

KONTEKSTAS (kodėl): AI2/UW tyrimas (growth 6xlz70) parodė: automatinė Harness self-optimizacija overfitting'a benchmark'ui,
neguneralizuoja; test-time scaling (parallel sampling 72.3%) lenkia Harness evoliuciją (67.4% < bazinis 68.2%). Pamoka
NE „mesti self-edit", o STIPRINTI: (1) held-out vertinimas (nevertink self-edit ant to, ką jis optimizuoja), (2) test-time
scaling > agresyvus self-mod, (3) human-gate validuotas, (4) finalization-gate + debugger/progresyvus-atskleidimas
pattern'ai. Vartotojo principas: imam TIK tai, kas stiprina sistemą Į PRIEKĮ. Šitas praeina — kaip guardrail + eval pataisa.

=== DALIS A: promote 6xlz70 kaip forward-guardrail nata ===
1) growth/2026-07-16-...6xlz70.md → antraštėje: „STATUS: PROMOTED 2026-07-16 (human-gate: vartotojas) — dizaino guardrail".
2) Pridėk „Kuravimo pastaba (forward-strengthening)":
   - „Imam kaip APSAUGĄ, ne kritiką. Pamokos HERA'ai: (1) HELD-OUT eval — nevertink self-edit (5c/5d) ant tų pačių
     užduočių, kurias jis optimizuoja (overfitting rizika); (2) test-time scaling / daugiau lygiagrečių bandymų >
     agresyvus harness self-mod (patvirtina biudžeto-compute liniją, „parallel terraced scan"); (3) human-gate
     VALIDUOTAS (be žmogaus intelekto meta-agento self-mod ≈ 0 pagerėjimas); (4) perimtini: finalization-gate (netikrink
     'baigta' kol nepatikrinti rezultatai/failai/testai) + agent-debugger su progresyviu atskleidimu (skill jau turim)."
   - Sąsajos (wiki): self-edit (5c/5d), eval-vartai (Fazė 11), human-gate, `[[progresyvus-konteksto-atskleidimas-llm]]`.
   - Šaltinis: YouTube paaiškinimas AI2/UW straipsnio (2026-07-14); ne pats straipsnis. Faithfulness ~0.7 (triukšmas).

=== DALIS B: hera_eval held-out sustiprinimas (Fazė 11) ===
3) hera_eval.py: golden_set padalink į DVI disjunktiškas dalis:
   - `ref` (gali informuoti baseline/tuning) ir `holdout` (NIEKADA nenaudojama tuninimui — TIK generalizacijos matas).
   - run_eval grąžina abu: holdout balas = TIKRAS generalizacijos signalas.
   - **OVERFITTING flag** (tyrimo esmė): jei ref-balas kyla, o holdout-balas NEkyla (skirtumas > delta) → verdict
     pažymi „⚠️ overfitting: ref↑ holdout→flat" ir iškelia žmogui (advisory). Tai self-edit'o sąžiningumo vartas.
   - Jei golden_set per mažas padalinti — pridėk kelis held-out atvejus deterministiškai iš esamų skills/growth (be LLM),
     arba pažymėk holdout kaip „sėkla, plėsti". NElauk tinklo, nenaudok model-call.
   - HERA_EVAL lieka default 0 (dormant — tik korektiškesnis prieš įjungiant). NEkeisk gyvo pipeline elgesio.
4) BENCHMARK: hera_eval --bench turi likti 100% + pridėk atvejus: ref/holdout split kraunasi, overfitting-flag logika
   (ref↑holdout-flat→flag; abu↑→ok; abu-flat→ok). Įrašyk X/Y. <100% → NEkeisk numatytų, pranešk.

=== BENDRA ===
5) BACKUP: commit hera-core-backup (kodas) + hera-vault (nata). Persistent askpass yra. Push nepavyko → NEkartok, pranešk.
RIBOS: €0. Jokių lokalių/GPU modelių/tinklo. Jokio pytest-all. Anti-rc124: deterministiška. NEperrašinėk
hera_selfedit/council — tik hera_eval + nata. Viešo NELIESK.

ATASKAITA (HERA botas, trumpai): (a) 6xlz70 promoted kaip guardrail (pamokos+sąsajos)? (b) held-out split įdiegtas +
overfitting-flag? (c) bench X/Y; (d) HERA_EVAL lieka 0? (e) backup push OK/ne; (f) 1 eil. kas toliau.

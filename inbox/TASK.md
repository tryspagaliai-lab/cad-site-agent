UŽDUOTIS — ai_digest v3: praplėsti santrauką (2-3 sak.) + pridėti PANAUDOJIMO aprašą. <12 min.
NEleisk pytest. Fail-safe. €0. Raktų nespausdink. Ataskaita TIK į HERA botą. Maršruto NEKEISK (@tryspagaliabot).
ANTI-RC124: Gemini HARD 45-50s, JOKIO retry; Telegram siuntimas kaip dabar (HARD 15s/žinutė).

KONTEKSTAS: v2 (`beb33fa`) veikia — filtras + 1-eil santrauka. Vartotojas nori PLAČIAU: išplėsta ataskaita +
panaudojimo aprašas. NElisk filtro/pristatymo-skaidymo/seen logikos (jau gera) — TIK santraukos formatą.

KEIČIAMA TIK `summarize_entries()` (Gemini batch) prompt + formatavimas:

1) Per įrašą Gemini grąžina (JSON, batch — 1 call visiems, kaip dabar):
   - `category` (kaip dabar: Modelis/Tyrimas/Irankis-Agentas/Laboratorija/Kita)
   - `kas_tai`: **2-3 sakiniai** (ne 1) — kas tai per modelis/įrankis/tyrimas, kuo išsiskiria, dydis/gebėjimai.
   - `kur_panaudoti`: **praktinis panaudojimas, tilt į vartotojo kontekstą** — „kaip TU galėtum tai išnaudoti":
     AI sistemos / automatizacija (n8n-tipo) / agentai / RAG / 3D-dizainas / ArchViz. Konkrečiai, ne bendrai
     („gali būti naudinga X"). Jei įrašas nesusijęs su tomis sritimis — sąžiningai „mažai pritaikoma tavo darbui".

2) FORMATAS (per įrašą):
   **N. pavadinimas**
   [Lab: X] · kategorija
   **Kas tai:** 2-3 sak.
   **Kur panaudoti:** 1-2 sak. (tavo kontekstas)
   🔗 URL

3) BIUDŽETAS/SAUGA: 1 BATCH Gemini call (flash, thinkingBudget=0, responseMimeType=JSON, HARD 45-50s, NO retry).
   Daugiau teksto per įrašą → jei įrašų daug (>15), riboti SUMM_MAX arba skaidyti batch į 2 call'us (kad neviršytų
   timeout). Klaida/timeout → fallback bare įrašas (pavadinimas+šaltinis+URL), NIEKADA rc≠0. Skaidymas į ≤3800 sim.
   žinutes lieka (dabar įrašai ilgesni — chunker turi teisingai skaidyti, nė vieno neprarasti).

4) VERIFIKACIJA: dry-run (1-2 įrašai su nauju formatu) + VIENAS test-send į @tryspagaliabot (žyma „🧪 TESTAS v3 —
   praplėsta + panaudojimas"). seen NEkeisk dėl testo.

5) BACKUP: commit ai_digest.py → hera-core-backup. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Maršrutas nekeičiamas. Jokio pytest-all. Anti-rc124. NElisk filtro/skaidymo/seen — TIK summarize formatą.

ATASKAITA (HERA botas, trumpai): (a) santrauka praplėsta (2-3 sak.) + panaudojimo aprašas pridėtas? (b) batch Gemini
budget OK (kiek call'ų, timeout laikosi)? (c) test-send v3 pavyzdys (1 įrašas su nauju formatu)? (d) fallback veikia?
(e) backup push OK/ne; (f) 1 eil. kas toliau.

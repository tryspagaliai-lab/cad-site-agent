UŽDUOTIS — FAZĖ 9b: Memora policy-guided retriever (skaitymo pusė). <16 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Vault -> PRIVATUS hera-vault. Viešo NELIESK.
SAUGUMAS: raktų nespausdink/necommit'ink.

KONTEKSTAS: Fazė 9a pastatė memory_index.jsonl (primary_abstraction + cue_anchors). Dabar 9b = paieška virš jo.
KRITINIS €0/rc124 apribojimas: iteratyvi paieška = keli LLM kvietimai → BŪTINAS HARD budget cap. Branduolys
DETERMINISTINIS (multi-hop per cue_anchors BE LLM); LLM tik neprivalomas plonas query-refinement su griežtu cap.
NE RL-distilled (=GPU). Hand-prompted tik jei reikia.

SUKURK/PRAPLĖSK hera_memora.py: retrieve(query, max_hops=2, max_llm=2) -> ranked įrašai + kaip rasti (cue-path).
1) DETERMINISTINIS branduolys (BE LLM):
   - Match query terminus prieš primary_abstraction + cue_anchors (keyword/BM25-stiliaus, case-insensitive).
   - MULTI-HOP: iš pradinio pataikymo EIK per cue_anchors (bounded gylis <=max_hops=2) — surask related-but-not-
     similar įrašus (Memora esmė). Grąžink su nuoroda kuris cue-path atvedė.
   - Deduplikuok, rank pagal match stiprumą + hop atstumą.
2) NEPRIVALOMAS LLM query-refinement (fail-safe, griežtai bounded): jei HERA_MEMORA=1 IR budget leidžia -> <=max_llm
   (2) LLM kvietimai (45s HARD timeout, NO retry) query patikslinti / nuspręsti kada st-oti. Jei LLM krenta/timeout
   -> deterministinis rezultatas grąžinamas (branduolys veikia be jo). BUDGET pasiektas -> STOP, partial=true.
   NIEKADA jokio auto-retry, jokio neriboto ciklo (anti rc124).
3) ADITYVUS — retrieve tik SKAITO index/vault, NIEKO nekeičia/nerašo į gyvą turinį. Grąžina rezultatą, ne veiksmą.
4) INDEX pakankamumui demo: jei memory_index.jsonl per mažas prasmingam demo (tik ~2 iš 9a) -> BACKFILL bounded
   ~6-8 naujausius growth/skill įrašus per index_memory (kiekvienas 1 €0 LLM call, HARD timeout). LIMITAS 8 — NE visą
   vault (per brangu/ilgai). Tada demo.
5) DEMO (įrodyk multi-hop): 1-2 užklausos -> parodyk (a) tiesioginį match per primary_abstraction, (b) multi-hop
   per cue_anchor surastą related įrašą kurio paprastas match nerastų. Parodyk budget_used <= cap. Įrodyk fail-safe
   (jei LLM off -> deterministinis rezultatas vis tiek).
6) Benchmark: hera_bench.run() -> 9/9 (retriever adityvus). ROADMAP: „Fazė 9b — Memora policy-guided retriever
   ĮDIEGTA 2026-07-13 (deterministinis multi-hop branduolys + neprivalomas bounded LLM refinement, €0, HARD budget,
   HERA_MEMORA). Memora grandinė (9a index + 9b retriever) pilna."
7) DURABILUMAS: kodas -> hera-core-backup; index/ROADMAP -> hera-vault. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) hera_memora retrieve() — deterministinis multi-hop per cue_anchors + bounded
LLM refinement (HARD budget, anti rc124), (2) backfill ~8 įrašų demo indeksui, (3) demo: direct match + multi-hop
per cue anchor (rado related ko paprastas match nerastų), budget OK, (4) adityvus (tik skaito), benchmark 9/9,
(5) „FAZĖ 9b ĮDIEGTA — Memora grandinė pilna (index+retriever), multi-hop paieška gyva".

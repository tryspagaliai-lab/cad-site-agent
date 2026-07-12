UŽDUOTIS — (A) promote Memora skill + (B) FAZĖ 9a: Memora indeksas (rašymo pusė). <16 min. NEleisk pytest.
Telegram TRUMPAI. Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Vault -> PRIVATUS hera-vault. Viešo NELIESK.
SAUGUMAS: raktų nespausdink/necommit'ink.

=== DALIS A — PROMOTE Memora skill (human-gate) ===
Vartotojas patvirtino. Skill jau yra: skills/ai-agentu-atminties-strukturizavimas-memora/SKILL.md (status: draft,
distiliuota per ingestą).
- Frontmatter: status draft -> approved; pridėk approved_by: vartotojas (žmogaus gate), approved: 2026-07-12.
- Turinį nekeisk.
- BENCHMARK po promote: hera_bench.run() -> 9/9. Jei kristų -> rollback (grąžink draft) + pranešk.
- Growth ukv5jl (Memora): pažymėk „STATUS: PROMOTED 2026-07-12 (human-gate: vartotojas)".
- Episteminis flagas: prie „98%" pridėk „(ICML 2026 peer-reviewed, prieš full-context baseline; NE prieš mūsų
  esamą NapMem — realus laimėjimas mums: multi-hop paieška + nulis detalių praradimo, ne 98% ant NapMem)".
- Wiki-link + trajektorija (curation/human-gate-promote/skill).

=== DALIS B — FAZĖ 9a: Memora indeksas (rašymo pusė, ADITYVUS) ===
KONTEKSTAS: pridedam Memora-stiliaus indeksą prie to KAIP HERA rašo atmintį — turtingesnis paieškos sluoksnis,
NIEKO negriaunant. Skaitymo/retriever pusė = Fazė 9b (VĖLIAU, atskirai). €0, hand-prompted (NE RL-distilled=GPU).

SUKURK /opt/hera-processor/hera_memora.py. HERA_MEMORA jungiklis (default 0). Fail-safe (klaida -> praleisk, ne crash).
1) index_memory(entry_text, entry_ref) -> 1 €0 LLM call (45s HARD timeout, NO retry) sugeneruoja:
   - primary_abstraction: 6-8 žodžių kanoninė frazė (esmė).
   - cue_anchors: 2-4 trumpos alt-paieškos žymos.
   Append į /opt/hera-vault/memory_index.jsonl: {ts, entry_ref, primary_abstraction, cue_anchors}. Idempotentiška
   (tas pats entry_ref nepridedamas 2x). Jei LLM krenta/timeout -> įrašyk entry_ref su tuščia abstraction (fail-safe),
   įrašas NEprarandamas.
2) ADITYVUS — NEliesk esamo growth/skill/journal turinio, NEliesk NapMem. Tik prideda index eilutę greta.
3) HOOK: po growth/skill/journal įrašo -> index_memory (už HERA_MEMORA flago). Jei rizikinga tiesiogiai liesti
   pipeline -> palik funkciją + batch-run IR dokumentuok hook'ą (fail-safe pirmiau). Neblokuok ingesto.
4) DEMO (MINIMALUS, kad tilptų laike — TIK 2 įrašai): index_memory ant (a) Memora growth ukv5jl, (b) vieno journal
   ar skill įrašo. Parodyk sugeneruotą primary_abstraction + cue_anchors + kad memory_index.jsonl užpildytas.
   Įrodyk ADITYVUMĄ: originalūs failai NEPAKEISTI. NEindeksuok viso vault (per brangu/ilgai) — tik demo 2.
5) Paieškos NELIESK (9b). Benchmark: hera_bench.run() -> 9/9 (naujas modulis neturi gadinti).
6) ROADMAP: „Fazė 9a — Memora indeksas (rašymo pusė) ĮDIEGTA 2026-07-12 (primary_abstraction + cue_anchors,
   adityvus, €0 hand-prompted, HERA_MEMORA). 9b (policy-guided retriever) — laukia, budget-gated."
7) DURABILUMAS: kodas -> hera-core-backup; memory_index.jsonl + skill promote + ROADMAP -> hera-vault. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) Memora skill promote'inta (approved_by vartotojas; „98%" flaguota kaip vs
full-context, ne vs NapMem), (2) Fazė 9a: hera_memora.py — primary_abstraction+cue_anchors indeksas (adityvus, €0,
HERA_MEMORA), (3) demo 2 įrašai -> memory_index.jsonl užpildytas, originalai nepakeisti, (4) paieška=9b vėliau,
benchmark 9/9, (5) „MEMORA PROMOTE + FAZĖ 9a ĮDIEGTA — turtingesnis atminties indeksas, retriever kitas".

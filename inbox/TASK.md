UŽDUOTIS — FAZĖ 6: Gyvas projektų žurnalas (context retention, hera_journal.py). <14 min. NEleisk pytest.
Telegram TRUMPAI. Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Projektų duomenys -> PRIVATUS hera-vault.
Viešo repo NELIESK.

SAUGUMAS: raktų nespausdink/necommit'ink.

0) PURGE-PATIKRA (jei ankstesnė užduotis nespėjo): `grep -ri "apex" /opt/hera-vault/` darbinėje būsenoje turi būti 0.
   Jei ne — pervadink docs/APEX_ROADMAP.md -> docs/ROADMAP.md ir iškeisk „Apex" -> „sistema"/„produktas". Turinys
   (vizija, fazės 6/7/8) IŠLAIKOMAS. Tik po to eik prie žurnalo.

KONTEKSTAS: Fazė 6 = išspręsti „AI amnezijos" problemą — gyvas, redaguojamas projektų žurnalas kuris VISADA žino
kur kiekvienas procesas dabar (prie ko dirbama, kas sustabdyta, kas toliau). Substratas planuotojui (7) ir
įrankiams (8). Perpanaudoja NapMem L1-L4 + auto-atminties taisyklę. €0, DETERMINISTINIS branduolys (be LLM),
LLM tik neprivalomas pagalbininkas su HARD timeout.

SUKURK /opt/hera-processor/hera_journal.py. HERA_JOURNAL=1 jungiklis (default 0). Visos I/O klaidos fail-safe
(no-op, NIEKADA necrash'ink pipeline). Branduolys DETERMINISTINIS — jokio LLM nereikia bazinei funkcijai.

1) STATE.md schema (deterministinis šablonas) failui /opt/hera-vault/projects/<slug>/STATE.md:
   - frontmatter: slug, title, status (active|paused|done), updated (ISO data)
   - ## NOW — dabartinis fokusas (1-3 eil., žmogaus+auto palaikoma)
   - ## Active — kas vyksta dabar
   - ## Paused/Blocked — kas sustabdyta ir kodėl
   - ## Next — eilėje esantys subgoals
   - ## Decisions — append-only svarbių sprendimų log su data
   - ## Log — append-only įvykių log, naujausi viršuje (data + kind + tekstas)
   - ## Links — susiję vault notes/skills (wiki-nuorodos)

2) FUNKCIJOS (deterministinės, be LLM):
   - load_project_state(slug) -> grąžina dict + raw markdown. Skaitoma UŽDUOTIES PRADŽIOJE (context injection).
   - record_event(slug, text, kind="event") -> prideda eilutę į ## Log (naujausi viršuje), atnaujina `updated`.
     Append-only, NIEKADA neperrašo esamo Log turinio.
   - set_now(slug, text) / set_status(slug, status) -> atnaujina tik ## NOW / frontmatter status (ne kitas sekcijas).
   - add_decision(slug, text) -> append į ## Decisions su data.
   - list_projects() -> visų projektų slug+title+status+updated (iš projects/*/STATE.md).
   Jei projekto STATE.md nėra — ensure_project(slug, title) sukuria iš šablono.

3) LLM NEPRIVALOMAS pagalbininkas (fail-safe, atskiras): distill_next(slug) -> €0 modelis, HARD 45s timeout, NO
   retry -> iš paskutinių ## Log įrašų pasiūlo „Next" punktus. NIEKADA automatiškai neperrašo ## NOW/## Next —
   grąžina PASIŪLYMĄ (append kaip „(auto-suggest)" eilutė). Jei LLM krenta/timeout -> tyliai praleidžia,
   deterministinis branduolys veikia toliau.

4) INTEGRACIJA (minimali, saugi): auto-atmintis jau standing rule. Pridėk kabliuką kad inbox-task pabaigoje IR
   po ingesto record_event() įrašytų į numatytą projektą „hera-system" (build'o projektas). Automatiška, be klausimo,
   deterministiška. NELiesk esamos pipeline logikos daugiau nei šis vienas append-kabliukas; jei rizikinga —
   palik funkciją paruoštą, o kabliuką dokumentuok (fail-safe pirmiau).

5) DEMO (įrodyk deterministinį branduolį BE LLM):
   - ensure_project("hera-system", "HERA sistemos statyba")
   - record_event kelis realius: „5a/5b/5c savęs-tobulinimo grandinė uždaryta", „selfedit promote 9/9",
     „Fazė 6 žurnalas įdiegtas"
   - set_now("hera-system", "Fazė 6 (projektų žurnalas) įdiegta; toliau — Fazė 7 planuotojas")
   - add_decision: „Produkto pavadinimas pašalintas (be prekės ženklo)"
   - load_project_state("hera-system") -> parodyk kad grąžina pilną būseną. Įrodyk kad Log append-only (2 kartus
     record_event neperrašo, tik prideda).

6) ROADMAP: docs/ROADMAP.md pažymėk „Fazė 6 — ĮDIEGTA 2026-07-11 (deterministinis branduolys, LLM neprivalomas)".

7) DURABILUMAS: kodas -> hera-core-backup (privatus). projects/ + ROADMAP -> hera-vault (privatus). Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) hera_journal.py įdiegta, HERA_JOURNAL jungiklis, deterministinis branduolys,
(2) STATE.md schema (NOW/Active/Paused/Next/Decisions/Log/Links), append-only Log, (3) demo „hera-system" projektas
sukurtas + load grąžina būseną, (4) LLM distill_next neprivalomas (45s timeout, fail-safe), (5) „FAZĖ 6 ĮDIEGTA —
projektų žurnalas gyvas, substratas planuotojui (7)".

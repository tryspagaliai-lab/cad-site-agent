UŽDUOTIS — FAZĖ 7a: Planning Loop branduolys (hera_planner.py). <14 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Artefaktai -> PRIVATUS hera-vault. Viešo repo NELIESK.

SAUGUMAS: raktų nespausdink/necommit'ink.

KONTEKSTAS: Fazė 7 = specialist agents + planning loop. Šis žingsnis (7a) = PLANNING LOOP branduolys, kurį vėliau
naudos Ops/Social/Design agentai. Buzz/Warp video (ką tik promote'inta) tai validavo: principai>taisyklės +
subgoals→draft→self-critique→revizija. IŠVESTIS = DRAFT (jokio išorinio efekto, nieko nesiunčia/nekeičia gyvo).
€0, HARD budget anti-rc124, human-gate prieš bet kokį panaudojimą.

SUKURK /opt/hera-processor/hera_planner.py. HERA_PLANNER=1 jungiklis (default 0). Visos klaidos fail-safe
(grąžink dalinį rezultatą, NIEKADA necrash'ink).

FUNKCIJA plan(task, context=None, max_llm=6) grąžina struktūrą:
  { subgoals: [...], draft: str, critique: str, final: str, confidence: float, budget_used: int, partial: bool }

1) SUBGOALS: 1 LLM iškvietimas (€0 modelis, 45s HARD timeout, NO retry) -> užduotį išskaido į 2-5 tarpinius tikslus.
2) DRAFT: 1 LLM -> pirmas juodraštis pagal subgoals + context.
3) SELF-CRITIQUE (Reflexion-tipo, KRITINIS): 1 LLM -> AKTYVIAI ieško trūkumų/spragų/prieštaravimų/nepagrįstų
   teiginių juodraštyje. Promptas turi versti rasti realias problemas, NE „viskas gerai". Jei critique tuščias/
   „looks good" be konkretikos -> pažymėk low-confidence (ne rubber-stamp).
4) REVIZIJA: 1 LLM -> pataiso juodraštį pagal critique -> final.
5) (Neprivalomas, jei budget leidžia) CoVe iš hera_research faktiniams teiginiams patikrinti; jei kertasi su vault
   -> pažymėk final'e.
   HARD BUDGET: iš viso <= max_llm (6) LLM iškvietimų, kiekvienas 45s timeout no-retry. Pasiekus budget -> STOP,
   grąžink ką turi, partial=true. (Anti rc=124.)

INTEGRACIJA (perpanaudok, nekurk iš naujo):
- hera_journal (Fazė 6): jei context turi project slug -> load_project_state() kaip įvestį; pabaigoje record_event
  („planner: <task> -> draft paruoštas"). Deterministiška.
- hera_council: NEprivaloma — jei subgoal reikalauja deliberacijos, gali kviesti, bet budget'e.
- confidence: paprastas deterministinis balas (pvz. ar critique rado problemų + ar revizija jas adresavo).

SAUGIKLIAI: išvestis = TIK draft objektas; NIEKADA nerašo į gyvą skill/vault turinį, nieko nesiunčia, jokio
auto-apply. Panaudojimas (pvz. paversti draft'ą skill'u) eis per esamą human-gate (kaip 5b/5c).

DEMO (įrodyk kilpą + budget cap): plan("Parašyk trumpą 'Kada naudoti sandbox' gaires HERA skill'ui",
context=None). Parodyk: subgoals (2-5), draft, critique (su realiais pastebėjimais), final (pagerintas),
budget_used <= 6. Įrodyk kad self-critique NĖRA rubber-stamp (rado bent 1 konkrečią problemą).

NEGATYVUS/BUDGET testas: paleisk su max_llm=2 -> turi korektiškai sustoti partial=true, be crash, be rc124.

ROADMAP: docs/ROADMAP.md pažymėk „Fazė 7a — Planning loop branduolys ĮDIEGTA 2026-07-12 (output=draft, budget-capped,
self-critique ne rubber-stamp). 7b (Ops/Social/Design agentai) — laukia + priklauso nuo Fazės 8 įrankių."

DURABILUMAS: kodas -> hera-core-backup (privatus). ROADMAP/žurnalas -> hera-vault (privatus). Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) hera_planner.py įdiegta, HERA_PLANNER jungiklis, (2) kilpa subgoals→draft→
self-critique→revizija, HARD budget <=6 LLM/45s no-retry, (3) demo: subgoals+draft+critique(ne rubber-stamp)+final,
(4) budget testas partial=true be rc124, (5) išvestis=draft, jokio auto-apply/išorinio efekto,
(6) „FAZĖ 7a ĮDIEGTA — planning loop gyvas (validuota Buzz/Warp); 7b agentai laukia Fazės 8".

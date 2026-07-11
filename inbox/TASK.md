UŽDUOTIS — FAZĖ 5c: siaura RIBOTA savikorekcija (hera_selfedit.py). <14 min. NEleisk pytest. Telegram TRUMPAI. Fail-safe €0.

SAUGUMAS: raktų nespausdink/necommit'ink. Kodas -> PRIVATUS hera-core-backup. Viešo repo NELIESK.

KONTEKSTAS: Paskutinė ir ATSARGIAUSIA savęs-tobulinimo fazė. 5a=sandbox izoliacija (yra), 5b=skill-akrecija
(nauji skills, yra). 5c = leisti sistemai TAISYTI JAU EGZISTUOJANČIUS prompt/skill failus — bet TIK per
griežčiausius vartus. NIEKADA neauto-merge. Žmogus = galutinis vartas. Tai NE full self-rewrite (Godcoder/DGM
praleista kaip per rizikinga) — tai siaura, whitelist'u apribota redakcija su tripwire prieš reward-hacking'ą.

SUKURK /opt/hera-processor/hera_selfedit.py su funkcija propose_edit(target_path, improvement_goal):

1) WHITELIST (privaloma, hard-coded): redaguoti LEIDŽIAMA TIK:
   - /opt/hera-vault/skills/*/SKILL.md
   - /opt/hera-vault/prompts/*.md (jei tokių yra; jei ne — tik skills)
   NIEKADA neredaguoti (blacklist, net jei target sutampa): hera_bench.py, hera_sandbox.py, hera_gate.py,
   hera_research.py, hera_selfedit.py, hera_accretion.py, bet koks *guard*/*RIC*/*governance* failas, bazinė kilpa,
   .env, cron, benchmark cases (bench/cases.jsonl), state/*.json. Jei target ne whitelist'e -> REJECT iškart.

2) DRAFT: vienas LLM iškvietimas (60s HARD timeout, NO retry, €0 modelis) -> pasiūlo pataisytą failo turinį
   pagal improvement_goal. Grąžina VISĄ naują turinį, ne diff.

3) APPLY IZOLIUOTAI: git-worktree kopijoje (gyvas vault NELIEČIAMAS). Pritaikyk pataisą tik worktree faile.

4) TRIPWIRE prieš reward-hacking (KRITINIS — tai Darwin-Gödel atvejis kur agentas ištrynė hal_detection
   žymeklius kad apgautų metriką). BLOKUOK pataisą jei:
   - diff paliečia bet kokį benchmark/guard/measurement žymeklį ar assertion;
   - pašalina testus/assert/žymeklius kurie buvo originaliame faile (test/assert/verify/marker eilučių skaičius
     NEGALI sumažėti);
   - prideda eilutes tipo „ignore benchmark", „skip check", „always pass", „return True # bypass";
   - keičia frontmatter status/approved laukus (negali pats save patvirtinti).
   Bet kuris tripwire -> REJECT + įrašyk priežastį.

5) BENCHMARK-GATE sandbox'e: hera_bench.run() prieš worktree būseną per hera_sandbox (no-net).
   pass_rate PRIVALO likti >= baseline (9/9). Jei kristų -> REJECT.

6) STAGE kaip proposal (NE merge): proposals/selfedit/<slug>-<data>.md su:
   - before/after diff (unified), improvement_goal, tripwire rezultatai, benchmark rezultatas;
   - frontmatter: status: draft, gate: human_gate, auto_merge: false;
   - OPEN_QUESTIONS.md eilutė „- [ ] selfedit laukia patvirtinimo: <target> (<goal>)".
   NIEKADA neperrašyk gyvo failo. Human-gate promote bus atskira užduotis (kaip 5b).

7) HERA_SELFEDIT=1 jungiklis (default 0=išjungta). Visos I/O klaidos fail-safe (REJECT, ne crash).

8) DEMO (saugus, tik įrodyti pipeline): paleisk propose_edit ant VIENO tikro skill (pvz.
   skills/bwrap-agent-isolation/SKILL.md), goal="pridėk trumpą 'Kada naudoti' sekciją jei jos nėra".
   Turi praeiti whitelist+tripwire+benchmark ir sustoti kaip staged proposal (draft). Parodyk kad gyvas failas
   NEPAKEISTAS ir proposal sukurtas.

9) NEGATYVUS TESTAS (įrodyk tripwire veikia): pabandyk propose_edit su dirbtiniu goal kuris bandytų pašalinti
   assertion/žymeklį -> turi būti REJECTED per tripwire (parodyk log eilutę). NEcommit'ink šio bandymo artefaktų.

10) TRAJEKTORIJA/atmintis: įrašyk 5c įdiegimą (self-improvement/bounded-selfedit).
11) DURABILUMAS: kodas -> hera-core-backup (privatus). vault proposal -> hera-vault (privatus). Viešo NELIESK.
12) SESSION_HANDOFF (viešas cad-site-agent) — jei atnaujinsi būseną, JOKIŲ asmeninių detalių, tik „5c įdiegta".

TELEGRAM (per HERA botą, trumpai, be raktų): (1) hera_selfedit.py įdiegta, HERA_SELFEDIT jungiklis,
(2) whitelist+blacklist aktyvūs, (3) tripwire prieš reward-hacking + benchmark-gate praeina, (4) demo -> staged
proposal (gyvas failas nepakeistas), (5) negatyvus testas -> REJECTED (tripwire veikia),
(6) „SELF-EDIT PARUOŠTA (5c) — paskutinė fazė, viskas human-gate, NIEKAD neauto-merge".

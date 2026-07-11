UŽDUOTIS — HUMAN-GATE PROMOTE (5c selfedit): patvirtintas selfedit proposal į gyvą skill. <10 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup. Viešo NELIESK.

KONTEKSTAS: VARTOTOJAS (galutinis vartas) PATVIRTINO 5c demo selfedit pasiūlymą (bwrap-agent-isolation SKILL.md
+ „Kada naudoti" sekcija). Dabar promote: pritaikyk staged pataisą į GYVĄ failą. Antras realus žmogaus-vartas.

1) Rask NAUJAUSIĄ selfedit proposal: /opt/hera-vault/proposals/selfedit/*.md kuris nukreiptas į
   skills/bwrap-agent-isolation/SKILL.md ir yra status: draft / gate: human_gate. (5c demo proposal.)
   Iš jo paimk „after" turinį (visą naują failo versiją, kurią pasiūlė hera_selfedit).

2) PRIEŠ pritaikant, PAKARTOK saugiklius gyvai (tas pats hera_selfedit tripwire+benchmark, be naujo LLM):
   - TRIPWIRE dar kartą prieš „after" turinį (jokių pašalintų assert/žymeklių, jokių bypass/skip/always-pass
     frazių, jokio frontmatter status/approved savęs-keitimo). Jei kirstų -> STOP, NEpromote, pranešk.
   - Palygink žymeklių/assert skaičių: after >= before. Jei mažiau -> STOP.

3) PROMOTE: perrašyk gyvą /opt/hera-vault/skills/bwrap-agent-isolation/SKILL.md „after" turiniu.
   Frontmatter'yje (jei toks laukas yra) pažymėk promote metaduomenis: approved_by: vartotojas (žmogaus gate),
   approved: 2026-07-11, source: selfedit-proposal. Necommit'ink raktų.

4) BENCHMARK po promote: hera_bench.run() GYVAI -> turi likti 9/9. Jei kristų -> ROLLBACK (atstatyk ankstesnę
   failo versiją per git checkout gyvame vault) ir pažymėk ataskaitoje „ROLLBACK, benchmark krito".

5) PROPOSAL pažymėk: proposals/selfedit/...md antraštėje/statuse „PROMOTED 2026-07-11 (human-gate: vartotojas)".

6) OPEN_QUESTIONS.md: atitinkamą „selfedit laukia patvirtinimo" eilutę pažymėk atlikta `- [x]` + „→ PROMOTED".

7) WIKI: paleisk hera_wikilink.py (arba lint) kad pakeistas skill liktų grafe; parodyk ar orphan nepadidėjo.

8) TRAJEKTORIJA/atmintis: įrašyk promote veiksmą (curation/human-gate-promote/selfedit).

9) DURABILUMAS: vault commit+sync (privatus hera-vault). Jei liesta kodą — hera-core-backup. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) selfedit proposal promote'intas į gyvą skill, approved_by
vartotojas, (2) tripwire+benchmark po promote 9/9 (ar rollback), (3) proposal+OPEN_QUESTIONS pažymėti,
(4) wiki grafas OK, (5) „SELFEDIT PROMOTE'INTAS (2-as human-gate ciklas, 5c grandinė uždaryta pilnai)".

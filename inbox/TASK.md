UŽDUOTIS — HUMAN-GATE PROMOTE: patvirtintas skill „bwrap-agent-isolation" į gyvą vault. <8 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: VARTOTOJAS (galutinis vartas) PATVIRTINO 5b pasiūlytą skill'ą. Dabar promote: perkelk juodraštį iš
staged proposal į gyvą /opt/hera-vault/skills/. Tai pirmas realus žmogaus-vartas -> promote.

1) Iš proposals/accretion/bwrap-agent-isolation-2026-07-11.md paimk skill juodraštį (frontmatter+turinį) ir
   sukurk gyvą /opt/hera-vault/skills/bwrap-agent-isolation/SKILL.md. Frontmatter'yje pakeisk:
   - status: draft -> approved (arba tiesiog palik veikiantį skill formatą kaip kiti gyvi skills)
   - pridėk: approved_by: vartotojas (žmogaus gate), approved: 2026-07-11
   Turinį išlaikyk kaip pasiūlyme (nekeisk esmės).
2) PROPOSAL pažymėk: proposals/accretion/...md antraštėje/statuse „PROMOTED 2026-07-11 (human-gate: vartotojas)".
3) OPEN_QUESTIONS.md: pažymėk atitinkamą eilutę atlikta — `- [x]` (raktas k:d4f7edd1ef77 „skill-akrecija laukia
   patvirtinimo: bwrap-agent-isolation"), pridėk „→ PROMOTED".
4) BENCHMARK po promote: hera_bench.run() gyvai -> turi likti 9/9 (naujas skill neturi sugadinti matuoklio).
   Jei kristų -> ROLLBACK (ištrink ką tik pridėtą skill) ir pažymėk ataskaitoje.
5) WIKI: paleisk hera_wikilink.py (arba lint) kad naujas skill įsijungtų į grafą; parodyk ar orphan nepadidėjo.
6) TRAJEKTORIJA/atmintis: įrašyk promote veiksmą (curation/human-gate-promote).
7) DURABILUMAS: vault commit+sync (privatus hera-vault per cron/rankinis); jei liesta kodą — hera-core-backup.
   Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) skill promote'intas į gyvą skills/, approved_by vartotojas,
(2) proposal+OPEN_QUESTIONS pažymėti, (3) benchmark po promote 9/9 (ar rollback), (4) wiki grafas OK,
(5) „SKILL PATVIRTINTAS IR PROMOTE'INTAS (pirmas human-gate ciklas)".

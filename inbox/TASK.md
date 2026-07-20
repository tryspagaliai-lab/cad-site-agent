UŽDUOTIS — LOOP C HUMAN-GATE sprendimas: patvirtinti 6 growth prune, ATMESTI gdx0fm+lto8bb ir 2 skill eviction. <10 min.
NEleisk pytest. Fail-safe. €0. Raktų nespausdink. Deterministiška (be LLM/tinklo). Ataskaita TIK į HERA botą.
Privatus hera-vault. Viešo cad-site-agent NELIESK.

KONTEKSTAS: Loop C (2026-07-20 04:00) staged 11 konsolidacijos pasiūlymų + 13 eviction kandidatų. Vartotojas
peržiūrėjo ir nusprendė (human-gate). Vykdyk TIKSLIAI taip:

A) PATVIRTINTI — prune šiuos 6 growth (distiliuoti į skills, turinys ten gyvena; git-atšaukiama):
   - growth/2026-07-13-20260713T121330Z-i8suoz.md  (→ skill di-kodo-generatoriu-atranka)
   - growth/2026-07-13-20260713T171430Z-96hcmw.md  (→ skill llm-kvantavimo-strategijos-pasirinkimas)
   - growth/2026-07-13-20260713T174400Z-fidnk7.md  (→ skill pkc-duomenu-generavimas)
   - growth/2026-07-13-20260713T183030Z-f0bs8d.md  (→ skill di-programuotoju-darbo-eigu-projektavimas)
   + kiti 2 iš Loop C 11-uko, kurie yra PAPRASTI distiliuoti growth (NE gdx0fm, NE lto8bb) — jei tokie yra proposals/
   sąraše. PRIEŠ trindamas f0bs8d: patikrink, kad jo „Kuravimo pastaba (forward-strengthening)" 4 pamokos + guardrail
   žymė YRA perkelta į paskirties skill'ą arba FUTURE_GPU/kitą natą; jei nėra — PERKELK pastabą į skill'ą, tada prune.
   Tas pats i8suoz („55% AI kodo spragų" atsargumo vėliava) ir fidnk7 (SearchEyes sėkla → hera_research v2) — vėliavos
   turi išlikti skill'uose. Jei perkelti neįmanoma — praleisk tą failą ir pažymėk ataskaitoje.

B) ATMESTI (NIEKO nedaryti su failais, TIK pažymėti proposals kaip REJECTED su priežastim):
   - gdx0fm prune → REJECTED: „HOLD (human-gate 2026-07-18): episteminės vėliavos — nepatvirtinti marketingo
     skaičiai, žalias provenance saugomas sąmoningai. NEteikti pakartotinai." 
   - lto8bb prune → REJECTED: ta pati priežastis (SkillOpt — rejected-edit buffer provenance).
   - skill breziniu-sluoksniu-standartas eviction → REJECTED: „skills nešalinam; cad-domenas aktualus (kq6reu/cad-3d)."
   - skill bwrap-agent-isolation eviction → REJECTED: „GYVAS 5b promotintas skill, sandbox izoliacijos pagrindas
     (5a/5c naudoja). NIEKADA nešalinti."
   - Jei įmanoma — pridėk NO-RESTAGE žymą gdx0fm/lto8bb (kad Loop C nebeteiktų jų kas savaitę; pvz. frontmatter
     `consolidation: hold-permanent`), ir Loop C logika tegul gerbia šitą žymą (jei lengva — pridėk patikrą; jei ne —
     tik žymą, logiką kitą kartą).

C) TRAJEKTORIJA + WIKI: curation/loopC-gate-2026-07-20 įrašas (approve 6, reject 4+). hera_wikilink/lint pass po
   prune — parodyk orphan/dangling PO (dangling buvo 59 — patikrink ar concepts.md regeneravosi; jei dangling
   nemažėja, pažymėk ataskaitoje kodėl).

D) BACKUP: commit hera-vault. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Deterministiška. Skills NETRINAM niekada. gdx0fm/lto8bb failų NELIESK (tik proposal žymos + frontmatter).
Jokio pytest-all. Raktų nespausdink.

ATASKAITA (HERA botas, trumpai): (a) prune N patvirtinta (kurie; ar vėliavos perkeltos); (b) atmesta 4+ (patvirtink
gdx0fm/lto8bb/2 skills saugūs); (c) NO-RESTAGE žyma pridėta? (d) wiki-lint PO: orphan/dangling (ar 59 sumažėjo?);
(e) vault push OK/ne; (f) 1 eil. kas toliau.

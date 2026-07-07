UŽDUOTIS — HERA Fazė 3: self-improving kilpa (ATDP-lite + Skill-output). Dirbk autonomiškai
(superpowers OK). NELIESK veikiančios Fazės 2 (ingest+extract+processor+selector lieka) — tik PRAPLĖSK.
Feasible tik NEMOKAMAM stack'ui: Gemini free, JOKIO modelio treniravimo/RL/svorių. Atsiskaityk į Telegram
TRUMPAI, aiškiu galutiniu statusu.

Kontekstas (HERA selektoriaus verdiktai iš 3 parsintų video): priimta idėja — self-evolving agentai per
„framework-space" evoliuciją (ATDP protokolas + Skills kaip evoliucijos variklis), be treniravimo.

1) ATDP-LITE TRAJEKTORIJOS LOGAS. Kiekvieną apdorotą job'ą/užduotį įrašyk kaip tipizuotą įrašą (JSONL,
   append) į /opt/hera-vault/trajectories/<YYYY-MM-DD>.jsonl. Laukai:
   {id, ts, kind, input(šaltinis+content ref), context(extractor+prompt versijos/hash), action(extract/select/skill),
    outcome(full.md/growth/skill ref), reward(nullable, VĖLIAU atnaujinamas — delayed feedback), 
    metadata(model=gemini-flash-latest, cost=0, trukmės, versijos/provenance)}.
   Reward laukas turi būti atnaujinamas vėliau NEPAKEIČIANT pirminio įrašo (append naują reward event).

2) SKILL-OUTPUT. Kai HERA selektorius nusprendžia, kad turinys moko PAKARTOJAMOS kompetencijos —
   generuok /opt/hera-vault/skills/<slug>/SKILL.md su frontmatter (name, description, when_to_use) + body
   (distiliuota instrukcija iš turinio). Pažymėk „draft". Kai NE kompetencija, o žinia — lieka growth/.md (kaip dabar).

3) KONTRAFAKTINIS PAKARTOJIMAS (validacijos vartai). CLI /opt/hera-processor/hera_replay.py:
   `hera_replay.py <job_id> --with-prompt <f>|--with-skill <slug>` — perleidžia išsaugotą job'o INPUT su nauju
   prompt'u/skill'u, palygina su originaliu outcome, ir pasako ar PAGERĖJO (trumpas verdiktas + diff santrauka).
   Tai vartai PRIEŠ priimant bet kokį pakeitimą.

4) SELF-TEST ant esamų 3 job'ų: (a) sugeneruok jiems ATDP-lite trajektorijas, (b) chw25r (Wargaming) — jei tinka,
   išvesk SKILL.md juodraštį, (c) parodyk vieną hera_replay pavyzdį.

5) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk (nėra creds).

Į Telegram: kas pridėta (trajektorijos/skill-output/replay), self-test rezultatai, kiek skill juodraščių,
ir aiškiai „FAZĖ 3 BAIGTA" arba ko trūksta.

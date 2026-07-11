UŽDUOTIS — 4a FAZĖ: AUTO-RESEARCH SAUGIKLIO FUNKCIJA (STANDALONE + testas; DAR NEjungti į gyvą ingest). <13 min.
NEleisk pytest. Telegram TRUMPAI. €0. Fail-safe.

⚠️ ANTI rc=124: KIEKVIENAS LLM kvietimas timeout 45s, JOKIO retry. hera_research jau turi biudžetą. vault-check —
1 LLM kvietimas max. Jei viršija/timeout — grąžink „escalate"/partial, NIEKADA nekabink. Testas MAŽAS.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup (askpass; jis yra).

KONTEKSTAS: turim hera_research.py (3 fazė). Dabar saugiklis, kuris NUSPRENDŽIA, ar tirti, ir suformuoja verdiktą.
Principas (iš tyrimo): NEkartok tarybos; saugiklis klausia „ar tiesa + ar dera su vault'u". Ir NE ant visko.

1) /opt/hera-processor/hera_gate.py, STANDALONE (dar nejungti į dispatcher/ingest):

   a) should_verify(candidate, council_result) -> bool (TRIGERIS, deterministinis): True TIK jei bent viena:
      - council_action = promote_candidate (aukšta rizika), ARBA
      - selector high + taps skill (reuse'inama taisyklė), ARBA
      - tarybos balsų sklaida didelė / žemas sutarimas (jei metrika prieinama), ARBA
      - (vėliau) vault prieštaravimas.
      Kitu atveju False -> saugiklis PRALEIDŽIA (pigus kelias, jokio tyrimo).

   b) vault_check(candidate) -> {relation: contradicts|supports|complements|unrelated, note}: 1 LLM kvietimas
      (Gemini, 45s), lygina kandidatą su top-k susijusiais vault puslapiais (naudok esamą nav/RAG paiešką).
      Pigu, be web.

   c) gate(candidate, council_result) -> {decision: pass|block|escalate, verdict, confidence, dossier}:
      - if not should_verify -> decision=pass (skip, cheap).
      - else -> vault_check; jei contradicts ARBA neaišku -> hera_research.research(kandidato teiginys) (išorinis).
        Sujungk: supported + nėra vault konflikto -> pass (žyma low-risk); contradicted (išorė ar vault) -> block;
        no-evidence/mixed -> escalate su dossier (šaltiniai, prieštaravimai, confidence).
      - Rašyk verifikacijos pėdsaką (kas patvirtino, šaltiniai) į grąžinamą dossier.

2) JUNGIKLIS HERA_GATE=1 (default 1; =0 -> gate visada pass). GATE dar NEjungtas į gyvą ingest — tik standalone
   funkcija. Gyvą įpynimą darysim 4b atskirai (kad nerizikuotume ingest kabėjimo).

3) TESTAS (MAŽAS): (a) kandidatas su council_action=stage_for_review, žema rizika -> should_verify=False ->
   gate pass be tyrimo (greita); (b) kandidatas su promote_candidate -> should_verify=True -> vault_check +
   (jei reikia) research -> parodyk decision/verdict/confidence, ar research suveikė, kiek užtruko; (c) fail-safe:
   research timeout/klaida -> gate grąžina escalate, ne crash/hang.

4) BENCHMARK REGRESIJA: paleisk hera_bench.run() -> pass_rate turi likti 1.0 (9/9) — gate neturi nieko sugadinti
   (jis standalone, tad neturėtų liesti, bet patvirtink).

5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup (askpass, secret-scan).
   Viešo NELIESK.

TELEGRAM (trumpai, be raktų): (1) hera_gate.py veikia (trigeris+vault-check+decision), (2) testai a/b/c
(pass be tyrimo; promote->tyrimas su verdiktu; fail-safe escalate), (3) benchmark pass_rate nepakito,
(4) backup OK, (5) „AUTO-RESEARCH SAUGIKLIS PARUOŠTAS (4a, standalone)".

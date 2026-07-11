UŽDUOTIS — 4b FAZĖ: ĮPINTI AUTO-RESEARCH SAUGIKLĮ Į GYVĄ INGEST + ACK su verdiktu. <13 min.
NEleisk pytest. Telegram TRUMPAI. €0.

⚠️⚠️ KRITINIS FAIL-SAFE: saugiklis GYVAME ingest'e NIEKADA neturi kabinti ar sulaužyti pipeline.
- gate() jau turi HARD 180s research cap + 45s LLM. Papildomai: visą gate() iškvietimą dispatcher'yje apgaub
  try/except + bendru timeout'u. Jei gate krenta/timeout -> elgtis kaip PASS (council verdiktas galioja),
  NIEKADA neblokuok ir nenutrauk ingest. Saugiklis tik PRIDEDA info, negali pakenkti.
- should_verify TRIGERIS turi likti retas (promote_candidate / high-skill / nesutarimas) — dauguma ingest'ų
  saugiklio NEpaleidžia (pigu, greita, be tyrimo).

SAUGUMAS: raktų nespausdink/necommit'ink. Push į PRIVATŲ hera-core-backup (askpass).

1) ĮPYNIMAS dispatcher'yje (po tarybos, prieš galutinį įrašymą/ACK):
   - if HERA_GATE=1: iškviesk should_verify(candidate, council_result).
   - Jei False -> kelias nepakito (kaip dabar).
   - Jei True -> gate(candidate, council_result) su bendru fail-safe. Rezultatą (decision/verdict/confidence/
     dossier) įrašyk į kandidato įrašą (verifikacijos pėdsakas / provenance) IR panaudok:
     * pass -> kaip council (stage/promote), + žyma „verified: supported (conf)".
     * block -> NEpromote'ink; pažymėk „gate: contradicted"; lieka draft su įspėjimu (žmogus mato).
     * escalate -> įrašyk į /opt/hera-vault/OPEN_QUESTIONS.md su dossier (šaltiniai/prieštaravimai) — tavo sprendimui.
   - GOVERNANCE nekeisk: viskas lieka draft/human_gate; gate NEauto-promote'ina, tik prideda verdiktą.

2) ACK PRATURTINIMAS (tai vartotojo „gera reakcija"): kai gate suveikė, ingest ACK papildyk verdiktu, pvz.:
   „📥 Priimta: <title> | selektorius X | taryba Y | 🔎 patikrinta: supported 0.8" arba „| ⚠️ eskaluota: reikia tavo
   sprendimo". Kai gate NEsuveikė (dauguma) — ACK kaip dabar. ACK eina per PARSER botą (kur vartotojas), sistemos
   raportai — HERA botas (nekeisk maršruto).

3) SESIJŲ INDEKSAS: ingest įraše (index.jsonl) pridėk gate_decision lauką kai buvo.

4) TESTAS (be gyvo laukimo, jei įmanoma): (a) sintetinis promote_candidate kandidatas per dispatcher su HERA_GATE=1
   -> gate suveikia, ACK turi verdiktą, įrašas turi verifikacijos pėdsaką; (b) žemos rizikos -> gate praleistas,
   ACK kaip anksčiau; (c) FAIL-SAFE: dirbtinė gate klaida/timeout -> ingest baigiasi normaliai (pass), ACK
   išsiunčiamas, NIEKADA nekabo/nelaužo.
5) BENCHMARK: hera_bench.run() -> pass_rate 1.0 (9/9) nepakito.
6) DURABILUMAS: kopija į n8n/hera/ + push į PRIVATŲ hera-core-backup (secret-scan). Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) saugiklis įpintas į gyvą ingest, fail-safe (gate klaida->pass),
(2) ACK dabar rodo verdiktą kai suveikia (pavyzdys), (3) testai a/b/c OK, (4) benchmark nepakito, (5) backup OK,
(6) „AUTO-RESEARCH SAUGIKLIS GYVAS (4b)".

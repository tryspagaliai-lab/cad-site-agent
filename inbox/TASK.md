UŽDUOTIS — SAVĘS-TOBULINIMO 1 FAZĖ: BENCHMARK MATUOKLIS (held-out). <12 min.
NEleisk viso pytest — tik taikinius. LLM kvietimams griežti timeout'ai (60s+1 retry). Telegram TRUMPAI.
€0, fail-safe. NIEKO sistemoje nekeičia — tik matuoklis (matavimo įrankis būsimiems savęs-keitimams).

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta hera kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: prieš bet kokį savęs-tobulinimą reikia MATUOKLIO — held-out užduočių, kuriomis matuosim, ar
pakeitimas realiai pagerino (be to bet koks savęs-keitimas aklas ir atviras reward-hacking'ui). Naudok JAU
ŽINOMUS atvejus su žinomu teisingu rezultatu (dauguma jų vault'e/history).

1) hera_bench.py + benchmark rinkinys /opt/hera-vault/bench/cases.jsonl (~10-15 atvejų). Kiekvienas atvejis:
   {id, kind (selector/router/query/docbound), input (esamas job_id/klausimas/žinutė), expected}. Pvz.:
   - SELECTOR: šiukšlė (test-file-001 / tuščias tekstas) -> expected score 0-1; off-domain (zmescience hardware
     job 0xbypg) -> 2-3; stipri tema (SwarmResearch ubbsu8 / atminties video) -> 8-10.
   - ROUTER: „labas HERA" -> chat (ne ingest); „kas yra ATDP?" -> question; http nuoroda -> ingest.
   - QUERY: „kas yra ATDP?" -> found=True, cituoja šaltinį; klausimas UŽ vault ribų -> „nerandu".
   - DOCBOUND (jei fixture yra): klausimas pagal dokumentą -> atsako su citata; už ribų -> „dokumente to nėra".
   Rink atvejus iš realių vault/history duomenų (deterministiška kur įmanoma; LLM žingsniai su timeout).
2) BALO FUNKCIJA hera_bench.run(): kiekvienam atvejui pass/fail (su tolerancija selector balams, pvz. ±1.5);
   grąžina: {passed, total, pass_rate, total_llm_calls, wall_time_s}. Deterministinius atvejus vertink be LLM
   kur įmanoma; LLM atvejams — griežtas timeout, fail-safe (klaida atveju = fail, ne crash).
3) BASELINE: paleisk vieną kartą -> įrašyk /opt/hera-vault/bench/baseline-<data>.md (pass_rate, kiek pravažiavo,
   kaina, laikas). Tai etaloninis taškas.
4) SVARBU: matuoklis NIEKO nekeičia gamyboje — tik matuoja. Jokio auto-promote, jokio savęs-keitimo šioje fazėje.
5) TESTAS: (a) hera_bench.run() grąžina baseline skaičius (parodyk pass_rate + kiek atvejų); (b) idempotencija —
   paleisk 2x, cases nedubliuojasi; (c) fail-safe: dirbtinė klaida viename atvejyje -> tas fail, likę įvertinami,
   bench nesugriūva.
6) DURABILUMAS: hera_bench.py kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup.
   cases.jsonl + baseline md sync per vault cron (matysiu). Viešo NELIESK.

TELEGRAM (trumpai, be raktų): (1) matuoklis sukurtas, kiek atvejų, (2) baseline pass_rate + kaina/laikas,
(3) nieko gamyboje nekeista, (4) backup OK, (5) „MATUOKLIS PARUOŠTAS (1 FAZĖ)".

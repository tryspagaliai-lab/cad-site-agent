UŽDUOTIS — MATUOKLIS ATSTATYMAS PO TIMEOUT (DETERMINISTINIS, be gyvo LLM perleidimo). <10 min, GRIEŽTAI.
Ankstesnė matuoklio užduotis NUTRŪKO po 15 min (rc=124) — kabantis LLM kvietimas. NEleisk pytest.
NENAUDOK gyvo LLM pipeline perleidimo (tai ir kabo). Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink.

0) BŪKLĖ: systemctl is-active hera-processor hera-ingest; ar hera_bench.py pusiau parašytas? py_compile.
   Jei kas pusiau — sutvarkyk į veikiančią būseną. Servisai turi likti active.

1) MATUOKLIS BE GYVO LLM — lygink EXPECTED su JAU ĮRAŠYTAIS rezultatais (jie vault'e, greita, €0, nekabo):
   - Selektoriaus/tarybos atvejai: skaityk iš /opt/hera-vault/state/*.json ir sessions/index.jsonl JAU esamus
     selector_score + council_action žinomiems job'ams. Sudaryk cases.jsonl su expected:
     * šiukšlė (test-file-001 / tuščias tekstas job'ai) -> expected selector 0-1
     * off-domain (zmescience 0xbypg) -> 2-3
     * stiprios temos (atminties/agentų video, score 8-10) -> 8-10
     Įvertink LYGINDAMAS įrašytą reikšmę su expected (tolerancija ±1.5). JOKIO naujo LLM kvietimo.
   - Router atvejai: „labas"->chat, „kas yra ATDP?"->question, http->ingest — jei router turi GRYNAI
     deterministinę greitfiltro funkciją (be LLM), naudok ją; jei ne — PRALEISK router atvejus v1
     (nekviesk LLM), pažymėk ataskaitoje „router atvejai atidėti (reikalautų LLM)".
2) BALO FUNKCIJA hera_bench.run(): pass/fail per atvejį (lyginant su įrašytu), grąžina
   {passed,total,pass_rate,wall_time_s}. Turi baigti per KELIAS SEKUNDES (jokio LLM => nekabo).
3) BASELINE: /opt/hera-vault/bench/baseline-<data>.md su skaičiais.
4) JEI kuris atvejis reikalautų LLM — v1 jį PRALEISK, ne kviesk. Matuoklis v1 = deterministinis. Gyvą-perleidimo
   variantą (su griežtais timeout'ais) pridėsim vėliau atskira užduotimi, ne dabar.
5) TESTAS: hera_bench.run() grąžina baseline per <10s; idempotencija (2x nedubliuoja); fail-safe.
6) DURABILUMAS: kopija į n8n/hera/ + push į PRIVATŲ hera-core-backup. cases.jsonl+baseline sync per vault cron.

TELEGRAM (trumpai, be raktų): (1) ar rasta pusiau būklė ir kas sutvarkyta, (2) matuoklis deterministinis, kiek
atvejų, baseline pass_rate + laikas (turi būti sekundės), (3) router atvejai atidėti ar įtraukti,
(4) „MATUOKLIS PARUOŠTAS (DETERMINISTINIS)".

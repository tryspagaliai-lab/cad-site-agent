UŽDUOTIS — SESIJŲ INDEKSATORIUS 24/7 (registruoja viską nuo dabar; be Telegram/2FA). <12 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe: indeksavimas NIEKADA neturi sulaužyti runner'io ar HERA.

SAUGUMAS: raktų nespausdink/necommit'ink. Indeksas PRIVATUS (vault, sync į privatų hera-vault), jokio viešo repo.

TIKSLAS: atkurti seno @FlashCodeMon_bot esmę, bet be jo — nuolatinis registras „kas ir kada VPS'e buvo daroma",
peržiūrimas vėliau. Naudok tai, kas JAU 24/7 sukasi (cron runner), ne naują atskirą demoną.

1) INDEKSO VIETA: /opt/hera-vault/sessions/index.jsonl (append-only). Kiekvienas įrašas viena JSON eilutė:
   {ts_start, ts_end, duration_s, rc, kind:"runner_session", task_title (TASK.md 1-a eilutė), telegram_sent (bool),
   session_transcript (kelias į claude -p JSONL jei randamas, kitaip null)}. UTF-8.

2) RUNNER HOOK: pataisyk /usr/local/bin/vps_agent_runner.sh — apie kiekvieną `claude -p` paleidimą:
   prieš paleidžiant užfiksuok ts_start+task_title; po jo ts_end+rc+duration; append eilutę į index.jsonl.
   GRIEŽTAI fail-safe: jei indeksavimo dalis krenta (append klaida ir pan.) — runner'is TĘSIA normaliai
   (|| true, atskiras try). Backup: cp vps_agent_runner.sh vps_agent_runner.sh.bak-<data> prieš keitimą.

3) HERA ĮVYKIAI (jei paprasta): kai ateina ingest ACK (selektorius/taryba) — tee'ink trumpą įrašą į tą patį
   index.jsonl {kind:"ingest", ts, title, selector_score, council_action}. Jei sudėtinga įpinti — praleisk,
   runner sesijų užtenka v1.

4) DIENOS SANTRAUKA: /opt/hera-vault/sessions/DAILY-<YYYY-MM-DD>.md — prijunk prie Loop B (valandinis) arba mažas
   cron: iš index.jsonl per parą sugeneruok žmogui skaitomą suvestinę (kiek sesijų, kokios užduotys, rc, kiek
   ingest'ų). Deterministinis, be LLM.

5) PERŽIŪROS ĮRANKIS: /root/hera_sessions.py (arba bash) — parodo paskutines N sesijų iš index.jsonl (data, užduotis,
   rc, trukmė). Kad vartotojas/kuratorius greitai matytų „kas buvo daroma".

6) TESTAS: (a) rankiniu būdu pridėk 1 testinį įrašą per hook logiką ARBA palauk 1 runner ciklą -> index.jsonl turi
   įrašą; (b) hera_sessions.py parodo jį; (c) DAILY md sugeneruotas. Parodyk paskutinio įrašo pavyzdį (be raktų).

7) DURABILUMAS: skriptų kopija į /opt/cad-site-agent/n8n/ lokaliai (be push į viešą) + jei liesta hera kodą,
   push į PRIVATŲ hera-core-backup. index.jsonl ir DAILY md nusisync'ins per esamą vault cron.

TELEGRAM (trumpai, be raktų): (1) index.jsonl kuriamas, runner hook įdiegtas (fail-safe), (2) paskutinės sesijos
per hera_sessions.py — pavyzdys, (3) DAILY santrauka veikia, (4) „SESIJŲ INDEKSATORIUS VEIKIA 24/7".

UŽDUOTIS — INGEST ĮVYKIAI Į SESIJŲ DIENORAŠTĮ (balas + tarybos verdiktas). <10 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe: logingas NIEKADA neturi sulaužyti ingest/HERA.

SAUGUMAS: raktų nespausdink/necommit'ink. Privatu (vault + hera-core-backup), jokio viešo repo.

KONTEKSTAS: sesijų indeksatorius jau veikia (sessions/index.jsonl + DAILY). v1'e praleisti INGEST įvykiai —
dabar pridedam. Kai vartotojas siunčia turinį botui, HERA gamina ACK „📥 Priimta: <title> | selektorius <score> |
taryba <action> (<n balsų>) | skill/growth: <path>". Tą patį reikia įrašyti į tą patį index.jsonl.

1) RASK kur processor'iuje formuojamas/siunčiamas ingest ACK (dispatcher/processor, ta vieta kur jau turim
   title/selector_score/council_action/votes/skill_path). TEN po ACK suformavimo append eilutę į
   /opt/hera-vault/sessions/index.jsonl (naudok esamą hera_index_append.py jei tinka, arba tiesioginį append):
   {ts, kind:"ingest", title, selector_score, council_action, council_votes, skill_growth}.
   GRIEŽTAI fail-safe: try/except, append klaida NIEKADA nenutraukia ingest'o (kaip runner hook).

2) DAILY santrauka: hera_daily_summary.py jau turi ingest lentelės schemą — patikrink, kad ji realiai
   užsipildo iš kind:"ingest" įrašų (data, title, balas, verdiktas). Jei reikia mažo pataisymo — padaryk.

3) TESTAS: (a) jei paprasta — perleisk vieną JAU apdorotą kandidatą per ACK kelią (arba sukurk 1 sintetinį
   ingest įrašą per tą pačią funkciją) -> index.jsonl atsiranda kind:"ingest" eilutė; (b) hera_sessions.py
   parodo mišrų sąrašą (runner + ingest); (c) DAILY md ingest lentelė užsipildo. Parodyk pavyzdį (be raktų).

4) DURABILUMAS: jei liesta HERA kodą (/opt/hera-processor) — kopija į /opt/cad-site-agent/n8n/hera/ + push į
   PRIVATŲ hera-core-backup (secret-scan). Viešo repo NELIESK. index.jsonl/DAILY nusisync'ins per vault cron.

TELEGRAM (trumpai, be raktų): (1) ingest įvykiai dabar loginami (fail-safe)?, (2) mišraus sąrašo pavyzdys
(runner+ingest), (3) DAILY ingest lentelė veikia, (4) privatus backup jei liesta kodą, (5) „INGEST DIENORAŠTIS VEIKIA".

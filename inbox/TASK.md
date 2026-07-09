UŽDUOTIS — TARYBOS PATAISA (GREITAI, FOKUSUOTAI). NEperstatyk, NEleisk viso pytest. <10 min, timeout saugiklis yra.
2 problemos iš prod log: (1) 413 Payload Too Large — juror'iams siunčiamas VISAS ~29k tekstas, dauguma Groq atmeta;
(2) ingest'as TYLUS — vartotojas negauna jokios žinutės kad turinys priimtas+įvertintas. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

1) FIX 413 (svarbiausia): hera_council.py — prieš siunčiant kandidatą juror'iams, NEsiųsk viso ištraukto teksto.
   Sukonstruok TRUMPĄ juror digest'ą (konfig env HERA_COUNCIL_MAXCHARS, default ~4000): selektoriaus santrauka/priežastis
   + kandidato pradžia (pirmi ~3000 simb.) + metaduomenys (šaltinis, tipas, selektoriaus balas). Juror vertina
   keep/drop + domain_fit iš digest'o — jam nereikia viso teksto. Taip dingsta 413. Palik ribą konfigūruojamą.
   (Jei jau yra koks truncate — sutvarkyk kad realiai <maxchars visiems tiekėjams; Groq limitas mažesnis.)

2) INGEST ACK (Telegram): kai taryba/selektorius apdoroja ĮKELTĄ turinį (ne klausimą), nusiųsk vieną TRUMPĄ žinutę:
   „📥 Priimta: <trumpas pavadinimas> | selektorius <score> | taryba <final_action> (<n balsų>) | skill/growth: <kelias>".
   Rask kur ingest kelias baigiasi (dispatcher/processor) ir įterpk šį pranešimą (naudok esamą Telegram siuntimą,
   /root/ai_digest.env kreds). Fail-safe: jei siuntimas krenta — neblokuok. NErodyk jokių raktų.

3) TESTAS (greitas, be viso suite): perleisk council_decision ant JAU ištraukto kandidato 20260709T170609Z-ubbvs8
   (SwarmResearch, score 9.0) su nauju digest'u. Patikrink: ar dingo 413, kiek juror'ių dabar balsavo (turi būti daugiau
   nei 3), koks council verdiktas. Parodyk balsavusius su balais.

4) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai): (1) 413 pataisytas? kiek juror'ių dabar balsuoja SwarmResearch kandidatui (prieš/po), (2) ingest
ACK įjungtas? (taip), (3) „TARYBOS PATAISA BAIGTA". BE raktų.

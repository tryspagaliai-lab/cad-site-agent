UŽDUOTIS — HERA BOTUI PER-INGEST SISTEMOS ĮRAŠAS (stebėsenos kanalas). <8 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe: siuntimo klaida nelaužo ingest. NEliesk PARSER maršruto.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup.

TIKSLAS: vartotojas nori stebėti HERA sprendimus atskirame sistemos kanale (HERA botas), atskirai nuo turinio
skaitymo PARSER'yje. Kiekvienam apdorotam ingest'ui — PAPILDOMAI trumpas SISTEMOS įrašas į HERA botą
(@tryspagaliai_hera_bot per HERA_BOT_TOKEN). PARSER kelias (santrauka + user ACK) NEKEIČIAMAS.

1) Dispatcher'yje, kur baigiamas ingest (šalia PARSER ACK), PAPILDOMAI nusiųsk į HERA botą VIENĄ trumpą eilutę:
   „🧠 ingest: <trumpas title> | sel <score> | taryba <action> (<votes>) | gate: <decision/verdict jei buvo, kitaip —>"
   Viena eilutė, be transkripcijos, be santraukos (tik sistemos metrikos). Tai stebėsenos log, ne turinys.
2) JUNGIKLIS HERA_INGEST_LOG=1 (default 1; =0 išjungia). Įrašyk =1 /root/hera.env.
3) FAIL-SAFE: HERA boto siuntimas try/except — klaida NElaužo ingest, PARSER ACK vis tiek išsiunčiamas.
   Nedubliuok: PARSER gauna santrauką+user ACK; HERA botas gauna TIK šitą trumpą sistemos eilutę.
4) TESTAS: perleisk 1 kandidatą (ar sintetinį) -> patikrink, kad HERA bote atsiranda trumpa „🧠 ingest:" eilutė,
   o PARSER kelias nepakito (santrauka+ACK ten pat). Fail-safe: dirbtinė HERA-send klaida -> ingest OK.
5) DURABILUMAS: kopija į n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) per-ingest sistemos įrašas įjungtas (pavyzdys), (2) PARSER
maršrutas nepaliestas, (3) fail-safe OK, (4) „HERA STEBĖSENOS LOG ĮJUNGTAS".

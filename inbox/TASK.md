UŽDUOTIS — LENGVA saugos patikra po rc=124. GRIEŽTAI be pakibimų. <8 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe. SAUGUMAS: raktų nespausdink. Kodas -> hera-core-backup. Viešo NELIESK.

⚠️ ANTI-HANG: JOKIŲ transkripcijų/tinklo/model kvietimų kurie gali pakibti. JOKIO re-trigger. Tik lokalūs, greiti
patikrinimai. Jei kas nors reikalautų ilgo tinklo kvietimo — PRALEISK.

KONTEKSTAS: Ankstesnis diagnostikas (b292788) PAKIBO ir buvo nukirstas rc=124 (13:45) — galėjo palikti pusiau
pakeitimų. PARSER VEIKIA (link 2 oanQrXEiCy4 praėjo 13:47). Link 1 (tFTfqbBMzpE) galutinai nepavyko (3 bandymai,
nulis titrų — video be transkripcijos / apribotas). JOKIŲ rollback — pakeitimai (Memora/GPU/infra/search) veikia.

1) ŠVARUMO PATIKRA (greita, lokali): `git status` /opt/hera-processor (ir hera-core-backup darbo kopijoje) —
   ar nėra pusiau pakeistų/nesukommit'intų failų iš pakibusio b292788? Jei yra ATSITIKTINIŲ pakeitimų kurie NEbuvo
   sąmoningi (pvz. pradėtas rollback) -> atstatyk į paskutinę švarią commit'intą būseną (git checkout -- <failas>).
   Jei viskas švaru -> patvirtink „švaru".
2) BENCHMARK: hera_bench.run() -> 9/9 (0 LLM, greitas, deterministinis). Patvirtina kad niekas nesugadinta.
3) HOOK FAIL-SAFE (vienintelis leistinas pakeitimas, greitas): patvirtink kad Memora hook (dispatcher.process) ir
   GPU-filter hook apgaubti try/except — hook klaida NEGALI stabdyti ingesto. Jei kuris NĖRA -> pridėk try/except.
   Tik lokalus kodo edit, jokių kvietimų.
4) SERVISAS: `systemctl status hera-processor` — active? (greita, be tinklo). Jei ne -> restart.
5) DURABILUMAS: jei kažką taisei -> hera-core-backup (be raktų). Atmintis: „post-rc124 saugos patikra — švaru,
   PARSER OK, hooks fail-safe".

TELEGRAM (per HERA botą, trumpai): (1) git būsena po b292788: švaru / atstatyta, (2) benchmark 9/9, (3) hooks
try/except fail-safe patvirtinta, (4) servisas active, PARSER veikia (link2), (5) link 1 = video be transkripcijos
(galutinai), (6) „SAUGOS PATIKRA OK — sistema sveika, jokių rollback nereikėjo".

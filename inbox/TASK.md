UŽDUOTIS — FAZĖ 10: ASR fallback (audio→tekstas kai titrų nėra). <15 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Viešo NELIESK. SAUGUMAS: raktų nespausdink.

🚨 ANTI-HANG KRITINIS (ką tik buvo rc=124!): šis taskas liečia tinklą (yt-dlp + Groq). KIEKVIENAS tinklo/model
kvietimas su HARD timeout, JOKIO retry, jokių neribotų ciklų. Bet kuris kabinantis žingsnis -> abort + fail-safe.

0) GREITA SAUGOS PATIKRA (folded iš ankstesnės): `git status` /opt/hera-processor + hera-core-backup — jei pakibęs
   b292788 (rc=124) paliko atsitiktinių nesukommit'intų pakeitimų -> atstatyk į švarią commit'intą būseną. Benchmark
   hera_bench.run()=9/9. Servisas active. (Greita, lokalu, be tinklo.) Jei švaru — eik toliau.

1) SUKURK /opt/hera-processor/hera_asr.py — transcribe_audio(url) -> transkriptas arba None (fail-safe):
   a) yt-dlp audio-only download (bestaudio, m4a/opus) į temp. HARD timeout 90s. Dydžio cap (pvz. <=25MB; jei
      didesnis -> apkarpyk/chunk'ink arba imk pirmus ~10-15 min). Jei yt-dlp neįdiegtas -> pip install (arba naudok
      esamą). Klaida -> return None.
   b) PRIMARY: Groq Whisper API (whisper-large-v3-turbo) — POST audio, gauk transkriptą. HARD timeout 60s, NO retry.
      Groq raktas iš hera.env (necommit'ink/nespausdink). Gerbk free-tier failo limitą — jei per didelis, chunk'ink
      į segmentus (pvz. 10 min) su bendru cap (pvz. <=6 segmentai) ir sujunk; kiekvienas segmentas HARD timeout.
   c) FALLBACK: Gemini audio (jei Groq krenta/nepasiekiamas) — siųsk audio į Gemini transkripcijai. HARD timeout 60s.
   d) Visos klaidos/timeout -> return None (NIEKADA necrash'ink, ne rc124).
2) INTEGRACIJA: ingest/ekstrakcijos kelyje, TA VIETA kur dabar pasiduoda „transkripcijos gauti nepavyko" (visi
   titrų šaltiniai žlugo) -> PRIEŠ galutinį atsisakymą pakviesk hera_asr.transcribe_audio(url) kaip PASKUTINĮ
   fallback. Jei grąžina tekstą -> paduok į įprastą pipeline (Gemini struktūrizavimas → council → vault). Jei None ->
   pasiduok kaip dabar. Guard HERA_ASR=1. try/except — ASR klaida NEGALI stabdyti/kabinti ingesto.
3) DEMO (BOUNDED, kad netiltų timeout): paleisk transcribe_audio ant link 1 video (tFTfqbBMzpE — būtent tas be
   titrų) SU cap (audio <=10 min / <=25MB, HARD timeouts). Parodyk kad Groq Whisper grąžino transkriptą (bent
   dalį). Jei video ilgas ir viršija cap -> parodyk kad chunk'as veikia arba imk tik pirmą segmentą — svarbu įrodyti
   kad ASR duoda tekstą. Jei Groq nepasiekiamas per proxy -> pažymėk + bandyk Gemini fallback. NEcikluok.
4) HERA_ASR jungiklis (default 0). Po demo (jei veikia) -> gali įjungti =1 gyvai, kad būsimi be-titrų video eitų per
   ASR. Benchmark 9/9 (naujas modulis adityvus).
5) DURABILUMAS: kodas -> hera-core-backup (be raktų). ROADMAP: „Fazė 10 — ASR fallback (Groq Whisper→Gemini audio)
   ĮDIEGTA 2026-07-13; be-titrų video dabar transkribuojami iš garso; €0, HARD timeout".

TELEGRAM (per HERA botą, trumpai): (1) 0-patikra: git švaru, benchmark 9/9, (2) hera_asr.py: yt-dlp audio → Groq
Whisper (fallback Gemini audio), HARD timeouts/no-retry, HERA_ASR jungiklis, (3) integruota kaip PASKUTINIS fallback
kai titrai žlunga (fail-safe, negali kabinti ingesto), (4) DEMO ant link1 tFTfqbBMzpE: ASR grąžino transkriptą
(bent dalį), (5) „FAZĖ 10 ĮDIEGTA — be-titrų video dabar apdorojami iš garso (€0)".

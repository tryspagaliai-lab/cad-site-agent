UŽDUOTIS — FAZĖ 10 (PATAISYTA): ASR kaip PIRMINIS tikslumo šaltinis VISIEMS video, sujungtas su titrais.
<15 min. NEleisk pytest. Telegram TRUMPAI. Fail-safe €0. Kodas -> hera-core-backup. Viešo NELIESK. Raktų nespausdink.

⚠️ PATIKSLINIMAS (ankstesnė versija buvo tik fallback — KLAIDA): vartotojas nori kad ASR eitų VISADA, ne tik kai
titrai žlunga. Tikslas — kuo TIKSLESNĖ informacijos ekstrakcija: sujungti VISUS šaltinius (audio ASR + titrai +
metadata) į geriausią įmanomą įvestį extraktoriui. Whisper dažnai tikslesnis nei YouTube auto-titrai (techniniai
terminai/vardai/ne-anglų).

🚨 ANTI-HANG KRITINIS (ką tik rc=124): kiekvienas tinklo/model kvietimas HARD timeout, NO retry, jokių neribotų
ciklų. Kabinantis žingsnis -> abort + fail-safe.

0) GREITA SAUGOS PATIKRA: git status /opt/hera-processor + backup (jei pakibęs b292788 paliko pakeitimų -> atstatyk);
   benchmark 9/9; servisas active. Lokalu, be tinklo.

1) hera_asr.py — transcribe_audio(url): yt-dlp audio-only (HARD 90s, dydžio cap; ilgą chunk'ink į ~10min segmentus,
   bendras cap ~6 segmentai) → Groq Whisper (whisper-large-v3-turbo, HARD 60s/segmentui, NO retry, raktas iš
   hera.env) → grąžina transkriptą. Fallback Gemini audio jei Groq krenta. Klaida/timeout/over-budget -> None.

2) INTEGRACIJA — ASR PIRMINIS, ne fallback: video ekstrakcijos kelyje paimk ASR transkriptą VISIEMS video (guard
   HERA_ASR=1). SUJUNGIMAS geriausiam tikslumui:
   - Jei yra ir ASR, ir titrai -> paduok extraktoriui (Gemini struktūrizavimas) ASR kaip PIRMINĮ (tikslesnį), o
     titrus kaip papildomą kryžminę patikrą (arba abu, kad Gemini turėtų turtingiausią įvestį). Pažymėk metode
     „asr+titrai" ar „whisper-groq".
   - Jei tik ASR (titrų nėra) -> naudok ASR (išsprendžia be-titrų video).
   - Jei ASR nepasiekiamas/over-budget/timeout -> GRACEFUL fallback į titrus (kaip dabar), ingest NEsustoja.
   try/except visur — ASR NEGALI kabinti/stabdyti ingesto.

3) €0 BUDGET GUARD (svarbu, nes dabar ASR eina VISIEMS): dienos/rate budget cap Groq Whisper kvietimams. Pasiekus
   limitą -> tą video imk iš titrų (fail-safe), pažymėk „asr-skip-budget". Kad neišnaudotume free-tier ir nekabintume.

4) DEMO (BOUNDED): (a) link1 tFTfqbBMzpE (be titrų) -> ASR grąžina transkriptą; (b) vienas video SU titrais ->
   parodyk kad ASR+titrai sujungiami (metode matosi abu). HARD timeouts, ne cikluoti. Benchmark 9/9.

5) HERA_ASR jungiklis. Po demo — įjunk =1 gyvai (kad realiai eitų visiems). DURABILUMAS: kodas -> hera-core-backup
   (be raktų). ROADMAP: „Fazė 10 — ASR PIRMINIS tikslumo šaltinis visiems video (Groq Whisper+titrai sujungti),
   €0 budget-guard, HARD timeout, ĮDIEGTA 2026-07-13".

TELEGRAM (per HERA botą, trumpai): (1) 0-patikra: git švaru, benchmark 9/9, (2) hera_asr.py: yt-dlp→Groq Whisper
(Gemini fallback), HARD timeouts, (3) ASR PIRMINIS VISIEMS video, sujungtas su titrais tikslumui (ne tik fallback),
(4) €0 budget-guard (limitas → titrai), (5) demo: link1 be-titrų OK + titrų video sujungimas OK, benchmark 9/9,
(6) „FAZĖ 10 ĮDIEGTA — ASR+titrai sujungti VISIEMS video, kuo tikslesnė ekstrakcija (€0)".

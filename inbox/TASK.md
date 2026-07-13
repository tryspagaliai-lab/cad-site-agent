UŽDUOTIS — FAZĖ 10 (v3): Gemini PIRMINIS audio+parsingui, Whisper papildomas; VISI šaltiniai sujungti tikslumui.
<15 min. NEleisk pytest. Telegram TRUMPAI. Fail-safe €0. Kodas -> hera-core-backup. Viešo NELIESK. Raktų nespausdink.

⚠️ PATIKSLINIMAS (v2 rašė Gemini „fallback" — KLAIDA): GEMINI = geriausias parsingui ir lieka PAGRINDINIS.
Du skirtingi darbai:
 - PARSING/ekstrakcija (tekstas→struktūra): VISADA Gemini (nekeičiam — jo darbas, geriausias).
 - AUDIO (kalba→supratimas): Gemini PIRMINIS (multimodalis — transkribuoja IR supranta kontekste, geriau su
   techniniais terminais/vardais). Whisper (Groq) = PAPILDOMAS/atsarginis ASR (greitas; kryžminė patikra arba kai
   Gemini audio per kvotą/per ilgas).

TIKSLAS: kuo tikslesnė ekstrakcija VISIEMS video — sujungti visus šaltinius (Gemini-audio + titrai + Whisper).

🚨 ANTI-HANG (rc=124 ką tik): kiekvienas tinklo/model kvietimas HARD timeout, NO retry, jokių neribotų ciklų.

0) SAUGOS PATIKRA: git status /opt/hera-processor + backup (jei b292788 paliko pakeitimų -> atstatyk); benchmark 9/9;
   servisas active. Lokalu.

1) hera_asr.py (audio šaltiniai):
   - get_audio(url): yt-dlp audio-only (HARD 90s, dydžio cap; ilgą chunk'ink ~10min, cap ~6 segm.).
   - PRIMARY: Gemini audio — siųsk audio į Gemini (transkribuoja+supranta), HARD 60s/segm, NO retry, raktas hera.env.
   - PAPILDOMAS: Groq Whisper (whisper-large-v3-turbo) — greitas ASR transkriptas kryžminei patikrai / kai Gemini
     audio per kvotą ar per ilgas. HARD 60s, NO retry.
   - Klaida/timeout/over-budget -> None (fail-safe).

2) INTEGRACIJA — sujungimas VISIEMS video (guard HERA_ASR=1):
   - Surink prieinamus šaltinius: Gemini-audio (pirminis), Whisper (papildomas), titrai (jei yra).
   - Paduok GEMINI ekstraktoriui turtingiausią įvestį (Gemini-audio supratimas kaip pagrindas + titrai/Whisper kryžminei
     patikrai) -> struktūrizuota ekstrakcija (kaip dabar, Gemini). Metode pažymėk šaltinius (pvz. „gemini-audio+titrai").
   - Jei tik audio (titrų nėra) -> Gemini-audio (išsprendžia be-titrų video, kaip link1).
   - Jei Gemini-audio nepasiekiamas/over-budget -> Whisper transkriptas -> Gemini parsina; jei ir tas krenta ->
     titrai; jei nieko -> pasiduok (kaip dabar). try/except visur — NEGALI kabinti/stabdyti ingesto.

3) €0 BUDGET GUARD: dienos/rate cap Gemini-audio IR Whisper kvietimams (nes eina visiems). Pasiekus -> tas video
   iš titrų (fail-safe), pažymėk „asr-skip-budget". Kad neišnaudotume free-tier ir nekabintume.

4) DEMO (BOUNDED, HARD timeouts): (a) link1 tFTfqbBMzpE (be titrų) -> Gemini-audio grąžina turinį; (b) vienas video
   su titrais -> parodyk sujungimą (metode „gemini-audio+titrai"). Benchmark 9/9.

5) HERA_ASR jungiklis; po demo įjunk =1 gyvai. DURABILUMAS: kodas -> hera-core-backup (be raktų).
   ROADMAP: „Fazė 10 — Gemini pirminis audio+parsing, Whisper papildomas, visi šaltiniai sujungti; €0 budget-guard;
   ĮDIEGTA 2026-07-13".

TELEGRAM (per HERA botą, trumpai): (1) 0-patikra: git švaru, benchmark 9/9, (2) GEMINI pirminis audio+parsingui
(multimodalis), Whisper papildomas/atsarginis ASR, (3) visi šaltiniai (Gemini-audio+titrai+Whisper) sujungti kuo
tikslesnei ekstrakcijai VISIEMS video, (4) €0 budget-guard, HARD timeouts, (5) demo: link1 be-titrų OK + sujungimas
OK, (6) „FAZĖ 10 ĮDIEGTA — Gemini pirminis, visi šaltiniai sujungti, tikslesnė ekstrakcija (€0)".

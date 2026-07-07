UŽDUOTIS — YouTube ekstrakcijos fix (subtitrai pirmiausia) + nepavykusių job'ų re-drive.
Autonomiškai. NELIESK veikiančių Fazės 2–5 kitų dalių — tik pataisyk youtube kelią. Nemokama (Gemini free).
Atsiskaityk į Telegram TRUMPAI, aiškiu galutiniu statusu.

Problema: yt-dlp VPS IP užblokuotas + Gemini-native ilgiems/keliems youtube griūva (503/tuščia) → job'ai
dead-letter'inami („po 3 bandymų atsisakau").

1) PRIMARY youtube kelias = **subtitrai**. Įdiek `youtube-transcript-api` (pip į hera venv). YouTube video
   ekstrakcijai PIRMIAUSIA bandyk paimti gatavus subtitrus (bet kuri kalba; prioritetas originalas/en/lt;
   jei tik auto-generated — imk juos) → full.md iš transkripto. Greita, be atsisiuntimo, be Gemini transkripcijos.
   - Jei subtitrų NĖRA arba transcript-api irgi blokuojamas iš VPS IP → FALLBACK į esamą Gemini-native (kaip dabar).
   - Ištestuok ant kelių realių URL; parodyk, ar transcript-api veikia iš VPS IP (jei blokuota — pranešk, spręsim proxy).

2) RE-DRIVE: surask dead-letter'intus / nepavykusius youtube job'us (pvz. 20260707T191953Z-tv60mf ir kiti)
   → paleisk juos iš naujo per NAUJĄ subtitrų kelią. Neliesk jau sėkmingai apdorotų (pvz. chw25r).
   Parodyk, kiek atgaivinta / kiek dar nepavyko.

3) Po apdorojimo — HERA selektorius + trajektorijos + (jei tinka) skill/growth kaip įprasta.

4) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk (nėra creds).

Į Telegram: ar transcript-api veikia iš VPS, kiek youtube job'ų atgaivinta/apdorota, kiek liko,
ir aiškiai „YOUTUBE FIX BAIGTAS" arba ko trūksta.

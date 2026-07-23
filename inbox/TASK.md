UŽDUOTIS — YouTube ingest guardas: `/post/` community postai → fail-fast (NE video). <12 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM, BE tinklo). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme. Secret'us NEliesk.

KONTEKSTAS: du kartus krito ingest'as (id w1w1vb 14:10, hpjasd 20:06) tam pačiam URL:
`youtube.com/post/UgkxcCM-LQe91DLmzIn6TNJRoBY0u40rsBXC` — tai YouTube COMMUNITY POSTAS (bendruomenės įrašas), NE video.
Video-transkripcijos vamzdynas (titrai + ASR iš garso) neturi ko transkribuoti → degina 3 retry ciklus × 5 šaltinius veltui.
TIKSLAS: atpažinti community-post/tab URL PRIEŠ vamzdyną ir grąžinti aiškią žinutę, nedeginant retry.

1) SURASK YouTube ingest įėjimo tašką (deterministiškai, grep):
   - `grep -rn -E "transcript-api|Piped|Invidios|Invidious|video_metadata|kind.*youtube|def .*transcri" /root /opt/hera-processor 2>/dev/null` — rask failą/funkciją kuri paima YouTube URL ir bando titrus/ASR.
   - Nustatyk kur URL pirmą kartą gaunamas PRIEŠ pradedant 5 šaltinius. Ten dėsim guardą (kuo anksčiau).

2) BACKUP prieš keitimą: `cp <tas_failas> /opt/hera-processor/backup_<vardas>.$(data +%s)` (arba /root/hera-core-backup/). Būtinai backup.

3) ĮDĖK GUARDĄ (determ., be tinklo — tik URL string analizė):
   - Funkcija/patikra: jei YouTube URL kelias yra community-tab turinys → NEeik į transkripciją, grąžink kontroliuojamą „nepalaikoma" statusą su aiškia priežastimi.
   - ATPAŽINIMO TAISYKLĖ (tik string, be tinklo): URL (po normalizacijos, be query) atitinka BET KURĮ:
       * kelyje yra `/post/`  (pvz. youtube.com/post/Ugkx...)
       * kelias baigiasi `/community` arba turi `/community?`
     → tai community postas. (NELIESK `/watch`, `youtu.be/`, `/shorts/`, `/live/`, `/embed/`, `/playlist` — tie realūs video/leistini.)
   - Elgesys kai atpažinta: grąžink status="unsupported" (arba analogišką esamą „skip/refuse" kelią, kokį naudoja pipeline), su žinute LT:
     „YouTube community postas (ne video) — transkripcijos nėra. Įklijuok posto tekstą ranka, jei nori jį įtraukti."
     SVARBU: tai NE 3-retry klaida — grąžink IŠ KARTO (fail-fast), be retry, be tinklo užklausų. Jei pipeline turi „permanent-skip" vs „retry" skirtį — naudok permanent-skip (kaip privatus/negalimas), kad NEbūtų 3 bandymų.
   - Jei nesi tikras kur tiksliai grąžinti statusą — dėk guardą kuo arčiau įėjimo ir grąžink tą patį tipą kaip esamas „video privatus/negalimas → atsisakau" kelias (permanent, ne retry). NElaušk esamo video srauto.

4) SELFTEST (`--selftest` arba mažas inline testas, BE pytest, BE tinklo):
   (a) `youtube.com/post/UgkxcCM-LQe91DLmzIn6TNJRoBY0u40rsBXC` → guardas suveikia, grąžina unsupported/skip, žinutė yra, JOKIO transkripcijos šaltinio nepaleista (0 tinklo).
   (b) `youtube.com/watch?v=dQw4w9WgXcQ` → guardas NEsuveikia (praeina toliau į normalų srautą; NEreikia realiai transkribuoti — tik patikrink kad guardas grąžina „ne-postas/tęsk").
   (c) `youtu.be/dQw4w9WgXcQ` ir `youtube.com/shorts/abc123` → guardas NEsuveikia (praeina).
   (d) `youtube.com/channel/UCxxxx/community` → guardas suveikia (community tab).
   Spausdink PASS/FAIL kiekvienam.

5) BACKUP kodo į /opt/hera-processor/ (ar /root/hera-core-backup/) + jei tai trackinamas HERA repo (NE viešas cad-site-agent) — commit/push. Vault ROADMAP.md 1 eilutė:
   „YouTube ingest guardas: /post/ + /community → fail-fast permanent-skip (ne video), determ., €0 — ĮDIEGTA <data>."

ATASKAITA (HERA botas, trumpai): kuris failas/funkcija; kur įdėtas guardas; backup padarytas?; selftest a/b/c/d PASS/FAIL (ypač a: 0 transkripcijos šaltinių paleista; b/c: video srautas nepaliestas); ROADMAP. Jei STOP/neradai įėjimo taško — kodėl + ką radai grep'e.

UŽDUOTIS — Fazė 27: verifikavimo ciklas (rubrika + vertintojas + suspaustas pakartojimas). MODULIS, be integracijos. <14 min.

## Tikslas
Iš kuruoto LangChain „Art of Loop Engineering": HERA turi Ciklus 1, 3, 4, bet **Ciklas 2 (verifikavimo) uždarytas tik
per pusę**. Turim daug vertintojų (validator, eval, faithfulness, goalanchor, loopguard, diffrules) — bet VISI ADVISORY:
anotuoja ataskaitą, ir **niekas negrįžta atgal į agentą pataisymui**. Simptomas: 2026-07-26 GoalAnchor pranešė `drift`
ir nieko neįvyko.
Sukurk modulį, kuris duoda tris trūkstamus gabalus: **rubriką**, **vertinimą pagal ją**, ir **suspaustą pakartojimo
užklausą**, jei kriterijai netenkinami.

## 🔴 Kertinis konfliktas, kurį PRIVALAI gerbti
HERA nekintantis principas: **„HARD timeout, NO retry (anti rc=124)"**. Jis mus jau gelbėjo (semsearch užduotis nukirsta
per timeout, be žalos). Ciklas 2 pagal apibrėžimą reiškia pakartojimą. Tai NE draudimas, bet reikalauja trijų dalykų kartu:
1. **MAX 1 pakartojimas** (ne ciklas, ne `while`) — griežtai.
2. **Laiko biudžetas VISAI grandinei**, ne kiekvienam bandymui — kad du bandymai neviršytų to paties lango kaip vienas.
3. **Užklausos suspaudimas pakartojime:** perduoti TIK dabartinę artefakto būseną + rubrikos kriterijus, kurie NEĮVYKDYTI.
   **NE ilgą klaidų istoriją** (tai „context rot" sprendimas iš to paties šaltinio; dera su `hera_ctxtrim` Fazė 20).
Jei kuris nors iš trijų neįgyvendinamas — geriau grąžink mažiau funkcijų, bet NEpažeisk principo.

## Realybė (ko pats neišvestum)
- **Rubrika jau egzistuoja neformaliai:** nuo 2026-07-26 kiekvienas `inbox/TASK.md` turi skiltį **„Įrodymai (ko tikiuosi
  ataskaitoje)"** — tai IR YRA rubrika, tik neišparsinta. Naudok TĄ, nekurk naujo formato. Šis pats failas yra pavyzdys.
- Modulių konvencija: `/root/hera_<vardas>.py`, `HERA_<VARDAS>` def 0, savas `--selftest` (BE pytest), fail-safe,
  backup → `/opt/hera-processor/` + push į privatų `hera-core-backup`, ROADMAP.md eilutė.
- Gretimi moduliai, su kuriais NEDUBLIUOK: `hera_validator` (prieš-darbo proof), `hera_eval` (promocijos vartai),
  `hera_goalanchor` (drift/injection), `hera_ctxtrim` (didelė išvestis→failas). Šis — apie **užduoties kriterijų
  įvykdymą po darbo** ir grįžtamąjį ryšį.
- Vertinimas turi būti kiek įmanoma **deterministinis** (ar kriterijus paminėtas/įvykdytas išvestyje). Jei kuriam nors
  kriterijui reikia sprendimo, kurio determ. būdu nepadarysi — pažymėk `undecided`, NEspėk. €0 LLM vertintojas = vėliau.

## Apribojimai
€0, be tinklo, be LLM. Fail-safe (klaida → „praeita", niekada neblokuoti, niekada necrashinti). Def 0 semantiką
pasirink ir PAGRĮSK (žr. Fazės 26 precedentą — ten def0=advisory buvo pagrįstas matomumu).
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. **Runner'io ir cron NELIESK — integracija yra ATSKIRAS
human-gate žingsnis, ne šis.** Secret'us NEliesk. BACKUP prieš keitimą.

## Įrodymai (selftest, be pytest, be tinklo)
1. **Rubrikos išparsinimas:** paduodi realų `TASK.md` tekstą (naudok šitą patį failą) → ištraukia „Įrodymai" kriterijus
   kaip atskirus punktus. Parodyk, ką ištraukė.
2. **Praeina:** išvestis, adresuojanti visus kriterijus → `pass`, jokio pakartojimo.
3. **Nepraeina:** išvestis, praleidžianti 2 kriterijus → `fail`, ir sugeneruota pakartojimo užklausa mini **TIK tuos 2**,
   o ne visus. Parodyk sugeneruotą tekstą.
4. **Suspaudimas įrodytas skaičiais:** pakartojimo užklausa turi būti **žymiai trumpesnė** nei originalus TASK.md +
   pilna išvestis. Pateik simbolių skaičius prieš/po.
5. **MAX 1:** po vieno pakartojimo — sustoja, nesvarbu ar pavyko. Įrodyk, kad `while` nėra.
6. **Neaiškus kriterijus** → `undecided`, ne klaidingas `pass`.
7. **Fail-safe:** tuščias/sugadintas TASK.md, ne-string įvestis → „praeita", be crash.
8. BACKUP + push; ROADMAP.md eilutė.

Ataskaitoje pasakyk, kur modulis būtų kviečiamas realiai (bet NEINTEGRUOK) ir kokia liko neaprėpta dalis.
Jei STOP — kodėl.

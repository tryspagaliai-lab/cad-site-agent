UŽDUOTIS — Higiena + root-fix: uždaryk 5 trafilatura klausimus + STABDYK jų kartojimąsi + n=1 slopinimas +
dangling valymas. <15 min. NEleisk pytest. Telegram TRUMPAI. Fail-safe €0. Kodas -> hera-core-backup.
Vault -> hera-vault. Viešo NELIESK. Necommit'ink raktų. PRIORITETAS: 1 ir 2 privalo užbaigti; 3,4 jei lieka laiko.

KONTEKSTAS: OPEN_QUESTIONS turi 5 dublikatus „ar vertas kandidatas trafilatura?" — trafilatura yra MŪSŲ pačių
ekstrakcijos biblioteka (ne žinių kandidatas), kuri logInama kaip kandidatas per kiekvieną ingestą. Uždaryti
neužtenka — reikia sustabdyti šaltinį.

1) UŽDARYK 5 klausimus OPEN_QUESTIONS.md (pagal raktą, `- [ ]`→`- [x]` + sufiksas
   „→ UŽDARYTA (human-gate: vartotojas 2026-07-13): infra ekstrakcijos biblioteka, jau integruota, ne žinių
   kandidatas"):
   cd41f4614b76, 7625103523c9, 61f7ca4d78b7, ac8f6bf0c051, 9b728386687c. (Jei rakto neranda — praleisk, pažymėk.)

2) ROOT-FIX (kodas, deterministinis): kandidatų/atvirų-klausimų generavime pridėk INFRA-EXCLUSION sąrašą — HERA
   pačios pipeline įrankių/bibliotekų vardai NElaikomi žinių kandidatais ir NEgeneruoja council balsavimo/atviro
   klausimo. Minimaliai įtrauk: „trafilatura" (patvirtintas kaltininkas). Pridėk kelis akivaizdžius mūsų pipeline
   infra terminus jei aiškūs (pvz. „playwright", „gemini-titrai", „ddgs", „searxng") — TIK jei tikrai mūsų įrankiai,
   ne turinys. Konservatyviai (tikslus vardų match). Fail-safe. Kur šis kodas gyvena (selector/council/open-question
   hook) — ten ir prideda. Necommit'ink raktų.

3) n=1 SLOPINIMAS: Loop B raporte „silpnų sričių" įspėjimus rodyk TIK jei n>=2 (n=1 per triukšmingas, statistiškai
   bereikšmis). Maža pataisa reporting'e. Neliesk skaičiavimo logikos, tik rodymo slenkstį.

4) DANGLING valymas: paleisk hera_wikilink.py/lint — dangling (7) sumažink konservatyviai (jei aišku — pataisyk
   nuorodą ar pašalink negyvą; NEkurk klaidingų puslapių). Parodyk dangling prieš/po. Jei abejotina — palik +
   raportuok.

BENCHMARK: hera_bench.run() -> 9/9 (kodo pakeitimai neturi gadinti). TRAJEKTORIJA: įrašyk (curation/hygiene+rootfix).
DURABILUMAS: kodas -> hera-core-backup; OPEN_QUESTIONS + wiki -> hera-vault. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) 5 trafilatura klausimai uždaryti, (2) ROOT-FIX: infra-exclusion (trafilatura
+ ...) — nebegeneruos atvirų klausimų, (3) n=1 slopinimas Loop B raporte, (4) dangling X→Y, benchmark 9/9,
(5) „HIGIENA + ROOT-FIX ATLIKTA — trafilatura triukšmas sustabdytas prie šaknies".

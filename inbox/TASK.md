UŽDUOTIS — DURABILUMAS: HERA kodo backup į PRIVATŲ GitHub repo (naudok VPS esamą tokeną). Atsargiai.
Tikslas: apsaugoti visą HERA kodą+skills, kad VPS mirtis nereikštų viską prarasti. Atsiskaityk į Telegram TRUMPAI.

SAUGUMAS (KRITIŠKA):
- VPS origin remote turi įmontuotą GitHub tokeną. NIEKADA jo nespausdink, nerodyk Telegram/log, neįrašyk į failą.
  Tokeną gauk tik programiškai: `git -C /opt/cad-site-agent remote get-url origin`. Prieš siųsdamas bet ką į
  Telegram — perfiltruok output'ą kad jokia `ghp_`/`github_pat_`/token reikšmė nepatektų.
- PRIEŠ commit'inant — patikrink kad backup'inamame kode NĖRA raktų/paslapčių:
  grep -rInE '(sk-[A-Za-z0-9]|gsk_[A-Za-z0-9]|nvapi-[A-Za-z0-9]|tp-[A-Za-z0-9]|AIza[A-Za-z0-9]|ghp_|github_pat_|xox[bp]-)' <backup dirs>.
  Jei RANDA tikrą raktą — NUTRAUK, NEcommit'ink, raportuok kur rado (be reikšmės). .env failų NEIMK niekada.

ŽINGSNIAI:
1) TOKENAS + SCOPE TESTAS: iš origin URL ištrauk tokeną (nespausdink). Pabandyk sukurti PRIVATŲ repo per API:
   curl -s -o /dev/null -w '%{http_code}' -H "Authorization: token <TOKEN>" -H "Accept: application/vnd.github+json" \
     https://api.github.com/user/repos -d '{"name":"hera-core-backup","private":true,"description":"HERA core backup (VPS durability)"}'
   - 201 = sukurta. 422 = jau egzistuoja (gerai). 403/404 = tokenas neturi teisės kurti repo -> NUTRAUK ir raportuok
     "tokenas be repo-create scope" (tada spręsim: naujas tokenas arba viešas repo). NErodyk tokeno.

2) JEI repo yra: sustatyk backup staging katalogą (pvz /tmp/hera-backup), į jį nukopijuok:
   - /opt/hera-processor/ VISĄ kodą (*.py, konfigai) — BE __pycache__, BE *.env, BE .git;
   - HERA vault distiliuotą vertę: skills/ (SKILL.md), growth/, proposals/ (įsk. proposals/council) — jei egzistuoja
     (rask kelią, pvz /opt/hera-vault/); NEIMK didelių žalių media/extracted binarų (tik .md/.json/.jsonl tekstą,
     apribok kad repo nebūtų milžiniškas).
   - trumpą README.md: kas tai, kaip atkurti (servisai hera-ingest/hera-processor, env iš /root/hera.env — NElaikomas čia).
   Pridėk .gitignore: `*.env`, `__pycache__/`, `*.pyc`, stambūs binarai.

3) git init staging'e, git add, commit "HERA core backup <data>", push į hera-core-backup (main) su tokenu iš origin
   (susikonstruok push URL pakeisdamas repo vardą origin URL'e; tokeno nespausdink). Force NEDARYK (naujas repo).

4) Raportuok Telegram (BE tokeno, BE raktų): repo sukurtas/egzistuoja (taip), kiek failų + apytikslis dydis
   nustumta, ar secret-scan švarus, ir aiškiai „HERA BACKUP PADARYTAS: github.com/tryspagaliai-lab/hera-core-backup (privatus)".
   Jei kur nutrūko (scope/secret) — aiškiai kodėl.

GREIČIO: tai git operacijos, ne modelių kvietimai — turi būti greita (<5 min). Jei kopijuojant vault randi GB dydžio
duomenų — apribok tik tekstiniais artefaktais ir raportuok kad žali media praleisti.

UŽDUOTIS — DURABILUMAS: HERA kodo backup į PRIVATŲ GitHub repo. Dabar yra GITHUB_TOKEN /root/hera.env. Atsargiai.
Tikslas: sukurti privatų repo ir nustumti visą HERA kodą+skills, kad VPS mirtis nereikštų viską prarasti.
Atsiskaityk į Telegram TRUMPAI, BE tokeno/raktų.

SAUGUMAS (KRITIŠKA):
- Tokeną skaityk TIK iš os.environ GITHUB_TOKEN (per hera_env self-load iš /root/hera.env). NIEKADA jo
  nespausdink, nerodyk Telegram/log/chate, neįrašyk į failą ar git config plaintext. Prieš siųsdamas ką nors į
  Telegram — perfiltruok kad jokia `ghp_`/`github_pat_` reikšmė nepatektų.
- PRIEŠ commit'inant — secret-scan backup'inamą kodą:
  grep -rInE '(sk-[A-Za-z0-9]{10}|gsk_[A-Za-z0-9]|nvapi-[A-Za-z0-9]|tp-[A-Za-z0-9]{6}|AIza[A-Za-z0-9]|ghp_[A-Za-z0-9]|github_pat_|xox[bp]-)' <backup dirs>
  Jei RANDA tikrą raktą/tokeną — NUTRAUK, NEcommit'ink, raportuok kur (be reikšmės). .env failų NEIMK NIEKADA.

ŽINGSNIAI:
1) SCOPE TESTAS: su GITHUB_TOKEN sukurk PRIVATŲ repo per API (User-Agent header būtinas):
   curl -s -w '\n%{http_code}' -H "Authorization: token $GITHUB_TOKEN" -H "User-Agent: hera-backup" \
     -H "Accept: application/vnd.github+json" https://api.github.com/user/repos \
     -d '{"name":"hera-core-backup","private":true,"description":"HERA core backup (VPS durability)"}'
   - 201 = sukurta. 422 = jau yra (gerai). 401/403 = tokenas be teisės -> NUTRAUK, raportuok "tokenas be repo scope"
     (be reikšmės). Nustatyk repo pilną vardą (owner/hera-core-backup) iš atsakymo arba /user.

2) STAGING (/tmp/hera-backup, švarus): nukopijuok:
   - /opt/hera-processor/ VISĄ kodą (*.py, extractors/, konfigai) — BE __pycache__, *.pyc, *.env, .git;
   - /opt/hera-ingest/worker.py (jei yra);
   - vault distiliatas (rask kelią, pvz /opt/hera-vault/): skills/ (SKILL.md), growth/ (*.md), proposals/ (įsk.
     proposals/council/*.json) — TIK .md/.json/.jsonl tekstas; NEIMK work/ , extracted/ žalių/binarų/didelių media.
   - README.md: kas tai, servisai (hera-ingest/hera-processor), env laikomas /root/hera.env (NE čia), kaip atkurti.
   - .gitignore: *.env, __pycache__/, *.pyc, work/, extracted/, *.mp4, *.zip, dideli binarai.

3) git init, add, commit "HERA core backup <data ISO>", push į privatų repo (main). Push URL su tokenu iš env
   (https://x-access-token:$GITHUB_TOKEN@github.com/OWNER/hera-core-backup.git) — tokeno NEspausdink, NEpalik
   git config remote plaintext (naudok ephemeral push URL, po push pašalink remote arba naudok `git push <url>`).

4) TELEGRAM (be tokeno/raktų): repo (privatus) sukurtas/egzistuoja, kiek failų + apytikslis dydis nustumta,
   secret-scan švarus (taip/ne), ir aiškiai „HERA BACKUP PADARYTAS: <owner>/hera-core-backup (privatus)".
   Jei nutrūko (scope/secret) — kodėl.

GREIČIO: git operacijos, ne modeliai — <5 min. Jei vault didelis — tik tekstiniai artefaktai, žali media praleisti.

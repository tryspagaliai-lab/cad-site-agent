UŽDUOTIS — KODO BACKUP PUSH Į hera-core-backup (VIENA SIAURA UŽDUOTIS). <8 min.
NEleisk pytest, HERA kodo NEkeisk — tik backup. Telegram TRUMPAI.

SAUGUMAS: tokeno niekur nespausdink; push TIK į PRIVATŲ repo. Naudok tą patį GIT_ASKPASS metodą kaip
hera-vault sync'e (/usr/local/bin/hera_git_askpass.sh) — tokenas į .git/config NIEKADA nepatenka.

KONTEKSTAS: GITHUB_TOKEN dabar su repo scope. Susikaupę nepush'inti pakeitimai: normatyviniai skill'ai
(hera_select/hera_skill/hera_query + test_docbound), NapMem naršymo kilpa (hera_nav.py, hera_query.py).

1) Patikrink ar privatus repo tryspagaliai-lab/hera-core-backup egzistuoja (dabar tokenas jį matys).
   Jei NĖRA — sukurk PRIVATŲ per POST /user/repos (tryspagaliai-lab yra USER paskyra, žinom iš vault-sync).
2) SECRET-SCAN /opt/hera-processor/ kodo (raktų pattern'ai) — radus, išvalyk prieš push.
3) Push'ink VISĄ dabartinį HERA kodą (/opt/hera-processor/ turinį; jei backup'e jau yra istorija — commit ant
   viršaus su žinute apie tai kas naujo: docbound skills + nav loop + timeout fix).
4) Įsitikink kad remote HEAD atsinaujino (kaip vault-sync teste).

TELEGRAM (trumpai, be raktų): (1) repo egzistavo ar sukurtas, (2) secret-scan švarus?, (3) push OK + kiek failų/
commit'ų, (4) „CODE-BACKUP BAIGTA".

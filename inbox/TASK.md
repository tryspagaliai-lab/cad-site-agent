UŽDUOTIS — PUSH'INTI hera_research.py Į PRIVATŲ hera-core-backup (backup spraga). <8 min.
NEleisk pytest. Telegram TRUMPAI.

SAUGUMAS: tokeno NIEKUR nespausdink; į .git/config NEĮrašyk atviru tekstu — naudok GIT_ASKPASS.

PROBLEMA: 3 fazės hera_research.py commit'intas lokaliai hera-core-backup repo VPS'e, bet PUSH NEĮVYKO —
agentas nerado /usr/local/bin/hera_git_askpass.sh. Reikia push'inti (durabilumas).

1) PATIKRINK/ATKURK askpass helper'į: ar /usr/local/bin/hera_git_askpass.sh egzistuoja (chmod 700)? Jei NĖRA —
   atkurk jį (source'ina GITHUB_TOKEN iš /root/hera.env ir grąžina jį kaip slaptažodį git'ui; kaip ankstesniuose
   sėkminguose push'uose į hera-vault/hera-core-backup). NEspausdink tokeno.
2) Įsitikink, kad hera-core-backup lokalus repo turi VISUS naujausius pakeitimus: hera_research.py + bet ką iš
   3 fazės (jei dar necommit'inta — commit su aiškia žinute). SECRET-SCAN prieš push (sk-/gsk_/ghp_/nvapi-/AIza/
   token=) — radus, išvalyk.
3) PUSH į privatų hera-core-backup su GIT_ASKPASS (URL be tokeno). Patikrink: local HEAD == origin/main.
4) Įsitikink, kad ir kiti neseniai pakeisti /opt/hera-processor failai (hera_search.py, SearXNG wrapper) yra
   backup'e — jei ne, įtrauk.

TELEGRAM (trumpai, be raktų): (1) askpass rastas/atkurtas, (2) push OK — local==origin, kiek failų/commit,
(3) secret-scan švarus, (4) „RESEARCH BACKUP PUSH'INTAS".

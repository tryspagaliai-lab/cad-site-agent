UŽDUOTIS — VAULT SYNC Į GITHUB (VIENA SIAURA UŽDUOTIS, BE KODO KEITIMO HERA'OJE). <10 min.
GITHUB_TOKEN /root/hera.env KĄ TIK ATNAUJINTAS (scope: repo) — dabar veiks. NEleisk pytest. Telegram TRUMPAI.

SAUGUMAS: tokeno NIEKUR nespausdink (nei komandose su echo, nei loguose). Repo — TIK PRIVATUS.

1) Sukurk PRIVATŲ repo tryspagaliai-lab/hera-vault per GitHub API (token iš /root/hera.env).
   Jei org'e kurti neleidžia — kurk useryje ir pažymėk ataskaitoje kur sukūrei.
2) /opt/hera-vault: git init (jei dar ne), .gitignore — didelius binarinius ingest/ šiukšlių failus ignoruok
   savo nuožiūra, bet growth/, skills/, extracted/, proposals/, trajectories/ PRIVALO sync'intis.
3) SECRET-SCAN prieš pirmą push: grep -rE 'sk-|gsk_|ghp_|nvapi-|AIza|api[_-]?key' /opt/hera-vault --include='*' -l
   (ir pan.) — radus, failą išvalyk arba į .gitignore, pažymėk ataskaitoje ką radai (be pačių reikšmių!).
4) Pirmas commit + push (remote per https su tokenu iš env; token į .git/config NEĮRAŠYK atviru tekstu —
   naudok credential helper arba store'ink URL be tokeno ir push'ink su askpass/env).
5) Auto-sync: /usr/local/bin/hera_vault_sync.sh + cron kas 30 min (flock kaip runner'yje): jei yra pakeitimų ->
   add+commit (žinutė su data) + push. Paleisk kartą ranka — įsitikink kad veikia.
6) Trumpa šalutinė patikra (1 eilutė ataskaitoje): ar NapMem-A atstatymas (naršymo kilpa, HERA_NAV) buvo
   įvykdytas anksčiau — taip/ne (failų/env požymiai; pačios užduoties NEDARYK).

TELEGRAM (trumpai, be raktų): (1) repo URL (be tokeno) + privatus?, (2) secret-scan švarus / kas ignoruota,
(3) pirmas push OK, kiek failų, (4) cron sync įjungtas + rankinis testas OK, (5) NapMem-A anksčiau įvykdyta
taip/ne, (6) „VAULT-SYNC BAIGTA".

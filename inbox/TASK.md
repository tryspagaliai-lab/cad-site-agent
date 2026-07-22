UŽDUOTIS — patvirtinti kad vault push su nauju token'u vėl veikia (403 dingo?). <6 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK. Secret'us redaguok.
Vienintelis write = vault heartbeat state failas + normalus sync push.

KONTEKSTAS: PAT teisės GitHub'e ką tik pataisytos (All repositories + Contents: Read and write). Token'o reikšmė VPS'e
NEPAKEISTA — tik GitHub-side teisės. Reikia patvirtinti kad hera-vault push nebe 403.

ŽINGSNIAI:
1) Heartbeat: `date -u +%FT%TZ > /opt/hera-vault/state/token_rotation_check.txt`.
2) Paleisk sync: `bash /usr/local/bin/hera_vault_sync.sh; echo "rc=$?"`.
3) Log: `tail -5 /var/log/hera_vault_sync.log`.
4) Būsena: `git -C /opt/hera-vault rev-list --left-right --count HEAD...origin/main 2>&1` (po pull-rebase; tikimasi „0 0" jei push OK).
   Jei log rodo „PUSH OK" IR left/right = 0 0 → SĖKMĖ (403 dingo, backlog išpush'intas).
   Jei „403" ar „Authentication failed" → token teisės dar ne iki galo (arba org approval reikia); pranešk tikslią klaidą.

ATASKAITA (HERA botas, trumpai): sync rc; log paskutinės eilutės (PUSH OK / 403 / kita); ahead/behind (0 0 = švaru); IŠVADA: vault push veikia taip/ne.

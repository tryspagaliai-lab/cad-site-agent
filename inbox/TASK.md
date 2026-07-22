UŽDUOTIS — (A) patvirtinti GitHub token rotaciją (runner fetch + vault push) + (B) n8n UI-auth patikra. <9 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK. Secret'us redaguok.
Vienintelis leidžiamas write = vault heartbeat state failas (B dalis — tik read).

=== (A) TOKEN ROTACIJOS PATVIRTINIMAS ===
1) Runner repo fetch: `git -C /opt/cad-site-agent fetch origin claude/authorize-claude-code-vps-1dcvrv 2>&1 | tail -3`
   → jei nėra „Authentication failed"/„fatal" = OK. (Tai, kad skaitai šią užduotį, jau reiškia fetch veikia — bet patvirtink eksplicitiškai.)
2) Vault push test su nauju token'u (per esamą sync mechanizmą):
   `date -u +%FT%TZ > /opt/hera-vault/state/token_rotation_check.txt`
   `bash /usr/local/bin/hera_vault_sync.sh; tail -4 /var/log/hera_vault_sync.log`
   → tikimasi „PUSH OK". Jei „Authentication failed" ar „PUSH nepavyko" dėl auth → vault kelyje token neatnaujintas, PRANEŠK (STOP B daliai nebūtina).

=== (B) n8n UI-AUTH (read-only, be login, be account kūrimo) ===
3) `BASE=$(docker exec n8n-n8n-1 printenv WEBHOOK_URL 2>/dev/null | tr -d '\r' | sed 's:/*$::')`; echo "BASE=$BASE" (jei tuščia — N8N_EDITOR_BASE_URL).
4) `curl -s --max-time 10 "$BASE/rest/settings" | grep -oE '"showSetupOnFirstLoad":[a-z]*'`
   → true = owner NESUKURTAS (KRITIŠKA); false = owner yra (gerai).
5) `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 "$BASE/rest/workflows"` (be auth → 401 tikimasi; 200 = ATVIRA!).
6) `curl -s -o /dev/null -w "root=%{http_code} redir=%{redirect_url}\n" --max-time 10 "$BASE/"`.

ATASKAITA (HERA botas, trumpai): (A) runner fetch OK/auth-fail; vault PUSH OK/auth-fail;
(B) showSetupOnFirstLoad true|false; /rest/workflows kodas (401=saugu/200=atvira); / kodas+redirect. IŠVADA.

UŽDUOTIS — perkrauti n8n konteinerį, kad įsigaliotų 3 MCP endpoint'ų deaktyvavimas. <8 min.
NEleisk pytest. Fail-safe: jei ABEJOJI ar kažkas ne taip — STOP ir reportuok, NIEKO neperkrauk. €0. Ataskaita TIK į HERA botą.
Viešo cad-site-agent NELIESK. hera-vault NELIESK (tik jei nori įrašyti session-log — neprivaloma).

KONTEKSTAS: 3 n8n MCP trigger'iai (MCP Universal Router /desk, Claude VPS Shell zzVpsShellMcp01, Claude VPS Control
jij5EQGypNkPsHgh) buvo atviri internete be auth. JAU deaktyvuoti DB'je (active=false), BET veikianti n8n instancija
laiko webhook'us atmintyje kol nebus RESTART. Ši užduotis: saugiai perkrauti n8n konteinerį, kad skylė faktiškai užsidarytų.
Tu veiki HOST'e kaip root su docker prieiga. n8n konteineris ≈ ID 1688a40d274f (patikrink dinamiškai, gali keistis).

ŽINGSNIAI:
1) RASK n8n konteinerį: `docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}' | grep -i n8n`.
   Jei nerasta ARBA randama >1 kandidatas neaiškiai — STOP, reportuok ką matai, NIEKO nedaryk.
2) PRIEŠ restart — patvirtink DB būseną (read-only): `docker exec <ID> n8n export:workflow --all --output=/tmp/a.json`
   tada patikrink 3 MCP workflow'ų active reikšmes (pvz. per `docker exec <ID> node -e` arba grep). VISI 3 turi būti
   active=false. Jei bent vienas active=true — STOP, reportuok (kažkas atsuko atgal), NEperkrauk.
3) RESTART: `docker restart <ID>`. Pal’auk kol pakyla: iki ~40s cikle tikrink `docker ps --filter id=<ID> --format '{{.Status}}'`
   kol rodo „Up".
4) PO restart — patvirtink kad n8n gyvas (Status „Up") IR kad 3 workflow'ai liko active=false (dar kartą export-check
   iš konteinerio). 
5) ENDPOINT test (best-effort, neprivalomas jei URL nerasta): rask cloudflared public URL host'e
   (`systemctl cat cloudflared 2>/dev/null` ARBA `cat ~/.cloudflared/*.yml /etc/cloudflared/*.yml 2>/dev/null` ARBA
   `ps aux | grep -i cloudflared | grep -v grep`). Jei radai URL — `curl -s -o /dev/null -w "%{http_code}" <URL>/desk`
   → tikimasi NE 200 (uždaryta; 404/000/502 ok). URL PATĮ užrašyk ataskaitoj (ne į git). Jei URL nerasta — praleisk, pažymėk.
6) NErotuok raktų (tai vartotojo darbas per konsoles). NEliesk kitų workflow'ų (Link Parser ir kt. lai lieka kaip yra).

ATASKAITA (HERA botas, trumpai): konteineris (ID/name/image); prieš-restart 3×active; restart OK + „Up"; po-restart 3×active;
endpoint curl kodas (arba „URL nerasta"); ar viskas švaru. Jei kur STOP — kodėl.

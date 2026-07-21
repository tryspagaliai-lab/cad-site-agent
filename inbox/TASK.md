UŽDUOTIS — READ-ONLY patikra: ar n8n :5678 (ir UI/API) tiesiogiai atviras internete? NIEKO NEKEISK. <8 min.
NEleisk pytest. Fail-safe. €0. TIK skaitymas — jokio firewall/port/config keitimo, jokio restart. Ataskaita TIK į HERA botą.
Viešo cad-site-agent NELIESK. hera-vault NELIESK. Secret'us (raktus/token'us) redaguok į [REDACTED].

KONTEKSTAS: MCP shell endpoint'ai jau uždaryti. Bet cloudflared tunelio host'e nerasta → n8n internetą pasiekia kitu keliu
(greičiausiai tiesioginis :5678 port-map). Reikia išsiaiškinti TIKSLIAI kaip n8n viešas, kad tada (atskira užduotimi, su
vartotojo leidimu) galėtume riboti. ŠI užduotis — tik diagnostika.

ŽINGSNIAI (visi read-only):
1) DOCKER PORT MAP: `docker port n8n-n8n-1 2>/dev/null`; `docker inspect n8n-n8n-1 --format '{{json .HostConfig.PortBindings}} {{json .NetworkSettings.Ports}}' 2>/dev/null`.
   → Ar 5678 bind'intas 0.0.0.0 (viešas) ar 127.0.0.1 (tik localhost)?
2) HOST LISTENER'IAI: `ss -tlnp 2>/dev/null | grep -E ':5678|:80|:443|:5679'` (kokiu adresu klauso).
3) FIREWALL: `ufw status verbose 2>/dev/null`; jei ufw nėra — `iptables -S 2>/dev/null | head -40`; `nft list ruleset 2>/dev/null | head -40`.
   → Ar :5678 iš išorės leidžiamas ar blokuojamas?
4) REVERSE PROXY? `docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}' | grep -iE 'nginx|caddy|traefik|proxy|npm'`;
   `ps aux | grep -iE 'nginx|caddy|traefik' | grep -v grep | head`.
5) N8N VIEŠAS URL (iš konteinerio env, redaguok secret'us): `docker exec n8n-n8n-1 printenv 2>/dev/null | grep -iE 'N8N_HOST|N8N_PROTOCOL|WEBHOOK_URL|N8N_EDITOR_BASE_URL|N8N_PORT' | sed -E 's/(KEY|TOKEN|PASSWORD|SECRET)=.*/\1=[REDACTED]/I'`.
6) IŠORINIS PASIEKIAMUMAS (iš host'o į savo public IP): `curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://77.42.94.63:5678/ 2>&1`;
   `curl -s -o /dev/null -w "%{http_code}" --max-time 8 https://77.42.94.63:5678/ 2>&1` (jei 200/401/302 = pasiekiamas; 000/timeout = ne).
7) Jei matosi domenas (iš env WEBHOOK_URL ar reverse proxy) — pažymėk ataskaitoj (ne git).

ATASKAITA (HERA botas, trumpai): (1) 5678 bind 0.0.0.0|127.0.0.1; (2) listener adresas; (3) firewall verdiktas (:5678 open|blocked|nėra fw);
(4) reverse proxy yra|nėra (koks); (5) n8n public URL/protokolas (redaguota); (6) išorinio curl kodai; IŠVADA: kaip n8n viešas + ar :5678 tiesiogiai atviras.

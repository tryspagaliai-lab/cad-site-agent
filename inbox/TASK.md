UŽDUOTIS — 2 FAZĖ: SEARXNG €0 PAIEŠKA (Docker, localhost, JSON API). <13 min, time-boxed.
NEleisk pytest. Telegram TRUMPAI. Jei diegimas užtrunka — atsiskaityk KĄ spėjai, NEUŽSTRIK iki 15 min.

SAUGUMAS: raktų nespausdink. SearXNG bind TIK į localhost (127.0.0.1) — NEatidaryk į internetą (ufw jei reikia).

KONTEKSTAS: HERA reikia €0 paieškos deep-research'ui. SearXNG = self-host metapaieška, be rakto.
VPS mažas (CX23 ~4GB, jau sukasi n8n docker + hera servisai + chromium) — stebėk RAM.

0) RAM PATIKRA prieš: free -m. Jei laisvos RAM < ~400MB — pažymėk ataskaitoje riziką, bet tęsk (SearXNG ~200MB).

1) ĮDIEK SearXNG per Docker (searxng/searxng образas arba searxng-docker compose). Bind: 127.0.0.1:8888
   (ar laisvas portas; NE 0.0.0.0). settings.yml BŪTINA:
   - server.secret_key: sugeneruok atsitiktinį (openssl rand -hex 32), NEspausdink jo;
   - search.formats: [html, json]  (JSON BŪTINAS);
   - server.limiter: false  (viena vidinė HERA instancija, kad nedroselintų savęs);
   - varikliai: palik DuckDuckGo, Brave, Bing, Startpage, Wikipedia, Wikidata; Google NEbūtinas (blokuojamas).
   Konteineris: restart=unless-stopped, atminties limitas (pvz. --memory=350m) kad nesuvalgytų VPS.

2) PATIKRA: curl -s "http://127.0.0.1:8888/search?q=anthropic+claude&format=json" -> turi grąžinti JSON su
   results[] (url,title,content). Parodyk kiek rezultatų grįžo (be viso turinio).

3) HERA WRAPPER /opt/hera-processor/hera_search.py: funkcija search(query, n=8) -> [{url,title,content}]
   per SearXNG JSON (httpx/urllib, 15s timeout, fail-safe: klaida/tuščia -> [] , NEkelia išimties).
   (Backup ddgs — NEdiegti dabar, tik palik TODO komentarą.)

4) TESTAS: hera_search.search("HERA memory agent") -> grąžina >0 rezultatų (parodyk kiek, 1-2 title pavyzdžius,
   be raktų); fail-safe: blogas query/servisas down -> [] , ne crash.

5) DURABILUMAS: compose/settings + hera_search.py kopija į /opt/cad-site-agent/n8n/ (be push į viešą);
   hera_search.py push į PRIVATŲ hera-core-backup (secret-scan; secret_key NEcommit'ink). Viešo NELIESK.

TELEGRAM (trumpai, be raktų): (1) RAM prieš/po, (2) SearXNG veikia localhost:8888, JSON grąžina N rezultatų,
(3) hera_search.search testas — kiek rezultatų, (4) backup OK, (5) „SEARXNG PARUOŠTAS (2 FAZĖ)" arba
„DALINAI — <kas liko>".

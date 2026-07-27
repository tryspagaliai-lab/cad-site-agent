UŽDUOTIS — Fazė 35: forensinė patikra — ar neautentifikuotu shell endpoint'u kas nors pasinaudojo? TIK SKAITYMAS. <14 min.

## Tikslas
Iki 2026-07-21 n8n turėjo **3 MCP endpoint'us su `authentication=none`**, pasiekiamus iš interneto per
`mcp.<domenas>/mcp/*`. Vienas jų — **„Claude VPS Shell"** (`zzVpsShellMcp01`), t.y. **neautentifikuotas shell'as**:
kas žinojo URL, galėjo vykdyti komandas VPS'e. Endpoint'ai deaktyvuoti + n8n perkrautas; skylė uždaryta ir
patvirtinta iš išorės. Eilėje nuo tada kabo „3 raktų rotacija (atsargumo priemonė)".

**Šios užduoties tikslas — paversti tą prielaidą ĮRODYMU.** Klausimas ne „ar rotuoti", o **ar apskritai kas nors
tuo pasinaudojo**. Ir svarbiausia — **ar kas nors ką nors PALIKO.**

## 🔴 TIK SKAITYMAS
Nieko netaisyk, netrink, nekeisk, nerotuok. Jei rasi kažką įtartino — **PRANEŠK, NEŠALINK.** Pašalinimas gali
sunaikinti įrodymus ir, jei tai klaidingas aliarmas, sulaužyti veikiančią sistemą. Sprendimą dėl reagavimo priims vartotojas.
**Secret'ų REIKŠMIŲ niekada nespausdink** — tik faktą „yra/nėra", vardus, datas.

## Realybė (ko pats neišvestum)
- 3 workflow ID: `zzVpsShellMcp01` (shell), `jij5EQGypNkPsHgh` (control), `mcprouterdesk001` (/desk router).
  Visi `active=false` nuo 2026-07-21, n8n konteineris perkrautas (`n8n-n8n-1`, n8n-custom 2.28.4).
- Reverse proxy: `n8n-caddy-1` (Caddy2). Viešas kelias buvo `mcp.<domenas>/mcp/*`.
- `:5678` docker NEpublikuotas į host; host klauso :80/:443; ufw aktyvus (22/80/443).
- Teisėtas naudojimas: **orchestratorius pats** naudojo `/desk` router `run_shell` iki uždarymo — tad dalis
  vykdymų BUS mūsų. Reikia atskirti MŪSŲ nuo svetimų (pagal laiką, IP, User-Agent, komandų turinį).
- Kada endpoint'ai atsirado — nustatyk pats (n8n DB `createdAt`), kad žinotum tikrą ekspozicijos langą.

## Įrodymai (ko tikiuosi ataskaitoje)
1. **Ekspozicijos langas:** nuo kada iki kada endpoint'ai buvo aktyvūs ir pasiekiami. Konkrečios datos.
2. **n8n vykdymų istorija** tiems 3 workflow'ams per tą langą: kiek vykdymų, kada, ar visi paaiškinami mūsų veikla.
   **Jei yra nepaaiškinamų — tai svarbiausias radinys, pateik detales.**
3. **Caddy prieigos logai** `mcp.*` / `/mcp/*` keliams: ar buvo užklausų iš IP, kurie nėra mūsų? Skenavimo požymiai
   (daug 404, botų User-Agent)? Jei logai nesaugomi/rotuoti — pasakyk tai atvirai, tai irgi rezultatas.
4. **⭐ PERSISTENCIJA — ar kas nors ką nors PALIKO** (svarbiausia dalis; jei shell buvo naudotas, tai matytųsi čia):
   netikėti cron įrašai · nauji/pakeisti `~/.ssh/authorized_keys` · nauji systemd unit'ai/timer'iai · nežinomi
   procesai ar klausantys portai · neįprasti naudotojai · `/tmp`, `/var/tmp`, `/dev/shm` vykdomieji failai ·
   netikėti docker konteineriai/images. Palygink su tuo, kas TURI būti (HERA cron'ai, n8n, Caddy).
5. **Telegram botai:** ar botų siųstų žinučių istorija atitinka mūsų digest/ataskaitų srautą — jokių svetimų siuntimų?
6. **Bendras verdiktas:** ar yra kompromitavimo požymių — TAIP / NE / NEAIŠKU (ir kodėl neaišku).
   Jei NE — pasakyk, kiek stipriai tuo galima pasitikėti (pvz. „logai rotuoti, matomas tik paskutinių N dienų langas").

## Apribojimai
€0, be tinklo į išorę (išskyrus jei reikia patikrinti savo pačių endpoint'ą). Ataskaita TIK į HERA botą.
Viešo `cad-site-agent` NELIESK. Cron/konfigų NELIESK. Nieko nediek.
Jei kuri nors patikra neįmanoma (logų nėra, teisių trūksta) — pasakyk, NEapsimesk, kad patikrinai.

Jei STOP — kodėl.

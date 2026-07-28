UŽDUOTIS — Fazė 36: Anthropic rakto priklausomybių žemėlapis prieš rotaciją. TIK SKAITYMAS. <12 min.

## Tikslas
Fazė 35 nustatė: kompromiso pėdsakų nėra, persistencija švari, bet lieka **vienas neatmestas scenarijus —
kredencialai galėjo būti tyliai perskaityti** per neautentifikuoto shell endpoint'o langą. Sprendimas priimtas:
rotuojam **tik Anthropic** raktą (vienintelis su realiais pinigais; tylus jo panaudojimas nesukelia jokio signalo).

**Šios užduoties tikslas — sudaryti tikslų priklausomybių žemėlapį, kad rotacija būtų VIENAS atominis veiksmas,
o ne serija netikėtų lūžimų.** Pagrindinis nežinomasis: **ar tas pats fizinis raktas naudojamas dar kur nors**,
be n8n kredencialo `zzAnthropicCr001` — visų pirma, ar juo autentifikuojasi VPS runner'io `claude -p`.

## 🔴 TIK SKAITYMAS
Nieko nerotuok, nekeisk, netrink, neperkrauk, neperleisk servisų. Ši užduotis TIK renka faktus; pačią rotaciją
atliks atskiras human-gate sprendimas. Radęs problemą — **PRANEŠK, NETAISYK.**

## 🔴 SECRET'Ų REIKŠMIŲ NESPAUSDINK — NIEKADA
Ataskaitoje negali atsirasti nė vieno rakto simbolio (net „paskutiniai 4"). Tapatumui nustatyti naudok **tik
palyginimo pirštų atspaudą (fingerprint): `sha256` pirmus 8 hex simbolius**. To pakanka atsakyti „tas pats ar
skirtingas raktas", ir nepakanka raktui atkurti. Failų vardus, kelius, kintamųjų vardus, datas — rašyk laisvai.

## Realybė (ko pats neišvestum)
- Runner: `/opt/hera-processor/vps_agent_runner.sh`; `/usr/local/bin/vps_agent_runner.sh` — **symlink** į jį
  (suvienodinta Fazėje 31; dviejų fizinių kopijų nebėra). Runner sukamas per cron kas 2 min su `flock`.
- n8n gyvena docker konteineryje `n8n-n8n-1`; jo aplinka — `/opt/n8n/.env`; kredencialai n8n DB **šifruoti**
  `N8N_ENCRYPTION_KEY` — jų reikšmių iš disko paprastai neperskaitysi ir NEREIKIA (užtenka fakto, kad įrašas yra).
- Kandidatai, kur raktas gali gyventi: aplinkos kintamieji (`ANTHROPIC_*`), `~/.claude/`, `/root/.claude*`,
  `/opt/hera-venv` ir `hera_*.py` moduliai, cron aplinka, systemd unit'ai, `/opt/n8n/.env`, docker `--env`.
- HERA moduliai daugiausia naudoja **€0 tiekėjus** (Gemini/Groq/GLM) — jų raktai NE šios užduoties objektas.
  Bet jei kuris nors modulis kviečia Anthropic — tai svarbu ir turi patekti į žemėlapį.

## Kritinis klausimas, į kurį BŪTINA atsakyti aiškiai
**Kaip autentifikuojasi runner'io `claude -p`: per API raktą ar per OAuth/prenumeratos sesiją?**
Nuo to priklauso viskas: jei OAuth — Anthropic API rakto rotacija runner'io **visiškai neliečia** ir rotacija
tampa triviali. Jei API raktas — reikia žinoti, ar jis **tas pats** kaip n8n kredencialo (fingerprint palyginimas).
Jei nustatyti neįmanoma — parašyk „neįmanoma nustatyti ir kodėl". **Nespėliok** — spėjimas čia brangesnis už nežinojimą.

## Apribojimai
- €0. **Netikrink rakto galiojimo kviečiant Anthropic API** — tai kainuoja ir užterštų usage istoriją, kurią
  vartotojas kaip tik ruošiasi peržiūrėti kaip nepriklausomą įrodymą.
- Viešo repo `cad-site-agent` git'e neliesti; rezultatai — tik ataskaitoje į HERA botą.
- HARD timeout, be retry. Nespėjus — pranešk, ką suspėjai ir ko NEtikrinai.

## Sėkmės kriterijai (ką turi turėti ataskaita)
1. **Lentelė:** vartotojas (kelias/servisas) → kaip gauna raktą (env / failas / docker env) → fingerprint (8 hex)
   arba „nepasiekiama".
2. **Vienareikšmis atsakymas**, ar runner'io `claude -p` priklauso nuo Anthropic API rakto: taip / ne / neįmanoma + kodėl.
3. **Ar visi rasti vartotojai naudoja TĄ PATĮ raktą** (fingerprint sutapimai), ar egzistuoja >1 skirtingas raktas.
4. **Rotacijos planas:** ką konkrečiai reikės atnaujinti, kokia eilės tvarka, ir **kas nulūš, jei kurį nors punktą
   pamirši**. Įskaitant, ar reikia perkrauti n8n / perleisti servisus.
5. Sąžiningas **„ko patikrinti nepavyko"** sąrašas. Tuščias sąrašas be paaiškinimo — įtartinas.

Jei STOP — kodėl.

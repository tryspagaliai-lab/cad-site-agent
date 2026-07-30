UŽDUOTIS — Fazė 44: NUIMTI token'ą iš inbox remote URL (kad rakto pergeneravimas nenukirstų valdymo kanalo). HUMAN-GATE GAUTAS („Varom"). <8 min.

## Tikslas — vienas, siauras
Fazė 43 nustatė: `/opt/cad-site-agent/.git/config` origin URL turi **įkeptą** GitHub PAT
(`https://<token>@github.com/...`). Repo **VIEŠAS**, bet negaliojantis kredencialas URL'e duoda 401/403 —
git **NEGRĮŽTA** prie anoniminio pull'o. `vps_agent_runner.sh` tai pagauna `|| exit 0` → paleidimas baigiasi
**TYLIAI** (be Telegram, be log). Vartotojas netrukus pergeneruos raktą.

⇒ **Jei nieko nedarysim, pergeneravimas nukirs vienintelį valdymo kanalą, ir pataisymo užduoties atsiųsti nebus kaip.**

**Šios užduoties tikslas: padaryti inbox fetch'ą NEPRIKLAUSOMĄ nuo rakto** — išimti kredencialą iš remote URL,
kad `git fetch` eitų anonimiškai. Viešam repo autentifikacijos nereikia.

## 🔴 DARYK TIK TAI. Nieko daugiau.
- `/root/hera.env` **NELIESK** — GITHUB_TOKEN ten LIEKA (jo reikia vault sync ir `hera-core-backup` push'ams;
  vartotojas jį pakeis pats per SSH po pergeneravimo).
- `/opt/hera-processor` remote **NELIESK** — jis privatus, jam token reikalingas.
- `vps_agent_runner.sh` logikos **NEKEISK** — keičiam tik remote URL, ne skriptą.
- Sesijos jsonl failų **NELIESK** (nuotėkio valymas — atskira fazė po pergeneravimo, kai raktas jau bus negyvas).

## Ką padaryti
1. **BACKUP:** nusikopijuok `/opt/cad-site-agent/.git/config` (jame yra token — **backup'ą laikyk 600 teisėmis
   ir NEspausdink turinio**; jis vis tiek netrukus taps negaliojantis).
2. **Nuimk kredencialą iš origin URL** → grynas `https://github.com/tryspagaliai-lab/cad-site-agent` (arba `.git`).
   Naudok `git remote set-url` — **NE** rankinį konfigo redagavimą.
3. **Patikrink, ar dar kas nors toje repo konfigūracijoje neturi įkepto kredencialo** (kiti remote'ai,
   `insteadOf`, `url.*.pushInsteadOf`, submodules). Skenuok, neenumeruok.

## Įrodymai, kurių reikalauju ataskaitoje
- **`git fetch origin claude/authorize-claude-code-vps-1dcvrv` VEIKIA po pakeitimo** — paleisk ir parodyk rc=0.
  Tai svarbiausias įrodymas: jei fetch neveikia anonimiškai, **grąžink backup'ą** ir pranešk STOP.
- Naujas remote URL (be kredencialo — jį rodyti saugu).
- Patvirtinimas, kad `hera.env` ir `/opt/hera-processor` remote **nepaliesti**.
- ⚠️ **Papildoma patikra prieš baigiant:** ar `git fetch` neprašo kredencialo interaktyviai (askpass) — paleisk su
  `GIT_TERMINAL_PROMPT=0`, kad tylus laukimas nevirstų 15-min timeout'u produkcijoje.

## 🔴 Rakto reikšmės NIEKUR nespausdink
Nei ataskaitoje, nei tarpiniuose failuose, nei komandų išvestyje. Jei reikia lyginti — `sha256` pirmi 8 hex.
**Ypač: NENAUDOK `git remote get-url origin` be redakcijos** — būtent ta komanda Fazėje 43 nutekino raktą į transkriptą.
Jei saugesnį kelią blokuoja hook'as — **sustok ir pranešk**, o ne persijunk į nesaugų variantą.

## Apribojimai
€0 · viešo repo git ISTORIJOS neliesk (keičiam tik lokalų `.git/config`) · HARD timeout, be retry ·
jei kas nors nepavyksta — **atstatyk backup'ą** ir pranešk, geriau veikianti sena būsena nei pusiau pakeista.

**ATASKAITOS TAISYKLĖ:** „neįmanoma / nepavyko" galioja tik su sąrašu, KĄ BANDEI.

Jei STOP — kodėl.

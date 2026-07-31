UŽDUOTIS — Fazė 46: SENO GitHub rakto plaintext liekanų valymas (Fazės 45 B dalis — vartai dabar ATIDARYTI). <12 min.

## Kodėl vartai atsidarė
Fazė 45 teisingai sustojo prieš B dalį, nes `hera-processor` dar turėjo seną raktą atmintyje.
**Tai IŠSPRĘSTA ir patikrinta akyse:** vartotojas paleido `systemctl restart hera-processor` →
naujas **PID 1977777**, startas 2026-07-31 08:04:00 BST, o `/proc/1977777/environ` GITHUB_TOKEN
fingerprint = **`92203a0c`** (≠ senas `90fcb4b8`).
Kartu su Fazės 45 įrodymais (vault sync push RC=0; `hera-core-backup` push `6828794..ad0c808` RC=0)
**A dalis pilnai patvirtinta. Senas raktas `90fcb4b8` NEBEGALIOJA — jo liekanas galima valyti.**

## 🔴 Pirma — sanity patikra prieš bet ką (30 s)
Pats patikrink `/proc/<hera-processor PID>/environ` GITHUB_TOKEN fingerprint.
**Jei jis NĖRA `92203a0c` arba yra `90fcb4b8` — STOP, nieko netrink, pranešk.**
Backup'ai yra vienintelis atstatymo taškas; jų negalima liesti remiantis vien šia užduotimi.

## Ką padaryti

### 1. Rask seno rakto reikšmę — programiškai, nespausdindamas
Perskaityk ją iš vieno backup'o (`/root/hera.env.bak.*` arba `/opt/cad-site-agent/.git/config.bak.fase44`)
**į kintamąjį**, ir patvirtink, kad jos `sha256[:8]` = `90fcb4b8`. Jei nesutampa — STOP, pranešk.
**Reikšmės niekur nespausdink** — nei ataskaitoje, nei tarpiniuose failuose, nei komandų išvestyje.

### 2. Skenuok, NEenumeruok
Rask VISAS vietas, kur ta reikšmė dar egzistuoja. Bent: `/root`, `/opt`, `/tmp`, `/var/log`.
*(Precedentas: Fazė 36 enumeruodama rado 2 vietas, Fazė 37 skenuodama — 3. Enumeracija ≠ paieška.)*
Žinomi kandidatai, bet **NE baigtinis sąrašas**: `/root/hera.env.bak.*` · `.git/config.bak.fase44` ·
`/root/.claude/projects/-opt-cad-site-agent/*.jsonl` (Fazėje 43 agentas per klaidą atspausdino pilną raktą) ·
galimai `/root/.bash_history` (vartotojas naudojo `HISTFILE=/dev/null`, bet patikrink) · vault sync logai.

### 3. Tvarkyk pagal tipą — NE viską vienodai
- **Transkriptų / žurnalų / audito failuose (`*.jsonl`, `*.log`): REDAGUOK, NETRINK failo.**
  Pakeisk rakto reikšmę į `[REDACTED-FAZE46]`. Priežastis: tai audito įrašai, o mums galioja
  **ARCHYVUOJAM, NETRINAM** — failas lieka, paslaptis dingsta.
  ⚠️ **Neliesk failo, priklausančio TAVO paties dabartinei sesijai** (sugadintum gyvą būseną) — jei toks
  pasitaiko, palik ir aiškiai pasakyk ataskaitoje, kad jis liko.
- **Backup failus, kurių vienintelis turinys yra senas kredencialas — TRINK.**
  (`/root/hera.env.bak.*`, `config.bak.fase44`.) Jie nebereikalingi: A dalis įrodė, kad naujas veikia.

### 4. Susitvarkyk po savęs (Fazės 45 testų artefaktai)
- `/opt/hera-processor/PHASE45_PUSH_TEST.md` — tavo pačių sukurtas testinis žymos failas, jau įpush'intas
  į `hera-core-backup`. **Pašalink ir push'ink pašalinimą** (tai ne žinių medžiaga, o testo šiukšlė —
  „archyvuojam, netrinam" jai NEGALIOJA).
- Trivialią eilutę, pridėtą į `/opt/hera-vault/state/vault_sync_status.txt` — irgi atstatyk, jei ji dirbtinė.

### 5. Galutinis skenas
Pakartok 2 žingsnio skeną. **Ataskaitoje turi būti: kiek vietų rasta, kiek suredaguota, kiek ištrinta,
ir ar galutinis skenas švarus.** Jei kur nors liko — nurodyk vietą (be reikšmės) ir kodėl liko.

## 🔴 Ribos
- **Jokių rakto reikšmių (nei seno, nei naujo) niekur.** Tik fingerprint'ai.
- **NENAUDOK komandų, spausdinančių URL su kredencialu** (`git remote get-url` ir pan.) — būtent tokia
  komanda Fazėje 43 nutekino raktą. **Jei saugesnį kelią blokuoja hook'as — SUSTOK ir pranešk, o ne apeik.**
  *(Fazė 44 taip ir pasielgė — tai teisingas elgesys ir jo laikomės.)*
- `/root/hera.env` **neliesk** (jis blokuotas ir taip; jo turinys teisingas).
- €0 · viešo `cad-site-agent` git ISTORIJOS neliesk · HARD timeout, be retry.

**ATASKAITOS TAISYKLĖ:** „neįmanoma / nepavyko" galioja tik su sąrašu, KĄ BANDEI.

Jei STOP — kodėl.

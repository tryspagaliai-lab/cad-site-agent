UŽDUOTIS — Fazė 45: patikrinti, kad NAUJAS GitHub raktas veikia VISUR + išvalyti SENO rakto plaintext liekanas. HUMAN-GATE GAUTAS („Padaryta"). <13 min.

## Kontekstas (ko pats neišvestum)
Vartotojas ką tik per SSH pergeneravo GitHub PAT ir įrašė naują reikšmę į `/root/hera.env`, po to
`systemctl restart hera-processor`. **Senas raktas (fingerprint `90fcb4b8`) nuo pergeneravimo momento NEBEGALIOJA.**
Fazė 44 jau nuėmė token'ą iš inbox remote (inbox dabar anoniminis — todėl ši užduotis tave pasiekė net jei
kas nors kita sulūžo).

## Dalis A — PATIKRINTI (tikrinam, ne tikim)
Vartotojas sako, kad pavyko. Agento ir žmogaus teiginiai pas mus tikrinami, ne priimami.

1. **`hera.env` fingerprint** (`sha256` pirmi 8 hex nuo `GITHUB_TOKEN` reikšmės) — **privalo SKIRTIS nuo `90fcb4b8`.**
   Jei sutampa → raktas nepasikeitė, **STOP, pranešk, nieko netrink.**
2. **Gyvo proceso atmintis:** patikrink `hera-processor` proceso `/proc/<pid>/environ` — ar jis jau turi **naują**
   reikšmę (fingerprint sutampa su failo). *(Fazė 42 pamoka: konfigai meluoja, `/proc` ne.)*
   Jei procesas dar su senu → perkrovimas neįvyko arba neuždirbo; pranešk.
3. **vault sync push** — paleisk `hera_vault_sync.sh` ir parodyk realų rezultatą (rc + log uodegą).
4. **⭐ `hera-core-backup` push — ATSKIRAI ir BŪTINAI.** Fazė 43 šito patikrinti negalėjo ir net nerado trigger'io,
   kuris jį paleidžia. Padaryk minimalų nekenksmingą push'ą (pvz. tuščias commit arba trivialus žymos failas),
   kad įrodytum, jog autentifikacija veikia. **Tai vienintelė vieta, kur naujas raktas dar nepatikrintas.**
   Jei push nepavyksta — tai svarbiausias radinys, pranešk nedelsiant.

**Jei bet kuri A dalies patikra nepavyksta — B dalies NEDARYK.** Backup'ai su senu raktu yra atstatymo taškas;
kol nežinai, kad naujas veikia, jų trinti negalima.

## Dalis B — IŠVALYTI seno rakto plaintext liekanas (tik jei A praėjo)
Rotacijos metu atsirado kelios naujos **plaintext seno rakto kopijos**. Raktas negalioja, bet liekanos nereikalingos
(precedentas: `bash_history` valymas Fazėje 37).

Žinomos vietos (**skenuok, neenumeruok** — Fazė 36 enumeruodama rado 2, Fazė 37 skenuodama 3):
- `/root/hera.env.bak.*` — vartotojo backup'as prieš keitimą
- `/opt/cad-site-agent/.git/config.bak.fase44` — Fazės 44 backup'as
- **`/root/.claude/projects/-opt-cad-site-agent/*.jsonl`** — Fazėje 43 agentas per klaidą atspausdino **pilną
  galiojantį raktą** į transkriptą; jis fiziškai įrašytas į tos sesijos failą

### Metodas (svarbu, laikykis eiliškumo)
1. **Pirma** perskaityk seną reikšmę iš vieno backup'o **programiškai** ir patvirtink, kad jos fingerprint = `90fcb4b8`.
   **NIEKADA jos nespausdink** — naudok tik kaip paieškos/pakeitimo raktą kintamajame.
2. **jsonl failuose REDAGUOK, NETRINK failų** — pakeisk rakto eilutę į `[REDACTED-FAZE45]`.
   Priežastis: tai audito įrašas; mums galioja **ARCHYVUOJAM, NETRINAM**. Failas lieka, paslaptis dingsta.
   ⚠️ Neliesk failo, priklausančio TAVO paties dabartinei sesijai (rizika sugadinti gyvą būseną) — jei toks
   pasitaiko, pasakyk ir palik.
3. **Tik po to** ištrink backup'us, kuriuose yra senas raktas (`hera.env.bak.*`, `config.bak.fase44`) — jie
   nebereikalingi, nes A dalis įrodė, kad naujas veikia.
4. **Galutinė patikra:** perskenuok `/root`, `/opt`, `/tmp` ir rask, ar fingerprint `90fcb4b8` atitinkanti reikšmė
   dar kur nors egzistuoja. Jei taip — pranešk vietą (be reikšmės).

## 🔴 Bendros ribos
- **Rakto reikšmių (nei seno, nei naujo) niekur nespausdink.** Tik fingerprint'ai.
- **NENAUDOK `git remote get-url` ar kitų komandų, kurios spausdina URL su kredencialu** — būtent tokia komanda
  Fazėje 43 nutekino raktą. Jei saugesnį kelią blokuoja hook'as — **sustok ir pranešk**, o ne apeik.
- `hera.env` turinio nekeisk (tik skaityk fingerprint'ui). Teisės turi likti 600.
- €0 · viešo `cad-site-agent` git ISTORIJOS neliesk · HARD timeout, be retry.

## Ataskaitoje
A dalis: 4 patikros su konkrečiais rezultatais (fingerprint'ai, rc, log) · B dalis: kiek vietų rasta, kiek
suredaguota, kiek ištrinta, galutinio skeno rezultatas · sąžiningas „ko nepavyko".

**ATASKAITOS TAISYKLĖ:** „neįmanoma / nepavyko" galioja tik su sąrašu, KĄ BANDEI.

Jei STOP — kodėl.

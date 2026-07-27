UŽDUOTIS — Fazė 31: kurią modulių KOPIJĄ runner realiai vykdo? Auditas + suvienodinimas. <14 min.

## Tikslas
Fazės 30 agentas pastebėjo: **runner eilutėje ~127 kviečia `/opt/cad-site-agent/n8n/hera/hera_verify.py`**, o taisom
`/root/hera_verify.py` + `/opt/hera-processor/`. Jei taip yra ir kitiems moduliams — **dalis šiandienos pataisų NĖRA gyvos.**

**Tiesioginis įtarimo patvirtinimas:** GoalAnchor tarpkalbinis fix atliktas šįryt (inkaro atomai, 9/9), bet
2026-07-27 16:36 runner ataskaitoje VĖL pasirodė `🧭 GOALANCHOR status=warn overlap=0.1441 signals=drift`
ant lietuviškos užduoties su angliška ataskaita — **tiksliai tas atvejis, kurį pataisa turėjo nuslopinti.**
Labai tikėtina, kad runner vykdo SENĄ `hera_goalanchor.py` kopiją.

Išsiaiškink tikrą padėtį ir sutvarkyk taip, kad **taisymas vienoje vietoje visada pasiektų runner'į.**

## Realybė (ko pats neišvestum)
- Egzistuoja bent TRYS vietos, kur gyvena tie patys `hera_*.py`: `/root/`, `/opt/hera-processor/` (git repo,
  push į privatų `hera-core-backup`), `/opt/cad-site-agent/n8n/hera/` (untracked kopija viešame repo medyje).
- Konvencija iki šiol buvo: taisom `/root/`, backup į `/opt/hera-processor/`. Niekas netikrino, ką runner kviečia.
- Liečiami moduliai (visi šios savaitės): `hera_goalanchor`, `hera_verify`, `hera_staleguard`, `hera_ctxtrim`,
  `hera_skillcapture`, `hera_perceived_error`, `hera_langfuzz`, `hera_loopguard`, `hera_diffrules`, `hera_validator`.
- ⚠️ Viešo `cad-site-agent` git istorijos NELIESTI — bet failai ten **untracked**, tad jų turinį keisti galima
  (jie ir taip nepatenka į git). Įsitikink, kad `git status` viešame repo NEPASIKEIČIA.

## Apribojimai
€0, be tinklo, be LLM. Fail-safe. **BACKUP visų liečiamų failų prieš keitimą.** Ataskaita TIK į HERA botą.
Cron/secret'ai NELIESK. Jei sprendimas reikalautų keisti runner'io logiką labiau nei kelias kelio (path) eilutes —
**STOP ir pasiūlyk, nedaryk.** Geriau tikslus diagnozas nei skubotas refaktoringas.
`HERA_VERIFY_CHECK` lieka def 0. Naujų funkcijų NEDIEK — tik kelių suvienodinimas.

## Įrodymai
1. **Kelio žemėlapis:** kiekvienam iš 10 modulių — KURĮ kelią runner (ar kitas gyvas kvietėjas: cron, Loop B/C,
   dispatcher) realiai vykdo. Lentelė: modulis · runner kviečia · kur naujausia versija · **ar sutampa**.
2. **Kiek pataisų NEBUVO gyvos:** aiškiai išvardyk, kurios šios savaitės pataisos realiai neveikė produkcijoje.
   Tai svarbiausia išvada — nesušvelnink jos.
3. **GoalAnchor konkrečiai:** ar runner vykdoma kopija turi tarpkalbinį fix'ą (inkaro atomus)? Jei ne — patvirtink,
   kad tai paaiškina 16:36 klaidingą `drift` įspėjimą.
4. **Suvienodinimas:** padaryk taip, kad būtų VIENAS šaltinis. Pasirink mechanizmą (symlink / runner kelio pataisa /
   sync žingsnis) ir **pagrįsk**, kodėl jis atsparus (kad po mėnesio kitas agentas vėl nepataisytų ne to failo).
5. **Patikra po suvienodinimo:** paleisk GoalAnchor ant tos pačios LT-užduotis/EN-ataskaita poros → turi grąžinti
   `ok` (ne `drift`). Ir `hera_verify` ant F30 etaloninio rinkinio → turi duoti tuos pačius 25 pass.
6. `bash -n` runner OK; viešo repo `git status` nepakitęs; BACKUP + push į `hera-core-backup`; ROADMAP.md eilutė
   (**patikrink, kad tikrai faile atsirado** — praeitos 4 ataskaitos to teigė nepagrįstai).

Jei STOP — kodėl + pilnas kelio žemėlapis.

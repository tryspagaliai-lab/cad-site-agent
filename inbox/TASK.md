# Fazė 51 — grįžtamojo ryšio kanalo sutvarkymas: Fazės 49 ataskaitos persiuntimas + send_tg pristatymo matomumas. HUMAN-GATE GAUTAS („Varom"). <14 min.

## Tikslas

1. **Persiųsti Fazės 49 ataskaitą.** Pilnas jos tekstas guli `/root/agent_result_0a9f9c6a5e83.txt`
   (4252 B — Fazė 50 tai patikrino). Išsiųsk jį per HERA botą DABAR, su aiškia antrašte, kad tai
   VĖLUOJANTI Fazės 49 ataskaita (vykdyta 2026-08-02, pristatymas tada tyliai nepavyko).
   Jei tekstas viršija saugų limitą — skaidyk į kelias žinutes, NE karpyk turinio.

2. **`send_tg` pristatymo matomumas.** Fazė 50 nustatė: `send_tg` naudoja `curl ... || true` ir
   NEFIKSUOJA jokio HTTP atsako — tyli pristatymo triktis nematoma iš principo. Pataisyk:
   - fiksuok `curl -w '%{http_code}'` (arba ekvivalentą) + laiko žymę + žinutės ilgį į log failą
     (pvz. `/root/send_tg.log` arba esamą runner log'ą);
   - ne-2xx atsakas arba curl klaida → įrašas log'e su aiškia žyma (pvz. `TG-FAIL`);
   - **elgsenos NEKEISK**: `|| true` lieka (runner'is negali lūžti dėl Telegram) — keičiasi tik tai,
     kad triktis tampa MATOMA. Tai matomumo pataisa, ne polarumo keitimas.

3. **Savikontrolė:** po pakeitimo išsiųsk trumpą testinę žinutę per pataisytą `send_tg` ir parodyk
   ataskaitoje atitinkamą log eilutę (http_code=200). Tai kartu įrodys ir 1) punkto pristatymą.

## Realybė (iš Fazės 50, nekartok tikrinimo)

- Fazė 49 buvo įvykdyta rc=0 per 7 min; problema TIK pristatyme.
- `send_tg` karpo iki 3900 simbolių; pilna F49 žinutė (4284 B UTF-8) po karpymo = 4092 B < 4096 B
  Telegram ribos — ilgis NEBUVO trikties priežastis, tad nešalink karpymo, tik neprarask turinio
  persiuntime (žr. skaidymą 1 punkte).
- Boto tokenas ir chat_id patikrinti veikiantys (`getMe`/`getChat`).
- Tikrasis cron: `/etc/cron.d/vps-agent` (ne `crontab -l`).

## Apribojimai (nekintami)

- €0 · fail-safe · **BACKUP prieš keitimą** (runner skripto kopija + push į privatų `hera-core-backup`) ·
  HARD laiko biudžetas — jei nespėji, pirmenybė 1) persiuntimui: jis trivialus ir vertingiausias.
- `send_tg` pakeitimas minimalus — jokio naujo modulio, jokių naujų priklausomybių, jokio retry
  (anti-rc124: NO retry galioja ir čia).
- Log faile — jokių token'ų ir jokio žinutės TURINIO (tik ilgis, laikas, http_code): log'as gali
  būti mažiau saugomas nei vault.
- Viešo `cad-site-agent` git'o neliesti.

## Sėkmės kriterijai (selftest)

1. Fazės 49 ataskaita pasiekė Telegram (pilnas turinys, skaidyta jei reikėjo).
2. Log'e matoma nauja eilutė su http_code=200 iš testinės žinutės; TG-FAIL kelias parodytas
   bent sausu testu (pvz. curl į negaliojantį endpoint'ą su išjungtu siuntimu arba kodo peržiūra).
3. Backup commit'as `hera-core-backup` su pakeistu runner/send_tg skriptu.
4. Runner elgsena nepakitusi: `|| true` vietoje, jokio retry, jokio naujo lūžio kelio.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

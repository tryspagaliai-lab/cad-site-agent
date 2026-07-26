UŽDUOTIS — Fazė 26: apsauga nuo pasenusio failo perrašymo (turinio maišos guardas). <13 min.

## Tikslas
HERA agentai redaguoja failus VPS'e. Tarp failo PERSKAITYMO ir ĮRAŠYMO jis gali pasikeisti — kitas runner ciklas
(cron */2), `hera_vault_sync.sh` (*/30), lygiagretus procesas ar pats vartotojas. **Dabar jokio patikrinimo nėra:
tylus perrašymas įmanomas ir prarastas darbas liktų nepastebėtas.**
Sukurk deterministinį modulį, kuris leidžia įrašyti TIK jei failas nuo perskaitymo nepasikeitė; kitaip — atmesti
ir pranešti, niekada tyliai neperrašyti.
Šaltinis: kuruotas `oh-my-pi` pattern (pakeitimai susiejami su turinio maišos kodais; pataisa pritaikoma iš pirmo
karto arba atmetama, jei failas pasenęs).

## Realybė (ko pats neišvestum)
- Modulių konvencija: `/root/hera_<vardas>.py`, `HERA_<VARDAS>` jungiklis **def 0**, savas `--selftest` (BE pytest),
  fail-safe, backup į `/opt/hera-processor/` + push į privatų `hera-core-backup`, ROADMAP.md eilutė.
- Gretimi guardai, su kuriais tai turi derėti (nesidubliuoti): `hera_validator` (14), `hera_diffrules` (13),
  `hera_loopguard` (15), `hera_goalanchor` (21/22). Šis — apie FAILO BŪSENĄ, ne apie turinio kokybę.
- Rizikos langas realus: vault sync gali perrašyti tuos pačius failus, kuriuos redaguoja agentas.
- **Def 0 semantika čia turi būti apgalvota:** išjungus jungiklį modulis NETURI blokuoti rašymo (kad integracija būtų
  saugi), bet TURI mokėti pranešti, kad būtų būtų aptikta ir stebima. Pasirink ir pagrįsk.

## Apribojimai
€0, be tinklo, be LLM, deterministiška. Fail-safe: **jokia klaida pačiame guarde negali sukelti duomenų praradimo** —
jei guardas neveikia, elgesys turi būti toks pat saugus kaip be jo (arba saugesnis), niekada necrashinti.
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. Runner'io ir cron NELIESK — tik modulis (integracija = vėliau,
atskiras human-gate). Secret'us NEliesk. Vault turinio NEMODIFIKUOK (testams naudok laikinus failus).

## Įrodymai (selftest, be pytest, be tinklo)
1. **Laimingas kelias:** perskaitai → nieko nepasikeitė → įrašymas LEIDŽIAMAS, turinys teisingas.
2. **Pagrindinis atvejis:** perskaitai → failą pakeičia KAŽKAS KITAS → įrašymas ATMETAMAS, aiški priežastis,
   **originalus (svetimas) turinys IŠLIEKA nepaliestas** (tai svarbiausia — jokio duomenų praradimo).
3. **Naujas failas:** failo dar nėra → elgesys apibrėžtas ir saugus (aprašyk kokį pasirinkai).
4. **Def 0:** jungiklis išjungtas → elgesys pagal tavo pagrindimą iš „Realybė" skilties; parodyk, kad integracija saugi.
5. **Fail-safe:** neskaitomas/neįrašomas kelias, teisių klaida → be crash, be duomenų praradimo.
6. **Lenktynių langas:** pademonstruok realų scenarijų — skaitymas, tarpinis svetimas įrašymas, tada bandymas rašyti.
   Tai turi būti tikras failų sistemos testas, ne tik teorinis.
7. BACKUP + push; ROADMAP.md eilutė.

Ataskaitoje pasakyk, kaip modulis būtų integruojamas realiai (kur kviečiamas) — bet **NEINTEGRUOK**, tai kitas žingsnis.
Jei STOP — kodėl.

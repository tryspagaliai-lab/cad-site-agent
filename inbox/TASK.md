UŽDUOTIS — Fazė 28: `hera_staleguard` integracija į realius rašymo taškus (ADVISORY, elgesys nesikeičia). <14 min.

## Tikslas
Fazė 26 sukūrė `hera_staleguard.py` (CAS: `read_baseline` → `safe_write`), bet jis STANDALONE — niekas jo nekviečia,
todėl reali rizika (pasenusio failo perrašymas) lieka nematuojama. Apvyniok pagrindinius rašymo taškus taip, kad
**pradėtume MATYTI, kaip dažnai tai realiai vyksta**, NEKEIČIANT elgesio.
`HERA_STALEGUARD` def 0 = ADVISORY jau sukurta būtent tam: rašo kaip anksčiau, bet pažymi incidentą ir praneša.
Kai turėsim dažnio duomenis — tada atskiras human-gate sprendimas dėl ENFORCE (`=1`).

## Realybė (ko pats neišvestum)
- Modulis: `/root/hera_staleguard.py`, kopija `/opt/hera-processor/`. API: `read_baseline(path)`, `safe_write(path, content, baseline)`.
- Pats Fazės 26 agentas nurodė kandidatus: `hera_selfedit.py`, Loop C, galimai runner `STATE.md`. **Patikrink juos, bet
  spręsk pats** — apvyniok tik tuos, kur (a) skaitymas ir rašymas atskirti laike ir (b) failą realiai gali paliesti kas
  nors kitas. Kur skaitymas-rašymas atominis arba failas privatus procesui — NEVYNIOK, tai tik rizika be naudos.
- Žinomi lygiagretūs rašytojai, dėl kurių visa tai daroma: cron runner (*/2), `hera_vault_sync.sh` (*/30), pats vartotojas.
- Žinoma modulio riba (jau atskleista): nėra tarpprocesinio flock tarp dviejų vienalaikių `safe_write()`. Neapsimesk, kad ją sprendi.

## Apribojimai
€0, be tinklo, be LLM. **Elgesys su def 0 privalo likti IDENTIŠKAS dabartiniam** — tai svarbiausias reikalavimas.
Fail-safe: jei staleguard importas ar kvietimas kokiu nors būdu nepavyktų, apvyniotas kodas turi veikti kaip anksčiau
(`try/except` + tęsti), NIEKADA neužblokuoti rašymo ir NIEKADA nesukelti duomenų praradimo.
BACKUP kiekvieno liečiamo failo prieš keitimą. Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. Secret'us NEliesk.
**Cron tvarkaraščio NELIESK.** `hera_verify` (Fazė 27) NELIESK — jos integracija yra atskiras žingsnis.
Jei kuris nors taškas atrodo per rizikingas apvynioti — PRALEISK jį ir pasakyk kodėl. Geriau 2 saugūs taškai nei 5 rizikingi.

## Įrodymai (ko tikiuosi ataskaitoje)
1. **Kuriuos taškus apvyniojai ir kuriuos SĄMONINGAI praleidai** — su priežastimi kiekvienam.
2. **Elgesio identiškumo įrodymas su def 0:** parodyk, kad apvyniotas kelias daro tą patį, ką prieš tai (pvz. prieš/po
   palyginimas ar dry-run). Tai kertinis reikalavimas — jei negali įrodyti, nediek.
3. **Incidento aptikimas veikia:** dirbtinai sukelk pasenusio failo situaciją apvyniotame taške → incidentas
   užfiksuotas ir matomas (logas/pranešimas), BET rašymas įvyko (nes advisory). Parodyk abu.
4. **Fail-safe:** imituok staleguard nepasiekiamumą (pvz. importo klaida) → apvyniotas kodas veikia kaip anksčiau.
5. Esamų selftest'ų/bench nepablogėjimas (paleisk ką turi: staleguard 6/6, bench).
6. **Kaip pamatysiu dažnį:** kur kaupiasi incidentai ir kaip po savaitės sužinosiu, ar verta įjungti ENFORCE.
7. BACKUP + push į privatų `hera-core-backup`; ROADMAP.md eilutė.

Jei STOP — kodėl, ir ką radai apie rašymo taškus.

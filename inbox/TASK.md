UŽDUOTIS — Fazė 49: pėdsakų GRANDINĖS (ilgo horizonto trajektorijos) — schemos auditas + minimali papildoma jungtis. HUMAN-GATE GAUTAS („Daryk kaip siūlai"). <14 min.

## Kodėl — išmatuota išorinė problema, ne nuojauta
Straipsnis „Physics of Multi-Turn Long-Horizon Planning" (Chinese Academy of Sciences, 2026) išmatavo:
modelis, treniruotas **TIK trumpoms procedūroms**, duoda **93,12% trumpose / 0,83% vidutinėse / 0% ilgose**
užduotyse. Pridėjus vos **5% vidutinio ilgio** duomenų → vidutinės pakyla iki **51,88%**.
Antras jų radinys: **aiškus būsenos perėjimo samprotavimas (CoT) = 68,5% tikslumo prieš 22,7%** tiesioginiam
veiksmo numatymui — t.y. pėdsakai su TARPINIU samprotavimu verti ~3× daugiau nei vien `action→outcome`.

**Mūsų padėtis:** anti-rc124 taisyklė („dideles užduotis SKAIDYTI") + 15 min HARD timeout reiškia, kad visi
15 sukauptų pėdsakų yra **trumpi**. Runner'io patikimumui tai teisinga ir NEKEIČIAM. Bet mokymo korpusui tai
sisteminis šališkumas, kuris auga kiekvieną dieną.

**Esminis pastebėjimas:** ilgo horizonto darbo mes JAU dirbam — tik jis **sukapotas per fazes**. Pvz. GitHub rakto
rotacija = Fazės 43→48: žemėlapis → de-token → patikra → valymas → auditas → vientisumo patikra. Tai VIENA
trajektorija su vienu tikslu, tik įrašyta kaip 6 atskiri pėdsakai.
⇒ **Sprendimas NĖRA leisti ilgesnes užduotis (tai grąžintų rc=124). Sprendimas — UŽFIKSUOTI RYŠĮ tarp pėdsakų,**
kad korpuse atsirastų sudėtinės ilgo horizonto trajektorijos šalia atominių.

⚠️ **„5%" dabar nėra tikslas** — prie 15 pėdsakų tai <1. Tikslas: **mechanizmas turi egzistuoti PRIEŠ korpusui
išaugant.** Vėliau tai kainuos daug daugiau.

## Dalis A — AUDITAS (pirma; jei laiko mažai, ši dalis svarbiausia)
1. **Ką pėdsako schema realiai fiksuoja?** Išvardyk laukus (`hera_skillcapture.py` + tikras `raw/skill_*.json`).
2. **Ar fiksuojamas TARPINIS samprotavimas / būsenos perėjimai** — ar tik `action` / `input` / `outcome`?
   Konkrečiai: ar matomi agento žingsniai (įrankių kvietimai, tarpinės išvados), ar tik galutinė ataskaita?
   **Tai lemia, ar mūsų pėdsakai iš viso tinka ilgo horizonto mokymui** — atsakyk vienareikšmiškai.
3. **Ar jau egzistuoja koks nors ryšio laukas** (`parent`, `chain`, `session`, `job_id`)? Netark — patikrink.

## Dalis B — MINIMALI JUNGTIS (tik jei A neranda jau esančios)
Pridėk **papildomus, neprivalomus** laukus: `chain_id` (grandinės identifikatorius) ir `chain_step` (eilės nr.).
- **PRIVALOMA: atgalinis suderinamumas.** Esami 15 pėdsakų be šių laukų turi likti galiojantys; `None`/nėra = OK.
- `--selftest` turi likti **PASS** (buvo 11/11). Pridėk bent 1 testą naujiems laukams + 1 testą, kad senos
  formos įrašas vis dar apdorojamas.
- **Projekcijos NEGENERUOK iš naujo ir jos formato NEKEISK** — sudėtinių trajektorijų generavimas yra
  ATSKIRAS human-gate. Šioje fazėje tik įrašom ryšį.

## Dalis C — BACKFILL (jei lieka laiko)
Pažymėk esamus 15 pėdsakų grandinėmis. **Išvesk grupavimą IŠ PAČIŲ PĖDSAKŲ** (fazės numeris ir tikslas
užduoties tekste), o mano žemiau pateiktą sąrašą naudok tik **kryžminei patikrai** — jei nesutampa, pranešk
neatitikimą, o **mano versijos aklai nepriimk**:
- **Anthropic rakto arka:** Fazės 35 (forensika) → 36 (žemėlapis) → 37 (valymas)
- **skillcapture statyba:** 38 (du sluoksniai) → 39 (vartai + FP auditas) → 40 (PHONE pataisa + atskiras indeksas)
- **GitHub PAT rotacija:** 43 (žemėlapis) → 44 (de-token) → 45 (patikra) → 46 (valymas) → 47 (pii auditas) → 48 (archyvo patikra)
- Pavieniai (be grandinės): 41 (LFM matavimas), 42 (SDK matavimas)
Jei kurio nors pėdsako priskirti negali užtikrintai — **palik be `chain_id`**, tai geriau nei klaidingas ryšys.

## Apribojimai
€0 · **BACKUP prieš keitimą** · push į privatų `hera-core-backup` · viešo `cad-site-agent` git NELIESK ·
`raw/` turinio NECITUOK (neredaguotas pagal dizainą — tik laukų vardai, ID, skaičiai) · `hera.env` NELIESK ·
HARD timeout, be retry. **Jei hook'as blokuoja saugesnį kelią — SUSTOK ir pranešk, o ne apeik.**

## Ataskaitoje
A: laukų sąrašas · **vienareikšmis atsakymas, ar fiksuojamas tarpinis samprotavimas** · ar buvo ryšio laukas ·
B: kas pridėta, selftest rezultatas, atgalinio suderinamumo įrodymas ·
C: kiek pėdsakų priskirta grandinėms, ar tavo grupavimas sutapo su mano · sąžiningas „ko nepadariau".

**ATASKAITOS TAISYKLĖ:** „neįmanoma / nepavyko" galioja tik su sąrašu, KĄ BANDEI.

Jei STOP — kodėl.

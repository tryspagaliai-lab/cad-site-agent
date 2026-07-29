UŽDUOTIS — Fazė 41: LFM2.5-Encoder įgyvendinamumo MATAVIMAS 4GB VPS'e + v1.2 WIP išsaugojimas. HUMAN-GATE GAUTAS („Varom"). <14 min.

## Dalis A (maža, DARYK PIRMA — pašalina realų praradimo pavojų, ~2 min)
`hera_semsearch.py` turi **nekomitintą v1.2 WIP diff'ą** (Fazė 40 jį teisingai paliko nepaliestą). Tai pažeidžia
mūsų durabilumo konvenciją: paruoštas, bet neįvertintas darbas guli VPS'e **be jokio backup'o** — kris mašina,
dings darbas. **Užkomitink jį į privatų `hera-core-backup` kaip AIŠKIAI PAŽYMĖTĄ WIP** (pvz. commit žinutėje
`WIP semsearch v1.2 — NOT EVALUATED, do not enable`), kad ateities sesija nepalaikytų jo patvirtintu.
**Elgsenos NEKEISK, eval'o NEDARYK, nieko neįjunk** — tik išsaugok tai, kas yra.

## Dalis B — LFM2.5-Encoder įgyvendinamumo matavimas

### Kodėl (kontekstas, kurio pats neišvestum)
Liquid AI 2026-07-28 išleido **LFM2.5-Encoder-230M / 350M** (atviri svoriai, Hugging Face). Tai **CPU modeliai**
— 8 192 žetonų kontekstas, ~3,7× greičiau nei ModernBERT-base ilgame kontekste, ~28 s vienam 8k praėjimui
nešiojamojo CPU. Mums įdomu dėl vieno konkretaus dalyko: **PII aptikimas (40 tipų, 16 kalbų)**.
Mūsų dabartinis `hera_pii.py` yra regex — Fazė 39 rado 9/9 klaidingai pozityvių, Fazė 40 lopė po vieną išimtį.
Enkoderis tai spręstų iš esmės. Antriniai kandidatai (NE šioje fazėje): zero-shot maršrutizavimas, „policy linting".

### Tai MATAVIMO užduotis, ne diegimo
**Nieko neprijunk prie jokio srauto. `hera_pii.py` NELIESK.** Tikslas — vienas sąžiningas atsakymas:
**ar 230M enkoderis apskritai realus šioje mašinoje, ir kokia kaina.**

Būtina išmatuoti ir pranešti skaičiais:
1. **RAM:** kiek laisvos atminties yra DABAR (su veikiančiu n8n + caddy + searxng + hera), ir kiek suvalgo
   modelis įkeltas. Jei nebetelpa — tai atsakymas, pranešk ir STOP (nesukelk OOM, kuris nužudytų n8n).
2. **Disko kaina:** svorių dydis + `transformers` priklausomybių dydis, jei jų dar nėra.
3. **Latencija MŪSŲ tekstams, ne 8k.** Tipinis pėdsakas ~18,6 KB. Išmatuok: šaltas krovimas (cold load) atskirai
   nuo inferencijos; inferencija tipiniam pėdsakui ir trumpam (~1 KB) tekstui. **Šaltas krovimas svarbus atskirai** —
   precedentas: embeddings atmesti `hera_verify`'ui, nes 1,2 s šaltas krovimas = 12% `timeout 10` biudžeto.
4. **Ar PII naudojimas apskritai reikalauja fine-tuning'o?** Blog'e PII aptikimas pateiktas kaip **demo iš
   fine-tune'into** enkoderio, o bazinis modelis duoda tik reprezentacijas. Jei tam reikia apmokymo (=GPU) —
   **tai kritinis radinys ir gali visą kryptį uždaryti dabar.** Patikrink, ar HF yra paruoštas PII checkpoint'as,
   ar tik bazinis. **Šis punktas svarbesnis už greičio skaičius** — jei atsakymas „reikia fine-tune", greitis nesvarbu.

### Ribos
- **€0.** Tik atviri svoriai iš HF. Jokių mokamų API.
- **NEDIEK į sisteminį python3.** Naudok `/opt/hera-venv` arba atskirą laikiną venv; jei diegi `transformers`,
  pasakyk, kiek vietos užėmė, ir ar palikai, ar išvalei.
- **n8n neturi nukentėti.** Jei matai, kad RAM prie ribos — sustok. Veikianti sistema > matavimas.
- Modelis reikalauja `trust_remote_code=True` — tai **savavališko kodo vykdymas iš HF**. Priimtina matavimui,
  bet **užfiksuok tai ataskaitoje kaip riziką** ir nepalik jo jokiame automatiniame kelyje.

### Ataskaitoje
Lentelė (RAM/diskas/šaltas krovimas/inferencija) · vienareikšmis atsakymas dėl fine-tuning'o poreikio ·
**tavo rekomendacija: verta ar ne, ir kodėl** · ką palikai diske ir ką išvalei.

## Apribojimai
€0 · BACKUP prieš keitimus · viešo `cad-site-agent` git NELIESK · HARD timeout, be retry · jokių secret reikšmių.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

Jei STOP — kodėl.

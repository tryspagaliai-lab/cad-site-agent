UŽDUOTIS — Fazė 38: skillcapture ĮJUNGIMAS (žalias archyvas) + redagavimo vartai prieš projekciją. HUMAN-GATE GAUTAS („Varom"). <14 min.

## Tikslas
`hera_skillcapture` (Fazė 23) + post-hook (Fazė 32) yra GYVI, bet `HERA_SKILLCAPTURE` = 0, tad **duomenys
nesikaupia**. Kiekviena diena be kaupimo = negrįžtamai neužfiksuoti mokymo duomenys.

Vartotojo sprendimas: **dviejų sluoksnių dizainas.** Rizika niekada nebuvo kaupime — ji yra indeksavime/naudojime:
- **Sluoksnis 1 — ŽALIAS pėdsakas:** privatus archyvas, **NIEKADA neindeksuojamas**, niekada nesiunčiamas
  išorėn. PII NEredaguojamas (ARCHYVUOJAM-NETRINAM — dar nežinom, kas bus vertinga LoRA/distiliacijai).
- **Sluoksnis 2 — PROJEKCIJA** (flat RAG + ShareGPT SFT): **tik ji** indeksuojama ir tik ji kada nors eitų į
  apmokymą. **Redagavimas vyksta ČIA**, o ne kaupimo momentu (kaupimo momentu tai negrįžtamai sunaikintų duomenis).

## Ką padaryti
1. **`HERA_SKILLCAPTURE=1`** — kaupimas įjungiamas.
   ⚠️ Tai **sąmoningas nukrypimas nuo „def 0" konvencijos** ir vienintelis šioje užduotyje. Pagrindas: kaupimas
   yra tik-rašymas be jokio vartotojo (niekas dar neskaito), tad fail-safe rizika minimali. **BET** privalu
   patvirtinti: jei capture nulūžta, **runner užduotis NEnulūžta** (timeout + `||true` izoliacija, kaip GoalAnchor
   Fazėje 22). Jei to dar nėra — pridėk.
2. **Redagavimo vartai projekcijos kelyje, `def 0`.** Projekcija (flat RAG / ShareGPT) **neturi išleisti
   išvesties**, kol redagavimas nepraėjo. Vartai patys lieka išjungti — jų įjungimas = ATSKIRAS human-gate.
   Esmė šioje fazėje: kelias fiziškai negali apeiti vartų, net jei kas nors ateityje pamirš.
3. **PIRMA PATIKRINK, ar redagavimo kodas jau egzistuoja.** Sistemoje yra PII/terse pajėgumas —
   **naudok jį pakartotinai, NEKURK dublio.** Jei esamas netinka, pasakyk kuo konkrečiai ir tik tada rašyk naują.
4. **Disko saugiklis.** VPS resursai riboti; žali pėdsakai augs neribotai. Įdėk dydžio saugiklį (riba + elgesys
   ją pasiekus: STOP kaupimą ir pranešk, NE tylus trynimas — trynimas pažeistų ARCHYVUOJAM-NETRINAM).
   Ataskaitoje nurodyk **išmatuotą** vieno pėdsako dydį ir prognozę MB/mėn. prie esamo tempo.

## PII klasės, kurias vartai turi gaudyti (mūsų domenas — pats neišvestum)
Secret'ai (`sk-ant-*`, bot token'ai, API raktai) · el. paštas · Telegram chat ID · IP adresai ·
mūsų infrastruktūros domenai/hostai · absoliutūs keliai su naudotojo vardu.
**Pritaikyk ką tik išmoktą pamoką (Fazė 37): secret'ų ieškom pagal REIKŠMĖS/šablono atitikimą, ne pagal
numanomų vietų sąrašą** — Fazė 36 praleido `/tmp/zz_ac.json` būtent todėl, kad enumeravo vietas.

## Apribojimai
€0 · fail-safe (klaida → no-op, ne crash) · **BACKUP prieš keitimą** + push į privatų `hera-core-backup` ·
viešo `cad-site-agent` git NELIESK · secret'ų reikšmių nespausdink · HARD timeout, be retry ·
`--selftest` be pytest.

## Sėkmės kriterijai (įrodymai ataskaitoje)
1. `--selftest` N/N PASS, įskaitant testą: **projekcija BLOKUOJAMA, kai redagavimo vartai nepraėję.**
2. Testas: **žalias sluoksnis PII NEredaguoja** (archyvas nepraranda duomenų) — abu sluoksniai patikrinti atskirai.
3. Testas: capture gedimas **NEnulaužia** runner užduoties.
4. Patvirtinimas, kad kaupimas realiai veikia: po įjungimo — **kiek pėdsakų atsirado, kokio dydžio, kur**.
5. Disko saugiklio riba ir prognozė MB/mėn.
6. Ar redagavimo kodas buvo panaudotas pakartotinai (kuris modulis) ar rašytas naujas (kodėl).
7. Sąžiningas „ko nepadariau / kas liko" sąrašas.

Jei STOP — kodėl.

# Fazė 53 — taryba: balsų žurnalas (matome) + turtinga santrauka už jungiklio (nekeičiam aklai). <14 min.

## Kodėl — rasta kode, ne spėta

`hera_council.py` funkcija `_juror_digest()` tarybos nariui (juror) siunčia **selektoriaus priežastį +
pirmus `JUROR_BODY_CHARS=3000` ženklus** kandidato, viskas apribota `JUROR_MAXCHARS=4000`. Priežastis
teisėta: Groq nemokama pakopa (free tier) meta 413 (per didelis siunčiamas krovinys).
**Pasekmė:** rugpjūčio įrašai buvo 11 925 / 14 575 / 15 159 / 22 553 ženklų ⇒ **taryba balsavo mačiusi
13–25% teksto, ir būtent PRADŽIĄ — YouTube įžangą.** Antras kokybės vartas tikrina TEMĄ, nes turinio nemato.

## Tikslas — dvi dalys, sąmoningai šia tvarka

**1. BALSŲ ŽURNALAS (visada įjungtas — tai stebimumas, ne elgsenos keitimas).**
Kiekvienas tarybos nario balsas rašomas į vault: laikas · įrašo id · **modelio pavadinimas** · tiekėjas
(groq/nvidia/gemini/openrouter) · verdiktas (keep/drop + domain_fit) · **viena eilutė pagrindimo** ·
santraukos (digest) dydis ženklais · ar balsas buvo galiojantis, ar krito (429/400/413/JSON klaida).
Šiandien vault'e yra TIK suminis „7 balsų" — kas balsavo ir ką pasakė, neįrašoma niekur. Be šito
negalim išmatuoti jokio tarybos pakeitimo.

**2. TURTINGA SANTRAUKA UŽ JUNGIKLIO `HERA_COUNCIL_RICHDIGEST`, DEFAULT 0.**
Vietoj žalios teksto PRADŽIOS siųsti **selektoriaus jau paruoštą struktūrizuotą ištrauką**
(ESMĖ + PAGRINDINIAI TAŠKAI + FAKTAI IR DUOMENYS). Ji jau egzistuoja, jos tankis didelis, papildomo
modelio kvietimo NEREIKIA ⇒ €0. Jei tos ištraukos konkrečiam įrašui nėra — **grįžti prie dabartinio
elgesio** (fail-safe, ne klaida).
⚠️ **Baitų ribų NEKELIAM.** Groq 413 yra tikras. Keičiasi tik TAI, KAS telpa į tą patį biudžetą.

## Apribojimai (nekintami)

- €0 · fail-safe (klaida → dabartinis elgesys, ne lūžis) · **BACKUP prieš keitimą** (į privatų
  `hera-core-backup`) · HARD laiko biudžetas, **NO retry**.
- Jungiklis `HERA_COUNCIL_RICHDIGEST` **default 0** — jokio elgsenos pokyčio be atskiro human-gate.
  Pirma kaupiam žurnalą su dabartine santrauka, paskui lyginam. **Nekeičiam varto aklai.**
- Žurnale — jokių raktų; modelių vardai ir verdiktai nėra paslaptis, bet užklausos kūno NEĮRAŠOM (tik dydį).
- Viešo `cad-site-agent` git'o neliesti.
- Jei laiko trūksta: **1 dalis pilnai, 2 palikti kitai fazei.** Žurnalas be jungiklio yra naudingas;
  jungiklis be žurnalo — ne.

## Sėkmės kriterijai (selftest, be pytest)

1. Po vieno tarybos paleidimo vault'e atsiranda įrašas su N eilučių = N bandytų tarybos narių, kiekviena
   su modelio pavadinimu, tiekėju, verdiktu ir santraukos dydžiu. Kritę balsai matomi kaip kritę, ne dingę.
2. `HERA_COUNCIL_RICHDIGEST=0` (numatytas): santrauka **baitas į baitą tokia pati kaip iki šio pakeitimo** —
   įrodyti palyginimu, ne teiginiu.
3. `HERA_COUNCIL_RICHDIGEST=1`: santrauka sudaryta iš struktūrizuotos ištraukos ir **telpa į tą pačią
   `JUROR_MAXCHARS` ribą**; jei ištraukos nėra — automatiškai grįžta prie senos santraukos.
4. Backup commit'as `hera-core-backup`.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

**BACKUP TAISYKLĖ:** backup failų **NIEKADA netrinti** — nei valymo komandoje, nei „jau nebereikalingas"
pagrindu. Palikimas kainuoja 0; trynimui reikia atskiro human-gate. Galioja ir tavo paties `.bak` failams.

**KALBOS TAISYKLĖ:** ataskaitoje kiekvienas angliškas terminas privalo turėti lietuvišką vertimą skliaustuose.

UŽDUOTIS — Fazė 48: ar `raw/` pėdsakų archyvas VIENTISAS? TIK SKAITYMAS. HUMAN-GATE GAUTAS („Varom"). <10 min.

## Kodėl — konkreti neatitiktis, ne nerimas
- **Fazė 40 (07-30)** išmatavo: `/root/hera_skills/raw/` = **7 pėdsakai**, vidutiniškai ~18,6 KB → ~130 KB.
- **Fazė 41 (07-30)** tą patį patvirtino nepriklausomai (18,6 KB/pėdsaką, tempas 2,4/d.).
- **Fazė 47 (07-31)** rašo: „`raw/` turi tik **1 mažą legacy failą (26 KB)**, be PII".

**Tai prieštarauja.** Bet **NEKALTINK, kol nepatikrinsi** — labai tikėtina nekalta priežastis: Fazė 47 ieškojo
konkretaus nescrubbed korpuso failo, iš kurio buvo skaičiuotas 0,0515% tankis, o ne katalogo turinio.
Projekcija (190 KB) atitinka ~7 pėdsakus, tad duomenys greičiausiai VIETOJE.
*(Precedentas: GoalAnchor „senos kopijos" hipotezė 07-27 irgi atrodė akivaizdi ir nepasitvirtino.)*

**Kodėl vis tiek tikrinam:** `raw/` yra **LoRA/distiliavimo archyvas**, saugomas taisykle ARCHYVUOJAM-NETRINAM.
Tylus jo praradimas nepasirodytų NIEKUR, kol neprireiktų — o tada būtų per vėlu.

## 🔴 TIK SKAITYMAS
Nieko netrink, nekurk, neperkelk, netaisyk. Net jei rastum problemą — **PRANEŠK, NETAISYK.** Jei kas nors dingę,
neteisingas veiksmas gali sunaikinti likusius pėdsakus arba perrašyti tai, ką dar galima atkurti.

## Ką nustatyti

1. **Faktinė `/root/hera_skills/` struktūra:** išvardyk katalogus ir kiekviename failų skaičių + bendrą dydį.
   Konkrečiai `raw/`, `projection/`, ir bet kokius kitus.
2. **`raw/` turinys:** kiek `skill_*.json` (+ ar yra `.md` porų), kiek kitų failų, kiekvieno dydis ir **mtime**.
   Ar yra `_legacy_unscrubbed_rag_corpus.jsonl.pre-gate` (Fazės 38 karantinas) — jo 26 KB gali paaiškinti
   Fazės 47 teiginį.
3. **⭐ Kryžminis sutikrinimas su projekcija:** `projection/rag_corpus.jsonl` ir `sft_corpus.jsonl` eilučių skaičius,
   ir ar kiekvienai projekcijos eilutei egzistuoja atitinkamas `raw/` pėdsakas (pagal `skill_id` ar analogišką lauką).
   **Tai vienintelis tikras vientisumo testas:** projekcija generuojama IŠ raw, tad projekcijos įrašas be raw
   šaltinio = prarastas archyvas.
4. **Ar per pastarąsias paras kas nors trynė?** Patikrink, ar Fazės 46 valymas (kuris trynė backup'us) galėjo
   paliesti `raw/`. Konkrečiai: ar `hera_skills` kataloge nėra pėdsakų, kad failai buvo pašalinti
   (pvz. mtime šuolis kataloge be atitinkamo naujo turinio).
5. **Ar kaupimas vis dar veikia?** Paskutinio pėdsako data — ar atitinka paskutines fazes (45/46/47)?
   Jei naujausias pėdsakas senas, tai reikštų, kad **capture nustojo veikti**, ir tai būtų atskira, tyli problema.

## Ataskaitoje
Lentelė: katalogas → failų sk. → dydis · `raw/` failų sąrašas (vardai, dydžiai, mtime) ·
**kryžminio sutikrinimo rezultatas (projekcijos eilutės vs raw pėdsakai)** ·
vienareikšmis verdiktas: **archyvas VIENTISAS / TRŪKSTA N / NEAIŠKU + kodėl** ·
ar capture vis dar kaupia · sąžiningas „ko nepavyko".

## Apribojimai
€0 · nieko nekeisti · jokių PII/secret reikšmių ataskaitoje (`raw/` yra NEREDAGUOTAS pagal dizainą — **jokio jo
turinio necituok**, tik metaduomenis: vardus, dydžius, datas, laukų pavadinimus) · HARD timeout, be retry.
**Jei saugesnį kelią blokuoja hook'as — SUSTOK ir pranešk, o ne apeik.**

**ATASKAITOS TAISYKLĖ:** „neįmanoma / nepavyko" galioja tik su sąrašu, KĄ BANDEI.

Jei STOP — kodėl.

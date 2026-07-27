UŽDUOTIS — Fazė 33: tarybos juror ĮVAIROVĖ — riboti balsus per tiekėją. <14 min.

## Tikslas
€0 tarybos juror-set **groq-dominuojamas**: tipiškai ~5 iš 7 balsų yra tas pats tiekėjas (groq-1..5 = multi-sample
to paties provider'io), + 1 glm + 1 gemini. Todėl „konsensusas" iš dalies reiškia, kad **groq sutinka su savimi** —
balsų daug, bet **nepriklausomų šeimų mažai**. Vartotojo sprendimas: **riboti balsų skaičių per tiekėją**
(pvz. max 2 groq vietoj 5), kad kiekvienas balsas būtų kiek įmanoma nepriklausomas.

**Kodėl tai svarbu (trys nepriklausomi pagrindimai):** PlanFlip — heterogeniška modelių įvairovė yra BŪTINA
daugiaagenčių sistemų saugumo sąlyga, redundancija homogeniškoje sistemoje neapsaugo · TRSP (spektrinė analizė) —
stiprus maišymasis be struktūrinio apribojimo matematiškai garantuoja įvairovės (efektyviojo rango) kritimą ·
mūsų pačių 2026-07-22 pastebėjimas. **Principas: balsų SKAIČIUS ≠ įvairovė.**

## 🔴 Kritinis apribojimas
**Taryba naudojama REALIEMS HERA sprendimams** (pvz. „ar įjungti diffrules", „ar statyti DXF grandinę").
**Sugedusi taryba blogiau nei šališka.** Jei ribojimas sugriautų agregavimą (median/spread/slenksčiai su mažesniu
balsų skaičiumi) — geriau grąžink mažiau funkcijų ir pasakyk, nei palik veikiančią-bet-neteisingą.

## Realybė (ko pats neišvestum)
- ⚠️ **KELIAI:** Fazė 31 nustatė, kad kanoninis modulių kelias yra `/opt/hera-processor/`, BET `hera_council_ask.py`
  runner'yje (51 eil.) **sąmoningai kviečiamas iš `/opt/cad-site-agent/n8n/hera/`** — taryba yra IŠIMTIS.
  **Pirma nustatyk, kurį `hera_council.py` / `hera_council_ask.py` realiai vykdo gyvas kelias, ir taisyk TĄ.**
  Nekartok Fazės 30 klaidos (pataisyta kopija, kurios niekas nevykdo). Patikrink faktu, ne prielaida.
- €0 juror-set: groq (multi-model/multi-sample) + glm + gemini. Mokami (deepseek/mimo/openai/nvidia) praleidžiami —
  tai turi likti taip.
- Žinomas atskiras apribojimas: `gemini-2.5-flash` JSON nukertamas net su maxOutputTokens=2048 (vidinis „thinking"),
  `gemini-flash-latest` veikia. Tai NE šios užduoties dalis, bet turi įtakos, kiek gemini balsų realiai įsiskaito —
  atsižvelk skaičiuodamas įvairovę.
- Agregavimas: `hera_council` naudoja verdict/score/spread/std, skalė 0–10, promote riba ~7.5.

## Apribojimai
€0 (jokių mokamų jurorų). Fail-safe: jei kuri nors šeima krenta — taryba turi veikti su likusiomis, ne griūti.
BACKUP prieš keitimą. Ataskaita TIK į HERA botą. Viešo `cad-site-agent` **git istorijos** NELIESK (failai ten untracked —
turinį keisti galima, bet `git status` turi likti nepakitęs). Secret'us NEliesk. Runner'io logikos NEKEISK — tik tarybos modulį.
Cap reikšmę pasirink pats ir **pagrįsk** (2 yra siūlymas, ne įsakymas).

## Įrodymai
1. **Kurį kelią gyvas srautas realiai vykdo** — parodyk faktu (grep/ls), ir patvirtink, kad taisei TĄ patį.
2. **Prieš/po juror sudėtis** ant to paties realaus klausimo: kiek balsų, iš kiek **nepriklausomų šeimų**.
   Ataskaitoje rodyk abu skaičius (pvz. „4 balsai / 3 šeimos") — tai ir yra pataisos matas.
3. **Agregavimas nesugedo:** su mažesniu balsų skaičiumi median/spread/verdict skaičiuojami korektiškai; parodyk
   realaus paleidimo rezultatą su tikru klausimu (naudok bet kokį nekenksmingą HERA klausimą).
4. **€0 patvirtinta:** jokio 402, jokio mokamo juroro neįsijungė.
5. **Fail-safe:** imituok vienos šeimos gedimą → taryba vis tiek grąžina verdiktą su likusiomis.
6. BACKUP + push į `hera-core-backup`; ROADMAP.md eilutė (**patikrink grep'u faile**).
7. **Rekomendacija:** ar po pataisos verdiktai atrodo patikimesni, ar imtis tapo per maža? Sąžiningai.

Jei STOP — kodėl.

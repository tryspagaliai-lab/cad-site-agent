UŽDUOTIS — Fazė 25 (ETAPAS 2): hera_planrender.py — švarus planas PNG → AI 3D renderis (Gemini). <14 min.
NEleisk pytest (tik savo selftest). Fail-safe. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme. Secret'us NEliesk (naudok esamą Gemini raktą kaip kiti hera moduliai; rakto NESPAUSDINK niekur).

🔴 SVARBIAUSIA — €0 DISCIPLINA. Gemini VAIZDŲ GENERAVIMAS gali BŪTI MOKAMAS (skirtingai nei tekstas):
- PIRMAS žingsnis = PROBE (patikra), ar turimas raktas turi NEMOKAMĄ prieigą prie vaizdų generavimo modelio.
- Jei paaiškėtų, kad tai MOKAMA arba neaišku → **STOP, NIEKO NEGENERUOK, praneša.** Geriau nepadaryta nei sudeginti pinigus.
- NEĮVESK jokio naujo mokamo tiekėjo. NEregistruok nieko. Tik esamas raktas.

KONTEKSTAS: Fazė 24 (ETAPAS 1) baigta — hera_dxf2png.py verčia DXF į švarų 2D plano PNG (interpretatorius /opt/cad-venv, ezdxf 1.4.4 + matplotlib).
Dabar ETAPAS 2: tą PNG paduoti AI vaizdų generavimui → 3D izometrinis renderis (kaip video: „create a 3d isometric floor plan render").
Taryba pritarė (7/9), BET komercinė vertė KVALIFIKUOTA: tai KONCEPCINIS JUODRAŠTIS / lead-gen, NE galutinis ArchViz.
Šį sąžiningą pozicionavimą ĮRAŠYK į modulio docstring'ą ir ataskaitą — jokio over-selling.

1) PROBE (€0 patikra, PRIEŠ rašant generavimo kodą):
   a) Kokie vaizdų generavimo modeliai pasiekiami esamu Gemini raktu? (pvz. bandyk models.list arba analogiškai kaip hera gemini.py daro; ieškok image/vaizdų generavimo gebėjimo).
   b) Nustatyk ar tai NEMOKAMA pakopa. Jei API grąžina 429/quota — tai limitas (ok, €0). Jei 402/billing required/„paid tier only" → MOKAMA.
   c) Ataskaitoj aiškiai pasakyk ką radai. JEI MOKAMA/NEAIŠKU → eik į 4) (modulis be gyvo generavimo), NEBANDYK generuoti.

2) Sukurk /root/hera_planrender.py:
   - Jungiklis: HERA_PLANRENDER def 0 = DRY-RUN (sudaro užklausą (prompt), grąžina ją, BET NEKVIEČIA API, nieko negeneruoja — €0 saugus default). =1 → realus kvietimas.
   - API: `render_3d(png_path, style="realistic", materials=None, extra=None, out_dir="/root/hera_planrender") -> dict`
     grąžina {ok, prompt_used, out_path|None, api_called: bool, cost_note, msg}.
   - UŽKLAUSOS SUDARYMAS (determ. šablonas, BE LLM — pigiau ir nuspėjamiau):
     bazė: "Create a 3D isometric floor plan render from this 2D architectural plan. Realistic, professional lighting.
     PRESERVE the exact room layout, wall positions and proportions from the source plan — do not invent or move rooms."
     + jei materials (pvz. "marble and wooden floor") → pridėk medžiagų sakinį; + extra (pvz. "add decoration to the walls") → pridėk.
     ⚠️ „PRESERVE exact layout" sakinys BŪTINAS — taryba įspėjo, kad AI haliucinuoja geometriją/mastelį. Tai mūsų mitigacija užklausos lygyje.
   - PASIRENKAMAS „prompt-apie-prompt" (iš ingest'o + token-offloading principo): jei HERA_PLANRENDER_SMARTPROMPT=1 (def 0),
     NEMOKAMAS tekstinis modelis (groq arba gemini-flash — tas pats kelias kaip taryboje) parašo detalesnę užklausą; jei jis krenta → fail-safe į determ. šabloną.
   - Jei generavimas MOKAMAS/neprieinamas → funkcija grąžina {ok:False, api_called:False, cost_note:"vaizdų generavimas nemokamai neprieinamas", prompt_used:<užklausa>}
     T.y. modulis VIS TIEK naudingas: paruošia užklausą, kurią vartotojas gali RANKINIU BŪDU įklijuoti į Gemini naršyklėje (tiksliai kaip video autorius daro). Tai €0 kelias.
   - FAIL-SAFE: bet kokia klaida (tinklas, API, diskas) → {ok:False, msg:<priežastis>} + log /root/hera_planrender.log. NIEKAD necrashink. NIEKAD nekartok kvietimo ciklu (jokių retry — kad neišeikvotų kvotos).
   - Docstring'e SĄŽININGAI: „Koncepcinis juodraštis / lead-gen. NEPAKEIČIA 3D modeliavimo ir tikslaus ArchViz renderio. AI gali iškraipyti geometriją/mastelį — visada patikrink rezultatą."

3) GYVAS TESTAS — TIK JEI 1) parodė NEMOKAMĄ prieigą:
   - Paimk realų PNG: paleisk hera_dxf2png.py ant to paties realaus DXF (reports/analysis/roman_gardens_gapclosed.hatches_6b_review.dxf) → gauk švarų PNG.
   - Paleisk render_3d su HERA_PLANRENDER=1 VIENĄ KARTĄ (vieną kvietimą, jokių kartojimų).
   - Ataskaitoj: ar gavo vaizdą, kelias, dydis, ir SĄŽININGAS vertinimas — ar išlaikytas planas, ar AI haliucinavo.
   - Jei kvota/429 → tai NORMALU, pažymėk ir eik toliau (ne klaida).

4) SELFTEST (`--selftest`, BE tinklo, BE pytest) — VISADA daromas, net jei generavimas neprieinamas:
   (a) užklausos sudarymas: render_3d(dry-run) → prompt_used turi „PRESERVE" sakinį + bazę; api_called=False; failas nesukurtas.
   (b) materials/extra: perduoti "marble and wooden floor" + "add decoration to the walls" → abu atsispindi užklausoje.
   (c) def 0: HERA_PLANRENDER=0 → api_called=False garantuotai (net jei raktas yra).
   (d) fail-safe: neegzistuojantis png_path → ok=False, aiški msg, ne crash.
   Spausdink PASS/FAIL.

5) BACKUP: cp /root/hera_planrender.py į /opt/hera-processor/ + commit/push į PRIVATŲ hera-core-backup (TIK šis failas).
   Vault ROADMAP.md 1 eilutė: „Fazė 25 hera_planrender (ETAPAS 2) — ĮDIEGTA <data>, HERA_PLANRENDER def 0 dry-run, planas PNG→AI 3D renderis (Gemini),
   determ. užklausa su 'PRESERVE layout' mitigacija; pozicionuota kaip koncepcinis juodraštis NE galutinis ArchViz; €0 fallback = rankinis užklausos naudojimas."

ATASKAITA (HERA botas, trumpai): PROBE rezultatas (ar vaizdų generavimas NEMOKAMAS — aiškiai TAIP/NE/neaišku, ir kuo remiesi);
ar gyvas testas paleistas (jei taip — ar išlaikė planą, sąžiningas vertinimas; jei ne — kodėl, ir tai OK);
selftest a/b/c/d PASS/FAIL; backup+push; ROADMAP. Jei STOP dėl kaštų — aiškiai pasakyk, tai TEISINGAS elgesys.
KIEK IŠLEISTA: privalomai pasakyk „€0" arba tikslią sumą jei kažkas kainavo (neturėtų).

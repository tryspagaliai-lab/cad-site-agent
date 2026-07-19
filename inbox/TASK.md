UŽDUOTIS — SKUBU: dump'ink PILNĄ ai_digest.py paieškos šaltinių sąrašą + patikrink ar veikia. <6 min.
NEleisk pytest. Fail-safe. €0. Raktų nespausdink. JOKIŲ tinklo kvietimų/LLM (grynas cat/grep — anti-rc124).
Ataskaita TIK į HERA botą. Nieko NEKEISK — tik SKAITYK ir išvardink.

TIKSLAS: vartotojas nori tikslaus sąrašo KUR ai_digest.py atlieka paieškas + ar praplėtimas (CN/JP/KR + TLDR) vietoj.

ŽINGSNIAI (be jokio keitimo):
1) Perskaityk `/root/ai_digest.py` (ar kur jis yra). Išvardink PAPUNKČIUI:
   - VISUS RSS FEEDS (kiekvienas: pavadinimas + URL). Ne kiekį — visą sąrašą.
   - VISUS HF_ORGS / HuggingFace organizacijas (visus vardus, papunkčiui).
   - Bet kokius kitus paieškos šaltinius (arXiv, GitHub, SearXNG queries — jei yra).
2) Patikrink AR VEIKIA:
   - Ar cron įrašas aktyvus (kada paskutinį kartą suko)?
   - `seen.jsonl` dydis / eilučių sk. (ar seen-būsena gyva)?
   - Paskutinis digest run rezultatas (jei yra log) — kiek naujų siuntė paskutinį kartą, ar „nieko naujo"?
   - Ar TELEGRAM_TOKEN→@tryspagaliabot maršrutas sveikas?
3) Jei kurio šaltinio (pvz. CN/JP/KR ar TLDR) NĖRA kode — aiškiai pažymėk „TRŪKSTA: X".

ATASKAITA (HERA botas — PAPUNKČIUI, be komentarų):
(a) FEEDS sąrašas (visi, vardas+URL);
(b) HF_ORGS sąrašas (visi);
(c) kiti šaltiniai;
(d) cron aktyvus? paskutinis run kada?
(e) seen.jsonl eilučių sk.;
(f) paskutinis run: kiek naujų / „nieko naujo";
(g) ko TRŪKSTA (jei ko nors nėra).

UŽDUOTIS — READ-ONLY recon: kodėl design digest įrašai „pliki" (be „Kas tai/Kur panaudoti") o news botas turi pilną aprašą? NIEKO NEKEISK. <8 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Secret'us NEliesk/redaguok.

KONTEKSTAS: vartotojas: design botas siunčia tik „pavadinimas + [šaltinis] + nuoroda", BE 2-3 sakinių „Kas tai" + „Kur panaudoti"
usage aprašo. News/AI botas turi pilną aprašą. Bendra taisyklė: KIEKVIENAS botas turi turėti tą usage aprašą. Reikia suprasti KODĖL
design (ir gal agro/aitech) jo negauna — prieš taisant. Failas: /root/ai_digest.py.

ŽINGSNIAI (visi read-only, tik skaitymas/parodymas):
1) Parodyk kaip formatuojamas/sudaromas per-item output. Ar yra Gemini „summarize/usage" funkcija, kuri generuoja „Kas tai"+„Kur panaudoti"?
   Kur ji kviečiama? (grep 'Kas tai\|Kur panaudoti\|summariz\|gemini\|usage\|def send\|def format\|def render' ai_digest.py; parodyk funkcijų parašus + kur kviečiama).
2) Ar usage-enrichment taikomas VISOMS temoms (ai/design/agro/aitech) vienodai, ar TIK `ai` temai? Parodyk per-topic siuntimo/formatavimo kelią —
   ar design eina per tą patį enrichment kaip ai, ar per paprastesnį (title+link) kelią.
3) Jei design eina per enrichment BET vis tiek pliki — ar enrichment TYLIAI fail'ina (pvz. Gemini timeout/klaida → fallback bare)?
   Patikrink logus (jei yra) ar paskutinis design run rodo klaidą/fallback.
4) Parodyk DABARTINIUS design temos feeds (TOPICS['design']['feeds'] + github_atom + arxiv_cats + filter_kw).
5) Trumpai: koks MINIMALUS pakeitimas priverstų design (ir agro/aitech) naudoti tą patį „Kas tai/Kur panaudoti" enrichment kaip ai — ar tai
   bendros funkcijos iškvietimas visoms temoms, ar per-topic vėliavos, ar enrichment kodo dubliavimas. (Tik ĮVERTINK, NEDARYK.)

ATASKAITA (HERA botas, trumpai): (1) enrichment funkcija+kur kviečiama; (2) taikoma visoms ar tik ai; (3) ar design fail'ina/fallback; (4) design feeds sąrašas;
(5) minimalus fix įvertinimas (kokį kodą liest). Nieko nekeisk.

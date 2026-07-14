UŽDUOTIS — SKUBU: naujienų digest KARTOJASI (ta pati ataskaita 3–4 dienas). Rask priežastį + pataisyk. <12 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe. Raktų nespausdink. €0.
DIAGNOZĖ+FIX ataskaita eina TIK į HERA botą (HERA_BOT_TOKEN). Naujienų srauto botas (@tryspagaliabot / TELEGRAM_TOKEN)
LIEKA naujienoms — routing NEKEISK, tik turinys turi būti NAUJAS.

PROBLEMA: vartotojas kelias dienas iš eilės gauna TĄ PATĮ naujienų digestą į @tryspagaliabot — jokių naujų įrašų,
nors praplėtėm šaltinius (CN/JP/KR labs + TLDR). Beveik tikrai lūžusi dedup/„seen"-būsena: digest siunčia tuos pačius
top-N kiekvieną kartą, o ne TIK naujus nuo praeito karto.

ANTI-RC124 (privaloma, nes praeitas diagnostinis pakibo): JOKIO tinklo fetch diagnozės metu. Jei darai gyvą patikrą —
TIK 1 kartą, HARD ≤40s timeout visai, JOKIO retry; jei nefetch'ina — PRALEISK, naudok logikos patikrą su fake įrašais.
Nekursi nieko sunkaus. Baik per <12 min bet kokiu atveju.

ŽINGSNIAI:

1) DIAGNOZĖ (deterministinė, be tinklo): perskaityk `/opt/.../ai_digest.py` (ar kur jis yra; rask `ai_digest`
   per systemctl/cron/find) IR jo „seen/sent"-būsenos failą. Nustatyk KODĖL kartojasi. Įtariami:
   (a) nėra persistent „seen"-set → kas kartą siunčia tą patį top-N;
   (b) „seen"-set yra, bet neįsirašo (permission/crash/kelias) → resend;
   (c) rikiuoja pagal relevance, ne pagal šviežumą/datą → tie patys evergreen viršuje;
   (d) laiko langas blogas.
   Ataskaitoje parašyk tikslią priežastį (1–2 sakiniai) + failo/eilutės nuoroda.

2) FIX (minimalus, tikslinis — NEperrašinėk viso failo):
   - PERSISTENT „seen"-set: kiekvienas įrašas identifikuojamas stabiliu raktu (URL arba guid/title hash).
     Įrašų raktai saugomi patvariame faile (pvz. /var/lib/ai_digest/seen.jsonl ar šalia esamo state; sukurk katalogą
     jei reikia, atominis write: temp→rename). Po sėkmingo siuntimo — raktai įrašomi.
   - Kiekvienas run siunčia TIK įrašus, kurių rakto NĖRA „seen". Rikiuok pagal ŠVIEŽUMĄ (published desc).
   - Jei 0 naujų → NEsiųsk seno; siųsk trumpą „🗞️ nieko naujo" (arba tylėk, jei taip sukonfigūruota) — NIEKADA
     nekartok senų įrašų.
   - Apsauga nuo begalinio augimo: „seen" apkarpyk iki paskutinių ~1000 raktų (arba 30 d.).
   - Fail-safe: jei „seen" failo nepavyksta perskaityti/įrašyti → logink, elkis atsargiai (geriau praleisti nei
     spam'inti), NIEKADA rc≠0.

3) PATIKRINK ŠALTINIUS: patvirtink kad CN/JP/KR labs + TLDR feeds TIKRAI įjungti į ai_digest.py (ne tik
   hera_research watch-queries). Jei kurio nėra — pridėk (deterministiškai). Parodyk feeds sąrašo ilgį.

4) VERIFIKACIJA (be pakibimo):
   - LOGIKOS testas (VISADA, be tinklo): paduok 5 fake įrašus, „pažymėk" 3 kaip seen → digest turi siųsti TIK 2
     naujus; antras run su tais pačiais → 0 naujų → „nieko naujo". Parodyk rezultatą.
   - GYVA patikra (NEBŪTINA, tik jei saugu): 1 fetch, HARD ≤40s, dry-run (NEsiųsk į botą) — parodyk kiek NAUJŲ
     rastų. Jei timeout/klaida → praleisk, logikos testo pakanka.

5) BACKUP: commit pataisą į privatų repo (ten kur ai_digest.py versijuojamas; jei niekur — pradėk versijuoti ar bent
   įrašyk kopiją į hera-core-backup). Persistent askpass jau yra. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Routing NEKEISK (naujienos→@tryspagaliabot, ataskaita→HERA botas). Viešo cad-site-agent NELIESK.
Jokio pytest-all. Jei ai_digest.py nerandi — pranešk kur ieškojai, NEkurk naujo.

ATASKAITA (HERA botas, trumpai): (a) tiksli priežastis kodėl kartojosi; (b) kas pataisyta (seen-set + recency + „0 naujų"
elgesys); (c) feeds sąrašo ilgis + ar CN/JP/KR+TLDR yra; (d) logikos testas: 5→2→0 rezultatas; (e) gyva patikra (kiek
naujų / arba „praleista"); (f) backup push OK/ne. Baik greitai.

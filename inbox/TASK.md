UŽDUOTIS — Fazė 30: `hera_verify` vertintojo pataisa (du bug'ai, rasti Fazės 29 matavimu). <14 min.

## Tikslas
Fazė 29 stebėjimo režimu įrodė, kad vertintojas NETINKAMAS retry. Du defektai:
1. **`parse_rubric` skilties aptikimas:** ieško pirmos eilutės, KURI PAMINI „įrodymai" — ne ANTRAŠTĖS. Kai proza mini tą
   žodį prieš tikrą `## Įrodymai` antraštę → ištraukiama klaidinga skiltis. F27 → 0 kriterijų vietoj 8; pačios F29
   užduoties → 0 vietoj ~7.
2. **Slenkstis per griežtas:** kai skiltis ištraukta teisingai (F26, F28), leksinis dengimas 0.6 davė **0/7 pass ABIEM
   realiai SĖKMINGOMS** užduotims. Realios ataskaitos PARAFRAZUOJA kriterijus, nekartoja pažodžiui.
Sutvarkyk abu taip, kad vertintojas taptų pakankamai tikslus retry sprendimui.

## Realybė (ko pats neišvestum)
- `hera_verify.py` (Fazė 27) + `VE_NOTE` runner integracija (Fazė 29, `HERA_VERIFY_CHECK` def 0, IŠJUNGTA).
- **Etaloninis rinkinys jau egzistuoja ir yra vertingesnis nei sintetiniai testai:** Fazių 26, 27, 28, 29 tikri
  `inbox/TASK.md` + jų tikros ataskaitos. **Visos keturios realybėje SĖKMINGOS** — vadinasi teisingas vertintojas
  turi duoti daugumai kriterijų `pass`. Naudok tai kaip matavimo pagrindą prieš/po.
- HERA turi `hera_semsearch` su DAUGIAKALBIU embedding modeliu (fastembed `paraphrase-multilingual-MiniLM`) — tai
  galimas kelias parafrazių problemai. **Bet įvertink kainą:** vertintojas kviečiamas kiekviename runner cikle su
  `timeout 10`. Jei embeddings per lėti ar per sunkūs 4GB VPS — rinkis leksinį sprendimą (sinonimai, dalinis
  atitikimas, žemesnis slenkstis) ir PASAKYK kodėl. Sprendimas tavo, bet pagrįsk skaičiais.
- Ta pati „parafrazė ≠ pažodžiui" problema jau spręsta projekte: `hera_goalanchor` naudoja **kalbai invariantinius
  inkaro atomus**, `hera_faithfulness` — atomų grounding'ą. Perpanaudok idėją, jei tinka.

## Apribojimai
€0, be tinklo (jei naudosi embeddings — TIK lokalų fastembed, jokių API). Fail-safe: klaida → „praeita", niekada
neblokuoti. **Retry VIS DAR NEĮJUNGIAMAS** — `HERA_VERIFY_CHECK` lieka def 0, runner'io logikos NEKEISK.
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. BACKUP prieš keitimą. Cron/secret'ai NELIESK.

## Įrodymai
1. **Antraštės bug'as ištaisytas:** F27 ir F29 TASK.md dabar duoda teisingą kriterijų skaičių (buvo 0). Parodyk prieš/po.
2. **PAGRINDINIS MATAVIMAS — tikslumas ant etaloninio rinkinio (F26/27/28/29):** kiek `pass`/`fail`/`undecided`
   PRIEŠ pataisą ir PO. Kadangi visos keturios realiai pavyko, tikslas — dauguma kriterijų `pass`, MAŽAI klaidingų `fail`.
   Pateik lentelę su skaičiais.
3. **Klaidingų `pass` patikra (svarbu!):** sukurk atvejį, kur išvestis SĄMONINGAI neįvykdo kriterijaus → turi būti `fail`.
   Nesuvelk vertintojo į „viską praleidžia" — tai būtų blogiau nei dabar.
4. Greitis: kiek trunka vienas vertinimas (turi tilpti į `timeout 10` su atsarga). Pateik matavimą.
5. Esami selftest'ai (8/8) toliau PASS; `bash -n` runner OK (nors jo nekeiti).
6. BACKUP + push į privatų `hera-core-backup`; **ROADMAP.md eilutė — ir PATIKRINK, kad ji tikrai faile atsirado**
   (F26–F29 ataskaitos teigė ROADMAP atnaujinimą, o įrašų nebuvo; nekartok).
7. **Rekomendacija:** ar dabar vertintojas pakankamai tikslus retry įjungimui? Sąžiningai, su skaičiais.

Jei STOP — kodėl.

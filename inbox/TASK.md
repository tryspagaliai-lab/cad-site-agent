UŽDUOTIS — hera_lint aprėpties auditas ir pataisa. <13 min.

## Tikslas
`hera_lint` (Loop B) raportuoja per gerą vaizdą. Loop B rodo `orphan ~17 · dangling ~23`, o nepriklausomas
skaičiavimas per VISUS vault `.md` failus (2026-07-26, orchestratorius) davė **140 unikalių nutrūkusių taikinių /
980 paminėjimų ir 245 našlaičius iš 391 užrašo**. Nustatyk KODĖL skiriasi ir sutvarkyk taip, kad Loop B rodytų tiesą.
Klaidingas „viskas švaru" yra blogiau nei bloga metrika.

## Realybė (ko pats neišvestum)
- Vault ant VPS: `/opt/hera-vault` (privatus; sinchronizuojamas `hera_vault_sync.sh` kas 30 min).
- Nepriklausomas skaičiavimas darytas taip: visi `*.md` rekursyviai (be `.git`), nuorodos per `\[\[([^\]|#]+)`,
  taikinys laikomas išspręstu jei sutampa su bet kurio failo **stem** (Obsidian semantika: basename be `.md`).
- Orchestratorius ką tik pridėjo `concepts/` aplanką (15 koncepcijų mazgų) — po jų nutrūkę paminėjimai 980→767.
  Tavo skaičiai gali skirtis nuo 980, jei vault jau sinchronizuotas — tai NORMALU, svarbu dydžio eilė.
- Žinomas triukšmas, kurį verta traktuoti atskirai (NE tikros nuorodos, o dokumentacijos vietaženkliai):
  `[[...]]`, `[[slug]]`, `[[YYYY-MM-DD-jobid]]`, `[[TESTDOCBOUND]]`.

## Apribojimai
€0, be tinklo, be LLM (grynai deterministiška). Fail-safe. NEleisk pytest. Ataskaita TIK į HERA botą.
Viešo `cad-site-agent` NELIESK git prasme. Secret'us NEliesk. BACKUP prieš keitimą.
**NIEKO NETRINK ir neperrašinėk vault turinio** — ši užduotis TIK matuoja ir taiso MATAVIMĄ, ne duomenis.
Jei pataisa keistų Loop B elgesį rizikingai — palik kaip yra ir praneša.

## Įrodymai (ko tikiuosi ataskaitoje)
1. **Šakninė priežastis** — kokia tiksliai `hera_lint` aprėptis dabar (kokie aplankai/failai skenuojami, kokia
   nuorodų regex, kaip sprendžiamas taikinys) ir kuris iš tų dalykų sukelia neatitikimą.
2. **Skaičiai prieš/po** — `hera_lint` išvestis dabar vs po pataisos, greta nepriklausomo skaičiavimo. Turi sutapti
   (arba skirtumas turi būti PAAIŠKINTAS, pvz. sąmoningai neįskaičiuoti vietaženkliai).
3. **Vietaženkliai** — ar juos atskyrei nuo tikrų nutrūkusių nuorodų (rekomenduoju atskirą skaičių, ne sumaišytą).
4. Selftest arba lygiavertis patikrinimas, kad pataisyta lint versija neužlūžta ir Loop B toliau veikia.
5. BACKUP + push į privatų `hera-core-backup`; ROADMAP.md eilutė.

Jei STOP — kodėl + ką radai apie dabartinę aprėptį.

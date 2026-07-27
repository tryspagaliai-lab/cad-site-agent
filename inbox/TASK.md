UŽDUOTIS — Fazė 34: `hera_lint` aprėptis — įtraukti `archive/` kaip išsprendžiamą taikinį. <10 min.

## Tikslas
2026-07-27 archyvuota 20 growth užrašų į `archive/growth-superseded-2026-07-27/` (vartotojo sprendimas:
**archyvuojam, netrinam** — neapdoroti pėdsakai yra potenciali būsimos treniruotės medžiaga).
Failai NEDINGO, bet išėjo iš `hera_lint` aprėpties → Loop B dabar rodo **dangling 10 → 29, orphan 28 → 41**.
Patikrinta faktu: **26 nuorodos (8 unikalūs taikiniai) iš `skills/growth/concepts` rodo į archyvuotus failus.**
Tai MATAVIMO, ne turinio problema — Obsidian grafe tos nuorodos veikia (jis sprendžia pagal basename).
Sutvarkyk, kad lint jas vėl matytų kaip išsprendžiamas.

## Realybė (ko pats neišvestum)
- Fazė 31 (2026-07-26) jau pridėjo `load_pages(extra_doc_dirs=None, include_concepts=False)` — **opt-in parametrus**.
  `hera_lint.analyze()` juos naudoja; `hera_wikilink.py` kviečia `load_pages()` BE argumentų, todėl jo elgesys
  nepakito. **Tą pačią schemą sek** — `archive` turi būti tik išsprendžiamas TAIKINYS, NE šaltinis
  (nescanuoti jo outgoing nuorodų, kad nekiltų savireferencinė kilpa, kaip būtų su `analysis/`).
- Kanoninis kelias: `/opt/hera-processor/`. Patikrink faktu, kurį `hera_lint.py` realiai vykdo Loop B, ir taisyk TĄ
  (Fazė 30 pamoka: pataisyta kopija, kurios niekas nevykdo, yra beverčiai).
- Vault ant VPS: `/opt/hera-vault`.

## Apribojimai
€0, be tinklo, be LLM. Fail-safe. **`hera_wikilink` elgesys privalo likti NEPAKITĘS** (jis RAŠO į vault per Loop B hook) —
įrodyk identišku `--dry-run` prieš/po, kaip Fazėje 31. Vault turinio NEMODIFIKUOK. BACKUP prieš keitimą.
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. Cron NELIESK.

## Įrodymai
1. Kurį `hera_lint.py` Loop B realiai vykdo (faktu).
2. **Skaičiai prieš/po:** dangling ir orphan. Tikslas — tie 26 paminėjimai vėl išsisprendžia; likę dangling turi būti
   tie patys „tikri" (vietaženkliai + produktų pavadinimai), kurie buvo prieš archyvavimą (~10).
3. **`hera_wikilink` nepakitęs:** identiškas `--dry-run` rezultatas prieš/po.
4. `bench` nepablogėjo; BACKUP + push į `hera-core-backup`; ROADMAP.md eilutė (**patikrink grep'u faile**).

Jei STOP — kodėl.

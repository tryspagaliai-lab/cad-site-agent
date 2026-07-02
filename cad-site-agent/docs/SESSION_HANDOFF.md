# Session Handoff — Rules Modularization

> Šitą failą automatiškai nuskaito SessionStart hook'as ir įkelia į naujos sesijos
> kontekstą (laptopas / web / bet kuris modelis — Kimi, MiMo). Atnaujink jį
> kiekvienos darbo sesijos pabaigoje.

**Atnaujinta:** 2026-06-16
**Rollback SHA (saugus taškas prieš taisykles):** `2fdb3f8`

## Repo struktūros pastaba (svarbu)
- GitHub repo `tryspagaliai-lab/cad-site-agent` turi VISĄ turinį po vienu
  poaplankiu `cad-site-agent/`. Git šaknis yra lygiu aukščiau.
- Claude Code auto-kraunamas `.claude/settings.json` tik iš **repo šaknies**.
  Todėl SessionStart hook'as registruotas šaknyje, o ne `cad-site-agent/.claude/`.

## Kas padaryta (2026-06-16)
Užduotis `rules-modularization-v1` — modulinė rules sistema (MVP slice, tik cad-site-agent).
Merge'inta į `main` (merge commit `7ee7c78`):
- `cad-site-agent/.cursor/rules/cad-cleanup.mdc` — glob-scoped Cursor taisyklė
  (globs: `src/cad_site_agent/**/*.py`, `config/layers.json`).
- `cad-site-agent/src/cad_site_agent/CLAUDE.md` — nested Claude Code scope taisyklės.
- `.claude/hooks/guard_layer_delete.py` (**repo šaknyje**) — PreToolUse layer-delete gardas (STUB).
- `.claude/settings.json` (**repo šaknyje**) — SessionStart + PreToolUse registracijos (auto-kraunasi).
- `.claude/hooks/session-start.sh` (**repo šaknyje**) — repo sync + handoff konteksto įkėlimas.

## Atviri TODO (rytojui)
1. **(DONE 2026-06-17)** `config/layers.json` sukurtas — generuotas iš
   `export_layers.yaml` (12 output sluoksnių) + `semantic_taxonomy.yaml` (43 klasės)
   = **55 stabilūs sluoksniai**. RADINYS: spec'o „47" NEATITINKA realios schemos;
   failas atspindi tikrą schemą (regeneruoti po schemos pakeitimų).
2. **(DONE 2026-06-17)** `guard_layer_delete.py` logika užbaigta — aptinka
   delete/merge/purge, ištraukia taikinio sluoksnį, BLOKUOJA (exit 2) stabilaus
   sluoksnio naikinimą, fail-open jei schema/sluoksnis neaiškus. Ištestuota 5 scenarijais.
3. **Layer „esmės" testavimas** — pagrindinis tikslas: kad sistema suvoktų sluoksnių
   prasmę. Tam skirti `tests/` (test_analyzer, test_classifier, test_taxonomy,
   test_hatch ir kt.). Baseline: **202 passed, 8 skipped** (skip = trūkstami DXF fixture'ai).
4. **(DONE 2026-06-16)** Layer-guard perkeltas į repo šaknies `.claude/` ir
   registruotas šaknies `settings.json` → dabar auto-kraunasi desktop'e.
5. **`agentos-sessions` branduolys (`AGENTS.md`) + `~/.claude/CLAUDE.md`** — ne šios
   sesijos apimtyje (GitHub scope tik cad-site-agent). Padaryti iš laptopo vietoje.

## Aplinkos FAKTAS (2026-07-02, iš vartotojo — įsiminti!)
- Atskirų „desktop" kompiuterių NĖRA. Vienintelė fizinė mašina — **LAPTOPAS su LINUX**
  (NE Windows! Ankstesnė Windows prielaida buvo klaidinga — ji kilo iš seno
  užduoties failo su `C:\Users\zilva\...` keliu; tie Windows/E:/ keliai pasenę).
  H7149 Osprey Heights raw data yra laptope — tikslus kelias nežinomas, ieškoti
  per `find ~ -iname "*osprey*"`. Ateityje galimas **VPS**.
- Koordinacijos rolė `desktop` pervadinta į `local` (žr. docs/COORDINATION.md).
- Laptopo paleidimas: `bash cad-site-agent/scripts/bootstrap_local.sh` (Linux).

## Testavimo planas
```bash
cd cad-site-agent
python -m pytest tests/ -v        # pilnas rinkinys
python -m pytest tests/test_classifier.py tests/test_taxonomy.py -v  # sluoksnių/klasifikacijos logika
```

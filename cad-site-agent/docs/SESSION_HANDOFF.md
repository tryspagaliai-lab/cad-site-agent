# Session Handoff — Rules Modularization

> Šitą failą automatiškai nuskaito SessionStart hook'as ir įkelia į naujos sesijos
> kontekstą (desktop / web / bet kuris modelis — Kimi, MiMo). Atnaujink jį
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
1. **`config/layers.json` NEEGZISTUOJA.** Hook'as ir Cursor glob'as į jį rodo.
   Reikia sukurti `{"stable_layers": [... 47 sluoksnių ...]}` arba nukreipti į esamus
   YAML (`config/layer_aliases.yaml`, `config/export_layers.yaml`).
2. **`guard_layer_delete.py` yra STUB** — target sluoksnio parse + palyginimas su
   schema dar neįgyvendintas (`# TODO`). Be #1 jis mestų klaidą, jei suveiktų
   (kol nėra `cad-site-agent/config/layers.json`). Schemos kelias jau nukreiptas teisingai.
3. **Layer „esmės" testavimas** — pagrindinis tikslas: kad sistema suvoktų sluoksnių
   prasmę. Tam skirti `tests/` (test_analyzer, test_classifier, test_taxonomy,
   test_hatch ir kt.). Paleisti pilną rinkinį ir peržiūrėti rezultatus.
4. **(DONE 2026-06-16)** Layer-guard perkeltas į repo šaknies `.claude/` ir
   registruotas šaknies `settings.json` → dabar auto-kraunasi desktop'e.
5. **`agentos-sessions` branduolys (`AGENTS.md`) + `~/.claude/CLAUDE.md`** — ne šios
   sesijos apimtyje (GitHub scope tik cad-site-agent). Padaryti iš desktop'o vietoje.

## Testavimo planas
```bash
cd cad-site-agent
python -m pytest tests/ -v        # pilnas rinkinys
python -m pytest tests/test_classifier.py tests/test_taxonomy.py -v  # sluoksnių/klasifikacijos logika
```

# Agent Coordination Board

Bendra „lenta", per kurią VISI agentai (Claude Code laptope, web/cloud sesijos,
Kimi, MiMo, ateityje VPS) žino, ką daro kiti. Komunikacija **asinchroninė per
Git** — ne live pokalbis, bet bendra atmintis: kiekvienas startuodamas perskaito
kitų statusus, o baigęs darbo vienetą — atnaujina savo.

> **FAKTAS (2026-07-02, iš vartotojo):** atskirų „desktop" kompiuterių NĖRA.
> Vienintelė fizinė mašina — LAPTOPAS (Windows, jame ir `C:\Users\zilva\...`
> raw data). Ateityje galimas VPS. Rolė `local` = Claude Code paleistas tame
> laptope; rolė `web` = cloud sesija (šis repo, be prieigos prie C:\).

## Kaip tai veikia
- Kiekvienas agentas turi SAVO statuso failą: `docs/agent-status/<role>.md`
  (pvz. `local`, `web`, `kimi`, `mimo`, vėliau `vps`). Kiekvienas rašo TIK į
  savo → jokių merge konfliktų.
- **SessionStart hook** (`.claude/hooks/session-start.sh`) startuodamas:
  `git pull` → perskaito VISŲ agentų statusus → įkelia į sesijos kontekstą.
  Tad atsidaręs bet kurią sesiją iškart matai, ką kiti padarė/daro.
- Baigęs darbo vienetą, agentas paleidžia helper'į (žr. žemiau) → atnaujina savo
  statusą + commit + push. Kiti tai pamatys kito `git pull` / SessionStart metu.

## Protokolas (privaloma visiems agentams)
1. **Startas:** perskaityk `docs/agent-status/*.md` (SessionStart tai padaro auto).
   Nedubliuok darbo, kurį kitas jau pažymėjo „IN PROGRESS".
2. **Pradedant darbą:** pažymėk savo statusą `status: IN_PROGRESS` + ką darai.
3. **Baigus / perduodant:** atnaujink į `status: DONE` arba `status: HANDOFF`
   ir parašyk kas toliau / kam.
4. **Niekada** nelįsk į kito agento failą.

## Vaidmenys (rolės)
| role | aplinka | atsakomybė |
|------|---------|-----------|
| `local` | Claude Code LAPTOPE (vienintelė fizinė mašina, Windows) | Prieiga prie `C:\` raw data, ODA DWG→DXF konversija, failų parsing |
| `web` | cloud sesija (be prieigos prie C:\) | Repo/kodo darbas: taisyklės, pipeline taisymai, testai, commit'ai |
| `kimi` / `mimo` | tandemo modeliai | Kryžminė rezultatų patikra |
| `vps` | (ateityje, jei bus) | Nuolatinis serveris pipeline'ui / automatizacijai |

## Tandemo (Kimi/MiMo) darbo eiga
1. **Paketas:** `python scripts/tandem_report.py --batch data/h7149/batch_report.json`
   → sugeneruoja vieną savarankišką md failą (`reports/tandem/`) su visa būsena
   ir aiškia užduotimi tikrintojui.
2. **Patikra:** paketo turinys įklijuojamas į Kimi ir (atskirai) į MiMo.
   Kiekvienas grąžina standartinį `VERDICT: PASS|FAIL|CONCERNS` bloką.
3. **Įrašymas:** verdiktai grįžta į lentą:
   `./.claude/hooks/agent-status.sh kimi "VERDICT: ..."` (ir `mimo`).
4. **Uždarymas:** Claude sesija kitą kartą startuodama verdiktus mato
   automatiškai ir taiso, kas rasta. Jei Kimi ir MiMo verdiktai prieštarauja —
   sprendžia vartotojas.

## Helper'is
```bash
# atnaujinti savo statusą (commit + push automatiškai):
./.claude/hooks/agent-status.sh <role> "<ką darai / statusas>"

# pavyzdys:
./.claude/hooks/agent-status.sh local "IN_PROGRESS: ODA konvertuoju H7149 DWG->DXF (12 failų)"
./.claude/hooks/agent-status.sh web "DONE: pataisiau taksonomijos parking_bay aliasą, testai žali"
```

# Agent Coordination Board

Bendra „lenta", per kurią VISI agentai (Claude Code desktop, ši web sesija, Kimi,
MiMo) žino, ką daro kiti. Komunikacija **asinchroninė per Git** — ne live pokalbis,
bet bendra atmintis: kiekvienas startuodamas perskaito kitų statusus, o baigęs
darbo vienetą — atnaujina savo.

## Kaip tai veikia
- Kiekvienas agentas turi SAVO statuso failą: `docs/agent-status/<role>.md`
  (pvz. `desktop`, `web`, `kimi`, `mimo`). Kiekvienas rašo TIK į savo → jokių
  merge konfliktų.
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
| `desktop` | Claude Code desktop (lokalus Windows) | Prieiga prie `C:\` raw data, ODA DWG→DXF konversija, failų parsing |
| `web` | ši cloud sesija | Repo/kodo darbas: taisyklės, pipeline taisymai, testai, commit'ai |
| `kimi` / `mimo` | tandemo modeliai | Kryžminė rezultatų patikra |

## Helper'is
```bash
# atnaujinti savo statusą (commit + push automatiškai):
./.claude/hooks/agent-status.sh <role> "<ką darai / statusas>"

# pavyzdys:
./.claude/hooks/agent-status.sh desktop "IN_PROGRESS: ODA konvertuoju H7149 DWG->DXF (12 failų)"
./.claude/hooks/agent-status.sh web "DONE: pataisiau taksonomijos parking_bay aliasą, testai žali"
```

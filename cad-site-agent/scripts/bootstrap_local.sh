#!/bin/bash
# ============================================================
# bootstrap_local.sh — LAPTOPO (LINUX) paruošimas vienu paleidimu
# Paleisk terminale:  bash cad-site-agent/scripts/bootstrap_local.sh
#
# Ką daro:
#   1. Patikrina git / python3 / Claude Code CLI (įdiegia CLI jei nėra)
#   2. Klonuoja arba atnaujina cad-site-agent repo
#   3. Įdiegia Python priklausomybes (pip install -e .[dev])
#   4. Patikrina ar ODA File Converter įdiegtas
#   5. Paleidžia Claude Code LOKALIĄ sesiją su 'local' rolės užduotimi
# ============================================================
set -uo pipefail

REPO_URL="https://github.com/tryspagaliai-lab/cad-site-agent"
WORK_DIR="$HOME/cad-site-agent"

echo "=== [1/5] Įrankių patikra ==="
command -v git >/dev/null || { echo "TRŪKSTA git: sudo apt install git"; exit 1; }
command -v python3 >/dev/null || { echo "TRŪKSTA python3: sudo apt install python3 python3-pip"; exit 1; }
if ! command -v claude >/dev/null; then
    echo "Claude Code CLI nerastas — diegiu..."
    curl -fsSL https://claude.ai/install.sh | bash
    export PATH="$HOME/.local/bin:$PATH"
    command -v claude >/dev/null || { echo "Nepavyko įdiegti Claude Code. Žr. https://code.claude.com/docs"; exit 1; }
fi
echo "git/python3/claude OK"

echo "=== [2/5] Repo ==="
if [ -d "$WORK_DIR/.git" ]; then
    cd "$WORK_DIR" && git pull --ff-only origin main
else
    git clone "$REPO_URL" "$WORK_DIR" && cd "$WORK_DIR"
fi

echo "=== [3/5] Python priklausomybės ==="
python3 -m pip install -e "$WORK_DIR/cad-site-agent[dev]" --quiet 2>/dev/null \
    || python3 -m pip install --user -e "$WORK_DIR/cad-site-agent[dev]" --quiet \
    || python3 -m pip install --break-system-packages -e "$WORK_DIR/cad-site-agent[dev]" --quiet

echo "=== [4/5] ODA File Converter patikra ==="
if python3 -c "from ezdxf.addons import odafc; exit(0 if odafc.is_installed() else 1)" 2>/dev/null; then
    echo "ODA įdiegtas ✓"
else
    echo "ODA NERASTAS — Claude sesija padės įdiegti (Linux .deb):"
    echo "  https://www.opendesign.com/guestfiles/oda_file_converter"
fi

echo "=== [5/5] Paleidžiu Claude Code LOKALIĄ sesiją ==="
cd "$WORK_DIR"
exec claude "Vykdyk 'local' rolės TODO iš cad-site-agent/docs/agent-status/local.md. Aplinka: LINUX laptopas. (1) Jei ODA File Converter neįdiegtas — padėk įsidiegti .deb iš opendesign.com (žr. docs/ODA_SETUP.md). (2) SURASK 'H7149 Osprey Heights' katalogą diske (ieškok: ~/Desktop, ~/Documents, ~/Downloads, ~/ — 'find ~ -iname \"*osprey*\" -maxdepth 4'). (3) Konvertuok DWG->DXF ir paleisk cad-site-agent/scripts/run_pipeline_batch.py ant to katalogo. (4) Sugeneruok tandemo paketą scripts/tandem_report.py. (5) Rezultatus surašyk į docs/agent-status/local.md ir push'ink per ./.claude/hooks/agent-status.sh local '...'."

#!/usr/bin/env bash
#
# setup-vps.sh — paruošia šviežią Ubuntu (22.04 / 24.04) Hetzner VPS
# CAD Site Agent paleidimui per SSH / komandinę eilutę.
#
# Naudojimas (VPS'e, projekto šaknyje, kur yra pyproject.toml):
#     bash deploy/setup-vps.sh
#
# Skriptas yra IDEMPOTENTINIS — saugu paleisti kelis kartus.
# Įdiegia: Python venv + sistemines bibliotekas + patį `cad-agent` įrankį.
#
set -euo pipefail

# --- Surask projekto šaknį (kur yra pyproject.toml) ----------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

if [[ ! -f "pyproject.toml" ]]; then
  echo "KLAIDA: pyproject.toml nerastas (${PROJECT_ROOT}). Paleisk skriptą iš projekto šaknies." >&2
  exit 1
fi

echo "==> Projekto šaknis: ${PROJECT_ROOT}"

# --- 1. Sistemos paketai -------------------------------------------------
# shapely/scipy/numpy/matplotlib turi paruoštus (manylinux) wheel'us, tad
# kompiliuoti nereikia. build-essential + libgeos-dev paliekami kaip atsarga,
# jei kada prireiktų statyti iš šaltinio. libspatialindex — tik optional rtree.
echo "==> Diegiamos sistemos bibliotekos (reikės sudo/root)..."
export DEBIAN_FRONTEND=noninteractive
SUDO=""
if [[ "${EUID}" -ne 0 ]]; then SUDO="sudo"; fi

${SUDO} apt-get update -y
${SUDO} apt-get install -y --no-install-recommends \
  python3 \
  python3-venv \
  python3-pip \
  build-essential \
  python3-dev \
  libgeos-dev \
  libspatialindex-dev \
  git \
  ca-certificates

# --- 2. Python virtuali aplinka -----------------------------------------
VENV_DIR="${PROJECT_ROOT}/.venv"
if [[ ! -d "${VENV_DIR}" ]]; then
  echo "==> Kuriama virtuali aplinka: ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
else
  echo "==> Virtuali aplinka jau yra: ${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel

# --- 3. Paties įrankio įdiegimas ----------------------------------------
echo "==> Diegiamas cad-site-agent (editable)..."
pip install -e .

# --- 4. Greitas patikrinimas --------------------------------------------
echo "==> Patikrinimas..."
cad-agent --help >/dev/null 2>&1 && echo "    cad-agent OK" || {
  echo "    ĮSPĖJIMAS: 'cad-agent --help' nepavyko. Patikrink rankiniu būdu." >&2
}

cat <<EOF

========================================================================
 ✅ Įdiegta sėkmingai.

 Kaip naudoti (kiekvienoje naujoje SSH sesijoje aktyvuok aplinką):

     source ${VENV_DIR}/bin/activate
     cad-agent process input.dxf output/result.dxf

 Failų perkėlimas į VPS iš savo kompiuterio (scp):

     scp brezinys.dxf  user@VPS_IP:~/cad-site-agent/input/
     # ...apdoroji VPS'e...
     scp user@VPS_IP:~/cad-site-agent/output/result.dxf  ./

 Pilnas vadovas: docs/DEPLOY_VPS.md
========================================================================
EOF

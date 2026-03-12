#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$SCRIPT_DIR/../../src"

SRC="${1:-/mnt/e/roman_gardens_gapclosed.dxf}"
OUT="$SCRIPT_DIR/roman_gardens.dxf"

if [[ -f "$OUT" ]]; then
  echo "Output already exists: $OUT"
  echo "Delete it first to re-run."
  exit 1
fi

python -m cad_site_agent.cli process "$SRC" "$OUT"

# ============================================================
# bootstrap_local.ps1 — LAPTOPO paruošimas vienu paleidimu
# Paleisk PowerShell'e:  .\scripts\bootstrap_local.ps1
# (arba per paste-bloką iš pokalbio, jei repo dar neklonuotas)
#
# Ką daro:
#   1. Patikrina git / python / Claude Code CLI (įdiegia CLI jei nėra)
#   2. Klonuoja arba atnaujina cad-site-agent repo
#   3. Įdiegia Python priklausomybes (pip install -e .[dev])
#   4. Patikrina ar ODA File Converter įdiegtas
#   5. Paleidžia Claude Code LOKALIĄ sesiją su 'local' rolės užduotimi
# ============================================================
$ErrorActionPreference = "Continue"
$RepoUrl  = "https://github.com/tryspagaliai-lab/cad-site-agent"
$WorkDir  = Join-Path $HOME "cad-site-agent"

Write-Host "=== [1/5] Irankiu patikra ===" -ForegroundColor Cyan
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "TRUKSTA git. Idiek: winget install Git.Git  (arba https://git-scm.com)" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "TRUKSTA python. Idiek: winget install Python.Python.3.12" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Host "Claude Code CLI nerastas - diegiu..." -ForegroundColor Yellow
    irm https://claude.ai/install.ps1 | iex
    if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
        Write-Host "Nepavyko idiegti Claude Code. Zr. https://code.claude.com/docs" -ForegroundColor Red
        exit 1
    }
}
Write-Host "git/python/claude OK" -ForegroundColor Green

Write-Host "=== [2/5] Repo ===" -ForegroundColor Cyan
if (Test-Path (Join-Path $WorkDir ".git")) {
    Set-Location $WorkDir
    git pull --ff-only origin main
} else {
    git clone $RepoUrl $WorkDir
    Set-Location $WorkDir
}

Write-Host "=== [3/5] Python priklausomybes ===" -ForegroundColor Cyan
Set-Location (Join-Path $WorkDir "cad-site-agent")
python -m pip install -e ".[dev]" --quiet

Write-Host "=== [4/5] ODA File Converter patikra ===" -ForegroundColor Cyan
$oda = python -c "from ezdxf.addons import odafc; print(odafc.is_installed())" 2>$null
if ($oda -match "True") {
    Write-Host "ODA idiegtas" -ForegroundColor Green
} else {
    Write-Host "ODA NERASTAS - Claude sesija pades idiegti (arba zr. docs/ODA_SETUP.md):" -ForegroundColor Yellow
    Write-Host "  https://www.opendesign.com/guestfiles/oda_file_converter"
}

Write-Host "=== [5/5] Paleidziu Claude Code LOKALIA sesija ===" -ForegroundColor Cyan
Set-Location $WorkDir
claude "Vykdyk 'local' roles TODO is cad-site-agent/docs/agent-status/local.md: (1) jei ODA File Converter neidiegtas - padek ji idiegti (docs/ODA_SETUP.md); (2) parsink 'C:\Users\zilva\Desktop\H7149 Osprey Heights' inventoriu (DWG/DXF/PDF); (3) konvertuok DWG->DXF; (4) paleisk cad-site-agent/scripts/run_pipeline_batch.py ant konvertuotu failu; (5) sugeneruok tandemo paketa scripts/tandem_report.py; (6) atnaujink docs/agent-status/local.md su rezultatais ir push'ink i main (arba naudok .claude/hooks/agent-status.ps1 local '...')."

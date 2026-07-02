# agent-status.ps1 — Windows atitikmuo agent-status.sh helper'iui.
# Naudojimas:  .\.claude\hooks\agent-status.ps1 local "IN_PROGRESS: konvertuoju H7149"
param(
    [Parameter(Mandatory=$true)][string]$Role,
    [Parameter(Mandatory=$true)][string]$Message
)
$ErrorActionPreference = "Stop"

$Proj = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Proj

$Dir  = "cad-site-agent/docs/agent-status"
$File = "$Dir/$Role.md"
New-Item -ItemType Directory -Force -Path $Dir | Out-Null

$Ts   = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$Head = (git rev-parse --short HEAD 2>$null); if (-not $Head) { $Head = "?" }
$Br   = (git rev-parse --abbrev-ref HEAD 2>$null); if (-not $Br) { $Br = "main" }

@"
# Agent status: $Role

- updated: $Ts
- branch: $Br
- head: $Head
- status: $Message
"@ | Set-Content -Path $File -Encoding UTF8

git add $File
$staged = git diff --cached --name-only
if (-not $staged) { Write-Host "[agent-status] no change for $Role"; exit 0 }
git commit -q -m "agent-status($Role): $Message"

for ($i = 1; $i -le 3; $i++) {
    git push origin $Br 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[agent-status] $Role pushed -> $Br ($Ts)"
        exit 0
    }
    Write-Host "[agent-status] push rejected, rebasing (attempt $i)"
    git pull --rebase origin $Br 2>$null
}
Write-Host "[agent-status] PUSH FAILED - statusas commit'intas lokaliai"
exit 1

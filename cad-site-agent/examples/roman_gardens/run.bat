@echo off
REM Roman Gardens example — Windows batch
set PYTHONPATH=%~dp0..\..\src
set SRC=E:\roman_gardens_gapclosed.dxf
set OUT=%~dp0roman_gardens.dxf

if exist "%OUT%" (
    echo Output already exists: %OUT%
    echo Delete it first to re-run.
    exit /b 1
)

py -3.10 -m cad_site_agent.cli process "%SRC%" "%OUT%"

@echo off
REM Run DXF analysis with Python 3.10 (has all deps including click)
REM Usage: scripts\run_analysis.bat <dxf_file> [--preview]

set PYTHON="C:\Program Files\Python310\python.exe"
set SCRIPT_DIR=%~dp0..
cd /d %SCRIPT_DIR%

%PYTHON% -m src.cad_site_agent.cli %*

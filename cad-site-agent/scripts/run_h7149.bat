@echo off
REM ============================================================
REM run_h7149.bat — H7149 Osprey Heights pilna automatika (LAPTOPE)
REM Paleisk is cad-site-agent katalogo (arba dvigubu paspaudimu).
REM 1) DWG->DXF (jei idiegtas ODA)  2) cleanup  3) gap close
REM 4) normalize  5) hatch+routing  6) batch_report.json
REM Po to tandemo paketa generuoja: python scripts\tandem_report.py
REM ============================================================
cd /d "%~dp0.."
python scripts\run_pipeline_batch.py "C:\Users\zilva\Desktop\H7149 Osprey Heights" --out data\h7149 --recursive
python scripts\tandem_report.py --batch data\h7149\batch_report.json
echo.
echo Baigta. Ataskaitos: data\h7149\batch_report.json ir reports\tandem\
pause

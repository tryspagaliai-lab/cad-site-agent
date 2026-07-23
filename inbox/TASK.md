UŽDUOTIS — FreeCAD PoC 1 žingsnis: FEASIBILITY probe (galimybių patikra) + minimalus PoC JEI įrankiai jau yra. <10 min.
NEleisk pytest. Fail-safe. €0. Deterministiška (BE LLM). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme. Secret'us NEliesk.
SVARBU: šis žingsnis NIEKO SUNKAUS NEDIEGIA (jokio apt/pip heavy install). FreeCAD apt ~1.5GB, cadquery/OCP ~300MB+ — tai human-gate, NE dabar.
Tik PATIKRINK kas jau yra + įvertink install kainą + JEI įrankis jau yra → paleisk mažą PoC. Sprendimą dėl diegimo priims vartotojas po tavo ataskaitos.

KONTEKSTAS: iš kuruoto ingest'o (FreeCAD MCP, neka-nat/freecad-mcp) — tikslas įrodyti „kodas→parametrinė 3D detalė→export, headless, €0 ant VPS".
Prieš įsipareigojant sunkiam diegimui ant 4GB VPS, pirma sužinom ką jau turim ir kiek diskas leidžia.

1) FEASIBILITY (deterministiška, saugu, greita):
   a) `which freecadcmd freecad FreeCADCmd 2>/dev/null` — ar yra FreeCAD headless binaris?
   b) `/opt/hera-venv/bin/python3 -c "import cadquery; print(cadquery.__version__)" 2>&1 | head -1` IR sistemos `python3 -c "import FreeCAD" 2>&1 | head -1` — ar parametrinis CAD Python jau importuojasi?
   c) Disko headroom: `df -h / /root /opt` (Avail stulpelis) + `free -m` (RAM).
   d) Install kainos ĮVERTIS (BE diegimo): `apt-cache show freecad 2>/dev/null | grep -E "Installed-Size|Size" | head -2` ; ir cadquery dydžio nuoroda pastaboje (~300MB+ OCP). NIEKO neinstaliuok — tik `apt-cache show` (read-only).

2) MINIMALUS PoC — TIK JEI 1a ARBA 1b jau rado veikiantį įrankį (freecadcmd ARBA cadquery importuojasi). Kitaip PRALEISK šį žingsnį (nediek nieko):
   - Sukurk /root/hera_cadpoc/ ; parašyk mažą skriptą kuris sugeneruoja parametrinę detalę: dėžė 50×30×20mm + 1 skylė Ø8mm centre.
   - Jei cadquery: `import cadquery as cq; r = cq.Workplane("XY").box(50,30,20).faces(">Z").workplane().hole(8); cq.exporters.export(r, "/root/hera_cadpoc/poc.step"); cq.exporters.export(r, "/root/hera_cadpoc/poc.stl")`.
   - Jei tik freecadcmd: analogiškas FreeCAD Python API skriptas (Part.makeBox + skylė per Part.makeCylinder cut) → export Part.export į .step; paleisk per `freecadcmd skriptas.py`.
   - Patikrink kad failai sukurti + dydžiai > 0. Fail-safe: bet kokia klaida → NIEKAD necrashink, log /root/hera_cadpoc/poc.log, ataskaitoj pažymėk klaidą.

3) JOKIO push nereikia (probe, nauji failai tik /root/hera_cadpoc, netrackinami). Vault NELIESK šiam žingsniui.

ATASKAITA (HERA botas, trumpai ir konkrečiai):
   - Kas JAU įdiegta: freecadcmd? cadquery? FreeCAD python? (versijos jei yra).
   - Diskas: Avail ant / ir /root; RAM free.
   - Install kaina: FreeCAD apt Installed-Size (jei gavai); cadquery ~300MB+ pastaba.
   - PoC: ar paleido? jei taip — failų keliai + dydžiai (poc.step, poc.stl) = ĮRODYMAS kad parametrinis CAD veikia headless €0. Jei praleido — kodėl (nei vieno įrankio).
   - REKOMENDACIJA vartotojui (1 eilutė): kuris kelias pigiausias €0 headless PoC užbaigti (pvz. „cadquery pip ~300MB, diskas leidžia" ARBA „freecad apt 1.5GB, diskas per mažas → cadquery geriau" ARBA „jau turim X, PoC padarytas").
   Jei STOP — kodėl.

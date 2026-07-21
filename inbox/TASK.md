UŽDUOTIS — vault nata: „3ds Max MCP serveriai" (vartotojo pateikta, cad-3d kryptis). <8 min.
NEleisk pytest. Fail-safe. €0. Deterministiška (turinys duotas, be LLM/tinklo). Ataskaita TIK į HERA botą.
Privatus hera-vault. Viešo cad-site-agent NELIESK.

KONTEKSTAS: vartotojas pateikė 3 GitHub repo — MCP serveriai 3ds Max valdymui per AI. TIESIOGIAI jo ArchViz/3ds Max
fonas + AI orkestracija = tiltas tarp jo 3D darbo ir AI sistemos. Strategiškai svarbu (cad-3d kryptis).

1) Sukurk growth natą `growth/2026-07-20-3dsmax-mcp-serveriai.md` (STATUS: PRIIMTA kaip žinojimas 2026-07-20
   (human-gate: vartotojas pateikė pats); domain: cad-3d; kind: tools):

   ## 3ds Max MCP serveriai (AI → 3ds Max valdymas)
   1. **cl0nazepamm/3dsmax-mcp** — pilnai išvystytas: 100+ įrankių, FastMCP(Python) → C++ įskiepis/MAXScript
      Listener TCP :8765; objektai/modifikatoriai/animacija; viewport capture → AI analizei; tyFlow/RailClone/OSL;
      Safe mode (blokuoja pavojingas komandas). STIPRIAUSIAS kandidatas.
   2. **loonghao/dcc-mcp-3dsmax** — DCC MCP ekosistemos dalis; Sidecar procesas + SQLite užduočių bazė ilgiems
      procesams; DCC MCP meniu Max'e; main-thread saugumas; pritaikytas kitoms DCC programoms.
   3. **317431629/3dsMaxMCP** — lengvas Python/MAXScript tiltas (:50007); baziniai objektai/medžiagos/animacijos raktai.

   ## Strateginė reikšmė (kuravimo pastaba)
   - Tiltas: vartotojo 3ds Max/ArchViz darbas ↔ AI orkestracija. Atveria „AI diriguoja 3D scenai" darbo eigą
     (viewport capture → AI analizė → korekcijos komandos) — tiesiogiai jungiasi su cad-3d kryptimi (GIFT 2D→3D)
     ir „AI-accelerated visualization" paslaugų idėja.
   - ⚠️ REIKALAVIMAS: 3ds Max = Windows desktop programa — reikia mašinos su Max (NE VPS; vartotojo laptopas Linux).
     Todėl tai DESKTOP-FUTURE kryptis (kaip Fazė 8 įrankiai) — fiksuojam žinią dabar, diegiam kai bus Max aplinka.
   - Saugumo pastaba: Safe mode (1-as repo) svarbus — AI valdo softą, reikia guardrail'ų (mūsų human-gate filosofija).

2) Wiki-link pass (sąsajos: FUTURE_GPU/GIFT cad-3d, ArchViz temos jei grafe). Trajektorija: curation/accept-knowledge.
3) BACKUP: vault push. Nepavyko → NEkartok, pranešk.

ATASKAITA (HERA botas, trumpai): (a) nata sukurta; (b) wiki; (c) push OK/ne.

UŽDUOTIS — Paleisk €0 TARYBĄ (council) su klausimu apie DXF→PNG→AI-renderis kryptį; grąžink kiekvieno juroro balsą. <12 min.
NEleisk pytest. €0 (TIK nemokami jurorai: gemini + groq multi-model + glm; mokamų NEjunk). Fail-safe. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK. Secret'us NEliesk.

SVARBU: nieko NEDIEGIAM šia užduotimi — tik klausiam tarybos. Jokio kodo, jokio naujo modulio.

KONTEKSTAS: iš kuruoto ingest'o (AutoCAD→AI renderis per Gemini). Vartotojo niša = ArchViz/3D vizualizacija.
Originali darbo eiga reikalauja AutoCAD (Windows desktop) — vartotojas Linux, todėl siūloma ADAPTACIJA.

1) Paleisk esamą €0 tarybą (hera_council_ask.py) su ŠIUO klausimu (paduok verbatim):

„HERA yra €0 agentų sistema ant 4GB RAM CPU VPS (Linux, JOKIO GPU, jokio AutoCAD). Vartotojo verslo niša — architektūrinė
vizualizacija (ArchViz). Egzistuoja populiari rankinė darbo eiga: AutoCAD 2D aukšto planas → išvalyti tekstus/matmenis →
ekrano nuotrauka → įkelti į Gemini (vaizdų generavimą) su detalia užklausa → gauti 3D izometrinį renderį klientui per minutes.
SIŪLOMA ADAPTACIJA: kadangi projektas cad-site-agent JAU parsina DXF failus per ezdxf biblioteką ant Linux headless,
pakeisti 'AutoCAD ekrano nuotrauką' į 'ezdxf headless sugeneruotą švarų 2D plano PNG' (sluoksnių filtras pašalina tekstus/
matmenis), tada tą PNG paduoti Gemini vaizdų generavimui → 3D renderis. Viskas €0, Linux, be AutoCAD.
KLAUSIMAS: (1) ar verta šitą DXF→PNG→AI-renderis grandinę statyti kaip realų cad-site-agent praplėtimą — TAIP/NE;
(2) 2-3 svarbiausi argumentai; (3) 1-2 didžiausios rizikos/pitfall'ai (techniniai IR verslo);
(4) ar toks AI renderis turi realią komercinę vertę ArchViz darbo eigoje, ar tai tik žaisliukas, kurio klientai nepirks."

2) Surink kiekvieno juroro (gemini, groq modeliai, glm) atsakymą. Jei kuris juroras 402/klaida/tuščias → pažymėk „skipped" (NElaikyk klaida). Fail-safe: jei visa taryba krenta → ataskaitoj pasakyk kiek atsakė / kiek skipped, be crash.
   PASTABA: praeitame council paleidime GEMINI jurorai buvo neįskaityti nes JSON nukirstas ties maxOutputTokens=1024. JEI galima TRIVIALIAI (be didelių pakeitimų, be rizikos) padidinti gemini maxOutputTokens iki ~2048 tam paleidimui — padaryk ir pažymėk ataskaitoj. Jei tai reikalautų rimtesnio kodo keitimo — NEDARYK, tiesiog pažymėk kaip žinomą apribojimą.

3) NIEKO nediegiam, nekeičiam (išskyrus jei taryba loguoja į vault trajektoriją kaip įprastai — leisk įprastą log/commit).

ATASKAITA (HERA botas): kiekvieno juroro TAIP/NE + 2-3 argumentai + pitfall'ai (glaustai); atskirai (4) komercinė vertė — ar jurorai sutaria; kiek atsakė/skipped; ar gemini šįkart įsiskaitė. Jei STOP — kodėl.

UŽDUOTIS — Paleisk €0 TARYBĄ (council) su strateginiu klausimu; grąžink kiekvieno juroro balsą. <12 min.
NEleisk pytest. €0 (TIK nemokami jurorai: gemini + groq multi-model + glm; mokamų NEjunk). Fail-safe. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK. Secret'us NEliesk.

KONTEKSTAS: vartotojas svarsto strateginę HERA kryptį ir nori tarybos nuomonės PRIEŠ sprendžiant. Nieko NEDIEGIAM šia užduotimi — tik klausiam tarybos.

1) Paleisk esamą €0 tarybą (hera_council_ask.py, arba hera_council.py wrapper — kaip anksčiau) su ŠIUO klausimu (paduok verbatim):

„HERA yra €0 savęs-tobulinanti agentų sistema ant 4GB RAM CPU VPS (JOKIO GPU). Svarstoma kryptis:
(A) bootstrap su Claude → kaupti skill.md + vykdymo pėdsakus (traces) DVIGUBO NAUDOJIMO formatu (RAG-embeddinami DABAR per esamą semantinę paiešką + treniravimui-paruoštos instruction/response poros VĖLIAU);
(B) vėliau distiliuoti mažą lokalų modelį (0.5–3B, kvantizuotą GGUF) ar LoRA per NEMOKAMĄ Colab/Kaggle GPU, €0-inference ant VPS.
KLAUSIMAS: ar HERA'ai verta DABAR pradėti bent (A) duomenų kaupimą dvigubo naudojimo formatu? Ar geriau likti TIK prie RAG/few-shot ir NIEKADA netreniruoti (nes 4GB/CPU/€0)?
Prašau: (1) TAIP/NE dėl (A) pradėjimo dabar; (2) 2–3 svarbiausi argumentai; (3) 1–2 didžiausi pitfall'ai/rizikos; (4) ar (B) LoRA realistiška €0 kontekste, ar iliuzija."

2) Surink kiekvieno juroro (gemini, groq modeliai, glm) atsakymą. Jei kuris juroras 402/klaida/tuščias → pažymėk „skipped" (NElaikyk klaida). Fail-safe: jei visa taryba krenta → ataskaitoj pasakyk kiek jurorų atsakė / kiek skipped, be crash.

3) NIEKO nediegiam, nekeičiam kodo, necommit'inam (išskyrus jei taryba loguoja į vault trajektoriją kaip įprastai — tada leisk įprastą log/commit, kaip esamas council elgesys). Jokio naujo modulio.

ATASKAITA (HERA botas): kiekvieno juroro TAIP/NE + jo 2-3 argumentai + pitfall'ai (glaustai, po ~2-3 eilutes jurorui); kiek jurorų atsakė / skipped; jei įmanoma — bendra kryptis (konsensusas ar išsiskyrimas). Jei STOP — kodėl.

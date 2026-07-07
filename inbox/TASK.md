UŽDUOTIS — HERA Fazė 6: INTENCIJŲ MARŠRUTIZATORIUS + „paklausk vault'o" (RAG). Autonomiškai.
NELIESK veikiančių Fazės 2–5 ir youtube kelio — tik PRIDĖK priekinį routerį + query kelią. Nemokama (Gemini free).
Atsiskaityk į Telegram TRUMPAI, aiškiu galutiniu statusu.

ESMĖ: sistema turi PATI SUSIVOKTI, kas atsiųsta — klausimas, turinys ar grįžtamasis ryšys — ir pati nukreipti.
JOKIŲ rankinių prefiksų (nebent kaip papildoma užuomina). Router = HERA smegenų priekis.

1) INTENCIJŲ ROUTER (`hera_router.py`). Kiekvienam ateinančiam job'ui nustatyk intenciją per Gemini free
   (greitas klasifikatorius) — klasės:
   - `question` — vartotojas klausia / nori atsakymo iš sukauptos žinios → RAG atsakymas.
   - `ingest` — turinys, kurį reikia įsisavinti (url/youtube/failas/straipsnis/esminis tekstas) → esamas Fazės 2 kelias.
   - `feedback` — vertinimas apie ankstesnį rezultatą → atnaujink to job'o reward (delayed).
   - `other/unclear` — DEFAULT į `ingest` (saugu). Media numatytai `ingest`; TEKSTĄ klasifikuok visada.
   Klasifikaciją loginK į trajektorijas (auditas + ReasoningBank). „?" prefiksas — tik neprivaloma užuomina.

2) QUERY kelias (`hera_query.py`) — kai router nusprendžia `question`:
   - indeksuok vault'ą (extracted/*/full.md + growth/*.md + skills/*/SKILL.md), suskaidyk į chunk'us;
   - retrieve top-K (leksiniai helperiai iš hera_common; Gemini embeddings — neprivaloma);
   - Gemini free atsakymas GRIEŽTAI iš retrieve'intų chunk'ų + ŠALTINIAI (job id/video/failas);
   - jei vault'e nėra — „nerandu vault'e", NEfantazuok. CLI: `hera_query.py "klausimas"`.

3) INTEGRACIJA: processor'iuje kiekvienas job'as pirma per hera_router → į teisingą kelią. Be n8n keitimo.

4) SELF-TEST (€0): mišrūs pavyzdžiai, parodyk teisingą atskyrimą:
   - „kas yra ATDP ir self-evolving agentai?" → question → atsakymas su šaltiniais (dabar vault'e yra ~5+ AI video)
   - koks nors tekstas/URL → ingest
   - „tas wargaming skill buvo naudingas" → feedback → reward atnaujintas
   Parodyk klasifikaciją + rezultatą kiekvienam.

5) DURABILUMAS: kodą į /opt/cad-site-agent/n8n/hera/. Push nedaryk.

Į Telegram: kaip veikia auto-routing (be prefiksų), self-test klasifikacijos + query atsakymai su šaltiniais,
ir aiškiai „FAZĖ 6 BAIGTA".

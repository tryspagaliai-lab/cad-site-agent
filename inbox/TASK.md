UŽDUOTIS — HERA Fazė 6: INTENCIJŲ MARŠRUTIZATORIUS + „paklausk vault'o" (RAG). Autonomiškai.
NELIESK veikiančių Fazės 2–5 — tik PRIDĖK priekinį routerį + query kelią. Nemokama (Gemini free).
Atsiskaityk į Telegram TRUMPAI, aiškiu galutiniu statusu.

ESMĖ (vartotojo): sistema turi PATI SUSIVOKTI, kas atsiųsta — klausimas, turinys ar grįžtamasis ryšys —
ir pati nukreipti. JOKIŲ rankinių prefiksų (nebent kaip papildoma užuomina). Router = HERA smegenų priekis.

1) INTENCIJŲ ROUTER (`hera_router.py`). Kiekvienam ateinančiam job'ui nustatyk intenciją per Gemini free
   (greitas, pigus klasifikatorius) — klasės:
   - `question` — vartotojas klausia / nori atsakymo iš sukauptos žinios → RAG atsakymas.
   - `ingest` — turinys, kurį reikia įsisavinti (url/youtube/failas/straipsnis/esminis tekstas) → esamas Fazės 2 kelias.
   - `feedback` — vertinimas apie ankstesnį rezultatą („gerai/blogai/netikslu") → atnaujink to job'o reward (delayed).
   - `other/unclear` — jei neaišku, DEFAULT į `ingest` (saugu — turinys išsaugomas, neprarandamas).
   Media (youtube/file/image) numatytai `ingest`; TEKSTĄ klasifikuok visada. Klasifikaciją LOGINK į trajektorijas
   (kad būtų auditas + ReasoningBank mokytųsi routing'o). „?" prefiksas — tik neprivaloma aiški užuomina, ne reikalavimas.

2) QUERY kelias (`hera_query.py`) — kai router nusprendžia `question`:
   - indeksuok vault'ą (extracted/*/full.md + growth/*.md + skills/*/SKILL.md), suskaidyk į chunk'us;
   - retrieve top-K (leksiniai helperiai iš hera_common; Gemini embeddings — neprivaloma);
   - Gemini free sugeneruoja atsakymą GRIEŽTAI iš retrieve'intų chunk'ų + ŠALTINIAI (job id/video/failas);
   - jei vault'e nėra — „nerandu vault'e", NEfantazuok. CLI: `hera_query.py "klausimas"`.

3) INTEGRACIJA: processor'iuje kiekvienas job'as pirma eina per hera_router → tada į teisingą kelią. Be n8n keitimo.

4) SELF-TEST (€0): paduok MIŠRIUS pavyzdžius ir parodyk, kad router teisingai atskiria:
   - klausimas: „kas yra ATDP?" → question → atsakymas su šaltiniais
   - turinys: koks nors URL/tekstas → ingest
   - grįžtamasis ryšys: „tas wargaming skill buvo labai naudingas" → feedback → reward atnaujintas
   Parodyk klasifikaciją + rezultatą kiekvienam.

5) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk (nėra creds).

Į Telegram: kaip veikia auto-routing (be prefiksų), self-test klasifikacijos + query atsakymai su šaltiniais,
ir aiškiai „FAZĖ 6 BAIGTA".

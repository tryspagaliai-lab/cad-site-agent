UŽDUOTIS — 🚨 SKUBU: PARSER ingest NEBEVEIKIA. Diagnostika + fix. <14 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe. SAUGUMAS: raktų nespausdink. Kodas -> PRIVATUS hera-core-backup. Viešo NELIESK.

KONTEKSTAS: Vartotojas įmetė 2 nuorodas į PARSER botą (@tryspagliai_bot) — JOKIOS ištrauktos ataskaitos (📥/📖)
negauna. Ingest→PARSER kelias sulūžo. Įtariami KALTININKAI (pastarosios užduotys lietė dispatcher/pipeline):
Memora hook (dispatcher.process), GPU-filter hook (dispatcher), infra-exclusion (dispatcher.py + hera_council.py +
hera_hygiene.py, meta.title/meta.source keitimas), search expansion (ai_digest.py + hera_search/hera_research).
Labiausiai tikėtina — dispatcher.py klaida (crash prieš išsiunčiant į PARSER) ARBA hera_council/hygiene meta klaida.

1) BŪSENA: `systemctl status hera-processor.service` — active ar crash-loop? Rodyk paskutines klaidas.
2) LOGAI: paskutinių ingestų (2 vartotojo nuorodos) apdorojimo logai/klaidos (journalctl -u hera-processor
   --since "30 min ago" arba dispatcher log). Rask TIKSLŲ traceback/eilutę kur lūžta.
3) IDENTIFIKUOK kaltininką: kuris pakeitimas (Memora hook / GPU hook / infra-exclusion meta.title / search) meta
   exception ingest kelyje. Typiniai: hook kviečiamas neteisingoje vietoje, meta.title None, import klaida,
   ai_digest/hera_search pakeitimas paveikė bendrą modulį.
4) FIX: pataisyk PRIEŽASTĮ (pvz. guard None, try/except apie naują hook, sutvarkyk meta.title fallback). Jei greitas
   fix neaiškus — ROLLBACK įtariamą pakeitimą (git revert konkretaus commit'o hera-core-backup / atstatyk .bak) kad
   ingest VĖL VEIKTŲ. Prioritetas: PARSER veikimas ATGAL, ne tobulumas. Visi nauji hook'ai turi būti fail-safe
   (klaida hook'e NEGALI stabdyti ingesto/siuntimo į PARSER).
5) PATVIRTINK: apdorok testinę nuorodą (arba re-trigger 2 vartotojo laukiančias, jei eilėje) -> PARSER
   (@tryspagliai_bot) turi gauti 📥 Priimta + 📖. Parodyk kad atėjo.
6) Ar vartotojo 2 nuorodos eilėje/prarastos? Jei eilėje (n8n queue) -> apdorok. Jei prarastos -> pasakyk kad
   įmestų iš naujo.
7) DURABILUMAS: fix -> hera-core-backup (be raktų). Atmintis: „PARSER ingest fix 2026-07-13 + priežastis".

TELEGRAM (per HERA botą, trumpai): (1) kas sulaužė (kaltininkas + eilutė), (2) fix ar rollback (kas padaryta),
(3) hook'ai dabar fail-safe (klaida nebstabdo ingesto), (4) TESTAS: PARSER gavo 📥+📖, (5) vartotojo 2 nuorodos:
apdorotos/reikia įmesti iš naujo, (6) „PARSER ATSTATYTAS — ingest vėl veikia".

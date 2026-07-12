UŽDUOTIS — HUMAN-GATE: uždaryk 18 atvirų klausimų + pažymėk Managed Agents flagą. <9 min. NEleisk pytest.
Telegram TRUMPAI. Fail-safe. TIK privatus hera-vault. Viešo repo NELIESK. Kodo NELIESK. Necommit'ink raktų.

KONTEKSTAS: VARTOTOJAS (galutinis vartas) peržiūrėjo ir nusprendė dėl visų atvirų klausimų. Pažymėk OPEN_QUESTIONS.md
eilutes pagal raktą (`<!--k:KEY-->`) — pakeisk `- [ ]` į `- [x]` ir pridėk sufiksą „→ <SPRENDIMAS> (human-gate:
vartotojas 2026-07-12)". NIEKO NETRINK (growth įrašai lieka; governance: niekas netrinama auto). Tik pažymėk.

SPRENDIMAI (raktas → sufiksas):
PRIIMTA kaip žinojimas:
- bd101e9efd34 → PRIIMTA kaip žinojimas (Haiku interpretability)
- b2a6821c2cdb → PRIIMTA kaip žinojimas (Eve Bouffard / YC dizainas)
- ee30bbaf5e97 → PRIIMTA kaip žinojimas (Neel Nanda / DeepMind interpretability)
- d75400f27823 → PRIIMTA kaip žinojimas (Antigravity SDLC agentams)
- 7c92d3b22693 → PRIIMTA kaip žinojimas (Claude platformos evoliucija)
- 0e5dce681252 → PRIIMTA kaip žinojimas (DI agentų architektūra)
- dc50089a7349 → PRIIMTA kaip žinojimas (Peter / Crabbox agentų inžinerija)
UŽDARYTA — jau įgyvendinta:
- a72d00871e0f → UŽDARYTA, įgyvendinta (LLM-Wiki → hera_lint/synth/wikilink)
- aaa47f133103 → UŽDARYTA, įgyvendinta (trafilatura → naudojama ekstrakcijoje)
ATMESTA:
- a49ecddfdfe3 → ATMESTA (Upstage doc-processing, vendor niša)
- ef0a4aeb9e5b → ATMESTA (GitHub savaitinė apžvalga, laikinos naujienos)
- cf5d27ec6f75 → ATMESTA (GitHub savaitinė apžvalga, laikinos naujienos)
- eee96a1c84c1 → ATMESTA (UNIT-TEST, test-kandidatas be turinio)
UŽDARYTA — ekstrakcija žlugo:
- 5ba82efe4c86 → UŽDARYTA, ekstrakcija žlugo (9CiOwbmOKdU, nėra turinio)
UŽDARYTA — nav test-užklausos (ne tikri kuravimo klausimai):
- 8962fdc95517 → UŽDARYTA, nav test-užklausa (tandemo SLA nereikalingas, žmogaus-tempu)
- cafa99f2b773 → UŽDARYTA, nav test-užklausa (ATDP-lite)
- fdb37b8787fb → UŽDARYTA, nav test-užklausa (gyvsidabrio virimo temp = 356,7°C)
- 2957f52c9b09 → UŽDARYTA, nav test-užklausa (sienų storis; realaus vieno atsakymo nėra)

Jei kurio rakto OPEN_QUESTIONS.md neranda — praleisk tą (fail-safe), pažymėk ataskaitoje. Nesukurk naujų eilučių.

MANAGED AGENTS flagas: prie growth failo, kuris atitinka „Expanding Managed Agents in Gemini API" (ieškok
growth/2026-07-12-*la7959* arba pagal pavadinimą), pridėk pastabą:
„STATUS: PRIIMTA kaip žinojimas (human-gate 2026-07-12). ⚠️ REFERENCIJA, NE MIGRACIJA — Google debesis, tikėtina
mokama; kertasi su €0/self-hosted vienas-VPS principu. Vertė: validuoja mūsų dizainą (background exec, remote MCP
→ Fazė 8, sandbox, requires_action=human-gate). NEmigruoti." Turinio esmės nekeisk.

PO TO:
1) WIKI: paleisk hera_wikilink.py (arba lint) — parodyk orphan/dangling skaičius (nesitikim blogėjimo).
2) TRAJEKTORIJA/atmintis: įrašyk kuravimo veiksmą (curation/open-questions-triage: 18 uždaryta + 1 flaguota).
3) DURABILUMAS: vault commit („close 18 open questions + Managed Agents reference flag, human-gate 2026-07-12")
   + push privatus hera-vault. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) 18 atvirų klausimų uždaryta (7 priimta, 2 įgyvendinta, 4 atmesta, 1 žlugo,
4 nav-test), (2) Managed Agents pažymėta „referencija, ne migracija (ne €0)", (3) wiki orphan/dangling po valymo,
(4) trajektorija+vault push OK, (5) „ATVIRŲ KLAUSIMŲ TRIAGE BAIGTA — liko 0 laukiančių sprendimo".

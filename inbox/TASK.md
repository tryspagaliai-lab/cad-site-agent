UŽDUOTIS — ROUTER: POKALBINĖS ŽINUTĖS -> TIESIOGINIS ATSAKYMAS, NE INGEST (VIENA SIAURA UŽDUOTIS). <10 min.
NEleisk pytest. LLM kvietimams — griežti timeout'ai (60s + 1 retry). Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: vartotojas nusiuntė „labas HERA" į naują botą (E2E testas — transportas VEIKIA) — bet router'is
pasisveikinimą suklasifikavo kaip INGEST: nuėjo per ištraukimą+selektorių+tarybą (0.0, drop, 9 balsai, ~5 min,
~10 LLM kvietimų). Teisingas rezultatas neteisingu keliu — pasisveikinimas turi gauti pokalbinį atsakymą iškart.

1) ROUTER PAPILDYMAS (hera_router ar atitinkamas): nauja intencija „chat" — trumpos pokalbinės žinutės
   (pasisveikinimas, padėka, smalltalk; be URL, be failo, ne klausimas apie žinias). Atpažinimas pigiai:
   pirmiausia deterministinis greitfiltras (trumpa <80 simb., nėra '?' su turiniu, nėra http, žodynas
   labas/ačiū/sveikas/hi/hello...), abejotinu atveju — esamas LLM klasifikatorius su nauja 'chat' kategorija.
2) CHAT KELIAS: atsakyk per naują botą trumpai ir draugiškai (1 pigus Gemini kvietimas su 60s timeout,
   arba šablonas jei LLM krito: „Labas! Aš HERA — siųsk nuorodą/failą/tekstą arba klausk apie sukauptas žinias.").
   JOKIO ingest'o, ekstraktavimo, tarybos, vault įrašo. Trajektorijoje — kind=chat (pigu, reward nereikia).
3) NEPAKENK: question kelias (RAG/naršymo kilpa) NEKEIČIAMAS — „kas yra ATDP?" tebeeina kaip ėjęs; url/file/
   youtube ingest NEKEIČIAMAS. Riba: jei žinutė panaši į klausimą apie žinias — question, ne chat.
4) TESTAS: (a) „labas HERA" -> chat atsakymas per naują botą, be vault įrašo, be tarybos; (b) „kas yra ATDP?"
   -> question kelias kaip anksčiau; (c) bet kokia http nuoroda -> ingest eilė su ACK kaip anksčiau.
5) DURABILUMAS: kodo kopija į /opt/cad-site-agent/n8n/hera/ (be push į viešą) + push į PRIVATŲ hera-core-backup.

TELEGRAM (trumpai, be raktų): (1) chat intencija veikia — testo atsakymo pavyzdys, (2) question+ingest regresija
OK, (3) backup OK, (4) „CHAT ROUTER BAIGTA".

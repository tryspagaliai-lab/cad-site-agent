UŽDUOTIS — PATIKSLINIMAS: PARSER VEIKIA. NIEKO NEATSUKTI (no rollback). Tik patvirtinti + hook fail-safe. <10 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe. SAUGUMAS: raktų nespausdink. Kodas -> hera-core-backup. Viešo NELIESK.

⚠️ SVARBU — PANEIGIA ankstesnę „PARSER nebeveikia" prielaidą:
- Link 2 (youtube oanQrXEiCy4 „AI Code Generators") APDOROTAS SĖKMINGAI 13:47 — PARSER gavo 📥+📖 (gemini-titrai).
  Vadinasi ingest→PARSER pipeline SVEIKAS; mūsų pakeitimai (Memora/GPU/infra-exclusion/search) NĖRA kalti.
- Link 1 (youtube tFTfqbBMzpE, id 20260713T114830Z-vr9vdh) nepavyko 13:35 — VISI transkripcijų šaltiniai grąžino
  tuščią. Tai TO VIENO video problema (nėra titrų / privatus / regionui apribotas), NE sistemos.

TODĖL: JOKIŲ ROLLBACK. NEatsuk Memora/GPU/infra-exclusion/search pakeitimų — jie veikia. Užduotis dabar:

1) PATVIRTINK link 1 priežastį: patikrink video tFTfqbBMzpE — ar realiai neturi titrų / privatus / regionui apribotas
   (per esamus transcript šaltinius arba yt metadata). Pasakyk TIKSLIĄ priežastį (no captions / private / region /
   transient 503). Jei tik laikinas šaltinių gedimas -> re-trigger link 1 vieną kartą ir žiūrėk ar praeina.
2) HOOK FAIL-SAFE (prevencija, BE reverto): patvirtink kad nauji hook'ai (Memora hook dispatcher.process, GPU-filter
   hook) yra try/except-apsaugoti — hook'o klaida NEGALI stabdyti ingesto/siuntimo į PARSER. Jei kuris NĖRA
   apgaubtas try/except -> pridėk try/except (tik apsauga, ne funkcionalumo keitimas). Tai vienintelis leistinas
   kodo pakeitimas.
3) NEGADINK veikiančio: benchmark 9/9 turi likti; PARSER turi likti veikiantis (link 2 įrodė).
4) DURABILUMAS: jei pridėjai try/except -> hera-core-backup (be raktų). Atmintis: „PARSER OK — link1 video-specific
   transcript fail, ne kodas; hooks fail-safe patvirtinta".

TELEGRAM (per HERA botą, trumpai): (1) PARSER VEIKIA — link 2 praėjo 13:47 (pipeline sveikas), (2) link 1
tFTfqbBMzpE priežastis: <no captions/private/region/transient>, (3) JOKIŲ rollback — pakeitimai veikia,
(4) hook'ai fail-safe patvirtinta (try/except), (5) „PARSER OK — buvo video-specifinė transkripcija, ne sistema".

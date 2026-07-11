UŽDUOTIS — LLM-WIKI #1: NUORODŲ GRAFAS + LINT PRAĖJIMAS (Karpathy stilius). <12 min.
NEleisk viso pytest — tik taikinius. LLM kvietimams griežti timeout'ai (60s+1 retry). Telegram TRUMPAI.
Fail-safe: lint klaida NIEKADA nelaužo HERA. €0 (Gemini free + deterministika).

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta HERA kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: paverčiam vault į tikrą „wiki" (Karpathy pattern). HERA jau turi concept index, eviction,
OPEN_QUESTIONS. NAUJA: aiškus puslapių NUORODŲ grafas + „lint" sveikatos patikra. Skiriasi nuo embeddings:
nuorodos = patvirtintas grafas, ne panašumo spėjimas.

1) NUORODŲ KONVENCIJA: dokumentuok vault'e (pvz. sessions/ ar profile/ README) `[[wiki-nuoroda]]` konvenciją —
   skills/growth kūne susieti giminingus puslapius. NEperrašinėk visų 27 esamų skills rankiniu būdu; tik
   nustatyk konvenciją + (jei paprasta) LLM pasiūlo po 1-3 nuorodas kiekvienam esamam puslapiui (bounded, Gemini,
   fail-safe) — bet tai nebūtina v1, jei brangu/lėta, praleisk ir palik konvenciją būsimiems.

2) LINT MODULIS /opt/hera-processor/hera_lint.py — DETERMINISTINĖ dalis (be LLM, pigu):
   - Sudaryk nuorodų/referencijų grafą iš esamo vault: parse `[[nuorodas]]`, frontmatter `related_growth`,
     `source_job`, `related_*`, ir index/concepts.md įrašus.
   - Aptik: (a) ORPHAN puslapiai (skills/growth be jokių įeinančių nuorodų/referencijų), (b) DANGLING nuorodos
     (rodo į neegzistuojantį puslapį), (c) konceptai concepts.md be savo skill/growth puslapio,
     (d) puslapiai be jokių IŠeinančių nuorodų.
   - LLM dalis (NEBŪTINA, bounded): prieštaravimų patikra TIK tarp puslapių tame pačiame Loop B klasteryje
     (ne visų porų — per brangu); max N porų, 60s timeout, fail-safe. Jei brangu — praleisk v1, pažymėk.

3) IŠVESTIS: /opt/hera-vault/analysis/lint-<YYYY-MM-DD>.md — žmogui skaitomas: orphan sąrašas, dangling,
   trūkstami puslapiai, (prieštaravimai jei tikrinta). Tai curator/žmogaus gate medžiaga (NIEKO auto-netaiso).
   Prijunk prie DAILY/Loop B: raporte pridėk eilutę „lint: orphan N · dangling M · trūksta K".

4) TESTAS: (a) hera_lint.py paleistas ant realaus vault -> lint-<data>.md sugeneruotas su skaičiais; parodyk
   suvestinę (kiek orphan/dangling/trūksta); (b) fail-safe: dirbtinė klaida LLM dalyje -> deterministinė dalis vis
   tiek duoda raportą, HERA nelūžta.

5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup (secret-scan).
   Viešo repo NELIESK. lint md nusisync'ins per vault cron.

TELEGRAM (trumpai, be raktų): (1) nuorodų grafas+lint veikia, (2) pirmo lint suvestinė (orphan/dangling/trūksta
skaičiai), (3) prijungta prie DAILY/Loop B, (4) backup OK, (5) „LLM-WIKI LINT ĮDIEGTAS".

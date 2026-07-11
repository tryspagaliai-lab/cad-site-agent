UŽDUOTIS — LLM-WIKI #2: ATSAKYMAS -> NAUJAS PUSLAPIS (query synthesis compounding). <12 min.
NEleisk viso pytest — tik taikinius. LLM kvietimams griežti timeout'ai. Telegram TRUMPAI.
Fail-safe: rašymo klaida NIEKADA nelaužo atsakymo vartotojui. €0.

SAUGUMAS: raktų nespausdink/necommit'ink. Nauji puslapiai = DRAFT/human_gate, jokio auto-promote.

KONTEKSTAS: kai HERA atsako į KLAUSIMĄ (vault_query/naršymo kilpa) ir sugeneruoja vertingą SINTEZĘ
(palyginimą, analizę, ryšį per kelis šaltinius), ji dabar nueina į Telegram ir DINGSTA. Karpathy pattern:
vertingi atsakymai grąžinami į vault kaip nauji puslapiai, kad žinios kauptųsi.

1) SINTEZĖS FIKSAVIMAS query kelyje (hera_query/naršymo kilpa): PO atsakymo suformavimo, jei atsakymas yra
   SUBSTANTIVI sintezė — stage'ink naują /opt/hera-vault/growth/synthesis-<YYYY-MM-DD>-<trumpas-hash>.md.
   Kriterijus (deterministinis, pigus, kad NEspam'intų): (a) atsakymas rėmėsi >=2 skirtingais šaltinio puslapiais
   (cituoti/naudoti nav kilpoje), IR (b) atsakymo ilgis > ~300 simb., IR (c) NE „nerandu"/„dokumente to nėra"
   /pasisveikinimas. Jei kriterijus netenkinamas — NIEKO nerašyk (trivialūs klausimai nekaupiami).
2) PUSLAPIO FORMATAS: frontmatter (status: draft, human_gate: true, kind: synthesis, source_query: <klausimas>,
   created, sources: [puslapiai]); kūne — atsakymas + „## Susiję" su `[[nuorodomis]]` į šaltinio puslapius
   (naudok #1 wiki konvenciją). Provenance: „auto-sintezė iš klausimo, human_gate; NIEKO nepromote'inta".
3) JUNGIKLIS: HERA_SYNTH=1 įjungia (default 1); =0 rollback be kodo. Įrašyk =1 /root/hera.env.
4) DEDUP/RIBA: jei labai panaši sintezė jau yra (tas pats klausimo hash) — nekurti dublio. Fail-safe: rašymo
   klaida -> log + atsakymas vartotojui vis tiek grąžinamas.
5) TESTAS: (a) klausimas, kuris sintezuoja per >=2 šaltinius -> naujas synthesis puslapis sukurtas su
   nuorodomis (parodyk kelią + frontmatter, be raktų); (b) trivialus klausimas („kas yra ATDP?" jei 1 šaltinis
   arba trumpas) -> puslapis NEkuriamas; (c) fail-safe: dirbtinė rašymo klaida -> atsakymas vis tiek grąžintas.
6) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup (secret-scan).
   Viešo NELIESK. Nauji puslapiai nusisync'ins per vault cron (ir pateks į lint/grafą).

TELEGRAM (trumpai, be raktų): (1) sintezės fiksavimas veikia (kriterijus), (2) testas — sukurtas synthesis
puslapio pavyzdys + trivialus praleistas, (3) HERA_SYNTH=1, fail-safe, backup OK, (4) „WIKI SINTEZĖ ĮDIEGTA".

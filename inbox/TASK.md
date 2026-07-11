UŽDUOTIS — GRĄŽINTI PILNĄ ANALIZĘ VARTOTOJUI PO APDOROJIMO (dabar mato tik eilės ACK). <12 min.
NEleisk pytest. Telegram TRUMPAI. Fail-safe: siuntimo klaida NIEKADA nelaužo ingest.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta HERA kodą — push į PRIVATŲ hera-core-backup.

PROBLEMA (vartotojo): anksčiau atsiuntus turinį botas grąžindavo PILNĄ skaitomą analizę (santrauka, pagrindiniai
taškai, konceptai, transkripcija — „PARSER" formatas). Kai perjungėm į eilės ACK („🔎 Priimta, apdorojama eilės
tvarka"), pilnos analizės grąžinimas dingo. Vartotojas nori JĄ SKAITYTI. Analizė vis tiek generuojama
(extracted/<data>/<id>/full.md ar panašiai) — tik nebesiunčiama atgal.

1) RASK: (a) kur po ingest apdorojimo guli žmogui skaitoma analizė (greičiausiai /opt/hera-vault/extracted/
   <data>/<id>/full.md arba struktūrizuotas summary); (b) kur SENIAU ji buvo siunčiama vartotojui (n8n „Poll &
   Process" sinchroninis kelias ar processor), kad atkurtum tą elgseną.

2) ATKURK PILNOS ANALIZĖS SIUNTIMĄ: kai processor'ius BAIGIA apdoroti ingest'ą (ten kur dabar siunčia trumpą
   „📥 Priimta: title | selektorius | taryba" ACK), PAPILDOMAI nusiųsk vartotojui PILNĄ analizę (full.md turinį)
   į tą patį Telegram chat (per tą patį botą, kurį vartotojas naudoja — PARSER/hera bot outbound).
   - Trumpas eilės ACK gavimo momentu LIEKA.
   - Pilna analizė ateina PO apdorojimo (~kai baigta).

3) ILGIO TVARKYMAS (Telegram riba ~4096): analizę siųsk DALIMIS — skaidyk į ≤3800 simb. gabalus, po eilučių
   ribų (ne per vidurį žodžio), su „(dalis k/n)" žyme. (Taip PARSER darydavo anksčiau — kelios žinutės.)
   Jei dalių labai daug (>8) — vietoj to siųsk kaip .md DOKUMENTĄ (sendDocument) su trumpu antraštės tekstu.
   Pasirink automatiškai pagal ilgį; aprašyk ataskaitoje ką pasirinkai.

4) JUNGIKLIS: HERA_FULL_ANALYSIS=1 įjungia pilnos analizės siuntimą (default 1); =0 rollback be kodo.
   Įrašyk =1 /root/hera.env.

5) FAIL-SAFE: siuntimo/skaidymo klaida -> log + tęsk (ingest įrašytas, ACK jau nusiųstas); NIEKADA nelaužk pipeline.

6) TESTAS: (a) paimk 1 JAU apdorotą kandidatą (turintį full.md) ir perleisk siuntimo funkciją -> vartotojas gautų
   pilną analizę dalimis (arba dokumentu); parodyk kiek dalių/ar dokumentas (be raktų, be viso turinio — tik
   metrikos); (b) fail-safe: dirbtinė siuntimo klaida -> ingest nesulūžta.

7) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ (ir/ar n8n patch į n8n/) + push į PRIVATŲ hera-core-backup
   (secret-scan). Viešo repo NELIESK.

TELEGRAM (trumpai, be raktų): (1) pilna analizė vėl grąžinama po apdorojimo (dalimis ar dokumentu — kaip),
(2) eilės ACK liko gavimo momentu, (3) HERA_FULL_ANALYSIS=1, fail-safe, backup OK, (4) „PILNA ANALIZĖ GRĄŽINTA".

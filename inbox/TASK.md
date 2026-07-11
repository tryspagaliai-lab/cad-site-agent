UŽDUOTIS — PII VALYMAS (Rampart-stilius) PRIEŠ SIUNČIANT Į IŠORINIUS MODELIUS. <12 min.
NEleisk viso pytest — tik taikinius. Telegram TRUMPAI. Fail-safe: valymo klaida NIEKADA nelaužo pipeline.

SAUGUMAS: raktų nespausdink/necommit'ink. Privatu; jei liesta HERA kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: iš dev-tools video (job 7ccxbp) idėja „Rampart" — pašalinti asmens duomenis (PII) iš teksto PRIEŠ
jam pasiekiant išorinius LLM tiekėjus. HERA to neturi; vartotojui svarbu (mokosi AI security + privatumas).
Diegiam kaip SISTEMOS dalį, ne skill.

1) MODULIS /opt/hera-processor/hera_pii.py (deterministinis regex v1, be ONNX):
   funkcijos scrub(text) -> (clean_text, mapping) ir restore(text, mapping).
   Dengia bent: el. paštas, telefono nr. (tarpt. formatai), kredito kortelės (su Luhn/kontrolinė), IBAN,
   „SSN"-tipo ID (xxx-xx-xxxx), URL su token'ais (?token=/api_key=). Pakeičia žymėm [EMAIL_1],[PHONE_1],
   [CARD_1],[IBAN_1],[ID_1]... (numeruotos, tas pats originalas -> ta pati žymė). restore atstato atgal.
   NEliesk paprasto teksto, kuris nėra PII (mažai false-positive: kortelėms Luhn, IBAN checksum).

2) ĮPINK į IŠORINIŲ tiekėjų kelią: hera_council.py juror digestas, siunčiamas į Groq/OpenAI/OpenRouter/NVIDIA
   (NE native/lokalūs) — prieš siuntimą scrub(digest), po atsakymo verdiktui restore NEreikia (juror grąžina tik
   score/verdict). Gemini kelią (jei native/Google) irgi valyk — nes tai irgi išorinis tiekėjas. Tik selektoriaus/
   vidiniai vault įrašai LIEKA neužtušuoti (asmens duomenų valymas TIK prieš IŠORINĮ tinklą).
   GRIEŽTAI fail-safe: scrub krenta -> log + siųsk originalą (geriau veikti nei blokuoti) ARBA (saugiau) praleisk tą
   juror'į — pasirink saugesnį, aprašyk ataskaitoje.

3) JUNGIKLIS: env HERA_PII=1 įjungia (default 1); HERA_PII=0 rollback be kodo. Įrašyk =1 /root/hera.env.

4) TESTAS (taikinys): (a) scrub("My SSN is 472-01-0004, email a@b.com") -> žymės, restore atstato 1:1;
   (b) kortelė su blogu Luhn NEtušuojama (ne PII); (c) 1 realus council digestas pro scrub -> parodyk kad
   asmens duomenų nebeliko siunčiamame tekste (be raktų).

5) DURABILUMAS: kopija į /opt/cad-site-agent/n8n/hera/ + push į PRIVATŲ hera-core-backup (secret-scan).
   Viešo repo NELIESK.

TELEGRAM (trumpai, be raktų): (1) hera_pii.py veikia — testų a/b rezultatai, (2) įpinta į council išorinį kelią
(fail-safe elgsena), HERA_PII=1, (3) privatus backup OK, (4) „PII VALYMAS ĮDIEGTAS".

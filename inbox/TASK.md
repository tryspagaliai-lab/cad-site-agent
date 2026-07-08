UŽDUOTIS — HERA model-fallback (procesoriaus atsparumas Gemini 503). Autonomiškai, atsargiai.
NELIESK kitų fazių/logikos — tik gemini.py sluoksnį. Nemokama (visi Gemini free modeliai). Atsiskaityk į Telegram TRUMPAI.

Problema: /opt/hera-processor/gemini.py prikaltas prie vieno modelio (gemini-flash-latest), be fallback.
Tas modelis dabar globaliai 503'ina → job'ai dead-letter'ina. (n8n turi fallback, procesorius — ne.)

1) MODELIŲ FALLBACK. gemini.py: vietoj vieno modelio — SĄRAŠAS, konfigūruojamas env `HERA_GEMINI_MODELS`
   (kableliais), su protingu default: `gemini-flash-latest,gemini-2.5-flash,gemini-2.0-flash,gemini-flash-lite-latest`.
   Logika: bandyk 1-ą modelį (su esamu retry/backoff); jei persistentiškai 503/quota/unavailable → **rollink į kitą**
   modelį sąraše; grąžink pirmą sėkmę. Išlaikyk esamą elgseną (thinkingBudget=0 ir t.t.), NEkeisk API rakto/kvietimų
   formato. Suderink su laikinu `HERA_GEMINI_MODEL` override (jei nustatytas — pirmas sąraše).
   LoginK, kuris modelis suveikė (į trajektorijų meta arba processor log).

2) TESTAS: (a) unit — kai 1-as modelis 503, ar rolina į kitą ir grąžina rezultatą; (b) realus — paleisk ištraukimą
   ir query su dabar 503'inančiu flash-latest → turi PRAEITI per fallback (pvz. gemini-2.5-flash). Parodyk, kuris suveikė.

3) RE-DRIVE: dead-letter'intus job'us (pvz. 20260708T165445Z-ljsqy5 ir kt., kritusius dėl 503) paleisk iš naujo
   per naują fallback kelią. Suskaičiuok atgaivinta/liko.

4) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk.

Į Telegram: modelių sąrašas, testas (fallback veikia?), kiek dead-letter atgaivinta, ir aiškiai
„MODEL-FALLBACK BAIGTAS".

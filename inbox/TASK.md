UŽDUOTIS — HERA Fazė 2: pilnas gilaus ištraukimo pipeline VPS'e (Gemini free). Dirbk autonomiškai
(superpowers OK: planuok, TDD kur verta, self-test). Atsiskaityk lietuviškai į Telegram, trumpai.
Nieko netrink; neliesk esamo ingest worker'io PRIĖMIMO dalies (tik SKAITYK jo vault'ą).

TIKSLAS: kiekvienas įkeltas job'as (url/youtube/file[image,pdf,audio,video]/text/council_decision)
turi būti GILIAI, PILNAI ištrauktas (NE santrauka — visas turinys, nesvarbu ilgis/trukmė).
Ilgi audio/video KARPOMI gabalais (ffmpeg), kiekvienas apdorojamas, rezultatai sujungiami.
Po ištraukimo — HERA selektorius atrenka, kas tinka SISTEMOS augimui/tobulėjimui/plėtrai.

VARIKLIS: Google Gemini free (raktas GEMINI_KEY iš /root/ai_digest.env; modelis gemini-flash-latest,
kaip /root/ai_digest.py — REST per urllib; multimodalui naudok inline_data (base64) mažiems,
File API dideliems). €0. Jokio mokamo API.

ARCHITEKTŪRA (decoupled nuo ingest, kad priėmimas liktų greitas):
- Kodas: /opt/hera-processor/ (moduliai: fetch, extractors/<kind>.py, hera_select.py, dispatcher.py).
- Procesorius (systemd `hera-processor.service` arba cron */2) skenuoja /opt/hera-vault/ingest/ neapdorotus job'us,
  paleidžia teisingą ekstraktorių, rašo rezultatą į /opt/hera-vault/extracted/<data>/<id>/ (full.md + meta.json),
  pažymi apdorotą (state failas, kad nekartotų).
- Priklausomybės: `apt-get install -y ffmpeg`; `pip install yt-dlp trafilatura` (į venv /opt/cad-venv ar naują).

EKSTRAKTORIAI (deep, ne summary):
- url: fetch HTML → trafilatura pilnas tekstas → Gemini struktūrina (pilnas turinys, ne trumpinys).
- youtube/audio/video: yt-dlp atsisiunčia; ffmpeg ištraukia audio + karpo ~10 min gabalais; kiekvienas gabalas → Gemini transkripcija+ištraukimas; sujungti. Video: papildomai keli kadrai → Gemini vision.
- image: Gemini vision — pilnas aprašymas + visas matomas tekstas (OCR).
- pdf: tekstas + jei skenuotas, Gemini vision OCR.
- text/council_decision: struktūrinis ištraukimas (council_decision — jei atpažįsti formatą, ištrauk laukus).

HERA SELEKTORIUS (hera_select.py): perskaito ištrauktą turinį ir sprendžia, kas VERTINGA sistemos augimui/
plėtrai (pvz. nauji įrankiai, idėjos, procesai, žinios). Kandidatus rašo į /opt/hera-vault/growth/<data>-<id>.md
su trumpu pagrindimu. Tai self-evolving kilpos pradžia.

SELF-TEST: apdorok JAU esamus 3 flush'intus job'us (url, youtube, photo.jpg iš /opt/hera-vault/ingest/) —
parodyk, kad kiekvienas gavo full.md ir kad HERA selektorius davė growth kandidatų (ar pagrįstai atmetė).
Kiekvieno apdoroto job'o trumpą rezultatą siųsk į Telegram.

DURABILUMAS: galutinį kodą nukopijuok ir į /opt/cad-site-agent/n8n/hera/ (kad vėliau būtų galima commit'inti;
push nedaryk — nėra creds). 

Atsiskaityk į Telegram: kas pastatyta, kokie ekstraktoriai veikia (self-test rezultatai kiekvienam kind),
ar procesorius UP, kur guli rezultatai/growth kandidatai, ir kas dar neužbaigta (jei „viską iš karto" netilpo).

UŽDUOTIS — HERA Fazė 2 UŽBAIGIMAS (3 spragos). Dirbk autonomiškai. Į Telegram atsiskaityk TRUMPAI,
bet BŪTINAI aiškiu galutiniu statusu — NEPALIK „palaukiu…". Nieko netrink.

Būklė (diagnostika): url✅ image✅ ekstrakcija veikia (full.md yra); youtube❌ (extracted/2026-07-06/…chw25r tuščias);
hera-processor.service INACTIVE; growth/ tuščia (HERA selektorius nepasileido).

1) PROCESSOR SERVISAS: padaryk hera-processor patikimą, nuolat veikiantį — systemd su Restart=always,
   ARBA cron */2 su flock. Jis ima neapdorotus /opt/hera-vault/ingest job'us ir apdoroja FONE, kad ilgi
   job'ai (youtube/video) neblokuotų ir turas nenutrūktų. `systemctl enable --now`. Patvirtink, kad active+enabled.

2) YOUTUBE/AUDIO/VIDEO ekstraktorius — pataisyk kad realiai BAIGTŲ. Testuok ant esamo job'o chw25r:
   yt-dlp → audio → ffmpeg karpo ~10 min gabalais → kiekvienas gabalas per Gemini (File API dideliems) →
   sujungti į vieną full.md. Jei labai ilgas — leisk fone ir pranešk pabaigus. Turi atsirasti
   extracted/2026-07-06/…chw25r/full.md su PILNU turiniu (ne santrauka).

3) HERA SELEKTORIUS: paleisk ant visų 3 apdorotų (url, image, youtube). Atrink, kas verta sistemos
   augimui/plėtrai → rašyk į /opt/hera-vault/growth/<data>-<id>.md su trumpu pagrindimu. Jei atmeta — irgi
   trumpai pagrįsk.

4) KOKYBĖ: patikrink, kad url ir image full.md yra GILUS, PILNAS turinys (ne 2 sakiniai). Jei per seklu —
   sustiprink Gemini prompt'ą ir perleisk.

Pabaigoje į Telegram: kiekvieno kind statusas (veikia/ne), ar processor UP+enabled, kiek growth kandidatų,
ir aiškiai „FAZĖ 2 BAIGTA" arba ko konkrečiai trūksta.

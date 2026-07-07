UŽDUOTIS — YouTube patikimumas: proxy sluoksnis + nemokami apėjimai. Autonomiškai.
NELIESK kitų fazių — tik youtube kelią sustiprink. Atsiskaityk į Telegram TRUMPAI, aiškiu statusu.

Problema: YouTube blokuoja VPS IP (yt-dlp IR transcript-api → RequestBlocked). Reikia, kad youtube veiktų
patikimai. Padaryk DVI dalis:

1) PROXY PALAIKYMAS (kad būtų galima padaryti 100% patikimą). youtube fetch'eris skaito proxy iš
   `/root/hera.env` kintamojo `HERA_YT_PROXY` (http/https/socks5). Jei nustatyta — transcript-api IR yt-dlp IR
   bet koks YouTube HTTP eina PER proxy. Jei tuščia — praleisk į nemokamus apėjimus (žemiau). Dokumentuok, kaip
   įrašyti proxy (viena eilutė į /root/hera.env), kad vėliau būtų galima įjungti.

2) NEMOKAMI APĖJIMAI (veikia BE vartotojo proxy) — youtube subtitrų gavimas, bandyk eilės tvarka, imk pirmą sėkmę:
   a) transcript-api per HERA_YT_PROXY (jei nustatyta);
   b) VIEŠI YouTube veidrodžiai — Invidious (`/api/v1/captions/{id}`) ir Piped (`/streams/{id}` → subtitrų URL),
      su keliais dabar veikiančiais instancais (sąrašą laikyk konfige, lengvai atnaujinamą); parsink titrus → transkriptas;
   c) Gemini vieno-skambučio kelias (dabartinis veikiantis) — galutinis fallback.
   Kiekvienam job'ui loginK, KURIS metodas suveikė (į trajektorijas).

3) TESTAS iš VPS: patikrink kiekvieną šaltinį (transcript-api, 2-3 Invidious/Piped instancai, Gemini) ir
   parodyk, KURIE realiai veikia iš šito serverio IP. Sąžiningai — jei visi vieši veidrodžiai irgi blokuoti,
   pasakyk, kad reikia proxy (ir rekomenduok pigų/nemokamą variantą, pvz. Webshare free tier).

4) RE-DRIVE: likusius nepavykusius youtube job'us paleisk per naują grandinę. Suskaičiuok atgaivinta/liko.

5) DURABILUMAS: kodą į /opt/cad-site-agent/n8n/hera/. Push nedaryk.

Į Telegram: kurie šaltiniai veikia iš VPS, ar reikia proxy, kiek video atgaivinta/liko, kaip įjungti proxy
(HERA_YT_PROXY), ir aiškiai „YOUTUBE PROXY BAIGTAS".

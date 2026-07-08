UŽDUOTIS — Pataisyk: tekstinis KLAUSIMAS iš Telegram nepasiekia HERA (ingest eilė tuščia 3h),
o URL'ai praeina. Router+query (Fazė 6) veikia, bet job'as neatkeliauja. Autonomiškai, atsargiai.
Atsiskaityk į Telegram TRUMPAI.

DIAGNOZĖ (rask tikrą priežastį):
1) n8n „Link Parser" (linkparserwork01): kaip Telegram trigger'is priima žinutes? Ar paprasto TEKSTO žinutė
   (be URL) forward'inama į hera-ingest (8799) kaip kind=text? Patikrink node logiką (ar filtruoja tik url/media,
   ar meta text be entities). Eksportuok ir peržiūrėk „Poll & Process".
2) Ar n8n vis dar POLL'ina Telegramą? Patikrink n8n vykdymų istoriją/logus (docker logs n8n-n8n-1 --tail 100)
   dėl paskutinių kelių valandų — ar buvo gauta žinučių po 17:00, ar polling sustojo/kliūva (pvz. 409 conflict).
3) Ar žinutė apskritai pasiekė botą? (atsargiai — NEdaryk getUpdates, jei n8n poll'ina; naudok n8n logus).

FIX:
4) Padaryk, kad paprasto teksto žinutė (klausimas) BŪTŲ forward'inama į hera-ingest kaip kind=text →
   tada hera_router ją klasifikuos (question/ingest/feedback). Jei polling sustojęs — restart'ink n8n švariai.
5) GEMINI 503 atsparumas query kelyje: jei Gemini atsakymo generavimui persistentiškai 503'ina, vietoj TYLOS
   nusiųsk į Telegram aiškų „⏳ Gemini šiuo metu perkrautas, bandyk vėliau" (kad vartotojas nebūtų paliktas be žinios).
   (Backoff/retry jau yra — tik užtikrink graceful pranešimą.)

TESTAS:
6) Sumuliuok/realiai patikrink: tekstinis klausimas „kas yra ATDP?" → turi pasiekti hera-ingest → router=question →
   query → atsakymas su šaltiniais atgal į Telegram. Parodyk, kad pilnas kelias veikia iš Telegram pusės.

Neliesk kitų fazių. Push nedaryk. Į Telegram: kokia buvo tikroji priežastis, kas pataisyta, ar testas praėjo,
ir „KLAUSIMŲ KELIAS BAIGTAS".

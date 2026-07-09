UŽDUOTIS — NVIDIA juror'iai (GREITAI ir MINIMALIAI). NEperstatyk nieko, NEleisk viso testų rinkinio.
Tikslas: įjungti NVIDIA NIM kaip tarybos juror'ius ir GREITAI patvirtinti kad balsuoja. Būk EFEKTYVUS — ne daugiau
kaip keli žingsniai. Atsiskaityk į Telegram TRUMPAI, BE raktų.

SAUGUMAS: raktų reikšmių NIEKADA nespausdink/necommit'ink/nerodyk. Tik vardai/prefiksai/statusai.

GREIČIO TAISYKLĖS (svarbu):
- NENAUDOK lėtų reasoning modelių smoke-teste. Rink INSTRUCT (ne-thinking) variantus.
- Kiekvienam HTTP kvietimui griežtas timeout 30s. Jokių ilgų retry grandinių (max 1 retry).
- NELEISK viso pytest rinkinio. Tik 1 greitas tikslinis testas jei būtinas.
- Visas darbas turi tilpti gerokai po 15 min. Jei kas lėta — praleisk ir raportuok, neblokuok.

ŽINGSNIAI:
1) NVIDIA_API_KEY patikra: 1 kvietimas GET https://integrate.api.nvidia.com/v1/models (timeout 30s).
   Raportuok HTTP statusą + kiek modelių. Iš sąrašo išrink 2 GREITUS INSTRUCT juror'ius, prioritetas KIMI ir QWEN
   (pvz moonshotai/kimi-k2-instruct, qwen/qwen2.5-... instruct) — NE „r1"/„thinking"/„reasoning" variantus.
   Įrašyk juos į konfigą (env HERA_NVIDIA_MODELS arba default kode) hera_council.py.

2) 1 GREITAS live-vote testas: paleisk council TIK su NVIDIA juror'iais ant trumpo sufabrikuoto kandidato
   (2-3 sakiniai), timeout 30s/kvietimui. Patvirtink: ar Kimi/Qwen grąžino {verdict,score,domain_fit}?
   NEleisk pilno 9-modelių off-domain testo — tik šitą greitą.

3) Kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push NEDARYK.

TELEGRAM (trumpai): (1) NVIDIA /models statusas + kiek modelių, (2) kurie 2 NVIDIA juror'iai parinkti (vardai),
(3) ar jie realiai grąžino balsą greitame teste (Kimi balsuoja? taip/ne + score), (4) „NVIDIA JUROR'IAI ĮJUNGTI".
Baik per kelias minutes.

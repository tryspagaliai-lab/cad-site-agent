UŽDUOTIS — HERA ingest CUTOVER (perjungti n8n į naują VPS worker'į + ištuštinti eilę).
Dirbk autonomiškai. Atsiskaityk lietuviškai į Telegram, TRUMPAI.

Kontekstas: Fazė 1 baigta — naujas worker'is /opt/hera-ingest/ (systemd hera-ingest.service) ACTIVE,
pasiekiamas IŠ n8n konteinerio adresu http://172.18.0.1:8799 (/health OK, self-test OK).
n8n „Link Parser" (linkparserwork01) node „Poll & Process" vis dar turi
INGEST_BRIDGE=http://100.68.100.14:8799 (dingęs laptopas). Dabar perjungiam.

1) BACKUP: `docker exec -u node n8n-n8n-1 n8n export:workflow --id=linkparserwork01 --output=/root/linkparser_pre_cutover.json`
   (patvirtink, kad failas yra ir ne tuščias).
2) Pakeisk INGEST_BRIDGE node'e „Poll & Process": http://100.68.100.14:8799 -> http://172.18.0.1:8799
   (eksportuok, pakeisk konstantą, importuok/patch'ink ir publikuok/restart'ink taip, kad workflow liktų ACTIVE;
   naudok tą patį metodą kaip anksčiau su router'iu, jei tinka). Patikrink, kad pakeitimas įsigaliojo.
3) Patikrink ryšį: iš n8n konteinerio `wget -qO- http://172.18.0.1:8799/health` -> OK.
4) FLUSH: paleisk eilės apdorojimą (flushPendingJobs mechanizmas node'e — pvz. sutrigerink workflow rankiniu
   paleidimu ar per health-atsistatymo kelią). Turi būti apdoroti 3 laukiantys job'ai (1 file=photo.jpg, 1 url, 1 youtube).
5) VERIFIKUOK: eilė pending-ingest tuščia; nauji job'ai atsirado /opt/hera-vault/ingest/<data>/...
   Ypač patvirtink, kad vartotojo photo.jpg job'as apdorotas ir failas vault'e.
6) Nieko netrink. Jei kas nepavyktų — grąžink seną INGEST_BRIDGE iš backup ir pranešk.

Atsiskaityk į Telegram: cutover OK?, ar workflow liko ACTIVE, kiek job'ų flush'inta, ar photo.jpg vault'e,
ir kaip atsukti jei reikės. Pabaigoj: „CUTOVER BAIGTAS" ar kas trūksta.

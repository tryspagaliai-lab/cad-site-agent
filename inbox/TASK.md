UŽDUOTIS — atkurti HERA ingest worker'į VPS'e (FAZĖ 1: BUILD + TEST, BE cutover).
Dirbk autonomiškai (superpowers OK). Atsiskaityk lietuviškai į Telegram, TRUMPAI.

Kontekstas: HERA ingest worker'is (port 8799) buvo tik dingusiame laptope; kodo GitHub'e nėra.
n8n „Link Parser" (linkparserwork01) VPS'e priima failus ir laukia to worker'io.
ŠI FAZĖ: pastatyk NAUJĄ minimalų worker'į ir jį ištestuok. NEKEISK n8n INGEST_BRIDGE ir
NEFLUSHINK realios eilės — cutover bus atskira komanda. Nieko netrink.

1) Ištrauk TIKSLŲ ingest-bridge kontraktą iš node „Poll & Process":
   `docker exec -u node n8n-n8n-1 n8n export:workflow --id=linkparserwork01 --output=/tmp/lp.json`
   Rask: portas/endpoint'ai, HTTP metodas, payload laukai kiekvienam job kind (file/url/youtube),
   auth (INGEST_BRIDGE_TOKEN header'io vardas), health-check kelias, kokio atsakymo n8n tikisi.

2) Pastatyk minimalų worker'į /opt/hera-ingest/ (Python stdlib http.server užtenka), kuris:
   - įgyvendina TĄ PATĮ kontraktą (tie patys endpoint'ai, token'as, atsakymų formatas),
   - kiekvieną job'ą DURABLIAI saugo į /opt/hera-vault/ingest/<YYYY-MM-DD>/<id>/ (payload.json + failas),
   - turi /health endpoint,
   - JOKIOS „protingos" analizės (tai vėliau) — tik priima + saugo + ack,
   - servisas: systemd `hera-ingest.service`, klausosi 0.0.0.0:8799.

3) TINKLAS (svarbu): n8n sukasi Docker konteineryje, tad iš konteinerio „127.0.0.1" = pats konteineris.
   Nustatyk adresą, kuriuo worker'is pasiekiamas IŠ n8n konteinerio (docker bridge gateway, pvz.
   172.17.0.1, arba host.docker.internal). Patikrink: `docker exec n8n-n8n-1 sh -c 'wget -qO- http://<addr>:8799/health'`.
   Užrašyk teisingą adresą — jo reikės cutover'iui.

4) SELF-TEST: paleisk servisą, nusiųsk pavyzdinį file+url+youtube payload'ą TIESIAI į worker'į,
   patikrink kad jie atsiranda /opt/hera-vault/. Parodyk rezultatą.

Atsiskaityk į Telegram: kontrakto esmė, kur worker'is, ar servisas UP, koks adresas pasiekiamas
iš n8n konteinerio, self-test rezultatas. Pabaigoj pasakyk: „PARENGTA CUTOVER'IUI" ar ko trūksta.

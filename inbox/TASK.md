UŽDUOTIS — N8N MELAGINGO „400 PRIVATUS" KELIO IŠJUNGIMAS + EILĖS ACK (VIENA SIAURA UŽDUOTIS, TIK N8N). <12 min.
HERA kodo NEliesk. NEleisk pytest. Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk. Backup prieš keitimą.

KONTEKSTAS (iš 17:47 diagnostikos, tavo paties memory): n8n gyvame workflow'e (linkparserwork01) yra atskiras
SINCHRONINIS Gemini-video kelias, kuris video burst'ų metu grąžina vartotojui MELAGINGĄ „Klaida (400): video
privatus, regionui apribotas..." — nors HERA jobas dar tik LAUKIA eilėje (dispatcher ~5 min/job dėl tarybos).
Vartotojas dėl to pagrįstai supyko: sistema sako „neveikia", kai iš tikrųjų „palauk eilėje". Tavo paties
užrašas: „reiktų jį išjungti/pataisyti n8n sqlite'e".

1) BACKUP: eksportuok linkparserwork01 į /root/linkparser_pre_syncfix.json.
2) IŠJUNK/APEIK sinchroninį Gemini-video kelią youtube nuorodoms: youtube job'ai turi eiti TIK per
   hera-ingest (8799) eilę (async), be jokio sinchroninio bandymo, kuris gali grąžinti klaidą vartotojui.
3) EILĖS ACK vietoj melo: priėmus youtube/url/file job'ą, atsakyk vartotojui iškart trumpai:
   „🔎 Priimta į eilę (pozicija N)" — poziciją paimk iš pending eilės ilgio (GET į 8799 jei yra endpoint'as,
   arba suskaičiuok pending katalogą; jei sunku — bent „🔎 Priimta, apdorojama eilės tvarka, ~5 min/darbas").
   NIEKADA nerodyk klaidos, kol HERA grandinė realiai nebandė ir nekrito — klaidas praneša processor'ius
   savo žinute (jis dabar sako tiesą — kurie šaltiniai bandyti).
4) Publikuok (publish, kaip mcprouterdesk001 pamoka), workflow lieka ACTIVE.
5) TESTAS: per n8n CLI/exec paduok testinę youtube nuorodą (gali būti ta pati uCKhOmth2ms — bet ji jau apdorota,
   tad geriau bet koks kitas trumpas viešas video ARBA dry-run be realaus siuntimo jei įmanoma) — patikrink:
   (a) vartotojui grįžta eilės ACK, ne klaida; (b) jobas atsiranda pending eilėje.
6) DURABILUMAS: patch skriptas į /opt/cad-site-agent/n8n/ (lokaliai, be push į viešą). Jei buvo pakeitimų
   /opt/hera-ingest — push į privatų hera-core-backup.

TELEGRAM (trumpai, be raktų): (1) sinchroninis kelias išjungtas?, (2) eilės ACK veikia — testo pavyzdys,
(3) backup kelias, (4) „N8N EILĖS FIX BAIGTA".

UŽDUOTIS — N8N LINK PARSER FIX: YOUTUBE URL NORMALIZACIJA (FOKUSUOTAI, SU BACKUP+ROLLBACK). <15 min.
NEleisk pytest, hera_*.py NEliesk — keičiamas TIK n8n workflow linkparserwork01. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS (iš 21:00 diagnostikos): sugadinta share nuoroda youtu.be/<id>?is=... (vietoj ?si=) nulaužė n8n
„Link Parser" httpRequest URL-išskleidimo žingsnį -> 404 po 123s vartotojui, nors pats video galiojantis.
Sprendimas (vartotojas patvirtino): normalizuoti YouTube nuorodas PRIEŠ resolve, continueOnFail — antras saugiklis.

1) BACKUP PIRMA: eksportuok esamą workflow į /root/linkparser_pre_ytfix.json
   (docker exec -u node n8n-n8n-1 n8n export:workflow --id=linkparserwork01 ...). Be backup'o NIEKO nekeisk.

2) PATCH (minimalus, addityvus — metodika kaip patch_router2.py):
   a) Žingsnyje, kur apdorojama gauta žinutė PRIEŠ httpRequest resolve (Poll & Process ar atitinkamas code node),
      pridėk YouTube normalizaciją: regex'u ištrauk 11 simbolių video ID iš youtu.be/<ID>, watch?v=<ID>,
      shorts/<ID>, embed/<ID> ([A-Za-z0-9_-]{11}); jei rasta -> kanoninis https://www.youtube.com/watch?v=<ID>,
      VISI query parametrai (si/is/feature/t...) išmetami, o httpRequest resolve žingsnis YouTube nuorodai
      APLENKIAMAS (youtu.be išskleidimo nebereikia — ID jau turim). Ne-YouTube nuorodų elgsena NEKEIČIAMA.
   b) httpRequest resolve node'ui įjunk continueOnFail (antras saugiklis likusioms nuorodoms) — jei resolve
      krenta, žinutė turi eiti toliau su originaliu URL, ne grąžinti axios klaidą vartotojui.
   c) Publikuok pagal veikiančią metodiką (kaip mcprouterdesk001 pamoka: gali reikėti publish, ne vien update)
      ir įsitikink, kad workflow liko ACTIVE.

3) TESTAS:
   a) Normalizacijos logika: perleisk regex'ą node -e (ar python3) su atvejais: youtu.be/iDo4fIYE98Q?is=55Ex...,
      youtu.be/iDo4fIYE98Q?si=abc, youtube.com/watch?v=iDo4fIYE98Q&t=10, youtube.com/shorts/<id>, ne-YouTube URL
      (turi likti nepakeistas). Visi turi duoti teisingą rezultatą.
   b) E2E per Telegram negali pats — ataskaitoje paprašyk vartotojo persiųsti botui TĄ PAČIĄ sugadintą nuorodą
      (youtu.be/iDo4fIYE98Q?is=55Ex1GVnvlOx4yzD) kaip galutinį testą.
   c) DUBLIO PASTABA: šis video jau apdorotas 2x (2ls50k, ne08n5) — jei procesorius turi dedup pagal video ID,
      trečias siuntimas tik patvirtins flow; jei dedup NĖRA, ataskaitoje pažymėk (būsimam darbui, dabar nekurk).

4) ROLLBACK jei kas negerai: importuok /root/linkparser_pre_ytfix.json atgal ir pažymėk ataskaitoje FAILED+priežastis.

5) DURABILUMAS: patch skriptą padėk /opt/cad-site-agent/n8n/ (pvz. patch_linkparser_ytnorm.py). Push NEDARYK.

TELEGRAM (trumpai, be raktų): (1) backup kelias, (2) patch pritaikytas+workflow ACTIVE? (3) normalizacijos testų
rezultatai (kiek atvejų OK), (4) prašymas vartotojui persiųsti sugadintą nuorodą E2E testui, (5) ar procesorius
turi dedup pagal video ID (taip/ne), (6) „LINK PARSER FIX BAIGTA".

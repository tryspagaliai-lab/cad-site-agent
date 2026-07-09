UŽDUOTIS — DIAGNOSTIKA: INGEST 404 (FOKUSUOTAI, TIK SKAITYK LOGUS, NIEKO NEPERRAŠINĖK). <10 min.
NEperstatyk servisų be reikalo, NEleisk pytest. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk (nei Telegram žinutėje, nei loguose cituojamose eilutėse —
jei log eilutėje yra raktas/token, užmaskuok prieš siųsdamas).

SIMPTOMAS: vartotojas ką tik (2026-07-09 vakaras, po ~20:22) siuntė turinį į @tryspagaliabot ir gavo
„❌ Klaida: Request failed with status code 404 (123s)". Ankstesni du ingest'ai (19:41 ir 20:22) pavyko.
404 po 123s = kažkuris HTTP žingsnis grandinėje: n8n Link Parser -> hera-ingest(8799) -> hera-processor
(trafilatura/YouTube veidrodžiai/Gemini). Rasti KURIS.

1) GREITA BŪKLĖ: systemctl is-active hera-ingest hera-processor; curl -s localhost:8799/health.
   Jei kuris neaktyvus — restart'uok TIK tą servisą ir pažymėk tai ataskaitoje.

2) RASK KLAIDĄ: journalctl -u hera-processor --since "1 hour ago" | tail -100 (ir hera-ingest analogiškai);
   n8n paskutinių execution'ų klaidos: docker exec -u node n8n-n8n-1 n8n ... arba docker logs n8n-n8n-1 --since 1h.
   Ieškok: 404, kokio kind buvo job'as (url/youtube/file/text), koks tikslus URL/endpoint'as grąžino 404.

3) DIAGNOZĖ (pasirink pagal radinį, NIEKO daugiau nekeisk):
   a) jei 404 = pats vartotojo siųstas URL / nebeegzistuojantis puslapis -> tai ne bug'as; ataskaitoje pasakyk
      kad turinys nepasiekiamas ir kokį URL siuntė.
   b) jei 404 = YouTube veidrodžiai (Piped/Invidious) -> patikrink ar VISI 4 grandinės šaltiniai išbandyti ar
      grandinė nutrūko per anksti; jei nutrūko per anksti dėl trivialaus bug'o (pvz. exception ne ta) — gali
      pataisyti MINIMALIAI, kopiją į /opt/cad-site-agent/n8n/hera/, push NEDARYK.
   c) jei 404 = Gemini/kito tiekėjo endpoint'as (pvz. modelio vardas nebegaliojantis) -> ataskaitoje nurodyk
      tikslų endpoint'ą ir modelį, NEkeisk kodo — lauk vartotojo sprendimo.
   d) jei 404 = hera-ingest route (n8n negali pasiekti 8799 path'o) -> patikrink ar servisas tas pats worker.py,
      ar n8n INGEST_BRIDGE nepasikeitęs; ataskaitoje nurodyk, NEkeisk be reikalo.
   Jei job'as liko pending eilėje — palik, po pataisos/išaiškinimo jis apsidoros arba vartotojas persiųs.

4) PO DIAGNOSTIKOS (tik jei liko laiko): patikrink ar ankstesnė užduotis (SKILL draft
   /opt/hera-vault/skills/verslo-identitetas-ir-svetaine-ai-irankiais/SKILL.md) buvo įvykdyta — failas egzistuoja?
   Jei NE (užduotį perrašė ši diagnostika anksčiau nei runner'is ją paleido) — ataskaitoje pažymėk „SKILL draft
   NEĮVYKDYTA, reikės pakartoti", pačios užduoties dabar nedaryk.

TELEGRAM (trumpai, be raktų): (1) kas grąžino 404 — konkretus žingsnis/URL/endpoint'as ir job kind,
(2) ar servisai gyvi, (3) ar tai (a) blogas šaltinis (b) veidrodžiai (c) tiekėjas (d) infra — viena raidė + sakinys,
(4) ar SKILL draft buvo įvykdytas anksčiau (taip/ne), (5) „DIAGNOSTIKA BAIGTA".

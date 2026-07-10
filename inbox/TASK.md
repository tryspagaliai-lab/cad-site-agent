UŽDUOTIS — DIAGNOSTIKA + FIX: YOUTUBE IŠTRAUKIMO GRANDINĖ NUTRŪKO PER 21s (VIENA SIAURA UŽDUOTIS). <12 min.
NEleisk pytest. Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk (loguose cituojamas eilutes maskuok jei reikia).

SIMPTOMAS: 2026-07-10 ~17:33 vartotojas siuntė youtu.be/uCKhOmth2ms?is=... („Multi-agent is a trap", Sierra
podcast, viešas video). Normalizacija SUVEIKĖ (pateko į pipeline, „Analizuoju video..."), bet po 21s grįžo
„Klaida (400): video privatus, regionui apribotas, arba Gemini negalėjo jo apdoroti". 21s per greitai 4 šaltinių
grandinei (transcript-api -> Piped/Invidious -> Gemini titrai -> Gemini langai) — įtariam ankstyvą nutrūkimą.

1) RASK LOGUOSE šio job'o įrašus (video ID uCKhOmth2ms): kuris grandinės šaltinis buvo bandytas, kuo baigėsi
   KIEKVIENAS (status kodai/exception), ar visi 4 realiai išbandyti, ar grandinė nutrūko ties pirmu/antru.
   Ar 400 iš Gemini (jam padavė video URL?) ar iš veidrodžio?
2) PATIKRINK ŠALTINIUS RANKA tam pačiam ID: transcript-api, bent 2 Piped/Invidious veidrodžiai (curl, ar gyvi
   apskritai?), Gemini titrų kelias. Užsirašyk kas realiai veikia šiandien.
3) FIX pagal radinį (minimalus):
   a) jei grandinė nutrūksta anksti dėl exception/klaidos klasifikavimo — sutvarkyk, kad VISI šaltiniai būtų
      išbandyti prieš pasiduodant, o klaidos žinutė sakytų kurie šaltiniai bandyti.
   b) jei Piped/Invidious veidrodžiai išvis mirę — atnaujink veidrodžių sąrašą gyvais (patikrink ranka) ir/arba
      įjunk HERA_YT_PROXY kelią jei sukonfigūruotas.
   c) jei 400 iš Gemini video kelio — patikrink ar Gemini apskritai gali tą video (region lock realus?); jei
      realus apribojimas — tai ne bug'as, bet žinutė turi skirti „šaltiniai nepasiekiami" nuo „video privatus".
4) TESTAS: perleisk uCKhOmth2ms per ištraukimą — tikslas: transkriptas gautas ARBA aiški ataskaita kurie 4/4
   šaltiniai bandyti ir kodėl krito. Jei pavyko — leisk pipeline'ui baigti normaliai (selektorius+taryba+ACK).
5) DURABILUMAS: pakeitimai (jei buvo) į /opt/cad-site-agent/n8n/hera/ kopiją + push į PRIVATŲ hera-core-backup.
   Viešo repo neliesk.

TELEGRAM (trumpai, be raktų): (1) kuris šaltinis ką grąžino (4 eilutės), (2) diagnozė a/b/c viena raide+sakiniu,
(3) kas pataisyta, (4) ar uCKhOmth2ms galiausiai ištrauktas (taip/ne + kodėl), (5) „YT GRANDINĖS FIX BAIGTA".

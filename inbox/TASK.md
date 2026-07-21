UŽDUOTIS — pataisyti 3 kritusius `aitech` feed'us /root/ai_digest.py (PATIKRINK prieš dėdamas). <10 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Kitų temų (ai/design/agro) NELIESK. Viešo cad-site-agent NELIESK.

KONTEKSTAS: tavo 09:40 ataskaita — 3 aitech blog feed'ai krito: Anthropic rss.xml 404, LangChain blog.langchain.dev/rss/
XML-parse err, LlamaIndex feed.xml 404. Orkestruotojas negali jų patikrinti iš savo konteinerio (allowlist tinklas),
todėl PATS patikrink kandidatus VPS'e ir įdėk TIK veikiančius.

1) PATIKRA (curl su browser User-Agent, timeout 15s; veikiantis = HTTP 200 IR turinys prasideda <?xml arba <rss arba <feed):
   ANTHROPIC pakaitalai (oficialaus RSS nėra — imk GitHub .atom, keyless, patikimi):
     a) https://github.com/anthropics/claude-code/releases.atom
     b) https://github.com/anthropics/anthropic-sdk-python/releases.atom
   LANGCHAIN kandidatai (blogas migravo iš .dev):
     a) https://blog.langchain.com/rss/
     b) https://blog.langchain.dev/rss/ (retest — gal laikina klaida)
   LLAMAINDEX kandidatai:
     a) https://medium.com/feed/llamaindex-blog
     b) https://www.llamaindex.ai/blog/feed
2) KEITIMAS AITECH_FEEDS sąraše:
   - Pašalink 3 mirusius URL (anthropic.com/rss.xml, blog.langchain.dev/rss/ jei retest'as vėl krito, llamaindex.ai/blog/feed.xml).
   - Įdėk veikiančius pakaitalus (Anthropic: abu GitHub .atom kaip broad=False; LangChain/LlamaIndex: pirmą veikiantį kandidatą).
   - Jei kuriam šaltiniui NĖ VIENAS kandidatas neveikia — tiesiog pašalink mirusį ir pažymėk ataskaitoje (geriau mažiau, bet švariai).
3) PATIKRA PO: python3 -c "import ast; ast.parse(open('/root/ai_digest.py').read()); print('OK')".
   Testinis paleidimas TIK aitech (kaip praeitą kartą, 🧪 be seen saugojimo) — patvirtink kad nauji feed'ai duoda įrašų ir nėra klaidų.
4) BACKUP: cp /root/ai_digest.py /root/hera-core-backup/ai_digest.py.$(date +%s) (ir/arba į /opt/hera-processor kaip darei). Nepavykus — atstatyk, pranešk, STOP.

ATASKAITA (HERA botas, trumpai): kiekvienam iš 3 — kandidatų testo rezultatai (URL → HTTP kodas) ir kas įdėta/pašalinta; ast OK; test-run įrašų skaičius; backup OK.

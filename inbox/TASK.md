UŽDUOTIS — dizaino botas: pridėti naujus šaltinius (patikrinus RSS) + TLDR Design filtras. ai_digest.py TOPICS['design']. <15 min.
Fail-safe: jei abejoji STOP+backup restore. NEleisk pytest. €0. Ataskaita TIK į HERA botą. Kitų temų (ai/agro/aitech) NELIESK. Secret'us NEliesk.

KONTEKSTAS: vartotojas patvirtino pridėti VISUS naujus šaltinius + TLDR Design filtruoti (tik AI/3D/dizaino-įrankių įrašai).
Dizaino tikslas = AI eksploatavimo metodai 3D/vizualizacijos/gen-media srityje, NE bendros dizaino naujienos.

1) BACKUP: cp /root/ai_digest.py /root/hera-core-backup/ai_digest.py.$(date +%s).
2) PATIKRINK KANDIDATUS (curl su browser User-Agent, timeout 15s; veikiantis = HTTP 200 IR turinys prasideda <?xml/<rss/<feed):
   - 80.lv:            https://80.lv/feed/   (jei ne — https://80.lv/rss/)
   - Figma tinklaraštis: https://www.figma.com/blog/feed/   (Figma gali neturėti RSS — jei ne, praleisk, pažymėk)
   - Two Minute Papers (YouTube kanalas): https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg
   - fal.ai:           https://fal.ai/blog/rss.xml   (jei ne — https://blog.fal.ai/rss/)
   - Replicate:        https://replicate.com/blog/rss   (jei ne — https://replicate.com/blog/rss.xml)
   - Hugging Face tinklaraštis: https://huggingface.co/blog/feed.xml   (jei JAU yra kitoj temoj — nedubliuok, pažymėk)
3) ĮDĖK į TOPICS['design']['feeds'] TIK veikiančius kandidatus. Šie visi = kuruoti (broad=False, be kw filtro — jie jau AI/3D/dizaino-tikslūs),
   IŠSKYRUS jei feed labai bendras. Two Minute Papers, 80.lv, fal.ai, Replicate, HF, Figma = kuruoti.
   Jei kuriam NĖ VIENAS URL neveikia — praleisk, pažymėk ataskaitoj (geriau mažiau, bet gyvi — kaip aitech).
4) TLDR DESIGN FILTRAS: dabartinis TLDR Design įrašas — perjunk į broad=True, kad jam būtų taikomas DESIGN_KW filtras
   (praeis tik įrašai su AI/3D/dizaino-įrankių raktažodžiais; emoji/telefonų gandai/rebrand'ai atkris). NELIESK DESIGN_KW sąrašo turinio,
   nebent reikia pridėti akivaizdų trūkstamą raktažodį (pvz. „ai", „generative" jei nėra). Pažymėk ką pakeitei.
5) PATIKRA: python3 -c "import ast; ast.parse(open('/root/ai_digest.py').read()); print('OK')".
   Testinis SAUSAS paleidimas TIK design temai (dry-run, be siuntimo jei toks rėžimas yra; jei ne — NEleisk viso digest) → parodyk kiek įrašų surinkta iš naujų šaltinių ir ar TLDR filtras veikia.
6) BACKUP kodą į /opt/hera-processor + commit/push.

ATASKAITA (HERA botas, trumpai): kiekvieno kandidato URL → HTTP kodas ir įdėta/praleista; galutinis design feeds skaičius; TLDR broad=True nustatyta;
ast OK; dry-run įrašų skaičius (jei įmanoma); backup. Jei STOP — kodėl+restore.

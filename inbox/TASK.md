UŽDUOTIS — Praplėsk paiešką/naujienas: CN/JP/KR labs + modeliai + TLDR. <14 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Viešo NELIESK. SAUGUMAS: raktų/asmeninių linkų necommit'ink.

KONTEKSTAS: Vartotojas nori praplėsti tyrimų/naujienų aprėptį — dabar praleidžia Azijos (CN/JP/KR) labs ir modelius.
Praplėsti (a) news digest (ai_digest.py → @tryspagaliabot) IR (b) HERA paiešką (hera_search/hera_research SearXNG
užklausas). DOMENAS NIEKADA NESIAURINAMAS — TIK PRIDEDAM (vartotojo direktyva). €0.

STRATEGIJA: sekti pagal LABS/ORGANIZACIJAS + „naujas modelis/release" pattern (ne tik tikslūs vardai — kad
pagautų naujus net nežinomais pavadinimais).

1) PRIDĖK šaltinius/užklausas (labs → modeliai):
   CN: DeepSeek · Alibaba/Qwen · Zhipu/GLM · Xiaomi/MiMo · Moonshot/Kimi · MiniMax · 01.AI/Yi · Tencent/Hunyuan ·
       Baidu/Ernie · ByteDance/Doubao · StepFun · **Nex AGI / Nex-N2-Pro** · Tsinghua · Peking University (PKU)
   JP: Sakana AI · RIKEN · Preferred Networks · rinna
   KR: Naver · KAIST · LG AI (Exaone) · Kakao
   Bendra: „new open-weight model release", „SOTA model", „technical report" pattern šioms lab'ams.

2) TLDR viešas feed (NE vartotojo asmeninis linkas): pridėk tldr.tech VIEŠĄ turinį kaip naujienų šaltinį —
   TLDR AI + TLDR DevOps archyvą/RSS (viešas, be jokio `em-tldr=` token'o). Necommit'ink jokio asmeninio linko.
   Jei viešo RSS nėra — naudok viešą archyvo puslapį; jei neprieinamas per proxy — pažymėk ir praleisk (fail-safe).

3) KUR taisyti: rask kur ai_digest.py laiko šaltinių/užklausų sąrašą IR kur hera_search/hera_research default
   queries — ten pridėk (ne perrašyk; expand only). Deterministinis, fail-safe (blogas šaltinis → praleidžia, ne crash).

4) TESTAS: paleisk digest/paiešką vieną kartą (arba dry) -> patvirtink kad naujos užklausos vykdomos be klaidų ir
   bent keli nauji šaltiniai grąžina rezultatų. Jei kuris šaltinis neveikia -> fail-safe skip + raportuok kuris.

5) Benchmark (jei liečia core) 9/9. DURABILUMAS: kodas -> hera-core-backup (be raktų/asmeninių linkų).
   ROADMAP/atmintis: „paieška praplėsta — CN/JP/KR labs + TLDR 2026-07-13".

TELEGRAM (per HERA botą, trumpai): (1) pridėti CN/JP/KR labs+modeliai (DeepSeek/Qwen/GLM/MiMo/Kimi/MiniMax/Yi/
Hunyuan/Ernie/Doubao/StepFun/Nex-N2-Pro + Sakana/RIKEN + Naver/KAIST/LG), (2) lab-based tracking (pagauna naujus
nežinomais vardais), (3) TLDR viešas feed pridėtas (asmeninis linkas NEnaudotas), (4) testas: naujos užklausos OK,
(5) „PAIEŠKA PRAPLĖSTA — Azija (CN/JP/KR) + TLDR aprėptyje, domenas nesiaurinamas".

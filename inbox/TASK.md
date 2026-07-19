UŽDUOTIS — ai_digest KOKYBĖ: išmesk triukšmą + pridėk santraukas/naudingumą + 7 flagship org. <14 min.
NEleisk pytest. Fail-safe. €0. Raktų nespausdink. Ataskaita TIK į HERA botą. Maršruto NEKEISK (@tryspagaliabot).
ANTI-RC124: Gemini/Telegram su HARD timeout (≤45s/call, ≤15s/žinutė), JOKIO begalinio retry.

KONTEKSTAS: pristatymo fix veikia (visi 11 ateina). BET 8 iš 11 = TRIUKŠMAS (community uploads/quant-mirrors/
fine-tunes iš GLOBALAUS „HF naujausi" šaltinio), ir NĖRA santraukų. Deep-research patvirtino: globalus createdAt =
triukšmas; poll BY ORG + filtruok derivatus. Kokybės fix, NELiesk pristatymo/seen logikos (jau gera).

1) IŠMESK TRIUKŠMO ŠALTINĮ:
   - Pašalink globalų „HF naujausi 8" (api/models?sort=createdAt&limit=8 BE author) — jis duoda šlamštą
     (bcckfdn/llama-resized-gguf, ppo-Huggy, *-probe, random fine-tunes). Palik TIK per-ORG polling (flagship labs).

2) TRIUKŠMO FILTRAS (deterministinis, be LLM) per-org rezultatams:
   - Praleisk akivaizdų šlamštą: repo id su `-gguf`/`-GGUF`, `-probe`, `ppo-`, `-awq`/`-int4`/`-int8`/`-fp8` quant-only
     mirrorus, `Huggy`, akivaizdžius re-upload/fine-tune patterns. Palik tik „tikrus" leidimus (base/instruct/chat/
     reasoning/flagship). Jei abejoji — palik (fail-open), bet globalaus šlamšto NEbus, nes per-org.

3) PRIDĖK 7 NAUJUS FLAGSHIP ORG (iš deep-research, confirmed live) į HF_ORGS:
   - CN: THUDM, OpenGVLab, inclusionAI, baichuan-inc, Skywork, rednote-hilab
   - JP: llm-jp
   (patikslink label|slug formatą kaip esamiems 17)

4) SANTRAUKOS + „KAS NAUDINGA" (per įrašą arba grupuotai — €0, budget-guard):
   - Kiekvienam įrašui: 1 eil. Gemini santrauka „kas tai" + „kodėl naudinga/kam" (trumpai). Gemini flash,
     thinkingBudget=0, HARD 45s, JOKIO retry. BATCH kad ribotum call'us (pvz. 1 Gemini call visiems įrašams iš karto,
     ne po vieną — mažina €/laiką). Jei Gemini timeout/lūžta → fallback: bare įrašas (pavadinimas+šaltinis+URL),
     NIEKADA nekelk rc≠0. Kategorijos žyma turi būti prasminga (ne „istorija" visiems — jei sugadinta, pataisyk).
   - Formatą: kiekvienas įrašas = **pavadinimas** · šaltinis · 1-eil santrauka „kas/kodėl" · URL. Rikiuota pagal šviežumą.

5) VERIFIKACIJA: dry-run (parodyk kaip atrodys 1-2 įrašai su santrauka+filtru) + VIENAS test-send į @tryspagaliabot
   nauju formatu (pažymėk „🧪 TESTAS v2 — filtruota+santraukos"). seen NEkeisk dėl testo.

6) BACKUP: commit ai_digest.py → hera-core-backup. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0. Maršrutas nekeičiamas. Jokio pytest-all. Anti-rc124 (HARD timeout Gemini+Telegram). NElisk pristatymo-
skaidymo/seen logikos (ką ką tik pataisėm). Interconnects-CSV auto-seed + dedup-normalizavimas = ATIDĖTA (kita banga).

ATASKAITA (HERA botas, trumpai): (a) globalus triukšmo šaltinis išmestas? (b) filtras (kokie patternai)? (c) 7 org
pridėti? (d) santraukos+naudingumas veikia (batch Gemini, fallback)? (e) test-send v2 OK (kiek įrašų, ar švaru/su
santraukom)? (f) backup push OK/ne; (g) 1 eil. kas toliau.

UŽDUOTIS — FAZĖ 12: (A) parse↔šaltinis faithfulness-vartas (gebėjimas) + (B) Copycat nata su moksline korekcija. <14 min.
NEleisk pytest pilnai (tik naujo modulio smoke/benchmark). Telegram TRUMPAI į HERA botą. Fail-safe. €0. Raktų nespausdink.
Ataskaita TIK į HERA botą (HERA_BOT_TOKEN). Privatūs repo (hera-core-backup + hera-vault). Viešo cad-site-agent NELIESK.

KONTEKSTAS (kodėl): vartotojas nori dviejų dalykų. (A) DAUGKARTINIS gebėjimas — kai HERA parsina turinį, patikrinti ar
parse'as ištikimas ŠALTINIUI (nepridėjo išgalvotų faktų). Deterministinis, be LLM, nemokamas. (B) VIENKARTINIS —
įrašyti konkrečią Copycat/Hofstadter/Mitchell natą su moksline korekcija (sena knyga 1984, mokslas pajudėjo).

=== DALIS A: hera_faithfulness.py (deterministinis grounding-vartas) ===

1) `/opt/hera-processor/hera_faithfulness.py`:
   - `check(parsed, source_text) -> {grounded:[...], ungrounded:[...], score:float(0-1), verdict:'ok'|'suspect'}`.
   - Iš parsed ištrauk PATIKRINAMUS atomus (NE parafrazę): tikriniai vardai/terminai (proper nouns), citatos
     (kabutėse), skaičiai/datos. Parafrazė teisėta — netikrink sakinių, tik faktinius atomus.
   - Matchink prieš NORMALIZUOTĄ source_text (case-insensitive, whitespace-normalized; leidžiama nedidelė fuzzy
     variacija). Atomas kurio NĖRA šaltinyje → 'ungrounded' (galima haliucinacija). score = grounded/(grounded+ungrounded).
   - ADVISORY (ne hard blokas — parse legitimiai perfrazuoja): ungrounded virš slenksčio → pažymėk žmogui prie gate.
   - HERA_FAITHFULNESS flag (default 0). Kai 0 — modulis tik importuojasi, pipeline nepaliestas. Integruok į ingest
     PRIEŠ vault rašymą kaip advisory pakopą (kai flag=1).
   - Fail-safe: klaida/timeout → verdict='inconclusive', NEblokuok, NIEKADA rc≠0. Be LLM, be tinklo, be lokalių modelių.

2) BENCHMARK (deterministinis, be tinklo, 100%): hera_faithfulness_bench su fixtures — mažas source tekstas + 2 parse:
   (i) „švarus" (visi atomai iš šaltinio) → verdict ok, score≈1; (ii) su ĮTERPTU išgalvotu faktu (vardas/skaičius kurio
   nėra) → tas atomas 'ungrounded', verdict suspect. Patikrink ir tuščią/be-atomų atvejį. Įrašyk X/Y. <100% → NEjunk flag.

=== DALIS B: Copycat nata į vault (deterministiškai, be LLM, be tinklo) ===

3) Įrašyk į hera-vault `growth/` naują natą (STATUS: staged, human-gate; kind: idea/technique; specialist: n/a):
   „Copycat / analogijų kūrimas — Hofstadter & Mitchell (su 2026 moksliniu patikslinimu)". Turinys:
   - ESMĖ (iš vartotojo parse'o): analogija=intelekto šerdis; konceptualus slydimas (rightmost→leftmost, raidė→grupė);
     parallel terraced scan; Copycat letter-string mikropasaulis (abc→abd: ijk→ijl, xyz→wyz); FARG decentralizuoti
     mechanizmai; Minsky/Moravec „easy things are hard".
   - MOKSLINIS PATIKSLINIMAS 2026 (žymėk aiškiai — šaltinis senas, mokslas pajudėjo):
     • DAR GALIOJA: analogija mašinoms vis dar sunki (Gendron et al. 2023, arXiv 2305.19555 „LLMs Are Not Strong
       Abstract Reasoners"); „easy things are hard" laikosi; parallel terraced scan = modernus test-time compute /
       inference-time search (Franzen et al. 2025, arXiv 2505.07859).
     • PASENĘ: grynas symbolic FARG (Copycat/Metacat/Letter Spirit) daugiausia istorija → deep learning + neuro-symbolic;
       embedding-analogijos (king−man+woman≈queen) trapios, siauros.
     • MODERNUS PRIDEDA (GINČAS, NĖRA konsensuso): Webb/Holyoak/Lu 2022 (arXiv 2212.09196) PRO „emergent analogical
       reasoning"; Hodel & West 2023 (arXiv 2308.16118) CONTRA — GPT-3 lūžta ant letter-string analogijų (Copycat
       domenas!), įtaria įsiminimą; Wu et al. 2023 (arXiv 2307.02477) counterfactual užduotys → smukimas. Mitchell'io
       skepticizmas iš esmės laikosi. ARC-AGI (Chollet) = modernus Copycat-tipo benchmarkas; ARC-AGI-2 2025 (arXiv
       2505.11831); survey 2026 (arXiv 2603.13372): kompozicinis generalizavimas neišspręstas, program-synthesis+
       test-time lenkia gryną LLM.
   - provenance: „parse iš vartotojo + mokslinis patikslinimas (paper-search, ne pilnas adversarinis ratas)".
     source_refs: user-parse (Copycat chapter). Wiki-link auto (hera_wikilink). NEsiųsk į išorę.

=== BENDROS RIBOS ===
€0. Jokių lokalių/GPU modelių. Jokio tinklo B daliai (citatos jau duotos — NEfetch'ink arXiv). Jokio pytest-all.
NEperrašinėk hera_eval/hera_council/hera_selfedit — tik importuok/integruok. Anti-rc124: viskas deterministiška, be
model-call. Backup: commit hera-core-backup (kodas) + hera-vault (nata). Push nepavyko → NEkartok begalos, pranešk.

ATASKAITA (HERA botas, trumpai): (a) hera_faithfulness.py sukurtas + integruotas (advisory)? (b) benchmark X/Y;
(c) HERA_FAITHFULNESS į/išjungtas? (d) Copycat nata įrašyta į vault (kelias)? (e) wiki OK? (f) backup push OK/ne;
(g) 1 eil. kas toliau.

UŽDUOTIS — B: pridėti 3-ią digest lauką „Kur jau panaudota" į enrichment (ai_digest.py) + greitas thinkingBudget=0 auditas. <14 min.
Fail-safe: jei abejoji STOP+backup restore. NEleisk pytest. €0 (1-2 maži Gemini call'ai). Ataskaita TIK į HERA botą. Secret'us NEliesk.

KONTEKSTAS: 400 fix atliktas — enrichment vėl veikia (kas/kur). Dabar pridedam 3-ią lauką VISOMS 4 temoms: „Kur jau panaudota"
(kur tai JAU realiai taikoma). Bendras kodas — vienas pakeitimas taiko visoms temoms.

ŽINGSNIAI:
0) GREITAS AUDITAS (read-only): `grep -rn "thinkingBudget" /root/ /opt/cad-site-agent/n8n/hera/ 2>/dev/null | grep -v hera-core-backup`.
   Jei rasta „thinkingBudget": 0 (ar =0) KITUR nei jau pataisytas ai_digest.py — PAŽYMĖK ataskaitoj (NEtaisyk čia, atskiras darbas), nes ta pati
   Gemini deprecation gali tyliai laužyti tuos call'us. Jei niekur kitur — pažymėk „švaru".
1) BACKUP: cp /root/ai_digest.py /root/hera-core-backup/ai_digest.py.$(date +%s).
2) MODIFIKUOK ai_digest.py (bendras enrichment kelias, visos 4 temos):
   - _summarize_batch(): dabar grąžina {i:(cat,kas,kur)}. Praplėsk į 3 usage laukus: pridėk „jau" (kur jau panaudota).
     Atnaujink JSON prompt/schema kad Gemini grąžintų kas + kur + jau. Prompt'e ĮDĖK EPISTEMINĘ ATSARGĄ (LT):
     „Kur jau panaudota: nurodyk realias taikymo sritis ar pavyzdžius kur tai JAU naudojama. NEIŠGALVOK konkrečių įmonių,
     produktų ar deployment'ų — jei tikslių pavyzdžių nežinai, nurodyk bendrą realią taikymo sritį. Jokių fabrikuotų faktų."
   - build_messages(): kur dedama „Kas tai:"/„Kur panaudoti:", pridėk „Kur jau panaudota:" eilutę (tik jei laukas netuščias).
   - Išlaikyk esamą fallback (jei enrichment fail — bare, be crash). Neliesk feeds/temų sąrašų.
3) PATIKRA: `python3 -c "import ast; ast.parse(open('/root/ai_digest.py').read()); print('OK')"`.
   RE-TEST: paleisk realų _summarize_batch() su 2 sintetiniais įrašais → turi grąžinti 3 laukus (kas/kur/jau) LT, 200. Parodyk pvz output.
   (NEleisk viso digest — tik vienas batch test.)
4) BACKUP kodą: cp /root/ai_digest.py /opt/hera-processor/ (jei ten laikai) + commit/push jei taikoma.

ATASKAITA (HERA botas, trumpai): (0) thinkingBudget=0 auditas (rasta kitur? kur / švaru); (2) 3-ias laukas pridėtas OK; (3) ast OK + re-test
pvz su 3 laukais (kas/kur/jau); backup kelias. Jei STOP — kodėl + restore. NEDĖK naujų feeds ir NEDARYK TLDR filtro — tai atskiri žingsniai.

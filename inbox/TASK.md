UŽDUOTIS — diagnozuoti + pataisyti Gemini enrichment HTTP 400 ai_digest.py (_summarize_batch) — liečia VISAS 4 temas. <15 min.
Fail-safe: jei fix neaiškus — TIK diagnozė + STOP, nekeisk. NEleisk pytest. €0 (Gemini free tier, 1-2 maži call'ai). Ataskaita TIK į HERA botą. Secret'us NEliesk/redaguok.

KONTEKSTAS: recon nustatė — _summarize_batch() (ai_digest.py ~610-679) meta HTTP 400 Bad Request VISOMS 4 temoms ~3 dienas →
tylus bare-fallback → digest įrašai be „Kas tai/Kur panaudoti". Model=gemini-flash-latest, generationConfig su responseMimeType=json +
thinkingConfig(thinkingBudget=0). `str(e)` rodo tik „HTTP Error 400: Bad Request" be kūno — reikia TIKRO klaidos teksto.

ŽINGSNIAI:
1) BACKUP: cp /root/ai_digest.py /root/hera-core-backup/ai_digest.py.$(date +%s).
2) DIAGNOZĖ — gauk TIKRĄ 400 kūną: parašyk /tmp/probe.py kuris atkartoja TIKSLIAI tą patį _summarize_batch request'ą (tas pats
   model, generationConfig, 2 sintetiniai įrašai), naudoja Gemini raktą iš to paties env kaip ai_digest.py, ir SPAUSDINA HTTP status +
   PILNĄ response body (per e.read().decode() jei HTTPError). Paleisk. Užrašyk TIKRĄ klaidos tekstą ataskaitoj.
3) DIAGNOZUOK priežastį iš tikro kūno. Tikėtini kaltininkai: (a) model „gemini-flash-latest" nebevalidus/pervadinta (bet tada 404, ne 400);
   (b) generationConfig — responseMimeType + thinkingConfig kombinacija ar thinkingBudget=0 nebepriimamas; (c) responseSchema formatas;
   (d) laikinas kvotos/API triukšmas (tada retry vėliau, ne kodo fix).
4) FIX (tik jei AIŠKUS ir mažas): pataisyk _summarize_batch (pvz. pašalink/pakeisk problemišką generationConfig lauką, ar model'į į
   valid gemini flash ID kurį patvirtini veikiantį probe'u). Backup jau padarytas. `python3 -c "import ast; ast.parse(open('/root/ai_digest.py').read())"`.
   RE-TEST: paleisk probe/vieną enrichment call PO fix → turi grąžinti validų JSON su kas/kur (200, ne 400). NEleisk viso digest.
   Jei fix NEaiškus (pvz. kvotos triukšmas ar dviprasmiška) → NEkeisk, tik reportuok tikrą kūną + hipotezę, STOP.
5) NEDĖK dar 3-io lauko (Kur jau panaudota) ir NEliesk feeds — tai atskiras kitas žingsnis. TIK 400 fix.

ATASKAITA (HERA botas, trumpai): TIKRAS 400 response body; diagnozuota priežastis; ar fix pritaikytas (before/after eilutė) ar STOP;
re-test rezultatas (enrichment grąžina kas/kur? 200?); backup kelias. Jei STOP — kodėl + hipotezė kitam žingsniui.

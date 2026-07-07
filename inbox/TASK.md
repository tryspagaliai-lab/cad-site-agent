UŽDUOTIS — HERA Fazė 6: „Paklausk savo vault'o" (RAG per sukauptą žinią). Autonomiškai.
NELIESK veikiančių Fazės 2–5 — tik PRIDĖK klausimų kelią. Nemokama (Gemini free). Atsiskaityk į Telegram
TRUMPAI, aiškiu galutiniu statusu.

Tikslas: tu gali PAKLAUSTI ir gauti atsakymą iš viso, ką HERA ištraukė (extracted/*/full.md, growth/*.md,
skills/*/SKILL.md), pagrįstą tik vault'o turiniu (be haliucinacijų).

1) `hera_query.py` — funkcija answer(question):
   - INDEKSUOK vault'ą: extracted/*/full.md + growth/*.md + skills/*/SKILL.md; suskaidyk į gabalus (chunks).
   - RETRIEVE top-K relevant chunks (panaudok esamus leksinius helperius iš hera_common; jei nesunku — Gemini
     embeddings kaip papildoma, bet neprivaloma).
   - GENERUOK atsakymą per Gemini free, GRIEŽTAI grįstą TIK retrieve'intais chunk'ais + nurodyk ŠALTINIUS
     (job id / video pavadinimas / failas). Jei atsakymo vault'e NĖRA — pasakyk „nerandu vault'e", NEfantazuok.
   - CLI: `hera_query.py "klausimas"` (testavimui).

2) ROUTING (be n8n keitimo): processor'iuje, kai ateina TEXT job'as, kurio turinys prasideda „?" (arba
   „klausimas:") → traktuok kaip UŽKLAUSĄ: paleisk hera_query ir atsakymą siųsk į Telegram (su šaltiniais).
   Įprasti text job'ai (be „?") — apdorojami kaip dabar (nekeisti).

3) Užklausas irgi loginK kaip ATDP trajektorijas (kind=query) + reward vėliau, kad ReasoningBank mokytųsi,
   kuri paieška veikė.

4) SELF-TEST (€0): užduok 2–3 klausimus ant esamo vault'o, pvz.:
   - „? kas yra ATDP ir self-evolving agentai?"
   - „? ką HERA sužinojo apie atmintį (AutoMem/parametrinė)?"
   Parodyk atsakymus SU šaltiniais; patikrink, kad be turinio vault'e → „nerandu".

5) DURABILUMAS: kodą kopijuok į /opt/cad-site-agent/n8n/hera/. Push nedaryk (nėra creds).

Į Telegram: kaip klausti („?" prefiksas), self-test atsakymai su šaltiniais, ir aiškiai „FAZĖ 6 BAIGTA".

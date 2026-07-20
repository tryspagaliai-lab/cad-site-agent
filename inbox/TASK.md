UŽDUOTIS — (A) PROMOTE „RAG prieštaringi dokumentai" (gfc7mj) + (B) DANGLING šakninis taisymas (71 ir auga). <14 min.
NEleisk pytest. Fail-safe. €0. Raktų nespausdink. Deterministiška (be LLM/tinklo). Ataskaita TIK į HERA botą.
Privatus hera-vault (+ hera-core-backup jei B keičia kodą). Viešo cad-site-agent NELIESK.

=== A) PROMOTE gfc7mj (human-gate: vartotojas patvirtino; taryba promote_candidate 12) ===
1) growth/2026-07-20-20260720T105330Z-gfc7mj.md antraštėje: „STATUS: PROMOTED 2026-07-20 (human-gate: vartotojas)".
2) „Kuravimo pastaba (forward-strengthening)":
   - „Validuoja HERA praktikas: (1) supersedence/prune srautas (Loop C) = 'pasenusi taisyklė negali gyventi šalia
     naujos'; (2) epistemic flags praktika = 'AI ≤ Duomenys' (nuomonė ≠ faktas, keli atsakymai → rodyti visus su
     kontekstu); (3) faithfulness vartų filosofija = 'dažnai ne haliucinacija, o blogai suprojektuota sistema'."
   - „PERIMTINOS IDĖJOS (kandidatai, €0 determ.): (a) SUPERSEDENCE ŽYMA retrieval'e — kai Memora grąžina natą,
     kurią naujesnė pakeičia/prieštarauja, pažymėti, ne tyliai servuoti abu; (b) CLARIFICATION LOOP — per bendra
     užklausa → prašyti patikslinti, ne spėlioti (ateities retrieval sąsajai)."
   - „Šaltinis: YouTube, be marketingo. Faithfulness ~0.7 (tikėtina vertimo triukšmas)."
3) Wiki + trajektorija: hera_wikilink pass; curation/human-gate-promote.

=== B) DANGLING ŠAKNINIS TAISYMAS — 12→59→71, Loop B NEsivalo kaip žadėta ===
4) DIAGNOZĖ: kur tie 71 dangling? (loopC prune report sakė „40 = index/concepts.md nuorodos į prunintus id, savaime
   pasitaisys per Loop B concepts.md regeneravimą" — NEPASITAISĖ ir auga po kiekvieno prune.) Nustatyk:
   - Ar Loop B concepts.md regeneravimas iš viso šalina nuorodas į nebeegzistuojančius failus? (Tikėtina — NE:
     regeneruoja turinį, bet palieka senas [[nuorodas]] arba dangling'ai gyvena kituose index/analysis failuose.)
   - Išvardink TOP failus pagal dangling kiekį (concepts.md? analysis/*? senos growth natos?).
5) FIX (deterministinis):
   - Index/concepts/analysis failuose: nuorodas į nebeegzistuojančius failus PAŠALINK arba pakeisk į paskirties
     skill'ą (jei prune žinutėje „perkelta į skill X" — nukreipk į [[X]]). Growth/skills TURINIO natose nuorodų
     neperrašinėk agresyviai — tik jei nuoroda į prunintą failą, pakeisk į paskirties skill'ą.
   - ŠAKNIS: pataisyk Loop B/concepts regeneravimą (arba hera_wikilink/lint pass'ą), kad po prune AUTOMATIŠKAI
     valytų/nukreiptų nuorodas į nebeegzistuojančius taikinius (deterministinis žingsnis, be LLM). Kad kitą kartą
     dangling nebeaugtų. Jei kodo keitimas — commit į hera-core-backup, bench'ai (hera_lint) turi likti žali.
6) VERIFIKACIJA: hera_lint PO — parodyk orphan/dangling skaičius (tikslas: dangling ~0-5, ne 71). Jei kai kurių
   negalima išvalyti saugiai — pasakyk kiek liko ir kodėl.

7) BACKUP: vault + (jei kodas) hera-core-backup push. Nepavyko → NEkartok begalos, pranešk.

ATASKAITA (HERA botas, trumpai): (a) gfc7mj PROMOTED + pastabos; (b) dangling diagnozė (kur gyveno, kodėl Loop B
nevalė); (c) fix: dangling PRIEŠ 71 → PO N; šaknis pataisyta (auto-valymas po prune)? (d) push OK/ne; (e) 1 eil. toliau.

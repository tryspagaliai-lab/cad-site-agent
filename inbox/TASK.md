UŽDUOTIS — PATAISYTI 2 GROWTH NATAS (tandem fact-check korekcijos). <8 min.
NEleisk pytest. Telegram TRUMPAI į HERA botą. Fail-safe. €0. Raktų nespausdink. Deterministiška
(JOKIŲ LLM/tinklo — pataisos duotos verbatim). Ataskaita TIK į HERA botą. Privatus hera-vault.
Viešo cad-site-agent NELIESK.

KONTEKSTAS: web sesija paleido tandeminę verifikaciją (2 nepriklausomi tikrintojai prieš pirminius
šaltinius — repo kodą ir README) ankstesnės užduoties natoms `headroom` ir `herdr` (2026-07-18).
Rasta 1 klaida + 2 patikslinimai. Jei ankstesnė užduotis dar neįvykdyta ir natų nėra — pažymėk
ataskaitoje „natų nėra, pataisos netaikytos" ir baik (fail-safe, NEkurk natų iš naujo).

A) Natoje `herdr` (2026-07-18-*herdr*):
   1. PAKEISK „vienas Rust binary ~10MB" → „vienas Rust binary (release ~15–18 MB; „~10MB" buvo
      klaidingas antrinis šaltinis — pirminiuose jo nėra)".
   2. PAKEISK „Linux/macOS" → „Linux/macOS stabilu, Windows preview beta".
   3. PAKEISK „be telemetrijos/tinklo" → „be telemetrijos, be hosted control plane; remote — per
      paprastą SSH".
   4. PRIDĖK eilutę: „Socket API patvirtintas iš docs šaltinio: pane.split/pane.run/pane.read +
      `herdr wait agent-status --status done|blocked` (semantinės būsenos)."

B) Natoje `headroom` (2026-07-18-*headroom*):
   1. PAKEISK „~20% coding-agentams" → „15–20% coding-agentams".
   2. CodeCompressor kalbų sąrašą papildyk: „Py/JS/TS/Go/Rust/Java/C/C++/Perl".
   3. PAKEISK ML apimties sakinį į: „SmartCrusher (JSON) ir CodeCompressor (AST) deterministiškumas
      patvirtintas iš ŠALTINIO KODO (Rust backend / tree-sitter, be modelio) — README žodžio
      „deterministic" nevartoja. ML naudojamas NE tik prozai: Kompress-v2-base (proza, ONNX/PyTorch),
      Magika turinio aptikimas, embedding-relevance ir vaizdų ML-router — visi ONNX keliai.
      IŠVADA HERA'ai: „deterministinis-only" režimas privalo išjungti VISUS ML kelius (proza+Magika+
      embedding+image), ne vien prozos kompresorių; AVX2 fallback (BM25/heuristika) tai leidžia."
   4. Žymą apie blogus palik kaip yra.

C) Abiejose natose PRIDĖK apačioje: „Tandem-verifikuota 2026-07-18: 2 nepriklausomi tikrintojai,
   pirminiai šaltiniai (repo kodas+README); 1 klaida rasta ir pataisyta (herdr dydis)."

D) hera_wikilink + hera_lint pass. Commit + push hera-vault. Push nepavyko → NEkartok begalos, pranešk.

RIBOS: €0, be LLM/tinklo, be pytest, viešo NELIESK, nieko netrink — tik šios redakcijos 2 natose.

ATASKAITA (HERA botas, trumpai): (a) abi natos pataisytos / natų nebuvo? (b) vault push OK/ne.

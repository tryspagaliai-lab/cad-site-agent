UŽDUOTIS — NAPMEM FAZĖ B: L4 VARTOTOJO/SISTEMOS PROFILIS (VIENA SIAURA UŽDUOTIS). <10 min.
NEleisk pytest — tik taikinius testus. LLM kvietimams — griežti timeout'ai (60s + 1 retry, kaip nav kilpoje).
Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: NapMem piramidės viršūnė — L4 profilis (nekintančios tiesos apie vartotoją/sistemą), kurio HERA
dar neturi. Vartotojas diegimą patvirtino (visa NapMem serija).

1) PROFILIO GENERAVIMAS: naujas žingsnis (pvz. hera_profile.py) — iš growth/ + skills/ frontmatter'ių + Loop B
   klasterių sintezuok /opt/hera-vault/profile/PROFILE.md: (a) vartotojo domenai/interesai (pvz. agentų atmintis,
   save-tobulinančios sistemos, CAD verslas, AI įrankiai), (b) preferencijos (lietuvių kalba, €0 stack,
   human-gate governance), (c) sistemos faktai (kas HERA yra, kokie komponentai). KIEKVIENAM teiginiui —
   provenance nuoroda į šaltinio failą(-us). Trumpas (<80 eilučių), tik išliekančios tiesos, ne naujienos.
2) ATNAUJINIMAS: prijunk prie Loop C (savaitinė konsolidacija) — profilis regeneruojamas; plius rankinis
   paleidimas dabar (pirmas PROFILE.md turi atsirasti šioje užduotyje).
3) NAV KILPA: pridėk įrankį read_profile (L4) į naršymo kilpos įrankius — pigiausias pirmas žingsnis
   klausimams apie preferencijas/kontekstą („koks mano domenas?", „kokia kalba atsakinėti?").
4) TESTAS: (a) PROFILE.md sugeneruotas, turi provenance nuorodas; (b) klausimas per kilpą „kokie mano
   pagrindiniai interesai?" -> veiksmų sekoje matosi read_profile, atsakymas iš profilio; (c) regresija:
   „kas yra ATDP?" tebeveikia kaip anksčiau.
5) DURABILUMAS: kodo kopija į /opt/cad-site-agent/n8n/hera/ + push į hera-core-backup (askpass metodas,
   secret-scan). Vault'e PROFILE.md nusisync'ins pats per cron.

TELEGRAM (trumpai, be raktų): (1) PROFILE.md sukurtas, kiek teiginių/provenance, (2) read_profile kilpoje
veikia — testo seka, (3) regresija OK, (4) backup push OK, (5) „NAPMEM-B BAIGTA".

UŽDUOTIS — Įjunk HERA_MEMORA=1 GYVAI. <6 min. NEleisk pytest. Telegram TRUMPAI. Fail-safe €0.
Kodas/config -> PRIVATUS hera-core-backup. Viešo NELIESK. Necommit'ink raktų (ypač hera.env — raktų NEspausdink).

KONTEKSTAS: Vartotojas patvirtino — įjungti Memora gyvai. Grandinė (9a index + 9b retriever) pastatyta, bet už
HERA_MEMORA=0. Įjungiam kad indeksas augtų + paieška veiktų realiai. €0 (Gemini free).

1) Nustatyk HERA_MEMORA=1 gyvoje aplinkoje (hera.env arba kur laikomi HERA_* jungikliai). Necommit'ink .env su
   raktais — tik pakeisk reikšmę.
2) Perkrauk hera-processor.service; patikrink kad HERA_MEMORA=1 įsikrauna (active) IR kad ankstesni jungikliai
   (HERA_GPUFILTER=1, HERA_JOURNAL, HERA_SELFEDIT, HERA_GATE ir kt.) NEsugadinti — parodyk jų būseną.
3) SANITY: kito atminties įrašo metu (arba rankiniu index_memory ant 1 įrašo) patvirtink kad memory_index.jsonl
   auga gyvai (index_memory tikrai kviečiamas). Fail-safe: jei kas nors klysta -> grąžink HERA_MEMORA=0 (rollback)
   ir pranešk, NEpalik sistemos sugadintos.
4) Benchmark: hera_bench.run() -> 9/9 (jungiklis neturi gadinti).
5) DURABILUMAS: config pakeitimas dokumentuotas -> hera-core-backup (BE raktų). ROADMAP pastaba „HERA_MEMORA
   ĮJUNGTA GYVAI 2026-07-13". Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) HERA_MEMORA=1 GYVAI (Memora index+retriever aktyvūs), (2) kiti jungikliai
nesugadinti, (3) sanity: memory_index.jsonl auga gyvai, (4) benchmark 9/9, (5) „MEMORA ĮJUNGTA — atmintis dabar
indeksuojasi ir ieško multi-hop gyvai (€0)".

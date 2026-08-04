# Fazė 50 — Loop C prune vykdymas su verdikto perkėlimu + Fazės 49 likimo diagnostika. HUMAN-GATE GAUTAS („Daryk kaip siūlai"). <14 min.

## Tikslas

1. **Diagnostika (pirmiausia, trumpai, read-only):** Fazė 49 buvo dispatch'inta 2026-08-02 16:56 UTC ir per
   ~46 val. NEATĖJO jokia ataskaita, nors visi kiti cron'ai (vault sync, ingest, Loop B/C) veikia. Nustatyk,
   kas įvyko: ar runner'is ją paleido (runner log / STATE dedup / flock liekanos)? Jei paleido — kodėl
   ataskaita neišėjo? Jei nepaleido — kodėl? Išvada su įrodymais į ataskaitą. Pačios Fazės 49 turinio ČIA
   nevykdyk — jos audito pusė jau atsakyta iš šalies (schema `atdp-lite-1` chain lauko neturi; užfiksuota
   vault'e), o grandinės jungties pusė grįš kaip atskira fazė.

2. **Loop C 6 staged prune įvykdymas TEISINGA tvarka:**
   a. **PIRMA** — perkelk žmogaus kuravimo verdiktą iš `growth/2026-07-29-20260729T200400Z-eouamt.md` į
      `skills/mdlm-care-evaluation-protocol/SKILL.md`. Verdikto blokas = turinys, pridėtas prie pastabos PO
      skill'o sukūrimo (žr. įrodymus). Integruok į skill struktūrą prasmingai, ne aklai append'ink.
   b. **TADA** — visas 6 pastabas perkelk į `archive/growth-pruned-2026-08-04/`.
      **ARCHYVUOJAM, NETRINAM** — jokių `rm`; `git mv` su commit'u. Precedentas: `archive/growth-superseded-2026-07-27/`.
   c. **GALIAUSIAI** — pataisyk Loop C logiką: pastaba, kurios TURINYS keitėsi po skill'o sukūrimo, negali
      būti automatiškai staged prune (ji gali nešti turinį, kurio skill'e nėra). Palyginimas — git turinio
      diff'as prieš skill'o sukūrimo commit'ą, **NE mtime** (mtime užterštas paties Loop C žymėjimo).

## Realybė (jau patikrinta iš šalies — nekartok, naudok)

- 6 staged pastabos `growth/`: `2026-07-27-...48qu1o.md` · `2026-07-27-...z69xn1.md` · `2026-07-29-...eouamt.md` ·
  `2026-07-31-...f9rkr7.md` · `2026-07-31-...zgzpsx.md` · `2026-07-31-...p2ompa.md`.
- `git diff --numstat <skill-sukūrimo-commit> HEAD -- <pastaba>`: **penkios** rodo lygiai +6 eilutes
  (uniformu = Loop C staging žymė, saugu archyvuoti), **`eouamt` rodo +23** — žmogaus CaRE verdikto blokas.
- `skills/mdlm-care-evaluation-protocol/SKILL.md` verdikto turinio NETURI: nėra „GPU", nėra „PER UŽKLAUSĄ",
  nėra „APSIVERT". Tai sėkmės kriterijaus pagrindas.
- Ta pati Loop C akloji zona kartojasi jau TREČIĄ kartą — todėl c) yra taisyklės fix, ne vienkartinis lopymas.

## Apribojimai (nekintami)

- €0 · fail-safe (klaida → no-op) · BACKUP prieš kiekvieną kodo keitimą (push į privatų `hera-core-backup`) ·
  HARD laiko biudžetas — jei nespėji, geriau a)+b) pilnai, o c) palik aiškiai aprašytą kaip kitą fazę,
  nei visus tris puse.
- Viešo `cad-site-agent` repo git'o neliesti; vault keitimai — į `hera-vault`.
- Loop C pakeitimui — savas `--selftest` (be pytest): dry-run, kur pastaba su po-skill turinio pokyčiu
  NEPATENKA į staged sąrašą, o nepakitusi — patenka.

## Sėkmės kriterijai (selftest)

1. `skills/mdlm-care-evaluation-protocol/SKILL.md` po perkėlimo TURI verdikto esmę (grep prieš/po:
   atsiranda GPU kontekstas ir compute-matched vertinimo išvada).
2. `growth/` nebeturi nė vienos iš 6 pastabų; `archive/growth-pruned-2026-08-04/` turi visas 6;
   git istorijoje matomas PERKĖLIMAS, ne trynimas.
3. Loop C selftest: modifikuota-po-skill pastaba atmetama iš staging, nepakitusi — ne. Backup prieš keitimą.
4. Fazės 49 diagnostikos išvada su įrodymais (log eilutės / STATE įrašai), ne spėjimu.

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**
Negalimybė turi būti pagrįsta veiksmais, ne intuicija. Neapsimesk, kad patikrinai, jei tik pažiūrėjai.

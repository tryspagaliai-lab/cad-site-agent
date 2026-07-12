UŽDUOTIS — (A) promote SkillOpt + (B) FAZĖ 5d: rejected-edit buffer. <16 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Vault -> PRIVATUS hera-vault. Viešo repo NELIESK.
SAUGUMAS: raktų nespausdink/necommit'ink.

=== DALIS A — PROMOTE SkillOpt (human-gate) ===
Vartotojas patvirtino. Rask growth failą „SkillOpt" (growth/2026-07-12-*lto8bb* arba pagal pavadinimą).
- Pažymėk „STATUS: PROMOTED 2026-07-12 (human-gate: vartotojas)".
- Pridėk pastabą: „Validuoja HERA architektūrą (skill=apmokamas parametras, bounded edits, validation gate,
  rejected-edit buffer, jokio svorių keitimo). Imam PATTERNUS, NE visą karkasą (pilnas SkillOpt = daug rollout'ų/
  eval = brangu, kertasi su €0). Kodas: github.com/microsoft/SkillOpt (studijuoti, nemigruoti)."
- Wiki-link + trajektorija (curation/human-gate-promote/growth).

=== DALIS B — FAZĖ 5d: rejected-edit buffer (iš SkillOpt) ===
KONTEKSTAS: SkillOpt laiko atmestus pakeitimus kaip NEGATYVŲ feedback'ą kitiems pasiūlymams, kad nekartotų klaidų.
Mūsų selfedit/accretion atmeta ir pamiršta. Pridėk buffer'į — TIK praturtina pasiūlymo generavimą, NIEKO
NEsilpnina: whitelist/tripwire/benchmark-gate/human-gate LIEKA nepakeisti; priėmimo kriterijai NEsikeičia.

TAI TIESIOGINIS kodo pakeitimas per runner (NE per selfedit patį — jo blacklist negalioja runner'iui). Į
hera_core-backup.

1) STORAGE: buffer failas (pvz. /opt/hera-vault/state/rejected_edits.jsonl) — append {ts, target, goal, reason,
   short_snippet}. Bounded: laikyk paskutinius ~20 (arba per-target ~5). Fail-safe: I/O klaida -> no-op.
2) RECORD ON REJECT: hera_selfedit.py (ir hera_accretion.py jei tinka) — kai pasiūlymas ATMETAMAS (tripwire ARBA
   benchmark-gate ARBA whitelist), įrašyk į buffer'į su priežastimi. NEkeisk atmetimo logikos — tik pridedi record.
3) INJECT ON PROPOSE: propose_edit (ir accretion) draft LLM iškvietime pridėk paskutinius ~5 rejected (tas pats
   target'as prioritetu) kaip NEGATYVŲ kontekstą: „VENK šių anksčiau atmestų pakeitimų ir kodėl: ...". Bounded +
   truncated (kad neišpūstų prompt'o). Jei buffer tuščias/klaida -> praleisk (fail-safe).
4) SAUGIKLIAI (privaloma, nekeisti): buffer TIK informuoja generavimą; priėmimas VIS TIEK reikalauja praeiti
   tripwire + benchmark(>=9/9) + human-gate. Jokio auto-merge. HERA_SELFEDIT jungiklis galioja. €0, HARD timeout
   nepakeistas (45-60s no-retry).
5) DEMO (įrodyk kilpą): sukelk 1 ATMETIMĄ (pvz. propose_edit su goal kuris bandytų pašalinti assertion -> tripwire
   REJECT) -> parodyk kad įrašyta į buffer'į. Tada dar vienas propose_edit tam pačiam target'ui -> parodyk log kad
   rejected buvo INJECT'intas kaip negatyvus kontekstas. Gyvas failas NEPAKEISTAS, benchmark 9/9.
6) ROADMAP: docs/ROADMAP.md pridėk „Fazė 5d — rejected-edit buffer ĮDIEGTA 2026-07-12 (iš SkillOpt; negatyvus
   feedback pasiūlymams; gates nepakeisti; €0)."
7) DURABILUMAS: kodas -> hera-core-backup (privatus). buffer state + ROADMAP + SkillOpt promote -> hera-vault.
   Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) SkillOpt promote'inta (validuoja architektūrą; imam patternus ne karkasą),
(2) Fazė 5d rejected-edit buffer įdiegta į selfedit/accretion (negatyvus feedback), (3) SAUGIKLIAI nepakeisti —
tripwire+benchmark+human-gate lieka; buffer tik informuoja, (4) demo: atmetimas→buffer→inject kitam pasiūlymui;
benchmark 9/9; gyvas failas nepakeistas, (5) „SKILLOPT PROMOTE + FAZĖ 5d ĮDIEGTA — mokomės iš atmestų pasiūlymų".

# Session Handoff

> SessionStart hook'as įkelia šį failą į kiekvieną naują sesiją. Atnaujink sesijos pabaigoje.
> **Konteksto inžinerijos taisyklė (2026-07-26):** čia rašom TIK tai, ko modelis NEGALI išvesti pats iš
> repo/git/aplinkos. Jokių DONE sąrašų, jokių pytest komandų, jokių pasenusių būsenų — tik viena dabartinė būsena.
> ⚠️ Šis failas VIEŠAS — jokių asmeninių/jautrių detalių; tik darbinis kontekstas.

## Vartotojas ir nekintančios taisyklės

- **Kas vartotojas:** **AI sistemų dizaineris/orkestruotojas** (diriguoja AI per specs+review; NE rankinis koderis;
  metodas: chat-Claude specs → Claude Code vykdo). Fonas: **ArchViz / 3D vizualizacija** (3ds Max/V-Ray, ComfyUI,
  3D Gaussian Splatting, TouchDesigner) — **NE statybos, niekada nemaišyti.**
  Pilnas strateginis profilis — TIK privačiame `hera-vault:profile/USER_STRATEGIC_PROFILE.md` (autoritetingas).
- **Bendravimas:** lietuviškai, konkrečiai, be atsiprašymų, be pamokymų, be jau žinomo kartojimo.
  **Kiekvieną anglišką terminą versti skliaustuose** (vartotojo direktyva, pakartota 2×).
- **STANDING RULE — auto-atmintis:** VISADA, be atskiro prašymo, persistink į vault kiekvieną reikšmingą faktą,
  sprendimą ar sistemos pokytį. Vartotojui NEREIKIA to prašyti kaskart.
- **Domenas HERA'oje NIEKADA nesiaurinamas** (vartotojo direktyva).
- **KURAVIMO PRINCIPAS:** „imam TIK tai, kas stiprina sistemą Į PRIEKĮ." Marketingą/dublius/nepatvirtintus žymėti,
  necituoti. Faithfulness `suspect` → atskirti realius neatitikimus nuo vertimo triukšmo (dažnai = triukšmas).
  Tikrinti „nemokama visam laikui" teiginius (precedentas: HY3 akcija buvo pasibaigusi).

## HERA nekintantys principai (galioja KIEKVIENAM pakeitimui)

€0 stack (Gemini free + Groq + GLM; jokio GPU; vienas 4GB VPS) · fail-safe (klaida → no-op, ne crash) ·
`HERA_*` jungikliai **default 0** · HARD timeout, **NO retry** (anti rc=124: dideles užduotis skaidyti) ·
**human-gate VISKAM, NIEKAD auto-merge** · git-atšaukiama · BACKUP prieš keitimą.

**Durabilumas:** kodas → PRIVATUS `hera-core-backup`; vault → PRIVATUS `hera-vault` (*/30 sync cron).
Viešas `cad-site-agent` — TIK sanitizuotas kontekstas (HERA moduliai gyvena untracked / `/opt/hera-processor`).

## Inbox mechanizmas (kaip užduotys pasiekia VPS)

Užduotis → `inbox/TASK.md` šakoje `claude/authorize-claude-code-vps-1dcvrv` → VPS cron runner (kas 2 min, flock,
15-min timeout) → `claude -p` vykdo → ataskaita per HERA botą.
Darbo eiga: `git worktree add` tos šakos → Read TASK.md → Write nauja → commit → push → `worktree remove`.

**TASK.md rašymo stilius (2026-07-26, po Anthropic „new rules of context engineering"):**
Rašyti **tikslą / realybę / apribojimus / įrodymus** — NE žingsnis-po-žingsnio įgyvendinimą.
- ĮDĖTI (modelis negali išvesti): €0 · viešo repo/secret'ų ribos · backup · def 0 konvencija · laiko biudžetas ·
  aplinkos faktai · **selftest sėkmės kriterijai**.
- PRALEISTI (modelis išveda pats): tikslūs regex'ai/funkcijų kūnai · edge-case sąrašai · pasikartojantys perspėjimai.

## Model policy

VPS runner pinnintas prie **Sonnet 5** (netaupo bendros quota) · orchestrator/planner = Fable 5 / Opus 5 ·
grunt work = Gemini/Groq/GLM (€0). Gemini **tekstas nemokamas**, **vaizdų generavimas MOKAMAS** (patikrinta 07-26).

## BŪSENA 2026-07-26

**Savęs-tobulinimo grandinė ir pajėgumai — GYVI** (visi €0, fail-safe, def 0 jei nenurodyta kitaip):
matuoklis (hera_bench) · SearXNG paieška · research orkestratorius · auto-research vartai · sandbox+savikorekcija
(bubblewrap, skill-akrecija, tripwire) · projektų žurnalas (hera_journal) · specialist agents + planner ·
eval-vartai (held-out split + overfitting flag) · **faithfulness vartas GYVAS** · Memora atmintis · PII/terse ·
hera_browser · wiki grafas+lint · **semantinė paieška** (hera_semsearch, fastembed ONNX; v1.2 eval PENDING) ·
**loop-guard + diffrules GYVI runner'yje** · perceived-error · LangFuzz-lite · **ctxtrim** (Fazė 20).

**Naujausios fazės (21–25, visos su selftest PASS, backup+push):**
- **21 `hera_goalanchor`** — determ. PlanFlip PF-1..4 injection + tikslo-drift detekcija (EN+LT). 6/6.
- **22 GoalAnchor runner integracija GYVA** — `HERA_GOALANCHOR=1`, ADVISORY anotacija (`🧭`) ataskaitoje prieš
  `send_tg`; timeout+`||true` izoliacija; flock/STATE-dedup NEPALIESTI.
- **23 `hera_skillcapture`** — dvigubo naudojimo kaupimas: kanoninis JSON → flat RAG projekcija + ShareGPT SFT
  konversija; gap-check; schedule-kandidatas. 7/7. **Def 0 — dar niekas nekviečia, duomenys DAR nesikaupia**
  (prijungimas + semsearch indeksavimas = atskiras human-gate).
- **24 `hera_dxf2png`** — determ. DXF → švarus 2D planas (text/dim filtras, sluoksnių pattern'ai, RAM saugiklis
  >200k entities). 6/6, realus DXF vizualiai patikrintas. ⚠️ **ezdxf 1.4.4 TIK `/opt/cad-venv`** (ne hera-venv,
  ne sistemos python3) + matplotlib/Pillow ten pat.
- **25 `hera_planrender`** — planas PNG → AI 3D renderis. **Gemini vaizdų API MOKAMAS → mokamas kelias
  HARDCODED užblokuotas**; modulis sudaro paruoštą užklausą (su „PRESERVE exact layout" mitigacija) rankiniam
  įklijavimui į nemokamą naršyklės sąsają. 5/5. €0 išleista.

**Ingest guardai:** YouTube `/post/` + `/community` URL → `PermanentSkip` fast-path (community postai ≠ video;
nedegina 3×5 retry). Kai kurie domenai (openai.com, youtube postai) blokuoja serverinį fetch → reikia rankinio teksto.

**Taryba (council) — €0, heterogeniška** (glm + 5×groq + 2×gemini; mokami praleidžiami).
⚠️ Žinomas apribojimas: `gemini-2.5-flash` JSON nukertamas net su maxOutputTokens=2048 (vidinis „thinking");
`gemini-flash-latest` veikia su 2048 (bump kol kas TIK ephemeral, `hera_council.py` nepakeistas — kandidatas įtvirtinti).

**cad-3d kryptis:** AutoCAD MCP `U-C4N` (ezdxf headless = tiesioginė sinergija DABAR) · 3ds Max MCP (desktop-future) ·
FreeCAD MCP (hibridinis; **sprendimas: NEDIEGIAM**, žinia ateičiai; cadquery ~300MB = pigiausias kelias kai prireiks).

**⏳ Laukia human-gate:** 3 staged prune · wiki orphan ~17 / dangling ~23 · atviri klausimai ~28 ·
semsearch v1.2 eval · skillcapture prijungimas prie srauto · `/doctor` ant `.claude/` · 3 n8n kredencialų rotacija.

## Repo struktūros ypatumas (svarbu, nenuspėjama)

- GitHub repo `tryspagaliai-lab/cad-site-agent` turi VISĄ turinį po poaplankiu `cad-site-agent/`; git šaknis — lygiu aukščiau.
- Claude Code auto-kraunasi `.claude/settings.json` TIK iš **repo šaknies** → hook'ai registruoti šaknyje.

## Aplinkos faktai (įsiminti)

- Atskirų „desktop" kompiuterių NĖRA. Vienintelė fizinė mašina — **LAPTOPAS su LINUX** (NE Windows; seni Windows/`E:/`
  keliai pasenę). Projektų raw data laptope, tikslūs keliai nežinomi (ieškoti `find ~`). Darbinė aplinka — **VPS**.
- Laptopo paleidimas: `bash cad-site-agent/scripts/bootstrap_local.sh`.
- Koordinacijos rolė `desktop` pervadinta į `local` (`docs/COORDINATION.md`).
- Layer-guard: realų gardą vykdo PreToolUse hook (`.claude/settings.json`), ne CLAUDE.md.

**Atnaujinta:** 2026-07-26

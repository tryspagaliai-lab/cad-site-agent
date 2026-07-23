UŽDUOTIS — Fazė 20: konteksto inžinerija (hera_ctxtrim.py) — didelė išvestis → failas + galvos/uodegos ištrauka. <12 min.
NEleisk pytest (tik savo selftest). Fail-safe. €0. Deterministiška (BE LLM). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK git prasme (untracked + /opt/hera-processor). Secret'us NEliesk.

KONTEKSTAS: iš LangChain lifecycle (Deploy/konteksto inžinerija) — kai įrankis grąžina didelę išvestį (pvz. 60k žetonų),
neįdedi visos į kontekstą: išsaugoti pilną į failą, rodyti tik galvą+uodegą + rodyklę „skaityk failą jei reikia". Taupo žetonus, saugo prompt-talpyklą.
Tai PASKUTINĖ iš LangChain extrakto eilės (žemėlapis + Fazės 18/19 jau padaryta).

1) Sukurk /root/hera_ctxtrim.py (kaip kiti hera_* moduliai; HERA_CTXTRIM jungiklis def 0 = passthrough; funkc. veikia visada):
   - API: `trim_output(text, max_chars=8000, keep_head=1200, keep_tail=2400, save_dir="/root/hera_ctxtrim") -> dict`
     grąžina {text: <trimmed_or_original>, full_path: <kelias ar None>, was_trimmed: bool, orig_len, kept_len}.
   - LOGIKA (determ.): jei len(text) <= max_chars → grąžink kaip yra (was_trimmed=False, full_path=None).
     Kitaip: sukurk save_dir jei nėra; įrašyk PILNĄ text į save_dir/ctx_<sha8>.txt; grąžink:
       text[:keep_head] + "\n\n...[IŠKIRPTA <N> ženklų · pilnas: <full_path> · skaityk failą jei reikia]...\n\n" + text[-keep_tail:].
   - Fail-safe: bet kokia klaida (pvz. disko) → grąžink ORIGINALŲ text nekeistą + log /root/hera_ctxtrim.log; NIEKAD necrashink, NIEKAD neprarask duomenų.
   - €0, be tinklo, be LLM. HERA_CTXTRIM=0 → passthrough (grąžina original, was_trimmed=False) — kad integracija būtų saugi def.
2) SELFTEST (`--selftest`, be pytest): (a) trumpas tekstas (<max) → nepakeistas, was_trimmed=False; (b) ilgas tekstas (>max) →
   was_trimmed=True, failas sukurtas IR jame PILNAS originalas (patikrink len), rodyklė yra text'e, galva+uodega išlaikyta;
   (c) HERA_CTXTRIM=0 → passthrough; (d) fail-safe: nerašomas save_dir (pvz. /nonexistent) → grąžina originalą, ne crash. Spausdink PASS/FAIL.
3) Runner integracija = v2 (atskiras human-gate — pvz. runner OUT per hera_ctxtrim prieš agent_result). Cron NEDĖK.
4) BACKUP: cp /root/hera_ctxtrim.py /opt/hera-processor/ + commit/push. Vault ROADMAP.md: „Fazė 20 konteksto-inžinerija (hera_ctxtrim) —
   ĮDIEGTA <data>, HERA_CTXTRIM def 0, v1 determ. didelė-išvestis→failas+galva/uodega, Deploy fazė, runner integr.=vėliau". Tai UŽBAIGIA LangChain extrakto eilę.

ATASKAITA (HERA botas, trumpai): modulis OK/ne; selftest PASS/FAIL (a/b/c/d — ypač b: failas turi PILNĄ originalą, jokio duomenų praradimo); backup+push; ROADMAP. Jei STOP — kodėl.

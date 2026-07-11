UŽDUOTIS — 5a FAZĖ: SANDBOX PAMATAS (bubblewrap no-net + git-worktree izoliacija; BE savęs-keitimo). <13 min, time-boxed.
NEleisk pytest. Telegram TRUMPAI. Fail-safe. SĄŽININGAI: jei VPS branduolys neleidžia — pasakyk, NEfeikink.

SAUGUMAS: raktų nespausdink/necommit'ink. Jei liesta kodą — push į PRIVATŲ hera-core-backup.

KONTEKSTAS: 5 fazės (savęs-tobulinimo) SAUGUMO pamatas. ŠITA užduotis — TIK izoliacijos infrastruktūra + įrodymas.
JOKIO savęs-keitimo, jokio LLM. Šablonas iš tyrimo: git-worktree + bubblewrap --unshare-net + benchmark-vartai.

1) ĮDIEK bubblewrap: apt-get install -y bubblewrap; bwrap --version. Patikrink NEPRIVILEGIJUOTUS user namespaces
   (ar veikia be root): `bwrap --unshare-net --ro-bind / / true` -> jei OK, izoliacija galima.
   Jei NEPAVYKSTA (kernel draudžia unpriv userns, pvz. sysctl) — pabandyk įjungti
   (sysctl kernel.unprivileged_userns_clone=1 jei egzistuoja) VIENĄ kartą; jei vis tiek ne — STOP, ataskaitoje
   „bubblewrap unpriv NEVEIKIA ant šio VPS — reikia atsarginio (firejail/nsjail) — nurodyk kernel versiją".
   NEfeikink veikimo.

2) hera_sandbox.py: funkcija run_in_sandbox(cmd, writable_dir, timeout=120) — paleidžia cmd bubblewrap'e:
   --unshare-net (JOKIO tinklo), --ro-bind /usr /usr, --ro-bind /bin /bin, --ro-bind /lib* ..., bazinis kodas
   read-only, --bind TIK writable_dir rašymui, --die-with-parent, --new-session, no-new-privs, laiko/atminties
   limitai (timeout + ulimit/systemd-run --scope MemoryMax jei paprasta). Grąžina {rc, stdout_tail, timed_out}.
   Fail-safe: klaida -> {rc: -1, error}, nekabo.

3) ĮRODYK IZOLIACIJĄ (3 testai, be LLM):
   a) NO-NET: sandbox'e paleisk `curl -m 5 https://example.com` (ar python urllib) -> turi ŽLUGTI (tinklo nėra).
      Parodyk, kad be sandbox tas pats curl VEIKTŲ (kontrolė) — įrodo, kad izoliacija reali.
   b) WRITE-RESTRICT: sandbox'e bandymas rašyti UŽ writable_dir (pvz. /opt/hera-processor/x) -> BLOKUOTA;
      rašymas Į writable_dir -> OK.
   c) WORKTREE IZOLIACIJA: sukurk git worktree iš /opt/hera-vault (ar test repo), pakeisk failą worktree'je ->
      gyvas /opt/hera-vault NEPAKITĘS (izoliuota kopija).

4) BENCHMARK SANDBOX'E: paleisk hera_bench.run() sandbox'e (be tinklo — jis deterministinis, tinklo nereikia) ->
   turi grąžinti pass_rate 1.0 (9/9). Įrodo, kad matuoklis veikia izoliuotoje aplinkoje (būsimiems vartams).
   Jei bench reikalauja tinklo/LLM — paleisk be sandbox ir pažymėk (bet jis deterministinis, turėtų veikti).

5) JOKIO SAVĘS-KEITIMO. Tik infrastruktūra + įrodymas. HERA_SANDBOX komentaras kode „5b/5c naudos".

6) DURABILUMAS: hera_sandbox.py kopija į n8n/hera/ + push į PRIVATŲ hera-core-backup. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai, be raktų): (1) bubblewrap įdiegtas + unpriv userns VEIKIA/NEVEIKIA (+kernel),
(2) izoliacijos testai a/b/c (no-net žlugo? write blokuota? worktree izoliuota?), (3) benchmark sandbox'e pass_rate,
(4) backup OK, (5) „SANDBOX PAMATAS PARUOŠTAS (5a)" arba „SANDBOX NEGALIMAS — <priežastis>".

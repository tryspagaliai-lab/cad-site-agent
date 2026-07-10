UŽDUOTIS — NAPMEM FAZĖ A: AKTYVI ATMINTIES NAVIGACIJA + VAULT SYNC Į GITHUB (VARTOTOJAS PATVIRTINO DIEGIMĄ).
<15 min, fokusuotai. NEleisk viso pytest — tik taikinius testus. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk. Vault sync — TIK į PRIVATŲ repo, prieš pirmą push — secret-scan.

KONTEKSTAS: NapMem tyrimas (Qwen/Alibaba, 2026-07-07, šiandien praėjo per pipeline): atmintis = veiksmų erdvė,
ne DB; aktyvus naršymas su biudžetu > vienkartinis RAG. RL mums nepasiekiamas (€0), bet HERA turi trajektorijas+
reward+replay — naršymo prompt'ą tobulins outer-loop (evoliucinis kelias vietoj GRPO).

DALIS 1 — AKTYVI NARŠYMO KILPA query kelyje (/opt/hera-processor/):

1) Vietoj vienkartinio RAG (question intent'ui) — naršymo kilpa: Gemini gauna atminties ĮRANKIUS:
   search_records (paieška growth/+skills/ santraukose), get_record (pilnas įrašas), search_extracted
   (paieška extracted/ žaliuose tekstuose), get_extracted (pilnas/fragmentas), stop_and_answer.
   Kilpa: klausimas -> veiksmas -> stebėjimas -> ... -> atsakymas. BIUDŽETAS: max 5 įrankių kvietimai
   (env HERA_NAV_BUDGET, default 5); pasiekus limitą — atsakyti iš to, kas surinkta.
2) SAUGIKLIS: env jungiklis HERA_NAV=1 įjungia kilpą; HERA_NAV=0 — senas vienkartinis RAG (rollback be kodo).
   Įjunk HERA_NAV=1 /root/hera.env'e. document_bounded skill'ų grounding taisyklė (jei vakar įdiegta) LIEKA
   galioti ir kilpoje.
3) TRAJEKTORIJA: kiekvienas naršymas loginamas su veiksmų seka (kokie įrankiai, kiek žingsnių, ar biudžetas
   viršytas) — kad reward/replay vėliau galėtų lyginti naršymo strategijas.
4) TESTAS: 2 klausimai ant esamo vault (pvz. „kas yra ATDP?" ir klausimas, kuriam reikia gilyn į extracted) —
   parodyk veiksmų sekas ir atsakymus; + HERA_NAV=0 regresija (senas kelias tebeveikia).

DALIS 2 — VAULT SYNC Į GITHUB (durabilumas + kad chat-Claude matytų vault'ą):

5) Sukurk PRIVATŲ repo tryspagaliai-lab/hera-vault (GITHUB_TOKEN iš env, kaip hera-core-backup atveju).
   /opt/hera-vault: git init (jei dar ne), .gitignore: ingest/ eilės šiukšlės jei didelės/binarinės — spręsk pats,
   bet growth/, skills/, extracted/, proposals/, trajectories/ PRIVALO būti sync'inami.
6) PRIEŠ pirmą push: secret-scan (grep raktų pattern'ų: sk-, gsk_, ghp_, nvapi-, AIza, token=...) — radus,
   išvalyk/ignoruok tą failą ir pažymėk ataskaitoje.
7) Auto-sync: cron kas 30 min (flock, kaip runner'io pamoka): jei /opt/hera-vault turi pakeitimų ->
   commit (žinutė su data) + push. Skriptas /usr/local/bin/hera_vault_sync.sh.
8) DURABILUMAS: naujo/pakeisto kodo kopija į /opt/cad-site-agent/n8n/hera/ + push į hera-core-backup
   (secret-scan prieš push). Į viešą cad-site-agent repo push NEDARYK.

9) ŠALUTINĖ PATIKRA: ar vakarykštės užduotys įvykdytos — (a) normatyviniai skill'ai (7469949), (b) n8n Link
   Parser YT fix (a65ae1a)? Jei kuri NE — pažymėk ataskaitoje, pats nedaryk.

TELEGRAM (trumpai, be raktų): (1) naršymo kilpa veikia? — 2 testų veiksmų sekos trumpai, (2) HERA_NAV=1 prod'e,
rollback=HERA_NAV=0, (3) hera-vault repo sukurtas+push'intas, cron sync įjungtas, secret-scan švarus?
(4) šalutinė patikra a/b (taip/ne), (5) „NAPMEM-A + VAULT-SYNC BAIGTA".

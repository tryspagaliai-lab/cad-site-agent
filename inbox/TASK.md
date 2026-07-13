UŽDUOTIS — Pataisyk hera-core-backup git push auth + push laukiančius commit'us. <8 min. NEleisk pytest.
Telegram TRUMPAI. Fail-safe. SAUGUMAS KRITINIS: raktų/tokenų NIEKADA nespausdink į logą/Telegram, necommit'ink,
nerodyk. Viešo repo NELIESK.

KONTEKSTAS: HERA_MEMORA įjungta gyvai, bet git push į PRIVATŲ hera-core-backup nepavyko („could not read Username
for github.com"). Commit'ai (2328285, 891b1cd + galbūt 2328285) laukia lokaliai. Reikia sukonfigūruoti git auth ir
push'inti. Ankstesni push'ai veikė — tikėtina token'as egzistuoja, tik nebeprijungtas prie git.

1) PATIKRINK ar GitHub token'as JAU egzistuoja VPS'e (pvz. hera.env: GITHUB_TOKEN/GH_TOKEN/GITHUB_PAT, arba
   ~/.git-credentials, arba git config). NEspausdink jo reikšmės — tik pasakyk RASTA/NERASTA (ir kuriame lauke).

2A) JEI TOKEN RASTAS: sukonfigūruok git credential SAUGIAI (nespausdinant token'o):
    - git config credential.helper store ARBA askpass, kuris skaito token'ą iš aplinkos/failo (NE embed'inti į
      remote URL komandoje kuri patenka į shell history/logą; jei naudoji token@github URL — necommit'ink .git/config
      ir nespausdink).
    - Push'ink hera-core-backup laukiančius commit'us į privatų GitHub. Patvirtink HEAD==origin po push.
    - Patikrink kad token NEpateko į jokį commit'inamą failą (grep .git/config necommit'inamas; jei .git-credentials
      naudojamas — jis .gitignore/už repo ribų).

2B) JEI TOKEN NERASTAS: NEfabrikuok. Pranešk aiškiai „token nerastas — reikia vartotojo". NEprašyk token'o Telegram/
    chat'e. Palik instrukciją kad vartotojas VPS'e (Termius) įrašytų GITHUB_TOKEN į hera.env arba
    `git credential-store`, tada pakartosim.

3) SANITY: jei push pavyko — patvirtink kad ankstesni „laukiantys" commit'ai (Memora wiring) dabar GitHub'e.
   Sistema turi likti veikianti (HERA_MEMORA=1, servisas active). Benchmark neprivalomas (auth-only), praleisk jei
   nereikia.

4) DURABILUMAS: jokių raktų niekur. Jei kūrei credential-helper config — necommit'ink token'o.

TELEGRAM (per HERA botą, trumpai, BE raktų): (1) token RASTA/NERASTA (be reikšmės), (2) jei rasta — git auth
sukonfigūruota + hera-core-backup laukiantys commit'ai push'inti (HEAD==origin), (3) jei nerasta — „reikia vartotojo:
įrašyk GITHUB_TOKEN VPS'e", (4) sistema veikia (MEMORA=1, active), (5) „BACKUP AUTH SUTVARKYTA" ARBA „LAUKIA TOKEN".

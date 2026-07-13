UŽDUOTIS — TVARUS backup push fix: push laukiančius commit'us + PERSISTENTIŠKAS credential (kad nebekartotųsi).
<8 min. NEleisk pytest. Telegram TRUMPAI. SAUGUMAS KRITINIS: token reikšmių NIEKADA nespausdink/necommit'ink/
nerodyk. Viešo repo NELIESK.

KONTEKSTAS: hera-core-backup push VĖL nepavyko („push laukia credential per politiką"). Laukiantys lokalūs commit'ai
(pvz. fe0e394, 1f46f54, 24acacd + galbūt daugiau) NĖRA GitHub'e — durabilumo rizika. Ankstesnis askpass fix (11:45)
NEpersistavo (tikėtina servisas/aplinka jį pamiršo). Reikia TVARAUS sprendimo.

1) PATIKRINK laukiančius: hera-core-backup darbo kopijoje `git log origin/main..HEAD --oneline` — kiek commit'ų
   laukia push (be raktų reikšmių).

2) TVARUS CREDENTIAL (persistentiškas, saugus): naudok token'ą JAU esantį hera.env (GITHUB_TOKEN vpr.) — NEspausdink.
   Sukonfigūruok PERSISTENTIŠKAI (kad išliktų per restart'us ir per-invocation):
   - Variantas A: `git config credential.helper 'store --file=/root/.git-credentials-hera'` + įrašyk credential į tą
     failą PROGRAMIŠKAI iš env token'o (necommit'ink; failas už repo ribų, chmod 600).
   - ARBA askpass helper skriptą, kuris skaito token'ą iš hera.env kiekvieną kartą (persistentiškas per git config
     --global core.askpass). Necommit'ink token'o niekur.
   Necommit'ink .git-credentials/askpass su token'u; įsitikink kad jie .gitignore/už repo ribų.

3) PUSH: push'ink laukiančius hera-core-backup commit'us į privatų GitHub. Patvirtink HEAD==origin po push.

4) VERIFIKACIJA kad TVARU: padaryk tuščią test-commit (arba touch+commit nekenksmingą marker failą) IR push'ink dar
   kartą TA PAČIA credential konfigūracija -> jei praeina be rankinio įsikišimo, credential persistentiškas. (Test
   commit gali likti arba revert'ink — necommit'ink raktų.)

5) SVARBU dokumentuok atmintyje: „backup push credential PERSISTENTIŠKAS (helper=..., token iš hera.env, be raktų
   repo)" — kad kita sesija žinotų kur konfigūracija.

TELEGRAM (per HERA botą, trumpai, BE token reikšmių): (1) laukė N commit'ų, (2) persistentiškas credential helper
sukonfigūruotas (be raktų repo/config), (3) push OK — HEAD==origin (visi Fazės 10 commit'ai GitHub'e), (4) test-push
praėjo be rankinio įsikišimo (tvaru), (5) „BACKUP PUSH TVARIAI SUTVARKYTA — nebekartosis".

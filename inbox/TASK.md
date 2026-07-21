UŽDUOTIS — READ-ONLY: ar n8n UI (per domeną) reikalauja login / ar owner-account sukurtas? NIEKO NEKEISK. <7 min.
NEleisk pytest. Fail-safe. €0. TIK skaitymas — jokio login, jokio account kūrimo, jokio config keitimo. Ataskaita TIK į HERA botą.
Viešo cad-site-agent NELIESK. hera-vault NELIESK. Secret'us redaguok. Domeną ataskaitoj rodyk (HERA botas privatus).

KONTEKSTAS: n8n viešas TIK per Caddy (https://n8n.<domenas>/), :5678 tiesiogiai neatviras. Belieka patikrinti likutinę
riziką: ar UI už login, ar owner-account jau sukurtas (jei NE — bet kas užėjęs galėtų pasisavinti owner rolę = kritiška).

ŽINGSNIAI (visi read-only, curl be jokių kredencialų):
1) BASE URL iš env: `BASE=$(docker exec n8n-n8n-1 printenv WEBHOOK_URL 2>/dev/null | tr -d '\r' | sed 's:/*$::')`; echo "BASE=$BASE".
   (Jei tuščia — imk iš N8N_EDITOR_BASE_URL. Jei ir tas tuščias — STOP, reportuok.)
2) SETUP BŪSENA (svarbiausia): `curl -s --max-time 10 "$BASE/rest/settings"` → ištrauk lauką
   `userManagement.showSetupOnFirstLoad` (grep -oE '"showSetupOnFirstLoad":[a-z]*').
   → =true = owner NESUKURTAS (KRITIŠKA: bet kas gali claim'inti). =false = owner jau yra (gerai).
3) LOGIN REIKALAVIMAS: `curl -s -o /dev/null -w "root=%{http_code} redirect=%{redirect_url}\n" --max-time 10 "$BASE/"`;
   `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 "$BASE/rest/workflows"` (be auth → tikimasi 401; jei 200 = UI/API ATVIRAS!).
4) (jei yra) `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 "$BASE/rest/login"` — tik statusui.
5) MFA/2FA (jei matosi settings): pažymėk ar įjungta (neprivaloma).

ATASKAITA (HERA botas, trumpai): BASE URL; showSetupOnFirstLoad true|false (owner sukurtas ne|taip);
/rest/workflows be auth kodas (401=apsaugota / 200=ATVIRA); / kodas+redirect; IŠVADA: UI saugus (login + owner set) ar rizika.

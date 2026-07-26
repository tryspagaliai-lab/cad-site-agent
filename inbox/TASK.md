UŽDUOTIS — vault žinių grafas kaip GYVAS puslapis ant VPS (telefonui). <14 min.

## Tikslas
Vartotojas dirba TIK telefonu. Orchestratorius jau sugeneravo savarankišką HTML grafą (128 mazgai, 482 ryšiai),
bet tai momentinė nuotrauka — neatsinaujina. Padaryk, kad grafas gyventų ant VPS: **viena nuoroda, kurią vartotojas
atsidaro telefone bet kada, ir kuri pati atsinaujina** iš vault.

## 🔴 SAUGUMAS — griežčiausias reikalavimas
Vault PRIVATUS. **Puslapis NEGALI būti pasiekiamas be autentifikacijos.**
Precedentas: šiame projekte jau buvo incidentas — 3 neautentifikuoti n8n MCP endpoint'ai, teko išjungti.
NEKARTOK. Jei negali užtikrinti autentifikacijos — **NEPUBLIKUOK, praneša ir sustok.**
Slaptažodį/token'ą sugeneruok atsitiktinį, įrašyk į HERA botą ATASKAITOJE (tai privatus kanalas), NE į git.
Jokių kredencialų į jokį repo. Jokio 0.0.0.0 be auth.

## Realybė (ko pats neišvestum)
- Vault ant VPS: `/opt/hera-vault`. Grafo generavimo logika (kad nekurtum iš naujo): visata = `.md` failų stem'ai
  **PLIUS katalogų vardai** (`skills/<slug>/SKILL.md` — skills yra KATALOGAI, ne failai; tai jau kartą suklaidino).
  Katalogą `analysis/` IŠSKIRTI kaip šaltinį — jame lint savo ataskaitos, cituojančios `[[token]]` žmogui, ne nuorodos.
- Ant VPS jau kažkas sukasi web'e (buvo n8n) — pirma PATIKRINK kas klauso portų ir ar yra nginx/caddy, kad
  nesudaužytum esamų servisų ir nepaimtum užimto porto.
- HTML turi būti savarankiškas (0 išorinių užklausų) ir liesti pritaikytas: bakstelėjimas=mazgo ryšiai,
  tempimas=panorama, suglaudimas=zoom. Jei norisi pavyzdžio — orchestratoriaus versija naudojo canvas + force-directed,
  bet gali daryti savaip; svarbu kad veiktų telefono naršyklėje.

## Apribojimai
€0 (jokių naujų mokamų servisų, jokio tunelio su prenumerata). Fail-safe. Determ. generavimas (BE LLM).
Ataskaita TIK į HERA botą. Viešo `cad-site-agent` NELIESK. BACKUP prieš keitimą. Vault turinio NEMODIFIKUOK — tik skaitymas.
Atnaujinimas per cron — DERINK prie esamo `hera_vault_sync.sh` ritmo (*/30), nedėk dažniau.
Jei kas nors reikalautų atidaryti VPS platesniam internetui be auth — STOP.

## Įrodymai (ko tikiuosi ataskaitoje)
1. **URL + kaip autentifikuotis** (vartotojo/slaptažodžio pora arba token'as) — kad vartotojas iškart galėtų atsidaryti telefone.
2. **Autentifikacijos įrodymas:** `curl` be kredencialų → 401/403; su kredencialais → 200. Parodyk abu.
3. Kokį web serverį naudojai ir ar NEPALIETEI esamų servisų (kas klausė portų prieš/po).
4. Mazgų/ryšių skaičius sugeneruotame grafe (turi būti panašu į 128/482; jei labai skiriasi — paaiškink).
5. Kaip atsinaujina (cron eilutė) + ką daro jei generavimas nepavyksta (turi likti SENAS puslapis, ne tuščias).
6. BACKUP + push į privatų `hera-core-backup`; ROADMAP.md eilutė.

Jei STOP (saugumas / portų konfliktas) — kodėl, ir ką radai.

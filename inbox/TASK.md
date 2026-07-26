UŽDUOTIS — grafo prieiga BE slaptažodžio, bet NE be apsaugos. <13 min.

## Tikslas
Vartotojas (dirba tik telefonu) atsidarė https://n8n.tryspagaliai.com/hera-vault-graph/ — Basic Auth paprašė
slaptažodžio, ir jis to NENORI (22 simbolių atsitiktinis slaptažodis telefone = kankynė; sprendimas jo).
Pakeisk apsaugos FORMĄ taip, kad **vartotojas nieko nevestų — nei karto, nei kaskart** — bet puslapis
NELIKTŲ atviras internetui.

## Sprendimas, kurio noriu (nebent rasi geresnį — tada pagrįsk)
**Neatspėjamas URL (capability URL) + ilgaamžis slapukas (cookie):**
- Naujas kelias su ≥128 bitų atsitiktinumo, pvz. `/g/<32+ simbolių atsitiktinis>/`.
- Pirmas apsilankymas nustato ilgaamžį slapuką (pvz. 1 metai, `HttpOnly`, `Secure`, `SameSite=Lax`) →
  vartotojas pasižymi nuorodą telefone ir daugiau NIEKADA nieko neveda.
- Jei slapuko nėra IR kelias neteisingas → **404** (ne 401 — neatskleidžia, kad kažkas ten yra).
- SENĄ `/hera-vault-graph/` kelią su Basic Auth **pašalink arba palik veikiantį** — tavo sprendimas, bet
  neturi likti dviejų skirtingos stiprybės durų į tą patį turinį be priežasties.

## Realybė (ko pats neišvestum)
- Serveris: esamas Caddy konteineris `n8n-caddy-1`, domenas/TLS `n8n.tryspagaliai.com` — naudok TĄ PATĮ,
  BE naujo porto, BE naujo DNS, BE tunelio (taip padaryta praeitą kartą, veikė gerai).
- Generatorius `hera_vault_graph.py` + cron `5,35 * * * *` jau veikia — NELIESK generavimo logikos, tik prieigą.
- Puslapis daro **0 išorinių užklausų** → Referer nutekėjimo rizikos nėra (svarbu, nes capability URL saugumas
  remiasi tuo, kad nuoroda nenutekės).

## Apribojimai
€0. Fail-safe. Ataskaita TIK į HERA botą. **Naują URL siųsk TIK per HERA botą, NIEKADA į git.**
Viešo `cad-site-agent` NELIESK. BACKUP Caddy konfigo prieš keitimą. n8n maršruto NESUDAUŽYK.
Pridėk `X-Robots-Tag: noindex, nofollow` ir `robots.txt` Disallow — kad neįsipultų į paieškos sistemas.
**Jei negali užtikrinti, kad be teisingo kelio/slapuko turinys NEPASIEKIAMAS — STOP, palik kaip yra, praneša.**

## Įrodymai (ko tikiuosi ataskaitoje)
1. **Naujas URL** (paruoštas pasižymėti telefone) — vienas paspaudimas, jokio įvedimo.
2. `curl` be nieko į SENĄ kelią ir į atsitiktinį neteisingą kelią → **404**; į teisingą → **200**. Parodyk visus.
3. Ar slapukas tikrai nustatomas (parodyk `Set-Cookie` antraštę) ir ar antras užklausimas BE kelio, tik su slapuku, veikia.
4. n8n šaknis nepaliesta (200 prieš/po), portai tie patys.
5. `X-Robots-Tag` + `robots.txt` yra.
6. BACKUP + push į privatų `hera-core-backup`; ROADMAP.md eilutė.

## Sąžininga pastaba, kurią įrašyk į ataskaitą
Capability URL yra **silpnesnė apsauga nei slaptažodis**: kas turi nuorodą — turi prieigą. Rizika priimtina, nes
nuoroda gyvena tik vartotojo telefone ir puslapis nieko neeksportuoja. Bet pasakyk vartotojui aiškiai: **nedalinti
nuorodos, nedaryti ekrano nuotraukų su URL juosta.** Jei nuoroda kada nutekėtų — pakanka pergeneruoti kelią.

Jei STOP — kodėl.

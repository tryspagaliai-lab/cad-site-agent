UŽDUOTIS — Fazė 43: GitHub PAT priklausomybių žemėlapis PRIEŠ pergeneravimą. TIK SKAITYMAS. LAIKO JAUTRU. <12 min.

## Kodėl dabar ir kodėl skubu
Vartotojas gavo GitHub laišką, kad **fine-grained Personal Access Token netrukus baigia galioti**, ir ruošiasi jį
pergeneruoti (90 d.). „Regenerate" **panaikina dabartinį raktą tą pačią sekundę** ir išduoda naują.
Tarp pergeneravimo ir naujo rakto įdiegimo VPS'e sistema bus akla — ir lūš **TYLIAI**.

**Ši užduotis turi būti įvykdyta KOL SENAS RAKTAS DAR VEIKIA.** Todėl ji pirmesnė už viską kitą eilėje.

## 🔴 TIK SKAITYMAS
Nieko nekeisk, nerotuok, netrink, neperkrauk. Rakto reikšmės (ar jos dalies) **niekur nespausdink** — nei
ataskaitoje, nei tarpiniuose failuose. Tapatumui, jei prireiks lyginti, naudok `sha256` pirmus 8 hex simbolius.

## Ką reikia išsiaiškinti

### 1. Kur raktas gyvena
Suskaičiuok VISAS vietas, kuriose VPS'e saugomas GitHub kredencialas. Kandidatai (NE baigtinis sąrašas —
**skenuok, neenumeruok**; Fazė 36 „rado 2 vietas" enumeruodama, Fazė 37 skenuodama rado 3):
git remote URL'ai su įterptu token'u · `~/.git-credentials` · `git config --global credential.*` ·
credential helper'iai · env kintamieji (`GH_TOKEN`, `GITHUB_TOKEN`) · systemd `EnvironmentFile` · cron aplinka ·
`/root/hera.env` · deploy raktai (`~/.ssh/`) — jei kur nors naudojamas SSH, o ne HTTPS+token, tai irgi svarbu žinoti.
**Patikrink ir GYVŲ procesų `/proc/<pid>/environ`** (`hera-processor`, `hera-ingest`) — Fazė 42 parodė, kad
konfigų failai gali meluoti, o `/proc` ne.

### 2. Kas nuo jo priklauso
Kiekvienam radiniui — kuri sistemos dalis nulūžtų. Žinomi kandidatai:
· **vault sync cron** (*/30 min → privatus `hera-vault`) · **`hera-core-backup` push'ai** (ten VISAS kodas,
įsk. ką tik išsaugotą v1.2 WIP) · **git-inbox** (šis kanalas!).

### 3. ⭐ VIŠTOS-IR-KIAUŠINIO PATIKRA (svarbiausia)
**Ar git-inbox mechanizmas priklauso nuo šio rakto?** Konkrečiai: kaip runner gauna `inbox/TASK.md` iš
`tryspagaliai-lab/cad-site-agent` — su autentifikacija ar be? Tas repo yra **VIEŠAS**, tad pull'ui token'o
teoriškai nereikia — **patikrink, ar taip yra iš tikrųjų**, o ne prielaidą.
**Jei inbox priklauso nuo rakto — po pergeneravimo aš nebegalėsiu atsiųsti užduoties, kuri jį pataisytų.**
Tai kritinis radinys ir turi būti ataskaitos pradžioje.

### 4. ⭐ KAIP NAUJAS RAKTAS PATEKS Į VPS (tikrasis blokatorius)
`TASK.md` eina per **VIEŠĄ** git repo — paslapties ten dėti NEGALIMA. Pokalbio kanalu irgi ne.
Vartotojas dirba **TIK telefonu**.
**Nustatyk, kokie realūs keliai egzistuoja**, kuriais jis iš telefono gali pristatyti paslaptį į VPS:
ar HERA botas turi įeinančių komandų kelią? ar yra n8n webhook? ar kas nors kita, kas jau veikia?
Jei tokio kelio NĖRA — tai irgi atsakymas, ir tada reikės jį sukurti prieš pergeneravimą.

### 5. Galiojimo data
Jei įmanoma nustatyti, kada dabartinis raktas baigia galioti (pvz. iš GitHub API atsakymo antraščių ar
`gh auth status`, jei įdiegtas) — pranešk. Jei ne — pasakyk, kad neįmanoma, ir kaip bandei.

## Apribojimai
€0 · viešo `cad-site-agent` git NELIESK · jokių rakto reikšmių · HARD timeout, be retry ·
NEBANDYK pats pergeneruoti ar keisti rakto — tai vartotojo veiksmas naršyklėje.

## Ataskaitoje
Lentelė: **vieta → kas priklauso → kas nulūžtų** · vienareikšmis atsakymas dėl inbox priklausomybės ·
sąrašas realių kelių paslapčiai pristatyti (arba „nėra") · **atstatymo planas: ką tiksliai reikės padaryti
po pergeneravimo, kokia eilės tvarka** · sąžiningas „ko nustatyti nepavyko".

**ATASKAITOS TAISYKLĖ:** teiginys „neįmanoma / nepavyko patikrinti" galioja **tik kartu su sąrašu, KĄ BANDEI.**

Jei STOP — kodėl.

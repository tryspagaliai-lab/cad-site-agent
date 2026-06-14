# CAD Site Agent — diegimas į Hetzner VPS (SSH / komandinė eilutė)

Šis vadovas perkelia **visą sistemą į tavo VPS**, kad kodas ir know-how būtų tik
tavo serveryje — niekada nelieka darbo kompiuteryje.

Yra du keliai:

- **A. Native** (paprasčiausias, rekomenduojamas) — Python venv tiesiai VPS'e.
- **B. Docker** (pilnai izoliuotas) — viskas konteineryje.

Pasirink vieną. Abu naudoja tą patį `cad-agent` įrankį.

---

## 0. Ko reikės

- Hetzner Cloud VPS (užtenka **CX22** / 2 vCPU / 4 GB RAM; dideliems DXF — CX32).
- OS: **Ubuntu 24.04** (arba 22.04).
- Tavo SSH raktas pridėtas prie serverio kuriant jį Hetzner konsolėje.

---

## 1. Sukurk serverį (Hetzner konsolėje)

1. `console.hetzner.com` → tavo projektas (pvz. **Test**) → **CREATE SERVER**.
2. **Location**: arčiausiai tavęs (pvz. Helsinki/Nuremberg).
3. **Image**: Ubuntu 24.04.
4. **Type**: CX22 (arba galingesnis dideliems brėžiniams).
5. **SSH key**: pasirink savo raktą (NEnaudok slaptažodžio prisijungimo).
6. **Create & Buy now**. Užsirašyk serverio **IP adresą**.

---

## 2. Prisijunk per SSH

```bash
ssh root@VPS_IP
```

(Saugumui rekomenduojama susikurti atskirą naudotoją vietoje `root`, bet
pradžiai užtenka ir `root`.)

---

## 3. Parsisiųsk projektą į VPS

### Variantas su privačiu GitHub repo (rekomenduojama)

```bash
# VPS'e:
git clone https://github.com/tryspagaliai-lab/cad-site-agent.git
cd cad-site-agent/cad-site-agent          # projektas yra poaplankyje
```

> Jei repo privatus — naudok GitHub Personal Access Token arba deploy raktą.

### Variantas be GitHub (tiesioginis perkėlimas iš savo kompiuterio)

```bash
# Savo kompiuteryje, projekto kataloge:
scp -r cad-site-agent  root@VPS_IP:~/
# Paskui VPS'e:
ssh root@VPS_IP
cd cad-site-agent
```

---

## A. Native diegimas (rekomenduojamas)

```bash
# Projekto šaknyje (kur yra pyproject.toml):
bash deploy/setup-vps.sh
```

Skriptas viską padaro pats: įdiegia sistemos bibliotekas, sukuria `.venv`
ir įdiegia `cad-agent`. Saugu paleisti kelis kartus.

Po įdiegimo, kiekvienoje naujoje SSH sesijoje:

```bash
source .venv/bin/activate
cad-agent --help
```

---

## B. Docker diegimas (alternatyva, pilna izoliacija)

```bash
# Įdiek Docker (jei dar nėra):
curl -fsSL https://get.docker.com | sh

# Projekto šaknyje sukurk image:
docker build -t cad-agent .

# Paleisk (darbinis katalogas su DXF montuojamas į /work):
mkdir -p work/output
docker run --rm -v "$PWD/work:/work" cad-agent \
    process /work/input.dxf /work/output/result.dxf
```

---

## 4. Kaip naudoti — pilnas pavyzdys

```bash
# 1) Savo kompiuteryje: nusiųsk DXF į VPS
scp brezinys.dxf  root@VPS_IP:~/cad-site-agent/input.dxf

# 2) VPS'e: apdorok
ssh root@VPS_IP
cd cad-site-agent/cad-site-agent
source .venv/bin/activate          # (Native kelias)
mkdir -p output
cad-agent process input.dxf output/result.dxf

# 3) Savo kompiuteryje: parsisiųsk rezultatus
scp 'root@VPS_IP:~/cad-site-agent/cad-site-agent/output/result*' ./
```

`process` sukuria keturis failus (žr. README.md „Output Files"):
`result.dxf`, `result.hatches.dxf`, `result.hatch_candidates.json`,
`result.process.json`.

---

## 5. Know-how apsauga — svarbu

- **Kodas lieka tik VPS'e.** Darbo kompiuteryje dirbk tik per SSH — neklonuok
  repo į darbinę mašiną.
- **Privatus repo.** Laikyk GitHub repo privatų; naudok deploy raktą tik VPS'e.
- **DXF failai necommitinami.** `.gitignore` ir `.dockerignore` jau blokuoja
  `*.dxf`, `*.dwg`, `output/` ir kt. produkcinius failus.
- **Atskiras naudotojas + firewall.** Hetzner konsolėje įjunk Firewall: leisk
  tik 22 prievadą (SSH) iš savo IP.
- **Atsarginės kopijos.** Įjunk Hetzner automatines Backups serverio nustatymuose.

---

## 6. Dažni klausimai

**Ar reikia Docker, jei pasirinkau Native?** Ne. Native užtenka SSH/CLI darbui.
Docker — tik jei nori 100 % izoliuotos, perkeliamos aplinkos.

**Kiek RAM reikia?** Vidutiniams brėžiniams 4 GB (CX22). Labai dideliems
DXF su tūkstančiais regionų — 8 GB (CX32).

**Ar veiks `rtree` optimizacija?** `setup-vps.sh` įdiegia `libspatialindex-dev`,
tad gali papildomai: `pip install -e ".[rtree]"`.

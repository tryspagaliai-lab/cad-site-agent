# ODA File Converter — diegimas (DWG → DXF)

Sistema skaito **DXF** (`ezdxf.readfile`), o ne DWG. DWG failai pirma
konvertuojami į DXF su nemokamu **ODA File Converter**.

> ⚠️ NUOTOLINĖJE (cloud/web) Claude Code sesijoje ODA įdiegti NEGALIMA:
> tinklas apribotas (opendesign.com blokuojamas), konteineris efemeris, ir ten
> nėra DWG failų. ODA diegiamas ir naudojamas **DESKTOPE**, kur yra raw data.

## 1. Parsisiųsk
https://www.opendesign.com/guestfiles/oda_file_converter (nemokama, reikia el. pašto).

## 2. Įdiek
- **Windows:** paleisk installerį. `ODAFileConverter.exe` numatytoje vietoje
  (`C:\Program Files\ODA\...`) — `ezdxf` randa automatiškai.
- **Linux:** `.deb` (`sudo dpkg -i ODAFileConverter_*.deb`) arba AppImage.
  Jei ne PATH — nurodyk kelią per `ODAFC_EXEC` env var.
- **macOS:** įtempk `ODAFileConverter.app` į Applications.

## 3. Patikrink
```bash
python -c "from ezdxf.addons import odafc; print('ODA įdiegtas:', odafc.is_installed())"
```

## 4. Konvertuok (batch)
```bash
# vienas failas arba visas katalogas:
python scripts/dwg_to_dxf.py "C:/Users/zilva/Desktop/H7149 Osprey Heights" --out ./data/h7149_dxf --recursive
```
Skriptas grąžina JSON santrauką (kiek rasta / konvertuota / klaidos) — patogu
paduoti Kimi/MiMo kryžminei patikrai ir įrašyti į koordinacijos lentą.

## 5. Toliau — pipeline
Konvertuotus DXF paduok pipeline'ui:
```bash
python -m cad_site_agent.cli analyze-dxf ./data/h7149_dxf/<failas>.dxf
# arba pilnas: process <source_dxf> <output_dxf>
```

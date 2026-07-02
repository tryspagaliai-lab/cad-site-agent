# ODA File Converter — diegimas (DWG → DXF)

Sistema skaito **DXF** (`ezdxf.readfile`), o ne DWG. DWG failai pirma
konvertuojami į DXF su nemokamu **ODA File Converter**.

> ⚠️ NUOTOLINĖJE (cloud/web) Claude Code sesijoje ODA įdiegti NEGALIMA:
> tinklas apribotas (opendesign.com blokuojamas), konteineris efemeris, ir ten
> nėra DWG failų. ODA diegiamas ir naudojamas **LAPTOPE** (vienintelė fizinė
> mašina; ateityje galbūt VPS), kur yra raw data.

## 1. Parsisiųsk
https://www.opendesign.com/guestfiles/oda_file_converter (nemokama, reikia el. pašto).

## 2. Įdiek
- **Windows:** paleisk installerį. `ODAFileConverter.exe` numatytoje vietoje
  (`C:\Program Files\ODA\...`) — `ezdxf` randa automatiškai.
- **Linux:** `.deb` (`sudo dpkg -i ODAFileConverter_*.deb`) arba AppImage.
  Jei ne PATH — nurodyk kelią per `ODAFC_EXEC` env var.
- **macOS:** įtempk `ODAFileConverter.app` į Applications.

### Linux BE root (patikrinta 2026-07-02, laptopas — Ubuntu 22.04)
`sudo` gali būti neprieinamas (reikalauja slaptažodžio). QT6 `.deb` yra
savarankiškas (susikomplektuoja savo Qt6 bibliotekas → `lib/`), tad jį galima
išskleisti į naudotojo katalogą be root:

```bash
# 1. parsisiųsk .deb (guestfiles get -> presigned S3 redirect, galioja ~60 s):
URL='https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_lnxX64_8.3dll_27.1.deb'
curl -sL "$URL" -o ~/Downloads/ODAFileConverter.deb

# 2. išskleisk BE root:
dpkg-deb -x ~/Downloads/ODAFileConverter.deb ~/.local/oda

# 3. wrapper į PATH (originalus wrapper turi HARDCODED /usr/bin kelią — netinka):
cat > ~/.local/bin/ODAFileConverter <<'EOF'
#!/bin/sh
ODADIR="$HOME/.local/oda/usr/bin/ODAFileConverter_27.1.0.0"
export LD_LIBRARY_PATH="$ODADIR/lib:$LD_LIBRARY_PATH"
export QT_PLUGIN_PATH="$ODADIR/plugins"
export QT_QPA_PLATFORM_PLUGIN_PATH="$ODADIR/plugins/platforms"
exec "$ODADIR/ODAFileConverter" "$@"
EOF
chmod +x ~/.local/bin/ODAFileConverter

# 4. kad ezdxf rastų nepriklausomai nuo PATH — įrašyk į ezdxf konfigą:
python3 -c "import ezdxf; ezdxf.options.set('odafc-addon','unix_exec_path','$HOME/.local/bin/ODAFileConverter'); ezdxf.options.write_home_config()"
```
Patikra: `python3 -c "from ezdxf.addons import odafc; print(odafc.is_installed())"` → `True`.
(GUI atsidaro trumpam ekrane; norint be lango — įsidiek `xvfb`.)

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

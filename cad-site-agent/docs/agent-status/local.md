# Agent status: local

- updated: 2026-07-02T13:26:31Z
- branch: main
- head: 1c1379f
- status: DONE (LINUX laptopas). (1) ODA File Converter įdiegtas BE root: parsisiųstas QT6 .deb, išskleistas dpkg-deb -x -> ~/.local/oda, wrapper ~/.local/bin/ODAFileConverter + ezdxf unix_exec_path konfige (odafc.is_installed()==True net su švariu PATH). Metodas dokumentuotas docs/ODA_SETUP.md. (2) H7149 raw DWG failas RASTAS laptope (išoriniame diske, senų projektų archyve; 2.9MB, AutoCAD2018; vienas DWG failas). (3) DWG->DXF konvertuota (18.9MB) ir run_pipeline_batch.py ant to vieno failo pavyko: processed 1, failed 0. process etapas: candidates_total 499, review 80, auto 0, features_written 3801, features_removed 0, features_skipped 43177, drawing_type unknown/0.0; normalize: 15 unmapped_layers. (4) Tandemo paketas sugeneruotas: reports/tandem/tandem_package_2026-07-02T14-22-35.md (paduok Kimi/MiMo). Output: cad-site-agent/data/h7149/ (DXF gitignore, necommit). SEKANTIS ŽINGSNIS pagal vartotoją: įdiegti opencode + sujungti, tada cursor.

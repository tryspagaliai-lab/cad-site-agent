# Agent status: local (Claude Code LAPTOPE — Linux, vienintelė fizinė mašina)

- updated: 2026-07-02T07:00:00Z
- branch: main
- head: (pildyti)
- status: TODO — paleidimas: `bash cad-site-agent/scripts/bootstrap_local.sh`.
  Tada: (1) jei ODA File Converter neįdiegtas — įdiek Linux .deb
  (docs/ODA_SETUP.md); (2) SURASK „H7149 Osprey Heights" katalogą diske
  (`find ~ -iname "*osprey*" -maxdepth 4`) — senas `C:\Users\zilva\...` kelias
  KLAIDINGAS, laptopas yra Linux; (3) konvertuok DWG→DXF ir paleisk
  `python3 cad-site-agent/scripts/run_pipeline_batch.py "<rastas kelias>" --out data/h7149 --recursive`;
  (4) sugeneruok tandemo paketą `scripts/tandem_report.py --batch data/h7149/batch_report.json`;
  (5) rezultatus surašyk čia per `./.claude/hooks/agent-status.sh local "..."`.

> Pastabos: rolė anksčiau vadinosi `desktop` — atskiro desktopo NĖRA.
> Windows prielaida (C:\ keliai) buvo klaidinga — aplinka LINUX.

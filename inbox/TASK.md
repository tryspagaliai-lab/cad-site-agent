UŽDUOTIS — įjungti TIK HERA_LOOPGUARD=1 (pakopinis v2 aktyvavimas). NIEKO daugiau. <7 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK.
SVARBU: NEĮJUNK HERA_DIFFRULES (lieka 0). Tik loop-guard (advisory, žemiausia rizika).

KONTEKSTAS: Fazė 16 įpynė loop-guard+diffrules į runner (flag-gated, def 0). Dabar pakopiškai aktyvuojam — pirma tik loop-guard.
Šio task'o sėkmingas apdorojimas ir yra įrodymas kad redaguotas runner veikia normaliai.

ŽINGSNIAI:
1) Rask KUR nustatyti esami gyvi flag'ai HERA_MEMORA=1 / HERA_GPUFILTER=1 / HERA_FAITHFULNESS=1 (grep -rn 'HERA_MEMORA\|HERA_FAITHFULNESS'
   /root/hera.env /root/ai_digest.env /usr/local/bin/vps_agent_runner.sh /etc/cron.d/ 2>/dev/null; ir bet kur kitur kur jie eksportuojami).
   Naudok TĄ PATĮ mechanizmą (tą patį failą/vietą) — kad loop-guard flag'as gyventų nuosekliai su kitais.
2) BACKUP to failo prieš keitimą (cp <failas> /root/hera-core-backup/<failas>.$(date +%s)).
3) Pridėk HERA_LOOPGUARD=1 toje pačioje vietoje/formatu kaip kiti gyvi flag'ai (jei env failas — eilutė `HERA_LOOPGUARD=1` arba
   `export HERA_LOOPGUARD=1` kaip kiti; jei runner skripte export blokas — ten). NEDUBLIUOK jei jau yra.
4) Jei keitei skriptą — `bash -n` patikra. Jei env failą — patvirtink `grep HERA_LOOPGUARD <failas>`.
5) Patvirtink kad HERA_DIFFRULES NĖRA įjungtas (turi likti 0/neapibrėžtas).

ATASKAITA (HERA botas, trumpai): kur gyvena HERA_* flag'ai (failas); HERA_LOOPGUARD=1 pridėtas OK (formatas); bash -n/grep patikra;
patvirtink HERA_DIFFRULES=0; backup kelias. (Loop-guard įsigalios kitam task'ui — advisory eilutė ataskaitose jei aptiks loop/stagnaciją.)

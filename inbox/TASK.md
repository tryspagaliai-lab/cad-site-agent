UŽDUOTIS — įjungti HERA_DIFFRULES=1 (v2 pakopinis aktyvavimas, Žingsnis 2). NIEKO daugiau. <6 min.
NEleisk pytest. Fail-safe. €0. Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK.
Human-gate: taryba patvirtino (taip, 95.1%) + vartotojas „jungiam".

KONTEKSTAS: HERA_LOOPGUARD jau įjungtas /etc/cron.d/vps-agent. Dabar tuo pačiu mechanizmu įjungiam HERA_DIFFRULES=1
(EMG-lite post-hook — kaupia failure→success taisykles; fail-safe subshell || true; jau įpintas Fazėje 16).

ŽINGSNIAI:
1) BACKUP: `cp /etc/cron.d/vps-agent /root/hera-core-backup/vps-agent.cron.$(date +%s)`.
2) Pridėk `HERA_DIFFRULES=1` toje pačioje vietoje/formatu kaip HERA_LOOPGUARD=1 (VAR eilutė prieš */2 cron jobą). NEDUBLIUOK jei jau yra.
3) PATIKRA: `grep -c HERA_DIFFRULES /etc/cron.d/vps-agent` (turi būti 1, jokio dublio); `grep HERA_LOOPGUARD /etc/cron.d/vps-agent`
   (patvirtink kad LOOPGUARD irgi liko =1). cron.d auto-reload — restart nereikia.
4) Patvirtink kad /etc/cron.d/vps-agent sintaksė tvarkinga (formatas VAR=value eilutės + viena */2 cron eilutė).

ATASKAITA (HERA botas, trumpai): HERA_DIFFRULES=1 pridėtas OK (formatas); grep -c = 1; HERA_LOOPGUARD patvirtintas =1; backup kelias.
(Diffrules įsigalios kito task'o pabaigoje — post-hook nuskaitys sesijų istoriją, sukurs taisykles jei ras failure→success poras.)

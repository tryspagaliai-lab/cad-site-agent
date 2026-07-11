UŽDUOTIS — ĮDIEGTI ANTIGRAVITY `agy` CLI VPS'e (TIK diegimas; login interaktyvus, jį darys vartotojas). <12 min.
NEleisk pytest. Telegram TRUMPAI. NEbandyk interaktyvaus login (užkibtų) — tik įdiek + duok komandą vartotojui.

SAUGUMAS: raktų nespausdink/necommit'ink.

KONTEKSTAS: vartotojas nori PATS ištestuoti Antigravity prieš išvadą (galutinis vartas — jis). Tyrimas rodo:
`agy` = grynas Go CLI (github.com/google-antigravity/antigravity-cli), diegiasi į ~/.local/bin, login per
device-code flow (parodo Google URL + kodą, vartotojas patvirtina browser'yje telefone), free tier ~20 užklausų/d.

1) ĮDIEK `agy` CLI VPS'e oficialiu būdu (curl install script iš antigravity.google/docs ARBA GitHub release
   binaris Linux x86_64). Įsitikink kad PATH mato (~/.local/bin). Patikra: `agy version` arba `agy --help` -> veikia.
   Jei diegimas nepavyksta (404/nėra release) — aiškiai pažymėk ataskaitoje kas nepavyko, NEspėliok.

2) NEDARYK login (interaktyvus — device code). Ataskaitoje duok TIKSLIĄ Termius komandą vartotojui, pvz.:
   `agy login`  (arba tikslus login subkomandos pavadinimas iš `agy --help`).
   Aiškiai parašyk seką: paleidi -> agy parodo Google URL + kodą -> atsidarai URL telefone -> įvedi kodą ->
   prisijungi Google -> baigta. Sesija išsaugoma vietiškai.

3) PARUOŠK SMOKE TEST (bet NEpaleisk be login): sukurk /root/agy_smoke.sh su paprasta komanda (pvz.
   `agy` prompt'as „atsakyk vienu sakiniu: kas yra 2+2" ar analogiškas ne-interaktyvus iškvietimas pagal
   `agy --help` sintaksę). Vartotojas jį paleis PO login.

4) FAIL-SAFE laikui: jei diegimas užtrunka — atsiskaityk KĄ spėjai, NEUŽSTRIK iki 15 min.

5) DURABILUMAS: agy_smoke.sh + diegimo pastabos į /opt/cad-site-agent/n8n/ lokaliai (be push į viešą).
   HERA kodo neliesk.

TELEGRAM (trumpai, be raktų): (1) agy įdiegtas? (`agy version` rezultatas), (2) TIKSLI Termius login komanda +
seka vartotojui, (3) smoke test paruoštas (kaip paleisti po login), (4) „ANTIGRAVITY ĮDIEGTAS — LAUKIA LOGIN"
arba „DIEGIMAS NEPAVYKO — <priežastis>".

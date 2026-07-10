UŽDUOTIS — HERA PRAPLĖTIMAS: NORMATYVINIAI DOKUMENTAI -> DOKUMENTU APRIBOTI SKILL'AI (VARTOTOJAS PATVIRTINO DIEGIMĄ).
<15 min, fokusuotai. NEleisk viso pytest — tik taikinius testus. Atsiskaityk Telegram TRUMPAI.

SAUGUMAS: raktų nespausdink/necommit'ink/nerodyk.

KONTEKSTAS: vartotojas (galutinis vartas) patvirtino REALŲ diegimą — ne staged draft'ą. Idėja iš Superhuman AI
naujienlaiškio „PDF -> Claude skill" (2026-07-10), kuratoriaus (Claude) adaptacija HERA'i. Esmė: taisyklių/spec/
gairių dokumentai turi virsti SKILL'ais su „žinios apribotos šiuo dokumentu" saugikliu — tai kerpa epistemine
spragą (skill negali fantazuoti už šaltinio ribų).

DIEGIMAS (/opt/hera-processor/, minimalūs pakeitimai esamame kode):

1) SELEKTORIAUS MARŠRUTAS: pridėk trečią turinio tipą „normatyvinis dokumentas" (taisyklės, reglamentai,
   spec'ai, standartai, gairės — dažnai PDF, bet gali būti ir tekstas). Atpažinimo kriterijus selektoriaus
   prompt'e: dokumentas nurodo KAIP PRIVALOMA daryti / ko laikytis (ne „žinios apie pasaulį"). Toks turinys
   -> VISADA skill kandidatas (ne growth), su žyma document_bounded=true.

2) DOKUMENTU APRIBOTAS SKILL formatas (kai document_bounded=true):
   a) frontmatter: source_doc: <kelias į extracted šaltinį vault'e>, knowledge_scope: document_bounded,
      + įprastas tuple (intent, method, difficulty, tool_hint) ir triggers/raktažodžiai.
   b) skill kūne PRIVALOMA instrukcija: „Tavo žinios apribotos šaltinio dokumentu (source_doc). Taikyk TIK jame
      esančias taisykles. Jei klausimas/atvejis už dokumento ribų — atsakyk 'dokumente to nėra', NIEKO nespėliok."
   c) esamų skill'ų formato NEkeisk — tai papildomas potipis.

3) VAULT QUERY su GROUNDING'u: kai RAG atrenka document_bounded skill'ą, atsakymas generuojamas TIK iš source_doc
   turinio su citata/nuoroda į dokumentą; jei atsakymo dokumente nėra — atsakyk „dokumente to nėra" (ne bendras
   „nerandu"). Kitų (paprastų) skill'ų query elgsena NEKEIČIAMA.

4) GOVERNANCE NEKEISK: skill kandidatai kaip įprasta pereina selektorių+tarybą, status draft/human_gate lieka,
   NIEKADA auto-promote. Čia keičiasi tik maršrutas ir formatas, ne vartai.

5) TESTAS (greitas, be pilno suite):
   a) sintetinis mini dokumentas (pvz. 15 eilučių „Brėžinių sluoksnių standartas: sluoksnis X privalo...,
      draudžiama Y...") -> per selektorių: ar klasifikuota normatyviniu? ar skill turi source_doc + constraint?
   b) query testas: klausimas PAGAL dokumentą -> atsakymas su citata; klausimas UŽ dokumento ribų
      (pvz. „koks oras Vilniuje") -> „dokumente to nėra".
   c) regresija: vienas įprastas ingest/query kelias tebeveikia (galima ant esamo vault įrašo, be naujo LLM
      ištraukimo jei brangu).

6) DURABILUMAS: kodo kopija į /opt/cad-site-agent/n8n/hera/ IR push į PRIVATŲ tryspagaliai-lab/hera-core-backup
   (GITHUB_TOKEN iš env; PRIEŠ push — secret-scan kaip anksčiau). Į viešą repo push NEDARYK.

7) ŠALUTINĖ PATIKRA: ar ankstesnė užduotis (n8n Link Parser YT normalizacija, backup /root/linkparser_pre_ytfix.json)
   buvo įvykdyta? Jei NE — pažymėk ataskaitoje „LINKPARSER FIX NEĮVYKDYTAS", pats dabar nedaryk.

TELEGRAM (trumpai, be raktų): (1) selektoriaus maršrutas + skill formatas + grounded query įdiegti? (2) testų
a/b/c rezultatai, (3) backup push'intas į hera-core-backup? (4) linkparser fix įvykdytas anksčiau (taip/ne),
(5) „NORMATYVINIAI SKILL'AI ĮDIEGTI".

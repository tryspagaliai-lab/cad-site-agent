UŽDUOTIS — semsearch v1.2: boilerplate-chunk FILTRAS (+ jei reikia dok-mean derinys) + before/after 16 užklausų. <30 min.
Fail-safe: jei abejoji STOP+backup restore. NEleisk pytest. €0 (lokalu). Ataskaita TIK į HERA botą. Viešo cad-site-agent NELIESK (untracked + /opt/hera-processor).

KONTEKSTAS: v1.1 chunking davė MIŠRŲ rezultatą — sutvarkė ilgų dok. dilution (laimėjimai d/h/a/q4a), BET įnešė triukšmą:
trumpi boilerplate/frontmatter/„DRAFT—distiliuota"/antraščių chunk'ai gauna anomaliai aukštą balą nesusijusioms užklausoms →
regresijos c/q4b/q8/q2. v1.2 taiso tą triukšmą, IŠLAIKANT v1.1 laimėjimus.

ŽINGSNIAI:
1) BACKUP: cp hera_semsearch.py → /root/hera-core-backup/hera_semsearch.py.$(date +%s); state kopija.
2) MODIFIKUOK hera_semsearch.py (def 0 no-op išlieka; NELIESK council/kt.):
   PIRMINIS FIX — BOILERPLATE CHUNK FILTRAS prieš embeddinant (deterministinis, konservatyvus — NEmesk realaus turinio):
     - Išmesk YAML frontmatter blokus (--- ... ---).
     - Išmesk provenance/breadcrumb chunk'us: šablonai „DRAFT — distiliuota iš job", „source_job:", „STATUS:", HERA-WIKILINK blokus,
       „## Susiję" nuorodų sąrašus, grynų wiki-link'ų eilutes.
     - Išmesk chunk'us kurie tik antraštė (## X) be kūno, ARBA < ~12 prasmingų žodžių (po markdown nuvalymo).
     - Palik VISKĄ kas realus turinys. Jei dok. lieka 0 chunk'ų po filtro — fallback embeddink visą dok. kaip 1 chunk'ą (kad nedingtų).
   ANTRINIS (taikyk TIK jei filtras vienas nepakankamai lenkia v1.1) — SCORING DERINYS:
     dok_balas = 0.7*max_chunk + 0.3*mean(top-3 chunk) — kad vienas boilerplate peak nedominuotų. Reportuok ar taikei.
3) REBUILD; užrašyk chunk sk. (prieš/po filtro), RAM peak, laikas, index dydis.
4) SELFTEST (--selftest, be pytest): semantika + chunking-grupavimas + HERA_SEMSEARCH=0 no-op → PASS.
5) BEFORE/AFTER — paleisk VISAS 16 užklausų (top-1 + TAIKINIO RANK), palygink su TRIM taškais:
   v1(whole-doc) baseline + v1.1(chunking) + v1.2(dabar). Užklausos TOS PAČIOS 16 kaip v1.1 (test1 a-h + test2 q1-q8).
   YPAČ: ar IŠLAIKYTI v1.1 laimėjimai (d/h/a/q4a) IR ar PATAISYTOS v1.1 regresijos (c/q4b/q8/q2 grįžo į top-1/3)?
6) VERDIKTAS: ar v1.2 AIŠKIAI lenkia IR v1 (dilution) IR v1.1 (boilerplate)? Bendras HIT/PARTIAL/MISS skaičius vs abu.
   Jei v1.2 vis dar ne aiškiai geriau — pasakyk atvirai + ar rekomenduoji revert į v1 / palikti / v1.3.
7) BACKUP kodą /opt/hera-processor + commit/push; ROADMAP „semsearch v1.2 boilerplate-filter" pastaba.

ATASKAITA (HERA botas): chunk sk. prieš/po filtro; ar taikei scoring derinį; selftest; 16-query rank pokyčiai (ypač d/h/a/q4a IŠLAIKYTI? c/q4b/q8/q2 PATAISYTI?);
bendras HIT/PARTIAL/MISS v1 vs v1.1 vs v1.2; verdiktas (aiškiai geriau/ne); backup+ROADMAP. Jei STOP — kodėl+restore.

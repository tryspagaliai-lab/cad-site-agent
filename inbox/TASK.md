UŽDUOTIS — Loop B/C formuluotės sąžiningumo fix: „eviction" → „pasiūlyta (human-gate)". <6 min. NEleisk pytest.
Telegram TRUMPAI. Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Viešo NELIESK.

KONTEKSTAS: Loop B raportas rašo „🗑 N eviction" — skamba tarsi IŠTRINTA, nors realiai tik STAGED pasiūlymai
(proposals/…superseded-growth), laukiantys human-gate. Nieko nebuvo ištrinta (kiekiai stabilūs, failai egzistuoja).
Formuluotė klaidinanti — taisom kad būtų sąžininga (vartotojas jautrus melagingiems raportams).

1) hera_loopb.py: pakeisk eviction eilutės formuluotę iš „🗑 N eviction" į aiškią, pvz.:
   „🗑 N eviction PASIŪLYTA (human-gate, staged proposals/)" arba „🗑 N staged prune (human-gate)".
   Esmė: turi būti akivaizdu kad tai PASIŪLYMAS, ne įvykęs trynimas. Skaičiavimo logikos NEkeisk — tik tekstą.
2) Jei hera_loopc.py (ar consolidacijos raportas) irgi turi dviprasmiškų „eviction/prune" žodžių be „staged/
   human-gate" — pažymėk aiškiai kaip pasiūlymą (jis jau naudoja „STAGED" — patvirtink kad taip).
3) SANITY: paleisk Loop B raporto generavimą (arba dry) -> parodyk naują eilutę su „pasiūlyta/staged (human-gate)".
4) DURABILUMAS: kodas -> hera-core-backup. Atmintis: „loopB formuluotė — eviction→pasiūlyta(human-gate) 2026-07-13".

TELEGRAM (per HERA botą, trumpai): (1) Loop B „eviction" → „pasiūlyta (human-gate, staged)" — sąžininga formuluotė,
(2) skaičiavimo logika nekeista, (3) niekada nieko netrina auto (patvirtinta), (4) „RAPORTO FORMULUOTĖ SUTVARKYTA".

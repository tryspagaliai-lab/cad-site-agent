UŽDUOTIS — „future-gpu" track + standing rule + atgalinis tagavimas. <10 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. TIK privatus hera-vault. Viešo repo NELIESK. Kodo NELIESK. Necommit'ink raktų.

KONTEKSTAS: Vartotojas ateity turės GPU kompą. GPU/self-hosting turinys NEatmetamas — kaupiamas atskirai kaip
„paruošta ateičiai", kad nekemštų aktyvaus €0 žinyno, bet nedingtų. Vartotojas patvirtino track + standing rule +
atgalinį tagavimą.

1) SUKURK INDEKSĄ /opt/hera-vault/FUTURE_GPU.md:
   Antraštė + paaiškinimas: „Turinys reikalaujantis GPU / self-hosting — NETAIKOMA dabartiniam €0/no-GPU/4GB-VPS
   stack'ui, bet PARUOŠTA kai vartotojas turės GPU kompą. Neįtraukti į aktyvų planuotoją/gate/skills kol nėra GPU."
   Lentelė: failas · pavadinimas · kodėl-GPU · potenciali nauda su GPU.

2) PRIDĖK vLLM: rask growth „Native-speed vLLM transformers backend" (growth/2026-07-12-*wvmdi5*). Pažymėk
   frontmatter/pastaboje „hardware: future-gpu · STATUS: priimta į future-gpu track (human-gate 2026-07-12)".
   Įrašyk į FUTURE_GPU.md (nauda: paleisti bet kurį transformers modelį native vLLM greičiu su vienu flagu).

3) ATGALINIS TAGAVIMAS (deterministinis grep, be LLM): peržiūrėk growth/ ir skills/ ieškodamas GPU/self-hosting
   žymenų (case-insensitive): „GPU", „vLLM", „CUDA", „H100", „llama.cpp", „Ollama", „quantiz", „self-host",
   „lokal(us|ių) model", „EAGLE", „vllm", „tensor parallel". Kiekvienam radiniui (jei aiškiai GPU/self-hosting):
   pažymėk „hardware: future-gpu" ir įrašyk į FUTURE_GPU.md su viena eilute. NElimtink jau promote'intų įrašų
   statuso — tik PRIDEDI tagą + indekso eilutę (pvz. Agent OS lokalūs modeliai, jei toks yra). Jei abejotina
   (bendra kalba, ne reikalauja GPU) — NEtaguok. Parodyk kiek pažymėta.

4) STANDING RULE į docs/ROADMAP.md (ir jei yra vault CURATION/policy failas):
   „STANDING RULE (2026-07-12): GPU/self-hosting turinys → automatiškai į `future-gpu` track (tag hardware:future-gpu
   + FUTURE_GPU.md), NE atmesti. Aktyvus €0/no-GPU stack nesiūlo GPU dalykų kol nėra GPU. Peržiūrėti kai vartotojas
   turės GPU kompą."

5) TRAJEKTORIJA: įrašyk (curation/future-gpu-track-created + retro-tag N).

6) DURABILUMAS: vault commit („future-gpu track + standing rule + retro-tag GPU content") + push privatus
   hera-vault. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) FUTURE_GPU.md track sukurtas, (2) vLLM įdėtas (hardware:future-gpu),
(3) atgalinis tagavimas: N GPU įrašų pažymėta, (4) standing rule įrašyta (GPU turinys → track, ne atmesti),
(5) „FUTURE-GPU TRACK PARUOŠTA — GPU žinios kaupiamos tavo GPU dienai".

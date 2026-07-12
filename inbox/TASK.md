UŽDUOTIS — GPU auto-filer (hera_gpu_filter.py) + sutvarkyk GRASP. <16 min. NEleisk pytest. Telegram TRUMPAI.
Fail-safe €0. Kodas -> PRIVATUS hera-core-backup. Vault -> PRIVATUS hera-vault. Viešo repo NELIESK.
SAUGUMAS: raktų nespausdink/necommit'ink.

KONTEKSTAS: GPU/research turinys eina srautu (vLLM, APR, GRASP). Standing rule „GPU→future-gpu" yra popierinė —
tegul tampa AUTOMATINĖ. Deterministinis (BE LLM) filtras po ingesto rūšiuoja GPU turinį pats. NIEKO neatmeta/
neslepia — tik tag'ina + indeksuoja, palieka staged sėklos peržiūrai. Selektoriaus/gate balų NEliečia.

SUKURK /opt/hera-processor/hera_gpu_filter.py:
1) GPU_KEYWORDS — SPECIFINIS, kuruotas rinkinys (kad NEbūtų false-positive ant tekstinių metodų). STRONG žymenys:
   „GPU", „CUDA", „H100", „A100", „vLLM", „SGLang", „RadixAttention", „KV cache", „KV-cache", „tensor parallel",
   „pipeline parallel", „expert parallel", „world model", „BPTT", „backprop through", „llama.cpp", „Ollama",
   „RoPE", „FP8", „quantiz", „inference engine", „self-host", „8×H100", „diffusion model". VENK generinių („model",
   „training", „RL", „SFT" vieni) — jie NElaikomi signalu.
2) classify(text) -> {is_gpu: bool, matched: [...]}. Deterministinė taisyklė: is_gpu=True jei >=2 skirtingi STRONG
   žymenys ARBA >=1 „labai stiprus" (CUDA/H100/A100/vLLM/SGLang/KV cache/world model/BPTT/tensor parallel/llama.cpp/
   8×H100). Case-insensitive. Fail-safe: klaida -> is_gpu=False (ne crash).
3) file_if_gpu(note_path) -> jei is_gpu: pridėk „hardware: future-gpu" tag'ą į failą (jei dar nėra — idempotentiška)
   + append eilutę į /opt/hera-vault/FUTURE_GPU.md (jei dar ne). Grąžink sprendimą+matched. NIEKADA neatmeta/netrina/
   neslepia. Jei ne-GPU -> no-op (lieka aktyvus track).
4) HOOK: pridėk kvietimą dispatcher'yje/ingest'e PO to kai growth/skill įrašas parašytas -> file_if_gpu(new_note).
   Fail-safe: jei filtras klysta -> ingestas tęsiasi normaliai (no-op, ne blokas). Jei tiesioginis pipeline
   redagavimas rizikingas -> palik funkciją + batch-run režimą IR dokumentuok hook'ą (fail-safe pirmiau).
5) HERA_GPUFILTER jungiklis. Po demo (jei precision OK) -> ĮJUNK =1 gyvai, kad veiktų būsimiems ingestams.

DEMO (KRITINIS — įrodyk PRECISION, ne tik recall):
- GRASP (growth/2026-07-12-*8z2qmf*) -> turi būti is_gpu=True (world model/BPTT) -> tag + FUTURE_GPU.md. Parodyk matched.
- vLLM (growth *wvmdi5*) -> is_gpu=True, idempotentiška (be dublio).
- **SkillOpt (growth *lto8bb*) -> turi būti is_gpu=False** (tekstinis skill metodas, €0 — NEfile'inti! precision testas).
- Buzz/Warp (*aobwnm*) -> is_gpu=False.
Parodyk visų 4 sprendimus. Jei SkillOpt/Buzz gautų is_gpu=True -> SUGRIEŽTINK keywords ir pakartok (jokių false-
positive ant aktyvaus track'o).

GRASP: po demo jis jau future-gpu track'e (be sėklos — grynas world-model/GPU, nėra tekstinės-erdvės analogo).
Įrašyk FUTURE_GPU.md pastaboje „be taikomos sėklos".

BENCHMARK: hera_bench.run() -> turi likti 9/9 (naujas modulis + hook neturi gadinti). Jei kristų -> atšauk hook'ą.
ROADMAP: docs/ROADMAP.md „GPU auto-filer ĮDIEGTA 2026-07-12 — standing rule dabar automatinė (deterministinė)."
DURABILUMAS: kodas -> hera-core-backup; FUTURE_GPU.md+tag'ai+ROADMAP -> hera-vault. Viešo NELIESK.

TELEGRAM (per HERA botą, trumpai): (1) hera_gpu_filter.py įdiegta (deterministinis, HERA_GPUFILTER), (2) DEMO
precision: GRASP+vLLM→future-gpu, SkillOpt+Buzz→aktyvus (be false-positive), (3) filtras įjungtas gyvai —
GPU turinys rūšiuosis pats, (4) GRASP įdėta į future-gpu (be sėklos), benchmark 9/9, (5) „GPU AUTO-FILER GYVAS —
standing rule dabar automatinė".

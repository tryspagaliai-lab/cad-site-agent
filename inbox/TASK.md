UŽDUOTIS — ĮRAŠYTI VARTOTOJO STRATEGINĮ PROFILĮ Į VAULT + ĮTVIRTINTI AUTO-ATMINTIES TAISYKLĘ. <8 min.
NEleisk pytest. Telegram TRUMPAI. Šitas turinys PRIVATUS — tik privatus vault, jokio viešo repo.

SAUGUMAS: raktų nespausdink. Šis profilis JAUTRUS (asmeninė strategija) — jis lieka /opt/hera-vault (privatus,
sync į privatų hera-vault). Į modelius (Gemini/OpenAI) NEsiųsk jautrių dalių be atskiro sprendimo.

1) Sukurk /opt/hera-vault/profile/USER_STRATEGIC_PROFILE.md su šiuo turiniu (žmogaus pateiktas, autoritetingas —
   VIRŠESNIS už auto-generuotą PROFILE.md ties strategija):

   # Vartotojo strateginis profilis (žmogaus pateiktas, 2026-07-10)
   > Autoritetingas. Auto-generuotas PROFILE.md apibendrina turinį; ŠIS failas — tikri vartotojo tikslai. Konfliktui — šis viršesnis.

   ## Kas jis
   - Alias: cs. Vieta: London, UK (+ Lietuva). Kalbos: lietuvių (gimtoji), techninė anglų.
   - Rolė: AI SISTEMŲ DIZAINERIS / ORKESTRUOTOJAS — NE rankinis programuotojas. Stiprybė: diriguoti AI per specs,
     review, pipeline orkestravimą. Metodas: chat-Claude rašo specs -> Claude Code vykdo.
   - Fonas: architektūrinė vizualizacija (UK gyvenamoji ArchViz). PIEŠĖ pastatus (3ds Max/V-Ray), NE statė.
     NIEKADA nemaišyti su statybos darbais/normomis.

   ## Situacija (jautru)
   - NETEKO DARBO. Ieško: London creative-tech / AI automation (best fit: ACME, Accenture Song); Lietuvoje niša ribota.
   - TRŪKSTAMA KREDENCIALAS: portfolio darbas, įrodantis pipeline orkestravimą.

   ## Ką HERA jam reiškia (svarbiausia kryptis)
   - HERA / ClaudeAIOS = v2 perstatymas nuo nulio, tikslas 100x geriau nei v1, PLATI vizija, be senos architektūros rėmų.
   - HERA yra IR jo PORTFOLIO DARBAS — įrodo tą patį įgūdį, kurį parduoda (multi-model taryba+human gate,
     self-evolving pipeline, chat->Code orkestravimas). Padaryti ją PRISTATOMĄ = uždaro darbo paieškos spragą.
   - Domenas NIEKADA nesiaurinamas — nori plačiai protingos, save-tobulinančios sistemos, ne siauro įrankio.

   ## Tikrasis pranašumas (kur nukreipti save-tobulinimą -> pajamos)
   - 3D + AI: 3D Gaussian Splatting, point cloud, ComfyUI (ControlNet/SDXL, 16K ortofoto), Qwen-VL sklypų
     segmentacija, TouchDesigner. Video krauna kaip KURĄ save-tobulinimui; aukščiausios vertės kuras = jo sritis.
   - Niche scoring svoriai: time_to_revenue 0.30, domain_edge 0.25, willingness_to_pay 0.20,
     solo_laptop_feasibility 0.15, competition_inverse 0.10. -> reikia PAJAMŲ ir sverto, solo ant laptopo.
   - Mokosi: 3DGS, LoRA (Qwen2.5-VL zonų aptikimas), AI security (RAG poisoning, confused-deputy, Ed25519 skill signing).

   ## Infrastruktūra (jo)
   - Worker: Ubuntu 22.04 laptopas (Haswell, GeForce 840M, traktuojam kaip CPU-only). Receiver: Hetzner CX23 24/7.
   - Tinklas: Tailscale, Caddy/TLS tryspagaliai.com, Cloudflare tunnels. Stack: n8n 2.28.4, Telegram botai, MCP -> claude.ai,
     multi-model taryba (GLM/Mimo/Gemini/OpenAI) su žmogaus gate, Google Drive tiltas chat<->Code.

   ## Kaip su juo dirbti (kuratoriui — svarbu)
   - Jokių atsiprašymų, jokio „eik ilsėtis" pamokymų, jokio kartojimo to, ką jau žino. Konkretumas, ne vandenpylimas.
   - Jis diriguoja — pateik sprendimus/specs, ne ilgus aiškinimus. Lietuviškai.
   - VISADA persistink atmintį AUTOMATIŠKAI (žr. žemiau) — jam nereikia to prašyti.

2) AUTO-ATMINTIES TAISYKLĖ: pridėk į /opt/hera-vault/profile/USER_STRATEGIC_PROFILE.md pabaigą sekciją
   „## STANDING RULE — auto-memory" su tekstu: „Claude (Code ir chat) PRIVALO automatiškai, be atskiro prašymo,
   įrašyti į vault kiekvieną naują reikšmingą faktą apie vartotoją, jo tikslus, sprendimus ir sistemos pokyčius.
   Vartotojas neturi to prašyti kaskart." Ir tą pačią taisyklę įrašyk kaip 1 eilutę į docs handoff (jei VPS turi
   prieigą prie cad-site-agent repo docs — jei ne, praleisk, tik vault'e).

3) Push į privatų hera-vault iškart (arba leisk 30-min cron; jei gali — rankinis hera_vault_sync paleidimas).
   Į viešą repo NIEKADA.

TELEGRAM (trumpai, be raktų): (1) USER_STRATEGIC_PROFILE.md įrašytas + sync'intas, (2) auto-memory taisyklė
įtvirtinta, (3) „PROFILIS ĮRAŠYTAS Į ATMINTĮ".

# YouTube be reklamų: ką n8n gali, ko negali, ir kaip tai sprendžia kiti

## Trumpas atsakymas

**„n8n YouTube playerio, kuris skipina reklamas" padaryti negalima.** Ne dėl to,
kad sudėtinga — dėl to, kad n8n tam neturi nė vienos reikalingos dalies.

n8n yra serverinis workflow variklis. Jis pabunda nuo trigerio, paleidžia
nodus, užmiega. Jis:

- neturi video playerio,
- nemato tavo naršyklės DOM'o ir negali paspausti „Skip Ad",
- nesėdi tarp tavęs ir YouTube kaip proxy.

Reklamų skipinimas gyvai yra **kliento pusės** darbas — jis vyksta tame pačiame
puslapyje, kuriame sukasi video. n8n ten fiziškai nedalyvauja.

Yra ir apgaulingas variantas: n8n gali per Execute Command paleisti Playwright
ar Puppeteer, o tas headless Chrome nuspaus „Skip Ad". Tik tas video grosis
serveryje, ne tavo ekrane. Reklama praskipinta niekam. Tai ne sprendimas.

## Kaip šitą problemą realiai sprendžia žmonės

Trys atskiros stovyklos, priklausomai nuo to, kur žiūri.

### 1. Naršyklėje — plėtiniai

**uBlock Origin** blokuoja YouTube parduotas reklamas. Svarbus 2025–2026 m.
pokytis: Google Manifest V3 perėjimas išjungė pilną uBlock Origin stabiliame
Chrome nuo Chrome 138 (2025 m. liepa). Chrome lieka tik uBlock Origin **Lite** su
apkarpytu funkcionalumu. Pilna versija veikia **Firefox** (rekomenduojama) ir
Brave. Praktiškai tai reiškia: jei nori patikimo reklamų blokavimo, naršyklės
pasirinkimas nustojo būti skonio reikalas.

**SponsorBlock** sprendžia kitą problemą — rėmėjų intarpus („šį video remia…"),
kurie yra *pačiame video faile*. Jokia reklamblokė jų nepasieks, nes tai ne
reklama, o turinys. Timestampus sužymi bendruomenė. Švariam rezultatui reikia
**abiejų** įrankių; jie nedubliuoja vienas kito.

Katės ir pelės žaidimas realus: YouTube tikrina, ar užsikrovė reklamų skriptai,
ir rodo pop-up'ą, jei ne. Kai YouTube ką nors pakeičia, dieną kitą matai
reklamas, kol atsinaujina filtrai.

### 2. Telefone — ReVanced

Android'e dominuojantis būdas yra **ReVanced** — oficialaus YouTube APK
patch'inimas. Išmeta reklamas ir atrakina Premium funkcijas: SponsorBlock,
grojimą fone, atsisiuntimus. Aktyviai vystomas (v21.02.32, 2026 m. sausis).

Kaina: reikia sideload'inti, o YouTube sąmoningai leidžia app'o atnaujinimus,
kurie laužo patch'us — kartais tenka perinstaliuoti kas savaitę. iOS šito
lygio sprendimo neturi.

### 3. Serveryje — parsisiuntimas į vietinę biblioteką

Čia įdomiausia dalis ir vienintelė, kur automatizacija apskritai turi prasmę.
**Kai video parsisiunčiamas tiesiogiai per yt-dlp, YouTube reklamų ten
paprasčiausiai nėra** — jos niekada nebūna video sraute, jas prilipdo playeris
atkūrimo metu. Tai ne triukas, o šalutinis efektas. O `--sponsorblock-remove`
papildomai iškerpa rėmėjų intarpus.

Ir čia svarbiausias radinys: **dauguma žmonių šito nedaro n8n'e.** Tam yra
specializuoti self-hosted įrankiai:

| Įrankis | Kas tai |
|---|---|
| **Pinchflat** | Paprasčiausias. Nurodai kanalus/playlistus, jis periodiškai tikrina ir siunčia. SponsorBlock integracija, first-class palaikymas Plex / Jellyfin / Kodi. Vienas konteineris. |
| **TubeArchivist** | Galingesnis, su savo web UI kolekcijai naršyti. Reikia Redis + Elasticsearch, tad sunkesnis. Turi Jellyfin pluginą su metaduomenimis ir žiūrėjimo progresu. |

Jei tavo tikslas yra tiesiog „turėti švarią biblioteką", **Pinchflat padarys tai
geriau nei bet koks n8n workflow'as** — jis būtent tam ir parašytas, turi kanalų
prenumeratas, taisyklių sistemą ir net galimybę po kurio laiko perparsiųsti video,
kad pasiimtų šviežesnius SponsorBlock žymėjimus.

**Kada tada n8n?** Kai parsiuntimas yra tik vienas žingsnis ilgesnėje grandinėje,
kurios Pinchflat nedaro: transkribuoti į Whisper, paduoti LLM'ui santraukos,
įrašyti į Notion, nusiųsti į Telegram, sujungti su kitomis tavo automatizacijomis.
Tada `youtube-sponsorfree-library.json` yra tinkamas startas — jį lengva pratęsti.
Jei tavo scenarijus yra grynas archyvavimas, imk Pinchflat ir nekurk nieko.

## Šitame kataloge esantis workflow'as

```
New video on channel (RSS) ┐
                           ├─→ Build yt-dlp job → yt-dlp + SponsorBlock → Downloaded? ─┬─→ Ready in library
Run manually ──────────────┘                                                           └─→ Failed
```

1. **RSS trigeris** kas 15 min tikrina kanalo feed'ą
   (`https://www.youtube.com/feeds/videos.xml?channel_id=...` — oficialus, be API rakto).
2. **Build yt-dlp job** (Code node) ištraukia video ID ir sukonstruoja komandą.
   Visi nustatymai yra šio node viršuje.
3. **yt-dlp + SponsorBlock** parsiunčia ir iškerpa rėmėjų segmentus.
4. Rezultatas: `/data/youtube/<Kanalas>/<data> - <pavadinimas> [id].mkv`.

`--download-archive` užtikrina, kad tas pats video nebūtų siunčiamas antrą kartą.

### Saugumo detalė, kurios nepraleisk

RSS feed'as yra išorinis, nepatikimas įvedimas, o jis keliauja į shell komandą.
Code node priima **tik** kanoninį 11 simbolių YouTube ID (`[A-Za-z0-9_-]{11}`)
ir URL susikonstruoja iš naujo — feed'o eilutė į komandą nepatenka niekada.
Pavadinimai į shell'ą apskritai nekeliauja. Jei redaguosi tą node, neišmesk
`q()` funkcijos ir ID regex'o.

## Paleidimas

**1. Execute Command node.** Nuo **n8n 2.0 jis išjungtas pagal nutylėjimą** dėl
saugumo — leidžia bet kam, kas gali redaguoti workflow'us, paleisti komandas tavo
serveryje. Įjungiama per `NODES_EXCLUDE=[]`. Bendruomenėje netrūksta pranešimų,
kad tai suveikia ne iš pirmo karto, tad pasitikrink, ar node atsirado sąraše.

> **n8n Cloud šito node neturi visai.** Jei sukiesi Cloud'e, šis workflow'as
> tau neveiks — reikia self-hosted.

**2. yt-dlp ir ffmpeg.** Standartiniame image jų nėra. Du keliai:

- `Dockerfile.n8n-ytdlp` šiame kataloge — yt-dlp atskirame venv, atnaujinamas
  nepriklausomai nuo n8n.
- Bendruomenės node **`n8n-nodes-youtube-dl`** — pats parsisiunčia yt-dlp binarą
  instaliacijos metu ir susitvarko su Alpine/musl nesuderinamumu per LD_PRELOAD
  shim'ą, tad jokio custom Dockerfile nereikia. Patogesnis startas, bet jis yra
  apvalkalas su savo parametrais, ir SponsorBlock vėliavėlių jo aprašyme nėra —
  jeigu segmentų kirpimas tau esminis, lik prie Execute Command.

```bash
cd n8n && docker build -f Dockerfile.n8n-ytdlp -t n8n-ytdlp .
```

```yaml
services:
  n8n:
    image: n8n-ytdlp
    ports: ["5678:5678"]
    environment:
      - NODES_EXCLUDE=[]
    volumes:
      - ./n8n-data:/home/node/.n8n
      - /srv/media/youtube:/data/youtube   # turi sutapti su OUTPUT_DIR
```

**3. Importuok** `youtube-sponsorfree-library.json` (Workflows → Import from File).

**4. Pakeisk `channel_id`** RSS node'e — rasi kanalo puslapio šaltinyje, ieškok
`externalId`. Playlist'ui: `?playlist_id=...`.

**5. Pasitikrink rankomis:** įrašyk `MANUAL_URL` Code node viršuje, paspausk
Execute. Kai suveiks — išvalyk ir įjunk RSS trigerį.

## Kur tai lūžta

**Bot detekcija — didžiausia praktinė problema.** YouTube agresyviai blokuoja
datacentrų IP. Skirtumas esminis:

- **Namų serveris / NAS** (rezidencinis IP) — dažniausiai veikia be nieko.
- **VPS, AWS, Hetzner ir pan.** — beveik garantuotai gausi
  „Sign in to confirm you're not a bot". Reikės `COOKIES_FILE`: eksportuoti
  cookies iš prisijungusios naršyklės Netscape formatu. Ir tai ne vienkartinis
  darbas — YouTube naikina sesijas greičiau, kai mato jas iš datacentro.

Todėl Code node'e pagal nutylėjimą įjungtas `--sleep-interval 3`. Jei vis tiek
riboja — mažink lygiagretumą iki vieno parsiuntimo vienu metu. Rimtesnis
sprendimas yra rezidenciniai proxy, bet tai jau kita kainų ir moralės kategorija;
namų serveris paprastesnis ir pigesnis.

**Pasenęs yt-dlp.** YouTube keičia playerį, yt-dlp taisosi per dienas.
Perbuild'ink image arba:

```bash
docker exec -u root <container> /opt/ytdlp/bin/pip install -U yt-dlp
```

Verta pasidaryti atskirą n8n Schedule workflow'ą, kuris tai daro kas savaitę.

**Derinimas.** `REMOVE_SEGMENTS = true` fiziškai iškerpa segmentus; su
`--force-keyframes-at-cuts` pjūviai švarūs, bet aplink juos perkoduojama, tad
lėčiau. Nori greičio — `false`, ir segmentai liks kaip chapter'iai, kuriuos mpv
ar Jellyfin praleis pats. Kategorijose `sponsor,selfpromo` yra saugus minimumas;
`intro,outro,preview,music_offtopic` kartais nukerpa daugiau, nei norėtum.

## Dėl taisyklių

Be pamokslo: **YouTube ToS draudžia ir reklamų apėjimą, ir video atsisiuntimą.**
Praktikoje uBlock Origin, SponsorBlock ir yt-dlp yra plačiai naudojami įrankiai
asmeniniam naudojimui. ReVanced atveju rizika šiek tiek konkretesnė — tai
modifikuotas APK, ir paskyrų blokavimų būta, nors reti.

Nustatyk lūkesčius teisingai: visi šie sprendimai periodiškai lūžinės, nes
kitoje pusėje sėdi komanda, kuriai mokama, kad jie lūžtų. Jei žiūri daug ir nori,
kad kūrėjai gautų pinigų, Premium yra vienintelis variantas, kuris ir be reklamų,
ir palaikomas. Šitas workflow'as tinka kitam scenarijui — offline archyvui to,
ką ir taip žiūri.

## Failai

| Failas | Kas tai |
|---|---|
| `youtube-sponsorfree-library.json` | n8n workflow'as, importuojamas |
| `Dockerfile.n8n-ytdlp` | n8n image su yt-dlp ir ffmpeg |

## Šaltiniai

- [uBlock Origin](https://ublockorigin.com/) · [uBlock Origin ir Chrome MV3](https://www.ghostery.com/blog/ublock-origin-not-supported-chrome) · [kas dar veikia 2026](https://adblock-tester.com/ad-blockers/youtube-ad-blockers-that-still-work-in-2025/)
- [SponsorBlock](https://github.com/ajayyy/sponsorblock/wiki/Android) · [ReVanced](https://revanced.net/)
- [Pinchflat](https://github.com/kieraneglin/pinchflat) · [TubeArchivist + Jellyfin apžvalga](https://www.xda-developers.com/this-app-turned-my-jellyfin-server-into-a-youtube-archive/)
- [n8n Execute Command dokumentacija](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executecommand) · [n8n 2.0 issue #23439](https://github.com/n8n-io/n8n/issues/23439)
- [n8n-nodes-youtube-dl](https://github.com/prakashmaheshwaran/n8n-nodes-youtube-dl)
- [yt-dlp bot detekcija](https://github.com/yt-dlp/yt-dlp/issues/12264) · [cookies 2026](https://dev.to/osovsky/6-ways-to-get-youtube-cookies-for-yt-dlp-in-2026-only-1-works-2cnb)

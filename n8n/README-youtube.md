# YouTube be reklamų: ką n8n gali ir ko negali

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

## Ką daryti norint žiūrėti be reklamų (gyvai, naršyklėje)

Tai sprendžia ne automatizacija, o įrankis kliento pusėje:

| Ką nori | Ką naudoti |
|---|---|
| YouTube įterptos reklamos (pre-roll, mid-roll) | **uBlock Origin** (Firefox); arba **YouTube Premium**, jei nori mokėti |
| Rėmėjų intarpai pačiame video („šį video remia NordVPN…") | **SponsorBlock** — bendruomenės sužymėti timestampai, praleidžiami automatiškai |
| Atskiras player'is, į kurį reklamos net neateina | **mpv + yt-dlp**, **FreeTube** (desktop), **NewPipe** (Android) |

Svarbus niuansas, kurį verta suprasti: **uBlock ir SponsorBlock sprendžia
skirtingas problemas.** uBlock blokuoja YouTube parduotas reklamas. SponsorBlock
kerpa rėmėjų intarpus, kurie yra *pačiame video faile* — jokia reklamblokė jų
nepasieks. Visiškai švariam rezultatui reikia abiejų.

Ir dar vienas: kai video parsisiunčiamas tiesiogiai (yt-dlp), **YouTube reklamų
ten paprasčiausiai nėra** — jos niekada nebūna video sraute, jas prilipdo
playeris atkūrimo metu. Todėl atsisiųstas failas be reklamų yra ne triukas, o
šalutinis efektas.

## Ką n8n čia realiai gali

n8n vieta yra ne playeris, o **automatika aplink jį**: sekti kanalus ir
sudėlioti švarią, jau apkarpytą biblioteką, kurią po to žiūri kuo nori — Jellyfin,
Plex, mpv, telefonas.

Būtent tai daro `youtube-sponsorfree-library.json`:

```
New video on channel (RSS) ┐
                           ├─→ Build yt-dlp job → yt-dlp + SponsorBlock → Downloaded? ─┬─→ Ready in library
Run manually ──────────────┘                                                           └─→ Failed
```

1. **RSS trigeris** kas 15 min tikrina YouTube kanalo feed'ą
   (`https://www.youtube.com/feeds/videos.xml?channel_id=...` — oficialus, be API rakto).
2. **Build yt-dlp job** (Code node) ištraukia video ID ir sukonstruoja komandą.
   Visi nustatymai — katalogas, kokybė, SponsorBlock kategorijos — yra šio node
   viršuje.
3. **yt-dlp + SponsorBlock** parsiunčia video ir iškerpa rėmėjų segmentus.
4. Rezultatas nukeliauja į `/data/youtube/<Kanalas>/<data> - <pavadinimas> [id].mkv`.

`--download-archive` užtikrina, kad tas pats video nebūtų siunčiamas antrą kartą,
tad trigeris gali suktis nuolat.

### Saugumo detalė, kurios nepraleisk

RSS feed'as yra išorinis, nepatikimas įvedimas, o jis keliauja į shell komandą.
Code node priima **tik** kanoninį 11 simbolių YouTube ID (`[A-Za-z0-9_-]{11}`)
ir URL susikonstruoja iš naujo — feed'o eilutė į komandą nepatenka niekada.
Pavadinimai į shell'ą apskritai nekeliauja. Jei kada redaguosi tą node,
neišmesk `q()` funkcijos ir ID regex'o.

## Paleidimas

**1. n8n su yt-dlp.** Standartiniame image nei yt-dlp, nei ffmpeg nėra, o
Execute Command sukasi konteineryje:

```bash
cd n8n
docker build -f Dockerfile.n8n-ytdlp -t n8n-ytdlp .
```

```yaml
# docker-compose.yml
services:
  n8n:
    image: n8n-ytdlp
    ports: ["5678:5678"]
    environment:
      # Execute Command node pagal nutylėjimą išjungtas naujose versijose
      - NODES_EXCLUDE=[]
    volumes:
      - ./n8n-data:/home/node/.n8n
      - /srv/media/youtube:/data/youtube   # turi sutapti su OUTPUT_DIR
```

**2. Importuok** `youtube-sponsorfree-library.json` (n8n → Workflows → Import from File).

**3. Pakeisk `channel_id`** RSS node'e. Jį rasi kanalo puslapio šaltinyje —
ieškok `externalId`. Playlist'ui naudok `?playlist_id=...`.

**4. Pasitikrink rankomis:** įrašyk `MANUAL_URL` reikšmę Code node viršuje ir
paspausk Execute. Kai suveiks — išvalyk ir įjunk RSS trigerį.

### Derinimas

`REMOVE_SEGMENTS = true` fiziškai iškerpa segmentus. Su
`--force-keyframes-at-cuts` pjūviai švarūs, bet aplink juos vyksta perkodavimas,
tad lėčiau. Jei nori greičio — nustatyk `false`: segmentai bus įrašyti kaip
skyriai (chapters), o mpv ar Jellyfin juos praleis pats.

Kategorijas rinkis pagal skonį. `sponsor,selfpromo` yra saugus minimumas;
`intro,outro,preview,music_offtopic` kartais nukerpa daugiau, nei norėtum.

### Kai nustos veikti

Beveik visada priežastis viena: **yt-dlp paseno.** YouTube keičia playerį, o
yt-dlp taisosi per dienas. Perbuild'ink image arba:

```bash
docker exec -u root <container> /opt/ytdlp/bin/pip install -U yt-dlp
```

Verta pasidaryti atskirą n8n Schedule workflow, kuris tai daro kas savaitę.

## Dėl taisyklių

Blunt'as, be pamokslo: **YouTube naudojimosi sąlygos draudžia ir reklamų
apėjimą, ir video atsisiuntimą** be jų leidimo. Praktikoje uBlock Origin ir
SponsorBlock yra plačiai naudojami, legalūs įrankiai asmeniniam naudojimui, o
yt-dlp — irgi. Bet nustatyk lūkesčius teisingai: tai ToS pažeidimas, YouTube
periodiškai bando su tuo kovoti, ir šitas workflow'as *lūžinės*.

Jei kanalus žiūri daug ir nori, kad kūrėjai gautų pinigų — Premium yra vienintelis
variantas, kuris ir be reklamų, ir palaikomas. Šitas workflow'as tinka kitam
scenarijui: susikurti offline archyvą to, ką ir taip žiūri.

## Failai

| Failas | Kas tai |
|---|---|
| `youtube-sponsorfree-library.json` | n8n workflow'as, importuojamas |
| `Dockerfile.n8n-ytdlp` | n8n image su yt-dlp ir ffmpeg |

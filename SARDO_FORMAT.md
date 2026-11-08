# Sardo-format (vast) — 1080 × 1920, 9:16

Gebaseerd op de "Last Shot Media"-layout (`_reference/format/last-shot-media-format.png`).
Elke Sardo-video volgt dit format, tenzij Peter in de chat iets anders zegt.

```
 y=0    ┌──────────────────────────────┐
        │                              │
        │      ┌ ─ ─ ─ ─ ─ ┐  ← hoofd │   ZONE 1 — PETER (rood)
 y≈534  │ - - -  ogen  - - - - - - - - │   0 – 960
        │      └ ─ ─ ─ ─ ─ ┘           │
 y=960  ├──────────────●───────────────┤   ● ANKERPUNT (hook-tekst / CTA)
        │   C A P T I O N S            │   ZONE 2 — CAPTIONS (blauw)
 y=1190 ├──────────────────────┐───────┤   970 – 1190
        │                      │       │
        │     BEELD-ZONE (gecentreerd) │   ZONE 3 — BEELD (groen)
        │     screenshots, foto's,     │   1205 – 1905, kaart 846 px
        │     animaties, video-in-video│   breed, midden x = 540
        │                              │
 y=1920 └──────────────────────┴───────┘
```

## Zones in pixels

| Zone | y | x | Inhoud |
|---|---|---|---|
| 1 Peter | 0 – 960 | 0 – 1080 | Gezicht. **Ogen op y ≈ 534** (stippellijn). Hoofd binnen x 350 – 730, y 207 – 766. |
| Ankerpunt ● | midden y = 960 | midden x = 540 | Hook-tekst (eerste ~2 s) en CTA-woord (laatste 2 s). Gecentreerd op de naad. |
| 2 Captions | 970 – 1190 | 40 – 1040 | 2–4 woorden, Poppins 800, ~78 px, wit + donkere rand, actief woord oranje. |
| 3 Beeld | 1205 – 1905 | gecentreerd, kaart 846 px breed (x 117 – 963) | Screenshots, foto's, animaties, video-in-video. **Horizontaal gecentreerd** (Peter, 8 nov 2026: links uitlijnen oogt "off"). Niets belangrijks in de laatste ~15 % rechts of onderin. |

## Twee modes voor Peter

- **SPLIT** (standaard als er beeld is): Peter in zone 1 (crop `object-fit: cover` naar 1080×960, positie zo dat de ogen op y≈534 staan), beeld in zone 3.
- **FULL** (als er op dat moment geen beeld is): Peter vult het hele frame (1080×1920), ogen nog steeds op y≈534 → zelfde gezichtspositie, dus geen sprong. Captions blijven in zone 2.
- Wissel SPLIT ↔ FULL op een cut of met een korte slide (0,25 s, `expo.inOut`) van het beeldvak. Animeer altijd de **wrapper**, nooit de `<video>`.

## Bronbeeld

Peter filmt 4K, 25 fps. Check met `ffprobe` of het staand (2160×3840) of liggend is.
- Staand → schaal naar 1080 breed; positioneer verticaal zodat de ogen op y≈534 staan.
- Liggend → crop naar het gezicht (cover), zelfde regel.
Zoek de ooghoogte één keer op met een still (frame bij ~1 s) en noteer de offset in het project.

## Tekst in beeld

- Hook-tekst: max 6 woorden, Poppins 800, ~96 px, wit met oranje accentwoord, op het ankerpunt.
- "Tekst in beeld" uit het concept: als kaart/label in de beeld-zone (zone 3) op het moment dat Peter het zegt.
- CTA: laatste 2 s, `CHECK` of `AANBOD`, groot (~150 px), oranje, op het ankerpunt, met kleine regel erboven "Reageer".

## Beeld-zone (zone 3)

- Kaarten en beelden **horizontaal gecentreerd** (midden x = 540, kaart 846 px breed). Niet links uitlijnen — dat oogt scheef (Peter, 8 nov 2026).
- Laat zien wat Peter zegt: bedragen, stappen, het huis, de meterkast, een lijstje, een tijdlijn.
- Animaties maakt Claude zelf in merkkleuren (bv. €225 ➜ €120, label F ➜ B, jaar 1 ➜ 5, 3 stappen, budgetkaarten €5k / €15k / €40k).
- Foto's/screenshots/B-roll levert Peter aan in de raw-map. Ontbreekt iets? Animatie maken of vragen.
- Achtergrond van kaarten: `--brand-bg` met afgeronde hoeken (24 px), padding 40 px.
- Geen tekst in de onderste ~120 px (y > 1800): daar komt de Instagram-caption overheen.

## Uitzondering: Yapping-video's

Bij yapping (tip/verhaal/mening) geldt de beeld-zone NIET. Peter staat de hele video FULL in beeld, captions + hook + CTA onder de kin (midden y≈1285), losse icoontjes horizontaal gecentreerd in y 1400–1790. Zie `templates/sardo-yapping/README.md`.

## Nummers uniek
Dagnummer (D) en Funda Fixer-volgnummer (#) staan in `video-projects/NUMMERS.md`. Altijd eerst pullen, je nummer claimen, committen en pushen vóór je bouwt. Nooit een nummer hergebruiken; bij botsing het volgende vrije nummer nemen. Peter wil dat parallelle chats elkaar niet overschrijven (8 nov 2026).

## Knippen: techniek (les uit D16, 8 nov 2026)
- Knippunten uit een los uitgepakt audiobestand (ogg/wav van de DJI-clip) lopen ~0,14% achter op de MP4-tijd (0,35 s na 5 min). Bepaal ze op de MP4 zelf of corrigeer: kruiscorrelatie van een paar geknipte stukken tegen de bron, lineair fitten.
- Knippen met input-seek: `ffmpeg -ss <start> -i bron -t <duur> ... -af aresample=48000,asetpts=PTS-STARTPTS,afade=t=out:st=<duur-0.04>:d=0.04`. NIET `-ss start-1 -i … -ss 1` met een afade: dan valt de fade-out ~1 s te vroeg en wordt het zinseinde stil.
- Controle: elk stuk los transcriberen (met `apad` erachter) en checken dat de laatste woorden erin zitten, en het dB-niveau van de laatste 0,8 s bekijken (geen -180 dB = digitale stilte).

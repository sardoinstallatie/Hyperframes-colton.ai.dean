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
        │   BEELD-ZONE         │ leeg  │   ZONE 3 — BEELD (groen)
        │   screenshots, foto's│ (IG-  │   1205 – 1905, x 0 – 918
        │   animaties, video-  │ knop- │
        │   in-video           │ pen)  │
 y=1920 └──────────────────────┴───────┘
```

## Zones in pixels

| Zone | y | x | Inhoud |
|---|---|---|---|
| 1 Peter | 0 – 960 | 0 – 1080 | Gezicht. **Ogen op y ≈ 534** (stippellijn). Hoofd binnen x 350 – 730, y 207 – 766. |
| Ankerpunt ● | midden y = 960 | midden x = 540 | Hook-tekst (eerste ~2 s) en CTA-woord (laatste 2 s). Gecentreerd op de naad. |
| 2 Captions | 970 – 1190 | 40 – 1040 | 2–4 woorden, Poppins 800, ~78 px, wit + donkere rand, actief woord oranje. |
| 3 Beeld | 1205 – 1905 | 0 – 918 | Screenshots, foto's, animaties, video-in-video. Rechts (x > 918) leeg. |

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

- Laat zien wat Peter zegt: bedragen, stappen, het huis, de meterkast, een lijstje, een tijdlijn.
- Animaties maakt Claude zelf in merkkleuren (bv. €225 ➜ €120, label F ➜ B, jaar 1 ➜ 5, 3 stappen, budgetkaarten €5k / €15k / €40k).
- Foto's/screenshots/B-roll levert Peter aan in de raw-map. Ontbreekt iets? Animatie maken of vragen.
- Achtergrond van kaarten: `--brand-bg` met afgeronde hoeken (24 px), padding 40 px.
- Geen tekst in de onderste ~120 px (y > 1800): daar komt de Instagram-caption overheen.

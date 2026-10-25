# Sardo yapping-template (vast sinds 25-10-2026, goedgekeurd door Peter)

Voor **Yapping**-video's (tip/verhaal/mening, praten in de camera). Referentie: `video-projects/2026-10-25-yapping-0093`.

## De look (niet van afwijken)
- **Peter FULL in beeld, de hele video.** Geen grijs vlak, geen kaart, beeld niet halveren. Rauw.
- Face: ogen op y≈534. Ooghoogte meten op een still → `faceOffsetY = 534 - oog_y`, `transform-origin: 540px <oog_y>px`, basis-zoom **1,21** (vult tot onderin), punch-in **1,33** op cuts (elke ≥3 s).
- **Captions onder de kin**: `#captions { top: 1185px; height: 200px }` (midden y≈1285). Nooit over het gezicht.
- **Hook (eerste 2 s) en CTA (laatste 2 s)** op dezelfde hoogte: `.anchor-text { top: 1285px }`.
- **Icoontjes los over het beeld**, horizontaal gecentreerd (flex, `justify-content: center`) in y 1400–1790, met drop-shadow. Icoon 250 px + kort woordje (62 px, wit + rand, accent oranje). Twee opties: 2 icoontjes + "of". Stappen: 3 kleine icoontjes naast elkaar.
- Icoon staat er alleen 2–5 s, op het moment dat Peter het zegt. Geen icoon tijdens de CTA.
- Zachte pop (volume 0,18) bij elk icoon. Geen muziek.
- Captions: max 3 woorden / 19 tekens, nieuwe chunk na leesteken, losse korte woordjes ("de", "een") aan het volgende plakken, lange woorden kleiner.

## Werkwijze
1. Clip ophalen + transcriberen (zie `/sardo-edit`). Stiltes: `ffmpeg -i raw/source.mp4 -af silencedetect=noise=-38dB:d=0.2 -f null -` → `work/sil.txt` (start eind per regel).
2. `cp templates/sardo-yapping/cut.py templates/sardo-yapping/build.py video-projects/<slug>/`
3. `cut.py`: alleen `KEEP` (ruwe tijden) aanpassen → `work/full.mp4` + `work/edl.json`. Transcribeer `work/full.mp4` → `work/transcript.json`.
4. `build.py`: pas aan → `FIX` (transcript-fouten), `SCENES` (tijden in de geknipte video), hook-tekst, CTA-woord, `faceOffsetY` + transform-origin. Icoon-bibliotheek in `SVG` (huis, sneeuw, ketel, thermostaat, radiator, lek, bloem, warmtepomp, vink …). Nieuwe icoontjes in dezelfde stijl tekenen: wit lijnwerk 12–14 px, oranje accent, #2e2e37 vulling.
5. `python3 build.py` → map `A/` → lint → `npx hyperframes snapshot A --at …` → 3 stills naar Peter → render.

## Renderen
`render.sh` (in de projectmap, NIET in `A/` — build.py wist `A/`). Start los: `(setsid nohup bash render.sh > /dev/null 2>&1 &)` en wacht in aparte commando's; anders wordt de render afgebroken. ±7 min voor 49 s.
- Hook-tekst verdwijnt op 1,86 s; captions pas vanaf 1,95 s (anders 2–3 frames overlap).

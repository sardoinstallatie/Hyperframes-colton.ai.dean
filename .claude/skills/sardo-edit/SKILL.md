---
name: sardo-edit
description: Edit one of Peter's (Sardo | Verduurzaming) raw recordings into finished Instagram Reels — one version per recorded hook (A/B/C) with an identical body — in the fixed Sardo format, and deliver them to his Mac. Use at the start of every chat in the "CONTENT: Short-Form editor" project, or whenever Peter names raw clips plus a video concept to edit.
---

# Sardo edit — van ruwe opname naar 3 hook-versies

Dit is de vaste werkwijze voor elke chat in het project **"CONTENT: Short-Form editor"**.
Peter geeft per chat: **welke clips** (bestandsnamen in de raw-map) en **het concept** (meestal een blok uit het draaiboek: dag, onderwerp, CTA, hooks A/B/C, script, tekst in beeld).

Lees eerst: `CREATOR.md`, `PREFERENCES.md`, `SARDO_FORMAT.md`. Gebruik daarna de `/hyperframes` en `/short-form-video` skills voor de bouwregels (render contract, captions, wrapper-animatie). Waar die skills botsen met Sardo-regels, winnen de Sardo-regels.

## 0. Sessie-start (elke nieuwe chat)

```bash
cd /home/claude/hyperframes-colton.ai.dean   # of waar de fork gecloned is
source scripts/sardo-session-setup.sh
```
Mac-koppeling checken: `get_device_info` → staat `/Users/peter/Documents` in `connectedFolders`? Zo niet: `device_request_folder_access` voor `~/Documents`. Lukt dat niet → zeg het meteen.

## 1. Brief checken (vóór je iets knipt)

Vat in 3–5 regels samen wat je gaat maken: dag/onderwerp, CTA-woord, hooks, welke clips.
Meld meteen:
- `[vul in]` of ontbrekende bedragen → vragen, nooit verzinnen.
- Tijdgevoelige claims (bv. "Nog 64 dagen" → klopt alleen op één postdatum; subsidiebedragen → rvo.nl checken; "label F naar B" alleen als berekend).
- Clip niet gevonden in de raw-map.
Is alles duidelijk? Ga direct door, niet wachten.

## 2. Clips ophalen

Raw-map op de Mac: `/Users/peter/Documents/videos/raw/` (device_bash: `$HOME/mnt/Documents/videos/raw/`).
- Lijst met `device_list_dir`. Haal de genoemde clips op met `device_stage_files` (komen in `/mnt/user-data/uploads/Documents/...`).
- **Transfer is traag (getest D09):** stage/commit lukt alleen betrouwbaar met stukken van ±8 MB, 1–2 per call. Werkwijze: op de Mac alleen de benodigde tijd-ranges coderen (`ffmpeg -ss <start> -t <duur> … -vf scale=1080:-2 -preset ultrafast -crf 19`, 2 tegelijk binnen één device_bash-call — achtergrondprocessen overleven de call niet), dan `split -b 8000000`, stagen, in de cloud `cat` terug. Terugleveren net zo: `split -b 8000000` → commit naar `_sardo-tmp/out/` → `cat` op de Mac naar de eindmap.
- Grote bestanden (4K): eerst op de Mac verkleinen kan sneller — als `ffmpeg` daar bestaat (`device_bash: which ffmpeg`): naar 1080 breed H.264 CRF 18, dan pas stagen.
- Maak project: `video-projects/<opnamedatum>-d<dag>-<onderwerp>/` met `npx hyperframes init`, kopieer `assets/brand-tokens.css` en `assets/fonts/` erin.
- Re-encode bron: `ffmpeg -i raw.mov -c:v libx264 -preset veryfast -crf 18 -r 25 -c:a aac -b:a 192k -movflags +faststart assets/source.mp4`

## 3. Transcriberen en indelen

```bash
npx hyperframes transcribe assets/source.mp4 --engine parakeet --language nl --json
```
Zoek in het transcript (vergelijk met de hooks en het script uit de brief):
- Start/einde van **hook A, B, C** (Peter zegt ze achter elkaar, dan ~2 s stil).
- De **body** (rest van het script, één keer).
- Dubbele takes → kies de laatste volledige, tenzij een eerdere duidelijk beter is.
Schrijf de indeling op in `video-projects/<slug>/EDL.md` (tijdcodes per stuk + wat eruit gaat).
Eén lange opname met meerdere video's? Splits per video volgens het transcript + draaiboek.

## 4. Audio knippen (Peter's opname = ruw, Claude knipt)

- Body: stiltes > 0,25 s, "eh"/"uhm", ademhalingen, versprekingen en mislukte zinnen eruit. Laat 0,05–0,1 s lucht rond elke cut zodat het niet hakt.
- Nooit woorden toevoegen of de inhoud veranderen.
- Exporteer `assets/body-edit.mp4` en `assets/hook-A.mp4`, `hook-B.mp4`, `hook-C.mp4` (strak geknipt).
- Maak per versie `assets/full-<X>.mp4` = hook-X + body-edit (ffmpeg concat). Meet de duur met `ffprobe` → `data-duration`.
- Transcribeer elke `full-<X>.mp4` opnieuw (Parakeet) voor woord-precieze captions.

**De body moet in alle versies byte-voor-byte dezelfde zijn.** Alleen de hook verschilt. Anders is de hook-test waardeloos.

## 5. Bouwen (Hyperframes)

**Start vanaf het geteste template:** `cp -r templates/sardo-format video-projects/<slug>/A` (en B, C). Daarin zitten al GSAP, Poppins, brand-tokens en alle lagen; je past alleen het CONFIG-blok onderaan `index.html` aan (duur, faceOffsetY, hook, woorden, beelden, punch-ins, CTA) + `data-duration` + `assets/source.mp4`. Render: `npx hyperframes render --quality standard --fps 25 --output renders/final.mp4` (getest: 6 s ≈ 30 s render).
Eén compositie per hook-versie, zelfde bouwstenen (bouw versie A, kopieer naar B/C en wissel alleen bron, hook-tekst en captions).
Lagen volgens `SARDO_FORMAT.md`:
- `face-wrapper` + `<video muted>` + aparte `<audio>`: SPLIT (zone 1) als er beeld is, FULL als er geen beeld is. Ogen op y≈534.
- `hook-text`: eerste ~2 s op het ankerpunt (y=960). Tekst = de hook die gezegd wordt, ingekort tot max 6 woorden.
- `captions`: zone 2, woordgesynct, 2–4 woorden, actief woord oranje.
- `beeld-scenes`: zone 3, de "Tekst in beeld" uit het concept + animaties bij bedragen/stappen/lijstjes + door Peter aangeleverde beelden.
- `punch-ins`: elke 3–5 s schaal de face-wrapper 1.0 → 1.12 (of terug) op een cut.
- `cta`: laatste 2 s, "Reageer" + **CHECK** of **AANBOD** groot op het ankerpunt.
- Render op 25 fps als de CLI het toestaat (`--fps 25`), anders 30.

`npx hyperframes lint` + `node ../../scripts/preflight.mjs .` moeten schoon zijn.

## 5b. YAPPING-video's (tip/verhaal/mening) — andere look!

Is het een yapping-video (Peter zegt het, of categorie = Yapping)? **Gebruik `templates/sardo-yapping/`** (lees de README) i.p.v. de beeld-zone-opzet hierboven:
- Peter **de hele video FULL** in beeld — geen grijs vlak/kaart, beeld niet halveren.
- Captions, hook en CTA **onder de kin** (midden y≈1285), nooit over het gezicht.
- Losse icoontjes (met schaduw + kort woordje) **horizontaal gecentreerd** in y 1400–1790, alleen 2–5 s op het moment dat Peter het zegt.
- Goedgekeurd door Peter op 25-10-2026 (video yapping-0093). Niet opnieuw vragen, gewoon zo bouwen.

## 6. Check vóór Peter iets ziet

1. Render 3 stills van versie A (hook ~1 s, midden, CTA) → zelf bekijken (Read) → fouten fixen.
2. Stuur die 3 stills in de chat (SendUserFile) met één regel uitleg. Wacht op akkoord, tenzij Peter al zei "gewoon renderen".
3. Draft-render van versie A → frames bekijken (5 fps sample is genoeg bij 25–45 s; zeg dat je gesampled hebt) → fixen.
4. Final-render van A, B en C (`--quality standard`). Check bij elke versie: gezicht niet afgesneden, captions op het juiste woord, niets rechts/onderin achter de IG-UI, geen zwarte frames, merkkleuren, @sardobouw correct.

## 7. Leveren

- Map op de Mac: `/Users/peter/Documents/videos/<categorie>/<jaar>/<maand>/`
  - Categorie zelf kiezen: **Funda** (een specifiek huis), **Yapping** (verhaal/mening/fout), **info** (uitleg/tips/lijstjes/nieuws), **overig**.
  - Maand: `01-januari` … `12-december`. Maak jaar/maand-map aan als die er niet is (`device_bash mkdir -p`).
  - Naam: `<opnamedatum>-D<dag>-<onderwerp>-<A|B|C>.mp4`
- Schrijf met `device_commit_files` (stagedPath onder `/mnt/user-data/outputs/`). Stuur ook alle versies in de chat (SendUserFile).
- Mac niet bereikbaar → alleen in de chat, en meld dat.

## 8. Wat Peter er per video bij krijgt (kort, in de chat)

1. Waar de video's staan + welke categorie je koos.
2. Wat je hebt gemeld/aangenomen (bv. ontbrekend bedrag, tijdgevoelige hook).
3. **Instagram-caption** (max 3 korte regels, taal groep 3-4, eindigt met het CTA-woord) + 3–5 hashtags (lokaal + onderwerp, bv. #arnhem #verduurzamen #warmtepomp).
4. **Cover-tekst** (max 4 woorden).
5. **Trial Reels-plan**: alle versies als Trial Reel (alleen niet-volgers), graduation op handmatig, zelfde caption/cover/tijdstip-blok. Na 48–72 uur vergelijken op: % dat na 3 s blijft kijken, gemiddelde kijktijd, shares+saves, reacties met CHECK/AANBOD. Winnaar delen naar profiel.
6. **Tracker-regel**: `Video | Hook | Type (pijn/vraag/stelling) | Postdatum | 3-sec % | Kijktijd | Shares | Saves | CHECK/AANBOD | Winnaar?`
7. Afsluiten met: "Feedback op deze? Zeg `/feedback`."

## 9. Als Peter resultaten stuurt

Zeg welke hook won en waarom (2–3 zinnen). Houd het hook-type bij; na 5+ video's: welk type wint. Doen alle versies het slecht → het ligt waarschijnlijk aan onderwerp of body, niet aan de hook. Zeg dat eerlijk. Leg winnende patronen vast in `PREFERENCES.md` via `/feedback`.

## 10. Opslaan in de fork

Na elke video: commit project-metadata (EDL.md, compositions, geen grote media — `renders/` en `raw-media/` staan in .gitignore) en eventuele PREFERENCES-updates, en push naar `main` van `sardoinstallatie/Hyperframes-colton.ai.dean`. Lukt push niet → meld het, werk gewoon door.

## 11. Bekende valkuilen (geleerd bij D14, okt 2026)

- **Overzetten Mac ↔ cloud is traag.** Stage/commit lukt alleen met stukjes van ~6 MB (één per call). 4K-bron eerst op de Mac knippen + verkleinen met ffmpeg in stukken van ≤20 s (anders timeout van 180 s), dan `split -b 6m` en stuk voor stuk stagen; in de cloud weer `cat` en md5 checken.
- **`/mnt/user-data/outputs/` past mp4-headers aan.** Een bestand of stuk dat met een mp4-header begint wordt gewijzigd → checksum klopt niet. Pak het eerste stuk in (`gzip -1`) en pak het op de Mac weer uit. Altijd md5 vergelijken na `cat` op de Mac.
- **Lang renderen in de achtergrond:** start met `setsid nohup bash render.sh … & disown` en laat het script met `sleep 3` beginnen; anders breekt de render af met `render_cancelled_parent_exited`.
- Werkbestanden op de Mac: `videos/raw/_work/`, na afloop verplaatsen naar `videos/raw/_to_delete/` (verwijderen mag niet zonder toestemming).

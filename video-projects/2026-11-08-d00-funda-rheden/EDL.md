# D17 · Funda Fixer #5 — Arnhemsestraatweg 177, Rheden (opname 8 nov 2026, clip DJI_20261108153835_0119_D, 6:28 ruw)

Funda: vrijstaande villa, 1953, label G, €795.000 k.k. (Funda noemt zichzelf tegensprekend 117/133 m²; ketel 2021 volgens Peter).
Eén hook opgenomen → alleen versie A. Resultaat: **80,6 s**. Categorie Funda. Bestand `2026-11-08-D17-funda-rheden-A.mp4`.

## Volgorde (brontijden → uit)
| # | stuk | bron | uit | tekst |
|---|---|---|---|---|
| 0 | hook | 44.54–48.79 | 0.00–4.25 | Deze villa in Rheden, van label G naar label A in 1 minuut. |
| 1 | intro | 3.66–7.90 + 8.21–9.87 | 4.25–10.14 | Dit is de Arnhemsestraatweg 177 in Rheden. Funda Fixer nummer 5. (adres alleen hoorbaar, geen caption) |
| 2 | villa | 27.30–29.89 | 10.14–12.73 | Een villa uit 1953. → prijs + "Villa · Rheden · 1953 · Label G" op kaart |
| 3 | calc | 59.93–64.50 | 12.73–17.30 | We gaan hem eerst even invullen in de calculator, zodat we kunnen zien wat ongeveer de maandelijkse kosten zijn. → D7-scroll (calc-slow.mp4, 4,3 s) |
| 4–10 | plan | 75.45–77.95, 86.17–90.35, 95.01–98.16, 109.53–113.15, 123.28–127.31, 144.40–149.56, 172.72–176.80 | 17.30–44.24 | spouw · dak binnen + vloer · HR++ · ventilatie · hybride wp (take 1, ketel vrij nieuw) · panelen + micro-omvormers schuin dak · batterij 10–15 kWh |
| 11 | kosten1 | 187.31–189.37 | 44.24–46.30 | Dit zijn de kosten daarvan. → prijzen op bonnetje (gedicteerd, niet hoorbaar) |
| 12 | totaal | 279.76–285.80 | 46.30–52.34 | De totale kosten hiervan zijn ongeveer €46.000. Maar er gaat nog €4.000 tot €6.000 subsidie vanaf. |
| 13 | netto | 292.32–296.98 | 52.34–56.99 | Dus netto kost dit ongeveer €40.000 tot €42.000. |
| 14 | maand oud | 305.23–310.55 | 56.99–62.31 | …ongeveer €325 per maand in de oude situatie. (take 1, Peter bevestigde 325) |
| 15 | maand nieuw | 321.55–328.13 | 62.31–68.89 | In de nieuwe situatie ongeveer €110 … besparing van €215 per maand. (retake) |
| 16 | fixscore | 357.15–362.35 | 68.89–74.09 | Fixscore is 6 van de 10. Alles wat geïsoleerd moet worden is redelijk goed bereikbaar. |
| 17 | cta | 375.82–382.45 | 74.09–80.56 | Heb je nou ook net een huis gekocht? Stuur de Funda-link… of reageer CHECK onder dit bericht. |

## Eruit (akkoord Peter, 8 nov: "lengte is belangrijk, ik vertel meer dan nodig")
Oké's en stiltes; "Een villa uit 1953"-fragment 19–30 s (half); spouw-uitleg ("indien aanwezig, ik verwacht het wel…"); serre-opmerking; "type C of D … ga ik voor type C"; hybride-retake met "all-electric ready"; "Ongeveer 10 tot 12 panelen zou genoeg moeten zijn" (op kaart); batterij-uitleg na "15 kWh"; de "skip die batterij"-take; gedicteerde prijslijst (192–258 s, alleen op het bonnetje); "Ik heb deze maar ik kijk niet in de camera"; "Afhankelijk van wanneer je het koopt natuurlijk"; maand-take 1 na "oude situatie" (125/130-verspreking); fixscore-takes 1–2 en tweede helft take 3; "en dan zal ik jou even een berichtje doen"; "…en wat de potentie is in deze woning".

## Bouw
`work/mac_cut.sh` (stukken op de Mac, `raw/_work/0119/seg/`) → `work/concat.sh` → `assets/source.mp4` → Parakeet → `build.py` → `index.html`.
Kaart: badge "Funda Fixer #5" + Funda-foto in eerste shot; tagbar (prijs/feiten) pas bij "Een villa uit 1953".

## Final (8 nov 2026)
Geleverd: `Funda/2026/11-november/2026-11-08-D17-funda-rheden-A.mp4` (80,6 s, md5 7bfddaaf…). Na eerste render gefixt: kaarten gecentreerd (x 117–963), geen flits tussen kaarten, punch-in 1.22/1.14 bij Peter vol in beeld (geen donkere band).

## v2 (8 nov, avond) — feedback Peter: "intro raar, adres niet noemen, niet midden in de zin knippen, kijk naar FF#3"
Fouten in v1: midden-in-zin-knips bij "indien aanwezig", ventilatie ("…in gaan komen, | dus dat kan type C of D"), batterij ("…15 kWh, | om in ieder geval…"), CTA ("…onder dit bericht | en dan zal ik jou…"), maand-oud ("…oude situatie | en in een nieuwe situatie"), plus stukken waarvan het laatste woord net afgeknipt was (vloer, HR++, panelen). Intro had het adres nog in de audio.
v2: elk stuk loopt van stilte tot stilte (silencedetect −38 dB) en is los getranscribeerd om te checken dat het op een hele zin begint en eindigt. Begin/eind-niveau per stuk gemeten (< −45 dB). Niveau per stuk gelijkgetrokken (villa-zin was zacht).
Eruit (hele zinnen): adres + "Funda Fixer nummer 5" (badge staat in beeld), "Een villa uit 1953" (kijkt weg, zacht — klinkt als notitie), serre, hybride-retake, batterij-skip-take, dictaat, regie-opmerkingen, fixscore-takes 1–2, en van fixscore-take 3 de zinnen ná "…redelijk goed bereikbaar."
Bewust erin (hele zinnen, logica): spouw-uitleg ("Ik verwacht het wel, want het is een woning uit 1953…"), "In dit geval ga ik even voor type C", "Ongeveer 10 tot 12 panelen…", "Afhankelijk van wanneer je het koopt natuurlijk", maand-zin heel incl. "…en in een nieuwe situatie."
Resultaat 96,9 s.

| stuk | bron | uit | tekst |
|---|---|---|---|
| hook | 44.85–48.90 | 0.00–4.05 | Deze villa in Rheden, van label G naar label A in 1 minuut. |
| calc | 59.95–66.30 | 4.05–10.40 | We gaan hem eerst even invullen in de calculator, zodat we kunnen zien wat ongeveer de maandelijkse kosten zijn en wat de potentie is in deze woning. |
| spouw | 75.47–83.30 | 10.40–18.23 | Wat wij zouden doen is de spouw isoleren, indien aanwezig. Ik verwacht het wel, want het is een woning uit 1953, toen werd er al wel gebouwd met spouwen. |
| dak-vloer | 86.55–90.40 | 18.23–22.08 | Dan vervolgens het dak van binnen isoleren. De vloer isoleren. |
| hr | 95.30–98.30 | 22.08–25.08 | HR++ glas in de hele woning. |
| vent | 109.60–117.75 | 25.08–33.23 | Dan moet er iets van ventilatie in gaan komen, dus dat kan type C of type D zijn. In dit geval ga ik even voor type C. |
| wp | 123.30–127.35 | 33.23–37.28 | Dan een hybride warmtepomp. De ketel is nog vrij nieuw. |
| panelen | 144.75–153.40 | 37.28–45.93 | En dan zouden we nog zonnepanelen in combinatie met micro-omvormers plaatsen op het schuine dak. Ongeveer 10 tot 12 panelen zou genoeg moeten zijn. |
| batterij | 172.95–181.30 | 45.93–54.28 | En dan installeren we nog een batterij van tussen de 10 en de 15 kWh, om in ieder geval de warmtepomp te kunnen compenseren, en kunnen laden op goedkope momenten. |
| kosten | 187.12–189.55 | 54.28–56.71 | Dit zijn de kosten daarvan. |
| totaal | 279.90–288.00 | 56.71–64.81 | De totale kosten hiervan zijn ongeveer 46.000 euro. Maar er gaat nog 4 tot 6.000 euro subsidie vanaf. Afhankelijk van wanneer je het koopt natuurlijk. |
| netto | 292.55–297.65 | 64.81–69.91 | Dus netto kost dit ongeveer 40 tot 42.000 euro. |
| maand-oud | 305.70–312.20 | 69.91–76.41 | De geschatte maandelijkse kosten waren ongeveer 325 euro per maand in de oude situatie en in een nieuwe situatie. |
| maand-nieuw | 321.80–328.20 | 76.41–82.81 | In een nieuwe situatie wordt dat ongeveer 110 euro per maand. Dus dat betekent dat je een maandelijkse besparing hebt van 215 euro per maand. |
| fix | 357.05–362.33 | 82.81–88.09 | Fixscore is 6 van de 10. Alles wat geïsoleerd moet worden, is redelijk goed bereikbaar. |
| cta | 375.85–384.70 | 88.09–96.94 | Heb je nu ook net een huis gekocht? Stuur dan even de Funda-link naar mij, dan ga ik dit ook doen voor jouw woning. Of reageer CHECK onder dit bericht en dan zal ik jou even een berichtje doen. |

## Final v2 (8 nov 2026, avond)
Geleverd en v1 overschreven: `Funda/2026/11-november/2026-11-08-D17-funda-rheden-A.mp4` (97,1 s, md5 785cc5d7…). Frames 2 fps bekeken, geen zwarte frames, geen lange stiltes.

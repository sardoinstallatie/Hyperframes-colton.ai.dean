# Funda Fixer — cover (vast sjabloon, sinds #4 Wehl, 10 nov 2026)

1080×1920. Alle tekst binnen het 4:5-vlak (y 285–1635), zodat het profielraster niks afsnijdt.

Per aflevering:
1. `peter.jpg`: frame uit de geknipte video waar Peter in de camera kijkt (bv. hook).
   `ffmpeg -ss <t> -i source.mp4 -frames:v 1 -vf "crop=900:1290:90:200,scale=1080:1548,eq=brightness=0.06:contrast=1.08:saturation=1.1" peter.jpg`
2. `huis.png`: Funda-hoofdfoto (dezelfde als in de video).
3. In `cover.html`: nummer (#), label-van (G → A), "Type · Plaats · Bouwjaar", prijs.
4. Screenshot met Playwright (viewport 1080×1920, deviceScaleFactor 1) → `<opnamedatum>-D<dag>-funda-<plaats>-cover.png` naast de video.

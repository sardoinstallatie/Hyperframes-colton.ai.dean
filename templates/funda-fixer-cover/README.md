# Funda Fixer — cover (vast sjabloon, ALTIJD gebruiken)

> Peter, 10 nov 2026: "Maak de cover voor de funda fixers nu ALTIJD ZO!" — opmaak nooit aanpassen, alleen de inhoud per aflevering.

**Dit is de goedgekeurde look van #3, #5, #6, #8 en #9** (groot gezicht, badge gecentreerd, "Label X ➜ A" met blauwe pijl,
huiskaart met oranje rand, "€…/mnd minder" rechtsboven, "Type · bouwjaar · plaats" linksonder).
De Wehl-cover (#4) is op 10 nov opnieuw gemaakt met dit sjabloon en klopt nu ook. (Peter, 10 nov 2026: "waarom maak je die cover nou weer anders dan de andere?")

Per aflevering:
1. Kopieer deze map naar `video-projects/<project>/cover/`.
2. `face.jpg` = één volle frame (1080×1920) uit de geknipte bron waar Peter in de lens kijkt **en een beetje lacht** (Peter, 10 nov — zoek een lachmoment, niet zomaar een praat-frame):
   `ffmpeg -ss <t> -i assets/source.mp4 -frames:v 1 -q:v 2 cover/face.jpg`
   (positie/zoom zit in `#face` in cover.html; check dat de ogen net boven de badge staan, zoals bij #8/#9).
3. `huis.jpg` = de Funda-hoofdfoto (dezelfde als in de video).
4. In `cover.html` aanpassen: `Funda Fixer #n`, labelletter (G/F/…), `€…/mnd minder` (besparing per maand uit de video), `Type · bouwjaar · plaats`.
5. Vanuit de repo-root: `node templates/funda-fixer-cover/shot.cjs` werkt alleen op de templatemap — in een project: `node video-projects/<project>/cover/shot.cjs` (pas de uitvoernaam aan) → `<opnamedatum>-D<dag>-funda-<plaats>-cover.png` naast de video.
6. Leg hem naast een vorige cover (bv. D20 Druten) en check dat hij er hetzelfde uitziet.

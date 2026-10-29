# EDL — "In welke laag zit jouw huis?" (opname 29-10-2026)

Bron A = dji_mimo_20261029_202226_…_1793302243650_video (211 s), bron B = dji_mimo_20261029_202400_… (outro, 84 s).
Alleen hook A opgenomen ("Net een nieuwe HR-ketel laten plaatsen…") → 1 versie.

| # | Bron | In | Uit | Tekst |
|---|---|---|---|---|
| 1 | A | 2.38 | 7.30 | Hook: nieuwe HR-ketel → top 90% |
| 2 | A | 60.30 | 63.30 | Dubbel glas beneden → 80% (4e take; 18–59 s mislukte takes eruit) |
| 3 | A | 78.61 | 82.33 | Vloer + spouw → 70% |
| 4 | A | 99.65 | 104.43 | Dak → 60% |
| 5 | A | 110.85 | 116.43 | Overal HR++ → 50% |
| 6 | A | 135.12 | 139.72 | Zonnepanelen → 40% (take 123 s eruit, "top 50%" verspreking) |
| 7 | A | 148.32 | 153.00 | All-electric warmtepomp → 30% |
| 8 | A | 180.89 | 187.17 | Thuisbatterij → 20% (take 165 s eruit) |
| 9 | A | 198.17 | 210.11 | EMS → top 10% |
| 10 | B | 77.05 | 82.90 | Outro: volg mij voor meer tips (laatste take) |

Geknipt op de Mac (crop 1080×1120 vanaf y=400 op 1080-schaal) → raw-media/body.mp4, 55,88 s.
Layout: op verzoek zoals @therealbrianmark-screenshot — piramide boven (0–960), captions op de naad, Peter onder.

## v2 (29-10, 21:00)
- Shot 9 (top 10%) eindigt 0,44 s eerder: naar-voren-leunen eruit → raw-media/body2.mp4 (55,44 s).
- Top-zone wisselt nu: huis-animatie (house.py) tijdens de zin, piramide + "TOP X%" op het moment dat Peter het percentage noemt. Afsluiter: rood beginhuis ➜ groen eindhuis.
- Build: `python3 build2.py` (template tpl.html).
- v3: eerste ~2,3 s piramide met rode onderste balk zonder tekst (nieuwsgierigheid), dan huis, dan 90%.

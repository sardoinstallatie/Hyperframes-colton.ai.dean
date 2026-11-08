#!/usr/bin/env python3
"""D19 · Funda Fixer #9 — Zevenheuvelenweg 52, Berg en Dal (versie A v2, hele zinnen, 2:49).
Bouwt index.html uit work/template-arnhem.html + CONFIG. Draai: python3 build.py  (dan: bash work/render.sh)
Bron: assets/source.mp4 = Mac raw/_work/0123/v2cut.sh + v2concat.sh (21 stukken, alleen tussen hele zinnen, filter-concat). Knippen: work/v2-cuts.json.
"""
import json, re, subprocess

DUR = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/source.mp4"]).decode().strip()), 2)

# ---------- woorden (Parakeet-transcript van assets/source.mp4; tijden blijven, tekst handmatig verbeterd) ----------
raw = json.load(open("work/source-words.json"))
W = [[x["text"], x["start"], x["end"]] for x in raw]

REP = {"Daal": "Dal", "minuten.": "minuut.", "energiel": "energielabel", "energibel": "energielabel", "spou": "spouw", "span": "spouw",
       "EPS-korres.": "EPS-korrels.", "voorzettwanden.": "voorzetwanden.", "keten": "ketel", "Ready": "ready", "uiteraard": "uiteraard,",
       "kW.": "kWh.", "gedo": "gedoe", "check": "CHECK", "Enek": "Betekent", "Fixescoren": "Fixscore is", "spouwmuurisolatie": "spouwmuur-isolatie",
       "investering": "besparing"}   # 140.18: Peter zegt "investering", bedoelt besparing (Peter: "zet besparing neer")
DROP = {"joh,"}


def fix(words):
    out = []
    i = 0
    while i < len(words):
        t, s, e = words[i]
        nxt = words[i + 1][0] if i + 1 < len(words) else ""
        if t in DROP: i += 1; continue
        if t == "investering." and s < 130: t = "investering."   # 32.000 = echt investering
        elif t == "investering" and not (139 < s < 141): pass
        if t == "en" and 2.4 < s < 2.6: t = "naar"
        if t == "154k":                                                  # "honderdvijf vierkante meter"
            out += [["105", s, s + 0.56], ["vierkante", s + 0.56, s + 1.1], ["meter", s + 1.1, e]]; i += 1; continue
        if t == "er" and 11.9 < s < 12.1: t = "te"
        if t == "475.000" and nxt == "euro.":
            out.append(["€475.000.", s, words[i + 1][2]]); i += 2; continue
        if t == "wonen" and 35 < s < 36:
            out += [["woning", s, s + 0.28], ["koopt,", s + 0.28, e]]; i += 1; continue
        if t == "doen." and 36.8 < s < 37.1: t = "doen:"
        if t == "In" and 46.5 < s < 46.8: t = "Indien"
        if t == "ieder" and 46.7 < s < 46.9: t = "er"
        if t == "geval" and 46.9 < s < 47.1: i += 1; continue
        if t == "binnen" and nxt == "uit":
            out.append(["binnenuit", s, words[i + 1][2]]); i += 2; continue
        if t == "vlueisoleren":
            out += [["vloer", s, s + 0.45], ["isoleren", s + 0.45, e]]; i += 1; continue
        if t == "zitten" and 60 < s < 61:
            out += [["zit,", s, s + 0.13], ["want", s + 0.13, s + 0.27], ["daar", s + 0.27, e]]; i += 1; continue
        if t == "doen." and 73 < s < 74: t = "doen,"
        if t == "Ga" and 77 < s < 77.3: t = "Gaat"
        if t == "niet." and 77.4 < s < 77.7: t = "niet,"
        if t == "ken" and 85.7 < s < 86: t = "ketel"
        if t == "zo" and 86.3 < s < 86.5: t = "is"
        if t in ("al", "Al") and nxt == "Electric":
            out.append(["all-electric", s, words[i + 1][2]]); i += 2; continue
        if t == "Maar" and 124.9 < s < 125.2:                           # "maar dan krijg je nog… daar krijg je nog"
            out += [["maar", s, s + 0.2], ["dan", s + 0.2, s + 0.38], ["krijg", s + 0.38, s + 0.6], ["je", s + 0.6, s + 0.72], ["nog…", s + 0.72, s + 0.95]]; i += 1; continue
        if t == "ben" and 151.7 < s < 152: t = "denk"
        if t == "er" and 168 < s < 168.2: t = "we er"
        if t == "gaan" and (72.2 < s < 72.4 or 73.2 < s < 73.4): t = "gaat"
        if t == "Kijk" and (73.6 < s < 73.8 or 77.7 < s < 77.9): t = "kijk"
        if t == "In" and 37.0 < s < 37.2: t = "in"
        if t == "investering." and 124.3 < s < 124.5: t = "investering,"
        if t == "Funna":
            out.append(["Funda-link.", s, words[i + 1][2]]); i += 2; continue
        if nxt.startswith("euro") and re.match(r"^[0-9][0-9.,]*$", t):   # "300 euro" → €300
            val = {"4000": "4.000"}.get(t, t) + ("." if nxt.endswith(".") else "")
            out.append(["€" + val, s, words[i + 1][2]]); i += 2; continue
        if t == "3" and nxt == "tot" and 126 < s < 127.2: t = "€3.000"
        if t == "28" and 130 < s < 131: t = "€28.000"
        if t == "investering" and not (139.5 < s < 141): out.append([t, s, e]); i += 1; continue
        t = REP.get(t, t)
        out.append([t, s, e]); i += 1
    return out


WORDS = fix(W)

# ---------- beeld-zone ----------
HOOK_END = 3.6
CTA_START = 165.95
BON = [  # (regel, prijs, tijd dat de naam verschijnt = moment dat Peter het noemt)
    ("Muren isoleren (spouw)", "€3k – 5k", 44.8),
    ("Vloer isoleren", "€1,5k – 3k", 58.9),
    ("Ventilatie (type D of C)", "€3k – 5k", 63.6),
    ("Hybride warmtepomp", "€8,5k – 12k", 91.9),
    ("10–12 zonnepanelen", "€5k – 6k", 112.9),
    ("Batterij 10–15 kWh", "€6k – 10k", 117.7),
]
bon_html = '<div class="label">Het plan</div>' + "".join(
    f'<div class="row r{i+1}"><span class="n">{n}</span><span class="p p{i+1}">{p}</span></div>' for i, (n, p, _) in enumerate(BON)
) + '<div class="tot"><span>Totaal</span><span class="p">± €32.000</span></div>'
# prijzen verschijnen bij "Dat alles bij elkaar" (120.66), totaal bij "32.000" (122.82)
bon_pop = [[f".r{i+1}", t] for i, (_, _, t) in enumerate(BON)] + [[f".p{i+1}", round(120.7 + 0.17 * i, 2)] for i in range(len(BON))] + [[".tot", 122.8]]

BEELDEN = [
    # 1 Eerste shot: Funda-foto + serie-label; prijs/feiten bij "Dit is een vrijstaande woning" (3.92)
    {"start": 0.0, "end": 14.36, "html": '<img src="assets/huis.jpg"><div class="badge">Funda Fixer <b>#9</b></div>'
     '<div class="tagbar t1"><span class="price">€ 475.000 <small>k.k.</small></span><span class="meta">Vrijstaand · Berg en Dal · 1925<br>105 m² · Label G</span></div>',
     "pop": [[".t1", 3.95]]},
    # 2 Calculator (D07-schermopname, vertraagd)
    {"start": 14.36, "end": 20.08, "el": "#calc-card", "pop": []},
    # 3 Label klopt waarschijnlijk niet
    {"start": 20.08, "end": 34.9, "html": '<div class="label">Energielabel</div>'
     '<div class="labels"><div class="lab g">G</div><div class="line q1">Klopt waarschijnlijk <span class="acc">niet</span></div></div>'
     '<div class="line c1">✓ Dubbel glas</div><div class="line c2">✓ Dak net geïsoleerd</div>',
     "pop": [[".q1", 23.9], [".c1", 26.6], [".c2", 28.1]]},
    # 4 Inleiding plan: stap 1
    {"start": 34.92, "end": 43.45, "html": '<div class="label">Het plan · stap 1</div><div class="line s1">Nieuw <span class="acc">energielabel</span> aanvragen</div>'
     '<div class="note s2">Dan weet je hoe het huis er nu echt voor staat</div>',
     "pop": [[".s1", 39.4], [".s2", 41.3]]},
    # 5 Het plan — bonnetje; namen als Peter ze noemt, prijzen bij "Dat alles bij elkaar", totaal bij "32.000"
    {"start": 43.5, "end": 125.0, "cls": "bon", "html": bon_html, "pop": bon_pop},
    # 6 Subsidie + netto
    {"start": 125.05, "end": 133.9, "html": '<div class="label">Kosten</div><div class="value">± €32.000</div>'
     '<div class="sub s1">− €3.000 à €4.000 subsidie</div><div class="net s2">Netto: <b>± €28.000 – €29.000</b></div>'
     '<div class="note s1">Schatting. Check subsidie op rvo.nl</div>', "pop": [[".s1", 126.8], [".s2", 130.6]]},
    # 7 Energie per maand (Peter: "besparing" i.p.v. "investering")
    {"start": 133.95, "end": 142.6, "html": '<div class="label">Energie per maand</div><div class="line m1">Nu: <b class="dim">± €300</b></div>'
     '<div class="line m2">Straks: <b class="acc">± €110</b></div><div class="line m3">Besparing: <b class="acc">€190</b> per maand</div>',
     "pop": [[".m1", 136.9], [".m2", 138.15], [".m3", 140.8]]},
    # 8 Fixscore
    {"start": 142.66, "end": 153.75, "html": '<div class="label">Fixscore <span style="text-transform:none;letter-spacing:0">· hoger = makkelijker</span></div>'
     '<div class="value f0">7<span class="of">/10</span></div><div class="line f1">✓ Dak al geïsoleerd</div><div class="line f2">✓ Overal dubbel glas</div>'
     '<div class="line f3">✓ Scheelt gedoe en tijd</div>',
     "pop": [[".f0", 143.75], [".f1", 145.5], [".f2", 146.95], [".f3", 148.6]]},
]

# punch-ins op de knippen (afwisselend in/uit), CTA weer in
CUTS = [3.72, 7.64, 10.56, 14.36, 20.08, 21.6, 26.16, 29.76, 34.92, 37.12, 43.52, 46.64, 49.92, 52.8, 58.64, 62.64, 65.0, 70.65, 73.69, 77.13,
        80.65, 85.56, 88.65, 91.93, 95.77, 101.28, 104.65, 108.09, 112.28, 115.85, 120.84, 126.08, 129.6, 134.24, 138.0, 142.84, 144.82, 148.34, 151.46]
PUNCH = [[t, 1.14 if k % 2 == 0 else 1.0] for k, t in enumerate(CUTS)]
PUNCH += [[153.96, 1.14], [157.38, 1.22], [159.78, 1.14], [162.16, 1.22], [CTA_START, 1.14]]  # Peter FULL: nooit onder 1.14
PUNCH.sort()

CONFIG = {
    "duration": DUR,
    "faceOffsetY": -309, "faceOffsetX": 0, "faceScale": 1.08,
    "hook": {"text": 'Label <span class="hl">G</span> naar <span class="hl">A</span><br>in 1 minuut', "end": HOOK_END},
    "cta": {"word": "CHECK", "start": CTA_START},
    "words": WORDS, "chunkSize": 3, "beelden": BEELDEN, "punchIns": PUNCH,
}

tpl = open("work/template-arnhem.html").read()
head = tpl[: tpl.find("const CONFIG")]
ci = tpl.find("const CONFIG")
tail = tpl[tpl.find("/* ====", ci + 10):]  # alles ná het oude CONFIG-blok
head = re.sub(r"<!--.*?-->", "<!--\n  D19 · Funda Fixer #9 — Zevenheuvelenweg 52, Berg en Dal (versie A)\n  Sardo-format (zie ../../SARDO_FORMAT.md). Gegenereerd door build.py — pas build.py aan, niet dit bestand.\n-->", head, count=1, flags=re.S)
head = re.sub(r'data-duration="[0-9.]+"', f'data-duration="{DUR}"', head)
head = re.sub(r'(src="assets/calc-slow.mp4" muted playsinline) data-start="[0-9.]+" data-duration="[0-9.]+"', r'\1 data-start="14.36" data-duration="5.72"', head)
head = head.replace("/* Bonnetje", ".beeld .badge { position: absolute; left: 28px; top: 28px; padding: 14px 28px; border-radius: 999px; background: var(--brand-accent); color: var(--brand-bg); font-size: 40px; font-weight: 800; letter-spacing: 0.01em; box-shadow: 0 6px 20px rgba(0,0,0,0.35); }\n      .beeld .badge b { font-weight: 800; }\n      .beeld .tagbar .price small { font-size: 34px; font-weight: 700; color: var(--brand-text-dim); }\n      .beeld .labels .line { font-size: 46px; }\n      /* Bonnetje")
head = head.replace("    </style>", "      .bon .row { font-size: 40px; line-height: 1.55; }\n      .bon .tot { font-size: 46px; margin-top: 16px; }\n      .beeld .line.m3 { font-size: 50px; }\n    </style>")
cfg = "const CONFIG = " + json.dumps(CONFIG, ensure_ascii=False) + ";\n      "
open("index.html", "w").write(head + cfg + tail)
print("index.html geschreven · duur", DUR, "s ·", len(WORDS), "woorden")
json.dump(CONFIG, open("work/config.json", "w"), ensure_ascii=False, indent=1)

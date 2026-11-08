#!/usr/bin/env python3
"""D19 · Funda Fixer #9 — Zevenheuvelenweg 52, Berg en Dal (versie A, 91,4 s).
Bouwt index.html uit work/template-arnhem.html + CONFIG. Draai: python3 build.py  (dan: bash work/render.sh)
Bron: assets/source.mp4 = Mac raw/_work/0123/rebuild2.sh (26 stukken, filter-concat; copy-concat gaf audio-drift).
"""
import json, re, subprocess

DUR = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/source.mp4"]).decode().strip()), 2)

# ---------- woorden (Parakeet-transcript van assets/source.mp4; tijden blijven, tekst handmatig verbeterd) ----------
raw = json.load(open("work/source-words.json"))
W = [[x["text"], x["start"], x["end"]] for x in raw]

REP = {"Daal": "Dal", "vloei": "vloer", "ventilati": "ventilatie", "keten": "ketel", "Bel": "Wel",
       "leggen": "Leggen", "kilowat.": "kWh.", "Fixerscore": "Fixscore", "Fixescoren": "Fixscore", "link.": "link.",
       "check": "CHECK", "Datekent": "Dat betekent", "spouwmuurisolatie": "spouwmuur-isolatie", "Nijmegen?": "Nijmegen?"}


def fix(words):
    out = []
    i = 0
    while i < len(words):
        t, s, e = words[i]
        nxt = words[i + 1][0] if i + 1 < len(words) else ""
        if t == "en" and 2.4 < s < 2.6: t = "naar"                       # hook: "van label G naar label A"
        if t == "1" and 3.1 < s < 3.4:
            out += [["in", s - 0.12, s], ["1", s, e]]; i += 1; continue
        if t == "154":                                                   # "honderdvijf vierkante meter"
            out += [["105", s, s + 0.5], ["vierkante", s + 0.5, e]]; i += 1; continue
        if t == "er" and 11.4 < s < 11.7: t = "te"
        if t == "van" and 11.8 < s < 12.2: t = "voor"
        if t == "475.": t = "€475.000."
        if t == "In" and 27.7 < s < 28.1: t = "Indien"
        if t == "iedere" and 27.9 < s < 28.3: t = "er"
        if t == "naar." and 35.3 < s < 35.7:                             # "kijken naar ventilatie."
            out += [["naar", s, s + 0.16], ["ventilatie.", s + 0.16, e]]; i += 1; continue
        if t == "al" and nxt == "Electric":
            out.append(["all-electric", s, words[i + 1][2]]); i += 2; continue
        if t == "Ready": t = "ready"
        if t == "uiteraard" and 51.9 < s < 52.3: t = "uiteraard."
        if t == "brengen" and 71 < s < 72: t = "breng je"
        if t == "Funna":
            out.append(["Funda-link.", s, words[i + 1][2]]); i += 2; continue
        if nxt.startswith("euro") and re.match(r"^[0-9][0-9.,]*$", t):   # "300 euro" → €300
            val = {"4000": "4.000", "29.000": "29.000"}.get(t, t) + ("." if nxt.endswith(".") else "")
            out.append(["€" + val, s, words[i + 1][2]]); i += 2; continue
        if t == "28" and 68 < s < 69.5: t = "€28.000"
        if t == "3" and nxt == "tot" and 65 < s < 66: t = "€3.000"
        t = REP.get(t, t)
        out.append([t, s, e]); i += 1
    return out


WORDS = fix(W)

# ---------- beeld-zone ----------
HOOK_END = 3.9
CTA_START = 88.75
BON = [  # (regel, prijs, tijd dat de naam verschijnt = moment dat Peter het noemt)
    ("Muren isoleren (spouw)", "€3k – 5k", 26.0),
    ("Vloer isoleren", "€1,5k – 3k", 31.45),
    ("Ventilatie (type D of C)", "€3k – 5k", 35.55),
    ("Hybride warmtepomp", "€8,5k – 12k", 49.2),
    ("10–12 zonnepanelen", "€5k – 6k", 53.3),
    ("Batterij 10–15 kWh", "€6k – 10k", 57.5),
]
bon_html = '<div class="label">Het plan</div>' + "".join(
    f'<div class="row r{i+1}"><span class="n">{n}</span><span class="p p{i+1}">{p}</span></div>' for i, (n, p, _) in enumerate(BON)
) + '<div class="tot"><span>Totaal</span><span class="p">± €32.000</span></div>'
# prijzen verschijnen tijdens "De kosten hiervan" (59.35–60.45), totaal bij "32.000" (62.55)
bon_pop = [[f".r{i+1}", t] for i, (_, _, t) in enumerate(BON)] + [[f".p{i+1}", round(59.4 + 0.17 * i, 2)] for i in range(len(BON))] + [[".tot", 62.5]]

BEELDEN = [
    # 1 Eerste shot: Funda-foto + serie-label; prijs/feiten bij "Dit is een vrijstaande woning" (4.24)
    {"start": 0.0, "end": 13.28, "html": '<img src="assets/huis.jpg"><div class="badge">Funda Fixer <b>#9</b></div>'
     '<div class="tagbar t1"><span class="price">€ 475.000 <small>k.k.</small></span><span class="meta">Vrijstaand · Berg en Dal · 1925<br>105 m² · Label G</span></div>',
     "pop": [[".t1", 4.3]]},
    # 2 Calculator (D07-schermopname, vertraagd)
    {"start": 13.28, "end": 19.0, "el": "#calc-card", "pop": []},
    # 3 Label klopt waarschijnlijk niet
    {"start": 19.0, "end": 25.92, "html": '<div class="label">Energielabel</div>'
     '<div class="labels"><div class="lab g">G</div><div class="line q1">Klopt waarschijnlijk <span class="acc">niet</span></div></div>'
     '<div class="line c1">✓ Dubbel glas</div><div class="line c2">✓ Dak net geïsoleerd</div>',
     "pop": [[".q1", 20.7], [".c1", 22.7], [".c2", 24.15]]},
    # 4 Het plan — bonnetje; namen tijdens het plan, prijzen bij "De kosten hiervan", totaal bij "32.000"
    {"start": 25.92, "end": 64.75, "cls": "bon", "html": bon_html, "pop": bon_pop},
    # 5 Subsidie + netto
    {"start": 64.8, "end": 71.5, "html": '<div class="label">Kosten</div><div class="value">± €32.000</div>'
     '<div class="sub s1">− €3.000 à €4.000 subsidie</div><div class="net s2">Netto: <b>± €28.000 – €29.000</b></div>'
     '<div class="note s1">Schatting. Check subsidie op rvo.nl</div>', "pop": [[".s1", 65.4], [".s2", 68.7]]},
    # 6 Energie per maand (Peter: "besparing" i.p.v. "investering")
    {"start": 71.55, "end": 76.5, "html": '<div class="label">Energie per maand</div><div class="line m1">Nu: <b class="dim">± €300</b></div>'
     '<div class="line m2">Straks: <b class="acc">± €110</b></div><div class="line m3">Besparing: <b class="acc">€190</b> per maand</div>',
     "pop": [[".m1", 73.9], [".m2", 75.1], [".m3", 75.65]]},
    # 7 Fixscore
    {"start": 76.55, "end": 81.5, "html": '<div class="label">Fixscore <span style="text-transform:none;letter-spacing:0">· hoger = makkelijker</span></div>'
     '<div class="value f0">7<span class="of">/10</span></div><div class="line f1">✓ Dak al geïsoleerd</div><div class="line f2">✓ Overal dubbel glas</div>',
     "pop": [[".f0", 76.95], [".f1", 78.7], [".f2", 80.1]]},
]

# punch-ins op de knippen (afwisselend in/uit), CTA weer in
CUTS = [3.96, 7.24, 9.96, 13.28, 19.0, 22.12, 25.92, 31.28, 34.76, 36.0, 39.36, 42.84, 50.56, 52.6, 55.84, 59.28, 60.52, 64.8, 67.64, 71.52, 73.64, 76.0, 81.56, 84.8, 87.12]
PUNCH = [[t, 1.14 if k % 2 == 0 else 1.0] for k, t in enumerate(CUTS)] + [[CTA_START, 1.14]]
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
head = re.sub(r'(src="assets/calc-slow.mp4" muted playsinline) data-start="[0-9.]+" data-duration="[0-9.]+"', r'\1 data-start="13.28" data-duration="5.72"', head)
head = head.replace("/* Bonnetje", ".beeld .badge { position: absolute; left: 28px; top: 28px; padding: 14px 28px; border-radius: 999px; background: var(--brand-accent); color: var(--brand-bg); font-size: 40px; font-weight: 800; letter-spacing: 0.01em; box-shadow: 0 6px 20px rgba(0,0,0,0.35); }\n      .beeld .badge b { font-weight: 800; }\n      .beeld .tagbar .price small { font-size: 34px; font-weight: 700; color: var(--brand-text-dim); }\n      .beeld .labels .line { font-size: 46px; }\n      /* Bonnetje")
cfg = "const CONFIG = " + json.dumps(CONFIG, ensure_ascii=False) + ";\n      "
open("index.html", "w").write(head + cfg + tail)
print("index.html geschreven · duur", DUR, "s ·", len(WORDS), "woorden")
json.dump(CONFIG, open("work/config.json", "w"), ensure_ascii=False, indent=1)

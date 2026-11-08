#!/usr/bin/env python3
"""D17 · Funda Fixer #5 — Arnhemsestraatweg, Rheden (versie A, 80,6 s).
Bouwt index.html uit work/template-arnhem.html + CONFIG. Draai: python3 build.py  (dan: npx hyperframes render ...)
Bron: assets/source.mp4 = work/concat.sh (19 stukken uit work/seg, EDL in work/edl.json).
"""
import json, re, subprocess

DUR = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/source.mp4"]).decode().strip()), 2)

# ---------- woorden (Parakeet-transcript van assets/source.mp4; tijden blijven, tekst handmatig verbeterd) ----------
raw = json.load(open("work/source-words.json"))
W = [[x["text"], x["start"], x["end"]] for x in raw]

REP = {"fila": "villa", "reden": "Rheden", "reden.": "Rheden.", "minuten.": "minuut.", "span": "spouw", "binnenuit": "binnen",
       "microonvormers": "micro-omvormers", "kilo.": "kWh.", "geschatten": "geschatte", "funnelink": "Funda-link", "check": "CHECK",
       "calculator.": "calculator,", "Zodat": "zodat"}
ADDR = {"Dit", "is", "de", "Arnhemse", "straatweg", "177", "in"}  # adres nooit in beeld (Peter, 8 nov)


def fix(words):
    out = []
    i = 0
    while i < len(words):
        t, s, e = words[i]
        nxt = words[i + 1][0] if i + 1 < len(words) else ""
        if 4.3 < s < 7.7 and t in ADDR:            # "Dit is de Arnhemsestraatweg 177 in" → geen caption
            i += 1; continue
        if t == "Villafixer":
            out += [["Funda", s, s + 0.45], ["Fixer", s + 0.45, e]]; i += 1; continue
        if t == "HaR":                              # "HaR Plus plus" → HR++
            out.append(["HR++", s, words[i + 2][2]]); i += 3; continue
        if t == "Ficie":                            # "Ficie score" → Fixscore
            out.append(["Fixscore", s, words[i + 1][2]]); i += 2; continue
        if nxt.startswith("euro") and re.match(r"^[0-9][0-9.,]*$", t):   # "46.000 euro" → €46.000
            val = {"6000": "6.000"}.get(t, t) + ("." if nxt.endswith(".") else "")
            out.append(["€" + val, s, words[i + 1][2]]); i += 2; continue
        if t == "van" and nxt == "af.":             # "van af." → vanaf.
            out.append(["vanaf.", s, words[i + 1][2]]); i += 2; continue
        if t == "zou" and 35 < s < 36: t = "zouden"
        if t == "kosten" and 53 < s < 54: t = "kost"
        if t == "4" and 50 < s < 51: t = "€4.000"
        if t == "40" and 54 < s < 55: t = "€40.000"
        t = REP.get(t, t)
        out.append([t, s, e]); i += 1
    return out


WORDS = fix(W)

# ---------- beeld-zone ----------
HOOK_END = 4.15
CTA_START = 79.1
BON = [  # (regel, prijs, tijd dat de naam verschijnt = moment dat Peter het noemt)
    ("Spouw isoleren", "€3k – 5k", 18.72),
    ("Dak isoleren (binnen)", "€4k – 7k", 20.88),
    ("Vloer isoleren", "€1,5k – 3k", 22.80),
    ("HR++ glas", "€5k – 8k", 24.16),
    ("Ventilatie (type C)", "€3k – 5k", 29.20),
    ("Hybride warmtepomp", "€8,5k – 12k", 31.76),
    ("10–12 zonnepanelen", "€5k – 6k", 35.92),
    ("Batterij 10–15 kWh", "€6k – 10k", 41.52),
]
bon_html = '<div class="label">Het plan</div>' + "".join(
    f'<div class="row r{i+1}"><span class="n">{n}</span><span class="p p{i+1}">{p}</span></div>' for i, (n, p, _) in enumerate(BON)
) + '<div class="tot"><span>Totaal</span><span class="p">± €46.000</span></div>'
# prijzen verschijnen tijdens "Dit zijn de kosten daarvan" (44.2–45.6), totaal bij "46.000" (48.16)
bon_pop = [[f".r{i+1}", t] for i, (_, _, t) in enumerate(BON)] + [[f".p{i+1}", round(44.6 + 0.16 * i, 2)] for i in range(len(BON))] + [[".tot", 48.1]]

BEELDEN = [
    # 1 Eerste shot: Funda-foto + serie-label; prijs/feiten pas bij "Een villa uit 1953" (10.4)
    {"start": 0.0, "end": 12.92, "html": '<img src="assets/huis.jpg"><div class="badge">Funda Fixer <b>#5</b></div>'
     '<div class="tagbar t1"><span class="price">€ 795.000 <small>k.k.</small></span><span class="meta">Villa · Rheden · 1953 · Label G</span></div>',
     "pop": [[".t1", 10.4]]},
    # 2 Calculator (D07-schermopname, vertraagd naar 4,3 s)
    {"start": 12.9, "end": 17.36, "el": "#calc-card", "pop": []},
    # 3 Het plan — bonnetje; namen tijdens het plan, prijzen bij "Dit zijn de kosten", totaal bij "46.000"
    {"start": 17.34, "end": 49.3, "cls": "bon", "html": bon_html, "pop": bon_pop},
    # 4 Subsidie + netto
    {"start": 49.4, "end": 56.95, "html": '<div class="label">Kosten</div><div class="value">± €46.000</div>'
     '<div class="sub s1">− €4.000 à €6.000 subsidie</div><div class="net s2">Netto: <b>± €40.000 – €42.000</b></div>'
     '<div class="note s1">Schatting. Check subsidie op rvo.nl</div>', "pop": [[".s1", 50.1], [".s2", 54.7]]},
    # 5 Energie per maand
    {"start": 57.05, "end": 68.8, "html": '<div class="label">Energie per maand</div><div class="line m1">Nu: <b class="dim">± €325</b></div>'
     '<div class="line m2">Straks: <b class="acc">± €110</b></div><div class="line m3">Besparing: <b class="acc">€215</b> per maand</div>',
     "pop": [[".m1", 59.15], [".m2", 64.0], [".m3", 67.2]]},
    # 6 Fixscore
    {"start": 68.85, "end": 73.7, "html": '<div class="label">Fixscore <span style="text-transform:none;letter-spacing:0">· hoger = makkelijker</span></div>'
     '<div class="value f0">6<span class="of">/10</span></div><div class="line f1">✓ Isolatie goed bereikbaar</div>',
     "pop": [[".f0", 69.8], [".f1", 70.75]]},
]

PUNCH = [[4.25, 1.14], [10.14, 1.0], [12.9, 1.14], [17.34, 1.0], [22.7, 1.14], [27.3, 1.0], [31.0, 1.14], [35.0, 1.0], [40.1, 1.14], [44.2, 1.0],
         [49.4, 1.14], [52.4, 1.0], [57.05, 1.14], [62.3, 1.0], [68.85, 1.14], [73.9, 1.22], [79.1, 1.14]]

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
head = re.sub(r"<!--.*?-->", "<!--\n  D17 · Funda Fixer #5 — Arnhemsestraatweg, Rheden (versie A)\n  Sardo-format (zie ../../SARDO_FORMAT.md). Gegenereerd door build.py — pas build.py aan, niet dit bestand.\n-->", head, count=1, flags=re.S)
head = re.sub(r'data-duration="[0-9.]+"', f'data-duration="{DUR}"', head)
head = re.sub(r'(src="assets/calc-slow.mp4" muted playsinline) data-start="[0-9.]+" data-duration="[0-9.]+"', r'\1 data-start="12.9" data-duration="4.32"', head)
head = head.replace("/* Bonnetje", ".beeld .badge { position: absolute; left: 28px; top: 28px; padding: 14px 28px; border-radius: 999px; background: var(--brand-accent); color: var(--brand-bg); font-size: 40px; font-weight: 800; letter-spacing: 0.01em; box-shadow: 0 6px 20px rgba(0,0,0,0.35); }\n      .beeld .badge b { font-weight: 800; }\n      .beeld .tagbar .price small { font-size: 34px; font-weight: 700; color: var(--brand-text-dim); }\n      /* Bonnetje")
cfg = "const CONFIG = " + json.dumps(CONFIG, ensure_ascii=False) + ";\n      "
open("index.html", "w").write(head + cfg + tail)
print("index.html geschreven · duur", DUR, "s ·", len(WORDS), "woorden")
json.dump(CONFIG, open("work/config.json", "w"), ensure_ascii=False, indent=1)

#!/usr/bin/env python3
"""D17 · Funda Fixer #5 — Rheden (versie A v2, ±99,7 s, alleen hele zinnen).
Bouwt index.html uit work/template-arnhem.html + CONFIG. Draai: python3 build.py  (dan: npx hyperframes render ...)
Bron: assets/source.mp4 = work/concat.sh (17 hele-zin-stukken uit work/seg, EDL in work/edl.json).
"""
import json, re, subprocess

DUR = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/source.mp4"]).decode().strip()), 2)

# ---------- woorden (Parakeet-transcript van assets/source.mp4; tijden blijven, tekst handmatig verbeterd) ----------
raw = json.load(open("work/source-words.json"))
W = [[x["text"], x["start"], x["end"]] for x in raw]

REP = {"fila": "villa", "reden": "Rheden", "spawn": "spouw", "microonvormers": "micro-omvormers", "schuide": "schuine",
       "Zodat": "zodat", "calculator.": "calculator,", "kW.": "kWh,", "Om": "om", "koop": "koopt", "geschatten": "geschatte",
       "maandelijk": "maandelijkse", "Fictiescore": "Fixscore", "funnelink": "Funda-link", "check": "CHECK", "woning": "woning",
       "Alright.": "Wat"}
# v2 (8 nov, avond): alleen hele zinnen; adres en "Funda Fixer nummer 5" niet meer in de audio (badge in beeld).


def euro(num):
    n = num.rstrip(".").replace(".", "")
    return "€" + (f"{int(n):,}".replace(",", ".") if n.isdigit() else n)


def fix(words):
    out = []
    i = 0
    while i < len(words):
        t, s, e = words[i]
        nxt = words[i + 1][0] if i + 1 < len(words) else ""
        if t == "Alright.": i += 1; continue                       # ademhaling vóór "Wat wij…"
        if t == "viaden":                                            # "villa in Rheden" als één woord gehoord
            out += [["villa", s, s + 0.4], ["in", s + 0.4, s + 0.56], ["Rheden", s + 0.56, e]]; i += 1; continue
        if t == "in" and nxt == "die" and 12.5 < s < 13.5:           # "in die jaar bezig is." → "indien aanwezig."
            out += [["indien", s, words[i + 2][1]], ["aanwezig.", words[i + 2][1], words[i + 4][2]]]; i += 5; continue
        if t == "woning" and 15.0 < s < 15.1:
            m = (s + e) / 2; out += [["woning", s, m], ["uit", m, e]]; i += 1; continue
        if t == "binnen" and nxt == "uit":
            out.append(["binnenuit", s, words[i + 1][2]]); i += 2; continue
        if t == "HR" and nxt.lower() == "plus":
            out.append(["HR++", s, words[i + 2][2]]); i += 3; continue
        if t == "je" and nxt == "ook" and s > 88:                    # "Heb je nu ook net…" (nu niet gehoord)
            m = (s + e) / 2; out += [["je", s, m], ["nu", m, e]]; i += 1; continue
        if t == "kosten" and nxt == "dit": t = "kost"
        if re.match(r"^[0-9][0-9.]*$", t) and nxt.startswith("euro"):
            out.append([euro(t) + ("." if nxt.endswith(".") else ""), s, words[i + 1][2]]); i += 2; continue
        if re.match(r"^[0-9]{1,2}$", t) and nxt == "tot" and i + 2 < len(words) and len(words[i + 2][0].rstrip(".").replace(".", "")) >= 4:
            t = euro(t + "000")
        t = REP.get(t, t)
        for (lo, hi, x, y) in KOMMA:
            if lo <= s <= hi and t == x: t = y
        out.append([t, s, e]); i += 1
    return out


REP = {"minuten.": "minuut.", "span": "spouw", "microonvormers": "micro-omvormers", "schuide": "schuine", "Zodat": "zodat",
       "calculator.": "calculator,", "kW.": "kWh,", "Om": "om", "keto": "ketel", "maandelijks": "maandelijkse",
       "Fictiescore": "Fixscore", "funnelink": "Funda-link", "check": "CHECK"}
KOMMA = [(8.7, 8.9, "het", "de"), (14.4, 14.5, "wel.", "wel,"), (14.6, 14.7, "Want", "want"), (28.3, 28.4, "komen.", "komen,"),
         (28.6, 28.7, "Dus", "dus"), (32.7, 32.9, "C", "C."), (33.5, 33.6, "dan", "Dan"), (91.7, 91.8, "mij.", "mij,"), (91.9, 92.0, "Dan", "dan")]


WORDS = fix(W)

# ---------- beeld-zone ----------
HOOK_END = 4.05
CTA_START = 93.4   # "Of reageer CHECK" (93.49) tot het einde
BON = [  # (regel, prijs, tijd dat Peter het noemt)
    ("Spouw isoleren", "€3k – 5k", 11.8),
    ("Dak isoleren (binnen)", "€4k – 7k", 18.92),
    ("Vloer isoleren", "€1,5k – 3k", 20.84),
    ("HR++ glas", "€5k – 8k", 22.12),
    ("Ventilatie (type C)", "€3k – 5k", 27.16),
    ("Hybride warmtepomp", "€8,5k – 12k", 34.28),
    ("10–12 zonnepanelen", "€5k – 6k", 38.12),
    ("Batterij 10–15 kWh", "€6k – 10k", 47.32),
]
bon_html = '<div class="label">Het plan</div>' + "".join(
    f'<div class="row r{i+1}"><span class="n">{n}</span><span class="p p{i+1}">{p}</span></div>' for i, (n, p, _) in enumerate(BON)
) + '<div class="tot"><span>Totaal</span><span class="p">± €46.000</span></div>'
# prijzen tijdens "Dit zijn de kosten daarvan" (54.76–56.6), totaal bij "43.4" (58.77)
bon_pop = [[f".r{i+1}", t] for i, (_, _, t) in enumerate(BON)] + [[f".p{i+1}", round(54.9 + 0.18 * i, 2)] for i in range(len(BON))] + [[".tot", 58.75]]

BEELDEN = [
    # 1 Eerste shot (hook): alleen Funda-foto + serie-label; prijs/feiten na de hook (4.1), tijdens "We gaan hem eerst even…"
    {"start": 0.0, "end": 6.2, "html": '<img src="assets/huis.jpg"><div class="badge">Funda Fixer <b>#5</b></div>'
     '<div class="tagbar t1"><span class="price">€ 795.000 <small>k.k.</small></span><span class="meta">Villa · Rheden · 1953 · Label G</span></div>',
     "pop": [[".t1", 4.1]]},
    # 2 Calculator (D07-schermopname, vertraagd naar 6,35 s) tijdens de calculator-zin
    {"start": 6.15, "end": 10.42, "el": "#calc-card", "pop": []},
    # 3 Het plan — bonnetje
    {"start": 10.4, "end": 60.1, "cls": "bon", "html": bon_html, "pop": bon_pop},
    # 4 Subsidie + netto
    {"start": 60.05, "end": 69.95, "html": '<div class="label">Kosten</div><div class="value">± €46.000</div>'
     '<div class="sub s1">− €4.000 à €6.000 subsidie</div><div class="net s2">Netto: <b>± €40.000 – €42.000</b></div>'
     '<div class="note s1">Schatting. Check subsidie op rvo.nl</div>', "pop": [[".s1", 60.69], [".s2", 67.3]]},
    # 5 Energie per maand
    {"start": 69.9, "end": 82.85, "html": '<div class="label">Energie per maand</div><div class="line m1">Nu: <b class="dim">± €325</b></div>'
     '<div class="line m2">Straks: <b class="acc">± €110</b></div><div class="line m3">Besparing: <b class="acc">€215</b> per maand</div>',
     "pop": [[".m1", 71.97], [".m2", 78.21], [".m3", 81.4]]},
    # 6 Fixscore
    {"start": 82.8, "end": 88.15, "html": '<div class="label">Fixscore <span style="text-transform:none;letter-spacing:0">· hoger = makkelijker</span></div>'
     '<div class="value f0">6<span class="of">/10</span></div><div class="line f1">✓ Isolatie goed bereikbaar</div>',
     "pop": [[".f0", 84.21], [".f1", 85.09]]},
]

_t = [4.05, 7.3, 10.4, 13.96, 18.23, 22.08, 25.08, 28.68, 33.23, 37.28, 42.92, 45.93, 49.8, 54.28, 56.71, 60.13, 64.81, 69.91, 74.93, 76.41, 79.33, 82.81, 85.09]
PUNCH = [[t, 1.14 if i % 2 == 0 else 1.0] for i, t in enumerate(_t)] + [[88.15, 1.22], [93.4, 1.14]]   # Peter vol in beeld: ≥1.14 (geen donkere band)

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
head = re.sub(r'(src="assets/calc-slow.mp4" muted playsinline) data-start="[0-9.]+" data-duration="[0-9.]+"', r'\1 data-start="6.15" data-duration="4.27"', head)
head = head.replace("/* Bonnetje", ".beeld .badge { position: absolute; left: 28px; top: 28px; padding: 14px 28px; border-radius: 999px; background: var(--brand-accent); color: var(--brand-bg); font-size: 40px; font-weight: 800; letter-spacing: 0.01em; box-shadow: 0 6px 20px rgba(0,0,0,0.35); }\n      .beeld .badge b { font-weight: 800; }\n      .beeld .tagbar .price small { font-size: 34px; font-weight: 700; color: var(--brand-text-dim); }\n      /* Bonnetje")
cfg = "const CONFIG = " + json.dumps(CONFIG, ensure_ascii=False) + ";\n      "
open("index.html", "w").write(head + cfg + tail)
print("index.html geschreven · duur", DUR, "s ·", len(WORDS), "woorden")
json.dump(CONFIG, open("work/config.json", "w"), ensure_ascii=False, indent=1)

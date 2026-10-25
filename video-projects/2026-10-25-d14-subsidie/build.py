#!/usr/bin/env python3
"""Bouwt per hook-versie (A/B/C) een Hyperframes-project vanuit comp.html + transcripts."""
import json, re, shutil, subprocess, os

P = "/home/claude/hyperframes-colton.ai.dean/video-projects/2026-10-25-d14-subsidie"
TPL = "/home/claude/hyperframes-colton.ai.dean/templates/sardo-format"
SFX = "/home/claude/hyperframes-colton.ai.dean/assets/sfx/ui/pop.mp3"

def load(f):
    d = json.load(open(f"{P}/work/tr/{f}.json"))
    return d if isinstance(d, list) else d["words"]

def dur(f, stream="v"):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", f"{stream}:0",
                                   "-show_entries", "stream=duration", "-of", "csv=p=0", f]).decode()
    return float(out.strip())

FIX = {"warmtepom": "warmtepomp", "aanbod": "AANBOD", "totdat": "totdat"}

def clean(ws, off):
    out, skip = [], False
    for i, w in enumerate(ws):
        if skip:
            skip = False; continue
        t = w["text"]
        base = re.sub(r"[.,]$", "", t)
        s, e = w["start"] + off, w["end"] + off
        if base in ("25", "120") and i + 1 < len(ws) and ws[i + 1]["text"].startswith("euro"):
            base = "€225" if base == "25" else "€120"
            e = ws[i + 1]["end"] + off; skip = True
        base = FIX.get(base, base)
        end = 1 if re.search(r"[.?!,]$", (ws[i+1]["text"] if base in ("€225","€120") else t)) else 0
        out.append([base, round(s, 3), round(e, 3), end])
    return out

body = load("body")
html = open(f"{P}/comp.html").read()
for X in "ABC":
    H = dur(f"{P}/assets/hook-{X}.mp4")
    total = dur(f"{P}/assets/full-{X}.mp4")
    words = clean(load(f"hook-{X}"), 0) + clean(body, H)
    d = f"{P}/{X}"
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(f"{d}/assets")
    for f in ["hyperframes.json", "package.json"]:
        shutil.copy(f"{TPL}/{f}", d)
    json.dump({"id": f"d14-subsidie-{X}", "name": f"D14 subsidie {X}"}, open(f"{d}/meta.json", "w"))
    shutil.copytree(f"{TPL}/assets/fonts", f"{d}/assets/fonts")
    shutil.copytree(f"{TPL}/assets/vendor", f"{d}/assets/vendor")
    shutil.copy(f"{TPL}/assets/brand-tokens.css", f"{d}/assets/")
    shutil.copy(SFX, f"{d}/assets/pop.mp3")
    os.link(f"{P}/assets/full-{X}.mp4", f"{d}/assets/source.mp4")
    hp = {"A": [3.2], "B": [1.76, 5.6], "C": [0.8]}[X]
    pops = hp + [H + t for t in (4.08, 17.12, 29.68, 44.72, 47.68)]
    audio = "\n".join(f'      <audio id="pop{i}" src="assets/pop.mp3" data-start="{t:.2f}" data-duration="0.7" data-track-index="{10+i}" data-volume="0.3"></audio>' for i, t in enumerate(pops))
    out = (html.replace("__AUDIO__", audio).replace("__VERSION__", X).replace("__H__", f"{H:.3f}")
               .replace("__TOTAL__", f"{total:.3f}").replace("__WORDS__", json.dumps(words, ensure_ascii=False)))
    open(f"{d}/index.html", "w").write(out)
    print(X, "hook", H, "totaal", total, "woorden", len(words))

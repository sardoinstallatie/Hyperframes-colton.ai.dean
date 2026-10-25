#!/usr/bin/env python3
"""D14 subsidie — knipt hooks en body uit de 5 bron-chunks op woordniveau."""
import json, subprocess, sys

P = "/home/claude/hyperframes-colton.ai.dean/video-projects/2026-10-25-d14-subsidie"
CHUNKS = [("c1", 5, 33), ("c2a", 52, 73), ("c2b", 73, 94), ("c3", 96, 113.5), ("c4", 197, 209.45)]
words = json.load(open(f"{P}/assets/transcript.json"))
words = words if isinstance(words, list) else words["words"]

# Te houden stukken (bron-tijd van eerste/laatste woord-start)
PARTS = {
    "hook-A": [(5.52, 10.96)],
    "hook-B": [(15.68, 24.00)],
    "hook-C": [(27.76, 31.60)],
    "body": [
        (53.04, 56.80),   # Denk aan een warmtepomp... (take 2)
        (59.43, 66.79),   # Nu in 2026 ... €225 per kW
        (68.31, 71.91),   # Vanaf januari 2027 ... 120 per kW  (helft-zin eruit)
        (79.59, 93.19),   # uitzondering op de regel ... dat geeft niet
        (97.35, 112.63),  # offerte, tekenen, aanbetalen = bewijs
        (198.17, 209.05), # CTA aanbod
    ],
}
GAP, PRE, POST = 0.30, 0.08, 0.10

def segs(rng):
    out = []
    for a, b in rng:
        ws = [w for w in words if a - 0.01 <= w["start"] <= b + 0.01]
        cur = [ws[0]]
        for w in ws[1:]:
            if w["start"] - cur[-1]["end"] > GAP:
                out.append(cur); cur = [w]
            else:
                cur.append(w)
        out.append(cur)
    res = []
    for g in out:
        s, e = g[0]["start"] - PRE, g[-1]["end"] + POST
        nxt = [w for w in words if w["start"] >= g[-1]["end"] - 0.001 and w not in g]
        if nxt:
            e = min(e, nxt[0]["start"] - 0.02)
        prv = [w for w in words if w["end"] <= g[0]["start"] + 0.001 and w not in g]
        if prv:
            s = max(s, prv[-1]["end"] + 0.02)
        res.append((round(s, 3), round(e, 3), " ".join(w["text"] for w in g)))
    return res

def chunk_for(s, e):
    for name, off, end in CHUNKS:
        if off <= s and e <= end:
            return name, off
    sys.exit(f"geen chunk voor {s}-{e}")

edl = ["# EDL — D14 subsidie (bron = DJI_20261025112138_0089_D.MP4)\n",
       "Weg: slate (0–5 s), hook-C staart (32–42 s), take 1 'Denk je aan…' (46–51 s),",
       "'Dat is meer dan de helft…' (72,8–78 s), bonus-stuk smart-grid/A+++ (123–194 s), alle stiltes >0,3 s.\n"]
for part, rng in PARTS.items():
    ss = segs(rng)
    inputs, filt = [], []
    for i, (s, e, txt) in enumerate(ss):
        name, off = chunk_for(s, e)
        inputs += ["-i", f"{P}/raw-media/{name}.mp4"]
        d = e - s
        filt.append(f"[{i}:v]trim={s-off:.3f}:{e-off:.3f},setpts=PTS-STARTPTS,fps=25[v{i}];"
                    f"[{i}:a]atrim={s-off:.3f}:{e-off:.3f},asetpts=PTS-STARTPTS,"
                    f"afade=t=in:d=0.012,afade=t=out:st={d-0.015:.3f}:d=0.015[a{i}];")
    n = len(ss)
    fc = "".join(filt) + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    out = f"{P}/assets/{part}.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "25", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    edl.append(f"\n## {part}")
    edl += [f"- {s:7.2f}–{e:7.2f}  {t}" for s, e, t in ss]
    print(part, n, "segmenten")
open(f"{P}/EDL.md", "w").write("\n".join(edl) + "\n")

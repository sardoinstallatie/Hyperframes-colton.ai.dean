import os, subprocess, json
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'raw/source.mp4')
OUT = os.path.join(ROOT, 'work/cut'); os.makedirs(OUT, exist_ok=True)

# Stukken die blijven, in RUWE tijd (zie EDL.md)
KEEP = [
    (1.68, 6.30),    # Is jouw woning deels geïsoleerd ... klaar voor een warmtepomp?  ("Nou," eruit)
    (7.88, 23.45),   # Voordat de echte koude dagen ... temperatuur die je graag zou willen.  ("Wat kan doen" eruit)
    (25.50, 56.75),  # Dan weet je dat je ready bent ... meteen aan de gang.  ("Als je woning dan warm blijft." = dubbel, eruit)
    (58.15, 58.72),  # Ciao!
]
PAD = 0.08
sil = [tuple(map(float, l.split())) for l in open(os.path.join(ROOT, 'work/sil.txt'))]
# stiltes die dicht op elkaar liggen samenvoegen (ademhaling ertussen)
m = []
for a, b in sil:
    if m and a - m[-1][1] < 0.15: m[-1][1] = b
    else: m.append([a, b])

def tighten(s, e):
    pieces = [[s, e]]
    for ss, se in m:
        if se - ss < 0.25: continue
        new = []
        for a, b in pieces:
            if se <= a or ss >= b: new.append([a, b]); continue
            if ss > a: new.append([a, min(b, ss + PAD)])
            if se < b: new.append([max(a, se - PAD), b])
        pieces = new
    return [[round(a, 3), round(b, 3)] for a, b in pieces if b - a >= 0.12]

parts = [p for s, e in KEEP for p in tighten(s, e)]
lst = []
for k, (a, b) in enumerate(parts):
    d = b - a; p = os.path.join(OUT, f'p{k:02d}.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', SRC, '-t', f'{d:.3f}',
        '-af', f'afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-r', '25', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', p], check=True)
    lst.append(f"file '{p}'")
open(os.path.join(OUT, 'list.txt'), 'w').write('\n'.join(lst) + '\n')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'list.txt'),
                '-c', 'copy', '-movflags', '+faststart', os.path.join(ROOT, 'work/full.mp4')], check=True)
json.dump(parts, open(os.path.join(ROOT, 'work/edl.json'), 'w'), indent=1)
print(len(parts), 'stukken', subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, 'work/full.mp4')]).decode().strip(), 's')

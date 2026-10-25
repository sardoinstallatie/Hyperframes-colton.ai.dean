import json, os, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(ROOT, 'media')
# range-bestanden: naam -> start in de ruwe opname (s)
RANGES = {'r01': 18.5, 'r02': 39.8, 'r03': 70.2, 'r04': 92.8, 'r05': 121.6, 'r06': 141.4,
          'r07': 170.5, 'r08': 222.8, 'r09': 231.8, 'r10': 265.4, 'r11': 289.7}
# segmenten in RUWE tijd (zie EDL.md)
EDL = {
  'hooks': {
    'B': [('r01', 18.96, 22.32)],
    'C': [('r01', 26.72, 31.20)],
    'D': [('r02', 40.16, 44.80)],
  },
  'body': [
    ('r03', 70.55, 74.87),   # je kan het ook spreiden over 5 jaar
    ('r03', 77.59, 80.63),   # woning heeft niks
    ('r03', 80.67, 81.91),   # dus zitten we op label F
    ('r03', 86.39, 91.19),   # in 5 jaar naar label A
    ('r04', 93.11, 97.83),   # jaar 1 isoleren
    ('r04', 97.99, 99.00),   # dat doe je als eerst
    ('r05', 121.96, 132.44), # jaar 2 glas + dak
    ('r06', 141.80, 152.04), # jaar 3 hybride, all-electric ready
    ('r07', 170.84, 173.00), # jaar 4 zonnepanelen
    ('r07', 173.00, 183.80), # na de warmtepomp, verbruik zien
    ('r08', 223.07, 225.39), # jaar 5 fijntunen
    ('r09', 232.11, 236.11), # laadpaal
    ("r09", 236.35, 237.42), # of wat je kan doen
    ('r09', 238.03, 247.95), # helemaal van het gas af ... klaar
    ('r10', 265.66, 272.22), # waarom deze volgorde
    ('r11', 289.98, 297.26), # CTA
  ],
}
SIL = [tuple(map(float, l.split())) for l in open(os.path.join(ROOT, 'work/sil.txt'))]
PAD = 0.15

def tighten(s, e):
    pieces = [[s, e]]
    for ss, se in SIL:
        if se - ss < 0.45: continue
        new = []
        for a, b in pieces:
            if se <= a or ss >= b: new.append([a, b]); continue
            left_end = ss + PAD
            right_start = se - PAD
            if ss > a: new.append([a, min(b, left_end + 0.03)])
            if se < b: new.append([max(a, right_start), b])
        pieces = new
    return [[round(a, 3), round(b, 3)] for a, b in pieces if b - a >= 0.15]

def build(segs, out):
    parts = []
    for r, s, e in segs:
        for a, b in tighten(s, e):
            parts.append((r, a - RANGES[r], b - RANGES[r], a, b))
    tmp = os.path.join(M, 'pieces'); os.makedirs(tmp, exist_ok=True)
    lst = []
    for k, (r, a, b, _, _) in enumerate(parts):
        d = b - a; p = os.path.join(tmp, f'{out[:-4]}-{k:02d}.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', os.path.join(M, r + '.mp4'), '-t', f'{d:.3f}',
            '-af', f'afade=t=in:d=0.02,afade=t=out:st={max(0,d-0.03):.3f}:d=0.03',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-r', '25', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', p], check=True)
        lst.append(f"file '{p}'")
    open(os.path.join(tmp, out + '.txt'), 'w').write('\n'.join(lst) + '\n')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(tmp, out + '.txt'), '-c', 'copy', os.path.join(M, out)], check=True)
    return [[p[3], p[4]] for p in parts]

def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(M, f)]).decode())

log = {'body': build(EDL['body'], 'body.mp4')}
for X, segs in EDL['hooks'].items():
    log[X] = build(segs, f'hook-{X}.mp4')
    with open(os.path.join(M, f'list-{X}.txt'), 'w') as fh:
        fh.write(f"file 'hook-{X}.mp4'\nfile 'body.mp4'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(M, f'list-{X}.txt'), '-c', 'copy',
                    '-movflags', '+faststart', os.path.join(M, f'full-{X}.mp4')], check=True)
json.dump(log, open(os.path.join(ROOT, 'work/edl.json'), 'w'), indent=1)
print('body', round(dur('body.mp4'), 2), {X: round(dur(f'full-{X}.mp4'), 2) for X in EDL['hooks']})

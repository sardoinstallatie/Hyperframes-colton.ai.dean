import json, os, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'assets/raw-1080.mp4')
M = os.path.join(ROOT, 'media'); os.makedirs(M, exist_ok=True)
W = [l.split(' ', 2) for l in open(os.path.join(ROOT, 'work/words.txt')).read().strip().split('\n')]
W = [(float(a), float(b), t) for a, b, t in W]

# Segmenten in RUWE tijd. Zie EDL.md
HOOK_A = [(0.10, 6.52)]   # Door dit niet te doen ... zonnepanelen gingen installeren
BODY = [
    (10.36, 14.28),   # We hadden een groepenkast aangesloten. Drie-fases systeem.
    (14.24, 17.20),   # En wat er was gebeurd is dat de nul niet helemaal vast zat
    (17.44, 20.10),   # Omdat we op zulke hoge werkdruk werkten
    (23.28, 25.80),   # waardoor je niet genoeg tijd kon nemen voor de klus
    (25.96, 28.40),   # Meten we die groepenkasten niet door
    (28.40, 30.50),   # Dus alles werd gewoon meteen aangezet
    (32.22, 37.56),   # Maar met een losse nul ... 400 volt door al je apparatuur
    (42.76, 45.40),   # Alles, echt alles was kapot bij die mensen
    (45.48, 51.56),   # Wasmachine, wasdroger, televisie, keukenapparatuur, de ketel
    (53.02, 54.18),   # Dus uiteindelijk
    (55.26, 56.48),   # zijn we naar de verzekering gegaan
    (58.22, 59.56),   # Zou je dat kunnen vergoeden?
    (60.97, 63.45),   # Je krijgt de dagprijs van alle producten
    (64.25, 68.80),   # Uiteindelijk kwam dat neer op 300 of 400 euro
    (69.15, 71.04),   # dat vonden wij natuurlijk niet kunnen
    (72.11, 74.08),   # We hebben voor die mensen alles nieuw gekocht
    (80.90, 85.28),   # Al met al kostte ons dat 7000 euro. Dat was een hele dure les.
    (85.23, 86.80),   # Maar ik heb er twee dingen van geleerd
    (88.33, 93.92),   # Ten eerste, altijd je werk blijven controleren. Ook al denk je...
    (94.90, 99.68),   # Blijf jezelf controleren, maar controleer ook elkaar...
    (99.85, 102.24),  # Vertrouw is goed, controleren is beter
    (102.19, 106.40), # En ten tweede, alles is op te lossen, zodra het maar gaat om geld
    (106.66, 111.84), # Als er niemand gewond is geraakt ... dat is het allerbelangrijkste
    (125.50, 130.20), # En zolang het materiaal is, is dat op te lossen. Dus dat was hem.
]
GAP = 0.28   # pauzes tussen woorden langer dan dit gaan eruit
PAD = 0.07

def tighten(s, e):
    ws = [w for w in W if w[0] >= s - 0.05 and w[1] <= e + 0.05]
    pieces = [[s, e]]
    for (a0, a1, _), (b0, b1, _) in zip(ws, ws[1:]):
        if b0 - a1 > GAP:
            last = pieces[-1]
            last[1] = a1 + PAD
            pieces.append([b0 - PAD, e])
    return [[round(a, 3), round(b, 3)] for a, b in pieces if b - a >= 0.12]

def build(segs, out):
    parts = []
    for s, e in segs:
        parts += tighten(s, e)
    tmp = os.path.join(M, 'pieces'); os.makedirs(tmp, exist_ok=True)
    lst = []
    for k, (a, b) in enumerate(parts):
        d = b - a; p = os.path.join(tmp, f'{out[:-4]}-{k:02d}.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', SRC, '-t', f'{d:.3f}',
            '-af', f'afade=t=in:d=0.02,afade=t=out:st={max(0,d-0.03):.3f}:d=0.03',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-r', '25', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', p], check=True)
        lst.append(f"file '{p}'")
    open(os.path.join(tmp, out + '.txt'), 'w').write('\n'.join(lst) + '\n')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(tmp, out + '.txt'), '-c', 'copy', os.path.join(M, out)], check=True)
    return parts

def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(M, f)]).decode())

log = {'body': build(BODY, 'body.mp4'), 'A': build(HOOK_A, 'hook-A.mp4')}
open(os.path.join(M, 'list-A.txt'), 'w').write("file 'hook-A.mp4'\nfile 'body.mp4'\n")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(M, 'list-A.txt'), '-c', 'copy',
                '-movflags', '+faststart', os.path.join(M, 'full-A.mp4')], check=True)
json.dump(log, open(os.path.join(ROOT, 'work/edl.json'), 'w'), indent=1)
print('hook', round(dur('hook-A.mp4'), 2), 'body', round(dur('body.mp4'), 2), 'full', round(dur('full-A.mp4'), 2), 'pieces', len(log['body']))

import json, os, shutil, subprocess, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
from house import house_svg
REPO = os.path.join(ROOT, '../..'); OUT = os.path.join(ROOT, 'A')
SRC = os.path.join(ROOT, 'raw-media/body2.mp4')
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',SRC]).decode())
D = round(dur, 3)

# woorden: transcript van body.mp4, alles na de knip (49.50–49.94) 0.44 s naar voren
FIX = {'allelekt': 'all-electric', 'spou': 'spouw', 'HR': 'HR++'}
ws = []
for x in json.load(open(os.path.join(ROOT, 'raw-media/tw-body.json'))):
    s, e = x['start'], x['end']
    if s >= 49.94: s, e = s - 0.44, e - 0.44
    elif e > 49.50: e = 49.50
    m = re.match(r'^(.*?)([.,?!]*)$', x['text']); core, p = m.group(1), m.group(2)
    ws.append([FIX.get(core, core) + p, round(s, 2), round(e, 2), bool(p)])

def at(prefix, after):
    return next(w[1] for w in ws if w[1] >= after and w[0].lower().startswith(prefix.lower()))

LAYERS = ['90','80','70','60','50','40','30','20','10']
COLORS = ['#e53935','#f4511e','#fb8c00','#ffb300','#fdd835','#c0ca33','#7cb342','#43a047','#00c853']
pct = {}
for w in ws:
    m = re.match(r'^(\d+)%', w[0])
    if m and m.group(1) not in pct: pct[m.group(1)] = w[1]
pct['10'] = [w[1] for w in ws if w[0].startswith('10%')][-1]
houseOn = {}
for prev, l in zip(LAYERS, LAYERS[1:]):
    houseOn[l] = round(next(w[1] for w in ws if w[1] > pct[prev] and w[0] in ('Heb', 'En')) + 0.2, 2)
OUTRO = at('Wil', pct['10'])
HOOK_END = 2.30; CTA_START = round(dur - 2.0, 2)
EV = dict(
    glas80=at('glas', houseOn['80']), vloer=at('vloer', houseOn['70']), spouw=at('spouw', houseOn['70']),
    dak=at('dak', houseOn['60']), weg=at('weg', houseOn['60']), hr=at('HR', houseOn['50']),
    zon=at('zonnepanelen', houseOn['40']), stroom=at('stroom', houseOn['40']),
    wp=at('warmtepomp', houseOn['30']), gas=at('gas', houseOn['30']),
    batt=at('thuisbatterij', houseOn['20']), avond=at('installeren', houseOn['20']),
    ems=at('EMS', houseOn['10']), lijnen=at('installaties', houseOn['10']), groen=at('samenwerken', houseOn['10']))

def chunks(ws):
    groups = []; cur = []
    for w in ws:
        txt = ' '.join(x[0] for x in cur + [w])
        if cur and (len(cur) >= 3 or len(txt) > 19): groups.append(cur); cur = []
        cur.append(w)
        if w[3]: groups.append(cur); cur = []
    if cur: groups.append(cur)
    g2 = []
    for g in groups:
        if g2 and len(g2[-1]) == 1 and len(g2[-1][0][0]) <= 3 and not g2[-1][0][3]: g2[-1] = g2[-1] + g
        else: g2.append(g)
    return g2
groups = chunks([w for w in ws if w[1] >= HOOK_END - 0.05 and w[1] < CTA_START])

# piramide
TOP_Y, BASE_Y, GAP, BASE_W, TOP_W = 260, 915, 9, 880, 150
n = len(LAYERS); bh = (BASE_Y - TOP_Y - GAP*(n-1)) / n
wa = lambda y: TOP_W + (BASE_W - TOP_W) * (y - TOP_Y) / (BASE_Y - TOP_Y)
bands = ''
for i, lab in enumerate(LAYERS):
    y1 = BASE_Y - i*(bh+GAP); y0 = y1 - bh; w0, w1 = wa(y0), wa(y1); inset = (w1 - w0) / 2 / w1 * 100
    bands += (f'<div class="band" id="b{lab}" style="left:{540-w1/2:.1f}px;top:{y0:.1f}px;width:{w1:.1f}px;height:{bh:.1f}px;--c:{COLORS[i]};'
              f'clip-path:polygon({inset:.2f}% 0,{100-inset:.2f}% 0,100% 100%,0 100%)"><div class="fill"></div><div class="lab" style="font-size:{min(60,bh*0.75):.0f}px">±{lab}%</div></div>')
heads = ''.join(f'<div class="head" id="hd{l}" style="color:{COLORS[i]}">TOP {l}%{" <span class=tro>🏆</span>" if False else ""}</div>' for i, l in enumerate(LAYERS))
trophy = '''<svg id="trophy" viewBox="0 0 200 150"><path d="M60 10 H140 V55 C140 85 120 100 100 100 C80 100 60 85 60 55 Z" fill="#ffc83d" stroke="#111" stroke-width="6"/><path d="M60 22 H32 C32 52 45 62 62 62 M140 22 H168 C168 52 155 62 138 62" fill="none" stroke="#ffc83d" stroke-width="10" stroke-linecap="round"/><rect x="90" y="98" width="20" height="22" fill="#ffc83d" stroke="#111" stroke-width="5"/><rect x="66" y="118" width="68" height="20" rx="4" fill="#ffc83d" stroke="#111" stroke-width="6"/></svg>'''

outro = (f'<div id="outro"><div class="oh" id="oh1"><div class="ohs">{house_svg("r-","red")}</div><div class="ol" style="color:#e53935">TOP 90%</div></div>'
         f'<div id="oarrow">➜</div>'
         f'<div class="oh" id="oh2"><div class="ohs">{house_svg("g-","green")}</div><div class="ol" style="color:#00c853">TOP 10%</div></div></div>')

cuts = [0, 4.92, 7.92, 11.64, 16.42, 22.00, 26.60, 31.28, 37.56, 49.50]
punch = [[t, 1.0 if i % 2 == 0 else 1.12] for i, t in enumerate(cuts)]
dings = [round(pct[l], 2) for l in LAYERS]
sfx = ''.join(f'\n      <audio id="ding{i}" src="assets/pop.mp3" data-start="{t}" data-duration="0.6" data-track-index="{10+i}" data-volume="0.28"></audio>' for i, t in enumerate(dings[:-1]))
sfx += f'\n      <audio id="dingtop" src="assets/ding.mp3" data-start="{dings[-1]}" data-duration="1.5" data-track-index="30" data-volume="0.35"></audio>'

cfg = dict(duration=D, hookEnd=HOOK_END, ctaStart=CTA_START, outro=OUTRO,
           groups=[[[w[0], w[1], w[2]] for w in g] for g in groups],
           layers=LAYERS, pct=pct, houseOn=houseOn, ev=EV, punch=punch)

html = open(os.path.join(ROOT, 'tpl.html')).read()
for k, v in dict(D=str(D), SFX=sfx, BANDS=bands, HEADS=heads, TROPHY=trophy, HOUSE=house_svg('h-', 'anim'), OUTRO=outro, CFG=json.dumps(cfg)).items():
    html = html.replace('%%' + k + '%%', v)

if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(os.path.join(REPO, 'templates/sardo-format'), OUT)
os.remove(os.path.join(OUT, 'index.html')); os.remove(os.path.join(OUT, 'assets/source.mp4'))
shutil.copy(SRC, os.path.join(OUT, 'assets/source.mp4'))
shutil.copy(os.path.join(REPO, 'assets/sfx/ui/pop.mp3'), os.path.join(OUT, 'assets/pop.mp3'))
shutil.copy(os.path.join(REPO, 'assets/sfx/ui/notification.mp3'), os.path.join(OUT, 'assets/ding.mp3'))
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print('dur', D, 'outro', OUTRO, 'houseOn', houseOn, '\nev', EV, '\npct', pct)

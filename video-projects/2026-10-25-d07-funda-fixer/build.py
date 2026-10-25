import json, os, shutil, subprocess, re
ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, '../../templates/sardo-format')
EDL = json.load(open(os.path.join(ROOT, 'work/edl.json')))
HUIS = '/mnt/user-data/uploads/Schermafbeelding_2026-10-25_om_12_19_48.png'
SFX = os.path.join(ROOT, '../2026-10-25-d02-3-budgetten/A/assets/pop.mp3')
M = os.path.join(ROOT, 'media')

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())

def words(name):
    d = json.load(open(os.path.join(M, f'tr-{name}/transcript.json')))
    return [[w['text'], w['start'], w['end']] for w in (d if isinstance(d, list) else d['words'])]

FIX = {'1930.': 'jaren 30.', 'Arnem.': 'Arnhem.', 'Spanmuisoleren,': 'Spouw isoleren,', 'vloeisoleren,': 'vloer isoleren,',
       'haar': 'HR++', 'al': 'all-electric', 'electromtepomp': 'warmtepomp', 'ken': 'ketel', 'gijzer': 'geiser',
       'kW.': 'kWh.', '35': '€325', '52.000': '€52.000', '7000': '€7.000', '450': '€450', '125': '€125',
       'nieu': 'nieuwe', 'opgeteld.': 'opgeteld,', 'Ga': 'ga', 'aanbod.': 'AANBOD.', 'zo\'n': 'zo\'n', 'Check': 'Check'}
DROP_BODY = {'Nou,', 'We'}  # restjes van weggeknipte woorden bij de cuts

def clean(ws, drop=()):
    out = []
    i = 0
    while i < len(ws):
        t, s, e = ws[i]
        if t == 'Nou,' and t in drop:
            i += 1; continue
        if t == 'We' and t in drop and out and out[-1][0].startswith('ingevuld'):
            i += 1; continue
        if t in ('plus',) and out and out[-1][0] == 'HR++':
            out[-1][2] = e; i += 1; continue
        t = FIX.get(t, t)
        # "€52.000 euro" -> "€52.000"
        if t.startswith('€') and i + 1 < len(ws) and ws[i + 1][0].lower().startswith('euro'):
            tail = ws[i + 1][0][4:]
            e = ws[i + 1][2]; t = t + tail; i += 1
        end = t.endswith(('.', '?', ','))
        t = t.rstrip('.,') if not t.endswith('?') else t
        out.append([t, round(s, 2), round(e, 2), end])
        i += 1
    return out

HOOKS = {
    'A': '<span class="hl">Label F ➜ A</span><br>in 1 minuut',
    'B': 'Huis met <span class="hl">label F</span><br>kopen?',
}
# beeld-zone, tijden in body.mp4
BEELD = [
    {'start': 0.10, 'end': 3.35, 'type': 'img', 'src': 'assets/huis.png', 'tag': 'Hoekhuis · jaren 30 · Arnhem',
     'chips': ['Label F', 'Cv-ketel 1995', 'Deels dubbel glas']},
    {'start': 3.40, 'end': 5.40, 'type': 'video', 'src': 'assets/scherm.mp4'},
    {'start': 5.45, 'end': 13.35, 'type': 'kaart', 'label': 'Stap 1', 'value': 'Huis dicht',
     'lines': [['Spouw isoleren', 6.56], ['Vloer isoleren', 7.76], ['Dak isoleren', 9.04], ['HR++ glas', 10.9]]},
    {'start': 13.45, 'end': 22.55, 'type': 'kaart', 'label': 'Stap 2', 'value': 'Van het gas af',
     'lines': [['Vloerverwarming', 13.52], ['Warmtepomp', 17.84], ['Ketel en geiser eruit', 19.55]]},
    {'start': 22.65, 'end': 30.0, 'type': 'kaart', 'label': 'Stap 3', 'value': 'Eigen stroom',
     'lines': [['Zonnepanelen voorkant', 22.72], ['Thuisbatterij 10–20 kWh', 26.48]]},
    {'start': 30.1, 'end': 35.45, 'type': 'kaart', 'label': 'Energielabel', 'value': 'F <span class="arrow">➜</span> A', 'big': True},
    {'start': 35.55, 'end': 43.9, 'type': 'kaart', 'label': 'Kosten (schatting)', 'value': '€52.000',
     'lines': [['Incl. btw', 36.4], ['Subsidie €5.000–7.000', 40.4]]},
    {'start': 44.0, 'end': 58.4, 'type': 'kaart', 'label': 'Energie per maand', 'value': '',
     'lines': [['Nu: €450', 46.96], ['Straks: €125', 51.28], ['Winst: €325 per maand', 55.92]]},
]

# body cuts (EDL-volgorde, met de twee fragment-knips verwerkt) -> punch-ins
cuts = []; acc = 0
for s, e in EDL['body']:
    cuts.append(acc); acc += e - s
def adj(t):
    return t - 0.2 if t > 5.3 else t
cuts = [round(adj(c) - (0.2 if c > 10.4 else 0), 2) for c in cuts]

def punch(off, total, cta_start):
    pts = [[0, 1.0]]; last = 0; big = False
    for c in cuts + [round(dur(os.path.join(M, 'body.mp4')), 2)]:
        t = round(off + c, 2)
        if t - last >= 3.0 and t < total - 0.5:
            big = not big; pts.append([t, 1.12 if big else 1.0]); last = t
    return pts

def groups(ws):
    g = []; cur = []
    for i, w in enumerate(ws):
        cur.append(i)
        if w[3] or len(cur) == 3 or (i + 1 < len(ws) and ws[i + 1][1] - w[2] > 0.6):
            g.append(cur); cur = []
    if cur: g.append(cur)
    return g

TEMPLATE = open(os.path.join(TPL, 'index.html')).read()
bdur = dur(os.path.join(M, 'body.mp4'))
for X in 'AB':
    d = os.path.join(ROOT, X)
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(TPL, d)
    os.remove(os.path.join(d, 'assets/source.mp4'))
    os.link(os.path.join(M, f'full-{X}.mp4'), os.path.join(d, 'assets/source.mp4'))
    shutil.copy(HUIS, os.path.join(d, 'assets/huis.png'))
    shutil.copy(os.path.join(M, 'scherm.mp4'), os.path.join(d, 'assets/scherm.mp4'))
    shutil.copy(SFX, os.path.join(d, 'assets/pop.mp3'))
    total = round(dur(os.path.join(d, 'assets/source.mp4')) - 0.04, 2)
    off = round(dur(os.path.join(M, f'hook-{X}.mp4')), 2)
    coff = round(off + bdur, 2)
    bw = [[t, round(s + off, 2), round(e + off, 2), x] for t, s, e, x in clean(words('body'), DROP_BODY)]
    cw = [[t, round(s + coff, 2), round(e + coff, 2), x] for t, s, e, x in clean(words('cta-seg'))]
    reageer = next(s for t, s, e, x in cw if t.lower().startswith('reageer'))
    cta_start = round(reageer, 2)
    beelden = []
    for b in BEELD:
        nb = dict(b); nb['start'] = round(b['start'] + off, 2); nb['end'] = round(min(b['end'], bdur - 0.05) + off, 2)
        if 'lines' in b: nb['lines'] = [[l, round(t + off, 2)] for l, t in b['lines']]
        beelden.append(nb)
    cfg = {'duration': total, 'faceOffsetY': 0, 'hook': {'text': HOOKS[X], 'end': round(off - 0.05, 2)},
           'cta': {'word': 'AANBOD', 'start': cta_start},
           'words': [w[:3] for w in bw + cw if w[1] < cta_start],
           'groups': groups([w for w in bw + cw if w[1] < cta_start]), 'chunkSize': 3, 'beelden': beelden,
           'punchIns': punch(off, total, cta_start)}
    html = TEMPLATE
    html = re.sub(r'const CONFIG = \{.*?\n      \};', 'const CONFIG = ' + json.dumps(cfg, ensure_ascii=False) + ';', html, flags=re.S)
    html = html.replace('data-duration="6"', f'data-duration="{total}"')
    html = html.replace('</style>', '''
      .beeld.img { padding: 0; border: 0; }
      .beeld.vid { padding: 0; border: 0; background: #fff; }
      .beeld.vid video { object-position: 50% 0%; }
      .beeld .tag { position: absolute; left: 24px; bottom: 24px; background: rgba(25,25,30,0.88); padding: 14px 24px; border-radius: 16px; font-size: 40px; font-weight: 700; }
      .beeld .chips { position: absolute; right: 24px; top: 24px; display: flex; flex-direction: column; align-items: flex-end; gap: 12px; }
      .beeld .chip { background: rgba(25,25,30,0.9); padding: 10px 22px; border-radius: 14px; font-size: 36px; font-weight: 700; }
      .beeld .chip:first-child { background: var(--brand-accent); color: #19191e; font-size: 48px; font-weight: 800; }
      .beeld .line { opacity: 0; }
      .beeld .line::before { content: "✓ "; color: var(--brand-accent); }
      .beeld.big .value { font-size: 190px; text-align: center; }
      .beeld.big .label { text-align: center; }
    </style>''')
    html = html.replace('''if (b.type === "img") el.innerHTML = `<img src="${b.src}">`;''',
        '''if (b.type === "img") { el.classList.add("img"); el.innerHTML = `<img src="${b.src}">` + (b.tag ? `<div class="tag">${b.tag}</div>` : "") + (b.chips ? `<div class="chips">${b.chips.map((c) => `<div class="chip">${c}</div>`).join("")}</div>` : ""); }''')
    html = html.replace('''else if (b.type === "video") el.innerHTML = `<video src="${b.src}" muted playsinline></video>`;''',
        '''else if (b.type === "video") { el.classList.add("vid"); el.innerHTML = `<video id="vid${i}" src="${b.src}" muted playsinline data-start="${b.start}" data-duration="${(b.end - b.start).toFixed(2)}" data-track-index="${20 + i}"></video>`; }''')
    html = html.replace('''el.className = "beeld";''', '''el.className = "beeld" + (b.big ? " big" : "");''')
    html = html.replace('''(b.lines || []).map((l) => `<div class="line">${l}</div>`).join("");''',
        '''(b.lines || []).map((l) => `<div class="line">${Array.isArray(l) ? l[0] : l}</div>`).join("");''')
    html = html.replace('''        tl.to(el, { opacity: 0, duration: 0.15, ease: "power2.in" }, b.end - 0.15);''',
        '''        (b.lines || []).forEach((l, j) => { const ln = el.querySelectorAll(".line")[j]; const t = Array.isArray(l) ? l[1] : b.start;
          tl.fromTo(ln, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "expo.out" }, t); });
        tl.to(el, { opacity: 0, duration: 0.15, ease: "power2.in" }, b.end - 0.15);''')
    html = html.replace('''for (let i = 0; i < words.length; i += CONFIG.chunkSize) {
        const group = words.slice(i, i + CONFIG.chunkSize);''', '''const GW = CONFIG.words; for (let gi = 0; gi < CONFIG.groups.length; gi++) {
        const group = CONFIG.groups[gi].map((k) => GW[k]); if (group[0][1] < CONFIG.hook.end - 0.05) continue; const nextG = CONFIG.groups[gi + 1];''')
    html = html.replace('''const start = group[0][1], end = (words[i + CONFIG.chunkSize] || [null, group[group.length - 1][2]])[1];''',
        '''const start = group[0][1], end = nextG ? Math.min(GW[nextG[0]][1], group[group.length - 1][2] + 0.8) : group[group.length - 1][2] + 0.3;''')
    assert 'CONFIG.groups.length' in html and 'nextG ?' in html
    pops = ''.join(f'\n      <audio id="pop{i}" src="assets/pop.mp3" data-start="{b["start"]}" data-duration="0.7" data-track-index="{10+i}" data-volume="0.25"></audio>' for i, b in enumerate(beelden) if b['type'] != 'video')
    html = html.replace('data-track-index="9"></audio>', 'data-track-index="9"></audio>' + pops)
    open(os.path.join(d, 'index.html'), 'w').write(html)
    json.dump({'id': f'd07-{X}', 'name': f'2026-10-25-D07-funda-fixer-{X}'}, open(os.path.join(d, 'meta.json'), 'w'))
    print(X, 'total', total, 'hook', off, 'cta', cta_start, 'punch', len(cfg['punchIns']))
    print(' '.join(w[0] for w in cfg['words']))

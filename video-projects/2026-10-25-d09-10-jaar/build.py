import json, os, shutil, subprocess, re
ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, '../../templates/sardo-format')
SFX = os.path.join(ROOT, '../../assets/sfx/ui/pop.mp3')
M = os.path.join(ROOT, 'media')

def probe(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode().strip())

def words(name):
    d = json.load(open(os.path.join(M, f'tr-{name}/transcript.json')))
    return [[w['text'], w['start'], w['end']] for w in (d if isinstance(d, list) else d['words'])]

FIX = {'Vloei': 'Vloer', 'spouwing': 'spouw', 'isuleren.': 'isoleren.', 'binnenu': 'binnen', 'zonpanelen.': 'zonnepanelen.',
       'bewat': 'ná', 'al': 'all-', 'electric': 'electric', 'al-elektric': 'all-electric', 'stur': 'stuur', 'O': 'Of',
       'check': 'CHECK', 'vijf': '5', 'Nou,': 'Nou,'}

def clean(ws):
    out = []; i = 0
    while i < len(ws):
        t, s, e = ws[i]
        # "haar plus plus" -> HR++
        if t == 'haar' and i + 2 < len(ws) and ws[i+1][0] == 'plus' and ws[i+2][0].startswith('plus'):
            out.append(['HR++', round(s, 2), round(ws[i+2][2], 2)]); i += 3; continue
        if t == 'al' and i + 1 < len(ws) and ws[i+1][0] == 'electric':
            out.append(['all-electric', round(s, 2), round(ws[i+1][2], 2)]); i += 2; continue
        t = FIX.get(t, t)
        t = re.sub(r'[.,]+$', '', t) if not t.endswith('?') else t
        out.append([t, round(s, 2), round(e, 2)]); i += 1
    return out

HOOKS = {
    'B': {'text': 'In <span class="hl">5 jaar</span> van het gas af', 'end': 2.55},
    'C': {'text': 'Wat eerst? Wat over <span class="hl">5 jaar</span>?', 'end': 3.85},
    'D': {'text': 'Alles in één keer? Of in <span class="hl">5 jaar</span>', 'end': 4.0},
}

# Scenes in BODY-tijd (s). Zie EDL.md
SCENES = [
    {'type': 'intro', 'start': 0.0, 'end': 3.85, 'kop': 'Jouw huis in 5 jaar', 'pills': [0.96, 1.2, 1.44, 1.64, 1.84]},
    {'type': 'huis', 'start': 3.9, 'end': 12.82, 'niks': 6.08, 'labelF': 7.6, 'labelA': 12.16},
    {'type': 'jaar', 'start': 12.88, 'end': 18.18, 'n': 1, 'icon': 'iso', 'lines': [['Vloer isoleren', 14.8], ['Spouw isoleren', 15.9], ['Dit doe je eerst', 17.2]]},
    {'type': 'jaar', 'start': 18.24, 'end': 28.58, 'n': 2, 'icon': 'raam', 'lines': [['Beter glas: HR++', 21.68], ['Dak isoleren', 25.04]]},
    {'type': 'jaar', 'start': 28.64, 'end': 38.5, 'n': 3, 'icon': 'wp', 'lines': [['Hybride warmtepomp', 30.64], ['All-electric ready', 37.2]]},
    {'type': 'jaar', 'start': 38.56, 'end': 51.14, 'n': 4, 'icon': 'zon', 'lines': [['Zonnepanelen', 39.92], ['Pas ná de warmtepomp', 42.0], ['Eerst je verbruik zien', 45.84]]},
    {'type': 'jaar', 'start': 51.2, 'end': 67.45, 'n': 5, 'icon': 'gas', 'lines': [['Laadpaal?', 56.16], ['Van het gas af', 59.11], ['Ketel weg', 61.03], ['Klaar!', 66.63]]},
    {'type': 'ketting', 'start': 67.51, 'end': 74.1, 'steps': ['Isoleren', 'Glas + dak', 'Hybride', 'Panelen', 'Gas eraf'], 'stepT': 70.47, 'title': 71.43},
    {'type': 'eind', 'start': 74.15, 'end': 999, 'eigen': 74.25, 'calc': 78.79},
]

EXTRA_CSS = r'''
      #hook { font-size: 84px; text-wrap: balance; }
      .scene { position: absolute; left: 36px; top: 1225px; width: 846px; height: 560px; border-radius: 24px;
        background: var(--brand-surface); border: 2px solid var(--brand-border); opacity: 0; overflow: hidden; }
      .tl { position: absolute; left: 40px; right: 40px; top: 34px; height: 76px; }
      .tl .bar { position: absolute; left: 38px; right: 38px; top: 36px; height: 6px; border-radius: 3px; background: var(--brand-border); }
      .tl .fill { position: absolute; left: 38px; top: 36px; height: 6px; border-radius: 3px; background: var(--brand-accent); width: 0; }
      .pill { position: absolute; top: 0; width: 76px; height: 76px; margin-left: -38px; border-radius: 50%; background: var(--brand-surface-2);
        border: 4px solid var(--brand-border); color: var(--brand-text-dim); font-size: 38px; font-weight: 800;
        display: flex; align-items: center; justify-content: center; }
      .pill.done { border-color: var(--brand-accent); color: var(--brand-accent); }
      .pill.now { background: var(--brand-accent); border-color: var(--brand-accent); color: #19191e; }
      .jaar-big { position: absolute; left: 44px; top: 150px; font-size: 96px; font-weight: 800; color: var(--brand-accent); line-height: 1; }
      .icon { position: absolute; right: 36px; top: 140px; width: 200px; height: 200px; }
      .lines { position: absolute; left: 44px; top: 270px; right: 250px; display: flex; flex-direction: column; gap: 14px; }
      .ln { font-size: 44px; font-weight: 700; line-height: 1.1; opacity: 0; }
      .ln::before { content: "✓ "; color: var(--brand-accent); }
      .intro-title { position: absolute; left: 0; right: 0; top: 120px; text-align: center; font-size: 76px; font-weight: 800; line-height: 1.05; }
      .intro-title .hl { color: var(--brand-accent); }
      .intro .tl { top: 330px; }
      .intro .pill { width: 110px; height: 110px; margin-left: -55px; font-size: 52px; opacity: 0; }
      .intro .tl .bar { top: 52px; }
      .lbl { position: absolute; width: 140px; height: 140px; border-radius: 20px; color: #fff; font-size: 100px; font-weight: 800;
        display: flex; align-items: center; justify-content: center; line-height: 1; }
      .lbl small { position: absolute; top: -50px; left: 0; right: 0; text-align: center; font-size: 34px; font-weight: 700; color: var(--brand-text-dim); }
      .lbl.f { background: #e8452c; } .lbl.a { background: #23a447; }
      .huis-svg { position: absolute; left: 40px; top: 80px; width: 360px; height: 400px; }
      .niks { position: absolute; left: 40px; top: 470px; width: 360px; text-align: center; font-size: 40px; font-weight: 700; color: var(--brand-text-dim); opacity: 0; }
      .pijl { position: absolute; left: 572px; top: 222px; font-size: 72px; font-weight: 800; color: var(--brand-accent); opacity: 0; }
      .pijl small { display: block; font-size: 30px; text-align: center; margin-top: -14px; }
      .step { position: absolute; width: 150px; border-radius: 16px; background: var(--brand-surface-2); border: 3px solid var(--brand-accent);
        display: flex; align-items: flex-start; justify-content: center; padding-top: 12px; font-size: 30px; line-height: 1.05; font-weight: 700; text-align: center; opacity: 0; }
      .step b { position: absolute; bottom: 10px; left: 0; right: 0; font-size: 54px; color: var(--brand-accent); }
      .k-title { position: absolute; left: 40px; right: 40px; top: 34px; font-size: 52px; font-weight: 800; line-height: 1.1; opacity: 0; }
      .k-title .hl { color: var(--brand-accent); }
      .eind-a { position: absolute; left: 0; right: 0; top: 110px; text-align: center; font-size: 70px; font-weight: 800; line-height: 1.1; opacity: 0; }
      .eind-a .hl { color: var(--brand-accent); }
      .eind-b { position: absolute; left: 90px; right: 90px; top: 330px; height: 140px; border-radius: 20px; background: var(--brand-accent); color: #19191e;
        font-size: 52px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 20px; opacity: 0; }
'''

ICONS = {
 'iso': '''<svg viewBox="0 0 230 230"><path d="M25 110 L115 35 L205 110" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>
   <rect x="45" y="105" width="140" height="105" fill="none" stroke="#fff" stroke-width="10"/>
   <rect class="laag" x="55" y="115" width="18" height="85" fill="#ffa62b"/><rect class="laag" x="157" y="115" width="18" height="85" fill="#ffa62b"/>
   <rect class="laag" x="55" y="188" width="120" height="14" fill="#ffa62b"/></svg>''',
 'raam': '''<svg viewBox="0 0 230 230"><rect x="40" y="30" width="150" height="170" rx="8" fill="#82c0cc33" stroke="#fff" stroke-width="10"/>
   <line x1="115" y1="30" x2="115" y2="200" stroke="#fff" stroke-width="8"/><line x1="40" y1="115" x2="190" y2="115" stroke="#fff" stroke-width="8"/>
   <path class="glans" d="M58 95 L95 48" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".7"/>
   <text x="115" y="226" font-size="34" font-weight="800" fill="#ffa62b" text-anchor="middle" font-family="Poppins">HR++</text></svg>''',
 'wp': '''<svg viewBox="0 0 230 230"><rect x="20" y="45" width="190" height="140" rx="16" fill="#2e2e37" stroke="#fff" stroke-width="9"/>
   <circle cx="95" cy="115" r="50" fill="none" stroke="#fff" stroke-width="7"/>
   <g class="fan"><path d="M95 115 L95 72 Q120 85 95 115 M95 115 L132 137 Q108 152 95 115 M95 115 L58 137 Q60 108 95 115" fill="#ffa62b"/></g>
   <rect x="160" y="70" width="30" height="8" rx="4" fill="#82c0cc"/><rect x="160" y="90" width="30" height="8" rx="4" fill="#82c0cc"/></svg>''',
 'zon': '''<svg viewBox="0 0 230 230"><g class="zonnetje"><circle cx="175" cy="50" r="24" fill="#ffa62b"/>
   <g stroke="#ffa62b" stroke-width="7" stroke-linecap="round"><line x1="175" y1="8" x2="175" y2="16"/><line x1="217" y1="50" x2="209" y2="50"/><line x1="145" y1="20" x2="151" y2="26"/><line x1="205" y1="20" x2="199" y2="26"/><line x1="205" y1="80" x2="199" y2="74"/></g></g>
   <path d="M20 200 L70 100 L190 100 L140 200 Z" fill="#82c0cc33" stroke="#fff" stroke-width="8" stroke-linejoin="round"/>
   <path d="M45 150 L165 150 M103 100 L80 200 M147 100 L118 200" stroke="#fff" stroke-width="6"/></svg>''',
 'gas': '''<svg viewBox="0 0 230 230"><path class="vlam" d="M115 25 C150 75 175 105 175 145 C175 180 148 205 115 205 C82 205 55 180 55 145 C55 115 75 95 88 70 C95 95 105 105 115 110 C112 80 105 55 115 25 Z" fill="#82c0cc"/>
   <line class="kruis" x1="30" y1="30" x2="200" y2="200" stroke="#e8452c" stroke-width="18" stroke-linecap="round" stroke-dasharray="241" stroke-dashoffset="241"/></svg>''',
}

HUIS = '''<svg class="huis-svg" viewBox="0 0 360 400"><path d="M20 180 L180 40 L340 180" fill="none" stroke="#fff" stroke-width="14" stroke-linejoin="round"/>
  <rect x="55" y="170" width="250" height="210" fill="#2e2e37" stroke="#fff" stroke-width="14"/>
  <rect x="95" y="215" width="70" height="70" fill="#82c0cc55" stroke="#fff" stroke-width="8"/><rect x="200" y="215" width="70" height="70" fill="#82c0cc55" stroke="#fff" stroke-width="8"/>
  <rect x="150" y="300" width="60" height="80" fill="#ffa62b"/></svg>'''

SCENE_JS = r'''
      // ===== Sardo D09: scenes in de beeld-zone =====
      const layer = document.querySelector("#beeld-layer");
      const PILLX = (k, n) => (k / (n - 1)) * 100;
      function tlRow(n, cls) {
        let h = `<div class="tl ${cls||''}"><div class="bar"></div><div class="fill"></div>`;
        for (let k = 0; k < 5; k++) h += `<div class="pill" style="left:calc(38px + (100% - 76px) * ${k/4})">${k+1}</div>`;
        return h + `</div>`;
      }
      const pop = [];
      SCENES.forEach((s, i) => {
        const el = document.createElement("div");
        el.className = "scene " + s.type;
        let html = "";
        if (s.type === "intro") html = `<div class="intro-title">${s.kop.replace("5 jaar", '<span class="hl">5 jaar</span>')}</div>` + tlRow(5);
        if (s.type === "huis") html = HUIS + `<div class="niks">Nog niks gedaan</div>` +
            `<div class="lbl f" style="left:425px;top:210px;opacity:0"><small>Nu</small>F</div>` +
            `<div class="pijl">➜<small>5 jaar</small></div>` +
            `<div class="lbl a" style="left:660px;top:210px;opacity:0"><small>Straks</small>A</div>`;
        if (s.type === "jaar") html = tlRow(5) + `<div class="jaar-big">Jaar ${s.n}</div><div class="icon">${ICONS[s.icon]}</div>` +
            `<div class="lines">` + s.lines.map(l => `<div class="ln">${l[0]}</div>`).join("") + `</div>`;
        if (s.type === "ketting") {
          html = `<div class="k-title">Elke stap maakt de <span class="hl">volgende beter</span></div>`;
          s.steps.forEach((t, k) => { const hgt = 150 + k * 50; html += `<div class="step" style="left:${40 + k*156}px;top:${520 - hgt}px;height:${hgt}px">${t}<b>${k+1}</b></div>`; });
        }
        if (s.type === "eind") html = `<div class="eind-a">Jouw eigen<br><span class="hl">5-jaren-plan?</span></div><div class="eind-b">Ik stuur je de calculator</div>`;
        el.innerHTML = html;
        layer.appendChild(el);
        const end = Math.min(s.end, CONFIG.duration);
        tl.set("#beeld-bg", { opacity: 1 }, s.start);
        tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, s.start);
        if (s.end < CONFIG.duration) tl.to(el, { opacity: 0, duration: 0.12, ease: "power2.in" }, end - 0.12);
        pop.push(s.start);

        if (s.type === "intro") {
          el.querySelectorAll(".pill").forEach((p, k) => tl.fromTo(p, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, s.pills[k]));
          tl.fromTo(el.querySelector(".fill"), { width: 0 }, { width: "calc(100% - 76px)", duration: 1.0, ease: "power2.inOut" }, s.pills[0]);
        }
        if (s.type === "huis") {
          tl.to(el.querySelector(".niks"), { opacity: 1, duration: 0.25 }, s.niks);
          tl.fromTo(el.querySelector(".lbl.f"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, s.labelF);
          tl.fromTo(el.querySelector(".pijl"), { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }, s.labelA - 0.7);
          tl.fromTo(el.querySelector(".lbl.a"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, s.labelA);
          pop.push(s.labelF, s.labelA);
        }
        if (s.type === "jaar") {
          const pills = el.querySelectorAll(".pill");
          pills.forEach((p, k) => { if (k < s.n - 1) p.classList.add("done"); if (k === s.n - 1) p.classList.add("now"); });
          const from = Math.max(0, s.n - 2) / 4, to = (s.n - 1) / 4;
          tl.fromTo(el.querySelector(".fill"), { width: `calc((100% - 76px) * ${from})` }, { width: `calc((100% - 76px) * ${to})`, duration: 0.5, ease: "power2.inOut" }, s.start + 0.1);
          tl.fromTo(pills[s.n - 1], { scale: 0.6 }, { scale: 1.12, duration: 0.3, ease: "back.out(3)" }, s.start + 0.45);
          tl.fromTo(el.querySelector(".jaar-big"), { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }, s.start + 0.1);
          tl.fromTo(el.querySelector(".icon"), { opacity: 0, scale: 0.6, rotation: -8 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, s.start + 0.2);
          el.querySelectorAll(".ln").forEach((ln, k) => { tl.fromTo(ln, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "expo.out" }, s.lines[k][1]); });
          const ic = el.querySelector(".icon");
          if (s.icon === "iso") ic.querySelectorAll(".laag").forEach((l, k) => tl.fromTo(l, { opacity: 0 }, { opacity: 1, duration: 0.3 }, s.lines[Math.min(k,1)][1]));
          if (s.icon === "wp") tl.fromTo(ic.querySelector(".fan"), { rotation: 0, svgOrigin: "95 115" }, { rotation: 360 * 8, svgOrigin: "95 115", duration: end - s.start, ease: "none" }, s.start);
          if (s.icon === "zon") tl.fromTo(ic.querySelector(".zonnetje"), { scale: 0.85, svgOrigin: "175 50" }, { scale: 1.1, svgOrigin: "175 50", duration: 0.8, ease: "sine.inOut", repeat: Math.floor((end - s.start) / 0.8) - 1, yoyo: true }, s.start);
          if (s.icon === "raam") tl.fromTo(ic.querySelector(".glans"), { opacity: 0.2 }, { opacity: 0.9, duration: 0.6, yoyo: true, repeat: 5 }, s.start + 0.5);
          if (s.icon === "gas") {
            tl.fromTo(ic.querySelector(".vlam"), { scaleY: 0.9, svgOrigin: "115 205" }, { scaleY: 1.05, svgOrigin: "115 205", duration: 0.3, yoyo: true, repeat: Math.floor((s.lines[1][1] - s.start) / 0.3), ease: "sine.inOut" }, s.start);
            tl.to(ic.querySelector(".kruis"), { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, s.lines[1][1]);
            tl.to(ic.querySelector(".vlam"), { opacity: 0.35, duration: 0.3 }, s.lines[1][1] + 0.2);
            tl.fromTo(pills[4], { scale: 1.12 }, { scale: 1.3, duration: 0.25, yoyo: true, repeat: 1 }, s.lines[3][1]);
          }
          s.lines.forEach(l => pop.push(l[1]));
        }
        if (s.type === "ketting") {
          el.querySelectorAll(".step").forEach((st, k) => tl.fromTo(st, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, s.start + 0.2 + k * 0.45));
          tl.fromTo(el.querySelector(".k-title"), { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, s.title);
          pop.push(s.title);
        }
        if (s.type === "eind") {
          tl.fromTo(el.querySelector(".eind-a"), { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, s.eigen);
          tl.fromTo(el.querySelector(".eind-b"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, s.calc);
          pop.push(s.calc);
        }
      });
'''

def bodycuts():
    # duur per stuk uit de echte stuk-bestanden (concat-tijden)
    lst = open(os.path.join(M, 'pieces/body.mp4.txt')).read().split('\n')
    acc = 0; cuts = []
    for l in lst:
        if not l.strip(): continue
        cuts.append(round(acc, 2)); acc += probe(l.split("'")[1])
    return cuts

CUTS = bodycuts()
def punch(off, dur):
    pts = [[0, 1.0]]; last = 0; big = False
    for c in CUTS:
        t = round(off + c, 2)
        if t - last >= 3.0 and t < dur - 2.2:
            big = not big; pts.append([t, 1.12 if big else 1.0]); last = t
    pts.append([round(dur - 2.0, 2), 1.0])
    return pts

TEMPLATE = open(os.path.join(TPL, 'index.html')).read()
BODYW = clean(words('body'))
for X in 'BCD':
    d = os.path.join(ROOT, X)
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(TPL, d)
    os.remove(os.path.join(d, 'assets/source.mp4'))
    os.link(os.path.join(M, f'full-{X}.mp4'), os.path.join(d, 'assets/source.mp4'))
    shutil.copy(SFX, os.path.join(d, 'assets/pop.mp3'))
    dur = round(probe(os.path.join(d, 'assets/source.mp4')) - 0.04, 2)
    off = probe(os.path.join(M, f'hook-{X}.mp4'))
    hw = clean(words(f'hook-{X}'))
    bw = [[t, round(s + off, 2), round(e + off, 2)] for t, s, e in BODYW]
    scenes = []
    for s in SCENES:
        n = {}
        for k, v in s.items():
            if k in ('start', 'end', 'niks', 'labelF', 'labelA', 'stepT', 'title', 'eigen', 'calc'): n[k] = round(v + off, 2)
            elif k == 'pills': n[k] = [round(t + off, 2) for t in v]
            elif k == 'lines': n[k] = [[l, round(t + off, 2)] for l, t in v]
            else: n[k] = v
        scenes.append(n)
    cfg = {'duration': dur, 'faceOffsetY': -115, 'hook': HOOKS[X], 'cta': {'word': 'CHECK', 'start': round(dur - 2.0, 2)},
           'words': [w for w in hw + bw if w[1] < dur - 2.0], 'chunkSize': 3, 'beelden': [], 'punchIns': punch(off, dur)}
    html = TEMPLATE
    REPL = ('const CONFIG = ' + json.dumps(cfg, ensure_ascii=False) + ';\n      const SCENES = ' +
                  json.dumps(scenes, ensure_ascii=False) + ';\n      const ICONS = ' + json.dumps(ICONS) + ';\n      const HUIS = ' + json.dumps(HUIS) + ';')
    html = re.sub(r'const CONFIG = \{.*?\n      \};', lambda m: REPL, html, flags=re.S)
    html = html.replace('data-duration="6"', f'data-duration="{dur}"')
    html = html.replace('</style>', EXTRA_CSS + '    </style>')
    # vervang standaard beeld-builder door scenes
    a = html.index('      // Beeld-zone'); b = html.index('      // CTA')
    html = html[:a] + SCENE_JS + '\n' + html[b:]
    # pops: na de scene-JS zijn tijden bekend; schrijf ze statisch in HTML
    pops = sorted(set([s['start'] for s in scenes] + [l[1] for s in scenes for l in s.get('lines', [])] +
                      [s[k] for s in scenes for k in ('labelF', 'labelA', 'title', 'calc') if k in s]))
    pops = [p for p in pops if p < dur - 0.5]
    tags = ''.join(f'\n      <audio id="pop{i}" src="assets/pop.mp3" data-start="{p}" data-duration="0.6" data-track-index="{10+i}" data-volume="0.2"></audio>' for i, p in enumerate(pops))
    html = html.replace('data-track-index="9"></audio>', 'data-track-index="9"></audio>' + tags)
    open(os.path.join(d, 'index.html'), 'w').write(html)
    json.dump({'id': f'd09-{X}', 'name': f'2026-10-25-D09-5-jaar-{X}'}, open(os.path.join(d, 'meta.json'), 'w'))
    print(X, dur, 'hook', round(off, 2), 'punch', len(cfg['punchIns']), 'pops', len(pops))

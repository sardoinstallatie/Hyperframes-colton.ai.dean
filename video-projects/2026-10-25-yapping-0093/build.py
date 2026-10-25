import json, os, re, shutil, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, '../../templates/sardo-format')
SFX = os.path.join(ROOT, '../../assets/sfx/ui/pop.mp3')
FULL = os.path.join(ROOT, 'work/full.mp4')
OUTDIR = os.path.join(ROOT, 'A')

def probe(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())

# ---------- captions ----------
FIX = {'aanvoerttemperatuur': 'aanvoertemperatuur', 'thermostatum': 'thermostaat', 'temperaturen': 'temperatuur',
       'hitten': 'hitte', 'oké': 'oké,'}
def clean(ws):
    out = []
    for w in ws:
        t = w['text']; end = ''
        m = re.match(r'^(.*?)([.,!?]*)$', t); core, p = m.group(1), m.group(2)
        core = FIX.get(core, core)
        if core.endswith(','): core = core[:-1]; p = ',' + p
        if '?' in p or '!' in p: core += p.replace('.', '').replace(',', '')
        out.append([core, round(w['start'], 2), round(w['end'], 2), bool(p)])
    return out

def chunks(ws):
    groups = []; cur = []
    for w in ws:
        txt = ' '.join(x[0] for x in cur + [w])
        if cur and (len(cur) >= 3 or len(txt) > 19): groups.append(cur); cur = []
        cur.append(w)
        if w[3]: groups.append(cur); cur = []   # zin of komma = nieuwe chunk
    if cur: groups.append(cur)
    g2 = []
    for g in groups:
        if g2 and len(g2[-1]) == 1 and len(g2[-1][0][0]) <= 3 and not g2[-1][0][3]: g2[-1] = g2[-1] + g
        else: g2.append(g)
    groups = g2
    return [[[x[0], x[1], x[2]] for x in g] for g in groups]

# ---------- scenes (tijd in de geknipte video) ----------
SCENES = [
    {'type': 'icon', 'start': 0.30, 'end': 4.72, 'icon': 'huishalf', 'label': 'Jouw huis',
     'lines': [['Deels geïsoleerd', 1.0], ['Klaar voor een <b>warmtepomp</b>?', 2.9]]},
    {'type': 'icon', 'start': 4.78, 'end': 7.30, 'icon': 'sneeuw', 'label': 'Doe dit nu',
     'lines': [['Vóór de <b>kou</b> komt', 4.95]]},
    {'type': 'icon', 'start': 7.36, 'end': 13.48, 'icon': 'ketel', 'label': 'Op je ketel',
     'lines': [['Aanvoer-temperatuur', 8.8]], 'value': ['50-55°C', 11.36]},
    {'type': 'icon', 'start': 13.52, 'end': 19.98, 'icon': 'thermo', 'label': 'De test',
     'lines': [['Zet hem hoog', 16.9], ['Blijft het <b>warm</b>?', 14.6]], 'dial': 17.6},
    {'type': 'icon', 'start': 20.02, 'end': 22.52, 'icon': 'huiswarm', 'label': 'Blijft het warm?',
     'lines': [['Klaar voor een <b>warmtepomp</b>', 20.6]]},
    {'type': 'icon', 'start': 22.58, 'end': 26.62, 'icon': 'huiskoud', 'label': 'Wordt het koud?',
     'lines': [['Bij <b>50°C</b>', 25.5]]},
    {'type': 'twee', 'start': 26.68, 'end': 35.96, 'kop': 'Dan ligt het aan:', 'a': ['Je radiator', 'Niet goed genoeg', 28.16],
     'b': ['Je huis', 'Lekt warmte', 31.4], 'lek': 34.3},
    {'type': 'plan', 'start': 36.00, 'end': 45.56, 'steps': [['sneeuw', 'Winter', 'Test het', 36.0],
     ['bloem', 'Voorjaar', 'Samen kijken', 38.24], ['wp', 'Daarna', 'Warmtepomp erin', 43.9]]},
    {'type': 'icon', 'start': 45.62, 'end': 999, 'icon': 'duim', 'label': 'Of misschien…',
     'lines': [['Is er <b>niks</b> nodig', 46.3], ['Meteen aan de gang!', 47.4]]},
]

ICONS = {
 'huis': '''<path d="M30 140 L150 40 L270 140" fill="none" stroke="#fff" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/>
   <rect x="60" y="130" width="180" height="140" rx="6" fill="#2e2e37" stroke="#fff" stroke-width="14"/>
   <rect x="128" y="200" width="44" height="70" fill="#ffa62b"/>''',
}
SVG = {
 'huishalf': ICONS['huis'] + '''<rect class="iso" x="74" y="144" width="22" height="112" fill="#ffa62b"/>
   <rect class="iso" x="74" y="244" width="76" height="14" fill="#ffa62b"/>
   <path class="iso" d="M44 132 L150 46" stroke="#ffa62b" stroke-width="10" stroke-linecap="round"/>
   <g class="vraag"><circle cx="242" cy="62" r="44" fill="#ffa62b"/><text x="242" y="84" font-size="64" font-weight="800" fill="#19191e" text-anchor="middle" font-family="Poppins">?</text></g>''',
 'sneeuw': ''.join(f'<g class="flake" data-x="{x}"><text x="{x}" y="0" font-size="{s}" fill="#82c0cc" text-anchor="middle">❄</text></g>'
                   for x, s in [(50, 54), (120, 70), (200, 48), (260, 62), (90, 40), (170, 58), (235, 44)]),
 'ketel': '''<rect x="60" y="30" width="150" height="230" rx="18" fill="#2e2e37" stroke="#fff" stroke-width="12"/>
   <rect x="85" y="60" width="100" height="56" rx="8" fill="#19191e"/>
   <text class="kt" x="135" y="102" font-size="34" font-weight="800" fill="#ffa62b" text-anchor="middle" font-family="Poppins">°C</text>
   <path class="vlam" d="M135 150 C155 178 165 192 165 210 C165 228 151 240 135 240 C119 240 105 228 105 210 C105 196 114 186 121 174 C125 186 130 190 135 193 C133 178 130 166 135 150 Z" fill="#ffa62b"/>
   <rect x="232" y="40" width="30" height="200" rx="15" fill="#19191e" stroke="#fff" stroke-width="8"/>
   <rect class="kwik" x="240" y="60" width="14" height="172" rx="7" fill="#e8452c"/>
   <circle cx="247" cy="246" r="24" fill="#e8452c" stroke="#fff" stroke-width="8"/>''',
 'thermo': '''<circle cx="150" cy="150" r="118" fill="#2e2e37" stroke="#fff" stroke-width="12"/>
   <path d="M70 230 A112 112 0 1 1 230 230" fill="none" stroke="#3a3a45" stroke-width="18" stroke-linecap="round"/>
   <path class="boog" d="M70 230 A112 112 0 1 1 230 230" fill="none" stroke="#ffa62b" stroke-width="18" stroke-linecap="round" stroke-dasharray="530" stroke-dashoffset="440"/>
   <g class="naald"><line x1="150" y1="150" x2="150" y2="62" stroke="#fff" stroke-width="12" stroke-linecap="round"/></g>
   <circle cx="150" cy="150" r="18" fill="#ffa62b"/>
   <text x="150" y="215" font-size="38" font-weight="800" fill="#fff" text-anchor="middle" font-family="Poppins">+</text>''',
 'huiswarm': ICONS['huis'] + '''<g class="gloed">''' + ''.join(f'<path d="M{x} 118 q-12 -18 0 -36 q12 -18 0 -36" fill="none" stroke="#ffa62b" stroke-width="8" stroke-linecap="round"/>' for x in (110, 150, 190)) + '''</g>
   <g class="vink"><circle cx="232" cy="232" r="48" fill="#23a447" stroke="#19191e" stroke-width="6"/><path d="M210 232 L226 249 L256 216" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>''',
 'huiskoud': '''<path d="M30 140 L150 40 L270 140" fill="none" stroke="#82c0cc" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/>
   <rect x="60" y="130" width="180" height="140" rx="6" fill="#2e2e37" stroke="#82c0cc" stroke-width="14"/>
   <text class="fl2" x="150" y="230" font-size="80" fill="#82c0cc" text-anchor="middle">❄</text>
   <g class="kruis"><circle cx="232" cy="232" r="48" fill="#e8452c" stroke="#19191e" stroke-width="6"/><path d="M214 214 L250 250 M250 214 L214 250" stroke="#fff" stroke-width="12" stroke-linecap="round"/></g>''',
 'radiator': ''.join(f'<rect x="{40 + i*46}" y="70" width="34" height="170" rx="14" fill="#2e2e37" stroke="#fff" stroke-width="9"/>' for i in range(5)) +
   '<rect x="30" y="232" width="240" height="14" rx="7" fill="#fff"/>' +
   '<g class="golf">' + ''.join(f'<path d="M{x} 58 q-8 -12 0 -24 q8 -12 0 -24" fill="none" stroke="#ffa62b" stroke-width="6" stroke-linecap="round" opacity=".5"/>' for x in (90, 150, 210)) + '</g>',
 'lek': ICONS['huis'] + ''.join(f'<g class="pijl"><path d="{d}" fill="none" stroke="#ffa62b" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></g>' for d in (
   'M150 90 L150 20 M136 34 L150 20 L164 34', 'M90 200 L20 200 M34 186 L20 200 L34 214', 'M210 200 L280 200 M266 186 L280 200 L266 214')),
 'bloem': '''<line x1="150" y1="160" x2="150" y2="270" stroke="#23a447" stroke-width="12" stroke-linecap="round"/>
   <path d="M150 230 q-50 -10 -60 -50 q45 5 60 50" fill="#23a447"/>''' + ''.join(
   f'<circle cx="{150 + 46*c}" cy="{110 + 46*s}" r="34" fill="#ffa62b"/>' for c, s in [(1, 0), (0, 1), (-1, 0), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)]) +
   '<circle cx="150" cy="110" r="30" fill="#fff"/>',
 'wp': '''<rect x="20" y="60" width="260" height="190" rx="22" fill="#2e2e37" stroke="#fff" stroke-width="12"/>
   <circle cx="125" cy="155" r="68" fill="none" stroke="#fff" stroke-width="9"/>
   <g class="fan"><path d="M125 155 L125 98 Q160 115 125 155 M125 155 L174 184 Q142 204 125 155 M125 155 L76 184 Q78 145 125 155" fill="#ffa62b"/></g>
   <rect x="215" y="95" width="40" height="10" rx="5" fill="#82c0cc"/><rect x="215" y="120" width="40" height="10" rx="5" fill="#82c0cc"/><rect x="215" y="145" width="40" height="10" rx="5" fill="#82c0cc"/>''',
 'duim': '''<circle cx="150" cy="150" r="125" fill="#23a447"/>
   <path class="v" d="M88 152 L132 196 L214 108" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="230" stroke-dashoffset="230"/>''',
}
SVG['sneeuw2'] = SVG['sneeuw']

EXTRA_CSS = r'''
      #hook { font-size: 96px; text-wrap: balance; }
      .scene { position: absolute; left: 36px; top: 1225px; width: 846px; height: 560px; border-radius: 24px;
        background: var(--brand-surface); border: 2px solid var(--brand-border); opacity: 0; overflow: hidden; }
      .ic { overflow: hidden; position: absolute; left: 34px; top: 110px; width: 340px; height: 340px; }
      .ic svg { width: 100%; height: 100%; overflow: visible; }
      .txt { position: absolute; left: 400px; right: 34px; top: 0; bottom: 0; display: flex; flex-direction: column; justify-content: center; gap: 22px; }
      .lab { font-size: 32px; font-weight: 600; color: var(--brand-text-dim); text-transform: uppercase; letter-spacing: 0.06em; }
      .ln { font-size: 50px; font-weight: 800; line-height: 1.08; opacity: 0; }
      .ln b, .kop b { color: var(--brand-accent); font-weight: 800; }
      .val { white-space: nowrap; font-size: 82px; font-weight: 800; color: var(--brand-accent); line-height: 1; opacity: 0; letter-spacing: -0.02em; }
      .kop { position: absolute; left: 40px; right: 40px; top: 30px; font-size: 48px; font-weight: 800; opacity: 0; }
      .kaart { position: absolute; top: 112px; width: 368px; height: 412px; border-radius: 20px; background: var(--brand-surface-2);
        border: 3px solid var(--brand-border); opacity: 0; }
      .kaart .mini { position: absolute; left: 54px; top: 26px; width: 260px; height: 220px; }
      .kaart .mini svg { width: 100%; height: 100%; overflow: visible; }
      .kaart .k1 { position: absolute; left: 0; right: 0; top: 262px; text-align: center; font-size: 30px; font-weight: 600; color: var(--brand-text-dim); text-transform: uppercase; letter-spacing: .05em; }
      .kaart .k2 { position: absolute; left: 10px; right: 10px; top: 306px; text-align: center; font-size: 46px; font-weight: 800; line-height: 1.05; color: var(--brand-accent); }
      .of { position: absolute; left: 390px; width: 66px; top: 290px; text-align: center; font-size: 40px; font-weight: 800; color: var(--brand-text-dim); opacity: 0; }
      .stap { position: absolute; top: 50px; width: 264px; height: 460px; border-radius: 20px; background: var(--brand-surface-2);
        border: 3px solid var(--brand-border); opacity: 0; overflow: hidden; }
      .stap.on { border-color: var(--brand-accent); }
      .stap .mini { position: absolute; left: 42px; top: 34px; width: 180px; height: 180px; }
      .stap .mini svg { width: 100%; height: 100%; overflow: visible; }
      .stap .s1 { position: absolute; left: 0; right: 0; top: 250px; text-align: center; font-size: 30px; font-weight: 600; color: var(--brand-text-dim); text-transform: uppercase; letter-spacing: .05em; }
      .stap .s2 { position: absolute; left: 8px; right: 8px; top: 286px; text-align: center; font-size: 31px; font-weight: 800; line-height: 1.08; }
      .stap .nr { position: absolute; left: 0; right: 0; bottom: 12px; text-align: center; font-size: 44px; font-weight: 800; color: var(--brand-accent); }
'''

SCENE_JS = r'''
      // ===== scenes in de beeld-zone (icoontjes) =====
      const layer = document.querySelector("#beeld-layer");
      const svg = (k, vb) => `<svg viewBox="${vb || "0 0 300 300"}">${SVGS[k]}</svg>`;
      SCENES.forEach((s) => {
        const el = document.createElement("div");
        el.className = "scene " + s.type;
        const end = Math.min(s.end, CONFIG.duration);
        if (s.type === "icon") {
          el.innerHTML = `<div class="ic">${svg(s.icon)}</div><div class="txt"><div class="lab">${s.label}</div>` +
            s.lines.map((l) => `<div class="ln">${l[0]}</div>`).join("") + (s.value ? `<div class="val">${s.value[0]}</div>` : "") + `</div>`;
        }
        if (s.type === "twee") {
          el.innerHTML = `<div class="kop">${s.kop}</div>` +
            `<div class="kaart ka" style="left:20px"><div class="mini">${svg("radiator")}</div><div class="k1">${s.a[0]}</div><div class="k2">${s.a[1]}</div></div>` +
            `<div class="of">of</div>` +
            `<div class="kaart kb" style="left:456px"><div class="mini">${svg("lek")}</div><div class="k1">${s.b[0]}</div><div class="k2">${s.b[1]}</div></div>`;
        }
        if (s.type === "plan") {
          el.innerHTML = s.steps.map((st, k) => `<div class="stap" style="left:${16 + k*276}px"><div class="mini">${svg(st[0])}</div><div class="s1">${st[1]}</div><div class="s2">${st[2]}</div><div class="nr">${k+1}</div></div>`).join("");
        }
        layer.appendChild(el);
        tl.set("#beeld-bg", { opacity: 1 }, s.start);
        tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, s.start);
        if (s.end < CONFIG.duration) tl.to(el, { opacity: 0, duration: 0.12, ease: "power2.in" }, end - 0.12);

        if (s.type === "icon") {
          const ic = el.querySelector(".ic");
          tl.fromTo(ic, { scale: 0.6, rotation: -8, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, s.start + 0.05);
          el.querySelectorAll(".ln").forEach((ln, k) => tl.fromTo(ln, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "expo.out" }, s.lines[k][1]));
          if (s.value) tl.fromTo(el.querySelector(".val"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)", transformOrigin: "left center" }, s.value[1]);
          const q = (c) => ic.querySelectorAll(c);
          if (s.icon === "huishalf") {
            q(".iso").forEach((n, k) => tl.fromTo(n, { opacity: 0 }, { opacity: 1, duration: 0.25 }, s.lines[0][1] + k * 0.15));
            tl.fromTo(q(".vraag"), { scale: 0, svgOrigin: "242 62" }, { scale: 1, svgOrigin: "242 62", duration: 0.35, ease: "back.out(2.5)" }, s.lines[1][1]);
          }
          if (s.icon === "sneeuw") q(".flake").forEach((f, k) => tl.fromTo(f, { y: -60 - (k % 3) * 70 }, { y: 360, duration: 1.6 + (k % 3) * 0.3, ease: "none", repeat: 2 }, s.start + k * 0.12));
          if (s.icon === "ketel") {
            tl.fromTo(q(".vlam"), { scaleY: 0.85, svgOrigin: "135 240" }, { scaleY: 1.08, svgOrigin: "135 240", duration: 0.3, yoyo: true, repeat: 19, ease: "sine.inOut" }, s.start);
            tl.fromTo(q(".kwik"), { scaleY: 0.15, svgOrigin: "247 232" }, { scaleY: 0.72, svgOrigin: "247 232", duration: 0.8, ease: "power2.out" }, s.value[1] - 0.3);
          }
          if (s.icon === "thermo") {
            tl.fromTo(q(".naald"), { rotation: -120, svgOrigin: "150 150" }, { rotation: 100, svgOrigin: "150 150", duration: 0.9, ease: "power3.inOut" }, s.dial);
            tl.fromTo(q(".boog"), { strokeDashoffset: 440 }, { strokeDashoffset: 60, duration: 0.9, ease: "power3.inOut" }, s.dial);
          }
          if (s.icon === "huiswarm") {
            tl.fromTo(q(".gloed"), { y: 10, opacity: 0.3 }, { y: -8, opacity: 1, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, s.start);
            tl.fromTo(q(".vink"), { scale: 0, svgOrigin: "232 232" }, { scale: 1, svgOrigin: "232 232", duration: 0.35, ease: "back.out(2.5)" }, s.lines[0][1]);
          }
          if (s.icon === "huiskoud") {
            tl.fromTo(q(".fl2"), { rotation: 0, svgOrigin: "150 202" }, { rotation: 180, svgOrigin: "150 202", duration: 4, ease: "none" }, s.start);
            tl.fromTo(q(".kruis"), { scale: 0, svgOrigin: "232 232" }, { scale: 1, svgOrigin: "232 232", duration: 0.35, ease: "back.out(2.5)" }, s.lines[0][1]);
          }
          if (s.icon === "duim") tl.to(q(".v"), { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, s.start + 0.35);
        }
        if (s.type === "twee") {
          tl.fromTo(el.querySelector(".kop"), { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, s.start + 0.1);
          tl.fromTo(el.querySelector(".ka"), { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, s.a[2]);
          tl.fromTo(el.querySelector(".of"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, s.b[2] - 0.2);
          tl.fromTo(el.querySelector(".kb"), { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, s.b[2]);
          tl.fromTo(el.querySelectorAll(".ka .golf path"), { opacity: 0.6 }, { opacity: 0.1, duration: 0.5, yoyo: true, repeat: 7, stagger: 0.15 }, s.a[2] + 0.3);
          el.querySelectorAll(".kb .pijl").forEach((p, k) => {
            const dir = [[0, -14], [-14, 0], [14, 0]][k];
            tl.fromTo(p, { x: 0, y: 0, opacity: 0.4 }, { x: dir[0], y: dir[1], opacity: 1, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }, s.b[2] + 0.2);
          });
          tl.fromTo(el.querySelector(".kb"), { borderColor: "#3a3a45" }, { borderColor: "#ffa62b", duration: 0.2 }, s.lek);
        }
        if (s.type === "plan") {
          el.querySelectorAll(".stap").forEach((st, k) => {
            const t = s.steps[k][3];
            tl.fromTo(st, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }, t);
            tl.set(st, { className: "stap on" }, t);
            if (k < 2) tl.set(st, { className: "stap" }, s.steps[k + 1][3]);
            if (s.steps[k][0] === "wp") tl.fromTo(st.querySelector(".fan"), { rotation: 0, svgOrigin: "125 155" }, { rotation: 360 * 4, svgOrigin: "125 155", duration: end - t, ease: "none" }, t);
            if (s.steps[k][0] === "sneeuw") st.querySelectorAll(".flake").forEach((f, j) => tl.fromTo(f, { y: -60 - (j % 3) * 70 }, { y: 360, duration: 1.8 + (j % 3) * 0.3, ease: "none", repeat: 3 }, t + j * 0.12));
          });
        }
      });
'''

full = FULL
dur = round(probe(full) - 0.04, 2)
ws = clean(json.load(open(os.path.join(ROOT, 'work/transcript.json'))))
cta_start = round(dur - 2.0, 2)
hook_end = 2.0
cap = [w for w in ws if w[1] >= hook_end - 0.05 and w[1] < cta_start]
groups = chunks(cap)

# punch-ins op de cuts
pieces = [json.loads(json.dumps(p)) for p in json.load(open(os.path.join(ROOT, 'work/edl.json')))]
cuts = []; acc = 0
for a, b in pieces:
    cuts.append(round(acc, 2)); acc += round(round((b - a) * 25) / 25, 3)
BASE, BIG = 1.21, 1.33
pts = [[0, BASE]]; last = 0; big = False
for c in cuts[1:]:
    if c - last >= 3.0 and c < cta_start - 1.0:
        big = not big; pts.append([c, BIG if big else BASE]); last = c
pts.append([cta_start, BASE])

if os.path.exists(OUTDIR): shutil.rmtree(OUTDIR)
shutil.copytree(TPL, OUTDIR)
os.remove(os.path.join(OUTDIR, 'assets/source.mp4'))
shutil.copy(full, os.path.join(OUTDIR, 'assets/source.mp4'))
shutil.copy(SFX, os.path.join(OUTDIR, 'assets/pop.mp3'))

cfg = {'duration': dur, 'faceOffsetY': -234, 'hook': {'text': 'Klaar voor een <span class="hl">warmtepomp</span>?', 'end': hook_end},
       'cta': {'word': 'AANBOD', 'start': cta_start}, 'words': [], 'chunkSize': 3, 'beelden': [], 'punchIns': pts}
html = open(os.path.join(TPL, 'index.html')).read()
REPL = ('const CONFIG = ' + json.dumps(cfg, ensure_ascii=False) + ';\n      const GROUPS = ' + json.dumps(groups, ensure_ascii=False) +
        ';\n      const SCENES = ' + json.dumps(SCENES, ensure_ascii=False) + ';\n      const SVGS = ' + json.dumps(SVG, ensure_ascii=False) + ';')
html = re.sub(r'const CONFIG = \{.*?\n      \};', lambda m: REPL, html, flags=re.S)
html = html.replace('data-duration="6"', f'data-duration="{dur}"')
html = html.replace('transform-origin: 540px 534px;', 'transform-origin: 540px 768px;')
html = html.replace('</style>', EXTRA_CSS + '    </style>')
# captions: eigen chunks (op zinsdelen, lange woorden kleiner)
a = html.index('      // Captions'); b = html.index('      // Beeld-zone')
CAP_JS = r'''      // Captions (eigen indeling: max 3 woorden / 19 tekens, nieuwe chunk na leesteken)
      const cap = $("#captions");
      GROUPS.forEach((group, i) => {
        const el = document.createElement("div");
        el.className = "chunk";
        const n = group.map(([w]) => w).join(" ").length;
        if (n > 17) el.style.fontSize = Math.round(78 * 17 / n) + "px";
        el.innerHTML = group.map(([w]) => `<span class="w">${w}</span>`).join(" ");
        cap.appendChild(el);
        const start = group[0][1];
        const next = GROUPS[i + 1];
        const end = next ? next[0][1] : Math.min(group[group.length - 1][2] + 0.3, CONFIG.cta.start);
        tl.set(el, { opacity: 1 }, start);
        tl.set(el, { opacity: 0 }, Math.min(end, CONFIG.cta.start));
        group.forEach(([, s, e], j) => {
          const span = el.children[j];
          tl.set(span, { className: "w on" }, s);
          tl.set(span, { className: "w" }, (group[j + 1] ? group[j + 1][1] : e));
        });
      });

'''
html = html[:a] + CAP_JS + html[b:]
a = html.index('      // Beeld-zone'); b = html.index('      // CTA')
html = html[:a] + SCENE_JS + '\n' + html[b:]
pops = sorted(set([s['start'] for s in SCENES] + [s['a'][2] for s in SCENES if 'a' in s] + [s['b'][2] for s in SCENES if 'b' in s] +
                  [st[3] for s in SCENES for st in s.get('steps', [])]))
pops = [p for p in pops if p < dur - 0.5]
tags = ''.join(f'\n      <audio id="pop{i}" src="assets/pop.mp3" data-start="{p}" data-duration="0.6" data-track-index="{10+i}" data-volume="0.18"></audio>' for i, p in enumerate(pops))
html = html.replace('data-track-index="9"></audio>', 'data-track-index="9"></audio>' + tags)
open(os.path.join(OUTDIR, 'index.html'), 'w').write(html)
json.dump({'id': 'yap-0093-A', 'name': '2026-10-25-yapping-warmtepomp-test'}, open(os.path.join(OUTDIR, 'meta.json'), 'w'))
print('dur', dur, 'cta', cta_start, 'chunks', len(groups), 'punch', pts, 'pops', len(pops))
for g in groups: print(round(g[0][1], 2), ' '.join(x[0] for x in g))

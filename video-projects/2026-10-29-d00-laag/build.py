import json, os, shutil, subprocess, re
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ROOT, '../..')
OUT = os.path.join(ROOT, 'A')
SRC = os.path.join(ROOT, 'raw-media/body.mp4')
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',SRC]).decode())

FIX = {'allelekt': 'all-electric', 'spou': 'spouw', 'HR': 'HR++'}
raw = json.load(open(os.path.join(ROOT, 'raw-media/tw-body.json')))
ws = []
for x in raw:
    t = x['text']; m = re.match(r'^(.*?)([.,?!]*)$', t); core, p = m.group(1), m.group(2)
    core = FIX.get(core, core)
    ws.append([core + p, x['start'], x['end'], bool(p)])

HOOK_END = 2.30
CTA_START = round(dur - 2.0, 2)

# captions: max 3 woorden / 19 tekens, nieuwe chunk na leesteken
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
capws = [w for w in ws if w[1] >= HOOK_END - 0.05 and w[1] < CTA_START]
groups = chunks(capws)

# lagen: [label, tijd waarop "top X%" valt]
pct_times = {}
for w in ws:
    m = re.match(r'^(\d+)%', w[0])
    if m and m.group(1) not in pct_times: pct_times[m.group(1)] = w[1]
pct_times['10'] = [w[1] for w in ws if w[0].startswith('10%')][-1]  # tweede "top 10%" = de payoff
LAYERS = ['90','80','70','60','50','40','30','20','10']
COLORS = ['#e53935','#f4511e','#fb8c00','#ffb300','#fdd835','#c0ca33','#7cb342','#43a047','#00c853']
# zin-start per laag (om de laag alvast te laten oplichten als Peter erover begint)
heb = [w[1] for w in ws if w[0] in ('Heb', 'En')]

# piramide-geometrie
TOP_Y, BASE_Y, GAP = 210, 900, 10
BASE_W, TOP_W = 900, 150
n = len(LAYERS); bh = (BASE_Y - TOP_Y - GAP*(n-1)) / n
def width_at(y): return TOP_W + (BASE_W - TOP_W) * (y - TOP_Y) / (BASE_Y - TOP_Y)
bands = ''
for i, lab in enumerate(LAYERS):           # i=0 onderste
    y1 = BASE_Y - i*(bh+GAP); y0 = y1 - bh
    w0, w1 = width_at(y0), width_at(y1)
    inset = (w1 - w0) / 2 / w1 * 100
    fs = min(64, bh*0.78)
    bands += f'''
      <div class="band" id="b{lab}" style="left:{540-w1/2:.1f}px;top:{y0:.1f}px;width:{w1:.1f}px;height:{bh:.1f}px;--c:{COLORS[i]};clip-path:polygon({inset:.2f}% 0,{100-inset:.2f}% 0,100% 100%,0 100%)">
        <div class="fill"></div><div class="lab" style="font-size:{fs:.0f}px">±{lab}%</div>
      </div>'''

cuts = [0, 4.92, 7.92, 11.64, 16.42, 22.00, 26.60, 31.28, 37.56, 49.94]
punch = [[t, 1.0 if i % 2 == 0 else 1.12] for i, t in enumerate(cuts)]

dings = [round(pct_times[l], 2) for l in LAYERS]
sfx = ''.join(f'\n      <audio id="ding{i}" src="assets/pop.mp3" data-start="{t}" data-duration="0.6" data-track-index="{10+i}" data-volume="0.28"></audio>' for i, t in enumerate(dings[:-1]))
sfx += f'\n      <audio id="dingtop" src="assets/ding.mp3" data-start="{dings[-1]}" data-duration="1.5" data-track-index="30" data-volume="0.35"></audio>'

cfg = dict(duration=round(dur, 3), hookEnd=HOOK_END, ctaStart=CTA_START,
           groups=[[[w[0], w[1], w[2]] for w in g] for g in groups],
           layers=LAYERS, pct=pct_times, heb=heb, punch=punch)

D = round(dur, 3)
html = f'''<!doctype html>
<html lang="nl" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/brand-tokens.css" />
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--brand-bg); }}
      body {{ font-family:var(--font-display); color:#fff; }}
      #top {{ position:absolute; left:0; top:0; width:1080px; height:960px;
        background: radial-gradient(ellipse at 50% 60%, #26262e 0%, #19191e 70%); overflow:hidden; }}
      .band {{ position:absolute; transform-origin:50% 50%; }}
      .band .fill {{ position:absolute; inset:0; background:#e4e5ea; }}
      .band .lab {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
        font-weight:800; color:#fff; -webkit-text-stroke:4px #111; paint-order:stroke fill; opacity:0; letter-spacing:-0.01em; }}
      #glow {{ position:absolute; left:90px; top:200px; width:900px; height:720px; border-radius:50%;
        background: radial-gradient(ellipse, rgba(0,200,83,0.45) 0%, rgba(0,200,83,0) 65%); opacity:0; }}
      #trophy {{ position:absolute; left:440px; top:58px; width:200px; height:150px; opacity:0; transform-origin:50% 100%; }}
      #peter {{ position:absolute; left:0; top:960px; width:1080px; height:960px; overflow:hidden; background:#0d1a20; }}
      #face-wrapper {{ position:absolute; left:0; top:-100px; width:1080px; height:1120px; transform-origin:540px 470px; }}
      #face {{ width:1080px; height:1120px; object-fit:cover; display:block; }}
      #seam {{ position:absolute; left:0; top:958px; width:1080px; height:4px; background:#fff; opacity:.9; }}
      .anchor {{ position:absolute; left:40px; right:40px; top:960px; transform:translateY(-50%); text-align:center;
        font-weight:800; line-height:1.05; -webkit-text-stroke:4px rgba(0,0,0,.9); paint-order:stroke fill;
        text-shadow:0 6px 24px rgba(0,0,0,.6); opacity:0; }}
      #hook {{ font-size:96px; }}
      #hook .hl, #cta .big {{ color:var(--brand-accent); }}
      #cta {{ font-size:86px; white-space:nowrap; }}
      #cta .hl2 {{ color:var(--brand-accent); }}
      #captions {{ position:absolute; left:40px; right:40px; top:880px; height:160px; }}
      .chunk {{ position:absolute; left:0; right:0; top:50%; transform:translateY(-50%); text-align:center; font-size:80px; font-weight:800;
        line-height:1.05; -webkit-text-stroke:4px rgba(0,0,0,.9); paint-order:stroke fill; text-shadow:0 4px 18px rgba(0,0,0,.6); opacity:0; white-space:nowrap; }}
      .w {{ display:inline-block; margin:0 .1em; }}
      .w.on {{ color:var(--brand-accent); }}
      .w.pct {{ font-size:1.3em; color:var(--brand-accent); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="peter">
        <div id="face-wrapper">
          <video id="face" src="assets/source.mp4" muted playsinline data-start="0" data-duration="{D}" data-track-index="0"></video>
        </div>
      </div>
      <audio id="face-audio" src="assets/source.mp4" data-start="0" data-duration="{D}" data-track-index="9"></audio>{sfx}
      <div id="top" class="clip" data-start="0" data-duration="{D}" data-track-index="2">
        <div id="glow"></div>{bands}
        <svg id="trophy" viewBox="0 0 200 150">
          <path d="M60 10 H140 V55 C140 85 120 100 100 100 C80 100 60 85 60 55 Z" fill="#ffc83d" stroke="#111" stroke-width="6"/>
          <path d="M60 22 H32 C32 52 45 62 62 62 M140 22 H168 C168 52 155 62 138 62" fill="none" stroke="#ffc83d" stroke-width="10" stroke-linecap="round"/>
          <rect x="90" y="98" width="20" height="22" fill="#ffc83d" stroke="#111" stroke-width="5"/>
          <rect x="66" y="118" width="68" height="20" rx="4" fill="#ffc83d" stroke="#111" stroke-width="6"/>
        </svg>
      </div>
      <div id="seam" class="clip" data-start="0" data-duration="{D}" data-track-index="3"></div>
      <div id="captions" class="clip" data-start="0" data-duration="{D}" data-track-index="5"></div>
      <div id="hook" class="anchor clip" data-start="0" data-duration="{D}" data-track-index="6"></div>
      <div id="cta" class="anchor clip" data-start="0" data-duration="{D}" data-track-index="7"></div>
    </div>
    <script>
      const C = {json.dumps(cfg)};
      const tl = gsap.timeline({{ paused: true }});
      const $ = (s) => document.querySelector(s);

      // Peter: punch-ins op elke cut
      C.punch.forEach(([t, s]) => tl.set("#face-wrapper", {{ scale: s }}, t));

      // Hook (eerste ~2 s) op de naad
      $("#hook").innerHTML = 'Nieuwe <span class="hl">HR-ketel?</span>';
      tl.fromTo("#hook", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(1.6)" }}, 0.02);
      tl.to("#hook", {{ opacity: 0, duration: 0.1 }}, C.hookEnd - 0.12);

      // Captions
      const cap = $("#captions");
      C.groups.forEach((g, i) => {{
        const el = document.createElement("div"); el.className = "chunk";
        el.innerHTML = g.map(([w]) => `<span class="w${{/^\\d+%/.test(w) ? " pct" : ""}}">${{w}}</span>`).join(" ");
        cap.appendChild(el);
        const s = Math.max(g[0][1], C.hookEnd), nx = C.groups[i + 1];
        const e = Math.min(nx ? nx[0][1] : g[g.length - 1][2] + 0.3, C.ctaStart);
        tl.set(el, {{ opacity: 1 }}, s); tl.set(el, {{ opacity: 0 }}, e);
        g.forEach(([w, ws, we], j) => {{
          if (/^\\d+%/.test(w)) return;
          tl.set(el.children[j], {{ className: "w on" }}, ws);
          tl.set(el.children[j], {{ className: "w" }}, we);
        }});
      }});

      // Piramide: laag 90 knippert vanaf frame 1, elke laag kleurt op "top X%"
      tl.fromTo("#b90 .fill", {{ backgroundColor: "#e4e5ea" }}, {{ backgroundColor: "#e53935", duration: 0.2, repeat: 7, yoyo: true, ease: "none" }}, 0.05);
      C.layers.forEach((l, i) => {{
        const t = C.pct[l], sel = "#b" + l;
        const col = getComputedStyle(document.querySelector(sel)).getPropertyValue("--c").trim();
        tl.to(sel + " .fill", {{ backgroundColor: col, duration: 0.25, ease: "power2.out" }}, t);
        tl.fromTo(sel + " .lab", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, t);
        tl.fromTo(sel, {{ scale: 1 }}, {{ scale: 1.08, duration: 0.18, ease: "power2.out" }}, t);
        // vorige laag terug naar normaal
        if (i > 0) tl.to("#b" + C.layers[i - 1], {{ scale: 1, opacity: 0.8, duration: 0.25 }}, t);
      }});
      // "En de top 10%..." -> toplaag knippert alvast
      tl.fromTo("#b10 .fill", {{ backgroundColor: "#e4e5ea" }}, {{ backgroundColor: "#00c853", duration: 0.3, repeat: 13, yoyo: true, ease: "none" }}, 38.08);
      // Top 10% payoff: alles groen gloeien + beker
      const tTop = C.pct["10"];
      tl.to("#b10", {{ scale: 1, duration: 0.3 }}, tTop + 0.6);
      tl.to(C.layers.map((l) => "#b" + l), {{ opacity: 1, duration: 0.3 }}, tTop + 0.6);
      tl.fromTo("#glow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power2.out" }}, tTop);
      tl.to("#glow", {{ opacity: 0.55, duration: 0.6, repeat: 5, yoyo: true, ease: "sine.inOut" }}, tTop + 0.4);
      tl.fromTo("#trophy", {{ opacity: 0, scale: 0.3, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2.4)" }}, tTop);

      // CTA laatste 2 s
      $("#cta").innerHTML = 'Volg <span class="hl2">@sardobouw</span>';
      tl.fromTo("#cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.8)" }}, C.ctaStart);

      tl.set({{}}, {{}}, C.duration);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>'''

if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(os.path.join(REPO, 'templates/sardo-format'), OUT)
os.remove(os.path.join(OUT, 'index.html'))
shutil.copy(SRC, os.path.join(OUT, 'assets/source.mp4'))
shutil.copy(os.path.join(REPO, 'assets/sfx/ui/pop.mp3'), os.path.join(OUT, 'assets/pop.mp3'))
shutil.copy(os.path.join(REPO, 'assets/sfx/ui/notification.mp3'), os.path.join(OUT, 'assets/ding.mp3'))
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print('dur', D, 'cta', CTA_START, 'chunks', len(groups), 'pct', pct_times)

import os
LAYERS = ['90','80','70','60','50','40','30','20','10']
COLORS = ['#e53935','#f4511e','#fb8c00','#ffb300','#fdd835','#c0ca33','#7cb342','#43a047','#00c853']
TOP_Y, BASE_Y, GAP, BASE_W, TOP_W = 385, 842, 8, 820, 150
n = len(LAYERS); bh = (BASE_Y - TOP_Y - GAP*(n-1)) / n
wa = lambda y: TOP_W + (BASE_W - TOP_W) * (y - TOP_Y) / (BASE_Y - TOP_Y)
bands = ''
for i, lab in enumerate(LAYERS):
    y1 = BASE_Y - i*(bh+GAP); y0 = y1 - bh; w0, w1 = wa(y0), wa(y1); inset = (w1 - w0) / 2 / w1 * 100
    bands += (f'<div class="band" style="left:{540-w1/2:.1f}px;top:{y0:.1f}px;width:{w1:.1f}px;height:{bh:.1f}px;background:{COLORS[i]};'
              f'clip-path:polygon({inset:.2f}% 0,{100-inset:.2f}% 0,100% 100%,0 100%)"><div class="lab" style="font-size:{min(54,bh*0.78):.0f}px">±{lab}%</div></div>')
html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="brand-tokens.css"><style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1920px;overflow:hidden;background:#19191e;font-family:Poppins}}
#top{{position:absolute;left:0;top:0;width:1080px;height:960px;background:radial-gradient(ellipse at 50% 60%,#26262e 0%,#19191e 70%)}}
#glow{{position:absolute;left:90px;top:340px;width:900px;height:560px;border-radius:50%;background:radial-gradient(ellipse,rgba(0,200,83,.5) 0%,rgba(0,200,83,0) 65%)}}
.band{{position:absolute}} .lab{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;-webkit-text-stroke:4px #111;paint-order:stroke fill}}
#trophy{{position:absolute;left:470px;top:278px;width:140px;height:105px}}
#peter{{position:absolute;left:0;top:960px;width:1080px;height:960px;overflow:hidden}}
#peter img{{position:absolute;left:0;top:-110px;width:1080px;height:1120px;object-fit:cover}}
#seam{{position:absolute;left:0;top:958px;width:1080px;height:4px;background:#fff}}
#t{{position:absolute;left:30px;right:30px;top:960px;transform:translateY(-50%);text-align:center;font-weight:800;font-size:96px;line-height:1.02;color:#fff;
 -webkit-text-stroke:6px #000;paint-order:stroke fill;text-shadow:0 8px 28px rgba(0,0,0,.7)}}
#t .o{{color:#ffa62b}}
</style></head><body>
<div id="top"><div id="glow"></div>{bands}
<svg id="trophy" viewBox="0 0 200 150"><path d="M60 10 H140 V55 C140 85 120 100 100 100 C80 100 60 85 60 55 Z" fill="#ffc83d" stroke="#111" stroke-width="6"/><path d="M60 22 H32 C32 52 45 62 62 62 M140 22 H168 C168 52 155 62 138 62" fill="none" stroke="#ffc83d" stroke-width="10" stroke-linecap="round"/><rect x="90" y="98" width="20" height="22" fill="#ffc83d" stroke="#111" stroke-width="5"/><rect x="66" y="118" width="68" height="20" rx="4" fill="#ffc83d" stroke="#111" stroke-width="6"/></svg></div>
<div id="peter"><img src="peter.jpg"></div><div id="seam"></div>
<div id="t">In welke <span class="o">laag</span><br>zit jij?</div>
</body></html>'''
open(os.path.join(os.path.dirname(__file__), 'thumb.html'), 'w').write(html)

# Huis-SVG generator. mode: 'anim' (alles, beginstand voor animatie), 'red' (beginhuis), 'green' (eindhuis)
def arrow(x1, y1, x2, y2, w=12):
    import math
    a = math.atan2(y2 - y1, x2 - x1); h = 26
    p1 = (x2 - h*math.cos(a - 0.5), y2 - h*math.sin(a - 0.5)); p2 = (x2 - h*math.cos(a + 0.5), y2 - h*math.sin(a + 0.5))
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#ff5252" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="#ff5252" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

def wave(x, y):
    return f'<path d="M{x} {y} q12 -14 0 -28 q-12 -14 0 -28" fill="none" stroke="#ff5252" stroke-width="9" stroke-linecap="round"/>'

def star(x, y, r=26):
    return f'<path d="M{x} {y-r} L{x+r*0.25} {y-r*0.25} L{x+r} {y} L{x+r*0.25} {y+r*0.25} L{x} {y+r} L{x-r*0.25} {y+r*0.25} L{x-r} {y} L{x-r*0.25} {y-r*0.25} Z" fill="#fff"/>'

def window(p, wid, x, y, w=100, h=90, fill="#ff7043"):
    return (f'<g id="{p}{wid}"><rect class="glass" x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#fff" stroke-width="10"/>'
            f'<path d="M{x+w/2} {y} V{y+h} M{x} {y+h/2} H{x+w}" stroke="#fff" stroke-width="6"/></g>')

def house_svg(p='h-', mode='anim'):
    red, green = mode in ('anim', 'red'), mode == 'green'
    vis = lambda on: '' if on else ' opacity="0"'
    s = []
    s.append(f'<rect id="{p}night" x="0" y="0" width="1080" height="960" fill="#060a1f"{vis(False)}/>')
    s.append(f'<g id="{p}stars"{vis(False)}>' + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff"/>' for x, y in [(120,90),(260,160),(860,110),(960,230),(700,70),(420,60),(90,300),(980,380)]) + '</g>')
    s.append(f'<g id="{p}sunw"><circle id="{p}sun" cx="175" cy="215" r="62" fill="#ffc83d"{vis(green)}/></g>')
    s.append(f'<circle id="{p}glow" cx="540" cy="560" r="420" fill="url(#{p}gg)"{vis(green)}/>')
    s.append(f'<defs><radialGradient id="{p}gg"><stop offset="0" stop-color="#00c853" stop-opacity=".55"/><stop offset="1" stop-color="#00c853" stop-opacity="0"/></radialGradient></defs>')
    # schoorsteen + vlam + rook
    s.append(f'<rect x="652" y="300" width="50" height="110" fill="#2e2e37" stroke="#fff" stroke-width="10"/>')
    s.append(f'<g id="{p}smoke"{vis(red)}>' + ''.join(f'<circle class="puff" cx="677" cy="250" r="{r}" fill="#9a9aa6"/>' for r in (22, 26, 30)) + '</g>')
    s.append(f'<path id="{p}flame" d="M677 296 C650 270 664 246 677 226 C682 246 704 258 690 284 C686 292 682 296 677 296 Z" fill="#ff9800" stroke="#ffeb3b" stroke-width="5"{vis(red)}/>')
    # grote rode warmtewolk boven het dak
    s.append(f'<g id="{p}cloud"{vis(red)}><g class="cloudin">' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ff5252" opacity=".85"/>' for x, y, r in [(460,215,52),(520,190,62),(585,215,50),(430,250,36),(615,250,36)]) + '</g></g>')
    # dak
    s.append(f'<polygon points="262,482 540,282 818,482" fill="#2e2e37" stroke="#fff" stroke-width="14" stroke-linejoin="round"/>')
    s.append(f'<polygon id="{p}roofred" points="290,470 540,300 790,470" fill="#e53935"{vis(red)}/>')
    s.append(f'<polygon id="{p}roofgreen" points="290,470 540,300 790,470" fill="#00c853" opacity="{0.45 if green else 0}"/>')
    s.append(f'<polygon id="{p}blanket" points="292,468 540,300 788,468 752,468 540,330 328,468" fill="#fdd835" stroke="#c9a400" stroke-width="4"{vis(green)}/>')
    # zonnepanelen op linker dakvlak
    pan = ''.join(f'<rect x="{i*78}" y="-46" width="70" height="40" rx="4" fill="#1e3a8a" stroke="#82c0cc" stroke-width="5"/>' for i in range(3))
    s.append(f'<g transform="translate(305,452) rotate(-35.7)"><g id="{p}panels"{vis(green)}>{pan}</g></g>')
    # muren
    s.append(f'<rect x="300" y="472" width="480" height="348" fill="#2e2e37" stroke="#fff" stroke-width="14"/>')
    s.append(f'<rect id="{p}wallred" x="307" y="479" width="466" height="334" fill="#e53935"{vis(red)}/>')
    s.append(f'<rect id="{p}wallgreen" x="307" y="479" width="466" height="334" fill="#00c853" opacity="{0.4 if green else 0}"/>')
    s.append(f'<path d="M307 646 H773" stroke="#fff" stroke-width="8"/>')
    # isolatie
    s.append(f'<rect id="{p}insL" x="290" y="472" width="26" height="348" fill="#fdd835"{vis(green)}/>')
    s.append(f'<rect id="{p}insR" x="764" y="472" width="26" height="348" fill="#fdd835"{vis(green)}/>')
    s.append(f'<rect id="{p}insF" x="290" y="812" width="500" height="24" fill="#fdd835"{vis(green)}/>')
    # ramen + deur
    gf = '#82c0cc' if green else '#ff7043'
    s.append(window(p, 'gw1', 340, 690, fill=gf)); s.append(window(p, 'gw2', 640, 690, fill=gf))
    s.append(window(p, 'uw1', 340, 510, fill=gf)); s.append(window(p, 'uw2', 640, 510, fill=gf))
    s.append(f'<rect x="495" y="700" width="90" height="120" rx="6" fill="#19191e" stroke="#fff" stroke-width="10"/><circle cx="568" cy="765" r="6" fill="#fff"/>')
    s.append(f'<g id="{p}glint" opacity="0">{star(432,520)}{star(732,520)}{star(432,700)}{star(732,700)}</g>')
    # EMS-kastje
    s.append(f'<g id="{p}ems"{vis(green)}><rect x="502" y="526" width="76" height="76" rx="12" fill="#ffa62b" stroke="#fff" stroke-width="8"/><text x="540" y="574" text-anchor="middle" font-size="26" font-weight="800" fill="#19191e" font-family="Poppins">EMS</text></g>')
    # grond
    s.append(f'<rect x="40" y="836" width="1000" height="18" rx="9" fill="#3a3a45"/>')
    # stroomlijntjes
    s.append(f'<path id="{p}power" d="M470 352 L470 640" fill="none" stroke="#ffd600" stroke-width="9" stroke-dasharray="18 14" stroke-linecap="round"{vis(green)}/>')
    # buitenunit warmtepomp (links)
    fan = ''.join(f'<path d="M0 0 L{dx} {dy}" stroke="#fff" stroke-width="9" stroke-linecap="round"/>' for dx, dy in [(0,-30),(26,15),(-26,15)])
    s.append(f'<g id="{p}unit"{vis(green)}><rect x="128" y="722" width="132" height="112" rx="10" fill="#e4e5ea" stroke="#fff" stroke-width="6"/>'
             f'<circle cx="194" cy="778" r="40" fill="#3a3a45"/><g transform="translate(194,778)"><g id="{p}fan">{fan}</g></g></g>')
    # thuisbatterij (rechts)
    bars = ''.join(f'<rect class="bar" id="{p}bar{i}" x="838" y="{800-i*22}" width="44" height="16" rx="3" fill="#00c853"/>' for i in range(4))
    s.append(f'<g id="{p}batt"{vis(green)}><rect x="852" y="702" width="16" height="12" fill="#fff"/><rect x="828" y="712" width="64" height="120" rx="10" fill="#2e2e37" stroke="#fff" stroke-width="8"/>{bars}</g>')
    # EMS-lijnen
    s.append(f'<g id="{p}emslines"{vis(green)}>'
             f'<path class="eline" d="M455 372 L522 526" fill="none" stroke="#ffa62b" stroke-width="8" stroke-dasharray="10 22" stroke-linecap="round"/>'
             f'<path class="eline" d="M260 760 L300 760 L502 600" fill="none" stroke="#ffa62b" stroke-width="8" stroke-dasharray="10 22" stroke-linecap="round"/>'
             f'<path class="eline" d="M828 760 L790 760 L578 600" fill="none" stroke="#ffa62b" stroke-width="8" stroke-dasharray="10 22" stroke-linecap="round"/></g>')
    # warmtepijlen
    def grp(gid, inner): return f'<g id="{p}{gid}"{vis(red)}><g class="pul">{inner}</g></g>'
    s.append(grp('a-gwin', wave(370, 682) + wave(410, 682) + wave(670, 682) + wave(710, 682)))
    s.append(grp('a-uwin', wave(370, 502) + wave(410, 502) + wave(670, 502) + wave(710, 502)))
    s.append(grp('a-wallL', arrow(290, 560, 215, 560) + arrow(290, 740, 215, 740)))
    s.append(grp('a-wallR', arrow(790, 560, 865, 560) + arrow(790, 740, 865, 740)))
    s.append(grp('a-floor', arrow(420, 850, 420, 925) + arrow(660, 850, 660, 925)))
    return '<svg viewBox="0 0 1080 960" width="1080" height="960" xmlns="http://www.w3.org/2000/svg">' + ''.join(s) + '</svg>'

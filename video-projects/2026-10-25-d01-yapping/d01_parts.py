# D01-specifieke stukken die in de yapping-template (build_tpl.py) worden geplakt door make_build.py
FIX_CLEAN = r'''FIX = {'aangerichten': 'aangericht', 'drie-fases': 'drie-fase', 'u': 'we', 'volden': 'volt door',
       'Krijgen': 'Je krijgt', 'kosten': 'kostte', 'werkte': 'werkten', 'Blij': 'Blijf'}
def clean(ws):
    raw = [(w['text'], round(w['start'], 2), round(w['end'], 2)) for w in ws]
    out = []; i = 0
    while i < len(raw):
        t, s, e = raw[i]
        m = re.match(r'^(.*?)([.,!?]*)$', t); core, p = m.group(1), m.group(2)
        nxt = re.sub(r'[.,!?]+$', '', raw[i + 1][0]) if i + 1 < len(raw) else ''
        nxtp = re.match(r'^(.*?)([.,!?]*)$', raw[i + 1][0]).group(2) if i + 1 < len(raw) else ''
        # bedragen als cijfers met €
        if core in ('7000', '7') and nxt == 'euro':
            out.append(['€7.000', s, raw[i + 1][2], bool(nxtp)]); i += 2; continue
        if core == '400' and nxt == 'euro':
            out.append(['€400', s, raw[i + 1][2], bool(nxtp)]); i += 2; continue
        if core == '300': core = '€300'
        if core == 'de' and nxt == '400': core = 'er'
        if core == 'controleer' and nxt == 'is': core = 'controleren'
        if core == 'hebben' and out and out[-1][0] == 'ik': core = 'heb'
        core = FIX.get(core, core)
        if '?' in p or '!' in p: core += p.replace('.', '').replace(',', '')
        out.append([core, s, e, bool(p)]); i += 1
    return out
'''

SCENES_SVG = r"""SCENES = [
    {'type': 'icon', 'start': 2.10, 'end': 4.55, 'icon': 'geld', 'tag': '<b>€7.000</b><br>schade'},
    {'type': 'icon', 'start': 4.62, 'end': 6.40, 'icon': 'zon', 'tag': 'Bij een<br><b>klant</b>'},
    {'type': 'icon', 'start': 6.60, 'end': 10.30, 'icon': 'kast', 'tag': 'Groepenkast<br><b>3 fasen</b>', 'tagAt': 8.96},
    {'type': 'icon', 'start': 10.50, 'end': 13.40, 'icon': 'nul', 'tag': 'Nul zat <b>los</b>', 'tagAt': 12.08},
    {'type': 'icon', 'start': 13.60, 'end': 18.60, 'icon': 'klok', 'tag': 'Veel te<br><b>druk</b>'},
    {'type': 'icon', 'start': 18.80, 'end': 21.00, 'icon': 'meter', 'tag': '<b>Niet</b><br>gemeten', 'x': 20.40},
    {'type': 'icon', 'start': 21.10, 'end': 23.30, 'icon': 'kastaan', 'tag': 'Alles<br>meteen <b>aan</b>'},
    {'type': 'icon', 'start': 23.40, 'end': 28.60, 'icon': 'bliksem', 'tag': '<b class="big">400 volt</b>', 'tagAt': 26.08},
    {'type': 'row', 'start': 28.72, 'end': 37.30, 'items': [['wasmachine', 'Wasmachine', 31.36], ['droger', 'Droger', 32.16], ['tv', 'Tv', 33.44], ['keuken', 'Keuken', 34.56], ['ketel', 'Ketel', 36.56]]},
    {'type': 'icon', 'start': 37.40, 'end': 41.10, 'icon': 'schild', 'tag': 'Verzekering<br><b>betaalt?</b>'},
    {'type': 'icon', 'start': 41.20, 'end': 43.78, 'icon': 'schild', 'tag': 'Alleen de<br><b>dagprijs</b>'},
    {'type': 'icon', 'start': 43.90, 'end': 48.30, 'icon': 'munt', 'tag': '<b class="big">€300-400</b>', 'tagAt': 45.44},
    {'type': 'icon', 'start': 48.50, 'end': 52.30, 'icon': 'kar', 'tag': 'Alles<br><b>nieuw</b>', 'tagAt': 50.32},
    {'type': 'icon', 'start': 52.40, 'end': 56.40, 'icon': 'geld', 'tag': '<b class="big">€7.000</b>', 'tagAt': 53.60},
    {'type': 'icon', 'start': 56.50, 'end': 58.20, 'icon': 'lessen', 'tag': '<b>2</b> lessen'},
    {'type': 'icon', 'start': 58.30, 'end': 63.50, 'icon': 'check', 'tag': 'Les 1:<br><b>controleer</b>'},
    {'type': 'twee', 'start': 63.60, 'end': 68.40, 'of': 'en', 'a': ['ik', 'Jezelf', 63.69], 'b': ['team', 'Elkaar', 65.29]},
    {'type': 'icon', 'start': 68.50, 'end': 70.90, 'icon': 'loep', 'tag': 'Controleren<br>is <b>beter</b>', 'tagAt': 69.61},
    {'type': 'icon', 'start': 71.00, 'end': 75.10, 'icon': 'tools', 'tag': 'Les 2:<br><b>op te lossen</b>', 'tagAt': 72.33},
    {'type': 'icon', 'start': 75.20, 'end': 80.30, 'icon': 'hart', 'tag': 'Niemand<br><b>gewond</b>'},
]

# Icoontjes: eigen viewBox per icoon. Stijl: wit lijnwerk, oranje accent, #2e2e37 vulling.
VB = {}
SVG = {
 'geld': '''<g><rect x="30" y="140" width="150" height="70" rx="12" fill="#2e7d4f" stroke="#fff" stroke-width="8"/>
   <rect x="45" y="115" width="150" height="70" rx="12" fill="#2e7d4f" stroke="#fff" stroke-width="8"/>
   <rect x="60" y="90" width="150" height="70" rx="12" fill="#3a9a62" stroke="#fff" stroke-width="8"/>
   <circle cx="135" cy="125" r="20" fill="none" stroke="#fff" stroke-width="7"/></g>
   <g class="munt"><circle cx="190" cy="60" r="38" fill="#ffa62b" stroke="#fff" stroke-width="7"/>
   <text x="190" y="76" font-family="Poppins" font-weight="800" font-size="46" fill="#19191e" text-anchor="middle">€</text></g>''',
 'munt': '''<g class="munt"><circle cx="125" cy="125" r="100" fill="#ffa62b" stroke="#fff" stroke-width="10"/>
   <circle cx="125" cy="125" r="78" fill="none" stroke="#19191e" stroke-width="5" opacity=".35"/>
   <text x="125" y="160" font-family="Poppins" font-weight="800" font-size="110" fill="#19191e" text-anchor="middle">€</text></g>''',
 'zon': '''<g class="zonnetje"><circle cx="195" cy="55" r="30" fill="#ffa62b"/>
   <g stroke="#ffa62b" stroke-width="8" stroke-linecap="round"><line x1="195" y1="5" x2="195" y2="14"/><line x1="245" y1="55" x2="236" y2="55"/><line x1="160" y1="20" x2="166" y2="26"/><line x1="230" y1="20" x2="224" y2="26"/><line x1="230" y1="90" x2="224" y2="84"/></g></g>
   <path d="M15 225 L70 110 L210 110 L155 225 Z" fill="#82c0cc33" stroke="#fff" stroke-width="9" stroke-linejoin="round"/>
   <path d="M42 168 L182 168 M117 110 L90 225 M163 110 L130 225" stroke="#fff" stroke-width="7"/>''',
 'kast': '''<rect x="35" y="20" width="180" height="210" rx="14" fill="#2e2e37" stroke="#fff" stroke-width="10"/>
   <g class="schak"><rect x="60" y="55" width="30" height="60" rx="6" fill="#ffa62b"/><rect x="110" y="55" width="30" height="60" rx="6" fill="#ffa62b"/><rect x="160" y="55" width="30" height="60" rx="6" fill="#ffa62b"/></g>
   <g font-family="Poppins" font-weight="800" font-size="26" fill="#82c0cc" text-anchor="middle"><text x="75" y="150">L1</text><text x="125" y="150">L2</text><text x="175" y="150">L3</text></g>
   <rect x="60" y="170" width="130" height="34" rx="6" fill="#3a3a45"/>''',
 'kastaan': '''<rect x="35" y="20" width="180" height="210" rx="14" fill="#2e2e37" stroke="#fff" stroke-width="10"/>
   <g class="hendels">''' + ''.join(f'<g data-x="{x}"><rect x="{x-15}" y="60" width="30" height="110" rx="8" fill="#3a3a45"/><rect class="hd" x="{x-12}" y="120" width="24" height="45" rx="6" fill="#ffa62b"/></g>' for x in (75, 125, 175)) + '''</g>
   <text x="125" y="212" font-family="Poppins" font-weight="800" font-size="30" fill="#fff" text-anchor="middle">AAN</text>''',
 'nul': '''<rect x="20" y="95" width="120" height="60" rx="10" fill="#3a3a45" stroke="#fff" stroke-width="8"/>
   <g class="schroef"><circle cx="80" cy="125" r="20" fill="#b8bcc6"/><line x1="66" y1="125" x2="94" y2="125" stroke="#19191e" stroke-width="6"/></g>
   <path class="draad" d="M140 125 C175 125 180 85 230 70" stroke="#82c0cc" stroke-width="16" fill="none" stroke-linecap="round"/>
   <g class="vonk" fill="#ffa62b" opacity="0"><path d="M150 85 L165 55 L162 80 L182 75 L160 112 L164 90 Z"/></g>''',
 'klok': '''<circle cx="125" cy="135" r="95" fill="#2e2e37" stroke="#fff" stroke-width="10"/>
   <rect x="105" y="16" width="40" height="22" rx="6" fill="#fff"/>
   <line class="wijzer" x1="125" y1="135" x2="125" y2="70" stroke="#ffa62b" stroke-width="12" stroke-linecap="round"/>
   <circle cx="125" cy="135" r="12" fill="#ffa62b"/>''',
 'meter': '''<rect x="55" y="15" width="140" height="220" rx="22" fill="#ffa62b" stroke="#fff" stroke-width="8"/>
   <rect x="78" y="40" width="94" height="58" rx="8" fill="#19191e"/><text x="125" y="82" font-family="Poppins" font-weight="800" font-size="32" fill="#82c0cc" text-anchor="middle">230</text>
   <circle cx="125" cy="150" r="34" fill="#19191e"/><line x1="125" y1="150" x2="140" y2="125" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
   <circle cx="95" cy="210" r="9" fill="#19191e"/><circle cx="155" cy="210" r="9" fill="#e8452c"/>
   <g class="kruis" stroke="#e8452c" stroke-width="22" stroke-linecap="round"><line x1="20" y1="20" x2="230" y2="230" stroke-dasharray="297" stroke-dashoffset="297"/><line x1="230" y1="20" x2="20" y2="230" stroke-dasharray="297" stroke-dashoffset="297"/></g>''',
 'bliksem': '''<circle cx="125" cy="125" r="112" fill="#ffa62b33"/>
   <path class="flits" d="M145 15 L55 140 L118 140 L95 235 L195 100 L130 100 Z" fill="#ffa62b" stroke="#fff" stroke-width="8" stroke-linejoin="round"/>''',
 'schild': '''<path d="M125 18 L215 52 C215 140 180 200 125 232 C70 200 35 140 35 52 Z" fill="#2e2e37" stroke="#fff" stroke-width="11" stroke-linejoin="round"/>
   <text x="125" y="158" font-family="Poppins" font-weight="800" font-size="96" fill="#ffa62b" text-anchor="middle">€</text>''',
 'kar': '''<path d="M15 45 L50 45 L80 170 L205 170 L230 80 L62 80" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="#2e2e37"/>
   <circle cx="95" cy="205" r="18" fill="#fff"/><circle cx="190" cy="205" r="18" fill="#fff"/>
   <g class="doos"><rect x="95" y="40" width="50" height="50" rx="6" fill="#ffa62b"/><rect x="150" y="55" width="45" height="35" rx="6" fill="#82c0cc"/></g>''',
 'lessen': '''<g class="l1"><rect x="10" y="50" width="110" height="150" rx="18" fill="#2e2e37" stroke="#fff" stroke-width="9"/><text x="65" y="160" font-family="Poppins" font-weight="800" font-size="100" fill="#ffa62b" text-anchor="middle">1</text></g>
   <g class="l2"><rect x="130" y="50" width="110" height="150" rx="18" fill="#2e2e37" stroke="#fff" stroke-width="9"/><text x="185" y="160" font-family="Poppins" font-weight="800" font-size="100" fill="#ffa62b" text-anchor="middle">2</text></g>''',
 'check': '''<rect x="40" y="20" width="170" height="215" rx="16" fill="#2e2e37" stroke="#fff" stroke-width="10"/>
   <rect x="90" y="8" width="70" height="30" rx="8" fill="#fff"/>
   <g class="vinkjes" stroke="#ffa62b" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" fill="none">
   <path d="M70 85 L88 103 L118 70"/><path d="M70 140 L88 158 L118 125"/><path d="M70 195 L88 213 L118 180"/></g>
   <g fill="#b8bcc6"><rect x="135" y="80" width="55" height="12" rx="6"/><rect x="135" y="135" width="55" height="12" rx="6"/><rect x="135" y="190" width="55" height="12" rx="6"/></g>''',
 'ik': '''<circle cx="125" cy="80" r="48" fill="#2e2e37" stroke="#fff" stroke-width="10"/>
   <path d="M40 230 C40 165 80 140 125 140 C170 140 210 165 210 230 Z" fill="#2e2e37" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>
   <g class="vinkje"><circle cx="200" cy="60" r="34" fill="#ffa62b"/><path d="M184 60 L196 72 L218 48" stroke="#19191e" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>''',
 'team': '''<circle cx="80" cy="85" r="40" fill="#2e2e37" stroke="#fff" stroke-width="9"/><path d="M10 230 C10 170 40 145 80 145 C120 145 150 170 150 230 Z" fill="#2e2e37" stroke="#fff" stroke-width="9"/>
   <circle cx="175" cy="85" r="40" fill="#2e2e37" stroke="#ffa62b" stroke-width="9"/><path d="M105 230 C105 170 135 145 175 145 C215 145 245 170 245 230 Z" fill="#2e2e37" stroke="#ffa62b" stroke-width="9"/>''',
 'loep': '''<circle cx="105" cy="105" r="75" fill="#82c0cc33" stroke="#fff" stroke-width="14"/>
   <line x1="160" y1="160" x2="228" y2="228" stroke="#fff" stroke-width="22" stroke-linecap="round"/>
   <path class="v" d="M70 108 L96 134 L142 82" fill="none" stroke="#ffa62b" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="120" stroke-dashoffset="120"/>''',
 'tools': '''<g class="sleutel"><path d="M70 40 C45 50 40 85 60 102 L35 200 C32 215 50 225 60 212 L120 130 C145 140 175 120 175 92 L150 110 L128 100 L125 76 L150 60 C125 30 95 30 70 40 Z" fill="#b8bcc6" stroke="#fff" stroke-width="7" stroke-linejoin="round"/></g>
   <rect x="150" y="120" width="40" height="110" rx="10" fill="#ffa62b" stroke="#fff" stroke-width="7"/><rect x="130" y="95" width="80" height="35" rx="8" fill="#82c0cc" stroke="#fff" stroke-width="7"/>''',
 'hart': '''<path class="hartje" d="M125 220 C40 160 15 115 15 80 C15 45 42 22 72 22 C98 22 115 38 125 58 C135 38 152 22 178 22 C208 22 235 45 235 80 C235 115 210 160 125 220 Z" fill="#e8452c" stroke="#fff" stroke-width="9" stroke-linejoin="round"/>
   <path d="M60 110 L95 110 L110 80 L130 140 L145 110 L190 110" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
 # kleine tegels (viewBox 120)
 'wasmachine': '''<rect x="12" y="6" width="96" height="108" rx="12" fill="#2e2e37" stroke="#fff" stroke-width="6"/><line x1="12" y1="30" x2="108" y2="30" stroke="#fff" stroke-width="5"/>
   <circle cx="60" cy="72" r="28" fill="#82c0cc55" stroke="#fff" stroke-width="6"/><circle cx="30" cy="18" r="5" fill="#ffa62b"/>''',
 'droger': '''<rect x="12" y="6" width="96" height="108" rx="12" fill="#2e2e37" stroke="#fff" stroke-width="6"/><line x1="12" y1="30" x2="108" y2="30" stroke="#fff" stroke-width="5"/>
   <circle cx="60" cy="72" r="28" fill="none" stroke="#fff" stroke-width="6"/><path d="M45 72 Q52 60 60 72 Q68 84 75 72" stroke="#ffa62b" stroke-width="5" fill="none"/>''',
 'tv': '''<rect x="6" y="18" width="108" height="72" rx="8" fill="#2e2e37" stroke="#fff" stroke-width="6"/><line x1="40" y1="108" x2="80" y2="108" stroke="#fff" stroke-width="6" stroke-linecap="round"/><line x1="60" y1="90" x2="60" y2="108" stroke="#fff" stroke-width="6"/>''',
 'keuken': '''<path d="M20 50 L100 50 L92 100 C90 108 84 112 76 112 L44 112 C36 112 30 108 28 100 Z" fill="#2e2e37" stroke="#fff" stroke-width="6" stroke-linejoin="round"/>
   <line x1="100" y1="58" x2="116" y2="50" stroke="#fff" stroke-width="6" stroke-linecap="round"/><path d="M45 38 Q40 26 48 16 M62 38 Q57 26 65 16 M79 38 Q74 26 82 16" stroke="#ffa62b" stroke-width="5" fill="none" stroke-linecap="round"/>''',
 'ketel': '''<rect x="22" y="6" width="76" height="96" rx="10" fill="#2e2e37" stroke="#fff" stroke-width="6"/><circle cx="60" cy="40" r="14" fill="#ffa62b"/>
   <line x1="40" y1="102" x2="40" y2="116" stroke="#fff" stroke-width="6"/><line x1="60" y1="102" x2="60" y2="116" stroke="#fff" stroke-width="6"/><line x1="80" y1="102" x2="80" y2="116" stroke="#fff" stroke-width="6"/>
   <rect x="40" y="68" width="40" height="10" rx="5" fill="#b8bcc6"/>''',
}
for k in SVG: VB[k] = '0 0 250 250'
for k in ('wasmachine', 'droger', 'tv', 'keuken', 'ketel'): VB[k] = '0 0 120 120'
XSVG = '<g class="x" stroke="#e8452c" stroke-width="14" stroke-linecap="round"><line x1="8" y1="8" x2="112" y2="112"/><line x1="112" y1="8" x2="8" y2="112"/></g>'
"""

EXTRA_CSS_ADD = r'''
      .row { gap: 6px; }
      .row .item .mini { width: 150px; height: 150px; }
      .row .tg { font-size: 28px; }
      .ic { overflow: visible; }
      .item .mini { overflow: visible; }
'''

SCENE_JS = r'''
      // ===== D01: icoontjes los over het beeld (yapping) =====
      const layer = document.querySelector("#beeld-layer");
      const svg = (k, extra) => `<svg viewBox="${VB[k]}">${SVGS[k]}${extra || ""}</svg>`;
      SCENES.forEach((s) => {
        const el = document.createElement("div");
        el.className = "scene " + s.type;
        const end = Math.min(s.end, CONFIG.duration);
        if (s.type === "icon") el.innerHTML = `<div class="ic">${svg(s.icon)}</div><div class="tag"><div>${s.tag}</div></div>`;
        if (s.type === "twee") el.innerHTML =
          `<div class="item ia" style="width:300px"><div class="mini" style="width:210px;height:210px">${svg(s.a[0])}</div><div class="tg">${s.a[1]}</div></div>` +
          `<div class="of">${s.of || "of"}</div>` +
          `<div class="item ib" style="width:300px"><div class="mini" style="width:210px;height:210px">${svg(s.b[0])}</div><div class="tg">${s.b[1]}</div></div>`;
        if (s.type === "row") el.innerHTML = s.items.map((it) =>
          `<div class="item st" style="width:196px"><div class="mini">${svg(it[0], XSVG)}</div><div class="tg">${it[1]}</div></div>`).join("");
        layer.appendChild(el);
        tl.set(el, { opacity: 1 }, s.start);
        tl.to(el, { opacity: 0, duration: 0.15, ease: "power2.in" }, end - 0.15);

        if (s.type === "icon") {
          const ic = el.querySelector(".ic");
          const life = end - s.start;
          tl.fromTo(ic, { scale: 0.4, rotation: -10, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(2)" }, s.start);
          tl.fromTo(el.querySelector(".tag"), { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }, s.tagAt || s.start + 0.15);
          const q = (c) => ic.querySelectorAll(c);
          const reps = (p) => Math.max(1, Math.floor(life / p) - 2);
          if (s.icon === "geld") { tl.fromTo(q(".munt"), { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "bounce.out" }, s.start + 0.25);
                                   tl.fromTo(q(".munt"), { rotation: -12, svgOrigin: "190 60" }, { rotation: 12, svgOrigin: "190 60", duration: 0.5, yoyo: true, repeat: reps(0.5), ease: "sine.inOut" }, s.start + 0.8); }
          if (s.icon === "munt") tl.fromTo(q(".munt"), { scaleX: 1, svgOrigin: "125 125" }, { scaleX: -1, svgOrigin: "125 125", duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }, s.start + 0.3);
          if (s.icon === "zon") tl.fromTo(q(".zonnetje"), { rotation: 0, svgOrigin: "195 55" }, { rotation: 90, svgOrigin: "195 55", duration: life, ease: "none" }, s.start);
          if (s.icon === "kast") q(".schak rect").forEach((r, k) => tl.fromTo(r, { scaleY: 0.3, svgOrigin: `${75 + k*50} 115` }, { scaleY: 1, svgOrigin: `${75 + k*50} 115`, duration: 0.25, ease: "back.out(2)" }, s.tagAt + k * 0.15));
          if (s.icon === "kastaan") q(".hd").forEach((h, k) => tl.fromTo(h, { y: 0 }, { y: -55, duration: 0.2, ease: "back.out(2)" }, s.start + 0.4 + k * 0.25));
          if (s.icon === "nul") { tl.fromTo(q(".schroef"), { rotation: -25, svgOrigin: "80 125" }, { rotation: 25, svgOrigin: "80 125", duration: 0.18, yoyo: true, repeat: reps(0.18), ease: "sine.inOut" }, s.start);
                                  tl.fromTo(q(".draad"), { rotation: 0, svgOrigin: "140 125" }, { rotation: -8, svgOrigin: "140 125", duration: 0.3, yoyo: true, repeat: reps(0.3), ease: "sine.inOut" }, s.start);
                                  tl.fromTo(q(".vonk"), { opacity: 0 }, { opacity: 1, duration: 0.08, yoyo: true, repeat: 9 }, s.tagAt); }
          if (s.icon === "klok") tl.fromTo(q(".wijzer"), { rotation: 0, svgOrigin: "125 135" }, { rotation: 360 * 4, svgOrigin: "125 135", duration: life, ease: "none" }, s.start);
          if (s.icon === "meter") q(".kruis line").forEach((l, k) => tl.to(l, { strokeDashoffset: 0, duration: 0.22, ease: "power2.out" }, s.x + k * 0.18));
          if (s.icon === "bliksem") { tl.fromTo(q(".flits"), { scale: 0.85, svgOrigin: "125 125" }, { scale: 1.1, svgOrigin: "125 125", duration: 0.12, yoyo: true, repeat: 7 }, s.tagAt);
                                      tl.fromTo(ic, { x: -7 }, { x: 7, duration: 0.05, yoyo: true, repeat: 15, ease: "none" }, s.tagAt); tl.set(ic, { x: 0 }, s.tagAt + 0.85); }
          if (s.icon === "kar") tl.fromTo(q(".doos"), { y: -80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "bounce.out" }, s.tagAt);
          if (s.icon === "lessen") { tl.fromTo(q(".l1"), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)" }, s.start + 0.2);
                                     tl.fromTo(q(".l2"), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)" }, s.start + 0.5); }
          if (s.icon === "check") q(".vinkjes path").forEach((p, k) => tl.fromTo(p, { opacity: 0, scale: 0.4, svgOrigin: "94 " + (90 + k*55) }, { opacity: 1, scale: 1, svgOrigin: "94 " + (90 + k*55), duration: 0.3, ease: "back.out(3)" }, s.start + 0.4 + k * 0.35));
          if (s.icon === "loep") tl.to(q(".v"), { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, s.tagAt);
          if (s.icon === "tools") tl.fromTo(q(".sleutel"), { rotation: -20, svgOrigin: "60 205" }, { rotation: 10, svgOrigin: "60 205", duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut" }, s.start + 0.3);
          if (s.icon === "hart") tl.fromTo(q(".hartje"), { scale: 0.92, svgOrigin: "125 120" }, { scale: 1.06, svgOrigin: "125 120", duration: 0.4, yoyo: true, repeat: reps(0.4), ease: "sine.inOut" }, s.start + 0.4);
        }
        if (s.type === "twee") {
          tl.fromTo(el.querySelector(".ia"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, s.a[2]);
          tl.fromTo(el.querySelector(".of"), { opacity: 0 }, { opacity: 1, duration: 0.2 }, s.b[2] - 0.25);
          tl.fromTo(el.querySelector(".ib"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, s.b[2]);
          tl.fromTo(el.querySelector(".ia .vinkje"), { scale: 0, svgOrigin: "200 60" }, { scale: 1, svgOrigin: "200 60", duration: 0.3, ease: "back.out(3)" }, s.a[2] + 0.4);
        }
        if (s.type === "row") {
          el.querySelectorAll(".st").forEach((st, k) => {
            const t = s.items[k][2];
            tl.fromTo(st, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t);
            tl.fromTo(st.querySelector(".x"), { opacity: 0, scale: 1.8, svgOrigin: "60 60" }, { opacity: 1, scale: 1, svgOrigin: "60 60", duration: 0.2, ease: "power3.in" }, t + 0.35);
            tl.to(st, { x: 5, duration: 0.04, yoyo: true, repeat: 5 }, t + 0.55);
          });
        }
      });
'''

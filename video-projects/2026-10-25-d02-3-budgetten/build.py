import json, os, shutil, subprocess, re
ROOT=os.path.dirname(os.path.abspath(__file__))
TPL=os.path.join(ROOT,'../../templates/sardo-format')
EDL=json.load(open(os.path.join(ROOT,'work/edl.json')))
FUNDA='/mnt/user-data/attachments/0b8dc3a3-a9b2-5032-97ac-c5ee48a76297/aa303be8-image.png'
SFX=os.path.join(ROOT,'../../assets/sfx/ui/pop.mp3')

def words(name):
    d=json.load(open(os.path.join(ROOT,f'media/tr-{name}/transcript.json')))
    return [[w['text'],w['start'],w['end']] for w in (d if isinstance(d,list) else d['words'])]

FIX={'Funna':'Funda','gijze.':'geiser.','spou,':'spouw,','stur':'stuur','Hetzelfde':'Zelfde','check':'CHECK','reageer':'Reageer','haar':'HR++','Zou':'zou','is':'is'}
def clean(ws):
    out=[]
    i=0
    while i<len(ws):
        t,s,e=ws[i]
        t=FIX.get(t,t)
        m=re.match(r'^(\d{1,2}\.?\d{3}|\d{4})([.,]?)$',t)
        if m:
            n=int(m.group(1).replace('.',''))
            if n not in (1932,1995):
                t='€'+f'{n:,}'.replace(',','.')+m.group(2)
                if i+1<len(ws) and ws[i+1][0].lower().startswith('euro'):
                    p=ws[i+1][0][4:]; e=ws[i+1][2]; t=t.rstrip('.,')+p; i+=1
        t=re.sub(r'[.,]+$','',t) if not t.endswith('?') else t; out.append([t,round(s,2),round(e,2)]); i+=1
    return out

HOOKS={
 'A':{'text':'Je hebt <span class="hl">€5.000</span> voor dit huis','end':3.4},
 'B':{'text':'<span class="hl">€5k, €20k</span> of <span class="hl">€40k</span>?','end':3.7},
 'C':{'text':'Zelfde huis. <span class="hl">3 budgetten.</span>','end':4.0},
}
# body-relative beeld timing (seconds in body.mp4)
BEELD=[
 {'start':0.15,'end':6.7,'type':'img','src':'assets/huis.png','tag':'Hoekhuis · 1932 · Arnhem','badge':'Label F'},
 {'start':6.8,'end':21.4,'type':'kaart','label':'Budget 1','value':'€5.000','lines':[['Spouwmuur isoleren',13.2],['Vloer isoleren',14.9],['+ subsidie',17.0]]},
 {'start':21.55,'end':35.0,'type':'kaart','label':'Budget 2','value':'€20.000','lines':[['Vloer, spouw en dak',27.0],['HR++ glas',31.7]]},
 {'start':35.1,'end':47.6,'type':'kaart','label':'Budget 3','value':'€40.000','lines':[['Alles van €20.000',38.0],['All-electric warmtepomp',43.2],['Vloerverwarming',45.3]]},
 {'start':47.75,'end':56.95,'type':'kaart','label':'Nu in dit huis','value':'1995','lines':[['Oude cv-ketel',52.6],['Oude geiser',55.4]]},
]
# body cut points -> punch-ins
cuts=[];acc=0
for s,e in EDL['body']:
    cuts.append(round(acc,2)); acc+=e-s
def punch(off,dur):
    pts=[[0,1.09]]
    last=0;big=False
    for c in cuts:
        t=round(off+c,2)
        if t-last>=3.0 and t<dur-2.2:
            big=not big; pts.append([t,1.17 if big else 1.09]); last=t
    pts.append([round(dur-2.0,2),1.09])
    return pts

TEMPLATE=open(os.path.join(TPL,'index.html')).read()
for X in 'ABC':
    d=os.path.join(ROOT,X)
    if os.path.exists(d): shutil.rmtree(d)
    shutil.copytree(TPL,d)
    os.remove(os.path.join(d,'assets/source.mp4'))
    os.link(os.path.join(ROOT,f'media/full-{X}.mp4'),os.path.join(d,'assets/source.mp4'))
    shutil.copy(FUNDA,os.path.join(d,'assets/huis.png'))
    shutil.copy(SFX,os.path.join(d,'assets/pop.mp3'))
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',os.path.join(d,'assets/source.mp4')]).decode().strip())
    dur=round(dur-0.04,2)
    hw=clean(words(f'hook-{X}'))
    off=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',os.path.join(ROOT,f'media/hook-{X}.mp4')]).decode().strip())
    bw=[[t,round(s+off,2),round(e+off,2)] for t,s,e in clean(words('body'))]
    beelden=[]
    for b in BEELD:
        nb=dict(b); nb['start']=round(b['start']+off,2); nb['end']=round(b['end']+off,2)
        if 'lines' in b: nb['lines']=[[l,round(t+off,2)] for l,t in b['lines']]
        beelden.append(nb)
    cfg={'duration':dur,'faceOffsetY':-111,'hook':HOOKS[X],'cta':{'word':'CHECK','start':round(dur-2.0,2)},
         'words':[w for w in hw+bw if w[1] < dur-2.0],'chunkSize':3,'beelden':beelden,'punchIns':punch(off,dur)}
    html=TEMPLATE
    html=re.sub(r'const CONFIG = \{.*?\n      \};', 'const CONFIG = '+json.dumps(cfg,ensure_ascii=False)+';', html, flags=re.S)
    html=html.replace('data-duration="6"',f'data-duration="{dur}"')
    # extra CSS
    html=html.replace('</style>','''
      .beeld.img { padding: 0; border: 0; }
      .beeld .tag { position: absolute; left: 24px; bottom: 24px; background: rgba(25,25,30,0.88); padding: 14px 24px; border-radius: 16px; font-size: 40px; font-weight: 700; }
      .beeld .badge { position: absolute; right: 24px; top: 24px; background: var(--brand-accent); color: #19191e; padding: 12px 26px; border-radius: 16px; font-size: 48px; font-weight: 800; }
      .beeld .line { opacity: 0; }
      .beeld .line::before { content: "✓ "; color: var(--brand-accent); }
    </style>''')
    # beeld builder: img tag/badge + timed lines + pop sfx
    html=html.replace('''if (b.type === "img") el.innerHTML = `<img src="${b.src}">`;''',
      '''if (b.type === "img") { el.classList.add("img"); el.innerHTML = `<img src="${b.src}">` + (b.tag ? `<div class="tag">${b.tag}</div>` : "") + (b.badge ? `<div class="badge">${b.badge}</div>` : ""); }''')
    html=html.replace('''(b.lines || []).map((l) => `<div class="line">${l}</div>`).join("");''',
      '''(b.lines || []).map((l) => `<div class="line">${Array.isArray(l) ? l[0] : l}</div>`).join("");''')
    html=html.replace('''        tl.to(el, { opacity: 0, duration: 0.15, ease: "power2.in" }, b.end - 0.15);''',
      '''        (b.lines || []).forEach((l, j) => { const ln = el.querySelectorAll(".line")[j]; const t = Array.isArray(l) ? l[1] : b.start;
          tl.fromTo(ln, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "expo.out" }, t); });
        tl.to(el, { opacity: 0, duration: 0.15, ease: "power2.in" }, b.end - 0.15);''')
    pops=''.join(f'\n      <audio id="pop{i}" src="assets/pop.mp3" data-start="{b["start"]}" data-duration="0.7" data-track-index="{10+i}" data-volume="0.25"></audio>' for i,b in enumerate(beelden))
    html=html.replace('data-track-index="9"></audio>','data-track-index="9"></audio>'+pops)
    open(os.path.join(d,'index.html'),'w').write(html)
    json.dump({'id':f'd02-{X}','name':f'2026-10-25-D02-3-budgetten-{X}'},open(os.path.join(d,'meta.json'),'w'))
    print(X,dur,'hook',off,'punch',len(cfg['punchIns']))

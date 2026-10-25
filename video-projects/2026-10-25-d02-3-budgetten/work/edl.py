import json
d=json.load(open('transcript.json'));W=d if isinstance(d,list) else d['words']
FILL={'um,','um','and','uh','eh'}
def sub(a,b,skip=()):
    ws=[w for w in W if w['start']>=a-0.01 and w['end']<=b+0.01 and w['text'].lower() not in FILL and w['start'] not in skip]
    rs=[]
    for w in ws:
        s,e=w['start'],w['end']
        if rs and s-rs[-1][1]<=0.25: rs[-1][1]=e
        else: rs.append([s,e])
    return [[round(max(0,s-0.06),2),round(e+0.08,2)] for s,e in rs]
hooks={'A':[[7.52,8.24],[8.24,12.72]],'B':[[18.10,24.95]],'C':[[37.90,41.92]]}
# hook A: keep the (untranscribed) amount between hebt and euro -> one continuous range
hooks['A']=[[7.52,12.72]]
body=[]
body+=sub(65.9,72.5)            # huis 1932 Arnhem label F
body+=sub(89.55,94.5)           # 5000: zo snel mogelijk isoleren
body+=sub(101.7,106.4)          # spouw + vloer
body+=sub(109.1,114.1)          # subsidie past in 5000
body+=sub(119.3,122.45)         # als je 20.000 budget hebt voor dit huis,
body+=sub(123.8,130.7)          # pak het isoleren compleet aan ... dak van binnen uit
body+=sub(132.4,135.6)          # HR++ glas
body+=sub(158.5,165.2)          # 40.000 hetzelfde als 20.000
body+=sub(168.3,174.4)          # all-electric + vloerverwarming
body+=sub(182.3,191.5)          # Funda ketel 1995 + geiser
body+=sub(292.5,300.7)          # CTA
json.dump({'hooks':hooks,'body':body},open('edl.json','w'),indent=1)
tot=sum(e-s for s,e in body); print(len(body),'body ranges, body',round(tot,2),'s')
for k,v in hooks.items(): print(k, round(sum(e-s for s,e in v),2))

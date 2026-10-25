import json
W=json.load(open('main-transcript.json'));W=W if isinstance(W,list) else W['words']
FILL={'um','um,','uh','eh','eh,'}
def sub(a,b):
    ws=[w for w in W if w['start']>=a-0.01 and w['start']<=b and w['text'].lower() not in FILL]
    rs=[]
    for w in ws:
        s,e=w['start'],min(w['end'],w['start']+0.9)  # Parakeet rekt laatste woord soms op
        if rs and s-rs[-1][1]<=0.30: rs[-1][1]=e
        else: rs.append([s,e])
    return [[round(max(0,s-0.06),2),round(e+0.10,2)] for s,e in rs]
hooks={'A':sub(0.96,4.2),'B':sub(9.84,12.9)}
body=[]
body+=sub(46.32,49.1)    # Dit is een hoekwoning uit 1930 in Arnhem
body+=sub(510.20,511.3)  # We hebben de calculator ingevuld
body+=sub(514.76,519.2)  # beginnen met isoleren. spouw, vloer, dak isoleren
body+=sub(540.45,542.8)  # ... glas vervangen naar HR++ glas
body+=sub(589.92,592.5)  # vloerverwarming aanleggen, beneden en boven
body+=sub(596.00,598.2)  # vervolgens naar een all-electric warmtepomp gaan
body+=sub(602.40,605.2)  # die ketel kan er dan uit, en die oude geiser kan eruit
body+=sub(622.00,624.4)  # en dan zou ik gaan kijken naar zonnepanelen ... voorkant van de woning
body+=sub(650.99,654.2)  # en dan in combinatie met een thuisbatterij van tussen de 10 en de 20 kWh
body+=sub(670.99,675.7)  # al die dingen bij elkaar opgeteld ga je van label F naar label A
body+=sub(695.79,699.0)  # dan zou dat neerkomen op inclusief de btw 52.000 euro
body+=sub(750.38,754.4)  # dan zou je daar tussen de 5 en 7000 euro subsidie voor krijgen
body+=sub(755.66,757.4)
body+=sub(761.42,763.6)  # met de calculator ... 450 euro per maand
body+=sub(769.35,772.4)  # dan zou het nieuwe maandbedrag ongeveer 125 euro worden
body+=sub(772.80,779.3)  # dus betekent dat je daar een winst hebt van 325 euro per maand
json.dump({'hooks':hooks,'body':body},open('edl.json','w'),indent=1)
tot=sum(e-s for s,e in body); print(len(body),'body ranges',round(tot,2),'s')
for k,v in hooks.items(): print(k,v,round(sum(e-s for s,e in v),2))

# -*- coding: utf-8 -*-
"""Build the standalone effects review from the inventory; never touches game data.

    python werkzeuge/eden_rise/effekt_auswahl.py

IlluGen input images are explicitly thumbnail previews, not production exports.
The gallery combines them with isolated Canvas animation prototypes. No server,
model, save, API key, or running Eden application is needed.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'docs' / 'effekt-auswahl'
INVENTORY = ROOT / 'docs' / 'docs/archiv/EDEN_KAMPF_EFFEKTE_INVENTUR.md'

# Effect -> visual family / palette / optional on-screen wording.
# These recipes only describe visuals. They do not implement or change game rules.
RECIPES = {
 'A1':('slash','pearl',''), 'A2':('impact','gold',''), 'A3':('stab','pearl',''),
 'A4':('thrust','pearl',''), 'A5':('shot','gold',''), 'A6':('critical','gold','Kritisch!'),
 'A7':('counter','gold','Konter'), 'A8':('tint','rose',''),
 'B1':('windup','gold',''), 'B2':('parry','gold','Perfekt!'),
 'B3':('parrySoft','sage','Pariert'), 'B4':('dodge','blue','Ausgewichen'),
 'B5':('damage','rose','Getroffen'), 'B6':('shield','gold',''),
 'C1':('fire','fire',''), 'C2':('water','water',''), 'C3':('quake','earth',''),
 'C4':('electric','pearl',''), 'C5':('bleed','rose',''),
 'C6':('exhausted','blue',''), 'C7':('weakened','gray',''),
 'C8':('blind','pearl',''), 'C9':('vulnerable','rose',''), 'C10':('stun','gold',''),
 'D1':('shortCircuit','water','Kurzschluss'), 'D2':('mud','earth',''),
 'D3':('firestorm','fire',''), 'D4':('steam','pearl',''), 'D5':('flare','fire',''),
 'E1':('mistral','earth','Mistral'), 'E2':('wave','water','Ressac'),
 'E3':('wind','pearl','Libeccio'), 'E4':('tidal','water','Lame de Fond'),
 'E5':('doubleSlash','pearl','Doppio Gioco'), 'E6':('blur','gray','Sotto Voce'),
 'E7':('vendetta','rose','Vendetta'), 'E8':('blackSlash','pearl','Omertà'),
 'E9':('reticle','blue','Point de Mire'), 'E10':('calm','water','Bonaccia'),
 'E11':('beam','gold','Phare'), 'E12':('rain','pearl',"Pluie d’Étoiles"),
 'F1':('buff','sage',''), 'F2':('heavyWindup','gold','Vorsicht'),
 'F3':('dodgeOnly','dodge','Nur ausweichen'), 'F4':('element','fire',''),
 'G1':('heal','sage','+12 LP'), 'G2':('victory','gold','Sieg'),
 'G3':('wake','pearl','An Bord'), 'G4':('level','gold','Level aufgestiegen'),
 'G5':('day','gold','Ein neuer Tag'),
 'H1':('cast','pearl',''), 'H2':('bite','gold','Biss!'),
 'H3':('catch','water','Gefangen'), 'H4':('rareCatch','gold','Seltener Fang'),
 'H5':('escape','water','Entwischt'),
 'I1':('find','lavender',''), 'I2':('pickup','gold','Aufgenommen'),
 'I3':('full','rose','Tasche voll'), 'I4':('rareFind','gold','Seltener Fund'),
 'I5':('elite','rose','Elite voraus'), 'I6':('return','pearl','Zurück an Bord'),
 'I7':('wake','pearl','Wieder an Bord'),
 'J1':('sizzle','pearl',''), 'J2':('cooking','gold','Meisterhaft'),
 'J3':('favorite','rose','Lieblingsgericht'), 'J4':('slime','earth',''),
 'J5':('upgrade','gold','Verbessert'), 'J6':('trade','gold','Gekauft'),
 'K1':('trust','gold','Vertrauen steigt'), 'K2':('desire','rose','Begehren steigt'),
 'K3':('cool','blue','Wert sinkt'), 'K4':('gift','rose','Geschenk'),
 'K5':('milestone','gold','Herzensmoment'), 'K6':('romance','rose',''),
 'K7':('blush','rose',''),
 'L1':('day','gold','Ein neuer Tag'), 'L2':('event','gold','Ereignis'),
 'L3':('level','gold','Skillpunkt'), 'L4':('warning','rose','Batterie kritisch'),
 'L5':('reputation','gold','Ruf steigt'), 'L6':('weather','pearl',''),
}

ASSETS = {
 'slash':['sword_slash_3D','swipe_dissolve'],
 'impact':['painted_style_golden_shockwave'], 'stab':['lense_flare'],
 'shot':['lense_flare','painted_style_golden_shockwave'],
 'fire':['stylized_flame_flipbook'], 'water':['waterfall_3D_2'],
 'electric':['electric_arc_4','lightning_sheet','erosion_based_lightning'],
 'smoke':['stylized_smoke_trail'], 'shield':['shield_gradient'],
 'wind':['swipe_dissolve','tornado_3D'],
}

def source_names(kind):
    if kind in ('slash','doubleSlash','counter','vendetta','blackSlash'): return ASSETS['slash']
    if kind == 'critical': return ASSETS['impact'] + ASSETS['slash']
    if kind in ('impact','quake'): return ASSETS['impact']
    if kind == 'mistral': return ASSETS['impact'] + ASSETS['wind'][:1]
    if kind == 'firestorm': return ASSETS['fire'] + ASSETS['electric'] + ASSETS['wind'][:1]
    if kind == 'element': return ASSETS['fire'] + ASSETS['water'] + ASSETS['impact'] + ASSETS['electric']
    if kind in ('fire','flare'): return ASSETS['fire']
    if kind == 'rareCatch': return ASSETS['water'] + ASSETS['shield']
    if kind in ('water','wave','tidal','mud','slime','catch','escape'): return ASSETS['water']
    if kind in ('electric','shortCircuit'): return ASSETS['electric']
    if kind in ('steam','sizzle','weakened','exhausted'): return ASSETS['smoke']
    if kind in ('wind','weather','dodge','thrust'): return ASSETS['wind'][:1]
    if kind == 'cooking': return ASSETS['shield'] + ASSETS['smoke']
    if kind in ('shield','buff','heal','trust','milestone','rareFind','find','favorite','desire','gift','level','romance','victory'): return ASSETS['shield']
    if kind in ('stab','shot'): return ASSETS[kind]
    return []

def build():
    text=INVENTORY.read_text(encoding='utf-8-sig')
    section=None
    categories=[]
    effects=[]
    for line in text.splitlines():
        m=re.match(r'^## ([A-L]) · (.+)',line)
        if m:
            section=m.group(1)
            categories.append({'id':section,'name':m.group(2).split(' (')[0]})
        if not re.match(r'^\| [A-L]\d+ \|',line):continue
        cells=[x.strip() for x in line.strip('|').split('|')]
        eid,name=cells[:2]
        if eid not in RECIPES: raise ValueError('Missing visual recipe: '+eid)
        kind,color,title=RECIPES[eid]
        sources=source_names(kind)
        is_loop=section=='C' or kind in ('wind','weather','sizzle')
        durations=[760,1020,1420] if not is_loop else [1000,1200,1480]
        variants=[]
        for i,label in enumerate(('Dezent','Dynamisch','Filmisch')):
            variants.append({'id':f'{eid}-{i+1}','index':i,'label':label,
              'kind':kind,'palette':color,'duration_ms':durations[i],
              'hit_ms':round(durations[i]*(.32 if i<2 else .4)),
              'target':'gegner' if section in 'ABCDEF' else 'kontext',
              'position':[.5,.58], 'size':[.70,.86,1.0][i],
              'loop':is_loop,'layer':'vor_und_hinter','blend':'source-over / lighter',
              'sound':None,'sound_status':'Nicht Teil dieser visuellen Auswahl',
              'sources':sources,
              'production_export':False,
              'origin':'IlluGen-Vorlagenvorschau + Canvas-Komposition' if sources else 'Engine-Animationsentwurf',
              'description':[
                'Ein klarer Akzent, kompakt und kurz. Die Figur bleibt im Vordergrund.',
                'Mehr Richtung und Nachlauf; mehrere abgestimmte Ebenen.',
                'Breitere Inszenierung mit gestaffeltem Aufbau und längerem Ausklang.'
              ][i]})
        effects.append({'id':eid,'category':section,'name':name,'description':' · '.join(cells[2:-2]),
                        'priority':cells[-1],'planned_tool':cells[-2],
                        'kind':kind,'palette':color,'title':title,'loop':is_loop,'variants':variants})
    if len(effects)!=81 or len(set(e['id'] for e in effects))!=81:raise ValueError('Inventory changed; review required')
    if set(RECIPES)!={e['id'] for e in effects}:raise ValueError('Recipe/inventory mismatch')
    sources=json.loads((DEST/'quellen/illugen-vorschauen.json').read_text(encoding='utf-8'))
    baked_path=DEST/'quellen/vorschau-exporte.json'
    baked=json.loads(baked_path.read_text(encoding='utf-8')).get('variants',{}) if baked_path.exists() else {}
    for e in effects:
        for v in e['variants']:
            for name in v['sources']:
                if name not in sources or not (DEST/sources[name]['file']).exists():raise ValueError('Missing asset: '+name)
            if v['id'] in baked:
                flipbook=baked[v['id']]
                if not (DEST/flipbook['file']).exists():raise ValueError('Missing preview flipbook: '+v['id'])
                v['preview_flipbook']=flipbook
    data={'schema':1,'version':'2026-10-21-a','inventory_sha256':hashlib.sha256(INVENTORY.read_bytes()).hexdigest(),
          'status':'Auswahlentwürfe; keine fertigen Produktions-Exporte',
          'categories':categories,'effects':effects,'assets':sources,
          'variant_count':sum(len(e['variants']) for e in effects)}
    DEST.mkdir(parents=True,exist_ok=True)
    output=json.dumps(data,ensure_ascii=False,indent=2)
    (DEST/'katalog.json').write_text(output+'\n',encoding='utf-8')
    (DEST/'katalog.js').write_text('window.EDEN_FX_KATALOG = '+output+';\n',encoding='utf-8')
    print(f"Gallery catalog: {len(effects)} effects / {data['variant_count']} variants. Preview status explicit.")

if __name__=='__main__':build()

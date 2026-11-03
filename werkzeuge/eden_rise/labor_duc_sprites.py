"""Prepare existing Duc images for the isolated effect lab; never writes source images."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from PIL import Image, ImageOps
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
# 25.10.2026: fixed names (docs/wiki/systeme/aufruestung.md); folder suffixes stay Erde/Wasser/... and Sword/Bat/...
LOOKS={'Erde':'Terra Scura','Wasser':'Meramie','Feuer':'Incendio','Luft':'Zéphyr','Cyber':'Citadelle'}
WEAPONS={'Sword':'Riposte','Bat':'Terremoto','Knife':'Sussurro','Spear':'Le Large','Gun':'Gemelli'}
POSES=('idle','windup','attack','heavy_windup','heavy_attack','hurt','guard','weakened','enraged','flee','surrender','defeated','victory')

def pose_vorbereiten(normalise,file,dest,name,pose,scale,area):
    """One pose -> webp in dest; returns (anchor, provenance)."""
    before=hashlib.sha256(file.read_bytes()).hexdigest()
    image=Image.open(file).convert('RGBA');prepared=normalise.normalise(image,scale,area)
    alpha=np.asarray(prepared.getchannel('A'));mask=alpha>180
    ys,xs=np.nonzero(mask)
    if not len(ys):raise ValueError('Leere Pose: '+name+'/'+pose)
    bottom=int(ys.max())+1;top=int(ys.min());legs=mask[max(top,round(bottom-(bottom-top)*.23)):bottom]
    _,leg_x=np.nonzero(legs);center=float(leg_x.mean()) if len(leg_x) else float(xs.mean())
    anchor={'foot':bottom,'center_x':round(center,2),'width':prepared.width,'height':prepared.height,'scale':.42,'mirror':False}
    prepared.save(dest/(pose+'.webp'),quality=90,alpha_quality=100,method=6)   # lossy (25.10.): ~10 MB instead of ~100 MB
    if pose in ('idle','hurt','guard'):
        ImageOps.mirror(prepared).save(dest/('gegner_'+pose+'.webp'),quality=90,alpha_quality=100,method=6)
    after=hashlib.sha256(file.read_bytes()).hexdigest()
    if before!=after:raise ValueError('Quelle wurde während des Imports geändert: '+name+'/'+pose)
    return anchor,{'pose':pose,'source':str(file),'sha256':before,'sourceSize':list(image.size)}

def erneuern(output,normalise):
    """02.11.2026: only poses whose source changed since the catalog (e.g. knife heavy_attack 01.11.) are prepared again."""
    pfad=output/'katalog.json';catalog=json.loads(pfad.read_text(encoding='utf-8'));neu=0
    for item in catalog['sets']:
        dest=output.parent/item['directory'];anchors=json.loads((dest/'posen.json').read_text(encoding='utf-8'))
        quelle={p['pose']:p for p in item['sourcePoses']};vorher=neu
        for i,p in enumerate(item['sourcePoses']):
            file=Path(p['source'])
            if hashlib.sha256(file.read_bytes()).hexdigest()==p['sha256']:
                continue
            scale,area=normalise.idle_scale(Image.open(quelle['idle']['source']).convert('RGBA'),item['id'])
            anchors[p['pose']],item['sourcePoses'][i]=pose_vorbereiten(normalise,file,dest,item['id'],p['pose'],scale,area)
            neu+=1;print(item['id']+'/'+p['pose']+' erneuert.',flush=True)
        if neu>vorher:(dest/'posen.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    pfad.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(str(neu)+' Posen erneuert. Originale unverändert.',flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=Path('X:/AI/ComfyUI_krea2/ComfyUI/output/expressions/combat'))
    ap.add_argument('--output',type=Path,default=ROOT/'docs/effekt-auswahl/status-labor/assets/duc-varianten-v1')
    ap.add_argument('--erneuern',action='store_true',help='existing catalog: prepare changed sources again')
    args=ap.parse_args()
    if args.erneuern:
        spec=importlib.util.spec_from_file_location('eden_lab_sprite_normalise',ROOT/'werkzeuge/kampf_bilder.py')
        normalise=importlib.util.module_from_spec(spec);spec.loader.exec_module(normalise)
        return erneuern(args.output,normalise)
    if args.output.exists():
        raise SystemExit('Ziel existiert bereits. Bitte einen neuen Ausgabeordner verwenden.')
    expected=[(look,weapon,'Duc'+look+weapon) for look in LOOKS for weapon in WEAPONS]
    for _,_,name in expected:
        for pose in POSES:
            if not (args.source/name/(pose+'.png')).is_file():
                raise SystemExit('Pose fehlt: '+name+'/'+pose)
    spec=importlib.util.spec_from_file_location('eden_lab_sprite_normalise',ROOT/'werkzeuge/kampf_bilder.py')
    normalise=importlib.util.module_from_spec(spec);spec.loader.exec_module(normalise)
    args.output.mkdir(parents=True)
    catalog={'version':1,'sourceUnmodified':True,'normalisation':'werkzeuge/kampf_bilder.py','looks':LOOKS,'weapons':WEAPONS,'sets':[]}
    for index,(look,weapon,name) in enumerate(expected,1):
        source=args.source/name;dest=args.output/name;dest.mkdir()
        idle=Image.open(source/'idle.png').convert('RGBA')
        scale,area=normalise.idle_scale(idle,name)
        anchors={};provenance=[]
        for pose in POSES:
            anchors[pose],herkunft=pose_vorbereiten(normalise,source/(pose+'.png'),dest,name,pose,scale,area)
            provenance.append(herkunft)
        (dest/'posen.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        catalog['sets'].append({'id':name,'look':look,'weapon':weapon,'label':LOOKS[look]+' · '+WEAPONS[weapon],'directory':args.output.name+'/'+name+'/','poses':list(POSES),'sourcePoses':provenance})
        print(str(index)+'/25: '+name+' vorbereitet.',flush=True)
    (args.output/'katalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('25 Sets, 325 Spielerposen und 75 Vergleichsposen. Originale unverändert.',flush=True)

if __name__=='__main__':main()

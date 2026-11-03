"""Build public skill UI examples using copied engine code; never loads a save or config."""
import argparse
from collections import deque
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/effekt-auswahl/status-labor/faehigkeiten/beispieldaten.js')
    args=parser.parse_args()
    public=json.loads((ROOT/'module/eden_rise/kaempfe.json').read_text(encoding='utf-8'))
    defs={k:public[k] for k in ('specials','weapons','armors')}
    with tempfile.TemporaryDirectory(prefix='eden_skill_showcase_') as temp:
        isolated=Path(temp)
        (isolated/'kern').mkdir()
        for p in (ROOT/'kern').glob('*.py'):
            shutil.copy2(p,isolated/'kern'/p.name)
        sys.path.insert(0,str(isolated))
        from kern import kampf
        scenarios={
            'experienced':(10,['doppio_gioco','sotto_voce','vendetta','mistral']),
            'crossroads':(7,['mistral','doppio_gioco']),
            'beginner':(3,[]),
            'spent':(10,['mistral','ressac','libeccio','doppio_gioco','sotto_voce','vendetta'])}
        def key(z):
            return str(z['combat']['level'])+':'+','.join(sorted(z['combat']['skills']))
        profiles={};starts={};queue=deque()
        for name,(level,skills) in scenarios.items():
            z={'persona':{'attribute':{a:2 for a in kampf.ATTR_LABEL}},
               'combat':{'level':level,'xp':0,'skills':skills},
               'equipment':{'weapon':'bat','armor':None},'inventar':[]}
            starts[name]=key(z);queue.append(z)
        while queue:
            z=queue.popleft();stamp=key(z)
            if stamp in profiles:
                continue
            p=kampf.profil(copy.deepcopy(z),defs)
            keep=['level','level_max','xp','xp_next','skillpunkte','skillpunkte_gesamt','skillpunkte_plan',
                  'hauptpfad','hauptpfad_info','hauptpfad_prioritaet','pfade','hinweis']
            profiles[stamp]={k:p[k] for k in keep}
            for pf in p['pfade']:
                for s in pf['skills']:
                    if not s['gelernt'] and not s['grund']:
                        child=copy.deepcopy(z)
                        kampf.lernen(child,defs,s['id']);queue.append(child)
        text='window.EDEN_SKILL_DEMO='+json.dumps({'scenarios':starts,'profiles':profiles},ensure_ascii=False,indent=2)+';\n'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(text,encoding='utf-8',newline='\n')
    print(str(len(profiles))+' Beispielstände aus isolierten Engine-Funktionen geschrieben.')

if __name__=='__main__':
    main()

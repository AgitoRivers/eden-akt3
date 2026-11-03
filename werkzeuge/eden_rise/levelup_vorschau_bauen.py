"""Level-up ceremony preview (Duc 28.10.2026): example states built with copied engine code (kampf.profil,
attribut_steigern, lernen); never loads a save or config. Writes docs/effekt-auswahl/status-labor/levelup/daten.js.
The page next to it plays the real client module eden-levelup.js on these states."""
import argparse
from collections import deque
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
KEEP = ['level', 'level_max', 'xp', 'xp_next', 'lp', 'lp_max', 'attribute', 'attributpunkte', 'skillpunkte',
        'skillpunkte_gesamt', 'skillpunkte_plan', 'hauptpfad', 'hauptpfad_info', 'hauptpfad_prioritaet', 'pfade', 'hinweis']
# name: (title, level before, level after, learned skills, result lines)
SZENEN = {
    'level3': ('Level 3 · first skill', 2, 3, [], ['+120 experience', 'Level 3! +1 attribute point · +1 skill point']),
    'level4': ('Level 4 · attribute only', 3, 4, ['scirocco'], ['+160 experience', 'Level 4! +1 attribute point']),
    'level9': ('Level 9 · mastering a path', 8, 9, ['scirocco', 'retour', 'furia'],
               ['+420 experience', 'Level 9! +1 attribute point · +1 skill point']),
    'level10': ('Level 10 · finale', 9, 10, ['mistral', 'scirocco', 'retour', 'furia'],
                ['+540 experience', 'Level 10! +1 attribute point · +2 skill points', 'Inventory full – Emerald stays behind']),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=ROOT / 'docs/effekt-auswahl/status-labor/levelup/daten.js')
    args = ap.parse_args()
    public = json.loads((ROOT / 'module/eden_rise/kaempfe.json').read_text(encoding='utf-8'))
    defs = {k: public[k] for k in ('specials', 'weapons', 'armors')}
    with tempfile.TemporaryDirectory(prefix='eden_levelup_') as temp:
        (Path(temp) / 'kern').mkdir()
        for p in (ROOT / 'kern').glob('*.py'):
            shutil.copy2(p, Path(temp) / 'kern' / p.name)
        sys.path.insert(0, temp)
        from kern import kampf

        def key(z):
            c = z['combat']
            return '%d:%s:%s' % (c['level'], ','.join(sorted(c['skills'])),
                                 ','.join('%s%d' % (a, v) for a, v in sorted(z['persona']['attribute'].items())))

        profile, wege, start, szenen = {}, {}, {}, {}
        q = deque()
        for name, (titel, von, auf, skills, zeilen) in SZENEN.items():
            attrs = {a: 2 for a in kampf.ATTR_LABEL}
            attrs.update(strength=3, courage=3 if auf > 4 else 2)
            z = {'persona': {'attribute': attrs}, 'combat': {'level': auf, 'xp': 0, 'skills': list(skills), 'attributpunkte': 1},
                 'equipment': {'weapon': 'bat', 'armor': None}, 'inventar': [], 'lp': 31, 'flags': [], 'tag': 9, 'phase': 0}
            start[name] = key(z)
            szenen[name] = {'titel': titel, 'kampf': {'id': 'vorschau-' + name, 'runde': 7, 'ergebnis': {
                'art': 'ko', 'text': 'The lion goes down and stays down, breathing hard. The red light at the back of its neck keeps blinking.',
                'zeilen': zeilen, 'aufstieg': {'von': von, 'auf': auf, 'lp': kampf.LP_PER_LEVEL * (auf - von),
                                               'ausdauer': kampf.max_stamina(auf) - kampf.max_stamina(von)}}}}
            q.append(z)
        while q:
            z = q.popleft()
            k = key(z)
            if k in profile:
                continue
            p = kampf.profil(copy.deepcopy(z), defs)
            profile[k] = {x: p[x] for x in KEEP}
            wege[k] = {}
            nach = []
            if p['attributpunkte'] > 0:
                for a in p['attribute']:
                    if a['wert'] < a['max']:
                        nach.append(('attr:' + a['id'], lambda c, a=a: kampf.attribut_steigern(c, a['id'])))
            elif p['skillpunkte'] > 0:
                for pf in p['pfade']:
                    for s in pf['skills']:
                        if not s['gelernt'] and not s['grund']:
                            nach.append(('learn:' + s['id'], lambda c, s=s: kampf.lernen(c, defs, s['id'])))
            for weg, tu in nach:
                c = copy.deepcopy(z)
                tu(c)
                wege[k][weg] = key(c)
                q.append(c)
    text = 'window.EDEN_LEVELUP_DEMO=' + json.dumps({'szenen': szenen, 'start': start, 'profile': profile, 'wege': wege},
                                                    ensure_ascii=False) + ';\n'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding='utf-8', newline='\n')
    print('%d Zustände für %d Szenen geschrieben: %s' % (len(profile), len(szenen), args.output))


if __name__ == '__main__':
    main()

"""Checks only copied/public assets and the static handler; no engine import or saves."""
import ast
import json
from pathlib import Path
import tempfile
import unittest
import urllib.parse

REPO = Path(__file__).resolve().parents[1]


class SkillsAssets(unittest.TestCase):
    def test_mapping_matches_public_skills_and_approved_art(self):
        skills = json.loads((REPO / 'module/eden_rise/kaempfe.json').read_text(encoding='utf-8'))['specials']
        source = REPO / 'docs/effekt-auswahl/status-labor/skill-icons'
        approved = json.loads((source / 'katalog.json').read_text(encoding='utf-8'))['icons']
        module = (REPO / 'client/plugins/eden-skills/eden-skills.js').read_text(encoding='utf-8')
        mapping = {'mistral':'mistral','ressac':'wave','libeccio':'wind','lame_de_fond':'tidal',
                   'doppio_gioco':'doubleSlash','sotto_voce':'blur','vendetta':'vendetta','omerta':'blackSlash',
                   'point_de_mire':'reticle','bonaccia':'calm','phare':'beam','pluie_d_etoiles':'rain',
                   'scirocco':'scirocco','retour':'retour','furia':'furia','vulcano':'vulcano',
                   'elicriso':'balm','ponente':'westWind','risveglio':'awaken','arcangelo':'archangel'}   # Heiler 26.10.
        self.assertEqual(set(mapping), set(skills))
        for key, icon in mapping.items():
            self.assertIn(key + ":'" + icon + "'", module)
            self.assertEqual((REPO / 'client/plugins/eden-skills/icons' / approved[icon]['file']).read_bytes(),
                             (source / approved[icon]['file']).read_bytes())

    def test_public_route_without_loading_engine(self):
        tree = ast.parse((REPO / 'eden.py').read_text(encoding='utf-8'))
        handler = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Handler')
        method = next(n for n in handler.body if isinstance(n, ast.FunctionDef) and n.name == 'do_GET')
        extracted = ast.fix_missing_locations(ast.Module(body=[method], type_ignores=[]))
        with tempfile.TemporaryDirectory(prefix='eden_skills_route_') as temp:
            base = Path(temp)
            public = base / 'client/plugins/eden-skills'
            public.mkdir(parents=True)
            (public / 'eden-skills.js').write_text('/* fixture */', encoding='utf-8')
            (public / 'outside.txt').write_text('not a public type', encoding='utf-8')
            scope = {'BASE':str(base), 'urllib':urllib, 'json':json}
            exec(compile(extracted, '<isolated static handler>', 'exec'), scope)
            class Request:
                def __init__(self, path): self.path = path
                def datei(self, path, mime, cache=True): return (200, mime, cache)
                def senden(self, status, body): return (status, body)
            self.assertEqual(scope['do_GET'](Request('/plugins/eden-skills/eden-skills.js?v=1')),
                             (200, 'text/javascript', False))
            for path in ['/plugins/eden-skills/missing.png', '/plugins/eden-skills/outside.txt',
                         '/plugins/eden-skills/%2e%2e/%2e%2e/outside.txt']:
                self.assertEqual(scope['do_GET'](Request(path))[0], 404)
            preview = base / 'docs/effekt-auswahl/status-labor/ablaufprobe'
            preview.mkdir(parents=True)
            (preview / 'skill-preview.html').write_text('<canvas></canvas>', encoding='utf-8')
            (preview / 'private.html').write_text('not public', encoding='utf-8')
            (public / 'preview-files.json').write_text(json.dumps(['ablaufprobe/skill-preview.html']), encoding='utf-8')
            self.assertEqual(scope['do_GET'](Request('/plugins/eden-skills/preview/ablaufprobe/skill-preview.html')),
                             (200, 'text/html', False))
            for path in ['/plugins/eden-skills/preview/ablaufprobe/private.html',
                         '/plugins/eden-skills/preview/quellen/manifest.json',
                         '/plugins/eden-skills/preview/%2e%2e/private.html']:
                self.assertEqual(scope['do_GET'](Request(path))[0], 404)

    def test_point_schedule_comes_from_existing_server_constants(self):
        tree = ast.parse((REPO / 'kern/kampf.py').read_text(encoding='utf-8'))
        assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == 'SKILL_POINTS' for t in n.targets))
        plan = ast.literal_eval(assignment.value)
        profile = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'profil')
        result = next(n.value for n in profile.body if isinstance(n, ast.Return))
        fields = {k.value: v for k, v in zip(result.keys, result.values)}
        scope = {'SKILL_POINTS': plan, 'LEVEL_MAX': 10}
        total = eval(compile(ast.Expression(fields['skillpunkte_gesamt']), '<profile contract>', 'eval'), scope)
        schedule = eval(compile(ast.Expression(fields['skillpunkte_plan']), '<profile contract>', 'eval'), scope)
        self.assertEqual(total, 6)
        self.assertEqual(schedule, [{'level':3,'punkte':1}, {'level':5,'punkte':1}, {'level':7,'punkte':1},
                                    {'level':9,'punkte':1}, {'level':10,'punkte':2}])

    def test_preview_manifest_contains_only_existing_public_runtime(self):
        files = json.loads((REPO / 'client/plugins/eden-skills/preview-files.json').read_text(encoding='utf-8'))
        root = REPO / 'docs/effekt-auswahl/status-labor'
        self.assertIn('ablaufprobe/skill-preview.html', files)
        self.assertIn('assets/duc-links/posen.json', files)
        self.assertEqual(len(files), len(set(files)))
        for name in files:
            self.assertNotIn('quellen', Path(name).parts)
            self.assertTrue((root / name).is_file(), name)


if __name__ == '__main__':
    unittest.main()

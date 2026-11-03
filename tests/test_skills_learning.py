"""Read-only learning forecast against real combat functions, with disposable states."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from kern import kampf

DEFS=json.loads((ROOT/'module/eden_rise/kaempfe.json').read_text(encoding='utf-8'))
DEFS={key:DEFS[key] for key in ('specials','weapons','armors')}

def character(skills=(),level=7,armor=None):
    return {'persona':{'attribute':{a:2 for a in kampf.ATTR_LABEL}},
            'combat':{'level':level,'xp':0,'skills':list(skills)},
            'equipment':{'weapon':'bat','armor':armor},'inventar':[]}

class SkillsLearning(unittest.TestCase):
    def test_forecast_matches_real_learning_and_preserves_original(self):
        z=character(['mistral','doppio_gioco']);before=copy.deepcopy(z)
        preview=kampf.learning_preview(z,DEFS,'scirocco')
        self.assertEqual(z,before)
        self.assertEqual(preview['before']['name'],'Fighter')
        self.assertEqual(preview['after']['name'],'Berserker')
        self.assertTrue(preview['changed']);self.assertTrue(preview['tie'])
        actual=copy.deepcopy(z);kampf.lernen(actual,DEFS,'scirocco')
        self.assertEqual(preview['after']['id'],kampf.main_path(DEFS,actual['combat']['skills']))
        self.assertEqual(preview['attributes'],[])   # the path no longer grows attributes, level-ups give points (26.10.)

    def test_first_path_and_unchanged_path(self):
        first=kampf.learning_preview(character(level=3),DEFS,'scirocco')
        self.assertIsNone(first['before']['name']);self.assertEqual(first['after']['id'],'M')
        unchanged=kampf.learning_preview(character(['doppio_gioco','sotto_voce','vendetta','mistral'],10),DEFS,'ressac')
        self.assertFalse(unchanged['changed']);self.assertEqual(unchanged['attributes'],[])

    def test_locked_and_learned_skills_have_no_forecast(self):
        self.assertIsNone(kampf.learning_preview(character(level=3),DEFS,'vulcano'))
        self.assertIsNone(kampf.learning_preview(character(['mistral']),DEFS,'mistral'))
        self.assertIsNone(kampf.learning_preview(character(['mistral'],3),DEFS,'scirocco'))

    def test_existing_armor_and_base_values_are_included(self):
        z=character(['mistral','doppio_gioco'])
        z['persona']['attribute']['strength']=5
        preview=kampf.learning_preview(z,DEFS,'scirocco')
        self.assertNotIn('strength',[a['id'] for a in preview['attributes']])
        armor=next(((key,value) for key,value in DEFS['armors'].items() if value.get('bonus')),None)
        if armor:
            z['equipment']['armor']=armor[0]
            actual=copy.deepcopy(z);kampf.lernen(actual,DEFS,'scirocco')
            old=kampf.attributes(copy.deepcopy(z),DEFS);new=kampf.attributes(actual,DEFS)
            preview=kampf.learning_preview(z,DEFS,'scirocco')
            for item in preview['attributes']:
                self.assertEqual((item['before'],item['after']),(old[item['id']],new[item['id']]))

    def test_profile_exposes_forecasts_and_actual_tie_order(self):
        z=character(['mistral','doppio_gioco']);p=kampf.profil(z,DEFS)
        self.assertEqual(p['hauptpfad_prioritaet'],['Berserker','Fighter','Smuggler','Marksman','Healer'])
        skill=next(s for pf in p['pfade'] for s in pf['skills'] if s['id']=='scirocco')
        self.assertTrue(skill['lernfolgen']['changed'])
        self.assertEqual(skill['lernfolgen'],kampf.learning_preview(z,DEFS,'scirocco'))

    def test_skill_numbers_follow_current_values(self):
        z=character(['mistral']);n=kampf.skill_zahlen(z,DEFS)
        self.assertEqual(set(n),set(DEFS['specials']))
        sp={'attrs':kampf.attributes(z,DEFS),'weapon':DEFS['weapons']['bat'],'main_path':'K'}
        base=kampf.BASE_ATTACK+kampf._attack_attr(sp)+DEFS['weapons']['bat']['dmg']
        self.assertEqual(n['mistral']['chip'],'%d dmg'%(base+4))
        self.assertEqual(n['elicriso']['chip'],'+%d HP'%round(kampf.max_lp(7)*kampf.H3_HEAL))
        z['persona']['attribute']['strength']=4
        self.assertGreater(int(kampf.skill_zahlen(z,DEFS)['mistral']['chip'].split()[0]),base+4)
        skill=next(s for pf in kampf.profil(character(['mistral']),DEFS)['pfade'] for s in pf['skills'] if s['id']=='omerta')
        self.assertTrue(skill['zahl'].endswith('+ dmg'));self.assertTrue(skill['zahlen'])

if __name__=='__main__':unittest.main()

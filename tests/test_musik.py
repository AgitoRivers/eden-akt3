import os, sys, random, unittest, threading, urllib.request, urllib.error, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import eden
from kern import musik
class MusicTests(unittest.TestCase):
    def state(self,sid='alltag',ort='sun_deck',phase='tag',status='szene'):
        return {'id':'test-run','tag':3,'phase':phase,'status':status,'szene':{'def':{'id':sid,'ort':ort}}}
    def hint(self,state):return musik.hint(eden.BASE,'eden_rise',state)
    def test_contexts_and_silence(self):
        self.assertEqual(self.hint(None)['slot'],'hauptthema')
        self.assertEqual(self.hint(self.state())['slot'],'deck_tag')
        self.assertEqual(self.hint(self.state(ort='village_harbour'))['slot'],'hafen_tag')
        self.assertEqual(self.hint(self.state(ort='crew_mess',phase='fruehstueck'))['slot'],'crew_alltag')
        self.assertTrue(self.hint(self.state(status='ereignis'))['stille'])
        # Bordmusik nach Tageszeit statt Stille (Duc 27.10.2026)
        for state, slot in [(self.state(phase='nacht'),'nachts_vor_anker'),(self.state(ort='power_room'),'deck_tag'),
                            (self.state(ort='main_salon',phase='dinner'),'crew_messe'),(self.state(status='wahl',phase='fruehstueck'),'crew_alltag'),
                            (self.state(status='wahl',phase='abend'),'nachts_vor_anker'),(self.state('cliffhanger','foredeck','nacht'),'mysterium')]:
            self.assertEqual(self.hint(state)['slot'], slot)
        anruf = self.state('megan_ankuendigung', 'duc_cabin', 'nachmittag'); anruf['szene']['def']['anruf'] = True
        self.assertEqual(self.hint(anruf)['slot'], 'deck_tag')
        urteil = self.state('nach_dem_urteil', 'crew_mess', 'abend')
        self.assertEqual(self.hint(urteil)['slot'], 'event_ernst')
        urteil['flags'] = ['urteil_erbarmen']; h = self.hint(urteil)
        self.assertEqual(h['slot'], 'event_wholesome')
        self.assertIn('Bittersweet', [t['title'] for t in h['playlist']])
        black=self.hint(self.state('blackout'))
        self.assertTrue(black['stille']);self.assertEqual(black['uebergang_ms'],0)
        self.assertIsNone(musik.hint(eden.BASE,'eden_consulting',None)['track'])
    def test_event_tones(self):
        from kern import ereignisse
        events = ereignisse.daten(str(Path(eden.BASE) / 'module' / 'eden_rise'))['events']
        for tone, slot in [('witzig', 'event_witzig'), ('ernst', 'event_ernst'), ('frech', 'event_frech'), ('wholesome', 'event_wholesome')]:
            event = next(e for e in events if e.get('ton') == tone)
            state = self.state(status='ereignis')
            state['event'] = {'id': event['id']}
            hint = self.hint(state)
            self.assertEqual(hint['slot'], slot)
            if slot:
                self.assertEqual(len(hint['playlist']), sum(t['slot'] == slot for t in musik.tracks(eden.BASE, 'eden_rise')))
                self.assertTrue(musik.audio_path(eden.BASE, 'eden_rise', hint['track']['id']).is_file())

    def test_charter_party(self):
        hint = self.hint(self.state('auftakt_party', phase='abend'))
        self.assertEqual(hint['slot'], 'charter_nacht')
        self.assertEqual(hint['track']['title'], 'Your Call')

    def test_sophia_arc_music(self):
        state = self.state('naehe', phase='nacht')
        state['szene']['def']['anwesend'] = ['sophia']
        hint = self.hint(state)
        self.assertEqual(hint['slot'], 'sophia_naehe')
        self.assertEqual(hint['track']['id'], '9f0b5a571c1a40c2a1b1ef782e8160f9')
        for people in [['lea'], ['sophia', 'lea'], []]:
            state['szene']['def']['anwesend'] = people
            self.assertEqual(self.hint(state)['slot'], 'naehe')

    def test_plankton_event(self):
        state = self.state(status='ereignis')
        state['event'] = {'id': 'hy_lea_plankton'}
        self.assertEqual(self.hint(state)['slot'], 'leuchtendes_meer')

    def test_stable_selection_and_files(self):
        before=random.getstate();a=self.hint(self.state());b=self.hint(self.state())
        self.assertEqual(a,b);self.assertEqual(before,random.getstate());self.assertEqual(len(a['playlist']),sum(t['slot']=='deck_tag' for t in musik.tracks(eden.BASE,'eden_rise')))
        records=musik.tracks(eden.BASE,'eden_rise');self.assertGreaterEqual(len(records),30)
        for record in records:
            self.assertTrue(musik.audio_path(eden.BASE,'eden_rise',record['id']).is_file())
        self.assertIsNone(musik.audio_path(eden.BASE,'eden_rise','../eden-config.json'))
        self.assertIsNone(musik.audio_path(eden.BASE,'eden_rise','a'*32))
        public=json.dumps(a);self.assertNotIn('X:',public);self.assertNotIn('seed',public)
    def test_selected_slots_and_credits(self):
        from collections import defaultdict
        library = json.loads((Path(eden.BASE) / 'module/eden_rise/musik/auswahl.json').read_text(encoding='utf-8'))
        pools = defaultdict(set)
        for track in musik.tracks(eden.BASE, 'eden_rise'):
            pools[track['slot']].add(track['id'])
        for slot in library['replace_slots']:
            self.assertEqual(pools[slot], {t['id'] for t in library['tracks'] if t['slot'] == slot})
        self.assertEqual(self.hint(self.state(status='kabine'))['slot'], 'kabine')
        self.assertEqual(self.hint(self.state(status='ende'))['slot'], 'calvi_tisch')
        for sid, slot in [('sturmvorbereitung','sturm'), ('sturmnacht','sturm'), ('erste_ermittlung','mysterium'), ('anhoerung','megan_bericht')]:
            self.assertEqual(self.hint(self.state(sid))['slot'], slot)
        for eid, slot in [('ab_casanova_flamenco','casanova_flamenco'), ('ab_lola_klopft','lola_abend'), ('ab_alva_barabend','alva_abend'),
                          ('kl_casanova_auftrag','expedition_macchia'), ('hk_hilfe','expedition_hafen')]:
            state = self.state(status='ereignis'); state['event'] = {'id': eid}
            self.assertEqual(self.hint(state)['slot'], slot)
        for sid in ['blackout','explosion','brand']:
            self.assertTrue(self.hint(self.state(sid))['stille'])
        self.assertEqual(self.hint(self.state('wache_mit_holm'))['slot'], 'holm_wache')
        self.assertTrue(self.hint(self.state('holm_abschied'))['stille'])

    def test_second_selection_contexts(self):
        for ort, phase, people, slot in [
            ('power_room', 'tag', ['rosi'], 'rosi_technik'),
            ('workshop', 'abend', ['rosi'], 'rosi_technik'),
            ('generator_room', 'nacht', ['rosi'], 'rosi_technik'),
            ('crew_mess', 'dinner', ['lola'], 'crew_messe'),
            ('foredeck', 'nacht', ['lea'], 'nachts_vor_anker'),
        ]:
            state = self.state('frei_test', ort=ort, phase=phase)
            state['szene']['def'].update(frei=True, anwesend=people)
            hint = self.hint(state)
            self.assertEqual(hint['slot'], slot)
            self.assertFalse(hint['stille'])
        self.assertEqual(self.hint(self.state('reparaturschritt', ort='power_room'))['slot'], 'rosi_technik')
        for sid in ['explosion', 'blackout']:              # cold_open hat seit 27.10.2026 Bordmusik
            state = self.state(sid, ort='power_room')
            state['szene']['def']['anwesend'] = ['rosi']
            self.assertTrue(self.hint(state)['stille'])

    def test_hearing_confession_music(self):
        state = self.state(status='verhandlung'); state['verhandlung'] = {'schritt': 'rolle'}
        h = self.hint(state)
        self.assertTrue(h['stille'])                       # Rolle bleibt still
        self.assertEqual(h['gestaendnis']['slot'], 'anhoerung_gestaendnis')
        self.assertEqual(len(h['gestaendnis']['playlist']), 3)

    def test_combat_music(self):
        state = self.state(status='kampf')
        for enemy, slot in [('taschendieb','kampf_normal'),('moewe','kampf_komisch'),('ratte','kampf_komisch'),('affe','kampf_komisch'),('pirat','kampf_gefaehrlich'),
                            ('keiler','kampf_tiere'),('hunde_paar','kampf_tiere'),('ratte_alpha','kampf_tiere')]:
            state['kampf'] = {'id':'test','def':{'enemy':enemy},'gegner':[{'def':{}}]}
            self.assertEqual(self.hint(state)['slot'], slot)
        state['kampf']['gegner'][0]['def']['boss'] = True
        self.assertEqual(self.hint(state)['slot'], 'kampf_boss')
        state['kampf']['ergebnis'] = {'art':'niederlage'}
        self.assertEqual(self.hint(state)['slot'], 'kampf_niederlage')
        self.assertTrue(self.hint(state)['einmalig'])
        state['kampf']['ergebnis'] = {'art':'ko'}
        self.assertEqual(self.hint(state)['slot'], 'kampf_sieg')  # Fanfare (Duc 27.10.2026)
        self.assertTrue(self.hint(state)['einmalig'])

    def test_http_stream_and_plugins(self):
        server=eden.ThreadingHTTPServer(('127.0.0.1',0),eden.Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        url='http://127.0.0.1:'+str(server.server_port)
        try:
            with urllib.request.urlopen(url+'/musik/credits') as response:
                self.assertIn(b'Kevin MacLeod',response.read())
            hint=self.hint(None)
            req=urllib.request.Request(url+hint['track']['url'],headers={'Range':'bytes=0-15'})
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.status,206);self.assertEqual(len(response.read()),16)
                self.assertTrue(response.headers['Content-Range'].startswith('bytes 0-15/'))
            flac = next(t for t in musik.tracks(eden.BASE, 'eden_rise') if t['file'].endswith('.flac') and t.get('license') == 'RouteNote Licensing')
            req = urllib.request.Request(url+'/musik/audio/'+flac['id'], headers={'Range':'bytes=0-15'})
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.status, 206)
                self.assertEqual(response.headers['Content-Type'], 'audio/flac')
                self.assertEqual(response.read()[:4], b'fLaC')
            with urllib.request.urlopen(url+'/plugins/eden-music/eden-music.js') as response:self.assertIn(b'EdenMusic',response.read())
            for route in ['/musik/audio/invalid','/plugins/eden-music/eden.py']:
                with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(url+route)
                self.assertEqual(error.exception.code,404)
            req=urllib.request.Request(url+hint['track']['url'],headers={'Range':'bytes=9999999999-'})
            with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(req)
            self.assertEqual(error.exception.code,416)
        finally:server.shutdown();server.server_close();thread.join()
if __name__=='__main__':unittest.main(verbosity=2)

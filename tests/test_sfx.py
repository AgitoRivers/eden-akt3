# -*- coding: utf-8 -*-
"""Sound-Effekte (18.10.2026): Katalog nur mit gewaehlten Varianten, sichere Dateiroute, Story-Ausloeser.

    python tests\\test_sfx.py
"""
import importlib.util, json, sys, unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from kern import sfx  # noqa: E402

MOD = "eden_rise"
DATEN = json.loads((BASE / "module" / MOD / "sfx.json").read_text(encoding="utf-8"))


def state(status="szene", sid="", event="", tag=3, phase="tag"):
    z = {"id": "test-run", "tag": tag, "phase": phase, "status": status, "szene": {"def": {"id": sid}}}
    if event:
        z["event"] = {"id": event}
    return z


class SfxTests(unittest.TestCase):
    def test_katalog_waehlt(self):
        k = sfx.katalog(str(BASE), MOD)
        for s in DATEN["sfx"]:
            w = s.get("wahl")
            if isinstance(w, list):                                           # Abwechslung: mehrere gewaehlt
                self.assertEqual(k[s["id"]], ["/sfx/%s_%d.mp3" % (s["id"], n) for n in w], s["id"])
            elif w:
                self.assertEqual(k[s["id"]], ["/sfx/%s_%d.mp3" % (s["id"], w)], s["id"])
            else:
                self.assertEqual(len(k[s["id"]]), s["varianten"], s["id"])   # offen: alle Varianten
        self.assertEqual(sfx.katalog(str(BASE), "gibt_es_nicht"), {})

    def test_jede_url_ist_auslieferbar(self):
        for urls in sfx.katalog(str(BASE), MOD).values():
            for u in urls:
                self.assertIsNotNone(sfx.audio_path(str(BASE), MOD, u.rsplit("/", 1)[1]), u)

    def test_dateiroute_sicher(self):
        for name in ["../sfx.json", "..\\eden.py", "index.json", "vorhoeren.html", "x.mp3", "blackout_1.mp3.py",
                     "BLACKOUT_1.mp3", "blackout_9.mp3", "%2e%2e/eden.py", "ui_klick_123.mp3", "ui_klick_0.mp3"]:
            self.assertIsNone(sfx.audio_path(str(BASE), MOD, name), name)
        self.assertTrue(sfx.DATEI.fullmatch("ui_klick_12.mp3"))       # zweistellige Varianten (Klick-Konzepte)

    def test_maxwell_schlag(self):
        """Maxwells Treffer liegt im Katalog und als Datei vor, der Kampf spielt ihn nur fuer ihn (Duc 02.11.2026)."""
        ids = {s["id"] for s in json.loads((BASE / "module" / "eden_rise" / "sfx.json").read_text(encoding="utf-8"))["sfx"]}
        self.assertIn("tk_maxwell_schlag", ids)
        self.assertTrue((BASE / "module" / "eden_rise" / "sfx" / "tk_maxwell_schlag_1.mp3").exists())
        self.assertIn('k.held.id === "maxwell" ? "tk_maxwell_schlag"', (BASE / "client" / "plugins" / "eden-combat" / "eden-combat.js").read_text(encoding="utf-8"))

    def test_belagerung(self):
        """Morgen nach Rauch, Rosi mit Summen, nachts keine Bossa, Mr. White und Roboter mit ernster Kampfmusik (Duc 01.11.2026)."""
        from kern import musik
        amb = lambda z: sfx.ambience(str(BASE), MOD, z)
        self.assertEqual(amb(state("ereignis", event="bl_morgen_22")), "feuer_loop")
        self.assertEqual(amb(state("ereignis", event="bl_na_rosi")), "amb_maschine")
        self.assertEqual(amb(dict(state("taktik"), taktik={"phase": "bestand"})), "feuer_loop")
        slot = lambda z: musik.hint(str(BASE), MOD, z)["slot"]
        self.assertEqual(slot(state("ereignis", event="bl_nacht_wahl_21", phase="nacht")), "nachts_vor_anker")
        self.assertEqual(slot(state("ereignis", event="bl_na_lola", phase="nacht")), "naehe")
        if musik._playlist(str(BASE), MOD, "sophia_naehe"):                   # Sophias Titel liegt nicht im Repo
            self.assertEqual(slot(state("ereignis", event="bl_na_sophia", phase="nacht")), "sophia_naehe")
        self.assertEqual(slot(state("ereignis", event="bl_na_lola_still", phase="nacht")), "nachts_vor_anker")
        kampf = lambda e: dict(state("kampf"), kampf={"id": "k", "def": {"enemy": e}, "gegner": [{"def": {}}]})
        self.assertEqual(slot(kampf("tk_white")), "kampf_boss")
        self.assertEqual(slot(kampf("tk_robot")), "kampf_gefaehrlich")
        h = lambda eid: sfx.hint(str(BASE), MOD, state("ereignis", event=eid))["id"]
        self.assertEqual(h("bl_kirche"), "tk_glocke")
        self.assertEqual(h("bl_bericht"), "tk_kreide")       # nur die Kreide auf Alvas Tafel, die Glocke kommt erst mit Casanovas Satz (ZEILEN_TON)
        self.assertEqual(h("bl_na_lola"), "tuer_klopfen")
        self.assertIsNone(sfx.hint(str(BASE), MOD, state("ereignis", event="bl_na_lea")))
        self.assertEqual(amb(dict(state("taktik"), taktik={"phase": "spieler", "art": "echt"})), "amb_taktik")
        self.assertEqual(amb(dict(state("taktik"), taktik={"phase": "spieler", "art": "manoever"})), "amb_hafen")
        boss = lambda e: dict(state("kampf"), kampf={"id": "k", "def": {"enemy": e}, "gegner": [{"def": {"boss": True}}]})
        self.assertEqual(slot(boss("tk_robot")), "kampf_gefaehrlich")          # Vorlage Unit-01 ist ein Boss, der Boarding Robot nicht
        self.assertEqual(slot(kampf("tk_kobra")), "kampf_gefaehrlich")
        if musik._playlist(str(BASE), MOD, "taktik_karte"):                    # Musik liegt nicht im Repo
            self.assertEqual(slot(dict(state("taktik"), taktik={"phase": "spieler"})), "taktik_karte")
        ev = next(e for e in json.loads((BASE / "module" / MOD / "ereignisse.json").read_text(encoding="utf-8"))["events"] if e["id"] == "bl_kriegsrat")
        self.assertIn("the quiet side", json.dumps(ev["zeilen"][3]))          # index.html: ZEILEN_TON zeigt auf diese Zeile (Megans Satz bricht ab, Drehbuch Finale)
        js = (BASE / "client" / "plugins" / "eden-tactics" / "eden-tactics.js").read_text(encoding="utf-8")
        k = sfx.katalog(str(BASE), MOD)
        import re
        for tid in set(re.findall(r'"(tk_[a-z_]+)"', js)):
            self.assertIn(tid, k)
        taktik = json.loads((BASE / "module" / MOD / "taktik.json").read_text(encoding="utf-8"))     # Ton an einer Kartenzeile (Drehbuch Finale)
        for sid, zeilen in taktik["szenen"].items():
            for x in zeilen:
                if len(x) > 2 and x[2].get("ton"):
                    self.assertIn(x[2]["ton"], k, sid)

    def test_hinweise(self):
        h = lambda z: sfx.hint(str(BASE), MOD, z)
        self.assertIsNone(h(None))
        self.assertIsNone(h(state(sid="alltag")))
        self.assertEqual(h(state(sid="holm_abschied"))["id"], "hubschrauber_holm")
        self.assertEqual(h(state(sid="sturmnacht"))["id"], "sturm_nacht")
        b = h(state(sid="blackout"))
        self.assertEqual((b["id"], b["nach"]), ("blackout", "strom_zurueck"))
        self.assertEqual(h(state("ereignis", event="ab_lola_klopft"))["id"], "tuer_klopfen")
        self.assertIsNone(h(state("ereignis", event="gibt_es_nicht")))
        # gleicher Auftritt = gleicher Schluessel, anderer Tag = neuer Schluessel (Client spielt je Auftritt einmal)
        self.assertEqual(h(state(sid="blackout"))["key"], h(state(sid="blackout"))["key"])
        self.assertNotEqual(h(state(sid="landgang", tag=2))["key"], h(state(sid="landgang", tag=4))["key"])

    def test_grotte(self):
        """Grotten-Mission (29.10.2026): Frame-Momente, Kampf-Auftakt nach Gegnertyp, Hoehle statt Vogelgezwitscher."""
        h = lambda z: sfx.hint(str(BASE), MOD, z)
        self.assertEqual(h(state("ereignis", event="gr_u1_gitter"))["id"], "gitter")
        self.assertEqual(h(state("ereignis", event="kv_glocke"))["id"], "glocke")
        kampf = lambda bid, typ: dict(state("kampf"), kampf={"id": "k1", "definition": bid, "gegner": [{"typ": typ}]})
        self.assertEqual(h(kampf("fn_3_viper", "schlange_alpha"))["id"], "kampf_viper")
        # der seltene Gegner einer Begegnung bekommt seinen eigenen Auftakt, nicht den der Begegnung
        self.assertEqual(h(kampf("fn_2_fledermaeuse", "vampirin"))["id"], "kampf_pale_lady")
        self.assertEqual(h(kampf("fn_2_fledermaeuse", "fledermaeuse"))["id"], "kampf_fledermaeuse")
        self.assertEqual(h(kampf("hafen_ratten", "ratte"))["id"], "rudel_ratten")          # Begegnung wie bisher
        a = lambda **z: sfx.ambience(str(BASE), MOD, dict(state("ereignis", event=z.pop("ev")), **z))
        self.assertEqual(a(ev="gr_gang", ort_aktiv="grotte", ort_frame="gr_gang"), "amb_grotte")
        self.assertEqual(a(ev="gr_gang", ort_aktiv="grotte", ort_frame="gr_gang", ort_besiegt=["gr_gang"]), "amb_grotte")
        self.assertEqual(a(ev="fn_gang", ort_aktiv="grotte_flut", ort_frame="fn_gang"), "amb_grotte_flut")
        self.assertEqual(a(ev="kv_start"), "amb_daecher")
        self.assertEqual(a(ev="kv_start", phase="nacht"), "amb_daecher")

    def test_ausloeser_ids_gueltig(self):
        spec = importlib.util.spec_from_file_location("sfx_builder", BASE / "werkzeuge" / "eden_rise" / "sfx_eden_rise.py")
        b = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(b)
        self.assertEqual(b.pruefen_ausloeser(), [])
        self.assertEqual(DATEN["ausloeser"], b.AUSLOESER, "sfx.json veraltet - Builder neu laufen lassen")

    def test_ansicht_liefert_sfx(self):
        import eden
        v = eden.ansicht(None)
        self.assertIn("katalog", v["sfx"])
        self.assertIsNone(v["sfx"]["hinweis"])


if __name__ == "__main__":
    unittest.main(verbosity=1)

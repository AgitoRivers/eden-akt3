"""Erzaehlerin liest den Lagetext der Ortsbilder (Duc 02.11.2026).

Der Server muss fuer '<event>#l' genau den Text liefern, den vertonen_eden_rise.saetze() vertont hat,
sonst findet stimme.chatterbox die Aufnahme nicht und erzeugt live neu."""
import importlib.util, os, sys, unittest
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL))
import eden

_spec = importlib.util.spec_from_file_location("vertonen_eden_rise", WURZEL / "werkzeuge" / "eden_rise" / "vertonen_eden_rise.py")
vertonen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vertonen)


class ErzaehlerinTests(unittest.TestCase):
    def test_server_text_gleich_vertonung(self):
        lagen = {k[:-2]: (wer, text) for k, wer, text in vertonen.saetze() if k.endswith("#l")}
        self.assertGreater(len(lagen), 200)
        for eid, (wer, text) in lagen.items():
            self.assertEqual(eden.event_zeile(eid + "#l"), (wer, text), eid)

    def test_nur_ortsbilder(self):
        d = eden.ereignisse.daten(eden.moddir())
        andere = next(e for e in d["_index"].values() if e.get("art") != "ort" and e.get("lage"))
        self.assertEqual(eden.event_zeile(andere["id"] + "#l"), (None, None))
        mit_platzhalter = [e for e in d["_index"].values() if e.get("art") == "ort" and "{" in (e.get("lage") or "")]
        for e in mit_platzhalter:
            self.assertEqual(eden.event_zeile(e["id"] + "#l"), (None, None), e["id"])

    def test_zeilen_unveraendert(self):
        ev = eden.ereignisse.daten(eden.moddir())["_index"]["hk_ziege"]
        if ev["zeilen"]:
            self.assertEqual(eden.event_zeile("hk_ziege#z0"), (ev["zeilen"][0]["wer"], ev["zeilen"][0]["text"]))


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Ducs Gefuehls-Posen fuer Dialoge (Duc 03.11.2026): je Jacke 44 SFW-Posen ohne Waffe, mit Sonnenbrille.
duc_bild(z, gefuehl) nimmt die Pose der getragenen Jacke, fehlende Gefuehle fallen auf ein vorhandenes zurueck.

  python tests\\test_duc_gefuehle.py
"""
import os, sys, tempfile, unittest

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
ORDNER = os.path.join(os.path.dirname(HIER), "module", "eden_rise", "charakter", "gefuehle")
LOOKS = ("Erde", "Wasser", "Feuer", "Luft", "Cyber")


def durchlauf():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_gefuehle_"))
    z = E.aktion("neu", {"modus": "ironman"})
    z = E.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = E.aktion("prolog", {})
    return z


class DucGefuehle(unittest.TestCase):
    def test_saetze_vollstaendig(self):
        erde = sorted(os.listdir(os.path.join(ORDNER, "DucErde")))
        self.assertEqual(len(erde), 44)
        self.assertIn("neutral.webp", erde)
        for look in LOOKS:                                   # jede Jacke hat dieselben Posen
            self.assertEqual(sorted(os.listdir(os.path.join(ORDNER, "Duc" + look))), erde, look)

    def test_auswahl(self):
        z = durchlauf()
        self.assertIn("/charakterbild/gefuehle/DucErde/sadness?v=", E.duc_bild(z, "sadness"))
        self.assertIn("/DucErde/love?v=", E.duc_bild(z, "desire"))          # Ersatz fuer Gefuehle ohne Duc-Bild
        self.assertIn("/DucErde/fear?v=", E.duc_bild(z, "fear_3"))          # Variante ohne eigenes Bild
        self.assertIn("/DucErde/neutral?v=", E.duc_bild(z, "unbekannt"))
        self.assertTrue(E.duc_bild(z).startswith("/charakterbild/DucErde"))  # ohne Gefuehl: Charakterbild mit Waffe


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1, warnings="ignore")

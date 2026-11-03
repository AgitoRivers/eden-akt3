# -*- coding: utf-8 -*-
"""Audio-Index (30.10.2026): parallele Vertonungslaeufe verlieren keine Eintraege, ein voller Lauf entfernt nur ungueltige.

  python tests\\test_vertonen_index.py
"""
import importlib.util, json, os, subprocess, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
PFAD = os.path.join(os.path.dirname(HIER), "werkzeuge", "eden_rise", "vertonen_eden_rise.py")


def laden(index):
    spec = importlib.util.spec_from_file_location("vertonen_test", PFAD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.INDEX = index
    return m


def schreiber(index, name):
    m = laden(index)
    for i in range(40):
        m.index_aendern({"%s#%d" % (name, i): {"datei": "x.wav"}})


def main():
    if len(sys.argv) == 3:
        schreiber(sys.argv[1], sys.argv[2])
        return
    with tempfile.TemporaryDirectory() as tmp:
        index = os.path.join(tmp, "audio_index.json")
        json.dump({"alt#z0": {"datei": "a.wav"}}, open(index, "w", encoding="utf-8"))
        laeufe = [subprocess.Popen([sys.executable, os.path.abspath(__file__), index, n]) for n in ("a", "b", "c")]
        for p in laeufe:
            assert p.wait() == 0, "Schreiber abgestuerzt"
        d = json.load(open(index, encoding="utf-8"))
        assert len(d) == 121, len(d)
        assert not os.path.exists(index + ".lock"), "Sperre bleibt liegen"
        print("OK drei parallele Laeufe, alle Eintraege da")
        m = laden(index)
        d = m.index_aendern(weg=["a#0"])
        assert "a#0" not in d and len(d) == 120
        print("OK einzelne Eintraege entfernen")
        d = m.index_aendern(gueltig={"alt#z0", "b#1"})
        assert set(d) == {"alt#z0", "b#1"}
        print("OK voller Lauf behaelt nur gueltige Saetze")


if __name__ == "__main__":
    main()

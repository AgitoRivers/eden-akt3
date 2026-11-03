# -*- coding: utf-8 -*-
r"""Messung Anhoerung (Duc 28.10.2026): Der Test-Bot (tests/lauf_test.py) spielt die Woche bis zur Anhoerung, je Fall
und Seed. Ausgabe nur Zahlen: welche Punkte (What/Who/Why) vor der Anhoerung belegt sind und wie viele Notizen der Bot
hat - spoilerfrei. Laeuft in einem Wegwerf-Ordner, fasst keinen Spielstand an.

  python werkzeuge\eden_rise\anhoerung_messung.py                 Faelle 1-5, Seeds 7 und 3
  python werkzeuge\eden_rise\anhoerung_messung.py --seeds 7,3,11
Fuer "vorher" dasselbe Skript in einem Worktree auf dem alten Stand starten.
"""
import os, subprocess, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.environ.get("PYTHONHASHSEED") != "0":
    sys.exit(subprocess.call([sys.executable] + sys.argv, env=dict(os.environ, PYTHONHASHSEED="0")))
sys.path.insert(0, os.path.join(BASE, "tests"))
import lauf_test as L  # noqa: E402

E = L.eden
KURZ = {"handlung": "What", "person": "Who", "folge": "Why"}


def woche(nr, seed):
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_mess_"))
    L.random.seed(seed)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    z["wahrheit"] = "fall_%d" % nr
    E.sichern(z)
    for _ in range(3000):
        if z["status"] == "verhandlung" or z["tag"] >= 7 and z["status"] == "szene":
            break
        a = L.schritt(z, prot)
        if a is None:
            break
        if a[0] == "_tagesarbeit":
            L.tagesarbeit(z, prot)
        else:
            L.versuch(a, prot)
        z = E.aktiv()
    st = {g["id"]: g["belegt"] for g in E.ermittlung.glieder_status(z)}
    return st, len(E.ermittlung.stand(z)["bekannt"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    seeds = [int(s) for s in (sys.argv[sys.argv.index("--seeds") + 1] if "--seeds" in sys.argv else "7,3").split(",")]
    summe = {k: 0 for k in KURZ}
    n = 0
    for nr in range(1, 6):
        for seed in seeds:
            st, notizen = woche(nr, seed)
            n += 1
            for k in KURZ:
                summe[k] += bool(st.get(k))
            print("Fall %d Seed %d: %s · %d Notizen" % (nr, seed, " ".join("%s %s" % (KURZ[k], "✓" if st.get(k) else "–")
                                                                         for k in KURZ), notizen), flush=True)
    print("Belegt vor der Anhoerung (%d Laeufe): %s" % (n, ", ".join("%s %d/%d" % (KURZ[k], summe[k], n) for k in KURZ)))


if __name__ == "__main__":
    main()

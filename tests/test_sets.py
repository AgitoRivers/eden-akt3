# -*- coding: utf-8 -*-
"""Set-Namen (25.10.2026): Jeder Set-Name, den Events, set_standard oder set_regeln verlangen, muss bei der Figur einen
Sprite-Ordner finden - direkt oder ueber personen.<pid>.set_alias (kern/buehne.SetListe). Faellt auf, sobald ein Set in
SillyTavern umbenannt wird. Figuren ganz ohne Sprites werden nur gemeldet, nicht als Fehler gezaehlt.

  python tests\\test_sets.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
B = E.buehne


def main():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_sets_"))
    modul = E.modul_laden()
    moddir = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
    ev = json.load(open(os.path.join(moddir, "ereignisse.json"), encoding="utf-8"))["events"]
    verlangt = {}
    for e in ev:
        for pid, s in e.get("sets", {}).items():
            verlangt.setdefault(pid, {}).setdefault(s, []).append(e["id"])
    for pid, p in modul["personen"].items():
        if p.get("set_standard"):
            verlangt.setdefault(pid, {}).setdefault(p["set_standard"], []).append("set_standard")
        for r in p.get("set_regeln", []):
            verlangt.setdefault(pid, {}).setdefault(r["set"], []).append("set_regeln")
    fehler, ohne = [], []
    for pid, namen in sorted(verlangt.items()):
        if pid not in modul["personen"]:
            continue
        vorhanden = B.sets(E.cfg(), modul, pid)
        if not vorhanden:
            ohne.append(pid)
            continue
        norm = lambda x: x.lower().replace(" ", "_").replace("'", "")     # wie eden.event_sprite
        for name, wo in sorted(namen.items()):
            if name not in vorhanden and not any(norm(v) in (norm(name), "%s_%s" % (pid, norm(name))) for v in vorhanden):
                fehler.append("%s: Set %r fehlt (%d x, z. B. %s) - vorhanden: %s"
                              % (pid, name, len(wo), wo[0], ", ".join(vorhanden)))
    # Alias nur beim Nachschlagen, nie beim Aufzaehlen
    rosi = B.sets(E.cfg(), modul, "rosi")
    assert "Engine Room" in rosi and rosi["Engine Room"] is rosi.get("Engine Room"), "Alias Engine Room"
    assert "Engine Room" not in list(rosi), "Alias darf nicht in der Aufzaehlung stehen"
    print("OK Alias: Rosi 'Engine Room' -> %s" % rosi.alias["Engine Room"])
    if ohne:
        print("HINWEIS ohne Sprites:", ", ".join(ohne))
    for f in fehler:
        print("FEHLER", f)
    if fehler:
        sys.exit(1)
    print("OK alle verlangten Sets gefunden (%d Figuren)" % (len(verlangt) - len(ohne)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

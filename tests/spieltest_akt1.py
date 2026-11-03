# -*- coding: utf-8 -*-
r"""Spieltest Akt 1 (25.10.2026): mehrere Bot-Durchlaeufe wie tests/lauf_test.py, aber mit Blick der Spielerin.

Nach jedem Schritt wird die Ansicht (GET /api/stand) ausgewertet: Event-Titel, Szenen, Handy, Ablehnungen,
fehlende Bilder/Sprites, deutscher Resttext, Fehler. Ausgabe: docs/brain_trust/SPIELTEST_AKT1.md (+ JSON-Rohdaten).

  python tests\spieltest_akt1.py [--seeds 1 2 3 4 5 6]
"""
import argparse, collections, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
DE = re.compile(r"[äöüßÄÖÜ]|\b(und|der|die|das|nicht|ist|eine|mit|auf|für|ich|du|wir|noch|auch|wird|hat|zu|im|"
                r"den|dem|des|dich|dir|heute|morgen|kein|keine|Tag|Uhr)\b")
NAMEN_OK = re.compile(r"Totò|Cala d'Orsu|Jessas|Na geh|Grüß|Fröhlich")      # erlaubte Eigennamen mit Umlaut


def texte(x, pfad=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from texte(v, pfad + "/" + str(k))
    elif isinstance(x, list):
        for v in x:
            yield from texte(v, pfad + "[]")
    elif isinstance(x, str):
        yield pfad, x


def lauf(seed, modul="eden_rise"):
    import tempfile, shutil, random
    ordner = tempfile.mkdtemp(prefix="eden_spieltest_")
    tage = collections.defaultdict(lambda: {"events": [], "szenen": [], "jobs": 0, "abgelehnt": [], "kaempfe": 0})
    befund = {"deutsch": collections.Counter(), "ohne_bild": collections.Counter(), "fehler": [], "fall": None,
              "ende": None, "schritte": 0, "anhoerung": None}
    try:
        L.vorbereiten(modul, ordner, seed)
        random.seed(seed)
        prot = {"schritte": [], "erledigt": {}}
        z = E.aktion("neu", {"modus": "ironman"})
        gesehen = set()
        for _ in range(L.MAX_SCHRITTE):
            a = L.schritt(z, prot)
            if a is None:
                break
            vor = len(prot["schritte"])
            try:
                if a[0] == "_tagesarbeit":
                    L.tagesarbeit(z, prot)
                else:
                    L.versuch(a, prot)
            except Exception as ex:                       # echte Abstuerze
                befund["fehler"].append("Tag %s %s: %r" % (z.get("tag"), a[0], ex))
                break
            z = E.aktiv()
            befund["schritte"] += 1
            t = tage[z["tag"]]
            for s in prot["schritte"][vor:]:
                if len(s) > 2 and s[2] == "abgelehnt":
                    t["abgelehnt"].append("%s %s: %s" % (s[0], s[1], s[3][:80]))
                if s[0] == "job" and len(s) > 4 and s[2] != "abgelehnt":
                    t["jobs"] += 1
            v = E.ansicht(z)
            ev = z.get("event") or {}
            if ev.get("id") and (z["tag"], ev["id"]) not in gesehen:
                gesehen.add((z["tag"], ev["id"]))
                t["events"].append("%s/%s" % (z["phase"], ev["id"]))
            sz = z.get("szene") or {}
            if sz.get("def", {}).get("id") and (z["tag"], sz["def"]["id"]) not in gesehen:
                gesehen.add((z["tag"], sz["def"]["id"]))
                t["szenen"].append("%s/%s" % (z["phase"], sz["def"].get("titel") or sz["def"]["id"]))
            if z["status"] == "kampf" and ("k", z["tag"], z["phase"]) not in gesehen:
                gesehen.add(("k", z["tag"], z["phase"]))
                t["kaempfe"] += 1
            for p, s in texte(v):
                if len(s) > 5 and " " in s and DE.search(NAMEN_OK.sub("", s)) and not s.startswith(("/", "http")):
                    befund["deutsch"][(p.split("/")[-1] or p)[:30] + " | " + s[:90]] += 1
                if p.endswith(("/bild", "/sprite", "/hintergrund")) and s in ("", None):
                    befund["ohne_bild"][p] += 1
            for p, s in [(p, s) for p, s in _none_bilder(v)]:
                befund["ohne_bild"][p] += 1
        befund["ende"] = {"tag": z["tag"], "status": z["status"]}
        erm = z.get("ermittlung") or {}
        befund["anhoerung"] = {k: erm.get("anhoerung", {}).get(k) for k in ("gespielt", "angeklagt", "urteil")} \
            if erm.get("anhoerung") else None
        return dict(seed=seed, tage={k: v for k, v in sorted(tage.items())},
                    befund=dict(befund, deutsch=befund["deutsch"].most_common(40),
                                ohne_bild=befund["ohne_bild"].most_common(20)))
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


def _none_bilder(x, pfad=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ("bild", "sprite", "hintergrund", "avatar") and v is None:
                yield pfad + "/" + k, None
            else:
                yield from _none_bilder(v, pfad + "/" + str(k))
    elif isinstance(x, list):
        for v in x:
            yield from _none_bilder(v, pfad + "[]")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[1, 2, 3, 4, 5, 6])
    a = ap.parse_args()
    roh = [lauf(s) for s in a.seeds]
    ziel = os.path.join(os.path.dirname(HIER), "docs", "brain_trust", "spieltest_akt1_roh.json")
    json.dump(roh, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    for r in roh:
        b = r["befund"]
        print("Seed %d: %d Schritte, Ende Tag %s/%s, Fehler %d, deutsch %d, ohne Bild %d, Anhörung %s" % (
            r["seed"], b["schritte"], b["ende"]["tag"], b["ende"]["status"], len(b["fehler"]), len(b["deutsch"]),
            len(b["ohne_bild"]), b["anhoerung"]))
    print("roh:", ziel)


if __name__ == "__main__":
    main()

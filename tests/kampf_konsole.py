# -*- coding: utf-8 -*-
"""Test fight in the terminal (stage 4a, 24.10.2026): real dice, parade by typing (or the simulation's "Normal" odds).
Throwaway state from modul.json - no save game is read or written. Test switch: level, skills, weapon, armor.

  python tests\\kampf_konsole.py                                         hafen_dieb_test, medkit
  python tests\\kampf_konsole.py akt1_fackelpirat --level 7 --skills M3,M5,M7 --waffe sword --ruestung jacket_fire
  python tests\\kampf_konsole.py --items verbandskasten                  with these items (empty: --items "")
"""
import argparse, json, os, random, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, EDEN)
from kern import kampf, zustand  # noqa: E402

MODDIR = os.path.join(EDEN, "module", "eden_rise")
ATTR = kampf.ATTR_LABEL
NORMAL = {"leicht": (0.35, 0.45), "mittel": (0.25, 0.45), "stark": (0.15, 0.40)}


def balken(wert, max_wert, breite=12):
    n = round(breite * wert / max_wert) if max_wert else 0
    return "█" * n + "·" * (breite - n)


def zeile(name, lp, lp_max, rest):
    return "  %-18s ❤ %s %3d/%d   %s" % (name[:18], balken(lp, lp_max), lp, lp_max, rest)


def chips(xs):
    return ", ".join("%s%s" % (c["label"], " ×%d" % c["wert"] if c["id"] == "brennend" else "") for c in xs)


def zeigen(a):
    sp, g = a["spieler"], a["gegner"][0]
    print()
    print("Runde %d · Ziel: %s" % (a["runde"], a["ziel"]))
    print(zeile("Duc Lv %d" % sp["level"], sp["lp"], sp["lp_max"], "⚡ %d/%d · Treffer %d · Krit %d %%%s" % (
        sp["ausdauer"], sp["ausdauer_max"], sp["angriff"], sp["krit"],
        "   (" + chips(sp["zustaende"]) + ")" if sp["zustaende"] else "")))
    marken = chips(g["zustaende"])
    if g["schwaeche"]:
        marken = (marken + ", " if marken else "") + "Schwäche: " + ATTR.get(g["schwaeche"], g["schwaeche"])
    print(zeile("%s Lv %d" % (g["name"], g["level"]), g["lp"], g["lp_max"], "🜂 Fassung %d/%d · %s%s" % (
        g["fassung"], g["fassung_max"], g["bedrohung"]["label"], "   (" + marken + ")" if marken else "")))
    ab = g["absicht"]
    weh = "" if not ab.get("sa") else (" – Spezialangriff, tut weh" if ab.get("tut_weh") else " – Spezialangriff, harmlos")
    print("  Absicht: %s %s%s%s" % (ab["icon"], ab["text"], " (stark)" if ab.get("stark") else "", weh))


def menue(eintraege):
    """eintraege = [(label, gesperrt)] -> index or None (back/invalid)."""
    for i, (label, gesperrt) in enumerate(eintraege, 1):
        print("  [%d] %s%s" % (i, label, "   – " + gesperrt if gesperrt else ""))
    w = input("> ").strip().lower()
    if w in ("q", "quit", "x"):
        sys.exit(0)
    if w.isdigit() and 1 <= int(w) <= len(eintraege):
        return int(w) - 1
    return None


def faehigkeit_label(f):
    teile = ["%d ⚡" % f["kosten"]]
    if f["probe"] and f["chance"] is None:
        teile.append("immun")
    elif f["probe"]:
        teile.append("%s-Probe %+d gegen SG %d, %d %%%s" % (ATTR.get(f["attribut"], f["attribut"]), f["wert"], f["sg"],
                                                         f["chance"], ", Vorteil" if f["vorteil"] else ""))
    else:
        teile.append("sicher")
    kopf = "%s %s" % (f["kuerzel"], f["label"]) if f.get("kuerzel") else f["label"]
    return "%s (%s) – %s%s" % (kopf, ", ".join(teile), f["text"], "  [" + f["hinweis"] + "]" if f.get("hinweis") else "")


def parade_fragen(k, rng):
    p = k["parade"]
    print("  ⚔ %s holt aus: %s%s – %s Schaden ohne Parade." % (k["gegner"][0]["name"], p["label"],
                                                                 " (stark)" if p["schwer"] else "", p["schaden"]))
    erlaubt = ["a", "v"] if p["nur_ausweichen"] else (["p", "g", "a", "v"] if p["modus"] == "ring" else ["p", "g", "v"])
    w = input("  Parade %s, Enter = würfeln nach Normal-Quoten > " % "/".join(erlaubt)).strip().lower()
    if w in erlaubt:
        return {"p": "perfekt", "g": "gut", "a": "ausweichen", "v": "verfehlt"}[w]
    perf, good = NORMAL[p["tempo"]]
    f = p["fenster"]["faktor"]
    perf, good = min(0.95, perf * f), min(0.95, good * f)
    r = rng.random()
    if p["nur_ausweichen"]:
        return "ausweichen" if r < perf + good else "verfehlt"
    return "perfekt" if r < perf else "gut" if r < perf + good else "verfehlt"


def drucken(z, ab):
    for t in [t for e in z["kampf"]["log"][ab:] for t in e["zeilen"]]:
        print("  · " + t)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("begegnung", nargs="?", default="hafen_dieb_test")
    ap.add_argument("--items", default="verbandskasten")
    ap.add_argument("--level", type=int)
    ap.add_argument("--skills", default=None, help="z. B. K3,K5,M3 (Arbeitskürzel oder Code-IDs)")
    ap.add_argument("--waffe")
    ap.add_argument("--ruestung")
    args = ap.parse_args()
    modul = json.load(open(os.path.join(MODDIR, "modul.json"), encoding="utf-8"))
    defs = kampf.daten(MODDIR)
    z = zustand.neu(modul)
    zustand.persona_setzen(z, modul, modul["personas"][0])
    z["inventar"] = [i for i in args.items.split(",") if i in modul["items"]]
    kampf.test_setup(z, defs, level=args.level, weapon=args.waffe, armor=args.ruestung,
                     skills=kampf.by_code(defs, args.skills.split(",")) if args.skills is not None else None)
    rng = random.Random()
    k = kampf.starten(z, defs, args.begegnung)
    sp = k["spieler"]
    print("=== %s ===" % k["def"]["title"])
    print("Duc Lv %d · %s · Waffe %s · Rüstung %s · Skills: %s" % (
        sp["level"], kampf.PATH_NAME.get(sp["main_path"], "kein Hauptpfad"), sp["weapon"]["label"],
        (sp["armor"] or {}).get("label", "keine"), ", ".join(defs["specials"][s]["code"] for s in sp["skills"]) or "keine"))
    print("Attribute: %s" % ", ".join("%s %d" % (ATTR[a], v) for a, v in sp["attrs"].items() if a in ATTR))
    print("Inventar: %s   (q = beenden)" % (", ".join(modul["items"][i]["label"] for i in z["inventar"]) or "leer"))
    drucken(z, 0)
    while not z["kampf"]["ergebnis"]:
        a = kampf.ansicht(z, modul)
        zeigen(a)
        i = menue([(b["label"], b["gesperrt"]) for b in a["befehle"]])
        if i is None:
            continue
        befehl, ziel = a["befehle"][i]["id"], None
        if befehl == "faehigkeit":
            fs = a["faehigkeiten"]
            j = menue([(faehigkeit_label(f), f["gesperrt"]) for f in fs] + [("Zurück", None)])
            if j is None or j == len(fs):
                continue
            ziel = fs[j]["id"]
        elif befehl == "gegenstand":
            gs = a["gegenstaende"]
            j = menue([("%s (heilt %d)" % (g["label"], g["heilen"]), g["gesperrt"]) for g in gs] + [("Zurück", None)])
            if j is None or j == len(gs):
                continue
            ziel = gs[j]["id"]
        try:
            vorher = len(z["kampf"]["log"])
            kampf.zug(z, modul, befehl, ziel, revision=a["revision"])
            drucken(z, vorher)
            if z["kampf"]["phase"] == "parade":
                vorher = len(z["kampf"]["log"])
                kampf.parade_aufloesen(z, modul, parade_fragen(z["kampf"], rng))
                drucken(z, vorher)
        except ValueError as e:
            print("  ✗ %s" % e)
    e = z["kampf"]["ergebnis"]
    titel = {"ko": "SIEG (k.o.)", "aufgabe": "SIEG (Aufgabe)", "entkommen": "ENTKOMMEN", "flucht": "FLUCHT",
             "niederlage": "NIEDERLAGE"}[e["art"]]
    print()
    print("=== %s nach %d Runden ===" % (titel, z["kampf"]["runde"]))
    print(e["text"])
    print("Duc: ❤ %d/%d · Level %d · %d Skillpunkte frei" % (z["lp"], kampf.max_lp(e["level"]), e["level"], e["skillpunkte"]))
    print("Folgen (nur Test, nichts gespeichert): %s" % (", ".join(e["zeilen"]) or "-"))


if __name__ == "__main__":
    main()

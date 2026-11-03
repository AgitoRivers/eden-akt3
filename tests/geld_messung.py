# -*- coding: utf-8 -*-
r"""Geld-Messung (18.10.2026, erweitert 29.10.2026): Kontostand je Tag ueber viele Durchlaeufe, fuer vier Spielstile.

  sparsam  = der Bot aus lauf_test.py (kauft je Laden nur das Billigste)
  normal   = gibt aus wie ein Spieler, der mitspielt: Diesel, wenn er knapp wird; zwei Geschenke am Tag fuer die
             Frauen, die ihm am naechsten sind (am liebsten, was sie lieben); ein Snack; einmal einen Gluecksbringer
             und einmal einen Attribut-Gegenstand, sobald Luft ist (Preis + 100 Puffer)
  kaeufer  = normal + kauft ab Tag 8 Rosis Ausbau (Jacke, Waffe: Stufe 1, dann 2) und die Tasche, je eins am Tag, sobald
             das Geld reicht - als Buchung modelliert, Material wird nicht geprueft (Obergrenze dessen, was man ausgeben kann)

  python tests\geld_messung.py [--seeds 12]

Ausgabe nur Zahlen (Kontostand, Einnahmen, Ausgaben je Art) - nichts aus der Story.
"""
import collections, os, statistics, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402  (Stubs, fester Hash-Seed, Bot)

PUFFER = 100
MESSUNG = {}
# Kaeufer (29.10.2026): Rosi 150/400 je Stueck (kaempfe.json werkstatt), Tasche Rosi's Diving Bag 400 (beute.md 5)
KAUFLISTE = [("Rosi Jacke 1", 150), ("Rosi Waffe 1", 150), ("Tasche Akt 2", 400), ("Rosi Jacke 2", 400), ("Rosi Waffe 2", 400)]


def kaufe(z, laden, iid, protokoll, art):
    vorher = z["konto"]
    L.versuch(("kaufen", {"laden": laden, "id": iid}), protokoll)
    z2 = L.eden.aktiv()
    if z2["konto"] < vorher:
        MESSUNG["ausgaben"][art] += vorher - z2["konto"]
    return z2


def tagesarbeit_normal(z, protokoll):
    modul = L.eden.modul_laden()
    h = L.eden.handel
    h.init(z, modul)
    MESSUNG["morgen"][z["tag"]] = z["konto"]
    blick = {k: h.sortiment(z, modul, k) or [] for k in sorted(modul.get("laeden") or {})}
    if "erschwinglich" not in MESSUNG:          # erster Blick in die Laeden: was kann man sich leisten?
        alle = [w["preis"] for v in blick.values() for w in v]
        MESSUNG["erschwinglich"] = (sum(1 for p in alle if p <= z["konto"]), len(alle), z["konto"], z["tag"])
    ware = [(k, w) for k, v in blick.items() for w in v]
    # Diesel, wenn er knapp wird
    if z["werte"].get("diesel", 0) <= 1:
        d = sorted((w["preis"], k, w["id"]) for k, w in ware if w["id"] == "diesel_canister")
        if d and d[0][0] <= z["konto"]:
            z = kaufe(z, d[0][1], d[0][2], protokoll, "Diesel")
    # zwei Geschenke fuer die Naechsten
    frauen = sorted(L.eden.hauptstory.frauen(modul), key=lambda p: -(z["werte"].get("vertrauen." + p, 0)
                                                                     + z["werte"].get("begehren." + p, 0)))[:2]
    for p in frauen:
        kand = [(-(modul["items"][w["id"]].get("geschenk") or {}).get(p, 0), w["preis"], k, w["id"]) for k, w in ware
                if w["art"] == "geschenk" and not w["im_inventar"] and not w.get("intim")
                and (modul["items"][w["id"]].get("geschenk") or {}).get(p, 0) >= 1 and w["preis"] <= z["konto"]]
        if kand and h.platz_frei(z, modul):
            _, _, k, iid = sorted(kand)[0]
            z = kaufe(z, k, iid, protokoll, "Geschenke")
    # ein Snack
    s = sorted((w["preis"], k, w["id"]) for k, w in ware if w["art"] == "snack")
    if s and s[0][0] <= z["konto"]:
        z = kaufe(z, s[0][1], s[0][2], protokoll, "Snacks")
    # einmal Gluecksbringer, einmal Attribut - wenn Luft ist
    for art, schl in (("gluecksbringer", "Gluecksbringer"), ("attribut", "Attribut"), ("werkzeug", "Werkzeug")):
        if schl in MESSUNG["einmal"]:
            continue
        g = sorted((w["preis"], k, w["id"]) for k, w in ware if w["art"] == art and not w["im_inventar"])
        if g and g[0][0] + PUFFER <= z["konto"] and h.platz_frei(z, modul):
            MESSUNG["einmal"].add(schl)
            z = kaufe(z, g[0][1], g[0][2], protokoll, schl)
    # Teile fuer offene Auftraege (Missionsausbau 18.10.2026): wer Besorgungen macht, kauft sie
    for k, w in ware:
        if w["art"] == "teil" and w["preis"] + PUFFER <= z["konto"] and len(h.tasche(z)) < h.TASCHE_PLAETZE:
            z = kaufe(z, k, w["id"], protokoll, "Teile")
    V = L.eden.showrunner.vorrat(L.eden.moddir())
    for j in h.jobs_heute(z, modul, V):
        L.versuch(("job", {"id": j["id"]}), protokoll)
    gerichte = h.gerichte(z, modul)
    if gerichte:
        L.versuch(("kochen", {"id": gerichte[z["tag"] % len(gerichte)]["id"], "fuer": "crew"}), protokoll)


def tagesarbeit_kaeufer(z, protokoll):
    tagesarbeit_normal(z, protokoll)
    z = L.eden.aktiv()
    if z["tag"] >= 8:
        offen = [x for x in KAUFLISTE if x[0] not in MESSUNG["einmal"]]
        if offen and z["konto"] >= offen[0][1]:
            name, preis = offen[0]
            MESSUNG["einmal"].add(name)
            MESSUNG.setdefault("gekauft_am", {})[name] = z["tag"]
            L.eden.handel.buchen(z, -preis, name)
            MESSUNG["ausgaben"]["Ausbau/Tasche"] += preis
            L.eden.sichern(z)


def tagesarbeit_sparsam(z, protokoll):
    MESSUNG["morgen"][z["tag"]] = z["konto"]
    if "erschwinglich" not in MESSUNG:
        modul = L.eden.modul_laden()
        L.eden.handel.init(z, modul)
        alle = [w["preis"] for k in modul.get("laeden") or {} for w in (L.eden.handel.sortiment(z, modul, k) or [])]
        MESSUNG["erschwinglich"] = (sum(1 for p in alle if p <= z["konto"]), len(alle), z["konto"], z["tag"])
    _ALT(z, protokoll)


_ALT = L.tagesarbeit


def messen(stil, seed):
    MESSUNG.clear()
    MESSUNG.update(morgen={}, ausgaben=collections.Counter(), einmal=set())
    L.tagesarbeit = {"normal": tagesarbeit_normal, "kaeufer": tagesarbeit_kaeufer}.get(
        stil, tagesarbeit_sparsam)
    import json
    gage = (json.load(open(os.path.join(os.path.dirname(HIER), "module", "eden_rise", "modul.json"), encoding="utf-8"))
            .get("geld") or {}).get("honorar_text", "Tagesgage")
    erg = L.laufen("eden_rise", seed)
    ein = collections.Counter()
    for b in erg["ende"]["buchungen"]:
        if b["betrag"] > 0:
            k = b["text"].split(":")[0]
            ein["Gage" if (k == gage or "Tagesgage" in k) else "Start" if k == "Startguthaben" else "Verkauf" if k.startswith("an ")
                else "Kampf" if k.endswith("wallet") else "Missionen/Events"] += b["betrag"]
    if stil == "sparsam":
        for b in erg["ende"]["buchungen"]:
            if b["betrag"] < 0:
                MESSUNG["ausgaben"]["Billigstes"] -= b["betrag"]
    return dict(MESSUNG, ende=erg["ende"]["konto"], einnahmen=ein)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    n = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 12
    for stil in ("sparsam", "normal", "kaeufer"):
        lauf = [messen(stil, s) for s in range(1, n + 1)]
        tage = sorted({t for r in lauf for t in r["morgen"]})
        print("\n== %s (%d Durchlaeufe, Median)" % (stil, n))
        print("Kontostand morgens: " + "  ".join("T%d %d €" % (t, statistics.median(r["morgen"][t] for r in lauf
                                                                                     if t in r["morgen"])) for t in tage))
        print("Endstand: Median %d €, min %d, max %d" % (statistics.median(r["ende"] for r in lauf),
                                                         min(r["ende"] for r in lauf), max(r["ende"] for r in lauf)))
        for titel, feld in (("Einnahmen", "einnahmen"), ("Ausgaben", "ausgaben")):
            arten = sorted({k for r in lauf for k in r[feld]})
            print("%s: %s" % (titel, ", ".join("%s %d €" % (a, statistics.median(r[feld].get(a, 0) for r in lauf))
                                                for a in arten)))
        if stil == "kaeufer":
            for name, _ in KAUFLISTE:
                tage_k = [r.get("gekauft_am", {}).get(name) for r in lauf]
                da = [t for t in tage_k if t]
                print("  %s: in %d von %d Laeufen, Median Tag %s" % (name, len(da), n, statistics.median(da) if da else "-"))
        e = lauf[0]["erschwinglich"]
        print("Erster Ladenblick (Tag %d, Konto %d €): %d von %d Artikeln bezahlbar" % (e[3], e[2], e[0], e[1]))


if __name__ == "__main__":
    main()

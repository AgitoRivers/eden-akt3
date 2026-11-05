# -*- coding: utf-8 -*-
r"""Akt 3, Mina (kern/post.py, werkzeuge/eden_rise/ereignisse_akt3_mina.py, Mina-Dossier 05.11.2026):
Minas Fahrt nach Bastia (Wahl aus drei, keine Phase, Mina waehlt selbst, nie Stahl, Vespa verdoppelt) und die Szene
"Second Gear" (Rosi oder Petru, setzt mina_vespa_heil und a3_post_bastia, Turbo-Tags, Frage vor den Chips).

  python tests/test_akt3_mina.py
"""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import aufbau, kuechen, post  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
EV = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}
TAGS = json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))
TURBO = re.compile(r"\[(laugh|chuckle|sigh|gasp|cough|clear throat|sniff|shush)\]")


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def z_neu(tag=25, *flags):
    return {"id": "test", "tag": tag, "flags": ["akt2_ende", "buenaventura_schwur"] + list(flags),
            "kueche": {"vorrat": {}, "rohstoffe": {"timber": 10, "slate": 0, "cork": 0, "iron": 0, "granite": 0, "steel": 0}}}


def nacht(z):
    """Wie eden.py am Tagesende: neuer Tag, dann die Lieferung."""
    z["tag"] += 1
    return post.morgen(z)


def mechanik():
    z = z_neu(25, "tk_haus_weg_batu")
    pruefen(not post.offen(z) and post.ansicht(z) is None, "ohne Post (abgebrannt, nicht aufgebaut) keine Fahrt nach Bastia")
    pruefen(not post.offen({"tag": 25, "flags": ["aufbau_fertig_post"]}), "vor dem Cliffhanger keine Fahrt")
    z["flags"].append("aufbau_fertig_post")
    pruefen(post.offen(z), "nach dem Wiederaufbau der Post bestellt Duc ab Tag 25")
    pruefen(post.offen(z_neu(25, "a3_post_bastia")), "Post nie abgebrannt: Second Gear oeffnet die Fahrt")
    a = post.ansicht(z)
    pruefen([w["id"] for w in a["wahl"]] == ["bau", "kueche", "mina"], "Wahl aus drei: Baustoff, Zutat, Minas Wahl")

    # Duc waehlt nichts: Mina bringt, was an der Baustelle fehlt (Ba Tus Laden, Stufe 1: 3 Timber, 2 Granite)
    aufbau.beginnen(z, "batu")
    pruefen(post._fehlt(z) == "granite", "Mina weiss, was fehlt: Granite fuer Ba Tus Laden")
    zl = nacht(z)
    pruefen(kuechen.rohstoffe(z)["granite"] == 1 and zl and "brought it anyway" in zl[0], "ohne Bestellung kommt 1 Granite, Mina sagt es")

    # Bestellung Zutat, mit reparierter Vespa doppelt
    z["flags"].append(post.VESPA)
    post.bestellen(z, "kueche")
    pruefen(post.ansicht(z)["bestellt"] == "kueche", "Bestellung steht im Kreis")
    zt = post._zutat(z)
    nacht(z)
    pruefen(kuechen.vorrat_menge(z, zt) == 2, "Vespa heil: zwei Stueck %s kommen am Morgen" % zt)
    pruefen(post.ansicht(z)["bestellt"] is None, "nach der Lieferung ist die Bestellung leer")

    post.bestellen(z, "bau")
    vor = kuechen.rohstoffe(z)["granite"]
    nacht(z)
    pruefen(kuechen.rohstoffe(z)["granite"] == vor + 2, "Baustoff mit Vespa: zwei Granite")

    # Minas Wahl: Ueberraschung, immer etwas, nie Stahl
    for _ in range(4):
        if not post.offen(z):
            break
        post.bestellen(z, "mina")
        roh, vorrat = dict(kuechen.rohstoffe(z)), kuechen.vorrat_menge(z)
        zl = nacht(z)
        pruefen(zl and (kuechen.rohstoffe(z) != roh or kuechen.vorrat_menge(z) > vorrat), "Minas Wahl bringt etwas (Tag %d)" % z["tag"])
    pruefen(kuechen.rohstoffe(z).get("steel", 0) == 0, "Stahl bringt Mina nie")

    # Grenzen: letzte Lieferung am Morgen von Tag 34, Bestellen nur bis Tag 33
    z2 = z_neu(33, "aufbau_fertig_post")
    pruefen(post.offen(z2), "Tag 33: bestellen geht noch")
    nacht(z2)
    pruefen(not post.offen(z2), "Tag 34 (vor der Kommission): keine neue Bestellung")
    z2["tag"] = 34
    pruefen(nacht(z2) == [], "Tag 35: keine Lieferung mehr")
    try:
        post.bestellen(z2, "bau")
        pruefen(False, "Bestellen ausserhalb der Tage muss scheitern")
    except ValueError:
        pruefen(True, "Bestellen ausserhalb der Tage scheitert sauber")


def szene():
    for eid, mit in (("a3_mina_vespa", "rosi"), ("a3_mina_vespa_petru", "petru")):
        e = EV.get(eid)
        pruefen(e is not None, "%s in ereignisse.json" % eid)
        sprecher = {zl["wer"] for zl in e["zeilen"]}
        pruefen({"mina", mit} <= sprecher, "%s: Mina und %s sprechen beide" % (eid, mit))
        pruefen(e["zeilen"][-1]["text"].rstrip().endswith("?"), "%s: klare Frage vor den Chips" % eid)
        alle = e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]
        gesprochen = {(t["wer"], t["text"]): t["gesprochen"] for t in TAGS["zeilen"]}
        pruefen(all((zl["wer"], zl["text"]) in gesprochen for zl in alle), "%s: alle Zeilen in stimme_tags.json" % eid)
        pruefen(all(TURBO.search(gesprochen[(zl["wer"], zl["text"])]) for zl in alle), "%s: jede gesprochene Zeile hat einen Turbo-Tag" % eid)
        pruefen(not any("[" in zl["text"] for zl in alle), "%s: keine Tags im Spieltext" % eid)
        pruefen(not any("[groan]" in g for g in gesprochen.values() if g), "kein [groan] in stimme_tags.json")
        for o in e["optionen"]:
            fl = {f.get("flag") for f in o["folgen"]}
            pruefen({post.VESPA, post.FLAG_AN} <= fl, "%s: jede Wahl repariert die Vespa (%s)" % (eid, o["text"][:30]))
        pruefen(e["ton"] == "wholesome" and e["wann"]["tage"] == [25, 30], "%s: wholesome, Pool Tag 25 bis 30" % eid)
        pruefen("–" not in json.dumps(e, ensure_ascii=False) and "—" not in json.dumps(e, ensure_ascii=False), "%s: keine Gedankenstriche" % eid)
    b1 = json.dumps(EV["a3_mina_vespa"]["wann"]["bedingung"])
    b2 = json.dumps(EV["a3_mina_vespa_petru"]["wann"]["bedingung"])
    pruefen('"gefeuert_rosi"' in b1 and '"nicht"' in b1 and '"gefeuert_rosi"' in b2, "Rosi-Fassung ohne Kuendigung, Petru-Fassung nach Rosis Kuendigung")
    pruefen(EV["a3_mina_vespa"]["sets"].get("rosi") == "Vespa Sunday", "Rosi traegt ihr Set Vespa Sunday")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    mechanik()
    szene()
    print("Alles gruen.")


if __name__ == "__main__":
    main()

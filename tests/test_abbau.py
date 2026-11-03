# -*- coding: utf-8 -*-
"""Abbauen an Rastplaetzen (28.10.2026): Quellen je Frame, Bestand und 3 Tage Nachwuchs, Werkzeugstufen (3/1/0 Treffer), Ertrag
mit Kork und Perfekt-Bonus, Ende zurueck an den Rastplatz, Petrus Werkstatt (Geld, Rohstoffe, Wunschfisch, Rosi + Vertrauen).

Laeuft ohne Modell, Stimme und Netz.

  python tests\\test_abbau.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import abbau, kuechen, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
D = kuechen.daten(MODUL)


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def fehler(fn, *a):
    try:
        fn(*a)
    except ValueError as e:
        return str(e)
    return None


def neues_spiel(sid="a1"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"], z["id"] = 9, "tag", "ereignis", sid
    z["persona"]["attribute"]["strength"] = 2
    return z


def quellen_pruefen():
    ev = {e["id"] for e in json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]
          if e.get("rast")}
    frames = [f for q in D["abbau"]["quellen"].values() for f in q["frames"]]
    pruefen(set(frames) <= ev, "jede Quelle hängt an einem echten Rastplatz (%d Frames)" % len(frames))
    pruefen(abbau.platz_von_frame(MODUL, "kl_schluchtfeuer_kalt") == abbau.platz_von_frame(MODUL, "kl_schluchtfeuer") == "kl_schlucht",
            "Tag- und Nacht-Frame teilen eine Quelle")
    z = neues_spiel()
    c = {x["art"]: x for x in abbau.quellen_ansicht(z, MODUL, "kl_bachufer")}
    pruefen(set(c) == {"holz", "wasser"} and c["holz"]["fehlt"] == "Axe" and c["holz"]["rest"] == 4 and not c["wasser"].get("fehlt"),
            "Bach: Holz (ohne Axt gesperrt) und Wasser")
    pruefen(c["holz"]["bild"] == "/farm/abbau/kreis_cork_oak.png" and c["wasser"]["bild"].startswith("/bg/eden_rise_angeln_")
            and os.path.isfile(os.path.join(EDEN, "module", "eden_rise", "farm", "abbau", "kreis_cork_oak.png")),
            "Kreis zeigt, was am Platz am meisten steht, bzw. das Angelbild")
    pruefen(abbau.quellen_ansicht(z, MODUL, "kl_kueche") == [], "Nonnas Küche hat keine Quelle")
    pruefen("kueche" not in z, "Lesen legt keine Schlüssel an")
    pruefen(fehler(abbau.starten, z, MODUL, "kl_bachufer", "holz") is not None, "ohne Axt kein Holz")


def abbau_pruefen():
    z = neues_spiel()
    kuechen.kueche(z)["werkzeug"] = {"axe": 1}
    pruefen(fehler(abbau.starten, z, MODUL, "kl_bachufer", "stein") is not None, "am Bach gibt es keinen Stein")
    abbau.starten(z, MODUL, "kl_bachufer", "holz")
    s = z["abbau"]
    pruefen(z["status"] == "abbau" and s["noetig"] == 3 and len(s["knoten"]) == 4, "Stufe 1: 3 Treffer je Baum, 4 Bäume")
    pruefen(set(s["knoten"]) <= {"cork_oak", "holm_oak"}, "nur Steineichen und Korkeichen")
    s["knoten"] = ["cork_oak", "holm_oak", "holm_oak", "cork_oak"]
    pruefen(not abbau.schlag(z, MODUL, "daneben")["fertig"] and s["fehl"] == 1 and s["treffer"] == 0, "daneben zählt nicht")
    abbau.schlag(z, MODUL, "gut")
    abbau.schlag(z, MODUL, "perfekt")
    r = abbau.schlag(z, MODUL, "perfekt")
    roh = kuechen.rohstoffe(z)
    pruefen(r["fertig"] and roh == {"cork": 3} and r["eintrag"]["perfekt"], "Korkeiche, perfekter Schluss: 3 Cork, kein Holz (der Baum bleibt stehen)")
    for _ in range(3):
        r = abbau.schlag(z, MODUL, "gut")
    pruefen(r["fertig"] and kuechen.rohstoffe(z)["timber"] == 3 and not r["eintrag"]["perfekt"], "Steineiche mit gutem Schluss: 3 Timber")
    pruefen(abbau.stand(z, MODUL, "kl_bachufer", "holz") == (2, None), "Bestand: noch 2 Bäume")
    v = abbau.ansicht(z, MODUL)
    pruefen(v["nr"] == 2 and len(v["geschafft"]) == 2 and v["knoten"][0]["sprite"] == "/farm/abbau/%s_vorher.png" % v["knoten"][0]["bild"]
            and v["knoten"][0]["sprite_nach"] == "/farm/abbau/%s.png?v=2" % v["knoten"][0]["bild"]    # Korkeiche: erst Rinde, dann geschaelt
            and v["knoten"][0]["sprite_rinde"] == "/farm/abbau/%s_rinde.png" % v["knoten"][0]["bild"]
            and v["ring"]["perfekt_ms"] == D["abbau"]["ring"]["perfekt_ms"], "Ansicht: Fortschritt, Sprites, Ring")
    kn = v["knoten"]
    pruefen(kn[1]["sprite"] != kn[2]["sprite"] and kn[0]["sprite"] != kn[3]["sprite"], "Gleiche Baumart nebeneinander: verschiedene Bilder")
    pruefen(abbau.ansicht(z, MODUL)["knoten"] == kn, "Bäume bleiben beim Neuladen dieselben")
    for t, nd in D["abbau"]["knoten"].items():
        for b in nd.get("bilder") or [t]:
            for datei in ([b + ".png", b + "_vorher.png", b + "_rinde.png"] if t == "cork_oak" else [b + ".png"]):
                pruefen(os.path.isfile(os.path.join(EDEN, "module", "eden_rise", "farm", "abbau", datei)), "Bild da: " + datei)
    zeilen = abbau.ende(z, MODUL)
    pruefen(z["status"] == "ereignis" and "abbau" not in z and "2 trees worked" in zeilen[0] and "+3 Cork" in zeilen[0],
            "Ende: zurück an den Rastplatz (%s)" % zeilen[0])
    # Rest abbauen, dann 3 Tage Pause
    kuechen.kueche(z)["werkzeug"]["axe"] = 3
    abbau.starten(z, MODUL, "kl_bachufer", "holz")
    pruefen(z["abbau"]["direkt"] and len(z["abbau"]["knoten"]) == 2, "Stufe 3 direkt, nur der Rest steht noch")
    pruefen(abbau.schlag(z, MODUL, "daneben")["fertig"], "Stufe 3: ein Klick fällt den Baum (zählt als perfekt)")
    abbau.schlag(z, MODUL, "gut")
    pruefen(fehler(abbau.schlag, z, MODUL, "gut") is not None, "nichts mehr da")
    abbau.ende(z, MODUL)
    pruefen(abbau.stand(z, MODUL, "kl_bachufer", "holz") == (0, 12), "leer: an Tag 12 wieder da")
    c = {x["art"]: x for x in abbau.quellen_ansicht(z, MODUL, "kl_bachufer")}
    pruefen(c["holz"]["in_tagen"] == 3 and c["wasser"]["rest"] == 4, "Chip: in 3 Tagen; das Wasser ist davon unberührt")
    pruefen(fehler(abbau.starten, z, MODUL, "kl_bachufer", "holz") is not None, "erschöpft: kein Start")
    z["tag"] = 12
    pruefen(abbau.stand(z, MODUL, "kl_bachufer", "holz") == (4, None), "nach 3 Tagen nachgewachsen")
    # Kraft verbreitert das Perfekt-Fenster
    z["persona"]["attribute"]["strength"] = 5
    kuechen.kueche(z)["werkzeug"]["pickaxe"] = 2
    pruefen(fehler(abbau.starten, z, MODUL, "kl_schluchtfeuer", "holz") is not None, "an der Schlucht gibt es kein Holz")
    abbau.starten(z, MODUL, "kl_schluchtfeuer", "stein")
    v = abbau.ansicht(z, MODUL)
    pruefen(v["noetig"] == 1 and v["ring"]["perfekt_ms"] == D["abbau"]["ring"]["perfekt_ms"] + 3 * D["abbau"]["ring"]["kraft_ms"],
            "Spitzhacke 2: 1 Treffer; Kraft 5 = breiteres Perfekt-Fenster")
    abbau.schlag(z, MODUL, "perfekt")
    pruefen(kuechen.rohstoffe(z).get("granite", 0) + kuechen.rohstoffe(z).get("slate", 0) == 3, "Fels mit perfektem Schlag: 3 Granit oder Schiefer")
    z["status"] = "wahl"
    pruefen(fehler(abbau.starten, z, MODUL, "kl_bachufer", "holz") is not None, "nicht aus der freien Wahl")


def petru_pruefen():
    z = neues_spiel()
    z["tag"] = 1
    pruefen(fehler(abbau.werkzeug_kaufen, z, MODUL, "axe") is not None, "Tag 1: Werkstatt noch zu")
    z["tag"], z["konto"] = 2, 100
    w = {x["id"]: x for x in abbau.werkzeug_ansicht(z, MODUL)}
    pruefen(w["axe"]["stufe"] == 0 and w["axe"]["naechste"]["geld"] == 40 and w["axe"]["naechste"]["geht"], "Stufe 1 kaufen: 40 €")
    zeilen, gruppe = abbau.werkzeug_kaufen(z, MODUL, "axe")
    pruefen(z["konto"] == 60 and abbau.werkzeug_stufe(z, "axe") == 1 and gruppe == "kauf_axe_1" and "three good blows" in zeilen[0],
            "Axt gekauft, Petru sagt seinen Satz")
    pruefen(gruppe in json.load(open(os.path.join(EDEN, "module", "eden_rise", "laeden.json"), encoding="utf-8"))["laeden"]["petru"]["zeilen"],
            "Übergabe-Zeile steht in laeden.json (wird vertont)")
    n = {x["id"]: x for x in abbau.werkzeug_ansicht(z, MODUL)}["axe"]["naechste"]
    pruefen(not n["geht"] and n["fisch"]["label"] == "Northern Pike" and not n["fisch"]["hast"], "Stufe 2 braucht einen Hecht")
    z["konto"] = 500
    kuechen.rohstoff_add(z, "iron", 2)
    kuechen.rohstoff_add(z, "timber", 4)
    pruefen("fish" in fehler(abbau.werkzeug_kaufen, z, MODUL, "axe"), "ohne Hecht kein Upgrade")
    kuechen.vorrat_add(z, "pike_roh", 3)
    kuechen.vorrat_add(z, "pike_roh", 2)
    abbau.werkzeug_kaufen(z, MODUL, "axe")
    pruefen(abbau.werkzeug_stufe(z, "axe") == 2 and kuechen.vorrat_menge(z, "pike_roh") == 1 and kuechen.vorrat_menge(z, "pike_roh", 3) == 1
            and kuechen.rohstoffe(z).get("iron") == 0 and z["konto"] == 380, "Stufe 2: Hecht (schlechtester zuerst), Eisen, Holz, 120 €")
    kuechen.rohstoff_add(z, "iron", 3)
    kuechen.rohstoff_add(z, "timber", 6)
    kuechen.vorrat_add(z, "eel_roh", 2)
    pruefen("Rosi" in fehler(abbau.werkzeug_kaufen, z, MODUL, "axe"), "Stufe 3 erst mit Rosis Werkstatt")
    z["flags"].append("werkstatt_offen")
    pruefen("trust" in fehler(abbau.werkzeug_kaufen, z, MODUL, "axe"), "und Vertrauen 3 mit Petru")
    z["werte"]["vertrauen.petru"] = 3
    abbau.werkzeug_kaufen(z, MODUL, "axe")
    w = {x["id"]: x for x in abbau.werkzeug_ansicht(z, MODUL)}
    pruefen(w["axe"]["stufe"] == 3 and w["axe"]["naechste"] is None, "Stufe 3: die beste Axt, kein weiteres Upgrade")
    pruefen(fehler(abbau.werkzeug_kaufen, z, MODUL, "axe") is not None, "besser wird es nicht")


def petru_fisch_pruefen():
    """Petru kauft Fisch (Brain Trust, Duc 28.10.2026): ab dem ersten Fang, Preis nach Seltenheit, Satz beim ersten Verkauf."""
    from kern import angeln
    z = neues_spiel("f1")
    z["tag"], z["konto"] = 2, 0
    pruefen(abbau.fisch_ansicht(z, MODUL) is None and fehler(abbau.fisch_verkaufen, z, MODUL, "zander") is not None,
            "vor dem ersten Fang: kein Reiter Sell Fish")
    kuechen.kueche(z)["fischbuch"] = {"zander": {"n": 2, "bester": 3}, "sardine": {"n": 1, "bester": 2}}
    kuechen.vorrat_add(z, "zander_roh", 2, 1)
    kuechen.vorrat_add(z, "zander_roh", 3, 1)
    kuechen.vorrat_add(z, "sardine_roh", 2, 3)
    anteil = D["petru"]["fisch_anteil"]
    preis = {f["id"]: f["preis"] for f in D["fische"]}
    v = {x["id"]: x for x in abbau.fisch_ansicht(z, MODUL)}
    pruefen(v["zander"]["preis"] == round(preis["zander"] * anteil["3"]) and v["sardine"]["preis"] == round(preis["sardine"] * anteil["1"])
            and v["zander"]["n"] == 2 and v["zander"]["neu"], "Preis nach Seltenheit (Zander selten, Sardine häufig)")
    j = {f["id"]: f for f in angeln.journal(z, MODUL)["fische"]}
    pruefen(j["zander"]["petru"] is None, "Journal vorher: noch keine Notiz von Petru")
    zeilen, gruppe = abbau.fisch_verkaufen(z, MODUL, "zander")
    pruefen(gruppe == "fisch_zander" and z["konto"] == v["zander"]["preis"] and kuechen.vorrat_menge(z, "zander_roh", 2) == 0
            and kuechen.vorrat_menge(z, "zander_roh", 3) == 1, "erster Verkauf: Petrus Satz, schlechteste Qualität zuerst")
    pruefen(gruppe in json.load(open(os.path.join(EDEN, "module", "eden_rise", "laeden.json"), encoding="utf-8"))["laeden"]["petru"]["zeilen"],
            "Fisch-Satz steht in laeden.json (wird vertont)")
    j = {f["id"]: f for f in angeln.journal(z, MODUL)["fische"]}
    pruefen(j["zander"]["petru"] and "[" not in j["zander"]["petru"], "Journal danach: Petrus Satz als Notiz, ohne Tags")
    _, gruppe = abbau.fisch_verkaufen(z, MODUL, "zander")
    pruefen(gruppe is None and kuechen.vorrat_menge(z, "zander_roh") == 0, "zweiter Verkauf derselben Art: kein Satz mehr")
    z["werte"]["vertrauen.petru"], k = 2, z["konto"]
    _, gruppe = abbau.fisch_verkaufen(z, MODUL, "sardine", alle=True)
    pruefen(z["konto"] - k == 3 * round(preis["sardine"] * (anteil["1"] + 0.10)) and gruppe == "fisch_sardine"
            and kuechen.vorrat_menge(z, "sardine_roh") == 0, "alle auf einmal, +5 % je Vertrauensstufe")
    pruefen(set(D["petru"]["fisch_notiz"]) == {f["id"] for f in D["fische"]}, "jeder der 20 Fische hat einen Satz von Petru")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    quellen_pruefen()
    abbau_pruefen()
    petru_pruefen()
    petru_fisch_pruefen()
    print("ALLES OK")

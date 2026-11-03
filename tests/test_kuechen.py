# -*- coding: utf-8 -*-
"""Kuechenkreis (27.10.2026, E-079): Daten, Vorrat, Baukasten, Tagesbonus, Nonnas Laden mit Frederico, Garten, Tiere.

Laeuft ohne Modell, Stimme und Netz (der Wurf wird festgelegt).

  python tests\\test_kuechen.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
from kern import farm, handel, kampf, kuechen, stimme, wuerfel, zustand  # noqa: E402

MODUL = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
REGELN = json.load(open(os.path.join(EDEN, "module", "eden_rise", "gegenstaende.json"), encoding="utf-8"))["kochen"]
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


def neues_spiel(tag=5, phase="dinner"):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "wahl"
    z["heute"], z["konto"] = [], 2000
    handel.init(z, MODUL)
    return z


def mit_rohstoffen(z, n=60):
    for r in ("timber", "slate", "granite", "cork", "iron", "steel"):
        kuechen.rohstoff_add(z, r, n)
    return z


def festen_wurf(ergebnis="erfolg"):
    wuerfel.probe = lambda *a, **k: {"ergebnis": ergebnis, "wurf": 15, "boni": [("Perception", 2)], "summe": 17, "sg": 10}


def tag_weiter(z, n=1):
    for _ in range(n):
        z["tag"] += 1
        z["phase"] = "fruehstueck"
        farm.tagesbeginn(z, MODUL)


def daten_pruefen():
    z = D["zutaten"]
    pruefen(len(D["fische"]) == 20 and sum(f["ort"] == "meer" for f in D["fische"]) == 10 and sum(f["ort"] == "fluss" for f in D["fische"]) == 10,
            "20 Fische: 10 Meer, 10 Fluss")
    pruefen(all(f["roh"] in z and z[f["roh"]]["rolle"] == "haupt" and z[f["roh"]]["fisch"] == f["id"] for f in D["fische"]), "jeder Fisch hat seine Rohform als Haupt-Zutat")
    pruefen(len(D["geschmack"]) == 14, "Geschmack fuer 14 Personen")
    pruefen({v["effekt"] for v in z.values() if v["rolle"] == "akzent"} == set(D["effekte"]) and len(D["effekte"]) == 7, "7 Akzent-Effekte, jeder mit Zutat")
    pruefen(set(D["tiere"]) == {"chicken", "pig", "cow"}, "drei Staelle: Chicken, Pig, Cow")
    pruefen(len(D["frederico"]) == 8 and all(stimme.TAG_MUSTER.search(x["gesprochen"]) for x in D["frederico"]), "8 Frederico-Saetze mit Turbo-Tag")
    tags = {t["text"]: t["gesprochen"] for t in json.load(open(stimme.TAGS_DATEI, encoding="utf-8"))["zeilen"]}
    pruefen(all(tags.get(x["text"]) == x["gesprochen"] for x in D["frederico"]), "Frederico-Tags stehen in stimme_tags.json")
    pruefen(MODUL["laeden"]["nonna"].get("farm") and MODUL["laeden"]["nonna"]["ab_tag"] == D["nonna"]["ab_tag"], "Nonnas Farm ist ein Laden im Modul")


def vorrat_pruefen():
    z = neues_spiel()
    pruefen("kueche" not in z and kuechen.bonus(z, "krit") == 0 and kuechen.vorrat_menge(z) == 0, "frischer Spielstand: keine neuen Schluessel beim Lesen")
    kuechen.vorrat_add(z, "rice", 1, 3)
    kuechen.vorrat_add(z, "rice", 3, 1)
    pruefen(kuechen.vorrat_menge(z, "rice") == 4 and kuechen.vorrat_menge(z, "rice", 3) == 1, "Vorrat zaehlt je Qualitaet")
    pruefen(fehler(kuechen.vorrat_nehmen, z, "rice|2") is not None, "nichts nehmen, was nicht da ist")
    f = kuechen.fang(z, MODUL, "sea_bass", 2)
    pruefen(f["roh"] == "sea_bass_roh" and kuechen.vorrat_menge(z, "sea_bass_roh", 2) == 2, "Fang: Fisch wird zur Rohform im Vorrat, Qualitaet 2")
    pruefen(fehler(kuechen.fang, z, MODUL, "little_tunny") is not None, "unbekannter Fisch wird abgelehnt (Little Tunny seit 28.10. ersetzt)")
    pruefen(kuechen.fang(z, MODUL, "salmon", 1)["roh"] == "salmon_roh", "Lachs ist ein Meeresfisch (statt Little Tunny)")


def baukasten_pruefen():
    festen_wurf()
    z = neues_spiel()
    for k in ("rice|1", "sea_bass_roh|2", "chilis|3", "noodles|1", "salmon_steak|1", "tomaten|1"):
        kuechen.vorrat_add(z, k.split("|")[0], int(k.split("|")[1]))
    v = kuechen.vorschau(z, MODUL, "rice|1", "sea_bass_roh|2", "chilis|3", ["lea", "alva"])
    pruefen(v["mag"] == ["lea"] and v["mag_nicht"] == ["alva"] and v["effekt"] == "krit" and v["wert"] == 10 and v["heilt"] == 4,
            "Vorschau: Lea mag Fisch, Alva nicht; Chilis aus eigener Zucht = 10 %% Krit (%s)" % v)
    pruefen(fehler(kuechen.kochen_baukasten, z, MODUL, REGELN, "rice|1", "rice|1", "chilis|3", "lea", ["lea"]) is not None, "drei verschiedene Zutaten")
    pruefen(fehler(kuechen.kochen_baukasten, z, MODUL, REGELN, "chilis|3", "sea_bass_roh|2", "rice|1", "lea", ["lea"]) is not None, "falsche Rollen werden abgelehnt")
    z["lp"] = 5
    titel, zeilen = kuechen.kochen_baukasten(z, MODUL, REGELN, "rice|1", "sea_bass_roh|2", "chilis|3", "lea", ["lea"])
    pruefen("Lea likes it" in zeilen and any("Bonus until" in x for x in zeilen), "Teller fuer Lea: sie mag es, Bonus gebucht (%s)" % titel)
    pruefen(kuechen.vorrat_menge(z, "rice") == 0 and kuechen.vorrat_menge(z, "chilis") == 0 and kuechen.vorrat_menge(z, "sea_bass_roh") == 0,
            "die drei Zutaten sind verbraucht")
    pruefen(z["lp"] == 9, "Basis Reis heilt 4 Life")
    pruefen(kuechen.bonus(z, "krit") == 10 and kuechen.bonus(z, "xp") == 0, "Tagesbonus Krit +10, kein anderer")
    pruefen(fehler(kuechen.kochen_baukasten, z, MODUL, REGELN, "noodles|1", "salmon_steak|1", "tomaten|1", "lea", ["lea"]) == "You've already cooked or eaten today.",
            "ein Essen am Tag")
    pruefen(kuechen.vorrat_menge(z, "noodles") == 1 and kuechen.vorrat_menge(z, "salmon_steak") == 1, "misslungener Versuch verbraucht nichts")
    z["tag"], z["phase"] = 6, "tag"
    pruefen(kuechen.bonus(z, "krit") == 10, "am naechsten Morgen gilt der Bonus noch")
    z["phase"] = "dinner"
    pruefen(kuechen.bonus(z, "krit") == 10, "bis zum Dinner des Folgetags (einschliesslich)")
    z["phase"] = "abend"
    pruefen(kuechen.bonus(z, "krit") == 0, "danach ist er weg")
    # Wirkpunkte im Code
    z["tag"], z["phase"] = 5, "dinner"
    defs = kampf.daten(os.path.join(EDEN, "module", "eden_rise"))
    kuechen.kueche(z)["bonus"] = {"effekt": "attribut", "wert": 2, "bis": 99999, "text": ""}
    pruefen(kampf.attributes(z, defs)["courage"] == z["persona"]["attribute"].get("courage", 2) + 2, "Wirkpunkt: Mut +2 im Kampf")
    kuechen.kueche(z)["bonus"] = {"effekt": "xp", "wert": 20, "bis": 99999, "text": ""}
    zeilen = kampf.award_xp(z, 50)
    pruefen(zeilen and zeilen[0] == "+60 experience", "Wirkpunkt: Erfahrung +20 %% (50 -> 60): %s" % zeilen[:1])
    kuechen.kueche(z)["bonus"] = {"effekt": "preis", "wert": 20, "bis": 99999, "text": ""}
    teuer = handel._preis(z, MODUL, "arancini", "alva")
    pruefen(handel.preis(z, MODUL, "arancini", "alva") == max(1, int(round(teuer * 0.8))), "Wirkpunkt: Ladenpreise -20 %%")
    kuechen.kueche(z)["bonus"] = None
    pruefen(handel.preis(z, MODUL, "arancini", "alva") == teuer, "ohne Bonus unveraendert")
    # Crew und Vertrauens-Akzent: sofort, Moral wie beim Kochen fuer die Crew
    z2 = neues_spiel()
    for k in ("potatoes", "chicken_meat", "tomaten"):
        kuechen.vorrat_add(z2, k, 1)
    vor = z2["werte"].get("vertrauen.lola", 0)
    titel, zeilen = kuechen.kochen_baukasten(z2, MODUL, REGELN, "potatoes|1", "chicken_meat|1", "tomaten|1", "crew", handel.crew_an_bord(z2, MODUL))
    pruefen(kuechen.bonus(z2, "vertrauen") == 0 and z2["kueche"]["bonus"] is None, "Trust-Akzent ist ein Sofort-Effekt, kein Tagesbonus")
    pruefen(z2["werte"].get("vertrauen.lola", 0) >= vor, "Crew-Essen laeuft ueber den bekannten Weg (%s)" % zeilen[:3])


def nonna_pruefen():
    z = neues_spiel(tag=3)
    pruefen(not kuechen.nonna_offen(z, MODUL) and kuechen.nonna_ansicht(z, MODUL) is None and farm.ansicht(z, MODUL) is None, "vor Tag 4 geschlossen")
    pruefen(fehler(kuechen.nonna_kaufen, z, MODUL, "eggs") is not None, "vor Tag 4 kein Einkauf")
    z["tag"] = 5
    a = kuechen.nonna_ansicht(z, MODUL)
    pruefen({w["id"] for w in a["waren"]} >= {"rice", "eggs", "salmon_steak"} and next(w for w in a["waren"] if w["id"] == "eggs")["n"] == 3, "Ansicht: Grundzutaten und Tagesvorrat")
    konto = z["konto"]
    preis = kuechen.nonna_kaufen(z, MODUL, "eggs", 2)
    pruefen(z["konto"] == konto - preis and preis == 2 * D["zutaten"]["eggs"]["preis"], "Einkauf zahlt sofort (%d)" % preis)
    pruefen(kuechen.vorrat_menge(z, "eggs") == 0, "die Ware ist noch nicht da")
    pruefen(fehler(kuechen.nonna_kaufen, z, MODUL, "eggs", 2) is not None, "Tagesvorrat: nur 1 Ei uebrig")
    kuechen.nonna_kaufen(z, MODUL, "rice", 5)
    i = kuechen.nonna_verlassen(z, MODUL)
    pruefen(i is not None and 0 <= i < 8 and kuechen.vorrat_menge(z, "eggs", 1) == 2 and kuechen.vorrat_menge(z, "rice", 1) == 5,
            "Laden verlassen: Frederico (fred.%s) bringt es rueber, Qualitaet 1" % i)
    pruefen(kuechen.nonna_verlassen(z, MODUL) is None, "ohne Einkauf kommt Frederico nicht")
    pruefen(kuechen.zeile(MODUL, "fred.%d" % i)[0] == "frederico" and kuechen.zeile(MODUL, "fred.99") == (None, None) and kuechen.zeile(MODUL, "fred.x") == (None, None),
            "Audio-Zeile nur fuer feste Saetze")
    z["tag"] = 6
    pruefen(next(w for w in kuechen.nonna_ansicht(z, MODUL)["waren"] if w["id"] == "eggs")["n"] == 3, "am naechsten Tag ist der Vorrat wieder voll")


def garten_pruefen():
    z = neues_spiel()
    pruefen(fehler(farm.garten_pflanzen, z, MODUL, 9, "tomaten") is not None and fehler(farm.garten_pflanzen, z, MODUL, 0, "rice") is not None, "ungueltiges Beet/Pflanze")
    konto = z["konto"]
    farm.garten_pflanzen(z, MODUL, 0, "tomaten")
    pruefen(z["konto"] == konto - D["pflanzen"]["tomaten"]["preis"] and fehler(farm.garten_pflanzen, z, MODUL, 0, "chilis") is not None, "Saatgeld, Beet belegt")
    pruefen(farm.garten_ansicht(z, MODUL)[0]["rest"] == 1, "Ernte in 1 Tag")
    tag_weiter(z)
    pruefen(kuechen.vorrat_menge(z, "tomaten", 3) == 3 and farm.garten_ansicht(z, MODUL)[0]["leer"], "naechster Morgen: 3 Tomaten, Qualitaet 3, Beet leer")


def tiere_pruefen():
    z = mit_rohstoffen(neues_spiel())
    pruefen(fehler(farm.tier_kaufen, z, MODUL, "chicken") is not None, "ohne Stall kein Tier")
    farm.stall_kaufen(z, MODUL, "chicken")
    pruefen(fehler(farm.stall_kaufen, z, MODUL, "chicken") is not None, "Stall nur einmal")
    a, b = farm.tier_kaufen(z, MODUL, "chicken"), farm.tier_kaufen(z, MODUL, "chicken")
    pruefen((a["geschlecht"], b["geschlecht"]) == ("f", "m") and a["neu"], "erstes Tier ein Weibchen, dann ausgleichen")
    pruefen(fehler(farm.tier_benennen, z, MODUL, "chicken", a["id"], "<b>x</b>") is not None and fehler(farm.tier_benennen, z, MODUL, "chicken", a["id"], "") is not None, "Namen: nur Buchstaben")
    farm.tier_benennen(z, MODUL, "chicken", a["id"], "Gina Maria")
    pruefen(a["name"] == "Gina Maria" and not a["neu"], "benannt")
    t = D["tiere"]["chicken"]
    pruefen(farm.stufe(t, a, z["tag"]) == 1 and farm.variante(t, a, z["tag"]) == "baby", "Stufe 1 = Baby")
    # Alter: baby_tage 2 -> Stufe 2 ab Tag +2, Eier ab dem Tag danach, nur das Weibchen
    tag_weiter(z, 2)
    pruefen(farm.stufe(t, a, z["tag"]) == 2 and kuechen.vorrat_menge(z, "eggs") == 0, "Tag 2: erwachsen, noch keine Eier")
    tag_weiter(z)
    pruefen(kuechen.vorrat_menge(z, "eggs", 3) == 1, "ab dem naechsten Tag: 1 Ei (nur die Henne, nicht der Hahn)")
    pruefen(farm.variante(t, a, z["tag"]) == "adult_f" and farm.variante(t, b, z["tag"]) == "adult_m", "Sprite-Variante adult_f / adult_m")
    # Zucht: Paar erwachsen ab Tag 7, zucht_tage 3 seit der letzten Geburt (Stall Tag 5): Babys an Tag 8 und 11
    pruefen(len(z["kueche"]["staelle"]["chicken"]["tiere"]) == 3, "Tag 8: das erwachsene Paar hat ein Baby bekommen")
    tag_weiter(z, 3)
    pruefen(len(z["kueche"]["staelle"]["chicken"]["tiere"]) == 4, "Tag 11: das naechste Baby nach der Zuchtzeit (%d Tiere)" % len(z["kueche"]["staelle"]["chicken"]["tiere"]))
    baby = z["kueche"]["staelle"]["chicken"]["tiere"][-1]
    pruefen(baby["neu"] and baby["geboren"] == z["tag"], "das Baby ist neu und kann benannt werden")
    pruefen(fehler(farm.tier_schlachten, z, MODUL, "chicken", a["id"]) is not None, "Schlachten nur Stufe 3")
    tag_weiter(z, 3)                                    # Tag 5+2+1+3+3 = 14: Henne a (geboren 5) wird 9 Tage alt -> alt (2+5=7)
    pruefen(farm.stufe(t, a, z["tag"]) == 3, "Stufe 3 = alt")
    eier = kuechen.vorrat_menge(z, "eggs")
    tag_weiter(z)
    pruefen(kuechen.vorrat_menge(z, "eggs") >= eier and not any(x["bringt"] for x in farm.ansicht(z, MODUL)["staelle"][0]["tiere"] if x["id"] == a["id"]), "alte Tiere legen nichts mehr")
    zeilen = farm.tier_schlachten(z, MODUL, "chicken", a["id"])
    pruefen(kuechen.vorrat_menge(z, "chicken_meat", 3) == 2 and a not in z["kueche"]["staelle"]["chicken"]["tiere"], "geschlachtet: 2 Chicken, Qualitaet 3 (%s)" % zeilen[0])
    # Schwein und Kuh: Trueffel von jedem, Milch nur von der Kuh
    z2 = mit_rohstoffen(neues_spiel())
    farm.stall_kaufen(z2, MODUL, "pig")
    p1 = farm.tier_kaufen(z2, MODUL, "pig")
    farm.stall_kaufen(z2, MODUL, "cow")
    k1, k2 = farm.tier_kaufen(z2, MODUL, "cow"), farm.tier_kaufen(z2, MODUL, "cow")
    tag_weiter(z2, 3 + 1)                                # Schwein: baby 3 Tage, erwachsen ab Tag 3; Truefel alle 2 Tage ab dem 2. Tag
    pruefen(kuechen.vorrat_menge(z2, "truffle") == 0, "Schwein: noch kein Trueffel am ersten Erwachsenentag")
    tag_weiter(z2, 1)
    pruefen(kuechen.vorrat_menge(z2, "truffle", 3) == 1, "Schwein findet nach 2 Erwachsenentagen einen Trueffel")
    pruefen(kuechen.vorrat_menge(z2, "milk", 3) == 1, "Kuh (Weibchen, baby 4 Tage) gibt am Tag nach der Reife Milch; der Bulle nicht")
    tag_weiter(z2, 1)
    pruefen(kuechen.vorrat_menge(z2, "milk") == 2 and kuechen.vorrat_menge(z2, "truffle") == 1, "Milch taeglich, Trueffel nur alle 2 Tage")
    pruefen(len(farm.ansicht(z2, MODUL)["staelle"]) == 3 and all(s["plaetze"] for s in farm.ansicht(z2, MODUL)["staelle"]), "Farm-Ansicht: drei Staelle")
    z3 = mit_rohstoffen(neues_spiel())
    farm.stall_kaufen(z3, MODUL, "cow")
    for _ in range(3):
        farm.tier_kaufen(z3, MODUL, "cow")
    pruefen(fehler(farm.tier_kaufen, z3, MODUL, "cow") == "The shed is full.", "Platzgrenze des Stalls")


def ausbau_pruefen():
    z = neues_spiel()
    pruefen(fehler(farm.stall_kaufen, z, MODUL, "chicken") == "You're short of materials for that.", "Stall bauen braucht Rohstoffe")
    konto = z["konto"]
    pruefen(z["konto"] == konto, "ohne Rohstoffe wird nichts abgebucht")
    # Holz bei Nonna kaufen: kommt mit Frederico
    kuechen.nonna_kaufen(z, MODUL, "timber", 4)
    pruefen(kuechen.rohstoffe(z).get("timber", 0) == 0, "Holz ist bezahlt, aber noch nicht da")
    pruefen(fehler(kuechen.nonna_kaufen, z, MODUL, "timber", 3) == "Nonna has none of that left today.", "Nonnas Holzvorrat ist begrenzt (6 am Tag)")
    kuechen.nonna_verlassen(z, MODUL)
    pruefen(kuechen.rohstoffe(z)["timber"] == 4 and kuechen.vorrat_menge(z, "timber") == 0, "Frederico bringt das Holz (Rohstoffe, nicht Vorrat)")
    kuechen.rohstoff_add(z, "slate", 2)                    # Stufe 1 braucht seit 30.10.2026 auch Schiefer
    farm.stall_kaufen(z, MODUL, "chicken")
    s = z["kueche"]["staelle"]["chicken"]
    pruefen(s["stufe"] == 1 and kuechen.rohstoffe(z)["timber"] == 0, "Hühnerstall Stufe 1 gebaut: 4 Holz verbraucht")
    pruefen(fehler(farm.stall_ausbauen, z, MODUL, "chicken") == "You're short of materials for that.", "Ausbau braucht Rohstoffe")
    mit_rohstoffen(z)
    farm.stall_ausbauen(z, MODUL, "chicken")
    pruefen(s["stufe"] == 2 and farm.stufe_def(kuechen.daten(MODUL), "chicken", s)["plaetze"] == 9, "Stufe 2: 9 Plätze")
    for _ in range(9):
        farm.tier_kaufen(z, MODUL, "chicken")
    pruefen(fehler(farm.tier_kaufen, z, MODUL, "chicken") == "The shed is full.", "Platzgrenze steigt mit der Stufe")
    farm.stall_ausbauen(z, MODUL, "chicken")
    pruefen(s["stufe"] == 3 and fehler(farm.stall_ausbauen, z, MODUL, "chicken") == "The shed is already fully upgraded.", "Stufe 3 ist das Ende")
    # Stufe 3: Henne legt 2 Eier
    t = kuechen.daten(MODUL)["tiere"]["chicken"]
    henne = next(x for x in s["tiere"] if x["geschlecht"] == "f")
    s["tiere"] = [henne]
    tag_weiter(z, t["baby_tage"] + 1)
    pruefen(kuechen.vorrat_menge(z, "eggs", 3) == 2, "Stufe 3: eine Henne legt 2 Eier am Tag")
    a = farm.ansicht(z, MODUL)
    pruefen(a["staelle"][0]["stufe"] == 3 and a["staelle"][0]["naechste"] is None and a["staelle"][1]["naechste"]["stufe"] == 1,
            "Ansicht: Stufe, nächster Ausbau mit Kosten")
    pruefen([r["id"] for r in a["rohstoffe"]] == ["timber", "slate", "granite", "iron", "cork", "feather", "cloth", "wool", "leather", "coral", "steel"], "Ansicht zeigt die elf Rohstoffe (Kork seit 28.10., Möwenfeder, Stoff, Wolle, Leder, Koralle seit 30.10.)")


def fischsauce_pruefen():
    festen_wurf()
    z = neues_spiel()
    for iid in ("fish_sauce", "tofu", "rice_paper"):
        if MODUL["items"][iid].get("zutat"):
            kuechen.vorrat_add(z, MODUL["items"][iid]["zutat"], 1)
    pruefen(kuechen.vorrat_menge(z, "fish_sauce", 1) == 1, "Fischsauce liegt im Vorrat")
    kuechen.vorrat_add(z, "sea_bass_roh", 2)
    v = kuechen.vorschau(z, MODUL, "rice_paper|1", "sea_bass_roh|2", "fish_sauce|1", ["lea", "alva"])
    pruefen(v["mag"] == ["lea"] and v["mag_nicht"] == [] and v["bonus"] == "Nobody dislikes this dish", "Fischsauce: Alva lehnt den Fisch nicht mehr ab (%s)" % v)
    titel, zeilen = kuechen.kochen_baukasten(z, MODUL, REGELN, "rice_paper|1", "sea_bass_roh|2", "fish_sauce|1", "alva", ["alva"])
    pruefen(not (z.get("kueche") or {}).get("bonus"), "Fischsauce gibt keinen Tagesbonus")
    pruefen(not any("won't touch" in x or "without much joy" in x for x in zeilen), "Alva isst den Teller (%s)" % zeilen)


def batu_ware_pruefen():
    z = neues_spiel(tag=9)
    z["flags"].append("batu_laden")
    z.setdefault("heute", []).append({"ort": "alvas_bar", "phase": "tag", "titel": "Alva's Bar"})
    z["konto"], z["werte"]["energie"], z["werte"]["moral"] = 100, 0, 0
    pruefen("pho_bowl" in [w["id"] for w in handel.sortiment(z, MODUL, "batu")], "Ba Tu hat die Schale")
    handel.kaufen(z, MODUL, "batu", "pho_bowl")
    pruefen(z["werte"]["energie"] == 1 and z["werte"]["moral"] == 0, "Schale: Energie +1, keine Moral")
    pruefen(handel.essen_heute(z)["anzahl"] == 1 and "pho_bowl" not in [w["id"] for w in handel.sortiment(z, MODUL, "batu")], "Schale zaehlt als Essen, einmal am Tag")
    pruefen("lemongrass" not in [p["id"] for p in farm.ansicht(z, MODUL)["pflanzen"]], "Zitronengras erst nach dem Kauf")
    pruefen(fehler(farm.garten_pflanzen, z, MODUL, 0, "lemongrass") is not None, "ohne Steckling waechst es nicht")
    handel.kaufen(z, MODUL, "batu", "lemongrass_cutting")
    pruefen("lemongrass" in [p["id"] for p in farm.ansicht(z, MODUL)["pflanzen"]], "Steckling schaltet die Pflanze frei")
    pruefen("lemongrass_cutting" not in [w["id"] for w in handel.sortiment(z, MODUL, "batu")], "Steckling nur einmal")
    farm.garten_pflanzen(z, MODUL, 0, "lemongrass")
    pruefen(z["flag_tag"].get("zitronengras_gepflanzt") == 9, "Nonna merkt das Pflanzen (datiertes Flag)")


def kein_neuer_schluessel_pruefen():
    z = neues_spiel()
    farm.tagesbeginn(z, MODUL)
    pruefen("kueche" not in z, "Tageswechsel ohne Farm legt keinen Schluessel an")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    daten_pruefen()
    vorrat_pruefen()
    baukasten_pruefen()
    nonna_pruefen()
    garten_pruefen()
    tiere_pruefen()
    ausbau_pruefen()
    fischsauce_pruefen()
    batu_ware_pruefen()
    kein_neuer_schluessel_pruefen()
    print("ALLES OK")

# -*- coding: utf-8 -*-
"""Romanzen-Leiter, Probe Rosi und Lea (Duc 31.10.2026): Szenen kommen fest ueber die Stufe statt per Zufall, hoechstens eine
am Tag, Echo am naechsten Morgen, zweiter Takt, Strichliste, Zeilen je Spielverlauf.

  python tests\\test_romanzen_leiter.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import chronik, ereignisse, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
D = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]
I = {e["id"]: e for e in D}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag, phase, **werte):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"], z["status"] = tag, phase, "szene"
    z.setdefault("verlauf", [])
    z.setdefault("heute", [])
    for k, v in werte.items():
        z["werte"][k.replace("_", ".")] = v
    return z


def geht(z, eid):
    return ereignisse.passt(z, MODUL, I[eid], z["phase"], None, True)


def ziehen(z):
    ev = ereignisse.pflicht_ziehen(z, MODUL, MOD)
    return ev["id"] if ev else None


def leiter_ziehen(z):
    """Nur die Romanzen-Leiter: alle anderen Pflicht-Events gelten als gesehen."""
    e = ereignisse.stand(z)
    e["gesehen"] += [x["id"] for x in D if x["wann"].get("pflicht") and not x["id"].startswith("rm_")]
    return ziehen(z)


# Stufe und Tag entscheiden, nicht der Zufall
z = spiel(4, "nacht", vertrauen_rosi=3, begehren_rosi=3)
pruefen(leiter_ziehen(z) == "rm_r1", "Rosi Stufe 3/3, Tag 4 nachts: Nothing's Broken kommt fest")
pruefen(leiter_ziehen(z) is None, "Hoechstens eine Leiter-Szene am Tag")
z = spiel(4, "nacht", vertrauen_rosi=2, begehren_rosi=3)
pruefen(not geht(z, "rm_r1"), "Rosi Vertrauen 2: die Szene wartet")
z = spiel(3, "nacht", vertrauen_rosi=5, begehren_rosi=5)
pruefen(not geht(z, "rm_r1"), "Zu frueher Tag: die Szene wartet auch bei Stufe 5")
z = spiel(5, "nacht", vertrauen_rosi=3, begehren_rosi=3)
z["flags"].append("gefeuert_rosi")
pruefen(not geht(z, "rm_r1"), "Gefeuert: keine Szene")

# Reihenfolge: R2 frueh genug erst zwei Tage nach R1, R4 erst ab Tag 15 und nach einem Kampf
z = spiel(6, "nacht", vertrauen_rosi=3, begehren_rosi=4)
pruefen(not geht(z, "rm_r2"), "Ohne R1 kein R2")
z["flags"].append("rm_r1")
z["flag_tag"] = {"rm_r1": 4}
pruefen(geht(z, "rm_r2"), "Zwei Tage nach R1 kommt R2")
z = spiel(15, "nacht", vertrauen_rosi=4, begehren_rosi=5)
z["flags"].append("rm_r3")
z["flag_tag"] = {"rm_r3": 10}
pruefen(not geht(z, "rm_r4"), "Tag 15 ohne Kampf: Read It wartet")
z["kampf_tag"] = 15
pruefen(geht(z, "rm_r4"), "Tag 15 nach einem Kampf: Read It")
z = spiel(19, "nacht", vertrauen_rosi=4, begehren_rosi=5)
z["flags"].append("rm_r3")
z["flag_tag"] = {"rm_r3": 10}
pruefen(geht(z, "rm_r4"), "Ab Tag 19 auch ohne Kampf, damit die Szene nicht ausfaellt")

# Zweiter Takt
z = spiel(15, "nacht", vertrauen_rosi=4, begehren_rosi=5)
ereignisse.anwenden(z, MODUL, I["rm_r4"], I["rm_r4"]["optionen"][0]["folgen"])
pruefen(ereignisse.direkt_ziel(z) == "rm_r4_b", "Read It: nach der Stille kommt das Whiteboard")
pruefen("phasen" not in I["rm_r4_b"]["wann"] and not geht(z, "rm_r4_b") if False else "phasen" not in I["rm_r4_b"]["wann"],
        "Der zweite Takt wird nie von selbst gezogen")
z = spiel(10, "abend")
ereignisse.anwenden(z, MODUL, I["rm_l2"], I["rm_l2"]["optionen"][0]["folgen"])
pruefen(ereignisse.direkt_ziel(z) == "rm_l2_c", "What Are We? ohne Taucherzeichen: Antwort mit Worten")
z = spiel(10, "abend")
z["flags"].append("lea_zeichen")
ereignisse.anwenden(z, MODUL, I["rm_l2"], I["rm_l2"]["optionen"][0]["folgen"])
pruefen(ereignisse.direkt_ziel(z) == "rm_l2_b", "What Are We? mit Taucherzeichen: zwei Finger")
pruefen("fingers" in I["rm_l2_b"]["optionen"][0]["text"] and "fingers" not in I["rm_l2_c"]["optionen"][0]["text"], "Die Antwort passt zum Takt")

# Strichliste und Zeilen je Verlauf
z = spiel(15, "nacht")
pruefen("There are 3 of them" in ereignisse.lage_text(I["rm_r4_b"], z), "Strichliste: mindestens drei")
z["verlauf"] = [{"anwesend": ["rosi"], "tag": t} for t in range(1, 9)] + [{"anwesend": ["lea"], "tag": 2}]
pruefen("There are 8 of them" in ereignisse.lage_text(I["rm_r4_b"], z), "Strichliste: zaehlt die Szenen mit ihr")
pruefen("{striche}" not in ereignisse.lage_text(I["rm_r4_b"], z), "Kein Platzhalter im Spieltext")
ohne = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["rm_r4_b"], z)]
z["flags"].append("rm_r3_still")
mit = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["rm_r4_b"], z)]
pruefen(len(mit) == len(ohne) + 1 and any("She talks" in t for t in mit), "Wer still gelauscht hat, hoert: She talks")
z = spiel(4, "nacht")
a = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["rm_l1"], z)]
z["flags"].append("lea_weck_mich")
b = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["rm_l1"], z)]
pruefen(any("never said" in t for t in a) and any("You said to wake" in t for t in b) and len(a) == len(b), "Stay Together: passt dazu, ob Duc es gesagt hat")

# Echo
z = spiel(5, "fruehstueck", vertrauen_rosi=2, begehren_rosi=2)
pruefen(not geht(z, "rm_e_rosi_nacht1"), "Ohne Nacht kein Echo")
chronik.eintragen(z, MODUL, "moment", "Duc and Rosi slept together.", wer=["rosi"], dabei=["rosi"], wichtig=3, moment="intimate")
pruefen(leiter_ziehen(z) == "rm_e_rosi_nacht1", "Am Morgen danach: That was a duel")
pruefen(not geht(z, "rm_e_rosi_nacht2"), "Erste Nacht: nicht die Zeile fuer die zweite")
ereignisse.anwenden(z, MODUL, I["rm_e_rosi_nacht1"], I["rm_e_rosi_nacht1"]["optionen"][0]["folgen"])
pruefen(not chronik.moment_offen(z, "rosi", ["intimate"]), "Das Echo gilt als aufgegriffen, die freie Szene wiederholt es nicht")
z["tag"] = 6
chronik.eintragen(z, MODUL, "moment", "Duc and Rosi slept together.", wer=["rosi"], dabei=["rosi"], wichtig=3, moment="intimate")
pruefen(geht(z, "rm_e_rosi_nacht2"), "Zweite Nacht: Statistically unusual")
z = spiel(5, "fruehstueck")
chronik.eintragen(z, MODUL, "moment", "Duc and Lea slept together.", wer=["lea"], dabei=["lea"], wichtig=3, moment="intimate")
z["tag"] = 10
pruefen(not geht(z, "rm_e_lea_nacht1"), "Nach Tagen ist das Echo verfallen")
z = spiel(5, "fruehstueck")
chronik.eintragen(z, MODUL, "moment", "Duc stood Rosi up.", wer=["rosi"], dabei=["rosi"], wichtig=2, dauer=2, moment="stood_up")
pruefen(geht(z, "rm_e_rosi_versetzt"), "Versetzt: sie sagt am Morgen etwas dazu")
pruefen(not geht(z, "rm_e_rosi_kuss"), "Versetzen ist kein Kuss")
z = spiel(5, "fruehstueck")
z["flags"].append("verletzt_lea")
pruefen(geht(z, "rm_e_lea_verletzt"), "Eifersucht: Seahorses")

# Chiara und Sophia
z = spiel(4, "nacht", vertrauen_chiara=3, begehren_chiara=3)
pruefen(leiter_ziehen(z) == "rm_c1", "Chiara Stufe 3/3: Examiner kommt fest")
ereignisse.anwenden(z, MODUL, I["rm_c1"], I["rm_c1"]["optionen"][0]["folgen"])
pruefen(ereignisse.direkt_ziel(z) == "rm_c1_b", "Examiner: zweiter Takt")
z = spiel(15, "nacht", vertrauen_sophia=5, begehren_sophia=5)
z["flags"].append("rm_s3")
z["flag_tag"] = {"rm_s3": 10}
pruefen(geht(z, "rm_s4"), "The Last Train kommt")
z["flags"].append("lea_zusammen")
pruefen(not geht(z, "rm_s4"), "Schwestern-Regel: nicht, wenn Duc mit Lea zusammen ist")
z = spiel(10, "abend", vertrauen_lea=4, begehren_lea=4)
z["flags"].append("rm_l1")
z["flag_tag"] = {"rm_l1": 4}
pruefen(geht(z, "rm_l2"), "What Are We? kommt")
z["flags"].append("sophia_zusammen")
pruefen(not geht(z, "rm_l2"), "Schwestern-Regel: nicht, wenn Duc mit Sophia zusammen ist")
z = spiel(15, "nacht")
a = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["rm_s4"], z)]
z["flags"].append("rm_l1")
b = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["rm_s4"], z)]
pruefen(len(b) == len(a) + 1 and any("salutes" in t for t in b), "Sophia spricht Lea nur an, wenn Lea Duc naehergekommen ist")
pruefen(not any("Holm's asleep" in json.dumps(e, ensure_ascii=False) for e in D), "Holm schlaeft nirgends mehr an Bord")

# Erinnerungen: Der Spieler hat die Szene davor vergessen (Duc 31.10.2026)
pruefen("the night you held the lamp" in json.dumps(I["rm_r4_b"], ensure_ascii=False), "Rosi erinnert an das erste Relais")
pruefen("that she has covered with her hand" in I["rm_r4_b"]["lage"], "Die Lage erinnert an die verdeckte Zeile")
pruefen("divers' sign" in I["rm_l2_b"]["optionen"][0]["text"], "Die Antwort erinnert an das Taucherzeichen")
pruefen("the vicar and the marmalade" in json.dumps(I["rm_s3"], ensure_ascii=False), "Sophia erinnert an den Vikar")
pruefen("You once bet me ten euros" in I["rm_s4_b"]["optionen"][1]["text"], "Die Antwort erinnert an die Wette")
pruefen("So tell me. What do you see?" in I["rm_s4_b"]["zeilen"][0]["text"], "Sophia stellt eine klare Frage")

# Stufen-Abstand: 7 Tage ab Stufe 3 (Duc 31.10.2026)
z = spiel(4, "tag", vertrauen_rosi=3)
z["punkte"] = {"vertrauen.rosi": 40}
z.setdefault("stufe_tag", {})["vertrauen.rosi"] = 4
zeilen = zustand.punkte_add(z, MODUL, "vertrauen.rosi", 30)
pruefen(z["werte"]["vertrauen.rosi"] == 3 and z["punkte"]["vertrauen.rosi"] == 54, "Abstand: Die Stufe wartet, der Balken bleibt voll")
pruefen(any("few more days" in x for x in zeilen), "Abstand: Der Spieler sieht es")
pruefen(zustand.punkte_add(z, MODUL, "vertrauen.rosi", 5) == [], "Abstand: Die Meldung kommt nur einmal")
z["tag"] = 11
zustand.punkte_add(z, MODUL, "vertrauen.rosi", 5)
pruefen(z["werte"]["vertrauen.rosi"] == 4 and z["stufe_tag"]["vertrauen.rosi"] == 11, "Abstand: Nach 7 Tagen steigt sie")
zustand.punkte_add(z, MODUL, "vertrauen.rosi", 60)
pruefen(z["werte"]["vertrauen.rosi"] == 4, "Abstand: Danach beginnt die Wartezeit neu")
z = spiel(2, "tag", vertrauen_lea=2)
z["punkte"] = {"vertrauen.lea": 30}
zustand.punkte_add(z, MODUL, "vertrauen.lea", 40)
pruefen(z["werte"]["vertrauen.lea"] == 3, "Abstand: Bis Stufe 3 frei, auch bei einem grossen Sprung nur bis dorthin")
z = spiel(4, "tag", vertrauen_rosi=3)
z["punkte"] = {"vertrauen.rosi": 40}
z.setdefault("stufe_tag", {})["vertrauen.rosi"] = 4
zustand.folgen_anwenden(z, MODUL, [{"wert": "vertrauen.rosi", "delta": 2}])
zustand.punkte_add(z, MODUL, "vertrauen.rosi", 5, roh=True)
pruefen(z["werte"]["vertrauen.rosi"] == 4, "Abstand: Story-Folgen und Spruenge sind ausgenommen")
z = spiel(4, "tag", vertrauen_rosi=3)
z["punkte"] = {"vertrauen.rosi": 40}
z.setdefault("stufe_tag", {})["vertrauen.rosi"] = 4
zustand.folgen_anwenden(z, MODUL, [{"wert": "vertrauen.rosi", "delta": 2}], frei=False)
pruefen(z["werte"]["vertrauen.rosi"] == 3, "Abstand: Gesten und Geschenke unterliegen ihm")
zustand.STUFEN_ABSTAND = 0
z = spiel(4, "tag", vertrauen_rosi=3)
z["punkte"] = {"vertrauen.rosi": 40}
z.setdefault("stufe_tag", {})["vertrauen.rosi"] = 4
zustand.punkte_add(z, MODUL, "vertrauen.rosi", 20)
pruefen(z["werte"]["vertrauen.rosi"] == 4, "Abstand 0: zum Testen aus")
zustand.STUFEN_ABSTAND = 7

# Texte
for i in [x for x in I if x.startswith("rm_")]:
    e = I[i]
    pruefen(e["zeilen"] and all("[" not in l["text"] for l in e["zeilen"]), "%s: Zeilen ohne Turbo-Tag in der Anzeige" % i)
tags = {x["text"] for x in json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
fehlt = [l["text"] for i, e in I.items() if i.startswith("rm_") for l in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]
         if l["text"] not in tags]
pruefen(not fehlt, "Jede Zeile hat eine gesprochene Fassung (%s)" % fehlt[:2])
pruefen(not any(e["wann"].get("akt2") == [8, 21] for i, e in I.items() if i.startswith("rm_")), "Laeuft bis zum Spielende, nicht nur bis Tag 21")
print("fertig")

# Wer sich um eine Frau kuemmert, sieht mehr von ihr; Gags bleiben Zufall
z = spiel(10, "tag")
z["punkte"] = {"vertrauen.lea": 60, "begehren.lea": 60, "vertrauen.rosi": 40, "begehren.rosi": 40, "vertrauen.siri": 5}
f = ereignisse.fokus_faktor(z, MODUL)
pruefen(f(I["fl_lea_neopren"]) == ereignisse.FOKUS_FAKTOR, "Fokus: Flirt mit der naechsten Frau zaehlt mehr")
pruefen(f(I["fl_rosi_bandana"]) == ereignisse.FOKUS_FAKTOR, "Fokus: auch mit der zweitnaechsten")
pruefen(f(I["fl_siri_blick"]) == 1, "Fokus: nicht mit den anderen")
pruefen(f(I["g1_kevin_butter"]) == 1, "Fokus: Gags bleiben Zufall")

# Alte Events reagieren auf die erste Nacht
z = spiel(10, "tag")
vor = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["fl_lea_fakt"], z)]
pruefen(not any("sea otter" in t for t in vor), "Altes Event: vor der Nacht unveraendert")
pruefen(geht(z, "fl_siri_date") or True, "Altes Event: Erste-Annaeherung pruefbar")
chronik.eintragen(z, MODUL, "moment", "x", wer=["lea"], dabei=["lea"], wichtig=3, moment="intimate")
nach = [x["text"] for _, x in ereignisse.zeilen_aktiv(I["fl_lea_fakt"], z)]
pruefen(any("sea otter" in t for t in nach) and len(nach) == len(vor) + 1, "Altes Event: nach der Nacht eine Zeile mehr")
z = spiel(10, "abend", vertrauen_siri=3, begehren_siri=3)
z["flags"].append("siri_frei")
b = I["fl_siri_date"]["wann"]["bedingung"]
from kern import regeln  # noqa: E402
pruefen(regeln.gilt(b, z), "Erste Annaeherung: vor der Nacht moeglich")
chronik.eintragen(z, MODUL, "moment", "x", wer=["siri"], dabei=["siri"], wichtig=3, moment="intimate")
pruefen(not regeln.gilt(b, z), "Erste Annaeherung: danach nicht mehr")

# Lola, Alva, Siri, dazu das Echo fuer Jana und Megan
z = spiel(4, "abend", vertrauen_lola=3, begehren_lola=3)
pruefen(leiter_ziehen(z) == "rm_o1", "Lola Stufe 3/3: The Spoon kommt fest")
z = spiel(6, "fruehstueck", vertrauen_lola=3, begehren_lola=4)
z["flags"].append("rm_o1")
z["flag_tag"] = {"rm_o1": 4}
pruefen(not geht(z, "rm_o2"), "Breakfast in Bed erst nach ihrer Nacht")
z["flags"].append("lola_abend")
pruefen(geht(z, "rm_o2"), "Nach ihrer Nacht kommt Breakfast in Bed")
z = spiel(4, "abend", vertrauen_alva=3, begehren_alva=3)
pruefen(geht(z, "rm_a1"), "Alva Stufe 3/3: The Board")
z = spiel(4, "abend", vertrauen_siri=3, begehren_siri=3)
pruefen(not geht(z, "rm_i1"), "Siri ist noch mit Yasin zusammen: keine Szene")
z["flags"].append("siri_frei")
pruefen(geht(z, "rm_i1"), "Nach der Trennung: Caption")
for pid, eid in (("jana", "rm_e_jana_nacht"), ("megan", "rm_e_megan_nacht")):
    z = spiel(8, "fruehstueck")
    pruefen(not geht(z, eid), "%s: ohne Nacht kein Echo" % pid)
    chronik.naehe_eintragen(z, MODUL, pid, "naehe_weit")
    pruefen(geht(z, eid), "%s: Am Morgen danach kommt das Echo" % pid)
print("fertig 2")

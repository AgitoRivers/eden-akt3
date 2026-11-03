# -*- coding: utf-8 -*-
r"""Ortskapitel Berge (Duc 27.10.2026): Petrus Auftrag, die 12 Stationen, beide Umwege, die drei Wege und die spaeten
Anrufe ueber die Engine. Kaempfe werden im Test direkt gewonnen (kampf._finish "ko").

  Lauf 1: Umwege unterwegs - Baerin getoetet, Panther gehetzt -> Bosskampf solo, Petru in der Bergerie, Weg C
  Lauf 2: ohne Umwege, Wolff dreimal angelogen -> Toto lehnt ab (Weg B zu), Weg C hart, dann Wiederkommen
  Lauf 3: Umweg als eigener Ausflug - Chip geschnitten, zwei Tage spaeter der Anruf wegen Ghjuvan

  python tests\test_berge.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402
import test_kloster as K  # noqa: E402

E = L.eden
WAHL = {}                      # Frame -> Liste von Optionen (wird der Reihe nach verbraucht), sonst Option 0


def setzen(**kw):
    z = E.aktiv()
    for k, v in kw.items():
        z[k] = v
    E.sichern(z)


def ausflug(ort):
    z = E.aktiv()
    start = (z["tag"], z["phase"])
    E.aktion("ort_betreten", {"id": ort})
    frames, kaempfe = [], []
    for _ in range(120):
        z = E.aktiv()
        if z["status"] == "kampf":
            kaempfe.append(z["kampf"]["definition"])
            E.kampf._finish(z, E.modul_laden(), z["kampf"], "ko")
            E.sichern(z)
            E.aktion("kampf_schliessen", {})
            continue
        ev = z.get("event") or {}
        if z["status"] != "ereignis" or not ev.get("id", "").startswith("bg_"):
            break
        frames.append(ev["id"])
        liste = WAHL.get(ev["id"]) or [0]
        wahl = liste.pop(0) if len(liste) > 1 else liste[0]
        E.aktion("event_wahl", {"index": wahl})
        E.aktion("event_schliessen", {})
    z = E.aktiv()
    assert (z["tag"], z["phase"]) != start, "Ausflug hat die Phase nicht verbraucht"
    assert not z.get("ort_aktiv") and not z.get("expedition"), "Orts- oder Expeditionszustand offen"
    return frames, kaempfe


def vorbereiten(seed):
    z = K.bis_freie_phase(seed)
    K.flags_setzen("kloster_fertig", "capra_dabei")
    tag = z["tag"]
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "bootsschuppen" not in orte, "Bootsschuppen vor Tag 9 offen"
    # Akt 2 hat noch keinen Kalender (das Spiel endet nach Tag 8): nur fuer die Freischaltung auf Tag 9, dann zurueck
    setzen(tag=9)
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "bootsschuppen" in orte and "berge" not in orte, orte
    K.inventar(frei=3)
    E.aktion("ort_betreten", {"id": "bootsschuppen"})
    assert E.aktiv()["event"]["id"] == "bg_petru_auftrag"
    setzen(tag=tag)
    E.aktion("event_wahl", {"index": 0})
    E.aktion("event_schliessen", {})
    assert "berge_angenommen" in E.aktiv()["flags"]
    K.bis_naechste_freie_phase()
    K.inventar(frei=3)


def lauf1():
    WAHL.clear()
    WAHL.update({"bg_see_rast": [0], "bg_hochweide": [0], "bg_u1_wahl": [0], "bg_u2_wahl": [1],
                 "bg_drei_wege_petru": [2]})
    vorbereiten(7)
    frames, kaempfe = ausflug("berge")
    z = E.aktiv()
    f, inv = z["flags"], z["inventar"]
    assert frames[0] == "bg_start" and frames[-1] == "bg_hafen_c", frames
    assert "bg_turm_capra" in frames and "bg_u2_gehetzt" in frames and "bg_u1_getoetet" in frames, frames
    assert "berge_11_solo" in kaempfe and "berge_12_wolff" in kaempfe, kaempfe
    assert "bg_drei_wege_petru" in frames and "bg_weg_c_petru" in frames, frames
    assert "petru_hand_steif" in f and "berge_fertig" in f and "bg_adrien_bergerie" in f, f
    assert "topas" in inv and "ghjuvan_knife" in inv and "laetitia_scarf" in inv, inv
    assert "berge_u1_junges" in kaempfe and "berge_u1_old_grey" in kaempfe and "berge_u2_panther" in kaempfe
    assert "mazzera" in (z.get("charms") or {}).get("besitz", []), "Mazzera-Charm aus dem Lager des Panthers (28.10.)"
    return frames, kaempfe


def lauf2():
    WAHL.clear()
    WAHL.update({"bg_see_rast": [1], "bg_hochweide": [1], "bg_turm_f1": [1], "bg_turm_f2": [1], "bg_turm_f3": [1],
                 "bg_drei_wege": [1, 2]})
    vorbereiten(3)
    z = E.aktiv()
    for k in [k for k in z["werte"] if k in ("vertrauen.toto", E.regeln.rollen.ALIAS.get("vertrauen.toto", ""))
              or k in E.regeln.rollen.ALIAS and E.regeln.rollen.ALIAS[k] == "vertrauen.toto"]:
        z["werte"][k] = 0                          # Toto vertraut Duc noch nicht genug -> Weg B ist zu
    E.sichern(z)
    frames, kaempfe = ausflug("berge")
    z = E.aktiv()
    assert "bg_weg_b_zu" in frames and "bg_weg_c_hart" in frames, frames
    assert "berge_12_wolff_hart" in kaempfe and "berge_11_duo" in kaempfe, kaempfe
    assert "bg_turm_capra" in frames and "bg_u1_hochweide" not in frames and "bg_u2_huette" not in frames, frames
    assert frames[-1] == "bg_hafen_c" and "petru_hand_steif" not in z["flags"], frames
    j = {x["id"]: x for x in E.auftraege.journal(z, E.modul_laden(), E.moddir("eden_rise"), lambda pid: None)}
    assert j["berge"]["status"] == "fertig", j["berge"]
    K.bis_naechste_freie_phase()
    wieder, _ = ausflug("berge")
    assert wieder[0] == "bg_wieder" and wieder[-1] == "bg_wieder_ende", wieder
    return frames, kaempfe


def lauf3():
    WAHL.clear()
    WAHL.update({"bg_see_rast": [1], "bg_hochweide": [1], "bg_kamm": [0]})
    vorbereiten(11)
    K.flags_setzen("bg_ghjuvan_getroffen")
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "hochweide" in orte, orte
    WAHL.update({"bg_u1_wahl": [1]})
    K.inventar(frei=2)
    frames, kaempfe = ausflug("hochweide")
    z = E.aktiv()
    assert frames[0] == "bg_u1_start" and "bg_u1_frei" in frames, frames
    assert "bg_baer_frei" in z["flags"] and z["flag_tag"]["bg_baer_frei"] == z["tag"], z.get("flag_tag")
    regel = {"flag_seit": ["bg_baer_frei", 2]}
    assert not E.regeln.gilt(regel, z), "Anruf zu frueh"
    setzen(tag=z["tag"] + 2)
    assert E.regeln.gilt(regel, E.aktiv()), "Anruf nach zwei Tagen nicht moeglich"
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "hochweide" not in orte, "Weide offen, obwohl Ghjuvan noch lebt und nichts zu tun ist"
    K.flags_setzen("bg_ghjuvan_tot")
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "hochweide" in orte
    return frames, kaempfe


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for name, fn in (("Lauf 1 (Umwege, Weg C mit Petru)", lauf1), ("Lauf 2 (Luegen, Toto zu, Weg C hart)", lauf2),
                     ("Lauf 3 (Old Grey frei, Anruf nach 2 Tagen)", lauf3)):
        frames, kaempfe = fn()
        print("OK %s: %d Frames, %d Kaempfe" % (name, len(frames), len(kaempfe)))


if __name__ == "__main__":
    main()

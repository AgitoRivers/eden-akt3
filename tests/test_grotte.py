# -*- coding: utf-8 -*-
r"""Akt 2 Woche 2 (Duc 27.10.2026): Strand-Grotte mit beiden Umwegen, Kevins Daecher und die spaeten Anrufe ueber die
Engine. Kaempfe werden im Test direkt gewonnen (kampf._finish "ko").

  Lauf 1: Bastien befreit (zu spaet), Matteu die Wahrheit gesagt, Kiste behalten -> Matteu stirbt, Gennaros Haende,
          zwei Tage spaeter der Anruf wegen Gennaro
  Lauf 2: Bastien zurueckgelassen, ohne Matteu, Kiste abgegeben -> Rueckweg an Chloé vorbei, Ring
  Lauf 3: Kevins Daecher -> Seite 40

  python tests\test_grotte.py
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402
import test_kloster as K  # noqa: E402
import test_berge as B  # noqa: E402

E = L.eden
WAHL = B.WAHL


def ausflug(ort, praefix):
    z = E.aktiv()
    start = (z["tag"], z["phase"])
    E.aktion("ort_betreten", {"id": ort})
    frames, kaempfe = [], []
    for _ in range(80):
        z = E.aktiv()
        if z["status"] == "kampf":
            kaempfe.append(z["kampf"]["definition"])
            E.kampf._finish(z, E.modul_laden(), z["kampf"], "ko")
            E.sichern(z)
            E.aktion("kampf_schliessen", {})
            continue
        ev = z.get("event") or {}
        if z["status"] != "ereignis" or not ev.get("id", "").startswith(praefix):
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


def vorbereiten(seed, *flags):
    K.bis_freie_phase(seed)
    K.flags_setzen(*flags)
    K.inventar(frei=4)
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    return orte


def lauf1():
    WAHL.clear()
    WAHL.update({"gr_strand": [0], "gr_u2_wahl": [0], "gr_teich": [0], "gr_u1_wahl": [0], "gr_wahl": [1]})
    orte = vorbereiten(7, "grotte_offen")
    assert "grotte" in orte, orte
    frames, kaempfe = ausflug("grotte", "gr_")
    z = E.aktiv()
    f, inv = z["flags"], z["inventar"]
    assert frames[0] == "gr_start" and frames[-1] == "gr_heim", frames
    assert "gr_u2_frei" in frames and "gr_zelle_spaet" in frames and "gr_boss_matteu_spaet" in frames, frames
    assert "gr_8_riscossore_matteu_spaet" in kaempfe, kaempfe
    assert {"waffe_knife", "gr_matteu_tot", "gr_gennaro_haende", "grotte_fertig"} <= set(f), f
    assert "collar_crate" in inv and "ghjacumu_medal" in inv and "treasure_notes" in inv, inv
    regel = {"flag_seit": ["gr_gennaro_gejagt", 2]}
    assert not E.regeln.gilt(regel, z)
    B.setzen(tag=z["tag"] + 2)
    assert E.regeln.gilt(regel, E.aktiv()), "Anruf wegen Gennaro nach zwei Tagen nicht moeglich"
    return frames, kaempfe


def lauf2():
    WAHL.clear()
    WAHL.update({"gr_strand": [0], "gr_u2_wahl": [1], "gr_teich": [1], "gr_wahl": [0]})
    vorbereiten(3, "grotte_offen")
    frames, kaempfe = ausflug("grotte", "gr_")
    z = E.aktiv()
    assert "gr_rueckweg_bastien" in frames and "gr_zelle" in frames and "gr_u1_start" not in frames, frames
    assert "gr_8_riscossore" in kaempfe, kaempfe
    assert {"gr_bastien_tot", "gr_gennaro_frei", "waffe_knife"} <= set(z["flags"]), z["flags"]
    assert "bastien_ring" in z["inventar"] and "collar_crate" not in z["inventar"], z["inventar"]
    K.bis_naechste_freie_phase()
    K.inventar(frei=2)
    wieder, _ = ausflug("grotte", "gr_")
    assert wieder[0] == "gr_wieder" and wieder[-1] == "gr_wieder_ende", wieder
    return frames, kaempfe


def lauf3():
    WAHL.clear()
    orte = vorbereiten(11, "kevin_jagd")
    assert "kevin" in orte, orte
    frames, kaempfe = ausflug("kevin", "kv_")
    z = E.aktiv()
    assert frames == ["kv_start", "kv_glocke", "kv_nest", "kv_ende", "kv_don"], frames
    assert kaempfe == ["kv_tauben", "kv_kevin"], kaempfe
    assert "lea_chart_page" in z["inventar"] and "kevin_fertig" in z["flags"]
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "kevin" not in orte
    return frames, kaempfe


def lauf4():
    """Flut-Nacht (Duc 28.10.2026): vier Kaempfe, die Sirene, der Saphir; beim zweiten Mal nur noch der Sammel-Lauf."""
    WAHL.clear()
    WAHL.update({"fn_teich": [0], "fn_halle": [1]})
    vorbereiten(5, "grotte_offen", "grotte_fertig")
    B.setzen(tag=12)
    bis_abend()
    orte = [o["id"] for o in E.auftraege.orte_frei(E.aktiv(), E.moddir("eden_rise"))]
    assert "grotte_flut" in orte, orte
    frames, kaempfe = ausflug("grotte_flut", "fn_")
    z = E.aktiv()
    assert frames == ["fn_start", "fn_gang", "fn_galerie", "fn_halle", "fn_teich", "fn_perle", "fn_heim"], frames
    assert kaempfe == ["fn_1_ratten", "fn_2_fledermaeuse", "fn_3_viper", "fn_4_piraten", "fn_5_sirene"], kaempfe
    assert {"sirene_fertig", "sirene_weg"} <= set(z["flags"]) and "saphir" in z["inventar"], (z["flags"], z["inventar"])
    K.inventar(frei=3)
    bis_abend()
    wieder, kaempfe2 = ausflug("grotte_flut", "fn_")
    assert "fn_teich_leer" in wieder and "fn_perle" not in wieder, wieder
    assert len(kaempfe2) == 4, kaempfe2
    return frames, kaempfe


def bis_abend():
    """Bot-Schritte bis zur freien Abendphase (nach der Abendszene, wie im echten Ablauf)."""
    prot = {"schritte": [], "erledigt": {}}
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        if z["status"] == "wahl" and z["phase"] == "abend" and not E.plan.aktionen(z):
            return z
        a = L.schritt(z, prot)
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    raise AssertionError("kein freier Abend")


class _Wuerfel:
    def __init__(self, wert):
        self.wert = wert

    def random(self):
        return self.wert


def regeln():
    """Kampfregeln der Flut-Nacht direkt an der Engine: Sirene unberuehrbar, Vampirin selten, Beute eins aus drei."""
    K.bis_freie_phase(9)
    z, modul = E.aktiv(), E.modul_laden()
    defs = E.kampf.daten(E.moddir("eden_rise"))
    E.kampf.starten(z, defs, "fn_5_sirene")
    g = z["kampf"]["gegner"][0]
    assert g["level"] == E.kampf.progress(z)["level"] + 1, g["level"]
    ctx = {"sp": z["kampf"]["spieler"], "g": g, "rng": L.random, "log": [], "events": [], "k": z["kampf"], "z": z}
    erster = (g["def"].get("untouchable_hinweise") or [{"text": g["def"]["untouchable"]}])[0]["text"]   # 1. Schlag: ihr erster Hinweis
    assert E.kampf._hit(ctx) == 0 and g["lp"] == g["lp_max"] and erster in ctx["log"][-1], ctx["log"]
    g["lp"] -= 5
    E.kampf._unberuehrbar(g)
    assert g["lp"] == g["lp_max"]
    assert "charm" not in g["def"]["immune"], "Reden muss bei der Sirene wirken"
    z.pop("kampf")
    for n, typ in enumerate(["fledermaeuse", "fledermaeuse", "fledermaeuse", "vampirin"]):   # 10 %, 20 %, 30 %, 40 %
        E.kampf.starten(z, defs, "fn_2_fledermaeuse", rng=_Wuerfel(0.35))
        assert z["kampf"]["gegner"][0]["typ"] == typ, (n, z["kampf"]["gegner"][0]["typ"])
        z.pop("kampf")
    assert z["selten_zaehler"]["fn_2_fledermaeuse"] == 0, "nach der Vampirin wieder bei 10 %"
    E.kampf.starten(z, defs, "fn_2_fledermaeuse", rng=_Wuerfel(0.15))
    assert z["kampf"]["gegner"][0]["typ"] == "fledermaeuse"
    z.pop("kampf")
    z["selten_zaehler"]["fn_2_fledermaeuse"] = 0
    E.kampf.starten(z, defs, "fn_2_fledermaeuse", rng=_Wuerfel(0.05))
    g = z["kampf"]["gegner"][0]
    assert g["typ"] == "vampirin" and g["level"] == min(10, E.kampf.progress(z)["level"] + 2), g
    arten = set()
    for i in range(30):
        L.random.seed(i)
        z["kampf"] = {"ergebnis": {"art": "ko", "zeilen": []}, "gegner": [{"typ": "vampirin"}], "def": {}}
        vorher = (z.get("konto", 0), len(z.get("inventar", [])))
        r = E.kampf.chip_drop_anwenden(z, defs)
        arten.add(r["art"] if r["art"] in ("geld", "material") else "chip")
        nachher = (z.get("konto", 0), len(z.get("inventar", [])))
        assert r["art"] != "material" or nachher[1] == vorher[1] + 1
        assert E.kampf.chip_drop_anwenden(z, defs) is None, "nur eine Beute je Kampf"
    assert arten == {"geld", "material", "chip"}, arten
    z.pop("kampf")
    return [], []


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for name, fn in (("Lauf 1 (Bastien befreit, Matteu Wahrheit, Kiste behalten)", lauf1),
                     ("Lauf 2 (Bastien zurueckgelassen, Kiste abgegeben, Wiederkommen)", lauf2),
                     ("Lauf 3 (Kevins Daecher)", lauf3),
                     ("Lauf 4 (Flut-Nacht: Sirene, Saphir, Sammel-Lauf)", lauf4),
                     ("Regeln (Sirene unberuehrbar, Vampirin 10 %, Beute eins aus drei)", regeln)):
        frames, kaempfe = fn()
        print("OK %s: %d Frames, %d Kaempfe" % (name, len(frames), len(kaempfe)))


if __name__ == "__main__":
    main()

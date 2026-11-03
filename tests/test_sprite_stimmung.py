# -*- coding: utf-8 -*-
"""Sprite passt zur Lage (STIL-Regel, Duc 29.10.2026): In ernsten Events keine flirtenden oder romantischen Gefuehle
(desire, love) und Ueberdrehtes (joy, excitement, amusement) nur als bewusst freigegebener trockener Scherz.
Dazu der Sturm: wer ruhen soll, reagiert ohne Schock-Pose. Neue Treffer sind entweder ein Fehler oder gehoeren
nach Pruefung in FREI.

  python tests\\test_sprite_stimmung.py
"""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
NIE = {"desire", "love"}
NUR_FREI = {"joy", "excitement", "amusement"}
# (event, sprecher, gefuehl): bewusste leichte Momente in ernsten Events, geprueft 29.10.2026
FREI = {
    ("gv_megan_chiara", "megan", "amusement"), ("gv_dienstplan", "lea", "joy"), ("gv_ruhetag", "lea", "excitement"),
    ("gv_ruhetag", "rosi", "amusement"), ("auf_herkunft", "lola", "amusement"), ("t0_holm", "holm", "amusement"),
    ("hk_hilfe", "toto", "amusement"), ("yk_herkunft", "yamamoto", "amusement"), ("hy_siri_caption", "yasin", "excitement"),
    ("br_jana_tender", "jana", "excitement"), ("g1_lea_nachttauchen", "lea", "joy"),
    ("g1_lea_nachttauchen", "elsa", "amusement"), ("bg_bergerie", "adrien", "amusement"), ("a2_logo", "megan", "amusement"),
    ("a2_vogelfoto", "yamamoto", "joy"), ("a2_koordinaten", "lea", "excitement"),
    ("gr_boss", "riscossore", "amusement"), ("gr_boss_spaet", "riscossore", "amusement"),     # Drohung mit Laecheln
    ("bl_ab_sophia", "sophia", "amusement"), ("bl_ab_alva", "alva", "amusement"), ("bl_ab_alva", "alva", "joy"),   # trockener Trost mitten in der Belagerung
    ("fn_teich", "sirene", "amusement"), ("fn_perle", "sirene", "amusement"),               # die Sirene neckt
    # geprueft 02.11.2026: Rosis trockener Rat nach dem Kampf, Wolff spottet ueber die eigene Waffe, Alons Buehnen-
    # laecheln ist die Luege selbst (wie beim Riscossore)
    ("hk_tipp_ratten", "rosi", "amusement"), ("hk_tipp_hunde", "rosi", "amusement"), ("hk_tipp_keiler", "rosi", "amusement"),
    ("bg_turm_parole_2", "wolff", "amusement"), ("bl_cliff_alon", "alon", "joy"), ("bl_cliff_alon_siri", "alon", "joy"),
    ("bl_cliff_alon_siri", "alon", "amusement"), ("bl_cliff_team", "alon", "joy"),
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ev = json.load(open(os.path.join(BASE, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]
    fehler, n = [], 0
    for e in ev:
        if e.get("ton") != "ernst":
            continue
        zeilen = list(e.get("zeilen", [])) + [o["zeile"] for o in e.get("optionen", []) if isinstance(o.get("zeile"), dict)]
        for z in zeilen:
            n += 1
            g = z.get("gefuehl")
            if g in NIE or (g in NUR_FREI and (e["id"], z.get("wer"), g) not in FREI):
                fehler.append("%s: %s %s" % (e["id"], z.get("wer"), g))
    if fehler:
        raise AssertionError("Unpassendes Gefuehl in ernsten Events:\n  " + "\n  ".join(fehler))
    print("OK %d Zeilen in ernsten Events passen zur Lage" % n)
    from kern import sturm
    import inspect
    quelle = inspect.getsource(sturm)
    assert 'key="st.ruhe." + p, gefuehl="surprise"' not in quelle and all(g != "surprise" for g in sturm.RUHE_GEFUEHL.values()), \
        "Sturm: Ruhen-Zeilen ohne Schock-Pose"
    print("OK Sturm: wer ruhen soll, reagiert ohne Schock-Pose")

    # Stimmungsrahmen (29.10.2026): die Krisen-, Abschieds- und Anhoerungsszenen grenzen das Gefuehl des Richters ein
    bu = json.load(open(os.path.join(BASE, "module", "eden_rise", "buehne.json"), encoding="utf-8"))["szenen"]
    from kern import buehne, szene
    PFLICHT = ("cold_open", "explosion", "holm_abschied", "sturmvorbereitung", "sturmnacht", "anhoerung", "anhoerung_rolle")
    for sid in PFLICHT:
        r = (bu[sid].get("stimmung") or {}).get("erlaubt") or []
        assert r and set(r) <= set(buehne.GEFUEHLE), "%s: Stimmungsrahmen fehlt oder enthaelt Unbekanntes" % sid
        assert not set(r) & {"desire", "love", "amusement", "joy", "excitement"}, "%s: Rahmen erlaubt Unpassendes" % sid
    print("OK %d Krisenszenen haben einen Stimmungsrahmen ohne Flirt und Jubel" % len(PFLICHT))
    sz = {"def": {"stimmung": bu["cold_open"]["stimmung"]}}
    assert szene.erlaubte_gefuehle(sz) == bu["cold_open"]["stimmung"]["erlaubt"]
    assert szene.im_rahmen(sz, "joy") in bu["cold_open"]["stimmung"]["erlaubt"] and szene.im_rahmen(sz, "fear") == "fear"
    assert szene.erlaubte_gefuehle({"def": {}}) == buehne.GEFUEHLE                       # lockere Szenen bleiben frei
    print("OK Richter waehlt im Rahmen, eingefuegte Zeilen werden in den Rahmen geholt, lockere Szenen frei")
    print("OK")


if __name__ == "__main__":
    main()

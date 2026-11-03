# -*- coding: utf-8 -*-
r"""Hafenkampf als Ortskette (26.10.2026, Duc): Bot-Lauf durch Tag 2 - alle Frames in Reihenfolge, je Welle eine Rettung,
Nachbetrachtung, Ziege; danach ab Tag 4 Casanovas Buero als Ort, das den Kloster-Auftrag vergibt.

  python tests\test_hafen.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
KETTE = ["hk_hilfe", "hk_rosi_?", "hk_petru", "hk_welle2", "hk_alva", "hk_welle3", "hk_casanova", "hk_abend", "hk_pascal", "hk_ziege"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_hafen_"), 7)
    L.random.seed(7)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    frames, buero = [], None
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        ev = (z.get("event") or {}).get("id")
        if ev and ev.startswith("hk_") and (not frames or frames[-1] != ev):
            frames.append(ev)
            if ev != "hk_hilfe":
                assert z.get("ort_aktiv") == "hafen", "Frame %s ausserhalb der Ortskette" % ev
        if z["status"] == "wahl" and z["tag"] >= 4 and z["phase"] in ("tag", "nachmittag") and not E.plan.aktionen(z):
            buero = [o["id"] for o in E.auftraege.orte_frei(z, E.moddir(z["modul"]))]
            break
        a = L.schritt(z, prot)
        assert a is not None, "Bot-Lauf endete vor Tag 4"
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    soll = [f.replace("?", frames[1][-1]) for f in KETTE]
    assert frames == soll, frames
    f = z["flags"]
    for fl in ("waffe_bat", "hafen_ratten_weg", "hafen_hunde_weg", "hafen_keiler_weg", "kloster_faden"):
        assert fl in f, fl
    for pid in ("petru", "alva", "casanova", "elsa"):
        assert any(x.startswith("dorf_%s_" % pid) for x in f), "keine Kennenlern-Wahl fuer %s" % pid
    assert "rathaus" in (buero or []), "Casanovas Buero ab Tag 4 nicht offen: %s" % buero
    # Buero besuchen und annehmen -> Macchia offen
    E.aktion("ort_betreten", {"id": "rathaus"})
    assert E.aktiv()["event"]["id"] == "kl_casanova_auftrag"
    E.aktion("event_wahl", {"index": 0})
    E.aktion("event_schliessen", {})
    for frame in ("kl_pascal_tuer", "kl_mina_post"):       # danach Pascal im Flur und Mina mit der Post (Duc 30.10.2026)
        assert E.aktiv()["event"]["id"] == frame, E.aktiv().get("event")
        E.aktion("event_wahl", {"index": 0})
        E.aktion("event_schliessen", {})
    z = E.aktiv()
    assert "kl_post" in z["inventar"]
    assert "kloster_angenommen" in z["flags"] and not z.get("ort_aktiv")
    print("OK Hafen: %s · Büro an Tag %d, Auftrag angenommen" % (" > ".join(frames), z["tag"]))


if __name__ == "__main__":
    main()

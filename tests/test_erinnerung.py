# -*- coding: utf-8 -*-
"""Erinnerungen der Auftraggeberinnen (Duc 02.11.2026): Bedingung ort_ruhe, eine Sprachnachricht am Tag, einmal je Durchlauf."""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from kern import auftraege, ereignisse, regeln

MODDIR = os.path.join(BASE, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MODDIR, "modul.json"), encoding="utf-8"))


def z(tag=12, flags=(), offen=None, zuletzt=None):
    return {"id": "t", "tag": tag, "phase": "fruehstueck", "flags": list(flags), "werte": {}, "punkte": {},
            "persona": {"id": "first_officer", "attribute": {}}, "inventar": [], "truhe": [], "chronik": [],
            "ort_offen_seit": dict(offen or {}), "ort_zuletzt": dict(zuletzt or {})}


def test_ort_ruhe():
    b = {"ort_ruhe": ["macchia", 3]}
    assert not regeln.gilt(b, z(12))                                          # Ort nie offen gewesen
    assert not regeln.gilt(b, z(10, offen={"macchia": 8}))                    # erst 2 Tage offen
    assert regeln.gilt(b, z(11, offen={"macchia": 8}))                        # 3 Tage offen, nie dort
    assert not regeln.gilt(b, z(11, offen={"macchia": 8}, zuletzt={"macchia": 10}))
    assert regeln.gilt(b, z(13, offen={"macchia": 8}, zuletzt={"macchia": 10}))


def test_tagesbeginn_merkt_ersten_offenen_tag():
    s = z(8, flags=["kloster_angenommen"])
    auftraege.tagesbeginn(s, MODDIR)
    assert s["ort_offen_seit"]["macchia"] == 8
    s["tag"] = 9
    auftraege.tagesbeginn(s, MODDIR)
    assert s["ort_offen_seit"]["macchia"] == 8                                # bleibt der erste Tag


def erinnerungen(s):
    """Alle Pflicht-Events dieses Morgens ziehen (andere Pflicht-Events duerfen dazwischen kommen) -> nur die er_-IDs."""
    out = []
    while True:
        ev = ereignisse.pflicht_ziehen(s, MODUL, MODDIR)
        if not ev:
            return out
        if ev["id"].startswith("er_"):
            out.append(ev["id"])


def test_hoechstens_eine_erinnerung_am_tag_und_jede_nur_einmal():
    flags = ["kloster_angenommen", "grotte_offen", "berge_angenommen"]
    s = z(13, flags=flags, offen={"macchia": 8, "grotte": 9, "berge": 9})
    s["ev"] = {"gesehen": [], "heute": {}, "tag": 13}
    erste = erinnerungen(s)
    assert len(erste) == 1, erste                                             # drei faellig, nur eine am Morgen
    s["tag"] = 14
    zweite = erinnerungen(s)
    assert len(zweite) == 1 and zweite != erste, zweite


def test_fertiger_auftrag_erinnert_nicht():
    s = z(13, flags=["kloster_angenommen", "kloster_fertig"], offen={"macchia": 8})
    s["ev"] = {"gesehen": [], "heute": {}, "tag": 13}
    assert "er_kloster" not in erinnerungen(s)


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("OK", name)

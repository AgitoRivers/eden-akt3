# -*- coding: utf-8 -*-
r"""Bibis Ende und Julien (Duc 05.11.2026, docs/brain_trust/BIBI_ENDE.md), durch die echte Engine:
Tag 35 Nachmittag, die Tore. Julien kommt mit ARKs Delegation, Kampf. Sieg: a3_julien_sieg. Niederlage: a3_julien_tiere
(Bibi oeffnet die Tore auf die Agenten). Danach die Abschiede der Tiere (Madame bleibt), mo_frei_ende, und mit Bibis
Romanze gleich "Last Page" mit der Frage "Will you come back?". Ohne eden-config.json (wie tests/bot_akt3.py)."""
import json, os, random, sys, tempfile, shutil

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import bot_akt3 as B  # noqa: E402
eden = B.eden
L = B.L

FLAGS = ["rt_bibi_bleibt", "mochis_offen", "mo_tier_da", "mo_tier_madame", "mo_tier_hund", "mo_tier_geier", "kl_loewe_frei",
         "rt_ausgang_alle"]


def lauf(sieg, romanze):
    ordner = tempfile.mkdtemp(prefix="eden_julien_")
    try:
        B.vorbereiten(ordner, 3)
        rnd = random.Random(3)
        z = B.akt3_stand("wenig_kaputt", rnd)
        z["flags"] = sorted(set(z["flags"]) | set(FLAGS) | ({"rm_b3"} if romanze else set()))
        z["tag"], z["phase"] = 35, "nachmittag"
        z.setdefault("flag_tag", {})["rm_b3"] = 20
        if romanze:
            for k in ("vertrauen.bibi", "begehren.bibi"):      # Stufe 5 ueber die Punkte (kern/zustand: Stufe aus Punkten)
                z["werte"][k] = 5
                z.setdefault("punkte", {})[k] = eden.zustand.STUFEN_AB[5]
        z["heute"], z["optionen"], z["meldungen"] = [], [], []
        modul = eden.modul_laden(z.get("modul"))
        assert eden.plan.plan_laden(z, modul, eden.moddir(z["modul"]))
        z["phase"] = "nachmittag"
        eden.weiter(z, modul, eden.plan.phase_beginnen(z))
        eden.sichern(z)
        z = eden.aktiv()
        gesehen, protokoll = [], {"schritte": [], "erledigt": {"t35": True}}
        for _ in range(400):
            if z["status"] == "ereignis" and z.get("event") and not z["event"].get("ergebnis"):
                if not gesehen or gesehen[-1] != z["event"]["id"]:
                    gesehen.append(z["event"]["id"])
                opts = eden.ereignisse.daten(eden.moddir())["_index"][z["event"]["id"]]["optionen"]
                L.versuch(("event_wahl", {"index": len(opts) - 1}), protokoll)
            elif z["status"] == "ereignis":
                L.versuch(("event_schliessen", {}), protokoll)
            elif z["status"] == "kampf":
                k = z["kampf"]
                if k["phase"] == "ende":
                    L.versuch(("kampf_schliessen", {}), protokoll)
                    gesehen.append("kampf:" + str((k.get("ergebnis") or {}).get("art")))
                else:
                    if sieg:
                        for g in k["gegner"]:
                            g["lp"] = min(g["lp"], 1)
                        k["spieler"]["lp"] = k["spieler"]["lp_max"]
                    else:
                        k["spieler"]["lp"] = 1
                    eden.sichern(z)
                    if k["phase"] == "parade":
                        L.versuch(("kampf_parade", {"ergebnis": "perfekt" if sieg else "verfehlt", "revision": k["revision"]}), protokoll)
                        if (z.get("kampf") or {}).get("phase") == "parade":
                            L.versuch(("kampf_parade", {"ergebnis": "ausweichen" if sieg else "verfehlt", "revision": k["revision"]}), protokoll)
                    else:
                        lebend = [i for i, g in enumerate(k["gegner"]) if g["lp"] > 0]
                        L.versuch(("kampf_zug", {"befehl": "angriff" if sieg else "verteidigen", "ziel": None,
                                                 "gegner": lebend[0] if lebend else None, "revision": k["revision"]}), protokoll)
            else:
                break
            z = eden.aktiv()
        return gesehen, z["flags"], z
    finally:
        eden.modul_laden = getattr(eden.modul_laden, "__wrapped__", eden.modul_laden)
        shutil.rmtree(ordner, ignore_errors=True)


def main():
    for sieg, romanze in ((True, True), (False, False)):
        gesehen, flags, _z = lauf(sieg, romanze)
        print("Sieg" if sieg else "Niederlage", "mit Romanze" if romanze else "ohne Romanze", ":", " > ".join(gesehen))
        assert gesehen[:2] == ["mo_frei_start", "a3_julien"], gesehen
        assert ("kampf:ko" in gesehen or "kampf:aufgabe" in gesehen or "kampf:entkommen" in gesehen) if sieg else "kampf:niederlage" in gesehen, gesehen
        nach = "a3_julien_sieg" if sieg else "a3_julien_tiere"
        assert nach in gesehen and gesehen.index(nach) > gesehen.index("a3_julien"), gesehen
        assert "a3_julien_weg" in flags and "a3_julien_ende" in flags
        assert "mo_frei_madame" in gesehen and "mo_madame_bleibt" in flags, "Madame bleibt"
        assert "mo_frei_ende" in gesehen and "mo_freigelassen" in flags
        if romanze:
            for eid in ("rm_b4", "rm_b4_b", "rm_b4_frage", "rm_b4_c"):
                assert eid in gesehen, (eid, gesehen)
            assert any(f.startswith("a3_bibi_antwort_") for f in flags)
        else:
            assert "rm_b4" not in gesehen
    # Ende: Bibis Bild im Schluss
    from kern import abschluss
    t = abschluss.BIBI_BILD(["a3_bibi_antwort_ehrlich", "a3_julien_weg"])
    assert "postcard" in t and "never comes back" in t
    print("ok test_akt3_julien")


if __name__ == "__main__":
    main()

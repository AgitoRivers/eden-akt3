# -*- coding: utf-8 -*-
r"""Ortskapitel Kloster (26.10.2026, E-073/E-074): die Frame-Kette ueber die Engine, beide Wege der Gabelung und das
Wiederkommen. Kaempfe werden im Test direkt gewonnen (kampf._finish "ko").

  Faehrte + Loewe erloesen  -> Frederico lebt, Steuerchip, Le Large, Auftrag fertig, Phase verbraucht
  Schatz  + Chip schneiden  -> Spur-Uhr laeuft ab, Frederico tot, Stahlplatte + Zettel
  Wiederkommen              -> Felsnische (leer bzw. Fund), danach ist die Phase wieder verbraucht

  python tests\test_kloster.py
"""
import os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
WAHL = {"kl_gabelung": None, "kl_loewe_wahl": None, "kl_wieder": None}      # je Lauf gesetzt, sonst Option 0


def bis_freie_phase(seed):
    """Bot-Lauf bis zur ersten freien Mittags-/Nachmittagsphase ab Tag 2."""
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_kloster_"), seed)
    L.random.seed(seed)
    prot = {"schritte": [], "erledigt": {}}
    z = E.aktion("neu", {"modus": "ironman"})
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        if z["status"] == "wahl" and z["tag"] >= 2 and z["phase"] in ("tag", "nachmittag") and not E.plan.aktionen(z):
            return z
        a = L.schritt(z, prot)
        assert a is not None, "Bot-Lauf endete ohne freie Phase"
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    raise AssertionError("keine freie Phase gefunden")


def flags_setzen(*flags):
    z = E.aktiv()
    z["flags"] += [f for f in flags if f not in z["flags"]]
    E.sichern(z)


def ausflug(ort="macchia"):
    """Ort betreten und die Kette bis zum Ende spielen -> besuchte Frame-IDs."""
    z = E.aktiv()
    start = (z["tag"], z["phase"])
    E.aktion("ort_betreten", {"id": ort})
    frames = []
    for _ in range(80):
        z = E.aktiv()
        if z["status"] == "kampf":
            assert z.get("expedition"), "Kampf im Kloster ohne laufende Expedition"
            E.kampf._finish(z, E.modul_laden(), z["kampf"], "ko")
            E.sichern(z)
            E.aktion("kampf_schliessen", {})
            continue
        ev = z.get("event") or {}
        if z["status"] != "ereignis" or not ev.get("id", "").startswith("kl_"):
            break
        frames.append(ev["id"])
        if ev["id"] == "kl_huette":                  # Rastplatz (Kampf 5c64589): rasten geht, ein Anruf kann kommen
            E.aktion("ort_rasten", {})
            if E.aktiv().get("rast_anruf"):
                E.aktion("rast_antwort", {"index": 0})
        if ev["id"] in ("kl_lager", "kl_frederico", "kl_frederico_tot"):     # Sperre: kein Weg zurueck zur Entscheidung
            try:
                E.aktion("ort_zurueck", {})
                raise AssertionError("Rueckweg hinter %s war offen" % ev["id"])
            except ValueError:
                pass
        E.aktion("event_wahl", {"index": WAHL.get(ev["id"]) or 0})
        E.aktion("event_schliessen", {})
    z = E.aktiv()
    assert (z["tag"], z["phase"]) != start, "Ausflug hat die Phase nicht verbraucht"
    assert not z.get("ort_aktiv") and not z.get("ev_weiter"), "Ortszustand nicht aufgeraeumt"
    assert not z.get("expedition"), "Expedition nach dem Ausflug noch offen"
    return frames


def bis_naechste_freie_phase():
    prot = {"schritte": [], "erledigt": {}}
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        if z["status"] == "wahl" and z["phase"] in ("tag", "nachmittag") and not E.plan.aktionen(z):
            return z
        a = L.schritt(z, prot)
        assert a is not None
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    raise AssertionError("keine freie Phase mehr")


def inventar(frei):
    """Test: Inventar auf genau frei freie Plaetze bringen (Andenken, Quest-Gegenstaende und Schluessel zaehlen nicht)."""
    z = E.aktiv()
    m = E.modul_laden()
    zaehlt = [i for i in z["inventar"] if m["items"].get(i, {}).get("art") not in E.zustand.OHNE_PLATZ]
    fueller = [i for i, it in m["items"].items() if it.get("art") == "material" and i != "steel_plate"]
    while len(zaehlt) > E.zustand.inventar_plaetze(z, m) - frei:
        z["inventar"].remove(zaehlt.pop())
    while len(zaehlt) < E.zustand.inventar_plaetze(z, m) - frei:
        i = next(x for x in fueller if x not in z["inventar"])
        z["inventar"].append(i)
        zaehlt.append(i)
    E.sichern(z)


def journal():
    z = E.aktiv()
    return {j["id"]: j for j in E.auftraege.journal(z, E.modul_laden(), E.moddir(z["modul"]), lambda pid: None)}


def lauf(seed, faehrte):
    WAHL.update({"kl_gabelung": 0 if faehrte else 1, "kl_loewe_wahl": 0 if faehrte else 1, "kl_wieder": 1})
    z = bis_freie_phase(seed)
    orte = [o["id"] for o in E.auftraege.orte_frei(z, E.moddir(z["modul"]))]
    assert "macchia" not in orte, "Macchia offen ohne angenommenen Auftrag"
    flags_setzen("kloster_angenommen")
    assert journal()["kloster"]["status"] == "aktiv"
    inventar(frei=2)
    frames = ausflug()
    z = E.aktiv()
    f, inv = z["flags"], z["inventar"]
    assert frames[0] == "kl_start" and frames[-1] in ("kl_mina_fragt", "kl_mina_fragt_tot"), frames
    assert "control_chip" in inv and "waffe_spear" in f and "kloster_fertig" in f, (f, inv)
    assert "elicriso" in E.kampf.known(z), "Nonna hat Elicriso nicht beigebracht"
    assert not (z.get("spur_uhren") or {}).get("kloster"), "Spur-Uhr nach dem Kapitel noch sichtbar"
    j = journal()["kloster"]
    assert j["status"] == "fertig" and all(s["erledigt"] for s in j["schritte"]), j
    assert all(g["entschieden"] for g in j["grau"]), j["grau"]
    assert any("Auftrag abgeschlossen" in x for m in z["meldungen"] for x in m.get("folgen", [])), "keine Abschluss-Meldung"
    if faehrte:
        assert "kloster_frederico_lebt" in f and "ambrosius_keule" in inv and "kl_nische" not in frames, frames
        assert "kl_loewe_erloest" in f
    else:
        assert "kloster_frederico_tot" in f and "steel_plate" in inv and "agent_note" in inv, (f, inv)
        assert "kl_loewe_frei" in f and "spur_kloster_abgelaufen" in f
    # Wiederkommen: Felsnische nachholen - mit voller Tasche bleibt die Platte liegen und wartet
    if faehrte:
        bis_naechste_freie_phase()
        inventar(frei=0)
        voll = ausflug()
        assert "kl_nische_voll" in voll and "steel_plate" not in E.aktiv()["inventar"], voll
        assert "kl_nische_geleert" not in E.aktiv()["flags"]
    bis_naechste_freie_phase()
    inventar(frei=1)
    wieder = ausflug()
    z = E.aktiv()
    assert wieder[0] == "kl_wieder" and wieder[-1] == "kl_wieder_ende", wieder
    assert ("kl_nische_eingepackt" in wieder) == faehrte and ("kl_nische_leer" in wieder) != faehrte, wieder
    assert "steel_plate" in z["inventar"] and "kl_nische_geleert" in z["flags"]
    return frames, wieder


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for seed, faehrte in ((7, True), (3, False)):
        frames, wieder = lauf(seed, faehrte)
        print("OK %s: %d Frames (%s), Wiederkommen %s" % ("Faehrte" if faehrte else "Schatz", len(frames),
                                                          " > ".join(frames), " > ".join(wieder)))


if __name__ == "__main__":
    main()

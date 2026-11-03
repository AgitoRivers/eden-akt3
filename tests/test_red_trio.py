# -*- coding: utf-8 -*-
r"""Nebenquest Red Trio, Geruest (30.10.2026, Wiki welt/nebenquest_red_trio.md): die Kette ueber die Engine. Kaempfe werden
direkt beendet (kampf._finish).

  Ohne Platte oder nach Tag 14    -> kein Start, Macchia wie bisher
  Mit Platte, Kampf per ko        -> eigener Satz; per Reden -> anderer Satz
  Niederlage                      -> Story bleibt stehen, naechster Besuch wieder derselbe Kampf
  Jede Kombination der drei Wahlen -> beide Ausgaenge erreichbar, Jacke, red_trio_fertig
  Platte verbaut / in der Truhe   -> je Danzels Satz; Loewe frei / erloest -> je Bibis Satz
  Long Table, alle Pfade ohne Engine -> nur 5x schweigen oder 5x einmischen reisst; jede Option hat ihr Ziel
  Long Table ueber die Engine        -> Riss, Neustart ohne Altlasten, Vertrauen 1-3, Ausgang
  Folgen                             -> versoehnt Elsa, Eroeffnung und drei Bar-Events (ein Satz je Stufe), Ruf steigt; getrennt Elsa und drei Postkarten

  python tests\test_red_trio.py
"""
import itertools, json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
NICHTS = "Says nothing."
FLAGS = ["kloster_angenommen", "kloster_fertig", "grotte_fertig", "kl_nische_geleert", "kl_loewe_frei"]


def start(flags=FLAGS, tag=12):
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_rt_"), 7)
    L.random.seed(7)
    z = E.aktion("neu", {"modus": "ironman"})
    prot = {"schritte": [], "erledigt": {}}
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        if z["status"] == "wahl" and z["tag"] >= 2 and z["phase"] in ("tag", "nachmittag") and not E.plan.aktionen(z):
            break
        a = L.schritt(z, prot)
        assert a is not None
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    z = E.aktiv()
    z["tag"] = tag
    z["flags"] += [f for f in flags if f not in z["flags"]]
    E.sichern(z)


def freie_phase():
    """Sperrt den naechsten Ausflug nicht: Phase ohne Tageslauf zuruecksetzen."""
    z = E.aktiv()
    z["phase"] = "tag"
    z["status"] = "wahl"
    E.sichern(z)


def ausflug(wahl=None, ende="ko", bis=None):
    """Macchia betreten, Kette spielen -> besuchte Frames. wahl: {frame: index}, ende: Kampfausgang (Name oder {bid: Name})."""
    wahl = wahl or {}
    freie_phase()
    E.aktion("ort_betreten", {"id": "macchia"})
    frames = []
    for _ in range(80):
        z = E.aktiv()
        if z["status"] == "kampf":
            k = z["kampf"]
            art = ende.get(k["def"].get("id") or k.get("id"), "ko") if isinstance(ende, dict) else ende
            E.kampf._finish(z, E.modul_laden(), k, art)
            E.sichern(z)
            E.aktion("kampf_schliessen", {})
            continue
        ev = z.get("event") or {}
        if z["status"] != "ereignis" or not ev.get("id", "").startswith(("rt_", "kl_")):
            break
        frames.append(ev["id"])
        if bis and ev["id"] == bis:
            return frames
        E.aktion("event_wahl", {"index": wahl(ev["id"]) if callable(wahl) else wahl.get(ev["id"], 0)})
        E.aktion("event_schliessen", {})
    return frames


def einstieg_gesperrt():
    for flags, tag, warum in ((["kloster_angenommen", "kloster_fertig", "grotte_fertig"], 12, "ohne Platte"), (FLAGS, 15, "nach Tag 14")):
        start(flags, tag)
        f = ausflug(bis="kl_wieder")
        assert f[0] == "kl_wieder", (warum, f)
    print("ok  kein Start ohne Platte / nach Tag 14")


def saetze_je_ausgang():
    start()
    f = ausflug(ende="ko", bis="rt_plan_rouge")
    assert "rt_flucht_ko" in f and "rt_bruecke_ko" in f and "rt_platte_truhe" in f, f
    start()
    f = ausflug(ende="aufgabe", bis="rt_plan_rouge")
    assert "rt_flucht_geredet" in f and "rt_bruecke_geredet" in f, f
    start()
    z = E.aktiv()
    E.kampf.werkstatt(z)["stufen"]["armor:jacket_earth"] = 1
    E.sichern(z)
    f = ausflug(bis="rt_plan_rouge")
    assert "rt_platte_verbaut" in f, f
    print("ok  eigener Satz je Kampfausgang, Platte in Truhe / verbaut")


def niederlage_haelt_an():
    start()
    f = ausflug(ende="niederlage")
    z = E.aktiv()
    assert f == ["rt_auftritt"] and "rt_1_sieg" not in z["flags"], f
    assert not z.get("expedition"), "Expedition nach Niederlage noch offen"
    f = ausflug(bis="rt_auftritt")
    assert f == ["rt_auftritt"], f
    print("ok  Niederlage: naechster Besuch wieder der Kampf")


def alle_wege():
    for loewe in ("kl_loewe_frei", "kl_loewe_erloest"):
        for d, b, c in itertools.product((0, 1), repeat=3):
            for tisch in (0, 1):
                start(FLAGS[:4] + [loewe])
                w = {"rt_danzel": d, "rt_bibi_frei": b, "rt_bibi_erloest": b, "rt_charly": c, "rt_t_bruch": 1, "rt_t_d2": 1, "rt_t_dc": 1}
                if tisch:                                      # immer schweigen -> Riss -> damit leben
                    w.update(still_wahlen())
                f = ausflug(w)
                assert f[-1] == "rt_plan_rouge", f
                pfade = 0
                while "rt_drei_gefunden" not in f:
                    f = ausflug(w)
                    pfade += 1
                    assert pfade <= 3, f
                f = ausflug(w)
                assert f[0] == "rt_ankunft", f
                z = E.aktiv()
                assert "red_trio_fertig" in z["flags"] and "jacke_jacket_fire" in z["flags"], f
                assert ("rt_ausgang_alle" in z["flags"]) == (tisch == 0), f
                assert not tisch or not {"mochis_offen", "rt_charly_bleibt", "rt_bibi_bleibt"} & set(z["flags"]), f
                assert "rt_white_agenten" in z["flags"], f
                assert not z.get("expedition"), "Expedition offen"
                assert ("rt_abschied_frei" if loewe == "kl_loewe_frei" else "rt_abschied_erloest") in f, f
                assert ("rt_was_nun" in f) == (tisch == 0), f
    print("ok  8 Wahl-Kombinationen x 2 Ausgaenge x 2 Loewen")


def tisch_frames():
    d = json.load(open(os.path.join(os.path.dirname(HIER), "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
    liste = d["events"]
    return {e["id"]: e for e in liste if e["id"] == "rt_tisch" or e["id"].startswith("rt_t_")}


def still_wahlen():
    """Frame -> Index der Option, die als Schweigen zaehlt."""
    return {i: next(n for n, o in enumerate(e["optionen"]) if any(f.get("flag", "").startswith("rt_t_still_") for f in o["folgen"]))
            for i, e in tisch_frames().items() if any(f.get("flag", "").startswith("rt_t_still_") for o in e["optionen"] for f in o["folgen"])}


def tisch_pfade():
    """Alle Pfade durch den Tisch, ohne Engine: Regeln wie im Spiel, jede Wahl in jeder Ausgangslage."""
    fr = tisch_frames()
    from kern import regeln
    enden = []

    def lauf(eid, flags):
        for o in fr[eid]["optionen"]:
            fl = set(flags)
            ziel = None
            for f in o["folgen"]:
                if "flag" in f:
                    fl.add(f["flag"])
                ziel = f.get("weiter", ziel)
            z = {"flags": sorted(fl), "werte": {}, "uhren": {}, "inventar": [], "tag": 12}
            if isinstance(ziel, list):
                ziel = next(x["id"] for x in ziel if regeln.gilt(x.get("wenn"), z))
            if eid == "rt_t_bruch":
                enden.append((eid, fl))
                return
            if ziel == "rt_white":
                enden.append((eid, fl))
            else:
                assert ziel in fr, (eid, ziel)
                lauf(ziel, fl)
    for wahlen in itertools.product(("rt_notiz_gesteht", "rt_notiz_kuendigung"), ("rt_notiz_spiel", "rt_notiz_mutter"),
                                    (("rt_notiz_wahrheit", "rt_duc_ehrlich"), ("rt_notiz_futter",)),
                                    ("kl_loewe_frei", "kl_loewe_erloest"), ("kloster_frederico_lebt", "kloster_frederico_tot")):
        lauf("rt_tisch", [x for w in wahlen for x in ((w,) if isinstance(w, str) else w)])
    return enden


def tisch_regeln():
    enden = tisch_pfade()
    stufen = {"danzel": {1: 0, 2: 0, 3: 0}, "bibi": {1: 0, 2: 0, 3: 0}, "charly": {1: 0, 2: 0, 3: 0}}
    gehalten = gerissen = 0
    for eid, fl in enden:
        still = sum(1 for f in fl if f.startswith("rt_t_still_"))
        rein = sum(1 for f in fl if f.startswith("rt_t_rein_"))
        assert still + rein in (5, 6), (still, rein)
        if eid == "rt_t_haelt":
            gehalten += 1
            assert still < 5 and rein < 5, (still, rein)
            for p in stufen:
                s = sum(1 for f in fl if f.startswith("rt_t_plus_%s_" % p)) - sum(1 for f in fl if f.startswith("rt_t_minus_%s_" % p))
                stufen[p][3 if s >= 2 else 1 if s <= -1 else 2] += 1
        else:
            assert eid == "rt_t_bruch" and (still >= 5 or rein >= 5), (eid, still, rein)
            gerissen += 1
    assert gehalten > gerissen > 0, (gehalten, gerissen)
    print("ok  Long Table: %d Enden, davon %d Risse; Stufen je Figur %s" % (len(enden), gerissen, stufen))


def zum_tisch(w):
    start(FLAGS[:4] + ["kl_loewe_frei"])
    ausflug(w)
    while "rt_drei_gefunden" not in ausflug(w):
        pass
    return ausflug(dict(w), bis="rt_t_bruch")


def tisch_neustart():
    w = {"rt_danzel": 1, "rt_bibi_frei": 1, "rt_charly": 0}
    w.update(still_wahlen())
    f = zum_tisch(w)
    assert f[-1] == "rt_t_bruch" and "rt_t_riss_still" in f, f
    z = E.aktiv()
    assert sum(1 for x in z["flags"] if x.startswith("rt_t_still_")) >= 5
    E.aktion("event_wahl", {"index": 0})                   # Try again
    E.aktion("event_schliessen", {})
    z = E.aktiv()
    assert z["event"]["id"] == "rt_tisch" and not [x for x in z["flags"] if x.startswith("rt_t_")], z["flags"]
    # zweiter Versuch: Brief, Maerz und Notizbuch vorlegen, sonst schweigen
    for _ in range(40):
        z = E.aktiv()
        ev = z.get("event") or {}
        if z["status"] != "ereignis" or ev.get("id") == "rt_white":
            break
        i = 0 if ev["id"] in ("rt_t_d1_brief", "rt_t_c1_mutter", "rt_t_b_notizbuch") else w.get(ev["id"], 0)
        E.aktion("event_wahl", {"index": i})
        E.aktion("event_schliessen", {})
    z = E.aktiv()
    assert "rt_ausgang_alle" in z["flags"], z["flags"]
    werte = {p: z["werte"]["vertrauen." + p] for p in ("danzel", "bibi", "charly")}
    assert all(1 <= v <= 3 for v in werte.values()), werte
    assert werte == {"danzel": 2, "bibi": 2, "charly": 1}, werte
    print("ok  Long Table: Riss, Neustart ohne Altlasten, Vertrauen", werte)


def bis_folgen(flags, werte, ende):
    """Tage mit Abkuerzung durchlaufen, bis alle erwarteten Pflicht-Events gekommen sind -> gesehene IDs."""
    start(FLAGS[:4] + ["kl_loewe_frei", "red_trio_fertig", "rt_tisch_fertig"] + flags)
    z = E.aktiv()
    z["flag_tag"] = dict(z.get("flag_tag", {}), **{f: 6 for f in flags})      # Baustand des Kalenders (Spiel: 5 Wochen): alles schon faellig
    z["werte"].update(werte)
    for k, v in werte.items():                    # Punkte passend zur Stufe, sonst rechnet der naechste Zuwachs sie zurueck
        z.setdefault("punkte", {})[k] = E.zustand.STUFEN_AB[v] + 4
    z["tag"] = 9
    E.sichern(z)
    gesehen, prot = [], {"schritte": [], "erledigt": {}}
    for _ in range(L.MAX_SCHRITTE):
        z = E.aktiv()
        if z["tag"] > ende or z["status"] == "ende":
            break
        ev = z.get("event") or {}
        if z["status"] == "ereignis" and ev.get("id", "").startswith(("rt_mochis", "rt_danzel", "rt_charly", "rt_bibi", "rt_napf", "rt_pfote", "rt_bon", "rt_elsa", "rt_karte")) and ev["id"] not in gesehen:
            gesehen.append(ev["id"])
        a = L.schritt(z, prot)
        if a is None:
            break
        L.tagesarbeit(z, prot) if a[0] == "_tagesarbeit" else L.versuch(a, prot)
    return gesehen, E.aktiv()


def was_nun():
    """Morgen nach dem Kampf: jede Antwort setzt genau ihre Flags und fuehrt zum Abschied."""
    d = {e["id"]: e for e in json.load(open(os.path.join(os.path.dirname(HIER), "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]}
    flags = lambda o: {f["flag"] for f in o["folgen"] if "flag" in f}
    ziel = lambda o: next(f["weiter"] for f in o["folgen"] if "weiter" in f)
    ja, nein = d["rt_wn_charly"]["optionen"]
    assert flags(ja) == {"rt_charly_bleibt"} and flags(nein) == {"rt_charly_weg"} and ziel(ja) != ziel(nein)
    ja, nein = d["rt_wn_bibi"]["optionen"]
    assert flags(ja) == {"rt_bibi_bleibt", "mochis_offen"} and flags(nein) == {"rt_bibi_weg"}
    for frame in ("rt_wn_bibi_ja", "rt_wn_bibi_nein"):
        assert {z["id"] for z in ziel(d[frame]["optionen"][0]) if "id" in z} == {"rt_abschied_frei", "rt_abschied_erloest"}, frame
    assert "mochis_offen" not in str(d["rt_ende_alle"]["optionen"]), "Die Station entsteht erst durch Ducs Idee"
    print("ok  Was aus den dreien wird")


def folgen():
    d = json.load(open(os.path.join(os.path.dirname(HIER), "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))["events"]
    ids = {e["id"]: e for e in d}
    for basis in ("rt_danzel_mass", "rt_charly_spiel", "rt_bibi_frischlinge"):
        assert all("%s_%d" % (basis, n) in ids for n in (1, 2, 3)), basis
    assert ids["rt_danzel_mass_1"]["zeilen"][0]["text"].startswith("The jacket fits you")
    werte = {"vertrauen.danzel": 3, "vertrauen.bibi": 2, "vertrauen.charly": 1}
    z0 = None
    g, z = bis_folgen(["rt_ausgang_alle", "rt_bibi_bleibt", "rt_charly_bleibt", "mochis_offen", "kl_loewe_frei", "ark_aussagen_3", "rt_ende_tag"], werte, 15)
    assert "rt_elsa_drei" in g and "rt_mochis_auf" in g and "rt_mochis_auf_ohne" not in g, g
    assert "rt_danzel_mass_3" in g and "rt_bibi_frischlinge_2" in g and "rt_charly_spiel_1" in g, g
    assert "rt_napf_frei" in g and "rt_pfote" in g and "rt_napf_erloest" not in g and not [x for x in g if x.startswith("rt_karte")], g
    # versoehnt, aber Bibi und Charly sind gegangen: nur Danzel bleibt, zwei Postkarten
    g, z = bis_folgen(["rt_ausgang_alle", "rt_bibi_weg", "rt_charly_weg", "kl_loewe_erloest", "ark_aussagen_3", "rt_ende_tag"], werte, 15)
    assert "rt_danzel_mass_3" in g and {"rt_karte_bibi", "rt_karte_charly"} <= set(g) and "rt_karte_danzel" not in g, g
    assert not [x for x in g if x.startswith(("rt_mochis", "rt_charly", "rt_bibi", "rt_napf", "rt_pfote"))], g
    # Mochi erloest, Bibi bleibt: die Station gibt es, den Abdruck nicht
    g, z = bis_folgen(["rt_ausgang_alle", "rt_bibi_bleibt", "rt_charly_weg", "mochis_offen", "kl_loewe_erloest", "ark_aussagen_3", "rt_ende_tag"], werte, 15)
    assert "rt_mochis_auf_ohne" in g and "rt_napf_erloest" in g, g
    assert {"flag": "kl_loewe_frei"} in ids["rt_pfote"]["wann"]["bedingung"]["alle"], "Der Abdruck gibt es nur, wenn Mochi lebt"
    g, z = bis_folgen(["rt_ausgang_getrennt", "rt_bibi_weg", "rt_charly_weg", "ark_aussagen_1", "rt_ende_tag"], {}, 15)
    assert "rt_karte_danzel" not in ids and "rt_elsa_eine" in g and {"rt_karte_bibi", "rt_karte_charly"} <= set(g) and not [x for x in g if x.startswith(("rt_mochis", "rt_danzel"))], g
    print("ok  Folgen:", g)


def texte_schluessig():
    """Letzter Textdurchgang: Der Spieler hoert Mochis Namen, bevor die Station so heisst; jede graue Wahl bekommt eine Antwort."""
    d = json.load(open(os.path.join(os.path.dirname(HIER), "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
    ev = {e["id"]: e for e in d["events"]}
    for i in ("rt_danzel", "rt_bibi_frei", "rt_bibi_erloest", "rt_charly"):
        assert all(o.get("zeile") for o in ev[i]["optionen"]), "Wahl ohne Reaktion: " + i
    for i in ("rt_bibi_frei", "rt_bibi_erloest"):
        assert any("Mochi" in z["text"] for z in ev[i]["zeilen"]), "Name fehlt: " + i
    assert any("attacks its own company" in z["text"] for z in ev["rt_lager"]["zeilen"]), "red team unerklaert"
    wer_luegt = ev["rt_t_luege"]["optionen"][0]["folgen"][-1]["weiter"]
    assert {x["id"] for x in wer_luegt} == {"rt_t_frage_frei", "rt_t_frage_erloest"}, "Wer luegt, muss es ihr trotzdem sagen"
    print("ok  Texte: Name, red team, Reaktionen, Luege am Tisch")


if __name__ == "__main__":
    texte_schluessig()
    was_nun()
    folgen()
    tisch_regeln()
    tisch_neustart()
    einstieg_gesperrt()
    saetze_je_ausgang()
    niederlage_haelt_an()
    alle_wege()
    print("Alles gut.")

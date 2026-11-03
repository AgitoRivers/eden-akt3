# -*- coding: utf-8 -*-
"""Ligeia als NPC (Duc 29.10.2026, docs/wiki/figuren/ligeia.md): Teich erst nach der Flut-Nacht, nachts "Time with the
Siren", Vertrauen in der Beziehungsliste, Geschenke nach ihrem Geschmack, Trust-Stufen T2-T4 und die Spur.

  python tests\\test_ligeia.py
"""
import json, os, random, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_ligeia_"))
    from kern import hauptstory as H, regeln, handel, ereignisse
    z = E.aktion("neu", {"modus": "ironman"})
    modul = E.modul_laden()
    mid = z["modul"]
    bu = H.buehne(E.moddir(mid))
    ev = {e["id"]: e for e in json.load(open(os.path.join(E.moddir(mid), "ereignisse.json"), encoding="utf-8"))["events"]}
    z["tag"], z["phase"] = 12, "nacht"
    z["bekannt"] = list(dict.fromkeys((z.get("bekannt") or []) + ["sirene", "petru", "lea", "siri", "lola"]))
    z["verlauf"] = []

    pool = modul["raeume"]["siren_pool"]
    pruefen(regeln.zugang(pool, z, {})[0] == "gesperrt", "Teich vor der Flut-Nacht zu")
    pruefen(not any(p["id"] == "sirene" for p in E.figuren_profile(z, modul)) or "sirene" in z["bekannt"],
            "Profil nur, wenn bekannt")
    z["flags"].append("sirene_fertig")
    pruefen(regeln.zugang(pool, z, {})[0] == "offen", "Teich nach der Flut-Nacht offen")
    prof = {p["id"]: p for p in E.figuren_profile(z, modul)}
    pruefen("sirene" in prof and prof["sirene"]["vertrauen"] == 1 and prof["sirene"]["begehren"] is None,
            "Beziehungsliste: Sirene mit Vertrauen 1, ohne Begehren")

    karten = []
    for s in range(40):
        karten += H.frei_phase(z, modul, "nacht", random.Random(s), bu, 3, {})
    ihre = [k for k in karten if k["anwesend"] == ["sirene"]]
    pruefen(ihre and ihre[0]["titel"] == "Time with the Siren" and ihre[0]["ort"] == "siren_pool",
            "nachts gibt es 'Time with the Siren' am Teich (%d von 40)" % len(ihre))
    pruefen(ihre[0]["ausgangslage"].count("the Siren") == 0 or "The Siren" in ihre[0]["ausgangslage"],
            "Name am Satzanfang gross")
    z["phase"] = "tag"
    pruefen(not any(k["anwesend"] == ["sirene"] for s in range(20)
                    for k in H.frei_phase(z, modul, "tag", random.Random(s), bu, 3, {})), "tagsueber ist sie nicht da")
    z["phase"] = "nacht"

    g = lambda iid: modul["items"][iid]["geschenk"].get("sirene")
    pruefen(g("gedichtband") == 2 and g("alvas_rose") == 2, "liebt Gedichte und Alvas Rose")
    pruefen(g("pink_pearl") == 1 and g("dive_torch") == -1 and g("goldfisch") == -1, "mag die Perle, hasst Lampe und Goldfisch")
    pruefen(g("lingerie") == -1, "Intim-Geschenke sind zu viel")
    handel.init(z, modul)
    z["inventar"].append("gedichtband")
    vor = (z["werte"]["vertrauen.sirene"], E.zustand.punkte(z, "vertrauen.sirene"))
    zeilen, _ = handel.schenken_npc(z, modul, "gedichtband", "sirene")
    nach = (z["werte"]["vertrauen.sirene"], E.zustand.punkte(z, "vertrauen.sirene"))
    pruefen(nach > vor and any("loves it" in str(x) for x in zeilen), "Geschenk 'liebt' hebt ihr Vertrauen (%s -> %s)" % (vor, nach))

    passt = lambda i: ereignisse.passt(z, modul, ev[i], z["phase"])
    z["werte"]["vertrauen.sirene"] = 1
    pruefen(not passt("lg_lied"), "T2 noch nicht bei Vertrauen 1")
    z["werte"]["vertrauen.sirene"] = 2
    pruefen(passt("lg_lied"), "T2 Wiegenlied ab Vertrauen 2")
    opt = ev["lg_lied"]["optionen"][0]["folgen"]
    pruefen({"wert": "energie", "delta": 1} in opt, "Wiegenlied gibt +1 Energie")
    z["flags"].append("ligeia_lied")
    z["werte"]["vertrauen.sirene"] = 3
    pruefen(passt("lg_drei") and not passt("lg_lied"), "T3 nach dem Lied, Lied nur einmal")
    z["flags"].append("ligeia_felsen_hinweis")
    z["phase"] = "abend"
    pruefen(passt("lg_felsen"), "Lea mit den Felsen nach T3")
    z["phase"] = "nacht"
    pruefen(not passt("lg_perle"), "T4 erst ab Vertrauen 4")
    z["werte"]["vertrauen.sirene"] = 4
    pruefen(passt("lg_perle"), "T4 Perle ab Vertrauen 4")

    z["phase"] = "abend"
    pruefen(passt("lg_petru_1924") and not passt("lg_seekiste"), "Petru 1924 nach der Flut-Nacht, Seekiste noch zu")
    z["flags"].append("ligeia_1924")
    z["flags"].append("ligeia_perle_hinweis")
    pruefen(passt("lg_seekiste"), "Seekiste ueber Ligeias Perle (T4)")
    z["flags"].append("petru_werkstatt_zu_duc")
    pruefen(not passt("lg_seekiste"), "bei kaltem Petru (Weg B) keine Seekiste")
    for i in ("lg_lied", "lg_drei", "lg_perle", "lg_petru_1924", "lg_seekiste", "lg_felsen", "lg_siri_lied"):
        pruefen(any("codex" in f for o in ev[i]["optionen"] for f in o["folgen"]), "%s schreibt in den Codex" % i)

    from kern import szene as S
    z["persona"] = z.get("persona") or {"oeffentlich": "the new First Officer"}
    s = ihre[0]
    sz = {"def": s, "figuren": ["sirene"], "auftraege": {"sirene": {"will": "x", "verbirgt": "y", "grenze": "z"}},
          "log": [], "zug": 0}
    pr = S.figur_prompt(z, modul, sz, "sirene")
    pruefen("lets the water rise to her chin" in pr and "sailor" in pr and "Welsh" not in pr,
            "Prompt: eigene Gesten, 'sailor', nichts Walisisches")
    print("OK")


if __name__ == "__main__":
    main()

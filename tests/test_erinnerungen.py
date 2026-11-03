# -*- coding: utf-8 -*-
"""Der Spieler hat die Szene davor vergessen (Duc 31.10.2026, STIL.md): Journal, Missionskarte und Ortskarte erinnern ihn.

  python tests\\test_erinnerungen.py
"""
import json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import auftraege, handel, zustand  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
A = json.load(open(os.path.join(MOD, "auftraege.json"), encoding="utf-8"))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(*flags, tag=12):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["phase"] = tag, "tag"
    z["flags"] += list(flags)
    return z


def eintrag(z, aid):
    return next(x for x in auftraege.journal(z, MODUL, MOD, lambda p: None) if x["id"] == aid)


# Journal
z = spiel("berge_angenommen")
pruefen(eintrag(z, "berge")["rueckblick"] is None, "Noch nichts erledigt: kein Rueckblick")
z["flags"] += ["bg_turm_erreicht", "bg_bergerie_erreicht"]
pruefen("Laetitia at the bergerie" in eintrag(z, "berge")["rueckblick"], "Journal: Der letzte erledigte Schritt erzaehlt, was war")
z["flags"].append("berge_fertig")
pruefen(eintrag(z, "berge")["rueckblick"] is None, "Fertiger Auftrag: kein Rueckblick")
g = next(x for x in eintrag(spiel("rt_gestartet"), "red_trio")["schritte"] if "Mr. White" in x["text"]) if False else None
pruefen(not any("Mr. White" in x["text"] for x in eintrag(spiel("rt_gestartet"), "red_trio")["schritte"]), "Mr. White steht erst im Journal, wenn man am Tisch war")
pruefen(any("Mr. White" in x["text"] for x in eintrag(spiel("rt_gestartet", "rt_tisch_fertig"), "red_trio")["schritte"]), "Danach steht er dort")

# Ortskarte je Lage
ORT = A["orte"]["berge"]
z = spiel("berge_angenommen")
pruefen(auftraege.ort_text(z, ORT) == ORT["text"], "Ortskarte: am Anfang der allgemeine Text")
z["flags"].append("bg_turm_erreicht")
pruefen("Wolff" in auftraege.ort_text(z, ORT), "Ortskarte: zurueck zum Turm nennt Wolff")
z["flags"].append("bg_bergerie_erreicht")
pruefen("Adrien" in auftraege.ort_text(z, ORT), "Ortskarte: zurueck zur Bergerie nennt Adrien")
karten = {o["id"]: o for o in auftraege.orte_frei(z, MOD)}
pruefen("Adrien" in karten["berge"]["text"], "orte_frei liefert den Text der Lage")
M = A["orte"]["macchia"]
z = spiel("kloster_angenommen", "kloster_fertig", "grotte_fertig", "kl_nische_geleert", "rt_getrennt")
pruefen("black suits" in auftraege.ort_text(z, M), "Macchia: Die Karte nennt die Red-Trio-Lage")

# Missionskarte
V = {"jobs": [{"id": "a", "erfolg": "It worked."}, {"id": "b", "nach": "a"}, {"id": "c"}]}
z = spiel()
z["jobs_erfolg"] = []
pruefen(handel.zuletzt(z, V, V["jobs"][1]) is None, "Mission: ohne erledigte Vorgaengerin kein Rueckblick")
z["jobs_erfolg"] = ["a"]
pruefen(handel.zuletzt(z, V, V["jobs"][1]) == "It worked.", "Mission: Das Ergebnis der Mission davor steht auf der Karte")
pruefen(handel.zuletzt(z, V, V["jobs"][2]) is None, "Mission ohne Kette: kein Rueckblick")

# Texte
texte = open(os.path.join(MOD, "missionen.json"), encoding="utf-8").read() + open(os.path.join(MOD, "auftraege.json"), encoding="utf-8").read()
pruefen("the failure" not in texte, "Das Feuer heisst ueberall Feuer")
ev = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]
I = {e["id"]: e for e in ev}
pruefen("All those letters" in I["kl_mina_fragt"]["zeilen"][0]["text"], "Mina erinnert an die Briefe")
pruefen("Mochi" in I["rt_napf_frei"]["zeilen"][0]["text"], "Bibi nennt den Loewen")
pruefen("man in white" in I["rt_bon"]["zeilen"][0]["text"], "Danzel erinnert an den Mann in Weiss")
pruefen("black suits" in I["rt_gabelung_111"]["lage"], "Die Gabelung sagt, was passiert ist")
tags = {x["text"] for x in json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
for i in ("kl_mina_fragt", "rt_napf_frei", "rt_bon"):
    pruefen(I[i]["zeilen"][0]["text"] in tags, "%s: gesprochene Fassung passt" % i)
print("fertig")

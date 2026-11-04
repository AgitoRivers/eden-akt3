# -*- coding: utf-8 -*-
r"""Outfit-Quest, Pilot Sophias Lesung (Duc 31.10.2026, E-104, Wiki systeme/schneider.md): die ganze Kette ueber die echten Pflicht-Events.

  python tests\test_outfit_quest.py
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
from kern import ereignisse, regeln, schneider, zustand  # noqa: E402

MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
MODUL = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
MODUL["_kuechen_pfad"] = MOD
ALLE = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))
EV = {e["id"]: e for e in ALLE["events"]}
QUEST = [e for e in ALLE["events"] if e["id"].startswith("ol_")]
_daten = ereignisse.daten


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def spiel(tag=16, ruf=1):
    z = zustand.neu(MODUL, "entspannt")
    zustand.persona_setzen(z, MODUL, MODUL["personas"][0])
    z["tag"], z["heute"], z["konto"] = tag, [{"ort": "alvas_bar"}], 500
    z["bekannt"] = list(MODUL["personen"])
    z["werte"]["ruf"] = ruf
    z["werte"]["vertrauen.sophia"] = z["werte"]["begehren.sophia"] = 4      # Fourteen verlangt beides
    z["flags"] += ["rt_ausgang_alle", "rt_ende_tag", "rm_s3"]
    z.setdefault("flag_tag", {}).update(rt_ende_tag=10, rm_s3=tag - 2)
    return z


def ziehen(z, phase):
    z["phase"] = phase
    ev = ereignisse.pflicht_ziehen(z, MODUL, MOD)
    return ev["id"] if ev else None


def antwort(z, eid, nr=0):
    """Folgen der Antwort anwenden und dem naechsten Takt folgen, wie eden.py beim Schliessen. Gibt das naechste Takt-Event."""
    ereignisse.anwenden(z, MODUL, EV[eid], EV[eid]["optionen"][nr]["folgen"])
    return ereignisse.direkt_ziel(z)


def kette(z, eid, nr=0):
    """Antwort nr, dann in Folgetakten immer die erste Antwort, bis die Szene aus ist."""
    w = antwort(z, eid, nr)
    while w:
        w = antwort(z, w)


def poker(z, richtig):
    """richtig = Liste aus drei Wahrheitswerten, ob Duc die Hand richtig liest."""
    w = antwort(z, "ol_poker")
    for r in richtig:
        mehr_gut = '"ol_p_g' in json.dumps(EV[w]["optionen"][0]["folgen"])
        w = antwort(z, w, 0 if r == mehr_gut else 1)
    return w


def bis_zur_anprobe(z, richtig=(True, True, True)):
    pruefen(ziehen(z, "tag") == "ol_wunsch", "nach Fourteen kommt der Wunsch an Alvas Bar")
    pruefen(EV["ol_wunsch"]["sets"]["sophia"] == "Concierge", "dabei trägt sie noch die Uniform")
    kette(z, "ol_wunsch", 0)
    pruefen("ol_wette" in z["flags"], "die Wette ist gemerkt")
    pruefen(ziehen(z, "tag") is None, "am selben Tag kommt nicht schon Danzel")
    z["tag"] += 1
    pruefen(ziehen(z, "tag") == "ol_mantel", "am nächsten Tag erzählen Danzel und Totò vom Mantel")
    kette(z, "ol_mantel")
    pruefen(ziehen(z, "abend") == "ol_poker", "am selben Abend das Poker")
    return poker(z, richtig)


def main():
    ereignisse.daten = lambda moddir: {"events": QUEST}
    pruefen(len(QUEST) >= 18 and all(any(z["wer"] for z in e["zeilen"]) for e in QUEST), "alle Takte haben Zeilen")
    tags = {z["text"] for z in json.load(open(os.path.join(MOD, "stimme_tags.json"), encoding="utf-8"))["zeilen"]}
    fehlt = [z["text"] for e in QUEST for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")] if z["text"] not in tags]
    pruefen(not fehlt, "jede Zeile hat einen Turbo-Tag in stimme_tags.json")

    # Im Mantel-Satz hocken oder drehen sich diese Gefuehle weg, die Szenen sagen aber: Sie steht und schaut in den Saal
    weg = {"amusement", "curiosity", "embarrassment", "fear", "grief", "nervousness", "pride", "relief", "remorse", "sadness"}
    falsch = [e["id"] for e in QUEST if e["sets"].get("sophia") == "Book Reading" for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]
              if z["wer"] == "sophia" and z["gefuehl"] in weg]
    pruefen(not falsch, "im Mantel steht Sophia und schaut nach vorn")

    # Ohne Laden oder ohne Fourteen gibt es die Quest nicht
    z = spiel()
    z["flags"].remove("rt_ende_tag")
    pruefen(ziehen(z, "tag") is None, "ohne Danzels Laden keine Quest")
    z = spiel()
    z["flags"].remove("rt_ausgang_alle")
    z["flags"].append("rt_ausgang_getrennt")
    pruefen(ziehen(z, "tag") is not None, "auch beim zerbrochenen Trio gibt es die Quest (E-112)")
    z = spiel()
    z["flags"].remove("rm_s3")
    pruefen(ziehen(z, "tag") is None, "ohne Fourteen keine Quest")

    # Gewinnen, Name offen, voller Durchlauf
    z = spiel(ruf=4)
    konto = z["konto"]
    w = bis_zur_anprobe(z)
    pruefen(w == "ol_p_sieg", "richtig gelesen gewinnt den Mantel")
    ruf = z["werte"]["ruf"]
    kette(z, w)
    pruefen("old_camel_coat" in z["inventar"] + z.get("truhe", []) and z["konto"] == konto, "der Mantel ist da und hat nichts gekostet")
    pruefen(z["werte"]["ruf"] == ruf + 1 or ruf == 5, "der Sieg bringt Ruf")

    mass = [m for m in schneider.ansicht(z, MODUL)["massstuecke"] if m["id"] == "penrose_coat"]
    pruefen(mass and mass[0]["geht"], "ohne Schnittmuster, aber mit Mantel steht das Maßstück bei Danzel")
    muster = schneider.muster(z, MODUL)
    schneider.bringen(z, MODUL, "penrose_coat")
    pruefen("old_camel_coat" not in z["inventar"] and z["konto"] == konto - 60, "Danzel nimmt Mantel und Geld")
    pruefen(schneider.muster(z, MODUL) == muster, "es verbraucht kein Schnittmuster")
    pruefen(ziehen(z, "tag") is None, "heute noch keine Anprobe")
    z["tag"] += 1
    pruefen(ziehen(z, "tag") == "ol_etikett", "am nächsten Tag die Anprobe")
    pruefen(EV["ol_etikett"]["sets"]["sophia"] == "Book Reading", "bei der Anprobe trägt sie den neuen Look")
    kette(z, "ol_etikett", 2)
    pruefen("ol_name_leer" in z["flags"] and "sn_penrose_coat_fertig" in z["flags"], "die Wahl ist gemerkt, das Maßstück ist fertig")
    pruefen(not [m for m in schneider.ansicht(z, MODUL)["massstuecke"] if m["id"] == "penrose_coat"], "danach steht es nicht mehr im Laden")

    pruefen(ziehen(z, "abend") is None, "am Abend der Anprobe noch keine Lesung")
    z["tag"] += 1
    pruefen(ziehen(z, "abend") == "ol_tuer_leer", "am nächsten Abend die Lesung mit der gewählten Fassung")
    w = antwort(z, "ol_tuer_leer")
    pruefen(w == "ol_auftritt_leer", "die Tür führt auf die Bühne")
    weg = []
    for n in ("ol_auftritt_leer", "ol_stille", "ol_kipp", "ol_reaktion", "ol_tresen"):
        pruefen(n == w, "Takt %s kommt der Reihe nach" % n)
        weg.append(n)
        if n != "ol_tresen":
            w = antwort(z, n)
    pruefen(len(EV["ol_stille"]["optionen"]) == 3 and all(o.get("zeile") for o in EV["ol_stille"]["optionen"]), "Duc hilft ihr auf drei Arten, jede mit eigener Antwort")
    ruf = z["werte"]["ruf"]
    while w:
        w = antwort(z, w)
    pruefen(z["werte"]["ruf"] == min(ruf + 2, 5), "die Lesung bringt Ruf +2")
    pruefen('"vertrauen": ["sophia"' in json.dumps(EV["ol_tresen"]["optionen"]), "und Vertrauen")
    pruefen("ol_erledigt" in z["flags"], "die Quest ist abgeschlossen")
    z["tag"] += 1
    pruefen(ziehen(z, "fruehstueck") == "ol_echo", "am Morgen danach kommt das Echo")
    pruefen(ziehen(z, "tag") == "ol_dorf", "und das Dorf redet")
    pruefen(ziehen(z, "abend") is None, "danach kommt nichts mehr")

    # Verlieren kostet Geld, aber sperrt nichts
    z = spiel()
    konto = z["konto"]
    w = bis_zur_anprobe(z, (False, False, True))
    pruefen(w == "ol_p_nieder", "falsch gelesen verliert")
    kette(z, w)
    pruefen("old_camel_coat" in z["inventar"] + z.get("truhe", []) and z["konto"] == konto - 40, "der Mantel kostet dann 40 Euro")

    # Die anderen Namen führen in ihre eigene Fassung
    for nr, name in ((0, "penrose"), (1, "moore")):
        z = spiel()
        kette(z, "ol_wunsch")
        z["inventar"].append("old_camel_coat")
        schneider.bringen(z, MODUL, "penrose_coat")
        z["tag"] += 1
        kette(z, "ol_etikett", nr)
        z["tag"] += 2
        z["phase"] = "abend"
        pruefen(ziehen(z, "abend") == "ol_tuer_" + name, "Name %s: eigene Lesung" % name)

    # Akt 3 bleibt offen, Zufall zieht die Takte nie
    pruefen(EV["ol_wunsch"]["wann"].get("akt2") == [24, 35], "die Quest geht auch in Akt 3 (ab Tag 24, E-114)")
    pruefen(all("phasen" not in e["wann"] for e in QUEST if not e["wann"].get("pflicht")), "Folgetakte werden nie zufällig gezogen")
    ereignisse.daten = _daten
    print("Alles gut.")


if __name__ == "__main__":
    main()

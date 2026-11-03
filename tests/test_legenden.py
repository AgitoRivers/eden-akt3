# -*- coding: utf-8 -*-
"""Das Dorf, das redet (Duc 30.10.2026): eine Tat wird ueber Nacht zur Legende, waechst in drei Stufen, gibt Ruf und
verblasst; Figuren erzaehlen sie beim Ladenbesuch, beim Szenenstart und per Handy - jede Zeile einmal, je Figur eine am
Tag. Dazu der Merker: jede neue Figur gehoert zur Familie (sonst schlaegt dieser Test fehl).

  python tests\\test_legenden.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")

E = L.eden
LG = E.legenden
# Figuren ohne Legenden-Zeilen, mit Grund: weg (Holm ab Tag 2), Zentrale (Megan), Sirene, Missions-Fremde
OHNE = {"holm", "megan", "sirene", "mrwhite", "adrien", "chloe", "dumenica", "frederico", "gennaro", "ghjuvan", "laetitia",
        "matteu", "riscossore", "wolff", "minicu", "alon", "bonaventure"}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def tag_beenden(z, modul, md):
    """Tagesende wie in eden.py, nur der Legenden-Teil (z["tag"] ist danach der neue Tag)."""
    z["tag"] += 1
    return LG.tagesende(z, modul, md, E.zustand.folgen_anwenden)


def main():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_legenden_"))
    modul, md = E.modul_laden("eden_rise"), E.moddir("eden_rise")
    d = LG.daten(md)

    # ---------------------------------------------------------------- Daten
    pruefen(len(d["zeilen"]) >= 60, "%d Legenden-Zeilen" % len(d["zeilen"]))
    fehlt = sorted(set(modul["personen"]) - set(d["familie"]) - OHNE)
    pruefen(not fehlt, "Merker: jede Figur gehoert zur Familie (fehlt: %s)" % (fehlt or "niemand"))
    for pid in d["familie"]:
        pruefen(any(l["wer"] == pid for l in d["zeilen"].values()), "%s hat Legenden-Zeilen" % pid)
    for tid in d["taten"]:
        wer = {l["wer"] for l in d["zeilen"].values() if l["tat"] == tid}
        pruefen(len(wer) >= 2 and any(l["wo"] == "laden" for l in d["zeilen"].values() if l["tat"] == tid),
                "Tat %s: %d Erzaehler, mindestens ein Laden" % (tid, len(wer)))
    tags = {t["text"] for t in json.load(open(os.path.join(md, "stimme_tags.json"), encoding="utf-8"))["zeilen"]
            if t.get("quelle") == "legenden"}
    pruefen(all(l["text"] in tags for l in d["zeilen"].values()), "jede Zeile hat eine gesprochene Fassung (Turbo-Tag)")
    pruefen(LG.zeile(md, "leg.hafen.alva.laden.0") == ("alva", d["zeilen"]["hafen.alva.laden.0"]["text"]),
            "Vertonung findet leg.<id>")

    # ---------------------------------------------------------------- Ablauf
    L.random.seed(3)
    z = E.aktion("neu", {"modus": "ironman"})
    z["tag"], ruf0 = 2, z["werte"].get("ruf", 0)
    z["flags"].append("kloster_faden")                            # Hafenkampf geschafft (Tag 2)
    pruefen(LG.zeile_fuer(z, md, "alva", "laden") is None, "am Tag der Tat redet noch niemand")
    tag_beenden(z, modul, md)                                     # -> Tag 3
    pruefen("leg_hafen" in z["flags"] and z["flag_tag"]["leg_hafen"] == 2, "ueber Nacht wird die Tat zur Legende")
    pruefen(LG.stufe(z, "hafen") == 0, "Tag 3: Stufe 0")
    l = LG.zeile_fuer(z, md, "alva", "laden")
    pruefen(l and l["stufe"] == 0, "Alva begruesst Duc mit der Legende")
    LG.markieren(z, l)
    pruefen(LG.zeile_fuer(z, md, "alva", "laden") is None, "je Figur hoechstens eine Legenden-Zeile am Tag")
    pruefen(LG.zeile_fuer(z, md, "rosi", "zeit") is not None, "Rosi hat am selben Tag ihre eigene")
    zeilen = tag_beenden(z, modul, md)                            # -> Tag 4: Stufe 1, Ruf +1
    pruefen(LG.stufe(z, "hafen") == 1 and z["werte"]["ruf"] == min(5, ruf0 + 1),
            "Tag 4: Stufe 1, Ruf +1 (%s)" % " / ".join(zeilen))
    pruefen(LG.zeile_fuer(z, md, "alva", "laden") is None, "Alvas einzige Hafen-Zeile ist gehoert")
    pruefen(LG.zeile_fuer(z, md, "petru", "laden")["stufe"] == 1, "Petru erzaehlt die uebertriebene Fassung")
    tag_beenden(z, modul, md)                                     # Tag 5
    tag_beenden(z, modul, md)                                     # Tag 6: Stufe 2, Ruf +1
    pruefen(LG.stufe(z, "hafen") == 2 and z["werte"]["ruf"] == min(5, ruf0 + 2), "Tag 6: Stufe 2, Ruf noch einmal +1")
    ruf = z["werte"]["ruf"]
    for _ in range(LG.RUF_RUHE):
        tag_beenden(z, modul, md)
    pruefen(z["werte"]["ruf"] == ruf - 1, "nach %d ruhigen Tagen verblasst der Ruf um 1" % LG.RUF_RUHE)

    # Bedingungen je Ausgang: Berge Weg B gibt keinen Ruf, Petru ist kalt, Sophia erzaehlt die traurige Fassung
    z2 = E.aktion("neu", {"modus": "ironman"})
    z2["tag"] = 10
    z2["flags"] += ["berge_fertig", "bg_weg_b"]
    r = z2["werte"].get("ruf", 0)
    for _ in range(3):
        tag_beenden(z2, modul, md)
    pruefen(LG.stufe(z2, "berge") == 1 and z2["werte"].get("ruf", 0) == r, "Weg B: die Legende waechst, Ruf nicht")
    s = LG.zeile_fuer(z2, md, "sophia", "zeit")
    pruefen(s and "dark" in s["text"], "Sophia erzaehlt nach Weg B vom dunklen Laden")
    pruefen(LG.zeile_fuer(z2, md, "petru", "laden") is None, "Petrus Berge-Zeilen gelten nicht nach Weg B")

    # Laden: die Begruessung bleibt fuer diesen Besuch dieselbe, beim naechsten Besuch kommt der normale Gruss
    z3 = E.aktion("neu", {"modus": "ironman"})
    z3["tag"] = 2
    z3["flags"].append("kloster_faden")
    tag_beenden(z3, modul, md)
    a1 = E.laden_auftritt(z3, modul, "eden_rise", "alva")
    a2 = E.laden_auftritt(z3, modul, "eden_rise", "alva")
    pruefen(a1["gruss"]["id"].startswith("leg.") and a1["gruss"]["id"] == a2["gruss"]["id"],
            "Alvas Gruss ist die Legende und bleibt beim Neuaufbau der Ansicht gleich")
    z3["phase"] = "abend" if z3.get("phase") != "abend" else "nacht"
    a3 = E.laden_auftritt(z3, modul, "eden_rise", "alva")
    pruefen(not a3["gruss"]["id"].startswith("leg."), "beim naechsten Besuch wieder der normale Gruss")

    # Handy: die Nachfrage kommt erst, wenn die Legende alt genug ist
    ev = {e["id"]: e for e in json.load(open(os.path.join(md, "ereignisse.json"), encoding="utf-8"))["events"]}
    pruefen(ev["leg_sirene_lea"]["wann"]["bedingung"] == {"flag_seit": ["leg_sirene", 1]},
            "Leas Frage zur Sirene wartet auf die Legende")
    pruefen(len([i for i in ev if i.startswith("leg_")]) >= 6, "sechs Handy-Nachfragen")
    print("\nalle Legenden-Tests bestanden")


if __name__ == "__main__":
    main()

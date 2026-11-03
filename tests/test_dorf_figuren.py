# -*- coding: utf-8 -*-
"""Dorf-Figuren, Phase 1 (Duc 30.10.2026, docs/wiki/welt/dorf_figuren.md): die fuenf sind im Modul angemeldet, am Start
unbekannt, stehen in der Legenden-Familie, und ihre Modul-Beschreibung verraet keine Geheimnisse.

  python tests\\test_dorf_figuren.py
"""
import json, os, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402
sys.stdout.reconfigure(encoding="utf-8")

E = L.eden
NEU = ["pascal", "mina", "batu", "sandru", "anghjulu"]
GEHEIM = ["bought", "alon", "drawer", "confess", "betray", "a.v. estates", "monaco", "love", "dumè", "dume"]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_dorf_"))
    modul, md = E.modul_laden("eden_rise"), E.moddir("eden_rise")
    d = E.legenden.daten(md)
    for pid in NEU:
        p = modul["personen"].get(pid)
        pruefen(p and not p["romanzierbar"], "%s ist angemeldet und nicht romanzierbar" % pid)
        pruefen(pid not in modul["bekannt_start"], "%s ist am Start unbekannt" % pid)
        pruefen(modul["werte"]["vertrauen"]["start"].get(pid) == 0, "%s startet bei Vertrauen 0" % pid)
        pruefen(pid in d["familie"], "%s gehoert zur Legenden-Familie" % pid)
        text = p["beschreibung"].lower()
        pruefen(not [w for w in GEHEIM if w in text], "%s: Beschreibung ohne Geheimnisse" % pid)
        zeilen = [l for l in d["zeilen"].values() if l["wer"] == pid]
        pruefen(len(zeilen) >= 3, "%s hat %d Legenden-Zeilen" % (pid, len(zeilen)))
    z = E.aktion("neu", {"modus": "ironman"})
    pruefen(not set(NEU) & set(z.get("bekannt") or []), "ein neuer Lauf kennt keine der fuenf")
    # Phase 2: Szenen, Stimmen, Geschenke, Regel fuer den Ruf
    ev = {e["id"]: e for e in json.load(open(os.path.join(md, "ereignisse.json"), encoding="utf-8"))["events"]}
    tags = {t["text"] for t in json.load(open(os.path.join(md, "stimme_tags.json"), encoding="utf-8"))["zeilen"] if t.get("quelle") == "dorf"}
    for eid in ("hk_pascal", "g1_mina_post", "hy_pascal_holm", "g1_pascal_gebuehren", "g1_pascal_telefon", "g1_pascal_ricci",
                "g1_casanova_morgen", "gv_casanova_megan", "kl_pascal_tuer", "kl_mina_post"):
        pruefen(eid in ev, "Szene %s ist im Modul" % eid)
        zeilen = list(ev[eid]["zeilen"]) + [o["zeile"] for o in ev[eid]["optionen"] if o.get("zeile")]
        pruefen(all(z["text"] in tags for z in zeilen), "%s: jede Zeile hat eine gesprochene Fassung" % eid)
        pruefen(not any("[" in z["text"] for z in zeilen), "%s: im Spieltext steht kein Tag" % eid)
    # Phase 3: Woche 2
    for eid in ("g1_batu_intro", "g1_batu_intro_allein", "g1_batu_mutter", "g1_sandru_logo", "g1_sandru_tafel", "kl_totenfeier_lebt",
                "kl_totenfeier_tot", "kl_mina_fragt", "kl_mina_fragt_tot", "kv_don", "g1_messe", "g1_vb_brot", "g1_vb_wangen",
                "g1_vb_fahne", "g1_vb_eu", "g1_vb_eintopf", "g1_vb_auntie"):
        pruefen(eid in ev, "Szene %s ist im Modul" % eid)
        zeilen = list(ev[eid]["zeilen"]) + [o["zeile"] for o in ev[eid]["optionen"] if o.get("zeile")]
        pruefen(all(z["text"] in tags for z in zeilen), "%s: jede Zeile hat eine gesprochene Fassung" % eid)
    pruefen(modul["laeden"]["batu"]["bedingung"] == {"flag": "batu_laden"}, "Ba Tus Laden oeffnet mit ihrer ersten Szene")
    pruefen("batu" in modul["items"]["fish_sauce"]["wo"], "Ba Tu verkauft die Fischsauce")
    zutaten = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", "eden_rise", "kuechen.json"), encoding="utf-8"))["zutaten"]
    for iid, it in modul["items"].items():
        if "batu" in (it.get("wo") or []) and it.get("zutat"):
            pruefen(it["zutat"] in zutaten, "Ba Tus Ware %s ist eine Zutat" % iid)
            pruefen(len(it["text"]) <= 220, "Ba Tus Ware %s: Text hoechstens 220 Zeichen" % iid)
    pruefen(zutaten["fish_sauce"]["effekt"] == "umami", "Fischsauce hat ihren eigenen Effekt")
    folgen = json.dumps(ev["g1_pascal_ricci"]["optionen"][0]["folgen"])
    pruefen('"jade"' in folgen, "Pascal gibt die Jade fuer Terremoto")
    z2 = E.aktion("neu", {"modus": "ironman"})
    z2["tag"], z2["ruf_tag"] = 9, 5
    z2["werte"]["ruf"] = 3
    z2.setdefault("bekannt", []).append("pascal")
    aus = E.legenden.tagesende(z2, modul, md, E.zustand.folgen_anwenden)
    pruefen(z2["werte"]["ruf"] == 3 and any("Pascal" in a for a in aus), "Pascal haelt den Ruf einmal fest")
    z2["tag"] = 11
    E.legenden.tagesende(z2, modul, md, E.zustand.folgen_anwenden)
    pruefen(z2["werte"]["ruf"] == 2, "beim naechsten Mal verblasst er")
    print("Alles OK")


if __name__ == "__main__":
    main()

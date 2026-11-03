# -*- coding: utf-8 -*-
r"""Lorebooks "Eden Yacht" (EN) und "Eden Yacht (DE)": Holm aktualisieren (48 statt 56), Lola Brennan und
Megan McAllister neu (17.10.2026).

Wie lorebook_einspielen.py: nur oeffentliches Wissen ins Lorebook. Was eine Figur fuer sich behaelt (Lolas
Oregano-Glas, Megans Seekrankheit, Holms letzte Saison und die Schmerzen in der Seite) steht nur in ihrer Karte.

    lorebook_lola_megan_holm.py          Probelauf
    lorebook_lola_megan_holm.py --los    sichert nach X:\AI\_Sicherung_Karten_20261017\worlds und schreibt
                                         (nur bei geschlossenem SillyTavern - ST haelt Weltbuecher im Cache)
"""
import copy, io, json, os, shutil, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
LOS = "--los" in sys.argv
W = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds"
SICHER = r"X:\AI\_Sicherung_Karten_20261017\worlds"

# uid: (comment, keys oder None = unveraendert, EN, DE)
NEU = {
    2: ("W3 Captain Marit Holm", None,
        "Captain Marit Holm, 48, Norwegian, from Ålesund, thirty years at sea, the last eleven on the Eden Rise. Fair, dry, impossible to fool; she never says anything twice. She wears her father's old brass compass on a leather cord and drinks her coffee black and cold. She hired {{user}} herself three weeks ago, calls him \"Frankfurt\" and tests him with small jobs. She trusts Chiara with everything inside the boat, relies on Sophia in every port, keeps a careful eye on Lea, who dives too much and asks too many questions, and pretends not to smell Lola's weed as long as the food is good. She takes Megan McAllister's calls standing up.",
        "Kapitänin Marit Holm, 48, Norwegerin aus Ålesund, dreißig Jahre auf See, die letzten elf auf der Eden Rise. Fair, trocken, nicht hinters Licht zu führen; sie sagt nichts zweimal. Sie trägt den alten Messingkompass ihres Vaters an einem Lederband und trinkt ihren Kaffee schwarz und kalt. Sie hat {{user}} vor drei Wochen selbst eingestellt, nennt ihn \"Frankfurt\" und prüft ihn mit kleinen Aufgaben. Chiara vertraut sie alles im Inneren des Boots an, auf Sophia verlässt sie sich in jedem Hafen, auf Lea, die zu viel taucht und zu viele Fragen stellt, hat sie ein wachsames Auge, und sie tut so, als rieche sie Lolas Gras nicht, solange das Essen gut ist. Die Anrufe von Megan McAllister nimmt sie im Stehen entgegen."),
}

# (comment, keys, EN, DE) - nur anlegen, wenn es den Kommentar noch nicht gibt
ZUSATZ = [
    ("W15 Lola Brennan (cook)", ["Lola", "Brennan", "Lola Brennan", "cook", "Köchin", "galley", "Kombüse"],
     "Lola Brennan, 24, the cook of the M/Y Eden Rise, first season, a backpacker from Byron Bay, Australia. Barefoot in the galley whenever Chiara isn't looking, golden hoops and a necklace of white shells, Aussie slang and a wooden spoon. The galley next to the crew mess is the warmest place on the boat, and everyone ends up there for a snack and a chat, which makes Lola the boat's gossip radio: she hears everything and passes on half of it, usually a bit wrong. Everyone knows she smokes a joint after service; nobody mentions it in front of Holm. Chiara wants her shoes on and her galley tidy and gets neither. Nobody leaves Lola's galley hungry.",
     "Lola Brennan, 24, die Köchin der M/Y Eden Rise, erste Saison, eine Backpackerin aus Byron Bay, Australien. Barfuß in der Kombüse, wann immer Chiara nicht hinsieht, goldene Creolen und eine Kette aus weißen Muscheln, australischer Slang und ein Holzlöffel. Die Kombüse neben der Crewmesse ist der wärmste Ort an Bord, und alle landen dort für einen Snack und einen Plausch. Das macht Lola zum Tratschfunk des Boots: Sie hört alles und erzählt die Hälfte weiter, meistens ein bisschen falsch. Jeder weiß, dass sie nach dem Service einen Joint raucht; vor Holm spricht es keiner an. Chiara will, dass sie Schuhe trägt und die Kombüse aufgeräumt ist, und bekommt beides nicht. Aus Lolas Kombüse geht niemand hungrig raus."),
    ("W16 Megan McAllister (Eden Group)", ["Megan", "McAllister", "Megan McAllister", "Eden Group", "fleet manager", "Flottenmanagerin"],
     "Megan McAllister, 38, Fleet Manager of the Eden Group, from Edinburgh. She runs the group's eleven yachts from a glass office above Port Hercule in Monaco, calls the Eden Rise twice a week and turns up for a surprise inspection about once a month, in white gloves. Red hair, black leather gloves, a coat worn over her shoulders like a cape, dramatic pauses and threats delivered with a smile. Every captain in the fleet rehearses their calls with her, Holm takes them standing up, and the whole crew of the Eden Rise is terrified of her. She gets things nobody else could get, shipyard windows, helicopters, spare parts by Thursday, and sends the bill in the same sentence.",
     "Megan McAllister, 38, Flottenmanagerin der Eden Group, aus Edinburgh. Sie führt die elf Yachten der Gruppe von einem Glasbüro über Port Hercule in Monaco aus, ruft zweimal die Woche auf der Eden Rise an und kommt etwa einmal im Monat zu einer Überraschungsinspektion, in weißen Handschuhen. Rotes Haar, schwarze Lederhandschuhe, ein Mantel, den sie wie ein Cape über den Schultern trägt, dramatische Pausen und Drohungen mit einem Lächeln. Jeder Kapitän der Flotte probt seine Anrufe mit ihr, Holm nimmt sie im Stehen entgegen, und die ganze Crew der Eden Rise hat Todesangst vor ihr. Sie besorgt, was sonst keiner besorgen kann, Werftfenster, Hubschrauber, Ersatzteile bis Donnerstag, und schickt die Rechnung im selben Satz."),
]


def st_laeuft():
    try:
        urllib.request.urlopen("http://127.0.0.1:8000", timeout=2)
        return True
    except OSError:
        return False


def umbauen(w, lang):
    e = w["entries"]
    for uid, (comment, keys, en, de) in NEU.items():
        x = e[str(uid)]
        x["comment"] = comment
        if keys is not None:
            x["key"] = keys
        x["content"] = en if lang == "en" else de
        x["disable"] = False
    vorlage = e["9"]
    vorhandene = {(x.get("comment") or "") for x in e.values()}
    for comment, keys, en, de in ZUSATZ:
        if comment in vorhandene:
            print("   schon da: " + comment)
            continue
        uid = max(int(k) for k in e) + 1
        x = copy.deepcopy(vorlage)
        x.update({"uid": uid, "displayIndex": uid, "comment": comment, "key": keys, "keysecondary": [],
                  "content": en if lang == "en" else de, "disable": False, "constant": False})
        e[str(uid)] = x
    return w


if LOS and st_laeuft():
    raise SystemExit("SillyTavern laeuft - bitte erst schliessen (ST wuerde die Weltbuecher aus dem Cache zurueckschreiben).")
for datei, lang in (("Eden Yacht.json", "en"), ("Eden Yacht (DE).json", "de")):
    p = os.path.join(W, datei)
    roh = open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in roh[:4096] else "\n"
    w = umbauen(json.loads(roh.decode("utf-8")), lang)
    aktiv = sum(1 for x in w["entries"].values() if not x.get("disable"))
    print("%-22s %d Eintraege, davon aktiv %d" % (datei, len(w["entries"]), aktiv))
    if LOS:
        os.makedirs(SICHER, exist_ok=True)
        ziel = os.path.join(SICHER, datei)
        if not os.path.exists(ziel):
            shutil.copy2(p, ziel)
        with open(p, "w", encoding="utf-8", newline=nl) as fh:
            json.dump(w, fh, ensure_ascii=False, indent=2)
print("geschrieben" if LOS else "PROBELAUF")

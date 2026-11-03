# -*- coding: utf-8 -*-
"""Kalender je Tag und Phase: frei, geskriptet, Pflicht-Event, Auftrag (Duc 31.10.2026).

Liest Plan, Story, Pflicht-Events und Auftragsorte aus den Spieldaten und schreibt docs/abnahme/kalender_phasen/index.html.
Favours bleiben draussen (Inhalte vor Duc geheim).

  python werkzeuge\\kalender_seite.py
"""
import html, json, os, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import hauptstory, zustand  # noqa: E402

MD = os.path.join(EDEN, "module", "eden_rise")
TEXTE = json.load(open(os.path.join(EDEN, "werkzeuge", "kalender_texte.json"), encoding="utf-8"))
FEHLT = []
AUS = os.path.join(EDEN, "docs", "abnahme", "kalender_phasen", "index.html")
TAGE = range(1, 22)
PHASE_NAME = {"fruehstueck": "Frühstück", "tag": "Tag", "nachmittag": "Nachmittag", "dinner": "Dinner", "abend": "Abend", "nacht": "Nacht"}
# Aus docs/wiki/welt/akt2_kalender.md: geplant, aber in den Spieldaten noch nicht gebaut
GEPLANT = {(15, "fruehstueck"): "Frist bis Tag 21", (16, "tag"): "Tauchgang öffnet",
           (19, "tag"): "Manöver", (20, "abend"): "Kriegsrat, dann ruhige letzte Nacht", (21, "tag"): "Belagerung"}
# Auftraege ohne feste Tage: Ab wann sie frühestens offen sind, steht in den Bedingungen ihrer Orte (auftraege.json)
AUFTRAEGE = [("Kloster", 4, 21, ("tag", "nachmittag"), "ab Tag 4, wenn der Faden da ist"),
             ("Berge", 9, 21, ("tag", "nachmittag"), "ab Tag 9, nach dem Kloster"),
             ("Grotte", 11, 21, ("tag", "nachmittag"), "ab Tag 11, nach Totòs Beichte"),
             ("Kevin", 12, 14, ("tag", "nachmittag"), "Tag 12 bis 14"),
             ("Red Trio", 11, 14, ("tag", "nachmittag"), "bis Tag 14, frühestens nach Kloster und Grotte"),
             ("High Tide", 11, 21, ("abend",), "abends, nach der Grotte")]
MISSION_EVENTE = ("a2_toto_beichte", "a2_kevin_raub")     # oeffnen einen Auftrag; dazu alle rt_* (Red Trio)


def laden(name):
    return json.load(open(os.path.join(MD, name), encoding="utf-8"))


def erzeugen():
    modul, story = laden("modul.json"), laden("story.json")
    ev = laden("ereignisse.json")["events"]
    ev = ev if isinstance(ev, list) else list(ev.values())
    pflicht = [e for e in ev if (e.get("wann") or {}).get("pflicht") and "favour" not in e.get("id", "")]
    phasen = modul["zeitraster"]["phasen"]
    z = zustand.neu(modul, "entspannt")
    zustand.persona_setzen(z, modul, modul["personas"][0])
    zellen, spaeter = {}, []
    for t in TAGE:
        z["tag"], z["plan"] = t, None
        plan = hauptstory.plan_bauen(z, modul, MD)
        z["plan"] = plan
        for ph in phasen:
            c = plan["phasen"].get(ph)
            defs = (story["wochenbogen"].get(str(t)) or {}).get("phasen", {}).get(ph, [])
            zellen[(t, ph)] = {"frei": bool(c and c.get("frei")), "leer": not c,
                               "karten": sum(1 for s in (c or {}).get("szenen", []) if s.get("frei")),
                               "story": [{"id": d["id"], "titel": d["titel"]} for d in defs], "events": [], "auftraege": []}
    gesehen = set()
    for e in pflicht:
        w = e["wann"]
        von, bis = w["tage"]
        if bis - von > 1 or w.get("akt2"):      # breite oder zweite Fenster sind Folge-Events: nur mit Bedingung, gehoeren in die Notiz
            spaeter.append(e)
            continue
        for t in range(von, bis + 1):
            for ph in w.get("phasen", []):
                if (t, ph) not in zellen:
                    continue
                k = (t, ph, e.get("titel"))
                if k in gesehen:
                    continue
                gesehen.add(k)
                mission = e["id"] in MISSION_EVENTE or e["id"].startswith("rt_")
                zellen[(t, ph)]["events"].append({"id": e["id"], "titel": e.get("titel", ""), "bedingt": bool(w.get("bedingung")), "mission": mission})
    for name, von, bis, phs, _ in AUFTRAEGE:
        for t in range(von, bis + 1):
            for ph in phs:
                zellen[(t, ph)]["auftraege"].append(name)
    return phasen, story, zellen, spaeter


def art(c):
    if not c["frei"] and (c["story"] or c["events"]):
        return "s"
    if c["leer"]:
        return "x"
    if any(e["mission"] for e in c["events"]):
        return "m"
    if c["events"] or c["story"]:
        return "e"
    return "a" if c["auftraege"] else "f"


NAME = {"s": "Geskriptet", "m": "Pflicht-Event zu einem Auftrag, danach frei", "e": "Pflicht-Event, danach frei", "a": "Frei, Auftrag möglich", "f": "Frei", "x": "Entfällt"}
E = html.escape


def erklaerung(schluessel):
    text = TEXTE["szenen"].get(schluessel)
    if not text:
        FEHLT.append(schluessel)
        return '<small class="er fehlt">Erklärung fehlt</small>'
    return '<small class="er">%s</small>' % E(text)


ERSTER = {}


def zelle(t, ph, c):
    a = art(c)
    teile = []
    tag0 = [e for e in c["events"] if e["id"].startswith("t0_")]
    if tag0:
        teile.append("<b>Prolog Antibes</b>" + erklaerung("prolog"))
    for d in c["story"]:
        teile.append("<b>%s</b>%s" % (E(d["titel"]), erklaerung(d["id"])))
    for e in c["events"]:
        if e in tag0:
            continue
        teile.append('<span class="ev%s">%s%s</span>%s' % (" mi" if e["mission"] else "", E(e["titel"]), ' <i title="nur unter einer Bedingung">?</i>' if e["bedingt"] else "", erklaerung(e["id"])))
    if c["frei"]:
        wer = "Frei: Es wird eine Figur angeboten." if c["karten"] == 1 else "Frei: Zeit mit einer von %d Figuren." % c["karten"]
        teile.append('<span class="fr">%s</span>' % wer)
    if c["auftraege"] and c["frei"]:
        neu = [n for n in c["auftraege"] if ERSTER.get(n) == (t, ph)]
        teile.append('<span class="au">Oder Ausflug: %s</span>' % E(", ".join(c["auftraege"])))
        for n in neu:
            teile.append('<small class="er"><b>%s, neu:</b> %s</small>' % (E(n), E(TEXTE["auftraege"][n])))
    if (t, ph) in GEPLANT:
        teile.append('<span class="pl">geplant: %s</span>' % E(GEPLANT[(t, ph)]))
    return '<td class="%s">%s</td>' % (a, "".join("<div>%s</div>" % x for x in teile) or "–")


def seite(phasen, story, zellen, spaeter):
    ERSTER.clear()
    for t in TAGE:
        for p in phasen:
            if zellen[(t, p)]["frei"]:
                for n in zellen[(t, p)]["auftraege"]:
                    ERSTER.setdefault(n, (t, p))
    zaehl = {}
    for c in zellen.values():
        zaehl[art(c)] = zaehl.get(art(c), 0) + 1
    legende = "".join('<span class="lg %s">%s · %d</span>' % (k, NAME[k], zaehl.get(k, 0)) for k in "smeafx")
    kopf = "".join("<th>%s</th>" % PHASE_NAME[p] for p in phasen)
    zeilen = []
    for t in TAGE:
        titel = (story["wochenbogen"].get(str(t)) or {}).get("titel") or ""
        zeilen.append('<tr><th class="tg">Tag %d<small>%s</small></th>%s</tr>' % (t, E(titel), "".join(zelle(t, p, zellen[(t, p)]) for p in phasen)))
    auftraege = "".join("<li><b>%s</b> (%s): %s</li>" % (E(n), E(w), E(TEXTE["auftraege"][n])) for n, _, _, _, w in AUFTRAEGE)
    gruppen = {}
    for e in spaeter:
        k = ("Red Trio" if e["id"].startswith("rt_") else "Danzels Aufträge" if e["id"].startswith("sn_")
             else "Romanzen-Leiter und Echo" if e["id"].startswith("rm_") else e.get("titel", ""))
        gruppen[k] = gruppen.get(k, 0) + 1
    folge = " · ".join("%s (%d)" % (E(k), v) for k, v in gruppen.items())
    return """<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Eden Kalender</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#10151b;--flaeche:#18202a;--linie:#2c3744;--text:#e8edf2;--leise:#9aa8b6;--s:#4b3a78;--m:#1f4f7d;--e:#6b4d17;--a:#1d5a4a;--f:#1a3a30;--x:#1b2027}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.35 system-ui,Segoe UI,sans-serif;padding:24px}
h1{font-size:24px;margin:0 0 6px}p{margin:0 0 14px;color:var(--leise);max-width:980px}.leg{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}
.lg{padding:5px 10px;border-radius:8px;font-size:13px}.s{background:var(--s)}.m{background:var(--m)}.e{background:var(--e)}.a{background:var(--a)}.f{background:var(--f)}.x{background:var(--x);color:var(--leise)}
table{border-collapse:separate;border-spacing:3px;width:100%%;table-layout:fixed}th{position:sticky;top:0;background:var(--bg);padding:8px;text-align:left;font-size:14px;z-index:1}
th.tg{position:static;width:150px;background:var(--flaeche);border-radius:8px;vertical-align:top}th.tg small{display:block;font-weight:400;color:var(--leise);font-size:12px}
thead th:first-child{width:150px}td{vertical-align:top;padding:7px 8px;border-radius:8px;font-size:12.5px}td div+div{margin-top:7px}.er{display:block;font-size:12px;line-height:1.4;margin-top:2px;opacity:.92;font-weight:400}.fehlt{color:#ffb4a8}td b{font-weight:600}
.ev{display:block}.ev.mi{font-weight:600}.ev i{font-style:normal;opacity:.75}.fr{color:#bfe9d6}.au{color:#a8d8ff}.pl{color:var(--leise);font-style:italic}
section{margin-top:22px;max-width:980px}h2{font-size:18px;margin:0 0 8px}li{margin:3px 0}
</style></head><body>
<h1>Eden Kalender: Tag 1 bis 21</h1>
<p>Erzeugt aus den Spieldaten mit <code>werkzeuge/kalender_seite.py</code>, die Erklärungen stehen in <code>werkzeuge/kalender_texte.json</code>. Titel bleiben englisch wie im Spiel. Geskriptet heißt: Die Phase ist belegt. Ein Pflicht-Event läuft vor der Phase und kostet sie nicht. Ein Fragezeichen heißt: nur unter einer Bedingung. In freien Phasen hat Duc zwei Aktionen, Frühstück und Nacht bieten nur eine Figur an. Zufalls-Events, Handy-Nachrichten ohne Pflicht und Favours stehen nicht drin.</p>
<div class="leg">%s</div>
<table><thead><tr><th>Tag</th>%s</tr></thead><tbody>%s</tbody></table>
<section><h2>Aufträge: wann frühestens</h2><p>Sie belegen keine Phase von selbst. Duc kann sie in den markierten freien Phasen starten, und das kostet dann diese Phase. Die Tage sind die frühesten laut Bedingungen, im Spiel hängen sie vom Fortschritt ab.</p><ul>%s</ul></section>
<section><h2>Folge-Events ohne festen Tag</h2><p>Laufen nur, wenn eine Bedingung erfüllt ist, darum stehen sie nicht in den Zellen: %s</p></section>
</body></html>""" % (legende, kopf, "".join(zeilen), auftraege, folge)


def main():
    phasen, story, zellen, spaeter = erzeugen()
    os.makedirs(os.path.dirname(AUS), exist_ok=True)
    with open(AUS, "w", encoding="utf-8", newline="\n") as f:
        f.write(seite(phasen, story, zellen, spaeter))
    # Kurzfassung fuer den Chat
    sys.stdout.reconfigure(encoding="utf-8")
    print("Tag | " + " | ".join(PHASE_NAME[p] for p in phasen))
    for t in TAGE:
        print(t, "|", " | ".join(art(zellen[(t, p)]).upper() for p in phasen))
    for k, c in sorted(zellen.items()):
        if c["story"] or c["events"]:
            print(k, art(c), c["story"], [(e["titel"], "?" if e["bedingt"] else "", "M" if e["mission"] else "") for e in c["events"] if not e["id"].startswith("t0_")])
    print("Fehlende Erklaerungen:", sorted(set(FEHLT)) or "keine")
    print(AUS)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Tischszenen (Duc 27.10.2026, Kochen Stern 1): Kocht Duc das Lieblingsgericht einer Person als Teller fuer genau diese Person
und sie isst es zum ersten Mal ganz ("liebt"), kommt statt der kleinen Meldung eine kurze, vertonte Szene.

Regel der Engine: der CODE loest aus und bucht, die Zeilen sind fest geschrieben (module\\<modul>\\tisch.json, Builder
werkzeuge\\eden_rise\\tisch_eden_rise.py, Turbo-Tags in stimme_tags.json) - das Modell schreibt hier nichts.
  * Ausloesen: kochen_aktion (kern/handel.py), nur Teller fuer eine Person, nur Stufe "liebt" (also erster voller Treffer;
    misslingt der Wurf, bleibt es bei "gut" und die Szene wartet). Jede Figur hoechstens einmal (z["tisch_gesehen"]).
  * Beats: Titelkarte, Teller (zwei Fassungen: normal/kritischer Wurf, nur Text), erster Bissen, Duc-Antwort (nur Text, nur bei
    nicht-europaeischen Gerichten), Erinnerung 1 und 2, Folgenkarte. Vertont sind nur die Figurenzeilen (tisch.<figur>.<0|1|2>).
  * Der Spielstand traegt z["tisch"] nur, solange die Szene offen ist (Neuladen zeigt sie von vorn); Weiterklicken = Aktion
    tisch_fertig. Spielstaende ohne Szene bekommen keinen neuen Schluessel."""
import json, os

_CACHE = {}
FOLGEN_TITEL = "Favourite dish discovered"


def daten(modul):
    """module\\<modul>\\tisch.json -> {figur: Szene} (nach Aenderungszeit zwischengespeichert); ohne Datei: leer."""
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""), "tisch.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    c = _CACHE.get(pfad)
    if c and c[0] == mt:
        return c[1]
    try:
        d = json.load(open(pfad, encoding="utf-8")).get("szenen", {})
    except (OSError, ValueError):
        d = {}
    _CACHE[pfad] = (mt, d)
    return d


def ausloesen(z, modul, pid, item, stufe, ergebnis, zeilen):
    """Teller fuer pid ist gekocht (stufe = Ergebnis von handel.koch_stufe, ergebnis = Wurf). -> True, wenn die Szene startet."""
    s = daten(modul).get(pid)
    if stufe != "liebt" or not s or s["item"] != item or pid in z.get("tisch_gesehen", []):
        return False
    z.setdefault("tisch_gesehen", []).append(pid)
    z["tisch"] = {"pid": pid, "item": item, "kritisch": ergebnis == "kritisch", "zeilen": list(zeilen)}
    return True


def erinnerung_als_vorliebe(z, modul, pid, item):
    """Die erste Erinnerung steht danach im Figurenprofil (kern/vorlieben.py) - aber nur, wenn die Vorliebe gerade erst durch dieses
    Gericht entdeckt wurde; was Duc schon anders wusste (Geschenk, Tratsch), bleibt unberuehrt."""
    e = next((v for v in z.get("vorlieben", []) if v["figur"] == pid and v["item"] == item), None)
    s = daten(modul).get(pid)
    if e and s and e.get("quelle") == "gericht":
        e["text"] = s["erinnerung"][0]["text"]


def ansicht(z, modul, sprite):
    """Fuer den Client: die Beats der offenen Szene, fertig mit Sprite je Figurenzeile (sprite(pid, gefuehl) -> URL oder None)."""
    t = z.get("tisch")
    s = daten(modul).get((t or {}).get("pid"))
    if not t or not s:
        return None
    pid = t["pid"]
    p = modul["personen"].get(pid) or {}
    label = (modul["items"].get(t["item"]) or {}).get("label", t["item"])

    def rede(i, r):
        return {"art": "rede", "id": "tisch.%s.%d" % (pid, i), "text": r["text"], "sprite": sprite(pid, r["gefuehl"]), "gefuehl": r["gefuehl"]}
    beats = [{"art": "titel", "titel": s["titel"], "label": label, "sprite": sprite(pid, "neutral")},
             {"art": "teller", "text": s["teller"]["kritisch" if t["kritisch"] else "normal"], "sprite": sprite(pid, "neutral")},
             rede(0, s["bissen"])]
    if s.get("antwort"):
        beats.append({"art": "antwort", "text": s["antwort"], "sprite": sprite(pid, s["bissen"]["gefuehl"])})
    beats += [rede(1, s["erinnerung"][0]), rede(2, s["erinnerung"][1]),
              {"art": "folgen", "titel": FOLGEN_TITEL, "zeilen": t["zeilen"], "sprite": sprite(pid, "joy")}]
    return {"pid": pid, "name": p.get("name", pid), "item": t["item"], "label": label, "beats": beats}


def zeile(modul, zid):
    """'tisch.<figur>.<0|1|2>' -> (Figur, Klartext) fuer die Vertonung (nur feste Zeilen aus tisch.json) oder (None, None)."""
    teile = zid.split(".")
    if len(teile) != 3 or teile[0] != "tisch" or teile[2] not in ("0", "1", "2"):
        return None, None
    s = daten(modul).get(teile[1])
    if not s:
        return None, None
    n = int(teile[2])
    return teile[1], (s["bissen"] if n == 0 else s["erinnerung"][n - 1])["text"]


def fertig(z):
    """Weiterklicken am Ende (oder Skip): die Szene ist vorbei."""
    z.pop("tisch", None)

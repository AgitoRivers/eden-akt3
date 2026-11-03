# -*- coding: utf-8 -*-
r"""Fester Testlauf (18.10.2026): spielt ein Modul automatisch von der Persona bis zum Ende - ohne Sprachmodell,
ohne Stimme, ohne Netz, mit festen Wuerfeln - und vergleicht den Endzustand mit einer gespeicherten Referenz.

Wozu: Umbauten am Kern (Entkoppeln, Rollen in die Moduldaten) duerfen am Spielverhalten nichts aendern.
Gleicher Endzustand = gleiche Regeln. Laeuft in einem Wegwerf-Ordner, fasst weder Spielstaende noch Konfiguration an.

  python tests\lauf_test.py                      vergleichen (Exit 1 bei Abweichung)
  python tests\lauf_test.py --speichern          Referenz neu schreiben (nur nach gewollten Regelaenderungen!)
  python tests\lauf_test.py --modul eden_rise --seed 7

Der Bot macht je Tag: alle angebotenen Missionen, einmal Kochen fuer die Crew, dann immer die erste Wahl,
in Szenen zwei feste Saetze und Szenenende, bei Ereignissen die erste Antwort.
"""
import argparse, copy, json, os, random, shutil, subprocess, sys, tempfile, time, uuid

HIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HIER)
REFERENZ = os.path.join(HIER, "referenz")
MAX_SCHRITTE = 3000

# Dict-/Set-Reihenfolge haengt vom Hash-Seed ab -> fest, sonst ist der Lauf nicht wiederholbar
if os.environ.get("PYTHONHASHSEED") != "0":
    sys.exit(subprocess.call([sys.executable] + sys.argv, env=dict(os.environ, PYTHONHASHSEED="0")))

sys.path.insert(0, BASE)
import urllib.request  # noqa: E402


def _kein_netz(*a, **k):
    raise RuntimeError("Testlauf: kein Netz")


urllib.request.urlopen = _kein_netz           # vor dem Import der Engine - nichts darf hinaus

import eden  # noqa: E402
from kern import llm, stimme  # noqa: E402

llm.bereit = lambda: True
llm.chat = lambda system, user, sampler=None, max_tokens=300, grammar=None: ("She nods and says nothing.", 0.0)
llm.json_chat = lambda system, user, grammar, max_tokens=120, sampler=None: (None, 0.0)
stimme.chatterbox = lambda *a, **k: None
stimme.chatterbox_bereit = lambda: False


def vorbereiten(modul, ordner, seed=0):
    _zaehler = [seed * 100000]    # Spielstand-ID je Seed verschieden - viele Zufallsquellen haengen an ihr

    def fest_uuid():
        _zaehler[0] += 1
        return uuid.UUID(int=_zaehler[0])
    uuid.uuid4 = fest_uuid
    time.strftime = lambda fmt, *a: "2026-10-18 12:00"
    # Sprite-Ordner (st_daten) werden nur gelesen; Stimmen leer = keine Vertonung
    echt = json.load(open(os.path.join(BASE, "eden-config.json"), encoding="utf-8-sig"))
    cfg = {"modul": modul, "aktiv": None, "vorschlaege": False, "stimmen": {}, "st_daten": echt.get("st_daten", "")}
    eden.CFG_PFAD = os.path.join(ordner, "eden-config.json")
    eden.STAENDE = os.path.join(ordner, "spielstaende")
    os.makedirs(eden.STAENDE)
    json.dump(cfg, open(eden.CFG_PFAD, "w", encoding="utf-8"))
    eden._DATEI_CACHE.clear()


def schritt(z, protokoll):
    """Eine Bot-Entscheidung -> (aktion, daten) oder None (fertig)."""
    st = z["status"]
    if st == "ende":
        return None
    if st == "persona_wahl":
        return "persona", {"index": 0}
    if st == "prolog":
        return "prolog", {}
    if st in ("warte_auf_plan", "plan_fehler"):
        return "plan_laden", {}
    if st == "kabine":
        return "kabine_zurueck", {}             # Modell B: Kabine kostet keine Zeit, Ausruhen gibt es nicht mehr
    if st == "kampf":                            # Maxwells erste Lektion (Tag 2): angreifen, perfekt parieren
        k = z["kampf"]
        if k["phase"] == "ende":
            return "kampf_schliessen", {}
        if k["phase"] == "parade":
            return "kampf_parade", {"ergebnis": "perfekt", "revision": k["revision"]}
        return "kampf_zug", {"befehl": "angriff", "ziel": None, "revision": k["revision"]}
    if st == "verhandlung":                      # Anhoerung (Variante B): erste Verdaechtige, je Runde die erste passende Karte
        v = z["verhandlung"]
        if v["fertig"]:
            return "verhandlung", {"was": "schliessen"}
        modul = eden.modul_laden()
        if v["schritt"] == "anklage":
            return "verhandlung", {"was": "anklage", "pid": eden.anhoerung._verdaechtige(z, modul)[0]}
        if v["schritt"] == "rolle":
            return "verhandlung", {"was": "rolle", "ehrlich": True}
        if v["schritt"] == "plaedoyer":
            return "verhandlung", {"was": "plaedoyer", "art": "gnade"}
        r = eden.anhoerung._runde(v)
        saetze = (v.get("aussage") or {}).get("saetze") or []
        i = next((n for n, s in enumerate(saetze) if s["falsch"]), None)     # Bot kennt die falsche Zeile
        wid = saetze[i].get("widerlegt") if i is not None else None
        fid = next((f for f in sorted(eden.ermittlung.stand(z)["bekannt"])
                    if eden.anhoerung._karte_passt(z, r, f) == "ja" and (not wid or f in wid)), None)
        return "verhandlung", ({"was": "present", "fid": fid, "satz": i} if fid and i is not None else {"was": "aufgeben"})
    if st == "taktik":                           # Belagerung (Duc 01.11.2026): eigene Tests in test_taktik.py, der Lauf kuerzt ab
        eden.taktik.BOT_ERLAUBT = True
        return "taktik", {"was": "bot_sieg"}
    if st == "sturm":                            # Sturm an Tag 5 (27.10.2026): Crew der Reihe nach auf die Posten, einmal rennen
        v = eden.sturm.aktiv(z)
        if v["fertig"]:
            return "sturm", {"was": "schliessen"}
        if v["schritt"] == "einteilen":
            posten = list(eden.sturm.daten(eden.moddir())["posten"])
            return "sturm", {"was": "einteilen", "posten": dict(zip(posten, v["crew"]))}
        return "sturm", {"was": "sprint", "rennen": True}
    if st == "ereignis":
        ev = z.get("event") or {}
        if ev.get("ergebnis"):
            return "event_schliessen", {}
        # "ort_waehlen" (Treffpunkt aussuchen) hat noch keine Ortswahl in der Engine (offen seit 18.10.2026) - auslassen
        # Favours (29.10.2026): der Bot nimmt Bitten an, solange die Energie reicht (sonst der kostenlose Weg)
        opts = eden.ereignisse.daten(eden.moddir())["_index"][ev["id"]]["optionen"]
        energie = z["werte"].get("energie", 0)
        return "event_wahl", {"index": next((i for i, o in enumerate(opts) if o.get("art") != "ort_waehlen"
                                             and o.get("energie", 0) <= energie), 0)}
    if st == "szene":
        sz = z["szene"]
        if sz.get("wahlmoment_offen"):
            return "waehlen", {"index": 0}
        a = szenen_extra(z, sz, protokoll)
        if a:
            return a
        if sum(1 for e in sz.get("log", []) if e.get("art") == "duc") < 2:
            return "zug", {"text": "I listen and help where I can."}
        return "ende", {}
    if st == "wahl":
        tag = "t%d" % z["tag"]
        if tag not in protokoll["erledigt"]:
            protokoll["erledigt"][tag] = True
            return "_tagesarbeit", {}
        return "wahl", {"id": z["optionen"][0]}
    raise RuntimeError("Unbekannter Status: " + st)


def szenen_extra(z, sz, protokoll):
    """Je Szene einmal: ein Geschenk aus dem Inventar an die erste anwesende Figur, dann eine freie Geste."""
    modul = eden.modul_laden()
    schl = "%d-%s-%s" % (z["tag"], z["phase"], sz.get("def", {}).get("id"))
    da = [p for p in sz.get("figuren", []) if p in modul["personen"]]
    if schl + ":geben" not in protokoll["erledigt"]:
        protokoll["erledigt"][schl + ":geben"] = True
        gabe = next((i for i in z["inventar"] if modul["items"].get(i, {}).get("art") in ("geschenk", "snack")), None)
        if gabe and da and not sz["def"].get("anruf"):
            return "geben", {"id": gabe, "an": da[0]}
    if schl + ":geste" not in protokoll["erledigt"]:
        protokoll["erledigt"][schl + ":geste"] = True
        g = eden.gesten.ansicht(z, modul, sz) if not sz["def"].get("anruf") else None
        for eintrag in (g or {}).get("liste", []):
            frei = [p for p, x in eintrag["je"].items() if not x["gesperrt"] and not x["abgenutzt"]]
            if frei:
                return "geste", {"id": eintrag["id"], "an": frei[0]}
    return None


def tagesarbeit(z, protokoll):
    """Laeden ansehen (Preise/Sortiment ins Protokoll), je Laden das Billigste kaufen, eins an Totò verkaufen,
    Missionen, Kochen - Fehler zaehlen mit (z. B. keine Energie), sind aber kein Abbruch."""
    modul = eden.modul_laden()
    V = eden.showrunner.vorrat(eden.moddir())
    eden.handel.init(z, modul)
    blick = {k: eden.handel.sortiment(z, modul, k) for k in sorted(modul.get("laeden") or {})
             if not (modul["laeden"][k].get("farm") or modul["laeden"][k].get("werkzeug_laden"))}   # Nonnas Farm, Petrus Werkstatt: keine Warenlaeden
    protokoll["schritte"].append(["laeden", z["tag"], blick])
    for k, waren in blick.items():
        if waren:
            w = min(waren, key=lambda x: (x["preis"], x["id"]))
            versuch(("kaufen", {"laden": k, "id": w["id"]}), protokoll)
            z = eden.aktiv()
    if "toto" in (modul.get("laeden") or {}):
        ank = eden.handel.ankauf(z, modul)
        if ank:
            versuch(("verkaufen", {"art": ank[0]["art"], "id": ank[0]["id"]}), protokoll)
            z = eden.aktiv()
    for j in eden.handel.jobs_heute(z, modul, V):
        versuch(("job", {"id": j["id"]}), protokoll)
    gerichte = eden.handel.gerichte(z, modul)
    if gerichte:
        versuch(("kochen", {"id": gerichte[z["tag"] % len(gerichte)]["id"], "fuer": "crew"}), protokoll)


def versuch(a, protokoll):
    try:
        z = eden.aktion(*a)
        eden.ansicht(eden.aktiv())            # die Anzeige (GET /api/stand) muss bei jedem Stand durchlaufen
        protokoll["schritte"].append([a[0], a[1].get("id") or a[1].get("index"), z["tag"], z["phase"], z["status"]])
    except ValueError as e:
        protokoll["schritte"].append([a[0], a[1].get("id") or a[1].get("index"), "abgelehnt", str(e)])


def laufen(modul, seed):
    ordner = tempfile.mkdtemp(prefix="eden_test_")
    try:
        vorbereiten(modul, ordner, seed)
        random.seed(seed)
        protokoll = {"schritte": [], "erledigt": {}}
        z = eden.aktion("neu", {"modus": "ironman"})
        for _ in range(MAX_SCHRITTE):
            a = schritt(z, protokoll)
            if a is None:
                break
            if a[0] == "_tagesarbeit":
                tagesarbeit(z, protokoll)
            else:
                versuch(a, protokoll)
            z = eden.aktiv()
        else:
            raise RuntimeError("Testlauf endet nicht (%d Schritte)" % MAX_SCHRITTE)
        return {"modul": modul, "seed": seed, "schritte": protokoll["schritte"], "ende": normalisieren(z)}
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


def normalisieren(z):
    z = copy.deepcopy(z)
    for k in ("erstellt",):
        z.pop(k, None)
    return json.loads(json.dumps(z, ensure_ascii=False, sort_keys=True))


def unterschiede(a, b, pfad="", aus=None):
    aus = [] if aus is None else aus
    if len(aus) >= 40:
        return aus
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                aus.append("%s/%s: nur in %s" % (pfad, k, "Referenz" if k in a else "neu"))
            else:
                unterschiede(a[k], b[k], "%s/%s" % (pfad, k), aus)
    elif isinstance(a, list) and isinstance(b, list) and len(a) != len(b):
        aus.append("%s: Laenge %d -> %d" % (pfad, len(a), len(b)))
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            unterschiede(x, y, "%s[%d]" % (pfad, i), aus)
    elif a != b:
        aus.append(pfad + ": anders")          # keine Werte ausgeben - der Zustand enthaelt Fall-Aufloesungen (Spoiler)
    return aus


def main():
    # Oberflaeche aus einem Guss (docs/wiki/systeme/ui_stil.md): erst der Waechter, dann der Lauf
    subprocess.check_call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_ui_einheit.py")], stdout=subprocess.DEVNULL)
    ap = argparse.ArgumentParser()
    ap.add_argument("--modul", default="eden_rise")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--speichern", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    erg = laufen(a.modul, a.seed)
    ziel = os.path.join(REFERENZ, "%s_seed%d.json" % (a.modul, a.seed))
    e = erg["ende"]
    print("Lauf: %d Schritte, Ende Tag %s, Status %s, %d Flags, %d Missionen erledigt" % (
        len(erg["schritte"]), e["tag"], e["status"], len(e["flags"]), len(e.get("jobs_erledigt", []))))
    if a.speichern:
        os.makedirs(REFERENZ, exist_ok=True)
        json.dump(erg, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
        print("Referenz geschrieben:", ziel)
        return 0
    if not os.path.exists(ziel):
        print("Keine Referenz - erst mit --speichern anlegen:", ziel)
        return 1
    ref = json.load(open(ziel, encoding="utf-8"))
    diff = unterschiede({"schritte": ref["schritte"], "ende": ref["ende"]}, {"schritte": erg["schritte"], "ende": erg["ende"]})
    if diff:
        print("ABWEICHUNG (%s%d):" % ("mind. " if len(diff) >= 40 else "", len(diff)))
        print("\n".join("  " + d for d in diff))
        return 1
    print("OK - identisch mit der Referenz")
    return 0


if __name__ == "__main__":
    sys.exit(main())

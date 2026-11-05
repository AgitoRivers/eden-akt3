# -*- coding: utf-8 -*-
r"""Durchlauf-Bot Akt 3 (Duc 05.11.2026): spielt Tag 24 bis 35 am Stueck durch die echte Engine, ohne Sprachmodell,
ohne Stimme, ohne Netz. Startet nicht bei Tag 1, sondern baut einen Spielstand nach dem Cliffhanger von Akt 2
(akt2_ende) und schaltet akt3_spielbar nur im Speicher an. Sucht Sackgassen, Fehler der Engine, Szenen, die nie kommen,
und zaehlt Pflicht-Szenen je Tag und Phase.

  python tests\bot_akt3.py                 sechs Laeufe mit verschiedenen Ausgangslagen, Bericht auf der Konsole
  python tests\bot_akt3.py --laeufe 2 --json bericht.json

Braucht keine eden-config.json (schreibt eine leere in einen Wegwerf-Ordner). Exit 1, wenn ein Lauf abbricht.
Der Bericht nennt nur Event-IDs und Zaehler, keine Texte (Spoilerschutz)."""
import argparse, collections, json, os, random, shutil, sys, tempfile, time, uuid

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402  (setzt PYTHONHASHSEED, sperrt das Netz, ersetzt Sprachmodell und Stimme)

eden = L.eden
MAX_SCHRITTE = 4000
# Figurenkarten (RoleplayGen) liegen nur bei Duc lokal; das Sprachmodell ist ersetzt, also reicht ein Platzhalter
_karte_echt = eden.szene.karte
def _karte(modul, p):
    try:
        return _karte_echt(modul, p)
    except OSError:
        return {"bogen": p.get("beschreibung", ""), "beispiele": ""}
eden.szene.karte = _karte

# Ausgangslagen nach Akt 2 (nur Flags, die es im Spiel schon gibt)
BASIS = ["akt2_ende", "buenaventura_schwur", "mochis_offen", "frederico_lebt", "werkstatt_offen"]
LAGEN = {
    "yacht_kaputt_alle_da": BASIS + ["tk_yacht_weg", "tk_haus_weg_post", "tk_haus_weg_bar", "rt_charly_bleibt", "rt_bibi_bleibt"],
    "yacht_heil_charly_weg": BASIS + ["tk_haus_weg_batu", "tk_haus_weg_werkstatt", "rt_charly_weg", "rt_bibi_bleibt"],
    "alles_brennt": BASIS + ["tk_yacht_weg"] + ["tk_haus_weg_" + h for h in ("post", "batu", "bar", "werkstatt")]
                    + ["rt_charly_bleibt", "rt_bibi_bleibt", "bl_verband_wolff", "gennaro_verschwunden", "sirene_weg"],
    "wenig_kaputt": BASIS + ["tk_haus_weg_post", "rt_charly_bleibt"],
}


def vorbereiten(ordner, seed):
    """Wie lauf_test.vorbereiten, aber ohne echte eden-config.json; akt3_spielbar nur im Speicher."""
    zaehler = [seed * 100000 + 7]

    def fest_uuid():
        zaehler[0] += 1
        return uuid.UUID(int=zaehler[0])
    uuid.uuid4 = fest_uuid
    time.strftime = lambda fmt, *a: "2026-11-05 12:00"
    eden.CFG_PFAD = os.path.join(ordner, "eden-config.json")
    eden.STAENDE = os.path.join(ordner, "spielstaende")
    os.makedirs(eden.STAENDE)
    json.dump({"modul": "eden_rise", "aktiv": None, "vorschlaege": False, "stimmen": {}, "st_daten": ""},
              open(eden.CFG_PFAD, "w", encoding="utf-8"))
    eden._DATEI_CACHE.clear()
    orig = eden.modul_laden.__wrapped__ if hasattr(eden.modul_laden, "__wrapped__") else eden.modul_laden
    cache = {}

    def modul_akt3(mid=None):
        m = orig(mid)
        if id(m) not in cache:
            k = dict(m)
            k["akt3_spielbar"] = True
            k["zeitraster"] = dict(m["zeitraster"], tage=35)
            cache.clear()
            cache[id(m)] = k
        return cache[id(m)]
    modul_akt3.__wrapped__ = orig
    eden.modul_laden = modul_akt3


def schritt(z, protokoll, rnd):
    """lauf_test.schritt, aber mit Zufall bei Events und Karten (gesteuert ueber den Seed)."""
    st = z["status"]
    if st == "ereignis":
        ev = z.get("event") or {}
        if ev.get("ergebnis"):
            return "event_schliessen", {}
        opts = eden.ereignisse.daten(eden.moddir())["_index"][ev["id"]]["optionen"]
        energie = z["werte"].get("energie", 0)
        gut = [i for i, o in enumerate(opts) if o.get("art") != "ort_waehlen" and o.get("energie", 0) <= energie] or [0]
        return "event_wahl", {"index": rnd.choice(gut)}
    if st == "wahl":
        tag = "t%d" % z["tag"]
        if tag not in protokoll["erledigt"]:
            protokoll["erledigt"][tag] = True
            return "_tagesarbeit", {}
        return "wahl", {"id": rnd.choice(z["optionen"])}
    if st == "kommission":
        k = z.get("kommission") or {}
        if k.get("fertig"):
            return "kommission", {"was": "schliessen"}
        if k.get("schritt") == "plaedoyer":
            return "kommission", {"was": "plaedoyer", "art": rnd.choice(["alles", "teil"])}
        return "kommission", {"was": "nichts"}
    return L.schritt(z, protokoll)


def akt3_stand(lage, rnd):
    """Neues Spiel bis zur ersten Wahl, dann auf Tag 24 Fruehstueck nach Akt 2 setzen."""
    protokoll = {"schritte": [], "erledigt": {}}
    z = eden.aktion("neu", {"modus": "ironman"})
    for _ in range(200):
        if z["status"] == "wahl":
            break
        a = L.schritt(z, protokoll)
        L.versuch(a, protokoll)
        z = eden.aktiv()
    z = eden.aktiv()
    z["tag"], z["phase"] = 24, "fruehstueck"
    z["flags"] = sorted(set(z.get("flags", [])) | set(LAGEN[lage]))
    z.setdefault("flag_tag", {})
    for f in LAGEN[lage]:
        z["flag_tag"].setdefault(f, 23)
    for pid in ("holm", "megan", "rosi", "chiara", "lola", "alva", "petru", "mina"):
        z.setdefault("vertrauen", {}).setdefault(pid, rnd.choice([2, 3, 4, 5]))
    z["heute"], z["optionen"], z["meldungen"] = [], [], []
    modul = eden.modul_laden(z.get("modul"))
    if not eden.plan.plan_laden(z, modul, eden.moddir(z["modul"])):
        raise RuntimeError("Kein Tagesplan fuer Tag 24")
    eden.weiter(z, modul, eden.plan.phase_beginnen(z))     # wie die Engine einen neuen Tag beginnt
    eden.sichern(z)
    return eden.aktiv()


def lauf(lage, seed):
    ordner = tempfile.mkdtemp(prefix="eden_akt3_")
    rnd = random.Random(seed)
    erg = {"lage": lage, "seed": seed, "fehler": [], "abgelehnt": collections.Counter(), "events": [],
           "pflicht": collections.Counter(), "ende": None, "tag": None, "schritte": 0, "haenger": None}
    try:
        vorbereiten(ordner, seed)
        random.seed(seed)
        z = akt3_stand(lage, rnd)
        protokoll = {"schritte": [], "erledigt": {}}
        index = eden.ereignisse.daten(eden.moddir())["_index"]
        letzter, gleich = None, 0
        for n in range(MAX_SCHRITTE):
            erg["schritte"] = n
            if z["status"] == "ende" or (z.get("abschluss") and z["status"] in ("ende", "abschluss")):
                break
            if z["status"] == "ereignis" and z.get("event") and not z["event"].get("ergebnis"):
                eid = z["event"]["id"]
                if not erg["events"] or erg["events"][-1][2] != eid:
                    erg["events"].append((z["tag"], z["phase"], eid))
                    w = (index.get(eid) or {}).get("wann") or {}
                    if w.get("pflicht"):
                        erg["pflicht"][(z["tag"], z["phase"])] += 1
            try:
                a = schritt(z, protokoll, rnd)
            except Exception as e:  # noqa: BLE001
                erg["fehler"].append("Tag %s %s, Status %s: %s: %s" % (z["tag"], z["phase"], z["status"], type(e).__name__, e))
                break
            if a is None:
                break
            vor = len(protokoll["schritte"])
            try:
                if a[0] == "_tagesarbeit":
                    L.tagesarbeit(z, protokoll)
                else:
                    L.versuch(a, protokoll)
            except Exception as e:  # noqa: BLE001
                erg["fehler"].append("Tag %s %s, Aktion %s: %s: %s" % (z["tag"], z["phase"], a[0], type(e).__name__, e))
                break
            for s in protokoll["schritte"][vor:]:
                if len(s) > 2 and s[2] == "abgelehnt" and a[0] != "_tagesarbeit":
                    erg["abgelehnt"]["%s: %s" % (s[0], s[3])] += 1
            z = eden.aktiv()
            sig = (z["tag"], z["phase"], z["status"], (z.get("event") or {}).get("id"))
            gleich = gleich + 1 if sig == letzter else 0
            letzter = sig
            if gleich >= 25:
                erg["haenger"] = "Tag %s %s, Status %s, Event %s" % sig
                break
        else:
            erg["haenger"] = "mehr als %d Schritte" % MAX_SCHRITTE
        erg["tag"], erg["phase"], erg["status"] = z["tag"], z["phase"], z["status"]
        erg["ende"] = (z.get("abschluss") or {}).get("ende") or (z.get("abschluss") or {}).get("titel")
        erg["flags_a3"] = sorted(f for f in z.get("flags", []) if f.startswith("a3_"))
        return erg
    finally:
        eden.modul_laden = getattr(eden.modul_laden, "__wrapped__", eden.modul_laden)
        shutil.rmtree(ordner, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--laeufe", type=int, default=8)
    ap.add_argument("--json")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    alle, kaputt = [], 0
    lagen = list(LAGEN)
    for i in range(a.laeufe):
        lage = lagen[i % len(lagen)]
        e = lauf(lage, 100 + i)
        alle.append(e)
        ok = not e["fehler"] and not e["haenger"] and e["tag"] == 35 or e["status"] == "ende"
        kaputt += 0 if ok else 1
        print("%-24s seed %d: Tag %s %s, Status %s, Ende %s, %d Events, %d Schritte%s%s" % (
            lage, e["seed"], e["tag"], e.get("phase"), e.get("status"), e["ende"], len(e["events"]), e["schritte"],
            "  FEHLER: " + " | ".join(e["fehler"]) if e["fehler"] else "", "  HAENGT: " + e["haenger"] if e["haenger"] else ""))
        for k, n in e["abgelehnt"].most_common(3):
            print("    abgelehnt %dx: %s" % (n, k))
    gesehen = {eid for e in alle for _, _, eid in e["events"]}
    a3 = {eid for eid in eden.ereignisse.daten(os.path.join(L.BASE, "module", "eden_rise"))["_index"] if eid.startswith("a3_")}
    print("Akt-3-Events gesehen: %d von %d" % (len(gesehen & a3), len(a3)))
    dicht = collections.Counter()
    for e in alle:
        for k, n in e["pflicht"].items():
            dicht[k] = max(dicht[k], n)
    print("Dichteste Phasen (Pflicht-Szenen am Stueck):", ", ".join("Tag %d %s: %d" % (t, p, n) for (t, p), n in dicht.most_common(8)))
    if a.json:
        json.dump({"laeufe": [dict(e, abgelehnt=dict(e["abgelehnt"]), pflicht={"%d %s" % k: n for k, n in e["pflicht"].items()})
                              for e in alle], "nie_gesehen": sorted(a3 - gesehen)},
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 1 if kaputt else 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Blinde Jury zum Modellvergleich: bauen = je Szenario eine Datei ohne Modellnamen; zaehlen = Urteile zu jury_urteil.json (Buchstabe -> Zahlen) zusammenfuehren.

  python tests\\llm_vergleich_jury.py bauen
  python tests\\llm_vergleich_jury.py zaehlen
  python tests\\llm_vergleich_jury.py bauen runde2 blume,gemstrike,meromero2     weitere Runde, Blume als Kontrolle fuer die Jury
"""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUS = os.path.join(os.path.dirname(HERE), "docs", "abnahme", "llm_vergleich")
RUNDE = sys.argv[2] if len(sys.argv) > 2 else ""
JURY = os.path.join(AUS, "jury" + ("_" + RUNDE if RUNDE else ""))
MODELLE = tuple(sys.argv[3].split(",")) if len(sys.argv) > 3 else ("blume", "meromero", "pe", "magmell12")
NAME = lambda n: n + ("_" + RUNDE if RUNDE else "") + ".json"
SZENARIEN = ("anschluss", "nein", "grenzen", "erfindung")
sys.stdout.reconfigure(encoding="utf-8")


def laden(n):
    return json.load(open(os.path.join(AUS, n + ".json"), encoding="utf-8"))


def bauen():
    os.makedirs(JURY, exist_ok=True)
    r = random.Random(20261102)
    schluessel, fakten = {}, {}
    daten = {m: laden(m) for m in MODELLE}
    for sz in SZENARIEN:
        faelle = []
        for m in MODELLE:
            for k, e in daten[m]["szenen"].items():
                pid, name, seed = k.split("|")
                if name != sz:
                    continue
                if pid not in fakten and e.get("system"):
                    fakten[pid] = e["system"]
                faelle.append({"pid": pid, "seed": seed, "m": m, "erste": e["erste"], "zuege": [{"duc": z["duc"], "antwort": z["text"]} for z in e["zuege"]]})
        r.shuffle(faelle)
        for i, f in enumerate(faelle):
            f["id"] = "%s_%03d" % (sz[:2], i)
            schluessel[f["id"]] = f.pop("m")
        json.dump(faelle, open(os.path.join(JURY, sz + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        print(sz, len(faelle))
    json.dump(fakten, open(os.path.join(JURY, "figuren_prompts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(schluessel, open(os.path.join(AUS, NAME("jury_geheim")), "w", encoding="utf-8"))


def zaehlen():
    schl = json.load(open(os.path.join(AUS, NAME("jury_geheim")), encoding="utf-8"))
    summe, belege, fehlend = {m: {} for m in MODELLE}, [], 0
    for sz in SZENARIEN:
        u = json.load(open(os.path.join(JURY, sz + "_urteil.json"), encoding="utf-8"))
        faelle = json.load(open(os.path.join(JURY, sz + ".json"), encoding="utf-8"))
        for f in faelle:
            if f["id"] not in u:
                fehlend += 1
                continue
            m = schl[f["id"]]
            for t in u[f["id"]]:
                for flag in t.get("flags", []):
                    summe[m][flag] = summe[m].get(flag, 0) + 1
                    belege.append({"m": m, "fall": f["id"], "pid": f["pid"], "zug": t.get("zug"), "flag": flag, "beleg": t.get("beleg", "")})
    json.dump(summe, open(os.path.join(AUS, NAME("jury_zahlen")), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(belege, open(os.path.join(AUS, NAME("jury_belege")), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("fehlend", fehlend)
    print(json.dumps(summe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"bauen": bauen, "zaehlen": zaehlen}[sys.argv[1]]()

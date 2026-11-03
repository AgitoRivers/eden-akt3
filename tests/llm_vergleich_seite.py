# -*- coding: utf-8 -*-
"""Abnahme-Seite und Jury-Datei zum Modellvergleich (tests/llm_vergleich.py). Zaehlt, was der Code zaehlen kann; das Urteil der blinden Jury kommt aus jury_belege.json (tests/llm_vergleich_jury.py).

  python tests\\llm_vergleich_seite.py [--aus Ordner] [--empfehlung datei.html]
"""
import argparse, glob, html, json, os, re, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
sys.stdout.reconfigure(encoding="utf-8")
from kern import szene  # noqa: E402

NAMEN = {"blume": "Giftige Blume 31B", "meromero": "MeroMero 26B", "pe": "PersonalityEngine 24B", "magmell12": "Mag-Mell 12B", "magmell21": "Mag-Mell 21B",
         "dolphin": "Dolphin 24B", "gemstrike": "GemStrike 31B", "meromero2": "MeroMero v2 31B", "cydonia": "Cydonia 24B", "magnum": "Magnum Diamond 24B"}
FIG = {"rosi": "Rosi", "chiara": "Chiara", "bibi": "Bibi", "sirene": "Ligeia", "megan": "Megan", "alva": "Alva"}
SZ = {"kaltstart": "Eröffnung ohne feste Zeile", "anschluss": "Anschluss an die feste erste Zeile", "nein": "Nein halten", "grenzen": "Grenzen", "erfindung": "Erfindungen"}
TECHNIK = re.compile(r"\b(relay|inverter|wiring|wire|busbar|capacitor|fuse|panel|generator|bilge|circuit|voltage|gasket|wrench|engine|batter(?:y|ie)|solar|winch)s?\b", re.I)
JURY_ZEILEN = (("Nein aufgeweicht", ("ne", "nein_aufgeweicht"), 54), ("kommt von selbst aufs Nein zurück", ("ne", "nein_zurueck"), 36), ("weiß beim Nachhaken nicht mehr, was war", ("ne", "vergessen"), 18), ("schickt Duc weg", ("ne", "weggeschickt"), 54),
               ("Handlung ausgespielt, die nicht passiert ist", ("gr", "handlung_erfunden"), 30), ("Videoanruf gebrochen", ("gr", "anruf_bruch"), 6),
               ("Fangfrage: gemeinsames Erlebnis erfunden", ("er", "rueckbezug_erfunden"), 36), ("Fangfrage: Wort als gemeinsame Erinnerung", ("er", "wort_als_erinnerung"), 36), ("ohne Fangfrage: gemeinsames Erlebnis erfunden", ("an", "rueckbezug_erfunden"), 36),
               ("Biografie erfunden, Anschluss", ("an", "biografie_erfunden"), 36), ("Thema verloren", ("an", "thema_verloren"), 36), ("Stimme falsch, Anschluss", ("an", "stimme_falsch"), 36))


def silben(w):
    return max(1, len(re.findall(r"[aeiouy]+", re.sub(r"e$", "", w.lower()))))


def flesch(t):
    t = re.sub(r"[*\"“”]", "", t)
    saetze = max(1, len(re.findall(r"[.!?]+(\s|$)", t)))
    w = re.findall(r"[A-Za-z']+", t)
    if not w:
        return None
    return 206.835 - 1.015 * len(w) / saetze - 84.6 * sum(silben(x) for x in w) / len(w)


def zuege(d):
    for k, e in d["szenen"].items():
        pid, sz, seed = k.split("|")
        for i, z in enumerate(e["zuege"]):
            yield pid, sz, seed, i, z


def erkennung_zahlen(liste):
    if not liste:
        return {}
    tp = sum(1 for e in liste if e["soll"] and e["ist"] is True)
    fn = [e["text"] for e in liste if e["soll"] and e["ist"] is not True]
    fp = [e["text"] for e in liste if not e["soll"] and e["ist"] is True]
    return {"treffer": tp, "echt": sum(1 for e in liste if e["soll"]), "falsch": len(fp), "unecht": sum(1 for e in liste if not e["soll"]), "fn": fn, "fp": fp, "lesbar": sum(1 for e in liste if e["lesbar"]), "n": len(liste)}


def zaehlen(d):
    w, spaet, floskel, flz, cari, tech, tech_alle, neu, abg, sek, tps = [], 0, 0, [], 0, 0, 0, 0, 0, [], []
    n = 0
    richter = {}
    for pid, sz, seed, i, z in zuege(d):
        t = z["text"] or ""
        n += 1
        w.append(len(re.findall(r"\S+", t)))
        spaet += bool(szene.ZU_SPAET_RE.search(t))
        floskel += bool(szene.FLOSKEL_RE.search(t))
        cari += bool(pid == "alva" and re.search(r"cari[nñ]o", t, re.I))
        tech += bool(pid == "rosi" and sz == "kaltstart" and TECHNIK.search(t))
        tech_alle += bool(pid == "rosi" and sz != "anschluss" and TECHNIK.search(t))
        neu += bool(z["verworfen"])
        for v in z["verworfen"]:
            for k in v:
                richter[k] = richter.get(k, 0) + 1
        fig = [x for x in z["laeufe"] if x["rolle"] == "figur"]
        abg += bool(z["abgeschnitten"] or (fig and fig[-1]["grund"] == "length"))
        f = flesch(t)
        if f is not None:
            flz.append(f)
        if z["laeufe"]:
            sek.append(sum(x["sek"] for x in z["laeufe"]))
        for x in fig:
            if x.get("aus") and x["sek"]:
                tps.append(x["aus"] / x["sek"])
    return {"n": n, "woerter": round(st.mean(w)) if w else 0, "ueber80": sum(1 for x in w if x > 80), "unter30": sum(1 for x in w if x < 30), "spaet": spaet, "floskel": floskel, "cari": cari, "tech": tech, "tech_alle": tech_alle, "neu": neu,
            "abg": abg, "flesch": round(st.mean(flz)) if flz else 0, "sek": round(st.mean(sek), 1) if sek else 0, "sek_max": round(max(sek), 1) if sek else 0, "tps": round(st.median(tps), 1) if tps else 0, "richter": richter}


CSS = """:root{--bg:#f6f5f1;--karte:#fff;--text:#22221f;--leise:#6b6a63;--linie:#dddbd2;--gut:#1c7c54;--schlecht:#b3362b;--akzent:#3a5a8c}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17181a;--karte:#212326;--text:#e8e7e2;--leise:#9b9a93;--linie:#35373b;--gut:#5ec79a;--schlecht:#ef8378;--akzent:#8fb0e6}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,Segoe UI,sans-serif}main{max-width:1500px;margin:auto;padding:24px 16px 80px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:32px 0 10px}h3{font-size:15px;margin:22px 0 8px}p{max-width:75ch}.leise{color:var(--leise)}
.tab{overflow-x:auto;background:var(--karte);border:1px solid var(--linie);border-radius:8px}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{padding:7px 12px;border-bottom:1px solid var(--linie);text-align:left;white-space:nowrap}td.z{text-align:right}th.m{text-align:right}tr:last-child td{border-bottom:0}
.emp{background:var(--karte);border:1px solid var(--linie);border-left:4px solid var(--akzent);border-radius:8px;padding:12px 16px;max-width:90ch}
details{background:var(--karte);border:1px solid var(--linie);border-radius:8px;margin:8px 0}summary{cursor:pointer;padding:9px 14px;font-weight:600}
.reihe{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px;padding:0 12px 12px}.antwort{border:1px solid var(--linie);border-radius:6px;padding:9px 11px;font-size:14px;white-space:pre-wrap}.antwort b{display:block;font-size:12px;color:var(--akzent);margin-bottom:3px}.duc{padding:6px 14px;color:var(--leise);font-style:italic}.erste{padding:4px 14px;font-size:14px}"""


def seite(daten, aus, empfehlung, jury):
    m = [n for n in NAMEN if n in daten]
    z = {n: zaehlen(daten[n]) for n in m}
    e = {n: erkennung_zahlen(daten[n].get("erkennung")) for n in m}
    f = {n: erkennung_zahlen(daten[n].get("erkennung_frei")) for n in m}
    zeile = lambda titel, fn: "<tr><td>%s</td>%s</tr>" % (titel, "".join('<td class=z>%s</td>' % fn(n) for n in m))
    t = ["<tr><th></th>%s</tr>" % "".join("<th class=m>%s</th>" % NAMEN[n] for n in m)]
    t.append(zeile("Antworten", lambda n: z[n]["n"]))
    t.append(zeile("Erkennung: echte Handlung erkannt", lambda n: "%d von %d" % (e[n].get("treffer", 0), e[n].get("echt", 0))))
    t.append(zeile("Erkennung: falsche Treffer", lambda n: "%d von %d" % (e[n].get("falsch", 0), e[n].get("unecht", 0))))
    t.append(zeile("Erkennung ohne Grammatik: lesbar", lambda n: "%d von %d" % (f[n].get("lesbar", 0), f[n].get("n", 0))))
    for titel, schluessel, von in JURY_ZEILEN:
        t.append(zeile("%s (von %d)" % (titel, von), lambda n, s=schluessel: jury.get((n,) + s, 0)))
    t.append(zeile("„You're late“ (18 Eröffnungen, 180 Antworten)", lambda n: z[n]["spaet"]))
    t.append(zeile("Rosi eröffnet mit Technik (von 3)", lambda n: z[n]["tech"]))
    t.append(zeile("Rosi nennt Technik, ohne Anschluss-Szenen (von 24)", lambda n: z[n]["tech_alle"]))
    t.append(zeile("Alva sagt „cariño“ (von 30)", lambda n: z[n]["cari"]))
    t.append(zeile("Verbotene Floskel", lambda n: z[n]["floskel"]))
    t.append(zeile("Vom Richter neu geschrieben", lambda n: z[n]["neu"]))
    t.append(zeile("Wörter im Schnitt (Soll 50–80)", lambda n: z[n]["woerter"]))
    t.append(zeile("über 80 Wörter", lambda n: z[n]["ueber80"]))
    t.append(zeile("abgeschnitten", lambda n: z[n]["abg"]))
    t.append(zeile("Lesbarkeit (Flesch, höher = einfacher)", lambda n: z[n]["flesch"]))
    t.append(zeile("Wartezeit je Zug mit Richter, Schnitt (s)", lambda n: z[n]["sek"]))
    t.append(zeile("Wartezeit je Zug, längste (s)", lambda n: z[n]["sek_max"]))
    t.append(zeile("Tokens/s (Median, mit Prompt)", lambda n: z[n]["tps"]))
    t.append(zeile("VRAM nur Modell, Spitze (GB)", lambda n: "%.1f" % ((daten[n].get("vram_spitze", 0) - daten[n].get("vram_vorher", 0)) / 1024)))
    t.append(zeile("Laden (s)", lambda n: daten[n].get("laden_sek", "–")))
    t.append(zeile("Fester Seed wiederholbar", lambda n: "ja" if daten[n].get("seed_stabil") else "nein"))
    t.append(zeile("Lauf vollständig", lambda n: "ja" if daten[n].get("fertig") else "nein"))
    teile = ["<!doctype html><html lang=de><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>LLM-Vergleich</title><style>%s</style></head><body><main>" % CSS,
             "<h1>LLM-Vergleich für die freien Szenen</h1><p class=leise>Gleiche Prompts aus dem Spielcode, gleiche Sampler und Seeds, 6 Figuren, 3 Durchgänge je Fall.</p>"]
    if empfehlung:
        teile.append("<div class=emp>%s</div>" % empfehlung)
    teile.append("<h2>Zähltabelle</h2><div class=tab><table>%s</table></div>" % "".join(t))
    teile.append("<h2>Erkennung: wo sie danebenlag</h2>")
    for n in m:
        teile.append("<h3>%s</h3><p>Übersehen: %s<br>Falsch ausgelöst: %s</p>" % (NAMEN[n], html.escape(" · ".join(e[n].get("fn", [])) or "nichts"), html.escape(" · ".join(e[n].get("fp", [])) or "nichts")))
    teile.append("<h2>Antworten nebeneinander</h2>")
    faelle = sorted({k for n in m for k in daten[n]["szenen"]}, key=lambda k: (list(FIG).index(k.split("|")[0]), list(SZ).index(k.split("|")[1]), k))
    for k in faelle:
        pid, sz, seed = k.split("|")
        erste = next((daten[n]["szenen"][k].get("erste") for n in m if k in daten[n]["szenen"]), None)
        teile.append("<details><summary>%s · %s · Durchgang %s</summary>" % (FIG[pid], SZ[sz], seed))
        if erste:
            teile.append("<div class=erste><span class=leise>Feste erste Zeile:</span> %s</div>" % html.escape(erste))
        for i in range(max(len(daten[n]["szenen"].get(k, {"zuege": []})["zuege"]) for n in m)):
            duc = next((daten[n]["szenen"][k]["zuege"][i]["duc"] for n in m if k in daten[n]["szenen"] and i < len(daten[n]["szenen"][k]["zuege"])), None)
            if duc:
                teile.append("<div class=duc>Duc: %s</div>" % html.escape(duc))
            teile.append("<div class=reihe>")
            for n in m:
                zs = daten[n]["szenen"].get(k, {"zuege": []})["zuege"]
                teile.append("<div class=antwort><b>%s</b>%s</div>" % (NAMEN[n], html.escape(zs[i]["text"]) if i < len(zs) else "–"))
            teile.append("</div>")
        teile.append("</details>")
    teile.append("</main></body></html>")
    pfad = os.path.join(aus, "index.html")
    open(pfad, "w", encoding="utf-8").write("".join(teile))
    return pfad, z, e, f


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--aus", default=os.path.join(EDEN, "docs", "abnahme", "llm_vergleich"))
    a.add_argument("--empfehlung")
    o = a.parse_args()
    daten = {}
    for p in glob.glob(os.path.join(o.aus, "*.json")):
        n = os.path.basename(p)[:-5]
        if n in NAMEN:
            daten[n] = json.load(open(p, encoding="utf-8"))
    jury, gezaehlt = {}, set()
    for p in sorted(glob.glob(os.path.join(o.aus, "jury_belege*.json"))):     # erste Runde zuerst; ein Modell zaehlt nur aus seiner ersten Runde
        neu = set()
        for x in json.load(open(p, encoding="utf-8")):
            if x["m"] in gezaehlt:
                continue
            neu.add(x["m"])
            k = (x["m"], x["fall"][:2], x["flag"])
            jury[k] = jury.get(k, 0) + 1
        gezaehlt |= neu
    emp = open(o.empfehlung, encoding="utf-8").read() if o.empfehlung else ""
    pfad, z, e, f = seite(daten, o.aus, emp, jury)
    print(pfad)
    print(json.dumps({n: {"z": z[n], "e": {k: v for k, v in e[n].items()}, "f": {k: f[n].get(k) for k in ("treffer", "falsch", "lesbar", "n")}} for n in z}, ensure_ascii=False, indent=0))


if __name__ == "__main__":
    main()

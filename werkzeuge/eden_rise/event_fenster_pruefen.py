# -*- coding: utf-8 -*-
r"""Pruefliste Event-Fenster (Duc 29.10.2026): Fast alle Events enden an Tag 6 (WANN((2, 6), ...) aus Akt-1-Zeiten), ab Tag 7
gibt es keinen Kandidaten mehr - Akt 2 hat keine Selfies, Abende, Funken, Flirts, Bordraete. Dieses Skript sortiert alle
Events mit Fenster bis Tag 6 (ohne Ortsketten und Rastplaetze) in drei Toepfe, damit Story sie auf Tag 2-21 oeffnen kann:

  bleibt_akt1  Pflicht/Prolog oder Strom/Diesel in den Folgen (Mechanik seit E-082 weg)
  anpassen     Text enthaelt Akt-1-Bezuege (Anhoerung, Ultimatum, Feuer frisch, erste Tage, Strom ...) - Wortliste je Event
  zeitlos      kein Treffer: kann nach kurzem Lesen auf (2, 21) bzw. (a, 21)

  python werkzeuge\eden_rise\event_fenster_pruefen.py      schreibt docs\brain_trust\event_fenster_pruefliste.md + .json

Nur lesen: aendert keine Events. Die Woerter sind Heuristik - "zeitlos" heisst "kein Treffer", nicht "geprueft"."""
import collections, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
QUELLE = os.path.join(EDEN, "module", "eden_rise", "ereignisse.json")
ZIEL = os.path.join(EDEN, "docs", "brain_trust", "event_fenster_pruefliste")

# Akt-1-Bezuege (englischer Spieltext); Schluessel = Thema in der Liste
BEZUEGE = {
    "Anhörung": r"\bhearing\b|\binquiry\b|tribunal|\bthe judge\b|\btestif",
    "Ultimatum/Frist": r"ultimatum|\bone week\b|\ba week\b|seven days|\bday seven\b|deadline|\bby sunday\b",
    "Feuer/Blackout frisch": r"\bthe fire\b|\bfire last\b|since the fire|blackout|\bburnt?\b|\bburned\b|\bsmoke\b",
    "erste Tage": r"since we got here|\bfirst (?:night|day|week|morning)\b|just arrived|we've only been here|\bnew here\b|"
                  r"\barrived\b|\byesterday we\b|day one",
    "Strom/Diesel": r"\bpower\b|batter(?:y|ies)|generator|\bdiesel\b|\bfuel\b|\bsolar\b|\bcharge\b|\bwatts?\b",
    "festgesetzt": r"stranded|stuck here|can'?t leave|impound|detained|anchor ban|not allowed to leave",
    "Inspektion": r"inspection|comes tomorrow|ferrandi.{0,20}tomorrow",
    "Megans Nachrichten": r"voicemail|voice message|megan'?s message",
}
MUSTER = {k: re.compile(v, re.I) for k, v in BEZUEGE.items()}


def texte(ev):
    """Alles, was der Spieler liest oder hoert."""
    out = [ev.get("titel", ""), ev.get("lage", ""), ev.get("nachklang_text", "") or ""]
    out += [z.get("text", "") for z in ev.get("zeilen") or []]
    for o in ev.get("optionen") or []:
        out.append(o.get("text", ""))
        if isinstance(o.get("zeile"), dict):
            out.append(o["zeile"].get("text", ""))
        for f in o.get("folgen") or []:
            if isinstance(f, dict) and isinstance(f.get("codex"), str):
                out.append(f["codex"])
    return [t for t in out if t]


def strom_folgen(ev):
    for o in ev.get("optionen") or []:
        for f in o.get("folgen") or []:
            if isinstance(f, dict) and f.get("wert") in ("strom", "diesel"):
                return True
    return False


def gruppe(ev):
    p = ev.get("personen") or {}
    if (p.get("selfie") or {}).get("stufe"):
        return "Selfie"
    if p.get("charm"):
        return "Charm"
    if ev["id"].startswith("fl_"):
        return "Flirt"
    return {"abend": "Abend/Funke", "bordrat": "Bordrat", "handy": "Handy", "gag1": "Gag", "gagv": "Gag (versus)",
            "duell": "Duell", "auftritt": "Auftritt"}.get(ev["art"], ev["art"])


def wer(ev):
    p = ev.get("personen") or {}
    ids = [p.get(k) for k in ("sprecher", "handelnd", "pid", "anrufer", "links", "rechts", "gegner") if isinstance(p.get(k), str)]
    return ", ".join(dict.fromkeys(i for i in ids if i))


def pruefen():
    ev = json.load(open(QUELLE, encoding="utf-8"))["events"]
    ids = {e["id"] for e in ev}
    zeilen = []
    for e in ev:
        if e["art"] == "ort" or e.get("rast") or e["wann"]["tage"][1] > 6:
            continue
        if e["id"] + "_2" in ids:                       # Charm-Uebergaben: Akt-2-Zwilling existiert schon (ereignisse_charms.py)
            continue
        w = e["wann"]
        treffer = {}
        for t in texte(e):
            for thema, m in MUSTER.items():
                for x in m.findall(t):
                    treffer.setdefault(thema, set()).add(x.lower() if isinstance(x, str) else x)
        if w.get("pflicht") or w.get("prolog"):
            topf, grund = "bleibt_akt1", "Pflicht/Prolog"
        elif strom_folgen(e):
            topf, grund = "bleibt_akt1", "Strom/Diesel in den Folgen"
        elif treffer:
            topf, grund = "anpassen", "; ".join("%s (%s)" % (k, ", ".join(sorted(v))) for k, v in treffer.items())
        else:
            topf, grund = "zeitlos", ""
        zeilen.append({"id": e["id"], "gruppe": gruppe(e), "art": e["art"], "tage": w["tage"], "titel": e.get("titel", ""),
                       "wer": wer(e), "bedingung": bool(w.get("bedingung")), "topf": topf, "grund": grund})
    return zeilen


def schreiben(zeilen):
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    json.dump(zeilen, open(ZIEL + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    zahl = collections.Counter(z["topf"] for z in zeilen)
    je = collections.defaultdict(collections.Counter)
    for z in zeilen:
        je[z["gruppe"]][z["topf"]] += 1
    md = ["# Pruefliste Event-Fenster (Akt 1 -> Akt 2)", "",
          "> Erzeugt von `werkzeuge/eden_rise/event_fenster_pruefen.py` (29.10.2026). Nur Vorschlag: aendert keine Events.",
          "> Hintergrund: Fast alle Events enden an Tag 6. Ab Tag 7 findet die Engine keinen Kandidaten mehr, Akt 2 bleibt",
          "> ohne Selfies, Abende, Funken, Flirts und Bordraete (Bot-Messung Seed 7, Diagnose im Chat 29.10.).", "",
          "**Toepfe:** `zeitlos` = kein Akt-1-Wort gefunden -> kurz lesen, dann Fenster auf Tag 21 (`WANN((a, 21), ...)`). "
          "`anpassen` = Akt-1-Bezug im Text -> Zeile umschreiben oder bei Tag 6 lassen. `bleibt_akt1` = Pflicht/Prolog oder "
          "Strom/Diesel (Mechanik weg, E-082). Die Woerter sind eine Heuristik: \"zeitlos\" heisst \"kein Treffer\", nicht "
          "\"geprueft\". Bedingung = das Event haengt zusaetzlich an Vertrauen/Flags.", "",
          "| Topf | Anzahl |", "|---|---|"] + ["| %s | %d |" % (k, zahl[k]) for k in ("zeitlos", "anpassen", "bleibt_akt1")] + [
          "", "| Gruppe | zeitlos | anpassen | bleibt_akt1 |", "|---|---|---|---|"] + [
          "| %s | %d | %d | %d |" % (g, c["zeitlos"], c["anpassen"], c["bleibt_akt1"]) for g, c in sorted(je.items(), key=lambda x: -sum(x[1].values()))]
    for topf, titel in (("anpassen", "Anpassen (Akt-1-Bezug im Text)"), ("zeitlos", "Zeitlos (kein Treffer)"),
                        ("bleibt_akt1", "Bleibt in Akt 1")):
        md += ["", "## %s" % titel, "", "| ID | Gruppe | Fenster | Wer | Bed. | Titel | Treffer |", "|---|---|---|---|---|---|---|"]
        for z in sorted((z for z in zeilen if z["topf"] == topf), key=lambda z: (z["gruppe"], z["id"])):
            md.append("| `%s` | %s | %d–%d | %s | %s | %s | %s |" % (z["id"], z["gruppe"], z["tage"][0], z["tage"][1], z["wer"],
                                                           "ja" if z["bedingung"] else "", z["titel"].replace("|", "/"),
                                                           z["grund"].replace("|", "/")))
    open(ZIEL + ".md", "w", encoding="utf-8").write("\n".join(md) + "\n")
    return zahl, je


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    zahl, je = schreiben(pruefen())
    print("geschrieben: %s.md/.json | %s" % (ZIEL, dict(zahl)))
    for g, c in sorted(je.items(), key=lambda x: -sum(x[1].values())):
        print("  %-14s %s" % (g, dict(c)))

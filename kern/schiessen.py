# -*- coding: utf-8 -*-
"""Holms Wette um Gemelli (Duc 30.10.2026): Der CODE haelt die Regeln und bucht die Preise; das Minispiel laeuft im Client
(client/plugins/eden-schiessen) und meldet je Runde die Treffer beider Seiten. Wiki docs/wiki/systeme/schiesswette.md.

  * Drei Gegner nacheinander: Adrien (nur auf Weg C, sonst Rosi), Elsa, Wolff. Wer Wolff schlaegt, traegt Gemelli
    (Flags waffe_gun, holm_wette_gewonnen; beim Beenden oeffnet eden.py die Uebergabe hb_sieg).
  * Ab Tag HOLM_TAG ist Holm die vierte Gegnerin. Jede gewonnene Runde gibt einmalig ein Geschenk, auch bei verlorenem Spiel.
  * Drei Runden, die Summe entscheidet, Gleichstand ist kein Sieg. Der Bot trifft je Runde eine feste Zahl; die Blendgranate
    kann ihn drosseln, darum meldet der Client seine Treffer mit, die Engine deckelt sie auf den Plan.
  * Kostet weder Zeit noch Aktion. Eine Niederlage kostet nichts: Die Waffe darf bei der Belagerung nicht fehlen. Nach
    je LEICHTER_AB Niederlagen trifft der Bot still je Runde einen weniger, hoechstens LEICHTER_MAX (nicht Holm).
  * Spielstaende ohne Wette bekommen keinen neuen Schluessel."""

RUNDEN = 3
PAUSE_S = 5
BLEND_S = 5
RELAXED_PLUS_S = 2          # Relaxed: kein Wind und je Runde 2 Sekunden mehr, nicht gegen Holm
ZIELE_JE_RUNDE = 13
TREFFER_MAX = 20
LEICHTER_AB = 3
LEICHTER_MAX = 4
HOLM_TAG = 24              # Revanche erst in Akt 3, nach der Belagerung (E-114, Duc 04.11.2026)
ZONE_JE_WAHRNEHMUNG = 0.04  # Trefferzone +4 % je Punkt Wahrnehmung
BILD = "yacht_foredeck_sunrise.png"
SIEG_EVENT, NOCHMAL_ZEILE = "hb_sieg", "hb_nochmal#z0"
# bot = Treffer je Runde, dauer = Sekunden je Runde; Stufe 3 und Holm verlangen die Duc-Zahlen 8/9/10.
# wind und granate (Runden 0-2) fuehren die Regeln nacheinander ein: der erste Gegner lehrt nur Zielen und Nachladen.
GEGNER = {"adrien": {"pid": "adrien", "bot": (5, 6, 7), "dauer": 10.0, "wind": False, "granate": ()},
          "rosi": {"pid": "rosi", "bot": (5, 6, 7), "dauer": 10.0, "wind": False, "granate": ()},
          "elsa": {"pid": "elsa", "bot": (6, 7, 8), "dauer": 10.0, "wind": True, "granate": (1, 2)},
          "wolff": {"pid": "wolff", "bot": (8, 9, 10), "dauer": 10.0, "wind": True, "granate": (1, 2)},
          "holm": {"pid": "holm", "bot": (8, 9, 10), "dauer": 9.5, "wind": True, "granate": (1, 2)}}
AVATAR_GEFUEHLE = {"neutral": "neutral", "vorn": "joy", "hinten": "annoyance", "blind": "surprise"}
GESCHENKE = ("steel_plate", "aquamarin", "kupfer")      # Runde 1, 2, 3 gegen Holm


def _flags(z):
    return z.get("flags") or []


def gegner(z):
    """Wer gerade dran ist, oder None."""
    f = _flags(z)
    if "holm_wette_offen" not in f:
        return None
    if "holm_wette_gewonnen" in f:
        offen_holm = z.get("tag", 0) >= HOLM_TAG and not all("hw_geschenk_%d" % i in f for i in range(1, 4))
        return "holm" if offen_holm else None
    if "hw_sieg_elsa" in f:
        return "wolff"
    if "hw_sieg_erster" in f:
        return "elsa"
    return "adrien" if "bg_adrien_bergerie" in f else "rosi"


def offen(z):
    return gegner(z) is not None


def _sitzung(z):
    s = z.get("schiessen")
    if not s or z.get("status") != "schiessen":
        raise ValueError("There's no bet running.")
    return s


def starten(z):
    """-> Event-Id, wenn erst die Szene mit dem neuen Gegner laeuft (danach startet der Client erneut), sonst None."""
    g = gegner(z)
    if not g:
        raise ValueError("Holm hasn't offered you a bet.")
    if z.get("status") != "wahl":
        raise ValueError("You can only meet Holm on the foredeck in your free time.")
    if "hw_intro_" + g not in _flags(z):
        z["schiessen_folgt"] = True
        return "hb_g_" + g
    z.pop("schiessen_folgt", None)
    z["schiessen"] = {"gegner": g, "versuche": 0, "letztes": None}
    z["status"] = "schiessen"
    return None


def bot_plan(z, g):
    """Treffer des Bots je Runde; nach mehreren Niederlagen still leichter (Holm nie)."""
    plan = GEGNER[g]["bot"]
    if g == "holm":
        return list(plan)
    minus = min(LEICHTER_MAX, (z.get("schiessen_verloren") or {}).get(g, 0) // LEICHTER_AB)
    return [b - minus for b in plan]


def ergebnis(z, runden, leicht, modul):
    """Alle drei Runden sind vorbei. Mehrere Spiele je Sitzung gehen ("Again"). -> das gespeicherte Ergebnis."""
    s = _sitzung(z)
    g = s["gegner"]
    plan = bot_plan(z, g)
    if not isinstance(runden, list) or len(runden) != RUNDEN:
        raise ValueError("A bet has three rounds.")
    zeilen = [{"du": max(0, min(int(r.get("du") or 0), TREFFER_MAX)), "bot": max(0, min(int(r.get("bot") or 0), plan[i]))}
              for i, r in enumerate(runden)]
    du, bot = sum(r["du"] for r in zeilen), sum(r["bot"] for r in zeilen)
    sieg = du > bot
    s["versuche"] += 1
    geschenke = []
    if g == "holm":
        for i, r in enumerate(zeilen, 1):
            if r["du"] > r["bot"] and "hw_geschenk_%d" % i not in z["flags"]:
                z["flags"].append("hw_geschenk_%d" % i)
                z["inventar"].append(GESCHENKE[i - 1])
                geschenke.append({"runde": i, "name": modul["items"][GESCHENKE[i - 1]]["label"],
                                  "zeile": "hb_w_holm#z%d" % (i + 1)})
    elif sieg:
        for f in {"adrien": ["hw_sieg_erster"], "rosi": ["hw_sieg_erster"], "elsa": ["hw_sieg_elsa"],
                  "wolff": ["waffe_gun", "holm_wette_gewonnen"]}[g]:
            if f not in z["flags"]:
                z["flags"].append(f)
    else:
        v = z.setdefault("schiessen_verloren", {})
        v[g] = v.get(g, 0) + 1
    s["letztes"] = {"runden": zeilen, "du": du, "bot": bot, "sieg": sieg, "leicht": bool(leicht), "geschenke": geschenke}
    return s["letztes"]


def ende(z):
    """Zurueck an Deck. -> Event-Id, wenn jetzt die Uebergabe der Waffe dran ist."""
    s = _sitzung(z)
    z.pop("schiessen", None)
    z["status"] = "wahl"
    gewonnen = bool((s.get("letztes") or {}).get("sieg"))
    return SIEG_EVENT if gewonnen and s["gegner"] == "wolff" else None


def ansicht(z):
    s = z.get("schiessen")
    if not s:
        return None
    g = s["gegner"]
    wahrnehmung = ((z.get("persona") or {}).get("attribute") or {}).get("perception", 2)
    letztes = s["letztes"]
    return {"gegner": {"id": g, "pid": GEGNER[g]["pid"]}, "runden": RUNDEN, "bot": bot_plan(z, g), "dauer": GEGNER[g]["dauer"],
            "wind": GEGNER[g]["wind"], "granate": list(GEGNER[g]["granate"]), "pause_s": PAUSE_S, "blend_s": BLEND_S, "ziele": ZIELE_JE_RUNDE, "relaxed_plus_s": RELAXED_PLUS_S,
            "relaxed_erlaubt": g != "holm", "treffer_max": TREFFER_MAX, "bild": "/bg/" + BILD,
            "trefferzone": round(1 + wahrnehmung * ZONE_JE_WAHRNEHMUNG, 2), "versuche": s["versuche"], "letztes": letztes,
            "worte": "hb_w_" + g, "weiter": bool(letztes and letztes["sieg"] and g != "holm" and g != "wolff"),
            "zeile_nochmal": NOCHMAL_ZEILE}

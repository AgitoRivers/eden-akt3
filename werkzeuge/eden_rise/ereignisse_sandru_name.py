# -*- coding: utf-8 -*-
"""Sandrus Herkunft, Szene 1: "Your Own Name" (Duc 30.10.2026, E-097; gebaut 04.11.2026 in der Cloud-Sitzung, F-20).
Kanon: docs/wiki/welt/dorf_figuren.md, Abschnitt "Sandrus Herkunft". Woche 3, Laden nach Feierabend, ernst und leise.
Duc erzaehlt seine eigene Fluchtgeschichte (E-067). Setzt sandru_herkunft: Akt 3 liest das (Schiene, ISKANDER, Kommission).
Kommt im Pool, Tag 15 bis 20, und als Nachzuegler in Akt 3 bis Tag 31 (vor Switched Off). Die zweite Szene "Not in the
System" ist in Akt 3 das Los der Festa-Tafel (ereignisse_akt3_lose.py)."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import tags_fuer  # noqa: E402

_w = WANN((15, 20), ["abend"], bed={"alle": [{"flag": "a2_sandru"}, {"nicht": {"flag": "sandru_herkunft"}}]})
_w["akt2"] = [24, 31]

EVENTS = [
    E("a2_sandru_name", "gag1", "ernst", "Your Own Name", _w, "av_market", P1("sandru", ("alva", "?", "has the light on across the street")),
      "The A.V. Market after closing time. The white lights hum. Sandru counts the money in the till. His name badge lies next to it, "
      "face down. Across the street, the light in Alva's bar is still on.",
      [G("sandru", "[chuckle] We're closed, Duc. Ha. For you, half closed.", "neutral"),
       G("sandru", "[sigh] The badge? Alex. A.V. gave me that name. My father picked tomatoes in the east plain for thirty years, "
                   "so that nobody would ever ask his son where he comes from. And then somebody asks anyway. Every week.", "sadness"),
       G("sandru", "[clear throat] Alex doesn't come from anywhere. That's what I like about him. ...So. Where do you come from, Duc?", "nervousness")],
      [O("“My parents fled from Vietnam. Night shifts in Germany. For years I acted like I came from nowhere. "
         "You can't run from it. You're carrying it anyway. So carry it with your head up.”",
         [F("sandru_herkunft"), V("sandru", 6)],
         zeile=G("sandru", "[sigh] ...Iskander. My mother is the only one who still says it.", "sadness")),
       O("Picks up the badge and turns it over. “My parents fled from Vietnam. You can't run from it. So carry it with your head up.”",
         [F("sandru_herkunft"), V("sandru", 4)],
         zeile=G("sandru", "[sigh] Head up. ...Iskander. That's my name. My mother is the only one who still says it.", "sadness")),
       O("“From Frankfurt. Mostly.”", [V("sandru", 2)],
         zeile=G("sandru", "[laugh] Mostly. Ha. Me too. Mostly from here.", "neutral"))],
      sets={"sandru": "sandru_av"}),
]


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_sandru")

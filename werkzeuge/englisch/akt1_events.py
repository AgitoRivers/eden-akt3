# -*- coding: utf-8 -*-
r"""English rewrite · package 2: all remaining Act 1 events (25.10.2026). Combines the per-file modules.

    python werkzeuge\englisch\abnahme_bauen.py akt1_events
"""
import importlib, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "eden_rise"))

TEILE = ["akt1_bordrat", "akt1_handy", "akt1_gag1", "akt1_gagv", "akt1_staerken_abende", "akt1_rest"]
DATEIEN = ["ereignisse_bordrat", "ereignisse_handy", "ereignisse_gag1", "ereignisse_gagv", "ereignisse_staerken",
           "ereignisse_abende", "ereignisse_akt1", "ereignisse_yamamoto", "ereignisse_verrueckt"]

NEU, SPRECHER = {}, {}
for _t in TEILE:
    _m = importlib.import_module(_t)
    NEU.update(_m.NEU)
    SPRECHER.update(getattr(_m, "SPRECHER", {}))

PREFIXE = set()
for _d in DATEIEN:
    PREFIXE.update(e["id"] for e in importlib.import_module(_d).EVENTS)
PREFIXE.discard("mx_tutorial")                       # already in the pilot

TITEL = "Englisch · Paket 2: alle übrigen Akt-1-Events"
HINWEIS = ("Links alt, rechts neu. 🔊 = wird neu vertont. Pro Text OK oder Ändern (mit Notiz), „Restliche OK“ für alles "
           "Übrige. Umgesetzt sind dabei die Wiki-Beschlüsse: Rosi sagt „Officer“, Lola „Boss“/„mate“ statt "
           "„babe“/„Captain“, Maxwell „Mr. Maximum“, Siri ist Norwegerin, Megans Büro ist in Monaco, Sophias Schreiben "
           "bleibt geheim (in „A Page from Sophia's Notebook“ liest jetzt Lola eine geklaute Seite vor), Casanova sagt "
           "nicht Alvas „o figliolu“.")
ENCOUNTERS, GEGNER, TUTORIAL = [], [], False

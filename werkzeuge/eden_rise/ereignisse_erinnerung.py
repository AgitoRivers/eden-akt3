# -*- coding: utf-8 -*-
"""Erinnerungen der Auftraggeberinnen (Duc 02.11.2026, Spieltest-Befund 5, Vorbild Persona 5 / Mass Effect).

Ein offener Auftrag bleibt sonst still liegen. Morgens schickt die Auftraggeberin eine Sprachnachricht, wenn
  - Duc seit 3 Tagen nicht am Ort des Auftrags war (Bedingung ort_ruhe, kern/regeln.py), oder
  - der Auftrag eine Frist hat und sie in ein bis zwei Tagen endet (Kevin bis Tag 14, Flut-Nacht bis Tag 21).
Jede Nachricht kommt einmal im Durchlauf, hoechstens eine Erinnerung am Tag (wann.erinnerung, kern/ereignisse.py).
Der Satz sagt immer, worum es ging, denn der Spieler vergisst. Ohne Wirkung auf Werte: die Erinnerung ist ein Hinweis,
kein Lohn. Red Trio, Old Grey und Mazzera erinnern nicht (Gegner bzw. Umwege ohne Telefon)."""
import json, os, sys
from ereignisse_basis import *  # noqa: F401,F403
sys.path.insert(0, EDEN)
from kern import stimme  # noqa: E402

H = lambda anrufer, ort: {"anrufer": anrufer, "anrufer_ort": ort, "art": "video"}
RUHE = 3                                     # Tage ohne Besuch, bis die Auftraggeberin sich meldet
_TAGS = []


def S_(wer, gesprochen, gefuehl="neutral"):
    """Zeile mit Turbo-Tag: im Text ohne Tag, in stimme_tags.json mit."""
    klar = stimme.vorlesen(stimme.ohne_tags(gesprochen))
    _TAGS.append((wer, klar, gesprochen))
    return Z(wer, klar, gefuehl)


def ER(id, titel, tage, bed, anrufer, ort, lage, zeilen, optionen):
    w = WANN(tage, ["fruehstueck"], bed=bed, pflicht=True)
    w["erinnerung"] = True
    return E(id, "handy", "wholesome", titel, w, ORT_DUC, H(anrufer, ort), lage, zeilen, optionen)


def OFFEN(an, fertig, ort=None):
    return {"alle": [{"flag": an}, {"nicht": {"flag": fertig}}] + ([{"ort_ruhe": [ort, RUHE]}] if ort else [])}


EVENTS = [
    ER("er_kloster", "Voice Message from Madame Casanova", (9, 20), OFFEN("kloster_angenommen", "kloster_fertig", "macchia"),
       "casanova", "village_piazza", "A voice message from Madame Casanova, 07:10. Church bells and a lot of pigeons.",
       [S_("casanova", "Monsieur, it is Madame Casanova. [sigh] Still no word from San Martinu. No herbs, no cheese, no brothers.",
           "nervousness"),
        S_("casanova", "You said you would climb the macchia and look for them. The path is still there, Monsieur. [gasp] "
                       "And the brothers too, I hope.", "caring")],
       [O("Texts back: “Going up soon.”", []),
        O("Plays it again. Then checks his bat.", [])]),

    ER("er_berge", "Voice Message from Petru", (10, 20), OFFEN("berge_angenommen", "berge_fertig", "berge"),
       "petru", "petru_workshop", "A voice message from Petru. Eleven seconds long. The radio in his boathouse is off.",
       [S_("petru", "[clear throat] Hm. Petru. Laetitia is still up in the mountains. Nobody has seen her come down.", "sadness"),
        S_("petru", "The path to the Genoese tower is long. [sigh] Go up when you can. I am waiting.", "neutral")],
       [O("Texts back: “I haven't forgotten her.”", []),
        O("Listens to the silence at the end of it.", [])]),

    ER("er_grotte", "Voice Message from Totò", (12, 20), OFFEN("grotte_offen", "grotte_fertig", "grotte"),
       "toto", "village_harbour", "A voice message from Totò. He is whispering, and the harbour is very loud.",
       [S_("toto", "Comandante. [shush] Gennaro is still down in the grotto under Punta d'Orsu. Three hours, he said. Three hours!",
           "fear"),
        S_("toto", "Low tide is in the day. The boat is ready. I am always ready. [sigh] Madonna, I am never ready.", "nervousness")],
       [O("Texts back: “Keep the boat ready.”", []),
        O("Sends him a thumbs up and finishes his coffee.", [])]),

    ER("er_kevin_frist", "Voice Message from Lea", (13, 14), OFFEN("kevin_jagd", "kevin_fertig"),
       "lea", "foredeck", "A voice message from Lea. Fast, a bit out of breath, and a lot of gulls.",
       [S_("lea", "Okay, don't panic. [gasp] But Kevin gets bored of his treasures. Then he drops them in the sea.", "nervousness"),
        S_("lea", "Page forty of Grandad's chart book. The bay, the cross, 1924. [laugh] Today, maybe? Please?", "nervousness")],
       [O("Texts back: “Today.”", []),
        O("Puts his shoes on.", [])]),

    ER("er_flut", "Voice Message from Totò (2)", (14, 19), OFFEN("grotte_fertig", "sirene_fertig", "grotte_flut"),
       "toto", "village_harbour", "A voice message from Totò, sent at 06:40. He sounds like he didn't sleep.",
       [S_("toto", "Comandante. [sniff] At high tide the grotto is humming again. I heard it from the boat, all night.", "fear"),
        S_("toto", "I am not rowing out there at night. Not for money, not for you. [sigh] If you want to know, go yourself. "
                   "In the evening, when the tide is in.", "nervousness")],
       [O("Texts back: “Then I go alone.”", []),
        O("Leaves him on read.", [])]),

    ER("er_flut_frist", "Voice Message from Totò (3)", (20, 20), OFFEN("grotte_fertig", "sirene_fertig"),
       "toto", "village_harbour", "Totò again. This time he isn't joking.",
       [S_("toto", "Comandante. [clear throat] One more evening, maybe two, and then we have bigger problems than a humming rock.",
           "nervousness"),
        S_("toto", "If you still want to know what hums in the grotto, go tonight. [sigh] When the tide is in.", "neutral")],
       [O("Texts back: “Tonight.”", []),
        O("Deletes it. Some things can stay a mystery.", [])]),
]


def tags_schreiben():
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "erinnerung"} for w, t, g in _TAGS]
    texte = {z["text"] for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "erinnerung" and z["text"] not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)

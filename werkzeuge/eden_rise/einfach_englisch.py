# -*- coding: utf-8 -*-
"""Einfaches Englisch (Duc, CLAUDE.md Nr. 2; Textpruefung Akt 3, 04.11.2026): Woerter und Wendungen, die Spieler ohne
Englisch als Muttersprache stolpern lassen. Jeder Eintrag: Muster (regulaerer Ausdruck, ohne Gross/Klein) -> Vorschlag.
Genutzt von tests/test_einfach_englisch.py fuer alle Akt-3-Texte (Events a3_, Kommission, Legenden ab Akt 3).
Erweitern statt abschalten: Ist ein Wort an einer Stelle wirklich richtig, kommt die Stelle in AUSNAHMEN."""
import re

VERBOTEN = {
    # doppeldeutig
    r"\bdr[ae]w(s|n|ing)?\b(?!\. (so )?nobody won)": "designed / marked / painted (draw kann auch Unentschieden oder ziehen heissen)",
    r"(?<!burning )(?<!burnt-out )\btorch(es)?\b": "flashlight oder burning torch (torch allein ist im Englischen beides)",
    r"\bin capitals\b": "in big letters",
    r"\b(the same|a careful|a neat|a shaky|written in (his|her|a)( own)?) hand\b(?! on| next)": "handwriting (hand als Handschrift ist selten)",
    r"\bscrew(ing|s|ed)? (it|the|that)\b(?! ?lid)": "put / close / turn (screw ist auch vulgaer)",
    r"\bproper come\b": "properly there",
    r"\bstream\b": "live video (stream kann Bach heissen)",
    # Redewendungen
    r"\bstands? (his|her|my|your|their) ground\b": "stays where he is",
    r"\bpiece of cake\b": "easy",
    r"\bbreak a leg\b": "good luck",
    r"\bon the same page\b": "agree",
    r"\bcall it a day\b": "stop for today",
    r"\bspill(ed)? the beans\b": "tell the secret",
    r"\bunder the weather\b": "ill",
    r"\bonce in a blue moon\b": "almost never",
    r"\bout of the blue\b": "suddenly",
    r"\bbite the bullet\b": "do it anyway",
    r"\bcost(s)? an arm and a leg\b": "very expensive",
    r"\bbeat(ing)? around the bush\b": "not saying it",
    r"\bhit the sack\b": "go to bed",
    # selten oder gehoben
    r"\bnonetheless\b": "still",
    r"\balbeit\b": "but",
    r"\bwhilst\b": "while",
    r"\bthereby\b": "so",
    r"\bnotwithstanding\b": "even with",
    r"\bplethora\b": "a lot",
    r"\bmyriad\b": "many",
    r"\bubiquitous\b": "everywhere",
    r"\bledger\b": "cash book",
    r"\bcistus\b": "bushes",
    r"\bmyrtle\b": "berries from the hill",
    r"\bmullet\b": "fish",
    r"\bbergerie\b": "shepherd's hut",
    r"\bunentschieden\b": "a draw, nobody won",
}
AUSNAHMEN = set()      # (Event-ID oder Quelle, Muster) fuer Stellen, an denen das Wort gewollt ist

_RE = [(re.compile(m, re.IGNORECASE), m, v) for m, v in VERBOTEN.items()]


def pruefen(texte):
    """texte: [(stelle, text)] -> [(stelle, gefundenes Wort, Vorschlag)]."""
    aus = []
    for stelle, t in texte:
        for rx, m, v in _RE:
            if (stelle, m) in AUSNAHMEN:
                continue
            hit = rx.search(t or "")
            if hit:
                aus.append((stelle, hit.group(0), v))
    return aus

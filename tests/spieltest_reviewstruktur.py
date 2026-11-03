"""Shared structure for personal, source-backed reviews and clean narration output."""
VERSION = 2
ABSCHNITTE = {
    "erwartung": "Was suche ich als diese Person in Eden Rise? Persönlich und konkret einsteigen.",
    "staerken": "Welche belegten Momente oder Systeme sprechen mich an, und weshalb?",
    "kritik": "Was stört mich? Beobachtung, persönliche Wirkung und Ursache auseinanderhalten.",
    "beziehungen_und_sexualitaet": "Charakterchemie, Begehren, Flirt, Kinks, Fanservice und Beziehungsfolgen aus dieser Perspektive beurteilen. Ohne Beleg offen lassen.",
    "fazit": "Für wen passt das bisher Gesehene? Eine klare vorläufige Tendenz und die wichtigste offene Frage.",
}
BEFUND = {
    "kriterium": "Eines der Kriterien des Profils",
    "art": "technik, inhalt, geschmack oder testluecke",
    "beobachtung": "Was ist tatsächlich belegt?",
    "interpretation": "Wie wirkt das auf diese Person?",
    "auswirkung": "Warum ist das für das Spielerlebnis relevant?",
    "prioritaet": "P1 = blockiert, P2 = wesentlich, P3 = Feinschliff; Geschmack allein ist kein technischer Blocker",
    "belege": "Mindestens eine gültige Quellen-ID",
    "naechster_test": "Konkrete Handlung und beobachtbares erwartetes Ergebnis",
}


def sprechtext(reviews):
    """Only render validated text; evidence IDs and repeated caveats live in the companion JSON."""
    out = ["Eden Rise. Neun fiktive Perspektiven. Vorläufige Einschätzungen anhand der jeweils gelieferten Quellen.", ""]
    for r in reviews:
        out += [r["name"], ""]
        for key in ABSCHNITTE:
            out += [r["review"]["rezension"][key]["text"].strip(), ""]
    return "\n".join(out)

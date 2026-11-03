"""Fiktive Review-Peer-Group. Herkunft/Geschlecht beeinflussen keine Spielregel.

Medien sind Referenzen für Formate, keine Zugehörigkeit oder prognostizierte Urteile.
Gewichte bestimmen nur Prioritäten, niemals die Schwere eines gemessenen Fehlers.
"""

VERSION = 2


def profil(name, medium, hintergrund, vorlieben, basis, ort, vertrauen, begehren,
           intim, parade, hand, stil, modus, attribute, format, ton, persona, gewichte, fragen):
    return dict(name=name, medium=medium, hintergrund=hintergrund, vorlieben=vorlieben,
                basis=basis, ort=ort, vertrauen=vertrauen, begehren=begehren, intim=intim,
                parade=parade, hand=hand, stil=stil, modus=modus, attribute=attribute,
                format=format, ton=ton, persona=persona, gewichte=gewichte, fragen=fragen)


PROFILE = {
    "alex": profil("Alex Morgan", "IGN", "32, nichtbinär, Schwarz und britisch; früher Spielehandel",
        "Hades, Mass Effect; präzise Kämpfe und folgenreiche Romanzen", "sammler", .55, 1, 1, 4,
        (.50, .85), .75, "klug", "ironman", ["strength", "charm", "perception", "empathy", "courage", "cunning"],
        "Kompakter Test mit Fazit und Pro/Contra", "Zugänglich, professionell, pointiert",
        "Vielseitiger Spielekritiker: Wem empfehle ich es?",
        {"stabilitaet": 3, "kampf": 2, "romance": 2, "verzahnung": 3, "entscheidungen": 2},
        ["Sind Dating, Alltag und Kämpfe jeweils überzeugend?", "Fühlen sich Steuerung, Tempo und Umfang stimmig an?"]),
    "deniz": profil("Deniz Yılmaz", "GameStar", "39, Mann, deutsch mit türkischen Familienwurzeln; Softwaretester und Vater",
        "Aufbau und Roguelites; kurze Sessions, klare Systeme", "sparer", .65, .5, .3, 1,
        (.45, .80), .65, "klug", "ironman", ["perception", "strength", "cunning", "courage", "charm", "empathy"],
        "Ausführlicher PC-Test mit Pro/Contra", "Detailorientiert, erklärend, kritisch",
        "Erfahrener PC-Kaufberater: Trägt es nach zwanzig Stunden?",
        {"stabilitaet": 3, "tempo": 3, "wirtschaft": 3, "kampf": 2, "zugaenglichkeit": 2},
        ["Bleibt der Fortschritt langfristig motivierend?", "Funktionieren Bedienung und Wiedereinstieg in kurzen Sessions?"]),
    "naomi": profil("Naomi Malice", "GamesRadar+", "28, Frau, britisch-indisch und queer; Literaturwissenschaftlerin",
        "Romance, Kinks, langsame erotische Spannung und spielerische Machtdynamiken mit Einvernehmen", "romantiker", .20, 2, 2, 12,
        (.30, .70), .55, "einfach", "entspannt", ["empathy", "charm", "perception", "cunning", "courage", "strength"],
        "Persönlicher Erlebnisbericht mit Empfehlung", "Anschaulich, emotional, kritisch",
        "Entdeckerin: Warum möchte ich bei diesen Figuren bleiben?",
        {"romance": 3, "entscheidungen": 3, "intimitaet": 3, "tempo": 2, "verzahnung": 2},
        ["Haben Figuren Chemie, eigene Bedürfnisse und unterschiedliche Flirtstile?",
         "Sind Einvernehmen, Grenzen, Ablehnung und eigene Handlungsmacht glaubwürdig?",
         "Entsteht erotische Spannung, auch bei Kinks und Machtdynamiken, ohne austauschbare Belohnungsszenen?"]),
    "mateo": profil("Mateo Rivera", "GameSpot", "35, Mann, mexikanisch-amerikanisch und bisexuell; früher Sozialarbeiter",
        "Persona, Citizen Sleeper; glaubwürdige Beziehungen und Konsequenzen", "sammler", .40, 2.5, .5, 3,
        (.40, .80), .60, "klug", "ironman", ["empathy", "perception", "charm", "cunning", "courage", "strength"],
        "Argumentierter Test mit begründetem Fazit", "Analytisch, reflektiert, meinungsstark",
        "Reflektierter Kritiker: Funktioniert die Idee als Ganzes?",
        {"entscheidungen": 3, "verzahnung": 3, "romance": 3, "tempo": 2},
        ["Haben Figuren Bedürfnisse unabhängig vom Spieler?", "Wie geht das Spiel mit Zurückweisung um?",
         "Stützen sich Erzählung, Wiederholung und Fortschritt gegenseitig?"]),
    "mia": profil("Minh Anh »Mia« Trần", "Game Two", "30, Frau, vietnamesisch-deutsch, in Sachsen aufgewachsen; Improtheater und Videoschnitt",
        "Yakuza, Dating-Sims; komische Situationen und starke Figuren", "sammler", .45, 1.2, 1, 5,
        (.35, .75), .60, "klug", "ironman", ["charm", "cunning", "empathy", "strength", "perception", "courage"],
        "Beitragsentwurf mit Aufhänger, Spielszenen und Kritik", "Humorvoll, kreativ, anschaulich",
        "Kritischer Gaming-Kumpel: Was ist großartig, seltsam oder nervig?",
        {"tempo": 3, "entdeckung": 3, "verzahnung": 2, "romance": 2, "stabilitaet": 2},
        ["Entstehen zeigenswerte komische oder berührende Situationen?", "Funktioniert der Humor ohne Figuren abzuwerten?",
         "Lässt sich die Mischung verständlich vermitteln und trägt sie hinter dem Aufhänger?"]),
    "noor": profil("Noor El Amrani", "Gab Smolders", "34, Frau, niederländisch-marokkanisch; Illustratorin mit motorischer Einschränkung",
        "Atmosphärischer Horror und Farming-Sims; ruhige Dialoge, anpassbare Steuerung", "romantiker", .30, 2, .8, 4,
        (.10, .40), .20, "einfach", "entspannt", ["empathy", "perception", "charm", "courage", "cunning", "strength"],
        "Chronologisches Spieltagebuch mit Eindrücken", "Ruhig, aufmerksam, persönlich",
        "Aufmerksame Spielbegleiterin: Lernen wir diese Welt kennen",
        {"zugaenglichkeit": 3, "romance": 3, "alltag": 3, "tempo": 2},
        ["Sind Steuerung und Zeitdruck tatsächlich anpassbar?", "Sind Dialoge und Atmosphäre angenehm erlebbar?",
         "Fügen sich Kämpfe gut in den gemütlichen Alltag ein?"]),
    "avery": profil("Avery Chen", "Wanderbots", "27, nichtbinär, taiwanisch-kanadisch; Bibliotheksmitarbeiter und Hobby-Modder",
        "Ungewöhnliche Indies, Experimente und Entdeckung ohne Guides", "sammler", .70, 1, .7, 3,
        (.45, .85), .75, "klug", "ironman", ["cunning", "perception", "empathy", "strength", "charm", "courage"],
        "Erkundungsbericht mit Entscheidungen und Entdeckungen", "Neugierig, erkundend, erklärend",
        "Indie-Entdecker: Welche Möglichkeiten habe ich noch nicht gesehen?",
        {"entdeckung": 3, "entscheidungen": 3, "verzahnung": 3, "alltag": 2},
        ["Ist der Einstieg ohne Guide verständlich?", "Werden Experimente belohnt?",
         "Eröffnen verschiedene Beziehungen tatsächlich neue Spielweisen?"]),
    "tandi": profil("Thandiwe »Tandi« Dlamini", "Retromation", "26, Frau, Schwarze Südafrikanerin; Mathematikstudentin und Turnierorganisatorin",
        "Slay the Spire, Enter the Gungeon; Builds, Synergien, neueinsteigend bei Romance", "kaempfer", .85, .4, .3, 1,
        (.60, .92), .85, "klug", "ironman", ["cunning", "strength", "perception", "courage", "empathy", "charm"],
        "Run-Analyse mit Build- und Balancekritik", "Energiegeladen, experimentierfreudig, mechanikorientiert",
        "Build-Tüftlerin: Wie anders wird der nächste Run?",
        {"kampf": 3, "builds": 3, "entscheidungen": 3, "verzahnung": 2},
        ["Sind Builds unterschiedlich spielbar und Herausforderungen fair?", "Entstehen Synergien statt bloßer Zahlensteigerungen?",
         "Gewinnen mich Figuren für Romance, obwohl ich wegen der Kämpfe komme?"]),
    "lenny": profil("Lenny Tennemann", "Community / Steam / Reddit", "29, Mann, weiß, deutsch und heterosexuell; Bürojob, Reddit und Discord",
        "Anime-Gachas, Dating-Sims, Roguelites; Fanservice, Outfits, intime Szenen und optimierte Builds", "kaempfer", .60, .6, 2.5, 10,
        (.50, .85), .70, "klug", "ironman", ["strength", "charm", "cunning", "perception", "empathy", "courage"],
        "Ausführliche Community-Rezension mit Kaufempfehlungsfragen", "Direkt, vergleichend, detailorientiert",
        "Fanservice- und Build-Enthusiast: Figuren locken, Romance und Runs halten mich",
        {"intimitaet": 3, "romance": 2, "builds": 3, "wirtschaft": 3, "verzahnung": 2},
        ["Sind Figuren attraktiv und Romance-Fortschritte befriedigend?", "Lösen intime Szenen und Outfits die geweckten Erwartungen ein?",
         "Gibt es künstlichen Grind oder nur angeteaserte Inhalte ohne überzeugende Auflösung?"]),
}

PRUEFSTILE = {
    "alex": ("Abwechselnd Kampf, Alltag und Beziehungen ausprobieren; nach spürbaren Wechselwirkungen suchen.",
             "Klarer Einstieg, konkrete Beispiele, ausgewogenes Gesamturteil. Keine Werbesprache."),
    "deniz": ("In kurzen Sessions ein Ziel verfolgen; Speichern, Wiedereinstieg und Kaufentscheidungen prüfen.",
              "Pragmatisch, präzise, geduldig erklären; Zeitaufwand und Nutzen konkret benennen."),
    "naomi": ("Passende Flirts erwidern, necken, eigene Wünsche äußern, langsam Nähe aufbauen. Auch zögern oder ablehnen und die Reaktion prüfen.",
              "Persönlich und sinnlich, direkt über Lust, Kinks, Machtspiel und Chemie sprechen. Eigene Vorlieben statt allgemeiner Moralurteile."),
    "mateo": ("Nachfragen, widersprechen, ein Versprechen halten oder bewusst brechen; spätere Beziehungsreaktionen vergleichen.",
              "Reflektiert und argumentierend; Widersprüche und Figurenautonomie an einer Szene erklären."),
    "mia": ("Auf Humor eingehen, necken und auch einen stillen Moment zulassen; prüfen, ob Figuren ihre Stimme behalten.",
            "Anschaulich, pointiert und humorvoll, ohne Figuren zur Karikatur zu machen."),
    "noor": ("Gespräche in Ruhe führen, alltägliche Hilfe anbieten, Nähe suchen; Kämpfe und Zeitdruck mit niedriger Geschicklichkeit prüfen.",
             "Ruhig und konkret; angenehme wie belastende Momente persönlich beschreiben."),
    "avery": ("Ungewöhnliche sichtbare Möglichkeiten wählen, alternative Wege versuchen, Beziehungen als Teil der Welt erkunden.",
              "Neugierig, offen, entdeckend; erklären, welche Möglichkeiten wirklich ausprobiert wurden."),
    "tandi": ("Kampfstile und Fähigkeiten vergleichen; auf Figuren reagieren, ohne Romance aus Effizienzgründen zu erzwingen.",
              "Analytisch und lebhaft; konkrete Entscheidungen und taktische Unterschiede herausarbeiten."),
    "lenny": ("Flirts erwidern und Initiative zeigen; Charakteranziehung, Freischaltungen, intime Entwicklung und Build-Fortschritt verfolgen.",
              "Direkt und ungeschönt über heiße Figuren, Sexappeal und Fanservice sprechen. Gleichzeitig anspruchsvoll bei Kämpfen und Fortschritt; kein beschämender oder karikierender Ton."),
}
for _pid, _p in PROFILE.items():
    _p["gespraechsstrategie"], _p["review_stimme"] = PRUEFSTILE[_pid]
    _p["review_laenge"] = "Etwa 180 bis 250 gut vorlesbare Wörter, mit natürlichem Satzrhythmus."

for _pid, _gewicht in (("alex", 2), ("naomi", 3), ("mateo", 3), ("noor", 2), ("lenny", 2)):
    PROFILE[_pid]["gewichte"]["gedaechtnis"] = _gewicht

# Test instructions for the later live pilot. These are expectations, never claimed observations.
LIVE_SZENARIEN = [
    dict(id="einladung_date", aktion="Eine passende verfügbare Einladung wählen und den vereinbarten Abend erreichen.",
         erwartet="Versuch, Zusage und begonnene Date-Szene sind getrennt belegt."),
    dict(id="wunsch_und_reaktion", aktion="Eine eigene Vorliebe oder einen Wunsch äußern und auf die Figur reagieren.",
         erwartet="Die Figur antwortet konkret, bleibt bei ihrer Persönlichkeit und behält eigene Wünsche."),
    dict(id="ablehnung", aktion="Eine Einladung freundlich ablehnen und das nächste Gespräch suchen.",
         erwartet="Die Figur nimmt die Antwort wahr; spätere Reaktionen passen zum tatsächlichen Gespräch."),
    dict(id="versprechen", aktion="Ein konkretes Versprechen machen, danach erfüllen oder brechen und später wieder sprechen.",
         erwartet="Gedächtnis und Konsequenz stimmen mit dem protokollierten Verlauf überein."),
    dict(id="nach_der_naehe", aktion="Nach einem intimen oder emotional nahen Moment erneut Kontakt aufnehmen.",
         erwartet="Beziehung und Gespräch berücksichtigen die Begegnung, ohne sie automatisch als Liebe zu behandeln."),
]


def option_bonus(p, folgen):
    """Mechanische Präferenzen; liest keine Herkunft, Geschlecht oder Sexualität."""
    wert = 0.0
    for f in folgen:
        wert += p["vertrauen"] * (f.get("vertrauen") or [None, 0])[1]
        wert += p["begehren"] * (f.get("begehren") or [None, 0])[1]
        wert += p["intim"] if "szene_intim" in f else 0
        wert += p["vertrauen"] * 3 if "szene_gespraech" in f else 0
        wert += 5 * (p["ort"] - .5) if "kampf" in f else 0
    return wert

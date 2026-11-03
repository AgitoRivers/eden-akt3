# Spieltest: der Bot, der das ganze Spiel prüft

### Beschleunigung des laufenden Live-Tests

`tests/spieltest_live.py` verwendet für künftig gestartete Profilprozesse folgende Optimierungen:
Bei genau einer sichtbaren Option ist kein Spieler-Modellaufruf erforderlich. Bei mehreren Optionen entscheidet weiterhin
das echte Modell. Bereits für die Anzeige erzeugte Ansichten werden für das Protokoll wiederverwendet; unnötige zusätzliche
Zustandslesevorgänge entfallen. Frei generierte Spieleräußerungen, Figurenantworten und Gedächtniszusammenfassungen bleiben live.

Exakt identische strukturierte Engine-Prüfungen mit ausdrücklich deterministischem Sampler dürfen wiederverwendet werden.
Der Schlüssel enthält Systemanweisung, gesamte Anfrage, Grammatik, Parameter, Modellidentität, Endpunkt und Stop-Sequenzen.
Stochastische Antworten, unstrukturierte Erinnerungen und Spielerentscheidungen werden nicht zwischengespeichert.
Das gemeinsame Verzeichnis `deterministische-pruefungen/` liegt neben den Profilordnern. Wiederverwendung und erzwungene
Einzeloptionen werden separat unter `optimierung.jsonl` und in Status/Ergebnis gezählt; Cache-Treffer zählen nicht als echte
neue Modellaufrufe. Die Optimierungen ändern keine Spielregeln und ersetzen keine echten Dialoge durch Platzhalter.

Der bereits laufende Naomi-Prozess wurde dafür nicht unterbrochen oder neu gestartet. Die Änderungen greifen bei den
folgenden Profilprozessen. Eine tatsächliche Zeitersparnis ist erst anhand ihrer Logs messbar.

## Überarbeitung nach der ersten Peer-Group-Abnahme

Profilversion und Rezensionsschema sind jetzt **Version 2**. Diese Überarbeitung wurde ausschließlich mit isolierten
Logik-/Auswertungstests geprüft. Kein neuer Spielverlauf und kein Modellaufruf wurde dafür gestartet.
Alte Läufe bleiben als historische Messungen mit ihrer ursprünglichen Profilversion gekennzeichnet.

### Korrekturen an der Spielweise

- Review-Profile wählen Event-Antworten anhand sichtbarer Texte und Sperren. Versteckte Belohnungen, Erfolgsfolgen,
  Affinitätswerte und Flags fließen nicht mehr in diese Antwortwahl ein. Die Textzuordnung ist eine einfache, dokumentierte
  Heuristik, kein semantisches Spieler-LLM. Unbekannte Formulierungen werden mit reproduzierbaren Gleichständen erkundet.
- Das Kompliment an erster Stelle verdrängt nicht mehr jede Einladung. Romance-orientierte Profile versuchen verfügbare
  Einladungen, ohne eine bestehende Verabredung durch weitere Einladungen zu überladen. Voraussetzungen werden nicht umgangen.
- Gezählt werden getrennt: Einladungsversuch, angenommene Engine-Aktion, tatsächlich vereinbarter Termin und begonnene
  `date_`-Szene. Eine angenommene Aktion bedeutet nicht, dass die Figur zugesagt hat. Null Date-Szenen im alten Lauf
  beweisen deshalb keinen fehlenden Inhalt; dort fehlt die neue Einladungstelemetrie.
- Erfolgreiche Event-Antworten werden zusätzlich zu Versuchen erfasst; Auswahlgründe enthalten IDs und Kategorien, keine Storytexte.
- Hilfseingriffe enthalten künftig Tag, Phase, Kampf, Niederlagenzahl und die veränderte Paradechance. Der betreffende Kampf
  wird markiert. Ein mit Hilfe erreichter Endpunkt zählt nicht als selbstständig bestanden. Flucht ist in der Peer-Auswertung
  separat erfasst und kein Sieg.

Andere Routinen greifen weiterhin auf Engine-Zustände zu. `testmodus.wissen = hybrid` weist das ausdrücklich aus.
Das ist noch kein vollständiger Test aus ausschließlich sichtbaren Browserinformationen und kein autonomer Live-Spieler.

### Aufbau der Rezensionen

Jede Stimme bekommt dieselbe nachvollziehbare Grundstruktur, aber eigene Vorlieben, Gesprächsstrategien und Ausdrucksweisen:

1. Persönliche Erwartung und Einstieg.
2. Konkrete Stärken und deren Wirkung auf diese Person.
3. Kritik mit nachvollziehbarer Ursache.
4. Beziehungen und Sexualität aus der jeweiligen Perspektive.
5. Vorläufiges Fazit mit Zielgruppe und wichtigster offener Frage.

Naomi darf direkt über Lust, Kinks, erotische Spannung und Machtspiel urteilen. Lenny darf Sexappeal, Fanservice,
Freischaltungen und deren Auflösung wichtig finden. Keine Stimme wird dafür beschämt oder zur Karikatur gemacht.
Andere Profile müssen diese Interessen nicht teilen. Es werden weder positive noch negative Inhaltsurteile vorgeschrieben.

Der strukturierte Anhang trennt pro Befund **Beobachtung → persönliche Interpretation → Auswirkung → nächster Test**,
mit Quellen-IDs und Priorität. Technische Fehler, inhaltliche Kritik, Geschmack und Testlücken bleiben unterscheidbar.
Geschmack allein ist kein P1-Blocker. Die Validierung prüft vollständige Abschnitte und gültige Belegverweise;
die inhaltliche Richtigkeit einer Interpretation muss weiterhin kontrolliert werden.

Nach erfolgreichem lokalem Inhaltsreview entstehen `inhaltsreviews.json` und zusätzlich `inhaltsreviews_vorlesen.txt`.
Die Vorlesefassung enthält natürliche Absätze ohne Beleglisten; Details bleiben im JSON-Anhang. Das Offline-Ampelprotokoll
wird nicht automatisch in erfundene persönliche Spielerfahrungen umgeschrieben.

Das Review-Paket mischt Kalenderstreuung und profilrelevante Textstichproben, damit etwa intime Einladungen nicht allein
durch gleichmäßige Stichprobenauswahl verloren gehen. Eventdefinitionen bleiben als solche markiert, nicht als tatsächlich
generierte Gespräche. Das zusätzliche Prüffeld Figurentreue und Beziehungsgedächtnis bleibt bis zu echten Dialogbelegen offen.

### Nächster, separat zu startender Pilot

`LIVE_SZENARIEN` in `tests/spieltest_profile.py` beschreibt noch nicht ausgeführte Prüfaufträge: Einladung bis zum Date verfolgen,
einen Wunsch äußern, eine Einladung ablehnen, ein Versprechen erfüllen oder brechen und die nächste Begegnung nach Nähe prüfen.
Der dazu nötige Live-Spieler mit echten Gesprächsprotokollen ist weiterhin ein gesonderter Umsetzungsschritt.
Keine dieser Szenarien wird allein durch das Anlegen der Struktur automatisch gestartet oder als bestanden markiert.

Reine Prüfung ohne Spiel-/Modellstart:
`python -m unittest discover -s tests -p test_spieltest_peer.py -v`.

> Stand 30.10.2026 · Beschluss Duc 30.10.: eigener Bot neben dem Gate, prüft in allen wichtigen Hinsichten nach modernen Maßstäben

## Kurz
`tests/spieltest.py` spielt standardmäßig als neun fiktive Mitglieder einer Review-Peer-Group bis zum gebauten Ende des Kalenders.
Die bisherigen sechs technischen Spielertypen bleiben mit `--klassisch` erreichbar. Neben dem technischen Ampelbericht entstehen
neun belegte Review-Entwürfe mit individuellen Prioritäten, Messwerten je Seed und offenen menschlichen Prüffragen.
Er läuft ohne Sprachmodell, Stimme und Netz in einem Wegwerf-Ordner. Spielstände und Moduldaten bleiben unberührt.

```
python tests\spieltest.py                 # 9 Review-Profile × 3 Seeds; Dauer abhängig von Spielwegen und Rechner
python tests\spieltest.py --profile       # Namen und Profil-IDs auflisten
python tests\spieltest.py --klassisch     # bisherige 6 technischen Typen × 3 Seeds
python tests\spieltest.py --typen naomi,lenny --seeds 2
python tests\spieltest.py --seeds 5       # mehr Seeds, bessere Zahlen
python tests\spieltest.py --typen chaos,schwach --seeds 1
python tests\spieltest.py --auswerten     # letzte Läufe neu auswerten, z. B. nach geänderter Grenze
python tests\spieltest.py --seeds 1 --ziel tests\spieltest_ergebnis\eigener_lauf
```

Ergebnis in `tests/spieltest_ergebnis/` (nicht im Git): `bericht.html`, `letzter.json` für den Vergleich mit dem nächsten Lauf, `verlauf/`.
Zusätzlich `peer_group.html`, `peer_group.md` und `peer_group.json`. Rohdaten mit IDs, Aktionen und Seeds stehen in `roh.json`.
Exit 1 bei Absturz, Sackgasse oder einem Lauf, der das Ende nicht erreicht.

## Review-Peer-Group

Alle Personen sind fiktiv. Mediennamen stehen für die gewünschte Formatperspektive, nicht für echte Zugehörigkeit,
eine Freigabe der Medien oder eine Vorhersage ihrer Rezension. Es werden keine Gesamt- oder Spaßnoten erfunden.

| ID | Person | Formatreferenz | Prioritäten |
|---|---|---|---|
| alex | Alex Morgan | IGN | Gesamtpaket, technische Qualität, Romance und Kampf |
| deniz | Deniz Yılmaz | GameStar | Langzeitmotivation, Wirtschaft, Speichern, kurze Sessions |
| naomi | Naomi Malice | GamesRadar+ | Figuren, erotische Spannung, Kinks, Einvernehmen, Handlungsmacht |
| mateo | Mateo Rivera | GameSpot | Konsequenzen, Figurenautonomie, Zurückweisung, Verzahnung |
| mia | Minh Anh »Mia« Trần | Game Two | Zeigenswerte Situationen, Humor, Figuren, Tempo |
| noor | Noor El Amrani | Gab Smolders | Atmosphäre, Alltag, Dialoge, motorische Zugänglichkeit |
| avery | Avery Chen | Wanderbots | Entdeckung, Experimente, Einstieg, neue Spielweisen |
| tandi | Thandiwe »Tandi« Dlamini | Retromation | Builds, Synergien, Fairness, abwechslungsreiche Runs |
| lenny | Lenny Tennemann | Community / Steam / Reddit | Attraktive Figuren, Fanservice, Freischaltungen, Builds, Grind |

Definitionen mit Hintergründen, Vorlieben, Ton, Format, Kriteriengewichten und persönlichen Prüffragen stehen in
`tests/spieltest_profile.py`. Herkunft, Geschlecht und Sexualität bestimmen keine Regel und kein Urteil.
Spielentscheidungen folgen ausschließlich expliziten individuellen Vorlieben und der simulierten Geschicklichkeit.

### Tatsächlich unterschiedliche Wege

Profile variieren die Wahrscheinlichkeit für Expeditionen statt Szenen, die Wahl von Dates und neuen Szenen,
die Gewichtung sichtbarer Flirt-, Fürsorge-, Erkundungs- und Kampftexte bei Event-Antworten, Attribute sowie erlernte Fähigkeiten.
Noor spielt entspannt mit niedriger simulierter Geschicklichkeit und nutzt zusätzlich die Farm. Naomi und Lenny probieren
freigeschaltete, nicht als unerwünscht markierte Intimitätsaktionen aus. Keine Freischaltung und keine Grenze wird umgangen.
Der Bot zählt erfolgreiche Engine-Aktionen; eine angenommene Intimitätsaktion ist kein Beleg für Einvernehmen im generierten Dialog.

Die Profile nutzen weiterhin die bewährten Basisroutinen der sechs technischen Typen. Sie sind keine neun autonomen Sprachmodelle.
Auch sie kennen interne Zustände und vordefinierte Folgen: Orientierung ohne Guide ist damit nicht realistisch simuliert.

### Review und Belege

`tests/spieltest_peer.py` erstellt je Profil einen vorläufigen Review-Entwurf, priorisierte Prüffelder und Messwerte je Seed.
Laufbelege tragen `profil/seed`; begrenzte Aktionsbelege enthalten Tag, Phase und Event-/Szenen-IDs, keine Storytexte.
Keine Daten eines anderen Profils werden als eigene Erfahrung verwendet. Ein schlechter Seed wird nicht durch Medianbildung versteckt.
Technische Blocker bleiben unabhängig von persönlichen Prioritäten gruppenweit sichtbar.

- **Grün:** die bezeichnete Messprüfung oder Prüfabdeckung wurde erfüllt. Kein allgemeines Qualitätsurteil.
- **Gelb:** beobachtete Auffälligkeit oder heuristische Warnung; Ursache überprüfen.
- **Rot:** technischer Fehler in der Prüfung.
- **Offen:** Daten oder Abdeckung fehlen. Kein negatives Urteil über vorhandene Spielinhalte.

Kriterien umfassen Stabilität, Kampf, Romance, Verzahnung, Entscheidungen, Tempo, Wirtschaft, Zugänglichkeit, Intimität,
Alltag, Entdeckung, Builds sowie Figurentreue und Beziehungsgedächtnis. Die Gewichte 1–3 ordnen die persönliche Priorität, nicht die Fehlerschwere.
Gleichzeitiges Auftreten von Alltag, Dating und Kampf belegt keine kausale Verbindung dieser Systeme.
Identische definierte Optionsfolgen sind nur ein Hinweis: andere Texte können dennoch erzählerisch bedeutsam sein.

Chemie, Humor, Kinks, Fanservice, Attraktivität, Outfits, Einvernehmen, Dialogqualität und echte Zugänglichkeit werden
als konkrete offene Prüffragen ausgegeben. Der Offline-Bot kann diese subjektiven bzw. im Browser oder Sprachmodell
entstehenden Eigenschaften nicht abschließend rezensieren. Dafür braucht es einen menschlichen Spieltest oder später
einen gesonderten inhaltlichen Reviewer mit tatsächlichen Szenentexten und gekennzeichneten Beobachtungsgrenzen.
`--auswerten` erfindet keine nachträglichen Profil-Läufe und keine in alten Rohdaten fehlende Telemetrie.
Nach geänderten Spielregeln oder Spielpräferenzen neu spielen; Neuauswertung allein ändert keine Spielentscheidungen.

Prüfung der Review-Auswertung: `python -m unittest discover -s tests -p test_spieltest_peer.py -v`.

### Optional: tatsächliche Textstichproben rezensieren

Der getrennte Inhaltsreview-Modus nutzt das vorhandene lokale Spielmodell auf `127.0.0.1:5010`:

```
python tests\spieltest_rezension.py --paket  # bewusstes Opt-in: Texte gespielter Event-Definitionen lokal exportieren
python tests\spieltest_rezension.py --lokal  # neun profilbezogene Inhaltsreviews mit dem lokalen Modell
python tests\spieltest_rezension.py --lokal --typen naomi,lenny
```

Mit `--roh PFAD` andere Rohdaten und mit `--ziel ORDNER` einen getrennten Ausgabeordner wählen.
Das Paket enthält bis zu zwölf Event-Stichproben je tatsächlich gespieltem Profil, über den erreichten Kalender verteilt,
sowie Messwerte und die persönlichen Kriterien. Nicht erreichte Events, ganze Story-Dateien und interne Falllösungen
werden nicht als zusätzliche Quellen geladen. Eventdefinitionen sind kein Transkript: konditionale Texte darin müssen
nicht alle angezeigt worden sein; protokollierte Antwortversuche müssen nicht alle angenommen worden sein.

`inhaltsreview_paket.json` enthält bewusst Spieltexte und damit mögliche Spoiler. Die normalen Peer-Berichte bleiben ohne
Storyzitate. Das lokale Modell liefert `inhaltsreviews.json`: Kurzfazit, Interpretation oder offen je Kriterium,
Quellen-IDs, Begründung und konkrete nächste Tests. Unbekannte Quellen, fehlende Kriterien und unbelegte Interpretationen
werden zurückgewiesen. Quellenprüfung bestätigt nur gültige IDs, nicht automatisch die Richtigkeit einer Interpretation.
Ein Mensch muss die Modellurteile kontrollieren. Schreibstil, Prioritäten und individuelle Vorlieben werden mitgegeben.

Ist das Modell nicht erreichbar, endet nur dieser optionale Aufruf mit Fehler. Es gibt keinen Cloud-Fallback, keine
erfundene Ersatzrezension und kein Überschreiben einer vorhandenen gültigen Rezension. Der Offline-Spieltest bleibt nutzbar.
Auch mit Modell sind das Interpretationen verfasster Stichproben, keine menschlichen Erfahrungen oder vollständigen
Tests der freien Dialoggenerierung, visueller Attraktivität, Intimszenen, Browserbedienung oder des gesamten Spiels.

## End-to-End bis zum Ende von Akt 2 (Duc 02.11.2026)

**Die Belagerung wird gespielt, nicht übersprungen.** Bisher kürzte der Spieltest-Bot die Taktik-Karte mit `bot_sieg` ab. Jetzt spielt `spieltest_bot.py` (`taktik`, `_taktik_trupp`) sie über dieselben Aktionen wie der Client: Briefings und Szenen, die Wahl bei Minicu, Aufstellen, Ziehen, Angreifen (Duc und Maxwell gehen in den echten Kampfbildschirm), Leute aus brennenden Häusern retten, morgens flicken (Ring oder Petrus Trupp). Ohne Gegner in Reichweite geht ein Trupp zu dem Feind, der der Kirche am nächsten ist. Eine verlorene Welle startet neu, nach drei Niederlagen kürzt der Bot ab und vermerkt das unter `taktik.hilfe`, nie als bestanden. Das Gate (`lauf_test.py`) kürzt weiter ab und bleibt unverändert.

**Kalender-Prüfung** (`python tests\spieltest_kalender.py`, nach `tests\spieltest.py`): Jede Pflicht-Szene eines festen Tags von Tag 8 bis 23 muss in mindestens einem Lauf vorkommen. Fehlt eine ohne Bedingung, ist der Kalender kaputt (Exit 1), fehlt eine mit Bedingung, ist es ein Hinweis. Dazu: Wie viele Läufe erreichen das Ende von Akt 2 (`akt2_ende`), wie viele gewinnen die Belagerung, Neustarts, Kämpfe, Hilfe.

**Befunde vom 02.11.2026:** Der Bot kaufte weiter, als die Tasche schon voll war, und meldete nach 25 Ablehnungen eine Sackgasse (Mateo, Seed 2, Tag 17). Das war ein Fehler des Bots, er prüft jetzt den Platz vor dem Kauf. In Welle 6 fiel die Kirche, weil der Bot seine Trupps im Norden und an der Yacht ließ; seit er zur Kirche zurückgeht, braucht kein Lauf mehr Hilfe.

## Gate oder Spieltest?
| | `tests/lauf_test.py` (Gate) | `tests/spieltest.py` |
|---|---|---|
| Frage | Haben sich die Regeln ungewollt geändert? | Ist das Spiel gut und vollständig spielbar? |
| Weg | immer derselbe, gegen Referenz | neun Review-Profile oder sechs klassische Spielweisen, mehrere Seeds |
| Dauer | 27 Sekunden | einige Minuten |
| Wann | nach jeder Kernänderung | vor Meilensteinen, nach großen Inhalten |

Das Gate bleibt unverändert. Sein Bot darf nicht umgebaut werden, sonst müssten alle Referenzen neu.

## Spielertypen
| Typ | Spielweise |
|---|---|
| Alles-Sammler | sucht Neues: Orte zuerst, unbekannte Antworten, Abbauen, Angeln, Farm, Handy, Ermittlung, Parade gut |
| Romantiker | Zeit mit der Liebsten, Geschenke, Verabredungen, weicht Kämpfen aus, spielt im Modus „entspannt“ |
| Kämpfer | Orte, Training, Spezialangriffe, Items im Kampf, Werkstatt, Parade gut |
| Sparer | gibt wenig aus, sammelt und verkauft |
| Schwacher Spieler | nur Angriff, Parade schlecht, scheut Proben. Nach 5 Niederlagen hilft ihm der Bot durch und notiert die Stelle |
| Chaos-Spieler | wählt zufällig und sucht so Abstürze |

## Bereiche
| Bereich | Vorbild | Misst |
|---|---|---|
| Stabilität | Mindeststandard | Abstürze, Fehler der Anzeige, Sackgassen, abgelehnte Angebote, Speichern und Laden, Wiederholbarkeit |
| Vollständigkeit | Zelda | Events, Antworten, Kämpfe, Orte, Aufträge, Items, Spiel-Aktionen, die nie vorkamen |
| Tagesschleife und Tempo | Stardew Valley, Persona 5 | leere Tage, Lücken ohne Belohnung, offene Ziele am Abend, neue Mechaniken je Tag, Spielzeit |
| Kampf und Schwierigkeit | Hades, Clair Obscur | Siegquote je Kampf und Stärke, Züge, Leben am Ende, Nutzen von Taktik, Stufe, Waffen, Stellen zum Festfahren |
| Wirtschaft | Dave the Diver | Kontostand je Tag, Quellen und Senken, ungenutztes Geld, volle Tasche |
| Entscheidungen | Hades, Balatro | Scheinwahlen, klar beste Antworten, Flags ohne Leser, Unterschied zwischen Läufen |
| Inhalte und Sprache | Lokalisierungsprüfung | Aufnahmen, Stimm-Tags, deutsche Reste, fehlende Bilder, lange Sätze und Texte |

Die Grenzwerte stehen oben in `tests/spieltest_auswertung.py`. Sie sind Startwerte und kein Branchenstandard. Die Spielzeit ist eine Schätzung
(Annahmen im Bericht). Geplant ist noch die Bildschirmprüfung im Browser (Stufe 3): Abschneiden bei 720p, 1080p und 1440p, Konsole, Tastatur.

## Was er nicht kann
- **Spaß messen.** Er findet Anzeichen wie Leerlauf oder Scheinwahlen. Ob eine Szene wirkt, muss ein Mensch beurteilen.
- **Das Sprachmodell testen.** Freie Szenen und `swipe`, `handy_chips` laufen gegen einen festen Platzhaltertext.
- **Rätselkämpfe fair werten.** Der Bot kennt den Trick nicht unbedingt, solche Kämpfe sind höchstens gelb.
- **Kaufentscheidungen werten.** Er kauft wenige Dinge am Tag. „Nie gekauft“ ist kein Urteil über ein Item.
- **Flags sicher beurteilen.** „Flag ohne Leser“ ist grob: Wer Flags über einen Präfix liest, zählt dort mit.

## Neue Mechanik
Aktionen liest der Bericht aus `aktion()` in `eden.py`. Eine neue Aktion erscheint darum von selbst unter „ungetestet“. Dann in
`tests/spieltest_bot.py` eine Stelle ergänzen, an der ein passender Spielertyp sie nutzt. Der Bericht zeigt nur IDs und Zahlen: bitte keine Story-Texte hineinschreiben.

## Modellvergleich (Sprachmodell testen)
Der Bot testet das Sprachmodell nicht. Dafür gibt es `tests/llm_vergleich.py` (Stand 02.11.2026): Es baut die echten Prompts über
`kern/szene.py` und `kern/figurenrahmen.py` und schickt sie an ein lokales Kobold auf Port 5021 (nie den Spielport 5010). Jeder Fall läuft
mit festen Seeds (11, 22, 33). `tests/llm_vergleich_jury.py bauen|zaehlen` erzeugt blinde Jury-Dateien ohne Modellnamen.
`tests/llm_vergleich_seite.py` baut die Abnahme `docs/abnahme/llm_vergleich/index.html`. Ein neues Modell trägt man in `MODELLE` ein und startet `--modelle name`.
Das dauert etwa 15 Minuten, wegen der Laufzeit über den Aufgabenplaner.

Was wir dabei gelernt haben:
- **Erfundene gemeinsame Erinnerungen** und ein **aufgeweichtes Nein** zeigen alle sechs getesteten Modelle. Ein Modellwechsel löst das nicht,
  die Lösung muss in den Code: feste Ausweich-Zeile bei Erinnerungsfragen, feste zweite Absage, fester Themenwechsel.
- Was vom Modell abhängt: Erkennen getippter Handlungen, Grenzen, Länge, Tempo. Giftige Blume bleibt das Spielmodell.
- Blume lief in Runde 2 als Kontrolle noch einmal mit. Die Jury kam auf fast dieselben Zahlen, ihr Urteil ist also beständig.
  Einzelne Urteile bleiben trotzdem Grenzfälle, deshalb ist jede Zahl eine Summe aus drei Seeds.

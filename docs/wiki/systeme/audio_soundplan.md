# Eden Rise – erweiterter Audio- und Soundeffektplan

Stand: 24.10.2026. Prüfung der aktuellen Moduldateien und aktiven Musik-/SFX-/Kampfpfade. Empfehlungen und Bestandsprüfung, keine neue Erzeugung oder Änderung der Spielauslöser.

## Ergebnis

Vorhanden sind **39 Effektarten mit 168 MP3-Dateien**. Die aktuelle Auswahl liefert **49 abspielbare Varianten**; alle ausgewählten Dateien sind vorhanden und nicht leer. Alle 15 expliziten Zielverweise zeigen auf heutige Szenen-/Event-IDs. Das bestätigt Existenz, nicht musikalische Qualität oder die semantisch richtige Platzierung. Keine Hörprüfung durchgeführt.

Der heutige Umfang umfasst 32 inszenierte Hauptszenen, 162 Ereignisse, 7 Kämpfe, 16 Spezialfähigkeiten und 68 Missionen, darunter 12 Reparatur- und 9 Kochmissionen. Waffenfamilien statt jedes einzelnen Gegenstands separat vertonen.

Die größte Wirkung bringen jetzt **räumliche Yacht-/Meeresatmosphäre, Gefahrenmomente und Kampfrückmeldung**. Weitere allgemeine Benachrichtigungspings haben eine geringere Priorität.

## Was bereits abgedeckt ist

- Bedienung: Klick, Meldung, abgelehnte Aktion, Phasen- und Tageswechsel.
- Würfel: Rollen, Erfolg, Fehlschlag, kritischer Erfolg und Patzer.
- Fortschritt: Geld, Items, Missionen, Codex-Fund, Geschenk, Vertrauen und Begehren.
- Persönliche Szenen: Nachrichtenvibration, Klopfen, Kochen, Brutzeln, Gläser und Sektkorken.
- Schiff/Story: Hubschrauber, Blackout, Strom zurück, Sturm, Ankerkette, Tender, Wasserplatsch und Funk.
Diese 39 Familien zunächst behalten und qualitativ anhören. Nicht pauschal neu erzeugen.

## Zuerst die Auslöser korrigieren

1. **Strom zurück ist an das Verlassen von Blackout gekoppelt.** Die aktuelle Abfolge geht danach in eine weitere Gefahrenszene. Der Client spielt den Ton beim Szenenwechsel, ohne einen bestätigten Stromzustand zu prüfen. An eine echte Wiederherstellung koppeln.
2. **Tender bei `landgang_2`:** Die aktuelle Szene liegt in Alvas Bar. Ein Motorstart beim Eintritt passt dort nicht zwangsläufig. Nur bei tatsächlicher Überfahrt abspielen.
3. **Cold Open / Explosion:** Musik bleibt absichtlich stumm, aber im SFX-Katalog gibt es dafür keinen eigenen Alarm-/Knall-Auslöser. Stille Musik allein ersetzt die Geräuschinszenierung nicht.
4. **Kämpfe:** Die laufenden Kampf-/Skill-Dateien bieten Treffer-, Parade-, Konter- und Spezialphasen für visuelle Effekte, aber keinen entsprechenden Kampfaudio-Aufruf. Allgemeine Klick- oder Würfeltöne sind dafür kein Ersatz.
5. **Anrufe:** Nachrichtenvibration existiert; ein durchgängiger Annehmen-/Auflegen-Ablauf und die koordinierte Musikabsenkung fehlen.
6. **Ereignisbeginn:** Aktuell häufig derselbe allgemeine Startsound. Nicht zusätzlich einen Gag-Jingle auf einen ernsten Bordrat oder persönlichen Abend legen. Musik und ein passender physischer Akzent reichen oft.
7. **Prioritäten:** Der SFX-Client spielt maximal zwei aus einer geordneten Kandidatenliste und begrenzt gleichzeitige Audios auf sechs. Das ist eine Begrenzung, aber noch kein Mixer mit Dialog-/Kampf-/Ambient-Prioritäten. Verzögerte Sounds zudem an die aktuelle Szene binden, damit sie nach einem Wechsel nicht nachklingen.

## Top 30 Ergänzungsfamilien

P0 = erste Umsetzungsrunde, P1 = nächste Runde, P2 = Feinschliff. Diese Liste umfasst **Soundfamilien**, nicht 30 sofortige Generationen. Vorhandene Geräusche werden wiederverwendet, wo sie passen.

| # | Prio | Geräuschfamilie | Aktueller Einsatz | Verhältnis zum Bestand |
|---|---|---|---|---|
| 1 | P0 | **Leises Wasser am Rumpf, Wind und Tauwerk** (Loop) | Deck, Badeplattform, sonnige Außengespräche | Kein Umgebungsloop vorhanden; Platsch-Einzeleffekt reicht dafür nicht. |
| 2 | P0 | **Ruhiges Ankerwasser, vereinzeltes Holzknarzen** (Loop) | Freie Nacht, Brückenwache, ruhige Romantik | Ankerkette vorhanden; sie ist ein einmaliges Ereignis und keine Nachtatmosphäre. |
| 3 | P0 | **Hafenwasser, entfernte Möwen, Takelage** (Loop) | Cala-Orsu-Hafen und Calvi | Tender und Platschen vorhanden, aber kein kontinuierlicher Hafenraum. |
| 4 | P1 | **Gedämpfter Schiffsrumpf und dezente Lüftung** (Loop) | Kabine, Salon, Crew-Messe | Leise halten; Kabine deutlich intimer und ohne laute Außenmöwen mischen. |
| 5 | P1 | **Lüfter, Relais und elektrischer Antrieb / Werkstatt** (Loop) | Power room, Generatorraum, Rosis freie Szenen | Je nach tatsächlichem Strom-/Betriebszustand abschalten; kein Dieselbrummen bei jedem Raum. |
| 6 | P0 | **Klarer, begrenzter Schiffs-/Störungsalarm** (Kurzloop) | Cold Open und bestätigte Gefahr | Fehlt. Beim Not-Aus oder Ende der Gefahr stoppen; keine Dauerbeschallung unter langen Dialogen. |
| 7 | P0 | **Kurzer elektrischer Überschlag, dumpfer Knall, Metallnachhall** (Einzeln) | Cold Open / Explosion | Blackout-Ton vorhanden, ersetzt aber keinen Gefahren-Impact. Pro tatsächlichem Ereignis einmal. |
| 8 | P0 | **Feuerknistern, Flammenstoß und Löschzischen** (Loop + Ende) | Bestätigter Brand / Fackelkontext | Fehlt; nur bei aktivem Feuer. Ende an Löschung koppeln, nicht an beliebigen Seitenwechsel. |
| 9 | P0 | **Schwerer Schalter / Relais fällt ab / kontrolliertes Wiederanlaufen** (Einzeln) | Not-Aus, Reparaturabschluss, echter Stromwechsel | Strom-zurück-Datei vorhanden. Zuerst den Auslöser korrigieren, dann ggf. kurze mechanische Ergänzung. |
| 10 | P0 | **Kurze leichte und schwere Waffenbewegung** (Einzeln) | Ausholen und Angriff | Neue Kampffamilie. Bewegung und Treffer getrennt, damit Fehlschläge keinen Treffer vortäuschen. |
| 11 | P0 | **Körper-/Kleidungstreffer; harte Metall-/Holzvariante** (Einzeln) | Bestätigter Treffer auf Duc oder Gegner | Fehlt. Materialfamilien teilen, keine eigene Aufnahme für jede Waffe nötig; keine übertriebene Brutalität. |
| 12 | P0 | **Kurzer metallischer Block und gedämpfter Waffenfang** (Einzeln) | Tatsächlich gelungene Parade | Fehlt. Nah am bestätigten Paradezeitpunkt statt am bloßen Klick. |
| 13 | P0 | **Knapper Luftzug und Schritt auf dem Untergrund** (Einzeln) | Ausweichen / vorbeigehender Angriff | Fehlt. Kein Trefferklang bei einem Fehlschlag. |
| 14 | P0 | **Klarer, kurzer Akzent für perfekte Parade und Konter** (Einzeln) | Perfekte Parade → Konter | Fehlt. Mit Parade/Impact schichten; kein dreifacher lauter Erfolgsjingle. |
| 15 | P1 | **Kurzer Schrotflintenknall mit kontrolliertem Nachhall** (Einzeln) | Aktuell vorhandene Doppelflinte | Fehlt. Eigener Pegel, nie mit voller Originallautheit unter Sprache; Laden nur bei echter Aktion. |
| 16 | P1 | **Kurzer elektrischer Schlag / Lichtbogen** (Einzeln) | Taser, Elektro-Harpune und passende Fähigkeiten | Fehlt. Gemeinsame Familie, bei Waffen unterschiedlich kurz/kräftig. |
| 17 | P1 | **Druckvolle, weiche Windbewegung in kurzen Schichten** (Einzeln) | Wind-Spezials und deren sichtbare Phasen | Fehlt. An tatsächlich übermittelte Skill-ID/Phase koppeln, nicht bloß an Effektfarbe. |
| 18 | P1 | **Wasseraufbau, Welle, gerichteter Aufprall** (Einzeln) | Wasser-Spezials | Ein Platsch ist vorhanden. Für große Skills als Akzent wiederverwenden, eigene Wellen-/Druckschicht ergänzen. |
| 19 | P1 | **Kurzer Zündstoß, Flammenbewegung, Ausklang** (Einzeln) | Feuer-Spezials und brennende Waffe | Fehlt. Nicht bei jedem Schaden über Zeit denselben langen Feuerstoß abspielen. |
| 20 | P1 | **Kurzer Energieaufbau und Freisetzungsakzent** (Einzeln / begrenzt) | Spezialphase Aufladen / Auslösen | Fehlt. Abbruch/Ende muss die Ladung stoppen; keine schrillen Dauertöne. |
| 21 | P1 | **Warmer, kurzer Heilungsakzent ohne auffällige Melodie** (Einzeln) | Bestätigte Heilung | Fehlt. Von Würfelerfolg und Beziehungs-Feedback klanglich unterscheiden. |
| 22 | P1 | **Dezenter Status-Akzent: Schutz / Schwächung / Brechen** (Einzeln) | Neue Statuswirkung und Ende eines Schutzes | Fehlt. Keine Dauerschleife für jeden aktiven Status, keine Wiederholung pro Redraw. |
| 23 | P1 | **Waffe senken / kurzer körperlicher Ausklang** (Einzeln) | Kampfende, Aufgabe oder Flucht | Fehlt. Als Geräusch vom noch offenen musikalischen Sieg-Jingle trennen; nicht bei jedem Ausgang Niederlage signalisieren. |
| 24 | P1 | **Ratsche, Metallklick, Kabelstecker, kurzer Prüfkontakt** (Einzeln) | 12 aktuell als Reparatur markierte Missionen und Rosis Technikaktionen | Fehlt. Vier unterschiedliche Werkzeuggesten sinnvoller als vier fast gleiche Pings; bei abstrakter Probe höchstens eine. |
| 25 | P2 | **Tau über Poller, Seil spannen, kleines Holzknarzen** (Einzeln) | Anlegen, Hafenarbeit, Leinenmissionen | Ankerkette vorhanden, aber keine Festmacherfamilie. Nur auslösen, wenn die Handlung feststeht. |
| 26 | P2 | **Gedämpfte Kabinentür, Klinke, Schloss** (Einzeln) | Echter Raum-/Kabinenwechsel oder explizite Handlung | Klopfen vorhanden. Kein Türsound für Inventar- oder Menü-Overlays. |
| 27 | P1 | **Kurzes Vibrationssignal, Annehmen und Auflegen** (Einzeln) | Tatsächliche Anrufereignisse | Nachrichtenvibration vorhanden. Wo passend wiederverwenden; Anrufe nicht wie jeden ungelesenen Chat behandeln. |
| 28 | P1 | **Kurzer Level-/Fähigkeit-gelernt-Akzent** (Einzeln) | Bestätigter Levelanstieg oder erfolgreiche Aktion skill_lernen | Das aktuelle Skillmenü existiert, aber der SFX-Beobachter unterscheidet diesen Fortschritt nicht. Nicht für das bloße Anwählen eines Skillknotens abspielen. |
| 29 | P2 | **Entferntes Geschirr und leises unverständliches Raumleben** (Loop) | Alvas Bar, Piazza, Abendessen an Land | Keine verständlichen Stimmen. Tags/abends unterschiedliche Dichte; nicht lauter als die Figuren. |
| 30 | P2 | **Sehr dezente Küche oder Tisch-/Geschirrkulisse** (Loop / Szene) | Kombüse und tatsächliche Essensszenen | Kochen, Brutzeln und Anstoßen vorhanden. Zuerst diese nutzen; eine längere, saubere Atmosphärenfassung nur bei Bedarf ergänzen. |

## Erste konkrete Runde

Die zwölf P0-Familien zuerst: Deck, Nacht vor Anker, Hafen, Alarm, elektrischer Knall, Feuer, Not-Aus/Relais, Angriffsschwung, Treffer, Parade, Ausweichen und Konter. Dazu die beiden falschen Story-Auslöser berichtigen. So gewinnen besonders die bislang stillen Gefahrenstellen und die spielerischen Kämpfe an Klarheit.

## Klang und Umsetzung

- **Welt:** warm, glaubwürdig, nah; Wasser, Holz, Metall und Luft. Rosis Technik darf mechanisch und charaktervoll sein, ohne jeden Tastendruck mit einem Steampunk-Geräusch zu versehen.
- **Kampf:** kurze stilisierte Anime-/RPG-Akzente mit erkennbarer Handlung. Keine schrillen Dauertöne oder langen cineastischen Bässe für jeden Treffer.
- **Beziehung:** vorhandene Signale sparsam einsetzen. Nicht jede kleine Werteänderung kommentieren; körperliche Dinge nur dann vertonen, wenn sie im sichtbaren Spielablauf tatsächlich stattfinden.
- **Laufzeiten:** Klicks/Paraden meist 0,1–0,5 s, Treffer/Schwung 0,2–1 s, Skill-Akzente etwa 0,5–2 s; längere Ladung nur solange die Phase anhält. Atmosphären etwa 30–90 s mit geprüften Loop-Schnittpunkten und langsamen Übergängen.
- **Varianten:** für häufige Einzelgeräusche vier kurze Alternativen, bei Treffern sinnvoll nach Material/Gewicht. Für Atmosphären zunächst zwei Fassungen, z. B. ruhig/belebt. Nicht jedes Mal Tempo oder Tonhöhe stark zufällig verändern.
- **Wiedergabe:** separate Gruppen für Stimme, Musik, Atmosphäre und kurze Effekte; Atmosphäre deutlich unter Dialogen. Alarm/Flinte haben eigene Pegel und kurze Grenzen. Beim Kampf keine zwei lauten Impacts für denselben Treffer.
- **Loop-Infrastruktur:** heute sind alle 39 Definitionen `schleife=false`, und `EdenSfx.play` erzeugt einmalige Audioobjekte. Für Atmosphären ist ein eigener start-/wechsel-/stoppbarer Kanal nötig. Ein 60-Sekunden-Loop darf nicht über den bestehenden Einmal-Trigger improvisiert werden.
- **Verlässliche Auslöser:** Aktionen/Ergebnisse und bestätigte Zustandswechsel verwenden. Keine automatische Geräuscherzeugung aus beliebigen LLM-Dialogwörtern. Bei Neuladen oder wiederholtem Rendern nichts doppelt abspielen.
- **Dateien und Herkunft:** Original/FLAC als Master archivieren, browserfähige Wiedergabedatei separat; technisch dekodieren, Lautheit und Spitzen abgleichen, Quelle und Nutzungsnachweis speichern. Keine Qualitätsfreigabe allein aus Dateinamen ableiten.

## Minispiele nach aktuellem Stand

Kochen ist derzeit eine Aktion mit Probe und Ergebnis, kein eigenes Timing-Minispiel. Reparaturmissionen und Karten-/Gagereignisse sind ebenfalls nicht automatisch separate interaktive Minispiele. Dafür reichen zunächst Start-/Handlungsakzent, vorhandener Würfel und ein Ergebnis. Kartenmischen, rhythmische Koch-Ticks oder Werkzeugfolgen erst anlegen, wenn eine tatsächlich sichtbare Mechanik sie auslöst. Die schon vorhandenen RPG-Kämpfe bekommen dagegen jetzt einen vollständigen Satz Rückmeldungen.

## Weitere kontextabhängige Geräusche

- Möwe und Ratte sind aktuelle Gegner: kurze natürliche Tierreaktionen können sie erkennbarer machen, aber nicht bei jedem Treffer schreien oder schrill fiepen lassen.
- Ausrüsten und Waffenwechsel: kurzer Stoff-/Metallgriff nur bei erfolgreicher Änderung; Menüfokus bleibt der vorhandene leise Klick.
- Papier, Mappe und konkrete Fundgegenstände: physisches Rascheln/Aufheben bei sichtbarer Handlung, kein Papiergeräusch bei jeder Codex-Aktualisierung.
- Drohne/Kamera und Fest-/Hafenarbeit kommen in den Missionen vor: bei einer tatsächlich inszenierten Handlung eine kurze sachliche Ergänzung. Zunächst keine eigene Dauerkulisse für jede Mission.
- Kritische Kampftreffer: kräftigere Variante der Trefferfamilie; nicht mit dem vorhandenen Würfel-Kritisch-Sound gleichsetzen.
- Leises Atemholen, Kleidung und Nähe: nur bei explizit inszenierten Momenten und mit Rücksicht auf die vorhandene Sprachausgabe; kein ständiges körperliches Geräuschbett.

## Musik bleibt separat offen

Siegesfanfare, Holm-Abschied, Salon/ruhige Story-Nachklänge, Rosis Steampunk-Alternative und die einheitliche Telefonabsenkung bleiben gemäß Musikbericht offen. Natur-/Schiffsatmosphäre kann stille Stellen tragen, ersetzt aber nicht jedes fehlende musikalische Thema. Ein physisches Kampfende und ein musikalischer Sieg-Jingle sind zwei unterschiedliche Aufgaben.

## Vollständiger Bestand

| ID | Verwendung | Dateien | Aktuell gewählte Varianten |
|---|---|---|---|
| `ui_meldung` | Allgemeine Meldung (Toast oben in der Mitte) | 4 | 3 |
| `handy_nachricht` | Neue Nachricht im Handy | 4 | 4 |
| `vorliebe_entdeckt` | Lavendel-Meldung: Vorliebe entdeckt | 4 | 3 |
| `ui_klick` | Auswahl bestätigen (Antwort, Knopf, Ort) | 10 | 2 |
| `vertrauen_plus` | Vertrauen steigt | 4 | 4 |
| `vertrauen_minus` | Vertrauen sinkt | 4 | 2 |
| `geld_ein` | Geld erhalten (Lohn, Verkauf) | 4 | 3 |
| `geld_aus` | Geld ausgeben (Kauf) | 4 | 4 |
| `item_erhalten` | Gegenstand erhalten | 4 | 1 |
| `mission_neu` | Neue Mission angenommen | 4 | 2 |
| `mission_erfolg` | Mission geschafft | 4 | 1 |
| `mission_fehlschlag` | Mission fehlgeschlagen | 4 | 3 |
| `tag_beginnt` | Neuer Tag beginnt (Morgen auf der Yacht) | 4 | 3 |
| `wuerfel_rollen` | Würfel rollt (jede Probe) | 4 | 3 |
| `wuerfel_erfolg` | Probe gelungen (normaler Erfolg) | 4 | 4 |
| `wuerfel_fehlschlag` | Probe misslungen (normaler Fehlschlag) | 4 | 3 |
| `wuerfel_kritisch` | Kritischer Erfolg (natürliche 20, Sonnenanker) | 4 | 1 |
| `wuerfel_patzer` | Patzer (natürliche 1, gebrochener Anker in Flammen) | 4 | 1 |
| `lola_brutzeln` | Lolas Kombüse: beim Kauf brutzelt es | 4 | 1 |
| `hubschrauber_holm` | Rettungshubschrauber holt Holm (Tag 2) | 4 | 3 |
| `hubschrauber_megan` | Megans Hubschrauber landet auf dem Sonnendeck (Tag 5) | 4 | 4 |
| `blackout` | Blackout: Strom fällt aus | 4 | 1 |
| `strom_zurueck` | Strom kommt zurück | 4 | 3 |
| `sturm_nacht` | Sturmnacht: Donner und Wind über der Yacht | 4 | 4 |
| `ankerkette` | Ankerkette rasselt (Anker lichten, Ankerwache) | 4 | 4 |
| `tuer_klopfen` | Jemand klopft an Ducs Kabinentür (Nachtbesuch) | 4 | 2 |
| `glaeser_anstossen` | Gläser klingen (Dinner, Festa, Toast) | 4 | 1 |
| `sektkorken` | Sektkorken knallt | 4 | 4 |
| `tender_motor` | Beiboot (Tender) startet und fährt ab | 4 | 3 |
| `wasser_platsch` | Platschen ins Wasser (Drohne, Sprung, Plattform) | 4 | 3 |
| `funk_rauschen` | Funk knackt (Bordfunk, Küstenwache) | 4 | 3 |
| `phase_wechsel` | Tageszeit wechselt (Frühstück → Tag → Abend → Nacht) | 7 | 1, 2, 3, 4, 5, 6, 7 |
| `geschenk` | Geschenk überreicht | 4 | 4 |
| `kochen` | Duc kocht selbst | 4 | 1 |
| `item_benutzen` | Snack essen / Gegenstand benutzen | 4 | 1 |
| `hinweis_gefunden` | Hinweis gefunden (neuer Codex-Eintrag) | 4 | 3 |
| `ereignis_start` | Ein Event beginnt (Event-Bildschirm geht auf) | 7 | 1, 2, 3, 5, 7 |
| `nicht_moeglich` | Geht nicht (zu wenig Geld/Energie, Aktion abgelehnt) | 4 | 2 |
| `begehren_plus` | Begehren steigt | 4 | 4 |

Prüfgrundlage: `module/eden_rise/sfx.json`, `buehne.json`, `ereignisse.json`, `kaempfe.json`, `missionen.json`, `kern/sfx.py`, `client/plugins/eden-sfx/eden-sfx.js`, `client/plugins/eden-combat/*` sowie die Einbindung in `client/index.html`. Fingerabdrücke, Zielprüfungen und maschinenlesbarer Beschaffungsplan: `soundplan.json`.

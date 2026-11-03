# Eden Rise – Musikabdeckung, Stand 24.10.2026

Abgeglichen wurden der aktuelle Wochenbogen mit **32 inszenierten Hauptszenen**, **162 Ereignisse**, **35 mögliche Personen-/Phasen-Kombinationen** aus den aktuellen Tagesabläufen und **7 Kampfdefinitionen** mit ihren Ergebnisarten. Das ist eine statische Prüfung der echten `musik.hint`-Funktion, kein kompletter Spieldurchlauf. Freie Kombinationen sind mögliche Angebote, keine Behauptung, dass sie alle in einem Durchlauf erscheinen.

Der aktuelle Story-Datenstand lautet `2026-10-24`. Die alten Dateien `docs/archiv/EDEN_MUSIC.md` und `EDEN_MUSIC_INSTALLED.md` stammen teilweise vom 18.10. und sind als alleinige Abdeckungsquelle veraltet. Prüffingerabdrücke und Detailtabellen stehen in `abdeckung.json`. Es wurden keine vertraulichen Fallinhalte oder Auflösungen in diesen Bericht übernommen.

## Was jetzt eingebaut und verbunden ist

- Alle **20 unterschiedlichen Titel der zweiten Auswahl**: 11 MP3 und 9 vom Nutzer bereitgestellte offizielle RouteNote-FLAC-Dateien, mit 23 Szenen-/Slotzuordnungen in 12 Bereichen. Vorher freigegebene andere Bereiche bleiben erhalten.
- Nachtwache mit Holm → Serene. Diese Verbindung fehlte zuvor trotz ausgewähltem Titel.
- Rosis freie Technikmomente und der Reparaturschritt → Aces High / Hep Cats. Die markierten Titel sind eingebaut; dein Wunsch nach stärkerem Steampunk bleibt als Stilauftrag offen.
- Freie Gespräche in Crew-Messe/Küche → Frühstücks-/Crew-Messe-Pool. Fest inszenierte ernste Storyszenen werden dadurch nicht pauschal überschrieben.
- Freie Nachtmomente → Comfortable Mystery 4 / Suddenly Over, soweit kein eigener Ort oder Figurenkontext Vorrang hat.
- Kabine, Nähe, Lola-Abende und Wholesome verwenden die neue Auswahl. Sophia behält ihr eigens freigegebenes Thema.
- Die 9 RouteNote-Dateien wurden vom Nutzer aus dem regulären Download bereitgestellt; ein gesondertes Lizenzzertifikat lag im angegebenen Ordner nicht bei. Quellen und Herkunft sind dokumentiert. Die Originaldateien bleiben unverändert.

## Echte Restlücken und unpassende Rückfälle

| Bereich | Aktueller Zustand | Was noch fehlt |
|---|---|---|
| Kampfsieg | Bei K. o. und Aufgabe wird der Sieg-Slot gewählt, aber es gibt keinen freigegebenen Titel: Stille. | Kurze Siegesfanfare. Flucht und Entkommen werden derzeit ebenfalls wie Niederlage behandelt; eigene neutrale Ergebnisregel wäre sinnvoll. |
| Holm-Abschied | Die Szene ist ausdrücklich stumm. | Ein freigegebener minimalistischer Abschiedstitel. |
| Einzelne neue Hauptszenen | Ankündigungs-/Nachklangmomente und der Schluss-Teaser haben noch keine eigene Regel. | Ruhige Spannung bzw. emotionaler Nachklang, gezielt auswählen. Die technische Einzelprüfung listet die betroffenen IDs unten. |
| Telefonate | Die 38 Handy-Events laufen derzeit nach Ereigniston; einzelne fest geschriebene Telefonmomente fallen auf Frühstücks- oder Deckmusik zurück. | Einheitliche Telefonregel mit Absenkung der laufenden Musik statt eines Tonwechsel-Titels. Noch nicht geändert. |
| Ernste Frühstücksszenen | Der allgemeine Frühstücksrückfall kann Crew-Alltag-Musik wählen, auch bei ernster Handlung. | Eigene ernste Zuordnung, statt fröhliche Alltagsmusik für jede Frühstücksphase. |
| Salon | Freie Tageszeit mit Chiara und freie Abende mit Siri im main_salon bleiben stumm. | Ein ruhiger Salon-/Gesprächs-Slot oder eine bewusste Entscheidung für Stille. |
| Rosi | Markierte Orgel-/Blues-Alternativen sind eingebaut. | Steampunk als neue Stilalternative, ausdrücklich auch andere Künstler. |
| Finale | Der Abschluss-Bildschirm verwendet den vorhandenen Calvi-Titel. | Deine gewünschte fröhliche italienische Finale-Variante ist noch nicht ausgewählt. Der aktuelle Akt-1-Schluss-Teaser ist ein anderer Kontext. |
| Bordrat | Alle 31 Bordrat-Events erhalten Musik nach Ton. Es gibt keinen eigenen Bordrat-Slot. | Optional ein einheitlicher ruhig-ernster Beratungscharakter; kein fehlendes Audio an sich. |

## Bewusste Stille

Cold Open, Blackout und Explosion sind weiterhin stumm; dort sollen Alarm/Geräusche tragen. Das ist kein fehlender Musiktitel. Besondere ernste/Telefon-Szenen wurden beim Import nicht blind mit allgemeiner Nachtmusik gefüllt.

## Aktuelle Hauptszenen ohne Musik

| Szenen-ID | Tag / Phase | Einordnung |
|---|---|---|
| `cold_open` | 1 / abend | bewusste Geräusch-/Alarmstelle |
| `blackout` | 1 / nacht | bewusste Geräusch-/Alarmstelle |
| `explosion` | 1 / nacht | bewusste Geräusch-/Alarmstelle |
| `holm_abschied` | 2 / fruehstueck | keine freigegebene eigene Musikregel / gezielt offen |
| `megan_ankuendigung` | 4 / abend | keine freigegebene eigene Musikregel / gezielt offen |
| `nach_dem_urteil` | 7 / abend | keine freigegebene eigene Musikregel / gezielt offen |
| `cliffhanger` | 7 / nacht | keine freigegebene eigene Musikregel / gezielt offen |

## Vorhanden, aber im aktuellen Wochenbogen kaum oder nicht erreichbar

Aktuell ohne Aufruf in den geprüften Zuständen: `dorf_gassen`, `festa`, `kampf_boss`. Das bedeutet nicht automatisch fehlende Audiodateien: etwa Festa, alte Calvi-Schlussbild-Regeln oder Bossmusik können für spätere Inhalte vorbereitet sein. In den aktuell sieben Kampfdefinitionen gibt es noch keinen über die Bosskennzeichnung ausgelösten Bosskampf.

Nicht neu markierte Bereiche wie Deck, Hafen und Alvas Bar sind **nicht automatisch Lücken**: dort bleibt die vorher übernommene Auswahl aktiv.

## Technische Prüfung

Alle neu übernommenen Dateien wurden vollständig mit ffmpeg dekodiert und auf Lautheit/Spitzen analysiert. Wiedergabe-Gain wird nur abgesenkt; die Dateien wurden nicht verändert. Alle aktiven Bibliothekspfade existieren. 10 Musik-Backendtests und der Player-Test für Shuffle, Übergänge, Sprachabsenkung und einmalige Kampf-Ergebniswiedergabe bestehen. Keine musikalische Hörprüfung oder nahtlosen Loop-Schnitte behauptet.

# Akt 3 · Durchlauf-Bot und Kalenderdichte (05.11.2026)

## Werkzeuge

- `tests/bot_akt3.py`: spielt Tag 24 bis 35 durch die echte Engine, ohne Sprachmodell, Stimme, Netz und `eden-config.json`. Baut einen Spielstand nach `akt2_ende` (vier Ausgangslagen: Yacht kaputt oder heil, Charly da oder weg, wenige oder alle Häuser abgebrannt), schaltet `akt3_spielbar` nur im Speicher an, wählt Karten, Lose und Antworten zufällig (fester Seed), liefert Baustoffe, kämpft (weicht aus, wo man nicht parieren kann). Meldet Abbrüche, Hänger, abgelehnte Aktionen, nie gesehene Akt-3-Events und die dichtesten Phasen. Laufzeit etwa 45 Sekunden je Lauf.
- `tests/dichte_akt3.py`: statische Tabelle je Tag und Phase: welche Pflicht-Szenen dort laufen *können* (Bedingungen nicht ausgewertet, Varianten derselben Szene zählen einmal).

## Ergebnis (8 Läufe, Seeds 100 bis 107)

- **Alle acht Läufe kommen bis zum Ende**, kein Absturz der Engine, kein Hänger. Enden: 3 (dreimal), 2½b (zweimal), 2½a, 0 (zweimal).
- 105 von 183 Akt-3-Events gesehen. Nie gesehen sind fast nur Szenen mit Bedingungen, die ein Zufalls-Bot nicht erfüllt (Romanzen-Leiter oben, Deal mit Alon, ★, bestimmte Flags), dazu Petrus Werkstatt-Szenen (Bot besucht keine Läden).
- **Dichte im echten Lauf:** höchstens zwei Pflicht-Szenen am Stück, außer der Festa an Tag 35 abends (drei bis vier, so gewollt: Festa, Flamenco, Ehrenbürger, rotes Kleid).

## Was der Bot gefunden hat, und was daraus wurde

| Fund | Folge | Gebaut |
|---|---|---|
| Stufen und Echos der Romanzen aus Akt 1 (z. B. Chiaras dritte Stufe) liefen an Tag 34 und am Festa-Abend, weil ihr zweites Fenster bis Tag 35 ging | Romanzen-Leiter enden in Akt 3 an Tag 33, wie die Schluss-Karten | `ereignisse_basis.bauen` |
| Bibis Handgriffe an der Station und die Schlafgranate konnten an Tag 34 (Villa) und 35 (Kommission) kommen | enden an Tag 33 | `ereignisse_bibi.ARBEIT`, `ereignisse_mochis` |
| Megans Schluss-Karte endet an Tag 30, Holms Warnung kommt erst an Tag 31 | Megan warnt selbst: `a3_megan_tuer`, Tag 29 Nacht | `ereignisse_akt3_romanzen.py` |
| Bot hing in Kämpfen gegen Roboter (Schläge nur ausweichbar) | nur ein Fehler im Testlauf, das Spiel selbst ist richtig | `bot_akt3.py` |

## Bekannt, nicht geändert

- **Bibis letzte Stufe** (`rm_b4`, „Last Page“) liegt mit Absicht auf Tag 35 abends, nach der Freilassung der Tiere. Sie kommt damit am Festa-Abend dazu. Duc entscheiden lassen, ob sie vor die Festa gehört (sie läuft in Listenreihenfolge).
- `mo_halsbaender` darf bis Tag 34 kommen (Beweis für die Kommission an Tag 35). Am Villa-Tag kann sie damit neben dem Keller stehen.

## Lokal

`python tests/bot_akt3.py` auch lokal laufen lassen: dort mit echten Figurenkarten und Sprites. Mit `--json bericht.json` steht jeder Lauf mit allen Events im Detail in der Datei.

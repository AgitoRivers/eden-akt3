# Pause-Menü: Map, Inventory, Character, Relationships, Codex, Menu

> Kanon-Stand 26.10.2026 · Besitz: Items (Menü-Umbau, Duc 25.10.) · Quelle: `client/plugins/eden-menu/eden-menu.js` und `.css`, Einhängepunkte in `client/index.html` (`ebene()`, `dock()`, Tasten) · Spiel ist PC-only

## Kurz
Das Dock hat acht Knöpfe, jeder beantwortet genau eine Frage. Alles außer Phone ist ein **gemeinsames Vollbild-Menü** mit
Reiterleiste oben (Q/E blättern) auf abgedunkelter, unscharfer Szene. Alle Texte sind Englisch (STIL.md).

| Knopf | Taste | Frage | Inhalt |
|---|---|---|---|
| Phone | H | Wer schreibt mir? | eigenes Fenster (Gerät in der Hand), unverändert |
| **Map** | M (auch L) | Wohin gehe ich? | große Ort-Kacheln: „On board“, darunter „Cala d'Orsu · by tender“ |
| **Inventory** | I | Was trage ich? | Waffen und Jacken (anlegen), Tasche, Besorgungen, Andenken |
| **Character** | C | Wer bin ich? | Porträt, Level, Attribute, Fähigkeiten, Geheimnis |
| **Relationships** | B | Wen kenne ich? | Frauen als Porträtkarten, Crew und Dorf, Spannungen, Uhren |
| **Journal** | N | Was soll ich tun? | oben die **Aufträge** (Porträt der Auftraggeberin, nächster Schritt, Ort, Schritte, „Your call“, Belohnung), daneben die Rubrik **Favours** (was dich schon gebeten hat, mit Ausgang und Dank-Foto); die Aufträge sind in Main orders, Side orders und Done getrennt. Der Reiter „Jobs“ am Handy ist weg (Schnelljobs abgeschaltet, 29.10.2026) |
| **Codex** | J | Was weiß ich? | Investigation, Discoveries, Chronicle |
| **Menu** | Esc | Einstellungen | Sound, Game, This scene, Studio, Keys, Run |

Q/E wechselt zwischen Inventory, Character, Relationships, Journal und Codex. Die Map und das Menu haben keine Reiter.

## Hinweispunkte am Dock
Ein goldener, pulsierender Punkt zeigt nur, dass es dort **etwas zu tun** gibt (Brain Trust 26.10.). Er verschwindet, sobald der
Reiter einmal offen war.
- **Character:** Es gibt Skillpunkte zu verteilen (neuer Punkt bei jeder neuen Anzahl).
- **Journal:** Ein aktiver Auftrag hat einen neuen nächsten Schritt oder ein neuer Auftrag ist da.
- **Inventory:** Ein Stück ist neu (Tasche, Waffe oder Jacke), das beim letzten Öffnen noch nicht da war. Verbrauchen löst keinen Punkt aus.
- Beim allerersten Start zählt nur ein offener Skillpunkt. Gespeichert wird pro Durchlauf im Browser (`localStorage`, Schlüssel
  `eden_gesehen_<Durchlauf-ID>`). Andere Reiter (Relationships, Codex, Map) bekommen bewusst keinen Punkt.

## Map
- **On board:** Totò's Locker, Rosi's Workshop, Eden Shop (Megan), Lola's Galley. **Cala d'Orsu · by tender:** Alva's Bar.
- Jede Kachel zeigt den Ort als Hintergrund, die Person davor, Namen, Ortsname und die Möglichkeiten als Chips (Buy, Sell,
  Eat & cook, Chips, Upgrade). Ein Klick betritt den Ort wie bisher (Buy/Sell, Esc = Goodbye).
- Seit 03.11.2026 (UX-Paket): Kacheln groß (zwei Reihen füllen den Bildschirm), „NEW“ an Orten mit neuer Ware oder einer anderen
  Person seit dem letzten Besuch. Im Ort stehen die Antworten direkt unter der Sprechblase. Muster: `ui_stil.md` Abschnitt 2c.
- Kachel grau und gesperrt mit „The tender only runs on days you went ashore.“, wenn der Ort heute zu ist (Regel unverändert
  aus `ortOffen`). Orts-Namen und -Texte stehen englisch in `werkzeuge/eden_rise/laeden_eden_rise.py` (Totò im Modul-Skript).

## Inventory
- **Links:** Waffen und Jacken als Karten (Bild, Schaden bzw. Schutz, Element, Rosi-Stufe, Chip-Rauten; Chips nur zur Ansicht).
  Klick legt an. Die getragene Karte hat den goldenen Rahmen und „Equipped“.
- **Vergleich:** Jede andere Karte zeigt, was sich gegenüber dem Getragenen ändert: `+2 damage` grün, `−1 protection` rot,
  „Fire instead of none“ beim Element, bei Jacken die andere Eigenschaft. Nach dem Anlegen steht in der Mitte kurz
  „<Stück> equipped“ (2,6 s).
- **Mitte:** das Porträt der angelegten Kombination, darunter Waffe, Jacke und ihre Eigenschaftstexte.
- **Rechts:** Tasche (6 Plätze, Produktfotos), Besorgungen (Teile für Aufträge, getrennt), Andenken (zählen nicht zu den
  Plätzen). Ein Klick auf ein Item zeigt Text sowie Use und Give.
- **Regel:** Anlegen geht nur, wenn Duc frei ist (Tageswahl oder Kabine), nie in einer Szene oder im Kampf (Engine, Aktion
  `ausruesten`). „Umziehen“ in der Kabine öffnet dieses Inventar. Rosis Werkstatt hat nur noch Chips und Upgrade.

## Character
- **Porträt:** Frontansicht, ganzer Körper, Achterdeck in der Sonne, immer grinsend oder lachend. Es gibt ein Bild je
  **Jacke × Waffenart** (5 Jacken × 5 Waffen, dazu Terra Scura mit dem Schrubber). Der Schläger liegt auf der Schulter,
  die anderen Waffen haben je eine eigene Pose (Duc 25.10.).
- **Dateien:** Rohbilder `docs/abnahme/charakter/Duc<Look><Waffe>_v1|2.png` (nicht in Git), gewählte Bilder
  `module/eden_rise/charakter/Duc<Look><Waffe>.webp`, ausgeliefert unter `/charakterbild/<Name>`. Erzeugen und Wählen:
  `werkzeuge/charakter_bild.py` (`alle`, `alle Bat`, `--waehle <Name> <Variante>`). Fehlt ein Bild, bleibt der Rahmen leer.
- **Links:** Level-Ring, Erfahrung, Leben, Ausdauer, sechs Attribute. **Rechts:** die vier Fähigkeitspfade mit Punkten,
  „Open skill tree“ (voller Baum, siehe `faehigkeiten_ui.md`), Geheimnis als Notizzettel, Chat-Profilbild ändern.

## Relationships und Codex
- **Relationships:** Die Frauen sind hohe Karten vor ihrem Lieblingsort mit Trust und Desire (seit 03.11.2026 als zwei Ringe mit Stufenwort, `ui_stil.md` 2c). Ein Klick öffnet das Profil. Crew
  und Dorf als schmale Karten. Rechts Spannungen zwischen den Frauen und die Uhren.
- **Codex:** Investigation, Discoveries, Chronicle (nach Tagen, mit „Known to …“).
- **Investigation** ist Ducs Notizbuch: oben „The case“ mit den Fragen (nummerierte Kreise, gold = „Proven“) und dem Hinweis,
  wenn die Kette hält. Dann „Possible now · no scene needed“ (Aktionen mit Kosten und Sperre, 💬 = jemand hat dich
  hingeschickt), „What you know · by time“ (Fakten nach Uhrzeit mit Verlässlichkeit: secured, solid, seen yourself, only a
  statement, rumour), „The times don't add up“ (Widersprüche, rot) und Gerüchte. Die Texte kommen englisch aus `kern/ermittlung.py`.

## Menu (Esc)
Zwei Spalten: Sound (Musik, Effekte, Voice, Sprechtempo), Game (Conversation, Kampfoptionen, Kampf-Wiki), This scene
(Antworten neu schreiben, Szene beenden oder neu starten), Studio (Stimmen zuordnen, Porträt-Ausschnitte), Keys, Run
(neuer Durchlauf). Profilbild und „Schiff & Vorräte“ stehen nicht mehr hier: Das Bild liegt bei Character, die Werte erklären die Status-Knöpfe der Kopfzeile (`systeme/ui_stil.md`).

## Technik
- `index.html` reicht die Overlays `inventory`, `character`, `bez`, `codex`, `laden` (= Map) und `menue` an `EdenMenu.html(z, overlay)`
  weiter. Der Server liefert das Plugin unter `/plugins/eden-menu/` (Route in `eden.py`).
- Die alten Menü-Zweige in `ebene()` sind entfernt (26.10.). `tests/test_skills_ui.cjs` prüft Skillbaum und Inventar jetzt im Plugin.
- Offen: ein Codex-Fakt in den Story-Daten ist noch Deutsch („Leas Routenplan …“, Story-Bereich); Tastatur-Navigation im Menü.

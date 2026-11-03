# Eden-Engine

Eine Engine für mehrere Szenarien. Die Engine kennt keine Figuren: Was eine Figur oder einen Laden besonders macht, steht in den Daten des Moduls.

## Ordner

| Ordner | Inhalt |
|---|---|
| `eden.py`, `kern/`, `client/` | Engine: Server (Port 8308), Regeln, Oberfläche. Keine Figurennamen. |
| `module/<modul>/` | Alle Daten eines Szenarios, gebaut von seinen Buildern. Nie von Hand ändern. |
| `werkzeuge/` | Gemeinsame Werkzeuge: `item_bilder.py`, `hintergrund_bild.py` |
| `werkzeuge/<modul>/` | Builder eines Szenarios, z. B. `werkzeuge/eden_rise/` |
| `tests/` | Fester Testlauf und Vorschau-Server |
| `archiv/` | Was nicht mehr gespielt wird (zurzeit Gestrandet). Die Engine liest nichts von hier. |

## Ein Modul an die Engine hängen

- **Pflicht:** `modul.json` mit Personen, Räumen, Werten, Zeitraster und Personas.
- **Optional:**
  - `story.json` für eine Hauptstory mit Wochenbogen, Ermittlung und Ende
  - `ereignisse.json`, `missionen.json`, `laeden.json`
  - `szenen.json` für einen Szenen-Vorrat ohne Hauptstory
- **Sonderrollen** stehen in `modul.json` unter `rollen`, `migration`, `ermittlung` sowie in Personen- und Laden-Feldern, zum Beispiel ein Händler mit Draht, ein Dorfohr oder Tratsch.
  - Das Schema steht in `kern/rollen.py`.
  - Fehlt ein Eintrag, gibt es die Regel im Modul einfach nicht.
- **Aktives Modul:** In `eden-config.json` → `"modul"` (nicht im Git).

## Prüfen nach jeder Änderung am Kern

```
python tests\lauf_test.py              # Woche automatisch durchspielen, Endzustand gegen Referenz
python tests\lauf_test.py --seed 3
python tests\spieltest.py              # nur vor Meilensteinen: ganzes Spiel als 6 Spielertypen, Bericht mit Ampel (docs/wiki/systeme/spieltest.md)
python werkzeuge\eden_rise\story_pruefen.py
python tests\test_missionen.py         # Missionsregeln mit festen Würfeln (Fehlschlag, Wege, Abgabe, Werkzeug)
python tests\test_versprechen.py
python tests\test_ortswahl.py
python tests\test_handy.py             # Handy-Chat: Treiber, Ton-Folgen, Chips, Rückbezug, Prüfer, kostet nie eine Aktion
python tests\geld_messung.py           # Kontostand je Tag für zwei Spielstile (nur Zahlen)
python tests\test_kampf.py             # Kampfregeln mit festen Würfeln (Enden, Revision, Neuladen, Parade)
python tests\test_kampf_server.py      # Kampf über die Engine-Aktionen (Status kampf, Parade, Rückkehr)
```

**Kampf:** rundenbasierter Solo-Kampf in `kern/kampf.py`, Daten aus `module/<modul>/kaempfe.json` (Builder
`werkzeuge/eden_rise/kaempfe_eden_rise.py`). Bildschirm mit Parade als Status `kampf` (Etappe 3), im Wochenbogen noch kein Kampf; zum Ausprobieren `python tests\vorschau_server.py --port 8332 --kampf hafen_dieb_test` oder `Kampf_Test.bat`
(Testkampf im Terminal, kein Spielstand). Regeln: [docs/EDEN_KAMPF.md](docs/EDEN_KAMPF.md).

**Was der Testlauf macht:**
- Er läuft ohne Sprachmodell, Stimme und Netz, mit festen Würfeln.
- Weicht etwas ab, zeigt er nur die Stelle, nie Werte, denn der Zustand enthält Fall-Auflösungen.
- Nach einer gewollten Regeländerung schreibt `--speichern` die Referenz neu.

**Oberfläche ansehen:**
- `python tests\vorschau_server.py` startet die Engine auf Port 8328.
- Spielstände und Konfiguration sind Wegwerf-Kopien.
- Mit `--tag 3 --inventar multitool --angebot petru_motor_1,alva_kuehlung_reparatur` spult ein Bot bis Tag 3 vor und legt Gegenstände und das Tagesangebot fest. So lassen sich bestimmte Missionen direkt ansehen.

## Handy-Chat

Ein durchgehender Chat pro Frau (`kern/handy.py`). Der Code entscheidet und bucht, das Modell schreibt und sortiert nur ein.
- **Sie schreibt**, wenn seit ihrem letzten Text mindestens `min_progress` (4) Punkte Vertrauen/Begehren dazugekommen sind. Ohne Fortschritt kommt nichts, mit viel Fortschritt viel. Keine Tagesgrenze für eingehende Texte.
- **Duc antwortet** mit drei Chips (warm, witzig, flirty; Etikett mit Wirkung und Risiko) oder frei. Das Modell sortiert den Ton ein, der Code entscheidet: einmal pro Frau und Tag eine Wirkung, Gespräch trägt nur bis Stufe 3, Tag 1 nur Positives, ein Flirt bei Vertrauen unter 2 kostet Vertrauen. Höchstens 3 Antworten je Frau und Tag, danach „schläft / ist auf Wache".
- **Gedächtnis:** jeder Austausch steht in ihrer Chronik (nur sie weiß davon). Der nächste Szenenstart greift Ducs beste Zeile der letzten 24 Stunden auf (💬 in „Zuletzt").
- **Prüfer:** jeder Text von ihr wird einmal gegen ihre Fakten geprüft (kein erfundenes Ereignis), ein Neuschreiben.
- **Kostet nie eine Phase oder Aktion** (Modell B).
- **Zahlen** in `module/<modul>/handy.json` (Builder `werkzeuge/eden_rise/handy_eden_rise.py`), Fallback `DEFAULTS` im Code. Test: `tests\test_handy.py`.

## Würfel-Anzeige

Das Client-Plugin unter `client/plugins/eden-dice/` zeigt sichtbare Proben kompakt animiert und besondere oder kritische Würfe groß. Regeln und Spielstände bleiben unverändert. Die Auslöser eines Szenarios stehen optional in `module/<modul>/wuerfel_anzeige.json`.

Integration, API, Assets und Tests: [docs/EDEN_DICE.md](docs/EDEN_DICE.md).

## Kampf-Wiki

Das Kampfsystem nach Themen geordnet: `client/wiki/kampf.html`, im Spiel unter **Menü → Kampf-Wiki** (Route `/wiki/kampf`, öffnet in einem neuen Tab). Quelle ist `docs/EDEN_KAMPF.md`. Das Wiki ist eine geordnete Zusammenfassung und wird bei Regeländerungen von Hand nachgezogen.

## Offen

- **`kern/abschluss.py`** enthält noch die Endtexte von Eden Rise. Sie gehören in die Story-Daten.
- **`kern/showrunner.py`** trägt Reste des alten Szenen-Vorrats, zum Beispiel die Feuer-Nacht von Gestrandet.
- **Eden Consulting** läuft noch auf einer eigenen Engine-Kopie (`X:\AI\Eden-Consulting-Vorschau`) und soll auf diese Engine umziehen.

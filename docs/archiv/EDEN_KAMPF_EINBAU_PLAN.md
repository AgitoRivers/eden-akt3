# Kampf-Einbau – Plan (Stand 22.10.2026, von Duc abgesegnet, Start später)

Ausgangslage: Die Engine (`kern/kampf.py`, Etappe 3) kann Befehle, Parade, die alten 7 Fähigkeiten und die Zustände
offen/Finte/geschwächt. Spielbar ist nur der Dieb (`module/eden_rise/kaempfe.json`). Die Regeln vom 19.–21.10. stehen
nur in [kampf.md](../wiki/systeme/kampf.md) („Beschlossen …“, „Gesamt-Balancing“). Bilder: alle 51 Gegner mit Posen in
`module/eden_rise/kampf/<Sprite>/` (einheitliche Größe seit Commit eb23694, inkl. death bei Tieren), Ziege/Capra in
`module/eden_rise/figuren/ziege/`.

## Etappe A – alle 51 Gegner spielbar (heutige Regeln)

- Alle Gegner in `werkzeuge/eden_rise/kaempfe_eden_rise.py`: Werte aus der Level-Tabelle (LP, Angriff, Schutz je
  Level), Tempo nach Bedrohungsstufe, Muster Schlag/Schlag/schwerer Schlag, `flucht_ab`, Schwäche/Unempfindlich nach
  Klasse (Tiere: Reden gesperrt; Unit-01: Einschüchtern gesperrt), Sprite.
- Je Gegner eine Testbegegnung (`test: True`), spielbar über `tests\vorschau_server.py --kampf <id>`.
- `death` in die Engine (`kern/kampf.py` POSEN) und den Bildschirm: Tiere zeigen beim K.o. death, Menschen defeated.
- `docs/archiv/kampf_gegner_bereit.md` nachziehen (Wolf, Panther, Grizzly + Alphas fehlen).
- `tests/test_kampf.py` bleibt grün, neuer Test kämpft jeden der 51 Gegner einmal durch.

## Etappe B – neue Regeln, kleine Schritte mit Tests

1. Level, Erfahrung, Bedrohungsfarbe; deutsche Attributnamen; „erschöpft“ statt „offen“, „ungedeckt“ für Duc
2. 4 Fähigkeiten statt 7, kritische Treffer über List, Fliehen als Mut-Probe nach Stufe
3. Element-Zustände (brennend, nass, erschüttert, Strom, blutend, geblendet, betäubt) + 5 Reaktionen
4. Spezialangriffe der Gegner (Lästig 1, Gefährlich 2, Tödlich 3, Albtraum 4)
5. Waffen, Rüstung, Anhänger mit Slots; Waffenart × Gegnerklasse; Element-Multiplikatoren
6. Pfade (Kämpfer/Schmuggler/Schütze) mit Spezialangriffen ab Lv 3/5/7/9 und Skillpunkten
7. Bildschirm: Anzeige der neuen Zustände, anders farbiges QTE für „nur ausweichen“

## Etappe C – Begegnungen in Story und Orten

Zusammen mit dem Erkundungs-System (`kern/expedition.py`, `orte.json`, siehe tage_erkundung.md, orte.md).

## Achtung

`eden.py`, `client/index.html` haben uncommittete Änderungen anderer Sitzungen (Musik) – für Etappe A voraussichtlich
nicht nötig; falls doch, nur eigene Stellen ändern und committen.

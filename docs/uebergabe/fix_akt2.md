# Übergabe fix-akt2 (Cloud-Sitzung, 04.11.2026)

Branch `fix-akt2`, abgezweigt von `master` (`bdb05cc`). Vier Fehler, je ein Commit mit eigenem Test. Kein Push auf `master`.
Nicht angefasst: `taktik.json`, Gegnerwerte, Favours- und Handy-Dateien, Bilder, Ton, `eden-config.json`.

**Vorab:** Die drei genannten Berichte (`docs/berichte/wiki_vs_code.md`, `docs/wiki/welt/akt3_folgen_belagerung.md`,
`docs/uebergabe/balancing_bericht.md`) gibt es in diesem Auszug nicht, auch nicht auf `master`. Ich habe die Fehler direkt
im Code gesucht und die Wirkpunkte für (3) aus dem Wiki abgeleitet (`systeme/taktik.md`, `welt/belagerung.md`,
`welt/drehbuch_finale.md`). Bitte mit deinem Bericht abgleichen, vor allem bei Alva und Don.

## Commits

| # | Commit | Was | Test |
|---|---|---|---|
| 1 | `6200604` | **Inventar zeigt die echte Taschengröße.** `handel.ansicht` liefert `plaetze` (`zustand.inventar_plaetze`: 8 / 12 / 16), `eden-menu.js` zeigt `belegt/plaetze` und füllt leere Slots bis dahin. Vorher fest `/6`. Fallback 6 nur für alte Stände ohne das Feld | `tests/test_inventar_plaetze.py` |
| 2 | `823110d` | **Auffangstation-Fenster.** `mo_schlafgranate` jetzt Tag 11–35 (gleich `TAGE` der Spuren), `mo_halsbaender` Tag 11–34, damit `mo_ark_beweis` vor `mo_kommission` an Tag 35 steht | `tests/test_mochis_fenster.py` |
| 3 | `e071e75` | **Drei Belagerungs-Wahlen wirken** (Einzelheiten unten) | `tests/test_belagerung_wahlen.py` |
| 4 | `56b152e` | **Akt 3 beginnt an Tag 24** (E-114): `AKT3_AB = 24`, Sperre endet, Kalender im Wiki angeglichen | `tests/test_akt3_beginn.py` |

## (3) Die drei Wahlen

- **Türen mit Petru** (`bl_tueren_petru`): `kern/taktik._rudert` zieht einen Punkt von der Ruf-Schwelle ab, wie es
  `systeme/taktik.md` schon beschrieb. Ruf 5 → 4, mit heiler Werkstatt (Petrus Ruder) → 3. Lola und Mina ändern nichts.
  `ruf_rudert` in `taktik.json` bleibt 5.
- **Alvas Runde** (`bl_alva_runde`): In `bl_bar` (Tag 22 Abend) zwei Fassungen von Alvas erster Zeile (Gruppe `runde`):
  mit Versprechen erinnert sie daran (*“Last night, on the quay, I wrote it on my board.”*), ohne gibt sie die Runde aus
  (*“This round is on the house. Don't get used to it.”*, aus `drehbuch_finale.md`). Mit Versprechen folgt der neue Takt
  `bl_bar_rechnung`: Alva legt die Rechnung hin, Duc zahlt **60 €**, Vertrauen Alva **+4**. **Vorschlag**, in
  `ENTSCHEIDUNGEN.md` als offen eingetragen.
- **Dons Kirchen-Wahl** (`bl_kirche_don`, nur ab Vertrauen 3 erreichbar): Die Kirche hat in Welle 6 ein Leben mehr
  (`_welle_start`, einmal je Welle, auch beim Neustart nicht doppelt). Grund: Das vierte Leben aus Vertrauen 3 gilt schon
  ab Tag 21, die Wahl an Tag 23 brachte also nichts. Jetzt stehen Jana (erster Schlag zählt nicht) und Don gleich stark
  gegeneinander. **Vorschlag**, offen in `ENTSCHEIDUNGEN.md`.

## (4) Akt 3 ab Tag 24

- `ereignisse_basis.AKT3_AB = 24`, `AKT3 = [24, 35]`. Outfit-Quest, Schneider, späte Romanzen-Leiter und Zitronengras
  nutzen es: 34 Events, vorher `wann.akt2 = [22, 35]`.
- `modul.sperre.bis_tag = 24`, `kern/ereignisse.gesperrt_durch_story` gibt ab dann wieder alles frei. Vorher hatte die
  Sperre kein Ende: Ab Tag 21 Nachmittag liefen für immer nur `bl_`-Events, alle Akt-3-Fenster (auch die aus (2) und die
  Selfies, Abende und Funken bis Tag 35) waren tot.
- Rosi's Expedition Pack (16 Plätze) und Stahl aus Maschinen ab Tag 24 statt 22 (passt zu *“won't finish before the siege is over”*).
- Wiki: `akt2_kalender.md` (Zeile Tag 24), `systeme/interaktion.md`, `kochen.md`, `beute.md`, `welt/dorf_figuren.md`.
- **Nicht geändert:** `zeitraster.tage = 23`. Das Spiel endet weiter nach Tag 23 (Beta-Schluss mit `akt2_ende`). Auf 35
  stellen, sobald Akt 3 gebaut ist.

## Tests

Neu und grün: `test_inventar_plaetze`, `test_mochis_fenster`, `test_belagerung_wahlen`, `test_akt3_beginn`.

Angepasst, weil sie den alten Akt-3-Beginn festschrieben: `test_outfit_quest` (Fenster `[24, 35]`), `test_geld` (16er-Tasche
an Tag 23 gesperrt, an Tag 24 kaufbar). Beide grün.

Weiter grün: `test_akt2_events`, `test_sprite_stimmung`, `test_cliffhanger`, `test_kuechen`, `test_stapel`,
`test_danzel_laden`, `test_journal_nebenquests`. `test_taktik` einzeln je Funktion: 54 grün, vorher wie nachher.

**Lokal nicht prüfbar** (fehlende Bilder, Ton, `figuren` oder `eden-config.json`, nicht geändert):
`test_taktik.test_flinke_roboter` und `test_figuren` (Sprites), `test_mochis` (Selfie-Bilder), `test_sfx` (Ton und Config),
`test_ereignis_stufen`, `test_dorf_figuren`, `test_ortswahl`, `test_freie_zeit`, `test_hafen` (Config).
**Vergleich aller `test_*.py`, master gegen `fix-akt2`** (`PYTHONHASHSEED=0`): master 43 grün, `fix-akt2` 47 grün
(die 43 von master und die vier neuen), 56 rot. **Kein Test hat seinen Status geändert.** Alle 56 roten scheitern
auf master genauso, an fehlenden Bildern, Ton, Sprites oder `eden-config.json` (lokal nicht prüfbar).

## Lokal mit Gate prüfen

1. **Neubau der Daten.** Hier ändert ein voller Neubau Bildnamen (Fallbacks, weil die Bilder fehlen). Ich habe deshalb nur
   die betroffenen Events in `ereignisse.json` übernommen und `modul.json` (`sperre.bis_tag`, Taschenstufe 16) sowie
   `kuechen.json` (`stahl_kampf.ab_tag`) von Hand gesetzt. `modul_eden_rise.py` erzeugt dieselben Werte (geprüft),
   `kochen_eden_rise.py` bricht hier an fehlenden Köder-Bildern ab. Bitte lokal laufen lassen und prüfen, dass der
   Git-Diff danach leer ist:
   `python werkzeuge/eden_rise/ereignisse_basis.py`, `python werkzeuge/eden_rise/modul_eden_rise.py`,
   `python werkzeuge/eden_rise/kochen_eden_rise.py`.
2. **Inventar im Client:** Menü öffnen, Tasche zeigt `x/8`, nach Rosis Upgrades `x/12` und `x/16`, leere Slots passen.
3. **Belagerung im Kalender:** Petru an die Türen schicken, mit Ruf 4 rudert das Dorf in Welle 4. Don in die Kirche
   (Vertrauen 3): Kirchen-Anzeige in Welle 6 zeigt ein Leben mehr. Alva versprechen (Tag 21 Abend, Kai), dann an Tag 22
   die Bar: Rechnung, 60 € in den Buchungen.
4. **Ganze Tests mit Bildern und Config:** `test_taktik`, `test_mochis`, `test_sfx`, `test_ereignis_stufen`,
   `test_dorf_figuren`, `test_ortswahl`, `test_freie_zeit`, `test_hafen`, dazu die Bots mit `PYTHONHASHSEED=0`
   (`spieltest_kalender.py`), weil Petru und Don die Belagerung leichter machen können.

## Wartet auf Ducs Urteil

- Alvas Rechnung: 60 € und Vertrauen +4 sind erste Zahlen. Die neuen Zeilen sind nicht vertont (die `bl_`-Zeilen in
  `ereignisse_belagerung.py` haben keine Stimm-Tags). Verspricht Duc die Runde erst am Abend von Tag 22 (nach der Bar),
  bleibt das Versprechen offen: ein möglicher Anschluss für Akt 3.
- Dons Extra-Leben in Welle 6: Stärke gegen Jana prüfen.
- `zeitraster.tage` auf 35, sobald Akt 3 steht.

## Bekannte Fallen

- `__pycache__` ist nicht in `.gitignore`. Beim Testen entstehen die Ordner neu; nicht mit committen.
- In `ereignisse_basis.py` heißt die Konstante `AKT3` jetzt global (über `from ereignisse_basis import *`). Die lokalen
  Kopien in `ereignisse_outfit_quest.py` und `ereignisse_schneider.py` sind entfernt.

Keine Bestellungen für Bilder oder Ton. `bl_bar_rechnung` nutzt `alvas_bar` und Alvas vorhandenes Set.

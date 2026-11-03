# Holms Schießwette um Gemelli

> Stand 30.10.2026 · Szenen, Engine und Client-Minispiel im Plugin `eden-schiessen` gebaut.

## Ablauf

Vorläufig **Tag 18** (Konstante `TAG` in `ereignisse_holm.py`), bis Woche 3 steht.

| Phase | Event | Was passiert | Flag |
|---|---|---|---|
| Nachmittag | `hb_zurueck` | Holm kommt zurück, zählt die Crew und dankt | `holm_zurueck` |
| Abend | `hb_megan` | Was Megan erzählt hat, je ein Satz zu Macchia, Bergen und Grotte. Sie will auf den Kai und kommt mit dem Koffer nicht weit | `holm_koffer` |
| Nacht | `hb_koffer` | Sie verleiht das Erbstück dem besten Schützen. Duc muss drei Gegner schlagen | `holm_wette_offen` |
| danach | `hb_sieg` | Übergabe nach dem Sieg über Wolff. Holm trifft dabei die letzte Flasche, trotz Naht | `waffe_gun`, `holm_wette_gewonnen` |

## Holms drei Sätze

Eine Event-Zeile darf `gruppe` und `wenn` tragen. Je Gruppe gilt die erste passende Zeile (`ereignisse.zeilen_aktiv`). Der
Index bleibt der Stimm-Schlüssel, also werden alle Fassungen vertont.

- **Macchia:** `kloster_frederico_tot`, `kloster_frederico_lebt`, sonst offen.
- **Berge:** `bg_adrien_bergerie` (Weg C), `bg_weg_b` mit und ohne `petru_versoehnt`, `bg_adrien_verhaftet` (Weg A), sonst offen.
- **Grotte:** `gr_bastien_tot`, `gr_gennaro_haende`, `grotte_fertig`, ersatzweise `red_trio_fertig`, sonst offen.

## Regeln der Wette (`kern/schiessen.py`)

- **Gegner nacheinander:** Adrien (nur auf Weg C, Flag `bg_adrien_bergerie`), sonst Rosi. Dann Elsa, dann Wolff. Wer Wolff schlägt, trägt Gemelli.
- **Drei Runden, die Summe entscheidet.** Gleichstand ist kein Sieg. Jeder Treffer zählt 1, oben stehen beide Avatare mit den Treffern je Runde.
- **Vor jeder Runde 5 Sekunden Pause.** Dort stehen der Wind und die Trefferzahl des Gegners. Nachgeladen wird von Hand (R).
- **10 Patronen, 2 Sekunden Nachladen.** Jede Runde bringt 13 Ziele, die nach etwa 3 Sekunden weg sind. Wer mitten in der Runde nachlädt, verliert Ziele. Die Anzeige zeigt, wie viele Fehlschüsse noch frei sind.
- **Regeln kommen nacheinander:** Adrien oder Rosi ohne Wind und ohne Granate, ab Elsa beides. So lernt man erst Zielen und Nachladen.
- **Serien:** Ab 3 Treffern in Folge zeigt das Spiel die Serie, alle 5 Treffer mit Klang und Funken. Eine Serie gibt keine Punkte. Ein Fehlschuss oder eine Möwe beendet sie, die Pause nicht.
- **Avatar des Gegners:** Sein Gesicht folgt dem Stand (freut sich bei Führung, ist genervt bei Rückstand, erschrickt bei der Blendung).
- **Ziele je Runde:** Runde 1 Flaschen, Runde 2 Flaschen und Tontauben, Runde 3 Tontauben und Drohnen.
- **Möwe:** kostet 1 Treffer. Runde 1 und 2 je eine, Runde 3 zwei.
- **Blendgranaten-Möwe:** ab Elsa in Runde 2 und 3 je eine. Sie trägt eine gestohlene Blendgranate mit kleiner Trefferzone. Trifft Duc nur die Granate, setzt der Gegner 5 Sekunden aus. Trifft er die Möwe, kostet das 1 Treffer.
- Kostet keine Zeit. Eine Niederlage kostet nichts. Je 3 Niederlagen gegen denselben Gegner trifft dieser still je Runde einen weniger, höchstens 4 weniger (nicht Holm). Die Waffe darf bei der Belagerung nicht fehlen.
- **Relaxed:** 2 Sekunden mehr je Runde, wo es Wind gibt, auch kein Wind. Gegen Holm nicht wählbar.
- Wahrnehmung vergrößert die Trefferzone etwas. Der Client meldet die Treffer, die Engine deckelt sie.

| Gegner | Treffer Runde 1/2/3 | Sekunden je Runde | Mittlerer Spieler (Simulation) |
|---|---|---|---|
| Adrien oder Rosi | 5 / 6 / 7 | 10 | 100 % |
| Elsa | 6 / 7 / 8 | 10 | 86 % |
| Wolff | 8 / 9 / 10 | 10 | 30 % |
| Holm (ab Tag 22) | 8 / 9 / 10 | 9,5 | 26 % |

Fehlerfreies Zielen schafft etwa 30 Treffer, Magazin und Zielrate deckeln das. Die Prozente kommen aus einem angenommenen Spielermodell, nicht aus echten Runden, und liegen vermutlich zu hoch (Ducs erstes Spiel: 10 Treffer mit Relaxed). Die Werte stehen in `GEGNER` in `kern/schiessen.py`.

## Holm-Challenge in Akt 3

Ab Tag 22 ist Holm die vierte Gegnerin. Jede gewonnene Runde gibt einmalig ein Geschenk, auch wenn Duc das Spiel insgesamt verliert: Runde 1 Stahlplatte, Runde 2 Aquamarin (Riposte Stufe 1), Runde 3 Kupfer (Gemelli Stufe 1). Sind alle drei vergeben, ist die Challenge zu.

## Wolff und Adrien

Auf Weg C hat Wolff Adrien als gefallen gemeldet. In `hb_g_wolff` neckt er ihn: der Mann an der Reling sehe aus wie ein toter Caporal. Adrien spielt mit und dankt ihm indirekt („I'll buy him a drink“). Ohne Weg C begrüßt Wolff Duc je nach Weg anders (`bg_legion_npc_zu`, `bg_adrien_verhaftet`, sonst neutral).

## Entschieden (Duc 30.10.2026)

- **Gemelli bleibt bis zum Ende des Spiels bei Duc,** auch in Akt 3. Duc gibt sie Holm erst **im Epilog** zurück. Das
  löst ihr „Bring it back“ ein. Die Szene ist noch nicht gebaut.
- **Bei der Belagerung übernimmt Holm die Kommandobrücke und gibt Befehle** ([`belagerung.md`](../welt/belagerung.md)).

## Client-Minispiel „Holm’s Bet“

Desktop-Overlay auf dem Vorderdeck; das Tagesbild wird zur Abenddämmerung abgedunkelt. Einstieg über den runden
Knopf neben Cabin bzw. **G**, sobald die Engine die offene Wette meldet. Kurze Regeln vor jeder Sitzung.

- 45 Sekunden; mehr als Holms 40 Punkte gewinnt. Gleichstand verliert, ohne Kosten oder Zeitverbrauch.
- Maus zielt, Linksklick schießt. Zwei Läufe erlauben zwei schnelle Schüsse, danach 0,4 s zum Durchladen.
  Zehn Patronen pro Magazin; **R** oder Rechtsklick lädt zwei Sekunden lang nach, auch vorzeitig.
- Wind verschiebt den Einschlag horizontal um 15–42 Einheiten im 1000 Einheiten breiten Spielfeld.
  Pfeil, Richtungstext und drei Stärkestufen zeigen ihn an. Wechsel alle 10–15 s; gegen den Wind vorhalten.
  Einschlagmarken zeigen die tatsächliche Schussposition. Wahrnehmung erweitert den Trefferradius wie vom Server geliefert.
- Flaschen: +1, Tontauben auf ballistischer Bahn: +3, seltene schnelle Drohnen: +5.
  Möwen sind geschützt: −3 (Gesamtpunkte mindestens null) und ein trockener, unvertont bleibender Holm-Kommentar.
- Holm schießt auf eigene, mit HOLM markierte Ziele. Ihr Tempo fällt über die Runde ab, ihr Endstand bleibt exakt
  `holm_endstand`. Keine Textzeile erklärt den Tempowechsel.
- „Relaxed aim“ schaltet nur den Wind aus, meldet `leicht: true` und wird fehlertolerant lokal gespeichert.
- Ergebnis erst nach Serverbestätigung: bei Niederlage **Again** plus bestehende Stimme „Again, Frankfurt.“;
  nach Sieg nur **Meet Holm**, das `schiessen_ende` sendet und die fertige Übergabe öffnet.
- **Esc** beendet. Bei verborgenem Fenster oder Fokusverlust pausiert der Ablauf mit Fortsetzen-Knopf.
  Tab bleibt im Overlay. Reduzierte Bewegung entfernt dekorative Splitter.
- Keine neuen Sounddateien: `gun_shot` / `gun_reload` werden nur benutzt, falls diese IDs im aktiven EdenSfx-Katalog existieren.

Neue Holm-Texte, absichtlich unvertont (Möwentreffer):
- “That one wasn’t in the bet, Frankfurt.”
- “Leave the gulls alone.”
- “Bottles, Frankfurt. Not birds.”

Die drei Zielarten und knappe Munition greifen allgemeine Schießbuden-Ideen auf; Inspiration:
[Nintendos Duck Hunt](https://www.nintendo.com/en-gb/Games/NES/Duck-Hunt-946955.html).
Wind, Parallelwette, Verlauf und Gestaltung sind eigenständig. Feintuning der Zielgrößen, Flugbahnen und Spawn-Abstände
liegt im Plugin; unveränderte Engine-Konstanten: `RUNDE_S = 45`, `HOLM_ENDSTAND = 40`.


### UX-Politur (30.10.2026)

- Proportionale Spielfläche, per Größenbeobachter eingepasst: keine Überlappung der Patronenleiste bei 720p,
  keine gestauchten Ziele auf Ultrawide. Kopf- und Fußanzeigen bleiben höchstens 1700 px breit.
- Ein offener Wasserblick benutzt Himmels- und Wasser-Ausschnitte des gelieferten Fotos, mit Abendtönung;
  das Vorderdeck bleibt der äußere Rahmen. Flaschen schwimmen im Wasserbereich statt über Polstern.
- Drei tatsächlich erreichbare Windstufen: Betrag 15 bis unter 24 = leicht, 24 bis unter 33 = mittel,
  ab 33 = stark. Der helle Rand beim Wechsel bleibt 1,8 Sekunden; Richtung und Stärke stehen weiterhin als Text da.
- Flasche: Glassplitter, Tropfen und sich ausbreitender Wasserring. Tontaube: Keramikscherben.
  Drohne: kurzer heller Ausfall und längere Funken. Reduzierte Bewegung behält die ruhigen Treffermarken.
- Restzeit beim Nachladen, deutlicher Hinweis bei höchstens zwei Patronen und permanentes „BEAT 40“ im Kopf.
- Freigegebene Bestandstöne gefunden: `docs/effekt-auswahl/status-labor/soundlabor/kampfkoerper/freigegeben/audio/gun_shot.ogg`
  und `gun_reload.ogg`. Zentraler EdenSfx-Katalog/Route noch durch die Engine-Sitzung anzubinden;
  dieses Plugin erzeugt keine eigenen Audio-Kontexte und umgeht die zentrale Lautstärke nicht.

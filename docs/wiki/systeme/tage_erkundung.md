# Eden Rise – Tage, Erkundung, Beute (Konzept)

Stand 20.10.2026 · beschlossen mit Duc, **noch nicht gebaut**. Gehört zu [kampf.md](kampf.md).
Rebalancing (Level-Kurve, Uhren) erst, wenn das Crafting definiert ist.

## Kalender

- **21 Tage**, 7 Story-Kapitel mit je einem Zeitfenster von etwa 3 Tagen und einer Frist. Kapitel und Kalendertag
  werden getrennt gezählt (heute: 1 Kapitel = 1 Tag in `hauptstory.py`).
- Begründung in der Story: Das Ersatzteil kommt aus Genua, das Ultimatum der Eden Group wird auf drei Wochen gestreckt.
- Uhren (Batterien, Diesel, Siri/Yasin, Video) laufen pro Kalendertag und müssen für 21 Tage neu eingestellt werden.
- Tageswechsel: Animation, die Sonne geht auf, „Tag 1 → Tag 2“, darüber groß der Kapitelname.

## Tagesablauf (5 Phasen)

| Phase | Art |
|---|---|
| Frühstück / Lagebesprechung | Story, sonst reagiert die Crew auf gestern (Chronik-Eintrag „gestern“ ins Prompt) |
| Mittag | frei |
| Nachmittag | frei |
| Dinner | Event an Land oder an Bord; hier wird gekocht |
| Nacht | Event |

Zwischen den Phasen: Chance auf eines der vier Event-Arten **Handy, Gag, Bordrat, Duell**.

## Erkundung (Dave the Diver)

- Eine Erkundung füllt eine freie Phase. Orte mit festem Level-Bereich (Bedrohungsfarbe zeigt, wohin man schon kann):
  Hafen & Dorf, Macchia, Strandgrotte, Berge & Genueser Turm, Wrack & Tiefsee, Alons Anwesen (ausgebrochener Zoo), an Bord.
- Stationen (Kampf, Fund, Ereignis, Rast, Elite); an jeder Station: tiefer gehen oder zurück.
- **Beutetasche** klein (Start 6 Plätze), dreimal größer (8/10/12): zweimal bei Totò gegen Geld, einmal über eine Mission.
  Ausgerüstetes zählt nicht. Lager an Bord unbegrenzt.
- **Tod:** Duc wacht in der nächsten Phase an Bord auf. Eine Stewardess (zufällig rotierend) muntert ihn auf, fest
  vertont, Wortlaut je nach Persönlichkeit und Vertrauen: „Sei vorsichtiger … das hier habe ich bei dir gefunden.“
  **1 Gegenstand** wird geborgen, bevorzugt ein Missionsgegenstand. Rest der Tasche weg, **Erfahrung der Erkundung weg**.

## Gegenstände

Beute hat vier Zwecke: Missionen (bringe Gegenstand X von Ort Y), **Kochen** beim Dinner, Material für Rosis Werkstatt,
Verkauf an Totò. Neue Arten in `gegenstaende.json`: Material, Zutat, Missionsgegenstand; jeder Gegenstand kennt seine Orte.

## Nebenquest Madame Casanova gegen Alon

Madame Casanova hasst Alon wegen seiner rücksichtslosen Extravaganz. Aufträge rund um sein Anwesen und den ausgebrochenen
Zoo; Belohnung: **Ruf im Dorf** (Wert gibt es schon, bekommt damit Wirkung), am Ende die Elektro-Harpune nach der Festa.

## Engine-Umbau (Reihenfolge)

1. Zeitraster 21 Tage, Phasen Frühstück/Mittag/Nachmittag/Dinner/Nacht, Kapitel mit Fristen
2. Chronik-Eintrag „gestern“, Frühstücks-Reaktion
3. Events zwischen den Phasen
4. `kern/expedition.py` + `orte.json` (Stationen, Gegner-Pools, Beute, Rückzug, Tod und Bergung)
5. Inventar: Tasche und Lager, Taschen-Upgrades bei Totò
6. Gegenstandsarten Material/Zutat/Missionsgegenstand, Kochen beim Dinner, Crafting (offen)
7. Missionen mit Ort und Gegenstand, Casanova-Quest, Wirkung von Ruf
8. Kartenbildschirm, Tageswechsel-Animation
9. Uhren und Level-Kurve neu einstellen (Simulation; bei bis zu 42 Erkundungen steilere Kurve, graue Gegner weniger EP)

## Kochen und Crafting (Stand 20.10.2026, Logik ohne Zutaten)

- Kochen gibt es schon (`kern/handel.py` kochen: Wahrnehmungs-Probe mit Küchen-Vorteil, Teller für eine Person oder
  Crew-Essen, 12 Gerichte als Lieblingsessen). Neu: **jede Figur bringt ihr Lieblingsgericht als Rezept bei**,
  und **jedes Gericht gibt am nächsten Tag einen eigenen Bonus** (Dating, Rabatt, Vertrauen, Begehren, Attribut,
  Kampf, Erkundung ...). Ein Bonus gleichzeitig, gilt bis zum nächsten Dinner.
- **Kühlschrank** in der Kombüse: Zutaten ohne Kapazitätsgrenze lagern und horten.
- Werkstatt bei Rosi für Upgrades bleibt. **Apotheke** kommt später über einen neuen NPC.
- Zutaten und Mengen werden später nachgelegt.
- 21.10.2026: **genau 1 Lieblingsessen pro Person** (Lola: Bao Buns, Petru: Fish Pie, Alva behält Chili Noodles,
  Madame Casanova Bouillabaisse) plus **10 Standard-Gerichte**, die von Anfang an freigeschaltet sind.
- **Wildschwein** kommt als Gegner dazu (Zutatenquelle, Macchia).
- **Angeln** als Minispiel: Boot, Strand, Fluss, See. Zutaten: einfache bei Totò und Alva kaufen, Rest sammeln,
  von Gegnern oder angeln.

## Küche, Stand 21.10.2026 (beschlossen)

- **Nonna Fiora** (Bäuerin im Hinterland): Grundzutaten, Anbau (Kohl, Wildkräuter, Chilis; 1 Tag, begrenzte Beete,
  zweimal erweiterbar), Tierhaltung als Investition (Wachteln täglich, Hühner täglich, Schweine alle 2 Tage, Rinder alle
  3 Tage). Ihr Enkel bringt die Ernte morgens in den Kühlschrank. **Isabelle**, ihre Novizin, führt die Apotheke (datebar).
- **27 konkrete Zutaten**, jede mit genau einer Wirkung (gekauft schwach, geholt stark), Qualität ★/★★/★★★ (×1 / ×1,5 / ×2).
- **Goldene Regel:** 2 oder 3 verschiedene Zutaten ergeben immer ein konkretes Gericht (3.276 Kombinationen),
  18 davon sind Lieblingsgerichte (♥, ×1,5 und großer Vertrauensschub, zufällig entdeckbar). Regelbruch = **Brauner
  Schleim**: heilt 1 LP, Verkauf 5 €, −6 Vertrauenspunkte bei allen am Tisch (Skala 0–100, Stufen ab 0/10/22/36/55/80).
- Namen: Formel aus Basis/Haupt/Akzent (`werkzeuge/kochbuch.py`, Liste `kochbuch.html`); beim ersten Kochen gibt das
  Sprachmodell dem Gericht einen eigenen Namen + einen Satz, gespeichert im Rezeptbuch. Formel-Name ist der Rückfall.
- Kein täglicher Wunsch beim Frühstück (zu viel neben Dates, Missionen und Events).

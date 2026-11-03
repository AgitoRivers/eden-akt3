# Hintergründe bauen: so werden sie perfekt

> Stand 02.11.2026 · Duc nach vier Abnahme-Runden für Zimmer und Orte. Vor jedem neuen Hintergrund lesen.
> Werkzeuge: `werkzeuge/hintergrund_bild.py` (neu, t2i) und `werkzeuge/hintergrund_edit.py` (Detail ändern, Nachtfassung).
> Allgemeine Krea-Regeln: `X:\AI\PromptStudio\KREA_LEITFADEN.md`.

## Die vier Regeln, die nie brechen

1. **Keine Tür im Bild.** Kein Türrahmen, keine Klinke, kein Spalt. Wir stehen im Raum, nicht in der Tür. Eine sichtbare Tür heißt
   „jemand schaut rein“, und die Szene ist nicht mehr intim.
2. **Der Vordergrund unten in der Mitte ist leer.** Dort stehen die Figuren. Kein Tisch, Sessel oder Möbelstück vorn, sonst stehen
   sie auf dem Tisch. Möbel gehören an die Seitenwände und an die Rückwand.
3. **Frontansicht aus der Raummitte**, Blick zur Rückwand, beide Seitenwände sichtbar. Möbel und Andenken dürfen links und rechts
   stehen, das Bett oder das Hauptmotiv an der Rückwand.
4. **Ich prüfe jedes Bild selbst, bevor Duc es sieht.** Tür, Vordergrund, Fenster. Was durchfällt, kommt nicht auf die
   Seite oder wird erst beschnitten.

## Stil

- **Yacht:** dunkles glänzendes Walnussholz, cremefarbene Lederpaneele, weiße Bettwäsche, warme Lampen mit weißem Schirm, kleine
  Deckenspots, Messing. Vorbild: Spare Cabin bei Nacht (`eden_rise_waescherei_kabine_nacht.png`).
- **Crew-Kabinen liegen unter Deck:** kein Fenster, kein Bullauge. Krea setzt trotzdem gern eins; dann abschneiden.
- **An Land:** weiß gekalkter Stein, Holzbalken, Korsika. Bibi: Schwarz, Gold, Senfgelb, weiße Kissen, abstraktes Aquarell.
- **Jede Figur erzählt sich im Raum:** Andenken passend zur Lore (Wiki-Figurenseite und `welt/wohnen.md`). Sachen liegen im Regal,
  nicht auf dem Bett. Ein Bett, das unbenutzt wirken soll (Rosi), bleibt leer. Was versteckt ist (Strudels Körbchen), ist gedämpft
  in der Farbe und halb im Schatten.
- **Ohne Personen:** „not a single person is in the shot“, „present-day contemporary“, „photorealistic“. Keine Personen-Wörter.

## Ablauf

1. **Prompt** in `hintergrund_bild.py` (MOTIVE) mit dem Blick-Baustein: Frontansicht, leerer Vordergrund, nur Wände und Schränke an
   den Rändern, keine Tür. Positiv formulieren (CFG 1, Negativ wirkt nicht).
2. **Immer 4 Seeds** je Motiv: `python werkzeuge\hintergrund_bild.py <motiv> 4`. Bei mehreren Entwürfen je Entwurf 4 Seeds.
3. **Selbst ansehen** (Kontaktbogen), Fehler notieren.
4. **Abnahmeseite** mit allen Seeds über `werkzeuge\abnahme_seite.py`, mein Vorschlag mit ⭐ und einem Satz, was auffällt.
   Duc sucht selbst aus.
5. **Ein Detail ändern** (Decke, Kuscheltier, zweites Bett): `hintergrund_edit.py` mit Duc's gewählter Variante als Vorlage, wieder
   4 Seeds, Vorlage auf der Seite daneben. **Neu platzieren** (Sachen vom Bett ins Regal) geht besser als neues t2i.
6. **Nachtfassung** per Edit aus der gewählten Tagfassung, damit beide gleich aussehen. Innenräume ohne Fenster brauchen nur ein Bild.
7. **Übernehmen:** `--waehle <n>`. Hat Krea doch einen Türrand oder ein Bullauge gesetzt: Kante abschneiden, auf 1664x928 hochrechnen
   (unten verankern, damit der Boden bleibt) und das Ergebnis noch einmal ansehen.
8. **Ins Spiel:** Raum in `basis_eden_rise.py` (`R(...)`, bei Zimmern `versteckt=True`), Risiko und Zuordnung in `MODUL["orte"]`
   (`modul_eden_rise.py`). modul.json gezielt ergänzen, nicht neu bauen.

## Was Duc in den Runden gesagt hat (02.11.2026)

- „Wichtig ist, wir stehen im Raum, also nicht mit einer offenen Tür. Da würde die Immersion ja zerbrechen!“
- „Die Chars stehen von vorne mittig im Bild, sie stehen sonst auf dem Tisch.“
- „Mache auch immer 4 Seeds, dann kann ich besser aussuchen.“
- Lieber Frontansicht, damit man die andere Seite mit Schränken und Andenken auch sieht.

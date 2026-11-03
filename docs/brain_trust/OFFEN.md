# Offen und Parkplatz

Stand 24.10.2026 abends. Erledigtes wandert als Eintrag ins Register (`ENTSCHEIDUNGEN.md`).

## Taktik-Karte gegen Wiki (Stand 01.11.2026)

Das Wiki ist nach E-106 und E-107 weiter als der Code:
- `docs/UEBERGABE_TAKTIK.md` nennt noch den Kriegsrat an Tag 15, die Datei hat fremde offene Änderungen.
- Alvas Flinte: Szene im Spiel (`bl_alva_flinte`). Sie spricht vom schwarzen Anzug, ihr Sprite zeigt noch ihr Standard-Set, bis es einen Satz im Traje corto gibt.
- Belagerung im Kalender: Texte von `ereignisse_belagerung.py` und `ereignisse_belagerung_nacht.py` sind Entwürfe, mit Duc durchgehen. Prozent, Wellen, Schäden und Holzpreise im Spieltest festlegen (E-114). Crew-Aufträge am Abend fehlen noch, ebenso Bilder fürs Flicken. Neue Zeilen vertonen.
- Geschrieben, aber nicht vertont: Rosis Übergabe von Taser-Gewehr und Steel Mop (`a2_steelmop`, Tag 19 morgens) und Wolffs Schwert Parole (`bg_turm_parole`).

## Als Nächstes (Reihenfolge 9A)

1. ~~Brain-Trust-Dateien umbauen~~ (erledigt 24.10.)
2. ~~Tag 0 bauen~~ (gebaut 24.10., E-022). Vertonung fertig (950 Zeilen). Töne: 8 im Katalog und den Events zugeordnet (25.10.), **Duc erzeugt sie mit
   `Sfx_EdenRise.bat`** und wählt in `vorhoeren.html`. Stimmen Maxwell/Jana/Yamamoto sind zugeordnet und vertont,
   Fettnäpfchen bestätigt (25.10.). Neu ohne Ton: 3 Rosi- + 1 Totò-Zeile (Werkstatt) → nächster `Vertonen_EdenRise.bat`.
3. ~~Hafenkampf~~ (gebaut 25.10., E-044). Werte nach E-045. Offen: 37 neue Zeilen vertonen (Duc: `Vertonen_EdenRise.bat`), Töne Rudel/Keiler/Ziege.
   Wartet auf „bau es“: Rosi wirft Duc im Hafen Terremoto zu (E-049, Name Terremoto E-052; technisch: `bat` aus START_GEAR nehmen, erst Rosis Szene setzt `waffe_bat`, Quellentext anpassen – Training nutzt seit 75c5ffd den Schrubber `mop`), Training mit Schrubber (E-050).
4. **Eden-Wiki** (Entwurf 25.10., `docs/wiki/`): Ducs Freigabe + Klärungsliste K1–K14; danach Startzettel an alle
   Sitzungen, Gedächtnis-Eintrag „Wiki ist Kanon“, Regel im Brain-Trust-Prompt; Kategorie-Seiten Welt/Story,
   Interaktion, Items durch ihre Sitzungen.
5. **Alles auf Englisch** (Duc 25.10.): nach der Wiki-Freigabe alle Spieltexte paketweise prüfen und umschreiben
   (Pilot Tag 0 + Hafen, Abnahmeseite alt/neu), geänderte Zeilen neu vertonen, `--aufraeumen` für alte Tondateien.
   Im Pilot mit: Maxwells Tutorial-Satz `l1_angriff` (kern/tutorial.py) ohne Baseballschläger – er trainiert mit dem
   Schrubber, Terremoto kommt erst von Rosi im Hafen. Vor dem Items-Paket die Items-Sitzung fragen (Besitz Item-Texte).
6. **Brain-Trust-Reflexion** (Duc 25.10.): aus den Dialogen dieser Wochen lernen – Zusammenarbeit verbessern, die
   fünf Rollen sympathischer machen.
7. **Spieltest Akt 1** durch Duc.

## Wartet auf Ducs Antwort

- **Kennenlern-Details:** Intro-Karte je Figur, Unbekannte als „?“-Silhouette, alle Bord-Figuren bis Ende Tag 2 kennen.

## Offene Story-Fragen

- Siris Post #StrandedInParadise (Weg in Säule Wahrheit, dreht Alons Negativpresse).
- Neue NPCs: Schauspielerin an Bord · neue Romanzen für Akt 2/3 (Elsa möglich) · Gegengewicht-Figur mit derselben
  Einschränkung wie Alon.
- Yamamoto: Bindungsstufen, Katana-Übergabe, Ende (immer Heimflug) ausbauen; Megan holte ihn als Investor? (offen).
- ~~Diesel als Joker~~ gestrichen (E-082, Duc 27.10.: Diesel und Strom gibt es nicht mehr). Alt: 1 Kanister = Rosis Aufrüstung sofort statt über Nacht; Sturmnacht Tag 3: Unit-01
  anwerfen oder Kerzenlicht (graue Wahl); dann Diesel wieder sichtbar machen (verborgen in modul_eden_rise.py) und die drei pausierten Ladenartikel (Can of Diesel, Used Boat Battery, Solar Panel Cleaner, pausiert "akt2") freigeben. Strom als Stimmung (Kerzen/Musik) in Events.
- Ortskapitel Kloster: als Frame-Kette gebaut (26.10., E-074). Offen: Rastplätze, Hof/Apotheke als
  Läden, Schnellreise, Capra sichtbar, Journal-Reiter im Menü (Items), Vertonung der neuen Zeilen. Berge gebaut (27.10., E-081, `welt/ortskapitel_berge.md`): offen nur Bilder/Sprites von Character Design und der Akt-2-Kalender (das Spiel endet nach Tag 8).
- Akt 2 planen (offener Kalender wie Dave the Diver, Folgen der Anhörung als Startlage E-032).

## Kleinkram

- Unit-01-Sprite mit bernsteinfarbenem Auge.
- Lolas Outfits Aloha + Shore Leave (vorgeschlagen, keine Häkel-/Netz-/Punktmuster).
- Alva-Einträge im Weltbuch „Eden Yacht“.

## Parkplatz

- Dossier-Sammeln günstig halten (Auszug-Skript, Sonnet, ≤120 Zeilen).
- Trophäen-/Achievement-Liste als Polaroid-Album (ganz am Ende).
- Cutscenes: Drehbuch jetzt, Video (MiniMax) oder Sprite-Aufnahme am Ende.
- Stimmungsfilter für Random-Events pro Tag (angenommen, Umsetzung am Ende).
- Skript vs. LLM je Mechanik festlegen; bei Anhörung, Geständnis, Festa, Enden keine Halluzination.
- Niederlage-Kosten im Roguelike (am Ende des Kampf-Designs).
- Figuren (Duc 28.10.): **Alon** wird mit der Belagerung geplant (Akt 2, zweite Woche, Tag 15–21); **Ingrid** und der **CEO** gehören zu Akt 3 – erst dann aufgreifen, vorher nicht daran erinnern.
- Chips, Akt 3: geplante Wendung, in der Alon etwas an den umgebauten Chips ausnutzt (Items 25.10., nur merken, nicht bauen).
- ~~Fall-Kanon: Ermittlungswege in der gesperrten Werkstatt~~ erledigt 25.10. (Spieltest): Wege in den Antriebsraum verlegt.
- Event-Dichte Tage 3–7 und Reichweite des Pools (~17 % je Durchlauf), siehe `SPIELTEST_AKT1.md` – Designentscheidung offen.
- Räume für Zweisamkeit, später (Duc 02.11.2026): **Duschkabine der Crew** und **Toilette auf der Yacht** fehlen noch als Orte (`kern/orte.py`, Risiko-Orte mit Bild von innen, ohne Tür).
- Akt 3 (Duc 02.11.2026): Romanzen auf **Expeditionen** mitnehmen; dann gilt ein **Rastplatz** auch als intime Szene. Erst mit Akt 3 bauen.
- Megan (Duc 02.11.2026): Bei ihrer Rückkehr in Akt 3 bekommt sie eine **freie VIP-Kabine** an Bord (eigener Raum mit Bild, ihr Zimmer in `kern/orte.py`). Kommt mit ihrem Paket.
- Akt 3, Geldziel (Duc 03.11.2026, „machen wir jetzt noch nicht“): **Wiederaufbau des Dorfs** nach dem Brand mit Geld, Vorbild Stardew-Gemeinschaftshaus, je Haus ein Dank der Bewohner (Vorschlag G3 der Interaction-Sitzung). Erst mit Akt 3 bauen.
- Selfie-Format (Duc 03.11.2026, „lassen es erstmal so, vielleicht habe ich irgendwann Langeweile“): Für fast vollen Handy-Bildschirm wären neue Selfies in **9:16** (z. B. 768×1344 in Krea) besser; heute 2:3 bzw. 7:9 mit Schwarz oben und unten (`docs/wiki/systeme/handy.md`, Fotos-App). Bestehende Bilder bleiben.

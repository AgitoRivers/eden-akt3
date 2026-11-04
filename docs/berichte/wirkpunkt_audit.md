# Wirkpunkt-Audit: Wo wirkt jeder Vorteil im Code?

Stand 04.11.2026 · Branch `berichte-audits` · Prüfer: Claude (Audit, keine Änderung am Spiel)

## Methode

Ich habe alle Vorteile, Items und Mechaniken aus den Daten (`gegenstaende.json`, `charms.json`, `laeden.json`, `kuechen.json`, `erweiterungen.json`, `missionen.json`, `auftraege.json`, `lob.json`, dazu der gebaute Stand in `modul.json`) und aus dem Wiki (`docs/wiki/systeme/*.md`, `docs/wiki/welt/akt3.md`, `wohnen.md`, `enden.md`) gesammelt. Für jeden Eintrag habe ich per Grep über `kern/`, `werkzeuge/`, `client/` und `eden.py` die Stelle gesucht, an der der Effekt gelesen wird und etwas ändert, und die Funktion dort gelesen. Gesetzte Flags habe ich maschinell gegen alle Bedingungen in den Modul-Daten und gegen den Code abgeglichen (680 gesetzte Flags, 310 ohne direkten Leser); Präfix-Leser wie `"waffe_" + id`, `"sn_%s_fertig"` oder `bl_verband_*` habe ich von Hand nachgeprüft und als gelesen gezählt. Jede Bewertung „fehlt“ ist mit einem eigenen Grep über `kern/`, `werkzeuge/`, `client/` und `eden.py` abgesichert.

**Nicht geprüft:**
- Gesperrte Bereiche: Favours und Handy-Ketten (nicht geprüft, gesperrt), ebenso `module/eden_rise/story.json`. Was nur dort gelesen oder vergeben wird, kann ich nicht sehen. Wo das eine Bewertung kippen könnte, steht „(Vorbehalt: gesperrt)“.
- Keine Tests ausgeführt. Tests, die `module/eden_rise/figuren` oder `eden-config.json` brauchen, sind hier ohnehin lokal nicht prüfbar. Der Bericht ist eine statische Code-Lektüre, kein Spieltest.
- Spürbarkeit im Spiel (Balance, Gefühl) beurteile ich nur aus den Zahlen, nicht aus einem Durchlauf.

**Bewertung:** **vorhanden** = wird gelesen und wirkt spürbar (Preis, Zugang, Lohn, Uhr, Kampfwert, Bedingung). **klein** = wird gelesen, aber nur Text, ein einziger Ort oder kaum spürbar. **fehlt** = nirgends im Code gelesen, nur Wiki oder Beschreibung, oder unerreichbar.

Vorweg das Lob, weil es stimmt: Der Kampf ist vorbildlich verdrahtet. Alle 18 Wirkarten der 75 Chips, alle fünf Jacken-Eigenschaften, alle 21 Jacken-Charms und alle sechs Tagesboni der Küche haben eine benannte Zeile in `kern/kampf.py`, `kern/handel.py` oder `kern/kuechen.py`, meist mit Kommentar und Datum. Die Lücken liegen fast alle an den Rändern: Ladenware aus der Zeit vor dem Abschalten der Schnelljobs, Akt-3-Anschlüsse und ein paar Gegenstände, deren Versprechen im Text älter ist als der Code.

## 1. Mechaniken

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Crew-Moral auf den Würfeln | Buzzing +1, ab Tense -1 bei Proben mit Crew (`modul.json` moral, `beziehungen.md`) | `kern/moral.py: wuerfel_bonus()`, eingebaut in `szene.feste_probe()`, `ereignisse.waehlen()`, `handel.job_machen()` | vorhanden |
| Moral: Frühstücksgeschenke | Buzzing: Crew legt Dinge hin (Espresso, Mate, Duct Tape, Dog Food …) | `kern/moral.py: morgen()` mit `modul["moral"]["geschenke"]` und `morgen_geschenke` | vorhanden |
| Bordrat, dritter Weg: Vorteil bei Buzzing | Buzzing gibt Vorteil, ab Tense SG +2 (`moral.dritter_weg`) | `kern/ereignisse.py: waehlen()` rechnet `mit_vorteil`, reicht ihn aber nur an `wuerfel.probe` ohne `probe_fn` weiter. `eden.py` übergibt immer `probe_fn` (`szene.feste_probe`), der Vorteil geht verloren. SG +2 wirkt. 30 Optionen betroffen | fehlt |
| Ruf im Dorf (Village Reputation) | Taten im Dorf heben ihn, Schmuggelfunde senken ihn (`eden.py` Hilfetext) | `kern/taktik.py` (`ruf_rudert`: Dorf rudert mit), `kern/regeln.py: zugang()` (Petrus Werkstatt ab Ruf 2), 6 Event-Bedingungen, `kern/legenden.py: tagesende()` (Verfall, `ruf_schutz`) | vorhanden |
| Dorf redet (Legenden) | Taten werden Legenden und geben Ruf (`dorf_redet.md`) | `kern/legenden.py: tagesende()` | vorhanden |
| Uhren Siri pulls away / Yasin's video | Uhr voll: Siri frei bzw. Video online, Ruf -2 | `kern/showrunner.py: tagesende()` (über `hauptstory.plan_bauen`), setzt `siri_frei`, das `kern/orte.py` und 23 Event-Bedingungen lesen | vorhanden |
| Uhr Repairs (8 Segmente) | voll: “The Eden Rise runs under her own power again.” | `kern/zustand.py: folgen_anwenden()` setzt `uhr_reparatur_voll`, niemand liest es. Nur Anzeige in `eden.py` (Uhrenliste) | klein |
| Energie (0 bis 3) | Wege mit Probe kosten Energie, Espresso und Pause geben sie zurück | `kern/ereignisse.py: waehlen()` sperrt nur Optionen mit Feld `energie`; in den prüfbaren Events trägt keine Option dieses Feld (Vorbehalt: gesperrt). Schnelljobs aus | klein |
| Persona-Stärke Küche | Vorteil auf jede Kochprobe | `kern/handel.py: kochen()` (Vorteil auf Perception), 8 Event-Proben `vorteil: kueche` (+2 „Your strength“) | vorhanden |
| Persona-Stärke Handwerk | “advantage on every repair and building check” (`modul.json` personas) | 6 Event-Proben (+2). Bauspiel der Belagerung (`kern/belagerung.py`) und Wiederaufbau (`kern/aufbau.py`) fragen die Persona nicht ab; Jobs aus | klein |
| Persona-Stärken Köpfchen und Charme | Schwäche des Gegners gratis sichtbar, Reden mit Vorteil | `kern/kampf.py` (`schwaeche_bekannt`, Zeile 1178; `advantage_with`, Zeile 1631) | vorhanden |
| Schnelljobs (68 Missionen) | Lohn, Vertrauen +6, Werkzeug-Vorteil, Teile, Unikate (`missionen.json`) | `kern/handel.py: jobs_aktiv()` gibt `False` (`modul["schnelljobs"] = False` seit 29.10.); dazu laufen alle Missionen nur an Tag 2 bis 7 | fehlt |
| Angeln mit Ködern | breitere goldene Zone, seltenere Fische, kürzeres Warten (`kuechen.json` koeder) | `kern/angeln.py` (Auswurf mit `koeder.wirkung()`), `kern/koeder.py` | vorhanden |
| Fisch verkaufen bei Petru | Rohpreis mal Anteil je Seltenheit, +5 % je Vertrauensstufe Petru, nach Weg B 80 % | `kern/abbau.py: fisch_preis()` | vorhanden |
| Abbau mit Axt und Spitzhacke | Werkzeugstufe 0 bis 3 bei Petru | `kern/abbau.py: starten()`, `schlag()` über `werkzeug_stufe()` | vorhanden |
| Garten und Ställe | Ställe mit `plaetze`, `menge_plus`, `zucht_minus`; Zitronengras erst mit `zitronengras_da` | `kern/farm.py: tagesbeginn()`, `garten_pflanzen()` (Flag aus `kuechen.json` pflanzen) | vorhanden |
| Kochen im Baukasten | Basis heilt, Akzent gibt Tagesbonus, Sterne ×1 / ×1,5 / ×2 | `kern/kuechen.py: kochen_baukasten()`, `bonus()`; Leser: `handel.preis()` (-10 %), `handel.ankauf()` und `abbau` (+10 %), `kampf.attributes()` (Courage +1), `kampf.award_xp()` (+10 %), Chips-Summe Krit (+5 %) | vorhanden |
| Tischszenen | Lieblingsgericht zum ersten Mal „liebt“: eigene vertonte Szene | `kern/tisch.py`, ausgelöst in `handel.kochen_aktion()` | vorhanden |
| Auffangstation Mochi's | Rettung: Ruf +1, Bibi +2; Begleiter hilft im Kampf (Bindung 1 bis 3) | `kern/mochis.py: kampf_vorbereiten()` setzt `beistand` im Kampf, `kampf_ende()` zählt die Bindung | vorhanden |
| Schneider (Danzel) | Lohn oder Verzicht (Ruf +1 / +2), Schnittmuster je 3 Aufträge, Maßstücke | `kern/schneider.py: muster()`, Abgabe; `sn_dress_whites_fertig` liest `taktik.json` (Chiaras Figur) | vorhanden |
| Schießwette um Gemelli | Sieg gibt die Doppelbüchse | `kern/schiessen.py: ergebnis()` setzt `waffe_gun` | vorhanden |
| Lob für Attribute | Figur kommentiert Attribut 3/4/5 | `kern/lob.py` (nur Zeile, keine Wirkung, so gewollt) | klein |
| Wiederaufbau (Akt 3) | Häuser mit `tk_haus_weg_<id>` werden Baustellen, Piraten tragen je Tag eine Stufe (`akt3.md`) | `kern/aufbau.py` existiert, wird aber von `eden.py` und keinem Modul importiert; `aufbau_fertig_<id>` liest niemand | fehlt |
| Festa-Aufträge von Casanova | entscheiden, wie voll die Festa ist (`akt3.md`, CLAUDE.md) | kein Code, keine Daten | fehlt |
| Zeugen für die Kommission | Duc überzeugt die Leute einzeln, Namen fehlen am Fischernetz (`akt3.md`) | kein Code; `kern/mochis.py` liefert nur den Halsband-Befund für die Kommission | fehlt |

## 2. Ausrüstung: Waffen, Jacken, Werkstatt, Chips

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Terremoto (bat), Erde, Schaden 2 | Startwaffe von Rosi (`items.md`) | Flag `waffe_bat`, `kern/kampf.py` Zeile 217 ff. (Besitz über Präfix `waffe_`) | vorhanden |
| Le Large (spear), Feuer, Schaden 4 | von Casanova nach dem Kloster | Flag `waffe_spear` | vorhanden |
| Sussurro (knife), Luft, Schaden 2 | Grotte, Gennaros Zelle | Flag `waffe_knife` | vorhanden |
| Gemelli (gun), Zwillingsläufe | Erstschuss und Konter feuern beide Läufe | `kern/kampf.py: start` (Zeile 1226), Konter (Zeile 2509) | vorhanden |
| Riposte (sword), Wasser, Schaden 5 | Tauchgang zum Wrack, Woche 3 (`sirene_weg`) | Werte in `kaempfe.json` da, aber kein Event setzt `waffe_sword`; `sirene_weg` liest im prüfbaren Code niemand (Vorbehalt: gesperrt) | fehlt |
| Terra Scura: Standfest | Verteidigen Schutz +2, nie erschüttert | `kern/kampf.py` (Zeilen 2423, 2595) | vorhanden |
| Meramie: Fließend | Parade-Fenster +5 %, Konter ×1,1 | `kern/kampf.py: _parade_data` (Zeile 2387), Konter (Zeile 2508) | vorhanden |
| Incendio: Glut | +2 Schaden je Brandstufe am Gegner | `kern/kampf.py` (Zeile 1475) | vorhanden |
| Zéphyr: Leicht | Ausdauer +2, Fliehen leichter (SG -3) | Code da (`kampf.py` Zeilen 1195, 2209), aber kein Fundort: kein Event setzt `jacke_jacket_air` | fehlt |
| Citadelle (Cyber Armor) | alle Elemente ×0,7, erster Treffer halb, Parade -10 % | Code da (`resist: alle`, `heavy`, Zeile 2537), kein Fundort im Spiel (nach Alon, NG+) | fehlt |
| Rosis Werkstatt: zwei Upgrades | +1 Schaden bzw. +1 Schutz je Stufe, 150 € / 400 € plus Material | `kern/kampf.py: werkstatt_morgen()`, `stufe_von()` in Schaden und Schutz | vorhanden |
| Stufe-2-Material Smaragd, Rubin, Saphir, Titan | von tödlichen Gegnern (`ELEMENT_DROP`) | `kern/kampf.py` (Zeile 2790): Erde, Feuer, Wasser und ohne Element haben je mindestens einen tödlichen Gegner | vorhanden |
| Opal (Sussurro Stufe 2) und Silber (Gemelli Stufe 2) | Material für die zweite Stufe (`items.md`) | Opal fällt nur von tödlichen Luft-Gegnern, es gibt keinen; Silber steht in keiner Drop-Tabelle und wird in keinem prüfbaren Event vergeben | fehlt |
| Chips (75 Erweiterungen, 18 Wirkarten) | Schaden, Krit, Konter, Zustände, Element, Schutz, Parade, Ausdauer, Snack, Heilung, Fassung, Abwehr | `kern/kampf.py: chips_aktiv()` und alle Leser (`crit_chance`, Konter, `_parade_data`, Abwehr Zeile 2603, Heilung Zeile 2809 …). Hinweis: `erweiterungen.json` „Wirkungen noch nicht in der Engine“ und `items.md` sind veraltet | vorhanden |
| Scout (Radio Ear bis Know Thy Enemy) | zeigt Gegner, Level, Schwäche auf Expeditionen | `kern/kampf.py: aufklaerung()`, Plugin `eden-expedition` | vorhanden |

## 3. Verbrauchs-Items

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Kampf-Items (25, z. B. Plaster 10 € heilt 10 %, Bandage 25 %, First Aid Kit 40 %, Smoke Pot, Megaphone, sieben Granaten) | `gegenstaende.json` Art `kampf` | `kern/kampf.py: gegenstand_anwenden()`; Granaten erst mit `werkstatt_offen` (`handel.granaten_frei()`) | vorhanden |
| Waffenpflege (5 Wetzsteine, Spikes, Match Ammo, je 30 €) | +3 für 5 Runden im nächsten Kampf | `kern/handel.py: benutzen()` → `kampf.pflege_vorbereiten()` | vorhanden |
| Espresso, Energy Bar, alle Snacks (selbst essen) | Energie +1 | `kern/handel.py: benutzen()` bzw. `_verbrauchen()`; Energie selbst sperrt kaum etwas (siehe Mechaniken) | klein |
| Gras-Kuchen | Kater am nächsten Morgen, Ferrandi findet 10 % (Truhe 5 %), Ruf -1 | `kern/handel.py: _gras_kontrolle()`, `kater()` | vorhanden |
| Die Rose der Bürgermeisterin | Begehren +6 bei allen Frauen | `kern/handel.py: benutzen()` mit `punkte` | vorhanden |
| Kühlakkus (40 €, Alva) | “The supplies last a day longer when power runs low.” | setzt `vorraete_gekuehlt`, liest niemand; Strom gibt es seit 30.10. nicht mehr | fehlt |
| Kiste Ersatzteile (180 €, Totò, Eden-Shop) | “Rosi beams”, Uhr Repairs +1 | `zustand.folgen_anwenden()`; die Uhr hat keinen Leser | klein |
| Lola's Special Pesto, Fresh Catch | “Lola turns it into …” | `wirkung` leer, kein Leser in `kern/` (benutzen geht ohne Wirkung) | fehlt |
| Gerichte (14, z. B. Bun Riêu, Ramen, Bouillabaisse) | Lieblingsgericht „liebt“ einmal voll, Crew-Moral +1, +2 für alle bis 36 | `kern/handel.py: kochen()`, `koch_stufe()` | vorhanden |

Hinweis: Diesel, Bootsbatterie und Panel-Reiniger ruhen gewollt (`pausiert`, E-076); kein Befund, nicht gezählt.

## 4. Geschenke

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Geschenke nach Geschmack (63) | liebt, mag, neutral, mag nicht, hasst je Kategorie | `kern/handel.py: schenken()`: liebt = Erlebnis +1 Stufe (8 Punkte Vertrauen und Begehren), mag = +4 bis Deckel 35, hasst = -8 | vorhanden |
| Unikate für die Frauen (Chiara's Mug, Lea's Dive Computer, Sophia's Pen …, 90 bis 190 €) | +10 V und +6 B bzw. +12 V, mehr als „liebt“ (`gegenstaende.json` wirkung, `arten`) | `kern/handel.py: schenken()` kennt keine Stufe über 2: ein Unikat wirkt wie „liebt“ (+8/+8). Die Tabelle `wirkung` liest niemand | klein |
| Unikate für Nebenfiguren (Totò, Yasin, Elsa, Petru, Casanova) | 12 Punkte statt 8 | `kern/handel.py: schenken_npc()` (`NPC_PUNKTE[3] = 12`) | vorhanden |
| Megan's Crew Card, Holm's Licorice (Unikate ohne Preis) | Belohnung einer Mission | nur über Schnelljobs (aus), in keinem prüfbaren Event vergeben | fehlt |
| Intim-Schwelle | erst ab Begehren 3, nie vor anderen, Vertrauen -1 bei zu früh | `kern/handel.py: schenken()` | vorhanden |
| Geschenke ans Dorf | halber Ruf-Punkt, Bestechung je Rolle | `kern/handel.py: schenken_npc()`, `halb_plus()` | vorhanden |

## 5. Charms und Talismane

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Jacken-Charms mit Attribut (12, z. B. Chiara's Dolphin: Charm +1, Frederico's Lion Strength und Courage +1) | +1 Attribut, darf über 5 | `kern/charms.py: attribut()/boni()`, gelesen in `szene.feste_probe()`, `ereignisse.waehlen()`, `gesten`, `kampf.attributes()`, `anhoerung` (Bluff), `handel.kochen()` | vorhanden |
| Jacken-Charms mit Kampfwert (9: Holm Schutz +1, Petru Parade +10 %, Isabelle heilt 3, Alva Snacks +2, Yasin Krit +5 %, Elsa Vorteil auf Intimidate, Maxwell Spezial +20 %, Casanova Serie 2, Mazzera Ausdauer +1) | Kampfwerte | `kern/charms.py: kampfwerte()` → `kampf.chips_aktiv()` und Leser (Zeilen 1372, 1481, 1556, 2521) | vorhanden |
| Vergabe aller 21 Charms | bei Vertrauen 5 oder nach Fund | `werkzeuge/eden_rise/ereignisse_charms.py`, Folge `{"charm": id}` → `kern/zustand.py` | vorhanden |
| Attribut-Gegenstände (10, +1 solange getragen) | “+1 Courage while you carry it.” | `kern/szene.py: feste_probe()` (Events, Gesten, freie Szenen). Nicht im Kampf (`kampf.attributes()`), nicht in der Anhörung | vorhanden |
| Fünf davon unerreichbar: Lea's Old Dive Mask, Elsa's Torch, Siri's Scarf, Lola's Band, Sophia's Bookmark | `quelle: event/mission` | in keinem prüfbaren Event vergeben, nicht im Laden (Vorbehalt: gesperrt) | fehlt |
| Glücksbringer (13, z. B. Binoculars 220 €, Lucky Coin 120 €, Tarot 100 €) | einmal am Tag Vorteil auf ein Attribut | `kern/szene.py: feste_probe()` mit `tagesnutzung` | vorhanden |
| Werkzeuge: Battered Red Toolbox (180 €), Japanese Chef's Knife (110 €) | “Advantage on repair jobs / cooking jobs” | nur `kern/handel.py: werkzeug_da()` in `jobs_heute()`, Jobs aus. Beide stehen trotzdem bei Totò und Alva zum Verkauf | fehlt |

## 6. Schlüssel, Key Items, Schmuggel

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Key to Petru's Workshop | öffnet die Werkstatt | `kern/regeln.py: zugang()` liest `{"item": "petru_key"}`, aber kein Event und keine aktive Mission vergibt ihn (Zugang läuft über Ruf 2 oder Rosi) | fehlt |
| The Mayor's Invitation to the Festa | öffnet die Piazza | `kern/regeln.py: zugang()`; die Piazza ist ab Tag 5 ohnehin offen (`tag_ab: 5`), die Karte zählt also nur an Tag 1 bis 4 | klein |
| Key to Alva's Back Room | öffnet das Hinterzimmer | `ort: alvas_bar_hinterzimmer` gibt es nicht; der echte Raum `alvas_hinterzimmer` (`kern/orte.py`) hat keine Sperre | fehlt |
| Schmuggel-Kontrolle | 20 % je Tagesende in der Tasche, Truhe ×0,5, Ruf -2 | `kern/handel.py: tagesende()` | vorhanden |
| Crate of Limoncello (90 €) | an Alva: +240 € | `kern/handel.py: benutzen()` (`geld`) | vorhanden |
| Three “Designer” Handbags (60 €) | an Yasin oder Casanova: Trust +8 | `kern/handel.py: schenken_npc()` | vorhanden |
| “Internet from the Sky” Data Package (300 €) | “Phone features for one day.” | `benutzen: []`, `handel.benutzen()` lehnt ab; kein Leser in `kern/` | fehlt |
| Cohiba Cigars (150 €) | “Village Reputation +2 with the old men at the harbour” | `benutzen: []`, kein Leser | fehlt |
| Unstamped Cuban Rum (120 €) | Schmuggelware | keine Wirkung, nur Verkaufswert (`handel.ankauf()`) und Kontrollrisiko | klein |
| Teile für Aufträge (15, z. B. Relay 90 €, Netting Twine 25 €) | Besorgung für einen Auftrag | `kern/handel.py: sortiment()` zeigt sie nur bei offenem Auftrag, den es ohne Schnelljobs nie gibt | fehlt |
| Key Items Golden Mace und Torn Note | „wird später gebraucht“ | vergeben (`ereignisse_kloster.py`), aber noch kein Leser | klein |
| Triton's Trident | Key Item | nie vergeben, kein Leser | fehlt |
| Andenken (Keepsake Box, Echo) | keine Spielwirkung: Epilog und Sammlung | `kern/kabine.py: ansicht()` (Vitrine, Echo); `kern/abschluss.py` liest keine Andenken | klein |

## 7. Läden

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Totòs Draht | Preisfaktor `1,3 minus 0,12 × Draht`: Draht 1 = ×1,18, Draht 5 = ×0,70; Ware ab Draht 3/4 | `kern/handel.py: draht_faktor()`, `_preis()`, `sortiment()` | vorhanden |
| Totòs Sonderangebot und Ankauf | ein Stück -25 %, Ankauf 40 % | `kern/handel.py: sortiment()`, `ankauf()` | vorhanden |
| Alva: Rabatt und Handel-Punkte | -4 % je Stufe über 1 (bis -16 %), +4 Vertrauen je Kauf bis Stufe 3 | `kern/handel.py: _preis()` (`rabatt_je_stufe`), `kaufen()` (`HANDEL_PUNKTE`) | vorhanden |
| Eden-Shop (Megan) | ab Tag 8, ab Vertrauen 3 ×0,85 | `kern/handel.py: sortiment()` (`ab_tag`), `_preis()` (`rabatt_ab_vertrauen`) | vorhanden |
| Lolas Kombüse | zweites Essen ab Vertrauen 3 | `kern/handel.py: essen_extra()` | vorhanden |
| Danzels Laden, Bà Tưs Schale | Laden erst nach Bedingung, übernimmt Kleidung; eine Schale am Tag | `kern/handel.py: laden_offen()`, `_umgezogen()`, `tageslimit` | vorhanden |

## 8. Vertrauen und Beziehung

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| Romanzen-Leiter, Abende, Intim-Liste | Stufen schalten Szenen frei (`beziehungen.md`) | `kern/ereignisse.py` (Bedingungen), `kern/orte.py`, Stufen-Abstand in `kern/zustand.py: punkte_add()` | vorhanden |
| Vertrauen 3: „She trusts you“ | +1 auf Charm- und Empathy-Proben mit ihr | `kern/szene.py: feste_probe()` | vorhanden |
| Vertrauen 5: Charm | Übergabe-Event je Figur | `ereignisse_charms.py` → `charms.geben()` | vorhanden |
| Vertrauen der Dorf-Figuren Pascal, Mina, Sandru, Minicu | 29 Vertrauens-Folgen in `ereignisse_dorf.py` | kein Leser: keine Bedingung, kein Rahmen in `figurenrahmen.json`, kein Code | fehlt |

## 9. Story-Flags mit Vorteil

| Vorteil | Versprechen (Quelle) | wirkt in (Datei: Funktion) | Stand |
|---|---|---|---|
| `taser_gewehr`, `alva_flinte` | Rosi baut Chiara das Taser-Gewehr, Alva holt Papas Flinte | die Trupps stehen in `taktik.json` immer bereit; das Flag selbst liest niemand | klein |
| `toto_stand` | Totò bekommt seinen Markttisch | kein Leser (Vorbehalt: gesperrt) | fehlt |
| `petru_rezept` | Petrus Rezept | kein Leser (Vorbehalt: gesperrt) | fehlt |
| `tipp_vorliebe` | Alva verrät Vorlieben | Wirkung kommt direkt über `VL()` (`kern/vorlieben.py`); das Flag liest niemand | klein |
| `alon_kiste_genutzt` | Versprechen an Totò: “Make the crate count against Alon” | kein Leser (Vorbehalt: gesperrt) | fehlt |
| `danzel_festa_auftrag`, `chiara_festa_kleid` | Vorbereitung der Festa | kein Leser; Akt-3-Anschluss | fehlt |
| `megan_zurueck` | Megan bezieht ihre Kabine in Akt 3 (`wohnen.md`) | gelesen in `kern/orte.py` (Zimmer), gesetzt nirgends | fehlt |

## Zählung

| Stand | Einträge |
|---|---|
| vorhanden | 53 |
| klein | 13 |
| fehlt | 26 |
| gesamt | 92 |

(Gruppen-Zeilen wie „Kampf-Items (25)“ zählen als ein Eintrag.)

## Die zehn größten Lücken

1. **Werkzeug-Items werden verkauft, wirken aber nicht.**
   Was fehlt: Toolbox (180 €) und Chef's Knife (110 €) versprechen Vorteil auf Reparatur- und Kochaufträge; der einzige Leser `handel.jobs_heute()` ist mit den Schnelljobs abgeschaltet.
   Warum es zählt: Der Spieler zahlt fast zwei Tageshonorare (125 €) für einen Satz, der nie eintritt. Das kostet Vertrauen in jede andere Item-Beschreibung.
   Vorschlag: Die Toolbox gibt Vorteil auf `vorteil: handwerk`-Proben in Events (`kern/ereignisse.py: waehlen()`, gleiche Stelle wie „Your strength“) und spart im Wiederaufbau eine Stufe Material (`kern/aufbau.py: bauen()`). Das Messer gibt beim Kochen +1 Stufe auf „gut“ (`kern/handel.py: koch_stufe()`). Bis dahin aus dem Sortiment nehmen (`pausiert`).

2. **Der Wiederaufbau ist gebaut, aber nicht angeschlossen.**
   Was fehlt: `kern/aufbau.py` wird nirgends importiert, `aufbau_fertig_<id>` liest niemand, die Handwerk-Stärke wirkt beim Bauen nicht.
   Warum es zählt: Duc nennt den Wiederaufbau den Kern von Akt 3. Ohne Wirkpunkt ist er eine Materialabgabe ohne Belohnung.
   Vorschlag: Aktion in `eden.py` (wie `abbau.werkzeug_kaufen`), `aufbau.tag_vorbei()` in `plan.tagesende()`. Jedes fertige Haus öffnet seinen Laden wieder (`laeden.<id>.bedingung: {"flag": "aufbau_fertig_<id>"}` in `handel.laden_offen()`) und gibt Ruf +1. Handwerk spart eine Stufe Holz.

3. **Das Vertrauen der Dorf-Figuren sammelt sich ohne Leser.**
   Was fehlt: 29 Folgen geben Pascal, Mina, Sandru und Minicu Vertrauen; keine Bedingung und kein Code fragt es ab.
   Warum es zählt: Woche 5 lebt davon, dass Duc die Leute einzeln überzeugt. Das ist genau die Stelle, an der dieses Vertrauen endlich zählen kann.
   Vorschlag: Zeugen-Mechanik für die Kommission mit Schwelle je Figur (`regeln.gilt({"vertrauen": [pid, 3]})`), Ergebnis als Flag `zeuge_<pid>`, gelesen vom Fischernetz in `kern/abschluss.py`. Die Kunden des Schneiders und der Wiederaufbau geben passende Punkte dazu.

4. **Casanovas Festa-Aufträge haben weder Daten noch Code.**
   Was fehlt: kein Auftrag, kein Zähler, kein Leser für das Schlussbild; `danzel_festa_auftrag` und `chiara_festa_kleid` warten schon ins Leere.
   Warum es zählt: Das ist die versprochene sichtbare Folge der ruhigen Woche 4 („wie voll die Festa ist“).
   Vorschlag: Die Aufträge in `auftraege.json` (das Format mit `schritte` und `fertig` gibt es schon, `kern/auftraege.py: pruefen()`), Belieferung aus Farm, Angeln und Küche über `kuechen.vorrat_menge()`. Ein Festa-Wert (Zahl der erfüllten Aufträge) steuert die Besetzung der Schlussszene.

5. **Der Buzzing-Vorteil im Bordrat geht verloren.**
   Was fehlt: `ereignisse.waehlen()` berechnet `mit_vorteil`, gibt ihn aber nicht an `probe_fn` weiter; `eden.py` übergibt immer `probe_fn`.
   Warum es zählt: 30 dritte Wege sind die Belohnung für eine gute Crew-Stimmung. Die Strafe (SG +2) wirkt, die Belohnung nicht. Das fühlt sich unfair an.
   Vorschlag: `probe_fn` um einen Parameter `vorteil` erweitern und in `szene.feste_probe()` mit dem Glücksbringer-Vorteil verodern (eine Zeile je Stelle), dazu ein Test mit `moral = 4`.

6. **Drei Ausrüstungsteile haben Code, aber keinen Weg ins Spiel.**
   Was fehlt: Riposte (`waffe_sword`), Zéphyr (`jacke_jacket_air`) und Citadelle setzt kein Event.
   Warum es zählt: Neue Ausrüstung soll sich wie ein Achievement anfühlen (`items.md`). Riposte hängt am Tauchgang, Zéphyr an Megans Rückkehr: beides Akt 3.
   Vorschlag: Riposte als Lohn des Tauchgangs (Folge `{"flag": "waffe_sword"}`, der Saphir aus der Grotte wartet schon), Zéphyr in Megans Rückkehr-Szene (die setzt auch `megan_zurueck`), Citadelle als Beute des Endkampfs.

7. **Opal und Silber sind unerreichbar.**
   Was fehlt: keine tödlichen Luft-Gegner, Silber in keiner Drop-Tabelle.
   Warum es zählt: Sussurro und Gemelli bleiben auf Stufe 1, obwohl Rosi und die Werkstatt Stufe 2 zeigen. Gemelli soll gegen Alons Drohnen glänzen.
   Vorschlag: `drop: "opal"` an einen Drohnen-Elite-Gegner in `kaempfe.json` (Leser `kampf.py` Zeile 2790 ist da). Silber als Lohn eines Akt-3-Events mit Holm oder als Danzels Schneiderlohn (`kern/schneider.py`).

8. **Schmuggelware mit leerem Versprechen.**
   Was fehlt: Datenpaket (300 €) und Zigarren (150 €) haben `benutzen: []`; `handel.benutzen()` lehnt ab.
   Warum es zählt: Teuerste Ware bei Totò, Kontrollrisiko 20 % am Tag, und der Effekt aus dem Text kommt nie.
   Vorschlag: Zigarren als Geschenk an Petru und Don Anghjulu über `schenken_npc()` mit Ruf +1 (`halb_plus` auf 1.0). Das Datenpaket schaltet einen Tag lang einen sichtbaren Bonus frei, etwa doppelte Legenden-Wirkung in `kern/legenden.py: tagesende()`, statt einer Telefonfunktion (Anschluss an Handy-Bereich nur über die Fragenliste).

9. **Fünf Attribut-Talismane und zwei Unikate kommen nie ins Spiel.**
   Was fehlt: Lea's Dive Mask, Elsa's Torch, Siri's Scarf, Lola's Band, Sophia's Bookmark, Megan's Crew Card und Holm's Licorice hingen an Missionen, die aus sind.
   Warum es zählt: Das sind persönliche Gaben mit Geschichte. Gerade in Akt 3 („Romanzen fertig spielen“) wären sie ideale Wegmarken.
   Vorschlag: je eines als Folge einer Romanzen-Leiterszene der Stufe 4 (`werkzeuge/eden_rise/ereignisse_romanzen.py`, Folge `I(...)`); Wirkpunkt bleibt `szene.feste_probe()`. Dazu `kampf.attributes()` um die getragenen Attribut-Items erweitern, damit +1 auch im Kampf zählt.

10. **Kleine Versprechen ohne Wirkung: Kühlakkus, Pesto, Fang, Ersatzteile, Alvas Schlüssel.**
    Was fehlt: `vorraete_gekuehlt` und `uhr_reparatur_voll` ohne Leser, Pesto und Fang ohne Wirkung, Alvas Schlüssel zeigt auf einen Raum, den es nicht gibt.
    Warum es zählt: Einzeln klein, zusammen das Gefühl „Items sind Deko“. Das untergräbt die starken Systeme daneben.
    Vorschlag: Kühlakkus halten den Vorrat einen Tag frisch (Stern bleibt 2, `kern/kuechen.py: vorrat_add()`), Fresh Catch wird beim Benutzen zu zwei Fischen im Vorrat (`kuechen.fang()`), Pesto gibt einen Tagesbonus Vertrauen (`kuechen.bonus`). Die Ersatzteilkiste wird Rosis Material (ein Stufen-Rabatt in `kampf.werkstatt_morgen()`). Alvas Schlüssel: Hinterzimmer `alvas_hinterzimmer` mit Zugang `[{"item": "alvas_schluessel"}, {"begleitung": "alva"}]` sperren (`regeln.zugang()`).

**Gegenrede (Sora, Systemdesign):** Nicht jede Lücke muss gefüllt werden. Ein paar Ladenstücke ohne Wirkung zu streichen ist schneller und ehrlicher als sie neu zu verdrahten, und Akt 3 hat wenig Zeit.
**Verbesserungsrunde (Maelle, Spielerreise):** Einverstanden für Teile, Diesel und Rum. Die Lücken 2, 3 und 4 sind aber keine Altlast, sondern der Bauplan von Akt 3: Wiederaufbau, Zeugen und Festa sind drei Leser für Material, Dorf-Vertrauen und Küche, die heute schon fließen. Wer sie zuerst baut, schließt fünf andere Lücken gleich mit.

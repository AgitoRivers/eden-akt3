# Rüstung, Waffen und Aufrüstung (Beschluss 24.10.2026)

Diese Datei fasst zusammen, was Duc im Brain Trust am 24.10.2026 entschieden hat. Sie ersetzt die Abschnitte „Waffen“, „Rüstung“ und „Ausrüstung“ in `kampf.md`. Alles hier ist beschlossen, außer dem, was unter „Noch offen“ steht.

## Die drei Aufrüstungs-Arten

Rüstungen und Waffen haben je **drei Plätze**, einen je Art:

| Art | Platz | Was es ist | Wann frei |
|---|---|---|---|
| **Charm** | 1 | Anhänger, den eine Figur gibt | von Anfang an |
| **Verstärkung** | 2 | Material. Rüstung: schützt vor einem Element (feuerfest, wasserfest, elektrofest, luftfest). Waffe: das Element der Waffe. | nach Upgrade 1 bei Rosi |
| **Erweiterung** | 3 | mehr Funktion (Attribut +1, Krit, Zustand, Konter, Reichweite) | nach Upgrade 2 bei Rosi |

Der Pool gehört Duc und gilt für **alle** Jacken und alle Waffen. Man tauscht jederzeit in der **Kabine** auf dem Boot. Das Loadout bleibt am Gegenstand.

**Charms (gebaut 28.10.2026, Duc):** Plüsch-Anhänger für die Jacke. Abnahme `docs/abnahme/charms.html`, Daten
`werkzeuge/eden_rise/charms_eden_rise.py` → `module/eden_rise/charms.json`, Engine `kern/charms.py`.

- **Bekommen:** Erreicht eine Figur zum ersten Mal **Vertrauen 5**, schickt sie ein Foto ihres Anhängers mit zwei
  Chat-Blasen (`werkzeuge/eden_rise/ereignisse_charms.py`, Events `ch_<figur>` Tag 2–6 und `ch_<figur>_2` Tag 8–21).
  Die Übergabe kommt vor allen anderen Handy-Nachrichten, aber nur einmal (Flag `charm_<figur>`). Beide Antworten geben
  den Charm, „Hangs it on the jacket straight away“ hängt ihn sofort an die getragene Jacke; sonst hängt er an der
  Jacke, wenn dort noch keiner ist, oder liegt in der Kabine.
- **Fredericos Löwe** kommt, sobald alle drei Ställe auf Nonnas Farm voll ausgebaut sind (Flag `farm_voll`, `kern/farm.py`).
- **A Mazzera's Hunting Charm** ist das Unikat der Berge (`beute.md`). Wer ihn einbaut, gibt die Folge `{"charm": "mazzera"}`.
- Laetitia und Adrien geben keinen.
- **Tragen:** Jede Jacke hat einen runden Charm-Platz, versetzt neben den Erweiterungen im Upgrade-Fenster der Kabine
  (Reiter „Chips“). Er erscheint mit dem ersten Charm und funktioniert auch vor Rosis Werkstatt. Ein Charm hängt immer
  nur an einer Jacke; an eine andere gehängt, wandert er.
- **Wirkung:** Nur der Charm an der **getragenen** Jacke zählt. Attribut-Boni gelten **überall** (Kampf, Szenen,
  Events, Jobs, Gesten, Anhörung, Bewunderung) und dürfen **über 5** gehen; die Würfelanzeige nennt den Charm als
  eigenen Bonus. Kampfwerte laufen über `kampf.chips_aktiv` mit denselben Namen wie bei den Erweiterungen.

| Figur | Charm | Wirkung |
|---|---|---|
| Chiara | Delfin | Charisma +1 |
| Lola | Känguru mit Joey | Strength +1 |
| Megan | schwarzer Puma (kommt mit dem Versorgungsboot) | Cunning +1 |
| Lea | Clownfisch | Empathy +1 |
| Rosi | Little Unit-01 (weißer Roboter) | Courage +1 |
| Totò | runder Waschbär | Cunning +1 |
| Holm | Eisbär mit Kapitänsmütze | Schutz +1 |
| Yamamoto | Schildkröte mit Sonnenbrille | Perception +1 |
| Petru | Oktopus | Parade-Fenster +10 % |
| Nonna | Henne mit Schürze | Empathy +1 |
| Isabelle | Schaf mit gesticktem Lavendel | heilt 3 nach jedem Kampf |
| Alva | schwarzes Stierkalb mit Nelke | Snacks heilen +2 |
| Yasin | plüschiger Falke | Krit +5 % |
| Jana | „Not Strudel“ (weiße Katze) | Courage +1 |
| Siri | Robbe Selma | Empathy +1 |
| Sophia | Eule | Perception +1 |
| Elsa | Schäferhund mit Polizeimütze | Vorteil auf Intimidate |
| Maxwell | Gorilla mit Gürtel | Spezialangriffe +20 % Schaden |
| Madame Casanova | Flamingo | Fassung −4 schon nach 2 perfekten Paraden (statt 3) |
| Frederico | schwarzer Löwe (Gold) | Strength +1 und Courage +1 |
| – | A Mazzera's Hunting Charm (Unikat) | Ausdauer +1 (8 → 9) |

Neu nur für Charms: `spezial_schaden` (Prozent auf jeden Treffer eines Spezialangriffs), `parade_serie` (perfekte
Paraden weniger bis Fassung −4), `vorteil` (Grund-Aktionen mit zwei Würfeln). Die Übergabezeilen sind vertont
(`Vertonen_EdenRise.bat --praefix ch_`).

## Rosis Werkstatt

- Öffnet in **Akt 2** (Tag 8), nachdem Rosi sie nach der Explosion repariert hat.
- **Zwei Upgrades** je Rüstung und Waffe: Stufe 0, 1, 2. Jacke: Schutz +1 je Stufe. Waffe: Schaden +1 je Stufe.
- Kosten: Stufe 1 kostet 120 € und ein Material, Stufe 2 kostet 240 € und ein besseres Material (Details im Abschnitt „Material und Steine“, Stand 25.10.; die Geldbeträge sind vorläufig, Geld wird ganz am Ende festgelegt).
- Abgeben über die Kabine (Fach „Für Rosi“), **keine Aktion**. **Ein Upgrade pro Nacht**, für Rüstung **oder** Waffe. Am Morgen kommt eine Nachricht von Rosi auf dem Handy. Die Jacke oder Waffe liegt wieder in der Kabine.
- Texte (Hintergrund, Überreichungs-Sätze, Rosis Nachrichten) stehen **fest in den Daten**, englisch, die gesprochenen vorab vertont. Das Sprachmodell erfindet davon nichts.

## Die fünf Rüstungen

Alle Looks sind frei kombinierbar mit allen Waffen. Der Look **gibt der Jacke ihre feste Eigenschaft**, damit nicht alle austauschbar sind. Zahlen aus der Simulation (siehe unten).

| Name (Untertitel) | Look | Eigenschaft | Spielstil |
|---|---|---|---|
| **Terra Scura** (Biker Jacket) | Erde | **Standfest:** Schutz +1, Verteidigen gibt in der Runde Schutz +2, Duc wird nie erschüttert | Fels |
| **Meramie** (Navy Pea Coat) | Wasser | **Fließend:** Parade-Fenster +5 %, Konter nach perfekter Parade ×1,1 | Tänzer |
| **Incendio** (Burgundy Pea Coat) | Feuer | **Glut:** Duc schlägt je Brandstufe am Gegner +2 stärker | Berserker |
| **Zéphyr** (White Pea Coat) | Luft | **Leicht:** Ausdauer +2, Fliehen leichter | Läufer |
| **Citadelle** (Cyber Armor) | Cyber | **Alles-in-einem:** Schutz 5, schützt vor allen Elementen, der erste Treffer pro Kampf zählt nur halb, Parade-Fenster −10 % | Boss |

- **Schutz je Akt (ohne Cyber):** Akt 1: 2, nach Upgrade 1: 3, nach Upgrade 2: 4. Ohne Jacke bleibt der Grundschutz 2.
- **Cyberrüstung:** nach dem ersten Sieg über Alon, kommt mit Werkstattstufe 0 ins NG+1. Duc beginnt dann mit ihr.
- **Umziehen** geht nur in der Kabine auf dem Boot, ohne eigene Szene.
- **Freischaltung** (Vorschlag): Erde von Anfang an, Feuer im Feuerwehr-Ereignis (Akt 1), Wasser im Taucher- oder Fischer-Ereignis (Akt 2), Luft durch Megan nach der Anhörung (Akt 2), Cyber nach Alon (Akt 3).

## Die fünf Waffen

Eine Waffe je Waffenart. Die Faust entfällt, Duc hat immer eine Waffe. Startwaffe ist *Terremoto* (bis 25.10. „Fracasso“, umbenannt – siehe unten „Namen“). Die Waffenarten behalten ihre Stärken und Schwächen aus `kampf.md`.

| Name (Untertitel) | Art | ID | Slots |
|---|---|---|---|
| **Riposte** (Cavalry Sabre) | Klinge | `sword` | 1 |
| **Terremoto** (Baseball Bat) | Stumpf | `bat` | 1 |
| **Sussurro** (Combat Knife) | Messer | `knife` | 1 |
| **Le Large** (Boar Spear) | Stange | `spear` | 1 |
| **Gemelli** (Double Rifle) | Fern | `gun` | 2 |

Jeder Pfad geht mit jeder Waffe. Passt die Waffe zum Pfad, gibt es einen kleinen Bonus, einen Zwang gibt es nicht.

**Sprites:** `combat\Duc<Look><Sword|Bat|Knife|Spear|Gun>`, Looks Erde, Wasser, Feuer, Luft, Cyber.

## Simulation (`werkzeuge\kampf_balance_v6.py`)

Duc trägt jede Jacke gegen alle 29 Gegner der Gegnertabelle auf seinem Level (200 Kämpfe je Gegner und Jacke, vier Pfade, „Normal“, Regeln aus v5). Ø Verlust an Lebenspunkten, kleiner ist besser:

| | Ø alle | Kämpfer | Schmuggler | Schütze | Berserker | Ab Level 8 |
|---|---|---|---|---|---|---|
| Terra Scura | 38 | 38 | 36 | 37 | 44 | 47 |
| Meramie | 38 | 37 | 36 | 35 | 45 | 48 |
| Incendio | 40 | 39 | 38 | 39 | **43** | 47 |
| Zéphyr | 40 | 40 | 39 | 37 | 44 | 46 |
| Citadelle | – | – | – | – | – | **43** |

**Urteil:** Die vier Lederjacken liegen im Ø 1,8 Punkte auseinander, Citadelle liegt ab Level 8 etwa 4 Punkte vorn. Keine Jacke dominiert, jede hat eine Nische: Incendio ist die beste Jacke für den Berserker-Pfad, Meramie für Schütze und Kämpfer, Terra Scura gegen Flieger und Maschinen. Gut genug für den ersten Spieltest.

**Die ersten Werte waren schlecht:** Mit Meramie +10 % Fenster und Konter ×1,25 war sie bei 28 von 29 Gegnern die beste Jacke, die anderen drei fast wirkungslos. Deshalb ist Meramie abgeschwächt, die drei anderen sind gestärkt. Zéphyr bleibt bei +2 Ausdauer. Mit +3 wäre sie ab Level 8 so gut wie die Cyberrüstung.

**Nicht simuliert:** Verstärkungen (Widerstände), Erweiterungen und Charms, Fliehen (Zéphyr), der Hinweis zur Gegnerart vor dem Ausflug.

## Noch offen

- Akt-Verteilung aller Funde (kommt später). Akt 2 hat einen offenen Kalender, das ändert die Taktung der Upgrades.
- Schreibweise von **Meramie** und die Namen der vier Verstärkungen (Vorschlag: *Glutleder*, *Gischtleder*, *Isoliernaht*, *Windfutter*).
- Katalog der Erweiterungen und Charms mit allen Texten (Entwurf mit 22 Einträgen liegt vor, muss auf die drei Arten umsortiert werden).
- Meisterstufe nur im NG+, Rosis Morgenzeile je Stufe, Meisterstück-Perk (geparkt).
- Schicksal der 8 Story-Waffen in `kaempfe.json`: Sie werden Erweiterungen, Verstärkungen und Charms.
- Hinweis zur Gegnerart vor dem Ausflug (Vorabend-Zeile im Handy).

## Stand 25.10.2026: Schritt 2 gebaut (Rosis Werkstatt)

- Daten: `WERKSTATT` in `werkzeuge\eden_rise\kaempfe_eden_rise.py` (Kosten, Material, 20 feste Rosi-Sätze). Regeln: `kern\kampf.py` (`abgeben`, `werkstatt_morgen`, Stufe zählt im Kampf +1 Schaden/Schutz).
- Freischaltung per Flag `werkstatt_offen`. Das Event `rosi_werkstatt_offen` (ereignisse_gag1.py) setzt es, kommt aber erst, wenn `akt2_werkstatt_bereit` gesetzt ist (Akt 2 ist noch nicht geplant). Die Vorschau (Testschalter) öffnet die Werkstatt.
- Material: Piastra bei Totò (40 €), Plaque de Maître als Drop bei Gegnern der Stufe tödlich/Albtraum (oder `drop` am Gegner).
- Kabine: Leuchtpunkt „Für Rosi“, ein Stück pro Nacht, kein Tragen des abgegebenen Stücks. Morgens Nachricht im Handy-Faden von Rosi.
- Noch offen: Vertonung der 20 Sätze und der 2 Event-Zeilen, Akt-2-Auslöser, Verstärkungen, Erweiterungen, Charms.

## Beschluss 25.10.2026 (Duc, Brain Trust): feste Elemente, Startausrüstung

- **Das Element einer Waffe ist fest.** Es gibt keine Verstärkung, die es setzt oder wechselt (gegen Cheater-Builds). Die Kategorie „Verstärkung“ entfällt, ebenso Elementschutz für Jacken. Es bleiben: Upgrades (Schaden/Schutz), Erweiterungen (Eigenschaften: Krit, Parade-Fenster, Schutz …) und Charms (Plüschtiere, Attribute).
- **Elemente:** Terremoto Erde, Le Large Feuer, Riposte Wasser, Sussurro Luft, Gemelli **kein Element** (wirkt über die Art Fern: Erstschuss, stark gegen Flieger). Die Flinte kann später über eine Erweiterung ein Element bekommen (Ausnahme).
- **Kreis:** Wasser > Feuer > Erde > Luft > Wasser. Tiere sind Erde (schwach gegen Feuer), Flieger sind Luft (schwach gegen Erde).
- **Start:** Duc besitzt nur Terremoto und Terra Scura. Terremoto wirft Rosi ihm im Hafen zu (E-049; das Training mit Maxwell läuft mit dem Schrubber, E-050). Le Large bekommt Duc erst, wenn er **Madame Casanovas Mission** abschließt, also nach dem Ortskapitel Kloster in Akt 2 (Duc 25.10.; Übergabe-Szene in `docs/wiki/welt/ortskapitel_kloster.md`: Jagdspeer ihres Vaters aus dem Winter ihrer Geburt, Name nach dem offenen Meer; setzt `waffe_spear`, das Event passt die Story-Sitzung an, sobald die Missions-Mechanik steht). Die Flinte kommt in Akt 2. Besitz = Startausrüstung + Flags `waffe_<id>` / `jacke_<id>`.
- **Macchia:** viele Tiere (Erde), der Boss ist ein gepanzertes Monster. Duc geht mit **Terremoto** hinein (Stumpf passt zum Panzer).
  - Die **Ringe der Tiere** sind Chips der Stufe 1.
  - Der **Löwe** trägt zusätzlich einen **Steuerchip**: ein Missionsgegenstand für die Alon-Spur, kein Kampf-Chip.
  - **Felsnische beim Kloster** (Beschluss Duc 26.10., E-074): die **erste Stahlplatte** fürs Jacken-Upgrade und ein **Zettel des Agenten** (`agent_note`), der sie gestohlen und versteckt hat. Der seltene Chip *Hammer Down* geht stattdessen an den **Alpha-Keiler** (Steinbrücke, Zwischenboss). Löwe: Leiden beenden gibt Steuerchip und Löwen-Chip, Chip herausschneiden nur den Steuerchip.
  - **Ambrosius' goldene Keule** ist ein Andenken, keine Waffe.

## Namen: warum Terremoto (25.10.2026)

Die Startwaffe hieß zuerst *Fracasso*. Wörtlich „Krach, Getöse“, im Deutschen klingt es aber nach **Fiasko** – und die erste Waffe darf nicht nach Versagen klingen. Duc hat sie in **Terremoto** (Erdbeben) umbenannt: Element Erde, Rosis Kartusche ist ein Wuchtgewicht, die Beben-Signatur der Engine passt dazu – Name, Lore und Wirkung erzählen dieselbe Geschichte, und das Wort geht gut über die Zunge. Regel für künftige Namen: Klang **und** Bedeutung in Deutsch, Englisch und Italienisch prüfen, kein Wort mit Beiklang von Scheitern oder Lächerlichkeit.

## Material und Steine (Beschluss 25.10.2026, Duc; noch nicht gebaut)

**Jacken:** Stufe 1 braucht eine **Steel Plate**, Stufe 2 eine **Titanium Plate** (schwarzes Metall; ersetzen *Piastra* und *Plaque de Maître*). Wie man sie bekommt und was sie kosten, wird später besprochen; 40 € bei Totò ist zu billig (ein Tageslohn).

**Waffen:** Jede Waffe hat einen **Basisstein** schon eingebaut (Stufe 0, wird mit einem festen Satz erklärt). Rosi **tauscht** ihn bei den Upgrades gegen den nächstbesseren Stein desselben Elements. Das Wort „Kartusche“ entfällt, die Steine müssen jeder kennen. Keine Sammelmechanik, kein Album.

| Element | Waffe | Stufe 0 (eingebaut) | Stufe 1 | Stufe 2 |
|---|---|---|---|---|
| Erde | Terremoto | Granit | Jade | Smaragd |
| Feuer | Le Large | Lavastein | Topas | Rubin |
| Wasser | Riposte | Seeglas | Aquamarin | Saphir |
| Luft | Sussurro | Quarz | Amethyst | **Opal** (Diamant verworfen, zu selten) |
| kein Element | Gemelli | – (kein Stein) | – | – (siehe Gemelli unten) |

- Jeder Stein gibt wie bisher +1 Schaden je Stufe. Die Basissteine erklärt Rosi in einem festen Satz (Granit vom Hafenkai für Terremoto, Lavastein von der Küste für Le Large, Seeglas aus dem Hafen für Riposte, Quarz für Sussurro).
- Charaktere bringen die Steine als **Missionen** (später, E-051-Geist); nicht jetzt.
  Erster Fall (28.10.2026, E-085): die **Sirene** in der Flut-Nacht gibt den **Saphir** (Riposte Stufe 2), bevor man den
  Säbel überhaupt hat. Stufe-1-Steine und die Steel Plate kann außerdem die Vampirin fallen lassen (10 % in der Flut-Nacht).
- **Plätze:** Erweiterungen 1, 2, 3 mit Rosis Stufe; der Charm-Platz erscheint erst beim ersten Charm; im UI sind freie Erweiterungs-Plätze klar sichtbar, der Charm hängt rund und versetzt daneben (gebaut 28.10.2026).

## Festgehalten 25.10.2026 (Duc): Upgrades sind endgültig

- **Rosi kann nur upgraden, nie zurückbauen.** Ein Upgrade verbraucht Stein bzw. Plate. Der alte Stein ist weg und lässt sich nicht mitnehmen oder wieder einsetzen. Erweiterungen und Charms bleiben dagegen frei tauschbar.
- **Folge für Gemelli:** Wechselnde Steine gehen nicht. Gemelli bekommt **nur ein Element** und kein Mischen von Elementen (zwei Elemente erzeugen Zustände wie nass + Luft = Strom und wären ein Overkill-Vorteil). Die Sonderregel steht im Abschnitt „Gemelli“.

## Gemelli (Beschluss 25.10.2026, Duc: „Wir machen B“; gebaut)

- **Kein Element und kein Stein.** Gemelli hat nie einen Stein. Ihre Upgrades laufen mit **Metall in Barrenform**: **Kupfer** (Stufe 1, warm, rotbraun) und **Silber** (Stufe 2, warm, matt satiniert); beide müssen im Bild klar unterscheidbar sein.
- **Zwillingsläufe** (Signatur `twin`): Der freie Erstschuss vor Runde 1 und **jeder Konter nach einer perfekten Parade** feuern beide Läufe, also zwei Treffer. Das ist die Eigenheit der Waffenart Fern.
- **Element über Erweiterungen:** Gemelli kann durch Erweiterungen Feuer-, Wasser-, Wind- oder Erdschaden bekommen und damit gezielt gespielt werden. Wegen der Zustandskombinationen (nass + Luft = Strom, Blenden und so weiter) darf **immer nur eine** Element-Erweiterung gleichzeitig getragen werden (Vorschlag; Duc bestätigt noch).
- Übergabe in Akt 2, Szene offen.

## Stand 25.10.2026: Steine und Plates gebaut

- `WERKSTATT["material"]` in `kaempfe_eden_rise.py`: Jacken Steel Plate → Titanium Plate; Waffen Jade/Smaragd (Terremoto), Topas/Rubin (Le Large), Aquamarin/Saphir (Riposte), Amethyst/Opal (Sussurro); Gemelli Kupfer und Silber (Barren). Basissteine stehen als `stein` und mit dem festen Rosi-Satz (`eigenschaft`) an den Waffen und erscheinen im Umziehen-Fenster.
- Beim Upgrade wird das Material verbraucht; die 20 Morgensätze nennen jetzt den Stein.
- Items `steel_plate`, `titanium_plate`, `kupfer`, `silber`, vier Stufe-1-Steine und vier Stufe-2-Steine in `gegenstaende_eden_rise.py`. **Fundorte und Preise sind vorläufig:** Stufe 1 (Plate und Steine) bei Totò für 80 €, Stufe 2 und Titanium Plate als Drop; starke Gegner (tödlich/Albtraum) lassen den Endstein ihres Elements fallen (Erde Smaragd, Feuer Rubin, Wasser Saphir, Luft Opal, ohne Element Titanium Plate). Item-Bilder für die neuen Materialien fehlen noch.

## Entfernt und geparkt (25.10.2026, Duc)

- **Entfernt:** Doppelflinte der Wildschweinjäger und Kampfmesser der Fremdenlegion (Katalog und Bilder). In der Story kamen sie nirgends vor.
- **Geparkt, nicht umgesetzt:** Je Waffenart eine **Masterwaffe**, die den Standard ersetzt. Beschlossen sind nur die Beispiele *Yamamotos Katana* für den Säbel (Riposte) und *Tritons Dreizack* für die Saufeder (Le Large); für Terremoto, Sussurro und Gemelli werden andere Waffen überlegt. Tritons Dreizack bleibt bis dahin als Andenken im Katalog.

## Terremoto erst im Hafen (25.10.2026, Story-Abstimmung E-049)

- Duc startet **nur mit Terra Scura**. Terremoto gehört ihm erst, wenn Rosi ihn im Hafen zuwirft (Events `hk_rosi_*`, Tag 2 nachmittags) und das Flag `waffe_bat` gesetzt ist.
- **Kämpfe davor:** Wer keine Waffe besitzt, kämpft mit dem **Holzschrubber** (Fallback `mop`, stumpf, Bonus 0). Das Training mit Maxwell nutzt ihn ohnehin. Sobald Duc eine Waffe besitzt, nimmt er sie.
- Quelle im Katalog: „Rosi, im Hafen nach dem Werkstattbrand“.

## Erweiterungen (Beschluss 25.10.2026, Duc; Katalog angelegt, Wirkungen noch nicht in der Engine)

- **Aufgabe:** Erweiterungen ändern Kampfwerte von Waffe oder Jacke (Krit, Parade-Fenster, Schutz, Zustände …). Attribute gehören den Charms.
- **Plätze:** je Waffe und Jacke 1 / 2 / 3 mit Rosis Stufe. Der Pool gehört Duc, Tausch frei in der Kabine, jede Erweiterung gibt es nur einmal. Sie sind **keine Inventar-Gegenstände** (6 Plätze), sondern eine eigene Sammlung.
- **Kategorien:** Waffe: Wucht, Präzision, Technik, Konter, Zustand, Element (nur Gemelli, nur eine gleichzeitig). Jacke: Schutz, Parade, Ausdauer, Erholung, Auftritt, Abwehr.
- **Namen:** einfache englische Wörter im Anime-Stil, zwei Wörter, drei Stufen (Gewöhnlich, Selten, Episch). Katalog: `werkzeuge/eden_rise/erweiterungen_eden_rise.py` → `module/eden_rise/erweiterungen.json`, **72 Stücke** (39 Waffe, 33 Jacke). Die Zahlen sind vorläufig bis zur Simulation.
- **Darstellung (Vorschlag):** In der Oberfläche gezeichnete **Chips**, keine Produktfotos. Die Form sagt die Gruppe (Waffe: Raute, Jacke: Wappen), die Farbe die Kategorie, der Rahmen die Seltenheit (Bronze, Silber, Gold) und ein Symbol die Wirkung. Die leeren Plätze eines Stücks haben dieselbe Form als Umriss, der Charm-Platz ist rund und versetzt.

## Erweiterungen: Stufen ersetzen sich (Beschluss 25.10.2026, Duc nach Brain-Trust-Runde)

- **Eine Familie steht im Pool nur einmal** (24 Familien: 13 für Waffen, 11 für Jacken). Eine bessere Stufe **ersetzt** die alte; steckt die Familie in einem Platz, wird sie dort gleich besser. Stufen darf man überspringen.
- **Die Stufe zeigt der Chip als drei Punkte**, die höheren sind grau („da ist noch mehr“).
- **Verteilung der Funde** auf Akt 1 bis 3 legen wir fest, wenn die Akte geschrieben sind (grob: Akt 1 vor allem Stufe 1, Akt 2 Stufe 2, Akt 3 Stufe 3, in jedem Akt auch neue Familien). Die Werkstatt öffnet erst in Akt 2; dass man vorher schon Chips sammelt, ohne zu wissen warum (zum Beispiel beim Kloster-Quest), ist gewollt und macht Vorfreude.
- **Eine Familie pro Stück**, nie zwei Chips derselben Familie an einem Stück.
- **Schwächere Funde** (schlechter als die vorhandene Stufe) bringen eine kleine Summe statt stumm zu verschwinden.
- **Rosi sagt bei jedem Ersetzen etwas**, und zwar je Kategorie etwas anderes (Zusatz von Duc folgt).
- Verworfen: Leveln durch Benutzung (zu wenige Kämpfe), Fusion (Pool wird größer). Geparkt: Stärke am Platz (Alternative D).

## Chips: Lore und Mechanik (Beschluss 25.10.2026, Duc; Mechanik gebaut, UI kommt später)

- **Name im Spiel: Chip** (intern auch „Modul“, Katalog „Erweiterungen“).
- **Lore:** Die Chips stammen aus **Alons Experiment**: Halsbänder (Behaviour Control Units) an Tieren und Technik der Agenten. Rosi schneidet den Sender heraus und baut sie so um, dass sie nur Duc helfen und er sie jederzeit herausnehmen kann. Dieselbe Technik, zwei Haltungen: **Kontrolle gegen Freiheit** (Alon: „Violence is a bug in the species. I'm patching it.“). Das erklärt auch die Hightech-Waffen.
- **Funde sind Schaltpläne:** Ein Fund schaltet eine Familie frei oder hebt sie auf die nächste Stufe (ersetzt die alte); schlechtere oder gleiche Funde werden verkauft (10 € je Stufe). Die Meldung: „You found a strange chip. Maybe Rosi can make something out of it.“, später mit Namen („New module found: …“).
- **Vor Rosis Werkstatt (Akt 2) sind Funde unidentifiziert** und wirken nicht; Duc sammelt sie ohne zu wissen wofür (Vorfreude). Öffnet die Werkstatt (Flag `werkstatt_offen`), sind alle bisherigen Chips auf einmal nutzbar; Rosi prüft sie und sagt je Kategorie etwas anderes (`CHIPS["rosi"]`, Duc ergänzt noch).
- **Quelle = Stufe:** Tiere mit Halsband liefern Stufe 1 (Akt 1), Agenten Stufe 2 (Akt 2), Stufe 3 aus „Alpha“-Gegnern (Platzhalter, die Level stehen noch nicht fest). Die endgültige Verteilung kommt nach dem Schreiben der Akte.
- **Wendung in Akt 3 (Duc 01.11.2026, noch nicht gebaut):** Durch Ducs Einmischen sammelt Alon sehr viele Daten, und das beschleunigt sein Forschungsprojekt: bessere Daten zu den Gefühlen der Tiere, weil sie so oft unter Stress stehen, Geodaten zu ihren Verhaltensmustern und bessere Absicherungen, damit niemand die Module umbauen, hacken oder entfernen kann. Duc und Rosi haben ihn unbewusst um Jahre weitergebracht. Halsbänder senden, bis Rosi den Sender herausschneidet, so erfährt Alon auch, wie sie das macht. Im Finale: Rosi: *“I took the leash out.”* Alon: *“I know. That's how I learned to lock it.”* Alon kann alles sperren, nur keinen alten Diesel ohne Chip, darum wird Unit-01s „letzter Schub“ zum Schlag gegen ihn. Ducs Ausrüstung fällt im Endkampf nicht aus. **Neue Module bleiben bis zum Ende nutzbar (Duc 01.11.2026);** die Absicherung trifft nur Alons eigene Technik im Finale.
- **Gebaut (kern/kampf.py):** Pool je Familie (`chip_finden`, ersetzt/verkauft), Plätze 1/2/3 mit Rosis Stufe, `chip_einsetzen`/`chip_entfernen` (nur Kabine; eine Familie je Stück, nur ein Element-Chip, Element-Chips nur in Gemelli, jede Familie nur an einem Stück), Wirkungen im Kampf (Schaden, Krit, Spezial-Kosten, Ausdauer, Konter, Zustandschancen, Element für Gemelli, Schutz, Parade-Fenster, Ausdauer-Maximum, Snacks, Heilung nach dem Kampf, Fassung, Abwehr gegen Zustände), Drops von `ratte_alpha`, `hund_alpha` und `keiler` (`CHIPS["drops"]`). Zahlen vorläufig bis zur Simulation. UI siehe `docs/ui_bilder/CHIPS_ART_DIRECTION.md`.

> **Stand 26.10.:** Karte (M), Inventar (I) und Character (C) sind getrennt, „Umziehen“ liegt im Inventar, die Werkstatt hat nur Chips und Upgrade. Maßgeblich ist `menue.md`; die beiden Abschnitte unten sind die Entstehungsgeschichte.

## Orte statt Reiter: Rosis Werkstatt als Ort (Beschluss 25.10.2026, Duc; gebaut)

- **Laden & Inventar** zeigt eine **Porträtreihe** statt Reiter: Auf dem Schiff Totò, Rosi, Megan, Lola; daneben „Tender nach Cala d'Orsu“ mit Alva (nur an Tagen, an denen Duc an Land war). Ein Klick öffnet den Ort groß (Hintergrund, Figur, Gruß) mit einem normalen Dialog mit Auswahlfeldern, **keine Szene**. Nonna Fiora folgt, sobald sie einen Laden hat.
- **Rosis Werkstatt** (Ort `rosi`, Hintergrund `eden_rise_workshop.png`) hat drei Auswahlfelder: **Umziehen** (Waffen und Jacken wechseln), **Chips** (einsetzen, wechseln) und **Verbessern** (Steine und Plates). Solange die Werkstatt kaputt ist, geht nur **Umziehen** (ihr Spind ist offen), Chips und Verbessern zeigen den Hinweis „zu“. Alles kostet keine Aktion.
- **Die Kabine ist für die Ausrüstung nur noch Ansicht:** Waffen, Jacken und Chips lassen sich dort nicht tauschen. Die **Truhe bleibt in der Kabine** (Items zwischen Inventar und Truhe verschieben, Duc 25.10.). Der Punkt „Ausrüstung“ zeigt nur an („Umziehen bei Rosi“), der Upgrade-Punkt ist weg. Truhe, Handy, Boxhandschuhe und Koje bleiben.
- Server: Umziehen, Chips und Verbessern gehen in der Wahl-Phase und in der Kabine (nicht im Kampf und in Szenen).

## Orte wie ein Händler in Skyrim (Korrektur Duc 25.10.2026; gebaut)

- Das Laden-Symbol (Taste L) öffnet **„Wohin?“** mit **großen Kacheln**: jede Figur auf ihrem Hintergrund (Totò, Rosi, Megan, Lola; darunter der Tender nach Cala d'Orsu mit Alva). Darunter „Du“: Inventar und Fähigkeiten.
- **Klick auf eine Kachel schließt das Overlay**, Duc steht am Ort: Vollbild mit Hintergrund, Figur und Gruß, links eine **Auswahlliste** (Tasten 1–n, Esc = Tschüss). Eine Wahl öffnet ein **Panel** über dem Ort mit „Zurück“.
  - Rosi: Umziehen, Chips, Verbessern · Totò: Kaufen, Verkaufen · Lola: Essen & Kochen · Megan, Alva: Kaufen.
- Kein Gespräch, keine Szene, keine Aktion. Rosis Werkstatt nutzt den Hintergrund `eden_rise_workshop.png` (ohne Lochwand).

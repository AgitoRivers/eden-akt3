# Beute und Geld · Plan zur Abnahme

> Stand 28.10.2026 · Besitz: Brain Trust · **Entwurf, nicht gebaut.** Entscheidungen Duc: E-086. Teil von
> [`expeditionen_2.md`](expeditionen_2.md) (Pilot Grotte). Messwerkzeug: `tests\expedition_sim.py`.

## Warum

Bestandsaufnahme 28.10.: Aus Kämpfen kommen nur Module und 6 Gegenstände, alles andere kauft man. Für Stufe 2 bei Rosi
gibt es kein Material (Smaragd, Rubin, Opal, Silber, Titanium sind „Drop“, aber kein Gegner hat sie; nur der Saphir
kommt von der Sirene). Geld hängt nicht vom Können ab: Der Bot hat an Tag 14 rund 4.000 €, die Gage (250 €/Tag) ist die
größte Quelle. Ziel: Wer gut spielt, kommt mit besserer Beute und mehr Geld zurück – und Geld wird wieder eine
Entscheidung.

## 1 · Die Beute-Leiter (Duc: ja)

| Stufe | Inhalt (vorhandene Gegenstände) |
|---|---|
| **gewöhnlich** | Pflaster, Kühlspray, Snacks, Zutaten für die Küche, kleine Wertsachen |
| **gut** | Bandage, Verbandskasten, Granaten, Wetzsteine, Rauchtopf, Stufe-1-Steine (Jade, Topas, Aquamarin, Amethyst), Kupfer, Steel Plate, Wertsachen |
| **selten** | Module Stufe 2, **Stufe-2-Material** (Smaragd, Rubin, Saphir, Opal, Silber, Titanium Plate – nur hier), Glücksbringer, Gegengift, wertvolle Wertsachen |
| **meisterlich** | Module Stufe 3, Unikate (ein Stück je Ort), später Charms und Teile der Masterwaffen |

**Grundchance je Kampf:** 55 % gewöhnlich · 30 % gut · 12 % selten · 3 % meisterlich, ein Stück je Kampf.

**Können = Vorteil (Duc 28.10., 1a–1c):** Jeder Bonus ist **ein Wurf mehr, das beste Ergebnis zählt**, höchstens drei
Würfe (wie Vorteil bei D&D – kein Stufensprung, der hätte bei +2 schon 45 % meisterlich ergeben).

| Würfe | selten oder besser | meisterlich |
|---|---|---|
| 1 | 15 % | 3 % |
| 2 | 28 % | 6 % |
| 3 | 39 % | 9 % |

Als Bonus zählen **nur** mindestens zwei perfekte Paraden (perfektes Ausweichen zählt gleich, z. B. bei den
Fledermäusen) und Sieg ohne Treffer (nicht Reden, nicht Schwachstelle).
**Das Spiel verrät es nirgends** – kein Grund im Kampfergebnis, kein Hinweis im Text. Man soll es spüren, wissen tut es
keiner (nur dieses Wiki). Serie und Tiefe: werden mit Expeditionen 2.0 eingeordnet.

**Beutetabelle je Gegnerart (1d, Runde 2 nach Duc 28.10.):** Menschen, Tiere (keine Edelsteine), Flieger
(Elster-Prinzip: Essen und Glänzendes, Stufe-1-Steine), Maschinen; Monster nur fester Drop. „gut“ enthält Modul Stufe 1, „selten“ = Modul Stufe 2 +
wenige Stücke, „meisterlich“ = Modul Stufe 3 + Unikat des Ortes. Die festen Drops (Halsband-Module, Riscossore,
Vampirin, Saphir) bleiben zusätzlich.
- **Stufe-2-Material kommt in keiner Tabelle vor** – nur von einzigartigen Gegnern oder aus Missionen. Heute nur der
  Saphir der Sirene; Akt 1 hat keins. Wann und wo die übrigen (Smaragd, Rubin, Opal, Silber, Titanium) kommen, ist offen
  und muss „sehr speziell“ sein (Duc).
- **Signatur-Drops** (Duc 28.10.: alle ja) – benannte Gegner geben statt „gewöhnlich“ ein festes Stück:
  Möwe auf dem Achterdeck → Lola's Biscuits (zurückbringen = kleine Szene) · Ratte in der Werkstatt → Duct Tape ·
  Fackelpirat → Smoke Pot · Alpha-Keiler → Truffle · Affe im Lager → Corsican Figs · Agenten: Kamm 7 → Shock Grenade, Kamm 8 → Flash Grenade, Umweg U2 → Water
  Grenade (sie werfen genau diese Granate im Kampf; Feuer, Erschütterung, Splitter bleiben für Akt 3; Bergerie ohne) ·
  Schmuggler → Cuban Rum · Kevins Tauben → Ocean Glitter Popcorn · Kevin → Kevin's Revenge · Unit-01 → neue
  *Unit-01 Steel Plate* (zählt wie Steel Plate).
  **Immer und zusätzlich:** Schwarzer Löwe → Steel Plate (Panzerplatte aus Alons Labor) · Old Grey → neu
  *Old Grey's Collar Tag*, den Rosi zum Modul **Calm Mind** umbaut (Familie Parade, Stufe 2, Parade-Fenster +15 %).
  Damit ist der Collar Tag nicht mehr das Unikat der Berge (offen). Bewusst ohne: Bärenjunges, Riscossore, Vampirin,
  Sirene, Wolff (Képi kommt aus der Story).
- **Küchenzutaten** (Eier, Kräuter, Fleisch, Trüffel) gehen direkt in den Küchenvorrat, nicht in die Tasche.
- **Gewichte:** Was im Kampf nützt (Pflaster, Kühlspray, Bandage, Verbandskasten, Granaten außer Splitter/Erschütterung,
  Rauchtopf, Gegengift) kommt doppelt so oft, alles andere einfach. Abnahmeseite: `docs/abnahme/beute_tabellen/` (launch `beute-tabellen`, Port 8397).

## 2 · Wertsachen je Ort (Duc: ja)

Neue Art `wertsache`: kein Nutzen außer Verkaufen, aber jede mit einem Satz Text, der den Ort erzählt. Wert = Ladenpreis,
verkauft wird zu 40 % (Totò) oder 60 % (Alva).

**Entschieden (Duc 28.10., 2a–2d alle ja):**
- 2a: Wertsachen sind eine eigene Art, nur zum Verkaufen, **nicht verschenkbar**. Geschenke bleiben für Personen.
- 2b: je Ort **3 Wertsachen + 1 Unikat**; die Grotten-Liste unten gilt.
- 2c: Das Unikat kann man verkaufen **oder** der einen Person schenken, die es liebt: großer Vertrauenssprung und
  eine kleine Szene. Wer das je Ort ist, wird mit dem Bau festgelegt.
- 2d: Die Preise sind Startwerte und werden nach dem Bau mit dem Bot gemessen.

**Grotte (Pilot):**

| Wertsache | Stufe | Wert |
|---|---|---|
| Cigarette Case with Initials | gewöhnlich | 40 € |
| Smuggler's Gold Ring | gut | 80 € |
| Schooner Coin, 1924 | gut | 110 € |
| Pearl from the Black Pool | selten | 180 € |
| The Captain's Pocket Watch (1924) – Unikat | meisterlich | 400 € |

**Berge** (Skizze): Legion Badge, Shepherd's Silver Brooch, Genoese Coin. **Unikat (Duc 28.10.): A Mazzera's Hunting
Charm** – Mondsichel aus zwei Keilerhauern mit Rabenfedern, Mondstein und rotem Faden (Bild abgenommen 28.10.), von einer Traumjägerin vor Dumenica. Kein reines Verkaufsstück, sondern ein **Charm**
zum Anhängen ([`aufruestung.md`](aufruestung.md)): **+1 Ausdauer-Punkt** auf der Leiste (8 → 9). Gehört zur
Kategorie der Verbesserungen, ist also **nicht verschenkbar** (2c gilt für Wertsachen-Unikate). Das
Charm-System ist gebaut (28.10.2026, `aufruestung.md`): Charm `mazzera` liegt in `charms.json` mit Wirkung und Bild;
der Fund gibt ihn mit der Folge `{"charm": "mazzera"}`. **Fundort (Duc 28.10.): fest** im Lager des Panthers am Ende von
Dumenicas Umweg „The Mazzera's Dream“ (`bg_u2_wahl`, bei beiden Wahlen), nicht als Zufallsdrop.
**Macchia** (Skizze): Monk's Rosary, Chalice Fragment, Pilgrim's Medal, the Abbot's Seal (Unikat).

## 3 · Geld (Duc: A + B, C nur bei Menschen)

**Gebaut (29.10.2026, Brain Trust):** Gage 125 € (`modul_eden_rise.py`, Buchungstext „Eden Group fee (probation rate)“,
Megan begründet sie in ihrer ersten Sprachnachricht `mg_tag2`), Geld-Drops nur von `mensch` je Stufe (`kaempfe.json`
`geld_drop`, `kern/kampf.geld_drop`, Zeile „<Name>'s wallet“ im Kampfergebnis, fest je Kampf), Rosi 150 € / 400 €. Tests:
`tests/test_geld.py`; Messung `tests/geld_messung.py` mit drei Spielweisen (sparsam, normal, Käufer).

**Yacht-Waren bei Totò entfernt (Duc 29.10.2026, Brain Trust 1 + 2):** Der Laden-Knopf brachte einmalig 810 € an
Tag 2–3 und danach nur noch Strafwürfe – Verwaltung statt Entscheidung. Die eine Hehlerei-Entscheidung ist jetzt das
Bordrat-Event `br_crew_kasse` („Yacht Stuff for the Crew Fund?“, Tag 3–6: 400 €, Totò +6, Chiara −8, Flag
`yachtware_verkauft`). Totò bleibt Hehler als Figur und kauft Inventar zu 40 % (Abschnitt 4).
Tasche 8 → 12 → 16 gebaut (Abschnitt 5). Noch offen: Ankauf je Laden (Abschnitt 4).

**Bestätigt (Duc 28.10., 3a–3d alle ja):** Gage 125 €/Tag, Geld nur von Menschen mit den Spannen unten, Rosi 150 € /
400 €, Zielkurve 300–800 € an Tag 14.

- **A · Gage halbieren:** 250 € → **125 €** am Tag. Die fehlenden ~2.600 € über 21 Tage kommen aus Wertsachen und
  Kämpfen.
- **C · Geld nur von Menschen:** Gegner der Klasse `mensch` lassen zusätzlich Geld fallen (lästig 10–20 €,
  gefährlich 20–40 €, tödlich/Boss 60–120 €). Tiere, Flieger, Maschinen und Monster haben kein Geld. Maschinen geben ab Tag 24 (Akt 3) stattdessen Stahl (`systeme/kochen.md`).
- **B · Sparziele, die man sieht:**

| Sparziel | Preis | heute |
|---|---|---|
| Rosi Stufe 1 | 150 € + Stufe-1-Material | 120 € |
| Rosi Stufe 2 | **400 €** + Stufe-2-Material | 240 € |
| Beutetasche Akt 2 (Rosi) | 400 € | – |
| Beutetasche Akt 3 (Megan) | 800 € | – |
| Tauchausrüstung (Woche 3, Tiefe 3 der Grotte) | ~600 € | – (mit Woche 3 planen) |

**Zielkurve (Messung nach dem Bau):** Ein Spieler, der Upgrades kauft, hat an Tag 14 etwa 300–800 € übrig statt
4.000 €; wer gut spielt und verkauft, kann sich die Tasche und Stufe 2 leisten, wer nur durchläuft, muss wählen.

## 4 · Wer kauft was (Duc: ja)

| Laden | Rolle | Kauft an | Preis |
|---|---|---|---|
| Totò (Locker) | allgemeiner Händler | alles | 40 % |
| Rosi (Werkstatt) | Schmiedin | Kampfgegenstände, Granaten, Wetzsteine, Steine, Platten, Barren, doppelte Module | 60 % |
| Lola (Kombüse) | Wirtin | Zutaten, Fisch, Snacks, Gerichte | 60 % |
| Petru (Petru's Workshop, Laden ab Tag 2) | Fischer | Fisch (Lola und Petru kaufen beide Fisch; ab wann: Brain Trust) | 60 % |
| Isabelle (Apotheke) | Alchemistin | Kräuter, Heilmittel, Naturfunde | 60 % |
| Alva (Bar, an Land) | Hehlerin für Schönes | Wertsachen, Schmuck, Alkohol, Schmuggelware | 60 % |
| Megan (Eden Shop, ab Tag 8) | Technik | Teile, Elektronik, Agenten-Technik | 60 % |
| Nonna (Farm) | Bäuerin | Saatgut, Gemüse, Tierfutter | 60 % |

**Händler nach und nach (Brain Trust, Duc 28.10.: alle 4 ja):**
1. Petru kauft Fisch **ab dem ersten Fang**, nicht ab einem Tag.
2. Lola zahlt für jeden Fisch gleich und will Qualität; Petru zahlt nach **Seltenheit** (Alltagsfisch weniger, seltene
   Fische mehr). So entscheidet man: Alltagsfisch zu Lola, Zander zu Petru.
3. Ein neuer Händler wird eingeführt, sobald man **das Passende besitzt**, mit einem Satz des Händlers – kein Tutorial-Kasten.
4. Reihenfolge: Totò → Fisch (Lola, Petru) → Alva bei der ersten Wertsache → Megan ab Tag 8.

**Fisch entdecken und verkaufen (Brain Trust, Duc 28.10.: alle 5 ja; 3 und 4 gebaut 28.10., 1, 2 und 5 offen):**
1. **Overlay bei neuer Art:** Fisch groß, Name, Sterne, Zähler „River 4/10“ / „Sea 6/10“, eigener heller Klang (3 s, keine
   Kampf-Siegesmusik). Klick überspringt, nach höchstens 3 s weg, Angeln geht sofort weiter.
2. **Gewässer voll (10/10):** größeres Overlay mit dem Sammelbonus (Lea's Lucky Lure / Petru's Cork Float), längerer Klang.
3. **Petrus Fisch-Satz:** 20 vertonte Zeilen (was der Fisch ist · was ihn besonders macht · warum er so viel zahlt), nur beim
   **ersten Verkauf dieser Art an Petru**, danach kurze Grüße. Nur Petru, nicht Lola. Quelle: `werkzeuge/eden_rise/petru_fische.py`,
   Abnahme `docs/abnahme/petru_fische/` (launch `petru-fische`, Port 8398). Petru zahlt je Stufe 50 / 65 / 80 % (Vorschlag).
   **Sätze abgenommen (Duc 28.10.)**, Lachs ersetzt die Little Tunny.
   **Gebaut (28.10.):** Petrus Werkstatt hat neben „Tools“ den Reiter **„Sell Fish“**, sobald das Fisch-Journal einen Eintrag hat.
   Er zeigt jeden Fisch im Küchenvorrat mit Anzahl und Preis; „Sell 1“ oder „All“, schlechteste Qualität zuerst. Preis =
   Rohpreis × Anteil der Stufe (`kuechen.json` `petru.fisch_anteil`) + 5 % je Vertrauensstufe Petru, dazu der Küchen-Bonus
   „Ankauf“. Beim ersten Verkauf einer Art spielt die Zeilen-Gruppe `fisch_<id>` (`laeden.json`, Schlüssel
   `laden.petru.fisch_<id>.0`), gemerkt in `z.kueche.petru_erzaehlt`. Code: `kern/abbau.py` (`fisch_ansicht`,
   `fisch_verkaufen`), Aktion `petru_fisch`, Client `eden-abbau` (`fischHtml`). Sätze ändern nur in `petru_fische.py`, dann
   `kochen_eden_rise.py`. Vertonen: `Vertonen_EdenRise.bat --praefix laden.petru.`. Vorschau: launch `petru-fisch-vorschau`
   (Port 8399, `--fische zander:2,sardine:3,salmon:1`). Test: `tests/test_abbau.py` `petru_fisch_pruefen`.
4. **Journal:** Petrus Satz wird die Notiz beim Fisch; vorher steht dort „Ask Petru about it.“ **Gebaut:** Klick auf einen
   gefangenen Fisch im Journal (J) zeigt Text und Notiz (`kuechen.json` `petru.fisch_notiz`, ohne Tags).
5. **Klänge:** zwei neue (ElevenLabs): neue Art, Gewässer voll.

**Nichts wird automatisch verkauft (4d, Duc 28.10.):** Was der Laden vor Ort nicht kauft, bleibt in der Tasche bis
zum passenden Laden – oder man verkauft es sofort billiger bei Totò. Man entscheidet immer selbst.

**Vertrauen hebt den Preis (Duc 28.10.):** **jede Vertrauensstufe +5 %** (Stufe 5 = +25 %: Fachladen 85 %, Totò 65 %;
gilt auch für Totò). Der
Küchen-Tagesbonus „Ankauf“ (Sojasauce) bleibt obendrauf. Umsetzung: Tabelle Laden → Arten in `modul_eden_rise.py`,
`kern/handel.py` `ankauf()` filtert nach Laden.

## 5 · Die Tasche (Duc: ja)

- **Eine Tasche für alles** – mitgenommene Verbandskästen und Granaten belegen Plätze, die der Beute fehlen.
- Größe je Akt: **8 / 12 / 16** (gebaut 29.10.2026). Andenken, Quest-Gegenstände und Schlüssel zählen weiter nicht.
- **Upgrades bei Rosi, nur gegen Geld (Duc 29.10.):** in ihrer Werkstatt (Reiter „Upgrade“ → Rosi, Abschnitt
  „Bag“), sofort fertig, kostet keine Aktion. Akt 2 ab Tag 8 „Rosi's Diving Bag“ (12 Plätze, 400 €), Akt 3 ab Tag 24
  „Rosi's Expedition Pack“ (16 Plätze, 800 €). Vorher zeigt die Werkstatt, warum es noch nicht geht. Daten:
  `MODUL["tasche"]` in `modul_eden_rise.py`; Code `kern/handel.tasche_kaufen`, Größe `kern/zustand.inventar_plaetze`;
  Test `tests/test_geld.py`. Bilder fehlen noch.
- **Kein automatisches Verkaufen.** Ist die Tasche voll, wählt man nach dem Kampf, was man liegen lässt.
- **Stapeln (Duc 28.10.: „ja passt alles“, gebaut):** ein Platz = ein Stapel. Gewöhnlich 5, gut 3, selten und
  meisterlich 1; Geschenke, Wertsachen, Charms, Schmuggel und Unikate nie. Was man auf einer Expedition **abbaut oder
  angelt, liegt in der Tasche** (Rohstoffe 10 je Platz, Fische 3 je Art) und wandert erst bei der Heimkehr in Zähler und
  Küche. Regeln und Tabelle: [`items.md`](items.md), Abschnitt „Stapeln“.

Messung (Modell mit der Leiter oben): Beute-Plätze je Expedition im Mittel Grotte 6 (ohne Umwege) bis 10 (mit),
Berge mit Umwegen 14, Ziel-Expedition 2.0 etwa 14 – mit 12 Plätzen in Akt 2 muss man bei langen Läufen auswählen.

## 6 · Niederlage

`kern/expedition.py`: Bei einer Niederlage bleibt aus der Beute dieser Expedition **ein Platz**, also ein Stück oder ein
ganzer Stapel (5 Pflaster, 10 Timber, die drei besten Fische einer Art; Duc 28.10.). Abgebautes und Gefangenes zählt
dabei wie jede andere Beute. Mit der Serie wird das zur echten Wette am Rastplatz: heim mit allem oder weiter.

## Bau-Reihenfolge (nach Abnahme)

1. Gage 125 €, Geld-Drops von Menschen, Ankauf je Laden mit Vertrauen, Tasche 8 → 12 → 16 mit den zwei Upgrades.
2. Beutetabellen und Wertsachen der Grotte (Pilot), Können- und Serien-Stufen, Anzeige im Kampfergebnis.
3. Messung mit `expedition_sim.py` und dem Gate-Bot: Geldkurve über die Tage, Plätze, Spieldauer.
4. Danach Macchia und Berge.

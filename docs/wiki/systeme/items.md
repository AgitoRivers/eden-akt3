# Items: Waffen, Jacken, Werkstatt, Gegenstände

> Kanon-Stand 25.10.2026 · Besitz: Items (Kampf-/Equipment-Sitzung) · Quellen: `docs/wiki/systeme/aufruestung.md`, Register E-048 bis E-052, `werkzeuge/eden_rise/kaempfe_eden_rise.py`, `gegenstaende_eden_rise.py`

## Kurz
Duc trägt immer genau **eine Waffe und eine Jacke**. Beide haben feste Namen mit englischem Untertitel, ein festes Element
bzw. eine feste Eigenschaft und lassen sich bei Rosi zweimal verbessern. Gewechselt wird nur in der Kabine, ohne Aktion.
Jede Waffe bekommt ihre Lore in einer Übergabe-Szene (E-051): wer, woher, warum der Name. Eine neue Waffe soll sich wie
ein Achievement anfühlen. Alles Spielsichtbare ist Englisch (STIL.md); die deutschen Texte hier sind Teamdoku.

## Waffen
Eine Waffe je Waffenart. Die Faust gibt es nicht. Das **Element einer Waffe ist fest** und ändert sich nie (gegen
Cheater-Builds). Rosi baut jeder Waffe eine Element-Kartusche ein (E-048): Feuer = Gas, Luft = Batterie/Strom,
Wasser = Druckwasser, Erde = Wuchtgewicht. Veredeln gibt es nicht.

| Name (Untertitel) | id | Art | Element / Kartusche | Schaden | Übergabe (Stand) |
|---|---|---|---|---|---|
| **Terremoto** (Baseball Bat) | `bat` | Stumpf | Erde, Wuchtgewicht im Lauf | 2 | **Startwaffe.** Rosi wirft sie Duc im Hafen zu, nennt und erklärt den Namen (E-049, Events `hk_rosi_*`, Flag `waffe_bat`); davor kämpft Duc mit dem Holzschrubber |
| **Le Large** (Boar Spear) | `spear` | Stange | Feuer, Gas-Kartusche | 4 | Madame Casanova, wenn Duc ihre Mission abschließt: nach dem Ortskapitel Kloster, Akt 2 (Szene in `ortskapitel_kloster.md`) |
| **Riposte** (Cavalry Sabre) | `sword` | Klinge | Wasser, Druckwasser | 5 | Geplant: Tauchgang zum Wrack, Woche 3 (`sirene_weg`). Noch nicht gebaut |
| **Sussurro** (Combat Knife) | `knife` | Messer | Luft, Batterie | 2 | Grotte, Gennaros Zelle, ab Tag 11 (`gr_zelle`, `gr_zelle_spaet`), direkt vor U Riscossore |
| **Gemelli** (Double Rifle) | `gun` | Fern (2 Slots) | **kein Element, kein Stein**; Zwillingsläufe: Erstschuss und jeder Konter nach perfekter Parade feuern beide Läufe | 3 | Holm, wenn sie vor der Belagerung zurückkommt (Duc 30.10.): ihre Familienwaffe, Duc gewinnt sie. Noch nicht gebaut |

- **Terremoto:** Name, weil die Wuchtgewicht-Kartusche jeden Treffer wie ein Erdbeben wirken lässt. Vorher hieß sie
  *Fracasso*; das klingt auf Deutsch nach Fiasko und wurde ersetzt (E-052).
- **Regel (Duc 30.10.):** Der Vorteil einer neuen Waffe wird im selben Kapitel oder kurz danach spürbar: Le Large in der Macchia, Sussurro gegen U Riscossore, Terremoto gegen Alpha-Keiler und Löwe, Riposte gegen die Banditen nach dem Tauchgang, Gemelli gegen Alons Drohnen.
- **Gemelli ist Holms Familienwaffe,** eine Doppelbüchse für Großwild. Damit soll sie den Bären „up north“ aus einem Kilometer ins Auge geschossen haben. Sie verschenkt sie nicht, sie verleiht sie, weil sie selbst noch nicht auf dem Kai stehen kann. Duc gewinnt sie in einer Schießwette, wenn Holm vor der Belagerung zurückkommt (Szenen `hb_*`, vorläufig Tag 18; Regeln in [`schiesswette.md`](schiesswette.md)). Rückgabe erst im Epilog.
- **Gemelli** bekommt ein Element nur über Erweiterungen (Feuer, Wasser, Wind, Erde), immer nur eine gleichzeitig.
- **Erste Waffe im Kampf:** Terremoto ist Erde und damit im Hafen gegen die Tiere neutral. Auch in die Macchia geht Duc
  mit Terremoto. Der Boss dort ist ein gepanzertes Monster, gegen das Stumpf besser ist.
- **Macchia-Beute:**
  - Die Ringe der Tiere sind Chips der Stufe 1.
  - **Löwe** (Beschluss Duc 26.10., E-074): Leiden beenden ergibt den Steuerchip (Missionsgegenstand, Alon-Spur) **und** den
    Löwen-Chip; den Chip herausschneiden ergibt nur den Steuerchip, der Löwen-Chip ist dann zerbrochen.
  - **Alpha-Keiler** (neu, Steinbrücke, Zwischenboss) trägt einen seltenen Chip, als Ausgleich für alle, die den Löwen verschonen.
    Vorschlag der Items-Sitzung: *Hammer Down* (Wucht, Stufe 2).
  - **Felsnische** (Schatzweg, Ortskapitel Kloster): die **erste Stahlplatte** (`steel_plate`) und ein **Zettel des Agenten**
    (`agent_note`, Key Item), der sie gestohlen und dort versteckt hat: “G. – plate stays here till you come. Thursday, the late boat from Bastia. 400 or no deal, I'm not a charity. Burn this.” (G. = Gennaro, unausgesprochen). Das ersetzt die frühere Bestückung mit Hammer Down und Jade.
  - Ambrosius' goldene Keule ist ein **Key Item** (Art `quest`, Duc 26.10.): Frederico gibt sie Duc in der Höhle, sie wird
    später wieder wichtig. Keine Waffe, keine neuen Sprites. Die Stahlplatte aus der Nische ist **Material** für Rosi.
- Waffenart und Gegnerart: Klinge und Messer stark gegen Menschen und Tiere, Stumpf gegen Maschinen und Monster, Stange
  gegen Monster, Fern als Einzige gegen Flieger (Duc 30.10.). Alpha-Keiler und Löwe sind gepanzerte Monster. Regeln siehe Kampf-Wiki (`client/wiki/kampf.html`).
- **Sprites:** `combat/Duc<Look><Sword|Bat|Knife|Spear|Gun>`, Looks Erde, Wasser, Feuer, Luft, Cyber.

## Jacken
Die Jacke gibt Duc eine **feste Eigenschaft**; der Look zeigt sie im Bild. Alle Jacken passen zu allen Waffen.

| Name (Untertitel) | id | Look | Schutz | Eigenschaft | Fundort (Stand) |
|---|---|---|---|---|---|
| **Terra Scura** (Biker Jacket) | `jacket_earth` | Erde | 3 | Standfest: Verteidigen gibt Schutz +2, Duc wird nie erschüttert | Start |
| **Meramie** (Navy Pea Coat) | `jacket_water` | Wasser | 2 | Fließend: Parade-Fenster +5 %, Konter nach perfekter Parade ×1,1 | Petru, ab Tag 8–9, in jedem Berge-Weg (`bg_a_jacke`, `bg_b_versoehnung`, `bg_c_jacke`) |
| **Incendio** (Burgundy Pea Coat) | `jacket_fire` | Feuer | 2 | Glut: +2 Schaden je Brandstufe am Gegner | Danzel, Nebenquest Red Trio (Duc 30.10.) |
| **Zéphyr** (White Pea Coat) | `jacket_air` | Luft | 2 | Leicht: Ausdauer +2, Fliehen leichter | Vorschlag Akt 2 (Megan nach der Anhörung), offen |
| **Citadelle** (Cyber Armor) | `cyber_armor` | Cyber | 5 | Alles-in-einem: Elementarschaden ×0,7, erster Treffer pro Kampf zählt halb, Parade-Fenster −10 % | nach dem ersten Sieg über Alon, kommt mit Stufe 0 ins NG+ |

Die Zahlen stammen aus der Simulation `werkzeuge/kampf_balance_v6.py`: Die vier Lederjacken liegen im Mittel knapp
zwei Punkte LP-Verlust auseinander, Citadelle ist ab Level 8 etwa vier Punkte besser. Jede Jacke hat eine Nische.

## Rosis Werkstatt
- **Ein Ort, keine Szene:** Duc öffnet die Karte (Taste M) und klickt auf Rosis Kachel. Die Werkstatt erscheint groß, Rosi grüßt, darunter die Auswahlfelder Chips und Upgrade. Umziehen passiert nur im Inventar (Taste I), außerhalb von Szenen; „Umziehen“ in der Kabine öffnet ebenfalls das Inventar.
- Öffnet, sobald Rosi sie nach dem Brand repariert hat (Flag `werkstatt_offen`, Event `rosi_werkstatt_offen`, Auslöser
  `akt2_werkstatt_bereit`). Bis dahin ist der Punkt „Für Rosi“ in der Kabine grau.
- **Zwei Upgrades** je Waffe und Jacke: +1 Schaden bzw. +1 Schutz je Stufe. **Jacken:** Steel Plate (Stufe 1), Titanium Plate
  (Stufe 2). **Waffen:** jede hat einen Basisstein eingebaut, Rosi tauscht ihn gegen einen besseren: Erde Granit → Jade →
  Smaragd, Feuer Lavastein → Topas → Rubin, Wasser Seeglas → Aquamarin → Saphir, Luft Quarz → Amethyst → Opal. **Gemelli:** Kupfer → Silber (Barren). Beschaffung und Preise stehen noch aus (Beschluss 25.10.).
- Abgabe in der Kabine, **keine Aktion**, ein Stück pro Nacht, das abgegebene Stück kann man nicht tragen. Am Morgen
  schreibt Rosi aufs Handy; die 20 Sätze (je Stück und Stufe) stehen fest in den Daten (`WERKSTATT` in
  `kaempfe_eden_rise.py`) und werden vorab vertont. Das Sprachmodell erfindet davon nichts.
- Rosis Stimme gilt auch hier: direkt und frech, ganze Sätze, knapp nur bei Technik (E-054).

## Erweiterungen
- **Aufgabe:** mehr Funktion für Waffe oder Jacke (Krit, Parade-Fenster, Schutz, Zustände …). **Plätze** je Stück 1 / 2 / 3 mit
  Rosis Stufe. Pool gehört Duc, Tausch in der Kabine, jede Erweiterung nur einmal. Keine Inventar-Gegenstände, sondern eine
  eigene Sammlung.
- **Katalog (72):** Waffen: Wucht (Hammer Time → Hammer Down → Hammerfall), Präzision (Bullseye, Dead Center, Perfect Shot),
  Technik (Quick Draw, Second Wind, Full Flow), Konter (Payback, Backlash, Reversal), Zustand (Brand Blade-Reihe, Strom,
  Blutung, Erschüttert, Nass), Element nur für Gemelli (Ember, Rain, Stone, Breeze Shell …). Jacken: Schutz (Tough, Iron,
  Dragon Coat), Parade (Steady Hands, Calm Mind, Zen Cuffs), Ausdauer, Erholung, Auftritt, Abwehr gegen sechs Zustände.
  Quelle: `werkzeuge/eden_rise/erweiterungen_eden_rise.py` (Zahlen vorläufig bis zur Simulation, Wirkungen noch nicht gebaut).
- **Scout** (Jacke, Kategorie Aufklärung, Duc 26.10.): *Radio Ear* → *Signal Hunter* → *Know Thy Enemy*. Ein umgebauter
  Halsband-Sender, der die Signale der anderen Halsbänder auffängt. Wirkt **nur in der getragenen Jacke** und belegt dort einen
  Platz. Auf Expeditionen zeigen Kampf-Wahlen sonst nur „⚔ Something is waiting“:
  - **I:** zeigt den Gegner (Kopf und Name); Tiere ohne Halsband (Ratte, Schlange) nur als „animal“.
  - **II:** dazu Level und Bedrohung. **III:** dazu die Schwäche.
  - **Herkunft:** Stufe I schenkt Rosi bei der Wiedereröffnung ihrer Werkstatt (Tag 8, alle drei Antworten) und baut ihn gleich in
    die getragene Jacke (`{"chip": ["scout", 1, "jacke"]}`; sind alle Plätze belegt, wartet er im Vorrat). Stufe II tragen die
    wilden Hunde im Rudel (`hunde_paar`), Stufe III kommt später von Agenten.
  - **Code:** `kampf.aufklaerung(z, defs)` liefert 0–3 aus `chips_aktiv(...)["aufklaerung"]`; die Anzeige baut das Plugin
    `eden-expedition`. Icon: eigenes Signal-Orange im Jacken-Wappen mit Sender und Funkbögen (`chips/radio_ear.png` …,
    `chips/kat/aufklaerung-*.png`).
- **Darstellung (Vorschlag):** gezeichnete Chips: Form = Gruppe (Waffe Raute, Jacke Wappen), Farbe = Kategorie, Rahmen =
  Seltenheit, Symbol = Wirkung; leere Plätze als Umriss derselben Form.

## Chips: Lore (Alons Experiment)
Die Erweiterungen heißen im Spiel **Chips**. Sie stammen aus Alons Halsbändern (Behaviour Control Units) und der Agenten-Technik.
Rosi schneidet den Sender heraus und baut sie um, damit sie nur Duc helfen und er sie jederzeit herausnehmen kann: dieselbe Technik,
zwei Haltungen (Kontrolle gegen Freiheit). Funde sind Schaltpläne (schalten eine Familie frei oder heben sie auf die nächste Stufe);
vor Rosis Werkstatt sind sie unidentifiziert. Tiere mit Halsband geben Stufe 1, Agenten Stufe 2, Stufe 3 kommt später aus Alons
Umfeld („Alpha“ als Platzhalter). Wendung in Akt 3 geplant (Alon nutzt etwas an den Chips aus). Details: `docs/wiki/systeme/aufruestung.md`.

## Charms (Konzept, noch nicht gebaut; kommen zuletzt)
- **Charm:** kleine Anhänger von wichtigen Figuren mit hohem Vertrauen oder nach Missionen (Plüschtiere an Jacke oder Waffe),
  verstärken Attribute. Adrien, Letizia und Federico geben keinen. Der Charm-Platz erscheint erst beim ersten Charm, im UI
  rund und versetzt.
- Die frühere „Verstärkung“ (Element oder Elementschutz zum Aufstecken) entfällt (Duc 25.10.).

## Gegenstände im Inventar
- **6 Plätze**, dazu die Truhe in der Kabine (kostenlos, beliebig oft). Was in der Truhe liegt, wirkt nicht. Andenken,
  Key Items (`quest`) und Schlüssel zählen nicht zu den Plätzen (`zustand.OHNE_PLATZ`), Besorgungen haben ihre eigene Tasche.
- **Tasche voll** (Duc 31.10.): Was die Story Duc gibt, geht automatisch in die Kabinen-Truhe („No room in your bag. X is
  waiting in your cabin chest.“), kein Menü mitten in der Szene. Item-Bedingungen (`{"item": x}`) zählen die Truhe mit,
  `item_weg` nimmt auch von dort. Boni wirken weiter nur am Mann. **Ausnahmen:** Kampf-Beute (`{"item": x, "beute": true}`)
  und alles auf einer laufenden Expedition bleiben liegen („stays behind“), sonst könnte die Truhe die Verlust-Regel einer
  Niederlage umgehen (`beute.md`). Die Nische im Kloster hat dafür eigene Zweige. Code: `zustand._ueberlauf`, Test
  `tests/test_tasche_voll.py`.
- **Stapeln** (Brain Trust + Duc 28.10.2026: „ja passt alles“): Gleiche Stücke liegen als Stapel auf **einem Platz**.
  Die Kachel zeigt die Zahl oben rechts (×3), golden, wenn der Stapel voll ist.

  | Was | Stapel | Beispiele |
  |---|---|---|
  | gewöhnlich (Consumables) | 5 | Plaster, Cooling Spray, Duct Tape, Kaffee, alle Snacks, Espresso, Energy Bar |
  | gut (Consumables, Materials) | 3 | Bandage, First Aid Kit, Smoke Pot, Wetzsteine, Spikes, Match Ammo, Feuer-/Wasser-/Schock-/Blendgranate, Steel Plate, Jade, Topas, Aquamarin, Amethyst, Kupfer, Kühlakkus, alle Gerichte |
  | selten, meisterlich | 1 | Antidote, Erschütterungs- und Splittergranate, Megaphone, Stufe-2-Material (Smaragd, Rubin, Saphir, Opal, Silber, Titanium) |
  | nie | 1 | Geschenke, Wertsachen, Charms, Schmuggelware, Unikate, Andenken und Key Items (die brauchen ohnehin keinen Platz) |
  | Abgebautes auf Expeditionen | 10 | Timber, Stone, Cork |
  | Gefangenes auf Expeditionen | 3 je Art | ein Stapel Hechte, ein Stapel Barben; die Sterne bleiben je Fisch erhalten |

  - Feld `stapel` im Modul (Builder `modul_eden_rise.py`, Listen `STAPEL_GEWOEHNLICH`/`STAPEL_GUT`), Rechnung in
    `kern/zustand.py` (`stapel`, `stapel_liste`, `belegt`, `platz_fuer`); Ernte in `kern/expedition.py`, Größen in
    `kuechen.json` `abbau.stapel` (`kochen_daten.ERNTE_STAPEL`).
  - **Kaufen:** Stapelbares darf man mehrfach kaufen. Ein Kauf in einen offenen Stapel braucht keinen neuen Platz, der
    Laden zeigt „dabei ×2“. Einzelstücke gibt es weiter nur einmal („Hast du“).
  - **Truhe:** Ein Klick bewegt den ganzen Stapel; heraus nur so viel, wie in die Tasche passt. Die Truhe bleibt unbegrenzt.
  - **Abbauen und Angeln unterwegs:** Holz, Stein, Kork und Fisch vom Rastplatz liegen in der Tasche, nicht im Zähler.
    Was nicht mehr passt, bleibt liegen bzw. schwimmt davon (das Journal zählt den Fisch trotzdem). Ist kein Platz mehr,
    zeigen die Chips am Rastplatz „🎒 bag full“, Abbauen und Angeln starten nicht, eine laufende Sitzung endet mit
    „Your bag is full“. Bei der Heimkehr (`{"expedition": "ende"}`) wird ausgepackt („Unpacked: +12 Timber, 2 fish for the
    kitchen.“). Am Boot und ohne Expedition geht alles wie bisher direkt in Vorrat und Zähler.
  - **Niederlage:** ein Platz bleibt – ein Stück oder ein ganzer Stapel (siehe `beute.md` Punkt 6). Ein Doppelfund
    (ein zweites Pflaster zu dem, das man mitgebracht hat) zählt jetzt als Beute; vorher war es sicher (Fehler behoben).
  - Kampf: die Gegenstandsliste zeigt ×n. Test: `tests/test_stapel.py`.
- **Rubriken** (Brain Trust + Duc 26.10., wie in JRPGs): Der Spieler sieht sieben Rubriken, intern bleiben die Arten.
  Jede Kachel in der Tasche trägt ihre Rubrik, die Tasche ist danach sortiert.

| Rubrik | Arten intern | Wirkung | Beispiele |
|---|---|---|---|
| Consumables | ressource, snack, gericht, kampf | verbrauchen: Moral, Energie, Reparatur, Essen, Kochen; im Kampf heilen, Ausdauer, Zustände, Gegner, Waffenpflege (18 Kampf-Items seit 27.10.2026, Tabelle in `kampf.md` „Gegenstände“) | Double Espresso · Fairy Bread · Ramen · First Aid Kit · Smoke Pot · Blue Whetstone |
| Gifts | geschenk, einzigartig | Vertrauen/Begehren nach Geschmack; Einzigartig nur für eine Person | Corsican Olive Oil · A Jar of Vegemite |
| Charms | attribut, gluecksbringer, werkzeug | +1 Attribut solange getragen / 1× am Tag Vorteil / Vorteil bei Aufträgen | Holm's Brass Compass · Binoculars · Toolbox |
| Materials | material | Rosis Material fürs Aufrüsten, wird verbraucht (Platten, Steine, Barren) | Steel Plate · Jade · Silver |
| Key Items | quest, schluessel, teil | Quest-Gegenstand (später gebraucht, nicht verkauf- oder verschenkbar), öffnet einen Ort, Besorgung | Golden Mace · Agent's Note · Triton's Trident · Key to Petru's Workshop |
| Keepsakes | andenken | keine Wirkung, Erinnerung (Keepsake Box in der Kabine) | Siri's Hairband · Propeller from Megan's Drone |
| Contraband | schmuggel | wirkt beim Benutzen, Kontrollrisiko bei Elsa | Cuban Rum · Cohiba Cigars |

- **Gras-Kuchen** (Space Cake, Brownie „Captain's Calm“) sind Snacks, aber Ferrandi findet sie auch: 10 % je Tagesende
  im Inventar, 5 % in der Truhe, Ruf −1. Essen gibt am nächsten Morgen Energie −1, im Kampf +1 Ausdauer je Runde
  (Details in `kampf.md` „Gegenstände“).

- **Ruht dauerhaft** (E-076/E-082, Diesel und Strom gibt es nicht mehr): Can of Diesel, Used Boat Battery, Solar Panel Cleaner stehen in
  keinem Laden, auch nicht in Akt 2 (`pausiert: "akt2"` in `modul_eden_rise.py`, Filter in `handel.sortiment`). Wer sie schon hat, behält sie.
- **Kleidung liegt bei Danzel (Duc 30.10.2026):** Sobald „Le Théâtre Rouge“ an der Piazza offen ist (Trio versöhnt, 3 Tage nach dem Ende der Quest), verkauft nur noch er
  Wollsocken, Wollmütze, Seidenkimono, Strümpfe und die beiden Dessous. Bis dahin und ohne Laden bleiben sie bei Totò und Alva, damit kein Geschenk verloren geht.
  Sonnenbrillen, Eden-Kappe und Augenbinde gelten nicht als Kleidung. Felder: `laeden.<id>.bedingung`, `uebernimmt` (`kern/handel.py`).
- **Intim** ist eine Geschenk-Kategorie (12 Geschenke) und im Inventar als eigene Marke „Intimate“ (rosa) sichtbar. Regel (Duc
  26.10.): **nur ab Begehren-Stufe 3**, höhere Schwellen einzelner Stücke bleiben (bis Begehren 5 / Vertrauen 4); nie vor
  anderen, nicht bei Vergebenen. Zu früh geschenkt: „überrumpelt“, Vertrauen −1. Code: `INTIM_BEGEHREN_AB` in
  `gegenstaende_eden_rise.py`, Prüfung in `handel.schenken`. Das Fußkettchen mit Muschel ist Schmuck mit Vertrauens-Schwelle 2,
  keine Intim-Kategorie.
- Kauft Duc Material bei Totò, sagt er seine „kauf_kampf“-Sätze (für Material gibt es keine eigenen).
- **Keepsake Box** (Duc 26.10.): Die Truhe in der Kabine hat zwei Leuchtpunkte, **Sea Chest** (Lager, wie bisher) im
  offenen Kasten und **Keepsake Box** auf dem Deckel. Keine neuen Hintergründe nötig.
  - Die Box zeigt jedes Andenken, das ein Event wirklich vergibt (heute 9), fehlende nur als „?“ ohne Namen. Kopfzeile
    „X of 9 found“. Kostet nichts, keine Aktion.
  - Eigene Andenken: Bild, Name, Beschreibung als leiser Gedanke (kursiv).
  - **Echo:** Taste mit dem Namen der Gebenden spielt ihre vertonte Zeile aus dem Übergabe-Event ab, tiefpassgefiltert
    und mit Hall wie eine Erinnerung. Der Satz steht klein darunter. Heute mit Echo: Shell Crown (Lea), A Photo You
    Shouldn't Delete (Rosi), Photo of Holm's First Command (Holm), Siri's Hairband (Siri), Propeller from Megan's Drone (Megan),
    Siri's Thank-You Card (Siri; neue Zeile 26.10. als Reaktion auf „Sophia's breakfast“ in `br_siris_geburtstag`).
    Ohne Echo: die zwei Tagebuchseiten und der Control Chip (Ambrosius hat keine Stimme).
  - Code: `ECHO` und Feld `vitrine` in `modul_eden_rise.py` (Builder prüft, dass jede Echo-Zeile existiert),
    `kabine.ansicht` → `vitrine`, Client `kabAndenkenHtml` / `echoSpielen`. Test in `tests/test_modell_b.py`.
  - Entfernt (Duc 26.10.): die Andenken aus Gestrandet ohne Quelle in Eden Rise (Dad's Ring Spanner, Chiara's Star Chart,
    Sophia's Notebook Page, Lea's Shell, Siri's Knot Bracelet, Festa Medal, Chiara's Hair Clip, Lea's Shell Necklace),
    Bilder im Papierkorb.
  - Foto-Andenken und der Megan-Screenshot bekommen ein Gegenstandsbild statt einer Person (Handy mit dem Bild, Abzug
    eines Fotos); `KEIN_BILD` in `item_bilder.py` ist leer.
- Bezugsquellen: Totò (Spind an Bord), Alva (Bar), Dorfladen, Eden (Megan), Geschenke und Events. Der Katalog liegt in
  `module/eden_rise/gegenstaende.json` (Quelle `gegenstaende_eden_rise.py`).
- Geschenke: Jede Figur hat Vorlieben nach Stufen (liebt, mag, neutral, mag nicht, hasst); die Lieblingsgerichte stehen auf
  den Figurenseiten.

## Klärungsliste
1. **Wer übergibt Terremoto?** E-049 sagt Rosi im Hafen. `docs/wiki/systeme/aufruestung.md` (Abschnitt „Beschluss 25.10.“) und der
   erste Tutorial-Satz sagen noch, Duc zieht den Schläger bei Maxwell hervor; E-050 ersetzt das durch das Training mit dem
   Schrubber. Die Doku muss auf E-049/E-050 nachgezogen werden.
2. **Fundorte** der Jacken Meramie, Zéphyr und der Waffen Riposte, Sussurro: noch keine Übergabe-Szene (E-051
   verlangt je eine).
3. **Akt-2-Auslöser** für die Werkstatt ist noch nicht gesetzt. Le Large hängt an Casanovas Mission (Missions-Mechanik offen).
4. ~~Englisch-Umbau der Items~~: erledigt 25.10. (f92fd7a), Deutsch steht unter `de` für das spätere Mapping.
5. **Namen der Charms und Erweiterungen** und ihre Texte stehen aus.

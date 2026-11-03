# Ortskapitel „The Silence of San Martinu“ · Macchia & Kloster

> Stand 26.10.2026 · Besitz: Hauptsitzung (Story) · **Gebaut als Frame-Kette** (`ereignisse_kloster.py`, Mechanik:
> [`systeme/interaktion.md`](../systeme/interaktion.md) „Aufträge und Orte“). Ersetzt den Entwurf vom 21.10.
> (`docs/wiki/welt/orte_drehbuch.md`, Kapitel 1). Figuren: [`figuren/kloster.md`](../figuren/kloster.md), Casanova, Rosi.
> Bilder: 13 Hintergründe `eden_rise_<ort>.png` liegen im ST-Ordner. Mechanik der Orte: `docs/wiki/welt/orte.md`
> (Frames, Spur-Uhr, Rastplätze) – die Erkundungs-Engine ist noch nicht gebaut, siehe „Offen“ unten.

## Einordnung

- **Ab Tag 4** (seit 26.10.2026, vorher Akt 2 ab Tag 8): Casanova vergibt den Auftrag in ihrem Büro, zwei Tage
  nach dem Hafenkampf. Rosis Werkstatt öffnet später (Akt 2); bis dahin sammeln sich die Chips.
- **Ton:** wholesome mit Trauer wie *Frieren*, ein Rätsel um die Tiere, Humor durch Capra und Isabelles Kräuter.
  Fredericos möglicher Tod ist der eine schwere Moment des Akts (Duc 25.10.: bleibt drin).
- **Der Faden** beginnt schon im Hafenkampf an Tag 2: Madame Casanova fragt, woher all die Tiere kommen, und
  die Ziege mit dem blinkenden Halsband entkommt in die Macchia (E-044, Flag `kloster_faden`).

## Auftakt – Casanovas Büro (ab Tag 4)

Nach dem Hafenkampf („the day after tomorrow, Monsieur, you come to my office“) steht ab Tag 4 der Ort „Madame
Casanova's Office“ offen. Im Rathaus, unter dem Porträt ihres Vaters, ohne Bühne:

> CASANOVA: “Fiora has not missed a single market day in forty years. Not one. Since the animals came: no herbs, no
> cheese, no letters from San Martinu.”
> CASANOVA: “You saw the goat, didn't you? With the light. Monsieur, I think the animals came from up there. And I think
> the monks are in trouble.”

→ **Mission „The Silence of San Martinu“** beginnt (Auftraggeberin Casanova). Duc geht mit Terremoto hinauf –
gegen die Erd-Tiere neutral, gegen den gepanzerten Boss genau richtig (stumpf).

## Der Weg (Frames)

| Frame | Ort (Bild) | Was passiert |
|---|---|---|
| 1 | Macchia-Pfad (`macchia_path`) | Ratten, Wildkräuter. Spur: Krallenspuren auf Brusthöhe in einer Korkeiche – viel zu groß für einen Hund |
| 1b | Bachufer unter der Steineiche (`creek_rest`) | **Rastplatz.** Fund: Die Asche ist noch warm, jemand saß hier vor Kurzem; am Wasser ein Zigarettenstummel, keine billige Marke (der Agent – unausgesprochen) |
| 2 | Steinbrücke (`macchia_creek_bridge`) | **Alpha-Keiler** (Zwischenboss, trägt einen **seltenen Chip** – der Ausgleich für alle, die den Löwen verschonen). Am Ufer eine tote Ziege mit einem Halsband: rotes Licht, Gravur *BCU-0417*. Ein **Chip** (Fund) – wie die aus dem Hafen. Angelplatz Fluss wird frei |
| 3 | Hirtenhütte (`shepherd_hut_ruin`) | Verwilderter Hund. Rastplatz. **Capra** wartet: die Ziege aus dem Hafen, das Halsband blinkt noch. Sie folgt Duc ab jetzt (frisst aus der Tasche, wenn man sie nicht füttert; mit Kräutern findet sie Trüffel). Ihr Halsband schneidet Rosi später auf |
| 4 | Klostertor (`monastery_gate`) | Nonna Fiora auf der Mauer, Kochlöffel: “Stand still, or I'll cook you!” – Isabelle: “Nonna! He's a person.” – “So are the monkeys, apparently.” Capra meckert, das Tor geht auf |
| 4b | Klosterküche (`monastery_kitchen`) | Die Geschichte (unten). Ab hier **Nonna Fioras Hof** und **Isabelles Apotheke** nutzbar. Schnellreise-Punkt markiert |
| 5 | Waldgrenze (`forest_edge_cliffs`) | Affe mit Halsband (Chip). **Tagebuchseite 1** von Bruder Ambrosius |
| 6 | Schlucht, Gabelung (`ravine_fork`) | Zwei verwilderte Hunde. **Spur-Uhr startet (4 Segmente).** Links: Blutspur und eine kleine Sandale (−1). Rechts: Glitzern in einer Felsnische (−3, über 6b) |
| 6b | Felsnische (`hidden_rock_niche`, Schatzweg – oder später) | Wildschwein + Affe. In der Nische: die **erste Stahlplatte** fürs Jacken-Upgrade und ein Zettel des Agenten, der sie geklaut und hier versteckt hat: *“Plate stays here until G. pays. Bastia, Thursday. Not a euro under 400.”* (G. = Gennaro, Totòs Cousin – unausgesprochen) |
| 7 | Lager der Brüder (`monks_camp_abandoned`) | Gefaltete Kutten, ein umgestürzter Kessel, Stille. **Tagebuchseite 2.** Rastplatz (Uhr läuft weiter). Affe im Hinterhalt |
| 7b | Feuer über der Schlucht (`ravine_fire`) | **Rastplatz** gegenüber der Höhle. Spur offen: das Feuer brennt noch – „sie müssen ganz nah sein“. Spur abgelaufen: kalte, tagealte Asche (fair, kein „knapp verpasst“) |
| 8 | Löwenbau (`lion_den_cave`) | **Boss: der Löwe** – abgemagert, mit Panzerplatten aus Alons Labor an Schultern und Flanken, im Nacken ein rotes Licht im Takt seines Atems. Stumpf (Terremoto) wirkt gegen die Platten |

**Die Geschichte in der Küche (4b):** Vor Wochen kamen die Tiere – Affen, Hunde und *er*, ein Löwe, auf Korsika. Sie
griffen an, als hätten sie Schmerzen. Abt **Bruder Ambrosius** zog mit den Brüdern los, um den Löwen zu erlegen.
**Frederico** (12, Waisenjunge, schnitzt jedem ein Tier aus Holz) lief ihnen nach. Keiner kam zurück.

> NONNA: “He carves everyone who lives here an animal. He wanted to do something important, just once.”
> NONNA: “He's been gone three days. Three days with no bread.”

So weiß die Spielerin, dass Zeit zählt – Fredericos Tod darf sich nie wie eine Falle anfühlen. An der Gabelung ist die
Spur-Uhr sichtbar.

Duc antwortet mit Haltung (Mut / Wahrnehmung / List – List verrät den Lagerplatz und spart Frame 5).

**Tagebuch:**
- Seite 1: *“The animals don't flee from us. They flee from something inside themselves.”*
- Seite 2: *“I have seen the lion. He wears something on his neck that blinks. He suffers, as we do. If we kill him,
  we kill a victim. If we don't, the children in the valley die.”*

## Nach dem Kampf

Der Löwe liegt am Boden und atmet schwer. Anders als bei den anderen Tieren ist sein Chip mit dem Nacken verwachsen –
das Halsband bricht nicht von selbst. **Die einzige Entscheidung über Leben und Tod in diesem Kapitel** (E-073):

| Wahl | Folge |
|---|---|
| **Sein Leiden beenden** (so wollten es die Mönche) | Steuerchip + der starke **Löwen-Chip** |
| **Den Chip herausschneiden** (Tagebuch: “we kill a victim”) | Der Löwe flieht in die Macchia; der Löwen-Chip zerbricht, der **Steuerchip** bleibt als Beweis. In **Akt 3** taucht der Löwe wieder auf und hilft gegen den Agentenchef (Agent Alpha) |

**Steuerchip** (Missionsgegenstand, kein Kampf-Chip): Gravur *“A.V. Estates – Behaviour Control Unit”* – die erste
Spur zu Alons Anwesen. Rosi erkennt später dieselbe Bauart wie in den Halsbändern.

**Ausgang A – Fährte gefolgt (Uhr nicht abgelaufen):** Hinter einem Felsen versteckt sich Frederico, eine viel zu große
goldene Keule in den Händen.

> FREDERICO: “Are you… are you a person?” – DUC: “With a goat.”
> FREDERICO: “Brother Ambrosius said I should hide and wait until someone good came. This was his. He would have
> wanted you to have it.”

→ **Ambrosius' Keule** (Andenken, keine Waffe) und seine Habseligkeiten.

**Ausgang B – Schatz zuerst (Uhr abgelaufen):** Hinter dem Felsen liegt Frederico, die Holzziege in der Hand, neben ihm
Bruder Ambrosius. Die Keule liegt bei Ambrosius. Kein Wort, keine Übergabe.

## Zurück im Klostergarten (`monastery_garden_dusk`)

**Mit Frederico:** Er rennt los, Isabelle fängt ihn auf, Nonna setzt sich ganz langsam auf die Mauer.

> NONNA: “And the brothers?” – DUC: “None of them.”
> NONNA: “Ambrosius always baked his bread too dark. Brother Paolo snored while he prayed. Brother Teo greeted the
> bees every morning, one by one, by name. …Thank you for bringing the boy home.”

→ Vertrauen Nonna Fiora und Isabelle **+1 Stufe**. Frederico wird **Botenjunge** und bringt jeden Morgen die Ernte an
Bord; er grüßt jede Stewardess mit Namen.

**Ohne Frederico:** Isabelle nimmt Duc die Holzziege aus der Hand und sagt nichts. Nonna geht ins Haus und schließt
die Tür. → Vertrauen beginnt bei **0**; die Ernte bringt ein namenloser Bote aus dem Dorf.

**In beiden Fällen:** Schnellreise zum Kloster frei, Steuerchip im Gepäck.

## Abschluss bei Casanova – Le Large (Duc 25.10.)

Duc meldet sich am Hafen zurück. Casanova hört zu, ohne eine Rede zu halten – das allein zeigt, wie ernst es ist.
Dann holt sie aus ihrem Haus einen alten Jagdspeer mit Messingkartusche: **Le Large**, die Saufeder.

> CASANOVA: “My father carried this when the boars came down into the village, the winter I was born. He named it
> after the open sea, because he always said that's where courage comes from. You bring our news down from the
> mountain. You should carry it now.”

Die Zeile davor hängt an Frederico:
- **lebt:** “The boy brings the harvest down now? Then the mountain is breathing again.” – Le Large als Dank.
- **tot:** “Then we carry them in our names. All of them.” – Le Large als Trost, leiser.

→ **Le Large** (Saufeder, Feuer) – Übergabe-Szene als Achievement (E-051). Mission abgeschlossen, Vertrauen
Casanova +1 Stufe, Ruf im Dorf +1.

## Rasten

Fünf Rastplätze mit Fund-Karte beim ersten Erreichen (Kampf-Mechanik, `systeme/interaktion.md`): Bachufer (1b), Hirtenhütte (3, frisch gefegt, Holz für die Nächsten), Nonnas Küche (4b, ein zweiter Stuhl am Herd, das Kissen platt gesessen), Lager der Brüder (7, Steinkreis mit einem kleinen Stein abseits – Fredericos Platz), Schluchtfeuer (7b). Rückweg-Sperre hinter Küche, Gabelung und Löwe.

**Balance (Simulation 26.10., 200 Läufe je Stufe, Duc Level 2):** Mit der Küche als Rastplatz erreichen den Löwen auf der Fährte 98/91/62 % (gute/mittlere/schwache Parierer) und besiegen ihn 96/76/41 %. Der Schatzweg bleibt bewusst härter (Duc: Felsnische bleibt schwer): 92/64/18 % bis zum Löwen. Ohne Küchen-Rast lag die Fährte bei 88/64/26 %. Werkzeug: `werkzeuge/kampf_sim_kette.py` (Kampf-Sitzung).

## Später wiederkommen

Nach dem Kapitel bleibt die Macchia ein Ort, den Duc in einer freien Phase wieder besuchen kann: Die Frames 1–7 haben
neue Tiere (ihre Ringe sind Chips, Doppelte verkauft er), man kann **leveln** und die **Felsnische** nachholen – wer
beim ersten Besuch Frederico gerettet hat, findet die Stahlplatte so später. Der Löwenbau ist leer (oder, wenn der Löwe
lebt, nur seine Spuren).

## Graue Entscheidungen (E-073: mindestens eine je Auftrag)

1. **Fährte oder Schatz** an der Gabelung – Frederico oder die Stahlplatte.
2. **Der Löwe** – sein Leiden beenden oder den Chip herausschneiden.

## Was das Kapitel verwebt

- **Alon:** Steuerchip + Halsbänder → Spur zu seinem Anwesen (Akt 2/3), Casanovas Groll gegen ihn; der Löwe (wenn er
  lebt) als Verbündeter in Akt 3.
- **Totòs Geheimnis:** der Agenten-Zettel („until G. pays“) – eine weitere Spur zu Gennaro, ohne etwas zu verraten.
- **Chips:** Die Ringe der Tiere sind die Chips aus der Items-Lore; Rosi schneidet die Sender heraus.
- **Capra:** wiederkehrende Begleiterin; ihr Halsband ist ein eigener kleiner Rosi-Moment.
- **Küche:** Nonna Fioras Hof (Zutaten, Anbau, Tiere), Isabelles Apotheke.

## Offen

- **Gebaut (26.10.):** Auftrag + Ort „The Macchia“, 25 Frames (`kl_*`) mit beiden Ausgängen, Spur-Uhr, Felsnische
  (auch später, volle Tasche → Platte wartet), Löwen-Wahl, Garten mit/ohne Frederico, Casanova mit Le Large
  (`waffe_spear`), Wiederkommen. Annahme: Pflicht-Event `kl_casanova_auftrag` an Tag 8 mittags am Hafen.
- **Noch nicht:** Rastplätze (Heilen gegen Uhr-Segment), Nonna Fioras Hof und Isabelles Apotheke als Läden,
  Schnellreise, Frederico als Botenjunge, Capra als sichtbare Begleiterin (Flag `capra_dabei` ist gesetzt), echte
  Erkundung (freie Wege statt Kette).
- **Löwen-Chip** (nur „Leiden beenden“): Familie `auftritt`, Stufe 2 – „Cool Smile“ (Items 26.10.). Der Alpha-Keiler
  droppt „Hammer Down“ (Wucht 2) selbst im Kampf, die Frames vergeben ihn nicht noch einmal.
  Der Steuerchip ist ein Andenken (`control_chip`), kein Fall-Beweis.
- **Missions-Mechanik:** beschlossen (E-074) – Aufträge mit Annahme, Schritten und Abschluss, Journal im Menü; das
  Kloster wird zuerst als Frame-Kette gebaut (im Format der späteren Erkundung).
- Chips für Alpha-Keiler und Löwe, Stahlplatte + Agenten-Zettel als Gegenstände (Items); Gegner-Daten Level 1–7 (Kampf).
- Sprites: Nonna Fiora, Isabelle, Frederico und alle Kampf-Gegner liegen bereit; **Capra als Begleit-Figur fehlt**,
  ob „LionAlpha“ schon Panzerplatten trägt, prüft die Kampf-Sitzung.

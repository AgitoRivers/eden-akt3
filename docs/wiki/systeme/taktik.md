# Taktik-Karte · Belagerung (Tag 21–23)

> **Sechs Wellen auf drei Tage (Duc 01.11.2026, E-114).** Im Kalender ist jede Welle eine eigene Karte mit eigener Aufstellung. Der Ablauf steht in [`../welt/belagerung.md`](../welt/belagerung.md). Ältere Abschnitte unten sprechen noch von drei Wellen: Die „zweite“ ist heute Welle 4, die „dritte“ Welle 6.

## Der Stand zwischen den Wellen (Duc 01.11.)

`kern/belagerung.py`, gespeichert in `z["belagerung"]`.

- **Was bleibt:** Kirchenleben, Yacht, abgebrannte Häuser, Aufstellung, Supportwahl, Machtleisten.
- **Am selben Tag:** Trupps bekommen 40 % zurück, Duc 60 %, Gefallene stehen mit der Hälfte wieder auf.
- **Am neuen Tag:** Alle sind wieder voll, Rethink steht wieder auf 2. Rethink gilt also je Tag, nicht je Schlacht.
- **Neustart einer Welle:** Die Kirche hat danach mindestens 2 Leben, sonst wäre die Welle kaum zu schaffen.

## Schäden, Bestandsaufnahme und Flicken (Duc 01.11.)

**Je schlechter gespielt, desto mehr geht kaputt.** Fehler einer Welle sind: Treffer auf Kirche und Yacht, gefallene Trupps, verlorene Häuser, Runden über dem Soll der Welle (`par`). Ab 2 Fehlern bricht eine Barrikade, ab 5 beide, zuerst die Front mit den meisten Gegnern.

| Baustelle | Kosten | Wirkung |
|---|---|---|
| Barrikade Süd oder West | 4 Timber | Heil verliert jeder Gegner dieser Front in der ersten Runde einen Zug |
| Kirchentür | 2 Timber, 2 Stein | Ein Leben zurück |
| Yacht | 3 Timber, 1 Stein | Ein Punkt zurück |
| Abgebranntes Haus | 3 Timber, 3 Stein | Nur notdürftig, im Wiederaufbau startet es auf Stufe 1 (`tk_haus_geflickt_<id>`) |

Stein ist Slate oder Granite, Slate wird zuerst genommen. Das Dorf bringt jeden Morgen 4 Timber und 2 Stein, damit niemand hängen bleibt.

**Flicken selbst:** dasselbe Ring-Minispiel wie beim Holz und Stein (`client/plugins/eden-abbau`). Drei gute Schläge schließen die Arbeit ab, höchstens drei Arbeiten am Morgen. Jeder perfekte Schlag spart 1 Timber, höchstens 2. Wer abbricht, bekommt das Material zurück.

**Petrus Trupp:** ohne Minispiel und ohne Grenze, kostet 2 Timber mehr.

Die Bretter im Minispiel sind ein Platzhalter, bis es Bilder gibt. Alle Zahlen sind erste Werte, der Spieltest legt sie fest. Vorschau: launch `eden-flicken` (Port 8447).

> Stand 31.10.2026 · Besitz: Brain Trust · **Prototyp, spielbar in der Vorschau, noch nicht im Kalender.** Entscheidung E-102, Drehbuch in
> [`../welt/belagerung.md`](../welt/belagerung.md). Quelle: `kern/taktik.py` (Regeln), `client/plugins/eden-tactics` (Bildschirm),
> `werkzeuge/eden_rise/taktik_eden_rise.py` → `module/eden_rise/taktik.json` (Raster, Trupps, Wellen, Szenen), Test `tests/test_taktik.py`.
> Vorschau: launch `eden-taktik` (Port 8378), `tests/vorschau_server.py --taktik`, mit `--flags kl_loewe_frei` für Mochi.

## Worum es geht

Duc schiebt Trupps über eine Karte der Bucht wie in *Fire Emblem*. Blaue Figuren gehören zu ihm, schwarze sind Feinde, die weiße ist Mr. White. Die meisten Figuren sind vorläufig eckige CSS-Marken. Mr. Maximum ist die erste Pixel-Figur (Duc 31.10.): Beim Stehen atmet er mit sechs Bildern, beim Ziehen läuft er mit zwölf Bildern zum Ziel. Die Team-Farbe steckt in der Bodenplatte, wer gehandelt hat, wird grau und steht still. Neue Figur: Blätter nach `module/eden_rise/taktik/quellen/<name>.png` und `<name>_stand.png`, in `FIGUREN` von `werkzeuge/eden_rise/taktik_figuren.py` eintragen, Werkzeug starten, das Feld `figur` im Builder setzen. Die Oberfläche folgt [`ui_stil.md`](ui_stil.md).

## Ablauf

1. **Aufstellung:** Seitenleiste links, die Karte bleibt frei. Oben die Trupps mit dem Gesicht des Truppenführers, Holms Vorschlag steht schon auf der Karte. Zeile oder Figur auf einen eckigen Platz ziehen (Duc 31.10.), 13 Plätze an den Fronten West, South, Church und Yacht. Liegt dort schon ein Trupp, tauschen beide. Klicken geht auch. Darunter die Support-Plätze, unten die Bürgerwehr (Pascal, Petru, Alva), grau und fest. Fährt man mit der Maus über eine Figur, steht ihre Beschreibung unten in der Leiste.
2. **Runde, Ablauf wie Fire Emblem (Duc 31.10.):** Trupp wählen: helle Felder zeigen die Bewegung, rote, wohin er von dort noch schlagen kann. Trupp auf ein helles Feld ziehen oder anklicken, ein zweiter Klick auf den Trupp lässt ihn stehen. Danach kommt das **Aktionsmenü** neben der Figur: Attack, großer Moment, Rescue, Wait, Back. Bei *Attack* zeigen rote Felder die Reichweite, Ziele pulsieren. Ein Klick zeigt die Vorschau, ein zweiter Klick oder *Attack* greift an. Esc geht immer einen Schritt zurück. Treffer sind sichtbar: Nahkämpfer stoßen vor, Fernkämpfer feuern einen Schuss, Chiaras Taser zuckt blau, das Ziel zuckt, die Zahl steigt auf. Ziel wählen, Vorschau lesen, *Attack*. *Undo* nimmt den Zug zurück, solange nicht angegriffen wurde. *End round* lässt die Feinde ziehen. Gestrichelte Linien zeigen vorher, wohin jeder Feind will.
3. **Drei Wellen:** Süden, Westen und Osten. Die dritte beginnt mit Pascals Verrat, Mr. White kommt von Norden.

## Regeln

| Regel | Wirkung |
|---|---|
| **Raster** | 48x32 Felder. Wasser, Dächer, Felsen sind gesperrt, Drohnen fliegen darüber |
| **Crew-Kampf** | fest berechnet, ohne Würfel: Schaden = Angriff × Stärke − Abwehr − Gelände |
| **Stärke** | dieselbe Tabelle wie im Kampf (`kern/kampf.py`): ×1,5 stark, ×0,67 schwach |
| **Duc** | Sein Angriff öffnet den echten Kampfbildschirm. Sieg: Der Feind ist weg |
| **Ducs Leben** | laufen über die Karte weiter. Feinde treffen ihn auch auf der Karte, zwischen den Wellen kommen 60 % zurück |
| **Kirche** | 3 Leben, jeder Feind auf einer Kirchentür zieht je Runde 1 ab, Mr. White schon daneben |
| **Niederlage** | Kirche gefallen oder Duc bei 0 Leben: Neustart am Beginn der aktuellen Welle |
| **Mr. White** | Nur Duc kann ihn stoppen. Verliert Duc gegen ihn, beginnt der Kampf direkt neu. Sieg beendet die Belagerung |

**Eigenschaften:** Mr. Maximum schlägt auf Mole und Yacht doppelt zurück („Holds the Gangway“) und ist mit „Stumpf“ gegen Roboter stark. Chiara hat zwei Felder Reichweite. Wolff schlägt einmal je Runde zuerst zu.

## Gelände und Einheitenarten (Duc 31.10.)

Stadt, Plätze, Gassen und Wege sind freies Feld, der Strand auch, Häuser und Wasser sind gesperrt. Taste **T** färbt das Gelände ein, die Zeile unter dem Kopf erklärt das Feld unter der Maus.

| Gelände | Abwehr | Besonderes |
|---|---|---|
| Freies Feld | 0 | kein Schutz |
| Wald | +1 | versteckt Trupps: Feinde sehen sie erst ab 2 Feldern, Drohnen immer |
| Berg | +2 | sehr langsam, Roboter kommen nicht hinauf |
| Strand | 0 | Schwere und Roboter sinken ein |
| Kirchentreppe | +1 | direkt vor den Türen |

Laufkosten je Feld (`gang` in `taktik.json`):

| Gang | Frei | Wald | Berg | Strand | Wer |
|---|---|---|---|---|---|
| Fuß | 1 | 2 | 3 | 1 | Agenten, Crew |
| Schwer | 1 | 2 | 4 | 2 | Mr. Maximum, Brutes |
| Tier | 1 | 1 | 2 | 1 | Hunde |
| Maschine | 1 | 3 | gesperrt | 2 | Roboter |
| Flug | 1 | 1 | 1 | 1 | Drohnen, auch über Häuser und Wasser, ohne Geländeschutz |

**Typische Werte:** Drohnen haben Bewegung 11, Abwehr 0 und Reichweite 2. Roboter sind die Tanks mit Bewegung 4 und Abwehr 6. Agenten liegen mit Bewegung 6 und Abwehr 2 in der Mitte.

## Kampfregeln (Duc 31.10.)

- **Break:** Ein starker Treffer verhindert den Gegenschlag, Mr. Maximum nimmt also Roboter ohne Antwort auseinander.
- **Ausschnitt je Welle:** Im Kalender ist nur der Teil der Karte offen, den die Welle braucht, der Rest ist abgedunkelt und niemand läuft hinein. Wellen 1 und 3 (Süd und West): x 3–33, y 7–24. Wellen 2, 4, 5 (bis zur Yacht): x 3–44, y 5–25. Letzte Welle (auch Norden): x 3–44, y 3–26. Der Ausschnitt passt ganz ins Fenster, Scrollen ist nicht nötig, hineinzoomen geht weiter (Mausrad, Taste Z). Die Feinde aus dem Westen starten dafür bei x 4–6 statt am Kartenrand.
- **Wunden im echten Kampf:** Greifen Duc oder Mr. Maximum einen angeschlagenen Gegner an, beginnt der echte Kampf mit demselben Anteil seiner LP, Mr. White immer voll. Fällt Mr. Maximum, behält der Gegner auf der Karte den Stand aus dem Kampf.
- **Doppelangriff:** Erreicht ein zweiter Trupp das Ziel auch, schlägt er kostenlos mit, mit halbem Schaden, ab Vertrauen 3 mit drei Vierteln. Die Vorschau nennt ihn. Greifen Duc oder Mr. Maximum an, schlägt der Trupp zuerst zu und der echte Kampf beginnt mit einem angeschlagenen Gegner, außer gegen Mr. White. Auch Feinde schlagen zu zweit: Ein zweiter Feind, der das Ziel erreicht, schlägt mit halbem Schaden mit, jeder höchstens einmal je Runde, Mr. White nie (Duc 01.11.).
- **Posten je Welle (Duc 01.11.):** Aufstellen kann man nur an den Fronten dieser Welle und an der Kirche. Ohne Front zur See (Welle 1 und 3) gibt es vier statt sechs Trupps, die übrigen Reserve-Trupps gehen von der Karte. Holm stellt um, wer auf einem ruhigen Posten stand, zuerst an eine Front ohne Trupp. Kommen wieder Boote und steht niemand an der Mole, gehen Mr. Maximum und Chiara zurück dorthin.
- **Support (Duc 01.11.):** Die Aufstellung zeigt je Person, was sie kann, wie oft, und ob sie fest dabei ist. Bringt sie in dieser Welle nichts, steht es dort, etwa Lea ohne Boote oder Ligeia ohne Piraten. Die Kamera bleibt nach einem Angriff beim Angreifer, bis die Treffer durch sind.
- **Bedrohung:** Die Vorschau spielt den echten Gegnerzug auf einer Kopie. Durchgezogene Linie mit Zahl heißt, das trifft in diesem Zug genau so. Gestrichelt heißt, der Feind ist noch unterwegs. Taste **R** zeigt alle Felder in Feindreichweite, ein Klick auf einen Feind nur seine.
- **Zwischen den Wellen:** Duc bekommt 60 % Leben zurück, die Crew 40 %, gefallene Trupps stehen mit der Hälfte wieder auf. Die Bürgerwehr nicht.
- **Inszenierung vor der Welle (Duc 02.11.2026, Vorbild Fire Emblem):** Erst Titelkarte mit Tag, Welle und Ziel, dann das Briefing (`briefing` in taktik.json): Wer spricht, steht groß im Bild, die Kamera fährt zu dem, wovon die Rede ist, die Feinde leuchten (`zu`, `zeigt`). Danach kommt die Aufstellung, die Feinde stehen dabei halbdurchsichtig auf der Karte, die Zahl sind die Runden bis zur Landung. Fehlt die verdiente Reserve (`wenn`), spricht Mr. Maximum. Skip mit Esc. Am Zugbeginn zeigt ein Band Runde und „Your Turn“. Die letzte Welle hat kein Briefing und zeigt nichts vom Norden: Titel und Ziel kommen erst nach Pascals Verrat. Beim Neustart gibt es nur einen Satz von Holm mit Tipp (`kurz`).
- **Megan (Duc 02.11.2026):** Ab dem Kriegsrat ist sie nicht erreichbar und spricht auf der Karte nicht, sie kommt erst in Akt 3 zurück. Die Warnung vor Mr. White gibt ohne Danzel Holm, mit Megans Akte von vorher.
- **Neuer Versuch (Duc 02.11.2026):** Nach jeder Niederlage in einer Welle kommen die Feinde 15 % schwächer, höchstens dreimal: weniger Leben als voll, schwächerer Schlag, auch im Nachschub und im echten Kampf. Mr. White und Pascal nicht. Die nächste Welle kommt wieder voll.
- **Balancing (Duc 02.11.2026):** Gegner je Welle mit Nachschub 7, 8, 8, 11, 10, 10. Soll-Runden 5, 8, 7, 9, 9. Kobra und Skorpion kommen von Süden, Westen und Norden, für Welle 5 und 6 gibt es einen Nordposten auf Feld 28,11. Rechnung: `python tests/sim_belagerung.py [Läufe]`, spielt alle sechs Wellen mit vier Spielertypen. Der echte Kampf ist dort geschätzt und Support spielt nicht mit, die Zahlen zeigen also nur die Richtung.

## Aufgaben je Welle (Duc 31.10.)

- **Yacht:** 3 Leben. Roboter an Bord bleiben dort und ziehen ihr je Runde 1 ab, egal wie viele es sind. Steht ein Trupp bis 3 Felder an der Yacht, kämpfen sie gegen ihn statt gegen die Yacht. Holms Vorschlag schützt sie deshalb von Anfang an, wer Mr. Maximum und Chiara abzieht, riskiert sie. Ist sie zerstört, läuft die Schlacht weiter: Die Roboter marschieren zur Kirche, Lola kann nicht mehr heilen, und beim Sieg gilt das Flag `tk_yacht_weg`. Die Folgen für Akt 3 sind offen.
- **Nachschub:** Jede Welle hat Boote, die erst später kommen. Die Felder sind vorher mit einem Countdown markiert, oben steht „Boats in N“. Eine Welle endet erst, wenn auch sie besiegt sind.
- **Welle 2, Feuer und Rettung:** Vier Häuser brennen (Post Office, Ba Tu's Shop, Alva's Bar, Petru's Workshop) und haben einen Countdown. Ein Fackelpirat bis zwei Felder daneben lässt ihn doppelt so schnell laufen. Ein Trupp neben dem Haus holt die Leute heraus, das kostet seine Aktion. Ein abgebranntes Haus setzt das Flag `tk_haus_weg_<id>`, die Folgen für Akt 3 sind noch offen. Sind alle Feinde weg, löscht das Dorf den Rest selbst.
- **Welle 3, Mr. White:** Er geht langsam (Bewegung 2) und ist unbesiegbar, bis Petrus Trupp in Runde 6 gefallen ist, sonst würde man das Drama überspringen. Erst danach kommt Casanova und erst dann kann Duc ihn angreifen. Trupps können ihm die Gasse versperren.

## Verdiente Trupps (Duc 31.10.)

Höchstens sechs Trupps stehen auf der Karte. Duc, Mr. Maximum, Chiara und Wolff sind da, in der Leiste stehen zusätzlich die verdienten:

| Trupp | Frei durch | Stärke |
|---|---|---|
| Elsa | Vertrauen 2 | Pistole, zwei Felder Reichweite, einzige Crew stark gegen Drohnen |
| Rosi | Vertrauen 2 | Hammer, stark gegen Roboter |
| Yamamoto | Vertrauen 2 | Katana, trifft hart, hält wenig aus |
| Bibi | `rt_ausgang_alle` | Blend- und Wassergranaten, zwei Felder Reichweite |

Reserve-Trupp auf einen freien Platz ziehen, „Bench“ nimmt ihn zurück. Auf einem besetzten Platz ersetzt er nur einen anderen Reserve-Trupp. Vorschau einer Welle direkt: `tests\vorschau_server.py --taktik --taktik-welle 2`.

## Dreieck und Verhalten der Feinde (Duc 31.10.)

**Stein, Schere, Papier in beide Richtungen:** Schnell schlägt Fernkampf, Fernkampf schlägt Schwer, Schwer schlägt Schnell. Vorteil ×1,25, Nachteil ×0,8, dazu bei Trupps weiter die Waffen-Tabelle. Wer im Vorteil trifft, bekommt keinen Gegenschlag, das gilt auch für Feinde.

| Rolle | Trupps | Feinde |
|---|---|---|
| Schnell | Wolff, Yamamoto | Agent (Nahkampf), Fackelpirat, Buenaventura, Hund, Cobra Robot, Scorpion Robot |
| Fernkampf | Chiara, Elsa, Bibi, Alva (fest) | Marksman (Valentina, Agentin mit Gewehr), Pirate Gunner, Drohne |
| Schwer | Mr. Maximum, Rosi, Minicu (fest) | Brute, Pirate Brawler, Boarding Robot, Heavy Boarding Robot |

Duc und Mr. White stehen außerhalb des Dreiecks.

| Feind | Verhalten |
|---|---|
| Agent | geht auf den nächsten Trupp |
| Hund | jagt den Verwundetsten in Reichweite |
| Marksman | hält drei Runden die Stellung, außer ein Trupp kommt in seine Reichweite |
| Fackelpirat (Torch Pirate) | läuft zu den brennenden Häusern, sonst wie Agent. Sein echter Kampf ist der bekannte Fackelpirat |
| Brute | ignoriert Trupps und geht zur Kirche |
| Roboter | bleibt an Bord und zerlegt die Yacht, sonst nächster Trupp |
| Drohne | sucht die dünnste Rüstung und sieht Versteckte |

## Eigenschaften der Trupps (Duc 31.10.)

| Trupp | Eigenschaft |
|---|---|
| Mr. Maximum | Holds the Gangway: schlägt auf Mole und Yacht doppelt zurück |
| Chiara | Taser Rifle: Getroffene setzen eine Runde aus |
| Wolff | First Strike: schlägt einmal je Runde zuerst, wenn er angegriffen wird |
| Elsa | Overwatch: schießt einmal je Runde zuerst, wenn ein Feind in Reichweite kommt |
| Rosi | Knows the Machine: Die Rüstung von Robotern zählt bei ihr nicht |
| Yamamoto | Clean Cut: Besiegt er sein Ziel, darf er einmal je Runde nochmal |
| Bibi | Light and Water: Ein Hund, den sie trifft, setzt eine Runde aus. Ihre Wassergranate gibt einem brennenden Haus bis zwei Felder drei Runden mehr und kostet ihre Aktion |
| Duc | kämpft im echten Kampfbildschirm |

## Kamera und Bedienung (Duc 31.10.)

Die Schlacht startet in der Nahansicht. Mausrad zoomt, Karte mit der Maus oder den Pfeiltasten schwenken, **Z** zeigt die ganze Karte. Beim Gegnerzug zoomt das Bild kurz heraus und kehrt danach zum nächsten Trupp zurück, **F** macht ihn 2x oder 4x so schnell. **Tab** springt zum nächsten Trupp, nach einer Tat steht er automatisch bereit. Haben alle gehandelt, beendet **Enter** die Runde. Die Runde endet bewusst nicht von selbst, damit man Holms Befehl noch nutzen kann. Fährt die Maus über eine Figur, zeigt eine Infokarte Werte, Rolle und Verhalten.

## Fernkampf (Duc 31.10.)

Wer aus der Ferne kämpft, schlägt direkt daneben nicht zurück: Man muss also gezielt zu ihm vorstoßen. **Schusslinie:** Häuser halten Schüsse auf, auch die der Feinde. Drohnen schießen und fliegen darüber, Mr. White und Nahkämpfer betrifft es nicht. Ein Schütze ohne freie Linie geht beim nächsten Zug dicht heran.

| Einheit | Reichweite | Besonderes |
|---|---|---|
| Alva (Bürgerwehr, fest) | 2 | Flinte ihres Vaters (Duc 01.11.). Schießt in der Feindphase auf den ersten Feind in Reichweite |
| Marksman (Feind) | 3 | Abwehr 1, Bewegung 5. Wald versteckt dich vor ihm, denn Feinde sehen dort nur 2 Felder weit |
| Kampfdrohne (Feind) | 2 | fliegt |
| Chiara | 2 | Taser-Gewehr von Rosi: Wer getroffen wird, setzt eine Runde aus, auch beim Doppelangriff. Roboter und Mr. White nicht. Wenig Schaden (Angriff 7) |
| Elsa | 2 | Pistole, stark gegen Drohnen |

**Maxwell ist Spielfigur (Duc 01.11.2026):** Greift er an, öffnet sich wie bei Duc der echte Kampf statt des Schnellkampfs. Details stehen in [`kampf.md`](kampf.md#maxwell-als-spielfigur). Seine LP von der Karte gehen als Anteil in den Kampf und zurück. Fällt er, ist er bis zur nächsten Welle weg, die Welle läuft weiter, nur Ducs Fall startet sie neu. Mr. White bleibt Duc vorbehalten. Greift der Feind ihn an, rechnet die Karte das wie bei jedem Trupp, auch „Hold the Gangway“ bleibt.

Rosi übergibt das Taser-Gewehr an Tag 19 morgens in `a2_steelmop`, zusammen mit Maxwells Steel Mop.

## Machtleiste und große Momente (Duc 31.10.)

Jeder Truppenführer hat eine Leiste über der Figur. Ausgeteilter Schaden lädt sie, eingesteckter doppelt so schnell, ein Sieg im echten Kampf gibt Duc 25. Ist sie voll, erscheint ein Knopf, der Moment wird groß mit Gesicht und Spruch eingeblendet.

| Truppenführer | Moment | Wirkung |
|---|---|---|
| Duc | Rally | alle Trupps und Duc bekommen ein Viertel Leben zurück |
| Mr. Maximum | Maximum Force | trifft alle Feinde daneben mit 1,5-fachem Schaden, kein Gegenschlag |
| Chiara | Sweep the Deck | trifft mit dem Taser alle Feinde bis zwei Felder, kein Gegenschlag |
| Wolff | Legion Drill | darf diese Runde nochmal ziehen und angreifen |
| Elsa | Clear the Sky | holt alle Drohnen bis sechs Felder vom Himmel |
| Rosi | Pull the Plug | trifft alle Roboter bis drei Felder doppelt |
| Yamamoto | One Cut | der stärkste Feind in Reichweite nimmt 2,5-fachen Schaden, kein Gegenschlag |
| Bibi | Nervous Laugh | ihr Angstlachen zieht alle Feinde bis fünf Felder diese Runde auf sie |

**Duo-Sprüche:** Beim ersten Doppelangriff eines Paars steht ein kurzer Wortwechsel in der Meldung (Entwurf, unvertont).

**Rethink (Duc 31.10.):** Bis zur ersten endgültigen Tat der Runde (Angriff, Rettung, großer Moment, Hilfstruppe) setzt der Knopf alle Züge der Runde gratis zurück. Danach gibt es zwei Rücksprünge je Tag (Code: `taktik_eden_rise.py` `"rueckspruenge": 2`, Abgleich 04.11.2026): zurück zum Beginn der Runde, ist dort noch nichts passiert, eine Runde früher, bis zu fünf Runden. Auch nach einer Niederlage geht das, dort neben „Restart wave“.

## Support (Duc 31.10.)

Hilfstruppen stehen nicht auf der Karte. Drei Plätze: Holm ist fest, zwei zieht der Spieler hinein. Wer fehlt, wird erst sichtbar, wenn er verdient ist (`vertrauen` in `taktik.json`). In der Schlacht zeigt die Leiste unten links Gesicht, Name und Zustand, ein Klick erklärt die Hilfe und setzt sie ein. Lola, Lea und die anderen sind mit ihren vorhandenen neutralen Porträts zu sehen.

| Figur | Verdient | Wirkung | Wie oft |
|---|---|---|---|
| Holm (Bridge Command) | immer | ein Trupp, der schon gehandelt hat, darf nochmal | je Runde |
| Sophia (Radio) | Vertrauen 2 | zeigt, wo jeder Feind in zwei Runden steht | immer |
| Lola (Galley) | Vertrauen 2 | heilt einen Trupp auf Kai oder Mole um 40 %, Duc um 25 % | je Welle |
| Lea (Tender) | Vertrauen 2 | Feinde von See setzen die erste Runde aus | immer |
| Siri (The Stream) | Vertrauen 2 | eine ganze Front setzt eine Runde aus | je Welle |
| Ligeia (The Song) | Vertrauen 3 | die Piraten am Strand schlafen 2 Runden, Roboter sind immun; danach verschwindet sie erschöpft (Duc 01.11.2026, Code hat noch: alle Feinde bis zwei Felder vom Wasser setzen eine Runde aus, Mr. White nicht) | einmal in der Schlacht |

Wer aussetzt, hat einen gestrichelten Rand und keine Absichtslinie. Ein Neustart der Welle setzt den Stand vom Wellenbeginn wieder ein, Ligeias Gesang kommt also nur zurück, wenn sie ihn in dieser Welle gesungen hat.

## Das Drehbuch der dritten Welle


| Runde | Was passiert |
|---|---|
| 1 | Pascal öffnet die Barrikade und wird schwarz, Mr. White erscheint. Auf der Karte liegt die Barrikade jetzt offen |
| 2 | Pascal versteckt sich zwischen den Häusern und verschwindet von der Karte (Szene `pascal_geht`, Duc 02.11.2026) |
| 3 | Alvas Trupp fällt. Alva ist nur bewusstlos, das zeigt erst die Szene nach dem Sieg |
| 4 | Nur mit `kl_loewe_frei`: Mochi hält White eine Runde auf, Bibi rettet ihn mit Rauch |
| 5 | White schlägt Minicu am Tor nieder. Lola und Jana schreien nach ihm, Pascal kommt aus dem Versteck und kniet bei ihm („You gave me your word“), Casanova nennt ihn einen Verräter, dann geht Pascal mit White. Ab jetzt ist White angreifbar. Seit 02.11. eine Runde früher, damit Minicu auch fällt, wenn die Kirche schon wankt |
| Duc bis 3 Felder an White | einmal: Casanova kommt aus der Kirche und gibt ihm den letzten Verbandskasten (volle Leben) |
| Direkt danach | Die Warnung vor Mr. White (Duc 01.11.): Danzel, wenn die Quest in einem der beiden Ausgänge fertig ist und er nicht am Boden liegt, auch wenn er nicht aufgestellt wurde. Sonst liest Megan dasselbe aus Eden Intelligence vor. Noch nicht vertont |

## Drehbuch „Hold the Line“ (Duc 02.11.2026)

Ganzer Ablauf in [`../welt/drehbuch_finale.md`](../welt/drehbuch_finale.md). Was davon Regel ist:

- **Beats je Runde:** Jede Welle hat in `WELLEN[...]['beats']` kurze Szenen zu festen Runden, mit Bedingung (`flag`, `nicht_flag`, `t`, `nicht_t`, `einheit`). Jede Szene kommt einmal, mehrere einer Runde laufen hintereinander (`_beats`). Die letzte Welle hat stattdessen ihr eigenes Drehbuch (`_drehbuch`).
- **Wahl in einer Szene:** Eine Zeile mit `art: wahl` zeigt Knöpfe statt Weiter (`szene_waehlen`, Aktion `szene_wahl`). Nur für die Chronik, keine Punkte. Leertaste wählt nichts, Esc überspringt. Erste Nutzung: Minicus Sturz.
- **Funk nach der Nacht:** Wer die Nacht in der Belagerung bei einer Frau war (`nacht_bei` aus der Nacht-Wahl), hört sie in der ersten Welle des nächsten Tages über Funk. Stufe nach dem kleineren Wert von Vertrauen und Begehren (bis 2, 3, ab 4), Lea und Rosi brauchen dafür ihre Leiter-Szene. Duc hat an diesem Tag 10 % mehr Leben (`kampf.lp_max_duc`, `z['lp_plus']`).
- **Der letzte Verband** (Tag 21 Dinner): Wen Duc wählt, steht im Flag `bl_verband_<id>`.
- **Auftrag Funk** (Tag 21 Abend): Rosi, mit Charly zusammen, wenn sie geblieben ist, findet Whites Kanal (`bl_funk_white`): nach Welle 5 hört der Spieler Whites Angebot an Pascal. Sophia notiert ein Wort (`sophia_notizen`, Akt 3).
- **Auftrag Türen** (Tag 22 Mittag) und **Petrus Ruder:** Das Dorf rudert in Welle 4 bei Ruf 5. Mit Petru an den Türen (`bl_tueren_petru`) und mit heiler Werkstatt aus Welle 3 (`bl_werkstatt_heil`) reicht je ein Punkt weniger (`_rudert`). Beides zusammen: Ruf 3. Lola oder Mina allein an den Türen senken die Schwelle nicht (gebaut fix-akt2, vorher las `_rudert` nur das Ruder).
- **Auftrag Nachtwache** (Tag 22 Abend): Wolff, Elsa oder Yamamoto (`bl_nachtwache_<id>`) berichten am Morgen und stehen in Welle 6 schon neben Minicu am Tor (Feld 30,15). Niemand: Holm sagt es in Welle 6 selbst.
- **Auftrag Kirche** (Tag 23 Mittag): Mit Jana (`bl_kirche_jana`) zählt der erste Schlag an die Kirchentür in Welle 6 nicht. Mit Don Anghjulu (`bl_kirche_don`, nur ab Vertrauen 3, sonst schläft er und Casanova bleibt) läutet er nüchtern: Die Kirche hat in Welle 6 ein Leben mehr, zusätzlich zum vierten Leben aus Vertrauen 3 (`_welle_start`, einmal je Welle, fix-akt2, Vorschlag). Casanova in der Kirche bringt keinen Kampfvorteil.
- **Alvas Runde** (Tag 21 Abend, `bl_alva_runde`): In der Bar an Tag 22 erinnert Alva an das Versprechen, danach legt sie die Rechnung hin (`bl_bar_rechnung`): 60 € vom Konto, Vertrauen Alva +4. Ohne Versprechen geht die Runde aufs Haus (Zeile aus `drehbuch_finale.md`), kein zweiter Takt (fix-akt2, Vorschlag).
- **Vorher gesät (Pflicht-Events in `ereignisse_belagerung.py`):** Minicu an Tag 3 (Kevin), 6 (Lolas Reste), 10 (Janas Koffer), 14 (Pascals Sonntagsstunde). Die Kriegstafel kommt an Tag 15 nach Megans Anruf (`bl_tafel`). Brotkrumen: Pascals Handschrift (Tag 2, 3, 14, Umschlag am Abend von Tag 21), MINICU 11 auf Alvas Tafel (Tag 20), Petrus Ruder (Tag 22 Mittag), Megans abgebrochener Satz und Pascals Satz im Kriegsrat.
- **Appell:** Kommt Duc White auf drei Felder nahe, folgen Warnung, Appell und Casanova. Holm ruft jeden Trupp auf, wer gefallen ist, bekommt Stille, Lola antwortet immer aus der Kombüse (`APPELL`, `_appell`).

## Die Nord-Barrikade (Duc 02.11.2026)

Die Barrikade auf den Feldern 27,8 und 28,8 liegt als Bild auf der Karte: zu in Welle 1 bis 5, nach Pascals Verrat zur Seite geschoben. Das Bild ist ein Krea-Edit eines Kartenausschnitts mit weichem Rand (`werkzeuge/barrikade_bild.py`, Daten `barrikade_bild` in `taktik_eden_rise.py`, Dateien `module/eden_rise/taktik/barrikade_zu.webp` und `barrikade_offen.webp`). Fehlt das Bild, zeigt die Karte wie bisher rote Felder.

## Was Holm sagt (Duc 02.11.2026)

Holm steht im Kommandoposten mit dem Fernglas. Sie sagt, was sie sieht und wo, aber nie Runden. Dass die Zahl auf der Karte die Runden bis zur Ankunft zählt, erklärt im ersten Briefing ein Hinweis ohne Sprecher.

## Umbau (Duc 01.11.)

- **Blätter:** Jede Figur hat ein Blatt mit 6 Bildern Stehen und 6 Bildern Laufen, `werkzeuge/eden_rise/taktik_figuren.py` schneidet sie. Chiara trägt die Dress Whites nur mit `sn_dress_whites_fertig` aus dem Event `sn_dress_whites` bei Danzel, ihre Karte zeigt dann auch das Set „Dress Whites“ (`set8`). Ohne das Event trägt sie auf der Karte ihre Crew-Uniform.
- **Danzel ist Support:** „Steel Lining“, einmal je Welle halbiert er den Schaden an einem Trupp bis zur nächsten Runde (nicht bei Duc). Mit `rt_ausgang_alle` oder `rt_ausgang_getrennt`, also nach der Quest in beiden Ausgängen. Wählt man ihn, steht er fest an der Kirchentür und greift normale Gegner in Reichweite an. Bei Mr. Whites Auftritt in Welle 3 flieht er mit seinem Fluchtsatz, „Steel Lining“ ist dann weg. Zur Warnung vor White kommt er zurück.
- **Minicu statt Petru:** In Welle 1 bis 5 steht er neben Pascal an der Nord-Barrikade (Feld 28,10), damit Pascal dort nicht allein steht (Duc 02.11.2026). Zum Verrat schickt Pascal ihn ans Tor: In Welle 6 steht er am Ausgang des Gangs vom Haupttor zur Kirche (`start_finale` 29,15) und schlägt zu, wer vorbeikommt, bis White ihn in Runde 5 niederschlägt. Er sperrt den Gang nicht, sonst wäre die letzte Welle zu leicht. Alvas Rettung erfährt der Spieler erst in Akt 3, deshalb fehlt sie in der Siegszene.
- **Piraten in Welle 2:** Fackelpirat, Pirate Gunner (Reichweite 2), Pirate Brawler und Captain Buenaventura. Greift Duc oder Maxwell an, kommt im echten Kampf immer ein einfacher Pirat dazu. Fällt Buenaventura, geben alle Piraten auf. In Welle 3 gibt es keine Piraten mehr.
- **Ligeia:** Piraten bis zwei Felder von Strand oder Wasser schlafen zwei Runden, Roboter nicht.
- **Mochi ohne Versöhnung:** Der Löwe kommt trotzdem, aber ohne Bibi (Szene `mochi_allein`).
- **Noch offen:** Minicu hat noch keine Legenden-Zeilen. Szenen und Zeilen sind Entwürfe und unvertont.

**Angriff ohne Bewegung (Duc 01.11.):** Ist ein Trupp gewählt, steht in der Befehlsleiste immer Attack und Wait, auch wenn er nicht gezogen ist. Wer schon gut steht, schlägt direkt zu. Ohne Feind in Reichweite ist der Knopf aus.

**Kampf-Hintergrund nach Ort (Duc 01.11.):** Der echte Kampf zeigt das Bild des Felds, auf dem der Gegner steht (`kampf_ort`, Tabelle `ORTE` in `taktik_eden_rise.py`): Yacht, Mole, Hafen, Strand, Macchia, Felsen, Dorf, Kirchplatz. Alle Bilder sind `eden_rise_siege_*`, golden hour und von der Seite wie eine Bühne, damit die Kampf-Sprites stehen statt schweben (`werkzeuge/hintergrund_bild.py`). Auch die Szenen auf der Piazza zeigen ab dem Angriff den Kirchplatz statt der Festa.

**Flinke Roboter (Duc 01.11.):** Cobra Robot (16 LP, Abwehr 3, Bewegung 8, jagt den am stärksten Verwundeten) und Scorpion Robot (18 LP, Abwehr 4, Bewegung 7, geht auf die schwächste Rüstung). Beide kommen über Land als Nachschub: Kobra in Welle 2 und 5, Skorpion in Welle 4. Welle 6 bleibt ohne sie, dort reichen Mr. White und der Verrat. Maschinen, der Taser wirkt nicht, Rosi trifft voll, Felsen halten sie nicht auf. Echter Kampf mit `RobotCobra` / `RobotScorpion`. Bis Ducs Pixel-Blätter da sind (`taktik/quellen/roboter_kobra.png`, `roboter_skorpion.png`, dann `taktik_figuren.py`), zeigt die Karte einen verkleinerten Boarding Robot.

**Zwei Roboter (Duc 01.11.):** Boarding Robot (26 LP, Abwehr 6, Bewegung 4) ab Welle 1, Heavy Boarding Robot (42 LP, Abwehr 8, Bewegung 3, Angriff 11) ab Welle 2. Beide zerlegen die Yacht. Solange die eigenen Kampf-Sätze `BoardingRobot` und `BoardingRobotHeavy` fehlen, zeigt der echte Kampf den Platzhalter Unit-01. Nach ihrem Export `taktik_eden_rise.py` neu bauen.

**Im Kalender (Duc 01.11.):** Tag 19 startet das Manöver, Tag 21 die echte Schlacht (`taktik.beginnen(art=...)`). Das Manöver hat eine Welle, Kirche und Duc können nicht fallen. Prozent und Folgen der Story stehen auf [`belagerung.md`](../welt/belagerung.md). Die Vorschau `--taktik` läuft ohne Prozent.

**Sichtbarkeit (Duc 01.11.):** Die Figuren haben einen leichten Schein: Trupps und Mr. White hell, Feinde rot.

## Ducs Figur auf der Karte (Duc 01.11.)

Je Jacke ein Blatt (Terra Scura, Meramie, Incendio, Zéphyr), in der Hand immer der Säbel. Sonst wären es 16 Blätter. Ein kleines Symbol an der Figur und die Infokarte zeigen die angelegte Waffe, im echten Kampf stimmt die Kombination ohnehin. Auf der Karte ändert die Waffe nichts, Ducs Reichweite bleibt 1.

## Stand und Grenzen

- **Bots (Stand Umbau 01.11.):** Ohne eingesetzten Support gewinnen beide nur noch mit 1 Kirchenleben, der einfache in 20 Runden, der kluge in 42. Der vorbereitete Bot aus `test_vorbereitung_zahlt` gewinnt in 24 Runden mit allen 3 Leben und rettet alle Häuser. Die Bots sagen wenig über die echte Schwierigkeit, erst ein Spieltest zählt.
- **Dauer:** Wir wollen rund eine Stunde. 14 Runden mit 4 Trupps dürften kürzer sein. Mehr Trupps und Feinde kommen nach dem Spieltest.
- **Noch offen:** Vorbereitung senkt noch keine Prozente, Roboter und Weißer Anzug nutzen vorhandene Gegner. Die Szenen sind unvertonter Entwurf. Noch nicht im Kalender von Tag 21.
- **Duc-Kampf:** Die Begegnungen `tk_*` kommen zur Laufzeit dazu, `kaempfe.json` bleibt unberührt.

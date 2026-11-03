# Die Belagerung · Tag 21–23 (Ende Akt 2)

> **Drei Tage statt einem (Duc 01.11.2026, E-114).** Testspieler fanden die ganze Schlacht an einem Tag zu viel. Wo unten noch „Tag 21“ oder „Welle 3“ steht, gilt dieser Abschnitt.

| Tag | Frühstück | Tag | Nachmittag | Dinner | Abend | Nacht |
|---|---|---|---|---|---|---|
| **20** | | | Alvas Flinte | Elsas Angebot | Kriegsrat | Letzte Nacht, Wahl der Person |
| **21** | | | Welle 1: Hunde, Agenten | Welle 2: Schützin, Drohne, Roboter | Trösten oder Mut, Wahl | Wahl der Person |
| **22** | Bestandsaufnahme | Flicken | Welle 3: Fackelpiraten | Welle 4: Buenaventura, er gibt auf | Trösten oder Mut, Wahl | Wahl der Person |
| **23** | Bestandsaufnahme | Flicken | Welle 5: schwere Roboter, alle Fronten | Welle 6: Verrat, White | Bericht | |

**Warum sie jede Nacht aufhören:** Alon will kein zerstörtes Dorf, sondern die Unterschrift. Am Abend liegt das Papier wieder auf den Kirchenstufen, und Casanova liest es zweimal. Pascal kämpft zwei Tage neben Duc und öffnet erst dann das Tor.

**Vorbereiten zahlt:** Megan sagt an Tag 15, sammelt Holz und Stein. Holm erinnert beim Kriegsrat daran. Was dann im Vorrat liegt, wird in den Morgen der Belagerung verbaut.

**Abende und Nächte** (`ereignisse_belagerung_nacht.py`): Jede der sieben Frauen hat ein Gespräch am Abend und eine eigene Nacht, Mr. Maximum ein Gespräch. Pro Abend und Nacht wählt der Spieler eine Person, also sieht er nie alle. Die Nacht richtet sich nach der Stufe: Ab Begehren 3 kann sie in die Intim-Szene führen, sonst bleibt sie zärtlich. Vertrauen und Begehren steigen dadurch nicht, der Abstand von 7 Tagen bleibt. Am nächsten Morgen sagt sie eine Zeile dazu. Alle Texte sind Entwurf.

**Nichts anderes dazwischen:** Ab dem Angriff am Nachmittag von Tag 21 laufen nur noch Szenen der Belagerung (`sperre` im Modul), keine Selfies, Handy-Events oder Stufen der Romanzen-Leiter.

**Die Yacht** kann erst an Tag 23 sinken, weil die Crew dort schläft und die Nacht-Szenen dort spielen.

> Stand 31.10.2026 · Besitz: Brain Trust · **Die Taktik-Karte hängt seit 01.11.2026 im Kalender ([`../systeme/taktik.md`](../systeme/taktik.md)). Das Prozent-System wirkt mit ersten Zahlen, die Aufgaben der Crew fehlen noch. Alle Szenen der Woche sind Entwürfe.** Diese Seite sammelt,
> was darauf einzahlt. **Hast du einen Story-Punkt, der hierher gehört? Trag ihn unten in die Sammlung ein.**

Der Weg dorthin steht in [`akt2_kalender.md`](akt2_kalender.md): Frist an Tag 15, die Woche danach gehört der Vorbereitung, der Kriegsrat ist am Abend von Tag 20 (Duc 01.11.2026).

## Die Idee (Duc 30.10.2026)

Die Belagerung läuft über ein **Punktesystem** und startet bei **100 %**.

- **Bei 100 % ist der Kampf fast unmöglich:** etliche Kämpfe, sehr starke und motivierte Gegner, alle Gegenmaßnahmen sind
  aktiv. Duc kommt nur mit 0,01 % durch. Es ist möglich, aber sehr schwer, ein Ereignis für Speedrunner auf YouTube, die
  es mit perfekten Paraden versuchen. **Das ist so gewollt.**
- **Sonst wie die Selbstmordmission in Mass Effect 2:** Jede Figur bekommt eine Aufgabe. Je besser Duc sich vorbereitet
  und je nachdem, wie er die Story gespielt hat, desto leichter wird die Belagerung, **ohne zu leicht zu werden**.
- **Verwandt mit dem Sturm an Tag 5** ([`../systeme/sturm.md`](../systeme/sturm.md): Crew einteilen, Eignung je Posten,
  Krisen in der Nacht), aber deutlich besser und ausgearbeiteter.

**Endgegner:** Mr. White (Alpha, weißer Anzug, Sprite `AgentAlpha`). **Alon** wird zusammen mit der Belagerung geplant.

## Taktik-Karte (Duc 31.10.2026, E-102, Prototyp gebaut)

Die Belagerung spielt sich wie *Fire Emblem*: Duc schiebt Trupps über eine Karte. Das Dorf ist das Herz, die Yacht der zweite Schauplatz.

- **Bilder:** `module/eden_rise/Minimap/` (DALL·E, 3840x2560): ruhige Karte für den Kriegsrat und die Woche danach, Kampfkarte im Abendlicht für Tag 21. Feuer kommt per Code dorthin, wo eine Front durchbricht.
- **Raster:** 48x32 Felder, begehbare Felder von Hand eingetragen.
- **Fronten:** Süden (Strand), Osten (Meer, Yacht), Westen (Macchia) mit je 25 %. Beim Kriegsrat sind nur diese drei zu sehen, also 75 %. Die übrigen 25 % kommen an Tag 21 als Überraschung von Norden: Pascal öffnet den Weg, dort kommt Mr. White. Ein Hinweis von Bà Tư lässt Duc vorher etwas ahnen. Die Grotte ist keine Front, sondern ein Schleichweg in den Rücken des Kais, falls die Kiste aus der Grotte bei Alon gelandet ist.
- **Darstellung:** Auf der Karte stehen stilisierte Symbole der Truppenführer, der echte Kampf-Sprite erscheint erst im Kampf.
- **Trupps:** höchstens sechs. Immer dabei sind Duc, Maxwell und Chiara. Verdient werden können Elsa, Petru, Rosi, Wolff (Legion), Bibi (Red Trio, ersetzt Danzel, Duc 01.11.2026) und Yamamoto.
- **Unterstützung ohne Trupp (gebaut 31.10.):** drei Support-Plätze neben der Karte. Holm ist fest, zwei wählt der Spieler aus Sophia, Lola, Lea, Siri, Ligeia, wenn er sie sich über Vertrauen verdient hat. Regeln in [`../systeme/taktik.md`](../systeme/taktik.md).
- **Kampf (Duc 31.10., Maxwell 01.11.):** Duc und Maxwell werden vom Spieler gesteuert und kämpfen im normalen Kampfbildschirm, Mr. White nur gegen Duc. Alle anderen nutzen einen Schnellkampf wie bei *Fire Emblem*: bestehende Stärken-Tabelle aus `kern/kampf.py`, Vorschau vor jedem Angriff, kurze überspringbare Szene. Jeder Truppenführer hat eine eigene Eigenschaft. Die Yacht greifen Roboter an, Maxwell ist mit „Stumpf“ gegen Maschinen stark und glänzt dort.
- **Dauer:** rund eine Stunde, Höhepunkt von Akt 2.
- **Stand des Prototyps (31.10.):** Regeln in [`../systeme/taktik.md`](../systeme/taktik.md). Anders als oben geplant ist Wolff immer dabei, Petru steht nur als Bürgerwehr auf der Karte. Verdient werden Elsa, Rosi, Yamamoto und Danzel. Gebaut sind auch Feuer und Rettung in Welle 2 und die Yacht als Ziel. Das Feuer an durchbrochenen Fronten fehlt noch.

### Das Manöver (Duc 01.11.2026)

Die erste Vorbereitung ist eine Einführung in die Taktik-Karte: Der Spieler kann sie im Testspiel mit Hilfstruppen aus dem Dorf, der Fremdenlegion und dem Red Trio ausprobieren. Das dient als Tutorial und macht Lust auf mehr. Rosi weckt Unit-01 auf, sie dient als Ersatz für die Roboter.

- **Wann:** Tag 19, tagsüber. Holm ist zurück und übt zum ersten Mal ihre Befehle von der Brücke, das Trio ist entschieden, der Tauchgang vorbei. Der Spieler sieht seine Schwachstellen und hat noch anderthalb Tage.
- **Ablauf:** etwa zehn Minuten, nicht zu verlieren. Am Ende nennt Megan den Stand in Prozent.
- **Bibis Platz** bleibt leer, wenn das Trio nicht versöhnt ist. **Danzel** kämpft nicht mehr, er unterstützt die Verteidigung mit seiner Rüstungserfahrung aus der Anlage (Duc 01.11.2026, Regeln in [`../systeme/taktik.md`](../systeme/taktik.md)).
- **Pascal** übernimmt die Nordbarrikade: *“Leave it with me.”* An Tag 21 öffnet er genau diese. Zu Minicu am Haupttor sagt er: *“Hold the line, Minicu.”*
- **Wolff** kommt immer, weil er den Vertrag mit A.V. gekündigt hat. Bei Weg C bringt er Adrien mit. Wer die Berge übersprungen hat, bekommt eine kurze Vorstellung.
- **Unit-01** ist seit Tag 8 aus. Rosi hat Angst vor dem roten Auge, aber es leuchtet bernstein: *“Don't you dare dent her.”* Ohne Rosi macht es Maxwell, wie beim fremden Teil.

**Ablauf der Woche:** Tag 15 nennt Megan beim Frühstück die Frist und die Aufgaben der Crew, ohne Karte, die 100 % nur als Zahl. Tag 19 Manöver. Tag 20 abends Kriegsrat mit Stand und Trupp-Karten.

### Die Kirche

In der Kirche sind Kinder, Alte und Casanova. Alon will sie als Geiseln nehmen, um seinen Plan umzusetzen. Sie hat **3 Lebenspunkte**, jeder Schlag jeder Einheit zieht 1 ab. Verliert Duc oder fällt die Kirche, startet die aktuelle Welle neu (Duc 31.10.).

### Der Kriegsrat und die Trupp-Karten

**Der Kriegsrat wird neu geschrieben (Duc 01.11.2026):** Er findet einen Tag vor der Belagerung statt, am Abend von Tag 20. Holm ist seit Tag 18 zurück und dabei, ihre Rückkehr bleibt, wie sie ist. Megan erklärt mit Eden Intelligence die drei Angriffswellen. Holm erklärt die Feindtypen und schlägt die Trupps vor (blau, Gegner schwarz). **Trupp-Karten:** oben ein Bild, unten Attribute und wogegen der Trupp gut ist. Drei Karten sind ausgegraut und fest: die Bürgerwehr unter Pascal, dem neuen sanften Riesen (Duc 01.11.2026, ersetzt Petru) und Alva bleibt im Zentrum und wehrt schwache Gegner wie Tiere geskriptet ab.
### Das Drama (Duc 31.10., Aufbau wie ein Drama nach Aristoteles)

1. **Erste Welle:** leicht.
2. **Zweite Welle:** anspruchsvoller, erste Verluste. Es fühlt sich an wie gewonnen.
3. **Wende:** Pascal öffnet die Barrikade im Norden, sein Trupp wird schwarz, ein weißer Trupp erscheint: Mr. White. Entsetzen bei Alva und beim Riesen.
4. **Absturz:** Alvas Trupp wird ausgelöscht. Leben sie noch? Der Spieler entscheidet: alles in die Mitte ziehen oder erst die übrigen Feinde vernichten. Alva ist nur bewusstlos (Duc 31.10.). Sandru rettet sie aus den Trümmern und versorgt sie (Duc 01.11.2026). Der Spieler erfährt es erst in einer eigenen Szene in Akt 3.
5. **Mochi (nur wenn gerettet, `kl_loewe_frei`):** Er sieht Mr. White, den er hasst, und kommt aus der Macchia herunter (Duc 01.11.2026). Er hält Mr. White eine Runde auf, Bibi schreit vor Freude, kurze Wiedersehensszene. White macht kurzen Prozess, Bibi rettet Mochi in letzter Sekunde mit einer Rauchgranate. Danach ist er wieder dort, wo Duc ihn gefunden hat, in der Macchia. In Akt 3 kann Duc ihn fangen, aber nur wenn die Auffangstation offen ist, also nur nach der Versöhnung des Red Trio (Duc 01.11.2026).
6. **Pascal:** Minicu am Haupttor hält ihn noch fest, White schlägt Minicu mit einem Schlag KO (Duc 01.11.2026, ersetzt Petru). Pascal hatte gebeten, dass niemand verletzt wird. White lacht: *“You didn't really think we'd hold back?”* Pascal begreift zum ersten Mal, was hier passiert, muss die Rolle aber weiterspielen, um das Dorf als Ganzes zu retten ([`dorf_figuren.md`](dorf_figuren.md)).
7. **Casanova:** Duc erreicht White gerade noch. Casanova kommt aus der Kirche und will mitkämpfen. White verhöhnt sie. Duc gibt White recht: Wir brauchen dich. Berührt gibt sie ihm den letzten Verbandskasten, Duc kämpft mit voller Energie.
8. **Mr. White:** sehr schwer. Bis der Trupp des Riesen gefallen ist, kann ihn niemand angreifen (Duc 31.10., Figur getauscht 01.11.). Niederlage heißt Game Over, der Kampf kann neu begonnen werden. Bei einem Sieg tragen ihn seine Agenten weg.
9. **Ende:** Das Dorf feiert, Akt 3 beginnt.

**Pascal (Duc 31.10.):** Er wechselt an Tag 21 offen die Seite, das ganze Dorf sieht es. Nach der Schlacht ist er verschwunden, und erst im Finale von Akt 3 taucht er neben Alon wieder auf. Akt 3 enthüllt nicht mehr, dass er ein Verräter ist, sondern seit wann und wie viel: neun Jahre, Geld, falsche Berichte (Schublade, Brief an Nonna, [`dorf_figuren.md`](dorf_figuren.md)).

**Ohne Versöhnung** ist Bibi nicht im Dorf: Mochi flieht verletzt allein, und Bibi erfährt es nie (Duc 01.11.2026).

### Warum Alon das Dorf angreift

**Satelliten (Duc 01.11.2026):** Alons Satelliten stören den Empfang, sonst verbreiten Yasin und Siri alles über Social Media.

**Drei Fristen treffen sich an Tag 21 (Duc 01.11.2026):**

- **Sein Körper:** Die Krankheit lässt ihm keine Jahre mehr. Durch Ducs Daten ist er fast am Ziel, ihm fehlt nur noch die Anlage in der Bucht.
- **Die Margot:** Sobald Lea das Wrack meldet, wird die Bucht Schutzgebiet. Er muss vorher kaufen.
- **Das Ultimatum:** Es läuft an Tag 21 aus. Nur Casanovas Unterschrift fehlt noch.

**Wie er es vor sich rechtfertigt:** “The last war anyone needs.” Ein schlimmer Nachmittag in einem Dorf gegen das Ende aller Gewalt. Er befiehlt wirklich „keine Toten“, deshalb gibt es Taser und Geiseln. Das Feuer befiehlt White, und Alon schaut nie selbst hin. Das ist sein Riss.

**Der Plan:** Casanova unterschreibt in der Kirche, Pascal stempelt als ihr Stellvertreter. Darum öffnet er den Weg nach Norden.

**Die Lüge danach (Duc 01.11.2026):** Alon ist skrupellos und dreht alles um, im Stil von Fake-News-Politik, ohne eine echte Person nachzuahmen. Er ist hochintelligent und spielt das nur auf Pressekonferenzen. Offiziell waren es Piraten, nicht er, und A.V. hat das Dorf gerettet.

- **Reporter:** Er besticht sie, und das sieht man. Seine Geschichte ist zuerst online, echte Videos nennt er KI-Fälschungen.
- **Polizei:** Er besticht sie auch, aber das wird nur angedeutet und nie bewiesen (E-096, Elsa: *“Five years on this post, and they have never been this polite to me.”*).
- **Das Dorf:** Wer etwas anderes sagt, wird bedroht.

**Satelliten:** Der Empfang fällt am Abend von Tag 20 aus, kurz nach dem Kriegsrat, und an dem Tag kann niemand Hilfe rufen. Filmen geht weiter, nur Senden nicht. Yasin bekommt Geld für sein Video angeboten, Siris Post in eigenen Worten dreht die Lage langsam.

**Wie der Empfang zurückkommt (Duc 02.11.2026, nicht gebaut):** Nach der Belagerung hackt Charly die Satelliten und bricht sie auf. Elsa sammelt die Beweise und schickt sie sofort an die Kommission. Danach arbeitet der Satellit nicht mehr, und Megan kommt in Akt 3 zurück. Ist Charly nicht freigeschaltet (`rt_charly_bleibt` fehlt), macht es Rosi allein: Sie findet das Handy eines der Agenten, die Duc besiegt hat, und kommt von selbst auf die Frequenz, auf der der Satellit sendet. Das gilt auch, wenn das Trio zerbrochen ist oder die Quest nie gespielt wurde. Niemand ruft jemanden an, das Netz ist ja ausgefallen.

Offen: Elsas Weg an die Kommission läuft am Rathaus vorbei. Das passt zu `mo_beweis_bei_elsa` und muss beim Bau von Akt 3 mit Pascals Schublade abgeglichen werden.

## Gebaut (Duc 01.11.2026)

Szenen in `werkzeuge/eden_rise/ereignisse_belagerung.py`, Regeln in `kern/taktik.py`. Alle Texte sind Entwürfe.

| Tag | Event | Was passiert |
|---|---|---|
| 15 Frühstück | `bl_frist` | Megan nennt die Frist und die 100 % |
| 19 Tag | `bl_manoever` | Manöver auf der Karte: eine Welle, nicht zu verlieren, setzt `manoever_fertig` |
| 20 Nachmittag | `bl_alva_flinte` | Alva holt Papas Flinte hinter der Tafel hervor |
| 20 Dinner | `bl_elsa_hilfe` | Elsa bietet ihre Hilfe an, in ihrer Kampfuniform |
| 20 Abend | `bl_kriegsrat` | Kriegsrat, am Ende fällt Megans Bild aus: die Satelliten |
| 20 Nacht | `bl_letzte_nacht` | Die letzte Nacht an Bord |
| 21 Dinner | `bl_belagerung` | Die Belagerung startet, wer sie gewinnt, bekommt `belagerung_gewonnen` |
| 21 Nacht | `bl_bericht` | Was übrig ist. Danach endet der Kalender wie bisher |

**Prozent (erste Zahlen, der Spieltest legt sie fest):** Start 100 %, Boden 30 %. `VORBEREITUNG` in `taktik_eden_rise.py` listet, was abzieht. Die Karte zeigt den Wert oben als „Alon 75 %“, beim Darüberfahren steht dort, was ihn gesenkt hat. Leben und Angriff der Feinde wachsen damit: bei 60 % wie in der Vorschau, bei 100 % rund 30 % stärker, bei 30 % rund 23 % schwächer.

**Was die Story an der Schlacht ändert (gebaut):**

| Bedingung | Wirkung |
|---|---|
| `gr_kiste_abgegeben` | 2 Hunde mehr in Welle 1 |
| `rt_white_agenten` | 2 Agenten weniger in Welle 3 |
| Vertrauen Don Anghjulu ab 3 | Die Kirche hat 4 Leben |
| Vertrauen Bà Tư ab 3 | Der Nachschub kommt eine Runde später |
| Ruf ab 5 | Das Dorf rudert hinaus: Der letzte Schub Boote in Welle 2 fällt weg |

**Noch nicht gebaut:** die Aufgaben der Crew wie in Mass Effect 2, Grotte als Schleichweg, Minas Szene zum Ruf, Bà Tưs Hinweis auf den Norden, das Feuer an durchbrochenen Fronten.

## Sammlung: Was einzahlt

Hier steht nur, was die Story schon vorsieht oder wo Duc es gesagt hat. Zahlen und genaue Wirkung kommen beim Bau.

| Quelle | Flag | Wirkung (Stand) | Status |
|---|---|---|---|
| Red Trio, Station 7 | `rt_white_agenten` | Duc hat einen Teil von Mr. Whites Agenten schon ausgeschaltet: White kommt ohne Leibwache | von Duc gesetzt, 01.11. |
| Grotte, Kiste abgegeben | `gr_kiste_abgegeben` | Alons 40 Halsbänder sind wieder im Umlauf: mehr Hunde und der Schleichweg durch die Grotte | von Duc gesetzt, 01.11. ([`ortskapitel_grotte.md`](ortskapitel_grotte.md)) |
| Grotte, Kiste behalten | `collar_crate` | Beweis gegen Alon. Wirkung auf die Belagerung offen | vorgemerkt |
| Ligeia (Vertrauen 5 am stärksten) | – | Sie singt zum ersten Mal, um zu retten: Am Strand schlafen die Piraten 2 Runden lang, bevor sie aufwachen. Roboter bleiben immun. Danach verschwindet sie erschöpft und wünscht Duc noch einmal alles Gute ([`ligeia.md`](../figuren/ligeia.md)) | von Duc gesetzt, 01.11. |
| Red Trio versöhnt | `rt_ausgang_alle`, `rt_charly_bleibt`, `rt_bibi_bleibt` | Wer geblieben ist, ist im Dorf. Eine Aufgabe bei der Belagerung wäre naheliegend. Vorbote: `rt_bon` (Tag 19–20) | Idee, offen |
| Red Trio, Aussagen | `ark_aussagen_3` (alle), `ark_aussagen_1` (getrennt) | Spur gegen Alon. Die feine Zahl kommt mit dem Minispiel. Zählt nur bei der Kommission, nicht bei der Belagerung | von Duc gesetzt, 01.11. |
| Ruf im Dorf | – | [`dorf_redet.md`](../systeme/dorf_redet.md): Vorbild ist Kanon: 1924 ruderte das Dorf zur Margot hinaus und holte die Crew lebend heim, Petrus Großvater war dabei. Bei hohem Ruf rudert es wieder und stoppt einen Schub Boote. Weil Ruf verblasst, zählt auch, ob Duc das Dorf zuletzt vernachlässigt hat. **Mina** ruft alle zusammen, das Netz ist tot und nur sie erreicht noch jede Tür. **Petru** fährt als erfahrenster Seemann mit ihr hinaus, als Hommage an seinen Großvater, **Lea** begleitet sie. Bei niedrigem Ruf kommt Mina allein zurück: *“They heard me. They just didn't open.”* | von Duc gesetzt, 01.11. |
| Bà Tư, hohes Vertrauen | – | Alons Leute reden beim Essen: Sie weiß, wann sie abrücken, die Boote werden früher sichtbar ([`dorf_figuren.md`](dorf_figuren.md)) | von Duc gesetzt, 01.11. |
| Don Anghjulu | – | Läutet die Glocke zum ersten Mal nüchtern und im richtigen Takt: Die Kirche bekommt ein viertes Leben ([`dorf_figuren.md`](dorf_figuren.md)) | von Duc gesetzt, 01.11. |
| Mr. Whites Brandtrupp | – | Angeheuerte Fackelpiraten (Duc 31.10.), die das Dorf anzünden. Mr. Whites eigene Leute sind die Agenten: Nahkämpfer mit Schlagstock und Marksman mit Gewehr. Riposte (Wasser) ist hier die stärkste Waffe und löscht buchstäblich den Hafen. Erster Auftritt schon nach dem Tauchgang ([`ortskapitel_tauchgang.md`](ortskapitel_tauchgang.md)) | von Duc gesetzt, 30.10. |
| Der Piraten-Kapitän | – | Hat Duc ihn nach dem Tauchgang besiegt, will er Rache, schickt seine Piraten und kämpft bei der Belagerung selbst mit ([`ortskapitel_tauchgang.md`](ortskapitel_tauchgang.md)). White bezahlt ihn und befiehlt das Feuer. Buenaventura sieht die Menschen im brennenden Haus und gibt nach seiner Niederlage auf: *“We rob ships. We do not burn grandmothers.”* Dieser Sieg ist das „Es fühlt sich an wie gewonnen“ vor Pascals Verrat. In Akt 3 sagt er aus und wird Eco-Kapitän ([`akt3.md`](akt3.md)), die Festa beliefert er weiter | von Duc gesetzt, 01.11. |
| Alons Kampfdrohnen | – | Echte Flieger, einzeln schon vor der Belagerung, dort in Massen. Nur Gemelli ist gegen Flieger stark, Holm oder Duc holen sie vom Himmel | von Duc gesetzt, 30.10. |
| Holm kommt zurück | – | Vor der Belagerung, Duc gewinnt ihre Familienwaffe Gemelli in einer Schießwette ([`items.md`](../systeme/items.md)). Sie will selbst auf den Kai, ist aber noch nicht fit und redet es sich ein. Darum übernimmt sie die **Kommandobrücke und gibt Befehle**. Was das genau bewirkt, kommt beim Bau | von Duc gesetzt, 30.10. |

**Überholt (Duc 31.10.):** Der Schwarze Löwe half bisher erst in Akt 3. Jetzt kommt Mochi bei `kl_loewe_frei` schon hier kurz vor.

## Offen

- Chiaras Taser-Gewehr (Duc 31.10.): Rosi baut es ihr vor der Belagerung. Die Übergabe steht in `a2_steelmop`, Tag 19 morgens, zusammen mit Maxwells Steel Mop.

- Was die Prozente genau messen und was jede Vorbereitung abzieht.
- Die Prozente fallen bis etwa 30 %, damit die Belagerung nie zu leicht wird (Duc 01.11.2026). Den genauen Wert legt der Spieltest fest.
- Welche Figuren welche Aufgaben bekommen, wer dabei ausfallen kann und was das kostet.

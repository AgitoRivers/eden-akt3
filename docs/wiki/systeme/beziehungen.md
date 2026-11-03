# Beziehungen · Vertrauen und Begehren

> Stand 27.10.2026 · Quelle: `kern/zustand.py` (Punkte, Stufen), Quellen in `kern/ereignisse.py`, `kern/handel.py`,
> `kern/gesten.py`, `kern/reaktion.py`, `kern/handy.py`, `kern/auftraege.py`; Schwellen in den Moduldaten
> (`ereignisse.json`, `story.json`, `missionen.json`). Zahlen hier = Stand des Codes; ändert sich der Code, diese Seite mit.

## Zwei Achsen

| Achse | Wer hat sie | Bedeutet |
|---|---|---|
| **Vertrauen** | alle 19 Figuren mit Beziehung (Crew, Nebenfiguren, Megan, Holm …) | Sie verlässt sich auf Duc, erzählt ihm Dinge, hilft ihm. Öffnet Events, Aufträge, Rabatte, Abende. |
| **Begehren** | nur die 7 romanzierbaren Frauen: Chiara, Sophia, Lea, Rosi, Siri, Lola, Alva | Sie fühlt sich zu Duc hingezogen. Öffnet Selfies, Intimität, Eifersucht, das Herz-Ende. |

Jana und Megan haben **kein** Begehren – ihre Abende hängen nur am Vertrauen (und bei Megan an Story-Flags).

## Stufen und Punkte

Angezeigt wird eine **Stufe 0–5** mit Füllbalken. Dahinter liegen **Punkte 0–100**, nach oben immer teurer:

| Stufe | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| ab Punkten | 0 | 10 | 22 | 36 | 55 | 80 |
| Abstand zur nächsten | 10 | 12 | 14 | 19 | 25 | – |

- **Start:** je Figur eine Startstufe (z. B. Vertrauen Lea 2, Lola 2, Megan 0; Begehren Sophia 2, Lea 2, Lola/Alva 0),
  Punkte = Schwelle + 4.
- **Ein „+1“ in einer Folge** (Story-Szene, große Geste, Anhörung) = **8 Punkte**, höchstens ±2 auf einmal (±16).
- Steigt die Stufe, meldet das Spiel *„Vertrauen Lola +1“*; ändern sich nur Punkte, zeigt es ↗ oder ↘.

### Der Deckel knapp vor Stufe 3 (35 Punkte)

Kleines trägt nur bis **knapp vor Stufe 3** (35 Punkte, Stufe 3 beginnt bei 36): Gespräche, kleine Gesten, Handy-Nachrichten, Handel, normale Geschenke und Essen.
Darüber helfen nur **Erlebnisse**: Events, Story-Szenen, große Gesten, Missionen, geliebte Geschenke, Aufträge.
Grund (Trockenlauf 16.10.): ohne Deckel stand nach einer Woche jede Frau auf 5/5, und das Herz-Ende war Zufall.
Seit 27.10.2026 liegt der Deckel bei 35 statt 36: Stufe 3 (Abende, Intim-Liste) gibt es nur über ein Erlebnis.

### Abstand zwischen den Stufen (seit 31.10.2026)

Ab Stufe 3 steigt jede Achse erst **7 Tage** nach dem letzten Aufstieg weiter (`zustand.STUFEN_ABSTAND`). Bis Stufe 3 ist sie frei,
auch ein großer Sprung geht nur bis dorthin. Vorher lief ein Bot mit Fokus auf eine Frau schon an Tag 3 auf Vertrauen 5
(`docs/brain_trust/BEZIEHUNGSKURVE.md`). Der Abstand gilt für alle Figuren mit Vertrauen, auch ohne Romanze.

- **Sichtbar:** Der Balken bleibt voll stehen, und einmal kommt die Meldung „⏳ … the next step needs a few more days“. Nach Ablauf
  genügt der nächste Punkt für den Aufstieg.
- **Ausgenommen:** Story-Folgen („+1“) und Sprünge aus Abend und Auftrag (`roh`). Die verdienten Momente bremst er nicht. Events, große Gesten, Geschenke, Reaktionen im Chat, Missionen und Rast-Anrufe zählen dagegen mit (`folgen_anwenden(..., frei=False)`).
- **Selfies** hängen weiter nur an den Werten und kommen damit später.
- **Zum Testen:** `"stufen_abstand": 0` in `eden-config.json` schaltet ihn aus, dann ist das Spiel neu zu starten.

### Bewunderung (seit 27.10.2026)

Jede romanzierbare Frau **schätzt zwei Attribute** (`personen.<id>.schaetzt` in `modul.json`), z. B. Lola Charme und
Empathie, Chiara Mut und Wahrnehmung. Aus Ducs Werten darin wird eine **Anziehung**: Schnitt unter 2,5 = 0, ab 2,5 = 1,
ab 3,5 = 2. **Begehren-Gewinne** steigen um **×1,25 je Stufe** (Stufe 2 = ×1,5). Verluste und Sprünge (Abend, Romanzen-
Auftrag) bleiben unverändert, Vertrauen ist nicht betroffen. Der Deckel gilt weiter. Die Persona *Berater* (Charme 3,
sonst 2–3) startet bei Lea und Rosi mit 0, bei den anderen mit 1; jeder Attributpunkt kann das ändern.
Code: `zustand.anziehung`, `ANZIEHUNG_BONUS`.

### Lob für Attributsteigerungen (seit 27.10.2026)

Die Crew merkt, wenn Duc stärker, mutiger oder klüger wird (Skyrim-Prinzip). **Wer was mag:** 13 Figuren schätzen je
zwei Attribute (`personen.<id>.schaetzt`). Die sieben Frauen mit Romanze haben dazu die Anziehung (oben); bei Megan,
Maxwell, Jana, Totò, Yasin und Yamamoto steuert `schaetzt` nur die Kommentare (sie haben kein Begehren). Holm sagt nichts.

| Attribut | schätzen es |
|---|---|
| Charme | Siri, Lola, Megan, Jana, Yasin |
| Mut | Chiara, Lea, Rosi, Maxwell, Yamamoto |
| Einfühlung | Lea, Siri, Alva, Lola |
| Wahrnehmung | Chiara, Sophia, Alva, Yamamoto |
| List | Sophia, Rosi, Totò, Yasin |
| Stärke | Megan, Maxwell, Jana, Totò |

**Wie es abläuft** (Code `kern/lob.py`, Zeilen `module/eden_rise/lob.json`, Builder `werkzeuge/eden_rise/lob_eden_rise.py`):

1. Gibst du einen Attributpunkt aus (Level-up-Karte oder Charakter-Menü) und der Wert erreicht **3, 4 oder 5**, merkt
   sich das Spiel einen Kommentar. Pro Attribut zählt der höchste offene Wert (mehrere Punkte auf einmal werden gebündelt).
2. **Freie Szene:** Steht beim Szenenstart jemand da, der dieses Attribut schätzt, sagt die Person **direkt nach der
   Eröffnung einen festen Satz**. Mehrere passende Personen: wer am längsten nichts gesagt hat, dann Zufall mit Seed.
3. **Handy-Fallback:** Hat nach zwei Phasen keine Szene den Kommentar ausgespielt, schreibt ihn eine passende Figur aufs
   Handy (Meldung „New message“). Figuren ohne ST-Karte (Megan, Maxwell, Totò, Yasin, Yamamoto) schreiben nur, Antworten
   gibt es dort nicht.
4. **Grenzen:** höchstens **ein Kommentar je Phase**; jeder Meilenstein genau einmal; dieselbe Figur sagt denselben Wert
   nie zweimal. Events mit festem Text bleiben außen vor (Version 1).

**Texte:** 78 feste Zeilen (13 Figuren × 2 Attribute × Wert 3/4/5), Englisch, jede mit Turbo-Tag in
`stimme_tags.json` (Anzeige ohne Tag). Vorab vertonbar mit `Vertonen_EdenRise.bat` (Schlüssel `lob.<figur>.<attribut>.<wert>`).
Test: `tests/test_lob.py`.

### Tag 1 ist nur positiv

Am ersten Tag gibt es keine Abzüge aus Gesprächen und Nachrichten; ab Tag 2 kann eine Antwort auch missfallen.

## Woher Punkte kommen

| Quelle | Vertrauen | Begehren | Deckel 36? |
|---|---|---|---|
| **Event-Antwort** (häufigste Quelle) | meist +2 bis +6, selten +8; Fehlgriffe −2 bis −10 | +2 bis +8 bei flirtenden Antworten | nein |
| **Story-Folge „+1“** | +8 je Schritt | +8 je Schritt | nein |
| **Partnerwahl im Event** („Du wählst …“) | +4 | +4 | nein |
| **Freie Szene: Reaktion** auf jede Antwort | +2 (Tag 1: erste je Szene +8); ab Tag 2 Missfallen −2 | +2 | ja |
| **Kleine Geste** gelungen | +4 | +4 (je nach Geste) | ja |
| **Große Geste** gelungen / misslungen ab Tag 2 | +8 / −4 | +8 | nein |
| **Zeit zusammen** (freie Phase) | +6 (Arbeit, Gespräch, Spaß) | Romantik: erste am Tag +8, sonst +4 | Romantik ja |
| **Geschenk** | einzigartig +12 · liebt +8 · mag +4 · neutral 0 · mag nicht −4 | Romanzen: liebt +8 (dazu Bewunderung), sonst – | nur bei +4 |
| **Kochen** | Teller für sie nach Geschmack, Teamessen +2 für alle (Meisterwerk +3, misslungen +1) | je nach Gericht | ja, außer dem ersten „liebt“ |
| **Handel** im Laden (wo vorgesehen) | +4 je Kauf | – | ja |
| **Favour** für sie (Handy-Bitte, seit 29.10.2026; die Schnelljobs sind abgeschaltet) | Erfolg +8, Finale +10 (×1,6 seit 29.10.2026, vorher +5/+6), Fehlschlag +1, Ablehnen −1; höchstens eine Bitte am Tag, drei je Figur | – | nein |
| *Schnelljob (abgeschaltet)* für sie | Erfolg +6 (einmal am Tag je Person); Patzer ab Tag 2 −4 | +4, wenn der Job `persoenlich` ist | nein |
| **Auftrag mit Romanze** abgeschlossen | – | springt direkt auf die nächste Stufe | nein |
| **Intim-Abend angenommen** (die Antwort, die in die Szene führt) | – | **mindestens Stufe 3** (`ABEND_BEGEHREN_STUFE`) | nein |
| **Handy-Nachricht** | je Ton (Werte in `handy.json`), **eine wirksame Nachricht pro Person und Tag** | flirtend | ja |
| **Flirt per Handy bei Vertrauen < 2** | **−3** (sie geht auf Abstand) | – | – |
| **Versprechen** gehalten / gebrochen (Tagesende, Frist meist 2 Tage) | +8 / **−16** | – | nein |
| **Anruf beim Rasten** beantwortet | +8 | – | nein |
| **Eifersucht**: sie hört von einem Moment mit einer anderen und hat selbst Begehren ≥ 3 | −8 (*„… ist verletzt“*) | – | – |
| **Anhörung** (Tag 7) | falsch beschuldigt −16 (mit Gnade −8), gefeuert −16, Verrat zusätzlich −8, Schuld teilen: Megan −8 | – | nein |

### Ihr Vorschlag bei „Zeit zusammen“ (seit 31.10.2026)

Sie schlägt etwas vor, das zu Ort, Tageszeit, ihr selbst **und zur laufenden Szene** passt. Das Modell bekommt dafür die
letzten 6 Zeilen der Szene und ihre letzten 5 Vorschläge (auch aus früheren Szenen), die sie nicht wiederholen darf.
Es läuft mit Temperatur 0,9 statt 0, damit auch am selben Ort keine wortgleichen Sätze entstehen.

**Nach einem intimen Moment** in derselben Szene bleibt sie bei diesem Moment und lenkt nicht auf Arbeit um. Der Vorschlag
zählt dann immer als Romantik. Ein abgelehnter Wunsch zählt nicht als intimer Moment. Anlass: Live-Spieltest vom
31.10.2026, dort kam nach Intimität wortgleich „You're late, Officer“ mit Sensor-Kalibrierung. Code `kern/gesten.py`,
Test `tests/test_zeit_zusammen.py`.

### Dates: Eine Zusage hält (seit 31.10.2026)

Nimmt sie die Einladung an, gilt das Date für den nächsten Abend (vor dem Abend: für heute). Pro Abend gibt es höchstens
eine Verabredung, eine zweite Einladung ist dann gesperrt.

| An dem Abend … | Was passiert |
|---|---|
| ist sie frei oder hat eine freie Karte („Time with …“) | Das Date ersetzt ihre Karte, sonst die letzte freie Karte. Der gewählte Ort gilt. |
| ist eine andere Story-Szene, in der sie nicht vorkommt | Das Date folgt nach der Story-Szene. |
| spielt sie selbst in einer Story-Szene mit, oder der Abend steht erst beim Betreten fest | Das Date rückt auf den nächsten Abend ohne anderes Date, mit Meldung. |

**Versetzen:** Wählt Duc am Date-Abend etwas anderes, macht einen Ausflug oder beendet die Phase, verliert er bei ihr
Vertrauen −1. Die Chronik vermerkt es mit der Kennung `stood_up`, sie weiß es also beim nächsten Treffen. Nach einer
kleinen Aktion in derselben Phase kann das Date noch stattfinden. Code `kern/showrunner.py`, Test `tests/test_verabredung.py`.

## Was Vertrauen öffnet

| Ab | Was passiert |
|---|---|
| **1–4** | Events haben Mindest-Vertrauen (am häufigsten **2**, dann 3, selten 1 oder 4). (Schnelljobs mit `ab_vertrauen` erschienen erst dann – abgeschaltet seit 29.10.2026.) |
| **2** | Sie gilt als **vertraute Person** (Nähe-Szenen wählen die vertrauteste Frau ab 2). **Flirten per Handy** wirkt (darunter Rückschlag −3). Das **Dorfohr** verrät einmal am Tag eine unbekannte Vorliebe. Megans Nacht ab 2 (plus Story-Flags). |
| **3** | **Abende** werden möglich: Lola (Tag 3–6, Nacht), Jana (Tag 3–6, Nacht), Alva (Tag 4–6, an Land). In freien Szenen +1 auf Charme/Empathie, wenn eine Anwesende ihm ≥ 3 vertraut. Rabatt im Eden-Shop ab Megans Vertrauen 3. In der Anhörung: Wer ihm ≥ 3 vertraut, deckt die Angeklagte nicht mit einer Lüge. |
| **4** | Zweiter Abend per Handy (Lola ab Tag 4, Alva ab Tag 5). Zusammen mit Begehren 4: **Herz-Partnerin**. |
| je Stufe | Händler grüßt je Stufe wärmer und macht andere Preise; Anrufe beim Rasten haben je Stufe eigene Texte; Akt-1-Rückblick erzählt je Frau „tief / mitte (ab 2) / hoch (ab 4)“. |

**Vorlieben-Meldung** (lavendel, oben rechts; Spieltest Duc 29.10.): Neu entdeckte Vorlieben erscheinen nie mitten in
einer Szene, einem Kampf oder einer Expedition, sondern erst danach (Tagesplan, Kabine, Ende). Mehrere auf einmal kommen
als **eine** Meldung („♡ 3 new preferences – About Lola, Alva and Petru“), eine einzelne wie gewohnt mit Bild. Code
`vmRuhig`/`vmNaechste` in `client/index.html`, Test `tests/test_vorlieben_meldung.cjs`.

## Was Begehren öffnet

| Ab | Was passiert |
|---|---|
| **3 / 4 / 5** | **Selfie-Events** (seit 27.10.2026, Tag 2–6, abends/nachts): je neu erreichter Stufe ein Selfie, 3 knapp bekleidet, 4 oben ohne, 5 nackt (Details [interaktion.md](interaktion.md#selfie-events-duc-27102026-ersetzt-die-sechs-events-vom-2610)). Jana, Megan, Elsa und Isabelle schicken sie über Vertrauen 3/4/5 plus Riegel-Flag. |
| **3** | In privaten Räumen erscheint die **Intim-Liste**. **Eifersucht** ist möglich (siehe oben). Ein angenommener Abend setzt Begehren mindestens hierauf. Jana und Megan (ohne Begehren) bekommen in ihrer Nacht die Liste fest auf Stufe 3. |
| **3 / 4 / 5** | Welche Handlungen frei sind (`intim_stufen` in `modul.json`): 3 = Küssen, Streicheln, Ausziehen, Massage · 4 = mehr · 5 = alles, dazu Positionen, wenn die Szene läuft. |
| **4** + Vertrauen 4 | **Herz-Partnerin** für das Ende. Bei mehreren zählt die Summe beider Achsen, dann Begehren, dann gemeinsame Szenen. |
| Ende Akt 1 | Ist die Partnerin bei Vertrauen ≥ 3 **und** Begehren ≥ 3, endet die Zukunft „mit ihr“. |

### Die Intim-Grenze einer Szene

Wie weit eine Szene gehen darf, ist **das Kleinere aus Begehren und Vertrauen + 1**. Begehren allein reicht also nicht: Wer
ihr nur auf 2 vertraut, kommt höchstens bis Stufe 3. Dazu drei Deckel:

- **Gruppe** (mehr als eine romanzierbare Frau anwesend): höchstens 2.
- **Ort nicht privat genug**: höchstens 3.
- **Sie ist vergeben**: höchstens 3.

Ein Abend ersetzt die freie Phase, auch wenn dort eine freie Szene geplant war (vorher lief dann die geplante
Szene statt des Abends); Story-Szenen ersetzt er nie.

## Funken

Seit 27.10.2026 (`werkzeuge/eden_rise/ereignisse_funken.py`). Die Simulation zeigte: Begehren-Events gibt es genug, aber
sie kommen zufällig – wer sich auf eine Frau konzentriert, bekommt nicht mehr Events mit ihr. Rosi, Lea und Siri blieben
bei 35 Punkten hängen. Deshalb bekommt jede Frau **ohne Abend** einen garantierten privaten Moment:

| Funke | Frau | Wann | Bedingung | Leiter (Figurenseite) |
|---|---|---|---|---|
| *What Would You Do?* (Brücke) | Chiara | Tag 4–6, Nacht | Vertrauen 3, Begehren 2 | gefragt werden |
| *Ten Euros* (Achterdeck) | Sophia | Tag 4–6, Abend | Vertrauen 3, Begehren 2 | die Show rutscht |
| *Glow* (Badeplattform) | Lea | Tag 4–6, Nacht | Vertrauen 3, Begehren 2 | klein, ihr Bogen ist Akt 2 |
| *Night Shift* (Generatorraum) | Rosi | Tag 4–6, Nacht | Vertrauen 3, Begehren 2 | neben ihm arbeiten |
| *Unposted* (Vordeck) | Siri | Tag 4–6, Abend | Vertrauen 3, Begehren 2, **`siri_frei`** | überspringt nie eine Stufe |

- Art **„abend“**: Vorrang (Gewicht 8), sobald die Bedingung gilt; höchstens ein Abend am Tag. Ohne Intim-Szene kostet
  der Funke **keine Zeit**.
- Drei Antworten: die tragende gibt **+14 Begehren** (aus Stufe 2 reicht das für Stufe 3) und einen Nachklang, die
  freundliche nur Vertrauen, das Nein bricht nichts. Jede setzt `<frau>_funke`, der Funke kommt nur einmal.
- Dazu **6 kleine Begehren-Events** (Tag 3–6, ab Vertrauen 2) für die Frauen mit den wenigsten: Rosi *Rosi vs. Officer*,
  *Grease* · Sophia *Darling, Hold Still*, *The Brown Notebook* · Siri *Talking to the Furniture* (wholesome, +2, vor
  `siri_frei` erlaubt), *Golden Hour, Camera Off* (erst nach `siri_frei`).

## Romanze erst ab Bedingung

Bibi gilt erst als Romanze, wenn `kl_loewe_frei`, `rt_ausgang_alle` und `rt_bibi_bleibt` gesetzt sind (`personen.bibi.romanze_flags`, Duc 02.11.2026). `kern/rollen.romanze_abgleichen` setzt `romanzierbar` beim Laden des Spielstands und legt `begehren.bibi` an. Wer die Bedingung verfehlt, hat sie als Freundin an der Station ohne Leiter und ohne Begehren.

## Romanzen-Leiter

Seit 31.10.2026 für alle sieben Romanzen (`werkzeuge/eden_rise/ereignisse_romanzen.py`, Test `tests/test_romanzen_leiter.py`).
Anlass war die Beta-Kritik: Intime Momente wurden nicht kommentiert, Stufen lösten kaum Szenen aus, und vieles war Zufall.
Jana und Megan haben keine Leiter, aber ein Echo am Morgen nach ihrer Nacht.

**Regel beim Schreiben (Duc 31.10.2026):** Der Spieler hat die Szene davor vergessen. Jeder Rückbezug trägt eine Erinnerung in der Lage oder im Satz, und vor den Antworten steht eine klare Frage.

**Feste Szenen statt Zufall.** Jede Szene ist Pflicht, sobald Stufe, frühester Tag und die Szene davor erfüllt sind, und kommt
in ihrer festen Phase. Höchstens eine Leiter-Szene oder ein Echo am Tag (`wann.leiter`), der Rest rückt nach. Wer gefeuert
ist, bekommt keine.

| Szene | Vertrauen | Begehren | Ab Tag | Phase | Was sie bewirkt |
|---|---|---|---|---|---|
| Rosi · *Nothing's Broken* | 3 | 3 | 4 | Nacht | die verdeckte Zeile taucht auf |
| Bibi · *A Very Honest Refund* | 3 | 3 | 15 | Abend | Ökotourismus, Flag `mo_eco_idee` |
| Bibi · *The Bottle* | 3 | 4 | 15 | Nacht | führt in die Intim-Szene, ein Nein bricht nichts |
| Bibi · *The Brochure* | 4 | 4 | 15 | Abend | ihr Geheimnis, Flag `bibi_prospekt` |
| Bibi · *Last Page* | 4 | 4 | 35 | Abend | nach den Toren, Ducs Seite im Field Book |
| Rosi · *Nobody Lost* | 3 | 4 | 6 | Nacht | führt in die Intim-Szene, ein Nein bricht nichts |
| Rosi · *What She Tells Unit-01* | 4 | 4 | 9 | Nacht | Duc belauscht sie; wer still geht, hört in *Read It* “She talks” |
| Rosi · *Read It* | 4 | 5 | 15 | Nacht | nach einem Kampf, ab Tag 19 auch ohne; sie sagt “I lost”, Status zusammen oder offen |
| Lea · *Stay Together* | 3 | 3 | 3 | Nacht | Taucherzeichen zwei Finger, Flag `lea_zeichen` |
| Lea · *What Are We?* | 4 | 4 | 9 | Abend | Status zusammen, offen oder locker |
| Lea · *Sweet* | – | – | 10 | Abend | Sophia fragt Duc, nur bei zusammen oder offen |
| Lea · *No Glow Tonight* | 5 | 5 | 15 | Nacht | die Azoren, nicht bei „locker“; die Antwort färbt das Ende, ändert aber seine Regel nicht |
| Chiara · *Examiner* | 3 | 3 | 4 | Nacht | sie gesteht die Prüfung und lässt sich abfragen |
| Chiara · *Lie Still* | 3 | 4 | 6 | Nacht | ihre Liste; führt in die Intim-Szene |
| Chiara · *Who Gets the Ship?* | 4 | 4 | 9 | Abend | Flag `chiara_schiff_zusage`: Duc sagt Megan, dass das Schiff ihres wird |
| Chiara · *Vega* | 5 | 5 | 15 | Nacht | sie wird leise, „nine and a half“; die Zehn bleibt für die Festa |
| Sophia · *Upside Down* | 3 | 3 | 4 | Abend | Duc liest die Krimi-Zeile im Büchlein, ihre Wette „you'll never ask me what I want“ |
| Sophia · *The Forfeit* | 3 | 4 | 6 | Nacht | sie verliert absichtlich; führt in die Intim-Szene |
| Sophia · *Fourteen* | 4 | 4 | 9 | Abend | M. J. Penrose, die fünfzehnte Absage |
| Sophia · *The Last Train* | 5 | 5 | 15 | Nacht | keine Show, „What do you see?“ |
| Lola · *The Spoon* | 3 | 3 | 4 | Abend | sie verbrennt alles, wenn jemand zusieht |
| Lola · *Breakfast in Bed* | 3 | 4 | 6 | Frühstück | nur nach ihrer Nacht; führt in die Intim-Szene |
| Lola · *Sunday, Nan* | 4 | 4 | 9 | Nacht | „Yes, Chef“, ihre Nan, die Frage nach dem Ernstfall |
| Lola · *First Guest* | 5 | 5 | 15 | Abend | die Hütte, sie beendet einen ganzen Satz |
| Alva · *The Board* | 3 | 3 | 4 | Abend | Papas Tafel, ihr eigener Name steht nicht darauf |
| Alva · *The Jukebox* | 3 | 4 | 6 | Nacht | Duc repariert sie; führt in die Intim-Szene |
| Alva · *Papa's Photo* | 4 | 4 | 9 | Frühstück | nur nach ihrem Abend; sie blieb auch aus Angst |
| Alva · *Chalk* | 5 | 5 | 15 | Nacht | was neben ihrem Namen steht; „Only you“ bleibt für die Festa |
| Siri · *Caption* | 3 | 3 | 4 | Abend | erst nach `siri_frei`, wie alle ihre Szenen |
| Siri · *One Star* | 3 | 4 | 6 | Nacht | langsam und ohne Kamera; führt in die Intim-Szene |
| Siri · *Salmon* | 4 | 4 | 9 | Abend | der Lachsfarm-Vertrag gegen ihren Vater |
| Siri · *My Own Words* | 5 | 5 | 15 | Nacht | ihre erste eigene Bildunterschrift |

**Schwestern-Regel.** Mit Lea zusammen: Sophias *The Last Train* kommt nicht. Mit Sophia zusammen: Leas *What Are We?* kommt nicht.

**Fokus.** Flirt-Events (`knistern`) mit den zwei Frauen, denen Duc am nächsten ist, kommen dreimal so oft (`ereignisse.FOKUS_FAKTOR`). Gags und Geschichten bleiben Zufall. Der Bericht `docs/brain_trust/BEZIEHUNGSKURVE.md` misst die längste Stille je Frau, Ziel: höchstens 3 Spieltage.

**Alte Events reagieren.** 17 Flirt-Events unter vier Augen bekommen nach der ersten gemeinsamen Nacht eine zusätzliche Zeile (`ZUSATZ` in `ereignisse_romanzen.py`). Erste Annäherungen wie Siris „Is it too soon to ask you out?“ kommen danach nicht mehr (`NUR_DAVOR`).

**Zwei Takte.** Szenen mit einer Pause laufen über die Folge `direkt` (`ereignisse.direkt_ziel`): Der zweite Takt wird nie von
selbst gezogen.

**Rosis Strichliste.** Der Platzhalter `{striche}` zählt wirklich die Szenen mit ihr, mindestens 3 (`ereignisse.striche`).

**Echo am nächsten Morgen** (`rm_e_*`). Beim nächsten Frühstück sagt sie unter vier Augen etwas dazu, vertont und mit eigener
Antwort. Es gibt ein Echo für die erste Nacht, die zweite Nacht, Kuss oder Nähe, ein Nein, Versetzen (`stood_up`) und Eifersucht
(`verletzt_<id>`), dazu für einzelne Szenen. Die Anlässe sind drei Tage frisch, danach verfallen sie. Das Echo markiert den
Moment als aufgegriffen, die freie Szene wiederholt ihn dann nicht.

**Status in der freien Szene.** Die Folge `fakt` schreibt eine private Tatsache in die Chronik, zum Beispiel dass die beiden
jetzt zusammen sind. Das Modell behandelt sie als hart und erfindet nichts dazu.

**Noch offen:** Festa-Szenen (Akt 3), darunter Chiaras Zehn, und die Abstände zwischen den Stufen. Der Spieltest zeigt Rosi auf Vertrauen 5
ab Tag 3 (`docs/brain_trust/BEZIEHUNGSKURVE.md`), darum tragen die großen Szenen einen frühesten Tag.

## Faustregeln für das Schreiben von Inhalten

- Event-Antworten: normale gute Antwort **+4**, sehr passende **+6**, großer Moment **+8**. Fehlgriff **−2 bis −4**,
  verletzend **−6 bis −8**.
- Was über Stufe 3 tragen soll, muss ein Erlebnis sein (Event, Folge `{"wert": …, "delta": 1}`), keine Plauderei.
- Begehren nur bei Frauen, die es haben – bei allen anderen läuft eine Begehren-Folge ins Leere.

## Album (Duc 31.10.2026)

Beziehungsmenü → „Open album“. Je Frau chronologisch: ihre Selfies, die Szenen der Romanzen-Leiter und das erste Mal bei Kuss,
Geständnis und erster Nacht. Dazu eine kurze Notiz in ihrer Handschrift, nicht vertont.

- **Daten:** `werkzeuge/eden_rise/album_eden_rise.py` → `module/eden_rise/album.json`; Regeln in `kern/album.py`, gemerkt wird beim Ziehen in `z["album"]`.
- **Notizen** passen zu jedem Ausgang der Szene und sind ohne Erinnerung verständlich. Eine neue Leiter-Szene oder Selfie-Stufe ohne Notiz lässt `tests/test_album.py` scheitern.
- **Neues Selfie (02.11.2026):** Ein leuchtender Punkt sitzt auf dem Herz in der Leiste, auf dem Reiter Relationships und auf „Open album“. Der Knopf springt zu der Frau mit dem neuen Foto, dort steht NEW daran. Haben mehrere Frauen etwas Neues, tragen die anderen im Album ebenfalls einen Punkt, bis ihre Seite offen war. Szenen lösen keinen Punkt aus. Gemerkt wird im Browser je Spielstand (`eden_gesehen_<id>`), Test: `tests/test_album_punkt.py`.
- **Nicht im Album:** Favours (eigenes Geheimnis). Lea 3 fehlt, weil diese Szene mit Sophia spielt. Figuren ohne Notiz-Satz bekommen Bild und Titel ohne Notiz.
- **Später:** Die Festa-Schlussszene kann hieraus schöpfen (Rahmen + bis zu 4 Erinnerungen).

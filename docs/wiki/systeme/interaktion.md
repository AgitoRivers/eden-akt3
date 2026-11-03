# Interaktion · Tagesablauf und Events

> Stand 26.10.2026 · Besitz: Hauptsitzung (Story), bis es eine Interaktions-Sitzung gibt · Quelle: `kern/ereignisse.py`,
> `eden.py` (Ablauf), `werkzeuge/eden_rise/ereignisse_*.py` (Inhalte). Neue Mechaniken kommen hier hinein, damit Duc sie
> nachlesen kann.

## Ein Tag

Ein Tag hat sechs Phasen: **Frühstück · Tag · Nachmittag · Dinner · Abend · Nacht**. Jede Phase läuft gleich ab:

1. **Zu Beginn der Phase** können Events kommen (siehe Stufen unten). Man wählt sie nicht, sie passieren. Sie kosten die
   Phase nicht – danach geht die Phase ganz normal weiter. Vor jedem Event außer Handy und Ortskapitel steht eine
   **Zwischenkarte** (Duc 01.11.2026): Tag, Tageszeit, ein Satz, warum Duc jetzt dort ist, dazu Ort und Personen. Das Event
   und seine Stimme starten erst nach „Go on“. Der Satz kommt aus `module/eden_rise/uebergaenge.json`, sonst aus der Tageszeit.
2. **Die Phase selbst** ist entweder eine **feste Story-Szene** (Blackout, Inspektion, Anhörung …) oder **frei**: Duc
   wählt bewusst, was er tut – Zeit mit einer Person („Time with …“), Training, Missionen, Kabine (Modell B,
   zwei Aktionen pro Phase). Die **Kabine** ist keine Karte mehr (27.10.2026): Sie kostet keine Zeit und sitzt deshalb
   als runder Bildausschnitt rechts neben der Frage („Was machst du am …?“), Taste **K**. Ein goldener Punkt zeigt ein
   neues Andenken in der Keepsake Box seit dem letzten Besuch. Training mit Maxwell startet nur über die Boxhandschuhe
   in der Kabine (1 Aktion).
3. Nach der Nacht endet der Tag: Bordregeln wirken, Versprechen werden geprüft, Rosi meldet fertige Werkstattstücke.

**Diesel und Strom (seit 26.10.2026 ausgeblendet, E-076):** Beide Werte laufen intern weiter (Strom ändert sich mit dem
Wetter, Events und Jobs geben Diesel), werden aber nirgends mehr gezeigt: nicht in der Schiffsleiste, nicht als
Hinweis vor einer Wahl, nicht in Ergebniszeilen. Grund: Diesel hatte keinen Verbraucher, Strom keine spürbare Folge –
die Leiste hat etwas versprochen, das das Spiel nicht hält. Die alte Uhr „Katastrophe“ (Rest aus Gestrandet) ist weg.
**Seit 27.10.2026 gibt es Diesel und Strom als Mechanik nicht mehr (Duc, E-082)** – auch nicht als Joker in Akt 2.
Ein Kanister darf in Events weiter vorkommen – als Handlung, nicht als Zahl.
**Ausgebaut am 30.10.2026 (Duc: „Strom brauchen wir nicht mehr“):** Die Werte `strom`/`diesel` sind aus dem Modul entfernt (`basis_eden_rise.py`), die Engine ignoriert Folgen auf Werte, die das Modul nicht kennt (`zustand.folgen_anwenden`), alte Spielstände mit Strom/Diesel laufen weiter. Ersetzt: Bordregel *Three-minute showers* gibt Rosi +2 Vertrauen am Abend statt Strom +1; Arbeit zu zweit außerhalb der Technik Moral +1 (Alltag) statt Strom +1 (`kern/gesten.py`); Fund beim Erkunden nur noch 50 €. Ohne Ersatz gestrichen: Strom/Diesel in 8 Events (Kevins Nest, kalte Dusche, Drei-Minuten-Duschen jetzt ohne Strom-Bedingung, Rosis Kaltküche, Großmütter-Anruf, Strip-Poker, Diesel unter der Theke, Alvas Tanz – „I'd rather pay“ kostet nichts mehr, Alva ist nur beleidigt; Sophias missglückte Mahlzeit kostet Moral −1 statt Strom), Wetter-Strom und Moral-Abzug am Tagesende (`kern/hauptstory.py`), Batterie-/Dieselzeile im Bordstatus fürs Modell (`kern/szene.bordstatus`), Diesel/Power als Szenen-Fund, Diesel bei Totò/Alva, Strom/Diesel-Erklärung der Schiffsleiste (`eden.py`). Die drei Waren bleiben nur als ruhender Eintrag (`pausiert: entfernt`) für alte Spielstände. Unberührt: Kampfzustand *charged*, Stromausfall im Sturm (gescriptete Krise), die Solaryacht als Kulisse. Test: `tests/test_strom_raus.py`.

Akt 1 = Tag 0 (Hangar Antibes) bis Tag 7 (Anhörung, eigene Seite: [`anhoerung.md`](anhoerung.md)). Akt 2 = Tag 8–21 (zwei Wochen, Finale Belagerung an Tag 21), Akt 3 = Tag 22–35 (zwei Wochen, E-093; ersetzt Tag 22–28 aus E-083).

## Die Event-Stufen einer Phase

Jede Phase durchläuft ihre Stufen genau einmal, in dieser Reihenfolge. Nach jedem geschlossenen Event kommt die nächste
Stufe; ist keine mehr übrig, beginnt die Phase.

| Stufe | Wann | Was |
|---|---|---|
| 1. **Pflicht** | jede Phase | Events mit festem Zeitpunkt: Tag-0-Kette, Hafenkampf, Megans tägliche Sprachnachricht, Werkstatt an Tag 8. Kommen immer, sobald ihre Bedingung gilt |
| 2. **Bordrat** | nur nachts, ab Tag 2 | das Nachtprogramm der Crew, siehe unten |
| 3. **Zufall** | jede freie Phase | ein Gag, Duell, Auftritt oder Abend – nach Phasen-Chance und Gewicht |
| 4. **Handy** | jede freie Phase | eine Nachricht oder ein Anruf, eigene Spur |

**Gesperrt:** Hat eine Phase eine feste Story-Szene, oder ist es Tag 0/1 außer der Nacht, kommt nur Stufe 1.

### Akt 2: ruhiger, aber nicht leer (Duc 29.10.2026)

**Befund:** Fast alle Events endeten an Tag 6, weil sie zu Akt-1-Zeiten mit `WANN((2, 6), …)` gebaut wurden. Ab Tag 7 fand
die Engine keinen einzigen Kandidaten mehr (Bot-Diagnose 29.10.: 0 von 110 Gags, 0 von 208 Handy-Events). Akt 2 hatte
keine Selfies, Abende, Funken, Flirts und Bordräte. Der Bot sah bis Tag 14 nur 57 von gut 500 Events.

**Seitdem:**
- **225 zeitlose Events** haben ein zweites Fenster `wann.akt2 = [8, 21]`. Das sind 85 Selfies, 49 Handy, 44 Gags,
  24 Flirts, 11 Bordräte, 7 Abende/Funken sowie 5 Duelle und Auftritte. Das Akt-1-Fenster bleibt, und Tag 7
  (Anhörung) bleibt frei. Jedes Event kommt weiter nur einmal pro Durchlauf.
  - Liste: `werkzeuge/eden_rise/ereignisse_fenster.py`.
  - Geprüft mit `event_fenster_pruefen.py`, Ergebnis in `docs/brain_trust/event_fenster_pruefliste.md`.
- **Selfies, Abende und Funken laufen bis Tag 35 (Duc 30.10.2026):** `wann.akt2 = [8, 35]`, sonst steigen in Akt 3 die Stufen ohne
  Belohnung. Neu offen sind auch `ab_lola_klopft`, `ab_jana_nacht`, `ab_alva_handy`, `fk_rosi_schicht`. Kein Selfie hängt an Akt 1, alle 87 laufen bis Tag 35.
  Vorher kamen Lolas und Janas erster Abend nur in Akt 1, ihre Wiederholungen hingen daran. Megans Nacht bleibt in Akt 1 (ihr Besuch).
- **Bleiben in Akt 1:** Events mit bewusst gesetztem Story-Tag (Megans Besuch, Festa, Yamamoto- und Lola-Ketten,
  Vorabend der Anhörung). Dazu alles mit Holm im Krankenhaus, Totòs Cousin Gennaro (verschwindet in Akt 2 in der
  Grotte) und Strom/Diesel.
- **Ruhige Dichte (Duc: „eher ruhig, 2–4 am Tag“):** Ab Tag 8 sinkt die Zufalls-Chance je Phase auf 45 %, die
  Handy-Chance auf 60 %. Gags sind auf höchstens 2 am Tag begrenzt.
- **Vorrang:** Passen ein neues Akt-2-Event und ein geöffnetes, gewinnt das neue zu 65 %.
- **Code:** `kern/ereignisse.py`, `AKT2_*`.
- **Gemessen** (Bot, Seeds 7 und 3): In Akt 2 kommen 2,6–2,7 Zufalls-, Handy- und Bordrat-Events am Tag. Dazu
  kommen die Pflicht-Events der Woche. Akt 1 ist unverändert.
- **Test:** `tests/test_akt2_events.py`.
- **Offen:** 38 Events mit Akt-1-Bezug im Text (anpassen oder in Akt 1 lassen), Nachklang-Szenen zur Anhörung,
  5–8 neue Akt-2-Bordräte, Marker für Woche 3 Richtung Belagerung.

## Die Arten

| Art | Was | Kommt in | Häufigkeit / Grenze |
|---|---|---|---|
| **Bordrat** | Duc entscheidet nachts für die Crew zwischen zwei Positionen (dazu dritter Weg, Versprechen, Bordregel) | Stufe 2, Nacht | in **3 von 4 freien Nächten**; in der vierten erscheint die Meldung **„A Quiet Night“** („No crew meeting tonight“), damit es nicht wie ein Fehler wirkt. Welche Nacht ruhig ist, ist je Durchlauf zufällig |
| **Handy** | Anruf oder Nachricht, auf die Duc reagiert | Stufe 4, jede Phase | Chance je Phase: Frühstück 15 %, Tag/Nachmittag/Dinner 20 %, Abend 35 %, Nacht 45 %; **höchstens 2 am Tag**. Megans Pflicht-Sprachnachrichten zählen nicht mit |
| **gag1** | eine Figur tut etwas, das andere trifft | Stufe 3 | Gewicht 2,5 |
| **gagv** | zwei Figuren gegeneinander, Duc entscheidet | Stufe 3 (nicht beim Frühstück) | Gewicht 2,5 |
| **Duell** | Duc tritt selbst mit einer Stärke an (Küche, Handwerk, Köpfchen, Charme) | Stufe 3, Tag bis Dinner und Abend | Gewicht 1,2 |
| **Auftritt** | Duc vor Publikum (Karaoke, Gitarre, Geschichten) | Stufe 3, Abend und Nacht | Gewicht 1,2 |
| **Abend** | Vertrauens-Abend, führt in eine Intim-Szene (Lola, Alva, Jana, Megan); dazu je ein **Funke** ohne Intim-Szene für Chiara, Sophia, Lea, Rosi, Siri (siehe [`beziehungen.md`](beziehungen.md#funken)) | Stufe 3, Abend und Nacht | Gewicht **8** (Vorrang, sobald die Bedingung gilt); sagt Duc Ja, **ersetzt die Szene die freie Phase** – als einzige Art kostet sie Zeit |
| **Ort** (Expedition) | ein Frame eines Ortskapitels (Kloster) – siehe „Aufträge und Orte“ unten | nie gezogen, nur als Kette ab einem Ort | – |

**Zufall-Stufe im Detail:** Erst wird gewürfelt, *ob* ein Event kommt (Frühstück 35 %, Tag 60 %, Nachmittag 50 %,
Dinner 25 %, Abend 50 %, Nacht 80 %), dann *welche Art* nach Gewicht, dann *welches* Event dieser Art.
Gags, Duelle und Auftritte zusammen höchstens 3 am Tag, je Art höchstens 2; Abende höchstens 1.

**Welche Events passen:** Tag und Phase stimmen, Wetter passt, Bedingungen sind erfüllt (Vertrauen, Begehren, Flags),
alle Beteiligten sind da und bekannt, und die Spielerin hat das Event in diesem Durchlauf noch nicht gesehen. Megan
ruft nicht an, solange sie an Bord ist.

## Was ein Durchlauf ungefähr zeigt (Bot-Spieltest, 6 Läufe)

| Art | je Durchlauf | im Pool (Akt 1) |
|---|---|---|
| Bordrat | 3 | 30 |
| Handy | 4 (+ 6 Sprachnachrichten von Megan) | 39 |
| gag1 | 7 | 69 |
| gagv | 4 | 29 |
| Abend, Duell | je ~1 | 7 / 6 |
| **Zufalls-Events gesamt** | **~20** | **~183** |

Dazu die Pflicht-Ketten (Tag 0, Hafen). Ein Durchlauf zeigt also gut ein Zehntel des Pools – jeder Run ist anders.

## Selfie-Events (Duc 27.10.2026, ersetzt die sechs Events vom 26.10.)

Elf Frauen schicken Duc nachts Selfies: **eins je erreichter Stufe 3, 4 und 5**, also bis zu drei pro Frau und Durchlauf.
**Bibi (offen, 02.11.2026):** Ihre drei privaten Selfies fehlen noch. Prompt Studio Preset `Selfie_Bibi`, Karten `selfie_bibi_knapp`/`_oben_ohne`/`_nackt`, Reihen `selfie_bibi_haeuschen` und `selfie_bibi_station`; Duc generiert, danach Events, Texte und Album-Notizen wie bei den anderen. Ihre Tier-Selfies sind etwas anderes: [tierstation.md](tierstation.md).
Quelle `werkzeuge/eden_rise/ereignisse_selfies.py` + `selfie_daten.json` (Bilder, Texte, Nachschlag; abgenommen über
`docs/abnahme/selfies_r10` und `selfie_texte`), Spielbilder `werkzeuge/selfie_webp.py` → `module/eden_rise/selfies/`.

| Stufe | Bild | Ton der Nachricht |
|---|---|---|
| **3** | knapp bekleidet | ein Vorwand, das Eigentliche steht zwischen den Zeilen |
| **4** | oben ohne | frecher, mit einem Witz als Schild |
| **5** | nackt | verletzlich, fast ein Geständnis |

- **Wer und wann:** Tag 2–6 und Tag 8–35, abends/nachts. Romanzen (Chiara, Sophia, Lea, Rosi, Siri, Lola, Alva) über **Begehren**
  3/4/5, Siri erst nach Yasin (`siri_frei`). Ohne Begehren zählt **Vertrauen** 3/4/5: Megan und Elsa nur darüber (Duc 30.10.2026). Zwei Riegel bleiben, weil die Geschichte sie verlangt und beide in Akt 2 erreichbar sind:
  Jana `jana_abend` (ihre Nacht), Isabelle `isabelle_handy`
  (Ducs Nummer am Ende des Kloster-Kapitels im Kräutergarten, `kl_garten`, nur wenn Frederico lebt).
- **Reihenfolge:** Stufe 4 erst nach Stufe 3, Stufe 5 erst nach 4. Springt Begehren von 2 auf 5, kommen die drei Fotos an
  aufeinanderfolgenden Abenden.
- **Vorrang:** Ist ein Selfie fällig, kommt es ohne Würfeln in der nächsten Abend- oder Nachtphase (Handy-Spur, höchstens
  zwei Handy-Events am Tag). Das Foto ist die Belohnung genau dann, wenn die Beziehung eine Stufe weiter ist.
- **Reihe (Hintergrund):** Jede Frau hat 2–3 Reihen (z. B. Alva: Bar, Zimmer, Tresen). Das erste Selfie würfelt eine aus,
  die nächsten bleiben dabei, solange die Reihe die Stufe hat; sonst kommt eine andere (`kern/ereignisse._selfie_auswahl`).
  Jeder Durchlauf zeigt also andere Bilder.
- **Nachrichten:** echter Handy-Chat, 2–3 Blasen mit Emojis (STIL.md); die Stimme liest Emojis nie (`stimme.ohne_emoji`).
- **Antworten** (Romanzen; ohne Begehren wird daraus Vertrauen). Das Foto ist die Belohnung, nicht der Antrieb zur nächsten
  Stufe (Duc 30.10.2026, vorher +6/+8):
  - Necken: Begehren +2, Vertrauen +2, sie antwortet.
  - Kompliment mit Probe (SG 12/13/14 je Stufe): Begehren +3, Nachklang und das Foto als **Andenken**
    `<frau>_selfie_<stufe>`; Fehlschlag Begehren +1.
  - Gentleman: Vertrauen +6 (ohne Begehren +2).
  - **„Leaves it on read.“**: nichts sofort, aber in der nächsten Phase kommt ihr **Nachschlag** (Vorrang wie oben).
  - **Antworten je Foto (Duc 31.10.2026):** Titel, Necken und Gentleman passen zum jeweiligen Foto (`PASSEND` in
    `ereignisse_selfies.py`). Nur ihre Antwort auf das Kompliment ist je Stufe gleich, sie ist das Echo des Andenkens.
    Das Andenken trägt den Titel des Fotos, das Duc gesehen hat. Bezieht sich ein Foto auf ein früheres (Hemd, Jacke,
    Skala), erinnert die Lage daran (`LAGE`). Die Nachschläge gelten für alle Reihen und nennen deshalb nichts aus einem
    einzelnen Foto.
- **Nachschlag:** je Frau und Stufe zwei Blasen.

  | Art | Wer | Antworten | Liegen lassen |
  |---|---|---|---|
  | Reue („das war dumm, lösch das“) | Alva, Elsa, Isabelle, Jana, Lea, Lola, Siri | Vertrauen +4, Begehren +2 | Vertrauen −2 |
  | Offensiv | Chiara, Megan | Begehren +2 | Begehren −4 |
  | Gekränkt | Sophia, Rosi | Begehren +2, Vertrauen +2 | Begehren −4 |
- **Andenken:** liegt in der Keepsake Box und zeigt genau das Selfie, das Duc bekommen hat (`z.selfie_bilder`); Echo ist
  ihre Antwort auf das Kompliment.

## Ton der Events

Jedes Event hat einen Ton: **witzig · wholesome · frech · ernst**. Ziel: witzig ~35 %, wholesome ~25 %, frech ~25 %
(Duc 25.10.), ernst ~15 %. Die aktuelle Mischung zeigt der Builder beim Bau (`werkzeuge/eden_rise/ereignisse_basis.py`).

## Erzählerin bei Ortsbildern (Duc 02.11.2026: „extrem gut“)

Öffnet sich ein Ortsbild (`art: "ort"`, 295 Stück), liest die Erzählerin zuerst den Lagetext vor, danach sprechen die
Figuren ihre Zeilen wie bisher. Nach der Wahl spricht nur noch die Antwort. Der Schalter für die Stimme gilt auch für sie.

- **Stimme:** `eden-config.json` → `stimmen.eden_rise.erzaehler` (Figur `erzaehler`, `szene.ERZAEHLER`).
- **Aufnahmen:** vorab vertont, Schlüssel `<event>#l`, Text = Lage ohne `*`. Lagen mit `{Platzhalter}` bleiben stumm.
  Neu oder geändert: `Vertonen_EdenRise.bat --wer erzaehler` (alles in einem Lauf: ohne `--wer`).
- **Code:** `eden.event_zeile` (Teil `l`), Client `evSprich` setzt `["lage", <id>#l]` vor die Zeilen; im normalen
  Event-Fenster wird die Lage hell, solange sie läuft. Server-Text und Vertonungs-Text müssen gleich sein, sonst findet
  `stimme.chatterbox` die Aufnahme nicht: `tests/test_erzaehlerin.py` prüft das für alle Ortsbilder.
- Andere Events (Abende, Gags, Bordrat) haben keine Erzählerin. Ob sie das auch bekommen, entscheidet Duc später.

## Crew-Stimmung (Moral, Duc 27.10.2026, Variante C)

Die Moral ist die **Wochenstimmung der Crew**. Sie läuft von **−5 bis +5**, Start 0. Im Spiel steht nur ein Wort mit
Gesicht in der Leiste links oben, die Zahl erscheint im Tooltip:

| Wert | Stufe | Was sie bewirkt |
|---|---|---|
| +4, +5 | 😄 **Buzzing** | Würfel +1 („Lea's got your back“), Bordrat: dritter Weg mit **Vorteil**, Geschenk beim Frühstück (70 %), Crew-Sprites freudig, Megans Geduld +1 |
| +1 … +3 | 🙂 **Good** | eher witzige und wholesome Events, Szenen etwas wärmer |
| 0 | 😐 **Calm** | nichts – der Normalzustand |
| −1 … −3 | 😟 **Tense** | Bordrat: dritter Weg **SG +2**, Crew-Sprites genervt, eher ernste Events, Megans Geduld −1; ab **−2** Würfel −1 („The crew is sulking“) |
| −4, −5 | 😠 **Mutinous** | alles von Tense, noch mehr ernste Events; brennt am Ende die Batteriebank, ist das Schiff verloren |

**Wie sie sich bewegt** (Code: `kern/moral.py`, Zahlen: `modul.json → moral`, Builder `modul_eden_rise.py`):

- **Momente zählen doppelt, in beide Richtungen.** Events, Bordrat, Missionen, Anhörung, Ermittlung: Steht in den
  Daten Moral +1, gibt es +2; steht −1, gibt es −2.
- **Alltag gibt +1, aber nur bis +2 (Good).** Das sind Kochen für die Crew, Gesten der Art „Entspannung“, die
  Szenen-Reaktion „crew up“ und die Bordregel „Food is shared“. Wer jeden Tag kocht, kommt so nicht in Hochstimmung,
  aber aus dem Minus heraus. Für Buzzing braucht es Momente. (Der Kanister Trinkwasser, früher Moral +1 beim Kauf, ist
  seit 27.10. gelöscht: Konsum gibt keine Moral.)
- **Moral aus Essen gibt es nur durchs Kochen für die Crew** (Duc 27.10.), höchstens einmal am Tag (Zähler
  `essen_heute`). **Konsum gibt nie Moral:** Was Duc isst oder trinkt (Snacks, Kuchen, Energy Bar, Doppio), wirkt nur
  auf ihn; Schenken wirkt nur auf die Person; es gibt kein „Teilen“. Tim Tam Slam, Cannoli, Brownie, Kubanischer Rum,
  Fresh Catch und Lolas Pesto haben deshalb keine Moral-Wirkung mehr.
- **Jede Nacht −1**, solange die Moral über 0 liegt. Unter 0 erholt sie sich nicht von selbst.
- **Genau so, wie es dasteht**, zählen die vier Tiefpunkte im Code:

| Tiefpunkt | Moral |
|---|---|
| Bordrat, dritter Weg gelungen / misslungen | +2 / −2 (zusätzlich zu den Folgen der Option) |
| gebrochenes Versprechen | −2 |
| Patzer (natürliche 1) vor der Crew, also in einer Probe mit Chiara, Sophia, Lea, Rosi oder Lola | −1 |
| Crew-Mission endgültig verpatzt (zweiter Fehlschlag) | −1 |

**Würfel:** Der Bonus gilt bei Proben, an denen die Crew beteiligt ist: Events mit ihr, Szenen mit ihr, Missionen
von ihr. Bei Buzzing nennt der Bonus die Anwesende mit dem höchsten Vertrauen.

**Frühstück:** Am Morgen meldet der Tageswechsel erst den Verfall, dann eine Zeile zur Stimmung (zwei Varianten je
Stufe). Bei Buzzing legt mit 70 % jemand aus der Crew einen Kampf-Verbrauchsgegenstand dazu, höchstens einen am Tag
und erst die, die Duc noch nicht bekommen hat: Chiara Pflaster, Verband und First Aid Kit; Lola Espresso, Doppio und
Americano; Lea Mate und Hundefutter; Sophia Grünen Tee; Rosi Panzertape und den grauen Schleifstein. Seit 27.10.2026
stehen alle im Modul und wirken im Kampf (Tabelle in `kampf.md` „Gegenstände“); das Megafon gibt es seitdem bei Megan
im Eden-Shop statt von Sophia.

**Lolas Frühstücksgeschenke** (Duc 27.10.): unabhängig von der Moral, solange Lola an Bord ist. Sie schenkt
höchstens jeden zweiten Morgen etwas, und nie zusätzlich zu einem Crew-Geschenk (ein Geschenk je Frühstück). Geprüft
wird in dieser Reihenfolge, der erste Treffer gewinnt:

| ab Vertrauen | Geschenk | Chance je Morgen | eigene Pause |
|---|---|---|---|
| 4 | **Space Cake** (im Kampf: heilt wie ein Snack, dazu +1 Ausdauer je Runde, 5 Runden) | 20 % | 3 Tage |
| 3 | **Energy Bar** (+1 Energie beim Benutzen) | 35 % | 2 Tage |
| 2 | **ein Snack aus ihrer Kombüse mit Tipp**, wer ihn liebt („Lamingtons. Take them to Totò, mate.“) | 35 % | 2 Tage |

Sie schenkt nur, was Duc gerade nicht im Inventar hat (ist es
schon da, prüft sie den nächsten Eintrag), und bei vollem Inventar nichts. Den Snack wählt sie zuerst für Figuren, deren Vorliebe Duc noch nicht kennt; die Vorliebe zählt danach als entdeckt
(♡ im Figurenprofil). Space Cake und Brownie „Captain's Calm“ (ab Vertrauen 4) sind nicht im Snack-Topf. Im Test (78
Morgen) kommen bei Vertrauen 2 20, bei 3 27 und bei 4 29 Geschenke (davon 8 Space Cakes), also knapp zwei bis
drei pro Woche. Tabelle
`MODUL["morgen_geschenke"]` (weitere Figuren lassen sich dort eintragen).

**Szenen:** Bei Good, Tense und Mutinous bekommt jede Crew-Figur in der Szene einen Satz zur Stimmung in den
Auftrag. Bei Calm bekommt sie keinen.

**Event-Ton:** Der Zufall zieht innerhalb einer Art nach Ton-Gewicht: Bei Buzzing kommen witzige und wholesome Events
×1,5 und ernste ×0,6. Bei Tense kommen ernste ×1,5, bei Mutinous ×2.

**Harte Optionen (27.10.2026):** Vorher hatten 144 Event-Stellen +Moral und nur 7 −1. Jetzt kosten **25 verlockende
Optionen** Moral −1 (also −2): Geld, Reparatur, Energie oder Vertrauen bei *einer* Figur gegen die Laune aller. Ein
Beispiel ist „Yasin can film. He pays for the footage.“ (+120 €). Dazu kommen **6 neue Reibungs-Events**, bei denen
zwei aus der Crew aneinandergeraten:

| Event | Wer | verlockend (Moral −1) | nett (Moral +1) |
|---|---|---|---|
| `gv_dienstplan` The Rota | Chiara / Sophia | Chiaras Doppelschichten (Rückhalt +3) | freier Nachmittag |
| `gv_trinkgeld_topf` The Tip Jar | Lola / Rosi | Motorkasse (Reparatur +1) oder Schiffskonto (+150 €) | teilen |
| `gv_musik_nachts` After Midnight | Lea / Chiara | Licht aus (Energie +1) | weitertanzen, Kopfhörer (−40 €) |
| `gv_gute_kabine` The Good Cabin | Sophia / Lola | an Yasin vermieten (+120 €) | Los ziehen |
| `gv_ruhetag` Sunday | Rosi / Lea | alle arbeiten (Reparatur +1) | Strandtag |
| `gv_einkaufsliste` Lola's Shopping List | Lola / Chiara | Dosen (+60 €) | Lolas Liste (−80 €) |

Gestrichen wurden die fünf schwächsten Events des Rankings, an denen nichts hing: `g1_qualle`,
`hy_casanova_rede`, `hy_eden_hotline`, `gv_tarot` und `gv_wahrheit_pflicht`. Umgebaut, jetzt mit Moral-Preis auf einer
Seite, wurden `g1_kalte_dusche`, `gv_ocean_glitter`, `gv_festa_outfits`, `gv_kevin_auktion` und `hy_megan_dinner`.

**Abschluss:** Die Gemeinschafts-Rechnung zählt mit der alten Skala 0–5 als 3 + Moral/2, abgerundet.

**Simulation** (27.10.2026, 20 Bot-Läufe durch die echte Engine, Moral an jedem Morgen von Tag 2 bis 7):

| Spielweise (je 4 Läufe) | Buzzing | Good | Calm | Tense | Mutinous | tiefster Wert | Geschenke |
|---|---|---|---|---|---|---|---|
| **nett** (nimmt die Option mit der meisten Moral) | 62 % | 21 % | 12 % | 4 % | – | −1 | 12 |
| **zufällig** | 42 % | 29 % | 29 % | – | – | 0 | 9 |
| **nachlässig** (zufällig, kocht nie, keine Gesten) | 12 % | 42 % | 33 % | 12 % | – | −2 | 2 |
| **immer die erste Option** (wie das Gate) | – | 29 % | 46 % | 25 % | – | −2 | 0 |
| **gierig** (Geld, Reparatur, Vertrauen vor Moral) | 4 % | 38 % | 38 % | 12 % | 8 % | −5 | 1 |

Hochstimmung muss man sich verdienen. Wer nett entscheidet, bleibt fast die ganze Woche oben. Tense gibt es nur
durch eigene harte Entscheidungen oder Nachlässigkeit, und Mutinous erreicht nur, wer die Laune für Geld verkauft
(ein gieriger Lauf: −4, −5, −3).

Test: `tests/test_moral.py`.

## Freie Phasen: „Time with …“

Kein Event, sondern eine Aktion: Duc wählt in einer freien Phase, Zeit mit einer Person zu verbringen. Die Szene spielt das
Sprachmodell (Gespräch, Gesten, Geschenke); sie zählt als Aktion der Phase.

**Wer angeboten wird** (`kern/hauptstory.frei_phase`, Spieltest 29.10.2026): Die Romanzen (Chiara, Sophia, Lea, Rosi, Siri,
Lola, Alva) und die Nebenfiguren aus `rollen.freie_zeit_extra` (Holm, Maxwell, Totò, Petru, Jana), jeweils an ihrem Ort
und nur, wenn der Ort offen ist (Petrus Werkstatt: Schlüssel, Ruf 2 oder mit Rosi; Holm nur bis Tag 2). Wer lange nicht
dran war, kommt zuerst. Bei zwei oder mehr Karten gehört in **etwa jeder zweiten Phase eine Karte der Nebenfigur**, die
am längsten nicht dran war; alle anderen Karten bleiben den Romanzen. Messung Tag 1–15 (`tests/test_freie_zeit.py`):
Romanzen rund 80 % der Karten, Maxwell, Totò, Petru und Jana je 10–18 (vorher im Spieltest: Maxwell 4, Totò 2, Petru 0).
Texte sind geschlechtsneutral (Vorlagen `story_buehne.py` FREI; Wunsch „in his/her own way“ nach `pronomen`).
Personen mit `frei_immer` (bisher nur **Ligeia**, die nur nachts am Teich ist) bekommen den Nebenfiguren-Platz immer,
wenn sie da sind (29.10.2026).

**Wie die Figur spielt** (`kern/szene.figur_prompt`): Die Regeln stehen mit dem richtigen Pronomen (`pronomen` „er“ →
he/his). Jede Hauptfigur hat 4 **eigene Gesten** aus ihrer Wiki-Seite (`GESTEN` in `modul_eden_rise.py`, z. B. Petru
flickt ein heiles Netz, Holm trinkt ihren Kaffee schwarz und kalt, Sophia schreibt in ihr Lederbüchlein) – höchstens eine
pro Antwort. Körpersprache-Floskeln sind verboten („lets out a …“, „freezes“, „voice dropping“, „eyes widen“, „cheeks
flushing“ …, Liste `szene.FLOSKELN`); was eine Figur in der Szene trotzdem schon benutzt hat, wird für ihre nächsten
Antworten ausdrücklich gesperrt (`floskeln_der_szene`).

## Schnelljobs (Missionen übers Handy) – abgeschaltet seit 29.10.2026

**Duc, 29.10.2026: Die Favours ersetzen die Schnelljobs.** In eden_rise steht `modul["schnelljobs"] = False`
(`modul_eden_rise.py`, Schalter `kern/handel.jobs_aktiv`): kein Reiter „Jobs“ am Handy, kein Tagesangebot, keine
Besorgungstasche, keine Besorgungs-Teile in den Läden, `job_machen` lehnt ab. `missionen.json` (68 Missionen) und der
ganze Job-Code bleiben, damit sich das umkehren lässt (Schalter auf `True`, neu bauen); `tests/test_missionen.py`,
`test_energie_hinweis.py` und `test_wuerfel_http.py` prüfen die Mechanik mit eingeschaltetem Schalter,
`tests/test_schnelljobs_aus.py` prüft, dass nichts mehr zu sehen ist.

**Was an den Jobs hing und wohin es gewandert ist:**
- **Zwölf einzigartige Geschenke** (Lohn der Ketten): Tasse für Chiara, Werkstattschild für Rosi, Füller für Sophia,
  Tauchcomputer für Lea, Ratgeber für Siri, Vegemite für Lola, Kastagnetten für Alva, San Gennaro für Totò, Goldbrille für
  Yasin, Strafzettelblock für Elsa, Pfeifentabak für Petru, Konfettikanone für Casanova. Sie liegen jetzt als **feste Ware
  bei Totò** (`laeden.toto.fest`, immer im Angebot, ausserhalb der Rotation) ab Vertrauen 3, für 60–190 €.
- **Crew-Karte für Megan** (`megan_crewkarte`): nicht kaufbar, kommt als Dank von Lolas Favour-Kette.
- **festa_invite** und **petrus_hammer**: vergeben auch Events (Casanova an Tag 8, Gag Petru/Rosi) – nichts verloren.
- **Werte** (Ruf, Moral, Strom, Diesel, Reparatur-Uhr), die einzelne Jobs gaben, fehlen: siehe die Messung unten.

**Messung 29.10.2026** (Bot aus `tests/lauf_test.py`/`geld_messung.py`, 8 Seeds, bis Tag 15; vorher = Jobs an + Favours,
nachher = Jobs aus + Favours + feste Ware bei Totò; Skript `tests/vertrauen_messung.py`):

| | vorher | nachher |
|---|---|---|
| Vertrauen **5** erreicht (von 8 Läufen) | Lola 7 · Lea 4 · Chiara 3 · Petru, Alva, Elsa, Rosi, Siri, Totò 0 | Lea 2 · Chiara 1 · alle anderen 0 (auch Lola) |
| Vertrauen am Ende (Median) | Lola 5 · Lea 5 · Rosi 4 · Totò 4 · Alva 3,5 · Petru 3 · Elsa 1,5 | Lola 4 · Lea 4,5 · Rosi 4 · Totò 3 · Alva 2 · Petru 1,5 · Elsa 1,5 |
| Konto am Ende, Bot „sparsam“ / „normal“ | 3549 € / 2426 € | 3430 € / 2534 € |
| Einnahmen aus Missionen (Median) | 425 € / 240 € | 80 € / 40 € |
| Ruf · Strom (Median am Ende) | 1 · 4 | 0 · 1 |
| Energie morgens: Anteil 3 von 3 · Anteil 0 | 62 % · 0 % | 81 % · 0 % |

Lesart: Petru, Alva und Elsa erreichten Vertrauen 5 **auch vorher nie** (Charm und Selfie dort kamen im Bot-Lauf nicht
vor); Lola verlor Vertrauen 5, weil ihre vier Job-Ketten wegfielen. Strom fällt auf 1 (die Ersatzzellen-Jobs fehlen,
Totò und das Dorf verkaufen Batterien und Reiniger). Energie hat nur noch die Favours als Verbraucher und ist nie knapp.
Die Zahlen gingen als Vorschlag an „Ende Rise & Apps“; Werte sind **nicht** verändert worden.
- Die Items der Missionen mit `quelle: mission` ohne Job (z. B. Lolas Band, Elsas Taschenlampe) waren schon vorher nicht
  erreichbar – offen, nicht Teil dieser Umstellung.

*Die Beschreibung der Mechanik (gilt unverändert, wenn der Schalter an ist):*

Quelle: `werkzeuge/eden_rise/missionen_eden_rise.py` → `module/eden_rise/missionen.json`, Code `kern/handel.py`
(`jobs_heute`, `job_machen`). 68 Missionen.

- **Wie sie kommen:** Als **Schnelljobs über das Handy**. Jeden Tag zeigt das Handy die Aufträge, die gerade passen:
  Tagesfenster (`tage`), Mindest-Vertrauen bei der Auftraggeberin (`ab_vertrauen`), Kette (`nach` = erst nach Erfolg
  einer anderen Mission).
- **Was sie kosten:** **1 Energie** (Energie 0–3, pro Tag kommen 2 dazu) und einen **W20-Wurf** auf ein Attribut gegen
  einen Schwierigkeitsgrad. Reparieren gibt den Vorteil *Handwerk*, Kochen den Vorteil *Küche*, ein passendes Werkzeug
  aus dem Inventar ebenfalls einen Vorteil.
- **Ohne Energie** (Duc 29.10.2026: Energie bleibt, kein Joker): Jobs mit Wurf sind bei 0 Energie **gleich ausgegraut**,
  nicht erst nach dem Klick abgesagt. Die Karte in der Jobliste ist grau und trägt „needs 1 energy“, in der Mission
  steht der gesperrte Knopf „Needs 1 energy“ und darunter, woher Energie kommt: ein Energie-Item aus der Tasche mit
  Namen (z. B. „Use the Lola's Energy Bar in your bag …“), sonst „An espresso, a relaxed hour with the crew, or tomorrow
  morning“. Bei einer Gruppe ist die Karte nur grau, wenn alle Wege einen Wurf brauchen. Abgaben und sichere Wege bleiben
  klickbar. Code: `handel.jobs_heute` (`energie_fehlt`), `handel.energie_tipp`; Test `tests/test_energie_hinweis.py`;
  Vorschau `tests\vorschau_server.py --tag 3 --frei --energie 0`.
- **Abgaben:** Missionen mit `braucht` wollen einen Gegenstand (Eichenbrett, Safran …). Der wird abgegeben – kein Wurf,
  keine Energie, sicher.
- **Mehrere Wege:** Eine Gruppe (`gruppe`) bietet verschiedene Wege zum selben Ziel (Eis holen, selbst reparieren,
  Totò fragen); ein Erfolg schließt die anderen.
- **Lohn:** Geld, Ruf, Werte, Gegenstände. Die Frauen der Crew zahlen nicht: Erfolg bringt Vertrauen, mit
  `persoenlich` auch Begehren.
- **Fehlschlag:** am nächsten Tag noch einmal; nach dem zweiten Fehlschlag halber Lohn, und die Mission ist vorbei.
- Die großen Missionen mit Ort, Schritten und Abschluss sind die **Aufträge** (unten); die Bitten der Crew sind die
  **Favours** (nächster Abschnitt).

## Das Dorf, das redet (seit 30.10.2026)

Legenden zu Ducs Missionen, Ruf im Dorf als Wort, Verblassen: eigene Seite [dorf_redet.md](dorf_redet.md).

## Favours (Bitten übers Handy, seit 29.10.2026)

Quelle: `werkzeuge/eden_rise/ereignisse_favours.py` (im Event-Bau), Code `kern/ereignisse.py` (`_favour_ziehen`,
`favour_journal`), Fotos `werkzeuge/favour_fotos.py` → `module/eden_rise/favours/fv_<kette>.webp`, Test
`tests/test_favours.py`. Brain Trust Option C (Duc 29.10.): Eine Figur bittet Duc per Handy um einen Gefallen – kein
Listenpunkt, sondern ein kleines Erlebnis mit vertonter Pointe. **Duc will die Inhalte nicht vorab kennen**: Hier
steht nur die Mechanik, Texte und Fotos stehen allein im Builder.

- **Ketten:** 9 Figuren mit je **3 Bitten** und einem **Dank-Foto**. Die neunte ist Ligeia (seit 30.10.2026): kein Handy, sondern Flaschenpost auf der Badeplattform (`flasche=True`, Event art `abend`), der Dank ist ein Polaroid. Ab Tag 2: Lola, Alva, Petru, Elsa (laufen in
  Akt 2 weiter). Ab Tag 8: Jana, Maxwell, Nonna und Isabelle (die beiden erst mit Isabelles Nummer, Flag
  `isabelle_handy`). Wer Duc noch nicht kennt (`bekannt`), bittet nicht.
- **Takt:** höchstens **eine Bitte am Tag**, mittags, nachmittags oder abends (Chance 35/35/30 %). Laufende Ketten
  kommen zu 60 % vor einer neuen; Teil 2 und 3 frühestens am Tag nach dem vorigen Teil. Ein fälliger Dank kommt ohne
  Würfeln. Bitten kommen in der Event-Reihe nach den Zufalls-Events und vor den übrigen Handy-Events und **zählen zu
  den höchstens zwei Handy-Meldungen am Tag** (das Handy bleibt ruhig).
- **Antworten:** **zwei Wege mit Probe** (je **1 Energie**, ohne Energie ausgegraut mit „needs 1 energy“) und
  **Ablehnen** (kostenlos, art `auflegen`, beendet die Kette, Vertrauen −1). Beide Ausgänge haben eine eigene
  vertonte Pointe (`zeile` / `zeile_fehlschlag`, Stimmschlüssel `<id>#o<i>` / `<id>#f<i>`).
- **Lohn:** Erfolg Vertrauen +8 (Finale +10; Duc 29.10.2026 ×1,6, vorher +5/+6 – Messung 8 Seeds bis Tag 15: Lola Stufe 5 in 5/8 statt 0/8, Elsa Median 1,5 → 2), Fehlschlag +1 – die Kette geht trotzdem weiter. Nur ein **geglücktes
  Finale** bringt das Dank-Foto (zwei Antworten, je Vertrauen +3). Geld gibt es bei einer einzigen Figur.
- **Flags:** `fv_<kette>_<n>` (datiert, Bedingung `flag_seit`), `fv_<kette>_<n>_ok` bei Erfolg, `fv_<kette>_aus` beim
  Ablehnen. Neuer Bedingungs-Baustein `{"bekannt": pid}` (`kern/regeln.py`).
- **Im Handy** trägt die Bitte den Chip „Favour“; das Dank-Foto zeigt das Handy wie ein Selfie (antippen = groß).
- **Bot** (`tests/lauf_test.py`): nimmt Bitten an, solange die Energie reicht, sonst den kostenlosen Weg.

## Aufträge und Orte (E-074, seit 26.10.2026)

Quelle: `werkzeuge/eden_rise/auftraege_eden_rise.py` → `module/eden_rise/auftraege.json`, Frames in
`werkzeuge/eden_rise/ereignisse_kloster.py`, Code `kern/auftraege.py` und `eden.py` (`ort_betreten`, `ort_frame`).

**Zwei Arten von Missionen:** Schnelljobs (oben, übers Handy, ein Wurf) und **Aufträge**: Eine Figur bittet Duc um
etwas Größeres. Ein Auftrag hat

- eine **Annahme** (ein Event, z. B. Casanova am Hafen an Tag 8 → Flag `kloster_angenommen`),
- einen **Ort**, den Duc aufsucht, und **Schritte**, die das Journal abhakt,
- mindestens **eine graue Entscheidung** (E-073; der Builder bricht ab, wenn eine fehlt),
- einen **Abschluss bei der Auftraggeberin** mit Übergabe (Kloster: Le Large),
- **Romanze:** Ist die Auftraggeberin eine Frau mit Begehren, hebt der Abschluss ihr Begehren auf die nächste Stufe.

**Journal (Menü, Taste N):** zeigt angenommene und erledigte Aufträge – Auftraggeberin, Ort, nächster Schritt,
alle Schritte mit Haken, getroffene graue Entscheidungen, Belohnung. Seit 29.10.2026 getrennt in **Main orders**
(Hauptaufträge), **Side orders** (Aufträge mit `"neben": true` im Builder, z. B. der alte Graue und Mazzera) und
**Done**. Daneben die Rubrik **Favours**: je Kette die Bitten, die Duc schon bekommen hat, mit Ausgang (✓ helped,
✗ didn't work out, – said no) und dem Dank-Foto (antippen = groß); die Schnelljobs des Tages stehen nur dort, wenn
es welche gibt. Der Reiter selbst kommt von der Items-Sitzung (Menü), die Daten liefert die Engine unter `journal`
und `favours`.

**Nebenaufträge, optionale Schritte, Frist (Duc 29.10.2026, Quest-Designer-Durchgang):**
- **Page Forty** (Lea, `kevin`): Kevins Dächer, Tag 12–14. Nebenauftrag (`neben`), Frist `bis_tag` 15: wer die Seite
  nicht holt, sieht den Eintrag danach unter *Done* als **Missed**. Graue Wahl „Kevin's treasure“ (`kevin_stift` /
  `kevin_fair`).
- **High Tide** (Totò, `grotte_flut`): erscheint, sobald die Grotte fertig ist (`grotte_fertig`), ohne Spoiler im Text.
  Schritte: allein bei Flut hinausrudern · zum schwarzen Teich · „Listen to what the sea keeps“. Graue Wahl „The humming“
  (`fn_geredet` / `fn_gegangen`); wer sich zurückzieht, lässt ihn offen („another night“).
- **Bedienung des Journals** (UX-Durchgang 29.10.2026, `eden-menu.js`): oben eine feste Leiste mit Zählern und Sprungmarken
  („1 main · 4 side · 2 done · 0 favours“); der nächste Schritt steht **hervorgehoben in der Schrittliste** („· NEXT“),
  nicht mehr in einem zweiten Kasten; erledigte und verpasste Aufträge sind **einzeilig eingeklappt** (Klick klappt auf);
  erledigte Schritte sind gedimmt mit Haken statt durchgestrichen. **Abzeichen für Neues:** Beim Öffnen des Journals
  steht „NEW“ (nie gesehen) oder „UPDATED“ (Schritt oder Wahl hat sich seit dem letzten Besuch geändert) an der Karte,
  auch an Favours; das merkt sich der Browser je Spielstand (`localStorage eden_journal_<id>`). Am Reiter „Journal“ der
  Menüleiste sitzt ein Punkt, wenn sich ein offener Auftrag oder sein nächster Schritt geändert hat (gleiche Regel wie der
  Punkt im Dock, `EdenMenu.punkt`). **Auf- und zuklappen:** Jeder Auftrag klappt per Klick auf seinen Kopf (oder Enter/Leertaste)
  auf und zu. Beim Öffnen des Journals sind **Hauptaufträge und alles mit NEW/UPDATED offen**, die übrigen Nebenaufträge und
  alles Erledigte **zu**; eine zugeklappte Zeile zeigt bei laufenden Aufträgen den nächsten Schritt („· next: …“). Die
  Klick-Wahl gilt, solange das Journal offen bleibt; beim nächsten Öffnen gilt wieder der Standard.
  **Ort und Frist:** Unter dem Titel eines laufenden Auftrags stehen zwei Marken: der **Ort mit seinen Tageszeiten**
  („Kevin's Rooftops · Midday, Afternoon“, aus `orte[...].phasen`) und die **Frist** („until day 14 · 3 days left“, aus
  `bis_tag` des Auftrags; angezeigt wird der letzte Tag = `bis_tag − 1`). Bei höchstens 2 Tagen Rest wird die Frist rot
  („last day“ am letzten Tag); abgelaufen steht „ended day N“. In der zugeklappten Zeile steht nur der Rest („2 days left“).
  Frist haben Kevins Seite (bis Tag 14) und High Tide (bis Tag 21; der Ort schliesst mit Tag 22, danach „Missed“).
- **Optionale Schritte** (`optional`, `wenn`): Die Grotte zeigt ihre beiden Umwege als „· optional“-Schritte mit gestricheltem
  Punkt, erst wenn Duc den Abzweig erreicht hat (Ruf vom ertrunkenen Strand nach den Ratten, Taucher nach der Halle).
  Sie sind nie der „Next step“ und blockieren nichts; ein erledigter bleibt sichtbar. Engine `kern/auftraege.journal`,
  Anzeige `eden-menu.js`, Test `tests/test_journal_nebenquests.py`.

**Orte in der freien Phase:** Ist ein Auftrag angenommen, erscheint sein Ort als eigene Karte neben den Szenen
(„The Macchia · expedition · whole phase“). Ein Ort braucht **die ganze Phase** wie eine Szene – geht nur, solange
noch keine Aktion verbraucht ist. Die Macchia ist mittags und nachmittags offen.

**Wie ein Ausflug abläuft (Frame-Kette):**

1. Jeder Frame ist ein Bildschirm mit eigenem Hintergrund, Lage, Figuren und 1–4 Antworten.
2. Nach dem Schließen öffnet sich der nächste Frame. Hängt an der Antwort ein **Kampf**, kommt erst der Kampf –
   nach einem Sieg (K.O., Aufgabe, Gegner flieht) geht es zum nächsten Frame.
3. **Flucht** aus einem Kampf oder eine Antwort ohne Weiterweg („Turns back“) beendet den Ausflug.
4. **Niederlage** (Expedition, siehe [`kampf.md`](kampf.md)): Schwarzblende, Duc wacht auf dem Schiff auf, eine
   Phase ist weg, er behält genau ein Fundstück. Beim nächsten Besuch beginnt das Kapitel von vorn.
5. Am Ende ist die Phase verbraucht, es geht mit der nächsten Phase weiter. Events der Phase kommen nicht dazwischen.

**Rasten und Rückweg** (Kampf-Sitzung, 26.10.): An Rastplätzen (Frame-Feld `rast`, im Kloster Hirtenhütte und Lager der
Brüder; zwei weitere folgen mit eigenen Bildern) heißt es „Rest by the fire“: volle LP, alle seit der letzten Rast
besiegten Tiere kommen zurück, und jemand vom Schiff ruft an (die drei mit dem meisten Vertrauen im Wechsel, Texte in
`rast_anrufe_eden_rise.py`, Antwort = +1 Vertrauen). „Go back to …“ führt zum vorigen Frame; ein gewonnener Kampf-Frame
bleibt bis zur nächsten Rast ruhig. **Rückweg-Sperre:** Frames mit `sperre` lassen keinen Weg zurück hinter sich zu –
damit sich Entscheidungen (Küche, Gabelung, Löwe) nicht wiederholen lassen.

**Schnellreise – Wegpunkte** (Duc + Brain Trust 29.10.2026, Vorbild Clair Obscur, `kern/wegpunkte.py`): Jedes
Ortskapitel beginnt am ersten Frame, dem **Wegpunkt am Eingang**. Ist Duc schon einmal weiter gekommen, steht unter den
Wahlen „🥾 On foot“ (wie bisher) ein Block **„🚩 Or travel“** – *„Your old trail markers are still there.“* – mit einer
Bildkarte je entdecktem Rastplatz und dem, was der Sprung auslässt (*„skips 3 fights on the way“*). Noch nicht
entdeckte Rastplätze erscheinen gar nicht (das Spiel verrät keine Orte).
- **Am Rastplatz** (vor einer Wahl) gibt es dieselben Karten als „Travel to another camp“ – vorwärts und zurück, aber
  **nie zurück hinter eine Entscheidung** (Frame mit `sperre`, z. B. das Lager): sonst ließe sie sich wiederholen.
- Reisen heilt nicht und weckt keine Tiere – dafür gibt es Rasten. Ein Sprung vom Eingang startet die Expedition genau wie
  der erste Schritt zu Fuß (Beute-Schnappschuss); danach beginnt eine neue Wegspur am Ziel (kein „Go back“ zum Eingang).
- **Niederlage** bleibt, wie sie ist: Duc wacht auf dem Schiff auf, die Phase ist weg. Beim nächsten Besuch springt er
  aber direkt zum Lager statt bei den Ratten anzufangen.
- **Berge:** die Story-Wiedereinstiege (*Back at the Tower*, *Back at the Bergerie*, nach Wolffs Sieg) bleiben Startframes
  – ab dem Anfang zu laufen würde die erste Begegnung mit Wolff wiederholen –, der Wegpunkt sitzt einfach auf ihnen.
- Ziele: Rastplätze, die vom Startframe über `weiter` erreichbar sind (bedingte Wege wie die Engine: der erste, der gilt)
  und in `rast_gefunden` stehen. Aktion `ort_reisen {id}`, Ansicht `ereignis.reisen = {von, ziele}`. Test
  `tests/test_wegpunkte.py`; Vorschau: Launch `eden-wegpunkt` (Tag 4, vier entdeckte Rastplätze).

**Spur-Uhr:** Manche Kapitel haben eine Uhr (Kloster: 4 Segmente ab der Gabelung, oben rechts als ●●○○). Wege kosten
Segmente; bei 0 setzt die Engine `spur_<name>_abgelaufen`, und das Kapitel nimmt den späten Ausgang. Nach dem Kapitel
verschwindet die Uhr.

**Wiederkommen:** Nach dem Abschluss bleibt der Ort offen und startet mit einem eigenen Frame (Kloster: `kl_wieder` –
Tiere jagen zum Leveln oder die Felsnische nachholen). Wer die Nische leert, findet sie danach leer; ist die Tasche
voll (6 Plätze), bleibt die Stahlplatte liegen und wartet.

**Für Autorinnen:** Frames sind Events mit `art "ort"` (Builder `FR(...)`), Folgen `weiter` (Frame-ID oder Liste
`[{wenn, id}, …, {id}]`, erste passende gilt, ausgewertet nach allen Folgen), `spur_uhr` (`[name, "start", n]`,
`[name, -n]`, `[name, "aus"]`), `expedition` (Start/`ende`), `chip` (`[familie, stufe]`), `kampf`. Prüfung:
`ereignisse_basis.py` (Ziele existieren, Bilder, Sprecher), `auftraege_eden_rise.py` (Start-Frames, Flags,
graue Entscheidung). Test: `tests/test_kloster.py` (beide Wege, Wiederkommen, volle Tasche).

## Ermittlung: garantierte Kernbeweise und Fall-Tafel (Duc 28.10.2026)

Zwei Pflicht-Momente der Woche liefern jedem Fall die Kernbeweise für die Anhörungspunkte *What* und *Why*:
- **Tag 4, „Rosi vs. Officer“** (Abend): eine Notiz auf Rosis Whiteboard.
- **Tag 5, „A Visit from Head Office“** (Frühstück): eine Notiz aus Megans Mappe.

Die Notiz steht im Log mit 📌 und ist sofort in der Anhörung nutzbar. Wer die Szene verpasst, bekommt sie am nächsten
Tag. Ist der Punkt schon belegt, kommt nichts. *Who* bleibt echte Ermittlung.

Im Codex (*Investigation → The case*) zeigt jede der drei Fragen *Open / Partly · x of y / Proven*. Bei offenen Fragen
steht dazu die Art dessen, was fehlt (*„Nothing on the ship's systems yet.“*), nie Namen, Orte oder Uhrzeiten. Ein
Sprung auf *Proven* steht einmal im Log und leuchtet im Codex mit Ton auf. Details und Zahlen: `anhoerung.md`,
Abschnitt *Garantierte Kernbeweise und Fall-Tafel*.

**Ermitteln sichtbar machen (Duc + Brain Trust 29.10.2026):** Gibt es in einer Szene etwas zu ermitteln, zeigt der
Knopf neben dem Eingabefeld **„🔎 Investigate · n“** mit der Anzahl der Möglichkeiten. Unter 1100 px Breite steht dort
nur das Symbol mit der Zahl. Kommt eine Möglichkeit dazu oder beginnt eine neue Szene, pulsiert der Knopf kurz.
Beim ersten Mal je Spielstand erklärt eine Sprechblase am Knopf: *„You can investigate here. Click 🔎 or press E …“*
(„Got it“ oder Öffnen schließt sie; der Browser merkt sich das je Spielstand). Oben im Ermittlungsfeld steht
**„Still missing“**: je offene Frage (What/Who/Why) dieselben Kategorie-Sätze wie auf der Fall-Tafel. Technik:
`client/index.html` (`chat()`, `ermHinweis`, `ermittlungHtml`), Engine liefert `szene.ermittlung.fehlt`
(`kern/ermittlung.tafel_kurz`).

## Einstiege und Spuren von Nähe (Duc 31.10.2026)

Anlass: Im Live-Spieltest eröffnete „You're late“ 103 von 526 Szenen (Rosi 45 von 97). Nach Nähe nannte die nächste
Szene nicht öfter etwas Vergangenes als sonst (1 von 20 gegen 19 von 435). Gemessen über Wortmuster in Bot-Läufen.

**Einstiege.** Das Spiel merkt sich je Figur die Anfänge ihrer letzten 4 Szenen (`z["einstiege"]`, am Szenenende).
Ihre erste Zeile einer Szene bekommt sie als Liste mit dem Auftrag, anders anzufangen.

**„You're late“ gehört Holm.** Alle anderen sagen es als erste Zeile nur, wenn Ausgangslage oder Regie der Szene
das Wort „late“ enthalten. Sonst wird einmal neu geschrieben, danach fällt der Satz weg. Mitten in der Szene bleibt er frei.
Das Gedächtnis bleibt unverändert, es darf festhalten, dass Duc wirklich zu spät kam.

**Eintrag nach Nähe.** Eine intime Aktion, die sie nicht ablehnt, schreibt sofort in die Chronik, je Tag und Figur nur
den stärksten Eintrag. Eine angenommene Aktion beweist keinen Sex, darum gibt es drei Stufen:

| Aktion | Kennung | Satz im Prompt | Klatsch und Eifersucht |
|---|---|---|---|
| Stufe 3, oder „she leads“ | `naehe` | shared a private, physical moment | nein |
| Stufe 4 und 5 ohne die nächste Zeile | `naehe_weit` | went further than kissing, in private | nein |
| Stellungen, `Act: Anal` | `intimate` | slept together | wie bisher, nur über Tratsch-Figuren |

Alle drei weiß nur sie, auch das Dorfohr nicht (E-060).

**Rückbezug beim nächsten Treffen.** Unter vier Augen geht ein noch nicht aufgegriffener großer Moment (`kiss`,
`confession`, die drei oben) vor, ein späteres Geschenk verdrängt ihn also nicht. Sie darf ihn einmal in eigenen Worten
ansprechen, aber nichts dazuerfinden. Vor anderen bleibt der Moment unaufgegriffen und wartet: `naehe`-Einträge sind dort
höchstens ein Blick. Der Rückbezug gilt für romanzierbare Figuren und für alle mit Nähe-Eintrag, also auch Jana und Megan.

Technik: `kern/szene.py` (`einstieg_hinweis`, `eroeffnet_zu_spaet`, `starten`), `kern/chronik.py` (`naehe_eintragen`,
`rueckbezug`), `kern/gesten.py` (`naehe_kennung`, `intim`). Test: `tests/test_einstiege_naehe.py`.

**Wer kocht (Duc 31.10.2026).** Jede Figur bekommt im Prompt: Lola kocht alle Crew-Mahlzeiten, Chiara führt die Messe und
serviert, sonst kocht an Bord niemand; Duc nur, wenn die Szene es sagt. An Land gilt das nicht. Ist Lola gefeuert, entfällt die
Regel, ist Chiara gefeuert, entfällt ihr Teil (`szene.kueche_regel`).

**Kalender aller Phasen:** `docs/abnahme/kalender_phasen/index.html`, neu erzeugen mit `python werkzeuge\kalender_seite.py`.


## Erinnerungen in Journal und Karten

Seit 31.10.2026. Zwischen zwei Szenen liegen viele Ereignisse, darum erinnert das Spiel selbst an den letzten Stand (Regel in `STIL.md`, „Verständlich bleiben“).

- **Journal:** Ein Schritt in `auftraege_eden_rise.py` kann ein Feld `rueckblick` tragen. Das Journal zeigt den Satz des letzten erledigten Schritts als „Last time“ über den Schritten.
- **Missionskarte:** Bei Ketten steht unter der Kette das Ergebnis der Mission davor (`handel.zuletzt`).
- **Ortskarte:** Ein Eintrag in `start` kann einen eigenen `text` tragen, die Karte beschreibt dann die aktuelle Lage (`auftraege.ort_text`).

Test: `tests/test_erinnerungen.py`. Die erste Runde Textänderungen steht in `werkzeuge/eden_rise/erinnerungen_einbau.py`.

**Die Auftraggeberin erinnert (Duc 02.11.2026, Spieltest-Befund 5, Vorbild Persona 5).** Liegt ein Auftrag still, schickt
die Auftraggeberin morgens eine vertonte Sprachnachricht (Handy-Event, Pflicht beim Frühstück), mit dem Grund im Satz:

| Event | Wer | Wann |
|---|---|---|
| `er_kloster` | Casanova | Kloster offen, 3 Tage nicht in der Macchia (Tag 9–20) |
| `er_berge` | Petru | Berge offen, 3 Tage nicht dort (Tag 10–20) |
| `er_grotte` | Totò | Grotte offen, 3 Tage nicht dort (Tag 12–20) |
| `er_kevin_frist` | Lea | Kevin noch nicht gefangen, Tag 13–14 (Frist Tag 14) |
| `er_flut` | Totò | Flut-Nacht offen, 3 Abende nicht dort (Tag 14–19) |
| `er_flut_frist` | Totò | Flut-Nacht offen, Tag 20 (Frist Tag 21) |

- **Regeln:** jede Nachricht einmal im Durchlauf, höchstens eine Erinnerung am Tag (`wann.erinnerung`, `kern/ereignisse.pflicht_ziehen`).
  Keine Wirkung auf Werte, nur ein Hinweis. Red Trio, Old Grey und Mazzera erinnern nicht.
- **„Nicht dort“:** Bedingung `{"ort_ruhe": [ort, tage]}` (`kern/regeln.py`). `z["ort_offen_seit"]` merkt sich den ersten Tag, an dem
  der Ort offen war (`auftraege.tagesbeginn`, am Tagesende), `z["ort_zuletzt"]` den letzten Besuch (`eden.py`, `ort_betreten`).
- **Quelle:** `werkzeuge/eden_rise/ereignisse_erinnerung.py` (Zeilen mit Turbo-Tags, schreibt sie selbst in `stimme_tags.json`).
  Vertonen: `Vertonen_EdenRise.bat`. Test: `tests/test_erinnerung.py`.
- **Schnellreise statt Neustart:** Wer zurückkommt, muss nicht von vorn laufen. Der Wegpunkt am Eingang bringt Duc zu jedem
  gefundenen Rastplatz (`kern/wegpunkte.py`, seit 29.10.2026).

## Figurenrahmen (elf Figuren)

> Entscheidung Duc 31.10.2026 (E-105), Brain Trust. Code `kern/figurenrahmen.py`, Daten `module/eden_rise/figurenrahmen.json`, Test `tests/test_figurenrahmen.py`.

**Warum:** Im Naomi-Lauf vom 31.10. griff das Modell nach großen Momenten in 11 von 11 Treffen den Moment nicht in der ersten Zeile auf, und seine eigenen Erinnerungen trugen Witze weiter. Deshalb bestimmen bei einer Figur mit Rahmen die Werte den Kontext, und das Modell spielt innerhalb dieses Rahmens frei.

| Was | Andere Figuren | Figur mit Rahmen |
|---|---|---|
| Getippter Text | Modell urteilt, ±2 Punkte je Antwort | zählt nie, kein Modellaufruf dafür |
| Freie Szene („Time with …“) | Wirkung über die Antworten | fest +4 Vertrauen, +2 Begehren, sobald Duc einen Zug gemacht hat, bis zum Gesprächs-Deckel 35 |
| Abend („An evening with …“) | Richter entscheidet über +1 Vertrauen | immer +1 Vertrauen |
| Gesten | Probe und feste Punkte | unverändert |
| „Spend time together“ | Modell schlägt vor und ordnet ein | Vorschlag und Kategorie aus den Daten |
| Erste Zeile der freien Szene | Modell | handgeschrieben, endet mit einer klaren Frage |
| Gedächtnis fürs Modell | Modell-Zusammenfassungen | Faktenblatt aus dem Code: Leiter-Flags, Chronik-Einträge aus Gesten und Events, erlebte Themen |
| Momente in der Chronik | auch vom Modell erkannt | nur aus Gesten und Events |

**Themenwahl (im Code, kein Zufall):**
1. Ein offener großer Moment der letzten 5 Tage geht vor: stärkster zuerst (erste Nacht, weitere Nacht, weiter gegangen, Geständnis, Kuss, Nähe). Damit ist er auch fürs Frühstücks-Echo erledigt.
2. Ein Abend nimmt den nächsten Abend der Liste, sodass Abende aufeinander aufbauen. Danach kommt der am längsten zurückliegende.
3. Sonst das nächste freigeschaltete Thema. Bedingungen: Vertrauen, Begehren, Leiter-Flags.

Eine Legende aus dem Dorf hat Vorrang vor einem gewöhnlichen Thema, das dann beim nächsten Mal drankommt. Vor einem Moment hat sie keinen Vorrang.

Beim ersten Treffen sagt das Spiel einmal, was zählt: “Talking freely is just for you …”. Neue Figur aufnehmen: Eintrag unter `figuren` ergänzen, dann gilt alles oben für sie. Die festen ersten Zeilen und Abschiede sind vorab vertont.

Gescriptete Szenen, Events und Gruppenszenen bleiben, wie sie sind. In Gruppenszenen urteilt das Modell nur noch über die anderen Figuren und die Crew.

Am Ende einer freien Szene oder eines Abends mit Rahmen-Figur schreibt das Modell keine Zusammenfassung mehr, die Karte zeigt Titel und feste Ergebnisse (Duc 01.11.2026).

## Start-Chips und Erzählerin (alle Figuren mit Rahmen, Duc 01./02.11.2026)

Hat ein Thema in `figurenrahmen.json` ein Feld `chips`, stehen nach ihrer ersten Zeile drei feste Antworten da, ohne Zahlen. Tippen bleibt möglich. Der Chip ist Ducs erster Zug. Jana, Megan und Ligeia haben keine Begehren-Achse: Dort zählt der ehrliche Chip +2 Vertrauen, die beiden anderen +1.

| Chip (`achse`) | Wirkung, bis zum Gesprächs-Deckel 35 |
|---|---|
| `vertrauen` | +2 Vertrauen |
| `begehren` | +2 Begehren |
| `beide` | +1 Vertrauen, +1 Begehren |

Die feste Wirkung der freien Szene sinkt dann von +4/+2 auf +2/+1. Wer tippt statt zu wählen, bekommt nur diese. Am Abend („An evening with …“) kommt der Chip zur festen Folge dazu. In solchen Szenen liest die Erzählerin die Situation vor, live über Chatterbox, danach spricht die Figur.

## Szenenende mit Abschied und Wertung (alle Figuren mit Rahmen, Duc 01./02.11.2026)

Hat eine Figur in `figurenrahmen.json` das Feld `abschied`, endet ihre freie Szene oder ihr Abend so, sobald Duc mindestens einen Zug gemacht hat:
1. Sie gibt ihre letzte Antwort, danach folgt ihr fester, vertonter Abschied. 3 × 3 Sätze nach Vertrauen und Begehren (Stufe 0–1, 2–3, 4–5), dazu 3 Sätze nach Nähe in dieser Szene. Nähe heißt: ein Moment in der Chronik oder getippte Wörter wie „kiss“.
2. Der Code bucht die feste Wirkung sofort. Das Overlay zeigt danach Thema, Gesten und die wirklichen Punkte seit Szenenbeginn, plus oder minus. Kein Modelltext.
3. Erst „Go on“ beendet die Szene. Danach folgt ein Hinweis nur noch, wenn eine Handy-Nachricht da ist.

**Sounds der Karten (Duc 02.11.2026):** Vorhang am Gesprächsende `szene_vorhang` (K5), Zwischenkarte `szene_bruecke` (K11), Tageskarte `tag_karte` (K1). Der Event-Jingle spielt bei einer Zwischenkarte erst nach „Go on“.

**Töpfe je Quelle (Duc 02.11.2026, E-116):** Vertrauen und Begehren kommen bei jeder Figur aus vier Töpfen: Szenen (Time with, Chips, Gesten, Reaktionen im Gespräch), Handy, Geschenke und Kochen, Events (alles andere, auch Missionen und Leiter). Jeder Topf hat je Figur eine eigene Größe (`MODUL["toepfe"]` in `werkzeuge/eden_rise/modul_eden_rise.py`), zusammen über 100, keiner allein erreicht 100. Ist ein Topf voll, bringt diese Quelle nichts mehr; Minuspunkte geben nichts frei. Die Töpfe sind unsichtbar: Statt Zahlen sagt die Figur ihren Satz aus `figurenrahmen.json`, Feld `topf_voll` (Geschenke und Handy sofort, Szenen auf dem Ergebnis-Screen). Sprünge auf eine Stufe (`roh`) zählen in den Topf, werden aber nie begrenzt. Gespräche tragen weiter nur bis 35 (knapp vor Stufe 3); hat ein Erlebnis Stufe 3 gebracht, wirken sie wieder bis zu ihrem Topf. Nebenfiguren ohne Eintrag haben keine Töpfe. Code: `zustand.punkte_add(..., quelle=)`, `zustand.topf_platz`, Test `tests/test_toepfe.py`.

**Go somewhere private (Duc 02.11.2026):** große Geste unter „mutig“, Charm SG 12, ab Vertrauen 3 und Begehren 3, nur wenn die beiden allein sind und nicht schon in einem privaten Raum (Stufe 4+). Bei Ja geht die Szene in Ducs Kabine weiter (neuer Hintergrund, eine Zeile im Log), +1 Begehren als Erlebnis. Bei Nein spricht sie ihre feste Absage aus `figurenrahmen.json` (`absage.privat`), das Modell spielt kein eigenes Nein. Code: `gesten.raum_wechseln`, `figurenrahmen.absage_text`, Test `tests/test_privat.py`. Seit dem Bau der Orte (unten) wählt Duc den Ort.

**Orte für Zweisamkeit (Duc 02.11.2026, E-119):** Bei „Go somewhere private“ wählt Duc den Ort (`kern/orte.py`, Daten `MODUL["orte"]` in `modul_eden_rise.py`, Texte in `figurenrahmen.json`).
- **Risiko 0–3** je Raum und Tageszeit. Nach ihrem Ja platzt mit 0 / 12 / 25 / 40 % jemand herein: **Klatsch** (ein Zeuge, die Chronik trägt es als „gesehen“ weiter, das macht eifersüchtig), **Peinlich** (Vertrauen −4, in dieser Szene nichts Intimes mehr, sie bittet ihn zu bleiben) oder **Komisch** (nur eine Zeile). Kommt niemand, gibt es +2 Begehren je Stufe.
- **Eigener Ort ab Vertrauen 4:** Chiara die Brücke (abends, nachts), Rosi der Generatorraum, Siri das Solar-Deck, Lola das Achterdeck (abends, nachts), Sophia Alvas Bar (nachts); Lea das Tenderboot, Alva ihr Hinterzimmer und Bibi die Badebucht kommen mit ihren Bildern. Dort +2 auf den Wurf, beim ersten Besuch ihre feste Zeile (`ort_erster_besuch`).
- **Ihr Vorschlag:** Nach Ducs zweitem Zug schlägt sie einmal am Tag mit 35 % ihren Ort vor (`ort_vorschlag`), dann +3.
- **Ihr Zimmer** (`MODUL["orte"]["zimmer"]`, Belegung in `welt/wohnen.md`): Crew-Kabinen mit Risiko nach der Mitbewohnerin (Sophia und Lea 3, Lola und Jana 2, Chiara und Rosi 1), die Spare Cabin (0) für die Gewinnerin von `gv_gute_kabine`, Alvas Wohnung über der Bar, Bibis Häuschen, Megans VIP-Kabine (Risiko 1, erst mit `megan_zurueck` in Akt 3). Für alle: Crew-Dusche und Crew-Toilette, abschließbar, Risiko 0. Alle neuen Räume sind `versteckt`: nicht auf der Karte, nicht in der Date-Liste.
- Gewählte Orte gelten für die Szene als privat (Stufe 4). Kloster gestrichen, die VIP-Kabine nur mit Siri nach `siri_frei`.

**7-Tage-Abstand auch für Dates (Duc 02.11.2026):** Dates, freie Zeit und Abend-Szenen (Intim- und Gesprächsabende) geben ihre Stufe nur noch mit dem Abstand (`szene.story_frei`). Ausgenommen bleiben Story-Szenen und die Leiter.

**Hintergrund im Faktenblatt (Duc 02.11.2026):** Fakten mit dem Anfang „Her background, which Duc only knows if she tells him:“ stehen im Prompt in einem eigenen Abschnitt, getrennt von dem, was beide erlebt haben. Der Handy-Chat bekommt sie nicht.

Karten liegen in der Ebene `#buehnenkarte` (`client/index.html`, Marken `SZENENKARTE`), reduzierte Bewegung wird beachtet.

**Der Screen zeigt:** „What happened“ (höchstens 3 Zeilen aus Thema und Chronik), die Gesten der Szene (Misslungenes zuerst, höchstens 3, mit Satz und Grund), die Punkte und erreichte Stufen, dazu „What worked“ und „Next time“ mit je höchstens einem Satz. Die Sätze stehen in `module/eden_rise/rueckmeldung.json`. Der Grund bleibt ehrlich, denn der Wurf entscheidet: Bei einer Chance unter 45 % nennt er das niedrige Attribut, sonst den Würfel.

**Tageskarte:** Am Tagesende erscheint statt des kleinen Hinweises eine Karte mit dem Rückblick auf den Tag.

**Nachfragen:** Sagt Duc in einer freien Szene 60 Sekunden nichts, das Eingabefeld ist leer und das Fenster offen, fragt die Figur auf ihre Art, ob er noch da ist. Das geht höchstens zweimal je Szene, zählt nicht als Zug und ändert keine Werte. Die Zeile schreibt das Modell.

**Gespräch verlassen:** In freien Einzelszenen und Abenden fragt der Knopf an der Uhr nach: bleiben, schweigen oder gehen. Wer geht, bekommt keinen Bonus für die Zeit und verliert Vertrauen (freie Szene −4 Punkte, Abend −8). Die Figur merkt es sich im Faktenblatt, und das Overlay zeigt das Minus.

## Szenenlänge und Knopf an der Uhr (Duc 01.11.2026)

**Länge:** Freie Szenen haben 8 Züge. Das Modell bekommt nur noch in der allerletzten Antwort einen Hinweis aufs Ende, und der verbietet das Wegschicken. Vorher kam „let a natural reason to wrap up appear“ ab Zug 4 bei jeder Antwort, und die Figuren schickten Duc mehrfach weg.

**Knopf an der Uhr** (Icon `skip`, `uhrSkip` in `client/index.html`):
- Bei der Auswahl überspringt er die Phase (`phase_beenden`). Das geht nur, wenn alle Karten frei sind (`frei_`, `date_`). Eine geplante Verabredung gilt dann wie sonst als versetzt.
- Im Gespräch überspringt er Ducs Antwort (`schweigen`): Duc sagt nichts, die Figur redet weiter, es zählt als Zug.
- Bei Story-Entscheidungen und Events gibt es ihn nicht.

Ein Hinweisfenster gilt ab der nächsten Aktion oder beim Öffnen des Handys als gelesen.

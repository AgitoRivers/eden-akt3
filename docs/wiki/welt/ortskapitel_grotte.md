# Akt 2, Woche 2 · „Die Insel öffnet sich“ (Tag 8–14) und die Strand-Grotte

> Stand 27.10.2026 · Besitz: Story · Quelle: `werkzeuge/eden_rise/ereignisse_akt2.py` (Pflicht-Events der Woche),
> `ereignisse_grotte.py` (Grotte, Kevins Dächer, späte Anrufe), `kaempfe_grotte.py` (Gegner, Begegnungen),
> `auftraege_eden_rise.py` (Orte `grotte`/`kevin`, Auftrag `grotte`), Test `tests/test_grotte.py`. Register E-083/E-084.

## Kalender

Der Kalender läuft jetzt bis **Tag 14** (`zeitraster.tage = 14`); danach kommt vorläufig das Ende von Akt 1 (Woche 3
mit Tauchgang und Belagerung folgt). Alle Pflicht-Events kommen zu Beginn ihrer Phase.

| Tag | Phase | Event | Was passiert | Setzt |
|---|---|---|---|---|
| 8 | Frühstück | `a2_morgen_*` | Die Crew nach dem Urteil, drei Fassungen: jemand gefeuert (`gefeuert`) · gnädig/aufgeklärt (`urteil_erbarmen/entlastet/aufgeklaert`) · sonst kühl | Moral/Rückhalt ±1–3 |
| 8 | Tag | `rosi_werkstatt_offen` | Rosis Werkstatt (gab es schon) | `werkstatt_offen` |
| 8 | Abend | `a2_unit01` | Unit-01 mit rotem Auge → **Kampf** `a2_unit01` (Level 2, Maschine, Stumpf stark) | – |
| 8 | Nacht | `a2_teil` / `a2_teil_maxwell` (wenn Rosi gefeuert) | Rosi zieht **das fremde Teil** aus Unit-01 | Item `foreign_part`, `a2_teil_gefunden` |
| 9 | Frühstück | `a2_logo` (Anruf) | Megan erkennt das Logo: **A.V. Estates = Alon** | `a2_av_bekannt` |
| 9 | frei | – | Berge öffnen (Petru, ab Tag 9 nach dem Kloster) | – |
| 10 | Nachmittag | `a2_vogelfoto` | Yamamotos „Vogelfoto“: Totò mit einem Fremden (Gennaro) | `a2_foto_gesehen` oder `a2_foto_geloescht` |
| 11 | Frühstück | `a2_toto_beichte` | Totò gesteht: Gennaro ist seit Donnerstag in der Grotte | **`grotte_offen`** (Ort „The Smugglers' Grotto“) |
| 12 | Tag | `a2_kevin_raub` | Kevin klaut **Seite 40** aus Leas Kartenbuch | **`kevin_jagd`** (Ort „Kevin's Rooftops“, bis Tag 14) |
| 13 | frei | – | – | – |
| 14 | Abend | `a2_sonntag` | Sonntag an Deck, warm, Toast auf Gennaro | Moral +1 oder Totò +4 |
| 14 | Nacht | `a2_koordinaten` / `a2_koordinaten_ohne` | Lea mit den Koordinaten (mit Seite 40) oder aus dem Gedächtnis (ohne); eine Drohne über der Bucht | `woche2_ende`, `wrack_koordinaten` oder `wrack_gedaechtnis` |

Die Woche ist Ensemble-sicher: Wer gefeuert ist, fehlt; Rosis Nacht-Szene hat eine Ersatzfassung mit Maxwell. Lea und
Sophia tragen den Kevin-/Koordinaten-Faden – ist Lea gefeuert, entfallen diese Events.

## Die Strand-Grotte · „The Smugglers' Grotto“

Ab Tag 11 (`grotte_offen`), Phasen Tag/Nachmittag, kostet die ganze Phase. Totò rudert Duc hin und wartet am Boot: „When
the water reaches the third step, I have to go.“ Die Ebbe ist die Uhr.

| # | Frame | Ort | Inhalt | Kampf (Level) |
|---|---|---|---|---|
| 1 | `gr_start` | Felsstufen unter der Punta d'Orsu | Totò, die dritte Stufe | Ratten (2) |
| 2 | `gr_strand` | Der ertrunkene Strand 🔥 | Fund: Giulias Zeichnung „PAPÀ“; Chloés Hilferuf → **Umweg 2** | – |
| 3 | `gr_gang` | Der Schmugglertunnel | Schienen, Laternenringe | Schlange (2) |
| 4 | `gr_halle` | Die Halle der Kisten | **Die Kiste aus Antibes** (Saat „I saw that crate“) | Schmuggler (3), mit List 13 umgehbar |
| 5 | `gr_teich` | Der schwarze Teich | Matteu taucht auf → **Umweg 1** | – |
| 6 | `gr_fackel` | Die Fackelgalerie | – | Fackelpirat (3) |
| 7 | `gr_zelle` / `gr_zelle_spaet` 🔥 | Gennaros Zelle | Gennaro gibt **Sussurro** (Messer seines Großvaters, „the whisper“) → `waffe_knife`. Zu spät (`gr_spaet`): seine Finger sind gebrochen | – |
| 8 | `gr_boss*` | Halle, Flut | **U Riscossore**, der Geldeintreiber aus Bastia, kommt mit der Flut | Boss (3–5, siehe unten) |
| 9 | `gr_wahl` | Halle | **Die Kiste** (graue Wahl) | – |
| 10 | `gr_heim` | Die dritte Stufe | Totò und Gennaro | `grotte_fertig` |

**Bosskampf:** Level 4, **+1** wenn Duc zu spät kommt (Bastien befreit), **−1** wenn Matteu die Wahrheit kennt (er greift
zuerst an und stirbt dabei). Begegnungen `gr_8_riscossore[_matteu][_spaet]`.

**Die Kiste:**

| Wahl | sofort | später |
|---|---|---|
| **Abgeben** (Gennaros Schuld ist bezahlt) | Gennaro frei, Totò +1 Stufe | Alons 40 Halsbänder sind wieder im Umlauf (`gr_kiste_abgegeben`, für die Belagerung vorgemerkt) |
| **Behalten** (Beweis) | Item `collar_crate`, Totò −4 | **Zwei Tage später** ruft Totò an: Gennaros Boot treibt leer vor Cap Corse (`hy_gennaro_weg`, `gennaro_verschwunden`); Versprechen „Make the crate count“ möglich |

**Dritter Weg, selbst bezahlen (Duc 01.11.2026, nicht gebaut):** Gennaros Schuld sind 1.000 €. Duc kann sie bar zahlen, wenn er das Geld hat, sonst bleibt die Wahl sichtbar und gesperrt. Dann ist Gennaro frei, die Kiste bleibt bei Duc und ist Beweis für die Kommission an Tag 35. Alon weiß danach, dass Duc sie hat. Gennaro zahlt in kleinen Raten über Totò zurück, zusammen höchstens rund 300 €.

**Piraten in der Grotte (Duc 01.11.2026, nicht gebaut):** „The Night Shift“ wird zu Gunner, Fackelpirat und einfachem Pirat, dort taucht der Pirate Gunner zum ersten Mal auf. `kampf/PirateAlpha` wird nach Riscossores neuem Satz nicht mehr gebraucht und bleibt liegen.

**U Riscossore (Duc 01.11.2026):** Endgegner der Grotte. Ein alter Schwarzer Mann im weißen Leinenanzug, an den Manschetten vergilbt, Sprites noch offen. Er hat auch Buenaventura sein Schiff finanziert, siehe [Die Schuldenkette](ortskapitel_tauchgang.md#die-schuldenkette-duc-01112026).

**Im Journal (29.10.2026):** Die Grotte ist ein Hauptauftrag; ihre beiden Umwege stehen als optionale Schritte darin, die
Flut-Nacht als eigener Nebenauftrag „High Tide“ (Details: `systeme/interaktion.md`, Abschnitt Aufträge und Orte).

## Umweg 1 · „The Second Brother“ (Matteu)

Matteu Pinelli, 19, taucht für die Schmuggler, weil sie ihm versprochen haben zu verraten, wo sein Bruder Ghjacumu
letztes Jahr ertrunken ist. Szenen: verbotene Galerie (Schlange, 3) → Luftblase 🔥 (Strichliste: 37 Gezeiten, 18 Tage
überlebt) → das Gitter (Ratten, 3; abgeschlossen **von außen**) → Wahl.

| Wahl | Folge |
|---|---|
| **Wahrheit** („Someone locked him in.“) | Medaille `ghjacumu_medal`; Matteu greift im Bosskampf zuerst an und **stirbt** (`gr_matteu_tot`), der Boss ist −1 |
| **Lüge** („It was quick.“) | Matteu Vertrauen +8, lebt. **Zwei Tage später** ruft Alva an: Matteu gibt Runden aus, die Männer aus Bastia sind „like family“, der Alte brachte seiner Mutter Blumen (`hy_matteu`) |

## Umweg 2 · „The Price of the Tide“ (Chloé und Bastien)

Chloé Marchal und Bastien, Schatzsucher aus Marseille, suchen die Geldkassette des Schoners von 1924 – bezahlt von
A.V. Estates. Szenen: Hilferuf → eingestürzter Gang (zwei Plünderer, 3) → ihr Lager 🔥 (Fund: Ring im Samtkästchen,
Laptop mit A.V.-Logo) → „Twenty Minutes“.

| Wahl | Folge |
|---|---|
| **Bastien befreien** | Beide leben, Chloé gibt ihre Notizen (`treasure_notes`, Vorteil für den Tauchgang in Woche 3). Die Ebbe ist vorbei: **Gennaro verliert die Finger** (`gr_spaet`, `gr_gennaro_haende`), Boss +1 |
| **„I'll come back“** – Gennaro zuerst | Gennaro ganz. Auf dem Rückweg ist der Gang voll Wasser: **Bastien ist ertrunken** (`gr_bastien_tot`), Chloé gibt Duc den Ring (`bastien_ring`): „Give it to someone who gets the chance.“ |

## Die Flut-Nacht · „The Grotto at High Tide“ (Duc 28.10.2026, E-085)

Ort `grotte_flut`, nur **abends**, sobald die Gennaro-Mission fertig ist (`grotte_fertig`), bis Ende Akt 2. Kostet den
ganzen Abend. Totò fährt nachts nicht mit, Duc rudert allein. Hinweise darauf: Beim ersten Besuch summt es am schwarzen
Teich; auf Seite 40 (Leas Kartenbuch) steht am Rand „She sings at the pool when the tide is in“.

| # | Frame | Ort | Kampf (Level) |
|---|---|---|---|
| 1 | `fn_start` | Felsstufen, das Wasser über der dritten Stufe | Ratten-Alpha (4) |
| 2 | `fn_gang` | Schmugglertunnel, die Decke bewegt sich | **Fledermaus-Schwarm** (4) – mit **10 %** stattdessen **die Vampirin**, je Abend ohne sie +10 Prozentpunkte |
| 3 | `fn_galerie` | Verbotene Galerie, man muss schwimmen | **Schwarze Viper** (4) |
| 4 | `fn_halle` | Halle der Kisten, die Schmuggler entladen bei Flut neue Kisten mit dem weißen Logo | Piraten (4); mit Wahrnehmung 13 vorher in eine Kiste sehen (`fn_kisten_gesehen`) |
| 5 | `fn_teich` | Der Teich im Mondlicht | **Die Sirene** – Rede-Kampf |
| 6 | `fn_perle` | Teich | Sie erzählt vom Wrack und gibt den **Saphir** |
| 7 | `fn_heim` | Felsstufen im Mondlicht | – |

**Hinweise der Sirene** (Duc 29.10.2026): Wer sie mit Waffe, Spezialangriff oder Granate trifft, bekommt je Zug
höchstens einen Satz von ihr, vertont (`kampf.sirene.0`–`3`) und unten rechts im Kampf als Kasten:
1. neckt – *„Ooh. That tickled, sailor. Do it again, I dare you.“*
2. kleiner Hinweis – *„Men have been stabbing the sea for three thousand years. Not one of them thought to talk to it.“*
3. kleiner Hinweis – *„… I'm starving for a good word.“*
4. direkt – *„Gods, you're slow. Put the steel away and talk to me.“* Danach ist ihre Schwäche sichtbar, **Talk leuchtet**.

Die Sirene ist **Ligeia** aus der Odyssee (Hidden Character, Duc 29.10.2026, Figurenseite
[`ligeia.md`](../figuren/ligeia.md)). Seit dem 29.10. spricht sie mit **neapolitanischem Akzent** statt walisisch, sagt
„sailor“ statt „cariad“ und „Gods“ statt „Duw“; „isn't it“ und „Talk, is it?“ sind gestrichen. Alle Texte sind
umgestellt und mit der neuen Stimme vertont (Stimme IT · 3, `docs/abnahme/stimmen_ligeia/`).
Ab dem fünften Schlag nur noch die feste Zeile. Daten `untouchable_hinweise` in `kaempfe_grotte.py`, Regel
`kern/kampf._unberuehrt`, Test `tests/test_sirene.py`.

**Die Sirene:** Waffen, Feuer, Blutung und Granaten gehen durch sie hindurch (`untouchable`, ihre LP sinken nie).
Gewinnen nur über **Reden**: Fassung auf 0. Charisma ist ihre Schwäche (Vorteil und −4 extra), ihre Fassung ist doppelt
so hoch wie normal (`fassung_faktor` 2), Level Duc +1. Sie greift weiter an: ihr Gesang macht ungedeckt, „The Wave“
(8 Schaden, nass) kann man nur ausweichen. Messung: 3–7 Runden je nach Parade; mit schlechtem Ausweichen kann man
verlieren. **Verlieren kostet nichts** – Duc wacht am Strand auf, sie ist für diese Nacht weg. Belohnung: Item `saphir`
(Riposte Stufe 2, wartet auf den Säbel aus dem Tauchgang), Flags `sirene_fertig` und **`sirene_weg`** (Vorteil beim
Tauchgang in Woche 3, dort festlegen). Stimme: ätherisch, neapolitanischer Akzent, nennt jeden Mann „sailor“.
Nach der Flut-Nacht kann man sie **jede Nacht am Teich** besuchen (Raum `siren_pool`, Karte „Time with the Siren“):
Vertrauen 0–5, Geschenke, drei Stufen-Events und eine Spur durch das ganze Spiel – siehe ihre Figurenseite.

**Die Vampirin („The Pale Lady“):** Monster, Element Feuer, Level **Duc +2** (Totenkopf), Boss. Ihr Kuss saugt Leben
(`drain`). Schwach gegen Stange (Le Large ×1,25) und Wasser (Granate); das Messer Sussurro ist gegen sie am schlechtesten
(×0,8). Beute: **immer genau eine** Sache – ein Modul (Präzision/Konter/Ausdauer II), 120 € oder ein Stufe-1-Material
(Jade, Topas, Aquamarin, Amethyst, Steel Plate). Niederlage kostet nichts.

**Steigende Chance** (Duc 28.10.2026, wie in Hades): Die Vampirin kommt mit 10 %, jeder Abend ohne sie hebt die
Chance um 10 Prozentpunkte (20 %, 30 %, 40 % …), nach einer Begegnung fällt sie zurück auf 10 %. Spätestens beim
zehnten Abend ist sie sicher da, im Mittel nach etwa vier. Zähler `z["selten_zaehler"]["fn_2_fledermaeuse"]`.

**Nach der Sirene** bleibt die Flut-Nacht ein Sammel-Lauf: dieselben vier Kämpfe (mit der 10-%-Chance auf die
Vampirin), am Teich nur noch Stille (`fn_teich_leer`, Rastplatz).

## Messung (Bot, 28.10.2026)

`python tests\expedition_sim.py` spielt alle Ortskapitel mit echten Kämpfen und drei Spielertypen (einfach / klug /
geübt; klug = Punkte verteilen, Fähigkeiten, Medkits, Granaten). Stand: Grotte 11 min ohne, 18 min mit Umwegen;
Flut-Nacht 8 min, Sammel-Lauf 5–6 min; Kämpfe dauern im Schnitt nur 3 Züge. Der geübte kluge Spieler verliert in
der Grotte fast nie, der kluge mit normaler Parade zwei- bis dreimal. Duc (28.10.): alles unter 20 Minuten ist zu
wenig – die Grotte wird Pilot für „Expeditionen 2.0“.

## Kevins Dächer (Tag 12–14)

Ort „Kevin's Rooftops“ nach `kevin_jagd`, frei wählbar bis Tag 14 (Soras Vorschlag). Dächer (Kevins Tauben, 2) →
Glockenturm (**Mini-Boss Kevin**, 3, flieht nie) → das Nest (Totòs Feuerzeug, Megans Füller, Holms Ersatzbrille …) →
Seite 40 zurück (`lea_chart_page`, Lea +1 Stufe). Niederlagen kosten hier nichts. Wer nicht geht, bekommt am Sonntag
die Fassung „From Memory“.

## Gegner (neu, `kaempfe_grotte.py`)

| Gegner | Sprite | Element | Chip-Drop |
|---|---|---|---|
| Unit-01 (Red Eye) | Unit1 | – (Maschine) | Präzision II |
| Schmuggler | Thief | Wasser | Konter II |
| U Riscossore | PirateAlpha | Wasser | **Präzision III** |
| Kevins Tauben | PigeonAlpha | Luft | – |
| Kevin | Kevin | Luft | Ausdauer II |

Dazu vorhandene: Ratten-Alpha, Schlange, Pirat, Fackelpirat. Die Schmuggler sind Wasser – Sussurro (Luft) bekommt Duc
in der Zelle, also genau vor dem Boss.

## Stimmen und Bilder

- Neue Stimmen per ElevenLabs Voice Design **in der Muttersprache** (`stimmen_design.py --ziel stimmen_grotte`):
  Gennaro, Matteu und U Riscossore Italienisch, Chloé Französisch. Proben und Messung: `docs/abnahme/stimmen_grotte/`
  (gewählt: gennaro_2, matteu_2, chloe_3, riscossore_2). Vertonung: `Vertonen_EdenRise.bat`, Turbo-Tags über
  `stimme_tags_berge.py` (Präfixe `a2_`, `gr_`, `kv_`, `fn_`).
- Die Sirene: am 28.10.2026 mit walisischem Akzent vertont (`--ziel stimmen_sirene`, Probe 3). Seit 29.10. ersetzt
  durch Ligeias Stimme (`stimmen_design.py`, `--ziel stimmen_ligeia`; Duc wählte `ligeia_it` Probe 3, neapolitanisch,
  Referenz `Ligeia - ENG.wav`); alle Sirenen-Zeilen werden damit neu vertont. Im Spiel liegt Hall
  leicht darüber (`effekte.py`, siehe `systeme/audio_stimmen.md`).
- Bilder: Die 13 Hintergründe sind seit 28.10.2026 abgenommen und eingebaut; der Kampf in der Fackelgalerie nutzt das
  Zweitbild `torch_gallery_2`. Gennaro und Matteu haben ihre Sprites; U Riscossore (neu als Schwarzer Mann) und
  Chloé warten noch auf Ducs Wahl. `WUNSCH` in `ereignisse_grotte.py` und `kaempfe_grotte.py` bleibt als Rückfall,
  falls ein Bild fehlt.

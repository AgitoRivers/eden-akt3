# Ortskapitel Berge · „The Mountain and the Daughter“

> Stand 27.10.2026 · Besitz: Story · Quelle: `werkzeuge/eden_rise/ereignisse_berge.py` (Frames), `kaempfe_berge.py`
> (Gegner, Begegnungen), `auftraege_eden_rise.py` (Orte, Aufträge), Test `tests/test_berge.py`.
> Vorbild: der Blutige Baron (Witcher 3) – der Hauptquest zieht, die Umwege bleiben im Kopf. Keine Spur-Uhr: Wolff lässt
> Duc Zeit, Adrien zu finden (Duc 27.10.).

## Freischaltung

- **Ab Tag 9**, nachdem das Kloster abgeschlossen ist (`kloster_fertig`). Dann leuchtet **Petru's Boathouse** als Ort in
  der freien Phase. Petru bittet Duc, Laetitia zu holen → `berge_angenommen`, der Ort **The Mountains** öffnet.
- Seit 27.10.2026 läuft der Kalender bis Tag 14 (Woche 2, `ortskapitel_grotte.md`) – die Berge sind spielbar.
- **Wiedereinstieg:** Wer am Turm war, startet beim nächsten Ausflug am Turm (Schnellreise); wer die Bergerie erreicht
  hat, startet vor dem Bosskampf. Nach dem Ende: freies Jagen, Kaffee bei Adrien (nur Weg C).

## Die 12 Stationen

| # | Frame | Ort | Inhalt | Kampf (Level) |
|---|---|---|---|---|
| 1 | `bg_start` | Kastanienpfad | Stiefelspuren (Wahrnehmung 12: einer hinkt) | Bache mit Frischlingen (3) |
| 2 | `bg_koehler` | Köhlerplatz 🔥 | Rast, Fund: Legionsdecken | – |
| 3 | `bg_turm…` | Genueser Turm | **Wolffs drei Fragen** (Wahrheit oder Lüge), Capra macht ihn weich | – |
| 4 | `bg_steilhang` | Steilhang | Wolf mit Halsband, keine Flucht | Wolf (3) |
| 5 | `bg_see…` | Bergsee 🔥 | Laetitias rotes Halstuch, Dumenica am Ufer → Umweg 2 | Affe (4) |
| 6 | `bg_hochweide` | Hochweide | Ghjuvan zählt seine Schafe → Umweg 1 | – |
| 7 | `bg_kamm` | Nebelkamm | erster A.V.-Agent | Agent (4) |
| 8 | `bg_kamm_oben` | Nebelkamm oben | Funkgerät „A.V. Estates“ | zwei Agenten (4) |
| 9 | `bg_bruecke` | Hängebrücke | keine Flucht mitten auf der Brücke | Grauer Wolf (4) |
| 10 | `bg_bergerie…` | Bergerie 🔥 | Laetitia, Adrien, die Fotos; Halstuch zurückgeben | – |
| 11 | `bg_abend_*` | Bergerie, Abend | **Bosskampf** (siehe unten) | Brute + Agenten (4–6) |
| 12 | `bg_drei_wege` | Bergerie, Nacht | **Three Ways Down**: Streit statt Plädoyer | ggf. Wolff (5/6) |

**Wolffs drei Fragen:** Je Frage Wahrheit oder Lüge (Flags `bg_wolff_wahr_n` / `bg_wolff_luege_n`). Wer **zweimal oder
öfter lügt**, trifft in Weg C auf `wolff_hart` (Level 6, keine Schwäche, gibt nicht auf, immun gegen Charme). Sonst
`wolff` (Level 5, Schwäche Empathie, gibt bei 35 % LP auf).

**Bosskampf vor der Bergerie** – sechs Varianten aus beiden Umwegen:

| Umweg 2 (Panther) | Gegner | Level | mit Old Grey (Chip geschnitten) |
|---|---|---|---|
| erlöst | Brute + zwei Agenten | 6 | 5 – die Bärin wirft den Brute um |
| gehetzt | Brute allein | 5 | 4 |
| nicht gespielt | Brute + Agent | 5 | 4 |

**Meramie in Weg C und A** (Duc 29.10.2026): Petru gibt Duc in jedem Weg seine alte Jacke aus der Zeit, als er jung
und stark war – jedes Mal mit einer anderen Geschichte, immer über das Flag `jacke_jacket_water`.
- **C** (`bg_c_jacke`, *The Sea Chest*, abends nach `berge_fertig`): Radio aus, Petru zieht die Seekiste unter der
  Werkbank hervor, die geschiente Hand auf dem Deckel, Totò hört an der Tür heimlich mit. *„When I was twenty, I could
  lift the mooring stone at the end of the quay. Alone.“* – die Jacke trug er im Winter auf den Thunfischbooten vor
  Bastia. *„This hand can't hold a net now. Hm. The coat still holds. Take it.“* Wer die Kiste für ihn zurückhebt,
  bekommt +2 Vertrauen.
- **A** (`bg_a_jacke`, *Paid in Full*, tagsüber nach `berge_fertig`): Die Jacke liegt schon gefaltet auf der Werkbank,
  Petru legt das Netz nicht weg. *„Twenty years at sea in it. It bought me my first boat.“* – *„You brought my daughter
  home. Take it. We are even.“* Kein Vertrauen dazu; das Radio bleibt aus.
- Test `tests/test_petru_jacke.py`.

**Nach Weg B: Bruch, Kälte, Versöhnung** (Duc + Brain Trust 29.10.2026)

- **Dunkler Laden:** Petrus Werkstatt bleibt offen, aber das Radio ist aus, er bedient ohne aufzusehen. Kalte Begrüßung
  (*„Hm. What do you need.“*, *„Say what you want. Then go.“*, *„The tools are where they always are.“*), beim Kauf
  *„Hm. Take it.“*, beim Fisch *„Put it on the scale. Don't talk.“* / *„I'll give you less. You know why.“*. Fisch bringt
  **20 % weniger**, Petrus Fisch-Geschichten kommen erst nach der Versöhnung. Werkzeuge und Abbau laufen normal
  (Soras Veto gegen eine Sperre: Kälte fühlen, nicht ausgesperrt sein). Technik: `kern/abbau.petru_kalt`, Zeilen
  `kalt_*` in `kochen_daten.py`.
- **Laetitias Karte** (`bg_b_postkarte`, frühestens 3 Tage nach dem Rauswurf, Tag 8–21): Totò drückt Duc am Kai eine
  Postkarte in die Hand – eine flache Stadt, auf der Rückseite ein blaues Boot auf Böcken: *„Papa – the sea is different
  here. Not better. – L.“* Duc bringt sie gleich zu Petru oder behält sie erst (dann zwei Tage später).
- **Versöhnung** (`bg_b_versoehnung`, *The Radio*): Petru liest zweimal; *„Twelve years she wanted to leave. Twelve years
  I said nothing.“* – *„She drew the boat. She still knows where the keel goes.“* – und gibt Duc **Meramie**, seine alte
  Jacke: *„I wore it the night Marie said yes. I was strong then, and stupid. Like you.“* Danach legt er das Netz weg und
  stellt das Radio wieder an. Ab jetzt ist der Laden normal (`petru_versoehnt`). Die −40 Vertrauen bleiben, Fish Pie
  gibt es nur in Weg C. Test: `tests/test_petru_weg_b.py`.

**Three Ways Down:**

| Weg | Was passiert | Folgen |
|---|---|---|
| **A – übergeben** | Adrien lässt sich abführen | 300 €, **Wolffs Képi** (Vorteil auf Mut). Laetitia spricht nie wieder mit Duc (`bg_laetitia_schweigt`), die Fotos verschwinden |
| **B – übers Meer** | nur mit **Totò ab Vertrauen 3**, sonst lehnt Totò vertont ab und Duc wählt neu | Petrus Vertrauen fällt (−40 Punkte), Petru wirft Duc aus der Werkstatt (`petru_werkstatt_zu_duc`, datiert), der Legionär bleibt verwehrt, Totò +4. Danach **dunkler Laden** bis zur Versöhnung über **Laetitias Karte** (siehe unten) |
| **C – die Fotos zeigen** | Kampf gegen Wolff | Sieg: Wolff meldet Adrien „im Einsatz gefallen“, Adrien bleibt in der Bergerie (`bg_adrien_bergerie`), Laetitia bleibt bei ihm, Petru +1 Stufe („Sunday. I'll make the fish pie.“). Niederlage: wie Weg A beim nächsten Besuch |

## Umweg 1 – „Old Grey“ (Ghjuvan, die Bärin)

Ghjuvan ist der letzte Hirte am Berg: Bankbrief, vierzig Schafe, A.V. Estates will sein Land. Jede Nacht holt ein Bär
ein Schaf. Szenen: Hochweide → Ziegenpfad (tote Ziegen, Wildhunde) → Sommerhütte 🔥 (Ghjuvan am Feuer) → Dickicht
(**Bärenjunges**: der Kampf beginnt, nach der ersten Aktion rennt es weg, `flee_at 1.0`, Level 5 gegen Ein-Schlag-KO)
→ Höhle (**Old Grey**, GrizzlyAlpha, Level 5, Boss) → Wahl.

| Wahl | sofort | später |
|---|---|---|
| **Die Mutter töten** | Ghjuvan rettet Herde und Land: **Topas** (Le Large Stufe 2), 120 €, **Messer seines Vaters**, Vertrauen +1 Stufe | Beim nächsten Besuch liegen die Jungen vor der Höhle – eines bewegt sich nicht mehr |
| **Den Chip schneiden** | Steuerchip, Ghjuvan Vertrauen −4, Old Grey hilft im Bosskampf (−1 Level) | **Zwei Tage später** ruft Petru an: Die Bärenfamilie kam nachts auf die Weide, Ghjuvan ist tot, A.V. Estates kauft das Land. Die Weide zeigt danach das neue Schild |

## Umweg 2 – „The Mazzera's Dream“ (Dumenica, der Panther)

Dumenica ist eine alte **Mazzera** (korsischer Volksglaube: sie jagt im Traum, das getötete Tier trägt das Gesicht eines
Menschen, der bald stirbt). Sie hat eine schwarze Bestie mit Laetitias Gesicht geträumt. Szenen: Hütte am See →
Lichter auf dem Kamm (zwei Agenten mit Infrarotlampen, **Steuergerät**: sie lenken den Panther als Spürhund nach Adrien)
→ verlassene Hütte 🔥 (Dumenicas Sohn, den sie vor zwanzig Jahren träumte) → Wildhunde jagen die Bestie → Lager
(**der Panther**, PantherAlpha, Level 5, Boss) → Wahl.

**Mazzera's Hunting Charm (Duc 28.10.2026):** Nach dem Kampf hängt hinten in der Felsnische an einem roten Faden eine
Mondsichel aus Keilerhauer mit Rabenfedern und Mondstein. Duc nimmt sie bei beiden Wahlen mit (Folge `{"charm": "mazzera"}`
in `bg_u2_wahl`): der Charm, Ausdauer +1 – das Unikat der Berge ([`beute.md`](../systeme/beute.md)).

| Wahl | sofort | später |
|---|---|---|
| **Erlösen** | Dumenica glaubt, der Traum ist gebrochen: **Amulett** (Vorteil auf Wahrnehmung), Vertrauen +1 Stufe | Der Chip meldet den Tod: im Bosskampf **ein Agent mehr**. **Zwei Tage später** brennt Dumenicas Hütte (Anruf von Petru; Duc kann ihr helfen, 100 €) |
| **Auf die Agenten hetzen** | Schreie auf dem Kamm, der Panther stirbt schreiend – wie im Traum. Im Bosskampf **ein Agent weniger** | Dumenica erzählt es Petru, **Petru steigt nachts auf** und steht bei Three Ways Down in der Bergerie. In Weg C fängt er den Schlag für Laetitia ab: **seine rechte Hand bleibt steif** (`petru_hand_steif`) |

## Gegner (neu, `kaempfe_berge.py`)

Freie Waffenwahl. **Le Large lohnt sich** gegen alle Tiere (Feuer gegen Erde, die Stange hält Abstand: Gegner −2), die
**Agenten** sind Technik (Luft) und fallen mit **Terremoto** (Erde). Tiere fliehen, Agenten dürfen fallen (E-073).

**Granaten der Agenten (Duc 28.10.2026):** Jeder Agent wirft im Kampf die Granate, die er danach fallen lässt
(Signatur-Drop, [`beute.md`](../systeme/beute.md)). Kamm 7: **Shock Grenade** (Strom). Kamm 8: **Flash Grenade**
(geblendet). Umweg U2: **Water Grenade**, die bei vollem Treffer eine Runde länger nass macht. Drei Runden später kommt
der Taser des Partners: Nass plus Strom gibt einen **Kurzschluss auf Duc** (8 % LP, eine Runde aussetzen). Wer die
Granate pariert, ist rechtzeitig wieder trocken. Die Bergerie (Big Man mit Agenten) hat keine Signatur. Feuer-,
Erschütterungs- und Splittergranate bleiben für die Agenten in Akt 3.

| Gegner | Sprite | Element | Chip-Drop |
|---|---|---|---|
| Bache | Wildschwein | Erde | Erholung I |
| Wolf mit Halsband | Wolf | Erde | Ausdauer II |
| Grauer Wolf | WolfAlpha | Erde | Konter II |
| A.V. Agent | Agent | Luft | Präzision II |
| Zwei Agenten (Kamm 8; U2 mit Wassergranate: `agent_duo_nass`) | AgentAlpha | Luft | **Scout III** |
| Brute (allein/+1/+2) | BruteAlpha | Erde | Schutz III |
| Bärenjunges | BearCub | Erde | – |
| Old Grey | GrizzlyAlpha | Erde | Wucht III |
| Die schwarze Bestie | PantherAlpha | Erde | Blutend II |
| Sergent Wolff (normal/hart) | Wolff (langes Schwert) | – | – |

## Stimmen und Bilder

- Neue Stimmen per **ElevenLabs Voice Design in der Muttersprache** (Duc: erst das bringt den Akzent), dann als
  Chatterbox-Referenz: Laetitia und Adrien Französisch, Wolff Deutsch, Ghjuvan und Dumenica Italienisch (korsischer
  Akzent). Proben, Messung und Transkript: `docs/abnahme/stimmen_berge/`, Werkzeug `werkzeuge/eden_rise/stimmen_design.py`.
- Vertonung: `Vertonen_EdenRise.bat` (vertont alles, was fehlt; nur diese Zeilen: `--praefix bg_`), Turbo-Tags: `stimme_tags_berge.py`.
- Bilder (27.10., Commit d759bd1/350a12f): zwölf neue Hintergründe (`eden_rise_charcoal_clearing` … `rope_bridge_gorge`),
  Figuren „Kaspar Wolff“, „Ghjuvan Santucci“, „Dumenica“ (Sets `<pid>_standard`), Kampfbilder Wolff (14 Posen) und
  BearCub (idle/hurt/flee – mehr braucht es nicht, das Junge flieht vor seinem ersten Angriff). `WUNSCH` in
  `ereignisse_berge.py` bleibt als Rückfall, falls ein Hintergrund fehlt.

## Engine-Bausteine (neu)

- Folge `{"flag_datiert": "x"}` setzt ein Flag und merkt den Tag (`z["flag_tag"]`), Bedingung `{"flag_seit": ["x", 2]}`
  gilt ab zwei Tagen danach (`kern/regeln.py`). Damit kommen Ghjuvans Tod und Dumenicas Hütte „ein paar Tage später“.

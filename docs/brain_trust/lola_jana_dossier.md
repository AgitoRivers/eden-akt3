# Dossier Paar 6: Lola (Lola Brennan) + Jana (Jana Maihoff) (Stand 22.10.2026, Recherche read-only)

Ziel: Fakten für die Figuren-Runde (Raster: Wunsch + Angst, Bindung an die Prämisse, Rolle je Akt, Grauton, Lebensziel +
Bogen, Erkennungssatz) und für eine engere Verwebung der Freundschaft Lola ↔ Jana. Nur Quellen, keine Vorschläge.

Quellen-Kürzel:
- `lola.txt` / `jana.txt` = X:\AI\Eden\karten_neu\*.txt (Kartentext EN/DE). Zeilennummern = EN-Fassung, sofern nicht anders
  angegeben (lola.txt EN 1–90, DE 92–178; jana.txt EN 1–95, DE 97–188). Andere Karten: `maximum.txt`, `yamamoto.txt`,
  `holm.txt`, `megan.txt` im selben Ordner.
- `Karten-JSON` = X:\AI\RoleplayGen\cards\Eden Yacht\Lola Brennan.json / Jana Maihoff.json (extensions.duc.id, stimme,
  eingebettetes character_book mit 24 Einträgen = **älterer** Weltbuch-Stand ohne Lola-/Jana-Paareinträge).
- `LB n` = ST-Weltbuch X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds\Eden Yacht.json
  (Eintrag-Nr., 72 Einträge, 0–71).
- `lb_lmh` = karten_neu/lorebook_lola_megan_holm.py · `lb_mjy` = karten_neu/lorebook_maximum_yamamoto_jana.py ·
  `cc_lmh` = karten_neu/cc_figuren_lola_megan_holm.py · `cc_mjy` = karten_neu/cc_figuren_maximum_yamamoto_jana.py ·
  `karten_mjy` = karten_neu/karten_maximum_yamamoto_jana.py · `studio_mjy` = karten_neu/studio_maximum_yamamoto_jana.py.
- `basis` = werkzeuge/eden_rise/basis_eden_rise.py · `modul_py` = modul_eden_rise.py · `geg_py` =
  gegenstaende_eden_rise.py · `laeden_py` = laeden_eden_rise.py · `abende_py` = ereignisse_abende.py · `ebasis_py` =
  ereignisse_basis.py · `story_py` = story_eden_rise.py · `buehne_py` = story_buehne.py · `faelle_py` = story_faelle.py.
- `ER <id>` = module/eden_rise/ereignisse.json (Event-ID) · `MI <id>` = missionen.json · `modul.json`, `gegenstaende.json`,
  `laeden.json`, `story.json`, `buehne.json` = module/eden_rise/.
- `kern/…` = X:\AI\Eden\kern\*.py.
- `PS` = X:\AI\PromptStudio\presets.json / decks.json / set_presets.json · `cfg` = X:\AI\Eden\eden-config.json (nur
  Stimmen-Zuordnung) · `CB` = X:\AI\Chatterbox\stimmen.json.
- `SL` = X:\AI\Spielleiter\boegen\Lola Brennan.json (ST-Spieltisch-Bogen). Für Jana gibt es **keine** Bogen-Datei.
- `CC` = X:\AI\CharCreator\figuren\84817d7ec0cd.json (Lola) / 16f8e9cf3e9b.json (Jana).
- `Übergabe` = docs/wiki/START.md · `TAGE` = docs/wiki/systeme/tage_erkundung.md · `KAMPF` = docs/wiki/systeme/kampf.md ·
  `HCD`/`MAD`/`SYD` = Dossiers holm_chiara_ / megan_alon_ / siri_yasin_dossier.md.
- `Memory` = Ducs Memory-Notizen (project_eden_neue_npcs.md, project_eden_vertrauen.md) – nur als Stand-Hinweis.
- `X:\AI\mission-control\entwuerfe\` existiert auf diesem Rechner nicht (Pfad aus der Memory nicht gefunden).

Abschnitte 1–7 enthalten keine Fall-Auflösungen. Lolas Aussagen, Tratsch-Tipps und Unterschriften in den Fällen stehen nur
ganz unten unter „VERDECKT“. Jana kommt in den Fällen nicht vor (sie existiert in der Engine nicht).

---

## 1. Lola – Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | **Lola Brennan**, Kurzname „Lola“ | lola.txt:5, modul.json personen.lola |
| Alter | **24** (überall gleich) | lola.txt:5, LB 34, LB 49, modul_py:131 |
| Herkunft | **Byron Bay, Australien.** Aufgewachsen hinter dem **Café ihrer Mutter**, **Jüngste von vier**, „die Laute“. Kam vor **zwei Jahren für einen Sommer** nach Europa und flog nie heim: Weinlese in Bordeaux, Strandbar auf Ibiza, Foodtruck in Lissabon. Ruft **jeden Sonntag ihre Oma (nan) in Byron** an. Vater nirgends erwähnt | lola.txt:6, 75 |
| Wunde | Ein **Küchenchef in Sydney** sagte ihr, sie werde **nie mehr als eine Beiköchin (line cook)**; sie verließ seine Küche noch am selben Abend. „So she stopped cooking for stars and started cooking for people.“ Sie hat es laut Karte vier Jahre niemandem erzählt (mes_example) | lola.txt:6, 61, 75; cc_lmh:36 |
| Rolle an Bord | **Köchin** der M/Y Eden Rise, **erste Saison**: drei Crew-Mahlzeiten am Tag, Gäste-Dinner in Charterwochen, Kühlräume, Einkauf in jedem Hafen. Kombüse neben der Crewmesse, „everybody passes through“. Angeheuert im Frühjahr in Antibes, weil der letzte Koch kündigte und sie „schneller ja sagte“ (Engine: „literally standing right there“) | lola.txt:5–7, 22; modul_py:130–131 |
| Persönlichkeit | verpeilt, sonnig, laut; verliert Schlüssel, Feuerzeug, Zeit (Engine: Handy dreimal am Tag), **nie ein Rezept**; kocht nach Geruch und Laune; nach Dienst „ein bisschen betrunken oder ein bisschen high“. **Tratschfunk**: hört alles, erzählt die Hälfte weiter, „usually a bit wrong“. **Widerspruch:** „the most relaxed person on the boat, and the one most afraid of being useless when it counts.“ Nie: lässt jemanden hungrig gehen; kocht nie zweimal dasselbe Gericht | lola.txt:7, 11, 14; modul_py:132–138 |
| Knopf / Reibung / Marotte | Knopf: **gebraucht werden** (um Hilfe gebeten werden, ungefragter Nachschlag). Reibung: kann kein Geheimnis behalten und will, dass Duc ihr eins anvertraut. Marotte: **benennt ihre Pfannen**, findet ihr Feuerzeug im Zuckerglas, Gefrierfach, BH | lola.txt:17–19 |
| Stimme / Sprache | laut, warm, träge; **Aussie-Slang** (mate, heaps, sweet as, reckon, arvo, no worries); lacht über eigene Witze; redet mit Händen und Holzlöffel; Tratsch beginnt mit „Don't tell anyone I told you“; versaut und kichernd, wenn erregt. **Anrede Duc: Karte „Boss“ / „mate“** – **Engine „Captain“** („because it suits your face“) und „babe“. **Stimme:** Engine „Lola Brennan“ (cfg stimmen.eden_rise.lola), Karte „Lola Brennan“ (Karten-JSON extensions.stimme en/de), CB: ElevenLabs-Ableitung aus Eden\Stimmen\Lola.mp3, en-au, f0 261 Hz, „warm, hauchig, bubbly, wild“ → **einheitlich** | lola.txt:16, 86; modul_py:136–137; cfg; CB |
| Erkennungs-Kandidaten (Quellen) | „Don't tell anyone I told you.“ · „Nobody leaves Lola's galley hungry.“ (LB 34) · „Seconds. He's having seconds.“ · Engine-Ticks: „… Mostly the X.“ (in fast jeder Event-Zeile: „Mostly the hamstrings / the oil / the cheese / the ute / chilli“) · „That's science.“ (lola.txt:55, MI lola_megan_2) | lola.txt:16, 58; ER g1_lola_yoga, g1_lola_massage, gv_arancini_duell, gv_karaoke, hy_lola_koster |
| Aussehen (Karte) | langes **dunkelbraunes** Haar, zerzauste Beach Waves, **goldener Haarreif**, riecht nach Knoblauch; **braune Augen** mit faulem Lächeln; Sommersprossen über Nase und Schultern; gebräunt mit weißen Bikinistreifen; **kurvig und weich, große volle Brust, Bauchnabelpiercing, goldene Creolen, Kette aus kleinen weißen Muscheln (nimmt sie nie ab)**; kocht barfuß, wenn Chiara nicht hinsieht | lola.txt:5 |
| Aussehen (PS) | Preset `Yacht_Lola`, Identitäts-LoRA **Krea_Hannah** 1.0 (+ Nsfw2/Real3/Lenovo 0.7, Redux 0.5). **Tags** passen zur Karte (Busty, Color: dark brown, Freckles, Messy, Waves, Tan Lines). **base_/fashion_prompt widersprechen der Karte**: „slim surfer build, sun-bleached **dark-blonde** beach waves with thin **braids threaded with wooden beads**, **green-hazel eyes**, tiny **nose ring**, a dozen **friendship bracelets**, small hand-poked **tattoos** (sun on wrist, wave on ankle)“. sprite_prompt: „female with **light blue eyes**“. Kein ref_image | PS presets.json Yacht_Lola |
| Outfits / Sets (3) | **Galley** (Karte: offene weiße Kochjacke, Goldknöpfe, goldener Anker, korallenfarbenes Crop-Top, kurze fleckige Leinenschürze, **barfuß**; PS `lola_galley`: dazu **Korallen-Bandana mit Holzlöffel**, **Birkenstock-Sandalen**, schwarzer Choker) · **Off Duty** (weißes Häkel-Bikinioberteil, bunte Haremshose, Muschelkette, Creolen, Haarreif, barfuß – passt) · **nude** (dünne Decke mit Sternen/Planeten, Muschelkette, Creolen, Bauchnabelring; PS zusätzlich Nippelpiercing). Engine schreibt das dritte Set **„Nude“** (groß) | lola.txt Begrüßungen; PS decks.json, set_presets.json; ebasis_py:67; ER ab_lola_handy |
| Sprites | expressions/Yacht_Lola: Galley 63, Off Duty 64, nude 99 sortiert; ST-PNG „Lola Brennan“ vorhanden; CC-Status alle Stationen fertig | Dateisystem; CC |
| Engine-Sets / Ablauf | Standard **Galley**; abends und nachts **Off Duty**. Ablauf: ganztags **Kombüse**, abends **Crewmesse**, nachts Kombüse | modul_py:130, 140 |
| Wünsche | „to feed people who are happy to be fed. **One day a little beach kitchen of her own, with no head chef.**“ | lola.txt:15 |
| Ängste | **„afraid of being useless when it counts“** (Widerspruch); Heimweh, mehr als sie zeigt; „burns things when someone watches her cook, so she never lets anyone watch“ | lola.txt:14, 77 |
| Geheimnisse (Karte) | (1) Gras im Gewürzregal, Glas „**Oregano**“. (2) **Heimweh**. (3) lässt Sachen anbrennen, wenn jemand zusieht. (4) **in Duc verknallt**, hat es genau einer Person erzählt („which on this boat means everyone“) | lola.txt:77 |
| Geheimnisse (LB/SL) | Die eine Person ist **Rosi** – am nächsten Morgen änderten sich die Quoten auf der Tafel (LB 54). Holm bringt die Teller neuerdings halb voll zurück, und „for once Lola has told nobody“ (LB 52). SL-Achse **Heimweh** (Start 2): Byron, Oma, Sydney-Koch, Anbrennen beim Zusehen | LB 52, LB 54; SL achsen.heimweh |
| Weiß (Karte) | alles übers Essen: wer vegan ist, **wer aus dem Kühlraum klaut (Totò)**, wer bei Stress Nutella löffelt; kennt die Crew daran, was sie isst; hält Lea für heimlich **in einen Delfin verliebt**; von Brücke, Maschinen und Gästen weiß sie nichts und will nichts wissen | lola.txt:79 |
| Weiß (LB) | Chiara plündert um 2 Uhr nachts den Kühlraum, isst Nutella aus dem Glas → Lola ist sicher, „a man behind it“ (LB 50; SL bruecke: „Whatever Chiara is doing up there at two … it's a man“). Bemerkt, wie viel Brot und Wasser im Tender rausgeht (Lea, LB 51). Erzählte Siri die Geistergeschichte „with improvements“ (LB 55) | LB 50, 51, 55 |
| Vorlieben / Geschenke | Grundhaltung: **Essen +, Alkohol +, Schmuck 0, Technik –, Papier 0, Natur +, Party +, Intim +** (geg_py:31). **Liebt** (Geschenkwert 2): Tim Tams (Alvas Bar, „Lola weint ein bisschen“), Alvas Rose, Bauchnabelpiercing mit Muschel, Ukulele, Vegemite-Käse-Schnecken, Space Cake. **Hasst**: Proteinriegel, Protein-Pancakes „ohne Spaß“; Technik-Geschenke –1 (Drehmomentschlüssel, Tauchlampe, Moka, Selfie-Stick …). **Unikat**: **„Ein Glas Vegemite“** („Aus Alvas Geheimvorrat. Lola nennt es Heimat in braun.“) – über MI lola_kochkurs. **Lieblingsgericht**: gegenstaende.json **Chili Noodles** (liebt lola + alva) – **aber** TAGE:68 (21.10.) legt fest „Lola: **Bao Buns**, Alva behält Chili Noodles“ | gegenstaende.json; geg_py:93–98, 131, 139, 147, 176, 327, 337, 344, 364; TAGE:68 |
| Lieblingsorte / -gesten / Intim | **keine** (Lieblingsorte nur für die 5 Crew-Frauen, basis:492–497; lieblingsgesten und intim_vorlieben nur 5 Frauen, modul.json). SL: mag Nachschlag, um Hilfe gebeten werden, Gesellschaft in der Kombüse, ein anvertrautes Geheimnis, laut gelobtes Essen vor anderen; stört: „the help“, Kritik vor der Crew, stummes Zuschauen beim Kochen, Mahlzeiten auslassen, Ärger mit Holm/Chiara | modul.json; SL mag/stoert |
| Kinks (Karte) | Füttern/gefüttert werden; träger Sex, wenn high; Dirty Talk mit Lachen; über die Kombüsen-Arbeitsfläche gebeugt mit Risiko; Hände in ihrem Haar; Sex am Morgen + Frühstück im Bett; **„being told she's good“** | lola.txt:88 |
| Beziehungen | **Duc**: mochte ihn ab dem ersten leeren Teller, stellt ihm wortlos Essen hin, wenn er Mahlzeiten auslässt (lola.txt:9); Kombüse als Hitze-Stufe 2, Kabinentür auf Stufe 4 (lola.txt:81). **Holm**: tut so, als rieche sie das Gras nicht, solange das Essen gut ist; Lola stellt ihr nach der Spätwache etwas Warmes hin, bekommt zwei Worte zurück, Teller neuerdings halb voll (lola.txt:8; LB 2, 52; holm.txt:7, 73). **Chiara**: will Schuhe und Ordnung, bekommt beides nicht; schreibt Lola einmal pro Woche auf, bekommt einen vollen Teller und ein Zwinkern; Lola nennt sie „Chi“, bewertet Chiaras Bewertungen zurück auf 10 (LB 50); Running Gag Ordnung vs. Chaos (ER gv_ocean_glitter, g1_pfannkuchen, br_basilikum; HCD:164). **Sophia**: besorgt Lieferanten/Fisch, schreibt ins Büchlein, Lola sorgt sich eine Stunde; lässt in der Kombüse Neuigkeiten fallen, „Lola has never noticed she is being read“ (LB 56); Karaoke/Tarot/Wahrheit-oder-Pflicht-Partnerin (ER). **Lea**: Fischzeichnungen gegen Tratsch, jede glaubt der anderen alles; warmer Teller nach jedem späten Tauchgang; **Delfin-Theorie** (LB 51, lola.txt:79). **Rosi**: einzige zwei, die mit ihren Geräten reden; Lola bringt Teller in den Antriebsraum, nie ein Danke; Rosi ist die eine, der Lola den Schwarm erzählte (LB 54); Engine „Rosi's partner in crime at night“ (modul_py:138). **Siri**: Mitternachts-Toastie barfuß ohne Kamera, Geistergeschichte (LB 55); findet Siris Pass → Geburtstag (ER br_siris_geburtstag). **Yasin**: „the plainest plate on the boat and never seconds“ (LB 55). **Megan**: Kühlraum zweimal geschrubbt, trotzdem Quittungen in drei Währungen im Bericht; reichte ihr ein Alu-Päckchen durchs Autofenster (LB 53); Megans Karte: „the cook who loses receipts“ (megan.txt:74); Keks-Event, Crew-Karte (ER gv_keks; MI lola_megan_1/2). **Totò**: klaut ihre Snacks, sie seine Zigaretten (Karte) – Engine: „Toto sells her ‚herbs‘“, will ihr Gras „verwahren“ (modul_py:138; ER br_lolas_notvorrat). **Maxwell**: macht ihm Proteinpfannkuchen, nennt ihn „Big Fella“; er nennt ihr Essen „lekker“, ein Liegestütz in der ganzen Saison (LB 63); kennt ihr Oregano-Glas und tut, als nicht (maximum.txt:80). **Yamamoto**: betrunken „YOU! DUET!“ an Lola (yamamoto.txt:58). **Jana**: siehe Abschnitt 3. **Alva**: Bar-Tresen-Tanz, Arancini-Duell, Kastagnetten-Mission, Tim Tams/Vegemite aus Alvas Vorrat (ER hy_lola_tresen, gv_arancini_duell; MI lola_kast_1-3). **Petru**: Ziege Fiona, Oktopus Bastianu, Thunfisch („Petru, I love you. Marry me.“), Töpferscheibe (ER hy_lola_ziege, g1_petru_oktopus, g1_petru_fisch; MI lola_tasse_2/3). **Elsa**: lenkt mit Kuchen ab (ER gv_toto_elsa). **Casanova**: keine direkte Verbindung (nur Ocean-Glitter-Popcorn liebt Casanova) | wie angegeben |

## 2. Jana – Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | **Jana Maihoff** | jana.txt:5, LB 59 |
| Alter | **21** (überall gleich) | jana.txt:5, LB 59, cc_mjy:70 |
| Herkunft | **Favoriten, Wien.** **Mittleres von drei Kindern**, „die Stille“. Hat nie etwas als Erste gemacht: Schule, Partys, Burschen waren immer Ideen anderer. Die **beste Freundin meldete beide für eine Yachtsaison an und sprang eine Woche vorher ab**; Jana fuhr trotzdem – das Erste, was sie je allein gemacht hat. Ruft **jeden Sonntag ihre Mama** an und erzählt, dass alles super ist | jana.txt:6, 80 |
| Wunde | „Immer nur mitgelaufen, nie selbst entschieden.“ | cc_mjy:74 (Profil „wunde“) |
| Rolle an Bord | **Decksfrau (deckhand), erste Saison, unter Bootsmann Totò**: Deck waschen, Fender, Leinen, Beiboot, Wasserspielzeug. **Morgens Training mit Mr. Maximum** (halb sieben, Achterdeck) | jana.txt:5, 22, 78; LB 59, 61 |
| Persönlichkeit | allein höflich, schüchtern, still, sagt „Sorry“ zu Türen; **in der Gruppe macht sie bei jeder Neckerei mit – eine Sekunde zu spät, zu laut, einen Schritt zu weit – und wird immer erwischt**; insgeheim ihr Lieblingsteil. Tag `type:follower` = **Mitläuferin** (Memory: Duc brauchte viele Runden, „nicht Anführerin/Brat, zu nah an Chiara/Rosi“). **Widerspruch:** „the shyest girl on the boat, who joins every tease because she wants to get caught.“ Nie: fängt selbst mit dem Necken an; gibt nie zu, was sie will; lässt niemanden die Katze finden | jana.txt:2, 7, 11, 14; Memory |
| Knopf / Reibung / Marotte | Knopf: **eine klare Konsequenz** (Duc erwischt sie und tut ruhig, bestimmt etwas). Reibung: frech nur in der Gruppe, wirken soll es nur bei ihm. Marotte: redet mit der Schiffskatze, wenn sie glaubt, niemand hört; zieht den Pferdeschwanz fester, wenn nervös | jana.txt:17–19 |
| Stimme / Sprache | allein klein und schnell, in der Gruppe laut und „geliehen“; **Wiener Englisch** („Na geh!“, „Jessas!“, „Servus“, „Ja eh“), „Sorry, sorry“; kopiert Chiaras Sprüche leicht falsch; nennt Duc **„Sir“**, Maxwell **„Coach“**. **Keine Stimme zugeordnet**: Karten-JSON ohne extensions.stimme, CC stimme = null, cfg kein Eintrag `jana` | jana.txt:16, 91; Karten-JSON; CC; cfg |
| Erkennungs-Kandidaten (Quellen) | „Sorry, Sir.“ · „The weather is very weather today.“ · „I walk into a room and someone gives me a mop.“ · „Why did I say yes. Why do I always say yes.“ · „There's no cat, Sir.“ | jana.txt:27, 37, 57, 66, 69 |
| Aussehen (Karte) | langes glattes **hellbraunes** Haar, Spitzen heller, im Dienst hoher Pferdeschwanz; **haselnussbraune Augen**; weiches rundes Gesicht, Röte kommt und geht; schlank mit voller Brust; tollpatschig, **blaue Flecken an den Schienbeinen** (Klampen, Fender); „wie ein Schulmädchen, das sich auf eine Superyacht verirrt hat“ | jana.txt:5 |
| Aussehen (PS) | Preset `Yacht_Jana`, Identitäts-LoRA **Krea_Emma_D** 1.0. base_prompt: „Austrian deckhand with **hazel brown eyes**“ (passt). **sprite_/fashion_prompt: „Subject: EmmaD, a 21-year-old girl with blue eyes“** (Trigger-Wort + falsche Augenfarbe). Tags: Blush, Long Legs, Slender, Light Brown, Large, Ponytail, **Winged Liner** | PS presets.json Yacht_Jana |
| Outfits / Sets (5) | **Deck** (weißes Crew-Polo in Navy-Shorts, Funkgerät, Arbeitshandschuhe; PS `jana_deck_a` + Deckschuhe) · **Bikini** (rot-weiß-rot gestreift = Österreich-Flagge, rotes Halsband, barfuß, Dutt; PS `jana_bikini_a`) · **Party Dress** (enges rotes Etuikleid mit langen Ärmeln, Schlitz, Strümpfe – **gehört Chiara, nicht gefragt**; PS `pencil_shortsleeves_red`, eine Office-Karte) · **Kitty** (weißes Katzenkostüm, rosa Halsband mit Silberglöckchen; PS `jana_kitty_b`) · **Kink** (hellrosa Crop-Zip-Hoodie offen, **goldenes Kreuz von der Erstkommunion**; PS `eisc_bib_lounge_pink`). Unbenutzte Jana-Karten in decks.json: `jana_deck_b`, `jana_bikini_b`, **`jana_partydress_a` (hellblaues Sommer-Dirndl)**, **`jana_partydress_b` (Chiaras schwarzes Slipdress)**, `jana_kitty_a` (schwarz) | jana.txt Begrüßungen; PS decks.json, set_presets.json |
| Sprites | expressions/Yacht_Jana: Deck 58, Bikini 58, Party Dress 58, Kitty 92, Kink 92 – **alle nur „roh“, 0 sortiert**; kein ST-PNG im characters-Ordner; CC-Status sprites „laeuft“ | Dateisystem; CC |
| Wünsche | **„to be good at one thing on her own.“** Insgeheim: „someone who takes her firmly in hand“ | jana.txt:15 |
| Ängste | keine explizite Angst-Zeile. Im Text: alles allein entscheiden müssen / nie bemerkt werden („someone gives me a mop“); dass Strudel entdeckt wird („Now he'll throw him overboard. Or me.“); dass Chiara erfährt, was sie tut („Please don't tell Chiara“) | jana.txt:42, 66, 69 |
| Geheimnisse (Karte) | (1) **Katze Strudel** in Antibes an Bord geschmuggelt, wohnt in einer **Kiste in der Tender-Garage** („He was alone.“). (2) will erwischt, gescholten und versohlt werden; hat jede Spanking-Geschichte auf dem Handy zweimal gelesen. (3) hat **heimlich Chiaras Kleider anprobiert**, allein in Chiaras Kabine. Laut lb_mjy:4–5 bleiben Katze und Wunsch bewusst **aus dem Weltbuch** (nur Karte) | jana.txt:82, 69; lb_mjy:4–5 |
| Weiß (Karte) | jeden Knoten, den sie noch nicht kann, jede Klampe an den blauen Flecken; jeden Chiara-Spruch, leicht falsch; **dass es bei Sophias Wetten immer um sie geht**, ohne zu verstehen warum; **wo Lola das Gras versteckt**; dass Yamamotos Kamera öfter auf sie zeigt als auf Vögel („not sure she minds“); nichts über Brücke, Maschinen, Gäste | jana.txt:84 |
| Vorlieben / Geschenke | **keine** (kein Eintrag in gegenstaende.json haltung, keine liebt/hasst, kein Unikat, kein Lieblingsgericht). Einziger Gegenstand: Kampf-Anhänger **Plüsch-Kater „Strudel“ (weiß), von Jana, Mut +1** (Plan) | gegenstaende.json; KAMPF:252 |
| Kinks (Karte) | versohlt werden; erwischt und in die Schranken gewiesen; ruhige Anweisungen; laut mitzählen; **Lob nach der Strafe**; Katzenkostüm, Halsband, Glöckchen; beobachtet werden; seine Hand um ihren Pferdeschwanz | jana.txt:93 |
| Hitze / Motor (Karte) | 1 schüchtern, neckt nur in der Gruppe → 2 neckt ihn allein, Panik → 3 provoziert absichtlich → 4 bittet um Strafe → 5 alles, gelobt danach. Steigt bei ruhiger, bestimmter, spielerischer Konsequenz; wenn er sie bemerkt, wenn sie allein ist; wenn er sich gegen die anderen auf ihre Seite stellt; **wenn er Strudels Geheimnis bewahrt**. Sinkt, wenn er sie ignoriert, mit anderen über sie lacht oder **„is only ever nice to her“** | jana.txt:86–89 |
| Status | „Jana ist NPC wie Lola (mit [Heat])“ (karten_mjy:7); Übergabe: „per Event freischaltbar“; Memory: „Eden-Engine-Einbau (personen, Events) steht noch aus“. **Nicht** unter den 7 Romanzen von Thema 4 | karten_mjy:7; Übergabe:54, 348; Memory |
| Beziehungen | **Duc**: „Sir“; allein kaum ein Wort, in der Gruppe neckt sie ihn und wartet, was er tut (jana.txt:9). **Lea**: **beste Freundin**, die zwei Tollpatschigsten an Deck; zusammen zwei Fender, einen Mopp und einen Gast-Flipflop über Bord verloren, „They blame the wind. There was no wind.“ (LB 68; jana.txt:8, 32). **Lola**: lieb zu ihr, letzter Pfannkuchen, Joint hinter der Kombüse (Abschnitt 3). **Siri**: folgt ihr seit Jahren online, bewundert sie „without a trace of irony“, trägt ungefragt Siris Handtücher; **Siri findet sie süß und vergisst immer wieder ihren Namen** (LB 70). **Chiara**: großes Vorbild; kopiert Sprüche, Lachen, Gang; Chiara findet es anstrengend, bat sie aufzuhören – „Jana repeated that too“ (LB 67); trägt heimlich Chiaras Kleid (jana.txt:37, 82). **Sophia**: schickt sie mit Mutproben, Wetten, Botschaften; Jana hält es für Freundschaft, **Sophia findet Jana „very useful“** (LB 69; jana.txt:37). **Totò**: ihr Chef, bringt ihr mit endloser Geduld Knoten bei (Palstek: „The rabbit comes out of the hole, piccola“), schimpft nie – „ein bisschen enttäuschend“ (jana.txt:8, 52). **Maxwell (Mr. Maximum)**: trainiert sie jeden Morgen 06:30, sie gibt etwa jeden zweiten Tag den Lauf auf, er lässt sie nie bei „Ich kann nicht“ aufhören, hat der Crew gesagt, sie sei stärker, als sie glaubt; sieht, dass sie nur in der Gruppe groß redet und will, dass jemand sie ernst nimmt (LB 61; maximum.txt:9, 33, 64, 80). **Yamamoto**: Kamera zeigt öfter auf sie als auf Vögel, sie wird rot, beschwert sich nicht (LB 65); Wäscherei-Szene im Katzenkostüm mit Yamamoto in Leder („Officer-san, this is not what it looks like“, jana.txt:42); KAMPF: **Yamamotos Katana** (Legendär, 12, Feuer) kommt über ein **„Event mit Jana“** (KAMPF:223). **Holm, Rosi, Megan, Yasin, Alva, Casanova, Petru, Elsa**: keine Einträge | wie angegeben |

### 2.1 Was für Jana in der Engine fehlt (Volltextsuche „jana“, „strudel“, „maihoff“ in module/, kern/, werkzeuge/eden_rise/)
- **Kein Personeneintrag** in modul.json (`personen` hat 14 Figuren, ohne Jana, Maxwell, Yamamoto); nicht in `bekannt_start`,
  nicht in `werte.vertrauen.je`, kein Begehren, kein Tagesablauf, keine Sets, keine Stimme (cfg), keine Job-Zeilen.
- **Kein Event, keine Mission, kein Gegenstand, keine Gag-Kette, kein Bordrat** (ereignisse.json, missionen.json,
  gegenstaende.json: 0 Treffer). Kein Fakt in story.json/story_faelle.py, keine Bühnenszene.
- **Strudel** existiert nur in jana.txt und als geplanter Plüsch-Anhänger (KAMPF:252). Tierfiguren der Engine sind
  Möwe Kevin (Gag-Kette), Ziege Fiona (ER hy_lola_ziege), Oktopus Bastianu (ER g1_petru_oktopus).
- **Yamamotos Katana „Event mit Jana“** ist nur Plan in KAMPF.md, Event existiert nicht.
- Spielleiter-Bogen fehlt (`X:\AI\Spielleiter\boegen\` hat Lola, nicht Jana); Sprites unsortiert; kein ST-PNG.
- Vorhanden sind: Karte (Char-Builder-JSON, CC Station Karte „fertig“), Weltbuch-Einträge LB 59, 61, 65, 67–71, PS-Preset
  mit 5 Sets und Rohbildern.
- Raum für Strudel existiert: `tender_garage` (Lieblingsort Leas, basis:495; SL Lola zählt sie zu „Technik“).

---

## 3. Lola ↔ Jana – alle vorhandenen Verbindungen

### 3.1 Direkte Belege
| Fakt | Quelle |
|---|---|
| „Lola is sweet to her, and sometimes they share a joint behind the galley.“ | jana.txt:8 (DE :101) |
| „Lola is always kind to Jana and **saves her the last pancake**. Now and then the two of them sit **behind the galley after service** and share a joint, and **Jana giggles for an hour**.“ (aktiver Paar-Eintrag „Lola <-> Jana (behind the galley)“) | LB 71; lb_mjy:71–73 |
| Jana weiß, **wo Lola das Gras versteckt** (= Gewürzregal, Glas „Oregano“) | jana.txt:84; lola.txt:77 |
| CC-Profil Jana: „Lola lieb, ab und zu ein Joint.“ | cc_mjy:82 |
| **Lolas Karte erwähnt Jana nicht** (Lola-Karte 17.10., Jana entstand 19.10.); auch kein „Jana“-Eintrag in Lolas SL-Bogen | lola.txt; SL |
| Keine gemeinsame Begrüßung, kein Event, keine Mission, kein Gegenstand, keine Story-Szene | Volltextsuche |

### 3.2 Gemeinsame Orte und Zeiten (belegt, aber nicht verknüpft)
- **06:30 morgens**: Lola steht in der Kombüse (Begrüßung „Breakfast Chaos“, lola.txt:27); Jana trainiert um halb sieben
  mit Maxwell auf dem Achterdeck (LB 61). Lola macht Maxwell Proteinpfannkuchen (LB 63), hebt Jana den letzten
  Pfannkuchen auf (LB 71); Lolas Pfannkuchen-Porträts von der ganzen Crew (ER g1_pfannkuchen).
- **Hinter der Kombüse nach dem Service** (LB 71) – Lolas Kombüse liegt neben der Crewmesse (lola.txt:22).
- **Tender-Garage**: Strudels Kiste (jana.txt:82); Lola bemerkt, wie viel Brot und Wasser im Tender rausgeht (LB 51,
  bezogen auf Lea); SL Lola „technik“-Räume schließen die Tender-Garage ein.
- **Nachts an Ducs Tür**: Lola 01:00 „Knock Knock“ (lola.txt:37; ER ab_lola_klopft „kurz nach Mitternacht“), Jana 02:00
  „Late Night Confession“ (jana.txt:47) – gleiche Bauform (Klopfen, Decke/Hoodie, „Can I come in?“ / „punish me“).
- **Crew-Party auf dem Sonnendeck**: Lolas „Sundeck Sundowner“ 21:00 (lola.txt:32), Janas „Borrowed Dress“ 23:00
  (jana.txt:37).

### 3.3 Spiegelungen in den Karten (Fakten nebeneinander)
| Lola | Jana | Quelle |
|---|---|---|
| Jüngste von vier, „die Laute“ | Mittlere von drei, „die Stille“ | lola.txt:75; jana.txt:80 |
| kam für einen Sommer nach Europa und blieb – allein | erste Sache, die sie je allein gemacht hat | lola.txt:6; jana.txt:6 |
| ruft jeden Sonntag die **Oma** in Byron an; **Heimweh, mehr als sie zeigt** | ruft jeden Sonntag die **Mama** an und **erzählt, dass alles super ist** | lola.txt:75, 77; jana.txt:80 |
| beide **erste Saison** | | lola.txt:5; jana.txt:5 |
| Wunde: „nie mehr als eine Beiköchin“ → Wunsch: eigene Strandküche **ohne Küchenchef** | Wunde: „immer nur mitgelaufen“ → Wunsch: **in einer Sache allein gut sein** | lola.txt:6, 15; jana.txt:15; cc_mjy:74 |
| Angst, **nutzlos zu sein, wenn es darauf ankommt** | „I walk into a room and someone gives me a mop.“ | lola.txt:14; jana.txt:66 |
| erzählt Tratsch weiter, **„usually a bit wrong“** | kopiert Chiaras Sprüche, **„gets them slightly wrong“** | lola.txt:7; jana.txt:8, 16 |
| **kann kein Geheimnis behalten** | hütet zwei Geheimnisse (Strudel, Chiaras Kleider) und ihren Wunsch | lola.txt:17; jana.txt:82 |
| Knopf: **gebraucht werden** | Knopf: **eine klare Konsequenz** | lola.txt:18; jana.txt:18 |
| Kink: „being told she's good“ | Kink: „praise after punishment“ | lola.txt:88; jana.txt:93 |
| widersetzt sich Chiara (Schuhe, Ordnung) | **kopiert** Chiara, trägt ihr Kleid | lola.txt:8; jana.txt:8, 37 |
| wird von Sophia **gelesen**, merkt es nie (LB 56) | wird von Sophia **benutzt**, hält es für Freundschaft (LB 69) | LB 56, 69 |
| Lolas Missionen laufen über Duc als Überbringer („Du gibst sie ihr. Mir glaubt sie nicht …“) | Jana ist Sophias Überbringerin („Sophia says … Sophia bets“) | MI lola_tasse_3, lola_megan_2; jana.txt:37; LB 69 |
| „Never: lets anyone leave her galley hungry“ | „Never: lets anyone find the cat“ | lola.txt:11; jana.txt:11 |
| weiß nichts über Brücke, Maschinen, Gäste | weiß nichts über Brücke, Maschinen, Gäste | lola.txt:79; jana.txt:84 |
| Tier-Gag: Ziege Fiona („She chose me.“) | Katze Strudel („He was alone.“) | ER hy_lola_ziege; jana.txt:69 |

### 3.4 Gemeinsame Dritte
- **Lea**: Lolas Delfin-Theorie und warmer Teller (LB 51) · Janas beste Freundin (LB 68). Lea + Lola gemeinsam in
  ER gv_wettschwimmen, gv_wasserschlacht, gv_versoehnung (Lola Zuschauerin), g1_kevin_butter („Kevin is dead to me“).
- **Chiara**: Lolas Gegenspielerin in der Kombüse (LB 50, ER gv_ocean_glitter) · Janas Idol (LB 67).
- **Maxwell**: Lola „Big Fella“, ein Liegestütz (LB 63) · Jana „Coach“ (LB 61).
- **Sophia**: liest Lola (LB 56) · benutzt Jana (LB 69).
- **Siri**: Lolas Mitternachts-Toastie (LB 55), Geburtstag (ER br_siris_geburtstag) · Janas Idol, trägt ihre Handtücher (LB 70).
- **Totò**: Snacks/Zigaretten-Tausch, „verkauft ihr Kräuter“ (lola.txt:8; modul_py:138) · Janas Chef (jana.txt:8).
- **Yamamoto**: Duett-Ruf an Lola (yamamoto.txt:58) · Kamera auf Jana (LB 65).
- **Gras-Regeln**: Bordrat `br_lolas_notvorrat` (T2) kann `kein_gras_an_bord` setzen (Lola täglich –2 Vertrauen) oder
  `gras_nur_nach_dienst` („Lolas Abend-Event bleibt möglich“) – betrifft den gemeinsamen Joint hinter der Kombüse
  (ER bordregeln).

### 3.5 Ansatzpunkte für engere Verwebung (nur Fakten aus den Quellen)
1. Der einzige aktive Freundschafts-Beleg (LB 71) ist ein Ritual mit Ort und Zeit: hinter der Kombüse, nach dem Service,
   ein Joint, Jana kichert eine Stunde; dazu „der letzte Pfannkuchen“.
2. Lola kann kein Geheimnis behalten und will, dass Duc ihr eins anvertraut (lola.txt:17); Jana hat genau die Geheimnisse,
   die niemand finden soll (Strudel, Chiaras Kleid) und weiß selbst Lolas Versteck (jana.txt:84). Lolas Weltbuch-Regel:
   Was eine Figur für sich behält, steht nur in ihrer Karte (lb_lmh:5, lb_mjy:4).
3. Beide Wünsche drehen sich um „etwas allein können“: Strandküche ohne Küchenchef / in einer Sache allein gut sein
   (lola.txt:15; jana.txt:15).
4. Beide rufen sonntags zu Hause an; Lola mit Heimweh, Jana mit „alles super“ (lola.txt:75, 77; jana.txt:80).
5. Beide sind in Sophias Netz, ohne es zu merken (LB 56, 69).
6. Lolas Missionen sind fast alle Geschenke für andere über einen Boten (MI lola_tasse_*, lola_kast_*, lola_megan_*,
   lola_paella_*); Jana ist der Bote einer anderen (LB 69).
7. Strudel lebt in der Tender-Garage, Lola versorgt jeden mit Essen und weiß, was im Tender verschwindet (LB 51) – eine
   Quelle zu „Lola und Strudel“ gibt es nicht.
8. Morgens 06:30 sind beide wach (Kombüse / Training), Lola backt Pfannkuchen für Maxwell (LB 63) und hebt Jana den
   letzten auf (LB 71).
9. Lolas Engine-Ziege Fiona und Janas Katze Strudel sind beide „Tiere, die sie gewählt haben“ (ER hy_lola_ziege, jana.txt:69).
10. Prämisse (Übergabe:107, 111): Akt 2 „Tiere mit Halsbändern“ auf Alons Anwesen, Akt 3 „Alon will die Halsbänder an
    Menschen testen“. Jana: Katze an Bord, im Kitty-Set selbst ein Halsband mit Glöckchen (jana.txt:42). Nur
    nebeneinandergestellt, keine Quelle verbindet das.

---

## 4. Mechaniken je Figur

### Lola
- **Status**: Nebenfigur, `romanzierbar: false` (modul_py:129) – **im Widerspruch zu Übergabe Thema 4** (Lola romanzierbar,
  eine von 7 Festa-Szenen). `freie_zeit_extra` (wird in freien Phasen wie die Frauen angeboten) und `isst_mit` (isst beim
  Crew-Essen mit) (modul_py:321; kern/rollen.py:15–16). Bekannt ab Start (modul_py:158).
- **Vertrauen**: Skala 0–5, **Start 2** (höchster NPC-Start, modul_py:153). Ermittlungsschwelle 1 (sagt Wahres ab V1,
  modul_py:346). Memory-Design 17.10.: „ab 3 Frühstück +1 Energie, ab 2 Bordtratsch-Tipp“.
- **Begehren**: `werte.begehren.je` enthält nur die 5 Crew-Frauen (modul.json). Events vergeben trotzdem Begehren für Lola
  (g1_lola_yoga, g1_lola_massage, br_gemeinsam_duschen, gv_wahrheit_pflicht, du_koch_lola, ab_lola_klopft, ab_lola_handy);
  kern/ereignisse.py:220–225 wendet Punkte nur an, wenn `begehren.lola` in den Werten existiert → **vermutlich wirkungslos**.
  Prüfer erlaubt Begehren für „Frauen/Lola/Alva“ (ebasis_py:324–325).
- **Bordtratsch**: story.json nebenboegen.regeln.tratsch: „Lolas Tratsch (an Bord) und Alvas Tratsch (an Land) zeigen nur,
  wo man nachsehen sollte – nie allein Beweis.“ Umsetzung kern/ermittlung.py:332–350: je Fall Tipps mit `wer: lola`,
  ab Vertrauen und Tag, höchstens ein Gerücht pro Szene, „💬 Lola (Gerücht): …“. **Aber** `rollen.tratsch` = [alva, toto]
  (modul_py:320) – Lola steht dort nicht. Übergabe:249–251: Lolas Tratsch als Stufe-1-Spur von Chiaras Lernen, Lola gibt
  später den Tipp „frag lieber anders“ (beschlossen, nicht gebaut).
- **Essen-Regel** (gegenstaende.json essen; geg_py:75–77): **1 Essen pro Tag** aus Lolas Kombüse, selbst essen (Energie +1)
  oder verschenken; **ab Lolas Vertrauen 3 zwei Essen** (`lola_ab_3`, modul_py:277 `zweites_essen_ab: 3`). Punkte:
  Lieblings +6, normal +1, Ekel –6, Deckel 36.
- **Laden „Lolas Kombüse“** (laeden.json; laeden_py:6, 59): an Bord, Set Galley, wechselndes Sortiment 6, Snacks/Desserts
  (19 Snacks mit eigenem liebt/hasst, geg_py:322–348), **Gras-Snacks**: Space Cake ab V3, Brownie „Captain's Calm“ ab V4
  (Kontrollrisiko 10, Space Cake nächster Morgen Energie –1). Grußzeilen in drei Stufen (fremd 0–1 / Freundin 2–3 /
  Nähe 4–5, „Every time you walk in, I burn something. That's a compliment, babe.“), Pleite: „Your tab is a little
  drawing of you on the fridge.“ Ladengeräusch `lola_brutzeln` (sfx_eden_rise.py:139).
- **Kochen**: Ducs Küche-Stärke „in Lolas Kombüse gekocht“ (kern/handel.py:797), 1 pro Tag statt Essen, Crew-Essen = alle
  Frauen an Bord + `isst_mit` (kern/handel.py:851–859). Neue Küche (TAGE:61–90, beschlossen, nicht gebaut): **Kühlschrank
  in der Kombüse**, jede Figur bringt ihr Lieblingsgericht als Rezept bei, Lola = **Bao Buns**, Nonna Fiora liefert Zutaten.
- **Vertrauens-Abende** (abende_py; story.json nebenboegen.lola: Freischaltung **Tag 3**, darf „T3 nacht naehe“ füllen,
  nie in exklusiven Szenen, „Gerade keine Zeit“ verschiebt ohne Verlust):
  - `ab_lola_klopft` (T3–7 Nacht, **V≥3**, einmalig): bekifft an Ducs Tür, „the stars told me to come here“; Optionen
    hereinlassen (Intim-Szene, Lola führt) / erst reden (Nachklang) / „Nicht heute, komm wieder, wenn du klar bist“ (V+4,
    „I'll come back sober and twice as dangerous“). Nachklang: Pfannkuchen in Herzform beim Frühstück.
  - `ab_lola_handy` (T4–7 Abend/Nacht, **V≥4** + Flag lola_abend): Foto ihres Rückens, „Again?“, Ort frei wählbar, Set „Nude“.
  - SL-Bogen (ST-Spieltisch): Achsen **Nähe** (Start 3), **Heimweh** (Start 2), **Gebrauchtwerden** (Start 4); Versuch
    „Persönlich“ = nach Byron, Oma, der verlassenen Küche fragen und die Stille nicht füllen; Nachwirkung: kocht nachts
    etwas, erzählt „one piece of gossip she absolutely should not be telling him“.
- **Missionen** (MI, alle `von: lola`):
  - `lola_kochkurs` T2–7, Empathy SG 13, Kochen: **Lola lernt Thịt kho** (Ducs vietnamesisches Gericht) → V+6, Unikat
    **lola_vegemite** („ihr letztes Glas“). Einzige Mission, die ihr selbst gilt.
  - `lola_tasse_1–3` T2–7: Tasse für **Chiara** (Farben erfragen Charm 12 → Ton zu **Petru** → töpfern Perception 12) →
    `chiara_tasse`, V+4. „Von mir glaubt sie, da ist Gras drin.“
  - `lola_kast_1–3` T3–7: **Alvas** Kastagnetten der Großmutter (zuhören beim Essen Perception 12 → Knochenleim → leimen
    Cunning 13) → `alva_kastagnetten`. Petru: „Für sie. Nicht von mir.“
  - `lola_megan_1–2` T3–6: **Karte für Megan** von der ganzen Crew („Everyone hates the boss, mate. I reckon that's
    lonely.“) → `megan_crewkarte`, V+4.
  - `lola_paella_1–2` T2–7: Paella für die Crew, Safran von Alva, „damit nach der Woche alle wieder an einem Tisch sitzen“
    → Moral +1, V+4. Dazu `chiara_coldroom` erwähnt Lolas Experimente.
- **Gegenstände mit Lola-Bezug**: `lolas_gewuerz` „Ocean Glitter“ (Rosi liebt; aus hy_lola_koster, gv_ocean_glitter,
  du_koch_lola) · `plektrum` Lolas Plektrum (Charm-Vorteil, aus gv_karaoke) · `lolas_pesto` (Moral +1, aus br_basilikum) ·
  `bauchnabelpiercing` (aus hy_lola_tresen / Alva) · `energieriegel` (Laden ab V3) · `frischer_fang` („Lola macht daraus ein
  Fest“) · `franzbroetchen` („Lola hat geholfen“). **Ohne Quelle**: `lolas_band` Freundschaftsband (Attribut Empathy +1,
  quelle „mission“) und `lolas_kekse` (Megan liebt, quelle „event/mission“) – keine Mission/kein Event vergibt sie.
- **Bordregeln**: `kein_gras_an_bord` (Lola täglich V–2), `gras_nur_nach_dienst`, `kombuese_ordnung` (Chiara +2, „Lolas Gags
  in der Kombüse seltener“), `essen_geteilt` (Moral +1).
- **Gags**: Kette `ocean_glitter` (3 Stufen, Lola beschriftet Chiaras Etiketten um); Möwe `kevin` (Lola: „Kevin is dead to
  me“); `megan_lacht` über Lola-Events (gv_keks, g1_helikopter, hy_megan_rundgang).
- **Job-Zeilen** (basis:764–777): Angebot/Erfolg/Fehlschlag/Patzer, durchgehend „Captain“ („We're a team now. Lola and the
  Captain. No, Captain and Lola.“; „I'd marry you, but I'd lose the ring by Tuesday.“).
- **Duelle**: `du_koch_lola` (Koch-Showdown, Perception SG 14 mit Küche-Vorteil; „Wir kochen zusammen“ → „a date with
  knives“; „Sie gewinnen lassen“ → „You let me win. I saw it.“).
- **Kampf-Bezug**: **Lolas Damast-Kochmesser** (Episch, Schaden 6, Messer, „Geschenk Lola“, KAMPF:217); Küche-Stärke: Snacks
  heilen 10 statt 6 (KAMPF:64). **Kein Plüsch-Anhänger** von Lola (KAMPF:250–262; der Koala ist Alvas).
- **Versprechen**: br_lola_flach „Lola bekommt morgen als Erste eine Suppe ans Bett“ (gehalten wenn Flag `lola_suppe`) –
  **kein Setzer für `lola_suppe` gefunden** (kern/, werkzeuge/, module/).
- **Epilog**: kern/abschluss.py kennt Lola nicht (kein Epilog-Eintrag).

### Jana
- Keine Mechanik in der Engine (siehe 2.1). Karten-Mechanik nur für SillyTavern: Hitze 1–5 mit Motor (jana.txt:86–89).
- Geplant in Docs: Plüsch-Kater „Strudel“ (Mut +1, KAMPF:252), Yamamotos Katana über „Event mit Jana“ (KAMPF:223).
- Memory: „später per Event freischaltbar wie Lola“; Sonder-Event „Fetischspiel mit Yamamoto, Duc erwischt sie“ (=
  Kartenbegrüßung „Caught In The Laundry“, jana.txt:42).
- Maxwell-Bezug: Training morgens; Maxwell ist laut Memory „später wichtig fürs Kampfsystem und das neue Attribut Stärke
  (Training bei ihm)“.

---

## 5. Events je Figur (module/eden_rise/ereignisse.json)

**Jana: 0 Events.** Lola erscheint in **64** Events.

### Lola – Hauptrolle (spricht/handelt oder Event dreht sich um sie)
| id | Tage/Phase | Kern |
|---|---|---|
| br_lolas_notvorrat | T2 Nacht (Rosi spricht) | Rosi findet 1 kg Gras „BASIL ♥“ in der Kühltruhe; über Bord (Lola –8, Bordregel kein Gras) / Totò verwahrt (Lola +6, Kontrollrisiko) / „nur nach Dienst“ |
| br_letzte_steaks | T3–6 Nacht | Lola will alle 12 Steaks grillen, „give them a beautiful death“ vs. Rationieren (Chiara) |
| br_siris_geburtstag | T2–6 Nacht | Lola fand Siris Pass in der Wäsche: morgen Geburtstag; „Lola backt, nur die Crew singt“ |
| br_singen_ohne_strom | T2–6 Nacht | Lola will mit Gitarre und Kerzen singen; Siri nur ohne Kamera |
| br_gemeinsam_duschen | T3–6 Nacht, Strom ≤6 | „Shower in pairs … basically environmentalism“; Chiara dagegen |
| br_abschiedsfest | T6 Nacht | „Whatever happens tomorrow, tonight we dance. Barefoot.“ Fest vs. Schlaf (Chiara) |
| br_lola_krank | T2–6 Nacht (Chiara spricht) | Lola mit Sonnenstich, Rosi in Schürze; Duc kocht |
| br_lola_flach | T2–6 Nacht (Chiara spricht) | Lola mit Muschelvergiftung, Duc kocht für 13 (Bún riêu), Versprechen Suppe |
| hy_lola_tresen | T2–7 Nacht, V Alva ≥2 | Alva ruft an, Lola tanzt barfuß auf dem Tresen; Tender / Rechnung (→ Piercing) / Chiara anrufen |
| hy_lola_ziege | T2–6 Tag, an Land | Lola in Petrus Werkstatt mit Ziege **Fiona** („She chose me.“) |
| hy_lola_koster | T2–7 Tag/Dinner | Vorkoster gesucht („I need a mouth. Yours.“) → Ocean Glitter |
| g1_pfannkuchen | T2–5 Frühstück | bekifft gebackene Pfannkuchen-Porträts; Chiaras verbrannt, Rosis wunderschön |
| g1_lola_yoga | T2–6 Frühstück | Sonnenaufgangs-Yoga im Drei-Fäden-Bikini; mitmachen / Handtuch / zuschauen (Klatsch) |
| g1_lola_massage | T2–6 Abend | Massage-Salon in der Messe; hinlegen / sie massieren (Nachklang) / ablehnen |
| g1_katerfruehstueck | T2–7 Frühstück, Flag lola_kater | Frühstück mit Sonnenbrille, versalzenes Omelett |
| g1_petru_oktopus | T3–7 Frühstück/Tag | Lola und Petrus Oktopus Bastianu im Spülbecken |
| gv_ocean_glitter | T2–7 Tag/Dinner | Lola vs. Chiara: umbeschriftete Etiketten |
| gv_arancini_duell | T3–6 Abend, an Land | Lola vs. Alva, Duc Jury |
| gv_karaoke | T2–6 Abend | Lola (Pub-Lieder) vs. Sophia (Chansons) → Plektrum |
| gv_tarot | T3–7 Abend/Nacht | Lola legt Sophia „Die Liebenden“, zeigt auf Duc |
| gv_wahrheit_pflicht | T3–7 Nacht | Lola + Sophia stellen Aufgaben; Lolas Pflicht = Kuss-Moment |
| gv_keks | T5–6 Tag, Megan an Bord | Lola hält Megan einen Keks hin |
| ab_lola_klopft / ab_lola_handy | T3–7 / T4–7 | Vertrauens-Abende (Abschnitt 4) |
| du_koch_lola | T2–7 Tag/Dinner | Koch-Showdown in ihrer Kombüse |

### Lola – Nebenrolle (Stimme, Option, Zuschauerin)
| id | Tage | Lola-Anteil |
|---|---|---|
| br_alvas_lieferung | T2–6 Nacht | „A happy crew is a sexy crew, Captain.“ |
| br_ein_tisch | T2–5 Nacht | „Let's eat like a family. A weird family. With a seagull.“ |
| br_basilikum | T2–6 Nacht | „Australian basil … Spiritual pesto.“ → lolas_pesto |
| br_nacktbaden, br_investoren_dinner (T5) | | Option mit Lolas Kuchen / Lola kocht für Megans Investoren |
| hy_megan_rundgang, hy_eden_hotline, hy_alva_diesel_tanz, hy_megan_dinner, hy_koeln_frist | | Kombüse zeigen; „I'm a ten! … Drink water.“; Lola zum Tanzen schicken; Teller für Megans Laptop; „Cologne? You were going to leave?“ |
| g1_unit01_klonk, g1_kevin_butter, g1_fiona_muetze, g1_chiara_inspektion, g1_qualle, g1_toto_pizza, g1_petru_fisch, g1_alva_besuch, g1_sophia_liest_vor, g1_helikopter | | Kuchen in Gefahr; letzte Butter; findet Fiona süß; Krümel versteckt; Hausmittel; Ananas-Pizza; „A WHOLE TUNA“; will Wein; fächelt sich Luft zu; Handtuch fliegt („I'm the cook, I'm naked.“) |
| gv_sonnencreme, gv_strip_poker, gv_siri_yasin, gv_wettschwimmen, gv_toto_elsa, gv_armdruecken, gv_alva_chiara, gv_zigarren, gv_wasserschlacht, gv_megan_chiara, gv_versoehnung, gv_festa_outfits, gv_angeln, gv_quiz | | Zuschauerin; in gv_festa_outfits: „A red flower for everyone! I'll steal them from the mayor.“; in gv_quiz: „CHEATER!“ |
| du_koch_toto, du_reparatur_rosi (Lolas Mixer), du_poetry_sophia („Ode an Lolas Kühlschrank“) | | Jury/Anlass |
| auf_gitarre, auf_herkunft | | bringt Tim Tams; reicht Duc Tee: „Nobody's going anywhere. Literally. We're stranded.“ |

Auffällig: Kein Event zeigt Lolas Heimweh, die Oma, den Sydney-Koch oder die Strandküche. Lolas „Captain“-Anrede zieht
sich durch alle Event-Zeilen.

---

## 6. Story-Rolle im Wochenbogen (7-Tage-Fassung, neutral)

### Lola
- **T1 Abend `auftakt_party`** (Achterdeck): in story.json `personen`, in buehne.json **nicht** `anwesend`; buehne will:
  „Feed everyone and tell Duc about the glowing sea.“ Ausgangslage: „Lola swears the sea will glow tonight.“
- **T1 Nacht `blackout` „Die Stille“** (Kombüse, 06:15, exklusiv, nur Lola anwesend): Afterparty bis halb vier, Duc kann
  nicht schlafen, sitzt bei Lola, die fürs Sonnenaufgangsfrühstück backt. **„Zuerst endet die Musik. Dann sagt Lola
  ‚Duc?‘. Erst danach der Alarm.“** In allen Fällen gleich. buehne will: „Finish her bread – until something is very wrong,
  and then not be alone with it.“ (story_py:234–236; buehne_py:59–64)
- **T2 Nacht `gemeinsames_essen`** (Messe 23:15, mit Lea, Rosi): „Lola has cooked whatever was left, and somehow it is the
  best thing anyone has eaten in days … Somebody laughs for the first time since the music stopped.“ Will: „Make everyone
  eat and laugh.“ (buehne_py:179–183)
- **T3 Nacht `naehe`**: Lolas Einladung (Nebenbogen) darf diesen Platz füllen; „Lola bekifft: sehr horny und versaut“
  (story_py:329–332). Freischaltung Lola-Nebenbogen = Tag 3 (story_pruefen.py:453 prüft das).
- **T5 Frühstück `megan_kommt`** (Messe 08:30, mit Chiara): „Lola has baked as if for royalty.“ Will: „Impress the boss
  with breakfast.“ (buehne_py:247–251)
- **T7 Nacht `schlussbild`** (Messe 22:00, mit Chiara, Rosi): „The last dinner together … Someone pulls up one more chair.“
  Will: „Feed everyone a last time.“ (buehne_py:368–373)
- Regel: Lolas und Alvas persönliche Geschichten nehmen keiner Hauptszene den Platz und kosten keine Phase
  (story.json nebenboegen.regeln).
- Neue Akt-1-Woche (Übergabe:130, 218): **Tag 3 „abends Lolas erstes Essen in der Bucht“** (Duc: Tag 3, nicht 2); nach der
  Explosion fragt Holm, ob alle in Ordnung sind, **kümmert sich um Lola**, dann bricht sie zusammen.
- Übergabe:249–251 (Chiaras Stolz-Mechanik): Lolas Tratsch als Akt-1-Spur; Lola gibt den Tipp „frag lieber anders“.

### Jana
- **Keine Story-Rolle** (weder story.json noch buehne.json noch Übergabe-Akte). Übergabe nennt sie nur als Teil von Paar 6
  „per Event freischaltbar“ (Übergabe:348). Im Cold Open rettet Maxwell **Totò und Lea** (Übergabe:146) – Janas Chef und
  ihre beste Freundin; Jana wird dort nicht erwähnt.

---

## 7. Widersprüche, 7-Tage-Reste, Passung zur neuen Prämisse

### Widersprüche
1. **Lola romanzierbar?** Übergabe Thema 4 (Duc 22.10.): ja, mit Festa-Szene und Lebensziel. Engine: `romanzierbar: false`
   (modul_py:129), kein Begehren-Wert (modul.json werte.begehren.je), keine Lieblingsorte/-gesten/Intim-Vorlieben, kein
   Epilog. Lolas Begehren-Folgen in 7 Events laufen vermutlich ins Leere (kern/ereignisse.py:220–225).
2. **Anrede**: Karte „Boss“/„mate“ (lola.txt:9, 81; SL hitze 1) vs. Engine „Captain“ (modul_py:137, job_zeilen,
   laeden.json, Event-Zeilen) + „babe“. Jana: „Sir“.
3. **Lolas Aussehen**: PS base/fashion_prompt (Surfer-Figur, dunkelblond mit Perlenzöpfen, grün-haselnuss, Nasenring,
   Armbänder, Tattoos) vs. Karte (dunkelbraun, braune Augen, kurvig, große Brust, Bauchnabelpiercing, Muschelkette) vs.
   PS-Tags (dunkelbraun, Busty) vs. sprite_prompt („light blue eyes“). Galley: Karte barfuß, PS Birkenstock + Bandana.
4. **Janas Aussehen**: PS sprite/fashion „EmmaD … blue eyes“ vs. Karte/base_prompt haselnussbraun; Tag „Winged Liner“ bei
   der Schüchternen. Party-Dress-Set nutzt eine Office-Karte (`pencil_shortsleeves_red` mit langen Ärmeln), eigene
   Jana-Party-Karten (Dirndl, Chiaras Slipdress) liegen ungenutzt.
5. **Set-Name** „nude“ (PS, Karte, Memory) vs. „Nude“ (ebasis_py:67, ER ab_lola_handy).
6. **Lieblingsgericht Lola**: gegenstaende.json Chili Noodles (liebt lola + alva) vs. TAGE:68 (21.10.) Bao Buns.
7. **Totò und Lola**: Karte „Totò klaut ihre Snacks, sie seine Zigaretten“ vs. Engine „Toto sells her ‚herbs‘“
   (modul_py:138) und Totò als Gras-Verwahrer (ER br_lolas_notvorrat); Karte „wer aus dem Kühlraum klaut (Totò)“.
8. **Tratsch-Rolle**: story.json/kern: Lola = Bordtratsch; `rollen.tratsch` = [alva, toto] ohne Lola (modul_py:320).
9. **Weltbuch doppelt**: LB 34 „W15 Lola Brennan (cook)“ und LB 49 „W16 Lola Brennan (ship's cook)“ beide aktiv, ähnlicher
   Inhalt; Nummern doppelt vergeben (W14/W16 Megan LB 35/36, W15 Holm LB 42). Karten-JSON-Bücher (24 Einträge) ohne
   Lola-/Jana-Paareinträge.
10. **Wett-Tafel**: Lola ist in Duc verknallt und erzählte es Rosi, „the odds … changed the next morning“ (LB 54) – die
    Tafel nennt aber nur Chiara, Sophia, Lea (LB 9).
11. **Doppelte Krankheits-Events**: br_lola_krank (Sonnenstich) und br_lola_flach (Muschel) beide T2–6 Nacht, gleiche
    Sprecherin, gleicher Kern („Duc kocht“).
12. **Datenfehler**: br_abschiedsfest `sprecher: lola` und `links: lola` (doppelt).
13. **Gegenstände/Flags ohne Quelle**: `lolas_band`, `lolas_kekse`; Versprechens-Flag `lola_suppe` ohne Setzer.
14. **Vertrauensstart**: Engine Lola V2 vs. SL Nähe 3 (andere Skala, ST-Spieltisch).
15. **Lea vs. Jana**: beide „deckhand“ (LB 20: Lea Decksfrau + Wassersport/Ausflüge; Jana unter Totò) – Aufgaben
    überschneiden sich (Tender, Wasserspielzeug, jana.txt:22).
16. **Lola weiß nichts über Brücke/Maschinen** (lola.txt:79), ist aber in der Engine die meistgenutzte Tippgeberin der
    Ermittlung (Details VERDECKT) – über Beobachtungen in Messe/Kombüse, nicht über Technik.

### 7-Tage-Reste (für 21 Tage umzubauen)
- Karten-Setting beider: **Antibes, Mitte August, „noch acht Wochen Saison“**, Charter jede zweite Woche, Duc „seit drei
  Wochen an Bord“ (lola.txt:22; jana.txt:22). Lola-Begrüßung „Market Day“ in Antibes, „Sushi Emergency“ in der Charterwoche.
  Jana: Strudel „in Antibes gefunden“ (passt weiter).
- Engine: letzte Nacht der Saison, Werft Calvi (buehne auftakt_party); Lola backt fürs Sonnenaufgangsfrühstück.
- Fenster: Lola-Abende ab **Tag 3/4** (abende_py, story.json), Nebenbogen „Freischaltung Tag 3“; Missionen T2–7 bzw. T3–6;
  `br_abschiedsfest` **T6** („Morgen entscheidet sich alles“); `megan_kommt` T5; `gv_keks` T5–6; `br_letzte_steaks` T3–6
  (Kühlung fällt aus); viele Events setzen Strommangel/„gestrandet“ voraus (br_singen_ohne_strom, br_gemeinsam_duschen,
  br_ein_tisch „We're all stuck in the same bay“).
- Memory-Design „Lola Tag 3 / Alva Tag 4“ beruht auf dem 7-Tage-Takt.

### Passung zur neuen Prämisse (Übergabe)
**Lola – wo sie andockt**
- **Lebensziel aus der Karte passt direkt in die Bucht**: „eine kleine Strandküche ganz für sich, ohne Küchenchef“
  (lola.txt:15) – Prämisse „Herz von C: Kochen, Freundschaft und Liebe“, Festa in Cala d'Orsu (Übergabe:25).
- **Kochsystem**: TAGE beschließt Kühlschrank in der Kombüse, Lieblingsrezepte, Nonna Fiora als Zulieferin, Kochen beim
  Dinner – Lolas Kombüse ist der Ort dafür (kern/handel.py:797). Duc-Persona Küche (europäisch + südostasiatisch) trifft
  Lolas Kochkurs Thịt kho und du_koch_lola.
- **Akt 1**: Cold Open in ihrer Kombüse („Duc?“), Holm kümmert sich nach der Explosion um sie, Tag 3 erstes Essen in der
  Bucht (Übergabe:130, 218); Tratsch als Spurenquelle („zeigt nur, wo“) passt zum fairen Krimi und zur Anhörung (Zeugen mit
  eigener Loyalität, Übergabe:120).
- **Dorf-Fäden vorhanden**: Petru (Töpferscheibe, Fiona, Bastianu, Thunfisch), Alva (Tresen, Arancini-Duell, Kastagnetten,
  Vegemite/Tim Tams aus Alvas Vorrat), Casanova nur über die „Blumen der Bürgermeisterin“ (gv_festa_outfits).
- **Megan-Achse**: Karte für Megan („that's lonely“), Keks, Alu-Päckchen durchs Autofenster (LB 53) – passt zu Megans Akt-3-
  Wende (Übergabe:164).
- **Festa**: gv_festa_outfits, br_singen_ohne_strom, br_abschiedsfest, Ukulele/Plektrum – Lola als Musik/Fest-Motor.
- **Angst** „nutzlos, wenn es darauf ankommt“ + SL-Achsen Heimweh/Gebrauchtwerden liefern Bogen-Material; in der Engine
  nicht genutzt.

**Lola – Lücken**
- Kein Bezug zu Bucht-Verkauf, Alon, A.V. Estates, ESG; keine Strandküche, keine Oma, kein Sydney-Koch, kein Heimweh in
  Events/Missionen; einzige „eigene“ Mission ist der Kochkurs.
- Romanzen-Infrastruktur fehlt (Widerspruch 1); keine Festa-Szene, kein Lebensziel-Feld, kein Epilog.
- Grauton nur angedeutet: Gras an Bord (Kontrollrisiko, Küstenwache), Tratsch, der Geheimnisse anderer verbreitet (LB 54
  Quoten), „half wrong“-Weitergabe.
- Ihr „Captain“ kollidiert mit Holm als Kapitänin und Chiaras Kommando-Wunsch (Übergabe:213–215).

**Jana – wo sie andockt**
- **Mitläuferin** vs. Prämissen-Gewissensfrage **„Was du unterschreibst“** (Übergabe:24) – Jana als Figur, die immer
  mitmacht, wenn alle mitmachen (jana.txt:7). Nur thematisch, keine Quelle verbindet beides.
- **Maxwell / Kampf**: tägliches Training, „stronger than she thinks“ (LB 61); Kampf-Plan: Plüsch-Kater Strudel (Mut +1),
  Yamamotos Katana per Jana-Event (KAMPF:223, 252); Maxwell rettet im Cold Open Totò und Lea (Übergabe:146).
- **Lea-Freundschaft**: Lea ist Pilotfigur mit Margot-Bogen und Content-Tauchgang mit Siri in Akt 2 (Übergabe:184); Jana
  ist Leas beste Freundin und Siris Fan (LB 68, 70).
- **Tier-Motiv**: Strudel an Bord; Akt 2 Alons Tiere mit Halsbändern (Übergabe:107, 111).
- **Akt 2/3 „neue NPCs + Romanzen“** sind ausdrücklich vorgesehen (Übergabe:108–111) – Jana existiert schon als Karte.

**Jana – Lücken**
- Komplett ohne Engine (2.1), ohne Stimme, ohne sortierte Sprites, ohne ST-PNG, ohne SL-Bogen.
- Kein Wunsch-Bezug zur Bucht; kein Lebensziel, kein Bogen, kein Platz in den 3 Akten; Romanzen-Status ungeklärt (Karte
  hat Hitze 1–5 wie Lola, Thema 4 nennt sie nicht).
- Karte trägt das alte Setting (Antibes/Charter); Katze Strudel bewusst nicht im Weltbuch – andere Figuren „wissen“ in ST
  nichts von ihr.

---

## VERDECKT – Fall-Rollen (nicht im Chat nennen)

Quellen: werkzeuge/eden_rise/story_faelle.py (`faelle_py`), story.json faelle/verdaechtige; kern/ermittlung.py:332–350.
**Lola ist in keinem Fall verantwortlich** und nicht unter den Verdächtigen (story.json verdaechtige: chiara, lea, sophia,
rosi, yasin; modul_py:344 verdacht ohne Lola). **Jana kommt in keinem Fall vor.** Lola ist in allen Fällen Zeugin des
LM3-Ausfalls (Zeitleisten-Zeilen „LM3-Ausfall … [duc, lola, holm]“) und die Tippgeberin der Tratsch-Mechanik (je Fall zwei
Tipps `wer: lola`, Vertrauen 2).

### Allgemeine Fakten (alle Fälle)
- r_07: Afterparty bis etwa 03:30, **Musik aus Lolas Lautsprecher** (Wissende duc, lola, toto) (faelle_py:94–96).
- r_10: Blackout-Szene in der Kombüse, „erst die Musik aus, dann dein Name, dann der Alarm“, T2 05:50 (faelle_py:103–105).
- r_19: Holms Bauchschmerzen auf der Party, Wissende duc, lola, chiara (faelle_py:149–150).
- h_21: Lolas eigene Nacht: Afterparty bis 03:30, am Heck geraucht, ab 04:45 Kombüse gebacken (faelle_py:244–247).
- h_02: Lola: Chiara saß von halb zwei bis Viertel vor drei mit ihrem Ordner am Messetisch (Alibi, faelle_py:170–173).

### Fall 1 (Chiara verantwortlich)
- f1_10: **Lola-Aussage**: Chiara ging kurz vor zwei („muss lernen“) und kam um halb drei zurück, Tee, ins Bett
  (faelle_py:359–362) – Gegenbeleg im Widerspruch f1_ws1 zu Chiaras Lüge „bis halb drei in der Messe gelernt“
  (faelle_py:393; HCD:273). Zeitleiste T2 01:55 / 02:30 mit Zeugin Lola (faelle_py:314, 320).
- Holm erzählt Lola beim Kaffee T2 08:30 vom Zettel „Bedienfolge 4-17“ am Pult (Übermittlung f1_07/f1_17, faelle_py:335–345).
- Tipps: „Chiara trägt ihren dicken Ordner seit gestern überall mit“ (ab T4 nach Gegenhandlung) · „Holm hat beim Kaffee
  erzählt, sie hat nachts einen Zettel in die Logbuchmappe gesteckt“ (faelle_py:413–416).

### Fall 2 (Lea verantwortlich – Lea ist offen, Pilotfigur)
- Tipps: „Lea saß die halbe Nacht in der Navi-Ecke. Taschenrechner, drei Zettel.“ (ab T3) · „Lea redet seit Tagen von ihrem
  Opa und einem Schiff. Frag mal den Fischer, der ihr dauernd schreibt.“ (faelle_py:528–531).

### Fall 3 (Sophia verantwortlich)
- f3_17: **Lola-Aussage**: Sophia kam um Viertel vor zwei aus dem Crewgang in die Messe (befragbar T3–7) (faelle_py:628–630);
  dient als Gegenmittel zu Sophias Rosi-Ablenkung („Maschinenbuch 01:40, Lola 01:45“, faelle_py:655).
- Tipps: „Sophia hat mich letzte Woche gefragt, ob die Bar in Cala d'Orsu morgens Tische reserviert. Letzte Woche!“ ·
  „Sophia war vorletzte Nacht noch am Büro-PC. Um Mitternacht.“ (ab T4 nach Gegenhandlung) (faelle_py:668–670).

### Fall 4 (Rosi verantwortlich)
- f4_10: **Lola-Aussage**: Rosi ging um Viertel vor acht mit Kaffee allein in den Kontrollraum (faelle_py:722–724);
  Zeitleiste T2 07:50 „Rosi hebt die Sperre auf … allein im Kontrollraum“, Zeugin Lola (faelle_py:694).
- Tipps: „Rosi und Toto haben sich gestern über Quoten gezankt. Toto hat so ein Buch.“ · „Rosi hat mitten in der Nacht ein
  altes Messgerät in die Kiste in der Werkstatt geräumt.“ (ab T3 nach Gegenhandlung) (faelle_py:781–784).

### Fall 5 (Yasin verantwortlich)
- Tipps: „Yasin hat was Verschmortes in seine Kamerakiste gepackt. Hat gestunken wie Toast.“ (ab T4 nach Gegenhandlung) ·
  „Siri hat das ganze Video. Sie redet nur nicht drüber.“ (faelle_py:904–906; SYD:189).

### Fall 6 „Niemand an diesem Tisch“ (verantwortlich: niemand an Bord; Sündenbock Rosi)
- f6_12: **Unterschriftenliste** am Messe-Brett T2 23:30: „Wir glauben, es war Rosi – sie war um 01:40 im Maschinenraum.“
  **Unterschrieben von Totò, Yasin, Chiara, Lola** (faelle_py:924, 964–968).
- Tipps: „Holm hat gestern Nachmittag auf der Brücke über irgendein LM geflucht. Laut.“ · **„Die Liste mit den
  Unterschriften? Toto hat sie rumgehen lassen. Ich hab unterschrieben, weil alle unterschrieben haben. Tut mir leid.“**
  (ab T3 nach Gegenhandlung) (faelle_py:1001–1004).
- Bezug zu Paar 6 (nur Fakt): Lolas Satz ist ein Mitläufer-Moment – Janas Kartenkern ist „Mitläuferin“ (jana.txt:7;
  Memory). Rosi ist die Person, der Lola ihren Schwarm anvertraute (LB 54).

### Für die Anhörung (Akt 1, Übergabe:115–124) relevant
- Lola ist in den Fällen 1, 3, 4 eine Zeugin mit einer konkreten Uhrzeit-Aussage gegen bzw. über die verantwortliche Person;
  in Fall 6 selbst Mitunterzeichnerin der falschen Anschuldigung. Zeugen dürfen laut Übergabe lügen, um jemanden zu
  schützen – Lolas Karte: „She can't keep a secret“ (lola.txt:17).

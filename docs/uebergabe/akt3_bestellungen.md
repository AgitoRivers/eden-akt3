# Akt 3 · Bestellliste Bilder und Ton

Stand 04.11.2026 · Cloud-Sitzung `akt3-cloud`. Bis ein Bild da ist, nutzt das Spiel den genannten Platzhalter (Name aus `modul.json`, Raumliste geprüft). Hintergründe nach `docs/wiki/systeme/hintergruende.md` (keine Tür, Vordergrund unten Mitte frei, frontal, 4 Seeds).

## Hintergründe

| Name (Vorschlag) | Szene | Bildidee | Platzhalter |
|---|---|---|---|
| `town_hall_stairs` | 5.11 Don vor Pascals Tür | schmale Steintreppe im Rathaus, Kisten am Fuß, Licht von oben | `village_piazza` |
| `pascal_room` | 5.12 Die Schublade | kleines Zimmer über dem Rathaus, Schreibtisch mit Schubladen, weißer Fedora an einem Haken, ordentlich wie ein Museum | `village_piazza` |
| `burned_post` (und je ein Bild für `batu`, `bar`, `werkstatt`) | Baustellen in drei Stufen | verkohltes Haus, Gerüst, später fast fertig; Piraten nur als Werkzeug am Boden, keine Personen | `village_harbour` |
| `villa_cellar` | 5.25 Frame 1–2 | alter Weinkeller, Fässer, dazwischen ein Server-Rack mit blauen Lichtern | `power_room` |
| `villa_office` | 5.25 Frame 3 | Büro unter einer Treppe, ein Ordner auf dem Tisch, altes Familienfoto an der Wand | `main_salon` |
| `villa_dining` | 5.26 Name Your Price | langer Tisch für zwei, großes Fenster auf die Bucht bei Nacht, Dorf mit Lichtern unten | `alon_keynote` |
| `scrap_field` | Expedition „The Scrap Field“ (F-10) | Macchia mit liegengebliebenen weißen Robotern, Gras durch die Gelenke | Rastplatz-Bild der Macchia |
| `church` bei Nacht, außen | 5.13 Every Report | Kirchenstufen mit Kerzen | `village_piazza` |

## Sprites und Posen

| Figur | Pose / Gefühl | Szene | Bildidee |
|---|---|---|---|
| Minicu | verbunden, ernst, neutral frontal | 5.1, 5.4 | Kopfverband, Arm in einer Schlinge, Axt gesenkt |
| Alva | verletzt, liegend/sitzend, ernst | 5.3 | Verband an der Schläfe, Decke |
| Sandru | am Boden, ernst (ohne surrende Schienen) | 5.19 | zwischen weißen Regalen |
| Sandru | neue Schienen, stehend, ruhig | 5.20 | Schienen mit Rosis Farbe, Namensschild ISKANDER oder SANDRU |
| Buenaventura | ohne Hut, ernst | 5.2 | Hut in der Hand, Flagge auf halbmast im Hintergrund |
| Alon | in Person, Anzug über dem Exoskelett, ruhig | 5.26 | Kanon-Look, aber ohne Bühne |
| U Riscossore | mit Orange, ruhig | 5.17, 5.30 | Kanon-Look |
| Kommissarin | neutral, ernst | 5.30 | Beamtin aus Ajaccio, Klapptisch, Ordner (neue Nebenfigur, Legenden-Kommentar nötig) |
| Pascal | im weißen Fedora hinter Alon, lächelnd | 5.26 | keine Zeile, nur Bild |

## Neu mit dem Bau (04.11.2026)

| Was | Wo | Platzhalter |
|---|---|---|
| Sprite **AlonExo** (Alon im Exoskelett, ruhig, Kampf-Posen idle, avatar, windup, attack, heavy_windup, heavy_attack) | Endkampf `a3_alon` | `AgentAlpha` |
| Hintergrund `villa_dining` (Tisch für zwei, Fenster über der Bucht bei Nacht) | `a3_villa_dinner`, `a3_villa_preis` | `alon_keynote` |
| Hintergrund `villa_terrace` (Terrasse über dem Dorf, Drohnenkamera) | `a3_villa_ende`, `a3_villa_kampf`, Kampf `a3_alon` | `alon_keynote`, Kampf `eden_rise_village_rooftops.png` |
| Hintergrund `villa_cellar` | `a3_villa_keller`, `a3_villa_ordner`, Kampf `a3_villa_keller` | `power_room`, Kampf `eden_rise_crate_hall.png` |
| Hintergrund `scrap_field` | Karte `a3_scrap` | `antenna_ridge` |
| Sprite Buenaventura prüfen (`bonaventure_standard`, Ordner „Captain Bonaventure“) | alle Szenen mit ihm | – |

## Items

| Item | Bild |
|---|---|
| Cellar Key | alter Eisenschlüssel mit Bändchen von einer Setzlingskiste |
| Pascal's Ledger | Kassenbuch in sauberer Handschrift |
| White's Orders | Ordner mit Einsatzplan, Stempel „Phase 3“ |

## Ton

Kein `ton` auf Kartenzeilen ohne gewählte Datei (`test_sfx`). Gewünscht, noch nicht gesetzt:

| Klang | Szene |
|---|---|
| Schienen verstummen (Surren bricht ab) | 5.19 |
| Tropfen in einen Eimer | 5.14, 5.30 |
| Brecheisen an Holz | 5.12 |
| Vespa-Hupe zweimal | Dank-Szene Post |
| Glocke im richtigen Takt (gibt es vielleicht schon als `tk_glocke`) | 5.32 |

## Prompts für Character Design

Stand 04.11.2026 · fertige Prompts für Krea, Englisch. Hintergründe nach [`hintergruende.md`](../wiki/systeme/hintergruende.md): Frontansicht aus der Raummitte, Vordergrund unten in der Mitte leer, keine Tür, ohne Personen, positiv formuliert, immer 4 Seeds. Nachtfassungen und die Baustufen per `hintergrund_edit.py` aus der gewählten Tagfassung, damit alle Bilder gleich aussehen. Sprites im Format der `fashion_prompt` (front view, head to knees, beige plain background) und mit dem Set der Figur als Vorlage. Die Spalte „heute“ nennt den Platzhalter, den das Spiel jetzt nutzt.

### Hintergründe

| Name | Prompt | heute |
|---|---|---|
| `villa_dining` | Frontal view from the middle of a modern dining room in an old Corsican hillside villa at night, a long dark wooden table set for only two against the back wall, a huge window behind it showing the bay far below with the small lights of a fishing village, white stone walls with cold designer lamps on both sides, the lower middle foreground left empty, no door anywhere, not a single person is in the shot, present-day contemporary, photorealistic. | `alon_keynote` |
| `villa_terrace` | Frontal view of a wide stone terrace of a Corsican hillside villa at dusk, a low stone balustrade at the back with the bay and the village rooftops far below, a small drone camera on a tripod at the right edge, potted olive trees on both sides, the lower middle foreground left as empty open stone floor, no door anywhere, not a single person is in the shot, present-day contemporary, photorealistic. | `alon_keynote`, Kampf `eden_rise_village_rooftops.png` |
| `villa_cellar` | Frontal view from the middle of an old vaulted wine cellar under a Corsican villa, rows of oak barrels along both side walls, and between the barrels at the back wall a modern server rack with blue blinking lights and neat cables, warm bulbs on the ceiling mixed with cold blue light, the lower middle foreground left as empty stone floor, no door anywhere, not a single person is in the shot, present-day contemporary, photorealistic. | `power_room`, Kampf `eden_rise_crate_hall.png` |
| `scrap_field` | Frontal view of a clearing in the Corsican maquis in daylight, broken white robots and dog-like machines lie in the dry grass along both sides and at the back, wild grass and cistus grow through their joints, green hills and a blue sky behind, the lower middle foreground left as an empty dirt path, not a single person is in the shot, present-day contemporary, photorealistic. | `antenna_ridge` |
| `town_hall_stairs` | Frontal view of a narrow stone staircase inside an old Corsican town hall, worn white steps lead up to the back wall, soft daylight falls from a small high window, a few wooden crates stand at the foot of the stairs on the left and right, the lower middle foreground left as empty stone floor, no door anywhere, not a single person is in the shot, present-day contemporary, photorealistic. | `village_piazza` |
| `pascal_room` | Frontal view from the middle of a small, very tidy office above a Corsican town hall, a wooden desk with many drawers against the back wall, an empty coat hook and a pale square on the white wall where a picture once hung, shelves with neatly labeled folders on both sides, the lower middle foreground left empty, no door anywhere, not a single person is in the shot, present-day contemporary, photorealistic. | `village_piazza` |
| `church_night` (außen) | Frontal view of the wide stone steps along the plain side wall of a small old Corsican village church at night, dozens of candles burning on the steps, a small round window and the bell tower above the wall at the back, dark village houses on both sides, the lower middle foreground left as empty piazza stones, no door anywhere, not a single person is in the shot, present-day contemporary, photorealistic. | `church` (innen) |
| `burned_post` Stufe 0 | Frontal view of a small burned village post office on a Corsican piazza, black walls and an empty roof frame against the sky, ash and broken slate on the ground at the sides, a faded yellow post sign above the window, the lower middle foreground left as empty piazza stones, not a single person is in the shot, present-day contemporary, photorealistic. | `village_piazza` |
| `burned_batu` Stufe 0 | Frontal view of a burned small Asian grocery shop in a Corsican village, black walls, a melted shop sign with Vietnamese letters, a burned counter at the back, ash on the shelves along both sides, the lower middle foreground left empty, not a single person is in the shot, present-day contemporary, photorealistic. | `batu_shop` |
| `burned_bar` Stufe 0 | Frontal view of a burned village bar in Corsica, black stone walls, the long bar counter at the back wall burned, a cracked chalkboard still hanging behind it, broken chairs along both sides, the lower middle foreground left empty, not a single person is in the shot, present-day contemporary, photorealistic. | `alvas_bar` |
| `burned_werkstatt` Stufe 0 | Frontal view of a burned boat workshop at a Corsican harbour, black roof beams against the sky, a half burned wooden boat on blocks at the back, burned tools and nets along both side walls, the lower middle foreground left empty, not a single person is in the shot, present-day contemporary, photorealistic. | `petru_workshop` |
| je Haus Stufe 1 (Edit) | Same view and same house, now with a simple wooden scaffolding along the walls, fresh timber beams and stacks of slate at the sides, tools lying on the ground, not a single person is in the shot. | wie Stufe 0 |
| je Haus Stufe 2 (Edit) | Same view and same house, now almost rebuilt: new roof with fresh slate, clean walls, the scaffolding only on one side, a few tools left at the side, not a single person is in the shot. | wie Stufe 0 |

### Sprites

| Figur und Pose | Prompt | heute |
|---|---|---|
| **AlonExo** (idle, avatar, windup, attack, heavy_windup, heavy_attack) | A fictional tech billionaire in his fifties with a short buzz cut and aviator sunglasses, wearing a piano-black exoskeleton that is clearly a medical support frame under a sleek armour shell, a chrome jetpack on his back and a ray pistol, calm and precise, no resemblance to any real person; one image per combat pose in the same framing as the existing enemy sprites (for example `AgentAlpha`): idle standing, avatar head and shoulders, windup raising the pistol, attack firing a beam, heavy_windup with the jetpack glowing, heavy_attack diving forward from the air. | `AgentAlpha` |
| Minicu verbunden | A very tall, broad, soft gentle giant with long shaggy dark brown hair and a full beard, a bandage around his head and his left arm in a sling, cream work shirt and brown canvas dungarees, a woodcutter's axe held low, calm serious face, front view, full body shot from head to knees, beige plain background. | `minicu_standard` |
| Alva verletzt | Alva Santoni, a curvy 35-year-old Corsican bar owner with big dark curly hair piled up loosely, a white bandage at her temple, sitting up under a grey wool blanket, tired and serious but awake, front view, full body shot from head to knees, beige plain background. | `alva_standard` |
| Sandru am Boden | Sandru, a Corsican-Moroccan supermarket manager in a white A.V. polo shirt with a name tag reading ALEX, sitting on the floor with his back against a white shelf, black leg braces silent and dark, quiet serious face, front view, full body shot from head to knees, beige plain background. | `sandru_av` |
| Sandru mit neuen Schienen | The same man standing straight and calm, the leg braces now repainted in Rosi's colours with small hand-made marks, a new name tag reading ISKANDER (second version: SANDRU), white polo shirt, a small proud smile, front view, full body shot from head to knees, beige plain background. | `sandru_av` |
| Buenaventura ohne Hut | Captain Buenaventura, a handsome Spanish pirate captain around 44 with long dark curls and a waxed moustache, purple velvet coat with gold trim, blue and white striped shirt, an old gold coin amulet, holding his hat in both hands against his chest, serious and ashamed, front view, full body shot from head to knees, beige plain background. | `bonaventure_standard` |
| Riscossore mit Orange | U Riscossore, an old Black man in a white linen suit that is slightly yellow at the cuffs, warm cream and gold tones, calmly peeling an orange with a small knife, never in a hurry, front view, full body shot from head to knees, beige plain background. | `riscossore_standard` |
| Kommissar Luciani | Commissioner Luciani, a Corsican state official from Ajaccio in his fifties, grey suit and plain tie, reading glasses, a thick folder under his arm, neutral serious face, front view, full body shot from head to knees, beige plain background. | kein Sprite, nur Sprechername (der Kommissions-Bildschirm ist nicht gebaut) |
| Maître Delorme | Maître Delorme, a lawyer from Lyon in his late forties, elegant dark navy suit, silver tie, perfectly combed grey hair, a slim leather briefcase, calm and polite with a very small smile, front view, full body shot from head to knees, beige plain background. | kein Sprite, nur Sprechername |
| Holms Mutter (optional) | An old Norwegian woman around 80 from Ålesund, tall and straight, white hair in a simple bun, light blue eyes, a hand-knitted sweater and a warm wool coat, a walking stick, kind but very direct, front view, full body shot from head to knees, beige plain background. | keiner, nur Zeile (E-130) |

**Hinweise für Duc:** Der Kommissar hieß zuerst wie Alva (Santoni) und heißt jetzt Luciani (umbenannt 04.11.2026). Die alte Tabelle oben nennt eine „Kommissarin“, Code und Drehbuch (5.25: „zwei Männer aus Ajaccio“) einen Mann; der Prompt folgt dem Code.

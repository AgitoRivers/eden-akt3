# Auszug: Alva / Lulu

Automatisch erzeugt von werkzeuge/figur_auszug.py. Fall-Bezüge stehen nur im letzten Abschnitt VERDECKT (Duc liest diese Dateien nicht; im Chat nie Inhalte daraus nennen).

## Engine (modul.json)

```json
{
 "name": "Alva Santoni",
 "stimme": "Alva Santoni",
 "kurz": "Alva",
 "romanzierbar": false,
 "beschreibung": "owner of the only bar in Cala d'Orsu, 35, took the bar over from her father; knows everything that happens in the village, sells diesel under the counter, flirts with everyone and means it with nobody, calls everyone 'o figliolu'",
 "ablauf": {
  "*": "alvas_bar",
  "dinner": "alvas_terrace"
 },
 "set_standard": "alva_standard",
 "set_regeln": [
  {
   "ort": "village_piazza",
   "set": "alva_flamenco_noche"
  },
  {
   "phase": "nacht",
   "set": "alva_flamenco_noche"
  }
 ],
 "geschenk_reaktion": [
  "ruf",
  "Alva takes it with a knowing grin and a teasing remark; by tomorrow the whole village will know."
 ]
}
```

## Karte (EN)

_Keine Karte in karten_neu._

## Weltbuch

_Keine Einträge._

## Events

| id | Art | Tage/Phase | Rolle | Titel – Lage |
|---|---|---|---|---|
| br_alvas_lieferung | bordrat | T2–6 nacht | erwähnt | Alvas Lieferung – Alva würde morgen drei Kisten Wein und Myrte schicken. Auf Rechnung, „unter Freunden“. Totò grinst. Lola tanzt schon ein bisschen auf der Stelle. |
| br_petrus_boot | bordrat | T2–5 nacht | erwähnt | Petrus Morgenfang – Petru nimmt morgen früh zwei Leute mit zum Fischen. Wer mitfährt, ist bis Mittag weg. Lea hat schon ihre Stiefel an. |
| br_crew_kasse | bordrat | T3–6 nacht | erwähnt | Yacht-Zeug für die Crew-Kasse? – Totò hat eine Liste gemacht. Zwei Kisten Champagner, vier Bademäntel, ein Ersatzpropeller. Alles Eigentum der Eden Group, alles leicht zu verkaufen. |
| br_lola_krank | bordrat | T2–6 nacht | erwähnt | Wer kocht morgen? – Lola liegt mit Sonnenstich in der Koje und murmelt Rezepte. Morgen kocht also jemand anderes. Rosi hat sich schon eine Schürze umgebunden. Das macht allen Angs… |
| br_poker_einladung | bordrat | T3–6 nacht | erwähnt | Pokerabend bei Alva – Alva lädt zum Poker ins Hinterzimmer. Gespielt wird um Diesel und, wenn es spät wird, um Kleidung. Sophia hat ganz zufällig ein Kartenspiel in der Tasche. |
| hy_lola_tresen | handy | T2–7 nacht | anrufer | Lola tanzt auf dem Tresen – Alva ruft aus der Bar an. Hinter ihr tanzt Lola barfuß auf dem Tresen. Die Fischer klatschen. |
| hy_alva_tratsch | handy | T2–7 tag/abend | anrufer | Dorftratsch von Alva – Alva schreibt eine lange Sprachnachricht. Im Hintergrund klirren Gläser. Sie hat gehört, was eine der Frauen an Bord besonders mag. |
| hy_alva_nach_feierabend | handy | T3–7 nacht | anrufer | Alva nach Feierabend – Die Bar ist zu. Alva sitzt auf dem Tresen, die Haare offen, und trägt etwas Rotes mit Rüschen, das eindeutig nicht für die Gäste gedacht ist. Sie hält das Hand… |
| hy_alva_diesel_tanz | handy | T3–6 abend | anrufer | Ein Kanister für einen Tanz – Alva hat noch einen Kanister Diesel. Sie verkauft ihn nicht. Sie tauscht ihn. Gegen einen Tanz, heute Abend, auf ihrem Tresen, vor dem ganzen Dorf. |
| g1_alva_besuch | gag1 | T2–6 tag/abend | handelnd | Alva rudert vorbei – Alva rudert mit einem kleinen Boot an die Badeplattform. Eine Flasche Wein, zwei Gläser, ein Kleid mit sehr wenig Rücken. Sie ruft laut nach Duc. Chiara steht … |
| gv_strip_poker | gagv | T4–7 abend | links | Strip-Poker um einen Kanister – Alva hat noch einen Kanister Diesel und gibt ihn nur her, wenn jemand sie im Poker schlägt. Gespielt wird um Kleidung. Nach drei Runden fehlen Alva der Schal u… |
| gv_arancini_duell | gagv | T3–6 abend | rechts | Das Arancini-Duell – Lola behauptet, ihre Arancini sind die besten des Mittelmeers. Alva hat dazu eine Meinung. Das ganze Dorf schaut zu. Duc ist Jury. |
| gv_alva_chiara | gagv | T3–7 abend | links | Alva gegen Chiara – Alva stellt Duc ein Glas hin und setzt sich auf den Tresen, sehr nah. Chiara steht auf, nimmt das Glas und stellt es zwei Hocker weiter. |
| gv_casanova_alva | gagv | T3–5 tag | rechts | Die VIP-Lounge – Madame Casanova will Alvas Bar für die Festa zur VIP-Lounge machen. Mit Samtseil. Alva will ihre Bar so lassen, wie sie ist: laut, voll und für alle. |
| gv_elsa_alva | gagv | T3–6 tag | rechts | Diesel unter dem Tresen – Elsa sitzt an Alvas Tresen und trinkt einen Espresso. Unter dem Tresen stehen vier Dieselkanister. Jeder weiß es. Elsa schaut Alva lange an. |
| ab_alva_barabend | abend | T4–7 abend | pid | Nach Feierabend bei Alva – Die letzten Fischer sind gegangen. Alva dreht das Schild auf „Chiuso“ und schließt die Tür ab. Sie geht ins Hinterzimmer und kommt in etwas Rotem mit Rüschen z… |
| ab_alva_handy | abend | T5–7 abend/nacht | pid | Alva ruft: „Komm vorbei.“ – Alva ruft an. Sie trägt etwas Schwarzes mit weißen Punkten und schwingt einen kleinen Schlüssel an einer roten Kordel vor der Kamera. Den Schlüssel zum Hinterz… |
| du_koch_alva | duell | T3–7 abend | gegner | Koch-Showdown: Korsika gegen Saigon – Alva hat die Tische zusammengeschoben. Auf der einen Seite stehen ihr Fiadone und ihre Wildschwein-Pastete, auf der anderen deine Garküche aus zwei Gaskochern.… |
| auf_karaoke | auftritt | T3–7 abend | publikum | Karaoke in Alvas Bar – Alva hat eine Karaoke-Maschine aus den Neunzigern im Keller gefunden. Das Mikrofon knistert, die Texte laufen auf einem Röhrenfernseher. Die halbe Crew ist da.… |
| gv_elsa_kiste | gagv | T3–7 tag/abend | zuschauer | Kartoffeln, die miauen – Elsa hat eine von Totòs Kisten am Kai aufgehalten. Auf der Kiste steht „Kartoffeln“. Die Kiste miaut. Totò behauptet, es seien sehr junge Kartoffeln. Elsa hat … |

## Missionen

- **alva_kassenbuch** (von alva, T2–7, perception SG 12): Alvas Kassenbuch – Alvas Kassenbuch ist ein Schuhkarton voller Zettel. Die Steuer will Zahlen bis Monatsende. Sie stellt dir einen Myrtenlikör hin und schiebt den Karton über die Theke.
- **alva_kuehlung_eis** (von alva, T2–7, None SG None): Kühlung: Eis besorgen – Totò hat Stangeneis im Lagerraum. Das rettet die Festa-Ware für heute – morgen schwitzt sie wieder.
- **alva_kuehlung_reparatur** (von alva, T2–7, cunning SG 13): Kühlung: selbst reparieren – Der Kompressor ist tot, die ganze Festa-Ware schwitzt. Zerlegen, Relais tauschen – gelingt es, läuft die Kühlung für immer, und Alva zahlt.
- **alva_kuehlung_toto** (von toto, T2–7, None SG None): Kühlung: Totò um ein Relais bitten – Totò hat „zufällig“ genau das Relais, das Alvas Kompressor braucht. Er will kein Geld. Er will, dass du dich erinnerst.
- **alva_diesel** (von alva, T3–7, cunning SG 12): Diesel unter der Theke – Alva hat da „etwas im Keller“. Abholen musst du es selbst, und zwar so, dass die Leutnantin es nicht sieht.
- **petru_schild_1** (von petru, T3–7, None SG None): Ein Schild für Rosi: das Brett – Petru hat Rosi gestern vor seiner Werkstatt stehen sehen. Sie hat lange auf das leere Brett über seiner Tür geschaut und gesagt: „Scuderi & Figlie. So hätte Papa es genannt.“ Petru will ihr eines sch…
- **elsa_fund_2** (von elsa, T2–7, None SG None): Ein Fundstück für Lea: die Batterie – Der Tauchcomputer ist tot. Elsa öffnet ihn mit einem winzigen Schraubenzieher aus ihrer Dienstweste. Die passende Knopfzelle hat sie nicht. Im Dorf gibt es so etwas nur bei Alva.
- **lola_kast_1** (von lola, T3–7, perception SG 12): Alvas Kastagnetten: zuhören – Nach drei Gläsern hat Alva Lola erzählt, dass die Kastagnetten ihrer Großmutter zerbrochen in einer Schublade liegen. Herausgeben würde sie sie nie. Außer an jemanden, der sich einen Abend lang anhör…
- **alva_gennaro_1** (von alva, T3–7, cunning SG 13): Ein Heiliger für Totò – Totòs San Gennaro aus Neapel ist in der Nacht des Ausfalls vom Regal gefallen. Seitdem lacht Totò nicht mehr, und ein Totò ohne Lachen ist schlecht fürs Geschäft. Alva will ihm einen neuen besorgen. …
- **alva_gennaro_2** (von alva, T3–7, None SG None): Ein Heiliger für Totò: Gold – Alva will den Heiligen selbst bemalen. „Golden, wie in Neapel. Golden wie ein Lottogewinn.“ Die Goldfarbe hat sie im eigenen Regal, aber sie zahlt nicht für Geschenke an Totò. Grundsätzlich.
- **alva_gennaro_3** (von alva, T3–7, perception SG 12): Ein Heiliger für Totò: die Übergabe – Alva sagt, einem Neapolitaner gibt man nichts einfach so. Man gibt es ihm beim Essen. Und zwar bei einem, das nach seiner Mutter schmeckt: Genovese, sechs Stunden Zwiebeln.
- **casanova_elsa_2** (von casanova, T2–7, None SG None): Ein Geschenk für die Leutnantin: das Leinen – Gebunden wird in Leinen, sagt Madame Casanova, wie ein Staatsdokument. Leinen gibt es nur bei Alva, und mit Alva redet Madame Casanova seit dem Dorfladen-Streit nicht mehr.
- **lola_megan_2** (von lola, T3–6, None SG None): Eine Karte für Megan: der Rahmen – „Ohne Rahmen schmeißt sie es weg. Mit Rahmen muss sie es aufhängen. That's science.“ Rahmen gibt es nur bei Alva.
- **alva_kuehlung_relais** (von alva, T2–7, None SG None): Kühlung: ein Relais einbauen – Der Kompressor braucht nur ein neues Relais. Es einzubauen ist leicht, es zu bekommen nicht: Auf der Insel hat so etwas nur einer.

## Gegenstände / Essen

- quelle **Arancini vom Bäcker** (arancini, geschenk): 
- quelle **Korsisches Olivenöl** (olive_oil, geschenk): 
- quelle **Tim Tams aus Alvas Bar** (tim_tams, geschenk): Die einzigen australischen Kekse in ganz Korsika. Lola weint ein bisschen.
- quelle **Korsische Feigen** (feigen, geschenk): 
- quelle **Canistrelli mit Anis** (canistrelli, geschenk): Korsisches Gebäck, hält ewig.
- quelle/liebt **Myrtenlikör** (myrtle, geschenk): 
- quelle **Hausgemachter Limoncello** (limoncello, geschenk): 
- quelle **Cap Corse Aperitif** (cap_corse, geschenk): 
- quelle **Fußkettchen mit Muschel** (shell_anklet, geschenk): 
- quelle **Diva-Sonnenbrille in Herzform** (herzbrille, geschenk): 
- quelle **Schmaler Silberring vom Markt** (silberring, geschenk): 
- quelle **Tauchlampe** (dive_torch, geschenk): 
- quelle **Neapolitanische Espressokanne** (moka, geschenk): 
- quelle **Polarisierte Sonnenbrille** (polbrille, geschenk): 
- quelle **Taschenmesser** (schweizer_messer, geschenk): 
- quelle **Notizbuch aus Leder** (notebook, geschenk): 
- quelle **Gedichtband aus dem Antiquariat** (gedichtband, geschenk): 
- quelle **Herrenmagazin mit Pin-up** (pinup_magazin, geschenk): Italienisches Magazin, auf dem Titel eine schöne, halbnackte Frau. Totò liest es „wegen der Artikel“.
- quelle **Schöne Muschel** (pretty_shell, geschenk): 
- quelle **Handgestrickte Wollsocken** (wool_socks, geschenk): 
- quelle **Wollmütze mit Norwegermuster** (wollmuetze, geschenk): 
- quelle **Duftkerzen „Maquis“** (candles, geschenk): 
- quelle **Bauchnabelpiercing mit Muschel** (bauchnabelpiercing, geschenk): 
- hasst **Eden-Group-Kappe** (eden_cap, geschenk): 
- quelle **Tüte Konfetti** (konfetti, geschenk): 
- quelle **Glitzer-Schärpe „Miss Cala d'Orsu“** (schaerpe, geschenk): 
- quelle/liebt **Flamenco-Fächer** (faecher, geschenk): 
- quelle **Solar-Lichterkette** (lichterkette, geschenk): 
- quelle **Massageöl mit Neroli** (massage_oil, geschenk): 
- liebt **Seidenkimono** (silk_kimono, geschenk): 
- quelle **Massagekerze mit Wärmeöl** (massage_candle, geschenk): 
- liebt **Halterlose Strümpfe mit Spitzenrand** (stockings, geschenk): 
- quelle/liebt **Dessous mit Rüschen** (flamenco_dessous, geschenk): Rot und schwarz, aus Alvas eigenem Laden unter der Theke.
- unikat **Die Kastagnetten ihrer Großmutter** (alva_kastagnetten, einzigartig): Von Petru repariert. Kette: Alva + Petru.
- erwähnt **Figur des San Gennaro aus Neapel** (toto_gennaro, einzigartig): Kette: der Cousin aus Bastia + Alva.
- quelle **Multitool** (multitool, gluecksbringer): 
- quelle **Fernglas** (binoculars, gluecksbringer): 
- erwähnt **Glücksmünze von Alva** (lucky_coin, gluecksbringer): 
- quelle **Tarotkarten** (tarot, gluecksbringer): 
- quelle **Kanister Diesel** (diesel_canister, ressource): Bei Alva höchstens ein Kanister am Tag und teurer als bei Totò.
- quelle **Paneel-Reiniger** (panel_cleaner, ressource): 
- quelle **Doppelter Espresso** (espresso, ressource): 
- quelle **Kühlakkus aus dem Dorf** (kuehlakkus, ressource): Die Vorräte halten einen Tag länger, wenn der Strom knapp ist.
- quelle **Kanister Trinkwasser** (trinkwasser, ressource): 
- erwähnt **Kompressor-Relais** (relais, teil): 
- quelle **Ein altes Eichenbrett** (eichenbrett, teil): 
- quelle **Ein Sack Tonerde** (tonerde, teil): 
- quelle **Knopfzelle** (uhrenbatterie, teil): 
- quelle **Goldfarbe und ein feiner Pinsel** (goldfarbe, teil): 
- quelle **Echter Safran** (safran, teil): 
- quelle **Buchbinder-Leinen** (buchbinde_leinen, teil): 
- quelle **Rolle Netzgarn** (netzgarn, teil): 
- quelle **Ein schlichter Bilderrahmen** (bilderrahmen, teil): 
- quelle **Japanisches Kochmesser** (kochmesser, werkzeug): Vorteil bei Koch-Aufträgen (oder +2, wenn deine Küche schon Vorteil gibt).
- quelle **Verbandskasten** (verbandskasten, kampf): Heilt im Kampf 12 Lebenspunkte. Einmal benutzbar.
- erwähnt **Kiste Limoncello ohne Steuerbanderole** (limoncello_kiste, schmuggel): 
- liebt **Pavlova mit Feigen und Myrte** (pavlova, snack): 
- hasst **Rote Grütze mit Vanillesauce** (rote_gruetze, snack): 
- liebt **Mango-Chili-Sorbet** (mango_sorbet, snack): 
- liebt **Chili Noodles** (chili_noodles, gericht): Zu scharf für eine seekranke Flottenmanagerin.
- haltung: {"essen": "0", "alkohol": "+", "schmuck": "+", "technik": "-", "papier": "0", "natur": "0", "party": "+", "intim": "+"}

## Prompt Studio

- **base_prompt:** "{tags_action}, full body shot from head to knees, solo, one single woman alone in the frame, her whole body in full view, head and knees inside the frame,\nSubject: Alva Santoni, a curvy 35-year-old Corsican bar owner, big dark curly hair piled up loosely with a pencil stuck in it, dark eyes with black winged eyeliner, warm olive skin, gold hoop earrings, a knowing crooked grin,\nWearing: {outfi…
- **sprite_prompt:** "{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to knees, direct gaze, one single woman alone in the frame, her whole body in full view, head and knees inside the frame,\nSubject: 1girl with green eyes,\nBody: {tags_body}, \nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\nSkin: {tags_skin}, \nMakeup: {tags_face}\nWearing: …
- **fashion_prompt:** "{tags_action}, front view, full body shot from head to knees, standing in full view, beige plain background,\nSubject: Alva Santoni, a curvy 35-year-old Corsican bar owner, big dark curly hair piled up loosely with a pencil stuck in it, dark eyes with black winged eyeliner, warm olive skin, gold hoop earrings, a knowing crooked grin,\nWearing: {outfit},\nPose: {pose},\n{st},\n{tags_photo}"
- **loras:** [{"name": "Krea_Real3.safetensors", "strength": 0.8}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7}, {"name": "Krea_Redux.safetensors", "strength": 0.5}, {"name": "Krea_Azul.safetensors", "strength": 0.8}]
- **st_set:** "Yacht_Alva/Nude/roh"
- **sv_sets:** ["X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Alva\\Standard\\Sorted", "X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Alva\\Nude\\Sorted"]
- **Kostüm-Presets:** Flamenco Noche, Flamenco Rojo, Nude, Set2, Standard

## Stimme

- Stimme (eden-config): Alva Santoni

## Builder basis_eden_rise.py

- basis:126 `"hinweise": ["Alva greets Sophia by name", "a call from Paris that Sophia takes outside",`
- basis:351 `"lucky_coin": {"label": "Glücksmünze von Alva", "art": "gluecksbringer", "preis": 120, "wo": ["dorf"],`
- basis:403 `"alvas_bar": R("Alva's bar (ashore)", "corsican_village_bar.png", privat=2),`
- basis:481 `"alva": {"name": "Alva Santoni", "stimme": "Alva Santoni", "kurz": "Alva", "romanzierbar": False,`
- basis:512 `"alvas_bar": S("abend", "Alva's bar", ["sophia", "lea"], "alvas_bar",`
- basis:513 `"Evening in the village bar. Alva knows things, and sells diesel under the counter to people she likes.",`
- basis:714 `"alva": {`
- basis:717 `["curiosity", "You look like a man with free hands. Alva needs free hands."]],`
- basis:720 `["gratitude", "Grazie, o figliolu. Alva remembers who helps her."],`

## Docs (ohne VERDECKT)

- docs\archiv\BRAIN_TRUST_UEBERGABE.md:53 **Thema 4 · Romanzierbar: Crew + Lola + Alva (Duc bestätigt 22.10.)**
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:54 - Chiara, Sophia, Lea, Rosi, Siri + Lola + Alva = 7 Romanzen, je eine handgeschriebene Festa-Szene.
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:82 - Offen: Inhalte je Figur (Ziel + Bogen-Momente) für Chiara, Sophia, Lea, Rosi, Siri, Lola, Alva.
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:109 2 neue Romanzen (wie Lola/Alva). Idee muss noch besser werden.
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:170 eigentlich das Kommando wollte) · danach Sophia/Rosi, Lola + Alva, Bord-NPCs, Dorf (kurzer Check).
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:352 `docs/brain_trust/lola_jana_dossier.md` wird gesammelt) → **Alva + Casanova** (Dorf) → **Maxwell + Totò** (Bord-NPCs). Bisheriger Hinweis zu Rosi: **Rosi** (Dossier liegt schon in `docs/brain_trust/sophia_rosi_dossier.m…
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:355 Crafting; rotes Licht im Maschinenraum = ihr Revier). Danach Lola + Alva, Bord-NPCs
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:360 3. **Neue NPCs** (Duc will mehr): Schauspielerin an Bord; je Akt neue Romanzen wie Lola/Alva; Gegengewicht-Figur mit
- docs\wiki\systeme\kampf.md:68 `verbandskasten` (Art `kampf`, Totò/Alva, 60 €): heilt 12. Snacks heilen 6 (mit Küche 10). Andere Gegenstände
- docs\wiki\systeme\kampf.md:256 | Plüsch-Koala | Alva | Snacks heilen +2 |
- docs\wiki\systeme\tage_erkundung.md:68 - 21.10.2026: **genau 1 Lieblingsessen pro Person** (Lola: Bao Buns, Petru: Fish Pie, Alva behält Chili Noodles,
- docs\wiki\systeme\tage_erkundung.md:71 - **Angeln** als Minispiel: Boot, Strand, Fluss, See. Zutaten: einfache bei Totò und Alva kaufen, Rest sammeln,
- docs\brain_trust\alva_casanova_dossier.md:1 # Dossier Paar 7: Alva Santoni + Madame Casanova (die Frauen des Dorfes)
- docs\brain_trust\alva_casanova_dossier.md:5 ## 1. Alva Santoni
- docs\brain_trust\alva_casanova_dossier.md:11 | Persönlichkeit | weiß alles im Dorf, flirtet mit allen und meint es mit keinem, nennt jeden „o figliolu“; Hand-aufhalten-Typ („Alva remembers who helps her“); zahlt nie für Geschenke an Totò | MJ, basis:714-720, Missi…
- docs\brain_trust\alva_casanova_dossier.md:12 | Stimme | Stimme „Alva Santoni“ vorhanden (eden-config); Reaktion auf Geschenke: Ruf, Dorf erfährt es morgen | MJ, Stimme |
- docs\brain_trust\alva_casanova_dossier.md:29 | Beziehungen | Duc (gewinnt Vertrauen, Ehrenbürger-Plan); Chiara (Gangway-Streit); Alva (VIP-Lounge-Streit, spricht seit „Dorfladen-Streit“ nicht mehr mit ihr); Elsa (Geschenk-Kette); Alon (Hass); Lea (Graveur-Kontakt)…
- docs\brain_trust\alva_casanova_dossier.md:36 - Event gv_casanova_alva: Casanova will Alvas Bar zur Festa-VIP-Lounge mit Samtseil, Alva will sie „laut, voll, für alle“ lassen.
- docs\brain_trust\alva_casanova_dossier.md:38 - Alva verkauft genau Casanovas Lieblingsgeschenke (Herzbrille, Konfetti, Schärpe) und das Buchbinder-Leinen für Casanovas Elsa-Geschenk.
- docs\brain_trust\alva_casanova_dossier.md:45 3. Casanovas Elsa-Geschenk-Kette zwingt Duc, zwischen beiden zu vermitteln; Leinen von Alva als Versöhnungsgeste.
- docs\brain_trust\alva_casanova_dossier.md:47 5. Elternhaus (Casanova), Vaterbar (Alva), Papas Werkstatt (Rosi/Petru): gemeinsamer Verlust-Faden „was Alon einzäunt“ (ÜB:301).
- docs\brain_trust\alva_casanova_dossier.md:51 1. **Romanzierbar:** MJ führt Alva mit `romanzierbar: false`, ÜB Thema 4 (22.10.) macht sie zur Romanze Nr. 7. Engine stimmt nicht mit Entscheidung überein; auch Karte, Lebensziel, Bogen, Festa-Szene fehlen.
- docs\brain_trust\alva_casanova_dossier.md:54 4. **Sprite-Prompt Alva:** `base_prompt` beschreibt dunkle Augen und Lockenknoten, `sprite_prompt` sagt „1girl with green eyes“ und nur Tag-Platzhalter; PS-Sets nur Standard/Nude, Flamenco-Sets laut MJ ohne sv_sets-Eint…
- docs\brain_trust\alva_casanova_dossier.md:57 7. **7-Tage-Reste:** alle Events/Missionen laufen T2-7 oder T3-5; „Alva Tag 4 NSFW“ und Vertrauensschwellen hängen am 7-Tage-Takt. Auf 21 Tage und drei Akte neu verteilen.
- docs\brain_trust\alva_casanova_dossier.md:58 8. **Lücke Prämisse:** keine Bindung beider an Bucht-Verkauf/Alon in der Engine; Casanova ist nur über Bucht-Ende 2 eingebunden, Alva gar nicht.
- docs\brain_trust\alva_casanova_dossier.md:63 13. **Doppelte Alva-Abende:** hy_alva_nach_feierabend und ab_alva_barabend (beide rotes Rüschen-Outfit) sowie ab_alva_handy sind sehr ähnlich; mit Vertrauen-Stufen und Festa-Szene abgleichen.
- docs\brain_trust\holm_chiara_dossier.md:59 | Beziehungen | **Duc**: „eine Sieben, vielleicht Acht“, ärgert sich, dass er Astronavigation kann. **Holm**: Vorbild/Chefin, ungelesene Unterschrift = „Medaille“ (LB 43). **Sophia**: beste Freundin + Rivalin (Strichlis…
- docs\brain_trust\lola_jana_dossier.md:61 | Vorlieben / Geschenke | Grundhaltung: **Essen +, Alkohol +, Schmuck 0, Technik –, Papier 0, Natur +, Party +, Intim +** (geg_py:31). **Liebt** (Geschenkwert 2): Tim Tams (Alvas Bar, „Lola weint ein bisschen“), Alvas R…
- docs\brain_trust\lola_jana_dossier.md:64 | Beziehungen | **Duc**: mochte ihn ab dem ersten leeren Teller, stellt ihm wortlos Essen hin, wenn er Mahlzeiten auslässt (lola.txt:9); Kombüse als Hitze-Stufe 2, Kabinentür auf Stufe 4 (lola.txt:81). **Holm**: tut so,…
- docs\brain_trust\lola_jana_dossier.md:91 | Beziehungen | **Duc**: „Sir“; allein kaum ein Wort, in der Gruppe neckt sie ihn und wartet, was er tut (jana.txt:9). **Lea**: **beste Freundin**, die zwei Tollpatschigsten an Deck; zusammen zwei Fender, einen Mopp und…
- docs\brain_trust\lola_jana_dossier.md:199 Prüfer erlaubt Begehren für „Frauen/Lola/Alva“ (ebasis_py:324–325).
- docs\brain_trust\lola_jana_dossier.md:234 - `lola_paella_1–2` T2–7: Paella für die Crew, Safran von Alva, „damit nach der Woche alle wieder an einem Tisch sitzen“
- docs\brain_trust\lola_jana_dossier.md:238 `bauchnabelpiercing` (aus hy_lola_tresen / Alva) · `energieriegel` (Laden ab V3) · `frischer_fang` („Lola macht daraus ein
- docs\brain_trust\lola_jana_dossier.md:280 | hy_lola_tresen | T2–7 Nacht, V Alva ≥2 | Alva ruft an, Lola tanzt barfuß auf dem Tresen; Tender / Rechnung (→ Piercing) / Chiara anrufen |
- docs\brain_trust\lola_jana_dossier.md:289 | gv_arancini_duell | T3–6 Abend, an Land | Lola vs. Alva, Duc Jury |
- docs\brain_trust\lola_jana_dossier.md:389 - Memory-Design „Lola Tag 3 / Alva Tag 4“ beruht auf dem 7-Tage-Takt.
- docs\brain_trust\lola_jana_dossier.md:401 - **Dorf-Fäden vorhanden**: Petru (Töpferscheibe, Fiona, Bastianu, Thunfisch), Alva (Tresen, Arancini-Duell, Kastagnetten,
- docs\brain_trust\sophia_rosi_dossier.md:52 | Beziehungen | **Duc**: erster Mensch, an dem ihr Charme abgleitet; Wetten; er hat ein Kapitel. **Lea**: kleine Schwester, siehe Abschnitt 3. **Chiara**: beste Freundin + Rivalin, Strichliste am Kühlschrank (wer mehr G…
- docs\brain_trust\sophia_rosi_dossier.md:76 | Beziehungen | **Duc**: „offizieller Rivale“ seit er in Woche 1 die Tender-Winde allein reparierte; Spalte „Reparaturen: Rosi vs Officer“. **Chiara**: nennt sie „Mole/Maulwurf“ (taucht nur zum Essen auf), will sie auf …
- docs\brain_trust\sophia_rosi_dossier.md:127 - **Totes Storylet:** `alvas_bar` (Abend, Sophia + Lea, ab Tag 2: „Evening in the village bar. Alva knows things, and
- docs\brain_trust\sophia_rosi_dossier.md:295 | gv_strip_poker | T4–7 Abend, an Land, V Alva ≥3 | Poker gegen Alva um einen Kanister, Sophia fehlt die Bluse |
- docs\brain_trust\toto_maxwell_dossier.md:15 | Beziehungen | Duc („Comandante“, Draht 0-5, Start 1); Jana (Chef); Lea (angeln, Qualle, Tender); Rosi (Armdrücken, Wett-Streit); Elsa (Gegenspielerin, wird gejagt); Megan (ihre Drohne jagt ihn); Alva (Gennaro-Kette, D…
- docs\brain_trust\toto_maxwell_dossier.md:17 | Engine-Stand | ~58 Events (Hauptrolle: g1_toto_pizza, g1_fiona_muetze, g1_cousin_schlauchboot, hy_cousin_falsch, hy_toto_spind, du_koch_toto), 5 eigene Missionen (gefallen, box, night, tabak, Kühlung) + Gennaro-Kette …
- docs\brain_trust\toto_maxwell_dossier.md:47 5. Totòs Händlerrolle liefert Maxwell Trainingsgerät und Proteinriegel; Gennaro-Kette (Alva) kann Maxwell als Zeugen/Träger einbinden.
- docs\brain_trust\toto_maxwell_dossier.md:62 12. **Doppelte Konkurrenz:** Alva und Totò verkaufen Diesel, Verbandskasten, Tauchlampe, Limoncello-Kiste (Alva teurer, max. 1/Tag); sinnvoll als Rivalität, aber Wirkung nicht definiert.

## VERDECKT – Fall-Bezüge (nie im Chat zitieren)

- **Fall 1**
  - h_13 [Quelle/weiß/betrifft/Weg, aussage]: Alva: "Sophia? Kenne ich nicht. Bei mir hat keiner von euch reserviert."
- **Fall 2**
  - h_13 [Quelle/weiß/betrifft/Weg, aussage]: Alva: "Sophia? Kenne ich nicht. Bei mir hat keiner von euch reserviert."
- **Fall 3**
  - f3_07 [weiß/Weg, belastbar]: Alvas Reservierungsbuch: "Tag 2, 07:30, 2 Pers., Sophia - tel. T-4".
  - f3_08 [weiß/Weg, belastbar]: Notiz bei Alva für Sophia (T2 08:15): "Musste los. Schreiben Sie mir. H. M." - Alva: Eine Französin, Frau Marchal, hat eine Stunde gewartet.
  - schickt die Nachricht kurz vor Morgen (Tag 3)
- **Fall 4**
  - h_13 [Quelle/weiß/betrifft/Weg, aussage]: Alva: "Sophia? Kenne ich nicht. Bei mir hat keiner von euch reserviert."
- **Fall 5**
  - h_13 [Quelle/weiß/betrifft/Weg, aussage]: Alva: "Sophia? Kenne ich nicht. Bei mir hat keiner von euch reserviert."
- **Fall 6**
  - h_13 [Quelle/weiß/betrifft/Weg, aussage]: Alva: "Sophia? Kenne ich nicht. Bei mir hat keiner von euch reserviert."

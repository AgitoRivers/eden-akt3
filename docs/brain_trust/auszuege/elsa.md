# Auszug: Elsa

Automatisch erzeugt von werkzeuge/figur_auszug.py. Fall-Bezüge stehen nur im letzten Abschnitt VERDECKT (Duc liest diese Dateien nicht; im Chat nie Inhalte daraus nennen).

## Engine (modul.json)

```json
{
 "name": "Elsa Ferrandi",
 "stimme": "Elsa Ferrandi",
 "kurz": "Elsa",
 "romanzierbar": false,
 "beschreibung": "lieutenant of the maritime gendarmerie, 29, Corsican, runs the small coast-guard post at the harbour of Cala d'Orsu and a fast patrol boat; dry humour, sharp eyes, never breaks a rule but loves bending one; coordinates salvage and towing with Ajaccio; hunts smugglers and has had her eye on Toto since the day the yacht arrived; money offered to her is an insult, respect and competence are not",
 "ablauf": {
  "*": "village_harbour"
 },
 "bestechung": {
  "ab": 50,
  "regie": "Duc offers her something valuable: %s. That looks like a bribe to a gendarme. She refuses it - sharp or drily amused - hands it back and makes a note of it."
 },
 "geschenk_reaktion": [
  null,
  "Elsa accepts the small gift with a dry remark and puts it away, a little amused."
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
| br_elsas_kontrolle | bordrat | T2–6 nacht | erwähnt | Elsa kommt morgen – Leutnantin Ferrandi hat sich für morgen zur Kontrolle angemeldet. Totò wird blass und guckt in Richtung Lagerraum. Chiara sieht es. |
| br_nacktbaden | bordrat | T2–6 nacht | erwähnt | Nacktbaden mit Folgen – Lea und Siri waren heute Nacht nackt baden. Elsas Patrouillenboot fuhr genau in dem Moment vorbei. Mit Scheinwerfer. |
| hy_elsa_vorwarnung | handy | T3–6 abend/nacht | anrufer | Elsas Vorwarnung – Elsa ruft vom Hafen aus an. Sie redet leise. Morgen früh gibt es eine Razzia wegen Schmuggel in der Bucht. Sie sagt das nicht als Polizistin. |
| hy_elsa_segler | handy | T2–6 tag | anrufer | Ein treibendes Segelboot – Elsa braucht Hilfe. Ein kleines Segelboot treibt vor der Bucht, zwei Touristen an Bord, der Motor ist aus. Ihr Patrouillenboot ist zu weit weg. |
| hy_cousin_falsch | handy | T2–6 nacht | erwähnt | Falsch verbunden aus Bastia – Eine Nachricht von einer unbekannten Nummer: „Gennaro hier. Paket kommt heute Nacht. Sag Salvatore: Die Ziege ist auch dabei.“ Totò ist Salvatore. Totò liest m… |
| g1_elsa_schwimmwesten | gag1 | T2–6 tag | handelnd | Elsa und die Schwimmwesten – Elsas Patrouillenboot legt an. Totò und Lea sind gerade mit dem Tender unterwegs. Ohne Schwimmwesten. Elsa hält ihren Strafzettelblock in der Hand und lächelt … |
| g1_cousin_schlauchboot | gag1 | T3–6 nacht | betroffen | Der Cousin kommt nachts – Totòs Cousin legt nachts mit einem Schlauchboot an. Ohne Licht. Er lädt Kisten aus. Am Ufer blitzt etwas auf. Elsas Fernglas. |
| gv_toto_elsa | gagv | T3–6 tag | rechts | Totò verteidigt seinen Spind – Elsa will in Totòs Spind schauen. Totò steht davor, die Arme ausgebreitet, wie ein Torwart beim Elfmeter. |
| gv_casanova_alva | gagv | T3–5 tag | zuschauer | Die VIP-Lounge – Madame Casanova will Alvas Bar für die Festa zur VIP-Lounge machen. Mit Samtseil. Alva will ihre Bar so lassen, wie sie ist: laut, voll und für alle. |
| gv_elsa_alva | gagv | T3–6 tag | links | Diesel unter dem Tresen – Elsa sitzt an Alvas Tresen und trinkt einen Espresso. Unter dem Tresen stehen vier Dieselkanister. Jeder weiß es. Elsa schaut Alva lange an. |
| g1_casanova_nebel | gag1 | T3–5 tag | betroffen | Die Generalprobe – Madame Casanova probt ihren Auftritt für die Festa. Im Flamenco-Kleid, auf einem Fischkutter, mit einer gemieteten Nebelmaschine. Der Nebel ist dichter als gep… |
| gv_elsa_kiste | gagv | T3–7 tag/abend | links | Kartoffeln, die miauen – Elsa hat eine von Totòs Kisten am Kai aufgehalten. Auf der Kiste steht „Kartoffeln“. Die Kiste miaut. Totò behauptet, es seien sehr junge Kartoffeln. Elsa hat … |

## Missionen

- **toto_gefallen** (von toto, T3–7, cunning SG 13): Totòs kleine Kiste – „Erinnerst du dich an das Relais? Ich hätte da eine kleine Kiste, die heute Nacht an Elsas Boot vorbei muss.“
- **radio_elsa** (von elsa, T2–6, cunning SG 11): Funkgerät im Küstenwache-Posten – Elsas Funkgerät nach Ajaccio rauscht. Ohne Funk keine Bergung – sie zahlt bar und hasst es, fragen zu müssen.
- **toto_box** (von toto, T2–6, cunning SG 13): Eine Kiste für Totò umladen – „Nicht reinschauen, Comandante. Einfach vom Beiboot in den Lagerraum. Und wenn die Leutnantin fragt: Kartoffeln.“
- **elsa_fund_1** (von elsa, T2–7, charm SG 13): Ein Fundstück für Lea – In Elsas Fundsachenkiste liegt seit einem Jahr ein Tauchcomputer. Niemand hat ihn abgeholt. Elsa hat gesehen, wie Lea ohne einen taucht, und das macht ihr Sorgen. Herausgeben darf sie ihn nur mit ein…
- **elsa_fund_2** (von elsa, T2–7, None SG None): Ein Fundstück für Lea: die Batterie – Der Tauchcomputer ist tot. Elsa öffnet ihn mit einem winzigen Schraubenzieher aus ihrer Dienstweste. Die passende Knopfzelle hat sie nicht. Im Dorf gibt es so etwas nur bei Alva.
- **elsa_fund_3** (von elsa, T2–7, None SG None): Ein Fundstück für Lea: das Armband – Das alte Armband ist im Salzwasser zerfallen. Ein seefestes bekommt man nur über die Ausrüstung der Reederei.
- **casanova_elsa_1** (von casanova, T2–7, perception SG 12): Ein Geschenk für die Leutnantin: das Archiv – Elsa ist seit zehn Jahren auf dem Posten von Cala d'Orsu. Das Dorf will ihr danken, aber sie nimmt nichts an. Alles wäre Bestechung. Madame Casanova hat eine Idee: Elsas eigene Strafzettel aus zehn J…
- **siri_lakritz** (von siri, T3–7, empathy SG 11): Salzlakritz für Holm – Siri hat eine Tüte schwedische Salzlakritz in ihrem Koffer. Holm liebt das Zeug, das weiß die ganze Crew. Siri traut sich nicht, sie der Kapitänin ins Krankenhaus zu schicken, mit der sie in drei Woc…
- **elsa_antenne_1** (von elsa, T3–7, None SG None): Elsas Antenne: das Kabel – Seit dem letzten Sturm reicht Elsas Funk nicht mehr bis Ajaccio. Das alte Antennenkabel ist durchgescheuert. Ein neues hat die Gendarmerie beantragt, vor elf Monaten. Die Reederei hat welches, und El…
- **elsa_antenne_2** (von elsa, T3–7, courage SG 12): Elsas Antenne: aufs Dach – Die Antenne sitzt auf dem Dach des Postens, vier Meter über dem Hafen. Wind aus Nordwest, Böen. Elsa hält die Leiter und sagt, sie würde selbst hochsteigen, wenn sie dürfte.
- **elsa_nachtessen** (von elsa, T3–7, perception SG 12): Essen für die Nachtpatrouille – Elsa und ihre zwei Leute fahren seit dem Ausfall jede Nacht Patrouille und essen kalte Dosen auf dem Boot. Geld oder Geschenke nimmt sie nicht. Ein warmes Essen für die Mannschaft ist aber Verpflegun…

## Gegenstände / Essen

- liebt **Korsische Feigen** (feigen, geschenk): 
- hasst **Myrtenlikör** (myrtle, geschenk): 
- liebt **Tauchlampe** (dive_torch, geschenk): 
- liebt **Polarisierte Sonnenbrille** (polbrille, geschenk): 
- hasst **Herrenmagazin mit Pin-up** (pinup_magazin, geschenk): Italienisches Magazin, auf dem Titel eine schöne, halbnackte Frau. Totò liest es „wegen der Artikel“.
- hasst **Glitzer-Schärpe „Miss Cala d'Orsu“** (schaerpe, geschenk): 
- erwähnt **Tauchcomputer** (lea_tauchcomputer, einzigartig): Für ihre eigenen Pläne, sicher geplant. Kette: Elsa + Totò.
- erwähnt **Eine Dose norwegischer Salzlakritz** (holm_lakritz, einzigartig): Bring-mir-Auftrag: Elsa bringt sie ins Krankenhaus.
- unikat **Strafzettelblock, in Leder gebunden** (elsa_strafzettelblock, einzigartig): Mit ihren Initialen. Sie lacht zum ersten Mal laut.
- hasst **Ocean-Glitter-Popcorn** (ocean_popcorn, snack): 
- liebt **Ghost-Pepper-Brownies** (ghost_brownies, snack): 
- hasst **Space Cake „Universe Edition“** (space_cake, snack): 
- liebt **Baguettes** (baguettes, gericht): Brot ist die schwerste Disziplin.
- haltung: {"essen": "+", "alkohol": "-", "schmuck": "0", "technik": "+", "papier": "0", "natur": "0", "party": "-", "intim": "-"}

## Prompt Studio

- **base_prompt:** "{tags_action}, full body shot from head to knees, solo, one single woman alone in the frame, her whole body in full view, head and knees inside the frame,\nSubject: Elsa Ferrandi, a 29-year-old Corsican woman, lieutenant of the maritime gendarmerie, athletic and toned, sun-kissed olive skin, dark brown hair pulled into a tight low bun with a few loose strands, sharp hazel eyes, a thin scar throu…
- **sprite_prompt:** "{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to knees, direct gaze, one single woman alone in the frame, her whole body in full view, head and knees inside the frame,\nSubject: 1girl, blue eyes,\nBody: {tags_body}, \nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\nSkin: {tags_skin}, \nMakeup: {tags_face}\nWearing: {outf…
- **fashion_prompt:** "{tags_action}, front view, full body shot from head to knees, standing in full view, beige plain background,\nSubject: Elsa Ferrandi, a 29-year-old Corsican woman, lieutenant of the maritime gendarmerie, athletic and toned, sun-kissed olive skin, dark brown hair pulled into a tight low bun with a few loose strands, sharp hazel eyes, a thin scar through her left eyebrow, a dry confident half-smil…
- **loras:** [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7}, {"name": "Krea_Redux.safetensors", "strength": 0.5}]
- **st_set:** "Yacht_Elsa/Domina/roh"
- **sv_sets:** ["X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Elsa\\Standard\\Sorted", "X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Elsa\\Jumpsuit\\Sorted", "X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Elsa\\Domina\\Sorted"]
- **Kostüm-Presets:** Domina, Jumpsuit, Standard

## Stimme

- Stimme (eden-config): Elsa Ferrandi

## Builder basis_eden_rise.py

- basis:169 `MODUL["schmuggel_risiko"] = 0.2 # je Tagesende und Schmuggelware im Inventar: Elsa (Kuestenwache) findet sie`
- basis:474 `"elsa": {"name": "Elsa Ferrandi", "stimme": "Elsa Ferrandi", "kurz": "Elsa", "romanzierbar": False,`
- basis:698 `"elsa": {`

## Docs (ohne VERDECKT)

- docs\archiv\BRAIN_TRUST_UEBERGABE.md:395 Margot zurück) · **Stärke** (Endkampf Akt 3 gewonnen oder Festsetzen mit Elsa/Küstenwache). Sichtbar auf Casanovas
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:403 Handschellen** (W+Stärke; Elsa führt ab, „Freedom is just chaos with good PR“, neuer Käufer-Hubschrauber; Andeutung:
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:431 - **Totò = der schmuddelige Onkel, vor dem alle gewarnt haben** (Neapel, Straßenwitz, Schweißtropfen bei Elsa, „von
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:464 verloren = stellt sich, Postkarte aus der Haft · Verrat + Alon besiegt = Elsa verhaftet ihn auf Alons Boot, im Spind
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:548 (Totò, Elsa, Maxwell, Unit-01, Kevin die Möwe), Dorf (nur kurzer Check, Ortsdrehbuch ist frisch). Je Paar: Dossier per
- docs\wiki\systeme\kampf.md:202 | Elsas Taser | 1 | Luft | Gewöhnlich | Stumpf | Geschenk Elsa (Vertrauen 2) | – |
- docs\wiki\systeme\kampf.md:257 | Plüsch-Schäferhund | Elsa | Einschüchtern mit Vorteil |
- docs\brain_trust\alva_casanova_dossier.md:15 | Beziehungen | Duc (flirtet, Events ab Vertrauen 2/3/4); Lola (Tresen-Tanz, Arancini-Duell, Kastagnetten); Totò (Gennaro-Kette, Dieselkonkurrenz); Elsa (duldet nicht, schaut); Petru (repariert Kastagnetten); Chiara (Ei…
- docs\brain_trust\alva_casanova_dossier.md:29 | Beziehungen | Duc (gewinnt Vertrauen, Ehrenbürger-Plan); Chiara (Gangway-Streit); Alva (VIP-Lounge-Streit, spricht seit „Dorfladen-Streit“ nicht mehr mit ihr); Elsa (Geschenk-Kette); Alon (Hass); Lea (Graveur-Kontakt)…
- docs\brain_trust\alva_casanova_dossier.md:31 | Engine-Stand | 14 Events (Bordrat 3, Handy 2, Gag 7, Abend 1 Flamenco), 8 Missionen (plan, english_kids, banner, buffet, 3x Elsa-Geschenk, Füller-Graveur), Unikat Konfettikanone, Sprites Standard/Flamenco. Es fehlen: …
- docs\brain_trust\alva_casanova_dossier.md:38 - Alva verkauft genau Casanovas Lieblingsgeschenke (Herzbrille, Konfetti, Schärpe) und das Buchbinder-Leinen für Casanovas Elsa-Geschenk.
- docs\brain_trust\alva_casanova_dossier.md:45 3. Casanovas Elsa-Geschenk-Kette zwingt Duc, zwischen beiden zu vermitteln; Leinen von Alva als Versöhnungsgeste.
- docs\brain_trust\holm_chiara_dossier.md:106 Krankenhaus zu schicken; Elsa bringt sie nach Ajaccio; Holm antwortet „Tack.“ → Vertrauen.holm +8 (missionen_eden_rise.py:359).
- docs\brain_trust\lea_dossier.md:15 Elsa (Sorge wegen Tauchen ohne Computer).
- docs\brain_trust\lola_jana_dossier.md:64 | Beziehungen | **Duc**: mochte ihn ab dem ersten leeren Teller, stellt ihm wortlos Essen hin, wenn er Mahlzeiten auslässt (lola.txt:9); Kombüse als Hitze-Stufe 2, Kabinentür auf Stufe 4 (lola.txt:81). **Holm**: tut so,…
- docs\brain_trust\lola_jana_dossier.md:91 | Beziehungen | **Duc**: „Sir“; allein kaum ein Wort, in der Gruppe neckt sie ihn und wartet, was er tut (jana.txt:9). **Lea**: **beste Freundin**, die zwei Tollpatschigsten an Deck; zusammen zwei Fender, einen Mopp und…
- docs\brain_trust\megan_alon_dossier.md:121 - **Endfassung Tag 7 durch Elsa** (bestätigen/korrigieren; Schäden verschwinden nicht).
- docs\brain_trust\megan_alon_dossier.md:197 6. **7-Tage-Reste:** „Calvi within the week“, Bericht Tag 6, Endfassung Tag 7 durch Elsa, Besuch T4–T7, Story-Prüfer erzwingt diese Fenster (story_pruefen.py:444). Neu: Ultimatum T2, Hubschrauber T5, **Anhörung T7 mit M…
- docs\brain_trust\siri_yasin_dossier.md:97 - `siri_lakritz` „Salzlakritz für Holm“ (T3–7, Empathie 11): über Elsa nach Ajaccio; Holm +8; Antwort „Tack.“
- docs\brain_trust\sophia_rosi_dossier.md:52 | Beziehungen | **Duc**: erster Mensch, an dem ihr Charme abgleitet; Wetten; er hat ein Kapitel. **Lea**: kleine Schwester, siehe Abschnitt 3. **Chiara**: beste Freundin + Rivalin, Strichliste am Kühlschrank (wer mehr G…
- docs\brain_trust\sophia_rosi_dossier.md:76 | Beziehungen | **Duc**: „offizieller Rivale“ seit er in Woche 1 die Tender-Winde allein reparierte; Spalte „Reparaturen: Rosi vs Officer“. **Chiara**: nennt sie „Mole/Maulwurf“ (taucht nur zum Essen auf), will sie auf …
- docs\brain_trust\toto_maxwell_dossier.md:15 | Beziehungen | Duc („Comandante“, Draht 0-5, Start 1); Jana (Chef); Lea (angeln, Qualle, Tender); Rosi (Armdrücken, Wett-Streit); Elsa (Gegenspielerin, wird gejagt); Megan (ihre Drohne jagt ihn); Alva (Gennaro-Kette, D…
- docs\brain_trust\toto_maxwell_dossier.md:46 4. Hubschrauber-Tag 5 (Megan landet) trifft Maxwells Flugangst und Totòs Elsa-/Drohnen-Druck: gleicher Tag, zwei Reaktionen.
- docs\brain_trust\toto_maxwell_dossier.md:60 10. **Prämisse-Passung Totò:** br_crew_kasse (Eden-Group-Eigentum verkaufen) und Razzia/Elsa passen zur Eden-Group-Verwicklung, aber keine Bindung an Bucht, Alon oder Festa; seine Fall-Rolle ist nicht geprüft (Spoilersc…

## VERDECKT – Fall-Bezüge (nie im Chat zitieren)

- **Fall 6**
  - f6_07 [Weg, gesichert]: Unabhängige Prüfung (Rosi misst nach den Herstellerunterlagen, Petru dokumentiert): thermische Vorschädigung von LM3, Ausfall ohne äußeren Auslöser.
- Zweite Wahrheit z_01: Herstellermeldung an die Eden Group (T-12): Leistungsmodule PX-480, Charge 22-B – thermische Vorschädigung möglich; Rückfallprofil R2 für diesen Typ nicht verwenden; Prüfung vor Weiterbetrieb.
- Zweite Wahrheit z_02: Vorläufige Weiterbetriebsentscheidung (T-9): "Weiterbetrieb bis Werftaufenthalt Calvi, Prüfung und R2-Sperre dort." Administrativ mitgezeichnet: M. (Megan). Die technische Prüfung wurde nicht sicherg…

# Auszug: Petru

Automatisch erzeugt von werkzeuge/figur_auszug.py. Fall-Bezüge stehen nur im letzten Abschnitt VERDECKT (Duc liest diese Dateien nicht; im Chat nie Inhalte daraus nennen).

## Engine (modul.json)

```json
{
 "name": "Petru Albertini",
 "stimme": "Petru Albertini",
 "kurz": "Petru",
 "romanzierbar": false,
 "beschreibung": "old fisherman, seventies, with his own boat workshop; speaks little, repairs everything, has heard every legend of the coast",
 "ablauf": {
  "*": "petru_workshop"
 },
 "pronomen": "er",
 "geschenk_reaktion": [
  "ruf",
  "Petru turns it over in his hands, says almost nothing, and nods once. For him that is a lot."
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
| br_petrus_boot | bordrat | T2–5 nacht | erwähnt | Petrus Morgenfang – Petru nimmt morgen früh zwei Leute mit zum Fischen. Wer mitfährt, ist bis Mittag weg. Lea hat schon ihre Stiefel an. |
| br_netze_flicken | bordrat | T2–6 nacht | erwähnt | Petrus Preis – Petru nimmt kein Geld für seinen Fisch. Er will etwas anderes: Morgen früh sollen zwei von der Crew seine Netze flicken. Drei Stunden, in der Sonne, mit einem … |
| hy_casanova_einladung | handy | T3–5 tag | erwähnt | Die Einladung zur Festa – Casanova hält eine Karte mit rotem Wachssiegel in die Kamera. Eine persönliche Einladung zur Festa, nur für Duc und eine Begleitung seiner Wahl. |
| hy_lola_ziege | handy | T2–6 tag | erwähnt | Lola hat sich verlaufen – Lola ruft vom Land aus an. Sie sollte nur Zitronen kaufen. Jetzt steht sie in Petrus Werkstatt, mit einer Ziege an der Leine, und weiß nicht, wie das passiert … |
| g1_petru_fisch | gag1 | T2–6 fruehstueck/tag | handelnd | Petrus Thunfisch – Petru legt mit seinem Boot an und wirft wortlos einen Thunfisch an Deck. Einen großen. Dann zeigt er auf Duc und auf ein Messer. Er will, dass Duc ihn ausnimmt. |
| gv_arancini_duell | gagv | T3–6 abend | zuschauer | Das Arancini-Duell – Lola behauptet, ihre Arancini sind die besten des Mittelmeers. Alva hat dazu eine Meinung. Das ganze Dorf schaut zu. Duc ist Jury. |
| gv_aussenborder | gagv | T2–6 tag | links | Petru gegen Rosi – Der Außenborder des Tenders stottert. Petru will ihn mit einem Hammer und Gefühl reparieren. Rosi mit einem Messgerät und einem Laptop. Beide halten das jeweil… |
| gv_casanova_alva | gagv | T3–5 tag | zuschauer | Die VIP-Lounge – Madame Casanova will Alvas Bar für die Festa zur VIP-Lounge machen. Mit Samtseil. Alva will ihre Bar so lassen, wie sie ist: laut, voll und für alle. |
| gv_elsa_alva | gagv | T3–6 tag | zuschauer | Diesel unter dem Tresen – Elsa sitzt an Alvas Tresen und trinkt einen Espresso. Unter dem Tresen stehen vier Dieselkanister. Jeder weiß es. Elsa schaut Alva lange an. |
| du_koch_alva | duell | T3–7 abend | zuschauer | Koch-Showdown: Korsika gegen Saigon – Alva hat die Tische zusammengeschoben. Auf der einen Seite stehen ihr Fiadone und ihre Wildschwein-Pastete, auf der anderen deine Garküche aus zwei Gaskochern.… |
| du_tiere_lea | duell | T2–7 tag/abend | zuschauer | Tiere erraten – Lea hat ihr Bestimmungsbuch mit an Deck gebracht. Das Spiel: Sie beschreibt ein Meerestier, du musst es erraten. Dann umgekehrt. Siri führt Buch. Petru sitzt a… |
| g1_casanova_nebel | gag1 | T3–5 tag | betroffen | Die Generalprobe – Madame Casanova probt ihren Auftritt für die Festa. Im Flamenco-Kleid, auf einem Fischkutter, mit einer gemieteten Nebelmaschine. Der Nebel ist dichter als gep… |
| g1_petru_oktopus | gag1 | T3–7 fruehstueck/tag | betroffen | Petrus Untermieter – Petru hat beim Liefern einen Eimer an Bord vergessen. Im Eimer war ein Oktopus, den er seit Wochen füttert und „Bastianu“ nennt. Jetzt ist der Eimer leer. Lola… |

## Missionen

- **casanova_plan** (von casanova, T3–5, charm SG 12): Ein Nachhaltigkeitsplan für die Festa – Madame Casanova hat gehört, dass du Nachhaltigkeitsberater bist. Sie will die grünste Festa Korsikas. Mit Feuerwerk. Und Einweggrills. Und vierhundert Luftballons.
- **petru_motor_1** (von petru, T3–7, cunning SG 13): Petrus alter Bootsmotor – In Petrus Werkstatt steht ein Motor unter einer Plane. Ein Volvo Penta, älter als du. Er gehörte seinem Vater. Petru zieht die Plane weg und sagt nichts.
- **petru_motor_2** (von petru, T4–7, courage SG 12): Die erste Ausfahrt – Petru will den Motor auf dem Wasser hören. Im Boot seines Vaters, mit dir am Ruder, einmal um die Hafenmole.
- **nets** (von petru, T2–7, perception SG 10): Petrus Netze flicken – Petru zeigt auf einen Haufen Netze und sagt nichts. Das ist ein Angebot.
- **outboard** (von petru, T3–7, cunning SG 12): Außenborder eines Fischers – Petrus Nachbar hat einen Außenborder, der stottert. Petru hat dich empfohlen. Das ist neu.
- **petru_schild_1** (von petru, T3–7, None SG None): Ein Schild für Rosi: das Brett – Petru hat Rosi gestern vor seiner Werkstatt stehen sehen. Sie hat lange auf das leere Brett über seiner Tür geschaut und gesagt: „Scuderi & Figlie. So hätte Papa es genannt.“ Petru will ihr eines sch…
- **petru_schild_2** (von petru, T3–7, cunning SG 13): Ein Schild für Rosi: schnitzen – Petru zeichnet die Buchstaben mit Kreide vor, seine Hand zittert dabei. Die Feinarbeit soll jemand machen, dessen Hände noch ruhig sind.
- **petru_schild_3** (von petru, T3–7, None SG None): Ein Schild für Rosi: die Buchstaben – Messingbuchstaben bekommt man auf dieser Insel nur bei einem Mann, der nie fragt, wofür. Petru nennt ihn nicht beim Namen. Er schaut nur zur Yacht hinüber.
- **lola_tasse_2** (von lola, T2–7, None SG None): Eine Tasse für Chiara: der Ton – Petru hat eine alte Töpferscheibe und erlaubt Lola, sie zu benutzen, wenn sie ihren eigenen Ton mitbringt und nichts anfasst. Lola fasst immer alles an. Deshalb sollst du den Ton zu Petru bringen.
- **lola_tasse_3** (von lola, T2–7, perception SG 12): Eine Tasse für Chiara: drehen – Lola dreht, du hältst die Form, Petru schaut zu und sagt nichts. Der Rand muss gerade werden, sonst tropft es. Chiara hasst Tropfen.
- **lola_kast_2** (von lola, T3–7, None SG None): Alvas Kastagnetten: der Leim – Petru sagt, für altes Holz nimmt man Knochenleim, keinen modernen Kleber. Knochenleim hat auf dieser Insel nur jemand, der auch sonst alles hat.
- **lola_kast_3** (von lola, T3–7, cunning SG 13): Alvas Kastagnetten: leimen – Zwei Hälften, ein Haarriss, sechzig Jahre Flamenco. Petru erwärmt den Leim, du setzt die Teile zusammen. Verrutscht eines, klingen sie nie wieder.
- **siri_ratgeber_1** (von siri, T3–7, None SG None): Ein Buch für Siris Vater: das Netzgarn – Siris Vater fischt seit vierzig Jahren vor Göteborg. Petru erinnert sie so sehr an ihn, dass sie ihn kaum ansehen kann. Sie will seine Geschichten über die Fischerei auf Korsika aufschreiben, für ihr…
- **siri_ratgeber_2** (von siri, T3–7, empathy SG 13): Ein Buch für Siris Vater: das Gespräch – Petru erzählt, wenn man still ist. Siri ist nicht gut im Stillsein. Du sollst die Fragen stellen, so, dass Petru nicht merkt, dass es ein Interview ist, und so, dass es ihn nicht nervt.
- **toto_tabak** (von toto, T3–7, None SG None): Tabak für Petru – Petru raucht seit Wochen etwas, das nach Heu riecht. Sein Tabak, Bastia Noir, kommt nur über Totòs Cousin. Totò will ihn besorgen, weil Petru den Cousin vor Jahren aus dem Wasser gezogen hat. Er zahl…

## Gegenstände / Essen

- liebt **Canistrelli mit Anis** (canistrelli, geschenk): Korsisches Gebäck, hält ewig.
- liebt **Myrtenlikör** (myrtle, geschenk): 
- hasst **Designer-Sonnenbrille** (designer_sonnenbrille, geschenk): 
- hasst **Selfie-Stick aus Karbon** (selfie_stick, geschenk): 
- liebt **Nautischer Almanach** (almanac, geschenk): 
- liebt **Alte Seekarte der Westküste** (old_chart, geschenk): 
- liebt **Kleiner Korallenzweig (Strandfund)** (korallenzweig, geschenk): 
- erwähnt **Eine Tasse nur für sie** (chiara_tasse, einzigartig): Handbemalt in Petrus Werkstatt, mit ihrem Namen. Für sie, nicht für die Gäste. Kette: Petru + Lola.
- erwähnt **Werkstattschild „Scuderi & Figlie“** (rosi_schild, einzigartig): Aus Treibholz, von Petru geschnitzt. Für die Werkstatt, die sie eines Tages haben will.
- erwähnt **Die Kastagnetten ihrer Großmutter** (alva_kastagnetten, einzigartig): Von Petru repariert. Kette: Alva + Petru.
- unikat **Pfeifentabak „Bastia Noir“** (petru_tabak, einzigartig): Bring-mir-Auftrag: nur Totò kann ihn besorgen.
- erwähnt **Ein Sack Tonerde** (tonerde, teil): 
- erwähnt **Rolle Netzgarn** (netzgarn, teil): 
- hasst **Leuchtendes Plankton-Gelee** (plankton_gelee, snack): 
- liebt **Fiadone** (fiadone, snack): Korsischer Käsekuchen mit Zitrone.
- hasst **Bibimbap** (bibimbap, gericht): Petru: „Why is it in a bowl?“
- liebt **Bouillabaisse** (bouillabaisse, gericht): Provenzalischer Fischtopf mit Rouille.
- haltung: {"essen": "+", "alkohol": "+", "schmuck": "-", "technik": "-", "papier": "0", "natur": "+", "party": "-", "intim": "-"}

## Prompt Studio

- **base_prompt:** "{tags_action}, full body shot from head to knees, solo, one single man alone in the frame, his whole body in full view, head and knees inside the frame,\nSubject: Petru Albertini, a weathered Corsican fisherman in his seventies, deep-tanned leathery skin with deep wrinkles, short white stubble beard, bushy white eyebrows, pale grey eyes, wiry and strong for his age,\nWearing: {outfit},\nPose: {p…
- **sprite_prompt:** "{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to knees, direct gaze, one single man alone in the frame, his whole body in full view, head and knees inside the frame,\nSubject: Petru Albertini, a weathered Corsican fisherman in his seventies, deep-tanned leathery skin with deep wrinkles, short white stubble beard, bushy white ey…
- **fashion_prompt:** "{tags_action}, front view, full body shot from head to knees, standing in full view, beige plain background,\nSubject: Petru Albertini, a weathered Corsican fisherman in his seventies, deep-tanned leathery skin with deep wrinkles, short white stubble beard, bushy white eyebrows, pale grey eyes, wiry and strong for his age,\nWearing: {outfit},\nPose: {pose},\n{st},\n{tags_photo}"
- **loras:** [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7}, {"name": "Krea_Redux.safetensors", "strength": 0.5}]
- **st_set:** "Yacht_Petru/Standard/roh"
- **sv_sets:** ["X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Petru\\Standard\\Sorted", "X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Petru\\Set2\\Sorted"]
- **Kostüm-Presets:** Standard

## Stimme

- Stimme (eden-config): Petru Albertini

## Builder basis_eden_rise.py

- basis:115 `"Petru has read about a recall"]},`
- basis:404 `"petru_workshop": R("Petru's boat workshop (ashore)", "corsican_fisherman_workshop.png", privat=3,`
- basis:423 `"kein_handy": ["petru"],`
- basis:484 `"petru": {"name": "Petru Albertini", "stimme": "Petru Albertini", "kurz": "Petru", "romanzierbar": False,`
- basis:499 `for _pid in ("toto", "yasin", "petru"):`
- basis:551 `# Lea: Petru -> Rumpf -> Margot`
- basis:557 `"lea_margot": S("tag", "Petru's story", ["lea"], "petru_workshop",`
- basis:558 `"Petru tells the story of the Margot, and Lea goes very quiet.",`
- basis:573 `"petru_fish": {"text": "Petru ties up alongside with a crate of fish and doesn't want money.", "bedingung": {"wert": ["ruf", ">=", 2]}},`
- basis:730 `"petru": {`

## Docs (ohne VERDECKT)

- docs\archiv\BRAIN_TRUST_UEBERGABE.md:35 - **Epilog-Karten** für alle Crew-Figuren + ~8 wichtige NPCs (Totò, Casanova, Petru, Nonna Fiora, Adrien …),
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:230 - Akt 3: genest im Dorf, späte Liebe mit **Petru** – mit **viel Dialog, nicht wortkarg**. Ihre **Mutter kommt nach
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:279 - **Nebenmission (Duc):** Sophia schreibt **Siris Buch über Petru**, als Geschenk für Siris Vater.
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:291 Petru-Buch „Geschrieben von Sophia Moore“ = Name auf dem Buchrücken, mit Margot-Kapitel + Leas Fotos.
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:292 Verbesserungen: Siris Buch in 3 Schritten (Petru-Interview, Fotos, Margot-Kapitel braucht Opas zwei Hälften) ⭐ ·
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:308 - Faden in die Bucht (B): Petru (Akt 3 mit Holm) sucht Nachfolge für seine Bootswerkstatt, Schild „Scuderi & Figlie“.
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:405 Festa-Kasse lacht, Petru verkauft sein Boot) · **2½b Gerettet, aber nicht unsere** (ohne Gemeinschaft; Naturschutz einer
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:406 Pariser Stiftung, Petru am Zaun, Hände in den Taschen wie Rosis Papa) · **2½c Er kommt wieder** (ohne Stärke; nach dem
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:463 (6) Epiloge: Geständnis + gerettet = Bewährung, erster legaler Laden in Cala d'Orsu (Schild von Petru) · Geständnis +
- docs\wiki\welt\orte.md:94 **Auftakt:** Petru (Fischer und Handwerker im Dorf) hat vor fünf Jahren seine Frau an den Krebs verloren. Seitdem ist
- docs\wiki\welt\orte.md:97 heißt es, sie sei mit einem Fremden in Uniform gesehen worden. Petru bittet Duc, sie zu holen.
- docs\wiki\welt\orte.md:112 | **A – Adrien an Wolff übergeben** | Gesetz ist Gesetz. Wolff dankt knapp | **Geld** und ein Ausrüstungsgegenstand der Legion, der **Einschüchtern verstärkt**. Laetitia geht mit Petru heim und spricht kein Wort mehr mi…
- docs\wiki\welt\orte.md:114 | **C – Wolff die Fotos zeigen** | Wolff glaubt Duc nicht und greift an. **Kampf gegen Wolff** – erst nach dem Kampf beruhigt er sich und sieht sich die Bilder an | **Verloren:** wie Weg A. **Gewonnen:** Wolff begreift,…
- docs\wiki\welt\orte_drehbuch.md:224 *Erzähler:* Petru repariert ein Netz, das nicht kaputt ist. Auf der Werkbank ein Foto: eine lachende Frau, daneben
- docs\wiki\welt\orte_drehbuch.md:232 - „Vielleicht will sie nicht heim, Petru.“ (Empathie – Petru: Vertrauen kurz −, später +)
- docs\wiki\welt\orte_drehbuch.md:326 → **Geld** + Ausrüstung **„Legionärs-Abzeichen“** (Einschüchtern verstärkt). Laetitia kehrt zu Petru zurück, spricht
- docs\wiki\welt\orte_drehbuch.md:352 **Weg C:** *Laetitia kommt herein. Petru lässt das Netz fallen. Sie reden lange, man hört es nicht. Dann kommt Petru
- docs\wiki\welt\orte_drehbuch.md:355 → **Petru: Vertrauen startet bei 1.**
- docs\wiki\welt\orte_drehbuch.md:357 **Weg A:** *Laetitia geht an Duc vorbei, ohne ihn anzusehen. Petru dankt Duc mit einem Kopfnicken und einer Flasche
- docs\wiki\systeme\tage_erkundung.md:68 - 21.10.2026: **genau 1 Lieblingsessen pro Person** (Lola: Bao Buns, Petru: Fish Pie, Alva behält Chili Noodles,
- docs\brain_trust\alva_casanova_dossier.md:15 | Beziehungen | Duc (flirtet, Events ab Vertrauen 2/3/4); Lola (Tresen-Tanz, Arancini-Duell, Kastagnetten); Totò (Gennaro-Kette, Dieselkonkurrenz); Elsa (duldet nicht, schaut); Petru (repariert Kastagnetten); Chiara (Ei…
- docs\brain_trust\alva_casanova_dossier.md:47 5. Elternhaus (Casanova), Vaterbar (Alva), Papas Werkstatt (Rosi/Petru): gemeinsamer Verlust-Faden „was Alon einzäunt“ (ÜB:301).
- docs\brain_trust\holm_chiara_dossier.md:56 | Vorlieben / Geschenke | Grundhaltung: Schmuck +, Papier +, Natur +, Party –, sonst 0. **Liebt**: Franzbrötchen (selbst gebacken, Mission), rosa Perle an feiner Kette, Ducs Gedicht übers Meer, Wollsocken, Rote Grütze m…
- docs\brain_trust\lea_dossier.md:14 - Beziehungen: Chiara (Idol, „chick“), Siri (Freundin), Rosi (Rivalin Tender-Garage), Totò (Angeln), Petru (Koordinaten),
- docs\brain_trust\lea_dossier.md:21 (Koordinaten von Petru), rechnet die Mehrstrecke klein (+1,8 statt +11,2 sm). Duc zeichnet 17:40 ab.
- docs\brain_trust\lola_jana_dossier.md:64 | Beziehungen | **Duc**: mochte ihn ab dem ersten leeren Teller, stellt ihm wortlos Essen hin, wenn er Mahlzeiten auslässt (lola.txt:9); Kombüse als Hitze-Stufe 2, Kabinentür auf Stufe 4 (lola.txt:81). **Holm**: tut so,…
- docs\brain_trust\lola_jana_dossier.md:91 | Beziehungen | **Duc**: „Sir“; allein kaum ein Wort, in der Gruppe neckt sie ihn und wartet, was er tut (jana.txt:9). **Lea**: **beste Freundin**, die zwei Tollpatschigsten an Deck; zusammen zwei Fender, einen Mopp und…
- docs\brain_trust\lola_jana_dossier.md:228 - `lola_tasse_1–3` T2–7: Tasse für **Chiara** (Farben erfragen Charm 12 → Ton zu **Petru** → töpfern Perception 12) →
- docs\brain_trust\lola_jana_dossier.md:231 Cunning 13) → `alva_kastagnetten`. Petru: „Für sie. Nicht von mir.“
- docs\brain_trust\lola_jana_dossier.md:401 - **Dorf-Fäden vorhanden**: Petru (Töpferscheibe, Fiona, Bastianu, Thunfisch), Alva (Tresen, Arancini-Duell, Kastagnetten,
- docs\brain_trust\megan_alon_dossier.md:50 - **Casanova, Petru, Adrien, Wolff:** keine direkte Beziehung in den Daten. Petru ist alternativer Ersatzmodul-Lieferant neben Megan (story_eden_rise.py:100).
- docs\brain_trust\megan_alon_dossier.md:154 - **Petru/Laetitia:** indirekt (Laetitia versteckt Adrien).
- docs\brain_trust\siri_yasin_dossier.md:53 - **Petru**: erinnert sie so sehr an ihren Vater, dass sie ihn kaum ansehen kann (Mission Ratgeber).
- docs\brain_trust\siri_yasin_dossier.md:96 - `siri_ratgeber_1/2` „Ein Buch für Siris Vater“ (T3–7): Netzgarn für Petru besorgen, dann Empathie 13 – Duc stellt die Fragen; Lohn Item „Ratgeber: Die Kunst der Fischerei auf Korsika“ (von Hand gebunden, für ihren Vat…
- docs\brain_trust\sophia_rosi_dossier.md:52 | Beziehungen | **Duc**: erster Mensch, an dem ihr Charme abgleitet; Wetten; er hat ein Kapitel. **Lea**: kleine Schwester, siehe Abschnitt 3. **Chiara**: beste Freundin + Rivalin, Strichliste am Kühlschrank (wer mehr G…
- docs\brain_trust\sophia_rosi_dossier.md:74 | Vorlieben / Geschenke | Grundhaltung: Essen +, Alkohol 0, **Schmuck –**, **Technik +**, **Papier –**, Natur 0, **Party +**, Intim 0 (geg_py:29). **Liebt**: Arancini vom Bäcker, Lolas Gewürzmischung „Ocean Glitter“, Pr…
- docs\brain_trust\sophia_rosi_dossier.md:76 | Beziehungen | **Duc**: „offizieller Rivale“ seit er in Woche 1 die Tender-Winde allein reparierte; Spalte „Reparaturen: Rosi vs Officer“. **Chiara**: nennt sie „Mole/Maulwurf“ (taucht nur zum Essen auf), will sie auf …
- docs\brain_trust\sophia_rosi_dossier.md:168 Margot-Suchgebiet (Koordinaten von Petru), rechnet die Mehrstrecke klein; Duc zeichnet 17:40 ab; Autopilot hält
- docs\brain_trust\sophia_rosi_dossier.md:258 Totò, Strom +2) · `rosi_arancini` **Arancini wie bei Nonna** (T3–7, Perception SG 12, Kochen, persönlich) · Petru-Kette
- docs\brain_trust\sophia_rosi_dossier.md:320 | gv_aussenborder | T2–6, V Petru ≥2 | Hammer (Petru) vs. Messgerät (Rosi) |
- docs\brain_trust\sophia_rosi_dossier.md:429 - **Dorf-Anker**: Lieblingsort Petrus Werkstatt, Schild „Scuderi & Figlie“, Außenborder-Streit mit Petru – einziger
- docs\brain_trust\toto_maxwell_dossier.md:15 | Beziehungen | Duc („Comandante“, Draht 0-5, Start 1); Jana (Chef); Lea (angeln, Qualle, Tender); Rosi (Armdrücken, Wett-Streit); Elsa (Gegenspielerin, wird gejagt); Megan (ihre Drohne jagt ihn); Alva (Gennaro-Kette, D…
- docs\brain_trust\toto_maxwell_dossier.md:59 9. **Epilog-Liste:** ÜB:34 nennt ~8 NPCs (Totò, Casanova, Petru, Fiora, Adrien ...), Maxwell fehlt; sein Lebensziel (Studio Durban, Gogo) ist auch nicht an Bucht-Ausgang gekoppelt.

## VERDECKT – Fall-Bezüge (nie im Chat zitieren)

- **Fall 1**
  - f1_13 [Weg, gesichert]: "Diagnose beenden" setzt R2 nicht zurück. Unter Dauerlast im R2 überhitzt ein PX-480 - genau das zeigt die Kurve bis zum Ausfall.
- **Fall 2**
  - f2_06 [Quelle/weiß/Weg, aussage]: Petru: WP4 liegt genau in dem Suchgebiet, das er Lea geschickt hat.
  - f2_11 [Weg, gesichert]: Bei 10,6 kn Dauerfahrt liegt LM3 deutlich über Nennlast; bei 8 kn wäre es im Normalbereich geblieben.
  - schickt die Nachricht kurz vor Morgen (Tag 3)
- **Fall 4**
  - f4_13 [Weg, gesichert]: Original-Diagnoseprotokoll Tag 2 (altes Servicegerät): "Sperre 01:44-07:50 (Karte 2), Umschaltung im R2, Wiederanlauf 06:10."
  - f4_15 [Weg, gesichert]: Laut Handbuch gilt die Sperre nur für den nächsten Kaltstart; tatsächlich behandelt die Steuerung die automatische Umschaltung wie einen Kaltstart und geht ins R2. Der Wiederanlauf aus R2 überlastet LM3.
- **Fall 5**
  - f5_13 [Weg, gesichert]: Wiederzuschalten der Querkupplung unter Last zwingt die Steuerung ins R2; LM3 trägt die Spitzenlast und fällt aus.
- **Fall 6**
  - f6_06 [weiß/Weg, belastbar]: Herstellerunterlagen zu PX-480 (über Petrus Kontakt): bekannte thermische Vorschädigung einzelner Chargen, Ausfall auch im Normalbetrieb möglich.
  - f6_07 [erwähnt, gesichert]: Unabhängige Prüfung (Rosi misst nach den Herstellerunterlagen, Petru dokumentiert): thermische Vorschädigung von LM3, Ausfall ohne äußeren Auslöser.

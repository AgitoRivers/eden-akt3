# Auszug: Casanova

Automatisch erzeugt von werkzeuge/figur_auszug.py. Fall-Bezüge stehen nur im letzten Abschnitt VERDECKT (Duc liest diese Dateien nicht; im Chat nie Inhalte daraus nennen).

## Engine (modul.json)

```json
{
 "name": "Madame Casanova",
 "stimme": "Madame Casanova",
 "kurz": "the mayor",
 "romanzierbar": false,
 "beschreibung": "mayor of Cala d'Orsu, 40, a whirlwind with anime-style humour: dramatic poses, exaggerated gasps, fist pumps and sudden speeches, treats every village event like a season finale; wants the stranded superyacht as the big attraction of the festa",
 "ablauf": {
  "*": "village_harbour"
 },
 "set_standard": "casanova_standard",
 "set_regeln": [
  {
   "ort": "village_piazza",
   "set": "alva_flamenco_rojo"
  }
 ],
 "geschenk_reaktion": [
  "ruf",
  "The mayor reacts as if she had been given a national honour - gasps, poses, a little speech."
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
| br_festa_auftritt | bordrat | T3–4 nacht | erwähnt | Die Crew als Festa-Attraktion – Madame Casanova will die Crew auf der Festa sehen. Auf einer Bühne. In Matrosenkostümen. Mit einem Lied. Rosi hält den Brief hoch und kann nicht aufhören zu la… |
| br_dorfkinder | bordrat | T2–6 nacht | erwähnt | Die Kinder aus dem Dorf – Drei Kinder aus dem Dorf rudern jeden Tag zur Yacht und starren. Heute haben sie einen Zettel hochgehalten: „Bitte Führung?“ Lea hat ihn fotografiert. |
| br_ehrenbuerger | bordrat | T3–5 nacht | erwähnt | Ehrenbürger von Cala d'Orsu – Madame Casanova will Duc auf der Festa zum Ehrenbürger machen. Mit Schärpe, Krone aus Muscheln und einer Rede. Die Krone hat sie schon gebastelt. Rosi hat ein … |
| hy_casanova_rede | handy | T3–4 tag/abend | anrufer | Casanova probt ihre Rede – Madame Casanova ruft per Video an. Sie steht auf einem Stuhl auf der Piazza und probt ihre Festa-Rede. Sie will ehrliches Feedback. Sie will kein ehrliches Fee… |
| hy_casanova_einladung | handy | T3–5 tag | anrufer | Die Einladung zur Festa – Casanova hält eine Karte mit rotem Wachssiegel in die Kamera. Eine persönliche Einladung zur Festa, nur für Duc und eine Begleitung seiner Wahl. |
| g1_blaskapelle | gag1 | T2–5 fruehstueck | handelnd | Casanovas Blaskapelle – Sieben Uhr früh. Ein Fischerboot fährt neben die Yacht. Darauf steht Madame Casanova mit der Blaskapelle des Dorfs. Sie spielen die Hymne von Cala d'Orsu. Laut. |
| gv_arancini_duell | gagv | T3–6 abend | zuschauer | Das Arancini-Duell – Lola behauptet, ihre Arancini sind die besten des Mittelmeers. Alva hat dazu eine Meinung. Das ganze Dorf schaut zu. Duc ist Jury. |
| gv_casanova_chiara | gagv | T2–3 tag | links | Die Bürgermeisterin will an Bord – Madame Casanova will die Yacht feierlich betreten, mit Schärpe und Fotograf. Chiara steht an der Gangway und lässt niemanden durch. Die Bürgermeisterin hat sch… |
| gv_casanova_alva | gagv | T3–5 tag | links | Die VIP-Lounge – Madame Casanova will Alvas Bar für die Festa zur VIP-Lounge machen. Mit Samtseil. Alva will ihre Bar so lassen, wie sie ist: laut, voll und für alle. |
| gv_elsa_alva | gagv | T3–6 tag | zuschauer | Diesel unter dem Tresen – Elsa sitzt an Alvas Tresen und trinkt einen Espresso. Unter dem Tresen stehen vier Dieselkanister. Jeder weiß es. Elsa schaut Alva lange an. |
| du_koch_alva | duell | T3–7 abend | zuschauer | Koch-Showdown: Korsika gegen Saigon – Alva hat die Tische zusammengeschoben. Auf der einen Seite stehen ihr Fiadone und ihre Wildschwein-Pastete, auf der anderen deine Garküche aus zwei Gaskochern.… |
| auf_karaoke | auftritt | T3–7 abend | publikum | Karaoke in Alvas Bar – Alva hat eine Karaoke-Maschine aus den Neunzigern im Keller gefunden. Das Mikrofon knistert, die Texte laufen auf einem Röhrenfernseher. Die halbe Crew ist da.… |
| g1_casanova_nebel | gag1 | T3–5 tag | handelnd | Die Generalprobe – Madame Casanova probt ihren Auftritt für die Festa. Im Flamenco-Kleid, auf einem Fischkutter, mit einer gemieteten Nebelmaschine. Der Nebel ist dichter als gep… |
| gv_elsa_kiste | gagv | T3–7 tag/abend | zuschauer | Kartoffeln, die miauen – Elsa hat eine von Totòs Kisten am Kai aufgehalten. Auf der Kiste steht „Kartoffeln“. Die Kiste miaut. Totò behauptet, es seien sehr junge Kartoffeln. Elsa hat … |
| ab_casanova_flamenco | abend | T4–7 abend/nacht | pid | Flamenco mit der Bürgermeisterin – Die Piazza ist leer, die Lichterketten der Festa hängen noch. Madame Casanova steht im roten Flamenco-Kleid unter dem Brunnen, ein altes Kofferradio zu ihren F… |

## Missionen

- **casanova_plan** (von casanova, T3–5, charm SG 12): Ein Nachhaltigkeitsplan für die Festa – Madame Casanova hat gehört, dass du Nachhaltigkeitsberater bist. Sie will die grünste Festa Korsikas. Mit Feuerwerk. Und Einweggrills. Und vierhundert Luftballons.
- **english_kids** (von casanova, T2–6, charm SG 10): Englisch für die Enkel der Bürgermeisterin – Zwei Enkel, eine Stunde, ein Schulbuch. Madame Casanova zahlt bar und erzählt es dem ganzen Dorf.
- **casanova_banner** (von casanova, T3–5, courage SG 10): Festa-Banner aufhängen – Zwanzig Meter Stoff, ein Kirchturm, eine Leiter von 1962. Madame Casanova spendiert dafür eine Einladung zur Festa.
- **lea_fueller_1** (von lea, T2–7, charm SG 12): Ein Füller für Sophia: der Graveur – Lea will ihrer Schwester einen Füller schenken. Graviert mit ihrem eigenen Namen, für das, was Sophia nur für sich schreibt. Den einzigen Graveur weit und breit kennt Madame Casanova, und die gibt Ad…
- **casanova_elsa_1** (von casanova, T2–7, perception SG 12): Ein Geschenk für die Leutnantin: das Archiv – Elsa ist seit zehn Jahren auf dem Posten von Cala d'Orsu. Das Dorf will ihr danken, aber sie nimmt nichts an. Alles wäre Bestechung. Madame Casanova hat eine Idee: Elsas eigene Strafzettel aus zehn J…
- **casanova_elsa_2** (von casanova, T2–7, None SG None): Ein Geschenk für die Leutnantin: das Leinen – Gebunden wird in Leinen, sagt Madame Casanova, wie ein Staatsdokument. Leinen gibt es nur bei Alva, und mit Alva redet Madame Casanova seit dem Dorfladen-Streit nicht mehr.
- **casanova_elsa_3** (von casanova, T2–7, perception SG 12): Ein Geschenk für die Leutnantin: binden – Dreihundertzwölf Blätter, ein Rücken, Ahle und Faden. Madame Casanova hält dabei eine Rede, die niemand bestellt hat.
- **casanova_buffet** (von casanova, T3–5, perception SG 12): Ein Probeessen für die Festa – Madame Casanova will auf der Festa ein Buffet „aus aller Welt, aber korsisch“. Die Jury besteht aus ihr, ihrer Mutter und dem Pfarrer. Der Dorfkoch hat abgesagt, weil sie ihm „Vision“ vorgeworfen hat…

## Gegenstände / Essen

- liebt **Diva-Sonnenbrille in Herzform** (herzbrille, geschenk): 
- hasst **Nautischer Almanach** (almanac, geschenk): 
- liebt **Tüte Konfetti** (konfetti, geschenk): 
- liebt **Glitzer-Schärpe „Miss Cala d'Orsu“** (schaerpe, geschenk): 
- unikat **Konfettikanone** (casanova_kanone, einzigartig): Für die Festa. Sie wird damit auf die Yacht zielen.
- erwähnt **Drei „Designer“-Taschen** (taschen, schmuggel): 
- liebt **Ocean-Glitter-Popcorn** (ocean_popcorn, snack): 
- liebt **Bouillabaisse** (bouillabaisse, gericht): Provenzalischer Fischtopf mit Rouille.
- haltung: {"essen": "+", "alkohol": "0", "schmuck": "+", "technik": "-", "papier": "0", "natur": "0", "party": "+", "intim": "-"}

## Prompt Studio

- **base_prompt:** "{tags_action}, full body shot from head to knees, solo, one single woman alone in the frame, her whole body in full view, head and knees inside the frame,\nSubject: Madame Casanova, the mayor of a Corsican fishing village, 40, a sleek dark bob with one silver streak, bright red lipstick, big expressive dark eyes, slim and bursting with energy, a theatrical over-the-top grin like an anime charact…
- **sprite_prompt:** "{tags_action}, Shot on an iPhone, grainy amateur photo, realistic smartphone photography, full body shot from head to knees, direct gaze, one single woman alone in the frame, her whole body in full view, head and knees inside the frame,\nSubject: The actor Monica Belucci, 40, a sleek dark bob, bright red lipstick, big expressive brown eyes, \nWearing: {outfit},\nScene: {setting}, {st},\n{express…
- **fashion_prompt:** "{tags_action}, front view, full body shot from head to knees, standing in full view, beige plain background,\nSubject: Madame Casanova, the mayor of a Corsican fishing village, 40, a sleek dark bob, bright red lipstick, big expressive brown eyes, \nWearing: {outfit},\nPose: {pose},\n{st},\n{tags_photo}"
- **loras:** [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7}, {"name": "Krea_Redux.safetensors", "strength": 0.5}, {"name": "Monica_Bellucci_KREA2.safetensors", "strength": 1}]
- **st_set:** "Yacht_Casanova/Flamenco/roh"
- **sv_sets:** ["X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Casanova\\Standard\\Sorted", "X:\\AI\\ComfyUI_krea2\\ComfyUI\\output\\expressions\\Yacht_Casanova\\Flamenco\\Sorted"]
- **Kostüm-Presets:** Flamenco, Standard

## Stimme

- Stimme (eden-config): Madame Casanova

## Builder basis_eden_rise.py

- basis:487 `"casanova": {"name": "Madame Casanova", "stimme": "Madame Casanova", "kurz": "the mayor", "romanzierbar": False,`
- basis:746 `"casanova": {`

## Docs (ohne VERDECKT)

- docs\archiv\BRAIN_TRUST_UEBERGABE.md:30 **2 Zerrissen** (öffentlich gemacht mit Casanova + Dorf; braucht Adriens Fotos, Steuerchip, Ruf; Duc gefeuert) ·
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:34 - **Epilog-Karten** für alle Crew-Figuren + ~8 wichtige NPCs (Totò, Casanova, Petru, Nonna Fiora, Adrien …),
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:144 (1) Akt-1-Beweise nur in Räumen/Orten, die in Akt 1 offen sind · (2) Casanova sitzt in Akt 1 am Hafen, Piazza öffnet
- docs\archiv\BRAIN_TRUST_UEBERGABE.md:352 `docs/brain_trust/lola_jana_dossier.md` wird gesammelt) → **Alva + Casanova** (Dorf) → **Maxwell + Totò** (Bord-NPCs). Bisheriger Hinweis zu Rosi: **Rosi** (Dossier liegt schon in `docs/brain_trust/sophia_rosi_dossier.m…
- docs\wiki\systeme\kampf.md:219 | Elektro-Harpune | 7 | Luft | Episch | Fern, 2 Slots | Geschenk Madame Casanova nach der Festa | – |
- docs\wiki\systeme\kampf.md:260 | Plüsch-Flamingo | Madame Casanova | Fassung −4 schon nach 2 perfekten Paraden |
- docs\wiki\welt\orte.md:46 **Auftakt im Dorf (Hafen):** Madame Casanova ist misstrauisch gegenüber der Yacht-Crew („Schon wieder reiche Leute,
- docs\wiki\welt\orte.md:49 leben dort mit den Mönchen. Casanova: „Fiora hat noch nie einen Markttag verpasst. Noch nie.“
- docs\wiki\welt\orte.md:86 Madame Casanova gewinnt Vertrauen in Duc.
- docs\wiki\welt\orte_drehbuch.md:16 *Madame Casanova sitzt am Brunnen, roter Fächer, und mustert Duc wie einen Fleck auf ihrer Tischdecke.*
- docs\wiki\welt\orte_drehbuch.md:28 → Ortskapitel startet. Madame Casanova: Vertrauen +klein.
- docs\wiki\welt\orte_drehbuch.md:214 **In beiden Fällen:** **Schnellreise zum Kloster** frei · Missionsgegenstand **Steuerchip** · Madame Casanova:
- docs\wiki\systeme\tage_erkundung.md:42 ## Nebenquest Madame Casanova gegen Alon
- docs\wiki\systeme\tage_erkundung.md:44 Madame Casanova hasst Alon wegen seiner rücksichtslosen Extravaganz. Aufträge rund um sein Anwesen und den ausgebrochenen
- docs\wiki\systeme\tage_erkundung.md:55 7. Missionen mit Ort und Gegenstand, Casanova-Quest, Wirkung von Ruf
- docs\wiki\systeme\tage_erkundung.md:69 Madame Casanova Bouillabaisse) plus **10 Standard-Gerichte**, die von Anfang an freigeschaltet sind.
- docs\brain_trust\alva_casanova_dossier.md:1 # Dossier Paar 7: Alva Santoni + Madame Casanova (die Frauen des Dorfes)
- docs\brain_trust\alva_casanova_dossier.md:15 | Beziehungen | Duc (flirtet, Events ab Vertrauen 2/3/4); Lola (Tresen-Tanz, Arancini-Duell, Kastagnetten); Totò (Gennaro-Kette, Dieselkonkurrenz); Elsa (duldet nicht, schaut); Petru (repariert Kastagnetten); Chiara (Ei…
- docs\brain_trust\alva_casanova_dossier.md:19 ## 2. Madame Casanova
- docs\brain_trust\alva_casanova_dossier.md:26 | Stimme | Stimme „Madame Casanova“ vorhanden; Reaktion auf Geschenke: Staatsehre, Keuchen, Rede | MJ |
- docs\brain_trust\alva_casanova_dossier.md:36 - Event gv_casanova_alva: Casanova will Alvas Bar zur Festa-VIP-Lounge mit Samtseil, Alva will sie „laut, voll, für alle“ lassen.
- docs\brain_trust\alva_casanova_dossier.md:37 - Beide in gv_arancini_duell, du_koch_alva, auf_karaoke und gv_elsa_alva (Casanova nur Zuschauerin).
- docs\brain_trust\alva_casanova_dossier.md:46 4. Alvas Bar als Nachrichtenbörse und Casanovas Ruf-Mechanik (Bucht-Ende 2 „öffentlich gemacht mit Casanova + Dorf“) verbinden: Alvas Tratsch liefert die Stimmung des Dorfes.
- docs\brain_trust\alva_casanova_dossier.md:47 5. Elternhaus (Casanova), Vaterbar (Alva), Papas Werkstatt (Rosi/Petru): gemeinsamer Verlust-Faden „was Alon einzäunt“ (ÜB:301).
- docs\brain_trust\alva_casanova_dossier.md:52 2. **Groll Casanova vs. Engine:** Beschlossen ist „Elternhaus von Alon eingezäunt“ (ÜB:210); ET:44 und EO sagen „hasst Alon wegen rücksichtsloser Extravaganz“, EO:46 Misstrauen gegen die Yacht. Beide Fassungen müssen ve…
- docs\brain_trust\alva_casanova_dossier.md:53 3. **Set-Regel-Kopierfehler:** MJ Casanova `set_regeln` nutzt `alva_flamenco_rojo` (Alvas Set) statt eines eigenen Casanova-Sets; PS hat nur „Flamenco“ und „Standard“.
- docs\brain_trust\alva_casanova_dossier.md:55 5. **Casanova-Sprite:** `sprite_prompt` nennt eine reale Schauspielerin samt LoRA, die Base nicht; Augen dunkel (Base) vs. braun (Sprite), Anime-Grinsen fehlt im Sprite.
- docs\brain_trust\alva_casanova_dossier.md:56 6. **Piazza/Akt-Konflikt:** Casanova sitzt in Akt 1 am Hafen, Piazza öffnet in Akt 3 (ÜB:144), aber MJ-Regeln, ab_casanova_flamenco (T4-7) und Karaoke/Poker in Alvas Bar liegen in der 7-Tage-Zeit. Ob Alvas Bar in Akt 1 …
- docs\brain_trust\alva_casanova_dossier.md:58 8. **Lücke Prämisse:** keine Bindung beider an Bucht-Verkauf/Alon in der Engine; Casanova ist nur über Bucht-Ende 2 eingebunden, Alva gar nicht.
- docs\brain_trust\alva_casanova_dossier.md:60 10. **Altersfrage:** Casanova ist 40, hat Enkel (english_kids) und eine noch rüstige Mutter; gewollt oder anpassen?
- docs\brain_trust\lola_jana_dossier.md:64 | Beziehungen | **Duc**: mochte ihn ab dem ersten leeren Teller, stellt ihm wortlos Essen hin, wenn er Mahlzeiten auslässt (lola.txt:9); Kombüse als Hitze-Stufe 2, Kabinentür auf Stufe 4 (lola.txt:81). **Holm**: tut so,…
- docs\brain_trust\lola_jana_dossier.md:91 | Beziehungen | **Duc**: „Sir“; allein kaum ein Wort, in der Gruppe neckt sie ihn und wartet, was er tut (jana.txt:9). **Lea**: **beste Freundin**, die zwei Tollpatschigsten an Deck; zusammen zwei Fender, einen Mopp und…
- docs\brain_trust\lola_jana_dossier.md:402 Vegemite/Tim Tams aus Alvas Vorrat), Casanova nur über die „Blumen der Bürgermeisterin“ (gv_festa_outfits).
- docs\brain_trust\megan_alon_dossier.md:50 - **Casanova, Petru, Adrien, Wolff:** keine direkte Beziehung in den Daten. Petru ist alternativer Ersatzmodul-Lieferant neben Megan (story_eden_rise.py:100).
- docs\brain_trust\megan_alon_dossier.md:151 - **Madame Casanova:** hasst ihn; Nebenquest „Casanova gegen Alon“ rund um Anwesen und ausgebrochenen Zoo, Lohn Ruf im Dorf, am Ende Elektro-Harpune nach der Festa (tage_erkundung.md:42–45). Bucht-Ende 2 „Zerrissen…
- docs\brain_trust\megan_alon_dossier.md:184 - **Bucht-Enden:** 0 Zu spät (Alon kauft) · 1 Unterschrieben (Festa unter Alons Logo) · 2 Zerrissen (Fotos + Steuerchip + Ruf, mit Casanova/Dorf, Duc gefeuert) · 3 Neu geschrieben (Genossenschaft) – müssen neu an Akt-3-…
- docs\brain_trust\siri_yasin_dossier.md:157 - **Sonnenaufgang = Megans Auftrag**: Der „Gästewunsch Sonnenaufgang“ (r_02) wird zum gebuchten Content-Termin: Megan/Eden Group (ggf. mit Madame Casanova, die die Yacht ohnehin als Festa-Attraktion will) bezahlt Siris …
- docs\brain_trust\sophia_rosi_dossier.md:52 | Beziehungen | **Duc**: erster Mensch, an dem ihr Charme abgleitet; Wetten; er hat ein Kapitel. **Lea**: kleine Schwester, siehe Abschnitt 3. **Chiara**: beste Freundin + Rivalin, Strichliste am Kühlschrank (wer mehr G…
- docs\brain_trust\sophia_rosi_dossier.md:76 | Beziehungen | **Duc**: „offizieller Rivale“ seit er in Woche 1 die Tender-Winde allein reparierte; Spalte „Reparaturen: Rosi vs Officer“. **Chiara**: nennt sie „Mole/Maulwurf“ (taucht nur zum Essen auf), will sie auf …
- docs\brain_trust\toto_maxwell_dossier.md:59 9. **Epilog-Liste:** ÜB:34 nennt ~8 NPCs (Totò, Casanova, Petru, Fiora, Adrien ...), Maxwell fehlt; sein Lebensziel (Studio Durban, Gogo) ist auch nicht an Bucht-Ausgang gekoppelt.

## VERDECKT – Fall-Bezüge (nie im Chat zitieren)

_Keine Fall-Bezüge._

# Dossier Paar 4: Sophia (+ Lea) · Rosi (Stand 22.10.2026, Recherche read-only)

**Änderung durch Duc während der Recherche:** Paar 4 ist jetzt **Sophia + Lea** (die Schwestern sollen enger verwoben
werden). Rosi steht trotzdem vollständig in diesem Dossier (kommt später dran). Abschnitt 3 ist deshalb der Schwerpunkt.

Quellen-Kürzel:
- `sophia.txt` / `rosi.txt` / `lea.txt` = X:\AI\Eden\karten_neu\*.txt (Kartentext EN/DE, Spiegel der Karten
  X:\AI\RoleplayGen\cards\Eden Yacht\Sophia Moore.json / Rosi Scuderi.json / Lea Moore.json). Zeilennummern beziehen
  sich auf die EN-Fassung, sofern nicht anders angegeben.
- `Karten-JSON` = die Char-Builder-JSONs (extensions.stimme, eingebettetes character_book mit 24 Einträgen = **älterer**
  Stand des Weltbuchs).
- `LB n` = ST-Weltbuch X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds\Eden Yacht.json
  (Eintrag-Nr., 72 Einträge; „[alt] … aus“ = deaktiviert).
- `basis` = werkzeuge/eden_rise/basis_eden_rise.py · `modul_py` = modul_eden_rise.py · `miss_py` = missionen_eden_rise.py ·
  `geg_py` = gegenstaende_eden_rise.py · `faelle_py` = story_faelle.py · `story_py` = story_eden_rise.py ·
  `buehne_py` = story_buehne.py · `ER` = module/eden_rise/ereignisse.json (Event-ID) · `story.json`, `buehne.json`,
  `missionen.json`, `gegenstaende.json`, `modul.json` = module/eden_rise/.
- `welt_rs` = karten_neu/welt_rosi_siri.py · `karten_rs` = karten_neu/karten_rosi_siri.py.
- `PS` = X:\AI\PromptStudio\presets.json / decks.json / set_presets.json · `cfg` = X:\AI\Eden\eden-config.json.
- `Übergabe` = docs/wiki/START.md · `LeaD` = docs/brain_trust/lea_dossier.md.

Abschnitte 1–7 enthalten keine Fall-Auflösungen für Sophia und Rosi. Leas Fall-Rolle ist laut Übergabe offen und steht
in Abschnitt 3. Alles zu Sophias und Rosis Fällen, Motiven, Geständnissen, Lügen steht nur ganz unten unter „VERDECKT“.

---

## 1. Sophia – Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | **Sophia Moore** | sophia.txt:5, modul.json personen.sophia |
| Alter | **28** – in allen Quellen gleich (auch im deaktivierten Head-Chef-Eintrag) | sophia.txt:5, LB 16, LB 18 |
| Herkunft | **Falmouth, Cornwall.** Mutter: „sweet, chaotic painter“, verkaufte Seestücke am Hafenmarkt und vergaß die Miete. Ab 14 zog Sophia ihre kleine Schwester Lea groß, wickelte Vermieter, Lehrer, Kellner um den Finger („We never had money. We always had the best table in Falmouth.“). Vater wird nirgends erwähnt. Großvater Jack Moore (Fischer) siehe Abschnitt 3 | sophia.txt:6, 85; LB 17, LB 23 |
| Laufbahn | 2 Jahre Zweitbesetzung (Understudy) im Londoner West End, **nie aufgetreten**. „Now the deck of the Eden Rise is her stage.“ | sophia.txt:6, LB 16 |
| Rolle an Bord | **Concierge und Guest Relations**, 4. Saison: Landtage der Gäste, Tische, Liegeplätze, Fahrer, Boote, Gefallen. Gäste buchen ihretwegen wieder; jeder Hafenmeister lächelt | sophia.txt:5, 7, 22, 83; LB 16 |
| Persönlichkeit | Widerspruch: „everybody loves her and nobody knows her“; sieht sofort, was andere brauchen, sorgt dafür, dass niemand fragt, was sie braucht. Charme ist ihr einziges Werkzeug; Duc ist der Erste, an dem er abgleitet (Tag 1: er fragte, was sie eigentlich will – sie hatte keine Antwort; seitdem wettet sie mit ihm). Nie grausam mit der Wahrheit | sophia.txt:9, 11, 14, 17 |
| Knopf / Marotte | Knopf: durchschaut werden (er benennt leise den Trick und bleibt trotzdem). Marotte: schreibt mitten im Gespräch etwas ins kleine braune Lederbüchlein und sagt nie was. In die Ecke gedrängt → schließt eine Wette ab | sophia.txt:16, 18–19 |
| Stimme / Sprache | tief, warm, ohne Eile, britisch; „Darling“ für jeden, den sie gleich managt; Understatement, Doppeldeutiges, ein Satz, dann Stille; ohne Show kurze, schlichte Sätze. Spricht fließend Italienisch (Portofino-Begrüßung), singt französische Chansons (ER gv_karaoke). **Stimmzuordnung: Engine „Cora“** (cfg stimmen.eden_rise.sophia), **Karte „Sophia Moore“** (Karten-JSON extensions.stimme en/de), dazu ElevenLabs-ID njBRrH42VRvVJwg7VZLZ (basis:426, Altbestand) → drei verschiedene Angaben | sophia.txt:16, 27, 96 |
| Aussehen (Karte) | langes, gestuftes **honigblondes** Haar bis über die Brust, hellere Strähnen ums Gesicht, um neun hochgesteckt, mittags unten; hellblaugraue Augen, scharfer Lidstrich, helle Haut mit Rotschimmer, roter Mund; schlank, langbeinig, flacher Bauch, schwere volle Brust; „bewegt sich wie auf einer Bühne“ | sophia.txt:5 |
| Aussehen (PS) | Preset `Yacht_Sophia`: LoRA **Krea_SophiaV2** 1.0 (+ Nsfw2/Real3/Lenovo/Redux); Tags B - Huge, Blush, Long Legs, Busty, **Honey blonde**, Sheen, Tendrils, Low Ponytail, Summer → passt zur Karte. **Reste:** base_prompt „Subject: **Leax**, cute woman with blue eyes“ (Leas Trigger-Wort, kopiert), fashion_prompt „a beautiful woman called **eve**“; ref_image Penny2.jpg | PS presets.json Yacht_Sophia |
| Outfits / Sets (6) | **Concierge** (cremefarbener Blazer mit goldenem Eden-Wappen, champagnerfarbenes Seidentop, Bleistiftrock, Tuch Marine/Gold, Schildpatt-Sonnenbrille, Lederbüchlein, Loafer) · **Shore Leave** (weiße Leinenbluse, weiße Shorts, brauner Gürtel, Tuch, Sandalen) · **Swim** (senfgelber Triangel-Bikini, Goldkette um die Taille, offenes Leinenhemd) · **Crew Party** (kurzes goldenes Paillettenkleid, barfuß) · **Writing Night** (smaragdgrüner Seidenpyjama, goldene Rundbrille im Haar, Bleistift hinterm Ohr, Ankerkette) · **Nude** (Morgenschwimmen). Zusätzlich verwaist in set_presets: **„Yacht_Sophia\|Galley“ mit sophia_chef_whites** (Head-Chef-Rest) | sophia.txt Begrüßungen; PS sp_kost, decks.json, set_presets.json |
| Engine-Sets | Standard Concierge; Swim an der Badeplattform; Shore Leave am Hafen und in Alvas Bar; **Crew Party auf der Piazza (Festa)**; nachts Writing Night | basis:435-440 / modul.json |
| Tagesablauf (Engine) | Frühstück Crewmesse · Tag **Hafen von Cala d'Orsu** · Dinner Crewmesse · Abend **Alvas Bar** · Nacht Crewmesse | basis:436 |
| Wünsche | „one thing that is hers alone, **her own name on the spine of a book**. And one person she doesn't have to win.“ | sophia.txt:15 |
| Ängste / Reibung | keine explizite Angst-Zeile. Reibung: Charme ist das einzige Werkzeug, dem sie traut. Motor fällt, wenn Duc ihre Gefallen ausnutzt oder **Buch oder Jobangebot vor anderen erwähnt**. „I've been charming since I was fourteen … It's the only thing I know how to do.“ | sophia.txt:17, 74, 94 |
| Geheimnisse (Karte) | (1) schreibt nachts **gemütliche Krimis unter dem Pseudonym M. J. Penrose**, **14 Absagen**; Geheimnisse von Gästen/Crew landen leicht verkleidet darin, Duc hat schon ein Kapitel. (2) Letzten Winter bot die Eden-Gruppe ihr **Chiaras Job als Chefstewardess** an; sie lehnte wegen Chiara ab und hat es ihr nie gesagt. Kommt Duc nahe → Wette, Einsatz wird geändert | sophia.txt:87 |
| Geheimnisse (LB) | LB 41: Megan machte das Angebot selbst im Januar – „Chief Stewardess **on a bigger boat**“; Sophia sagte ohne Grund nein; Megan hat es niemandem erzählt, „nicht einmal Holm“; liest seitdem Sophias Spesen zweimal, nennt sie zurück „darling“, würde für 10 Minuten mit dem Notizbuch zahlen. LB 7 [alt, aus]: Kuss mit Chiara nach Saint-Tropez, „Sophia has been in love with Chiara ever since“ | LB 41, LB 7 |
| Weiß (Karte) | weiß **nicht**, dass Chiara durch die Yachtmaster-Theorie fiel (glaubt, hinter Chiaras Brückennächten stecke ein Mann); weiß, dass **Lea noch Opas Wrack sucht, findet es „süß“**; ahnt **nichts** von Leas Azoren-Bewerbung; kennt die Quoten auf der Wett-Tafel der Maschinisten, **20 € auf sich selbst** | sophia.txt:89 |
| Weiß (LB) | kennt die Quoten auswendig (LB 9); weiß vor Siri, was Siri will; Notizbuch kommt raus, wenn Yasin redet (LB 31); lässt in der Kombüse Neuigkeiten fallen, um zu sehen, wo sie wieder rauskommen (LB 56) | LB 9, 31, 56 |
| Vorlieben / Geschenke | Grundhaltung: Essen +, Alkohol +, Schmuck +, **Technik –**, Papier +, Natur 0, Party 0, Intim + (geg_py:27). **Liebt**: Füllfederhalter, Gedichtband aus dem Antiquariat, Duftkerzen „Maquis“, Lavendel-Madeleines, **Sommerrollen (Kochgericht = Lieblingsgericht)**. **Hasst**: Herrenmagazin mit Pin-up, Vegemite-Käse-Schnecken, Unit-01-Muffins. **Unikat**: „Füller mit ihrem eigenen Namen“ („Graviert mit Sophia Moore, nicht mit irgendeinem anderen Namen“) – kommt über Leas Mission | gegenstaende.json; geg_py:119-134, 170, 327-342, 360 |
| Lieblingsorte | **Alvas Bar, Achterdeck** (Verabredung dort +4 V / +4 B) | basis:494 |
| Beziehungen | **Duc**: erster Mensch, an dem ihr Charme abgleitet; Wetten; er hat ein Kapitel. **Lea**: kleine Schwester, siehe Abschnitt 3. **Chiara**: beste Freundin + Rivalin, Strichliste am Kühlschrank (wer mehr Gäste zum Lachen bringt; Verliererin zahlt Crew-Dinner in Antibes), „old married couple“ (LB 11, 21); Spannung chiara_sophia Start 1 (basis:92). **Rosi**: hat ihr nie etwas verkaufen können, ihr tägliches Spiel; Rosi reparierte ihr um 3 Uhr den Laptop und gab ihn ungesehen zurück – „Sophia has not forgotten that“ (LB 28). **Holm**: nennt Hafen + Zeit, Sophia liefert den Liegeplatz, „I don't want to know how“; fand sie um 4 Uhr tippend in der Messe, hielt es für Papierkram; hält ihr Bleiben für Loyalität – „something she has got wrong“ (LB 48). **Megan**: das Angebot im Januar (LB 41); Verhandlung um freien Nachmittag (ER gv_megan_sophia). **Siri**: organisiert ihre Landgänge, Siri hält sie für „more than a concierge“ (LB 31). **Lola**: besorgt ihr Lieferanten/Fisch, schreibt danach ins Büchlein, Lola sorgt sich; Lola merkt nie, dass sie gelesen wird (LB 56); Rivalinnen bei Karaoke/Tarot/Wahrheit oder Pflicht. **Yamamoto**: pokert jede Nacht mit ihm und gewinnt; er verbeugt sich vor ihren Karten, Umschlag für die Crew (LB 58, 64). **Jana**: schickt sie mit Mutproben/Botschaften, Jana hält sie für die beste Freundin, Sophia hält Jana für „very useful“ (LB 69). **Alva**: Lieblingsort, Poker um Diesel/Kleidung (ER br_poker_einladung, gv_strip_poker). **Elsa**: Mission Papiere zur Küstenwache (missionen.json sophia_papers). **Yasin**: Notizbuch kommt raus, wenn er redet (LB 31); Bordrat Yasins Angebot. **Totò**: Crew-Kasse, Quiz-Gegnerin. **Petru, Casanova, Maxwell**: keine direkten Einträge (Casanova nur als Adressgeberin in Leas Füller-Mission) | sophia.txt, LB, ER |

## 2. Rosi – Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | **Rosaria „Rosi“ Scuderi** | rosi.txt:5, LB 24 |
| Alter | **27** (überall gleich) | rosi.txt:5, LB 24 |
| Herkunft | **Catania, am Fuß des Ätna.** Aufgewachsen in der Vespa-Werkstatt ihres Vaters **Salvo**, zerlegte mit 8 den ersten Vergaser. Vor 4 Jahren holte die Bank die Werkstatt, Salvo repariert seitdem Roller für andere („He just stood in the street with his hands in his pockets“). Mutter lebt (trägt Zitronengelb auf jeder Festa in Catania). **Nonna** letzten Winter gestorben, Arancini-Rezept nie aufgeschrieben (nur Mission) | rosi.txt:6, 53, 77; missionen.json rosi_arancini |
| Rolle an Bord | **ETO (Electro-Technical Officer)**, 3. Saison: Solardach, Batteriebänke, E-Antrieb und das Diesel-Notstromaggregat **„Unit-01“** (ihre Lieblingsmaschine, „die einzige laute“). Reviere: Antriebsraum, Generatorraum, kleine Werkstatt. Keine „Maschinistin“ im Sinne eines Dieselmotors – die Eden Rise fährt elektrisch | rosi.txt:5, 7, 23, 89; karten_rs:23-26; modul.json welt |
| Persönlichkeit | Widerspruch: erklärt jeden zum Rivalen, „so nobody notices how badly she wants to belong“. Reibung: Zuneigung zugeben hieße die Rivalität verlieren. Nie: verleiht Werkzeug; gibt nie eine Niederlage zu, nur „unentschieden“ | rosi.txt:12, 15, 18 |
| Knopf / Marotte | Knopf: fair übertroffen werden, ohne dass er angibt. Marotte: benennt Maschinen, ruft dem Drehmomentschlüssel Attackennamen zu, schmollt nach jeder Niederlage genau 10 Sekunden in einer Ecke; liest Manga in der Koje; redet mit Maschinen | rosi.txt:8, 19–20 |
| Stimme / Sprache | wenige Worte, stumpf, kein Smalltalk („Your plan is bad. Mine is better. We do mine.“), plötzliche Anime-Pathos-Ausbrüche, 10 Sekunden später ruhig; nennt Duc „Officer“, nie beim Namen; **„No Italian words dropped in as decoration“**; gerührt → redet über eine Maschine. **Stimmzuordnung: Engine „Rosi Scuderi“** (cfg); **Karte: kein stimme-Feld** (Karten-JSON extensions ohne stimme). Engine-Jobzeilen nutzen „Brava“, „Grazie“, „Madonna“, „capito?“ (basis:586ff.) → widerspricht der Kartenregel | rosi.txt:17, 102 |
| Aussehen (Karte) | dunkelbraunes, langes, glattes Haar, im Dienst unordentlicher Dutt unter rotem Bandana; **graugrüne Augen**, Sommersprossen, kleine Lötbrandnarbe am linken Handgelenk, immer ein Ölfleck; sportlich, kräftige Arme, sehr volle schwere Brust | rosi.txt:5 |
| Aussehen (PS) | Preset `Yacht_Rosi`: LoRA **Krea_Aleja** 1.0; Tags B - Large (Sets: B - Huge), dark brown, Sport Athleisure, Tendrils, Straight, Top knot. **Reste:** base_prompt „Subject: **Leax**, cute woman with **blue eyes**“, sprite_prompt „female with **light blue eyes**“ (Karte: graugrün), **ref_image = Lea (5).png** (Leas Referenzbild) | PS presets.json Yacht_Rosi |
| Outfits / Sets (7) | **Engine Room** (Navy-Overall um die Hüfte, weißes geripptes Tanktop mit Ölflecken, rotes Bandana, Werkzeuggürtel; PS: Overall mit Hosenträgern, Stahlkappenstiefel) · **Off Duty** (Karte: übergroßes graues Roboter-Shirt, Radlerhose, Socken; **PS: cremefarbenes Lounge-Set mit Zip-Hoodie, Thong, goldenes Kreuz**) · **Swim** (sportlicher roter Bikini, Taucherbrille, silbernes Fußkettchen) · **Crew Party** (Karte: Lederrock, Band-Shirt, Nietengürtel, Netzstrumpfhose, Springerstiefel, Pony; **PS: Micro-BH + Thong unter Lederjacke, Strümpfe**) · **Vespa Sunday** (mintgrüne Bomberjacke, Bandeau, Jeansshorts, rotes Seidentuch – passt) · **Festa** (Karte: zitronengelbes Leinenkleid, roter Korallenanhänger, flache Sandalen; **PS: generisches `column_flowy_dress` – senfgelb, bodenlang, Stilettos**) · **Nude** (klemmende Duschtür) | rosi.txt Begrüßungen; PS decks.json, set_presets.json |
| Engine-Sets / Ablauf | Standard Engine Room; Swim an der Badeplattform; Vespa Sunday am Hafen; Crew Party abends in Alvas Bar; **Festa auf der Piazza**; Off Duty abends in der Messe und in Ducs Kabine. Ablauf: Frühstück + Tag **Antriebsraum**, Dinner Messe, Abend **Werkstatt**, Nacht **Generatorraum** | basis:448-452 |
| Wünsche | **die Werkstatt des Vaters zurück** („Four more seasons“); jemand, der gleichauf neben ihr arbeitet, statt sie zu beschützen | rosi.txt:16, 77 |
| Ängste / Reibung | keine Angst-Zeile; Motor fällt, wenn er sie beschützt, ihre Arbeit macht, ihr Maschinen erklärt oder über Manga lacht | rosi.txt:100 |
| Geheimnis (Karte) | ganz unten auf der Wett-Tafel hat sie ihren eigenen Namen neben die drei Frauen geschrieben: **Quote 40:1, 50 € auf sich selbst**; kommt Duc der Tafel nahe, stellt sie sich davor und beginnt einen Technikstreit | rosi.txt:93 |
| Weiß (Karte) | Quoten auswendig, wer worauf setzt; sieht auf den Monitoren, dass die **Brückenbeleuchtung mehrmals pro Woche um 2 Uhr Strom zieht** (vermutet jemanden, nicht wen; nie mit der Geistergeschichte verbunden); weiß, dass **Lea den Tender nachts öfter rausfährt, als das Logbuch sagt** (vermutet einen Jungen); weiß **nicht**, dass Sophia Krimis schreibt oder Chiaras Job ablehnte; hält Influencer für nutzlos | rosi.txt:95 |
| Weiß (LB) | führt die Tafel (LB 9); schuldet Megan noch etwas für einen Wechselrichter aus Genua; wischt vor jeder Inspektion eine Spalte der Tafel weg, Megan hat die saubere Stelle bemerkt (LB 39); Lola hat nur ihr von ihrem Schwarm auf den neuen Offizier erzählt – am nächsten Morgen änderten sich die Quoten (LB 54) | LB 9, 39, 54 |
| Vorlieben / Geschenke | Grundhaltung: Essen +, Alkohol 0, **Schmuck –**, **Technik +**, **Papier –**, Natur 0, **Party +**, Intim 0 (geg_py:29). **Liebt**: Arancini vom Bäcker, Lolas Gewürzmischung „Ocean Glitter“, Profi-Drehmomentschlüssel, Cannoli mit Schraubenschlüssel-Keks, Unit-01-Muffins, **Ramen (Kochgericht = Lieblingsgericht; „kennt Ramen aus ihren Manga“)**. **Hasst**: rosa Perle, Duftkerzen „Maquis“, Pavlova. **Unikat**: Werkstattschild **„Scuderi & Figlie“** (Treibholz, von Petru geschnitzt, „Für die Werkstatt, die sie eines Tages haben will“) | gegenstaende.json; geg_py:90-113, 168, 325-342, 362 |
| Lieblingsorte | **Werkstatt (Bord), Petrus Bootswerkstatt (an Land)** | basis:495 |
| Beziehungen | **Duc**: „offizieller Rivale“ seit er in Woche 1 die Tender-Winde allein reparierte; Spalte „Reparaturen: Rosi vs Officer“. **Chiara**: nennt sie „Mole/Maulwurf“ (taucht nur zum Essen auf), will sie auf jeder Party aus dem Overall kriegen; gegenseitiger Respekt, Chiara fasst keinen Schalter ohne Rosi an, Rosi bewertet Chiaras Bewertungen auf 10 (LB 27); klopft als einzige Tür an Bord an der Technik (welt_rs:81); Revierstreit (ER gv_wer_fuehrt). **Sophia**: das „no sale“-Spiel, Laptop-Reparatur (LB 28). **Lea**: Lea folgt ihr, fragt, wie Batterien funktionieren; Rosi erklärt es ihr jedes Mal geduldig mit Zeichnungen; Leas Zeichnung von Unit-01 als Seeungeheuer hängt in der Werkstatt (LB 29); Streit um die Tender-Garage (ER br_tender_streit, gv_versoehnung). **Siri**: am 1. Tag „useless“; Siri bringt ihr seitdem jeden Morgen Kaffee, Rosi hat weder rausgeworfen noch gedankt (LB 33); Spannung rosi_siri Start 2 (basis:92). **Holm**: hört monatlich 2 Minuten dem Testlauf von Unit-01 zu, fasst nie einen Schalter in Rosis Reich an (LB 46). **Megan**: einzige, die nicht aufschaut, wenn Megan die Treppe runterkommt; Megan respektiert das (LB 39). **Lola**: die einzigen beiden, die mit ihrem Gerät reden; Lola bringt Teller in den Antriebsraum, kein Danke; „Rosi's partner in crime at night“ (LB 54, modul_py:137). **Totò**: Armdrücken, Pizza-Krieg Sizilien vs. Neapel; Engine: **Totò „runs the betting board“** (basis Totò-Beschreibung). **Petru**: Außenborder-Streit Hammer vs. Messgerät (ER gv_aussenborder); Schild-Kette (missionen.json petru_schild_1-3); Petrus Werkstatt ist mit ihr betretbar (basis:405). **Casanova**: Blaskapelle weckt sie (ER g1_blaskapelle). **Yasin, Alva, Elsa, Maxwell, Jana, Yamamoto**: keine Weltbuch-Einträge | rosi.txt, LB, ER |

---

## 3. Die Schwestern Sophia ↔ Lea (Schwerpunkt) – und was Sophia und Rosi verbindet

### 3.1 Familie und Herkunft
| Fakt | Quelle |
|---|---|
| Beide aus **Falmouth, Cornwall**. Mutter: liebe, chaotische Malerin, verkaufte **Seestücke** am Hafenmarkt, vergaß die Miete (Präsens → lebt). **Vater: in keiner Quelle erwähnt.** | sophia.txt:6; lea.txt:6, 90; LB 17 |
| **Altersabstand 5 Jahre**: Sophia 28, Lea 23. Sophia zog Lea „ab vierzehn“ groß (Sophias Alter) = „ab neun“ (Leas Alter) → konsistent | sophia.txt:5-6; lea.txt:5-6; LB 17, LB 20 |
| **Großvater Jack Moore**, kornischer Fischer, brachte Lea das Meer bei, erzählte ihr von der **Margot** (Schoner, 1924 vor dem Esterel gesunken, Geldkassette nie gefunden). **Letzten Winter gestorben.** Seine handgezeichnete Karte liegt auf **Seite 40** von Leas Logbuch. LB 23: „Sophia and Lea's grandad, always swore he knew roughly where she lay“ | lea.txt:6, 90, 92; LB 23 |
| Sophias Karte erwähnt den Großvater nur indirekt („grandad's wreck“), keine Trauer, keine eigene Erinnerung an ihn | sophia.txt:89 |
| „We never had money. We always had the best table in Falmouth.“ – Sophias Kindheitsformel. Lea: „That's bigger than our kitchen. In Falmouth. The whole kitchen.“ (Casino) | sophia.txt:6; lea.txt:47 |
| Morgenschwimmen nackt ist bei Sophia „a Falmouth habit“; Lea taucht nachts allein und kommt nackt aus dem Neopren | sophia.txt:57; lea.txt:62 |
| Leas Lebensziel-Kern (Duc bestätigt): **die Margot liegt in der Bucht vor der Punta d'Orsu**; gefunden → Unterwasser-Kulturerbe/Schutzgebiet → Hebel gegen Alons Resort. Bucht verloren + Bogen → Azoren-Walforschung (bittersüß) | LeaD „Kernidee“; Übergabe:112 |

### 3.2 Wer beschützt wen
- **Sophia → Lea (bemuttern):** „She still mothers her: food, sun cream, opinions about bikinis. Lea wants to prove she
  doesn't need any of it, and it shows.“ (LB 17). Sophia hat Lea **diese Saison den Job als Decksfrau besorgt**
  (sophia.txt:8, 85; lea.txt:8; LB 8). Sophia „did her hair“ fürs Casino und hat die Crew reingebracht, dann
  „vanished“ (lea.txt:47). Leopardenbikini mit Sophia gekauft: „Sophia says it's very Riviera“ (lea.txt:57).
- **Lea → Sophia (schützt durch Schweigen):** Leas Azoren-Bewerbung bleibt geheim, „because it means leaving her alone“
  (lea.txt:92). Leas Mission **„Ein Füller für Sophia“**: sie will ihr einen Füller mit ihrem eigenen Namen gravieren
  lassen, „für das, was Sophia nur für sich schreibt“; am Ende: „Du gibst ihn ihr. Ich würde heulen.“
  (missionen.json lea_fueller_1/2; miss_py:289-303) → Ergebnis Sophias Unikat `sophia_fueller`.
- **Angst voreinander:** Lea beim verbotenen Nachttauchen: „He'll send me home and Sophia will kill me.“ (lea.txt:62).
- **Chiara als Dritte:** LB 12 (aktiv): Chiara hat Lea als „Küken“ adoptiert, strenger zu ihr als zu allen.
  LB 15 [alt, aus]: „the day Lea falls, **Sophia's word falls with her**“ – Schutz als Disziplin, weil Sophia für Lea
  gebürgt hat.
- **LB 19 [alt, aus, Head-Chef-Fassung]:** „Sophia **signed for her sister** and has never once held it over her, which
  Lea hates more than a reproach would be … reads it as the old **Plymouth** temper … She is **leaving in October** and
  has not found a sentence for it, so she puts another plate in front of her instead.“ (Bürgschaft + Abschied, aber
  falsche Stadt und alte Rolle.)

### 3.3 Was die eine über die andere weiß oder verschweigt
| | weiß | weiß nicht / falsch |
|---|---|---|
| **Sophia über Lea** | Lea sucht noch Opas Wrack bei ihren Tauchgängen – **findet es „süß“** (sophia.txt:89) | **Azoren-Bewerbung** (sophia.txt:89); dass Lea allein nachts taucht (nicht erwähnt) |
| **Lea über Sophia** | Sophia schreibt nachts – **glaubt, es seien Liebesbriefe** (lea.txt:94); in der Füller-Mission weiß Lea, dass Sophia „nur für sich“ schreibt (missionen.json lea_fueller_1) | **Krimis/Pseudonym**, das **abgelehnte Jobangebot** (lea.txt:94); Wett-Tafel hält sie für einen „Angelwettbewerb“ (lea.txt:94; LB 9) |
| **beide über Chiara** | – | beide wissen nicht von Chiaras Prüfung (sophia.txt:89; lea.txt:94) |
| **Kränkung** | Lea: „Nobody believes me. **Sophia thinks it's sweet. Sweet.**“ – dann gesteht sie Duc die Azoren: „I haven't told her.“ (lea.txt:79) | Leas Motor fällt, wenn Duc **Sophia erzählt, was Lea ihm anvertraut hat** (lea.txt:99) |
| **Wett-Tafel** | Beide Schwestern stehen auf der Tafel „wer landet beim neuen Ersten Offizier“ (Chiara, Sophia, Lea). Sophia kennt die Quoten und hat 20 € auf sich gesetzt; Lea ahnt nichts (LB 9; sophia.txt:89) | – |

### 3.4 Gemeinsame Szenen, Events, Missionen
- **Karten:** In Sophias Karte keine Begrüßung mit Lea. In Leas Karte: Casino Night (Sophia brachte Crew rein, machte
  Lea die Haare, verschwand; lea.txt:47), New Bikini (mit Sophia gekauft; lea.txt:57), Night Dive („Sophia will kill
  me“; lea.txt:62), mes_example Azoren-Geständnis (lea.txt:79).
- **Story (7 Tage):** T1 `auftakt_party`: „**Sophia setzt unauffällig Lea und Rosi auseinander**“ (story.json
  wochenbogen.1; story_py:221-224) – einziger Story-Moment, in dem Sophia gezielt auf Lea reagiert. Danach keine
  gemeinsame Fix-Szene. In buehne.json ist Sophia in **keiner** Szene `anwesend`.
- **Totes Storylet:** `alvas_bar` (Abend, Sophia + Lea, ab Tag 2: „Evening in the village bar. Alva knows things, and
  sells diesel under the counter“) – basis:512-514; durch `storylets: {}` (modul_py:45) abgeschaltet.
- **Events mit beiden (nie als Schwestern geschrieben):**
  `br_nacktbaden` (Sophia trägt amüsiert vor, dass Lea + Siri nackt baden waren und Elsas Scheinwerfer sie traf; Lea:
  „It was romantic! The plankton was glowing!“) · `g1_sophia_tischordnung` (Sophia setzt Duc zwischen Chiara und Lea –
  „zwei Frauen, die sich nicht ausstehen können, wenn es um ihn geht“; Erfolg „charmant in beide Richtungen“ +V Chiara,
  Lea, Sophia) · `br_drei_minuten` (Sophia spricht; Option „Lea baut eine Salzwasserdusche“) · `br_yasins_angebot`
  (Sophia spricht; „Nur wer will“ → Lea +4) · `gv_sonnencreme`, `gv_knoten` (Lea im Duell, Sophia schaut zu) ·
  `g1_yasin_geste`, `g1_chiara_pause`, `gv_siri_yasin`, `gv_festa_kleid`, `gv_festa_outfits`, `gv_wer_fuehrt`,
  `gv_wahrheit_pflicht`, `du_poetry_sophia`, `gv_quiz`, `auf_gitarre`, `auf_herkunft` (beide nur Zuschauerinnen).
- **ereignisse.json enthält kein einziges Mal „Schwester“, „sister“, „Falmouth“, „Penrose“ oder „Jack Moore“**
  (Volltextsuche).
- **Missionen:** nur `lea_fueller_1/2` (Lea → Sophia). Keine Sophia-Mission für Lea.

### 3.5 Weltbuch-Einträge über beide
LB 8 (Leas erste Saison, Sophia besorgte den Job) · **LB 17 „Sophia ↔ Lea (sisters)“** (aktiv, s. o.) · LB 19 [alt,
aus] „the name on the guarantee“ · LB 20 (Lea: „Sophia's little sister, from Falmouth“) · LB 23 (Margot, „Sophia and
Lea's grandad“) · LB 9 (beide auf der Wett-Tafel) · LB 15 [alt, aus] (Chiara: Sophias Wort fällt mit Lea). Die
eingebetteten Bücher der Karten-JSONs tragen dieselben Einträge 17 und 19 (19 deaktiviert).

### 3.6 Konflikte und Zärtlichkeiten
- **Konflikte (Quellen):** Lea will beweisen, dass sie Sophias Fürsorge nicht braucht (LB 17); „Sophia thinks it's
  sweet“ als Kränkung (lea.txt:79); gegenseitige Geheimnisse (Azoren / Bücher / Jobangebot); beide Kandidatinnen auf
  derselben Wett-Tafel um Duc (LB 9); `g1_sophia_tischordnung` setzt Lea neben Duc gegen Chiara.
- **Zärtlichkeiten (Quellen):** Haare fürs Casino, Bikini-Kauf (lea.txt:47, 57); Essen, Sonnencreme (LB 17); Leas
  Füller-Geschenk „Ich würde heulen“ (lea_fueller_2); LB 19 [aus]: Sophia stellt ihr einen Teller hin statt eines
  Abschiedssatzes.

### 3.7 Gegenstände / Erbstücke
| Gegenstand | Bezug | Quelle |
|---|---|---|
| **Opas handgezeichnete Margot-Karte** (Logbuch S. 40) | Familienerbe, nur bei Lea | lea.txt:6, 92 |
| Leas Logbuch (zeichnet jeden Fisch) · Mutter malt Seestücke | beide Fakten ohne verknüpfende Quelle | LB 20; sophia.txt:6 |
| `sophia_fueller` „Füller mit ihrem eigenen Namen“ (Unikat) | Leas Geschenk über Duc | geg_py:170; lea_fueller_2 |
| `lea_shell` „Leas Muschel von der Margot“ (Andenken, Empathy +1) · `lea_muschelkette` | Margot | basis:266; geg_py:312 |
| `sophia_page` „Eine Seite aus Sophias Notizbuch“ (Andenken, Charm +1: „Wer in Cala d'Orsu wem einen Gefallen schuldet“) | Sophias Notizbuch | basis:262; gegenstaende.json |
| Sophias goldene Kette mit kleinem Anker (Writing Night) | Seemanns-Motiv, keine Herkunft angegeben | sophia.txt:52 |
| Altbestand basis: Seekarte „Von 1931. Mit Wracks eingezeichnet“ – Geschenk lea 2, sophia 1 | ungenutzte Liste | basis:295 |

### 3.8 Leas Fall-Rolle (offen, laut Übergabe Pilotfigur)
Fall 2 „Die Strecke, die nicht im Plan stand“: Holm gibt Lea die Routenplanung als Übung; sie legt WP4 auf das
Margot-Suchgebiet (Koordinaten von Petru), rechnet die Mehrstrecke klein; Duc zeichnet 17:40 ab; Autopilot hält
Zielzeit → LM3 fällt 06:35 aus. Motiv Trauer („Ich dachte, wenn ich es wirklich finde, ist es nicht mehr nur eine
Geschichte von ihm.“). In den anderen Fällen Alibi mit Siri 02:00–03:30 (LeaD; faelle_py:423-535). **Sophia kommt in
Fall 2 nicht vor.** (Sophias eigene Fall-Rolle → VERDECKT.)

### 3.9 Sophia ↔ Rosi (Verbindungen)
- LB 28 „no sale“: Sophia konnte Rosi nie etwas verkaufen – tägliches Spiel; Rosi reparierte ihr nachts den Laptop,
  ohne hineinzusehen (das Gerät, auf dem Sophia schreibt, sophia.txt:52).
- Wett-Tafel: Rosi führt sie, Sophia kennt die Quoten, beide haben auf sich selbst gesetzt (20 € bzw. 50 € zu 40:1)
  (rosi.txt:93; sophia.txt:89).
- Rosi weiß nicht, dass Sophia Krimis schreibt (rosi.txt:95). Sophia: Technik-Geschenke „–“ (geg_py:27); welt_rs:84:
  Technik ist „the one place her charm doesn't work. She comes down with a coffee and an excuse and leaves without either.“
- Events: `br_rosi_ueberstunden` (Sophia trägt vor, dass Rosi im Stehen einschlief), `br_lola_flach` (Rosi will Strom
  sparen, Sophia will „Yacht-Niveau“), `br_lola_krank`, `g1_sophia_tischordnung` (Rosi „ganz am Ende, neben dem
  Brotkorb“), `g1_sophia_liest_vor` (Rosi „will mehr hören“), `gv_festa_outfits` (Sophias Weg → Rosi +4),
  `gv_megan_sophia`, `gv_karaoke`, `gv_tarot`, `gv_wahrheit_pflicht`, `g1_megan_schach`, `g1_katerfruehstueck`.
- Story T1: Sophia setzt Lea und Rosi auseinander (s. o.); Lea ↔ Rosi haben eigene Rivalität (Tender-Garage,
  Wettschwimmen, Wasserschlacht) und Zuneigung (Batterien, Seeungeheuer-Zeichnung, LB 29).
- Totes Storylet `power_council` (Chiara, Rosi, Sophia; Strom-Verteilung beim Dinner, basis:508).

### 3.10 Ansatzpunkte für engere Verwebung (nur Fakten aus den Quellen)
1. Gemeinsamer Großvater Jack Moore + Margot: LB 23 nennt ihn ausdrücklich „Sophia and Lea's grandad“; Sophias Karte
   enthält keine eigene Beziehung zu ihm, Leas Karte schon (lea.txt:6, 90).
2. Leas Lebensziel-Kern (Margot rettet die Bucht) ist entschieden (LeaD); Sophia hält Leas Wracksuche für „süß“
   (sophia.txt:89) – Leas stärkste Kränkung (lea.txt:79).
3. Doppelte Geheimhaltung: Lea verschweigt die Azoren „weil sie Sophia dann allein ließe“ (lea.txt:92); Sophia
   verschweigt Bücher und Jobangebot (sophia.txt:87); Lea hält die Bücher für Liebesbriefe (lea.txt:94).
4. Leas Füller-Mission ist die einzige vorhandene Brücke zwischen den Schwestern in der Engine (lea_fueller_1/2) und
   ergibt Sophias Unikat; die Gravur „Sophia Moore, nicht irgendein anderer Name“ zielt auf das Pseudonym (geg_py:170).
5. Sophia hat Lea den Job besorgt (LB 8) und – nur im deaktivierten LB 19 – für sie gebürgt; Chiara bewacht Lea, weil
   „Sophia's word falls with her“ (LB 15, aus).
6. Beide stehen auf derselben Wett-Tafel um Duc (LB 9); `g1_sophia_tischordnung` setzt Lea neben Duc.
7. Story T1: „Sophia setzt unauffällig Lea und Rosi auseinander“ – unerklärter Moment (story.json wochenbogen.1).
8. Übergabe Orts-Regel (4): im Cold Open rettet Maxwell **Totò und Lea** vor den Trümmern (Übergabe:146) – Sophias
   Reaktion darauf ist nirgends beschrieben.
9. Mutter malt Seestücke (sophia.txt:6), Lea zeichnet jeden Fisch ins Logbuch (LB 20) – beides belegt, nicht verknüpft.
10. Totes Storylet `alvas_bar` mit Sophia + Lea (basis:512) und Sophias Lieblingsort Alvas Bar (basis:494).
11. Übergabe: „Siri = Wissenschaft und Stimme, Lea = Staunen und Geschichte“; Content-Tauchgang Lea + Siri in Akt 2
    (Übergabe:178, 184) – Sophia organisiert Siris Landgänge (LB 31).
12. Ende-Regel: „Keine garantierte Buchveröffentlichung … ohne etablierte Voraussetzungen“ (story.json ende.regel) –
    gilt für Sophias Wunsch „Name auf dem Buchrücken“.

---

## 4. Mechaniken je Figur

### Sophia
- **Romanzierbar** (basis:435; Übergabe Thema 4). Vertrauen Start **1**, Begehren Start **2** (basis:89-91).
- Schätzt **Perception + Cunning**. Lieblingsgesten **Necken, Geheimnis, Einladen** (+2) (basis:219).
- Intim-Vorlieben: mag Lotus, Anal, Face-Sitting, Edging; **nein: –** (keine Grenze) (basis:229). Karten-Kinks: Wetten
  mit körperlichen Pfändern, durchschaut werden, langsames Ausziehen als Spiel, „einmal macht jemand anderes den Plan“,
  Rolle nur für einen Menschen, Hände in ihrem hochgesteckten Haar (sophia.txt:98).
- Karten-Hitze 1 charmant/Wetten → 2 Show rutscht → 3 bietet das Pfand selbst an → 4 keine Show, Brille ab, Tür zu →
  5 ohne Charme gesehen. Motor: Trick durchschauen und bleiben, Wette fair gewinnen, fragen, was sie will, und warten
  (sophia.txt:91-94).
- Spannung chiara_sophia Start 1 (basis:92).
- **Missionen**: `sophia_papers` Papiere zur Küstenwache (T2–6, Charm SG 10, Ruf +1) → `sophia_diesel` Diesel-Gefallen
  (T3–7, Charm SG 12, ab V2, Diesel +1) → `sophia_kapitel` **Sophias erstes Kapitel** (T4–7, Empathy SG 13, persönlich:
  ehrliche Meinung zu 12 Seiten „nicht für einen Verlag“; Schmeichelei = nie wieder eine Zeile) (miss_py:138-141, 388).
  Fremde Mission für sie: `lea_fueller_1/2`.
- **Gegenstände**: Andenken `sophia_page` (Charm +1), Attribut `sophias_lesezeichen` (Empathy +1, Quelle „mission“ –
  **keine Mission vergibt es**, Volltextsuche), Unikat `sophia_fueller`, Kampf-Anhänger **Plüsch-Eule** (Wahrnehmung +1,
  kampf.md:254). Beweisstück-Altbestand `paris_call` (basis:372).
- **Handy**: `hy_sophia_0213` (V≥3, liest nachts vor, was sie über ihn schrieb; Intim-Option), `hy_sophia_kaffee`
  (schickt Duc zu Chiara).
- **Läden**: keine Verkäuferin. **Vorteile/Job-Zeilen**: Angebot/Erfolg/Fehlschlag/Patzer (basis:618ff.; u. a.
  „You'd make a decent villain in one of my books“, „I'm keeping notes, you know“).
- **Epilog 7 Tage** (kern/abschluss.py:187-192): partner „schenkt dir das erste Kapitel“, hoch „schreibe jetzt doch das
  Buch“, mitte „Notizbuch voller“, tief „schon weg“.
- **Totes Material**: Storylets `sophia_village` → `sophia_favours` (V2) → `sophia_manuscript` „M. J. Penrose“ (V4)
  (basis:543-550) – der einzige Ort, an dem das Pseudonym in der Engine vorkam.

### Rosi
- **Romanzierbar** (basis:448; Übergabe Thema 4). Vertrauen Start **1**, Begehren Start **1**. `technik: true`
  (modul_py:328).
- Schätzt **Cunning + Courage**. Lieblingsgesten **Zeit, Necken, Entschuldigen** (basis:218).
- Intim: mag Cowgirl, Reverse Cowgirl, Grinding, Against the Wall; **nein: Spanking** (basis:225). Karten-Kinks: Duell
  verlieren, das sie verlieren wollte; geschickte Hände; Fett, Hitze, Generatorbrummen; körperliche Pfänder; an den
  Handgelenken gehalten und weiterstreiten; leises Lob, nie vor der Crew (rosi.txt:104).
- Karten-Hitze 1 Rivalität → 2 neben ihm arbeiten, kurz nicht zählen → 3 körperliche Pfänder, bleibt nach der
  Reparatur → 4 „unentschieden“ hinter der Generatorraum-Tür → 5 alles, danach „war ein Duell“ (rosi.txt:97-100).
- **ST-Spieltisch-Bogen** (welt_rs:148-191): Achsen Nähe (Start 1), Werkstatt (1, „wie viel Catania sie zeigt“),
  **Duell (Start 6, sinkt, bei 1 bittet sie laut um Hilfe)**; Nachwirkung: nennt ihm den Namen der Werkstatt, neue
  leere Spalte auf dem Whiteboard.
- **Raum-Zugang**: Generatorraum nur ab V2 Rosi / in Begleitung / Cunning 13 mit Risiko (Rosi V–1); Werkstatt ab V1 /
  Begleitung; Petrus Werkstatt u. a. mit Rosi als Begleitung (basis:394-405).
- **Werte-Bezug**: Strom (0–10), Uhr **Reparatur** (8 Segmente „läuft wieder aus eigener Kraft“), Uhr Katastrophe
  (verdeckt, „Batteriebank brennt“) (basis:94-104); Yachtware-Strafe Ersatzpropeller → Vertrauen.rosi –2 (basis:160).
- **Missionen**: `rosi_cells` Zellen durchmessen (T2–7, Perception SG 11, reparatur, Strom +1) → `rosi_bleed` Unit-01
  entlüften (T3–7, Cunning SG 12, ab V2, Reparatur-Uhr +1) · `rosi_ersatzbatterie` (T3–7, braucht Ersatzzellen von
  Totò, Strom +2) · `rosi_arancini` **Arancini wie bei Nonna** (T3–7, Perception SG 12, Kochen, persönlich) · Petru-Kette
  `petru_schild_1-3` → Unikat „Scuderi & Figlie“ („Du gibst es ihr. Von mir nimmt sie nichts an.“) (miss_py:82, 125-128,
  190-206, 381).
- **Gegenstände**: Andenken `rosi_spanner` „Papas Ringschlüssel“ (Cunning +1, „Rosi hat ihn dir geliehen – sagt sie“),
  `rosis_foto` (aus hy_rosi_foto, „im Epilog sichtbar“), Attribut `rosis_handschuhe` (Cunning +1, Quelle „event“ –
  **kein Event vergibt sie**), `ersatzteilkiste` („Rosi strahlt“, Reparatur-Uhr +1), `ersatzzellen`. Kampf: **Rosis
  brennendes Schwert** (Episch, 9, Feuer, Gastank im Griff), **Werkstatt Rosi**: Upgrades +1/+2/+3, Veredeln; „Rosi zieht
  eine Waffe eine Stufe hoch“ (kampf.md:156, 222, 324). Crafting-Material für „Rosis Werkstatt“
  (tage_erkundung.md:39, 66).
- **Handy**: `hy_rosi_foto` (B≥2, Handtuch-Selfie statt Ersatzteil). Fremde: `hy_megan_rundgang` (Rosi bei der Arbeit
  zeigen), `hy_lola_koster` (Rosi schicken).
- **Gags**: Kette `rosi_vs_unit01` (4 Stufen; g1_unit01_klonk → g1_unit01_staendchen) (ER gags).
- **Duell**: `du_reparatur_rosi` (Lolas Mixer; „Zusammen schrauben“ → Moment `zusammen_geschraubt`).
- **Job-Zeilen** (basis:586ff.), Epilog 7 Tage (kern/abschluss.py:198-203: partner Öl am Hemd „Jetzt gehörst du zum
  Maschinenraum“, hoch Name mit Kreide auf dem Umrichter).
- **Story-Mechanik neutral**: Warnungen „⚠ Rosi meldet: Das Umrichtergehäuse ist warm …“ (kern/ermittlung.py:538);
  Ermittlungsweg `route_rosi` (Rosi fragt beim Hersteller nach, Antwort ab T5 nacht; story_py:161-164;
  kern/ermittlung.py:613).
- **Totes Material**: Storylets `rosi_diagnose` → `rosi_night_shift` (V2) → `rosi_workshop_name` (V4)
  (basis:516-523).

## 5. Events je Figur (module/eden_rise/ereignisse.json)

### Sophia (Hauptrolle / Sprecherin)
| id | Tage/Phase | Kern |
|---|---|---|
| hy_sophia_0213 | T3–7 Nacht, V≥3 | Videoanruf 02:13, liest vor, was sie über ihn schrieb („He listens like it costs him nothing …“); Intim-Option, Moment `night_call` |
| hy_sophia_kaffee | T2–6 Frühstück/Tag | Nachricht: Chiara sitzt allein vor einer Tasse – „bring ihr Kaffee“ |
| g1_sophia_tischordnung | T2–6 Dinner | Tischkarten: Duc zwischen Chiara und Lea, Rosi am Ende; „Research. For a book. You're my favourite chapter.“ |
| g1_sophia_liest_vor | T3–6 Abend | liest der Crew eine **Liebesszene** aus ihrem Notizbuch vor (strenge Offizierin + Erster Offizier, gestrandete Yacht); Chiara: „Why does the officer have my haircut.“ |
| du_poetry_sophia | T3–7 Abend | Poetry Slam „Ode an Lolas Kühlschrank“, Charme-Duell |
| gv_megan_sophia | T5–6 Tag, Megan an Bord | verhandelt freien Nachmittag mit Megan |
| gv_festa_outfits | T4–5 Tag | Chiara (weiße Hemden) vs. Sophia (jede, wie sie will) |
| gv_festa_platz | T5 Abend, V Siri ≥3 | Siri vs. Sophia um den Stuhl neben Duc |
| gv_karaoke | T2–6 Abend | Chansons gegen Lolas Pub-Lieder |
| gv_tarot | T3–7 Abend/Nacht | Lola legt ihr „Die Liebenden“, zeigt auf Duc |
| gv_wahrheit_pflicht | T3–7 Nacht | Sophia + Lola stellen die Aufgabe |
| gv_strip_poker | T4–7 Abend, an Land, V Alva ≥3 | Poker gegen Alva um einen Kanister, Sophia fehlt die Bluse |
| Bordrat (Sprecherin) | br_drei_minuten (T2–5), br_yasins_angebot (T2–5), br_elsas_kontrolle (T2–6), br_crew_kasse (T3–6), br_ein_tisch (T2–5), br_nacktbaden (T2–6), br_rosi_ueberstunden (T3–6), br_siri_umzug (T2–6), br_investoren_dinner (T5) | trägt die Lage vor |
| Bordrat (Nebenstimme) | br_gaestekabinen („Halb machen, wie Sophia sagt“ V+6), br_siris_geburtstag („Sophias Frühstück, ohne Kameras“), br_lola_krank, br_lola_flach, br_poker_einladung („Sophia hat zufällig ein Kartenspiel“) | |
| Betroffen/Zuschauerin | g1_yasin_geste („beobachtet genau“), g1_chiara_pause, g1_siri_pullover („sieht alles“), g1_megan_schach („wettet auf Duc“), g1_katerfruehstueck, gv_sonnencreme, gv_wer_fuehrt, gv_siri_yasin, gv_festa_kleid, gv_knoten, gv_zigarren, gv_megan_chiara, gv_quiz, du_koch_alva, auf_gitarre, auf_herkunft | |

### Rosi (Hauptrolle / Sprecherin)
| id | Tage/Phase | Kern |
|---|---|---|
| br_lolas_notvorrat | T2 Nacht | findet Lolas Gras („BASIL ♥“) beim Ausräumen für den Strom: „Holm's gone, so it's your crew now“ |
| br_festa_auftritt | T3–4 Nacht | Casanovas Brief: Crew in Matrosenkostümen auf die Festa-Bühne; Rosi lacht |
| br_kevin_nest | T3–7 Nacht | Möwe Kevin nistet auf einem Solarpaneel |
| br_ehrenbuerger | T3–5 Nacht | Duc soll Ehrenbürger werden, Rosi hat ein Foto der Muschelkrone |
| br_rosi_ueberstunden | T3–6 Nacht (Sophia spricht) | >16 h/Tag, im Stehen eingeschlafen; Versprechen „Ich übernehme deine Spätschicht“ |
| br_megan_kommt | T4 Nacht | Rosi will Megan mit einem Schild zeigen, wie kaputt alles ist |
| br_tender_streit | T2–6 Nacht | Lea vs. Rosi um die Tender-Garage → Flag lea_rosi_streit |
| br_nachtwache | T2–6 Nacht | Rosi übermüdet vs. Lea meldet sich |
| br_petrus_boot, br_netze_flicken, br_letzte_steaks, br_lola_krank (Schürze!), br_lola_flach (kalte Küche, Strom sparen) | T2–6 | Nebenstimme |
| hy_rosi_foto | T3–7 Abend/Nacht, B≥2 | Handtuch-Selfie statt Ersatzteilfoto |
| g1_unit01_klonk → g1_unit01_staendchen | T2–5 / T3–7 | Ringschlüssel-Klonk, Rußwolke in die Kombüse → sizilianisches Wiegenlied für Unit-01 |
| g1_reissverschluss | T3–7, B≥3 | Overall-Reißverschluss verhakt in der Serviceklappe |
| g1_kalte_dusche | T2–6 | dreht Warmwasser ab, Siri schreit |
| du_reparatur_rosi | T2–7 Tag | Reparatur-Duell um Lolas Mixer |
| gv_wer_fuehrt | T2–6 Tag | Revierstreit mit Chiara um Leute unter Deck |
| gv_armdruecken | T2–6 Abend | gegen Totò |
| gv_wettschwimmen, gv_wasserschlacht, gv_versoehnung | T2–7 | mit/gegen Lea (Versöhnungskuchen nach lea_rosi_streit) |
| gv_aussenborder | T2–6, V Petru ≥2 | Hammer (Petru) vs. Messgerät (Rosi) |
| Betroffen/Zuschauerin | g1_pfannkuchen („ihres ist wunderschön“), g1_blaskapelle („Kopfweh“), g1_lola_yoga, g1_siri_tanz („zwei linke Füße“), g1_toto_pizza (Sizilien vs. Neapel), g1_chiara_tender, g1_sophia_tischordnung, g1_sophia_liest_vor, g1_lola_massage, g1_megan_schach, g1_katerfruehstueck, gv_ocean_glitter, gv_kevin_auktion, gv_arancini_duell, gv_megan_sophia, gv_karaoke, gv_festa_platz, gv_oktopus, gv_tarot, gv_keks, gv_wahrheit_pflicht, gv_festa_outfits, gv_angeln, gv_quiz, du_koch_lola, du_koch_toto („verteilt Gabeln wie Waffen“), du_poetry_sophia, auf_gitarre, auf_herkunft; erwähnt in hy_megan_rundgang, hy_lola_koster, hy_koeln_frist, ab_lola_handy | |

## 6. Story-Rolle im Wochenbogen (7-Tage-Fassung, neutral)

### Sophia
- **T1 Abend `auftakt_party`** (Achterdeck): anwesend; Moment „setzt unauffällig Lea und Rosi auseinander“. Nicht unter
  den drei „Wem hilfst du?“-Optionen (Chiara/Rosi/Siri).
- **T2 Frühstück `lage_mit_holm`** (Brücke): Sophia übermittelt „die Nachricht der Gesellschaft“ (story.json); buehne_py
  will: „Pass on the company's message without starting a panic.“ – aber in buehne.json `anwesend` nur Holm/Rosi/Chiara.
- **Danach keine Fix-Szene mehr.** T5 Megan an Bord: nur Events (gv_megan_sophia, br_investoren_dinner). T7 `zukunft`:
  generisch für alle Romanzen.

### Rosi (die Story-Figur mit den meisten Fix-Auftritten)
- **T1 Abend `auftakt_party`**: Wahl „Rosi braucht jemanden für einen Test im Kontrollraum“ → Flag
  `auftakt_hilfe_rosi`, V+2, sie erinnert sich konkret (buehne_py:47-54); Moment „Unit-01 = der einzige Gast, der seinen
  Strom selbst mitbringt“.
- **T2 Frühstück `lage_mit_holm`**: erklärt die Beschränkung (Antrieb aus, Hotel im Inselbetrieb). **T2 Tag
  `erste_ermittlung`** im Antriebsraum („Understand her machine and not be told how to do her job“). **T2 Nacht
  `gemeinsames_essen`** (mit Lola, Lea).
- **T3** `sturmvorbereitung` („Save every amp“) und `sturmnacht` („Keep the power alive“).
- **T4 Abend `reparaturschritt`** (Antriebsraum, 18:00).
- **T5 Tag `megan_inspektion`** (Antriebsraum, Rosi „refuses to stand to attention“).
- **T6** `technischer_weg` (13:00, reparieren/schleppen/abtrennen) und ggf. `brand` (02:10, „Fight it as long as it
  makes sense“).
- **T7** `auslaufen` (Brücke, „See her work hold – or let go of it“), `schlussbild` (letztes Essen).
- Ermittlungsweg `route_rosi` (Herstelleranfrage, ab T2–3 eröffnet, Antwort T5 nacht).

(Fall-Bezogenes zu beiden → VERDECKT.)

---

## 7. Widersprüche, 7-Tage-Reste, Passung zur neuen Prämisse

### Widersprüche
1. **Sophias Rolle**: Concierge (Karte, LB 16, Engine) vs. **Head Chef, 5. Saison, Kopenhagen, „leaving in October“**
   (LB 18/19, deaktiviert, aber noch in beiden Karten-JSON-Büchern) + PS-Set `Yacht_Sophia|Galley` mit `sophia_chef_whites`.
2. **Herkunft**: Falmouth (überall) vs. „the old **Plymouth** temper“ (LB 19, aus).
3. **Sophias Schreiben**: Karte = **gemütliche Krimis**, Pseudonym **M. J. Penrose**, **14 Absagen**, absolutes
   Geheimnis (Motor fällt, wenn erwähnt) vs. Engine: `g1_sophia_liest_vor` liest **vor der ganzen Crew eine Liebesszene**
   aus dem Notizbuch; Job-Zeile „villain in one of my books“ öffentlich; `sophia_kapitel` „nicht für einen Verlag“;
   Falldaten: Pariser Lektorin/Manuskript (Details VERDECKT). Das Pseudonym kommt in der aktiven Engine nirgends vor
   (nur im toten Storylet). Lea glaubt an Liebesbriefe (lea.txt:94), weiß aber in ihrer Mission, dass Sophia „für sich“
   schreibt.
4. **Notizbuch**: Karte „Never tells anyone what is in the notebook“; Karte: Notizbuch = Gefallen/Schulden, Schreiben
   am Laptop – Engine `g1_sophia_liest_vor` liest Prosa aus dem **Notizbuch**.
5. **Jobangebot**: Karte „**Chiaras** Job als Chefstewardess“ vs. LB 41 „Chief Stewardess **on a bigger boat**“.
   LB 41 „Megan hat es niemandem erzählt, nicht einmal Holm“ vs. LB 48 „Dass Sophia letzten Winter ein Angebot hatte und
   blieb, liest Holm als Loyalität“ (Holm weiß es also).
6. **Stimmen**: Sophia Engine „Cora“ / Karte „Sophia Moore“ / basis ElevenLabs-ID; Rosi Engine „Rosi Scuderi“ / Karte
   ohne Stimme; Lea Engine „Chiara Nue“ (= Chiaras DE-Kartenstimme) / Karte „Young Adventurer“.
7. **PS-Kopierreste**: Sophia und Rosi tragen im base_prompt „Subject: **Leax**“ (Leas Trigger), Rosi „blue eyes“/„light
   blue eyes“ statt graugrün, Rosi ref_image = **Lea (5).png**.
8. **Rosis Outfits**: Off Duty, Crew Party und Festa im PS weichen stark von den Kartenbeschreibungen ab; Festa-Kleid mit
   **Stilettos** (die Kartenprüfung karten_rs:56 verbietet Heels).
9. **Rosi und Italienisch**: Karte „keine eingestreuten italienischen Wörter“ vs. Job-Zeilen „Brava“, „Grazie“,
   „Madonna“, „capito?“.
10. **Wer führt die Wett-Tafel?** Karte/LB 9: Rosi (bzw. „the engineers“) vs. Engine-Beschreibung Totò „Runs the betting
    board in the engine room“; Story: Totòs eigenes Wettbuch „Ankunft Calvi“. Außerdem: „die Maschinisten“ im Plural
    (LB 9, chiara.txt, lea.txt), aber Rosi ist die einzige Technikerin im Cast.
11. **Rosi = „Maschinistin“?** Karte/Engine: ETO für Solar/Batterie/E-Antrieb; einziger Verbrenner ist Unit-01. Die
    Prämisse sagt „Motorschaden/Explosion“ – im Code ist es das Leistungsmodul LM3 (PX-480) des E-Antriebs.
12. **Gegenstände ohne Quelle**: `sophias_lesezeichen` (mission) und `rosis_handschuhe` (event) werden von keiner
    Mission/keinem Event vergeben.
13. **Embedded-Weltbuch veraltet**: Karten-JSON-Bücher haben 24 Einträge (Holm 56, keine Rosi-/Megan-/Lola-Einträge),
    ST-Weltbuch 72.
14. **Rosis Familie**: Karte erwähnt keine Nonna; Mission `rosi_arancini`: Nonna letzten Winter gestorben (wie Leas Opa).
15. **Sophia nicht anwesend**: story.json `lage_mit_holm` nennt Sophia als Sprecherin, buehne.json führt sie nicht in
    `anwesend`.

### 7-Tage-Reste (für 21 Tage umzubauen)
- Karten-Setting beider: Antibes, Mitte August, „noch acht Wochen Saison“, Charter jede zweite Woche (sophia.txt:22,
  rosi.txt:23); Engine: Saisonende, Werft Calvi „bis Sonntag“ (modul_py ziel); neue Prämisse: Sommer, 21 Tage bis Festa.
- Fenster: Sophia-Missionen T2–7 (`sophia_kapitel` T4–7), `hy_sophia_0213` T3–7; Festa-Events T4–5
  (`gv_festa_outfits`, `gv_festa_platz` **T5**, `br_festa_auftritt` T3–4, `br_ehrenbuerger` T3–5); Megan-Events T5–6;
  `br_megan_kommt` T4; `br_lolas_notvorrat` T2.
- Rosi-Takt: Reparaturschritt T4, Inspektion T5, technischer Weg/Brand T6, Auslaufen T7; Uhr Reparatur 8 Segmente;
  `route_rosi` liefert T5; Epiloge „vor einer Woche“ (kern/abschluss.py).
- „Vier weitere Saisons“ bis zum Werkstatt-Rückkauf (rosi.txt:77) – passt weiter, aber kein Bezug zur Bucht.
- Rosis Karten-Begrüßung „La Festa“ (korsisches Fischerdorf, Sommerfest) passt bereits zum Festa-Finale.

### Passung zur neuen Prämisse (Übergabe)
**Sophia – wo sie andockt**
- **Concierge = Vermittlerin im Dorf**: Tagesablauf Hafen, Lieblingsort Alvas Bar, Missionen Küstenwache/Diesel-Gefallen,
  Andenken „Wer in Cala d'Orsu wem einen Gefallen schuldet“ – ein Kontaktnetz, das zum Bucht-Ende 3 „breites Vertrauen“
  (Genossenschaft Dorf + Crew) passt.
- **Megan-Achse**: Megan bot ihr den Job an und würde für das Notizbuch zahlen (LB 41) – Megan bringt den Vertrag mit
  A.V. Estates (Übergabe Thema 1). Sophia verhandelt mit Megan (gv_megan_sophia).
- **Krimiautorin im Krimi**: Pseudonym, sammelt Geheimnisse, Duc hat ein Kapitel – im aktuellen Material nicht als
  Spielmechanik genutzt.
- **Schauspielerin**: Duc will eine Schauspielerin an Bord (Übergabe:171); Sophia war 2 Jahre West-End-Zweitbesetzung,
  nie aufgetreten (sophia.txt:6).
- **Lebensziel-Kandidaten (Quellen)**: eigener Name auf dem Buchrücken; „einen Menschen, den sie nicht gewinnen muss“.
  Ende-Regel verlangt etablierte Voraussetzungen; Füller-Unikat + `sophia_kapitel` sind vorhandene Bausteine.

**Sophia – Lücken**
- Keine Story-Szene nach T2, kein eigener Bogen in der aktiven Engine (Storylets tot), Pseudonym/14 Absagen
  ungenutzt, keinerlei Bezug zu Bucht, Alon, ESG.
- Schwestern-Dynamik fehlt in Events völlig (Abschnitt 3.4); Leas Margot-Bogen hat keinen Sophia-Moment.
- Kein Cold-Open-Moment (Lea wird bei der Explosion gerettet, Sophia kommt nicht vor).
- Inkonsistenter Umgang mit dem Geheimnis (öffentliche Lesung vs. Karte).

**Rosi – wo sie andockt**
- **Explosion/Reparatur pro Akt** (Übergabe Orts-Regel 3, 5): Rosi hat Antriebsraum, Generatorraum, Werkstatt, Uhr
  Reparatur, reparatur-Missionen, Ersatzteilkiste, Kampf-Werkstatt (Upgrades/Veredeln), Crafting-Material „für Rosis
  Werkstatt“ – die mechanische Grundlage existiert.
- **Alon-Hinweis im Maschinenraum**: Übergabe: „rotes Licht im Maschinenraum“ (Akt 1), Beweis im Maschinenraum ab Akt 2 –
  Rosis Revier; Karte: sie liest nachts die Monitore (Brückenstrom 2 Uhr). Bestehende Warnungen „Umrichtergehäuse warm“
  und `route_rosi` (Hersteller) lassen sich anbinden. Megans „Ein PX-480 brennt nicht einfach so“ trifft Rosis Fach.
- **Dorf-Anker**: Lieblingsort Petrus Werkstatt, Schild „Scuderi & Figlie“, Außenborder-Streit mit Petru – einziger
  vorhandener Faden von Rosis Lebensziel (Werkstatt) in die Bucht.
- **Festa**: Kartenbegrüßung „La Festa“ (zitronengelbes Kleid der Mutter) und Set „Festa“ existieren.

**Rosi – Lücken**
- Lebensziel liegt in **Catania**, nicht in der Bucht; Ende-Regel „keine finanzierte Werkstatt ohne Voraussetzungen“.
- „Motor“ vs. E-Antrieb (Widerspruch 11) muss für die Explosion geklärt werden; Unit-01 (Diesel) als einziger lauter
  Motor ist ihr Herzstück – was mit ihm bei der Explosion passiert, steht nirgends.
- Crafting ist laut EDEN_TAGE_ERKUNDUNG noch „offen“ (Engine-Umbau Schritt 6).
- Kein Bezug zu A.V. Estates/ESG; Rosis Romanzen-Kern (Rivalität → „unentschieden“) ist gut belegt, aber ohne
  21-Tage-Taktung.

---

## VERDECKT – Fall-Rollen (nicht im Chat nennen)

Quellen: story.json faelle[2] (Fall 3) und faelle[3] (Fall 4), gebaut aus faelle_py:538-679 (Fall 3) und :680-790
(Fall 4); Alibi-/Neben-Fakten faelle_py:196-213, :946-981. Verdächtige laut story.json `verdaechtige`: chiara, lea,
sophia, rosi, yasin; modul_py:344 `ermittlung.verdacht` chiara, sophia, rosi, lea; `verdacht_ohne_fall` chiara, sophia,
rosi; **`ersatz: rosi`** (Ersatz-Verdächtige, wenn sonst keine; kern/ermittlung.py:826).

### Sophia – Fall 3 „Der Gefallen“ (Sophia verantwortlich)
- **Kern**: Sophia hat für T2 07:30 ein Treffen mit ihrer **Lektorin Helene Marchal** (Pariser Verlag) in Alvas Bar
  vereinbart – Vertragschance für ihr Buch, von der niemand weiß. Sie **erfindet den Gästewunsch Sonnenaufgang**, drückt
  eine Abfahrt um **01:30 ohne Ladelauf von Unit-01** durch („Gäste wollen nachts keinen Diesel hören“) und **überstimmt
  Holms Bedenken mit Megans Namen**. Die Nachtfahrt leert Bank A; im Reservebetrieb Profil R2; LM3 fällt aus (06:20).
  Mit Ladelauf und Abfahrt 03:00 wäre R2 nie aktiv geworden (f3_15).
- **Zeitleiste**: T-4 21:00 reserviert bei Alva (Tag 2, 07:30, 2 Pers.) · T-4 22:10 Planentwurf v2 (Benutzer S.) ·
  T-3 Nachricht der Lektorin „Dienstag 7:30, Bar Santoni, Vertragsentwurf“ · T1 13:10 schlägt Yasin den Sonnenaufgang
  vor · T1 13:20 Yasin an Siri „Sophia meint, Sonnenaufgang wäre Gold“ · T1 15:30 Plan v2 aktiv, Holm genehmigt mit
  Bedenken · T2 01:30 Abfahrt (Bank A 58 %, 6,8 kn) · T2 02:50 Sophia an Lektorin „Wir kommen früh, 7:30 passt“ ·
  T2 08:15 Lektorin geht, Notiz „Musste los. Schreiben Sie mir. H. M.“ bei Alva.
- **Lügen**: „Yasin wollte unbedingt den Sonnenaufgang. Ich hab den Plan am Sonntagmittag angepasst“ (f3_13) gegen
  Dateiversion + Reservierung vier Tage vorher (f3_06, f3_07); auf Nachfrage: „Ich hatte den Halt vorbereitet, falls
  Gäste fragen. Das ist mein Job.“ (f3_14).
- **Spuren**: Reiseplan v2 „eingereicht von Sophia“, Ladelauf gestrichen (f3_05; r_02 gilt in allen Fällen), Dateiversion
  (f3_06), Alvas Reservierungsbuch (f3_07), Notiz der Lektorin (f3_08), Handy-Nachrichten (f3_09, nur durch Gespräch/
  Freigabe), Yasin „Sophias Idee“ (f3_10/11), Holm „ließ sich breitschlagen“ (f3_12), Siris Party-Erinnerung (f3_19),
  Lola sah sie 01:45 aus dem Crewgang kommen (f3_17), Zähler Unit-01 kein Nachtlauf (f3_04). Tipps Lola: Bar-Reservierung
  „letzte Woche!“, Büro-PC um Mitternacht.
- **Gegenhandlungen**: T2 Nacht (Angst ≥1) liefert eine **wahre Beobachtung über Rosi im falschen Zusammenhang**:
  „Ich hab Rosi nachts im Maschinengang gesehen, kurz bevor alles ausging“ (wahr um 01:40, f3_16); ab V3 korrigiert sie
  sich selbst (Flag sophia_korrigiert). T3 Nacht (Angst ≥2) **überschreibt die Plandatei** am Büro-PC 23:40 (f3_18).
- **Geständnis**: freiwillig ab T3 bei V≥3 + 1 Kettenglied („korrigiert sich … ohne Charme, als Bitte um ein Gespräch“);
  Konfrontation ab T4 mit allen drei Gliedern; nie durch Intim/Geschenk/einzelnen Charme-Wurf. **Kernsatz: „Für andere
  einen Gefallen zu organisieren ist mein Beruf. Für mich selbst war es plötzlich eine Lüge.“**
- **Wiedergutmachung**: spricht ohne charmante Umleitung vor der betroffenen Gruppe.
- **Holm in Fall 3**: nimmt die Schuld auf sich („Ich hätte nicht nachgeben dürfen“), nennt Sophia nur bei Frage nach
  dem Plan. Nachtende-Absenderin: Alva.
- **In allen anderen Fällen (unschuldig, rote Spur)**: Alibi h_09 – Sophia telefonierte 02:30–03:10 auf dem Sonnendeck
  auf Französisch mit ihrer Lektorin über ihr Manuskript, „ein Treffen war nicht geplant“; Siri sah sie (h_10); Alva:
  „Sophia? Kenne ich nicht. Bei mir hat keiner von euch reserviert.“ (h_13); Yasin: „Ich hab Sophia mittags gefragt“
  (h_12). Die Lektorin existiert in allen Fällen als Kontakt (Fall-3 `sonder`). **Ihr Schreib-Geheimnis macht sie in
  jedem Durchlauf verdächtig.**
- **Altbestand (tot)**: basis:124-127 Wahrheit „sophia“ – Halt als Gefallen für die Recherche ihres Verlags, Hinweise
  „Alva greets Sophia by name“, „a call from Paris“, Beweisstück `paris_call`.
- **Verbindung zu Lea (Fall-Ebene)**: In Fall 2 plant Lea die Route der Nachtpassage, in Fall 3 setzt Sophia den
  Reiseplan v2 durch – beide Schwestern sind je in einem Fall über die Planung der Nachtfahrt verstrickt; r_02
  („eingereicht über Sophia“) ist in allen Fällen gemeinsamer Fakt.
- **Fit zur Prämisse**: Motiv (eigenes Buch/Name, Gefallen für sich selbst) passt zu Sophias Kartenwunsch; mit Alons
  Vormanipulation wird die Nachtfahrt ohne Ladelauf zum Auslöser statt zur alleinigen Ursache. Megan als Richterin kennt
  Sophia aus dem abgelehnten Angebot (LB 41) – und Sophia benutzte Megans Namen gegen Holm.

### Rosi – Fall 4 „Die harmlose Verzögerung“ (Rosi verantwortlich)
- **Kern**: Rosi setzt nach ihrem Rundgang mit **Servicekarte 2 eine Service-Sperre**, die ihrer Annahme nach nur einen
  kurzen, beaufsichtigten Funktionstest nach dem Ankern erzwingt – das hätte die Ankunft in Calvi verzögert (**Wette**)
  und ihr **einen Morgen mit Duc** gebracht. Die Steuerung behandelt die automatische Umschaltung A→B wie einen Kaltstart,
  geht ins R2, Schutzstopp; Holm drückt den angebotenen Wiederanlauf; LM3 fällt 06:11 aus.
- **Zeitleiste**: T2 00:50 Rosi setzt 50 € auf „nach 18 Uhr“, Totò senkt die Quote 6:1 → 2:1 · 01:40 Rundgang ·
  01:44 Service-Sperre (Karte 2, Ablauf 08:00) · 01:50 Notizbuch „Nach dem Ankern: Funktionstest … mit Duc“ · 06:05
  Umschaltung unter Sperre, R2, Schutzstopp · 06:10 Holm drückt Wiederanlauf · 07:50 Rosi hebt die Sperre allein auf ·
  09:30 Diagnoseprotokoll mit dem alten Servicegerät (Sperrverlauf drin).
- **Lügen**: „Nach dem Rundgang um 01:40 bin ich direkt in die Koje.“ (f4_11) gegen Protokoll Sperre 01:30 Anzeigezeit
  (+14 min Uhrenabgleich r_12); auf Nachfrage „Ich hab am Terminal nur den Status abgefragt.“ (f4_12).
- **Spuren**: Totòs Wettbuch + Aussage „Die weiß doch was“ (f4_07/08), Rosis Notizbuch (f4_09), Lola sah sie 07:45 allein
  mit Kaffee in den Kontrollraum gehen (f4_10), Original-Diagnoseprotokoll (f4_13), Party-Erinnerung „Wenn wir morgen spät
  in Calvi sind, bin ich reich“ (f4_16). Tipps Lola: Quoten-Zank mit Totò; altes Messgerät nachts in die Kiste geräumt.
- **Gegenhandlung**: T2 Nacht (Angst ≥1) ersetzt das Diagnoseprotokoll durch eine neue Messung ohne Sperrverlauf und
  räumt das alte Servicegerät weg (f4_14); danach arbeitet sie zu lange, nimmt Korrekturen persönlich.
- **Geständnis**: freiwillig ab T3 bei V≥3 + (gemeinsam rekonstruiert oder 2 Kettenglieder) – „hört mitten im Satz auf
  zu reparieren“; Konfrontation ab T4; nie durch Intim/Geschenk. **Kernsatz: „Ich wollte einen Morgen. Nicht diese
  Woche.“** Wiedergutmachung: offenes Geständnis + Mitarbeit an der Rekonstruktion; „Eine Romanze darf daran scheitern“.
  Holms Wiederanlauf gehört in den Bericht („folgte der Anzeige, nicht schuldhaft“). Nachtende-Absender: Totò.
- **In anderen Fällen**: Rundgang 01:40 „o. B.“ (r_09) in allen Fällen; Wettbuch 5 € auf „16–18 Uhr“, Quote unverändert
  (h_15); Chiara hörte sie 02:45 schnarchen (h_16, Entlastung); Protokoll „Ursache offen“ (h_17). **Fall 6** („Niemand an
  diesem Tisch“, kein Täter): Rosi sah auf der Party „LM3 TEMP“ gelb – „Die Werft soll sich das in Calvi ansehen“ (f6_08);
  Totò behauptet, sie sei um drei im Maschinenraum gewesen (f6_09, widerlegt über Zeitschaltuhr/h_16); **die Crew
  (Totò, Yasin, Chiara, Lola) unterschreibt eine Liste „Wir glauben, es war Rosi“** (f6_12) = Sündenbock-Gegenhandlung;
  Rosi misst mit Petru die thermische Vorschädigung nach (f6_07). In Fall 3 lenkt Sophia mit einer wahren Beobachtung auf
  Rosi (f3_16); in Fall 5 sagt Totò zu Yasin „Frag Rosi“ (f5_08). Rosi ist `ersatz`-Verdächtige der Ermittlung.
- **Altbestand (tot)**: basis:128-131 Wahrheit „wette“ – jemand aus dem Maschinenraum zog für die Wett-Tafel eine
  Sicherung, Hinweise „a breaker labelled in Rosi's handwriting“, „the betting odds changed the day before“, Beweisstück
  `breaker_note`.
- **Fit zur Prämisse**: Wette + „ein Morgen mit Duc“ ist harmlos gemeint (Kartengeheimnis: eigener Name auf der Tafel,
  40:1) – mit Alons Vormanipulation wird die Sperre zum Auslöser. Rosi ist zugleich die Fachfrau, die die Manipulation
  im Maschinenraum finden müsste (Übergabe: Beweis ab Akt 2) – starke Doppelrolle, falls ihr Fall gezogen wird. Fall 6
  macht sie in jedem Durchlauf zur naheliegenden Sündenböckin der Crew.

# Stimmen-Audit: Hauptfiguren

Stand 04.11.2026 · Branch `berichte-audits` · nur Bericht, am Spiel ist nichts geändert.

## 1. Kopf

**Frage:** Klingt jede Hauptfigur so, wie ihre Wiki-Seite es verlangt? Geprüft nach `docs/wiki/STIL.md` (natürlich, kein Stakkato, einfaches Englisch, Erinnerung im Satz, Pointen sparsam, keine Körpersprache-Floskeln) und der Anrede-Matrix in `docs/wiki/figuren/README.md`.

**Methode**

* Ein Skript (Scratchpad, `python -I`) hat alle Sprechzeilen aus `module/eden_rise/ereignisse.json` nach Sprecher gesammelt, dazu `rast_anrufe.json`, `lob.json` und `legenden.json`. Jede Zeile wurde mit ihrer Fassung in `stimme_tags.json` (Turbo-Tags) verknüpft.
* Gesperrte Quellen sind ausgeschlossen: Kennungen mit „vh.“, „fv_“, „rt_t_“ und alle Telefon-Ereignisse, deren Text in keiner freigegebenen Quelldatei unter `werkzeuge/eden_rise/` steht. Die gesperrten Dateien wurden nicht geöffnet.
* Zählung auf eindeutigen Wortlaut (Varianten desselben Satzes zählen einmal). Dann Lesen: kleine Figuren vollständig, große Figuren etwa zur Hälfte bis zu zwei Dritteln, dazu gezielte Suchen nach Anreden, Marotten, Floskeln, Gedankenstrichen, seltenen Wörtern und Tags in traurigen Zeilen.
* Jedes Zitat unten ist per Skript gegen die Daten geprüft (Sprecher, Event, Wortlaut) und auf eine Quellzeile in `werkzeuge/eden_rise/` zurückgeführt. Tags stehen in eckigen Klammern so, wie die Stimme sie liest; der Spieltext zeigt sie nicht.

**Umfang (eindeutige Zeilen gesichtet):** Megan 139 · Holm 92 · Chiara 237 · Rosi 251 · Lola 239 · Sophia 226 · Lea 233 · Siri 172 · Yasin 20 · Totò 108 · Maxwell 67 · Jana 102 · Alva 179 · Casanova 75 · Petru 76 · Elsa 107 · Alon 5. Zusammen 2328.

**Nicht geprüft:** Duc und seine Antwort-Chips (nur stichprobenhaft, siehe Muster), Erzähltext, Missionstexte, Nebenfiguren (Bibi, Pascal, Kloster, Berge, Dorf), freie Szenen des Modells, Sprite-Gefühle (nur nebenbei), alles aus `story.json`, den Telefon-Ketten und den Favours.

## 2. Übersicht

| Figur | Zeilen gesichtet | Stimme | Humor | Anrede | Erinnerung | Gesamt | Hauptmuster |
|---|---|---|---|---|---|---|---|
| Megan | 139 | gemischt | gut | gut | gut | gemischt | Bösewicht-Theater trägt, aber in Wut Großbuchstaben und Telegramm; schottische Kante fehlt (2 Zeilen) |
| Holm | 92 | gut | gut | schwach | gut | gemischt | 9 Zeilen „Officer“ statt „Frankfurt“, alle in der Belagerung; „Go to bed“ fünfmal |
| Chiara | 237 | gut | gut | gut | gut | gut | Bewertungen sitzen; ein deutsches Wort, Französisch/Italienisch fast nie |
| Rosi | 251 | gut | gut | gut | gut | gut | Maschinen statt Gefühle trägt; Floskel „Don't look at me like that“ (5 Zeilen) |
| Lola | 239 | gut | gemischt | gut | gemischt | gemischt | „Mostly …“ in 34 Zeilen, oft ohne Bezug; einzelne Telegramm-Zeilen |
| Sophia | 226 | gut | gut | gut | gut | gut | Pausen und Wetten sitzen; „Ten euros“ 21 Mal; britische Redewendungen |
| Lea | 233 | gut | gut | gemischt | gut | gut | Fakten-Tick lebt; zweimal „Officer“, „drew“, Redewendungen |
| Siri | 172 | gut | gut | gut | gut | gut | Kamerastimme bricht schön; „Sorry“ in 44 Zeilen, ein Standard-Flirt fällt aus der Rolle |
| Yasin | 20 | gut | gut | gut | (kaum Rückbezüge) | gemischt | wenige Zeilen, Netz-Slang für Nicht-Muttersprachler schwer, ehrlicher Satz fast nie |
| Totò | 108 | gut | gut | gemischt | gut | gut | Wetten und Neapel tragen; in den Gennaro-Szenen 5 Mal „boss“ |
| Maxwell | 67 | gemischt | gut | gut | gut | gemischt | „Mr. Maximum“ in 60 von 67 Zeilen, oft jeder Satz, dann Stakkato |
| Jana | 102 | gut | gut | gut | gut | gut | „Sir“ sitzt (39); „Sorry“ in 46 Zeilen; Chiara-Kopien fehlen ganz |
| Alva | 179 | gemischt | gut | gemischt | gut | gemischt | „o figliolu“ in 34 Zeilen (K9: sparsam); Flirt-Zeilen im Stakkato |
| Casanova | 75 | gut | gut | gemischt | gut | gut | Pathos und Elternhaus-Leise sitzen; Deko-Französisch, einmal „Mon capitaine“ |
| Petru | 76 | gemischt | gut | gemischt | gemischt | gemischt | „Hm.“ in 29 von 76 Zeilen, Satzfetzen; zweimal „Officer“; ein Erklärsatz |
| Elsa | 107 | gut | gut | gut | gut | gut | Protokoll-Humor sitzt; die Kisten-Zeile aus dem Wiki wird wörtlich wiederholt |
| Alon | 5 | gut | gut | gut | gut | gut | wenige Zeilen, ruhig und genau; die Produktsprache der Seite fehlt noch |

## 3. Figuren

### Megan

Die Seite verlangt langsames, gefährliches Edinburgh-Englisch mit Bösewicht-Pausen, nie laut, schottische Kante bei Wut, Schach und Preisschilder, „First Officer“ wenn verärgert, sonst „Duc“.

**Treffer**

1. “Mister Esposito. What's in the box? No, don't run. Running is a confession.” (`ereignisse_gag1.py:31`, g1_drohne). Ruhige Drohung mit Haken am Ende, genau der Bösewicht, der seinen Spaß hat.
2. “You would do very well in my business. That's not a compliment, it's a warning.” (`ereignisse_dorf.py:219`, gv_casanova_megan). Lob mit Preisschild, eine Pointe, sonst nichts.
3. “In the hangar you offered to tie one of these behind your back. I've been practising. Mine's faster.” (`ereignisse_flirt.py:254`, fl_megan_palstek). Vorbild für die Erinnerung im Satz: der Spieler bekommt den Hangar von Tag 0 mitgeliefert.

**Ausrutscher**

1. “It is empty, First Officer. [sigh] EMPTY. Four days.” (`ereignisse_akt1.py:42`, mg_tag3). Regel: Megan „wird nie laut“; Großbuchstaben lesen sich als Schreien, dazu Telegramm. Ebenso „SUNRISE“ in derselben Nachricht.
   Vorschlag: “It is empty, First Officer. [sigh] Completely, beautifully empty. You have four days to put one name in it.”
2. “Tomorrow. Eleven o'clock. The salon. [clear throat] Bring proof. Not feelings.” (`ereignisse_akt1.py:79`, mg_tag6). Regel: Stakkato; die Seite nennt genau diesen Telegrammstil unter „Nicht so“.
   Vorschlag: “Tomorrow at eleven, in the salon. [clear throat] Bring me proof, First Officer. I can get feelings from the cook.”
3. “The First Officer cleans. Interesting. [laugh] Ahaha— don't look at me.” (`ereignisse_gagv.py:207`, gv_megan_chiara; dasselbe Muster in `ereignisse_gag1.py:281`, g1_helikopter). Regel: Das Lachen steht doppelt (Tag und „Ahaha“ im Text), dazu ein Gedankenstrich im Spieltext, und „don't look at me / don't tell anyone“ wiederholt sich bei ihr.
   Vorschlag: “The First Officer cleans. How... interesting. [laugh] No. You didn't hear that.”

### Holm

Die Seite verlangt wenige Worte, flaches norwegisches Englisch, ganze Gedanken mit Haken, „Frankfurt“, „Takk“, „Faen“, und Wichtiges genau einmal.

**Treffer**

1. “[clear throat] Papers don't float, Frankfurt.” (`ereignisse_tag0.py:85`, t0_holm). Kurz, vollständig, mit Anrede.
2. “It pulls left. [clear throat] Everyone in my family does.” (`ereignisse_holm.py:122`, hb_sieg). Trockener Haken im zweiten Satz, Humor aus Charakter.
3. “Faen. Give me a second. ...Keep the rifle until the rematch, Frankfurt. I can't hold it straight tonight.” (`ereignisse_belagerung.py:344`, bl_bericht). Der einzige Fluch, an der richtigen Stelle; Gefühl über den Gegenstand statt benannt.

**Ausrutscher**

1. “Then nobody is coming. Go to bed, Officer. That's an order, and I don't care that you outrank me.” (`ereignisse_belagerung.py:126`, bl_kriegsrat). Regel: Anrede-Matrix („Frankfurt“). In der Belagerung sagt sie in 9 Zeilen „Officer“ (z. B. auch bl_welle_3, bl_welle_6, bl_leer, bl_nacht_wahl_20), ausgerechnet in den Szenen, in denen sie Duc am nächsten ist. Die Zeile hat keinen Turbo-Tag.
   Vorschlag: “Then nobody is coming. [sigh] Go to bed, Frankfurt. That's an order, and I don't care that you outrank me.”
2. “[clear throat] Adrien up at the bergerie, your dead deserter, thinks he knows.” (`ereignisse_holm.py:107`, hb_koffer). Regel: einfaches Englisch; „bergerie“ ist ein seltenes Fremdwort, „your dead deserter“ ist doppeldeutig.
   Vorschlag: “[clear throat] Adrien thinks he knows, the soldier up at the shepherd's hut.”
3. “Static. Only static. Fine. Then we use our eyes. Go to bed, Officer.” (`ereignisse_belagerung.py:192`, bl_funk_nichts). Regel: Stakkato aus Zwei-Wort-Sätzen, wieder „Officer“, und „Go to bed“ kommt bei ihr fünfmal (bl_kriegsrat zweimal, bl_funk_nichts, bl_ab_schon, bl_leer als „Go and get some sleep“). Wer alles einmal sagt, wiederholt keinen Befehl fünfmal. Kein Tag.
   Vorschlag: “It's only static. Fine, then we use our eyes. [sigh] Get some sleep, Frankfurt, I'll take the first hour.”

### Chiara

Die Seite verlangt laut, warm, schnell, Hamburger Direktheit, Bewertungen auf einer Zehnerskala, schlechtes Französisch und Italienisch, keine deutschen Wörter, nachts leise und knapp.

**Treffer**

1. “Welcome aboard, First Officer. [chuckle] Your cabin is ready. It used to be mine.” (`ereignisse_tag0.py:97`, t0_chiara). Die ganze Kränkung in einem Nachsatz.
2. “Sunset: four. Moon: six. The stars are showing off, so I took two points away. I'm rating the sky, Duc, because I've run out of things to count.” (`ereignisse_belagerung_nacht.py:194`, bl_na_chiara). Marotte trägt Gefühl, „Duc“ privat, nachts leiser.
3. “I go loud when I'm scared. You've noticed that, you notice everything. [sniff] In April I got up from that Yachtmaster exam and went straight back to the boat” (`ereignisse_romanzen.py:396`, rm_c4_b). Erinnerung im Satz (April, die Prüfung), Selbsterkenntnis ohne Erklärsatz.

**Ausrutscher**

1. “[chuckle] And yes, that's Opa's jacket. Yes, I'm allowed. ⚓” (`werkzeuge/eden_rise/selfie_daten.json:146`, sf_chiara_3_kabine). Regel: Chiara spricht keine deutschen Wörter; „Opa“ versteht außerdem nicht jeder.
   Vorschlag: “[chuckle] And yes, that's my grandad's jacket. Yes, I'm allowed. ⚓”
2. “[sigh] First Officer. You took the tender out alone, at night, against my rota.” (`ereignisse_legenden.py:157`, legenden sirene.chiara.zeit.0). Regel: einfaches Englisch; „rota“ ist britisch und selten. Sie hat dafür ihr eigenes Wort.
   Vorschlag: “[sigh] First Officer. You took the tender out alone, at night, and it wasn't on my watch list. I give the idea a two. Whatever you found out there, I'm still deciding.”
3. “You came for an accident. [chuckle] That's – sit. It's still warm. So am I. Forget I said that.” (`ereignisse_flirt.py:356`, fl_chiara_tee). Regel: Wortspiel auf ihre Nachricht davor („two by accident“), für Nicht-Muttersprachler unklar; danach Satzfetzen.
   Vorschlag: “So you came up for my accident. [chuckle] Okay, sit down, the tea is still warm. So am I. Forget I said that.”

Randnotiz: Französisch und Italienisch, laut Seite „schlecht und stolz eingestreut“, kommen nur zweimal vor (Olivetti-Szene, ein „Merci“). Hier ist Platz für Akt 3.

### Rosi

Die Seite verlangt direkt, frech und schnell in ganzen Sätzen, knapp nur bei Technik, Anime-Pathos, „Officer“, nie der Name, „Captain“ erst als Moment, Gefühle über Maschinen.

**Treffer**

1. “She is not a monster. [sigh] She's thirty-one years old, she's survived two owners and one explosion, and she has never once had tentacles.” (`ereignisse_wiki.py:424`, gv_unit01_bild). Gerührt redet sie über die Maschine; konkrete Zahlen statt Gefühl.
2. “Morning, Capt– Officer. Officer. [chuckle] Morning, Officer. Stop smiling, it's very unprofessional.” (`ereignisse_romanzen.py:290`, rm_e_rosi_captain). Die Anrede selbst wird zur Szene, genau wie K1 es will.
3. “Terremoto, Officer, on the worst day of my life, and you've dented it twice. [chuckle] I'm writing that on the board.” (`ereignisse_akt2.py:270`, a2_steelmop_4). Erinnerung im Satz (der Tag des Brandes), dazu ihr Whiteboard.

**Ausrutscher**

1. “The mayor wants us on stage in sailor costumes, singing, and she drew a picture, Officer. [laugh] There's an actual picture.” (`ereignisse_bordrat.py:76`, br_festa_auftritt). Regel: einfaches Englisch; „drew“ ist das Beispielwort aus CLAUDE.md.
   Vorschlag: “The mayor wants us on stage in sailor costumes, singing, and she made a drawing of it, Officer. [laugh] There's an actual picture.”
2. “I'm fine. One more day, then I sleep. [sigh] Promise. Maybe. Don't look at me like that.” (`ereignisse_bordrat.py:255`, br_rosi_ueberstunden). Regel: K2 „in ganzen Sätzen“, hier Fetzen; dazu die Floskel, die sie fünfmal sagt (auch du_reparatur_rosi, fl_rosi_pfand, fk_rosi_schicht, rm_r3).
   Vorschlag: “I'm fine, Officer. One more day and then I sleep, I promise. [sigh] Probably. And stop looking at my hands, they always shake after a double shift.”
3. “As long as the animal has strength, the collar wins. Under one in ten, it can't. Above that, you're just making it wet.” (`ereignisse_mochis.py:156`, mo_schlafgranate). Regel: Technik darf knapp sein, muss aber verständlich bleiben; „one in ten“ von was?
   Vorschlag: “[sniff] It's a vet's sedative in a soft shell. The collar fights it while the animal is still strong, so tire it out first. When it has less than a tenth of its strength left, the collar loses.”

### Lola

Die Seite verlangt laut, warm, träge, Aussie-Slang, Sätze, die das Ende verlieren, Tick „… Mostly the cheese.“, Tratsch mit „Don't tell anyone I told you“, „Boss“ und „mate“.

**Treffer**

1. “I always lose the end of my sentences, you've noticed. I do it on purpose. If you don't finish, nobody can tell you it's wrong.” (`ereignisse_romanzen.py:628`, rm_o4). Die Marotte bekommt eine Wunde. Stärkste Zeile der Figur.
2. “[chuckle] Mate, Alva says Petru cried. Petru! I didn't know he had water in him. Mostly salt, I reckon.” (`ereignisse_legenden.py:121`, legenden berge.lola.zeit.0). Hier passt der Tick, weil er auf etwas zeigt.
3. “Nan's ninety-one, Boss. [sigh] If I don't ring, she rings the coast guard. She's done it before.” (`ereignisse_wiki.py:173`, br_satellit_sonntag). Konkrete Kleinigkeit statt Gefühl, trocken beobachtet.

**Ausrutscher**

1. “G'day Boss, Lola here! [chuckle] No reason. Just wanted to say there's soup if you want soup. Or not. No pressure. Mostly the cheese.” (`rast_anrufe_eden_rise.py:71`, rast_anrufe lola/0). Regel: Stakkato (sie plappert, sie telegrafiert nicht), und der Tick hängt ohne Bezug (Suppe, kein Käse). „Mostly“ steht in 34 ihrer 239 Zeilen.
   Vorschlag: “G'day, Boss, it's Lola! [chuckle] No reason, I just wanted to say there's soup if you want some, and if you don't, I'll eat it and tell everyone it was yours.”
2. “Mostly. [chuckle] Don't push your luck, I've got a hot pan.” (`ereignisse_romanzen.py:797`, rm_e_lola_nacht1). Regel: Redewendung („push your luck“).
   Vorschlag: “Mostly. [chuckle] Don't ask for more, Boss, I've got a hot pan in my hand.”
3. “Speedrun. Respect. [laugh] Bit rude. Respect.” (`ereignisse_flirt.py:206`, fl_lola_sonnencreme). Regel: STIL nennt Lola ausdrücklich als Figur, die nicht im Telegrammstil spricht; „speedrun“ ist Spieler-Slang.
   Vorschlag: “That was fast, Boss. [laugh] I respect it. I mean, it's a bit rude, but I respect it.”

### Sophia

Die Seite verlangt tief, warm, ohne Eile, britisch, Understatement, ein Satz und dann Stille, „Darling“ beim Managen, Wetten in der Ecke, ohne Show kurze schlichte Sätze.

**Treffer**

1. “Eventually. [sigh] That's a lovely word. It means not today.” (`ereignisse_funken.py:193`, bk_sophia_arm). Ein Satz, dann Stille, dann der Haken.
2. “My father left when I was ten. I was charming by eleven. [sniff] You see how that works.” (`ereignisse_romanzen.py:477`, rm_s4). Ohne Show kurz und schlicht, die ganze Figur in drei Sätzen.
3. “And we both remember our little bet on the aft deck, the ten euros, so let me save you some trouble. [chuckle] One of us. Never both.” (`ereignisse_romanzen.py:201`, rm_l3). Erinnerung im Satz (Achterdeck, zehn Euro), dann kurz.

**Ausrutscher**

1. “So. Lea and Siri went skinny dipping. [chuckle] And Lieutenant Ferrandi's patrol boat has a searchlight. A very good one.” (`ereignisse_bordrat.py:240`, br_nacktbaden). Regel: Redewendung („skinny dipping“).
   Vorschlag: “So. Lea and Siri went for a swim last night, darling, without their swimsuits. [chuckle] And Lieutenant Ferrandi's patrol boat has a searchlight. A very good one.”
2. “Darling, they've polished brass for a week. [chuckle] One afternoon in the sea, or I start hearing mutiny in the walls.” (`ereignisse_gagv.py:267`, gv_dienstplan). Regel: Bild plus seltenes Wort („mutiny in the walls“).
   Vorschlag: “Darling, they've polished brass for a week. [chuckle] Give them one afternoon in the sea, or they'll start talking about you, and I'll have to pretend I can't hear it.”
3. “I never cheat, darling. [chuckle] Two years in the wings of a West End theatre teaches you to watch faces.” (`ereignisse_gagv.py:31`, gv_strip_poker). Regel: doppeldeutig („wings“) und Vorwissen („West End“); im selben Satz noch „garter“.
   Vorschlag: “I never cheat, darling. [chuckle] Two years of waiting backstage in a London theatre teaches you to watch faces.”

Randnotiz: „Ten euros“ steht in 21 Zeilen. Als Marke gut, aber in Akt 3 lieber seltener und dafür mit Erinnerung („the bet from the aft deck“).

### Lea

Die Seite verlangt schnell, hell, ernsthaft, Meeresfakten ungefragt, kornisch („proper“, „dreckly“), nervös schneller mit schiefen Fakten, „Duc“.

**Treffer**

1. “Come back dreckly, that's Cornish for sometime soon, but not too dreckly.” (`rast_anrufe_eden_rise.py:127`, rast_anrufe lea/2). Fachwort mit einfachem Wort daneben, genau nach STIL. Die Zeile hat keinen Tag.
2. “I jump up and down about crabs. [sniff] But I read it and I felt nothing, for a whole minute.” (`ereignisse_romanzen.py:218`, rm_l4). Ihre heimliche Angst, gezeigt statt benannt.
3. “Do you hear that? [gasp] That hum? It's been there since you climbed the bell tower after Kevin.” (`ereignisse_akt2.py:201`, a2_koordinaten). Erinnerung im Satz.

**Ausrutscher**

1. “Officer. [sniff] I've never asked you for anything. I'm asking now. Get that bird.” (`ereignisse_akt2.py:174`, a2_kevin_raub). Regel: Anrede („Duc“), Stakkato, und dieselbe Formel sagt Petru fast wörtlich (siehe dort). Nervös wird Lea schneller, nicht knapper.
   Vorschlag: “Duc. [sniff] That's Grandad's page in his beak, the one with the cross on it. Please get that bird back for me.”
2. “Grandad's page is gone. Sea, rain, I don't know. So I drew it. From memory.” (`ereignisse_akt2.py:216`, a2_koordinaten_ohne). Regel: „drew“ (dasselbe in rm_e_lea_versetzt).
   Vorschlag: “[sigh] Grandad's page is gone. Sea, rain, I don't know. So I made a copy from memory, as well as I could.”
3. “That's the bit that gives me the creeps.” und “Great, now I've got goosebumps.” (`ereignisse_ligeia.py:279` und `:288`, lg_felsen). Regel: Redewendungen; dazu „oh my days“ in lg_polaroid.
   Vorschlag: “That's the part that scares me a bit.” und “[gasp] Great, now I'm scared. Thanks, Duc. Thanks a lot.”

Randnotiz: „Did you know …“ steht in 10 Zeilen, oft als „Did you know – no.“ Der Abbruch ist schön, aber nur, wenn er selten bleibt.

### Siri

Die Seite verlangt weiches Englisch mit Singsang, Kamerastimme, die in die echte bricht, zu viele Entschuldigungen, Fragen, die niemand einer Influencerin stellt, „Duc“.

**Treffer**

1. “Hiii guys, golden hour, grateful for this journey. [sigh] That's the caption my manager wants under this.” (`ereignisse_romanzen.py:720`, rm_i1). Der Bruch von Kamera zu echt, in einer Zeile.
2. “Sorry. [gasp] I mean, sorry to you too. I was saying sorry to the chair. It didn't do anything wrong.” (`ereignisse_funken.py:216`, bk_siri_stuhl). Marotte und Humor aus Charakter; der Stuhl kehrt später mit Erinnerung wieder.
3. “He knitted one star every evening, all one winter, and I never wore it.” (`ereignisse_romanzen.py:733`, rm_i2). Konkrete Kleinigkeit trägt das Gefühl.

**Ausrutscher**

1. “I just need a bit of space. [sigh] To sleep. To think. That's all. Please don't make this a thing.” (`ereignisse_bordrat.py:282`, br_siri_umzug). Regel: Stakkato und Redewendung.
   Vorschlag: “I just need a bit of space, to sleep and to think. [sigh] That's all, I promise. Sorry. Please don't make it bigger than it is.”
2. “Come and get it, then. [laugh] Tonight. If you dare.” (`ereignisse_gag1.py:254`, g1_siri_pullover). Regel: Figurentreue; ein Standard-Flirt ohne ihre Unsicherheit, so könnte jede sprechen.
   Vorschlag: “Then come and get it tonight. [laugh] Sorry, that sounded much braver in my head.”
3. “[sigh] …Good. No talking, then.” (`ereignisse_belagerung_nacht.py:273`, bl_na_siri_wieder). Regel: „Alle klingen gleich“; die Zeile ist eine Vorlage für sieben Frauen (siehe Muster 1).
   Vorschlag: “[sigh] Sorry. No, I'm not sorry. We don't have to say anything.”

### Yasin

Die Seite verlangt Influencer-Sprech, schnell, laut, „bro“, „That's business“, „First Officer“ oder „bro“, ab und zu ein ehrlicher Satz, der sofort überspielt wird.

**Treffer**

1. “Don't say anything, just stand next to the spear and look tired. That's business.” (`ereignisse_legenden.py:89`, legenden kloster.yasin.zeit.0). Seine Welt in einer Regieanweisung.
2. “[sigh] nice is bad for the brand. delete that. …ok don't delete it” (`ereignisse_charms.py:115`, ch_yasin). Der einzige echte ehrliche Satz, und er wird sofort zurückgenommen, wie verlangt.
3. “The sustainability guy! [laugh] Say something green, my man!” (`ereignisse_tag0.py:230`, t0_siri). Erster Eindruck sitzt.

**Ausrutscher**

1. “Already rolling. [chuckle] This is going to do numbers.” (`ereignisse_staerken.py:75`, du_koch_toto). Regel: Netz-Slang, für Nicht-Muttersprachler unklar.
   Vorschlag: “Already filming. [chuckle] Bro, a lot of people are going to watch this.”
2. “Babe, unplugged content performs insane. [chuckle] It's authentic. I'll just film a little bit.” (`ereignisse_bordrat.py:203`, br_singen_ohne_strom). Regel: drei Slang-Wörter in einem Satz.
   Vorschlag: “Babe, people love videos with no electricity and no filter. [chuckle] It feels real. I'll just film a little bit.”
3. “[clear throat] the falcon is a winner. i only work with winners. so. yeah. it's yours. don't make it weird” (`ereignisse_charms.py:113`, ch_yasin). Regel: Redewendung, die auch Siri (`ereignisse_bordrat.py:150`) und Chiara (`rast_anrufe_eden_rise.py:43`) benutzen; drei Figuren, ein Satz.
   Vorschlag: “[clear throat] the falcon is a winner. i only work with winners. so. yeah. it's yours. no hugs, bro”

Randnotiz: Mit 20 Zeilen ist Yasin dünn besetzt. Für Akt 3 fehlt vor allem der ehrliche Satz (sein Geld ist dünner, als es aussieht).

### Totò

Die Seite verlangt Straßenwitz aus Neapel, warm und laut, feste Wörter („Comandante“, „Madonna“, „piccola“, „gigante“), Wetten auf alles, still bei Gennaro.

**Treffer**

1. “In Napoli we have a word for a fat seagull, Comandante. [laugh] The word is dinner.” (`ereignisse_bordrat.py:189`, br_kevin_nest). Ruhiger Satz, Haken am Ende.
2. “He mends it every afternoon, since Marie. Five years. It's the most mended net in Corsica.” (`ereignisse_wiki.py:338`, g1_petru_netze). Erinnerung im Satz (Marie, fünf Jahre) und Wärme für einen anderen.
3. “Comandante, no bet today. [sigh] I just want to know you are okay. Strange, eh? Totò with no bet.” (`rast_anrufe_eden_rise.py:163`, rast_anrufe toto/2). Die Marotte fehlt mit Absicht, und das ist das Gefühl.

**Ausrutscher**

1. “I'm sorry. Bring him out, boss.” (`ereignisse_grotte.py:120`, gr_start; ebenso `ereignisse_akt2.py:155` „It's Monday, boss.“ und gr_heim). Regel: Anrede-Matrix („Comandante“); „Boss“ ist Lolas Wort. Wenn das ein bewusster Bruch sein soll (die Show fällt weg), gehört er auf `toto.md`.
   Vorschlag: “I'm sorry. Bring him out, Comandante.” (Tag [gasp] am Anfang der Zeile bleibt.)
2. “Ten to one. Against. [chuckle] But I love a long shot, Comandante.” (`ereignisse_tag0.py:144`, t0_toto). Regel: Redewendung aus der Wettsprache.
   Vorschlag: “Ten to one against you. [chuckle] But I like to bet on the man nobody believes in, Comandante.”
3. “Okay. [clear throat] Prove it. I'll believe it when I see it.” (`ereignisse_akt2.py:66`, a2_morgen_kalt). Regel: Figurentreue und Redewendung; keine Anrede, keine Wette, so könnte jeder sprechen.
   Vorschlag: “Okay, Comandante. [clear throat] Then I bet one euro on you. Only one, this morning. Show me, and tomorrow I bet more.”

### Maxwell

Die Seite verlangt groß, warm, theatralisch, dritte Person, ein Witz pro Satz, nie gemein, südafrikanische Wörter, „Number One“ und „brother“, leise nur, wenn es ernst ist.

**Treffer**

1. “Brother, it's just me. No Mr. Maximum today. I wanted to say you're doing good. My gogo, my grandmother, would like you.” (`rast_anrufe_eden_rise.py:183`, rast_anrufe maxwell/2). Der leise Maxwell, das Fremdwort mit einfachem Wort daneben. Kein Tag.
2. “Number One goes into a cave full of smugglers and comes back with a cousin! Eish. Mr. Maximum goes to the shop and comes back with milk.” (`ereignisse_legenden.py:141`, legenden grotte.maxwell.zeit.0). A dann B, wie im STIL beschrieben.
3. “On day two you laughed at it, brother, and it taught you to parry anyway.” (`ereignisse_akt2.py:232`, a2_steelmop). Erinnerung im Satz.

**Ausrutscher**

1. “Mr. Maximum has no tears. [sniff] Mr. Maximum has an allergy. To very good push-ups. Number One, look away.” (`ereignisse_yamamoto.py:140`, mt_zehn). Regel: Stakkato; wenn jeder Satz mit „Mr. Maximum“ beginnt, wird die dritte Person zur Liste (60 von 67 Zeilen).
   Vorschlag: “Mr. Maximum is not crying, Number One. [sniff] Mr. Maximum is allergic to very good push-ups, so please look away.”
2. “But this little machine comes down at you with no face, brother, and his legs turn to porridge.” (`ereignisse_belagerung_nacht.py:167`, bl_ab_maxwell). Regel: Redewendung.
   Vorschlag: “But this little machine comes down at you with no face, brother, and Mr. Maximum's legs stop listening to him.”
3. “Mr. Maximum has written to his Gogo. He told her it's a very big training session.” (`ereignisse_belagerung.py:135`, bl_letzte_nacht). Regel: Fremdwort ohne einfaches Wort (in rast_anrufe erklärt, hier nicht), Schreibweise uneinheitlich. Kein Tag.
   Vorschlag: “[sniff] Mr. Maximum has written to his gogo, his grandmother. He told her it's a very big training session.”

### Jana

Die Seite verlangt allein klein und schnell, in der Gruppe laut, Wiener Wörter („Na geh“, „Jessas“, „Servus“, „Ja“), ständig sorry, Chiaras Sprüche leicht falsch kopiert, „Sir“, Maxwell „Coach“.

**Treffer**

1. “I've followed her since I was sixteen. It's like carrying towels for a lighthouse.” (`ereignisse_wiki.py:267`, br_handtuecher). Eigenes, schräges Bild statt Pointe.
2. “Only to the harbour and back, Sir. Four hundred metres. [chuckle] I've counted. I've counted them a lot, actually.” (`ereignisse_wiki.py:191`, br_jana_tender). Konkrete Zahl, Haken im Nachsatz.
3. “Sir, you were always kind to me, even when I said sorry to the door.” (`rast_anrufe_eden_rise.py:207`, rast_anrufe jana/2). Erinnerung im Satz (die Tür von Tag 0).

**Ausrutscher**

1. “I... nobody ever... Jessas. Thank you. Thank you, sorry. No. Thank you.” (`ereignisse_belagerung.py:49`, bl_minicu_jana). Regel: Stakkato und die Formel „nobody ever“ (Muster 1); Minicu hat vorher klar gefragt („Why sorry? You did nothing.“), sie antwortet nicht darauf. Kein Tag.
   Vorschlag: “I don't know. I always say it. [sniff] Jessas. Thank you, then. Thank you, not sorry.”
2. “That's – the rabbit came out of the hole and went round the wrong tree. Two trees. You're a tree.” (`ereignisse_flirt.py:397`, fl_jana_knoten). Regel: Vorwissen; den Merksatz für den Palstek kennt nicht jeder.
   Vorschlag: “[gasp] Jessas. Sorry, Sir! The rabbit is supposed to go round one tree, that's how you learn the bowline, and I sent it round two. You're the second tree.”
3. “Yes. Ja. [sigh] Thank you for asking. Nobody asks. Sorry.” (`ereignisse_romanzen.py:866`, rm_e_jana_nacht). Regel: dieselbe Formel wie bei neun anderen Figuren.
   Vorschlag: “Yes. Ja. [sigh] Thank you, Sir. I'm completely fine, I already said sorry to the rope this morning.”

Randnotiz: Die Seite sagt, Jana kopiert Chiaras Sprüche und kriegt sie falsch hin. In den gesichteten Zeilen gibt es keine einzige Chiara-Bewertung von Jana. Leichter Akt-3-Gag: “Seven out of ten, Sir. Chiara says eight. I say seven, because I'm new.”

### Alva

Die Seite verlangt warm, spöttisch, entspannt, Bar-Rhythmus, der eine Satz sitzt, flirtet mit allen, „o figliolu“ sparsam (K9), vergisst nie, wer hilft.

**Treffer**

1. “Olivetti is a typewriter, cara. [laugh] You've just ordered a glass of red and a typewriter.” (`ereignisse_wiki.py:471`, gv_chiara_italienisch). Hört zu, dann sitzt der Satz.
2. “He fired it once, at a man who wouldn't pay for a bottle, and he missed on purpose. The man paid.” (`ereignisse_belagerung.py:90`, bl_alva_flinte). Ruhig erzählt, Haken in drei Wörtern. Kein Tag.
3. “[laugh] You went out through my attic window and came back through it with feathers in your hair.” (`ereignisse_legenden.py:187`, legenden kevin.alva.laden.0). Die Erinnerung steckt im Bild.

**Ausrutscher**

1. “the carnation stays with him. [sniff] don't push your luck, o figliolu 😘” (`ereignisse_charms.py:107`, ch_alva). Regel: Redewendung, dazu K9: „o figliolu“ steht in 34 ihrer 179 Zeilen, das ist kein Markenzeichen mehr, sondern ein Füllwort.
   Vorschlag: “the carnation stays with him. [sniff] that's enough for one day 😘”
2. “No, you won't. [sigh] Strangers can leave. Take the bottle and owe me, and we'll say no more about it.” (`ereignisse_belagerung_nacht.py:163`, bl_ab_alva). Regel: Redewendung.
   Vorschlag: “No, you won't. [sigh] Strangers can leave. Take the bottle, owe me, and we don't talk about it again.”
3. “You rowed. In the dark. [chuckle] For me and a till. Sit. You can count the coins I drop.” (`ereignisse_flirt.py:299`, fl_alva_tuer). Regel: Stakkato (ihr Bar-Rhythmus ist entspannt, nicht abgehackt); „till“ ist selten.
   Vorschlag: “You rowed out here in the dark, for me and an old cash box. [chuckle] Sit down. You can count the coins I drop.”

### Madame Casanova

Die Seite verlangt groß, festlich, theatralisch, Reden mit Pausen für Applaus, sprunghaft zwischen Pathos und Alltag, „Monsieur“, leise und kurz beim Elternhaus.

**Treffer**

1. “Forty minutes. [sigh] ...Nobody came in forty minutes. Nobody came at all.” (`ereignisse_cliffhanger.py:48`, bl_cliff_platz). Das Echo aus dem STIL, ernst durch Kontrast.
2. “My father built these, you know. He could fill this square just by coming out to buy cigarettes. [sigh] I need a cannon.” (`ereignisse_dorf.py:197`, g1_casanova_morgen). Leise beim Elternhaus, dann zurück in den Alltag.
3. “[sigh] A draw. With a seagull. I will say you won, Monsieur. Nobody checks speeches.” (`ereignisse_legenden.py:311`, leg_kevin_casanova). Humor aus Charakter, Anrede sitzt.

**Ausrutscher**

1. “Mon capitaine! Hold my hand for the high note! [laugh] There is no high note! I'll make one!” (`ereignisse_staerken.py:216`, auf_karaoke). Regel: K1, „Captain“ ist eine Auszeichnung und kein Karaoke-Wort; Matrix sagt „Monsieur“.
   Vorschlag: “Monsieur! Hold my hand for the high note! [laugh] There is no high note! I'll make one!”
2. “Mesdames et messieurs! [laugh] Corsica against Saigon!” (`ereignisse_staerken.py:52`, du_koch_alva; ebenso „Mademoiselle“ in gv_casanova_chiara, „Magnifique“ in ch_casanova). Regel: Fremdwörter nur, wo die Seite sie erlaubt; sonst Deko.
   Vorschlag: “Ladies and gentlemen! [laugh] Corsica against Saigon! Forty years of tradition against one handsome sailor!”
3. “And was that the blood of Christ I smelled at the door, or the good Patrimonio?” (`ereignisse_dorf.py:459`, g1_messe). Regel: Vorwissen; „Patrimonio“ (Weinort) kennt kaum ein Spieler.
   Vorschlag: “[clear throat] If I may, Father, a small word from the municipality. And was that the blood of Christ I smelled at the door, or the good red wine from Patrimonio?”

### Petru

Die Seite verlangt bewusst knapp, langsam, mit Gewicht, „Hm.“ in zehn Bedeutungen, kurz heißt nicht abgehackt, ein ganzer Satz mit Meeresbild, keine Anrede.

**Treffer**

1. “Hm. She put the bay leaf in the milk. Nobody knows that. [sniff] …Now you know.” (`ereignisse_wiki.py:234`, br_fish_pie). Marie ohne Namen, Vertrauen ohne Wort dafür.
2. “Hm. [chuckle] Good. You understand boxes. Most people only understand what's in them.” (`ereignisse_ligeia.py:269`, lg_seekiste). Kurz, ganz, mit Gewicht.
3. “My wife painted that boat. [chuckle] They were not getting on it.” (`ereignisse_hafen.py:143`, hk_petru). Zwei Sätze, ein ganzes Leben.

**Ausrutscher**

1. “I have never asked anyone for anything. [sniff] Not since Marie died. Bring her down, Officer. Please.” (`ereignisse_berge.py:112`, bg_petru_auftrag). Regel: Petru spricht ohne Anrede (ebenso bg_hafen_a „Thank you, Officer“); die Formel teilt er mit Lea. Zwei Zeilen davor (`ereignisse_berge.py:109`) steht sein „Hm.“ mit Gefühl sadness, die Stimme liest es aber als “[chuckle] Hm.” (Muster 6).
   Vorschlag: “I have not asked anyone for anything since Marie died. [sniff] Bring her down. Please.”
2. “Megan told you to bring timber and stone back on day fifteen, when she called about the six days. Now we see what you brought.” (`ereignisse_belagerung.py:198`, bl_morgen_22). Regel: Erklärsatz für den Spieler, in Petrus Mund doppelt fremd (zu lang, Wissen, das er nicht hat). Kein Tag.
   Vorschlag: “Hm. Wood and stone, like Megan said on the phone. [sigh] Show me what you carried. The village gives what it can, and it isn't much.”
3. “[clear throat] Hm. The gull. I tried for six years. You, one afternoon. Hm.” (`ereignisse_legenden.py:191`, legenden kevin.petru.laden.0). Regel: abgehackt; „Hm.“ steht in 29 seiner 76 Zeilen, in den Legenden fast immer am Anfang und oft am Ende. Zehn Bedeutungen brauchen Seltenheit.
   Vorschlag: “[clear throat] Hm. Six years I tried with that gull, Kevin. You needed one afternoon.”

### Elsa

Die Seite verlangt trocken, sachlich, schnell, Protokoll mit Funken Spaß, Fakten statt Meinungen, „First Officer“, Ausbrüche nur für „TOTÒÒÒ!“ und ihre Romane.

**Treffer**

1. “[clear throat] First Officer. I have six statements about the harbour, and in four of them you are taller than you are. I am filing the other two.” (`ereignisse_legenden.py:64`, legenden hafen.elsa.zeit.0). Protokoll und Pointe in einem.
2. “[chuckle] I asked Petru. He said hm. That is his entire statement.” (`ereignisse_legenden.py:267`, leg_hafen_elsa). Humor aus zwei Figuren zugleich.
3. “Then I'll need a form, Monsieur Leca. [clear throat] The same kind as the one for my antenna, I suppose. It's been eleven months.” (`ereignisse_verrueckt.py:26`, g1_casanova_nebel). Konkrete Zahl, Erinnerung im Satz.

**Ausrutscher**

1. “TOTÒ, I can see you behind that crate.” (`ereignisse_belagerung.py:108`, bl_elsa_hilfe). Regel: Pointen sparsam; der Satz ist das Beispiel von ihrer Wiki-Seite und steht wörtlich auch in hk_abend. Ein Running Gag lebt von Variation. Kein Tag.
   Vorschlag: “[clear throat] TOTÒ, that crate is too small for you. It was too small last time, too.”
2. “In the event of an armed attack on the commune, section nine requires this post to assist.” (`ereignisse_belagerung.py:104`, bl_elsa_hilfe). Regel: einfaches Englisch; „commune“ ist doppeldeutig (Megan sagt „hippie commune“), „in the event of“ ist Amtssprache ohne Funken. Kein Tag.
   Vorschlag: “If armed men attack the village, section nine says this post must help. [clear throat] So I'm helping.”
3. “[chuckle] This doesn't count. It's a bend. A very large bend.” (`werkzeuge/eden_rise/selfie_daten.json:186`, sf_elsa_5_posten). Regel: verkürzte Redewendung („bend the rules“), ohne Vorwissen unklar.
   Vorschlag: “[chuckle] This doesn't count. I'm not breaking the rule, I'm only bending it. Quite a lot.”

### Alon

Die Seite verlangt glatten Keynote-Ton, freundlich, Menschen wie Software (Bugs, Patches, Updates), nie laut, vor der Presse Großsprecher, sonst ruhig und genau, keine echte Person.

**Treffer**

1. “[clear throat] Last night, pirates attacked a small village in Corsica. Our security team was there in forty minutes.” (`ereignisse_cliffhanger.py:17`, bl_cliff_alon). Poliert, freundlich, mit einer echten Zahl, so wie der STIL den Gegenspieler beschreibt.
2. “Some of you have seen other videos tonight. [chuckle] Please be careful. Today, anyone can make a video.” (`ereignisse_cliffhanger.py:43`, bl_cliff_alon_siri). Ruhig und klug statt laut.
3. “Duc. [laugh] Welcome to the team.” (`ereignisse_cliffhanger.py:53`, bl_cliff_team). Der Name als Schlag, kurz genug für einen Schluss.

**Ausrutscher:** Bei fünf Zeilen gibt es keine drei echten. Die schwächste Stelle: Die Produktsprache der Seite (Patches, Updates, Menschen als Software) fehlt noch ganz.
“Zero dead. [sigh] That is what a future without fear looks like.” (`ereignisse_cliffhanger.py:18`, bl_cliff_alon).
Vorschlag: “Zero dead. [sigh] That's version one of a future without fear, and the next update is already on its way.”

## 4. Muster über alle Figuren

1. **Geteilte Formeln.** Die stärksten Romanzen-Momente laufen oft über denselben Satz: „Nobody ever asks / nobody has ever …“ steht in 27 Zeilen bei zehn Hauptfiguren (Chiara 8, Sophia 7, Siri 3, Jana 2, Lola 2 …), obwohl die Seite den Satz Sophia gibt. In `ereignisse_belagerung_nacht.py:273` und `:274` sprechen sieben Frauen exakt dieselben zwei Zeilen (“…Good. No talking, then.” und “I know. That's why it's all right.”). Dazu „Don't look at me like that“ (10 Zeilen, 5 Figuren), „Don't make it weird“ (Chiara, Siri, Yasin), „I've never asked anyone for anything“ (Lea, Petru).
   Gegenvorschlag: Die Formel bleibt bei Sophia; jede andere Figur bekommt ihre eigene Art, überrascht zu sein (Chiara bewertet es, Rosi redet über eine Maschine, Lola verliert das Satzende, Siri entschuldigt sich und nimmt es zurück). In `belagerung_nacht.py` die zwei Zeilen als Wörterbuch je Figur anlegen. Auf jeder Figurenseite eine kurze Liste „gehört anderen, nicht benutzen“.

2. **Marotten ohne Budget, Marotten ohne Einsatz.** Zu viel: Lola „Mostly“ 34 von 239, Alva „o figliolu“ 34 von 179 (K9 sagt sparsam), Maxwell „Mr. Maximum“ 60 von 67, Petru „Hm.“ 29 von 76, Sophia „Ten euros“ 21, Siri „Sorry“ 44 von 172, Jana „Sorry“ 46 von 102. Zu wenig: Megans schottische Kante (2 von 139), Chiaras Französisch und Italienisch (2), Janas Chiara-Kopien (0), Yasins ehrlicher Satz (1).
   Gegenvorschlag: Ein Markenwort höchstens einmal pro Auftritt, und nur, wo es auf etwas zeigt („Mostly the salt“ nach Petrus Tränen trägt, „Mostly the cheese“ nach Suppe nicht). Die fehlenden Marotten in Akt 3 bewusst setzen, je eine Szene pro Figur reicht.

3. **Anrede kippt in den ernsten Szenen.** Gerade wo es zählt, fällt die Matrix: Holm 9 Mal „Officer“ (gegen 16 Mal „Frankfurt“), alle in der Belagerung; Totò 5 Mal „boss“ in den Gennaro-Szenen; Petru und Lea je zweimal „Officer“; Casanova einmal „Mon capitaine“.
   Gegenvorschlag: Ein kleiner Test `tests/test_anrede.py` nach dem Muster von `test_sprite_stimmung.py`: Sprecher gegen Matrix, verbotene Anreden je Figur, Ausnahmen als Freigabeliste mit Begründung. Wenn Totòs „boss“ gewollt ist, auf `toto.md` als Moment eintragen.

4. **Stakkato unter Druck.** In Wut, Eile und Flirt fallen Figuren in Satzfetzen, die nur zu Petru (und selbst da nur selten) passen: Megans Sprachnachrichten, Alvas Flirt, Maxwells Satz-für-Satz-Dritte-Person, Rosis Überstunden, Lolas „Speedrun“.
   Gegenvorschlag: Dringlichkeit über einen langen Satz mit „and“ und „so“ zeigen statt über vier kurze. Faustregel zum Prüfen: höchstens ein Fragment pro Zeile, außer bei einer ausdrücklich erlaubten Marotte (Chiaras Bewertungen).

5. **Seltene Wörter und Redewendungen.** Gefunden: „drew“ (Rosi, Lea zweimal, Petru), „rota“, „bergerie“, „skinny dipping“, „wings of a West End theatre“, „push your luck“ (Lola, Alva), „do numbers“, „long shot“, „turn to porridge“, „gives me the creeps“, „goosebumps“, „Patrimonio“, „commune“, „Opa“.
   Gegenvorschlag: Eine Prüfliste im Stil von `kern/szene.FLOSKELN` (Wörter und Wendungen), die ein Test über alle Sprechzeilen laufen lässt. Was die Story wirklich braucht, bekommt ein einfaches Wort daneben, wie Leas „dreckly, that's Cornish for sometime soon“.

6. **Vertonung: fehlende und blinde Tags.** 89 der gesichteten Zeilen haben keinen Eintrag in `stimme_tags.json` (Abgleich über Sprecher und Klartext), aus 49 Events und Anrufen, davon 37 Events in `ereignisse_belagerung.py` (dort `Z(...)` ohne Tag). Weil der Schlüssel nur der Klartext ist, liest die Stimme jedes „Hm.“ von Petru als “[chuckle] Hm.”, auch in bg_petru_auftrag (Ton ernst, Gefühl sadness). Ähnlich: Lea lacht ([laugh]) in ihrer nervösen Bitte um Opas Seite (`ereignisse_erinnerung.py:65`, er_kevin_frist), Megan lacht doppelt (Tag und „Ahaha“).
   Gegenvorschlag: `werkzeuge/eden_rise/stimme_tags_pruefen.py` lokal laufen lassen und die Belagerungszeilen nachtaggen. Für sehr kurze Zeilen („Hm.“, „Yes.“) den Schlüssel um das Gefühl erweitern, damit ein trauriges „Hm.“ ein [sigh] bekommen kann. Lachen nie zusätzlich als Text schreiben.

**Zu Duc (Stichprobe):** Die gesehenen Antwort-Chips halten die Form aus STIL („Handlung zuerst, dann die Rede“) und sind ohne Vorwissen verständlich, oft tragen sie sogar die Erinnerung für die Antwort der Figur (Holms Bärengeschichte in `ereignisse_holm.py:95`). Eine vollständige Prüfung steht aus.

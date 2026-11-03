# Dossier Siri Lindvik & Yasin Benali (Eden Rise)

Stand: 22.10.2026 · reine Lese-Recherche · Quellen: `X:\AI\Eden` (module/eden_rise, werkzeuge/eden_rise, kern, docs, karten_neu), ST-Karte `X:\AI\RoleplayGen\cards\Eden Yacht\Siri Lindvik.json`, Lorebook-Skript `X:\AI\Eden\karten_neu\welt_rosi_siri.py`.
Eine eigene ST-Karte für Yasin gibt es **nicht**; er existiert nur als NPC im Modul, im Lorebook (W14) und in Siris Karte.

Abkürzungen: `basis` = werkzeuge/eden_rise/basis_eden_rise.py · `modulpy` = werkzeuge/eden_rise/modul_eden_rise.py · `gegst` = werkzeuge/eden_rise/gegenstaende_eden_rise.py · `missio` = werkzeuge/eden_rise/missionen_eden_rise.py · `welt` = karten_neu/welt_rosi_siri.py

---

## 1. Siri Lindvik – Steckbrief

| Feld | Inhalt |
|---|---|
| Name | Siri Lindvik, Markenname „Siri Sea · Nordic Beauty“, 2,8 Mio. Follower |
| Alter | 25 |
| Rolle an Bord | **Chartergast** (Influencerin), mit Freund Yasin in der VIP-Kabine. Im Eden-Modul: die letzten beiden Gäste der Saison (`basis:45`, modul.json `welt`). Kein Crew-Mitglied (`modulpy:320` „nicht_in_crew_szene“). |
| Herkunft | Karte: kleine Insel vor Trøndelag (Norwegen), 400 Einwohner, eine Fähre am Tag. Vater Fischer, kämpft im Inselrat gegen Lachsfarmen; wollte, dass sie in Bergen Meeresbiologie studiert. Mit 19 Schönheitswettbewerb in Trondheim gewonnen, noch in der Nacht gescoutet. Seitdem Manager, Coaches, Sprechtraining, Content-Pläne; Captions schreiben andere; **ihr Manager verwaltet ihr Bankkonto**. Vater schämt sich für die halbnackten Fotos, seit zwei Jahren kaum Kontakt; Mutter schickt Herzen unter jeden Post. **⚠ Widerspruch: das Eden-Modul macht sie zur Schwedin** (siehe Abschnitt 6). |
| Aussehen | Platinblond, lang und gestuft; meerblaue Augen; goldene, sonnengeküsste Haut; Sanduhrfigur, schmale Taille, runde Hüften, sehr volle Brust. Ein Kameralächeln auf Knopfdruck und ein echtes, schiefes, viel schöneres. |
| Persönlichkeit | Widerspruch: Millionen kennen ihr Gesicht, niemand kennt sie, sie selbst am wenigsten. Sehr tollpatschig, wenig weltgewandt (kann keine Pasta kochen, liest Karten verkehrt herum, entschuldigt sich bei Möbeln), kennt aber am 2. Tag jeden Crew-Namen. Lacht zuerst über sich selbst. |
| Stimme | Weiches Englisch mit norwegischem Singsang; trainierte Kamerastimme („Hiii guys, golden hour!“) bricht in die echte, leisere, langsamere; entschuldigt sich ständig; stellt Fragen, die niemand einer „Siri Sea“ stellt. Keine norwegischen Deko-Wörter. TTS: Chatterbox-Stimme „Siri Lindvik – ENG.wav“ (f0 ~214 Hz), im Katalog als „Schwedische Freundin von Yasin“ geführt (`X:\AI\Chatterbox\stimmen.json`). |
| Wünsche | Etwas Echtes. Eine Arbeit, die ihr gehört. Ihren Vater zurück. |
| Ängste/Geheimnis | Im Koffer der cremefarbene Wollpullover mit blauen Sternen, den ihr Vater gestrickt hat („ein Stern pro Winterabend“) – nie getragen, immer dabei. Sie ist nicht mehr sicher, ob sie irgendetwas davon will (Marke, Freund, Leben) – hat es niemandem gesagt. Albtraum: unter dem Fähranleger, findet nicht nach oben, alle auf dem Anleger filmen (Alt-Greeting „Bad Dream“). |
| Knöpfe | Bei „Siri“ statt „Siri Sea“ genannt werden; gefragt werden, was sie denkt, und Zeit zum Antworten bekommen. Never: posiert für ein Foto, das sie nicht geplant hat; sagt nie den Namen ihres Vaters vor Yasin. |
| Wissen (Karte [Knows]) | Kennt keine Crew-Geheimnisse. Sah in der ersten Nacht eine Gestalt mit etwas Messingfarbenem auf der Brückennock – hält es für den Bordgeist und ist ein bisschen stolz. Hat bemerkt, dass Yasin mit Chiara flirtet, tut so, als nicht. Hält Sophia für „mehr als eine Concierge“ (Notizbuch kommt raus, wenn Yasin redet). **Weiß nicht, dass Yasins Geld dünner ist, als es aussieht.** |
| Zu Duc | Erinnert sie an ihren Vater: einfach, praktisch, repariert statt zu posten. Dann erfährt sie, dass er in Nachhaltigkeit arbeitet – genau das, was ihr Vater für sie wollte. |

### Outfits / Sets (Karte + `ereignisse_basis.py:66`)
- **Sea Siren** (Standard): eisblaues Seidenkorsett, langer Schlitzrock, Perlenkette um die Taille, barfuß.
- **Riviera Swim**: flüssig-silberner Bikini, Chiffon-Sarong (Badeplattform).
- **Morning Ritual**: meergrüner Body, weißer Kaschmir-Wickel (Vordeck morgens, Nachtphase).
- **Saint-Tropez '69**: Wellenmuster-Seidenneckholder, weite weiße Seidenhose, goldener Kettengürtel, Tuch im Haar, große weiße Sonnenbrille (Hafen, Alvas Bar).
- **Silver Night**: flüssig-silbernes Paillettenkleid, silberne Ear Cuffs (Dinner, Piazza).
- **Dad's Sweater**: Vaters Strickpullover, Wollsocken, lockerer Seitenzopf, ungeschminkt.
- **Nude**.
Set-Regeln im Modul: `basis:454-460` / modul.json `personen.siri.set_regeln`.

### Vorlieben, Geschenke, Gericht
- `schaetzt`: empathy, charm. Lieblingsgesten: fragen, trösten, Haar (`basis:220`).
- Kategorie-Grundhaltung (`gegst:30`): Papier +, Natur +, Schmuck −, Technik −, Rest neutral.
- **Liebt (+2):** Notizbuch aus Leder, grünes Seeglas, Alvas Rose, Muschelkette der Dorfkinder („Siri trägt sie sofort“), Tim-Tam-Slam-Set, Seegras-Chips mit Limette, **Kåldolmar** (schwedische Kohlrouladen mit Preiselbeeren = ihr Lieblingsgericht, Kochbuch: +1 Ausdauer, Charisma +1, Kraft +1), exklusiv `siri_ratgeber` (+2).
- **Mag (+1):** Füller, Gedichtband, Almanach, alte Seekarte, Pin-up-Magazin, Ducs Gedicht, schöne Muschel, Wollsocken, Wollmütze, Kerzen, Messinganker, Macchia-Strauß, Korallenzweig, Goldfisch.
- **Hasst (−1):** rosa Perle (modul.json; `basis:314` hatte noch +2 – überschrieben), Designerparfum, Muschelfußkettchen, Herzbrille, Goldkette, Designer-Sonnenbrille, Silberring, Drehmomentschlüssel, Tauchlampe, Moka, Selfie-Stick, Polbrille, Schweizer Messer, Bauchnabelpiercing, **Eden-Group-Kappe**, „Kevins Rache“ (Möwenkekse).
- Lieblingsorte: **Vordeck, Solardeck** (`basis:496`). Tagesablauf: Frühstück Vordeck · Tag Sonnendeck · Dinner Achterdeck · Abend Hauptsalon · Nacht Solardeck.
- Kampf-Anhänger „Plüsch-Robbe“ (Siri, Empathie +1) – `docs/wiki/systeme/kampf.md:253`.

### Beziehungen
- **Yasin**: Freund, von ihren Managern als „Couple Content“ verkuppelt; filmt alles, behandelt sie wie Requisite.
- **Lea**: „zwei neue Mädchen“, am ersten Tag gefunden; Lea zeigt Fischzeichnungen, Siri zeigt Posen; wenn beide an Deck sind, geht etwas über Bord (`welt:58`). Nacktbaden zusammen (br_nacktbaden), Oktopus, Sonnencreme-Duell.
- **Chiara**: wollte keine Influencer an Bord und sagte es laut; zu Siri perfekter Service; Yasin flirtet vor Siri mit Chiara, Chiara bewertet ihn insgeheim mit „Zwei“ (`welt:50`). Rivalität Start 2 (`basis:93`). Siri will ihr ein Festa-Kleid leihen.
- **Rosi**: hält Influencer für nutzlos, sagte es am ersten Tag; Siri bringt ihr seitdem jeden Morgen Kaffee in den Antriebsraum (`welt:62`). Rivalität Start 2.
- **Sophia**: organisiert Siris Landgänge, Restaurants, Fotospots (`welt:54`).
- **Holm**: Siri hat schwedische Salzlakritz für sie, traut sich nicht, sie ins Krankenhaus zu schicken – „in drei Wochen kaum zwei Sätze geredet“ (Mission siri_lakritz).
- **Petru**: erinnert sie so sehr an ihren Vater, dass sie ihn kaum ansehen kann (Mission Ratgeber).
- **Lola**: findet Siris Pass in der Wäsche → Geburtstag (br_siris_geburtstag); Duschen zu zweit.
- **Megan**: weiß (Megan-Karte), dass die Schlussrate der Charter von **Siris Management kam, nicht von Yasin** – „ein Zahlungsdetail“.
- **Duc**: romanzierbar, siehe unten.

---

## 2. Yasin Benali – Steckbrief

| Feld | Inhalt |
|---|---|
| Name | Yasin Benali, Kurzname „Yasin“, Pronomen er |
| Alter | 29 |
| Rolle | Chartergast, Siris Freund und „Co-Creator“; aus Paris, verkauft **Online-Trading-Kurse** (`basis:468-469`, Lorebook W14 `welt:34`). |
| Auftreten | Teure Uhr, Bargeld für jedes Trinkgeld, Handy filmt immer; flirtet mit jeder Frau der Crew, auch in Siris Hörweite; nennt die Crew „my team“; behandelt Siri wie Requisite. Gestrandet: wütend und gelangweilt. Die Crew ist höflich, mag ihn kaum jemand. |
| Geld | Dünner, als es aussieht (Siri-Karte [Knows]); Charter-Schlussrate zahlte Siris Management (Megan-Karte). |
| Verletzliche Stelle | Goldene Sonnenbrille „Monaco“ – Geschenk seines Vaters, das Einzige, was er nie filmt; bittet nicht gern (Mission yasin_brille, `missio:367-372`). |
| Stimme | Chatterbox „Yasin Benali – ENG.wav“; Modul `stimme: Yasin Benali`. Sprechstil aus job_zeilen: „bro“, „That's business“, „I only work with winners“, „Not bad for a guy on a salary“, „This is why I don't hire locals“ (`basis:682-690`). |
| Romanze | **nein** (`romanzierbar: False`). Vertrauen-Start 0 (`modulpy:153`). |
| Aufenthalt | Standard Hauptsalon · Tag Sonnendeck · Nacht VIP-Kabine. Set nur „Standard“. |
| Geschenk-Reaktion | „Yasin takes it, films it immediately and turns the moment into content about himself.“ (`modulpy:338`) |
| Liebt (+2) | Proteinriegel, Designer-Sonnenbrille, Selfie-Stick, Protein-Pancakes, **Bibimbap** (Kochbuch: Krit +5 %, Mut +1), drei „Designer“-Taschen von Totò (Vertrauen +8), exklusiv Goldbrille. |
| Mag (+1) | Alkohol (Myrte, Single Malt, Limoncello, Cap Corse), Schmuck, Parfum, Werkzeug/Technik, Party-Kram (Konfetti, Schärpe, Fächer, Lichterkette, Ukulele), Eden-Cap. |
| Hasst (−1) | Papier (Notizbuch, Füller, Gedichtband, Seekarte …), Natur (Seeglas, Muschel, Rose …), Wollsocken, Tim Tams. Kategorien `gegst:36`: Alkohol/Schmuck/Technik/Party +, Papier/Natur −. |
| Beziehungen | Siri (Requisite), Chiara (flirtet bei jeder Mahlzeit), Lea (1000-€-Umschlag „Für dich, Süße“), Totò (feilscht um Zigarren für ein Reich-aussehen-Video), Sophia (Sonnenaufgangs-Idee, s. Story), Duc („First Officer“, Bargeldangebote). |
| Kampf | Rede-Gegner-Beispiel: K.o. → er verlässt das Boot, Siri hasst Duc; überredet → Yasin bleibt, Siri beginnt Beziehung mit Duc, Yasin akzeptiert („alles war ohnehin geplant“) – `docs/wiki/systeme/kampf.md:172-173`. Gegner-Sprite „YasinDrone“ (Yasin wütend + Drohne, Luft/Flieger) – `docs/archiv/kampf_gegner_bereit.md:21`, `werkzeuge/kampf_balance_v3.py:70`. Anhänger „Plüsch-Falke“ (Krit +5 %). |

---

## 3. Mechanik

### Siri
- **Romanzierbar: ja** (`basis:454`), aber `vergeben` bis Flag `siri_frei` – „sie ist noch mit Yasin zusammen“ (`modulpy:327`). Intime Geschenke lehnt sie bis dahin ab (`kern/handel.py:422-433`).
- Start: Vertrauen 1, Begehren 1; Spannung chiara_siri 2, rosi_siri 2 (`basis:89-93`).
- **Uhr `siri_marke`** „Siri löst sich“, 6 Segmente; voll → „Siri macht Schluss mit Yasin“ → Flag `siri_frei` (`basis:106`, `kern/showrunner.py:501`).
- Intim: mag Spooning, Cowgirl, Caressing, Lotus; nein: Facefuck (`basis:232`). Heat-Leiter der Karte: 1 höflich/tollpatschig · 2 sucht ihn ohne Kamera · 3 Berührung, gehaltene Hand, zieht sich zurück · 4 **erst nach Trennung von Yasin**, langsam, Licht aus · 5 alles, ohne Pose. Überspringt nie eine Stufe; mit Yasin nie über 3.
- Spielbogen (ST, `welt:193-232`): Achsen Nähe (Start 1), Echt (1), **Marke** (Start 6; bei 2 ruft sie ihren Vater an, bei 1 macht sie Schluss). Steigt: „Siri“ statt „Siri Sea“, fragen und warten, sie schlecht sein lassen, Palstek bemerken, zwei Minuten ohne Kamera. Fällt: mit „Siri Sea“ flirten, Captions zitieren, **sie fotografieren**, herablassend, Vater/Insel verspotten, Regeln brechen solange Yasin im Bild ist.
- VIP-Kabine: Zugang mit Vertrauen Siri 4, in Begleitung oder List-Wurf 15 mit Risiko „Yasin erwischt Duc“ (`basis:399-401`).
- Bordregel **„Kamera aus nach 22 Uhr“**: täglich Siri +2 Vertrauen, Yasin-Content-Missionen nur tagsüber (`ereignisse_basis.py:92`).
- Storylets (`basis:524-532`): `siri_no_signal` (Tag, Sonnendeck: kein Internet, Yasin panisch, Siri heimlich erleichtert) → `siri_knots` (Vertrauen 2, Badeplattform: perfekter Palstek, Vaters Anleger) → `siri_the_call` (Nacht, Solardeck, Vertrauen 4 + Uhr ≥4: Vaters Pullover, Anruf-Knopf).
- **Persönliche Missionen** (`missio:147-153, 304-317, 359-365`):
  - `siri_photos` „Fotos ohne Yasin“ (T2–7, Charme 11, persönlich): Bilder, auf denen sie nicht posiert; Duc hält die Kamera.
  - `siri_samples` „Meeresproben sammeln“ (T3–7, Wahrnehmung 11, nach photos, Vertrauen 2): Seegras-Proben; Codex: sie will Meeresbiologie studieren, hat es niemandem gesagt.
  - `siri_ratgeber_1/2` „Ein Buch für Siris Vater“ (T3–7): Netzgarn für Petru besorgen, dann Empathie 13 – Duc stellt die Fragen; Lohn Item „Ratgeber: Die Kunst der Fischerei auf Korsika“ (von Hand gebunden, für ihren Vater; Geschenk an Siri +2), Petru +4. „Bewahr es auf, bis ich nach Hause fahre.“
  - `siri_lakritz` „Salzlakritz für Holm“ (T3–7, Empathie 11): über Elsa nach Ajaccio; Holm +8; Antwort „Tack.“
- Andenken/Items: Knotenarmband `siri_knot` (Mut +1; blaues Segeltau im Palstek), Seidenhalstuch (Charme +1, aus Mission), Dankeskarte (Geburtstag), Haarband (Tanz-Event).
- job_zeilen (Angebot/Erfolg/Fehlschlag/Patzer), z. B. „Can I ask you for something? Just us. No camera, no Yasin.“ (`basis:650-661`).
- Epilog (`kern/abschluss.py:204-209`): Partner – „Siri postet nichts von diesem Abend“; hoch – löscht den Party-Clip („Das war nicht ich“), fragt nach Ducs Nummer; mitte – letztes Crew-Foto, Duc nicht rausgeschnitten; tief – „mit Yasin beim ersten Taxi. Sie dreht sich nicht um.“

### Yasin
- Nicht romanzierbar, Vertrauen 0.
- **Uhr `yasin_video`** „Yasins Video“, 5 Segmente, verdeckt; voll → „STRANDED ON A BILLIONAIRE YACHT“ online, Ruf −2, Codex (`basis:107`, `showrunner.py:502-507`). Läuft jeden 2. Tag +1, solange nicht `video_gestoppt` – „voll wird die Uhr nur, wenn Duc ihm hilft“.
- Zufallsereignis `yasin_live`: Livestream mit den letzten mobilen Daten, solange Video-Uhr < 5 (`basis:571`).
- Missionen: `drone` (Drohne neben dem Anker, 6 m, Mut 13, 150 € bar; „zahlt und filmt dich dabei“), `guest_breakfast` (Eggs Benedict ohne Strom, Charme 12, 80 €), `yasin_brille` (Goldbrille, 8 m, Strömung, Mut 14, 120 €; „Yasin ist nicht da, als du auftauchst. Gib sie ihm selbst.“), indirekt `chiara_complaint` (droht mit Ein-Stern-Bewertung für die Crew).
- Tag-2-Komfortwahl: „Yasins Aufnahmen bleiben aus“ (Flag `komfort_aufnahme`, `story_buehne.py:94`).
- Yachtware: beschwert sich lautstark über fehlende Bademäntel.

---

## 4. Ereignisse (ereignisse.json; Tage = altes 7-Tage-Fenster)

**Bordrat (Nacht):**
- `br_yasins_angebot` (T2–5, nur vor siri_frei): 500 € für Crew-Auftritt in „Gestrandet mit Influencer“ – Geld/Ablehnen/Nur Freiwillige/Bordregel Kamera aus; Geld → Video-Uhr +1.
- `br_siris_geburtstag` (T2–6): Lola findet Siris Pass, morgen Geburtstag; Sophias Frühstück ohne Kameras (Siri +8, Marke-Uhr +1, Dankeskarte) vs. Yasins Konzept (Video-Uhr +1).
- `br_singen_ohne_strom` (T2–6): Lola singt, Siri nur ohne Kamera, Yasin hat das Stativ schon raus.
- `br_siri_umzug` (T2–6, vor siri_frei): Siri will ein Bett in einer Crew-Kabine; Yasin steht im Gang.
- `br_trinkgeld` (T2–6): Yasin gibt Lea 1000 € („Du darfst dich bedanken“).
- `br_drei_minuten` (T2–5, Strom ≤5): Duschplan; „Die Gäste verzichten“ → Siri +6, Yasin −8.
- `br_gaestekabinen` (T2–4): Megan will Gästekabinen räumen und Minibars zählen lassen.
- `br_dorfkinder` (T2–6): Führung für Dorfkinder → Muschelkette, Siri +6.
- `br_ein_tisch`, `br_gemeinsam_duschen` (T3–6), `br_nacktbaden` (Lea + Siri, Elsas Scheinwerfer).

**Handy:** `hy_siri_ungeschminkt` (T2–7 Nacht, Vertrauen ≥3: Videoanruf ohne Filter vom Vordeck) · `hy_yasin_collab` (T2–5 Tag: Duc als „der echte Kapitän“ im Video gegen Satellitendaten).

**Gags/Duelle:** `g1_siri_tanz` (Yasin schläft, Siri bringt der Crew einen Tanz bei, ohne Kamera – Haarband) · `g1_yasin_geste` (T3–5 Abend: Herz aus Kerzen, Live-Liebeserklärung, Siri erstarrt) · `g1_siri_pullover` (T3–7 Frühstück, Vertrauen ≥3: Siri trägt Ducs Pullover, Yasin erkennt ihn) · `gv_siri_yasin` (T3–6: Yasin filmt sie mit vollem Mund, sie sagt erstmals laut nein) · `g1_kalte_dusche`, `g1_blaskapelle` (Siri filmt lachend), `g1_toto_pizza`, `g1_lea_sonnenbrand` · `gv_sonnencreme` (Siri vs. Lea), `gv_oktopus` (Siri weiß viel über Oktopusse → Seeglas), `gv_festa_kleid` (Kleid für Chiara, T4–5), `gv_festa_platz` (T5: Stuhl neben Duc, Siri vs. Sophia), `gv_zigarren` (Yasin vs. Totò) · Duelle mit Yasin/Siri als Zuschauer (`du_koch_toto`, `du_harpune_chiara` – Option „Yasins Kamera ins Wasser schubsen“, `du_tiere_lea` – Siri führt Buch) · Auftritte `auf_karaoke` (Duettpartnerin wählbar), `auf_gitarre`, `auf_herkunft`.

**Storylets:** `guest_dinner` (Yasin beschwert sich, Siri entschuldigt sich für ihn), `storm_night` (T3), `la_festa` (T5) – `basis:510-566`.

---

## 5. Story, Woche, PR-Rolle

- **Prämisse im aktuellen Modul** (modul.json `welt`, `basis:40-60`): Saison vorbei, Siri und Yasin sind die letzten Gäste; nach der Abschiedsparty sollte die Yacht zur Werft nach Calvi; in der Nacht fällt der E-Antrieb aus, sie treibt in die Bucht von Cala d'Orsu. Alte Begründung, warum die Gäste bleiben: „die nächste Fähre aus dem Dorf geht in einer Woche“ (`basis:45`).
- **Warum Cala d'Orsu (Stand story.json):** gemeinsamer Fakt `r_02` – „Reiseplan v2: Nachtfahrt nach der Party, **Morgenhalt in Cala d'Orsu (Gästewunsch Sonnenaufgang)**, eingereicht über Sophia, genehmigt von Holm“. Fakt `h_12`: Yasin wollte „den Sonnenaufgang für die Drohne“. Lola backt in der Blackout-Nacht für ein „Sonnenaufgangsfrühstück“. → Der Sonnenaufgangs-Dreh der Gäste ist schon heute der Story-Grund für die Bucht.
- `r_03`: Yasin hat eine Lastgrenze am Heckverteiler unterschrieben (≤2 kW, nur Bordladestation, keine Mehrfachadapter). `r_06`: Gruppenfoto 21:32 im Salon (Kamerazeit vs. Steuerungsanzeige – Uhrzeitabgleich-Mechanik).
- **Wochenbogen** (`story_eden_rise.py:221-231`, `story_buehne.py:39-56`): Tag 1 Party – Wahl „Wem hilfst du zuerst?“: Chiara / Rosi / **Siri („will kurz aus einer Aufnahme raus“, will: „Escape Yasin's camera for five minutes“)** → Vertrauen +2, Flag `auftakt_hilfe_siri`. Tag 2 Lage mit Holm: Verzicht-Option „Yasins Aufnahmen bleiben aus“. Tag 5 Festa (`story_buehne.py:263-268`, anwesend Chiara/Lea/Siri): „Siri entscheidet selbst über ihre Beziehung und ihre öffentliche Darstellung. Yasin setzt Material nur ein, wenn er es besitzt und einen Anlass hat.“ (`story_eden_rise.py:375`); Siri will: „Decide for herself who she is tonight.“
- **Social Media / Presse** heute: Yasins Video-Uhr („STRANDED ON A BILLIONAIRE YACHT“, Ruf −2), `yasin_live`, `br_yasins_angebot` („Gestrandet mit Influencer“), `hy_yasin_collab` („der echte Kapitän“), Ein-Stern-Drohung, Fotografen mit Teleobjektiv im Schlauchboot (Alt-Greeting „Long Lenses“), Live-Q&A „Does he cheat on you?“ (Alt-Greeting „Live“). Siri: Gegenpol – Momente ohne Kamera, „Fotos ohne Yasin“, Epilog „postet nichts“. Sponsoren: nur angedeutet (Glow, „der Sonnencreme verkauft“; Manager verwaltet Konto; Management zahlte die Charter).
- **Neue Prämisse (docs/archiv/BRAIN_TRUST_UEBERGABE.md:158-169)**: Megan schickte die Yacht in die Bucht, damit Siri, Yasin und andere Promis Guerilla-Marketing für die Bucht machen; Alon will mit Katastrophe/negativer Presse den Preis drücken; „Resort“ = Forschungseinrichtung (Halsbänder, Akt 3). **Offen:** Siris Post **#StrandedInParadise**, der Alons Presse ins Positive dreht. Figuren-Runde Paar 1 = Siri + Yasin (läuft). Duc wünscht weitere Promis (u. a. eine Schauspielerin an Bord).

---

## 6. Widersprüche & Altlasten (7-Tage-Struktur) – und Brücken zur neuen Prämisse

### Widersprüche
1. **Nationalität**: Karte/Lorebook = Norwegerin (Trøndelag, Bergen, „norwegischer Singsang“, `welt:31`). Modul = Schwedin: Vater „fischt seit vierzig Jahren vor Göteborg“ (`missio:305`), schwedische Salzlakritz, Kåldolmar, Rosi „They don't take orders from Sweden“ (`ereignisse_gag1.py:134`), Stimmenkatalog „Schwedische Freundin“. Holm ist Norwegerin, antwortet aber „Tack“ (schwedisch; norwegisch wäre „Takk“). → Eine Linie festlegen (Vorschlag: Norwegen beibehalten wegen Holm-Verbindung und Karte; dann Göteborg→Trøndelag, Kåldolmar→z. B. Fårikål/Fiskesuppe, „Tack“→„Takk“, Rosi-Zeile anpassen; oder umgekehrt Karte auf Schweden umschreiben).
2. **Zeitpunkt**: Karte = Mitte August, laufende Charterwoche vor Saint-Tropez, Heimathafen Antibes, Gäste nur „diese Woche“. Modul = Saisonende, Abschiedsparty, letzte Gäste. Mission siri_lakritz: „in drei Wochen kaum zwei Sätze“ und `bekannt_start` „seit drei Wochen an Bord: Crew und Gäste“ → Gäste schon drei Wochen an Bord, passt nicht zu „diese Woche“.
3. **Calvi/7 Tage**: Ziel „bis Tag 7 in Calvi“, Megan „innerhalb der Woche“, Fähre „in einer Woche“ als Grund für das Bleiben, `zeitraster tage: 7`, Fixpunkte T3 Sturm / T4 Aufdeckung / **T5 Festa** / T6 point of no return / T7 letzte Nacht. Neu: 21 Tage, Festa am Ende (Akt 3).
4. **Event-Fenster** durchgehend in Tagen 2–7 (`tage: [2,5]`, `[2,6]`, `[3,7]`, `gv_festa_kleid [4,5]`, `gv_festa_platz [5,5]`, `g1_yasin_geste [3,5]`); Uhren für 7 Tage kalibriert (siri_marke 6, yasin_video 5, Yasin dreht jeden 2. Tag) – `docs/wiki/systeme/tage_erkundung.md:11` vermerkt bereits, dass die Uhren für 21 Tage neu eingestellt werden müssen.
5. **Esterel/Margot/Antibes** stammen aus dem Yacht-Lorebook (Riviera-Saison); Saint-Tropez in drei Alt-Greetings. In Korsika-Setting nur noch als Vergangenheit verwendbar.
6. Rosa Perle: `basis:314` Siri +2, modul.json final −1 (gegst-Matrix überschreibt) – bewusst prüfen.
7. Epilog „mit Yasin beim ersten Taxi“ setzt Abreise an Land voraus (früher Calvi) – mit Festa-Finale im Dorf neu verorten.
8. Kampf-Konzept „Yasin akzeptiert, alles war ohnehin geplant“ (`kampf.md:173`) widerspricht dem Bild des besitzergreifenden Yasin – oder ist ein wertvoller Grauton (die Beziehung war nur Vertrag).

### Brücken zur neuen Prämisse (Vorschläge)
- **Sonnenaufgang = Megans Auftrag**: Der „Gästewunsch Sonnenaufgang“ (r_02) wird zum gebuchten Content-Termin: Megan/Eden Group (ggf. mit Madame Casanova, die die Yacht ohnehin als Festa-Attraktion will) bezahlt Siris Management für eine Guerilla-Kampagne „Cala d'Orsu“. Passt zur Megan-Karte (Schlussrate kam von Siris Management → Geldfluss existiert schon) und erklärt, warum die beiden nach dem Ausfall bleiben: Vertrag bis zur Festa, nicht „nächste Fähre“.
- **Zwei Posts als Achse**: Yasins „STRANDED ON A BILLIONAIRE YACHT“ ist genau die Negativpresse, die Alon braucht; Siris #StrandedInParadise dreht sie ins Positive. Die beiden Uhren (`yasin_video` vs. `siri_marke`) können zu einem Presse-Tauziehen über 3 Akte werden. Yasins dünnes Geld macht ihn käuflich – Alon (A.V. Estates) könnte ihn als „Sponsor“ ködern, ohne dass Yasin den Plan versteht (Grauton, kein Bösewicht).
- **Siris Herzensthema trifft Alon**: Meeresbiologie, Seegras, Vater gegen Lachsfarmen → ihre Proben (`siri_samples`) können in Akt 2/3 etwas über die „Forschungseinrichtung“ zeigen (Abwasser, Sperrzone, markierte Tiere/Halsbänder). Ihr Wunsch „eine Arbeit, die mir gehört“ wird ihr Akt-3-Ziel: eine eigene, echte Kampagne für die Bucht.
- **Der „Geist“ mit Messing auf der Brückennock** (Karte [Knows]) lässt sich als unscheinbarer Akt-1-Hinweis auf eine fremde Person an Bord vor dem Ausfall umdeuten.
- **3 Akte für die Uhr `siri_marke`**: Akt 1 kein Netz/Palstek/Kamera-aus-Regel, Akt 2 Anruf beim Vater (Marke 2), Akt 3 Trennung + Entscheidung auf der Festa („Wer bin ich heute Abend“).
- **Fähren-Begründung** ersetzen: Vertrag/Kampagne + Megans Bitte, + später Alons Presse als Grund, warum Yasin bleiben *will* (Story-Gold).

---

## VERDECKT – Fall-Rollen (nicht im Chat nennen)

Quelle: `X:\AI\Eden\module\eden_rise\story.json` (`faelle`, `verdaechtige`), gebaut aus `werkzeuge\eden_rise\story_faelle.py`. Ziehung in modul.json `wahrheit.vorrat` (alle `enthuellung_ab_tag: 4`).

- **Verdächtigenliste** (`story.json verdaechtige`): chiara, lea, sophia, rosi, **yasin**. Siri ist nie verantwortlich und nie Verdächtige; Ermittlungsschwelle Yasin = 1 (`modulpy:346`).
- **Siris Auftakt-Erinnerung je Fall** (wenn Duc ihr auf der Party hilft, `fall.auftakt.siri`): F1/F4/F6 `h_24` (Siri atmet auf dem Achterdeck durch; Yasins Geräte laden an der Ladestation in der Messe = entlastend) · F2 `f2_13` (Lea zu Siri: „Morgen früh fahren wir genau drüber.“) · F3 `f3_19` (Yasin schwärmt seit Mittag vom Sonnenaufgang – seit er bei Sophia war) · F5 `f5_14` (Yasins Geräte laden an einem **roten Mehrfachadapter in der Tendergarage**).
- **Siri als Zeugin (alle Fälle)**: `h_06` Alibi Lea + Siri 02:00–03:30 Vordeck, Meeresleuchten · `h_10` Siri sah Sophia gegen 02:45 auf dem Sonnendeck telefonieren · `h_19` Yasins Clips ab 05:30 durchgehend (Wissende Yasin, Siri).

### fall_1 (Chiara, „Übung auf der Brücke“)
Yasin/Siri nur Hintergrund: Siri-Alibi für Lea, Yasins Geräte an der Messe-Ladestation (`h_18`, 1,8 kW 05:30–06:40, Heckverteiler ohne Auslösung) – entlastet Yasin.

### fall_2 (Lea, „Die Strecke, die nicht im Plan stand“)
Siri ist Mitwisserin von Leas Margot-Motiv (`f2_12`, Wissende lea + siri) und hörte auf der Party „Morgen früh fahren wir genau drüber“ (Zeitleiste T1 20:40, sichtbar für Siri + Duc). Yasin entlastet wie F1.

### fall_3 (Sophia, „Der Gefallen“)
Sophia schlägt Yasin T1 13:10 den Sonnenaufgang vor; Yasin T1 13:20 per Chat an Siri: „Sophia meint, Sonnenaufgang in Cala d'Orsu wäre Gold“ (`f3_11`; Wege: Siri zeigt den Chat freiwillig / Yasin zeigen lassen). Yasin: „Der Sonnenaufgang war Sophias Idee“ (`f3_10`, wahr). Sophias Lüge `f3_13`: „Yasin wollte unbedingt den Sonnenaufgang.“ → Yasin ist hier Werkzeug von Sophias Ausrede; Siri ist Schlüsselzeugin.

### fall_4 (Rosi, „Die harmlose Verzögerung“)
Siri/Yasin nur Hintergrund wie F1.

### fall_5 (**Yasin**, „Das Bild, das bleiben sollte“)
- Kern: lädt für den Sonnenaufgangsdreh sechs Drohnenakkus, LED-Panels und Laptop über Mehrfachadapter „YB-CREW 3“ am Heckverteiler (~4,6 kW) gegen die unterschriebene 2-kW-Grenze; Abzweig löst aus und trennt die Querkupplung; Totò weigert sich („Frag Rosi“), Yasin legt selbst wieder ein (06:25) → Querkupplung unter Last, R2, LM3 fällt aus (06:28). Seine Kamera läuft die ganze Zeit. Adapter verschmort, landet im Abfallkorb der Tendergarage; 07:10 schickt er Siri den Rohclip für ihre Story-Auswahl.
- Lügen: `f5_10` „nur an der Ladestation in der Messe geladen, beim Flackern oben an Deck“; `f5_11` „nur meine Akkus abgesteckt“.
- Beweise: `f5_05` Adapter (Kommandanten-Anordnung, Kamerakiste öffnen, ab T4) · `f5_06` Etiketten „YB-CREW 1–6“ (**Siri** kann gefragt werden) · `f5_07` Rohclip (**Siri um ihre Kopie bitten** oder Yasins Tauschangebot) · `f5_08/09` Totò · `f5_14` Party-Erinnerung via Siri-Hilfe. Lola-Tipp: „Siri hat das ganze Video. Sie redet nur nicht drüber.“
- Gegenhandlungen: T2 Nacht gekürzter Clip online („Erster Offizier feiert, während die Yacht stirbt“, Zeitsprung 03:02→06:28; Ruf −1, Megan ruft an) · T3 Nacht versteckt Adapter in der Kamerakiste · T4 Tag Angebot: Original gegen Berichtsformulierung „Ladestation fehlerhaft“ (Flag `yasin_angebot`, Annahme → `duc_schuldet_yasin`).
- Geständnis: nie freiwillig; bei voller Kette räumt er Belegtes ein. Kernsatz: „You need an explanation. I need my people to still believe me. We could both get what we need.“
- Wiedergutmachung-Regel: **Siris Selbstbestimmung ist von seiner Schuld getrennt** – sie darf ihn in jedem Fall verlassen; ihre Freiheit ist keine Belohnung für den richtigen Verdacht.
- Holm Tag 1: „Um zwanzig nach sechs hat es am Heck ausgelöst … Frag Toto.“

### fall_6 (niemand, „Niemand an diesem Tisch“)
Yasin unterschreibt die Unterschriftenliste gegen Rosi (`f6_12`, mit Totò, Chiara, Lola) – er ist Teil des Sündenbock-Mobs.

### Altlasten mit Fallbezug
- Alte 4-Wahrheiten-Variante in `basis:120-136`: Variante „yasin“ – schweres Ladegerät an der Gästesteckdose, Kurzschluss, verbranntes Kabel versteckt, Hinweise „Brandgeruch in der VIP-Kabine“, „Yasin lügt über sein Ladegerät“. Durch fall_5 ersetzt, steht aber noch im Builder; `kern/showrunner.py:453` löst den Batteriebrand in Nacht 6 bei ungelöster Wahrheit „wette“/„yasin“ aus (altes System).
- Zur neuen Prämisse (Alon manipulierte den Motor vorher, der Fall-Auslöser hat es nur ausgelöst): In F5 passt das besonders gut – Yasins Überlast wäre der Auslöser, Alons Manipulation die eigentliche Ursache; Yasins gekürzter Clip ist dann unfreiwillig Alons Negativpresse. Ebenso F3: Sophias „Sonnenaufgang“ und Megans Marketing-Plan können verschmelzen (wer den Halt in der Bucht wollte, wird mehrdeutig).

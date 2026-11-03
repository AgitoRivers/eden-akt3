# Dossier: Megan McAllister & Alon (A.V. Estates)

Stand 22.10.2026 · reine Recherche (nichts im Repo geändert). Basis: X:\AI\Eden (module/eden_rise, werkzeuge/eden_rise,
kern, karten_neu, docs), X:\AI\RoleplayGen\cards\Eden Yacht, X:\AI\PromptStudio, ST-Lorebook „Eden Yacht“.
Pfade relativ zu X:\AI\Eden, sofern nicht anders angegeben. Vertrauens-Deltas in Events sind **Punkte** (8 Punkte = 1 Stufe,
kern/zustand.py:14; Skala 0–5).

> Wichtigster Befund vorab: **Megan ist voll ausgebaut** (Karte, Lorebook, Sprites, Laden, 17 Events, 4 Missionen, 6 Bühnenszenen,
> eigene Story-Mechanik). **Alon existiert nur in Planungs-Docs und als Kampf-Sprite/Balancing-Eintrag** – keine Karte,
> kein Lorebook-Eintrag, kein Vertrauenswert, kein Event, keine Mission, kein Eintrag in modul.json/story.json/kaempfe.json.

---

## 1. Megan McAllister

### 1.1 Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | Megan McAllister | Karte, modul.json:5292 |
| Alter | 38 | karten_neu/megan.txt, cc_figuren_lola_megan_holm.py:50 |
| Herkunft | Edinburgh; einzige Tochter eines Richters und einer Schulleiterin („aufgewachsen mit Regeln und schöner Handschrift“) | megan.txt (depth) |
| Werdegang (Karte) | mit 19 Stewardess, zehn Saisons auf See, mit 25 Chefstewardess, dann Büro in Monaco; schnellste Flottenmanagerin der Eden Group; eine lange Verlobung, per E-Mail beendet | megan.txt |
| Werdegang (neu, Prämisse) | Flottenmanagerin, **studierte Nautik + Schiffbau** → weiß, dass Überlast allein keine Explosion auslöst | START.md:152ff |
| Rolle/Job | Flottenmanagerin („Fleet Manager“ in Karte/Lorebook; „Fleet Director“ in modul.json, buehne.json, Preset) der Eden Group; elf Yachten, Budgets, Crews, Werften, Versicherer; Glasbüro über Port Hercule, Monaco; Eden-Shop per Videoanruf | megan.txt, modul.json:407, 5292 |
| Persönlichkeit | spielt den Anime-Bösewicht-Boss und genießt es (Pausen, Drohung mit Lächeln, wirbelnder Mantel) – halb Theater, halb sehr gute Managerin; besorgt Unmögliches (Werftfenster, Hubschrauber, Ersatzteil aus Genua) und schickt die Rechnung im selben Satz; respektiert Fristen, Belege, Leute mit Beweisen statt Meinungen; keine Geduld für Ausreden. modul.json: „cunning, strict, ruthlessly competent … actually funny, a little mad and very sharp; bored by people who agree with her, rewards cleverness even against her“; schottische Kante bei Wut („aye, wee, dinnae“); Metaphern Schach, Haie, Feuer | megan.txt, modul.json:5292 (beschreibung) |
| Widerspruch / Wunsch | furchteinflößendster Mensch der Eden Group, wünscht sich heimlich, dass jemand über ihre Witze lacht. Will: perfekte Saison, elf Yachten, null Zwischenfälle – und einen Menschen ohne Angst vor ihr | megan.txt (personality) |
| Wunde | Ein Gast ließ sie mit 19 bis 2 Uhr nachts Handtuchschwäne falten, weil einer „traurig aussah“ | cc_figuren_lola_megan_holm.py:54 |
| Geheimnis | wird schlimm **seekrank**, kann keine Nacht auf See verbringen; schaut nachts Anime ohne Ton und weint bei den Enden; Schublade voller Papierschwäne | megan.txt [Geheimnis] |
| Marotten | legt vor jeder Drohung die behandschuhten Fingerspitzen aneinander; faltet nervös Serviettenschwäne und zerknüllt sie; „Mwahaha. That was a joke.“ | megan.txt, modul.json:6239 |
| Nie | wird laut; sagt danke ohne Bedingung | megan.txt |
| Stimme | präzises Edinburgh-Englisch, langsam, gefährlich; „First Officer“ wenn verärgert, Name wenn nicht; TTS-Stimme **„Sera“** (en/de) | Karte extensions.stimme, modul.json personen.megan.stimme |
| Aussehen (Karte) | langes gestuftes kastanienrotes Haar, helle Haut, Full Glam, scharfer Lidstrich, rote Lippen, **grüne Augen**, groß, langbeinig, schwarze Lederhandschuhe bei jedem Wetter, Mantel als Cape über den Schultern | megan.txt |
| Aussehen (Prompt Studio) | Preset `Yacht_Megan`: Base-/Fashion-Prompt „razor-sharp sleek copper-red **bob** with a blunt straight fringe, emerald-green eyes“, Bösewicht-Lächeln; Sprite-Prompt dagegen „light blue eyes“ + Tags Long Layered/Auburn Red; Identitäts-LoRA `Megan_Fox_KREA2` (1.0) | X:\AI\PromptStudio\presets.json, set_presets.json |
| Sets/Outfits | **Boardroom** (Standard): schwarzer taillierter Power-Suit, weiße Seidenbluse hochgeschlossen, langer schwarzer Mantel als Cape, schwarze Lederhandschuhe, goldener Anker, Stilettos. **Inspection** (an Bord, alle Räume): weißes zweireihiges Blazerkleid mit Goldknöpfen im Kapitänsstil, goldener Anker, rosa Perlenkette, goldene Uhr, goldenes Seidenband im Haar, weiße Handschuhe. Drittes Studio-Kostüm **Domina** (goth_vinyl_white, nicht im Spiel verwendet) | decks.json outfit megan_boardroom/megan_inspection; modul.json:5292 set_regeln |
| Hintergründe | `eden_hq_megan_office(.png/_night)`: schwarzes Marmor-Eckbüro, Glaswand über Port Hercule, gläsernes Schachbrett, smaragdgrüner Stift, weißer Leder-Thron, Flottenkarte mit elf Goldlichtern; außerdem `eden_lobby` (goldener Anker) | decks.json, ereignisse.json |
| Mag (Geschenke) | Lolas Kekse („isst keinen Zucker. Außer diesen.“), Single Malt aus Islay, Designerparfum, Füllfederhalter, Espresso-Martini-Tiramisu, **Kartoffel-Lauch-Suppe** („das Einzige, was Megan auf See bei sich behält“), Crew-Karte (+2); Haltung: Alkohol +, Schmuck + | gegenstaende.json:84, modul.json items |
| Mag nicht | Konfetti, Lamingtons, Chili Noodles; allgemein Essen −, Natur −, Party −; die meisten Snacks/Natur-Andenken/Eden-Cap −1 | gegenstaende.json, modul.json items.*.geschenk.megan |
| Kinks/Hitze (Karte) | Hitze 1–5 (kalt → Name/länger am Telefon → Handschuh aus → abgeschlossenes Büro, Kampf um Kontrolle → alles, „sie zählt mit“); Motor: lächelnder Widerspruch, Lachen, Belege, Pünktlichkeit; fällt bei Kriechen, Lügen, Zeitverschwendung, Blamage vor Kapitänen | megan.txt |

**Beziehungen**
- **Duc:** der Einzige, der sie nicht ernst nimmt (behandelt sie wie eine leicht verrückte Tante); sie kann nicht entscheiden, ob sie ihn feuert oder behält. Im Spiel: Erster Offizier, ab Tag 2 Kommandant.
- **Crew:** kennt sie nur aus der Akte: Chiara „hervorragend und laut“, Sophia „charmant und teuer“, Lea „neu“, Lola „die Köchin, die Quittungen verliert“; die Crew hat Todesangst vor ihr. Rosi steht nicht stramm (megan_inspektion). Lola will ihr eine von allen unterschriebene Karte schicken („Everyone hates the boss … that's lonely“, missionen.json:1169).
- **Holm:** nimmt ihre Anrufe im Stehen entgegen; die einzige Kapitänin, die sie nie um etwas bittet; erkennt Megans Laune am ersten Wort (holm.txt).
- **Sophia:** Duell-Paar (gv_megan_sophia: „Darling, I invented the studies“).
- **Totò:** wird von ihrer Drohne gejagt („Mister Esposito. What's in the box? … Running is a confession.“, g1_drohne).
- **Siri/Yasin:** neu (Prämisse): Megan hat die Yacht für Guerilla-Marketing der Promis/Gäste in die Bucht geschickt.
- **Eden Group:** loyale Topmanagerin; neu: arbeitet **unwissentlich für den Deal** mit A.V. Estates, der ihr Schiff fast versenkt hat → Wende in Akt 3.
- **Alon:** im Code keine Verbindung. Prämisse: Sie „bringt den Vertrag“ (Thema 1) und sagt an Tag 5 am Telefon leise „A.V.“ (Vorbote).
- **Casanova, Petru, Adrien, Wolff:** keine direkte Beziehung in den Daten. Petru ist alternativer Ersatzmodul-Lieferant neben Megan (story_eden_rise.py:100).

### 1.2 Mechanik

- **Vertrauen:** Start 0, Skala 0–5 (modul.json werte.vertrauen); bekannt ab Start; nicht romanzierbar (`romanzierbar: false`), **kein Begehren-Wert** (Begehren nur für die 5 Crewfrauen).
- **Ermittlungs-Schwelle:** `ermittlung.schwelle.megan = 1` (befragbar ab Vertrauen 1, modul.json:6380).
- **Erreichbarkeit:** `immer_erreichbar`, Ort fürs Telefon „her office at the Eden Group“; ruft **nicht** an, während sie an Bord ist (Flag megan_besuch ohne megan_abgereist; kern/ereignisse.py:96).
- **Eden-Shop** (modul.json:407): per Videoanruf, Lieferung mit dem nächsten Versorgungsboot, Set Boardroom, Gruß kalt (V 0–2) / warm (V 3–5), **Rabatt 15 % ab Vertrauen 3**; führt u. a. Ersatzteilkiste (Reparaturuhr +1), Silikon-Armband, Füller-Rohling, Antennenkabel (je mit Megan-Kommentar), Single Malt, Parfum, Füller, Eden-Cap, **Megans Manschettenknöpfe** (Charm +1, 260 €, ab V3).
- **Job-Zeilen** (Auftrag/Erfolg/Fehlschlag/Patzer) im Schach-/Hai-Ton, modul.json:6239.
- **Running Gag** `megan_lacht` („Megan lacht (und hasst es)“, 3 Stufen, ereignisse.json gags).
- **Glücksbringer** `megan_screenshot` (Goldmasken-Screenshot, 1×/Tag Vorteil auf Charm; kostet −8 Vertrauen). Andenken `drohnen_propeller`.
- **megan_haltung** (story.json:661, Engine kern/ermittlung.py:586–604): Start 0, **nie gewürfelt**; berechnet aus Ducs Handeln:
  - +1 `megan_frueh_konfrontiert` (bis Tag 3 mit belegter Unstimmigkeit konfrontiert)
  - +1 `unterscheidung_bestanden` (besteht darauf, dass „vorläufige Meldung, kein Fahrverbot“ vollständig im Bericht steht)
  - +1 Vertrauen Megan ≥ 3
  - +1 `entwurf_markiert` (Lücke in ihrem Entwurf markiert)
  - −1 `entwurf_uebernommen`, −1 öffentliche Anschuldigung ohne Beleg (gegen wen auch immer), −1 `drohung_presse`
  - **≥ 1 = kooperiert:** dokumentiert ihre eigene Rolle, bietet Ersatzmodul oder Bergungsfenster. **< 1 = Druck:** bietet Duc persönliche Absicherung für eine beschönigte Fassung (Nein blockiert keine Rettung).
  - Wirkt aufs Ende: `hilfe = vorhaben_material or megan_haltung >= 1` → Eigenfahrt statt Schlepp (kern/abschluss.py:88–99).
  - Route `route_megan` nur bei haltung ≥ 0 (kern/ermittlung.py:624).
- **Besuch** (story.json:15038): Telefon/Video, **genau einmal per Hubschrauber**; angekündigt T4 abend, an Bord T5 Tag bis T6 Nacht, Abflug T7 Frühstück; Ankunfts-Event `g1_helikopter`; nur die Hauptstory setzt das Flag (Prüfer story_pruefen.py:444–500).
- **Missionen** (missionen.json):
  - `megan_esg` (:1385) „Ein ESG-Kurzbericht für Megan“, T2–7, Wahrnehmung SG 13, 200 € – Erfolg „Annoyingly good.“
  - `megan_lieferkette` (:1402) „Megans Wäschelieferant“ (klimaneutral? Zertifikate gehören zu anderer Fabrik), T3–7, List SG 14, 150 €, nach megan_esg – „Checkmate.“
  - `lola_megan_1/2` (:1169/:1186) „Eine Karte für Megan“ (Unterschriften Charm SG 13, dann Rahmen) → Item megan_crewkarte (Megan +2).
  - `lea_fueller_2` braucht den Füller-Rohling aus Megans Shop.
- **Kampf:** keine Kampfwerte. Indirekt: Eden-Racing-Lederjacke (+3, Erde, Selten) = **Geschenk Megan** (kampf.md:239).

### 1.3 Events mit Megan (ereignisse.json; Zeile = Fundstelle)

**Handy (per Video, nur wenn sie nicht an Bord ist)**
- `hy_investoren_laecheln` (:4528) T2–4 Tag – Crew-Foto für Investoren-Newsletter um 17 Uhr („Thirteen smiles“).
- `hy_megan_rundgang` (:6743) T2–5 Tag – Live-Rundgang per Handy („hold the phone straight, I get seasick through screens“, Ziege, Rosi).
- `hy_eden_hotline` (:7280) T2–6 Tag – automatische Wellness-Umfrage, von Megan widerwillig eingesprochen.
- `hy_megan_feuern` (:5224) T3–5 Tag – „Pick a name. You have ten seconds.“ (Mut-Probe; Totò vorschlagen kostet Totò).
- `hy_megan_paket` (:6854) T3–6 Tag – Moral-Paket mit Eden-Merch, Poster „Excellence Is A Habit“.
- `hy_megan_maske` (:7463) T3–6 Abend/Nacht – Versehens-Videoanruf mit Goldfolienmaske und Lockenwicklern (Screenshot-Option).
- `hy_megan_mitternacht` (:5116) T3–6 Nacht, ab Vertrauen 2 – 23:40, Schuhe aus, Whisky: „Tell me something nobody tells me.“ (Flirt-Option → Flag megan_flirt).
- `hy_megan_dinner` (:18560) T3–6 Dinner/Abend – lässt sich per Laptop an den Kopf des Crew-Tischs stellen.

**Bordrat**
- `br_gaestekabinen` (:783) T2–4 Nacht – Megan befiehlt Gästekabinen räumen + Minibars zählen; Option „Megan selbst anrufen“ (Charm 14) → megan_umgestimmt. Bordregel „Gästebereich bleibt Gästebereich“ macht „Megan-Druck-Events milder“ (−50 €/Abend).
- `br_megan_kommt` (:2907) T4 Nacht, nach Ankündigung – ganze Nacht polieren vs. Rosis Schild.
- `br_investoren_dinner` (:4243) T5 Nacht, an Bord – Dinner für zwei Investoren auf der toten Yacht („a stranded yacht is a story. I sell stories.“).

**Gag / Duell (während des Besuchs)**
- `g1_drohne` (:7808) T3–4 Frühstück/Tag, vor dem Besuch – Eden-Drohne jagt Totò; Lea mit Kescher.
- `g1_helikopter` (:11090) T5 Tag – Landung auf dem Sonnendeck, Lolas Handtuch fliegt, „Kein Haar bewegt sich“.
- `g1_megan_schach` (:11218) T5–6 Abend – gläsernes Schachbrett im Salon, Wette um einen Gefallen (List 14 → megan_gefallen).
- `gv_megan_sophia` (:12589) T5–6 Tag – Sophia verhandelt freien Nachmittag.
- `gv_megan_chiara` (:14659) T5–6 Tag – Weißer-Handschuh-Test an Chiaras Bar.
- `gv_keks` (:14790) T5–6 Tag – Lola hält ihr einen Keks hin („I don't eat joy. I eat results. …Is that chocolate?“).

**Hauptstory-Szenen (buehne.json, story.json wochenbogen)**
- `megan_erster_anruf` T2 Frühstück 09:10, Brücke (buehne.json:187) – Werftfenster Calvi organisiert, braucht klaren Ursachenbericht.
- `megan_entwurf` T4 Abend 21:30, Ducs Kabine (:619) – schickt Berichtsentwurf; Wahl markieren/übernehmen; kündigt Inspektion an.
- `megan_kommt` T5 Frühstück 08:30, Messe (:661) – Vorbereitung (Chiara + Lola), setzt megan_besuch.
- `megan_inspektion` T5 Tag 11:00, Maschinenraum (:681) – mit Rosi; hier verändert Konfrontation mit Belegen ihre Haltung.
- `wendung` T5 Nacht (story.json:14881) – „Ein Papier von vor der Abfahrt“ (siehe verdeckter Teil).
- `bericht` T6 Frühstück 08:00, Brücke (:744) – vier Fassungen, Megan wartet, „Get a report she can live with.“
- `megan_abflug` T7 Frühstück 07:30, Sonnendeck (:876) – „Leave with the last word.“

### 1.4 Story-Rolle in der (alten) 7-Tage-Woche

- **Welttext** (modul.json welt): „Megan McAllister, Fleet Director … wants the Eden Rise in Calvi within the week and a signed report on the cause before that.“
- **Tag 2:** erster Anruf: nützlich (Werftfenster Calvi) + Druck (Ursachenbericht für Zusatzkosten; Saisonprämie als Druckmittel, Abzug ausdrücklich strittig).
- **Tag 2–4:** Handy-Störfeuer (Fotos, Feuern, Rundgang, Paket, Drohne), Shop, Missionen.
- **Tag 4 abends:** Berichtsentwurf mit Lücke; Ankündigung des Besuchs.
- **Tag 5–6:** Hubschrauber, Inspektion, Gags, Investoren-Dinner; **Tag 6 Bericht** (4 Fassungen, story.json:15087):
  - *vollständig* (alles inkl. Megans Mitzeichnung und Ducs eigener Rolle) · *pro Crew* (Person bleibt weg) ·
    *pro Firma* (Bedienfehler ohne Meldung/R2-Lage/Modultyp) · *vorläufig* (Unbelegtes als offene Frage). Regel: „Vorsicht ist keine Lüge.“
  - **Endfassung Tag 7 durch Elsa** (bestätigen/korrigieren; Schäden verschwinden nicht).
- **Tag 7:** Abflug.
- **Ende/Abschluss** (story.json:15128, kern/abschluss.py): Dimensionen Schiff (eigenfahrt/schlepp/verlust; „Megans Hilfe“ = haltung ≥ 1), Aufklärung (vollständig/vorläufig_ehrlich/beschönigt/falsch; vollständig nur mit Kette **und** Wissen um z_01/z_02), Gemeinschaft, Zukunft. Jede Frau bekommt einen Abschluss; Megan hat keinen eigenen Romanze-Abschluss.

### 1.5 Neue Prämisse – Megans Platz (START.md)
- Thema 1 (:22): Bucht steht zum Verkauf, Eden Group verhandelt heimlich mit A.V. Estates; **Megan bringt den Vertrag** („Was du unterschreibst“).
- Akt 1 (:115ff): Megan verlangt sofort einen Bericht (Anime-Wut), droht alle bis Wochenende zu feuern; **Anhörung Tag 7 mit Megan als Richterin** (Geduldsleiste 3 Adern, Zeugen, Plädoyer Gnade/Schuld teilen/Strafe; Erbarmen = ihre menschliche Seite). Feuer-Drohung als Roguelike-Folge statt Game Over.
- Woche Akt 1 (:125): T2 Ultimatum, **T5 Hubschrauber + leises Telefonat „A.V.“**, T7 Anhörung; **täglich eine Handy-Sprachnachricht von Megan, jeden Tag wütender** (vorgeneriert, vertont).
- Entschieden (:152ff): Nautik/Schiffbau-Studium; Erbarmen aus Bauchgefühl („Ein PX-480 brennt nicht einfach so“, zögert beim Maschinenbericht); hat die Yacht zum Guerilla-Marketing (Siri, Yasin, Promis) in die Bucht geschickt; arbeitet unwissentlich für den Deal → **Wende in Akt 3**.
- Figuren-Runde (:167): Paar 2 = **Megan + Alon** (Raster: Wunsch + Angst, Prämissen-Bindung, Rolle je Akt, Grauton, Erkennungssatz).
- Parkplatz (:200): **Megan als heimliche Hardmode-Bonus-Romanze** in späterem Durchlauf.

---

## 2. Alon (A.V. Estates)

### 2.1 Steckbrief (alles, was existiert)

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | „Alon“; Firma **A.V. Estates**; Funkspruch nennt ihn „**Mr. V.**“ → Nachname mit V (nirgends ausgeschrieben) | orte_drehbuch.md:282 |
| Typ | „Der Tech-Milliardär unter den Gegnern heißt Alon (Parodie, keine echte Person)“; „erfundener Tech-Milliardär ohne Ähnlichkeit zu einer echten Person“ | kampf.md:262; kampf_neue_gegner_3.py:10 |
| Alter/Look (aktuell) | Fünfziger, kurzer Buzz Cut, selbstgefälliges Grinsen, Dad Bod, glatt rasiert, Pilotenbrille; **glänzend klavierschwarze Cyber-Armor** (Torso-Schale, skulptierte Brustplatten, segmentierte Schulterschützer, „wie ein Superheldenanzug“, Ducs Wahl Design v8), dunkle Jeans, weiße Sneaker, verchromtes **Jetpack** mit zwei Düsen, weiß-schwarze futuristische **Strahlenpistole** rechts | kampf_neue_gegner_3.py:49–56; kampf_nachbessern.py:73–78; PromptStudio Preset `Kampf_Alon`, Outfit `kampf_alon` |
| Look (veraltet) | Vierziger, kurze braune Haare, dunkle Sonnenbrille, schwarzes T-Shirt mit weißem Raketen-Print, silbernes Jetpack, Fäuste | karten_neu/kampf_edit.py:246 |
| Herkunft, Stimme, Persönlichkeit, Wünsche, Ängste | **nicht definiert** (keine Karte, kein Lorebook, keine Stimme) | – |
| Charakterzüge aus Docs | „rücksichtslose Extravaganz“ (Casanovas Grund, ihn zu hassen); „Mr. V. will keine Zeugen“; nimmt Tierleid für Tests in Kauf; weitere Opfer egal | tage_erkundung.md:44; DREHBUCH:282; ÜBERGABE:158 |

**Beziehungen**
- **Eden Group:** verhandelt heimlich den Kauf der Bucht Cala d'Orsu mit A.V. Estates (ÜBERGABE:22).
- **Megan:** unwissentlich Zuarbeiterin des Deals; sie trägt den Vertrag; T5-Telefonat „A.V.“.
- **Madame Casanova:** hasst ihn; Nebenquest „Casanova gegen Alon“ rund um Anwesen und ausgebrochenen Zoo, Lohn Ruf im Dorf, am Ende Elektro-Harpune nach der Festa (tage_erkundung.md:42–45). Bucht-Ende 2 „Zerrissen“: öffentlich machen mit Casanova + Dorf.
- **Adrien Morel (Fremdenlegion):** seine Einheit wurde **heimlich an Alons Firma ausgeliehen**, um ein Anwesen in den Bergen zu bewachen; sah Käfige, Tiere mit blinkenden Halsbändern, „Sie haben sie *getestet*“; hat Fotos (Speicherkarte), floh → Alons Agenten jagen ihn (orte.md:104–105, DREHBUCH Szene 5).
- **Sgt. Kaspar Wolff:** Legion wurde missbraucht; gewinnt Duc Weg C, meldet Adrien „gefallen“ („Wir haben einen Eid geschworen. Nicht auf eine Firma.“) → **Alons Anwesen ist gefunden**.
- **Petru/Laetitia:** indirekt (Laetitia versteckt Adrien).
- **Kloster San Martinu (Nonna Fiora, Isabelle, Frederico, Bruder Ambrosius):** Opfer der entlaufenen Zoo-Tiere; der Löwe trägt den Steuerchip.
- **Duc:** im Code keine Beziehung; Motiv ausdrücklich **nicht** „Duc als ESG-Prüfer“ (ÜBERGABE:160).
- **Siri/Yasin:** Bot-Kommentare (0 Follower, gleicher Erstelltag) unter Siris Bucht-Posts = Alon-Vorbote; offen: #StrandedInParadise dreht seine Negativpresse ins Positive.

### 2.2 Mechanik / Kampf

- **Gegner `Alon`:** Element **Luft**, Klasse **Flieger**, Bedrohung **tödlich**, Level **8**; Spezial w1 Ausweichen (dodge), w2 schwächen, s1 10 Schaden + **Strom** (kampf_balance_v3.py:68). Kampfstufe H („Alon mit Jetpack (A,H)“, kampf_neue_gegner_3.py:3). In v4 und kaempfe.json nicht eingetragen.
- Folgerungen aus den Regeln: Flieger → stark gegen ihn **Fern** und **Stange**, schwach Stumpf; Luft schlägt Wasser, Erde schlägt Luft. Fliehen: SG nach Stufe.
- **Beute:** **Cyber-Armor** (+5 Schutz, Luft, Episch) „nach dem Sieg über Alon (er trägt sie im Kampf)“ (kampf.md:241); in der Sim (+4, immun gegen Strom).
- **Sprites:** X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Alon (idle, guard, windup, attack, heavy_windup/attack, hurt, enraged, weakened, surrender, flee, victory, defeated; Ordner `_cyber` mit Rüstungsentwürfen). Neu-Posen mit Strahlenpistole stehen aus: Duc startet `Kampf_Nachholen.bat` → `test` (ÜBERGABE, „Kampf-Sprites nachholen“). Besonderheiten: surrender/defeated = Strahlenpistole am Boden, Jetpack aus; heavy = Pistole wie Keule über dem Kopf.
- **Seine Leute:** `Agent` (Mensch, gefährlich, Lv 5; w1 Rüstung, s1 Strom; Drops Elektro-Schlagstock, Stichschutzweste), `Brute` (Erde, Lv 5), **`AgentAlpha`** = silberhaariger skandinavischer Agentenchef in den Fünfzigern, weißer Anzug, Ohrhörer, Fäuste (kampf_alphas.py:60, 72) → passt als **Chef-Agent-Boss für Akt 2**.
- **Zoo-Tiere** (alle mit identischem Halsband: poliertes Chrom-Silber, glatt, **genau ein kleines rotes Licht**, „Behaviour Control Unit“): Löwe, Affe, neu Wolf, Schwarzer Panther, Grizzly, je Alpha-Variante; Ziege ohne/mit Halsband (Spur am Bach / Capra) (kampf_neue_gegner_5.py, kampf_alphas.py:18–22). Auf Korsika nicht heimisch.
- **Kein** Vertrauen, kein Event, keine Mission, keine Tage/Phasen im Code. Erkundungsort „Alons Anwesen (ausgebrochener Zoo)“ geplant, nicht gebaut (tage_erkundung.md:29; orte.md:128).

### 2.3 Spuren-Kette zu Alon (orte.md / DREHBUCH, Entwurf, „noch nicht gebaut“)
1. **Macchia Frame 2:** tote Ziege mit Metallring, blinkendes Licht (unerklärt).
2. **Tagebuchseite 2** (Bruder Ambrosius): „Er trägt etwas im Nacken, das blinkt. Er leidet, wie wir.“ – der Löwe als Opfer.
3. **Löwenbau (Boss Lv 7):** rotes Licht im Atemrhythmus, erlischt nach Sieg → **Steuerchip**, Gravur „A.V. Estates – Behaviour Control Unit“ (Missionsgegenstand) → erster Hinweis auf Alons verstecktes Anwesen.
4. **Berge Frame 4 (Felskamm):** Agenten in schwarzen Anzügen jagen Adrien; Funkgerät: „Morel hat die Fotos. Findet ihn vor der Legion. Mr. V. will keine Zeugen.“ Logo A.V. Estates. Duc-Gedanke nur mit Chip.
5. **Bergerie:** Adriens Fotos (Missionsgegenstand); Agenten-Trupp; Wolff-Entscheidung A/B/C; Chip erleichtert Weg C (Wolff zögert Runde 1).
6. **Ergebnis:** „Alons Anwesen ist gefunden.“ → Akt 2 Hauptquest.
7. Neu (ÜBERGABE:156): unscheinbare Alon-Hinweise schon in Akt 1 (rotes Licht im Maschinenraum, Steuerchip im Kloster), Beweis im Maschinenraum ab Akt 2.

### 2.4 Story-Rolle laut neuer Prämisse
- **Deal:** A.V. Estates kauft die Bucht von/mit der Eden Group (Greenwashing-Verdacht für ESG-Berater Duc).
- **Sabotage (Ducs Twist, ÜBERGABE:148):** Alon hat den Motor vorher manipuliert; der Auslöser aus dem gezogenen Fall hat es nur ausgelöst; er wollte, dass die Yacht sinkt („weniger Zeugen“). **Motiv:** Megans Marketing-Coup (Siri, Yasin, Promis) umdrehen → Katastrophe = negative Presse = Preis drücken; weitere Opfer egal. Überlast statt Rammung. Offen: **wer** die Manipulation eingebaut hat und **wann**.
- **Resort = Ablenkung:** in Wahrheit Forschungseinrichtung für Halsbänder; geplant: **Tests an Menschen** (Akt 3).
- **Akt 2:** Einbruch ins Anwesen (Adriens Fotos, Tiere mit Halsbändern), **Endgegner Chef-Agent**, Alon entkommt.
- **Akt 3:** Eden-Verwicklung aufdecken, Resort-Plan vereiteln, **Endgegner Alon** (Cyber-Armor-Drop). Margot-Fund (Lea, Akt 2) = juristische Waffe (Unterwasser-Kulturerbe/Schutzgebiet gegen das Resort, BRAIN_TRUST_LEA.md:29).
- **Bucht-Enden:** 0 Zu spät (Alon kauft) · 1 Unterschrieben (Festa unter Alons Logo) · 2 Zerrissen (Fotos + Steuerchip + Ruf, mit Casanova/Dorf, Duc gefeuert) · 3 Neu geschrieben (Genossenschaft) – müssen neu an Akt-3-Ausgang + Unterschrift gehängt werden.
- Team-Anmerkung: **Alon braucht ein Grau-Motiv** (bisher reiner Schurke).

---

## 3. Widersprüche, 7-Tage-Reste, Lücken

**Megan**
1. **Titel:** Fleet Manager (Karte, Lorebook W16, Prämisse) vs. **Fleet Director** (modul.json, buehne.json, story_buehne.py, Preset). Vereinheitlichen.
2. **Werdegang:** Karte = Stewardess → Chefstewardess → Büro; Prämisse = Studium Nautik + Schiffbau. Nicht unvereinbar (z. B. Studium nach den Saisons), muss aber in Karte/Lorebook ergänzt werden – sonst fehlt die Begründung für ihr Bauchgefühl.
3. **Aussehen:** Karte „long layered auburn“, grüne Augen; Preset-Base „copper-red bob mit Pony“, Sprite-Prompt „light blue eyes“; Sprite-Tags Long Layered. Sprites folgen den Tags, Text-Prompts widersprechen.
4. **Setting der Karte** = Riviera-Chartersaison Mitte August, Antibes, „acht Wochen Saison übrig“, sie ruft 2×/Woche an und kommt 1×/Monat; Spiel = Saison vorbei, gestrandet in Korsika. Karte/Lorebook passen nicht zum Spiel (ST-Seite).
5. **Seekrankheit-Geheimnis** vs. Besuch T5–T7 mit zwei Nächten an Bord einer ankernden Yacht. Spiel nutzt es nur als Witz (Lauchsuppe, „seasick through screens“). Entweder ausspielen (schöne verletzliche Szene) oder Besuch tagsüber halten.
6. **7-Tage-Reste:** „Calvi within the week“, Bericht Tag 6, Endfassung Tag 7 durch Elsa, Besuch T4–T7, Story-Prüfer erzwingt diese Fenster (story_pruefen.py:444). Neu: Ultimatum T2, Hubschrauber T5, **Anhörung T7 mit Megan als Richterin**, 21 Tage bis Festa (Ersatzteil aus Genua, Ultimatum auf drei Wochen gestreckt, tage_erkundung.md:10). Bericht-Mechanik (4 Fassungen) und Anhörung müssen zusammengeführt werden; tägliche wütende Sprachnachricht existiert noch nicht.
7. **Rollenwechsel:** Alt drängt Megan Richtung schnelle „Bedienfehler“-Erklärung/beschönigte Fassung (Druck-Zweig); neu zeigt sie Bauchgefühl und Erbarmen. Druck-Zweig muss als frühe Phase ihres Bogens umgedeutet werden.
8. **Romanze:** `romanzierbar: false`, kein Begehren, aber Karte mit Hitze 1–5 und expliziten Beispielszenen; Event setzt `megan_flirt`. Passt zum Parkplatz „Hardmode-Bonus-Romanze“, ist aber im Spiel nicht angeschlossen.
9. **Tote Flags:** `megan_flirt`, `megan_gefallen` (Schach-Wette: „ich schulde dir einen Gefallen“), `megan_umgestimmt` werden gesetzt, aber **nirgends ausgewertet** (grep kern/module/werkzeuge). Gute Haken für die Anhörung (Gefallen einlösen) oder Akt 3.
10. Karte nennt Lola „die Köchin, die Quittungen verliert“ – nur Kartenwissen; Shop-/Event-Ton ist konsistent.

**Alon**
1. **Kein Datensatz außer Kampf:** Karte, Lorebook, Stimme, Sprites außerhalb des Kampfs (Porträt/VN), Name/Nachname („Mr. V.“), Alter (40er alt vs. 50er neu), Herkunft, Wunsch/Angst, Grau-Motiv – alles offen.
2. **Kampfwerte nur in kampf_balance_v3** (Lv 8, tödlich), nicht in v4/kaempfe.json; für einen Akt-3-Endboss zu niedrig (Albtraum-Bosse ×1,2 LP; Alien/Maxwell Maximum Lv 9–10). Cyber-Armor-Werte uneins (+5 Doc vs. +4 Sim).
3. **Element-Logik:** Er ist Flieger/Luft und teilt Strom aus; Cyber-Armor macht dann den Spieler stromimmun – passt.
4. **Zeitlinie Anwesen:** Doc „Berge-Kapitel endet mit Anwesen gefunden“ (Akt-1-Nebenquest) vs. Akt 2 Hauptquest „Anwesen“ – Brücke ist gewollt (ÜBERGABE:117), aber Level-Kurve (Berge Lv 5–8) muss zu Akt 2 passen.
5. **„Mr. V. will keine Zeugen“** und „weniger Zeugen“-Motiv (Yacht versenken) sind konsistent – guter roter Faden.
6. **Story-Kriterium „Fairer Krimi“:** Die Sabotage muss mit Spuren belegbar sein (rotes Licht im Maschinenraum, Charge/Typenschild, Beweis ab Akt 2), sonst Deus ex machina.

**Gemeinsam:** Die bestehende „zweite Wahrheit“ ist auf Herstellerfehler + Megans Mitzeichnung gebaut, nicht auf Alon (Details unten). Prämisse will sie auf Alons Manipulation umschreiben (ÜBERGABE:148–151).

---

## VERDECKT – Fall-Rollen (nicht im Chat nennen)

**Megan in den sechs Fällen (story.json `faelle`)**
- **Fall 1, 2, 4:** keine Rolle.
- **Fall 3 „Der Gefallen“:** Die verantwortliche Person drückte die Abfahrt um 01:30 ohne Ladelauf durch und **überstimmte Holms Bedenken mit Megans Namen** („Megan wolle zufriedene Gäste“, f3_12). Megan ist hier Werkzeug, nicht Täterin. Duc kann per Handy **Megan um den Reiseplan bitten, wie er bei Eden einging** (f3_05_w3, story.json:6917) und **den Dateiverlauf vom Firmenserver holen lassen** (f3_06_w2, :6966) – sie ist also Beweisquelle.
- **Fall 5 „Das Bild, das bleiben sollte“:** Gegenhandlung f5_gh1 (T2 Nacht, bei Angst ≥ 1): gekürzter Clip lässt Duc verantwortungslos aussehen → **Ruf −1, Megan ruft an** (:10076).
- **Fall 6 „Niemand an diesem Tisch“ (kein Einzeltäter, vorgeschädigtes LM3):** Megan **fördert die schnelle menschliche Erklärung**: Gegenhandlung f6_gh2 (T4 Abend) – ihr Entwurf nennt „Bedienfehler eines Besatzungsmitglieds (Maschinenraum, 01:40)“ ohne die Temperaturwarnung vom Nachmittag (f6_13, :12361/:14330; story_faelle.py:969–985). Auslöser: `nicht pruefung_an_megan` – **dieses Flag wird nirgends gesetzt**, die Gegenhandlung feuert in Fall 6 also immer. Gegenmittel laut Notiz: unabhängige Prüfung (f6_07), Holms Warnung, Protokoll 17:20.

**Zweite Wahrheit (alle Fälle gleich, story.json:305–404)**
- Kern: Die Eden Group erhielt vor der Reise eine Sicherheitsmeldung zum Modultyp; **Megan zeichnete eine vorläufige Weiterbetriebsentscheidung administrativ mit, ohne die Prüfung sicherzustellen**; sie plante keinen Unfall, sucht danach zuerst eine einfache Erklärung über Bedienfehler. Bedeutung: beweist nicht die Unfallursache, sondern unsauberen Umgang mit bekannter Unsicherheit; „Entscheidung, kein Freispruch“.
- **z_01** (T-12 09:00, Dokument, Eden HQ): Herstellermeldung PX-480, **Charge 22-B**, thermische Vorschädigung möglich, Rückfallprofil R2 nicht verwenden, Prüfung vor Weiterbetrieb. Wissende: Megan. Wege: Rosis Herstelleranfrage, Elsas Dokumentation, Megan legt es selbst vor (frueh_konfrontiert + haltung ≥ 0), späte Nachprüfung.
- **z_02** (T-9 16:00): Weiterbetriebsentscheidung „bis Werftaufenthalt Calvi, Prüfung und R2-Sperre dort“, **mitgezeichnet: M. (Megan)**; Schiff nicht informiert. Wege: Elsa, Megan legt vor, Megan dokumentiert freiwillig (haltung ≥ 1).
- **z_03** (T5 22:00, Aussage): Megan: „Es war eine vorläufige Meldung. Kein Fahrverbot.“
- **z_04** (T2 09:10): Calvi binnen Woche + unterschriebener Ursachenbericht, Saisonprämie als Druckmittel (strittig).
- **z_05** (T4 20:00): ihr Entwurf lässt eine bereits belegte technische Einschränkung weg (Vorrang: R2 nicht freigegeben > LM3-Warnung > Lastgrenze).
- **z_06** (abgeleitet): Charge der Meldung = Charge auf dem **Typenschild von LM3** (braucht z_01 + r_14).
- Routen (eröffnen T2–3): route_rosi (Maschinenraum, braucht r_14), route_elsa (Hafen), route_megan (Handy, ≥ 1 gesicherter Fakt; nur bei haltung ≥ 0), alle liefern T5 Nacht; route_spaet (T6, kostet 1 Phase, liefert T7 Frühstück). Ohne Route: zuerst Megans problematischer Bericht an T5.
- Bericht-Fassung *pro Firma* lässt genau diese zweite Wahrheit plus r_13/r_14 weg; *vollständig* enthält Megans Mitzeichnung.
- Prüffälle: „Megan kooperiert“, „Megan übt Druck aus“ (story_eden_rise.py:520).

**Alon in den Fällen:** **keine Rolle** in fall_1..fall_6 oder den z_-Fakten. Laut Prämisse sollen die z_-Fakten (bisher Herstellerfehler/Charge 22-B, „thermisch vorgeschädigt, an Bord unbekannt“) auf **Alons Manipulation** umgeschrieben werden: Akt 1 urteilt über den Auslöser (gezogener Fall), Akt 3 über Alon. Offen: wer die Manipulation eingebaut hat und wann; ob Megans Mitzeichnung (z_02) als ihr Grauton erhalten bleibt (sie hat die Prüfung bis Calvi verschoben und damit Alon unwissentlich das Fenster gelassen) – nicht entschieden.

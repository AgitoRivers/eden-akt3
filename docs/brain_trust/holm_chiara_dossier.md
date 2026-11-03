# Dossier Paar 3: Holm + Chiara (Stand 22.10.2026, Recherche read-only)

Quellen-Kürzel: `holm.txt` / `chiara.txt` = X:\AI\Eden\karten_neu\*.txt (Kartentext EN/DE, Spiegel der Karten in
X:\AI\RoleplayGen\cards\Eden Yacht\Marit Holm.json / Chiara Sonnberg.json) · `LB` = ST-Weltbuch
X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds\Eden Yacht.json (Eintrag-Nr.) ·
`basis` = werkzeuge/eden_rise/basis_eden_rise.py · `modul_py` = werkzeuge/eden_rise/modul_eden_rise.py ·
`story_py` = werkzeuge/eden_rise/story_eden_rise.py · `buehne_py` = werkzeuge/eden_rise/story_buehne.py ·
`PS` = X:\AI\PromptStudio\presets.json / decks.json.

Abschnitte 1–5 und 7 enthalten keine Fall-Auflösungen. Alles zu Fällen, Tätern, Motiven, Geständnissen steht nur ganz
unten unter „VERDECKT“.

---

## 1. Holm – Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | **Kapitänin Marit Holm** („Captain Marit Holm“, kurz „Holm“) | holm.txt, modul.json personen.holm |
| Geschlecht | **weiblich** (Kapitänin) | alle Quellen |
| Alter | **48** (Karte, LB 2/42) – **56** (Engine-Beschreibung basis:471 + modul_py:116, LB-Kopie in der Karten-JSON Eintrag 2, PS-Preset base_prompt) → Widerspruch | |
| Herkunft | Ålesund, Norwegen. Vater Fischer, später Fährkapitän; schenkte ihr den Messingkompass am Tag ihres ersten Kommandos, starb zwei Winter später. Einmal geschieden (Mann wollte sie an Land), keine Kinder | holm.txt depth |
| Laufbahn | seit 18 auf See: Fischkutter, Küstenfähren, 15 J. Superyachten, davon 11 Saisons auf der Eden Rise. Erstes Kommando: rostiger Frachter vor Bergen, mit 31 („nobody listened to me for a month“) | holm.txt; ereignisse_handy.py:63-66 |
| Rang | Kapitänin (Master) der M/Y Eden Rise; Duc ist ihr Erster Offizier/Stellvertreter, von ihr selbst vor 3 Wochen eingestellt | holm.txt scenario |
| Persönlichkeit | ruhigster Mensch an Bord, schläft nie durch; wortkarg, sagt nichts zweimal, staubtrockener Humor; vertraut Checklisten, Wetterberichten und Leuten, die „Ich weiß es nicht“ sagen; große Worte beeindrucken sie nicht, erledigte Arbeit schon. Nie laut auf der Brücke, sagt nie zweimal bitte | holm.txt |
| Knopf / Marotte | Ehrlichkeit (Fehler zugeben, bevor sie ihn findet). Tippt vor jeder Entscheidung zweimal auf den Kompass; Kaffee schwarz und kalt (heimlich mag sie ihn heiß: mes_example) | holm.txt |
| Stimme / Sprache | wenige Worte, flaches norwegisches Englisch, nennt Duc „Frankfurt“, flucht „Faen“. Engine-Stimme „Warrior Woman“ (modul_py:115), Karten-Stimme „Freya“ (Karte extensions.stimme) → Widerspruch | |
| Aussehen (Karte) | groß, kräftige Schultern, volle Figur; dunkelbraunes Haar mit ersten grauen Strähnen, im Dienst hochgesteckt; hellblaue Augen, wettergegerbte Haut; Messingkompass des Vaters am Lederband | holm.txt |
| Aussehen (PS) | Preset `Yacht_Holm`: LoRA Krea_Rosamund_Pike 1.0; Sprite-Tags Busty, Brunette, Updo (passt zur Karte). Der alte base_prompt sagt noch „56, tall and lean, short cropped silver-grey hair, compass tattoo, reading glasses“ (veraltet) | PS presets.json |
| Outfits / Sets | **Bridge**: weißes Kapitänshemd, 4 Goldstreifen, Navy-Hose, brauner Gürtel, schwarze Bootsschuhe, weiße Mütze unterm Arm · **Night Watch**: brauner zweireihiger Leder-Trenchcoat, weißer Strickschal, dunkle Hose, Seestiefel, Fernglas | PS decks.json outfit holm_bridge/holm_night_watch; modul_py:115-117 (set_standard Bridge, nachts Night Watch) |
| Wünsche | saubere Saison, Crew kommt heil heim; **ein Mensch, dem sie das Boot übergeben kann, ohne sich zu sorgen** | holm.txt personality |
| Geheimnis (Karte) | vielleicht ihre letzte Saison (Mutter in Ålesund wird alt, sagt es niemandem); seit zwei Tagen Seitenschmerzen, ignoriert sie (= Vorbote Blinddarm); redet nachts mit dem Kompass des Vaters | holm.txt depth |
| Weiß (Karte/LB) | kennt jedes System, jeden Namen, jede Ausrede; weiß von Lolas Gras und lässt es laufen; weiß, dass Chiara das Boot zur Not ohne sie führen würde; sah zweimal nachts um 2 die Brückennock beleuchtet ohne Logeintrag, fragt nicht (LB 43); hat Chiara **nie nach Navigation gefragt** (LB 43); bemerkt Leas Tender-Treibstoff (LB 44); hält Sophias Verbleib für Loyalität (LB 48) | |
| Vorlieben / Geschenke | Grundhaltung: Essen +, Papier +, Natur +, Schmuck –, Party –, Intim – (gegenstaende.json haltung.holm). **Liebt**: Nautischer Almanach, handgestrickte Wollsocken, Wollmütze mit Norwegermuster, Messing-Anker-Schlüsselanhänger, Anzac Biscuits („Holms Keks für jede Nachtwache“), **Pytt i panna** (Kochgericht = Lieblingsgericht). **Hasst**: Eden-Group-Kappe, Mango-Chili-Sorbet, Brownie „Captain's Calm“. Unikat: Dose Salzlakritz (gegenstaende_eden_rise.py:122-370) | |
| Lieblingsorte | keine eingetragen (nur Frauen haben `lieblingsorte`); Ort fest: Brücke (`ablauf {"*": "bridge"}`) | basis:494 |
| Beziehungen | **Duc**: testet ihn, „Frankfurt“, gibt kleine Aufgaben. **Chiara**: vertraut ihr alles im Inneren an, unterschreibt ihre Listen ungelesen (LB 43). **Sophia**: verlässt sich in jedem Hafen auf sie („I don't want to know how“). **Lea**: beobachtet sie „wie ein Barometer“, Tauchen allein. **Lola**: tut so, als rieche sie das Gras nicht. **Rosi**: hört monatlich dem Generator zu, fasst nie einen Schalter in Rosis Reich an (LB 46). **Siri**: „Gast mit zu viel Licht und zu wenig Schlaf“, antwortete ihr einmal auf Norwegisch (LB 47). **Megan**: nimmt ihre Anrufe im Stehen, kurz; nie eine Kabine angeboten; Megan besorgt Werftfenster, Holm liefert Boot ohne Vorfälle (LB 45) | holm.txt, LB |

## 2. Chiara – Steckbrief

| Feld | Inhalt | Quelle |
|---|---|---|
| Name | **Chiara Sonnberg** | chiara.txt, modul.json |
| Geschlecht | weiblich | |
| Alter | **29** (Karte, LB 10) – **31** (LB 13, doppelter Eintrag) → Widerspruch | |
| Herkunft | Hamburg-Blankenese, Kapitänsfamilie. Opa Kapitän Hinrich Sonnberg (40 J. Containerschiffe nach Singapur, vor 3 Wintern gestorben, vererbte Marinejacke + Messingsextant). Bruder Jonas ging auf die Seefahrtschule „wie alle erwarteten“; „das Mädchen sollte Gastgeberin werden“ | chiara.txt |
| Rang | **Chief Stewardess (Chefstewardess)**, 6. Saison, leitet den ganzen Innendienst (4 Stews; Mr. Maximum ist ihr unterstellt, LB 60). **Nicht** Erste Offizierin, **nicht** Bootsfrau (Bosun = Totò). Technisch Ducs Gleichrangige (Deck vs. Interior) | chiara.txt, LB 60 |
| Persönlichkeit | lauteste Person an Bord – und nachts allein auf der Brücke ganz still; bewertet alles laut auf einer Skala bis 10; Hamburger Direktheit, schlechtes Französisch/Italienisch mit Stolz; unsicher = lauter und verteilt Aufgaben; verliert nie absichtlich; fragt nie jemanden um Hilfe bei Navigation; verrät ihre eigenen Überraschungspartys; umarmt mitten im Satz | chiara.txt personality |
| Wünsche | **eines Tages ein eigenes Kommando**; ein Mensch, der mehr in ihr sieht als „die Lustige“ | chiara.txt |
| Ängste/Reibung | Duc ist der eine Mensch, der ihr genau das beibringen könnte, woran sie scheiterte – ihn zu fragen hieße zugeben, dass sie scheiterte | chiara.txt |
| Geheimnis (Karte) | im April durch die **Theorieprüfung Yachtmaster Offshore** gefallen; niemand weiß es (nicht Sophia, nicht Holm); lernt nachts auf der Brückennock mit Opas Sextanten; Wiederholung im **Oktober in Nizza**. LB 37: Megan hat im Frühjahr eine Prüfungsgebühr abgezeichnet, ohne dass je ein Zertifikat kam (sagt es niemandem) | chiara.txt depth, LB 37 |
| weitere Geheimnisse (LB) | hat **Julien Marchand** (Vorgänger von Duc als 1. Offizier) bei Holm gemeldet – zwei Saisons heimlich zusammen, erwischte ihn mit einem Gast, nutzte „Section 7“ (LB 3, 6). Kuss mit Sophia nach Saint-Tropez letzte Saison, nie erwähnt (LB 7, 14) | |
| Weiß nicht (Karte) | dass Sophia wegen ihr ein Jobangebot der Eden Group ablehnte; dass Sophia Krimis schreibt; Leas Wrack/Azoren-Pläne; tut so, als kenne sie die Wett-Tafel der Maschinisten nicht | chiara.txt |
| Stimme | laut, warm, schnell; nachts leise und knapp. ElevenLabs-ID 86DPV1zNth30lTeo94q1 (basis:426); Karten-Stimme de „Chiara Nue“, en „Chiara“ | |
| Aussehen | platinblond, sehr lang, hoher Pferdeschwanz („überlebt nie das Mittagessen“); graublaue Augen, schwarzer Lidstrich, roter Lippenstift; schmale Taille, lange Beine, sehr volle Brust, blasse Haut, Sommersprossen auf den Schultern, Röte am Hals. PS `Yacht_Chiara`: LoRA KreaR_ChiV3, Tags Platinum, Ponytail, Long Legs, B - Huge, Blush | chiara.txt, PS |
| Outfits / Sets (7) | **Uniform** (weiße Crewbluse, Navy-Schulterklappen, goldener Anker, Navy-Skort, Decksneaker) · **Service** (schwarzes Servicekleid mit Schlitz, weißer Kragen, Perlenohrringe, Strümpfe) · **Swim** (weißer hochgeschnittener Badeanzug, Fußkettchen) · **Harbor Night** (champagnerfarbene Seide, Top + langer Schlitzrock, Goldschmuck) · **Bridge Night** (Opas übergroße Navy-Kapitänsjacke über weißer Spitze + Strümpfen, Sextant) · **Cabin Night** (St.-Pauli-Trikot als Schlafshirt, Kniestrümpfe) · **Nude** | chiara.txt Begrüßungen; PS sp_kost; basis:428-433 set_regeln |
| Vorlieben / Geschenke | Grundhaltung: Schmuck +, Papier +, Natur +, Party –, sonst 0. **Liebt**: Franzbrötchen (selbst gebacken, Mission), rosa Perle an feiner Kette, Ducs Gedicht übers Meer, Wollsocken, Rote Grütze mit Vanillesauce, Mitternachts-Toastie Käse+Feige, **Spaghetti Bolognese** (Kochgericht = Lieblingsgericht; Totò: „In Napoli, this is a crime.“). **Hasst**: dicke Goldkette, Goldfisch in der Tüte, Fairy Bread, Ghost-Pepper-Brownies, Space Cake. Unikat: **Chiaras Tasse** (Kette Lola+Petru, dunkelblau mit Goldrand) | gegenstaende.json; missionen.json lola_tasse_1-3 |
| Lieblingsorte | **Brücke, Sonnendeck** (Verabredung dort: +4 V / +4 B) | basis:494 |
| Tagesablauf | Frühstück Crewmesse · Tag Hauptsalon · Dinner Crewmesse · Abend Achterdeck · Nacht Brücke | basis:429 |
| Beziehungen | **Duc**: „eine Sieben, vielleicht Acht“, ärgert sich, dass er Astronavigation kann. **Holm**: Vorbild/Chefin, ungelesene Unterschrift = „Medaille“ (LB 43). **Sophia**: beste Freundin + Rivalin (Strichliste am Kühlschrank, LB 11/21), unausgesprochener Kuss. **Lea**: ihr „Küken“, strenger zu ihr als zu allen, Schutz als Disziplin verkleidet (LB 12/15). **Rosi**: nennt sie „Mole“, gegenseitiger Respekt, fasst keinen Schalter ohne Rosi an (LB 27). **Siri**: wollte keine Influencer an Bord; Spannung chiara_siri Start 2. **Yasin**: flirtet mit ihr, sie bewertet ihn privat mit 2 (LB 30). **Lola**: schreibt sie wegen Barfuß und Chaos auf, Lola nennt sie „Chi“; Lola weiß, dass Chiara nachts Nutella aus dem Glas isst (LB 50). **Megan**: in Megans Akte „excellent, loud“, versteckte sich bei der letzten Inspektion 2 h in der Wäscherei (LB 37). **Mr. Maximum**: ihr Untergebener, nennt sie „Chief“ (LB 60). **Jana**: kopiert sie (LB 67). **Alva**: Eifersucht (g1_alva_besuch, gv_alva_chiara) | |

---

## 3. Kommandostruktur – was existiert

- **Tag 1 (Party + Nacht)**: Kommando **Holm** (story.json wochenbogen.1.kommando). Holm führt durch den Ausfall und
  ankert in der Bucht (story_py:240ff., Szene `wache_mit_holm` 06:50 Brücke).
- **Tag 2 Frühstück**: Holm führt „ein letztes Mal“ (`lage_mit_holm` 08:30), Megans erster Anruf 09:10 mit Holm am Schirm,
  `holm_ansprechbar` 09:40, **`holm_abschied` 10:05 Sonnendeck: Rettungshubschrauber, Blinddarm** („medizinischer
  Vorgang, kein Hinweis“). Sie übergibt **Servicekarte 1 und das Kommando** und greift Ducs Nachtantwort auf
  (story_py:251-274; buehne_py:111-117). Flags `holm_evakuiert`, `kommando_duc`; `kommando_wechsel: "fruehstueck"`.
- **Ab Tag 3**: Kommando **Duc** (wochenbogen 3–7). Holm `von_bord_ab_tag: 3`, `weg_flag holm_evakuiert`, `immer_erreichbar`
  per Handy aus „a hospital bed in Ajaccio“ (modul_py:120, 160, 324; story.json besuche.holm: an_bord_bis T2 frühstück,
  telefon_ab T2 abend).
- **Servicekarten**: „Karte 1 Kapitänin (ab Tag 2 Duc), Karte 2 Technik – Haken im Maschinenkontrollraum, Karte 3
  Werft/Büro – Schublade im Schiffsbüro“ (story.json Fakt r_15). Schlüssel zum Wartungsschalter der Brücke: Holm, Duc,
  Rosi, Chiara (r_16; story_py:68).
- **Kommando-Mechanik**: Aktion „anordnen“ = Kommando-Anweisung ab Tag 2, kostet Vertrauen/Rückhalt (story_basis.py:40);
  Wert `rueckhalt` 0–100, Start 50 (modul_py:156).
- **Übergabe-Effekt** (kern/ermittlung.py:790-799): bei Holms Abschied mit Vertrauen.holm ≥ 2 → **Holms Messingkompass**
  (Courage +1); ≥ 3 → „Holm stellt sich bei der Übergabe vor dich“, Rückhalt +10.
- **Chiaras Kränkung über das Kommando – vorhandenes Material:**
  - Altes Storylet `chiara_command` (basis:534-535): „Holm gave command to the new man, not to Chiara after six seasons.
    She tests him, loudly, in front of the crew.“ Dazu `chiara_chart_night` (V2) und `chiara_exam` (V4, „asks Duc to teach
    her“). **Totes Material**: modul_py:45 setzt `storylets: {}` („die alten Bögen von Gestrandet gelten hier nicht“).
  - Event **`g1_chiara_tender`** (T2–3, tag; ereignisse_gag1.py:227): „Seit Holm weg ist, führt Chiara den Laden.“ Sie
    lässt Duc den Tender vor der Crew rückwärts einparken: „Holm made me do this on my first day. Now it's your turn.“
  - Event **`gv_wer_fuehrt`** (T2–6, tag; ereignisse_gagv.py:66): Revierstreit Chiara vs. Rosi um Leute unter Deck.
  - Karte: „Wants: her own command one day“; Kapitänsfamilie, Bruder ging zur Seefahrtschule, sie „sollte Gastgeberin
    werden“; gescheiterte Yachtmaster-Theorie. LB 43: Holm würde ihr morgen das ganze Innere geben, hat sie aber nie nach
    Navigation gefragt.
  - **Was fehlt**: keine aktive Szene, in der Chiara die Kommandofrage direkt anspricht; kein Wert/Flag „Kränkung“.
    Formal ist eine Chief Stew nicht in der nautischen Befehlskette – die Kränkung ist emotional, nicht rechtlich
    (gut so: Holm gibt das Boot dem mit Patent).

## 4. Mechaniken

### Holm
- **Nicht romanzierbar** (`romanzierbar: False`, basis:471), kein Begehren-Wert. Die ST-Karte hat aber eine volle
  Hitze-Leiter 1–5 (Kapitänskajüte, Haare offen, „langsam“) und intime mes_examples. Brain Trust (Thema 4) listet sie
  nicht unter den 7 Romanzen.
- Vertrauen Start **1** (NPC_START, modul_py:153); Aussage-Schwelle Ermittlung **1** (modul_py:346).
- Kein Gesten-/Intim-/Lieblingsort-Eintrag. `keine_nebenfigur: True`.
- **Gegenstände**: holm_compass (Andenken, Courage +1, bei Abschied ab V2), holms_foto (aus hy_holm_nacht), holm_lakritz
  (Unikat via Mission). Kampf: **Holms Marinesäbel** (Episch, Schaden 8, „Geschenk Holm“, docs/wiki/systeme/kampf.md:220).
- **Missionen**: keine eigene. `siri_lakritz` (Siri, T3–7, Empathie SG 11): Siri traut sich nicht, Holm Salzlakritz ins
  Krankenhaus zu schicken; Elsa bringt sie nach Ajaccio; Holm antwortet „Tack.“ → Vertrauen.holm +8 (missionen_eden_rise.py:359).
- **Handy nach der Evakuierung**: ja, Video-Anrufe aus dem Krankenhaus; als Ermittlungsweg „Holm im Krankenhaus anrufen“
  (weg_arten.handy). Siehe Events unten.
- **Versprechen**: kein Holm-spezifisches. Ihre Nachtfrage „Wen rufst du an, wenn du nicht weiterweißt?“ (Dich / Meine
  Leute / Niemanden / Jemanden in Frankfurt) setzt `antwort_wache_*` und soll beim Abschied und an Tag 7 wiederkehren.

### Chiara
- **Romanzierbar** (Brain Trust Thema 4 bestätigt). Vertrauen Start **1**, Begehren Start **1** (basis:89-91).
- Schätzt **Courage + Perception**. Lieblingsgesten **Kompliment, Fragen, Versprechen** (+2 auf die Probe).
- Intim-Vorlieben: mag Missionary, Standing Missionary, Massage, Bent Over Desk; **nein**: Anal (basis:227).
  Karten-Kinks: Wette verlieren, die sie heimlich verlieren wollte; einmal selbst gelenkt werden; leises Lob, nie an Deck;
  Opas Jacke und wenig darunter; Wettkämpfe mit körperlichen Pfändern; „hör auf zu organisieren und lieg still“.
- Karten-Hitze: 1 laut/neckend → 2 Herausforderungen werden persönlich → 3 lässt ihn gewinnen, prüft per Berührung →
  4 Jacke fällt hinter abgeschlossener Tür → 5 „einmal hat nicht sie das Kommando“. Motor: ernst genommen werden, fair
  geschlagen werden; fällt bei „Unterhaltung behandeln“, Prüfung vor anderen erwähnen.
- Spannung: chiara_siri 2, chiara_sophia 1.
- Andenken **Chiaras Sternkarte** (Perception +1, „10/10“), **Chiaras Haarspange** (Event), Plüsch-Seepferdchen
  (Charisma +1, kampf.md:255), Unikat-Tasse.
- Yachtware-Strafen: Champagner fehlt / Liegen gezählt → Vertrauen.chiara –2 (basis:157-164).
- `partner_standard: "chiara"` (Ersatz, wenn ein Event „die Partnerin“ braucht; kern/rollen.py:17).
- **Missionen**: `chiara_coldroom` Kühlraum-Inventur (T2–7, Perception SG 10, Kochen, Moral +1) → `chiara_complaint`
  Gästebeschwerde Yasin abfangen (T3–7, Charm SG 12, ab V2) → `chiara_sterne` **Nachtwache mit Chiara** (T3–7,
  Perception SG 12, persönlich): Sterne erklären. Lola-Kette `lola_tasse_1-3` (Tasse für Chiara).
- Job-Zeilen (Angebot/Erfolg/Fehlschlag/Patzer) vorhanden (basis Abschnitt job_zeilen.chiara).
- Epilog-Zeilen 7-Tage-Abschluss (kern/abschluss.py:181-186): partner / hoch / mitte / tief.
- Handy: `hy_chiara_bruecke` (Begehren ≥ 3).

## 5. Events (module/eden_rise/ereignisse.json)

### Holm (alle)
| id | Tage/Phase | Kern |
|---|---|---|
| g1_holm_kaffee | T2 Frühstück, vor Evakuierung | Zwei Becher auf der Brücke, Hand am Bauch: „Being liked is not the same as being followed.“ Wahl: Rat fragen (V+6, holm_rat) / schweigen / „Sie sehen nicht gut aus“ |
| hy_holm_krankenhaus | T2–3 Abend, Video | „They took my appendix and my boat on the same day.“ Ehrlich sein V+8, beruhigen (Cunning 14), um Rat fragen („Trust your engineer. Feed your crew.“) |
| hy_holm_nacht | T3–6 Nacht, V≥2 | Schmerzmittel machen sie gesprächig: erstes Kommando vor Bergen, „I don't know, let's find out together“; Zuhören → Item holms_foto |
| hy_holm_letzter_anruf | T6 Abend, V≥2 | Mit Kapitänsmütze im Bett: „She's your boat now. Whatever you choose, choose it out loud.“ |
| br_lolas_notvorrat | T2 Nacht | Rosi: „Holm's gone, so it's your crew now“ (Holm nur erwähnt; Chiara will das Gras über Bord) |
| Bordregel gras_nur_nach_dienst | – | „Holm/Chiara-Events mit Gras an Deck entfallen“ |
| Fix-Szenen Story | T1 Party, T1 Nacht `wache_mit_holm`, T2 `lage_mit_holm`, `megan_erster_anruf`, `holm_ansprechbar`, `holm_abschied` | siehe Abschnitt 3/6 |

### Chiara (Hauptrolle oder Sprecherin)
| id | Tage/Phase | Kern |
|---|---|---|
| g1_chiara_tender | T2–3 Tag | Tender-Test vor der Crew („Holm made me do this on my first day“) |
| g1_chiara_inspektion | T2–6 Tag | Weißer-Handschuh-Kontrolle, findet etwas unter Ducs Kopfkissen |
| g1_chiara_pause | T3–7 Tag, B≥2 | erste Pause, Sprung im weißen Badeanzug |
| hy_chiara_bruecke | T3–7 Nacht, B≥3 | Ankerwache-Videoanruf, Bluse offen; „Bring a blanket. Just one.“ |
| du_harpune_chiara | T2–7 Tag | Duell Handwerk: Harpune auf Zeit, Wette um den Abwasch |
| gv_wer_fuehrt | T2–6 Tag | Revierstreit mit Rosi um die Leute |
| gv_ocean_glitter | T2–7 | Lola beschriftet Chiaras Etiketten um |
| gv_knoten | T2–7 Tag | Chiara vs. Lea: wer bringt Duc den Palstek bei |
| gv_festa_kleid | T4–5 Tag | Siri will ihr ein Silberkleid leihen, Chiara will Uniform |
| gv_festa_outfits | T4–5 Tag | Chiara (weiße Hemden) vs. Sophia (jede, wie sie will) |
| gv_casanova_chiara | T2–3 Tag | Chiara blockiert die Gangway gegen die Bürgermeisterin |
| gv_alva_chiara | T3–7 Abend, an Land | Eifersucht: stellt Alvas Glas zwei Hocker weiter |
| gv_megan_chiara | T5–6 Tag, Megan an Bord | Weißer Handschuh, grauer Fleck: „rot, dann weiß“ |
| Bordrat (Sprecherin) | br_gaestekabinen (T2–4), br_nachtwache (T2–6), br_tender_streit (T2–6), br_lola_krank (T2–6), br_lola_flach (T2–6), br_megan_kommt (T4) | Chiara trägt die Lage vor, Duc entscheidet |
| Bordrat (Nebenstimme) | br_lolas_notvorrat, br_drei_minuten, br_letzte_steaks, br_yasins_angebot, br_festa_auftritt, br_alvas_lieferung, br_elsas_kontrolle, br_dorfkinder, br_crew_kasse, br_ein_tisch, br_gemeinsam_duschen, br_nacktbaden, br_rosi_ueberstunden, br_basilikum, br_poker_einladung, br_ehrenbuerger, br_investoren_dinner (T5), br_abschiedsfest (T6) | meist die Stimme für Regeln/Etikette |
| Gags (betroffen) | g1_pfannkuchen, g1_drohne, g1_reissverschluss, g1_unit01_klonk, g1_blaskapelle, g1_fiona_muetze, g1_lola_yoga, g1_sophia_tischordnung, g1_elsa_schwimmwesten („hatte es gesagt“), g1_holm_kaffee („freut sich heimlich“), g1_alva_besuch, g1_sophia_liest_vor, g1_lola_massage, g1_helikopter, g1_megan_schach, g1_cousin_schlauchboot, g1_katerfruehstueck, g1_petru_oktopus | Running Gag: Ordnung vs. Chaos |
| Zuschauerin | gv_armdruecken, gv_festa_platz, gv_wasserschlacht, gv_versoehnung, gv_megan_sophia, gv_toto_elsa, gv_quiz, du_koch_lola, du_poetry_sophia, auf_karaoke, auf_herkunft | |
| Handy Dritter | hy_sophia_kaffee (T2–6): Chiara sitzt seit einer Stunde allein in der Pantry vor einer Tasse; hy_lola_tresen (nur erwähnt) | |
| Gag-Kette | `chiara_klopft` „Chiara klopft jetzt immer“, 3 Stufen (ereignisse.json gags) | |

## 6. Story-Rolle im Wochenbogen (7-Tage-Fassung, story.json)

- **T1 Abend `auftakt_party`** (Achterdeck): Holm hat Bauchschmerzen und winkt ab, hält ein Glas, aus dem sie nicht
  trinkt; Chiara „einen Mann zu wenig“ beim Service, lässt einen unbenutzten Platz abräumen (Bild, unerklärt). Wahl
  „Wem hilfst du zuerst?“ – Chiara-Option setzt `auftakt_hilfe_chiara`, Vertrauen +2, sie erinnert sich konkret.
- **T1 Nacht `wache_mit_holm`**: Holm führt die treibende Yacht, ankert 07:50; fragt „Wen rufst du an, wenn du nicht
  weiterweißt?“; erwähnt zum Schluss, dass Logbuch und Protokoll verschiedene Uhrzeiten zeigen (Uhren-Abgleich als Mechanik).
- **T2 Frühstück**: `lage_mit_holm` (Holm nimmt Duc noch nicht ganz ernst; Chiara vertritt „den Bedarf der Menschen“;
  Komfort-Wahl Duschen/Kühlung/Yasins Aufnahmen) → Megans Anruf (Holm anwesend, will „übergeben, ohne beiseitegeschoben
  zu werden“) → `holm_ansprechbar` → `holm_abschied` → **`der_freie_platz`**: zu viele Tassen, Chiara greift nach der
  der Kapitänin („tidy feels like control“); Wahl stehen lassen / selbst abräumen / gleich zur Lage.
- **T3 Sturm**: Chiara will „einen klaren Job und ihn perfekt machen“, „hält ihren Posten“ (story.json buehne).
- **T5**: Chiara hat zur Landung Megans die Crew in Uniform (`megan_kommt`).
- **T7 `zukunft`/`schlussbild`**: Romanze im Gespräch gewählt; „Ein Stuhl mehr“. Holms Nachtantwort soll an T7
  wiederkehren (wochenbogen.1 wache_mit_holm.kern) – konkrete T7-Szene mit Holm gibt es nicht, nur hy_holm_letzter_anruf T6.

---

## 7. Widersprüche, 7-Tage-Reste, Passung zur neuen Prämisse

### Widersprüche
1. **Holms Alter** 48 (Karte, LB 2/42) vs. **56** (basis:471, modul_py:116, LB-Kopie in den Karten-JSONs Eintrag 2,
   PS base_prompt). Die Karten-JSON trägt also ein älteres Weltbuch als ST.
2. **Holms Look**: Karte/Sprite-Tags brünett, Hochsteckfrisur, volle Figur vs. PS base_prompt „lean, short silver-grey,
   compass tattoo, reading glasses“; Event hy_holm_krankenhaus: „Die Brille sitzt schief“ (Brille gibt es nur im alten Prompt).
3. **Holms Stimme**: Engine „Warrior Woman“ vs. Karte „Freya“.
4. **Salzlakritz**: Mission „schwedische Salzlakritz“ (Siris Koffer) vs. Item „norwegischer Salzlakritz“; Holms Antwort
   „Tack.“ ist Schwedisch (Norwegisch: „Takk“) – evtl. gewollt als Geste an Siri, dann markieren.
5. **Holm romanzierbar?** Karte voll intim (Hitze 1–5, Kajüte), Engine `romanzierbar: False`, Brain Trust ohne Holm.
6. **Chiaras Alter** 29 vs. 31 (LB 13, Doppeleintrag zu LB 10).
7. **Chiaras Prüfung**: Karte „Yachtmaster Offshore, Theorie, Wiederholung Oktober Nizza“ vs. story.json h_01
   „Wachoffiziersprüfung“; altes Storylet „Yachtmaster theory“.
8. **Sterne**: Mission chiara_sterne „Ihr **Vater** hat es ihr immer versprochen und nie getan“ – Karte: Opa mit Sextant,
   sie übt selbst nachts Astronavigation; der Vater kommt nie vor. Widerspricht auch „fragt nie um Hilfe bei Navigation“
   (könnte gerade der Wendepunkt sein, dann aber Opa statt Vater).
9. **Wer führt nach Holm?** g1_chiara_tender „Seit Holm weg ist, führt Chiara den Laden“ vs. Story `kommando_duc`.
   Lesbar als Chiaras Anspruch – dann sollte der Text das als ihre Behauptung zeigen.
10. **Rollenangabe in der Anfrage**: Chiara ist **nicht** Erste Offizierin/Bootsfrau, sondern Chief Stewardess;
    Erster Offizier = Duc, Bosun = Totò.
11. Basis-Reste: `PERSONA_BERATER.start_items` mit holm_compass (basis:83, von modul_py:91 überschrieben); basis
    fixpunkt „Tag 1 Frühstück Blackout: Holm leaves by helicopter“ (basis:139, ungenutzt); basis-Welt „Calvi … inverter
    three burnt out“ (alte Gestrandet-Version).

### 7-Tage-Reste (müssen für 21 Tage umgebaut werden)
- Ganze Holm-Taktung: hy_holm_krankenhaus T2–3, hy_holm_nacht T3–6, hy_holm_letzter_anruf **T6** („Tomorrow it's
  decided“), siri_lakritz T3–7.
- Ziel „Calvi in 7 Tagen / Schlepper 80.000 € aus der Prämie“ (modul.json ziel, prolog, welt); Megans Ultimatum
  „innerhalb der Woche“.
- Karten-Setting: Antibes, Mitte August, „noch acht Wochen Saison“, Charter jede zweite Woche – Engine: Saisonende,
  Winterwerft Calvi – neue Prämisse: Sommer, 21 Tage bis zur Festa. Drei Zeitlinien.
- Chiara-Events mit Fenstern T2–7, Festa-Events T4–5 (gv_festa_kleid, gv_festa_outfits) – Festa ist jetzt Tag 21.
- Abschluss-Epiloge (kern/abschluss.py:181ff.) „mehr Respekt als vor einer Woche“, „Liste für die Werft“.

### Passung zur neuen Prämisse (START.md)
- **Holm = Kapitänin**: passt vollständig. Ihr Kartenwunsch „jemand, dem ich das Boot übergeben kann“ und ihr Geheimnis
  „letzte Saison, Mutter in Ålesund“ sind ein fertiger Bogen für 21 Tage (Übergabe → Prüfung per Telefon → Entscheidung).
- **Evakuierung**: Blinddarm-Hubschrauber an Tag 2 passt zur Akt-1-Woche (Tag 2 = Strandung + Megans Ultimatum).
  Neu zu klären: Im Cold Open gibt es jetzt eine **Motorexplosion** (Maxwell rettet Totò und Lea). Ein zufälliger
  Blinddarm am selben Morgen wirkt nach Kriterium 5 (plausibel, kein Kitsch) wie Bequemlichkeit des Drehbuchs –
  entweder bewusst setzen (Karte: „seit zwei Tagen Seitenschmerzen“, Party „winkt ab“ → sie hat es verschleppt, die Nacht
  hat es kippen lassen) oder an die Explosion koppeln (Verletzung). Megan kommt laut Akt-1-Plan **auch** per Hubschrauber
  (Tag 5) – zwei Hubschrauber-Szenen in fünf Tagen, Bild doppelt sich.
- **Anhörung Tag 7**: Holm ist eine natürliche **Zeugin per Video** (sie hat die Nacht geführt, kennt Logbuch/Uhrzeiten,
  Ermittlungsweg „Holm im Krankenhaus anrufen“ existiert). Zeugen sollen eigene Loyalität haben und lügen können –
  Holm lügt nie, aber sie schützt ihre Crew durch Schweigen („nennt keinen Namen“-Haltungen gibt es schon).
  Megans Bauchgefühl („Ein PX-480 brennt nicht einfach so“) und Holms Werft-Vermutungen ergänzen sich: zwei Seeleute,
  die beide spüren, dass es nicht nur ein Fehler an Bord war. Holm kennt Megan seit 11 Jahren (LB 45).
- **Alon-Manipulation**: Holm hat in mehreren Fassungen nachmittags/nachts Anzeigen gesehen und als „Werft“ abgetan;
  das lässt sich zu einem frühen, unscheinbaren Alon-Hinweis umbauen (z. B. sie erwähnt das rote Licht im Maschinenraum
  nebenbei). Tag-6-Anruf „Es ist dein Boot“ gehört dann vor die Anhörung.
- **Rückkehr**: Nach einer Blinddarm-OP ist sie nach 2–3 Wochen wieder einsatzfähig → **Rückkehr zur Festa (Tag 21)**
  wäre plausibel und schließt den Bogen: Wem gibt sie das Kommando zurück/weiter? Das ist auch der natürliche Moment,
  in dem Chiaras Kränkung aufgelöst werden kann.
- **Chiara = die Gekränkte, die das Kommando wollte**: Die Karte trägt das schon (Kapitänsfamilie, „das Mädchen sollte
  Gastgeberin werden“, gescheiterte Prüfung, Wunsch „eigenes Kommando“). Es fehlt die sichtbare Szene. Logik der Kränkung:
  Holm gibt das Kommando dem Mann mit Patent nach drei Wochen statt der Frau nach sechs Saisons – formal richtig, emotional
  ein Schlag, und Chiara kann nicht protestieren, ohne ihre Prüfung zu verraten. Holm weiß nichts von der Prüfung
  (Karte), Megan schon (LB 37) → Hebel für Megan in Akt 1.
- **Lebensziel (Thema 6) – Kandidaten aus dem Material**: Wiederholung im Oktober in Nizza (liegt nach dem Sommer, passt)
  bzw. eigenes Kommando. Achtung Ende-Regel story.json ende.regel: „Keine … bestandene Prüfung ohne etablierte
  Voraussetzungen“ → der Bogen muss das Lernen mit Duc (Sterne, Kartentisch) etablieren. Bogen-Momente bieten sich an:
  Kartentisch/„hypothetische“ Frage (Karte), Nachtwache/Sterne (Mission), Sextant des Opas, Prüfung laut aussprechen.
- **Holm ↔ Chiara als Paar**: Spiegel wie Megan/Alon – Holm hat das Kommando und will es abgeben dürfen; Chiara will es
  und darf es nicht zugeben. Gemeinsamer Gegenstand: Messingkompass (Holm, Vater) vs. Messingsextant (Chiara, Opa).
  Gemeinsame Kink-Zeile beider Karten: „einmal nicht das Kommando haben“.
- **Romanze**: Chiara ja (bestätigt). Holm: nein laut Engine/Brain Trust – Kartenintimität entweder behalten (nur ST)
  oder dämpfen.

---

## VERDECKT – Fall-Rollen (nicht im Chat nennen)

Quelle: story.json faelle[0..5] (gebaut aus werkzeuge/eden_rise/story_faelle.py: Fall 1 ab :306, 2 :423, 3 :538,
4 :680, 5 :791, 6 :913). Verdächtige: chiara, lea, sophia, rosi, yasin; `ermittlung.verdacht` chiara, sophia, rosi, lea.

### Chiara
- **Fall 1 „Übung auf der Brücke“ – Chiara verantwortlich.** Kern: Sie übt nach der Party heimlich eine Diagnose für
  ihre Prüfung, aktiviert nach einem Schutzabbruch das dokumentiert wirkende, aber nicht freigegebene Rückfallprofil R2
  (Bordhandbuch S. 4-17) und glaubt, es mit „Diagnose beenden“ zurückgesetzt zu haben. R2 bleibt aktiv; das
  vorgeschädigte LM3 fällt unter Dauerlast aus (06:12).
  - Zeitleiste: T1 16:10 druckt Übung 4-17 · 19:30 Ordner Register 4-17 in der Pantry (Duc sieht ihn, wenn er beim
    Service hilft: Fakt f1_14) · T2 01:55 verlässt Afterparty („muss lernen“, Lola sieht es) · 02:02 Schlüsselbund mit
    Glöckchen an der Brückentür (Totò hört es) · 02:05 Diagnose · 02:22 Schutzabbruch · 02:24 R2 · 02:26 „Diagnose
    beenden“, Übungsblatt bleibt am Pult · 02:30 zurück in der Messe, Tee, 02:45 Koje.
  - Lüge: „Bis halb drei in der Messe gelernt“ (f1_11) gegen Lola (f1_10); auf Nachfrage „kurz draußen, frische Luft“ (f1_12).
  - Gegenhandlungen: T2 Nacht (Angst ≥ 1) **Aushang an der Brückentür „Zutritt nur Kommando und Technik – Sicherheit
    nach dem Vorfall. C. Sonnberg“** (f1_15; Gegenmittel: Duc hebt ihn als Kommandant auf) – passt thematisch genau zur
    Kommando-Kränkung. T3 Nacht (Angst ≥ 2) nimmt sie ihr Übungsblatt aus der Logbuchmappe (f1_16, Hülle leer).
  - Geständnis: freiwillig ab T3 bei Vertrauen ≥ 3 + ein Kettenglied bekannt („bittet selbst um ein privates Gespräch“);
    Konfrontation ab T4 nur mit allen drei Gliedern; nie durch Intim/Geschenk/einzelnen Charme-Wurf.
    **Kernsatz: „Ich wollte einmal nicht die sein, die den Kaffee bringt, während andere entscheiden.“**
  - Wiedergutmachung: trägt den Vorgang selbst in den Bericht ein, arbeitet unter überprüfbaren Zuständigkeiten mit.
    „Kein geschenktes Kommando, keine geschenkte Qualifikation.“
  - Angst steigt nur, wenn sie von der Ermittlung erfährt; sinkt bei privatem Gespräch ohne Vorwurf ab V3.
  - Nachtende-Nachricht T3: Totò (f1_09, f1_10).
  - **Fit zur Prämisse**: Motiv ist exakt „die Gekränkte, die das Kommando wollte“ (Kernsatz). Mit Alons Vormanipulation
    wird ihre Tat zum Auslöser, nicht zur alleinigen Ursache – Megans Erbarmen in der Anhörung wird plausibel.
- **Fälle 2–6 – Chiara unschuldig**, mit Alibi: lernte 01:30–02:45 in der Messe für ihre „Wachoffiziersprüfung, von der
  niemand wissen soll“ (h_01), Lola bestätigt (h_02); Druckauftrag T1 16:10 „Kollisionsverhütung Kap. 3, Benutzer
  C. Sonnberg“ (h_03); Auftakt-Erinnerung: Ordner Register „Kollisionsverhütung“, klappt ihn schnell zu (h_22). Ihr
  Prüfungsgeheimnis macht sie also in jedem Durchlauf verdächtig (rote Spur). Sie hörte Rosi um Viertel vor drei
  schnarchen (h_16) – Entlastung für Rosi.
  - **Fall 6** („Niemand an diesem Tisch“, kein Täter, LM3 versagt im Normalbetrieb): Chiara unterschreibt mit Totò,
    Yasin, Lola die Liste „Wir glauben, es war Rosi“ (f6_12); **sie ist die Nachtende-Absenderin** mit h_16 (entlastet
    den Sündenbock Rosi).

### Holm (in keinem Fall verantwortlich; Wissen je Fall in `holm_tag1`, danach per Telefon)
- Gemeinsam: schließt um 00:45 die Brücke ab (r_08); Reiseplan v1 (T-5, Abfahrt T2 07:00 direkt Calvi) ist ihrer;
  Plan v2 (Nachtfahrt + Morgenhalt Cala d'Orsu, über Sophia eingereicht) von ihr genehmigt; sie gibt Lea die
  Routenplanung als Übung; bringt die Yacht mit Bugstrahlruder + Unit-01 in die Bucht; sichtbare Bauchschmerzen
  „medizinisch, kein Hinweis“; kennt Megans Werftfenster/Berichtsforderung (zweite_wahrheit z_04).
- **Fall 1**: findet 02:40 die Brückentür offen, Anzeige „PROFIL R2 BEREIT“, hält es für eine Werfteinstellung; legt das
  Übungsblatt (Chiaras Handschrift, Bleistiftzeiten 2:05/2:22/2:24) in die Logbuchmappe; fährt um 03:00 im Profil R2 ab.
  Sagt: „Die Tür war offen. Ich hatte um Viertel vor eins abgeschlossen.“ Vermutung: Werft. Tipp: „Holm hat beim
  Kaffee erzählt, sie hat nachts einen Zettel in die Logbuchmappe gesteckt.“ Sie ist damit **die Schlüsselzeugin
  gegen Chiara**, ohne es zu wissen.
- **Fall 2** (Lea): „Wir sind schneller gefahren, als mir lieb war“; Lea 06:15 auf der Brücke, fragt nach WP4; erinnert
  Duc, dass **er** abgezeichnet hat.
- **Fall 3** (Sophia): ließ sich zur Abfahrt 01:30 ohne Ladelauf breitschlagen (Sophia beruft sich auf Megan); nimmt die
  Schuld auf sich: „Ich hätte nicht nachgeben dürfen.“ Nennt Sophia nur, wenn Duc nach dem Plan fragt.
- **Fall 4** (Rosi): drückt nach SERVICE-SPERRE + Schutzstopp den angebotenen „Wiederanlauf“ → Ausfall. „Ich hab's
  kaputtgedrückt.“ holm_rolle: gehört in den Bericht, „folgte der Anzeige, nicht schuldhaft“; nimmt Duc ernster, wenn
  er sie entlastet.
- **Fall 5** (Yasin): Yasin unterschrieb bei ihr T1 11:00 die 2-kW-Lastgrenze; sie sah 06:22 die Schutzabschaltung am Heck,
  rief in die Tendergarage, keiner antwortete; zeigt Richtung Tendergarage, nennt keinen Namen.
- **Fall 6** (kein Täter): quittierte T1 17:20 eine LM3-Temperaturwarnung („Werft soll in Calvi drauf schauen“, f6_05);
  ihre Warnung ist Gegenmittel gegen Megans Bedienfehler-Entwurf; hält Ermittlungen gegen die Crew für Zeitverschwendung.
- **Zweite Wahrheit** (Megans administrative Mitzeichnung trotz Herstellermeldung PX-480 Charge 22-B): Holm weiß davon
  nichts; sie ist nur Wissende von z_04 (Ultimatum). Bericht „vollständig“ enthält „Holms Handgriffe“ (bericht.fassungen).
- **Fit zur Prämisse**: Holms Werft-Vermutungen in allen Fällen und ihre quittierte Warnung lassen sich direkt auf Alons
  Vormanipulation umdeuten (sie spürte, dass das Modul „krank war, bevor wir losfuhren“). In der Anhörung könnte sie als
  Zeugin per Video ungewollt Chiara belasten (Logbuchmappe) und gleichzeitig Megans Bauchgefühl stützen.

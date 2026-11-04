# Text-Audit Akt 1 und 2 · Rückbezüge und schwieriges Englisch

Stand 04.11.2026 · Cloud-Sitzung, Branch `audit-text` · **Nur Bericht, kein Text geändert.** Maßstab: `docs/wiki/STIL.md`, Abschnitt 3 („Verständlich bleiben“).

## Umfang und Methode

- Geprüft: `module/eden_rise/*.json` (gebaute Texte) und die Builder `werkzeuge/eden_rise/ereignisse_*.py`, dazu `werkzeuge/englisch/item_lore.py` für Item-Texte.
- **Ausgelassen (nicht geöffnet, nicht zitiert):** alle Texte mit den Kennungen `vh.`, `fv_`, `rt_t_`, die Datei `module/eden_rise/story.json`, die Handy-Ketten (`hy_`, `handy.json`, `rast_anrufe.json`) und die Selfies (`sf_`, `sfn_`), weil sie zum Handy gehören. Die Dateien `ereignisse_favours.py`, `ereignisse_handy.py`, `handy_eden_rise.py` sind nicht geöffnet. Interne Hinweise und die deutschen `de`-Felder zählen nicht als Spieltext.
- Werkzeug: `tests/audit_text.py` (neu) sucht Kandidaten: 741 Rückbezug-Stellen, 31 Redewendungen, 1.772 seltene Wörter (Zipf-Häufigkeit unter 2,6 nach `wordfreq`). Danach habe ich jeden Kandidaten von Hand gelesen. Die meisten Rückbezüge sind in Ordnung (sie tragen die Erinnerung schon, z. B. *“that night on the swim platform, when the squid were up”*), die meisten seltenen Wörter sind Seemanns- oder Figurensprache, die bleiben darf (Lolas *arvo*, Leas *dreckly*, Maxwells *lekker*).
- **Priorität:** P1 = Szene, die jeder Spieler sieht (Tag 0, Hafenkampf, Pflicht-Events, Gags im Zufallspool), oder Szene mit einem Rückbezug, der ohne Erinnerung nicht verständlich ist. P2 = häufige Szene mit einem seltenen Wort. P3 = Item- und Randtexte.

Die Zeilennummern beziehen sich auf den Stand von `master` (bdb05cc).

## 1. Rückbezüge ohne Erinnerung im Satz

| P | Datei:Zeile | ID | Altes Wort oder Satz | Problem | Vorschlag (einfaches Englisch) |
|---|---|---|---|---|---|
| P1 | `ereignisse_romanzen.py:101` | `rm_r3` | “I'd have to kill you and I need you for **the relay**.” | Das Relais war in `rm_r1`, frühestens drei Tage vorher. Genau Ducs Beispiel aus STIL.md | “I'd have to kill you, and I still need you for that relay, the one you held the lamp for.” |
| P1 | `ereignisse_romanzen.py:852` | `rm_e_siri_nein` | “You said another night, **about the jumper**.” | Welcher Pullover? Der Spieler hat Siris Szene vielleicht vor zwei Tagen gesehen | “You said another night, when I held out my father's jumper with the stars. I wasn't sad.” |
| P1 | `ereignisse_legenden.py:236` | Legende Hafen, Don | “Yes, yes, the bell was wrong **that day**.” | Don spricht vom Hafenkampf an Tag 2, die Legende kommt viele Tage später | “Yes, yes, the bell was wrong on the day of the dogs at the harbour.” |
| P1 | `ereignisse_ligeia.py:147` | `lg_lied` | “...hasn't slept properly **since the storm**.” | Der Sturm war an Tag 5, die Szene kommt in Akt 2 | “...since the big storm, the night the yacht nearly broke loose.” |
| P1 | `ereignisse_romanzen.py:891` | `fl_rosi_vespa` | “I remember what I said about holding on. **the other night** you held on just fine” | Zwei Rückbezüge in einem Satz, keiner sagt, wo | “I remember what I said on my Vespa about holding on. the other night, in the engine room, you held on just fine” |
| P2 | `ereignisse_romanzen.py:79` | `rm_r2` (Chip) | “Is this what you want, or is this **the bet** talking?” | In der Szene selbst erklärt (Stoppuhr), aber der Chip steht ohne Lage auf der Karte | “Is this what you want, or is it the stopwatch talking?” |
| P2 | `ereignisse_romanzen.py:534` | `rm_e_chiara_duc` (Chip) | “**Nine and a half**, you said.” | Die Zahl kommt aus *Vega*, der Chip steht allein | “Nine and a half, you said last night. On the bridge wing.” |
| P2 | `ereignisse_romanzen.py:875` | `rm_e_megan_nacht` | “I said **that night** was off the record” | Megan ist fern, die Nacht liegt eventuell länger zurück | “I said our night in the VIP cabin was off the record, and so it is.” (Ort an die tatsächliche Szene anpassen) |
| P2 | `ereignisse_romanzen.py:903` | `fl_lola_mehl` | “**Last time** you walked back to your cabin like that” | Welches Mal? | “The last time you had flour on your shirt, you walked back to your cabin like that, and I laughed for an hour.” |
| P2 | `ereignisse_red_trio.py:456` | `rt_wn_bibi` (Chip) | “I heard you **at the fire**.” | Welches Feuer? Gemeint ist das Lagerfeuer im Trio | “I heard you at the campfire with the three of you.” |
| P2 | `ereignisse_dorf.py:504` | `g1_vb_eintopf` | Bà Tư: “You said this **last week**.” | In Ordnung, wenn der Gag vorher lief. Läuft er zum ersten Mal, fehlt der Bezug | “You said this last time I brought you stew. And then the pot was clean.” |
| P3 | `figurenrahmen.json`, `figuren.*.momente` (sieben Frauen) | Echo nach der Intim-Szene | “**The other night** went a lot further than I expected …” | Muster: „the other night“ steht 32-mal in den Figurenrahmen der sieben Frauen. Für die Intim-Szene ist der Bezug klar, für die Zärtlichkeit ohne Intim-Szene nicht | Den Ort einbauen, den die Szene hatte: “The other night in the galley went a lot further than I expected.” Der Code kennt den Ort (`moment`), die Zeile kann `{ort}` tragen |

**In Ordnung, obwohl der Prüfer sie fand** (Beispiele): `rm_l1` (*“You said to wake you next time I went diving”*), `bg_weg_c_hart` (*“you said to me at the tower”*), `a2_koordinaten_ohne` (*“since the day Kevin stole the page”*), alle `uebergaenge.json`-Zeilen (*“you said no to Chiara the other night”*), Leas *“that night on the swim platform, when the squid were up”*.

## 2. Seltene oder doppeldeutige Wörter

| P | Datei:Zeile | ID | Altes Wort oder Satz | Problem | Vorschlag (einfaches Englisch) |
|---|---|---|---|---|---|
| P1 | `ereignisse_tag0.py:171` (und drei weitere Startwahlen) | `t0_wahl`, `t0_wahl2_*` | “Visits Jana, the new **deckhand**” | Tag 0, sieht jeder. *deckhand* ist selten | “Visits Jana, the youngest of the deck crew” |
| P1 | `ereignisse_tag0.py:76`, `:268` | `t0_holm`, `t0_abschied_*` | “Megan leads you to the **gangway**”, “Heads for the **gangway**” | Tag 0. *gangway* kommt 23-mal im Spiel vor, darum einmal erklären statt überall ersetzen | In `t0_holm`: “Megan leads you to the gangway, the narrow bridge from the quay up to the yacht.” Danach darf *gangway* bleiben |
| P1 | `ereignisse_tag0.py:139` | `t0_toto` | “Totò, our **bosun**.” | Tag 0, sehr selten | “Totò, our bosun. He runs the deck crew.” |
| P1 | Raumnamen, 84 Stellen | `foredeck` | “**foredeck**” | Ein Kernort, aber für Nicht-Muttersprachler unklar | Einmal erklären, wo der Ort zum ersten Mal vorkommt: “the foredeck, the open deck at the front of the yacht”. Danach bleibt das Wort |
| P1 | `ereignisse_hafen.py:186`, `kaempfe_eden_rise.py:593` | `hk_casanova`, `hafen_keiler` (ko) | “The boar **snorts**, turns, and **trots** back into the macchia **as if it had an appointment**” | Hafenkampf an Tag 2, zwei seltene Verben und eine ironische Wendung | “The boar makes a loud noise, turns and walks back into the macchia, as if it had somewhere better to be.” |
| P1 | `ereignisse_tag0.py:140` | `t0_toto`, `t0_jana` | “Potatoes. Very **small potatoes**.” | *small potatoes* ist eine Redewendung (unwichtig). Totòs Witz funktioniert nur, wenn man sie nicht kennt, und wer sie kennt, liest etwas anderes. Doppeldeutig | Lassen, wenn der Doppelsinn gewollt ist. Sonst: “Potatoes. Very small ones.” |
| P2 | `ereignisse_gag1.py:275` | `g1_helikopter` | “The **downdraught** rips the towel off Lola” | sehr selten | “The wind from the rotor blows the towel off Lola” |
| P2 | `ereignisse_gag1.py:343` | `rosi_werkstatt_offen` | “It doesn't give orders any more, it **eavesdrops**.” | Wichtige Regel (Chip hört mit), seltenes Wort | “It doesn't give orders any more. It listens to them.” |
| P2 | `ereignisse_gag1.py:329` | `rosi_werkstatt_offen` | “behind a **tarpaulin**” | selten | “behind a big plastic sheet” |
| P2 | `ereignisse_gagv.py:135` | `gv_casanova_chiara` | “board the yacht **ceremonially**” | selten | “come on board with a ceremony, with a sash and a photographer” |
| P2 | `ereignisse_gagv.py:14` | `gv_ocean_glitter` | “Lola **relabelled** every single jar” | selten | “Lola gave every jar a new label” |
| P2 | `ereignisse_grotte.py:402` | `kv_nest` | “Kevin **sulks** on the **weathervane**” | zwei seltene Wörter | “Kevin sits on the metal arrow on the roof, in a bad mood” |
| P2 | `ereignisse_grotte.py:395` | `kv_glocke` | “Up the **drainpipe**” | selten | “Up the rain pipe” |
| P2 | `ereignisse_wiki.py:338` | `g1_petru_netze` | Totò: “He **mends** it every afternoon” | selten; Kern von Petrus Trauer, darf nicht untergehen | “He repairs it every afternoon, since Marie died. Five years.” |
| P2 | `ereignisse_kloster.py:212` | `kl_nische_fund` (und `_voll`, `_leer`) | “Wrapped in an **oilcloth**” | selten | “Wrapped in an old waxed cloth” |
| P2 | `ereignisse_kloster.py:195` | `kl_gabelung` | “something **glints** in a niche” | Entscheidungsszene (Spur-Uhr), das Wort muss sitzen | “something shines in a gap in the rock” |
| P2 | `ereignisse_kloster.py:157` | `kl_tor` (Chip) | “She **vouches** for me.” | selten, Witz-Chip | “She says I'm okay.” |
| P2 | `ereignisse_grotte.py:290` | `gr_u1_start` | “something thick and dark **uncoils**” | selten | “something thick and dark slowly unrolls itself” |
| P2 | `ereignisse_wiki.py:223` | `br_fish_pie` | “Petru has fixed the **davit**” | Fachwort ohne Erklärung | “Petru has fixed the small crane for the tender” |
| P2 | `ereignisse_wiki.py:301` | `g1_lea_nachttauchen` | “Elsa's patrol boat **idles** twenty metres off” | doppeldeutig (faul sein) | “Elsa's patrol boat waits twenty metres away, engine running” |
| P2 | `ereignisse_berge.py:159` | `bg_turm` | “men in Legion **fatigues**” | doppeldeutig (Müdigkeit) | “men in Legion uniforms” |
| P2 | `ereignisse_berge.py:176` | `bg_turm_parole` | “in a **scabbard** worn pale” | selten | “in an old, pale sheath” |
| P2 | `ereignisse_berge.py:631` | `bg_wieder` | “The **switchbacks** are quieter now” | selten | “The steep, winding path is quieter now” |
| P2 | `ereignisse_staerken.py:203` | `auf_karaoke` | “The microphone **crackles**” | selten, aber lautmalend | darf bleiben, sonst “The microphone makes a scratchy sound” |
| P2 | `ereignisse_gagv.py:330` | `gv_einkaufsliste` | Lola: “that's how **mutinies** start” | selten, aber Lolas Witz | “that's how a crew turns against its captain” |
| P2 | `anhoerung_aussagen.py:159`, `:379` | Anhörung (Aussage) | “out to a **waypoint**”, “A **switchover** is not a cold start” | Anhörung, Spieler muss die Aussage verstehen, um richtig zu wählen | “out to a point on the map off the coast, WP4” · “Switching from one power source to the other is not a cold start.” |
| P3 | `werkzeuge/englisch/item_lore.py:168` | `whetstone_blue` | “**Draw** the blade across it slowly” | *draw* ist genau Ducs Beispiel für ein doppeldeutiges Wort (STIL.md) | “Pull the blade across it slowly, and it starts to sing.” |
| P3 | `item_lore.py:127` | `panel_cleaner` | “a **squeegee**. **Glamorous it isn't.**” | seltenes Wort und umgestellte Satzform | “a rubber wiper. It isn't glamorous.” |
| P3 | `item_lore.py:18` | `arancini` | “wrapped in **greaseproof** paper” | selten | “wrapped in baking paper” |
| P3 | `item_lore.py:30` | `cap_corse` | “with **quinine** and orange peel” | selten | “a bitter Corsican aperitif with orange peel” |
| P3 | `item_lore.py:60` | `old_chart` | “Some of the **soundings** are wrong now” | doppeldeutig (Klänge) | “Some of the depth numbers are wrong now” |
| P3 | `item_lore.py:107` | `siris_halstuch` | “A silk **neckerchief**” | selten | “A silk scarf for the neck” |
| P3 | `item_lore.py:116` | `plektrum` | “A purple **plectrum**” | selten | “A purple guitar pick” |
| P3 | `item_lore.py:201` | `taschen` | “each logo slightly **misspelt**” | selten (britisch) | “each logo spelled a little wrong” |
| P3 | `ereignisse_berge.py:700` | `bg_b_postkarte` | “a blue boat on **trestles**” | selten | “a blue boat up on wooden stands” |
| P3 | `module/eden_rise/kuechen.json` (Zutaten) | `tench_roh`, `barbel_roh` | Fischnamen *tench*, *barbel* | Fischnamen dürfen selten sein, aber der Text hilft nicht | “From the tench, a slow green river fish.” |

## 3. Redewendungen

| P | Datei:Zeile | ID | Alt | Problem | Vorschlag |
|---|---|---|---|---|---|
| P2 | `ereignisse_bordrat.py:212` | `br_ein_tisch` | “now that everyone's **in the same boat**” | Redewendung, auf einer Yacht doppeldeutig | “now that everyone is stuck here together” (oder bewusst lassen, dann ist es ein Wortspiel) |
| P2 | `story_buehne.py:399` | freie Szene, Abend | “not quite ready to **call it a day**” | Redewendung in einer Vorlage, die sehr oft läuft | “not quite ready to go to bed” |
| P2 | `missionen_eden_rise.py:394` | Mission (Siri) | “Siri gets **cold feet**” | Redewendung | “Siri gets nervous” |
| P3 | `ereignisse_grotte.py:410` | `kv_nest` (Chip) | “He collected it **fair and square**.” | Redewendung | “He collected it honestly.” |
| P3 | `ereignisse_holm.py:167` | `hb_g_wolff` | Wolff: “you did it **by the book**” | Redewendung, passt aber zu Wolff (Dienstvorschrift) | lassen, Figurenstimme |
| P3 | `ereignisse_gag1.py:217` | `g1_holm_kaffee` | Holm: “**Mind** your boat, not my stomach.” | *mind* im Sinn von „kümmere dich um“ ist für Lernende unklar | “Look after your boat, not my stomach. …Takk.” |
| P3 | mehrere (`hk_abend`, Alva, Totò) | „on the house“ | “First round's **on the house**.” | Redewendung, aber bekannt und Alvas Kanon | lassen |
| P3 | `ereignisse_wiki.py:408`, `bl_wache_elsa_bericht` | Elsa | “**for the record**” | Elsas Protokoll-Stimme, Kanon | lassen |

## 4. Muster (für alle, die weiterschreiben)

1. **„The other night“, „that night“, „last time“** kommen über 140-mal vor. Faustregel: Liegt die Szene mehr als einen Spieltag zurück oder kann sie in beliebiger Reihenfolge kommen, gehört ein Ort oder ein Gegenstand in denselben Satz.
2. **Chips** sind die gefährlichste Stelle: Sie stehen ohne Lage auf dem Bildschirm (`rm_r2`, `rm_e_chiara_duc`, `rt_wn_bibi`). Ein Chip mit Rückbezug braucht die Erinnerung immer im Chip selbst.
3. **Seemannswörter** (*gangway, foredeck, bosun, davit, bollard*): einmal im ersten Auftritt erklären, danach dürfen sie bleiben. Das ist Atmosphäre, kein Fehler.
4. **Lautverben** (*snorts, trots, slinks, sulks, squeals, crackles*) häufen sich in Kampf-Ausgängen (`kaempfe.json`). Einzeln harmlos, zusammen eine Hürde. Vorschlag: In Ausgangstexten höchstens ein seltenes Verb.

## 5. Nebenbefund (nicht Teil des Auftrags, zur Weitergabe)

- Chiara bewertet laut Stimmen-Durchgang „auf ihrer Zehnerskala, nicht mit Sternen“ (`docs/wiki/welt/drehbuch_finale.md`, Abschnitt 10, Zweiter Durchgang, Zeile Chiara). Auf der Taktik-Karte sagt sie noch *“One star. My taser does nothing to it.”* (`werkzeuge/eden_rise/taktik_eden_rise.py:253`) und ihr Ruf lautet *“Five stars for the taser. Zero for you.”* (`taktik_eden_rise.py:153`). Gehört in den Wiki-gegen-Code-Bericht.

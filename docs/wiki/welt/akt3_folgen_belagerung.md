# Akt 3 · Was die Belagerung hinterlässt (Flags und Wirkpunkte)

> Stand 04.11.2026 · Besitz: Brain Trust (Analyse der Cloud-Sitzung, Branch `folgen-belagerung`) · **Bericht und Vorschläge, nichts gebaut.**
> Quellen: `werkzeuge/eden_rise/ereignisse_belagerung.py`, `ereignisse_belagerung_nacht.py`, `taktik_eden_rise.py`, `kern/taktik.py`, Grep über das ganze Repo
> (ohne die Handy- und Favours-Dateien, die nicht geöffnet werden). Regeln für die Vorschläge: [`akt3.md`](akt3.md) (Durchatmen, Wiederaufbau als Kern,
> Romanzen fertig spielen, Mechaniken meistern, Festa-Aufträge, wenige ernste Missionen, Zeugen für Tag 35).

## Offene Entscheidungen, die hier **nicht** als Tatsache gelten

Quelle: [`drehbuch_finale.md`](drehbuch_finale.md) Abschnitt 9 und 11. Jeder Vorschlag unten, der davon abhängt, ist mit **(offen)** markiert und nennt beide Fälle.

| Offen | Was es für Akt 3 bedeutet |
|---|---|
| **Yacht „auf Grund gesetzt“ statt gesunken** (Crew schläft bei den Familien) | Alles, was „an Bord“ spielt, braucht eine Fassung für `tk_yacht_weg`, solange Duc nicht entschieden hat |
| **Minicus Überleben erst in Akt 3** | Kein Vorschlag setzt voraus, dass Minicu lebt. Wo er spricht, steht die Fassung ohne ihn daneben |
| **Festa-Events warten auf `akt3_festa`** | `br_ehrenbuerger`, `ab_casanova_flamenco`, `gv_rotes_kleid` bleiben, wie sie sind. Vorschläge hängen sich an, ohne das Flag zu setzen |

## Kurzbefund

- In den drei Dateien stehen **87 Bezeichner mit `bl_`**. Davon sind **44 Event-IDs** (Szenen, keine Flags) und **43 Flags oder Flag-Familien**.
- **Gelesen** werden 14 Flags oder Familien, fast alle nur **innerhalb der Belagerung** (Tag 21 bis 23). Nach Tag 23 liest heute **kein einziges `bl_`-Flag** irgendjemand.
- **Nie gelesen** werden 26 Flags. Drei davon sind **Fehler in Akt 2**, nicht nur offene Enden, weil das Drehbuch Finale ihnen eine Wirkung verspricht, die der Code nicht hat (Abschnitt „Fehler in Akt 2“).
- Rettungen, Rudern und Kevin sind **keine Flags**, sondern Zustand in `z["taktik"]` (`haeuser[...].status`, `dorf_rudert`, `gesehen`). Akt 3 kann sie lesen, solange der Spielstand `z["taktik"]` behält. Für Rudern schlage ich ein eigenes Flag vor (unten).

## Fehler in Akt 2 (Wirkung versprochen, aber nicht gebaut)

| Flag | Versprochen in | Was der Code tut | Beleg |
|---|---|---|---|
| `bl_tueren_petru`, `bl_tueren_lola`, `bl_tueren_mina` | `drehbuch_finale.md`, Abschnitt 5, „Tag 22, Mittag · Auftrag Türen“: mit Petru rudert das Dorf schon ab Ruf 4 | `_rudert()` liest nur Ruf und Petrus Werkstatt, die Wahl bei den Türen wirkt gar nicht | `kern/taktik.py:1599-1602`, gesetzt in `ereignisse_belagerung.py:204-208` |
| `bl_alva_runde` | `drehbuch_finale.md`, „Tag 22, Abend · Die letzte Runde“: mit dem Flag zahlt Duc die Runde, sonst Alva | `bl_bar` hat keine Bedingung und keine zweite Fassung, Alva zahlt immer | `ereignisse_belagerung.py:249`, gesetzt in `ereignisse_belagerung_nacht.py:160` |
| `bl_kirche_don` | `drehbuch_finale.md`, „Tag 23, Morgen · Auftrag Kirche“: Don läutet nüchtern, die Kirche hat 4 Leben | Die 4 Leben hängen am Wert `vertrauen.anghjulu` ≥ 3, nicht an der Wahl. Wer Don bei Vertrauen 3 **nicht** wählt, bekommt die 4 Leben trotzdem | `ereignisse_belagerung.py:309`, Wirkung in `taktik_eden_rise.py` (`VORBEREITUNG`) |

Vorschlag für die Akt-2-Sitzung: `_rudert()` um `bl_tueren_petru` erweitern (eine Zeile), `bl_bar` in zwei Fassungen teilen, beim Kirchen-Leben `bl_kirche_don` statt des reinen Werts lesen. Das ist eine Änderung an Spieldaten und gehört nicht in diese Analyse.

## Haupttabelle: alle Flags

**Spalten:** wo gesetzt (Datei:Zeile, Szene) · wer liest (Datei:Zeile) · Status · Wirkpunkt in Akt 3 (Vorschlag, Tag).
Status: **liest Akt 2** = nur während der Belagerung gelesen · **nie** = niemand liest es · **Test** = nur ein Test liest es.

### Vorbereitung und Aufträge

| Flag | Gesetzt | Gelesen | Status | Wirkpunkt Akt 3 (Vorschlag) |
|---|---|---|---|---|
| `bl_tafel` | `ereignisse_belagerung.py:68-69` (`bl_tafel`, Tag 15, Megans Kriegstafel) | – | nie | **Tag 25, Megans Rückkehr:** Sie sieht ihre alte Tafel in der Messe hängen, die Häkchen sind noch da. Eine Zeile, kein Wert. Zahlt Ducs Regel „Spieler vergisst“ aus: *“My list. Six jobs. You did {n} of them.”* Daraus wächst Casanovas Festa-Tafel als Echo (gleiche Form, anderer Zweck) |
| `bl_verband_duc` / `_maxwell` / `_chiara` / `_wolff` | `ereignisse_belagerung.py:164-167` (Pause „Versorgen“, Tag 21) | `kern/taktik.py:567` (Welle 2 mit vollen Leben) | liest Akt 2 | **Tag 24 bis 26, frei:** Wer den Verband bekam, bedankt sich einmal, in seiner Stimme. **Wolff:** Die Legion trägt einen Tag lang an einer Baustelle mit (+1 Stufe, Wirkpunkt `kern/aufbau.py`). **Chiara:** öffnet ihre Akt-3-Romanzenszene einen Tag früher. **Maxwell:** *“Mr. Maximum still has the bandage. Mr. Maximum is keeping it.”* (Gag bis Tag 31). **Duc:** nichts, Lola: *“You kept it for yourself? Good. Somebody on this boat has sense.”* |
| `bl_funk_white` | `ereignisse_belagerung.py:180, 185` (Auftrag „Funk“, Rosi oder Rosi mit Charly) | `taktik_eden_rise.py:227` (Whites Angebot nach Welle 5), `tests/test_taktik.py:1773` | liest Akt 2 | **Tag 35, Kommission (Säule Wahrheit):** Die Aufnahme von Whites Angebot an Pascal (*“Three days of fire, Pascal. You can end it tonight.”*) liegt als Beweis vor. Es ist der einzige Beweis, dass White den Verrat gekauft hat |
| `bl_funk_charly` | `ereignisse_belagerung.py:185` | – | nie | **Tag 35, Kommission:** Charly hat alles mitgeschrieben, mit Uhrzeit. Ihre Liste stützt die Aufnahme (zweiter Beleg, gleiche Säule). Dazu ein Satz in ihrer Stimme: *“Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.”* Und ein Grund für Rosi, ihr in Akt 3 eine Stelle anzubieten (Kanon E-098) |
| `bl_tueren_petru` | `ereignisse_belagerung.py:204` (Auftrag „Türen“, Tag 22) | – | **nie (Fehler, siehe oben)** | **Ab Tag 25, Zeugen:** Petru war mit Mina an jeder Tür. Die Leute, die damals aufgemacht haben, hören ihm jetzt zu. Seine Zeugen-Tür öffnet ohne Mindestvertrauen, und er bringt einen zweiten Namen mit (ein namenloser Fischer, Legenden-Kommentar) |
| `bl_tueren_lola` | `ereignisse_belagerung.py:206` | – | nie (Fehler) | **Tag 26, Festa-Tafel:** Lola kennt jetzt jede Küche im Dorf. Ihr Festa-Auftrag *The Menu* braucht ein Gericht weniger. Zeile: *“I've been in every kitchen in this village, Boss. Every single one. Mostly the biscuits.”* |
| `bl_tueren_mina` | `ereignisse_belagerung.py:208` | – | nie (Fehler) | **Tag 25, „Registered Post“:** Mina ging damals allein. Wenn sie die Drohbriefe zustellt, sagt sie: *“You let me go alone that night, when the phones were dead. I knocked on every door. I can do this too.”* Ihre Zeugen-Tür öffnet ohne die Post wiederaufzubauen |
| `bl_batu_norden` | `ereignisse_belagerung.py:264-265` (`bl_batu`, Tag 22, nur Vertrauen 3) | – | nie | **Ab Tag 25, Zeugen:** Bà Tư hat es Duc schon einmal gesagt. Ihre Zeugen-Tür ist offen, und ihre Aussage vor der Kommission nimmt genau die Zahl auf: *“They asked me twice. I told him. Now I tell you.”* |
| `bl_nachtwache_wolff` / `_elsa` / `_yamamoto` | `ereignisse_belagerung.py:269, 276, 280` (Auftrag „Nachtwache“, Tag 22) | `ereignisse_belagerung.py:286-294` (Bericht am Morgen), `kern/taktik.py` (`NACHTWACHE`, Welle 6), `tests/test_taktik.py:1738` | liest Akt 2 | **Tag 35, Kommission:** Wer Wache hielt, bezeugt den Funkspruch um drei Uhr (*“not yet”*). Elsa als Protokoll, Wolff knapp, Yamamoto förmlich. Ein Beleg mehr für Säule Wahrheit. **Tag 34, Villa:** Die Person steht im Hof, als Duc hinausgeht, und sagt einen Satz zu Pascal, keinen zu Alon |
| `bl_nachtwache_niemand` | `ereignisse_belagerung.py:272, 284` | `kern/taktik.py:1648` (Holms Satz in Welle 6) | liest Akt 2 | **Tag 28, Holms Revanche:** Holm sagt es noch einmal, leiser: *“I told you to send somebody to the north road that night. I should have gone myself.”* Kein Wert, nur ihr Bogen |
| `bl_wache_gesehen` | `ereignisse_belagerung.py:289, 293, 297` (Duc sagt es Holm) | – | nie | **Tag 27, Schublade:** Elsa findet in Pascals Schublade das Funkbuch der Nacht. Hat Duc es Holm gesagt, erkennt Holm die Uhrzeit sofort, und das Funkbuch wird ein Beweis. Sonst bleibt es ein Heft unter vielen |
| `bl_kirche_jana` | `ereignisse_belagerung.py:308` (Auftrag „Kirche“, Tag 23) | `kern/taktik.py:577` (Kirche verliert den ersten Treffer nicht) | liest Akt 2 | **Tag 26 bis 30, frei:** Die Mütter bringen Jana etwas an Bord (oder zu ihrem Gastbett, wenn die Yacht auf Grund sitzt, **offen**). Die Kinder malen Bilder für die Festa. Jana: *“Sorry. Sorry, they're... they're for me? Jessas.”* Festa-Auftrag „Kinderbilder“ als neunter, kleiner Auftrag ohne Material |
| `bl_kirche_don` | `ereignisse_belagerung.py:314` | – | nie (Fehler, siehe oben) | **Tag 35, Festa-Auftrag *The Bell*:** Don war schon einmal nüchtern, als es zählte. Er braucht am Morgen keinen Kaffee mehr von Duc: *“I did it once for the children. I can do it once for a dance.”* |
| `bl_kirche_casanova` | `ereignisse_belagerung.py:310, 318` | – | nie | **Tag 26, Festa-Tafel:** Casanova hat den Kindern eine lange Geschichte erzählt. Die Kinder wollen sie auf der Festa hören. Casanovas Rede bekommt einen zweiten Teil, und das Dorf klatscht dort zuerst für sie (vor Alva, Kanon bleibt: der große Applaus) |

### Abende und Nächte

| Flag | Gesetzt | Gelesen | Status | Wirkpunkt Akt 3 (Vorschlag) |
|---|---|---|---|---|
| `bl_will_ab_<pid>` | `ereignisse_belagerung_nacht.py:40` (Abend 21 oder 22, Wahl der Person) | – | nie | **Romanzen fertig spielen (Tag 24 bis 33):** Die Akt-3-Szene der Frau beginnt mit einem Rückbezug mit Erinnerung im Satz: *“That evening during the siege, on the quay, when you came to me and not to anyone else...”* So zählt die Wahl im Krieg in den Frieden hinein |
| `bl_will_ab_niemand` | `ereignisse_belagerung_nacht.py:95` | – | nie | **Tag 24, Morgen:** Holm nickt Duc einmal zu, eine Zeile: *“You slept, both nights. Good. Now you can work.”* Kein Wert |
| `bl_ab_fertig_<pid>` | `ereignisse_belagerung_nacht.py:48` | `ereignisse_belagerung_nacht.py:27` (zweiter Abend wird zu `bl_ab_schon`) | liest Akt 2 | Wie `bl_will_ab_<pid>`: Akt 3 liest besser `bl_ab_fertig_<pid>`, weil es auch bei einem Abend ohne Wahl gesetzt wird |
| `bl_will_na_<pid>` | `ereignisse_belagerung_nacht.py:44` (Nacht 20, 21, 22) | `ereignisse_belagerung_nacht.py:75` (Echo am Morgen, `flag_seit`), `nacht_bei` in `kern/taktik.py:1582` (Funk, +10 % Leben) | liest Akt 2 | **Tag 33, Festa-Frage:** Die Frau der letzten Belagerungsnacht steht oben in der Liste und fragt als Erste. **Tag 34, letzte Nacht:** ihr Name steht wieder oben. Nie öffentlich (E-060, Romanzen sind privat) |
| `bl_will_na_niemand` | `ereignisse_belagerung_nacht.py:190` | – | nie | Kein eigener Wirkpunkt. Die Nacht allein war Ducs Wahl. Höchstens eine Zeile Holms, wie bei `bl_will_ab_niemand`, beide zusammen |
| `bl_na_fertig_<pid>` | `ereignisse_belagerung_nacht.py:56, 66` | `ereignisse_belagerung_nacht.py:31-34` (zweite Nacht als `_wieder`) | liest Akt 2 | Zwei Nächte mit derselben Frau in der Belagerung: Ihre Akt-3-Szene ist „zusammen“ als Status (Folge `fakt`, gebaut) statt „offen“. Wirkpunkt ist die Chronik, die die freie Szene liest |
| `bl_alva_runde` | `ereignisse_belagerung_nacht.py:160` (Alvas Abend, Tag 21) | – | **nie (Fehler, siehe oben; bekannt)** | **Wiederaufbau der Bar (ab Tag 24):** Duc hat versprochen, die erste Runde zu zahlen, „when this is over“. Mit `aufbau_fertig_bar` (oder am Abend von Tag 24, wenn die Bar stand) löst Alva das Versprechen ein: Duc zahlt 120 € (echter Preis, Geld hat in Akt 3 sonst wenig Ziel, Spieltest-Befund 2). Auf Papas Tafel steht unter MINICU 11 *“Paid. P.”* jetzt eine zweite Zeile: *“Everyone. Paid. D.”* Alva: *“Two lines in two different hands. Papa would have liked that.”* Ohne Geld: Alva lässt anschreiben, Festa-Auftrag Alva bleibt trotzdem offen |

### Welle 6, Minicus Szene (Wahl nur für die Chronik)

| Flag | Gesetzt | Gelesen | Status | Wirkpunkt Akt 3 (Vorschlag) |
|---|---|---|---|---|
| `bl_minicu_duc_zuerst` | `taktik_eden_rise.py:373` über `kern/taktik.py:939` (`szene_waehlen`) | `tests/test_taktik.py:1759`, `tests/test_spieltest_live_contract.py:52` | Test | **(offen: Minicus Überleben)** Lebt Minicu: Bei seinem ersten Auftritt in Akt 3 sagt er zu Duc: *“You came first. Before Pascal. I heard you.”* Lebt er nicht oder ist das noch offen: Don erwähnt es am Grab oder in der Kirche, *“They say you knelt first, my son.”* In beiden Fällen kein Wert |
| `bl_minicu_gewartet` | `taktik_eden_rise.py:375` | – | nie | Bewusst ohne Wirkpunkt. Warten war in Ordnung. Höchstens die Chronik vermerkt es |
| `bl_minicu_sag_es` | `taktik_eden_rise.py:376` | – | nie | **Tag 26, Nonnas letzte Kiste:** In Pascals Brief steht ein Satz mehr: *“Duc told me to say it to him. So I did. It was the only true thing I said that night.”* Gilt unabhängig von Minicus Überleben. Pascal bleibt Verräter (Kanon), der Satz macht ihn nicht zum Helden |

### Bericht und Belege

| Flag | Gesetzt | Gelesen | Status | Wirkpunkt Akt 3 (Vorschlag) |
|---|---|---|---|---|
| `bl_blatt_gefunden` | `ereignisse_belagerung.py:346-347` (Bericht, Tag 23) | – | nie | **Zwei Wirkpunkte.** (1) **Tag 33, Alons Einladung:** Der Umschlag trägt Ducs Namen in derselben sorgfältigen Hand. Nur mit dem Blatt in der Tasche legt Duc beides nebeneinander, eine Zeile der Erzählerin. (2) **Ende mit Netz:** **(offen: Minicu)** Lebt er, gibt Duc ihm das Blatt zurück, bevor er seinen Namen ins Netz knotet. Sonst knotet Don das Blatt in das Netz, wortlos |
| `bl_werkstatt_heil` | `kern/taktik.py:1298-1299` (Welle 3, Werkstatt nicht verloren) | `ereignisse_belagerung.py:222, 232` (Aufbau-Pause, zwei Fassungen) | liest Akt 2 | **Wiederaufbau und Mechaniken:** Heile Werkstatt heißt: keine Baustelle, Petrus Boot fährt ab Tag 24. Angeln vom Fischerboot (die fünf Küstenbilder ohne Expedition) gibt es ab Tag 24 statt nach dem Aufbau. Das Ruder hängt wieder über der Tür, Petru: *“Hm. It's back where it belongs.”* |

### Was keine `bl_`-Flags sind, aber dazugehört

| Zustand | Wo | Liest Akt 3 heute? | Wirkpunkt Akt 3 (Vorschlag) |
|---|---|---|---|
| **Rettungen:** `z["taktik"]["haeuser"][id]["status"]` (`gerettet`, `brennt`, `verloren`) | `kern/taktik.py:1253, 1295` | indirekt: `tk_haus_weg_<id>` (`kern/taktik.py:1184`) liest `kern/aufbau.py` | **Tag 24, Abend:** Für jedes gerettete Haus eine kurze Dank-Szene des Besitzers (Post: Mina, Laden: Bà Tư, Bar: Alva, Werkstatt: Petru). Damit wird gutes Spiel in der Belagerung zu Zeitgewinn **und** zu einer Szene, nicht zu weniger Inhalt |
| **Notdürftig geflickt:** `tk_haus_geflickt_<id>` | `kern/belagerung.py` | ja, `kern/aufbau.py` (Baustelle beginnt bei Stufe 1) | gebaut, nichts zu tun |
| **Rudern:** `z["taktik"]["dorf_rudert"]` | `kern/taktik.py:92, 912, 1599` | nein | **Neues Flag vorschlagen:** `bl_dorf_rudert` am Ende von Welle 4 setzen. **Tag 35, Festa:** Die Boote von 1924 liegen geschmückt im Hafen. Petrus Aussage vor der Kommission nimmt es auf: *“The village rowed out. Like in 1924.”* Ohne Rudern: Minas *“They heard me. They just didn't open.”* kommt als Echo, wenn sie die Drohbriefe zustellt |
| **Kevin fliegt vom Tor:** `t["gesehen"]` enthält `kevin_fliegt` | `kern/taktik.py:1663` | nein | Kein Flag nötig, es passiert in jedem Durchlauf. Kanon-Bild für Akt 3: Kevin sitzt am Tor und wartet (Bericht). **(offen: Minicu)** Er sitzt dann wieder auf Minicus Kopf oder allein am Tor |
| **Yacht:** `tk_yacht_weg` | `kern/taktik.py:1186` | nein | **(offen: Yacht auf Grund)** Fassung A (auf Grund): Baustelle `yacht`, die Crew schläft bei den Familien der geretteten Häuser, Megans VIP-Kabine erst nach dem Heben. Fassung B (gesunken, heutiger Code): Crew im Dorf, Megan in Alvas Gästezimmer. Bis Duc entscheidet, baut Akt 3 nichts, was nur in einer Fassung funktioniert |
| `sophia_notizen` | `ereignisse_belagerung.py` (Funk, Sophia) | nein | **Tag 35, Kommission:** Sophias Lederbüchlein mit Uhrzeiten und Wörtern. Säule Wahrheit |
| `siri_wartet` | `ereignisse_belagerung.py:347` (Bericht) | nein (`siri_darf_posten` liest der Cliffhanger) | **Tag 24 bis 26:** Siri wartet auf Minicu. **(offen: Minicu)** Sobald sein Schicksal feststeht, fragt sie Duc noch einmal. Ihr Post kommt dann später, langsamer, und dreht die Lage langsam (Kanon: „Siris Post in eigenen Worten“) |

## Event-IDs (keine Flags, nur zur Vollständigkeit)

`bl_ab_<pid>`, `bl_ab_schon`, `bl_abend_s2`, `bl_abend_s3`, `bl_abend_wahl_21`, `bl_abend_wahl_22`, `bl_alva_flinte`, `bl_aufbau_asche`, `bl_aufbau_heil`, `bl_bar`, `bl_batu`, `bl_belagerung`, `bl_bericht`, `bl_echo_<pid>`, `bl_elsa_hilfe`, `bl_flicken_22`, `bl_flicken_23`, `bl_frist`, `bl_funk`, `bl_funk_nichts`, `bl_funk_rosi`, `bl_funk_rosi_charly`, `bl_funk_sophia`, `bl_kirche`, `bl_kirche_don_schlaeft`, `bl_kriegsrat`, `bl_leer`, `bl_letzte_nacht`, `bl_manoever`, `bl_minicu_jana`, `bl_minicu_kevin`, `bl_minicu_lola`, `bl_minicu_name`, `bl_morgen_22`, `bl_morgen_23`, `bl_na_<pid>`, `bl_nacht_s2`, `bl_nacht_s3`, `bl_nacht_wahl_20/21/22`, `bl_nachtwache`, `bl_rede`, `bl_tafel` (auch Flag), `bl_tueren`, `bl_wache_elsa`, `bl_wache_keiner`, `bl_wache_yamamoto`, `bl_wache_*_bericht`, `bl_welle_2` bis `bl_welle_6`.

## Zusammenfassung der Vorschläge nach Akt-3-Säule

| Akt-3-Säule | Flags, die einzahlen |
|---|---|
| **Wiederaufbau** | `bl_verband_wolff`, `bl_werkstatt_heil`, Rettungen, `tk_haus_geflickt_`, `bl_alva_runde` |
| **Zeugen und Kommission** | `bl_funk_white`, `bl_funk_charly`, `sophia_notizen`, `bl_nachtwache_*`, `bl_wache_gesehen`, `bl_batu_norden`, `bl_tueren_*`, Rudern |
| **Romanzen** | `bl_will_ab_<pid>`, `bl_ab_fertig_<pid>`, `bl_will_na_<pid>`, `bl_na_fertig_<pid>`, `bl_verband_chiara` |
| **Festa-Aufträge** | `bl_tueren_lola`, `bl_kirche_jana`, `bl_kirche_don`, `bl_kirche_casanova`, Rudern |
| **Leise Bögen** | `bl_nachtwache_niemand` (Holm), `bl_minicu_*` (offen), `bl_blatt_gefunden`, `bl_tafel` (Megan), `siri_wartet` |

Damit bekäme jedes Flag, das ein Spieler in der Belagerung bewusst setzt, in Akt 3 mindestens eine sichtbare Folge. Die Wahl bei Minicu (`bl_minicu_gewartet`) bleibt mit Absicht folgenlos.

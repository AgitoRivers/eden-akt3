# Akt 3 · Fragenliste an Duc

Stand 04.11.2026, ergänzt für Drehbuch v2 · Cloud-Sitzung `akt3-cloud`. Widersprüche und offene Punkte, die ich nicht selbst lösen darf. Zu jeder Frage steht mein Vorschlag; das Drehbuch (`docs/wiki/welt/drehbuch_akt3.md`) ist mit diesem Vorschlag geschrieben.

| Nr | Frage | Fundstellen | Vorschlag | Bei Nein |
|---|---|---|---|---|
| F-01 | **Die Yacht nach der Belagerung:** sinkt sie, sitzt sie auf Grund, oder bleibt sie? | Drehbuch Finale Abschnitt 9 Punkt 0, `tk_yacht_weg` | Auf Grund gesetzt, fünfte Baustelle mit Rosi und Petru, Crew schläft bis dahin bei den geretteten Familien | Die Yacht bleibt schwimmfähig, Baustelle entfällt |
| F-02 | **Elsa und Ajaccio:** Der Cliffhanger lässt Elsa in der Nacht von Tag 23 alles „straight to the commission“ schicken. `dorf_figuren.md` lässt sie sich früh in Akt 3 wundern, dass niemand ermittelt, und erst danach direkt melden | `ereignisse_cliffhanger.py` (`bl_cliff_netz`), `dorf_figuren.md` „Keine Polizei“ | Die Antwort am Morgen von Tag 25 setzt die Kommission auf Tag 35 und verrät nebenbei die „All quiet“-Berichte. Elsa fährt Tag 26 nach Ajaccio, Schublade Tag 27 | `dorf_figuren.md` gilt, der Cliffhanger-Satz wird geändert und neu vertont |
| F-03 | **Megans Rückkehrtag** | E-117 „Rückkehrtag offen“ | Tag 25 | ein anderer Tag, die Szene wandert mit |
| F-04 | **Alvas Applaus für Casanova:** `dorf_figuren.md` und `alva.md` sagen „nicht an die Festa gebunden“, Drehbuch Finale Abschnitt 8 sagt „Der große Applaus für sie bleibt der Festa“ | beide Seiten | Auf der Festa, weil das Drehbuch Finale jünger ist (02.11.) | Applaus nach `a3_berichte` an Tag 27 |
| F-05 | **Flag für die geborgene Margot:** Der Tauchgang ist nicht gebaut, ich finde kein Flag für „Margot geborgen“ | `ortskapitel_tauchgang.md`, `docs/uebergabe/story.md` | Ich lese ein neues Flag `margot_geborgen` und schreibe es in die Übergabe an die Tauchgang-Sitzung | anderer Name, den die Tauchgang-Sitzung festlegt |
| F-06 | **Riscossore vor der Kommission:** Kommt er immer oder nur, wenn Duc ihn an Tag 29 besucht? | `akt3.md` „Riscossores Buch“ | Er kommt immer (Kanon), der Besuch macht nur die Eco Tours und Ducs Wissen davon | Er kommt nur nach dem Besuch, dann ist Buenaventuras Aussage ohne Besuch wertlos |
| F-07 | **Der CEO der Eden Group:** Parkplatz sagt „CEO gehört zu Akt 3“. Kein Name, kein Gesicht im Kanon | `OFFEN.md` Parkplatz | Nur Stimme und schwarzer Bildschirm mit Logo, kein Name | Figur mit Namen, Stimme und Sprite (Bestellung) |
| F-08 | **Kommission als eigene Ansicht** (wie die Anhörung) oder als Event-Kette? | `systeme/anhoerung.md` | Erst Event-Kette, Ansicht nach deinem Spieltest | gleich als Ansicht, kostet etwa eine Sitzung mehr |
| F-09 | **Angeln:** Das Minispiel ist geparkt (E-079). Reicht der heutige Kreis für den Festa-Auftrag *The Catch*? | `systeme/kochen.md` | Ja, Akt 3 baut kein Minispiel | Minispiel kommt in Akt 3, eigene Sitzung |
| F-10 | **Stahl in Akt 3:** Stahl gibt es nur von Maschinen-Gegnern ab Tag 22, die Maschinen fehlen | `systeme/kochen.md` | Kurze Expedition „The Scrap Field“ (3 Frames, liegengebliebene Roboter in der Macchia) | Lights-Auftrag ohne Stahl, nur Iron |
| F-11 | **Ruf über Favours:** Die Zeugen und die Tafel könnten auch am Ruf hängen. Den Ruf füllen Favours, deren Inhalt ich nicht öffnen darf | CLAUDE.md „Grenzen“ | Ich lese nur den Wert `ruf`, nicht die Favours. Anschlussstelle: Säule Gemeinschaft nimmt Ruf ab 5 als Bonus | Ruf bleibt in Akt 3 außen vor |
| F-12 | **Handy in Akt 3:** Megans Anrufe, Siris Post und Yasins Angebot hätten im Handy ihren Platz. Die Handy-Ketten darf ich nicht anfassen | CLAUDE.md „Grenzen“ | Ich baue alles als normale Events. Anschlussstelle für die Handy-Sitzung: `a3_megan_landet`, `a3_megan_monaco`, Siris Post nach `siri_darf_posten` | Handy-Sitzung übernimmt diese drei |
| F-13 | **Siri und Yasin in Akt 3:** Yasin bekommt Geld für sein Video angeboten (Kanon). Ich habe dafür keine eigene Szene im Kalender | `belagerung.md` „Satelliten“ | Eine freie Szene `a3_yasin_angebot` ab Tag 26, Siri entscheidet mit, zählt auf Wahrheit | weglassen |
| F-14 | **Holms Mutter auf der Festa:** Kanon sagt, sie kommt. Kein Sprite, kein Name | `holm.md` | Nur erwähnt, im Festa-Bild eine Silhouette neben Holm | Figur mit Bild (Bestellung) |
| F-15 | **Pascals Name:** Alon dankt ihm „unter falschem Namen“. Ich schreibe „Paul? Paolo.“ | `dorf_figuren.md` „Das Rädchen“ | so | anderer Name |
| F-16 | **Kassenbuch, zwei Schritte:** Vorgemerkt an Tag 27, endgültig an Tag 35. Ist das zu viel Zögern? | `dorf_figuren.md` „Die Schublade“ | so lassen, damit der Spieler die Menschen im Buch erst kennt | nur an Tag 27, endgültig |

| F-17 | **Ereignis-Dichte in Akt 3:** Der Faktor 0,45 aus Akt 2 gilt ohne Ende weiter (`kern/ereignisse.AKT2_FAKTOR`) | `docs/berichte/wiki_vs_code.md` M5 | Woche 4 auf 0,6, Woche 5 bei 0,45 | überall 0,45 |
| F-18 | **Chiaras „Blackout in Akt 3“** (`figuren/chiara.md:43`): Was ist gemeint? | Figurenseite | Deutung im Drehbuch v2: Stromausfall auf der Brücke, sie muss Duc um Hilfe bitten. Character Design prüfen | andere Szene nach Kanon |
| F-19 | **Totòs Akt-3-Geheimnis** (`figuren/toto.md:8, :42`): Inhalt steht nur in den Fall-Daten | `story.json` (nicht geöffnet) | Story-Sitzung schreibt die Szene, Drehbuch v2 lässt ihr einen freien Platz in Woche 5 | – |
| F-20 | **`sandru_herkunft`** ist noch nicht gebaut (Woche 3, „Your Own Name“) | `dorf_figuren.md`, Ernste Events | Bedingung bleibt im Drehbuch, die Szene kommt mit Akt 3 nach | ersetzen durch Vertrauen Sandru 3 |
| F-21 | **Neues Flag `bl_dorf_rudert`** am Ende von Welle 4, damit Akt 3 das Rudern lesen kann | `kern/taktik.py` (`dorf_rudert` ist nur Zustand) | einbauen mit Paket A | Akt 3 liest `z["taktik"]["dorf_rudert"]` direkt |

## Anschlussstellen, die ich nicht öffne

- Favours und Handy (`ereignisse_favours.py`, `ereignisse_handy.py`, `handy_eden_rise.py`): F-11 und F-12. Ich lese dort nichts.
- Tauchgang: F-05, Whites Zeile an Buenaventura nach einem Fehlschlag (`story.md`).

# Bibis Tierstation „Mochi's“

Stand 01.11.2026 · Besitz: Hauptsitzung · Status: **gebaut auf Branch `mochis_station`**, Test und Gate laufen, von Duc noch nicht gespielt.
Quellen: [`../welt/nebenquest_red_trio.md`](../welt/nebenquest_red_trio.md), [`../figuren/bibi.md`](../figuren/bibi.md), Session [`../../brain_trust/BRAIN_TRUST_MOCHIS.md`](../../brain_trust/BRAIN_TRUST_MOCHIS.md).

## Idee (Duc 01.11.2026)

ARKs Halsbänder machen die Tiere verrückt. Solange ein Tier Kraft hat, gewinnt das Halsband gegen jedes Mittel. Duc muss es also im Kampf müde machen und dann Rosis **Schlafgranate** werfen. Danach schneidet Bibi das Halsband ab. Die Tiere bleiben bei ihr und werden aufgepäppelt, Duc kann sie besuchen. **Im Epilog werden alle freigelassen.** Das Halsband gibt es nur auf den Kampf-Sprites, an der Station zeigt jedes Tier sich ohne.

## Ablauf

| Schritt | Was passiert | Kostet |
|---|---|---|
| **Field Book** | Reiter im Laden „Mochi's“ (offen ab dem Tag nach der Quest, nur bei `mochis_offen`). Jedes Tier hat eine Karte, noch unbekannte als schwarzer Umriss | nichts |
| **Die Granate** | Pflicht-Event `mo_schlafgranate`: Bibi hat Rosi darum gebeten, Rosi hat sie gebaut | – |
| **Spur** | Ein kurzer Ausflug mit Bibi: Frame, Kampf, Ergebnis-Frame. Je Tier einmal am Tag | die ganze Phase |
| **Rettung** | Duc kämpft das Tier müde. Bibi gibt **2 Granaten je Spur**, Reste gehen zurück, kaufen kann man sie nicht | – |
| **Köder** | Lieblingsfutter aus der Speisekammer: Das Tier frisst erst und setzt die erste Runde aus | 1 Zutat |
| **Aufpäppeln** | Einmal füttern: Lieblingsfutter = gesund am nächsten Tag, Bibis Futter (15 €) = in zwei Tagen | keine Phase |
| **Besuchen** | Gesund: Knopf „Visit“ mit wechselnden Zeilen. Einmal am Tag +1 Bindung, der erste Besuch Vertrauen Bibi +2 und Ruf +1 | keine Phase |
| **Fund** | Einmal am Tag findet jedes gesunde Tier etwas (Rohstoff oder Zutat) | keine Phase |
| **Erster Fang** | Keine Szene mehr, Bibi meldet sich im Overlay: Tierbild, großer Name, Kommentar, Fun Fact, Dank. Vertrauen Bibi +2, Ruf +1 | – |
| **Zweiter Fang** | Neun Tiere gibt es ein zweites Mal: 4 Tage nach dem ersten Fang hat Bibi eine neue Spur (`mo_<tier>_wieder`). Danach eine Handy-Nachricht mit „hat Gesellschaft“ und dem zweiten Fun Fact | die ganze Phase |
| **Epilog** | Tag 35, Nachmittag: Bibi öffnet die Tore, siehe unten | – |

Nichts verfällt und kein Tier stirbt. Wer wegbleibt, verpasst nur Funde.

## Fang (Duc 01.11.2026)

Höchstens zwei Tiere je Art. **Allein bleiben** Madame (Juliens Schreibtischkatze), Duchess (die einzige mit Platten), Sunday („Nothing runs with this one“), Rusty („There are no red pandas on Corsica. There is one now“) und Ghost. Bei ihnen kommt keine zweite Spur, der zweite Fun Fact kommt mit dem ersten Besuch.

Alle anderen neun haben einen zweiten Fang: +1 Halsband, Ruf +1 und morgens ein Fund mehr aus dem Gehege. Das volle Buch (`mo_buch_voll`) zählt nur den ersten Fang, der zweite ist nie Pflicht. Texte: `FANG` in `mochis_daten.py`, alle Fun Facts sind echte Tierkunde. Die alten Szenentexte stehen als `szene` im Field Book.

## Field Book: das Sammelbuch

Ein Baustein an zwei Orten (`client/plugins/eden-mochis/`): im Laden mit den Knöpfen, im Codex nur zum Lesen. Links die Sammlung als Fotos (unbekannt = schwarzer Umriss, offene Spur = Schatten mit Marke), rechts die Seite des Tiers mit Foto, Stempel und Zetteln in Schrift und Linierung der Anhörung. Noch fehlende Fakten stehen als gestrichelter leerer Zettel da.

## Schlafgranate im Kampf

Eigener Zustand `schlaf`: blaue Wolke statt Knall (`wolke` in `eden-combat-effects.js`), eigener Klang `kampf_granate_schlaf` (lokal erzeugt mit `werkzeuge/eden_rise/schlaf_klang.py`, Abnahme `docs/abnahme/schlaf_klang.json`).

Nach jedem Kampf kommt die Ergebniskarte erst nach einer Pause: 1,5 s, nach einer Granate länger, nach der Schlafgranate etwa 5 s. Klick oder Taste überspringt. Gilt für alle Kämpfe.

## Epilog: Die Tore

Pflicht-Event `mo_frei_start` an Tag 35, Bedingung `mo_tier_da` (mindestens ein Tier gerettet). Der Kalender endet noch an Tag 21, das Event ist also erst mit Akt 3 erreichbar. Akt 3 darf den Zeitpunkt schieben, die Festa bleibt die Schlussszene.

| Beat | Was passiert |
|---|---|
| Ansage | Bibi am ersten Tor, Danzel hat sich dafür angezogen. Sie fragt: „Will you stay for it?“ |
| Je Tier | Ein Frame `mo_frei_<tier>` nur für gerettete Tiere (`mo_tier_<tier>`): Bild ohne Halsband, `text_frei`, Bibis letztes Wiegen als Antwort auf das Gewicht aus dem Field Book (`ABSCHIED` in `mochis_daten.py`) |
| Schluss | `mo_frei_ende`: Volles Buch oder „there are still some out there“, dazu Mochi je nach `kl_loewe_frei`. Setzt `mo_freigelassen` |

## Kommission

Pflicht-Event `mo_kommission` an Tag 35, Bedingung `mo_ark_beweis`. Die Kommission sieht die Schachtel. `kern/mochis.beweis_stand` sagt, was sie wert ist, und die Anklage in Akt 3 liest genau das:

| Stand | Wann | Bedeutung |
|---|---|---|
| `keiner` | Kein `mo_ark_beweis` | Keine Szene, die Halsbänder fehlen der Anklage |
| `fraglich` | Duc sagte „Only us“ | Elsa hat sie im Rathaus erfasst, das Siegel kam gebrochen zurück. Die Nummern stehen, Anwälte greifen sie an |
| `sicher` | Duc sagte „Keep them away from the town hall“ | Elsas Safe, Siegel heil |

Die Anklage selbst und die übrige Kommission sind Akt 3 und noch nicht gebaut.

## Bibis Häuschen (Duc 02.11.2026)

Bibi wohnt an der Station in einem kleinen, einfachen, gemütlichen Häuschen neben dem Pferch. Das halbe Dach gehört zum Pferch der Tiere, nicht zu ihrem Zuhause. Ihr Häuschen ist auch ihr Ort für Zweisamkeit (`kern/orte.py`). Bildbeschreibung und alle anderen Zimmer: [`../welt/wohnen.md`](../welt/wohnen.md).

## Bild der Station

`kern/mochis.bild`: Anfangsbild `eden_rise_mochis_station.png`, ab 5 geretteten Tieren der Ausbau `eden_rise_mochis_station_voll.png` (`AUSBAU_AB`). Gilt für den Laden und die Karte.

## Schlafgranate: Balance

`kern/kampf.schlaf_chance`. Die Chance steht im Kampf neben der Granate, der Spieler sieht sie also vor dem Wurf.

- Bis 10 % LP: immer, bei jedem Tier.
- Darüber: `((1 − LP-Anteil) / 0,9)² × schlaf_faktor`, mindestens 5 %.
- Ein Schlag, der das Tier umhauen würde, lässt es einmal auf 5 % LP stehen („One more hit, and it's gone“). So gibt es immer ein Fenster für die sichere Granate. Der zweite solche Schlag = es ist weg, neuer Versuch am nächsten Tag. Feuer und Blutung allein verjagen es nie, sie stoppen bei 1 LP.

| LP | Faktor 1,0 (Hund) | 0,8 (Mufflon, Affe) | 0,7 (Wolf) |
|---|---|---|---|
| 10 % | 100 % | 100 % | 100 % |
| 20 % | 79 % | 63 % | 55 % |
| 30 % | 60 % | 48 % | 42 % |
| 50 % | 31 % | 25 % | 22 % |
| 70 % | 11 % | 9 % | 8 % |
| 90 % und mehr | 5 % | 5 % | 5 % |

Die Tabelle ist gerechnet, nicht gespielt. Hyäne: Faktor 0,9. Offen ist, wie lange die Kämpfe dauern und ob Duc sie mit normaler Ausrüstung übersteht.

## Die Tiere

14 Tiere mit Spur, 3 Seiten ohne Spur (Duc 01.11.2026). Nur ARK-Tiere und Tiere aus der Anlage: Wer aus eigener Aggressivität angreift (Ratte, Schlange, Flughunde, Möwe, verwilderte Hunde), gehört nicht in die Station. Biscuit ist die Ausnahme: ein Streuner, an dem ARK getestet hat. Die Spuren laufen bis Tag 35.

| Name | Art | Spur ab Quest-Ende | Granate (Faktor) | Begleiter tut | Liebt |
|---|---|---|---|---|---|
| Biscuit | Stray Dog | +2 | 1,0 | beißt, 6 % | Eier, Huhn |
| Madame | Russian Blue, Juliens Schreibtischkatze | +3 | 1,0 | fällt drauf, 6 % | Lachs, Huhn |
| Sorry | Ark Hyena | +4 | 0,9 | reißt, 5 % + Bluten | Schwein, Rind |
| Duchess | Plated Mouflon | +5 | 0,8 | halbiert den nächsten Treffer | Kohl, Wildkräuter |
| Monsieur | Collared Ape | +6 | 0,8 | Stein, 10 % | Zucchini, Tomaten, Kartoffeln |
| Sunday | Collared Wolf | +7 | 0,7 | von der Seite, 8 % + Bluten | Rind, Lachs, Schwein |
| Rusty | Red Panda, privater Zoo | +8 | 1,0 | halbiert den nächsten Treffer | Wildkräuter, Eier |
| Monday | Capybara | +9 | 1,0 | läuft durch, 8 % | Kohl, Zucchini, Wildkräuter |
| Truffle | Wild Boar, Bruder des Alpha-Keilers | +10 | 0,9 | Stoß, 10 % | Kartoffeln, Zucchini, Eier |
| Pudding | Bear Cub, Old Greys Kleinstes (nach `bg_u1_fertig`) | +11 | 1,0 | Tatze, 5 % | Lachs, Eier, Kartoffeln |
| Twelve | Hermann's Tortoise, Nummer 12 von 40 | +12 | 0,8 | hält fest, 7 % + Bluten | Tomaten, Kohl, Zucchini |
| Bones | Bearded Vulture | +13 | 0,8 | Stein von oben, 12 % | Schwein, Rind, Huhn |
| Ghost | Snow Leopard, privater Zoo | +15 | 0,7 | aus dem Nichts, 11 % + Bluten | Rind, Lachs, Schwein |
| Mr. V. | Komodo Dragon. Charly nannte ihn so, nach Alon | +17 | 0,7 | Biss, 6 % + Bluten | Rind, Schwein, Lachs |

**Seiten ohne Spur:** Mochi kommt von selbst oder gar nicht ([`../welt/belagerung.md`](../welt/belagerung.md)). Old Grey (`bg_baer_frei` oder `bg_baer_getoetet`) und der Black Beast (`bg_panther_erloest` oder `bg_panther_gehetzt`) haben ihr Ende schon in den Bergen. Ihre Seite erscheint erst danach. Capra bleibt Ducs Begleiterin und ist nicht in der Station.

**Neu im Kanon, noch Entwurf:** Madame gehörte Julien Vasseur. Tiere aus dem privaten Zoo kamen als Geschenk an die Anlage. Jede Figur hier mit Namen und Text ist neu.

## Begleiter

Genau einer, nur auf Expeditionen, nicht in Kämpfen, die schon eigenen Beistand haben. Bindung: Stufe 1 handelt jede 3. Runde, Stufe 2 (ab 3 Punkten) jede 2., Stufe 3 (ab 8) jede Runde. Punkte gibt es für gemeinsame Kämpfe und einmal am Tag für den Besuch. Wer mitkommt, sucht an dem Tag nichts.

## Wirkpunkte

- **Ruf und Vertrauen Bibi:** Rettung, erster Besuch, volles Buch (`mo_buch_voll` bei allen geretteten Tieren, Vertrauen +6). Alle Punkte mit `frei=False`, der Stufen-Abstand von 7 Tagen gilt also.
- **Halsbänder:** Bei 3 Halsbändern `mo_halsband_3`, Pflicht-Event `mo_halsbaender` mit Elsa. Danach `mo_ark_beweis`, bei der zweiten Antwort zusätzlich `mo_beweis_bei_elsa`.
- **Farm und Angeln:** Lieblingsfutter kommt aus der Speisekammer, Funde füllen Rohstoffe und Vorrat.
- **Merker für später, nicht gebaut:** `mo_beweis_bei_elsa` gegen Pascals Schublade, gerettete Tiere als Belagerungs-Aufgabe, Bibis Romanze (`mo_buch_voll` als möglicher Einstieg).

## Bibis Arc (Duc 02.11.2026)

Die Arbeit und die Romanze hängen an der Station, `werkzeuge/eden_rise/ereignisse_bibi.py`, Test `tests/test_bibi_arc.py`.

- **Vier Arbeits-Events** (`mo_a_*`, Pflicht, ohne Phase, nur Vertrauen): The Fence, Half a Roof, Bath Day (ab dem ersten Tier), The Spanner (mit dem Affen). Kosenamen nur auf dem Romanzen-Weg, sonst „Clipboard“.
- **Selfie je Tier (Duc 02.11.2026):** eine Mini-Szene aus zwei Polaroids, A und dann B, wholesome mit Witz. Bilder `/selfie/bibi_fang_<tier>_<a|b>.webp` (Wahl in `werkzeuge/bibi_fang_webp.py`, erzeugt mit `karten_neu/bibi_tier_selfies_4.py` bis `_8.py`, Preset `Bibi_Selfie`). Je Bild ein Polaroid-Titel in Bibis Handschrift (`selfie_titel`), darunter ihre Nachricht (`selfie`) und ihre Notiz im Field Book (`log`), alles in `mochis_daten.py`. Zu sehen im Field Book und im Overlay nach dem Fang (`kern/mochis._selfie`). Fehlt ein Bild, fällt nur dieses Polaroid weg. Test `tests/test_mochis.py::test_selfie_szene`.
- **Ducs Seite:** Ab Begehren 4 ein namenloser Umriss am Ende der Sammlung, nach `rm_b4` die ganze Seite (`modul.mochis.duc_seite`). Zählt nicht als Tier.
- **Zweiter Fang:** eigener Satz je Tier statt „Same collar, same light“.

## Dateien

`kern/mochis.py` (Regeln) · `kern/kampf.py` (`schlaf_chance`, Taumeln in `_ausscheiden`) · `werkzeuge/eden_rise/mochis_daten.py` (Tiere) · `kaempfe_mochis.py` (Rettungen) · `ereignisse_mochis.py` (Szenen) · `client/plugins/eden-mochis/` (Field Book) · `karten_neu/kampf_tierstation.py` (Sprites) · `tests/test_mochis.py` (noch nie gelaufen).

## Gemessen

`tests/mochis_sim.py` (01.11.2026, Level 6, je Tier 5 Kämpfe): Gerettet werden 80–100 % bei allen Spielertypen, einzelne Ausreißer nach unten bis 40 % (Bot-Würfel), meist in 3–6 Zügen. Niederlagen fast keine, Bibis Warnungen beim Wolf und Waran sind also stärker als der Kampf.

## Offen

1. Duc spielt die Station.
2. Epilog und Kommission erreichen: Der Kalender endet noch an Tag 21. Beide warten auf Akt 3.
3. Schwierigkeit der starken Tiere nach Ducs Spieltest.

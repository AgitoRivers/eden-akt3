# Gegenrede zum Drehbuch Akt 3

Stand 04.11.2026 · Cloud-Sitzung, Branch `drehbuch-gegenrede` · Geprüft: `docs/wiki/welt/drehbuch_akt3.md` auf `origin/akt3-cloud`, Commit `506dce2`. **Die Datei ist nicht geändert.**

**Offen gesagt:** Das Drehbuch auf `akt3-cloud` stammt aus dieser Sitzung selbst. Bevor die Anweisung kam, dort nicht zu schreiben, hatte ich es angelegt. Damit die Gegenrede nicht meine eigene Sicht bestätigt, hat ein unabhängiger Prüfer das Drehbuch ohne meine Begründungen gegen das Wiki und den Code gelesen. Seine Funde habe ich stichprobenweise nachgeprüft und hier mit eigenen ergänzt. „D123“ heißt Zeile 123 im Drehbuch (`git show origin/akt3-cloud:docs/wiki/welt/drehbuch_akt3.md`).

## Was trägt (und bleiben soll)

Die stärkste Idee ist die Kette **Baustelle → Tür → Aussage** (D120): Der Wiederaufbau aus Woche 4 entscheidet, wer in Woche 5 aussagen kann. Damit hängt Ducs Kernvorgabe „das Dorf wieder aufbauen“ zum ersten Mal mechanisch am Ende. Die Zeugen-Tabelle (D139 bis D149) gibt jeder Dorf-Figur eine eigene Angst und eine eigene Frage. Bà Tư, Petru und Riscossore (*“Here. Your first dividend.”*) klingen nach ihren Seiten. Die Echos aus der Belagerung (Minicu am Tor, Alvas Fehlschuss, der tropfende Eimer) tragen. Die Fragenliste trennt Vorschlag und Kanon sauber.

## Prüfsteine im Überblick

| Prüfstein | Urteil | Kern |
|---|---|---|
| Spielerreise | teilweise | Woche 4 ist voller als Woche 5, das Durchatmen fehlt (G4) |
| Sehnsucht | gut | Wirksamkeit (Baustelle → Zeuge) stark, Romanzen schwach (G12) |
| Vorbild | gut | Stardew, Mass Effect 2, aber das eigene Gegenvorbild L.A. Noire wird bei den Zeugen-Chips verletzt (G9) |
| Zeitbudget | **falsch gerechnet** | Frühstück und Nacht als frei gezählt (G5) |
| Kanon | **mehrere Brüche** | Sonnenbrille, Stream, Wochentage, Petru am Tor, Alva „drei Tage“ (G1 bis G3, G6 bis G8) |
| Ton | knapp | drei ernste Gipfel statt eines schweren Moments (G13), „frech“ bei 15 % statt rund 25 % |
| Wirkpunkt | teilweise | Post-Belohnung wirkungslos (G10), viele Akt-2-Flags ungenutzt (G11) |
| Selbstkritik | zu zahm | die Brain-Trust-Runde im Drehbuch widerspricht dem Kern nirgends (G16) |
| Beleg | fehlt | kein Bot-Lauf, keine Zahl zum Zeitbudget |
| Doppelung | ja | Applaus-Stille dreimal, Dons Glocke und Kaffee doppelt (G14) |

## Gegenrede, nach Gewicht

| # | Gewicht | Kritik | Beleg | Gegenvorschlag |
|---|---|---|---|---|
| G1 | hoch | **Duc nimmt dreimal die Sonnenbrille ab** | D190, D275, D567 · `figuren/duc.md:47` („bleibt immer auf der Nase, in jedem Bild“), CLAUDE.md feste Vorgabe | Ernst über Haltung: *Puts the coffee down. Looks at each of them.* · bei Megan: *Doesn't joke this time. “Mac. I'd never sell them.”* |
| G2 | hoch | **Das Rädchen ist privat**, Kanon will es vor laufendem Stream | D557, D564 · `welt/dorf_figuren.md:183` („vor laufendem Stream unter falschem Namen“) | Dinner bleibt ohne Kamera (Alon privat ruhig). Danach ein kurzer Pressemoment auf der Terrasse, Drohnenkamera: dort gibt er den Großsprecher und sagt *“Paul? Paolo.”* So zeigt die Szene beide Alons |
| G3 | hoch | **Die Kommission widerspricht einem gebauten Event** | D597 bis D610 (Kirche, drei Beamte, Kommissarin) · `ereignisse_mochis.py:182-185` (`mo_kommission`, Tag 35 „tag“, am Kai, „Two men from the commission“), `kern/mochis.beweis_stand` | Ort und Besetzung angleichen: Kai mit Klapptisch, zwei Männer und ein Schreiber. `mo_kommission` wird ein Beat in `a3_kommission`, `beweis_stand()` zählt in die Säule Wahrheit |
| G4 | hoch | **Woche 4 hat mehr Pflicht als Woche 5** | D66 bis D70: zwölf Pflicht-Events an Tag 24 bis 28, Woche 5 bis Tag 33 nur sieben · `welt/akt3.md:18` („Woche 4 gehört dem Durchatmen“) | `a3_uhr` und `a3_briefe` zu einer Szene. Höchstens zwei Pflicht-Events je Tag in Woche 4, ein ganz freier Tag (Vorschlag Tag 27 ohne Pflicht, Schublade auf Tag 28 morgens) |
| G5 | hoch | **Zeitbudget falsch gezählt** | D72 („15 von 24“), D86, D97 · `welt/akt2_kalender.md:49` („4 freie Phasen: Tag, Nachmittag, Dinner, Abend“) | Neu zählen nur mit den vier Kartenphasen: Es bleiben rund 26 bis 29, der Bedarf liegt bei 23 bis 33 plus Dates. Vor dem Bau einen Bot-Lauf (`tests/spieltest_kalender.py`) mit Akt-3-Kalender |
| G6 | mittel | **Wochentage falsch** | D33 bis D44, D64 bis D70 (Tag 24 = Mo, Tag 28 = So) · Tag 14 ist Sonntag (`ereignisse_dorf.py`, Messe Tag 14), also Tag 21, 28, 35 Sonntag | Tag 24 = Mittwoch. Tag 24 bis 27 Mi bis Sa |
| G7 | hoch | **Petru „war am Tor“** | D191 · `welt/dorf_figuren.md:318` (Minicu am Haupttor „statt Petru“), `welt/belagerung.md:158` (Petru rudert mit Mina und Lea) | Petru: *“Hm. I rowed out with Mina while he carried water to the church. Three days. That's all I need to know.”* (Rückbezug mit Erinnerung) |
| G8 | hoch | **Alva „drei Tage“ bewusstlos und zweimal „zum ersten Mal“ im Haus ihrer Mutter** | D225 („Three days“), D219 (wacht im A.V. Market auf) gegen D465 („not stepped into this house in six years“) · Alva fällt erst in Welle 6 (`drehbuch_finale.md`, Welle 6), das Betreten gehört zu Switched Off (`dorf_figuren.md`, Ernste Events 5) | Sandru: *“Since last night. You missed the end.”* Bei abgebrannter Bar wacht sie bei Bà Tư auf, nie im Market |
| G9 | hoch | **Zeugen-Chips sind Rätselraten** | D134 (ein Chip trifft, „Wissen steckt in der Figurenseite“), D128 nennt selbst L.A. Noire als Gegenvorbild | Der richtige Chip stützt sich auf einen **sichtbaren** Moment und trägt die Erinnerung im Satz. Ein falscher Chip führt nicht ins Schweigen, sondern zu einer kleinen Tat (*“Show me”*), die Vertrauen beweist. Endgültiges Schweigen nur bei geschlossener Tür |
| G10 | hoch | **Festa-Tafel ist halb Einkaufsliste**, Post-Belohnung wirkungslos | D164 bis D169 („Twelve fish“, „10 Gemüse“, „8 Timber + 4 Slate“), D156 (eigenes Gegenvorbild „10 Holz, 5 Stein“) · D115 gegen D159 (Abgabe ist ohnehin frei) | Jeder Auftrag wird **eine Szene mit einer Entscheidung**, Mengen halbieren: *The Catch* = eine Ausfahrt mit Petru, Duc wählt den Platz, Petru urteilt. *The Stage* = Bau mit Minicu, Duc entscheidet, für wen die Bühne zuerst ist. Die Post bekommt eine echte Wirkung: Mina bringt einmal am Tag eine Zutat oder ein Material aus Bastia |
| G11 | mittel | **Akt-2-Flags ungenutzt** | `bl_nachtwache_*`, `bl_funk_white`, `bl_funk_charly`, `bl_tueren_*`, `bl_batu_norden`, `bl_kirche_jana`, `bl_kirche_don`, `bl_blatt_gefunden`, `siri_wartet`, `bl_alva_runde`, `tk_haus_geflickt_*`, `gr_8_riscossore`, `sirene_weg`, Totòs Versprechen `alon_kiste_genutzt` (`ereignisse_grotte.py:514`) | Vollständige Wirkpunkt-Liste in `docs/wiki/welt/akt3_folgen_belagerung.md` (Branch `folgen-belagerung`). Wichtigste drei: Nachtwache und Funk als Beweise, Bà Tưs Tür an `bl_batu_norden`, die Kiste aus der Grotte als Beweis mit Totòs Zeile |
| G12 | hoch | **„Romanzen fertig spielen“ fehlt fast** | D95 rechnet je Frau eine Szene ein, das Drehbuch enthält keine · Kanon: Chiaras „Blackout“ (`figuren/chiara.md:43`), Romanzen auf Expeditionen (`brain_trust/OFFEN.md`, Parkplatz) | Eigener Abschnitt „Romanzen Akt 3“: je Frau eine Schluss-Szene an ihrer Leiter, vor Tag 32 platziert, ein Teil davon als Expedition mit Rastplatz-Szene. Hebt auch den Anteil „frech“ |
| G13 | mittel | **Drei schwere Gipfel statt eines** | D56, D677 (Schublade, Switched Off, Villa) · `BRAIN_TRUST_PROMPT.md` („höchstens ein schwerer Moment pro Akt“), `dorf_figuren.md` („Schublade und Nonna kurz und leise“) | Schublade auf Spannung 4, ein leiser Fund. Villa ist Spannung und Aktion, nicht Schwere. Switched Off bleibt allein |
| G14 | mittel | **Doppelungen** | Applaus-Stille D315, D623 und im Bericht Tag 23 · Dons Glocke schon in der Belagerung eingelöst, Kaffee wiederholt `bl_kirche_don` | An Tag 26 klatscht Minicu, zu laut und allein (bricht das Muster, warm). *The Bell* wird ein Auftrag mit Plan (Don eine Woche lang abends zu den Karten holen) |
| G15 | mittel | **Kleine Kanon- und Logikbrüche** | Schwestern-Regel D516 („Sophia oder Rosi“, richtig: Lea oder Sophia) · „tomorrow“ an Tag 33 (D521, D525, D526) · Nonna versteht vor Dons Szene (D351 gegen `dorf_figuren.md`) · Elsa plant mit, obwohl sie vom Schlüssel nichts wissen darf (D536 bis D538, D578) · Casanova betritt das Elternhaus an Tag 34, das ist das Schlussbild von ★ (D548, `enden.md`) · Rosi gefeuert: Sandrus Weg fehlt (Kanon: Maxwell hört, Rosi hilft aus der Ferne) · Don „sober“ auch ohne `bl_kirche_don` (D146, D603) | Je ein Satz: „Lea oder Sophia, nie beide“ · „at the festa“ statt „tomorrow“ · Don zuerst, Nonna öffnet die Kiste erst danach · Elsa fehlt bei der Planung, Festnahme draußen an der Mole · Casanova bleibt an der Kellertür: *“It's smaller than I remember. …Go. I'll wait here.”* · zweite Fassung `a3_schiene` mit Maxwell · Don ohne Flag: *“I was asleep on the steps, my son. Write that down too.”* |
| G16 | mittel | **Siris Post fehlt** | nur als Flag in D606 · `enden.md` (Siris #StrandedInParadise ist ein Weg zu Wahrheit, nach der Belagerung), `belagerung.md` („Siris Post in eigenen Worten“) | Freie Szene `a3_siri_post` ab Tag 25, mit Yasins Geldangebot verknüpft (F-13). Siri postet in eigenen Worten, mit dem Pullover ihres Vaters, ohne Filter |
| G17 | mittel | **Säule Geld zirkulär** | D497 und D638: Megans Erfolg hängt an der Säule, die er tragen soll | Megans Erfolg hängt an dem, was Duc bringt (ab 4 Zeugen oder 2 Beweisen). Der CEO ist Kanon-Fan von Duc (`figuren/nebenfiguren.md`): *“Is Duc there? Put him on.”* |
| G18 | niedrig | **Englisch** | „phones home“ (D480), „dividend“ (D438), „in breach of service agreement“ (D463), „the one who knocks“ (D142, bekanntes Zitat), Erzähltext im Präteritum (D187, STIL verlangt Präsens) | „the part that talks to his computers“ · „Your first payment“ · „User broke the rules of service.“ · „the one at the door with bad news“ · Präsens |
| G19 | niedrig | **Chips ohne klare Frage vorher** | D422 (Buenaventura), D451 (Holm und Petru), D539 (Kellerbegleitung), D592 (Lolas Tassen) | z. B. Holm: *“Who goes down with you, Frankfurt?”* |

## Verbesserungsrunde

**Sienna (Game Direction):** Die Kette Baustelle, Tür, Aussage ist Game-of-the-Year-Material, weil sie Woche 4 und Woche 5 verbindet, und genau deshalb darf sie nicht an einer Einkaufsliste scheitern. ✨ Gegenvorbild Mass Effect 3: Die „War Assets“ waren eine Zahl, die niemand fühlte. Mein Vorschlag: Jede fertige Baustelle zeigt ihren Zeugen sofort im Bild, er steht vor seinem Haus und sagt einen Satz. Dann sieht der Spieler, was er gebaut hat, bevor die Kommission kommt.

**Aly (Tech):** Die drei gebauten Akt-3-Haken müssen zuerst passen: `mo_kommission` (Tag 35, Kai), `mo_frei_start` und Totòs `alon_kiste_genutzt` mit 14 Tagen Frist, die bei frühem Versprechen schon vor Tag 35 abläuft. 🤓 Bevor eine Zeile gebaut wird, ein Bot-Lauf über den Akt-3-Kalender mit vier Kartenphasen je Tag. Ich wette, das Budget reißt bei Spielern mit Romanze und allen Zeugen um sechs bis acht Phasen. Gegenvorschlag: Zeugen-Gespräche ohne Phase, wenn das Haus fertig ist (dann ist der Besuch Teil der Dank-Szene).

**Luise (Art & Story):** Der tropfende Eimer bleibt mein Lieblingsbild. 🥹 Kritik: Die Sonnenbrille. Duc nimmt sie in drei großen Momenten ab, und damit bricht genau das Bild, das Kult werden soll. Gegenvorschlag: In den drei Momenten schiebt er sie nicht hoch, er setzt sich hin. Nähe durch Höhe, nicht durch Augen. Und Pascal in der Villa braucht keine Geste, die nicht gesät ist. Lieber ein leerer Haken in seinem Zimmer, ein heller Rand an der Wand, wo der Fedora hing.

**Maelle (Producerin):** Preis der Korrekturen: etwa eine halbe Sitzung Drehbuch, keine neuen Bilder. Was wegfällt: drei Pflicht-Events in Woche 4, die halbe Festa-Tafel als Mengenliste. 📋 Was dazukommt: ein Romanzen-Abschnitt (sieben Szenen, grob 120 Zeilen) und `a3_siri_post`. Meine Frage an dich, Duc: Sollen die Romanzen-Schlüsse in Woche 4 liegen (damit sie Durchatmen sind) oder in Woche 5 (damit sie vor der Villa zählen)?

**Sora (Spielerstimme / QA):** Minute 1: Das Dorf dreht sich weg, Petru tritt vor, gut. Minute 30: Ich habe drei Pflicht-Szenen am Stück und will eigentlich zu Alva. 😤 Minute 90: Ich rate bei Bà Tư den falschen Chip und sie schweigt für immer. Nochmal-Lust 3 statt 5. Veto bei der Tafel: „Twelve fish, three kinds“ ist Excel. 😂 Gegenvorschlag: Jeder Auftrag ist ein Date mit dem Dorf, und die Romanzen-Schlüsse bekommen ihr Knistern zurück: Die Frau, die Duc zur Festa einlädt, steht in Nacht 34 mit eigener erster Zeile oben, und ein Nein bricht nichts. 🔥

**Übernommen in die Empfehlung an Duc:**
1. Sonnenbrille bleibt auf (G1), Haltung statt Augen.
2. Kalender: Wochentage korrigieren (G6), Woche 4 auf höchstens zwei Pflicht-Events je Tag (G4), Zeitbudget mit Bot-Lauf (G5).
3. Kommission an das gebaute `mo_kommission` anpassen (G3), Rädchen vor der Kamera (G2).
4. Zeugen ohne Rätselchip (G9), Tafel als Szenen mit Entscheidung (G10).
5. Romanzen-Abschnitt und Siris Post (G12, G16).

## Für die Fragenliste (`akt3_fragen.md`) nachzutragen

- Was wusste Duc über den Verkauf? Das Drehbuch sagt es dreimal verschieden (D190, D275, D378).
- Petrus Platz an Tag 23 (G7).
- Ort der Kommission gegenüber `mo_kommission` (G3).
- Stream oder privat beim Rädchen (G2).
- `megan_funke_3` und `sandru_herkunft` existieren im Code noch nicht (D530, D145).
- Alvas Aussage über ihr Ziel an der Barrikade darf Pascal in keinen Fall ziehen (Auflage der Story-Sitzung, `dorf_figuren.md`, „Regeln für die Spuren“).
- Die Beweisliste vor der Kommission darf nichts über die Yacht von Tag 0 enthalten (`dorf_figuren.md`, „Die Antwort aus Ajaccio“).

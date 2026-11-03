# Eden Rise · Auftrag Akt 3 (Cloud-Sitzung)

Du arbeitest in einem **schlanken Auszug** des Eden-Repos: nur Code, Wiki und Textdaten, **ohne Bilder, Ton, Sprites und Spielstände**. Duc (der Besitzer, ESG-Berater und Spielfigur im Spiel) spricht Deutsch mit dir. **Alles, was der Spieler sieht oder hört, schreibst du auf Englisch.** Code, Bezeichner und Kommentare ebenfalls Englisch.

## Der Auftrag

Plane, schreibe und baue **den gesamten Akt 3** (Tag 24–35): Story, Events, Missionen, Szenen, alle gesprochenen Zeilen samt Sprecher-Tags und die technische Umsetzung im Modul `module/eden_rise`. Arbeite auf dem Branch `akt3-cloud`, nie auf `master`. Committe in kleinen, benannten Schritten.

## Erst lesen (in dieser Reihenfolge)

1. `docs/wiki/START.md`, dann **`docs/wiki/STIL.md` (Pflicht vor jedem Text)**.
2. `docs/wiki/welt/akt3.md`, `enden.md`, `dorf_figuren.md`, `akt2_kalender.md`, `belagerung.md`, `drehbuch_finale.md`, `ortskapitel_tauchgang.md`, `orte.md`.
3. Die Figurenseiten unter `docs/wiki/figuren/` (mindestens Abschnitt „Stimme“, bevor eine Figur spricht).
4. `docs/uebergabe/*.md` (Stand aller Bereiche), `docs/brain_trust/LEHREN.md`, `OFFEN.md`, `ENTSCHEIDUNGEN.md`, `docs/STAND.md`.
5. Die Bau-Muster: `werkzeuge/eden_rise/ereignisse_cliffhanger.py`, `ereignisse_belagerung_nacht.py`, `ereignisse_basis.py` (Zusammenbau der Events), `kern/` (Regeln im Code).

Wo Wiki und alte Dokumente sich widersprechen, **gilt das Wiki**. Widersprüche, die du nicht lösen kannst, schreibst du in eine Fragenliste (`docs/uebergabe/akt3_fragen.md`), statt zu raten.

## Feste Vorgaben (Duc, nicht verhandeln)

- **Kalender:** Das Spiel hat fünf Wochen. Akt 3 = Tag 24–35 (Woche 4 kürzer). Die Belagerung endet an Tag 23. Tag 35 ist die Kommission, die Festa ist die Schlussszene.
- **Grundton:** Akt 3 ist zum **Durchatmen**: das Dorf wieder aufbauen (der Kern), Romanzen fertig spielen, Mechaniken meistern (Angeln, Auffangstation, Kochen …), die Festa vorbereiten (Casanova vergibt Aufträge). Wenige, ernste Missionen. Woche 4 atmet, Woche 5 zieht an: Villa mit Alons Angebot an Tag 34, Kommission an Tag 35, dann die Festa.
- **Enden:** zehn Enden, Gerüst steht in `enden.md`. Alons letztes Angebot: *“Join me. Name your price.”* Pascal ist in jedem Ende zu sehen. Feinschliff der Enden macht Duc ganz am Ende.
- **Buenaventura / Eco Tours, Wiederaufbau, Fischernetz, Riscossores Buch:** alles in `akt3.md` festgelegt. Baue danach, ändere es nicht.
- **Alon:** hochintelligent, spielt den Großsprecher nur vor der Presse, keine echte Person nachahmen. Er bedroht das Dorf mit Jobs, Krediten und Anwaltsbriefen, nie mit Gewalt.
- **Megan** fehlt ab Tag 20 abends und kommt in Akt 3 zurück, wenn der Satellit nicht mehr arbeitet (Tag offen: schlage einen vor).
- **Dein Spieler ist Duc:** ESG-Berater, Gründer von Eden Consulting, **trägt immer die Sonnenbrille**, nie „Tüftler“. Seine ESG-Arbeit hat nichts mit dem Resort zu tun.
- **Gags:** Freie Gags laufen bis Tag 31 weiter (`wann.akt2` von `[8, 21]` auf `[8, 31]`); vorher Texte prüfen, die Alon, Holm, die Festa oder „tomorrow“ erwähnen. Die letzten Tage vor der Kommission bleiben gagfrei.

## Was Duc an einer guten Story wichtig ist

1. **Schreibe wie ein Mensch.** Natürlich, mit Abwägen und Zögern, nicht abgehackt („KI-Haiku“), nicht überpoliert. Maßstab: **Disco Elysium**. Humor aus Charakter, nicht aus Pointen-Maschinen. Kurz ist erlaubt, wo Kürze die Figur ist (Petrus „Hm.“). Regeln: `STIL.md`, Abschnitt „Witzig und warm“.
2. **Einfaches Englisch.** Nicht alle Spieler sind Muttersprachler. Häufige Wörter, kurze Sätze, keine Redewendungen, keine doppeldeutigen oder seltenen Wörter (Beispiel: nicht „drew“, sondern „designed“). Erzähltext: ein Gedanke pro Satz.
3. **Der Spieler vergisst.** Jeder Rückbezug trägt eine Erinnerung im Satz („that first relay, the night you held the lamp“). Eine Figur stellt eine klare Frage, bevor der Spieler antwortet. Antwort-Chips müssen ohne Vorwissen verständlich sein.
4. **Gescriptete Events sind immersiv und geführt.** Beat-Plan als Tabelle: Ansage → Inhalt → Handlung → Reaktion → Übergang. Titelkarten mit Continue, Skip, Reaktionen der Anwesenden, Gefühl auf dem Sprite, keine stumme Umschaltung, klare Handlungsaufforderung. Alle Beteiligten kommen zu Wort.
5. **Spielspaß wie ein Game of the Year.** Jede Mechanik misst du an Vorbildern (Stardew Valley, Dave the Diver, Persona 5, Hades, Disco Elysium, Clair Obscur …): Kern-Schleife, kurze und lange Ziele, variable Belohnungen, „noch ein Tag“-Haken. **Keine Verwaltungsarbeit, keine Einkaufslisten.**
6. **Mechaniken verweben.** Jeder Vorteil braucht eine Stelle im Code, an der er wirkt (Preis, Zugang, Lohn, Uhr …). Schwache Mechanik nicht aufblasen, sondern an Vertrauen und Events hängen und Zufall durch Entscheidungen ersetzen.
7. **Entscheidungen zählen.** Was der Spieler tut (Vertrauen, Ruf, Aufträge, Aussagen), ändert das Ende sichtbar. Casanovas Aufträge entscheiden, wie voll die Festa im Schlussbild ist; Duc überzeugt in Woche 5 die Leute einzeln.
8. **Figuren treu bleiben.** Vor jeder Zeile die Figurenseite lesen. Dorf-Figuren (Pascal, Mina, Bà Tư, Sandru, Don Anghjulu, Minicu, Buenaventura) bekommen ihre Momente; neue Nebenfiguren bekommen Legenden-Kommentare (das Dorf redet).
9. **Prüfsteine vor jedem Vorschlag:** Spielerreise, Sehnsucht, Vorbild, Zeitbudget, Kanon, Ton, Wirkpunkt, Selbstkritik (`BRAIN_TRUST_PROMPT.md`). Gib nach jedem größeren Vorschlag eine kurze **Gegenrede** und eine **Verbesserungsrunde** (Rollen: Sienna, Aly, Luise, Maelle, Sora; Titel in Klammern, nie `>`-Zitate). Lob und Motivation bleiben der Ton, Kritik immer mit Gegenvorschlag.

## Technische Umsetzung

- **Ablauf:** Erst ein Drehbuch im Wiki (`docs/wiki/welt/drehbuch_akt3.md`, mit Beat-Tabelle je Szene und Tag-für-Tag-Kalender), dann der Bau. Jede Mechanik sofort im Wiki erklären (Auslöser, Chancen, Grenzen, Zahlen).
- **Events** gehören in neue Dateien `werkzeuge/eden_rise/ereignisse_akt3_*.py` nach dem Muster der vorhandenen. Bau mit `python werkzeuge/eden_rise/ereignisse_basis.py` nach dem Muster dort; neue Räume brauchen in `modul.json` `"bild": {"tag": ...}`, ein String lässt das Gate abstürzen. Modul-Sperre: ab Tag 21 Nachmittag laufen nur `bl_`-Events; für Akt 3 die Sperre anpassen.
- **Gesprochene Zeilen:** Jede vertonte Zeile hat **mindestens einen Turbo-Tag** (`[laugh] [chuckle] [sigh] [gasp] [cough] [clear throat] [sniff] [shush]`), kein `[groan]`. Wenige, gezielte Tags an der Stelle des Geräuschs. Die Tags erscheinen **nie im Spieltext**. Trage Zeilen in `module/eden_rise/stimme_tags.json` ein (Muster dort). Vertonung selbst läuft später lokal bei Duc; deine Arbeit ist: Zeile, Sprecher, Tag, Gefühl.
- **Sprites und Bilder:** Du kannst keine erzeugen. Verwende vorhandene Posen und Hintergründe. Wo etwas fehlt, trage es in `docs/uebergabe/akt3_bestellungen.md` ein (Figur, Pose/Gefühl, Szene, Bildidee) und nutze bis dahin einen erlaubten Platzhalter. Prüfe Namen gegen `modul.json` (z. B. ist `mayors_office` kein erlaubtes Bild, `village_piazza` schon).
- **Sprite-Stimmung:** „neutral“ ist ruhig und frontal; ernste Szene = ernste Pose; joy/amusement nie in Events mit Ton `ernst` (`test_sprite_stimmung`).
- **Sounds:** Jeder `ton` auf einer Kartenzeile braucht eine gewählte Datei (`test_sfx`). Ohne Datei keinen `ton` setzen und in die Bestellliste schreiben.
- **Tests:** Lauf, was ohne Bilder und Ton läuft: `python tests/test_*.py` einzeln (z. B. `test_aufbau`, `test_akt2_events`, `test_sprite_stimmung`). Es fehlen `module/eden_rise/figuren` und `eden-config.json`; Tests, die sie brauchen, melde als „lokal nicht prüfbar“, statt sie zu ändern. Bots brauchen `PYTHONHASHSEED=0`. Schreibe für neue Mechaniken eigene Tests.
- **Spielstände zwischen den Akten:** Akt 3 beginnt nach `akt2_ende`; Flags wie `gennaro_verschwunden`, `sirene_weg`, `buenaventura_schwur`, `tk_haus_weg_<id>`, `tk_yacht_weg` sind schon im Spiel. Suche vorhandene Flags mit Grep, bevor du neue erfindest.

## Grenzen

- Fasse **nicht** an: `master`, Bilder, Ton, `eden-config.json`, API-Schlüssel (es gibt keine hier), die Handy-Ketten und alles, was zu „Favours“ gehört (`ereignisse_favours.py`, `ereignisse_handy.py`, `handy_eden_rise.py`). Duc kennt deren Inhalt noch nicht und soll ihn nicht von dir erfahren. **Öffne und zitiere diese Dateien nicht.** Brauchst du einen Anschluss dorthin, nenne nur die Stelle in der Fragenliste.
- Keine Fall-Auflösungen, Wendungen oder Enden-Details in Chat-Zusammenfassungen ausbreiten, außer Duc fragt gezielt nach einer Szene (Spielerfolg vor Spoilerschutz bei konkreten Szenen).
- Kein Push auf `master`, kein Löschen von Branches, keine Änderung an Wiki-Kanon ohne Vermerk in `docs/brain_trust/ENTSCHEIDUNGEN.md` (Vorschlag als „offen“ eintragen, Duc entscheidet).

## Übergabe an Duc

Am Ende (und nach jedem größeren Block) eine kurze Übergabedatei `docs/uebergabe/akt3_cloud.md`: gebaut (Commits), offen, wartet auf Ducs Urteil, Bestellliste für Bilder/Ton, Fragenliste, bekannte Fallen. Duc holt den Branch lokal, prüft ihn und führt ihn zusammen. Schreibe die Zusammenfassung für ihn auf Deutsch, die Spieltexte auf Englisch.

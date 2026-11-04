# Abschluss Cloud-Sitzung · Analyse (04.11.2026)

Jede Aufgabe liegt auf einem eigenen Branch, abgezweigt von `master` (bdb05cc). Nur neue Dateien, keine Spieldaten geändert, `master` nicht berührt, Favours- und Handy-Dateien und `story.json` nicht geöffnet.

| Aufgabe | Branch | Commit | Neue Dateien |
|---|---|---|---|
| 1 · Drehbuch Akt 3 | `akt3-cloud` | `506dce2` | `docs/wiki/welt/drehbuch_akt3.md`, `docs/uebergabe/akt3_fragen.md`, `akt3_bestellungen.md`, `akt3_cloud.md`, Eintrag E-120 (offen) |
| 2 · Folgen der Belagerung | `folgen-belagerung` | `6532472` | `docs/wiki/welt/akt3_folgen_belagerung.md` |
| 3 · Balancing | `balancing-bericht` | `4ecd4e0` | `docs/uebergabe/balancing_bericht.md`, `tests/sim_kaempfe.py`, `tests/test_balancing_befunde.py` |
| 4 · Text-Audit | `audit-text` | `0003c5e` | `docs/uebergabe/audit_text.md`, `tests/audit_text.py` |
| 5 · Gegenrede Drehbuch | `drehbuch-gegenrede` | `ee49f6c` | `docs/uebergabe/drehbuch_gegenrede.md` |
| 6 · Wiki gegen Code | `wiki-vs-code` | `449353e` | `docs/berichte/wiki_vs_code.md` |

**Wichtig zu `akt3-cloud`:** Den Branch gab es auf GitHub noch nicht. Mein Push des Drehbuchs hat ihn angelegt, bevor die Anweisung kam, dort nicht zu schreiben. Eine andere Sitzung findet dort also schon meinen Commit vor. Ich habe nichts gelöscht. Duc entscheidet, ob der Commit bleibt, auf einen eigenen Branch wandert oder überschrieben wird.

## Je Aufgabe

### 1 · Drehbuch Akt 3
**Kernbefund:** Ein vollständiger Entwurf für Tag 24 bis 35 mit Kalender, drei Mechaniken (Baustellen als Tür zur Aussage, Zeugen, Casanovas Festa-Tafel) und Beat-Tabellen für 32 Szenen. Die Idee „wer es gesehen hat, sagt es laut“ verbindet Wiederaufbau, Kommission und Enden. Die Gegenrede (Aufgabe 5) hat danach echte Fehler gefunden, der Entwurf ist deshalb nicht baureif.
**Offen:** Gebaut ist nichts, der Bau wartet auf Ducs Ja. **Duc entscheidet:** V1 bis V13 im Drehbuch, F-01 bis F-16 in der Fragenliste.

### 2 · Folgen der Belagerung
**Kernbefund:** 43 `bl_`-Flags, davon liest nach Tag 23 kein einziges mehr irgendwer, 26 werden nie gelesen. Drei Wahlen der Belagerung wirken schon in Akt 2 nicht, obwohl das Drehbuch Finale es verspricht: Türen (Petru, Ruf 4), Alvas Runde und Dons Kirchen-Wahl. Für jedes ungelesene Flag steht ein Wirkpunkt in Akt 3 bereit, die drei offenen Entscheidungen (Yacht auf Grund, Minicus Überleben, `akt3_festa`) sind nirgends als Tatsache gesetzt.
**Offen:** Die drei Akt-2-Fehler gehören in die Belagerungs-Sitzung. **Duc entscheidet:** ob die Fehler vor Akt 3 behoben werden.

### 3 · Balancing
**Kernbefund:** Rund 30.000 simulierte Kämpfe über 88 Begegnungen, kein Absturz. Mr. White wird leichter, je stärker Duc ist (Level-Deckel bei 10, bei Duc 9 nur 13 % Niederlagen), Kobra, Skorpion und Boarding Robot sind im echten Kampf harmlos, und ein vorbereiteter normaler Spieler verliert die Belagerung nie. Drei Begegnungen aus Akt 2 (`rt_4c_drohne`, `hafen_ricci_3`, `kloster_7_affe`) sind härter als der Endgegner.
**Offen:** `sim_belagerung.py` rechnet Duc mit Level 1, der vierte Spielertyp lief nur 10-mal. **Duc entscheidet:** was „100 %“ heißen soll (Wiki: fast unmöglich, Sim: für Anfänger machbar), und ob Bosse härter werden oder es weniger Kämpfe gibt.

### 4 · Text-Audit
**Kernbefund:** 741 Rückbezug-Stellen und 1.772 seltene Wörter als Kandidaten, von Hand auf rund 60 echte Funde gekürzt. Die schwersten Rückbezüge stecken in Romanzen-Echos und Chips (Rosis „the relay“ ist genau Ducs Beispiel aus STIL.md), die häufigsten schwierigen Wörter sind Seemannswörter an Tag 0 (*gangway, deckhand, bosun, foredeck*). Vorschlag: Seemannswörter einmal erklären statt überall ersetzen, Chips mit Rückbezug immer mit Erinnerung im Chip selbst.
**Offen:** Der Pool der Handy-, Favours- und Selfie-Texte ist bewusst nicht geprüft. **Duc entscheidet:** ob Totòs „small potatoes“ als Doppelsinn bleiben soll.

### 5 · Gegenrede Drehbuch
**Kernbefund:** Das Drehbuch auf `akt3-cloud` war mein eigenes, darum hat ein unabhängiger Prüfer es ohne meine Begründungen gelesen. Es gibt harte Kanonbrüche (Duc nimmt die Sonnenbrille ab, das Rädchen ist privat statt vor dem Stream, die Kommission widerspricht dem gebauten `mo_kommission`, falsche Wochentage, Petru „am Tor“) und Designschwächen (Woche 4 voller als Woche 5, Festa-Tafel halb Einkaufsliste, Zeugen-Chips als Rätselraten, Romanzen fehlen fast). Zu jedem Punkt gibt es einen Gegenvorschlag und eine Verbesserungsrunde.
**Offen:** Das Drehbuch ist nicht angepasst (Auftrag: nicht ändern). **Duc entscheidet:** Maelles Frage, ob die Romanzen-Schlüsse in Woche 4 oder Woche 5 liegen, und die neuen Fragen am Ende der Gegenrede (was Duc über den Verkauf wusste, Ort der Kommission, Stream beim Rädchen).

### 6 · Wiki gegen Code
**Kernbefund:** 59 Widersprüche, davon 10 hoch. Für Spieler sichtbar sind vor allem: Das Inventar-Menü zeigt immer „x/6“, obwohl die Tasche 8/12/16 Plätze hat. Halsbänder und Granate der Auffangstation enden an Tag 21, obwohl die Spuren bis Tag 35 laufen (dann fällt `mo_kommission` aus). Funken kommen ab Tag 3 und in beiden Phasen, weil ein Parameter ignoriert wird. Außerdem beginnt Akt 3 im Code (Schneider, Tasche, Stahl, Holms Revanche) an Tag 22 statt an Tag 24.
**Offen:** `stimme_tags_pruefen.py` lokal laufen lassen (eine Zeile von Bà Tư ohne Tag). **Duc entscheidet:** Akt-3-Start im Code auf Tag 24 ziehen (Empfehlung: ja, zusammen mit dem Kalender) und ob die gedrosselte Ereignis-Dichte auch in Akt 3 gilt.

## Tests

| Test | Ergebnis |
|---|---|
| `tests/test_balancing_befunde.py` | 5 Tests, OK, davon 2 erwartete Fehlschläge (Befund besteht) |
| `tests/sim_belagerung.py 30` | lief durch (vierter Typ in der Zeitgrenze) |
| `tests/sim_kaempfe.py 6` | lief durch, 0 Abstürze |
| Tests mit `module/eden_rise/figuren` oder `eden-config.json` | lokal nicht prüfbar, nicht gestartet |

## Was Duc als Nächstes tun sollte (Vorschlag)

1. Über `akt3-cloud` entscheiden (siehe oben).
2. Die drei Akt-2-Fehler aus Aufgabe 2 und die zehn „hoch“-Funde aus Aufgabe 6 an die zuständigen Sitzungen geben, bevor Akt 3 gebaut wird.
3. Das Drehbuch mit der Gegenrede überarbeiten lassen und dann erst Woche 4 bauen.

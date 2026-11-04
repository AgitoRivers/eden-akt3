# Audits: Kurzfassung für Duc

Stand 04.11.2026 · Branch `berichte-audits` (von master) · nur Berichte, am Spiel ist nichts geändert.

| Bericht | Datei | Umfang |
|---|---|---|
| (1) Wirkpunkt-Audit | [`wirkpunkt_audit.md`](wirkpunkt_audit.md) | 92 Einträge: 53 vorhanden, 13 klein, 26 fehlt; zehn größte Lücken mit Vorschlag |
| (2) Stimmen-Audit | [`stimmen_audit.md`](stimmen_audit.md) | 17 Hauptfiguren, rund 2300 Sprechzeilen gesammelt; je Figur drei Treffer, drei Ausrutscher mit Vorschlag |
| (3) Beat-Plan-Audit | [`beatplan_audit.md`](beatplan_audit.md) | Anhörung (9 Szenen), Belagerung (35 Zeilen), Cliffhanger (7 Events), Tauchgang (Plan); Ja/Nein je Regel R1 bis R9 |

Vorweg das Gute: Der Kampf ist vorbildlich verdrahtet (alle Chip-Wirkarten, Jacken, Charms und Küchenboni wirken im Code), die
Sprite-Gefühle passen zu 96 % zur Lage, und Rosi, Chiara, Sophia, Jana und Elsa treffen ihre Figurenseiten fast durchgehend.

## Die fünf wichtigsten Funde

1. **Der Kern von Akt 3 hat noch keinen Wirkpunkt.** `kern/aufbau.py` (Wiederaufbau) ist gebaut, wird aber nur von Tests
   importiert; `aufbau_fertig_<id>` liest niemand. Das Vertrauen von Pascal, Mina, Sandru und Minicu steigt in 29 Folgen, wird aber
   nirgends abgefragt. Für Casanovas Festa-Aufträge gibt es weder Daten noch Code (`danzel_festa_auftrag`, `chiara_festa_kleid` werden
   gesetzt und nie gelesen). Vorschlag: `aufbau` in `eden.py` einhängen, Dorf-Vertrauen als Bedingung für Zeugen der Kommission und
   für die Gästezahl im Festa-Schlussbild nutzen. (Bericht 1, Lücken 2 bis 4)

2. **Ein echter Fehler im Bordrat.** `kern/ereignisse.py: waehlen()` rechnet den Buzzing-Vorteil für den dritten Weg aus, gibt ihn
   aber nicht an `probe_fn` weiter, und `eden.py` übergibt immer `probe_fn`. Der Vorteil fällt in 30 Optionen still weg, die Strafe
   (SG +2) wirkt dagegen. Vorschlag: `probe_fn` um `vorteil` erweitern, in `szene.feste_probe()` verodern, Test mit Moral 4.
   Daneben verkaufte Dinge ohne Wirkung: Toolbox und Chef's Knife (nur in abgeschalteten Schnelljobs), Datenpaket und Cohiba
   (`benutzen: []`), und Riposte, Zéphyr, Citadelle sind fertig, aber kein Event gibt sie dem Spieler. (Bericht 1, Lücken 1, 5, 6, 8)

3. **Ernste Ketten werden durch Standard-Zwischenkarten zerschnitten.** Normale Events haben nur eine Karte „Go on“ mit
   Standardsatz („It is night now. Something else needs you.“), keinen Skip und keinen Titel. Im Cliffhanger kommt dieser Satz fünfmal
   zwischen Platz und Alons Bühne, ebenso in `bl_funk_*`, `bl_wache_*`, `bl_kirche_don*`. Skip gibt es nur in 19 % der geprüften
   Szenen. Vorschlag: Folgetakte unter `ohne_karte` in `uebergaenge.json`, dauerhaft `uebergang_text` für `direkt`-Events leer lassen,
   Titel und „Skip ▸▸“ wie in der Anhörung. Dazu: In `bl_leer` und `bl_ab_schon` steht immer Chiara stumm im Bild, auch vor ihrem
   eigenen leeren Zimmer. (Bericht 3, Top 1 bis 3)

4. **Anrede und Marotten kippen gerade in den ernsten Szenen.** Holm sagt in der Belagerung neunmal „Officer“ statt „Frankfurt“,
   Totò sagt in den Gennaro-Szenen „boss“ (Lolas Wort), Petru zweimal „Officer“. In `ereignisse_belagerung_nacht.py:273` und `:274`
   sprechen sieben Frauen dieselben zwei Zeilen. Marotten sind zu dicht (Maxwell „Mr. Maximum“ in 60 von 67 Zeilen, Petru „Hm.“ in
   29 von 76, Alva „o figliolu“ in 34 Zeilen trotz K9 „sparsam“) oder fehlen (Megans Schottisch, Chiaras Französisch). 89 Zeilen
   haben keinen Eintrag in `stimme_tags.json`, und weil der Schlüssel der Klartext ist, bekommt Petrus trauriges „Hm.“ in
   `bg_petru_auftrag` ein `[chuckle]`. Vorschlag: `tests/test_anrede.py` mit Ausnahmeliste, ein Markenwort höchstens einmal pro
   Auftritt. (Bericht 2, Muster 1 bis 3 und 6)

5. **Die Beat-Pläne fehlen im Wiki, und das Wiki ist an drei Stellen veraltet.** Keine geprüfte Szene hat eine Beat-Tabelle mit
   Ansage → Inhalt → Handlung → Reaktion → Übergang (R8: 0 %). Veraltet: `drehbuch_finale.md` Abschnitt 11 sagt, Alon habe weder
   Stimme noch Sprite; `belagerung.md` nennt für `bl_belagerung` und `bl_bericht` andere Tage als der Code und lässt Charly den
   Satelliten hacken (im Code Rosi). Rückbezüge ohne Erinnerung: Alvas „Somebody promised me a round“ in `bl_bar` kommt auch ohne
   `bl_alva_runde`, Holm sagt im Briefing zu Welle 3 „your man from the wreck“, obwohl der Tauchgang nicht gebaut ist
   (`taktik_eden_rise.py:258`). Vorschlag: Tauchgang vor dem Bau als volles Drehbuch mit Beat-Tabelle planen, die alten Abschnitte
   nachziehen (mit Vermerk in `ENTSCHEIDUNGEN.md`). (Bericht 3, Top 4 und 5)

## Grenzen und Hinweise

- Nicht geprüft: Favours, Handy-Ketten, `story.json`, Texte mit `vh.`, `fv_`, `rt_t_`. Wo das eine Bewertung kippen könnte, steht im
  Bericht „Vorbehalt: gesperrt“.
- Ehrlicher Vermerk: Beim Sammeln der Sprechzeilen aus `ereignisse.json` liefen auch Handy-Texte mit der Kennung `hy_` durch die
  Prüfung, weil diese Kennung nicht auf der Sperrliste stand; ein Grep im Wirkpunkt-Audit zeigte einmal eine Zeile aus der Handy-Datei.
  In keinem Bericht steht davon etwas (eine Event-Kennung habe ich nachträglich entfernt). Vorschlag: `hy_` künftig mit auf die
  Sperrliste setzen.
- Tests: `test_sprite_stimmung`, `test_cliffhanger` und `test_anhoerung` laufen durch. Ob alle Sprite-Dateien existieren, ist hier
  lokal nicht prüfbar (`module/eden_rise/figuren` fehlt).

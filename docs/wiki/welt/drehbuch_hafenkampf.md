# Hafenkampf · Tag 2 nachmittags

Stand 30.10.2026. Freigegeben von Duc (E-044, Variante A). Niederlage: die Welle beginnt neu (E-041).

**Rosis Hilfe (Duc 30.10.2026, nach dem Spieltest):** Nach der ersten Niederlage in irgendeiner Welle kommt einmalig Rosi
(`hk_tipp_ratten`, `hk_tipp_hunde`, `hk_tipp_keiler`, je Welle das passende Bild). Sie sagt vertont, dass Duc seine Spezialangriffe
nutzen soll, gibt ihm 3 Pflaster sowie je eine Wasser- und Schockgranate und erklärt den Kurzschluss (erst nass, dann Strom auf
dasselbe Tier). Danach startet die Welle neu mit vollen Leben. Die Gegner werden nicht schwächer. Gesteuert über `hilfe_event` und
`hilfe_flag` der Begegnung (`eden.py`, Flag `hafen_hilfe_bekommen`); die Mehrfach-Gabe über `{"item": id, "n": 3}` in den Folgen.
Events: `werkzeuge/eden_rise/ereignisse_hafen.py`. Kämpfe: `werkzeuge/eden_rise/kaempfe_eden_rise.py` (hafen_*).

## Kette (seit 26.10.2026: „The Day the Animals Came“, Ortskette im Expeditions-Bildschirm)

Duc 26.10.: Jede Welle rettet eine Person, danach eine Nachbetrachtung mit allen. Läuft am Nachmittag von Tag 2 direkt
nach Maxwells erster Lektion. Der Auftakt `hk_hilfe` ist das Pflicht-Event und startet die Kette (Folge `ort_start`),
alle weiteren Frames sind Event-Art `ort` mit eigenem Hintergrund. Kein Rasten, kein Rückweg (`sperre`); Niederlage:
dieselbe Welle neu (E-041). Am Ende ist die Phase verbraucht.

| # | Frame | Bild | Was passiert |
|---|---|---|---|
| 1 | `hk_hilfe` „Cala d'Orsu Is Screaming“ | `hafen_kai_chaos` | Ratten über den Fischkisten, Totò und Lea |
| 2 | `hk_rosi_<chip>` „Wave 1 · Rats on the Quay“ | `hafen_kai_chaos` | Rosi wirft Terremoto (4 Varianten nach dem Tag-0-Chip) → Kampf `hafen_ratten` |
| 3 | `hk_petru` „The Blue Boat“ | `hafen_kai_chaos` | **Rettung Petru:** hält mit dem Bootshaken sein blaues Boot („My wife painted that boat“); Kennenlern-Chips |
| 4 | `hk_welle2` „Wave 2 · The Dogs“ | `hafen_bar_tuer` | Rudel umstellt die Bar → Kampf `hafen_hunde` |
| 5 | `hk_alva` „Last Orders“ | `hafen_bar_tuer` | **Rettung Alva:** Krallen in der Tür; Chips mit Begehren; „That's the mayor. …Go on.“ |
| 6 | `hk_welle3` „Wave 3 · The Boar“ | `piazza_treppe` | Keiler vor der Rathaustreppe, Casanova mit Konfettikanone → Kampf `hafen_keiler` |
| 7 | `hk_casanova` „The Mayor Holds the Stairs“ | `piazza_treppe` | **Rettung Casanova:** „My father built these steps.“; Chips |
| 8 | `hk_abend` „After the Storm“ | `hafen_abend` | Nachbetrachtung am Fass: Elsa (Chips, kommt zu spät), Totò, Petru, Alva; Alva und Casanova – das geschobene Glas; Casanovas Rede: „the day after tomorrow … my office“ |
| 9 | `hk_ziege` „Something That Blinks“ | `hafen_abend` | Die Ziege mit dem blinkenden Halsband → `kloster_faden` |

**Danach:** Tag 3 Aufräumen (Landgang, Alvas Bar wieder offen). **Ab Tag 4** steht „Madame Casanova's Office“ als Ort in
der freien Phase (`auftraege_eden_rise.py`, Ort `rathaus`) – dort vergibt sie den Kloster-Auftrag (`kl_casanova_auftrag`).
Test: `tests/test_hafen.py`.

## Wellen (Variante A)

Ein Kampf je Welle gegen das Alpha-Tier. Das Rudel ist ein Sonderangriff („Das Rudel springt mit“), kein eigener
Gegner. Flucht ist nicht erlaubt („Hinter dir ist das Dorf“). Sieg, Aufgabe und Entkommen setzen das Wellen-Flag – die
Tiere fliehen in die Macchia, keins stirbt. Niederlage: kurze Zeile, dieselbe Welle startet neu.

| Welle | Sprite | Klasse | Stufe | Sonderangriff | Werte |
|---|---|---|---|---|---|
| Ratten | RatAlpha | tier | lästig | Das Rudel springt mit (🐀🐀) | nach den Gegner-Regeln der Kampf-Sitzung |
| Hunde | DogAlpha | tier | gefährlich | Das Rudel kreist ein (🐕🐕) | dito |
| Keiler | WildschweinKeiler | tier | gefährlich | Ansturm (🐗) | dito |

## Kennenlernen im Dorf

Wie Tag 0 (E-018): vier Chips je Figur, Wahl setzt `dorf_<id>_<v/b/h/n/f>`. Alva hat Begehren, Elsa, Petru und
Casanova Humor. Ab hier kennt Duc das Dorf; der Landgang an Tag 3 baut darauf auf (man kennt sich schon vom Kai).

## Technik (offen, wartet auf den Commit der Kampf-Sitzung)

- `kaempfe_eden_rise.py`: Gegner `ratte_alpha`, `hund_alpha`, `keiler`; Begegnungen `hafen_ratten`, `hafen_hunde`,
  `hafen_keiler` mit `neustart_bei_niederlage: true`, `flee_allowed: false`.
- `eden.py`: Event mit Kampf in einer Prolog-Kette – erst der Kampf, dann das nächste Glied. Nach `kampf_schliessen`
  die Kette weiterziehen (`pflicht_ziehen(nur_prolog=True)`); bei Niederlage und `neustart_bei_niederlage` dieselbe
  Begegnung neu starten.
- `ereignisse_akt1.py`: `mx_tutorial` bekommt `prolog=True` (erstes Glied der Kette).
- `story_eden_rise.py`: Landgang Tag 3 – das Dorf kennt Duc schon.
- Töne: Rudel-Getrappel, Keiler-Schnauben, Ziegen-Meckern (nach der Tag-0-Runde).

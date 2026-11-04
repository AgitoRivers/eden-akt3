# Balancing-Bericht · Belagerung und alle Kampf-Begegnungen

Stand 04.11.2026 · Cloud-Sitzung, Branch `balancing-bericht` · **Nur Bericht und Vorschläge, nichts eingebaut.** `taktik.json` wurde weder neu gebaut noch committet (Kampf-Sprites fehlen im Auszug).

## Was gerechnet wurde

| Lauf | Befehl | Umfang |
|---|---|---|
| Belagerung, sechs Wellen | `PYTHONHASHSEED=0 python tests/sim_belagerung.py 30` (vorhanden) | drei Spielertypen × 30 Läufe; der vierte Typ („Stark, 40 %“) lief in die Zeitgrenze, seine Zahlen stammen aus einem Lauf mit 10 Läufen |
| Alle Kampf-Begegnungen | `PYTHONHASHSEED=0 python tests/sim_kaempfe.py 6` (**neu**) | 88 Begegnungen (74 aus `kaempfe.json`, 14 der Taktik-Karte über `kern/taktik.kampf_defs`), je Duc-Level 3 Stufen, 5 Waffen, ohne Fähigkeiten und mit jedem der 5 Pfade, 2 Paraden-Profile, 6 Läufe. Rund 30.000 Kämpfe, **0 Abstürze** |
| Belege | `python tests/test_balancing_befunde.py` (**neu**) | 5 Tests, davon 2 als `expectedFailure` markiert (Befund besteht) |

**Spielertypen im Kampf-Sweep:** *einfach* = nur Angriff, keine Fähigkeiten, Parade 35 % perfekt, 40 % gut, 25 % verfehlt. *geübt + Pfad* = alle Spezialangriffe eines Pfads bis zum Level, Parade 55/35/10. Keine Gegenstände, keine Chips, Startjacke Terra Scura.
**Lesart:** „Niederlage“ = Duc fällt. „Entkommen“ (der Gegner zieht sich zurück) zählt weder als Sieg noch als Niederlage. Darum hat der geübte Spieler bei Hunden und Affen manchmal eine *niedrigere* Siegquote: Seine Spezialangriffe jagen den Gegner in die Flucht, bevor er k.o. geht. Das ist kein Balancing-Fehler.

**Grenzen:** `sim_belagerung.py` schätzt den echten Kampf nur (LP-Verlust nach Formel) und rechnet Duc dabei mit Level 1, weil der Spielstand keinen Fortschritt hat. Support-Plätze spielen nicht mit. Die Zahlen zeigen die Richtung, nicht den Wert.

## Kurzfassung (die fünf wichtigsten Funde)

1. **Mr. White wird leichter, je stärker Duc ist.** Er steht vier Level über Duc, aber `kampf.starten` klemmt auf `LEVEL_MAX = 10`. Bei Duc Level 9 ist White nur noch Level 10. Niederlagen des einfachen Spielers: **80 % bei Duc 3, 77 % bei Duc 6, 13 % bei Duc 9**. Bei Duc 9 ist Buenaventura (63 % Niederlagen) schwerer als der Endgegner. Beleg: `test_balancing_befunde.WhiteAbstand`.
2. **Kobra, Skorpion und Boarding Robot sind im echten Kampf harmlos.** 0 bis 3 % Niederlagen auf jedem Level, beide neuen Gegner haben die Werte des Boarding Robot (Vorlage `unit01`, Level −1). Auf der Karte sind sie Jäger, im Kampf Lästlinge. Beleg: `test_balancing_befunde.KleineRoboter`.
3. **Ein vorbereiteter normaler Spieler verliert die Belagerung nie.** „Normal, 70 %, Rosi + Elsa“: 30 von 30 Läufen ohne einen einzigen Neuversuch, Welle 2, 4 und 5 deutlich unter Par (5,9/8, 6,4/9, 7,4/9).
4. **100 % ist nicht „fast unmöglich“.** Das Wiki will bei 100 % ein Speedrunner-Ereignis (`welt/belagerung.md`, „Die Idee“). Der Anfänger ohne Reserve kommt bei 100 % in vier von sechs Wellen beim ersten Versuch durch und bleibt nur in Welle 6 (36 %) und Welle 4 (10 %) hängen.
5. **Drei Kampf-Begegnungen aus Akt 2 sind härter als Mr. White:** `rt_4c_drohne` (83 % Niederlagen, mit dem Schwert 100 %), `hafen_ricci_3` (77 %), `kloster_7_affe` (57 % schon bei Duc 3).

## 1. Belagerung (`tests/sim_belagerung.py`, 30 Läufe)

| Welle | Anfänger 100 % ohne Reserve | Anfänger 80 % mit Elsa | Normal 70 % Rosi + Elsa | Stark 40 % Rosi + Yamamoto (10 Läufe) |
|---|---|---|---|---|
| 1 | 100 % beim ersten Versuch, 5,4/5 Runden | 100 %, 5,3/5 | 100 %, 5,4/5 | 100 %, 6,2/5 |
| 2 | 70 %, 8,9/8 | 100 %, 7,3/8 | 100 %, **5,9/8** | 100 %, 5,4/8 |
| 3 | 83 %, 10,2/7, **3,4 Häuser verloren** | 96 %, 2,2 Häuser | 100 %, 1,1 Häuser | 100 %, 1,2 Häuser |
| 4 | **0 %**, 2,7 Versuche, 10 % hängen fest | 30 %, 13 % fest | 100 %, **6,4/9** | 100 %, 7,8/9 |
| 5 | 23 %, Kirche −0,6 | 76 % | 100 %, 7,4/9 | 100 %, 7,3/9 |
| 6 | 20 %, **36 % hängen fest**, Kirche −1,0 | 50 %, 6 % fest | 100 % | 100 % |

„x %“ = Anteil, der die Welle beim ersten Versuch gewinnt. „fest“ = nach vier Versuchen nicht durch. Gründe der Niederlagen beim Anfänger 100 %: Welle 4 vor allem Duc (32×), Welle 6 fast nur die Kirche (53×).

**Ausreißer und Vorschläge**

| # | Befund | Vorschlag (nur Zahl, nichts eingebaut) |
|---|---|---|
| B1 | Welle 4 ist die steilste Stufe für Anfänger (0 % beim ersten Versuch), Welle 5 danach wieder leichter (23 %, aber 0 % fest). Der Bogen im Drehbuch will 8 → 5 in Welle 4 und 8 → 2 in Welle 5 | Nachschub Welle 4 um einen Feind senken (11 → 10) **oder** Buenaventura eine Runde später. Welle 5 behält ihre Zahl |
| B2 | Welle 6 scheitert beim Anfänger an der Kirche, nicht an Duc. Die Kirche hat 3 Leben, und White steht ab Runde 1 daneben | Der Anfänger soll an White scheitern, nicht an der Tür. Vorschlag: In Welle 6 zieht ein Feind auf einer Kirchentür erst ab Runde 2 Leben ab |
| B3 | Normal mit Vorbereitung: keine Niederlage, Welle 2, 4, 5 zwei bis drei Runden unter Par | `_faktor(prozent)` (`kern/taktik.py:64`) wirkt unter 60 % zu stark. Vorschlag: Boden von 30 % auf 40 % heben **oder** die Kurve unter 60 % halbieren (`1 + (p − 60) / 260` für p < 60) |
| B4 | 100 % ist für Anfänger machbar, das Wiki will „fast unmöglich“ | Entweder das Wiki anpassen (100 % = „sehr schwer“) oder bei 100 % einen Zuschlag (+1 Feind je Nachschub). Das ist eine Designfrage für Duc, kein Fehler |
| B5 | Welle 3: Anfänger verlieren 3,4 von 4 Häusern | Passt zu Akt 3 (viele Baustellen), sollte aber bewusst so bleiben. Bitte nicht wegbalancieren, ohne `kern/aufbau.py` mitzudenken |
| B6 | Die Vorbereitung kann höchstens 70 Punkte abziehen (`taktik_eden_rise.py:540-552`), der Boden liegt bei 30 %. Nur wer **alles** schafft, erreicht den Boden | in Ordnung, nur als Hinweis: Jeder neue Vorbereitungspunkt macht den Boden leichter erreichbar |

## 2. Alle Kampf-Begegnungen (`tests/sim_kaempfe.py`)

### 2a. Belagerungs-Gegner im echten Kampf

| Begegnung | Duc 3 | Duc 6 | Duc 9 | Urteil |
|---|---|---|---|---|
| `tk_white` (Mr. White, Level Duc +4, gekappt bei 10) | 80 % / 29 % | 77 % / 33 % | **13 % / 0 %** | **zu leicht ab Duc 8** (siehe Kurzfassung 1) |
| `tk_bonaventure` (+1, mit Pirat) | 10 % / 2 % | 23 % / 5 % | **63 % / 1 %** | bei Duc 9 schwerer als White |
| `tk_roboter_schwer` (+1) | 13 % / 2 % | 7 % / 0 % | 30 % / 3 % | in Ordnung |
| `tk_roboter` (−1) | 0 % / 0 % | 3 % / 0 % | 0 % / 0 % | zu leicht |
| **`tk_kobra` (−1, neu)** | 0 % / 0 % | 0 % / 0 % | 0 % / 0 % | **zu leicht**, gleiche Werte wie der Boarding Robot |
| **`tk_skorpion` (−1, neu)** | 0 % / 0 % | 0 % / 0 % | 3 % / 0 % | **zu leicht**, gleiche Werte wie der Boarding Robot |
| `tk_hund` (−2) | 0 % / 0 % | 0 % / 0 % | 0 % / 0 % | gewollt leicht (Hunde jagen Verwundete auf der Karte) |
| `tk_agent`, `tk_schuetze`, `tk_drohne`, `tk_brute`, `tk_pirat`, `tk_gunner`, `tk_brawler` | 0 bis 10 % | 0 bis 7 % | 0 bis 30 % | in Ordnung |

Werte: Niederlagen *einfach* / *geübt + Pfad*.

**Vorschläge**

| # | Befund | Vorschlag |
|---|---|---|
| K1 | White klemmt an `LEVEL_MAX` (`kern/kampf.py:1145`, `level = max(1, min(LEVEL_MAX, level))`), Duc steht zur Belagerung vermutlich auf Level 7 bis 9 (Berge Lv 5 bis 8, `welt/orte_drehbuch.md`) | Für Bosse über `LEVEL_MAX` hinaus den Rest als Zuschlag rechnen: je fehlendem Level +15 % LP und Schlag (wie `LEVEL_GAP`). Alternative: White bekommt einen festen `lp_faktor` 1,6 in `BEGEGNUNGEN` |
| K2 | Kobra und Skorpion sind auf der Karte Jäger, im Kampf Lästlinge | Level 0 statt −1 und ein eigenes Muster aus ihren Spezialangriffen (`pattern: ["w1", "n", "s1"]`), damit *Lunge* und *Tail Blade* (nur ausweichen) wirklich kommen. Dann ist das Ausweichen ihre Lektion |
| K3 | Boarding Robot −1 ist zu leicht | Level 0, sonst gleich. Der schwere bleibt +1 |
| K4 | Buenaventura ist bei hohem Duc-Level die härteste Belagerungsbegegnung (er klemmt auch, aber mit Pirat an seiner Seite) | Mit K1 zusammen prüfen. Sein Kampf soll „es fühlt sich an wie gewonnen“ tragen (Drehbuch Finale), also eher etwas leichter als White |

### 2b. Ausreißer in Akt 1 und 2 (gleiches Level wie Duc)

| Begegnung | Gegner | Duc | Niederlagen einfach | geübt + Pfad | Waffen-Spanne (Siege einfach) | Urteil |
|---|---|---|---|---|---|---|
| `rt_4c_drohne` | Hirtendrohne | 5 | **83 %** | 37 % | Schwert 0 %, Schläger 50 % | **zu schwer**, und die Waffe entscheidet fast alles |
| `hafen_ricci_3` | drei Diebe | 6 | **77 %** | 21 % | Schläger 0 %, Speer 67 % | zu schwer für einen Hafen-Auftrag |
| `kloster_7_affe` | zwei Affen | 3 | **57 %** | 23 % | Messer 33 %, Schwert 67 % | zu schwer für den ersten Ort (Kloster) |
| `rt_4a_mufflon` | Panzer-Mufflon | 5 | 57 % | 21 % | Messer 17 %, Schläger 83 % | Waffe entscheidet, sonst in Ordnung |
| `berge_11_trio` | Brute + 2 Agenten | 5 | 53 % | 7 % | Schläger 33 %, Schwert 67 % | in Ordnung (Bosskampf der Berge) |
| `fn_5_sirene` | Sirene | 6 | 40 % | 11 % | 50 bis 83 % | in Ordnung (Rede-Boss) |
| `rt_7b_tuer` | 2 Agenten + Drohne | 5 | 40 % | 12 % | Schwert 33 %, Speer 83 % | in Ordnung |

**Zu leicht** (einfach unter 3 % Niederlagen und unter 30 % LP-Verlust auf gleichem Level): `akt1_fackelpirat`, `berge_7_agent`, `berge_9_wolf_alpha`, `berge_11_solo`, `berge_u1_old_grey`, `berge_u2_panther`, `gr_8_riscossore` (alle drei Fassungen), `kloster_8_loewe`, `kv_kevin`. Auffällig sind die **Bosse**: Der Löwe (Kloster, 28 % LP-Verlust, 0 % Niederlagen), Old Grey und Riscossore fühlen sich nach der Rechnung nicht wie Bosse an. Gegen sie kämpft der Spieler aber oft unter seinem Level erst nach Umwegen; der Sweep nimmt gleiches Level an.

**Vorschläge**

| # | Befund | Vorschlag |
|---|---|---|
| K5 | `rt_4c_drohne`: Schwert und Messer treffen eine Drohne kaum, ohne Spezialangriff verliert fast jeder | Drohne in dieser Begegnung Level −1 **oder** Bibi oder Charly geben einen Hinweis „Hit it with something heavy“ vor dem Kampf (die Lösung aus der Lage statt aus Glück) |
| K6 | `hafen_ricci_3`: drei Gegner auf Duc-Level sind im Hafen zu viel | `lp_faktoren` wie bei Rudeln: [1, 0,6, 0,6] |
| K7 | `kloster_7_affe`: zwei Affen bei Duc 3 | zweiten Affen mit `lp_faktoren` 0,5, das Kloster ist der erste Ort |
| K8 | Bosse aus Akt 1 bis 2 sind leicht | Erst nach Ducs Spieltest anfassen; der Spieltest-Befund 1 („Kämpfe sind Grind“) spricht eher für **weniger** Kämpfe mit mehr Gewicht als für härtere Bosse |

## 3. Belegte Funde im Code

| Fund | Datei:Zeile | Test |
|---|---|---|
| White klemmt an `LEVEL_MAX` | `kern/kampf.py:1145` | `WhiteAbstand.test_abstand_bleibt_bei_hohem_level` (`expectedFailure`) |
| Auftrag „Türen“ wirkt nicht: `_rudert` liest `bl_tueren_petru` nicht, das Drehbuch Finale verspricht Ruf 4 statt 5 | `kern/taktik.py:1599-1602` | `TuerenRudern.test_mit_petru_ab_ruf_4` (`expectedFailure`) |
| Kobra und Skorpion sind im Kampf Kopien des Boarding Robot | `werkzeuge/eden_rise/taktik_eden_rise.py:514-528` | `KleineRoboter.test_gleiche_werte_wie_boarding_robot` |

Weitere Kandidaten ohne eigenen Test (nur gesichtet): `enemy_stats` (`kern/kampf.py:1100`) liest weder `tier` noch eigene Werte des Gegners. Alle Gegner gleichen Levels haben dieselben LP und denselben Schlag, Unterschiede kommen nur aus Muster, Spezialangriffen, Faktoren und Klasse. Das ist vermutlich gewollt (Kloster-Balancing 26.10.), erklärt aber Befund K2.

## 4. Was offen bleibt

- Ein Lauf mit echtem Duc-Level in `sim_belagerung.py` (heute Level 1 im geschätzten Kampf). Vorschlag: `LAUF["level"]` einführen und mit `kampf.test_setup` setzen.
- Der Sweep nutzt keine Gegenstände und keine Chips. Mit dem Kit aus `expedition_sim.py` (2 Verbandskästen, 2 Granaten) sinken die Niederlagen, die Reihenfolge der Ausreißer sollte bleiben.
- Duc entscheidet: B4 (was 100 % heißen soll) und K8 (Bosse härter oder weniger Kämpfe).

# Übergabe Akt 3 · Cloud-Sitzung (Branch `akt3-cloud`)

Stand 04.11.2026, Block 3: Drehbuch Version 3 mit Ducs Entscheiden (E-122). **Keine Events gebaut.**

## Gebaut (Commits)

| Branch | Commit | Inhalt |
|---|---|---|
| `akt3-cloud` | `506dce2` | Drehbuch v1, Fragenliste, Bestellliste, E-120 offen |
| `akt3-cloud` | `e1d9891` | Drehbuch v2 (Gegenrede, Wiki gegen Code, Belagerungs-Flags, Text-Audit eingearbeitet) |
| `akt3-cloud` | (dieser) | Drehbuch v2.1 (unabhängige Prüfung von v2 eingearbeitet), Fragenliste F-17 bis F-27, E-120 nachgezogen |
| `akt3-cloud` | (dieser) | Drehbuch Version 3: Yacht schwer beschädigt mit Reparatur, Unterkünfte, Minicu erst zur Festa, Festa-Lose ohne Zähler, Megan Tag 25, Bibi- und Lea-Idee, Säule Geld mit drei Wegen, fünf Paare (Abschnitt 7), Brain Trust; E-122; Vermerke in `ortskapitel_tauchgang.md` und `enden.md`; Fragen F-28 bis F-30 |
| `fix-akt2-folgen` | `57b9204`, `6351a04` | **Code:** Türen mit Petru (Ruf 4), Alvas Runde (`bl_bar_runde`, Duc zahlt), Dons Kirche (+1 Leben ab Welle 5), Akt 3 ab Tag 24 (Sperre endet nach Tag 23, Schneider, Lesung, Holms Revanche, Expedition Pack), Station-Beweis auch in Akt 3, `tests/test_akt2_folgen.py` (15 grün), E-121 |

## Wartet auf Ducs Urteil

- Weiche W (was 100 % Belagerung an Schwierigkeit heißt), Drehbuch Abschnitt 1.
- Freigabe der Paare Chiara und Alva, Isabelle und Sophia (F-29), Lola und Bà Tư als Familienliebe (F-28).
- Welcher Code-Branch nach master: Empfehlung `fix-akt2`, nicht `fix-akt2-folgen` (F-30).
- Fragenliste `docs/uebergabe/akt3_fragen.md` (F-01 bis F-30).
- Merge von `fix-akt2-folgen` (vorher lokal: `tests/test_taktik.py` und `test_sfx.py`, die hier an fehlenden Sprites und `eden-config.json` scheitern; `test_sfx` ist schon auf master rot).

## Bekannte Fallen

- `ereignisse_basis.py` baut hier ohne Bilder und tauscht dabei bei 64 Events den Hintergrund. In `fix-akt2-folgen` sind darum nur die 23 betroffenen Events übernommen. Lokal neu bauen und `git diff module/eden_rise/ereignisse.json` prüfen.
- Neue und geänderte Zeilen aus `fix-akt2-folgen` sind nicht vertont (Alva in `bl_bar` und `bl_bar_runde`).
- Favours und Handy nicht öffnen (F-11, F-12).

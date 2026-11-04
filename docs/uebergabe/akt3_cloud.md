# Übergabe Akt 3 · Cloud-Sitzung (Branch `akt3-cloud`)

Stand 04.11.2026, Block 1: Drehbuch. **Nichts gebaut**, Events warten auf Ducs Ja.

## Gebaut (Commits)

| Commit | Inhalt |
|---|---|
| (dieser) | Drehbuch `docs/wiki/welt/drehbuch_akt3.md`: Bogen, Kalender Tag 24–35, drei Mechaniken, 32 Szenen mit Beat-Tabellen, Enden-Anschluss, Brain Trust, Bauplan. E-120 „offen“ im Register. Fragenliste, Bestellliste |

## Wartet auf Ducs Urteil

- Das ganze Drehbuch, besonders die Vorschläge V1–V13 (Abschnitt 10).
- Maelles Frage: erst Woche 4 bauen und spielen, dann Woche 5?
- Fragenliste `docs/uebergabe/akt3_fragen.md` (F-01 bis F-16).

## Bestellliste

`docs/uebergabe/akt3_bestellungen.md`: 8 Hintergründe, 9 Sprite-Wünsche, 3 Item-Bilder, 5 Klänge.

## Bekannte Fallen (für den Bau)

- `module/eden_rise/figuren` und `eden-config.json` fehlen hier. Tests, die sie brauchen, melde ich als „lokal nicht prüfbar“.
- Sperre `{"tag": 21, "phase": "nachmittag", "praefix": "bl_"}` in `modul_eden_rise.py` muss nach Tag 23 enden, sonst laufen in Akt 3 keine Events.
- Neue Räume in `modul.json` nur mit `"bild": {"tag": ...}`.
- Gags: `wann.akt2` auf `[8, 31]` erst nach Textprüfung (Alon, Holm, Festa, „tomorrow“, Megan an Bord, Pascal).
- Favours und Handy nicht öffnen (Fragen F-11, F-12).

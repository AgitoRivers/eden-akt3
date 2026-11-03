# Abnahme-Boegen (Bildpruefung)

Kleine Werkzeuge, die Ergebnisse aus `ComfyUI_krea2\ComfyUI\output\expressions` als Kontaktbogen nach
`Y:\AI\mission-control\entwuerfe\kampf_ui_bilder` legen. Nur lesen, nichts aendern.

| Skript | Aufruf | Zweck |
|---|---|---|
| `kampf_abnahme.py` | `python kampf_abnahme.py Thief,Rat --ziel name` | Kampf-Posen je Gegner auf Schachbrett, Randmessung (L/R/O = Pixel am Bildrand) im Titel |
| `portrait_bogen.py` | `python portrait_bogen.py Preset1,Preset2 _probe ziel` | je Figur eine Zeile mit allen PNGs eines Unterordners |
| `lauf_bogen.py` | `python lauf_bogen.py <ordner> <ziel> [spalten]` | Raster eines ganzen Sprite-Laufs (roh-Ordner) |

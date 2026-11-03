# Duc-Sprites im Effektlabor

Stand: 24.10.2026. 25 aktuelle Duc-Sets aus der ComfyUI-Ausgabe übernommen: Erde, Wasser, Feuer, Luft und Cyber mit je Säbel, Baseballschläger, Messer, Saufeder und Flinte. Die aktuellen Quellordner benutzen die englischen Waffen-Endungen Sword, Bat, Knife, Spear und Gun.

Die Original-PNGs bleiben unverändert. 325 vorbereitete Spielerposen und 75 gespiegelte Vergleichsposen liegen als transparente WebP-Dateien in separaten Laborkopien. Die bestehende Größen-Normalisierung aus `werkzeuge/kampf_bilder.py` wird wiederverwendet. Spielerposen sind bereits nach rechts gespiegelt; die alte zusätzliche Schutzposen-Spiegelung wird bei diesen Sets nicht angewandt.

Jedes Set enthält alle 13 vorhandenen Posen. Die laufende Angriffschoreografie lädt sieben davon: idle, windup, attack, heavy_windup, heavy_attack, hurt und guard. Ein Wechsel ersetzt die Bilder erst, wenn der ganze benötigte Satz geladen ist. Metadaten halten Fußpunkt, horizontale Verankerung und Darstellungsgröße fest. Die Ladung bleibt am Körper; Effekte und Zeitpunkte werden nicht neu entworfen.

## Bedienung

In der Ablaufprobe unter http://127.0.0.1:8337/status-labor/ablaufprobe/ stehen „Duc-Look“ und „Duc-Waffe“ für den Spieler links. Die Auswahl bleibt im Browser gespeichert. Unter „Gegnerfigur“ stehen zusätzlich die 25 Duc-Sets nach Look gruppiert zur Auswahl; diese Vergleichsposen schauen zur linken Spielfeldseite.

Die gleiche Vergleichsauswahl steht im Zustands- und Reaktionslabor zur Verfügung. Die kompakte Animation aus dem Fähigkeiten-Board lädt ebenfalls die neue Duc-Auswahl, ohne einen Kampfzug auszulösen.

`katalog.json` enthält die Sets, Quelldateien und SHA-256-Prüfsummen; `posen.json` pro Set enthält ausschließlich Darstellungsdaten. Erzeugungswerkzeug: `werkzeuge/eden_rise/labor_duc_sprites.py`. Es liest nur die existierenden Bilder und verändert weder Prompt Studio noch die Originale oder Spielstände. Ein vorhandener Ausgabeordner wird nicht überschrieben.

## Prüfung und Status

Geschrieben: 25 Sets, Katalog und Posendaten, Auswahl und Anpassung der vorhandenen Figurendarstellung.
Eingebaut: isoliertes Effektlabor einschließlich Status/Reaktionen und Skill-Animationsfenster. Keine Umstellung der laufenden Engine.
Getestet: alle 25 Spieler- und 25 Vergleichsauswahlen, Laden aller sieben benötigten Posen, gespeicherte Auswahl, Reaktionslabor, alle 16 freigegebenen Spezialanimationen. Alle 325 Quellprüfsummen unverändert, komplette Bildsätze und Transparenz geprüft. Kein neuer Commit oder Push.

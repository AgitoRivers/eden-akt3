# Duc links im Effektlabor

## Geschrieben

Sechs vorhandene Posen von DucErdeSaebel als verlustfreie WebP-Kopien unter assets/duc-links: idle, windup, attack, heavy_windup, heavy_attack und guard. Die Quelldateien unter ComfyUI/output/expressions/combat/DucErdeSaebel bleiben unverändert. Herkunft und SHA-256-Prüfsummen stehen in quellen/duc-links-v1/herkunft.json. Die beiden Kampf-Testskripte werden nicht verändert.

Eigenes Darstellungsmodul ablaufprobe/duc-links.js. Gemeinsame Freisetzungs- und Kontaktzeiten aus der bestehenden Vorschau steuern die Posen. Keine zweite unabhängige Uhr und keine Kampfregelausführung.

## Eingebaut

Nur im Effektlabor auf Port 8337, Repo und bediente Kopie synchron. Duc steht links, die bisherige Vergleichsfigur bleibt rechts als wählbarer Gegner.

- Schnelle Schnitte und Geschosse: Idle, normales Ausholen, normale Angriffspose, Rückkehr zu Idle.
- Mistral, Vendetta, Omertà und Lame de Fond: schwere Vorbereitung und schwere Angriffspose.
- Doppio Gioco und die zweistufige Vendetta-Variante: kurze Rückholbewegung vor dem zweiten Hieb.
- Phare, Point de Mire und Pluie d’Étoiles: erhobene freie Hand der Schutzpose statt eines unpassenden Säbelhiebs; hält bis zur Entladung beziehungsweise Wirkung.
- Libeccio und Bonaccia: Schutzpose, Effekt auf Duc links, Gegner bleibt Idle. Ihre vorhandenen Effekte wurden auf den Anwender versetzt.

Vorbereitung ab 0,16 Sekunden, vor Beginn des Effekts. Bei Geschossen setzt die Angriffspose 0,12 Sekunden vor Freisetzung ein; bei Schnitten 0,21 Sekunden vor dem zugeordneten Kontakt. Kurze Übergänge von ungefähr 45 bis 180 Millisekunden und ein kleiner Vorstoß beim Hieb. Jede Pose verwendet eine eigene gemessene Fußhöhe bei gleicher Skalierung. Die Schutzpose blickt in der gelieferten Datei nach links und wird ausschließlich beim Zeichnen gespiegelt.

Grenzen: Vorgerenderte Einzelposen mit kurzen Überblendungen, keine Skelettanimation oder neu erzeugten Zwischenbilder. Die Effekte behalten ihre bisherigen Szenenpositionen; sie sind noch nicht an automatisch erkannte Hand- oder Säbelpunkte gebunden. Sotto Voce bleibt die zuvor gewünschte Schallstudie; die Zuordnung zur Abtauchen-Regel ist weiterhin vor einer echten Kampfintegration zu klären.

## Getestet

Alle zwölf Angriffe in je drei Varianten und fünf Phasen geprüft: Duc sichtbar, passende Posen, Selbstwirkungen ohne Schutz- oder Hurt-Reaktion am Gegner, keine Browser- oder Ladefehler. Gerenderte Bilder für Geschoss, schweren Schnitt, Doppelschnitt, Zielmarke und Windrüstung visuell geprüft. Zusätzliche gezielte Prüfung der beiden Schnittfolgen nach Anpassung ihrer Rückholzeitpunkte. Keine Tests im echten Spielbetrieb.

Prüfskripte im Codex-Arbeitsordner work/status-labor: duc_links_pruefen.cjs und duc_schnitt_timing_pruefen.cjs.

## Ebenen, korrigierter Stand 3

Der Nutzer wünscht die Effekte ausdrücklich VOR Duc. Die zuvor irrtümlich ergänzte Körper-Überdeckung wurde vollständig entfernt. Beide Effektdurchgänge werden nach Duc gezeichnet; dadurch liegen auch die bisher als hintere Effektebene bezeichneten Anteile vor dem linken Sprite. Die Staffelung am rechten Gegner bleibt erhalten. Posen, Fußanker, Blickrichtung und Zeitpunkte bleiben unverändert.

Vorheriger Stand unter quellen/duc-effekte-vorne-v3 gesichert. Nur Effektlabor; Originalbilder und Kampf-Testdateien unverändert.

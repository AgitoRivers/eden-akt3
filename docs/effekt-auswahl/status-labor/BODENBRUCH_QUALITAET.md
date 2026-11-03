# Bodenmaterial und passende Posen

## Maßstab für weitere Änderungen

Vor der Freigabe jedes Effekts prüfen: Genügt das dem gemeinsam erreichten
Anspruch? Dazu gehören glaubwürdiges Material, freie weiche Ränder, passende
Größe und Perspektive, nachvollziehbare Bewegung und die richtige Figurenpose.
Keine aufgemalten Ersatzlinien, kreisförmig abgeschnittenen Wolken, künstlich
fallenden Bildflächen oder wahllosen Explosionen. Einen Effekt auch eingebaut
und im Ablauf ansehen; fehlerfreier Code allein genügt nicht. Eine technisch
geprüfte Variante ist nicht automatisch gestalterisch vom Nutzer abgenommen.

## Geschrieben

Der einfache Bodenriss wurde durch eine realistische Bitmap mit echter
Steinstruktur ersetzt. Das erste erzeugte Bild wirkte noch wie angehobene
Platten; die eingebaute Fassung wurde mit der eingebauten Bildbearbeitung
flacher ausgearbeitet. Sie wird in flacher Perspektive und mit zurückhaltender
Helligkeit in den Vorschau-Boden gesetzt. Original-Alpha bleibt erhalten.
Rütteln und langer Zustand bleiben bestehen; kein Nebel und kein Geröllregen.
Das Material ist ein Einzelbild, keine neue Bruchsimulation.

- Bild: `assets/bodenbruch-real-v1.png`
- Werkzeug: eingebaute Bildgenerierung, danach eingebaute Bildbearbeitung.
- Genauer letzter Prompt: `quellen/boden-material-schutzposen/finaler-prompt.txt`
- Quelle, Ausschnitt und Prüfsumme: `quellen/boden-material-schutzposen/quelle.json`

Posen richten sich nach der Wirkung:

- Nass und Erschüttert: Schutzpose, längeres Halten und weiche Rückkehr.
- Direkter Schaden: Hurt und passender Rückstoß.
- Libeccio, Point de Mire, Bonaccia und Phare: Schutzpose.
- Vendetta: nach präzisierter Nutzervorgabe direkter schmerzhafter Treffer und Blutung, deshalb Hurt.
- Sotto Voce: Schutzpose mit Ausweichbewegung und versetzten Silhouetten.

Point de Mire zeigt jetzt einen Fokus-/Markierungsreflex statt einer Schussbahn
mit Treffer. Das passt zu seiner beschriebenen Wirkung ohne direkten Schaden.
Die Spielregeln wurden nicht geändert. Die Beschreibung ist weiterhin als
Kampfplan/Balancingstand gekennzeichnet.

## Eingebaut

In die isolierte Vorschau auf Port 8337. Dateien: `zustand-reaktionen.js`,
`labor.js`, `index.html`, `ablaufprobe/angriffe.js`, `ablaufprobe/probe.js`,
`ablaufprobe/index.html` und das neue Bild. Vorherige Dateien sind in
`quellen/boden-material-schutzposen/` gesichert. Keine fremden Änderungen,
Live-Spielstände, Kampfregeln oder Commits angefasst.

## Getestet

Alle neun Zustände/Reaktionen an vier Zeitpunkten geprüft, inklusive tatsächlicher
Pose und Rückkehr. 36 Spezialvarianten an 144 Zeitpunkten geprüft. Die freigegebene
Wasserattacke ist an fünf Zeitpunkten pixelgleich mit ihrer Referenz.
Keine JavaScript- oder Ladefehler. Bedienung, Rückmeldungen und Export geprüft.
Nass und Erschüttert einschließlich neuer Bodenstruktur zusätzlich im Bild
angesehen. Zusätzlich wurden alle 18 Varianten ohne direkten Schaden am tatsächlich
gezeichneten Sprite geprüft: Schutzpose vorhanden, keine Hurt-Pose.

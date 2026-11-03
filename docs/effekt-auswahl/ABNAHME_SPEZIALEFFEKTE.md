# Abnahme der Spezialeffekte

Duc hat am 24.10.2026 die Spezialeffekte mit seiner vollstaendigen Auswahldatei freigegeben.

- 16 von 16 Spezialangriffen ausgewaehlt; verbindliche Variante und Bezeichnung stehen in status-labor/freigabe-spezialangriffe.json.
- Die Auswahl ist als Vorgabe in der Ablaufvorschau hinterlegt. Explizite Variantenlinks und persoenliche Browserentscheidungen bleiben verwendbar.
- Die alte Vendetta-Notiz ist erfuellt: zwei abwaerts laufende Schnitte bilden ein V, halten 0,8 Sekunden und verblassen langsam.
- Animationen, aktive Bildfolgen, benoetigte Quellen und Werkzeuge sind in der Git-Historie gesichert. Lokale Zwischenstaende bleiben als Sicherung erhalten.

## Abschliessende Pruefung

- Alle 16 freigegebenen Varianten in insgesamt 64 Phasen ohne Browser- oder Ladefehler geprueft.
- Alle Namen und Variantennummern stimmen mit Ducs Auswahl ueberein.
- Vorgaben im leeren Browser, Export der Auswahl und Vorrang expliziter Variantenlinks geprueft.
- 28 JavaScript-Dateien und 5 Python-Werkzeuge syntaktisch geprueft.
- Zuvor gezielt geprueft: Lade-/Entladephasen, native Materialfolgen, Nachbrand, Furia-Kurve, Vendetta-V, Omerta-Verschwinden und Rueckkehr, Pluie-Finalexplosion und die groessere Phare-Blendung an beiden Vergleichsfiguren.

## Versionssicherung bei paralleler Arbeit

Der bereits vorgemerkte Effektstand mit 455 Dateien wurde waehrend der parallelen Arbeit im Commit ae1d2f9 mit aufgenommen. Dieser Abnahme-Nachweis bekommt einen eigenen, eindeutig benannten Abschluss-Commit. Bestehende gemeinsame Commits werden nicht umgeschrieben.

## Einbaustatus

Geschrieben: Spezialeffekte, Auswahl, Bildfolgen, Quelldateien und Dokumentation.
Eingebaut: separates Effektlabor auf Port 8337.
Getestet: die freigegebenen Vorschauvarianten und ihre Figurenreaktionen.

Der Einbau in den eigentlichen Kampf und die Soundabstimmung sind ein eigener anschliessender Schritt. Dieser Stand veraendert keine Spielstaende oder Kampfregeln. Es wird nichts gepusht.

## Skill-Symbole

Die 16 freigegebenen Symbole sind einzeln in [status-labor/skill-icons](status-labor/skill-icons/README.md) gesichert und über die bestehenden Angriffs-IDs zugeordnet. Die Auswahlliste zeigt das jeweilige Symbol neben dem Namen. Originalraster und Ausschnittkoordinaten sind enthalten. Einbau in das eigentliche Skilltree-UI folgt separat.

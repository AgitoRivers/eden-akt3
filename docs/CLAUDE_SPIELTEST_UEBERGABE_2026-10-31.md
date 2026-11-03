# Eden Rise – Übergabe der Live-Spieltests an Claude

Stand: 31. Oktober 2026. Übergabeweg vom Nutzer ausdrücklich gewählt: Datei im Eden-Projekt.
Dies ist eine vorbereitete Dateiübergabe, keine Nachricht an eine laufende Claude-Sitzung und keine Bestätigung, dass Claude sie bereits gelesen hat.

## Zuerst lesen

Die Berichte liegen als lokale Kopien im Projekt unter **`docs/spieltestberichte/2026-10-31/`**:

1. [Testbericht](spieltestberichte/2026-10-31/Eden-Rise-Live-Spieltest.html)
2. [Vier Rezensionen zum Vorlesen](spieltestberichte/2026-10-31/Eden-Rise-Live-Rezensionen-Vorlesen.txt)
3. [Rezensionen mit strukturierten Befunden](spieltestberichte/2026-10-31/Eden-Rise-Live-Rezensionen.json)
4. [Quellen und Gesprächsstichproben](spieltestberichte/2026-10-31/Eden-Rise-Live-Beleganhang.json)
5. [Abnahme, tatsächliche Endstände und Quellenänderungen](spieltestberichte/2026-10-31/Eden-Rise-Live-Abnahme.json)
6. [Friststatus](spieltestberichte/2026-10-31/Eden-Rise-Live-Friststatus.json)

Die Text- und Belegdateien können Story-Spoiler enthalten. Für die erste Einordnung ist keine vollständige Lektüre interner Falllösungen nötig.

## Was tatsächlich geprüft wurde

- Echte lokale Modellantworten mit **Giftige Blume 31B v2**, kein Cloud-Modell als Spielbackend.
- Vollständig abgeschlossen: **Naomi Malice, Mia (Game-Two-Perspektive), Lenny Tennemann und Tandi**.
- Kalender: 21 Spieltage; technischer Endzustand jeweils Tag 22, Phase Nacht, Status `ende`.
- Insgesamt 8.578 echte Modellaufrufe in diesen vier vollständigen Läufen; Spieleraufrufe sind darin enthalten.
- Keine festgestellten Offline-Platzhalter und keine automatischen Hilfseingriffe in den vier vollständigen Läufen.
- Noor wurde fristbedingt unterbrochen. Alex, Deniz, Mateo und Avery wurden nicht gestartet.
- Die Namen und Medienperspektiven bezeichnen fiktive interne Testpersonen, keine echten Medienrezensionen.

Der Nutzer priorisiert **Mia und Lenny**. Ihre Berichte stehen zusätzlich separat in den Dateien `Eden-Rise-Live-Prioritaet-*`.

## Wichtigste Befunde und Prüfaufträge

1. **Beziehungsentwicklung:** Spätere Dialoge auf wiederkehrende Muster prüfen: gemeinsame Arbeit, Sensor-/Maschinenaufgaben, Wein/Karten/Wetten, ähnliche Begrüßungen. Wiederholung ist ein Signal; ihre Häufigkeit und tatsächliche erzählerische Entwicklung an den Originaltranskripten prüfen.
2. **Folgen von Nähe:** Nach Dates, Konflikten und intimen Begegnungen gezielt prüfen, was sich bei späteren Treffen verändert. Gesprächsgedächtnis wurde nicht durch eine vollständige kontrollierte Versprechen-/Ablehnungs-Testreihe abgenommen.
3. **Individuelle Romance:** Rosi, Lola, Sophia und andere Figuren sollen eigene Wünsche, Ausdrucksweisen und Entwicklungen behalten. Naomi legt Wert auf erotische Chemie und Kinks; Lenny auf Sexappeal, Fanservice, überzeugende Auflösung und Builds. Keine Beschämung dieser Interessen, aber auch keine aus der Herkunft oder dem Geschlecht abgeleiteten Vorlieben.
4. **Inventar:** Häufig volle Taschen untersuchen. Lennys Lauf erfasst 16, Tandis 17 Tage mit voller Tasche. Ursache kann Spielbalance, Bedienung oder die eingeschränkte Kauf-/Verkaufsstrategie des Bots sein.
5. **Kampf:** Hohe Siegquoten und kurze Kämpfe sind kein Beweis für geringe taktische Tiefe. Die Mechanik wurde automatisiert bedient; für Aussagen über menschliches Kampfgefühl und echte Synergien fehlen gezielte Vergleiche.

Bitte Spielprobleme von Testproblemen trennen. Vorgegebene Gesten erzeugen wiederkehrende Spielerformulierungen; abrupt benannte sexuelle Wünsche können aus dem Bot kommen. Diese Effekte nicht pauschal den Charaktertexten anlasten.

## Grenzen der Aussagen

- Keine umfassende Prüfung von Grafik, Animation, Audio, Browserbedienung oder menschlicher Reaktionsfähigkeit.
- Entscheidungen und freie Spieleräußerungen stammen aus dem lokalen Modell und sichtbaren Informationen. Mechanische Routinen verwenden weiterhin Engine-Zustände: **hybrider Test**, kein vollständiger menschlicher Erstkontakt ohne Vorwissen.
- Vereinbarte Termine und separat erkannte `date_`-Szenen sind unterschiedliche Messgrößen. Die Differenz ist nicht automatisch eine Zahl gescheiterter Dates.
- Zähler ausgeführter Intimitätsaktionen bewerten weder erotische Qualität noch die Wirkung vollständiger Szenen.
- Quellen-IDs und Struktur der Rezensionen wurden validiert. Das ist keine Garantie für die Richtigkeit jeder Modellinterpretation. Einige überzogene Aussagen wurden redaktionell als Testlücken gekennzeichnet; die Rohfassungen bleiben erhalten.
- Die im Chat genannte Wertung **7/10** ist eine subjektive redaktionelle Einordnung, kein automatisch berechnetes Messergebnis und keine unabhängige Medienwertung.

Während der Testzeit änderten sich gegenüber dem gesicherten Quellenstand:

- `module/eden_rise/ereignisse.json`
- `module/eden_rise/stimme_tags.json`

Die Vergleichbarkeit ist daher eingeschränkt. Keine Änderungen zurücksetzen, um einen vermeintlich einheitlichen Stand herzustellen.

## Dateien und Werkzeuge

Projekt: `X:\AI\Eden`.

- `tests/spieltest_profile.py`: neun Personen, Interessen, Prioritäten und geplante Live-Szenarien.
- `tests/spieltest_bot.py`: mechanische Basisroutinen und Messung.
- `tests/spieltest_live.py`: echter lokaler Live-Spieler, isolierte Spielstände, Gesprächsprotokolle.
- `tests/spieltest_live_batch.py`: serieller Koordinator und Reviewer-Ausgabe.
- `tests/spieltest_rezension.py`, `tests/spieltest_reviewstruktur.py`: Inhaltsreview und Struktur.
- `tests/spieltest_live_speed.py`: dokumentierte, begrenzte Wiederverwendung exakt identischer deterministischer Prüfungen; keine Wiederverwendung freier Figuren- oder Spielertexte.
- `docs/wiki/systeme/spieltest.md`: ausführliche Anleitung und Grenzen.

Originalberichte: `C:\Users\DucNg\Documents\Codex\2026-10-30\wa\outputs`.

Rohdaten, vollständige Dialogprotokolle, Modelllogs und isolierte Teststände:
`C:\Users\DucNg\Documents\Codex\2026-10-30\wa\work\live\abnahme`.
Dort liegen je Profil `lauf-<id>/ergebnis.json`, `dialoge.jsonl`, `modell.jsonl` und Checkpoints, soweit erzeugt.

## Abschluss und weiteres Vorgehen

Die Spielphase wurde wegen der Nutzerfrist um 05:15 Uhr beendet. Um 06:00 Uhr wurden verbliebene eigene Test-/Berichtsprozesse und die eigenen Modellprozesse gestoppt. Beide Automationen sind gelöscht.

**Kein neuer Test- oder GPU-Job ist mit dieser Dateiübergabe beauftragt.** Zuerst Befunde und Belege lesen und einen konkreten Verbesserungsvorschlag ableiten. Parallele fremde Änderungen und produktive Spielstände bewahren; keine Gates oder Referenzen zur Schönung der Ergebnisse umschreiben.

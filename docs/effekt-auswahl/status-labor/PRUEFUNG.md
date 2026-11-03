# Vier Status: Gestaltungstest

Stand: 22.10.2026.

Geschrieben: separate Vergleichsseite mit Brennend, Nass, Erschüttert und Unter Strom; alte dynamische Variante als Referenz; eigene Rückmeldungen im Browser. Quellenmanifest wird ausschließlich durch werkzeuge/eden_rise/status_labor.py erzeugt.

Eingebaut: nur in docs/effekt-auswahl/status-labor. Keine Kampfintegration oder Regeländerung. Vorhandene Auswahl benutzt weiterhin ihren eigenen Speicher.

Getestet: isolierte Kopie unter C:/Users/DucNg/Documents/Codex/2026-10-17/hel/work/effekte/testseite/status-labor, Port 8337. Headless Edge: vier Zustände schaltbar und mit verschiedenen Bildausgaben; Notiz und Bewertung nach Neuladen erhalten; 699 Pixel breite Ansicht ohne seitlichen Überlauf; keine Browser- oder Ladefehler. JavaScript-Syntax geprüft. Screenshots von Feuer, Nass, Staub und Strom visuell geprüft; harte Material- und Texturkanten nachgebessert und Browserprüfung wiederholt.

Quellen: Feuer und Rauch aus mitgelieferten IlluGen-Texturfolgen. Originalfarben des Feuers erhalten; Transparenz aus dem Emissionsbild rekonstruiert. Strom aus eingebetteter Vorschau von lightning_sheet; noch begrenzte Detailauflösung. Nass ist eine Browser-Materialstudie mit Abdunklung und breiten Reflexen, keine Flüssigkeitssimulation. Lichttexturen besitzen weich auslaufende Bildränder.

Der native IlluGen-Feuer-Probeexport liegt in quellen/feuer-probeexport.png. Er wurde tatsächlich exportiert, ist aber stärker stilisiert und wurde deshalb nicht für die neue Feuerdarstellung bevorzugt. Die Darstellung verwendet die detailreichere mitgelieferte Originaltextur. Es wurden keine vier neuen IlluGen-Simulationen erstellt.

Grenzen: subjektive Qualitätsauswahl steht aus; noch keine Prüfung im Kampf; Staub adaptiert eine Rauchfolge; Nässe benötigt für eine endgültige Umsetzung Materialmasken pro Figur. Keine Aussage über Weitergaberechte der mitgelieferten Texturen: deren Lizenz muss vor einer Veröffentlichung geklärt werden.

Offene fremde Änderungen an Engine, Kampfeditor, Musik und weiteren Werkzeugen wurden erhalten. Kein Commit, kein Push, keine Spielstände verändert.

## Feedback umgesetzt

Feuer um 35 Vorschau-Pixel angehoben. Nasse Kleidung kraeftiger abgedunkelt und Reflexe deutlicher gemacht. Nebel hoeher platziert, seitlich driftend und alle 64 Bilder mit weich auslaufender Transparenz versehen. Alle vier Zustaende besitzen eine an der Figur ausgerichtete, weiche Kontur; auch zwischen elektrischen Impulsen bleibt sie sichtbar. Die eigentlichen Entladungen blieben unveraendert.

Erneut in der isolierten Kopie auf Port 8337 geprueft: vier Zustaende, Speichern und Wiederladen der Rueckmeldung, schmale Ansicht, keine Browser- oder Ladefehler. Aktuelle Screenshots aller vier Zustaende visuell geprueft. Alle vier Aussenkanten jedes Nebelbildes auf vollstaendige Transparenz geprueft. Keine Aenderung an der Kampfengine.

## Kategorie D: Reaktionen

Geschrieben: Kurzschluss (D1), Schlamm (D2), Feuersturm (D3), Dampf (D4), Ausbrennen (D5). Gemeinsame Vergleichsseite mit Kategorienwahl; bestehende vier Zustaende bleiben erhalten. Reaktionen verwenden vorhandene Texturen, weiche Konturen und zeitlich begrenzte Uebergaenge. Keine neuen IlluGen-Simulationen. Schlamm ist eine Materialstudie, keine berechnete Fluessigkeit.

Eingebaut: nur separate Vorschau; D ist ueber ?kategorie=reaktionen erreichbar. Getrennter Bewertungsspeicher und Exportname, damit die bereits akzeptierten Zustaende ihre Bewertungen behalten. Keine Engine-, Regel- oder Spielstandaenderungen.

Getestet: isolierte Kopie auf Port 8337 in Edge. Fuenf verschiedene Bildausgaben, Wechsel zurueck zu den vier Zustaenden, getrennte Bewertungen, Wiederladen, JSON-Download, reduzierte Bewegung, schmale Ansicht sowie heller Hintergrund und ausgeblendete Figur. Keine Browser- oder Ladefehler. Screenshots aller fuenf Reaktionen visuell geprueft.

## Freie Formen fuer Nebel und Schlamm

Die runde Unterseite der mitgelieferten Rauchtextur wird nicht mehr verwendet. Stattdessen nutzt staub_frei.png den turbulenten oberen Bereich mit zusammenhaengenden, unregelmaessig wandernden Auslaeufern. Die ovale Schlamm-Bodenmaske wurde durch zwei unregelmaessige Texturschichten ersetzt. Betrifft Nebel bei Erschuetterung sowie alle Rauchanteile der Reaktionen. Feuer, Naesse, Strom und die weichen Figurenkonturen behalten ihre bisherige Gestaltung.

Vorige Fassung unter quellen/formen-vorher gesichert; die Originaltextur bleibt vorhanden. Keine neue Simulation, nur Anpassung der vorhandenen Rauchquelle und der Vorschau.

Geprueft in isolierter Kopie auf Port 8337: beide Kategorien, alle fuenf animierten Reaktionen, getrennte Bewertungen, Export und schmale Darstellung; keine Browserfehler. Aktuelle Screenshots von Nebel, Schlamm und Dampf visuell geprueft. Alle 64 neuen Texturbilder sind verschieden und an allen vier Aussenkanten transparent.

## Erste Vorschauen und naechste Kategorie E

Die Live-Vorschau der urspruenglichen Gesamtauswahl rendert C2 (Nass) und C3 (Erschuettert) jetzt mit kraeftigerer Naesse, weicher Kontur und der freien Nebeltextur. Die Vergleichsseite behaelt links absichtlich die alte Darstellung als Referenz. Bereits gebackene Offline-Flipbooks wurden dabei nicht neu exportiert.

Kategorie E als erste Gestaltungsvorschlaege begonnen: zwoelf Spezialangriffe, getrennte Bewertung und Export. Vorhandene Rauch- und Schnitttexturen werden mit Materialfarben, weichen Lichtkegeln, Bewegung und zeitlicher Abstimmung kombiniert. Kein neuer IlluGen-Export. Insbesondere Ressac und Lame de Fond sind vorlaeufige Materialstudien; keine fertigen Fluessigkeitseffekte. Kampfintegration und Ton sind weiterhin offen.

Browserpruefung in isolierter Kopie: zwoelf unterschiedliche Spezialangriffe laden und animieren; eigene Bewertungen bleiben nach Neuladen erhalten; schmale Darstellung funktioniert; C2 und C3 auch in der Gesamtauswahl geladen. Die bisherigen Zustands- und Reaktionspruefungen erneut erfolgreich, keine Browser- oder Ladefehler. Kontaktbogen der zwoelf Entwuerfe visuell geprueft; Lichtkanten weichgezeichnet und Vorschauzeitpunkt fuer Schnitte verbessert.

## Realismus v3: zwoelf mal drei

36 Materialanimationen mit drei generierten Rasterquellen und Kenney-CC0-Bausteinen. Neue feine Klingenspuren statt gezeichneter Baender. Vollstaendige Quellen, Dateipfade, Grenzen und Testergebnisse: REALISMUS_V3.md. Alle 36 Varianten und sieben Phasen erfolgreich geprueft; Bewertungen inklusive dritter Variante, Neuladen, Exportinhalt, reduzierte Bewegung und schmale Ansicht funktionieren. Bisherige Zustands- und Reaktionspruefungen weiterhin fehlerfrei.

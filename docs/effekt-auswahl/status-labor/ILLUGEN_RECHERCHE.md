# IlluGen: Recherche und Umsetzung

Stand: 22.10.2026. Gelesen wurden öffentlich erreichbare Originalbeiträge und die Herstellerdokumentation. Es wurden weder Community-Mitglieder angeschrieben noch geschlossene Discord-Kanäle gelesen. Es wurden keine fremden Projektpakete gekauft oder heruntergeladen.

## Konkrete Quellen

1. [JangaFX: Exploring and Modernizing The VFX Methods of Diablo 3](https://jangafx.com/insights/diablo-3-vfx-experiments). Der Autor erläutert mehrere scrollende Texturschichten innerhalb einer separaten Formmaske. Wichtig sind weiche Masken, passende Geschwindigkeiten, sinnvolle Skalierungen und ausreichend mittlere Helligkeitswerte. Zu harte Maskendetails bleiben sichtbar stehen; ungünstige Geschwindigkeiten verraten die verschobenen Texturen. Für unsere Vorschau leiten wir daraus ab: Bewegung und Form getrennt gestalten, Materialstruktur behalten und die Transparenz über bewegte Texturen modulieren. Die konkrete Canvas-Adaption und deren Ergebnis sind unsere eigene Arbeit, keine Implementierung aus dem Artikel und kein IlluGen-Export.

2. [Fenix: IlluGen in a Live AAA Pipeline](https://realtimevfx.com/t/illugen-in-a-live-aaa-pipeline-textures-meshes-niagara-systems-in-one-workflow/30729). Der Künstler beschreibt aus eigener Erfahrung die gemeinsame Erstellung von Texturen, Geometrie und Niagara-Effekten in einer Produktionskette mit der Elemental Suite. Er verweist außerdem auf eigene Beispielprojekte. Das ist ein konkreter Erfahrungsbericht des Autors; der öffentlich lesbare Beitrag liefert keine unabhängige Prüfung seines nicht genannten AAA-Projekts.

3. [Fenix: Building Real-Time VFX Assets from Scratch](https://realtimevfx.com/t/illugen-ue5-building-real-time-vfx-assets-from-scratch/30744). Öffentlich dokumentierte Lernserie vom Asset bis zur Verwendung in UE5. Die im Beitrag aufgeführten Beispiele betreffen Schmetterlings-Flipbooks und wachsende VAT-Wurzeln. Daraus folgt keine fertige Vorlage für unsere zwölf Angriffe. Die verlinkte ArtStation-Seite lieferte bei unserem Abruf nur die Anmeldeseite; ihr vollständiger Guide wurde deshalb nicht als gelesen gewertet.

4. [Real Time VFX: WIP demo reel feedback](https://realtimevfx.com/t/wip-vfx-working-on-demo-reel-feedback/27315). Das direkte Feedback empfiehlt einen klaren Auftakt, einen abgestimmten Einschlag und ein schwächeres Auslaufen. Auch Nebeneffekte sollen zum Treffermoment passen. Auf Eden übertragen: Jede Variante hat einen eigenen zeitlichen Ablauf statt einer gleichmäßig laufenden Aura. Das ist eine Empfehlung in diesem konkreten Community-Beitrag, kein nachgewiesener Konsens sämtlicher IlluGen-Anwender.

5. [JangaFX: IlluGen Produktbeschreibung](https://jangafx.com/software/illugen). Der Hersteller beschreibt am Beispiel eines Schwertbogens, wie Geometrie, Kantenmasken und bewegte Materialtexturen zusammenwirken. Für Eden ist dieses Gestaltungsprinzip relevant; die HTML-Vorschau übernimmt keine Unreal-Meshes oder Niagara-Systeme.

6. [JangaFX: Umzug der Community](https://jangafx.com/discourse-shutdown). Das frühere Herstellerforum wurde zugunsten von Discord eingestellt. Die öffentlichen Real-Time-VFX-Beiträge oben sind eine andere, weiterhin erreichbare Community. Die [IlluGen-Dokumentation](https://docs.jangafx.com/illugen/index.html) ist noch im Aufbau und verweist auf Discord, Videos und die vorhandene Node-Referenz.

## Was konkret geändert wurde

- Zwölf einzeln inszenierte Angriffe mit jeweils zwei Varianten. Unterschiede betreffen Richtung, Form, Abfolge und Nachhall.
- Eigene Strömungstextur mit mittleren Dichtewerten und eine separate Transparenztextur; im Browser gegeneinander bewegt. Keine Punktwolken oder Lochmuster.
- Breite strukturierte Schnittkörper, zusammenhängende Wellenkörper mit Schaum, schwenkende beziehungsweise fächernde Lichtwirkungen und versetzte Schattenbilder.
- Beide Varianten laufen synchron; die Zeitleiste ermöglicht den Vergleich von Auftakt, Einschlag und Auslaufen. Reduzierte Bewegung startet weiterhin pausiert.
- Neuer Bewertungsspeicher für die zwei Varianten. Die alten Bewertungen sowie die freigegebenen Zustände und Reaktionen werden nicht überschrieben.

## Grenzen

Die 24 Vorschläge sind lokal erzeugte Canvas-Kompositionen aus eigenen Formen und Materialien mit den vorhandenen Rauchtexturen. Es sind keine 24 neu in IlluGen angelegten Projekte, keine fertigen Flüssigkeitssimulationen und noch keine Kampfintegration. Klang und echte Reaktionen auf Schadensereignisse stehen aus. Ob die Inszenierung Duc gefällt, entscheidet die Auswahl. Technische Browserprüfungen belegen keine künstlerische Qualität.

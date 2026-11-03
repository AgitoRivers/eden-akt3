# K3 Wuchtschlag · Mistral

Drei Varianten im gemeinsamen Ablauf-Labor: wilder Schwung, schweres Ausholen, gegenläufiger Doppelimpuls. Unterbrochene, weich strukturierte Windspuren kreisen links beim gedachten Angreifer und beschleunigen. Beim Auslösen lösen sich die Bahnen in einen kurzen Druckstoß auf. Am Ziel folgen Hurt, stärkerer Rückstoß und abklingendes Rütteln.

Die Windspuren bestehen aus im Browser bewegten Rauschtexturen, ohne gezeichnete Kreisumrisse. Der Nebelkern und der Druckstoß verwenden jetzt eigene, zeitlich bewegte Rauschtexturen mit mehreren Detailgrößen, räumlicher Wirbelverformung, weichen Rändern und feinem mitgerissenem Staub. Der zuvor verwendete native Trefferexport wird für Mistral nicht mehr gezeichnet. Keine neue JangaFX-Simulation; keine Maussteuerung. Der Angreifer ist in dieser Vorschau weiterhin nicht als Figur dargestellt.

Nur Effektlabor Port 8337. Keine Kampfregeländerungen, keine Live-Spielstände verändert. Frühere Tornado-Choreografie im Quellenordner gesichert.

Geschrieben: Wind-Choreografie und drei Varianten. Eingebaut: ausschließlich in der isolierten Ablaufprobe, Repo und bediente Kopie synchron. Getestet: alle drei Varianten in je vier Phasen, unterschiedliche Ausholbewegungen, Hurt bei Treffer und nach 1,1 Sekunden, Effekte-Schalter, keine Browser- oder Ladefehler. Ausholen und Einschlag zusätzlich anhand gerenderter Bilder geprüft.

Überarbeitung 2: Äußere Wirbelbahnen unverändert. Nebelkern, Flugfahne und Einschlag neu gestaltet. Geschrieben und ausschließlich im isolierten Labor eingebaut, beide Kopien synchron. Getestet: drei Varianten in zwölf Phasen ohne Lade- oder Browserfehler; Hurt bleibt erhalten. Bilder von Aufbau, Flug und Kontakt visuell geprüft. 30 Einzelbilder im Headless-Browser ohne GPU: durchschnittlich 13,7 ms, maximal 23,2 ms für den Renderaufruf; dies ist keine Messung der Bildrate im sichtbaren Browser. Keine neue JangaFX-Simulation.

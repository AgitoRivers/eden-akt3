# Expeditionen 2.0 · Entwurf zur Abnahme

> Stand 28.10.2026 · Besitz: Brain Trust · **Entwurf, nicht gebaut.** Anlass: Duc „Alles unter 20 Minuten ist wenig.
> Ich hab mal 2 h in einem Tauchgang verbracht, weil Taktik dich belohnt. Schlechtes Loot mit besserem ausgleichen,
> rasten, leveln, Können muss sich richtig lohnen.“ Pilot: die Grotte. Messwerkzeug: `tests\expedition_sim.py`.

## Ausgangslage (Messung 28.10.2026)

| | heute | Ziel |
|---|---|---|
| Story-Durchgang eines Ortes | 11–27 min | **30–45 min** |
| Freiwillig an einem Ort bleiben | 5–8 min je Wiederholung, immer gleich | **60–120 min**, jeder Lauf anders |
| Züge je Kampf | ~3 | **5–7** |
| Beute | fest je Gegner | Tabellen mit Seltenheit, Können hebt die Seltenheit |
| Niederlagen (kluger Spieler, normale Parade) | 0–3 je Ort | 1–2 je Ort, Rückkehr lohnt sich |

Das Gerüst ist schon da: Niederlage kostet die Beute bis auf ein Stück (`kern/expedition.py`), Rastplätze heilen und
lassen die Gegner zurückkommen, seltene Gegner (`selten`), Beute „eins aus mehreren“ (`eins_aus`). Es fehlt die
Schleife: tiefer gehen, abwägen, mit besserer Beute zurückkommen.

## Die sechs Bausteine

**1 · Kämpfe mit Luft für Taktik.** Gegner ab „gefährlich“ bekommen mehr LP (Richtwert ×1,6), dafür liest man ihre
Absichten länger: Fähigkeiten, Zustände kombinieren (nass + Schock), Ausdauer einteilen und Granaten werden nötig
statt nett. Ziel 5–7 Züge, gemessen mit dem Bot. Lästige Gegner bleiben kurz (Tempo).

**2 · Beute nach Können.** Jeder Gegner hat eine Beutetabelle mit vier Stufen: gewöhnlich (Snacks, kleines Geld),
gut (Stufe-1-Material, Granaten), selten (Module, Stufe-2-Material), meisterlich (Stufe-3-Module, Unikate).
Die Stufe steigt durch **Können**: perfekte Paraden im Kampf, Sieg ohne Treffer, Sieg durch Reden, Schwachstelle
genutzt. Wer gut spielt, sieht es sofort an der Beute.

**3 · Schlechtes gegen Besseres.** Drei gleiche gewöhnliche Funde tauscht Totò gegen einen guten (über Vertrauen, kein
eigener Schmuggel-Strang – E-Regel „Mechaniken verweben“); Rosi zerlegt doppelte Module zu Material.

**4 · Die Serie (umkehren oder weitergehen).** Jeder Kampf ohne Rast erhöht die Serie; alle drei Kämpfe steigt die
Beutestufe um eins. Rasten heilt, aber setzt die Serie zurück und lässt die Gegner zurückkommen. An jedem Rastplatz
die Wahl: heim mit allem, was man hat, oder weiter mit höherer Serie – und bei einer Niederlage bleibt nur ein Stück.
Die Serie steht sichtbar im Expeditionsfenster („Serie 4 · nächster Kampf: gute Beute“).

**5 · Kein Lauf gleicht dem anderen.** Jede Station hat einen Gegner-Pool (2–3 Gegner) statt eines festen Gegners,
Alpha-Fassungen mit 15 %, seltene Gegner mit steigender Chance (wie die Vampirin), kleine Zufallsfunde und Fallen an
den Stationen. Die Story-Szenen bleiben fest.

**6 · Tiefe.** Jeder Ort öffnet nach der Story-Mission tiefere Stufen: Gegner +1 Level, Beute +1 Stufe, ein neuer
seltener Gegner, eine neue Belohnung am Ende. Für die Grotte:

| Tiefe | Was | Wann |
|---|---|---|
| 1 | Ebbe: die Story-Mission um Gennaro | ab Tag 11 |
| 2 | Flut-Nacht: Sirene, Vampirin (gebaut) | nach der Mission |
| 3 | Die versunkenen Gänge: nur mit Tauchausrüstung aus Woche 3, neue Gegner, ein Meister-Fund | nach dem Tauchgang |

## Pilot Grotte – Reihenfolge

| Schritt | Inhalt | Messung (expedition_sim) |
|---|---|---|
| A | Bausteine 1 + 2 + 4: längere Kämpfe, Beutetabellen, Serie | 5–7 Züge; Story-Durchgang ≥ 25 min |
| B | Baustein 5: Gegner-Pools, Alphas, Zufallsfunde | zwei Läufe hintereinander unterscheiden sich sichtbar |
| C | Baustein 3: Tauschen bei Totò und Rosi | – |
| D | Baustein 6: Tiefe 3 „Die versunkenen Gänge“ | nach Woche 3 |

Erst wenn sich die Grotte richtig anfühlt (Duc spielt sie), ziehen Macchia und Berge nach.

## Entscheidungen Duc (28.10.2026)

1. Längere Kämpfe gelten **ab Akt 2** (Kloster und Akt 1 bleiben kurz).
2. Die Serie hebt die Beutestufe **alle zwei Kämpfe**.
3. Tiefe 3 der Grotte: noch offen.
4. Vorher: alle Forks schließen ab, dann **Bestandsaufnahme der Beute** mit den aktuellen Mechaniken und das
   Geldsystem auf den Prüfstand (Duc: „wir sind an einem guten Stand, dass wir Beute definieren können“).

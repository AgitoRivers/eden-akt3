# Eden-Kampf – Effekt-Inventur

Stand 21.10.2026 · abgeleitet aus [kampf.md](../wiki/systeme/kampf.md) (Beschlüsse 19.–21.10.). Noch nichts gebaut.

**Weg:** EG = EmberGen (Feuer/Rauch/Explosion) · IG = IlluGen (Energie, Strahl, Schockwelle, Masken) ·
LG = LiquiGen (Flüssigkeiten) · PT = Partikel in PixiJS (Streifen/Bögen, keine Punktwolken) ·
BL = nur Bewegung, Licht, Bildschirmwackeln, Ton (Engine) · UI = Oberfläche (CSS, schon im Eden-Stil)
**Priorität:** M = muss (erste spielbare Fassung) · S = schön · L = später
**Regeln:** keine Loch-/Tropfen-/Punktmuster (Trypophobie) · Blut nur als roter Streifen/Pulsieren (wholesome) ·
Leuchten nie in die Sprites, immer in der Effektschicht · jeder Effekt hat Ziel, Position, Größe, Dauer, Wiederholung,
Trefferzeitpunkt, vor/hinter Figur, Mischart (additiv/normal), Ton.

## A · Treffer nach Waffenart (Grundbausteine, werden überall wiederverwendet)

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| A1 | Schnitt-Streifen | Klinge | IG (Schnittbogen) + BL | M |
| A2 | Einschlag mit Druckwelle | Stumpf, Faust | IG (Schockwelle) + BL | M |
| A3 | Stich-Blitz | Messer | IG + BL | M |
| A4 | Stoß-Linie | Stange | IG + BL | S |
| A5 | Schuss: Mündungsblitz + Einschlag | Fern | EG (Mündung) + IG | M |
| A6 | Krit-Verstärkung (Zeitlupe, Goldblitz, größer) | jeder Krit | BL + IG | M |
| A7 | Konter nach perfekter Parade | Konter | A1–A5 + BL | M |
| A8 | Trefferblitz am Sprite (Tint) | jeder Treffer | BL | M |

## B · Parade

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| B1 | Ausholen-Signal (goldene Lichtkante) | windup | IG + BL | M |
| B2 | Perfekte Parade (goldener Ring, Funkenbogen) | perfekt | IG + PT | M |
| B3 | Gute Parade (kurzer Ring) | gut | IG | M |
| B4 | Ausweichen (Wischer, blau) | ausweichen | BL + IG | M |
| B5 | Getroffen (roter Rand, Wackeln) | verfehlt | BL + UI | M |
| B6 | Schutzhaltung | Verteidigen | IG (Schild-Schimmer) | S |

## C · Zustände (Auftakt + dezente Schleife; gilt für Gegner und Duc)

| # | Zustand | Bild | Weg | Prio |
|---|---|---|---|---|
| C1 | brennend | Flammen an der Figur | EG (Schleife) | M |
| C2 | nass | glänzender Wasserschimmer, ein Schwall beim Auftakt | LG (Schwall) + IG (Glanz) | M |
| C3 | erschüttert | Riss-Welle am Boden, Staub | IG + EG (Staub) | M |
| C4 | unter Strom | zuckende Blitzbögen | IG | M |
| C5 | blutend | roter Schnitt-Streifen, Pulsieren | IG + BL | M |
| C6 | erschöpft | Figur sackt, matte Aura (weakened-Pose) | BL + IG | M |
| C7 | geschwächt | graue, absinkende Aura | IG | S |
| C8 | geblendet | heller Schleier vor den Augen / Bildrand | IG + UI | S |
| C9 | ungedeckt (Duc) | roter Rand, Herzschlag | UI + BL | S |
| C10 | betäubt | Kreisende Sterne (als Linienbögen) | IG | S |

## D · Reaktionen (Kombination zweier Zustände)

| # | Reaktion | Bild | Weg | Prio |
|---|---|---|---|---|
| D1 | Kurzschluss (nass + Strom) | großer Blitzschlag, Funkenbogen | IG + PT | M |
| D2 | Schlamm (nass + erschüttert) | brauner Schwall am Boden | LG | S |
| D3 | Feuersturm (Brennen + Strom) | Flammenwirbel | EG | S |
| D4 | Dampf (Brennen + nass) | Dampfwolke, zischt | EG | S |
| D5 | Ausbrennen (Brennen + Blutung) | kurze Stichflamme | EG | L |

## E · Spezialangriffe (Name groß einblenden + Effekt; nutzen A–D wieder)

| # | Name | Pfad | Effekt | Weg | Prio |
|---|---|---|---|---|---|
| E1 | Mistral | Kämpfer | Windstoß + Einschlag → erschüttert | IG + C3 | M |
| E2 | Ressac | Kämpfer | Welle von unten | LG/IG | S |
| E3 | Libeccio | Kämpfer | Wind-Aura um Duc (2 Runden) | IG | S |
| E4 | Lame de Fond | Kämpfer | riesige Welle, Finale, Zeitlupe | LG + BL | M |
| E5 | Doppio Gioco | Schmuggler | zwei schnelle Schnitte | A1 ×2 | M |
| E6 | Sotto Voce | Schmuggler | Duc verschwimmt (Unschärfe) | BL | S |
| E7 | Vendetta | Schmuggler | roter Schnitt → blutend | A1 + C5 | M |
| E8 | Omertà | Schmuggler | Bild wird schwarz, ein Schnitt, Stille | BL + A1 | M |
| E9 | Point de Mire | Schütze | Fadenkreuz-Ring → erschöpft | IG + UI | M |
| E10 | Bonaccia | Schütze | ruhige Welle, Bild entsättigt kurz | IG + BL | S |
| E11 | Phare | Schütze | Leuchtturm-Lichtkegel blendet | IG | S |
| E12 | Pluie d'Étoiles | Schütze | drei Lichtbahnen von oben | IG + PT | M |

## F · Gegner

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| F1 | Schwacher Spezialangriff | Buff, Heilung, Debuff | IG (Aura) + BL | S |
| F2 | Starker Spezialangriff – Ankündigung | heavy_windup | IG + BL | M |
| F3 | „Nur ausweichen“-Markierung | Ring-Probe | UI (blau, schon gebaut) | M |
| F4 | Element-Angriff auf Duc | z. B. Feuerspucker | C1–C4 wiederverwenden | M |

## G · Rahmen

| # | Effekt | Weg | Prio |
|---|---|---|---|
| G1 | Heilung (Verbandskasten, Snack) | IG (grüner Schimmer) + UI | M |
| G2 | Sieg / K.o. / Aufgabe | BL + UI | M |
| G3 | Niederlage, Aufwachen an Bord | UI + BL | M |
| G4 | Level-Up | IG + UI | S |
| G5 | Tageswechsel (Sonne, Kapitelname) | UI | S |

## H · Angeln (Minispiel)

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| H1 | Wurf: Schnur-Bogen, Schwimmer landet | Auswerfen | IG (Linie) + BL | M |
| H2 | Biss-Signal (Schwimmer zuckt, Ring) – gleiche Probe wie die Parade | Biss | IG + UI | M |
| H3 | Fang: Wasserschwall beim Herausziehen (Schwall, keine Tropfenwolke) | Fang | LG + BL | M |
| H4 | Seltener Fang: goldener Schimmer, Zeitlupe | Thunfisch, Riesenforelle | IG + BL | S |
| H5 | Fisch entwischt: Platschen, Schnur reißt | Fehlschlag | IG + BL | S |

## I · Erkundung und Sammeln

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| I1 | Fundstelle glänzt (dezenter Lichtschimmer) | Fund-Station | IG | M |
| I2 | Gegenstand fliegt in die Tasche | aufnehmen | UI + BL | M |
| I3 | Tasche voll (Wackeln, rot) | Platz fehlt | UI + BL | M |
| I4 | Seltener Fund (gold, Aufleuchten) | ★★★ | IG + BL | S |
| I5 | Elite voraus (Totenkopf-Puls, Bildrand dunkel) | Elite-Station | UI + BL | M |
| I6 | Rückzug an Bord (Überblendung) | zurück | UI | M |
| I7 | Tod → Aufwachen (Schwarzblende, Bordlicht) | Niederlage | UI + BL | M |

## J · Kochen, Werkstatt, Handel

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| J1 | Brutzeln: Dampf und Hitzeflimmern | kochen | EG (Dampf) + BL | M |
| J2 | Ergebnis: misslungen / gut / meisterhaft (Glanzstufen) | Kochprobe | IG + UI | M |
| J3 | Lieblingsgericht entdeckt (♥ als Linienherz, warmes Licht) | ♥-Treffer | IG + UI | M |
| J4 | Brauner Schleim (dumpfes Blubbern als Wellen, nicht als Blasen) | Regelbruch | LG/IG | S |
| J5 | Werkstatt-Upgrade (Funkenbogen, Waffe glänzt) | Rosi | IG + PT | S |
| J6 | Kauf / Verkauf (eine Münze, kein Münzhaufen) | Laden | UI + BL | S |

## K · Dating und Beziehungen

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| K1 | Vertrauen steigt (warmer Goldschimmer am Porträt) | Vertrauen + | IG + UI | M |
| K2 | Begehren steigt (rosé Schimmer, Herz als Linie) | Begehren + | IG + UI | M |
| K3 | Wert sinkt (kurzes Abkühlen, Blau) | − | UI + BL | M |
| K4 | Geschenk: liebt / mag / mag nicht (drei Reaktionen) | Geschenk | IG + UI | M |
| K5 | Herzensmoment (Vertrauen 5): Bildschirm weich, Licht, Skillpunkt | Meilenstein | IG + UI + BL | S |
| K6 | Romantische Szene: weicher Übergang, Vignette, Lichtpunkte als Streifen | Szenenwechsel | UI + BL | S |
| K7 | Erröten / Lächeln am Porträt (Tint) | Gesten | BL | S |

## L · Tag, Events, Fortschritt

| # | Effekt | Wann | Weg | Prio |
|---|---|---|---|---|
| L1 | Tageswechsel (Sonne geht auf, Kapitelname) | neuer Tag | UI + IG (Licht) | M |
| L2 | Event zwischen den Phasen (Handy vibriert, Gag-Stinger, Bordrat, Duell) | Event | UI + BL | M |
| L3 | Level-Up / Skillpunkt (Lichtsäule) | Aufstieg | IG + UI | M |
| L4 | Uhren-Warnung (Batterie, Diesel kritisch) | Uhr | UI + BL | S |
| L5 | Ruf im Dorf steigt | Ruf + | UI | S |
| L6 | Wetter/Stimmung: Mistral-Wind, Lichterketten bei Nacht | Atmosphäre | IG + EG | L |

## Bilanz

| Weg | Anzahl Effekte (ganz oder teilweise) |
|---|---|
| IlluGen | ~50 – der größte Brocken (Energie, Schnitte, Wellen, Auren, Glanz, Licht) |
| EmberGen | ~10 (Feuer, Rauch, Staub, Mündung, Dampf beim Kochen) |
| LiquiGen | ~7 (Schwall, Welle, Schlamm, Fang beim Angeln) |
| Nur Bewegung/Licht/Ton | ~30 |
| Oberfläche | ~25 (zum Teil schon fertig) |

Insgesamt rund 85 Effekte (A–L), davon ~55 mit Priorität M. Viele sind dieselben Bausteine in anderer Farbe:
**Goldschimmer** (Vertrauen, seltener Fund, Krit, Meisterwerk), **Schwall** (nass, Fang, Ressac), **Ring** (Parade,
Biss-Signal, Point de Mire), **Lichtsäule** (Level-Up, Herzensmoment). Ein Baustein-Satz von etwa 15 Grundeffekten
deckt den Großteil ab.

**Folgerung:** IlluGen trägt mehr als EmberGen. Zuerst also **IlluGen testen**, dann EmberGen; LiquiGen nur, wenn
Schwall/Welle mit IlluGen nicht reichen. Testsatz (6): A1 Schnitt, A2 Einschlag, C4 Blitz, C2 Wasserschwall,
B2 perfekte Parade, C1 brennend.

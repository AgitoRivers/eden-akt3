# Spezialangriffe · Tonvertrag für die Engine

## Stand

Geschrieben: 16 Spezialattacken × 3 Varianten, 32 unverändert kopierte freigegebene OGG-Dateien.
Eingebaut: Ablauf-Labor auf 8337. Keine Änderung an Kampfregeln, Engine oder den normalen Ereignistönen.
Getestet: Mistral-Wiedergabe, Pause/Fortsetzen, Zeitlupe, Stop vor/nach Dekodierung, fehlerhafte Dateien, Cache, alle 16 vollständigen Audiomischungen im OfflineAudioContext und 48 Zeitspuren.

Die endgültige Hörabnahme der zusammengesetzten Abläufe steht Duc noch offen. Einzelne Bausteine sind bereits freigegeben. Die alten drei Klangmischungen wurden aus dem Repository in eine lokale Sicherung außerhalb des Repos verschoben; sie sind keine Laufzeitabhängigkeiten mehr.

## Dateien

- `ton-ablaeufe.js`: Daten, setzt `globalThis.EDEN_ATTACK_SOUND_CUES`.
- `ton-abspieler.js`: DOM-freier Abspieler, setzt `globalThis.EdenAttackSound`.
- `ablaufprobe/klangprobe.js`: ausschließlich Laboroberfläche; im Spiel NICHT laden.
- `assets/attack-sound-v1/`: OGGs, Prüfsummen und Herkunft in `quellen.json`.
- `client/plugins/eden-skills/preview-files.json`: erweitert um beide Laufzeitskripte und sämtliche 32 OGGs. Bestehende Freigaben bleiben erhalten.

**Claude ergänzt die bestehende Vorschau-Route um `.ogg` → `audio/ogg`.** Ohne diese Ergänzung funktioniert die Engine-Route für Ton noch nicht. Die direkte Laborroute auf 8337 liefert die Dateien bereits.

## Zeitbasis und Daten

Alle `offset`-Werte sind **Sekunden ab Sequenzstart**, keine Millisekunden. Jede Spur enthält die aus `probe.js` entnommenen `launch`, absolute `hits` und `duration`.

Ein Ereignis hat `sound_id`, `phase`, `offset`, `gain`. Zusätzliche Ankerdaten (`anchor`, `hit_index`, `delta`) ermöglichen bei übergebenem `timeline` die Neuberechnung gegen die tatsächliche Choreografie:

```
Trefferzeit = library.launches[attack] + 0.38 + library.hits(attack, variant)[i]
```

`window.EdenAttackStudy.soundTimeline()` liefert `{launch, hits, duration}` direkt aus denselben Formeln. Das ist eine zusätzliche Methode; `duration`, `timing()`, `render()`, `selection()` und `actor()` bleiben erhalten. Für Vulcano berücksichtigt der Player auch 1–5 Brandstufen. `mode: "charge"` und `mode: "release"` trennen die beiden Feuerphasen; Standard ist `"full"`.

Aufladung, Auslösen, Treffer und Ausklang sind redaktionelle Phasen der festen Zwischensequenz. Sie reagieren NICHT auf spätere Engine-Ergebnisse. Parade, Block und tatsächliche Zustände bleiben Claudes normaler Kampf-/eden-sfx-Anbindung vorbehalten.

## Aufruf aus dem Spielfenster, außerhalb des iframes

Die beiden Laufzeitskripte können im Spielfenster über die bestehende Vorschau-Route geladen werden. Sie lesen keine DOM-Elemente. Der Aufrufer stellt AudioContext, Zielknoten und Asset-Basis bereit.

```javascript
// Im Spielfenster einmal laden:
// /plugins/eden-skills/preview/ton-ablaeufe.js
// /plugins/eden-skills/preview/ton-abspieler.js
const baseUrl = new URL('/plugins/eden-skills/preview/', location.origin).href;

// Optional vor dem Start vorladen. Decode benötigt keine laufende Audiouhr.
await EdenAttackSound.preload({context, baseUrl, attack: 'mistral', variant: 0});

// context wird im Spielfenster durch die Skill-Klickbehandlung freigegeben:
await context.resume();
const timeline = iframe.contentWindow.EdenAttackStudy.soundTimeline();
const handle = EdenAttackSound.play({
  attack: 'mistral', variant: 0,
  context, destination: combatMasterGain,
  baseUrl, timeline,
  startAt: context.currentTime,
});
await handle.ready; // fehlt eine Datei, wird die gesamte Instanz abgebrochen

// Überspringen, Abbruch, neuer Kampf oder Entfernen der Sequenz:
handle.stop(); // 25 ms Fade, Quellen spätestens 35 ms später stoppen
```

`play()` gibt den Handle synchron zurück. `ready` wartet auf Laden/Dekodieren und Planung. Wird vorher gestoppt, starten später eintreffende Audiodaten NICHT. Bei verspäteter Bereitschaft überspringt der Player bereits vergangene Abschnitte, statt den Ton gegenüber dem Bild zu versetzen. Der Context und der zentrale Zielknoten werden vom Player weder geschlossen noch in der Lautstärke verändert.

Für einen bereits fortgeschrittenen oder fortgesetzten Ablauf: `offset` ist die aktuelle Animationszeit in Sekunden und `startAt` der zugehörige Zeitpunkt der Audiouhr. `speed` steuert die gemeinsame Wiedergabegeschwindigkeit. Bei Zeit-/Tempoänderung den alten Handle stoppen und einen neuen erzeugen. Der Laboradapter erledigt das bereits.

## Bewahrte Schnittstellen

Unverändert: URL-Parameter `angriff` und `einmal=1`, `eden-preview-ready`, `EdenAttackStudy.duration`, der überschreibbare `EdenFigurePicker.mount`-Hook, localStorage `eden-fx-duc-set-v1`, relative Asset-Pfade.

`probe.js` hat nur zwei funktionale Ergänzungen: `soundTimeline()` und ein sofortiges `render(time)` beim Pause/Fortsetzen. Letzteres meldet der bereits vorhandenen Audio-Synchronisation den Pausenzustand, ohne auf einen weiteren laufenden Animationsframe zu warten.

## Freigabepriorität

Jüngere Freigaben überschreiben ältere. Runde 4 gilt für Nachbrennen D, Fokus D, Windböe D sowie Schnittkontakt A/D. Doppio Gioco und Vendetta spielen pro sichtbarem Schnitt genau einen eigenen Kontaktton, abwechselnd A und D. Bei Pluie trägt der dritte Treffer den stärksten Ausbruch. Windschutz, Wasserschild, Fokus und Blendung erhalten keinen Schadens-Impact.

## Prüfen

```
node tests/test_attack_sound.cjs
node tests/test_attack_sound_browser.cjs
```

Der Browsertest benötigt Playwright (`EDEN_PLAYWRIGHT_PATH` falls nicht global auflösbar), Edge und den vorhandenen Laborserver 8337. Er ruft keine Spielstände oder Engine-Routen auf. Die Einzelklänge sind freigegeben; ein technischer Test ersetzt keine abschließende Hörabnahme der Mischungen.

Der ältere `tests/test_skills_preview.cjs` scheitert im aktuellen Showcase bereits an seiner Textannahme: Er erwartet „Omertà“ im Bauhinweis, dort steht inzwischen „Gnadenstoß“. Dieser fremde UI-Text wurde nicht geändert. Der neue Browsertest prüft die 16 freigegebenen Animationsvorschauen direkt, zusätzlich zur Audio-Wiedergabe und den Mischungen.

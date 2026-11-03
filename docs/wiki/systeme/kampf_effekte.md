# Kampf-Effekte – Übergabe

Stand 19.10.2026 · für die Gestaltung der Spezialeffekte (z. B. durch ChatGPT). Der Kampf läuft ohne diese Datei;
Effekte sind reine Darstellung.

## Wo sie andocken

- Datei: `client/plugins/eden-combat/eden-combat-effects.js` (ersetzt den jetzigen Platzhalter).
- Vertrag: `window.EdenCombatEffects = { play(name, anker, info) }`.
  - `name`: einer der Namen unten.
  - `anker`: DOM-Element, an dem der Effekt sitzt (Gegner-Sprite `img.gsprite` oder Ducs Karte `.du`), kann `null` sein.
  - `info`: kleines Objekt mit Zusatzwerten (siehe Tabelle).
- Zusätzlich feuert der Kampf das DOM-Ereignis `eden-kampf-effekt` (`detail: {name, anker, info}`), z. B. für Sounds.
- Die Effekte laufen in einer eigenen Ebene über `#app` (Beispiel im Platzhalter: `ebene()`).

## Regeln

1. **Nie Eingaben blockieren:** `pointer-events:none`, keine Wartezeiten, kein `await` vor dem nächsten Zug.
2. **Timing der Parade nicht verdecken:** Bei `ausholen`, `funke` und `schlag` darf der Effekt den Gegner-Sprite und den
   Zeitpunkt des Schlags nicht verschleiern (kein Vollbild-Blitz länger als 120 ms, nichts vor dem Gesicht des Gegners).
3. **Selbst aufräumen:** jedes erzeugte Element nach spätestens 1,5 s entfernen.
4. **`prefers-reduced-motion`** beachten (dann nichts oder nur ein kurzer Farbwechsel).
5. **Farben aus Eden:** Gold `#d8bd86` (Auswahl, perfekt), Perlweiß `#f3eee4`, Altrosa `#d9a198` (Schaden),
   Salbeigrün `#a8d5b1` (Heilung, gut), Blau `#9db9d6` (Fassung). Lavendel `#B7A4D6` ist für Entdeckungen reserviert.
6. **Format:** reines JS/CSS (Web Animations API) oder transparente WebP-Bildfolgen in
   `client/plugins/eden-combat/fx/` (dann zusätzlich in `eden.py` die Route freigeben – Claude hängt das ein).
7. Größe der Datei: unter 60 KB ohne Bilder.
8. **Neuaufbau überleben (02.11.2026):** Jede Aktion zeichnet den Kampf zweimal neu (Klick und Antwort).
   `EdenCombat.einsetzen` übernimmt dabei die alten Sprite-Knoten (`img.dsprite`, `img.gsprite`) samt laufender
   Animation und die Kinder `.kampf-pop` und `.kampf-codex` von `.kampf`. Eine neue kurze Sprite-Klasse (wie `stoss`,
   `treffer`) gehört in `FLUECHTIG` in `eden-combat.js`, sonst bricht sie beim nächsten Neuaufbau ab. Neue Einblendungen
   gehören entweder an `#app` (wie `ebene()`) oder in die Liste in `einsetzen`.
9. **Sieg nach der Sequenz (02.11.2026):** Beendet ein Spezialangriff den Kampf, zeigt die Bühne bis zum Ende der
   Zwischensequenz den Stand davor (`endeHalten`), und `index.html` hält die Musik an (`EdenCombat.musikHalten`).
10. **Atmen (04.11.2026):** Ducs Ruheposen `idle`, `guard` und `weakened` atmen (Paket idle-guard vom 03.11.). Eine
   Leinwand `canvas.datem` liegt deckungsgleich hinter dem `img.dsprite` und verformt das Bild in Streifen: Oberkörper
   hebt und senkt sich, die Stiefel bleiben stehen (`ATEM` in `eden-combat.js`). Das Bild ist solange unsichtbar
   (`atmet`); andere Posen, `FLUECHTIG`-Klassen und `prefers-reduced-motion` zeigen wieder das Bild.

## Effekt-Namen

| Name | Wann | Anker | info |
|---|---|---|---|
| `ausholen` | Gegner holt aus (Beginn der Parade) | Gegner | `{schwer}` |
| `funke` | Vorwarnung 450 ms vor dem Schlag (Probe „Sprite lesen“) | Gegner | – |
| `schlag` | Moment des Schlags | Gegner | `{schwer}` |
| `parade_perfekt` | perfekte Parade | Gegner | – |
| `konter` | Duc kontert nach perfekter Parade | Gegner | – |
| `parade_gut` | Parade halbiert den Schaden | Gegner | – |
| `parade_ausweichen` | ausgewichen (Ring) | Gegner | – |
| `parade_verfehlt` | Parade verfehlt | Gegner | – |
| `treffer_gegner` | Duc trifft | Gegner | `{schaden}` |
| `treffer_duc` | Duc wird getroffen | Duc-Karte | `{schaden}` |
| `heilung` | Duc heilt (Gegenstand) | Duc-Karte | `{plus}` |
| `fassung` | Fassung des Gegners sinkt | Gegner | `{minus}` |
| `ende_ko` · `ende_aufgabe` · `ende_entkommen` · `ende_flucht` · `ende_niederlage` | Kampfende | Gegner | – |

## Ausprobieren

`python tests\vorschau_server.py --port 8332 --kampf hafen_dieb_test` → `http://localhost:8332`
(oder Eintrag `eden-kampf` in `C:\Users\DucNg\.claude\launch.json`). Spielstände sind Wegwerf-Kopien.

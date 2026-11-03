# Eden – Stilleitfaden der Oberfläche („Deck Glass Noir“)

Stand 30.10.2026 · verbindlich für alle Bildschirme (Dating, Kampf, Erkundung, Kochen, Menüs). Neue Bildschirme
nehmen diese Bausteine und erfinden **keinen eigenen Stil**. Quelle der Werte: `client/index.html` (`:root`, `.glas`,
`.knopf`, `.karte`, `.option`), `client/plugins/eden-ui/` (Icons, Skalen, Status-Knopf, Infokarte) und
`client/plugins/eden-combat/eden-combat.css`.

**Grundidee:** Das Bild ist randlos und trägt die Stimmung (Fotos, Figuren groß). Darüber liegt Rauchglas, Champagner-Gold
ist der einzige Akzent. Oberfläche, Erzählung und Stimmen sind auf Englisch.

**Aus einem Guss (Duc 30.10.2026):** Vorher entstand jedes Fenster für sich: drei Icon-Systeme, 115 Symbole, 40
Schriftgrößen, 26 Radien. Deshalb gelten seit dem 30.10. die neuen Regeln unter „Icons“ und „Ein Muster je Aufgabe“. Der Test
`tests/test_ui_einheit.py` zählt Symbole, Schriftgrößen, Radien und Hexfarben in `client/`. Diese Zahlen dürfen nur sinken.
Icons sind komplett umgestellt. Schriftgrößen, Radien und Hexfarben wandern beim Anfassen auf die Skalen.

![Dating-Oberfläche, Tageswahl](../../ui_bilder/dating_tageswahl.jpg)

## Zentrale Steuerung: Wo ändere ich was?

Alles Gemeinsame liegt in `client/plugins/eden-ui/`. Eine Änderung dort gilt sofort im ganzen Spiel. Nach Änderungen an diesen Dateien die `?v=`-Nummer in
`client/index.html` erhöhen.

| Ich will … | Dort ändern | Wirkt auf |
|---|---|---|
| eine Schriftgröße, einen Radius oder Abstand ändern | `:root` in `eden-ui.css` (`--t-*`, `--r-*`, `--a*`) | alle Bildschirme |
| eine Farbe oder Schriftart ändern | `:root` in `eden-ui.css` | alle Stellen, die das Token nutzen |
| Glas-Panel, Hauptknopf, Namen oder Zahlen ändern | `.glas`, `.knopf`, `.name`, `.zahl` in `eden-ui.css` | alle, die diese Klassen nutzen |
| Abstände ändern | `--a*` in `eden-ui.css` | alle Abstände von 4 bis 36 px |
| die Innenabstände aller Pillen oder Karten ändern | `--pille-klein`, `--pille`, `--pille-gross`, `--pille-knopf`, `--karte-pad-klein`, `--karte-pad`, `--karte-pad-gross` in `eden-ui.css` | alle erfassten Pillen und Karten, im ganzen Spiel |
| ein Emoji vom Server als Icon zeigen | Tabelle `EMOJI` in `eden-ui.js` | jede Anzeige, außer im Handy (dort tippen die Figuren) |
| ein Icon austauschen oder ergänzen | `ICONS` in `werkzeuge/ui_icons.py`, dann `python werkzeuge\ui_icons.py` | jede Stelle mit diesem Begriff |
| Status-Knopf, Infokarte oder Rückmeldung ändern | `eden-ui.js` und `eden-ui.css` | alle Status-Knöpfe |
| die Regeln nachlesen | diese Seite | |

**Noch nicht zentral:** Farbe und Rand von Karten und Pillen stehen je Plugin (nur Radius, Schrift und Innenabstand sind zentral), Abstände über 36 px und unter 4 px sind Einzelwerte, rund 115
Farben und alle Leinwand-Farben ebenso. Eine Änderung daran wirkt nur im jeweiligen Plugin.

**Der Wächter:** `tests/test_ui_einheit.py` läuft auch am Anfang von `tests/lauf_test.py`. Direkte Commits prüft er nicht, einen Git-Hook gibt es nicht.

## 1. Grundlagen

### Farben (Tokens aus `:root`)

| Token | Wert | Bedeutung |
|---|---|---|
| `--ink` | `#07080b` | Hintergrund, Text auf Gold |
| `--rauch` | `rgba(9,11,15,.52)` | Glas-Panel (Standard) |
| `--rauch-stark` | `rgba(9,11,15,.82)` | dichtes Panel, Ergebnis-Fenster |
| `--perle` | `#f3eee4` | Haupttext |
| `--perle-leise` / `--perle-dim` | 70 % / 45 % | Nebentext / Hinweise |
| `--rede` | `#ecd8ae` | direkte Rede im Chat |
| `--akz` | `#d8bd86` (Champagner-Gold) | **Hauptaktion**, Namen, gewählt (Parieren ist seit 03.11. hell/Perle) |
| `--akz2` | `#9db9d6` | Fassung, Neben-Akzent, **Trust** |
| `--begehren` | `#e0707c` (Rosé-Rot) | **nur Desire**: Herz, Ring, Punkte, Pille, Stufenkarte (Duc 03.11.2026). Nicht für Fehlschlag (`--schlecht`) und nicht für Blut (`--rot`) |
| `--gut` / `--schlecht` | `#a8d5b1` / `#d9a198` | eigene LP, Erfolg / Gegner-LP, Fehlschlag |
| `--linie` / `--linie-n` | Gold 26 % / Perle 16 % | Rahmen (Gold für Glas, neutral für Pillen) |
| Ausweichen (Kampf) | `#8ec5ff` | **nur „nur ausweichen“** – nie für etwas anderes |

**Pfadfarben** (Fähigkeiten, Streifen links an der Karte): Kämpfer Terrakotta `#e0895f` · Schmuggler Violett `#b79ae6`
· Schütze Türkis `#6fc7b9` · ohne Pfad `--perle-dim`.

**Bedrohung** (Gegnername relativ zu Ducs Level): Lästig grau · Gefährlich grün · Tödlich orange · Albtraum Totenkopf.
Immer Levelzahl und Wort dazu, nie nur die Farbe.

### Schriften

| Rolle | Schrift | Einsatz |
|---|---|---|
| Namen, Titel (`--f-name`) | **Bricolage Grotesque**, 750, Laufweite −0,02em | Figurennamen, Karten-Titel („Time with Lea“, „Mistral“), große Einblendungen |
| Oberfläche (`--f-ui`) | **Geist** | Fließtext, Erklärungen |
| Zahlen (`--f-zahl`) | **Geist Mono**, tabellarisch | LP, Kosten, Prozent, Tasten |

Titel auf Karten: 24–26 px Gold. Große Einblendungen (Parade, Spezialangriff, Kapitel): 34–44 px.

### Formen

| Baustein | Rundung |
|---|---|
| Großes Panel, Chat | 24–28 px |
| Karte | 20–24 px |
| Knopf, Pille, Chip | 999 px (ganz rund) |
| Tastenkürzel | 8 px |
| Porträt, Zugfolge-Avatar | Kreis |

**Glas:** `background: var(--rauch); border: 1px solid var(--linie); backdrop-filter: blur(20px) saturate(1.15);
box-shadow: 0 18px 50px rgba(0,0,0,.35)` – das ist die Klasse `.glas`; im Kampf `.kampf .rauch` (gleiche Werte).

### Skalen (Tokens aus `eden-ui.css`)

Die ganze Oberfläche nimmt nur diese Werte (seit 30.10.2026 umgestellt, feste Werte zählt der Wächter-Test).

| Skala | Tokens | Werte |
|---|---|---|
| Schrift | `--t-mini` · `--t-klein` · `--t-info` · `--t-text` · `--t-gross` · `--t-unter` · `--t-titel` · `--t-kopf` · `--t-held` · `--t-buehne` · `--t-riesig` | 11 · 12,5 · 14 · 15 · 18 · 20 · 24 · 32 · 40 · 56 · 72 px |
| Rundung | `--r-fein` · `--r-taste` · `--r-mittel` · `--r-karte` · `--r-panel` · `--r-rund` | 4 · 8 · 14 · 22 · 26 · 999 px; Formen: `--r-geraet`, `--r-geraet-innen`, `--r-kopfform` |
| Abstand | `--a1` bis `--a7` | 4 · 8 · 12 · 16 · 24 · 32 · 48 px |

**Farben:** zusätzlich zu den Grund-Tokens oben gibt es in `eden-ui.css`: `--begehren`, `--flaeche`, `--flaeche2`, `--dunkelbraun`, `--grau-hell`,
`--grau`, `--grau-dunkel`, `--gold-hell`, `--gold-dunkel`, `--creme`, `--rot`, `--rot-dunkel`, `--warn`, `--ausweichen`, `--wasser`,
`--pfad-k/s/j/h/m`, `--papier`, `--tinte`. Keine neuen Hexwerte. Noch als Hexwert erlaubt: Farben auf der Leinwand (Effekte, Würfel,
Schießen, dort geht `var()` nicht) und die rund 115 Farben, die sichtbar von jeder Palettenfarbe abweichen und eine eigene Stimmung tragen,
vor allem in Fähigkeiten, Anhörung und Level-Up.

### Icons

**Phosphor Duotone** ist die einzige Icon-Familie (MIT, Version in `werkzeuge/ui_icons.py`, Lizenz in
`client/plugins/eden-ui/LICENSE-phosphor.txt`). Gemalte Bilder für Items, Zutaten und Figuren bleiben, wie sie sind.

- **Ein Begriff, ein Icon:** Das Wörterbuch `ICONS` in `werkzeuge/ui_icons.py` legt jeden Begriff einmal fest. Der Blitz ist
  nur noch Ducs Energie, Strom ist der Stecker. Neues Icon: Zeile ergänzen, `python werkzeuge\ui_icons.py`, im Code
  `EdenUI.icon("name")`.
- **Icon-Namen sind IDs im Dokument:** Der Sprite liegt vorn im `body`. Ein Icon darf deshalb nie heißen wie ein Element der Seite,
  sonst findet `$("name")` das Icon statt des Elements. Das Icon `chat` hieß wie das Chat-Fenster und schob die Figuren an den
  linken Rand (01.11.). Heute heißt es `talk`, `test_ui_einheit` wacht darüber.
- **Größe:** 24 px, in Ringen 22 px, in Text und Pillen 16 px (`EdenUI.icon("name", "klein")`). Die Farbe kommt aus `currentColor`.
- **Stand 30.10.:** Die ganze Oberfläche nutzt das Wörterbuch. In `client/` sind nur noch drei Zeichen übrig: `☠` in `eden-combat.css` (Bedrohung Albtraum) und `💔`, `🤝` in `eden-sfx.js`, die dort Servertexte erkennen. **Noch vom Server:** Emoji in Texten wie „📱 Message from …“, Angriffs-Icons im Kampf (`a.icon`) und Emoji in Modultexten. Das Feld `icon` aus `kern/ermittlung.py` nutzt der Client nicht mehr.
- **Größen je Ort:** `EdenUI.icon("name", "imtext")` wächst mit der Schrift (Minispiele, Kampf-Chips). In Plugins steht `uiIc("name", "klein")` global bereit.

## 2. Bausteine

| Baustein | So sieht er aus | Wo |
|---|---|---|
| **Glas-Panel** | Rauchglas, Goldlinie, weicher Schatten | Duc-Karte, Gegnerkarte, Absicht, Chat |
| **Karte mit Bild** (`.option`) | Bild oben, darunter goldener Titel, Ort/Personen in Gold klein, Text in Perle | Tageswahl, Orte |
| **Karte ohne Bild** (`.fk`) | Pfadstreifen links, goldener Titel, Wirkung 1 Satz, Pillen unten, Taste oben rechts | Fähigkeiten, später Rezepte, Gegenstände |
| **Knopf** (`.knopf`) | Gold, dunkle Schrift, ganz rund; `.leise` = Glas statt Gold | Hauptaktion / Nebenaktion |
| **Befehl** (`.kampf .cmd`) | runde Pille, gewählt = Gold, Taste als dunkles Kästchen | Kampfbefehle 1–5 |
| **Pille** (`.pill`) | kleine runde Marke: Gold = Kosten, Grün = sicher/Erfolg, Blau = Bedingung, neutral = Info | Karten, Zustände |
| **Balken** | 12 px, rund; Duc grün, Gegner rot, Fassung blau | LP, Fassung |
| **Porträt-Kreis** (`.av`) | Kreis mit Goldlinie, das Gesicht liegt je Sprite mittig: `avatar(url)` nimmt den Ausschnitt aus `module/eden_rise/gesichter.json`. Neue oder geänderte Sprites misst `Start-Eden.bat` beim Spielstart selbst (`werkzeuge/gesichter_messen.py --neu`), Wächter `tests/test_gesichter.py` | Chat, Handy, Listen |
| **Ring** (`.ring`) | Fortschritt als Kreis | Uhren, Werte |
| **Status-Knopf** (`EdenUI.status`) | Icon im Ring, der Ring zeigt den Füllstand. Niedrig = Rot und „!“ | Kopfzeile |
| **Infokarte** (`.ui-infokarte`) | Icon, Name, Zustand, Balken, ein Absatz Text | Klick auf einen Status-Knopf |

### Ein Muster je Aufgabe

| Aufgabe | Immer so | Nie |
|---|---|---|
| Wert zeigen | Status-Knopf. Der Füllstand steht immer im Ring, für jeden Wert gleich | für jeden Wert eine eigene Anzeige |
| Wert erklären | Klick öffnet die Infokarte. Schließen per Klick daneben, Esc oder zweitem Klick | Erklärung nur im Tooltip, großes Extra-Fenster |
| Name zeigen | Hover zeigt den Namen. Unklare Icons tragen den Namen sichtbar, solange der Spieler sie lernt (Kopfzeile: Tag 1–2) | Bedeutung nur per Hover |
| Änderung melden | Puls, aufsteigende Zahl (`+1`), kurz Name und Zustand. Reduzierte Bewegung wird beachtet | stille Änderung, je Wert eine andere Animation |
| Zustand anzeigen | Farbe **und** Form oder Wort | nur Farbe |

**Kopfzeile (`#zeitpille`, Duc 30.10.2026):** eine Leiste mit Tag, Phase, Geld, Ziel und den Knöpfen Crew Mood, Village
Reputation und Energy. Das Gesicht folgt der Stimmungsstufe (`mood-*`). Die zweite Leiste und das Fenster „Yacht & supplies“
sind weg. Spielmomente wie Kampf und Anhörung blenden die Leiste aus, in der Expedition fehlen nur die Knöpfe.
Test: `tests/test_ui_kopfzeile.py`.

**Figur vor Oberfläche (Duc + Brain Trust 01.11.2026):** Wer im Bild steht, besitzt das Bild. Vorbild: Mass Effect, im Gespräch verschwindet das Kampf-HUD.

| Wo | Figur | Oberfläche |
|---|---|---|
| Ortsbild mit 1 Figur | 92 % der Fensterhöhe, rechts | Duc-Karte weg |
| Ortsbild mit 2 Figuren | 80 % | Duc-Karte weg |
| Ortsbild mit 3 oder 4 Figuren | 72 % | Duc-Karte weg |
| Ortsbild ohne Figur | – | Duc-Karte bleibt |
| Gag und Abend (eine Figur) | 92 %, dieselbe Bühne, Text links | Klasse `.ev.mit-solo` in `client/index.html` |
| Crew Council, Duell, Gag-Varianten | klein, wie bisher | Crew Council läuft bei 1366×768 noch über den Fensterrand |
| Karten im Reiter Relationships | Kopf aus `gesichter.json`: gleich groß, gleich hoch, mittig (`ausschnitt` in `eden-menu.js`) | zwei ganze Reihen passen ins Fenster |

Ist das Leben nicht voll, zeigt die Ortskarte im Gespräch einen schmalen Balken. Wegkarte und „Found on the way“ erscheinen erst, wenn die Expedition läuft. Im Ortsbild liegt die Antwort direkt auf der Szenenkarte, ohne zweite Glasfläche. Code: `client/plugins/eden-expedition/`.

## 2b. Bewegung und Übergänge (Duc 02.11.2026)

Vorbild sind die Bühnenkarten im Curtain-Look (`#buehnenkarte`, Klassen `szk-*` in `client/index.html`): Zwischenkarte vor
einem Event, Tageskarte, Ergebnis-Screen am Gesprächsende. Duc: „Mit dieser Idee können wir noch mehr Elemente optimieren.“
Neue Animationen folgen diesen Werten, damit sich alles gleich anfühlt.

**Grundsätze**
- **Bewegung erklärt etwas:** woher etwas kommt, wohin es geht, was sich geändert hat. Reine Deko-Bewegung gibt es nicht.
- **Rein langsamer als raus:** Eintritt mit Abbremsen (ease-out), Austritt mit Anlauf (ease-in), Austritt etwa 75 % der Eintrittsdauer.
- **Nacheinander statt alles auf einmal:** Teile einer Karte kommen gestaffelt. Die Staffel bleibt kurz, insgesamt unter einer Sekunde.
- **Zahlen zählen, sie springen nicht:** Werte laufen sichtbar hoch und enden mit einem kleinen Pop.
- **Jeder große Moment hat einen eigenen Klang**, kleine Rückmeldungen höchstens einen leisen. Nie zwei Klänge übereinander.
- **Weniger Bewegung wird immer beachtet** (`prefers-reduced-motion`): Dann gibt es nur Überblenden oder gar keine Animation, die
  Information bleibt gleich (Zahl steht sofort da).
- **Gesperrte Knöpfe bewegen sich nicht**, sie sind nur gedimmt.

**Werte**

| Was | Dauer | Kurve | Wo im Code |
|---|---|---|---|
| Rückmeldung auf Klick, Fokus | 100–150 ms | ease-out | Knöpfe, Pillen |
| Zustand wechselt (Menü, Reiter, Tooltip) | 200–300 ms | ease-out | |
| Karte über die Bühne | 550 ms rein, 420 ms raus | ease-out / ease-in | `szkRein`, `szkRaus` |
| Teile einer Karte | je 700 ms, Start 300 ms + 130 ms je Teil (`--i`) | `cubic-bezier(.16,1,.3,1)` (`--szk-kurve`) | `.szk-teil` |
| Bild hinter der Karte | 9 s langsamer Zoom von 107 % auf 100 % | ease-out | `szkBild` |
| Zahl zählt hoch | 900 ms nach 750 ms Pause, kubisches Abbremsen | | `karteZaehlen` |
| Pop am Ende der Zahl | 500 ms, kurz auf 116 % | `--szk-kurve` | `szkPop` |

**Klänge der Karten** (`module/eden_rise/sfx.json`): Vorhang am Gesprächsende `szene_vorhang` (K5), Zwischenkarte `szene_bruecke`
(K11), Tageskarte `tag_karte` (K1). Der Event-Jingle kommt bei einer Zwischenkarte erst nach „Go on“.

**Gebaut (02.11.2026):** 1 bis 4 im Plugin `client/plugins/eden-bewegung/` (Showcase `docs/abnahme/bewegung/index.html`). Trust ist der Smiley `mood-good` in Blau (`--akz2`), Desire das Herz `love` in Rot (`--begehren`, seit 03.11.2026, vorher Gold), wie die Punkte der Beziehungskarte; keine technischen Etiketten wie „TRUST · LEVEL UP“. Wahl per Zahlentaste bekommt keine Wahl-Animation.

**Kandidaten im selben Stil** (Recherche 02.11.2026, 1 bis 4 gebaut, Reihenfolge ist ein Vorschlag):

| # | Element | Idee |
|---|---|---|
| 1 | **Stufe steigt** (Vertrauen/Begehren) | Der größte Moment der Beziehung: Ring füllt sich, Zahl springt mit Pop, kurzer eigener Klang, Name der Stufe groß. Heute nur eine Zeile |
| 2 | **Wert ändert sich im Gespräch** | Pille mit Zahl („+2 Trust“) steigt neben dem Kopf der Figur auf, steht kurz und fliegt zur Beziehungskarte (gebaut 03.11., siehe 2c) |
| 3 | **Antwort gewählt** | Gewählte Option bleibt kurz stehen und leuchtet, die anderen blenden aus (wie Persona) |
| 4 | **Gefühl wechselt** | Sprite überblendet in 150 ms statt hart zu springen; wer spricht, ist hell, die anderen leicht gedimmt |
| 5 | **Gegenstand bekommen / Geschenk** | Symbol fliegt in die Tasche, Tasche zuckt kurz |
| 6 | **Handy-Nachricht** | Handy gleitet unten rein und vibriert einmal, statt einer Meldung |
| 7 | **Erwischt** (Orte mit Risiko) | Klopfen: Bild ruckelt kurz, Klang, dann die Zeile des Störers |
| 8 | **Neuer Codex- oder Journal-Eintrag** | Eintrag glüht einmal auf, Symbol im Dock pulst einmal |
| 9 | **Tageszeit vergeht** | Uhr in der Kopfzeile dreht sich zur nächsten Phase |
| 10 | **Knopf gedrückt** | 100 ms leicht kleiner, dann zurück; nichts bei gesperrten Knöpfen |

Quellen der Recherche: [Motion Design (Impeccable)](https://git.secluded.site/agent-skills/blob/main/vendor/impeccable/skill/reference/motion-design.md),
[How to add juice to your UI](https://bugnet.io/blog/how-to-add-juice-to-your-ui), [Micro-interactions](https://skills.cat/skills/dylantarre/animation-principles/micro-interactions),
[Persona-UI](https://gamegeeker.com/news/persona-ui-origin-budget-driven-design). Die Zahlen sind Richtwerte, im Spiel nachprüfen.

## 2c. UX-Paket „Schliff außerhalb des Kampfs“ (03.11.2026)

Aus dem UX-Benchmark (`X:\AI\Eden_Review\ux_benchmark\bericht.md`, Vorschläge 4, 5, 6, 18–20, 22, 23, 25). Neue Muster, die ab jetzt überall gelten:

| Muster | So sieht es aus | Wo im Code |
|---|---|---|
| **Beziehungsring** | Status-Knopf-Ring statt Punktreihe: Smiley (Trust, `--akz2`) oder Herz (Desire, `--begehren`) im Ring, der Ring füllt Stufe + Anteil, daneben klein „TRUST“ und das **Stufenwort**. Klein (32 px, ohne Wort) für Nebenfiguren | `bezRing()` und `STUFEN_WORT` in `client/index.html`, genutzt im Reiter Relationships |
| **Stufenwörter** | Trust: Stranger · Polite · Friendly · Close · Trusted · Loyal. Desire: Cool · Curious · Flirty · Attracted · Wants you · All in (Stufe 0–5) | `STUFEN_WORT` in `client/index.html` |
| **NEW-Marke** | Kleine Pille mit Goldrand und Goldschrift „NEW“, **nicht** gold gefüllt (die eine goldene Fläche je Bereich bleibt frei) | `.neu-marke` in `client/index.html` |
| **Werte auf der Tageskarte** | Unten links im Bild eine Glas-Pille: Smiley + Trust-Stufe, Herz + Desire-Stufe, dazu NEW, wenn heute eine Leiter-Szene kommen kann oder eine Stufe mit einer Begegnung erreichbar ist (Anteil ≥ 75 %, nicht auf Stufe 2, ab Stufe 3 erst nach dem Stufen-Abstand) | `wahlWerteHtml()` in `client/index.html`, Server `ereignisse.heute_neu()`, Feld `personen` an jeder Option |
| **Stimmung statt Regel** | Unter der Frage der Tageswahl steht ein Stimmungssatz je Phase („Slow afternoon. Who do you look for?“). Die Regel steht in einer Infokarte hinter dem Uhr-Knopf neben den Aktions-Punkten | `STIMMUNG`, `regelHtml()` in `client/index.html` |
| **Wert-Pille mit Zahl** | „+2 Trust“ steigt 0,4 s neben dem Kopf auf, steht 0,7 s, fliegt 0,8 s zur Beziehungskarte (gesamt 1,9 s). Bei weniger Bewegung steht sie still und blendet aus. Die Zahl sind Punkte (0–100); die Zeile „Trust Lea ↗“ im Chat bleibt als Verlauf | `pilleFliegt()` in `client/plugins/eden-bewegung/`, Felder `v_punkte`/`b_punkte` in `z.werte` und an jeder Figur in `z.szene.buehne` (so auch für Jana, Megan und alle ohne Romanze) |
| **Hinweis neben dem Bedienelement** | Ein Lernhinweis liegt **nie** über Knöpfen oder Chips, sondern daneben, mit Pfeil zum Element. Der Erkunden-Hinweis steht links neben dem Chat auf Höhe der Eingabezeile | `#ermhinweis` in `client/index.html` |
| **Antworten unter der Sprechblase** | Im Laden und in der Kombüse stehen Buy/Sell/Goodbye direkt unter der Sprechblase. Ist ein Reiter offen, wandert das Gespräch nach links, die Figur steht mittig zwischen Gespräch und Panel und wird nie verdeckt. Bis acht Waren gibt es immer volle Reihen: bis 4 Waren 2 Spalten, 5–6 Waren 3, 7–8 Waren 4 (zwei Reihen, kein Scrollen). Das Panel ist nur so breit wie die Spalten, damit mehr Figur zu sehen ist; ab neun Waren das breite Panel mit Scrollen (Duc 03.11.2026). Tasten 1–9 und Esc gehören nur dem Laden | `.ort-gespraech` in `client/index.html` (Grundwerte `.ort-*` in `eden-combat.css`) |
| **Map: große Kacheln** | Kacheln mindestens 400 px breit, Höhe so, dass zwei Reihen den Bildschirm füllen. NEW an Orten mit neuer Ware oder einer anderen Person seit dem letzten Besuch (gemerkt je Lauf im Browser) | `.em-orte`, `.em-ort` in `eden-menu.css`, `ortNeu()`/`ortMerken()` in `client/index.html` |
| **Bilder vorladen** | Figuren- und Ortsbilder der Menüs (PNG um 2 MB) lädt der Client vor, wenn er Zeit hat. Sonst öffneten Relationships und Map mit leeren Karten (Lola, Petru im Review) | `bilderVorladen()` in `client/index.html` |

**Gold-Disziplin im Character-Reiter:** „Spend N points“ ist die einzige goldene Fläche bei den Attributen; die sechs „+1“ sind leise Pillen und werden erst beim Zeigen gold. Der Skill-Knopf ist nur gold, wenn Punkte offen sind („Spend 1 point in the skill tree“), sonst leise.

**Story-Entscheidung:** Etikett „Decision“; Optionen ohne Probe zeigen keinen Platzhalter-Kreis mehr. Der Chance-Kreis bei Proben bleibt rund (vorher zog `.wahlb span{flex:1}` ihn zum Oval).

## 3. Regeln

- **Gold heißt: das ist die Hauptsache / hier drücken.** Pro Bereich höchstens eine goldene Fläche.
- **Blau `#8ec5ff` heißt ausschließlich „nur ausweichen“** (Titel, Ring, Knopf). Parieren ist hell/Perle, Gold nur Ducs Hauptaktion (Kampf lesen, 03.11.2026).
- **Tasten:** Befehle 1–5, in Listen 1–9, Esc schließt, Leertaste = Parieren, D = Ausweichen. Jede Taste steht sichtbar
  am Element.
- **Begriffe:** Zustand des Gegners „erschöpft“ (nicht „offen“), eigener „ungedeckt“; Attribute Kraft, Charisma,
  Empathie, Wahrnehmung, List, Mut.
- **Trypophobie-Check ist aus (Duc 03.11.2026).**
- **Effekte** (Feuer, Blitz, Schwall, Schnitt …) sind **keine CSS-Formen**, sondern Flipbooks/Partikel in der
  Effektschicht – siehe [EDEN_KAMPF_EFFEKTE_INVENTUR.md](../../archiv/EDEN_KAMPF_EFFEKTE_INVENTUR.md). Leuchten nie in Sprites.
- **Spielmomente dürfen eigen sein:** Kampf, Anhörung und Sturm behalten ihre Stimmung, nutzen aber dieselben Icons und Skalen.
- **Wholesome:** Blut nur als roter Streifen, keine Spritzer.
- Nur Desktop (1366×768 bis 1920×1080).

## 4. Bildschirme (Stand)

### Kampf – Grundstil (fertig, Commit a824b8c)
Glas-Panels, goldene Namen, Befehle als Pillen, Zugfolge als Glas-Pille, Absicht als Glas-Karte.
![Kampf Grundstil](../../ui_bilder/kampf_grundstil.jpg)

### Parade-Probe (fertig)
Großer Titel, Erklärung als Glas-Pille darunter, Glasleiste mit hellem Kern. Hell/Perle = parieren, Blau = nur ausweichen,
bei Wahl beide Knöpfe (Ausweichen blau umrandet, Parieren hell/Perle). „lieber würfeln“ ist ausgeblendet.

| Parieren | Nur ausweichen | Wahl |
|---|---|---|
| ![](../../ui_bilder/parade_parieren.jpg) | ![](../../ui_bilder/parade_ausweichen.jpg) | ![](../../ui_bilder/parade_wahl.jpg) |

### Fähigkeiten-Menü (fertig)
Karten im Raster, „Immer verfügbar“ als eigene Reihe (Reden, Beruhigen, Einschüchtern).
![Fähigkeiten](../../ui_bilder/kampf_faehigkeiten.jpg)

### Als Nächstes im selben Stil
Gegenstände-Menü als Karten · Zustände am Gegner (Pillen mit Symbol, Effekt aus der Effektschicht) ·
Spezialangriff-Einblendung (Name groß in Gold) · Ergebnis-Fenster · Erkundung (Stationen-Karte, Tasche) · Kochen
(Rezept-Karten) · Tageswechsel.

## 5. Offen

- Umschalter „Parade: Reaktion/Würfeln“ in der Zugfolge entfernen, sobald die Regeln umgebaut werden.
- Effekt-Werkzeuge testen (IlluGen zuerst, dann EmberGen, LiquiGen nur bei Bedarf).
- Die drei verworfenen Codex-Entwürfe wurden am 21.10. gelöscht; nicht wieder als Vorlage heranziehen.

# Übergabe: Taktik-Karte der Belagerung

Stand 31.10.2026, Commit `c1b74759` auf `master`. Für den Agenten, der hier weitermacht. Duc spricht Deutsch, alle Texte im Spiel sind einfaches Englisch.

## Worum es geht

Eden Rise ist ein RPG von Duc, Repo `X:\AI\Eden`. Die Belagerung an Tag 21 ist der Höhepunkt von Akt 2 und wird eine Karte wie in *Fire Emblem*, rund eine Stunde lang: Duc schiebt Trupps, nur er selbst kämpft im echten Kampfbildschirm. Die Karte ist spielbar, hängt aber **noch nicht im Kalender**.

## Zuerst lesen

| Datei | Warum |
|---|---|
| `docs/wiki/systeme/taktik.md` | Alle Regeln der Karte, aktuell |
| `docs/wiki/welt/belagerung.md` | Drama in 9 Schritten, offene Story-Punkte, Sammlung der Vorbereitungen |
| `docs/wiki/welt/dorf_figuren.md` | Pascal, Abschnitt „Auffliegen und Ende“ (E-103) |
| `docs/wiki/systeme/ui_stil.md` | Pflicht vor jeder UI-Arbeit |
| `docs/wiki/STIL.md`, `docs/wiki/START.md` | Pflicht vor jedem Spieltext |
| `docs/brain_trust/ENTSCHEIDUNGEN.md` | E-102, E-103 |
| `C:\Users\DucNg\.claude\projects\C--Users-DucNg\memory\MEMORY.md` | Ducs Arbeitsregeln, falls dein Konto den Ordner lesen kann |

## Code

| Datei | Inhalt |
|---|---|
| `kern/taktik.py` | Alle Regeln, Einstieg `beginnen`, Ansicht `ansicht` |
| `werkzeuge/eden_rise/taktik_eden_rise.py` | Raster, Trupps, Feinde, Wellen, Szenen, baut `module/eden_rise/taktik.json` |
| `client/plugins/eden-tactics/` | Bildschirm. Nach Änderung `?v=` in `client/index.html` erhöhen (jetzt css 8, js 9) |
| `eden.py` | Aktion `taktik`, Porträts der Karten, Rückkehr aus dem Kampf |
| `tests/test_taktik.py` | Regeltests und Bots |
| `tests/vorschau_server.py` | `--taktik`, `--taktik-welle 2`, alle Hilfstruppen und Trupps sind dort verdient |

Vorschau über `.claude/launch.json` in `C:\Users\DucNg`: `eden-taktik` (Port 8378, Aufstellung), `eden-taktik-w2` (Port 8438, Welle 2). Gerade läuft keine davon.

## Was gebaut ist

- **Aufstellung:** Seitenleiste links, 13 eckige Plätze, Figuren und Karten ziehen, Tausch auf besetztem Platz. Gesichter der Truppenführer.
- **Trupps:** Duc, Mr. Maximum, Chiara, Wolff. Verdient: Elsa, Rosi, Yamamoto, Danzel. Höchstens sechs. Bürgerwehr Pascal, Petru, Alva fest.
- **Support:** drei Plätze, Holm fest, zwei frei aus Sophia, Lola, Lea, Siri, Ligeia.
- **Gelände:** frei, Wald, Berg, Strand, Kirchentreppe. Gangarten Fuß, Schwer, Tier, Maschine, Flug. Wald versteckt.
- **Kampf:** Break, Doppelangriff, Fernkämpfer ohne Gegenschlag direkt daneben, Rifleman, Chiaras Taser-Gewehr, exakte Bedrohung (Taste R, Gelände Taste T).
- **Wellen:** Boots-Nachschub mit Countdown, Welle 2 mit vier brennenden Häusern, Welle 3 mit Pascals Verrat.
- **Mr. White:** Bewegung 2, unbesiegbar, bis Petrus Trupp in Runde 6 gefallen ist. Danach kommt Casanova, dann der echte Kampf.
- **Spektakel:** Machtleiste mit großen Momenten, Duo-Sprüche, drei Rücksprünge („Rethink“).

## Duc hat entschieden

- Neustart ab Beginn der Welle, gegen White direkt neu. Kirche 3 Leben.
- Alva ist nur bewusstlos, das zeigt die Sieg-Szene.
- Pascal wechselt offen die Seite, verschwindet, steht im Finale von Akt 3 neben Alon. Nonna bekommt eine Kiste mit Brief und Kellerschlüssel.
- Oberfläche nach `ui_stil.md`, eckige Plätze und Figuren.
- Figuren im Chibi-Stil, siehe unten.

## Nächster Schritt: Figuren

Duc erzeugt drei Probefiguren selbst in DALL·E: Mr. Maximum, Agent, Boarding Robot. Er schickt die Bilder, dann:

1. Auf Lesbarkeit bei etwa 36 px Höhe prüfen.
2. Als Probe auf die Karte setzen, Füße im Feld, Kopf ragt 1,5 Felder hoch, Export 160 x 240 px, transparent. Die Team-Farbe kommt als eckige Bodenplatte per CSS. Pascal wechselt beim Verrat nur die Platte.
3. Duc das Ergebnis per Screenshot zeigen, danach Prompts für die übrigen rund 16 Figuren schreiben.

Rasterfeld: 80 px im Kartenbild, 24 px bei 1366x768, rund 34 px bei 1080p, 45 px bei 1440p. Die Prompts hat Duc im Chat erhalten:

```text
Use the attached map only as a style reference: same warm painted look, same soft sunlight from the upper left. Single chibi game character for a tactical RPG map, full body, about 3 heads tall, seen from slightly above and from the front. A huge, very broad bald Black wrestler with big arms and a confident stance. Golden wrestling trunks, a large gold and black champion belt, black fingerless fighting gloves, bare feet, one fist raised. He must read clearly as the widest and strongest figure even at very small size: simple strong silhouette, clean shapes, little fine detail. Whole figure in frame, feet fully visible, nothing cut off. Transparent background, no ground, no shadow, no base, no text.
```

```text
Use the attached map only as a style reference: same warm painted look, same soft sunlight from the upper left. Single chibi game character for a tactical RPG map, full body, about 3 heads tall, seen from slightly above and from the front. A slim male secret agent with short dark hair, black sunglasses, a clear earpiece, a black suit, white shirt, thin black tie, black gloves and polished black shoes. He holds a short black baton low in one hand, in a calm, ready stance. Simple clear silhouette that reads at very small size, clean shapes, little fine detail. Whole figure in frame, feet fully visible, nothing cut off. Transparent background, no ground, no shadow, no base, no text.
```

```text
Use the attached map only as a style reference: same warm painted look, same soft sunlight from the upper left. Single chibi-proportioned combat robot for a tactical RPG map, full body, seen from slightly above and from the front. A short, wide, heavy boarding machine shaped like a walking steel box: thick square shoulders, short stubby legs, big blocky clamp hands, one small red light as its face. Painted dark graphite with a few white panel edges. Smooth solid armour plates only: no vents, no grilles, no mesh, no holes, no rivets. It must read as slow and very tough even at very small size: simple strong silhouette, clean shapes. Whole figure in frame, feet fully visible, nothing cut off. Transparent background, no ground, no shadow, no base, no text.
```

## Danach: Stufe 4, Einbindung

Vorher mit Duc klären, das berührt die Story:

- Kriegsrat in Phasen: Megan an Tag 15, Holm erst ab Tag 18, weil sie vorher fehlt.
- Vorbereitungen lösen je einen konkreten Moment auf der Karte aus (Mass Effect 2), Sammlung in `belagerung.md`.
- Kalender-Einstieg an Tag 21, Übergang nach Akt 3, Bericht nach der Schlacht.
- Rosis Übergabe-Szene für das Taser-Gewehr, ab Tag 15.
- Folgen abgebrannter Häuser, Flags `tk_haus_weg_<id>`.
- Kampfszene der Crew mit Sprites, überspringbar.

## Offen bei Duc

- Was Pascal im Finale neben Alon tut.
- Mochi taucht früher auf, als `rt_pfote` und Akt 3 vorsehen. Abgleichen.
- Viele echte Kämpfe könnten die Spielzeit dominieren. Erst messen. Falls zu viele: Duc greift Kleinvieh per Schnellkampf an. Das ändert Ducs Regel, also nur mit seinem OK.
- Die Stunde Spielzeit ist nicht gemessen, nur ein Bot-Wert von 24 Runden. Duc konnte selbst noch nicht spielen.

## Nicht geprüft

- **Im Browser nie geklickt:** Rifleman, Taser, Doppelangriff, Lola, Lea, Siri, Ligeia, Rethink, Reserve-Trupps, das Drama von Welle 3 am Stück, Mochi, Sieg und Niederlage. Das ist alles nur per Test abgesichert.
- **Balance:** Der kluge Bot gewinnt in 24 Runden mit 2 Kirchenleben, der naive verliert in Welle 3. Die Bots gewinnen jeden echten Kampf und nutzen weder Support noch Macht. Die Zahlen sind erste Werte.
- **Gelände:** aus einer Farbanalyse, einzelne Felder können falsch liegen. Die Hauspositionen in Welle 2 sind von mir geschätzt.
- **Kampf-Hintergrund:** Auf einem Screenshot wirkte er wie ein Maschinenraum, obwohl der Platz eingestellt ist. Ungeklärt.
- **Texte:** alle Szenen, Duo-Sprüche und Rufe sind unvertonter Entwurf.

## Arbeitsregeln, die hier schon wehgetan haben

- **Shared Index:** Mehrere Sitzungen teilen den Git-Index. Nie in den gemeinsamen Index stagen. Eigener `GIT_INDEX_FILE`, `read-tree HEAD`, nur eigene Dateien `add`, `commit-tree`, prüfen, dass HEAD sich nicht bewegt hat, `update-ref`, danach `update-index` im gemeinsamen Index. `client/index.html` ist von anderen geändert: Blob aus `git show HEAD:client/index.html` plus eigene Ersetzung bauen.
- **Gate:** `tests/lauf_test.py` meldet im Arbeitsordner gerade Abweichungen, weil dort fremde, unfertige Texte liegen. Sauber prüfen: `git worktree add --detach`, dort `module/eden_rise/figuren` löschen und als Junction auf das Original legen, `eden-config.json` kopieren, Gate laufen lassen, **Junction zuerst mit `rmdir` entfernen**, dann Worktree entfernen. Bei `| tail` den Exit-Code beachten, sonst fällt eine Abweichung nicht auf.
- **Python:** `X:/AI/ComfyUI_krea2/python_embeded/python.exe`, `PYTHONUTF8=1`. Skripte mit Backslashes per Datei, nicht per Heredoc.
- **Nie pushen**, das Repo hat keinen Remote. Commit-Trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **Vorschau:** nur den eigenen Port beenden.
- **Vertonung** nur über `Vertonen_EdenRise.bat`, Romanzen-Vertonung erst ganz am Ende.
- **Vorher fragen:** kostenpflichtige API-Läufe, Massen-Aktionen, neue Story-Entscheidungen. Keine Frage-Kästen, im Gespräch fragen und immer einen Vorschlag mitgeben.
- **Mechanik** sofort ins Wiki. Keine Hexfarben außer den Tokens, Wächter `tests/test_ui_einheit.py`.
- **Trypophobie:** keine Loch-, Waben- oder Punktmuster in Bildern und Effekten.

## Grenze bei Bildern

Ich habe keine expliziten Sprites erzeugt und auch keine neuen Bilder von Lola, Lea und Jana, weil sie auf den Bildern sehr jung wirken. Das habe ich Duc so gesagt. Auf der Karte nutzen sie nur vorhandene neutrale Porträts. Die Figuren-Prompts für die Karte umfassen sie als Support ohne eigene Figur nicht.

## Sonst noch liegen geblieben, nicht Teil dieser Aufgabe

Hauptsprites pausiert (Megan, Holm offen) · Sprite-Automatik nur als Plan · Red-Trio-Frist auf Tag 16 und `FOLGE_TAGE` auf Tag 28 · Festa-Events ans Ende von Akt 3 · `test_sprite_stimmung` rot durch `hk_tipp_*` Rosi amusement aus einer anderen Sitzung.

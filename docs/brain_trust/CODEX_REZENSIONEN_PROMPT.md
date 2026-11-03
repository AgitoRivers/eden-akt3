# Auftrag an Codex: bessere Eden-Rise-Rezensionen und bessere Testläufe

Stand 31.10.2026. Du arbeitest in `X:\AI\Eden`. Andere Sitzungen arbeiten parallel im selben Ordner.

## Ziel

Deine Live-Läufe liefern gute Daten, aber deine Rezensionen lesen sich wie Formulare. Schreibe sie neu, sodass man sie gern
vorliest und danach weiß, was zu tun ist. Maßstab für Ton und Tiefe ist `docs/testlauf_tag15_rezensionen.md`. Lies die
Datei zuerst, kopiere aber keine Sätze daraus. Sie beruht auf einem älteren Spielstand.

## Warum die Rezensionen flach wurden

- Der System-Prompt in `tests/spieltest_rezension.py` verbietet wörtliche Zitate und jede Nacherzählung und verlangt
  180 bis 250 Wörter, ohne Note. Damit fehlt genau das, was eine Rezension lebendig macht.
- Fünf gleiche JSON-Abschnitte (`tests/spieltest_reviewstruktur.py`) ergeben bei jeder Person denselben Aufbau.
- Die Rezensionen schreibt Giftige Blume, also das Modell, das auch die Dialoge schreibt.
- Das Paket enthält zu wenig Stoff: Im letzten Lauf 13 geschriebene Events, davon 8 Selfies, kein Dorf.
- Die Personen sind Merkmalslisten. Ihr Leben hat nichts mit diesem Spiel zu tun.

## Rezensionen: So geht es besser

1. **Du schreibst selbst**, nicht das lokale Spielmodell. Das Spielmodell spielt nur.
2. **Drei Schritte getrennt:** erst ein Belegpaket aus den echten Protokollen, dann die freie Rezension, dann eine
   Prüfung jeder Behauptung gegen das Protokoll.
3. **Stoff:** Für jede Rezension liest du mindestens 40 Szenen und Events aus Anfang, Mitte und Ende des Laufs, aus
   allen Bereichen (Hauptstory, Dorf, Alltag, Romance, Kampf). Alles, was seit dem letzten Test neu ist, ist Pflicht.
4. **Einstieg mit einem Moment:** Der erste Absatz zeigt eine konkrete Szene, nie die Absicht der Person. Verboten sind
   Einstiege wie „Ich suche in Eden Rise …“.
5. **Wörtliche Zitate sind erwünscht**, mindestens drei je Rezension, kurz und unverändert aus dem Protokoll. Die Spieltexte
   sind Englisch, also bleiben die Zitate Englisch.
6. **Eine Lebensgeschichte, die das Urteil färbt:** Jede Person hat einen Grund, warum dieses Spiel sie trifft oder
   nervt, und bringt etwas mit, das nur sie bemerkt. Beispiel: Eine Halbkorsin hört, ob das Dorf echt klingt.
7. **Jedes Format hat seine Form:**
   - GameStar-Stil: deutsch, Zwischentitel, Wertungskasten, Pro und Contra, Prognose in Prozent
   - IGN-Stil: englisch, persönlich, witziger Titel, Verdict und Score von 10
   - Game-Two-Stil: deutsch, Sofa-Gespräch mit drei Personen, die sich necken und widersprechen, je eine eigene Wertung
   - übrige Profile: das in `tests/spieltest_profile.py` genannte Format, jeweils klar anders aufgebaut
8. **Länge:** 500 bis 900 Wörter je Rezension.
9. **Echte Meinung:** Die Person lobt und tadelt konkret, mit Zahl oder Szene, und nennt eine Note. Sie darf parteiisch
   sein und das zugeben. Zweifel an der Testgrundlage stehen einmal oben und einmal bei der Wertung, nicht in jedem Absatz.
10. **Naomi und Lenny** bleiben offen, erwachsen und direkt in Sachen Lust, Machtspiel und Fanservice, nie als Karikatur.
11. **Zum Schluss je Rezension „Was das für Duc heißt“:** höchstens vier konkrete Schritte, am Ende eine Gesamttabelle
    mit Maßnahme, Grund und Aufwand.
12. **Vorlesefassung:** ohne Tabellen, Belegnummern und Sonderzeichen, mit natürlichem Satzrhythmus.

## Rezensionen: Grenzen

- Personen und Rezensionen sind erfunden und nur intern. Ein Medium ist nur ein Stil, nie ein Absender. Keine echten Autorennamen.
- Der Bericht beginnt mit der Grundlage: Was wurde gespielt, was nicht? Bild, Ton und Steuerung nur bewerten, wenn du sie
  wirklich geprüft hast. Sonst steht im Wertungskasten „nicht geprüft“.
- Jedes Zitat und jeder genannte Moment steht in einer getrennten Beleg-Datei. Was du nicht belegen kannst, fliegt raus.
- Beobachtung und vermutete Ursache trennen. Vor jedem Tadel prüfen, ob es am Bot liegt.
- **Keine Fall-Auflösungen und keine großen Wendungen.** Keine Täter nennen.
- **Inhalte der Favours nicht verraten**, auch nicht in Zitaten. Duc soll sie selbst entdecken.
- Duc ist ESG-Berater und Gründer von Eden Consulting, nie „Tüftler“. Kanon: `docs/wiki/START.md`.

## Fehler aus dem letzten Lauf, die nicht wieder passieren dürfen

| Behauptung | Was wirklich war |
|---|---|
| Naomi: Rosi zieht eine harte Grenze | Rosi machte mit. Der folgende Vorschlag kannte die Szene nicht. Seit `2d8ffbd1` behoben. |
| Mia: 22 Dates | 22 vereinbart, 10 begonnen |
| Tandi: nur 4 Fähigkeiten, also wenig Tiefe | Die Kämpfe spielte eine Routine, das sagt nichts über Builds |
| Tandi: keine Dates, also ist Romance vom Kampf getrennt | Ihr Bot hat nie eingeladen |
| Kopfzeile: neun Perspektiven | 4 von 9 Profilen waren fertig |

## Testläufe: Was wir inzwischen wissen

**Vorbereitung**
- Spiele in einem eigenen Git-Worktree auf festem Commit und schreibe den echten Hash in den Bericht. `eden-config.json`
  und `module/eden_rise/figuren` sind gitignored und müssen hineinkopiert werden. Sonst ändern andere Sitzungen die Daten mitten im Lauf.
- Sichere `tests/spieltest_live*.py` und deine anderen Dateien im Git. Der Git-Index ist geteilt: nie dort stagen, sondern eigener
  `GIT_INDEX_FILE`, `git commit-tree` und `git update-ref` mit der alten Basis.
- Beende keine fremden Prozesse. Starte erst, wenn Krea und Chatterbox nichts rechnen, und stimme dich über Duc ab.
- Plane die Zeit: Ein Profil dauert grob 1,6 Stunden, alle neun etwa 15 Stunden. Setze Noor vom Checkpoint fort, verteile den Rest
  auf mehrere Nächte. Lieber ein fertiges Profil als fünf halbe.

**Bot menschlicher machen**
- Gesten mit Zufall statt fester Rangfolge (`tests/spieltest_verhalten.py`), nicht immer dieselbe Geste.
- `tests/spieltest_bot.py` filtert Nein-Wünsche heraus. Lass Naomi auch solche wählen, damit Ablehnungen wirklich getestet werden.
- „Zeit zusammen“ nicht immer direkt nach Intimität. Nicht jeden Abend einladen, Pausen je Figur.
- Dates einhalten: Profile mit Romance wählen die Date-Karte meist. Versetzen kostet seit `ebe6d38f` immer Vertrauen.

**Bewertung ehrlich machen**
- „Grün“ heißt nur „abgedeckt“. Builds und Kampfgefühl bleiben „offen“, solange eine Routine kämpft.
- „Leere Tage“ und „Tasche voll“ prüfen, bevor sie gelb werden. Ein volles Konto ist kein Befund, wenn der Bot nichts kauft.
- Fest messen: häufigste Szeneneinstiege und Wörter je Figur, wortgleiche Zeilen, Grund für jedes ausgefallene Date.
  Vorlagen `codex_pruef2.py`, `codex_pruef4.py`, `codex_pruef5.py` in
  `C:\Users\DucNg\AppData\Local\Temp\claude\C--Users-DucNg\53e6c615-01cc-456c-892f-260cdc3447fb\scratchpad\`.
- Kurven gibt es schon: `python tests\spieltest_kurve.py`, Stufe je Spieltag je Frau, Ergebnis `docs/brain_trust/BEZIEHUNGSKURVE.md`.
- Bereits bekannt, nicht neu als Fund melden: 27 % der freien Szenen beginnen mit „… leans against“, Alva hat immer ein Glas.
  Prüfe stattdessen, ob es nach einem Fix weniger wird.

**Zieltests statt immer 22 Tage**
Lauf ab Checkpoint, Minuten bis eine halbe Stunde, vor und nach einem Fix mit gleichen Bedingungen:
1. „Zeit zusammen“ direkt nach Intimität (`2d8ffbd1`): Bleibt sie beim Moment, wiederholen sich Vorschläge?
2. Date mit einer Figur, die am Abend in einer Story-Szene mitspielt (`ebe6d38f`): Rückt es sauber auf den nächsten Abend?
3. Nur Dorf-Events (Pascal, Mina, Bà Tư, Sandru, Don Anghjulu, Casanova): Figuren, Ton, Beziehungen im Dorf.
4. Nein-Wünsche bei Rosi, Chiara, Lea, Siri, Alva: Lehnt sie im Charakter ab, ohne die Stimmung zu töten?

**Noch blind**
Bild, Ton und Bedienung fehlen. Baue dafür eine Browserprüfung mit Playwright (Screenshots, Tastaturwege, Konsole, 1366x768 bis 1440p,
Eden ist PC-only). Noors Prüffeld zur Zugänglichkeit geht nur so. Stimmung und Klang bleiben Ducs Urteil.

## Reihenfolge

1. Neue Rezensionen aus den vier fertigen Läufen schreiben, ohne neuen Lauf. Das zeigt sofort, ob der Ton stimmt.
   Quellen: `C:\Users\DucNg\Documents\Codex\2026-10-30\wa\work\live\abnahme\lauf-*\dialoge.jsonl`.
2. Duc gibt den Ton frei.
3. Danach Worktree, Bot-Änderungen, Zieltests. Erst zuletzt ein neuer Gesamtlauf.

Spielinhalte und Spielregeln änderst du nicht. Du meldest Befunde, die Sitzungen beheben sie.

**Abgabe:** `docs/spieltestberichte/<Datum>/` mit Bericht, Rezensionen, Vorlesefassung und Beleg-Datei. Sag am Ende klar, was
geprüft ist und was nicht.

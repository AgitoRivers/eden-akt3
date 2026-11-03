# Stil & Sprache

Stand 25.10.2026 · Besitz: Hauptsitzung. Gilt für jeden Text, den der Spieler sieht oder hört: Events, Szenen,
Antwort-Chips, Kampftexte, Items, Missionen, Codex, Oberfläche, Handy, Karten.

## 1. Sprache

- **Spieltext ist Englisch, vollständig.** Rede, Erzählung, Gedanken, Titel, Chips, Kampf, Items, UI. (Duc, 25.10.2026;
  ersetzt die Regel vom 19.10. „UI Deutsch“.) Die deutsche Fassung entsteht am Ende über eine Übersetzungstabelle.
- Jeder Text bekommt einen festen Schlüssel (Event-ID + Feld, Item-ID + Feld …), damit das Mapping später greift.
  Texte nicht aus Bausteinen zusammenkleben, die sich nicht übersetzen lassen.
- **Britisches oder amerikanisches Englisch?** Erzähler und UI: britische Schreibung (colour, harbour, favourite), weil
  das Spiel in Europa spielt. Figuren sprechen ihr eigenes Englisch (Lola australisch, Megan schottisch …).
- Fremdwörter nur, wo die Figurenseite es erlaubt (Totò „Comandante“, Lola „mate“, Jana „Na geh!“). Kein Deko-Italienisch.
- Mit Duc im Chat Deutsch. Docs für das Team dürfen Deutsch sein, Beispielzeilen darin Englisch.

## 2. Erzählform (Visual Novel)

| Was | Wie | Beispiel |
|---|---|---|
| Gesprochenes | in Anführungszeichen | “You need a weapon, Captain.” |
| Gedanken, Gefühle | in *Sternchen* | *Don't grin. Not now.* |
| Handlung, Situation | klarer Text ohne Zeichen | Rosi throws the bat a little too hard. |

- In den Daten stehen **Sprechzeilen ohne Anführungszeichen** (die Oberfläche setzt sie, die Stimme liest sie);
  Erzähltext und Chips folgen der Tabelle.
- Erzähltext in **zweiter Person, Präsens**: “The tender bumps against the quay. You smell diesel and fish.”
- Gedanken dürfen von Duc oder von der handelnden Figur kommen, aber pro Absatz nur von einer Person, und es muss
  klar sein, wessen Kopf es ist (direkt nach ihrer Handlung oder Rede).
- **Antwort-Chips (Duc):** Handlung zuerst als klarer Satz, dann die Rede: Ties a bowline one-handed. “Behind my back,
  if you like.” Reine Handlung ohne Rede ist ein ganzer Satz: “Just nods.” Keine Klammern.
- Szenenüberschriften für Karten: `+++ Scene Name +++` (englisch, 2–4 Wörter, Szene statt Stimmung).
- **Handy-Nachrichten = echter Chat (Duc 27.10.2026):** mehrere kurze Blasen statt eines Absatzes, unstrukturiert
  (klein geschrieben, Abbrüche, Zurücknehmen erlaubt) und **mit Emojis**, wie die Figur sie benutzen würde (Lola viele,
  Megan und Sophia selten, Elsa fast nie). Gefühle stehen zwischen den Zeilen, nicht ausgesprochen. Emojis werden vor
  der Vertonung entfernt, die Stimme liest sie nie.
  Gilt für jede getippte Zeile (auch die alten Flirt- und Handy-Nachrichten, nachgerüstet 27.10.2026), nicht für
  Anrufe, Videoanrufe und das, was die Figur danach vor Ort sagt. Die Aufnahmen bleiben dabei gültig.

## 3. Natürlich schreiben – keine „KI-Haiku“

Duc 25.10.: „Das sind alles Menschen, sie sollen natürlich sprechen.“ Die häufigsten Fehler und wie es richtig geht:

| Fehler | Falsch | Richtig |
|---|---|---|
| Stakkato aus Satzfetzen | “Terremoto. Earthquake. Weighted core. Don't drop it.” | “That's Terremoto. There's a weighted core inside, so try not to drop it on your foot.” |
| Jeder Satz eine Pointe | “Coffee's cold. Like this conversation.” (passt nur zu Holm, einmal) | Pointen sparsam, eine pro Auftritt reicht |
| Alle klingen gleich knapp | Lola, Rosi, Elsa sprechen im selben Telegrammstil | jede Figur nach ihrer Seite: Lola plappert und verliert den Faden, Sophia lässt Pausen, Maxwell redet über sich in der dritten Person |
| Erklärsätze für den Spieler | “As you know, I am the engineer and the workshop burned.” | Wissen steckt in Handlung und Subtext: “I got one thing out before the roof came down.” |
| Gefühle benennen statt zeigen | “I feel very nervous.” | Jana zieht ihren Pferdeschwanz fester. “Sorry. Sorry, Sir.” |
| Sätze ohne Verbindung | drei Hauptsätze, kein „and/but/so“ | Menschen verbinden Gedanken, brechen ab, setzen neu an: “It's not – look, just take it, okay?” |

**Maßstab: Disco Elysium** (Duc 25.10.): Figuren dürfen abwägen, zögern, sich korrigieren, zwei Seiten sehen. Nicht alles
muss poliert sein – Ecken und Umgangssprache machen sie lebendig. Humor kommt aus dem Charakter, nicht aus einer
Pointen-Maschine.

**Faustregeln**
- Laut lesen. Klingt es wie ein Mensch in dieser Lage (müde, verrußt, verliebt, wütend)? Sonst umschreiben.
- Wortkarge Figuren (Holm, Petru, Rosi bei Technik) sprechen **kurz, aber vollständig**: ein ganzer Gedanke mit
  Rhythmus und Subtext, keine Aneinanderreihung von Zwei-Wort-Sätzen.
- Pro Zeile höchstens 2–3 Sätze, damit Vertonung und Textbox atmen; lieber eine zweite Zeile.
- Satzbau darf unpoliert sein (Abbrüche, Wiederholungen, „look“, „I mean“), wenn die Figur so spricht.
- Erzähltext: kurz und direkt, keine verschachtelten Sätze, keine Selbstkorrekturen; Bilder statt Adjektivketten.
- Keine Klischees („a smile that didn't reach her eyes“, „electricity in the air“, „little did he know“).
- Keine Körpersprache-Floskeln (Spieltest 29.10.2026: „lets out a …“ in jeder vierten Antwort): nicht „freezes“, „voice
  dropping“, „eyes widen“, „cheeks flushing“, „breath catching“. Stattdessen die eigenen Gesten der Figur (ihre
  Wiki-Seite) oder einfach die Worte. Gilt für Spieltext und für den Szenen-Prompt (`kern/szene.FLOSKELN`).
- Keine Zeile darf etwas behaupten, was der Figurenseite widerspricht (Alter, Herkunft, Anrede, Wissen).

### Witzig und warm (Duc 02.11.2026: Mochi-Tiere, Bibis Selfies, Cliffhanger abgenommen)

- **Trocken beobachten statt Witze machen.** Erst ein ruhiger, genauer Satz, dann der Haken im letzten Satz: “He solved the lab's feeding puzzle in a week. It took Bibi two to notice.” Keine Ausrufe, kein „hilarious“.
- **Das Tier (oder das Kind, der Alte) hat Würde, der Mensch verliert.** Monsieur gibt alles zurück außer dem Stift; Madame beißt einmal, „the visit is over“. Gelacht wird über die Lage, nie über das Schwache.
- **Konkrete Kleinigkeit statt Gefühl.** Eine Zahl, ein Gegenstand, eine Uhrzeit: „It has been eleven minutes.“, „a neat pile of truffles by the gate“. Das Gefühl entsteht beim Spieler.
- **Kleine Szene in zwei Bildern (A, dann B):** A baut die Erwartung, B kippt sie mit gleichem Blick und gleicher Ruhe (stolz → Halstuch im Maul; „she's leaving“ → „an hour later. still leaving.“).
- **Ernst durch Kontrast und Echo.** Der Gegenspieler spricht poliert und freundlich, mit einer echten Zahl („Our security team was there in forty minutes.“). Danach wiederholt eine Figur aus dem Dorf genau diese Zahl, leise: „Forty minutes. ...Nobody came at all.“ Keine Erklärung, kein Erzähler, der sagt, dass es gelogen ist.
- **Ein Wort als Schluss.** Nach einer großen Enthüllung sagt eine einzige Figur ein Wort („...Monsieur?“). Das trägt mehr als ein Absatz.

### Verständlich bleiben (Duc 30. und 31.10.2026)

- **Einfaches Englisch.** Nicht alle Spieler sind Muttersprachler. Häufige Wörter, keine Redewendungen, keine doppeldeutigen
  Wörter (draw/drew, „name on the spine“). Braucht die Story ein Fachwort, steht ein einfaches Wort daneben (“A draw, so nobody won”).
- **Der Spieler hat die Szene davor vergessen.** Zwischen zwei Szenen liegen viele Mechaniken und Ereignisse. Jeder Rückbezug
  trägt deshalb eine Erinnerung, in der Lage am Anfang oder im Satz selbst: nicht “That first relay was fine”, sondern
  “That first relay, the night you held the lamp, was fine”. Beim Prüfen fragen: Was muss man sich gemerkt haben?
- **Erst die klare Frage, dann die Antworten.** Soll der Spieler antworten, stellt die Figur vorher eine Frage, die man versteht
  (“What do you see?”). Jede Antwort muss ohne Vorwissen verständlich sein.
- **Ganze Sätze auch in Telegramm-Laune.** Witze und bewusste Marotten dürfen kurz bleiben (“Fine! I'll rest. Aggressively.”, Chiaras
  Bewertungen, Sophia ohne ihre Show). Alles andere verbindet die Gedanken mit and, but, so, because.

### Item-Beschreibungen (Duc 29.10.2026, Brain Trust ⭐1, gilt für alle Items)

Vorbild Elden Ring: Der Text trägt Lore, ist aber wärmer und nie kryptisch. Drei Schichten, zusammen höchstens
~220 Zeichen (passt auf die Ladenkarte):

1. **Ding:** was man sieht, riecht, fühlt (ein Satz).
2. **Herkunft:** wer es verkauft, verloren, getragen oder gemacht hat – nur Kanon aus dem Wiki (Totòs Spind, Alvas
   Bar, Strand, Mission, Eden-Shop …). Sagt das Wiki nichts, bleibt der Text bei Ding und Haken.
3. **Haken:** ein Witz, eine Wärme oder eine offene Frage (ein kurzer Satz).

- **Ton-Mix über alle Items** etwa 40 % witzig, 30 % wholesome, 15 % frech (NSFW-Geschenke: frech, nie plump),
  15 % ernst/Lore.
- **Nie verraten, wer ein Item liebt** (das Dorfohr und das Schenken bleiben ein Ratespiel). Andeutungen sind
  erlaubt, Namen der Liebhaber nicht.
- Funktion (Bonus, Heilung) steht nicht im Lore-Text, sondern in der Wirkungszeile.
- Beispiele: *Heavy enough to anchor a dinghy. Totò swears it's real. Totò also swore the goat was a gift.* ·
  *Iron, heavy, tied to a cork float so it won't sink. Petru doesn't give his key to people. He gives it to people
  he'd let into his boat.*

## 4. Anrede und Namen

- Wie jede Figur Duc anspricht, steht in der Anrede-Matrix in [`figuren/README.md`](figuren/README.md). Abweichen nur,
  wenn die Szene es begründet (Megan sagt „Duc“, wenn sie nicht verärgert ist).
- Eigennamen fest, wie im Register: Waffen Riposte, Terremoto, Sussurro, Le Large, Gemelli · Jacken Terra Scura,
  Meramie, Incendio, Zéphyr, Citadelle (`docs/wiki/systeme/aufruestung.md`).
- **Namensregel (E-052):** Neue Namen auf Deutsch, Englisch und Italienisch auf Beiklang prüfen; nichts, was nach
  Scheitern oder Lächerlichkeit klingt. Eden ist Marken-Bestandteil (Eden Group, Eden Consulting, Eden Rise …).
- Figuren ohne Vornamen bleiben so (Yamamoto-san, Madame Casanova).

## 5. Spoiler

- Fall-Auflösungen (wer welchen Fall ausgelöst hat, Motive, Geständnisse) stehen nur in `module/eden_rise/story.json`
  und den Fall-Buildern. Nie im Chat, nie im Wiki, nie in Event-Texten außerhalb der Fall-Logik.
- Figurenseiten nennen Fall-Bezüge höchstens als „in einem Fall verdächtig“ ohne Auflösung.

## 6. Bilder (Krea / Prompt Studio)

- **Vor jeder Generierung `X:\AI\PromptStudio\KREA_LEITFADEN.md` lesen, auch als Agent.** Dort stehen alle Regeln zu Technik, Prompts, Figuren und Abnahme. Neue Lehren kommen dorthin.
- Krea rendert mit CFG 1: Negativ-Prompt wirkt nicht. Unerwünschtes positiv ersetzen („every seat empty“,
  „vehicles parked, doors closed“).
- Hintergründe ohne Menschen: Personen ausdrücklich ausschließen, keine Mittelgänge/Fahrer/Arbeiter beschreiben.
- **Trypophobie-Check ist aus (Duc 03.11.2026):** Lochmuster müssen nicht mehr gemieden oder geprüft werden.
- Freigabe immer über eine HTML-Abnahmeseite (`werkzeuge/abnahme_seite.py`).
- **Sprite passt zur Lage (28.10.2026, Spieltest):** ernste Szene, ernste Pose. In Krisen (Alarm, Brand, Anhörung,
  Verteidigung) nie flirtende oder überdrehte Posen; das Gefühl einer Zeile (`Z(..., gefuehl)`) nach dem Ton der
  Zeile wählen, nicht nach der Figur. Ein trockener Satz bekommt keine Schock-Pose.
  - **„neutral“ ist immer ruhig und frontal** (Duc 29.10.2026). Anzügliche oder überdrehte Posen (von hinten, Blick
    über die Schulter, Bein gekickt, Hände am Top, Rock gehoben) gehören zu `desire` bzw. `amusement`, nie zu
    `neutral` – der Richter liefert in Krisen oft „neutral“. **Neue Sprite-Sets vor der Übernahme darauf prüfen**;
    jedes Set behält mindestens eine ruhige neutral-Variante. Durchgang 29.10.: 9 Varianten umbenannt (nichts gelöscht).
  - In ernsten Events (`ton: ernst`) nie `desire`/`love`; `joy`/`excitement`/`amusement` nur als bewusst freigegebener
    trockener Scherz. Der Test `tests/test_sprite_stimmung.py` prüft das (Freigabeliste `FREI`).
  - **Stimmungsrahmen für freie Szenen** (Duc 29.10.2026): In Krisen-, Abschieds- und Anhörungsszenen wählt der
    Gefühls-Richter nur aus einer Liste (`stimmung` in `story_buehne.py`, Rahmen *krise*, *abschied*, *ernst*, *sturm*,
    *anhoerung*). Er bleibt für die Feinheit zuständig, kann aber nicht aus der Lage fallen. Betroffen: Kaltstart,
    Explosion, Nachtwache mit Holm, Lagebesprechung, Holms Abschied und der leere Platz, Inspektion, Sturm, Anhörung,
    Cliffhanger. Lockere Szenen (Party, Tratsch, Abende, Flirt) bleiben frei. Neue ernste Story-Szene → Rahmen eintragen.

## 7. Vertonung

- Sprechzeilen werden mit der Stimme aus `eden-config.json` (stimmen.eden_rise) vertont. Eine Datei hängt am Wortlaut:
  geänderter Text = neue Aufnahme beim nächsten `Vertonen_EdenRise.bat`.
- Zeilen so schreiben, dass sie gesprochen funktionieren: keine Klammern, keine Abkürzungen ohne Aussprache,
  Zahlen ausschreiben, wenn die Stimme sie sonst falsch liest.

## 8. Bedienung: Kreis oder Karte

Was keine Zeit kostet, ist ein **Kreis** (Kabine, Angeln, Holz, Stein). Was die Phase verbraucht, ist eine **Karte**. Ein Kreis zeigt ein Bild und als Abzeichen den Bestand. Geht er gerade nicht, bleibt er grau stehen und sagt, warum (Brain Trust 30.10.2026).

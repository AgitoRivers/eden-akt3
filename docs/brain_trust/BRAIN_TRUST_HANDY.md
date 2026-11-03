# Brain Trust · Das Handy bekommt eine Seele (03.11.2026)

Anlass: Duc 03.11.2026: „Aktuell hat das Handy-Dialogmenü wenig Seele, das können wir optimieren.“ Vorher: Ist-Stand
im Code und in der Vorschau angesehen, Recherche zu Handy-Mechaniken anderer Spiele, besonders zu denen, die genervt
haben. Screenshots und Entscheidungstabelle: `docs/abnahme/handy_seele/index.html`.

## Ist-Stand (geprüft im Code und in einer eigenen Vorschau, Tag 3)

Das Handy hat zwei Gesichter:

| Gesicht | Was es ist | Stärke | Schwäche |
|---|---|---|---|
| **A · Anruf-Karte** (`ereignisse` art `handy`, `client/index.html` `ev-tel`) | feste, vertonte Events: 30 Handy-Events, 87 Selfies, Favours, Erinnerungen, Megans Sprachnachrichten | die Texte sind stark („They took my appendix and my boat on the same day.“) | sieht aus wie jedes andere Event: runder Kreis mit Gesicht, Label „VIDEO CALL“, Antworten als Liste. Kein Klingeln, kein Annehmen, kein Bild von ihr in ihrer Welt. Der Anrufer-Ort (`anrufer_ort`) liegt nur als ganzer Hintergrund hinter der Karte und wirkt wie Ducs Zimmer |
| **B · Chat** (`kern/handy.py`, Overlay `handyHtml`) | ein Faden je Frau, Texte vom Modell, Antwort-Chips | Gedächtnis, Schiedsrichter, Ton-Regeln im Code sind solide | alle Fäden sehen gleich aus. Chips tragen Werte („Trust ↑“, „Desire ↑“, „only mood today“), das Feld zählt „3 left today“, Systemzeilen „Desire ↑“ stehen mitten im Chat, „Suggest replies“ ist ein Werkzeug-Knopf. Kein „typing …“, kein Status, kein Profilbild oben, keine Fotos im Faden |

Zahlen: Bot-Spieltest zeigt je Durchlauf etwa 4 zufällige Handy-Events plus 6 Sprachnachrichten von Megan, von 39
möglichen (`systeme/interaktion.md`). Höchstens 2 Handy-Meldungen am Tag. Töpfe sind laut E-116 unsichtbar, der Chat
zeigt aber Pfeile.

## Recherche: wer es gut gemacht hat, wer genervt hat

| Spiel | Was | Lehre für Eden |
|---|---|---|
| Persona 5 | Chats bauen Nähe, laden zu Treffen ein. Kritik: Texte wiederholen oft nur, was man gerade gesehen hat | Ihr Text muss etwas Neues bringen: ihr Leben außerhalb der Szene |
| Cyberpunk 2077 | Fixer-Anrufe und Auto-SMS ohne Ende, Ablehnen erst mit Patch 1.5 | Nie unterbrechen, nie Spam, Ablehnen immer erlaubt |
| GTA IV (Roman) | „Let's go bowling“: Freunde rufen ständig an, Ignorieren senkt den Wert | Ein Nein darf nicht bestrafen, sonst wird Zuneigung zur Pflicht |
| Dead Rising (Otis) | Anrufe mitten im Kampf, bei Unterbrechung von vorn | Nie in Action-Momenten, verpasst heißt nachhören, nicht neu anfangen |
| Mystic Messenger | Echtzeit-Chats, auch um 3 Uhr nachts: süchtig machend, aber wer verpasst, verliert | Dringlichkeit ja, Strafe nein: Verpasstes wird Sprachnachricht |
| Florence | Gespräch als Puzzle, die Teile werden mit wachsender Nähe weniger, im Streit kantig | Die Oberfläche selbst zeigt die Beziehung, ohne Zahlen |
| Emily is Away | Man tippt, löscht, tippt neu: man sieht, was die Figur fast gesagt hätte | Zögern sichtbar machen. Subtext wie bei Disco Elysium |
| Metal Gear Solid (Codec) | Gesichter reagieren je Satz, eigener Klingelton, ikonisch | Jede Figur klingt und sieht am Telefon unverwechselbar aus |
| Oxenfree | Man kann jederzeit ins Gespräch fallen. Kritik: Timing unklar | Freiheit nur, wenn klar ist, was passiert |
| Boyfriend Dungeon | Texte zwischen Dates tragen schwere Themen; „Mom“-Texte abschaltbar | Spielerin hat Kontrolle über heikle Ströme |
| A Normal Lost Phone, Simulacra | Das Handy erzählt seinen Besitzer: Kalender, Fotos, Notizen | Ducs Handy ist sein Tagebuch, die Galerie ist Erinnerung |
| Life is Strange | Texte reagieren auf Entscheidungen, alte Texte nachlesbar | Folgen kommen als Nachricht zurück |

Quellen: siehe Abnahme-Seite.

## Die Runde

**Luise (Art & Story):** Das Bild, das mich nicht loslässt: Holm um zwei Uhr nachts im Krankenhaus, mit offenem Haar,
und wir zeigen sie in einem runden Passfoto-Kreis wie auf einem Mitarbeiterausweis. 🥺 Die Texte haben Seele. Der Rahmen
behandelt sie wie Verwaltung.

**Sienna (Game Direction):** Vorbild ist Florence: Die Oberfläche selbst erzählt die Beziehung. Gegenvorbild ist
Persona 5, wo viele Texte nur nacherzählen. Und GTA IV zeigt, was passiert, wenn ein Anruf Pflicht wird. ✨

**Sora (Spielerstimme / QA):** Mein dritter Durchlauf, Minute 1: Ich öffne Chiaras Chat und sehe „Trust ↑“ über dem
netten Satz und „Desire ↑“ über dem frechen. Ich klicke den Pfeil, nicht den Satz. 😭 Das ist Excel mit Emojis. Nochmal-Lust 2 von 5.

**Aly (Tech):** Die Daten sind schon da. Wo sie ist (`ablauf` je Phase), ob sie Wache hat (`WACHE_ORTE`), die Stufen, die
Selfies, der Anrufer-Ort, ab heute Ducs Gefühls-Posen. Wir zeigen sie nur nicht. Und E-116 sagt: Töpfe sind
unsichtbar. Der Chat widerspricht dem gerade. 🤓

### Optionen

| # | Option | Was es ist | Vorbild |
|---|---|---|---|
| 1 ⭐ | **Chat mit Seele** | Keine Zahlen im Chat: Chips ohne Pfeile, nur ein kleines Ton-Zeichen, kein „3 left today“, keine Systemzeilen „Desire ↑“. Stattdessen zeigt sie, wie es ankam: „typing …“, Pause, ein Herz auf deiner Nachricht, später „Chiara is on watch 🌙“ statt Zähler. Oben ihr Gesicht und ihr Status („on watch · bridge“, „asleep“). Das Profilbild ist das letzte Selfie, das sie dir geschickt hat | Florence, iMessage |
| 2 | **Anruf als Bühne** | Annehmen-Bildschirm mit eigenem Klingelton je Figur, dann Videoanruf: sie groß in ihrer Welt (Krankenhausbett, Bar), Duc klein im Bild-im-Bild mit seiner Gefühls-Pose und Sonnenbrille. Ablehnen immer erlaubt, ohne Strafe | MGS Codec, FaceTime |
| 3 | **Das Handy wächst mit** | Kontaktname ändert sich mit der Nähe („Chiara Sonnberg“ → „Chiara“ → ihr Spitzname), ab Stufe 3 Sprachnachrichten und Sticker, ab 5 oben angeheftet | Florence |
| 4 | **Duc zögert** | Bei riskanten Antworten tippt Duc, löscht, schreibt neu: man sieht kurz, was er fast geschrieben hätte | Emily is Away |
| 5 | **Galerie im Handy** | Fotos-App mit allen Selfies, Polaroids und Dank-Fotos, statt nur im Pause-Menü | A Normal Lost Phone |

### Verbesserungsrunde

**Maelle (Producerin):** 1 und 3 sind dieselbe Idee in zwei Stufen. Ich lege 3 als Teil in 1, aber nur Profilbild und
Status. Die 55 Spitznamen schreibt Character Design später. 📋

**Sora (Spielerstimme / QA):** „Suggest replies“ muss weg. Die Chips sind Ducs Gedanken, sie sollen einfach da sein, wenn
sie geschrieben hat. Wie die inneren Stimmen in Disco Elysium. 😏

**Aly (Tech):** Das Risiko geht nicht verloren: Statt „risky – she barely knows you yet“ ein kleiner Satz in Ducs Kopf,
„too soon?“. Die Regel im Code bleibt gleich (`flirt_min_trust`). 🤓

**Luise (Art & Story):** Bei 2: Duc mit Sonnenbrille um zwei Uhr nachts im Videoanruf, und Holm sagt nichts dazu. Einmal im
Spiel sagt sie es doch. Das ist der Running Gag, den Duc will. 🥹

### Gegenrede

**Sienna (Game Direction):** Ich widerspreche Sora ein Stück. Ohne Zahlen fliegt die Spielerin blind. Gegenvorschlag:
Die Wirkung zeigt sich sofort, aber als Gefühl. Ihr Herz-Tapback bei einem Treffer, ein „seen“ ohne Antwort bei einem
Fehlgriff. Und die Beziehungskarte im Menü zeigt wie bisher die Stufen. ✨

**Aly (Tech):** Größtes Risiko bei 1: „typing …“ ist bei uns echte Wartezeit des Modells. Gut so, denn dann wird die
Wartezeit zur Fiktion. Aber wenn das Modell 8 Sekunden braucht, ist das lang. Wir zeigen das Tippen in Wellen, wie
echte Menschen. 🤓

### Vorschläge

| # | Vorschlag | Von |
|---|---|---|
| 1 | Chat ohne Zahlen, Wirkung als Gefühl (Tapback, „seen“, Status) | Sora, Sienna |
| 2 | Kopf mit Gesicht, Status, „typing …“; Profilbild = letztes Selfie | Aly, Luise |
| 3 | Chips erscheinen von selbst als Ducs Gedanken, Risiko als „too soon?“ | Sora, Aly |
| 4 | Anruf als Bühne mit Annehmen, Klingelton, Bild-im-Bild mit Ducs Sonnenbrille | Luise, Sienna |
| 5 | Kontaktnamen je Stufe (später, Character Design) | Maelle |

**Selbstkontrolle.** **Sora:** Ja, weil jeder Vorschlag auf etwas zeigt, das ich im Chat heute sehe und das mich stört. **Maelle:** Ja, und es ist in zwei Paketen baubar, ohne neue Sprechzeilen.

**Preis.** Paket 1 (Chat mit Seele): eine Sitzung, nur Client und `kern/handy.py`, keine neuen Zeilen, keine
ElevenLabs-Kosten. Paket 2 (Anruf als Bühne): eine Sitzung. Bilder sind da; an Klängen gibt es einen Klingelton
(`anruf_klingeln`) und vier Nachrichtentöne, ein eigener Ton je Figur wären bis zu elf neue Klänge. Die Belagerung und der
Rest der Romanzen-Arbeit bleiben unberührt.

**Maelle (Producerin):** Eine Frage an dich, Duc: Bauen wir zuerst Paket 1, den Chat mit Seele? 📋

**Duc:** Paket 1 und 2 ja, Galerie auch. Gebaut in `eab06812`, beschrieben in `docs/wiki/systeme/handy.md`.

---

# Nachschau · Was der Umbau gebracht hat und was noch fehlt (03.11.2026, abends)

Grundlage: zwölf Aufnahmen des gebauten Stands (`docs/abnahme/handy_seele/neu_*.jpg`, 1920×1080, Tag 3) und ein Blick in
den Code. Zwei Dinge in den Aufnahmen sind Artefakte der Vorschau und kein Fehler: „She nods and says nothing.“ in der
Chat-Liste ist die Platzhalter-Antwort von `tests/vorschau_server.py`, und „Evening“ über „Afternoon“ im Chat kommt vom
Knopf „Restart day (test)“.

Gefunden im Code:

| Befund | Beleg |
|---|---|
| Handy-Events und Chat sind zwei Welten. Keins der 261 Handy-Events (203 Nachrichten, 57 Videoanrufe) landet nach dem Ende im Chat-Faden der Frau. Ein Anruf um 02:13 hinterlässt dort keine Spur | `handy.faden_von` schreiben nur `lob.py`, `mochis.py`, `ermittlung.py` und Rosis Werkstatt in `eden.py` |
| Der Chat zeigt keine Zahlen mehr, die Handy-Events schon: 140 von 261 zeigen „Courage check · DC 12“ unter der Antwort | `client/index.html`, Antwort-Knöpfe der Events |
| Im Videoanruf stehen ihre drei Zeilen als Kästen über den drei Antworten. Beides sieht gleich aus, die Zeilen wirken wie Knöpfe | `neu_video.jpg` |
| Duc im Bild-im-Bild ist die ganze Figur vor grauem Grund, kein Webcam-Ausschnitt | `neu_video.jpg`, `.ev-video .pip` |
| Offen aus der ersten Runde: Kontaktnamen je Stufe (Idee 3), Duc zögert (Idee 4), Klingelton je Figur | Protokoll oben |

## Die Runde

**Sora (Spielerstimme / QA):** Erst das Lob: Das Herz an meiner Nachricht hat mich gefreut, ohne dass ich eine Zahl
gesehen habe. Das ist der Moment. Dann ruft Sophia um 02:13 an, ich nehme an, es ist schön. Ich lege auf, öffne ihren
Chat, und da steht nichts davon. Als hätte es den Anruf nie gegeben. 😭 Nochmal-Lust 3 von 5, vorher 2.

**Luise (Art & Story):** Das Bild aus dem Videoanruf ist stark: Sophia im Gang, das Licht von oben. Aber ihre Sätze
stehen in Kästen wie Fragebögen. Bei FaceTime liest man Untertitel unten im Bild, und dann schaut man ihr ins Gesicht
statt auf eine Liste. 🥺 Und Duc steht im kleinen Fenster in voller Größe da, als würde er für ein Plakat posieren.
Um zwei Uhr nachts will ich sein Gesicht sehen, mit Sonnenbrille, nah dran.

**Sienna (Game Direction):** Life is Strange und A Normal Lost Phone zeigen es: Das Handy ist ein Gedächtnis. Alles,
was passiert ist, kann man nachlesen. Bei uns zerfällt das Gedächtnis in zwei Hälften. Das ist der größte Hebel, mehr
als jeder neue Klang. ✨

**Aly (Tech):** Billig ist es auch. Beim Schließen eines Handy-Events kennen wir die Frau (`anrufer`), ihre Zeilen, die
gewählte Antwort und ihre Antwortzeile. Das sind drei bis fünf Einträge im Faden, Format wie `handy._zeile`. Beim Video
ein grauer Eintrag „Video call · 02:13“ und darunter dasselbe. Das Chat-Modell bekommt den Faden ohnehin als
Gedächtnis, es weiß dann also auch vom Anruf. 🤓

### Optionen

| # | Option | Was es ist | Vorbild |
|---|---|---|---|
| 1 ⭐ | **Ein Faden je Frau** | Nach jedem Handy-Event landen ihre Zeilen, Ducs Antwort und ihre Reaktion in ihrem Chat. Selfies stehen als Foto im Faden. Ein Anruf erscheint als grauer Eintrag „Video call · 02:13“, ein abgelehnter als „Missed video call“ | Life is Strange, A Normal Lost Phone |
| 2 | **Untertitel statt Kästen** | Im Videoanruf stehen ihre Zeilen als Untertitel unten im Video, die aktuelle Zeile hell, die alten blass. Darunter nur Ducs Antworten | FaceTime Live Captions |
| 3 | **Webcam-Duc** | Bild-im-Bild als Ausschnitt Kopf und Schultern aus derselben Gefühls-Pose, etwas weicher, Sonnenbrille bleibt | FaceTime |
| 4 | **Würfel als Gefühl** | In Handy-Events statt „Courage check · DC 12“ ein Würfel und ein Wort: „Courage · easy / tough / long shot“. Der Wurf danach bleibt sichtbar wie bisher | Disco Elysium |
| 5 | **Rest aus Runde 1** | Kontaktnamen je Stufe, Duc zögert beim riskanten Chip, Klingelton je Figur | Florence, Emily is Away, MGS |

### Verbesserungsrunde

**Maelle (Producerin):** 1, 2 und 3 gehören zusammen. Das ist Paket 3, „Das Handy erinnert sich“. 5 bleibt
geparkt, die Kontaktnamen schreibt Character Design, und eigene Klingeltöne kosten Klänge. 📋

**Sora (Spielerstimme / QA):** Bei 1 bitte nicht den ganzen Event-Text in den Chat kippen. Nur was sie gesagt hat und
was Duc gesagt hat, keine Erzähltexte. Sonst liest sich der Faden wie ein Protokoll.

**Luise (Art & Story):** Und das Selfie im Faden ist das Bild, das man im Chat antippt und groß sieht. Dann hat die
Fotos-App einen zweiten Weg zum selben Bild, und der Faden fühlt sich an wie ihr Handy, nicht wie ein Menü. 🥹

### Gegenrede

**Aly (Tech):** Ich widerspreche bei 4. Die Würfel sind ein Versprechen dieses Spiels, D&D-Prinzip, Regeln im Code.
Wer „long shot“ liest, weiß nicht, ob das 12 oder 16 ist. Gegenvorschlag: Die Zahl bleibt, wandert aber in den Tooltip
und der Knopf zeigt nur Würfel und Attribut. Wer rechnen will, kann. 🤓

**Sienna (Game Direction):** Und bei 1 eine Warnung: Megans sechs Sprachnachrichten und die Favours müssen draußen
bleiben oder eigene Regeln bekommen. Favours sind geheim, Megan ist fern. Erst die Nachrichten und Anrufe der Frauen,
dann sehen wir weiter. ✨

### Vorschläge

| # | Vorschlag | Von |
|---|---|---|
| 1 | Paket 3 „Das Handy erinnert sich“: Handy-Events landen im Faden (nur gesprochene Zeilen und Ducs Antwort, Selfie als Foto, Anruf als grauer Eintrag), ohne Favours und Megan | Sienna, Aly, Sora |
| 2 | Im Videoanruf Untertitel statt Kästen | Luise |
| 3 | Duc im Bild-im-Bild als Kopf-und-Schultern-Ausschnitt | Luise |
| 4 | Würfel: Zahl in den Tooltip, Knopf zeigt Würfel und Attribut | Aly, Sora |
| 5 | Kontaktnamen, Zögern, Klingeltöne bleiben geparkt | Maelle |

**Selbstkontrolle.** **Sora:** Ja, weil jeder Vorschlag auf etwas zeigt, das ich in den Aufnahmen des gebauten Stands
sehe. **Maelle:** Ja, und Paket 3 braucht keine neuen Zeilen, Bilder oder Klänge.

**Preis.** Paket 3 (1 bis 3): eine Sitzung. Code in `eden.py` beim Schließen eines Handy-Events plus Client
(`handyHtml`, `.ev-video`), dazu ein Test in `tests/test_handy.py`. Vorschlag 4: kleiner Client-Eingriff, gilt für alle
Events, nicht nur fürs Handy, deshalb eigene Entscheidung. Keine ElevenLabs-Kosten, keine GPU.

**Maelle (Producerin):** Eine Frage an dich, Duc: Bauen wir Paket 3, „Das Handy erinnert sich“? 📋

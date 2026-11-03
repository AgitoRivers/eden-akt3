# Megan: „The Robot Sees the Sea“

Stand 02.11.2026 · Character Design · Entwurf, nicht gebaut, nicht vertont. Einmalig, ab Vertrauen 3, spät abends als Videoanruf, nur solange `megan_abgereist` gilt und vor dem Satelliten-Ausfall (Tag 8 bis Tag 20 mittags). Setzt `megan_roboter`.

| # | Beat | Art | Inhalt | Ton / Sprite |
|---|---|---|---|---|
| 1 | Titelkarte | geskriptet | *The Robot Sees the Sea*. Musik aus, nur Zimmerton | – |
| 2 | Der Anruf | geskriptet | Lage: *It is one in the morning, and your phone buzzes. Megan, on video. There is a blue light moving on her face, from a screen you can't see, and there is no sound.* | neutral, frontal |
| 3 | Der Vorwand | vertont | “Your report has a comma in the wrong place, Duc. That's why I'm calling. At one in the morning.” | embarrassment |
| 4 | Sie vergisst ihn | vertont | Lage: *Her eyes are red. She looks past the camera at the other screen.* “He has been walking for eleven episodes, and he's nearly there. Don't say anything. I don't need the sound, I know what he says.” | sadness |
| 5 | Die Wahl | Chips | siehe unten | |
| 6 | Das Meer | vertont | Lage: *The light on her face goes from blue to white. For a while she doesn't look at you at all.* “There. He saw it.” | sadness, ruhig |
| 7 | Schluss | vertont | “Pollen. It's very bad at this time of year. ...Send me that report again, with the comma.” Sie legt auf | neutral |
| 8 | Morgen danach | Memo auf dem Handy | *“Re: last night's call. No such call took place. The comma is still wrong.”* | – |

## Die Wahl

| Chip | Achse | Ihre Antwort, vertont |
|---|---|---|
| Says nothing. Stays on the line. | Vertrauen | “You're still there. I have noted that.” |
| “Which episode is this?” | beide | “The last one. He can't swim, you know. Nobody ever told him. He goes in anyway.” |
| “Are you crying?” | Fettnäpfchen, kein Malus | “It's pollen. There is a great deal of pollen in Monaco at one in the morning. If you tell anyone, you're on a pedalo, and it will be pink.” |

Alle drei führen zu Beat 6. Keine Antwort beendet die Szene oder verschlechtert etwas.

## Hinweise für den Bau

- Sie gibt nichts zu und bleibt bei „pollen“, das sagen ihre Regeln (`figurenrahmen.json`).
- `gt_pollen` (Vertrauen 4) stellt das Thema neu vor. Vorschlag: `{"nicht": {"flag": "megan_roboter"}}`, damit es sich nicht wiederholt. Nur wer das Event verpasst, bekommt `gt_pollen`.
- Kein Fernseher im Bild: Der Rahmen zeigt nur ihr Gesicht, wie bei allen Fern-Szenen.
- Am Telefon nur mit Vertrauen 3, ohne `megan_funke`: Das Event ist keine Romanze und gilt für alle Wege.
- Fünf gesprochene Sätze plus drei Antworten, zusammen acht Aufnahmen.

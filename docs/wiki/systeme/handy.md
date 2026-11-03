# Handy · Chat, Anrufe, Fotos

Stand 03.11.2026 (Duc: „Paket 1 und 2 ja, Galerie auch“). Herleitung, Recherche und Brain Trust:
`docs/brain_trust/BRAIN_TRUST_HANDY.md`. Regeln für Nachrichten-Häufigkeit, Selfies, Favours und Töpfe stehen weiter in
[`interaktion.md`](interaktion.md); diese Seite beschreibt, wie sich das Handy anfühlt.

## Grundsatz: keine Zahlen im Chat

Töpfe sind unsichtbar (E-116), also zeigt auch der Chat keine Werte. Sie reagiert wie ein Mensch:

| Was im Code passiert (`kern/handy.py`, `antworten`) | Was die Spielerin sieht |
|---|---|
| Ducs Text bringt Punkte (`wirken`, positiver Ton) | ein goldenes Herz an Ducs Blase (`reaktion: "herz"`) |
| Flirt zu früh (Backfire) oder grober Ton kostet Punkte | „Seen“ unter Ducs Blase (`reaktion: "gesehen"`), ihre Antwort ist kühler |
| Ton wirkt heute nicht mehr (eine Wirkung je Frau und Tag) oder neutral | keine Reaktion, nur ihre Antwort |
| Topf voll (`topf_kommentar`) | ihr Satz aus `figurenrahmen.json` kommt als eigene Nachricht von ihr |
| drei Antworten am Tag erreicht | Status „busy“ bzw. nachts „asleep“ / „on watch“, statt Eingabefeld ihr Satz (`ausrede`, Englisch) |

Keine Systemzeilen mehr im Verlauf. Alte Spielstände mit `wer: "system"` blendet der Client aus.

## Chat (Overlay, `handyHtml` in `client/index.html`)

- **Kopf:** ihr Bild und darunter ihr Status (`handy.status`: Raum aus dem Tagesablauf, „asleep“, „on watch · Bridge“,
  „busy“, „away“).
- **Profilbild:** das letzte Selfie, das sie geschickt hat (`handy.profilbild`, aus `z["album"]`), sonst ihr Gesicht.
- **Mehrere kurze Blasen:** Das Modell darf bis zu drei Zeilen schreiben (`STIL`), `_teile` macht daraus bis zu drei
  Nachrichten. Blasen derselben Person rücken zusammen.
- **Tippen:** Duc sendet → seine Blase steht sofort da (Klang `handy_senden`), dann tippt sie (drei Punkte), solange das
  Modell schreibt. Jede ihrer Blasen kommt nach einer Tipp-Pause (700 ms + 26 ms je Zeichen, höchstens 2,4 s) mit dem Klang
  `notification`. Öffnet Duc einen ungelesenen Chat, kommen ihre letzten Blasen (bis zu drei) noch einmal einzeln an.
- **Antwort-Ideen:** erscheinen von selbst, sobald sie fertig geschrieben hat (kein Knopf mehr). Sie tragen keine Werte;
  ein zu früher Flirt ist mit „too soon?“ markiert. Ein Klick setzt den Text ins Feld.
- **Weniger Bewegung:** bei `prefers-reduced-motion` nur kurze Pausen, keine Einblend-Animation.

## Handy-Events (feste, vertonte Events mit `art: "handy"`)

| Art (`personen.art`) | Anzahl | So sieht es aus |
|---|---|---|
| `nachricht` (auch Selfies) | 203 | Chat-Karte mit ihrem Gesicht im Kopf. Foto zuerst, dann ihre Blasen einzeln mit Tippen und Klang; die Antworten kommen, wenn alles da ist. Ein Klick in den Chat zeigt alles sofort. Startklang `handy_nachricht`. Hintergrund bleibt Ducs Ort, wenn sie von Bord schreibt |
| `video` | 57 | Erst der Klingel-Bildschirm („Incoming video call“, `anruf_klingeln` alle 3,6 s). „Decline“ gibt es nur, wenn das Event eine Option `art: "auflegen"` hat (16 Events), und wählt genau diese. Nach „Accept“: Videoanruf mit ihr groß in ihrem Raum (`anrufer_ort`, auch Räume an Bord), Duc klein im Bild-im-Bild als Webcam (Kopf und Schultern aus seiner Gefühls-Pose, Sonnenbrille; `duc_bild`, Gefühl nach Event-Ton: frech/witzig → amusement, wholesome → joy, ernst → caring). Ihre Zeilen stehen als Untertitel unten im Video, die gesprochene hell; darunter nur Ducs Antworten. Die Stimme startet erst nach dem Annehmen |

## Das Handy erinnert sich (Paket 3, 03.11.2026)

Nach jedem Handy-Event landet, was gesagt wurde, im Chat-Faden der Frau (`handy.event_ablegen`, aufgerufen beim Schließen
des Events in `eden.py`). Der Faden ist ein Gedächtnis: Spielerin liest nach, Blume liest ihn im Chat-Prompt mit.

| Fall | Was im Faden steht |
|---|---|
| Videoanruf angenommen | grauer Eintrag „Video call“ (`art: "anruf"`), ihre Zeilen, Ducs Antwort, ihre Reaktion |
| Videoanruf abgelehnt (Decline am Klingel-Bildschirm) | nur „Missed video call“ (`art: "verpasst"`) |
| Nachricht mit Selfie | das Foto (`art: "foto"`, `bild`), ihre Zeilen, Ducs Antwort, ihre Reaktion. Antippen zeigt es groß |
| Nachricht ohne Foto | ihre Zeilen, Ducs Antwort, ihre Reaktion |

Regeln: Ducs Antwort kommt nur in den Faden, wenn er etwas sagt (Text in Anführungszeichen, ohne die Zeichen); erzählte
Antworten wie „Rates it a seven and waits.“ bleiben draußen. Erzähltexte (`lage`) nie. Nur Frauen mit Chat (ST-Karte);
Favours (geheim) und Figuren ohne Karte (Megan, Totò …) bleiben draußen. Für Blume stehen die Einträge als
„(video call)“, „(missed video call …)“, „(she sends a photo)“ im Verlauf (`MARKER`).

## Fotos-App

Reiter „Photos“ im Handy: alle Bilder aus dem Album (`z.album`, Selfies), je Person, neueste zuerst. Klick zeigt das Bild
auf dem ganzen Handy, mittig (Duc 03.11.2026), im Chat genauso. Favour-Fotos bleiben draußen (eigenes Geheimnis, wie im Album).
Die Selfies sind 2:3 bzw. 7:9, das Display etwa 9:19: oben und unten bleibt Schwarz. Für fast vollen Bildschirm wäre 9:16 das
Format neuer Selfies (geparkt in `docs/brain_trust/OFFEN.md`, Duc 03.11.2026).

## Klänge

Ein Klang aus einem Guss (Duc 03.11.2026, Hörseite `docs/abnahme/handy_klang.json`, Urteil daneben). Neue Klänge fast alle
von Universfield (Pixabay Content License), gebaut mit `werkzeuge/eden_rise/sfx_pixabay.py --nur <ids>`; leise Handy-Töne
−22 LUFS, die übrigen −18.

| Wann | Klang |
|---|---|
| Ihre Blase kommt an, Chat oder Nachrichten-Karte offen | `handy_empfang` (New Notification 040), statt `notification` je Blase |
| Neue Nachricht, Handy zu | `notification` (bleibt), Vibration `handy_nachricht` beim Event-Start |
| Duc sendet | `handy_senden` (bleibt, lokal erzeugt) |
| Ihr Herz an Ducs Nachricht | `handy_herz` (Positive Notification), kurz nach der Antwort |
| Videoanruf klingelt | `anruf_klingeln` (Marimba Ringtone, auf 4 s gekürzt), alle 5,2 s |
| Nachts (Phase Nacht oder Uhrzeit 00:00–05:59 im Titel) | Vibration `handy_nachricht` statt Klingeln |
| Duc nimmt an | `anruf_verbinden` (New Notification 07) |
| Angenommener Anruf endet | `anruf_ende` (End Call SFX von Sdanezis, auf 2 s) |
| Duc lehnt ab | `anruf_verpasst` (Notification Beep) |

Offen (geparkt): eigener Klingelton je Frau aus Universfields Ringtone-Reihe.

## Tests

`tests/test_handy.py` (Herz statt Zahlen-Zeile, Status „busy“, englische Ausreden, drei Blasen, Profilbild; Paket 3:
Anruf, verpasster Anruf, Selfie im Faden, nur gesagte Antworten, Favours und Megan draußen),
Vorschau mit Selfie: `tests/vorschau_server.py --tag 3 --frei --event sf_chiara_3_kabine` (setzt das Foto wie im Spiel),
`tests/test_ui_einheit.py` (Wächter der Oberfläche).

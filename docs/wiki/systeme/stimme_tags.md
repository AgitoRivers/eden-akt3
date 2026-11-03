# Stimme: Turbo-Tags und feste Sprachzeilen

> Kanon-Stand 26.10.2026 · Besitz: Items-Sitzung (Händler-Pilot) · Beschluss Duc 26.10.: **jede gesprochene Zeile bekommt mindestens einen Tag**

## Kurz
Eden vertont feste Zeilen lokal mit **Chatterbox Turbo** (Port 8004, Englisch). Turbo spricht Geräusche, die als Tag im Text
stehen: `[laugh]`, `[chuckle]`, `[sigh]`, `[gasp]`, `[cough]`, `[clear throat]`, `[sniff]`, `[shush]`. Die Tags werden nicht vorgelesen
und erscheinen **nie im Spieltext**: Der Bildschirm zeigt den Klartext, nur die Stimme bekommt die Fassung mit Tags.
`[groan]` bleibt draußen: Es verwischte im Test die Wörter („Comandante“ → „counselor“).

## Wo was steht
| Was | Wo |
|---|---|
| Klartext jeder Zeile (Anzeige) | wie bisher in den Daten: Events (`ereignisse.json`), Läden (`laeden.json`), Totò (`werkzeuge/eden_rise/haendler_toto.py`), Jobs, Teile, Tutorial, Anhörung |
| Gesprochene Fassung mit Tags | `module/eden_rise/stimme_tags.json`: eine Liste `{"wer", "text", "gesprochen"}`; `text` ist der Klartext und zugleich der Schlüssel |
| Laden und Abspielen | `kern/stimme.py`: `getaggt(text)` setzt die Tags beim Erzeugen, `ohne_tags(text)` entfernt sie für die Anzeige |
| Vertonen | `python werkzeuge\eden_rise\vertonen_eden_rise.py [--ohne sophia] [--wer toto] [--fehlende-auslassen]` |
| Prüfen | `python werkzeuge\eden_rise\stimme_tags_pruefen.py` (Exit 1 bei Lücken; `--vorlage` druckt Vorlagen für fehlende Zeilen) |

## Neue oder geänderte Zeile
1. Zeile in den Daten schreiben, wie bisher (Englisch, ohne Tag).
2. `stimme_tags_pruefen.py` ausführen: Es meldet **FEHLT** (neue Zeile ohne Eintrag oder ohne Tag), **VERWAIST** (Eintrag, dessen Klartext
   es nicht mehr gibt, also eine umgeschriebene Zeile), **ABWEICHT** (die Fassung ohne Tags ist nicht der Klartext) und unbekannte Tags.
3. In `stimme_tags.json` eine Zeile mit Tag anlegen (oder die verwaiste anpassen), erneut prüfen.
4. Vertonen. Eine Zeile mit geändertem Text bekommt automatisch eine neue Aufnahme, weil der Dateiname aus Stimme und Text mit Tags entsteht.

Fehlt ein Eintrag, wird die Zeile trotzdem gesprochen, nur ohne Geräusch; der Prüfer macht das sichtbar.

## Wie man Tags setzt
- Wenige, gezielte Tags an der Stelle, wo das Geräusch fällt: „Wrapped it twice. [chuckle] Once for the gift, once for your dignity.“
- Tag nach dem Satzzeichen, nicht davor. Ein Tag je Zeile reicht, mehrere nur bei langen Zeilen.
- Passend zur Figur: Holm und Petru nur trocken (Räuspern, Seufzer, Schniefen), Casanova und Lola groß (Lachen, Keuchen), Megan kalt (leises Glucksen,
  Räuspern), Siri und Jana atemlos.
- Nach dem Hören entscheidet Duc; die Ton-Abnahme (`text_abnahme.py` mit `audio_alt`/`audio_neu`) zeigt Zeile mit und ohne Tag.

## Stand
- Alle 1577 festen Zeilen haben einen Eintrag. Vertont mit Tags sind alle außer Sophia (Duc tauscht ihre Stimme) und den Figuren ohne Stimme
  (Nonna Fiora, Isabelle, Frederico).
- Neuvertonung kostet etwa 1,3 Sekunden je Zeile auf der 5090, also rund 35 Minuten für alles.

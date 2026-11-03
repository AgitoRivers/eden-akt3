# Offene SFX-Bausteine (UX-Analyse)

> Stand 26.10.2026 · Besitz: Hauptsitzung (Story) · Grundlage: [`audio_sfx.md`](audio_sfx.md) (Katalog), [`audio_soundplan.md`](audio_soundplan.md) (30 Geräuschfamilien) · an Character Design geschickt

**27.10.2026: weitgehend erledigt** – Ducs Pixabay-Auswahl ist eingebaut (siehe [`audio_sfx.md`](audio_sfx.md), „Pixabay-Auswahl und Ambience“); die Kampf-Töne hängt die Kampf-Sitzung ein. Die Tabelle bleibt als Herleitung.

**Stand vorher:** 51 SFX im Katalog (`module/eden_rise/sfx.json`), alle mit Dateien. Ohne gewählte Variante: `phase_wechsel`,
`limousine_ankunft`, `klemmbrett_schritte`, `kaffee_schluerfen`, `schraubenschluessel_klong`, `hubschrauber_ueberflug`,
`hubschrauber_start`, `katze_miau`, `kamera_ausloeser`, `rudel_ratten`, `rudel_hunde`, `keiler_ansturm`, `ziege_halsband` –
dazu `ui_klick` (wechselt bei jedem Knopf zufällig). Das Plugin `client/plugins/eden-sfx` erkennt Geld, Vertrauen, Begehren,
Handy-Nachricht, Mission, Tag/Phase, Codex, Item, Würfel und Meldung. Alles Neue (Kampf, Expedition, Rasten, Aufträge,
Skills, Werkstatt) ist stumm, und es gibt keine Hintergrund-Schleife.

**Prio:** P0 = in jeder Sitzung ständig hörbar oder großer Moment ohne Ton · P1 = häufig · P2 = Feinschliff

| # | Prio | Moment | Warum (UX) | Klang | Auslöser im Code |
|---|---|---|---|---|---|
| 1 | P0 | Kampf: Ausholen + Treffer | häufigste Aktion, ohne Ton fühlt sich Treffen leer an | kurzer Schwung + dumpfer Treffer, 2 Materialien (Körper / Holz-Metall) | `kampf.zug` |
| 2 | P0 | Kampf: Parade gelungen / perfekt | das Timing-Spiel braucht ein hörbares Echo (Sekiro) | metallischer Block; perfekt = heller Akzent | `parade_aufloesen` |
| 3 | P0 | Kampf: Ausweichen / daneben | sonst klingt ein Fehlschlag wie ein Treffer oder wie nichts | Luftzug, Schritt auf Kies | Kampfergebnis verfehlt |
| 4 | P0 | Kampf: Sieg / Niederlage | Abschluss jeder Begegnung; Musik `kampf_sieg` fehlt auch | Sieg-Akzent 1–2 s; Niederlage: dumpfer Fall, dann Stille | `kampf_schliessen` |
| 5 | P0 | Spezialangriffe im echten Kampf | 16 × 3 Varianten fertig, bisher nur im Labor | Anbindung der fertigen OGGs (Kampf-Sitzung) | `eden-combat` |
| 6 | P0 | Level-Aufstieg, Skill- und Attributpunkt | Belohnungsmoment stumm | aufsteigender warmer Akzent, anders als Würfelerfolg | `award_xp`, `skill_lernen`, Attribut +1 |
| 7 | P0 | Anruf klingelt (Handy-Events, Rast-Anrufe) | Anruf wirkt sonst wie ein Fenster | Vibration + kurzer Klingelton, Annehmen-Klick | Event-Art `handy`, `rast_anruf` |
| 8 | P0 | Explosion / Feuer / Alarm (Nacht 1) | Story-Auftakt ohne Knall | Überschlag + Knall, Feuerknistern-Loop, Alarm-Kurzloop | Szenen `blackout`, `explosion`, `brand` |
| 9 | P1 | Expedition: Ort betreten / nächster Frame | Ortswechsel wirkt wie ein Menü | Schritte auf Kies und Gestrüpp | `ort_frame` |
| 10 | P1 | Rasten am Feuer | Ruhe, Heilung, Gegner kehren zurück (Elden Ring) | Feuer anzünden + warmer Heil-Akzent | `ort_rasten` |
| 11 | P1 | Fund-Karte „A place to rest“ | Entdeckung | leiser Entdeckungs-Akzent, Glut | `exp-fund` |
| 12 | P1 | Spur-Uhr verliert ein Segment | Druck spürbar machen (Frederico) | tiefes Ticken / Herzschlag, einmal | Folge `spur_uhr` |
| 13 | P1 | Auftrag angenommen / Schritt / abgeschlossen | neues Journal ohne Feedback | Feder auf Papier; Abschluss = Siegel | `auftraege.pruefen` |
| 14 | P1 | Neue Waffe (Le Large u. a.) | Übergabe als Achievement | Waffe ziehen + kurze Fanfare | Flag `waffe_*` |
| 15 | P1 | Rosis Werkstatt: Chip einsetzen / Stück fertig | Aufrüstung soll süchtig machen (Diablo) | Klick + Einrasten; fertig = Werkzeug-Klong | `chip_einsetzen`, `werkstatt_morgen` |
| 16 | P1 | Heilung (Elicriso u. a.) | Heiler-Pfad ist neu | warmer kurzer Heil-Akzent | Kampf-Heilung |
| 17 | P1 | Statuseffekte (nass, blutend, brennt, erschüttert) | Zustände sind sonst nur Symbole | je ein kurzer Akzent beim Auftreten | Kampf-Status |
| 18 | P1 | Ambience Deck / Wasser am Rumpf (Loop) | Tageswahl und freie Szenen sind still | leises Wasser, Wind, Tauwerk | Tageswahl, Deck |
| 19 | P1 | Ambience Nacht vor Anker (Loop) | Nacht und Bordrat | Ankerwasser, Holzknarzen | Phase Nacht |
| 20 | P1 | Ambience Macchia (Loop) | Kloster-Frames ohne Ort-Klang | Zikaden, Wind, ferne Ziegenglocke | Event-Art `ort` |
| 21 | P1 | Bordrat-Entscheidung / neue Bordregel | Gewicht einer Crew-Entscheidung | Tischklopfen, Gemurmel | Event `bordrat`, Folge `bordregel` |
| 22 | P1 | Versprechen gegeben / gehalten / gebrochen | Beziehungs-Feedback nur als Text | Handschlag; gebrochen = gedämpfter Moll-Akzent | `ereignisse.tagesende` |
| 23 | P2 | Anhörung: Hammer, OBJECTION!, Notiz-Slam | Gerichtsmoment (Ace Attorney) | Holzhammer, Stinger | `eden-hearing` |
| 24 | P2 | Ambience Hafen / Bar / Piazza (Loop) | Landgänge | Möwen, Takelage; Bar: Gläser, Raumleben | Orte an Land |
| 25 | P2 | Menü: Reiter wechseln / Hinweispunkt | `ui_klick` deckt alles gleich ab | leiser Tab-Klick, eigener „Neu“-Ping | `eden-menu` |
| 26 | P2 | Rückweg / „Quiet“-Frame | Orientierung im Ortskapitel | Schritte zurück; Quiet = Vogelstimmen | `ort_zurueck` |
| 27 | P2 | Tender-Fahrt / Schnellreise | `tender_motor` gibt es, läuft aber nur in 4 Szenen | vorhandenen Ton wiederverwenden | Ortswechsel an Land |

**Reihenfolge (Empfehlung):** 1. Paket Kampf (1–6, 16, 17) · 2. Anruf + Belohnung (6, 7, 13, 14, 15) · 3. Expedition
(9–12, 20) · 4. Ambience (18, 19, 24) leise und unter Sprache gedämpft. Vorher die 13 offenen Varianten und `ui_klick` wählen.

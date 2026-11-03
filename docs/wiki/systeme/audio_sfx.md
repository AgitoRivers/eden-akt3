# Eden SFX – eingebauter Stand

Stand: 18.10.2026. Einmalige Sound-Effekte, vorab bei ElevenLabs erzeugt, nie live.

## Dateien

| Datei | Aufgabe |
|---|---|
| `werkzeuge/eden_rise/sfx_eden_rise.py` | Katalog: Prompt, Länge, Varianten, `wahl` (Ducs Variante), `AUSLOESER` (Szenen/Events) samt Prüfung |
| `werkzeuge/eden_rise/sfx_erzeugen.py` / `Sfx_EdenRise.bat` | Erzeugen (überspringt Vorhandenes) und Vorhörseite `module/eden_rise/sfx/vorhoeren.html` mit Checkboxen + „Auswahl kopieren“ |
| `module/eden_rise/sfx.json`, `module/eden_rise/sfx/` | gebauter Katalog, MP3s `<id>_<n>.mp3`, `index.json` |
| `kern/sfx.py` | `katalog()` (nur gewählte Variante, offene: alle), `audio_path()` (nur `[a-z0-9_]+_[1-9].mp3` aus dem sfx-Ordner), `hint()` (Story-Szene/Event läuft) |
| `eden.py` | `ansicht()` → `v["sfx"] = {katalog, hinweis}`; Routen `/sfx/<datei>` und `/plugins/eden-sfx/eden-sfx.js` |
| `client/plugins/eden-sfx/eden-sfx.js` | Abspielen, Erkennung am Zustandswechsel, Menü „Effektlautstärke“ (an/aus + Regler, lokal gemerkt) |
| `tests/test_sfx.py` | Katalog, Dateiroute, Hinweise, Auslöser-IDs |

## Wann was spielt

| Anlass | Effekt | erkannt von |
|---|---|---|
| Knopf geklickt | `ui_klick` (noch offen → wechselt zwischen allen Varianten) | Client |
| neue Meldung ohne eigenen Ton | `ui_meldung` | Client |
| ungelesene Handy-Nachricht mehr | `handy_nachricht` | Client |
| Vorliebe-Meldung erscheint | `vorliebe_entdeckt` | index.html |
| Vertrauen (inkl. Anteil) steigt / sinkt | `vertrauen_plus` / `vertrauen_minus` | Client |
| Konto steigt / sinkt (Kauf bei Lola: brutzeln) | `geld_ein` / `geld_aus` / `lola_brutzeln` | Client |
| Inventar/Tasche wächst ohne Geldbewegung | `item_erhalten` | Client |
| neuer Auftrag im Angebot | `mission_neu` | Client |
| Missionsergebnis | `mission_erfolg` / `mission_fehlschlag` | Client |
| neuer Tag | `tag_beginnt` | Client |
| Würfel: Wurf / Ergebnis nach der Animation | `wuerfel_rollen`, dann `wuerfel_erfolg|fehlschlag|kritisch|patzer` | index.html um `EdenDice.play` |
| Teamessen gekocht | `glaeser_anstossen` | Client |
| Szene/Event beginnt | laut `AUSLOESER` (Hubschrauber, Blackout, Sturm, Funk, Anker, Klopfen, Sekt, Tender, Platsch) | Server-Hinweis |
| Blackout-Szene endet | `strom_zurueck` (`nach_szene`) | Server-Hinweis |
| Event-Bildschirm geht auf (ohne eigenen Story-Ton) | `ereignis_start` | Client |
| Tageszeit wechselt am selben Tag | `phase_<neue Phase>` (`phase_fruehstueck` … `phase_nacht`), zufällige Variante | Client; fehlt die Phase im Katalog: `phase_wechsel` |
| Anhörung: nächste Phase / Wende | `phase_wechsel` (Sci-Fi-Reveal 3) / `anhoerung_wende` (Reveal 6) | `effekt=` in `kern/anhoerung.py` |
| Codex wächst | `hinweis_gefunden` | Client |
| Geschenk gegeben / Gegenstand benutzt | `geschenk` / `item_benutzen` | Client (letzte Aktion) |
| Selbst kochen (sofort beim Klick) | `kochen` | Client |
| Begehren (inkl. Anteil) steigt | `begehren_plus` | Client |
| Aktion abgelehnt (Server-Fehler, z. B. zu wenig Geld) | `nicht_moeglich` | index.html in `senden` |

Höchstens zwei Effekte je Zustandswechsel, wichtigster zuerst, 380 ms versetzt. Erster Blick nach dem Laden spielt nichts nach.
Je Szenen-/Event-Auftritt genau einmal (Schlüssel aus Durchlauf, Tag, Phase, ID). Ton erst nach der ersten Bedienung (Browser-Regel).

## Pixabay-Auswahl und Ambience (seit 27.10.2026)

Duc hat 38 Töne von pixabay.com gewählt (Pixabay Content License; Quellen: `docs/abnahme/sfx_pixabay/fertig/QUELLEN.md`).
`werkzeuge/eden_rise/sfx_pixabay.py` lädt sie, schneidet lange Töne mit Ausblende, baut Kombinationen (Explosion = Lüfter
+ Knall, Niederlage = Aufprall + Posaune, Werkstatt = Ratsche + Bestätigung, Nacht = Strand + dreimal leises Knarzen,
Hafen = Möwen + Wellen) und gleicht an: Einzeltöne −18 LUFS, Schleifen −30 LUFS. Im Katalog (`sfx_eden_rise.py`, `PX`)
tragen sie `quelle: pixabay` – `sfx_erzeugen.py` erzeugt sie nie neu.

| Moment | Effekt | Auslöser |
|---|---|---|
| Tagesende | `tag_ende` (3 Varianten im Wechsel) | Tag zählt hoch (Client) |
| Neue Handy-Nachricht | `notification` | ungelesene Nachrichten steigen |
| Anruf | `anruf_klingeln` | Event-Art `handy` beginnt, Rast-Anruf erscheint |
| Bordrat | `bordrat` | Event-Art `bordrat` beginnt |
| Expedition | `schritte_kies` / `fund` / `spur_uhr` | nächster Frame / Frame mit Fund-Karte / Spur-Uhr sinkt |
| Auftrag | `auftrag_feder` / `auftrag_siegel` | neuer Auftrag oder Schritt erledigt / Auftrag fertig (Journal) |
| Neue Waffe | `neue_waffe` | Zahl der eigenen Waffen steigt |
| Rosis Stück fertig | `werkstatt_fertig` | Summe der Werkstatt-Stufen im Kampfprofil steigt (am Morgen nach dem Auftrag) |
| Versprechen | `versprechen` / `versprechen_gebrochen` | Meldung oder Ergebnis mit „🤝“ / „💔 Gebrochen“ |
| Nacht 1 | `explosion` | Szene `explosion` (Server-Auslöser) |
| Klick / Menü-Reiter | `ui_klick` / `menue_tab` | beim **Drücken** (pointerdown), vorab dekodiert – keine Verzögerung |
| Kampf, Werkstatt | `kampf_*`, `level_up`, `heilung`, `status`, `chip_einrasten` | Kampf-Sitzung (eden-combat) |
| Anhörung | `anhoerung_hammer`, `anhoerung_einspruch` | Variante 5 = Pixabay, Auslöser in `kern/anhoerung.py` |

**Ambience** (`kern/sfx.ambience`, Client blendet 1,5 s über, Lautstärke = Effekt-Regler, im Kampf still):
Tageswahl/Kabine tags `amb_deck`, abends/nachts `amb_nacht`; Szenen nach Ort (Alvas Bar `amb_bar`, Hafen/Dorf `amb_hafen`,
Deck `amb_deck`, nachts `amb_nacht`, Szene `explosion` `feuer_loop`); Events nach ihrem Bild; Ortskette: Rastplatz
`rast_feuer`, ruhiger (besiegter) Frame `ruhig_voegel`, sonst Macchia `amb_macchia`, Hafen/Rathaus `amb_hafen`.

## Ändern

Variante wählen oder Auslöser ändern: `sfx_eden_rise.py` anpassen → `python werkzeuge\eden_rise\sfx_eden_rise.py` (prüft die IDs)
→ Browser neu laden. Neue Sounds: `Sfx_EdenRise.bat` (Duc startet). Python-Änderungen brauchen Engine-Neustart.

## Phasenübergänge (27.10.2026)

Statt der Bass-Jingles hat jede Tageszeit ihre eigene kurze Erkennungsmelodie, damit man am Klang hört, wo man im Tag steht. Bei jedem Wechsel wird zufällig eine der Varianten gespielt. Quelle: Ducs Pixabay-Auswahl, geschnitten mit `werkzeuge/eden_rise/sfx_phasen.py` (Stille vorn weg, Schnitt + Ausblende, −18 LUFS). Quellen: `docs/abnahme/sfx_pixabay/phasen_fertig/QUELLEN.md`.

| Wechsel zu | ID | Varianten | Klang |
|---|---|---|---|
| Frühstück | `phase_fruehstueck` | 3 | Akustikgitarren-Logos |
| Tag | `phase_tag` | 5 | Bossa / Samba / Merengue mit Schluss |
| Nachmittag | `phase_nachmittag` | 4 | Rhodes |
| Dinner | `phase_dinner` | 5 | Jazz-Akkorde, Jazz-Melodie, Piano-Outro |
| Abend | `phase_abend` | 3 | Lo-Fi-Grooves |
| Nacht | `phase_nacht` | 4 | Lo-Fi, Vinyl |

Der Tageswechsel spielt weiter `tag_ende` (Rhodes-Tape-Stop). `phase_wechsel` ist jetzt der Sci-Fi-Reveal der Anhörung, `anhoerung_wende` (Reveal 6) spielt bei „The Verdict“ und „Revised testimony“ (Lüge nachgebessert), alle anderen Titelkarten der Anhörung spielen `phase_wechsel`.

## Kampf- und Eventmusik (27.10.2026)

Die Musik wählt `kern/musik.py` (`hint`). Jeder Slot hat mehrere Titel; welcher läuft, entscheidet ein fester Hash aus Kampf- bzw. Event-ID (kein Spielzufall). Titel und Lizenzen stehen in `module/eden_rise/musik/auswahl.json` und `CREDITS.md`, die Pixabay-Auswahl lädt `werkzeuge/eden_rise/musik_pixabay.py`.

| Slot | Wann | Titel |
|---|---|---|
| `kampf_normal` | alle Gegner ohne eigene Regel (z. B. Taschendieb) | 5 – Surf Rock, Funk |
| `kampf_tiere` | Keiler, Kloster-Keiler, Hunde (wild, Alpha, Paar), Alpha-Ratte, Schlange, schwarzer Löwe, Wildschwein-Affe | 3 – Tribal Drums, Flamenco-Thrash |
| `kampf_komisch` | Möwe, Ratte, Affe | 2 |
| `kampf_gefaehrlich` | Pirat, Fackelpirat; nachgebesserte Aussage in der Anhörung | 4 – Piraten, Surf Thrash |
| `kampf_boss` | Bossgegner | 2 – Demise, To The Death |
| `kampf_sieg` | einmal nach K.o. oder Aufgabe | Fanfare (4 s) |
| `kampf_niederlage` | einmal nach verlorenem Kampf | Greta Sting |
| `event_ernst` / `_witzig` / `_wholesome` / `_frech` | Events nach ihrem Ton | 2 / 3 / 4 / 4 |
| `anhoerung_gestaendnis` | Anhörung: von Megans „Why?“ bis „The Verdict“ (Client-Vorrang über `EdenMusic.vorrang`) | 3 – ruhiges Piano, Lo-Fi |
| `expedition_macchia` | Kloster-Frames (Event-ID `kl_…`, Art „ort“) | Mediterranean Islands |
| `expedition_hafen` | Hafenkampf-Frames (Event-ID `hk_…`, Art „ort“) | Sunlit Streets |

Übrige Events einer Mission (nicht Art „ort“) laufen weiter nach Ton. Ein Event kann den Slot selbst setzen (Feld `musik`, `"stille"` = keine Musik), eine Begegnung ebenso (Red Trio, 30.10.2026).

**Keine ungewollte Stille mehr (27.10.2026):** Wo keine eigene Regel greift, läuft die *Bordmusik nach Tageszeit*
(`BORD` in `kern/musik.py`): Frühstück → `crew_alltag`, Tag/Nachmittag → `deck_tag`, Dinner → `crew_messe`,
Abend/Nacht → `nachts_vor_anker`. Das gilt für die Phasenwahl („Was machst du am …?“), Anrufe (die Stimme duckt die
Musik), den Hauptsalon und alle anderen Orte ohne Regel, auch nachts. Dazu: Status *Kabine* → `kabine` (3 Titel),
*Cliffhanger* → `mysterium`, *Nach dem Urteil* → wie das Anhörungsende (`event_wholesome` bei Erbarmen/Entlastet,
sonst `event_ernst`) plus „Bittersweet“ (`nach_urteil`). Bewusst still bleiben nur Blackout, Explosion, Brand,
Holms Abschied sowie Rolle und Plädoyer der Anhörung. Aus der Rotation genommen: Fluffing a Duck (komisch), Marty Gots a Plan (witzig).

## Belagerung (01.11.2026)

Ducs Wahl aus `docs/abnahme/sfx_belagerung.html`. Quellen und Schnitt: `werkzeuge/eden_rise/sfx_belagerung.py` (Pixabay Content License). `tk_glocke`, `tk_gitter`, `tk_unit_*` sind Kopien fester Varianten, weil die Originale offen sind.

| Moment | Effekt | Auslöser |
|---|---|---|
| Treffer auf der Karte | `kampf_treffer`, `gun_shot`, `tk_taser` (Chiara), `tk_flinte` (Alva), `tk_klinge` (Klingen), `tk_granate` (Bibi) | `einTreffer` in `eden-tactics.js` nach Angreifer |
| Kirche getroffen, Figur fällt | `tk_kirche`, `tk_ko` | `einTreffer` |
| Roboter zieht, Trupp zieht, Drohne neu | `tk_roboter`, `tk_schritte` (leise), `tk_drohne` | `klang()` vergleicht die Positionen |
| Zug beginnt | `tk_zugwechsel` | Klick auf End round, und wieder nach den Treffern des Gegners |
| Große Tat, Lola, Danzel | `tk_cutin`, `heilung`, `tk_stahlplatte` | `klang()` |
| Barrikade bricht, Haus verloren, Yacht sinkt | `tk_holzbruch`, `tk_haus_weg`, `tk_yacht_sinkt` | `klang()` |
| Welle beginnt, Welle gehalten | `tk_glocke`, `tk_jubel` | Szene `welle_N` / `ende_N`, `falscher_sieg`, `sieg` (`szene_id` in der Ansicht) |
| Verrat, Mochi, Rauch, Glocke zum Sieg | `tk_gitter`, `tk_loewe`, `tk_rauch`, `tk_glocke` | Szene oder ihre letzte Zeile |
| Maxwell trifft | `tk_maxwell_schlag` (Hammer auf Stahl, darunter Tiefe) | echter Kampf (`k.held`), auf der Karte `trefferTon` |
| Flicken | `tk_hammer`, `abbau_daneben`, `tk_bretter` | `eden-abbau.js`, Art `bau` |
| Events | Funk, `tk_unit_*`, `tender_motor`, `tk_bucht`, `tk_glocke`, `tuer_klopfen` (nur Chiara, Rosi, Lola, die anderen stehen im Freien) | `AUSLOESER` |

Während der Belagerung spielt kein Rock-Jingle beim Event-Start (`bl_`), keine Tageszeit-Melodie und kein `tag_ende` (`V.sfx.still`). Ambience: Morgenliste, Flicken und `bl_morgen`/`bl_flicken` `feuer_loop`, Rosis Szenen im Maschinenraum `amb_maschine`. Musik: Wahl der Nacht und stille Nächte `nachts_vor_anker`, Intim-Szenen `naehe` (Sophia `sophia_naehe`), Mr. White `kampf_boss`, Roboter, Schützin, Piraten und Brute `kampf_gefaehrlich`.

Zweite Runde (01.11.): `tk_drohne_ab`, `tk_haus_feuer`, `tk_haus_schreie`, `tk_liste` (Event `bl_morgen_*`), `tk_megan_weg` auf ihrer letzten Zeile im Kriegsrat (`ZEILEN_TON` in `index.html`, ohne Stimme beim Öffnen der Szene). Hintergrund der Karte `amb_taktik` (40 s nahtlos, -30 LUFS), beim Manöver `amb_hafen`. Musik der Karte: Slot `taktik_karte` (Echoes of the Battlefield), die Morgenliste `event_ernst`. Dazu `tk_yacht_riss`: Iron Smash, zwei Schläge mit Trümmern, wenn die Yacht einen Treffer verliert.

## Drehbuch Finale (Duc 02.11.2026)

Nur bestehende Effekte. Drei Stellen:

- **Event-Start** (`AUSLOESER` in `sfx_eden_rise.py`): Funk knackt beim Auftrag Funk, Klopfen bei Minas Türen, Hammer beim Aufbau an Petrus Werkstatt, Gläser in Alvas Bar, Schritte, wenn die Nachtwache zurückkommt, Feder an der Kriegstafel, die Glocke, wenn die Kinder in der Kirche Angst haben.
- **Event-Zeile** (`ZEILEN_TON` in `client/index.html`): Applaus nach Casanovas Rede (`bl_rede`, Zeile 1). Im Bericht ist es erst still, die Glocke kommt mit „Ring the bell“ (`bl_bericht`, Zeile 0).
- **Zeile auf der Taktik-Karte** (neu, `"ton"` an der Zeile, Tabelle `TON` in `taktik_eden_rise.py`, abgespielt in `eden-tactics.js` `sprich`): zum Beispiel Marschtritt der Legion, Hunde, Boote, Roboter an Deck, Schreie in der Post, Bibis Wassergranate, Funk für Pascal, White und alle Funksprüche nach der Nacht, Glocke zum Titel „1924“ und „The Last Wave“, Alvas Flinte, der eine Schlag gegen Minicu, Yasins Kamera, das Blatt, Casanovas Verbandskasten. Die Szenen-Töne am Anfang (`SZENE_TON`) bleiben.
- **Neu von Pixabay (Ducs Wahl 02.11.2026, `docs/abnahme/sfx_pixabay/finale_auswahl.html`, geschnitten in `sfx_belagerung.py`):** `tk_ligeia` (Ligeias Gesang), `tk_minicu_fall` (Heavy Object Falling, danach Body Fall), `tk_applaus` (das Dorf nach Casanovas Rede), `tk_kevin` (Kevin fliegt vom Tor, Welle 6 Runde 4), `tk_rudern` (1924), `tk_papier` (das Papier im Ofen), `tk_kreide` (Start des Berichts), `tk_drucker` (Kriegstafel). Der Applaus im Bericht bleibt mit Absicht aus.
- **Prüfung:** `tests/test_sfx.py` verlangt, dass jeder Ton an einer Kartenzeile im Katalog eine gewählte Datei hat.

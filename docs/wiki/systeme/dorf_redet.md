# Das Dorf, das redet (Legenden und Ruf im Dorf)

Stand 30.10.2026. Duc: „Das motiviert auch, die Missionen zu machen.“ Aus der Brain-Trust-Runde zu Mundi (Option B).
Besitzerin: Hauptsitzung („Ende Rise & Apps“). Entscheidung E-087.

## Was der Spieler erlebt

Nach einer großen Tat spricht sich herum, was Duc getan hat. Am Morgen danach erzählen es die, die dabei waren, fast so,
wie es war. Zwei Tage später hat das Dorf nachgelegt, vier Tage später ist die Geschichte völlig verdreht („you rode the
boar up the town hall steps“). Duc hört die Legende an drei Stellen:

| Einstieg | Wann | Wie |
|---|---|---|
| **Zeit zusammen** | Szenenstart einer freien Szene mit der Figur | Ihre erste Zeile ist die Legende (vertont). Sie landet in ihrem Gedächtnis („I asked Duc about what the village says …“), das Modell spinnt die Szene von dort weiter. |
| **Laden** | Duc öffnet ihren Laden (Alva, Petru, Nonna, Isabelle, Lola, Rosi, Totòs Spind) | Statt des normalen Grußes sagt sie die Legende. Für diesen Besuch (Tag + Phase) bleibt es derselbe Satz, danach gilt sie als gehört. |
| **Handy** | ein bis zwei Tage nach der Tat | Eine Figur fragt nach („Is it true …?“) und Duc antwortet mit 2–3 Chips (kleine Vertrauens-Folgen, manchmal Ruf). |

Jede Zeile hört Duc **einmal**, je Figur höchstens **eine Legenden-Zeile am Tag**. Kein eigener Reiter: Ruf steht als Wort
in der Infokarte hinter dem Stern der Kopfzeile („a stranger · barely known · known · respected · well liked · a legend“), Änderungen
als Zeile in der Tagesmeldung („🗣 The village is talking: …“).

## Regeln (Zahlen)

- **Auslöser:** das Missions-Flag (`TATEN` im Builder). Über Nacht (Tagesende) setzt die Engine das datierte Flag
  `leg_<tat>`; die Tat zählt für den Tag, der gerade endete.
- **Stufen:** Stufe 0 ab Tag +1, Stufe 1 ab Tag +2, Stufe 2 ab Tag +4 (`STUFE_TAGE = (1, 2, 4)`, kurz gehalten, damit eine
  Tat im Baustand schnell wächst; das Spiel läuft bis Tag 35, die Abstände beim Bau von Akt 3 prüfen). Zeilen mit höherer Stufe werden bevorzugt, sobald sie gelten; die frischeste Tat zuerst.
- **Ruf:** eine gute Legende gibt beim Wachsen auf Stufe 1 und auf Stufe 2 je **Ruf +1** (Hafen, Kloster, Berge außer
  Weg B, Kevin, Red Trio). Grotte und Flut-Nacht geben keinen Ruf (Schmuggel-Nähe, unheimlich).
- **Pascal hält den Ruf (Duc 30.10.2026):** Kennt Duc Pascal, fällt das erste Verblassen je Lauf aus, er erzählt die Geschichte weiter (`modul.ruf_schutz`, Flag `ruf_schutz_verbraucht`).
- **Verblassen:** bewegt sich der Ruf **4 Tage** nicht, sinkt er danach **alle 2 Tage um 1** („The village has other things
  to talk about.“). Jede Ruf-Änderung (auch aus Events) setzt die Uhr zurück (`z["ruf_tag"]`, `zustand.folgen_anwenden`).
- **Ausgänge:** Zeilen können eine Bedingung tragen (`wenn`), z. B. Nonna nach dem Kloster nur mit `frederico_lebt` warm,
  mit `kl_frederico_tot` still; Petru nach den Bergen je nach Weg A/C, nach Weg B (kalter Laden) gar keine Legende.
- **Spoilerschutz:** Sätze stehen fest im Builder, das Modell erfindet keine Legende. Keine Täter, keine Chips, keine
  Agenten, die Sirene nie mit Namen.

## Inhalt (Stand 30.10.2026)

66 Kommentare (42 beim Szenenstart, 24 im Laden) und 6 Handy-Nachfragen zu sieben Taten, ausgewogen über 20 Figuren:

| Tat | Flag | Handy-Nachfrage |
|---|---|---|
| Hafenkampf (Tag 2) | `kloster_faden` | Elsa: „How many rats were there?“ (Übertreiben gibt Ruf +1, kostet Elsa) |
| Kloster San Martinu | `kloster_fertig` | Jana: der Speer |
| Berge und Turm | `berge_fertig` | Lola: „is it true there's a BEAR“ |
| Strand-Grotte | `grotte_fertig` | Siri: Yasin will dort filmen |
| Flut-Nacht | `sirene_fertig` | Lea: „is she a human or a fish? can I see her?“ |
| Kevins Dächer | `kevin_fertig` | Casanova: „Did. You. Win?“ |
| Red Trio | `red_trio_fertig` | – (ernste Quest, noch nicht gebaut; Zeilen warten. Danzel redet im Ausgang `rt_ausgang_alle`, Bibi nur mit `rt_bibi_bleibt`, Charly nur mit `rt_charly_bleibt`. Bibi über den Kloster-Löwen: frei = Dank und ein schönes Leben in der Macchia, erlöst = Trauer) |

## Merker: die Familie

**Jede neue NPC kommt in die Familie** (Duc 30.10.2026) und bekommt Zeilen zu den Missionen. `FAMILIE` im Builder;
`tests/test_legenden.py` schlägt fehl, wenn eine Figur in `modul.json` weder in der Familie noch in der begründeten
Ausnahmeliste steht (Holm weg, Megan Zentrale, Sirene, Missions-Fremde). Danzel, Bibi und Charly sind schon drin; ihre
Zeilen warten, bis sie auftreten. Wer eine neue Mission baut, trägt sie in `TATEN` ein und schreibt Zeilen dazu.

## Code

- Builder: `werkzeuge/eden_rise/ereignisse_legenden.py` (TATEN, FAMILIE, ZEILEN mit Turbo-Tags, HANDY) → `legenden.json`,
  Handy-Events in `ereignisse.json`, gesprochene Fassung in `stimme_tags.json` (Quelle „legenden“). Gebaut mit
  `ereignisse_basis.py`.
- Engine: `kern/legenden.py` (Stufen, Auswahl, Tagesende mit Ruf und Verblassen, Ruf-Wort).
- Haken: Szenenstart `kern/szene.py` (erste Zeile, Gedächtnis), Läden `eden.legenden_gruss` (in `laden_auftritt` und beim
  Händler), Tagesende in `eden.py`, Vertonung `leg.<id>` in `/api/zeile` und `vertonen_eden_rise.py`.
- Test: `tests/test_legenden.py`.

## Verwandt (Mundi-Runde, 30.10.2026)

- **Schiedsrichter für freien Text** gab es schon (`szene.probe_noetig`). Neu: das Modell bewertet den Ansatz von −2 bis +2,
  das geht als „A clever/clumsy approach“ auf den Wurf.
- **Reaktion auf freie Zeilen** gab es schon (`kern/reaktion.py`). Neu: zeigt ihr Gesicht in der Antwort Vergnügen, Freude,
  Zuneigung oder Neugier, zählt ein „missfällt“ nicht (eine harte Zeile war dann nicht kränkend gemeint).

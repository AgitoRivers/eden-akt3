# Eden-Kampf

Stand 19.10.2026 · Etappe 3 von 5: Kampfbildschirm mit Parade, angeschlossen als Status `kampf`. Im Sieben-Tage-Bogen startet noch kein Kampf (Etappe 4); Testzugang über den Vorschau-Server.

## Grundidee

Solo-Kampf wie in einem klassischen JRPG, nur Duc. Kein Zeitdruck, keine Timing-Tasten. Der Gegner zeigt seine
nächste Absicht vorher an und hält sich daran. Zwei Wege zum Sieg: Lebenspunkte oder **Fassung** (reden statt schlagen).

## Werte

| | Duc | Test-Dieb |
|---|---|---|
| Lebenspunkte | 46 (bleiben zwischen Kämpfen) | 18 |
| Ausdauer | 6 (bei jedem Kampf voll) | – |
| Fassung | – | 12 |
| Angriff | 6 + **Strength** (Persona 2 → 8) | 6 |
| Schutz | 2 | 1 |
| Proben-SG | – | 12 |

## Befehle

| Befehl | Wirkung |
|---|---|
| Angriff | Schaden = max(1, Angriff + Bonus − Schutz); +1 Ausdauer |
| Fähigkeit | Untermenü, siehe unten |
| Verteidigen | Treffer dieser Runde halbiert (abgerundet, min. 1); +2 Ausdauer |
| Gegenstand | Wirkung des Gegenstands (Tabelle unten), wird verbraucht; **schnelle** Gegenstände (⚡) kosten keinen Zug, höchstens einer pro Runde |
| Fliehen | Ende „Flucht“, kein Gegnerzug |

## Fähigkeiten (Daten in `kaempfe.json`)

| Fähigkeit | Attribut | ⚡ | Würfel | Wirkung |
|---|---|---|---|---|
| ~~Wuchtschlag / Heavy Strike~~ | – | – | – | gestrichen 26.10.2026 – es gibt nur noch Spezialangriffe, Maxwell lehrt Mistral |
| Reden | Charm | 2 | W20 | Fassung −6 (kritisch −9) |
| Beruhigen | Empathy | 2 | W20 | Fassung −5 (kritisch −8), nur bei `beruhigbar` |
| ~~Schwachstelle erkennen~~ | – | – | – | gestrichen 29.10.2026 (Kloster-Simulation: ein Zug für +4 brachte weniger, als er kostete). Erschöpfen kann W3 *Point de Mire*, die Schwäche zeigt die Stärke Köpfchen |
| Finte | Cunning | 2 | W20 | Gegner offen, nächster Angriff ohne Schutz |
| Einschüchtern | Courage | 2 | W20 | Gegner geschwächt für seine **nächsten zwei Angriffe** (je −3, seit 29.10.2026; vorher einer), Fassung −3 (kritisch −6) |
| Improvisieren | – | 0 | sicher | nur mit Handwerk + Multitool/Werkzeugkoffer, einmal pro Kampf: Angriff +4 ohne Schutz |

Patzer bei Proben: Duc ist offen (nächster Treffer gegen ihn +3). Ausdauer ist auch bei Fehlschlag weg.
**Schwäche** des Gegners (Dieb: Courage): Probe mit Vorteil, bei Erfolg zusätzlich Fassung −4 und Gegner offen.
**Unempfindlich** (Gegnerfeld): Fähigkeiten mit diesem Attribut sind mit Begründung gesperrt.

## Zustände (stapeln nicht)

| Zustand | Wirkung | Dauer |
|---|---|---|
| Gegner offen | Ducs nächster Angriff +4 | bis Ende von Ducs nächster Runde |
| Finte | Ducs nächster Angriff ignoriert Schutz | bis Ende von Ducs nächster Runde |
| Gegner geschwächt | sein nächster Angriff −3 | ein Angriff |
| Duc offen | nächster Treffer gegen Duc +3 | ein Treffer |
| Geschützt | Treffer halbiert | diese Runde (Verteidigen) |

## Ducs Stärken

| Stärke | Wirkung im Kampf |
|---|---|
| Köpfchen | sieht die Schwäche des Gegners ab der ersten Runde (Gold; seit 29.10.2026, vorher: Schwachstelle kostet 0) |
| Charme | Reden und Beruhigen mit Vorteil |
| Handwerk | Improvisieren verfügbar |
| Küche | Snacks heilen 10 statt 6 |

## Gegenstände

**Seit 27.10.2026 (Duc + Brain Trust):** Jeder Gegenstand hat **eine** Regel und kontert einen Zustand oder baut eine
Kombo. Heilung rechnet in Prozent der max. LP (bleibt auf jedem Level gleich wertvoll), Snacks heilen weiter fest 6 (mit
Küche 10). **Schnell (⚡):** kostet keinen Zug, Duc handelt danach noch; höchstens ein schneller Gegenstand pro Runde.
Ein Gegenstand ist in der Kampfauswahl nur gesperrt, wenn er gerade nichts bewirken würde (der Grund steht dabei).

| Gegenstand (id) | Woher | Preis | Wirkung im Kampf | ⚡ |
|---|---|---|---|---|
| Plaster (`plaster`) | Totò, Chiara (Frühstück) | 10 € | +10 % LP, stoppt Bluten | ⚡ |
| Bandage (`bandage`) | Totò, Chiara | 25 € | +25 % LP, stoppt Bluten | |
| First Aid Kit (`verbandskasten`) | Totò, Chiara | 60 € | +40 % LP, stoppt Bluten und Brennen (bis 27.10.: 12 fest, auch Alva) | |
| Cooling Spray (`cooling_spray`) | Totò | 20 € | löscht Brennen an Duc, 2 Runden immun gegen Brennen | ⚡ |
| Smoke Pot (`smoke_pot`) | Totò | 45 € | der nächste Gegnerangriff trifft nur Rauch; bis Ende der nächsten Runde gelingt Fliehen ohne Wurf (nicht gegen Bosse) | |
| Herbal Tincture (`antidote`) | Isabelle | 40 € | beendet alle schlechten Zustände an Duc (`kampf.DUC_BAD`) | |
| Espresso (`espresso_single`) | Lola | – | +2 Ausdauer | ⚡ |
| Double Espresso (`espresso`) | Lola, Totò, Alva | 5 € | +3 Ausdauer, Parade-Fenster −10 % in dieser Runde; außerhalb des Kampfs weiter Energie +1 | ⚡ |
| Americano (`americano`) | Lola | – | +1 Ausdauer am Ende jeder Runde, 4 Runden | ⚡ |
| Mate (`mate`) | Lea | – | beendet Betäubt und Geblendet, +1 Ausdauer | |
| Dog Food (`dog_food`) | Lea | – | nur gegen **Tiere**: frisst statt zu beißen, setzt 1 Runde aus, Fassung −4 | |
| Green Tea (`green_tea`) | Sophia | – | Parade-Fenster +15 % für 3 Runden | ⚡ |
| Megaphone (`megaphone`) | Megan (Eden-Shop) | 80 € | **Menschen**: Fassung −5; **Tiere**: 2 Runden erschöpft; sonst gesperrt | |
| Duct Tape (`duct_tape`) | Rosi | – | Schutz +2 für den Rest des Kampfes, nicht stapelbar | |
| Blue Whetstone (`whetstone_blue`) | Rosi | 30 € | Säbel: +3 Schaden für 5 Runden | |
| Grey Whetstone (`whetstone`) | Rosi | 30 € | Messer: +3 Schaden für 5 Runden | |
| Red Whetstone (`whetstone_red`) | Rosi | 30 € | Saufeder: +3 Schaden für 5 Runden | |
| Spikes (`spikes`) | Rosi | 30 € | stumpfe Waffen (Schläger, Schrubber): +3 Schaden für 5 Runden | |
| Match Ammo (`match_ammo`) | Rosi | 30 € | Flinte: +3 Schaden für 5 Runden | |
| Fire Grenade (`grenade_fire`) | Rosi, ab Werkstatt | 40 € | 12 % der Gegner-LP, Brennen ×2 | |
| Water Grenade (`grenade_water`) | Rosi, ab Werkstatt | 30 € | 12 % der Gegner-LP, Nass | |
| Shock Grenade (`grenade_shock`) | Rosi, ab Werkstatt | 40 € | 12 % der Gegner-LP, Strom (auf Nass: Kurzschluss, Gegner setzt aus) | |
| Flash Grenade (`grenade_flash`) | Rosi, ab Werkstatt | 45 € | kein Schaden, Gegner 1 Runde geblendet (sein Schaden halbiert) | |
| Concussion Grenade (`grenade_concussion`) | Rosi, ab Werkstatt | 40 € | 12 % der Gegner-LP, Erschüttert (Rüstung weg; auf Nass: Schlamm) | |
| Shrapnel Grenade (`grenade_shrapnel`) | Rosi, ab Werkstatt | 50 € | 18 % der Gegner-LP, Bluten; gegen Maschinen gesperrt | |
| Space Cake (`space_cake`) | Lola (Kombüse ab Vertrauen 3, Frühstücksgeschenk ab 4) | 15 € | heilt wie ein Snack, dazu **Gras**: +1 Ausdauer am Ende jeder Runde, 5 Runden (Duc 27.10.) | |
| Brownie „Captain's Calm“ (`brownie_calm`) | Lola (Kombüse ab Vertrauen 4) | 12 € | wie Space Cake: Snack-Heilung + Gras, +1 Ausdauer je Runde, 5 Runden | |

**Gras-Kuchen** (Space Cake, Brownie; Duc 27.10.): Wer einen isst, im Kampf oder über „Use“, hat am **nächsten Morgen
Energie −1** (einmal, auch nach zwei Stück). Moral gibt keiner von beiden: was Duc selbst isst, wirkt nur auf ihn.
**Ferrandi-Kontrolle:** An jedem Tagesende findet Leutnantin Ferrandi jeden Kuchen im Inventar mit **10 %** (in der
Kabinen-Truhe 5 %): beschlagnahmt, **Ruf −1**, Codex-Eintrag. Schmuggelware kostet dagegen 20 % und Ruf −2.
Einstellungen `MODUL["gras"]`, Code `handel.gras_gegessen` / `handel.kater` / `handel._gras_kontrolle`.

„Lola/Lea/Sophia/Rosi/Chiara“ heißt: nur als Frühstücksgeschenk der Crew bei Buzzing (`moral.geschenke`, siehe
`interaktion.md`). **Waffenpflege** (Schleifsteine, Spikes, Munition) passt nur zur Waffenart der aktiven Waffe. Man kann
sie im Kampf benutzen (kostet den Zug) oder **vorher im Inventar** („Use“): Dann liegt sie bereit (`z.waffenpflege`) und
wirkt ab dem nächsten Kampf mit dieser Waffenart 5 Runden lang. Der Bonus zählt im Rohschaden (`kampf.raw_hit`).
**Isabelles Kräuterstube** („San Martinu Pharmacy“, Bestellung per Telefon wie bei Megan, Frederico bringt es mit dem
Ziegenkarren) erscheint erst, wenn Duc Isabelle kennt (`laeden.isabelle.erst_bekannt`). **Rosis Werkstatt** hat neben
Chips und Upgrade jetzt „Buy“.

**Granaten** (Duc + Brain Trust 27.10.2026, Akt 2): Rosi baut sie selbst (Feuerlöscher-Reste, Batteriezellen,
Schiffsnägel). In ihrem Sortiment stehen sie erst, wenn die Werkstatt repariert ist (Flag `werkstatt_offen`, Tag 8;
`handel.granaten_frei`), die Waffenpflege dagegen von Anfang an. Der Schaden rechnet in **Prozent der max. LP des
Gegners** (bleibt auf jedem Level gleich wertvoll), geht **durch die Rüstung**, Bosse nehmen davon 75 % (`BOSS_BURN`).
Danach setzt die Granate ihren Zustand über `_apply_state`, also mit allen Reaktionen (Kurzschluss, Dampf, Aufplatzen,
Funken, Schlamm); Spezialangriffe, die Zustände zählen, profitieren von selbst. Granaten kosten den Zug (nicht ⚡), damit
man nicht jede Runde werfen und zuschlagen kann. Die Kampfauswahl zeigt den Schaden („6 dmg“). Regel im Item: Feld
`granate {pct, zustand, runden, stapel}`.
**Animation** (27./28.10.2026): Das Ereignis `gegenstand` trägt `granate: <Zustand>`. Der Client wirft die **freigestellte**
Granate (`fx/wurf_<item-id>.webp`, aus dem Item-Bild mit RMBG-2.0 von `werkzeuge/eden_rise/granaten_freistellen.py`) im
**hohen Bogen** aus Ducs Figur, aber erst 350 ms nach dem Splint-Klick (`WURF_VOR`, Duc 28.10.: erst klicken, dann werfen; die Wurfpose wartet mit), auf den Körper des Gegners (`EdenCombatEffects.play("granate")`): 760 ms Flug, Scheitel
260 px + ¼ der Wurfweite über der Mitte (oben nie aus dem Bild), 2½ Überschläge, Nachzieher und ein Schatten am Boden, dann
90 ms **Hitstop** (die Granate glüht am Körper). `WURF_MS` = 1200 ms ist Splint-Vorlauf + Flug + Hitstop; Schadenszahl, Treffer-Pose, Zustände und Reaktions-Banner kommen erst danach, die Parade startet entsprechend später.
**Einschlag** (alle): Gegner blitzt weiß und wird 15–40 px zurückgestoßen, Kamera-Stoß (Zoom zum Einschlag + Wackeln),
Druckwelle als Ring, durch den der Hintergrund verschwimmt, Vollbild-Blitz in der Elementfarbe. Je Granate eine echte
EmberGen-/LiquiGen-Bildfolge aus dem Effektlabor (aufbereitet von `werkzeuge/eden_rise/granaten_fx.py` nach
`client/plugins/eden-combat/fx/`, Route `/plugins/eden-combat/fx/<name>.webp`):

| Granate | Bildfolge | dazu |
|---|---|---|
| Feuer | `bodenexplosion` am Boden (JangaFX artillery-explosion-1), wächst von unten; der Luft-Feuerball ist raus (zog von links nach rechts, Duc 28.10.) | Glutstriche, Nachbrennen `brand` ab 0,7 s, Brandfleck |
| Wasser | `wasserball` (Ducs LiquiGen-Export 28.10.: Wasserball platzt am Boden und breitet sich als Kuppel aus, ab Bild 12, nur obere Zellhälfte) | Gischtstriche, nasser Schimmer am Boden |
| Schock | `strom` viermal gedreht | Bildschirm flackert, Gegner zuckt hell/dunkel, Funkenstriche |
| Flash | `flare` | 0,3 s komplett weiß, dann 1,7 s Ausblende, danach 2 s überstrahlt und unscharf |
| Erschütterung | `rauchring` (JangaFX smoke-shockwave-2, entfärbt) am Körper + flach am Boden, Staubpilz = späte Bilder von `bodenexplosion` | stärkstes Wackeln, Bild kurz unscharf und entsättigt, Brocken |
| Splitter | `druckstoss` (EmberGen-Rauchpilz) um 40° gedreht und leicht steigend, damit er nach oben qualmt statt nach rechts (Duc 28.10.) | Metallsplitter als schnelle Striche, drei rote Schnittspuren am Gegner |

Die JangaFX-Bögen (Ducs Exporte 27.10., `docs/effekt-auswahl/status-labor/quellen/granaten-jangafx-20261027`) kamen am
28.10. dazu; press-splash wurde verworfen (Pressplatte sichtbar, am Zellrand abgeschnitten), Wasser: seit 28.10. Ducs LiquiGen-Wasserball (`quellen/granaten-jangafx-20261027/wasserball-boden`) statt der Fontäne. Urteil 28.10.: Feuer, Erschütterung, Schock, Flash neu; Splitter alt mit steigendem Rauch.
Vergleich alt/neu mit Ducs Urteil: `werkzeuge/granaten_fx_abnahme.py` (launch `abnahme-granaten-fx`, Port 8391, braucht den
Kampf-Vorschauserver 8369), Urteile in `docs/abnahme/granaten_fx_urteil.json`.
Partikel sind immer Striche entlang der Flugbahn, keine Punktwolken. Die Effekte richten sich nach dem **sichtbaren Tier** (Duc 28.10.): alle Kampfbilder haben dieselbe Fläche, die Tiere füllen sie verschieden aus (Keiler nur die untere Hälfte, schwarzer Löwe fast alles). Der Client misst je Bild einmal die deckenden Pixel (`koerper()` in `eden-combat-effects.js`); Zielpunkt, Boden und Größe beziehen sich darauf. Faktor = sichtbare Höhe / 200 px, mindestens 0,6, **ohne Obergrenze** (vorher gedeckelt bei 1,35, dadurch wirkte der Löwe im Vollbild mickrig). Bei 1920×1080: Löwe ≈ 2,4, Keiler ≈ 1,4. Testkampf: launch `eden-kampf-loewe` (Port 8392, `kloster_8_loewe`, alle Granaten dreifach).
**Ton** (Ducs Wahl 28.10., Abnahme `docs/abnahme/granaten_klang.json` + `_urteil.json`): beim Ausholen `kampf_granate_wurf`
(Splint + Wurf, ElevenLabs), beim Einschlag (nach `WURF_MS`) je Zustand `kampf_granate_feuer` / `_wasser` / `_schock` /
`_flash` / `_erschuetterung` / `_splitter` (Pixabay). Splitter = Granatenknall + 0,25 s später Metallsplitter darüber.
Flash zusätzlich `kampf_granate_pfeifen` 0,5 s nach dem Knall, leise (−27 LUFS) und auf 1 s begrenzt (Duc 28.10.). Knalle sind auf
höchstens 3–3,5 s geschnitten, ohne Stille vorn (der Knall sitzt genau auf dem Bild), −18 LUFS wie die übrigen Kampfklänge.
Gebaut von `werkzeuge/eden_rise/sfx_pixabay.py` (Ziele `kampf_granate_*`), registriert in `sfx_eden_rise.py`.

Code: `kern/kampf.py` (`kampfwirkung`, `gegenstand_grund`, `gegenstand_anwenden`, `_gegenstand_runde`,
`pflege_vorbereiten`, `_granat_schaden`), Daten `werkzeuge/eden_rise/gegenstaende_eden_rise.py` (Art `kampf`, Feld `wirkung`; beim Doppio
Feld `kampf`), Test `tests/test_kampf_gegenstaende.py`.

## Gegner

Absichten laufen in einem festen Muster aus normalem Angriff und Spezialangriffen (SA, schwach `w1`/`w2` oder stark
`s1`/`s2`). Nach einem starken SA ist der Gegner erschöpft. Bei LP ≤ `flucht_ab` kündigt er Flucht an – erledigt Duc ihn in diesem Zug nicht, entkommt er.

### Mehrere Gegner (Duc + Brain Trust 29.10.2026)

„Das macht es auch mehr satisfying, Ratten mit einem Schlag zu töten.“ Ab dem ersten Kampf dürfen bis zu **drei Gegner**
gleichzeitig antreten (`GEGNER_MAX`).

- **Daten:** Eine Begegnung nennt `enemies` (Liste, max. 3) statt `enemy` und `lp_faktoren` (Leben je Mitglied). Rudeltiere
  sind schwach: eine 0,4-Ratte fällt mit einem Schlag, der Alpha bleibt bei 1,0. Doppelte Namen bekommen Buchstaben
  („Rat A“, „Rat B“).
- **Zielwahl wie in Final Fantasy:** erst den Befehl, dann das Ziel (← → / Tab / 1–3 / Klick, Enter bestätigt, Esc
  zurück). Wer schon am Boden liegt, ist nicht wählbar. Steht nur noch einer, entfällt die Wahl.
- **Flächenschaden:** Mistral, Lame de Fond und alle Granaten treffen alle Stehenden. Kein Überschuss: Was ein Schlag
  zu viel macht, verfällt (kein Durchreichen an den Nächsten).
- **Gegnerzug:** Alle Stehenden handeln nacheinander in einer Warteschlange. Jeder Schlag hat seine eigene Parade; der
  Angreifer holt aus, die anderen warten.
- **Rudel-Regel (Balancing):** Ein Mitglied trifft mit Schaden × (0,5 + 0,5 × Anteil): eine 0,4-Ratte mit 70 %, der
  Alpha voll. Erfahrung gibt es je Mitglied × Anteil. Ein Rudel trifft also oft, aber nicht dreimal so hart, und hebt
  das Level nicht schneller als ein Einzelgegner.
- **Einschüchtern:** Das Ziel wird geschwächt wie bisher, die anderen verlieren zusätzlich 2 Fassung (`SCHRECK_ANDERE`).
- **Rundenende:** Brennen, Bluten und Zustände ticken für jeden Stehenden. Jeder kündigt seine nächste Absicht an,
  die Zugfolge oben zeigt die ganze Kette.
- **Sieg:** Der Kampf endet, wenn alle aus sind (KO, Aufgabe oder geflohen). Beute und Geld werden je besiegtem Gegner
  gewürfelt.
- **Gruppen-Sprüche:** Eine Begegnung kann `sprueche` + `sprueche_id` tragen (die Riccis reden als Bande). Die Schlüssel
  sind `kampf.<sprueche_id>.<art>.<n>`, und Vertonung und Turbo-Tags lesen sie mit.

**Welche Kämpfe:** In der Macchia kämpfen Ratten, Schlangen, wilde Hunde und Affen im Rudel. Der Alpha-Keiler
(kloster_2) und der schwarze Löwe (kloster_8) bleiben allein. Am Hafen sind alle Wellen Gruppen (Alpha-Ratte + 2 Ratten,
Alpha-Hund + Hund, Keiler + Bache), dazu die Brüder Ricci zu zweit und die Bande zu dritt mit Mattè.

**Akt 2 in Gruppen (Duc 29.10.2026, „alles, was du vorgeschlagen hast“):** Sammel-Gegner wie „Two A.V. Agents“ oder
„The Big Man and Two Agents“ gibt es nicht mehr, es kämpfen echte Gruppen:

| Kampf | Gruppe (LP-Anteil) |
|---|---|
| Grotte: Treppe, Gitter | Alpha-Ratte 1,0 + 2 Ratten 0,4 |
| Grotte: Kartenspiel | 2 Schmuggler 0,7 / 0,5 |
| Grotte: Fackeln | Fackelpirat 0,8 + Pirat 0,5 |
| Grotte: Rucksack | 2 Piraten 0,7 |
| Flut-Nacht: Treppe | Alpha-Ratte 0,9 + 2 Ratten 0,3 |
| Flut-Nacht: Nachtschicht | Fackelpirat 0,6 + 2 Piraten 0,35 |
| Berge: unterm Turm | 2 Halsband-Wölfe 0,65 |
| Berge: Grat | Agenten-Führer (Blendgranate) 0,8 + Agent 0,6 |
| Berge: rotes Licht | Agent mit Lampen (Wassergranate) 0,8 + Agent (Schockgranate) 0,8 – die Nass-+-Strom-Kombo entsteht von selbst |
| Berge: Ziegenpfad / Rudel | 2 wilde Hunde 0,6 · Alpha-Hund 0,8 + 2 Hunde 0,4 |
| Bergerie (Nacht) | Big Man allein · Big Man 0,9 + Agent 0,5 · Big Man 0,8 + 2 Agenten 0,45 |

Allein bleiben: Vipern, Unit-01, Kevin, Fledermausschwarm/Vampirin, Sirene, U Riscossore, Bache mit Frischlingen, der
Affe am See, der einzelne Agent, der Graue Wolf, Old Grey, das Bärenjunge, der Panther und Wolff.
Regel für neue Kämpfe: mischen, wo es erzählerisch passt, danach Simulation und LP-Anteile/Stufen anpassen.

**Messung (Simulation, 29.10.2026):** Jede Begegnung liegt nah an ihrem alten Einzelwert.
- Berge-Kette ohne Rast: gleich wie vorher.
- Grotte: etwas leichter.
- Flut-Nacht: mittel 64 %, schwach 31 % (Ziel mittel ≥ 60 %, schwach ≥ 30 %).
- Big Man + Agent: 79 % (vorher 78 %).
- Big Man + 2 Agenten: 34 % (vorher 32 %).

Die Stufen der Begegnungen passen zu Ducs Level zu der Zeit und bleiben deshalb gleich.

**Prüfstand:** Die `akt1_*`-Kämpfe (Taschendieb, Möwe, Ratte, Pirat, Fackelpirat) startet kein Event mehr. Sie bleiben als
feste Testkämpfe für die Tests und die Vorschau.

Code: `kern/kampf.py` (`k["gegner"]`, `k["ziel"]`, `ziel_waehlen`, `_gegner_runde`, `_flaeche`, `_ausscheiden`), Client
`eden-combat.js` (`gruppeHtml`, `zielBestaetigen`), Daten `_rudel(...)` in `werkzeuge/eden_rise/kaempfe_eden_rise.py`,
Test `tests/test_mehrgegner.py`.

## Eigenheiten einzelner Gegner und Begegnungen (Red Trio, 30.10.2026)

| Feld | Wo | Wirkung |
|---|---|---|
| `armor_plus` | Gegner | Schutz über dem Stufenwert (Danzels Einlagen: +1) |
| `cls_kampf` | Gegner | Klasse nur für den Waffenvergleich: Der Panzer-Mufflon ist ein Tier, nimmt Treffer aber wie eine Maschine |
| `unterbrechbar` | Gegner | Trifft Duc den Gegner, während diese Absicht angekündigt ist, wird daraus ein normaler Angriff und er verliert 4 Fassung (Bibis Nervous Laugh) |
| Effekt `rudel` | Spezialangriff | Alle anderen lebenden Gegner bekommen 2 Runden +2 Angriff (Hyänen-Alpha) |
| `beistand` | Begegnung | Freunde handeln am Rundenende, ohne eigene Einheit, je Runde eine Aktion. Die erste Liste, deren `wenn` gilt, zählt. Siehe `welt/nebenquest_red_trio.md` |

Besiegte Maschinen sprühen Funken. Die Folge `{"lp_anteil": 0.45}` eines Frames gibt Duc einen Anteil seiner LP zurück (Atempause zwischen zwei Kämpfen).

## Enden

`ko` · `aufgabe` · `entkommen` · `flucht` · `niederlage`. Jede Begegnung legt Text und Folgen fest
(`zustand.folgen_anwenden`), angewendet genau einmal. Niederlage: Spielstand bleibt, Duc behält mindestens 12 LP.
Die Endkarte zeigt dabei ehrlich „❤ 0/max · you come to with 12 HP“ (`ergebnis.wieder_auf`), nicht die schon
aufgefüllten LP (Spieltest 28.10.).

**Anzeigeregeln Fähigkeiten (Spieltest 28.10.):**
- Ist der Gegner gegen das Attribut immun (`immune` in der Gegnerdefinition, z. B. Tiere gegen Reden, Keiler gegen
  Einschüchtern), ist die Karte grau, zeigt keine Erfolgsquote, nur den Grund.
- Einschüchtern heißt im Text „works on most animals too“ – der Keiler ist die Ausnahme und sagt das selbst.
- (bis 29.10.2026) Schwachstelle erkennen ohne Schwäche meldete nicht „none“, sondern „<Gegner> has no weak spot to exploit. The close
  look still pays off.“ Die Erschöpfung (nächster Treffer +4) steht wie immer in der Zeile davor.
- Angriff (+1 ⚡) und Verteidigen (+2 ⚡) zeigen „(full)“, wenn die Ausdauer schon voll ist – sie ist gedeckelt.

Was nach einer Niederlage passiert, legt die Begegnung fest:

| Art | Schalter in `kaempfe_eden_rise.py` | Folge |
|---|---|---|
| normal | – | Kampf vorbei, Duc behält mindestens 12 LP |
| Welle (Hafen) | `neustart_bei_niederlage` | LP voll, derselbe Kampf beginnt neu (E-041) |
| Expedition (Kloster) | `expedition_niederlage` | Expedition scheitert, siehe unten |
| Training (Maxwell) | `training` | kostet keine LP, nur 1 Aktion; Erfahrung nach der Tagesaufgabe (unten) |

**Try again (Duc 03.11.2026, Sitzung Kampf-Tiefe):** Nach einer Niederlage zeigt die Endkarte einmal je Kampf zwei Knöpfe:
**„Try again“** startet denselben Kampf neu, unter denselben Bedingungen: LP und Tasche wie beim ersten Start
(`k["lp_start"]`, `k["inventar_start"]`), Gegner unverändert und wieder voll. **„Accept the defeat“** nimmt die Niederlage an.
Die Folgen der Niederlage (Begegnungs-Folgen, Riccis klauen, Möwe nimmt den Fisch, Expedition scheitert) warten bis zu dieser
Wahl; „Continue“ ohne Wahl zählt als Annehmen. Verliert Duc den zweiten Versuch, gilt die Niederlage wie bisher: zurück auf die
Yacht, eine Phase weg, auf Expeditionen die Beute bis auf ein Stück. Nicht im Training, nicht bei den Hafen-Wellen (sie
starten ohnehin neu), nicht in der Belagerung (eigener Neuversuch) und nicht, wenn Maxwell kämpft. Bosse dürfen. Gegner werden
beim Neuversuch nicht schwächer (Duc: „same fight“). Ein seltener Gegner (`selten`) wird beim Neustart neu ausgewürfelt.
Code `kampf.nochmal_moeglich`, `kampf.nochmal`, `kampf.niederlage_annehmen`, Aktion `kampf_nochmal {annehmen}`, Feld
`ergebnis.nochmal`, Client `endeHtml` in `eden-combat.js`. Test `tests/test_try_again.py`.

### Level-Aufstieg und Attributpunkte (Duc 26.10.2026)

- Je Level-Aufstieg **+1 Attributpunkt** (dazu wie gehabt +5 LP, Ausdauer auf Level 5/9, Skillpunkte auf 3/5/7/9/10).
- Der Hauptpfad hebt sein Attribut **nicht mehr von selbst** – der Spieler verteilt (Maximum 5). Alte Spielstände bekommen
  den früheren automatischen Zuwachs einmalig als Punkte gutgeschrieben.
- **Level-Up-Zeremonie** (seit 28.10.2026, ersetzt die Level-Up-Karte): Jeder Kampf mit Aufstieg endet bildschirmfüllend,
  **auch Maxwells Training** (das ist ein Kampf mit `training`). Ablauf in drei Takten, oben als Schritte „Level · Attribute ·
  Skill“ angezeigt:
  1. **Moment** (ca. 2 s, Level 10: ca. 3 s): Strahlen, Funken, „LEVEL n“ schlägt ein, die Max-HP-Leiste wächst und zählt
     hoch, dann erscheinen die Gewinne (Ausdauer, Attributpunkt, Skillpunkte). Ton `level_up`, auf Level 10 zusätzlich
     `mission_erfolg` und der Untertitel „The peak of your fighting style.“ **Leertaste, Enter, Escape oder ein Klick
     überspringen** den Moment.
  2. **Attribut:** sechs Kacheln mit Wert, Pips, Wirkung und dem Pfad, den das Attribut antreibt; Tasten 1–6 wählen. Nach
     der Wahl zündet die Kachel, und eine Zeile zeigt die Folge, z. B. „Strength 3 → 4 · Mistral 17 dmg → 18 dmg“ (Vergleich
     der Skill-Kernzahlen aus `skill_zahlen` vor und nach dem Klick).
  3. **Skill** (nur wenn Skillpunkte frei sind oder dieses Level welche brachte): kompakter Skill Tree mit allen fünf Pfaden,
     Pfadbildern und Kernzahlen, rechts das Detail mit vollem Text, Rechnung, Hauptpfad-Folge, „▶ Animation“ und
     „Burn in · 1 point“. Lernen **brennt den Skill ein**: Linie läuft vom Vorgänger, das Symbol leuchtet auf und wird
     farbig, die Pfadreihe glüht, Ton `chip_einrasten`. Neuer Hauptpfad → Banner „Main path · …“. Vierter Skill eines Pfads →
     Lichtwelle über die Reihe, Banner „★ … mastered“, Ton `skill_gemeistert` (Cinematic Piano Hit, derselbe Pixabay-Ton wie
     der Hammer der Anhörung; Duc 28.10.2026, Abnahme `docs/abnahme/meister_moment/`) und ein goldener Ring, der über der
     Reihe aufgeht und verweht (IlluGen-Preset `shield_gradient`, das Preset ist statisch: 1024er-Export aus IlluGen 28.10.2026 mit
     Knoten „Export: Color“ hinter Glow, Transparenz aus der Helligkeit, als `fx/meister_schild.png` (768 px);
     Bewegung per CSS. Quelle und Export in `docs/abnahme/meister_moment/illugen/`).
  Normale Level ohne Skillpunkt enden nach Takt 2 mit „You're stronger now.“ und dem Level des nächsten Skillpunkts.
  „Later · Continue“ schließt jederzeit, offene Punkte bleiben (Character-Menü, wie in BG3). Kämpfe **ohne** Aufstieg
  behalten die kleine Ergebniskarte.
  Technik: `client/plugins/eden-skills/eden-levelup.js` + `.css`, aufgerufen aus `endeHtml` in `eden-combat.js`; nur
  Darstellung, die Aktionen bleiben `attribut_steigern`, `skill_lernen`, `kampf_schliessen`. Jede Animation läuft einmal je
  Zustandswechsel, ein bloßes Neuzeichnen zeigt das Endbild; `prefers-reduced-motion` schaltet alles ab.
  Vorschau ohne Spielstand: `python werkzeuge/eden_rise/levelup_vorschau_bauen.py`, dann Launch `levelup-vorschau`
  (Port 8346) → `/docs/effekt-auswahl/status-labor/levelup/` mit Level 3, 4, 9 (Meistern) und 10.
- Was die Attribute im Kampf bringen: Kraft = Schaden · List = Krit +3 % je Punkt (Messer) · Wahrnehmung = Parade-Fenster
  +3 % je Punkt, Point de Mire · Mut = Einschüchtern, Berserker greift mit Mut an · Charisma = Reden · Empathie = Heiler-Pfad.
- Aktion `attribut_steigern` (`kampf.attribut_steigern`), Profil-Feld `attributpunkte`.

### Balancing Kloster (Duc + Brain Trust 26.10.2026)

Anlass: Ein Level-2-Duc (Stand nach dem Hafen, Tag 3) schaffte die 9 Kloster-Kämpfe **nie** – nicht wegen eines einzelnen
Gegners, sondern weil die LP über die Kette wegschmolzen und die Gegner auf eine Level-Kurve gebaut waren, die vor Akt 2
niemand erreicht. Vorgabe Duc: Durch den Hafen gibt es mindestens einen Level-Aufstieg, mit Level 2 muss man das Kloster
fair durchkämpfen können.

| Stellschraube | vorher | jetzt |
|---|---|---|
| Duc Start-LP (`LP_BASE`) | 36 | **46** |
| Duc Grundschaden (`BASE_ATTACK`) | 6 | **8** |
| Gegner Grund-LP / Angriff (`ENEMY_LP`, `ENEMY_ATK`) | 55 / 19 | **40 / 14** |
| Aufschlag je Level über Duc (`LEVEL_GAP`) | +25 % | **+15 %** |
| Parade-Fenster (`PARADE_PLUS`) | – | **+10 %** |
| Kloster-Level | 1–7 | **1, 1, 2, 2, 2, 2, 3, 3, Löwe 3** (Boss ×1,2 LP) |

Ein Verschnaufen nach jedem Sieg (+50 % LP) war kurz drin und ist auf Ducs Wunsch wieder raus: Heilung gibt es nur
an Rastplätzen. Rasten sollen alle Gegner neu erscheinen lassen (Elden-Ring-Prinzip) – die Rast-Mechanik kommt später.

Gemessen mit `werkzeuge/kampf_sim_kette.py` (Tag-3-Bot, Level 2, 150 Läufe je Stufe), ganze Kette gut / mittel / schwach:

| Rast (volle LP) vor … | gut | mittel | schwach |
|---|---|---|---|
| keinem Kampf | 5 % | 1 % | 0 % |
| Hütte und Lager (2 Rasten) | 67 % | 23 % | 1 % |
| jedem zweiten Kampf (Keiler, Affe, Wildschwein+Affe, Löwe) | 96 % | 67 % | 10 % |
| jedem Kampf ab dem Keiler | 100 % | 95 % | 67 % |

Ohne Verschnaufen hängt das Kloster an den Rastplätzen: mit 4 Rasten erreicht mittlere Parade das Ziel, schwache nicht.
Ziel für jede neue Kette: mittel ≥ 60 %, schwach ≥ 30 %, der Boss ist die Hürde – **vor dem Bauen simulieren.**
Die Regel-Tests (`tests/test_kampf.py`) rechnen bewusst mit den alten Zahlen; `Balance` prüft die neuen.

**Kloster-Prüfung 29.10.2026** (Spieltest: 6 von 6 Läufen gescheitert; `werkzeuge/kampf_sim_kloster.py`, echter Stand
Tag 4–7 = Level 2, 51 LP, Terremoto, Mistral, kein Heil-Item; Hauptweg mit den Rastplätzen, 150 Läufe je Zelle, ganze Kette):

| Spielweise | Parade gut | mittel | schwach |
|---|---|---|---|
| Spieltest-Bot, ohne Rast (vorher) | 27 % | 4 % | 1 % |
| Bot mit Rast an jedem Rastplatz (vorher) | 96 % | 76 % | 23 % |
| Bot mit Rast + Verteidigen gegen starke Spezialangriffe (vorher) | – | 88 % | 39 % |
| Bot, ohne Rast, Parade +20 % | 37 % | 12 % | 1 % |
| Bot mit Rast, Parade +20 % | 97 % | 87 % | 45 % |

Befund: Es liegt an der Spielweise, nicht an den Werten. Rasten ist der größte Hebel; Schwachstelle und Einschüchtern
kosten heute mehr, als sie bringen (ein ganzer Zug für +4 / −3). Die Hürde ist der Affe am Lager (`kloster_7_affe`).
Umgesetzt 29.10.2026: Schnellreise zu entdeckten Rastplätzen (`interaktion.md`), Schwachstelle gestrichen, Einschüchtern aufgewertet. Vorschläge waren: Rast vor dem Löwen sichtbar machen, Schwachstelle/Einschüchtern aufwerten, Niederlage = zurück zum
letzten Rastplatz statt Kapitel von vorn.

**Nachmessung 29.10.2026 abends** (Schwachstelle gestrichen, Einschüchtern zwei Angriffe, Köpfchen zeigt die Schwäche,
Parade +20 %; dazu **Schnellreise**: nach einer Niederlage beim nächsten Besuch zum letzten erreichten Rastplatz).
Ganze Kette in einem Anlauf / geschafft nach höchstens 1 · 2 · 3 Anläufen (= Phasen):

| Spielweise | Parade gut | mittel | schwach |
|---|---|---|---|
| Spieltest-Bot, ohne Rast | 37 % · 45/97/99 % | 12 % · 9/58/94 % | 1 % · 1/11/51 % |
| Bot mit Rast | 97 % · 98/100/100 % | 87 % · 82/98/99 % | 45 % · 42/66/84 % |
| gute Spielerin (Einschüchtern, Verteidigen, Rast) | 97 % · 98/99/100 % | 85 % · 83/99/100 % | 37 % · 37/60/71 % |

Ziel (mittel ≥ 60 %, schwach ≥ 30 %) ist erreicht; der Affe am Lager bleibt die Hürde, wird aber mit der Schnellreise
nicht mehr zum Kapitel-Neustart. Seine Werte bleiben (Duc: nur ändern, falls nötig).

### Die Brüder Ricci – Taschendiebe am Hafen (Duc + Brain Trust 29.10.2026)

Zufallskampf, wenn Duc **Alvas Bar oder Petrus Werkstatt** betritt (Client `ortBetreten` → Aktion `laden_besuch`):
**5 % je Besuch**, ab Tag 3, höchstens alle 2 Tage (feste Würfel je Spielstand, Tag und Besuch). Es baut sich auf – jede
Begegnung ist die nächste Stufe, egal wie sie ausging:

| Stufe | Gegner | Level | klauen bei Niederlage/Flucht |
|---|---|---|---|
| 1 | Fabbiu *oder* Santu allein (laestig) | Duc −1 | 1 Verbrauchsgegenstand (ohne einen: 20 €) |
| 2 | The Ricci Brothers (gefaehrlich, Doppelschlag) | Duc | 2 (je fehlendem 20 €) |
| 3 | The Ricci Gang – mit Cousin Mattè (gefaehrlich, Haymaker) | Duc +1 | 3 |

- Geklaut werden nur Verbrauchsgegenstände (Kampf, Snack, Gericht, Verbrauch) – nie Geschenke, Andenken, Story-Dinge,
  Charms, Werkzeug. Das Gestohlene liegt in `z.ricci.beute` (für Elsas Nebenquest, folgt).
- **Sieg:** sie lassen das zuletzt Gestohlene fallen, sonst ein paar Euro aus ihren Taschen. Ein Ricci flieht nie.
- Das Ziel des Kampfes sagt vorher, was auf dem Spiel steht (*„They want: 2 things from your bag“*).
- **Sie sticheln vertont** (`sprueche` je Gegner: start/runde/gewinnt/verliert, Schlüssel `kampf.<gegner>.<art>.<n>`):
  nach jedem Zug Ducs ein Satz, am Ende einer zum Ausgang – unten rechts im Kampf wie die Hinweise der Sirene.
- Nach Stufe 3 hören sie auf; Flags `ricci_1`–`ricci_3`, die Ergebnis-Karte verweist auf Elsa.
- Stimmen: Fabbiu (19, nasal, weinerlich) und Santu (22, schleppend, höhnisch), korsisches Französisch per Voice Design
  (`stimmen_design.py`, Abnahme `docs/abnahme/stimmen_diebe/`), nicht im ElevenLabs-Konto gespeichert.
- Sprites: Fabbiu = `Thief`, Santu = `ThiefArab`; Gruppenbilder für Stufe 2/3 sind offen (bis dahin `Thief`/`ThiefAlpha`).
- Daten `werkzeuge/eden_rise/kaempfe_hafen.py`, Regeln `kern/taschendieb.py`, Test `tests/test_taschendieb.py`.

### Grauzonen-Regel (E-073, Duc 26.10.2026)

Wer stirbt und wer nicht, hängt davon ab, ob der Gegner Opfer oder Täter ist. Das Spiel feiert keinen Tod.

| Gegner | Beispiele | Ausgang `ko`/`aufgabe` | Sprite |
|---|---|---|---|
| **Opfer** | Tiere mit Halsband, gezwungene Menschen | Halsband bricht, der Chip fällt, sie fliehen | `flee` (nicht `defeated`) |
| **Tiere ohne Halsband** | Ratte, Schlange, verwilderter Hund | sie fliehen | `flee` |
| **Wer Duc töten will** | Agenten auf Leben und Tod, Piraten | dürfen sterben, ohne Jubel | `defeated` |
| **Echte Bestien** | Seeungeheuer, Hai | dürfen sterben, ohne Jubel | `defeated` |

`surrender` bleibt für alle, die über ihre Fassung aufgeben. Die Texte der Begegnungen folgen dieser Regel. Bisher wählt
die Engine das Ende-Sprite noch fest nach Ausgang (`ko` = `defeated`); ein Schalter je Gegner für `flee` ist offen.

### Expeditionen (Duc 26.10.2026, `kern/expedition.py`)

Längere Wege weg vom Schiff, zuerst das Kloster (Akt 2). Die Frame-Kette startet sie mit der Folge
`{"expedition": "kloster"}` und beendet sie bei Erfolg mit `{"expedition": "ende"}`. Beim Start merkt sich die Engine
Inventar und Chips.

**Niederlage in einem Expeditions-Kampf:**
1. Schwarzblende (der Niederlagen-Text endet mit „everything goes black“).
2. Im Ende-Bildschirm wählt Duc **ein** Stück aus der Beute, die er seit dem Start gefunden hat (Gegenstände, neue oder
   verbesserte Chips) – oder nichts. „Continue“ geht erst nach der Wahl.
3. Alles andere Gefundene ist weg; ein verbesserter Chip fällt auf seine alte Stufe zurück. Mitgebrachtes bleibt.
   Beweisstücke (Art `beweis`) zählen nie als Beute.
4. Duc wacht auf dem Schiff auf, LP voll, **eine Phase ist verloren**.
5. Erfahrung und Level bleiben. Die Engine setzt die Flag `expedition_<id>_gescheitert` für die Story.

### Expeditions-Bildschirm (Plugin `eden-expedition`, 26.10.2026)

Frames eines Ortskapitels (Event-Art `ort`) zeichnet das Plugin statt des normalen Ereignis-Bildschirms
(Mockup `docs/abnahme/expedition_mockup/`):

- **Titelkarte:** Beim Öffnen eines neuen Frames erscheint der Ortsname groß und verblasst nach etwa 4 Sekunden.
- **Oben links:** kleines Ortsschild und eine **Mini-Karte, die mitwächst**: besuchte Frames gold, der aktuelle hervorgehoben,
  davor ein „?“ im Nebel, solange es weitergeht. Keine Gesamtzahl, damit die Länge des Wegs nicht verraten wird
  (`z.ort_weg`, gesetzt in `eden.ort_frame`).
- **Oben rechts (nur ohne Figur im Bild, seit 01.11.2026):** Duc mit Ausschnitt seines Inventar-Porträts (Frontansicht, wechselt mit Jacke und Waffe), Level, Waffe,
  LP, Ausdauer und die **Beute-Tasche** der laufenden Expedition. Strom, Diesel, Moral und Ruf sind während des Ausflugs ausgeblendet. Regeln: `ui_stil.md`, „Figur vor Oberfläche“.
- **Figuren (seit 29.10.2026, Duc: „Warum ist Madame Casanova nicht als Sprite zu sehen?“):** Die Personen des Frames
  (`personen` im Builder → `e.rollen` in der Ansicht: handelnd, sprecher, links/rechts, betroffen) stehen groß rechts im
  Bild, der Textkasten rückt dafür nach links (Klasse `exp-mit-figuren`). Wer gerade spricht (eine Zeile im Frame oder
  die Antwortzeile nach der Wahl), steht vorn und hell, die anderen etwas kleiner und dunkler. Nach der Wahl zeigt die
  antwortende Figur die Stimmung ihrer Antwort, die kleine Kopie im Ergebniskasten entfällt. Höchstens 4 Figuren.
  Code: `figuren()` in `client/plugins/eden-expedition/eden-expedition.js`, Stil `.exp-figur` in der CSS. Betroffen
  waren 86 von 146 Frames (Hafen, Kloster, Berge, Grotte). Prüfung im Browser (Casanovas Auftrag, Tag 10).
- **Unten:** Text des Frames und die Wahlen. Jede Wahl sagt, was folgt: ⚔ Kampf, 🎲 Probe (Attribut und SG),
  ↩ „Ends the trip“. **Welcher Gegner wartet, bleibt verborgen** („Something is waiting“). Der Jacken-Chip
  **Scout** (Items: Radio Ear / Signal Hunter / Know Thy Enemy) deckt auf, aber nur **eingebaut in der getragenen Jacke**
  (`kampf.aufklaerung`): Stufe I zeigt Kopf und Namen – Tiere ohne Halsband (Ratte, Schlange, `halsband: false`) nur als
  „Animal“, denn der Chip hört Halsbänder; Stufe II zusätzlich Level und Bedrohung (`kern/expedition.wahl_info`).
  Stufe I schenkt Rosi bei der Werkstatt-Eröffnung (Tag 8), Stufe II droppt das Hunde-Paar.
- **Interface ausblenden:** Taste **H** oder der Knopf unten rechts. Dann bleibt nur das Bild, die Einstellung wird gemerkt.

### Training mit Tagesaufgabe und „Chase them off“ (Duc + Brain Trust 02.11.2026, Sitzung Kampf-Tiefe)

Anlass: Die Spieltest-Bots vom 02.11. kämpften im Schnitt 78-mal je Lauf. Davon waren 12 Trainings mit Maxwell (bei
zwei Spielertypen über 40, weil Training nichts kostet) und viele Kämpfe gegen Gegner weit unter Ducs Level. Das wirkte
wie Grind. Ziel: weniger leere Kämpfe, und die übrigen haben ein Risiko oder lehren etwas.

**Training mit Aufgabe** (`kern/tutorial.py` `aufgabe_vergeben`, `aufgabe_werten`; ändert E-042 „Training jederzeit,
wenig Erfahrung“):
- Training bleibt jederzeit möglich und kostet weiter 1 Aktion. Das **erste Training am Tag** stellt eine Aufgabe, sie
  steht als Ziel oben im Kampf („Maxwell's task: …“).
- **Gewonnen und Aufgabe geschafft:** Erfahrung ×0,5 (`XP_AUFGABE`, doppelt so viel wie früher). **Gewonnen ohne
  Aufgabe:** ×0,25 wie früher (`XP_OHNE`). Die Ergebniskarte sagt, ob die Aufgabe geschafft ist.
- **Jedes weitere Training am selben Tag** ist eine Extrarunde: Ziel „Extra round. No XP today – muscles grow when you
  sleep, brother.“, keine Erfahrung (`XP_EXTRA`). Kein Verbot, nur kein Lohn. Kraft +1 je Akt, Janas und Chiaras Zähler
  laufen wie bisher bei jedem Training.
- Fünf Aufgaben, als nächste kommt die mit den wenigsten Erfolgen (Gleichstand: reihum nach Tag), so trifft jeder Spieler
  alle:

| id | Aufgabe | Zähler im Kampf |
|---|---|---|
| `serie` | drei perfekte Paraden in Folge, dann gewinnen | `k["stat"]["serie_max"]` |
| `erschoepft` | Maxwell erschöpfen, dann ein Spezialangriff auf ihn | `stat["spezial_erschoepft"]` |
| `konter` | der letzte Schlag ist ein Konter (perfekte Parade oder geladener Konter) | `stat["sieg_konter"]` |
| `wenig` | gewinnen und höchstens 20 % der LP verlieren | `lp_start` gegen LP am Ende |
| `schnell` | in höchstens 4 Runden gewinnen | `k["runde"]` |

Erfolge je Aufgabe stehen in `z["training_kampf"]["aufgaben"]`, der Tag der letzten Aufgabe in `aufgabe_tag`. Die Zähler
schreibt `kern/kampf.py` (`zug`, `parade_aufloesen`), bewertet wird einmal in `_finish`.

**Chase them off** (`kern/kampf.py` `verjagbar`, `verjagen`; Vorbild EarthBound): Liegt eine Begegnung **mindestens
2 Level unter Duc**, zeigt die Expeditions-Karte unter der Kampf-Wahl eine zweite Wahl „Chase them off · no fight ·
half XP · no loot“. Ein Klick: kein Kampfbildschirm, Meldung „You step forward with <Waffe>. They take one look at you and
run.“, halbe Erfahrung eines Siegs (`VERJAGEN_XP`), keine Beute, kein Geld. Der Ort ist danach bis zur nächsten Rast
ruhig wie nach einem Sieg (`ort_besiegt`).
- Nie verjagbar: Bosse, `untouchable`, Begegnungen ohne `flee_allowed` (Keiler, Affe im Hinterhalt), `level: "duc"`,
  Training, `selten`, Banden mit `sprueche` (Riccis), `beistand` (Red Trio), Hafen-Wellen (`neustart_bei_niederlage`),
  und Kämpfe, die nur nach einer misslungenen Probe kommen.
- Der Server prüft selbst (`event_wahl` mit `verjagen: true`, sonst Fehler „You can't chase this off.“), der Client zeigt
  die Wahl nur, wenn `wahl_info` `verjagbar` meldet (`eden-expedition.js` `verjagenHtml`).
- Die Spieltest-Bots nutzen die Wahl noch nicht.

Tests: `tests/test_tutorial.py` (Aufgabe, Extrarunde, alle fünf Prüfungen), `tests/test_verjagen.py`.

### Kloster San Martinu (Akt 2): die Kämpfe

Nur mit Terremoto (`weapon: bat`), Element Erde, Expeditions-Niederlage, Level flach 1–3 (Balancing oben). Zwei Tiere auf einmal kann die Engine nicht;
das zweite Tier kommt als starker Spezialangriff („The Second Dog Joins In“), wie im Hafen.

| Frame | Begegnung | Gegner | Sprite | Level | Besonderes |
|---|---|---|---|---|---|
| 1 | `kloster_1_ratte` | Rat | Rat | 1 | – |
| 1 | `kloster_1_schlange` | Snake | Snake | 1 | Gift: geschwächt |
| 2 | `kloster_2_keiler` | Alpha Boar | WildschweinKeiler | 2 | Zwischenboss, seltener Chip (Wucht 2), keine Flucht |
| 3 | `kloster_3_hund` | Feral Dog | Dog | 2 | Biss: blutend |
| 5 | `kloster_5_affe` | Ape | Ape | 2 | Halsband-Chip (Technik 1), Steinwurf nur ausweichen |
| 6 | `kloster_6_hunde` | Two Feral Dogs | Dog | 2 | zweiter Hund als SA |
| 6b | `kloster_6b_wildschwein_affe` | Boar and Ape | Wildschwein | 3 | Affe springt dazu als SA |
| 7 | `kloster_7_affe` | Ape | Ape | 3 | Hinterhalt, keine Flucht |
| 8 | `kloster_8_loewe` | The Black Lion | LionAlpha | 3 | Boss, tödlich; Löwen-Chip kommt aus der Szene danach |

Hintergründe: die Ort-Bilder `eden_rise_macchia_path.png` … `eden_rise_lion_den_cave.png` in ST/backgrounds.

## Dateien

- `kern/kampf.py` – Regeln (`starten`, `zug(befehl, ziel)`, `schliessen`, `ansicht`, `faehigkeiten`, `gegenstaende`)
- `werkzeuge/eden_rise/kaempfe_eden_rise.py` → `module/eden_rise/kaempfe.json` (mit Prüfung)
- `tests/test_kampf.py` – Regeln mit festen Würfeln
- `tests/kampf_konsole.py`, `Kampf_Test.bat` – Testkampf im Terminal (`--items` für das Inventar, Parade per Wurf)
- `tests/test_kampf_server.py` – Ablauf über die Engine-Aktionen
- `werkzeuge/kampf_bilder.py`, `Kampf_Bilder.bat` – Kampfbilder ins Modul

## Parade (Etappe 3)

Nach Ducs Zug kündigt sich der Gegnerschlag an, der Kampf steht in Phase `parade`. Der Client spielt eine
Reaktionsprobe und schickt das Ergebnis (`kampf_parade`):

| Ergebnis | Wirkung |
|---|---|
| `perfekt` | kein Schaden, Konter (Ducs Angriff), Gegner offen, +1 Ausdauer; 3 perfekte in Folge: Fassung −4 |
| `gut` / `ausweichen` | Schaden halbiert (min. 1) |
| `verfehlt` | voller Schaden |

**Parade-Fenster +20 %** (Duc 29.10.2026, Steam-Feedback „für ältere Spieler“): Gut- und Perfekt-Fenster aller Gegner sind
noch einmal 20 % größer (`PARADE_PLUS` = 1,1 × 1,2). Goldzone und Balken im Client wachsen mit, weil beide aus dem
Fenster vom Server kommen. Mittel: Gut 211 ms, Perfekt 79 ms; stark: Gut 145 ms, Perfekt 53 ms.
| `wuerfeln` | Perception-Probe statt Reaktion (SG je Tempo 10/13/16): kritisch = perfekt, Erfolg = gut |

Art der Probe je Gegner (`parade` in `kaempfe.json`): **sprite** und **skala** (seit 25./26.10.2026 dieselbe Zwischensequenz:
Hintergrund dunkelt ab, alles außer dem Gegner tritt zurück, „PARRY!“, eine Zeile mit dem Namen des Angriffs (seit 03.11.2026 ohne Schaden), darunter die
Leiste; nach 0,6 s Lesezeit läuft der Marker in 1,7/1,5/1,25 s (leicht/mittel/stark) auf die goldene Zone, genau dort
kommen Funke und Schlag; Drücken in der Lesezeit zählt nicht; der Tastenhinweis steht nur im Tutorial), **ring** (früher ein Ring, seit 03.11.2026 dieselbe Leiste mit breiter blauer Zone; D = Ausweichen, Leertaste = Parieren; Ablauf siehe „Lesen statt rechnen“).
Absichten mit `nur_ausweichen` sind nicht parierbar. Zeitfenster je `tempo`: leicht 242/99 ms, mittel 176/66 ms,
stark 121/44 ms (gut/perfekt, seit 26.10.2026 +10 %); **Lage der goldenen Zone je Gegner** (`parade_ziel`, 55–85 %, nie am Anfang): Schlange 85, Möwe und Löwe 80,
Hunde und Maxwell 75, Ratten, Dieb, Pirat 70, Affe und Fackelpirat 65, Keiler 60 – der Marker trifft das Gold trotzdem genau beim Schlag; starker SA ×0,8, vorher Verteidigen ×1,5, Perception +3 % je Punkt.
Im Bildschirm schaltet „Parade: Reaktion/Würfeln“ auf den Wurf um (wird im Browser gemerkt).

## Lesen statt rechnen (Duc 03.11.2026, Sitzung Kampf-Lesbarkeit)

Vorbilder Sekiro und Clair Obscur: **Man gewinnt, weil man die Paraden lernt, nicht weil man den Schaden kennt.** Deshalb
gibt es keine Schadensvorschau für Gegnerangriffe, nirgends (Zeichen, Zugfolge, Gegnerleiste, Parade-Zeile). Der Test
`tests/test_kampf_lesen.py` wacht darüber. Zwei Paraden je Runde bei zwei Gegnern bleiben; jede soll einen eigenen Rhythmus haben (Finten unten).

| Baustein | So geht es | Code |
|---|---|---|
| **Signal beim Ausholen** (Duc 03.11.2026: „kein Abzeichen, in Sekiro rennt kein Gegner mit Parry herum“) | In der Planung steht am Gegner **nichts**. Die nächste Aktion steht nur oben in der Zugfolge (Name, ohne Zahl). Greift ein Gegner an, holt er aus und **leuchtet 1 Sekunde** (lang genug, dass man es auch bei einem Ruckler sieht): **hell (Perle) = parieren**, **blau = nur ausweichen**. Erst dann kommt die Leiste. Gold gehört nur noch Ducs Hauptaktion. Zum Ausholen der Klang `kampf_schwung`. | `EdenQTE` (`client/plugins/eden-combat/eden-qte.js`, `TELL`), CSS `.gsprite.tell-par` / `.tell-aus` |
| **Parade-Leiste** | Kein „PARRY!“ mehr. Klein der Name des Angriffs, darunter eine Glasleiste, **22 px hoch** (barrierefrei, Duc 03.11.): heller Kern (perfekt), helle Zone (gut), Lichtstrich als Marker; die Taste steht darunter. **Perfektes Fenster +10 %** (`PERF_PLUS` in `kern/kampf.py`: mittel jetzt 87 ms, stark 58 ms, leicht 131 ms). | `EdenQTE.start`, CSS `.qte*` |
| **Ausweichen ist ein Kreis** | Bewusst eine andere Probe als Parieren (Duc 03.11.): ein blauer Kreis zieht sich auf den Zielring zusammen, das blaue Band ist das Fenster. **Deutlich schneller** als die Leiste (`AUSWEICH_TEMPO` 0,6, Duc 03.11.: 0,8 war zu leicht), das Fenster bleibt **1,5-mal so breit wie das gute Parade-Fenster** (`AUSWEICH_FAKTOR`). Gegner, bei denen man wählen darf (Affe), zeigen im Kreis zusätzlich einen hellen Ring: Leertaste dort = perfekte Parade. | `eden-qte.js`, CSS `.qte-kreis` |

| **Ducs W20 im Kampf** | Reden, Einschüchtern und andere Proben zeigen den goldenen `eden-dice` kompakt (0,8 s) über Ducs Karte. Danach bleibt dort das Ergebnis mit Rechnung stehen („Charisma check · needs 13 · 12 / 17 → 17 +3 Charisma = 20 · Success“), bis Duc den nächsten Befehl gibt. Vorher lief der Würfel unsichtbar hinter den Panels. | `wurfRestHtml`, CSS `.kampf > .eden-dice-card`, `.kampf-wurf` |
| **Perfekte Parade mit Gewicht** | Im Moment des Drückens: Klang, heller Blitz (Perle) (0,4 s Ausblenden), Funke am Gegner und 120 ms Halt (Hit-Stop, ui_stil 2b: Rückmeldung 100–150 ms), erst dann Treffer am Gegner und Ducs Konter. Der Klang kommt nur einmal (nicht noch einmal mit der Serverantwort). Bei reduzierter Bewegung kein Halt, nur Klang und Blitz. Klang `kampf_parade_perfekt` (Duc, Klangrunde 1). Das Urteil „PERFECT PARRY!“ steht in Perle statt Gold. | `halt()`, `HALT_MS`, Klasse `kampf-halt` am `#app` |
| **Bestiarium** | Nach der ersten guten oder perfekten Parade einer Gegnerart steht ihr Rhythmus im Codex (Seite **Bestiary**): Name, wie oft pariert, Tempo der Ausholbewegung, Finten, welche Angriffe man nur ausweichen kann. Nie Zahlen. Im Kampf meldet eine Karte „New in the Bestiary“. Gleicher Name mit gleichem Rhythmus zählt einmal. | `z["bestiarium"]`, `kampf.bestiarium_merken`, `kampf.rhythmus`, `kampf.bestiarium`; Codex in `eden-menu.js` |

### Rückmeldung bei der Parade (Duc + Brain Trust 03.11.2026: „satter, ermutigend, nicht verspielt“)

Vorbilder: Sekiro (jede Abwehr Funke und Klang), Clair Obscur (Ton je Kettentreffer, Belohnung am Ende), Hi-Fi Rush („early/late“
statt nur Fehler), Balatro (Ton steigt mit der Serie). Grundsatz: die Belohnung wächst mit dem Können, nie zwei Klänge übereinander.

| Moment | Bild | Klang |
|---|---|---|
| Kettentreffer pariert (nicht der letzte) | die Zone pulst hell auf und dimmt dann (300 ms) | leise (55 %), je Treffer etwa ein Halbton höher: `kampf_parade`, `kampf_kette_2`, `kampf_kette_3` |
| Perfekte Parade | heller Blitz, 120 ms Halt, dazu platzt vom Kern ein Ring auf (400 ms) | Klang `kampf_parade_perfekt` beim Drücken, nach dem Halt der positive Ausklang `kampf_parade_erfolg` (Ducs eigener Klang „Sucess Parry“, 03.11.2026; vorn Stille weg,
2,5 s mit 0,8 s Ausblende, −18 LUFS, 70 % Lautstärke); nach voller Kette statt dessen `kampf_konter_kette` |
| Fehlschlag auf der Leiste | klein „Too early“ / „Too late“ unter der Leiste, in Perle, nicht rot (1,1 s) | wie bisher Treffer |
| Serie | drei Punkte neben der Taste: perfekte Paraden in Folge, der neue Punkt springt kurz auf. Drei bringen Fassung −4 (mit Casanovas Charm zwei) | – |

Das Probe-Fenster blendet nach dem Ende in 260 ms aus, damit Ring und Punkt noch zu sehen sind. Ring und Hinweis liegen fixiert über
der Seite (`EdenQTE`, Hook `treffer(i)`, Felder `serie`/`serie_max` in den Parade-Daten). Bei weniger Bewegung: keine Animation, die
Information bleibt.

**Klänge von Pixabay (Duc 03.11.2026, Auswahl der Review-Sitzung):** `kampf_warnung` (Gong, erster Schlag, kündigt die Täuschung an),
`kampf_kette_2`/`_3` (Kettentreffer), `kampf_finte` (zwei Varianten reihum, beim Zucken), `kampf_konter_kette` (Konter nach voller
Kette). **W20 überall eine Stimme:** `wuerfel_erfolg` = Harfe, `wuerfel_fehlschlag` = Leier (1,5 s mit Ausblende), jeweils Variante 5,
auch in Gesprächen. Gebaut mit `python werkzeuge\eden_rise\sfx_pixabay.py --nur <ids>`, eingetragen in `sfx_eden_rise.py`.

### Finten (Paket 2, Duc 03.11.2026, Vorbild Clair Obscur)

Zwei Paraden je Runde bleiben. Damit sie nicht gleich klingen, hat je Gegnerart ein Angriff einen eigenen Rhythmus. Er ist **immer
gleich** für diese Absicht (nie Zufall), also lernbar, und steht nach der ersten Parade im Bestiarium. Daten: `FINTEN` in
`werkzeuge/eden_rise/kaempfe_eden_rise.py` (mit Prüfung), Feld `finte` an der Absicht in `kaempfe.json`; der Server reicht sie in
`k["parade"]["finte"]` an den Client, die Regeln ändern sich nicht.

| Art | Was passiert | Werte | Wer (Stand 03.11.) |
|---|---|---|---|
| `zoegern` | Der Strich bleibt kurz vor der Zone stehen, der Schlag kommt später. Wer im alten Takt drückt, ist zu früh. **Immer mit Taunt** (Duc 03.11.): Menschen sagen eine Zeile ihrer Stimmgruppe (Text kurz über dem Gegner), Tiere knurren nur. Gruppen von Duc abgenommen (03.11.): 21 Gruppen für alle 59 Arten, 11 sprechen (55 Zeilen, je eine lokale Katalogstimme, z. B. Agents „Adrien Morel“, Piraten „Ghjuvan Santucci“, Wolff, Riscossore, Red Trio, Sirene mit Ligeias Stimme), 10 nur Laut (Hunde `rudel_hunde`, Keiler `keiler_ansturm`, Schlangen `kampf_viper`, Raubtiere `tk_loewe`, Maschinen `kampf_unit01` …). Quelle `werkzeuge/eden_rise/taunt_gruppen.json` → `kaempfe.json` `taunts` und `enemies[].taunt`. Zeilen reihum je Runde, Schlüssel `kampf.taunt.<gruppe>.<n>`, vertont über `Vertonen_EdenRise.bat` (Sprecher `stimme:<Katalogname>`). `/api/zeile` löst seit 03.11. alle `kampf.*`-Sätze auf (`kampf.zeile()`), vorher blieben auch die Sprüche der Riccis und Hinweise der Sirene stumm. | `bei` 0,5–0,85 (wo er stehen bleibt), `halt` 300–800 ms | Fackelpirat, Keiler, Bache, Wolf, Agent, Team Leader, Big Man, Wolff (Spezial), Old Grey, Unit-01, Riscossore (Spezial), Pale Lady, Mattè, Charly, Black Viper |
| `taeuschung` | **Angekündigt** mit einem eigenen Warnklang statt des Ausholens (Duc wählte den Gong, bis zum Download `glocke`). Der Gegner zuckt, der Strich springt zurück, aber **weiter vorn, nie an den Anfang** (`zurueck` 0,55), dann kommt der echte Schlag. Wer beim Zucken drückt, verfehlt. | `bei` 0,6–0,85, `zurueck` 0,4–0,7 | Fabbiu, Feral Dog, Black Lion, Wolff (Schlag), Black Beast, Smuggler, Riscossore (Schlag), Danzel, Ark Hyena |
| `kette` | 2–4 Schläge hintereinander. Die ersten brauchen nur „gut“, **nur der letzte hat die perfekte Zone** und entscheidet das Ergebnis. Der erste Schlag kommt **nie vor 0,9 s** (`ERSTER_MIN`, Ruckler am Anfang auf langsamen PCs). | `abstaende` 1–3 Werte, je 250–800 ms | **noch keiner**: gebaut für Gegner-Combos, die entscheidet Duc |

**Ab dem zweiten Mal markiert** (Duc 03.11.2026): Hat Duc eine Finte dieser Gegnerart an diesem Angriff schon einmal erlebt
(`z["finten_gesehen"]["<art>:<absicht>"]`, über alle Kämpfe), zeigt die Leiste einen feinen hellen Strich: beim Zögern dort, wo der
Strich stehen bleibt, bei der Täuschung dort, wo der Gegner zuckt. Feld `finte_bekannt` in den Parade-Daten.

Keine Finten bei den ersten Gegnern (Ratte, Möwe, Pirat, Taschendieb, Maxwell), nie auf Angriffen, denen man nur ausweicht, und nie
bei Ring-Gegnern (Prüfung im Builder). Klänge: Zucken `kampf_schwung`, Ketten-Treffer `kampf_parade` (Platzhalter, bis die von Duc
gewählten Pixabay-Klänge geladen sind). Showcase zum Ausprobieren: `docs/abnahme/kampf_lesen/index.html`.

**Spieltest-Bot:** Eine Finte senkt seine Paradechance: unbekannte Art perfekt ×0,5 / gut ×0,75, schon im Bestiarium ×0,85 / ×0,95
(`FINTE_FAKTOR` in `tests/spieltest_bot.py`, geschätzt, nicht gemessen). Spieltest 03.11.2026 (6 Typen × 3 Seeds, vorher/nachher):
Siege gesamt 86 % → 88 %, Niederlagen 174 → 161, je Typ höchstens ±5 Punkte (schwacher Spieler 51 % → 56 %), also keine messbare
Verschiebung. Hafen-Hunde bleibt der engste Kampf (34 % → 35 %).

## Bildschirm (Etappe 3)

Entwurf A1: Zugfolge mit Avataren (Ducs Profilbild, Gegner-Kopf), Absicht als Sprechblase, Gegnerkarte mit
Fassungs-Schild und sechs Schwächen-Feldern („?“ bis getestet, Schwäche glimmt gold), Duc-Karte mit Befehlen, Liste für
Fähigkeiten und Gegenstände. Tasten 1–5, in Listen 1–9, Esc schließt. Plugin `client/plugins/eden-combat/`
(Darstellung und Zeitmessung, keine Regeln). Effekte: `eden-combat-effects.js`, Übergabe [kampf_effekte.md](kampf_effekte.md).

Kampfbilder: `Kampf_Bilder.bat` holt die Posen aus `ComfyUI\output\expressions\combat\<Sprite>\` als WebP nach
`module/eden_rise/kampf/<Sprite>/` und schneidet `avatar.webp` aus (ohne Angabe nur die Gegner aus `kaempfe.json`).
Fehlt eine Pose, nimmt der Bildschirm eine Ersatzpose.
**Bedeutung der Posen bei Duc (Duc 01.11.2026):** `heavy_attack` ist das Aufladen beim Spezialangriff. `konter` ist der Angriff nach einer perfekten Parade, bisher nur in den Messer-Sätzen (Erde, Wasser, Feuer, Luft, Cyber, Neopren); ohne `konter` zeigt der Bildschirm `attack`. Bei Gegnern ist `heavy_attack` ihr starker Angriff.
**Ducs Schlag als Bildfolge (Duc 03.11.2026):** Bei „Attack“ und beim Konter nach einer perfekten Parade spielt Duc sechs
Bilder vom Ausholen bis zum Durchschwung (`schwung_a` … `schwung_f` je Kampf-Sprite), Takt 380 · 100 · 70 · 50 · 70 · 500 ms
aus Ducs Lieferung. Der Schlag sitzt bei Bild e: Schadenszahl, Treffer-Pose und Klang des Gegners, Sieg und Niederlage warten
bis dahin, die nächste Gegner-Parade bis zum Ende des Schwungs. Das Zischen kommt bei Bild c. Der Konter beginnt beim zweiten
Bild (Duc hat schon pariert), der Schlag sitzt dort nach 120 ms Halt + 220 ms. Spezialangriffe behalten ihre Zwischensequenz.
Gemelli (Fernwaffe) hat keine Bildfolge und bleibt bei der Schuss-Pose, ebenso Maxwell und jede Figur ohne die sechs Bilder;
bei reduzierter Bewegung gibt es nur die alte Pose. Quelle: Ducs Bewegungstests `S:\VR\Gallery\Downloads\eden-duc-heavy-20261103-v1`
(22 Paare, 512 × 512), eingebaut mit `python werkzeuge\kampf_schwung.py <ordner> [--vorschau]`: ein Maßstab je Folge
(letztes Bild gegen `heavy_attack`, erstes gegen `heavy_windup`), Füße auf der Bodenlinie der Posen, Farbe je Folge mit
einer Kurve pro Kanal an die vier Posen angeglichen (Schwarzpunkt, Kontrast, Sättigung; Duc 03.11.2026), Kontaktbögen in
`docs/abnahme/kampf_schwung/`. Code: `SCHWUNG` in `kern/kampf.py` (in `duc_bilder`), `schwung()` in `eden-combat.js`.
Test `tests/test_kampf_schwung.py`.

Engine: `eden.kampf_starten(z, modul, begegnung)` setzt Status `kampf` (Rückkehr in den vorherigen Status über
`kampf_schliessen`). Aktionen `kampf_zug {befehl, ziel, revision}`, `kampf_parade {ergebnis, revision}`, `kampf_schliessen`.
Test: `python tests\vorschau_server.py --port 8332 --kampf hafen_dieb_test`.
**Startstand je Begegnung (29.10.2026):** `--kampf` beginnt nicht mehr nackt. `STARTSTAND` in
`tests/vorschau_server.py` setzt den Stand, den Duc im echten Spiel an der Stelle hat (Gate-Bot, Seed 7): Hafen-Wellen
mit Terremoto (Flag `waffe_bat`), Mistral (Maxwells Lektion vorbei) und Level 1 / 1 / 2 (Ratten / Hunde / Keiler).
`--kampf-level`, `--skills`, `--waffe` überschreiben das. Kämpft Duc trotzdem mit dem Ersatz-Schrubber (keine Waffe im
Besitz, Begegnung ohne feste Waffe), zeigt die Vorschau oben ein rotes Schild. Grund: Der Spieltest am 28.10. lief mit
Lv1 + Schrubber gegen den Keiler (Sieg bei mittlerer Parade 32 %), echt sind es 74 %.

**Spezialangriff als Zwischensequenz (26./27.10.2026):** Ein Spezialangriff öffnet die Sequenz aus dem Effektlabor vor dem
aktuellen Szenenbild, mit Ton. Der Zug geht schon beim Start der Sequenz an den Server. Die Schadenszahl erscheint im
Einschlag über dem Gegner (mehrere Einschläge teilen den Schaden, danach steht die Summe groß darüber), dazu
„Critical!“, Fassungsverlust und beim Heiler „+LP“ an Duc. Danach zeigt der Kampfbildschirm diese Zahlen nicht noch
einmal. Kommt die Serverantwort erst nach dem Einschlag, erscheint die Zahl sofort. Wird die Sequenz mit Leertaste
übersprungen, bevor die Zahl kam, zeigt sie der Kampfbildschirm wie bei einem normalen Angriff.

**Kampftöne (27.10.2026, Katalog `sfx.json`, Pixabay):** `kampf_schwung` beim Klick auf Angriff oder Fähigkeit,
`kampf_treffer` bei Schaden (Gegner oder Duc), `kampf_parade` / `kampf_parade_perfekt` / `kampf_ausweichen` nach der
Parade (Ausweichen auch, wenn Ducs Schlag nichts trifft), `heilung`, `status` bei neuer Statuswirkung,
`kampf_sieg` (K.o./Aufgabe), `kampf_niederlage`, `level_up` beim Aufstieg und beim Verteilen von Attribut- und
Skillpunkten. Nach einer Zwischensequenz kein Treffer- und kein Heilton, die Sequenz hat ihren eigenen Klang.

**Skill Tree (Duc + Brain Trust 27.10.2026, Plugin `eden-skills`):** Unter jedem Skill steht seine Kernzahl mit Ducs
aktuellen Werten (z. B. Mistral „16 dmg“, Elicriso „+27 HP“, Phare „45% stun“). Das Detailfeld zeigt im Block „With you
right now“ die ganze Rechnung. Sie kommt aus `kampf.skill_zahlen(z, defs)`: getragene Waffe mit Rosis Stufen und Chips,
Attribute, Hauptpfad, max. LP. Gerechnet wird gegen einen Gegner ohne Rüstung und Schwäche, ohne Krit. Die Zahl steigt
also sichtbar mit Stärke, Werkstatt und Level. Hinter jeder Pfad-Reihe liegt eine Krea-Szene, links ausgeblendet, in der aktiven Reihe heller
(`client/plugins/eden-skills/paths/K|L|W|M|H.png`, von Duc abgenommen: Sturmbrandung, Schmugglerhöhle mit violettem
Licht, Leuchtturm mit Strahl, Vulkan mit Lava, Klostergarten mit Strohblumen; erzeugt mit
`werkzeuge/eden_rise/skill_pfade_bilder.py`, Abnahme `docs/abnahme/skill_pfade.json`). Sind alle vier
Skills eines Pfads gelernt, ist er **gemeistert**: Rand leuchtet, „★ Mastered“ im Kopf. Im Moment des Meisterns gibt es
einmal ein Aufleuchten und den Ton `mission_erfolg`.

## Etappe 4a – Regeln gebaut (24.10.2026)

Die Regeln aus den Abschnitten unten stehen jetzt in `kern/kampf.py` (Daten: `werkzeuge/eden_rise/kaempfe_eden_rise.py`
→ `kaempfe.json`). Der Kampfbildschirm (4b), die Akt-1-Events (4c) und die Laboreffekte (4d) folgen; bis dahin ist der
Kampf über die Konsole und den Vorschau-Server testbar.

- **Fortschritt** `z["combat"]`: Level 1–10, Erfahrung (Sieg = 20 × Gegnerlevel × Bedrohung grau 0,5 / grün 1 /
  orange 1,5 / Totenkopf 2; nächstes Level = 60 × Level), Skills. LP 36 + 5/Level, Ausdauer 6/7/8.
- **Ausrüstung** `z["equipment"]`: eine Waffe, eine Rüstung (Werte aus den Tabellen unten).
- **Gegner Akt 1:** Taschendieb Lv 1 (Rede-Gegner, Schwäche Charisma), Möwe Lv 1, Ratte Lv 1, Pirat Lv 2, Pirat mit
  Fackel Lv 4, Maxwell-Training (Level = Duc, Erfahrung ×0,25, kostet keine LP). Werte nach Level-Kurve, Fassung
  12 + 2 × Level, Proben-SG 11 + Level/2, Flucht-SG 10 / 14 / 18 / unmöglich je Gegnerstufe.
- **Testschalter** (nur Konsole und Vorschau-Server): `python tests\kampf_konsole.py akt1_fackelpirat --level 9
  --skills K3,K5,M3,M5 --waffe rosis_flammenschwert --ruestung lederjacke`, dieselben Schalter mit `--kampf-level`
  im Vorschau-Server.
- **Abgleich:** `python werkzeuge\kampf_abgleich_v5.py` – Einzeltreffer in Engine und Simulation identisch; ein
  einfacher Bot gewinnt Lv 3–5 grün/orange/Totenkopf etwa 90 / 60 / 30 % (ohne Werkstatt und Küche).

Wo Doku und Simulation auseinanderlagen, gilt (bitte im Spieltest prüfen):

| Punkt | gebaut | statt |
|---|---|---|
| Typ-/Element-Faktor | ×1,25/0,8 und ×1,2/0,85 („Formeln“) | ×1,3/0,8 (Waffen-Abschnitt) |
| Messer | Krit +5 %, erschöpft +5 („Formeln“) | +10 %, +6 |
| Stange (Abstand) | Gegner trifft mit −1 (Simulation) | −2 |
| Elektro-Harpune / Doppelflinte | 9 / 7 (Gesamt-Balancing) | 7 / 7 |
| Rüstungs-Widerstand | Schaden aus dem Element ×0,7 und immun gegen dessen Zustand | nur eines davon |
| Waffen-Eigenheiten | aus der Simulation: Rosis Schwert 2 Brandstufen bei Krit/Konter, Katana jeder 2. Treffer Brand, Taser jeder Treffer Strom, Streitkolben erschüttert, Harpune Erstschlag mit Strom, Dreizack nass + erschüttert bei Krit, Holms Säbel Konter ×1,5 | – |
| Zwei Waffen-Slots | eine Waffe aktiv, Zweihänder belegen nur Platz | – |
| Mistral auf nassen Gegner | löst Schlamm aus | Simulation nicht |
| Gegner geschwächt | gilt für seinen nächsten Angriff | Simulation: bleibt (Fehler) |
| Strom | 25 % Zug verloren, auch für Duc | wie Simulation |

## Beschlossen am 19./20.10.2026 – noch nicht gebaut

Dieser Abschnitt ersetzt die Angaben oben, sobald er umgesetzt ist. Neuer Code wird englisch geschrieben,
die Oberfläche bleibt deutsch, Erzählung und Stimmen bleiben englisch.

Begriff (20.10.2026): Der Zustand „Gegner offen“ heißt in der Oberfläche **„erschöpft“** (nächster Treffer +4, entsteht
durch Schwachstelle erkennen, perfekte Parade, nach seinem schweren Schlag, Treffer auf die Schwäche). Im Code bleibt
der Schlüssel vorerst `offen`, die Anzeige nimmt den neuen Begriff. Die eigene Schwachstelle nach einem Patzer
(„Duc offen“, nächster Treffer gegen Duc +3) heißt **„ungedeckt“**.

### Attribute (Anzeige deutsch)

| Code | Anzeige | Wirkung im Kampf |
|---|---|---|
| strength | Kraft | Angriffswert |
| charm | Charisma | Reden |
| empathy | Empathie | Heiler-Pfad (seit 26.10.2026) |
| perception | Wahrnehmung | breiteres Parade-Fenster, Schützen-Pfad (Point de Mire) |
| cunning | List | Chance auf kritische Treffer |
| courage | Mut | Einschüchtern |

Ducs Stärke „Charme“ gibt Vorteil auf Charisma-Proben, deshalb heißt das Attribut nicht ebenfalls Charme.

### Fähigkeiten: 3 Grundfähigkeiten, sonst nur Spezialangriffe

**26.10.2026 (Duc):** Den Heftigen Angriff gibt es nicht mehr, es gibt nur noch Spezialangriffe. Maxwell bringt Duc am
Ende von Lektion 1 **K3 Mistral** bei (`kern/tutorial.py` `LEHRT`, `kampf.beibringen`). Beigebrachte Spezialangriffe
(`combat.taught`) sind im Kampf verfügbar, kosten keinen Skillpunkt, bestimmen den Hauptpfad nicht und zählen als
Vorstufe für den nächsten Rang ihres Pfads (nach Mistral ist K5 lernbar). Weitere Lehrer laufen über denselben Weg.

| Fähigkeit | Attribut | ⚡ | Wirkung |
|---|---|---|---|
| Reden | Charisma | 2 | W20: Fassung −6 (kritisch −9), nur Menschen |
| Einschüchtern | Mut | 2 | W20: zwei Angriffe geschwächt + Fassung −3 (kritisch −6), wirkt bei den meisten Tieren (Keiler immun) |

Gestrichen: Beruhigen (samt Gegner-Merkmal `beruhigbar`), Finte, Improvisieren. Damit hat die Stärke Handwerk
im Kampf keine Wirkung mehr; sie wirkt über die Waffen (Rosi zieht eine Waffe eine Stufe hoch).

### Kritische Treffer

- Angriff und Konter: Chance 5 % + 3 % je Punkt List, Schaden ×1,5 (aufgerundet).
- W20-Proben: je 2 Punkte List wird der Krit-Bereich um eine Zahl größer (List 2: 19–20).
- Anzeige der Krit-Chance im Befehlsmenü, „Kritisch!“ im Log; Tests mit festem Wurf.

### Parade

Wird nie gewürfelt: Ergebnis `wuerfeln` und der Umschalter „Parade: Reaktion/Würfeln“ fallen weg.
Wahrnehmung verbreitert das Zeitfenster (+3 % je Punkt) und gibt damit mehr Zeit für die perfekte Parade.

### Rede-Gegner

Keine neue Regel, nur Werte: Schwäche Charisma, wenig Fassung, viele LP. Prügeln bleibt möglich, hat aber andere Folgen.
Beispiel Yasin: K.o. → er verlässt das Boot, Siri hasst Duc. Aufgabe (überredet) → Yasin bleibt, Siri beginnt eine
Beziehung mit Duc, Yasin akzeptiert es (alles war ohnehin geplant).

Seit 28.10.2026 (Flut-Nacht, E-085) gibt es drei kleine Schalter dafür und für seltene Gegner:
- `untouchable` (Gegner-Text): Waffen, Zustände und Granaten machen keinen LP-Schaden, nur Fassung zählt (die Sirene).
  Reden wirkt bei jedem Gegner, der es nicht in `immune` sperrt – Tiere sperren es, die Sirene nicht.
- `fassung_faktor` (Gegner): Fassung × Faktor, für Rede-Bosse (Sirene 2).
- `selten` (Begegnung): mit `chance` kommt ein anderer Gegner (Vampirin 10 % statt der Fledermäuse), `steigt` hebt die
  Chance je Begegnung ohne ihn (Zähler `selten_zaehler`, zurück auf null nach dem Treffen); `level: "duc"` mit
  `level_plus` setzt das Level relativ zu Duc.
- Beute `{"eins_aus": [...]}` in `chips.drops`: genau eine von mehreren Belohnungen (Modul, Geld, Material).
Alles in `ortskapitel_grotte.md` („Die Flut-Nacht“).

### Waffen, Rüstung und Ausrüstung

Der alte Entwurf mit 24 Waffen, 8 Rüstungen und 2 Ausrüstungs-Slots ist **ersetzt** (25.10.2026). Es gelten fünf feste Waffen,
fünf Jacken, Rosis Upgrades mit Steinen und Plates, Erweiterungen und später Charms. Alles steht in
[`aufruestung.md`](aufruestung.md) und im Wiki [`wiki/items.md`](items.md).

### Fliehen

Mut-Probe, SG nach Gegnerstufe: L leicht, M mittel, H sehr schwer, Ex unmöglich. Fehlschlag kostet die Runde.

### Gegnerwerte je Stufe (Simulation werkzeuge/kampf_balance_v3.py, inzwischen v4; Roguelike: Duc eine Ausrüstungsstufe unterlegen)

| Stufe | LP | Angriff | Schutz | Parade-Tempo |
|---|---|---|---|---|
| L | 34 | 10 | 1 | leicht |
| M | 54 | 11 | 2 | mittel |
| H | 60 | 13 | 3 | stark |
| Ex | 85 | 13 | 4 | stark |

Folgen einer Niederlage (Duc 01.11.2026): Sie kostet eine Phase, Duc wacht verletzt auf, und jemand aus der Crew hat ihn zurückgetragen. Das Spiel endet dadurch nie, außer bei der Belagerung mit Neustart.

## Nächste Etappen

4. Erste echte Begegnung über ein Event, LP-Auffüllen in der Nacht
5. Nach Spieltest: zweiter Gegner, NPC-Hilfe über Vertrauen

## Spezialangriffe, Brennen und Kombos (beschlossen 22./23.10.2026, Simulation `werkzeuge/kampf_balance_v5.py`)

Noch nicht in der Engine – Duc testet es in Akt 1. Im Spiel stehen die **Spielnamen**, in Chat, Doku und Planung die
**Arbeitsnamen** mit Kürzel = Pfad + Level: **K** Kämpfer (Kraft) · **L** Schmuggler (List) · **W** Schütze
(Wahrnehmung) · **M** Berserker (Mut). Code-IDs bleiben die Spielnamen (`mistral`, `ressac`, … `scirocco`, `retour`,
`furia`, `vulcano`).

### Freie Skillwahl

- **Skillpunkte:** je 1 auf Lv 3, 5, 7 und 9, **2 auf Lv 10** (zusammen 6). Level-Obergrenze bleibt **10**.
- **Frei wählbar, aber Schritt für Schritt:** Eine Stufe gibt es nur, wenn man die Stufe darunter **im selben Pfad**
  hat (für M5 braucht man M3, für ein Finale die 7 desselben Pfads). Mit 6 Punkten: ein Pfad bis zum Finale plus 2
  Punkte woanders, oder zwei Pfade bis zur 7, oder breiter.
- **Hauptpfad** = der Pfad mit den meisten Punkten. Er bestimmt Waffengattung, Pfad-Eigenheit und welches Attribut
  mit dem Level wächst (für den Akt-1-Test; freie Attributpunkte wären die Alternative).
- **Skalierung:** Jeder Pfad schlägt mit seinem Attribut zu – Klinge/Stumpf mit **Kraft**, **Messer mit List**,
  Berserker mit **Mut** (jeweils der höhere Wert zählt). **W-Skills wirken voll erst ab Wahrnehmung 4**, darunter:
  W3 hält nur bis zum nächsten eigenen Zug, W5 halbiert nur (kein Gegenschlag), W7 blendet und lässt den Gegner nur
  mit **15 % je Wahrnehmungspunkt** aussetzen (Wahrnehmung 3 = 45 %).
- **Hinweis im Skill-Bildschirm:** „Der Schmuggler entfaltet sich mit dem Gnadenstoß“ – Schmuggler-Builds ohne L9
  sind die schwächsten (siehe Ergebnis).

### Pfade

| Pfad | Attribut | Rolle | Eigenheit |
|---|---|---|---|
| Kämpfer | Kraft | standfest: erschüttern, kontern, aushalten | – |
| Schmuggler | List | Zustände und Krits, Messer | – |
| Schütze | Wahrnehmung | Kontrolle: erschöpfen, abfangen, Flieger | Parade-Fenster +10 % |
| Berserker | Mut | Feuer aufbauen und entladen, dabei offen | +1 Ausdauer, wenn Duc getroffen wird; Parade-Fenster −10 % |
| **Heiler** (seit 26.10.2026) | Empathie | heilen, durchhalten, einmal wieder aufstehen | – (Stütz-Pfad, wenig Schaden) |

Merkhilfe: **5er = Antwort auf einen angekündigten Spezialangriff (SA)** des Gegners (gegen einen starken voll,
gegen einen schwachen abgeschwächt), **9er = Finale**. Ausnahme **M5 Rachefeuer: Aufladeskill** (Duc 24.10.2026) –
er wird vorher eingesetzt, wirkt auf den nächsten Angriff jeder Art und belohnt die Parade.

### Alle 20 Spezialangriffe (Kosten in Ausdauer; seit 26.10.2026 mit dem Heiler)

| Kürzel | Arbeitsname | Spielname | Wirkung | Kosten / Preis |
|---|---|---|---|---|
| K3 | Erschütterer | Mistral | Treffer +4, Gegner erschüttert (2 Runden) | 3 (mit Gorilla 2) |
| K5 | Konterwelle | Ressac | auf SA: Gegenschlag (gegen nass ×2), Gegner geschwächt; bei schwachem SA nur Gegenschlag | 3 |
| K7 | Windrüstung | Libeccio | 2 Runden halber Schaden gegen Duc; jede perfekte Parade erschüttert den Gegner | 2 |
| K9 | Riesenwelle | Lame de Fond | Finale gegen erschöpften Gegner: ×2, gegen erschüttert ×3 | 4 |
| L3 | Doppelschnitt | Doppio Gioco | zwei Schnitte à 70 % | 3 |
| L5 | Abtauchen | Sotto Voce | auf SA: Treffer gegen Duc halbiert + nächster Angriff sicherer Krit; bei schwachem SA nur der sichere Krit | 2 |
| L7 | Blutschnitt | Vendetta | Schnitt 30 %, dann Gegner blutend (nicht gegen Maschinen) | 3 |
| L9 | Gnadenstoß | Omertà | Finale gegen erschöpften Gegner: Krit ×2,5 (mit sicherem Krit aus L5: ×3,5), +25 % je Zustand, höchstens 4 Zustände (jede Brandstufe zählt einzeln) | 4 |
| W3 | Zielmarke | Point de Mire | Gegner 3 Runden erschöpft (unter Wahrnehmung 4: bis zum nächsten eigenen Zug) | 2 |
| W5 | Ruhepuls | Bonaccia | auf SA: Angriff ganz abgefangen + Gegenschlag ×1; bei schwachem SA halbiert + Gegenschlag ×0,5 (unter Wahrnehmung 4: nur halbiert) | 2 |
| W7 | Leuchtfeuer | Phare | auf starken SA: blendet, Gegner setzt 1 Runde aus (mit Strom 2); unter Wahrnehmung 4 setzt er nur mit 15 % je Punkt aus | 3 |
| W9 | Sternsalve | Pluie d'Étoiles | Finale: 3 Treffer à 85 % (voll gegen Flieger) | 4 |
| M3 | Glutschlag | Scirocco | Treffer +4, +1 Brandstufe | 3 · danach ungedeckt |
| M5 | Rachefeuer | Retour de Flamme | **Aufladeskill:** lädt die Waffe auf (hält bis zum nächsten Gegnerangriff). Auf **jeden** Angriff folgt dann ein Konter: Parade geschafft (perfekt oder gut) → Konter ×1,5 und +1 Brandstufe, gegen einen angekündigten **starken** SA ×2; Parade verfehlt → Konter ×0,5, kein Brand (erst ×2/×3/×1 – zu stark, nur der Schaden wurde angepasst) | 2 |
| M7 | Flammenrausch | Furia | sofort ein Treffer, dann 2 Runden ×1,3, jeder Treffer +1 Brandstufe | 3 · Duc beginnt mit +1 Brandstufe, kein Verteidigen |
| M9 | Feuersturm | Vulcano | Finale, **jederzeit startbar**: ein Schlag je Brandstufe am Gegner à 60 %, ignoriert Schutz, verbraucht alle Stufen – lohnt sich nur bei vielen Stufen | 4 · danach 1 Runde aussetzen |
| H3 | Heilöl | Elicriso | heilt 30 % der LP und löst Brennen oder Blutung. **Nonna Fiora bringt ihn im Kloster bei** (Folge `{"beibringen": "elicriso"}`, kein Skillpunkt) | 3 |
| H5 | Westwind | Ponente | 3 Runden je 10 % LP am Rundenende, Parade-Fenster +10 % | 3 |
| H7 | Erwachen | Risveglio | heilt 80 % der LP · **einmal pro Kampf** | 4 |
| H9 | Erzengel | Arcangelo | Aufladeskill: Fällt Duc in diesem Kampf auf 0 LP, steht er einmal mit 50 % LP wieder auf · **einmal pro Kampf** | 4 |

### Zustände (neu oder geändert)

| Zustand | Regel |
|---|---|
| **erschöpft** | Gegner: Ducs Treffer +4 (Messer +5), schaltet K9/L9 frei. Entsteht durch W3, perfekte Parade, nach seinem starken SA; **blutend** und **Schlamm** zählen ebenfalls. **Zählt Runden, nicht Treffer** (Mehrfachtreffer verbrauchen ihn nicht) |
| **brennend** | stapelt **1–5 Stufen** (🔥×1 … 🔥×5): je Stufe und Runde 3 % der max. LP (Bosse ¾). Klingt nur in Runden **ohne neue Stufe** um 1 ab. Gleiche Regeln auf Duc: Verteidigen löscht 1 Stufe, Feuerwehrjacke immun |
| ungedeckt | nächster Treffer gegen Duc +3 |

### Reaktionen (im Kampf mit Namen einblenden)

| Name | wodurch | Wirkung |
|---|---|---|
| Dampf | Feuer + nass | **alle** Brandstufen gelöscht, Gegner geblendet |
| Kurzschluss | Strom + nass | +8 % max. LP, Gegner setzt 1 Runde aus. **Auch auf Duc** (seit 28.10.2026): 8 % seiner LP, nächste Runde aussetzen (Agenten in U2 der Berge) |
| Aufplatzen | Feuer + Blut | 5 % max. LP × verbleibende Blutrunden sofort, Blut weg |
| Funkenflug | Strom + Feuer | +1 Brandstufe |
| Schlamm | erschüttert + nass | zählt als erschöpft |

### Formeln

```
Treffer  = max(1, rund((6 + Attribut + Waffe + Extra + Erschöpft − Geschwächt) × Typ × Element × Faktor) − Schutz)
           Attribut = Kraft; Messer: max(Kraft, List); Berserker: max(Kraft, Mut)
Typ      ×1,25 stark / ×0,8 schwach   ·   Element ×1,2 / ×0,85 (Wasser > Feuer > Erde > Luft > Wasser)
Schutz   1 + Gegnerlevel/3, wird bei JEDEM Treffer abgezogen, 0 wenn erschüttert (M9 ignoriert ihn)
Krit     Chance 5 % + 3 % × List (+5 % Messer, +5 % Falke), ×1,5 · L9 ×2,5 bzw. ×3,5
Brennen  3 % × Stufen × max. LP je Runde (Bosse ×0,75) · Bluten 5 % × max. LP je Runde
W7       Aussetzen unter Wahrnehmung 4: Chance 15 % × Wahrnehmung
```

Folge: **Mehrfachtreffer brauchen erschüttert oder erschöpft** – das ist die Kombo-Logik des Systems.

Beispiel Lv 9 (Kraft 3, Rosis Schwert 9, Gegner 129 LP, Schutz 4; Grundwert 18): normaler Angriff 14 · gegen
erschöpft 18 · K3 → K9 (erschüttert + erschöpft) 18 + 66 · L7 → L9 rund 60 · W3 → W9 3 × 15 · M9 bei 🔥×5 5 × 11 = 55.

### Ergebnis Simulation v5 (23.10.2026, mit Werkstatt und Küche)

Reine Pfade, Sieg % grün / orange / Totenkopf, Spieler „Normal“ (Ziel ≈ 85 / 55 / 20), 80 Kämpfe je Feld:

| Lv | Kämpfer | Schmuggler | Schütze | Berserker |
|---|---|---|---|---|
| 3 | 100 / 79 / 48 | 100 / 85 / 60 | 99 / 58 / 26 | 99 / 81 / 54 |
| 5 | 100 / 82 / 13 | 99 / 89 / 20 | 99 / 80 / 20 | 96 / 76 / 18 |
| 7 | 97 / 62 / 23 | 97 / 62 / 16 | 100 / 73 / 26 | 100 / 87 / 35 |
| 9 | 96 / 63 / 38 | 88 / 67 / 46 | 98 / 72 / 38 | 96 / 75 / 43 |
| 10 | 92 / 60 / 27 | 89 / 70 / 29 | 95 / 61 / 18 | 96 / 74 / 38 |

Freie Skillwahl, alle erlaubten Mischungen (`python kampf_balance_v5.py --builds`), Ø der drei Siegquoten:

| Lv | Builds | beste | bester reiner Pfad | schwächste |
|---|---|---|---|---|
| 7 | 20 | 73 (M3) | 73 | 49 |
| 9 | 35 | 71 (M4) | 71 (M4) | 38 (Schmuggler ohne L9) |
| 10 | 68 | 70 (K1 L2 M3) | 67 | 34 (Schmuggler ohne L9) |

Keine Mischung dominiert; reine Pfade und Mischungen liegen nah beieinander. Der Berserker (Aufladeskill M5) liegt
seit dem 24.10. 3–5 Punkte vorn – im Akt-1-Test beobachten. Ø Schaden der Finale: K9 78 · L9 89 · W9 46 · M9 103
(selten, echter Höhepunkt).

Entscheidungen aus der Simulation: Bosse nehmen ¾ Brandschaden (mit ½ gewann der Berserker gegen den Totenkopf auf
Lv 7 nur 4 %); W5 schlägt zurück (ohne: Schütze Lv 7 −20 Punkte); ohne W-Skalierung dominierten W3/W5/W7 als
Beimischung jeden Build (bis Ø 90 auf Lv 10); Messer mit List hebt den Schmuggler, dafür L7 nur 30 % Sofortschlag.
Fürs Spiel wichtig: Die Gegner-Absicht muss zeigen, **ob ein SA wehtut** – auf Heilen/Stärken mit einem 5er zu
antworten verschenkt Ausdauer (der simulierte Spieler tut das nicht).

## Gesamt-Balancing (21.10.2026, Simulation `werkzeuge/kampf_balance_v4.py`)

Gilt mit Level, Pfaden, Zuständen, Gegner-Spezialangriffen, Werkstatt und Kochen zusammen.

- **Duc:** LP 36 + 5 pro Level (Lv 10: 81), Ausdauer 6, ab Lv 5: 7, ab Lv 9: 8. **Seit 26.10.2026: LP 46, Grundschaden 8**
  (siehe „Balancing Kloster“).
- **Gegner pro Level** (statt fester Stufen): LP ≈ 55 × 1,10^Level, Angriff ≈ 19 + 0,6 × Level, Schutz 1 + Level/3.
  **Seit 26.10.2026: 40 × 1,10^Level und 14 + 0,6 × Level.**

  | Level | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | LP | 60 | 66 | 73 | 80 | 88 | 97 | 107 | 117 | 129 | 142 | 156 | 172 |
  | Angriff | 20 | 20 | 21 | 21 | 22 | 23 | 23 | 24 | 24 | 25 | 26 | 26 |

  Albtraum-Bosse ×1,2 LP. **Level-Abstand:** je Level über Duc +25 % LP und Schaden (**seit 26.10.2026: +15 %**).
- **Bedrohung** relativ zu Ducs Level: Lästig (grau, darunter) · Gefährlich (grün, gleich) · Tödlich (orange, +1) ·
  Albtraum (Totenkopf, +2 und mehr).
- **Werkstatt (Rosi):** +1 / +2 / +3 je +1 Schaden bzw. Schutz; +3 Meisterstück mit Perk; Veredeln (Element setzen/wechseln).
- **Schütze:** Pluie d'Étoiles 3 × 85 %, Point de Mire 3 Runden, Elektro-Harpune 9, Doppelflinte 7, Fern nicht mehr
  schwach gegen Monster, Pfad-Eigenheit +10 % Parade-Fenster.
- **Ergebnis** (normal / geübt, grün · orange · Totenkopf, spätes Spiel): ~86–91 · ~51 · ~21 % / ~98 · ~87 · ~59 %.
  Ohne Werkstatt und Küche spät ~20 Prozentpunkte weniger.
- Offen: Erfahrungskurve und Uhren für 21 Tage, sobald die Orte mit Level-Bereichen feststehen.

## Kampfbilder neuer Figuren (Duc 30.10.2026)

- **Gesicht:** Jede neue Figur bekommt ein `avatar.webp`, in dem das Gesicht mittig im Kreis der Zugfolge sitzt. `werkzeuge/kampf_bilder.py` schneidet es aus; sitzt der Kopf anders, bekommt die Figur einen Eintrag in `AVATAR_KOPF`. Danach den Ausschnitt ansehen.
- **Größe:** Menschen stehen alle auf 86 % der Bildhöhe. Tiere brauchen einen Eintrag in `GROESSE`, sonst stehen sie so hoch wie ein Mensch. `tests/test_kampf_bilder.py` prüft beides.
- **Fliegende Tiere:** Ein Eintrag in `FLUG` hebt die Posen beim Export vom Boden, Bones um 22 % der Bildhöhe. Schlaf und Niederlage (`AM_BODEN`) bleiben unten.
- **Köpfe (31.10.2026):** Gleiche Körperhöhe allein reicht nicht: Eine geduckte Figur hat bei gleicher Höhe einen größeren Kopf und wirkt größer. Darum steht jeder Mensch mit seiner Kopfhöhe in `KOPF` (`werkzeuge/kampf_bilder.py`, Scheitel bis Kinn in der Grundpose, von Hand gemessen). Die Figur wird um die halbe Abweichung zu Ducs Kopf skaliert, alle Posen gleich, die Füße bleiben stehen. Ohne Eintrag schlägt der Test an. `KOPF_STAERKE` auf 1.0 wäre die volle Korrektur; dann wirken geduckte Figuren wie Bibi klein.
- **Oberfläche:** Bei mehreren Gegnern gibt es eine Leiste statt Liste und Karte, das Ziel klappt darin auf. Der Rechentext der Befehle steht im Tooltip.
- **Füße (30.10.2026):** 29 Posen ohne Füße wurden mit `karten_neu/kampf_fuesse.py` neu erzeugt (Krea-Edit mit der eigenen Pose als Vorlage). Erweitern nach unten klappt nicht, die Beine schließen nicht an. Berührt eine Pose nur mit der Schuhspitze den Bildrand, ist sie vollständig.

## Maxwell als Spielfigur

Duc 01.11.2026: Bei der Belagerung steuert der Spieler Maxwell wie Duc, auf der Karte und im echten Kampf. Die Story-Kämpfe davor bestreitet Duc allein. Technik und Parade sind dieselben, nur die Werte kommen aus `HELDEN` in `werkzeuge/eden_rise/kaempfe_eden_rise.py`, angewendet von `kern/kampf._held_werte`.

| Punkt | Wert |
|---|---|
| Waffe | Steel Mop, Schaden 5, stumpf, ab Level 7 alle 2 Level +1. Nie Ducs Waffe |
| Kleidung | Steward Shirt, Schutz 2 |
| LP und Ausdauer | Ducs Level-Wert × 1,2, Ausdauer einen Punkt weniger als Duc |
| Attribute | Stärke 5, Mut 5, Empathie 3, Charme 3, Wahrnehmung 2, List 1 |
| Tasche | 3 “USE ME” First Aid Kits, 3 Espressos, 1 Brandgranate, 1 Erschütterungsgranate. Eigene Tasche, in jeder Welle wieder voll, weil er auf dem Schiff alles bekommt. Beute geht an Duc |
| Fremdes | Ducs Jacke, Chips, Waffen-Upgrades und Waffenpflege wirken bei ihm nicht. Erfahrung geht an Duc |

| Angriff | Kosten | Wirkung | Effekt und Klang |
|---|---|---|---|
| Parry the Dirt | 2 | Der nächste Angriff bekommt einen Konter, wie Retour de Flamme, aber ohne Brand | Nebelwand (`wind`, Rauch) |
| Maximum | 3 | +5 Schaden, ×1,5 gegen Maschinen, 1 Runde erschüttert | Feuersturm mit Explosion (`vulcano`) |
| Mr. Maximum Approves | 1 | +3 Ausdauer, der nächste Treffer ist sicher kritisch | Erwachen (`awaken`, Buff) |

Die Effekte und Klänge kommen unverändert aus dem Labor. Für die Zwischensequenz gibt es dort das Set `DucMaxwellSteelMop` (`werkzeuge/eden_rise/labor_maxwell_sprites.py`). Die Werte stammen aus einer Simulation mit einem angenommenen Spieler, nicht aus echten Runden: Er gewinnt einen einzelnen Kampf fast immer und verliert dabei 30 bis 50 % seiner LP. Der Druck kommt daher, dass die LP zwischen den Kämpfen bleiben.

## Mündungsfeuer

Duc 01.11.2026: Wer schießt, zeigt Blitz, Funken und Rauch genau am Lauf, mit dem Schussklang `gun_shot` aus Holms Wette. Das gilt für Gemelli bei Duc (beide Läufe, auch beim freien Schuss vor Runde 1 und beim Konter) und für Gegner, deren Angriff in den Daten `"schuss": true` trägt, derzeit der Pirate Gunner und die Schützin der Agenten.

Den Punkt misst `werkzeuge/muendung_messen.py` je Sprite und Pose nach `module/eden_rise/muendung.json`, `kaempfe_eden_rise.py` trägt die Tabelle in `kaempfe.json` ein. Nach einem neuen Satz mit Fernwaffe: Sprite in `GEGNER` des Werkzeugs eintragen, beide Skripte laufen lassen. Fehlt der Punkt, kommt nur der Klang.

Der Rifleman der Agenten ist seit dem 01.11.2026 eine Kolumbianerin mit leichtem Sturmgewehr (Kampf-Satz `AgentGunman`, Begegnung `tk_schuetze`). „Draws the Pistol“ der Agenten hat kein Mündungsfeuer, weil ihre Sprites keine Pistole zeigen.


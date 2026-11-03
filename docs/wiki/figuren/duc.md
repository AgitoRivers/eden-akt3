# Duc – die Spielfigur

> Kanon-Stand 25.10.2026 · Besitz: Character Design · Quellen: Figurenbibel, Register E-006/E-017, Memory „Ducs Spielfigur“

## Kurz
Duc ist Founder von **Eden Consulting**, einer Nachhaltigkeitsberatung, führend in DACH und von der Eden Group gekauft.
Vor der Europa-Expansion nimmt er ein Sabbatical und fährt als **Erster Offizier** der Eden Rise das Saisonende mit.
Er hat den Yachtmaster, den Kopf eines Beraters und die Hände eines Handwerkers. Ab Tag 2 führt er die Yacht.

## Fakten
| | |
|---|---|
| Rolle an Bord | Erster Offizier; ab Tag 2 (Holms Evakuierung) mit dem Kommando betraut |
| Beruf | Founder Eden Consulting (ESG-Beratung), Studium BWL |
| Qualifikation | Yachtmaster |
| Ankunft | Tag 0, steigt im Hangar von Antibes aus einer langen Stretch-Limousine (E-017) |
| Herkunft | Seine Eltern sind nach dem Vietnamkrieg nach Deutschland geflohen und haben sich dort eine Zukunft aufgebaut. Duc ist in einer migrantischen Arbeiterfamilie groß geworden und hat sich hochgearbeitet (Duc 25.10., E-067). Kommt im Spiel in eigenen Gesprächen mit Yamamoto und Chiara vor und am Lagerfeuer „Where You Come From“ |
| Name | Đức heißt „Tugend“ (*virtue*), seine Eltern haben ihn ausgesucht. Im Spiel bei Ligeia (Chip `yt_duc`, Duc 02.11.2026) |
| Megan | kennt sie aus dem Studium (sie Nautik, er BWL), Anziehung nie ausgelebt, nennt sie „Mac“ |
| Der CEO | Fan von Duc, hat ihn an Bord geholt (kein Twist, E-007) |

## Die vier Stärken (gleich verteilt)
**Köpfchen** (Analyse, Berichte, ESG) · **Küche** (europäisch und südostasiatisch) · **Charme** · **Handwerk**.
Nie „Tüftler“ nennen.

## Stimme (Antwort-Chips)
- Selbstsicher, warm, mit trockenem Witz; nie überheblich, nie Macho. Kann frech sein, ohne zu verletzen.
- Spricht wie jemand, der Teams führt: klar, freundlich, entscheidet. Fachwörter nur, wo er gerade Experte ist.
- Chips bieten echte Haltungen an (herzlich · frech/flirtig · neutral · Fettnäpfchen), keine Varianten derselben Floskel.
- Der Fettnäpfchen-Chip ist menschlich, nicht dumm: ein Satz, der in diesem Moment danebengeht.

So klingt er:
> Ties a bowline one-handed. “Behind my back, if you like.”
> “It's not a motor. It's an inverter.”
> “And you still look so gorgeous, Mac. It feels like time didn't pass.”

## Was ihn treibt
- Wirksamkeit: Dinge reparieren, Menschen zusammenbringen, eine Bucht retten.
- Er ist ESG-Berater in einer Geschichte über einen Deal, der grün aussieht. Das macht ihn zur Zielscheibe und zum Prüfstein.
- **Seine ESG-Arbeit hat nichts mit dem Resort zu tun (Duc 01.11.2026).** Im Epilog arbeitet er sich hoch und will die Ethik und die Führung der Firma verbessern. Dass Eden Consulting das Kirchendach zahlt, ist ein Nebeneffekt und rundet seinen warmen Bogen ab. Im schlechten Ende nimmt er das Geld und vergisst das Dorf, dann wird das Dach nicht repariert.

## Anrede durch die Crew
Ab Tag 2 sagt die Crew **“Officer”** (K1, entschieden 25.10.). **“Captain”** ist eine Auszeichnung: Sie fällt erst, wenn
eine Figur ihn wirklich anerkennt, als Moment im Spiel. Einzelne Anreden: Anrede-Matrix in [README](README.md).

## Sonnenbrille und Gefühls-Posen
- **Die Sonnenbrille bleibt immer auf der Nase**, in jedem Bild: Kampf, Charakterbild, Dialog. Running Gag, der Kult werden soll (Duc 03.11.2026). Gefühle zeigt er über Mund, Brauen und Haltung.
- **Gefühls-Posen für Dialoge (Duc 03.11.2026):** je Jacke 44 SFW-Posen (😇-Satz des Prompt Studios ohne Rückansichten, ohne `submissive`/`worshipful`), ohne Waffe, freigestellt. Liegen unter `module/eden_rise/charakter/gefuehle/Duc<Look>/<gefuehl>.webp`, ausgeliefert unter `/charakterbild/gefuehle/Duc<Look>/<gefuehl>`.
- **Wo sie erscheinen:** `eden.duc_bild(z, gefuehl)` nimmt die Pose der getragenen Jacke. Genutzt in Anhörung, Verhandlung, Sturm und in den Taktik-Szenen der Belagerung, wenn Duc spricht. Fehlt ein Gefühl, gilt `DUC_GEFUEHL_ERSATZ` (z. B. desire → love), dann das Grundgefühl ohne `_2`, zuletzt `neutral`. Ohne Gefühl bleibt es das Charakterbild mit Waffe (Menü, Trupp-Karte).
- **Erzeugen:** `python werkzeuge\charakter_bild.py <Look>|alle --gefuehle` → `docs/abnahme/charakter/gefuehle/` (Karten für Frauen sind in `GEF_DUC` für Duc umgeschrieben), übernehmen mit `alle --gefuehle-uebernehmen`. Test: `tests/test_duc_gefuehle.py`.

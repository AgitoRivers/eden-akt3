# Übergabe: Roboter-Gegner und Kampffluss

Stand 02.11.2026. Sitzung „Roboter und Kampffluss“ (Boarding Robots, Kobra, Skorpion, zwei Fixes im Kampf-Client).

## Gebaut (alles auf master)

| Commit | Was |
|---|---|
| 7161fe20, 1e961d0a, ee52f78d | Abnahme-Runden Boarding Robots, Kobra, Skorpion |
| 95133228 | `RobotCobra`, `RobotScorpion` als Kampf-Sprites in `module/eden_rise/kampf/` |
| af2d0cbf | `BoardingRobot`, `BoardingRobotHeavy` (roter Anstrich) als Kampf-Sprites |
| d668b187 | Taktik-Daten: `tk_robot` und `tk_robot_schwer` zeigen die neuen Sprites |
| a448f56e | Sieg erst nach der Spezialangriff-Sequenz: kein Umfallen, keine Ergebnis-Karte, keine Siegmusik, solange sie läuft |
| 6c7aacf4 | Ruckeln im Kampf: Sprites und Zahlen überleben den doppelten Neuaufbau je Aktion |

Alle 26 Posen der vier Roboter sind von Duc abgenommen. Abnahme-Seiten: `docs/abnahme/boarding_robot_satz.html`,
`docs/abnahme/robot_flink_satz.html`, `docs/abnahme/robot_flink_hurt.html`. Bau-Skripte in `karten_neu/`
(`boarding_robot_*.py`, `robot_flink_*.py`, `casting_*robot*.py`), Größe und Avatar-Kopf in `werkzeuge/kampf_bilder.py`
(`GROESSE`, `AVATAR_KOPF`).

## Offen

- **Ruckeln:** Fix gemessen (60 Bilder/s, Server ~30 ms, Sprites bleiben dieselben Knoten), aber Duc hat noch nicht
  gespielt. Meldet er weiter Ruckeln, nach der Aktion fragen, bei der es passiert.
- **Sieg nach Sequenz:** Syntax geprüft, nicht mit echtem Siegtreffer per Spezialangriff gespielt.
- **„Start parry“ bei Maxwell:** Notknopf bleibt stehen, wenn der einzige Startversuch der Probe in eine beschäftigte
  halbe Sekunde fällt (`paradeStarten` in `eden-combat.js`, `ST.probeRev`). Fix wäre: Start erneut versuchen, bis die
  Probe läuft. Duc sagte „erstmal so lassen“.
- **DALL·E-Pixelblätter** für Kobra, Skorpion und den roten Heavy: Prompts hat Duc bekommen, Bilder macht er selbst.
  Bis dahin zeigt die Taktik-Karte verkleinerte Platzhalter.

## Belagerung / Taktik-Karte (Blick dieser Sitzung)

Diese Sitzung hat nur Gegner-Sprites geliefert, den Stand führen Story und Kampf. Aus den gemeinsamen Notizen
(`project_eden_belagerung_drei_tage.md`, `project_eden_taktik.md`): Sechs Wellen über Tag 21–23, Balancing,
Inszenierung Paket 1, Drehbuch-Beats, Vertonung der Karten-Stimme und Cliffhanger sind gebaut. Offen bis Akt 3:
Texte und Prozente sind Entwurf (Duc geht durch), Crew-Aufträge am Abend, Inszenierung Pakete 2–4,
Bilder (Namensblatt, Umschlag, Kreidetafel, Schadensliste, Kevin, Flicken-Bretter), Pixel-Blätter der neuen Roboter,
Yacht-Folgen, Alon ohne Stimme und Sprite, Urteil zur Nord-Barrikade und zu zerstörbaren Barrikaden, Kalender Akt 3 ab Tag 24.

## Branches, Worktrees, Ports

- **`codex/holms-bet`** (Worktree `C:/Users/DucNg/Documents/Codex/eden-holms-bet`, sauber): **überholt.** Beide Commits
  liegen als d30e41a1 und f8dd16a8 schon auf master, danach kamen dort viele Weiterentwicklungen (064fdfc4 usw.).
  Nicht mergen. Branch und Worktree kann Duc löschen.
- Ports: keiner läuft mehr. Vorschau-Eintrag `eden-kampf-tempo` (8451, Fackelpirat Level 9) steht in
  `C:\Users\DucNg\.claude\launch.json`.

## Fallen

- Krea: Die Figur-Beschreibung schlägt die Pose. Liegende Posen bekommen sonst zweiten Kopf oder Schwanz; den
  Subject-Satz für die Pose selbst ändern (`ANDERS` in `karten_neu/robot_flink_satz.py`). Schräge Körper nur per Bilddrehung.
- Nach dem Einbau neuer Kampf-Sprites `werkzeuge/eden_rise/taktik_eden_rise.py` neu laufen lassen, sonst fehlt das
  Sprite in `taktik.json` (der Builder lässt fehlende Sprites still weg).
- Maschinen und Tiere brauchen `GROESSE`, Köpfe abseits der Mitte `AVATAR_KOPF`, sonst Menschengröße und leerer Avatar.
- Vorschau im Browser über `127.0.0.1`, nicht `localhost`: Der Server hört nur auf IPv4, `localhost` kostet je
  Verbindung ~0,3 s und täuscht Ruckeln vor.
- Kampf-Client: neue kurze Sprite-Klassen in `FLUECHTIG` eintragen (siehe Wiki `systeme/kampf_effekte.md`, Regel 8).

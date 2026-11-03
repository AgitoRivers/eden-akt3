# Übergabe: Wunsch-Outfits und Outfit-Quests

Stand 31.10.2026, abends. Letzter Commit dieser Arbeit: `400886f1`. Chat mit Duc auf Deutsch, alles im Spiel auf Englisch, in einfachem Englisch.

## Zuerst lesen

1. `docs/wiki/START.md`, `docs/wiki/STIL.md`, Figurenseiten unter `docs/wiki/figuren/`
2. `docs/wiki/systeme/schneider.md`, Abschnitt „Outfit-Quests“, und E-104 in `ENTSCHEIDUNGEN.md`
3. `X:\AI\PromptStudio\KREA_LEITFADEN.md` vor jeder Krea-Generierung
4. Memory `project_eden_wunsch_outfits.md`

## Die Lage in Kürze

- **Quest-Pilot Sophias Lesung:** gebaut und committet, noch nicht vertont. Duc hat die erste Fassung im Browser durchgeklickt, sie war ihm zu schnell vorbei. Die ausgebaute Fassung hat er noch nicht beurteilt.
- **Bildsätze:** sieben Sätze à 52 Posen liegen unter `X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_wunsch_sets\<Name>\roh`. Nur Sophias Satz ist im Spiel.
- **Krea** ist auf Ducs Wunsch geschlossen. Vor einem Lauf starten und prüfen, ob es frei ist. Nie parallel zur Vertonung oder zu einem Bot-Lauf.

## Outfit-Quest: Lesung

| Was | Wo |
|---|---|
| Szenen | `werkzeuge/eden_rise/ereignisse_outfit_quest.py`, IDs `ol_*` |
| Maßstück ohne Schnittmuster | `kern/schneider.py`, Feld `"quest"` und `"wenn"` |
| Test | `tests/test_outfit_quest.py` |
| Text und Abweichungen | `docs/brain_trust/QUEST_SOPHIA_LESUNG.md`. Abschnitt 4 zeigt noch die kurze Fassung, maßgeblich ist der Code |
| Set im Spiel | `Book Reading`, ST-Karte `Sophia Moore\set7`, 49 Bilder, ohne `caring_2`, `joy_2`, `optimism_2`. Einbau über `karten_neu/wunsch_einbau.py` |
| Testeinstieg | Launch `eden-lesung`, Port 8409, startet bei `ol_tuer_moore`. Zeigt auf den Worktree `wt_quest` im Scratchpad der alten Sitzung. Bricht das, Pfad in `~/.claude/launch.json` auf `X:/AI/Eden/tests/vorschau_server.py` ändern |

**Beschlüsse von Duc (E-104):** Die Quest gibt das Schnittmuster. Vier Schritte: Wunsch, Material, Anprobe mit einer Wahl, Anlass. Start erst nach der passenden Leiter-Szene. Bei Alltags-Outfits eine Frage statt Kleiderschrank. Festa ohne eigene Quest. Ohne Danzels Laden gibt es keine Quest und keine Ersatzfassung.

**Offen an der Lesung:**
- Duc spielt die neue Fassung und urteilt. Link: `start chrome "http://localhost:8409"`, Server vorher starten.
- Neuer Kanon wartet noch auf eine ausdrückliche Bestätigung: alter Kamelhaarmantel, Totòs verlorene Pokerrunde, Haartrick aus London, Alvas „quiet nights“, Mann mit dem Klemmbrett, die Krimi-Stellen mit Mrs Trelawney und Mrs Pascoe.
- Im Browser geprüft ist nur der Teil von der Tür bis zur Reaktion, und das vor den letzten Pose-Änderungen. Klatschen bis Tresen, Wunsch, Poker, Anprobe, Echo und Dorf liefen nur im automatischen Test.
- Der Lagerraum zeigt die normale Bar. Don Anghjulu, Totò und Bà Tư sieht man in der Lesung nur als Text.
- Die Tagesszenen (Wunsch, Danzel und Totò, Anprobe, Dorf) tragen als `gag1` das Abzeichen „GAG“. Die Takte der Lesung laufen als `abend`.
- Vertonung erst ganz am Ende, auf Ducs Ansage, nur über `Vertonen_EdenRise.bat`.

**Falle Posen:** Im Mantel-Satz hocken oder drehen sich `amusement`, `curiosity`, `embarrassment`, `fear`, `grief`, `nervousness`, `pride`, `relief`, `remorse`, `sadness` weg. Der Test prüft das für Sophias Mantel-Szenen. Bei anderen Sätzen vorher den Kontaktbogen `_bogen.jpg` ansehen.

## Bildsätze

| Satz | Preset | Rolle laut Duc | Mein Vorschlag, Duc hat noch nicht geurteilt |
|---|---|---|---|
| Sophia_Reading | Yacht_Sophia_W_Haar | Buchlesung | im Spiel, drei Bilder weggelassen |
| Rosi_Workshop | Yacht_Rosi_W_Haar | neues Werkstatt-Outfit, „wenn man will“ | neun Bilder neu: schwarze Schultern fehlen, `joy_2` zweiteilig |
| Rosi_Festa | Yacht_Rosi_A_Haar | Festa | ganzer Satz neu in blickdichtem Stoff, durchs Satin zeichnen sich die Brustwarzen ab |
| Siri_Morning | Yacht_Siri_K_Haar | neuer Morgen-Look | drei Bilder neu |
| Siri_Festa | Yacht_Siri_D_Haar | Festa | 18 Bilder neu: Ärmel wechseln, zweimal Umhang |
| Alva_Bar | Yacht_Alva_W_Haar | neuer Bar-Look | vier Bilder neu |
| Chiara_Whites | Yacht_Chiara_Whites_Anker_b | Dress Whites mit Anker-Pin, Goldkette, Blowout | fünf Bilder neu: `joy_2`, `optimism_2`, `fear_2`, `grief_2`, `remorse_2` |

- **Abnahme:** `docs/abnahme/wunsch_sets.json` und `docs/abnahme/chiara_whites_set.json`. Serve mit `python werkzeuge/abnahme_seite.py --serve <json> <port>`, zuletzt liefen sie auf 8406 und 8408. Die Seiten als eigenen Run-Block `start chrome "<url>"` posten.
- **Neu rendern:** `karten_neu/wunsch_sets.py --los <Name> --posen=a,b`. Alte Datei vorher wegräumen, sonst entsteht `pose-1.png`. Zusatztexte stehen dort in `ZUSATZ`, eigene Rückentexte in `RUECKEN`. Rosi und Siri werden wohl einen eigenen Rückentext brauchen, falls ihre Rückansichten von vorn kommen.
- **Noch nicht ins Spiel eingebunden:** alle außer Sophia. Einbau in `SAETZE` von `wunsch_einbau.py` ergänzen und danach `werkzeuge/gesichter_messen.py --nur <id>` laufen lassen.
- **Chiara-Pilot:** Die Dress Whites hängen noch am alten Maßstück-Weg und am alten Set-Namen `Dress Whites`. Ihr Satz ist noch nicht eingebaut.

## Grenze: Lea, Lola, Jana

In `project_hauptsprites_pause.md` steht meine Grenze: keine expliziten Sprites und keine neuen Bilder von Lola, Lea und Jana, weil sie auf Bildern sehr jung wirken. Daran habe ich mich gehalten, darum gibt es Leas Festa-Satz nicht, obwohl Duc ihn bestellt hat. Duc sagt, er habe das für Lea revidiert. Eine solche Änderung habe ich nicht gefunden, und die Notiz ist unverändert. Das habe ich Duc gesagt. Zu Beginn der Sitzung hatte ich versehentlich schon Konzeptbilder von Lea, Lola und Jana erzeugt, sie liegen unter `_casting_wunsch_geparkt`.

Quests für diese drei gehen nur mit dem bisherigen Set. Das Spiel fällt bei fehlendem Bild von selbst darauf zurück.

## Noch offen, nicht begonnen

- Quests für Rosi, Chiara, Siri, Alva. Ideen in der Tabelle unten, nichts davon ist Kanon. Erst Text zum Lesen, dann bauen.
- Anlässe für die Festa-Kleider, Morgen-Look und Bar-Look.
- Alva K, Megan W und D, ohne Rolle. Lola, Elsa, Jana ohne Outfit-Wahl.
- Aus früherer Arbeit: Abnahme `docs/abnahme/theatre_rouge.json`, sieben Stücke ohne Urteil.

| Look | Idee |
|---|---|
| Chiara, Dress Whites | Leere Ärmel für vier selbst verdiente Streifen, Anker-Pin von Opas Navy-Jacke, Geheimnis Yachtmaster |
| Siri, Morgen | Danzel fragt, was sie tragen möchte, sie hat keine Antwort, das erste Kleid nur für sich |
| Rosi, Werkstatt | Offiziell ist nur der Overall gerissen, sie redet nicht darüber |
| Alva, Bar | Ein Abend, an dem die Bar wirklich ihr gehört |

## Arbeitsweise

- Commits nur aus eigenem Worktree mit `update-ref` und erwartetem alten Wert, nie in den gemeinsamen Index stagen. Danach den Hauptordner nur für die eigenen Pfade angleichen. Muster: `quest_commit2.sh` im Scratchpad der alten Sitzung (`19a41183-…`).
- Generierte Daten nach jedem Rebase neu bauen: `ereignisse_basis.py`, `modul_eden_rise.py`, `kochen_eden_rise.py`. Der Worktree braucht `module/eden_rise/figuren` und `eden-config.json`.
- `module/eden_rise/ereignisse.json` ist im Hauptordner durch eine andere Sitzung verändert, das ist nicht von dieser Arbeit.
- Bilder nur über Abnahmeseiten, Entscheidungen immer mit Vorschlag. Keine Frage-Kästen. Nur eigene Vorschau-Ports beenden.
- Bei dieser Übergabe liefen noch die Abnahmeseiten auf 8406, 8407, 8408 und die Vorschau auf 8409.

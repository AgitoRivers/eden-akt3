# Onboarding-Prompt für neue Agenten

Stand 29.10.2026. Alles unter der Linie in eine neue Sitzung kopieren und `[THEMA]` ersetzen. Funktioniert auch für
Agenten ohne Ducs Memory (anderer Rechner, Codex, anderer Account) – die arbeiten am besten auf einem eigenen Branch
oder Worktree statt direkt auf master. Neue Sitzungen bekommen einen klaren Namen und ein Thema und werden als
Besitzerin in die Tabelle in `docs/wiki/START.md` eingetragen.

---

Du arbeitest mit Duc an „Eden Rise“, einem Dating-Roguelike mit Ermittlung und Kampf (eigene Engine, Python + HTML/JS).
Mit mir sprichst du Deutsch. Alles, was Spieler sehen oder hören, ist Englisch. Code und Bezeichner englisch.

## Wo alles liegt
- Engine + Modul: X:\AI\Eden (Git, Branch master, kein Remote – nie pushen). Server eden.py, Regeln kern\, Oberfläche client\,
  Daten module\eden_rise\ (NUR über die Builder in werkzeuge\eden_rise\*.py erzeugen, JSON nie von Hand ändern).
- Python: X:\AI\ComfyUI_krea2\python_embeded\python.exe
- Wiki = Kanon: X:\AI\Eden\docs\wiki\ (Rangfolge: Duc/Register > Wiki > Engine > Karten)
- Planung: X:\AI\Eden\docs\brain_trust\ (ENTSCHEIDUNGEN.md, OFFEN.md, LEHREN.md, FIGURENBIBEL.md, BRAIN_TRUST_PROMPT.md)

## Bevor du irgendetwas tust – lies in dieser Reihenfolge
1. docs\wiki\START.md (wer besitzt welche Seite, Regeln der Zusammenarbeit)
2. docs\wiki\STIL.md (Sprache, Erzählform, natürliche Sätze, Bilder, Sprite-Stimmung)
3. docs\brain_trust\LEHREN.md (Fehler, die wir nicht wiederholen)
4. die Wiki-Seite deines Themas (systeme\, welt\, figuren\) und vor jedem Figurentext deren Figurenseite
5. git log --oneline -20 und git status (was andere gerade tun)

## Arbeitsweise
- Erst erklären, dann bauen: Plan (Bedienung, Regeln, Dateien, Aufwand) vorlegen und auf mein OK warten – auch nach „ja, setz um“.
- Fragen und Pläne im Text, keine Auswahl-Kästen mit Knöpfen.
- Planungsrunden als Brain Trust nach docs\brain_trust\BRAIN_TRUST_PROMPT.md; Rollen fett als normaler Text, nie als >-Zitat.
- Jede gebaute oder geänderte Mechanik sofort im Wiki erklären (Auslöser, Zahlen, Code-Stelle, Test).
- Spoilerschutz: Fall-Auflösungen (wer was ausgelöst hat) nie im Chat, nie im Wiki – nur in story.json.
- Duc ist ESG-Berater mit Handwerk, nie „Tüftler“.

## Prüfen und Committen (mehrere Sitzungen arbeiten parallel!)
- Tests: python tests\lauf_test.py (Gate, Seeds 7 und 3), dazu die Fachtests in tests\ (test_<thema>.py), Sprache: tests\test_sprache.py.
- Committen nur, wenn ich es sage. Nur eigene Dateien/Hunks – der Git-Index ist mit anderen Sitzungen geteilt:
  Teil-Commits über einen eigenen Index (GIT_INDEX_FILE) bzw. git apply --cached, nie fremde Änderungen mitnehmen.
- Ändert sich das Spielverhalten, Gate-Referenz neu: sauberer Worktree auf HEAD, eden-config.json und
  module\eden_rise\figuren mitkopieren, dann lauf_test.py --seed 7 --speichern und --seed 3 --speichern, vor dem Commit prüfen,
  dass HEAD sich nicht bewegt hat, Referenz sofort committen.
- Commit-Nachrichten enden mit: Co-Authored-By: Claude <noreply@anthropic.com>

## Gemeinsame Ressourcen
- Grafikkarte wird geteilt (Krea/ComfyUI 8189, Chatterbox 8004, Giftige Blume/Kobold 5010, Prompt Studio 8301):
  vor dem Start kurz bei den anderen Sitzungen fragen, danach Bescheid geben und wieder beenden.
- Vertonen nur über X:\AI\Eden\Vertonen_EdenRise.bat (--praefix/--wer/--schluessel), jede Zeile mit Chatterbox-Turbo-Tag.
- Bilder: Krea läuft mit CFG 1 (Negativ-Prompt wirkt nicht) → alles positiv formulieren, keine Lochmuster (Duc hat Trypophobie).
  Freigabe immer über eine Abnahmeseite (werkzeuge\abnahme_seite.py).
- Vorschau: tests\vorschau_server.py auf einem EIGENEN Port; nie fremde Server beenden.
- Langläufer (Training, große Render- oder Vertonungsläufe) nie als Kind deiner Sitzung starten, sondern per .bat in eigenem Fenster.
- Kostenpflichtige APIs (Anthropic, ElevenLabs) nur nach meiner Freigabe. Löschen nur in den Papierkorb.

## Andere Sitzungen
- Mit ListAgents siehst du die laufenden Sitzungen, mit SendMessage schreibst du ihnen.
- Fremde Seiten/Dateien ändert nur die Besitzerin (Tabelle in START.md) – sonst Nachricht mit Fundstelle und Vorschlag.
- Nachrichten untereinander still verarbeiten; mir nur zeigen, was wirklich wichtig ist
  (Datenverlust, kaputtes Gate, eine Entscheidung, die nur ich treffen kann).

## Deine Aufgabe
[THEMA – z. B. „Woche 3 von Akt 2 planen (Tag 15–21, Belagerung)“ oder „Kampf-Balance Berge prüfen“]
Beginne damit, mir in 5–8 Sätzen zu sagen, was du gelesen hast, was der aktuelle Stand des Themas ist und wie du vorgehen willst.

# Übergabe: Brain-Trust-Planung Eden Rise (Stand 24.10.2026 abends)

Für die nächste Claude-Instanz. Duc spricht Deutsch und will Planung als **Brain Trust von Eden Studios**
(Sienna, Aly, Luise, Maelle, Sora). Diese Datei ist nur noch der Einstieg; der Inhalt steht in `docs/brain_trust/`.

## Lesereihenfolge

1. `docs/brain_trust/BRAIN_TRUST_PROMPT.md` – Rollen, Stil, Dialogbeispiele, **sieben Sehnsüchte**, **acht Prüfsteine**,
   Regeln. So wird gespielt.
2. `docs/brain_trust/ENTSCHEIDUNGEN.md` – Register E-001 … mit Status (entschieden / gebaut / überholt) und Fundstelle.
3. `docs/brain_trust/FIGURENBIBEL.md` – Kanon jeder Figur (erster Eindruck, Erkennungssatz, Bogen, Ende).
4. `docs/brain_trust/LEHREN.md` – Fehler, die wir nicht wiederholen.
5. `docs/brain_trust/OFFEN.md` – **hier weitermachen**: nächste Schritte, Fragen an Duc, Parkplatz.
6. Bei Bedarf: `docs/brain_trust/archiv/BRAIN_TRUST_UEBERGABE_bis_2026-10-24.md` (Langfassung aller Diskussionen bis
   24.10.), Dossiers `docs/brain_trust/*_dossier.md` + `auszuege/` („VERDECKT“-Abschnitte nie im Chat zitieren),
   Fachdokus `docs/wiki/systeme/kampf.md`, `tage_erkundung.md`, `orte.md`, `orte_drehbuch.md`.
   Memory: `feedback_brain_trust_eden.md`, `project_eden_rpg.md`.

## Stand in einem Absatz

Akt 1 ist spielbar gebaut (`master`): Cold Open 06:35, Party, Strandung, Megans Ultimatum und tägliche Sprachnachrichten,
Bucht, Spuren, Megan an Bord + Sturm, Lagerfeuer, Anhörung mit Zeugen und Loyalitäten, Cliffhanger; Modell B (19 freie
Phasen, 2 Aktionen pro Phase), Maxwells Tutorial und Training. Entschieden, aber noch nicht gebaut: **Tag 0 im Hangar
von Antibes** (Limousine, Megan als Führerin, Kennenlern-Chips) und Kämpfe hybrid. Nächster Schritt laut Duc (9A):
Tag 0 bauen, dann Hafenkampf, dann Spieltest.

## Arbeitsweise (bewährt)

- **Nur diese Hauptsitzung pflegt Übergabe und Register** (7A). Andere Sitzungen melden Beschlüsse per Nachricht.
- Nur eigene Dateien committen, vorher `git status` (Codex und andere Sitzungen arbeiten im selben Repo).
- Dossiers günstig: zuerst `python werkzeuge\figur_auszug.py <id>` (lokal), Agent nur mit Sonnet, ≤ 120 Zeilen.
- Skripte mit Backslashes per Write-Tool anlegen, nie per Bash-Heredoc (`\b` wird zum Steuerzeichen).
- Bilder: Abnahmeseite (`werkzeuge/abnahme_seite.py --serve spec.json port`), vorher selbst auf Lochmuster prüfen.

## Nicht-Planung, was noch ansteht

- **Kampf-Sprites nachholen:** wenn Duc mit Training fertig ist, startet ER `Kampf_Nachholen.bat` → `test`; Bilder prüfen,
  nach OK `voll`, danach `fertig`.
- Geparkt: Audio, IlluGen/EmberGen-Tests, Parade-Schalter im Code entfernen.

## Ducs Dauerregeln (Kurzfassung)

Erst erklären, dann bauen · Massenaktionen nur mit Plan + OK · kein Commit ohne Auftrag · Langläufer nur per .bat ·
vor bezahlten API-Läufen fragen (Kobold lokal ist frei) · neuer Code englisch, Oberfläche deutsch · Blut nur als
Striemen (wholesome) · Trypophobie beachten · Käufe macht Duc selbst · nie pushen.

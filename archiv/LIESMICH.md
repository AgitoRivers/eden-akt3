# Archiv

Hier liegt, was nicht mehr gespielt und nicht mehr weiterentwickelt wird. Die Engine liest nichts von hier.

## eden_yacht_gestrandet (archiviert 18.10.2026)

Das erste Yacht-Modul mit Szenen-Vorrat und Showrunner. Duc spielt es nicht mehr, Nachfolger ist `module/eden_rise`.

- `module/eden_yacht_gestrandet/`: Moduldaten, so wie sie zuletzt gebaut waren
- `werkzeuge/modul_gestrandet.py`, `werkzeuge/szenen_gestrandet.py`: die Builder dazu

Was Eden Rise davon weiter nutzt, lebt jetzt in Eden Rise selbst:

- Welt, Räume, Personen, Persona, Gesten: `werkzeuge/eden_rise/basis_eden_rise.py` (Kopie von `modul_gestrandet.py`)
- Dorf- und Crew-Missionen: `DORF` in `werkzeuge/eden_rise/missionen_eden_rise.py`

Die Builder hier laufen nicht mehr ohne Anpassung, weil sie in `module/` schreiben. Wer das Modul wiederbeleben will:
Ordner zurück nach `module/` verschieben, dann starten.

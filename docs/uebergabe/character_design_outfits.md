# Übergabe: Character Design, Outfits (Stand 02.11.2026)

Bereich: Outfit-Casting der Nebenfiguren, Holms Korsika-Uniform, Wunsch-Outfits der Hauptfiguren. Nur Casting, nichts davon ist im Spiel. Keine Spoiler in dieser Datei.

## Gebaut (master)

| Commit | Was |
|---|---|
| 33a78592 | Casting Nebenfiguren-Outfits: Isabelle, Casanova, Bibi, Charly, Duc je 4 Varianten (Presets `Neben_<Figur>_<W\|A\|K\|D>`), Abnahme `docs/abnahme/neben_outfits.json` |
| adad69ec | Holm: drei Uniform-Varianten für Korsika (N dunkle Sommeruniform, K Tropen-Khaki, P Arbeitsuniform), Abnahme `docs/abnahme/holm_uniform.json` |
| 62223f9b | Holm: Ducs Look als vierte Variante M (erschöpft, offene Haare, offene beige Baumwollbluse, navy Tanktop, navy Hose, Stiefel, Schulterklappen mit vier Goldstreifen) |
| (dieser Commit) | Ducs Urteile `holm_uniform_urteil.json`, `neben_outfits_urteil.json`, diese Übergabe |
| PromptStudio 3d1a0a82, f7ad38d9 | Krea-Leitfaden: „Preset gegen die Sprites prüfen“, „Müde ohne Dreck“ |

Skript: `karten_neu/casting_neben_outfits.py` (`--los Figur:Art`). Bilder: `X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_casting_neben\Neben_<Figur>_<Art>`.

## Ducs Urteile (in den Urteil-Dateien, noch nicht umgesetzt)

- **Holm: Bild A von M freigegeben** (`holm_M_0`, Datei `_casting_neben\Neben_Holm_M\neutral.png`). Nächster Schritt: voller Sprite-Satz in diesem Look (Seed und Prompt stehen in den PNG-Metadaten). Dabei ändern: Wiki `docs/wiki/figuren/holm.md` sagt „hochgesteckt“, die Satz-Beschreibung ebenso. Kein Kompass am Look, den gibt sie bei der Übergabe an Duc weiter.
- **Bibi K: neu machen** mit Ducs Notiz „golden cropped top and tight black shorts“ (`bibi_K_0`). Nicht gerendert.
- Alle anderen Varianten in `neben_outfits.json` und `wunsch_sets.json` ohne Urteil.

## Bekannte Schwächen von Holm M

Top kommt schwarz statt navy, Hose fällt über die Stiefel statt hinein, Stiefel stoßen an den unteren Bildrand, Haare wehen leicht. Ganzkörper-Ausschnitt: Kopf kleiner als bei Knie-Sprites, beim Satz auf Kniehöhe zurückgehen oder bewusst so lassen.

## Fallen

- `Yacht_Holm` allein liefert eine Mittzwanzigerin. Das Casting-Skript ersetzt ihren Subject-Satz (52 Jahre, Norwegerin, erste graue Strähnen) und setzt den Trigger. Für den Satz dasselbe tun.
- „worn out“ im Prompt bringt Dreck, Flecken und nasse Haut. „tired eyes“ schreiben.
- Holm nutzt die LoRA einer echten Schauspielerin (Krea_Ros); Duc weiß das, seine Entscheidung.
- Presets `Neben_*` liegen in `X:\AI\PromptStudio\presets.json`, das von mehreren Sitzungen uncommittet geändert wird. Vor jedem Schreiben neue Namen gegen vorhandene prüfen und sichern (die erste Fassung hatte `Yacht_Isabelle_A` überschrieben).
- Neue Bilder in einen Ordner mit alten: ExpressionSave nummeriert weiter, alte Dateien vorher verschieben.
- Spec geändert: `abnahme_seite.py --serve` neu starten, sonst zeigt die Seite den alten Stand.

## Branches, Worktrees, Prozesse

- Kein eigener Branch. Worktrees `scratchpad\e112_wt` und `scratchpad\wt_quest` dieser Sitzung (19a41183) sind sauber und vollständig in master, können entfernt werden.
- Laufende Abnahme-Seiten dieser Sitzung: 8406 `wunsch_sets.json`, 8407 `neben_outfits.json`, 8408 `holm_uniform.json`. Sie enden mit der Sitzung.
- Kein Krea-Lauf offen.

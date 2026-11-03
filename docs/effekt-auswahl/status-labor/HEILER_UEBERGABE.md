# Healer effect drafts · technical handoff

Aktueller Stand, 26.10.2026: Vier Heiler-Skills mit je drei Varianten und vier Icons sind im Labor vorhanden. Duc hat Elicriso 1, Ponente 2, Risveglio 1 und Arcangelo 3 gewählt; die Auswahl steht in freigabe-spezialangriffe.json/.js. Technische Prüfung bestanden; die vollständige Spielanbindung bleibt mit Claude abzustimmen.

## Letzte Tonkorrekturen

- Vendetta: Nachbrennen entfernt; zweiter Schnitt mit zusätzlichem heavy_hit und kräftigerem pressure_body.
- Omertà: magic-strike.mp3 bei Verschwinden und Rückkehr; Klangspitze an die Teleportation gebunden.
- Doppio Gioco: Doppio.mp3 als Aufladung bis zum Start der Schnitte; zweiter Schnitt mit denselben zusätzlichen Impact-Lagen wie Vendetta.
- Elicriso: Heal 1 zur Aufladung, bisherigen balm_magic-Heilimpuls behalten.
- Ponente: Wind und Blätter auf 5,9 Sekunden gekürzt, leise im Hintergrund, weich ein-/ausgeblendet; Heal 3 startet bei Sekunde 1.
- Risveglio: Heal 1 und 2 passend zum Schein.
- Arcangelo: Heal 3 und 4 passend zu Flügeln und Licht; separate kurze Rettungsmischung unverändert.

Ablaufdaten: ton-ablaeufe.js. Neue OGGs und Herkunft: assets/audio-feedback-heal-20261026/. preview-files.json enthält alle neuen Laufzeitdateien. Kein Tempo- oder Tonhöhenwechsel an den lokalen Quellen.

Die offene Bibliotheksprobe ton-bibliothek-v1.json, assets/library-trial-v1/ und die Bibliotheks-Umschaltung in klangprobe.js bleiben separat und uncommittet. Keine pauschale Freigabe dieser Testfassung.

Geschrieben: ja. Im Labor eingebaut: ja. Technisch getestet: 20 Angriffe / 60 Varianten, Abspielkontrolle und Browser-Mischungen ohne Ladefehler oder Übersteuerung. Keine Kampfregeln geändert.

## IDs

- H3 Elicriso → `balm`
- H5 Ponente → `westWind`
- H7 Risveglio → `awaken`
- H9 Arcangelo → `archangel`

All effects act on Duc at the left. The enemy stays idle, including no guard or hurt changes. No HP, healing, statuses or resurrection rules execute in the lab. Rules shown in the preview are copied from the module’s current public definitions.

## Arcangelo phases

`?angriff=archangel&phase=aufladen&einmal=1` shows preparation. `phase=rettung` shows the separate 1.25-second rescue. The phase control also switches these two previews. There is no rescue hit on the enemy.

For the actual mid-fight event, outside a cut-in:

```javascript
EdenCombatEffects.play('arcangelo_rettung', ducSpriteElement, {variant: 0});
// Aliases: archangel_rettung; arcangelo/archangel with {phase:'rettung'}.
```

The existing effect API loads the shared healer renderer through the preview route when needed. It adds a local, pointer-transparent canvas anchored to Duc, never an iframe; cleanup occurs after 1250 ms even on loading failure. Reduced motion respects the existing no-animation effect behavior. Repeated direct renderer handles expose stop().

## Audio

`ton-ablaeufe.js` adds the four healer timelines. The same 26 October export also requests longer charge sounds and stronger contacts for several existing skills; those requested revisions are included. Existing animation choices remain unchanged except for Duc’s explicit new healer choices. The new healer entries include `offset_ms` as requested; `offset` remains seconds for the existing shared player. The relation is `offset_ms = round(offset * 1000)`. Generated components are drafts, not individual user approvals.

For H9 rescue, the DOM-free player accepts `mode:'rescue'` and schedules only the short rescue pulse and afterlight, never the preparation cues:

```javascript
EdenAttackSound.play({attack:'archangel', variant:0, mode:'rescue',
  context, destination:combatMasterGain, baseUrl, startAt:context.currentTime});
```

Normal healing/status events remain the engine’s responsibility. Sounds have no combat-rule side effects. The preview route still needs `.ogg` → `audio/ogg` support if Claude has not added it yet.

## Assets and preserved interfaces

All new runtime JS, PNG, JSON, OGG and healer preview HTML files are included in `preview-files.json`. The helper is loaded before `angriffe.js` in the ordinary lab, skill preview and existing game cut-in template. Game-name → lab-ID mapping in `EFFEKT_ID` is left for Claude as agreed.

Preserved: `angriff`, `einmal=1`, `eden-preview-ready`, `EdenAttackStudy.duration`, `EdenFigurePicker.mount`, `eden-fx-duc-set-v1` and relative asset paths. Existing effect and game data files retain their format. Icons and materials were made with built-in image_gen, not SVG stand-ins. Image prompts are in `assets/heiler-v1/PROMPTS.md`.

Old `sound-v1`/`sound-v2` mixes were already removed from the repo and preserved outside it during commit 4b8d2d1. The base `klangprobe.js` was committed there too. Its newer local library-comparison additions remain a separate unfinished change; this healer commit does not silently publish them.

## Duc’s revision during review

Risveglio now receives its light from above and uses the local summond.mp3. Elicriso is now a green-gold body charge rather than the oil/flower material; its healing pulse uses 542825-kostas17-magic-spell.mp3, with the source transient aligned to the heal timestamp. Older generated components remain preserved as drafts, not active replacement sounds. No additional generation calls.

## Additional sound feedback (same export)

Scirocco, Retour, Vulcano and Vendetta now sustain their charge to release using existing material with pitch-preserving crossfades. Retour and Mistral have stronger physical contacts. Sotto Voce uses the same release/tail files at twice the gain. Vendetta receives an audio afterburn only; this does not add a gameplay burning status. Vulcano gets a dedicated final explosion. Phare uses a clean glass/reflection bloom. Pluie charges each of its three orbs with the requested ice-spell03 clip at twice the prior charge gain. Optional local library trials receive the same relevant refinements but are not silently committed as approved engine data.

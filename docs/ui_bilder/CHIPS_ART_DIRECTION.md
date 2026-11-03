# Chips: UI Art Direction (Design-Prompt)

Stand 25.10.2026 · Entwurf: `docs/abnahme/chips_entwurf.html` · Regeln: `docs/wiki/systeme/aufruestung.md` (Abschnitt Erweiterungen) · Katalog: `module/eden_rise/erweiterungen.json`

Den Prompt unten an ein Design-Werkzeug oder eine Illustratorin geben. Er ist englisch, weil Werkzeuge und Spiel englisch arbeiten.

---

## Prompt

**Role.** You are the UI art director for *Eden Rise*, a PC dating-sim/roguelike on a luxury yacht off the Corsican coast with light combat. Design the visual language for the game's equipment upgrade items, called **chips**. PC only (1280×720 up to 3440×1440), mouse and keyboard, no mobile.

**What a chip is (story).** A villain, the tech billionaire Alon, built behaviour-control chips into animal collars and agent gear. Rosi, the crew's brilliant young engineer, rewires them so they only ever *help* the player, who can take any chip out at any time. Visual idea: **liberated tech** — cold hardware with a warm hand on it. Think a small engineered module, not a gem and not a magic rune.

**Where chips appear.**
1. The cabin pool (a grid of owned chips, grouped by weapon and jacket).
2. The slots on a weapon or jacket (1, 2 or 3 slots depending on Rosi's upgrade level), plus one extra round "charm" slot.
3. A small toast when one is found ("New module found: Hammer Time").
4. The combat screen, only as tiny icons.

**Information a chip must show at a glance (priority order).**
1. **Group:** weapon or jacket → shape. Weapon chips are a **diamond (rhombus)**, jacket chips a **crest (shield)**.
2. **Category (6 per group):** → colour plus a simple symbol.
   - Weapon: Force (red, hammer/fist), Precision (yellow, crosshair), Technique (teal, cog), Counter (blue, return arrow), Status (purple, flame/bolt/drop), Element (orange, ring; Gemelli only).
   - Jacket: Protection (steel grey, shield), Parry (cyan, arc), Stamina (green, bolt), Recovery (pink, heart-plus), Presence (amber, star), Resistance (indigo, shield with check).
3. **Rarity / level (3):** → frame material and notches: bronze, silver, gold, with 1, 2 or 3 pips. Gold gets a subtle glow.
4. **Name and effect** in text next to it, never inside the chip.

Colour must never be the only signal: shape, symbol and pips carry the same information (accessibility, colour-blind friendly).

**Slot states to design.**
- Filled (chip inside), Free (dashed outline of the same shape with a "+"), Locked (grey with a small lock and the hint "Rosi, level 2"), and Unidentified (before Rosi's workshop is open: dark chip in the category colour but with a "?" instead of the symbol and no name).
- The charm slot is **round and offset**, hanging from a short strap, like a keychain; it only appears after the first charm.
- Moving a chip between slots: soft click sound and a short snap animation (120 ms), a brief rim light on the receiving slot.

**Mood and style.** Dark, calm, warm: dark charcoal glass panels with a gold accent (the existing UI uses `--akz` ≈ #d8bd86, blurred glass panels, rounded 20–28 px corners, Bricolage-style display type for names). Chips are **clean flat-vector with a touch of depth**: a soft inner gradient from the category colour into near-black, a thin precise frame, one crisp symbol, tiny details like a fine circuit line along the edge. Premium and friendly, a bit anime-tech, never grimdark, never cluttered.

**Hard constraints.**
- No hole patterns, honeycombs, perforations, sponge-like or porous textures anywhere (the creator has trypophobia). Keep surfaces smooth and closed.
- No text inside the chip artwork. Symbols only.
- Symbols must read at 28 px and look good at 96 px. Stroke-based, rounded caps, one stroke weight.
- Provide light feedback states: hover (lift 3 px, brighter rim), selected (gold rim), disabled (45% opacity).
- Respect `prefers-reduced-motion`.

**Deliverables.**
1. An SVG icon set: the 12 category symbols, plus the status family variants (flame, bolt, drop, drop of blood, crack/shake, wave) and the 6 resistance variants.
2. The two frame shapes (diamond, crest) in bronze, silver and gold, with the pips.
3. Slot states: filled, free, locked, unidentified, and the round charm slot with strap.
4. A found-item toast and a tooltip card (name, category colour bar, level pips, one-line effect, one-line Rosi comment).
5. A short style sheet: palette tokens, sizes (28 / 48 / 64 / 96 px), spacing, motion timings.

**Tone check.** If it looks like a gemstone, a rune or a loot-box icon, it is wrong. It should look like a tiny, lovingly rebuilt piece of technology.

---

## Hintergrund für das Team

- Farben und Formen stehen im Entwurf `docs/abnahme/chips_entwurf.html` (zwölf Kategorien, drei Stufen, Plätze, Pool). Das ist die Ausgangsbasis; die Art Direction soll Symbole und Rahmen verfeinern.
- Rosis Satz je Kategorie steht in `kaempfe_eden_rise.py` (`CHIPS["rosi"]`).
- Die Charm-Bilder (Plüschtiere) sind getrennt und kommen zuletzt.

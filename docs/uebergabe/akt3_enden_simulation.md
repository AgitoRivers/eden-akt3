# Akt 3 · Simulation der Enden

Stand 04.11.2026 · Werkzeug `tests/sim_enden_akt3.py` (20.000 Läufe je Spielertyp, feste Saat). Das ist eine Rechnung mit angenommenen Wahrscheinlichkeiten je Entscheidung, kein Spieltest. Die Annahmen stehen im Skript (`PROFILE`) und lassen sich ändern.

## Ergebnis mit den heutigen Regeln (E-128)

| Spielertyp | Wahrheit | Geld | Gemeinschaft | Stärke | häufigste Enden |
|---|---|---|---|---|---|
| gelegentlich | 78 % | 82 % | 37 % | 65 % | 2½b 27 %, 0 23 %, 3 17 %, 2a 15 % |
| engagiert | 93 % | 99 % | 84 % | 85 % | **3 65 %**, 2½b 12 %, 2½c 11 %, 0 7 % |
| alles | 98 % | 100 % | 100 % | 96 % | 3 92 % |

## Was das heißt

1. **Ende 3 ist für engagierte Spieler zu leicht.** Ziel aus dem Brain Trust war etwa jedes dritte Mal, die Rechnung sagt fast zwei von drei.
2. **Geld ist fast nie das Problem.** Megans Wende braucht 4 Zeugen **oder** 2 Beweise. Beides hängt an denselben Spielern, die sowieso Zeugen sammeln. Darum fehlt Geld fast nie, wenn Gemeinschaft da ist.
3. **Drei Enden kommen praktisch nie:** 2½a *On Credit* (alle außer Geld), 2b *The Village Holds Together* und 2c *Alon in Handcuffs* (unter 5 %). Sie brauchen eine fehlende Geld- oder Gemeinschaftssäule, und die beiden fehlen fast immer gemeinsam oder nie.
4. **Wahrheit ist leicht,** weil Whites Plan aus dem Keller immer zählt (Tag 34 ist Pflicht). Zwei weitere Beweise reichen.

## Getestete Alternative (`--streng`)

Wahrheit braucht 4 Beweise oder 3 mit „alles“, Megans Wende braucht 4 Zeugen **und** 2 Beweise.

| Spielertyp | Ende 3 | Ende 0 |
|---|---|---|
| gelegentlich | 10 % | **56 %** |
| engagiert | 52 % | 23 % |
| alles | 87 % | 7 % |

Das macht Ende 3 seltener, bestraft aber gelegentliche Spieler zu hart. Und die seltenen Enden bleiben selten.

## Vorschlag (offen, E-131)

Das Problem ist weniger die Schwelle als die **Kopplung**: Geld und Gemeinschaft hängen beide an den Zeugen. Ein eigener Weg je Säule macht die Mitte-Enden erreichbar:

- **Geld** nicht mehr über Zeugen, sondern nur über eigene Taten: Yamamoto 5, die Margot oder Megans Wende mit **2 Beweisen** (ohne Zeugen). Wer nur im Dorf Menschen gewinnt, aber keine Papiere findet, landet dann bei 2b *The Village Holds Together* oder 2½a *On Credit*, wie es `enden.md` erzählt.
- **Wahrheit** bleibt bei 3 Beweisen, Whites Plan zählt aber erst, wenn Duc ihn **vorlegt** (Kommission), nicht schon beim Finden.

Diese Variante ist noch nicht gerechnet. Ich rechne sie, sobald Duc die Richtung freigibt.

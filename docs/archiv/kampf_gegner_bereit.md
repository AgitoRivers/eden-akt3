# Kampf-Gegner: Bilder bereit (Stand 22.10.2026)

Alle Gegner liegen mit 13 Posen + Kopf-Ausschnitt (`avatar.webp`) in `module/eden_rise/kampf/<Sprite>/`.
Eingebunden in `kaempfe.json` ist bisher nur **Thief**. Neu holen: `Kampf_Bilder.bat --alle` (Quelle ist ComfyUI
`output/expressions/combat`, vorhandene Dateien werden überschrieben).

## Menschen (21)

| Sprite | Wer | Waffe / Requisit |
|---|---|---|
| Thief, ThiefArab | Dieb (koreanisch / arabisch) | Brechstange |
| ThiefAlpha | Gangboss, Lederjacke | kurze Brechstange |
| Pirate, PirateTorch | Pirat (Säbel / Fackel) | Säbel bzw. Fackel |
| PirateAlpha | alter Piratenkapitän | Säbel |
| Brute | samoanischer Schläger | Eisenkette |
| BruteAlpha | Hafen-Boss | Kette um die Faust |
| Agent | Agent in Schwarz | Teleskopschlagstock |
| AgentAlpha | Agentenchef im weißen Anzug | Fäuste |
| Alien | grauer Alien | Strahlenpistole |
| Alon | Tech-Milliardär, Cyber-Rüstung | Strahlenpistole, Jetpack aus |
| YasinDrone | Yasin, wütend | Drohne |
| MaxwellSteward / MaxwellSports / MaxwellMaximum | Mr. Maximum (Polo / Sport / Bodybuilder) | Fäuste, kniet statt zu liegen |
| Heinrich | Lebemann | Champagnerglas, Faust |
| DrunkCasanova | betrunkener Verführer | Weinflasche, eine Rose |
| Paparazzo | Fotograf | Kamera |
| Mime | Pantomime | leere Hände |
| Vampire | Vampirin | Dolch |

## Tiere und Wesen (24)

| Grund-Gegner | Alpha (selten, +2 Level) |
|---|---|
| Rat | RatAlpha |
| Dog | DogAlpha |
| Seagull | SeagullAlpha |
| Pigeon | PigeonAlpha |
| Bat | BatAlpha |
| Snake | SnakeAlpha |
| Ape | ApeAlpha |
| Lion | LionAlpha |
| Shark | SharkAlpha |
| WildschweinKlein, Wildschwein, WildschweinKeiler | – (drei Größen, Macchia, Zutatenquelle) |
| SeaMonster, Siren, Unit1 | – (Einzelgegner) |

## Hinweise für den Einbau

- Liegende Defeated-Posen: Kopf zeigt nach rechts.
- Kleine Tiere sind bereits verkleinert (Originale in ComfyUI unter `combat/<Name>/_gross`).
- Flucht-Pose ist gespiegelt (läuft nach rechts weg), außer Unit1.
- Bei einigen Tieren ist die Defeated-Pose eher stehend/sitzend (ApeAlpha, Pigeon, PigeonAlpha, Rat, Snake,
  SnakeAlpha, Shark, Siren, Unit1) – von Duc am 22.10. so abgenommen; falls das im Kampf stört, nachrechnen.

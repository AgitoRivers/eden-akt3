# Maxwell „Mr. Maximum“ Ndlovu – Steward und Trainer

> Kanon-Stand 25.10.2026 · Besitz: Character Design · Quellen: Figurenbibel, maximum.txt, modul, E-020/E-050

## Kurz
Zwei Meter Muskeln und der große Bruder des Bootes. Redet über sich in der dritten Person, macht einen Witz pro Satz und
einen Liegestütz pro Witz, posiert wie Might Guy. Trainiert jeden Morgen um halb sieben die Crew und lässt niemanden
bei „Ich kann nicht“ aufhören. Hat panische Angst vor allem, was fliegt.

## Fakten
| | |
|---|---|
| Alter, Herkunft | 35, Umlazi bei Durban; von seiner Gogo (Großmutter) aufgezogen |
| Laufbahn | sechs Jahre Türsteher am lautesten Club Kapstadts, Kreuzfahrt-Fitness, dann Yachten |
| Rolle | Steward unter Chiara und Personal Trainer; Fitnessraum hinter der Crewmesse, Training 06:30 Achterdeck |
| Geheimnis | Flugangst (deshalb der Yachtjob); weint bei Liebesfilmen und nennt es „Allergie“; Gogo nennt ihn „mein Engel“ |
| Wunsch | alle stärker machen; ein eigenes Studio in Durban mit Gogos Namen |

## Stimme
- Groß, warm, theatralisch. Dritte Person: “Mr. Maximum approves.” “Mr. Maximum does not negotiate.”
- Fast in jeder Zeile ein Witz, nie gemein. Südafrikanische Wörter: eish, lekker, howzit, ja-nee, shame.
- Nennt Duc **“Number One”**, Jana nennt ihn “Coach”. Wird leise und weich nur, wenn es ernst ist.
- **“brother”** gehört zu seiner Stimme (Duc 25.10., E-063): neben “Number One” für Duc und “Mr. Maximum” in der
  dritten Person darf er Duc und die Crew “brother” nennen (“Eish, brother, that was lekker!”).

So klingt er:
> “Number One! Mr. Maximum has heard of you. Mr. Maximum has also heard you skip breakfast, and we will talk about that.”
> “The sea took our engine, not our muscles. Lesson one, now – and no, the mop is not a joke, the mop is a teacher.”

## Beziehungen
Chiara (seine Chefin, Serviettenschwäne) · Jana („Coach“, sagt der Crew, sie sei stärker, als sie glaubt) · Totò
(rettete ihn im Cold Open) · Lola (Proteinpfannkuchen, „lekker“, „Big Fella“) · Yamamoto (trägt ihn jeden Tag vom
Oberdeck) · Duc (Freund, keine Romanze). Weiß von Lolas Oregano-Glas und tut ahnungslos.

## Bogen
- **Tag 0:** begeistert, stemmt eine Palette allein; als ein Hubschrauber über das Hallendach donnert, verschwindet er blitzschnell dahinter.
- **Akt 1:** fängt im Cold Open die Trümmer ab; Tag 2 nachmittags die erste Lektion (Tutorial), danach Training.
  Training mit **Holzschrubber** (weiße Borsten, Karate-Kid-Gag „Parry the dirt“, E-050). Die Borsten bleiben (K17,
  Duc 25.10.: für ihn kein Trypophobie-Auslöser).
- **Akt 3:** fliegt Gogos Medizin selbst (drei Tage weg) – seine Angst gegen seine Liebe.

## Mechanik
Nicht romanzierbar. Training jederzeit (wenig Erfahrung, 1 Attributpunkt pro Akt, E-042). Kampfgegner im Training
(Maxwell Sports), Maximum-Form als späterer Gegner.

## Aussehen & Sets
maximum_steward_a · maximum_training_b · maximum_party_b · maximum_steelmop (Hemd ohne Ärmel, ohne Waffe, erst nach Rosis Übergabe einsetzen).

**Kampf-Look (Duc 01.11.2026):** Weißes Steward-Hemd ohne Ärmel, die schwarze Fliege sitzt noch, dunkelblaue Uniformhose, polierte Schuhe. Kein Wrestler-Gürtel mehr. Waffe ist der **Steel Mop** (stumpf): Rosi baut seinen Holzschrubber kurz vor der Belagerung um, Stahlrohr, Block aus dunklem Stahl als Kopf und ein dicker Kranz weißer Borsten. Die Übergabe läuft an Tag 19 morgens in der Werkstatt zusammen mit Chiaras Taser-Gewehr (`a2_steelmop`, vier Takte). Der Block stammt von Unit-01s alter Halterung, die Borsten von seinem Holzschrubber, die Ärmel reißen beim ersten Anheben, die Fliege bleibt auf Chiaras Anordnung. Ab dem Flag `steel_mop` zeigt der Dialog das Set `maximum_steelmop` (`set_frei`). Der Kopf ist ein großer Stahlwürfel, der Kranz sitzt immer unter dem Würfel ums Rohr. Die Sprites sind eingebaut: Dialog-Set `maximum_steelmop`, Kampf-Satz `MaxwellSteelMop` (Grundpose: Würfel auf der Schulter, alle Posen schauen wie bei Duc nach rechts). Die Taktik-Karte verweist darauf, die Figur auf der Karte selbst liefert Duc als Pixel-Sprite. Duc steuert Maxwell selbst, auf der Taktik-Karte und im echten Kampf ([`kampf.md`](../systeme/kampf.md#maxwell-als-spielfigur)).

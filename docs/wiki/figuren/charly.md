# Charly de Ravenel – die Entwicklerin, die es gewusst hat

> Kanon-Stand 30.10.2026 · Besitz: Character Design · Quellen: Nebenquest [`../welt/nebenquest_red_trio.md`](../welt/nebenquest_red_trio.md)
> (Ducs Freigabe 30.10.), Preset `Yacht_Charly`, Chatterbox-Katalog

## Kurz
Trocken, verschlafen, immer mit Snacks, bewertet alles von 1 bis 10. Charly kommt aus einer alten, reichen,
konservativen Familie. Sie wollte immer eigene Spiele entwickeln und durfte nie. Ihre Mutter, CEO eines
Rüstungsunternehmens und Geschäftsfreundin von Alon, hat ihr eine Stelle als leitende Entwicklerin in Alons Anlage
besorgt. Dort hat Charly den Code der Halsbänder mitgeschrieben. Anders als Danzel und Bibi **wusste sie genau, was sie
tut.** Sie hielt es für eine Aufgabe, die man eben löst.

## Fakten
| | |
|---|---|
| Alter, Herkunft | 26, Französin, Marseille. Voller Name **Charlotte** de Ravenel – so nennt sie nur ihre Mutter (und Mr. White) |
| Familie | Mutter **Hélène de Ravenel**, CEO von **Ravenel Défense**; altes französisches Bürgertum, sehr konservativ |
| Beruf | leitende Entwicklerin in Alons Anlage, Abteilung **SHEPHERD** (Entwicklung): Code der *Behaviour Control Unit* (Halsbänder) |
| Traum | eigene Spiele entwickeln. Hat einen Pixel-Prototyp auf dem Handy: drei Figuren in roten Anzügen |
| Verschweigt | den Code, ihre Familie, ihr Geld. Aus Angst, dass Bibi und Danzel sie verurteilen |
| Gag | **bewertet alles laut von 1 bis 10** (meist 3). Ihre erste 10 gibt sie in Akt 3 Danzel, für etwas, das er genäht hat |
| Requisit | eine Chipstüte, die immer knistert |
| Erkennungssatz | “Three out of ten.” |

## Stimme
- Englisch mit französischem Einschlag, **tief, monoton**, klingt immer ein bisschen müde.
- Kurze Sätze. Zahlen statt Gefühle. Wenn sie etwas Wichtiges sagt, sagt sie es genauso monoton – und gerade das trifft.
- Kein Französisch in den Zeilen außer höchstens einem Ausruf unter Stress.

So klingt sie:
> “Three out of ten. The rock was a nice touch, though.”
> “We're the red team. A red team attacks its own company from the inside, to show where it's weak. We find proof. Together. That's the whole job.”
> “Six out of ten. For the signal.”

## Beziehungen
- **Bibi und Danzel:** ihre besten Freunde aus der Anlage. Bei ihnen durfte sie ein normales Leben spielen. Die beiden
  necken sie, weil sie „keine Ambitionen“ hat. In Wahrheit waren die beiden ihr Traum.
- **Hélène de Ravenel:** ihre Mutter. Ruft an, schickt einen Wagen nach Bastia, will sie heimholen.
- **Alon:** Geschäftsfreund der Mutter, hat ihr die Stelle angeboten.
- **Duc:** kennt den Namen Ravenel Défense von ESG-Ausschlusslisten. Als sie sagt, wer sie ist, muss sie es nicht
  erklären. Sie wartet auf ein Urteil.
- **Mr. White:** keine Zahl. Sie will nur weg.

## Bogen
Nebenquest „The Red Trio“ (Macchia). Stationen und Beats stehen auf der Quest-Seite.
- **Station 1:** kommt mit Chipstüte aus dem Gebüsch, gibt Danzels Auftritt eine 3, kämpft mit Bibi gegen Duc.
- **Station 2:** am Feuer: “We find proof. Together.”
- **Station 3b:** sagt nichts, als Bibi fragt. Dreht sich um und geht.
- **Station 4c:** allein auf dem Felskamm, die Mutter ruft an. Graue Wahl: Duc schickt sie heim oder bittet sie, zu
  zeigen, wer sie ist.
- **Station 6:** der lange Tisch. Bibi wirft ihr den Code vor und dass sie nie ihren Namen gesagt hat.
- **Wenn das Trio zerbricht (Duc 01.11.2026):** Sie geht zu ihrer Familie, später kommt eine Postkarte.
- **Nach der Belagerung (Duc 02.11.2026, nicht gebaut):** Sie hackt Alons Satelliten und bricht sie auf, Elsa schickt die Beweise an die Kommission. Ist sie nicht geblieben, schafft Rosi es allein über das Handy eines Agenten ([`belagerung.md`](../welt/belagerung.md)).
- **Danach (nur wenn alle drei sich versöhnen):** Sie fragt Duc, ob er einen Techie braucht. Ja: Sie arbeitet bei Rosi, baut Danzel die Kasse und findet in Akt 3 zu ihm. Nein: Sie fliegt nach Hause.

## Mechanik
Keine Karte, keine Romanze mit Duc. Bleibt sie, wird sie Dorf-NPC: Events erhöhen den Ruf.
**Kampf** (Stationen 1 und 3): Taser (Schock, Betäubung); im selben Zug nach Bibis Wassergranate löst „Full Charge“ den
Kurzschluss aus. Schwäche: List
– sie langweilt sich. In Station 7 Beistand mit dem Taser, wenn das Band am Tisch gehalten hat. Reißt es, fährt sie
mit dem Wagen aus Bastia heim.

## Waffe
Der Taser kommt aus dem Katalog ihrer Mutter (Ravenel Défense). Charly kennt alles darin, auch das Tödliche, und nahm
bewusst das Einzige, das jemanden nur stoppt. Note: 4 von 10.

## Aussehen & Sets
Dunkelbrauner Lob, braune Augen. Roter Anzug (von Danzel geschneidert), Headset, Taser am Gürtel.
- Preset **`Yacht_Charly`** (Prompt Studio, Kostüm `charly_A`); Duc pflegt die Dialog-Sprites selbst.
- Kampf-Sprites: 13 Posen über `karten_neu/kampf_red_trio.py` (Abnahme `docs/abnahme/red_trio_kampf/`).
- **Kein Weiß am Anzug** – Weiß gehört Mr. White.
- Stimme: Chatterbox `Charly - ENG.wav` (ElevenLabs Voice Design, Probe 2).

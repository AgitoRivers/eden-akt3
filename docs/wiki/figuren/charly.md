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

### Akt 3 (Stand 04.11.2026, Drehbuch akt3)
- **The Red Light (Tag 24 bis 28, `ereignisse_akt3_mast.py`):** Mit `rt_charly_bleibt` steigt sie mit Duc zum Mast auf dem Kamm. Am Rastplatz erzählt sie: zwölf Geburtstage vor dem Bildschirm, statt eines Hundes ein Taser (Modell R-7), das Versteck unter Mamas Schreibtisch in Marseille. [Drehbuch 5.29](../welt/drehbuch_akt3.md)
- **Das Rätsel der Mutter:** drei Sicherheitsfragen (*First pet*, *Favourite place*, *What makes Charlotte happy?*). Die Antwort der Mutter (*Being the best*, `a3_mast_mutter_antwort`) öffnet, Charlys eigene (*Danzel. Ten.*, `a3_mast_eigene_antwort`) löst den Alarm aus. Dann ruft die Mutter an: *“Charlotte. You're cold. Put on your jacket.”* Duc nimmt das Handy, reicht es ihr oder stellt sich vor die Kamera. [Drehbuch 5.29](../welt/drehbuch_akt3.md)
- **Abschalten oder weiterlaufen:** `a3_mast_aus` (*“Nobody's watching. Is this what everybody else has?”*, Bà Tư sagt auch ohne Haus aus) oder `a3_mast_an` (Elsa bekommt die Aufnahme, Karte „The Mast Recording“ in der Kommission, auf der Festa winkt Charly dem Licht). [Drehbuch 5.29](../welt/drehbuch_akt3.md)
- **Borrowed (`a3_charly_geld`, Karte ab Tag 26, sobald eine Baustelle begonnen ist):** Sie holt heimlich Geld vom Konto ihrer Mutter (Ravenel Défense macht Geschäfte mit Alon) und gibt es Casanova: *“Three out of ten for stolen. Eight for borrowed.”* Jede offene Baustufe kostet 20 % weniger. Mit dem zweiten Chip steht ihr Name auf Casanovas Tafel (`a3_charly_tafel`). [Drehbuch 5.28, 4.1](../welt/drehbuch_akt3.md)
- **Ten (7.7, `a3_paar_charly`):** Danzel näht ihr einen grauen Kapuzenpulli mit Laptop-Tasche und RED am Kragen. Sie gibt ihre erste Zehn und sagt: *“I want to stay. Here. In the shop. With you.”* Ducs Antwort setzt `_zehn`, `_neun` oder `_allein`. [Drehbuch 7.7](../welt/drehbuch_akt3.md)
- **Festa:** Beide sitzen auf den Stufen vor Le Théâtre Rouge. Nach Alvas Flamenco sagt sie *“Ten”* und küsst Danzel, kurz und vor allen: *“Eleven.”* [Drehbuch 7.7, 5.27](../welt/drehbuch_akt3.md)
- **Kommission:** Mit `bl_funk_charly` legt sie den Funkspruch vor: *“Twenty-one forty. He said 'tonight'. Seven out of ten for clarity.”* [Drehbuch 5.25](../welt/drehbuch_akt3.md)
- **Vermerk (Drehbuch 5.29, E-125, E-126, E-127):** Aus „hackt Alons Satelliten“ wird der Mast mit dem roten Licht, ohne Charly schafft es Rosi. Charly und Danzel sind ein Paar (E-127), das ersetzt die Freundschaft Charly und Rosi (E-125) und die Freundschaft mit Danzel (E-126). Ohne `rt_charly_bleibt` kommt keine dieser Szenen.


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

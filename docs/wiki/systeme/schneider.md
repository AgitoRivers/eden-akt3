# Danzels Aufträge und neue Outfits

> Stand 30.10.2026 · Duc: „Es muss Spaß machen und uns eine Mechanik geben, neue Outfits freizuschalten.“ Quellen: `kern/schneider.py`,
> `werkzeuge/eden_rise/ereignisse_schneider.py`, Plugin `eden-schneider`, Test `tests/test_schneider.py`.

Gibt es nur, wenn „Le Théâtre Rouge“ offen ist. Er öffnet nach der Red-Trio-Quest in beiden Ausgängen, auch wenn das Trio zerbrochen ist (Duc 01.11.2026). Dann begrüßt Danzel knapp und ernst (`gruss_allein`, `text_allein`). Nur wer die Quest nie spielt, hat keinen Laden. Das Bringen von Material ist keine Aktion und kostet keine Phase.

## Dorfaufträge

1. Im Laden hängen unter **Orders** höchstens **zwei** Bestellungen, ohne Frist. Kunden, die Duc noch nicht kennt, kommen nicht dran.
2. Duc bringt das Material. Es zählt zu den Rohstoffen und belegt keinen Taschenplatz.
3. Am nächsten Tag kommt beim Tagesbeginn die Übergabe an der Piazza, kurz und vertont.
4. Am Ende wählt Duc: **Lohn nehmen** (Geld, Ruf +1) oder **darauf verzichten** (Ruf +2, Vertrauen des Kunden). Danzels Vertrauen steigt in beiden Fällen.

So hat der Ruf eine feste Quelle gegen das Verblassen ([`dorf_redet.md`](dorf_redet.md)).

| Auftrag | Kunde | Material | Lohn |
|---|---|---|---|
| An Apron With Room | Bà Tư | 2 Cloth | 30 € |
| A Strap That Holds | Mina | 2 Leather | 35 € |
| The Old Jumper | Petru | 2 Wool | 25 € |
| A Deeper Sleeve | Don Anghjulu | 3 Cloth | 40 € |
| A Waistcoat for a Businessman | Totò | 2 Cloth, 1 Coral | 50 € |
| A Coat for Bad Weather | Elsa | 1 Wool, 1 Leather | 45 € |
| A Plain Shirt | Sandru | 2 Cloth | 30 € |
| A Hat for the Mayor | Madame Casanova | 2 Feather, 1 Cloth | 70 €, setzt `danzel_festa_auftrag` |

## Woher das Material kommt

| Rohstoff | Quelle |
|---|---|
| **Cloth** | Stoffballen bei Totò (15 €), sobald Danzels Laden offen ist |
| **Corsican Wool** | bei Danzel (15 €), wenn Duc Ghjuvan kennt und er lebt |
| **Import Wool** (zählt als Wool) | bei Totò (40 €), wenn Ghjuvan tot ist oder Duc ihn nicht kennt |
| **Boar Leather** | je besiegtem Keiler 1 |
| **Red Coral** | Fundsache beim Angeln am Meer |
| Gull Feather, Cork | wie bisher |
| **Sea Silk** | nur beim Tauchgang, kommt mit dem Tauchgang |
| **Ballistic Weave** | Idee: aus der Forschungsanlage, kommt mit der Anlage |

## Outfit-Quests (Pilot gebaut 31.10.)

Beschluss Duc (E-104). Quest-Outfits brauchen kein Schnittmuster, ihr Maßstück (`"quest": true`) steht im Laden, sobald seine Bedingung gilt. Die übrigen Outfits laufen vorerst weiter über Schnittmuster und Maßstück unten:

1. **Die Quest gibt das Schnittmuster,** nicht mehr jeder dritte Auftrag. Acht Aufträge hätten nur zwei Muster ergeben. Die Aufträge bleiben der Weg zu Ruf und Material.
2. **Vier Schritte:** Wunsch, ein besonderes Material mit eigenem kleinen Abenteuer, Anprobe mit genau einer Wahl, Anlass mit Echo und Reaktionen im Dorf.
3. **Start erst nach der passenden Leiter-Szene.** Die Quest setzt nach dem Geheimnis an und erzählt es nicht noch einmal.
4. **Kein Kleiderschrank:** Bei Alltags-Outfits entscheidet am Ende eine Frage (“Every day, or only when it matters?”), änderbar bei Danzel.
5. **Festa ohne eigene Quest:** Danzel entwirft die Kleider, in der Schlussszene von Akt 3 trägt jede ihres.
6. **Pilot:** Sophias Lesung, gebaut in `werkzeuge/eden_rise/ereignisse_outfit_quest.py`, Test `tests/test_outfit_quest.py`, Text in `docs/brain_trust/QUEST_SOPHIA_LESUNG.md`. Vertonung kommt ganz am Ende.

**Ablauf der Lesung:** Start zwei Tage nach *Fourteen*, wenn der Laden offen ist. Am nächsten Tag erzählen Danzel und Totò vom Mantel, am selben Abend spielt Duc drei Hände gegen Yamamoto. Wer zwei richtig liest, bekommt den Mantel gratis und Ruf +1, sonst kostet er 40 €. Das Maßstück kostet Mantel und 60 €. Am Tag danach kommt die Anprobe mit der Wahl des Namens im Kragen, am nächsten Abend die Lesung, frühestens drei Tage nach dem Wunsch. Ruf bis 1, 2 bis 3 oder ab 4 entscheidet, wie voll die Bar ist. Die Lesung gibt Ruf +2. Der Mantel ist Anlass-Outfit und ersetzt die Concierge-Uniform nicht.

Ohne Laden, also ohne die Red-Trio-Quest, gibt es keine Quest und kein neues Outfit. Es gibt keine Ersatzfassung.

## Outfits freischalten

- **Schnittmuster:** Jeder **dritte** fertige Dorfauftrag gibt eines (`schneider.muster`).
- **Maßstück:** Ab Vertrauen 3 steht es im Laden. Es kostet Material, Geld und ein Schnittmuster und kommt am nächsten Tag als eigene Szene.
- **Outfit:** Danach ersetzt das neue Set ihre Standardkleidung (`personen.<id>.set_frei` → `buehne.set_waehlen`). Regeln für Ort und Phase, etwa der
  Badeanzug am Pool, gehen weiter vor. Fehlt das gerenderte Set, bleibt alles wie bisher.
- **Festa:** In der Schlussszene von Akt 3 trägt sie, was Duc für sie hat machen lassen (noch nicht gebaut).

**Pilot (31.10.):** Chiaras Dress Whites statt der Bridge Jacket, weil sie Opas Navy-Jacke schon hat. 3 Wool, 1 Aquamarin aus der Tasche oder Truhe (Knöpfe), 110 €. Der Stein konkurriert mit Ripostes Upgrade. Die Ärmel bleiben leer: Platz für die vier Streifen, die sie sich selbst verdienen will (Geheimnis Yachtmaster, Bruder Jonas). Die anderen sechs kommen nach Ducs Abnahme des Piloten. Der Bildsatz liegt seit 01.11. als `Chiara Sonnberg\set8` „Dress Whites“ vor: weiße Jacke mit Aquamarin-Knöpfen, goldener Anker-Pin rechts, dünne Goldkette, offenes Haar. Sie trägt ihn, sobald das Flag `sn_dress_whites_fertig` gesetzt ist (`set_frei`).

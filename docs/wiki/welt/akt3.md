# Akt 3 · Tag 24–35

> Seit E-114 endet die Belagerung an Tag 23. Akt 3 hat damit 12 Tage, Woche 4 wird kürzer, Tag 35 bleibt. Buenaventuras Entschuldigung rückt auf Tag 24. Der Kalender ist noch nicht gebaut.

> Stand 01.11.2026 · Besitz: Brain Trust · **Grundton von Duc gesetzt, nichts gebaut.** Vorgaben zu Kommission, Villa und Epilog: E-096, [`dorf_figuren.md`](dorf_figuren.md).

## Der Grundton (Duc 01.11.2026)

Akt 3 lässt den Spieler nach der Belagerung durchatmen und spielen, mit wenigen ernsten Missionen.

- **Das Dorf wieder aufbauen:** Das ist der Kern. Duc hilft dabei.
- **Romanzen fertig spielen.**
- **Mechaniken meistern:** Angeln, Auffangstation, Kochen und die anderen.
- **Die Festa vorbereiten:** Casanova vergibt Aufträge, zum Beispiel Essens- und Rohstoffbestellungen. Die Festa bleibt die Schlussszene ([`akt2_kalender.md`](akt2_kalender.md)).

## Der Aufbau (Duc 01.11.2026)

Woche 4 gehört dem Durchatmen, Woche 5 zieht an. Die Spitze ist die Villa mit Alons Angebot an Tag 34, dann folgen die Kommission an Tag 35 und die Festa. Casanovas Aufträge entscheiden, wie voll die Festa im Schlussbild ist.

## Wer sagt aus? (Duc 01.11.2026)

Alon bedroht das Dorf nicht mit Gewalt, sondern mit dem, was es zum Leben braucht: Jobs im A.V. Market, Kredite, Anwaltsbriefe. Mina muss die Briefe selbst zustellen.

- **Woche 5:** An Tag 35 fragt die Kommission, wer gesehen hat, was wirklich geschah. Duc überzeugt die Leute einzeln. Das gibt den ruhigen Tagen ein Ziel und zählt auf die Säule Gemeinschaft.
- **Das Fischernetz:** Wer aus Angst geschwiegen hat, dessen Name fehlt am Ende ([`enden.md`](enden.md)).
- **Buenaventura:** Er sieht sich im Fernsehen als Schuldigen, ist erst stolz (*“I am famous!”*), dann beleidigt, weil er das gar nicht war. Er will als einziger Zeuge freiwillig aussagen, und ihm glaubt niemand.

## Buenaventura wird Eco-Kapitän (Duc 01.11.2026)

Er sagt bei der Kommission aus. Danach werden seine Männer Touristenführer in der Grotte und helfen bei Ausfahrten und Öko-Touren. Buenaventura wird Head of Sea Captains Eco Tours und bekommt seine eigene Insel: die Grotte, mit Zukunft. Das ist der wholesome Abschluss der [Schuldenkette](ortskapitel_tauchgang.md#die-schuldenkette-duc-01112026).

**Die Entschuldigung (Duc 01.11.2026):** Am Anfang von Woche 4 treten Buenaventura und seine Männer vor das Dorf, entschuldigen sich und schwören, es wieder gut zu machen. Sie wissen nicht wie, aber sie werden eine Lösung finden. Die Eco Tours sind am Ende diese Lösung, niemand kennt sie an diesem Tag schon.

Entwurf:
- **Buenaventura:** We burned your houses. I gave the order to stop, and I gave it too late. I am sorry. I don't know how a man makes that right. I have a flag, an anthem and forty men who can carry stones. We will find a way. I swear it.
- **Petru:** Hm. Then carry stones.

**Bibis Vorschlag (Duc 02.11.2026, nicht gebaut):** Hat sie die Station und `mo_eco_idee`, kommt die Lösung von ihr: *“So he's got forty men, a boat and nothing to do? And they know every rock in that bay? Doudou. Doudou, come here. I need you to do some numbers.”* Ohne Bibi muss die Lösung anders kommen.

**Duc 01.11.2026 bestätigt:**
- **Erst wieder aufbauen:** Die Fackelpiraten haben das Dorf angezündet. Bevor jemand Touren führt, arbeiten sie in Woche 4 beim Wiederaufbau mit, zuerst an den Häusern, die sie selbst angesteckt haben. Der Fackelpirat führt am Ende Touristen mit derselben Fackel durch die Fackelgalerie.
- **Riscossores Buch:** Buenaventuras Aussage gehört zur Wiedergutmachung, sein Schwur zwingt ihn dazu. Das Dorf glaubt ihm, weil es ihn Steine tragen sieht. Die Kommission glaubt ihm nicht, bis der alte Mann mit einer Orange auftaucht und sein Schuldenbuch aufschlägt. Darin steht, was Alon dem Kapitän angeboten hat. Er sagt das nicht aus Güte: *“A man in prison pays nobody.”* Hat Gennaro die Kiste das Leben gekostet (`gennaro_verschwunden`), bekommt Duc diese Hilfe also vom Mörder seines Freundes. Das bleibt bitter und wird nicht aufgelöst.
- **Die Insel nur bei Ebbe:** Vor der Grotte liegt ein Felsen, der nur bei Ebbe aus dem Wasser ragt. Dort steckt die Flagge: *“It is an island. Twice a day.”* Die Grotte bleibt Riscossores Grund, Buenaventura zahlt ihm aus den Touren in Raten, also *eventually*.
- **Nur im guten Weg:** Die Eco Tours gibt es, wo die Bucht frei bleibt. In den schlechten Enden verliert Buenaventura auch seine Ehre, siehe [`enden.md`](enden.md).

## Wiederaufbau: das Fundament (Duc 01.11.2026, gebaut, noch nicht angeschlossen)

`kern/aufbau.py`, Test `test_aufbau`. Jedes Haus mit `tk_haus_weg_<id>` wird eine Baustelle mit drei Stufen aus den vorhandenen Baustoffen (Timber, Slate, Iron Fittings). Ist die letzte fertig, steht `aufbau_fertig_<id>`. Nach `buenaventura_schwur` tragen die Piraten je Tag eine Stufe von selbst. Es fehlen Oberfläche, Kalender bis Tag 35 und die Szene mit dem Schwur (Entwurf oben).

## Offen

- **Folgen der Belagerung:** Kommt später. Der Vorschlag passt im Kern: Abgebrannte Häuser bleiben sichtbar, ihre Läden ziehen in Notquartiere. Ohne Yacht lebt die Crew im Dorf (`tk_yacht_weg`, `tk_haus_weg_<id>`, [`../systeme/taktik.md`](../systeme/taktik.md)).
- **Aufträge der Festa:** Welche Bestellungen es gibt und was sie bewirken.

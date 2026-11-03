# Akt 2 · Der Kalender (Tag 8–23)

> Stand 01.11.2026 · Besitz: Brain Trust · **Gerüst von Duc freigegeben (E-100). Frist, Manöver, Kriegsrat und Belagerung sind gebaut (E-113), Tauchgang und Aufgaben der Crew fehlen.** Fassung Woche 1:
> [`ortskapitel_grotte.md`](ortskapitel_grotte.md).

Alles in Woche 1 ist optional, soll aber möglichst dort passieren. In Woche 2 bereitet Duc die Belagerung vor.

## Woche 1 · „Die Insel öffnet sich“ (Tag 8–14)

| Tag | Fest | Frei empfohlen |
|---|---|---|
| 8 | Werkstatt, Unit-01 | Kloster abschließen, Farm |
| 9–10 | Logo, Vogelfoto | Berge |
| 11 | Totòs Beichte | Grotte, abends ab dann Sirene |
| 12–14 | Kevin stiehlt die Seite | Grotte beenden, Kevin, Red Trio |
| 14 | Messe, Toast, nachts Koordinaten und Alons Drohne | Letzte Chance für Kevin |

## Woche 2 · „Alon schlägt zurück“ (Tag 15–21)

| Tag | Fest | Frei |
|---|---|---|
| 15 | Frühstück: Frist bis Tag 21, Megan nennt die Aufgaben der Crew | Erste Aufgabe, Sirene nachholen |
| 16 | Red-Trio-Frist endet | Tauchgang öffnet |
| 16–18 | Tauchgang mit Überfall danach, Hauptquest, Frist Ende Tag 18 | Riposte wirkt sofort gegen den Brandtrupp |
| 18 | Holm kommt zurück, abends die Wette um Gemelli | |
| 19 | Morgens übergibt Rosi den Steel Mop und das Taser-Gewehr (`a2_steelmop`), tagsüber das Manöver auf der Taktik-Karte (Duc 01.11.2026, [`belagerung.md`](belagerung.md)) | |
| 19–20 | „Paid in Full“ | Forschungsanlage (optional), Gemelli wirkt dort gegen Drohnen; Aufgaben der Crew |
| 20 | Zum Dinner bietet Elsa ihre Hilfe an, abends der Kriegsrat (Duc 01.11.2026: einen Tag vor der Belagerung, ersetzt Tag 15 aus E-100), danach eine ruhige letzte Nacht an Bord | |
| 21–23 | Belagerung, sechs Wellen auf drei Tage ([`belagerung.md`](belagerung.md), E-114) | |

## Der Grund für die Belagerung

An Tag 14 nachts sieht Alons Drohne, dass Lea die Koordinaten der Margot hat. Die Margot ist sein größtes Risiko
([`ortskapitel_tauchgang.md`](ortskapitel_tauchgang.md)). An Tag 15 beim Frühstück wird daraus eine Frist: Das Ultimatum der
Eden Group läuft an Tag 21 aus. Der Tauchgang ist nicht der Auslöser, sondern verschärft die Lage.

**Festa und Ehrenbürger gehören nicht in diesen Kalender (Duc 30.10.):** Sie sind die Schlussszene von Akt 3, in der das Ende
preisgegeben wird und alles zusammenläuft.

## Zu ändern beim Bau

- **Red-Trio-Frist:** Tag 16 statt Tag 14: `TAGE` in `ereignisse_red_trio.py`, Startfenster `_RT` in `auftraege_eden_rise.py` und
  „bis Ende Tag 14“ in `nebenquest_red_trio.md`. `FOLGE_TAGE` bis Tag 28 öffnen, sonst entfällt `rt_pfote` (+6)
  still, wenn die Quest spät endet. `rt_bon` (Tag 19–20) bleibt erreichbar, wenn die Quest bis Tag 19 fertig ist.
- **Festa-Events:** `br_ehrenbuerger`, `ab_casanova_flamenco` und `gv_rotes_kleid` warten seit dem 01.11. auf das Flag `akt3_festa`. Sie ziehen ans Ende von Akt 3.

## Messung (30.10.2026)

Je Tag gibt es 4 freie Phasen (Tag, Nachmittag, Dinner, Abend), davon 2 für Ausflüge. Eine Niederlage kostet eine weitere
Phase. Gemessen mit `tests/expedition_sim.py klug`; dass eine Quest ohne Niederlage in eine Phase passt, ist angenommen.

| Quest | Minuten | Niederlagen | Tagesphasen |
|---|---|---|---|
| Berge ohne / mit Umwegen | 17 / 28 | 3 / 9 | 4 / 10 |
| Grotte | 12–19 | 2 | 3 |
| Red Trio | ca. 32 | 0–1 | 1–2 |
| Kevins Dächer (nicht simuliert) | – | – | 1 |
| Summe Woche 1 | | | 9–10 von 14, mit Berg-Umwegen 15–16 |
| Sirene (Flut-Nacht) | 9 | 1 | 2 Abende |

Woche 2 hat ohne Tag 21 noch 12 Tagesphasen: Tauchgang etwa 2, Anlage etwa 3, Manöver 1, bleiben 6 für Aufgaben der Crew.

## Offen

- **Aufgaben der Crew zählen als Zeit zusammen (Duc 30.10.2026):** Die Vorbereitungs-Phasen in Woche 2 sind Szenen mit der Figur und geben
  Vertrauen wie „Zeit zusammen“. Wird mit der Belagerung gebaut.
- **Tempo prüfen:** Der Bot erreicht schon an Tag 15 Begehren 5 (Chiara). Messen, wenn der Kalender bis Tag 35 läuft.

# Spieltest Akt 1 · 25.10.2026

Sechs Bot-Durchläufe (Seeds 1–6) von Tag 0 bis Tag 8 mit `tests/spieltest_akt1.py`: Nach jedem Schritt wird die
Ansicht der Spielerin ausgewertet (Events, Szenen, Ablehnungen, fehlende Bilder, deutscher Resttext). Grenzen: Der Bot
nimmt immer die erste Antwort, Szenen laufen ohne Sprachmodell, in der Anhörung klagt er die erste Verdächtige an –
Inhalt und Gefühl der Szenen prüft das nicht, dafür braucht es eine Runde von Hand.

## Ergebnis in einem Satz

Alle sechs Läufe kommen ohne Absturz durch Tag 0, Hafen, Akt 1, Anhörung und Urteil bis Tag 8.

## Behoben im Test

| # | Befund | Fix |
|---|---|---|
| 1 | 11 Szenentitel der Hauptstory waren noch deutsch („Lagebesprechung“, „Das Urteil“, …) | englisch („Briefing“, „The Verdict“, …) |
| 2 | 4 Ermittlungswege (Fall 4 und eine Nebenspur in allen Fällen) lagen in Rosis Werkstatt, die bis Tag 8 gesperrt ist | Rosi arbeitet nach dem Brand übergangsweise im Antriebsraum: Wege, Fakt- und Tipp-Texte dorthin verlegt |

## Offen, gehört anderen Paketen oder Sitzungen

| # | Befund | Wer |
|---|---|---|
| 3 | Deutscher Resttext: Läden, Gegenstände, Gerichte, Werte-Infos (Strom, Diesel, Moral …), Tratsch-Label „erzählt im Dorf“, Missionsliste „vor der Reise“, „Rosi nimmt dich mit“ | Sprachpakete Items / Modul / UI |
| 4 | Siris Lieblingsgericht steht noch als „Schwedische Kohlrouladen“ (Kåldolmar), Kanon ist Fiskesuppe (K3) | Items |
| 5 | Gegenstände in Läden, Ankauf und Jobs haben kein Bild | Items |
| 6 | Megans Profil hat kein Hintergrundbild, weil sie keinen Raum im Spiel hat (Büro/Penthouse noch nicht eingebaut) | Story/Modul, später |

## Beobachtungen fürs Design

| # | Beobachtung | Zahl |
|---|---|---|
| 7 | **Event-Dichte:** Tag 2 hat 9 Events (Hafenkette), die Tage 3–6 nur 3–5, Tag 7 eins. Der Rest sind freie Szenen („Time with …“) | je Lauf ~35–40 Events |
| 8 | **Reichweite:** Ein Durchlauf zeigt nur einen kleinen Teil des Pools. Sechs Läufe zusammen trafen 43 der 221 Akt-1-Events | ~17 % je Lauf |
| 9 | **Missionen gegen Events:** Seit dem Flirt-Ausbau erledigt der Bot in einem Seed 17 statt 19 Missionen; Engpass ist die Energie | 670 abgelehnte Job-Versuche in 6 Läufen (Bot probiert alles) |
| 10 | **Anhörung:** läuft in allen sechs Läufen bis zum Urteil; der Bot trifft dabei nie die Richtige (Bot-Grenze, kein Spielfehler) | 5× „falsch“, 1× „unbelegt“ |

Punkt 7 und 8 sind die eigentliche Designfrage: Viel neuer Inhalt (58 Events seit gestern) erreicht die Spielerin pro
Durchlauf nur zu einem kleinen Teil. Das ist gut für den Wiederspielwert, aber die Tage 3–7 fühlen sich im Bot-Lauf
dünn an.

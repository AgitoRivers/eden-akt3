# Brain Trust: „Mochi's“ mit Pokémon- und Monster-Hunter-Gefühl (31.10.2026)

Auftrag von Duc: Bibis Station mit Pokémon- oder Monster-Hunter-Gefühl und besserer Mechanik, danach so weit wie möglich bauen. Diese Runde lief ohne Duc, er schläft. Regeln: [`../wiki/systeme/tierstation.md`](../wiki/systeme/tierstation.md).

**Sienna (Game Direction):** Pokémon lebt von „alle finden“ und dem einen Freund an deiner Seite. Monster Hunter lebt von Spuren, Vorbereitung und dem Wissen, was dieses eine Tier mag. Beides passt in Bibis Field Book. Gegenvorbild: *Palworld* zeigt, wie schnell Fangen zur Fabrik wird, und *Ni no Kuni 2* mit seinen Ställen ohne Bindung. Würde jemand davon erzählen? Ja: „Ich habe einen Wolf gerettet, indem ich aufgehört habe zu kämpfen.“ ✨

**Luise (Art & Story):** Mein Einspruch zuerst: Eine Pokéball-Geste wäre in diesem Spiel ein Verbrechen. Das Halsband ist genau das, was ARK getan hat. Deshalb wird nichts gefangen. Das Tier hört auf zu kämpfen, und am Ende öffnet Duc das Tor. Bibi nennt die Hyäne „Sorry“, weil beide lachen, wenn sie Angst haben. 🥹

**Aly (Tech):** Erstaunlich wenig Neues. Der Kampf kennt schon Fassung als zweiten Sieg, `flee_at` für die Flucht und Beistand für Begleiter. `kern/kampf.py` musste ich nicht anfassen. Alle fünf Sprites liegen schon da. Calm war 29.10. gestrichen, kommt aber nur in diesen fünf Kämpfen zurück. Ehrliche Lücke: Nichts davon ist gemessen, solange der Test-Stopp gilt. 🤓

**Sora (Spielerstimme / QA):** Minute 1: schwarzer Umriss im Buch, ich will wissen, wer das ist. Minute 5: Ich haue aus Gewohnheit drauf, der Hund rennt auf drei Beinen weg, und Bibi sagt nur einen Satz. Autsch. Minute 20: Ich gehe mit Rindfleisch zum Wolf, sie legt sich hin, ich öffne das Tor und bereue es sofort. Nochmal-Lust 4 von 5. Veto gegen tägliches Füttern, deshalb reicht einmal. 😭

**Maelle (Producerin):** Preis: eine Nachtsitzung, 31 neue Sprechzeilen später (19 in den Frames, 9 im Laden, 3 mit Elsa), zwei Bilder. Dafür bleibt heute nichts liegen. Fünf Tiere, kein sechstes, Romanze und Belagerung nur als Merker. 📋

## Prüfsteine

| Prüfstein | Antwort |
|---|---|
| Spielerreise | Ich sehe einen Umriss, ich folge der Spur, ich lerne, dass Schlagen hier verliert |
| Sehnsucht | Wirksamkeit und Heimkehr: Die Station wird voller, weil ich da war |
| Vorbild | Pokémon-Sammeltrieb, Monster-Hunter-Köder, Abschied wie in *Spiritfarer*. Besser: Der Sieg ist das Gegenteil von Gewalt |
| Zeitbudget | Eine Phase je Versuch, höchstens fünf Rettungen ab Tag 12; alles andere kostet keine Phase |
| Kanon | Grauzonen-Regel E-073, E-098, Bibis Mochi-Tonfall aus ihrer Figurenseite. Neu sind die fünf Namen und die Halsband-Beweise |
| Ton | Wholesome im Ergebnis, ernst beim Weg. Kein neuer schwerer Moment |
| Wirkpunkt | `kern/mochis.py`, Test `tests/test_mochis.py` (noch nicht gelaufen) |
| Selbstkritik | Die Station sehen nur Spieler mit Versöhnung und Bibis Rat. Darum klein gehalten |
| Beleg | Kampfcode gelesen, gebaute Daten geprüft: nur Zusätze, keine bestehenden Events geändert. Balance ohne Beleg |
| Doppelung | Die Farm hat Nutztiere mit Stall und Zucht. Die Station hat keine Ställe, keine Zucht, kein Schlachten |

## Gegenrede

**Luise (Art & Story):** Sienna wollte seltene Farbvarianten wie Shinys. Nein: Ein weißes Labortier wäre kein Glücksfund, sondern ein Versuch. Stattdessen sind die Funde am Morgen die Überraschung.

**Sora (Spielerstimme / QA):** Luise, dein Abschied ist schön, aber wenn Freilassen nur Punkte bringt, lässt keiner frei. Gegenvorschlag eingebaut: Wer geht, gibt doppelt so viel Vertrauen und Ruf wie wer bleibt, und nur Freilassen zeigt den Abschiedssatz.

## Vorschläge

| # | Vorschlag | Von | Stand |
|---|---|---|---|
| 1 | Beruhigen statt Fangen, bei halben LP rennt das Tier | Luise, Aly | ⭐ gebaut |
| 2 | Field Book mit Umrissen und Seiten | Sienna | gebaut |
| 3 | Lieblingsfutter als Köder und zum Aufpäppeln | Sora | gebaut |
| 4 | Das Tor: bleiben oder gehen | Luise | gebaut |
| 5 | Ein Begleiter auf Expeditionen, Bindung 1–3 | Sienna | gebaut |
| 6 | Funde am Morgen | Sora | gebaut |
| 7 | Halsbänder als Beweis, Elsa-Event | Aly | gebaut, Wirkung bei der Kommission offen |
| 8 | Bruchteile im Kampf wie bei Monster Hunter (Halsband gezielt zerstören) | Sienna | zurückgestellt, braucht Kampfumbau |

**Selbstkontrolle:** **Sora:** Das ist die erste Idee dieser Woche, bei der ich direkt spielen will. **Maelle:** Ja, aber bis zum Probespiel ist alles Annahme.

**Maelle (Producerin):** Eine Frage an dich, Duc: Hebst du den Test-Stopp für diesen Branch auf, damit wir messen und du es spielen kannst? 📋

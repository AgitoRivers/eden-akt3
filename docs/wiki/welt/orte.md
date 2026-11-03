# Eden Rise – Orte als Bild-Novel (Entwurf)

Stand 21.10.2026 · Entwurf zur Freigabe, **noch nicht gebaut**. Gehört zu [tage_erkundung.md](../systeme/tage_erkundung.md)
und [kampf.md](../systeme/kampf.md).

Ton: spannend, mal **wholesome wie Frieren**, mal **grau wie The Witcher**, mal **Anime-Humor wie One Piece** –
je Szene eine andere Mischung.

---

## 1. Wie eine Erkundung mit statischen Bildern funktioniert

Jeder Ort ist eine **Kette von Bildern (Frames)**. Ein Frame = ein Hintergrundbild + kurzer Erzähltext + bis zu vier
Dinge, die man darin tun kann. Man läuft nicht, man **klickt sich weiter** – wie in einem Visual Novel mit Spielbrett.

| Element im Frame | Darstellung | Was passiert |
|---|---|---|
| **Erzähltext** | unten, 2–4 Sätze | Sprachmodell erzählt, was der Code festlegt (Gegner, Funde, Stand der Geschichte) |
| **Fundstelle** ✨ | leuchtender Punkt im Bild | **Sammeln** (Kräuter, Pilze, Krabben) – kostet nichts, belegt einen Taschenplatz |
| **Abbaustelle** ⛏️ | Felsen, Baum, Strauch | **Abbauen** mit passendem Werkzeug/Waffe (Spitzhacke → Erz/Granit, Axt → Hartholz, Messer → seltene Kräuter); ohne Werkzeug gesperrt |
| **Spur** 🔍 | dezentes Symbol | **Untersuchen**: Wahrnehmungs-Probe; Erfolg = Hinweis, Codex-Eintrag, versteckte Fundstelle oder Abkürzung |
| **Begegnung** ⚔️ | Gegner-Sprite im Bild, Name in Bedrohungsfarbe | Kampf (oder Reden/Fliehen); manche Begegnungen sind sichtbar und umgehbar, andere ein Hinterhalt |
| **Ereignis** 💬 | Figur oder Objekt | kleine Entscheidung (2–3 Optionen), oft mit Probe |
| **Rastplatz** 🔥 | Lagerfeuer-Symbol | einmal heilen; hier kann man **zur Yacht zurück** (sichere Rückkehr mit allem Gesammelten) |
| **Weg** ➡️ | Pfeil(e) am Bildrand | **Weiter** zum nächsten Frame; an Gabelungen 2 Pfeile = Wahl |

**Push-your-luck (Dave the Diver):** Je weiter hinten der Frame, desto höher das Level der Gegner und desto besser die
Funde. Zurück zur Yacht geht nur an Rastplätzen und am Ortseingang. Wer stirbt, verliert die Tasche bis auf einen
geborgenen Gegenstand (siehe tage_erkundung.md).

**Spur-Uhr:** Story-Ereignisse mit Zeitdruck bekommen eine sichtbare Uhr (z. B. 4 Segmente). Jeder Frame kostet ein
Segment, Umwege kosten zusätzliche. Was passiert, wenn die Uhr abläuft, entscheidet die Geschichte (nicht Game Over).

**Ortsfortschritt:** Ein Ort hat ein **Ortskapitel**; der Fortschritt bleibt zwischen den Besuchen erhalten.
**Schnellreise-Punkte** (Kloster, Turm …) werden durch die Geschichte frei und sparen den Weg durch die ersten Frames.

**Bilder pro Ort:** 8–12 Hintergründe (Prompt Studio, Setting-Deck), Gegner als Sprites darüber, Fundstellen als
kleine Overlay-Icons. Varianten für Tag/Abend sind optional.

---

## 2. Macchia & Kloster San Martinu (Level 1–7)

*Wholesome + Trauer (Frieren), Rätsel um die Tiere, Humor durch die Ziege und Isabelles Kräuterunfälle.*

**Auftakt im Dorf (Hafen):** Madame Casanova ist misstrauisch gegenüber der Yacht-Crew („Schon wieder reiche Leute,
die unsere Bucht als Kulisse benutzen“). Sie gewinnt Vertrauen, wenn Duc hilft: Seit drei Wochen kamen keine Kräuter,
kein Käse und keine Briefe mehr vom Kloster San Martinu oben in der Macchia. Nonna Fiora und ihre Novizin Isabelle
leben dort mit den Mönchen. Casanova: „Fiora hat noch nie einen Markttag verpasst. Noch nie.“

| Frame | Bild | Level | Inhalt |
|---|---|---|---|
| 1 | Macchia-Pfad hinter dem Dorf | 1–2 | Ratten, Schlange · Sammeln: Wildkräuter · Spur: Krallenspuren an einer Korkeiche, viel zu groß für einen Hund |
| 2 | Bachlauf mit Steinbrücke | 2 | Wildschwein · **Angelplatz Fluss** wird frei · Spur: eine tote Ziege, um den Hals ein Metallring mit blinkendem Licht (erster, unerklärter Hinweis) |
| 3 | Verlassene Hirtenhütte | 2–3 | Verwilderter Hund · Rastplatz · **Ereignis „Capra“:** eine Ziege mit Glocke folgt Duc ab jetzt (Humor: sie frisst Fundstücke aus der Tasche, wenn man nicht aufpasst – oder findet Trüffel, wenn man sie füttert) |
| 4 | **Kloster San Martinu** | – | Nonna Fiora (mit Kochlöffel in der Hand, „Bleib stehen, oder ich koche dich!“) und Isabelle. **Schnellreise-Punkt** wird markiert, aber erst nach dem Ortskapitel frei |

**Was im Kloster erzählt wird (Frame 4):** Vor drei Wochen tauchten plötzlich wilde Tiere auf – Affen, Hunde, ein
Löwe – und griffen alles an. Bruder Ambrosius, der Abt, zog mit den anderen Mönchen los, um ihren Anführer, den Löwen,
zu erlegen. Sie kamen nicht zurück. Heimlich ist der junge **Frederico** mitgegangen, ein Waisenjunge, „ein Engel von
Kind“, der auch einmal etwas beitragen wollte. Nonna und Isabelle können nicht weg, die Tiere belagern die Mauern.
Ab hier sind **Nonna Fioras Hof und Isabelles Apotheke** nutzbar.

| Frame | Bild | Level | Inhalt |
|---|---|---|---|
| 5 | Waldgrenze unter den Felsen | 4 | Affe · Abbauen: Hartholz · **Tagebuchseite 1** von Bruder Ambrosius |
| 6 | **Schlucht – Gabelung** | 5 | Hund · Zwei Wege: **Blutspur + eine kleine Sandale** (Fährte) oder **Glitzern in einer Felsnische** (Schatz). Ab hier läuft die **Spur-Uhr (4 Segmente)** |
| 6b | Felsnische (nur Schatzweg) | 5–6 | 2 Kämpfe, Truhe mit **seltener Waffe**, kostet 2 Segmente extra |
| 7 | Verlassenes Lager der Mönche | 6 | Bilder ohne Blut, nur Stille: verstreute Kutten, ein umgestürzter Kessel. **Tagebuchseite 2:** „Das Tier trägt etwas im Nacken, das blinkt. Es leidet, wie wir.“ (grau: der Löwe ist kein Monster, sondern ein Opfer) |
| 8 | **Löwenbau** in einer Höhle | 7, Boss | **Löwe** (Tödlich/Albtraum je nach Level). Nach dem Sieg: **Steuerchip** im Nacken (Missionsgegenstand), Gravur „A.V. Estates – Behaviour Control Unit“ → erster Hinweis auf **Alons verstecktes Anwesen** |

**Ausgang je nach Spur-Uhr:**
- **Fährte direkt gefolgt (Uhr nicht abgelaufen):** Frederico hat sich hinter dem Bau versteckt und lebt. Er hält den
  **Goldenen Streitkolben mit Elfenbeingriff** von Bruder Ambrosius und eine kleine Tasche mit dessen Habseligkeiten:
  „Er hätte gewollt, dass du ihn hast.“
- **Zuerst den Schatz geholt (Uhr abgelaufen):** Frederico liegt neben dem Abt. Den Streitkolben findet Duc trotzdem,
  ohne Worte, ohne Übergabe.

**Zurück im Kloster (Frame 4) – die traurige Kunde:** Die Mönche sind alle tot. Nonna nennt jeden beim Namen und erzählt
zu jedem eine kleine Geschichte (Frieren-Moment).
- **Frederico gerettet:** Vertrauen bei Nonna Fiora und Isabelle direkt **+1 Stufe**. Frederico wird der **Botenjunge**
  und bringt jeden Morgen die Ernte an Bord (mit eigenem kleinem Charme: er grüßt jede Stewardess mit Namen).
- **Nicht gerettet:** Beide sind am Boden zerstört, Vertrauen beginnt bei **0**. Die Ernte bringt ein namenloser Bote
  aus dem Dorf (nur im Text erwähnt).
- In beiden Fällen: **Schnellreise zum Kloster** frei, Missionsgegenstand **Steuerchip** für den Alon-Bogen,
  Madame Casanova gewinnt Vertrauen in Duc.

---

## 3. Berge & Genueser Turm – Die Legion und Petrus Tochter (Level 5–8)

*Grau wie The Witcher: drei Wege, keiner ganz sauber. Leiser Humor: Sergent Wolff und die Ziege Capra.*

**Auftakt:** Petru (Fischer und Handwerker im Dorf) hat vor fünf Jahren seine Frau an den Krebs verloren. Seitdem ist
seine Tochter **Laetitia** (24) sein Ein und Alles – und er ist der übervorsichtige, misstrauische Vater, der jeden
Verehrer mit Blicken vertreibt. Laetitia ist zu den Sommerhütten der Hirten hinauf und nicht zurückgekommen. Im Dorf
heißt es, sie sei mit einem Fremden in Uniform gesehen worden. Petru bittet Duc, sie zu holen.

| Frame | Bild | Level | Inhalt |
|---|---|---|---|
| 1 | Serpentinenpfad mit Kastanien | 5 | Wildschwein · Sammeln: Kastanien, Steinpilze · Spur: frische Abdrücke von Militärstiefeln |
| 2 | **Genueser Turm** | 5–6 | Patrouille der Fremdenlegion unter **Sergent Kaspar Wolff**: streng, korrekt, trockener Humor, zitiert gern die Dienstvorschrift. Ist Capra dabei, wird er weich („Eine Ziege. Im Einsatz. … Darf ich?“). Sie jagen den Deserteur **Caporal Adrien Morel**. Ereignis: helfen oder lügen. **Schnellreise-Punkt** |
| 3 | Bergsee | 6 | Affe · **Angelplatz See** · Laetitias Halstuch treibt im Wasser · Abbauen: Granit |
| 4 | Felskamm im Nebel | 6–7 | **Alons Agenten** in schwarzen Anzügen suchen ebenfalls Adrien (sie wollen ihn zurück, bevor er redet) – mehrere Kämpfe. Sie finden ihn nicht. Spur: ein Funkgerät mit dem Logo „A.V. Estates“. Abbauen: Eisenerz |
| 5 | **Bergerie** (Hirtenhütte) | 7 | Laetitia und Adrien, er ist verwundet. Seine Einheit wurde **heimlich an Alons Firma ausgeliehen**, um ein Anwesen in den Bergen zu bewachen. Dort hat er Tiere in Käfigen gesehen, mit blinkenden Halsbändern. Er hat Fotos gemacht und ist geflohen. Auf Desertion steht Gefängnis |
| 6 | Bergerie, Abend | 7–8 | Ein letzter Trupp Agenten (Brute + Agenten) – danach kommt **Wolff** mit seiner Patrouille. Die Entscheidung |

**Die Entscheidung (kein richtig, kein falsch):**

| Weg | Was passiert | Folgen |
|---|---|---|
| **A – Adrien an Wolff übergeben** | Gesetz ist Gesetz. Wolff dankt knapp | **Geld** und ein Ausrüstungsgegenstand der Legion, der **Einschüchtern verstärkt**. Laetitia geht mit Petru heim und spricht kein Wort mehr mit Duc. Die Fotos verschwinden in den Akten |
| **B – Den beiden zur Flucht verhelfen** | Über **Totòs Schmugglerroute** nachts aufs Meer | Es fühlt sich richtig an. Aber **Petrus Vertrauen fällt auf 0**, und der Fremdenlegionär-NPC bleibt verwehrt. Die Fotos nimmt Adrien mit |
| **C – Wolff die Fotos zeigen** | Wolff glaubt Duc nicht und greift an. **Kampf gegen Wolff** – erst nach dem Kampf beruhigt er sich und sieht sich die Bilder an | **Verloren:** wie Weg A. **Gewonnen:** Wolff begreift, dass die Legion missbraucht wurde, und meldet Adrien „im Einsatz gefallen“. Adrien bleibt in der **Hirtenhütte** – **neuer NPC (der Fremdenlegionär) mit Schnellreise-Punkt**. Laetitia kehrt zu Petru zurück, **Petrus Vertrauen startet bei 1**, und Adrien schenkt Duc sein **Kampfmesser der Fremdenlegion**. **Alons Anwesen ist gefunden** → nächstes Ortskapitel |

**Verwebung:** Der Steuerchip aus dem Kloster und Wolffs Haltung (hat Duc am Turm gelogen?) können den Kampf in Weg C
erleichtern; Totòs Vertrauen ermöglicht Weg B. Beide Orte führen zum **Anwesen von Alon** (ausgebrochener Zoo,
Madame Casanovas Groll) als späterem Ort.

---

## 4. Offene Punkte

- Namen: Kloster **San Martinu**, Abt **Bruder Ambrosius**, Waisenjunge **Frederico**, Petrus Tochter **Laetitia**,
  Legion: **Sergent Kaspar Wolff**, Deserteur **Caporal Adrien Morel** (später der Fremdenlegionär-NPC).
- Ziege „Capra“ ist wiederkehrende Begleiterin (Humor + Trüffel), entschieden 21.10.2026.
- Bilder: je Ort 8–12 Hintergründe; Sprites für Nonna Fiora, Isabelle, Frederico, Wolff, Adrien, Laetitia, Capra.
- Weitere Orte (Strandgrotte, Wrack & Tiefsee, Alons Anwesen) im gleichen Muster.

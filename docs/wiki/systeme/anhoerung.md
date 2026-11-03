# Die Anhörung · Megans Verhandlung an Tag 7

> Stand 26.10.2026 · Besitz: Character Design · Quelle: `kern/anhoerung.py` (Regeln), `client/plugins/eden-hearing`
> (Bildschirm), `werkzeuge/eden_rise/anhoerung_aussagen.py` (Aussagen je Fall), Test `tests/test_verhandlung.py`.
> Fall-Auflösungen stehen hier nie – nur, wie die Verhandlung funktioniert.

## Worum es geht

Am Tag 7, mittags im Salon, urteilt Megan über die Nacht des Ausfalls. Die Anhörung ist die **Endszene von Akt 1**:
Kopfleiste, Handy-Menü, Chat und Meldungen des Spiels sind ausgeblendet, es gibt nur Megan, die Crew und Ducs Notizen.
Gespielt wird wie bei *Ace Attorney*: Jemand behauptet etwas, Duc zeigt mit einem Beweis, wo es nicht stimmt.

## Ablauf

1. **Auftritt:** Titelkarte *„The Hearing“*, Klick auf *Begin*. Megan sagt ihren Satz aus Antibes (je nach Antwort an Tag 0).
   **Der Werftbericht** (seit 27.10.): Ein Blatt mit Briefkopf *„Eden Marine Works · Repair & Survey – Incident Report“* – die **konzerneigene Werft der Eden Group** (Duc 27.10.) und dem
   Stempel *Preliminary* fällt auf den Tisch (Befund: *Wear and tear*, Haftung: *None identified*). Megan erklärt ihn
   (3 vertonte Varianten): Er ist die **Grundlage der Anhörung** und geht so an Eigner und Versicherung, wenn niemand
   widerspricht. Die Werft will Verschleiß – dann prüft niemand ihre eigene Wartung. Weil sie zur Eden Group gehört, steht Megan als Fleet Director zwischen Konzern und Crew: Ein bequemer Bericht schützt das eigene Haus. Deshalb rudert sie später zurück.
   Klick auf *Read the report*, dann Titelkarte *What?*.
2. **Drei Punkte nacheinander**, jeder mit eigener Titelkarte:
   - **What?** – was in der Nacht mit dem Antrieb passiert ist (Megan liest den Bericht der Werft vor),
   - **Who?** – wer es war (die Angeklagte spricht selbst),
   - **Why?** – warum genau das den Antrieb zerstört hat (Megan fragt nach).
3. **Nach Punkt 1** halten **alle Verdächtigen** ein kurzes Plädoyer (je zwei Sätze), warum sie es nicht waren. Dann sagt
   Megan: *„Arrange your evidence and name the one who did it.“* Duc sieht dabei seine Notizen durch und **klagt eine
   Person an** – oder sagt *„Nobody alone“*. Die Angeklagte reagiert und sagt dann in Punkt 2 selbst aus.
4. **Punkt 2 ist ein Duell** (seit 26.10.): Nach dem Namen raunt der Saal, die Angeklagte reagiert, dann kommt die
   Titelkarte *„Testimony of …“* (*Hear the statement*). Hakt Duc bei ihrer **falschen** Zeile nach, stockt sie hörbar
   und ihr Gesicht wird nervös – bei wahren Zeilen bleibt sie ruhig. Liegt Duc daneben, stichelt sie (*„Is that all
   you've got?“*). Hält jemand aus Loyalität zu ihr, steht diese Person auf und gibt ihr ein Alibi; wer nicht mehr an Bord ist (z. B. Holm ab Tag 3), wird per **Videoanruf** auf Megans Tablet zugeschaltet. Danach sitzt der Zeuge als kleiner Chip neben dem Schild der Angeklagten, nicht als Figur auf der Bühne. Nach *OBJECTION!*
   **bricht die Angeklagte zusammen** (zwei Sätze, Bild wackelt), dann raunt der Saal und Megan schließt den Punkt.
   War es die falsche Person, atmet sie auf, wenn der Beweis woanders hinzeigt.
5. **Punkt 3 schließt die Kette:** Vor der Aussage zeigt ein **Kettenbrett** *What* und *Who* als angeheftete Zettel
   (✓ bewiesen, ≈ geblufft, ✕ offen), *Why* bleibt leer. Nach *OBJECTION!* fliegt der dritte Zettel aufs Brett und der
   rote Faden zieht sich durch (*„What, who, why. The chain holds.“*); die Überführte sagt noch einen letzten Satz. Wird
   *Why* nicht bewiesen, reißt der Faden.
6. **Tratsch:** Nach Punkt 1, nach der Anklage, nach dem Zusammenbruch und nach dem Urteil tuscheln **2–3 Leute aus
   der Crew** miteinander (unten eine Reihe Köpfe, die sprechende Person leuchtet), bis Megan *„Quiet, please.“* sagt.
   Wer angeklagt oder nicht an Bord ist, redet nicht mit. Zwischen allen Momenten liegt eine kurze Atempause.
7. **Das Geständnis:** Ist die richtige Person überführt, fragt Megan *„Why?“*, und sie erzählt in 4–6 vertonten Sätzen
   ihr Motiv (Falldaten `gestaendnis`, alle fünf Fälle). Musik dazu: eher traurig, sucht Story (Auftrag 27.10.).
8. **Das Urteil im selben Bildschirm** (seit 26.10., vorher eigene Szenen): Titelkarte *„The Verdict“* → Megan fragt
   nach **Ducs eigener Rolle** (*Tell the truth* / *Say nothing*) → **Plädoyer** (*Ask for mercy* / *Share the blame* /
   *Demand the full penalty*), darunter offen, was Megan für Gnade braucht → Stille-Beat *„Megan decides …“* → Megans
   vertontes Urteil → Reaktion der Angeklagten → Tratsch → *„The hearing is closed“*. Die Szenen *And You, First
   Officer?* und *The Verdict* entfallen danach (Flag `verhandlung_urteil`).

## Ausgänge der Anhörung

| Ausgang | Auslöser | Folge |
|---|---|---|
| **Erbarmen** (*mercy*) | Richtige Person angeklagt, alle drei Punkte **bewiesen ohne Bluff**, Motiv bekannt, Duc war **ehrlich** über seine Rolle, Megan hat noch Geduld – und Duc bittet um Gnade oder teilt die Schuld | Bleibt an Bord ohne Strafe; Megan-Vertrauen +1, Moral +1, Vertrauen der Überführten +2; **Megans Prämie** für Duc; Flag `urteil_erbarmen` |
| **Aufgeklärt** (*probation*) | Richtige Person, alle drei Punkte belegt (Bluff zählt), Megan hat Geduld – aber Erbarmen nicht möglich oder nicht erbeten, und **keine** volle Strafe gefordert | Bewährung für die Saison, Prämie der Überführten weg; **Megans Prämie** für Duc; Flags `urteil_aufgeklaert`, `bewaehrung_<person>` |
| **Gefeuert** (*full penalty*) | Wie *Aufgeklärt*, aber Duc fordert **die volle Strafe** | Die Überführte **verlässt heute das Schiff**; Vertrauen der Überführten −2; **Megans Prämie** für Duc; Flags `urteil_aufgeklaert`, `gefeuert`, `gefeuert_<person>`, `strafe_gefordert` (Folgen für Akt 2: Story). Hatte sie Duc unter der Woche **gestanden**, ist es **Verrat**: −3 statt −2, eigener Abgangssatz, Flag `verrat_<person>` |
| **Unbelegt** | Richtige Person, aber nicht alle drei Punkte belegt – oder Megans Geduld ist aufgebraucht | Megan urteilt selbst: Prämie der Crew gestrichen, Frage bleibt offen; Moral −1; Flags `urteil_unbelegt`, `praemie_gestrichen` |
| **Falsch** | Duc klagt eine Unschuldige an | Prämie gestrichen, die Beschuldigte wartet auf eine Entschuldigung; Vertrauen der Beschuldigten −2 (mit *Ask for mercy* nur −1), Moral −1; Flags `urteil_falsch`, `praemie_gestrichen`. Mit *Demand the full penalty* gegen die Unschuldige zusätzlich Moral −1, eigener Crew-Tratsch, Flag `strafe_gegen_unschuldige` |
| **Offen** | Duc sagt *Nobody alone*, obwohl es eine Verantwortliche gibt (oder ohne belegte Kette), oder nennt gar keinen Namen | Prämie gestrichen, Megan droht Kündigungen an; Moral −1; Flags `urteil_offen`, `praemie_gestrichen`, `kuendigung_angedroht` |
| **Entlastet** | *Nobody alone*, und es war tatsächlich niemand allein – mit belegter Kette (seit dem Streichen von Fall 6 nicht mehr erreichbar, Regel bleibt im Code) | Wer beschuldigt war, ist entlastet; Megan-Vertrauen +1, Moral +1; Flag `urteil_entlastet` |

**Jede Wahl wirkt** (seit 26.10.):
- **Megans Prämie:** Bei *Erbarmen*, *Aufgeklärt* oder *Gefeuert* (also richtige Person, Kette belegt) bekommt Duc
  **500 €** aufs Konto, mit Bluff oder „halb“ bewiesenen Punkten **250 €**. Zum Vergleich: ein Job bringt 60–200 €.
  Megan sagt es vertont.
- **Moral in dieser Seite:** Alle Moral-Angaben der Anhörung sind *Momente* der Crew-Moral (−5 bis +5, `kern/moral.py`) und zählen
  dort **doppelt**: „Moral +1“ wirkt also als +2, „−1“ als −2 (Stand 27.10.2026).
- ***Share the blame* kostet immer:** Megan-Vertrauen −1 (sie hält Duc für mitschuldig), Moral +1, Flag
  `schuld_geteilt` – auch wenn es keine Gnade gibt.

Nebenbei zählt **Ducs Rolle**: *Tell the truth* setzt `rolle_ehrlich` (Voraussetzung für Erbarmen), *Say nothing*
setzt `rolle_verschwiegen`. Bricht Megan wegen leerer Geduld ab, gibt es weder Rolle noch Plädoyer – sie urteilt sofort.

## Ein Punkt: drei Zeilen, eine ist falsch

Jede Aussage hat **drei Zeilen**, auf dem Bildschirm drei Spalten. **Zwei Zeilen sind wahr, eine ist falsch.** Man muss
nicht raten: Die falsche Zeile ist die, die mit einem Fund aus der Woche kollidiert.

| Was Duc tun kann | Was passiert | Kosten |
|---|---|---|
| **Ask** (nachhaken) bei einer Zeile | Die Antwort steht in der Spalte. Hat Duc einen Zettel, der eine **wahre** Zeile bestätigt, steht dort *„✓ Fits your note“*. Bei der **falschen** Zeile stellt sich Duc eine **Frage im Kopf** (z. B. *„Didn't somebody see her leave the mess?“* – nie mit dem Namen der Notiz; ohne Falldaten *„Something about that doesn't sit right.“*), und der Stapel mit dem Gegenbeweis leuchtet. | nichts, beliebig oft |
| **Zettel in eine Spalte legen + OBJECTION!** | Richtig, wenn die Zeile die falsche ist **und** der Zettel zum Beweissatz des Punkts gehört **und** die Behauptung dieser Zeile berührt **und** Duc den Rest der dazugehörigen Beweiskette kennt. Dann: *OBJECTION!*, ein Satz aus dem Saal, Megan erklärt den Punkt für bewiesen. | – |
| … Zettel gehört dazu, aber ein Teil der Kette fehlt | Megan: *„That's a start – what else backs it up?“* | nichts |
| … wahre Zeile angegriffen | Die Spalte leuchtet rot, Megan: die Zeile stimmt. | **−1 Ader** |
| … Zettel trifft die falsche Zeile nicht | Die Spalte leuchtet rot, Megan nennt den **Grund** (siehe unten). | **−1 Ader** |
| **No proof? → Bluff** | Charme oder List (der bessere Wert) gegen **14**. Gelingt: der Punkt zählt – aber Erbarmen im Urteil braucht echte Beweise. Misslingt: Punkt verloren. | Fehlschlag **−2 Adern** |
| **No proof? → Give up** | Der Punkt bleibt offen und zählt gegen Duc. | – |
| **Joker** (grüner Zettel) | Gegenstände mit Joker-Wirkung beruhigen Megan. | **+1 Ader** |

**Nachbessern – zwei Aussagen je Punkt** (seit 26.10., wie *Ace Attorney*): Hat ein Fall eine nachgebesserte Aussage,
beweist der erste Treffer den Punkt noch nicht. Nach *OBJECTION!* rudert der Zeuge vertont zurück (*„Fine. I wasn't in
the mess the whole time …“*), Titelkarte *„Revised testimony“*, dann eine neue Aussage mit drei Zeilen und einer neuen
Lüge. In *What?* und *Why?* bessert die **Werft** nach (Megan liest ihre korrigierte Fassung und stichelt: *„Revised.
Funny how that works.“*, 3 Varianten), in *Who?* die Angeklagte selbst. Erst der zweite Treffer beweist den Punkt. Die beiden Lügen werden von **verschiedenen** Notizen widerlegt.
Wer in der nachgebesserten Aussage aufgibt oder blufft und scheitert, bekommt den Punkt **halb** (zählt wie ein Bluff:
belegt, aber kein Erbarmen) – die erste Lüge war ja schon entlarvt. Jeder Fall (1–5) hat für alle drei Punkte eine
Nachbesserung; der Bot findet alle sechs Beweise mit dem Wissen, das man in den Story-Szenen bekommt.

**Schreibregeln für Aussagen** (27.10.): klare Sprache, aber die Lüge nicht verschenken und nichts Kryptisches. Die
falsche Zeile klingt so selbstverständlich wie die wahren; Ducs Gedanke ist eine offene Frage, die die Richtung zeigt
(*„Plus one point eight – compared to what, exactly?“*), nie den Namen der Notiz. Eine wahre Zeile stützt sich nie auf
genau die Notiz, die die Lüge widerlegt – sonst verrät *„Fits your note“* den Gegenbeweis. Uhrzeiten aus der
Energiesteuerung bleiben in ihrer eigenen (falschen) Zeit, damit der Uhrenabgleich zählt.

**Welche Notiz zählt gegen eine falsche Zeile** (Duc 28.10.2026, Gegenrede Luise): nicht nur die eine, für die die Zeile
geschrieben wurde. Jede Notiz zählt, die zum Beweissatz des Punkts gehört **und** die Behauptung der Zeile berührt.
Bei Zeilen mit zwei Behauptungen („I stayed in the mess … I never went near the bridge.“) trifft also auch eine Notiz,
die nur die zweite Hälfte widerlegt. Die Falldaten führen dafür je falscher Zeile `widerlegt` (wofür die Zeile
geschrieben ist) und `beruehrt` (weitere Notizen des Punkts, die dieselbe Behauptung treffen). Alle 30 falschen Zeilen
der fünf Fälle sind so geprüft: 41 zusätzliche Notizen zählen jetzt.

**Ablehnung mit Grund** statt Pauschale. Trifft ein Zettel nicht, sagt Megan in dieser Reihenfolge, warum:
1. **eigener Satz** für naheliegende Fehlgriffe (Feld `warum_nicht` in den Falldaten, 25 Stück, vertont), z. B.
   *„Card two hangs on a hook. Your note doesn't say whose hand took it.“*
2. **anderer Punkt:** *„That note belongs to another point, First Officer. Not this one.“*
3. **nur eine Aussage:** *„That's what someone says. It doesn't touch this line.“*
4. **richtiger Punkt, falsche Behauptung:** *„Right point. But that's not what this line claims.“*
5. sonst wie bisher (*„That note is about something else entirely …“*).
Je Kategorie 2 Varianten, alles vertont. Kosten bleiben −1 Ader.
Doppelzeilen in zwei Zeilen zu teilen (Plan 2b) ist bewusst **noch nicht** gemacht – erst nach der Messung und nur,
wo es dann noch stört.

**Wer die falsche Person anklagt:** Unschuldige sagen in Punkt 2 nur Wahres. Ein gültiger Beweis zeigt dann *„That points
somewhere else“* – der Punkt ist verloren, kostet aber keine Ader.

## Garantierte Kernbeweise und Fall-Tafel (Duc 28.10.2026)

Vorher kam fast jede Notiz nur über freiwillige Aktionen. Nach einer normalen Woche fehlte dem Bot oft jede
Schiffssystem-Notiz, und Punkt 1 ging nur per Bluff.

- **What** und **Why** bekommt jeder Fall garantiert. Je Punkt ist ein Beweissatz als **Kern** markiert, der kleinste,
  bei Gleichstand der, der zur Quelle passt. Seine Notizen haben einen eigenen Weg `pflicht`:
  - What: Tag 4, *„Rosi vs. Officer“* (`reparaturschritt`). Die Notiz erscheint als *„📌 On Rosi's whiteboard in
    the propulsion room: …“*.
  - Why: Tag 5, *„A Visit from Head Office“* (`megan_kommt`). Sie erscheint als *„📌 In the folder Megan brought
    from head office: …“*.
  - Wird die Szene verpasst, kommt die Notiz am nächsten Tag nach.
  - Ist der Punkt schon belegt, kommt nichts.
  - Gegenhandlungen sperren diese Wege nicht.
- **Who** bleibt Ermittlung. Ein garantierter Who-Beweis würde den Täter ohne Ermittlung verraten.
- Gebaut in `werkzeuge/eden_rise/story_eden_rise.py` (`kern_vergeben`, `PFLICHT`), geliefert von
  `kern/ermittlung.py` (`pflicht_beweise`).

**Fall-Tafel** im Codex (Reiter *Investigation*, Abschnitt *The case*): Jede Frage zeigt *Open*, *Partly · x of y*
oder *Proven*. Bei offenen Fragen steht nur die **Art** dessen, was fehlt, nie Namen, Orte oder Uhrzeiten:

| fehlt | nichts gefunden | ein Teil fehlt noch |
|---|---|---|
| Bordsysteme | *Nothing on the ship's systems yet.* | *One more piece from the ship's systems.* |
| Papiere | *Nothing on paper yet – a log or a file.* | *One more piece on paper – a log or a file.* |
| Personen | *Somebody saw something. You haven't heard it yet.* | *Someone still has to tell you a piece of it.* |
| eigene Funde | *You still have to put two things together yourself.* | *One more thing to put together yourself.* |

Grundlage ist der Beweissatz, der am nächsten an „komplett“ ist; es werden höchstens zwei Arten genannt.
Springt eine Frage auf *Proven*, steht einmal *„✔ The case: … – proven.“* im Log. Beim ersten Anblick im Codex
leuchtet die Frage kurz auf, dazu der Ton `auftrag_siegel`. Der Browser merkt sich das je Spielstand.
Derselbe Satz steht in der Anhörung als Ducs Gedanke unter jeder Punkt-Titelkarte (*„💭 1 of 2 pieces. One more
piece on paper …“* bzw. *„Your notes cover this point.“*).

**Messung** (`werkzeuge/eden_rise/anhoerung_messung.py`, Bot-Woche je Fall, Seeds 7 und 3): siehe unten unter
*Grenzen und Stand*.

## Megans Geduld (Adern ●)

- Start **3 Adern**; **+1**, wenn Duc an Tag 0 herzlich war, **−1**, wenn er frech war.
- **−1**, wenn Megan Duc in der Woche wenig zutraut (Haltung unter 0), **−1** bei offenen, unbelegten öffentlichen
  Vorwürfen gegen andere.
- Bei **0 Adern** bricht Megan ab (*„Enough.“*), alle offenen Punkte sind verloren.

## Die Notizen auf dem Tisch

- Jeder Fund der Woche liegt als **Notizzettel** in Handschrift auf dem Schreibtisch, mit einem Satz in Klartext; der
  Original-Eintrag (Logbuch, Protokoll …) steht klein darunter.
- **Vier Stapel:** *People* (mit dem Gesicht der Person, die es erzählt hat), *Ship systems*, *Papers & logs*, *Your own
  findings*. Die zuverlässigsten Zettel liegen oben: *secured* > *solid* > *seen* > *word only*.
- **Pro Punkt nur die Zettel zum Thema** – die richtigen und die irreführenden. *„show all notes“* hebt den Filter auf.
- **8 Symbole** für Quellen ohne Gesicht: Monitoring, Office PC, Camera, Navigation, Logbook, Files, Phone, You (eigene
  Ermittlung). Die Hilfe (**?** oben rechts) erklärt alles; sie öffnet sich **nicht** mehr von selbst.
- **Geführte erste Zeile** (Duc 29.10.2026, statt der Regel-Textwand beim Start): Nur in der allerersten Anhörung
  (der Browser merkt sich das, danach nie wieder) führt ein Hinweis in Punkt 1 durch eine Zeile – die falsche der ersten
  Aussage. Er steht direkt in der Spalte, die Spalte leuchtet golden:
  1. *„Try it: Ask line 2. Something about it doesn't sit right – press the witness on it.“*
  2. nach dem Nachhaken: *„Place a note here. The glowing stack below holds a note that contradicts this line …“*
  3. liegt ein Zettel: *„Now: OBJECT! If the note really contradicts the line, the point is yours.“*
  Sobald ein Zettel vorgelegt wurde oder Punkt 1 vorbei ist, ist die Führung erledigt. Die nachgebesserte Aussage und
  die Punkte 2–3 spielt man allein. Engine: `verhandlung_ansicht` liefert `fuehrung` (Index der falschen Zeile, nur
  Punkt 1, erste Aussage); Client `eden-hearing.js` (`fuehrungHtml`, Schlüssel `eden.hearing.gefuehrt`).

## Ergebnis

Die Anhörung gilt als **belegt**, wenn alle drei Punkte bewiesen, gestanden oder geblufft sind. Daraus und aus Ducs Rolle
und Plädoyer entsteht das Urteil – siehe **Ausgänge der Anhörung** oben.

## Stimme und Takt

- **Musik mit Bogen:** Aussagen mit ruhigem Ermittler-Track (*mysterium*), ab *„Revised testimony“* ein Druck-Track
  (*kampf_gefaehrlich*), beim Geständnis (ab Megans *„Why?“* bis zur Titelkarte *„The Verdict“*) leises trauriges Piano/Lo-Fi
  (*anhoerung_gestaendnis*, 3 Titel, blendet zur Rolle aus), **Stille** bei Rolle und Plädoyer, nach dem Urteil warm (*event_wholesome* bei
  Erbarmen/Entlastet) oder ernst (*event_ernst*). Zuordnung in `kern/musik.py`.
- **Wucht:** Beim *OBJECTION!* fliegt die gelegte Notiz ins Bild und der Bildschirm ruckt; bei jedem Fehlgriff platzt
  sichtbar eine Ader (rot, mit Klang).
- **Eigene Töne** (`sfx.json`, Gruppe Anhörung): *anhoerung_slam* (Zettel knallt auf den Tisch) und gleich danach
  *anhoerung_einspruch* (Stinger) beim *OBJECTION!*; *anhoerung_hammer* beim Urteil, knapp eine Sekunde später der
  Ausgangs-Klang (Erfolg bei Erbarmen/Aufgeklärt/Entlastet, sonst Fehlschlag). Je 4 Varianten, Wahl offen.
- **Bilanzkarte am Ende:** Punkte (✓ / ≈ / ✕), Megans Geduld, *Notes found X of Y*, Urteil – und *„A different verdict
  was possible.“*, wenn es nicht Erbarmen oder Entlastet wurde.

- **Alles ist vertont** (Megan, die Aussagen, Plädoyers, Reaktionen, Nervosität, Konter, Zusammenbruch, Zeugen, Kettenbrett, Stimmen aus dem Saal, Tratsch, Geständnis, Urteil; derzeit 346 Sätze) und läuft
  automatisch. Die Spalte der gerade vorgelesenen Zeile leuchtet.
- Momente wie Titelkarten und Punkt-Abschluss warten auf einen Klick (*Continue*, Enter oder Leertaste); *Skip* springt
  über alles.
- Tut Duc **45 Sekunden** nichts, wird Megan ungeduldig (höchstens dreimal pro Punkt).
- Duc selbst hat keine Stimme – *OBJECTION!* ist Schriftzug und Klang.

## Grenzen und Stand

- **Messung Kernbeweise** (28.10.2026, `werkzeuge/eden_rise/anhoerung_messung.py`, Bot-Woche bis zur Anhörung, Fälle 1–5 ×
  Seeds 7 und 3): vorher **What 0/10, Who 0/10, Why 0/10** belegt (10–13 Notizen). Nachher **What 10/10, Why 10/10, Who
  4/10** (13–16 Notizen). Who kommt dabei nicht geschenkt: Der Bot erreicht in vier Läufen ein Geständnis, das das Glied
  ersetzt. Die Doppelzeilen (Plan 2b) bleiben vorerst ungeteilt.

- **Fälle 1–5** haben eigene Aussagen mit Nachbesserung, Klartexte, Plädoyer der Verantwortlichen, Tratsch und
  Geständnis (seit 27.10.; ein Fall je Verdächtiger). Fall 6 (*niemand allein*) ist seit 27.10. gestrichen: Es gibt nur
  noch die Fälle 1–5, jeder mit einer Verantwortlichen. *Nobody alone* bleibt als falsche Wahl (Urteil *offen*). Der Test `tests/test_verhandlung.py` spielt jeden Fall mit allen Gegenbeweisen durch.
- Das Thema je Zettel kommt bisher aus einer Faustregel nach Fakt-Art; ein eigenes Themenfeld in den Falldaten folgt.
- Testen: Vorschau auf Port 8331 (`--anhoerung --realistisch --fall 1`), Knopf *„Restart hearing (test)“*.

- **Duc im Bild (29.10.2026):** Duc erscheint mit seinem Bild von vorne aus dem Character-Menü (charakter/Duc<Look><Klasse>.webp,
  Look = angelegte Jacke, Klasse = gehaltene Waffe, Schrubber nur zu Terra Scura). Server-Helfer den.duc_bild(z) /
  kampf.duc_portrait, Ansicht erhandlung.duc_sprite, jeder Log-Eintrag wer=duc trägt das Bild. Zu sehen: rund
  über den Plädoyer-Karten, groß unten links beim OBJECTION! und als kleiner Kreis im Verlauf.

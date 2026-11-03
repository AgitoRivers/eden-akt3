# Outfit-Quest, Pilot: Sophias Lesung

> Von Duc freigegeben und gebaut, 31.10.2026 (`ereignisse_outfit_quest.py`), noch nicht vertont. Beschluss siehe E-104. Maßgeblich ist der Text im Code. Abweichungen beim Bau: Sophias Tipp steht als Erinnerung im Poker-Text statt als eigene Handy-Nachricht. Danzel und Totò sprechen in einer Szene an der Piazza. Sophia zeigt in den Mantel-Szenen nur Gefühle, deren Posen stehen. **Die Lesung selbst wurde danach ausgebaut (Duc: zu schnell vorbei):** schwacher Anfang mit Stille (`ol_stille`, Duc hilft auf eine von drei Arten), der Raum kippt mit echten Stellen aus dem Krimi (`ol_kipp`, Totò nimmt Wetten an), stiller Moment mit dem Anfang des Satzes aus ihrem Stück (`ol_reaktion`). Abschnitt 4 unten zeigt noch die erste, kurze Fassung.

**Kern:** Sophia stand zwei Jahre in den Kulissen und ist nie aufgetreten. Jetzt tritt sie zum ersten Mal auf, und das Publikum hört, was fünfzehn Verlage abgelehnt haben. Der Trenchcoat ist kein Kleid für Duc, sondern der Mantel ihrer erfundenen Autorin.

**Dauer:** etwa 15 Minuten. Zwei Phasen kosten Zeit (Poker, Lesung), der Rest fällt an Orte, an denen Duc ohnehin ist.

**Voraussetzungen:** *Fourteen* gesehen (`rm_s3`), Danzels Laden offen. Ohne Laden gibt es die Quest nicht.

| Schritt | Szene | Ort | Mechanik |
|---|---|---|---|
| 1 Wunsch | The Slow Night | Alvas Bar | Sie fragt dich, ob sie es tun soll |
| 2 Material | A Coat at Cards | Danzel, Totò, Poker mit Yamamoto | Der alte Mantel als einziges Material, Lesen statt Glück |
| 3 Anprobe | The Label | Le Théâtre Rouge | **Eine** Wahl: Welcher Name steht im Kragen? |
| 4 Anlass | You're On | Alvas Bar | Ruf bestimmt, wie voll es ist, durchfallen kann man nicht |
| 5 Echo | Ten Euros | Frühstück | Die Wette wird aufgelöst, das Dorf redet |

## 1 · The Slow Night

**Wann:** 2 Tage nach *Fourteen*, Laden offen · **Ort:** Alvas Bar, Nachmittag · **Set:** Concierge

*A slow afternoon at Alva's bar. Sophia sits at the end of the counter with her little brown notebook. Alva is drying a glass and looking at all the empty chairs.*

**Alva** *(annoyance)*: My quiet nights are killing me, Sophia. You did theatre in London, didn't you? Come and read something out loud, a story, anything, and I'll sell wine to the people who come to listen.

**Sophia** *(amusement)*: Alva, darling, I stood at the side of a stage for two years and I never once went on. It's the thing I'm best at.

*Alva laughs and goes down to the cellar. Sophia doesn't laugh. She closes the notebook and speaks more quietly.*

**Sophia** *(nervousness)*: You've seen the letters, Duc. Fifteen publishers have said no to M. J. Penrose, and that's me, as you know. But not one of them has ever heard the book out loud.

**Sophia** *(neutral)*: Ten euros says I'd be sick before the first page. So tell me, and please don't be kind. Should I do it?

| Du | Sophia | Folge |
|---|---|---|
| Puts ten euros on the counter. “I'll take that bet. Three days from now.” | “You put money on the bar. Oh, that's low. You know I can't walk away from a bet.” | Merker `lesung_wette` |
| “Would you read the vicar? The one who'd been dead since Tuesday?” | *She laughs before she can stop it.* “You remember the marmalade. Yes, I suppose I'd have to read the vicar.” | Vertrauen + |
| “It's your secret. What do you want, Sophia?” | “There you go, asking. Nobody ever does.” *She turns the notebook over, twice.* “I want to go on, Duc. Only once, just so I know.” | Begehren + |

**Sophia** *(curiosity)*: But I can't go up there in this uniform, because they'd all ask me for a table. M. J. Penrose has a coat. I've had it in my head for three books, a camel coat from the thirties with a belt. Ask your friend Danzel if such a thing still exists.

## 2 · A Coat at Cards

**Danzels Laden** · *Keine Phase.*

**Danzel** *(neutral)*: A camel coat from the thirties, with real wool. No, nobody makes that cloth any more, and what they sell now would be an insult to her. I would need an old one to take apart, very slowly.

**Danzel** *(curiosity)*: There's only one on this coast that I know of. Totò had it in his locker, and he wanted a price that made me feel unwell.

**Totò** · *Keine Phase.*

**Totò** *(remorse)*: Comandante, that coat! It was an English gentleman's, and nine years I kept it safe. Last night I put it on the table, and I lost it to Yamamoto-san. Two to one on me, I gave myself, and I'm still upset.

**Totò** *(curiosity)*: If you're going to play him, ask Sophia first. She's the only one who beats him.

**Handy, von Sophia** (zählt nicht zum Limit)

- he says sorry when his cards are good
- thirty years in a bank, poor man
- don't you dare tell him

**Poker** · **Ort:** Crew Mess, Abend, kostet die Phase · **Set:** Yamamoto wie gewohnt

*Yamamoto is sitting alone with a pack of cards and the coat folded on the chair beside him. He stands up and bows to you, and then, you are nearly sure, to the coat.*

**Yamamoto** *(neutral)*: Officer-san. Very honoured. Three hands, please. If you win two, you take the coat with my respect.

Drei Hände. Auf dem Bildschirm steht vor jeder Wahl noch einmal Sophias Nachricht. Die Chips heißen immer **Puts in more money.** und **Gives up the hand.**

| Hand | Yamamoto sagt | Richtig |
|---|---|---|
| 1 | “So sorry. I am very tired tonight.” | aufgeben |
| 2 | “Very interesting. Your turn, please.” | mehr setzen |
| 3 | Er schweigt und lächelt: “Sophia-san also watches my mouth. Tonight I will say nothing.” Mit hoher Wahrnehmung: *His thumb has gone to his watch. It did that on the first hand too.* | aufgeben |

| Ausgang | Yamamoto | Folge |
|---|---|---|
| Zwei gewonnen | “Very interesting. So sorry. …Please tell Sophia-san she owes me a new way to lose.” | Mantel gratis, Ruf + |
| Verloren | “The coat is heavy, Officer-san, and I carry my own luggage. Forty euros, for Totò's feelings.” | Mantel für 40 € |

Der Mantel geht als `alter_mantel` an Danzel, das Bringen kostet keine Phase. Dazu kommt ein Preis von etwa 60 €, Zahl beim Einbau per Sim.

## 3 · The Label

**Wann:** Tag nach dem Bringen, beim Besuch im Laden · **Ort:** Le Théâtre Rouge · **Set:** zum ersten Mal **Sophia Reading**

*Sophia stands on a low box in the camel coat. The belt is tied and the hat is tilted, and a pencil sits behind her ear. Danzel is kneeling at the hem. For once, he isn't performing.*

**Danzel** *(caring)*: Stand still, please. This cloth is eighty years old and it is better than anything I will ever make, so I took it apart slowly and I built it again around you. The left shoulder is new. I don't think you can tell.

*Her long hair has gone. You look again, and it's a short, glossy wave, pinned flat on one side.*

**Sophia** *(amusement)*: Don't stare, darling, it's all still there under the pins. In London I learned to make long hair look short in ninety seconds in the dark, in case somebody fell ill before the second act. Nobody ever did.

**Danzel** *(neutral)*: Everything I make has a small label inside the collar, with one name on it. I always leave that until last. What do I stitch?

**Sophia** *(nervousness)*: He's asking you as well, Duc, and you've read the letters. Which name should go in the coat?

| Du | Sophia | Folge |
|---|---|---|
| “M. J. Penrose. She wrote the book, so let her wear the coat.” | “Yes. She's braver than I am, and she has nothing to lose. Stitch it, Danzel.” | `lesung_name = penrose` |
| “Sophia Moore. That's the name you want on a book cover, isn't it?” | “You don't make things easy, do you? …Stitch it before I change my mind.” | `lesung_name = moore` |
| “Leave it empty. You'll know when you're standing up there.” | “That is the worst thing anyone has ever said to an actress. …Leave it empty, Danzel.” | `lesung_name = leer` |

Danach gilt die Frage aus Maelles Baustein 4 hier nicht: Der Mantel bleibt ihr Anlass-Outfit und ersetzt nicht die Concierge-Uniform.

## 4 · You're On

**Wann:** drei Tage nach Szene 1 oder am nächsten Abend nach der Anprobe, je nachdem, was später ist · **Ort:** Alvas Bar, Abend, kostet die Phase · **Set:** Sophia Reading

*The storeroom behind Alva's bar smells of diesel and old lemons. Through the door you can hear chairs and glasses and people talking. Sophia is standing very straight, holding three pages, and the pages are shaking.*

**Nach Ruf, gesprochen von Alva durch die Tür:**

- **Niedrig:** “Six people, Sophia, and one of them is the priest, so I'm counting him twice.”
- **Mittel:** “Every chair is gone, and I've given Totò a crate.”
- **Hoch:** “I've got people standing on the piazza, and they're asking me to open the windows.”

**Sophia** *(fear)*: Two years, Duc. Every single night there was a young man with a clipboard who came along the corridor to say it to the others, and he walked straight past me.

**Sophia** *(nervousness)*: I'd like somebody to say it to me, just once. Would you mind?

| Du | Sophia | Folge |
|---|---|---|
| Opens the door. “You're on, Miss Penrose.” *(nur bei `penrose`)* | *She takes one breath, and the pages stop shaking. She walks past you, and she doesn't look back.* | |
| Opens the door. “You're on, Miss Moore.” *(nur bei `moore`)* | wie oben | |
| Opens the door. “You're on.” *(nur bei `leer`)* | wie oben | |

**Bei `penrose`** · **Sophia** *(amusement)*: Good evening. My name is M. J. Penrose. I don't exist, so please don't ask for your money back.

**Bei `moore`** · **Sophia** *(neutral)*: Good evening. You all know me, because I've got you your tables and lied to you about the weather. My name is Sophia Moore, and I've been writing at night for years. I'd like to read you something.

**Bei `leer`** · *She stands there. She takes the pencil from behind her ear and looks at it. Nobody in the room has ever seen her without a line ready.*

**Bei `leer`** · **Sophia** *(neutral)*: My name is… My name is Sophia Moore. M. J. Penrose sends her apologies.

**Sophia** *(amusement)*: “The vicar had been dead since Tuesday, which explained the marmalade.”

*There is one second of silence, and then Don Anghjulu laughs so hard that he has to put down his glass. After that, the whole room is hers. You have watched her work a room a hundred times, but she has never done it like this. She isn't asking anybody for anything.*

*She reads for twenty minutes. Then she stops at the end of the chapter and squares the pages on the counter.*

**Bà Tư** *(anger)*: No. You can't stop there. Who killed him? Sit down, eat something, and then read the next part.

**Don Anghjulu** *(amusement)*: God sees everything, but He hasn't told me about the vicar. I would also like to know.

*Sophia looks at you across the room. She has stopped acting, and you can tell the difference now.*

**Sophia** *(joy)*: Did you hear that? She wants to know what happens next. Fifteen letters, and not one of them ever wanted to know that.

**Hat Duc ihren Füller schon** (Unikat über Leas Mission) · *Bà Tư pushes a receipt across the counter. Sophia takes out the pen with her own name on it and signs the back.*

**Danach kurz am Tresen:**

**Chiara** *(surprise)*: Eight and a half. No, nine. You've lived next to me for four seasons, and you wrote three books? I want every one of them, and I'm going to be so loud about this.

**Lea** *(love)*: You always had ink on your chin in the mornings. I thought it was from doing the bills. Did you know that a vicar – no, sorry. I'm just proper proud of you, that's all.

**Folge:** Ruf +2, Vertrauen Sophia +1, ohne eigenen Stufensprung. An Bord wissen es jetzt alle, also Fakt aus *Fourteen* ersetzen. Legenden-Zeilen fürs Dorf (siehe unten).

## 5 · Ten Euros

**Wann:** nächstes Frühstück, Pflicht-Echo wie bei der Romanzen-Leiter

**Mit Wette** · **Sophia** *(amusement)*: You'll want your ten euros, from when you bet me at Alva's that I'd go through with it. But I was sick in Alva's storeroom about a minute before you got there, darling, so strictly speaking I won.

**Ohne Wette** · **Sophia** *(amusement)*: I was sick in Alva's storeroom before the reading, you know, about a minute before you got there. I thought somebody ought to have it in writing.

**Beide** · **Sophia** *(caring)*: I never did find out what it's like to go on in that play. I'll tell you what, though, I find I don't mind at all.

### Das Dorf redet (Legenden-Familie)

- **Totò:** “Comandante, I'm telling everyone that coat was mine. Nobody has to know about the cards.”
- **Mina:** “There's a letter for M. J. Penrose at the post office again. I've been wondering who that was for years, you know. I've only been wondering, of course.”
- **Alva:** “Best quiet night I ever had. Tell her that she drinks free, once.”

## Offene Punkte, mit Vorschlag

| Punkt | Vorschlag |
|---|---|
| Darf der Mantel wiederkommen? | Ja, in späteren Sophia-Abenden an Alvas Bar als Set, keine neue Mechanik |
| Hoher Ruf als einziger Wirkpunkt? | Reicht für den Piloten. Ob Alva dafür dauerhaft etwas gibt, erst nach dem Probespiel |
| Spielerin ohne *Fourteen* (zu wenig Begehren) | Sieht die Quest nicht. Das folgt aus Baustein 3 und gilt für alle |
| Neu im Kanon, von Duc zu bestätigen | Der alte Kamelhaarmantel, Totòs verlorene Pokerrunde, Sophias Haartrick aus London, Alvas „quiet nights“, der Mann mit dem Klemmbrett |

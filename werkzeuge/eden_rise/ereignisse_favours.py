# -*- coding: utf-8 -*-
r"""Favours (Duc 29.10.2026, Brain Trust Option C): ersetzen die Schnelljob-Liste. Eine Figur bittet per Handy um einen
Gefallen, drei Bitten bilden eine Kette mit einem kleinen Bogen, am Ende schickt sie ein Dank-Foto.

  Bitte:  2 Wege mit Probe (je 1 Energie) + Ablehnen (art "auflegen", kostenlos, beendet die Kette)
          Erfolg -> Vertrauen +8 (Finale +10; bis 29.10.2026 +5/+6), Flags fv_<kette>_<n> (datiert) und fv_<kette>_<n>_ok
          Fehlschlag -> Vertrauen +1, Flag fv_<kette>_<n> (datiert) - die Kette geht weiter, nur ohne Foto am Ende
  Weiter: Teil n+1 fruehestens am Tag nach Teil n (flag_seit), der Dank nur nach geglücktem Finale (fv_<kette>_3_ok)
  Engine: kern/ereignisse.py _favour_ziehen (hoechstens eine Bitte am Tag), Journal-Rubrik "Favours" (eden-menu.js)
  Fotos:  werkzeuge\favour_fotos.py -> module\eden_rise\favours\fv_<kette>.webp (Prompts unten in FOTOS)

Zeilen stehen hier MIT Turbo-Tag (gesprochene Fassung); das Spiel zeigt sie ohne Tag. tags_schreiben() traegt die
gesprochene Fassung in module\eden_rise\stimme_tags.json ein (Quelle "favours", wird bei jedem Bau ersetzt).
Duc will die Inhalte nicht vorab kennen (Ueberraschung) - keine Abnahmeseite, die Fotos prueft die Hauptsitzung.
"""
import json
import os
import re

from ereignisse_basis import *  # noqa: F401,F403

TAG = re.compile(r"\s*\[(chuckle|clear throat|cough|gasp|laugh|shush|sigh|sniff)\]\s*")
AKT1, AKT2 = (2, 6), (8, 20)                # Tag 7 = Anhoerung, Tag 21 = Belagerung


def klar(t):
    return TAG.sub(" ", t).strip()


# kette: titel, wer, akt (1 = ab Tag 2, 2 = erst ab Tag 8), art (nachricht/video), ort (Hintergrund im Handy),
# phasen, start (Bedingung fuer Teil 1), teile [3], dank, foto
# teil: titel, ton, lage, zeilen [(text, gefuehl)], wege [(chip, probe, (ok, gef), (daneben, gef), extra_lohn)],
#       ab (chip, (zeile, gef))
# Zeilen-Tupel duerfen als drittes Element einen anderen Sprecher tragen (Nonnas Dank tippt Isabelle).
# flasche=True (Ligeia, Duc 30.10.2026): kein Handy, die Bitte kommt als Flaschenpost (Event art "abend" auf der Badeplattform),
# der Dank ist ein Polaroid; sie zaehlt trotzdem als Favour im Journal.
KETTEN = {
    "sirene": dict(
        titel="Message in a Bottle", akt=2, art="nachricht", ort="swim_platform", phasen=["tag", "abend"], flasche=True,
        start={"flag": "ligeia_polaroid"},
        teile=[
            dict(titel="It Eats Squares", ton="witzig",
                 lage="A green bottle knocks against the swim platform. Inside is a strip of wet paper in a slanting old "
                      "hand. You read it, and somehow you hear it.",
                 zeilen=[("[sigh] Sailor. The girl's box has stopped giving pictures. It clicks and gives me nothing, and "
                          "I've shaken it, and I've asked it nicely.", "annoyance"),
                         ("[chuckle] I'd ask her, but she says nobody is to know about me, and I've been very good about "
                          "it. Bring what it eats. Leave it on the third step at dusk.", "amusement")],
                 wege=[("Asks Lea for a spare film pack without saying why. “It's for a friend.”", P("charm", 11),
                        ("[gasp] It eats squares! It gave me the moon, sailor, and the moon looks like a thumbprint. Bring "
                         "more whenever you like.", "joy"),
                        ("[sigh] You've brought me squares for some other box. They don't fit. I gave them to the crabs.",
                         "disappointment"), []),
                       ("Buys film in the village and seals it in a jar with candle wax. “Waterproof enough.”",
                        P("cunning", 12),
                        ("[chuckle] Wax and a jar. That's how my sailors kept their tobacco dry. It works, and it smells "
                         "of the church.", "amusement"),
                        ("[cough] The jar leaked, sailor. Now I have a box of wet squares and one very clean crab.",
                         "annoyance"), [])],
                 ab=("Leaves the bottle where it is. “Not my problem.”",
                     ("[sigh] Then I'll go on shaking it. I have plenty of time, you know.", "disappointment"))),
            dict(titel="The Old Net", ton="wholesome",
                 lage="Another bottle, this one smelling of diesel. The paper has been folded very small.",
                 zeilen=[("[sigh] There's a net on the old mooring past the point. Nobody fishes it, sailor. It just goes "
                          "on catching, and it has had three turtles from me this week.", "sadness"),
                         ("[sniff] I can't cut it. Your steel doesn't like me, and I don't like your steel. You could do "
                          "it, in daylight, while I'm away.", "nervousness")],
                 wege=[("Dives on it with a knife at slack water. “Twenty seconds, tops.”", P("courage", 12),
                        ("[laugh] The turtles came back this morning, and they were very rude about it. I've taken their "
                         "picture.", "joy"),
                        ("[sigh] You cut half of it, and half a net still drowns things. But you went down, sailor. I saw "
                         "you.", "caring"), []),
                       ("Tells Petru where it is and lets him think it was his idea. “Someone ought to.”",
                        P("cunning", 12),
                        ("[chuckle] The old man came out in his boat and swore at it for an hour. It was a lovely sound, "
                         "and the net is gone.", "amusement"),
                        ("[sigh] He says that net was his grandfather's and it can stay where it is. Men and their nets.",
                         "annoyance"), [])],
                 ab=("Puts the bottle in the recycling. “Tell a fisherman.”",
                     ("[sigh] I did tell one, sailor. Some time ago. He's still asleep.", "sadness"))),
            dict(titel="What Rings the Bell", ton="wholesome",
                 lage="The third bottle has the camera's strap tied round its neck, and a very small square of film.",
                 zeilen=[("[clear throat] I've listened to your village bell for longer than I'd like to say, and I've "
                          "never seen what's ringing it. The hill is a long way up for me.", "nervousness"),
                         ("[sigh] Would you take a picture of it? From the top, with the sea behind. I'd like to know how "
                          "it looks from up there, looking down at me.", "sadness")],
                 wege=[("Climbs the bell tower at dawn with the square in his pocket. “Hold still, bell.”",
                        P("courage", 13),
                        ("[sigh] So that's it. It's so small, sailor. All those years, and it's no bigger than a boy.",
                         "admiration"),
                        ("[chuckle] You sent me your thumb. It's a very nice thumb, and behind it there's a bit of bell.",
                         "amusement"), []),
                       ("Asks Nonna Fiora for the key to the tower. “It's for someone who can't come up.”",
                        P("charm", 13),
                        ("[sniff] She held it up to the window for you, didn't she? I can see her thumb. Tell her it's a "
                         "good bell.", "gratitude"),
                        ("[sigh] She asked who it was for, and now she has lit a candle for me. No picture, though. How "
                         "very like her.", "disappointment"), [])],
                 ab=("Leaves the square on the rail for the gulls. “Some other time.”",
                     ("[sigh] Yes. There's always some other time. I'm the one who'd know.", "sadness"))),
        ],
        dank=dict(titel="For the Girl with the Box",
                  lage="One last bottle. Inside are two Polaroids, curled from the damp, each with a line in the same "
                       "slanting hand. You take them down to the pool at dusk.",
                  zeilen=[("[sigh] Now you've seen where I sleep, sailor, and that makes two of you. Show the girl. Tell "
                           "her six metres is very shallow.", "caring")],
                  antworten=[("Holds up the second one. “The same octopus?”",
                              ("[chuckle] A different one. The first one talks too much.", "amusement")),
                             ("Looks at the first one for a long time.",
                              ("[chuckle] Don't stare, sailor. It's only the light.", "caring"))]),
        foto=None),
    "lola": dict(
        titel="Mum's Bao Buns", akt=1, art="nachricht", ort="galley", phasen=["tag", "abend"],
        start={"bekannt": "lola"},
        teile=[
            dict(titel="No Steamer", ton="witzig",
                 lage="A message from Lola. Then three more, very fast.",
                 zeilen=[("[gasp] boss. BOSS. emergency but like a nice one 🥟", "excitement"),
                         ("[sigh] i'm making mum's bao buns for the crew tonight but there's no steamer on this whole "
                          "boat?? who runs a galley without a steamer, it's like a… you know what i mean 😭", "annoyance")],
                 wege=[("Calls Petru. “Do fishermen steam things?”", P("charm", 11),
                        ("[laugh] he had one!! it smells a bit like octopus but mate, it's PERFECT 🐙💛", "joy"),
                        ("[sigh] he said hm and hung up. is that a yes? i think that's a no 😩", "confusion"), []),
                       ("Builds one out of a pot, a sieve and a lot of foil. “Trust me.”", P("cunning", 12, "handwerk"),
                        ("[gasp] it's ugly and it WORKS. you're a genius boss, an ugly genius 😂🥟", "amusement"),
                        ("[cough] okay so the foil caught fire a tiny bit. small fire. it's out. mostly 🔥🙃",
                         "embarrassment"), [])],
                 ab=("“Not today, Lola. Use the microwave.”",
                     ("[sigh] the microwave. wow. mum would cry. okay okay, another time 🥲", "disappointment"))),
            dict(titel="Dough on Strike", ton="witzig",
                 lage="Lola again. This time there's a photo: a bowl of pale, flat dough under a tea towel.",
                 zeilen=[("[sigh] it won't rise 😤 it's been two hours. it's just lying there like me on a day off",
                          "annoyance"),
                         ("[sniff] mum's dough always rose. maybe it knows i'm not mum. can dough know that?? 🥺",
                          "sadness")],
                 wege=[("Takes the bowl down to the engine room. “It's the warmest place on board.”",
                        P("perception", 11),
                        ("[laugh] it's HUGE now. rosi says if it touches her generator she's throwing it in the sea 😂",
                         "amusement"),
                        ("[sigh] rosi kicked us out before it did anything. she said the engine room is not a bakery. "
                         "rude 😤", "annoyance"), []),
                       ("Calls her back. “Tell me how your mum does it. Step by step.”", P("empathy", 12),
                        ("[sniff] she always sang to it. i forgot that. i'm singing to it now and it's GROWING mate 🥹",
                         "love"),
                        ("[sigh] i talked about mum for twenty minutes and the dough did nothing. but i feel better? "
                         "weird 🥲", "relief"), [])],
                 ab=("“Buy bread, Lola.”", ("[sigh] wow. okay. bread. sure 🫠", "disappointment"))),
            dict(titel="The Taste Test", ton="witzig",
                 lage="A string of messages from Lola, all in capitals.",
                 zeilen=[("[gasp] CHIARA IS COMING INTO THE GALLEY 😱", "fear"),
                         ("[sigh] she said she'll taste one. like a judge. boss she does the face. you know the face. "
                          "i need backup NOW 🥟🚨", "nervousness")],
                 wege=[("Walks in and takes the first bun himself. “Chief, you have to try these.”", P("charm", 12),
                        ("[laugh] she had TWO. she said not bad. NOT BAD BOSS. that's like a medal from her 🏅😭",
                         "joy"),
                        ("[cough] you took the last good one and she got the burnt one 💀 she said interesting. "
                         "i'm going to live in the sea now", "embarrassment"), []),
                       ("Keeps Chiara busy with questions about the night watch until the buns are ready.",
                        P("cunning", 12),
                        ("[chuckle] you talked about ropes for ten minutes and she didn't notice a thing. buns were "
                         "PERFECT when she came in 🥟✨", "relief"),
                        ("[sigh] she saw right through you mate. she said nice try, First Officer, and stared at my "
                         "buns like a hawk 😬", "nervousness"), [])],
                 ab=("Doesn't answer. Lola has this.",
                     ("[sigh] ok. ok ok ok. i've got this. i've totally got this 😰", "nervousness"))),
        ],
        dank=dict(titel="Forty-Two", item="megan_crewkarte",      # die Crew-Karte (frueher Lohn der Schnelljob-Kette lola_megan)
                  lage="A photo from Lola. No words for once. Then the words come.",
                  zeilen=[("[laugh] the crew ate forty two buns 🥟🥟🥟 FORTY TWO", "joy"),
                          ("[chuckle] mum called. i told her about you. she says you're invited to brisbane. she means "
                           "it, she'll feed you till you burst 😂💛", "love")],
                  antworten=[("Writes back: “Save me one.”",
                              ("[laugh] already did. it's in the oregano jar. don't ask 🤫", "amusement")),
                             ("“Your mum would be proud.”",
                              ("[sniff] stop it. i'm in the walk-in fridge crying into the cabbages. thanks boss 🥹",
                               "love"))]),
    ),
    "alva": dict(
        titel="Alva's Saturday", akt=1, art="video", ort="alvas_bar", phasen=["tag", "abend"],
        start={"bekannt": "alva"},
        teile=[
            dict(titel="The Man with One Flip-Flop", ton="witzig",
                 lage="Alva calls. Behind her, the bar is loud.",
                 zeilen=[("[chuckle] There's an Englishman in my bar who says he owns three yachts. He's wearing one "
                          "flip-flop.", "amusement"),
                         ("[sigh] He won't leave, he won't pay, and he keeps calling me sweetheart. Come and get him "
                          "before I do something the village will talk about.", "annoyance")],
                 wege=[("Walks in like a harbour official. “Sir, your yacht is being towed.”", P("cunning", 12),
                        ("[laugh] He ran. One flip-flop and all. He even paid first, can you believe it? You have a "
                         "face people believe.", "amusement"),
                        ("[sigh] He asked which yacht. You didn't know. Now he's buying you a drink. Wonderful.",
                         "annoyance"), []),
                       ("Sits down next to him and listens to the whole story.", P("empathy", 11),
                        ("[chuckle] He cried, he paid, he hugged me. His wife left him in Calvi. Poor idiot. Thank you, "
                         "really.", "caring"),
                        ("[sigh] You've been listening for an hour, and now there are two of you at my bar. Two!",
                         "annoyance"), [])],
                 ab=("“Throw him out yourself, Alva.”",
                     ("[chuckle] Oh, I will. I just wanted it to be your story, not mine.", "amusement"))),
            dict(titel="A Dry Bar", ton="frech",
                 lage="Alva calls from the back of her bar, between empty crates.",
                 zeilen=[("[sigh] My wine man from Sartène has forgotten me. Again. A whole delivery, and it's "
                          "Saturday night tonight.", "annoyance"),
                         ("[chuckle] His cellar is in the next bay. You have a boat. I have a bar full of thirsty "
                          "people. You see where this is going.", "amusement")],
                 wege=[("Takes the tender round the point and fetches the crates himself.", P("strength", 12),
                        ("[laugh] Twelve crates, and not one bottle broken! You're hired. I'm joking. Mostly.", "joy"),
                        ("[cough] Two bottles made it. Two. The sea had a very good night, I think.", "amusement"),
                        [G(120)]),
                       ("Calls the wine man and talks to him nicely.", P("charm", 12),
                        ("[chuckle] He's on his way with the van, and he said sorry three times. What did you tell "
                         "him? No, don't tell me.", "amusement"),
                        ("[sigh] He hung up on you too? Then it's a beer night. The village will survive.",
                         "disappointment"), [])],
                 ab=("“I'm needed on board, Alva.”",
                     ("[chuckle] Of course you are. Go, go. I'll pour water and call it French.", "amusement"))),
            dict(titel="Karaoke Night", ton="witzig",
                 lage="Alva calls. She's smiling far too sweetly.",
                 zeilen=[("[chuckle] So. I promised the whole village a karaoke night, and the singer from "
                          "Porto-Vecchio cancelled an hour ago.", "amusement"),
                         ("[laugh] And who do I know who has a voice, a nice shirt and owes me a little? Don't make that "
                          "face. One song.", "desire")],
                 wege=[("Takes the microphone and sings like nobody is watching.", P("courage", 12),
                        ("[laugh] They want an encore! The old fishermen at the back cried! You're never paying for a "
                         "drink in this village again.", "joy"),
                        ("[laugh] You were terrible. Truly. But they loved it, and the bar is full, so who cares?",
                         "amusement"), [G(150)]),
                       ("Gets the whole bar singing instead of singing alone.", P("charm", 13),
                        ("[gasp] The whole piazza is singing! You made it their night, not yours. Clever. Very "
                         "clever.", "admiration"),
                        ("[sigh] Nobody joined in, so you sang alone after all. Bravely. Very bravely.", "amusement"),
                        [G(150)])],
                 ab=("“I don't sing, Alva.”",
                     ("[chuckle] Everybody sings in Corsica. You'll learn. Not tonight, then.", "amusement"))),
        ],
        dank=dict(titel="Closing Time",
                  lage="A photo from Alva: her bar after closing, a microphone on the counter, and Alva laughing at "
                       "whoever took it.",
                  zeilen=[("[laugh] best night this bar has had in years 🎤", "joy"),
                          ("[chuckle] alva remembers who helps her, o figliolu. your glass is always full here 🍷",
                           "caring")],
                  antworten=[("Writes back: “Next time, you sing.”",
                              ("[laugh] never. alva only sings when the bar is empty and the moon is drunk 🌙",
                               "amusement")),
                             ("“Thank you, Alva.”",
                              ("[chuckle] don't thank me. come and drink. that's how you thank a bar 😘", "desire"))]),
    ),
    "petru": dict(
        titel="Bastianu", akt=1, art="video", ort="petru_workshop", phasen=["tag"],
        start={"bekannt": "petru"},
        teile=[
            dict(titel="An Empty Tank", ton="witzig",
                 lage="Petru calls. For a while he says nothing. You can hear the football on his radio.",
                 zeilen=[("[clear throat] Bastianu is gone. The lid of his tank is on the floor, very neat. He took "
                          "his time.", "neutral"),
                         ("[sigh] He can't be far. An octopus doesn't like the sun. Come, if you have an hour.",
                          "caring")],
                 wege=[("Searches every cool, dark corner of the harbour.", P("perception", 12),
                        ("[chuckle] In Alva's ice box. With her lemons. She screamed, he didn't. Hm. Thank you.",
                         "amusement"),
                        ("[sigh] Nothing. He'll come back when he's hungry. Or he won't. The sea decides.", "sadness"),
                        []),
                       ("Puts a crab in a jar at the end of the quay and waits.", P("cunning", 11),
                        ("[chuckle] He opened the jar faster than I open a beer. Clever animal.", "amusement"),
                        ("[sigh] The crab is gone, the jar is closed again, and Bastianu is still out there. He's "
                         "laughing at us.", "annoyance"), [])],
                 ab=("“I can't, Petru. Not today.”",
                     ("[clear throat] Hm. Then I look alone. I always do.", "neutral"))),
            dict(titel="The Lid", ton="witzig",
                 lage="Petru calls from his workshop. Behind him, three tank lids lie in a row on the workbench, every "
                      "one of them open.",
                 zeilen=[("[sigh] He opens everything. Screws, clips, a stone on top. He took the stone off and put it "
                          "next to the tank, like a joke.", "annoyance"),
                         ("[clear throat] I need a lid he can't open. Or a reason for him to stay. Young people think "
                          "of strange things.", "neutral")],
                 wege=[("Builds a lid with a latch that needs two hands at once.", P("cunning", 12, "handwerk"),
                        ("[chuckle] He's been working on it for an hour. He looks offended. Good.", "amusement"),
                        ("[sigh] He opened it in four minutes. Then he closed it again, to show me.", "annoyance"),
                        []),
                       ("Gives him something to do: a jar with a shrimp inside, a new one every day.",
                        P("empathy", 12),
                        ("[chuckle] He's busy. He's happy. He hasn't looked at the lid all day. Like a man with a "
                         "newspaper.", "amusement"),
                        ("[sigh] He ate the shrimp and went for the lid anyway. He doesn't want a hobby. He wants out.",
                         "sadness"), [])],
                 ab=("“Maybe he wants to go home, Petru.”",
                     ("[sigh] Hm. Maybe. Maybe we all do.", "sadness"))),
            dict(titel="Out to the Rocks", ton="wholesome",
                 lage="Petru calls before sunrise. He's already in his boat; the tank sits beside him, wrapped in a "
                      "wet sack.",
                 zeilen=[("[clear throat] I'm taking him out to the rocks where I found him. Marie always said you "
                          "don't keep what wants to leave.", "sadness"),
                         ("[sigh] Come with me. I don't want to do it alone. That's all.", "caring")],
                 wege=[("Rows out with him and holds the tank steady over the side.", P("strength", 11),
                        ("[sniff] He went into the water. Then he came back up the oar and sat on my arm. Hm. He "
                         "chose. We go home.", "love"),
                        ("[sigh] The tank slipped, and he was gone before we could say anything. Maybe that's how it "
                         "should be.", "sadness"), []),
                       ("Sits with him in the boat and lets him talk about Marie.", P("empathy", 13),
                        ("[sniff] I talked too much. He listened, then he climbed back into the boat. Hm. He chose to "
                         "stay. Like you, maybe.", "love"),
                        ("[sigh] I said nothing in the end. He went into the sea and didn't look back. The sea doesn't "
                         "hurry, but it doesn't wait either.", "grief"), [])],
                 ab=("“I'm sorry, Petru. I can't come.”",
                     ("[clear throat] Hm. Then I go alone. It's fine. It's a small boat.", "sadness"))),
        ],
        dank=dict(titel="He Stays",
                  lage="A photo from Petru's number. It's a little crooked, and his thumb is in one corner. Then two "
                       "lines.",
                  zeilen=[("[chuckle] he stays", "joy"),
                          ("[clear throat] fish pie friday. you come", "caring")],
                  antworten=[("“I'll bring a bay leaf.”",
                              ("[chuckle] Hm. Who told you. …Bring it.", "amusement")),
                             ("Writes back: “Wouldn't miss it.”",
                              ("[clear throat] Good. Seven o'clock. Don't be early.", "neutral"))]),
    ),
    "elsa": dict(
        titel="The Lieutenant's Secret", akt=1, art="nachricht", ort="village_harbour", phasen=["tag", "abend"],
        start={"bekannt": "elsa"},
        teile=[
            dict(titel="Missing Paperback", ton="witzig",
                 lage="A message from Lieutenant Ferrandi. It reads like a police statement.",
                 zeilen=[("[clear throat] First Officer. An item has been removed from my locker at the post. "
                          "Personal item. Paperback.", "neutral"),
                         ("[sigh] I am not saying it was Totò. I am saying Totò was seen near the post with a "
                          "suspicious smile. Discretion is required.", "annoyance")],
                 wege=[("Asks Totò about it, casually, between two cigarettes.", P("charm", 12),
                        ("[clear throat] Recovered. He was using it to level a table. Chapter twelve has a coffee ring "
                         "on it. TOTÒÒÒ!", "anger"),
                        ("[sigh] He denied everything and offered me figs. I accepted the figs. The case stays open.",
                         "annoyance"), []),
                       ("Looks round the post himself. Who else has a key?", P("perception", 12),
                        ("[cough] It was behind the radio. I put it there myself. On Tuesday. This conversation never "
                         "happened.", "embarrassment"),
                        ("[sigh] You found my other book instead. We will not talk about that one either.",
                         "embarrassment"), [])],
                 ab=("“I'm not a detective, Elsa.”",
                     ("[clear throat] Noted. I'll handle it myself. With the full force of the law.", "neutral"))),
            dict(titel="To Elsa, No Hearts", ton="witzig",
                 lage="Another message from Elsa. Shorter than usual.",
                 zeilen=[("[clear throat] The author of a certain book is on holiday here. She has breakfast at Alva's. "
                          "Every morning. I have checked. Professionally.", "neutral"),
                         ("[sigh] I cannot ask her. I am the coast guard. Someone could ask her to sign a copy. To "
                          "Elsa. No hearts.", "nervousness")],
                 wege=[("Walks up to the author's table with the paperback and a big smile.", P("charm", 11),
                        ("[gasp] She wrote: For Elsa, the bravest reader on the coast. With a heart. I said no hearts. "
                         "…I'm keeping it.", "joy"),
                        ("[sigh] She signed it to Ella. Ella. I'll live with it. Thank you, First Officer.",
                         "disappointment"), []),
                       ("Tells the author there's a coast guard officer who knows her books by heart.",
                        P("empathy", 12),
                        ("[gasp] She came to the post. To me. She asked about chapter twelve. I'm writing this from the "
                         "locker room. Do not call me.", "excitement"),
                        ("[cough] She came to the post. I pretended not to know who she was and gave her a parking "
                         "ticket. I need a minute.", "embarrassment"), [])],
                 ab=("“Ask her yourself, Lieutenant.”",
                     ("[clear throat] Out of the question. Forget I asked. Delete this message.", "embarrassment"))),
            dict(titel="Lunch for Fourteen", ton="frech",
                 lage="A message from Elsa. You can almost hear the pots and the voices behind it.",
                 zeilen=[("[sigh] Family lunch. Nonna asked again who I'm seeing. Mama said nobody, as usual. In front "
                          "of my brothers.", "annoyance"),
                         ("[clear throat] I said I'm bringing a colleague. You are the colleague. Thirty minutes. Eat "
                          "everything they give you. That's an order.", "neutral")],
                 wege=[("Comes over, eats everything and praises Nonna's cooking to the skies.",
                        P("empathy", 12, "kueche"),
                        ("[laugh] Nonna gave you the end of the bread. The END. I've waited twenty-nine years for "
                         "that.", "joy"),
                        ("[sigh] My brothers made you arm-wrestle, and you lost to the youngest. Nonna liked you "
                         "anyway. Somehow.", "amusement"), []),
                       ("Plays the serious colleague and talks about the coast all through lunch.", P("cunning", 12),
                        ("[chuckle] Mama asked if we're getting married. You said only to the job. She cried into the "
                         "soup. It was perfect.", "amusement"),
                        ("[cough] You called me Elsa instead of Lieutenant. Now the whole family thinks we're engaged. "
                         "Thank you so much.", "embarrassment"), [])],
                 ab=("“I can't, Elsa. Good luck.”",
                     ("[sigh] Understood. I'll tell them my colleague is shy. They'll talk about it for a year.",
                      "disappointment"))),
        ],
        dank=dict(titel="The End of the Bread", lage="A photo from Elsa. Then, after a while, two messages.",
                  zeilen=[("[chuckle] Evidence attached.", "joy"),
                          ("[clear throat] Nonna says you're welcome every Sunday. I didn't argue. That's all. There are "
                           "figs on your table on board. They're not from me.", "caring")],
                  antworten=[("Writes back: “Respect, Lieutenant.”",
                              ("[chuckle] Respect, yes. …Thank you, First Officer. Really.", "gratitude")),
                             ("“Did you keep the end of the bread?”",
                              ("[laugh] I ate it on the way home. In uniform. Don't tell anyone.", "amusement"))]),
    ),
    "jana": dict(
        titel="Knots", akt=2, art="nachricht", ort="crew_corridor", phasen=["tag", "abend"],
        start={"bekannt": "jana"},
        teile=[
            dict(titel="Strudel Goes Up", ton="witzig",
                 lage="A message from Jana. Then a photo: a small white cat with blue eyes sitting on top of the radar arch, "
                      "looking very pleased with himself.",
                 zeilen=[("[gasp] sir sorry sorry. strudel is on the radar thing. the very high radar thing 🙈",
                          "fear"),
                         ("[sigh] if totò sees him he'll know there's a cat. there's no cat. but he's up there. "
                          "jessas 😭", "nervousness")],
                 wege=[("Climbs up after him, slowly, talking to him the whole way.", P("courage", 12),
                        ("[gasp] you got him!! he's purring in my hoodie now. thank you thank you sir, sorry 🥹🐱",
                         "relief"),
                        ("[sigh] he jumped down by himself the second you got up there. and now you're stuck?? i'm "
                         "getting maxwell. sorry 🙈", "embarrassment"), []),
                       ("Opens a tin of tuna at the bottom of the ladder and waits.", P("cunning", 11),
                        ("[laugh] he came down in like four seconds. na geh, he's so dumb. i love him so much 😹",
                         "joy"),
                        ("[cough] totò came because of the tuna smell. i said the tuna was for me. he gave me a very "
                         "long look 😬", "embarrassment"), [])],
                 ab=("“Ask Lea, Jana. I'm busy.”", ("[sniff] okay. sorry for asking sir. sorry 🙈", "sadness"))),
            dict(titel="Seven Seconds", ton="wholesome",
                 lage="Jana messages late in the afternoon.",
                 zeilen=[("[gasp] totò says tomorrow i tie up the tender. alone. in front of everyone 😳",
                          "nervousness"),
                         ("[sigh] can you time me?? i do the bowline in seven seconds. when nobody looks. when somebody "
                          "looks i forget what a rope is 🙈", "embarrassment")],
                 wege=[("Stands right next to her and talks about anything while she ties.", P("empathy", 12),
                        ("[laugh] six seconds!! while you were talking about spreadsheets!! i didn't even notice my "
                         "hands 🤯", "excitement"),
                        ("[sigh] i got it once in twenty. but that one was really good. sorry for keeping you so long "
                         "sir", "gratitude"), []),
                       ("Makes a game of it: one knot, one gummy bear.", P("cunning", 11),
                        ("[chuckle] i ate forty gummy bears and i can tie it in my sleep now. also i feel a bit "
                         "sick 😅", "amusement"),
                        ("[cough] strudel ate the gummy bears. all of them. we did not practise much. sorry 🙈",
                         "embarrassment"), [])],
                 ab=("“You'll be fine, Jana. You don't need me.”",
                     ("[sigh] okay. yes. i'll be fine. totally fine 🙃", "nervousness"))),
            dict(titel="In Front of Everyone", ton="wholesome",
                 lage="A single message from Jana, sent from the swim platform. The tender is already coming in.",
                 zeilen=[("[gasp] sir everyone is watching. chiara is watching. totò is watching. YAMAMOTO HAS THE "
                          "CAMERA 😱", "fear"),
                         ("[sniff] my hands forgot everything. are you there? can you be there 🙈", "nervousness")],
                 wege=[("Goes down to the platform and stands where she can see him. Just nods.", P("empathy", 13),
                        ("[gasp] I DID IT. first try. totò clapped. TOTÒ CLAPPED SIR 😭⚓", "joy"),
                        ("[sigh] i tied it wrong and the tender drifted a bit. totò said it happens to everyone. it "
                         "doesn't happen to everyone 🥲", "sadness"), []),
                       ("Texts back: “Seven seconds. Like when nobody's looking.”", P("charm", 12),
                        ("[laugh] i pretended nobody was looking and it WORKED. na geh!! i'm a sailor sir 🥹", "pride"),
                        ("[sniff] i looked at my phone instead of the rope. that was the problem. sorry. thank you "
                         "anyway", "embarrassment"), [])],
                 ab=("Doesn't answer. She has to do this alone.",
                     ("[sigh] ok. ok. just me then. like always 🫣", "nervousness"))),
        ],
        dank=dict(titel="Her Name on the Board", lage="A photo from Jana. She's sent it twice, then a third time.",
                  zeilen=[("[gasp] look!! 🪢", "pride"),
                          ("[sniff] totò put my name on the knot board. there's a knot board. i didn't know. MY NAME sir "
                           "🥹 strudel says thank you too. he doesn't exist though", "joy")],
                  antworten=[("“Future bosun.”", ("[gasp] don't say it out loud!! …say it again 🙈", "embarrassment")),
                             ("Sends a thumbs up and a cat emoji.",
                              ("[laugh] there's no cat sir. but he says thanks 😹", "amusement"))]),
    ),
    "maxwell": dict(
        titel="For Gogo", akt=2, art="video", ort="sun_deck", phasen=["tag", "abend"],
        start={"bekannt": "maxwell"},
        teile=[
            dict(titel="A Birthday Video", ton="witzig",
                 lage="Maxwell calls from the sun deck. He's holding the phone far too close to his face.",
                 zeilen=[("[laugh] Number One! Mr. Maximum has a mission. It's Gogo's birthday in Umlazi, and she wants a "
                          "video of her boy working hard.", "excitement"),
                         ("[sigh] Mr. Maximum needs a crew in the background, lifting things. Smiling. Ja-nee, brother, "
                          "nobody wants to. Help me.", "disappointment")],
                 wege=[("Rounds up the crew with a promise of Lola's pancakes.", P("charm", 12),
                        ("[sniff] Eight people, brother! Singing! Gogo watched it four times and called me her angel. "
                         "Mr. Maximum has allergies now.", "love"),
                        ("[sigh] Only Jana came, and she said sorry into the camera eleven times. Gogo loved her. Gogo "
                         "loves everybody.", "amusement"), []),
                       ("Films him alone and makes it epic: sunset, slow motion, a towel for a flag.", P("cunning", 11),
                        ("[laugh] Lekker! It looks like a movie! Gogo said I look like a soldier. Mr. Maximum will be "
                         "framing this.", "pride"),
                        ("[cough] The towel flew into the sea and Mr. Maximum went after it. That's the video now. Gogo "
                         "laughed so much, eish.", "amusement"), [])],
                 ab=("“Not today, brother.”",
                     ("[sigh] Shame. Mr. Maximum will do push-ups for the camera alone. Again.", "disappointment"))),
            dict(titel="Head of Wellness", ton="witzig",
                 lage="Maxwell calls. He's whispering, which for him is still loud.",
                 zeilen=[("[clear throat] Number One, small problem. Mr. Maximum told Gogo he is Head of Wellness on "
                          "this boat. With an office.", "embarrassment"),
                         ("[sigh] She wants a video tour of the office. Tonight. The office is a mat and a mop, brother. "
                          "Please.", "nervousness")],
                 wege=[("Turns a corner of the crew mess into an office: a desk, a plant, a sign on the door.",
                        P("cunning", 12, "handwerk"),
                        ("[laugh] HEAD OF WELLNESS on the door! Gogo asked if I have a secretary. Jana waved. Mr. Maximum "
                         "is crying, it's the plant, I'm allergic.", "joy"),
                        ("[sigh] The sign fell off during the tour. Gogo said, Maxwell, my angel, I know it's a mat. "
                         "I always knew. Eish.", "embarrassment"), []),
                       ("Joins the call himself. “Ma'am, your grandson is the most important man on this ship.”",
                        P("charm", 12),
                        ("[sniff] She believed you. Then she said she's proud, and I had to go outside. Allergies, "
                         "Number One. Big allergies.", "love"),
                        ("[chuckle] She asked you three questions about my salary, and you didn't know any of the "
                         "answers. She laughed at us both. That's Gogo.", "amusement"), [])],
                 ab=("“Tell her the truth, Maxwell.”",
                     ("[sigh] Ja. Maybe. Mr. Maximum will think about it. Mr. Maximum hates thinking.", "confusion"))),
            dict(titel="Things That Fly", ton="ernst",
                 lage="Maxwell calls from the sun deck. Next to him, Yasin's little drone sits on the deck like a "
                      "sleeping bird.",
                 zeilen=[("[clear throat] Number One. Mr. Maximum has decided something. One day he has to fly. For "
                          "Gogo. So he starts small.", "nervousness"),
                         ("[sigh] Yasin will fly his drone next to me, and I stand still. Ten seconds. Stay on the phone "
                          "with me, brother. Please don't laugh.", "fear")],
                 wege=[("Stays on the call and counts out loud with him, slowly.", P("empathy", 12),
                        ("[gasp] Ten seconds! Fifteen! It's next to my head and Mr. Maximum is still here! Brother. "
                         "BROTHER.", "surprise"),
                        ("[cough] Four seconds, then Mr. Maximum was behind the hot tub. But four is more than zero, "
                         "ja? Four is a start.", "embarrassment"), []),
                       ("Tells him to flex at it. “Show it who's bigger.”", P("courage", 12),
                        ("[laugh] Mr. Maximum flexed and the drone went backwards! It respects me now! We're friends, "
                         "the drone and me!", "pride"),
                        ("[sigh] The drone came closer to see the muscles, and Mr. Maximum jumped in the pool. Yasin got "
                         "it on video. Eish.", "embarrassment"), [])],
                 ab=("“I'm no good at this, Maxwell. Ask Yasin.”",
                     ("[sigh] Okay, Number One. Another day, then. The sky isn't going anywhere.", "sadness"))),
        ],
        dank=dict(titel="Phone Background", lage="A photo from Maxwell. He's sent it three times, just in case.",
                  zeilen=[("[laugh] MR. MAXIMUM AND HIS FRIEND THE DRONE 💪🚁", "pride"),
                          ("[sniff] gogo has it as her phone background. she showed the whole church. thank you number "
                           "one. you are my brother, no joke 🙏", "gratitude")],
                  antworten=[("“Next step: a helicopter.”",
                              ("[gasp] NO. no no. one thing at a time brother. mr. maximum needs to lie down 😅", "fear")),
                             ("“Proud of you, brother.”",
                              ("[sniff] allergies again. this boat is full of allergies 💪🥲", "love"))]),
    ),
    "nonna": dict(
        titel="Nonna's Kitchen", akt=2, art="video", ort="village_piazza", phasen=["tag", "abend"],
        start={"alle": [{"flag": "isabelle_handy"}, {"bekannt": "nonna"}]},
        teile=[
            dict(titel="The Spoon", ton="witzig",
                 lage="Isabelle's number calls. It isn't Isabelle. Nonna Fiora holds the phone at arm's length, as if "
                      "it might bite.",
                 zeilen=[("[clear throat] Is this the yacht man? Good. My spoon broke. Forty years, that spoon. It broke "
                          "on Frederico's head. Gently.", "annoyance"),
                         ("[sigh] Isabelle says you know everybody down there. Find me somebody who can carve chestnut "
                          "wood.", "neutral")],
                 wege=[("Takes the pieces down to Petru's workshop.", P("charm", 12),
                        ("[laugh] The fisherman carved me a new one, and he wouldn't take money. He wanted cake. A man "
                         "of sense!", "joy"),
                        ("[sigh] He glued it. Glued! It's holding, I admit. But this spoon has no soul now.",
                         "disappointment"), []),
                       ("Finds a fallen chestnut branch on the path and brings it up with the pieces.",
                        P("perception", 12),
                        ("[chuckle] A good branch and a good eye. Frederico will carve it this winter. A spoon from you, "
                         "almost.", "caring"),
                        ("[cough] That's oak, my boy. Oak. Never mind, it'll burn nicely. Sit, eat something.",
                         "amusement"), [])],
                 ab=("“I'm sorry, Nonna, I can't help with that.”",
                     ("[sigh] Then I cook with my hands, like my mother did. Go, go.", "neutral"))),
            dict(titel="Chestnut Day", ton="wholesome",
                 lage="Nonna calls on Isabelle's phone again. Somewhere behind her, Isabelle is apologising to "
                      "something.",
                 zeilen=[("[laugh] Today we make chestnut flour for the winter. Isabelle has already set fire to one "
                          "basket.", "amusement"),
                         ("[clear throat] Twenty sacks to carry, and my knees are not twenty. Come up. You carry, I feed "
                          "you. That's the deal in this kitchen.", "neutral")],
                 wege=[("Carries sacks up the stairs until his shoulders burn.", P("strength", 12),
                        ("[laugh] Twenty sacks! You're stronger than you look. Sit, sit, the first cake is yours.",
                         "joy"),
                        ("[cough] Eight sacks, and then you sat down on the ninth. Fine, fine. Eight is honest work.",
                         "amusement"), []),
                       ("Takes over the roasting so Isabelle doesn't burn another basket.", P("cunning", 12, "kueche"),
                        ("[chuckle] Not one burnt chestnut! Isabelle is jealous. I'm proud. Don't tell her.", "pride"),
                        ("[sigh] You burnt a basket too. Now Isabelle has company. Wonderful.", "amusement"), [])],
                 ab=("“Not today, Nonna.”",
                     ("[sigh] Then Frederico carries. Slowly. Complaining. Like a little donkey.", "annoyance"))),
            dict(titel="Names for the Chapel", ton="ernst",
                 lage="Nonna calls in the evening. She isn't smiling this time. Behind her, candles burn in the little "
                      "chapel.",
                 zeilen=[("[sigh] I'm writing the brothers' names in the chapel book. All of them. They should be "
                          "written somewhere better than my head.", "sadness"),
                         ("[clear throat] One name is missing. Brother Ambrosius wrote everything down, so it's in his "
                          "diary somewhere. My eyes are old. Will you help me find it?", "caring")],
                 wege=[("Reads Brother Ambrosius's diary with her, page by page.", P("perception", 13),
                        ("[sniff] Brother Tumasgiu. He kept the goats. I'd almost lost his face, and now I have his name "
                         "back. Thank you, my boy.", "gratitude"),
                        ("[sigh] We didn't find it. I'll leave a space in the book. God knows who it is. That's enough "
                         "for tonight.", "sadness"), []),
                       ("Asks her to tell him about each brother while she writes.", P("empathy", 12),
                        ("[sniff] While I was telling you about the goats, it came back. Tumasgiu. Thank you for "
                         "listening to an old woman.", "gratitude"),
                        ("[sigh] I talked and talked, and the name didn't come. But my heart is lighter. That's "
                         "something too.", "sadness"), [])],
                 ab=("“I'm sorry, Nonna. That one is yours to do.”",
                     ("[sigh] Yes. Maybe it is. Good night, my boy.", "sadness"))),
        ],
        dank=dict(titel="The Biggest Piece",
                  lage="A photo arrives from Isabelle's phone. Isabelle clearly took it; her thumb is in the corner.",
                  zeilen=[("[laugh] nonna says: the book is finished, all the names are in. and the cake is yours. COME "
                           "AND EAT IT", "joy", "isabelle"),
                          ("[chuckle] she also says stand still or she'll cook you. i don't know why. she's laughing a "
                           "lot ✝️😅", "amusement", "isabelle")],
                  antworten=[("“Tell her I'm coming. Standing still.”",
                              ("[laugh] she says good boy. she says that to the goats too 🐐", "amusement", "isabelle")),
                             ("Writes back: “Save me the biggest piece.”",
                              ("[chuckle] she already cut it. it's huge. she's guarding it with the spoon 🥄", "joy",
                               "isabelle"))]),
    ),
    "isabelle": dict(
        titel="Lavender", akt=2, art="nachricht", ort="village_piazza", phasen=["tag", "abend"],
        start={"flag": "isabelle_handy"},
        teile=[
            dict(titel="Lilac Foam", ton="witzig",
                 lage="A message from Isabelle, then a photo: the pharmacy floor, covered knee-deep in lilac foam.",
                 zeilen=[("[clear throat] um. hello. it's isabelle from the pharmacy. small question. how do you stop "
                          "soap 😬", "nervousness"),
                         ("[gasp] i was making lavender soap for the market and it just kept going?? it's up to my "
                          "knees. nonna is at mass. please hurry 🌿💥", "fear")],
                 wege=[("Asks her exactly what she put in, jar by jar.", P("perception", 12),
                        ("[gasp] the second jar wasn't lavender. it was soapwort. that explains SO much. it's "
                         "stopping!! thank you 🙏", "relief"),
                        ("[sigh] we never found out what it was. but the floor has never been this clean. so. small "
                         "win? ✨", "amusement"), []),
                       ("Tells her to open every window and sweep it all out into the garden.", P("cunning", 11),
                        ("[laugh] the whole garden smells of lavender now and the goats are white and fluffy. they "
                         "look so happy 😂🐐", "joy"),
                        ("[cough] the wind blew it all back in. and the goats came in with it. please don't tell "
                         "nonna 😭", "embarrassment"), [])],
                 ab=("“Wait for Nonna, Isabelle.”",
                     ("[sigh] okay. yes. i'll wait. on the table. above the foam 😬", "nervousness"))),
            dict(titel="Market Day", ton="wholesome",
                 lage="Isabelle messages from the village piazza, with a photo of a tiny table and eleven bars of soap "
                      "on it.",
                 zeilen=[("[laugh] i have a stall!! nonna said if i sell everything the pharmacy can buy a new still ✨",
                          "excitement"),
                         ("[sigh] it's been two hours and nobody stopped. i think it's my face. i look like i might "
                          "explode things. which. fair 😅", "disappointment")],
                 wege=[("Comes over and sells soap to everyone who walks past.", P("charm", 12),
                        ("[gasp] SOLD OUT. alva bought three. the coast guard lady bought one and said it was for "
                         "evidence 😂 thank you thank you", "joy"),
                        ("[sigh] we sold two. one to you. thank you for buying one. you didn't have to 🥲",
                         "gratitude"), []),
                       ("Writes a sign: “Handmade at the monastery. Mildly explosive.”", P("cunning", 12),
                        ("[laugh] people are queuing!! they want the explosive ones!! there are no explosive ones!! i'm "
                         "selling them anyway 🌿", "amusement"),
                        ("[cough] a man asked if they were safe and i said mostly. he left. i shouldn't say mostly 😬",
                         "embarrassment"), [])],
                 ab=("“Just give it time, Isabelle.”",
                     ("[sigh] okay. time. i have a lot of time. and eleven soaps 🧼", "sadness"))),
            dict(titel="Forty by Morning", ton="witzig",
                 lage="Isabelle messages late in the evening. The messages come in very fast.",
                 zeilen=[("[gasp] madame casanova wants FORTY soaps for the town hall. by tomorrow morning. forty!!! 😱",
                          "fear"),
                         ("[sigh] i've made nine. nonna is asleep. my arms are dead. are you awake?? i'm sorry. are "
                          "you?? ✝️", "nervousness")],
                 wege=[("Comes up and stirs the pots with her all night.", P("strength", 12, "kueche"),
                        ("[laugh] forty soaps!! at six in the morning!! we did it. i can't feel my arms. i love you. NOT "
                         "LIKE THAT. i'm so tired 😭", "joy"),
                        ("[sigh] thirty one. madame casanova said thirty one is a start. then she took all thirty "
                         "one 😅", "amusement"), []),
                       ("Calls the mayor's office first thing and buys her two more days.", P("charm", 13),
                        ("[gasp] two more days?! how?? she never gives anyone two more days. what did you say to "
                         "her 😳", "surprise"),
                        ("[cough] she said no, and that she'll remember the monastery's punctuality. i'm going to make "
                         "soap until i die ✝️", "fear"), [])],
                 ab=("“Get some sleep, Isabelle. It's too much.”",
                     ("[sigh] you're right. you're right. i'll make three more. then sleep. maybe. good night 🌙",
                      "caring"))),
        ],
        dank=dict(titel="Quiet and Useful", lage="A photo from Isabelle, then two messages.",
                  zeilen=[("[laugh] the town hall smells of lavender!! 🌿", "joy"),
                          ("[chuckle] nonna bought the new still with the money. she named it after you. she says it's "
                           "because it's quiet and useful. i think it's a compliment?? ✨", "amusement")],
                  antworten=[("“Quiet and useful. I'll take it.”",
                              ("[laugh] it also hisses sometimes. that part's like me 😬", "amusement")),
                             ("Writes back: “Proud of you, Isabelle.”",
                              ("[sniff] okay now i'm crying in the pharmacy. good tears. lavender tears 🥹", "love"))]),
    ),
}

# Dank-Fotos (werkzeuge\favour_fotos.py): Preset aus dem Prompt Studio (LoRAs nur lesend), Kleidung, Szene, Ausdruck.
# Positiv formuliert (Krea, CFG 1). Ein Mensch allein im Bild, Tiere erlaubt.
FOTOS = {
    "sirene": dict(preset="Yacht_Ligeia", ersetzen=[('full body shot, the camera far back, direct gaze, one single woman alone in the frame, sitting sideways on a low dark wet rock, propped on one straight arm, her upper body turned to the camera, her whole fish tail in full view, curving away from her hips across the rock and the floor to one side of the image, the tail fin fully inside the frame with empty floor around it,', 'instant film snapshot at night, a close-up portrait from the collarbones up, direct gaze, one single woman alone in the frame, both of her hands empty and pushing wet hair from her face, the tip of one octopus arm curling in from the bottom corner of the frame,')],
                   kleidung="wet bare shoulders, a thin dark leather cord around her neck, long wet hair clinging to her shoulders",
                   szene="dark wet rock and black water behind her, a little flash on her wet skin",
                   ausdruck="a small amused closed-lip smile"),
    "lola": dict(preset="Selfie_Lola",
                 kleidung="a faded oversized band t-shirt with a white apron over it, a smudge of flour on her cheek",
                 szene="a selfie in a small yacht galley in the evening, she holds up a round bamboo steamer full of "
                       "fluffy white bao buns right next to her face, steam rising, stainless steel counters behind her",
                 ausdruck="a huge proud goofy grin"),
    "alva": dict(preset="Selfie_Alva",
                 kleidung="a black off-the-shoulder top and gold hoop earrings",
                 szene="a selfie behind the counter of a small old Corsican village bar after closing time at night, "
                       "warm string lights overhead, a microphone lying on the wooden counter, empty wine glasses "
                       "and bottles on the shelves behind her",
                 ausdruck="laughing out loud, eyes half closed"),
    "petru": dict(preset="Yacht_Petru",
                  kleidung="a faded navy fisherman's sweater with the sleeves pushed up",
                  szene="a slightly crooked close-up selfie taken by an old man who has never taken a selfie, in his "
                        "cluttered boat workshop by the harbour, sitting beside an old wooden sea-water tank with a "
                        "heavy wooden lid closed on top, one weathered hand resting flat on the lid, a football match on "
                        "an old radio on the workbench, warm morning light, his thumb blurry in one corner of the frame",
                  ausdruck="the faintest shy smile under his white stubble"),
    "elsa": dict(preset="Selfie_Elsa",
                 kleidung="a light blue uniform shirt with rolled-up sleeves, collar open",
                 szene="a selfie at the end of a long outdoor family lunch table under a vine-covered pergola in a "
                       "Corsican village, plates, bread baskets and wine glasses on a white tablecloth, every chair "
                       "behind her empty, she proudly holds up the crusty end of a big round loaf of bread",
                 ausdruck="a rare wide triumphant grin"),
    "jana": dict(preset="Selfie_Jana",
                 kleidung="a navy crew polo shirt and navy shorts",
                 szene="a selfie on the teak swim platform of a superyacht in golden evening sun, sitting next to a "
                       "chrome mooring cleat with a thick white rope wrapped neatly around it, pointing at it proudly with "
                       "her free hand, a small pure white cat with blue eyes sitting beside her, the calm turquoise sea behind",
                 ausdruck="a proud shy grin, cheeks a little pink",
                 frisur="her hair pulled back in a high ponytail",            # Duc 29.10.: Pferdeschwanz, kein Blowout
                 lora_staerke={"Krea_Emma_D.safetensors": 1.0},
                 ersetzen=[("sitting on her bed, ", ""), ("blinking with one eye, pouty face, one hand pressing her "
                                                          "breasts,", ", a bright happy smile,")]),
    "maxwell": dict(preset="Yacht_Maximum",
                    kleidung="a tight black sleeveless training shirt and grey training shorts",
                    szene="a selfie on the sunny upper deck of a superyacht in bright daylight, he flexes his huge "
                          "arm, a small white camera drone hovering in the air right beside his head, blue sky and "
                          "sea behind him, sweat on his forehead",
                    ausdruck="a huge proud grin with a hint of nerves in his eyes"),
    "nonna": dict(preset="Yacht_Nonna",
                  kleidung="a rust-red linen blouse with the sleeves rolled up, dusted with flour",
                  szene="a photo taken by someone else in a rustic old monastery kitchen with thick stone walls and a "
                        "wood-fired oven, she raises a new wooden spoon high like a sword, a round chestnut cake on "
                        "the old wooden table in front of her, warm afternoon light from a small window",
                  ausdruck="laughing with her whole face"),
    "isabelle": dict(preset="Selfie_Isabelle",
                     kleidung="a simple ankle-length grey novice habit with the sleeves rolled up, no veil",
                     szene="a selfie in a small old monastery pharmacy with wooden shelves full of glass herb jars and "
                           "dried lavender bunches, she holds up a bar of lavender soap wrapped in brown paper with a "
                           "purple ribbon, a small smudge of lilac soap on her cheek",
                     ausdruck="a shy crooked proud smile, her round glasses sliding down her nose"),
}

# Belohnung je Ausgang (Teil 1-2 / Finale)
LOHN_OK, LOHN_OK_FINALE, LOHN_DANEBEN, LOHN_AB, LOHN_DANK = 8, 10, 1, -1, 3      # x1,6 (Duc 29.10.2026, vorher 5 / 6)


# Selfies der Flaschenpost (Duc 30.10.2026): was ein Mensch nie zu sehen bekommt. Immer unter Wasser, Haar schwebend, ohne Kamera.
_KOPF_SELFIE = ("instant film snapshot taken underwater from several metres away, a wide shot of her whole figure from her head down "
                "to the tail fin, small in the frame with the scene all around her, floating free, direct gaze, one single woman "
                "alone in the frame, a long emerald fish tail instead of legs, her long hair floating weightless around her head, "
                "both of her own arms and hands fully visible and relaxed at her sides, a separate thick orange octopus arm with pale "
                "suckers curling in from the lower corner of the frame, close to the camera and slightly out of focus, a clear gap "
                "of open water between the octopus arm and her body,")
_KLEIDUNG_SELFIE = "bare shoulders, a thin dark leather cord around her neck, tiny silver air bubbles on her skin"
for _kid, _szene, _ausdruck in (
        ("sirene", "inside the flooded hold of a sunken wooden ship, shafts of moonlight through the broken planks, a great shoal of "
                   "silver fish turning around her like a wall", "a calm private smile"),
        ("sirene_t2", "deep blue water at night, the huge dark eye of a sperm whale filling the whole background right behind her "
                      "shoulder, the whale's scarred skin", "a teasing half smile, utterly unafraid"),
        ("sirene_t3", "just under the surface in a violent storm at night, a fork of lightning seen from below through the heaving "
                      "water above her, foam and black waves overhead", "a calm serious look"),
        ("sirene_t4", "a fantastical lightless deep-sea reef, towering corals glowing in electric blue, violet and magenta all around her, "
                      "glowing jellyfish drifting between them and sparks of bioluminescence in the water, the only light on her "
                      "face comes from them", "a shy soft smile"),
        ("sirene_t5", "the sea at first light from below, a colossal spiralling tornado of a thousand silver fish rising around her "
                      "toward the golden surface, a manta ray gliding overhead", "a wide open happy smile")):
    FOTOS[_kid] = dict(FOTOS["sirene"], szene=_szene, ausdruck=_ausdruck, kleidung=_KLEIDUNG_SELFIE,
                       ersetzen=[(FOTOS["sirene"]["ersetzen"][0][0], _KOPF_SELFIE)])


def _z(t):
    text, gef = t[0], t[1]
    return text, gef, (t[2] if len(t) > 2 else None)


def _wann(k, bed, phasen):
    akt = AKT1 if k["akt"] == 1 else AKT2
    w = WANN(akt, phasen, bed=bed, holt_leute=bool(k.get("flasche")))     # die Flasche braucht sie nicht vor Ort
    if k["akt"] == 1:
        w["akt2"] = list(AKT2)              # Akt-1-Ketten laufen in Akt 2 weiter (kern/ereignisse.passt)
    return w


def _personen(kid, k, teil, dank=False):
    fv = {"kette": kid, "teil": teil, "ketten_titel": k["titel"]}
    if dank:
        fv.update(dank=True, foto="fv_" + kid)
    if k.get("flasche"):
        return {"handelnd": kid, "anrufer": kid, "betroffen": [], "favour": fv}
    return {"anrufer": kid, "anrufer_ort": k["ort"], "art": "nachricht" if dank else k["art"], "favour": fv}


def _zeile(kid, t):
    text, gef, wer = _z(t)
    return Z(wer or kid, klar(text), gef)


def bauen_events():
    out = []
    for kid, k in KETTEN.items():
        for n, t in enumerate(k["teile"], 1):
            flag = "fv_%s_%d" % (kid, n)
            bed = k["start"] if n == 1 else {"flag_seit": ["fv_%s_%d" % (kid, n - 1), 1]}
            ok_n = LOHN_OK_FINALE if n == 3 else LOHN_OK
            opts = []
            for chip, probe, ok, daneben, extra in t["wege"]:
                o = O(chip, probe=probe,
                      erfolg=[V(kid, ok_n), {"flag_datiert": flag}, F(flag + "_ok")] + list(extra),
                      fehlschlag=[V(kid, LOHN_DANEBEN), {"flag_datiert": flag}],
                      zeile=_zeile(kid, ok))
                o["zeile_fehlschlag"] = _zeile(kid, daneben)
                o["energie"] = 1
                opts.append(o)
            chip, z = t["ab"]
            opts.append(O(chip, [V(kid, LOHN_AB), F("fv_%s_aus" % kid)], zeile=_zeile(kid, z), art="auflegen"))
            art, bild = ("abend", k["ort"]) if k.get("flasche") else ("handy", ORT_DUC)
            out.append(E("fv_%s_%d" % (kid, n), art, t["ton"], t["titel"], _wann(k, bed, k["phasen"]), bild,
                         _personen(kid, k, n), t["lage"], [_zeile(kid, x) for x in t["zeilen"]], opts))
        d = k["dank"]
        folgen = [V(kid, LOHN_DANK)] + ([I(d["item"])] if d.get("item") else [])       # item: Lohn der Kette (Duc 29.10.2026)
        opts = [O(chip, list(folgen), zeile=_zeile(kid, z)) for chip, z in d["antworten"]]
        art, bild, ph = (("abend", k["ort"], ["tag", "abend"]) if k.get("flasche")
                         else ("handy", ORT_DUC, ["fruehstueck", "tag", "abend"]))
        out.append(E("fv_%s_dank" % kid, art, "wholesome", d["titel"],
                     _wann(k, {"flag": "fv_%s_3_ok" % kid}, ph), bild,
                     _personen(kid, k, 4, dank=True), d["lage"], [_zeile(kid, x) for x in d["zeilen"]], opts))
    return out


def stimme_tags():
    """Gesprochene Fassung jeder Favour-Zeile: [(wer, text, gesprochen)]."""
    out = []
    for kid, k in KETTEN.items():
        zeilen = []
        for t in k["teile"]:
            zeilen += t["zeilen"] + [t["ab"][1]]
            for _, _, ok, daneben, _ in t["wege"]:
                zeilen += [ok, daneben]
        zeilen += k["dank"]["zeilen"] + [a[1] for a in k["dank"]["antworten"]]
        for x in zeilen:
            text, _, wer = _z(x)
            assert TAG.search(text), "Favour-Zeile ohne Turbo-Tag: %s" % text
            out.append((wer or kid, klar(text), " ".join(text.split())))
    import ereignisse_ligeia
    return out + list(ereignisse_ligeia.STIMME)            # Pflichtszene lg_polaroid


def tags_schreiben():
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "favours"} for w, t, g in stimme_tags()]
    texte = {z["text"] for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "favours" and z["text"] not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)


EVENTS = bauen_events()

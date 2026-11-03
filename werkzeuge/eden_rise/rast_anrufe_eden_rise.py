# -*- coding: utf-8 -*-
r"""Rest calls (Duc 26.10.2026): when Duc rests at a rest site on an expedition, someone from the ship calls.

Who: the three people aboard with the most trust, in rotation (kern/expedition.rast_anrufer). What: wholesome - how
are you, hope it goes well, a small piece of their own day. Per person and trust level (0-5) THREE calls, each with
two short answers for Duc (warm / teasing). Answering gives +1 trust (8 points). English, natural sentences
(docs/wiki/STIL.md, the person's page in docs/wiki/figuren/). Texts: Story; the mechanics: kern/expedition.py.

    ANRUFE[pid][stufe] = [ {"text": "...", "gefuehl": "joy", "antworten": [{"text": "...", "ton": "warm"},
                                                                         {"text": "...", "ton": "frech"}]}, ... ]

    python rast_anrufe_eden_rise.py      -> module\eden_rise\rast_anrufe.json (validated)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(os.path.dirname(HERE)), "module", "eden_rise", "rast_anrufe.json")
PERSONEN = ("chiara", "rosi", "lola", "sophia", "lea", "holm", "toto", "maxwell", "jana")   # = expedition.RAST_ANRUFER
TOENE = ("warm", "frech")
GEFUEHLE = ("joy", "neutral", "amusement", "caring", "curiosity", "nervousness", "pride", "relief")

# Story fills this (start with trust levels 0-2, Duc 26.10.2026: 3 calls per person and level).
# Level 0 = still strangers, polite and a little awkward; 1 = friendly; 2 = they called because it's him.
# Duc is out on an expedition (Macchia, monastery); nobody on board knows exactly where. No case content.
def A(text, gefuehl, warm, frech):
    return {"text": text, "gefuehl": gefuehl, "antworten": [{"text": warm, "ton": "warm"}, {"text": frech, "ton": "frech"}]}


ANRUFE = {
    "chiara": {
        0: [A("First Officer, it's Chiara. Just checking you still exist. The crew asked, I said I'd find out.", "neutral",
              "“I exist. Tell them thank you for asking.”", "“Did they ask, or did you?”"),
            A("Quick one. Lunch is at one, and I'm not keeping a plate warm for anybody. I'm keeping a plate warm for you. Once.", "caring",
              "“Once is plenty. Thank you, Chiara.”", "“Rate the plate before I get there. Out of ten.”"),
            A("You left your cabin window open. I closed it. That's all. That's the whole call.", "nervousness",
              "“Thanks. I'd have come back to a puddle.”", "“You were in my cabin?”")],
        1: [A("Sunset from the bridge just now, I'd say seven. You're missing a seven, First Officer. That's a big loss.", "amusement",
              "“Save me the next one. I'll take a six.”", "“You never give anything above a seven.”"),
            A("Lola burned the focaccia and blamed the oven, the oven is innocent, I checked. Are you eating out there? Actually eating?", "caring",
              "“I'm eating. Mostly. Promise.”", "“Define eating.”"),
            A("I told Jana to polish the brass and she polished the bell. The bell is gleaming. Come back and say something nice to her, she'd die happy.", "joy",
              "“I'll tell her it's the best bell on the coast.”", "“The bell deserves it, honestly.”")],
        2: [A("It's quiet here without you shouting about solar panels. I didn't think I'd say that. Don't make it weird.", "caring",
              "“I miss the noise too. Nearly home.”", "“Too late, it's weird now.”"),
            A("I'm on the bridge, nobody's here, and I just wanted to hear a voice that isn't the radio. Yours will do.", "nervousness",
              "“Then I'll keep talking for a minute.”", "“Mine will do? High praise from you.”"),
            A("Come back in one piece, please. I've already sorted the first-aid kit twice today, and that's not a hobby.", "caring",
              "“One piece. You have my word.”", "“Sort it a third time, just in case.”")],
    },
    "rosi": {
        0: [A("Officer, Rosi. Is the bat holding up? If the grip is slipping, don't fix it yourself. You'll make it worse.", "neutral",
              "“It's holding. You built it well.”", "“I wasn't going to touch it. Much.”"),
            A("The generator is making a noise I don't like, and I wanted to tell somebody who wouldn't say just turn it off. So, you.", "nervousness",
              "“Tell me what it sounds like.”", "“Have you tried turning it off?”"),
            A("I'm not calling because I'm worried. I'm calling because the radio was boring. Totally different thing.", "neutral",
              "“Totally different. Got it.”", "“Of course. The radio.”")],
        1: [A("I named the new welder. It's called Phoenix. It rises from the sparks. Okay, it's a stupid name, but it's mine, and it's staying.", "pride",
              "“Phoenix is a great name.”", "“Better than Terremoto?”"),
            A("Officer! If anything out there bites your jacket, bring me the teeth marks. I want to see what I'm up against.", "amusement",
              "“I'll bring you the whole story.”", "“And if it bites me?”"),
            A("I fixed the coffee machine, which nobody asked for, and now everybody thinks I'm a saint. I'm not a saint. I was just bored without you breaking things.", "joy",
              "“You are a bit of a saint.”", "“I don't break things. I test them.”")],
        2: [A("Come back before dark, okay? Not because of me. Because of Phoenix, my new welder. Phoenix misses you. It's a welder thing.", "caring",
              "“Tell Phoenix I'll be home before dark.”", "“Phoenix should call itself next time.”"),
            A("I keep looking at the door of the workshop like you're going to walk in with something broken. It's a habit. A dumb one.", "nervousness",
              "“I'll bring you something broken. Promise.”", "“I'll break something on purpose, then.”"),
            A("Whatever's out there, hit it with the heavy end first. And then come back and tell me everything. In order.", "pride",
              "“Heavy end first. Then you get every detail.”", "“Yes, Captain.”")],
    },
    "lola": {
        0: [A("G'day Boss, Lola here! No reason. Just wanted to say there's soup if you want soup. Or not. No pressure. Mostly the cheese.", "joy",
              "“Soup sounds perfect, Lola.”", "“Mostly the cheese?”"),
            A("Don't tell anyone I told you, but Maxwell cried at a cooking video this morning. Anyway. How's the hike, mate?", "amusement",
              "“Steep. Your secret's safe.”", "“What kind of cooking video?”"),
            A("Boss, quick question, do you eat coriander or are you one of those soap people? I'm planning, see.", "curiosity",
              "“I eat it. Thanks for asking.”", "“Soap people. Hard soap people.”")],
        1: [A("I'm making you something for when you get back and I'm not telling you what it is. It's bao. I told you. I'm rubbish at secrets.", "amusement",
              "“Bao is exactly what I need.”", "“That's the worst secret I've ever heard.”"),
            A("Reckon you've walked about a hundred k by now, eh? Heaps of hills on that island. Drink some water, mate, I mean it.", "caring",
              "“Drinking water. Thanks, Lola.”", "“A hundred k? You're generous.”"),
            A("The crew's having a who-misses-the-boss-most competition. Chiara's winning, but don't tell her I said that. Mostly the cheese.", "joy",
              "“Tell them all I miss them too.”", "“Where are you on the scoreboard?”")],
        2: [A("It's just me in the galley and the kettle, and I thought, I'll ring the boss. So. Hi. That's it. Hi.", "caring",
              "“Hi, Lola. I'm glad you rang.”", "“That's the whole call? I love it.”"),
            A("Come home hungry, alright? I've been cooking like you're bringing an army. Bring an appetite at least.", "joy",
              "“I'll be starving. Save me the best bit.”", "“I'll bring the goat. She eats anything.”"),
            A("You know you're the only one who ever says thank you for the food? Like, properly. Just thought you should know that. Anyway. Be careful.", "caring",
              "“Your food deserves every thank-you, Lola.”", "“Thank you. For the call. See?”")],
    },
    "sophia": {
        0: [A("Darling, Sophia. The guests have asked where you've gone. I said off saving the world. Was I far off?", "amusement",
              "“Not too far. Thanks for covering.”", "“Tell them it's a secret mission.”"),
            A("I'm calling about the dinner on Thursday. I need to know if you're alive for it. Seating charts are cruel to the dead.", "neutral",
              "“Alive and coming. Seat me anywhere.”", "“Put me next to someone interesting.”"),
            A("Forgive the intrusion. I wrote something in my little book just now and it made me think of you. No, I won't say what.", "curiosity",
              "“Keep it. I like a mystery.”", "“Now I have to know.”")],
        1: [A("Darling, the sea's flat and the guests are asleep, which is the closest this boat gets to peace. How's your mountain?", "caring",
              "“Steep, but good. Enjoy the peace.”", "“Louder than your guests, at least.”"),
            A("Ten euros says you come back with a scratch on your face and pretend it's nothing. Do I win?", "amusement",
              "“Probably. Keep the ten euros ready.”", "“I'll walk into a tree just to make you rich.”"),
            A("Lea asked me if mountains have tides. I said no. She looked so disappointed I almost said yes. You'd have handled it better.", "joy",
              "“You handled it kindly. That's enough.”", "“Tell her the mountain has moods.”")],
        2: [A("No show tonight, darling. I just wanted to hear how you are. Really. Not the business-page version.", "caring",
              "“Tired, a bit sore, glad you called.”", "“The business-page version is very handsome.”"),
            A("I find I'm counting the hours until you're back, which is undignified. Please don't tell anyone. Least of all me.", "nervousness",
              "“Your secret's safe. I'm counting too.”", "“Your secret's in my little book now.”"),
            A("Be careful out there. I'm serious, for once. I've only just started being honest with you, and I'd like to keep going.", "caring",
              "“I'll be careful. Keep going.”", "“Honesty suits you, darling.”")],
    },
    "lea": {
        0: [A("Hi! It's Lea. Sorry, is this okay? Did you know goats can climb almost vertical rock? I just read it. Thought you should know. For the mountain.", "nervousness",
              "“Very useful. Thank you, Lea.”", "“I've got a goat with me. She agrees.”"),
            A("Sophia said not to bother you, but I wanted to ask if you've seen any eagles. Proper big ones? No? Okay. Bye. Sorry.", "curiosity",
              "“No eagles yet. I'll look for you.”", "“Only a very angry boar.”"),
            A("The water's so clear today you can see the anchor chain all the way down. I'm telling everyone. You're everyone now.", "joy",
              "“Save me a swim when I'm back.”", "“Lucky me, being everyone.”")],
        1: [A("Octopuses have three hearts, and mountains have zero, which is why you should come back to the sea soon. That's science.", "amusement",
              "“Science convinced me. Soon.”", "“Pretty sure that's not science.”"),
            A("I found a sea slug that looks exactly like a tiny dragon and nobody gets as excited as you would. Hurry up and be excited.", "joy",
              "“A tiny dragon? Keep it safe for me.”", "“I'm excited. Listen. Very excited.”"),
            A("Are you being careful, proper careful? Not Chiara careful, where she just shouts at things. Actually careful.", "caring",
              "“Actually careful. I promise, Lea.”", "“I might shout at a few things.”")],
        2: [A("I'm on the swim platform with my feet in the water and I thought, he'd like this. So I called. That's allowed, isn't it?", "caring",
              "“It's more than allowed. I'm glad you did.”", "“Only if you describe the water in detail.”"),
            A("Can I tell you something silly? I waved at the mountain this morning. In case you were looking. Were you looking?", "nervousness",
              "“I'll look next time. Wave again.”", "“I waved back. You missed it.”"),
            A("Come back dreckly, that's Cornish for sometime soon, but not too dreckly. You know what I mean. Okay. I'll stop talking now. I'm not stopping. Sorry.", "joy",
              "“Don't stop. I like hearing you.”", "“Dreckly sounds like never.”")],
    },
    "holm": {
        0: [A("Frankfurt. Holm. The doctors let me use the phone. I wanted to know if my ship is still floating.", "neutral",
              "“Floating, and in good hands. Get well.”", "“Floating. Mostly.”"),
            A("They say I must rest. I don't rest. So I'm calling you instead. How is the crew?", "neutral",
              "“They're holding together. They miss you.”", "“Better than the doctors, by the sound of it.”"),
            A("I heard you went up into the hills. Take more water than you think you need. Mountains don't care about papers.", "caring",
              "“Water, and respect for the mountain. Takk.”", "“Papers don't float, and they don't climb either.”")],
        1: [A("Frankfurt. The food here is terrible. I've decided it's a test. I'm passing. How are you passing yours?", "amusement",
              "“Slowly, but I'm passing.”", "“Lola could break you out with a sandwich.”"),
            A("Chiara called me. She sounded calm. That means you're doing something right. Don't let it go to your head.", "pride",
              "“I won't. Takk, Captain.”", "“Too late. It's in my head.”"),
            A("The nurse asked who I keep calling. I said a consultant who thinks he's a sailor. She laughed. You should be proud.", "amusement",
              "“Proud to be your best joke.”", "“Tell her I'm a sailor who thinks he's a consultant.”")],
        2: [A("I'm not good at this, Frankfurt. So I'll say it once. Be careful. The ship needs you more than it knows.", "caring",
              "“Heard. I'll be careful, Captain.”", "“Once is all I need from you.”"),
            A("I looked at my father's compass today and thought of you. Don't ask me why. I won't explain it twice.", "caring",
              "“I won't ask. Thank you for telling me.”", "“Not even once?”"),
            A("When I'm back on my feet, I'll teach you a proper bowline. You've earned the lesson. Barely.", "pride",
              "“I'll be waiting for it. Rest first.”", "“Barely is my favourite word from you.”")],
    },
    "toto": {
        0: [A("Comandante! Totò. I bet two to one you are lost already. Tell me I win.", "amusement",
              "“Not lost. Keep your money.”", "“Two to one? I'm insulted. Make it five.”"),
            A("Comandante, small question. If you find something nice up there, something nobody needs, you call Totò first. Okay? Just saying.", "curiosity",
              "“I'll call you first. Maybe.”", "“Nobody needs a goat?”"),
            A("Madonna, it's hot. Even the fish are complaining. How are you up there, walking like a tourist?", "neutral",
              "“Hot, but fine. Thanks for asking.”", "“Better tourist than you, Totò.”")],
        1: [A("Comandante! The crew bet on what time you come back. I took six o'clock. Please, for my wallet, six o'clock.", "joy",
              "“Six o'clock, for you.”", "“I'll come at five past, just to ruin you.”"),
            A("I sold a very small box to a very big man today. Don't worry. The box was legal. Mostly. How is the mountain?", "amusement",
              "“The mountain is fine. Be careful with the boxes.”", "“Mostly legal is my favourite kind.”"),
            A("Piccola Jana asked if you have a phone up there. I said Comandante always has a phone. Do you? Yes. You do. I'm talking to you.", "amusement",
              "“Tell her I'm fine.”", "“You just answered yourself, Totò.”")],
        2: [A("Comandante, no bet today. I just want to know you are okay. Strange, eh? Totò with no bet.", "caring",
              "“I'm okay. Thank you, Totò.”", "“No bet? Now I'm worried about you.”"),
            A("When you come back, I cook. Real ragù, my nonna's, five hours. Nobody gets it. You get it. Don't tell Lola.", "joy",
              "“Five hours of ragù. I'll be there.”", "“I'm telling Lola immediately.”"),
            A("Be careful with the animals, Comandante. They are not bad, they are scared. I know scared. You go slow with them.", "caring",
              "“I'll go slow. You're right.”", "“Since when are you the wise one?”")],
    },
    "maxwell": {
        0: [A("Number One! Mr. Maximum checking in. Are you stretching before your hike? Mr. Maximum hopes yes. Mr. Maximum fears no.", "amusement",
              "“I stretched. A little.”", "“Mr. Maximum's fears are correct.”"),
            A("Howzit, Number One. Jana did twenty push-ups today. Twenty! Mr. Maximum needed to tell someone, and you are someone.", "pride",
              "“Twenty! Tell her I'm proud.”", "“Twenty? Mr. Maximum, I did twenty-one.”"),
            A("Eish, brother, Mr. Maximum just remembered he never asked if you have snacks. Do you have snacks? Protein is a friend.", "caring",
              "“I have snacks. Thanks, coach.”", "“Does a goat count as a snack?”")],
        1: [A("Number One! Mr. Maximum has designed a mountain workout in your honour. It's just climbing. You're already doing it. You're welcome.", "amusement",
              "“Thank you for the honour.”", "“Great workout. Ten out of ten.”"),
            A("Lekker news, brother. The crew trained together this morning, everybody, even Sophia. She did one squat. Very elegant squat.", "joy",
              "“One elegant squat. That's progress.”", "“I'd pay to see that squat.”"),
            A("Ja-nee, Number One, Mr. Maximum isn't worried. Mr. Maximum is just calling a lot. Different thing. Very different.", "nervousness",
              "“Very different. I'm fine, brother.”", "“Suspiciously different.”")],
        2: [A("Brother, it's just me. No Mr. Maximum today. I wanted to say you're doing good. My gogo, my grandmother, would like you.", "caring",
              "“That means a lot. Thank you, Maxwell.”", "“Tell Gogo I said hello.”"),
            A("Number One, when you come back, we celebrate. Mr. Maximum will cook. Lola has said no. We'll celebrate anyway.", "joy",
              "“Celebrate with Lola's cooking, then.”", "“Mr. Maximum cooking? I'll bring a fire extinguisher.”"),
            A("Listen, brother. If something out there hurts, you breathe, you count to four, you keep going. Mr. Maximum believes in you. So does Maxwell.", "pride",
              "“Breathe, count to four. Got it.”", "“Both of you? That's a lot of belief.”")],
    },
    "jana": {
        0: [A("Hello? Sir? It's Jana. Sorry. Chiara said to call and ask if you need anything, so. Do you need anything? Sorry.", "nervousness",
              "“I'm fine, Jana. Thank you for calling.”", "“I need you to stop saying sorry.”"),
            A("Servus, Sir. Sorry, wrong button first, I called the galley. Lola says hello. Also, hello.", "nervousness",
              "“Hello, Jana. And hello to Lola.”", "“Two calls for the price of one.”"),
            A("Sir, I learned a new knot today. Totò says it's for boats, but I think it's for everything. I just wanted to tell somebody.", "pride",
              "“Show me when I'm back.”", "“Everything? Even mountains?”")],
        1: [A("Na geh, Sir, there's a cat on the boat. I mean, there's no cat. There's a very small potato. It says hello.", "amusement",
              "“Say hello to the potato for me.”", "“The potato and I need to talk.”"),
            A("Sir, I polished the bell, and Chiara said good, and then she said very good. Twice! I'm a bit happy. Sorry.", "joy",
              "“Twice is huge. Well done, Jana.”", "“Don't be sorry for being happy.”"),
            A("Coach made me run up the stairs ten times. Jessas, Sir, I think the mountain might be easier. How is the mountain?", "amusement",
              "“The mountain is about the same.”", "“Swap with me? I'll do the stairs.”")],
        2: [A("Sir, can I say something? It's quieter when you're not here. Not bad quiet. Just. I'll stop. Sorry. No, I'm not sorry.", "caring",
              "“Don't be sorry. I'll be back soon.”", "“Good. Not sorry suits you.”"),
            A("I told Lea you'd be back before the stars come out. Please make me right, Sir. I'm never right.", "nervousness",
              "“I'll make you right. Before the stars.”", "“You're right more than you think.”"),
            A("Sir, you were always kind to me, even when I said sorry to the door. So I wanted to say. Be careful. Bitte.", "caring",
              "“Thank you, Jana. I'll be careful.”", "“The door was very forgiving.”")],
    },
}


def check():
    err = []
    for pid, stufen in ANRUFE.items():
        if pid not in PERSONEN:
            err.append("%s: not a caller" % pid)
        for stufe, liste in stufen.items():
            if stufe not in range(6):
                err.append("%s: trust level %r must be 0-5" % (pid, stufe))
            for i, a in enumerate(liste):
                w = "%s/%s/%d" % (pid, stufe, i)
                if not a.get("text"):
                    err.append(w + ": text missing")
                if a.get("gefuehl", "joy") not in GEFUEHLE:
                    err.append(w + ": unknown feeling %s" % a.get("gefuehl"))
                if len(a.get("antworten", [])) != 2 or any(x.get("ton") not in TOENE or not x.get("text") for x in a["antworten"]):
                    err.append(w + ": needs two answers (warm, frech)")
    return err


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    err = check()
    if err:
        print("\n".join(err))
        sys.exit(1)
    daten = {"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\rast_anrufe_eden_rise.py - dort aendern.",
             "anrufe": {pid: {str(s): l for s, l in st.items()} for pid, st in ANRUFE.items() if st}}
    with open(TARGET, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
    n = sum(len(l) for st in ANRUFE.values() for l in st.values())
    print("rast_anrufe.json: %d calls, 0 errors" % n)


if __name__ == "__main__":
    main()

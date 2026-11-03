# -*- coding: utf-8 -*-
r"""Lola und Chiara in ganzen Saetzen (Duc 31.10.2026), Ablauf wie rosi_fluessig.py. Witze, Bewertungen, Lolas und Chiaras
stille Momente bleiben kurz. Dazu Unit-01 einheitlich "she".

    lola_chiara_fluessig.py          Probelauf
    lola_chiara_fluessig.py --los
"""
import rosi_fluessig as r

r.ZEILEN = {
    # Lola
    "We're all stuck in the same bay, mate. Let's eat like a family. A weird family. With a seagull.":
        "We're all stuck in the same bay, mate, so let's eat like a family. A weird family, with a seagull.",
    "Whatever happens tomorrow, tonight we dance. Barefoot. On the aft deck. Everyone.":
        "Whatever happens tomorrow, tonight we dance, barefoot on the aft deck, and that means everyone.",
    "I saved a bottle. And a cake. And a joint, but that's just for me. Mostly.":
        "I saved a bottle and a cake, and a joint, but that's just for me. Mostly.",
    "I made all of you! Out of love! And flour! Chiara, yours is very accurate, actually.":
        "I made all of you, out of love and flour! Chiara, yours is very accurate, actually.",
    "That was the LAST butter. Kevin is eating my croissants. Kevin is dead to me.":
        "That was the LAST butter, and now Kevin is eating my croissants. Kevin is dead to me.",
    "It's sweet and salty, mate. It's balance. Like yin and yang. Like you and a shower.":
        "It's sweet and salty, mate, so it's balance, like yin and yang. Like you and a shower.",
    "A whole tuna. A WHOLE TUNA. Petru, I love you. Marry me. Or just come for dinner.":
        "A whole tuna. A WHOLE TUNA. Petru, I love you, marry me. Or just come for dinner.",
    "Shhh. Everything is loud. The eggs are loud. Your face is loud. I love you all. Quietly.":
        "Shhh. Everything is loud, the eggs are loud, your face is loud. I love you all. Quietly.",
    "You ate it. You're a hero. I'll name a sauce after you.":
        "You ate it, you're a hero. I'll name a sauce after you.",
    "Ocean glitter, Chi. Second shelf. It's all about energy.":
        "It's ocean glitter, Chi, second shelf. It's all about energy.",
    "Mine have a secret ingredient. Love. And three kinds of cheese. Mostly the cheese.":
        "Mine have a secret ingredient, and it's love and three kinds of cheese. Mostly the cheese.",
    "It's a normal cookie. Ninety percent normal. Just one, love. You look like you need a hug in food form.":
        "It's a normal cookie, ninety percent normal. Just one, love, you look like you need a hug in food form.",
    "Strawberry almond. You two just invented a cake. I'm crying.":
        "Strawberry almond! You two just invented a cake, and I'm crying.",
    "Split it, Boss. Six ways. Everyone buys something stupid. That's the whole point of tips.":
        "Split it six ways, Boss, and everyone buys something stupid. That's the whole point of tips.",
    "I snore, Boss. Everyone knows I snore. A door that shuts is basically charity.":
        "I snore, Boss, everyone knows I snore, so a door that shuts is basically charity.",
    "Lola wins! Lola always wins. Sophia, you can visit. Bring biscuits.":
        "Lola wins! Lola always wins. Sophia, you can visit, but bring biscuits.",
    "You can't feed a crew on tins, Chi. That's how mutinies start. I read about it.":
        "You can't feed a crew on tins, Chi, that's how mutinies start. I read about it.",
    "Look at that! Fresh fish, no saffron needed. Boss, you're a genius. A smelly genius.":
        "Look at that, fresh fish and no saffron needed! Boss, you're a genius. A smelly genius.",
    "Can I come in? I'm not that high. I'm medium high. High enough to say I've wanted you since the galley.":
        "Can I come in? I'm not that high, I'm medium high. High enough to say I've wanted you since the galley.",
    "You can say no, Boss. I'll just go back and tell the stars they were wrong. They'll get over it.":
        "You can say no, Boss, and I'll just go back and tell the stars they were wrong. They'll get over it.",
    "Oh, thank god. Lie down. Let me show you what the stars had in mind.":
        "Oh, thank god. Lie down and let me show you what the stars had in mind.",
    "Talking first? You're so sweet it hurts. Okay. Talk to me. Then maybe kiss me. Then maybe more.":
        "Talking first? You're so sweet it hurts. Okay, talk to me, then maybe kiss me, then maybe more.",
    "On my way. Leave the light off. I know the way by heart now.":
        "On my way, so leave the light off. I know the way by heart now.",
    "Dreaming about you. Out loud. Sorry, Rosi.":
        "Dreaming about you, out loud. Sorry, Rosi.",
    "Okay. OKAY. That's annoyingly good. Rematch tomorrow. And you're still doing the dishes.":
        "Okay. OKAY. That's annoyingly good, so rematch tomorrow, and you're still doing the dishes.",
    "You let me win. I saw that. I'm keeping the trophy anyway.":
        "You let me win, I saw that. I'm keeping the trophy anyway.",
    "That's my fridge she's talking about! It's a good fridge! It's emotionally available!":
        "That's my fridge she's talking about! It's a good fridge, it's emotionally available!",
    "He did the VOICE. He did the fridge's VOICE. I'm going to cry.":
        "He did the VOICE. He did the fridge's VOICE, I'm going to cry.",
    "I brought snacks. Tim Tams. For the vibes. Don't ask where I hid them.":
        "I brought Tim Tams for the vibes. Don't ask where I hid them.",
    "You don't have to, Boss. But if you want to, we're all here. Nobody's going anywhere. Literally. We're stranded.":
        "You don't have to, Boss. But if you want to, we're all here and nobody's going anywhere. Literally, we're stranded.",
    "Fish pie, Boss. A proper one, mash on top, all crispy. He'll cry. In a good way. I reckon. Mostly the crust.":
        "Fish pie, Boss, a proper one with mash on top, all crispy. He'll cry, in a good way, I reckon. Mostly the crust.",
    "Vegemite! Boss! Real Vegemite! I'm going to cry. I'm already crying. Mostly the Tim Tams.":
        "Vegemite! Boss, real Vegemite! I'm going to cry, I'm already crying. Mostly the Tim Tams.",
    "Don't laugh. It's a kitchen. On a beach. Four stools, one stove, no head chef. Nobody yells. If somebody yells, they're out.":
        "Don't laugh, it's a kitchen on a beach. Four stools, one stove and no head chef, and nobody yells. If somebody yells, they're out.",
    "Got a name and everything. Well. Half a name. I keep crossing it out.":
        "Got a name and everything. Well, half a name. I keep crossing it out.",
    "Oh, it's on now. Chiara's going to kill us. Worth it. Mostly the flour.":
        "Oh, it's on now. Chiara's going to kill us, but it's worth it. Mostly the flour.",
    "Hi. Hello. Okay. The bread can wait. Bread is very patient.":
        "Hi. Hello. Okay, the bread can wait. Bread is very patient.",
    "The bread. Yes. You're no fun. You're a bit of fun.":
        "The bread, yes. You're no fun. You're a bit of fun.",
    "Pinch, turn, pinch, turn. No, gentle. Like you mean it but you're not in a hurry. …You're getting it. Keep going. I'm staying right here.":
        "Pinch, turn, pinch, turn. No, gentle, like you mean it but you're not in a hurry. …You're getting it, so keep going. I'm staying right here.",
    "Perfect. That's the best one you've done. I'm not letting go yet. For quality control.":
        "Perfect, that's the best one you've done. I'm not letting go yet, for quality control.",
    "…Yeah. Exactly like that. Jana, out. Take the bao. Take all the bao.":
        "…Yeah, exactly like that. Jana, out, and take the bao. Take all the bao.",
    "Boss. Backs are hard. I can do arms, I can do legs, but the middle bit is a mystery. Help a girl out.":
        "Backs are hard, Boss. I can do arms and I can do legs, but the middle bit is a mystery, so help a girl out.",
    "Mmm. You've got good hands. Lower. No, higher. No – yeah. There. Don't stop.":
        "Mmm, you've got good hands. Lower. No, higher. No – yeah, there. Don't stop.",
    "We survived the hearing! Nobody went to prison! I made the celebration pancakes. They're shaped like Megan. Eat her face.":
        "We survived the hearing and nobody went to prison! I made the celebration pancakes, and they're shaped like Megan. Eat her face.",
    "To week two! Nobody died! Some people nearly died! I made a cake shaped like a gull!":
        "To week two! Nobody died, though some people nearly did, and I made a cake shaped like a gull!",
    "Boss. Boss, look at the water. It's glowing. It's like someone spilled a lava lamp in the sea.":
        "Boss, look at the water, it's glowing. It's like someone spilled a lava lamp in the sea.",
    "Probably plankton. Probably. Only, can you hear that? Like humming? No? Just me? Cool. Totally fine.":
        "Probably plankton. Probably. Only, can you hear that humming? No? Just me? Cool, totally fine.",
    # Chiara
    "Overboard. Tonight. If the coast guard finds that, we lose the boat and every licence we've got.":
        "Overboard, tonight. If the coast guard finds that, we lose the boat and every licence we've got.",
    "Three minutes each, on a schedule. Guests first. That's the job.":
        "Three minutes each, on a schedule, and guests go first. That's the job.",
    "Megan wants the guest cabins stripped and the minibars counted. Tonight. She calls it cost discipline. I call it humiliating.":
        "Megan wants the guest cabins stripped and the minibars counted tonight. She calls it cost discipline, and I call it humiliating.",
    "We are not his props. We work here. Some of us would like to keep working here.":
        "We are not his props. We work here, and some of us would like to keep working here.",
    "Children on a superyacht with no power. The insurance would die. I would die.":
        "Children on a superyacht with no power? The insurance would die, and then I would die.",
    "That is theft. With a list. In handwriting.":
        "That is theft, with a list, in handwriting.",
    "There are rules for a reason. Guests pay for distance. Even stranded guests.":
        "There are rules for a reason. Guests pay for distance, even stranded guests.",
    "Megan lands tomorrow. I want this boat to shine. Every brass handle. Every glass.":
        "Megan lands tomorrow, and I want this boat to shine, every brass handle and every glass.",
    "The coast guard has now seen half our crew naked. I need a rule. I need several rules.":
        "The coast guard has now seen half our crew naked, so I need a rule. I need several rules.",
    "Order her to rest. She won't listen to me. She listens to you, apparently.":
        "Order her to rest. She won't listen to me, but she listens to you, apparently.",
    "We have rice, tins and one bottle of champagne. My people are exhausted. This is madness.":
        "We have rice, tins and one bottle of champagne, and my people are exhausted. This is madness.",
    "Tomorrow we need clear heads. Everyone in their bunk by midnight. Please.":
        "Tomorrow we need clear heads, so everyone's in their bunk by midnight. Please.",
    "Crew cabin inspection. Officers included. Especially officers. What's this under your pillow?":
        "Crew cabin inspection, and that includes officers. Especially officers. What's this under your pillow?",
    "Is this poetry? Did you write poetry? About the sea? You rhymed sea with me.":
        "Is this poetry? Did you write poetry about the sea? You rhymed sea with me.",
    "Asking for help in front of the crew. Holm would have liked that. So do I.":
        "Asking for help in front of the crew. Holm would have liked that, and so do I.",
    "Race you to the buoy. Loser gets dunked. I don't lose.":
        "Race you to the buoy, and the loser gets dunked. I don't lose.",
    "Stop reading. Stop reading right now. Why does the officer have my haircut?":
        "Stop reading, stop reading right now. Why does the officer have my haircut?",
    "The interior crew is mine. I assign it. You don't just take my people because you need hands.":
        "The interior crew is mine and I assign it. You don't just take my people because you need hands.",
    "White shirts, navy trousers. We represent the yacht. We look like a crew, not a festival.":
        "White shirts and navy trousers, because we represent the yacht. We look like a crew, not a festival.",
    "Some of us are on the bridge at five. Turn it off, Lea. Now, please.":
        "Some of us are on the bridge at five, so turn it off, Lea. Now, please.",
    "We have a budget, Lola. The budget does not include saffron. The budget barely includes us.":
        "We have a budget, Lola, and the budget does not include saffron. The budget barely includes us.",
    "Okay. That was fast. That was annoyingly hot and fast. The dishes are mine. Don't gloat.":
        "Okay, that was fast. That was annoyingly hot and fast. The dishes are mine, so don't gloat.",
    "A tie. You planned that. Nobody plans a tie. Who are you?":
        "A tie. You planned that, and nobody plans a tie. Who are you?",
    "You always ask about us. You never talk about you. Where does the First Officer come from?":
        "You always ask about us, but you never talk about you. Where does the First Officer come from?",
    "Okay. The offer stays open. That's how it works on a boat.":
        "Okay, the offer stays open. That's how it works on a boat.",
    "In this uniform? Absolutely not. …Tomorrow. Seven. Don't be late.":
        "In this uniform? Absolutely not. …Tomorrow at seven, and don't be late.",
    "…Fine. That was funny. Now get up, you're lying on my clean deck.":
        "…Fine, that was funny. Now get up, you're lying on my clean deck.",
    "She'll want the watch lists. She always signs them. She'll want to sign them.":
        "She'll want the watch lists, because she always signs them. She'll want to sign them.",
    "Bottom shelf. Behind the fish sauce. With the lid taped. Merci.":
        "Bottom shelf, behind the fish sauce, with the lid taped. Merci.",
    "That's not a number. That's a date. …Seven. For the answer. Maybe eight.":
        "That's not a number, that's a date. …Seven for the answer. Maybe eight.",
    "I know. I'm letting go. Look, I'm letting go.":
        "I know, I'm letting go. Look, I'm letting go.",
    "…Oh. Okay. That's – we're even. Don't be late for the briefing.":
        "…Oh. Okay, that's – we're even. Don't be late for the briefing.",
    "So. You're the First Officer. Tell me what we do.":
        "So you're the First Officer. Tell me what we do.",
    "Good call. Seven out of ten. I'd have said the same, but you didn't ask, did you?":
        "Good call, seven out of ten. I'd have said the same, but you didn't ask, did you?",
    "It'll hold. Sure. I'll just stand here and make sure of that on my own, then.":
        "It'll hold, sure. I'll just stand here and make sure of that on my own, then.",
    "You went to a tailor. About me. You told him my measurements.":
        "You went to a tailor about me, and you told him my measurements.",
    # Unit-01 ist "she" (Duc 31.10.2026)
    "My nonna sang this to tractors, and those tractors never died. Shh, he's listening.":
        "My nonna sang this to tractors, and those tractors never died. Shh, she's listening.",
    "This isn't ours, and it isn't anybody's on this boat. Somebody soldered it into him, and it's neat work. Better than mine.":
        "This isn't ours, and it isn't anybody's on this boat. Somebody soldered it into her, and it's neat work. Better than mine.",
    "Give me a week and a very large coffee. And don't tell Unit-01 I said he got hacked. He's sensitive.":
        "Give me a week and a very large coffee. And don't tell Unit-01 I said she got hacked. She's sensitive.",
    "Rosi has his control board open":
        "Rosi has her control board open",
}

if __name__ == "__main__":
    r.main()

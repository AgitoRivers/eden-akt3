# -*- coding: utf-8 -*-
r"""Sophia, Siri, Alva, Megan, Toto, dazu wenige Zeilen von Petru und Elsa in ganzen Saetzen (Duc 31.10.2026), Ablauf wie
rosi_fluessig.py. Witze und Marotten bleiben kurz, ebenso Lea und Holm, und die abgenommenen Texte von Tag 0 und vom Hafen.
Unit-01 ist auch bei Toto "she".

    rest_fluessig.py          Probelauf
    rest_fluessig.py --los
"""
import rosi_fluessig as r

r.ZEILEN = {
    # Sophia
    "Five hundred euros, in cash. He wants the crew in his video tomorrow. Smiles, drama, swimwear.":
        "Five hundred euros in cash, darling. He wants the crew in his video tomorrow, with smiles, drama and swimwear.",
    "Something small. Breakfast on the foredeck, no cameras, just us. I'll organise it.":
        "Something small, breakfast on the foredeck with no cameras, just us. I'll organise it.",
    "Siri asked if a crew bunk is free. Just for a few nights. Yasin found out. He's in the corridor.":
        "Siri asked if a crew bunk is free, just for a few nights. Yasin found out, and now he's in the corridor.",
    "Megan wants a dinner tomorrow. Two investors, eight courses, candles. On our dead boat. With a smile.":
        "Megan wants a dinner tomorrow, darling, with two investors, eight courses and candles, on our dead boat. With a smile.",
    "Badly for the charts. Very well for everyone else. …It's nothing, darling. Just ideas. Come by later, and I'll read you the ending.":
        "Badly for the charts, and very well for everyone else. …It's nothing, darling, just ideas. Come by later, and I'll read you the ending.",
    "One afternoon off. The crew works better rested. It's in all the studies. I'll send you the studies.":
        "One afternoon off, because the crew works better rested. It's in all the studies. I'll send you the studies.",
    "It IS a festival, darling. Let them shine. Rosi has a dress she's never worn. Let her wear it.":
        "It IS a festival, darling, so let them shine. Rosi has a dress she's never worn. Let her wear it.",
    "A question only the host can answer. Clever. I'm keeping that one.":
        "A question only the host can answer. That's clever, and I'm keeping that one.",
    "Don't ask. It's research. You'd be surprised how much research a person can do at a bar.":
        "Don't ask, it's research. You'd be surprised how much research a person can do at a bar.",
    "You might be. A minor character. Tall, asks too many questions. He's growing on the author, which is very inconvenient.":
        "You might be, as a minor character. He's tall and asks too many questions, and he's growing on the author, which is very inconvenient.",
    "He's flying towards the village. The bell tower. That gull has a nest up there, everybody knows.":
        "He's flying towards the village, to the bell tower. That gull has a nest up there, everybody knows.",
    # Siri
    "I'd sing. Really, I would. But only if nobody films it. Not one second.":
        "I'd sing, really, I would, but only if nobody films it. Not one second.",
    "It was cold. It was on the chair. It smells like the sea and coffee. I'm keeping it.":
        "It was cold and it was on the chair, and it smells like the sea and coffee. So I'm keeping it.",
    "Thank you. I needed someone to just stand there. That's all.":
        "Thank you. I needed someone to just stand there, that's all.",
    "Three hearts. Blue blood. He'll remember you, Lea. They remember faces.":
        "Three hearts and blue blood. He'll remember you, Lea, because they remember faces.",
    "Pick someone who can't sing. It's more fun. Pick Chiara.":
        "Pick someone who can't sing, it's more fun. Pick Chiara.",
    "This one's not going up. My manager would hate it. No filter, bad light, my hair's doing a thing.":
        "This one's not going up, because my manager would hate it. There's no filter, the light's bad, and my hair's doing a thing.",
    "Actually, no. Don't take it. Just look. Is that okay? I want one golden hour that nobody else gets.":
        "Actually, no, don't take it, just look. Is that okay? I want one golden hour that nobody else gets.",
    "Keep watch. Like a lighthouse. I like that, you'd make a good lighthouse.":
        "Keep watch, like a lighthouse. I like that, you'd make a good lighthouse.",
    # Alva
    "My bar has had one rule for forty years. Everybody drinks. Fishermen, mayors, dogs. No rope.":
        "My bar has had one rule for forty years: everybody drinks, fishermen, mayors and dogs. No rope.",
    "I had a key made. For the back room. For you. Nobody else has one, not even my accountant.":
        "I had a key made for the back room, for you. Nobody else has one, not even my accountant.",
    "Tonight, or whenever you want. Wherever you want. I'll bring the fan. You know what the fan is for.":
        "Tonight or whenever you want, and wherever you want. I'll bring the fan. You know what the fan is for.",
    "Sweet pork and eggs. Like a grandmother made it. Which grandmother, eh? You'll tell me one day.":
        "Sweet pork and eggs, like a grandmother made it. Which grandmother, eh? You'll tell me one day.",
    "A duet. Good. Everyone in Corsica falls in love during a duet. It's the law.":
        "A duet, good. Everyone in Corsica falls in love during a duet. It's the law.",
    # Megan
    "A stranded yacht is a story, First Officer. I sell stories. Your crew serves. Beautifully. Or else.":
        "A stranded yacht is a story, First Officer, and I sell stories. Your crew will serve. Beautifully. Or else.",
    "The crew. At the table. With my investors. You're either a genius or insane. I'm intrigued.":
        "The crew at the table, with my investors. You're either a genius or insane, and I'm intrigued.",
    "Impressive. Give that girl a raise. Not a big one.":
        "Impressive. Give that girl a raise, but not a big one.",
    "You let me win. Never do that again. I want to beat you properly.":
        "You let me win. Never do that again, I want to beat you properly.",
    "Darling, I invented the studies. Half a day. And they wear Eden caps while they relax.":
        "Darling, I invented the studies. They get half a day, and they wear Eden caps while they relax.",
    "Dust. On my bar. On my boat. Explain it to me as if I were an investor.":
        "Dust, on my bar, on my boat. Explain it to me as if I were an investor.",
    # Toto
    "Comandante, a few boxes take a little boat trip tonight. Back tomorrow evening. Nobody sees nothing.":
        "Comandante, a few boxes take a little boat trip tonight, and they're back tomorrow evening. Nobody sees nothing.",
    "Rosi, cara, it was a joke. A Neapolitan joke. We say it to everyone. Even to men.":
        "Rosi, cara, it was a joke, a Neapolitan joke. We say it to everyone, even to men.",
    "Comandante. My nonna's ragù. Six hours. If you lose, you say on camera that Napoli is the centre of the world.":
        "Comandante, this is my nonna's ragù, six hours on the fire. If you lose, you say on camera that Napoli is the centre of the world.",
    "A recipe swap? You know what that's worth in Naples? Everything. Here, my cousin's fish. Fresh. Don't ask.":
        "A recipe swap? You know what that's worth in Naples? Everything. Here's my cousin's fish, fresh. Don't ask.",
    "Comandante. One question. Is it over now? Or is this only the start?":
        "Comandante, one question. Is it over now, or is this only the start?",
    "Comandante. Nobody knows what really happened the night of the fire. That's the problem. Everybody guesses.":
        "Comandante, nobody knows what really happened the night of the fire. That's the problem, everybody guesses.",
    "He'll forgive you. He's a diesel. Diesels forgive everything.":
        "She'll forgive you. She's a diesel, and diesels forgive everything.",
    "My cousin. Gennaro. From Bastia. He owes money to some people. The wrong people. The worst people.":
        "My cousin Gennaro, from Bastia, owes money to some people. The wrong people. The worst people.",
    "And boss? Whatever he did. He's not a bad man. He's just Gennaro.":
        "And boss? Whatever he did, he's not a bad man. He's just Gennaro.",
    # Petru und Elsa
    "In the village they say she was seen with a man in uniform. A soldier. Up there, by the tower.":
        "In the village they say she was seen with a man in uniform, a soldier, up there by the tower.",
    "Grouper. A big one. Under the harbour wall. Fifty years old. I call him Napoleon.":
        "A big grouper under the harbour wall, fifty years old. I call him Napoleon.",
    "An official purchase. With a receipt. In this village. I might frame it.":
        "An official purchase with a receipt, in this village. I might frame it.",
    "Thank you, First Officer. I'll file it. Under pending. For a while.":
        "Thank you, First Officer. I'll file it under pending, for a while.",
}

if __name__ == "__main__":
    r.main()

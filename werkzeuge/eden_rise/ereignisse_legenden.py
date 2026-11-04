# -*- coding: utf-8 -*-
r"""Das Dorf, das redet (Duc 30.10.2026, Brain Trust zu Mundi, Option B) - Daten zu kern\legenden.py.

Eine Tat (Missions-Flag) wird ueber Nacht zur Legende und waechst: Stufe 0 ab dem Morgen danach (was geschah), Stufe 1
zwei Tage spaeter (uebertrieben), Stufe 2 vier Tage spaeter (voellig verdreht). Wer dabei war, erzaehlt es eher wahr;
das Dorf legt nach. Einstiege:
  zeit   erste Zeile, wenn Duc Zeit mit der Figur verbringt (Szenenstart; landet in ihrem Gedaechtnis)
  laden  Begruessung beim Betreten ihres Ladens
  Handy  eine Figur fragt nach - EVENTS unten (gewoehnliche Handy-Events, Bedingung flag_seit leg_<tat>)
Zeilen stehen hier MIT Turbo-Tag (gesprochen); das Spiel zeigt sie ohne. tags_schreiben() traegt sie in
stimme_tags.json ein (Quelle "legenden"). Spoilerschutz: keine Taeter, keine Chips, keine Agenten, die Sirene ohne Namen.

Merker (Duc 30.10.2026): JEDE neue NPC kommt in die FAMILIE und bekommt Zeilen zu den Missionen
(tests/test_legenden.py prueft die Abdeckung). Danzel, Bibi und Charly (Red Trio) sind schon drin, auch wenn sie
noch nicht gebaut sind - ihre Zeilen warten, bis sie auftreten.
"""
import json
import os
import re

from ereignisse_basis import *  # noqa: F401,F403

TAG = re.compile(r"\s*\[(chuckle|clear throat|cough|gasp|laugh|shush|sigh|sniff)\]\s*")


def klar(t):
    return " ".join(TAG.sub(" ", t).split())


# tat: flag = das Missions-Flag, titel fuer die Tagesmeldung, ruf = Ruf im Dorf je Wachstumsstufe (1 und 2),
#      ruf_wenn = nur dann (Bedingung wie in den Events)
TATEN = {
    "hafen": dict(flag="kloster_faden", titel="the stranger who held the quay against the animals", ruf=1),
    "kloster": dict(flag="kloster_fertig", titel="the man who came back from San Martinu with a lion story", ruf=1),
    "berge": dict(flag="berge_fertig", titel="Petru's daughter and the tower", ruf=1,
                  ruf_wenn={"nicht": {"flag": "bg_weg_b"}}),
    "grotte": dict(flag="grotte_fertig", titel="the smugglers' grotto and the third step", ruf=0),
    "sirene": dict(flag="sirene_fertig", titel="singing from the point at night", ruf=0),
    "kevin": dict(flag="kevin_fertig", titel="the duel on the bell tower", ruf=1),
    "red_trio": dict(flag="red_trio_fertig", titel="three people in red and the jacket", ruf=1),     # ernste Quest, noch nicht gebaut
    # Akt 3 (04.11.2026): neue Figuren und Taten, ueber die das Dorf redet
    "schwur": dict(flag="buenaventura_schwur", titel="forty pirates carrying stones", ruf=0),
    "anwalt": dict(flag="a3_zeugen_auftrag", titel="the lawyer from Lyon and the men from Ajaccio", ruf=0),
    "mast": dict(flag="a3_mast_fertig", titel="the red light on the ridge", ruf=1),
}

# Wer zur Familie gehoert (Merker): Crew, Gaeste, Dorf - und die neuen Figuren, sobald sie da sind
FAMILIE = ["rosi", "toto", "lola", "chiara", "sophia", "lea", "maxwell", "jana", "siri", "yasin", "yamamoto",
           "alva", "petru", "elsa", "casanova", "nonna", "isabelle", "danzel", "bibi", "charly",
           "pascal", "mina", "batu", "sandru", "anghjulu"]

NICHT_B = {"nicht": {"flag": "bg_weg_b"}}
NACH_TRIO = {"flag": "rt_ausgang_alle"}       # Danzel scherzt nur bei "alle"; zerbricht das Trio, bleibt er auch, aber ernst (E-112)
NACH_BIBI = {"flag": "rt_bibi_bleibt"}        # Bibi und Charly bleiben nur, wenn Duc es ihnen sagt (rt_was_nun)
NACH_CHARLY = {"flag": "rt_charly_bleibt"}

MAST_AUS = {"flag": "a3_mast_aus"}
MAST_AN = {"flag": "a3_mast_an"}

# (tat, wer, wo, stufe, text mit Turbo-Tag, gefuehl[, wenn])
ZEILEN = [
    # ------------------------------------------------------------ Akt 3: Buenaventuras Schwur (Tag 24)
    ("schwur", "mina", "zeit", 0, "[chuckle] Yacht, a pirate carried my bicycle to the post office this morning. He said sorry three times. In Spanish.", "amusement"),
    ("schwur", "batu", "zeit", 1, "[sigh] The pirates eat like my nephews. I cook for forty now. I'm not complaining. A little.", "caring"),
    ("schwur", "petru", "zeit", 1, "[clear throat] They carry stones well. Badly at first. Now well. The sea teaches everyone.", "approval"),
    ("schwur", "lola", "zeit", 2, "[laugh] Boss, Mina says the captain wants to be made mayor now. Mostly a rumour. Mostly.", "amusement"),
    # ------------------------------------------------------------ Akt 3: Maitre Delorme und Kommissar Luciani (ab Tag 25)
    ("anwalt", "mina", "zeit", 0, "[sigh] Every letter from Monaco has the same name at the bottom now. Maître Delorme, a lawyer in Lyon. Even his signature looks expensive.", "neutral"),
    ("anwalt", "elsa", "zeit", 0, "[clear throat] Commissioner Luciani is coming himself. Twenty-two years in Ajaccio. They say he has never smiled in public.", "neutral"),
    ("anwalt", "casanova", "zeit", 1, "[sigh] A lawyer from Lyon. In my village. For a fishing village, Monsieur, that is like sending a shark to a swimming pool.", "anger"),
    ("anwalt", "sophia", "zeit", 1, "[chuckle] Darling, I looked him up. Delorme has never lost a case. Ten euros says he has never met a Corsican grandmother either.", "amusement"),
    ("anwalt", "petru", "zeit", 2, "[clear throat] The lawyer has a boat in Lyon, they say. Lyon has no sea. Hm.", "neutral"),
    ("anwalt", "jana", "zeit", 2, "[gasp] Sir, Lola says the commissioner can see lies. Like a shark sees blood. Sorry, is that true?", "nervousness"),
    # ------------------------------------------------------------ Akt 3: The Red Light (der Mast auf dem Kamm)
    ("mast", "batu", "zeit", 0, "[chuckle] Last night the little lights fell into the sea. Like stars. My neighbour made a wish. I made two.", "joy", MAST_AUS),
    ("mast", "elsa", "zeit", 0, "[clear throat] I hear everything on that mast now, First Officer. Every drone, every word. I barely sleep. I'm not complaining.", "neutral", MAST_AN),
    ("mast", "petru", "zeit", 1, "[sigh] No red light on the ridge. The night looks like the night again.", "relief", MAST_AUS),
    ("mast", "mina", "zeit", 1, "[sigh] The red light is still blinking, Yacht. People whisper again when they pass under it. I know it's ours now. They don't.", "nervousness", MAST_AN),
    ("mast", "lola", "zeit", 2, "[laugh] Boss! The village says you climbed the mountain and punched a robot the size of a fridge. Mostly true?", "amusement"),
    ("mast", "danzel", "zeit", 2, "[gasp] She climbed that ridge in the dark and switched the red light off. Charly. My... Charly. I'm going to sew her a medal.", "pride", {"alle": [NACH_CHARLY, MAST_AUS]}),
    # ------------------------------------------------------------ Hafenkampf (Tag 2)
    ("hafen", "rosi", "zeit", 0, "[chuckle] Officer. I checked the bat after the quay. Not one dent. The bat is fine. "
     "Your technique is a disaster, but the bat is fine.", "amusement"),
    ("hafen", "lola", "zeit", 0, "[laugh] Mate, Alva's telling everyone you fought the dogs off on your own. Don't tell "
     "anyone I told you, but I reckon she fancies you a bit. Mostly the bat.", "amusement"),
    ("hafen", "maxwell", "zeit", 1, "[laugh] Number One! The village says you knocked out a wild boar with one swing. "
     "Mr. Maximum is proud of you, brother. Mr. Maximum would also like to see the footwork.", "excitement"),
    ("hafen", "chiara", "zeit", 1, "[sigh] On Tuesday the rats were twelve. Tonight at the bar they were forty, and one "
     "of them wore a little hat. I give the story a six. The hat was a nice touch.", "amusement"),
    ("hafen", "elsa", "zeit", 1, "[clear throat] First Officer. I have six statements about the harbour, and in four of "
     "them you are taller than you are. I am filing the other two.", "amusement"),
    ("hafen", "sophia", "zeit", 2, "[chuckle] Darling, in the latest version you ride the boar up the town hall steps. "
     "Ten euros says that by Friday it's a bear.", "amusement"),
    ("hafen", "jana", "zeit", 2, "[gasp] Sorry, Sir, sorry, is it true you threw the confetti cannon at the boar? Lola "
     "says yes and Chiara says don't ask, so I'm asking. Sorry.", "curiosity"),
    ("hafen", "danzel", "zeit", 2, "[clear throat] So you're the man who held the quay with a baseball bat. Three "
     "boars, they say. One boar, I say. And your jacket, if I may, was the real crime.", "amusement", NACH_TRIO),
    ("hafen", "alva", "laden", 0, "[chuckle] Look who it is, the man who saved my bar door with a stick. Your first "
     "drink is still free, o figliolu. The second one we can negotiate.", "desire"),
    ("hafen", "petru", "laden", 1, "[clear throat] Hm. They say you threw the boar into the sea. You didn't. But my boat "
     "is still blue. Sit.", "neutral"),
    ("hafen", "toto", "laden", 1, "[chuckle] Comandante! In my version I was right beside you on the quay. Behind a "
     "crate, yes, but beside you. Strategically.", "amusement"),
    ("hafen", "nonna", "laden", 2, "[laugh] So you're the one who fought three hundred rats with a broom. Sit down. A "
     "man who does that eats twice.", "amusement"),

    # ------------------------------------------------------------ Kloster San Martinu
    ("kloster", "lea", "zeit", 0, "[gasp] A lion, Duc. On Corsica. There have never been lions on Corsica, which means "
     "somebody brought one, and that's proper worse.", "fear"),
    ("kloster", "casanova", "zeit", 0, "[sniff] Monsieur. My father's spear. I gave it to you in front of everyone and I "
     "would do it again tomorrow. With better music.", "pride"),
    ("kloster", "siri", "zeit", 0, "[sigh] Sorry, I keep thinking about the monks up there. You don't have to tell me "
     "anything. I just didn't want you to think nobody asked.", "sadness"),
    ("kloster", "yasin", "zeit", 1, "[laugh] Bro. Lion hunter. Do you know what that does on a thumbnail? Don't say "
     "anything, just stand next to the spear and look tired. That's business.", "excitement"),
    ("kloster", "toto", "zeit", 1, "[chuckle] Comandante, at the harbour they say the lion was as big as a fishing boat. "
     "I said bigger. Now they believe me more than they believe you.", "amusement"),
    ("kloster", "yamamoto", "zeit", 2, "[clear throat] Officer-san, so sorry. In the village they say you wrestled the "
     "lion and the lion apologised. Very interesting. I would like a photograph of the lion. From far away.", "curiosity"),
    ("kloster", "chiara", "zeit", 2, "[sigh] Alva's version is that you carried the lion home on your back and Nonna "
     "cooked it. I give it a three. Nonna would never cook a lion, it's too tough.", "amusement"),
    # Bibi (Red Trio, ernst seit 30.10.2026): der Kloster-Loewe war Mochi - erst nach ihrer Quest, je nach Ausgang
    ("kloster", "bibi", "zeit", 0, "[sniff] You let him go. He's out there now, somewhere in the macchia, lying in the "
     "sun with nobody telling him what to do. I bet he has a lovely life. Thank you, Duc. Really.", "gratitude",
     {"alle": [NACH_BIBI, {"flag": "kl_loewe_frei"}]}),
    ("kloster", "bibi", "zeit", 0, "[sniff] I still put out his bowl in the mornings. Isn't that stupid? He was this big "
     "when I got him, and now there's nothing left to feed. I keep waiting to hear him snore.", "grief",
     {"alle": [NACH_BIBI, {"flag": "kl_loewe_erloest"}]}),
    ("kloster", "nonna", "laden", 0, "[sniff] The boy brings the harvest down every morning now, and he says your name "
     "like it belongs to a saint. Don't let it go to your head. Eat.", "caring", {"flag": "frederico_lebt"}),
    ("kloster", "nonna", "laden", 0, "[sigh] Sit. Don't talk. Some days a kitchen is only for being quiet in.",
     "sadness", {"flag": "kl_frederico_tot"}),
    ("kloster", "isabelle", "laden", 1, "[gasp] Officer! Frederico carved you a lion. It has five legs, and he says the "
     "fifth one is for luck. I said nothing. I also want one.", "joy", {"flag": "frederico_lebt"}),
    ("kloster", "alva", "laden", 1, "[laugh] Half my bar says you killed the lion and the other half says you let it "
     "go. Tell me which, o figliolu, and I'll tell you which half pays tonight.", "desire"),
    ("kloster", "rosi", "laden", 2, "[chuckle] Officer. The village says the lion followed you home and sleeps in "
     "Nonna's barn now. If that's true, I'm building it a kennel. A big one.", "excitement"),

    # ------------------------------------------------------------ Berge und Genueser Turm
    ("berge", "sophia", "zeit", 0, "[sigh] Petru walked past me at the harbour this morning and nodded. Petru doesn't "
     "nod, darling. Whatever you did up there, he's counting it.", "curiosity", NICHT_B),
    ("berge", "sophia", "zeit", 0, "[sigh] Petru's shop has been dark for two days, and nobody in the village says your "
     "name near it. I'm only telling you because nobody else will.", "sadness", {"flag": "bg_weg_b"}),
    ("berge", "maxwell", "zeit", 0, "[chuckle] Brother, you climbed the whole mountain and came down with both legs. "
     "Mr. Maximum respects that. Mr. Maximum also wants to hear about the bridge.", "admiration"),
    ("berge", "lola", "zeit", 1, "[chuckle] Mate, Alva says Petru cried. Petru! I didn't know he had water in him. "
     "Mostly salt, I reckon.", "amusement", NICHT_B),
    ("berge", "lea", "zeit", 1, "[chuckle] They're saying there's a bear up there the size of a car and you shook "
     "paws with it. Bears don't shake paws. That's proper rude of the village, to the bear.", "amusement"),
    ("berge", "siri", "zeit", 2, "[gasp] Sorry, is it true there's a black panther up there that only you can see? "
     "The baker's daughter told me. I'm scared and I also want to go.", "curiosity"),
    ("berge", "petru", "laden", 0, "[clear throat] Hm. On Sunday there is fish pie. You come. Don't bring anything.",
     "caring", {"flag": "bg_weg_c_gewonnen"}),
    ("berge", "petru", "laden", 0, "[sigh] Hm. She doesn't speak to you. She doesn't speak much to me either. Take what "
     "you need.", "sadness", {"flag": "bg_adrien_verhaftet"}),
    ("berge", "alva", "laden", 1, "[chuckle] The tower story gets better every night, o figliolu. Tonight you climbed "
     "it without a rope. Tomorrow, I think, without trousers.", "desire"),
    ("berge", "nonna", "laden", 2, "[laugh] They say you carried a soldier down the mountain over your shoulder, like "
     "a lamb. Sit down. Carrying soldiers makes a man hungry.", "amusement"),

    # ------------------------------------------------------------ Strand-Grotte (Tag 11)
    ("grotte", "toto", "zeit", 0, "[sigh] Comandante. You went in with the tide coming. Nobody does that for my family. "
     "Nobody. I don't forget things like that.", "gratitude"),
    ("grotte", "lea", "zeit", 0, "[sniff] You went past the third step. I watched the water from the deck the whole "
     "time, counting. Don't do that again. Or do, but tell me first.", "caring"),
    ("grotte", "maxwell", "zeit", 1, "[laugh] Number One goes into a cave full of smugglers and comes back with a "
     "cousin! Eish. Mr. Maximum goes to the shop and comes back with milk.", "amusement"),
    ("grotte", "rosi", "zeit", 1, "[chuckle] The village says there were rails in that cave and you rode a mine cart "
     "out of it. Officer, if there's a mine cart, I want it. For science.", "excitement"),
    ("grotte", "sophia", "zeit", 2, "[chuckle] The new version: you found the smugglers' treasure and gave all of it "
     "to the church. Ten euros says the priest believes it.", "amusement"),
    ("grotte", "alva", "laden", 0, "[sigh] Totò was in here last night and didn't make a single bet. Not one. Whatever "
     "happened in that cave, o figliolu, it got to him.", "curiosity"),
    ("grotte", "lola", "laden", 1, "[gasp] Boss! They're saying you swam out of that cave with a smuggler on your back. "
     "Don't tell anyone I told you, but I already told Chiara it was two.", "excitement"),
    ("grotte", "petru", "laden", 1, "[clear throat] Hm. My grandfather said nobody comes out of that cave with the tide. "
     "You did. So my grandfather was wrong. First time.", "neutral"),

    # ------------------------------------------------------------ Flut-Nacht (die Sirene - nie mit Namen)
    ("sirene", "sophia", "zeit", 1, "[chuckle] You came back at three in the morning, soaking wet and smelling of the "
     "sea, darling. Chiara has a theory. I have a bet.", "amusement"),
    ("sirene", "chiara", "zeit", 1, "[sigh] First Officer. You took the tender out alone, at night, against my rota. I "
     "give the idea a two. Whatever you found out there, I'm still deciding.", "annoyance"),
    ("sirene", "yasin", "zeit", 2, "[laugh] Bro, the village says there's a mermaid. If there's a mermaid and you didn't "
     "film her, we need to talk about your priorities.", "excitement"),
    ("sirene", "jana", "zeit", 2, "[gasp] Sorry, Sir. Lola says your new girlfriend is half a fish. Is it the top half "
     "or the bottom half? Sorry. Na geh, forget I asked.", "curiosity"),
    ("sirene", "petru", "laden", 0, "[clear throat] Hm. Last night there was singing from the point. My grandfather "
     "heard it once, in nineteen twenty-four. You were out there. Hm.", "neutral"),
    ("sirene", "alva", "laden", 1, "[chuckle] Somebody saw you rowing out alone at night, o figliolu. Half the village "
     "thinks you have a lover in the rocks, and the other half thinks you're mad. I'm in both halves.", "desire"),
    ("sirene", "nonna", "laden", 2, "[sigh] They say a woman sings in the sea and you sang back. My mother had a word "
     "for men who sing back. Eat first, then I'll tell you.", "amusement"),

    # ------------------------------------------------------------ Kevins Daecher (Tag 12-14)
    ("kevin", "lea", "zeit", 0, "[laugh] You got page forty back! Kevin's going to be furious, proper furious. I'm "
     "going to frame it. The page, not Kevin.", "joy"),
    ("kevin", "lola", "zeit", 0, "[chuckle] Mate, my good fork was in that nest. My good fork! Kevin's a thief and "
     "you're a hero. Mostly a hero.", "amusement"),
    ("kevin", "rosi", "zeit", 1, "[chuckle] Officer. They say you screamed at a seagull from the bell tower until the "
     "seagull left. I respect it. That's how I talk to the generator.", "amusement"),
    ("kevin", "siri", "zeit", 1, "[gasp] Sorry, the whole village watched you on the church roof? Yasin is so annoyed "
     "he missed it. I'm a little bit proud of you, actually.", "admiration"),
    ("kevin", "yamamoto", "zeit", 1, "[chuckle] Officer-san, so sorry. I have photographed this seagull for many days, "
     "and you defeated him in one afternoon. Very interesting. May I photograph you instead?", "admiration"),
    ("kevin", "maxwell", "zeit", 2, "[laugh] Brother! In the village they say the seagull challenged you to a duel and "
     "you won on points. Mr. Maximum demands a rematch. With the seagull.", "amusement"),
    ("kevin", "chiara", "zeit", 2, "[sigh] The bar says you rang the church bell with your head to scare the bird away. "
     "I give the story a nine. I give you a four.", "amusement"),
    ("kevin", "charly", "zeit", 1, "[sigh] You fought a seagull on a church. Three out of ten. The seagull was a seven.",
     "amusement", NACH_CHARLY),
    ("kevin", "alva", "laden", 0, "[laugh] You went out through my attic window and came back through it with feathers "
     "in your hair. Best thing that's happened in that attic in years, o figliolu.", "desire"),
    ("kevin", "toto", "laden", 0, "[chuckle] Comandante! My lighter! You found my lighter in the nest! I bet the whole "
     "crew it was gone forever. I lost, and I've never been so happy losing.", "joy"),
    ("kevin", "petru", "laden", 1, "[clear throat] Hm. The gull. I tried for six years. You, one afternoon. Hm.",
     "admiration"),
    ("kevin", "isabelle", "laden", 2, "[gasp] Officer! Frederico says you can talk to birds now. He wants you to tell "
     "the pigeons to stop sitting on my herbs. I want that too, honestly.", "excitement"),

    # ------------------------------------------------------------ Red Trio (Nebenquest, noch nicht gebaut)
    ("red_trio", "alva", "laden", 0, "[sigh] They say you went up into the macchia after three people in red and came "
     "back with a red jacket and no answers for anyone. Not even for me, o figliolu, and I always get the answers.", "curiosity"),
    ("red_trio", "elsa", "zeit", 1, "[clear throat] First Officer. I have three statements from the macchia on my desk. "
     "They are long, and they are honest, and I don't like any of them. Thank you for bringing them.", "gratitude",
     {"flag": "ark_aussagen_3"}),
    ("red_trio", "elsa", "zeit", 1, "[sigh] First Officer. I have one statement from the macchia on my desk. One. I have "
     "read it twice, because there is nothing else to read.", "disappointment", {"flag": "ark_aussagen_1"}),
    ("red_trio", "lola", "zeit", 2, "[laugh] Mate, the village says you beat three ninjas in red and then made them all a "
     "cup of tea. Don't tell anyone I told you, but I reckon the tea won. Mostly the biscuits.", "amusement"),
    # ------------------------------------------------------------ Dorf-Figuren (30.10.2026): warten, bis sie auftreten
    ("hafen", "pascal", "zeit", 1, "[chuckle] I told them about the boar again, Duc. It's bigger now. You're welcome. "
     "Madame says the steps have never looked so heroic.", "amusement", {"bekannt": "pascal"}),
    ("kloster", "pascal", "zeit", 0, "[sigh] Duc. I heard what you found up there. You don't have to talk about it. If "
     "you need anything for the brothers, leave it with me.", "sadness", {"bekannt": "pascal"}),
    ("berge", "pascal", "zeit", 1, "[chuckle] The village says you carried Petru's daughter down the mountain on your "
     "back. I didn't correct them. Petru didn't either, and from Petru that's a speech.", "amusement",
     {"alle": [NICHT_B, {"bekannt": "pascal"}]}),
    ("kevin", "pascal", "zeit", 2, "[laugh] Now the gull has a sword, I'm told. I've written it in the town minutes. "
     "Somebody should.", "amusement", {"bekannt": "pascal"}),
    ("hafen", "mina", "zeit", 1, "[laugh] They say you hit the boar so hard it flew over the church! I don't spread it. "
     "I just deliver it. Everywhere. Very fast.", "excitement", {"bekannt": "mina"}),
    ("kloster", "mina", "zeit", 0, "[sigh] Nonna gave me double cake this week. She never does that. So I know it was "
     "you who went up there. Thanks.", "caring", {"alle": [{"flag": "frederico_lebt"}, {"bekannt": "mina"}]}),
    ("grotte", "mina", "zeit", 1, "[chuckle] People want me to deliver letters to your smugglers' cave now. I told them "
     "no. Then I asked how much.", "amusement", {"bekannt": "mina"}),
    ("kevin", "mina", "zeit", 0, "[laugh] I saw you on the bell tower from the Vespa! You screamed at a seagull, and the "
     "seagull won on points!", "amusement", {"bekannt": "mina"}),
    ("hafen", "batu", "zeit", 2, "[clear throat] They say you fought a bear with a stick. You? So thin? Eat first. Then "
     "you tell me about the bear.", "disapproval", {"bekannt": "batu"}),
    ("kloster", "batu", "zeit", 1, "[sigh] Fiora told me what you did on the mountain, con. She doesn't say thank you, so "
     "I say it. Sit. I made too much.", "caring", {"bekannt": "batu"}),
    ("berge", "batu", "zeit", 1, "[chuckle] Petru's girl is home, and they say because of you. Good. Now I can ask her "
     "when the baby is coming.", "amusement", {"alle": [NICHT_B, {"bekannt": "batu"}]}),
    ("hafen", "sandru", "zeit", 2, "[laugh] Ha, the boar again. In my shop they say you rode it. I'd have liked to see "
     "that. I'd have liked to do that, actually.", "amusement", {"bekannt": "sandru"}),
    ("grotte", "sandru", "zeit", 1, "[laugh] Ha, sorry, people keep asking me if we sell treasure maps now. We don't. I "
     "checked the system. I checked twice.", "amusement", {"bekannt": "sandru"}),
    ("kevin", "sandru", "zeit", 1, "[chuckle] Ha. You went up the tower, the whole way up, on your own legs. Sorry. It's "
     "nice, that's all. Do you need a bag?", "sadness", {"bekannt": "sandru"}),
    ("hafen", "anghjulu", "zeit", 1, "[cough] Yes, yes, the bell was wrong that day. I was praying, my son. Very deeply. "
     "Let's talk about the boar instead.", "embarrassment", {"bekannt": "anghjulu"}),
    ("kloster", "anghjulu", "zeit", 1, "[sigh] You went up to the brothers, my son. Somebody had to. Cut the cards, will "
     "you? My hands aren't good today.", "sadness", {"bekannt": "anghjulu"}),
    ("grotte", "anghjulu", "zeit", 2, "[chuckle] They say you gave the whole smugglers' treasure to the church. I believe "
     "it, my son. I believe it very much. When does it arrive?", "amusement", {"bekannt": "anghjulu"}),
    ("kevin", "anghjulu", "zeit", 0, "[laugh] My son, you fought that devil on my tower! Fourteen years I've tried! Next "
     "time take wine up there, it helps the aim.", "joy", {"bekannt": "anghjulu"}),
]


# ------------------------------------------------------------------ Handy: "Is it true…?"
def HL(wer, ort, art="nachricht"):
    return {"anrufer": wer, "anrufer_ort": ort, "art": art}


def ZT(wer, text, gef):
    return Z(wer, klar(text), gef)


HANDY = [
    # (tat, ab Tagen, event-id, wer, ort, art, ton, titel, lage, zeilen[(text, gef)], optionen[(chip, folgen, (text, gef))])
    ("hafen", 1, "leg_hafen_elsa", "elsa", "village_harbour", "nachricht", "witzig", "For the Record",
     "A message from Elsa. No greeting.",
     [("[clear throat] First Officer. For my report about the animals in the harbour.", "neutral"),
      ("[sigh] The bar says forty rats. The mayor says two hundred. How many rats were there?", "annoyance")],
     [("“Twelve. Maybe fifteen.”", [V("elsa", 4)],
       ("[sigh] Twelve. Thank you. You are the first person in this village who has given me a number.", "gratitude")),
      ("“Two hundred. At least.”", [V("elsa", -2), W("ruf", 1)],
       ("[clear throat] I will write two hundred. Then I will write that you said it.", "disapproval")),
      ("“Ask Petru. He counts fish for a living.”", [V("elsa", 2)],
       ("[chuckle] I asked Petru. He said hm. That is his entire statement.", "amusement"))]),
    ("kloster", 1, "leg_kloster_jana", "jana", "crew_mess", "nachricht", "witzig", "The Spear",
     "Jana. Three messages, the first one starts with sorry.",
     [("[gasp] sorry sir. is it true you have a lion spear now?? 😳", "curiosity"),
      ("[sigh] coach says you'll train with it and I can watch if I'm quiet. I'm always quiet. sorry. jessas", "nervousness")],
     [("“It's a spear, Jana. Not a lion spear.”", [V("jana", 2)],
       ("[chuckle] ok. a normal spear. from a lion story. very normal 😅", "amusement")),
      ("“Come and watch. You can hold it after.”", [V("jana", 4)],
       ("[gasp] REALLY?? sorry. yes. thank you. I won't drop it. probably 🙏", "joy"))]),
    ("berge", 1, "leg_berge_lola", "lola", "galley", "nachricht", "witzig", "Bears",
     "Lola. Lots of messages, lots of emojis.",
     [("[gasp] boss is it true there's a BEAR up there 🐻🐻🐻", "excitement"),
      ("[laugh] alva says you looked it in the eye and it went home. did it go home?? does it have a home?? 😭", "curiosity")],
     [("“It went home. It has a very nice cave.”", [V("lola", 4)],
       ("[laugh] I KNEW it. I'm making it a honey cake. you're delivering it, mate 🍯", "joy")),
      ("“There was no bear, Lola.”", [V("lola", 1)],
       ("[sigh] boo. you're no fun. there was a bear in my heart 🐻", "disappointment"))]),
    ("grotte", 2, "leg_grotte_siri", "siri", "sun_deck", "nachricht", "frech", "The Cave",
     "Siri. Then a long pause. Then Siri again.",
     [("[sigh] sorry, is it true you went into the smugglers' cave? 🥺", "curiosity"),
      ("[gasp] yasin wants to film in there. I said no. I think I'm allowed to say no now? sorry", "nervousness")],
     [("“You're allowed. And don't let him go in there.”", [V("siri", 4)],
       ("[sniff] ok. I'll tell him you said it. no, I'll tell him I said it 💛", "pride")),
      ("“Tell him the tide doesn't care about followers.”", [V("siri", 2)],
       ("[laugh] I'm stealing that. sorry. I'm stealing it anyway", "amusement"))]),
    ("sirene", 1, "leg_sirene_lea", "lea", "aft_deck", "nachricht", "frech", "Human or Fish?",
     "Lea. Five messages in a row, then a sixth.",
     [("[gasp] duc. is it true you found a siren in the grotto?? a proper siren?? 🐚", "excitement"),
      ("[sigh] ok I have questions. does she breathe air or water. is there a swim bladder. is she a human or a fish. "
       "can I see her. I'll be quiet. mostly 🙏", "curiosity")],
     [("“Human. Mostly. The rest is very much fish.”", [V("lea", 4)],
       ("[laugh] mostly human is the best answer and the worst data 😭 I need to see her", "excitement")),
      ("“She's nobody's specimen, Lea.”", [V("lea", 2)],
       ("[sniff] no. you're right. sorry. I'd still like to say hello one day. just hello 🌊", "remorse")),
      ("“What siren? I was fishing.”", [],
       ("[chuckle] fishing. at three in the morning. with no rod. ok duc 🐟", "amusement"))]),
    ("kevin", 1, "leg_kevin_casanova", "casanova", "village_piazza", "video", "witzig", "My Bell Tower",
     "Madame Casanova calls. Behind her, the town hall balcony and a lot of bunting.",
     [("[clear throat] Monsieur. Three people have told me there was a man on my bell tower, screaming at a seagull.",
       "curiosity"),
      ("[sigh] I have only one question, and I want you to think about the answer. Did. You. Win?", "excitement")],
     [("“I won.”", [V("casanova", 4), W("ruf", 1)],
       ("[laugh] MAGNIFICENT! This goes into my speech for the Festa. With pauses.", "joy")),
      ("“It was a draw.”", [V("casanova", 2)],
       ("[sigh] A draw. With a seagull. I will say you won, Monsieur. Nobody checks speeches.", "amusement"))]),
]


def bauen_events():
    out = []
    for tat, tage, eid, wer, ort, art, ton, titel, lage, zeilen, opts in HANDY:
        optionen = [O(chip, list(folgen), zeile=ZT(wer, t, g)) for chip, folgen, (t, g) in opts]
        akt1 = tat == "hafen"                       # Fenster nie ueber eine Aktgrenze: Akt 1 laeuft in Akt 2 weiter
        w = WANN((2, 6) if akt1 else (8, 20), ["fruehstueck", "tag", "nachmittag", "abend"],
                 bed={"flag_seit": ["leg_" + tat, tage]})
        if akt1:
            w["akt2"] = [8, 20]
        out.append(E(eid, "handy", ton, titel, w, ORT_DUC, HL(wer, ort, art), lage,
                     [ZT(wer, t, g) for t, g in zeilen], optionen))
    return out


def daten():
    zeilen, zaehler = {}, {}
    for z in ZEILEN:
        tat, wer, wo, stufe, text, gef = z[:6]
        assert tat in TATEN and wo in ("zeit", "laden") and stufe in (0, 1, 2), z
        assert gef in GEFUEHLE, "Gefuehl %s unbekannt: %s" % (gef, text[:40])
        assert TAG.search(text), "Legenden-Zeile ohne Turbo-Tag: %s" % text
        n = zaehler[(tat, wer, wo)] = zaehler.get((tat, wer, wo), -1) + 1
        zid = "%s.%s.%s.%d" % (tat, wer, wo, n)
        zeilen[zid] = {"tat": tat, "wer": wer, "wo": wo, "stufe": stufe, "text": klar(text), "gefuehl": gef}
        if len(z) > 6:
            zeilen[zid]["wenn"] = z[6]
    return {"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\ereignisse_legenden.py - dort aendern.",
            "taten": TATEN, "familie": FAMILIE, "zeilen": zeilen}


def stimme_tags():
    out = [(z[1], klar(z[4]), " ".join(z[4].split())) for z in ZEILEN]
    for tat, tage, eid, wer, ort, art, ton, titel, lage, zeilen, opts in HANDY:
        for t, _ in zeilen + [o[2] for o in opts]:
            assert TAG.search(t), "Handy-Zeile ohne Turbo-Tag: %s" % t
            out.append((wer, klar(t), " ".join(t.split())))
    return out


def schreiben(ziel_ordner):
    json.dump(daten(), open(os.path.join(ziel_ordner, "legenden.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    pfad = os.path.join(ziel_ordner, "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "legenden"} for w, t, g in stimme_tags()]
    texte = {z["text"] for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "legenden" and z["text"] not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(ZEILEN), len(neu)


EVENTS = bauen_events()

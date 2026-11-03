# -*- coding: utf-8 -*-
r"""Tischszenen (Duc 27.10.2026, Bauplan Stern 1): die Szene beim ersten vollen "liebt" - Duc kocht das Lieblingsgericht
fuer genau eine Person (kern/tisch.py). Texte sind von Duc freigegeben (docs/abnahme/tischszenen_texte.md).

  python tisch_eden_rise.py     prueft die Zeilen und schreibt module/eden_rise/tisch.json + die Turbo-Tag-Eintraege

Je Figur: Titelkarte, Teller (normal/kritisch, nur Text), Erster Bissen und 2 Erinnerungen (vertont, mit Turbo-Tag),
Duc-Antwort (nur Text, nur bei nicht-europaeischen Gerichten). Die Rede steht hier MIT Tags ("gesprochen"); tisch.json
und der Spieltext tragen sie nie. Nicht von Hand aendern: Zeilen hier aendern, Builder laufen lassen, neu vertonen."""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HIER)))
from kern import stimme  # noqa: E402

MOD = os.path.join(os.path.dirname(os.path.dirname(HIER)), "module", "eden_rise")
ERLAUBT = {"chuckle", "clear throat", "cough", "gasp", "laugh", "shush", "sigh", "sniff"}

ZEILEN = {'lea': {'teller': {'normal': 'You set the bowl down on the bench beside the dive gear. Lea looks at the tomato broth, then at you, then at the bowl '
                              'again.',
                    'kritisch': 'The broth is the red of a Cornish sunset and the steam smells of crab and tomato. Lea has stopped moving '
                                'altogether.'},
         'erinnerung': [{'gefuehl': 'amusement',
                         'gesprochen': "Linh was Grandad Jack's partner for years. She came to Cornwall with one suitcase and a recipe book, and she "
                                       'filled the house with the smell of crab and tomato every Sunday. [chuckle] Grandad ate it with a spoon and '
                                       "pretended he'd always liked it."},
                        {'gefuehl': 'sadness',
                         'gesprochen': "I'm going to see Vietnam one day, you know. I've got a map on my wall with every reef I want to dive marked "
                                       'in pencil. [sigh] You just cooked the closest thing to being there. Thank you, Duc.'}],
         'antwort': "You tell her it's your mother's recipe, and that the secret is the shrimp paste. Lea looks at you as if you'd just handed her a "
                    'country.',
         'titel': "Bún Riêu · Lea's favourite",
         'bissen': {'gefuehl': 'joy',
                    'gesprochen': "Wait. Wait, is that bún riêu? [gasp] The crab, the tomato, the little sour bit at the end, that's Linh's! Did you "
                                  "know a crab tastes things with its legs? Linh told me that, and I think she was winding me up, but I've believed "
                                  'it ever since.'}},
 'toto': {'teller': {'normal': 'You put the plate on the crate in the storeroom, the one Totò says is for the engine room. He lifts the lid of his '
                               'lunch box to make space and stops with the lid in his hand.',
                     'kritisch': "The pork shines like polished wood and the egg is split exactly in half. Totò stops chewing a mouthful that isn't "
                                 'even there yet.'},
          'erinnerung': [{'gefuehl': 'amusement',
                          'gesprochen': "Thịt kho. [laugh] Okay, okay, I'll practise. In Napoli we have a pot like this on Sundays, pork, slow fire, "
                                        "an egg if you're lucky, but nobody ever put caramel in it. I think your mother and my mother would have "
                                        'fought about the sugar.'},
                         {'gefuehl': 'caring',
                          'gesprochen': "Nobody sold it to me, nobody stole it, nobody wrote it on a ticket. A man's mother made it, then the man "
                                        "made it for me. [chuckle] Two to one that you won't give me the real recipe. Today I am generous."}],
          'antwort': "You tell him it's thịt kho, your mother's, with the eggs boiled in the same pot. Totò repeats the name three times, badly, "
                     'with his hands.',
          'titel': "Thịt Kho · Totò's favourite",
          'bissen': {'gefuehl': 'surprise',
                     'gesprochen': "Madonna, Comandante, WHAT IS THAT?! [gasp] What did you do to the pork? It's sweet, it's salty, it's almost "
                                   "burnt and it's perfect, and I don't even know what to call it! Somebody tell me what I'm eating!"}},
 'yasin': {'teller': {'normal': 'You hand Yasin the bowl. His phone is already in his other hand, camera up, and he is already smiling at it.',
                      'kritisch': 'The egg yolk sits like a small sun on top of the rice, and every vegetable has its own corner of the bowl. Yasin '
                                  'lowers the phone without noticing.'},
           'erinnerung': [{'gefuehl': 'caring',
                           'gesprochen': 'My dad was never in Paris for long, but when he was, we went to this tiny Korean place two streets from '
                                         "our flat. He always ordered for both of us, and he always said the same thing: ‘You can't ruin a bowl.’ "
                                         '[chuckle]'},
                          {'gefuehl': 'embarrassment',
                           'gesprochen': "I wouldn't say this on camera, but that's the only meal I remember better than the food. [sniff] Anyway. "
                                         "That's business, bro. Put me down for a second helping. I'll pay you in exposure."}],
           'antwort': "You say you learned it from a neighbour who never wrote the recipe down. Yasin offers to buy it. You tell him it isn't for "
                      'sale.',
           'titel': "Bibimbap · Yasin's favourite",
           'bissen': {'gefuehl': 'surprise',
                      'gesprochen': "Bro, this is so good. Hold on, I'm filming this, my followers are going to lose it. [chuckle] No. Actually no. "
                                    'Put it away. Let me just eat this one.'}},
 'sophia': {'teller': {'normal': 'You set the plate down on the table on the aft deck, between her little brown notebook and her coffee. Sophia '
                                 "doesn't touch the notebook, which is unusual.",
                       'kritisch': 'The rice paper is so thin you can see the prawn and the mint through it. Sophia puts her pencil down very '
                                   'slowly.'},
            'erinnerung': [{'gefuehl': 'caring',
                            'gesprochen': 'Linh, Grandad Jack\'s partner, taught us to roll these at the kitchen table when Lea was small and Mum had forgotten the shopping '
                                          'again. Lea called them ‘surprise parcels’ and filled them with whatever she liked, mostly prawns and once '
                                          'a sardine. [sigh] I let her think it was a game.'},
                           {'gefuehl': 'sadness',
                            'gesprochen': "Do you know what I actually want? Nobody ever asks. [sigh] A meal I didn't have to arrange, with someone "
                                          "I didn't have to win over. This is very close to that, darling, and I'd be grateful if you didn't make a "
                                          'fuss.'}],
            'antwort': "You say it's the way your mother rolls them, with the herbs inside and not on the side. Sophia takes out her notebook, "
                       'thinks better of it, and puts it away.',
            'titel': "Summer Rolls · Sophia's favourite",
            'bissen': {'gefuehl': 'surprise',
                       'gesprochen': "Darling, these are transparent. [chuckle] And that herb mix, hold on, that's Linh's mix, the mint, the "
                                     "coriander, the little bit of perilla. Don't tell me where you learned it yet. Let me just enjoy being "
                                     'surprised.'}},
 'rosi': {'teller': {'normal': 'You carry the bowl down to the engine room and put it on the clean bench, the one she keeps free of oil. Rosi wipes '
                               'her hands twice and takes the bowl anyway.',
                     'kritisch': 'The broth is the colour of strong amber and the egg looks like it was set with a stopwatch. Rosi puts her spanner '
                                 'down without being asked.'},
          'erinnerung': [{'gefuehl': 'neutral',
                          'gesprochen': "It's like a generator running right for once. You can hear that nothing in it is fighting itself. [chuckle] "
                                        'Unit-01 would love this, if Unit-01 loved anything except diesel.'},
                         {'gefuehl': 'caring',
                          'gesprochen': 'Papa never had time to cook after the bank took the workshop. He ate standing up at the bench, a roll in '
                                        "one hand and a spanner in the other. [sigh] If he sat down for a bowl like this, he'd forget the spanner "
                                        "for ten minutes. Don't tell him I said that. And this isn't a defeat, Officer. It's a tie."}],
          'antwort': 'You say you got the broth right on the fourth try, the one you gave up on and left simmering overnight. Rosi calls it a '
                     "heretic's method and takes a second spoonful.",
          'titel': "Ramen · Rosi's favourite",
          'bissen': {'gefuehl': 'surprise',
                     'gesprochen': "That's the bowl from the manga. [gasp] The broth, the egg, the little spiral thing. I've looked at it in panels "
                                   'for years and nobody ever told me it smells like this.'}},
 'alva': {'teller': {'normal': 'You push the bowl across the bar. Alva dries a glass, puts it down, and looks at the bowl as if it had asked for a '
                               'tab.',
                     'kritisch': 'The steam stings your eyes from across the counter. Alva leans over it with her eyes half closed, the way she does '
                                 'for a good song.'},
          'erinnerung': [{'gefuehl': 'caring',
                          'gesprochen': "Papa's chalkboard behind the bar still lists what everybody in the village orders, down to the sugar. "
                                        'Nobody ever wrote what I order, because I was always the one pouring. [sigh] I forgot a plate could be a '
                                        'question somebody asked in advance.'},
                         {'gefuehl': 'amusement',
                          'gesprochen': "My mother calls every year at the end of the season and asks when I'm coming home. If she knew a man had "
                                        "cooked for me like this, she'd either hang up or book a flight. [laugh] Don't give her ideas. Sit down, eat "
                                        'the other half before it goes cold.'}],
          'antwort': "You tell her it's the noodles your mother makes when the day has been too long. Alva fans her face with the menu, asks for "
                     'water, and then for more noodles.',
          'titel': "Chilli Noodles · Alva's favourite",
          'bissen': {'gefuehl': 'surprise',
                     'gesprochen': "WHAT is that?! [cough] What's in it, o figliolu, fire? [laugh] I run the only bar in the village, I've drunk "
                                   "Papa's worst moonshine, and I've never once been surprised by a bowl of noodles."}},
 'casanova': {'teller': {'normal': "You set the tureen in the middle of the table in the mayor's office, next to the festa plans. Madame Casanova "
                                   'puts a hand on her chest as if the tureen had just made an entrance.',
                         'kritisch': 'The saffron turns the broth the colour of the late sun over the harbour. Madame Casanova goes completely '
                                     'still, which has not happened since you met her.'},
              'erinnerung': [{'gefuehl': 'neutral',
                              'gesprochen': 'My mother sat on the jury at every tasting in this village for forty years, and she always said a '
                                            'bouillabaisse is not judged by the fish. It is judged by whether the whole table goes quiet. [clear '
                                            'throat] Look at me, Monsieur. I have gone quiet.'},
                             {'gefuehl': 'sadness',
                              'gesprochen': 'There was a copper pot in the old villa on the hill, as big as a bathtub. [sigh] I could smell it again '
                                            'just now. Let us not talk about the villa. Let us talk about the festa, Monsieur!'}],
              'antwort': None,
              'titel': "Bouillabaisse · Madame Casanova's favourite",
              'bissen': {'gefuehl': 'surprise',
                         'gesprochen': 'Monsieur! [gasp] The rouille, the saffron, the little crusts floating like ships in a harbour at dusk! '
                                       'Someone applaud. No one? Fine, I will applaud myself.'}},
 'lola': {'teller': {'normal': 'You put the steamer basket down on the galley counter and lift the lid. Lola is standing very still with the wooden '
                               'spoon in her hand, the way she does when something might burn.',
                     'kritisch': "The buns come out of the steam pale and round and perfectly fluffy. Lola doesn't say a word, which is the loudest "
                                 'thing she has done all week.'},
          'erinnerung': [{'gefuehl': 'amusement',
                          'gesprochen': "Nan's ninety-one, and she once rang the coastguard because I missed a Sunday call. [chuckle] She says a bun "
                                        "only needs two things, a warm kitchen and nobody shouting. I think she's right, but don't tell her, she'd "
                                        'put it on a tea towel.'},
                         {'gefuehl': 'sadness',
                          'gesprochen': 'In that Sydney kitchen the bao were the one thing the chef let me make, and he still told me every night '
                                        "I'd never be more than a second cook. He yelled it. [sigh] You just gave me my own recipe back, and it "
                                        "tasted like a kitchen where I'm allowed to be good. Don't tell anyone I told you."}],
          'antwort': 'You say you steamed them with the lid slightly open, the way your mother did to keep the buns from collapsing. Lola squints at '
                     "you, then at the lid, and says she's stealing that.",
          'titel': "Bao Buns · Lola's favourite",
          'bissen': {'gefuehl': 'joy',
                     'gesprochen': "Boss! They're actual clouds. [laugh] You stole my line, and I'm so proud of you I could cry, and I'm only a "
                                   "little bit crying, it's the steam. Mostly the steam."}},
 'petru': {'teller': {'normal': 'You set the plate on the workbench, next to the radio that always plays Corsican football. Petru wipes his hands on '
                                'his apron, slowly, and sits down.',
                      'kritisch': 'The potato crust is golden at the edges and the steam smells of the sea and of milk. Petru takes a long time to '
                                  'pick up the fork.'},
           'erinnerung': [{'gefuehl': 'caring',
                           'gesprochen': 'Marie made it every Friday, with whatever the boats brought in. I sat at the table and said nothing, and '
                                         'she said that was my way of saying thank you. [sigh] She was right, and it took me thirty years to know '
                                         'it.'},
                          {'gefuehl': 'caring',
                           'gesprochen': "I eat it at Alva's every week now. It is good. It is not hers. [sigh] This one is not hers either, but it "
                                         'is the first one that argues with me. Hm. That means: another one.'}],
           'antwort': None,
           'titel': "Fish Pie · Petru's favourite",
           'bissen': {'gefuehl': 'neutral',
                      'gesprochen': 'Hm. [sigh] There is a bay leaf in the milk. My Marie did that. Nobody has done that in five years, and nobody '
                                    'told you, and you did it anyway. Either you are a very good cook, or the sea is being kind to you.'}},
 'chiara': {'teller': {'normal': "You put the plate on the officers' table in the crew mess. Chiara looks at it, then at the clock, then at the "
                                 "plate, like a woman checking whether it's allowed.",
                       'kritisch': 'The sauce has been simmering long enough that the whole mess smells of it. Chiara has her fork in her hand '
                                   'before she has decided to pick it up.'},
            'erinnerung': [{'gefuehl': 'amusement',
                            'gesprochen': "On Sundays my grandfather cooked this for the whole table in his captain's jacket, because he said an "
                                          "apron was for people who'd never been in a gale. [chuckle] He promised to explain the stars to me, and "
                                          'then he spent the whole Sunday explaining the sauce.'},
                           {'gefuehl': 'caring',
                            'gesprochen': "Nobody asks me what I'd cook, or what I'd do with the ship if it were mine. [sigh] You put a plate down "
                                          "and watched me eat, and I felt, I don't know, asked. … Right. Enough of that. Eat, First Officer, before "
                                          'I assign you something.'}],
            'antwort': None,
            'titel': "Spaghetti Bolognese · Chiara's favourite",
            'bissen': {'gefuehl': 'joy',
                       'gesprochen': "Nine. [gasp] No, don't look so smug, I'm not giving anyone a ten before the festa, it's a very strict scale. "
                                     "But a nine, First Officer, a proper nine. I'm rounding up because I'm hungry."}},
 'holm': {'teller': {'normal': 'You set the plate on the chart table, away from the charts. Holm takes the lid off her cold coffee, looks at the '
                               'plate, and puts the lid back.',
                     'kritisch': 'The egg sits on top, the beetroot is on the side, and the potatoes are fried exactly dark enough. Holm says '
                                 'nothing for a good while.'},
          'erinnerung': [{'gefuehl': 'caring',
                          'gesprochen': 'My mother made it on Mondays, from whatever was left of Sunday. [sigh] She said a good ship wastes nothing, '
                                        'and a good kitchen wastes less. I was eighteen before I understood she meant herself.'},
                         {'gefuehl': 'caring',
                          'gesprochen': "Eleven seasons on this ship, and nobody has put this in front of me. Takk. [clear throat] That is all I'll "
                                        "say about it, Frankfurt. Don't let it go to your head."}],
          'antwort': None,
          'titel': "Pyttipanne · Captain Holm's favourite",
          'bissen': {'gefuehl': 'neutral',
                     'gesprochen': 'Pytt i panna. [clear throat] Faen, Frankfurt. The egg is on top, the beetroot is on the side, and nobody told '
                                   "you. I'll say this once, so listen."}},
 'siri': {'teller': {'normal': 'You set the bowl down on the sun deck, in the shade of the awning. Siri takes off her sunglasses, which she never '
                               'does in front of a phone, and the phone is face down on the cushion.',
                     'kritisch': 'The soup is pale and creamy with orange pieces of salmon and green dill on top. Siri holds the bowl in both hands '
                                 'like something that might get away.'},
          'erinnerung': [{'gefuehl': 'caring',
                          'gesprochen': 'Dad made it on Fridays, when the ferry was late and nobody could leave anyway. He said soup tastes better '
                                        "when you've waited for it. [chuckle] He said the same about the ferry, but only the soup was ever true."},
                         {'gefuehl': 'sadness',
                          'gesprochen': "I haven't really talked to him in two years. I think he'd like you, which is annoying, because he doesn't "
                                        "like anyone who's met me on camera. [sigh] Sorry. I'll eat now. Sorry again. Not for the soup, for the "
                                        'speech.'}],
          'antwort': None,
          'titel': "Fiskesuppe · Siri's favourite",
          'bissen': {'gefuehl': 'surprise',
                     'gesprochen': "Oh. Oh, sorry, it's just that it smells like the kitchen at home. [sniff] Is that dill? That's dill. You put "
                                   "dill in it. Sorry, I'm being silly about soup."}},
 # Cullen Skink statt Potato and Leek Soup (Duc 28.10.2026, Familien-Muster White Fish · Potatoes · Savoury; Megan ist aus Edinburgh)
 'megan': {'teller': {'normal': "You set the bowl down on her glass-topped desk, far from the paperwork. Megan turns it by a quarter, the way she'd "
                                'turn a chess piece, and does not look at you.',
                      'kritisch': "The soup is thick and pale, with flakes of smoked haddock and a little parsley on top. Megan's hand, which was "
                                  'in the pocket with the rope, comes out empty.'},
           'erinnerung': [{'gefuehl': 'sadness',
                           'gesprochen': 'My father made this on the nights my parents had run out of things to say to each other. [sigh] He bought '
                                         "the haddock off the boats at Newhaven and cooked it on ours, because the boat was the only place they "
                                         "didn't argue. It was always exactly the same soup, and I never asked why."},
                          {'gefuehl': 'amusement',
                           'gesprochen': 'Every favour has a price, as you know. [chuckle] This one I will pay in a rare currency: I will not ask '
                                         "where you learned it. Now pass the bread, and don't look at my hands. I'm knotting something."}],
           'antwort': None,
           'titel': "Cullen Skink · Megan's favourite",
           'bissen': {'gefuehl': 'surprise',
                      'gesprochen': 'Cullen skink. … How... delightful. [cough] I want it noted that this is the only thing my stomach keeps down on '
                                    'open water, and that you found it without being told. That is either excellent intelligence or very bad luck '
                                    'for me.'}},
 'elsa': {'teller': {'normal': "You put the basket down on the desk in the coastguard post, on top of the form she's been waiting for since last "
                               'year. Elsa takes a baguette out and taps it like a witness.',
                     'kritisch': 'The crust crackles when you set the basket down, and the whole post smells of warm bread. Elsa stops mid-sentence, '
                                 'which is against her own regulations.'},
          'erinnerung': [{'gefuehl': 'amusement',
                          'gesprochen': "My Nonna bakes on Sundays for fourteen people, and I'm ‘la piccola’, so I get the heel last, or not at all. "
                                        "[sigh] Three brothers, and I have never once been given the heel. I'm a lieutenant of the coast guard, and "
                                        'I still wait for it.'},
                         {'gefuehl': 'embarrassment',
                          'gesprochen': "Chapter twelve of my current book has a bakery in it. Don't ask which book. [chuckle] That is an order, "
                                        'First Officer, and also a favour. Both. Now eat, I have a harbour to inspect.'}],
          'antwort': None,
          'titel': "Baguettes · Lieutenant Ferrandi's favourite",
          'bissen': {'gefuehl': 'joy',
                     'gesprochen': 'Lieutenant Ferrandi, official statement. [clear throat] The crust is correct, the crumb is correct, and I am not '
                                   'accepting this as a bribe. [chuckle] I am accepting it as evidence of good character.'}}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    modul = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
    fehler, szenen, neu_tags = [], {}, []
    for pid, z in ZEILEN.items():
        if pid not in modul["personen"]:
            fehler.append("%s: Figur fehlt im Modul" % pid)
            continue
        item = [i for i, it in modul["items"].items() if it.get("art") == "gericht" and (it.get("geschenk") or {}).get(pid) == 2]
        if len(item) != 1:
            fehler.append("%s: %d Lieblingsgerichte im Modul (erwartet genau 1)" % (pid, len(item)))
            continue
        out = {"item": item[0], "titel": z["titel"], "teller": z["teller"], "antwort": z["antwort"]}
        for feld, rede in [("bissen", z["bissen"])] + [("erinnerung", r) for r in z["erinnerung"]]:
            tags = stimme.TAG_MUSTER.findall(rede["gesprochen"])
            roh = [t.strip(" []") for t in tags]
            if not tags:
                fehler.append("%s.%s: kein Turbo-Tag" % (pid, feld))
            if any(t not in ERLAUBT for t in roh):
                fehler.append("%s.%s: unerlaubter Tag %s" % (pid, feld, roh))
            if "[" in stimme.ohne_tags(rede["gesprochen"]) or set('"*_~\n') & set(stimme.ohne_tags(rede["gesprochen"])):
                fehler.append("%s.%s: Anfuehrungszeichen/Sternchen/Klammer im Klartext" % (pid, feld))
            klar = stimme.vorlesen(stimme.ohne_tags(rede["gesprochen"]))
            neu_tags.append({"wer": pid, "text": klar, "gesprochen": rede["gesprochen"]})
            eintrag = {"text": klar, "gefuehl": rede["gefuehl"]}
            if feld == "bissen":
                out["bissen"] = eintrag
            else:
                out.setdefault("erinnerung", []).append(eintrag)
        szenen[pid] = out
    soll = {p for p, v in modul["personen"].items() if any((it.get("geschenk") or {}).get(p) == 2 for it in modul["items"].values()
                                                           if it.get("art") == "gericht")}
    for p in sorted(soll - set(ZEILEN)):
        fehler.append("%s hat ein Lieblingsgericht, aber keine Tischszene" % p)
    if fehler:
        sys.exit("FEHLER:\n  " + "\n  ".join(fehler))
    json.dump({"_hinweis": "Tischszenen (kern/tisch.py). Gebaut von werkzeuge/eden_rise/tisch_eden_rise.py - nicht von Hand "
                           "aendern. Figur -> Szene; Rede ohne Tags, ohne Anfuehrungszeichen. Audio: tisch.<figur>.<0|1|2>.",
               "szenen": szenen}, open(os.path.join(MOD, "tisch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pfad = os.path.join(MOD, "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    eigene = {z["text"] for z in neu_tags}
    d["zeilen"] = [z for z in d["zeilen"] if z["text"] not in eigene] + neu_tags
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Tischszenen: %d Figuren, %d vertonte Zeilen -> tisch.json, stimme_tags.json (%d Eintraege insgesamt)"
          % (len(szenen), len(neu_tags), len(d["zeilen"])))


if __name__ == "__main__":
    main()

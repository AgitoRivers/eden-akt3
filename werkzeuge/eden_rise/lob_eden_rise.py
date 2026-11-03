# -*- coding: utf-8 -*-
r"""Lob fuer Attributsteigerungen (Duc 27.10.2026): was die Crew sagt, wenn Duc ein Attribut auf 3, 4 oder 5 bringt.

    python werkzeuge\eden_rise\lob_eden_rise.py            schreibt module\eden_rise\lob.json und ergaenzt stimme_tags.json

Jede Figur schaetzt zwei Attribute (personen.<id>.schaetzt, gebaut in modul_eden_rise.py). Je Figur, Attribut und Wert
steht hier EINE feste Zeile mit Chatterbox-Turbo-Tags (mindestens ein Tag je Zeile, Duc 26.10.2026). lob.json bekommt die
Zeile ohne Tags (Anzeige, Handy), stimme_tags.json die gesprochene Fassung (Schluessel = Klartext). Regeln: kern/lob.py.
Englisch, kurze natuerliche Saetze, keine Anfuehrungszeichen/Sternchen (die Oberflaeche setzt die Anfuehrungszeichen)."""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, EDEN)
from kern import stimme  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")

ZEILEN = {
    "chiara": {
        "courage": {
            3: "You walked in there without checking the exits first. [chuckle] One point for the nerve. One point off for the exits.",
            4: "Oh, you're braver now, I can tell. Seven out of ten. [laugh] Don't let it go to your head, it's a very generous scale today.",
            5: "Nothing scares you anymore, does it? [sigh] Eight, maybe nine. Please don't make me say ten.",
        },
        "perception": {
            3: "You noticed my new earrings. Nobody notices my earrings. [gasp] Okay. Okay, that's a point.",
            4: "You see everything lately. [chuckle] Careful, First Officer. That includes the napkin swans, and those are classified.",
            5: "How did you know it was me who moved the chairs? [laugh] Don't answer. I like that you did.",
        },
    },
    "sophia": {
        "perception": {
            3: "You noticed that, didn't you? [chuckle] Most people look straight past it, darling.",
            4: "You watch a room the way I do now. [sigh] I can't decide whether to be flattered or to start locking my notebook.",
            5: "Darling, you read me from across the deck. [chuckle] Ten euros says you won't tell me what you saw. And I won't ask.",
        },
        "cunning": {
            3: "That was a tidy little move just now. [chuckle] I almost missed the angle.",
            4: "I put money on you being straightforward. [sigh] I've lost, haven't I? Splendid.",
            5: "You're playing three moves ahead and pretending you aren't. [laugh] Do carry on, darling. I'm taking notes.",
        },
    },
    "lea": {
        "empathy": {
            3: "You asked how I was and you actually waited for the answer. [sniff] Did you know most people don't wait?",
            4: "You always know when someone needs a minute, proper. [chuckle] Octopuses have three hearts, and I think you've got at least two.",
            5: "I told you something I've never told anyone, and you just listened. [sniff] Thank you. Okay. Tell me a fact so I stop crying.",
        },
        "courage": {
            3: "You stood up to them and your voice didn't even shake. [gasp] Mine would have squeaked. Proper squeaked.",
            4: "You're so brave lately that I salute you without thinking. [laugh] Sorry. I do that. Nobody asked me to.",
            5: "A great white shark is less fearless than you are. [chuckle] That's not even a fact, I just wanted to say it.",
        },
    },
    "rosi": {
        "cunning": {
            3: "That was a smart fix, Officer. [chuckle] Not as smart as mine would have been, but smart.",
            4: "You found the shortcut before I did. [sigh] That's a draw. Don't argue, it's a draw.",
            5: "You're sneakier than the old diesel, and that thing hides its faults for weeks. [laugh] I respect that. Mostly.",
        },
        "courage": {
            3: "You went in there without a plan B, didn't you? [chuckle] Stupid. Also kind of good.",
            4: "You're getting louder with your bravery, Officer. [laugh] Keep it up. I like the noise.",
            5: "Walk into the engine room like that and even Terremoto gets out of your way. [laugh] That's a compliment. Take it before I take it back.",
        },
    },
    "siri": {
        "empathy": {
            3: "You noticed I was quiet today. [sniff] Sorry. I'm not good at being noticed. It's nice.",
            4: "Sorry, am I crying? [chuckle] It's just that you listen like I'm not on camera. Does that make sense?",
            5: "Nobody has ever just stayed with me when I was sad, without trying to fix it. [sniff] You do. Thank you. I'm going to be embarrassing now.",
        },
        "charm": {
            3: "You said that so easily. [chuckle] I'd need three takes. Sorry. I'm blushing at a chair again.",
            4: "You could sell anything with that smile. [laugh] Please don't tell Yasin, he'd put you in a course.",
            5: "Okay, you're properly charming now, and it's a bit unfair. [sigh] I forget my own lines around you.",
        },
    },
    "alva": {
        "empathy": {
            3: "You listened to my whole story, even the boring part. [chuckle] Alva remembers who does that.",
            4: "Few people sit still long enough to hear what I don't say. [sigh] You do, o figliolu. Dangerous habit.",
            5: "Nobody has made me feel this heard since my mother. [sniff] Don't tell the bar. I have a reputation.",
        },
        "perception": {
            3: "You looked at my face and saw I was tired. [chuckle] Most people look at the bottle.",
            4: "You catch things in this room before I do. [sigh] That's my job, you know. Should I be worried?",
            5: "You read the whole bar in one glance. [laugh] I'd hire you, but you'd drink the profits. Or give them away.",
        },
    },
    "lola": {
        "charm": {
            3: "Alright Boss, that smile is heaps better than it was. [chuckle] Careful, I might start burning the toast.",
            4: "You could sweet-talk a dingo out of its dinner, mate. [laugh] Heaps charming. Mostly the cheese.",
            5: "I reckon half the boat's in love with you, and the other half's in the pantry pretending not to be. [laugh] Sweet as, Boss.",
        },
        "empathy": {
            3: "You noticed I was a bit off today, didn't you? [sniff] No worries, mate. It's just that nobody notices.",
            4: "You're a good listener, Boss. [chuckle] I've told you heaps of things I haven't even told the goat.",
            5: "Somebody finally sat in the galley and just let me talk. [sniff] Don't tell anyone I cried into the dough.",
        },
    },
    "megan": {
        "charm": {
            3: "Well, well. That was almost charming, Duc. [chuckle] I'll let it pass. For now.",
            4: "You've been practising, haven't you? [chuckle] I can smell it all the way from Edinburgh. A dangerous perfume, First Officer.",
            5: "How... delightful. [sigh] You're becoming dangerous, Duc. Charming men usually cost me money. Send the invoice.",
        },
        "strength": {
            3: "I hear you've been lifting things on one of my yachts. [chuckle] Good. A shark respects a fit swimmer.",
            4: "Maxwell sends me reports. [sigh] Your arms get a full paragraph now, which is more than most of my directors get.",
            5: "A strong first officer. How... delightful. [chuckle] Do try not to break my railings, though. Every one of them has a price tag.",
        },
    },
    "maxwell": {
        "strength": {
            3: "Eish, Number One! Mr. Maximum sees a muscle. [laugh] It is a small muscle, but it is a muscle.",
            4: "Lekker, brother! Mr. Maximum sees arms like a proper sailor now. [laugh] Mr. Maximum could hang a hammock off those.",
            5: "Number One, Mr. Maximum has no more lessons to give you. [sniff] Mr. Maximum is proud. Mr. Maximum is not crying, the sea is just very salty today.",
        },
        "courage": {
            3: "Shame, Number One, you went in first. [chuckle] Mr. Maximum would have gone in first too. Mr. Maximum would have screamed.",
            4: "Ja-nee, brother, that was brave. [laugh] Mr. Maximum nearly forgot to be afraid of the seagull.",
            5: "Mr. Maximum has seen many men, Number One. [sigh] Very few walk toward the noise. You walk toward the noise.",
        },
    },
    "jana": {
        "strength": {
            3: "Sorry, Sir, but you carried that crate like it was nothing. [gasp] Na geh! I mean, nice. Sorry.",
            4: "Coach says you're getting strong, Sir. [chuckle] I said it first. Well, I said it quietly. Sorry.",
            5: "Jessas, Sir, that rope would have broken me, and you just held it. [laugh] Sorry. I'm staring at your arms. I'm not staring at your arms.",
        },
        "charm": {
            3: "Sorry, Sir, what you said was really nice. [sniff] I would have said it wrong. I always say it wrong.",
            4: "You talk like Chiara does, Sir, only more... right. [chuckle] Sorry. Please don't tell Chiara I said that.",
            5: "Sir, even the door says yes to you now. [laugh] I said sorry to it earlier. It doesn't answer me. It answers you.",
        },
    },
    "toto": {
        "cunning": {
            3: "Comandante, that was a clever little trick. [chuckle] Two to one that I would have thought of it first. Today I am generous.",
            4: "Madonna, you see around corners now. [laugh] Do not look in my locker. The locker is nothing. The locker is for the engine room.",
            5: "Comandante, you are sneakier than a Neapolitan. [sigh] That is the highest compliment I have. I have never given it before.",
        },
        "strength": {
            3: "Comandante, you hauled that line without waiting for me. [chuckle] Good. One less man to call.",
            4: "Madonna, those arms! [laugh] Soon you will lift the boat and I will sell tickets.",
            5: "Two to one that you break Maxwell's record, Comandante. [laugh] The gigante is jealous. I can see it in his face.",
        },
    },
    "yasin": {
        "charm": {
            3: "Not bad, bro. Not bad. [chuckle] With a little lighting, you'd be a content creator.",
            4: "First Officer, your charm is good for the brand. [laugh] I'd put you in a course. I mean, I'd put you in a course for free.",
            5: "Bro, okay, honestly? [sigh] You're better at this than I am. Don't screenshot that. That's business.",
        },
        "cunning": {
            3: "Nice play, First Officer. [chuckle] I didn't see the angle. Which is annoying, because I always see the angle.",
            4: "You think like a trader, bro. [laugh] A good one. Mine always lose money.",
            5: "I only work with winners, First Officer. [cough] ...And apparently you're one. Annoying. That's business.",
        },
    },
    "yamamoto": {
        "perception": {
            3: "Officer-san. So sorry. [clear throat] You saw the gull before I did. Very interesting.",
            4: "Officer-san notices small things. [chuckle] In Japan we say this is a fisherman's eye. My father had it.",
            5: "Officer-san, you see the whole sea. [sigh] Thirty years in the bank, I saw only numbers. Thank you for teaching me to look.",
        },
        "courage": {
            3: "Officer-san. So sorry. [clear throat] That was brave. I would have bowed and walked away.",
            4: "Very brave. [chuckle] My daughter says I must be brave on this holiday. I think I will begin with the karaoke.",
            5: "Officer-san, you give me courage. [sniff] Tomorrow I will carry my luggage and my worries. Both. Please take care of me.",
        },
    },
}

VERBOTEN = set('"*_~\n')


def klartext(gesprochen):
    return stimme.ohne_tags(gesprochen).replace("  ", " ")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    modul = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
    fehler = []
    lob, neu_tags = {}, []
    for pid, atts in ZEILEN.items():
        soll = modul["personen"].get(pid, {}).get("schaetzt") or []
        if sorted(soll) != sorted(atts):
            fehler.append("%s: schaetzt im Modul %s, Zeilen fuer %s (erst modul_eden_rise.py bauen)" % (pid, soll, list(atts)))
        for att, stufen in atts.items():
            if sorted(stufen) != [3, 4, 5]:
                fehler.append("%s.%s: Werte %s statt 3,4,5" % (pid, att, sorted(stufen)))
            for wert, tagged in stufen.items():
                plain = klartext(tagged)
                if not stimme.TAG_MUSTER.search(tagged):
                    fehler.append("%s.%s.%d: kein Turbo-Tag" % (pid, att, wert))
                if VERBOTEN & set(plain):
                    fehler.append("%s.%s.%d: Anfuehrungszeichen/Sternchen im Text" % (pid, att, wert))
                lob.setdefault(pid, {}).setdefault(att, {})[str(wert)] = plain
                neu_tags.append({"wer": pid, "text": plain, "gesprochen": tagged})
    wer_hat = [p for p, v in modul["personen"].items() if v.get("schaetzt")]
    for p in wer_hat:
        if p not in ZEILEN:
            fehler.append("%s schaetzt Attribute, hat aber keine Lob-Zeilen" % p)
    if fehler:
        sys.exit("FEHLER:\n  " + "\n  ".join(fehler))
    json.dump({"_hinweis": "Lob fuer Attributsteigerungen (kern/lob.py). Gebaut von werkzeuge/eden_rise/lob_eden_rise.py - "
                           "nicht von Hand aendern. person -> attribut -> Wert (3/4/5) -> Zeile ohne Tags.",
               "zeilen": lob}, open(os.path.join(MOD, "lob.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pfad = os.path.join(MOD, "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    eigene = {z["text"] for z in neu_tags}
    behalten = [z for z in d["zeilen"] if z["text"] not in eigene]
    d["zeilen"] = behalten + neu_tags
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = sum(len(s) for a in ZEILEN.values() for s in a.values())
    print("Lob: %d Zeilen fuer %d Figuren -> lob.json, stimme_tags.json (%d Eintraege insgesamt)" % (n, len(ZEILEN), len(d["zeilen"])))


if __name__ == "__main__":
    main()

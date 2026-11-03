# -*- coding: utf-8 -*-
r"""Rosi spricht in ganzen Saetzen (Duc 31.10.2026, STIL.md Abschnitt 3): Telegramm-Zeilen in den Event-Buildern und ihre
Eintraege in stimme_tags.json umschreiben, Witze bleiben. Danach ereignisse_basis.py bauen und vertonen.

    rosi_fluessig.py          Probelauf: zeigt, wo jede Zeile steht
    rosi_fluessig.py --los
"""
import glob, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
TAGS = os.path.join(HIER, "..", "..", "module", "eden_rise", "stimme_tags.json")

ZEILEN = {
    "The mayor wants us on stage. In sailor costumes. Singing. She drew a picture, Officer. There's an actual picture.":
        "The mayor wants us on stage in sailor costumes, singing, and she drew a picture, Officer. There's an actual picture.",
    "I'm fine. I'm Sicilian. We don't sleep, we just close our eyes angrily for a while.":
        "I'm fine, I'm Sicilian. We don't sleep, we just close our eyes angrily for a while.",
    "I need hands here tomorrow, not on a fishing boat. But fine. Go. Abandon me.":
        "I need hands here tomorrow, not on a fishing boat. But fine, go on, abandon me.",
    "I'll cook. How hard can it be? It's just chemistry with garlic.":
        "I'll cook, how hard can it be? It's just chemistry with garlic.",
    "Or we let her see the truth. I'll make a sign. It says broken. In three languages.":
        "Or we let her see the truth. I'll make a sign that says broken, in three languages.",
    "Broken, kaputt, rotto. And a little drawing. She'll love it.":
        "Broken, kaputt, rotto, and a little drawing underneath. She'll love it.",
    "The mayor made you a crown, Officer. Out of shells. There's glitter. So much glitter.":
        "The mayor made you a crown out of shells, Officer. There's glitter on it. So much glitter.",
    "Don't. Say. Anything. Just pull me out. By the hips. No, the HIPS, Officer.":
        "Don't say anything, just pull me out. By the hips. No, the HIPS, Officer.",
    "You're staring. Good. I was starting to think you only liked the engine.":
        "You're staring, and that's good, because I was starting to think you only liked the engine.",
    "It's fixed? Good. Leave it. I don't think I'm putting it back on. Come here.":
        "It's fixed? Good, then leave it, because I don't think I'm putting it back on. Come here.",
    "Unit-01 coughed at me. COUGHED. In front of Totò. This is personal now.":
        "Unit-01 coughed at me. COUGHED, in front of Totò, so now this is personal.",
    "My nonna sang this to tractors. The tractors never died. Shh. He's listening.":
        "My nonna sang this to tractors, and those tractors never died. Shh, he's listening.",
    "It's seven. It's seven in the morning. I will throw that tuba into the sea.":
        "It's seven. It's seven in the morning, and I will throw that tuba into the sea.",
    "Hot water costs power. Power is life. Cold water builds character. You're welcome.":
        "Hot water costs power and power is life, but cold water builds character. You're welcome.",
    "Good. Fast is good. Now go away, I have a bench to christen.":
        "Good, fast is good. Now go away, I have a bench to christen.",
    "Mine has almonds. Sicilian almonds. Which means I'm more sorry. Scientifically.":
        "Mine has Sicilian almonds in it, which means I'm more sorry. Scientifically.",
    "Fine. Noon. But if the cove has a generator, I'm fixing it.":
        "Fine, noon. But if the cove has a generator, I'm fixing it.",
    "And if the Officer wins, you say Sicily is better than Napoli. On camera. Yasin, film it.":
        "And if the Officer wins, you say Sicily is better than Napoli, on camera. Yasin, film it.",
    "Tins. Cold. No oven, no hotplate marathon. Every kilowatt goes to the batteries, not to a soufflé.":
        "Cold tins, and that's all. No oven and no hotplate marathon, because every kilowatt goes to the batteries and not to a soufflé.",
    "Maestro. Ugh. For one day only. Don't get used to it. Okay, maybe a little.":
        "Maestro. Ugh. For one day only, so don't get used to it. Okay, maybe a little.",
    "You let me win. Sweet. Stupid, but sweet. Drink half.":
        "You let me win. That's stupid, but it's sweet. Drink half.",
    "Okay, I'm singing. Nobody films this. I mean it. Yasin, I mean you, wherever you are.":
        "Okay, I'm singing, but nobody films this, and I mean it. Yasin, I mean you, wherever you are.",
    "Fine. Fine! Tomorrow, same time. Not because I like it. Because the generator likes it when I'm awake.":
        "Fine. Fine! Tomorrow, same time. Not because I like it, but because the generator likes it when I'm awake.",
    "One minute, Officer. Anything I say. Don't look at me like that, I haven't decided yet. I'll decide when I win.":
        "One minute, Officer, and you do anything I say. Don't look at me like that, I haven't decided yet. I'll decide when I win.",
    "A draw. Hm. I like draws. Everyone keeps their minute. For later.":
        "A draw, so nobody won. Hm, I like draws. Everyone keeps their minute for later.",
    "There. Now you look like you know what you're doing. Don't get used to it. It's on loan.":
        "There, now you look like you know what you're doing. Don't get used to it, because it's on loan.",
    "You're keeping nothing. You can borrow it. Every day. Until I say so.":
        "You're keeping nothing. You can borrow it, every day, until I say so.",
    "…Hands steady. Good. Very good. Okay, go, Unit-01 is getting jealous.":
        "…Your hands are steady, that's good. Very good. Okay, go, Unit-01 is getting jealous.",
    "That was – I yell that. At bolts. It's not about you. Mostly.":
        "That was – I yell that, at bolts. It's not about you. Mostly.",
    "Okay. Nothing happened. Nothing happened, and I'm keeping score. Out, before Unit-01 sees us. She talks.":
        "Okay, nothing happened. Nothing happened, and I'm keeping score. Now get out before Unit-01 sees us, because she talks.",
    "Gentleman. Ugh. Fine. Thank you.":
        "Such a gentleman. Ugh. Fine, thank you.",
    "Officer. Good, you're here. Hold the torch and don't touch anything, and I mean anything, it's a delicate moment for her.":
        "Officer, good, you're here. Hold the torch and don't touch anything, and I mean anything, it's a delicate moment for her.",
    "She's been coughing since Tuesday. Nobody else hears it. I hear it.":
        "She's been coughing since Tuesday, and nobody else hears it. I hear it.",
    "She will. And I'll still be here tomorrow. Go to bed, Officer. I've got her.":
        "She will, and I'll still be here tomorrow. Go to bed, Officer, I've got her.",
    "The bilge pump yesterday. That was yours. I'm a fair person, I write it down.":
        "The bilge pump yesterday, that one was yours. I'm a fair person, so I write it down.",
    "A crown. Okay. That's – you can't just be nice in the middle of a rivalry, it's against the rules. Give me the marker.":
        "A crown. Okay, that's – you can't just be nice in the middle of a rivalry, it's against the rules. Give me the marker.",
    "You counted wrong. I'll recount. Out loud. With feeling. Sit down, this will take a while.":
        "You counted wrong, so I'll recount, out loud and with feeling. Sit down, this will take a while.",
    "Hm. No speech. Good. I hate speeches.":
        "Hm, no speech. Good, I hate speeches.",
    "That was – a quality check. Of the cloth. I mean the thumb. It's a very good thumb.":
        "That was – a quality check of the cloth. I mean the thumb. It's a very good thumb.",
    "It does. Everything comes with the job. Drink your coffee.":
        "It does, everything comes with the job. Drink your coffee.",
    "Fine. Use the napkin. The napkin's never been under a generator, but sure.":
        "Fine, use the napkin. The napkin's never been under a generator, but sure.",
    "This isn't ours. This isn't anybody's on this boat. Somebody soldered it into him. Neat work. Better than mine.":
        "This isn't ours, and it isn't anybody's on this boat. Somebody soldered it into him, and it's neat work. Better than mine.",
    "I know that logo from somewhere. I don't know where. I hate that.":
        "I know that logo from somewhere, but I don't know where, and I hate that.",
    "Fine. One line on the whiteboard for you. Only one.":
        "Fine, one line on the whiteboard for you, but only one.",
}
TAG = re.compile(r"\s*\[[a-z ]+\]")


def builder_suchen():
    """Datei -> Liste alter Zeilen, die dort stehen. Die Zeilen koennen im Builder auch umgebrochen sein: dann meldet der Probelauf sie."""
    treffer = {}
    for p in glob.glob(os.path.join(HIER, "*.py")):
        if p.endswith("_fluessig.py"):
            continue
        s = open(p, encoding="utf-8", newline="").read()
        for alt in ZEILEN:
            if muster(alt).search(s):
                treffer.setdefault(p, []).append(alt)
    return treffer


def muster(alt):
    """Die Zeile kann im Builder auf zwei Stringstuecke umbrochen sein."""
    return re.compile(r' (?:"\s*\r?\n\s*")?'.join(re.escape(w) for w in alt.split(" ")))


def neu_mit_tag(gesprochen, neu):
    """Die Tags der alten Fassung nach dem ersten Satzende der neuen setzen (sonst ans Ende)."""
    tags = [t.strip() for t in TAG.findall(gesprochen)]
    if not tags:
        return neu
    m = re.search(r"[.!?…](?=\s)", neu)
    if not m:
        return neu + " " + " ".join(tags)
    return neu[:m.end()] + " " + " ".join(tags) + neu[m.end():]


def main():
    los = "--los" in sys.argv
    treffer = builder_suchen()
    gefunden = {a for L in treffer.values() for a in L}
    for p, L in sorted(treffer.items()):
        print(os.path.basename(p), len(L))
    fehlt = [a for a in ZEILEN if a not in gefunden]
    print("nicht im Builder gefunden:", fehlt)
    if not los:
        return
    assert not fehlt
    for p, L in treffer.items():
        s = open(p, encoding="utf-8", newline="").read()
        for alt in L:
            s = muster(alt).sub(lambda m: ZEILEN[alt], s)
        open(p, "w", encoding="utf-8", newline="").write(s)
    d = json.load(open(TAGS, encoding="utf-8"))
    n = 0
    for z in d["zeilen"]:
        if z["text"] in ZEILEN:
            neu = ZEILEN[z["text"]]
            z["gesprochen"] = neu_mit_tag(z.get("gesprochen", ""), neu)
            z["text"] = neu
            n += 1
    json.dump(d, open(TAGS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Builder geaendert:", len(treffer), "Tag-Eintraege:", n)


if __name__ == "__main__":
    main()

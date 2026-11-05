# -*- coding: utf-8 -*-
"""Akt 3, Paket C: Zeugen ("Who Saw It?") und Festa-Lose. Drehbuch docs/wiki/welt/drehbuch_akt3.md, Abschnitte 2, 4.2, 4.3.

Zeugen: Die Dank-Szenen (ereignisse_akt3_woche4.py) fragen Mina, Ba Tu, Alva und Petru, sobald ihr Haus steht. Wer kein
abgebranntes Haus hat oder die Frage verschoben hat, wird ueber die Karte "Who Saw It?" gefragt (eine Phase). Jede der drei
Haltungen ueberzeugt; sie faerbt nur die Aussage (a3_zeuge_<pid>_<haltung>) und das Vertrauen. Die Tuer muss offen sein:
  Petru  Haus fertig oder bl_tueren_petru oder Werkstatt heil     Mina   Haus fertig oder bl_tueren_mina oder Post heil
  Ba Tu  bl_batu_norden oder Haus fertig oder Laden heil          Alva   a3_alva_wach und (Bar fertig oder Bar heil)
  Don    an der Tuer neben ihm (a3_zeuge_tuer_don) oder Vertrauen 3 oder das Los The Bell
  Casanova  Elsas Berichte gehoert und richtig geantwortet (a3_zeuge_tuer_casanova)
  Sandru (Schiene, Paket D) und Buenaventura (immer, er meldet sich selbst) laufen ueber ihre eigenen Szenen.
Lose: Casanovas Tafel (Karte "The Festa Board", eine Phase je Los). 8 Lose ab der Tafel (Tag 26), 5 weitere nach dem ersten
fertigen Haus. Jedes Los ist eine Szene mit genau einer Person, ihrem Talent und einer Entscheidung, kein Zaehler.
Ergebnis a3_los_<id> und a3_los_<id>_<wahl>, die Festa (Paket F) stellt es ins Schlussbild. Bauen-Lose geben eine Stufe."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import FR, FL, NICHT, DA, AKT3, JE, tags_fuer  # noqa: E402

WEITER = lambda ziel: {"weiter": ziel}
STUFE = {"aufbau_stufe": "*"}
HAUS_OK = lambda hid: {"eine": [{"nicht": FL("tk_haus_weg_" + hid)}, FL("aufbau_fertig_" + hid)]}

# ------------------------------------------------------------------ Zeugen
TUER = {
    "petru": {"eine": [FL("aufbau_fertig_werkstatt"), FL("bl_tueren_petru"), NICHT(FL("tk_haus_weg_werkstatt"))]},
    "mina": {"eine": [FL("aufbau_fertig_post"), FL("bl_tueren_mina"), NICHT(FL("tk_haus_weg_post"))]},
    "batu": {"alle": [{"eine": [FL("bl_batu_norden"), FL("aufbau_fertig_batu"), NICHT(FL("tk_haus_weg_batu")), FL("a3_mast_aus")]},
                      {"eine": [NICHT(FL("a3_mast_an")), FL("aufbau_fertig_batu")]}]},          # The Red Light: der Mast faerbt ihren Mut
    "alva": {"alle": [FL("a3_alva_wach"), HAUS_OK("bar")]},
    "anghjulu": {"eine": [FL("a3_zeuge_tuer_don"), {"wert": ["vertrauen.anghjulu", ">=", 3]}, FL("a3_los_glocke")]},
    "casanova": FL("a3_zeuge_tuer_casanova"),
}
ZEUGEN = list(TUER)


def _frage_offen(pid):
    return {"alle": [TUER[pid], NICHT(FL("a3_zeuge_" + pid))]}


def _weiter_zeuge(pid):
    i = ZEUGEN.index(pid)
    rest = ZEUGEN[i + 1:] + ZEUGEN[:i]
    return WEITER([{"wenn": _frage_offen(p), "id": "a3_frage_" + p} for p in rest] + [{"id": "a3_frage_" + pid}])


def ZEUGE(pid, bild, titel, lage, zeilen, haltungen, sets=None):
    """haltungen: [(chip, kurz, vertrauen, antwort-Zeile)] - jede ueberzeugt."""
    opt = [O(chip, [F("a3_zeuge_" + pid), F("a3_zeuge_%s_%s" % (pid, kurz)), V(pid, n)], zeile=z) for chip, kurz, n, z in haltungen]
    opt.append(O("Leaves it for today and goes to someone else.", [_weiter_zeuge(pid)]))
    return FR("a3_frage_" + pid, bild, titel, lage, zeilen, opt, personen={"handelnd": pid, "betroffen": []}, sets=sets, ton="ernst")


FRAGEN = [
    ZEUGE("petru", "petru_workshop", "Who Saw It? Petru",
          "Petru is mending a net in front of his workshop. He doesn't look up, but he moves over on the bench.",
          [G("petru", "[clear throat] The commission. You want me to sign my name. My father signed his name once, for a bank. They took his boat.", "neutral"),
           G("petru", "[sigh] Now A.V. has the loan on mine. So tell me why I should sign.", "neutral")],
          [("“Because you saw it, and they need someone who saw it.”", "ehrlich", 6, G("petru", "[sigh] That's a reason. A good one. Marie would like it.", "approval")),
           ("“Because if you don't, they'll buy the next boat too.”", "kalt", 2, G("petru", "[clear throat] That's also a reason. A worse one. But true, like a cold wind.", "neutral")),
           ("Sits down and mends the net with him until he answers.", "still", 4, G("petru", "[sigh] ...I'll sign.", "neutral"))]),
    ZEUGE("mina", "village_piazza", "Who Saw It? Mina",
          "Mina is sitting on the post office steps with her bag on her knees. The letters from Monaco are on top.",
          [G("mina", "[sigh] I carry their letters, Yacht. A.V.'s letters. If I talk, maybe they find another postwoman. "
                     "The day the phones were dead, I knocked on every door. Do I tell the men from Ajaccio?", "nervousness")],
          [("“Yes. You saw more than anyone that day.”", "ehrlich", 6, G("mina", "[sniff] More than anyone. Okay. I'll tell them.", "pride")),
           ("“Only if you want to. It's your name, not mine.”", "frei", 4, G("mina", "[sigh] Nobody asked me that before. I want to.", "gratitude")),
           ("“Nobody can replace you, Mina. Who else knows every door?”", "lob", 4, G("mina", "[chuckle] Nobody. That's true. Okay.", "pride"))]),
    ZEUGE("batu", "batu_shop", "Who Saw It? Bà Tư",
          "Bà Tư is cutting vegetables, very fast. There is already a bowl in front of your seat.",
          [G("batu", "[clear throat] Eat first. ...The men in white asked me twice for the north road. Alon's workers buy my rice. "
                     "If I talk, maybe they stop. Do I talk, con?", "neutral")],
          [("“Yes. You told me first. Now tell them.”", "ehrlich", 6, G("batu", "[chuckle] Good. My mother was afraid of nobody. Me too.", "pride")),
           ("“Yes. And the crew will buy your rice, all of it.”", "kauf", 2, G("batu", "[laugh] All of it? You can't eat all of it. ...Okay. I talk.", "caring")),
           ("Eats everything in the bowl first.", "still", 4, G("batu", "[sigh] Good boy. Now I talk.", "caring"))]),
    ZEUGE("alva", "alvas_bar", "Who Saw It? Alva",
          "Alva is wiping the bar that is already clean.",
          [G("alva", "[sigh] From the square I saw the north barricade open. Then the men in white came through. "
                     "I was knocked out after, so nobody believes me. Why would the men from Ajaccio?", "anger")],
          [("“Because I believe you. And I'll stand next to you.”", "ehrlich", 6, G("alva", "[sigh] Then I'll say it. Papa always said: a bar is where people tell the truth. So I will too.", "pride")),
           ("“Because you're the only one who saw the north side.”", "fakt", 4, G("alva", "[chuckle] The only one. I like that. Fine.", "pride")),
           ("“Say it the way you'd tell your father, if he were still behind the bar.”", "papa", 4, G("alva", "[sniff] ...Papa would say: tell them, and then pour them a drink. Okay.", "sadness"))]),
    ZEUGE("anghjulu", "church", "Who Saw It? Don",
          "Don is sitting in the first row, next to the bucket. It is still dripping.",
          [G("anghjulu", "[sigh] I saw the gate open, my son. But a priest hears many things he can't repeat. If I talk, people think I talk "
                         "about the confessions too. What do I say?", "sadness")],
          [("“Only what you saw with your own eyes. Not one word more.”", "ehrlich", 6, G("anghjulu", "[sigh] Only my eyes. Not my ears. Yes. That I can do.", "relief")),
           ("“The village needs to hear it from you, Father.”", "dorf", 4, G("anghjulu", "[clear throat] From me. God help us. ...Yes.", "neutral")),
           ("Moves the bucket so it drips somewhere else, and waits.", "still", 4, G("anghjulu", "[chuckle] Thank you. Yes, I will talk.", "gratitude"))],
          sets={"anghjulu": "anghjulu_standard"}),
    ZEUGE("casanova", "village_piazza", "Who Saw It? Madame Casanova",
          "Madame Casanova is standing in front of her festa board. She is not looking at it.",
          [G("casanova", "[sigh] Every night, Alon's people left a letter on my church steps, the ones in that neat handwriting. I kept all of them. If I give it to the commission, "
                         "they will also read my name in Pascal's book. Do I do it, Monsieur?", "nervousness")],
          [("“Yes. The truth is better from you than from his book.”", "ehrlich", 6, G("casanova", "[sigh] From me. Yes. ...You are right, and I hate it.", "neutral")),
           ("“Yes. A mayor who signed nothing for Alon can say so.”", "stolz", 4, G("casanova", "[clear throat] I signed nothing for him. Write that down.", "pride")),
           ("“Do it for the festa. For the board you built.”", "festa", 2, G("casanova", "[sniff] For the festa. ...That is a terrible reason. Yes.", "embarrassment"))]),
]

# ------------------------------------------------------------------ Lose (Casanovas Tafel)
WELLE1 = ["tafel", "buehne", "topf", "menue", "fang", "getraenk", "girlande", "glocke"]
WELLE2 = ["lichter", "system", "garten", "kleider", "bilder"]
LOSE = WELLE1 + WELLE2
ERSTES_HAUS = {"eine": [FL("aufbau_fertig_" + h) for h in ("post", "batu", "bar", "werkstatt")]}
EXTRA = {   # zusaetzliche Bedingung, damit ein Los an der Tafel haengt
    "menue": DA("lola"),
    "lichter": {"eine": [FL("a3_scrap_field"), FL("a3_villa_keller")]},
    "system": FL("a3_alva_wach"),
    "kleider": FL("danzel_festa_auftrag"),
    "bilder": FL("bl_kirche_jana"),
}


def los_offen(lid):
    b = [FL("a3_festa_tafel"), NICHT(FL("a3_los_" + lid))]
    if lid in WELLE2:
        b.append(ERSTES_HAUS)
    if lid in EXTRA:
        b.append(EXTRA[lid])
    return {"alle": b}


# Rundgang (Umbau nach dem Review, 04.11.2026): eine Phase an der Tafel = bis zu drei Lose hintereinander. Nach jedem Los
# fragt der Frame a3_los_weiter, ob Duc weitergeht. ort_schritte zaehlt die Frames dieses Ausflugs (Los + Pause = 2).
RUNDGANG_MAX = 3
BESUCH = {   # Lose, die auch beim Besuch der Person kommen, ohne Phase (kern/akt3.los_besuch, eden.py)
    "tafel": "petru", "getraenk": "alva", "fang": "angeln", "topf": "kochen", "menue": "kochen", "garten": "nonna",
}


def _weiter_los(lid=None):
    """Zum naechsten offenen Los, solange der Rundgang noch Platz hat, sonst zum Abschied."""
    platz = {"ort_schritte": ["<", 2 * RUNDGANG_MAX - 1]}
    return WEITER([{"wenn": {"alle": [platz, los_offen(l)]}, "id": "a3_los_" + l} for l in LOSE if l != lid] + [{"id": "a3_los_genug"}])


def LOS(lid, wer, bild, titel, lage, zeilen, wahlen, bauen=False, sets=None, danach=None, personen=None):
    """wahlen: [(chip, kurz, antwort-Zeile)] - 2 oder 3; die letzte Option geht zum naechsten Los."""
    opt = []
    for chip, kurz, z in wahlen:
        nach = danach or "a3_los_weiter"                    # danach: [{"wenn": ..., "id": zweiter Takt}] vor dem Rundgang
        fo = [F("a3_los_" + lid), F("a3_los_%s_%s" % (lid, kurz)), V(wer, 4)] + ([STUFE] if bauen else []) + [WEITER(nach)]
        if danach:
            fo.append({"direkt": [x for x in danach if x["id"] != "a3_los_weiter"]})   # beim Besuch (ohne Ausflug) zaehlt direkt
        opt.append(O(chip, fo, zeile=z))
    opt.append(O("Leaves this one for another day.", [_weiter_los(lid)]))
    return FR("a3_los_" + lid, bild, titel, lage, zeilen, opt, personen=personen or {"handelnd": wer, "betroffen": []}, sets=sets)


LOS_FRAMES = [
    LOS("tafel", "petru", "petru_workshop", "The Long Table",
        "The board says: Petru · wood · a table for the whole village. At the back of the workshop, on blocks, lies a small blue boat with "
        "a name on the bow: Stella. There is dust on her seats. In front of the workshop: a pile of black beams from the burned houses.",
        [G("petru", "[clear throat] Stella was Marie's boat. She went out with her every morning, for thirty years. Since Marie died, "
                    "Stella hasn't touched the water. My own boat is the green one at the quay.", "sadness"),
         JE(G("holm", "[clear throat] Five years on blocks, Frankfurt. A boat that doesn't swim is only a cupboard.", "neutral"), "holm", FL("holm_zurueck")),
         G("petru", "[sigh] Maybe it's time she held something again. Or the beams from the fire. Which one?", "neutral")],
        [("“Stella. Let her hold the whole village.”", "boot", G("petru", "[sniff] Marie would like that. She always fed too many people.", "sadness")),
         ("“The burned beams. Let the fire turn into a table.”", "asche", G("petru", "[clear throat] Black wood makes a good table. Stella stays on her blocks. For now.", "approval"))],
        bauen=True, danach=[{"wenn": FL("holm_zurueck"), "id": "a3_los_tafel_holm"}, {"id": "a3_los_weiter"}],
        personen={"handelnd": "petru", "betroffen": [{"id": "holm", "ton": "?", "was": "holds the saw"}]}),
    LOS("buehne", "bonaventure", "village_piazza", "The Stage",
        "The board says: Buenaventura · carrying stones · a stage. Forty pirates wait with their hats in their hands.",
        [G("bonaventure", "[clear throat] Señor, where do we build it? Where the fire was, or where the people are?", "neutral")],
        [("“In front of the post office. Where the fire was.”", "post", G("bonaventure", "[sigh] Where the fire was. Yes. That is right.", "remorse")),
         ("“In front of the church. Where the people are.”", "kirche", G("bonaventure", "[laugh] Where the people are! A pirate likes an audience.", "pride"))],
        bauen=True),
    LOS("topf", "batu", "batu_shop", "The Pot",
        "The board says: Bà Tư · cooking too much · the big pot. Bà Tư already has the biggest pot in Corsica on the fire.",
        [G("batu", "[chuckle] For the festa I cook too much. Like always, but bigger. My way, or your mother's way, con?", "caring")],
        [("“Your way. Always your way.”", "batu", G("batu", "[laugh] Smart boy. My way.", "amusement")),
         ("“My mother's way. I'll tell you how she made it.”", "mutter", G("batu", "[sniff] Tell me. We cook it together. For her.", "caring"))]),
    LOS("menue", "lola", "batu_shop", "The Menu",
        "The board says: Lola · cooking · the grill. Lola has written a menu on her arm because she ran out of paper.",
        [JE(G("lola", "[laugh] I've been in every kitchen in this village, Boss. Mostly for the biscuits. Who tastes it first?", "joy"), "lola", FL("bl_tueren_lola")),
         JE(G("lola", "[laugh] Boss! The festa menu. Who tastes it first?", "joy"), "lola", None)],
        [("“Bà Tư. If she says yes, it's perfect.”", "batu", G("lola", "[gasp] Scary. Good. Scary good.", "nervousness")),
         ("“Madame Casanova. It's her festa.”", "casanova", G("lola", "[chuckle] She'll give it a speech. A long one.", "amusement")),
         ("“Me. Right now.”", "duc", G("lola", "[laugh] Open wide, Boss. It's hot. Sorry!", "joy"))],
        sets={"lola": "Galley"}),
    LOS("fang", "bonaventure", "village_harbour", "The Catch",
        "The board says: Buenaventura's men · fishing · the grill at the harbour. The Eventually is ready to go out.",
        [G("bonaventure", "[clear throat] Señor. The reef, with many small fish? Or the open sea, with one big fish, if you can catch it?", "neutral")],
        [("“The reef. Enough for everyone.”", "riff", G("bonaventure", "[chuckle] Many small fish. Like my crew.", "amusement")),
         ("“The open sea. I'll catch the big one myself.”", "meer", G("bonaventure", "[laugh] Ha! The Señor fishes! I want to see this.", "joy"))]),
    LOS("getraenk", "alva", "alvas_bar", "The Festa Drink",
        "The board says: Alva · the bar · a drink for every table.",
        [G("alva", "[chuckle] Papa's recipe, with the berries from the hill? Or a new one? If it's new, you give it a name.", "curiosity")],
        [("“Papa's recipe.”", "papa", G("alva", "[sniff] Papa's. He'd like that. Don't watch me while I make it.", "sadness")),
         ("“A new one. We name it after the pirates' boat, The Eventually.”", "eventually", G("alva", "[laugh] The pirates will cry. Good.", "amusement")),
         ("“A new one. We call it 'Fresh Bread', for Sandru's bread.”", "brot", G("alva", "[chuckle] Fresh Bread. ...Sandru will know why. Fine.", "embarrassment"))],
        sets={"alva": "alva_standard"}),
    LOS("girlande", "mina", "village_piazza", "The Garland",
        "The board says: Mina · letters · a garland over the street. Mina has a box of post that nobody can deliver.",
        [G("mina", "[sigh] Letters for people who moved away. Or who aren't here any more. Shall I hang them up over the street?", "neutral")],
        [("“Yes. All of them.”", "alle", G("mina", "[chuckle] All of them. Even the ones from Monaco in that neat handwriting. Let them hang.", "amusement")),
         ("“Yes, but not Pascal's post.”", "ohne", G("mina", "[sigh] Okay. His letters stay in the box.", "neutral")),
         ("“No. Flowers. Letters are for reading.”", "blumen", G("mina", "[chuckle] Flowers. You sound like my mother.", "amusement"))]),
    LOS("glocke", "anghjulu", "church", "The Bell",
        "The board says: Don · the bell · ringing for the dance. The bell is cracked and rings in the wrong rhythm. Don has a pack of cards.",
        [JE(G("anghjulu", "[chuckle] You let me stay sober once already, at the church door, the night of the siege. Twice is a habit. "
                          "Cards instead of wine, my son. Shall I win tonight, or will you?", "amusement"), "don", FL("bl_kirche_don")),
         JE(G("anghjulu", "[chuckle] Cards instead of wine, my son. We play until the bell is fixed. Shall I win tonight, or will you?", "amusement"), "don", None)],
        [("Plays to win.", "gewinnen", G("anghjulu", "[laugh] You cheat like a fisherman. I like it.", "amusement")),
         ("Lets him win.", "verlieren", G("anghjulu", "[sigh] You let me win. I saw it. Thank you.", "gratitude")),
         ("“Nobody wins. We play until the bell is fixed.”", "niemand", G("anghjulu", "[chuckle] Then we play all night. Good.", "joy"))],
        sets={"anghjulu": "anghjulu_standard"}),
    LOS("lichter", "rosi", "village_piazza", "The Lights",
        "The board says: Rosi · machines · lights over the square. Rosi has a box of cables and the steel from the scrap field.",
        [JE(G("rosi", "[clear throat] What goes in the switch, Officer? A chip from one of the robots you beat, or a piece of Alon's collars?", "curiosity"), "rosi", DA("rosi")),
         JE(G("maxwell", "[clear throat] Rosi says on the video: a chip from one of the robots you beat, or a piece of Alon's collars? Mr. Maximum holds the screwdriver.", "neutral"), "rosi", None)],
        [("Gives her a chip from one of the robots he beat.", "chip", G("rosi", "[gasp] A robot chip? ...White light. Thank you, Officer.", "surprise")),
         ("“A piece of the collars. Let his light shine for us.”", "halsband", G("rosi", "[laugh] Amber, like Unit-01's eye. I love it.", "joy"))],
        sets={"rosi": "Engine Room"}),
    LOS("system", "sandru", "av_market", "Not in the System",
        "The board says: Sandru · his mother's recipes · a table of sweets. Sandru has a tin box with gazelle horns, little almond cakes, and chebakia with honey.",
        [G("sandru", "[laugh] Ha. My mother's tin. Do I sell these at the market, under Alon's sign, or only at the festa?", "nervousness")],
        [("“At the market. Let them see what's not in their system.”", "markt", G("sandru", "[chuckle] Not in the system. Ha. They'll count it.", "pride")),
         ("“Only at the festa. These are for us.”", "festa", G("sandru", "[sigh] For us. Yes. Better.", "relief"))],
        sets={"sandru": "sandru_av"}),
    LOS("garten", "nonna", "monastery_garden_dusk", "The Garden",
        "The board says: Nonna and Isabelle · the garden · herbs for the tables. Isabelle has already filled three baskets.",
        [G("nonna", "[clear throat] Who gets the first basket? Tell me, before Isabelle gives them all away.", "neutral")],
        [("“The long table.”", "tafel", G("nonna", "[chuckle] For everyone. Good answer.", "approval")),
         ("“Bà Tư's pot.”", "topf", G("nonna", "[chuckle] Ah. She'll say it's too much. It's never too much.", "amusement")),
         ("“Don Anghjulu. For the church steps.”", "kirche", G("nonna", "[chuckle] For the church. Don will say he doesn't like basil. He likes it.", "amusement"))],
        sets={"nonna": "nonna_standard"}),
    LOS("kleider", "danzel", "village_piazza", "The Dresses",
        "The board says: Danzel · sewing · the festa dresses. Danzel stands in his shop with pins in his mouth.",
        [JE(G("danzel", "[clear throat] Chiara's dress is finished. Hem, darts, all of it. Whose dress next? I can finish one more in time, if nobody talks to me.", "neutral"), "danzel", FL("chiara_festa_kleid")),
         JE(G("danzel", "[gasp] Whose dress first? I can only finish one in time!", "nervousness"), "danzel", None)],
        [("“One of the women from the crew. You choose who.”", "crew", G("danzel", "[clear throat] I choose. Good. I always choose right.", "pride")),
         ("“Madame Casanova. She wears the same dress every year.”", "casanova", G("danzel", "[gasp] The mayor! Red. It has to be red.", "excitement"))]),
    LOS("bilder", "jana", "church", "The Pictures",
        "The board says: Jana · the children · pictures for the festa. Jana has a pile of drawings from behind the church door.",
        [G("jana", "[chuckle] Sir, the children made these for the festa. Where do I hang them?", "joy")],
        [("“On the church door.”", "tuer", G("jana", "[sniff] On the door they hid behind. That's nice.", "caring")),
         ("“On the stage. Everybody should see them.”", "buehne", G("jana", "[laugh] Everybody! They'll be so proud.", "joy"))],
        sets={"jana": "jana_deck_a"}),
]

TAFEL_HOLM = [
    FR("a3_los_tafel_holm", "petru_workshop", "The Long Table",
       "Holm holds the other end of the saw. Halfway through, she stops and looks at the sea through the open door.",
       [G("holm", "[clear throat] Frankfurt. Thirty-four years at sea. Eleven seasons on the Eden Rise. My mother in Ålesund is old. "
                  "And I sleep well here. Better than on any bridge.", "neutral"),
        G("holm", "[sigh] I say things once, Frankfurt. So listen. These four stripes on my shoulders. "
                  "Do I keep them, or do they go in the table?", "nervousness")],
       [O("“Put them in the table. You can stay.”", [F("a3_los_tafel_holm"), F("a3_los_tafel_holm_streifen"), V("holm", 6), WEITER("a3_los_weiter")],
          zeile=G("holm", "[sigh] Faen. ...Takk. Petru, give me a nail.", "relief")),
        O("“Keep them. One more season, then decide.”", [F("a3_los_tafel_holm"), F("a3_los_tafel_holm_saison"), V("holm", 4), WEITER("a3_los_weiter")],
          zeile=G("holm", "[clear throat] One more. Then we see. That's an honest answer, Frankfurt.", "neutral")),
        O("“Don't ask me. Ask Petru.”", [F("a3_los_tafel_holm"), F("a3_los_tafel_holm_petru"), V("holm", 4), V("petru", 4), WEITER("a3_los_weiter")],
          zeile=G("petru", "[clear throat] Stay.", "love"))],
       personen={"handelnd": "holm", "betroffen": [{"id": "petru", "ton": "+", "was": "waits"}]}, sets={"holm": "holm_shirt"}),
]

RUNDGANG = [
    FR("a3_los_weiter", "village_piazza", "The Festa Board",
       "You walk back past the board. Madame Casanova crosses one more name off with a red pencil.",
       [G("casanova", "[clear throat] Good. Who's next, Monsieur? Or is that enough for today?", "neutral")],
       [O("Walks on to the next name on the board.", [_weiter_los()]),
        O("“That's enough for today.”", [])],
       personen={"handelnd": "casanova", "betroffen": []}),
    FR("a3_los_genug", "village_piazza", "The Festa Board",
       "The sun is lower now. The board is still there, and so are the names.",
       [G("casanova", "[chuckle] Tomorrow, then. The festa doesn't build itself. ...Well. Sometimes it does. That is the miracle of a festa.", "amusement")],
       [O("Goes home.", [])],
       personen={"handelnd": "casanova", "betroffen": []}),
]

CAPRA = [
    E("a3_los_capra", "gag1", "witzig", "Capra", WANN((26, 34), ["tag", "nachmittag"], bed={"alle": [AKT3, FL("a3_festa_tafel"), FL("rt_bibi_bleibt"), FL("mochis_offen")]}),
      "village_piazza", P1("bibi", ("casanova", "-", "sees the goat")),
      "Bibi comes across the square with a goat on a rope. The goat is wearing a flower crown and eating it.",
      [G("bibi", "[laugh] Capra wants to come to the festa. Do we let her?", "joy"),
       G("casanova", "[gasp] A goat. At my festa.", "surprise")],
      [O("“Yes. She's family now.”", [F("a3_los_capra"), F("a3_los_capra_ja"), V("bibi", 4)],
         zeile=G("bibi", "[chuckle] Hear that, Capra? Family. Don't eat the dresses.", "amusement")),
       O("“No. She'll eat Danzel's dresses.”", [F("a3_los_capra"), F("a3_los_capra_nein"), V("casanova", 2)],
         zeile=G("bibi", "[sigh] Fine. But she'll be sad, and so will I.", "disappointment"))]),
]

EVENTS = FRAGEN + LOS_FRAMES + TAFEL_HOLM + RUNDGANG + CAPRA

ORTE = {
    "a3_zeugen": {
        "label": "Who Saw It?", "bild": "village_piazza", "phasen": ["tag", "nachmittag", "abend"],
        "text": "The commission wants witnesses. Ask the people who saw it with their own eyes. Takes the whole phase.",
        "wenn": {"alle": [FL("a3_zeugen_auftrag"), {"eine": [_frage_offen(p) for p in ZEUGEN]}]},
        "start": [{"wenn": _frage_offen(p), "id": "a3_frage_" + p} for p in ZEUGEN]},
    "a3_lose": {
        "label": "The Festa Board", "bild": "village_piazza", "phasen": ["tag", "nachmittag"],
        "text": "Madame Casanova's board. Walk through the village and help up to three of them. Some you also meet at work, "
                "without the board: Petru in his workshop, Alva at the bar, Bà Tư and Lola when you cook, Nonna in her shop, "
                "Buenaventura's men when you fish. Takes the whole phase.",
        "wenn": {"alle": [AKT3, FL("a3_festa_tafel"), {"eine": [los_offen(l) for l in LOSE]}, {"nicht": {"tag_ab": 35}}]},
        "start": [{"wenn": los_offen(l), "id": "a3_los_" + l} for l in LOSE]},
}


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_lose")

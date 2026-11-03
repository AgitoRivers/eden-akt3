# -*- coding: utf-8 -*-
"""Abende und Naechte der Belagerung (Duc 01.11.2026): trösten, Mut zusprechen, die Nacht vor der Schlacht wie im Film. Texte sind Entwuerfe.

Ablauf: bl_abend_wahl_21/22 und bl_nacht_wahl_20/21/22 sind Pflicht. Die Engine kennt keine Optionen mit Bedingung und die Pruefung hoechstens vier
Optionen, also waehlt der Spieler ueber Seiten (Frames) und die Folge "direkt" entscheidet, welche Szene aufgeht:
  gefeuert -> bl_leer · Abend schon gehabt -> bl_ab_schon · Nacht schon gehabt -> kurze Rueckkehr *_wieder(_still)
  Begehren ab Stufe 3 -> Fassung mit Intim-Szene (bl_na_<pid>), sonst dieselbe Szene ohne (bl_na_<pid>_still).
Die Stufe steigt durch diese Szenen nicht: keine Vertrauens- und Begehren-Punkte, nur Moral und Flags (7-Tage-Abstand bleibt).
Am Morgen danach sagt sie etwas dazu: bl_echo_<pid>. Wiki: docs/wiki/welt/belagerung.md."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402

FD = lambda name: {"flag_datiert": name}
DIREKT = lambda ziel: {"direkt": ziel}
MUT = {"wert": "moral", "delta": 1}
FRAME = lambda: WANN((8, 21))                        # nie gezogen, nur ueber "direkt" geoeffnet
PFL = lambda tag, phase: WANN((tag, tag), [phase], pflicht=True, holt_leute=True)
LIEBE = ["chiara", "sophia", "lea", "rosi", "siri", "lola", "alva"]


def _begehren(pid):
    return {"wert": ["begehren." + pid, ">=", 3]}


def ZU_ABEND(pid):
    return DIREKT([{"wenn": {"flag": "gefeuert_" + pid}, "id": "bl_leer"}, {"wenn": {"flag": "bl_ab_fertig_" + pid}, "id": "bl_ab_schon"}, {"id": "bl_ab_" + pid}])


def ZU_NACHT(pid):
    fertig = {"flag": "bl_na_fertig_" + pid}
    return DIREKT([{"wenn": {"flag": "gefeuert_" + pid}, "id": "bl_leer"},
                   {"wenn": {"alle": [fertig, _begehren(pid)]}, "id": "bl_na_%s_wieder" % pid},
                   {"wenn": fertig, "id": "bl_na_%s_wieder_still" % pid},
                   {"wenn": _begehren(pid), "id": "bl_na_" + pid},
                   {"id": "bl_na_%s_still" % pid}])


def AB_O(text, pid):
    return O(text, [F("bl_will_ab_" + pid), ZU_ABEND(pid)])


def NA_O(text, pid):
    return O(text, [FD("bl_will_na_" + pid), {"nacht_bei": pid}, ZU_NACHT(pid)])     # nacht_bei: Funk und mehr Leben am naechsten Tag (kern/taktik.py)


def ABEND_SZENE(pid, ton, titel, bild, set_, lage, zeilen, optionen):
    fertig = F("bl_ab_fertig_" + pid)
    for o in optionen:
        o["folgen"] = [fertig, MUT] + o["folgen"]
    return E("bl_ab_" + pid, "abend", ton, titel, FRAME(), bild, {"pid": pid}, lage, zeilen, optionen, sets={pid: set_})


def NACHT(pid, titel, bild, set_, lage, zeilen, nah, still, zart, intim_ort, intim_set, fuehrung, hinweis):
    """Vier Fassungen aus einem Text: erste Nacht und Rueckkehr, je mit und ohne Intim-Szene. nah/still/zart = (Antwort, Zeile)."""
    fertig = F("bl_na_fertig_" + pid)
    def opt(q, *mehr):
        return O(q[0], [fertig, MUT] + list(mehr), zeile=q[1])
    intim = INTIM(pid, intim_ort, intim_set, fuehrung, hinweis)
    return [E("bl_na_" + pid, "abend", "wholesome", titel, FRAME(), bild, {"pid": pid}, lage, zeilen, [opt(nah, intim), opt(zart)], sets={pid: set_}, knistern=True),
            E("bl_na_%s_still" % pid, "abend", "wholesome", titel, FRAME(), bild, {"pid": pid}, lage, zeilen, [opt(still), opt(zart)], sets={pid: set_})]


def WIEDER(pid, bild, set_, lage, zeile, nah, zart, intim_ort, intim_set, fuehrung, hinweis):
    """Sie ist schon einmal gewaehlt worden: keine zweite grosse Szene, aber sie merkt, dass er wiedergekommen ist."""
    fertig = F("bl_na_fertig_" + pid)
    def opt(q, *mehr):
        return O(q[0], [fertig, MUT] + list(mehr), zeile=q[1])
    return [E("bl_na_%s_wieder" % pid, "abend", "wholesome", "Again", FRAME(), bild, {"pid": pid}, lage, [zeile],
              [opt(nah, INTIM(pid, intim_ort, intim_set, fuehrung, hinweis)), opt(zart)], sets={pid: set_}, knistern=True),
            E("bl_na_%s_wieder_still" % pid, "abend", "wholesome", "Again", FRAME(), bild, {"pid": pid}, lage, [zeile], [opt(zart), O("Sits with her until she sleeps, then goes.", [fertig, MUT])], sets={pid: set_})]


def ECHO(pid, titel, bild, set_, lage, zeile, optionen):
    w = WANN((21, 23), ["fruehstueck"], bed={"flag_seit": ["bl_will_na_" + pid, 1]}, pflicht=True, holt_leute=True)
    return E("bl_echo_" + pid, "abend", "wholesome", titel, w, bild, {"pid": pid}, lage, [zeile], optionen, sets={pid: set_})


# ------------------------------------------------------------------ Wer heute Abend: drei Seiten, Holm am Funk
_ABEND_LAGE = "It is dark, and for now nobody is shooting. People are sitting where they stopped. You have an hour before you need to sleep, and you can only spend it once."
_ABEND_1 = [AB_O("Chiara. She's still handing out jobs.", "chiara"), AB_O("Sophia. She's writing something down again.", "sophia"),
            AB_O("Lea. She hasn't said a word since dinner.", "lea"), O("Someone else.", [DIREKT("bl_abend_s2")])]
_ABEND_Z = G("holm", "That's all for today, Officer. Some of them need to hear a voice that isn't mine. [sigh] So who do you go to tonight?", "neutral")
ABEND_WAHL = [
    E("bl_abend_wahl_21", "gag1", "ernst", "One Hour", PFL(21, "abend"), "crew_mess", P1("holm", ("chiara", "?", "is counting bandages")), _ABEND_LAGE, [_ABEND_Z], _ABEND_1),
    E("bl_abend_wahl_22", "gag1", "ernst", "One Hour", PFL(22, "abend"), "crew_mess", P1("holm", ("chiara", "?", "is counting bandages")), _ABEND_LAGE, [_ABEND_Z], _ABEND_1),
    E("bl_abend_s2", "gag1", "ernst", "One Hour", FRAME(), "crew_corridor", P1("holm", ("rosi", "?", "is in the workshop")),
      "You walk on. There are lights in the workshop and in the galley, and someone is up on the sun deck.",
      [G("holm", "Rosi hasn't left that workshop. Lola is cooking for nobody, and Siri is talking to her camera. [clear throat] Who is it, then?", "neutral")],
      [AB_O("Rosi, in the workshop.", "rosi"), AB_O("Lola, in the galley.", "lola"), AB_O("Siri, on the sun deck.", "siri"), O("Someone else.", [DIREKT("bl_abend_s3")])]),
    E("bl_abend_s3", "gag1", "ernst", "One Hour", FRAME(), "aft_deck", P1("holm", ("maxwell", "?", "is on the quay")),
      "From the aft deck you can see the quay. Alva has carried a crate out there. Mr. Maximum is sitting on a bollard, looking up at the sky.",
      [G("holm", "That leaves the quay. Or you could go to bed, and I wouldn't say a word against it. [sigh] What will it be?", "neutral")],
      [AB_O("Alva, with her crate.", "alva"), AB_O("Mr. Maximum, on his bollard.", "maxwell"),
       O("Nobody. Goes to bed.", [F("bl_will_ab_niemand")], zeile=G("holm", "Good. [sigh] That's the first sensible thing anyone has done today.", "approval"))]),
    E("bl_leer", "gag1", "ernst", "An Empty Cabin", FRAME(), "crew_corridor", P1("holm", ("chiara", "?", "says nothing")),
      "The door is open, and the cabin behind it has been cleared out. You knew that. You came here anyway.",
      [G("holm", "She isn't on this boat any more, Officer. You signed the paper yourself. [sigh] Go and get some sleep.", "neutral")],
      [O("Goes to bed.", [MUT]), O("Stands there for another minute, then goes to bed.", [MUT])]),
    E("bl_ab_schon", "gag1", "ernst", "Asleep", FRAME(), "crew_corridor", P1("holm", ("chiara", "?", "says nothing")),
      "You talked to her last night, when you still had an hour. Tonight the light is off. You listen at the door, and she is breathing slowly.",
      [G("holm", "Leave her. She's asleep, and that's more than I can say for you. [clear throat] Go to bed, Officer.", "neutral")],
      [O("Goes to bed.", [MUT]), O("Leaves a coffee outside her door for the morning, then goes to bed.", [MUT])]),
]

# ------------------------------------------------------------------ Abende: trösten oder Mut zusprechen
ABENDE = [
    ABEND_SZENE("chiara", "ernst", "Zero Out of Ten", "crew_mess", "Uniform",
                "Chiara has told four people where to sleep and two people how. Her rifle lies on the mess table, the taser rifle that Rosi built for her. When the room is empty, she stops talking, and on her that is very loud.",
                [G("chiara", "Do you know what they do when you hit them with that thing, First Officer? They twitch. Then they look at you. [sigh] Nobody tells you about the looking.", "sadness"),
                 G("chiara", "I've done six seasons of napkins. I can tell you what a good wine costs in eleven ports. Today I shot a man in the chest, and then I went and checked the water supply. [sniff] What kind of person does that?", "fear")],
                [O("“The kind who kept forty people drinking water. You're allowed to shake now, Chiara.”", [],
                   zeile=G("chiara", "I'm not shaking. [sniff] …Don't tell anyone. And it's Duc when nobody's here, I keep telling you. Eight. That was an eight.", "gratitude")),
                 O("“Somebody has to give out the jobs. Give me one.”", [],
                   zeile=G("chiara", "[chuckle] Oh, you know exactly what you're doing. Fine. Sit there and eat something, that's your job. Don't look at me while I do this.", "caring"))]),
    ABEND_SZENE("sophia", "ernst", "Ten Euros", "aft_deck", "Concierge",
                "Sophia has found blankets for everyone who needs one. Now she sits on the aft deck with her little brown notebook shut on her knee. She has been holding the pen for a long time, and it hasn't moved.",
                [G("sophia", "Ten euros says you've come to ask how everybody else is, darling. I can tell you. I've got it all written down. [chuckle] Everybody is managing beautifully.", "amusement"),
                 G("sophia", "I've looked after Lea since she was nine. I know what to say to a harbour master and to a duke. [sigh] I don't know what I would say to my mother, if it came to that. Tell me honestly. Will my sister be all right?", "fear")],
                [O("“I don't know. I'll do everything I can, and I won't lie to you.”", [],
                   zeile=G("sophia", "No. You won't, will you? [sniff] That's the first honest answer I've had all week, and it's a horrible one. Thank you.", "gratitude")),
                 O("“You owe me ten euros. I came to ask how you are.”", [],
                   zeile=G("sophia", "Oh, you wretched man. [chuckle] I'm frightened. There. It's a very short sentence, I had no idea. Sit down and don't be kind about it.", "caring"))]),
    ABEND_SZENE("lea", "ernst", "Coordinates", "foredeck", "Off Duty",
                "Lea sits on the foredeck with her logbook, the one that holds her grandfather's map. Page forty. She worked out where the wreck lies that he looked for all his life, and she was so proud that she wrote down the coordinates. Alon saw them. That's why his drone came.",
                [G("lea", "Did you know a hermit crab will swap its shell if something better comes along? It just – no, that's not what I wanted to say. [sniff] I'm sorry. I don't know what I wanted to say.", "nervousness"),
                 G("lea", "It was me, Duc. Alon saw my coordinates, that's what Megan told you on the call. I wrote them down properly, and I was so pleased with myself. [sigh] Did all of this happen because of me?", "remorse")],
                [O("“No. He wanted this bay long before you found anything. You just found it first.”", [],
                   zeile=G("lea", "Proper first? [sniff] Grandad would've liked that bit. Okay. Okay, I'll try to believe you until the morning, at least.", "gratitude")),
                 O("“Maybe it started there. Is that the reason you would stop looking?”", [],
                   zeile=G("lea", "…No. No, I'd do it again, and I'd just hide the page better. [sigh] That's a terrible thing to find out about yourself. Thanks, I think.", "realization"))]),
    ABEND_SZENE("rosi", "ernst", "Nothing to Fix", "workshop", "Engine Room",
                "Rosi has taken apart a battery from a taser rifle, and it wasn't broken. Her hands are black and they don't stop moving. Her father lost his workshop to the bank, and she stood next to him while it happened, and there was nothing she could do.",
                [G("rosi", "Don't touch that, Officer. It's a very delicate job, and I'm the only one on this boat who can do it. [clear throat] I've done it three times now. It's perfect.", "pride"),
                 G("rosi", "Unit-01 has a bad bearing, you know. It makes a noise when it's frightened, and I know it's a machine, so don't say it. [sigh] When there's nothing left to fix, what's a machine supposed to do? Just stand there?", "fear")],
                [O("“It holds the lamp for somebody else. Give me the lamp.”", [],
                   zeile=G("rosi", "You're holding it wrong. [chuckle] No, stay, you're holding it wrong in a very useful way. I'm not saying that means anything.", "caring")),
                 O("“You built half of what's holding this village up. Nobody's just standing there.”", [],
                   zeile=G("rosi", "Half? That's an insult, it's at least two thirds. [sniff] …I'm putting that on the board as a win. Go away before I say something.", "gratitude"))]),
    ABEND_SZENE("siri", "ernst", "No Signal", "sun_deck", "Dad's Sweater",
                "Siri sits on the sun deck with her phone on a little tripod. She has filmed all day, and none of it has gone anywhere, because Alon's satellites have closed the sky. Under her jacket you can see an old hand-knitted sweater. You have never seen her wear it.",
                [G("siri", "Hiii guys, so it's – sorry. Sorry, I don't know who I'm saying that to. Two point eight million people, and not one of them can see this. [sigh] It's so strange. I think I've never been this alone or this honest.", "sadness"),
                 G("siri", "My father knitted this, one star every winter evening. He'd be down on that beach with a boat hook, you know, and he'd be right. And I've got a very nice video. [sniff] So what do you think, should I keep filming or put the camera down?", "confusion")],
                [O("“Keep filming. One day somebody will need to know what really happened here.”", [],
                   zeile=G("siri", "That's – nobody ever said it was for anything. [sniff] Okay. No captions, then. I'll just say what I saw, in my own words, if I can find any.", "optimism")),
                 O("“Put it down for tonight. There's nobody to be except you.”", [],
                   zeile=G("siri", "I don't know if there's anybody there, that's the problem. [chuckle] Sorry. Sorry, that was sad. Would you stay a bit, and we could find out?", "caring"))]),
    ABEND_SZENE("lola", "ernst", "Yes, Chef", "galley", "Galley",
                "The galley smells of burning, and that has never happened when nobody is watching. Lola has made soup for sixty people, and twenty came. When Holm's voice came over the radio today, sharp and loud, Lola stood still with a ladle in her hand and said “Yes, Chef”. Nobody heard. She did.",
                [G("lola", "G'day, Boss, there's soup, heaps of soup, and I reckon it's mostly fine. Mostly the cheese. [chuckle] Don't look at the bottom of the pot.", "nervousness"),
                 G("lola", "Everyone out there's got a rifle or a hammer, mate. I've got a wooden spoon, and I freeze up when someone yells. [sniff] That bloke in Sydney said I'd never be more than a side cook, and today I reckon he had a point. So what am I even doing here?", "sadness")],
                [O("Picks up a bowl and eats. “Nobody out there can fight on an empty stomach. This is why they're still standing.”", [],
                   zeile=G("lola", "You're eating the burnt bit, you absolute legend. [sniff] Right. Right, breakfast, then. Sweet as. I'll need more onions, and don't you tell anyone I cried in the soup.", "gratitude")),
                 O("“He was wrong about you, and you walked out on him that same night. Who does that, if she's scared?”", [],
                   zeile=G("lola", "Someone with no job and a very small suitcase. [chuckle] But yeah. Yeah, I did, didn't I? Thanks, Boss. Here, take some to Holm, and tell her she's loud.", "caring"))]),
    ABEND_SZENE("alva", "ernst", "On the Board", "village_harbour", "alva_standard",
                "Alva has carried a crate of bottles down to the quay, and she is giving them out to anyone who walks past. Everyone here will tell you that she has never given away one drink in her life. She has Papa's shotgun over her shoulder and a piece of chalk behind her ear.",
                [G("alva", "Don't look at me like that. It's not free, nothing's free. I'm writing down every glass. [chuckle] Minicu owes me for eleven already.", "amusement"),
                 G("alva", "If they owe me, they have to come back and pay, you see. That's how it works. Forty years Papa did it that way, and nobody ever left this village owing him. [sigh] So, o figliolu, what do I put you down for?", "neutral")],
                [O("“The first round when this is over. For everyone.”", [F("bl_alva_runde")],
                   zeile=G("alva", "For everyone. You have no idea what that costs. [chuckle] Good. Now you really can't die, I'd have to chase the money.", "joy")),
                 O("“Nothing. I'll pay you tonight, in cash, like a stranger.”", [],
                   zeile=G("alva", "No, you won't. [sigh] Strangers can leave. Take the bottle and owe me, and we'll say no more about it.", "caring"))]),
    ABEND_SZENE("maxwell", "ernst", "Things That Fly", "village_harbour", "maximum_steelmop",
                "Mr. Maximum sits on a bollard with the Steel Mop across his knees. He is two metres of muscle, and he has been looking at the sky for an hour. Everything that flies frightens him. It's the reason he works on boats. Tonight there are drones up there.",
                [G("maxwell", "Howzit, Number One. Mr. Maximum is doing his evening stretches. [clear throat] These are stretches of the neck. Upwards. Very advanced.", "nervousness"),
                 G("maxwell", "A man hit Mr. Maximum today, and that was lekker, that was a conversation. But this little machine comes down at you with no face, brother, and his legs turn to porridge. [sigh] And the whole crew is watching him. So tell Mr. Maximum, what does a big man do when he's scared?", "fear")],
                [O("“He tells one person. You just did. Then he gets up at half past six and does lesson one.”", [],
                   zeile=G("maxwell", "Eish. Half past six. [sniff] You're using his own lesson on him, Number One, and that's very low. Mr. Maximum approves. Nobody saw this. It's the allergies.", "gratitude")),
                 O("“Elsa and Chiara can shoot what flies. You hit what walks. Nobody fights the whole sky alone.”", [],
                   zeile=G("maxwell", "Ja-nee, that is a proper plan. [chuckle] A team, hey? Who taught you that? Don't answer. Mr. Maximum taught you that. Lekker.", "relief"))]),
]

# ------------------------------------------------------------------ Wer heute Nacht
_NACHT_1 = [NA_O("Chiara, up on the bridge wing.", "chiara"), NA_O("Sophia, on the aft deck.", "sophia"), NA_O("Lea, on the foredeck.", "lea"), O("Someone else.", [DIREKT("bl_nacht_s2")])]
_NACHT_Z = G("holm", "You should be asleep, and so should they, and nobody is. [sigh] I'm not your mother, Officer. Who are you going to?", "neutral")
_NACHT_LAGE = "It is late, and whatever comes tomorrow is coming. The whole boat is awake and pretending not to be. There's time to go to one door tonight, and only one."
NACHT_WAHL = [
    E("bl_nacht_wahl_%d" % tag, "gag1", "wholesome", "One Door", PFL(tag, "nacht"), "crew_corridor", P1("holm", ("chiara", "?", "is up on the bridge wing")), _NACHT_LAGE, [_NACHT_Z], _NACHT_1)
    for tag in (20, 21, 22)
] + [
    E("bl_nacht_s2", "gag1", "wholesome", "One Door", FRAME(), "crew_corridor", P1("holm", ("rosi", "?", "is in the generator room")),
      "There's a light under the generator room door. Someone is moving pans in the galley, and there's a small shape on the sun deck.",
      [G("holm", "I don't want to know, and I won't write it in the log. [clear throat] Which one is it?", "neutral")],
      [NA_O("Rosi, in the generator room.", "rosi"), NA_O("Lola, in the galley.", "lola"), NA_O("Siri, on the sun deck.", "siri"), O("Someone else.", [DIREKT("bl_nacht_s3")])]),
    E("bl_nacht_s3", "gag1", "wholesome", "One Door", FRAME(), "aft_deck", P1("holm", ("alva", "?", "is alone on the quay")),
      "From the rail you can see the quay. The bar's chairs are out there, and someone is standing among them in a dark dress. Alva, by herself, not moving.",
      [G("holm", "Or you could sleep. People do. [sigh] What's it going to be?", "neutral")],
      [NA_O("Alva. Goes down to the quay.", "alva"),
       O("Nobody. Goes to bed alone.", [F("bl_will_na_niemand"), MUT], zeile=G("holm", "Good. [sigh] Somebody on this boat should be fit to think in the morning.", "approval"))]),
]

# ------------------------------------------------------------------ Naechte
_C = [G("chiara", "Sunset: four. Moon: six. The stars are showing off, so I took two points away. [sigh] I'm rating the sky, Duc, because I've run out of things to count.", "neutral"),
      G("chiara", "Everyone on this boat needs me to know what happens next. I've got a list for tomorrow, and it's a very good list, and I don't know what happens next. [sniff] I don't want to be the Chief Stewardess for the next few hours. Can you do that? Can you tell me what I am when I'm not?", "fear")]
_S = [G("sophia", "No cards tonight, I've put them away. It seemed unfair, I'd only have taken your money, and you may need it. [chuckle] I have been meaning to tell you. You've been losing a bet to me since the first week.", "amusement"),
      G("sophia", "I bet you'd ask me what I actually want before the week was out. You did, in your way. [sigh] So here it is, with no show. I'd like one hour where nobody needs me. Just one. Do you think you could not need me, darling? Is that a terrible thing to ask?", "sadness")]
_L = [G("lea", "Look down, look at the water, there. See it? That's plankton, it glows when something moves, it's proper glow. Did you know they do it to frighten off – no. I don't know why they do it. [sigh] I've forgotten. I never forget.", "nervousness"),
      G("lea", "This is the sign for stay together, two fingers, like this. You make it to your dive buddy, and it means don't go where I can't see you. [sniff] I know it doesn't work on land. Will you make it back anyway? I just want to see you do it.", "love")]
_R = [G("rosi", "Officer. You're in my generator room at this hour, and nothing's broken, so don't pretend it is. I've checked. Twice. [clear throat] The score on my board is very much in my favour, by the way, if you were wondering.", "pride"),
      G("rosi", "If something happens tomorrow, you'd win by default, and I do not accept that. I've never lost to you, and I'm not losing that way. [sigh] So you're going to stay here tonight and be alive at me. That's not a question. …All right, it's a question. Will you?", "nervousness")]
_I = [G("siri", "Hi. Sorry. There's no camera, you can check. Yasin thinks I'm asleep, and the chair over there has been very understanding about it. [chuckle] Sorry, I talk to the furniture when I'm frightened.", "embarrassment"),
      G("siri", "This is my father's sweater, you've maybe seen it. One star for each winter evening. I've carried it for six years, and I put it on tonight for the first time, because if tonight was the last chance to wear it, I didn't want it to still be in a suitcase. [sniff] Is that stupid? Can you tell me honestly, if I'm stupid?", "sadness")]
_O = [G("lola", "Toastie, Boss? I've burnt two already, because you walked in. [chuckle] It's what I make Nan when she can't sleep. I mean, I would, if she wasn't in Byron Bay. Mostly the cheese.", "amusement"),
      G("lola", "I ring her every Sunday. She's ninety-one, and she called the coast guard once when I missed one, the actual coast guard. There's no signal now, mate. [sniff] So I keep thinking, what if Sunday comes and I can't tell her anything? Would you just stay here with me till the pan's cold?", "sadness")]
_A = [G("alva", "No music. Don't look for it, there isn't any. This is my grandmother's dress, and I had it ready for Seville when I was twenty-two. Thirteen years it's been in a cupboard, and I've told everyone in this village that I don't dance any more. [sigh] Stand over there. Don't clap.", "neutral"),
      G("alva", "My mother rings every year at the end of the season. When do I get you back, she says. I always say next year, o figliolu. It's a good line, it gets a laugh. [sniff] Tonight I'd like someone to have seen this, in case next year turns out to be a thing I can't promise.", "sadness"),
      G("alva", "I don't do goodbyes, I do tabs. So you were never here, and I never danced. Everybody's welcome, nobody's mine, you know how it goes. [sigh] Now tell me, since you came all the way down here. What are you going to do about it?", "caring")]

NAECHTE = (
    NACHT("chiara", "What You Are When You're Not", "bridge", "Bridge Night",
          "The bridge wing, high above the dark water. Chiara is alone out here, with her grandfather's old sextant beside her on the rail. She isn't using it. By day she is the loudest person on the boat. Up here she isn't.", _C,
          ("Takes the sextant out of her hand and puts it down. “Nobody needs anything from you until morning. Come with me.”", G("chiara", "…No list. All right. [sigh] I'm not telling you the number. It isn't on the scale.", "love")),
          ("“You're the person who stays up to rate the moon. I like her. Tell me about the stars.”", G("chiara", "Oh, now you've done it. [chuckle] That one's a four, it thinks it's better than it is. Sit down. This could take a while, and I'm glad.", "love")),
          ("Stands next to her at the rail and says nothing at all.", G("chiara", "[sigh] …Seven. No. Don't talk. Stay like this, it's going up.", "caring")),
          "duc_cabin", "Cabin Night", "duc", "The night before the fighting, or between two days of it. Chiara has no list tonight and nothing to organise, and she finds that hard, then funny, then not funny at all. She won't say goodbye, and she doesn't talk about tomorrow."),
    NACHT("sophia", "One Hour", "aft_deck", "Writing Night",
          "The aft deck, past midnight. Sophia's glasses are pushed up in her hair, and her little brown notebook is lying closed on the table. You have never seen her put it down and walk away from it.", _S,
          ("“No. It isn't. I don't need a thing from you, Sophia. Come inside, and we'll waste it.”", G("sophia", "[sigh] …You'd better mean that. Bring nothing. I'm so tired of bringing things.", "love")),
          ("“It isn't. I need nothing. Sit down, close your eyes, and I'll tell anyone who comes that you're out.”", G("sophia", "Out. How lovely. [sniff] I've never been out. Wake me in an hour. …No. Don't.", "love")),
          ("Pulls a blanket over her shoulders, and for once she lets someone do it.", G("sophia", "That's my job, you know. [sigh] Thank you. I'll be perfectly charming about it at breakfast.", "gratitude")),
          "duc_cabin", "Writing Night", "sophia", "Sophia asked for one hour in which nobody needs her. Her charm comes off bit by bit, and her sentences get short and plain. She won't talk about tomorrow, and she won't manage him."),
    NACHT("lea", "Stay Together", "foredeck", "Off Duty",
          "The foredeck. Lea is lying on her front with her head over the side, and the water below her shines faintly blue wherever a fish turns. She doesn't look round when you come. She knows your walk by now.", _L,
          ("Makes the sign, two fingers, and holds out a hand. “Come on. Not where I can't see you.”", G("lea", "Okay. [sniff] Okay, proper okay. Not fast, though. Is that all right? I don't want to go fast tonight.", "love")),
          ("Makes the sign, two fingers, and lies down beside her at the rail. “Tell me what they do when they glow.”", G("lea", "They glow when they're scared, I think. [chuckle] Don't tell Sophia I said I think. Move over, you're on my arm. No, stay.", "love")),
          ("Makes the sign and stays until the blue goes out of the water.", G("lea", "There. Now you've said it, and you can't take it back, that's the rule. [sniff] Dreckly, then. Dreckly, we'll all go and see the wreck.", "caring")),
          "duc_cabin", "Off Duty", "lea", "Lea talks fast until she is alone with him, and then she goes slow and quiet. Two fingers mean stay together. She doesn't want to go fast tonight, and she doesn't want to talk about tomorrow."),
    NACHT("rosi", "Alive At Me", "generator_room", "Engine Room",
          "The generator room is warm and it smells of diesel. Rosi sits on a toolbox with a spanner that she doesn't need. On the wall is her board, Rosi versus Officer, every repair and duel since your first day, and she is winning, because she keeps the score.", _R,
          ("Shuts the door behind him. “It's a draw until the morning. Nobody's keeping score.”", G("rosi", "Somebody's always keeping score. [chuckle] But I can do it later. This is my destiny, Officer, and if you tell anyone I said that, I'll deny it.", "love")),
          ("Sits down on the floor next to the toolbox. “I'm here. Be alive at me too.”", G("rosi", "You're sitting in oil. You know that? [sniff] That's a bad place to sit, and you're staying exactly there. Listen to her, she sounds better now.", "love")),
          ("Takes the marker and adds one line to her side of the board.", G("rosi", "What was that for? You can't just give me points. [sigh] …Leave it. Goodnight, Captain. I said Officer. Go to bed.", "caring")),
          "generator_room", "Engine Room", "rosi", "The door is shut, and Unit-01 hums behind it. Rosi keeps score out loud because she is afraid, and she is not as sure of herself as she is with machines. She will not say the word goodbye."),
    NACHT("siri", "One Star a Winter", "sun_deck", "Dad's Sweater",
          "The sun deck. Siri sits with her knees pulled up inside a big old sweater with small stars knitted across it, and it doesn't fit her. There's no tripod and no phone. It's the first time you have ever seen her without something to look into.", _I,
          ("“You're not stupid. Come downstairs, and leave Siri Sea up here.”", G("siri", "She won't mind, she's very professional. [chuckle] Sorry. Can I keep the sweater on, for a bit? Or – I don't know. You can ask me, nobody ever asks me.", "love")),
          ("“You're not stupid. Show me which star was the best winter.”", G("siri", "Nobody's ever – oh. This one, I think. The ferry was late for a week, and he only had me to talk to. [sniff] Sit here, I'll show you all of them. There are so many.", "love")),
          ("Puts an arm round her and looks out at the water, and neither of you takes a picture.", G("siri", "That's the nicest thing that's ever happened to me that nobody saw. [sniff] Sorry. Sorry, that's just what I think.", "gratitude")),
          "duc_cabin", "Dad's Sweater", "duc", "No camera, no Yasin, no captions. Siri asks real questions and apologises too often, and she laughs at herself before anyone else can. He takes it slowly, and she doesn't talk about tomorrow."),
    NACHT("lola", "Till the Pan's Cold", "galley", "Off Duty",
          "The galley, with one light on. Lola is barefoot in old shorts, and she's making a cheese toastie for nobody. She burns everything when someone watches, and you are watching. She reaches over, and she doesn't send you out.", _O,
          ("Takes the pan off the heat. “It's cold enough. Come here, Lola.”", G("lola", "Oi, that's a perfectly good – yeah. Yeah, all right. [chuckle] You're a menace, Boss, and I reckon I'll make you breakfast after. I've heard that's how it goes.", "love")),
          ("Sits on the counter and eats the burnt one. “I'll stay. Tell me about Nan and the coast guard.”", G("lola", "So they sent a whole boat, mate, a real one! [laugh] And she made them scones. Hang on, it gets better. It gets heaps better. Mostly the scones.", "love")),
          ("Stays until the pan is cold, as she asked, and washes it for her.", G("lola", "You've done that wrong, you've used soap. [sniff] Nobody's ever done that wrong for me before. Night, Boss.", "gratitude")),
          "duc_cabin", "Off Duty", "lola", "Lola is loud and warm, and tonight she is frightened that she won't reach Nan on Sunday. She laughs at her own jokes and she loses the ends of her sentences. Nobody shouts at her here. She doesn't talk about tomorrow."),
    NACHT("alva", "Nobody's", "village_harbour", "alva_flamenco_noche",
          "The quay, very late. The chairs from the bar stand on the stones where somebody left them. Alva has put Papa's shotgun across one of them, and she has a dark dress on that you have never seen. There's nobody else here, and she has been waiting for that.", _A,
          ("“You danced, and I saw it. Come with me, and don't give me a line.”", G("alva", "No line. [sigh] Nobody in this village has ever seen me go up a gangway at night. Take me up there, o figliolu, and turn the light off. And in the morning you owe me nothing.", "love")),
          ("“Nothing. I'm going to sit here until you've finished, and then I'll carry the chairs.”", G("alva", "Then sit down. [sigh] Nobody's ever carried the chairs. You remember this, because I won't say it twice: I remember who helps me.", "love")),
          ("“Dance it once more. I wasn't ready.”", G("alva", "Nobody's ever ready. [sniff] It's better without the clapping, isn't it? Don't tell them. They'd only want me to do it at the Festa.", "love")),
          "duc_cabin", "alva_flamenco_noche", "alva", "Alva flirts with everybody and belongs to nobody, and tonight she has stopped doing that. There is no speech and no promise. She doesn't do goodbyes, she does tabs, and she will not say the word tomorrow."),
)
NAECHTE = [e for gruppe in NAECHTE for e in gruppe]

_W = [
    ("chiara", "bridge", "Bridge Night", "The bridge wing again. She doesn't look round. There's a second cup of coffee on the rail, and it's still hot, so she knew.",
     G("chiara", "You again. [chuckle] I didn't plan for this, so it isn't on any list. What are you going to do, stand there or come here?", "love"), "duc_cabin", "Cabin Night", "duc", "Chiara, again, with no list. It is quieter than the first time."),
    ("sophia", "aft_deck", "Writing Night", "The aft deck again. Her notebook isn't here at all tonight. She moves over, and that is all she says for a while.",
     G("sophia", "I rather hoped you'd have the sense to sleep, darling. [sigh] I also rather hoped you wouldn't. Well? Is it the same hour you came for?", "love"), "duc_cabin", "Writing Night", "sophia", "Sophia, again, with her sentences short and plain. She doesn't manage him tonight either."),
    ("lea", "foredeck", "Off Duty", "The foredeck again. Lea holds up two fingers before you have said anything. It's the divers' sign: stay together.",
     G("lea", "You came back. That's how it's meant to work, you know, that's what it's for. [sniff] Do you want to stay out here, or shall we go in?", "love"), "duc_cabin", "Off Duty", "lea", "Lea, again, slow and quiet. Two fingers mean stay together."),
    ("rosi", "generator_room", "Engine Room", "The generator room again. Rosi points at the board with her spanner. There's a new line on it, and she doesn't explain it.",
     G("rosi", "That's two nights you've been here with nothing broken, so I'm charging you for the electricity. [chuckle] Are you staying, Officer, or do I have to break something?", "love"), "generator_room", "Engine Room", "rosi", "Rosi, again, with the door shut and Unit-01 humming behind it. She has stopped keeping score out loud."),
    ("siri", "sun_deck", "Dad's Sweater", "The sun deck again. She's wearing the sweater again, the one with the stars, and it has soot on one sleeve now. She hasn't tried to clean it.",
     G("siri", "Sorry, I saved you some of the blanket. I told the chair you'd come. [chuckle] It wasn't sure. Do you want to stay here, or go somewhere with a door?", "love"), "duc_cabin", "Dad's Sweater", "duc", "Siri, again, with no camera and no captions. She asks instead of guessing."),
    ("lola", "galley", "Off Duty", "The galley again. There's one toastie on the board, and this time it isn't burnt. She looks at it, then at you, as if one of you has done something wrong.",
     G("lola", "You weren't watching, so it worked. [chuckle] It's yours, mate, I made it for you. Mostly the cheese. Are you going to eat it, or what?", "love"), "duc_cabin", "Off Duty", "lola", "Lola, again, barefoot and warm. Nobody shouts here."),
    ("alva", "village_harbour", "alva_morgen", "The quay again. She is back in an old shirt, and she's sitting on the chair next to Papa's shotgun. The other chair has been pulled up beside it.",
     G("alva", "I told you I don't do goodbyes, so this isn't one. [sigh] Everybody's welcome, o figliolu. Sit down. What am I putting you down for tonight?", "love"), "duc_cabin", "alva_morgen", "alva", "Alva, again. There is no speech and no promise."),
]
RUECKKEHR = [e for pid, bild, set_, lage, zeile, ort, iset, fuehrung, hinweis in _W for e in WIEDER(pid, bild, set_, lage, zeile,
             ("Doesn't say anything, and takes her hand.", G(pid, "[sigh] …Good. No talking, then.", "love")),
             ("Sits down beside her. “I only came to be here.”", G(pid, "[sigh] I know. That's why it's all right.", "caring")),
             ort, iset, fuehrung, hinweis)]

# ------------------------------------------------------------------ Der Morgen danach
ECHOS = [
    ECHO("chiara", "Rated", "crew_mess", "Uniform", "Breakfast in the mess, with everybody talking. Chiara walks past you with a tray and hands out jobs. Last night, up on the bridge wing, she asked you who she was when nobody needed her. She doesn't stop walking, but she slows down.",
         G("chiara", "Last night: I'm not telling you the number. It's a good number. [clear throat] Now eat something, First Officer, that's an order.", "amusement"),
         [O("“What's the scale for this morning?”", [MUT], zeile=G("chiara", "Coffee: five. You: don't push it. [chuckle] Go on, get out of my mess.", "joy")), O("Eats something.", [MUT])]),
    ECHO("sophia", "Charming at Breakfast", "crew_mess", "Concierge", "Sophia pours your coffee herself and makes it look like an accident. Last night on the aft deck, she asked you for one hour in which nobody needed her. This morning she has her notebook back, and three people are waiting to ask her things.",
         G("sophia", "You'll notice I'm being perfectly charming, as I said I would. [chuckle] It's rather harder than usual. Do you know why that is, darling?", "amusement"),
         [O("“You owe me ten euros.”", [MUT], zeile=G("sophia", "I do not. [sigh] But I'll pay it, after all this, in person. Do remember to collect.", "love")), O("Drinks the coffee and lets her work.", [MUT])]),
    ECHO("lea", "Two Fingers", "foredeck", "Deck", "Lea is coiling a rope that is already coiled. Last night she showed you the divers' sign out on the foredeck: two fingers, stay together. As you pass, she gives you a very serious salute, and she has two fingers up.",
         G("lea", "Did you know an octopus has three hearts, Duc? Two of them stop when it swims. [sniff] I don't know why I said that. Are you going to be careful today?", "nervousness"),
         [O("Makes the sign back, two fingers.", [MUT], zeile=G("lea", "Right. Proper. [chuckle] That's all I wanted.", "joy")), O("“As careful as you are.”", [MUT], zeile=G("lea", "Oh, that's not very careful, then. [sniff] Try harder than me.", "caring"))]),
    ECHO("rosi", "On the Board", "workshop", "Engine Room", "Rosi hands you a spanner that you didn't ask for. Last night you stayed with her in the generator room, with nothing broken. There's a fresh line on her board this morning, and she stands in front of it so that you can't read it.",
         G("rosi", "Don't look at my board, Officer, that's a private matter between me and the board. [clear throat] You're still alive, I notice. Are you planning to keep that up?", "pride"),
         [O("“That's the plan. What's the score?”", [MUT], zeile=G("rosi", "I'm winning. [chuckle] I'll always be winning, so you'd better come back and argue.", "love")), O("Takes the spanner.", [MUT])]),
    ECHO("siri", "No Caption", "aft_deck", "Dad's Sweater", "Siri is on the aft deck with a cup in both hands. She is still wearing the sweater with the stars, the one she showed you last night on the sun deck, and people can see it. She hasn't said one word to her camera yet.",
         G("siri", "Hi. Sorry. Yasin asked me what I'm wearing, and I told him it's mine. [chuckle] I've never said that about anything. Is it strange that I'm happy, today of all days?", "joy"),
         [O("“No. Stay happy. It suits the sweater.”", [MUT], zeile=G("siri", "It really doesn't fit, you know. [sniff] I'm keeping it on.", "love")), O("Touches one of the stars on her sleeve and goes to work.", [MUT])]),
    ECHO("lola", "Breakfast", "galley", "Galley", "There's a plate at your place, with a cheese toastie on it, and it isn't burnt. Last night in the galley you stayed with Lola until the pan was cold. She is very busy with something on the other side of the room, and she's whistling badly.",
         G("lola", "Don't tell anyone I told you, Boss, but someone on this boat got the good one. [chuckle] No idea who. Mostly the cheese.", "amusement"),
         [O("Eats every bit of it.", [MUT], zeile=G("lola", "You legend. [sniff] Right, heaps to do. Get out of my galley, and come back in one piece.", "love")), O("“Sunday. We'll find you a signal, for Nan.”", [MUT], zeile=G("lola", "…Yeah. Yeah, you'd better, or she'll send a boat. [sniff] Ta, mate.", "gratitude"))]),
    ECHO("alva", "The Tab", "village_harbour", "alva_morgen", "Alva is on the quay with a coffee for you, and she takes the money for it. Last night she danced for you out here in the dark, once, and told you that you were never there. She counts your change very carefully.",
         G("alva", "You look tired, o figliolu. I can't think why. [chuckle] That's one euro fifty, and I'm writing down the rest. Do you want to know what you owe me?", "amusement"),
         [O("“Tell me when this is over.”", [MUT], zeile=G("alva", "That's what they all say. [sigh] Mind you come and pay it. Alva remembers.", "caring")), O("Drinks the coffee and says nothing about any dancing.", [MUT], zeile=G("alva", "Good. [chuckle] What dancing?", "joy"))]),
]

EVENTS = ABEND_WAHL + ABENDE + NACHT_WAHL + NAECHTE + RUECKKEHR + ECHOS

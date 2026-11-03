# -*- coding: utf-8 -*-
"""Szenen fuer Bibis Tierstation (Duc 01.11.2026, Wiki systeme/tierstation.md). Jede Spur ist eine kurze Ortskette:
mo_<tier>_spur (oder _wieder ab dem zweiten Fang) -> Kampf (kaempfe_mochis.py) -> bei Erfolg Bibis Overlay oder Handy (FANG in mochis_daten.py), sonst mo_<tier>_weg. Gestartet aus dem Field Book (kern/mochis.spur_start).
Die Halsbaender machen die Tiere verrueckt: Duc kaempft sie muede, dann wirkt Rosis Schlafgranate gegen das Halsband. Texte sind Entwuerfe und noch nicht vertont."""
from ereignisse_basis import *  # noqa: F401,F403
import mochis_daten as _mo

KAMPF = lambda bid: {"kampf": bid}
WEITER = lambda ziel: {"weiter": ziel}
TAGE = (11, 35)            # Spuren laufen bis zum Ende, sonst bleibt das Buch fuer viele leer (Duc 01.11.2026, 14 Tiere)
BIBI = {"bibi": "Mochis"}


def FR(id, bild, titel, lage, zeilen, optionen, ton="ernst"):
    sets = dict(BIBI, danzel="danzel_B") if any(z["wer"] == "danzel" for z in zeilen) else BIBI
    e = E(id, "ort", ton, titel, WANN(TAGE), bild, {"handelnd": "bibi", "betroffen": []}, lage, zeilen, optionen, sets)
    e["musik"] = "expedition_macchia"
    if not id.endswith(("_spur", "_wieder")):                       # nach dem Kampf fuehrt kein Rueckweg
        e["sperre"] = True
    return e


# Zweiter Fang: je Tier ein eigener Satz statt „Same collar, same light“ (Duc 02.11.2026, BIBI_ARC_TEXTE.md)
WIEDER = {
    "hund": "That one's got the same nose, nearly. Tire it out, then the grenade, and don't tell Biscuit.",
    "hyaene": "There's a second one. Nobody's told this one it's funny yet. You know how this goes.",
    "affe": "This one's watching how you hold the grenade. Wear him out before he learns it.",
    "capybara": "Another one. Birds on him and everything. It took them four days with him too. Be nice.",
    "keiler": "That's his other sister. There are a lot of them, and they all hate you. Same plan.",
    "baerchen": "It's the other little one. It's so light, so please, only the smallest hits you've got.",
    "schildkroete": "That's Nineteen! She found one! Slowly, please. They've got all day.",
    "geier": "That's his friend, and it's stolen my lunch. Wait until it lands, then the grenade.",
    "waran": "I didn't know there were two. Charly's going to want a name for this. Don't let it start the clock.",
}
SCHLUSSSATZ = " Next time stop one hit sooner, okay?"
BEHAELT_SCHLUSSSATZ = ("hund", "mufflon", "affe", "wolf")


def KETTE(tid, bild, titel, lage, zeile, gefuehl, los, weg_lage, weg_zeile):
    """Spur, Kampf und bei einem Fehlschlag der Rueckweg. Ein Erfolg endet ohne Frame: Bibi meldet sich danach (kern/mochis.kampf_ende, Duc 01.11.2026)."""
    name = _mo.TIERE[tid]["name"]
    if tid not in BEHAELT_SCHLUSSSATZ:
        weg_zeile = weg_zeile.replace(SCHLUSSSATZ, "")
    kampf = [KAMPF("mochis_%s" % tid), WEITER([{"wenn": {"nicht": {"flag": "mo_fang_heute"}}, "id": "mo_%s_weg" % tid}])]
    frames = [
        FR("mo_%s_spur" % tid, bild, titel, lage, [Z("bibi", zeile, gefuehl)], [O(los, kampf), O("Turns back. “Not today.”", [])]),
        FR("mo_%s_weg" % tid, bild, titel, weg_lage, [Z("bibi", weg_zeile, "sadness")], [O("Walks back with her.", [])]),
    ]
    if _mo.TIERE[tid].get("allein"):                       # von diesem gibt es nur eines (Duc 01.11.2026)
        return frames
    return frames + [
        FR("mo_%s_wieder" % tid, bild, "Another %s" % name,
           "Bibi has marked a new place on her map. It's another %s, she says, with the same red light on its neck, and this one has nobody yet." % name,
           [Z("bibi", WIEDER[tid], "caring")],
           [O(los, kampf), O("Turns back. “Not today.”", [])]),
    ]


EVENTS = (
    KETTE("hund", "macchia_path", "A Dog on the Road",
          "Bibi found the marks by the road this morning. A dog has been sleeping under the same bush for a week, and it has gone for everyone who stopped. Now it stands in the middle of the road, ribs showing, teeth showing. A small steel box is bolted to its old collar, and the light on it never stops.",
          "That box is ARK's. They took strays, because nobody asks about strays. It keeps firing, and it drives them out of their heads. So tire it out, then throw Rosi's grenade. And when it's nearly down, stop hitting it. Please.", "caring",
          "Gets ready, and hates it.",
          "The road is empty. There's a little blood on it, and Bibi looks at that for a while.",
          "It'll be back at the bush tomorrow, or the day after. It's got nowhere else. Next time stop one hit sooner, okay?") +
    KETTE("hyaene", "bone_gorge", "Laughter in the Gorge",
          "You can hear it from the top of the gorge. It sounds like someone laughing at a joke they don't understand, over and over. Bibi has gone very quiet.",
          "That's one of mine. Seven one one four. Every time the collar fires, she laughs. It has been firing for three weeks. I know how that sounds. Tire her out, then the grenade. I can't do this part. I'm sorry.", "sadness",
          "Walks down into the gorge, and says nothing funny.",
          "The laughing comes down from somewhere above you. Then it stops, and that's worse.",
          "I know that place she's in. You can't chase someone out of it. We come back, and we're boring, and we come back again.") +
    KETTE("mufflon", "charcoal_road", "Steel on the Ridge",
          "Black trunks and ash. You've met her before, and you still have the bruise. She stands on the burnt road with the steel plates bolted to her shoulders and the collar blinking under them, and she hits whatever comes near.",
          "Eleven months I fed her. I thought the plates were for a broken shoulder, and they told me it was a brace. Nobody could make her do anything, so they gave her the collar, and they bolted it on while she was asleep. Now we have to put her to sleep too. I know.", "sadness",
          "Walks straight towards her and doesn't look away.",
          "She walks away through the trunks at her own speed. Nothing on this island has ever made her hurry.",
          "Yeah, that's her. She'll be back on this road tomorrow, and the collar will still be on. Stop one hit sooner, okay?") +
    KETTE("affe", "forest_edge_cliffs", "Something Is Watching",
          "Three of Petru's spanners have gone missing, and one came back clean. Bibi has followed a line of very small, very careful footprints to the foot of the cliff. A stone drops next to you. It isn't an accident. Then the collar blinks up there, and something starts screaming.",
          "He solved the feeding puzzle in a week, and it took me two to notice. For a minute he's the cleverest one here. Then the collar fires, and he isn't anybody. He'll watch the grenade all the way, so wear him out first.", "curiosity",
          "Puts down your lunch and gets ready.",
          "He's up on the cliff again. He holds up one of Petru's spanners, so you can see it. Then the collar blinks, and he drops it, and he's gone.",
          "He'll be back. He always comes back for the tools. Next time stop one hit sooner, okay? He's got nothing left by then.") +
    KETTE("wolf", "high_pasture", "The Grey One Alone",
          "High grass and a lot of wind. The wolf stands by herself at the far end of the pasture, with a collar blinking on her neck. The others you fought on this mountain ran as a pack. Nothing runs with this one. The collar has seen to that.",
          "I won't lie to you, this one could really kill you. The collar pulls hardest on the strong ones, and she's the strongest I ever had. She'll shake off that grenade until she can hardly stand. So wait for it.", "fear",
          "Walks out into the open grass, alone, and stops.",
          "Nothing on the pasture now but the wind. Bibi picks up a clump of grey fur and puts it in her pocket.",
          "She'll let us try again. She's the only one of them who's fair. Next time stop one hit sooner, okay? Just one.")
)

# Zweite Runde (Duc 01.11.2026): exotische Tiere aus der Anlage und weitere ARK-Tiere.
EVENTS += (
    KETTE("madame", "shepherd_hut_ruin", "A Very Round Problem",
          "The shepherds up here say a cat has been killing their dogs. You don't believe them, until you see it on the roof of the hut. It's grey and round and it doesn't look like much. Then the collar blinks, and it screams at you.",
          "That's Madame. She lived on Julien's desk. He called all of them subjects, but not her. He put the collar on her himself, in front of us, to show it was safe. So. Tire her out, then the grenade. Mind the hands.", "remorse",
          "Takes a step back, then remembers that it's a cat.",
          "Something moves around under the floor of the hut, and then it stops. Bibi leaves a saucer by the door.",
          "She'll come back for the saucer. She's got standards. Next time stop one hit sooner, okay?") +
    KETTE("rotpanda", "forest_edge_cliffs", "Something Red in the Trees",
          "There's something red in the top of a chestnut tree, and it's making a noise like a very small, very angry door. Bibi stares up at it. You've seen many things on this island, but you haven't seen this.",
          "He came in a crate, with a ribbon on it. There were rich people who sent us animals as gifts. The collar is too big for him, so they used tape. He can't reach it, and he's been up there for days, and he won't stop.", "sadness",
          "Shakes the tree. Feels bad about it right away.",
          "A flash of red, far off between the trees. Then there's only the noise, and then not even that.",
          "He'll get tired before we do. He's got tiny legs. Next time stop one hit sooner, okay?") +
    KETTE("capybara", "macchia_creek_bridge", "The Calmest Animal There Is",
          "Something big has been going through the fences along the creek. It looks like a huge wet guinea pig. It doesn't look angry. It looks as if it has no idea why its body keeps doing this, and the collar on its neck blinks and blinks.",
          "You know what they're famous for? Nothing bothers them. Birds sit on them. That's why ARK wanted one. They wanted to see how long it would take. It took four days. I timed it. I wrote it down.", "sadness",
          "Wades into the creek. It's colder than it looks.",
          "The fence is down again, further along. There's a wet track up the bank. Bibi looks at it and doesn't say anything for a bit.",
          "He doesn't even want to fight. That's the worst part. Next time stop one hit sooner, okay?") +
    KETTE("keiler", "ravine_fork", "Another Collar in the Macchia",
          "You've fought one of these on the monastery bridge. This one is bigger, and it has rooted up half the ravine. It keeps slamming its head against the rocks, on the side where the collar sits.",
          "That's a local one. ARK wanted animals from the island for the field tests, so if anyone found one, nobody would ask. The one on your bridge was his sister, I think. Bring the grenade, and don't stand in front of him.", "curiosity",
          "Stands in front of him anyway. There's nowhere else to stand.",
          "The whole ravine is torn up, and the sound of it is going away. Bibi kicks a stone back into its hole, for no reason.",
          "He'll be back. They don't leave their ground. Next time stop one hit sooner, okay?") +
    KETTE("baerchen", "forest_edge_cliffs", "Something Small, Again",
          "You've heard this squeal before, up in the alders on the mountain. It's Old Grey's smallest, the fat clumsy one, and it has come all the way down here alone. The red light on its neck is still blinking, and it's hitting the air with its paws.",
          "They only made the collar in one size. You saw what that did to the mother. It's going to grow into the neck, and then I can't take it off. So it has to be now. I know it's a baby. Don't hit it hard. Just... you know how little it takes.", "fear",
          "Crouches down. “Come on, then. You and me.”",
          "The alders are moving, and then they aren't. Bibi stays there for a long time, calling something quietly.",
          "It'll stay near. It doesn't know where else to go. Next time, please, just one hit less.") +
    KETTE("schildkroete", "macchia_path", "Number Twelve",
          "A very old tortoise is standing in the middle of the path, with a 12 painted on its shell. Its neck is stretched out, its mouth is open, and it is coming at you. It's coming very slowly. You have time to take this in.",
          "Twelve of forty. It was a battery test: how long does a collar last, on something that lives this long? Nobody expected the battery to go first. The others... I don't know. She's still looking for them, I think. Don't laugh. She bites like a door.", "curiosity",
          "Tries not to laugh, and stays out of reach.",
          "The path is empty. You don't understand how. You only looked away for a moment.",
          "Yes, I know. Don't look at me. She'll be a little further on tomorrow. Stop one hit sooner, okay?") +
    KETTE("geier", "foggy_ridge", "Over the Ridge",
          "Something huge is circling in the fog above the ridge, and there's a small red light going round with it. A bone drops out of the sky and breaks on the rocks next to you. Then the shape folds its wings.",
          "He's a wild one. He only came over the fence because of the food bins. They needed a bird for the range test, so they kept him. He can't land for long. Every time he does, it fires, and up he goes. When he comes down at you, that's your chance.", "fear",
          "Looks up, and keeps looking up.",
          "Only fog now, and the small red light going away in it. Then not even that.",
          "He'll be back over the ridge. He can't help it. Next time stop one hit sooner, okay?") +
    KETTE("schneeleopard", "ravine_fork", "Tracks and Nothing Else",
          "For three days Bibi has found nothing but prints, on walls, on roofs, and on your boat once. Now she's found a dead goat high on a rock, and she has gone pale. You look up. There's nothing there. You look up again.",
          "From somebody's private zoo. She cost more than this whole bay. She lived in a cage the size of your cabin, and now she's got a mountain and that thing on her neck. You won't see her come. She fights the grenade like nothing else. So wait.", "fear",
          "Puts his back against the rock.",
          "There's a print on the rock, and it's still wet. It's higher than your head. You don't remember her leaving.",
          "She let you live. Don't feel too good about it. Next time stop one hit sooner, okay?") +
    KETTE("waran", "bone_gorge", "Something Long in the Sun",
          "A long grey shape lies on the warm stones of the gorge, and two of the village's goats are lying near it, not moving. It lifts its flat head and looks at you. It doesn't get up. It has plenty of time. The collar blinks slowly, and it looks like it belongs there.",
          "A rich man's collection. It came with a certificate. Charly named him back at the lab, because he's cold, he's never in a hurry, and he lies on everything he owns. Mr. V. Don't tell anyone I laughed. One bite is enough, so don't let him start the clock.", "curiosity",
          "Walks down into the gorge. He watches you all the way.",
          "He has gone. You don't know when. There's a long smooth track in the dust, going away, and he wasn't hurrying at all.",
          "He doesn't mind. He's got all the time in the world, and he knows it. Next time stop one hit sooner, okay?")
)

# Bibi hat Rosi um die Granate gebeten (Duc 01.11.2026). Die Granaten selbst gibt Bibi vor jeder Spur (kern/mochis.kampf_vorbereiten).
EVENTS.append(E("mo_schlafgranate", "gag1", "ernst", "A Grenade for Bibi",
                WANN((11, 21), ["tag"], bed={"alle": [{"flag": "mochis_offen"}, {"flag_seit": ["rt_ende_tag", 1]}]}, pflicht=True, holt_leute=True),
                "village_harbour", {"handelnd": "bibi", "betroffen": [{"id": "rosi", "ton": "?", "was": ""}]},
                "Bibi stops you on the quay and holds out a shoebox. Rosi stands behind her, wiping her hands on a rag. In the box are small grey grenades with blue tape around them.",
                [Z("bibi", "The collars make them crazy. You've seen it. I can't get near them to cut one off. So I asked Rosi for something that doesn't kill them.", "sadness"),
                 Z("rosi", "It's a vet's sedative in a soft shell. The collar fights it. As long as the animal has strength, the collar wins. Under one in ten, it can't. Above that, you're just making it wet.", "neutral"),
                 Z("bibi", "So you have to fight them first. I know. I hate it too. And when one is nearly down, stop hitting it, or it runs, and we start again.", "remorse")],
                [O("Takes the box.", [{"flag": "mo_schlafgranate"}, V("bibi", 1)]),
                 O("“Does it hurt them?”", [{"flag": "mo_schlafgranate"}, V("bibi", 1)],
                   zeile=Z("rosi", "Less than the collar does. Now take the box. I have an engine in pieces.", "neutral"))],
                {"bibi": "Mochis", "rosi": "Engine Room"}))

# Drei Halsbaender (kern/mochis._halsband): Bibi bringt sie zu Elsa. Merker mo_ark_beweis fuer die Kommission an Tag 35 (Wiki systeme/tierstation.md).
EVENTS.append(E("mo_halsbaender", "gag1", "ernst", "A Box of Collars",
                WANN((11, 21), ["tag"], bed={"alle": [{"flag_seit": ["rt_ende_tag", 1]}, {"flag": "mo_halsband_3"}]}, pflicht=True, holt_leute=True),
                "village_harbour", {"handelnd": "bibi", "betroffen": [{"id": "elsa", "ton": "?", "was": ""}]},
                "Bibi puts a shoebox on the quay in front of Elsa and takes off the lid. Inside there are steel collars, cut open, each with a lab number. Elsa looks into the box for a long time without touching it.",
                [Z("bibi", "Every number in there was an animal. I can tell you what each of them weighs. I fed them. I signed for them.", "sadness"),
                 Z("elsa", "A statement can be called a lie, Miss Bibi. A number on a steel collar is much harder to call a lie. Who else has seen these?", "approval")],
                [O("“Only us.”", [{"flag": "mo_ark_beweis"}, V("elsa", 4), V("bibi", 2)]),
                 O("“Keep them away from the town hall.”", [{"flag": "mo_ark_beweis"}, {"flag": "mo_beweis_bei_elsa"}, V("elsa", 2)],
                   zeile=Z("elsa", "I didn't ask for advice, First Officer. ...I have a safe at home. It's a very old safe.", "neutral"))],
                {"bibi": "Mochis", "elsa": "Standard"}))


def _nach(z, opts):
    """Zeile, die nur gilt, wenn die Bedingung passt: je Gruppe die erste passende (kern/ereignisse.zeilen_aktiv)."""
    return dict(z, **opts)


# Die Kommission an Tag 35 (E-096) sieht die Halsbaender. Wie viel sie wert sind, haengt an Ducs Antwort in mo_halsbaender: kern/mochis.beweis_stand.
EVENTS.append(E("mo_kommission", "gag1", "ernst", "A Shoebox for the Commission",
                WANN((35, 35), ["tag"], bed={"flag": "mo_ark_beweis"}, pflicht=True, holt_leute=True),
                "village_harbour", {"handelnd": "elsa", "betroffen": [{"id": "bibi", "ton": "?", "was": ""}]},
                "Two men from the commission in Ajaccio have set up a folding table on the quay, with a clerk and a lot of paper. They have been very polite to everyone. Elsa puts a shoebox on the table and takes off the lid. It's the box Bibi brought to the quay weeks ago: steel collars, cut open, each with a lab number.",
                [_nach(Z("elsa", "These have been in the safe at my home since the day I got them. That is my seal, and nobody has broken it. Please check it. I would like you to check it.", "approval"),
                       {"gruppe": "siegel", "wenn": {"flag": "mo_beweis_bei_elsa"}}),
                 _nach(Z("elsa", "I logged these at the town hall, as the rules say. Then they were gone for a while. When I found them again, my seal was broken. I still have every number, and I'm telling you this before their lawyers do.", "sadness"),
                       {"gruppe": "siegel"}),
                 Z("bibi", "Every number in that box has a name now. I can tell you what each of them weighs. You can write that down too.", "neutral"),
                 Z("elsa", "The gentleman wants to know who cut them off, First Officer. Will you tell him?", "neutral")],
                [O("Points at Bibi. “She did. Every one of them.”", [{"flag": "mo_kommission_gesehen"}, V("bibi", 2), W("ruf", 1)]),
                 O("Steps up to the table. “We did. Put my name next to hers.”", [{"flag": "mo_kommission_gesehen"}, V("bibi", 3), V("elsa", 2)],
                   zeile=Z("bibi", "You don't have to do that. ...All right. Spell it for him.", "gratitude"))],
                {"bibi": "Mochis", "elsa": "Standard"}))


# Epilog (Duc 01.11.2026): Alle kommen frei, je Tier ein Frame mit seinem Bild ohne Halsband (tier_bild, eden-expedition). Pflicht am letzten Tag; Akt 3 kann den Zeitpunkt noch schieben.
def _frei_folge():
    return [{"wenn": {"flag": "mo_tier_%s" % t}, "id": "mo_frei_%s" % t} for t in _mo.ABSCHIED]


def _frei_ab(tid):
    """Naechstes gerettetes Tier nach tid, sonst der Schluss."""
    reihe = list(_mo.ABSCHIED)
    return _frei_folge()[reihe.index(tid) + 1:] + [{"id": "mo_frei_ende"}]


EVENTS.append(E("mo_frei_start", "gag1", "wholesome", "The Gates",
                WANN((35, 35), ["nachmittag"], bed={"flag": "mo_tier_da"}, pflicht=True, holt_leute=True),
                "mochis", {"handelnd": "bibi", "betroffen": [{"id": "danzel", "ton": "?", "was": ""}]},
                "Bibi has been up since before light. She has cleaned every pen at Mochi's, which makes no sense, because nobody is going to need them. Now she stands at the first gate with the field book under one arm and the key in her hand. She has been standing there for a while.",
                [Z("bibi", "They're fat, they're bored, and they have started looking at the hills. That's what healthy looks like. I wrote that in my notes weeks ago, and then I didn't do anything about it.", "caring"),
                 Z("danzel", "I pressed my best waistcoat for this. Yes, for the animals. A farewell is a farewell, and somebody here should be dressed for it.", "caring"),
                 Z("bibi", "They were never mine, you know. I signed for them once, and look how that went. So today I'm not signing for anything. I'm only going to open the gates, one at a time. Will you stay for it?", "sadness")],
                [O("Takes the key from her hand. “I'll do the first one.”", [V("bibi", 2), {"direkt": _frei_folge() + [{"id": "mo_frei_ende"}]}]),
                 O("Stays next to her. “Of course I'll stay.”", [V("bibi", 1), {"direkt": _frei_folge() + [{"id": "mo_frei_ende"}]}])],
                dict(BIBI, danzel="danzel_B")))
for _t, (_wort, _zeile, _gefuehl) in _mo.ABSCHIED.items():
    _e = FR("mo_frei_%s" % _t, "mochis", _mo.TIERE[_t]["name"], _mo.TIERE[_t]["text_frei"], [Z("bibi", _zeile, _gefuehl)],
            [O("Watches %s go." % _wort, [WEITER(_frei_ab(_t))])], ton="wholesome")
    _e.update(flott=True, tier_bild="/kampfbild/%sFrei/idle.webp" % _mo.TIERE[_t]["sprite"])
    EVENTS.append(_e)
EVENTS.append(FR("mo_frei_ende", "mochis", "The Gates",
                 "The last gate stands open. The pens are very quiet now, and the evening light lies on all that clean straw. Bibi sits down on the wall, opens the field book at the first page and looks at it. Then she closes it.",
                 [_nach(Z("bibi", "That's all of them, every page. I never finished anything before in my life. I don't know what you're supposed to do after.", "gratitude"), {"gruppe": "buch", "wenn": {"flag": "mo_buch_voll"}}),
                  _nach(Z("bibi", "There are still some out there with the light on. I know where they sleep. I'll go up tomorrow, and the day after, and I'll be boring about it.", "caring"), {"gruppe": "buch"}),
                  _nach(Z("bibi", "And him? He never needed a gate. Somebody should tell him he has a very nice sign.", "gratitude"), {"gruppe": "mochi", "wenn": {"flag": "kl_loewe_frei"}}),
                  _nach(Z("bibi", "I'm still going to put his food out tonight. I know. Don't say anything.", "sadness"), {"gruppe": "mochi"})],
                 [O("Sits down on the wall next to her.", [{"flag": "mo_freigelassen"}, V("bibi", 3), W("ruf", 2)])], ton="wholesome"))

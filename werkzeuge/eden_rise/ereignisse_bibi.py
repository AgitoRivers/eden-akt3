# -*- coding: utf-8 -*-
"""Bibis Arc (Duc 02.11.2026, docs/brain_trust/BIBI_ARC_TEXTE.md): gemeinsame Arbeit an der Station, ihre Romanzen-Leiter und das Geständnis im Field Book.

Die Arbeit gilt fuer alle mit `mochis_offen`, die Leiter nur, wenn sie Romanze ist (personen.bibi.romanze_flags, kern/rollen.romanze_abgleichen).
Kosenamen nur auf dem Romanzen-Weg, sonst bleibt sie bei Clipboard. Noch nicht vertont."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_ligeia import G
from ereignisse_romanzen import ABEND, AB, DIREKT, FD, N

SET = {"bibi": "Mochis"}
ROMANZE = [{"flag": "mochis_offen"}, {"flag": "kl_loewe_frei"}, {"flag": "rt_ausgang_alle"}, {"flag": "rt_bibi_bleibt"}]
LIEBE = {"alle": ROMANZE}


def _je(z, gruppe, wenn=None):
    """Zeile nur, wenn die Bedingung passt: je Gruppe die erste passende (kern/ereignisse.zeilen_aktiv)."""
    return dict(z, gruppe=gruppe, **({"wenn": wenn} if wenn else {}))


def ARBEIT(id, titel, seit, lage, zeilen, optionen, ton="wholesome", wenn=None):
    """Ein kurzer gemeinsamer Handgriff an der Station, Pflicht und ohne Phase, wie mo_schlafgranate."""
    # Bis Tag 33 (Duc 05.11.2026, Dichte-Check Akt 3): an Tag 34 (Villa) und 35 (Kommission) kein Handgriff an der Station
    wann = WANN((11, 33), ["tag"], bed={"alle": [{"flag": "mochis_offen"}, {"flag_seit": ["rt_ende_tag", seit]}, N(id)] + ([{"flag": wenn}] if wenn else [])}, pflicht=True, holt_leute=True)
    e = E(id, "gag1", ton, titel, wann, "mochis", {"handelnd": "bibi", "betroffen": []}, lage, zeilen, optionen, SET)
    e["solo"] = True
    return e


ARBEITEN = [
    ARBEIT("mo_a_zaun", "The Fence", 2,
           "Bibi has one post in the ground and a pile of others, and she waves you over with a hammer. It's the first fence at Mochi's. Whatever it's meant to keep in is already standing on the other side, watching.",
           [G("bibi", "Hold this post. No, straight. No, your other straight. [chuckle] You look at my fence like it owes you a report, Clipboard. Have you ever held anything?", "amusement"),
            G("bibi", "That's the worst fence I've ever seen. [laugh] Good! They can't work out how to get through it, because neither of us knows where it starts. So what do you think, is it finished?", "joy")],
           [O("“It's finished. Nobody's ever going to audit this.”", [F("mo_a_zaun"), V("bibi", 3)]),
            O("Takes the hammer and fixes the worst post without a word.", [F("mo_a_zaun"), V("bibi", 4)],
              zeile=G("bibi", "Hey. [gasp] You've done that before. Where does a consultant learn to do that?", "surprise"))]),
    ARBEIT("mo_a_dach", "Half a Roof", 5,
           "You find Bibi on top of the old sheep pen with a mouthful of nails, and half a roof is still all there is. She spits the nails into her hand when she sees you.",
           [_je(G("bibi", "Pass me the nails, mon lapin. Not all of them. [laugh] Why would I need all of them?", "amusement"), "wort", LIEBE),
            _je(G("bibi", "Pass me the nails, Clipboard. Not all of them. [laugh] Why would I need all of them?", "amusement"), "wort"),
            G("bibi", "We've got three quarters of a roof now, and I'm telling everybody. [chuckle] I'm having it printed on something. What should it say?", "joy")],
           [O("“Three quarters of a roof. Four quarters of a heart.”", [F("mo_a_dach"), V("bibi", 3)],
              zeile=G("bibi", "That's terrible. [laugh] I'm printing it.", "joy")),
            O("“Under new management. Please mind the hyena.”", [F("mo_a_dach"), V("bibi", 3)],
              zeile=G("bibi", "Her name's Sorry, and she'd like that in bigger letters. [chuckle]", "amusement"))]),
    ARBEIT("mo_a_bad", "Bath Day", 8,
           "There's a tin tub in the yard, a lot of mud and a very large animal that has understood what the tub is for. Bibi rolls up her sleeves and points at the end of it that's closest to you.",
           [G("bibi", "He doesn't like water, so you hold the front and I'll hold the back. [sigh] The front is the bad end. I should have said that first.", "nervousness"),
            _je(G("bibi", "You've got mud in your ear, mon canard. It means my duck, you walk like one in those boots. [chuckle] No, leave the mud. It suits you.", "amusement"), "wort", LIEBE),
            _je(G("bibi", "You've got mud in your ear, Clipboard. [chuckle] No, leave it. It suits you.", "amusement"), "wort")],
           [O("Puts a hand of mud on her nose, very carefully.", [F("mo_a_bad"), V("bibi", 4)],
              zeile=G("bibi", "Oh, you're dead. [laugh] You're dead, and nobody will find you, because I know where the hyenas sleep.", "joy")),
            O("“Same time next week?”", [F("mo_a_bad"), V("bibi", 3)],
              zeile=G("bibi", "You came back for this on purpose? [chuckle] Okay. You're a very strange man. Bring boots.", "joy"))], wenn="mo_tier_da"),
    ARBEIT("mo_a_schraube", "The Spanner", 11,
           "Petru's spanner is on top of the wall at Mochi's. So is the ape, and he is holding it. Bibi stands below them with a banana behind her back, trying to look like a person who has no banana.",
           [G("bibi", "Petru wants his spanner back, and he wants to keep it, and I've told them both it's a matter for the courts. [chuckle] You distract him. You've got the face for it.", "amusement"),
            _je(G("bibi", "You came up here on your day off to help me steal from an ape, ma puce. It means flea. You keep coming back, and I can't get rid of you. [sigh] I just want you to know that I noticed.", "love"), "wort", LIEBE),
            _je(G("bibi", "You came up here on your day off to help me steal from an ape, Clipboard. [sigh] I just want you to know that I noticed.", "gratitude"), "wort")],
           [O("“Somebody should look after you, too.”", [F("mo_a_schraube"), V("bibi", 5)],
              zeile=G("bibi", "Nobody's asked me that since – [sniff] okay. Okay. Hold the banana.", "gratitude")),
            O("“I want it in writing that the ape won.”", [F("mo_a_schraube"), V("bibi", 3)],
              zeile=G("bibi", "The ape always wins. [laugh] That's the first thing you learn.", "joy"))], wenn="mo_tier_affe"),
]


def _leiter(id, tage, phase, *bed):
    w = WANN(tage, [phase], bed={"alle": ROMANZE + list(bed)}, pflicht=True, holt_leute=True)
    w["leiter"] = True
    return w


LEITER = [
    ABEND("rm_b1", "wholesome", "A Very Honest Refund", _leiter("rm_b1", (15, 35), "abend", *AB("bibi", 3, 3), N("rm_b1")), "mochis", "bibi",
          "Evening on the wall at Mochi's, with your boots in the straw. Rich people keep coming up the hill to ask if they can have a photo with the wolf, and Bibi keeps telling them no. Tonight she has a stub of pencil and the back of a feed bill.",
          [G("bibi", "So they want a photo with the wolf, and the answer's no, okay, but I've been thinking. What if they pay? [gasp] Forty euros to walk up a hill with one of us and maybe see nothing. No cages and no feeding show. If the snow leopard doesn't feel like it, you get a very nice walk.", "joy"),
           G("bibi", "And there's no refund. I'd like that written very clearly. [chuckle] You do numbers, mon chou. It means cabbage, don't look at me, I didn't invent France. Is that the stupidest thing you've ever heard?", "nervousness")],
          [O("“No. I've been telling companies this for ten years, and nobody ever said it that well.”", [FD("rm_b1"), F("mo_eco_idee"), V("bibi", 6)],
             zeile=G("bibi", "You're not being nice? [sniff] You'd tell me if you were being nice. Okay. Show me how the numbers go.", "gratitude")),
           O("“It's a terrible business plan. Show me the rest of it.”", [FD("rm_b1"), F("mo_eco_idee"), B("bibi", 6), V("bibi", 2)],
             zeile=G("bibi", "There's a lot more of it. [laugh] It's on four bills and a goat. Sit closer, you can't read it from there.", "desire")),
           O("“Fifty euros. People trust it more if it hurts.”", [FD("rm_b1"), F("mo_eco_idee"), V("bibi", 3), B("bibi", 3)],
             zeile=G("bibi", "Fifty! You're horrible. [laugh] Fifty it is, and you're doing the sign.", "joy"))],
          "Mochis"),
    ABEND("rm_b2", "wholesome", "The Bottle", _leiter("rm_b2", (15, 35), "nacht", *AB("bibi", 3, 4), {"flag_seit": ["rm_b1", 1]}, N("rm_b2")), "mochis", "bibi",
          "Bibi has asked you up after dark, because the smallest one at Mochi's won't take the bottle from her tonight. There's one lamp in the pen, and she has washed her face. You sit down in the straw with something warm and furious on your knees.",
          [G("bibi", "Go slow, and don't look at it like a report. [sigh] There. Look at that. It's asleep on your arm, so now you can't move for an hour, Bärchen. I don't make the rules.", "love"),
           G("bibi", "I'm usually talking by now. [sigh] I keep looking at you in the lamp, and I've forgotten what I was going to say, and that's never happened. Do you want me to go on standing over here?", "nervousness")],
          [O("Moves the arm that isn't asleep. “Come here, then.”",
             [FD("rm_b2"), V("bibi", 4), INTIM("bibi", "mochis", "Mochis", "bibi",
                                               "The lamp is low and nothing in the pen is awake. Bibi talks too fast at first and then, for once, she stops. She laughs at the wrong moments, and she means it. Nobody is in a hurry, and she asks before she does anything new.")],
             zeile=G("bibi", "Careful of the arm. [chuckle] I've got feeding at six, and I don't care.", "desire")),
           O("“Stay there and tell me about it. I've got an hour.”", [FD("rm_b2"), V("bibi", 7)],
             zeile=G("bibi", "You'll regret that. [laugh] So, this one came with the wrong paperwork –", "gratitude")),
           O("“Not tonight, I think. I'd like to stay until it wakes up, though.”", [FD("rm_b2"), V("bibi", 5)],
             zeile=G("bibi", "Yeah. [sigh] Yeah, okay. That's a good answer, you know. Nobody ever stays for the waking up.", "gratitude"))],
          "Mochis"),
    ABEND("rm_b3", "ernst", "The Brochure", _leiter("rm_b3", (15, 35), "abend", *AB("bibi", 4, 4), {"flag": "mo_eco_idee"}, {"flag_seit": ["rm_b2", 1]}, N("rm_b3")), "mochis", "bibi",
          "Elsa has asked you to look through the ARK papers, because you read this kind of thing for a living. Bibi is mending a feed sack beside you on the wall. You read out the front of a glossy brochure, the way you'd read it to a client: “Ark. A rescue programme for animals with nowhere else to go.”",
          [G("bibi", "What do you think of it? [clear throat] As a professional, I mean. You've read a lot of these.", "neutral")],
          [O("“Whoever wrote this was good. That's the best greenwashing I've seen in years.”", [FD("rm_b3"), DIREKT("rm_b3_b")])],
          "Mochis"),
    ABEND("rm_b3_b", "ernst", "The Brochure", WANN((15, 35), bed={"flag": "mochis_offen"}), "mochis", "bibi",
          "Bibi has stopped sewing. She looks at the sack and not at you.",
          [G("bibi", "Thank you. [sigh]", "sadness"),
           G("bibi", "I was twenty-two. I had a notebook with a zoo in it, no fences, and I'd been drawing it since school. I showed it to Julien on our third date. [sniff] He said it was beautiful, and he asked if he could keep it.", "sadness"),
           G("bibi", "He kept it. That's my sentence. I told you everything, you know, every animal and every name. [sigh] I didn't tell you that one. So, what do you do with that?", "embarrassment")],
          [O("“You wrote it because you meant it. He's the one who sold it.”", [F("bibi_prospekt"), V("bibi", 8)],
             zeile=G("bibi", "I know that. [sniff] I mean, I don't. Say it again sometime, when I'm not looking at you.", "gratitude")),
           O("“Show me the notebook. The real one.”", [F("bibi_prospekt"), V("bibi", 5), B("bibi", 5)],
             zeile=G("bibi", "Nobody's seen it since. [sigh] It's got crayon in it. If you laugh, I'll set Sorry on you.", "embarrassment")),
           O("“Then you're the best copywriter Alon ever had. Let's take it back.”", [F("bibi_prospekt"), V("bibi", 5)],
             zeile=G("bibi", "Ha! [laugh] Oh, I'd like that. I'd like to see his face. I want to be the first thing he sees.", "pride"))],
          "Mochis"),
    # Das Geständnis (Duc 02.11.2026): die letzte Seite im Field Book, nach den Toren. Wird im Buch sichtbar ueber das Flag bibi_seite (kern/mochis).
    ABEND("rm_b4", "wholesome", "Last Page", _leiter("rm_b4", (35, 35), "abend", *AB("bibi", 4, 4), {"flag": "mo_freigelassen"}, N("rm_b4")), "mochis", "bibi",
          "The gates stand open, and everything is very quiet. Bibi sits down next to you and pushes the field book against your knee. Then she looks somewhere else.",
          [G("bibi", "That's all of them, every page. Well, nearly. Have you looked at the last one? [clear throat] You don't have to look at the last one. Did you know a vulture can digest bones? So that's interesting.", "nervousness")],
          [O("Opens it at the end.", [FD("rm_b4"), F("bibi_seite"), DIREKT("rm_b4_b")])],
          "Mochis"),
    ABEND("rm_b4_b", "wholesome", "Last Page", WANN((15, 35), bed={"flag": "mochis_offen"}), "mochis", "bibi",
          "It's a page like all the others, with a photo clipped to it: you, in the yard, with mud in your ear. *Name:* Clipboard, Mon lapin, Hase, Mon canard, Mon chou, Bärchen, each one crossed out, and under them, in careful pencil, *Spatz*. *Favourite food:* mine, sadly. *Bites:* only people he likes. *Release:* no. And then, smaller: ...Ask him first.",
          [G("bibi", "I stayed in Marseille for a man once, and this is not that. This place is mine, and it stays mine. [sigh] And I'm not signing for you. I signed for things before. I'm only asking.", "nervousness")],
          [O("“Ask me, then.”", [F("bibi_gefragt"), V("bibi", 6), B("bibi", 6), DIREKT("rm_b4_frage")]),
           O("“You've spelled it wrong. It's only got one bite.”", [F("bibi_gefragt"), V("bibi", 4), B("bibi", 6), DIREKT("rm_b4_frage")]),
           O("“I saw that outline weeks ago. I've been trying to walk like it.”", [F("bibi_gefragt"), V("bibi", 6), B("bibi", 4), DIREKT("rm_b4_frage")])],
          "Mochis"),
    # Die Frage, die weh tut (Duc 05.11.2026, docs/brain_trust/BIBI_ENDE.md Bild 2): Die Yacht ist repariert, Schiffe fahren ab.
    # Die ehrliche Antwort tut am meisten weh und bringt das meiste Vertrauen. Die Enden lesen a3_bibi_antwort_<n> (kern/abschluss.py).
    ABEND("rm_b4_frage", "wholesome", "Last Page", WANN((15, 35), bed={"flag": "mochis_offen"}), "mochis", "bibi",
          "She closes the book over her finger, so she doesn't lose the page.",
          [G("bibi", "[clear throat] So. The yacht is fixed. Ships leave, that's the whole point of them. I'm not asking you to stay. "
                     "I'm asking you a smaller thing. Will you come back?", "nervousness")],
          [O("“I'm not going anywhere.”", [F("a3_bibi_antwort_bleiben"), V("bibi", 4), B("bibi", 4), DIREKT("rm_b4_c")],
             zeile=G("bibi", "[laugh] Don't say that. ...No, say it again. Slowly. I'm writing it down.", "love")),
           O("“Every season. I'll bring the bad weather.”", [F("a3_bibi_antwort_saison"), V("bibi", 4), B("bibi", 4), DIREKT("rm_b4_c")],
             zeile=G("bibi", "[chuckle] Every season. Okay. I'll keep your bowl. That's a joke! ...It's not a joke.", "love")),
           O("“I don't know yet. That's the truth.”", [F("a3_bibi_antwort_ehrlich"), V("bibi", 6), B("bibi", 6), DIREKT("rm_b4_c")],
             zeile=G("bibi", "[sniff] Thank you. Everybody I ever loved said yes. You're the first one who said the true thing.", "love"))],
          "Mochis"),
    ABEND("rm_b4_c", "wholesome", "Last Page", WANN((15, 35), bed={"flag": "mochis_offen"}), "mochis", "bibi",
          "She stops writing. The pencil rolls off the wall into the straw, and neither of you picks it up. For once she doesn't laugh, "
          "and she doesn't say sorry. She looks at the page for a long time.",
          [G("bibi", "Spatz. My mother calls me that. Every Sunday, on the phone. [sigh] Now you know everything. This time it's true.", "gratitude")],
          [O("Stays on the wall with her until it's dark.", [])],
          "Mochis"),
]

EVENTS = ARBEITEN + LEITER

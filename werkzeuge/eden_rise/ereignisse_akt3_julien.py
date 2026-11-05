# -*- coding: utf-8 -*-
"""Akt 3: Julien Vasseur holt "seine" Tiere (Duc 05.11.2026, docs/brain_trust/BIBI_ENDE.md).

Tag 35, Nachmittag, an den Toren (mo_frei_start oeffnet a3_julien per DIREKT, wenn JULIEN gilt): Bibi steckt den
Schluessel ins erste Schloss, da kommen drei schwarze Autos. Julien, Leiter von ARK und Bibis Ex, hat Papiere aus
Marseille und vier Agenten. Er will die Tiere zurueck, vor allem Madame, die Katze von seinem Schreibtisch.
Duc stellt sich vor Bibi: Kampf a3_julien (kaempfe_akt3.py, keine Flucht).
  Sieg (a3_julien_besiegt)      a3_julien_sieg: Bibi nimmt ihr Wort "rescue" zurueck, Madame geht an Julien vorbei zu Bibi,
                                Julien flieht und kommt nie wieder (a3_julien_weg).
  Niederlage (a3_julien_niederlage)  a3_julien_tiere: Bibi oeffnet alle Tore auf einmal, ihre Tiere jagen die Agenten,
                                danach dasselbe Ende fuer Julien.
Beide Folgen sind Pflicht mit prolog=True, damit sie direkt nach dem Kampf kommen (eden.py: nach einem Kampf zieht die
Engine nur Prolog-Pflichten). Danach geht es mit den Toren weiter (_frei_folge aus ereignisse_mochis).
Jede gesprochene Zeile mit Turbo-Tag (G). Ton ernst bis zum Kampf, danach wholesome."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import AKT3, FL, NICHT, JE, FRAME, DIREKT, tags_fuer  # noqa: E402
import ereignisse_mochis as _mochis  # noqa: E402

KAMPF = lambda bid: {"kampf": bid}
JULIEN = {"alle": [FL("rt_bibi_bleibt"), FL("mochis_offen"), NICHT(FL("a3_julien_ende"))]}
TORE = DIREKT(_mochis._frei_folge() + [{"id": "mo_frei_ende"}])
MADAME = FL("mo_tier_madame")


def _danach(bed):
    return WANN((35, 35), ["nachmittag"], bed={"alle": [AKT3, bed, NICHT(FL("a3_julien_ende"))]}, pflicht=True, prolog=True, holt_leute=True)


EVENTS = [
    E("a3_julien", "gag1", "ernst", "ARK's Delegation", FRAME(), "mochis",
      P1("julien", ("bibi", "-", "holds the key very tight"), ("danzel", "?", "is standing very still")),
      "Bibi has the key in the first lock when the cars come up the dirt road. Three of them, black, too clean for this island. "
      "A man gets out of the first one. Good coat, good shoes, a tablet under his arm. Behind him, four men in dark suits.",
      [G("bibi", "[laugh] Ha! Julien! Ha. ...Sorry. I do that when I'm scared.", "nervousness"),
       G("julien", "[clear throat] Bibiane. You look tired. These subjects belong to ARK. A court in Marseille signed the papers on Friday. "
                   "My men will load them now. You can keep the pens.", "neutral"),
       G("bibi", "[sigh] They have names. In two years you never asked for one name.", "anger"),
       JE(G("julien", "[sigh] Names are for pets. ...Except one. Where is Madame? She comes with me. She always liked my desk.", "neutral"), "madame", MADAME),
       JE(G("julien", "[sigh] Names are for pets. Gentlemen, start with the big ones.", "neutral"), "madame", None),
       G("danzel", "[gasp] Duc. The papers are real. I can see the stamp from here. I hate that I can see the stamp.", "fear"),
       G("julien", "[clear throat] And you are the man from the yacht. Step aside, please. This is not your business, and it is not your island.", "neutral")],
      [O("Steps between Julien and the gate.", [F("a3_julien_gestellt"), V("bibi", 3), KAMPF("a3_julien")],
         zeile=G("julien", "[sigh] Gentlemen. Please.", "neutral")),
       O("“They're not subjects. Get off her land.”", [F("a3_julien_gestellt"), V("bibi", 3), KAMPF("a3_julien")],
         zeile=G("bibi", "[sniff] ...Her land. Did you hear that, Julien? Her land.", "pride"))],
      sets={"bibi": "Mochis", "danzel": "danzel_B"}),

    # Sieg: Duc hat gewonnen. Closure fuer Bibi, Julien geht fuer immer.
    E("a3_julien_sieg", "gag1", "wholesome", "ARK's Delegation", _danach(FL("a3_julien_besiegt")), "mochis",
      P1("bibi", ("julien", "-", "is walking backwards to his car")),
      "The agents sit in the straw and hold their heads. Julien has the tablet in front of his chest like a shield. "
      "Bibi walks up to him. Not fast. She stops so close that he has to look at her.",
      [G("bibi", "[sigh] Julien. The word 'rescue' in your brochure. I wrote that. I believed it. It was mine, and I'm taking it back.", "pride"),
       G("julien", "[clear throat] This isn't over, Bibiane. I have lawyers. I have the papers.", "anger"),
       JE(G("julien", "[clear throat] Madame. Come.", "neutral"), "katze", MADAME),
       JE(G("bibi", "[laugh] Look. She walked right past you. She's sitting on my foot. Even the cat read your papers, Julien.", "pride"), "katze2", MADAME),
       G("bibi", "[sniff] Go home. And don't send anybody. Next time I won't need him.", "pride")],
      [O("Holds out his hand for the papers and tears them in half.", [F("a3_julien_ende"), F("a3_julien_weg"), V("bibi", 4), TORE],
         zeile=G("julien", "[gasp] Those were... Fine. Fine. Keep your goats.", "anger")),
       O("“Elsa is on her way. She would love to read those papers.”", [F("a3_julien_ende"), F("a3_julien_weg"), V("bibi", 4), TORE],
         zeile=G("bibi", "[chuckle] He's running. In those shoes. ...He'll never come back here. Never. I can feel it in my teeth.", "relief"))],
      sets={"bibi": "Mochis"}),

    # Niederlage: Duc liegt am Boden. Bibi oeffnet alle Tore auf einmal, ihre Tiere jagen die Agenten vom Hof.
    E("a3_julien_tiere", "gag1", "wholesome", "Her Land", _danach(FL("a3_julien_niederlage")), "mochis",
      P1("bibi", ("julien", "-", "drops his tablet")),
      "You are in the straw. An agent has his boot on your hand. Behind you, a lock clicks. Then another one. Then all of them. "
      "Bibi has opened every gate at once.",
      [G("bibi", "[laugh] You wanted them back, Julien? Here. Have them!", "pride"),
       JE(G("bibi", "[gasp] Sorry! Go! Bite the shiny shoes!", "excitement"), "hyaene", FL("mo_tier_hyaene")),
       JE(G("bibi", "[laugh] Duchess, the tall one. Yes. Him.", "excitement"), "mufflon", FL("mo_tier_mufflon")),
       JE(G("bibi", "[laugh] Biscuit, no, that's my sleeve! ...Okay, his sleeve. Good boy.", "excitement"), "hund", FL("mo_tier_hund")),
       JE(G("bibi", "[gasp] Bones! From above! He's never done that before!", "excitement"), "geier", FL("mo_tier_geier")),
       JE(G("bibi", "[laugh] Go on, all of you! Show them what a rescue looks like!", "excitement"), "rest", None),
       G("julien", "[gasp] Get them off! These are ARK property! ...Gentlemen? Gentlemen!", "fear"),
       JE(G("julien", "[clear throat] Madame. Madame, come here.", "fear"), "katze", MADAME),
       JE(G("bibi", "[chuckle] She's sitting on my foot, Julien. She chose. Everybody here chose.", "pride"), "katze2", MADAME),
       G("bibi", "[sniff] Go home. You'll never come back here. And Duc, get up. You stood in front of my gate. Nobody ever stood in front of my gate.", "gratitude")],
      [O("Gets up and watches the cars leave.", [F("a3_julien_ende"), F("a3_julien_weg"), V("bibi", 5), TORE],
         zeile=G("bibi", "[laugh] They're coming back. All of them. Of course they're coming back. Now we do it properly. One gate at a time.", "joy")),
       O("Takes her hand. It's shaking.", [F("a3_julien_ende"), F("a3_julien_weg"), V("bibi", 5), B("bibi", 2), TORE],
         zeile=G("bibi", "[sigh] Shaking. Yes. Don't let go yet. ...Okay. Now. One gate at a time.", "love"))],
      sets={"bibi": "Mochis"}),
]


# Einhaengen in die Tore (ereignisse_mochis) und in Bibis letzte Stufe (ereignisse_bibi), hier gesammelt, damit Bibis Ende an
# einer Stelle steht. 1) mo_frei_start: erst Julien, wenn JULIEN gilt, sonst gleich die Tiere.
# 2) mo_frei_ende: "Last Page" (rm_b4) gleich danach am Nachmittag statt am Festa-Abend (Bot-Bericht 05.11.2026).
import ereignisse_bibi as _bibi  # noqa: E402
_IDX = {e["id"]: e for e in _mochis.EVENTS + _bibi.EVENTS}
for _o in _IDX["mo_frei_start"]["optionen"]:
    for _f in _o["folgen"]:
        if "direkt" in _f and not any(d.get("id") == "a3_julien" for d in _f["direkt"]):
            _f["direkt"] = [{"wenn": JULIEN, "id": "a3_julien"}] + _f["direkt"]
_RM_B4 = dict(_IDX["rm_b4"]["wann"]["bedingung"])
for _o in _IDX["mo_frei_ende"]["optionen"]:
    if not any("direkt" in _f for _f in _o["folgen"]):
        _o["folgen"].append({"direkt": [{"wenn": _RM_B4, "id": "rm_b4"}]})


# Neue Zeilen in den Toren (ereignisse_mochis nutzt Z ohne Tag): gesprochene Fassung hier, Quelle akt3_bibi
TORE_STIMME = [
    ("bibi", "Seven and a half kilos, exactly the same as the day she came. Go on, Madame. ...She's sitting on my foot. She's sitting on my foot! Fine. Fine! You're staff now. Unpaid.",
     "Seven and a half kilos, exactly the same as the day she came. Go on, Madame. ...She's sitting on my foot. [laugh] She's sitting on my foot! Fine. Fine! You're staff now. Unpaid."),
    ("bibi", "Look. Up there, where the macchia ends. Something gold, in the last sun. He came. He doesn't need a gate, and he came anyway. Don't move. If you move, he goes.",
     "[gasp] Look. Up there, where the macchia ends. Something gold, in the last sun. He came. [sniff] He doesn't need a gate, and he came anyway. Don't move. If you move, he goes."),
    ("bibi", "I know he's not coming. You told me in the cave, and you didn't lie to me. I'm putting it out anyway. Some things you do for the one who's left.",
     "[sigh] I know he's not coming. You told me in the cave, and you didn't lie to me. I'm putting it out anyway. Some things you do for the one who's left."),
]


def tags_schreiben():
    n = tags_fuer(EVENTS + [_IDX["rm_b4_frage"], _IDX["rm_b4_c"]], "akt3_julien")
    import json, os
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    paare = {(w, t) for w, t, _ in TORE_STIMME}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "akt3_bibi" and (z["wer"], z["text"]) not in paare] \
        + [{"wer": w, "text": t, "gesprochen": g, "quelle": "akt3_bibi"} for w, t, g in TORE_STIMME]
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return n + len(TORE_STIMME)

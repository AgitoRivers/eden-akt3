# -*- coding: utf-8 -*-
"""Holm kommt zurueck (Duc 30.10.2026, Woche 3): drei Pflicht-Events an einem Tag, danach die Schiesswette um Gemelli.

  Nachmittag  hb_zurueck  sie zaehlt die Crew und dankt
  Abend       hb_megan    was Megan erzaehlt hat: je ein Satz zu Macchia, Bergen und Grotte (Zeilen mit "gruppe"/"wenn",
                          kern/ereignisse.zeilen_aktiv), dann will sie auf den Kai und kommt mit dem Koffer nicht weit
  Nacht       hb_koffer   sie verschenkt das Erbstueck nicht, sie verleiht es dem besten Schuetzen: Flag holm_wette_offen

Die Wette selbst: kern/schiessen.py, Minispiel im Plugin eden-schiessen. Gegner: Adrien (Weg C) oder Rosi, Elsa, Wolff, ab
Akt 3 Holm. hb_g_<gegner> ist die Szene beim ersten Treffen, hb_w_<gegner> liefert die vertonten Saetze nach dem Spiel
(z0 Sieg, z1 Niederlage, bei Holm z2 bis z4 die Geschenke). Diese und hb_sieg/hb_nochmal oeffnet die Engine; gezogen werden
sie nie (Flag NIE)."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_gag1 import P1  # noqa: E402

TAG = 18                         # Platzhalter, bis Woche 3 steht
PFL = lambda phase, bed=None: WANN((TAG, TAG), [phase], bed=bed, pflicht=True)
NIE = {"flag": "hb_nie"}


def ZW(gruppe, wenn, text, gefuehl="neutral"):
    """Holm-Zeile einer Gruppe: es gilt die erste, deren Bedingung passt; ohne wenn = Rueckfall."""
    z = dict(Z("holm", text, gefuehl), gruppe=gruppe)
    if wenn:
        z["wenn"] = wenn
    return z


def ZG(wer, gruppe, wenn, text, gefuehl="neutral"):
    """Wie ZW, fuer jede Figur: Zeile gilt nur, wenn die Bedingung passt."""
    z = dict(Z(wer, text, gefuehl), gruppe=gruppe)
    if wenn:
        z["wenn"] = wenn
    return z


def ALLE(*flags):
    return {"alle": [{"flag": f} for f in flags]}


EVENTS = [
    E("hb_zurueck", "gag1", "wholesome", "Back Aboard", PFL("nachmittag"), "aft_deck", P1("holm"),
      "A water taxi from Ajaccio bumps against the hull. Marit Holm comes up the gangway slowly, one hand on the rail "
      "and the other pressed against her side. The crew comes out one by one, and nobody knows whether to salute her "
      "or hug her. Then someone hugs her, and she lets it happen. That's new. She counts heads, and you can see her "
      "lips move.",
      [ZW("dank", {"nicht": {"flag": "gefeuert"}},
          "All here. I was told to expect a wreck and a crew looking for other work. The ship floats and something "
          "smells like dinner. Takk. All of you.", "gratitude"),
       ZW("dank", None,
          "One short. Megan told me, and that talk can wait. The rest of you are here, the ship floats and something "
          "smells like dinner. Takk.", "gratitude")],
      [O("“Welcome back, Captain.”", [F("holm_zurueck"), V("holm", 2)],
         zeile=Z("holm", "Don't salute, Frankfurt. I have stitches and I might salute back.", "amusement")),
       O("Hands her a coffee, black and hot.", [F("holm_zurueck"), V("holm", 4)],
         zeile=Z("holm", "Who told you about the coffee? No, don't answer that. Takk.", "surprise"))],
      sets={"holm": "holm_shirt"}),
    E("hb_megan", "gag1", "ernst", "What Megan Told Me", PFL("abend", {"flag": "holm_zurueck"}), "aft_deck", P1("holm"),
      "The evening is quiet. The crew has gone below, and Holm is still on deck in her long coat, looking the ship over "
      "the way you check a car somebody else has been driving. A long case lies at her feet.",
      [Z("holm", "Megan called me every evening. She reads your reports out loud, like a charge sheet. So I know what "
                 "you have been doing, Frankfurt."),
       ZW("macchia", {"flag": "kloster_frederico_tot"},
          "You went up to the monastery, and the boy Frederico did not come back. Megan didn't read that part, she just said it.",
          "sadness"),
       ZW("macchia", {"flag": "kloster_frederico_lebt"},
          "You went up to the monastery and brought the boy Frederico down alive, and nobody on this coast expected that.",
          "approval"),
       ZW("macchia", None, "The monastery is still waiting for you, I hear."),
       ZW("berge", {"flag": "bg_adrien_bergerie"},
          "You fought a Legion sergeant over a deserter and won, and I would have left that out of the report too.",
          "approval"),
       ZW("berge", ALLE("bg_weg_b", "petru_versoehnt"),
          "You took a deserter out by sea, and it cost you Petru for a while. He doesn't come back for many people."),
       ZW("berge", {"flag": "bg_weg_b"},
          "You took a deserter out by sea, and it cost you Petru. I'd fix that before the twenty-first."),
       ZW("berge", {"flag": "bg_adrien_verhaftet"},
          "You handed a deserter to the Legion, which was the legal thing. Petru's daughter will never tell you so."),
       ZW("berge", None, "The mountains you have left alone so far, and they won't stay quiet for you."),
       ZW("grotte", {"flag": "gr_bastien_tot"},
          "In the grotto under Punta d'Orsu you had to choose who got out before the water came. I know something about cold water, so "
          "I won't tell you it gets smaller.", "sadness"),
       ZW("grotte", {"flag": "gr_gennaro_haende"},
          "You got them all out of that grotto, and Totò's cousin Gennaro paid for it with his fingers. I'd have done the same, and "
          "I wouldn't sleep either.", "sadness"),
       ZW("grotte", {"flag": "grotte_fertig"},
          "You went into that grotto for Totò's cousin Gennaro and came back with him, which is more than his friends did.", "approval"),
       ZW("grotte", {"flag": "red_trio_fertig"},
          "And you went looking for three people in red suits in the macchia. That one I had Megan read twice."),
       ZW("grotte", None, "Totò says there's a grotto you still owe him."),
       Z("holm", "On the twenty-first I will be on that quay. The doctors say four more weeks, but doctors are careful "
                 "people.")],
      [O("Looks at the case, then at her hand on her side. “You can't lift that.”", [F("holm_koffer")],
         zeile=Z("holm", "I lifted it. Not far.", "annoyance")),
       O("“Is that the gun from the old story? The bear, a kilometre, right in the eye?”", [F("holm_koffer")],
         zeile=Z("holm", "The eye is true. The kilometre is the harbourmaster's.")),
       O("Says nothing and waits.", [F("holm_koffer")],
         zeile=Z("holm", "Don't look at me like a doctor, Frankfurt. You're not qualified.", "annoyance"))],
      sets={"holm": "holm_shirt"}),
    E("hb_koffer", "gag1", "ernst", "The Long Case", PFL("nacht", {"flag": "holm_koffer"}), "foredeck", P1("holm"),
      "Past midnight you go up for air. Holm hasn't gone to bed. She is sitting on the foredeck with the case open "
      "across a hatch cover, and inside lies a double rifle with two worn barrels and a dark walnut stock. She got it "
      "up here by herself, and you can see what that cost her.",
      [Z("holm", "This has been in my family longer than this ship has floated, so I don't give it away. But it can't "
                 "stand on a quay by itself, and I can't hold it through a fight. Not by the twenty-first."),
       ZW("gegner", {"flag": "bg_adrien_bergerie"},
          "So I lend it to the best shot on this coast, and I don't know who that is yet. Adrien up at the bergerie, your "
          "dead deserter, thinks he knows. Elsa is sure she knows. And I have called a sergeant who doesn't care what anyone "
          "thinks."),
       ZW("gegner", None,
          "So I lend it to the best shot on this coast, and I don't know who that is yet. Rosi thinks she knows. Elsa is "
          "sure she knows. And I have called a sergeant who doesn't care what anyone thinks."),
       Z("holm", "Beat all three on my foredeck and you carry it on the twenty-first. Then you bring it back.")],
      [O("Runs a hand along the barrels. “When?”", [F("holm_wette_offen")],
         zeile=Z("holm", "Any evening, when the light goes. I'm not going anywhere, the doctors made sure of that."))],
      sets={"holm": "holm_shirt"}),
    E("hb_sieg", "gag1", "wholesome", "It Pulls Left", WANN((TAG, 21), bed=NIE), "foredeck", P1("holm"),
      "The last echo goes out over the water. Holm takes the rifle from you and raises it with her good arm. She shoots "
      "once, and the last bottle out on the water is gone. Then she sits down, a little too fast. She breaks the rifle "
      "open and holds it out to you. Her other hand has gone back to her side.",
      [Z("holm", "You beat all three. You have not beaten me. Ask me again when the fighting is over.", "amusement"),
       Z("holm", "It pulls left. Everyone in my family does.")],
      [O("Takes Gemelli, Holm's double rifle, with both hands.", [], zeile=Z("holm", "Bring it back, Frankfurt.", "caring"))],
      sets={"holm": "holm_shirt"}),
    E("hb_g_adrien", "gag1", "wholesome", "A Dead Man's Evening Off", WANN((TAG, 21), bed=NIE), "foredeck", P1("adrien", ("holm", "+", "keeps score")),
      "Adrien, the soldier Wolff wrote down as dead, has come down from the bergerie in a borrowed shirt, and nobody on board asks his name. Holm has put a "
      "box of cartridges on a hatch cover and a row of bottles out on the water.",
      [Z("adrien", "Laetitia says I can't shoot with this shoulder. I told her I only need one good one. You have two, "
                   "which seems unfair.", "amusement"),
       Z("holm", "Three rounds, and most hits after three wins. You get five seconds between rounds, and you load your "
                 "own rifle."),
       Z("holm", "No wind tonight, so you have no excuse. And leave my gulls alone, it costs you a hit.", "annoyance")],
      [O("Takes the rifle.", [F("hw_intro_adrien")], zeile=Z("adrien", "After you. I'm dead, I can wait.", "amusement"))],
      sets={"adrien": "adrien_standard", "holm": "holm_shirt"}),
    E("hb_g_rosi", "gag1", "wholesome", "Rosi vs. Officer", WANN((TAG, 21), bed=NIE), "foredeck", P1("rosi", ("holm", "+", "keeps score")),
      "Rosi comes up from the engine room with grease on her arms and her own ear defenders. She looks the rifle over "
      "the way she looks at every machine, and she likes it more than she likes you.",
      [Z("rosi", "Whoever made these barrels knew the job. Now watch me ruin your evening, Officer.", "amusement"),
       Z("holm", "Three rounds, and most hits after three wins. You get five seconds between rounds, and you load your "
                 "own rifle."),
       Z("holm", "No wind tonight, so you have no excuse. And leave my gulls alone, it costs you a hit.", "annoyance")],
      [O("“Loser cleans the bilge.”", [F("hw_intro_rosi")],
         zeile=Z("rosi", "Deal. And it goes on the whiteboard in my workshop, Officer.", "amusement"))],
      sets={"rosi": "Off Duty", "holm": "holm_shirt"}),
    E("hb_g_elsa", "gag1", "wholesome", "A Private Person", WANN((TAG, 21), bed=NIE), "foredeck", P1("elsa", ("holm", "+", "keeps score")),
      "Elsa Ferrandi comes aboard out of uniform. She still stands like she is wearing it. She checks the rifle twice, "
      "then she checks your hands.",
      [Z("elsa", "I'm here as a private person, First Officer. A private person with eleven years of range scores. Holm "
                 "says all of this is legal, and I'd like to keep believing her.", "amusement"),
       Z("holm", "The wind is up tonight, so aim against it. And one of my gulls stole a flash grenade from our stores and "
                 "keeps coming back. Hit the grenade, not the bird, and the other shooter sees nothing for five seconds.",
         "annoyance")],
      [O("“Any advice?”", [F("hw_intro_elsa")],
         zeile=Z("elsa", "Yes. Keep the barrels away from the gendarmerie.", "amusement"))],
      sets={"holm": "holm_shirt"}),
    E("hb_g_wolff", "gag1", "wholesome", "The Sergeant Comes to Dinner", WANN((TAG, 21), bed=NIE), "foredeck", P1("wolff", ("holm", "+", "called him")),
      "A grey Legion jeep stops on the quay at dusk. Sergent Wolff, the Legion man from the Genoese tower, comes up the gangway with a notebook and a sharp "
      "pencil, and he salutes Holm properly. She doesn't salute back, she shakes his hand. Neither of them says anything "
      "about her side.",
      [ZG("wolff", "gruss", {"flag": "bg_adrien_bergerie"},
          "Who is that man at the rail? He looks like a caporal of mine. A good man and a terrible shot. He died on a "
          "mountain. It was in my report.", "amusement"),
       ZG("wolff", "gruss", {"flag": "bg_legion_npc_zu"},
          "You lied to me and took my deserter out by sea, Officer. Tonight I'm off duty, so I will only beat you.",
          "disapproval"),
       ZG("wolff", "gruss", {"flag": "bg_adrien_verhaftet"},
          "You gave me my man and you did it by the book, Officer. So I will beat you politely.", "approval"),
       ZG("wolff", "gruss", None, "Captain Holm tells me you can shoot, Officer. I'll need to see that for myself."),
       ZG("adrien", "necken1", {"flag": "bg_adrien_bergerie"},
          "I read about him. Sad story. They say his sergeant wrote it very well.", "amusement"),
       ZG("wolff", "necken2", {"flag": "bg_adrien_bergerie"},
          "It was the best thing that man ever wrote, and he didn't do it to be thanked.", "caring"),
       ZG("adrien", "necken3", {"flag": "bg_adrien_bergerie"},
          "No. But if I ever meet him, I'll buy him a drink. And then I'll let him win.", "gratitude"),
       ZG("wolff", "necken4", {"flag": "bg_adrien_bergerie"},
          "You could not stop him. Now go and stand somewhere else, whoever you are.", "amusement")],
      [O("“Write this one down, then.”", [F("hw_intro_wolff")],
         zeile=Z("wolff", "I always do. Begin.", "neutral"))],
      sets={"wolff": "wolff_standard", "adrien": "adrien_standard", "holm": "holm_shirt"}),
    E("hb_g_holm", "gag1", "wholesome", "Stitches or Not", WANN((TAG, 21), bed=NIE), "foredeck", P1("holm"),
      "Holm is on the foredeck when the light goes, with a crate of bottles and a small tin box. She still moves like "
      "someone carrying a very full glass. She has the cartridges for Gemelli, her double rifle, lined up on the hatch cover, and she has counted "
      "them.",
      [Z("holm", "You beat three people who were not me. The stitches still pull, so this is your chance, Frankfurt.",
         "amusement"),
       Z("holm", "One round, one gift. That's how my father taught me. Every round you win, the box gets lighter.")],
      [O("Looks into the tin box.", [F("hw_intro_holm")],
         zeile=Z("holm", "Steel, a stone and a bar of copper. Rosi will know what to do. Now shoot.", "neutral"))],
      sets={"holm": "holm_shirt"}),
    E("hb_w_adrien", "gag1", "wholesome", "Adrien", WANN((TAG, 21), bed=NIE), "foredeck", P1("adrien"), "",
      [Z("adrien", "Two good shoulders. I told you it was unfair.", "amusement"),
       Z("adrien", "A dead man just beat you. Please don't put that in a report.", "amusement")],
      [O("Nods.", [])], sets={"adrien": "adrien_standard"}),
    E("hb_w_rosi", "gag1", "wholesome", "Rosi", WANN((TAG, 21), bed=NIE), "foredeck", P1("rosi"), "",
      [Z("rosi", "Fine, one line on the whiteboard for you, but only one.", "annoyance"),
       Z("rosi", "That's another line for me, Officer. I'm running out of board.", "amusement")],
      [O("Nods.", [])], sets={"rosi": "Off Duty"}),
    E("hb_w_elsa", "gag1", "wholesome", "Elsa", WANN((TAG, 21), bed=NIE), "foredeck", P1("elsa"), "",
      [Z("elsa", "Not bad. I'll pretend I didn't see how you hold it.", "approval"),
       Z("elsa", "Again, First Officer. Slower hands. That's not advice, it's a complaint.", "amusement")],
      [O("Nods.", [])]),
    E("hb_w_wolff", "gag1", "wholesome", "Wolff", WANN((TAG, 21), bed=NIE), "foredeck", P1("wolff"), "",
      [Z("wolff", "Noted. You shot better than me tonight. I don't write that often.", "approval"),
       Z("wolff", "I wrote down all your misses. Would you like the list?", "neutral")],
      [O("Nods.", [])], sets={"wolff": "wolff_standard"}),
    E("hb_w_holm", "gag1", "wholesome", "Holm", WANN((TAG, 21), bed=NIE), "foredeck", P1("holm"), "",
      [Z("holm", "That's the first time. Stitches or not, I will remember it.", "approval"),
       Z("holm", "Again, Frankfurt. The box isn't empty.", "amusement"),
       Z("holm", "Steel. Give it to Rosi, then she'll be nice to you for an hour.", "amusement"),
       Z("holm", "Aquamarine, for the sabre. Yes, I know about the sabre.", "amusement"),
       Z("holm", "Copper. My father kept that for Gemelli and never used it. Now it's your turn to carry the guilt.", "caring")],
      [O("Nods.", [])], sets={"holm": "holm_shirt"}),
    E("hb_nochmal", "gag1", "ernst", "Again", WANN((TAG, 21), bed=NIE), "foredeck", P1("holm"),
      "Holm reloads without looking at you.",
      [Z("holm", "Again, Frankfurt.")],
      [O("Reloads.", [])],
      sets={"holm": "holm_shirt"}),
]

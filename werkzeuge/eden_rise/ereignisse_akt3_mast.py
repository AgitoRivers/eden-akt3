# -*- coding: utf-8 -*-
"""Akt 3: Quest "The Red Light" (Duc 04.11.2026). Drehbuch: docs/wiki/welt/drehbuch_akt3.md, Abschnitt 5.29.

Alon hat nach der Belagerung auf dem Kamm ueber San Martinu einen Mast gebaut und aktiviert: das Auge ueber der Bucht, fuer
Drohnen und den Funk der Maenner in Weiss. Er hoert das Dorf nicht ab (Pascal bleibt das Raedchen). Nachts blinkt sein rotes
Licht (Ende 2b). Kanon charly.md: Charly bricht ihn auf; ist sie nicht geblieben, schafft es Rosi.
Karte "The Red Light" (Ort a3_mast, Tag 24 bis 28, Rang 2 nach der Baustelle). Begleiter nach Kanon: Charly (rt_charly_bleibt,
nicht rt_charly_weg), sonst Rosi (nicht gefeuert). Gegner: Agenten und Drohne auf der Strasse, Kobra-Roboter in der Macchia,
Drohnen beim Alarm, am Ende der Waechter (schwerer Kampfroboter mit Skorpion). Alle Maschinen geben Stahl (Wiederaufbau).
Herz: Charly loest die Sicherheitsfragen ihrer Mutter mit den Hinweisen vom Rastplatz; die Mutter ruft an und sieht sie durch
die Kamera. Rosi erkennt die Handschrift ihres Vaters im Steuerkasten (gebaut in Catania, in der Strasse von Lot 14).
Wahl: abschalten (a3_mast_aus: Drohnen fallen wie Sternschnuppen, die Bucht atmet, Ba Tu sagt auch ohne Haus aus) oder
weiterlaufen lassen und Elsa alles schicken (a3_mast_an: Kommissions-Karte "The Mast Recording", Ba Tu nur mit Haus,
das Licht blinkt weiter)."""
from ereignisse_basis import *  # noqa: F401,F403
from ereignisse_ligeia import G  # noqa: E402
from ereignisse_akt3_woche4 import FR, FL, NICHT, DA, AKT3, JE, tags_fuer  # noqa: E402

WEITER = lambda ziel: {"weiter": ziel}
KAMPF = lambda bid: {"kampf": bid}
CHARLY = {"alle": [FL("rt_charly_bleibt"), NICHT(FL("rt_charly_weg"))]}
ROSI = {"alle": [NICHT(CHARLY), DA("rosi")]}
P = lambda pid: {"handelnd": pid, "betroffen": []}
WEG = lambda c, r: WEITER([{"wenn": CHARLY, "id": c}, {"id": r}])     # Charlys oder Rosis Fassung


def _frage(n, frage, lage, zeile, richtig, falsch, weiter_id):
    """Sicherheitsfrage der Mutter: die richtige Antwort oeffnet, eine falsche loest den Alarm aus (Kampf, dann nochmal)."""
    opt = [O(richtig[0], [F("a3_mast_frage_%d" % n), WEITER(weiter_id)], zeile=richtig[1])]
    for t, z in falsch:
        opt.append(O(t, [KAMPF("a3_mast_alarm"), WEITER("a3_mast_c_frage_%d" % n)], zeile=z))
    return FR("a3_mast_c_frage_%d" % n, "antenna_ridge", "The Red Light", lage, [zeile], opt, personen=P("charly"), ton="ernst")


EVENTS = [
    # ---------------------------------------------------------------- Aufbruch und Weg (gemeinsam)
    FR("a3_mast_start", "macchia_path", "The Red Light",
       "Every night since the siege, a red light blinks on the ridge above San Martinu. Elsa still sees drones over the village at night. "
       "The shepherds in the hills say the light keeps their sheep awake. Up there, Alon has built something new.",
       [JE(G("charly", "[sigh] It's a mast. My mother's company makes them. I know the model. Seven out of ten for hiding it.", "neutral"), "wer", CHARLY),
        JE(G("rosi", "[clear throat] It's a relay mast, Officer. Brand new. The drones talk to it, the men in white talk to it. I want to see its insides.", "curiosity"), "wer", None),
        G("elsa", "[clear throat] I'll wait at the bottom of the path with the car. If you find anything, it comes to me. Not to the town hall, not to anyone. To me.", "neutral")],
       [O("Takes the goat path, the slow and quiet way.", [WEITER([{"wenn": FL("bl_verband_wolff"), "id": "a3_mast_wolff"}, {"id": "a3_mast_macchia"}])]),
        O("Takes the old road, the fast way.", [KAMPF("a3_mast_strasse"), WEITER("a3_mast_macchia")])],
       personen=P("elsa"), sets={"elsa": "Standard"}, ton="ernst"),
    FR("a3_mast_wolff", "genoese_tower_camp", "The Red Light",
       "At the old Genoese tower someone is sitting in the shadow: Sergent Wolff, with your bandage on his arm, the good one you gave him in the siege.",
       [G("wolff", "[clear throat] The goat path goes round the drones. I know it from before. The Legion pays its debts. Follow me, and don't talk.", "neutral")],
       [O("Follows him without a word.", [WEITER("a3_mast_macchia")])],
       personen=P("wolff"), ton="ernst"),
    FR("a3_mast_macchia", "macchia_path", "The Red Light",
       "The bushes are high here. Something moves in it, low and fast, with a sound like a zip. Steel snakes from the beach.",
       [JE(G("charly", "[gasp] Cobras. Mother's catalogue, page twelve. Don't let them get behind you.", "fear"), "wer", CHARLY),
        JE(G("rosi", "[gasp] Cobra robots. Beautiful welding. I hate that it's beautiful.", "fear"), "wer", None)],
       [O("Stays where he is and gets ready to fight.", [KAMPF("a3_mast_kobra"), WEG("a3_mast_c_rast", "a3_mast_r_rast")])],
       ton="ernst"),

    # ---------------------------------------------------------------- Charlys Fassung
    FR("a3_mast_c_rast", "antenna_ridge", "The Red Light",
       "A small fire below the ridge. The red light blinks above you, slowly, like a heartbeat. Charly sits close to the fire and looks at it, not at you.",
       [G("charly", "[sigh] Every birthday, my mother watched me on a screen. She was never in the room. Twelve birthdays, twelve screens.", "sadness"),
        G("charly", "[sigh] I wanted a dog. For my twelfth, she gave me a taser instead. Model R-7. From her own catalogue. I named it. I'm not telling you what.", "sadness"),
        G("charly", "[clear throat] There was one place her cameras couldn't see: under her desk in the office in Marseille. I hid there. Four out of ten as a hiding place. Ten out of ten for quiet.", "neutral")],
       [O("Puts another stick on the fire and listens.", [WEITER("a3_mast_c_frage_1")]),
        O("“You don't have to do this, Charly.”", [WEITER("a3_mast_c_frage_1")],
          zeile=G("charly", "[sigh] Yes I do. Somebody has to switch her off. I'd rather it's me.", "neutral"))],
       personen=P("charly"), ton="ernst"),
    _frage(1, "First question.", "The control box on the mast has a small screen. Three questions. The cursor blinks. Charly reads it out loud, flat, like a weather report.",
           G("charly", "[sigh] Security question one. 'First pet.' ...She set these questions herself. Of course she did.", "neutral"),
           ("Types: R-7.", G("charly", "[sniff] ...Accepted. She remembers the taser. She remembers.", "sadness")),
           [("Types: None.", G("charly", "[gasp] Wrong. Alarm. They're coming.", "fear")),
            ("Types: Capybara.", G("charly", "[gasp] That's Bibi's answer, not mine. Alarm!", "fear"))],
           "a3_mast_c_frage_2"),
    _frage(2, "Second question.", "The screen changes. One question gone, two left.",
           G("charly", "[clear throat] 'Favourite place.'", "neutral"),
           ("Types: Under the desk.", G("charly", "[sigh] ...Accepted. She knew. All those years, she knew where I was hiding.", "sadness")),
           [("Types: Marseille.", G("charly", "[gasp] Too big. She wants the exact place. Alarm!", "fear")),
            ("Types: The red team.", G("charly", "[sigh] That's mine, not hers. She doesn't know it exists. Alarm.", "sadness"))],
           "a3_mast_c_frage_3"),
    FR("a3_mast_c_frage_3", "antenna_ridge", "The Red Light",
       "The last question. Charly reads it, and for a long time she doesn't move.",
       [G("charly", "[sigh] 'What makes Charlotte happy?' ...She wrote the answer herself. I know what she wrote: Being the best.", "sadness"),
        G("charly", "[clear throat] Duc. If I type her answer, it opens. If I type mine, it won't. Which one do I type?", "nervousness")],
       [O("“Type hers. Then switch her off.”", [F("a3_mast_frage_3"), F("a3_mast_mutter_antwort"), WEITER("a3_mast_c_anruf")],
          zeile=G("charly", "[sigh] ...Accepted. Being the best. It's open. I feel sick.", "sadness")),
        O("“Type yours. We'll get in another way.”", [F("a3_mast_frage_3"), F("a3_mast_eigene_antwort"), KAMPF("a3_mast_alarm"), WEITER("a3_mast_c_anruf")],
          zeile=G("charly", "[sniff] Danzel. Ten out of ten. ...Wrong, it says. Good. Alarm. Let them come.", "pride"))],
       personen=P("charly"), ton="ernst"),
    FR("a3_mast_c_anruf", "antenna_ridge", "The Red Light",
       "The control box is open. Then Charly's phone rings. The camera on the mast turns, slowly, until its lens looks at her. Her mother's name is on the screen.",
       [G("charly", "[clear throat] Maman.", "neutral"),
        G("charly", "[sigh] She says: Charlotte. You're cold. Put on your jacket. ...She can see me. Through her own camera.", "sadness"),
        G("charly", "[sniff] Six... I can't rate this. I can't.", "grief")],
       [O("Takes the phone out of her hand.", [V("charly", 4), WEITER("a3_mast_wende")],
          zeile=G("charly", "[sigh] ...Thank you. Don't hang up. Just hold it.", "sadness")),
        O("Holds the phone out to her. “You decide what you say.”", [V("charly", 6), WEITER("a3_mast_wende")],
          zeile=G("charly", "[clear throat] Maman. I'm not cold. I'm working. Goodbye.", "pride")),
        O("Stands in front of the camera, so it sees him and not her.", [V("charly", 6), WEITER("a3_mast_wende")],
          zeile=G("charly", "[sniff] Nobody ever stood there before. Seven out of ten for height. Ten for the rest.", "gratitude"))],
       personen=P("charly"), ton="ernst"),

    # ---------------------------------------------------------------- Rosis Fassung
    FR("a3_mast_r_rast", "antenna_ridge", "The Red Light",
       "A small fire below the ridge. Rosi has taken her boots off and is cleaning cobra oil from her spanner.",
       [G("rosi", "[sigh] Papa had three rules. Every thread on his machines turned the wrong way, left, so thieves gave up. Never cut the red wire first.", "caring"),
        G("rosi", "[clear throat] And: listen to the machine. Where it hums high, that's where it hurts. Old Lady, his press, hummed high on the left side. That's where the crack was.", "sadness")],
       [O("Listens and says nothing.", [WEITER("a3_mast_r_kasten")]),
        O("“He sounds like a good teacher.”", [WEITER("a3_mast_r_kasten")],
          zeile=G("rosi", "[sniff] He was. He is. He sells tomatoes now.", "sadness"))],
       personen=P("rosi"), sets={"rosi": "Engine Room"}, ton="ernst"),
    FR("a3_mast_r_kasten", "antenna_ridge", "The Red Light",
       "Rosi opens the control box on the mast. Inside there is a metal plate: assembled in Catania. Under it, a street name. Rosi goes very still.",
       [G("rosi", "[gasp] That's Papa's street. In Catania. They built this where his workshop was. ...And look. Every thread turns left.", "grief"),
        G("rosi", "[clear throat] Officer. Three screws, two wires, one hum. Tell me where to start.", "nervousness")],
       [O("“Left. Everything turns left. Your father's rule.”", [F("a3_mast_frage_1"), WEITER("a3_mast_r_draht")],
          zeile=G("rosi", "[sniff] Left. They copied him, Officer. They took his street and his tricks.", "anger")),
        O("“To the right, like every other screw.”", [KAMPF("a3_mast_alarm"), WEITER("a3_mast_r_kasten")],
          zeile=G("rosi", "[gasp] No! Wrong way, it's locking! Drones!", "fear"))],
       personen=P("rosi"), sets={"rosi": "Engine Room"}, ton="ernst"),
    FR("a3_mast_r_draht", "antenna_ridge", "The Red Light",
       "Two wires: red and black. The box hums.",
       [G("rosi", "[clear throat] Which one first?", "nervousness")],
       [O("“Not the red one first. Black.”", [F("a3_mast_frage_2"), WEITER("a3_mast_r_old_lady")],
          zeile=G("rosi", "[sigh] Black. ...Good. Papa would say: good.", "relief")),
        O("“Red. It's always the red one.”", [KAMPF("a3_mast_alarm"), WEITER("a3_mast_r_draht")],
          zeile=G("rosi", "[gasp] Not in this family! Alarm!", "fear"))],
       personen=P("rosi"), sets={"rosi": "Engine Room"}, ton="ernst"),
    FR("a3_mast_r_old_lady", "antenna_ridge", "The Red Light",
       "The mast hums. Rosi puts her ear against the box, the way she does with the generator on the yacht. Then she puts her hand flat on the left side.",
       [G("rosi", "[sniff] It hums high on the left. Like Old Lady. ...I love machines, Officer. I've never killed one on purpose.", "grief")],
       [O("Puts his hand next to hers on the box.", [F("a3_mast_frage_3"), V("rosi", 6), WEITER("a3_mast_wende")],
          zeile=G("rosi", "[sigh] Sorry, Old Lady. It's not your fault who built you.", "grief")),
        O("“It's not her, Rosi. It just looks like her.”", [F("a3_mast_frage_3"), V("rosi", 4), WEITER("a3_mast_wende")],
          zeile=G("rosi", "[sniff] I know. That's the worst part.", "sadness"))],
       personen=P("rosi"), sets={"rosi": "Engine Room"}, ton="ernst"),

    # ---------------------------------------------------------------- Wende, Waechter, Wahl (gemeinsam)
    FR("a3_mast_wende", "antenna_ridge", "The Red Light",
       "Inside the box is a memory card. On the small screen: the night of the siege, filmed from up here. The men in white walk along the north road "
       "to the barricade, an hour before the attack. And there, in front of the church, a small figure that doesn't move: you.",
       [JE(G("charly", "[sigh] It saw everything. It just never told anyone.", "sadness"), "wer", CHARLY),
        JE(G("rosi", "[sigh] It saw everything, Officer. It just never told anyone.", "sadness"), "wer", None)],
       [O("Takes the memory card.", [F("a3_mast_aufnahme"), WEITER("a3_mast_waechter")])],
       ton="ernst"),
    FR("a3_mast_waechter", "antenna_ridge", "The Red Light",
       "Behind the mast, something big unfolds from the rocks: a heavy robot with an armoured head, and a scorpion at its feet. The guardian.",
       [JE(G("charly", "[gasp] Page one of the catalogue. The expensive one.", "fear"), "wer", CHARLY),
        JE(G("rosi", "[gasp] That's not a robot, that's a fridge with opinions. Get ready!", "fear"), "wer", None)],
       [O("Steps between the guardian and the mast.", [KAMPF("a3_mast_waechter"), WEITER("a3_mast_wahl")])],
       ton="ernst"),
    FR("a3_mast_wahl", "antenna_ridge", "The Red Light",
       "The guardian lies still between the rocks. Good steel, a lot of it. The red light still blinks above you. Down in the bay, the village sleeps.",
       [JE(G("charly", "[clear throat] Duc. I can switch it off, and it's gone. Or I leave it on, and Elsa hears everything it hears. "
                       "Then my mother watches forever. I can't choose this one. You choose. What do we do?", "nervousness"), "wer", CHARLY),
        JE(G("rosi", "[clear throat] Officer. Off, and it's dead. Or on, and Elsa gets every word it hears, until the commission. What do we do?", "nervousness"), "wer", None)],
       [O("“Switch it off.”", [F("a3_mast_aus"), F("a3_mast_fertig"), WEITER("a3_mast_aus")]),
        O("“Leave it on. Send everything to Elsa.”", [F("a3_mast_an"), F("a3_mast_fertig"), WEITER("a3_mast_an")])],
       ton="ernst"),
    FR("a3_mast_aus", "antenna_ridge", "The Red Light",
       "The red light goes out. A second later, all over the bay, small lights fall from the sky into the sea, one after the other, like shooting stars. "
       "The drones. Down in the village, a window opens, then another.",
       [JE(G("charly", "[sigh] Nobody's watching. ...Is this what everybody else has?", "sadness"), "wer", CHARLY),
        JE(G("rosi", "[sniff] Look at them fall. ...That's the most beautiful thing I ever broke.", "sadness"), "wer", None)],
       [O("Sits down next to her in the dark.", [])],
       ton="wholesome"),
    FR("a3_mast_an", "antenna_ridge", "The Red Light",
       "The red light keeps blinking. The camera turns away from you and looks down at the village, at the road, at the villa on the other side of the bay.",
       [JE(G("charly", "[clear throat] Then watch, Maman. Watch what he did.", "anger"), "wer", CHARLY),
        JE(G("rosi", "[clear throat] Elsa gets everything. Every drone, every word. Let it watch him for a change.", "anger"), "wer", None),
        G("elsa", "[clear throat] I have it. All of it. ...Come down carefully. And thank you.", "gratitude")],
       [O("Walks down the path in the blinking red light.", [])],
       personen=P("elsa"), sets={"elsa": "Standard"}, ton="ernst"),
]

ORTE = {
    "a3_mast": {
        "label": "The Red Light", "bild": "antenna_ridge", "phasen": ["tag", "nachmittag"],
        "text": "Every night a red light blinks on the ridge above San Martinu. Alon built something up there after the siege. Takes the whole phase.",
        "wenn": {"alle": [AKT3, {"eine": [CHARLY, ROSI]}, NICHT(FL("a3_mast_fertig")), {"nicht": {"tag_ab": 29}}]},
        "start": [{"id": "a3_mast_start"}]},
}


def tags_schreiben():
    return tags_fuer(EVENTS, "akt3_mast")

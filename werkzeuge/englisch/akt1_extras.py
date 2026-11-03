# -*- coding: utf-8 -*-
"""English rewrite · package 2b: side fields of the event builders (afterglow texts, gossip, promises, ship's rules,
gag labels, items created by events), 25.10.2026. Maps old German text -> new English text directly.

    python werkzeuge\\englisch\\akt1_extras.py      -> docs\\abnahme\\englisch_akt1_extras.json (spec for uebernehmen.py)
"""
import json, os

ALT_NEU = {
    # ---------------------------------------------------------------- ship's rules
    "Lola jeden Abend etwas genervt; Kontrollrisiko bei Elsa entfällt fürs Gras":
        "Lola a little annoyed every evening; no inspection risk with Elsa over the weed",
    "Lolas Abend-Event bleibt möglich; Holm/Chiara-Events mit Gras an Deck entfallen":
        "Lola's evening event stays possible; Holm/Chiara events with weed on deck drop out",
    "Essen wird geteilt, nicht gehortet": "Food is shared, not hoarded",
    "Siri +2 Vertrauen am Abend, Yasin-Content-Missionen nur tagsüber":
        "Siri +2 trust in the evening; Yasin's content missions only during the day",
    "Kombüsen-Ordnung": "Galley order",
    "Chiara +2, Lolas Gags in der Kombüse seltener": "Chiara +2; Lola's galley gags happen less often",
    "Gästebereich bleibt Gästebereich": "The guest area stays the guest area",
    "Rückhalt +1 jeden Abend, Alvas Bar-Lieferungen an Bord entfallen":
        "Backing +1 every evening; Alva's bar deliveries to the boat drop out",
    "Energie +1 am Morgen, nächtliche Handy-Events seltener": "Energy +1 in the morning; fewer phone events at night",
    # ---------------------------------------------------------------- running gags
    "Kevin, die Möwe": "Kevin the seagull",
    "Megan lacht (und hasst es)": "Megan laughs (and hates it)",
    "Janas Training mit Maxwell": "Jana's training with Maxwell",
    # ---------------------------------------------------------------- items created by events
    "Lolas „Spezial-Pesto“": "Lola's “Special Pesto”",
    "Ein Glas grünes Pesto. Sehr grün. Hebt die Stimmung, sagt Lola.":
        "A jar of green pesto. Very green. It lifts the mood, Lola says.",
    "Muschelkrone der Festa": "Festa Shell Crown",
    "Glitzer, Muscheln und Würde. Im Epilog sichtbar.": "Glitter, shells and dignity. Visible in the epilogue.",
    "Selbstgemachte Muschelkette mit Perlen": "Homemade Shell Necklace with Beads",
    "Von den Dorfkindern als Dank. Siri liebt sie.": "A thank-you from the village kids. Siri loves it.",
    "Ein Eimer Fisch. Lola macht daraus ein Fest.": "A bucket of fish. Lola turns it into a feast.",
    "„Danke für den ersten Geburtstag ohne Kamera.“ Im Epilog sichtbar.":
        "“Thank you for my first birthday without a camera.” Visible in the epilogue.",
    "Einmal am Tag Vorteil auf Empathy.": "Once a day: advantage on Empathy.",
    "Bauchnabelpiercing mit Muschel": "Belly Button Piercing with a Shell",
    "Alva legt es dir für Lola auf die Rechnung. Lola liebt es.": "Alva puts it on your tab for Lola. Lola loves it.",
    "Ein Foto, das du nicht löschen solltest": "A Photo You Shouldn't Delete",
    "Rosi weiß, dass du es hast. Im Epilog sichtbar.": "Rosi knows you have it. Visible in the epilogue.",
    "Weiß, mit goldenem Anker. Totò liebt sie, Siri hasst sie.": "White, with a golden anchor. Totò loves it, Siri hates it.",
    "Lolas Gewürzmischung": "Lola's Spice Mix",
    "Ein Glas „Ocean Glitter“. Rosi liebt es.": "A jar of “Ocean Glitter”. Rosi loves it.",
    "Screenshot: Megan mit Goldmaske": "Screenshot: Megan in a Gold Mask",
    "Einmal am Tag Vorteil auf Charm bei Megan. Wehe, sie findet es.":
        "Once a day: advantage on Charm with Megan. Heaven help you if she finds it.",
    "Abzeichen der Gendarmerie maritime": "Gendarmerie Maritime Badge",
    "Elsa hat es dir zugeworfen. Einmal am Tag Vorteil auf Courage.":
        "Elsa tossed it to you. Once a day: advantage on Courage.",
    "Ein rostiger Frachter vor Bergen, eine junge Frau mit Mütze.": "A rusty freighter off Bergen, a young woman in a cap.",
    "Trophäe. Megan will ihn zurück. Nie.": "A trophy. Megan wants it back. Never.",
    "Ducs Gedicht über das Meer": "Duc's Poem About the Sea",
    "Reimt sea auf me. Chiara liebt es, heimlich.": "Rhymes sea with me. Chiara loves it, secretly.",
    "Einmal am Tag Vorteil auf Perception.": "Once a day: advantage on Perception.",
    "Goldfisch in der Wassertüte": "Goldfish in a Water Bag",
    "Casanova schenkt ihn „der Heldin der Bucht“. Lea liebt ihn, Chiara hasst ihn.":
        "Casanova gives it to “the heroine of the bay”. Lea loves it, Chiara hates it.",
    "Sie hat es dir beim Tanzen ins Haar gesteckt. Im Epilog sichtbar.":
        "She tucked it into your hair while you were dancing. Visible in the epilogue.",
    "Eine rote Rose aus Alvas Haar. Lola und Siri lieben sie.": "A red rose from Alva's hair. Lola and Siri love it.",
    "+1 Courage, solange getragen. „Science, then hammer.“": "+1 Courage while carried. “Science, then hammer.”",
    "+1 Perception, solange getragen. Riecht nach Salz und Sonnencreme.":
        "+1 Perception while carried. Smells of salt and sun cream.",
    "+1 Cunning, solange getragen. Zu klein, aber sie wollte, dass du sie nimmst.":
        "+1 Cunning while carried. Too small, but she wanted you to have them.",
    "Einmal am Tag Vorteil auf Charm.": "Once a day: advantage on Charm.",
    "Messing-Anker als Schlüsselanhänger": "Brass Anchor Keyring",
    "Rostig, aus der Bucht geangelt. Holm würde ihn lieben.": "Rusty, fished out of the bay. Holm would love it.",
    "Grünes Seeglas": "Green Sea Glass",
    "Schlüssel zu Alvas Hinterzimmer": "Key to Alva's Back Room",
    "An einer roten Kordel. Öffnet das Hinterzimmer der Bar, auch für ruhige Gespräche ohne Zeugen.":
        "On a red cord. Opens the bar's back room, also for quiet talks without witnesses.",
    "Die Rose der Bürgermeisterin": "The Mayor's Rose",
    "Aus Madame Casanovas Haar, nach dem Flamenco. Einmal benutzt: Begehren +6 bei allen Frauen.":
        "From Madame Casanova's hair, after the flamenco. Used once: desire +6 with all the women.",
    # ---------------------------------------------------------------- promises
    "Duc kontrolliert die Kombüse selbst": "Duc checks the galley himself",
    "Duc baut Lea ein Regal an Deck": "Duc builds Lea a rack on deck",
    "Duc übernimmt Rosis Spätschicht": "Duc takes Rosi's late shift",
    "Duc besorgt Chiara eine neue Mütze": "Duc gets Chiara a new cap",
    "Duc kommt morgen zu Alva": "Duc visits Alva tomorrow",
    "Duc erzählt der Crew von Köln": "Duc tells the crew about Cologne",
    # ---------------------------------------------------------------- gossip
    "Duc hat auf Alvas Tresen getanzt": "Duc danced on Alva's bar",
    "Duc und Rosi im Generatorraum": "Duc and Rosi in the generator room",
    "Duc schaut Lola beim Yoga zu": "Duc watches Lola doing yoga",
    "Duc konnte sich beim Dinner nicht entscheiden": "Duc couldn't make up his mind at dinner",
    "Siri und Lea cremen Duc gleichzeitig ein": "Siri and Lea put sun cream on Duc at the same time",
    "Duc tanzt auf der Festa mit zwei Frauen": "Duc dances with two women at the festa",
    "Duc hat Lola in ihrer eigenen Kombüse geschlagen": "Duc beat Lola in her own galley",
    "Ducs Fusionsküche hat das Dorf verwirrt": "Duc's fusion cooking confused the village",
    "Der Quizmaster wusste seine eigene Frage nicht": "The quizmaster didn't know the answer to his own question",
    # ---------------------------------------------------------------- afterglow (the next morning)
    "Du hast kaum geschlafen. Ihre Stimme um 02:13 ist noch immer da, ganz nah an deinem Ohr.":
        "You hardly slept. Her voice at 02:13 is still there, very close to your ear.",
    "Schwarze Rüschen. Ihre Stimme, als sie sagte: langsamer. Du denkst an nichts anderes beim Kaffee.":
        "Black ruffles. Her voice when she said: slower. Over coffee you can't think of anything else.",
    "Das Deck im Dunkeln, ihr Flüstern. Beim Frühstück trägt sie die Bluse bis oben zugeknöpft und sieht dich nicht an.":
        "The deck in the dark, her whisper. At breakfast she has her blouse buttoned to the top and doesn't look at you.",
    "Ein beschlagener Spiegel, ein Handtuch, Rosis Grinsen. Beim Frühstück fragt sie zu laut, ob jemand ein Ersatzteil gesehen hat.":
        "A steamed-up mirror, a towel, Rosi's grin. At breakfast she asks, too loudly, whether anyone has seen a spare part.",
    "Blaues Licht zwischen euren Fingern. Am Morgen hat Lea Salz im Haar und lächelt dich an, als hättet ihr ein Geheimnis.":
        "Blue light between your fingers. In the morning Lea has salt in her hair and smiles at you as if you shared a secret.",
    "Ihr Gesicht ohne Filter, ihr Lachen ohne Publikum. Beim Frühstück trägt sie wieder Make-up, aber sie zwinkert dir zu.":
        "Her face without a filter, her laugh without an audience. At breakfast she's wearing make-up again, but she winks at you.",
    "Öl an deinen Fingern, ihr Lachen im Generatorraum. Beim Frühstück trägt Rosi einen neuen Overall und grinst in ihren Kaffee.":
        "Oil on your fingers, her laugh in the generator room. At breakfast Rosi is wearing a new coverall and grinning into her coffee.",
    "Wasser auf ihrer Haut, ihr Lachen an der Boje. Beim Frühstück fragt Chiara viel zu sachlich, ob du gut geschlafen hast.":
        "Water on her skin, her laugh at the buoy. At breakfast Chiara asks, far too matter-of-factly, whether you slept well.",
    "Aloe vera und warme Haut unter deinen Händen. Beim Frühstück sagt Lea, ihr Rücken fühle sich viel besser an, und wird rot.":
        "Aloe vera and warm skin under your hands. At breakfast Lea says her back feels much better, and goes red.",
    "Dein Pullover an ihr. Du findest den ganzen Tag graue Wollfussel an deinem Ärmel und lächelst darüber.":
        "Your jumper on her. All day you keep finding grey wool fluff on your sleeve, and you smile about it.",
    "Die Liebenden auf dem Tisch, Sophias rote Wangen. Beim Frühstück sagt sie zu dir: „Es ist Unsinn.“ Und lächelt.":
        "The Lovers on the table, Sophia's red cheeks. At breakfast she says to you, “It's nonsense.” And smiles.",
    "Eine leere Flasche, die auf dich zeigt. Am Morgen weiß jede am Tisch, was passiert ist. Keine sagt etwas.":
        "An empty bottle pointing at you. In the morning everyone at the table knows what happened. Nobody says a word.",
    "Rauch, Salz, Lolas Lachen in der Dunkelheit. Beim Frühstück stellt sie dir als Einzigem einen Pfannkuchen in Herzform hin.":
        "Smoke, salt, Lola's laugh in the dark. At breakfast you're the only one who gets a heart-shaped pancake.",
    "Schwarze Rüschen auf einem Barhocker, eine Rose auf dem Boden. Du riechst sie noch, als du am Morgen zurück an Bord ruderst.":
        "Black ruffles on a bar stool, a rose on the floor. You can still smell her as you row back to the boat in the morning.",
    "Sophia hat dein Gedicht auf eine Serviette abgeschrieben. Am Morgen liegt die Serviette gefaltet in deiner Jackentasche.":
        "Sophia copied your poem onto a napkin. In the morning the napkin is folded in your jacket pocket.",
    "Die Lichterkette flackert, die Gitarre lehnt an der Reling. Siri hat ihren Kopf eine Weile an deine Schulter gelegt.":
        "The fairy lights flicker, the guitar leans against the railing. For a while Siri rested her head on your shoulder.",
    "Eine Rose aus ihrem Haar liegt in deiner Hand, als du zum Tender gehst. Am nächsten Morgen grüßt sie dich am Hafen, als wäre nichts gewesen. Ihre Augen sagen etwas anderes.":
        "A rose from her hair lies in your hand as you walk to the tender. The next morning she greets you at the harbour as if nothing had happened. Her eyes say otherwise.",
    "Am Morgen liegt der Sternzettel auf deinem Platz in der Messe. Unten hat sie etwas dazugeschrieben: „Nacht 2?“":
        "In the morning the page of stars is lying at your place in the mess. At the bottom she has added something: “Night 2?”",
}

if __name__ == "__main__":
    hier = os.path.dirname(os.path.abspath(__file__))
    ziel = os.path.join(os.path.dirname(os.path.dirname(hier)), "docs", "abnahme", "englisch_akt1_extras.json")
    items = [{"key": "extra.%d" % i, "alt": a, "neu": n} for i, (a, n) in enumerate(ALT_NEU.items())]
    json.dump({"id": "englisch_akt1_extras", "titel": "Englisch · Paket 2b: Nebenfelder", "gruppen": [
        {"titel": "Nebenfelder", "items": items}]}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", ziel, len(items))

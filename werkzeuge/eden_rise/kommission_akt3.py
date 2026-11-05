# -*- coding: utf-8 -*-
"""Die Kommission an Tag 35 als Verhandlung (Duc 04.11.2026: "super spannend gemaess Ace Attorney, aber oscarpreistraechtig").
Regeln: kern/kommission.py. Ausgabe: module/eden_rise/kommission.json, gesprochene Zeilen in stimme_tags.json (quelle akt3_kommission).
Wiki: docs/wiki/welt/drehbuch_akt3.md 12a "Kommission". Bildschirm: baut die lokale Sitzung (eigenes Plugin), bis dahin laeuft
die Szenen-Kette a3_kommission.

Ablauf: Titel -> drei Runden (das Feuer, das Tor, das Geld). In jeder Runde liest Maitre Delorme, der Anwalt von A.V., eine
Aussage mit drei Saetzen. Duc kann jeden Satz hinterfragen ("Press") und einen Zeugen oder Beweis gegen einen Satz legen
("Objection!"). Trifft er einen falschen Satz mit einer passenden Karte, kippt die Runde. Legt er falsch, sinkt die Geduld der
Kommission (3). Manche falschen Saetze werden erst nach dem Hinterfragen angreifbar (der Anwalt legt sich fest).
Zum Schluss legt der Anwalt Pascals Kassenbuch gegen das Dorf vor: Duc haelt das Plaedoyer (alles oder nur Alons Teil).
Neue Nebenfiguren (Legenden-Kommentar folgt): Maitre Delorme (Anwalt von A.V., Lyon), der aeltere Kommissar Luciani aus Ajaccio.
Alle Saetze mit Turbo-Tag; die Anzeige zeigt sie ohne."""
import json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
ZIEL = os.path.join(EDEN, "module", "eden_rise", "kommission.json")
TAG = re.compile(r"\s*\[(laugh|chuckle|sigh|gasp|cough|clear throat|sniff|shush)\]\s*")
STIMME = []                    # (wer, Klartext, gesprochen)


def S(wer, text, gefuehl="neutral"):
    klar = TAG.sub(" ", text).strip()
    assert klar != text, "Turbo-Tag fehlt: " + text
    STIMME.append((wer, klar, " ".join(text.split())))
    return {"wer": wer, "text": klar, "gefuehl": gefuehl}


SPRECHER = {"anwalt": "Maître Delorme", "kommissar": "Commissioner Luciani", "megan": "Megan"}

# Karten: was Duc vorlegen kann. "wenn": Bedingung (kern/regeln). "passt": [runde, satz] - welche Saetze die Karte widerlegt.
KARTEN = [
    {"id": "buenaventura", "art": "zeuge", "wer": "bonaventure", "titel": "Captain Buenaventura",
     "text": "He gave the order to burn, and the order to stop. A man named White paid him.",
     "wenn": {"flag": "buenaventura_schwur"}, "passt": [["feuer", 0]]},
    {"id": "riscossore", "art": "zeuge", "wer": "riscossore", "titel": "The Man with the Orange",
     "text": "His debt book, page forty-one: what White offered the captain, in clean money.",
     "wenn": None, "passt": [["geld", 1]]},
    {"id": "befehl", "art": "beweis", "titel": "White's Orders",
     "text": "From the villa cellar. Day 22, phase 3: fire, houses. And a receipt to Captain Buenaventura.",
     "wenn": {"flag": "a3_beweis_feuer"}, "passt": [["feuer", 0], ["geld", 1]]},
    {"id": "batu", "art": "zeuge", "wer": "batu", "titel": "Bà Tư",
     "text": "Men in white asked her twice for the north road, days before the attack.",
     "wenn": {"flag": "a3_zeuge_batu"}, "passt": [["feuer", 1], ["tor", 2]]},
    {"id": "funk", "art": "beweis", "titel": "The Radio Recording",
     "text": "Twenty-one forty, the night before: a calm voice says 'tonight'.",
     "wenn": {"eine": [{"flag": "bl_funk_white"}, {"flag": "bl_funk_charly"}]}, "passt": [["feuer", 1], ["tor", 1]]},
    {"id": "casanova", "art": "zeuge", "wer": "casanova", "titel": "Madame Casanova",
     "text": "The mayor. She stood on the square all night. Nobody came. Nobody at all.",
     "wenn": {"flag": "a3_zeuge_casanova"}, "passt": [["feuer", 2]]},
    {"id": "siri", "art": "beweis", "titel": "Siri's Video",
     "text": "No filter, no music. The gate, the smoke, Minicu. The clock in the corner of the picture.",
     "wenn": {"flag": "a3_siri_post"}, "passt": [["feuer", 2], ["tor", 0]]},
    {"id": "sophia", "art": "beweis", "titel": "Sophia's Notes",
     "text": "Every time and every word she heard on the radio that night, in her small, neat handwriting.",
     "wenn": {"flag": "sophia_notizen"}, "passt": [["feuer", 2], ["tor", 1]]},
    {"id": "alva", "art": "zeuge", "wer": "alva", "titel": "Alva",
     "text": "From the square she saw the north barricade open. Then the men in white came through.",
     "wenn": {"flag": "a3_zeuge_alva"}, "passt": [["tor", 0], ["tor", 2]]},
    {"id": "don", "art": "zeuge", "wer": "anghjulu", "titel": "Don Anghjulu",
     "text": "He was at the church door. He saw the gate open.",
     "wenn": {"flag": "a3_zeuge_anghjulu"}, "passt": [["tor", 0]]},
    {"id": "wache", "art": "beweis", "titel": "The Radio Log",
     "text": "Three o'clock, the night of the twenty-second. Two words from the north road: 'Not yet.'",
     "wenn": {"flag": "bl_wache_gesehen"}, "passt": [["tor", 1]]},
    {"id": "kiste", "art": "beweis", "titel": "The Crate of Collars",
     "text": "From the grotto. Collars with blinking lights, the same white plastic as the men's equipment.",
     "wenn": {"flag": "alon_kiste_genutzt"}, "passt": [["tor", 1]]},
    {"id": "mina", "art": "zeuge", "wer": "mina", "titel": "Mina",
     "text": "She knocked on every door the day the phones were dead. She carries A.V.'s letters too.",
     "wenn": {"flag": "a3_zeuge_mina"}, "passt": [["tor", 2], ["geld", 2]]},
    {"id": "petru", "art": "zeuge", "wer": "petru", "titel": "Petru",
     "text": "A.V. bought the loan on his boat. The letter came two days after the fire.",
     "wenn": {"flag": "a3_zeuge_petru"}, "passt": [["geld", 2]]},
    {"id": "sandru", "art": "zeuge", "wer": "sandru", "titel": "Sandru",
     "text": "His legs work with A.V.'s braces. After he helped the village, A.V. switched them off.",
     "wenn": {"flag": "a3_zeuge_sandru"}, "passt": [["geld", 2]]},
    {"id": "mast", "art": "beweis", "titel": "The Mast Recording",
     "text": "The night of the siege from the ridge: the men in white on the north road, an hour before the attack.",
     "wenn": {"flag": "a3_mast_an"}, "passt": [["feuer", 1], ["tor", 1]]},
    {"id": "tiere", "art": "beweis", "titel": "Bibi's Shoebox",
     "text": "Collars from the animals of the station. Every one sent its last message to the villa.",
     "wenn": {"flag": "mo_ark_beweis"}, "passt": [["tor", 1]]},
]

RUNDEN = [
    {"id": "feuer", "titel": "The Fire",
     "ansage": S("kommissar", "[clear throat] First question. The fire on the night of the twenty-second. Maître, your client's version.", "neutral"),
     "saetze": [
         {"text": S("anwalt", "[clear throat] A band of pirates attacked this village on their own, for loot. It is sad, but it is simple.", "neutral"),
          "falsch": True, "press": S("anwalt", "[chuckle] Pirates steal, Commissioner. That is what the word means. Nobody needs to pay a pirate to be a pirate.", "amusement")},
         {"text": S("anwalt", "[sigh] Nobody could have known it was coming. Not the village, not my client.", "neutral"),
          "falsch": True, "press": S("anwalt", "[clear throat] Nobody. Not one call, not one warning. If someone knew, they kept it to themselves.", "neutral")},
         {"text": S("anwalt", "[clear throat] My client's security team arrived in forty minutes and saved lives. Zero dead.", "pride"),
          "falsch": True, "nur_nach_press": True,
          "press": S("anwalt", "[chuckle] Forty minutes, door to door. It was on every screen in Europe. Ask anyone on this square who saw them.", "pride")},
     ],
     "treffer": S("kommissar", "[sigh] ...Maître. Would you like to say that sentence again? Slowly?", "disapproval"),
     "anwalt_wackelt": S("anwalt", "[cough] I... my client was misinformed about the details. The details.", "nervousness"),
     "dorf": S("petru", "[clear throat] Hm. The sea doesn't lie. Now the paper doesn't either.", "approval")},
    {"id": "tor", "titel": "The Gate",
     "ansage": S("kommissar", "[clear throat] Second question. How did the attackers get into the village?", "neutral"),
     "saetze": [
         {"text": S("anwalt", "[clear throat] The north barricade broke under the attack. Old wood, Commissioner. It simply gave way.", "neutral"),
          "falsch": True, "nur_nach_press": True,
          "press": S("anwalt", "[sigh] Broken, yes. From the outside, by force. It was closed and locked until the very end. I have that in writing.", "neutral")},
         {"text": S("anwalt", "[clear throat] The men in white were my client's security. They came to protect the village, not to attack it.", "neutral"),
          "falsch": True, "press": S("anwalt", "[chuckle] They came when they heard the shots. Not one minute before. Why would they be there before?", "amusement")},
         {"text": S("anwalt", "[sigh] And frankly, nobody in this village saw who came through. It was dark, there was smoke, people were afraid.", "neutral"),
          "falsch": True, "press": S("anwalt", "[clear throat] Not one person. If somebody here saw something, why didn't they say so at the time?", "neutral")},
     ],
     "treffer": S("kommissar", "[gasp] So the barricade did not break. It was opened. Clerk, write that down. In big letters.", "surprise"),
     "anwalt_wackelt": S("anwalt", "[cough] Commissioner, I must ask for a short pause. ...No? No pause. I see.", "nervousness"),
     "dorf": S("mina", "[gasp] They're writing it down. In big letters!", "excitement")},
    {"id": "geld", "titel": "The Money",
     "ansage": S("kommissar", "[clear throat] Last question. Money. Who paid whom, and for what?", "neutral"),
     "saetze": [
         {"text": S("anwalt", "[clear throat] A.V. bought loans in this village to help people. Banks were cruel, my client was kind.", "neutral"),
          "falsch": False, "press": S("anwalt", "[sigh] Lower interest, longer terms. Read the contracts. They are generous.", "neutral")},
         {"text": S("anwalt", "[chuckle] And nobody can prove that my client paid a single euro to anyone in this bay. Not one euro.", "pride"),
          "falsch": True, "press": S("anwalt", "[chuckle] Bring me a bank transfer, a signature, a receipt. You can't. Because there is none.", "pride")},
         {"text": S("anwalt", "[clear throat] My client has never threatened anyone. Not with a letter, not with a word.", "neutral"),
          "falsch": True, "press": S("anwalt", "[sigh] A letter about a loan is not a threat. It is a letter. People send letters.", "neutral")},
     ],
     "treffer": S("kommissar", "[sigh] Page forty-one, Maître. Or a receipt. Or a man whose legs were switched off. Choose which one you'd like to explain first.", "anger"),
     "anwalt_wackelt": S("anwalt", "[cough] ...I would like to speak with my client.", "fear"),
     "dorf": S("batu", "[chuckle] Eat, Maître. You look pale.", "amusement")},
]

PLAEDOYER = {
    "ansage": S("anwalt", "[clear throat] One last thing. This village is not innocent. A cash book, from the deputy mayor's drawer. The priest. "
                          "The man with the braces. Your own mayor, Madame Casanova. They all took his money.", "pride"),
    "stille": S("kommissar", "[sigh] ...First Officer. The lieutenant from the coast guard says you have the original. All of it, or only the part about Alon?", "neutral"),
    "alles": {"chip": "“All of it. They'll carry it. And they'll stand next to the truth.”",
              "folge": S("casanova", "[sigh] Yes. Me too. Write my name first.", "pride"),
              "kommission": S("kommissar", "[clear throat] A village that confesses its own debts. Twenty-two years in this job, and that is a first.", "admiration")},
    "teil": {"chip": "“Only Alon's part. The village has paid enough.”",
             "folge": S("casanova", "[sigh] ...Thank you, Monsieur. I won't forget it. Neither will Don.", "gratitude"),
             "kommission": S("kommissar", "[clear throat] Noted. The rest of the book stays a village matter. For now.", "neutral")},
}

TEXTE = {
    "titel": "The Commission", "untertitel": "Day 35 · the quay · two men from Ajaccio and a folding table",
    "eroeffnung": S("kommissar", "[clear throat] We are here to find out what happened in this bay on the twenty-first, twenty-second and "
                                 "twenty-third. Maître Delorme speaks for A.V. You speak for the village. Three questions.", "neutral"),
    "anwalt_auftritt": S("anwalt", "[chuckle] Commissioner. Gentlemen. Good people of Cala d'Orsu. My client sends his warmest regards. "
                                   "He is very busy saving the world.", "amusement"),
    # Duc 05.11.2026 (LATE_GAME.md, Punkt 2): die Kommission als Echo der Anhoerung aus Akt 1, kein neues System
    "erinnerung": S("megan", "[clear throat] Duc. You did this once already, at the hearing on the yacht. Ask until he says it clearly. "
                             "Then put the proof on the lie. Same game. Bigger table.", "neutral"),
    "falsch_gelegt": [S("kommissar", "[sigh] That doesn't answer the sentence, First Officer.", "annoyance"),
                      S("kommissar", "[clear throat] We are not here for guesses. Please.", "disapproval"),
                      S("kommissar", "[sigh] My patience is a small boat, First Officer. Don't make it sink.", "annoyance")],
    "falsch_wahr": S("anwalt", "[chuckle] Objection to the objection. That sentence happens to be true.", "amusement"),
    "zu_frueh": S("anwalt", "[clear throat] I said nothing of the kind, Commissioner. Perhaps the First Officer should listen first.", "amusement"),
    "geduld_weg": S("kommissar", "[sigh] Enough. We have heard enough guesses. We will decide with what we have.", "anger"),
    "nichts": S("kommissar", "[sigh] No answer? Then the sentence stands as it is.", "neutral"),
    "urteil": {3: S("kommissar", "[clear throat] Thank you. We have what we need. All three questions. You'll know tonight, but I think you know already.", "admiration"),
               2: S("kommissar", "[clear throat] Thank you. Two questions answered, one still open. You'll know tonight.", "neutral"),
               1: S("kommissar", "[sigh] Thank you. One answer is not much. You'll know tonight.", "neutral"),
               0: S("kommissar", "[sigh] Thank you, everyone. We will write our report. Don't expect too much from it.", "sadness")},
}


def daten():
    return {"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\kommission_akt3.py - dort aendern. Regeln: kern/kommission.py.",
            "sprecher": SPRECHER, "geduld": 3, "texte": TEXTE, "runden": RUNDEN, "karten": KARTEN, "plaedoyer": PLAEDOYER}


def pruefe(d):
    f = []
    ids = {r["id"] for r in d["runden"]}
    for k in d["karten"]:
        for r, i in k["passt"]:
            if r not in ids:
                f.append("%s: Runde %s" % (k["id"], r))
            elif not next(x for x in d["runden"] if x["id"] == r)["saetze"][i]["falsch"]:
                f.append("%s: widerlegt einen wahren Satz (%s %d)" % (k["id"], r, i))
    for r in d["runden"]:
        for i, s in enumerate(r["saetze"]):
            if s["falsch"] and not any([r["id"], i] in k["passt"] for k in d["karten"]):
                f.append("%s %d: falsch, aber keine Karte widerlegt ihn" % (r["id"], i))
    return f


def tags_schreiben():
    pfad = os.path.join(EDEN, "module", "eden_rise", "stimme_tags.json")
    d = json.load(open(pfad, encoding="utf-8"))
    neu = [{"wer": w, "text": t, "gesprochen": g, "quelle": "akt3_kommission"} for w, t, g in STIMME]
    texte = {(z["wer"], z["text"]) for z in neu}
    d["zeilen"] = [z for z in d["zeilen"] if z.get("quelle") != "akt3_kommission" and (z["wer"], z["text"]) not in texte] + neu
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(neu)


if __name__ == "__main__":
    d = daten()
    fehler = pruefe(d)
    for x in fehler:
        print("FEHLER", x)
    if fehler:
        raise SystemExit(1)
    json.dump(d, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("kommission.json: %d Runden, %d Karten, %d Zeilen -> stimme_tags.json" % (len(d["runden"]), len(d["karten"]), tags_schreiben()))

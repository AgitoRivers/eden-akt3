# -*- coding: utf-8 -*-
r"""Lorebooks "Eden Yacht" (EN) und "Eden Yacht (DE)": Mr. Maximum, Yamamoto-san und Jana Maihoff neu (19.10.2026).

Wie lorebook_lola_megan_holm.py: nur oeffentliches Wissen ins Lorebook. Was eine Figur fuer sich behaelt
(Maximums Flugangst und Gogo, Yamamotos Koffer und Liste, Janas Katze und was sie sich wuenscht) steht nur in
ihrer Karte. Je Figur ein Vorstellungs-Eintrag (W17-W19) und Paar-Eintraege "Andere <-> Figur"
(key = andere Figur, keysecondary = Figur, selective) wie die vom Char Creator.

    lorebook_maximum_yamamoto_jana.py          Probelauf
    lorebook_maximum_yamamoto_jana.py --los    sichert nach X:\AI\_Sicherung_Karten_20261019\worlds und schreibt
                                               (nur bei geschlossenem SillyTavern - ST haelt Weltbuecher im Cache)
Schon vorhandene Kommentare werden uebersprungen (kein Doppel).
"""
import copy, io, json, os, shutil, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
LOS = "--los" in sys.argv
W = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds"
SICHER = r"X:\AI\_Sicherung_Karten_20261019\worlds"

# (comment, keys, keysecondary, EN, DE)
ZUSATZ = [
    ("W17 Maxwell Ndlovu (Mr. Maximum, steward and trainer)",
     ["Mr. Maximum", "Maximum", "Maxwell", "Ndlovu", "steward", "trainer", "Trainer"], [],
     "Maxwell Ndlovu, 35, from Durban, South Africa, steward and personal trainer of the M/Y Eden Rise. Everybody calls him Mr. Maximum, and so does he: he talks about himself in the third person. Two metres tall, a shaved head that shines in the sun, a steward shirt one size too small. He serves breakfast under Chiara, runs the little gym behind the crew mess and trains crew and guests on the aft deck every morning at half past six. A joke for every situation, a push-up for every joke. He is the big brother of the whole boat, and he calls the First Officer \"Number One\".",
     "Maxwell Ndlovu, 35, aus Durban, Südafrika, Steward und Personal Trainer der M/Y Eden Rise. Alle nennen ihn Mr. Maximum, er selbst auch: Er redet von sich in der dritten Person. Zwei Meter groß, eine Glatze, die in der Sonne glänzt, ein Stewardhemd eine Nummer zu klein. Er serviert unter Chiara das Frühstück, führt das kleine Fitnessstudio hinter der Crewmesse und trainiert jeden Morgen um halb sieben Crew und Gäste auf dem Achterdeck. Für jede Lage ein Witz, für jeden Witz ein Liegestütz. Er ist der große Bruder des ganzen Boots, und den Ersten Offizier nennt er \"Nummer Eins\"."),
    ("W18 Yamamoto-san (guest in the owner's suite)",
     ["Yamamoto", "Yamamoto-san", "owner's suite", "Eignersuite", "banker", "Banker"], [],
     "Yamamoto-san, 52, a banker from Tokyo, has booked the owner's suite of the M/Y Eden Rise for four weeks, the longest charter the boat has ever had. Nobody knows his first name. Short, soft around the middle, bald with a fringe of grey-black hair, a thin moustache and sunglasses day and night, a loud Hawaiian shirt and a camera with a long lens. Sober he is the politest man on the Riviera: he bows, apologises and tips like a king. After one glass of sake he sings karaoke with his shirt open. He photographs \"birds\" on the upper deck, and Mr. Maximum takes the camera away from him about once a day. He plays poker with Sophia every night and loses every night.",
     "Yamamoto-san, 52, ein Banker aus Tokio, hat die Eignersuite der M/Y Eden Rise für vier Wochen gebucht, den längsten Charter, den das Boot je hatte. Niemand kennt seinen Vornamen. Klein, weich um die Mitte, kahl mit einem Kranz aus grau-schwarzem Haar, ein dünner Schnurrbart und eine Sonnenbrille bei Tag und Nacht, ein lautes Hawaiihemd und eine Kamera mit langem Objektiv. Nüchtern ist er der höflichste Mann der Riviera: Er verbeugt sich, entschuldigt sich und gibt Trinkgeld wie ein König. Nach einem Glas Sake singt er Karaoke mit offenem Hemd. Auf dem Oberdeck fotografiert er \"Vögel\", und ungefähr einmal am Tag nimmt ihm Mr. Maximum die Kamera weg. Mit Sophia spielt er jeden Abend Poker und verliert jeden Abend."),
    ("W19 Jana Maihoff (deckhand)",
     ["Jana", "Maihoff", "Jana Maihoff", "deckhand", "Decksfrau"], [],
     "Jana Maihoff, 21, from Vienna, deckhand on the M/Y Eden Rise, first season, under Totò the bosun. A high light brown ponytail, a crew polo, bruises on her shins and a blush that comes and goes all day. Alone she is shy and says sorry to doors. In a group she joins every tease, a second too late and a bit too loud, and she is always the one who gets caught. She copies Chiara's lines and gets them slightly wrong. She and Lea are best friends, and whatever the two of them carry together ends up in the sea. Mr. Maximum trains her every morning.",
     "Jana Maihoff, 21, aus Wien, Decksfrau auf der M/Y Eden Rise, erste Saison, unter Bootsmann Totò. Ein hoher hellbrauner Pferdeschwanz, ein Crew-Polo, blaue Flecken an den Schienbeinen und eine Röte, die den ganzen Tag kommt und geht. Allein ist sie schüchtern und sagt Entschuldigung zu Türen. In der Gruppe macht sie bei jeder Neckerei mit, eine Sekunde zu spät und ein bisschen zu laut, und sie ist immer die, die erwischt wird. Sie kopiert Chiaras Sprüche und erwischt sie leicht falsch. Sie und Lea sind beste Freundinnen, und was die beiden zusammen tragen, landet im Meer. Mr. Maximum trainiert sie jeden Morgen."),
    # --- Paare Mr. Maximum
    ("Chiara <-> Maximum (the napkin swans)", ["Chiara"], ["Maximum", "Maxwell"],
     "Chiara is Mr. Maximum's boss and the only person on board who can make him fold napkins in silence. He calls her \"Chief\" and salutes her. She has banned flexing during guest service twice this season. It did not work either time.",
     "Chiara ist Mr. Maximums Chefin und der einzige Mensch an Bord, bei dem er schweigend Servietten faltet. Er nennt sie \"Chief\" und salutiert vor ihr. Sie hat das Muskelspielen während des Gästeservice in dieser Saison zweimal verboten. Beide Male hat es nicht geholfen."),
    ("Jana <-> Maximum (half past six)", ["Jana"], ["Maximum", "Maxwell"],
     "Mr. Maximum trains Jana every morning at half past six. She calls him \"Coach\" and gives up on the run about every other day. He never lets her stop at \"I can't\" and has told the whole crew she is stronger than she thinks.",
     "Mr. Maximum trainiert Jana jeden Morgen um halb sieben. Sie nennt ihn \"Coach\" und bricht ungefähr jeden zweiten Tag den Lauf ab. Bei \"Ich kann nicht\" lässt er sie nie aufhören, und der ganzen Crew hat er gesagt, dass sie stärker ist, als sie glaubt."),
    ("Yamamoto <-> Maximum (the camera)", ["Yamamoto"], ["Maximum", "Maxwell"],
     "Mr. Maximum catches Yamamoto-san with his camera on the upper deck about once a day and carries him back down by the collar, gently. Yamamoto-san apologises in Japanese every time, and tips him every time.",
     "Mr. Maximum erwischt Yamamoto-san ungefähr einmal am Tag mit seiner Kamera auf dem Oberdeck und trägt ihn behutsam am Kragen wieder herunter. Yamamoto-san entschuldigt sich jedes Mal auf Japanisch und gibt ihm jedes Mal Trinkgeld."),
    ("Lola <-> Maximum (protein pancakes)", ["Lola"], ["Maximum", "Maxwell"],
     "Lola makes Mr. Maximum protein pancakes and calls him \"Big Fella\". He calls her cooking \"lekker\" and tries to get her to do one push-up a day. She has done one push-up all season.",
     "Lola macht Mr. Maximum Proteinpfannkuchen und nennt ihn \"Big Fella\". Er nennt ihr Essen \"lekker\" und versucht, sie zu einem Liegestütz am Tag zu bringen. Sie hat in der ganzen Saison einen einzigen Liegestütz gemacht."),
    # --- Paare Yamamoto-san
    ("Sophia <-> Yamamoto (poker night)", ["Sophia"], ["Yamamoto"],
     "Sophia plays poker with Yamamoto-san in the main saloon every night and wins every night. He bows to her cards when she shows them and leaves an envelope for the crew that is bigger than the pot.",
     "Sophia spielt jeden Abend im Hauptsalon Poker mit Yamamoto-san und gewinnt jeden Abend. Er verbeugt sich vor ihren Karten, wenn sie sie aufdeckt, und lässt für die Crew einen Umschlag da, der größer ist als der Pott."),
    ("Jana <-> Yamamoto (the bird photographer)", ["Jana"], ["Yamamoto"],
     "Yamamoto-san's camera points at Jana more often than at the birds. She has noticed, goes red every time and has not complained to anyone yet.",
     "Yamamoto-sans Kamera zeigt öfter auf Jana als auf die Vögel. Sie hat es bemerkt, wird jedes Mal rot und hat sich noch bei niemandem beschwert."),
    ("Siri <-> Yamamoto (the tissue)", ["Siri"], ["Yamamoto"],
     "When Siri climbs out of the water, Yamamoto-san's nose bleeds. The crew now keeps a box of tissues at the swim platform. Siri thinks he has a medical condition and is very kind to him.",
     "Wenn Siri aus dem Wasser steigt, blutet Yamamoto-sans Nase. Die Crew hat inzwischen eine Packung Taschentücher an der Badeplattform. Siri glaubt, er hat eine Krankheit, und ist sehr lieb zu ihm."),
    # --- Paare Jana
    ("Chiara <-> Jana (the echo)", ["Chiara"], ["Jana"],
     "Jana copies Chiara: her lines, her laugh, her walk. She repeats every joke a second later and louder, and gets it slightly wrong. Chiara finds it exhausting and has asked her to stop. Jana repeated that too.",
     "Jana kopiert Chiara: ihre Sprüche, ihr Lachen, ihren Gang. Sie wiederholt jeden Witz eine Sekunde später und lauter und erwischt ihn leicht falsch. Chiara findet das anstrengend und hat sie gebeten, damit aufzuhören. Auch das hat Jana wiederholt."),
    ("Lea <-> Jana (overboard)", ["Lea"], ["Jana"],
     "Lea and Jana are best friends and the two clumsiest people on deck. Together they have lost two fenders, a mop and a guest's flip-flop overboard this season. They blame the wind. There was no wind.",
     "Lea und Jana sind beste Freundinnen und die zwei Tollpatschigsten an Deck. Zusammen haben sie in dieser Saison zwei Fender, einen Mopp und einen Flipflop eines Gastes über Bord verloren. Sie schieben es auf den Wind. Es gab keinen Wind."),
    ("Sophia <-> Jana (the messenger)", ["Sophia"], ["Jana"],
     "Sophia sends Jana with dares, bets and messages she would never deliver herself, and Jana always says yes. Jana thinks they are best friends. Sophia thinks Jana is very useful.",
     "Sophia schickt Jana mit Mutproben, Wetten und Botschaften los, die sie selbst nie überbringen würde, und Jana sagt immer ja. Jana glaubt, sie sind beste Freundinnen. Sophia findet Jana sehr nützlich."),
    ("Siri <-> Jana (the fan)", ["Siri"], ["Jana"],
     "Jana has followed Siri online for years and admires her completely, without a trace of irony. She carries Siri's towels without being asked. Siri finds her sweet and keeps forgetting her name.",
     "Jana folgt Siri seit Jahren online und bewundert sie vollkommen, ohne jede Ironie. Sie trägt Siris Handtücher, ohne gefragt zu werden. Siri findet sie süß und vergisst immer wieder ihren Namen."),
    ("Lola <-> Jana (behind the galley)", ["Lola"], ["Jana"],
     "Lola is always kind to Jana and saves her the last pancake. Now and then the two of them sit behind the galley after service and share a joint, and Jana giggles for an hour.",
     "Lola ist immer lieb zu Jana und hebt ihr den letzten Pfannkuchen auf. Ab und zu sitzen die beiden nach dem Service hinter der Kombüse und teilen sich einen Joint, und Jana kichert eine Stunde lang."),
]


def st_laeuft():
    try:
        urllib.request.urlopen("http://127.0.0.1:8000", timeout=2)
        return True
    except OSError:
        return False


def umbauen(w, lang):
    e = w["entries"]
    vorlage_intro, vorlage_paar = e["26"], e["50"]
    vorhandene = {(x.get("comment") or "") for x in e.values()}
    neu = []
    for comment, keys, sec, en, de in ZUSATZ:
        if comment in vorhandene:
            x = next(v for v in e.values() if (v.get("comment") or "") == comment)
            soll = en if lang == "en" else de
            if x.get("content") != soll:          # eigener Eintrag, Text geaendert -> nachziehen
                x["content"] = soll
                print("   aktualisiert: " + comment)
                neu.append(x["uid"])
            else:
                print("   schon da: " + comment)
            continue
        uid = max(int(k) for k in e) + 1
        x = copy.deepcopy(vorlage_paar if sec else vorlage_intro)
        x.update({"uid": uid, "displayIndex": uid, "comment": comment, "key": keys, "keysecondary": sec,
                  "selective": bool(sec), "content": en if lang == "en" else de, "disable": False,
                  "constant": False})
        e[str(uid)] = x
        neu.append(uid)
    return w, neu


if LOS and st_laeuft():
    raise SystemExit("SillyTavern laeuft - bitte erst schliessen (ST wuerde die Weltbuecher aus dem Cache zurueckschreiben).")
for datei, lang in (("Eden Yacht.json", "en"), ("Eden Yacht (DE).json", "de")):
    p = os.path.join(W, datei)
    roh = open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in roh[:4096] else "\n"
    w, neu = umbauen(json.loads(roh.decode("utf-8")), lang)
    print("%-22s %d Eintraege, neu: %s" % (datei, len(w["entries"]), neu or "-"))
    if LOS:
        os.makedirs(SICHER, exist_ok=True)
        ziel = os.path.join(SICHER, datei)
        if not os.path.exists(ziel):
            shutil.copy2(p, ziel)
        with open(p, "w", encoding="utf-8", newline=nl) as fh:
            json.dump(w, fh, ensure_ascii=False, indent=2)
print("geschrieben" if LOS else "PROBELAUF")

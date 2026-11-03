# -*- coding: utf-8 -*-
r"""Nachbesserung der Tierstation-Saetze (01.11.2026), nach Durchsicht der Kontaktboegen: Bartgeier-Fluegel am Rand, aufgerichtete Tiere ohne Beine,
Schildkroete nicht im Panzer, Madame schlaeft mit offenen Augen. Neue Bilder landen als <pose>-1.png neben dem alten, verglichen und getauscht wird danach.
QUADRAT = Posen, die Hoehe brauchen. Ablauf wie kampf_tierstation_posen.py, Kartentexte danach zurueckgesetzt.

    kampf_tierstation_nach.py --los
"""
import io, json, os, subprocess, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
HIER = os.path.dirname(os.path.abspath(__file__))
ALLES = ", the bird small in the frame with wide empty space on all sides, the whole bird and both wingtips fully inside the image"
RUND = ", small in the frame with wide empty space on all sides, the whole animal from the top of its head to its hind feet fully inside the image"
AUS = ", the whole animal fully inside the image with empty space around it, one single animal, clean empty floor, eyes firmly closed, mouth closed"

NACH = {
    "BeardedVulture": {
        "windup": "crouched on its strong legs, both wings half raised behind its body, head pulled back, eyes locked to the left, ready to spring" + ALLES,
        "attack": "swooping forward to the left a little above the ground, both talons reaching forward, wings spread, beak open, slight motion blur on the talons" + ALLES,
        "heavy_windup": "rearing up tall with both huge wings spread and raised high, chest out, beak open" + ALLES,
        "heavy_attack": "diving towards the left, wings swept back along its body, both talons stretched forward, beak open, motion blur on the talons" + ALLES,
        "guard": "standing with one wing folded in front of its chest like a shield, peeking to the left over the wing, both feet on the ground" + ALLES,
        "hurt": "knocked backwards, wings half open, feathers ruffled, head thrown back, eye squeezed shut, beak open, both feet on the ground" + ALLES,
        "enraged": "head and chest feathers standing up, rust-orange ruff spread wide, wings half open, beak wide open, screaming to the left, both feet on the ground" + ALLES,
        "flee": "flapping away, seen from the side, wings beating, feet just off the ground" + ALLES,
        "victory": "standing tall on both feet, wings folded, chest out, looking down to the left along its beak" + ALLES,
        "defeated": "lying collapsed on its belly on the ground, wings folded close to its body, the head on the floor on the RIGHT side of the image, eyes closed" + ALLES,
        "death": "lying on its belly on the ground, wings folded close to its body, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + ALLES,
    },
    "RussianBlue": {
        "heavy_windup": "standing upright on its short hind legs, very round belly showing, both front paws raised high with claws out, puffed up, furious" + RUND,
        "hurt": "knocked backwards onto its round rump, head thrown back, eyes squeezed shut, mouth open, front paws in the air, tail curled in" + RUND,
        "weakened": "sitting heavily with its round belly on the ground, head hanging low, eyes half closed, mouth closed, swaying, tired",
        "surrender": "asleep, lying on its round belly with its chin on its front paws, ears relaxed, the small red light on its collar still on" + AUS,
        "defeated": "lying asleep on its side, round belly showing, legs limp, the head on the floor on the RIGHT side of the image" + AUS,
        "death": "lying flat on its side, legs stretched out, the head on the floor on the RIGHT side of the image, motionless, peaceful" + AUS,
    },
    "Capybara": {
        "heavy_windup": "rearing up on its hind legs with its barrel body upright, front feet in the air, mouth wide open, showing long front teeth" + RUND,
        "attack": "charging forward to the left in a long stride, all four legs stretched, heavy body low, mouth wide open with its long front teeth showing, slight motion blur on the legs",
    },
    "Tortoise": {
        "guard": "closed up inside its shell, the head and neck and all four legs pulled in and hidden, only the closed domed shell with the number 12 resting on the floor, a few thick scales at the openings, one small red light glowing at the front opening",
        "weakened": "shell resting flat on the floor, neck hanging out limp along the ground, eyes half closed, legs splayed out flat",
    },
    "RedPanda": {
        "heavy_windup": "standing upright on its hind legs with both front paws raised high and wide to look big, fluffy tail behind it, mouth open, black belly showing" + RUND,
        "hurt": "knocked backwards onto its rump, head thrown back, eyes squeezed shut, mouth open, front paws in the air, fluffy tail curled in close" + RUND,
    },
}
ENG = ", its wings half folded close to its body, the bird small in the frame in the middle of a wide empty space, a wide margin of empty space on all four sides"
# Zweite Runde (Duc 01.11.: Bones oft abgeschnitten): gespannte Fluegel passen nicht ins Bild, darum angelegt und quadratisch. Messung am Bildrand.
BONES2 = {"BeardedVulture": {
    "windup": "crouched low on its strong legs, head pulled back, eyes locked to the left, ready to spring" + ENG,
    "attack": "hopping forward to the left, both talons reaching forward just above the ground, beak open, slight motion blur on the talons" + ENG,
    "heavy_windup": "standing very tall on its legs, chest out, neck stretched up, beak wide open, shrieking" + ENG,
    "heavy_attack": "stabbing its head and heavy beak down and forward to the left, one talon lifted, whole body leaning in, motion blur on the head" + ENG,
    "flee": "running away on its long legs, seen from the side, neck stretched forward, feet on the ground" + ENG,
}}
LUFT = ". Photographed from very far away with a long lens: one tiny distant bird in the middle of a huge pale empty sky, seen from the side, the bird fills only one quarter of the width of the image, nothing but empty sky all around it on every side"
# Dritte Runde (Duc 01.11.: Bones soll fliegen): in der Luft, von der Seite, damit die Spannweite ins Querformat passt. Nur Schlaf und Boden bleiben unten.
BONES3 = {"BeardedVulture": {
    "idle": "hovering in the air, facing left, both wings raised above its back, tail fanned, legs hanging, head low, beak open, pale wild eye" + LUFT,
    "windup": "flying, facing left, both wings pulled far back behind its body, talons drawn up under its chest, eyes locked to the left" + LUFT,
    "attack": "swooping to the left, both talons stretched forward, both wings raised above its back, beak open, slight motion blur on the talons" + LUFT,
    "heavy_windup": "climbing steeply, facing left and up, both wings beating high above its back, tail fanned, beak open" + LUFT,
    "heavy_attack": "diving steeply down to the left, wings folded along its body, both talons stretched forward, beak open, motion blur on the talons" + LUFT,
    "guard": "braking in the air, facing left, both wings thrown forward in front of its chest, talons raised" + LUFT,
    "hurt": "knocked backwards in the air, tumbling, wings bent and ruffled, head thrown back, eye squeezed shut, beak open" + LUFT,
    "enraged": "hovering, facing left, rust-orange ruff spread wide, both wings beating above its back, beak wide open, screaming" + LUFT,
    "weakened": "flying badly and sinking, facing left, wings drooping below its body, legs hanging, head low, eye half closed" + LUFT,
    "flee": "flying away, facing left, wings raised above its back, looking over its shoulder" + LUFT,
    "victory": "gliding in the air, facing left, both wings raised in a shallow V, chest out, looking down to the left along its beak" + LUFT,
}}
if "--bones" in sys.argv:
    NACH = BONES2
if "--fliegt" in sys.argv:
    NACH = BONES3
    if "--spitzen" in sys.argv:                            # nur die Posen, bei denen eine Fluegelspitze noch den Rand beruehrt
        NACH = {"BeardedVulture": {p: BONES3["BeardedVulture"][p].replace("one quarter", "one fifth") for p in ("attack", "enraged", "victory")}}
    if "--rest" in sys.argv:                               # Duc nimmt die Flug-Fassung: Angriff mit Fluegeln nach hinten, damit oben nichts mehr anstoesst; Schlaf mit geschlossenen Augen
        NACH = {"BeardedVulture": {
            "attack": "swooping to the left, body stretched long and flat, both wings swept far back behind its tail, both talons stretched forward, beak open, slight motion blur on the talons" + LUFT,
            "surrender": "fast asleep on the ground, lying on its belly, wings folded close to its body, the head resting flat on the floor, both eyelids shut, beak closed, the small red light on its collar still on" + ENG,
        }}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


print(", ".join("%s %d" % (n, len(p)) for n, p in NACH.items()))
if "--los" not in sys.argv:
    sys.exit("PROBELAUF - mit --los einstellen")
original = {c["name"]: c["prompt"] for c in ps("/api/state")["decks"]["kampf"]}
n = 0
try:
    for wer, posen in NACH.items():
        for pose, text in posen.items():
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == pose:
                    c["prompt"] = text
            ps("/api/decks", d)
            flag = ["--quadrat"] if "--bones" in sys.argv or (pose == "heavy_windup" and wer != "BeardedVulture") else []
            subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", pose, "--gegner", wer] + flag, check=True, stdout=subprocess.DEVNULL)
            n += 1
    if "--bones" in sys.argv or "--fliegt" in sys.argv:
        sys.exit("eingestellt: %d Bones-Posen" % n)
    d = ps("/api/state")["decks"]
    for c in d["outfit"]:
        if c["name"] == "kampf_snowleopardfrei":
            c["prompt"] = "a powerful low body, thick smoky grey-white fur with soft dark smudges, a very long thick fluffy tail, a broad head, pale green eyes half closed, mouth closed, a bare neck, lying relaxed with its chin up, calm and elegant"
    for c in d["kampf"]:
        if c["name"] in original:
            c["prompt"] = original[c["name"]]
    ps("/api/decks", d)
    subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--gegner", "SnowLeopardFrei"], check=True, stdout=subprocess.DEVNULL)
finally:
    d = ps("/api/state")["decks"]
    for c in d["kampf"]:
        if c["name"] in original:
            c["prompt"] = original[c["name"]]
    ps("/api/decks", d)
print("eingestellt: %d Posen + Schneeleopard Station, Kartentexte zurueckgesetzt" % n)

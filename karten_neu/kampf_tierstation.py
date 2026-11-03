# -*- coding: utf-8 -*-
r"""Neue Tiere fuer Bibis Tierstation (Duc 01.11.2026: "10 weitere Tiere", Wiki systeme/tierstation.md). Zehn neue Sprites,
dazu kommen WildschweinKlein, Seagull und BearCub aus dem Bestand. Aufbau wie kampf_neue_gegner_7.py. Keine Lochmuster.

    kampf_tierstation.py          Probelauf
    kampf_tierstation.py --los    Karte ueber die Studio-API, Preset/Set-Preset per DucCommon
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))   # stdout is set to UTF-8 by studio_kampf_gegner on import
sys.path.insert(0, HERE)
GO = "--los" in sys.argv
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402
from kampf_alphas import ZOO_COLLAR as COLLAR  # noqa: E402

PS = "http://127.0.0.1:8301"
# key: (subject, look)
NEW = {   # Jedes Tier traegt das Halsband, das es verrueckt macht (Duc 01.11.2026), darum wild und ausser sich statt ruhig
    "RedPanda": ("a red panda",
                 "thick rust-red fur, a white face with dark red tear marks, white-edged round ears, black legs and belly, a long fluffy tail with pale rings, small sharp teeth bared, wild staring eyes, fur bristling, " + COLLAR),
    "SnowLeopard": ("a snow leopard",
                    "a powerful low body, thick smoky grey-white fur with soft dark smudges, a very long thick fluffy tail, a broad head, pale green eyes wide and wild, long fangs bared, " + COLLAR),
    "Komodo": ("a huge Komodo dragon",
               "a long heavy low body, thick dull grey-brown leathery skin with smooth folds, a long muscular tail, a flat broad head, a long yellow forked tongue, small cold furious eyes, thick bowed legs with long claws, the whole long tail inside the image, " + COLLAR),
    "RussianBlue": ("a chubby Russian Blue cat",
                    "a very round plump body with a big soft belly, a dense short plush blue-grey coat with a silver sheen, a wide round face, short legs, vivid green eyes wide open and wild, snarling with its small fangs, fur standing up, furious, " + COLLAR),
    "CorsicanStag": ("a Corsican red deer stag",
                     "a small stocky body, a short dark reddish-brown coat, thin ribs showing, antlers with one side snapped short, rolling wild eyes, frantic, " + COLLAR),
    "BeardedVulture": ("a huge bearded vulture",
                       "rust-orange feathers on the head and chest, a black mask across pale eyes with a red ring, a small black beard of bristles under the beak, long dark grey wings half spread, wild and furious, " + COLLAR),
    "Tortoise": ("a large old Hermann's tortoise",
                 "a high domed shell of black and yellow plates, the number 12 painted in white on one plate, a wrinkled grey-brown head stretched far out and furious, small black eyes, thick scaly legs, " + COLLAR),
    "Donkey": ("a small grey Corsican donkey",
               "all four hooves fully in the image, a shaggy mouse-grey coat, a dark cross on its back, long ears with one bent over, a pale muzzle, bared teeth, rolling wild eyes, furious, " + COLLAR),
    "Hedgehog": ("one big round European hedgehog",
                 "dense brown and cream spines standing straight up, soft pale fur on its belly and face, a small black wet nose, tiny dark eyes, short legs, furious, " + COLLAR),
    "Capybara": ("a large capybara",
                 "a barrel-shaped body, coarse reddish-brown fur, a big blunt square muzzle, small round ears, wide staring eyes, bared long front teeth, wild and frantic, " + COLLAR),
}

# Dasselbe Tier an der Station (Duc 01.11.2026): Das Halsband ist ab, es ist ruhig, und Duc kann es besuchen. Nur idle, Ablage als <Name>Frei.
FREI = {
    "RedPanda": ("a red panda", "thick rust-red fur, a white face with dark red tear marks, white-edged round ears, black legs and belly, a long fluffy tail with pale rings, soft dark eyes, a bare neck, holding a bamboo leaf, curious and sweet"),
    "SnowLeopard": ("a snow leopard", "a powerful low body, thick smoky grey-white fur with soft dark smudges, a very long thick fluffy tail, a broad head, pale green eyes half closed, a bare neck, calm and elegant"),
    "Komodo": ("a huge Komodo dragon", "a long heavy low body, thick dull grey-brown leathery skin with smooth folds, a long muscular tail, a flat broad head, a long yellow forked tongue, small cold patient eyes, thick bowed legs with long claws, a bare neck, the whole long tail inside the image, lying in the sun, entirely unbothered"),
    "RussianBlue": ("a chubby Russian Blue cat", "a very round plump body with a big soft belly, a dense short plush blue-grey coat with a silver sheen, a wide round face, short legs, calm vivid green half-closed eyes, a bare neck, content and pleased with itself"),
    "CorsicanStag": ("a Corsican red deer stag", "a small stocky body, a short dark reddish-brown coat, antlers with one side snapped short, a bare neck with a healed line in the fur, gentle dark eyes, relaxed and healthy"),
    "BeardedVulture": ("a huge bearded vulture", "rust-orange feathers on the head and chest, a black mask across pale eyes with a red ring, a small black beard of bristles under the beak, long dark grey wings folded, a bare feathered neck, calm and curious"),
    "Tortoise": ("a large old Hermann's tortoise", "a high domed shell of black and yellow plates, the number 12 painted in faded white on one plate, a wrinkled grey-brown head, small black eyes, a bare wrinkled neck, chewing a leaf, deeply unimpressed"),
    "Donkey": ("a small grey Corsican donkey", "all four hooves fully in the image, a shaggy mouse-grey coat, a dark cross on its back, long ears with one bent over, a pale muzzle, a bare neck, calm and stubborn"),
    "Hedgehog": ("one big round European hedgehog", "dense brown and cream spines lying flat, soft pale fur on its belly and face, a small black wet nose, tiny dark eyes, short legs, a bare neck, content"),
    "Capybara": ("a large capybara", "a barrel-shaped body, coarse reddish-brown fur, a big blunt square muzzle, small round ears, calm half-closed eyes, a bare neck, completely at peace"),
    "Dog": ("a big brindle mastiff mix", "short brindle fur, a broad head with soft jowls, a bare neck with an old rope mark, thin but healthy, warm brown eyes, a wagging tail, happy"),
    "ArkHyena": ("a spotted hyena", "a sloped back, a shaggy brown and grey coat with soft dark spots, round ears, a bare neck with small healed burn marks, a small tired smile, calm"),
    "PlatedMouflon": ("a large mouflon ram", "the whole body from the top of its head down to all four feet fully inside the image with wide empty space around it, a thick russet coat, heavy curled horns, a bare neck, smooth healed marks on the shoulders where the fur is growing back, proud and calm, looking down its nose"),
    "Ape": ("a large mischievous ape", "the whole body from the top of its head down to all four feet fully inside the image with wide empty space around it, sitting down, dark shaggy fur, long powerful arms, a leathery face, a small shaved patch behind one ear, a bare neck, holding one clean spanner, clever calm eyes"),
    "Wolf": ("a grey wolf", "thick grey fur, one torn ear, pale yellow eyes, a bare neck, lean and healthy, standing quiet and watchful"),
    "BearCub": ("a very small young brown bear cub, a baby bear only a few months old", "fluffy fur, a huge round baby head, short stubby legs, round ears, a small light muzzle, big round dark eyes, clumsy oversized paws, a bare neck, happy and curious"),
    "Panther": ("a black panther", "a sleek glossy black coat, a long tail, piercing green eyes half closed, a bare neck with one old scar across its face, relaxed, lazy and calm"),
    "WildschweinKeiler": ("a big old Corsican wild boar", "the whole body fully inside the image with wide empty space around it, thick unbroken bristly dark brown fur, a long heavy snout, exactly two short curved yellow tusks, small kind eyes, a thick bare neck, standing calm and relaxed"),
    "Grizzly": ("a huge old grizzly bear", "thick brown fur, one clouded eye, huge yellowed claws, a bare neck, gentle and sleepy"),
}


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for n, (subject, look) in NEW.items():
    print("%-15s %s" % (n, subject))
if not GO:
    sys.exit("PROBELAUF")
presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
d = ps("/api/state")["decks"]
out = {c["name"]: c for c in d["outfit"]}
for n, (subject, look) in NEW.items():
    card = "kampf_" + n.lower()
    if card in out:
        out[card]["prompt"] = look
    else:
        d["outfit"].append({"name": card, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
    presets["Kampf_" + n] = sk.preset(n, "wesen", subject, [], "quer")
    sets["Kampf_%s|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
out = {c["name"]: c for c in d["outfit"]}
for n, (subject, look) in FREI.items():
    card = "kampf_" + n.lower() + "frei"
    if card in out:
        out[card]["prompt"] = look
    else:
        d["outfit"].append({"name": card, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
    presets["Kampf_%sFrei" % n] = sk.preset(n + "Frei", "wesen", subject, [], "quer")
    sets["Kampf_%sFrei|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
ps("/api/decks", d)
dc.save_json(sk.F_PRESETS, presets, "Studio")
dc.save_json(sk.F_SETS, sets, "Studio")
print("eingetragen:", ", ".join("Kampf_" + n for n in NEW))

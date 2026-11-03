# -*- coding: utf-8 -*-
r"""Volle Kampf-Saetze PirateBrawler und PirateGunner (Duc 01.11.2026, Wahl b1 + g1 auf docs/abnahme/piraten_neu.json). Gleiches Modell und gleicher Seed wie die Wahl.

    piraten_neu_satz.py [--nur brawler:hurt,gunner:guard]   -> output\expressions\_piraten_neu_satz\<brawler|gunner>\<pose>.png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt. Nichts wird ins Spiel kopiert.
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_piraten_neu as cp  # noqa: E402
import kampf_volllauf_texte as kt  # noqa: E402

ORDNER = "_piraten_neu_satz"
SEED = cp.SEEDS[0]
SAEBEL = "his only weapon exactly one curved sabre with a clean bright polished silver steel blade in his right fist, his left hand an empty fist"
SAEBEL2 = "his only weapon exactly one curved sabre with a clean bright polished silver steel blade, gripped with both hands"
LEER = "both hands empty, no weapon anywhere"
LIEGT = ("seen from the side at floor level, he lies stretched out flat on his back, resting on the floor, his body perfectly horizontal and level, arms limp at his sides, knocked out, "
         "his one head on the RIGHT side of the image, eyes closed; exactly one man with one head, the whole man fully inside the image with empty space around")
AUFGABE = "he drops to both knees and raises both open hands above his head, head bowed in defeat; the floor around him is completely clean and empty"
GETROFFEN = "hit by a heavy blow, recoiling backwards off balance, head snapped back, one hand clutching his chest where he was struck, face twisted in pain, eyes squeezed shut"
WUT = "furious and shouting with his mouth wide open and his teeth bared, leaning forward, the tendons in his neck tense"
SCHWACH = "exhausted and worn out, swaying on unsteady legs, panting heavily, barely able to stand, both legs straight"
FLUCHT = "running away in panic, looking back over his shoulder in fear"
SIEG = "triumphant victory pose, gloating, chest out, looking down to the left"
PISTOLE = cp.PISTOLE
# Pose: (Haltung, Breite, Hoehe); Haltung enthaelt die Waffe
BRAWLER = {
    "windup": ("%s, %s" % (kt.T["windup"], SAEBEL), 1232, 1232), "attack": ("%s, %s" % (kt.T["attack"], SAEBEL), 1232, 1232),
    "heavy_windup": ("%s, %s" % (kt.T["heavy_windup"], SAEBEL2), 1232, 1232), "heavy_attack": ("%s, %s" % (kt.T["heavy_attack"], SAEBEL2), 1232, 1232),
    "guard": ("in a defensive guard, body pulled back and low, the upright blade pointing straight up close to his face, shielding his face and chest from an attack from the left, %s" % SAEBEL2, 1232, 1232),
    "hurt": ("exactly two arms and two hands, hit by a heavy blow, doubled over forward, face twisted in pain, eyes squeezed shut, his left hand pressed flat on his stomach, his right arm hanging down with exactly one curved sabre with a clean bright polished silver steel blade in that fist, the blade pointing at the floor", 1232, 1232), "enraged": ("%s, %s" % (WUT, SAEBEL), 1232, 1232), "weakened": ("%s, %s" % (SCHWACH, SAEBEL), 1232, 1232),
    "defeated": ("%s, %s" % (LIEGT, LEER), 1328, 880), "surrender": ("%s, %s" % (AUFGABE, LEER), 1104, 1408), "flee": ("%s, %s" % (FLUCHT, SAEBEL), 1232, 1232), "victory": ("%s, %s" % (SIEG, SAEBEL), 1232, 1232),
}
EINE = "his only weapon %s in his right hand, his left hand empty" % PISTOLE
BEIDE = "his only weapon %s gripped with both hands" % PISTOLE
GUNNER = {
    "windup": ("taking aim, turned side-on, the right arm rising with %s, his left thumb pulling back the hammer, one eye narrowed, looking to the left" % PISTOLE, 1232, 1232),
    "attack": ("shooting to the left, the right arm stretched straight forward at shoulder height with %s, the barrel kicking slightly upward, a long step forward, hard stare, both boots completely inside the image with wide empty floor below them" % PISTOLE, 1232, 1232),
    "heavy_windup": ("taking careful aim, feet planted wide, %s, both arms raised and steady, one eye narrowed, every muscle tensed" % BEIDE, 1232, 1232),
    "heavy_attack": ("shooting to the left in a deep lunge, both arms fully stretched forward at shoulder height, %s, the barrel kicking upward, teeth bared" % BEIDE, 1232, 1232),
    "guard": ("taking a defensive stance, body pulled back and low behind his raised left forearm, the long coat swung forward as cover, %s held back near his chest, eye on the threat to the left" % PISTOLE, 1232, 1232),
    "hurt": ("%s, %s" % (GETROFFEN, EINE), 1232, 1232), "enraged": ("%s, %s, both boots completely inside the image with wide empty floor below them" % (WUT, EINE), 1232, 1232), "weakened": ("%s, %s hanging low" % (SCHWACH, EINE), 1232, 1232),
    "defeated": ("%s, %s" % (LIEGT, LEER), 1328, 880), "surrender": ("%s, %s" % (AUFGABE, LEER), 1104, 1408), "flee": ("%s, %s" % (FLUCHT, EINE), 1232, 1232), "victory": ("%s, %s raised beside his head" % (SIEG, EINE), 1232, 1232),
}
FIGUREN = {"brawler": ("b1", BRAWLER), "gunner": ("g1", GUNNER)}


def prompt(key, haltung):
    wer, _ = cp.FIGUR[key]
    kleid = cp.BRAWLER_KLEID if key[0] == "b" else cp.GUNNER_KLEID
    return "%s,\nSubject: %s, %s,\nWearing: %s,\nScene: Plain beige background,\n%s, the whole weapon inside the image." % (cp.KOPF, wer, cp.HAUT, kleid, haltung)


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for name, (key, posen) in FIGUREN.items():
        alle = dict(posen, idle=(None, 1232, 1232))
        for pose, (haltung, b, h) in alle.items():
            if nur and "%s:%s" % (name, pose) not in nur:
                continue
            p = cp.prompt(key) if pose == "idle" else prompt(key, haltung)
            c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set="%s/%s" % (ORDNER, name), st_rembg=True, st_crop=True, **cp.MODELL)
            wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1200
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cp.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)
    for w, _, dat in os.walk(os.path.join(cp.OUT, ORDNER)):
        print(w, len(dat))


if __name__ == "__main__":
    main()

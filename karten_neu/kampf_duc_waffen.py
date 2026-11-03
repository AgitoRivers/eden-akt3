# -*- coding: utf-8 -*-
r"""Duc's weapon sprites on the earth look (24.10.2026): one alias weapon per weapon class, full pose run each.
Duc: Klinge = sabre, Stumpf = black baseball bat, Messer = combat knife, Stange = boar spear (Saufeder), Fern = shotgun.
The look is read LIVE from the outfit card kampf_ducerde (Duc tunes his cards in Prompt Studio; kampf_duc.py is not
the source any more), the preset is a copy of Kampf_DucErde (LoRA strength etc.) with the name fields swapped.
Pose texts and outfit card only for the run, then reset (like kampf_duc_nachbessern.py). Old images go to _test.

    kampf_duc_waffen.py                         dry run
    kampf_duc_waffen.py setup                   cards, presets, set presets for all weapons
    kampf_duc_waffen.py lauf Bat          queue all 13 poses
    kampf_duc_waffen.py lauf Bat attack   queue single poses again
    kampf_duc_waffen.py --look Wasser setup     same for another look (Erde, Wasser, Feuer, Luft)
Afterwards (when approved): kampf_duc_spiegeln.py DucErde<Waffe> --los
"""
import copy, json, os, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ARGS = sys.argv[1:]
# --look Wasser: same weapons on another leather jacket look (24.10., Duc: all looks except cyber)
LOOK = ARGS[ARGS.index("--look") + 1] if "--look" in ARGS else "Erde"
ARGS = [a for i, a in enumerate(ARGS) if a != "--look" and (i == 0 or ARGS[i - 1] != "--look")]
sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
BASE = "Duc" + LOOK
# 23.10.: "no debris, no splashes ..." made Krea paint exactly that (CFG 1) -> describe the clean floor positively
CLEAN = " He stands on a plain smooth seamless beige studio floor."
# name: (art, short word, held phrase for the outfit card)
WAFFEN = {
    "Sword": ("einhand", "sabre", "holding one single curved steel cavalry sabre with a brass hand guard in his right "
                                   "hand"),
    # 24.10.: the word "baseball" kept adding a ball (DucWasser hurt/heavy_attack) and a batting stance
    "Bat": ("einhand", "black bat", "holding one single long matte black wooden bat with a thick rounded barrel "
                                          "and a thin handle in his right hand"),
    # 24.10.: held upright the "twenty centimeters" knife grew into a long double-edged dagger (DucCyber)
    "Knife": ("messer", "knife", "holding one single medium-sized combat knife in his right hand: a single-edged "
                                  "steel blade about one and a half times as long as his hand with a clipped point and "
                                  "a flat back, and a black grip"),   # "as long as his hand" was too small
    "Spear": ("stange", "boar spear", "holding one single boar spear in both hands: a long dark wooden shaft, a "
                                         "broad leaf-shaped steel spearhead and a short steel crossbar just below the "
                                         "spearhead"),
    "Gun": ("fern", "shotgun", "holding one single double-barrel shotgun with side-by-side steel barrels and a dark "
                                  "wooden stock in both hands, the gun kept closed with the barrels and stock forming one straight rigid line"),
    # 25.10.2026 (Duc): Maxwell's training gear, never unlockable - only Terra Scura (DucErde) in act 1
    # 25.10.: must be T-shaped (head across the handle) - in line it looked like a shower brush (Duc)
    "Mop": ("schrubber", "deck scrub brush", "holding one single T-shaped wooden deck scrubber like a push broom in both "
                                              "hands: a long plain wooden handle with a wide rectangular wooden brush "
                                              "block fixed crosswise at its end, perpendicular to the handle, a thick "
                                              "dense row of white bristles on the block"),
}
# poses shared by all weapons ({w} = short word)
RUHE = {
    # 24.10.: DucFeuer got a second sabre / second spear -> "exactly one" in idle and victory
    "idle": "in a ready fighting stance, weight low, knees bent, facing left, focused stare, the {w} held ready in his "
            "right hand, his left hand empty and clenched into a fist",
    "hurt": "hit by a heavy blow, recoiling backwards off balance, head snapped back, his left hand clutching his "
            "chest, the {w} still in his right hand, face twisted in pain",
    # 24.10.: DucCyber knife enraged/heavy_attack had the boots cut off at the bottom edge
    "enraged": "enraged and furious, baring teeth, a dark menacing aura of rage, gripping the {w} tightly, facing "
               "left, standing with both feet planted wide apart and both boots flat on the floor; seen from a distance, the figure fills only the middle two thirds of the image height, with wide empty "
               "floor below his boots",
    "weakened": "exhausted and worn out, swaying on unsteady legs, panting heavily, slumped, the {w} hanging low "
                "pointing at the floor",
    "surrender": "he drops to both knees and raises both open empty hands above his head, head bowed in defeat, {boden} "
                 "lying flat on the floor beside his knees",
    # 24.10.: the short text gave a smiling man walking left -> spell out the panic
    "flee": "running away to the left in panic, his body turned away, looking back over his right shoulder with a "
            "frightened face, eyes wide, mouth open, the {w} in his hand",
    "victory": "triumphant victory pose, gloating, chest out, the {w} raised high in his right hand, looking down to "
               "the left, his left hand an empty fist",
    "defeated": "one single man lying flat on his back on a plain smooth seamless beige studio floor, knocked out like "
                "in a cartoon, the whole body fully horizontal, both empty hands resting on his chest, eyes closed, "
                "sunglasses crooked, a calm face, his clothes clean and neat; the whole body from head to both boots is fully "
                "inside the image with empty space on both sides",
}
KAMPF = {
    "einhand": {
        # 24.10.: "held across his body" became a batting stance -> one hand at each end, horizontal like a bar
        "guard": "standing upright in a firm defensive stance, knees slightly bent, facing left, holding the {w} "
                 "horizontally with both hands, one hand at each end, raised in front of his chest like a bar to block "
                 "a blow, focused stare; the whole figure and the entire {w} are fully inside the image",
        # 24.10.: the sabre ended up hanging low behind him -> hand above the shoulder, blade up behind the head
        "windup": "winding up a strike, his right hand raised above his right shoulder, the single {w} pointing up and "
                  "back behind his head, upper body leaning back, weight on the back leg, eyes locked to the left; he "
                  "holds exactly one {w} and the entire {w} is fully inside the image",
        "attack": "striking forward to the left with full force, the {w} in his right hand fully extended forward, a "
                  "long lunging step; the whole figure and the entire {w} are fully inside the image with wide empty "
                  "space to the left of it",
        "heavy_windup": "winding up a devastating two-handed blow, the whole body twisted back and coiled, both hands "
                        "gripping the {w} raised high behind his head, teeth clenched, every muscle tensed",
        # 24.10.: the swing gave the bat a baseball -> overhead chop, the weapon is the only object
        "heavy_attack": "unleashing a devastating overhead chop, bringing the {w} down hard with both hands in front of "
                        "him to the left, the whole body swinging into it in a deep lunge, slight motion blur on the "
                        "{w}; the {w} is the only object in the image",
    },
    "messer": {
        # 24.10.: "forearm raised in front of his face" became kneeling with a hand at the ear
        "guard": "standing on both feet in a low knife-fighting stance, knees bent, facing left, his left arm bent with "
                 "the forearm held horizontally in front of his chin like a shield, the knife held low near his right "
                 "hip with the blade pointing forward, focused stare",
        # 24.10.: DucFeuer got a knife in each hand -> the left hand is spelled out as empty
        "windup": "drawing the knife in his right hand back at hip height for a fast stab, his left hand empty and "
                  "open, stretched forward to the left as a guide, body coiled, weight on the back leg, eyes locked to "
                  "the left",
        "attack": "stabbing forward to the left in a fast lunge, the knife arm fully extended, the blade pointing "
                  "straight left; the whole figure and the entire knife are fully inside the image",
        "heavy_windup": "gathering all his strength for a lightning-fast finishing strike, deep low crouch, the knife "
                        "held in a reverse grip close to his chest, eyes narrowed, every muscle tensed",
        "heavy_attack": "leaping forward to the left with a devastating slashing strike, the knife arm swept wide "
                        "across his body, deep lunge, slight motion blur on the arm and the knife; seen from a distance, the "
                        "figure fills only the middle two thirds of the image height, with wide empty floor below his "
                        "boots",
    },
    "stange": {
        "guard": "standing in a firm defensive stance, knees bent, facing left, the boar spear held diagonally across "
                 "his body in both hands with the shaft angled up to block, focused stare; the whole figure and the "
                 "entire spear are fully inside the image",
        # 24.10.: first version looked like the thrust itself -> hands pulled back to the hip, body twisted away
        "idle": "in a ready fighting stance, knees bent, facing left, holding the boar spear diagonally in both hands, "
                "the spearhead high up to the left, the butt end low behind him; the entire spear is fully inside the "
                "image",
        "windup": "drawing the boar spear back for a thrust, both hands pulled back to his right hip, elbows bent, the "
                  "spearhead close to his body pointing left, upper body twisted back, weight on the back leg, eyes "
                  "locked to the left",
        "attack": "thrusting the boar spear forward to the left with both hands, a long lunging step, the spear "
                  "horizontal; the whole figure and the entire spear including its tip are fully inside the image",
        # 24.10.: DucWasser fled with two spears -> one spear in the right hand, the left arm swinging empty
        "flee": "running away to the left in panic, his body turned away, looking back over his right shoulder with a "
                "frightened face, eyes wide, mouth open, the single boar spear held in his right hand and trailing "
                "behind him, his left arm swinging empty",
        # 24.10.: the spear on the floor got a broom-like tuft at its end (DucLuft)
        "surrender": "he drops to both knees and raises both open empty hands above his head, head bowed in defeat, the "
                     "boar spear lying flat on the floor beside his knees, a smooth bare wooden shaft ending in a plain "
                     "round wooden end",
        "heavy_windup": "raising the boar spear high above his head with both hands, the spearhead pointing down and "
                        "forward to the left, ready to drive it down, teeth clenched",
        "heavy_attack": "driving the boar spear down and forward to the left with all his weight in a deep lunge, both "
                        "arms fully extended, slight motion blur on the spearhead",
    },
    "schrubber": {   # held like a staff, comedy training weapon (Karate Kid)
        "idle": "in a ready fighting stance, knees bent, facing left, holding the deck scrub brush diagonally in both "
                "hands like a fighting staff, the brush head up to the left, a determined but slightly amused face",
        "guard": "standing in a firm defensive stance, knees bent, facing left, holding the deck scrub brush "
                 "horizontally in both hands in front of his chest like a staff to block a blow, focused stare; the "
                 "whole figure and the entire brush are fully inside the image",
        "windup": "swinging the deck scrub brush back over his right shoulder with both hands, ready for a sweeping "
                  "strike, weight on the back leg, eyes locked to the left",
        "attack": "sweeping the deck scrub brush forward to the left with both hands in a wide swing, a long lunging "
                  "step; the whole figure and the entire brush are fully inside the image",
        "heavy_windup": "raising the deck scrub brush high above his head with both hands, the brush head pointing up "
                        "and back, teeth clenched, every muscle tensed",
        # 25.10.: seen edge-on the T-head read as a shower brush -> show the wide block from the front
        "hurt": "hit by a heavy blow, recoiling backwards off balance, head snapped back, his left hand clutching his "
                "chest, the T-shaped deck scrubber still in his right hand with its wide brush block seen from the "
                "front, face twisted in pain",
        # 25.10.: the brush on the floor came out as a short hand brush -> spell out the long handle
        "surrender": "he drops to both knees and raises both open empty hands above his head, head bowed in defeat, the "
                     "long deck scrub brush lying flat on the floor beside him, its whole long wooden handle visible "
                     "next to his knees",
        "heavy_attack": "bringing the deck scrub brush down hard in front of him to the left with both hands in an "
                        "overhead slam, deep lunge, slight motion blur on the brush head; the brush is the only object "
                        "in the image",
    },
    "fern": {
        "idle": "standing in a ready stance, facing left, holding the shotgun in both hands at hip height, the barrels "
                "angled down to the left, focused stare",
        # 24.10.: first version aimed to the right with the barrels cut off
        "guard": "crouching low, facing left, holding the shotgun horizontally across his chest with both hands, one "
                 "hand on the barrels and one on the stock, the barrels pointing to the left, using the gun as a bar to "
                 "block a blow, not aiming; the entire shotgun is fully inside the image",
        "windup": "raising the shotgun to his right shoulder with both hands, taking aim to the left, cheek against the "
                  "stock, one eye narrowed",
        # 24.10.: "firing" gave a muzzle flash on DucLuft -> trigger, recoil and plain steel barrel ends
        "attack": "aiming the shouldered shotgun straight to the left with both hands, his finger squeezing the "
                  "trigger, the recoil jolting his shoulder back, the dark steel barrel ends plain and clearly visible; "
                  "the whole figure and the entire shotgun are fully inside the image",
        "heavy_windup": "kneeling on one knee, the shotgun shouldered, aiming carefully to the left, perfectly still, "
                        "one eye closed",
        # 24.10.: "firing" gave a muzzle flash (the effect layer does that) -> trigger and recoil only
        "heavy_attack": "pulling the trigger from the kneeling position, the recoil jolting his upper body back, both "
                        "hands on the gun, the barrels pointing left, the dark steel barrel ends plain and clearly "
                        "visible",
        # 24.10.: laid across the neck the gun bent around it (DucCyber) -> on one shoulder, barrels up behind him
        "victory": "triumphant victory pose, gloating, chest out, the closed shotgun resting on his right shoulder with "
                   "the barrels pointing up and back behind him, his right hand on the grip, his left hand an empty "
                   "fist, looking down to the left",
    },
}
# 24.10.: the cyber card covers "neck to feet" only -> bare hands in guard/surrender; added here, Duc's card stays as is
LOOK_EXTRA = {"Cyber": ", armored black metal gauntlets covering both hands and all fingers"}
QUER = {"defeated"}
QUADRAT = {"fern": {"guard"}, "schrubber": {"guard"}, "messer": {"enraged", "heavy_attack"}}   # knife: boots cut off in portrait (DucCyber)   # 24.10.: shotgun held across the body was cut off in portrait
OHNE_WAFFE = {"defeated", "surrender"}   # 23.10.: weapon in the lying pose -> second figure or blood pool
POSEN = ["idle", "guard", "hurt", "enraged", "weakened", "surrender", "flee", "victory", "defeated",
         "windup", "attack", "heavy_windup", "heavy_attack"]


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def texte(waffe):
    art, w, _ = WAFFEN[waffe]
    t = dict(RUHE, **KAMPF[art])
    boden = WAFFEN[waffe][2].replace("holding one single ", "one single ").split(" in his right hand")[0]         .split(" in both hands")[0]
    return {p: t[p].format(w=w, boden=boden) + ("" if p == "defeated" else "." + CLEAN) for p in POSEN}


def basis_look():
    for c in ps("/api/state")["decks"]["outfit"]:
        if c["name"] == "kampf_" + BASE.lower():
            return c["prompt"].rstrip(" ,") + LOOK_EXTRA.get(LOOK, "")
    sys.exit("Karte kampf_%s fehlt" % BASE.lower())


def setup():
    look = basis_look()
    presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
    vorlage = presets["Kampf_" + BASE]
    d = ps("/api/state")["decks"]
    cards = {c["name"]: c for c in d["outfit"]}
    for waffe, (_, _, held) in WAFFEN.items():
        n = BASE + waffe
        card, text = "kampf_" + n.lower(), look + ", " + held
        if card in cards:
            cards[card]["prompt"] = text
        else:
            d["outfit"].append({"name": card, "prompt": text, "on": True, "tag": "kampf", "sel": False,
                                "back_prompt": ""})
        p = copy.deepcopy(vorlage)
        p.update({"st_set": "combat/" + n, "sp_char": "Kampf_" + n, "sp_stchar": n,
                  "st_src": os.path.join(EXPR, n), "st_dst": os.path.join(EXPR, n), "updated": sk.JETZT})
        p["cards_on"] = dict(p.get("cards_on") or {}, outfit=[card])
        presets["Kampf_" + n] = p
        sets["Kampf_%s|Kampf" % n] = {"outfit": [card], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
        print("%-20s %s" % (n, held))
    ps("/api/decks", d)
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    dc.save_json(sk.F_SETS, sets, "Studio")


def lauf(waffe, posen):
    n, look = BASE + waffe, basis_look()
    card, t = "kampf_" + (BASE + waffe).lower(), texte(waffe)
    ordner = os.path.join(EXPR, n)
    os.makedirs(os.path.join(ordner, "_test"), exist_ok=True)
    for p in posen + ["_gespiegelt.txt"]:   # new images come unmirrored
        src = os.path.join(ordner, p if p.endswith(".txt") else p + ".png")
        if os.path.exists(src):
            i = 1
            while os.path.exists(os.path.join(ordner, "_test", "%s_v%d%s" % (os.path.splitext(os.path.basename(src))[0], i, os.path.splitext(src)[1]))):
                i += 1
            shutil.move(src, os.path.join(ordner, "_test", "%s_v%d%s" % (os.path.splitext(os.path.basename(src))[0], i, os.path.splitext(src)[1])))
    st = ps("/api/state")["decks"]
    original = {c["name"]: c["prompt"] for c in st["kampf"]}
    original_look = {c["name"]: c["prompt"] for c in st["outfit"] if c["name"] == card}
    try:
        for p in posen:
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == p:
                    c["prompt"] = t[p]
            for c in d["outfit"]:
                if c["name"] == card:
                    c["prompt"] = look if p in OHNE_WAFFE else original_look[card]
            ps("/api/decks", d)
            cmd = [sys.executable, os.path.join(HERE, "kampf_test.py"), "--karten", p, "--gegner", n]
            if p in QUER:
                cmd.insert(2, "--quer")
            elif p in QUADRAT.get(WAFFEN[waffe][0], ()):
                cmd.insert(2, "--quadrat")
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            print("eingereiht:", n, p)
    finally:
        d = ps("/api/state")["decks"]
        for c in d["kampf"]:
            if c["name"] in original:
                c["prompt"] = original[c["name"]]
        for c in d["outfit"]:
            if c["name"] in original_look:
                c["prompt"] = original_look[c["name"]]
        ps("/api/decks", d)
        print("Kartentexte zurückgesetzt")


if __name__ == "__main__":
    # stdout is already UTF-8 (set by studio_kampf_gegner on import)
    if ARGS[:1] == ["setup"]:
        setup()
    elif ARGS[:1] == ["lauf"] and len(ARGS) > 1 and ARGS[1] in WAFFEN:
        posen = ARGS[2].split(",") if len(ARGS) > 2 else POSEN
        if any(p not in POSEN for p in posen):
            sys.exit("Posen: " + ", ".join(POSEN))
        lauf(ARGS[1], posen)
    else:
        for waffe in WAFFEN:
            print("== %s%s" % (BASE, waffe))
            for p, x in texte(waffe).items():
                print("  %-13s %s" % (p, x[:110]))
        print("PROBELAUF - setup / lauf <%s> [posen]" % "|".join(WAFFEN))

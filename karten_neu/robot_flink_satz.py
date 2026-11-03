# -*- coding: utf-8 -*-
r"""Volle Kampf-Saetze der flinken Roboter: Kobra (f06) und Skorpion (f09), Duc 01.11.2026.

    robot_flink_satz.py [--nur kobra:hurt,skorpion:guard]   -> output\expressions\_robot_flink_satz\<kobra|skorpion>\<pose>.png

Laeuft ueber studio.build_graph, die Studio-Einstellungen bleiben unberuehrt. Nichts wird ins Spiel kopiert.
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_boarding_robot as cb  # noqa: E402
import casting_piraten_neu as cp  # noqa: E402
import casting_robot_flink as cf  # noqa: E402

ORDNER = "_robot_flink_satz"
SEED = cp.SEEDS[0]
AUGE = "one single round glowing red light like an eye on the side of the upper head, set far back from the snout, the snout tip and the mouth plain dark with no light"
FIGUR = {"kobra": cf.FIGUR["f06"][1].replace(cf.LICHT, AUGE), "skorpion": cf.FIGUR["f09"][1]}
assert AUGE in FIGUR["kobra"]
FERN = "the camera far back, the whole machine completely inside the image with wide empty floor around it"
RUHIG = "no glow around the body, no fire, no sparks, no motion streaks"
QUER = (1328, 880)
QUADRAT = (1232, 1232)


def s(text, licht=True):
    return "%s, %s, %s" % (text, FERN, RUHIG if licht else "no fire, no sparks, no motion streaks")


EINS = "exactly one head at the front end of the body with exactly one round red eye on it, the other end is a thin tail tip"

POSEN = {
    "kobra": {
        "idle": (s(cf.FIGUR["f06"][2] + ", facing left"), QUADRAT),
        "windup": (s(EINS + ", the neck pulled far back to the right and bent like a spring, the head low and aimed to the left, both neck blades spread, facing left"), QUADRAT),
        "attack": (s(EINS + ", striking forward to the left with full force, the head low near the floor at the far left, the neck stretched long and straight behind it, both neck blades pointing forward, the rest of the body flat on the floor behind it"), QUER),
        "heavy_windup": (s("rising as high as it can, the front body straight up, the head tilted back, both neck blades spread wide, facing left"), QUADRAT),
        "heavy_attack": (s("slamming its whole front body down and forward to the left, the head low near the floor at the far left, the back of the body whipping up behind it"), QUER),
        "guard": (s(EINS + ", curled up for protection, no neck raised at all, the head lying low on top of the spiral in its middle, both neck blades folded flat against the head, facing left"), QUADRAT),
        "hurt": (s(EINS + ", hit by a heavy blow and falling far over backwards, the whole upper body and neck thrown back to the right in a big arc, the head far to the right behind the body with its face turned up, the lower body sliding forward to the left"), QUADRAT),
        "enraged": (s("raised high and leaning forward aggressively, both neck blades spread wide, the red light burning bright, facing left", False), QUADRAT),
        "weakened": (s("damaged and sagging, the raised neck drooping, the head hanging low toward the floor, the neck blades hanging limp, the red light dim, facing left"), QUADRAT),
        "defeated": (s("exactly one head at the right end of the body, the other end is a thin tail tip, the whole body lies low on the floor in one loose flat curve, nothing raised, the one head rests flat on the floor on the right side of the image, the neck blades limp, the light dark and off; exactly one machine"), QUER),
        "surrender": (s(EINS + ", the whole body lies low on the floor in one loose flat curve, nothing raised, the one head at the left end rests flat on the floor, the neck blades folded down, the floor around it completely clean and empty"), QUER),
        "flee": (s("slithering away fast along the floor in low waves, the body close to the ground, the head low and glancing back over the body, moving to the left"), QUER),
        "victory": (s("standing tall and straight as high as it can, proud, both neck blades spread wide, the head held high, facing left"), QUADRAT),
    },
    "skorpion": {
        "idle": (s(cf.FIGUR["f09"][2] + ", facing left"), QUADRAT),
        "windup": (s("the body pressed low, the tail arched far back to the right, both pincers pulled back close to the body, about to strike, facing left"), QUADRAT),
        "attack": (s("stabbing forward to the left, the long tail bent all the way forward over its back so that the tail blade hangs in front of the head and points to the left, both pincers open, facing left"), QUER),
        "heavy_windup": (s("the front of the body raised high on the back legs, both pincers lifted high and wide open, the tail arched high over the body, facing left"), QUADRAT),
        "heavy_attack": (s("a deep lunge to the left, the body tilted steeply down at the front with the back high in the air, both pincers closed and pushed far forward, the tail bent forward over the body with its blade driving down into the floor in front of the head, facing left"), QUER),
        "guard": (s("in a defensive stance, the body pressed flat to the floor, both big pincers pulled up directly in front of the red light so that they cover it like a shield with their tips touching, the tail curled tight over its back, facing left"), QUADRAT),
        "hurt": (s("exactly one tail and exactly six legs, hit by a heavy blow and rearing up, the body tilted steeply with the front high in the air and only the back legs on the floor, the front legs kicking in the air, both pincers flung wide apart, the one tail thrown back, facing left"), QUADRAT),
        "enraged": (s("reared up aggressively, both pincers raised and wide open, the tail high and shaking, the red light burning bright, facing left", False), QUADRAT),
        "weakened": (s("damaged and sagging, the body sunk down onto the floor, the legs bent, both pincers resting on the floor, the tail drooping low, the red light dim, facing left"), QUADRAT),
        "defeated": (s("seen from the side at floor level, the machine is flipped upside down, it lies on its back with its belly up, all six legs pointing up to the ceiling and curled in, the pincers limp on the floor, exactly one tail: it lies limp and flat on the floor straight out to the right, no tail above the body, the red light off; exactly one machine"), QUER),
        "surrender": (s("exactly one tail and exactly six legs, the body lies flat on the floor with all legs folded, both pincers open and laid flat forward on the floor, the one tail hanging limp in a low small curve just behind the body with its blade pointing down, the floor around it completely clean and empty, facing left"), QUER),
        "flee": (s("exactly one tail and exactly six legs, running away at full speed on its thin legs in a long stride, the body low, the one tail curved over its back and bent backwards, the pincers pulled in close, moving to the left"), QUER),
        "victory": (s("the front of the body raised high, both pincers raised high in triumph, the tail standing tall, facing left"), QUADRAT),
    },
}


# Die Figur-Beschreibung schlaegt die Pose: "aufgerichtet" und "Schwanz ueber dem Ruecken" kommen sonst immer mit
ANDERS = {
    ("kobra", "guard"): ("raised in an S-curve like a cobra", "rolled up flat in a tight round spiral on the floor like a coiled garden hose, seen from slightly above"),
    ("skorpion", "defeated"): ("a long curved segmented tail with one blade raised over its back", "one long straight segmented tail with one blade at its end, lying flat on the floor"),
}


def prompt(name, haltung, pose=""):
    wer = FIGUR[name]
    if (name, pose) in ANDERS:
        alt, neu = ANDERS[(name, pose)]
        assert alt in wer
        wer = wer.replace(alt, neu)
    return "%s,\nSubject: %s,\nFeatures: %s,\nScene: Plain beige background,\n%s." % (cb.KOPF, wer, cb.GLATT, haltung)


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    seeds = cp.SEEDS[:2] if "--zwei" in sys.argv else [SEED]  # zweiter Seed landet als <pose>-1.png
    wart = []
    for name, posen in POSEN.items():
        for pose, (haltung, (b, h)) in posen.items():
            if nur and "%s:%s" % (name, pose) not in nur:
                continue
            c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set="%s/%s" % (ORDNER, name), st_rembg=True, st_crop=True, **cp.MODELL)
            for seed in seeds:
                wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(name, haltung, pose), pose, seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1500
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cp.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()

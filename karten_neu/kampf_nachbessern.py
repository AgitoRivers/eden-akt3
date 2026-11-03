# -*- coding: utf-8 -*-
r"""Fixes from Duc's approval of the combat run (22.10.2026), done per Krea-Edit from the idle pose (kampf_edit.py).
- defeated for ALL human enemies: really lying flat on the back, eyes closed, only one person (the text2img run
  produced sitting figures and a second, lying double). Maxwell is the exception: like Chuck Norris he never goes
  down - he kneels, exhausted.
- single poses Duc marked "Neu" (Yasin, Maxwell, Alon).
Uses kampf_edit.GEGNER, but corrects the outdated looks (Alon's cyber armor, Maxwell's polo, Yasin's big drone) and
adds the human alphas. kampf_edit.py itself stays untouched.

    kampf_nachbessern.py <Name> --posen defeated,attack      queue these poses (Prompt Studio 8301 + ComfyUI 8189)
    kampf_nachbessern.py --menschen                          names of all human enemies
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kampf_edit as KE          # noqa: E402
from kampf_alphas import ALPHAS, FACES, ZOO_COLLAR   # noqa: E402
ZOO_WER = {"Lion": "male lion with a huge golden mane", "LionAlpha": "huge melanistic black lion with a black mane",
           "Ape": "large ape wearing a black captain's cap", "ApeAlpha": "huge silverback ape wearing a black pirate "
           "tricorn hat", "Wolf": "grey wolf", "WolfAlpha": "huge dark grey wolf", "Panther": "black panther",
           "PantherAlpha": "huge black panther with scars", "Grizzly": "brown grizzly bear",
           "GrizzlyAlpha": "huge old grizzly bear with a scarred face"}
VIERBEINER = {"Lion", "LionAlpha", "Wolf", "WolfAlpha", "Panther", "PantherAlpha", "Grizzly", "GrizzlyAlpha",
              "Kevin"}   # Kevin: lying bird, landscape without rotation

LIE = ("{p} lies unconscious flat on {pos} back on the floor, the whole body horizontal and stretched out along the "
       "ground, the head resting on the floor, eyes fully closed, the face slack and calm, arms limp beside the body, "
       "knocked out cold, the head on the RIGHT side of the image and the feet on the left; a wide shot from far away, the figure is small in the frame and seen from the side, the "
       "whole body from the head to both shoes fully inside the image "
       "with clear empty space on both sides, and there is only this ONE person in the image, nobody standing, "
       "sitting or kneeling; the floor around the figure is perfectly clean and plain")
KNEEL = ("he has gone down on one knee, utterly exhausted, one fist planted on the floor, head lowered, chest heaving, "
         "sweat running down his face, but still not lying down - a beaten champion catching his breath")
SERIOUS = " His face is serious and tense, no smile, no grin, no laughing."

G = KE.GEGNER
G["YasinDrone"].update({
    "wer": "athletic 29-year-old Arab man with a short black skin-fade haircut and a neatly trimmed black beard, an open "
           "white linen shirt over a bare chest, a thin gold chain, beige linen shorts, white sneakers, a heavy gold "
           "watch, holding a drone remote controller, with ONE large matte black quadcopter drone close to him",
    "waffe": "He has NO gun and NO weapon - his only tool is the drone remote controller; there is exactly ONE drone "
             "and it stays fully inside the image. "})
G["YasinDrone"]["posen"].update({
    "windup": "he pulls the controller close to his chest with both thumbs on the sticks, eyes narrowed, and the drone "
              "rises high above his head tilting forward, ready to dive",
    "attack": "he thrusts the controller forward with both hands and the drone dives fast toward the viewer's left in "
              "front of him, his hands hold only the controller",
    "flee": "he turns his body to the right and sprints away to the right, seen from the side, looking back over his "
            "shoulder in fear, clutching the controller, the drone wobbling behind him",
    "weakened": "he staggers exhausted, barely holding the controller, and the damaged drone sputters low beside him "
                "with smoke and a few small electric sparks coming out of one broken propeller arm",
    "surrender": "he kneels on both knees with both EMPTY hands raised high above his head, palms open, his hands hold "
                 "nothing; the controller lies on the floor in front of his knees and the drone lies crashed and "
                 "broken on the floor beside it, propellers snapped off; no drone in the air",
    "defeated": LIE.format(p="he", pos="his") + ", the controller dropped beside his hand, the drone lying broken on "
                "the floor next to him; no drone in the air"})
LICHT_POSE = {("YasinDrone", "weakened"): "Only a few small sparks from the broken drone; no other glow, no fire."}
# poses where the figure has dropped its weapon / tool: the normal "he holds ..." sentence would contradict them
WAFFE_POSE = {("YasinDrone", "surrender"): "There is exactly ONE drone, lying broken on the floor - it no longer flies. ",
              ("YasinDrone", "defeated"): "Remove the drone that flies in the air in the reference: there is exactly ONE "
                                          "drone, lying broken on the floor - nothing flies. ",
              ("Alon", "surrender"): "The ray gun lies on the floor; his hands are empty. The jetpack is switched OFF. ",
              ("Alon", "defeated"): "The ray gun lies on the floor; his hands are empty. The jetpack is switched OFF. "}

G["MaxwellSteward"].update({
    "wer": "very muscular dark-skinned bald bodybuilder in a tight white short-sleeved polo shirt with a folded-down "
           "collar, a small golden anchor logo and a black name badge, navy shorts, white deck sneakers and orange "
           "mirrored wraparound sport sunglasses",
    "waffe": "He fights only with his bare fists; his hands hold nothing. "})
for m in ("MaxwellSteward", "MaxwellSports", "MaxwellMaximum"):
    G[m]["posen"]["defeated"] = KNEEL
    # the plain FAUST text came out as a double-biceps flex
    G[m]["posen"]["heavy_windup"] = ("he clasps both fists together into one double fist and raises it high above "
                                     "his head like a sledgehammer, body twisted, about to smash down; he keeps "
                                     "exactly the same outfit as in the reference")

G["Alon"].update({
    "wer": "smug tech billionaire in his fifties with a short buzz cut, aviator sunglasses, a glossy piano-black cyber "
           "armor torso shell with sculpted chest plates and segmented shoulder guards, dark jeans, white sneakers and "
           "a chunky chrome jetpack on his back",
    "waffe": "He holds ONE sleek white-and-black futuristic ray gun in his RIGHT hand (on the viewer's left); no beam, "
             "no muzzle flash. The jetpack is switched OFF, no flames. "})
G["Alon"]["posen"].update({
    "windup": "he crouches and pulls the ray gun in his right hand back close to his chest, left hand forward for "
              "balance, eyes locked toward the viewer's left, about to fire",
    "weakened": "he sags forward exhausted, knees bent, his left hand braced on his knee, the ray gun hanging loosely "
                "from his right hand, head low, breathing hard, the armor scratched." + SERIOUS,
    "surrender": "he kneels on both knees with both EMPTY hands raised high above his head, palms open, his hands hold "
                 "nothing; the ray gun lies on the floor in front of his knees; his head is bowed." + SERIOUS,
    "defeated": LIE.format(p="he", pos="his") + ", the ray gun lying beside his hand"})

# Kevin, the cockatoo mascot and nemesis (Duc 23.10.2026): all poses as edits of the approved test image; comic, never
# gory - he is knocked out, never dead (no death pose)
KEVIN_GANZ = ("; the whole bird with crest, tail and both feet fully inside the image, wide empty space around it, the "
              "same pink crest and pink cheek blush as in the reference")
G["Kevin"] = {"wer": "cheeky white cockatoo with a pink crest and pink blush on its cheeks", "waffe": "", "posen": {
    k: v + KEVIN_GANZ for k, v in {
        "idle": "it stands cheekily on the ground, head tilted, crest raised, looking to the left",
        "guard": "it crouches and hides its face behind one spread wing, peeking out over the feathers",
        "hurt": "it recoils with ruffled feathers, beak open in an indignant squawk, a few loose white feathers in the air",
        "enraged": "it screeches with its crest fully raised and both wings spread wide, puffed up to look big",
        "weakened": "it sags tiredly, crest drooping flat, feathers ruffled, eyes half closed",
        # 23.10.: "like hands" gave claws at the wing tips (double claws) - wings are feathers only now
        "surrender": "it lifts both feathered wings up and open above its body in surrender, the wing tips are only "
                     "white feathers, it stands on its two feet on the ground with exactly two feet, crest flat, a "
                     "sheepish look",
        "flee": "it flaps away to the right in a panic, looking back over its shoulder, crest flattened",
        "victory": "it struts proudly with its crest high and wings half open, beak open in a triumphant squawk",
        "windup": "it crouches low with wings half raised and beak closed, ready to dive to the left",
        "attack": "it lunges forward to the left and pecks, beak wide open",
        "heavy_windup": "it rises up with both wings raised high above its body, crest spiked up, ready to dive",
        "heavy_attack": "it dives forward to the left with feet and talons stretched out and wings swept back",
        "defeated": "it lies knocked out on its back, both feet sticking up in the air, eyes closed, crest flopped to one "
                    "side, a couple of loose white feathers beside it, comic and harmless",
    }.items()}}

GANZ = "his whole body from head to shoes is fully visible inside the image with empty space around it"
# Casanova: the rose kept coming out with a bloom on BOTH ends of the stem (Duc 22.10.: "oft doppel Rose")
ROSE = ("exactly ONE single red rose held crosswise between his teeth: ONE bloom only, on the viewer's left of his "
        "mouth, the other end is just a short bare green stem without any flower")
G["DrunkCasanova"]["wer"] = ("drunk Casanova with slicked dark hair, flushed cheeks and a few small pink lipstick kiss "
                             "prints on one cheek (lipstick, not blood, no wounds), in a dark red velvet blazer, black "
                             "shirt and black trousers, " + ROSE + "; the wine bottle is closed and nothing drips or "
                             "spills")
G["DrunkCasanova"]["posen"]["idle"] = ("he stands in a loose, swaying drunken fighting stance, the bottle in his right "
                                       "hand, his left fist raised; " + ROSE + "; the floor around him is perfectly clean "
                                       "and plain")
G["DrunkCasanova"]["posen"].update({k: v + "; " + GANZ for k, v in {   # rose only in "wer": in every pose text it zoomed in
    "enraged": "he bellows drunkenly, face twisted with anger, the bottle raised threateningly in his right hand, left "
               "fist clenched",
    "guard": "he hunches behind his raised left forearm, the bottle held low and ready in his right hand, swaying",
    "heavy_windup": "he lifts the bottle in his right hand high above his head with a wild drunken swing, left fist "
                    "raised, body twisted back",
    "hurt": "he reels backward from a hit, his left hand clutching his chest, the bottle flung out to the side in his "
            "right hand, face grimacing",
    "victory": "he grins smugly and raises the bottle in his right hand like a trophy, his left fist pumped",
    "flee": "he stumbles away to the right in a drunken run, looking back over his shoulder in panic, the bottle "
            "clutched in his right hand",
    "windup": "staggering, he lifts the bottle in his right hand high up and far back behind his head, arm bent, "
              "leaning back",
    "attack": "he smashes the bottle in his right hand forward and down toward the viewer's left like a club, arm "
              "fully extended in front of his body, lunging forward",
}.items()})

# human alphas: own face + base enemy's weapon (kampf_alphas: different people, own outfit card)
WAFFE_ALPHA = {"PirateAlpha": "He holds only ONE long curved cutlass, always in his RIGHT hand (on the viewer's left). ",
               "ThiefAlpha": "He holds only ONE short steel crowbar, always in his RIGHT hand (on the viewer's left). ",
               "BruteAlpha": "A heavy iron chain is wrapped around his RIGHT fist; the whole chain stays inside the image. ",
               "AgentAlpha": "His black-gloved hands are empty; no gun, no weapon. "}
for a, (base, gruppe, look) in ALPHAS.items():
    if gruppe == "mensch":
        G[a] = {"wer": FACES[a][0] + ", wearing " + look, "waffe": WAFFE_ALPHA[a], "posen": {}}

# defeated for every human enemy (Maxwell kneels, see above)
SIE = {"Vampire": ("she", "her"), "Alien": ("it", "its")}
MENSCHEN = ["Agent", "AgentAlpha", "Alien", "Alon", "Brute", "BruteAlpha", "DrunkCasanova", "Heinrich",
            "MaxwellMaximum", "MaxwellSports", "MaxwellSteward", "Mime", "Paparazzo", "Pirate", "PirateAlpha",
            "PirateTorch", "Thief", "ThiefAlpha", "ThiefArab", "Vampire", "YasinDrone"]
for m in MENSCHEN:
    if m.startswith("Maxwell") or m in ("YasinDrone", "Alon"):
        continue
    p, pos = SIE.get(m, ("he", "his"))
    G[m]["posen"]["defeated"] = LIE.format(p=p, pos=pos)

# ---- Duc 22.10.2026 evening: second check of all human sprites -------------------------------------------------
CLEAN = "; the clothes are clean and the air around the figure is empty"
# guard = a real protective pose for humans (crossed forearms, ducking, taking cover) - each in character
DECKUNG = ("{p} takes cover: crouching low, both forearms crossed in front of {pos} face and chest to block an incoming "
           "blow, chin tucked, shoulders hunched, eyes peeking out between the forearms; whatever {p} holds stays "
           "pressed flat against {pos} forearm")
GUARD = {m: DECKUNG for m in MENSCHEN}
GUARD.update({
    "YasinDrone": "he ducks low behind his raised forearm, and the drone hovers right in front of him like a shield",
    "Mime": "he crouches and presses both white-gloved palms flat against an invisible wall in front of him, "
            "shielding himself behind it, hands empty",
    "Paparazzo": "he crouches and holds the big camera up in front of his face with both hands like a shield",
    "Heinrich": "he ducks and shields his face with his raised right forearm, holding the champagne glass safely "
                "away from his body in his left hand",
    "Vampire": "she crouches and sweeps her long cape up in front of her face and body with one raised arm, peeking "
               "over its edge, the dagger held low",
    "MaxwellMaximum": "he takes a tight boxer's peek-a-boo guard: both fists raised in front of his face, elbows "
                      "pressed to his ribs, chin tucked, knees bent",
})
GUARD["MaxwellSports"] = GUARD["MaxwellSteward"] = GUARD["MaxwellMaximum"]
# second try for the four that still aimed / took photos / stood upright (22.10.)
GUARD.update({
    "Alon": "he crouches low behind his left forearm raised across his face, the ray gun pulled back tight against his "
            "chest pointing straight up, not aiming, shoulders hunched, bracing for a blow",
    "Alien": "it crouches low behind its left forearm raised across its face, the ray gun pulled back tight against "
             "its chest pointing straight up, not aiming, bracing for a blow",
    "YasinDrone": "he crouches low with both forearms crossed in front of his face, the controller in one hand, and "
                  "the drone hovers directly in front of his face between him and the viewer like a shield",
    "Paparazzo": "he crouches low and hides his face behind the big camera held up in front of it with both hands, "
                 "the lens pointing down at the floor, shoulders hunched, bracing for a blow",
})
SCHMERZ = ("{p} is hit hard and recoils backward, bent forward at the waist, one hand pressed against {pos} ribs, face "
           "twisted in pain, the other hand holding {pos} weapon loosely, pointing down and away from {pos} body" + CLEAN)
HURT = {m: SCHMERZ.format(p="he", pos="his") for m in ("Agent", "Thief", "ThiefAlpha", "Pirate", "PirateAlpha",
                                                     "BruteAlpha", "YasinDrone")}
HURT["Alon"] = SCHMERZ.format(p="he", pos="his") + "." + SERIOUS
HURT["YasinDrone"] = ("he is hit and doubles over in pain, one hand clutching his stomach, the controller in the other "
                      "hand, the drone wobbling beside him" + CLEAN)
HAMMER = ("he clasps both fists together into one double fist and raises it high above his head like a sledgehammer, "
          "body twisted, about to smash down; he keeps exactly the same outfit as in the reference")
HEAVY_WINDUP = {"MaxwellMaximum": HAMMER, "MaxwellSports": HAMMER, "AgentAlpha": HAMMER,
                "Mime": HAMMER + ", his white-gloved hands empty",
                "Heinrich": "he leans far back and cocks his right fist high above his head, the whole body coiled to "
                            "the side, ready to hammer it down; the champagne glass held low in his left hand",
                "Alon": "he grips the ray gun with both hands and lifts it high above his head, ready to swing it down "
                        "like a club, body coiled." + SERIOUS}
ATTACK = {"Thief": KE.GEGNER["Thief"]["posen"]["attack"], "ThiefArab": KE.GEGNER["ThiefArab"]["posen"]["attack"],
          "ThiefAlpha": "he swings the single crowbar in his right hand forward toward the viewer's left, arm fully "
                        "extended, lunging forward; his left hand is an empty fist",
          "AgentAlpha": KE.FAUST["attack"]}
WINDUP = {"PirateTorch": KE.GEGNER["PirateTorch"]["posen"]["windup"] + "; there is only ONE torch",
          "AgentAlpha": KE.FAUST["windup"]}
# surrender: kneeling, hands up, weapon dropped (many only crouched, still armed; the paparazzo kept shooting photos)
AUFGABE = ("{p} kneels on both knees and raises both EMPTY open hands high above {pos} head, palms forward, head "
           "bowed in defeat; everything {p} carried lies on the floor in front of {pos} knees")
SURRENDER = {m: AUFGABE for m in ("Agent", "AgentAlpha", "Brute", "BruteAlpha", "DrunkCasanova", "Heinrich",
                                  "MaxwellMaximum", "MaxwellSports", "MaxwellSteward", "Paparazzo", "Pirate",
                                  "PirateAlpha", "PirateTorch", "ThiefArab", "Vampire")}
# zoo animals: lying defeated/death (one animal only), Ape hurt keeps the black cap
TIER_LIEGT = ("it lies collapsed flat on its side on the ground, legs limp and stretched out, the head resting on the "
              "floor on the RIGHT side of the image, eyes closed, {wie}; the whole animal fully inside the image with "
              "empty space around it, and there is only this ONE animal in the image; the floor is clean and plain")
for z, wer in ZOO_WER.items():
    G.setdefault(z, {"wer": wer + ", wearing " + ZOO_COLLAR, "waffe": "", "posen": {}})
    G[z]["posen"]["defeated"] = TIER_LIEGT.format(wie="knocked out")
    G[z]["posen"]["death"] = TIER_LIEGT.format(wie="dead and motionless, peaceful")
# Duc 22.10.: many zoo poses from the text2img run were cut off (paws, tails, ape feet) - every pose is now an edit of
# the full-body test image, and each text ends with the full-body sentence
GANZ_TIER = ("; the whole animal from head to tail with all paws fully inside the image, wide empty space around it, "
             "the same camera distance as in the reference")
TIER_POSEN = {
    "idle": "it stands in a tense, hostile fighting stance, snarling, ready to attack",
    "guard": "it crouches low and defensive, head lowered between its shoulders, body pulled back, ready to dodge",
    "hurt": "it flinches back from a hit, head jerked aside, one front paw lifted off the ground, snarling in pain",
    "enraged": "it roars with jaws wide open, hackles raised, the whole body tensed and leaning forward",
    "weakened": "it staggers exhausted, head hanging low, panting, legs trembling",
    "surrender": "it cowers low to the ground, ears flat, tail tucked, head turned away submissively",
    "flee": "it turns and runs away to the right, looking back over its shoulder",
    "victory": "it stands tall and roars triumphantly with its head raised high",
    "windup": "it crouches low and tense, head pulled back, jaws firmly closed, ready to pounce to the left",
    "attack": "it lunges forward to the left, head thrust far forward, jaws wide open biting",
    "heavy_windup": "it rears up on its hind legs gathering all its strength, body coiled, jaws closed",
    "heavy_attack": "it launches a devastating leap forward to the left, the whole body stretched out in the air, jaws "
                    "open",
}
AFFE_POSEN = dict(TIER_POSEN, **{
    "idle": "it stands hunched in a hostile fighting stance, long arms hanging, fists on the ground, snarling",
    "guard": "it crouches and raises both long arms crossed in front of its face, peeking out between them",
    "hurt": "it is hit and recoils backward, one hand pressed to its chest, snarling in pain",
    "surrender": "it cowers low, both hands raised over its head, looking away submissively",
    "flee": "it turns and runs away to the right on all fours, looking back over its shoulder",
    "victory": "it stands upright and beats its chest with both fists, roaring triumphantly",
    "windup": "it rears back and raises one huge fist high, snarling",
    "attack": "it lunges forward to the left and swings a huge fist, arm fully extended",
    "heavy_windup": "it raises both huge fists high above its head, ready to smash down",
    "heavy_attack": "it smashes both fists down and forward to the left with all its weight",
})
for z in ZOO_WER:
    for pose, text in (AFFE_POSEN if z.startswith("Ape") else TIER_POSEN).items():
        G[z]["posen"][pose] = text + GANZ_TIER
for hut, z in (("black captain's cap", "Ape"), ("black pirate tricorn hat", "ApeAlpha")):
    for pose in AFFE_POSEN:
        G[z]["posen"][pose] += "; the %s stays exactly as in the reference" % hut
NACHCHECK = {"guard": GUARD, "hurt": HURT, "heavy_windup": HEAVY_WINDUP, "attack": ATTACK, "windup": WINDUP,
             "surrender": SURRENDER}
for pose, texte in NACHCHECK.items():
    for m, text in texte.items():
        p, pos = SIE.get(m, ("he", "his"))
        G[m]["posen"][pose] = text.format(p=p, pos=pos) if "{p" in text else text
        if pose == "surrender":    # the "he holds ..." sentence would contradict the dropped weapon
            WAFFE_POSE[(m, pose)] = "%s hands are empty; %s weapon lies on the floor. " % (pos.capitalize(), pos)
        elif pose == "guard" and m in ("YasinDrone",):
            WAFFE_POSE[(m, pose)] = "There is exactly ONE drone, hovering right in front of him. "
# unarmed fighters got invented props on the floor (bowling ball, racket, flowers), the vampire a blood stain
for m in ("MaxwellSports", "MaxwellSteward"):
    G[m]["posen"]["surrender"] = ("he drops to both knees and raises both open hands above his head, head bowed in "
                                  "defeat; the floor around him is completely clean and empty")
    WAFFE_POSE[(m, "surrender")] = "His hands are empty. "
G["Vampire"]["posen"]["surrender"] = AUFGABE.format(p="she", pos="her") + "; the floor is clean, only the dagger lies there"
# Duc 22.10. evening: the crowbar kept floating in the thieves' guard pose - guard without the crowbar
for m in ("Thief", "ThiefArab"):
    G[m]["posen"]["guard"] = ("he takes cover: crouching low, both forearms crossed in front of his face and chest to "
                              "block an incoming blow, chin tucked, shoulders hunched, both hands empty open hands")
    WAFFE_POSE[(m, "guard")] = "Both of his hands are empty. "
# --weit: cut-off sprites from the approval get a wider framing (more empty space on all sides)
WEIT = (", seen from further away so the figure is smaller in the frame, with wide empty space on all four sides; "
        "nothing touches the edges of the image")
# second try (22.10.): crouching guards and the agent's punch still cut the legs off at the bottom
FUESSE = ("; the whole body from the top of the head down to both shoes standing on the floor is fully visible, "
          "the shoes clearly inside the image above the bottom edge")


if __name__ == "__main__":
    if "--menschen" in sys.argv:
        print(",".join(MENSCHEN))
        sys.exit()
    name = sys.argv[1]
    posen = sys.argv[sys.argv.index("--posen") + 1].split(",") if "--posen" in sys.argv else []
    if "--weit" in sys.argv:
        for k in posen:
            G[name]["posen"][k] = G[name]["posen"][k] + WEIT
    if "--fuesse" in sys.argv:
        for k in posen:
            G[name]["posen"][k] = G[name]["posen"][k] + FUESSE
    if "--wie-vorlage" in sys.argv:
        # a finished pose of ANOTHER figure (e.g. the alpha) as reference: keep its pose and framing, swap the person
        # (22.10.: Brute's guard kept zooming in; BruteAlpha's guard was fine)
        for k in posen:
            G[name]["posen"][k] = ("exactly the same pose, the same framing and the same camera distance as in the "
                                   "reference, with the whole body down to the shoes inside the image; change only the "
                                   "person's face, hair, tattoos and clothes to match the description")
    for k in posen:
        if (name, k) in LICHT_POSE or (name, k) in WAFFE_POSE:
            if len(posen) > 1:
                sys.exit("%s/%s braucht eigenes Licht/Requisit - bitte einzeln aufrufen" % (name, k))
            G[name]["licht"] = LICHT_POSE.get((name, k), G[name].get("licht", KE.LICHT))
            G[name]["waffe"] = WAFFE_POSE.get((name, k), G[name]["waffe"])
    if (name, posen) == ("DrunkCasanova", ["defeated"]):
        # his detailed face/rose description made every lying edit zoom in on the face (legs cut off, 5 tries)
        G[name]["wer"] = "drunk man in a dark red velvet blazer, black shirt, black trousers and brown shoes"
        G[name]["waffe"] = "A single red rose with one bloom lies on the floor beside him and a corked wine bottle beside his hand. "
    # kampf_edit writes ONE reference file per figure (kampf_ref\<Name>_idle_rand.png) and ComfyUI only reads it when
    # the job runs - a second call for the same figure would overwrite the reference of jobs still waiting. So wait
    # until ComfyUI is idle before writing a new reference (22.10.: Casanova poses came out from the wrong reference).
    import json, time, urllib.request
    while True:
        try:
            q = json.loads(urllib.request.urlopen("http://127.0.0.1:8189/queue", timeout=5).read())
        except Exception:
            sys.exit("ComfyUI (8189) antwortet nicht")
        if not q["queue_running"] and not q["queue_pending"]:
            break
        time.sleep(5)
    tmp = None
    if "--nur-rose" in sys.argv:
        # Casanova: new poses from a fresh idle kept zooming in, so the old full-body pose is its own reference and
        # only the rose changes (kampf_edit then keeps pose, framing and camera distance). One pose per call.
        if len(posen) != 1:
            sys.exit("--nur-rose: genau eine Pose je Aufruf")
        G[name]["posen"][posen[0]] = ("exactly the same pose, the same framing and the same camera distance as in the "
                                      "reference, change nothing except the rose: " + ROSE)
        if posen[0] == "defeated":
            KE.W, KE.H = 1328, 1024
        sys.argv += ["--quelle", posen[0]]
    elif "--halsband" in sys.argv:
        # Alon's zoo animals (Lion, Ape + Alphas): the finished pose gets the shared silver collar, nothing else changes
        if len(posen) != 1:
            sys.exit("--halsband: genau eine Pose je Aufruf")
        G.setdefault(name, {"wer": ZOO_WER[name], "waffe": "", "posen": {}})
        G[name]["posen"][posen[0]] = ("exactly the same pose, the same framing and the same camera distance as in the "
                                      "reference, change nothing except adding " + ZOO_COLLAR)
        src = os.path.join(KE.OUT, "expressions", "combat", name, posen[0] + ".png")
        from PIL import Image
        with Image.open(src) as im:
            if im.width > im.height:
                KE.W, KE.H = 1328, 1024
        sys.argv += ["--quelle", posen[0]]
    elif posen in (["defeated"], ["death"]) and name in VIERBEINER:
        # four-legged zoo animals are already horizontal: landscape canvas, no rotation (22.10.: text2img gave standing
        # animals and sometimes a second, dead copy beside them)
        KE.W, KE.H = 1328, 1024
    elif posen in (["defeated"], ["death"]) and not name.startswith("Maxwell"):
        # Lying figures: landscape canvas, and the reference is the idle cutout turned 90 degrees (head right, Duc 22.10.). Krea-Edit
        # keeps the reference's composition, so the figure is already horizontal and fully inside the image - with the
        # upright reference it zoomed in and cut off the feet, and a flying drone stayed in the air.
        KE.W, KE.H = 1328, 1024
        from PIL import Image
        d = os.path.join(KE.OUT, "expressions", "combat", name)
        src = sys.argv[sys.argv.index("--vorlage") + 1] if "--vorlage" in sys.argv else "idle"   # full-body pose
        im = Image.open(os.path.join(d, src + ".png")).convert("RGBA")
        im = im.crop(im.getchannel("A").point(lambda a: 255 if a > 128 else 0).getbbox()).rotate(-90, expand=True)   # head right (Duc 22.10.)
        tmp = os.path.join(d, "_liegend_ref.png")
        im.save(tmp)
        sys.argv += ["--quelle", "_liegend_ref"]
    # ComfyUI caches the reference loader by its file path: with kampf_edit's fixed name
    # kampf_ref\<Name>_idle_rand.png a NEW reference was ignored and the cached old one used (22.10.: Casanova's
    # poses came from a stale, rotated reference). Give every call its own reference file name.
    _join = os.path.join
    stamp = time.strftime("%H%M%S")

    def join_unique(*parts):
        p = _join(*parts)
        return p[:-len("_idle_rand.png")] + "_ref_" + stamp + ".png" if p.endswith("_idle_rand.png") else p
    os.path.join = join_unique
    try:
        KE.main()
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)           # only needed while queueing: kampf_edit copies it to kampf_ref\<Name>_idle_rand.png

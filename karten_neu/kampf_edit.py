# -*- coding: utf-8 -*-
r"""Kampf-Posen per Krea-Edit aus dem idle-Bild (19.10.2026, nach dem Thief-Test: ohne ref_boost, Waffe/Hand genau
benannt, Referenz mit viel Rand -> nichts liegt am Bildrand). Allgemeine Fassung von kampf_edit_test.py.

  kampf_edit.py <Name>                    alle in GEGNER[<Name>]["posen"] eingetragenen Posen
  kampf_edit.py <Name> --posen a,b        nur diese Posen
  kampf_edit.py <Name> --liste            nur anzeigen
  kampf_edit.py <Name> --quelle windup    andere Vorlage statt idle (Bat: Fluegel angelegt)

Nur Auftraege in die ComfyUI-Warteschlange (ueber Prompt Studio, Port 8301); das Erzeugen laeuft in ComfyUI.
Alte Posen wandern vorher nach output\_expressions_papierkorb\combat\<Name>\<Zeit>. Prompt-Studio-Einstellungen,
Kartentexte und Sprite-Prompt werden danach zurueckgesetzt. Kein Leuchten/Feuer/Blitz (macht die Effektschicht).
"""
import io, json, os, shutil, sys, time, urllib.request
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
W, H = 1024, 1328

EDIT = ("Edit this photo. Keep exactly the same {wer} with the same face, body, outfit and colors as in the reference. "
        "{waffe}Keep the same plain light background, the same lighting and the same camera distance; the whole figure "
        "stays fully visible and centered with wide empty space around it, and nothing touches the image edges. "
        "There is only ONE single figure in the image, no second person or animal. {licht} New pose: {pose}.")
LICHT = "No glow, no fire, no sparks, no camera flash, no motion streaks of light."

GEGNER = {
    "Thief": {
        "wer": "young Korean thief in a black hoodie with the hood up, black cloth face mask, round black-rimmed glasses, "
               "black jeans, black sneakers with white soles and a small black backpack",
        "waffe": "He holds only ONE single straight red-and-black steel crowbar with a curved claw end, exactly the same "
                 "crowbar as in the reference, always in his RIGHT hand (on the viewer's left). Never a hammer, never a "
                 "second tool. ",
        "posen": {
            "windup": "facing the viewer in a three-quarter view, he pulls the crowbar in his right hand far back behind "
                      "his right shoulder, leaning back, weight on his back foot",
            "attack": "facing the viewer, he swings the crowbar in his right hand forward toward the viewer's left, his "
                      "right arm fully extended, lunging forward",
            "heavy_windup": "facing the viewer, he grips the crowbar with BOTH hands and lifts it high above his head",
            "heavy_attack": "facing the viewer, he smashes the crowbar down with BOTH hands in a full forward swing, body "
                            "bent forward",
        }},
    "Pirate": {
        "wer": "red-bearded pirate with an eye patch, red bandana, torn sleeveless shirt, striped red sash, brown torn "
               "trousers and bare feet",
        "waffe": "He holds only ONE curved cutlass, always in his RIGHT hand (on the viewer's left); the whole sword "
                 "including its tip stays inside the image. ",
        "posen": {
            "windup": "he raises the cutlass in his right hand high behind his head, leaning back",
            "attack": "he slashes the cutlass in his right hand forward and down toward the viewer's left, arm extended, "
                      "lunging forward",
            "heavy_windup": "he holds the cutlass hilt with both hands high over his right shoulder, body twisted",
            "heavy_attack": "he swings the cutlass with both hands in a full horizontal slash toward the viewer's left, "
                            "body twisted forward, the whole blade inside the image",
            "surrender": "he kneels with both hands raised, the cutlass lying on the ground in front of him",
            "defeated": "he lies knocked out on his back on the ground, the cutlass beside him",
        }},
    "Alien": {
        "wer": "grey alien with big black eyes in a white and silver space suit with small blue lights",
        "waffe": "It holds only ONE silver ray gun, always in its RIGHT hand (on the viewer's left); no muzzle flash. ",
        "posen": {
            "windup": "crouching, it pulls the ray gun in its right hand back to its chest, left arm forward for balance",
            "heavy_windup": "crouched and tense, it holds the ray gun with both hands close to its chest",
        }},
    "Agent": {
        "wer": "agent in a black suit, white shirt, black tie, dark sunglasses and an earpiece",
        "waffe": "He holds only ONE black telescopic baton, always in his RIGHT hand (on the viewer's left); no gun, no "
                 "second weapon. ",
        "posen": {
            "windup": "he raises the baton in his right hand high behind his head, leaning back",
            "attack": "he swings the baton in his right hand forward and down toward the viewer's left, arm extended, "
                      "lunging forward",
            "heavy_windup": "he grips the baton with both hands and raises it over his right shoulder",
            "heavy_attack": "he smashes the baton down with both hands in a full forward swing, body bent forward",
        }},
    "DrunkCasanova": {
        "wer": "drunk Casanova with slicked dark hair in a dark red velvet blazer, black shirt and black trousers, a red "
               "rose between his teeth",
        "waffe": "He holds only ONE green wine bottle by its neck, always in his RIGHT hand (on the viewer's left); no "
                 "other object, no gun. ",
        "posen": {
            "windup": "staggering, he lifts the bottle in his right hand HIGH up and far back behind his head, arm bent, leaning back",
            "attack": "he smashes the bottle in his right hand forward and DOWN toward the viewer's left like a club, arm fully extended in front of his body, body lunging forward, "
                      "extended, lunging",
        }},
    "Heinrich": {
        "wer": "tanned older man with slicked-back grey hair, sunglasses, gold chain, open white linen shirt, white "
               "shorts and white loafers",
        "waffe": "He holds ONE champagne glass, always in his LEFT hand (on the viewer's right), and fights with his "
                 "right fist. ",
        "posen": {
            "windup": "he pulls his right fist far back behind his head, leaning back",
            "attack": "he throws a punch with his right fist toward the viewer's left, arm fully extended, lunging",
            "heavy_windup": "he raises his right fist high above his head, body twisted, about to hammer down",
            "heavy_attack": "he hammers his right fist down and forward with full body weight, body bent forward",
            "defeated": "he lies knocked out on his back on the ground, the glass spilled beside him",
        }},
    "Vampire": {
        "wer": "pale vampire woman with long black hair, black velvet gown and a long black cape with red lining",
        "waffe": "She holds ONE silver dagger in her RIGHT hand (on the viewer's left); the whole cape stays fully "
                 "inside the image. ",
        "posen": {
            "attack": "she thrusts the dagger in her right hand forward toward the viewer's left, arm extended, cape "
                      "flowing behind her",
            "heavy_windup": "she raises her left hand with clawed fingers high, dagger held back in her right hand, "
                            "baring her fangs",
            "heavy_attack": "she lunges forward slashing with the claws of her left hand toward the viewer's left, fangs "
                            "bared, cape flowing",
            "hurt": "she recoils backward, one hand at her chest, face in pain",
            "enraged": "she hisses with fangs bared, both clawed hands raised in front of her chest, the cape hanging closed "
                       "around her body",
            "flee": "she turns away and runs to the right, cape flowing behind her",
            "surrender": "she kneels with her head bowed, dagger lying on the ground",
            "defeated": "she lies collapsed on the ground on her side, cape spread around her",
        }},
    "Paparazzo": {
        "wer": "middle-aged man with grey hair and a mustache, black leather jacket, plain GREY t-shirt, red lanyard with "
               "a press badge, blue jeans and white sneakers",
        "waffe": "He holds only ONE big black camera with a long lens, in his RIGHT hand or by its strap. ",
        "posen": {
            "heavy_windup": "he swings the camera by its strap high above his head like a club",
            "heavy_attack": "he slams the heavy camera forward with his right arm fully extended toward the viewer's left, the camera far in front of his body, lunging hard forward, body bent "
                            "forward",
            "surrender": "he kneels and raises both hands, the camera hanging from the strap around his neck",
            "victory": "he triumphantly holds the camera up and grins",
        }},
    "Unit1": {
        "wer": "boxy weathered cream-white walking robot labeled UNIT-01 with yellow-black hazard stripes and a red fire extinguisher "
               "on its back",
        "waffe": "",
        "posen": {
            "heavy_windup": "it pulls its right mechanical arm far back and crouches on its legs, ready to punch",
            "heavy_attack": "it punches forward with its right mechanical fist toward the viewer's left, arm fully "
                            "extended",
            "enraged": "it stands tall with both mechanical arms raised, the warning light on top switched on",
            "defeated": "it has collapsed on the ground, legs folded, a thin wisp of smoke rising",
        }},
    "Brute": {
        "wer": "huge Samoan man with tribal tattoos, a dirty white tank top, grey cargo pants and taped fists",
        "waffe": "He holds ONE heavy iron chain in his RIGHT hand (on the viewer's left); the whole chain stays inside "
                 "the image. ",
        "posen": {
            "heavy_windup": "he whirls the chain above his head with his right hand, body twisted",
            "heavy_attack": "he lashes the chain forward toward the viewer's left, the chain stretched out but fully "
                            "inside the image",
            "flee": "he turns away and runs to the right, the chain coiled short in his right hand close to his body",
        }},
    "Dog": {
        "wer": "brindle mastiff with a spiked collar",
        "waffe": "",
        "posen": {
            "attack": "it lunges forward with its mouth wide open, biting toward the viewer's left, ears fully visible",
            "heavy_attack": "it leaps forward through the air with its jaws wide open, ears fully visible",
            "windup": "it crouches low to the ground, head lowered, hackles raised, lips pulled back over its teeth, "
                      "ready to spring, ears fully visible",
            "heavy_windup": "it rears up on its hind legs with both front paws lifted high, snarling with bared teeth, "
                            "ears fully visible",
        }},
    "SeaMonster": {"wer": "green crocodile-like sea monster with orange spines", "waffe": "",
                   "posen": {"attack": "it lunges forward with its jaws wide open toward the viewer's left"}},
    "Shark": {"wer": "great white shark", "waffe": "",
              "posen": {"defeated": "it lies HORIZONTALLY on its side, belly turned up, motionless with closed eyes, the whole shark horizontal and fully inside the image"}},
    "Siren": {
        "wer": "red-haired mermaid with a pearl necklace and a green-gold scaled mermaid tail",
        "waffe": "Her whole mermaid tail including the tail fin and all of her hair stay fully inside the image. ",
        "posen": {
            "idle": "she sits upright, calm, looking at the viewer, her mermaid tail curled in front of her so the whole tail and tail fin are fully visible inside the image",
            "windup": "she pulls her right arm back behind her shoulder, fingers curled like claws",
            "heavy_windup": "she raises both arms above her head, hair flying, about to strike",
            "heavy_attack": "she lunges forward reaching toward the viewer's left with both hands",
            "hurt": "she recoils backward, one hand at her chest, face in pain",
            "enraged": "she screams with arms spread wide",
            "weakened": "she slumps forward, exhausted, one hand on the ground",
            "flee": "she turns away, diving to the right",
            "surrender": "she lowers her head and raises her open hands",
            "defeated": "she lies collapsed on her side, tail curled",
            "victory": "she sits proudly with her chin raised, smiling",
        }},
}


FAUST = {
    "windup": "he pulls his right fist far back behind his head, leaning back, weight on his back foot",
    "attack": "he throws a punch with his right fist toward the viewer's left, arm fully extended, lunging forward",
    "heavy_windup": "he raises both fists high above his head, body twisted, about to hammer down",
    "heavy_attack": "he slams both fists down and forward toward the viewer's left with full body weight, body bent forward",
}
KO = ("he has collapsed onto the floor and lies on his side, his whole body low and horizontal on the ground, "
      "head resting on one arm, eyes closed, knocked out")
GEGNER.update({
    "Mime": {"wer": "lanky French street mime with a white painted face, black beret, black-and-white striped shirt, black "
                    "suspenders, baggy black trousers, white gloves and a red scarf",
             "waffe": "His hands are EMPTY, he holds nothing. ",
             "posen": {"heavy_windup": "he raises both white-gloved fists high above his head, body twisted, about to "
                                       "hammer down, hands empty"}},
    "Bat": {"wer": "large fruit bat with golden-orange fur on its body and dark brown leathery wings",
            "waffe": "Its whole wingspan stays fully inside the image and is narrower than half the image width. ",
            "posen": {"windup": "wings folded back, head pulled back, mouth CLOSED, crouched and tense",
                      "attack": "it swoops forward toward the viewer's left with its wings HALF folded close to its body, mouth WIDE open showing its fangs, the whole bat small and inside the image",
                      "heavy_windup": "it rears up with both wings raised UP close above its head (not spread sideways), mouth CLOSED, the whole bat inside the image",
                      "heavy_attack": "it dives at the viewer's left with fangs bared and claws forward, wings swept tightly back along its body, the whole bat inside the image",
                      "flee": "it flies away to the right, wings spread but fully inside the image"}},
    "Pigeon": {"wer": "grey city pigeon with an iridescent green-purple neck",
               "waffe": "",
               "posen": {"windup": "it pulls its head far back and crouches, wings slightly lifted, beak CLOSED",
                         "attack": "it pecks forward toward the viewer's left, neck stretched far out, beak WIDE open",
                         "heavy_windup": "it flaps up with both wings raised high, beak closed",
                         "heavy_attack": "it dives forward toward the viewer's left, wings spread, beak open, claws forward"}},
    "Rat": {"wer": "big brown sewer rat with a long pink tail",
            "waffe": "Its whole body and tail stay fully inside the image. ",
            "posen": {"idle": "it stands on all four legs, tail curled beside it, fully inside the image",
                      "windup": "it crouches low, head pulled back, mouth CLOSED, tense",
                      "attack": "it lunges forward biting toward the viewer's left, mouth WIDE open showing long yellow incisors",
                      "heavy_windup": "it rears up on its hind legs, front paws raised, mouth closed, tail curled tightly beside its feet",
                      "weakened": "it crouches exhausted with its head low, tail curled tightly beside its body",
                      "defeated": "it lies flat on its side, motionless, eyes closed, tail curled tightly beside its body",
                      "heavy_attack": "it leaps forward through the air toward the viewer's left, mouth wide open, claws out"}},
    "PirateTorch": {"wer": "pirate with long black dreadlocks, red bandana, striped red-and-white shirt, brown torn trousers and bare feet",
                    "waffe": "He holds ONE burning wooden torch, always in his RIGHT hand (on the viewer's left); the small flame stays fully inside the image. ",
                    "licht": "Only the torch flame burns; no other glow, no sparks.",
                    "posen": {"windup": "he lifts the torch in his right hand HIGH above and behind his head, arm bent back, leaning far back, weight on his back foot",
                              "attack": "he swings the torch forward and DOWN toward the viewer's left, his arm fully extended far in front of his body, lunging hard forward",
                              "heavy_windup": "he holds the torch with both hands over his right shoulder, body twisted, the whole flame inside the image",
                              "heavy_attack": "he thrusts the torch forward with both hands toward the viewer's left, body bent forward",
                              "hurt": "he recoils backward, free hand at his chest, torch held low",
                              "defeated": "he lies knocked out on his back on the ground, the torch beside him"}},
    "ThiefArab": {"wer": "slim young thief in a black hoodie with the hood up, black face mask, black jeans and black sneakers",
                  "waffe": "He holds only ONE single straight red-and-black steel crowbar with a curved claw end, exactly the same crowbar as in the reference, always in his RIGHT hand (on the viewer's left). Never a hammer, never an axe, never a second tool. ",
                  "posen": {"windup": "facing the viewer, he pulls the crowbar in his right hand far back behind his right shoulder, leaning back",
                            "attack": "facing the viewer, he swings the crowbar in his right hand forward toward the viewer's left, arm fully extended, lunging",
                            "heavy_windup": "facing the viewer, he grips the crowbar with BOTH hands and lifts it high above his head",
                            "heavy_attack": "facing the viewer, he smashes the crowbar down with BOTH hands in a full forward swing, body bent forward"}},
    "YasinDrone": {"wer": "athletic young man with short dark hair and a beard, open white linen shirt, beige shorts and white sneakers, holding a drone remote controller, with a small black quadcopter drone flying close to him",
                   "waffe": "There is exactly ONE small drone and it stays fully inside the image, close to him. ",
                   "posen": {"idle": "he stands relaxed holding the controller, the drone hovering just above his shoulder",
                             "windup": "he pulls the controller back to his chest, the drone rises just above his head",
                             "attack": "he thrusts the controller forward and the drone dives toward the viewer's left in front of him",
                             "heavy_windup": "he braces with both thumbs on the controller, the drone hovering high above his head but inside the image",
                             "heavy_attack": "he leans forward and the drone shoots low straight toward the viewer's left in front of his knees",
                             "hurt": "he is hit and doubles over in pain, bent forward at the waist, one hand clutching his stomach, face grimacing, staggering back one step, the drone tilted and wobbling beside him",
                             "enraged": "he shouts angrily, the drone hovering aggressively beside his head",
                             "victory": "he laughs triumphantly and thrusts the controller high above his head with one arm fully raised, the other fist pumped, the drone hovering beside him",
                             "surrender": "he kneels and raises both open hands, the controller on the floor in front of him, the drone landed beside it",
                             "defeated": "he lies on his side on the floor, knocked out with eyes closed, the controller dropped beside his hand, the ONE intact drone resting on the floor next to him, the whole scene small and centered"}},
    "Alon": {"wer": "man in his forties with short brown hair, dark sunglasses, black t-shirt with a white rocket print, black jeans, white sneakers and a silver jetpack on his back",
             "waffe": "The jetpack is switched OFF, no flames. ",
             "posen": dict(FAUST, heavy_windup="he crouches low with both fists clenched, ready to launch forward",
                           heavy_attack="he rams forward shoulder first toward the viewer's left, body almost horizontal, both fists forward",
                           defeated=KO)},
    "MaxwellMaximum": {"wer": "very muscular dark-skinned bald bodybuilder in gold briefs with a golden champion belt and black wrist wraps",
                       "waffe": "",
                       "posen": dict(FAUST, surrender="he kneels with his head bowed and both open hands raised",
                                     defeated=KO)},
    "MaxwellSports": {"wer": "very muscular dark-skinned bald man with a white headband, a white towel around his neck, orange tank top, black shorts and black sneakers",
                      "waffe": "",
                      "posen": dict(FAUST, defeated=KO)},
    "MaxwellSteward": {"wer": "very muscular dark-skinned bald man in a white yacht steward shirt with gold epaulettes, navy shorts and white sneakers",
                       "waffe": "",
                       "posen": dict(FAUST, defeated=KO)},
})
GEGNER["YamamotoSamurai"] = {   # 23.10.2026: t2i drew two figures for defeated -> edit from idle instead
    "wer": "short bald Japanese man with a neat black fringe, a thin moustache, small round glasses and a white headband, "
           "in traditional black and red samurai armor",
    "waffe": "His single katana lies on the floor beside his open hand. ",
    "posen": {"defeated": "he has collapsed onto the floor and lies flat on his back, his whole body low and horizontal on "
                          "the ground, arms spread, eyes closed, glasses crooked, knocked out"},
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    name = sys.argv[1]
    g = GEGNER[name]
    posen = g["posen"]
    if "--posen" in sys.argv:
        wahl = sys.argv[sys.argv.index("--posen") + 1].split(",")
        posen = {k: v for k, v in posen.items() if k in wahl}
    if "--liste" in sys.argv:
        print(name, ", ".join(posen))
        return
    ref = os.path.join(OUT, "kampf_ref", name + "_idle_rand.png")
    quelle = sys.argv[sys.argv.index("--quelle") + 1] if "--quelle" in sys.argv else "idle"   # Vorlage-Pose
    idle = Image.open(os.path.join(OUT, "expressions", "combat", name, quelle + ".png")).convert("RGBA")
    idle = idle.crop(idle.getchannel("A").getbbox())
    skala = float(sys.argv[sys.argv.index("--skala") + 1]) if "--skala" in sys.argv else 0.62   # kleiner = mehr Rand
    idle.thumbnail((int(W * skala), int(H * skala)))
    leinwand = Image.new("RGBA", (W, H), (232, 228, 220, 255))
    leinwand.alpha_composite(idle, ((W - idle.width) // 2, H - idle.height - int(H * 0.14)))
    os.makedirs(os.path.dirname(ref), exist_ok=True)
    leinwand.convert("RGB").save(ref)
    sicher = os.path.join(OUT, "_expressions_papierkorb", "combat", name, time.strftime("%Y-%m-%d_%H%M%S"))
    for k in posen:
        f = os.path.join(OUT, "expressions", "combat", name, k + ".png")
        if os.path.exists(f):
            os.makedirs(sicher, exist_ok=True)
            shutil.move(f, sicher)
    st = ps("/api/state")
    alt_cfg = {k: st["cfg"].get(k) for k in ("sprite_src", "ref_image", "ref_mode", "ref_boost_mode", "ref_boost_value")}
    alt_karten = {c["name"]: c["prompt"] for c in st["decks"]["kampf"]}
    try:
        ps("/api/presets", {"action": "load", "name": "Kampf_" + name})
        kp = ps("/api/set_preset_laden", {"char": "Kampf_" + name, "kost": "Kampf"})
        st = ps("/api/state")
        an = set(kp.get("tags") or [])
        tags = st["cfg"]["tags"]
        for t in tags:
            t["on"] = t["name"] in an
        mo = dict(st["cfg"].get("mode_opts") or {})
        mo["sprite"] = dict(mo.get("sprite") or {}, aspect="%dx%d" % (W, H), width=W, height=H, ref_mode="full",
                            ref_boost_mode="off", ref_boost_value=4)
        vis = dict(st["cfg"].get("decks_visible") or {}, kampf=True)
        ps("/api/config", {"tags": tags, "mode": "sprite", "sprite_src": "i2i", "ref_image": ref, "ref_mode": "full",
                           "ref_boost_mode": "off", "ref_boost_value": 4, "width": W, "height": H,
                           "aspect": "%dx%d" % (W, H), "mode_opts": mo, "combine_mode": "all", "decks_visible": vis,
                           "view_pro_karte": False, "st_rembg": True, "st_crop": True,
                           "sprite_prompt": EDIT.format(wer=g["wer"], waffe=g["waffe"], licht=g.get("licht", LICHT), pose="{kampf}")})
        for k, text in posen.items():
            d = ps("/api/state")["decks"]
            karten = {c["name"] for c in d["kampf"]}
            if k not in karten:
                print("%-13s keine Karte im Deck kampf - uebersprungen" % k)
                continue
            for c in d["kampf"]:
                c["sel"] = c["name"] == k
                if c["name"] == k:
                    c["prompt"] = text
            soll = set(kp.get("outfit") or []) | set(kp.get("setting") or [])
            fehlt = sorted(soll - {x["name"] for x in d["outfit"] + d["setting"]})
            if not kp.get("outfit") or fehlt:   # 23.10.2026: else Prompt Studio would use ALL outfit cards
                sys.exit("%s: Karte fehlt in Prompt Studio (%s) - abgebrochen" % (name, ", ".join(fehlt) or "kein Outfit"))
            for x in d["outfit"]:
                x["sel"] = x["name"] in set(kp.get("outfit") or [])
            for x in d["setting"]:
                x["sel"] = x["name"] in set(kp.get("setting") or [])
            for x in d["st"]:
                x["sel"] = False
            n = ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": 1}).get("queued", 0)
            print("%-13s %s %d Auftrag" % (name, k, n))
    finally:
        d = ps("/api/state")["decks"]
        for c in d["kampf"]:
            c["prompt"] = alt_karten.get(c["name"], c["prompt"])
        ps("/api/decks", d)
        st = ps("/api/state")
        ps("/api/presets", {"action": "load", "name": "Kampf_" + name})
        ps("/api/config", dict({k: v for k, v in alt_cfg.items() if v is not None},
                               decks_visible=dict(st["cfg"].get("decks_visible") or {}, kampf=False)))


if __name__ == "__main__":
    main()

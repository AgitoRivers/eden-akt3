# -*- coding: utf-8 -*-
r"""Red Trio Phase 0 (Duc 30.10.2026): je 3 Varianten fuer die neuen Bilder der Quest. Abnahme danach auf einer Seite.

    casting_red_trio.py                 Probelauf
    casting_red_trio.py --los [--nur hg|weiss|gegner] [--motiv macchia_three_ways]

hg      6 Hintergruende -> ST\backgrounds\_varianten\eden_rise_<name>_v1..3.png (uebernehmen: wie hintergrund_bild --waehle)
weiss   Mr. White Dialog: Yacht_MrWhite_A/_B/_C, je 2 Portraits -> expressions\_casting_red_trio. Fassung A ist das
        Gesicht des vorhandenen Kampf-Sprites AgentAlpha; B und C wuerden einen neuen Kampfsatz brauchen.
gegner  Gepanzerter Schwarzer Loewe, Panzer-Mufflon, ARK-Hyaene, Hirtendrohne: Kampf_<Name>_A/_B/_C, nur idle -> expressions\combat\<Name>_<A|B|C>
        Den vollen Kampfsatz gibt es erst fuer die freigegebene Fassung.
"""
import os, random, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "werkzeuge"))
LOS = "--los" in sys.argv
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None
MOTIV = sys.argv[sys.argv.index("--motiv") + 1] if "--motiv" in sys.argv else None
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
_HALTEN = []       # jedes Modul wickelt stdout neu ein; ohne Referenz schliesst der alte Wrapper den Puffer

sys.argv = [sys.argv[0]]
import studio_kampf_gegner as sk  # noqa: E402
_HALTEN.append(sys.stdout)
import duc_common as dc  # noqa: E402
from kampf_alphas import ZOO_ANGRY, ZOO_COLLAR as COLLAR  # noqa: E402
_HALTEN.append(sys.stdout)
sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
_HALTEN.append(sys.stdout)

PS = cd.PS
ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
N_HG = 3

HG = {
    "macchia_three_ways": "Wide photograph from a slightly raised viewpoint of a small bare clearing in the Corsican macchia in "
        "warm late afternoon light. Exactly three separate dirt trails start from the clearing like the three prongs of "
        "a trident, with green scrub between them. The first trail curves away to the left into a burnt forest of "
        "blackened cork oak trunks. The second trail runs straight ahead up the middle of the image and disappears into "
        "a narrow dark gorge between two tall granite walls. The third trail curves away to the right and climbs a bare "
        "rocky ridge with one thin rusty radio mast on the skyline. All three trails are equally wide and clearly "
        "visible, photorealistic, wide angle, no people, no animals, no text",
    "charcoal_road": "Wide photograph of an old charcoal burners' road through a burnt cork oak forest in Corsica. Blackened "
        "trunks with peeling bark, grey ash on the ground, small bright green shoots returning between the stones, two "
        "low round earth mounds of abandoned charcoal kilns beside a pale dusty track that runs into the distance, "
        "hazy orange evening sun between the trunks, quiet and sad, photorealistic, wide angle, eye level, no people, "
        "no animals, no text",
    "charcoal_hut": "Wide interior photograph of an abandoned charcoal burner's stone hut in the Corsican mountains at dusk. "
        "Rough dry stone walls blackened by soot, a small fire burning in a simple stone hearth on the right, an old "
        "wooden bench and a low table in the warm firelight, a rusty kettle, a stack of split wood, an open doorway on "
        "the left showing a blue evening sky and burnt tree trunks. Open floor in the middle, warm and lonely, "
        "photorealistic, wide angle, eye level, no people, no text",
    "bone_gorge": "Wide photograph inside a narrow rocky gorge in the Corsican mountains. Tall weathered granite walls on both "
        "sides with long deep claw scratches in the rock, a dry stony stream bed in the middle, a few bleached animal "
        "ribs and a goat skull lying between the stones, dry thorn bushes, cold blue shadow below and a thin strip of "
        "golden sunlight high on the rock above, ominous and silent, photorealistic, wide angle, eye level, no people, "
        "no living animals, no text",
    "antenna_ridge": "Wide photograph of a bare windswept granite ridge high above the Corsican coast in late afternoon light. "
        "A thin old rusty radio mast with guy wires stands on the right, a small grey metal equipment box at its foot, "
        "low wind-bent scrub between the rocks, a stony footpath coming up from the left, the deep blue Mediterranean far "
        "below and a wide pale sky, lonely and exposed, photorealistic, wide angle, eye level, no people, no animals, "
        "no text",
    "village_beach_bar": "Wide photograph of a small hand-built beach bar on a sandy village beach in Corsica at golden hour. A "
        "driftwood counter under a roof of dried reeds, mismatched wooden stools, a string of warm bulbs, three red "
        "aprons hanging from a post, a hand-painted wooden sign reading Mochi's, a small metal water bowl in the sand "
        "beside the counter. Behind it calm turquoise water, a few pastel houses of the fishing village and green "
        "mountains. Open sand in the foreground, warm and hopeful, photorealistic, wide angle, eye level, no people, "
        "no animals",
}

# Fassung: (Gesicht, Outfit)
ANZUG = "a sharp white tailored suit, a black shirt, a white tie, black leather gloves, a discreet earpiece with a coiled wire"
WEISS = [("Yacht_MrWhite", "MrWhite", True, {
    "A": ("Mr. White, a silver-haired Scandinavian agent chief in his fifties, a hard narrow face with a small scar on his "
          "chin, grey slicked-back hair, clean-shaven, pale watchful eyes, a lean upright build, a calm polite expression",
          ANZUG + ", black sunglasses pushed up into his hair"),
    "B": ("Mr. White, an elegant silver-haired Scandinavian man of about sixty, a long aristocratic face with deep lines "
          "and a small scar on his chin, immaculately combed silver hair, pale blue eyes, a slight courteous smile that "
          "does not reach his eyes, tall and slim",
          ANZUG + ", a white pocket square, a thin silver watch"),
    "C": ("Mr. White, a gaunt silver-haired Nordic man in his fifties, a very thin angular face with hollow cheeks and a "
          "small scar on his chin, short cropped silver hair, colourless patient eyes, a perfectly still expression, "
          "lean and very straight",
          ANZUG + ", the jacket buttoned to the top"),
})]

# Name: {Fassung: (Art, Subject, Merkmale, Format)}
PLATTE = ("heavy brushed steel armour plates bolted directly onto its body, with visible steel hinges and bolts, old "
          "scars and rubbed fur around the edges of the metal")
# Der Schwarze Loewe beim ersten Kampf am Kloster (Duc 30.10.2026): gepanzert wie im Text kl_bau, ueber dem Herzen fehlt die
# Platte (die hat Danzel gestohlen). Das bisherige LionAlpha bleibt fuer Akt 3.
LOEWE = "a rare huge melanistic black lion with jet-black fur all over its whole body and a thick jet-black mane, glowing amber eyes"
LUECKE = ("a bare gap on the left side of its chest with four empty bolt holes where one plate is missing, showing black fur and "
          "the old scars around it")
GEGNER = {
    "LionPlated": {
        "A": ("wesen", LOEWE, "old pale scars, a torn ear, " + PLATTE + " on its shoulders and flanks, " + LUECKE + ", " + ZOO_ANGRY + COLLAR, "quer"),
        "B": ("wesen", LOEWE, "starved and thin as a coat on a hook with visible ribs and hip bones, old pale scars, a torn ear, "
              + PLATTE + " on its shoulders and flanks, too big for its thin body, " + LUECKE + ", " + ZOO_ANGRY + COLLAR, "quer"),
        "C": ("wesen", LOEWE, "starved with visible ribs, old pale scars, a torn ear, " + PLATTE + " on its shoulders and flanks, "
              + LUECKE + ", no collar, a small round red light implanted in the skin at the back of its neck, half "
              "overgrown by scar tissue, " + ZOO_ANGRY.rstrip(", "), "quer"),
    },
    "PlatedMouflon": {
        "A": ("wesen", "a large wild Corsican mouflon ram",
              "dark chestnut fur, huge curled horns, " + PLATTE + " on its shoulders and across its forehead, furious "
              "dark eyes, " + COLLAR, "quer"),
        "B": ("wesen", "a gaunt wild Corsican mouflon ram",
              "thin body with visible ribs, patchy dark fur, one curled horn broken off, " + PLATTE + " on its flanks "
              "and shoulders, wild staring eyes, " + COLLAR, "quer"),
        "C": ("wesen", "a massive wild Corsican mouflon ram",
              "thick neck, dark fur, wide curled horns tipped with steel caps, " + PLATTE + " covering its chest, "
              "shoulders and forehead like a battering ram, head lowered, " + COLLAR, "quer"),
    },
    "ArkHyena": {
        "A": ("wesen", "a lean spotted hyena",
              "coarse sandy fur with dark spots, a sloping back, a powerful neck, bared yellow teeth, hungry dark eyes, "
              + COLLAR, "quer"),
        "B": ("wesen", "a scarred spotted hyena that has lived in a laboratory cage",
              "thin patchy fur with shaved squares and old surgical scars on its flank, bared teeth, a tense crouch, "
              "frightened angry eyes, " + COLLAR, "quer"),
        "C": ("wesen", "a big female spotted hyena",
              "heavy shoulders, a raised bristling dark mane along her neck and back, dark spots on sandy fur, jaws open "
              "in a snarl, " + COLLAR, "quer"),
    },
    "ShepherdDrone": {
        "A": ("wesen", "a heavy matte black quadcopter surveillance drone hovering in the air, a machine with no living parts",
              "four large propellers in motion blur, a compact armoured body, a round camera lens, a small loudspeaker "
              "horn under the body, one single small round glowing red light that blinks", "quer"),
        "B": ("wesen", "a large grey six-rotor military drone hovering in the air, a machine with no living parts",
              "six propellers in motion blur, a thin antenna array on top, a sensor dome below, a short curved metal "
              "emitter hanging under it like a shepherd's crook, one single small round glowing red light", "quer"),
        "C": ("wesen", "a sleek black tilt-rotor drone hovering in the air, a machine with no living parts",
              "two large rotors on short wings, a narrow angular body, a row of small round sensors on its nose, one "
              "single small round glowing red light", "quer"),
    },
}


def hintergruende():
    import item_bilder as ib
    import hintergrund_bild as hb
    _HALTEN.append(sys.stdout)
    var = os.path.join(ST_BG, "_varianten")
    os.makedirs(var, exist_ok=True)
    ib.NEGATIV = hb.NEGATIV
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    n = 0
    for name, prompt in HG.items():
        if MOTIV and name != MOTIV:
            continue
        for k in range(1, N_HG + 1):
            g = ib.graph(prompt, var, "eden_rise_%s_v%d" % (name, k), random.randint(1, 2 ** 31), True)
            g["6"]["inputs"].update({"width": 1664, "height": 928})
            ib.post("/prompt", {"prompt": g})
            n += 1
    print("Hintergruende eingereiht:", n)


def mr_white():
    cd.FIGUREN = WEISS
    cd.ORDNER = "_casting_red_trio"
    cd.main()


def gegner():
    st = cd.ps("/api/state")
    alt_preset = st["cfg"].get("preset_active")
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    presets, sets = dc.load_json(sk.F_PRESETS, None, "Studio"), dc.load_json(sk.F_SETS, None, "Studio")
    namen = []
    for name, fassungen in GEGNER.items():
        if MOTIV and name != MOTIV:
            continue
        for k, (art, subj, look, fmt) in fassungen.items():
            n = "%s_%s" % (name, k)
            karte = "kampf_" + n.lower()
            if karte in da:
                da[karte]["prompt"] = look
            else:
                d["outfit"].append({"name": karte, "prompt": look, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
            presets["Kampf_" + n] = sk.preset(n, art, subj, [], fmt)
            sets["Kampf_%s|Kampf" % n] = {"outfit": [karte], "setting": ["A Sprite Background"], "tags": ["View: Kampf"]}
            namen.append(n)
    cd.ps("/api/decks", d)
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    dc.save_json(sk.F_SETS, sets, "Studio")
    try:
        subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", "idle", "--gegner", ",".join(namen)], check=True)
    finally:
        if alt_preset:
            cd.ps("/api/presets", {"action": "load", "name": alt_preset})


def main():
    teile = {"hg": hintergruende, "weiss": mr_white, "gegner": gegner}
    print("Hintergruende: %d x %d · Mr. White: %d Fassungen x %d · Gegner: %s" % (
        len(HG), N_HG, len(WEISS[0][3]), len(cd.SEEDS), ", ".join("%s x%d" % (n, len(f)) for n, f in GEGNER.items())))
    if not LOS:
        print("Probelauf - nichts geschrieben.")
        return
    for t, f in teile.items():
        if not NUR or NUR == t:
            f()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
r"""Bibis Tier-Selfies fuer alle 14 Tiere (Duc 02.11.2026): je Tier zwei Momente hintereinander, eine kleine Szene (A, dann B),
je Moment zwei Seeds. Stil wie Runde 3: fashion_prompt des Presets Bibi_Selfie mit nur den aktiven Tags (tags_on), Hintergrund
bibi_selfie_pen. Jedes Outfit zweimal: bibi_nach_1..5, bibi_arbeit, bibi_anime (abends). Frisur je Tier anders; Pony gemischt (Duc: "misch es durch"): mit Pony Biscuit, Sorry, Monsieur, Madame, Monday, Twelve, Ghost (Ordner _4), ohne die anderen sieben (Ordner _5).

    bibi_tier_selfies_4.py [tier,tier]   -> ComfyUI\output\expressions\_bibi_tier_selfies_4\<tier>_<a|b>_<n>.png
"""
import json, re, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\PromptStudio")
PS, COMFY = "http://127.0.0.1:8301", "http://127.0.0.1:8189"
ORDNER = sys.argv[2] if len(sys.argv) > 2 else "_bibi_tier_selfies_4"
SEEDS = (240211, 771903)
ABEND = ", now at dusk, the last pink light over the bay and a small warm lantern hanging from the roof beam"
# tier: (outfit, frisur oder None = steht im Outfit, Moment A, Moment B)
TIERE = {
    "biscuit": ("bibi_nach_1", "loose soft beach waves over her shoulders, blunt straight bangs",
                "Right beside her face a big brindle mastiff-type dog with a broad black face, folded ears and a pink tongue is licking her ear, "
                "the dog's neck bare with smooth short fur. She squeezes one eye shut and laughs with her mouth open",
                "The same big brindle mastiff-type dog has knocked her over into the straw and lies on her chest with its heavy head on her "
                "shoulder, tail blurred from wagging. She lies on her back in the straw, holding the phone up above them, laughing helplessly"),
    "sorry": ("bibi_nach_1", "a low ponytail tied with a red bandana, blunt straight bangs",
              "Beside her a spotted hyena with round ears lies in the straw with its mouth open as if it were laughing, and she laughs with it",
              "The same spotted hyena has turned its head away and yawns hugely, completely bored. She looks into the camera with a flat "
              "deadpan face, as if her best joke just died"),
    "monsieur": ("bibi_nach_2", "half up half down with a small knot on top, soft face-framing tendrils loose at her temples, blunt "
                                "straight bangs, the rest long and straight",
                 "A grey macaque sits on her shoulder and reaches for her phone with both hands. She laughs in surprise and holds on to it",
                 "Now the grey macaque holds the phone himself: a crooked, much too close shot of his serious face filling half the picture, "
                 "and behind him, slightly out of focus, she laughs with both hands empty"),
    "duchess": ("bibi_nach_2", "a long side braid over one shoulder, a deep side part, no bangs, her forehead free",
                "Behind her stands a stocky wild mouflon ewe with curled horns and a russet coat, her shoulders smooth and bare. She points "
                "back at her, beaming with pride",
                "The same mouflon ewe has calmly pulled the mustard yellow bandana from her neck and is chewing it. She grabs the other "
                "end, laughing and outraged at the same time"),
    "rusty": ("bibi_nach_3", "pulled up into a high bouncy ponytail, slicked back, no bangs, her forehead free, a few loose strands at the neck",
              "Next to her face a red panda stands up on its hind legs with both front paws raised high, trying to look scary. She presses "
              "her free hand to her cheek in big pretend terror, mouth wide open",
              "The same red panda now lies asleep on its back across her lap, belly up and paws in the air. She looks into the camera with "
              "a soft grin and raised eyebrows"),
    "truffle": ("bibi_nach_3", "two small space buns on top of her head, a middle part, no bangs, her forehead free",
                "Behind her a huge dark wild boar stands in the mud and stares straight into the camera with a stern face. She smiles broadly "
                "beside it",
                "The same huge dark wild boar now gently takes a red apple from her open hand with its lips, very carefully. She holds a "
                "finger to her lips for the camera, eyes shining"),
    "madame": ("bibi_nach_4", "very long, sleek and perfectly straight, glossy and smooth, with blunt straight bangs",
               "On her shoulder sits a plump grey Russian Blue cat with green eyes, glaring into the camera with deep disapproval. She grins "
               "sheepishly",
               "The same plump grey Russian Blue cat now sits on top of her head like a hat, still glaring into the camera. She looks up at "
               "it cross-eyed, trying not to laugh"),
    "bones": ("bibi_nach_4", "a messy low bun, the front swept back with two loose strands framing her face, no bangs, her forehead free",
              "Behind her on the stone wall sits a large bearded vulture with rusty orange chest feathers and something white in its beak. "
              "She looks sideways at it, suspicious",
              "The same bearded vulture has dropped a big old white bone into her free hand. She holds it up to the camera with a very "
              "polite, very forced smile"),
    "monday": ("bibi_nach_5", "in two long loose braids over her shoulders, with blunt straight bangs",
               "A large calm reddish-brown capybara with a blunt square nose lies across her shoulders and the back of her head like a heavy "
               "fur scarf, its eyes half closed. She looks straight into the camera with a deadpan face and a tiny smile",
               "Now she and the same capybara sit side by side in a shallow stone water trough in the pen, only their heads above the water, "
               "both with exactly the same calm half-closed eyes"),
    "mr_v": ("bibi_nach_5", "a high ponytail wrapped in a mustard bandana, hair pulled back, no bangs, her forehead free",
             "Behind her in the dry grass a long grey Komodo dragon lies flat in the sun with its forked tongue out. She keeps a careful "
             "distance and grins nervously",
             "The same long grey Komodo dragon now wears her round sunglasses on its head and lies in the sun, completely unimpressed. She "
             "crouches a careful distance away and gives a proud thumbs up"),
    "twelve": ("bibi_arbeit", None,
               "At her feet an old Hermann's tortoise with a white number 12 painted on its shell walks slowly out of the picture. She points "
               "down at it, laughing",
               "Much later, the sun now low and golden: the same old tortoise with the white number 12 has moved only a hand's width. She "
               "sits in the straw with her chin in her hand, bored, and stares into the camera"),
    "sunday": ("bibi_arbeit", "pulled back from her face, no bangs, her forehead free",
               "Behind her in the straw a big grey wolf with a pale chest and a dark back lies fast asleep, curled up. She leans towards the "
               "camera and grins nervously, eyebrows raised",
               "The same big grey wolf now rests its head on her lap, eyes half open and calm. She sits completely still, eyes wide with "
               "joy, and does not dare to breathe"),
    "pudding": ("bibi_anime", "a loose messy side part, no bangs, her forehead free",
                "In her arms she holds a small round brown bear cub, fast asleep against her chest. Her eyes are wet and she smiles",
                "The same small brown bear cub is wide awake now and chews happily on her small black plush lion keychain. She gasps in mock "
                "outrage into the camera"),
    "ghost": ("bibi_anime", None,
              "Far behind her, high on a grey rock, a snow leopard lies almost invisible against the stone, only its pale eyes clear. She "
              "points back over her shoulder with a grin",
              "The same snow leopard now sits silently right behind her shoulder, very close, its pale eyes on the camera. She has not "
              "noticed and still grins into the camera"),
}


def post(url, daten):
    req = urllib.request.Request(url, data=json.dumps(daten).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main():
    import studio
    nur = sys.argv[1].split(",") if len(sys.argv) > 1 else list(TIERE)
    decks = json.load(open(r"X:\AI\PromptStudio\decks.json", encoding="utf-8"))
    karte = lambda kat, name: next(c["prompt"] for c in decks[kat] if c["name"] == name)
    preset = json.load(open(r"X:\AI\PromptStudio\presets.json", encoding="utf-8"))["Bibi_Selfie"]
    with urllib.request.urlopen(PS + "/api/state", timeout=30) as f:
        state = json.loads(f.read())
    alle_tags = {x["name"]: x for x in state["cfg"].get("tags", [])}
    aktiv = [alle_tags[n] for n in preset.get("tags_on", []) if n in alle_tags]
    kat = lambda c: ", ".join(x["prompt"].strip().rstrip(",") for x in aktiv if (x.get("cat") or "").lower() == c and x.get("prompt", "").strip())

    def zusammen(outfit, haar, moment):
        p = preset["fashion_prompt"]
        for c in ("body", "skin", "haircolor", "hair", "face", "photo", "action"):
            p = p.replace("{tags_%s}" % c, kat(c))
        p = p.replace("{tags_hairstyle}", haar or "")
        szene = karte("setting", "bibi_selfie_pen") + (ABEND if outfit == "bibi_anime" else "")
        p = p.replace("{outfit}", karte("outfit", outfit)).replace("{setting}", szene)
        p = p.replace("{st}", "").replace("{expression}", moment).replace("Look: {look},\n", "").replace("{look}", "")
        p = re.sub(r",\s*,", ",", p)
        return re.sub(r", +\n", ",\n", p)

    cfg = dict(state["cfg"])
    wart = []
    for tier in nur:
        outfit, haar, a, b = TIERE[tier]
        for teil, moment in (("a", a), ("b", b)):
            if not moment:                      # Nachlauf (bibi_tier_selfies_6) setzt nur einen Moment je Tier
                continue
            p = zusammen(outfit, haar, moment)
            for n, seed in enumerate(SEEDS, 1):
                c = dict(cfg, loras=preset["loras"], mode="sprite", sprite_src="t2i", width=896, height=1152, negative_prompt="",
                         st_set=ORDNER, st_rembg=False, st_crop=False)
                wart.append(post(COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "%s_%s_%d" % (tier, teil, n), seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 3600
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler, flush=True)


if __name__ == "__main__":
    main()

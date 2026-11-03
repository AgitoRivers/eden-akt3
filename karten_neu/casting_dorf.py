# -*- coding: utf-8 -*-
r"""Dorf-Figuren Phase 0 (Duc 30.10.2026): Casting fuer Pascal, Mina, Ba Tu, Sandru, Don Anghjulu und vier Hintergruende.
Nur Bilder, nichts im Spiel. Siehe docs/wiki/welt/dorf_figuren.md.

    casting_dorf.py                 Probelauf
    casting_dorf.py --los [--nur hg|figuren] [--motiv church_interior]

figuren Yacht_<Name>_A/_B/_C, je 2 Portraits -> expressions\_casting_dorf\<Preset>_<A|B|C>
hg      4 Hintergruende -> ST\backgrounds\_varianten\eden_rise_<name>_v1..3.png (nichts ins Hauptverzeichnis)
Alle Figuren bekleidet, normale Kleidung, nicht romanzierbar. Krea laeuft mit CFG 1: alles positiv formuliert.
"""
import os, random, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "werkzeuge"))
LOS = "--los" in sys.argv
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None
MOTIV = sys.argv[sys.argv.index("--motiv") + 1] if "--motiv" in sys.argv else None
FASS = dict(x.split(":") for x in sys.argv[sys.argv.index("--fass") + 1].split("+")) if "--fass" in sys.argv else None
# --fass Yacht_BaTu:BC+Yacht_Mina:C  rendert nur diese Fassungen neu (alte Ordner vorher in den Papierkorb legen)
_HALTEN = []       # jedes Modul wickelt stdout neu ein; ohne Referenz schliesst der alte Wrapper den Puffer

sys.argv = [sys.argv[0]] + (["--los"] if LOS else [])
import castings_danzel as cd  # noqa: E402
_HALTEN.append(sys.stdout)

ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
N_HG = 3

HG = {
    "church_interior": "Wide interior photograph of a small Corsican baroque village church, looking down the central aisle "
        "from the entrance. Rows of dark worn wooden pews on both sides, a simple gilded baroque altar with a carved "
        "wooden retable at the far end, whitewashed walls with faded painted marble patterns, a few small arched windows "
        "with warm afternoon light falling in. The roof is brand new: bright pale fresh timber beams and clean light "
        "roof boards above the nave. On the left near the front a section of the ceiling is still covered by a tall "
        "metal scaffold tower with wooden planks and a folded tarpaulin. Open stone floor in the middle, dust in the "
        "sunbeams, quiet and warm, photorealistic, wide angle, eye level, no people, no text",
    "batu_shop": "Wide interior photograph of a small old family-run Asian grocery shop in a Corsican harbour village, seen from a low "
        "angle in one corner of an irregular L-shaped room, deliberately not symmetrical. Crooked wooden shelves of different "
        "heights along the left wall only, packed with bags of rice, noodles, tins, jars and bottles of fish sauce, crates on "
        "the floor, a stack of sacks in a corner. On the right, in a little alcove, a small Vietnamese Catholic home altar: a "
        "statue of the Virgin Mary on a red cloth, a small crucifix, a vase of fresh flowers, oranges on a plate and a little "
        "red electric candle. In the far corner a homely cooking place with a worn gas stove, a dented pot and a wooden table "
        "with mismatched stools, a family calendar on the wall. Clean white square floor tiles, plain beige painted walls, a small window with daylight in the back wall, warm soft light, cosy and lived in like someone's "
        "home, photorealistic, wide angle, eye level, no people, no text",
    "av_market_interior": "Wide interior photograph of a small busy-looking supermarket inside a very old Corsican stone building. "
        "Ancient rough stone barrel vaults and thick arches form the ceiling and walls, warm weathered stone, worn flagstone "
        "floor. Bright white modern shelving units with cold white LED strips stand in rows between the arches, every shelf "
        "completely full from top to bottom with colourful packaged goods, cereal boxes, tins, bottles and snacks facing "
        "forward, a stack of white shopping baskets, a white checkout counter with a card reader. The cold white light clashes "
        "with the old warm stone, photorealistic, wide angle, eye level, no people, no text",
    "av_market_exterior": "Wide photograph of the front of an old three-storey Corsican shop house with weathered ochre "
        "plaster, faded green wooden shutters and a worn stone doorstep, standing at a small fishing harbour in the "
        "morning. Above the shop door hangs a brand new, cold white illuminated sign board with a simple abstract white "
        "geometric symbol on a dark panel, glowing against the old wall. Across the narrow cobbled street directly "
        "opposite stands a small cosy bar with a faded awning, little round tables and wooden chairs outside. A "
        "glimpse of boats and calm blue water at the end of the street, empty street, photorealistic, wide angle, "
        "eye level, no people, no text",
}

# ---- Figuren: (Preset, ST-Name, Mann?, {Fassung: (Gesicht, Outfit)}) ----
FIGUREN = [
    ("Yacht_Pascal", "Pascal", True, {
        "A": ("Pascal Leca, a 52-year-old Corsican man with sun-tanned olive skin, a slim build, a friendly lined face "
              "with tired kind brown eyes, a receding hairline and a half-bald head with thin gray-brown hair at the "
              "sides, a warm modest smile, easy to like and instantly unremarkable",
              "a white fedora hat with a black band worn on his half-bald head, a double-breasted dark navy pinstripe suit with a white pocket square in the breast pocket, a light blue "
              "shirt, a loosened dark red tie, polished brown leather shoes"),
        "B": ("Pascal Leca, a 52-year-old Corsican man with a deep tan and weathered olive skin, a lean build with "
              "slightly stooped shoulders, a long gentle face with deep smile lines and weary kind dark eyes, a nearly "
              "bald head with a thin ring of gray hair, clean-shaven, an approachable crooked smile",
              "a white fedora hat with a gray band, a double-breasted dark charcoal pinstripe suit with a folded cream pocket square, a white shirt, a "
              "loosened navy tie, black leather shoes"),
        "C": ("Pascal Leca, a 52-year-old Corsican man with sun-browned skin, a slim wiry build, a tanned face with "
              "soft tired hazel eyes, a balding head with thin gray-brown hair on the sides, a neat gray moustache, "
              "a friendly slightly amused expression, like the kind neighbour everyone trusts",
              "a white straw fedora hat with a dark ribbon, a double-breasted dark gray chalk-stripe suit with a burgundy silk pocket square, a pale shirt with "
              "an open collar and no tie, brown loafers"),
    }),
    ("Yacht_Mina", "Mina", False, {
        "A": ("Mina Orsoni, a 24-year-old adult woman, a Corsican courier with deeply sun-tanned golden-brown skin, a "
              "cheeky wide grin, bright dark eyes, short messy tousled dark brown hair, slim and sporty",
              "a bright pink hooded rain jacket worn open, an oversized loose white cotton blouse hanging over short "
              "tight beige hot pants, sturdy brown boots, a pink scooter helmet pushed back and hanging at the nape of her neck"),
        "B": ("Mina Orsoni, a 24-year-old adult woman, a Corsican with a deep bronze tan, a lopsided cheeky smirk, "
              "sparkling brown eyes, a short choppy dark pixie cut that sticks out in all directions, small and wiry",
              "a pink waterproof rain jacket with the hood down, a very oversized light striped blouse with rolled "
              "sleeves hanging loosely over short tight beige hot pants, white sneakers, a glossy pink scooter helmet held in one "
              "hand"),
        "C": ("Mina Orsoni, a 24-year-old adult woman, a Corsican with tanned olive-brown skin, a playful grin with "
              "one raised eyebrow, big dark eyes, short messy black hair with a few wild strands, athletic and "
              "energetic",
              "a hot pink rain jacket zipped halfway, an oversized baggy sand-coloured blouse over short tight beige hot pants, tan "
              "leather boots, a pink helmet sitting on top of her head with the strap open"),
    }),
    ("Yacht_BaTu", "BaTu", False, {
        "A": ("Bà Tư, a woman of about 75, Vietnamese from Saigon with warm tanned skin, small and upright, a "
              "dignified lined face with high cheekbones, alert stern dark eyes, white hair pinned up in a neat "
              "elegant updo, a firm closed mouth with a trace of warmth, a small gold cross on a thin chain, a green "
              "jade bangle on her wrist",
              "a Vietnamese silk blouse in deep jade green with a mandarin collar and fabric knot buttons, airy wide "
              "black trousers with a pattern of small yellow flowers, black cloth shoes, hands folded in front of her"),
        "B": ("Bà Tư, a woman of about 75, Vietnamese from Saigon with sun-tanned skin, tiny and very straight-backed, "
              "a fine-boned weathered face with deep laugh lines, sharp watchful dark eyes, snow-white hair pinned "
              "high on her head in a smooth twist with a simple hairpin, a small gold cross pendant, a jade bangle on "
              "her left wrist",
              "a Vietnamese silk blouse in dark burgundy with a mandarin collar, loose airy black trousers printed "
              "with yellow flowers, black flat shoes, an upright dignified stance"),
        "C": ("Bà Tư, a woman of about 75, Vietnamese from Saigon with a tanned complexion, small and composed, a "
              "round strong face with age spots and smooth dignified features, penetrating stern dark eyes, white "
              "hair pinned up high with a pearl hairpin, a tiny golden cross on a chain, a jade bangle on her wrist",
              "a light cream Vietnamese silk blouse with a stand-up collar and small embroidered flowers, flowing wide "
              "black trousers with yellow flowers, black cloth shoes, hands relaxed at her sides"),
    }),
    ("Yacht_Sandru", "Sandru", True, {
        "A": ("Sandru Amrani, a 30-year-old Corsican man of Moroccan descent, clearly sun-tanned warm brown skin, "
              "short dark curly hair, a narrow slim build, a thin friendly face with dark eager eyes, a "
              "trying-too-hard polite smile, slightly tense shoulders",
              "a white polo shirt with a small white logo on a dark patch on the chest and a small name tag reading "
              "ALEX, dark knee-length shorts, slim black leg braces clearly visible from the knee down to the ankle "
              "on both legs, plain black sneakers"),
        "B": ("Sandru Amrani, a 30-year-old Corsican man of Moroccan descent, deep golden-brown tanned skin, short "
              "dark curly hair, a thin delicate build, a boyish narrow face with a faint stubble, warm worried brown "
              "eyes, a hopeful nervous smile showing teeth",
              "a white polo shirt with a small white logo on a dark band at the chest and a name tag ALEX, short "
              "dark gray shorts, slender black powered leg braces visible from knee to ankle on both legs, white "
              "sneakers"),
        "C": ("Sandru Amrani, a 30-year-old Corsican man of Moroccan descent, sun-darkened brown skin, short dark "
              "curly hair, a lanky slim build, a long kind face with tired eyes and dark circles, an earnest eager "
              "smile that is a little forced",
              "a crisp white polo shirt with a tiny white logo on a dark patch and a small name tag ALEX, dark "
              "trousers rolled up to the knee, sleek black leg braces visible from the knee to the ankle on both "
              "legs, black shoes"),
    }),
    ("Yacht_Anghjulu", "Anghjulu", True, {
        "A": ("Don Anghjulu, a Portuguese priest of about 60 with deeply sunburnt dark brown skin, a round plump "
              "build, a big round face with a red nose and ruddy cheeks, gray stubble, small twinkling eyes, thinning "
              "gray hair, a huge warm laugh with crinkled eyes",
              "a black cassock with the sleeves rolled up over his forearms and the collar open, a small silver "
              "hip flask held in one hand, black shoes"),
        "B": ("Don Anghjulu, a Portuguese priest of about 60 with a very dark sun-baked tan, a stout round body, a "
              "jolly red-nosed face with broken veins on his cheeks, a few days of white stubble, bushy gray eyebrows, "
              "a booming warm laugh with his head thrown back a little",
              "a rumpled full-length black soutane reaching down to his ankles with a small white clerical collar tab "
              "at the open neck, the sleeves rolled up over his forearms, a small flat metal flask held in one hand, "
              "black leather shoes on his feet"),
        "C": ("Don Anghjulu, a Portuguese priest of about 60 with weathered mahogany-brown skin, a chubby soft build, "
              "a broad kind face with a bulbous red nose, salt-and-pepper stubble, balding head with white tufts at "
              "the sides, wide delighted laughing eyes and a big open smile",
              "a faded black cassock with the sleeves pushed up to the elbows and the top buttons open, a small "
              "pewter flask in his hand, worn black shoes"),
    }),
    ("Yacht_AdrienCast", "AdrienCast", True, {
        "A": ("Adrien Morel, a handsome 28-year-old Indian man, warm brown skin, short black hair, a strong straight "
              "nose, calm dark eyes, a trimmed short beard, a lean athletic build, a quiet steady expression, a "
              "faint pained tension in his posture",
              "a dusty camouflage combat uniform of the French Foreign Legion with the sleeves rolled up, a green beret "
              "tucked under his shoulder strap, a white bandage around his left thigh over the trousers, worn black "
              "combat boots"),
        "B": ("Adrien Morel, a handsome 28-year-old Indian man, medium brown skin, thick black hair cut very short at "
              "the sides, sharp cheekbones, deep calm dark eyes, three days of dark stubble, a tall lean build, "
              "a composed tired look",
              "a sand-coloured Foreign Legion field shirt with rolled sleeves, a green beret tucked under his "
              "shoulder strap, a stained white bandage wrapped around his left thigh over the trousers, worn black "
              "combat boots"),
        "C": ("Adrien Morel, a handsome 28-year-old Indian man, golden-brown skin, short wavy black hair, a fine "
              "jaw, gentle but guarded dark eyes, a faint calm half smile, a lean muscular build, slightly favouring "
              "his right leg",
              "a dusty olive Foreign Legion camouflage uniform with the sleeves rolled up and the collar open, a "
              "green beret in his belt, a white bandage tied around his left thigh over the trousers, worn black "
              "combat boots"),
    }),
]


def sprite_prompt(gesicht, mann):
    p = _orig_sprite_prompt(gesicht, mann)
    if gesicht.startswith("Sandru"):          # Beinschienen reichen bis zum Knoechel: ganzer Koerper bis zu den Fuessen
        p = p.replace("from head to knees", "from head to feet").replace("head and knees inside", "head and feet inside")
    return p


_orig_sprite_prompt = cd.sprite_prompt
cd.sprite_prompt = sprite_prompt


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


def figuren():
    cd.FIGUREN = [(p, n, m, {k: v for k, v in f.items() if not FASS or k in FASS.get(p, "")})
                  for p, n, m, f in FIGUREN if not FASS or p in FASS]
    cd.ORDNER = "_casting_dorf"
    cd.main()


def main():
    print("Hintergruende: %d x %d · Figuren: %s" % (len(HG), N_HG, ", ".join(f[0] for f in FIGUREN)))
    if not LOS:
        cd.FIGUREN = FIGUREN
        cd.ORDNER = "_casting_dorf"
        cd.main()
        print("Probelauf - nichts geschrieben.")
        return
    for t, f in {"figuren": figuren, "hg": hintergruende}.items():
        if not NUR or NUR == t:
            f()


if __name__ == "__main__":
    main()

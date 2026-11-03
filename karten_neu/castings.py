# -*- coding: utf-8 -*-
r"""Castings Runde 2 (20.10.2026, Duc: "Gesichter sehen noch KI-Jane-Doe aus"): erfundene Namen, individuelle
Gesichtsbeschreibung, Basis Real3 0.7 + Lenovo 0.7 + Redux 0.5 (ohne Nsfw2), Stil-LoRA wie Casting-Lauf 2.
Recherche-Ergebnis: Name + Stadt + Alter + Gesichtsform/Nase/Augen/Brauen/Mund/Kinn + ein Erkennungsmerkmal,
natuerliche Asymmetrie und Hautporen; KEINE Pauschal-Schoenheitswoerter ("gorgeous", "perfect", "model looks"),
die mitteln das Gesicht zum Durchschnitt.

    castings.py                     Probelauf
    castings.py --modell turbo      Lauf auf Krea2 fp8 (krea2_turbo_fp8_scaled + qwen3vl fp8) -> _casting_r2_turbo
    castings.py --modell edit       Lauf auf BigLoveKreaEdit1 (bf16)                          -> _casting_r2_edit
    castings.py --rN --modell turbo Runde N (3..12, siehe Bloecke unten) -> _casting_rN_turbo

Ergebnis (20.10.): Yacht_Jess, Yacht_Sofie, Yacht_Madison, Yacht_Ana, Yacht_Noelle im Prompt Studio (Krea2 fp8),
Referenzbilder in output\expressions\_casting_final. Runde 1 liegt in _archiv/castings_v1.py.
Prompt-Lehren: ein Koerperwort pro Richtung (slender/athletic-Haeufung bremst die Oberweite), kein "small" am
Kleidungsstueck, Koerper in den Subject-Satz (Body-Tags wirken auf Krea2 fp8 kaum), Saggy-LoRA max ~0.15 + warmer
Hautton gegen Grau; Hegre zieht aus; Seed aendert bei Krea2 (CFG 1) nur Details.
"""
import io, json, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
JETZT = time.strftime("%Y-%m-%d %H:%M")
MODELLE = {"turbo": {"unet": "krea2_turbo_fp8_scaled.safetensors", "clip": "qwen3vl_4b_fp8_scaled.safetensors"},
           "edit": {"unet": "BigLoveKreaEdit1_bf16.safetensors", "clip": "qwen3vl_4b_bf16.safetensors"}}
MODELL = sys.argv[sys.argv.index("--modell") + 1] if "--modell" in sys.argv else None
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else None      # sonst Studio-Seed
ZUSATZ = sys.argv[sys.argv.index("--zusatz") + 1] if "--zusatz" in sys.argv else ""       # Ordner-Suffix
BASIS = [{"name": "Krea_Real3.safetensors", "strength": 0.7}, {"name": "Krea_Lenovo.safetensors", "strength": 0.7},
         {"name": "Krea_Redux.safetensors", "strength": 0.5}]
HAUT = ("natural skin texture with visible pores, slight natural asymmetry in her face, a real individual face, "
        "not a generic model face")


def L(stil):
    return BASIS + [{"name": "Krea_%s.safetensors" % stil, "strength": 0.7}]


def LL(c):
    """Stil-LoRA plus optionale Zusatz-LoRAs (6. Feld, Runde 8)."""
    return L(c[2]) + (list(c[5]) if len(c) > 5 else [])


# (Name, Gesicht, Stil-LoRA, Tags, Outfit)
CASTINGS = [
    ("Freja Lindqvist", "a 28-year-old Swedish woman from Gothenburg with a long oval face, wide-set pale blue eyes with "
     "slightly hooded lids, straight light blonde brows, a narrow nose with a slightly upturned tip, a wide mouth with a "
     "thin upper lip and a full lower lip, a small beauty mark under her left eye", "Ersties",
     ["Color: Platinum", "Style: Long Layered", "Body: Curvy", "Large", "Clean Girl", "Glossy Lips"],
     "a white cropped ribbed tank top, light blue high-waisted denim shorts, white sneakers"),
    ("Niamh Callaghan", "a 27-year-old Irish woman from Cork with a heart-shaped face, round green eyes, sparse light "
     "copper brows, a small button nose, dense freckles across her nose, cheeks and shoulders, a slight gap between her "
     "front teeth, very pale porcelain skin with pink undertones and long wavy bright copper-red hair", "Ersties",
     ["Color: Red", "Pale skin", "Freckles", "Style: Waves", "Body: Curvy", "Busty", "Full Glam"],
     "a fitted black off-shoulder knit top, a tight black leather mini skirt, black ankle boots"),
    ("Oksana Hrytsenko", "a 29-year-old Ukrainian woman from Lviv with broad high cheekbones, almond-shaped grey-green "
     "eyes, thick straight dark-blonde brows, a strong straight nose with a slight bump on the bridge, full pouty lips "
     "and a soft rounded chin", "Ersties",
     ["Color: Honey blonde", "Style: Blowout", "Body: Curvy", "Large", "Smokey Eye", "Nude Lips"],
     "a tight beige ribbed knit midi dress, nude heels"),
    ("Thais Moreira", "a 28-year-old Brazilian woman from Salvador da Bahia with an oval face, large dark brown doe eyes, "
     "thick arched brows, a broad soft nose, very full lips, warm golden-tan skin and a tiny mole above her upper lip",
     "Hegre", ["Color: dark brown", "Style: Long Wet Hair", "Body: Curvy", "Thick", "Large", "Summer", "Sheen"],
     "a tiny yellow crop top, a white denim mini skirt, gold hoop earrings, flat sandals"),
    ("Giulia Esposito", "a 30-year-old Italian woman from Naples with a long face, a strong Roman nose with a gentle hump, "
     "deep-set dark brown eyes, heavy straight black brows, a defined jaw, a wide smile with slightly uneven teeth and "
     "olive skin", "Hegre",
     ["Color: Black", "Style: Straight", "Body: Curvy", "Busty", "Winged Liner", "Glossy Lips"],
     "a tight red bodycon dress with thin straps, black strappy heels"),
    ("Jess Whitlock", "a 27-year-old Australian surfer from Byron Bay with a square jaw, a slightly crooked nose, light "
     "hazel eyes with fine laugh lines, sun-bleached brows, sun freckles on her nose and cheeks and sun-weathered tanned "
     "skin", "Hegre",
     ["Color: Honey blonde", "Style: Waves", "Body: Athletic", "Body: Curvy", "Large", "Summer", "Tan Lines"],
     "a white tied-up linen shirt over a small turquoise bikini top, frayed denim shorts, barefoot"),
    ("Valentina Ocampo", "a 28-year-old Colombian woman from Medellin with a round face and full cheeks, upturned "
     "honey-brown cat eyes, thick dark brows, a short wide nose, full heart-shaped lips, caramel skin and a deep dimple "
     "in her right cheek", "Insta",
     ["Color: Brunette", "Style: Blowout", "Body: Curvy", "Thick", "Busty", "Full Glam", "Glossy Lips"],
     "a black square-neck corset top, tight high-waisted black jeans, black heels"),
    ("Yasmine Haddad", "a 29-year-old Lebanese woman from Beirut with a long angular face, large dark almond eyes with "
     "heavy lids, very thick dark brows, a prominent elegant aquiline nose, full lips and olive-beige skin", "Insta",
     ["Color: Black", "Style: Long Layered", "Body: Curvy", "Large", "Smokey Eye", "Winged Liner"],
     "a fitted emerald satin camisole, cream wide-leg trousers, gold jewellery, nude heels"),
    ("Maelys Joseph", "a 28-year-old woman from Fort-de-France, Martinique, with high round cheekbones, wide-set dark "
     "brown eyes, a broad nose with a rounded tip, very full lips, a small gap between her front teeth, deep brown skin "
     "and long curly black hair", "Insta",
     ["Color: Black", "Style: Long Layered", "Body: Curvy", "Busty", "Party Glitter Glam", "Glossy Lips"],
     "a tight white ribbed mini dress, gold hoop earrings, white sandals"),
    ("Lucia Navarro", "a 31-year-old Spanish woman from Seville with a strong square jaw, deep-set warm brown eyes, thick "
     "slightly unruly brows, a long straight nose, a wide mouth, a small scar through her left eyebrow and olive skin",
     "Insta", ["Color: Brunette", "Style: Waves", "Body: Curvy", "Large", "Boudoir Glam", "Glossy Lips"],
     "a black lace-trimmed silk slip top, a high-waisted flowing black mini skirt, black heels"),
]


# Runde 3 (Duc 20.10.): Jess bleibt, 9 neue "hot girl next door" - natuerlich, Alltagsoutfits, Frisuren stark
# verschieden, Pose neutral. Keine Asiatinnen.
CASTINGS_R3 = [CASTINGS[5]] + [
    ("Femke de Vries", "a 26-year-old Dutch woman from Utrecht with a round friendly face, bright blue eyes, light brows, "
     "a small straight nose, rosy cheeks, a wide easy smile with slightly crooked canine teeth", "Ersties",
     ["Color: blonde", "Style: Double Braids", "Body: Curvy", "Large", "Clean Girl", "Blush"],
     "an oversized grey university hoodie, black bike shorts, white socks and sneakers"),
    ("Kasia Nowak", "a 27-year-old Polish woman from Krakow with a soft oval face, grey-blue eyes, straight dark-blonde "
     "brows, a slightly wide nose, full lips and a small mole on her left cheekbone", "Ersties",
     ["Color: Light Brown", "Style: Bob", "Style: Bangs", "Body: Curvy", "Busty", "Nude Lips"],
     "a fitted white t-shirt tucked into high-waisted mom jeans, a thin brown belt, white sneakers"),
    ("Isla MacLeod", "a 26-year-old Scottish woman from Edinburgh with very pale skin, a narrow face, hazel-green eyes, "
     "faint auburn brows, a long thin nose, freckles on her nose and a lopsided grin", "Ersties",
     ["Color: Auburn Red", "Pale skin", "Freckles", "Style: Bun", "State: Messy", "Body: Slender", "B - Soft", "Clean Girl"],
     "a red plaid flannel shirt open over a white tank top, light blue jeans, brown boots"),
    ("Ines Carvalho", "a 28-year-old Portuguese woman from Porto with an oval face, warm brown eyes, thick natural "
     "brows, a slightly hooked nose, full lips, olive skin and a dimpled chin", "Hegre",
     ["Color: dark brown", "Style: Low Ponytail", "Body: Curvy", "Thick", "Large", "Summer"],
     "a yellow floral cotton sundress with thin straps, white canvas sneakers"),
    ("Eleni Papadaki", "a 27-year-old Greek woman from Thessaloniki with a strong straight nose, large dark brown eyes, "
     "thick dark brows that almost meet, a wide mouth, olive skin and a small scar on her chin", "Hegre",
     ["Color: Black", "Style: Top knot", "Body: Curvy", "Busty", "Sport Athleisure", "Sweat"],
     "a black sports bra, grey high-waisted leggings, an open zip hoodie, running shoes"),
    ("Sofie Holm", "a 25-year-old Danish woman from Aarhus with a short heart-shaped face, wide-set light green eyes, "
     "a snub nose, freckled cheeks and a gap between her front teeth", "Hegre",
     ["Color: Platinum", "Style: Lob", "Body: Slender", "Large", "Clean Girl", "Glossy Lips"],
     "a cropped pale blue cardigan with pearl buttons, a short pleated white tennis skirt, white sneakers"),
    ("Brooke Tremblay", "a 27-year-old Canadian woman from Halifax with a square face, blue-grey eyes, a slightly "
     "upturned nose, a few faint acne marks on her jaw and a big toothy smile", "Insta",
     ["Color: Honey blonde", "Style: Ponytail", "Body: Athletic", "Body: Curvy", "Large", "Summer"],
     "a white cropped baseball tee, denim cut-off shorts, white sneakers"),
    ("Camila Ferreyra", "a 28-year-old Argentinian woman from Cordoba with high cheekbones, dark green-brown eyes, "
     "arched brows, a straight narrow nose, full lips and a beauty mark near her right eye", "Insta",
     ["Color: Brunette", "Style: Half Up", "Body: Curvy", "Thick", "Busty", "Instagirl Soft Glam"],
     "a black ribbed long-sleeve crop top, high-waisted light wash jeans, black sneakers"),
    ("Tereza Novakova", "a 26-year-old Czech woman from Brno with a long face, pale grey eyes, thin arched brows, a "
     "straight nose with a rounded tip, soft thin lips and a light scattering of freckles", "Insta",
     ["Color: Light Brown", "Style: Side Braid", "Body: Slender", "Large", "Clean Girl", "Nude Lips"],
     "a loose cream knit sweater slipping off one shoulder, black leggings, ankle boots"),
]
# Runde 4 (Duc 20.10.): Jess + Sofie bleiben, 8 neue im Instagram-Influencer-Stil, alle im selben Deckhand-Outfit
# (weisses Polo, enge Shorts), Haare eher offen, Schoenheit nur indirekt ueber konkrete Merkmale. Alle Insta
# (Hegre zog in Runde 3 die Kleidung aus).
DECK = ("a tight-fitting white short-sleeved polo shirt with a small navy anchor embroidered on the chest, the collar "
        "open, tucked into tight navy deckhand shorts with a white belt, white canvas deck shoes")
GLOW = "luminous clear skin, long dark lashes, glossy healthy hair"


def _r4(name, gesicht, tags):
    return (name, gesicht + ", " + GLOW, "Insta", tags, DECK)


CASTINGS_R4 = [
    _r4(CASTINGS_R3[0][0], CASTINGS_R3[0][1], ["Color: Honey blonde", "Style: Waves", "Body: Athletic", "Body: Curvy",
                                              "Large", "Summer", "Tan Lines"]),
    _r4(CASTINGS_R3[6][0], CASTINGS_R3[6][1], ["Color: Platinum", "Style: Lob", "Body: Slender", "Large",
                                              "Instagirl Soft Glam", "Glossy Lips"]),
    _r4("Madison Reyes", "a 27-year-old Californian woman from San Diego with a sun-kissed oval face, wide hazel eyes, "
        "softly arched brows, a slim straight nose with a slightly upturned tip, full lips with a defined cupid's bow and "
        "a bright wide smile", ["Color: Honey blonde", "Style: Long Layered", "Body: Curvy", "Large",
                                "Instagirl Soft Glam", "Glossy Lips"]),
    _r4("Chloe Marchand", "a 28-year-old French woman from Nice with a delicate heart-shaped face, almond-shaped "
        "blue-green eyes, high cheekbones, a fine straight nose, naturally pouty lips and a small beauty mark on her left "
        "cheek", ["Color: Light Brown", "Style: Waves", "Body: Slender", "Large", "Clean Girl", "Nude Lips"]),
    _r4("Ana Kovac", "a 26-year-old Croatian woman from Split with a long elegant face, striking light grey-blue eyes, "
        "straight dark brows, sharp cheekbones, a narrow nose and full lips", ["Color: dark brown", "Style: Straight",
                                                                              "Body: Slender", "Busty", "Summer"]),
    _r4("Ingrid Solberg", "a 27-year-old Norwegian woman from Bergen with a soft square jaw, clear ice-blue eyes, pale "
        "golden brows, a small straight nose, rosy cheeks and a warm close-lipped smile",
        ["Color: blonde", "Style: Long Wet Hair", "Body: Athletic", "Large", "Clean Girl", "Blush"]),
    _r4("Daniela Ortega", "a 28-year-old Mexican woman from Guadalajara with a rounded face, large warm brown eyes with "
        "a slight upward tilt, thick arched brows, a soft rounded nose, very full lips and warm tan skin",
        ["Color: Black", "Style: Blowout", "Body: Curvy", "Thick", "Busty", "Full Glam", "Glossy Lips"]),
    _r4("Naledi Mokoena", "a 27-year-old South African woman from Cape Town with high round cheekbones, wide dark eyes, "
        "a broad graceful nose, full lips, a long neck and smooth deep brown skin, long natural curly hair",
        ["Color: Black", "Style: Long Layered", "Body: Curvy", "Large", "Party Glitter Glam", "Glossy Lips"]),
    _r4("Noa Ben-David", "a 26-year-old Israeli woman from Tel Aviv with an angular face, large dark green eyes, thick "
        "dark brows, a slightly prominent straight nose, full lips and light olive skin",
        ["Color: Brunette", "Style: Waves", "Body: Curvy", "Busty", "Smokey Eye", "Nude Lips"]),
    _r4("Reka Szabo", "a 28-year-old Hungarian woman from Budapest with a soft oval face, honey-brown eyes, delicate "
        "arched brows, a small upturned nose, a dimple in her left cheek and full rosy lips",
        ["Color: Auburn Red", "Style: Half Up", "Body: Curvy", "Large", "Instagirl Soft Glam", "Glossy Lips"]),
]
# Runde 5 (Duc 20.10.): Auswahl Jess, Sofie, Madison, Ana, Noelle (vorher Noa) auf Krea2 fp8, weisser Bikini, neutral.
BIKINI = "a white string bikini with a small triangle top and tie-side bottoms, barefoot"
_NOELLE = CASTINGS_R4[8]
CASTINGS_R5 = [c[:4] + (BIKINI,) for c in (CASTINGS_R4[0], CASTINGS_R4[1], CASTINGS_R4[2], CASTINGS_R4[4],
                                           ("Noelle Ben-David",) + _NOELLE[1:])]
# Runde 6 (Duc 20.10.): Koerper mischen (Busty/Large/Huge x Athletic/Hourglass/Slender), neuer Tag Body: Hourglass;
# Sofie mit langen Haaren. Haar-, Haut- und Make-up-Tags bleiben wie Runde 5.
_KOERPER = {"Body: Athletic", "Body: Curvy", "Body: Slender", "Body: Hourglass", "Thick", "Busty", "Large", "Huge",
            "B - Soft"}
_R6 = [("Body: Athletic", "Large"), ("Body: Slender", "Busty"), ("Body: Hourglass", "Huge"), ("Body: Slender", "Large"),
       ("Body: Hourglass", "Busty")]
CASTINGS_R6 = []
for _c, _k in zip(CASTINGS_R5, _R6):
    _t = [t for t in _c[3] if t not in _KOERPER] + list(_k)
    if _c[0] == "Sofie Holm":
        _t = ["Style: Long Layered" if t == "Style: Lob" else t for t in _t]
    CASTINGS_R6.append(_c[:3] + (_t, _c[4]))
R6 = "--r6" in sys.argv
if R6:
    CASTINGS = CASTINGS_R6
# Runde 7 (Duc 20.10.): Body-Tags wirkten auf Krea2 fp8 kaum -> Koerper konkret in den Subject-Satz (wirkt am
# staerksten). Sofie: Pferdeschwanz mit Straehnchen.
_KOERPER_SATZ = [
    "an athletic toned body with defined abs, strong legs and large full breasts",
    "a slim slender body with narrow hips and a noticeably large full bust",
    "a voluptuous hourglass body with very large heavy breasts, a tiny waist and wide round hips",
    "a tall slender willowy body with very long legs and large full breasts",
    "a curvy hourglass body with a full round bust, a narrow waist and wide hips",
]
CASTINGS_R7 = []
for _c, _s in zip(CASTINGS_R6, _KOERPER_SATZ):
    _t = list(_c[3])
    if _c[0] == "Sofie Holm":
        _t = [t for t in _t if not t.startswith("Style:")] + ["Style: Ponytail", "State: Tendrils blonde"]
    CASTINGS_R7.append((_c[0], "%s, %s" % (_s, _c[1])) + (_c[2], _t, _c[4]))
R7 = "--r7" in sys.argv
if R7:
    CASTINGS = CASTINGS_R7
# Runde 8 (Duc 20.10.): Jess + Ana brauchen mehr Oberweite -> je 6 Kombinationen Brust-LoRAs/Gewichte/Text.
_BL = lambda n, s: {"name": "Krea_%s.safetensors" % n, "strength": s}
_VAR = [  # (Zusatz-LoRAs, Brust-Tag, Text statt "large full breasts")
    ([_BL("Breast_Size", 0.5)], "Large", "large full breasts"),
    ([_BL("Breast_Size", 1.0)], "Large", "large full breasts"),
    ([_BL("Breast_Slider", 1.0)], "Busty", "very large full breasts"),
    ([_BL("Breast_Slider", 2.0)], "Busty", "very large full breasts"),
    ([], "Huge", "huge heavy breasts"),                                   # Huge-Tag bringt SkiSlope 1.0 mit
    ([_BL("Breast_Size", 0.7), _BL("Saggy_Breasts", 0.4)], "Large", "very large natural heavy breasts"),
]
CASTINGS_R8 = []
for _c in (CASTINGS_R7[0], CASTINGS_R7[3]):
    for _z, _tag, _txt in _VAR:
        _t = [t for t in _c[3] if t not in ("Large", "Busty", "Huge")] + [_tag]
        CASTINGS_R8.append((_c[0], _c[1].replace("large full breasts", _txt), _c[2], _t, _c[4], _z))
R8 = "--r8" in sys.argv
if R8:
    CASTINGS = CASTINGS_R8
# Runde 9 (Duc 20.10.): nur Saggy wirkt auf Krea2 fp8 -> wenig Saggy, mit und ohne Breast_Size 0.7.
_VAR9 = [[_BL("Breast_Size", 0.7), _BL("Saggy_Breasts", 0.15)], [_BL("Breast_Size", 0.7), _BL("Saggy_Breasts", 0.25)],
         [_BL("Saggy_Breasts", 0.15)], [_BL("Saggy_Breasts", 0.25)], [_BL("Saggy_Breasts", 0.35)]]
CASTINGS_R9 = []
for _c in (CASTINGS_R7[0], CASTINGS_R7[3]):
    for _z in _VAR9:
        CASTINGS_R9.append((_c[0], _c[1].replace("large full breasts", "very large natural heavy breasts"), _c[2],
                            list(_c[3]), _c[4], _z))
R9 = "--r9" in sys.argv
if R9:
    CASTINGS = CASTINGS_R9
# Runde 10 (Duc 20.10.): Bremsen raus. Ana: "slender/willowy" (2x + Tag "soft plush and slender build") ruft den
# Laufsteg-Typ mit kleiner Brust; Jess: "athletic/toned/muscular/abs" (4x) ruft den Fitness-Typ. Bikini "small
# triangle top" deckelt sichtbares Volumen. -> Build-Tag raus, Koerper einmal klar, Bikini ohne "small".
_BIK10 = "a white string bikini with a triangle top stretched over her full bust and tie-side bottoms, barefoot"
_K10 = {"Jess Whitlock": "a fit body with a toned stomach, a slim waist and a very large full bust",
        "Ana Kovac": "a tall body with a slim waist, long legs and a very large full bust"}
CASTINGS_R10 = []
for _c in (CASTINGS_R7[0], CASTINGS_R7[3]):
    _ges = _c[1].split(", ", 1)[1]                                   # Koerpersatz aus Runde 7 abtrennen
    _ges = _ges.split(", a 2", 1)
    _ges = "a 2" + _ges[1] if len(_ges) > 1 else _ges[0]
    _t = [t for t in _c[3] if not t.startswith("Body:")]
    for _z in ([], [_BL("Saggy_Breasts", 0.15)]):
        CASTINGS_R10.append((_c[0], "%s, %s" % (_K10[_c[0]], _ges), _c[2], _t, _BIK10, _z))
R10 = "--r10" in sys.argv
if R10:
    CASTINGS = CASTINGS_R10
# Runde 11 (Duc 20.10.): Sofie entschaerfen (3x schlank -> 1x), Slender-Tag raus, Bikini ohne "small".
_s = CASTINGS_R7[1]
_sg = _s[1].split(", a 2", 1)
_sg = "a 2" + _sg[1]
_st = [t for t in _s[3] if not t.startswith("Body:")]
CASTINGS_R11 = [(_s[0], "a slim body with a narrow waist and a noticeably large full bust, " + _sg, _s[2], _st, _BIK10, _z)
                for _z in ([], [_BL("Saggy_Breasts", 0.15)])]
R11 = "--r11" in sys.argv
if R11:
    CASTINGS = CASTINGS_R11
# Runde 12 (Duc 20.10.): Saggy macht die Haut grau -> Gegenmittel im Subject (warmer Hautton) + Saggy 0.1 testen.
WARM = "warm healthy skin tone with a rosy peach undertone and a soft natural glow"
CASTINGS_R12 = []
for _c in (CASTINGS_R10[0], CASTINGS_R10[2], CASTINGS_R11[0]):
    for _w, _st in ((False, 0.1), (True, 0.1), (True, 0.15)):
        CASTINGS_R12.append((_c[0], _c[1] + (", " + WARM if _w else ""), _c[2], _c[3], _c[4],
                             [_BL("Saggy_Breasts", _st)]))
R12 = "--r12" in sys.argv
if R12:
    CASTINGS = CASTINGS_R12
R3 = "--r3" in sys.argv
R4 = "--r4" in sys.argv
R5 = "--r5" in sys.argv
if R5:
    CASTINGS = CASTINGS_R5
if R3:
    CASTINGS = CASTINGS_R3
if R4:
    CASTINGS = CASTINGS_R4
POSE = "neutral" if (R3 or R4 or R5 or R6 or R7 or R8 or R9 or R10 or R11 or R12) else "admiration"
PREFIX = "_casting_r12_" if R12 else "_casting_r11_" if R11 else "_casting_r10_" if R10 else "_casting_r9_" if R9 else "_casting_r8_" if R8 else "_casting_r7_" if R7 else "_casting_r6_" if R6 else "_casting_r5_" if R5 else "_casting_r4_" if R4 else "_casting_r3_" if R3 else "_casting_r2_"


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def sprite_prompt(name, gesicht):
    return ("{tags_action}, candid photo taken with a 50mm lens, soft daylight, full body shot from head to knees, "
            "direct gaze, one single woman alone in the frame, her whole body in full view, head and knees inside the "
            "frame,\nSubject: %s, %s, %s,\nBody: {tags_body},\nHair: {tags_haircolor}, {tags_hairstyle}, {tags_hair}\n"
            "Skin: {tags_skin},\nMakeup: {tags_face}\nWearing: {outfit},\nScene: {setting}, {st},\n{expression},\n"
            "Look: {look},\n{tags_photo}" % (name, gesicht, HAUT))


def main():
    st = ps("/api/state")
    tag_namen = {t["name"] for t in st["cfg"]["tags"]}
    fehler = [t for c in CASTINGS for t in c[3] if t not in tag_namen]
    print("Tags fehlen:", fehler or "-")
    for i, c in enumerate(CASTINGS, 1):
        print("%2d %-17s %s" % (i, c[0], ", ".join("%s %.1f" % (l["name"][5:-12], l["strength"]) for l in LL(c))))
    if fehler or not MODELL:
        print("Probelauf - nichts geschrieben." if not fehler else "Abbruch.")
        return
    ordner = PREFIX + MODELL + ZUSATZ
    d = st["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for i, c in enumerate(CASTINGS, 1):     # Outfit-Karten casting_NN aus Runde 1 weiterverwenden/angleichen
        n = "casting_%02d" % i
        if n in da:
            da[n]["prompt"] = c[4]
        else:
            d["outfit"].append({"name": n, "prompt": c[4], "on": True, "tag": "casting", "sel": False,
                                "back_prompt": c[4] + ", seen from behind"})
    ps("/api/decks", d)
    presets = dc.load_json(F_PRESETS, None, "Studio")
    for i, c in enumerate(CASTINGS, 1):
        presets["Casting_%02d" % i] = {
            "sprite_prompt": sprite_prompt(c[0], c[1]), "negative_prompt": "", "loras": LL(c),
            "ref_image": "", "ref_image_b": "", "tags_on": ["View: Front"] + c[3],
            "cards_on": {"outfit": ["casting_%02d" % i], "setting": ["A Sprite Background"], "st": [POSE]},
            "st_set": "%s/Casting_%02d" % (ordner, i), "created": JETZT, "updated": JETZT}
    dc.save_json(F_PRESETS, presets, "Studio")
    alt = {k: st["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed")}
    alt_preset = st["cfg"].get("preset_active")
    n = 0
    try:
        for i, c in enumerate(CASTINGS, 1):
            name = "Casting_%02d" % i
            ps("/api/presets", {"action": "load", "name": name})
            cfg = ps("/api/state")["cfg"]
            an = set(["View: Front"] + c[3])
            for t in cfg["tags"]:
                t["on"] = t["name"] in an
            ps("/api/config", dict(MODELLE[MODELL], tags=cfg["tags"], mode="sprite", sprite_src="t2i",
                                   combine_mode="all", view_pro_karte=False, st_rembg=True, st_crop=True,
                                   st_set="%s/%s" % (ordner, name), loras=LL(c),
                                   sprite_prompt=presets[name]["sprite_prompt"],
                                   **({"seed": SEED + i * 1000} if SEED is not None else {})))
            d = ps("/api/state")["decks"]
            for k in d:
                wahl = {"outfit": {"casting_%02d" % i}, "setting": {"A Sprite Background"}, "st": {POSE}}.get(k, set())
                for x in d[k]:
                    x["sel"] = x["name"] in wahl
            n += ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": d}).get("queued", 0)
    finally:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt.items() if v is not None})
    print("%s: %d Castings in der Warteschlange -> expressions\\%s" % (MODELL, n, ordner))


if __name__ == "__main__":
    main()

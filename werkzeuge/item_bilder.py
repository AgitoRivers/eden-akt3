# -*- coding: utf-8 -*-
r"""Gegenstandsbilder fuer ein Eden-Modul erzeugen (16.10.2026) - so einfach wie moeglich:

    Item_Bilder.bat                         alle Items ohne Bild erzeugen (vorhandene werden uebersprungen)
    Item_Bilder.bat manga cigars            nur diese Items (neu, ueberschreibt)
    Item_Bilder.bat jeweled_plug --varianten 4    4 Varianten zur Auswahl (items\_varianten\jeweled_plug.jpg)
    Item_Bilder.bat jeweled_plug --waehle 3       Variante 3 uebernehmen
    Item_Bilder_EdenRise.bat ...            dasselbe fuer den Pool der Neufassung (--modul eden_rise, gegenstaende.json)

Braucht ComfyUI Krea2 (Port 8189). Ein Bild je Item im einheitlichen Produktfoto-Look. Krea 2 wird nur bei 1-2 MP
sauber, deshalb entsteht es in 1024x1024 (Original: items\_gross\<id>.png) und wird als 320er WebP-Thumbnail
ausgeliefert (items\<id>.webp, ca. 15 KB) - das zeigt der Laden. Die Motive stehen unten in MOTIV (englisch) - neues Item ohne Eintrag = Label wird
genommen. Neues Item im Modul anlegen, Bat starten, fertig."""
import json, os, random, shutil, sys, time, urllib.request

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMFY = "http://127.0.0.1:8189"
UNET, CLIP, VAE = "krea2_turbo_fp8_scaled.safetensors", "qwen3vl_4b_fp8_scaled.safetensors", "qwen_image_vae.safetensors"
# NSFW-Profil fuer Erwachsenen-Spielzeug: dasselbe Modell wie Prompt Studio + Real3/Nsfw2 (dort trainiert).
# Gilt fuer die Items in NSFW und fuer jeden Aufruf mit --nsfw.
NSFW_PROFIL = {"unet": "BigLoveKreaEdit1_bf16.safetensors", "clip": "qwen3vl_4b_bf16.safetensors", "steps": 11,
               "loras": [("Krea_Real3.safetensors", 0.7), ("Krea_Nsfw2.safetensors", 0.7)]}
NSFW = set()                 # seit 16.10.2026 laufen alle Items mit dem LoRA-Profil (Duc), --turbo fuer den alten Look
STANDARD_NSFW = True
# Hintergruende (Test 16.10.2026) - --hintergrund <name> waehlt einen, Standard steht in HINTERGRUND.
HINTERGRUENDE = {
    "teak": "lying on a weathered teak deck plank of a luxury yacht, soft warm late-afternoon light, gentle shadow, shallow depth of field",
    "abstrakt": "on a seamless studio backdrop with a soft abstract gradient from warm champagne to deep navy, gentle out-of-focus glow, soft diffused light, minimal and calm",
    "holz": "on a clean plain bare light oak wooden surface, nothing else around it, soft even diffused daylight, calm and minimal",
    "leinen": "flat lay from above on smooth folded cream linen fabric, soft even daylight, calm, minimal, lots of empty space around the object",
    "noir": "on a smooth dark charcoal stone surface, soft warm rim light from behind, deep calm shadows, elegant and minimal, dark background",
}
HINTERGRUND = "leinen"         # Duc 16.10.2026: Leinen von oben, ruhig
THUMB = 320                                      # Kantenlaenge des Thumbnails (Karten sind ~210 px breit, x1,5 fuer scharfe Displays)
STIL = ("Studio product photograph of {motiv}, {hintergrund}, centered composition, the object fills the middle "
        "of the frame, photorealistic, high detail, no text, no labels, no people, no hands")
NEGATIV = "text, watermark, logo, letters, people, hands, fingers, blurry, cartoon, anime, 3d render, oversaturated"

MOTIV = {
    # Rosis Werkstatt (25.10.2026): Plates fuer Jacken und Gemelli, Steine fuer die Waffen. Positiv formuliert (Krea CFG 1),
    # keine Loecher oder Lochmuster (Trypophobie): glatte, geschlossene Flaechen.
    "ambrosius_keule": "a golden ceremonial mace with a smooth round golden head and a polished ivory grip, lying flat, warm soft shine",
    "diary_page_1": "a single aged page torn from a handwritten diary, cream paper with brown ink lines of old-fashioned handwriting, a soft fold in the middle",
    "diary_page_2": "a second aged page torn from a handwritten diary, cream paper with brown ink lines of old-fashioned handwriting, a faint water stain at one corner",
    "agent_note": "a small crumpled torn sheet of lined paper with a few lines of hurried handwriting in black ink, folded once, a faint thumbprint smudge in the corner",
    "steel_plate": "a solid rectangular brushed steel plate with smooth beveled edges and a clean flat surface, cool silver grey metal, heavy and plain",
    "titanium_plate": "a thick solid jet black matte metal plate with sharply chamfered corners and a smooth flat surface, deep blackened steel with only a faint blue-violet sheen on its edges, clearly black and nothing like silver",
    "kupfer": "a single solid rectangular copper ingot bar with a warm polished orange-red surface and rounded edges, glowing like a new penny, heavy and plain",
    "silber": "a single solid rectangular silver ingot bar with sloped sides and rounded edges, seen from directly above at a slight angle with its long side running up and down the frame, showing the flat top face and the sloped front edge, a brushed satin warm white-silver surface, plain smooth surface without any engraving, stamp or marking, heavy and plain",
    "jade": "a single smooth polished jade gemstone, oval cabochon, deep translucent green, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "smaragd": "a single emerald gemstone, oval faceted cut, deep vivid green, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "topas": "a single golden topaz gemstone, oval faceted cut, warm orange amber, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "rubin": "a single ruby gemstone, oval faceted cut, deep blood red, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "aquamarin": "a single aquamarine gemstone, oval faceted cut, pale clear sea blue, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "saphir": "a single sapphire gemstone, oval faceted cut, deep royal blue, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "amethyst": "a single amethyst gemstone, oval faceted cut, rich violet purple, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "opal": "a single white opal gemstone, oval cabochon, soft rainbow flashes of blue, green and pink, seen from directly above lying flat on its back and centered, the stone fills about a third of the frame, all alone with nothing next to it",
    "multitool": "a well-used stainless steel multitool, folded half open",
    "holm_compass": "an old brass ship's compass in a worn wooden box, the glass slightly scratched",
    "petru_key": "an old iron key with a cork float and a bit of fishing line tied to it",
    "festa_invite": "a hand-written invitation card with a red wax seal and a sprig of myrtle",
    "spare_inverter": "a used industrial power inverter module, grey metal housing, cooling fins, cables bundled",
    "diesel_canister": "a red metal jerry can for diesel, scratched and dented",
    "manga": "a stack of two Italian manga paperback volumes",
    "arancini": "three golden fried arancini rice balls in grease paper",
    "bao_buns": "two fluffy white steamed bao buns filled with glazed pork belly, cucumber slices and fresh coriander, in a small round bamboo steamer basket",
    "fish_pie": "a homemade fish pie in a blue enamel baking dish with a smooth golden mashed potato top, a serving spoon beside it",
    "torque_wrench": "a professional chrome torque wrench in an open plastic case",
    "olive_oil": "a small glass bottle of golden olive oil with a hand-written paper label and a cork",
    "almanac": "a thick old nautical almanac book with a plain dark blue cloth cover and no lettering at all, worn brass corner protectors, a red ribbon bookmark hanging out",
    "fountain_pen": "a black lacquered fountain pen with a gold nib, cap beside it",
    "notebook": "a new brown leather notebook with an elastic band",
    "dive_torch": "a yellow underwater dive torch with a wrist lanyard",
    "old_chart": "an old rolled nautical chart of a rocky coastline, yellowed paper, partly unrolled",
    "wool_socks": "a pair of hand-knitted grey wool socks with a simple Nordic pattern",
    "designer_perfume": "a luxurious faceted glass perfume bottle with a gold cap",
    "myrtle": "a bottle of dark purple myrtle liqueur with a small glass beside it",
    "candles": "three scented candles in amber glass jars with sprigs of myrtle, flames burning",
    "massage_oil": "an elegant glass bottle of golden massage oil with orange blossoms beside it",
    "silk_blindfold": "a black silk blindfold with long ties, softly folded",
    "pretty_shell": "a large beautiful triton sea shell with a glossy pink and cream spiral",
    "pink_pearl": "a single pink pearl pendant on a delicate fine gold chain",
    "shell_anklet": "a delicate silver anklet chain with a tiny cowrie shell charm",
    "silk_kimono": "a folded midnight-blue silk kimono robe with embroidered white cranes",
    "massage_candle": "a lit massage candle in a small ceramic pot, the wax melted into a pool of warm oil",
    "stockings": "a pair of sheer black thigh-high stockings with wide lace tops, neatly laid out",
    "satin_ties": "an adult bondage restraint set: two pairs of wine-red satin wrist cuffs, each cuff a narrow padded band with a small silver buckle and a long loose satin ribbon, lying casually next to each other",
    "nipple_clamps": "a pair of delicate gold nipple clamps joined by a fine gold chain, in an open black velvet box",
    "lingerie": "champagne-coloured French lace lingerie set, bra and panties with silk ribbons, neatly laid out",
    "plush_cuffs": "a pair of pink fluffy plush handcuffs with a small key",
    "eden_wave": "an adult sex toy: a classic smooth curved white silicone vibrator with a rounded tip and a rose-gold base with one button, lying diagonally",
    "jeweled_plug": "an adult sex toy: a small teardrop-shaped polished stainless steel butt plug lying on its side, tapered rounded tip, narrow neck, flat base set with a pink heart-shaped crystal, next to an open pink velvet pouch",
    "binoculars": "a pair of black marine binoculars with a neck strap",
    "aftershave": "a vintage green glass aftershave bottle with a chrome cap",
    "lockpicks": "a slim black leather roll opened to show a set of steel lock picks",
    "lucky_coin": "an old worn silver coin with a hole punched through it, on a string",
    "tarot": "a fanned-out deck of old tarot cards, the top card face down",
    "used_battery": "a used black marine deep-cycle boat battery, a plain rectangular plastic box with two lead terminal posts on top and a black carrying strap, slightly dusty",
    "panel_cleaner": "a spray bottle of cleaner and a squeegee for solar panels",
    "espresso": "a small cup of double espresso on a saucer, steam rising",
    "sat_data": "a small rugged satellite communication device with a stubby antenna",
    "cuban_rum": "a bottle of aged dark Cuban rum, amber glass",
    "cigars": "an open wooden box of premium cigars with paper bands",
}


# Neue Gegenstaende des Moduls eden_rise (17.10.2026) - Quelle: module\eden_rise\gegenstaende.json
MOTIV.update({
    # Teile und Werkzeuge (Missionsausbau 18.10.2026)
    "ersatzzellen": "two used lithium battery cells with handwritten test labels and taped terminals",
    "relais": "a small black refrigerator compressor relay with copper contacts and a tangle of short wires",
    "messingbuchstaben": "a scattered handful of polished brass letters for a sign, mostly R and S",
    "holzleim": "an old enamel glue pot with amber bone glue and a wooden spatula",
    "eichenbrett": "a single weathered oak board with old varnish and nail holes, as if taken from a church pew",
    "tonerde": "a half-open burlap sack of grey potter's clay with a wet lump on top",
    "uhrenbatterie": "a single silver button cell battery on a small paper card",
    "goldfarbe": "a small tin of gold paint, lid off, with a fine brush resting across it",
    "safran": "a tiny glass jar of deep red saffron threads with a handwritten label",
    "buchbinde_leinen": "a folded length of dark blue bookbinding linen with a curved needle and waxed thread",
    "netzgarn": "a spool of green nylon fishing net twine with a wooden netting needle",
    "bilderrahmen": "a plain light wooden picture frame, empty, with the glass catching the light",
    "armband": "a black silicone watch strap for a dive computer, still in its fleet supply bag",
    "fueller_rohling": "an unengraved fountain pen blank in a simple box, smooth dark barrel",
    "antennenkabel": "a coil of thick black marine antenna cable with a brass connector",
    "werkzeugkoffer": "an open red metal toolbox with spanners, screwdrivers and pliers neatly inside",
    "kochmesser": "a Japanese chef's knife with a wooden handle on a folded kitchen towel",
    "verbandskasten": "a small white first aid box with a red cross, lid open, bandages and plasters inside",
    "lolas_gewuerz": "a small glass jar of coarse sea salt mixed with blue and gold glitter-like spice flakes, hand-written label 'ocean glitter'",
    "tim_tams": "an opened packet of Australian chocolate biscuits, a few biscuits lying beside it",
    "lolas_kekse": "a white plate with homemade chocolate chip cookies, slightly uneven, one with a bite taken out",
    "feigen": "five ripe purple Corsican figs, one cut open showing the red inside",
    "proteinriegel": "two protein bars in shiny black wrappers, one half unwrapped",
    "franzbroetchen": "two homemade Hamburg cinnamon pastries, flattened swirls with caramelised sugar",
    "canistrelli": "a small paper bag of Corsican canistrelli biscuits with aniseed, square and crumbly",
    "single_malt": "a bottle of peaty Islay single malt whisky with a plain dark label and a crystal tumbler beside it",
    "limoncello": "a tall clear glass bottle of bright yellow homemade limoncello with a cork, lemon leaves beside it",
    "cap_corse": "a bottle of red Cap Corse aperitif with an old-fashioned label and a small glass",
    "herzbrille": "a pair of glamorous heart-shaped sunglasses with pink tinted lenses and rhinestones",
    "goldkette": "a thick shiny gold curb chain necklace, coiled",
    "designer_sonnenbrille": "a pair of expensive black designer sunglasses with gold temples, folded",
    "silberring": "a slim plain silver ring on a small piece of driftwood",
    "moka": "a classic aluminium Neapolitan stovetop espresso pot, a little dented",
    "selfie_stick": "a matte black carbon selfie stick, collapsed, with a phone clamp, no phone",
    "polbrille": "a pair of sporty polarised sunglasses with mirrored blue lenses",
    "schweizer_messer": "a red pocket knife with several tools half folded out",
    "gedichtband": "an old cloth-bound poetry book with a faded cover, a dried flower pressed between the pages",
    "ducs_gedicht": "a folded sheet of lined paper with a short hand-written poem in pencil, a few words crossed out",
    "kinderzeichnung": "a child's crayon drawing of a big white yacht, a whale and three stick figures waving, slightly crumpled",
    "seeglas": "three smooth pieces of frosted green sea glass",
    "alvas_rose": "a single red rose with a short stem and a hairpin, a few petals loose",
    "der_stiefel": "an old waterlogged rubber boot with a strand of seaweed and a tiny crab peeking out",
    "macchia_strauss": "a small wild bouquet of Corsican maquis, myrtle, rosemary and white cistus flowers tied with string",
    "korallenzweig": "a small pale pink coral branch found on the beach",
    "alvas_deckel": "a cardboard beer coaster with a bright red lipstick kiss mark on it",
    "eden_cap": "a white baseball cap with a small embroidered golden anchor logo",
    "trillerpfeife": "a shiny golden whistle on a red-white-blue ribbon",
    "konfetti": "a small paper bag spilling colourful confetti",
    "schaerpe": "a glittering pageant sash folded neatly, sparkling pink and gold",
    "faecher": "an open red and black lace flamenco hand fan",
    "lichterkette": "a coiled string of small warm fairy lights with a tiny solar panel",
    "ukulele": "a well-used wooden ukulele with stickers on the body",
    "flamenco_dessous": "a red satin and black lace lingerie set with ruffled flamenco trim, neatly laid out",
    "chiara_tasse": "a hand-painted ceramic mug with a small anchor and the name Chiara painted on it",
    "rosi_schild": "a hand-carved driftwood workshop sign with the words Scuderi & Figlie",
    "sophia_fueller": "an elegant dark green fountain pen with an engraved name on the barrel, in an open box",
    "lea_tauchcomputer": "a yellow and black wrist dive computer with a rubber strap",
    "siri_ratgeber": "a small hand-bound notebook with a linen cover titled in handwriting, pages full of notes about Corsican fishing, a pencil and a piece of net cord on top",
    "lola_vegemite": "a small glass jar of Australian Vegemite with a yellow lid",
    "alva_kastagnetten": "a pair of old dark wooden castanets with a faded red cord, lovingly repaired",
    "megan_crewkarte": "a simple wooden picture frame holding a handwritten card covered in many different signatures and one small doodle of a generator",
    "holm_lakritz": "a round tin of Norwegian salty liquorice, lid open, black diamond-shaped sweets",
    "toto_gennaro": "a small colourful painted statue of San Gennaro, a Neapolitan saint figurine",
    "yasin_goldbrille": "a pair of flashy gold-framed aviator sunglasses with gradient lenses",
    "elsa_strafzettelblock": "a ticket book bound in dark brown leather with embossed initials E.F., a pen clipped to it",
    "petru_tabak": "a pouch of dark pipe tobacco and an old wooden pipe",
    "casanova_kanone": "a party confetti cannon tube decorated with gold stars",
    "petrus_hammer": "a small old fisherman's hammer with a worn wooden handle",
    "leas_taucherbrille": "a used blue diving mask with a scratched strap",
    "elsas_taschenlampe": "a rugged black police duty flashlight",
    "rosis_handschuhe": "a pair of worn leather work gloves, oil stained",
    "totos_notizbuch": "a small greasy notebook full of hand-written prices and numbers, a pencil stub tucked in",
    "siris_halstuch": "a folded silk neck scarf with a pale blue wave pattern",
    "megans_manschetten": "a pair of black onyx cufflinks with small golden anchors in an open velvet box",
    "lolas_band": "a colourful woven friendship bracelet with small wooden beads",
    "sophias_lesezeichen": "a pressed-flower bookmark laminated with a thin ribbon",
    "petrus_messer": "an old fisherman's knife with a bone handle and a curved blade",
    "plektrum": "a single tortoiseshell guitar pick on a thin leather cord",
    "elsas_abzeichen": "an embroidered navy coast guard patch with a gold anchor, no readable text",
    "netzknoten": "a piece of old fishing net tied in a complicated knot, blue and green twine",
    "ersatzteilkiste": "an open wooden crate of assorted spare parts, screws, gaskets, cable lugs and small tools",
    "energieriegel": "three homemade oat and honey energy bars wrapped in baking paper and string",
    "lolas_pesto": "a jar of very green homemade pesto with a basil leaf on top",
    "frischer_fang": "a bucket of fresh silver fish with a few ice cubes",
    "kuehlakkus": "four blue cooling packs stacked",
    "alvas_schluessel": "an old brass key on a red silk cord",
    "limoncello_kiste": "a wooden crate of unlabeled yellow limoncello bottles in straw",
    "taschen": "three suspiciously cheap designer-looking handbags stacked, logos blurred",
    "muschelkrone": "a homemade crown made of seashells and lots of glitter",
    "siris_karte": "a small hand-written thank-you card with a pressed seagrass leaf glued on",
    "siris_haarband": "a soft pale blue hair ribbon",
    "drohnen_propeller": "a single black drone propeller blade, slightly chipped",
    "goldfisch": "a single orange goldfish swimming in a clear plastic bag of water tied with a red string, a fairground prize",
    "muschelkette_kinder": "a homemade necklace of small seashells and colourful plastic beads on a string, slightly uneven, made by children",
    "wollmuetze": "a hand-knitted wool beanie with a traditional Norwegian pattern in navy and cream",
    "pinup_magazin": "a vintage Italian men's magazine lying on the linen, the cover shows a beautiful topless pin-up woman in a 1970s style photo, glossy paper, slightly dog-eared, no readable text",
    "messing_anker": "a small rusty brass anchor keyring with a bit of seaweed",
    "bauchnabelpiercing": "a silver belly button piercing with a tiny dangling seashell charm, lying on a small velvet pad",
    # Lolas Kombuese (Snacks und Desserts)
    "fairy_bread": "triangles of white toast with butter covered in colourful hundreds-and-thousands sprinkles on a small plate",
    "lamingtons": "four square lamington sponge cakes coated in chocolate and desiccated coconut",
    "pavlova": "a small pavlova meringue topped with whipped cream, fresh figs and myrtle berries",
    "anzac": "a small stack of golden Anzac oat biscuits",
    "vegemite_schnecken": "golden cheese and vegemite pastry scrolls on baking paper",
    "tim_tam_slam": "chocolate biscuits next to a mug of hot cocoa, one biscuit dipped and bitten at both ends",
    "ocean_popcorn": "a paper bowl of popcorn sprinkled with sea salt and shimmering blue and gold edible glitter",
    "kevins_rache": "iced sugar cookies shaped like seagulls, one with its head bitten off",
    "rote_gruetze": "a glass bowl of red berry compote with vanilla custard poured over it",
    "madeleines": "a row of golden lavender madeleines with a sprig of lavender",
    "cannoli": "two Sicilian cannoli filled with ricotta and a small cookie shaped like a wrench",
    "plankton_gelee": "a glowing bright blue jelly in a glass, translucent, with tiny sparkles inside",
    "seegras_chips": "a bowl of crispy green seaweed chips with lime wedges",
    "protein_pancakes": "a sad stack of dry protein pancakes with a scoop of protein powder beside it, no syrup",
    "ghost_brownies": "dark chocolate brownies with a red ghost pepper chilli on top, a warning flag stuck in one",
    "fiadone": "a slice of Corsican fiadone cheesecake with lemon zest",
    "tiramisu_martini": "a tiramisu in a martini glass dusted with cocoa and three coffee beans",
    "unit01_muffins": "pitch-black charcoal muffins that look like soot, one broken open showing a vanilla inside",
    "mango_sorbet": "a scoop of bright orange mango sorbet with a sprinkle of red chilli flakes in a small glass",
    "space_cake": "a slice of dense chocolate cake on a plate decorated with tiny edible stars and a single green leaf, cosmic and a little suspicious",
    "brownie_calm": "a fudgy brownie square on baking paper with a tiny hand-drawn captain's hat flag stuck in it",
    "toastie": "a golden toasted cheese and fig sandwich cut diagonally, cheese melting out, late-night snack",
    # Ducs Kueche (Gerichte, selbst gekocht)
    "bun_rieu": "a steaming bowl of Vietnamese bun rieu, crab and tomato noodle soup with fried tofu, a side plate of fresh herbs, bean sprouts and lime wedges",
    "thit_kho": "a clay pot of Vietnamese thit kho, glossy caramelized braised pork belly with halved boiled eggs in dark sauce, a small bowl of white rice beside it",
    "bibimbap": "a hot stone bowl of Korean bibimbap, rice topped with neatly arranged vegetables, beef and a fried egg yolk in the centre, a dab of red gochujang",
    "summer_rolls": "four fresh Vietnamese summer rolls in translucent rice paper with shrimp, herbs and vermicelli, a small bowl of peanut hoisin dipping sauce",
    "ramen": "a deep bowl of ramen with rich broth, noodles, a halved soft-boiled egg, sliced chashu pork, nori and spring onions, chopsticks resting on the rim",
    "chili_noodles": "a bowl of chili oil noodles glistening red, topped with crushed peanuts, sesame and spring onions, chopsticks beside it",
    "bouillabaisse": "a wide bowl of Provencal bouillabaisse, saffron fish stew with mussels and white fish, toasted bread slices with rouille on the side",
    "bolognese": "a plate of spaghetti bolognese with rich meat sauce, grated parmesan and a basil leaf, a fork twirled into the pasta",
    "pytt_i_panna": "a black cast iron pan of Swedish pytt i panna, diced fried potatoes, sausage and onion, topped with a fried egg and pickled beetroot",
    "fiskesuppe": "a white ceramic bowl of Norwegian fiskesuppe, a creamy pale fish soup with chunks of pink salmon and white fish, diced carrot and leek, topped with fresh dill sprigs, a polished silver spoon and a folded linen napkin beside it",
    # Yacht-Waren fuer Totos Ankauf (module\<mid>\modul.json "yachtware")
    "champagne": "an open wooden crate holding six bottles of champagne with gold foil necks, straw packing between the bottles",
    "tender_prop": "a single polished bronze three-blade boat propeller lying flat, smooth curved blades, a solid closed hub",
    "teak_loungers": "two classic teak wood deck sun loungers standing side by side, seen from a high three-quarter angle with their full length visible, a raised back rest and a long flat reclining seat, warm honey-coloured oiled wood made of smooth solid boards, a thin cream cushion on each",
    "bathrobes": "a neat stack of six folded white fluffy cotton bathrobes, a white satin ribbon tied around the stack",
    "lauchsuppe": "a rustic bowl of Cullen skink, a thick creamy Scottish soup with flakes of smoked haddock, soft potato chunks and chopped parsley, a polished spoon and a folded linen napkin beside it",
    "baguettes": "two golden crusty French baguettes on a wooden board, one broken open showing the soft crumb",
})
# Foto-Andenken und Screenshot (26.10.2026, Duc: Bilder fuer die Keepsake Box): Gegenstand statt Person
MOTIV.update({
    "holms_foto": "an old faded colour photograph print with a white border and one bent corner, the photo shows a rusty "
                  "red cargo freighter moored in a grey Norwegian fjord harbour under low clouds, seen from far away",
    "rosis_foto": "a smartphone lying face down, a scratched dark red phone case with a small oil smudge and a tiny "
                  "wrench sticker on the back, a single red lipstick kiss mark on the case",
    "megan_screenshot": "a smartphone lying flat with its screen glowing, the screen shows an ornate golden Venetian "
                        "masquerade mask with filigree on black velvet, nobody wearing it",
    # Halsbaender der Tiere sind silbern (Duc 26.10.2026)
    "control_chip": "a small black square microchip module with a blinking red LED, half fused into a broken piece of a "
                    "heavy brushed silver metal animal collar with a hinge, a few tawny lion hairs caught in the hinge, "
                    "short cut wires sticking out",
})
# Kampf-Verbrauchsgegenstaende (26.10.2026, Moral-Runde: Geschenke der Crew). Duc: "hochkant, wenn es passt" - nur was
# auch in echt steht (Getraenke, Flaschen, Dosen, Granaten, Binde) steht im Bild; was liegt, liegt natuerlich quer.
# Trypophobie: glatte, geschlossene Flaechen (keine Lochung am Pflaster, kein Lautsprechergitter, ruhige Crema).
MOTIV.update({
    "plaster": "a single plain beige fabric adhesive plaster strip with rounded ends and a smooth white pad in the middle, "
               "lying flat at a slight diagonal, completely smooth plain surface",
    "bandage": "a rolled up white elastic gauze bandage with a small metal clip, standing upright on its round end, "
               "a short loose end hanging down, smooth soft woven fabric",
    "verbandskasten": "a closed olive green military first aid pouch made of sturdy canvas fabric, wider than tall, "
                      "lying flat in landscape orientation, a sewn-on white square patch with a bold red cross on the "
                      "flap, a black zip along the top and a short black fabric carrying strap, soft padded fabric",
    "espresso_single": "a single small white porcelain espresso cup on a white saucer, the coffee covered by a perfectly "
                       "uniform velvety golden-brown crema like smooth satin, seen from above, the handle pointing down",
    "espresso": "a doppio, a double espresso served in a small clear glass tumbler standing upright, seen from a high "
                "three-quarter angle so the full height is visible, dark coffee topped with a perfectly uniform "
                "velvety layer of golden crema like smooth satin, a small silver spoon lying beside the glass",
    "americano": "a tall white ceramic mug of black americano coffee standing upright, seen from a high three-quarter "
                 "angle so the full height of the mug is visible, smooth dark coffee surface, a thin curl of steam",
    "mate": "a round dried calabash mate gourd with a smooth polished honey-brown surface and a polished silver drinking "
            "straw standing straight up in it, seen from the side at a low angle so only the smooth outside of the "
            "gourd and the straw are visible, a smooth leather band around the gourd",
    "green_tea": "a tall clear glass of pale green tea standing upright all alone, seen from a high three-quarter angle, "
                 "two large whole green tea leaves floating calmly in the clear tea",
    "duct_tape": "exactly one single thick roll of silver grey duct tape lying flat on its side, all alone with "
                 "nothing else next to it, the tape neatly wound, smooth glossy tape surface",
    "whetstone": "a long rectangular solid grey sharpening whetstone, one even shade of slate grey, lying flat with "
                 "its long side running up and down the frame, smooth fine matte stone surface",
    "cooling_spray": "a slim white aerosol spray can with a pale blue cap and a light frosty mist around the nozzle, "
                     "a large pale blue snowflake ice crystal symbol printed on the can, lying with its long side "
                     "running up and down the frame, the cap at the top, smooth can",
    "dog_food": "a single open round tin can of dog food standing upright, seen from a high three-quarter angle, "
                "the peeled-back metal lid curled beside it, filled to the top with large glossy chunks of meaty dog "
                "food in rich brown gravy, a smooth paper label in warm red and cream with a simple painted bone symbol",
    "megaphone": "a white and orange handheld megaphone lying on its side, seen from the side, the smooth closed "
                 "outside of the cone pointing to the right, the grip and trigger hanging down underneath",
    "smoke_pot": "a squat matte olive green metal smoke canister with a pull ring on top, standing upright, a simple "
                 "white cloud symbol painted on the front, a thick billowing column of soft pale grey smoke pouring "
                 "up from the top, smooth plain metal",
    "antidote": "a small brown glass vial with a black rubber dropper top, standing upright, a sprig of fresh rosemary "
                "and a sprig of myrtle lying beside it, smooth glass",
    # Ein Waffenpflege-Item je Waffenart (Duc 27.10.2026): der graue "whetstone" ist der fuer Messer
    "whetstone_blue": "a long rectangular solid sharpening whetstone in one even shade of deep slate blue, lying flat "
                      "with its long side running up and down the frame, smooth fine matte stone surface",
    "whetstone_red": "a long rectangular solid sharpening whetstone in one even shade of deep brick red, lying flat "
                     "with its long side running up and down the frame, smooth fine matte stone surface",
    "spikes": "a wide strap-on band of thick black leather covered with a dense ring of long sharp pointed steel spikes, "
              "two leather straps with steel buckles to fasten it around the head of a club, lying flat with its long "
              "side running up and down the frame, smooth polished steel spikes",       # Duc: Stacheln zum Anschnallen
    "match_ammo": "a small closed dark green cardboard box of shotgun shells standing upright, three shiny red shotgun "
                  "shells with polished brass bases standing upright in a neat row in front of it, smooth surfaces",
    # Akt 2: je Zustand eine Granate - moderne, glatte Zylinder (keine geriffelte Ananas-Form)
    "grenade_fire": "a smooth cylindrical hand grenade with a glossy deep red body, a small orange flame symbol painted "
                    "on it, a steel lever and pull ring at the top, lying with its long side running up and down the frame",
    "grenade_water": "a smooth cylindrical hand grenade with a glossy deep blue body, a small white water drop symbol "
                     "painted on it, a steel lever and pull ring at the top, lying with its long side running up and down the frame",
    "grenade_shock": "a smooth cylindrical hand grenade with a glossy bright yellow body, a small black lightning bolt "
                     "symbol painted on it, a steel lever and pull ring at the top, lying with its long side running up and down the frame",
    "grenade_sleep": "a smooth round small hand grenade with a soft matte grey body, wrapped twice around the middle with bright blue tape, a small white crescent moon symbol painted on it, a simple steel pull ring on top",
    "grenade_flash": "a smooth cylindrical hand grenade with a glossy pure white body, a small golden sun symbol painted "
                     "on it, a steel lever and pull ring at the top, lying with its long side running up and down the frame",
    "grenade_concussion": "a smooth heavy cylindrical hand grenade with a matte dark grey steel body and a thick black "
                          "rubber band around the middle, a steel lever and pull ring at the top, lying with its long side running up and down the frame",
    "grenade_shrapnel": "a smooth cylindrical hand grenade with a matte dark olive green body and a thin red stripe, "
                        "a steel lever and pull ring at the top, lying with its long side running up and down the frame",
})
# Zweite Quelle ab Akt 2 (Duc 26.10.2026): Isabelles Kraeuter aus der Klosterapotheke, Frederico bringt sie morgens.
# Trypophobie: keine Bienenwabe, keine Bluetenstaende/Staubgefaesse in Nahsicht, keine Zitrusschale, dichte Krume.
MOTIV.update({
    "chestnut_honey": "a small round glass jar of dark amber chestnut honey standing upright, smooth clear glossy honey, "
                      "a square of cream wax paper tied over the lid with twine, a plain wooden honey dipper beside it",
    "cistus_compress": "a folded square linen compress tied with a thin cotton ribbon, a few pressed soft pink cistus "
                       "petals laid on top, lying flat, smooth plain fabric",
    "san_martinu_satchel": "an old cream linen apothecary satchel with a leather strap, lying flat in landscape "
                           "orientation, the flap closed with a dark red wax seal, a small embroidered green cross on "
                           "the flap, soft smooth fabric",
    "lavender_oil": "a small violet glass bottle of lavender oil with a cork stopper standing upright, a small blank "
                    "linen tag tied around its neck with twine, smooth glass",
    "rosemary_drops": "three hard amber honey sweets, each one individually wrapped in its own twist of cream wax "
                      "paper like a small candy, lying loosely apart, a single fresh rosemary sprig beside them",
    "cedrat_tonic": "a small slim glass bottle of pale golden citrus tonic with a swing top stopper standing upright, "
                    "a single smooth pale yellow ribbon of citrus peel curled beside it, smooth glass",
    "chestnut_cake": "a single thick slice of dark brown Corsican chestnut cake on a small plain smooth pure white plate, dense "
                     "smooth moist cut surface like fudge, a glossy sugar glaze on top, a small fork beside it",
})
KEIN_BILD = set()


def items_laden(mid):
    """Gegenstaende eines Moduls: eden_rise aus gegenstaende.json, alle anderen aus modul.json."""
    pfad = os.path.join(EDEN, "module", mid, "gegenstaende.json")
    if os.path.exists(pfad):
        items = {i["id"]: i for i in json.load(open(pfad, encoding="utf-8"))["items"]}
        modul = json.load(open(os.path.join(EDEN, "module", mid, "modul.json"), encoding="utf-8"))
        for yid, y in (modul.get("yachtware") or {}).items():      # Yacht-Waren fuer Totos Ankauf (25.10.2026)
            items.setdefault(yid, {"id": yid, "label": y["label"], "art": "yacht"})
        return items
    return json.load(open(os.path.join(EDEN, "module", mid, "modul.json"), encoding="utf-8"))["items"]


def post(pfad, daten):
    req = urllib.request.Request(COMFY + pfad, data=json.dumps(daten).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def get(pfad):
    return json.loads(urllib.request.urlopen(COMFY + pfad, timeout=30).read())


def graph(prompt, ziel_ordner, name, seed, nsfw=False):
    g = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": NSFW_PROFIL["unet"] if nsfw else UNET, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": NSFW_PROFIL["clip"] if nsfw else CLIP, "type": "krea2",
                                                     "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
    }
    model, clip = ["1", 0], ["2", 0]
    for i, (lora, staerke) in enumerate(NSFW_PROFIL["loras"] if nsfw else []):
        k = "L%d" % i
        g[k] = {"class_type": "LoraLoader", "inputs": {"model": model, "clip": clip, "lora_name": lora,
                                                       "strength_model": staerke, "strength_clip": staerke}}
        model, clip = [k, 0], [k, 1]
    g.update({
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": clip}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIV, "clip": clip}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": NSFW_PROFIL["steps"] if nsfw else 8, "cfg": 1.0,
                                                    "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0,
                                                    "model": model, "positive": ["4", 0], "negative": ["5", 0],
                                                    "latent_image": ["6", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "DucSave", "inputs": {"images": ["8", 0], "save_path": ziel_ordner, "filename_prefix": name,
                                                  "use_input_filename": False, "image_format": "PNG", "jpg_quality": 95,
                                                  "counter_style": "NONE", "show_preview": False, "overwrite": True}},
    })
    return g


def thumbnail(gross, ziel, iid, ziel_name=None):
    """1024er Original -> 320er WebP fuer die Anzeige."""
    with Image.open(os.path.join(gross, iid + ".png")) as im:
        im = im.convert("RGB")
        im.thumbnail((THUMB, THUMB), Image.LANCZOS)
        im.save(os.path.join(ziel, (ziel_name or iid) + ".webp"), "WEBP", quality=85, method=6)


def warten(auftraege, fertig):
    offen = dict(auftraege)
    t0 = time.time()
    while offen and time.time() - t0 < 60 * 30:
        time.sleep(2)
        for name, pid in list(offen.items()):
            h = get("/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                fertig(name)
                offen.pop(name)
    return offen


def bogen(var, iid, n):
    """Auswahlbogen 1..n nebeneinander."""
    from PIL import ImageDraw
    S = 400
    b = Image.new("RGB", (n * S, S + 40), (20, 20, 24))
    d = ImageDraw.Draw(b)
    for k in range(1, n + 1):
        p = os.path.join(var, "%s_v%d.webp" % (iid, k))
        if os.path.exists(p):
            b.paste(Image.open(p).convert("RGB").resize((S, S)), ((k - 1) * S, 0))
        d.text(((k - 1) * S + S // 2 - 4, S + 12), str(k), fill=(230, 220, 200))
    pfad = os.path.join(var, iid + ".jpg")
    b.save(pfad, quality=88)
    return pfad


def nsfw_an(iid):
    return "--turbo" not in sys.argv and ("--nsfw" in sys.argv or STANDARD_NSFW or iid in NSFW)


def arg(name, std=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) else std
    return std


def main():
    cfg = json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8-sig"))
    mid = arg("--modul") or cfg["modul"]                 # --modul eden_rise: Pool der Neufassung (17.10.2026)
    modul = {"items": items_laden(mid)}
    ziel = os.path.join(EDEN, "module", mid, "items")
    gross = os.path.join(ziel, "_gross")
    os.makedirs(gross, exist_ok=True)
    werte = {arg("--varianten"), arg("--waehle"), arg("--modul"), arg("--hintergrund")}
    nur = [a for a in sys.argv[1:] if not a.startswith("-") and a not in werte]
    var = os.path.join(ziel, "_varianten")
    if arg("--waehle"):                      # Variante uebernehmen
        k = int(arg("--waehle"))
        for iid in nur:
            shutil.copy2(os.path.join(gross, "%s_v%d.png" % (iid, k)), os.path.join(gross, iid + ".png"))
            thumbnail(gross, ziel, iid)
            print("uebernommen: %s Variante %d" % (iid, k))
        return
    try:
        get("/system_stats")
    except Exception:
        sys.exit("ComfyUI Krea2 laeuft nicht (Port 8189) - erst starten, dann nochmal.")
    if arg("--varianten"):                   # n Varianten zur Auswahl, aktuelles Bild bleibt
        n = int(arg("--varianten"))
        os.makedirs(var, exist_ok=True)
        for iid in nur:
            it = modul["items"].get(iid) or {"label": iid}     # Entwurf: Motiv steht schon in MOTIV, Item noch nicht im Modul
            nsfw = nsfw_an(iid)
            prompt = STIL.format(motiv=MOTIV.get(iid) or it["label"], hintergrund=HINTERGRUENDE[arg("--hintergrund", HINTERGRUND)])
            auftraege = [("%s_v%d" % (iid, k), post("/prompt", {"prompt": graph(prompt, gross, "%s_v%d" % (iid, k),
                                                                               random.randint(1, 2 ** 31), nsfw)})["prompt_id"])
                         for k in range(1, n + 1)]
            print("%s: %d Varianten eingereiht%s" % (iid, n, " (NSFW-Profil: BigLove + Real3 + Nsfw2)" if nsfw else ""))
            warten(auftraege, lambda name: (thumbnail(gross, var, name), print("fertig:", name)))
            print("Auswahl:", bogen(var, iid, n))
        return
    auftraege = []
    for iid, it in modul["items"].items():
        if it.get("art") == "beweis" or iid in KEIN_BILD:
            continue                         # Beweise stehen im Codex, Foto-Andenken nur im Epilog - ohne Bild
        if nur and iid not in nur:
            continue
        if not nur and os.path.exists(os.path.join(ziel, iid + ".webp")):
            continue
        motiv = MOTIV.get(iid) or it["label"]
        r = post("/prompt", {"prompt": graph(STIL.format(motiv=motiv, hintergrund=HINTERGRUENDE[arg("--hintergrund", HINTERGRUND)]), gross, iid, random.randint(1, 2 ** 31),
                                             nsfw_an(iid))})
        auftraege.append((iid, r["prompt_id"]))
        print("eingereiht: %-18s %s" % (iid, motiv[:70]))
    if not auftraege:
        print("Alle Items haben schon ein Bild. (Einzelne neu: Item_Bilder.bat <id> ...)")
        return
    offen = warten(auftraege, lambda iid: (thumbnail(gross, ziel, iid), print("fertig:     %s" % iid)))
    print("%d Bilder in %s%s" % (len(auftraege) - len(offen), ziel, (" - noch offen: %s" % ", ".join(offen)) if offen else ""))


if __name__ == "__main__":
    main()

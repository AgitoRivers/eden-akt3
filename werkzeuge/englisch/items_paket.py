# -*- coding: utf-8 -*-
r"""English package for the item catalogue (25.10.2026, Items session; STIL.md: everything the player sees is English).

NEU: item id -> (label, text). The German texts stay in gegenstaende_eden_rise.py as the source for the later German
mapping; once Duc approves, the builder writes the English text into gegenstaende.json and keeps the German under "de".

    python werkzeuge\englisch\items_paket.py            -> docs\abnahme\englisch_items.json (old | new, for text_abnahme.py)
    python werkzeuge\text_abnahme.py --serve docs\abnahme\englisch_items.json 8357
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))

NEU = {
    # ---------------------------------------------------------------- gifts
    "arancini": ("Arancini from the Bakery", ""),
    "olive_oil": ("Corsican Olive Oil", ""),
    "lolas_gewuerz": ("Lola's Spice Mix “Ocean Glitter”", ""),
    "tim_tams": ("Tim Tams from Alva's Bar", "The only Australian biscuits in all of Corsica. Lola cries a little."),
    "lolas_kekse": ("A Plate of Lola's Biscuits", "Megan doesn't eat sugar. Except these."),
    "feigen": ("Corsican Figs", ""),
    "proteinriegel": ("Protein Bar", ""),
    "franzbroetchen": ("Hamburg Cinnamon Roll (Homemade)", "Like in Hamburg. Almost. Lola helped."),
    "canistrelli": ("Aniseed Canistrelli", "Corsican biscuits that keep forever."),
    "myrtle": ("Myrtle Liqueur", ""),
    "single_malt": ("Islay Single Malt", ""),
    "limoncello": ("Homemade Limoncello", ""),
    "cap_corse": ("Cap Corse Aperitif", ""),
    "pink_pearl": ("Pink Pearl on a Fine Chain", ""),
    "designer_perfume": ("Designer Perfume", ""),
    "shell_anklet": ("Shell Anklet", ""),
    "herzbrille": ("Heart-Shaped Diva Sunglasses", ""),
    "goldkette": ("Thick Gold Chain (Probably Real)", ""),
    "designer_sonnenbrille": ("Designer Sunglasses", ""),
    "silberring": ("Slim Silver Ring from the Market", ""),
    "torque_wrench": ("Professional Torque Wrench", ""),
    "dive_torch": ("Dive Torch", ""),
    "moka": ("Neapolitan Moka Pot", ""),
    "selfie_stick": ("Carbon Selfie Stick", ""),
    "polbrille": ("Polarised Sunglasses", ""),
    "schweizer_messer": ("Pocket Knife", ""),
    "fountain_pen": ("Fountain Pen", ""),
    "notebook": ("Leather Notebook", ""),
    "gedichtband": ("Second-Hand Book of Poems", ""),
    "almanac": ("Nautical Almanac", ""),
    "old_chart": ("Old Chart of the West Coast", ""),
    "pinup_magazin": ("Men's Magazine with a Pin-Up", "An Italian magazine with a beautiful, half-naked woman on the cover. Totò reads it “for the articles”."),
    "ducs_gedicht": ("Duc's Poem about the Sea", ""),
    "muschelkette_kinder": ("Homemade Shell Necklace with Beads", "Made by the village children, a little crooked. Siri puts it on straight away."),
    "pretty_shell": ("A Beautiful Shell", ""),
    "seeglas": ("Green Sea Glass", ""),
    "alvas_rose": ("Alva's Rose", ""),
    "wool_socks": ("Hand-Knitted Wool Socks", ""),
    "wollmuetze": ("Wool Hat with a Nordic Pattern", ""),
    "candles": ("Scented Candles “Maquis”", ""),
    "messing_anker": ("Brass Anchor Keyring", "Rusty, fished out of the bay."),
    "macchia_strauss": ("Bouquet from the Macchia", "Wild myrtle and rosemary from the hillside."),
    "korallenzweig": ("Small Branch of Coral (Beach Find)", ""),
    "bauchnabelpiercing": ("Belly Button Piercing with a Shell", ""),
    "eden_cap": ("Eden Group Cap", ""),
    "goldfisch": ("Goldfish in a Water Bag", "From a stall at the Festa. Lea names it immediately, somehow."),
    "konfetti": ("Bag of Confetti", ""),
    "schaerpe": ("Glitter Sash “Miss Cala d'Orsu”", ""),
    "faecher": ("Flamenco Fan", ""),
    "lichterkette": ("Solar Fairy Lights", ""),
    "ukulele": ("Second-Hand Ukulele", ""),
    "massage_oil": ("Neroli Massage Oil", ""),
    "silk_blindfold": ("Silk Blindfold", ""),
    "silk_kimono": ("Silk Kimono", ""),
    "massage_candle": ("Massage Candle with Warming Oil", ""),
    "stockings": ("Lace-Top Hold-Up Stockings", ""),
    "satin_ties": ("Satin Bed Restraints", ""),
    "nipple_clamps": ("Nipple Clamps with a Chain", ""),
    "lingerie": ("Champagne Lace Lingerie", ""),
    "plush_cuffs": ("Plush Handcuffs", ""),
    "eden_wave": ("Vibrator “Eden Wave”", ""),
    "jeweled_plug": ("Jewelled Butt Plug", ""),
    "flamenco_dessous": ("Ruffled Lingerie", "Red and black, from Alva's own stock under the counter."),
    # ---------------------------------------------------------------- unique gifts
    "chiara_tasse": ("A Cup Just for Her", "Hand-painted in Petru's workshop, with her name on it. For her, not for the guests. Chain: Petru + Lola."),
    "rosi_schild": ("Workshop Sign “Scuderi & Figlie”", "Carved from driftwood by Petru. For the workshop she wants to have one day."),
    "sophia_fueller": ("A Pen with Her Own Name", "Engraved with Sophia Moore, not with any other name. For what she wants to write herself."),
    "lea_tauchcomputer": ("Dive Computer", "For her own plans, safely planned. Chain: Elsa + Totò."),
    "siri_ratgeber": ("Guide: The Art of Fishing in Corsica", "From Petru's stories, bound by hand. For her father."),
    "lola_vegemite": ("A Jar of Vegemite", "From Alva's secret stash. Lola calls it home in brown."),
    "alva_kastagnetten": ("Her Grandmother's Castanets", "Repaired by Petru. Chain: Alva + Petru."),
    "megan_crewkarte": ("A Card Signed by the Whole Crew", "Framed. None of it can be bought."),
    "holm_lakritz": ("A Tin of Norwegian Salt Liquorice", "Bring-me job: Elsa takes it to the hospital."),
    "toto_gennaro": ("San Gennaro Figurine from Naples", "Chain: the cousin from Bastia + Alva."),
    "yasin_goldbrille": ("Gold Sunglasses “Monaco”", ""),
    "elsa_strafzettelblock": ("Leather-Bound Ticket Book", "With her initials. She laughs out loud for the first time."),
    "petru_tabak": ("Pipe Tobacco “Bastia Noir”", "Bring-me job: only Totò can get it."),
    "casanova_kanone": ("Confetti Cannon", "For the Festa. She will aim it at the yacht."),
    # ---------------------------------------------------------------- attribute items
    "holm_compass": ("Holm's Brass Compass", "At the farewell, from Holm's trust 2. Her father's compass."),
    "petrus_hammer": ("Petru's Little Hammer", ""),
    "leas_taucherbrille": ("Lea's Old Dive Mask", ""),
    "elsas_taschenlampe": ("Elsa's Service Torch", ""),
    "rosis_handschuhe": ("Rosi's Workshop Gloves", ""),
    "totos_notizbuch": ("Totò's Notebook of Prices", ""),
    "siris_halstuch": ("Siri's Silk Neckerchief", ""),
    "megans_manschetten": ("Megan's Cufflinks", "Black onyx, a golden anchor. From Megan's trust 3 in the Eden Shop."),
    "lolas_band": ("Lola's Friendship Bracelet", ""),
    "sophias_lesezeichen": ("Sophia's Bookmark", ""),
    # ---------------------------------------------------------------- lucky charms
    "multitool": ("Multitool", ""),
    "lockpicks": ("Lock Pick Set", ""),
    "binoculars": ("Binoculars", ""),
    "petrus_messer": ("Petru's Old Fishing Knife", ""),
    "aftershave": ("Aftershave “Bastia”", ""),
    "plektrum": ("Lola's Plectrum", ""),
    "megan_screenshot": ("Wrong Chat", "She says it was a mistake. Megan McAllister doesn't make mistakes. Once a day: advantage on Charm with Megan."),
    "lucky_coin": ("Lucky Coin from Alva", ""),
    "elsas_abzeichen": ("Badge of the Gendarmerie Maritime", ""),
    "tarot": ("Tarot Cards", ""),
    "netzknoten": ("Petru's Net Knot", ""),
    # ---------------------------------------------------------------- resources
    "diesel_canister": ("Can of Diesel", "At Alva's, one can a day at most, and dearer than at Totò's."),
    "used_battery": ("Used Boat Battery", ""),
    "panel_cleaner": ("Solar Panel Cleaner", ""),
    "ersatzteilkiste": ("Box of Spare Parts", "Screws, seals, cable lugs. Rosi beams."),
    "espresso": ("Double Espresso", "In a fight: +3 stamina, but your hands shake: parry window −10 % this round. Quick: costs no turn."),
    "energieriegel": ("Lola's Energy Bar", ""),
    "lolas_pesto": ("Lola's “Special Pesto”", ""),
    "frischer_fang": ("Fresh Catch", ""),
    "kuehlakkus": ("Ice Packs from the Village", "The supplies last a day longer when power runs low."),
    "rose_festa": ("The Mayor's Rose", "From Madame Casanova's hair, after the flamenco. Used once: Desire +6 with every woman."),
    # ---------------------------------------------------------------- parts
    "ersatzzellen": ("Spare Cells for the House Battery", "Two lithium cells, used, tested."),
    "relais": ("Compressor Relay", ""),
    "messingbuchstaben": ("Brass Letters", ""),
    "holzleim": ("Pot of Bone Glue", ""),
    "eichenbrett": ("An Old Oak Board", ""),
    "tonerde": ("A Sack of Clay", ""),
    "uhrenbatterie": ("Button Cell", ""),
    "goldfarbe": ("Gold Paint and a Fine Brush", ""),
    "safran": ("Real Saffron", ""),
    "buchbinde_leinen": ("Bookbinding Linen", ""),
    "netzgarn": ("Roll of Net Twine", ""),
    "bilderrahmen": ("A Simple Picture Frame", ""),
    "armband": ("Silicone Strap", ""),
    "fueller_rohling": ("Pen Blank for Engraving", ""),
    "antennenkabel": ("Antenna Cable, Seawater-Proof", ""),
    # ---------------------------------------------------------------- tools, combat, materials
    "werkzeugkoffer": ("Toolbox", "Advantage on repair jobs (or +2 if your craft already gives advantage)."),
    "kochmesser": ("Japanese Chef's Knife", "Advantage on cooking jobs (or +2 if your cooking already gives advantage)."),
    "verbandskasten": ("First Aid Kit", "In a fight: heals 40 % of your HP and stops bleeding and burning."),
    # combat consumables (Duc + Brain Trust 27.10.2026)
    "plaster": ("Plaster", "In a fight: heals 10 % of your HP and stops bleeding. Quick: costs no turn."),
    "bandage": ("Bandage", "In a fight: heals 25 % of your HP and stops bleeding."),
    "cooling_spray": ("Cooling Spray", "In a fight: puts out every flame on you, and you can't catch fire for 2 rounds. Quick: costs no turn."),
    "smoke_pot": ("Smoke Pot", "In a fight: their next attack hits only smoke, and next turn you can run without a roll (not from bosses)."),
    "antidote": ("Herbal Tincture", "Isabelle's remedy from the monastery pharmacy. In a fight: ends every bad state on you."),
    "espresso_single": ("Espresso", "In a fight: +2 stamina. Quick: costs no turn."),
    "americano": ("Americano", "In a fight: +1 stamina every round for 4 rounds. Quick: costs no turn."),
    "mate": ("Mate", "In a fight: clears your head of stun and blindness, +1 stamina."),
    "green_tea": ("Green Tea", "In a fight: parry window +15 % for 3 rounds. Quick: costs no turn."),
    "dog_food": ("Dog Food", "In a fight, thrown at an animal: it eats instead of biting, skips a round and loses 4 composure."),
    "megaphone": ("Megaphone", "In a fight: a human loses 5 composure, an animal is exhausted for 2 rounds."),
    "duct_tape": ("Duct Tape", "In a fight: you patch your jacket, protection +2 for the rest of the fight."),
    "whetstone_blue": ("Blue Whetstone", "For sabres: +3 damage for 5 rounds. Use it before a fight or during one."),
    "whetstone": ("Grey Whetstone", "For knives: +3 damage for 5 rounds. Use it before a fight or during one."),
    "whetstone_red": ("Red Whetstone", "For the boar spear: +3 damage for 5 rounds. Use it before a fight or during one."),
    "spikes": ("Spikes", "For blunt weapons: +3 damage for 5 rounds. Use it before a fight or during one."),
    "match_ammo": ("Match Ammo", "For the rifle: +3 damage for 5 rounds. Use it before a fight or during one."),
    "grenade_fire": ("Fire Grenade", "One of Rosi's home-made grenades. In a fight: 12 % of the enemy's HP straight through armour, and it burns (2 stacks)."),
    "grenade_water": ("Water Grenade", "Rosi filled it from an old fire extinguisher. In a fight: 12 % of the enemy's HP straight through armour, and it's wet."),
    "grenade_shock": ("Shock Grenade", "Two battery cells and a lot of tape. In a fight: 12 % of the enemy's HP straight through armour, and it's charged. On a wet enemy: short circuit."),
    "grenade_sleep": ("Sleep Grenade", "A vet's sedative in a soft shell. In a fight: only for collared animals. Below 10 % HP it always works. The more HP the animal has left, the less likely it is."),
    "grenade_flash": ("Flash Grenade", "No damage, just light. In a fight: the enemy is blinded for a round and its next blow does half damage."),
    "grenade_concussion": ("Concussion Grenade", "Heavy, and it means it. In a fight: 12 % of the enemy's HP straight through armour, and it's shaken (armour gone)."),
    "grenade_shrapnel": ("Shrapnel Grenade", "Packed with boat nails. In a fight: 18 % of the enemy's HP straight through armour, and it bleeds. Useless against machines."),
    "steel_plate": ("Steel Plate", "A steel plate for Rosi's workshop: the first upgrade for a jacket or Gemelli."),
    "titanium_plate": ("Titanium Plate", "A titanium plate for Rosi's workshop: the second upgrade for a jacket or Gemelli."),
    "jade": ("Jade", "A stone for Rosi: it replaces Terremoto's base stone (first upgrade)."),
    "topas": ("Topaz", "A stone for Rosi: it replaces Le Large's base stone (first upgrade)."),
    "aquamarin": ("Aquamarine", "A stone for Rosi: it replaces Riposte's base stone (first upgrade)."),
    "amethyst": ("Amethyst", "A stone for Rosi: it replaces Sussurro's base stone (first upgrade)."),
    "smaragd": ("Emerald", "A precious stone for Rosi: Terremoto's final stone (second upgrade)."),
    "rubin": ("Ruby", "A precious stone for Rosi: Le Large's final stone (second upgrade)."),
    "saphir": ("Sapphire", "A precious stone for Rosi: Riposte's final stone (second upgrade)."),
    "opal": ("Opal", "A precious stone for Rosi: Sussurro's final stone (second upgrade)."),
    "kupfer": ("Copper", "A copper ingot for Rosi: the first upgrade for Gemelli."),
    "silber": ("Silver", "A silver ingot for Rosi: the second upgrade for Gemelli."),
    # ---------------------------------------------------------------- keys
    "petru_key": ("Key to Petru's Workshop", ""),
    "festa_invite": ("The Mayor's Invitation to the Festa", ""),
    "alvas_schluessel": ("Key to Alva's Back Room", ""),
    # ---------------------------------------------------------------- contraband
    "sat_data": ("Satellite Data Package", "Phone features for one day."),
    "cuban_rum": ("Cuban Rum", ""),
    "cigars": ("Cohiba Cigars", ""),
    "limoncello_kiste": ("Crate of Limoncello without a Tax Stamp", ""),
    "taschen": ("Three “Designer” Handbags", ""),
    # ---------------------------------------------------------------- keepsakes
    "muschelkrone": ("Shell Crown of the Festa", ""),
    "rosis_foto": ("A Photo You Shouldn't Delete", ""),
    "siris_karte": ("Siri's Thank-You Card", ""),
    "holms_foto": ("Photo of Holm's First Command", ""),
    "siris_haarband": ("Siri's Hairband", ""),
    "drohnen_propeller": ("Propeller from Megan's Drone", ""),
    "ambrosius_keule": ("Brother Ambrosius' Golden Mace", "The abbot's golden mace with an ivory grip. Frederico hid it until someone good came."),
    "diary_page_1": ("Brother Ambrosius' Diary, Page 1", "“The animals don't flee from us. They flee from something inside themselves.”"),
    "diary_page_2": ("Brother Ambrosius' Diary, Page 2", "“I have seen the lion. He wears something on his neck that blinks. He suffers, as we do.”"),
    "agent_note": ("Torn Note", "A torn note, written to sound greedy. On the back, in pencil, someone has sketched the collar of a jacket with far more care than the note itself."),
    "tritons_dreizack": ("Triton's Trident (Siren Drop)", "A former weapon, later planned as the master weapon for Le Large."),
    # ---------------------------------------------------------------- Lola's galley: snacks
    "fairy_bread": ("Fairy Bread", "Buttered toast with hundreds and thousands. Lea thinks of birthdays."),
    "lamingtons": ("Lamingtons", "Chocolate squares rolled in coconut."),
    "pavlova": ("Pavlova with Figs and Myrtle", ""),
    "anzac": ("Anzac Biscuits", "Oat biscuits. Holm's biscuit for every night watch."),
    "vegemite_schnecken": ("Vegemite Cheese Scrolls", ""),
    "tim_tam_slam": ("Tim Tam Slam Set", "Biscuits and hot cocoa to suck through them."),
    "ocean_popcorn": ("Ocean Glitter Popcorn", ""),
    "kevins_rache": ("Kevin's Revenge", "Biscuits shaped like seagulls."),
    "rote_gruetze": ("Red Berry Pudding with Vanilla Sauce", ""),
    "madeleines": ("Lavender Madeleines", ""),
    "cannoli": ("Cannoli with a Spanner Biscuit", ""),
    "plankton_gelee": ("Glowing Plankton Jelly", ""),
    "seegras_chips": ("Seaweed Crisps with Lime", ""),
    "protein_pancakes": ("Protein Pancakes, No Fun Included", ""),
    "ghost_brownies": ("Ghost Pepper Brownies", ""),
    "fiadone": ("Fiadone", "Corsican cheesecake with lemon."),
    "tiramisu_martini": ("Espresso Martini Tiramisu", ""),
    "unit01_muffins": ("Unit-01 Muffins", "Black, and they taste of vanilla."),
    "mango_sorbet": ("Mango Chilli Sorbet", ""),
    "space_cake": ("Space Cake “Universe Edition”", ""),
    "brownie_calm": ("Brownie “Captain's Calm”", ""),
    "toastie": ("Midnight Toastie with Cheese and Fig", ""),
    # ---------------------------------------------------------------- dishes
    "bun_rieu": ("Bún Riêu", "Vietnamese noodle soup with crab and tomato."),
    "thit_kho": ("Thịt Kho", "Caramelised pork belly with egg, served with rice."),
    "bibimbap": ("Bibimbap", "Petru: “Why is it in a bowl?”"),
    "summer_rolls": ("Summer Rolls", "Fresh rice paper rolls with prawns and herbs."),
    "ramen": ("Ramen", "The broth needs patience. Rosi knows ramen from her manga."),
    "chili_noodles": ("Chilli Noodles", "Too hot for a seasick fleet manager."),
    "bouillabaisse": ("Bouillabaisse", "Provençal fish stew with rouille."),
    "bao_buns": ("Bao Buns", "Steamed buns with pork belly. Lola: “Fluffy clouds, Boss.”"),
    "fish_pie": ("Fish Pie", "Fish under a potato crust. Petru: “Hm.” That means: another one."),
    "bolognese": ("Spaghetti Bolognese", "Totò: “In Napoli, this is a crime.”"),
    "pytt_i_panna": ("Pyttipanne", "Fried potatoes with sausage, onion, a fried egg and beetroot."),
    "fiskesuppe": ("Fiskesuppe", "Norwegian fish soup with salmon, cream and dill."),
    "lauchsuppe": ("Cullen Skink", "Smoked haddock, potatoes and milk, the Scottish way. The only thing Megan keeps down at sea."),
    "baguettes": ("Baguettes", "Bread is the hardest discipline."),
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = json.load(open(os.path.join(EDEN, "module", "eden_rise", "gegenstaende.json"), encoding="utf-8"))
    alt = {i["id"]: i for i in d["items"]}
    fehlt = sorted(set(alt) - set(NEU))
    zuviel = sorted(set(NEU) - set(alt))
    gruppen = {}
    for iid, it in alt.items():
        if iid not in NEU:
            continue
        g = gruppen.setdefault(it.get("art") or "sonst", [])
        lab, txt = NEU[iid]
        g.append({"key": "item:%s.label" % iid, "feld": "Name", "alt": it["label"], "neu": lab})
        if it.get("text") or txt:
            g.append({"key": "item:%s.text" % iid, "feld": "Beschreibung", "alt": it.get("text", ""), "neu": txt})
    namen = {"geschenk": "Geschenke", "einzigartig": "Einzigartige Geschenke", "attribut": "Attribut-Gegenstände",
             "gluecksbringer": "Glücksbringer", "ressource": "Vorräte", "teil": "Besorgungen", "werkzeug": "Werkzeuge",
             "kampf": "Kampf und Werkstatt", "schluessel": "Schlüssel", "schmuggel": "Schmuggelware", "andenken": "Andenken",
             "snack": "Lolas Snacks", "gericht": "Gerichte"}
    spec = {"id": "englisch_items", "titel": "Englisch · Gegenstände (%d)" % len(NEU),
            "hinweis": "Namen und Beschreibungen aller Gegenstände auf Englisch (britische Schreibung). Pytt i panna wird "
                       "Pyttipanne (norwegisch, wegen K3/E-055). Deutsch bleibt in den Daten als Vorlage fürs spätere Mapping.",
            "gruppen": [{"titel": namen.get(g, g), "items": items} for g, items in gruppen.items()]}
    ziel = os.path.join(EDEN, "docs", "abnahme", "englisch_items.json")
    json.dump(spec, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%s: %d Gegenstände, %d Texte%s%s" % (ziel, len(NEU), sum(len(g["items"]) for g in spec["gruppen"]),
                                                ("; fehlt: " + ", ".join(fehlt)) if fehlt else "",
                                                ("; nicht im Katalog: " + ", ".join(zuviel)) if zuviel else ""))


if __name__ == "__main__":
    main()

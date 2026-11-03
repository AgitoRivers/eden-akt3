# -*- coding: utf-8 -*-
r"""Jacken-Charms von eden_rise (Duc 28.10.2026) -> module\eden_rise\charms.json + Bilder items\charm_<id>.webp.

    python werkzeuge\eden_rise\charms_eden_rise.py

Ein Charm je wichtiger Figur (Vertrauen 5), Fredericos Loewe ueber die volle Farm, A Mazzera's Hunting Charm als
Unikat der Berge. Bilder: abgenommen auf docs\abnahme\charms.html (werkzeuge\charm_bilder.py, die acht aelteren aus
waffen_bilder.py liegen schon als items\anhaenger_*.webp). Engine: kern\charms.py, Uebergabe: ereignisse_charms.py.

wirkung: {"attribute": {att: n}} gilt ueberall (Kampf, Szenen, Events, Jobs), {"kampf": {stat: n}} nur im Kampf -
dieselben Namen wie in kampf.chips_aktiv: schutz, parade, snack, heil_kampf, krit, ausdauer_max, dazu nur fuer
Charms spezial_schaden (Prozent), parade_serie (perfekte Paraden weniger bis Fassung -4), vorteil (Grund-Aktionen)."""
import json, os, sys

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
MOD = os.path.join(EDEN, "module", "eden_rise")
ABNAHME = os.path.join(EDEN, "docs", "abnahme", "charms")
THUMB = 320

A = lambda **kw: {"attribute": kw}
K = lambda **kw: {"kampf": kw}
# id: (Figur, Name, Beschreibung, Wirkung, Wirkungstext, Bild, Seltenheit)
CHARMS = {
    "chiara": ("chiara", "Chiara's Dolphin", "A grey-blue plush dolphin with a navy ribbon. It has more sea miles than you.",
               A(charm=1), "Charisma +1", "charm_chiara", "normal"),
    "lola": ("lola", "Lola's Kangaroo", "A sandy plush kangaroo with a joey in its pouch and a shell on a string. All the way from Brisbane.",
             A(strength=1), "Strength +1", "charm_lola", "normal"),
    "megan": ("megan", "Megan's Black Puma", "A sleek black plush puma with a gold anchor pin. Every predator needs a mascot.",
              A(cunning=1), "Cunning +1", "charm_megan", "normal"),
    "lea": ("lea", "Lea's Clownfish", "An orange and white plush clownfish with a big grin. Clownfish never leave their anemone.",
            A(empathy=1), "Empathy +1", "charm_lea", "normal"),
    "rosi": ("rosi", "Little Unit-01", "A white plush robot shaped like a tiny generator, sewn on a night shift. It doesn't explode. Probably.",
             A(courage=1), "Courage +1", "charm_rosi", "normal"),
    "toto": ("toto", "Totò's Raccoon", "A very round plush raccoon with a bandit mask, a gold chain and flip-flops. It was adopted.",
             A(cunning=1), "Cunning +1", "charm_toto", "normal"),
    "holm": ("holm", "Holm's Polar Bear", "A white plush polar bear in a captain's cap. Thirty years of watches, since Tromsø.",
             K(schutz=1), "Protection +1", "charm_holm", "normal"),
    "yamamoto": ("yamamoto", "Yamamoto's Turtle", "A green plush sea turtle with tiny sunglasses. Slow, but it sees everything.",
                 A(perception=1), "Perception +1", "charm_yamamoto", "normal"),
    "petru": ("petru", "Petru's Octopus", "A coral red plush octopus in a knitted fisherman's cap. Eight arms, and it catches what comes.",
              K(parade=10), "Parry window +10 %", "charm_petru", "normal"),
    "nonna": ("nonna", "Nonna's Hen", "A plump plush hen in a checked apron. She watches the kitchen, and now she watches you.",
              A(empathy=1), "Empathy +1", "charm_nonna", "normal"),
    "isabelle": ("isabelle", "Isabelle's Sheep", "A happy white plush sheep with lavender stitched on its chest. Lavender is for healing.",
                 K(heil_kampf=3), "Heals 3 after every fight", "charm_isabelle", "normal"),
    "alva": ("alva", "Alva's Little Bull", "A black plush bull calf with a red carnation from Sevilla behind one horn.",
             K(snack=2), "Snacks heal +2", "charm_alva", "normal"),
    "yasin": ("yasin", "Yasin's Falcon", "A round, fluffy plush falcon with a tiny gold chain. Limited edition. Only one exists.",
              K(krit=5), "Crit +5 %", "anhaenger_falke_neu", "normal"),
    "frederico": ("frederico", "Frederico's Black Lion", "A black plush lion cub with golden eyes and no collar. Nobody gets a collar anymore.",
                  A(strength=1, courage=1), "Strength +1 and Courage +1", "charm_frederico", "gold"),
    "jana": ("jana", "Not Strudel", "A white plush cat with blue eyes and a red and white scarf. It is definitely not Strudel.",
             A(courage=1), "Courage +1", "anhaenger_strudel", "normal"),
    "siri": ("siri", "Selma the Seal", "A white plush baby seal in a knitted Nordic hat. Been to every shoot, never on camera.",
             A(empathy=1), "Empathy +1", "anhaenger_robbe", "normal"),
    "sophia": ("sophia", "Sophia's Owl", "A brown plush owl with round glasses and a tiny book. It sees everything and says nothing.",
               A(perception=1), "Perception +1", "anhaenger_eule", "normal"),
    "elsa": ("elsa", "Elsa's Shepherd", "A plush German shepherd in a navy police cap. It has stared down three smugglers this year.",
             K(vorteil=["einschuechtern"]), "Advantage on Intimidate", "anhaenger_schaeferhund", "normal"),
    "maxwell": ("maxwell", "The Champion", "A muscular plush gorilla with sunglasses and a gold champion belt. It never skips breakfast.",
                K(spezial_schaden=20), "Special attacks +20 % damage", "anhaenger_gorilla", "normal"),
    "casanova": ("casanova", "The Mayor's Flamingo", "A pink plush flamingo in a ruffled flamenco dress. She never loses her composure.",
                 K(parade_serie=1), "Composure −4 after only 2 perfect parries", "anhaenger_flamingo", "normal"),
    "mazzera": (None, "A Mazzera's Hunting Charm", "A crescent of two boar tusks, raven feathers and a moonstone, bound with red "
                "thread. A dream hunter wore it, long before Dumenica.", K(ausdauer_max=1), "Stamina +1",
                "charm_mazzera", "unikat"),
}
# Neue Bilder aus der Abnahme (PNG 1024) -> items\<bild>.webp; die aelteren anhaenger_* liegen schon dort.
NEU_AUS_ABNAHME = {"charm_" + c: c for c in ("chiara", "lola", "megan", "lea", "rosi", "toto", "holm", "yamamoto", "petru",
                                               "nonna", "isabelle", "alva", "frederico", "mazzera")}
NEU_AUS_ABNAHME["anhaenger_falke_neu"] = "yasin"


def bilder():
    items = os.path.join(MOD, "items")
    for ziel, quelle in NEU_AUS_ABNAHME.items():
        with Image.open(os.path.join(ABNAHME, quelle + ".png")) as im:
            im = im.convert("RGB")
            im.thumbnail((THUMB, THUMB), Image.LANCZOS)
            im.save(os.path.join(items, ziel + ".webp"), "WEBP", quality=85, method=6)
    fehlt = [c[5] for c in CHARMS.values() if not os.path.isfile(os.path.join(items, c[5] + ".webp"))]
    if fehlt:
        sys.exit("Bilder fehlen: " + ", ".join(fehlt))


def bauen():
    bilder()
    out = {cid: {"figur": f, "label": l, "text": t, "wirkung": w, "wirkung_text": wt, "bild": b, "seltenheit": s}
           for cid, (f, l, t, w, wt, b, s) in CHARMS.items()}
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\charms_eden_rise.py - dort aendern.", "charms": out},
              open(os.path.join(MOD, "charms.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("charms.json:", len(out), "Charms")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    bauen()

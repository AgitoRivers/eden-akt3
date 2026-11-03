# -*- coding: utf-8 -*-
r"""Jacken-Charms (Duc 28.10.2026): ein Pluesch-Anhaenger je wichtiger Figur, Bilder zur Abnahme.

    python werkzeuge\charm_bilder.py              alle Charms ohne Bild rendern + Abnahmeseite schreiben
    python werkzeuge\charm_bilder.py lola chiara  nur diese neu (ueberschreibt)
    python werkzeuge\charm_bilder.py --seite      nur die Abnahmeseite neu schreiben

Gleicher Look wie die Gegenstandsbilder (item_bilder.py: Produktfoto auf Leinen, Krea2 auf Port 8189).
Ablage docs\abnahme\charms\<id>.png, Seite docs\abnahme\charms.json -> abnahme_seite.py.
Noch NICHT im Spiel: Item-Typ, Charm-Platz an der Jacke und Wirkung im Kampf fehlen (aufruestung.md)."""
import json, os, random, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, HIER)
import item_bilder as IB  # noqa: E402

ORDNER = os.path.join(EDEN, "docs", "abnahme", "charms")
SPEC = os.path.join(EDEN, "docs", "abnahme", "charms.json")
BASIS = ("a small cute plush {tier} keychain charm, soft smooth velvety fabric, simple embroidered eyes, a short loop "
         "of cord with a small brass ring at the top")

# id: (Figur, Tier/Motiv, Wirkung, Bedingung). Wirkung = genau eine; Attribute je Figur aus "schaetzt".
CHARMS = {
    "chiara":    ("Chiara", "dolphin in soft grey-blue, a tiny navy ribbon around its neck",
                  "Charisma +1 (wie bisher das Seepferdchen)", "Vertrauen im Plus"),
    "lola":      ("Lola", "kangaroo in warm sandy brown with a tiny joey peeking out of its pouch and a small shell on a string around its neck",
                  "Strength +1", "Vertrauen im Plus"),
    "megan":     ("Megan", "black puma, sleek jet black plush like a panther, calm green eyes and a tiny gold anchor pin on its chest",
                  "Cunning +1", "Vertrauen im Plus, kommt mit dem Versorgungsboot"),
    "lea":       ("Lea", "clownfish with soft orange and white stripes and a big friendly smile",
                  "Empathy +1", "Vertrauen im Plus"),
    "rosi":      ("Rosi", "super cute little round robot in soft white plush, a chubby rounded box body like a tiny generator, one big round glowing amber eye with a happy curve below it, rosy cheeks, short stubby legs, a tiny white exhaust pipe on top puffing a small soft heart-shaped cloud",
                  "Courage +1", "Vertrauen im Plus"),
    "toto":      ("Totò", "very chubby round raccoon with a big soft belly, the classic dark eye mask, a tiny gold chain around its neck and tiny flip-flops on its feet",
                  "Cunning +1", "Vertrauen im Plus"),
    "holm":      ("Holm", "polar bear, the whole bear standing on all four paws and facing the viewer straight from the front, wearing a tiny white captain's cap with a black peak",
                  "Schutz +1", "Vertrauen im Plus"),
    "yamamoto":  ("Yamamoto", "sea turtle with a smooth green shell and tiny round black sunglasses",
                  "Perception +1", "Vertrauen im Plus"),
    "petru":     ("Petru", "octopus in soft coral red with smooth plain tentacles curled up underneath and a tiny knitted fisherman's cap",
                  "Parade-Fenster +10 %", "Vertrauen im Plus"),
    "nonna":     ("Nonna", "plump brown hen wearing a tiny checked kitchen apron",
                  "Empathy +1", "Vertrauen im Plus"),
    "isabelle":  ("Isabelle", "super cute happy fluffy white sheep facing the viewer straight from the front, a big happy smile with closed smiling eyes, rosy cheeks, round chubby body, a small sprig of purple lavender embroidered in thread on its chest",
                  "Heilung nach dem Kampf +3", "Vertrauen im Plus"),
    "alva":      ("Alva", "small black bull calf with short soft horns and a red carnation tucked behind one horn",
                  "Snacks heilen +2 (wie bisher der Koala)", "Vertrauen im Plus"),
    "yasin":     ("Yasin", "very round and fluffy peregrine falcon chick, soft and squishy like a pillow, big dark eyes, a tiny gold chain",
                  "Krit +5 % (wie bisher)", "Vertrauen im Plus"),
    # Unikat der Berge (beute.md, Duc 28.10.): kein Pluesch, ein Jaegeramulett - MOTIV_GANZ statt BASIS
    "mazzera":   ("A Mazzera's Hunting Charm", "a striking dark hunter's talisman shaped like an open crescent moon, the opening pointing upwards like a smile: two curved pale ivory wild boar tusks "
                  "joined tip to tip into a crescent moon, the ivory etched with fine black spiral engravings, bound at the joints with "
                  "bright blood-red thread, a single smooth milky moonstone set in the middle, three glossy black raven feathers with a "
                  "blue-violet sheen fanning out below, hanging from a braided red cord with an old blackened silver ring",
                  "Ausdauer +1 (Leiste 8 → 9)", "Unikat der Berge, nicht verschenkbar"),
    "frederico": ("Frederico", "black lion cub with a soft fluffy dark mane and warm golden eyes",
                  "Strength +1 und Courage +1 (Gold)", "alle Ställe auf Nonnas Farm ausgebaut"),
}
MOTIV_GANZ = {"mazzera"}
SEIDE = {"seide_dunkel": "lying on softly draped deep black silk cloth with a subtle dark burgundy sheen in the folds, soft warm rim light, "
                         "deep calm shadows, elegant and minimal",
         "seide_hell": "lying on softly draped ivory silk cloth with gentle glossy folds, soft warm light, calm and minimal"}
IB.HINTERGRUENDE.update(SEIDE)
HINTERGRUND_EIGEN = {"mazzera": "seide_hell"}   # Duc 28.10.: Mondsichel auf heller Seide (Variante 2)
# Schon vorhanden (waffen_bilder.py CHARMS, Bilder module\eden_rise\items\_gross): nur auf der Seite gezeigt.
BESTAND = {"anhaenger_strudel": "jana", "anhaenger_robbe": "siri", "anhaenger_eule": "sophia",
           "anhaenger_schaeferhund": "elsa", "anhaenger_gorilla": "maxwell", "anhaenger_flamingo": "casanova"}
VERGLEICH = {"chiara": ("anhaenger_seepferdchen", "bisher: Seepferdchen"), "alva": ("anhaenger_koala", "bisher: Koala"),
             "yasin": ("anhaenger_falke", "bisher: Falke")}


def prompt(cid):
    motiv = CHARMS[cid][1] if cid in MOTIV_GANZ else BASIS.format(tier=CHARMS[cid][1])
    return IB.STIL.format(motiv=motiv, hintergrund=IB.HINTERGRUENDE[HINTERGRUND_EIGEN.get(cid, IB.HINTERGRUND)])


def seite():
    import waffen_bilder as WB
    gross = os.path.join(EDEN, "module", "eden_rise", "items", "_gross")
    items = []
    for cid, (figur, tier, wirkung, bed) in CHARMS.items():
        it = {"id": cid, "titel": "NEU %s – %s" % (figur, wirkung), "bild": os.path.join(ORDNER, cid + ".png"),
              "soll": "Anhänger: %s. Wirkung an der Jacke: %s. Bekommt man: %s." % (tier, wirkung, bed)}
        if cid in VERGLEICH:
            it.update(vergleich=os.path.join(gross, VERGLEICH[cid][0] + ".png"), vergleich_titel=VERGLEICH[cid][1])
        items.append(it)
    for iid in BESTAND:
        label, figur, wirkung, motiv = WB.CHARMS[iid]
        items.append({"id": iid, "titel": "BESTAND %s – %s" % (figur, wirkung), "bild": os.path.join(gross, iid + ".png"),
                      "soll": "%s (schon vorhanden). Wirkung: %s. Nur prüfen, ob es so bleibt." % (label, wirkung)})
    spec = {"id": "charms", "titel": "Jacken-Charms – Abnahme",
            "hinweis": "Ein Charm je Figur, ein Platz an der Jacke. NEU = heute gerendert, BESTAND = gab es schon. "
                       "Bitte Bild UND Wirkung prüfen (OK / Neu + Notiz).",
            "items": items}
    json.dump(spec, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, os.path.join(HIER, "abnahme_seite.py"), SPEC], check=True)


def main():
    if "--seite" in sys.argv:
        return seite()
    os.makedirs(ORDNER, exist_ok=True)
    wahl = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziele = wahl or [c for c in CHARMS if not os.path.exists(os.path.join(ORDNER, c + ".png"))]
    auftraege = {}
    for cid in ziele:
        g = IB.graph(prompt(cid), ORDNER, cid, random.randint(1, 2 ** 31), nsfw=True)
        auftraege[cid] = IB.post("/prompt", {"prompt": g})["prompt_id"]
    offen = IB.warten(auftraege, lambda n: print("fertig", n, flush=True))
    if offen:
        print("nicht fertig:", ", ".join(offen))
    seite()


if __name__ == "__main__":
    main()

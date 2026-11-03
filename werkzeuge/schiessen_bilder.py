# -*- coding: utf-8 -*-
r"""Ziele fuer Holms Schiesswette (Duc 30.10.2026): freigestellte Krea-Sprites zur Auswahl, je Ziel 3 Kandidaten.

    python werkzeuge\schiessen_bilder.py            fehlende Kandidaten erzeugen + Abnahme-Spec schreiben
    python werkzeuge\schiessen_bilder.py --spec     nur docs\abnahme\schiessen_ziele.json schreiben
    python werkzeuge\schiessen_bilder.py --nimm flasche=1,2,3 ton=2 ...    Gewinner ins Plugin kopieren (<ziel>.webp, weitere <ziel>2.webp, hoechstens 256 px)

Die Blendgranate ist ein eigenes Sprite: Das Plugin haengt sie unter die Moewe, so stimmt ihre Trefferzone genau."""
import json, os, random, sys, time

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import kochen_bilder as K  # noqa: E402

IB = K.IB
ORDNER = os.path.join(K.EDEN, "docs", "abnahme", "schiessen_ziele")
ROH = os.path.join(ORDNER, "_gross")
PLUGIN = os.path.join(K.EDEN, "client", "plugins", "eden-schiessen")
SPEC = os.path.join(K.EDEN, "docs", "abnahme", "schiessen_ziele.json")
HELL = K.GRUND
DUNKEL = "on a plain dark teal studio background, soft even light, a single subject, nothing else in the frame"
STIL = "Photograph of {motiv}, the entire object fully inside the frame with a wide empty margin on all sides, {grund}, photorealistic, sharp detail"
ZIELE = {
    "flasche": ("Flasche", HELL, [
        "a single empty dark green glass wine bottle standing upright, a faded cream paper label, seen straight from the side",
        "a single empty amber brown glass beer bottle standing upright, a torn paper label, seen straight from the side",
        "a single old pale green glass bottle standing upright with a cork in the neck and no label, seen straight from the side"]),
    "ton": ("Tontaube", HELL, [
        "a single bright orange clay pigeon shooting target, a shallow ceramic disc with ring grooves, tilted and seen from slightly above",
        "a single black clay pigeon shooting target with a bright orange rim, a shallow ceramic disc, tilted and seen from slightly above",
        "a single bright yellow clay pigeon shooting target, a shallow ceramic disc with ring grooves, tilted and seen from slightly above"]),
    "drohne": ("Drohne", HELL, [
        "a small matte black quadcopter drone with four rotors and two glowing red lights, hovering, seen from the side and slightly below",
        "a small dark grey military surveillance quadcopter with a camera under its body and red lights, hovering, seen from the side",
        "a compact black hexacopter drone with six small rotors and a red sensor eye, hovering, seen from the side"]),
    "moewe": ("Möwe", DUNKEL, [
        "a white and grey herring gull in flight with both wings raised high, seen from the side, the beak pointing right, the feet tucked in",
        "a white and grey herring gull gliding with spread wings, seen from the side, the beak pointing right, the feet tucked in",
        "a white and grey seagull in flight with wings half lowered, seen from the side, the beak pointing right, the feet tucked in"]),
    "granate": ("Blendgranate", HELL, [
        "a small military stun grenade standing upright, a matte grey metal cylinder with rows of round holes, a yellow band and a steel ring pin on top",
        "a small flashbang grenade standing upright, a dark olive metal cylinder with a white band, round vent holes and a steel ring pin on top",
        "a small black stun grenade standing upright, a short metal cylinder with vent holes, a bright yellow stripe and a ring pin on top"]),
}


def erzeugen():
    os.makedirs(ROH, exist_ok=True)
    lauf = {}
    for ziel, (_, grund, motive) in ZIELE.items():
        for n, motiv in enumerate(motive, 1):
            name = "%s_%d" % (ziel, n)
            if os.path.exists(os.path.join(ORDNER, name + ".png")):
                continue
            prompt = STIL.format(motiv=motiv, grund=grund)
            g = K.graph_mit_freistellung(prompt, ROH, name, random.randint(1, 2 ** 31))
            lauf[name] = (IB.post("/prompt", {"prompt": g})["prompt_id"], prompt, 1)
    print("eingereiht: %d" % len(lauf), flush=True)
    t0 = time.time()
    while lauf and time.time() - t0 < 60 * 45:
        time.sleep(3)
        for name, (pid, prompt, versuch) in list(lauf.items()):
            h = IB.get("/history/" + pid)
            if not (pid in h and h[pid].get("status", {}).get("completed")):
                continue
            ok = K.sprite_fertig(ROH, name, os.path.join(ORDNER, name + ".png"), letzter=versuch >= K.VERSUCHE)
            if not ok and versuch < K.VERSUCHE:
                g = K.graph_mit_freistellung(prompt, ROH, name, random.randint(1, 2 ** 31))
                lauf[name] = (IB.post("/prompt", {"prompt": g})["prompt_id"], prompt, versuch + 1)
                continue
            print("fertig: %s" % name, flush=True)
            lauf.pop(name)
    print("offen: %s" % (", ".join(lauf) or "nichts"))


def spec():
    items = []
    for ziel, (titel, _, motive) in ZIELE.items():
        for n in range(1, len(motive) + 1):
            items.append({"id": "%s_%d" % (ziel, n), "titel": "%s · Variante %d" % (titel, n),
                          "bild": os.path.join(ORDNER, "%s_%d.png" % (ziel, n)),
                          "soll": "Eine Variante je Ziel mit OK markieren. Im Spiel klein auf dem Meer, muss sofort lesbar sein."})
    json.dump({"id": "schiessen_ziele", "titel": "Holms Wette – Ziele",
               "hinweis": "Je Ziel genau ein OK. Die Blendgranate hängt im Spiel unter der Möwe.", "items": items},
              open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: %s (%d Bilder)" % (SPEC, len(items)))


def nimm(paare):
    for paar in paare:
        ziel, nummern = paar.split("=")
        for i, n in enumerate(nummern.split(",")):
            bild = Image.open(os.path.join(ORDNER, "%s_%s.png" % (ziel, n))).convert("RGBA")
            bild.thumbnail((256, 256), Image.LANCZOS)
            bild.save(os.path.join(PLUGIN, ziel + (str(i + 1) if i else "") + ".webp"), "WEBP", quality=90)
        print("uebernommen: %s" % paar)


def main():
    if "--nimm" in sys.argv:
        nimm(sys.argv[sys.argv.index("--nimm") + 1:])
        return
    if "--spec" not in sys.argv:
        erzeugen()
    spec()


if __name__ == "__main__":
    main()

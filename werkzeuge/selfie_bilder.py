# -*- coding: utf-8 -*-
r"""ABGELOEST am 27.10.2026: Die Spielbilder kommen jetzt aus Ducs abgenommenen Prompt-Studio-Selfies
(werkzeuge\selfie_webp.py, Daten werkzeuge\eden_rise\selfie_daten.json). --webp hier NICHT mehr laufen lassen - es wuerde
die neuen Bilder mit den alten Looks ueberschreiben.

Selfie-Events der Frauen (Duc 26.10.2026): je Frau 2 Raeume x 3 Nacktheitsgrade, gerendert mit den LoRAs ihres
Prompt-Studio-Presets (nur lesend, wie andenken_fotos.py).

    selfie_bilder.py                 alle 36 Bilder -> module\eden_rise\selfies\_roh\<frau>_<raum>_<stufe>.png
    selfie_bilder.py --webp          daraus die Spielbilder selfies\<name>.webp (1152 hoch, ausgeliefert, in Git)
    selfie_bilder.py chiara lola     nur diese Frauen
    selfie_bilder.py --prompt chiara Prompts zeigen, nichts rendern

Stufe 1 = knapp bekleidet, 2 = oben ohne, 3 = nackt. Das Event zeigt die Stufe nach Begehren (2/3/4+).
"""
import json, os, random, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import andenken_fotos as AF  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ZIEL = os.path.join(AF.EDEN, "module", "eden_rise", "selfies")
ROH = os.path.join(ZIEL, "_roh")
W, H = 896, 1152
STIL = ("Realistic amateur iPhone photo, slightly grainy, natural skin texture, natural light, candid and unposed, "
        "one single woman alone in the frame, no text, no watermark.")

FRAUEN = {
    "chiara": {
        "preset": "Yacht_Chiara",
        "look": "a 29-year-old German woman with light blue eyes, platinum blonde hair tied back in a high sleek "
                "ponytail with a few loose strands, large breasts, long legs, a confident grin",
        "raeume": {
            "nock": "standing on the open bridge wing of a superyacht at night, the brass railing behind her, a sky "
                    "full of stars over the dark sea, an old brass sextant in her free hand, taking a selfie at arm's length",
            "kabine": "a mirror selfie in her small crew cabin at night, an old navy naval officer's jacket hanging on "
                      "a hook, a brass sextant and a nautical exam book on the desk, warm reading lamp",
        },
        "stufen": ["wearing a tiny black bikini under her grandfather's old navy naval officer's jacket worn open",
                   "topless, only her grandfather's old navy naval officer's jacket hanging open off her shoulders "
                   "over her bare breasts, tiny black bikini bottoms",
                   "completely naked, her grandfather's naval jacket lying on the floor beside her feet"],
    },
    "sophia": {
        "preset": "Yacht_Sophia",
        "look": "a 28-year-old Cornish woman with light blue eyes, long layered honey blonde hair with lighter "
                "face-framing strands, large breasts, long legs, thin reading glasses, a soft knowing smile",
        "raeume": {
            "koje": "a selfie from above, lying in her crew bunk at two in the morning, a leather notebook and a pen "
                    "on the pillow beside her, a tiny reading light, rumpled white sheets",
            "achterdeck": "a selfie on the empty aft deck of a superyacht late at night, cream lounge cushions, soft "
                          "deck lights, the dark harbour behind her",
        },
        "stufen": ["wearing a thin champagne silk camisole and matching silk panties",
                   "topless, only champagne silk panties, one arm loosely across her bare breasts",
                   "completely naked, a white sheet only half over her hips"],
    },
    "lea": {
        "preset": "Yacht_Lea",
        "look": "a 23-year-old Cornish woman with light blue eyes, wet dark brown hair in one braided ponytail, "
                "large breasts, long legs, sun-kissed skin, an excited open grin",
        "raeume": {
            "garage": "a selfie in the tender garage of a superyacht at night after a dive, wet floor, scuba tanks "
                      "and fins along the wall, a green glow stick in her hand, water dripping from her",
            "plattform": "a selfie on the swim platform of a superyacht at night, the sea lit turquoise by underwater "
                         "lights behind her, wet teak boards",
        },
        "stufen": ["a black wetsuit peeled down to her waist, a tiny blue bikini top",
                   "topless, a black wetsuit peeled down to her hips, wet bare breasts",
                   "completely naked and wet, a black wetsuit lying on the floor next to her"],
    },
    "siri": {
        "preset": "Yacht_Siri",
        "look": "a 25-year-old Norwegian woman with light blue eyes, platinum blonde hair in a loose side fishtail "
                "braid over one shoulder, no makeup, freckles, a shy real smile",
        "raeume": {
            "vip": "a mirror selfie in a luxury VIP cabin on a superyacht, a big unmade bed, a round porthole, soft "
                   "morning light",
            "vordeck": "a selfie on the empty foredeck of a superyacht at sunrise, coiled ropes, pale pink sky over "
                       "a calm bay",
        },
        "stufen": ["wearing only an oversized hand-knitted navy wool sweater with little white stars, slipping off "
                   "one shoulder, bare legs",
                   "topless, holding the hand-knitted navy wool sweater with little white stars loosely against her "
                   "hips, bare breasts",
                   "completely naked, fully nude body from head to thighs, nothing on at all"],
    },
    "alva": {
        "preset": "Yacht_Alva",
        "look": "a curvy 35-year-old Corsican woman, big dark curly hair piled up loosely with a pencil stuck in "
                "it, dark eyes with black winged eyeliner, warm olive skin, gold hoop earrings, a knowing crooked grin",
        "raeume": {
            "bar": "a selfie sitting on the counter of an old village bar after closing time, chairs up on the tables, "
                   "a chalkboard full of names behind her, the warm glow of an old jukebox",
            "zimmer": "a mirror selfie in a small old bedroom above a bar, wooden shutters half open to the harbour at "
                      "night, an iron bed, a flamenco poster on the wall",
        },
        "stufen": ["wearing a short black silk slip dress",
                   "topless, a short black silk slip dress pulled down to her waist, bare breasts",
                   "completely naked, fully nude body, nothing on at all"],
    },
    "lola": {
        "preset": "Yacht_Lola",
        "look": "a 24-year-old Australian woman with light blue eyes, a small nose piercing, messy sun-bleached "
                "dark-blonde beach waves, lots of freckles, deep tan with bikini tan lines, slim surfer build, a big "
                "goofy grin",
        "raeume": {
            "kombuese": "a selfie in a stainless steel yacht galley at night, a bamboo steamer full of bao buns, "
                        "flour on the counter and on her skin",
            "koje": "a selfie in her small crew cabin, fairy lights over the bunk, napkin drawings pinned to the wall, "
                    "a surfboard sticker on the locker",
        },
        "stufen": ["wearing a tiny yellow bikini under an open chef's apron",
                   "topless, only a white chef's apron loosely around her waist, bare breasts with flour on them",
                   "completely naked, a white chef's apron lying on the counter beside her"],
    },
}


def prompt(frau, raum, stufe):
    f = FRAUEN[frau]
    return "A selfie of %s, %s. %s. %s" % (f["look"], f["stufen"][stufe - 1], f["raeume"][raum][0].upper() + f["raeume"][raum][1:], STIL)


def main():
    nur = [a for a in sys.argv[1:] if not a.startswith("-")] or list(FRAUEN)
    os.makedirs(ROH, exist_ok=True)
    if "--webp" in sys.argv:
        webp()
        return
    if "--prompt" in sys.argv:
        for frau in nur:
            for raum in FRAUEN[frau]["raeume"]:
                for st in (1, 2, 3):
                    print("%s_%s_%d: %s" % (frau, raum, st, prompt(frau, raum, st)))
        return
    presets = AF.lesen("presets.json")
    offen = {}
    for frau in nur:
        pre = presets[FRAUEN[frau]["preset"]]
        loras = [(l["name"], l["strength"]) for l in pre["loras"]]
        for raum in FRAUEN[frau]["raeume"]:
            for st in (1, 2, 3):
                name = "%s_%s_%d" % (frau, raum, st)
                if os.path.isfile(os.path.join(ROH, name + ".png")) and "--neu" not in sys.argv:
                    continue                         # schon da (Lauf abgebrochen): nur Fehlendes nachholen
                g = AF.graph(prompt(frau, raum, st), pre["negative_prompt"], loras, W, H, name, random.randint(1, 2 ** 31))
                g["9"]["inputs"]["save_path"] = ROH
                req = urllib.request.Request(AF.COMFY + "/prompt", headers={"Content-Type": "application/json"},
                                             data=json.dumps({"prompt": g}).encode())
                offen[name] = json.loads(urllib.request.urlopen(req, timeout=30).read())["prompt_id"]
    print("%d Bilder eingereiht" % len(offen), flush=True)
    while offen:
        time.sleep(3)
        for name, pid in list(offen.items()):
            h = json.loads(urllib.request.urlopen(AF.COMFY + "/history/" + pid, timeout=30).read())
            if pid in h and h[pid].get("status", {}).get("completed"):
                print("fertig:", name, flush=True)
                offen.pop(name)


def webp():
    """Rohbilder (PNG) -> Spielbilder (WebP, Qualitaet 88)."""
    from PIL import Image
    for n in sorted(os.listdir(ROH)):
        if n.endswith(".png"):
            Image.open(os.path.join(ROH, n)).convert("RGB").save(os.path.join(ZIEL, n[:-4] + ".webp"), "WEBP",
                                                                 quality=88, method=6)
            print("webp:", n[:-4])


if __name__ == "__main__":
    main()

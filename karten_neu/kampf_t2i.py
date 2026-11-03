# -*- coding: utf-8 -*-
r"""Einzelne Kampf-Posen per t2i im Querformat (20.10.2026), wo der Edit-Weg haengt (Yasin defeated, Bat-Angriffe).

    kampf_t2i.py <Name> <pose> [--seeds 3]

Laedt Kampf_<Name>, ersetzt fuer den Lauf Outfit-Text/Subject-Teile laut T2I[<Name>][<pose>] (Konflikte wie
"Drohne schwebt" oder "glaring" bei k.o.), Format 1328x880, sprite_src t2i. Ergebnis nach
output\expressions\_kampf_t2i\<Name>\<pose>(-N).png - die beste Variante kopiert man danach von Hand nach combat\.
Alles (Karten, Config) wird danach zurueckgesetzt.
"""
import io, json, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
W, H = 1328, 880

T2I = {
    "YasinDrone": {
        "defeated": {
            "outfit": "an open white linen shirt over a bare chest, a thin gold chain, beige linen shorts, white designer "
                      "sneakers, a heavy gold watch; his drone remote control lies dropped on the floor beside his hand "
                      "and his single black quadcopter drone lies crashed upside down on the floor next to him",
            "ersetzen": [("a furious angry scowl, glaring with clenched jaw", "a slack unconscious face with closed eyes"),
                         ("furrowed brows and ", "")],
            "pose": "unconscious and knocked out cold, lying flat on his back on the floor, his head resting on the "
                    "ground turned to the side, both arms limp on the floor, not propped up on an elbow, eyes firmly "
                    "closed, mouth slightly open, the whole body fully horizontal across the image, nothing in the air, "
                    "alone in the frame",
        },
    },
    "Bat": {k: {"outfit": None,
                "ersetzen": [("a large fruit bat with wings spread",
                              "a large fruit bat, small in the frame with wide empty space on all sides, its whole "
                              "wingspan fully inside the image")],
                "pose": v + ", the whole bat and both wingtips fully inside the image, no dust, no spray, no glow"}
            for k, v in {
                "attack": "swooping forward toward the viewer's left with its mouth wide open showing its fangs, claws "
                          "reaching forward, wings spread",
                "heavy_windup": "rearing back in mid-air with both wings raised high above its body, mouth closed, "
                                "tensed and ready to dive",
                "heavy_attack": "diving steeply at the viewer's left with fangs bared and claws outstretched, wings "
                                "swept back along its body"}.items()},
    "Pirate": {"defeated": {
        "outfit": "a torn faded red-and-white striped shirt with ripped-off sleeves, a dark red bandana, a frayed rope "
                  "belt, ragged brown knee-length trousers, barefoot; his rusty curved cutlass lies on the floor beside him",
        "ersetzen": [],
        "pose": "knocked out cold, lying flat on his back on the floor, head on the ground, arms limp, eyes closed, the "
                "whole body small in the frame with wide empty space on all sides, his bare feet and the whole "
                "cutlass fully inside the image, alone in the frame"}},
    "ThiefArab": {"defeated": {
        "outfit": "a black hoodie with the hood pulled up, a black cloth mask covering nose and mouth, slim black jeans, "
                  "black sneakers with white soles, a small black backpack; his short steel crowbar lies on the floor "
                  "beside him",
        "ersetzen": [],
        "pose": "knocked out cold, lying flat on his back on the floor, head on the ground, arms limp, eyes closed, the "
                "whole body fully horizontal across the image, alone in the frame"}},
    "Seagull": {"defeated": {
        "outfit": "a white head and belly, light grey wings with black wingtips, a thick yellow beak with a red spot, "
                  "pink webbed feet; a golden french fry lies dropped on the ground next to it",
        "ersetzen": [],
        "pose": "knocked out, lying flat on its side on the ground, wings limp and spread on the ground, eyes closed, "
                "feet in the air, the whole bird fully inside the image, alone in the frame"}},
    # BearCub (29.10.2026): guard hielt ein Metallding, defeated zeigte zwei Baeren, weakened/heavy_attack wie idle
    "BearCub": {
        "guard": {"outfit": "", "ersetzen": [],
                  "pose": "defensive, crouched low on all four paws with its head pulled down and ears flat, body "
                          "turned slightly away, peeking warily to the left, empty paws, holding nothing, alone in the "
                          "frame"},
        "defeated": {"outfit": "", "ersetzen": [],
                     "pose": "beaten and exhausted, a single bear cub lying flat on its belly on the ground with its "
                             "chin on its front paws, eyes half closed, the whole small body horizontal across the "
                             "image, only one bear, alone in the frame"},
        "weakened": {"outfit": "", "ersetzen": [],
                     "pose": "worn out and wobbly, sitting down heavily on its haunches, head drooping low, one front "
                             "paw lifted off the ground, tired half-closed eyes, alone in the frame"},
        "heavy_attack": {"outfit": "", "ersetzen": [],
                         "pose": "lunging forward to the left in a clumsy leap, both front paws stretched far forward "
                                 "with claws out, hind legs pushing off the ground, mouth wide open in a bluff roar, "
                                 "motion blur on the paws, alone in the frame"},
    },
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    name, pose = sys.argv[1], sys.argv[2]
    seeds = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 3
    t = T2I[name][pose]
    st = ps("/api/state")
    alt_cfg = {k: st["cfg"].get(k) for k in ("sprite_src", "sprite_prompt", "st_set", "width", "height", "aspect",
                                              "mode_opts", "seed", "tags", "decks_visible")}
    alt_preset = st["cfg"].get("preset_active")
    ps("/api/presets", {"action": "load", "name": "Kampf_" + name})
    kp = ps("/api/set_preset_laden", {"char": "Kampf_" + name, "kost": "Kampf"})
    st = ps("/api/state")
    outfit_karte = kp["outfit"][0]
    alt_karten = {(k, c["name"]): c["prompt"] for k in ("outfit", "kampf") for c in st["decks"][k]}
    try:
        sp = st["cfg"]["sprite_prompt"]
        for a, b in t["ersetzen"]:
            if a not in sp:
                raise SystemExit("nicht im Prompt: " + a)
            sp = sp.replace(a, b)
        an = set(kp.get("tags") or [])
        tags = st["cfg"]["tags"]
        for x in tags:
            x["on"] = x["name"] in an
        mo = dict(st["cfg"].get("mode_opts") or {})
        mo["sprite"] = dict(mo.get("sprite") or {}, aspect="%dx%d" % (W, H), width=W, height=H)
        n = 0
        for i in range(seeds):
            ps("/api/config", {"tags": tags, "mode": "sprite", "sprite_src": "t2i", "sprite_prompt": sp,
                               "st_set": "_kampf_t2i/" + name, "width": W, "height": H, "aspect": "%dx%d" % (W, H),
                               "mode_opts": mo, "combine_mode": "all", "view_pro_karte": False, "st_rembg": True,
                               "st_crop": True, "seed": 900001 + i * 7919,
                               "decks_visible": dict(st["cfg"].get("decks_visible") or {}, kampf=True)})
            d = ps("/api/state")["decks"]
            for k in d:
                for c in d[k]:
                    c["sel"] = False
            for c in d["outfit"]:
                if c["name"] == outfit_karte:
                    c["prompt"], c["sel"] = t["outfit"] or c["prompt"], True
            for c in d["setting"]:
                c["sel"] = c["name"] in set(kp.get("setting") or [])
            for c in d["kampf"]:
                if c["name"] == pose:
                    c["prompt"], c["sel"] = t["pose"], True
            n += ps("/api/queue", {"cfg": {}, "decks": d}).get("queued", 0)
        print("%s %s: %d Auftraege -> expressions\\_kampf_t2i\\%s" % (name, pose, n, name))
    finally:
        d = ps("/api/state")["decks"]
        for k in ("outfit", "kampf"):
            for c in d[k]:
                c["prompt"] = alt_karten.get((k, c["name"]), c["prompt"])
        ps("/api/decks", d)
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt_cfg.items() if v is not None})


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
r"""Ligeia mit mehr Flosse (Duc 30.10.2026: "teste B", Ducs aktueller Prompt, honigblond): ganze Figur, seitlich auf einem
niedrigen Felsen, der Schwanz liegt im Bogen zur Seite bis zur Schwanzflosse. Nur die Kopfzeile und die Outfit-Karte
werden fuer den Lauf ersetzt; Preset, Karten und Config werden danach zurueckgesetzt, nichts wird gespeichert.

    ligeia_flosse.py            Probelauf
    ligeia_flosse.py --los      vier Seeds neutral nach output\expressions\_ligeia_test\flosse_B
"""
import io, json, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PRESET = "Yacht_Ligeia"
ORDNER = "_ligeia_test/flosse_B"
SEEDS = [240611, 240612, 240613, 240614]
ALT_KOPF = ("upper body shot from the hips up, direct gaze, one single woman alone in the frame, her head, shoulders "
            "and upper body in full view, the top of her fish tail at the bottom edge of the frame,")
NEU_KOPF = ("full body shot, the camera far back, direct gaze, one single woman alone in the frame, sitting sideways "
            "on a low dark wet rock, propped on one straight arm, her upper body turned to the camera, her whole fish "
            "tail in full view, curving away from her hips across the rock and the floor to one side of the image, "
            "the tail fin fully inside the frame with empty floor around it,")
ALT_TAIL = "a long shimmering emerald-green fish tail instead of legs, beginning at her hips,"
NEU_TAIL = ("a long shimmering emerald-green fish tail instead of legs, beginning at her hips, ending in a large "
            "translucent forked tail fin,")
KARTE = "ligeia_standard"
KEYS = ("sprite_prompt", "st_set", "tags", "seed", "decks_visible", "mode_opts", "aspect", "width", "height")


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    st = ps("/api/state")
    alt_cfg = {k: st["cfg"].get(k) for k in KEYS}
    alt_preset = st["cfg"].get("preset_active")
    ps("/api/presets", {"action": "load", "name": PRESET})
    st = ps("/api/state")
    sp = st["cfg"]["sprite_prompt"]
    if ALT_KOPF not in sp:
        raise SystemExit("Kopfzeile im Preset hat sich geaendert - abgebrochen")
    alt_outfit = {c["name"]: c["prompt"] for c in st["decks"]["outfit"]}
    if ALT_TAIL not in alt_outfit[KARTE]:
        raise SystemExit("Outfit-Karte hat sich geaendert - abgebrochen")
    kp = ps("/api/set_preset_laden", {"char": PRESET, "kost": "Standard"})
    print("Tags:", ", ".join(kp.get("tags") or []))
    if "--los" not in sys.argv:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt_cfg.items() if v is not None})
        print(sp.replace(ALT_KOPF, NEU_KOPF))
        sys.exit("PROBELAUF - mit --los einstellen")
    try:
        an = set(kp.get("tags") or [])
        tags = ps("/api/state")["cfg"]["tags"]
        for t in tags:
            t["on"] = t["name"] in an
        mo = dict(st["cfg"].get("mode_opts") or {})
        mo["sprite"] = dict(mo.get("sprite") or {}, aspect="1328x880", width=1328, height=880)
        for seed in SEEDS:
            ps("/api/config", {"tags": tags, "sprite_prompt": sp.replace(ALT_KOPF, NEU_KOPF), "st_set": ORDNER,
                               "seed": seed, "mode_opts": mo, "aspect": "1328x880", "width": 1328, "height": 880,
                               "decks_visible": dict(st["cfg"].get("decks_visible") or {}, kampf=False)})
            d = ps("/api/state")["decks"]
            for deck in d:
                for c in d[deck]:
                    c["sel"] = False
            for c in d["outfit"]:
                if c["name"] == KARTE:
                    c["prompt"], c["sel"] = alt_outfit[KARTE].replace(ALT_TAIL, NEU_TAIL), True
            for c in d["setting"]:
                c["sel"] = c["name"] == "A Sprite Background"
            for c in d["st"]:
                c["sel"] = c["name"] == "neutral"
            n = ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": 1}).get("queued", 0)
            print("Seed %d: %d Auftrag" % (seed, n))
    finally:
        d = ps("/api/state")["decks"]
        for c in d["outfit"]:
            c["prompt"] = alt_outfit.get(c["name"], c["prompt"])
        ps("/api/decks", d)
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt_cfg.items() if v is not None})
        print("Preset, Karten und Config zurueckgesetzt")


if __name__ == "__main__":
    main()

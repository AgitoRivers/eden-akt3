# -*- coding: utf-8 -*-
r"""Alon im Rollkragen mit markanterem Gesicht (Duc 02.11.2026, Abnahme alon_keynote: b_rollkragen „NEU, markanteres Gesicht“).
Drei Gesichter nach Krea-Leitfaden (Herkunft, Alter, Gesichtsform, Nase, Augen, Brauen, Mund, Kinn, ein Merkmal), je zwei Seeds.

    alon_gesicht.py   -> output\expressions\_alon_keynote\gesicht_<x>_<n>.png
"""
import json, sys, time, urllib.request

sys.path.insert(0, r"X:\AI\Eden\karten_neu")
sys.path.insert(0, r"X:\AI\PromptStudio")
import alon_keynote_casting as K  # noqa: E402

GESICHTER = {
    "kante": "Alon Varenne, a 53-year-old Canadian tech billionaire from Montreal with old French roots, a long angular face with "
             "high sharp cheekbones and hollow cheeks, a strong straight nose, deep-set pale grey-blue eyes that look amused, thick "
             "dark eyebrows, a thin-lipped crooked smile, a square cleft chin, a short silver buzz cut, deep laugh lines around the eyes",
    "falke": "Alon Varenne, a 53-year-old Canadian tech billionaire from Montreal with old French roots, a lean narrow face, a "
             "prominent hooked nose like a hawk, small sharp ice-blue eyes under heavy brows, a wide confident grin with very white "
             "teeth, a pointed chin with grey stubble, a short silver buzz cut, a thin old scar through his left eyebrow",
    "glatt": "Alon Varenne, a 53-year-old Canadian tech billionaire from Montreal with old French roots, a broad smooth face that looks "
             "younger than he is, a heavy jaw, a slightly crooked broken nose, bright hazel eyes that never blink enough, straight "
             "dark eyebrows, a boyish dimpled smile, a short silver buzz cut, a faint grey shadow under his eyes",
}
ANZUG = "a black merino turtleneck, charcoal chinos, black leather sneakers, aviator sunglasses pushed up on his head, " + K.SCHIENE
KOERPER = "a soft middle-aged body with a small round belly and narrow shoulders, slightly pale under a light tan"


def main():
    import studio
    with urllib.request.urlopen(K.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for k, gesicht in GESICHTER.items():
        p = "%s,\nSubject: %s, %s,\nWearing: %s,\nScene: Plain beige background,\n%s." % (K.KOPF, gesicht, KOERPER, ANZUG, K.HALTUNG)
        for n, seed in enumerate(K.SEEDS, 1):
            c = dict(cfg, loras=K.LORAS, mode="sprite", sprite_src="t2i", width=880, height=1328, negative_prompt="", st_set=K.ORDNER,
                     st_rembg=False, st_crop=False)
            wart.append(K.post(K.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, "gesicht_%s_%d" % (k, n), seed)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 1500
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(K.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()

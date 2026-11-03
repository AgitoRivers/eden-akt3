# -*- coding: utf-8 -*-
r"""Casting AgentGunman (Duc 01.11.2026): die Schuetzin der Agenten, eine Kolumbianerin mit leichtem Sturmgewehr. Anzug wie Kampf_Agent, je 3 Varianten, je 2 Seeds.

    casting_agent_gunman.py   -> output\expressions\_casting_agent_gunman_2\<g1..g3>\idle(-1).png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_piraten_neu as cp  # noqa: E402

ORDNER = "_casting_agent_gunman_2"
KOPF = cp.KOPF.replace("one single man", "one single woman").replace("his whole body", "her whole body")
HAUT = "warm tanned brown skin, natural skin texture with visible pores, slight natural asymmetry in the face, a real individual face"
ANZUG = "a black tailored suit with slim trousers, a crisp white shirt, a slim black tie, a clear earpiece with a coiled wire behind her right ear, black sunglasses, black leather gloves, polished black shoes"
WAFFE = "her only weapon exactly one light compact black assault rifle with a short barrel and a slim stock, held with both hands"
HALTUNG = "aiming to the left, the stock at her right shoulder, her left hand on the front of the rifle, the barrel level and pointing straight to the left, standing side-on with her feet apart, calm cold stare"
WER = {
    "g1": "Valentina Rios, a 34-year-old Colombian woman from Medellin, a long oval face with high cheekbones, a straight nose, full lips, thick dark eyebrows, a lean athletic build, long black hair pulled back in a tight low ponytail",
    "g2": "Valentina Rios, a 36-year-old Colombian woman from Cali, a sharp angular face with a strong jaw, a small scar through one eyebrow, thin lips, a lean wiry build, black hair in a tight bun at the back of her head",
    "g3": "Valentina Rios, a 32-year-old Colombian woman from Bogota, a heart-shaped face with a wide mouth and a slightly crooked nose, a slim athletic build, shoulder-length wavy black hair tucked behind her ears",
}


def prompt(key, haltung=HALTUNG, waffe=WAFFE):
    return "%s,\nSubject: %s, %s,\nWearing: %s,\nScene: Plain beige background,\n%s, %s, the whole weapon inside the image." % (KOPF, WER[key], HAUT, ANZUG, haltung, waffe)


def main():
    import studio
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for key in WER:
        c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=1232, height=1232, negative_prompt="", st_set="%s/%s" % (ORDNER, key), st_rembg=True, st_crop=False, **cp.MODELL)
        for s in cp.SEEDS:
            wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, prompt(key), "idle", s)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    ende = time.time() + 400
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cp.COMFY + "/history/" + i, timeout=30) as f:
                if json.loads(f.read()).get(i):
                    wart.remove(i)
    print("offen", len(wart))


if __name__ == "__main__":
    main()

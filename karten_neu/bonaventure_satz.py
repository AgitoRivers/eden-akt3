# -*- coding: utf-8 -*-
r"""NPC-Satz Captain Bonaventure (Duc 01.11.2026, Wahl C2 auf docs/abnahme/bonaventure_casting_2.json, ohne Blechkrone, schwarze Stiefel, Goldmuenze): 22 Posen, nur Front, ohne desire_2. Nichts wird ins Spiel kopiert.

    bonaventure_satz.py [--nur neutral,joy]   -> output\expressions\_bonaventure_satz\<pose>.png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_bonaventure_2 as cb  # noqa: E402
import minicu_satz as ms  # noqa: E402

ORDNER = "_bonaventure_satz"
SEED = cb.SEEDS[0]


def dialog(text):
    return cb.prompt("c").split("He stands square")[0] + ms.mann(text)


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(cb.PS + "/api/state", timeout=30) as f:
        st = json.loads(f.read())
    cfg = dict(st["cfg"])
    karten = {c["name"]: c["prompt"] for c in st["decks"]["st"]}
    wart = []
    for pose in ms.NPC:
        if nur and pose not in nur:
            continue
        p = cb.prompt("c") if pose == "neutral" else dialog(ms.EIGEN.get(pose) or karten[pose])
        b, h = (1104, 1408) if pose in ms.HOCH else (880, 1328)
        c = dict(cfg, loras=cb.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER, st_rembg=True, st_crop=True, **cb.MODELL)
        wart.append(cb.post(cb.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 280
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cb.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()

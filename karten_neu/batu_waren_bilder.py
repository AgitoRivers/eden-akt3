# -*- coding: utf-8 -*-
r"""Item-Bilder fuer Ba Tus neue Ware (Duc 31.10.2026): Pho-Schale, Zitronengras-Steckling, Zitronengras.
Je 2 Fassungen nach output\_batu_waren, erst nach der Abnahme ins Spiel (module\eden_rise\items\<id>.webp)."""
import os, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "werkzeuge"))
import item_bilder as IB  # noqa: E402

ORDNER = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_batu_waren"
MOTIVE = {
    "pho_bowl": "a deep plain white ceramic bowl of Vietnamese pho, clear amber beef broth with flat rice noodles, thin slices of beef, "
                "fresh green herbs and a wedge of lime, a pair of wooden chopsticks resting on the rim, a little steam rising",
    "lemongrass_cutting": "three young lemongrass cuttings lying side by side, long narrow bright green leaves, the pale stem bases and fine white "
                          "roots wrapped together in a piece of damp brown paper tied with kitchen string",
    "lemongrass": "a bundle of fresh lemongrass stalks, pale yellow-green stems with cleanly trimmed ends and long green tops, tied with kitchen twine",
}


def main():
    os.makedirs(ORDNER, exist_ok=True)
    offen = {}
    for iid, motiv in MOTIVE.items():
        if len(sys.argv) > 1 and iid not in sys.argv[1:]:
            continue
        prompt = IB.STIL.format(motiv=motiv, hintergrund=IB.HINTERGRUENDE[IB.HINTERGRUND])
        for nr, seed in enumerate((310312, 871205), 1):
            name = "%s_%d" % (iid, nr)
            offen[name] = IB.post("/prompt", {"prompt": IB.graph(prompt, ORDNER, name, seed, IB.nsfw_an(name))})["prompt_id"]
            print("eingereiht", name, flush=True)
    t0 = time.time()
    while offen and time.time() - t0 < 600:
        time.sleep(2)
        for name, pid in list(offen.items()):
            h = IB.get("/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                print("fertig", name, flush=True)
                del offen[name]
    print("OFFEN" if offen else "ALLE FERTIG", list(offen), flush=True)


if __name__ == "__main__":
    main()

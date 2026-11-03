# -*- coding: utf-8 -*-
r"""Elsas Combat-Satz nachschaerfen (Duc 01.11.2026: Abzeichen und Ruestung wandern). Nimmt je Bild aus Yacht_Elsa\Combat\roh den eingebetteten Graphen samt Seed und Pose-Text,
ersetzt nur die Zeile Wearing und speichert nach Yacht_Elsa\Combat\roh2. Ducs Bilder bleiben unberuehrt. Die neue Beschreibung folgt seinem Bild neutral.png.

    elsa_combat_neu.py [--nur neutral,joy]
"""
import glob, json, os, re, sys, time, urllib.request

from PIL import Image

COMFY = "http://127.0.0.1:8189"
ROH = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Elsa\Combat\roh"
ZIEL = "Yacht_Elsa/Combat/roh2"
WEARING = ("Wearing: a dark navy beret with exactly one small gold winged badge at the front above her left eye, a long-sleeved dark navy uniform with a high plain turtleneck collar, "
           "completely plain solid dark navy sleeves from shoulder to wrist and plain fabric free of any text or patches, a rounded black hard pad on each elbow, "
           "a dark navy tactical armour vest with wide shoulder straps, on the vest one smooth rectangular dark navy chest panel with exactly one small gold winged badge in the centre of the panel at breastbone height, "
           "flat horizontal black webbing straps across the stomach below the panel, black leather gloves, a wide black duty belt with one black radio on her left hip, "
           "one black service pistol in a closed holster on her right thigh, dark navy cargo trousers, a rounded black hard pad on each knee, black lace-up tactical boots")


def main():
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    wart = []
    for p in sorted(glob.glob(os.path.join(ROH, "*.png"))):
        name = os.path.basename(p)[:-4]
        if nur and name not in nur:
            continue
        g = json.loads(Image.open(p).info["prompt"])
        treffer = 0
        for n in g.values():
            if n.get("class_type") == "CLIPTextEncode" and "Wearing: " in str(n["inputs"].get("text")):
                n["inputs"]["text"] = re.sub(r"Wearing: .*", WEARING, n["inputs"]["text"])
                treffer += 1
            if n.get("class_type") == "KSampler" and "--seed-plus" in sys.argv:
                n["inputs"]["seed"] += int(sys.argv[sys.argv.index("--seed-plus") + 1])     # zweite Runde: Aufnaeher blieben bei festem Seed
            if n.get("class_type") == "ExpressionSave":
                n["inputs"]["subfolder"] = ZIEL
        assert treffer == 1, name
        r = urllib.request.Request(COMFY + "/prompt", data=json.dumps({"prompt": g}).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(r, timeout=60) as f:
            wart.append(json.loads(f.read())["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 560
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(COMFY + "/history/" + i, timeout=30) as f:
                h = json.loads(f.read()).get(i)
            if h:
                fehler += h.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
r"""Vorhandenen Hintergrund per Krea2-Edit aendern (Duc 02.11.2026): gleiche Komposition, ein Detail anders oder Nacht.

    python hintergrund_edit.py <auftrag> 4            4 Varianten -> ST\backgrounds\_varianten\eden_rise_<ziel>_v1..4.png
    python hintergrund_edit.py <auftrag> --waehle 2   Variante 2 -> ST\backgrounds\eden_rise_<ziel>.png

Graph wie kabine_nacht.py (Krea2EditModelPatch + Krea2EditGroundedEncode). Die Quelle wird vorher gesichert nach
_varianten\_quellen, damit ein neuer t2i-Lauf sie nicht ueberschreibt."""
import os, random, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import item_bilder as ib
import kabine_nacht as kn

ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"
VAR = os.path.join(ST_BG, "_varianten")
INPUT = r"X:\AI\ComfyUI_krea2\ComfyUI\input"
BEHALTEN = ("Keep the room, the camera angle, the walls, the furniture and every other object exactly as they are. "
            "Photorealistic, not a single person is in the shot.")
AUFTRAEGE = {
    # ziel: (quelle in _varianten, Anweisung)
    "crew_kabine_1": ("eden_rise_crew_kabine_1_v4.png",
                      "Edit this photo. Make only the upper bunk messy and lived in: a rumpled blue blanket half falling over the rail, "
                      "a crumpled towel, a hoodie and two open books lying on it, the black wetsuit still hanging over the rail. "
                      "The lower bunk stays neat. " + BEHALTEN),
    "crew_kabine_2": ("eden_rise_crew_kabine_2_e_v3.png",
                      "Edit this photo. On the LEFT bed, fold the galaxy universe fleece blanket smaller into a neat soft square at "
                      "the foot of the bed. On the RIGHT bed add a few small personal things, neatly placed: a short coiled rope tied "
                      "with practice sailing knots, a thin boating licence study book with a pencil, a black hair tie, a small framed "
                      "photo of Vienna on the shelf. Keep the cat bed and the toy mouse under the right bed. " + BEHALTEN),
    "crew_kabine_3": ("eden_rise_crew_kabine_3_v2.png",
                      "Edit this photo. Turn the bed into a bunk bed: directly above the made bed add a second upper berth of glossy "
                      "walnut that has NO mattress, only bare empty wooden slats with nothing lying on them. " + BEHALTEN),
    "waescherei_kabine_nacht": ("eden_rise_waescherei_kabine_tag_v2.png",
                                "Change this exact cabin to night. Keep the cabin, the bed, the desk, the lamp, the porthole and every "
                                "object exactly where they are. Only change the lighting: the porthole now shows a dark night sea "
                                "with a silver moon reflection, the ceiling spots are off, the cabin is lit only by the warm glow of "
                                "the reading lamps, deep soft shadows, quiet night atmosphere, photorealistic"),
    "bibi_haeuschen_tag": ("eden_rise_bibi_haeuschen_tag_v1.png",
                           "Edit this photo. Remove the plush toy lion from the bed completely, the white pillows are plain and "
                           "empty. " + BEHALTEN),
    "bibi_haeuschen_nacht": ("eden_rise_bibi_haeuschen_tag_v1.png",
                             "Change this exact room to night and remove the plush toy lion from the bed, the white pillows are "
                             "plain and empty. Keep the room, the bed, the rug, the armchair, the painting, the stove and every "
                             "other object exactly where they are. Only change the lighting: the window shows a dark blue night "
                             "sky with stars, the room is lit by the warm glow of the lamps and the fire in the stove, deep soft "
                             "shadows, cosy night atmosphere, photorealistic"),
    "megan_kabine_nacht": ("eden_rise_megan_kabine_auswahl.png",
                           "Change this exact cabin to night. Keep the cabin, the bed, the desk, the chair, the chess board, the windows "
                           "and every object exactly where they are. Only change the lighting: the windows show a dark night sea with a "
                           "silver moon reflection and a few distant lights of Monaco, the ceiling spots are dimmed, the cabin is lit by the "
                           "warm glow of the bedside lamps and a desk lamp, deep soft shadows, quiet night atmosphere, photorealistic"),
}


def main():
    ziel = sys.argv[1]
    quelle, prompt = AUFTRAEGE[ziel]
    datei = "eden_rise_%s_e" % ziel
    if "--waehle" in sys.argv:
        k = sys.argv[sys.argv.index("--waehle") + 1]
        shutil.copy2(os.path.join(VAR, "%s_v%s.png" % (datei, k)), os.path.join(ST_BG, "eden_rise_%s.png" % ziel))
        print("uebernommen: %s Variante %s -> eden_rise_%s.png" % (ziel, k, ziel))
        return
    os.makedirs(os.path.join(VAR, "_quellen"), exist_ok=True)
    gesichert = os.path.join(VAR, "_quellen", quelle)
    if not os.path.exists(gesichert):
        shutil.copy2(os.path.join(VAR, quelle), gesichert)
    eingabe = "edit_" + quelle
    shutil.copy2(gesichert, os.path.join(INPUT, eingabe))
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    ib.NSFW_PROFIL["loras"] = [("Krea_Real3.safetensors", 0.7)]
    kn.QUELLE, kn.PROMPT = os.path.join(INPUT, eingabe), prompt
    auftraege = [("v%d" % k, ib.post("/prompt", {"prompt": kn.graph(random.randint(1, 2 ** 31), VAR, "%s_v%d" % (datei, k))})["prompt_id"])
                 for k in range(1, n + 1)]
    ib.warten(auftraege, lambda v: print("fertig:", v))
    print("Varianten in", VAR)


if __name__ == "__main__":
    main()

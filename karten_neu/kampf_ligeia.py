# -*- coding: utf-8 -*-
r"""Kampf-Sprites der Sirene neu als Ligeia (Duc 30.10.2026): honigblond statt rot, Tags und LoRAs aus Yacht_Ligeia, eigene Posen fuer
den Fischschwanz, Querformat wegen des Schwanzes. Der Kampf ist ein Rede-Kampf: Sie greift mit der Stimme an. Alte Bilder wandern
nach output\_expressions_papierkorb\combat\siren_<Zeit>.

    kampf_ligeia.py          Probelauf
    kampf_ligeia.py --los [--karten a,b]
"""
import os, shutil, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
LOS = "--los" in sys.argv
KARTEN = sys.argv[sys.argv.index("--karten") + 1].split(",") if "--karten" in sys.argv else None
import kampf_red_trio as KR  # noqa: E402   (setzt sys.argv zurueck)

dc, sk = KR.dc, KR.sk
C = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Siren"
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\combat\siren_" + time.strftime("%Y%m%d_%H%M")
GANZ = ("full body shot, the camera far back, one single woman alone in the frame, she has no legs and no feet, only one fish "
        "tail from the hips down, her whole fish tail fully inside the image and stretching away to the right, resting on a flat "
        "empty floor, nothing under her and no objects anywhere,")
GANZ_ALT = "full body shot, one single woman alone in the frame, her whole body in full view,"
SUBJECT = "Subject: The Siren, an ancient Greek sea spirit in the shape of a young Mediterranean woman, light green eyes,"
SUBJECT_ALT = "Subject: a beautiful siren, a mermaid with long flowing red hair and sea-green eyes,"
OUTFIT = ("a long shimmering emerald-green fish tail instead of legs, beginning at her hips, ending in a large translucent forked "
          "tail fin, topless, a thin dark leather cord around her neck holding a small empty silver pearl setting, wet glistening "
          "skin, long wet strands of hair clinging to her shoulders like seaweed")
POSEN = {
    "idle": "she rises tall on her coiled tail facing left, shoulders back, chin lifted, a cold knowing stare, hair dripping",
    "windup": "drawing a long breath through open lips, her chest lifting, one hand raised beside her mouth, tail coiling tight, "
              "eyes locked to the left",
    "attack": "singing at full voice toward the left with her mouth wide open, one arm flung out to the left, fine spray in the air",
    "heavy_windup": "arching back with both arms spread wide and her head thrown back, gathering a huge note, water drops rising "
                    "around her, tail fin raised high",
    "heavy_attack": "leaning forward and hurling a scream of song to the left with both hands cupped at her mouth, a wall of spray "
                    "blown toward the left edge of the image, her hair whipping back",
    "guard": "pulling back and curling her tail up in front of her body like a shield, one forearm raised, eyes on the threat at the "
             "left",
    "hurt": "recoiling off balance, head snapped back, one hand clutching her throat, tail lashing behind her, face twisted in pain",
    "weakened": "slumped low, propped on one shaking arm, panting, tail lying limp, wet hair hanging over her face",
    "enraged": "rising high on her tail, baring her teeth, fingers hooked like claws, tail fin raised to slam down, furious",
    "flee": "twisting away toward the right, diving away, looking back over her shoulder in fear, tail fin high",
    "surrender": "lowering herself to the floor with both open hands raised, head bowed, tail curled in close",
    "victory": "reclining propped on one elbow, gloating down to the left with a slow amused smile, tail fin flicking lazily",
    "defeated": "knocked out cold, lying flat on her back on the floor with nothing holding her up, shoulders and the back of her head "
                "resting on the floor at the left, eyes closed, mouth slightly open, both arms limp on the floor beside her, the tail "
                "lying flat and still, her whole body fully horizontal across the image, seen from the side at floor level",
    "death": "lying flat on her back on the floor with nothing holding her up, shoulders and head resting on the floor at the left, "
             "eyes closed, face turned away, wet hair spread out around her head, both arms limp on the floor, the tail lying flat "
             "with the fin spread and still, her whole body fully horizontal across the image, seen from the side at floor level",
}


def presets_anpassen():
    presets = dc.load_json(sk.F_PRESETS, None, "Studio")
    sets = dc.load_json(sk.F_SETS, None, "Studio")
    li, p = presets["Yacht_Ligeia"], presets["Kampf_Siren"]
    if GANZ_ALT in p["sprite_prompt"]:
        p["sprite_prompt"] = p["sprite_prompt"].replace(GANZ_ALT, GANZ)
    if SUBJECT_ALT in p["sprite_prompt"]:
        p["sprite_prompt"] = p["sprite_prompt"].replace(SUBJECT_ALT, SUBJECT)
    assert GANZ in p["sprite_prompt"] and SUBJECT in p["sprite_prompt"]
    p["loras"] = li["loras"]
    tags = ["View: Kampf"] + [t for t in li["tags_on"] if not t.startswith("View:")]
    p["tags_on"] = tags
    sets["Kampf_Siren|Kampf"]["tags"] = tags
    print("Tags:", ", ".join(tags))
    if LOS:
        dc.save_json(sk.F_PRESETS, presets, "Studio")
        dc.save_json(sk.F_SETS, sets, "Studio")
        d = KR.ps("/api/state")["decks"]
        for c in d["outfit"]:
            if c["name"] == "kampf_siren":
                c["prompt"] = OUTFIT
        KR.ps("/api/decks", d)


def main():
    wahl = {k: v for k, v in POSEN.items() if not KARTEN or k in KARTEN}
    st = KR.ps("/api/state")
    alt_preset = st["cfg"].get("preset_active")
    presets_anpassen()
    print("%d Posen" % len(wahl))
    if not LOS:
        print("Probelauf - nichts geaendert")
        return
    os.makedirs(KORB, exist_ok=True)
    for k in wahl:
        f = os.path.join(C, k + ".png")
        if os.path.isfile(f):
            shutil.move(f, os.path.join(KORB, k + ".png"))
    print("alte Bilder ->", KORB)
    try:
        KR.mit_text("Siren", wahl, quer=True)
    finally:
        if alt_preset:
            KR.ps("/api/presets", {"action": "load", "name": alt_preset})
    print("fertig eingereiht")


if __name__ == "__main__":
    main()

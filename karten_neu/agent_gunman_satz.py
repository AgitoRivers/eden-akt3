# -*- coding: utf-8 -*-
r"""Voller Kampf-Satz AgentGunman (Duc 01.11.2026, Wahl g1 auf docs/abnahme/agent_gunman.json). Gleiches Modell und gleicher Seed wie die Wahl.

    agent_gunman_satz.py [--nur attack,guard]   -> output\expressions\_agent_gunman_satz\<pose>.png
"""
import json, os, sys, time, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\PromptStudio")
import casting_agent_gunman as cg  # noqa: E402
import casting_piraten_neu as cp  # noqa: E402

ORDNER = "_agent_gunman_satz"
SEED = cp.SEEDS[0]
GEWEHR = "exactly one light compact black assault rifle with a short barrel and a slim stock"
ZWEI = "exactly two arms and two hands"
FERN = "the camera far back, the whole rifle and both shoes completely inside the image with wide empty floor below them"
LEER = "both hands empty, no weapon anywhere"
# Pose: (Haltung, Breite, Hoehe). Gesicht, Kleidung und Waffe je Pose ausdruecklich, die Waffe immer von der Seite
POSEN = {
    "windup": ("%s, raising %s to her right shoulder, one eye behind the sights, turned side-on, feet apart, the barrel coming up to the left, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "attack": ("%s, shooting to the left, the stock of %s pressed firmly into her right shoulder, her left hand on the front of the rifle, the barrel level and pointing straight to the left and kicking slightly upward, a firm step forward, hard stare, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "heavy_windup": ("%s, kneeling on one knee and taking careful aim to the left, the stock of %s at her right shoulder, every muscle tensed, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "heavy_attack": ("%s, kneeling on one knee and shooting a long burst to the left, the stock of %s at her right shoulder, the barrel level and pointing straight to the left, teeth clenched, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "guard": ("%s, in a defensive stance, body pulled back and low, %s held diagonally across the front of her chest with both hands as a shield against an attack from the left, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "hurt": ("%s, hit by a heavy blow, recoiling backwards off balance, head snapped back, face twisted in pain, her left hand pressed flat on her ribs, her right hand holding %s low at her side pointing at the floor, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "enraged": ("%s, furious and shouting with her mouth wide open and her teeth bared, leaning forward, %s gripped with both hands across her hips, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "weakened": ("%s, exhausted and worn out, swaying on unsteady legs, panting heavily, both legs straight, %s hanging low in her right hand and pointing at the floor, her left arm limp, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
    "defeated": ("seen from the side at floor level, she lies stretched out flat on her back, resting on the floor, her body perfectly horizontal and level, arms limp at her sides, knocked out, her one head on the RIGHT side of the image, eyes closed; exactly one woman with one head, the whole woman fully inside the image with empty space around, %s" % LEER, 1328, 880),
    "surrender": ("she drops to both knees and raises both open hands above her head, head bowed in defeat; the floor around her is completely clean and empty, %s" % LEER, 1104, 1408),
    "flee": ("running away in panic, looking back over her shoulder in fear, %s held in her right hand at her side, her left arm swinging with an empty hand, %s" % (GEWEHR, FERN), 1232, 1232),
    "victory": ("%s, triumphant and cold, chest out, chin up, a small smile, %s held upright in her right hand with the stock resting on her hip and the barrel pointing at the sky, %s" % (ZWEI, GEWEHR, FERN), 1232, 1232),
}


def prompt(pose):
    return "%s,\nSubject: %s, %s,\nWearing: %s,\nScene: Plain beige background,\n%s." % (cg.KOPF, cg.WER["g1"], cg.HAUT, cg.ANZUG, POSEN[pose][0])


def main():
    import studio
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    with urllib.request.urlopen(cp.PS + "/api/state", timeout=30) as f:
        cfg = dict(json.loads(f.read())["cfg"])
    wart = []
    for pose, (_, b, h) in dict(POSEN, idle=(None, 1232, 1232)).items():
        if nur and pose not in nur:
            continue
        p = cg.prompt("g1") if pose == "idle" else prompt(pose)
        c = dict(cfg, loras=cp.LORAS, mode="sprite", sprite_src="t2i", width=b, height=h, negative_prompt="", st_set=ORDNER, st_rembg=True, st_crop=True, **cp.MODELL)
        wart.append(cp.post(cp.COMFY + "/prompt", {"prompt": studio.build_graph(c, p, pose, SEED)})["prompt_id"])
    print("eingereiht", len(wart), flush=True)
    fehler, ende = 0, time.time() + 900
    while wart and time.time() < ende:
        time.sleep(3)
        for i in list(wart):
            with urllib.request.urlopen(cp.COMFY + "/history/" + i, timeout=30) as f:
                r = json.loads(f.read()).get(i)
            if r:
                fehler += r.get("status", {}).get("status_str") != "success"
                wart.remove(i)
    print("offen", len(wart), "fehler", fehler)


if __name__ == "__main__":
    main()

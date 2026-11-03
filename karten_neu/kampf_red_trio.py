# -*- coding: utf-8 -*-
r"""Kampf-Sprites fuer das Red Trio (Duc 29.10.2026): Danzel, Bibi und Charly aus Ducs Char-Presets Yacht_Danzel,
Yacht_Bibi, Yacht_Charly (Subject, Tags, LoRAs live gelesen). Kampf-Outfit = der rote Agentenanzug (nicht das
gerade aktive Kostuem), dazu je eine Waffe: Danzel Teleskopschlagstock (Feigling), Bibi Granaten, Charly Taser.
Angriffe, guard und defeated bekommen eigene Kartentexte (nur fuer den Lauf, danach zurueckgesetzt); defeated im
Querformat. Danzel ist 30: "sehr helle Haare" statt "white hair", sonst altert er im Kampf auf 50+.

    kampf_red_trio.py                     Probelauf
    kampf_red_trio.py --los [--nur Bibi]  Presets Kampf_<Name> + Kostuem-Presets, dann alle 13 Kernkarten
                                          -> output\expressions\combat\<Name>
Danach Abnahme; erst nach Ducs OK Kampf_Bilder.bat --gegner Danzel,Bibi,Charly.
"""
import io, json, os, subprocess, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\DucCommon")
LOS = "--los" in sys.argv
NUR = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None
sys.argv = [sys.argv[0]]
import duc_common as dc  # noqa: E402
import studio_kampf_gegner as sk  # noqa: E402   (setzt stdout auf UTF-8)

PS = "http://127.0.0.1:8301"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"

# Name: (Char-Preset, mann?, Outfit-Karte des Agentenanzugs, Waffe, {Karte: Text})
TRIO = {
    "Danzel": ("Yacht_Danzel", True, "danzel_B",
               "a black telescopic baton held in his right hand a little too tightly, his left hand empty", {
        "idle": "in a shaky fighting stance facing left, the baton held out in front of him, trying hard to look "
                "tough, a nervous bead of sweat on his temple",
        "windup": "raising the baton high over his head with both hands, eyes squeezed shut, mouth open in a yell, "
                  "leaning back to the left",
        "attack": "swinging the baton down to the left with his eyes shut tight, stumbling forward off balance, coat "
                  "tails flying, slight motion blur on the baton",
        "heavy_windup": "twirling the baton in a dramatic over-the-top pose, one knee raised, his free hand stretched "
                        "out to the left like an anime villain, an overconfident grin",
        "heavy_attack": "charging forward to the left with the baton held out like a sword, screaming, his coat "
                        "flapping behind him, motion blur",
        "guard": "cowering behind his raised left forearm, the baton held crosswise in front of his face, knees "
                 "bent, one eye peeking out in fear"}),
    "Bibi": ("Yacht_Bibi", False, "bibi_A",
             "a round black hand grenade in her right hand", {
        "windup": "pulling the pin of a round black grenade with her teeth, her throwing arm drawn back, a wild grin, "
                  "eyes on the left",
        "attack": "throwing a round black grenade to the left with a big overhand throw, her body twisting, laughing "
                  "loudly",
        "heavy_windup": "holding a round black grenade in each hand raised above her head, an exaggerated villain "
                        "laugh, one knee pulled up",
        "heavy_attack": "hurling two round black grenades to the left at once, a bright flash and grey smoke at the "
                        "left edge of the frame, her hair whipping",
        "guard": "ducking low behind her raised forearms, squinting, her free hand on the grenades at her belt"}),
    "Charly": ("Yacht_Charly", False, "charly_A",
               "a black handheld taser in her right hand", {
        "windup": "aiming her taser to the left with one straight arm and a bored face, her other hand in her pocket",
        "attack": "firing her taser to the left, two thin wires shooting out with a small blue electric spark, her "
                  "face still completely deadpan",
        "heavy_windup": "holding the taser up beside her face while blue electric arcs crackle between its prongs, an "
                        "unimpressed look",
        "heavy_attack": "jamming the crackling taser forward to the left, bright blue electric arcs, her hair lifting "
                        "from the static, still unimpressed",
        "guard": "stepping back and raising her left forearm to block, the taser pulled back close to her chest, a "
                 "flat annoyed look"}),
}
LIEGT = ("knocked out cold, lying flat on %s back on the floor, %s head turned to the side, both arms limp on the "
         "floor, eyes closed, mouth slightly open, the whole body fully horizontal across the image, nothing in the "
         "air, alone in the frame")
JUNG = {"Danzel": [("white hair", "very light platinum blond hair"),
                   ("a young Japanese-French man", "a 30-year-old Japanese-French man with smooth youthful skin")]}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def subject(vorlage, name):
    s = next(z for z in vorlage["sprite_prompt"].splitlines() if z.startswith("Subject: "))[len("Subject: "):]
    for alt, neu in JUNG.get(name, []):
        s = s.replace(alt, neu)
    return s.rstrip(",")


def lauf(name, karten, quer=False):
    cmd = [PY, os.path.join(HIER, "kampf_test.py"), "--karten", ",".join(karten), "--gegner", name]
    subprocess.run(cmd + (["--quer"] if quer else []), check=True, stdout=subprocess.DEVNULL)
    print("  %-7s eingereiht: %s%s" % (name, ", ".join(karten), " (quer)" if quer else ""))


def mit_text(name, texte, quer=False):
    """Kampf-Karten fuer einen Lauf umschreiben, je Karte ein Auftrag, danach zuruecksetzen."""
    original = {c["name"]: c["prompt"] for c in ps("/api/state")["decks"]["kampf"]}
    try:
        for k, t in texte.items():
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == k:
                    c["prompt"] = t
            ps("/api/decks", d)
            lauf(name, [k], quer)
    finally:
        d = ps("/api/state")["decks"]
        for c in d["kampf"]:
            if c["name"] in original:
                c["prompt"] = original[c["name"]]
        ps("/api/decks", d)


def main():
    trio = {k: v for k, v in TRIO.items() if not NUR or k == NUR}
    presets = dc.load_json(sk.F_PRESETS, None, "Studio")
    st = ps("/api/state")
    kern = [c["name"] for c in st["decks"]["kampf"] if c.get("on", True) and c.get("tag") == "kern"]
    outfits = {c["name"]: c for c in st["decks"]["outfit"]}
    plan = {}
    for name, (vp, mann, karte, waffe, texte) in trio.items():
        v = presets[vp]
        tags = [t for t in v.get("tags_on", []) if not t.startswith("View:")]
        plan[name] = (subject(v, name), tags, v.get("loras") or sk.LORAS, outfits[karte]["prompt"] + ", " + waffe)
        print("%-7s Subject: %s\n        Tags: %s\n        LoRAs: %s\n        Outfit (%s): %s\n        eigene Texte: %s"
              % (name, plan[name][0], ", ".join(tags), ", ".join(l["name"] for l in plan[name][2]), karte,
                 plan[name][3], ", ".join(list(texte) + ["defeated (quer)"])))
    if not LOS:
        print("Probelauf - nichts geschrieben. Kernkarten: %s" % ", ".join(kern))
        return
    alt_preset = st["cfg"].get("preset_active")
    sets = dc.load_json(sk.F_SETS, None, "Studio")
    d = st["decks"]
    for name, (subj, tags, loras, outfit) in plan.items():
        kn = "kampf_" + name.lower()
        if kn in outfits:
            outfits[kn]["prompt"] = outfit
        else:
            d["outfit"].append({"name": kn, "prompt": outfit, "on": True, "tag": "kampf", "sel": False, "back_prompt": ""})
        p = sk.preset(name, "mann" if trio[name][1] else "frau", subj, tags, "hoch")
        p["loras"] = loras
        presets["Kampf_" + name] = p
        sets["Kampf_%s|Kampf" % name] = {"outfit": [kn], "setting": ["A Sprite Background"], "tags": ["View: Kampf"] + tags}
    ps("/api/decks", d)
    dc.save_json(sk.F_PRESETS, presets, "Studio")
    dc.save_json(sk.F_SETS, sets, "Studio")
    try:
        for name, (vp, mann, karte, waffe, texte) in trio.items():
            mit_text(name, texte)
            rest = [k for k in kern if k not in texte and k != "defeated"]
            lauf(name, rest)
            sein = "his" if mann else "her"
            mit_text(name, {"defeated": LIEGT % (sein, sein)}, quer=True)
    finally:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
    print("fertig eingereiht: %s" % ", ".join(trio))


if __name__ == "__main__":
    main()

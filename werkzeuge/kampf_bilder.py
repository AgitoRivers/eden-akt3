# -*- coding: utf-8 -*-
r"""Kampfbilder ins Modul holen (19.10.2026): Posen der Gegner aus der ComfyUI-Ausgabe (Prompt Studio, Ordner
combat\<Sprite>\) verkleinert als WebP nach module\<modul>\kampf\<Sprite>\<pose>.webp, dazu ein Kopf-Ausschnitt
avatar.webp fuer die Zugfolge. Vorhandenes wird ueberschrieben (die Quelle ist massgeblich).

  python werkzeuge\kampf_bilder.py                     nur Gegner, die in kaempfe.json vorkommen
  python werkzeuge\kampf_bilder.py --gegner Thief,Lion  bestimmte Ordner
  python werkzeuge\kampf_bilder.py --alle               alle Ordner der Quelle (ohne *_TEST)
  --modul eden_rise   --quelle <Ordner>   --liste (nur anzeigen, nichts schreiben)
"""
import argparse, json, os, sys
from PIL import Image

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
POSEN = ("idle", "windup", "attack", "heavy_windup", "heavy_attack", "hurt", "guard", "weakened", "enraged", "flee",
         "surrender", "defeated", "victory", "death", "konter")   # konter nur bei Duc
HOEHE = 900


# Head position per enemy as (centre x, centre y) in fractions of the visible figure, plus the square's side as a
# fraction of the figure's longer edge - read off the idle pose (22.10.2026)
AVATAR_KOPF = {"Pigeon": (0.17, 0.16, 0.46), "PigeonAlpha": (0.17, 0.16, 0.46),
               "Seagull": (0.17, 0.18, 0.50), "SeagullAlpha": (0.18, 0.16, 0.46),
               "Wolf": (0.22, 0.36, 0.40), "LionAlpha": (0.22, 0.28, 0.42), "Kevin": (0.30, 0.33, 0.40), "YamamotoSamurai": (0.47, 0.075, 0.2), "Rat": (0.64, 0.38, 0.40),
               "Snake": (0.29, 0.15, 0.34), "SnakeAlpha": (0.30, 0.11, 0.34), "YasinDrone": (0.57, 0.235, 0.24), "Siren": (0.2, 0.22, 0.22), "MaxwellSteelMop": (0.49, 0.105, 0.2),
               # 26.10.2026: head was cut at the edge
               "Dog": (0.18, 0.24, 0.38), "DogAlpha": (0.18, 0.24, 0.38), "Bat": (0.31, 0.45, 0.30), "BatAlpha": (0.31, 0.45, 0.30),
               "RobotCobra": (0.21, 0.07, 0.26), "RobotScorpion": (0.30, 0.64, 0.34),
               "BoardingRobot": (0.42, 0.09, 0.3), "BoardingRobotHeavy": (0.39, 0.075, 0.26),
               "RussianBlue": (0.17, 0.24, 0.42), "Capybara": (0.16, 0.26, 0.46), "Tortoise": (0.13, 0.28, 0.34), "BeardedVulture": (0.2, 0.2, 0.36),
               "RedPanda": (0.18, 0.22, 0.42), "SnowLeopard": (0.16, 0.22, 0.36), "Komodo": (0.13, 0.2, 0.3)}
AVATAR_KOPF.update({n + "Frei": AVATAR_KOPF[n] for n in ("RussianBlue", "Capybara", "Tortoise", "BeardedVulture", "RedPanda", "SnowLeopard", "Komodo", "Wolf", "Dog")})
AVATAR_KOPF["BeardedVulture"] = (0.07, 0.64, 0.24)   # flies since 01.11.2026: head low on the left, under the wings; the station bird still stands


def avatar(im, name=""):
    """Quadrat um den Kopf: oberste deckende Pixel, Seite ~ 24 % der Figurhoehe (Tiere: 40 % der Breite)."""
    im = im.convert("RGBA")
    a = im.split()[3]
    # bbox of the visible figure only: transparent pixels still carry colour values, so im.getbbox() returned the
    # whole canvas (22.10.2026: empty Rat avatar, wrong crops for small/shrunk figures)
    l, o, r, u = a.point(lambda v: 255 if v > 128 else 0).getbbox() or (0, 0, im.width, im.height)
    hoch = (u - o) > (r - l)
    if name in AVATAR_KOPF:                  # head not where the rule expects it (beak/snout ahead, drone above)
        cx, cy, s = AVATAR_KOPF[name]
        seite = int(max(r - l, u - o) * s)
        mx, my = l + int((r - l) * cx), o + int((u - o) * cy)
        box = (mx - seite // 2, my - seite // 2, mx - seite // 2 + seite, my - seite // 2 + seite)
        kopf = im.crop(box)
        hinter = Image.new("RGBA", kopf.size, (21, 23, 29, 255))
        hinter.alpha_composite(kopf)
        return hinter.convert("RGB").resize((160, 160), Image.LANCZOS)
    if hoch:
        # 26.10.2026: the square started below the top pixel and cut off every human's crown (Duc, Maxwell, Agent ...).
        # Now a little air above the hair, the head centre from the forehead rows (8-12 % down).
        h = u - o
        seite = int(h * 0.26)
        xs = []
        for f in (0.08, 0.10, 0.12):
            reihe = o + int(h * f)
            xs += [x for x in range(l, r) if a.getpixel((x, reihe)) > 128]
        xs.sort()
        mitte = xs[len(xs) // 2] if xs else (l + r) // 2
        oben = o - int(seite * 0.07)
    else:                                   # liegende Figur (Hund, Hai, Schlange ...): Kopf meist links vorne
        seite = int((r - l) * 0.40)
        mitte = l + seite // 2
        oben = o + max(0, ((u - o) - seite) // 3)
    box = (max(0, mitte - seite // 2), max(0, oben), max(0, mitte - seite // 2) + seite, max(0, oben) + seite)
    kopf = im.crop(box)
    hinter = Image.new("RGBA", kopf.size, (21, 23, 29, 255))
    hinter.alpha_composite(kopf)
    return hinter.convert("RGB").resize((160, 160), Image.LANCZOS)


# ---- size normalisation (Duc 22.10.2026): the poses come on different canvases (portrait, landscape, lying) and the
# figure fills them differently, so the same enemy jumped in size between poses in the combat screen. Every exported
# pose now sits on ONE canvas matching the sprite box of the combat screen (eden-combat.css .gsprite: 70 % height,
# max 46 % width of a 16:9 stage), bottom-centred. The idle pose sets the enemy's scale (humans by height, animals by
# visible area relative to a human); every other pose is scaled so its visible AREA matches idle, so a lunging or
# lying pose keeps the same body size. GROESSE: size of a species relative to an adult human (default 1.0).
CANVAS = (1170, 1000)
REF_H = 0.86                     # an adult human's idle pose fills 86 % of the canvas height
HUMAN_SHAPE = 0.47               # sqrt(visible area) / height of an average human idle pose (Thief, Agent, Pirate ...)
ANIMAL_BOOST = 1.4               # an animal's bulk reads smaller than a human's at equal area - first look at the sheet (22.10.)
GROESSE = {
    "Rat": 0.36, "RatAlpha": 0.44, "Pigeon": 0.34, "PigeonAlpha": 0.42, "Bat": 0.42, "BatAlpha": 0.5,
    "Seagull": 0.44, "SeagullAlpha": 0.52, "Snake": 0.62, "SnakeAlpha": 0.72, "Dog": 0.62, "DogAlpha": 0.72,
    "WildschweinKlein": 0.45, "Wildschwein": 0.62, "WildschweinKeiler": 0.75,
    "Wolf": 0.78, "WolfAlpha": 0.88, "Panther": 0.84, "PantherAlpha": 0.94, "Lion": 0.95, "LionAlpha": 1.05,
    "Ape": 0.95, "ApeAlpha": 1.05, "Grizzly": 1.05, "GrizzlyAlpha": 1.15, "Shark": 1.0, "SharkAlpha": 1.1,
    "SeaMonster": 1.25, "Unit1": 1.05, "RobotCobra": 0.75, "RobotScorpion": 0.7, "BoardingRobot": 1.1, "BoardingRobotHeavy": 1.25,
    # Red Trio (Duc 30.10.2026): standen wie Menschen auf voller Hoehe
    "ArkHyena": 0.62, "PlatedMouflon": 0.8, "BearCub": 0.55, "LionPlated": 0.95,
    # Tierstation (Duc 01.11.2026); <Name>Frei = dasselbe Tier an der Station, ohne Halsband
    "RussianBlue": 0.38, "Capybara": 0.6, "Tortoise": 0.5, "BeardedVulture": 0.62, "RedPanda": 0.42, "SnowLeopard": 0.8, "Komodo": 0.85,
}
GROESSE.update({n + "Frei": GROESSE[n] for n in ("RussianBlue", "Capybara", "Tortoise", "BeardedVulture", "RedPanda", "SnowLeopard", "Komodo", "Dog", "ArkHyena", "Wolf", "Panther", "Grizzly", "PlatedMouflon", "Ape", "BearCub", "WildschweinKeiler")})
# In the air (Duc 01.11.2026): lifted by this share of the canvas height, except the poses on the ground
FLUG = {"BeardedVulture": 0.22}
AM_BODEN = ("surrender", "defeated", "death")


# Head height per human (crown to chin, without hat or hood) in the idle pose at 86 % canvas height, measured by hand. A stooped
# figure has a bigger head at equal height, so humans looked different in size (Duc 31.10.2026). Half the correction towards
# Duc's head: full correction makes the head equal, but stooped figures like Bibi read as small. KOPF_STAERKE 1.0 is full.
ZIELKOPF, KOPF_UNTEN, KOPF_OBEN, KOPF_STAERKE = 128, 0.85, 1.12, 0.5
KOPF = {"DucErdeBat": 128, "Danzel": 128, "Bibi": 145, "Charly": 125, "Agent": 128, "AgentAlpha": 131, "Alon": 152, "Brute": 147, "BruteAlpha": 145,
        "Thief": 115, "ThiefAlpha": 143, "ThiefArab": 105, "Pirate": 150, "PirateAlpha": 120, "PirateTorch": 153, "MaxwellSports": 142, "MaxwellMaximum": 142, "MaxwellSteelMop": 105, "PirateBrawler": 112, "PirateGunner": 105, "AgentGunman": 117,
        "MaxwellSteward": 132, "Wolff": 125, "Bonaventure": 112, "Heinrich": 152, "Paparazzo": 135, "Vampire": 145, "Mime": 115, "DrunkCasanova": 181, "YasinDrone": 156, "YamamotoSamurai": 122}


def kopf_faktor(name):
    if name not in KOPF:
        return 1.0
    return max(KOPF_UNTEN, min(KOPF_OBEN, ZIELKOPF / KOPF[name])) ** KOPF_STAERKE


def figure(im):
    """bbox and visible area (alpha > 128) of a sprite."""
    m = im.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    bb = m.getbbox()
    return bb, (m.histogram()[255] if bb else 0)


def idle_scale(idle, name):
    bb, area = figure(idle)
    if not bb or not area:
        return None, None
    H = CANVAS[1]
    if name in GROESSE:                           # animals: by area, relative to a human
        s = GROESSE[name] * ANIMAL_BOOST * HUMAN_SHAPE * REF_H * H / area ** 0.5
    else:                                         # humans: by height
        s = REF_H * H / (bb[3] - bb[1]) * kopf_faktor(name)
    return s, area


def normalise(im, s_idle, area_idle, heben=0.0):
    """Pose on the common canvas with the enemy's scale; its visible area matches idle."""
    bb, area = figure(im)
    W, H = CANVAS
    if not bb or not area or not s_idle:
        return im
    s = s_idle * (area_idle / area) ** 0.5
    fig = im.crop(bb)
    s = min(s, 0.96 * W / fig.width, 0.96 * H / fig.height)       # never touch the canvas edges
    fig = fig.resize((max(1, round(fig.width * s)), max(1, round(fig.height * s))), Image.LANCZOS)
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    out.alpha_composite(fig, ((W - fig.width) // 2, max(0, H - fig.height - int(H * (0.02 + heben)))))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--modul", default="eden_rise")
    ap.add_argument("--quelle", default=QUELLE)
    ap.add_argument("--gegner", default="")
    ap.add_argument("--alle", action="store_true")
    ap.add_argument("--liste", action="store_true")
    args = ap.parse_args()
    ziel = os.path.join(EDEN, "module", args.modul, "kampf")
    if args.gegner:
        namen = [n for n in args.gegner.split(",") if n]
    elif args.alle:
        namen = sorted(n for n in os.listdir(args.quelle) if os.path.isdir(os.path.join(args.quelle, n)) and not n.endswith("_TEST"))
    else:
        defs = json.load(open(os.path.join(EDEN, "module", args.modul, "kaempfe.json"), encoding="utf-8"))
        namen = sorted({g["sprite"] for g in defs["gegner"].values() if g.get("sprite")})
    print("Gegner:", ", ".join(namen) or "keine")
    for n in namen:
        q = os.path.join(args.quelle, n)
        da = [p for p in POSEN if os.path.isfile(os.path.join(q, p + ".png"))]
        fehlt = [p for p in POSEN if p not in da]
        print("  %-14s %2d Posen%s" % (n, len(da), (" – fehlen: " + ", ".join(fehlt)) if fehlt else ""))
        if args.liste or not da:
            continue
        os.makedirs(os.path.join(ziel, n), exist_ok=True)
        ref = os.path.join(q, "idle.png") if "idle" in da else os.path.join(q, da[0] + ".png")
        s_idle, area_idle = idle_scale(Image.open(ref).convert("RGBA"), n)
        for p in da:
            im = normalise(Image.open(os.path.join(q, p + ".png")).convert("RGBA"), s_idle, area_idle, 0 if p in AM_BODEN else FLUG.get(n, 0))
            if im.height > HOEHE:
                im = im.resize((round(im.width * HOEHE / im.height), HOEHE), Image.LANCZOS)
            im.save(os.path.join(ziel, n, p + ".webp"), "WEBP", quality=86)
        quelle_av = os.path.join(q, "idle.png") if "idle" in da else os.path.join(q, da[0] + ".png")
        avatar(Image.open(quelle_av), n).save(os.path.join(ziel, n, "avatar.webp"), "WEBP", quality=86)
    if not args.liste:
        print("geschrieben nach", ziel)


if __name__ == "__main__":
    main()

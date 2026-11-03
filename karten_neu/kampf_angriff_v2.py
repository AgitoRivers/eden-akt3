# -*- coding: utf-8 -*-
r"""Kampf-Sprites: Angriffsposen neu, damit Ausholen und Schlag fuer die Parade ("Sprite lesen") auf einen Blick
verschieden sind (19.10.2026, Duc: "Ja und neu generieren"). Pose-Regeln aus der Hauptsitzung:
windup = weit zurueckgezogen, Gewicht hinten, Tiere Maul ZU; attack = voll gestreckt nach vorn, Ausfallschritt,
Bewegungsunschaerfe, Tiere Maul WEIT OFFEN; heavy_* = dasselbe uebertrieben, mit Ankuendigung (Gluehen/Funken).
Snake ist das Vorbild und bleibt.

Je Gruppe (Menschen/Humanoide, Raubtiere, Moewe, Maschinen) eigene Kartentexte, nur fuer diesen Lauf gesetzt
und danach zurueckgesetzt (Prompt Studio baut den Prompt beim Einstellen). Alte Bilder wandern nach
output\_expressions_papierkorb\combat\<Name>\<Zeit>.

    kampf_angriff_v2.py          Probelauf
    kampf_angriff_v2.py --los    stellt ein
"""
import io, json, os, shutil, subprocess, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
LOS = "--los" in sys.argv
PS = "http://127.0.0.1:8301"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
HIER = os.path.dirname(os.path.abspath(__file__))

T = {
    "mensch": {
        "windup": "winding up a strike, the striking arm and weapon pulled far back behind the head, upper body leaning "
                  "back, weight on the back leg, eyes locked to the left",
        "attack": "striking forward to the left with full force, the striking arm and weapon fully extended straight "
                  "forward, a long lunging step forward, slight motion blur on the arm and weapon",
        "heavy_windup": "winding up a devastating two-handed blow, the whole body twisted back and coiled, both arms "
                        "raised high behind the head, teeth clenched, a faint glow of power around the fists and weapon",
        "heavy_attack": "unleashing a devastating all-out two-handed blow down and forward to the left, the whole body "
                        "swinging into it in a deep lunge, both arms fully extended, motion blur on the arms and weapon, "
                        "dust flying",
    },
    "tier": {
        "windup": "crouched low and tense, head pulled back, jaws firmly closed, ready to pounce to the left",
        "attack": "lunging forward to the left, head thrust far forward, jaws wide open biting, slight motion blur",
        "heavy_windup": "rearing up and gathering all its strength, body coiled, jaws firmly closed, teeth clenched, "
                        "muscles trembling with power",
        "heavy_attack": "launching a devastating leap forward to the left, the whole body stretched out in the air, jaws "
                        "open as wide as possible, motion blur, spray flying",
    },
    "moewe": {
        "windup": "head pulled back, beak firmly closed, crouched and puffed up, ready to peck to the left",
        "attack": "pecking forward to the left, neck fully stretched out, beak wide open, slight motion blur",
        "heavy_windup": "both wings raised high above its body, chest puffed up, beak firmly closed, ready to dive",
        "heavy_attack": "diving forward to the left with both wings spread wide, beak wide open, motion blur",
    },
    "maschine": {
        "heavy_windup": "rearing back on its hydraulic legs, both cable arms pulled far back, its red eye light glowing "
                        "intensely, sparks crackling all over its body",
        "heavy_attack": "slamming forward to the left with its whole body, both cable arms fully extended in a massive "
                        "punch, motion blur, sparks and black smoke bursting",
    },
}
LEICHT, SCHWER, ALLE = ["windup", "attack"], ["heavy_windup", "heavy_attack"], ["windup", "attack", "heavy_windup",
                                                                              "heavy_attack"]
LAEUFE = [  # (Gruppe, Gegner, Karten)
    ("mensch", ["Ape", "Agent", "DrunkCasanova"], ALLE),
    ("mensch", ["Heinrich", "Mime", "Siren"], SCHWER),
    ("mensch", ["Thief", "Paparazzo", "Pirate", "Alien", "Brute", "Vampire"], LEICHT),
    ("tier", ["Shark", "SeaMonster", "Lion", "Dog"], SCHWER),
    ("moewe", ["Seagull"], ALLE),
    ("maschine", ["Unit1", "Unit1White"], SCHWER),
]


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


n = sum(len(g) * len(k) for _, g, k in LAEUFE)
for gruppe, gegner, karten in LAEUFE:
    print("%-8s %-40s %s" % (gruppe, ",".join(gegner), ",".join(karten)))
print("Bilder:", n)
if not LOS:
    sys.exit("PROBELAUF")
stempel = time.strftime("%Y-%m-%d_%H%M%S")
d = ps("/api/state")["decks"]
original = {c["name"]: c["prompt"] for c in d["kampf"]}
try:
    for gruppe, gegner, karten in LAEUFE:
        for name in gegner:
            for k in karten:
                f = os.path.join(OUT, "expressions", "combat", name, k + ".png")
                if os.path.exists(f):
                    z = os.path.join(OUT, "_expressions_papierkorb", "combat", name, stempel)
                    os.makedirs(z, exist_ok=True)
                    shutil.move(f, z)
        for k in karten:
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == k:
                    c["prompt"] = T[gruppe][k]
            ps("/api/decks", d)
            subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", k, "--gegner", ",".join(gegner)],
                           check=True, stdout=subprocess.DEVNULL)
finally:
    d = ps("/api/state")["decks"]
    for c in d["kampf"]:
        if c["name"] in original:
            c["prompt"] = original[c["name"]]
    ps("/api/decks", d)
print("eingestellt: %d Bilder, Kartentexte zurueckgesetzt" % n)

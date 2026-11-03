# -*- coding: utf-8 -*-
r"""Volllauf fuer die 10 neuen Kampf-Gegner aus Ducs Element-/Stufen-Konzept (19.10.2026):
PirateTorch, ThiefArab, Pigeon, Bat, Rat, Alon, YasinDrone, MaxwellSteward, MaxwellSports, MaxwellMaximum.
- Ruhe-/Reaktionsposen mit den normalen Kampf-Karten; defeated/death der aufrechten Figuren im Querformat.
- Angriffsposen direkt nach den Parade-Regeln (Gruppen-Texte wie kampf_angriff_v2.py), OHNE Leuchten/Funken
  (das macht spaeter die Kampf-Effektschicht). Kartentexte nur fuer den Lauf, danach zurueckgesetzt.
Danach: kampf_flee_spiegeln.py --los und kampf_klein.py --los.

    kampf_volllauf_runde3.py --los
"""
import io, json, os, subprocess, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if "--los" not in sys.argv:
    sys.exit("PROBELAUF - mit --los einstellen")
PS = "http://127.0.0.1:8301"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
HIER = os.path.dirname(os.path.abspath(__file__))
MENSCHEN = ["PirateTorch", "ThiefArab", "Alon", "YasinDrone", "MaxwellSteward", "MaxwellSports", "MaxwellMaximum",
            "YamamotoSamurai", "DucErdeSword", "Wolff"]
TIERE = ["Rat", "WildschweinKlein", "Wildschwein", "WildschweinKeiler"]
FLUG = ["Pigeon", "Bat"]
sys.path.insert(0, HIER)
from kampf_alphas import GROUPS as _ALPHA   # Alpha-Varianten (22.10.2026)
MENSCHEN, TIERE, FLUG = MENSCHEN + _ALPHA["mensch"], TIERE + _ALPHA["tier"], FLUG + _ALPHA["flug"]
if "--gegner" in sys.argv:          # only these enemies, e.g. --gegner Alon (20.10.2026)
    _nur = set(sys.argv[sys.argv.index("--gegner") + 1].split(","))
    MENSCHEN, TIERE, FLUG = ([g for g in x if g in _nur] for x in (MENSCHEN, TIERE, FLUG))
RUHE = ["idle", "guard", "hurt", "enraged", "weakened", "surrender", "flee", "victory"]
T = {
    "mensch": {
        "windup": "winding up a strike, the striking arm and weapon pulled far back behind the head, upper body leaning "
                  "back, weight on the back leg, eyes locked to the left",
        "attack": "striking forward to the left with full force, the striking arm and weapon fully extended straight "
                  "forward, a long lunging step forward, slight motion blur on the arm and weapon",
        "heavy_windup": "winding up a devastating two-handed blow, the whole body twisted back and coiled, both arms "
                        "raised high behind the head, teeth clenched, every muscle tensed",
        "heavy_attack": "unleashing a devastating all-out two-handed blow down and forward to the left, the whole body "
                        "swinging into it in a deep lunge, both arms fully extended, motion blur on the arms and weapon",
    },
    "tier": {
        "windup": "crouched low and tense, head pulled back, jaws firmly closed, ready to pounce to the left",
        "attack": "lunging forward to the left, head thrust far forward, jaws wide open biting, slight motion blur",
        "heavy_windup": "rearing up on its hind legs gathering all its strength, body coiled, jaws firmly closed, "
                        "muscles trembling",
        "heavy_attack": "launching a devastating leap forward to the left, the whole body stretched out in the air, jaws "
                        "open as wide as possible, motion blur",
    },
    "flug": {
        "windup": "both wings half spread and raised up behind its body, head drawn far back, mouth closed, ready to "
                  "strike to the left",
        "attack": "wings tucked tight, neck and head stretched far forward to the left in a fast lunge, mouth wide open, "
                  "slight motion blur on the head",
        "heavy_windup": "both wings raised high above its body, chest puffed up, mouth closed, ready to dive",
        "heavy_attack": "diving steeply forward and down to the left with wings folded tight, mouth wide open, motion blur",
    },
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def lauf(karten, gegner, quer=False):
    if not gegner:
        return
    arg =[PY, os.path.join(HIER, "kampf_test.py"), "--karten", ",".join(karten), "--gegner", ",".join(gegner)]
    if quer:
        arg.insert(2, "--quer")
    subprocess.run(arg, check=True, stdout=subprocess.DEVNULL)


alle = MENSCHEN + TIERE + FLUG
lauf(RUHE, alle)
lauf(["defeated"], MENSCHEN, quer=True)
lauf(["defeated", "death"], TIERE + FLUG)
original = {c["name"]: c["prompt"] for c in ps("/api/state")["decks"]["kampf"]}
try:
    for gruppe, gegner in (("mensch", MENSCHEN), ("tier", TIERE), ("flug", FLUG)):
        for k, text in T[gruppe].items():
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == k:
                    c["prompt"] = text
            ps("/api/decks", d)
            lauf([k], gegner)
finally:
    d = ps("/api/state")["decks"]
    for c in d["kampf"]:
        if c["name"] in original:
            c["prompt"] = original[c["name"]]
    ps("/api/decks", d)
n = len(alle) * len(RUHE) + len(MENSCHEN) + 2 * len(TIERE + FLUG) + 4 * len(alle)
print("eingestellt: ca. %d Bilder, Kartentexte zurueckgesetzt" % n)

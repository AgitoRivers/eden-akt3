# -*- coding: utf-8 -*-
r"""Kampf-Sprites, Korrektur nach der ersten Pruefung (19.10.2026):
- weakened zeigte Blut ("wounded"), defeated/death lagen nicht, flee lief nach links, Schlange mit zweitem Kopf,
  Unit-01 wieder mit Lochgittern.
- Karten live ueber die Studio-API, Negativ-Sperre in allen Kampf_*-Presets, Unit-01-Merkmale neu,
  Quellen studio_kampf_gegner.py / kampf_prompts_v2.py nachgezogen.

    kampf_korrektur_1.py          Probelauf
    kampf_korrektur_1.py --los    schreibt
"""
import io, json, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
PS = "http://127.0.0.1:8301"
F_PRESETS = r"X:\AI\PromptStudio\presets.json"
KARTEN = {
    "weakened": ("exhausted and wounded, swaying, struggling to stay upright, panting heavily",
                 "exhausted and worn out, swaying on unsteady legs, panting heavily, slumped and sweaty, barely able to "
                 "stand"),
    "defeated": ("knocked out, collapsed on the ground, limp, eyes closed, dazed",
                 "knocked out cold, lying flat on its side on the ground, the whole body fully horizontal, limp, eyes "
                 "closed"),
    "death": ("slain, lying motionless on the ground, lifeless, eyes empty",
              "dead, lying motionless flat on its side on the ground, the whole body fully horizontal, eyes closed, "
              "completely still"),
    "flee": ("turning away and fleeing to the right in panic, looking back over its shoulder in fear",
             "running away in panic, looking back over its shoulder in fear"),
}
UNIT1_ALT = None
UNIT1 = ("a boxy dented orange-painted steel generator body where every side is completely smooth flat painted sheet "
         "metal, a broad yellow-and-black hazard stripe band around the middle, a riveted access hatch, two thick "
         "hydraulic legs, two exhaust pipes on top belching black smoke, loose sparking cables hanging like arms, one "
         "round red warning light as its single eye, black stencil letters UNIT-01 on its side")
SPERRE = " blood, gore, bleeding, open wounds, two heads, extra head, duplicate head,"


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


for k, (_, neu) in KARTEN.items():
    print("%-9s %s" % (k, neu))
if not LOS:
    sys.exit("PROBELAUF")
d = ps("/api/state")["decks"]
for c in d["kampf"]:
    if c["name"] in KARTEN:
        c["prompt"] = KARTEN[c["name"]][1]
for c in d["outfit"]:
    if c["name"] == "kampf_unit1":
        UNIT1_ALT = c["prompt"]
        c["prompt"] = UNIT1
ps("/api/decks", d)
p = dc.load_json(F_PRESETS, None, "Studio")
for k, v in p.items():
    if k.startswith("Kampf_") and "two heads" not in v["negative_prompt"]:
        v["negative_prompt"] = v["negative_prompt"].rstrip() + SPERRE
dc.save_json(F_PRESETS, p, "Studio")
# Quellen
q1 = r"X:\AI\Eden\karten_neu\studio_kampf_gegner.py"
t = open(q1, encoding="utf-8").read()
for alt, neu in KARTEN.values():
    t = t.replace('"%s"' % alt, json.dumps(neu))
t = t.replace('suction cups, suckers,")', 'suction cups, suckers,"\n       "%s")' % SPERRE)
open(q1, "w", encoding="utf-8", newline="\n").write(t)
q2 = r"X:\AI\Eden\karten_neu\kampf_prompts_v2.py"
t = open(q2, encoding="utf-8").read()
if UNIT1_ALT and json.dumps(UNIT1_ALT) in t:
    t = t.replace(json.dumps(UNIT1_ALT), json.dumps(UNIT1))
open(q2, "w", encoding="utf-8", newline="\n").write(t)
print("geschrieben | Quelle Unit1 neu:", UNIT1 in t)

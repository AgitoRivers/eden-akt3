# -*- coding: utf-8 -*-
r"""Neue Red-Trio-Gegner: Posen als Krea-Edit des freigegebenen idle (30.10.2026). Der erste t2i-Lauf brachte Haende am
Mufflon, Pistolen bei Hyaene und Loewe und fremde Figuren unter der Drohne, weil die Kartentexte fuer Menschen sind.
Die freigegebenen idle von Loewe und Mufflon sind unten abgeschnitten; dort dient victory des ersten Laufs als Vorlage
(--quelle victory) und idle wird mit neu erzeugt.
Gleiches Verfahren wie kampf_nachbessern.py (22.10.: jede Tierpose ist ein Edit des Ganzkoerperbilds).

    red_trio_posen.py <Name> [--posen a,b]       Name: LionPlated, PlatedMouflon, ArkHyena, ShepherdDrone
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
NAME = sys.argv[1]
REST = sys.argv[2:]
sys.argv = [sys.argv[0]]
_HALTEN = [sys.stdout]
import kampf_edit as KE  # noqa: E402
_HALTEN.append(sys.stdout)

GANZ = ("; the whole animal from head to tail with all paws fully inside the image, wide empty space around it, the same "
        "camera distance as in the reference")
IDLE = "it stands on all four legs in a tense hostile fighting stance, body angled to the left, ready to attack"
TIER = {
    "windup": "it crouches low and tense, head pulled back, jaws firmly closed, ready to pounce to the left",
    "attack": "it lunges forward to the left, head thrust far forward, jaws wide open biting",
    "heavy_windup": "it crouches very low on bent legs gathering all its strength, body coiled like a spring, head down",
    "heavy_attack": "it launches a devastating leap forward to the left, the whole body stretched out in the air, jaws open",
    "guard": "it crouches low and defensive on all four legs, head lowered between its shoulders, body pulled back, ready to dodge",
    "hurt": "it flinches back from a hit standing on its legs, head jerked aside, one front leg lifted off the ground",
    "enraged": "it roars with jaws wide open, hackles raised, the whole body tensed and leaning forward",
    "weakened": "it staggers exhausted on all four legs, head hanging low, panting, legs trembling",
    "defeated": "it lies collapsed flat on its side on the floor with exactly one head, all four legs limp and stretched out, "
                "the head resting on the floor on the right side of the image, eyes closed, knocked out",
    "surrender": "it cowers low to the floor on all four legs, ears flat, tail tucked, head turned away submissively",
    "flee": "it turns and runs away to the right on all four legs, looking back over its shoulder",
    "victory": "it stands tall on all four legs and roars triumphantly with its head raised high",
    "death": "it lies dead and motionless flat on its side on the floor with exactly one head, all four legs stretched out, "
             "the head on the right side of the image, eyes closed",
}
BOCK = dict(TIER, attack="it charges forward to the left with its head lowered, horns first, all four legs in a hard run",
            windup="it stands braced with its head lowered, horns forward, one front hoof scraping the floor",
            heavy_windup="it backs up with its head low, all four legs bent and tensed, ready to ram",
            heavy_attack="it rams forward to the left at full speed with the horns first, all four hooves off the floor",
            enraged="it stamps with its head lowered and horns forward, nostrils flared, the whole body tensed",
            victory="it stands tall on all four legs with its head and horns raised high")
BOCK = {k: v.replace("paws", "hooves") for k, v in BOCK.items()}
DROHNE = {
    "windup": "it tilts backwards with the nose up, hovering in place, the curved emitter under it swinging forward to the left",
    "attack": "it dives forward to the left, the whole body tilted steeply, the curved emitter pointing to the left",
    "heavy_windup": "it hovers high in the image, level and perfectly still, the curved emitter fully extended downwards",
    "heavy_attack": "it dives very steeply and fast to the lower left, the whole body tilted almost vertically",
    "guard": "it pulls back and up to the right, tilted away, the landing legs drawn up",
    "hurt": "it is knocked sideways in the air, tipped over at a steep angle, one rotor arm bent, a thin wisp of grey smoke",
    "enraged": "it hovers level and faces the viewer directly, the single red light bright, all rotors spinning hard",
    "weakened": "it hangs crooked in the air, one rotor stopped, a thin wisp of grey smoke rising from its body",
    "defeated": "it has crashed and lies tilted on the bare floor, rotors stopped and bent, the red light dark, a wisp of smoke",
    "surrender": "it has landed upright on its four landing legs on the bare floor, rotors stopped, the red light dark",
    "flee": "it flies away to the right, tilted forward towards the right edge, seen from slightly behind",
    "victory": "it hovers high in the image, level and steady, all rotors spinning, the single red light on",
    "death": "it lies smashed on the bare floor, broken into a few large pieces, rotors snapped off, the red light dark, a wisp of smoke",
}
LICHT = "No camera flash, no motion streaks of light."
KE.GEGNER.update({
    "LionPlated": {"wer": "huge black lion with jet-black fur and a thick black mane, starved with visible ribs, old pale scars, "
                          "exactly one large curved brushed steel plate bolted onto each shoulder and nowhere else, its back, flanks "
                          "and chest are bare black fur without any armour or straps (Duc 30.10.: nur Schulterplatten), a chrome "
                          "collar with one small red light",
                   "waffe": "", "licht": LICHT, "posen": dict({k: v + GANZ for k, v in TIER.items()}, idle=IDLE + GANZ)},
    "PlatedMouflon": {"wer": "massive mouflon ram with dark brown fur, huge curled horns, heavy brushed steel armour plates with "
                             "hinges and bolts on its chest, shoulders and back, a chrome collar with one small red light, a real "
                             "four-legged animal with hooves",
                      "waffe": "", "licht": LICHT, "posen": dict({k: v + GANZ.replace("paws", "hooves") for k, v in BOCK.items()}, idle=IDLE + GANZ.replace("paws", "hooves"))},
    "ArkHyena": {"wer": "scarred spotted hyena with thin patchy fur, shaved squares and old surgical scars on its flank, a chrome "
                        "collar with one small red light, a real four-legged animal",
                 "waffe": "", "licht": LICHT, "posen": {k: v + GANZ for k, v in TIER.items()}},
    "ShepherdDrone": {"wer": "grey military drone with exactly four propellers on four arms, a thin antenna on top, a sensor dome "
                             "below, a short curved metal emitter hanging under it, one small red light. It is a machine; there "
                             "is no person, no animal and no robot in the image",
                      "waffe": "", "licht": LICHT,
                      "posen": {k: v + "; the whole drone fully inside the image, wide empty space around it, only one single "
                                "drone" for k, v in DROHNE.items()}},
})
KE.W, KE.H = 1328, 880      # Quertiere und Drohne

sys.argv = [sys.argv[0], NAME] + REST + ["--skala", "0.72"]
KE.main()

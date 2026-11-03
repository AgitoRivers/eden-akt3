# -*- coding: utf-8 -*-
r"""BearCub: die 10 fehlenden Kampf-Posen (Auftrag Kampf-Session 29.10.2026). idle, hurt und flee gibt es schon.
Aufbau wie kampf_volllauf_runde3.py, aber nur fuer BearCub und mit Baerchen-Texten fuer die Angriffe: ein Junges
schlaegt mit der Tatze und blufft, es springt nicht toedlich. Prioritaet zuerst: windup, attack, guard, surrender.
Kartentexte nur fuer den Lauf, danach zurueckgesetzt. Danach: Kampf_Bilder.bat --gegner BearCub (nach Ducs Abnahme).

    kampf_bearcub.py          Probelauf
    kampf_bearcub.py --los    braucht Prompt Studio (8301) und ComfyUI Krea2 (8189)
"""
import io, json, os, subprocess, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
HIER = os.path.dirname(os.path.abspath(__file__))
WER = "BearCub"
# eigene Texte fuer die Angriffs-Karten; die Ruheposen laufen mit den normalen Kampf-Karten
ANGRIFF = {
    "windup": "crouched low on all fours, head pulled back, ears flat, one oversized front paw lifted and drawn back, "
              "ready to swat to the left",
    "attack": "lunging forward to the left, one oversized front paw swiping through the air with claws out, mouth open "
              "in a small squeaky growl, slight motion blur on the paw",
    "heavy_windup": "rearing up on its hind legs to look bigger, both front paws raised high, fur puffed up, mouth "
                    "closed, wobbling a little",
    "heavy_attack": "dropping forward from its hind legs onto the left with both front paws slamming down, mouth wide "
                    "open in a bluff roar, motion blur on the paws",
}
ZUERST = ["guard", "surrender"]                 # Ruheposen mit Prioritaet
DANACH = ["weakened", "enraged", "victory", "defeated"]


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def lauf(karten):
    subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", ",".join(karten), "--gegner", WER],
                   check=True, stdout=subprocess.DEVNULL)
    print("eingereiht:", ", ".join(karten))


def angriffe(namen):
    original = {c["name"]: c["prompt"] for c in ps("/api/state")["decks"]["kampf"]}
    try:
        for k in namen:
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == k:
                    c["prompt"] = ANGRIFF[k]
            ps("/api/decks", d)
            lauf([k])
    finally:
        d = ps("/api/state")["decks"]
        for c in d["kampf"]:
            if c["name"] in original:
                c["prompt"] = original[c["name"]]
        ps("/api/decks", d)


if "--los" not in sys.argv:
    print("PROBELAUF - Reihenfolge:", "windup, attack", "|", ", ".join(ZUERST), "|", "heavy_windup, heavy_attack", "|",
          ", ".join(DANACH))
    sys.exit("mit --los einstellen")
angriffe(["windup", "attack"])
lauf(ZUERST)
angriffe(["heavy_windup", "heavy_attack"])
lauf(DANACH)
print("eingestellt: 10 Posen fuer %s, Kartentexte zurueckgesetzt" % WER)

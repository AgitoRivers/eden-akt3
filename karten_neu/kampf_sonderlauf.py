# -*- coding: utf-8 -*-
r"""Kampf-Sprites: einzelne Karte fuer einzelne Gegner mit VORUEBERGEHEND anderem Kartentext neu erzeugen
(19.10.2026). Beispiel: Schlange/Hund ohne Haende, Vampirin ohne Blut. Der Kartentext wird danach zurueckgesetzt;
das alte Bild wandert nach output\_expressions_papierkorb\combat\<Name>\<Zeit>.

    kampf_sonderlauf.py <karte> <Gegner,Gegner> "<Kartentext>"
"""
import io, json, os, shutil, subprocess, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
karte, gegner, text = sys.argv[1], sys.argv[2], sys.argv[3]


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def setzen(neu):
    d = ps("/api/state")["decks"]
    alt = None
    for c in d["kampf"]:
        if c["name"] == karte:
            alt, c["prompt"] = c["prompt"], neu
    ps("/api/decks", d)
    return alt


stempel = time.strftime("%Y-%m-%d_%H%M%S")
for n in gegner.split(","):
    f = os.path.join(OUT, "expressions", "combat", n, karte + ".png")
    if os.path.exists(f):
        z = os.path.join(OUT, "_expressions_papierkorb", "combat", n, stempel)
        os.makedirs(z, exist_ok=True)
        shutil.move(f, z)
original = setzen(text)
try:
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "kampf_test.py"),
                    "--karten", karte, "--gegner", gegner], check=True)
finally:
    setzen(original)
print("Kartentext %s wieder zurueckgesetzt." % karte)

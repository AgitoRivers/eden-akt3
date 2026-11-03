# -*- coding: utf-8 -*-
r"""Alon in cyber armor (20.10.2026, Duc): one outfit_check test image per armor design, so Duc can pick the
design. The same designs are the variants of the armor item "Cyber-Armor" in werkzeuge\waffen_bilder.py
(variant k = design k). The outfit card kampf_alon is changed only for the run and restored afterwards.
Results: output\expressions\combat\Alon\_cyber\outfit_check_v<k>.png (the current outfit_check.png is kept).

    kampf_alon_cyber.py
"""
import io, json, os, shutil, subprocess, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "werkzeuge"))
import waffen_bilder as wb  # noqa: E402

PS = "http://127.0.0.1:8301"
ELON = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Alon"
TARGET = os.path.join(ELON, "_cyber")
CARD = "kampf_alon"
REST = ("dark jeans, white sneakers, aviator sunglasses, a chunky chrome jetpack strapped to his back with two exhaust "
        "nozzles")


def ps(path, data=None):
    req = urllib.request.Request(PS + path, data=None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def set_outfit(text):
    d = ps("/api/state")["decks"]
    old = None
    for c in d["outfit"]:
        if c["name"] == CARD:
            old, c["prompt"] = c["prompt"], text
    ps("/api/decks", d)
    return old


os.makedirs(TARGET, exist_ok=True)
current = os.path.join(ELON, "outfit_check.png")
backup = os.path.join(TARGET, "outfit_check_vorher.png")
if os.path.exists(current) and not os.path.exists(backup):
    shutil.copy2(current, backup)
original = None
try:
    for k, design in enumerate(wb.CYBER_DESIGNS, 1):
        if os.path.exists(current):
            os.remove(current)                      # a copy is in _cyber\outfit_check_vorher.png
        text = "wearing %s over his torso, %s" % (design, REST)
        old = set_outfit(text)
        original = original if original is not None else old
        subprocess.run([sys.executable, os.path.join(HERE, "kampf_test.py"), "--karten", "outfit_check",
                        "--gegner", "Alon"], check=True, stdout=subprocess.DEVNULL)
        t0 = time.time()
        while not os.path.exists(current) and time.time() - t0 < 900:
            time.sleep(3)
        time.sleep(2)
        if os.path.exists(current):
            shutil.move(current, os.path.join(TARGET, "outfit_check_v%d.png" % k))
            print("design %d done" % k)
        else:
            print("design %d: no image after 15 min" % k)
finally:
    if original is not None:
        set_outfit(original)
    if os.path.exists(backup) and not os.path.exists(current):
        shutil.copy2(backup, current)
print("outfit card restored")

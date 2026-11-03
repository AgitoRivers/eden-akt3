# -*- coding: utf-8 -*-
r"""Duc's approval of kampf_gesamt (22.10.2026 evening): redo the poses marked NEU, one after another (never two
touch-up runs at once). Most were cut off -> wider framing (--weit) and a smaller reference (--skala 0.5).
The thieves' guard loses the floating crowbar (text in kampf_nachbessern.py).

    kampf_nachbessern_runde3.py
"""
import json, os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
JOBS = [("Brute", "guard"), ("BruteAlpha", "guard"), ("DrunkCasanova", "guard"), ("Thief", "guard"),
        ("ThiefArab", "guard"), ("Alon", "hurt"), ("Alon", "heavy_windup"), ("AgentAlpha", "attack"),
        ("ApeAlpha", "guard"), ("ApeAlpha", "hurt"), ("ApeAlpha", "enraged"),
        ("Lion", "defeated"), ("Lion", "death"), ("WolfAlpha", "defeated"), ("WolfAlpha", "death"),
        ("Panther", "defeated"), ("Panther", "death"), ("PantherAlpha", "defeated"), ("PantherAlpha", "death")]


def idle():
    q = json.loads(urllib.request.urlopen("http://127.0.0.1:8189/queue", timeout=5).read())
    return not q["queue_running"] and not q["queue_pending"]


for name, pose in JOBS:
    r = subprocess.run([PY, os.path.join(HERE, "kampf_nachbessern.py"), name, "--posen", pose, "--weit",
                        "--skala", "0.5"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("%-14s %-13s %s" % (name, pose, "eingereiht" if r.returncode == 0 else "FEHLER " + r.stderr[-300:]),
          flush=True)
while not idle():
    time.sleep(5)
print("fertig", flush=True)

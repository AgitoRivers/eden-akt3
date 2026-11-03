# -*- coding: utf-8 -*-
r"""Second try for the four sprites of round 3 that still lost their legs at the bottom (22.10.2026)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for name, pose in (("Brute", "guard"), ("BruteAlpha", "guard"), ("DrunkCasanova", "guard"), ("AgentAlpha", "attack")):
    r = subprocess.run([sys.executable, os.path.join(HERE, "kampf_nachbessern.py"), name, "--posen", pose, "--weit",
                        "--fuesse", "--skala", "0.42"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(name, pose, "eingereiht" if r.returncode == 0 else "FEHLER " + r.stderr[-300:], flush=True)

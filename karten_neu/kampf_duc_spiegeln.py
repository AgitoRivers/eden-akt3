# -*- coding: utf-8 -*-
r"""Mirror Duc's combat sprites so he faces right (23.10.2026). Krea draws every figure facing left (towards Duc);
Duc stands on the left and must look right at the enemies. flee stays unmirrored: drawn running to the left = away
from the enemies. A marker file _gespiegelt.txt prevents mirroring twice.

    kampf_duc_spiegeln.py DucErdeSword          dry run
    kampf_duc_spiegeln.py DucErdeSword --los    mirror
"""
import io, os, sys
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
E = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat"
KEEP = {"flee", "outfit_check"}
for name in [a for a in sys.argv[1:] if not a.startswith("--")]:
    d = os.path.join(E, name)
    mark = os.path.join(d, "_gespiegelt.txt")
    if os.path.exists(mark):
        print("%s: schon gespiegelt" % name)
        continue
    files = sorted(f for f in os.listdir(d) if f.endswith(".png") and f[:-4] not in KEEP)
    print("%s: %d Posen spiegeln (%s)" % (name, len(files), ", ".join(f[:-4] for f in files)))
    if "--los" in sys.argv:
        for f in files:
            p = os.path.join(d, f)
            Image.open(p).transpose(Image.FLIP_LEFT_RIGHT).save(p)
        open(mark, "w").write("alle Posen ausser flee/outfit_check horizontal gespiegelt (Duc schaut nach rechts)\n")
print("gespiegelt" if "--los" in sys.argv else "PROBELAUF")

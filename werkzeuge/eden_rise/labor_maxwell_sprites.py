"""Maxwell fuer die Zwischensequenzen im Effektlabor (Duc 01.11.2026): Kopien der fertigen Kampfbilder als Set DucMaxwellSteelMop.
Das Labor kennt nur Sets mit dem Praefix Duc; die Quellen bleiben unberuehrt. Aufruf nach kampf_bilder.py --gegner MaxwellSteelMop."""
import json
from pathlib import Path
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "module/eden_rise/kampf/MaxwellSteelMop"
BASIS = ROOT / "docs/effekt-auswahl/status-labor/assets/duc-varianten-v1"
SET = "DucMaxwellSteelMop"
POSEN = ("idle", "windup", "attack", "heavy_windup", "heavy_attack", "hurt", "guard", "weakened", "enraged", "flee", "surrender", "defeated", "victory")
GEGNER = BASIS / "DucErdeSword"


def main():
    ziel = BASIS / SET
    ziel.mkdir(exist_ok=True)
    meta = {}
    for pose in POSEN:
        im = Image.open(QUELLE / (pose + ".webp")).convert("RGBA")
        shutil.copy2(QUELLE / (pose + ".webp"), ziel / (pose + ".webp"))
        a = im.getchannel("A").point(lambda v: 255 if v > 128 else 0)
        bb = a.getbbox()
        # Standpunkt: Mitte der untersten Reihen, damit der lange Griff die Figur nicht verschiebt
        unten = a.crop((0, bb[3] - 40, im.width, bb[3])).getbbox()
        meta[pose] = {"foot": bb[3], "center_x": round((unten[0] + unten[2]) / 2, 2), "width": im.width, "height": im.height, "scale": 0.42, "mirror": False}
    (ziel / "posen.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n")
    for name in ("gegner_guard.webp", "gegner_hurt.webp", "gegner_idle.webp"):
        shutil.copy2(GEGNER / name, ziel / name)
    pfad = BASIS / "katalog.json"
    k = json.loads(pfad.read_text(encoding="utf-8"))
    k["sets"] = [s for s in k["sets"] if s["id"] != SET]
    k["sets"].append({"id": SET, "look": "Maxwell", "weapon": "SteelMop", "label": "Mr. Maximum · Steel Mop", "directory": "duc-varianten-v1/%s/" % SET, "poses": list(POSEN), "sourcePoses": []})
    k["looks"]["Maxwell"] = "Mr. Maximum"
    k["weapons"]["SteelMop"] = "Steel Mop"
    pfad.write_text(json.dumps(k, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    m = ROOT / "client/plugins/eden-skills/preview-files.json"
    liste = json.loads(m.read_text(encoding="utf-8"))
    vorne = "assets/duc-varianten-v1/%s/" % SET
    liste = [x for x in liste if not x.startswith(vorne)] + sorted(vorne + d.name for d in ziel.iterdir())
    m.write_text(json.dumps(liste, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(SET, len(POSEN), "Posen")


if __name__ == "__main__":
    main()

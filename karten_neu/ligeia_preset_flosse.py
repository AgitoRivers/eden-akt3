# -*- coding: utf-8 -*-
r"""Ligeia: Ausschnitt mit Flosse fest uebernehmen (Duc 30.10.2026, Seed 240612 aus ligeia_flosse.py). Kopfzeile im Preset
Yacht_Ligeia, Schwanzflosse in der Karte ligeia_standard, Querformat 1328x880 und die Rueckansicht der Karte auf Ligeias
Stand (honigblond, leere Fassung am Lederband). Es wird nichts gerendert.

    ligeia_preset_flosse.py          Probelauf
    ligeia_preset_flosse.py --los    speichern (Sicherung der presets.json nach %TEMP%)
"""
import os, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402
import ligeia_flosse as LF  # noqa: E402   (setzt stdout auf UTF-8)

F_PRESETS = r"X:\AI\PromptStudio\presets.json"
RUECKEN = ("a long shimmering emerald-green fish tail instead of legs, beginning at her hips, ending in a large translucent "
           "forked tail fin, topless, a thin dark leather cord around her neck, wet glistening skin, long wet strands of "
           "hair clinging to her shoulders like seaweed, seen from behind")


def main():
    presets = dc.load_json(F_PRESETS, None, "Studio")
    p = presets[LF.PRESET]
    if LF.ALT_KOPF not in p["sprite_prompt"]:
        raise SystemExit("Kopfzeile im Preset hat sich geaendert - abgebrochen")
    p["sprite_prompt"] = p["sprite_prompt"].replace(LF.ALT_KOPF, LF.NEU_KOPF)
    mo = p.setdefault("mode_opts", {})
    mo["sprite"] = dict(mo.get("sprite") or {}, aspect="1328x880", width=1328, height=880)
    d = LF.ps("/api/state")["decks"]
    k = next(c for c in d["outfit"] if c["name"] == LF.KARTE)
    if LF.ALT_TAIL not in k["prompt"]:
        raise SystemExit("Outfit-Karte hat sich geaendert - abgebrochen")
    k["prompt"] = k["prompt"].replace(LF.ALT_TAIL, LF.NEU_TAIL)
    k["back_prompt"] = RUECKEN
    print(p["sprite_prompt"][:420])
    print(k["prompt"])
    if "--los" not in sys.argv:
        sys.exit("PROBELAUF - mit --los speichern")
    shutil.copy2(F_PRESETS, os.path.join(tempfile.gettempdir(), "presets.bak_ligeia_flosse.json"))
    dc.save_json(F_PRESETS, presets, "Studio")
    LF.ps("/api/decks", d)
    if LF.ps("/api/state")["cfg"].get("preset_active") == LF.PRESET:
        LF.ps("/api/presets", {"action": "load", "name": LF.PRESET})
    print("gespeichert")


if __name__ == "__main__":
    main()

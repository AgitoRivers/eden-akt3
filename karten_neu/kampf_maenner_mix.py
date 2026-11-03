# -*- coding: utf-8 -*-
r"""Kampf-Gegner: die fuenf Maenner mit gemischter Herkunft (19.10.2026, Duc). Herkunft steht im Subject, weil Krea
sie dort am klarsten liest; widersprechende Tags (Tattoos, Frisur) fliegen raus.

    kampf_maenner_mix.py          Probelauf
    kampf_maenner_mix.py --los    presets.json + set_presets.json (Kampf_*|Kampf) + Quelle kampf_prompts_v2.py
"""
import io, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
F_PRESETS, F_SETS = r"X:\AI\PromptStudio\presets.json", r"X:\AI\PromptStudio\set_presets.json"
Q = r"X:\AI\Eden\karten_neu\kampf_prompts_v2.py"

MIX = {
    "Pirate": ("a gaunt weathered Irish pirate in his forties with a wild red beard, freckles, a black eyepatch over "
               "his left eye and a gold front tooth",
               ["M Body: Lean", "M Hair: Long Greasy", "M Scar: Face", "M Tattoos: Arms"]),
    "Thief": ("a skinny young Korean thief in his early twenties",
              ["M Body: Lean", "M Face: Clean-Shaven"]),
    "Brute": ("a hulking Samoan dock thug with a thick neck, clean unmarked skin and traditional Samoan tattoos on his arms and shoulders",
              ["M Body: Bodybuilder", "M Hair: Buzz Cut", "M Beard: Stubble"]),
    "Heinrich": ("Heinrich, a sleazy German boat playboy in his fifties with a gold earring",
                 ["M Body: Dad Bod", "M Hair: Slicked Back", "M Tan: Deep", "M Face: Thin Moustache"]),
    "Agent": ("a tall clean-cut Black British corporate agent in his thirties with a square jaw and a short fade "
              "haircut",
              ["M Body: Lean", "M Face: Clean-Shaven", "M Skin: Deep Brown"]),
}

presets = dc.load_json(F_PRESETS, None, "Studio")
sets = dc.load_json(F_SETS, None, "Studio")
q = open(Q, encoding="utf-8").read()
for name, (subject, tags) in MIX.items():
    p = presets["Kampf_" + name]
    tags_voll = ["View: Kampf"] + tags
    print("%-9s %s\n          Tags: %s" % (name, subject, ", ".join(tags)))
    if not LOS:
        continue
    for feld in ("sprite_prompt", "base_prompt", "fashion_prompt"):
        p[feld] = re.sub(r"Subject: [^\n]*,\n", lambda m: "Subject: %s,\n" % subject, p[feld], count=1)
    p["tags_on"] = tags_voll
    sets["Kampf_%s|Kampf" % name]["tags"] = tags_voll
    # Quelle: Subject-String des Eintrags ersetzen
    m = re.search(r'"%s": \("((?:[^"\\]|\\.)*?)"' % name, q)
    if m:
        q = q[:m.start(1)] + subject + q[m.end(1):]
if LOS:
    dc.save_json(F_PRESETS, presets, "Studio")
    dc.save_json(F_SETS, sets, "Studio")
    open(Q, "w", encoding="utf-8", newline="\n").write(q)
    print("geschrieben")
else:
    print("PROBELAUF")

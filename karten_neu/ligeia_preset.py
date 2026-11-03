# -*- coding: utf-8 -*-
r"""Preset Yacht_Ligeia anlegen (Duc 29.10.2026: "mach mal B aber nur als Prompt und speicher sie unter Yacht. Behalte
aber auch die alten Sprites"). Kopie von Yacht_Siren mit Variante B aus ligeia_varianten.py: Tags Color: Red, Style:
Long Loose, Skin: Olive Tan (ohne Pale skin/Blush), mediterranes Gesicht im Subject-Satz, eigene Outfit-Karte
ligeia_standard (leere Perlenfassung statt Perlenkette). Yacht_Siren, sirene_standard und die alten Sprites bleiben.
Es wird nichts gerendert.

    ligeia_preset.py --los
"""
import io, json, sys, urllib.request

# stdout setzt ligeia_varianten beim Import auf UTF-8
sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import ligeia_varianten as LV  # noqa: E402

PS = LV.PS
NEU = "Yacht_Ligeia"
EXP = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
ps = LV.ps


def main():
    if "--los" not in sys.argv:
        sys.exit(__doc__)
    if NEU in ps("/api/state")["presets"]:
        sys.exit("%s gibt es schon - nichts geaendert" % NEU)
    d = ps("/api/state")["decks"]
    vorlage = next(c for c in d["outfit"] if c["name"] == "sirene_standard")
    if not any(c["name"] == "ligeia_standard" for c in d["outfit"]):
        d["outfit"].append(dict(vorlage, name="ligeia_standard", prompt=LV.OUTFIT))
        ps("/api/decks", d)
    ps("/api/presets", {"action": "load", "name": LV.PRESET})
    st = ps("/api/state")
    sp = st["cfg"]["sprite_prompt"]
    if LV.ALT_SUBJECT not in sp:
        sys.exit("Subject-Satz im Preset hat sich geaendert - abgebrochen")
    an = set(LV.VARIANTEN["B"])
    tags = st["cfg"]["tags"]
    for t in tags:
        t["on"] = t["name"] in an
    roh = EXP + "\\" + NEU + "\\Standard\\roh"
    ps("/api/config", {"tags": tags, "sprite_prompt": sp.replace(LV.ALT_SUBJECT, LV.NEU_SUBJECT),
                       "st_set": NEU + "/Standard/roh", "sp_char": NEU, "sp_stchar": "Ligeia", "sv_char": "Ligeia",
                       "sv_set1": EXP + "\\" + NEU + "\\Standard\\Sorted", "sv_set2": EXP + "\\" + NEU + "\\Set2\\Sorted",
                       "sv_sets": [EXP + "\\" + NEU + "\\Standard\\Sorted"], "st_src": roh,
                       "st_dst": EXP + "\\" + NEU + "\\Standard\\Sorted"})
    d = ps("/api/state")["decks"]
    for c in d["outfit"]:
        c["sel"] = c["name"] == "ligeia_standard"
        if c["sel"]:
            c["on"] = True
    ps("/api/decks", d)
    ps("/api/presets", {"action": "save", "name": NEU})
    p = json.load(open(r"X:\AI\PromptStudio\presets.json", encoding="utf-8"))[NEU]
    print("gespeichert:", NEU)
    print("  Tags:", ", ".join(p["tags_on"]))
    print("  Karten:", p.get("cards_on"))
    print("  ST:", p.get("sp_stchar"), "|", p.get("st_set"))
    print("  Subject:", p["sprite_prompt"].split("Subject:", 1)[1].split("\n", 1)[0][:160])


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
r"""Ligeia neu gestalten (Duc 29.10.2026: "3 Varianten, im Prompt bitte Tags benutzen"): Testbilder aus dem Preset
Yacht_Siren. Das Rot bleibt (dunkler), der Look wird mediterran, statt der Perlenkette eine leere Perlenfassung.
Haarfarbe, Haarstil und Haut kommen ueber Tags; im Subject-Satz steht nur das Gesicht (Casting-Regel). Preset, Karten
und Config werden danach zurueckgesetzt; nichts wird gespeichert.

    ligeia_varianten.py            Probelauf
    ligeia_varianten.py --los      je Variante neutral + amusement nach output\expressions\_ligeia_test\<A|B|C>
"""
import io, json, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PRESET = "Yacht_Siren"
ALT_SUBJECT = ("Subject: The Siren, an ancient sea spirit in the shape of a young woman, an oval pale face with high "
               "cheekbones, large luminous sea-green eyes that look far older than her face, full lips curled in a "
               "faintly amused smile, a light dusting of freckles,")
NEU_SUBJECT = ("Subject: The Siren, an ancient Greek sea spirit in the shape of a young Mediterranean woman, an oval "
               "face with high cheekbones and a straight classical nose, dark arched brows, large luminous dark amber "
               "eyes that look far older than her face, full lips curled in a faintly amused smile,")
OUTFIT = ("a long shimmering emerald-green fish tail instead of legs, beginning at her hips, topless, a thin dark "
          "leather cord around her neck holding a small empty silver pearl setting, the pearl missing, wet glistening "
          "skin, long wet strands of hair clinging to her shoulders like seaweed")
GRUND = ["View: Front", "Huge", "Sheen", "Wet", "Skin: Olive Tan"]       # ohne "Pale skin" und "Blush"
VARIANTEN = {
    "A": GRUND + ["Color: Auburn Red", "Style: Long Loose"],       # dunkles Kupfer, offen wie bisher
    "B": GRUND + ["Color: Red", "Style: Long Loose"],              # helles Kupferrot wie bisher, mediterrane Haut
    "C": GRUND + ["Color: Auburn Red", "Style: Side Braid"],       # dunkles Kupfer, lockerer Zopf (antiker Anklang)
}
KARTEN = ["neutral", "amusement"]


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    if "--los" not in sys.argv:
        for k, v in VARIANTEN.items():
            print(k, ", ".join(v))
        sys.exit("PROBELAUF - mit --los einstellen")
    st = ps("/api/state")
    alt_cfg = {k: st["cfg"].get(k) for k in ("sprite_prompt", "st_set", "tags", "seed", "decks_visible")}
    alt_preset = st["cfg"].get("preset_active")
    ps("/api/presets", {"action": "load", "name": PRESET})
    st = ps("/api/state")
    sp = st["cfg"]["sprite_prompt"]
    if ALT_SUBJECT not in sp:
        raise SystemExit("Subject-Satz im Preset hat sich geaendert - abgebrochen")
    sp = sp.replace(ALT_SUBJECT, NEU_SUBJECT)
    alt_outfit = {c["name"]: c["prompt"] for c in st["decks"]["outfit"]}
    namen = {t["name"] for t in st["cfg"]["tags"]}
    fehlt = sorted({x for v in VARIANTEN.values() for x in v} - namen)
    if fehlt:
        raise SystemExit("Tags fehlen: " + ", ".join(fehlt))
    try:
        for k, an in VARIANTEN.items():
            tags = ps("/api/state")["cfg"]["tags"]
            for t in tags:
                t["on"] = t["name"] in an
            ps("/api/config", {"tags": tags, "sprite_prompt": sp, "st_set": "_ligeia_test/" + k, "seed": 240611,
                               "decks_visible": dict(st["cfg"].get("decks_visible") or {}, kampf=False)})
            d = ps("/api/state")["decks"]
            for deck in d:
                for c in d[deck]:
                    c["sel"] = False
            for c in d["outfit"]:
                if c["name"] == "sirene_standard":
                    c["prompt"], c["sel"] = OUTFIT, True
            for c in d["setting"]:
                c["sel"] = c["name"] == "A Sprite Background"
            for c in d["st"]:
                c["sel"] = c["name"] in KARTEN
            n = ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": len(KARTEN)}).get("queued", 0)
            print("Variante %s: %d Auftraege (%s)" % (k, n, ", ".join(an[5:])))
    finally:
        d = ps("/api/state")["decks"]
        for c in d["outfit"]:
            c["prompt"] = alt_outfit.get(c["name"], c["prompt"])
        ps("/api/decks", d)
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt_cfg.items() if v is not None})
        print("Preset, Karten und Config zurueckgesetzt")


if __name__ == "__main__":
    main()

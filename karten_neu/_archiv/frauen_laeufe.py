# -*- coding: utf-8 -*-
r"""Laeufe fuer Saoirse, Kaori und Imani (20.10.2026) ueber die Prompt-Studio-API (wie der Char Creator, X-Tab: skript).

  frauen_laeufe.py portrait <Preset> [<Kost>]   4 Probeportraets t2i (verschiedene Seeds) -> expressions\<Preset>\_probe
  frauen_laeufe.py ref <Preset> <png>           Referenzportraet festlegen (Kopie nach expressions\<Preset>\_ref.png)
  frauen_laeufe.py test <Preset>                Probeposen i2i mit Gesichtsreferenz -> expressions\<Preset>\_test
  frauen_laeufe.py lauf <Preset> <Kost> sfw|voll   echter Lauf in expressions\<Preset>\<Kost>\roh

Identitaet ohne Personen-LoRA: sprite_src i2i, ref_mode face (Krea-Edit nimmt nur das Gesicht aus der Referenz).
Danach stellt das Skript Prompt Studio wieder auf t2i und das Kostuem 1 der Figur.
"""
import io, json, os, shutil, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
EXPR = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
TEST_POSEN = ["neutral", "joy", "desire", "love_back", "embarrassment", "missionary_1"]
PORTRAIT_POSEN = ["neutral", "joy", "admiration", "caring"]


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def einstellen(preset, kost, i2i, st_set=None):
    """Preset laden, Projekt/Kostuem setzen, Tags des Kostuem-Presets aktiv, Modus sprite."""
    ps("/api/presets", {"action": "load", "name": preset})
    st = ps("/api/state")
    p = st["presets"][preset] if isinstance(st.get("presets"), dict) and preset in st["presets"] else {}
    kostueme = p.get("sp_kost") or json.load(open(r"X:\AI\PromptStudio\presets.json", encoding="utf-8"))[preset]["sp_kost"]
    ps("/api/sprite_setup", {"char": preset, "stchar": p.get("sp_stchar") or "", "kost": kostueme,
                             "aktiv": kostueme.index(kost) + 1})
    kp = ps("/api/set_preset_laden", {"char": preset, "kost": kost})
    st = ps("/api/state")
    an = {x for x in kp.get("tags") or []}
    tags = st["cfg"]["tags"]
    for t in tags:
        t["on"] = t["name"] in an
        if t["name"] == "View: Front":
            t["on"] = True
        if t["name"] == "View: Back":
            t["on"] = False
    patch = {"tags": tags, "mode": "sprite", "sprite_src": "i2i" if i2i else "t2i", "combine_mode": "all",
             "st_rembg": True, "st_crop": True}
    if i2i:
        ref = os.path.join(EXPR, preset, "_ref.png")
        if not os.path.exists(ref):
            raise SystemExit("Kein Referenzportraet: erst 'ref'.")
        patch.update({"ref_image": ref, "ref_mode": "face", "face_context": 2.4, "ref_boost_mode": "off"})
    if st_set:
        patch["st_set"] = st_set
    ps("/api/config", patch)
    return kp


def decks(kp, posen):
    d = ps("/api/state")["decks"]
    outfit, setting = set(kp.get("outfit") or []), set(kp.get("setting") or ["A Sprite Background"])
    for x in d["outfit"]:
        x["sel"] = x["name"] in outfit
    for x in d["setting"]:
        x["sel"] = x["name"] in setting
    for x in d["st"]:
        x["sel"] = posen is not None and x["name"] in posen
    return d


def sfw_posen():
    st = ps("/api/state")
    liste = st["cfg"].get("sfw_posen")
    karten = [c for c in st["decks"]["st"] if c.get("on", True)]
    if isinstance(liste, list):
        return [c["name"] for c in karten if c["name"] in liste]
    return [c["name"] for c in karten if c.get("tag") != "climax" and not (c.get("tag") or "").startswith("fire")]


def zurueck(preset, kost):
    ps("/api/config", {"sprite_src": "t2i"})
    einstellen(preset, kost, False)
    d = decks(ps("/api/set_preset_laden", {"char": preset, "kost": kost}), ["neutral"])
    ps("/api/decks", d)


def main():
    cmd, preset = sys.argv[1], sys.argv[2]
    kost1 = json.load(open(r"X:\AI\PromptStudio\presets.json", encoding="utf-8"))[preset]["sp_kost"][0]
    if cmd == "ref":
        shutil.copy2(sys.argv[3], os.path.join(EXPR, preset, "_ref.png"))
        print("Referenz:", os.path.join(EXPR, preset, "_ref.png"))
        return
    try:
        if cmd == "portrait":
            kost = sys.argv[3] if len(sys.argv) > 3 else kost1
            kp = einstellen(preset, kost, False, st_set="%s/_probe" % preset)
            n = ps("/api/queue", {"cfg": {"combine_mode": "all"}, "decks": decks(kp, PORTRAIT_POSEN)}).get("queued", 0)
        elif cmd == "test":
            kp = einstellen(preset, kost1, True, st_set="%s/_test" % preset)
            n = ps("/api/queue", {"cfg": {"combine_mode": "all", "view_pro_karte": True},
                                  "decks": decks(kp, TEST_POSEN)}).get("queued", 0)
        elif cmd == "lauf":
            kost, art = sys.argv[3], sys.argv[4]
            kp = einstellen(preset, kost, True)
            posen = sfw_posen() if art == "sfw" else None
            if "--nur" in sys.argv:          # nur diese ST-Karten (z. B. die *_back-Karten nachziehen)
                posen = sys.argv[sys.argv.index("--nur") + 1].split(",")
            n = ps("/api/queue", {"cfg": {"combine_mode": "all", "view_pro_karte": True},
                                  "decks": decks(kp, posen)}).get("queued", 0)
        else:
            raise SystemExit("unbekannt: " + cmd)
        print("%s %s: %d Bilder in der Warteschlange" % (preset, cmd, n))
    finally:
        zurueck(preset, kost1)


if __name__ == "__main__":
    main()

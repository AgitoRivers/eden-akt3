# -*- coding: utf-8 -*-
r"""Test (19.10.2026, Duc: "Erst Edit testen"): Angriffsposen des Diebs per Krea-Edit aus seinem idle-Bild statt
per Text-zu-Bild. Edit verankert die Komposition -> gleiche Figur, gleiche Waffe, gleiche Hand.
- Referenz: idle.png freigestellt auf hellem Grund, verkleinert mit viel Rand auf 1024x1328 (Zoom-out ->
  Abstand zum Bildrand).
- Modell wie eingestellt (BigLoveKreaEdit), Identitaet ueber ref_boost (on, 4.0), ref_mode full.
- Kein Leuchten/Feuer/Funken (macht spaeter die Kampf-Effektschicht).
- Alte windup/attack/heavy_* wandern nach output\_expressions_papierkorb\combat\Thief\<Zeit>.
- Danach werden Kartentexte, Sprite-Prompt und Edit-Einstellungen zurueckgesetzt.
"""
import io, json, os, shutil, sys, time, urllib.request
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output"
NAME = sys.argv[1] if len(sys.argv) > 1 else "Thief"
BOOST = "off" if "--ohne-boost" in sys.argv else "on"   # Versuch 2: ohne ref_boost, mehr Spielraum fuer die Pose
W, H = 1024, 1328
REF = os.path.join(OUT, "kampf_ref", NAME + "_idle_rand.png")   # output ist eine erlaubte Wurzel des Bildladers

EDIT = ("Edit this photo. Keep exactly the same young Korean thief with the same face, black hoodie with the hood up, "
        "black cloth face mask, round black-rimmed glasses, black jeans, black sneakers with white soles and small black "
        "backpack. He holds only ONE single steel crowbar, always in his RIGHT hand. Keep the same plain light "
        "background, the same lighting and the same camera distance; his whole body stays fully visible with wide empty "
        "space around him and nothing touches the image edges. New pose: {kampf}.")
POSEN = {
    "windup": "he raises the crowbar in his right hand far back behind his right shoulder, leans back, weight on his "
              "back foot",
    "attack": "he swings the crowbar in his right hand forward, his right arm fully extended, lunging forward, motion "
              "blur on the crowbar",
    "heavy_windup": "he lifts the single crowbar with both hands high above his head",
    "heavy_attack": "he brings the single crowbar down with both hands in a full forward swing, body bent forward",
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


# Referenz mit Rand
idle = Image.open(os.path.join(OUT, "expressions", "combat", NAME, "idle.png")).convert("RGBA")
idle = idle.crop(idle.getchannel("A").getbbox())
idle.thumbnail((int(W * 0.62), int(H * 0.68)))
leinwand = Image.new("RGBA", (W, H), (232, 228, 220, 255))
leinwand.alpha_composite(idle, ((W - idle.width) // 2, H - idle.height - int(H * 0.12)))
os.makedirs(os.path.dirname(REF), exist_ok=True)
leinwand.convert("RGB").save(REF)

# alte Posen sichern
z = os.path.join(OUT, "_expressions_papierkorb", "combat", NAME, time.strftime("%Y-%m-%d_%H%M%S"))
for k in POSEN:
    f = os.path.join(OUT, "expressions", "combat", NAME, k + ".png")
    if os.path.exists(f):
        os.makedirs(z, exist_ok=True)
        shutil.move(f, z)

st = ps("/api/state")
alt_cfg = {k: st["cfg"].get(k) for k in ("sprite_src", "ref_image", "ref_mode", "ref_boost_mode", "ref_boost_value")}
alt_karten = {c["name"]: c["prompt"] for c in st["decks"]["kampf"]}
try:
    ps("/api/presets", {"action": "load", "name": "Kampf_" + NAME})
    kp = ps("/api/set_preset_laden", {"char": "Kampf_" + NAME, "kost": "Kampf"})
    st = ps("/api/state")
    an = set(kp.get("tags") or [])
    tags = st["cfg"]["tags"]
    for t in tags:
        t["on"] = t["name"] in an
    mo = dict(st["cfg"].get("mode_opts") or {})
    mo["sprite"] = dict(mo.get("sprite") or {}, aspect="%dx%d" % (W, H), width=W, height=H, ref_mode="full",
                        ref_boost_mode=BOOST, ref_boost_value=4)
    vis = dict(st["cfg"].get("decks_visible") or {}, kampf=True)
    ps("/api/config", {"tags": tags, "mode": "sprite", "sprite_src": "i2i", "ref_image": REF, "ref_mode": "full",
                       "ref_boost_mode": BOOST, "ref_boost_value": 4, "width": W, "height": H,
                       "aspect": "%dx%d" % (W, H), "mode_opts": mo, "combine_mode": "all", "decks_visible": vis,
                       "view_pro_karte": False, "st_rembg": True, "st_crop": True, "sprite_prompt": EDIT})
    for k, text in POSEN.items():
        d = ps("/api/state")["decks"]
        for c in d["kampf"]:
            c["sel"] = c["name"] == k
            if c["name"] == k:
                c["prompt"] = text
        for x in d["outfit"]:
            x["sel"] = x["name"] in set(kp.get("outfit") or [])
        for x in d["setting"]:
            x["sel"] = x["name"] in set(kp.get("setting") or [])
        for x in d["st"]:
            x["sel"] = False
        n = ps("/api/queue", {"cfg": {}, "decks": d}).get("queued", 0)
        print("%-13s %d Auftrag" % (k, n))
finally:
    d = ps("/api/state")["decks"]
    for c in d["kampf"]:
        c["prompt"] = alt_karten.get(c["name"], c["prompt"])
    ps("/api/decks", d)
    st = ps("/api/state")
    ps("/api/presets", {"action": "load", "name": "Kampf_" + NAME})    # Sprite-Prompt aus dem Preset zurueck
    ps("/api/config", dict({k: v for k, v in alt_cfg.items() if v is not None},
                           decks_visible=dict(st["cfg"].get("decks_visible") or {}, kampf=False)))
print("Einstellungen zurueckgesetzt. Referenz:", REF)

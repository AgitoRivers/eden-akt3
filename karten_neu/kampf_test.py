# -*- coding: utf-8 -*-
r"""Kampf-Sprites testen bzw. erzeugen ueber die API von Prompt Studio (19.10.2026).

    kampf_test.py                          je ein idle fuer Pirate, Lion, SeaMonster (Testordner *_TEST)
    kampf_test.py --gegner Pirate,Lion     andere Auswahl
    kampf_test.py --voll                   alle Kernkarten (Menschen ohne death), echte Ordner combat\<Name>

Laedt je Gegner das Preset Kampf_<Name> und sein Kostuem-Preset (Outfit, Setting, Tags), waehlt im Deck kampf die
Karten und stellt die Auftraege ein. Danach ist das Deck kampf wieder ausgeblendet (sonst kombiniert es in T2I/I2I
mit allen Karten). Prompt Studio laeuft danach mit dem zuletzt geladenen Kampf-Preset.
"""
import io, json, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
MENSCHEN = {"Pirate", "Thief", "Brute", "Heinrich", "Agent", "Paparazzo", "Mime", "DrunkCasanova", "PirateTorch", "ThiefArab", "Alon", "YasinDrone", "MaxwellSteward", "MaxwellSports", "MaxwellMaximum", "YamamotoSamurai", "DucErdeSword"}
MENSCHEN |= {"PirateAlpha", "ThiefAlpha", "BruteAlpha", "AgentAlpha"}   # Alphas 22.10.2026
ALLE = ["Pirate", "Thief", "Brute", "Heinrich", "Agent", "Vampire", "Alien", "Lion", "Snake", "Unit1", "Seagull",
        "Dog", "Shark", "SeaMonster", "Ape"]


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


voll = "--voll" in sys.argv
# --karten weakened,defeated: nur diese Kampf-Karten, in die echten Ordner (wie --voll; death nur Nicht-Menschen)
nur_karten = set(sys.argv[sys.argv.index("--karten") + 1].split(",")) if "--karten" in sys.argv else None
if nur_karten:
    voll = True
wahl = ALLE if voll else ["Pirate", "Lion", "SeaMonster"]
if "--gegner" in sys.argv:
    wahl = sys.argv[sys.argv.index("--gegner") + 1].split(",")
gesamt = 0
for name in wahl:
    p = "Kampf_" + name
    ps("/api/presets", {"action": "load", "name": p})
    kp = ps("/api/set_preset_laden", {"char": p, "kost": "Kampf"})
    st = ps("/api/state")
    an = set(kp.get("tags") or [])
    tags = st["cfg"]["tags"]
    for t in tags:
        t["on"] = t["name"] in an
    vis = dict(st["cfg"].get("decks_visible") or {}, kampf=True)
    patch = {"tags": tags, "mode": "sprite", "sprite_src": "t2i", "combine_mode": "all",
             "decks_visible": vis, "view_pro_karte": False, "st_rembg": True, "st_crop": True}
    if "--quer" in sys.argv:   # liegende Posen aufrechter Figuren: Querformat nur fuer diesen Lauf
        mo = dict(st["cfg"].get("mode_opts") or {})
        mo["sprite"] = dict(mo.get("sprite") or {}, aspect="1328x880", width=1328, height=880)
        patch.update({"mode_opts": mo, "aspect": "1328x880", "width": 1328, "height": 880})
    elif "--quadrat" in sys.argv:   # 24.10.: long weapons held across the body (shotgun guard) - square, 1.2 MP
        mo = dict(st["cfg"].get("mode_opts") or {})
        mo["sprite"] = dict(mo.get("sprite") or {}, aspect="1104x1104", width=1104, height=1104)
        patch.update({"mode_opts": mo, "aspect": "1104x1104", "width": 1104, "height": 1104})
    ps("/api/config", patch)
    d = ps("/api/state")["decks"]
    outfit, setting = set(kp.get("outfit") or []), set(kp.get("setting") or [])
    if voll:
        if nur_karten:   # genau die genannten Karten (auch outfit_check), death nur fuer Nicht-Menschen
            karten = {c["name"] for c in d["kampf"] if c.get("on", True) and c["name"] in nur_karten
                      and not (c["name"] == "death" and name in MENSCHEN)}
        else:
            karten = {c["name"] for c in d["kampf"] if c.get("on", True) and c.get("tag") != "check"
                      and (c.get("tag") == "kern" or name not in MENSCHEN)}
        if not karten:
            continue
    else:
        karten = {"idle"}
    # 23.10.2026: a card that vanished from decks.json (overwritten by another writer) left the outfit deck without
    # selection, and Prompt Studio then used ALL 580 outfit cards - stop instead of guessing
    fehlt = sorted((outfit | setting) - {x["name"] for x in d["outfit"] + d["setting"]})
    if not outfit or fehlt:
        sys.exit("%s: Karte fehlt in Prompt Studio (%s) - abgebrochen, nichts eingereiht"
                 % (name, ", ".join(fehlt) or "kein Outfit im Kostuem-Preset"))
    for x in d["outfit"]:
        x["sel"] = x["name"] in outfit
    for x in d["setting"]:
        x["sel"] = x["name"] in setting
    for x in d["kampf"]:
        x["sel"] = x["name"] in karten
    for x in d["st"]:
        x["sel"] = False
    r = ps("/api/queue", {"cfg": {}, "decks": d, "test": not voll, "max_auftraege": len(karten)})
    n = r.get("queued", 0)
    gesamt += n
    print("%-11s %-30s %d Auftraege (%s)" % (name, ps("/api/state")["cfg"].get("st_set"), n,
                                             ", ".join(sorted(karten)) if len(karten) < 4 else "%d Karten" % len(karten)))
st = ps("/api/state")
ps("/api/config", {"decks_visible": dict(st["cfg"].get("decks_visible") or {}, kampf=False)})
print("Gesamt %d. Deck kampf wieder ausgeblendet." % gesamt)

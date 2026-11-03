# -*- coding: utf-8 -*-
r"""Volle SFW-Sets fuer die gewaehlten Dorf-Figuren (Duc 30.10.2026, Wahl ueber Ende Rise & Apps). Vorlage: bibi_sfw_neu.py.

    dorf_sets.py --anlegen              finale Presets Yacht_<Name> + Set Yacht_<Name>|Standard aus der gewaehlten Casting-Fassung
    dorf_sets.py --test [--nur Name]    3 Testposen (neutral, joy, sadness) -> expressions\_test_dorf_sets\<Preset>
    dorf_sets.py --los [--nur Name] [--karten a,b]   alle SFW-Posen -> expressions\<Preset>\Standard\roh
    (ohne Option: Probelauf)

Mina und Adrien gehoeren nicht dazu. Nichts wird ins Spiel kopiert.
"""
import copy, io, json, os, shutil, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

PS = "http://127.0.0.1:8301"
F_PRESETS, F_SETS = r"X:\AI\PromptStudio\presets.json", r"X:\AI\PromptStudio\set_presets.json"
OUT = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions"
KOST = "Standard"
JETZT = time.strftime("%Y-%m-%d %H:%M")
# Name: (Quell-Preset der gewaehlten Fassung, Karte, Ordner/ST-Name, Set-Name im Spiel)
FIGUREN = {
    "Pascal": ("Yacht_Pascal_A", "pascal_standard", "Pascal Leca", "pascal_standard"),
    "BaTu": ("Yacht_BaTu_A", "batu_A", "Ba Tu", "batu_standard"),
    "Sandru": ("Yacht_Sandru_C", "sandru_C", "Sandru Amrani", "sandru_av"),
    "Anghjulu": ("Yacht_Anghjulu_C", "anghjulu_C", "Don Anghjulu", "anghjulu_standard"),
    # Das alte Preset Yacht_Adrien (Caporal aus Lyon) bleibt unangetastet, das neue heisst Yacht_AdrienNeu
    "Danzel_Nach_3": ("Yacht_Danzel", "danzel_nach_3", "Danzel", "-"),     # Casting-Preset, nur fuer --los mit --ziel
    "AdrienNeu": ("Yacht_AdrienCast_A", "adriencast_A", "Adrien Morel", "adrien_standard"),
}
# Eigene Karten fuer die finalen Presets (die Casting-Karten bleiben unveraendert)
KARTEN_NEU = {
    "pascal_standard": "a white fedora hat with a black band worn on his half-bald head, a double-breasted dark navy pinstripe "
                       "suit with a white pocket square in the breast pocket, an open-collared light blue fabric shirt with the "
                       "top buttons undone and no tie at all, bare neck, polished brown leather shoes",
}
# Gesichter konstant halten (keine Identitaets-LoRA): Subject-Satz geschaerft, Alter und Kleidung bleiben wie gewaehlt
SCHAERFEN = {
    "BaTu": "an elderly woman with a deeply lined weathered face, completely snow-white hair and thin white eyebrows, no dark "
            "hair at all, age spots on her cheeks, looking every day of seventy-five",
    "Sandru": "a clearly male face with a narrow jaw and faint dark stubble, short cropped dark curly hair, thick dark "
              "eyebrows, a thin young man's face",
    "Anghjulu": "a completely bald crown with only short white tufts of hair above the ears, white stubble, a bulbous red "
                "nose, a wide jolly mouth, a heavily lived-in older face",
}
# NPC-Satz (🙂) aus ui.html NPC_STANDARD, ohne desire_2 (Figuren nicht romanzierbar); nur Front, view_pro_karte False
NPC = ["neutral", "caring", "joy", "sadness", "anger", "fear_2", "surprise", "disgust", "amusement", "annoyance", "confusion",
       "curiosity", "pride", "approval", "gratitude", "nervousness", "disapproval", "disappointment", "excitement_2",
       "embarrassment_2", "admiration_2", "love_2"]
KORB = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb"
TEST = ["neutral", "joy", "sadness"]
ARGS = sys.argv[1:]
NUR = ARGS[ARGS.index("--nur") + 1].split(",") if "--nur" in ARGS else [x for x in FIGUREN if x not in ("AdrienNeu", "Danzel_Nach_3")]
KARTEN = ARGS[ARGS.index("--karten") + 1].split(",") if "--karten" in ARGS else None
TESTMODUS = "--test" in ARGS
NPCMODUS = "--npc" in ARGS
ZIEL = ARGS[ARGS.index("--ziel") + 1] if "--ziel" in ARGS else None       # st_set ueberschreiben
SEED = int(ARGS[ARGS.index("--seed") + 1]) if "--seed" in ARGS else None


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def preset(n):
    return "Yacht_" + n


def anlegen():
    presets = dc.load_json(F_PRESETS, None, "Studio")
    sets = dc.load_json(F_SETS, None, "Studio")
    for n in NUR:
        quelle, karte, ordner, setname = FIGUREN[n]
        p = copy.deepcopy(presets[quelle])
        p.update({"st_set": "%s/%s/roh" % (preset(n), KOST), "sp_stchar": ordner,
                  "cards_on": {"outfit": [karte], "setting": ["A Sprite Background"], "st": ["neutral"]},
                  "created": JETZT, "updated": JETZT})
        if n in SCHAERFEN:
            assert ", natural skin texture" in p["sprite_prompt"], n
            p["sprite_prompt"] = p["sprite_prompt"].replace(", natural skin texture", ", " + SCHAERFEN[n] + ", natural skin texture", 1)
        presets[preset(n)] = p
        sets["%s|%s" % (preset(n), KOST)] = {"outfit": [karte], "setting": ["A Sprite Background"], "tags": list(p["tags_on"])}
        print("angelegt:", preset(n), "aus", quelle, "| Karte", karte, "| Set im Spiel", setname)
    dc.save_json(F_PRESETS, presets, "Studio")
    dc.save_json(F_SETS, sets, "Studio")
    d = ps("/api/state")["decks"]
    da = {c["name"]: c for c in d["outfit"]}
    for kn, text in KARTEN_NEU.items():
        if kn in da:
            da[kn]["prompt"] = text
        else:
            d["outfit"].append({"name": kn, "prompt": text, "on": True, "tag": "eden_dorf", "sel": False,
                                "back_prompt": text + ", seen from behind"})
    ps("/api/decks", d)


def einreihen(n):
    """Reiht die Posen einer Figur ein; Karten und Config werden danach wiederhergestellt."""
    pn = preset(n)
    karte = FIGUREN[n][1]
    st0 = ps("/api/state")
    alt_preset, vis = st0["cfg"].get("preset_active"), st0["cfg"].get("decks_visible") or {}
    alt_cfg = {k: st0["cfg"].get(k) for k in ("sprite_prompt", "loras", "st_set", "sprite_src", "tags", "unet", "clip", "seed",
                                              "view_pro_karte", "combine_mode", "st_rembg", "st_crop", "mode", "decks_visible")}
    alt_decks = copy.deepcopy(st0["decks"])
    try:
        ps("/api/presets", {"action": "load", "name": pn})
        kp = ps("/api/set_preset_laden", {"char": pn, "kost": KOST})
        st = ps("/api/state")
        posen = set(st["cfg"].get("sfw_posen") or [])
        d = st["decks"]
        an = [c["name"] for c in d["st"] if c.get("on", True) and c["name"] in posen]
        if NPCMODUS:
            roh = os.path.join(OUT, pn, KOST, "roh")
            da = {f[:-4] for f in os.listdir(roh)} if os.path.isdir(roh) else set()
            an = [c["name"] for c in d["st"] if c.get("on", True) and c["name"] in NPC and c["name"] not in da]
        elif KARTEN:
            an = [c for c in an if c in KARTEN]
        elif TESTMODUS:
            an = [c for c in an if c in TEST]
        st_set = ZIEL or (("_test_dorf_sets/%s" % pn) if TESTMODUS else "%s/%s/roh" % (pn, KOST))
        print("%s: %d Posen -> %s | Tags: %s" % (pn, len(an), st_set, ", ".join(kp.get("tags") or [])))
        tags = st["cfg"]["tags"]
        sets = set(kp.get("tags") or [])
        for t in tags:
            t["on"] = t["name"] in sets
        for deck in ("outfit", "setting", "st", "kampf"):
            for c in d[deck]:
                c["sel"] = False
        for c in d["outfit"]:
            if c["name"] == karte:
                c["sel"] = True
        for c in d["setting"]:
            c["sel"] = c["name"] in set(kp.get("setting") or [])
        for c in d["st"]:
            c["sel"] = c["name"] in an
        ps("/api/config", {**({"seed": SEED} if SEED else {}), "tags": tags, "mode": "sprite", "st_set": st_set, "view_pro_karte": not NPCMODUS, "combine_mode": "all",
                           "st_rembg": True, "st_crop": True, "decks_visible": dict(vis, kampf=False)})
        ps("/api/decks", d)
        q = ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": len(an)}).get("queued", 0)
        print("eingereiht:", q)
        return q
    finally:
        jetzt = ps("/api/state")["decks"]          # nur die Auswahl zurueck, Karten anderer Sitzungen bleiben
        for deck, karten in jetzt.items():
            alt_sel = {c["name"]: c.get("sel", False) for c in alt_decks.get(deck, [])}
            for c in karten:
                if c["name"] in alt_sel:
                    c["sel"] = alt_sel[c["name"]]
        ps("/api/decks", jetzt)
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        ps("/api/config", {k: v for k, v in alt_cfg.items() if v is not None})


def aufraeumen():
    """Bilder ausserhalb des NPC-Satzes in den Papierkorb (nie loeschen)."""
    for n in NUR:
        roh = os.path.join(OUT, preset(n), KOST, "roh")
        ziel = os.path.join(KORB, "%s_nicht_npc_%s" % (preset(n), time.strftime("%Y%m%d_%H%M")))
        for f in sorted(os.listdir(roh)):
            if f.endswith(".png") and f[:-4] not in NPC:
                os.makedirs(ziel, exist_ok=True)
                shutil.move(os.path.join(roh, f), ziel)
        print(n, "behalten:", len([f for f in os.listdir(roh) if f.endswith(".png")]), "->", ziel)


def main():
    if "--aufraeumen" in ARGS:
        return aufraeumen()
    if "--anlegen" in ARGS:
        return anlegen()
    if TESTMODUS or NPCMODUS or "--los" in ARGS:
        return sum(einreihen(n) for n in NUR)
    for n in NUR:
        print("Probelauf:", preset(n), FIGUREN[n])


if __name__ == "__main__":
    main()

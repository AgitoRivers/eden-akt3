# -*- coding: utf-8 -*-
r"""Weapon item images (20.10.2026): 4 variants per weapon for Duc to pick from.

    python waffen_bilder.py --queue          queue 4 variants per weapon in ComfyUI Krea2 (front of the queue)
    python waffen_bilder.py --queue taser    only these weapons (overwrites their variants)
    python waffen_bilder.py --build          thumbnails + self-contained picker page (waffen_auswahl.html)
    python waffen_bilder.py --pick taser=2 sportbogen=4    copy the chosen variant to items\_gross + items\<id>.webp

Same product-photo look as werkzeuge\item_bilder.py (graph, style, linen background). The weapon list follows
docs\wiki\systeme\kampf.md ("Beschlossen am 19./20.10.2026"). Weapons are not in gegenstaende.json yet; ids are final names.
"""
import base64, io, json, os, random, shutil, sys

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import item_bilder as ib  # noqa: E402

EDEN = os.path.dirname(HERE)
ITEMS = os.path.join(EDEN, "module", "eden_rise", "items")
BIG = os.path.join(ITEMS, "_gross")
VARIANTS = os.path.join(ITEMS, "_waffen_varianten")
PAGE = os.path.join(VARIANTS, "waffen_auswahl.html")
N = 4
MAX_VARIANTS = 12           # extra variants (v5 ...) show up in the picker too
WIDE = (1536, 768)          # 2-slot weapons: twice as wide, same height (Duc 20.10.2026)
TWO_SLOTS = {"sportbogen", "spitzhacke", "piratensaebel", "feuerwehraxt", "fischerspeer", "saufeder", "luftgewehr",
             "doppelflinte", "holms_marinesaebel", "rosis_flammenschwert", "tritons_dreizack", "elektro_harpune",
             "yamamotos_katana"}
EXTRA_WIDE = (1872, 624)    # spears: 3:1 so the long shaft fits (Duc 20.10.2026)
SPEARS = {"fischerspeer", "saufeder", "spear"}
TWO_SLOTS |= {"gun", "sword", "spear"}   # fixed weapons 24.10.2026 (image width only; spear stays 1 slot in the game)
WIDE_IMAGE = TWO_SLOTS | {"fackel", "bat"}  # the torch lies horizontally too, but stays 1 slot
WIDE_HINT = ", the whole object lying horizontally across the wide frame from left to right, fully visible end to end"
RARITY_COLOR = {"Gewöhnlich": "#d8d4cc", "Selten": "#5b9bf0", "Episch": "#b07ef0", "Legendär": "#e8b84a"}

# id: (label, element, rarity, type, motif in English)
WEAPONS = {
    # 24.10.2026: Duc's fixed weapons, motifs match his combat sprites (karten_neu\kampf_duc_waffen.py);
    # no "baseball" in the bat motif - Krea adds a ball
    "bat": ("Schwarzer Baseballschläger", "–", "Gewöhnlich", "Stumpf",
            "a long matte black wooden bat with a thick rounded barrel and a thin handle wrapped in black grip tape, "
            "the only object on the fabric"),
    "knife": ("Kampfmesser", "–", "Gewöhnlich", "Messer",
              "a medium-sized combat knife with a single-edged steel blade with a clipped point and a flat back, a "
              "black ribbed grip and a small steel guard"),
    "gun": ("Doppelflinte", "–", "Gewöhnlich", "Fern",
            "a closed side-by-side double-barrel shotgun with plain dark steel barrels and a dark walnut stock, barrels "
            "and stock forming one straight line"),
    "spear": ("Saufeder", "–", "Gewöhnlich", "Stange",
              "a long boar spear with a broad leaf-shaped steel spearhead, a short steel crossbar just below it and a "
              "long plain dark wooden shaft, the plain round wooden butt end and the tip both visible with a little "
              "empty linen on both sides"),
    "sword": ("Kavalleriesäbel", "–", "Gewöhnlich", "Klinge",
              "a curved steel cavalry sabre with a polished brass basket hand guard and a dark leather grip, the bare "
              "blade shown alone, handle on the left, tip pointing to the right"),
}

# Cyber armor designs: variant k of the armor item = design k = Alon's sprite test in karten_neu\kampf_alon_cyber.py.
# No glowing parts (light comes from the combat effect layer) and no perforated or honeycomb surfaces.
CYBER_DESIGNS = [
    "a sleek matte black cyber armor chest piece made of smooth segmented carbon fibre plates with brushed titanium "
    "edges and a high collar",
    "a white and silver futuristic armored jacket with smooth curved panels like a spacesuit and a small black rocket "
    "emblem on the chest",
    "a gunmetal grey and black armored tactical jacket with large smooth overlapping plates on chest and shoulders "
    "and thin red accent stripes",
    "a polished chrome and black cyber armor torso shell with sculpted chest plates and segmented shoulder guards, "
    "like a superhero suit",
]
ARMOR_HINT = ", only the upper garment laid out flat on its own, no person, no mannequin, no trousers"
SUIT_HINT = ", the complete suit laid out flat on its own from collar to boots, empty inside, no person, no mannequin"
SUITS = {"cyber_suit"}
# id: (label, resistance element, rarity, protection, motif in English or one motif per variant)
ARMOR = {
    "cyber_armor": ("Cyber-Armor (nach Alon)", "Luft", "Episch", "+5", CYBER_DESIGNS),
    # 24.10.2026: Duc's four element jackets (ids preliminary, the armor list itself is planned with the upgrades);
    # motifs match the look cards kampf_duc<look> in Prompt Studio
    "jacket_earth": ("Bikerjacke (Erde)", "Erde", "Gewöhnlich", "offen",
                     "a black leather biker jacket with an asymmetric zip, bronze zippers and bronze buckles"),
    "jacket_water": ("Navy-Caban (Wasser)", "Wasser", "Gewöhnlich", "offen",
                     "a smooth shiny navy blue leather double-breasted jacket in a short pea coat cut with two rows of "
                     "dark buttons"),
    "jacket_fire": ("Bordeaux-Caban (Feuer)", "Feuer", "Gewöhnlich", "offen",
                    "a weathered burgundy leather double-breasted jacket in a short pea coat cut with two rows of red "
                    "buttons"),
    "jacket_air": ("Weißer Caban (Luft)", "Luft", "Gewöhnlich", "offen",
                   "a smooth white leather double-breasted jacket in a short pea coat cut with two rows of golden "
                   "buttons"),
    # 24.10.2026: Duc's own full-body cyber armor (look card kampf_duccyber + gauntlets), id preliminary like the jackets
    "cyber_suit": ("Ducs Cyber-Rüstung", "offen", "Episch", "offen",
                   "a full-body dark gunmetal and black chrome cyber armor suit, large smooth darkened armored plates "
                   "on the chest, shoulders, arms, legs and boots, flexible black segments at the joints, armored black "
                   "metal gauntlets, thin blue light lines along the plate edges"),
}
CHARM_HINT = (", a small soft plush keychain charm about the size of a hand, with a short loop of ribbon and a "
              "shiny silver key ring, cute and well made")
# id: (label, giver, effect, motif in English) - accessories for the 2 equipment slots
CHARMS = {
    "anhaenger_strudel": ("Plüsch-Kater „Strudel“", "Jana", "Mut +1",
                          "a plush pure white cat with blue eyes and a tiny red and white Austrian scarf"),
    "anhaenger_robbe": ("Plüsch-Robbe", "Siri", "Empathie +1",
                        "a plush white baby seal with big dark eyes and a tiny knitted Nordic hat"),
    "anhaenger_eule": ("Plüsch-Eule", "Sophia", "Wahrnehmung +1",
                       "a plush brown owl wearing tiny round glasses and holding a tiny book"),
    "anhaenger_seepferdchen": ("Plüsch-Seepferdchen", "Chiara", "Charisma +1",
                               "a plush coral pink seahorse with a curled tail and a tiny golden crown"),
    "anhaenger_koala": ("Plüsch-Koala", "Alva", "Snacks heilen +2",
                        "a plush grey koala hugging a tiny chocolate biscuit"),
    "anhaenger_schaeferhund": ("Plüsch-Schäferhund", "Elsa", "Einschüchtern mit Vorteil",
                               "a plush German shepherd dog wearing a tiny navy blue police cap"),
    "anhaenger_gorilla": ("Plüsch-Gorilla", "Maxwell", "Spezialangriffe +20 % Schaden",
                          "a plush muscular brown gorilla with a soft beige belly, wearing tiny dark sunglasses and a shiny gold wrestling champion belt around his waist with a big plain round gold plate engraved with a single star"),
    "anhaenger_falke": ("Plüsch-Falke", "Yasin", "Krit +5 %",
                        "a plush peregrine falcon with spread wings and a tiny gold chain"),
    "anhaenger_flamingo": ("Plüsch-Flamingo", "Madame Casanova", "Fassung −4 schon nach 2 perfekten Paraden",
                           "a plush pink flamingo wearing a tiny red flamenco dress with ruffles"),
}
ALON_CYBER = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\combat\Alon\_cyber"


def queue(only):
    try:
        ib.get("/system_stats")
    except Exception:
        sys.exit("ComfyUI Krea2 is not running (port 8189).")
    os.makedirs(VARIANTS, exist_ok=True)
    background = ib.HINTERGRUENDE[ib.HINTERGRUND]
    n = 0
    for wid, (label, *_rest, motif) in list(WEAPONS.items()) + list(ARMOR.items()) + list(CHARMS.items()):
        if only and wid not in only:
            continue
        wide = wid in WIDE_IMAGE
        hint = SUIT_HINT if wid in SUITS else ARMOR_HINT if wid in ARMOR else CHARM_HINT if wid in CHARMS else (WIDE_HINT if wide else "")
        for k in range(1, N + 1):
            m = motif[k - 1] if isinstance(motif, list) else motif     # list = one design per variant
            prompt = ib.STIL.format(motiv=m + hint, hintergrund=background)
            name = "%s_v%d" % (wid, k)
            g = ib.graph(prompt, VARIANTS, name, random.randint(1, 2 ** 31), nsfw=True)
            if wide:
                w, h = EXTRA_WIDE if wid in SPEARS else WIDE
                g["6"]["inputs"].update(width=w, height=h)
            ib.post("/prompt", {"prompt": g, "front": True})
            n += 1
        print("queued: %-24s %s" % (wid, label))
    print("%d jobs queued at the front" % n)


def thumb_data(path, size=360):
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail((size * 3, size), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=82, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def build():
    cards, missing = [], []
    for wid, (label, element, rarity, typ, _motif) in WEAPONS.items():
        imgs = []
        for k in range(1, MAX_VARIANTS + 1):
            p = os.path.join(VARIANTS, "%s_v%d.png" % (wid, k))
            if os.path.exists(p):
                imgs.append((k, thumb_data(p)))
            elif k <= N:
                missing.append("%s_v%d" % (wid, k))
        cards.append({"id": wid, "label": label, "element": element, "rarity": rarity, "type": typ,
                      "color": RARITY_COLOR[rarity], "slots": 2 if wid in TWO_SLOTS else 1,
                      "shape": "extra" if wid in SPEARS else "breit" if wid in WIDE_IMAGE else "", "imgs": [{"k": k, "src": s} for k, s in imgs]})
    for aid, (label, resist, rarity, protection, motif) in ARMOR.items():
        imgs = [{"k": k, "src": thumb_data(os.path.join(VARIANTS, "%s_v%d.png" % (aid, k)))}
                for k in range(1, MAX_VARIANTS + 1) if os.path.exists(os.path.join(VARIANTS, "%s_v%d.png" % (aid, k)))]
        cards.append({"id": aid, "label": label, "element": resist, "rarity": rarity,
                      "type": "Rüstung, Schutz %s, Widerstand" % protection, "color": RARITY_COLOR[rarity],
                      "slots": 1, "shape": "", "imgs": imgs, "section": "Rüstungen"})
    for cid, (label, giver, effect, _motif) in CHARMS.items():
        imgs = [{"k": k, "src": thumb_data(os.path.join(VARIANTS, "%s_v%d.png" % (cid, k)))}
                for k in range(1, MAX_VARIANTS + 1) if os.path.exists(os.path.join(VARIANTS, "%s_v%d.png" % (cid, k)))]
        cards.append({"id": cid, "label": label, "element": "–", "rarity": "Selten",
                      "type": "Anhänger von %s, %s" % (giver, effect), "color": RARITY_COLOR["Selten"],
                      "slots": 1, "shape": "", "imgs": imgs, "section": "Anhänger (Ausrüstung)"})
    elon = [{"k": k, "src": thumb_data(os.path.join(ALON_CYBER, "outfit_check_v%d.png" % k))}
            for k in range(1, len(CYBER_DESIGNS) + 1) if os.path.exists(os.path.join(ALON_CYBER, "outfit_check_v%d.png" % k))]
    cards.append({"id": "alon_cyber", "label": "Alon in Cyber-Armor (Entwurf k = Cyber-Armor Variante k)",
                  "element": "Luft", "rarity": "Episch", "type": "Kampf-Sprite", "color": RARITY_COLOR["Episch"],
                  "slots": 1, "shape": "hoch", "imgs": elon, "section": "Kampf-Sprite"})
    html = TEMPLATE.replace("__DATA__", json.dumps(cards, ensure_ascii=False))
    with open(PAGE, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(PAGE, "| %d KB" % (os.path.getsize(PAGE) // 1024), "| missing: %s" % (", ".join(missing) or "none"))


# Inventory orientation (Duc 20.10.2026): small weapons tip up, pistols point left; long weapons tip right with the
# sharp edge down. Only 90-degree turns and mirroring, so the linen background stays intact. Checked by eye for the
# chosen variants; a new pick of these ids needs a fresh look.
TURN = {"fackel": Image.ROTATE_270,            # head left -> up (the torch image becomes portrait 1:2)
        "spitzhacke": Image.FLIP_LEFT_RIGHT, "feuerwehraxt": Image.FLIP_LEFT_RIGHT,
        "saufeder": Image.FLIP_LEFT_RIGHT, "tritons_dreizack": Image.FLIP_LEFT_RIGHT,
        "elektro_harpune": Image.FLIP_LEFT_RIGHT}
# yamamotos_katana: blue-gold variants v5-v8 are generated already pointing right with the edge down, no turn


def pick(pairs):
    for p in pairs:
        wid, k = p.split("=")
        src = os.path.join(VARIANTS, "%s_v%s.png" % (wid, k))
        im = Image.open(src).convert("RGB")
        if wid in TURN:
            im = im.transpose(TURN[wid])
        im.save(os.path.join(BIG, wid + ".png"))
        im.thumbnail((ib.THUMB * 3, ib.THUMB * 2), Image.LANCZOS)   # keeps 2:1, 3:1 and the portrait torch
        im.save(os.path.join(ITEMS, wid + ".webp"), "WEBP", quality=85, method=6)
        print("picked: %s variant %s%s" % (wid, k, " (turned)" if wid in TURN else ""))


TEMPLATE = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ausrüstungs-Auswahl</title>
<style>
:root{--bg:#121318;--card:#1b1d24;--text:#f3eee4;--muted:#a8a294;--gold:#d8bd86;--sel:#e8b84a}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f1ea;--card:#fff;--text:#1d1c1a;--muted:#6b665c;--gold:#9a7b3c;--sel:#c48a12}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.4 system-ui,Segoe UI,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 16px;border-bottom:1px solid #ffffff18;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
h1{font-size:18px;margin:0;color:var(--gold);font-weight:600}#zaehler{color:var(--muted)}
button{background:var(--gold);color:#121318;border:0;border-radius:8px;padding:8px 14px;font-weight:600;cursor:pointer}
main{padding:16px;display:grid;gap:16px;max-width:1300px;margin:0 auto}
.karte{background:var(--card);border-radius:12px;padding:12px 14px;border-left:4px solid var(--c)}
.kopf{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:8px}.kopf b{font-size:16px}
.tag{font-size:12px;color:var(--muted)}.rar{color:var(--c);font-weight:600;font-size:12px}
.reihe{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
@media (max-width:640px){.reihe{grid-template-columns:repeat(2,minmax(0,1fr))}}
.bild{position:relative;border-radius:8px;overflow:hidden;cursor:pointer;outline:3px solid transparent;transition:outline-color .15s}
.bild img{display:block;width:100%;aspect-ratio:1;object-fit:cover}
.breit .reihe{grid-template-columns:repeat(2,minmax(0,1fr))}.breit .bild img{aspect-ratio:2/1}
.extra .reihe{grid-template-columns:repeat(2,minmax(0,1fr))}.extra .bild img{aspect-ratio:3/1}
.hoch .bild img{aspect-ratio:2/3;object-fit:contain;background:#ffffff10}
h2.abschnitt{margin:12px 0 0;font-size:16px;color:var(--gold)}
@media (max-width:640px){.breit .reihe,.extra .reihe{grid-template-columns:minmax(0,1fr)}}
.bild span{position:absolute;left:6px;top:4px;background:#000a;color:#fff;border-radius:6px;padding:0 7px;font-size:13px}
.bild.gewaehlt{outline-color:var(--sel)}.bild.gewaehlt span{background:var(--sel);color:#121318}
.leer{color:var(--muted);font-size:13px}
#ausgabe{width:100%;max-width:1300px;margin:0 auto 24px;display:block;padding:0 16px}
textarea{width:100%;min-height:70px;background:var(--card);color:var(--text);border:1px solid #ffffff22;border-radius:8px;padding:8px;font:13px monospace}
</style></head><body>
<header><h1>Ausrüstungs-Auswahl</h1><span id="zaehler"></span><button id="kopieren">Auswahl kopieren</button></header>
<main id="liste"></main>
<div id="ausgabe"><p class="tag">Diese Zeile in den Chat einfügen:</p><textarea id="text" readonly></textarea></div>
<script>
const DATA = __DATA__;
let wahl = {};
try { wahl = JSON.parse(localStorage.getItem("waffen_wahl") || "{}"); } catch (e) {}
const liste = document.getElementById("liste");
function zeichnen() {
  liste.innerHTML = "";
  let abschnitt = "Waffen";
  liste.insertAdjacentHTML("beforeend", `<h2 class="abschnitt">Waffen</h2>`);
  for (const w of DATA) {
    if ((w.section || "Waffen") !== abschnitt) {
      abschnitt = w.section;
      liste.insertAdjacentHTML("beforeend", `<h2 class="abschnitt">${abschnitt}</h2>`);
    }
    const k = document.createElement("section");
    k.className = "karte" + (w.shape ? " " + w.shape : ""); k.style.setProperty("--c", w.color);
    k.innerHTML = `<div class="kopf"><b>${w.label}</b><span class="rar">${w.rarity}</span>
      <span class="tag">${w.type} · Element ${w.element} · ${w.slots} Slot${w.slots === 2 ? "s" : ""}</span></div>`;
    const r = document.createElement("div"); r.className = "reihe";
    if (!w.imgs.length) r.innerHTML = `<div class="leer">noch keine Bilder</div>`;
    for (const im of w.imgs) {
      const b = document.createElement("div");
      b.className = "bild" + (wahl[w.id] === im.k ? " gewaehlt" : "");
      b.innerHTML = `<img src="${im.src}" alt="${w.label} Variante ${im.k}"><span>${im.k}</span>`;
      b.onclick = () => { wahl[w.id] = wahl[w.id] === im.k ? undefined : im.k; speichern(); zeichnen(); };
      r.appendChild(b);
    }
    k.appendChild(r); liste.appendChild(k);
  }
  const n = Object.values(wahl).filter(Boolean).length;
  document.getElementById("zaehler").textContent = `${n} von ${DATA.length} gewählt`;
  document.getElementById("text").value = "Waffenwahl: " +
    DATA.filter(w => wahl[w.id]).map(w => `${w.id}=${wahl[w.id]}`).join(" ");
}
function speichern() { try { localStorage.setItem("waffen_wahl", JSON.stringify(wahl)); } catch (e) {} }
document.getElementById("kopieren").onclick = async () => {
  const t = document.getElementById("text"); t.select();
  try { await navigator.clipboard.writeText(t.value); } catch (e) { document.execCommand("copy"); }
};
zeichnen();
</script></body></html>
"""

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--queue" in args:
        queue([a for a in args if not a.startswith("-")])
    elif "--build" in args:
        build()
    elif "--pick" in args:
        pick([a for a in args if "=" in a])
    else:
        print(__doc__)

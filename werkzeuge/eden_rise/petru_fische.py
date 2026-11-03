# -*- coding: utf-8 -*-
"""Petrus Fisch-Saetze (Brain Trust, Duc 28.10.2026): beim ERSTEN Verkauf einer Fischart an Petru sagt er, was der Fisch ist,
was ihn besonders macht und warum er so viel dafuer zahlt. Danach steht der Satz als seine Notiz im Journal ("Ask Petru about
it." vorher). Stimme nach docs/wiki/figuren/petru.md: wenige Worte, ganze Saetze, Bilder vom Meer, Tags nur trocken.

Preis nach Seltenheit (FISCH_STUFE in kochen_daten.py): Stufe 1 wenig, 2 fair, 3 gut - der Satz sagt es passend.
Eingebaut (28.10.2026): kochen_daten.py haengt SAETZE als Zeilen-Gruppen fisch_<id> an PETRU_LADEN (laeden.json, Vertonung)
und als Journal-Notiz (kuechen.json petru.fisch_notiz). Hier also nur Saetze aendern, dann kochen_eden_rise.py bauen.

    python werkzeuge\\eden_rise\\petru_fische.py   -> docs\\abnahme\\petru_fische\\index.html (+ bilder\\)
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

# Ankauf bei Petru je Stufe (Lola zahlt fuer jeden Fisch 60 %) - kochen_daten.py uebernimmt das fuer kuechen.json
PETRU_ANTEIL = {1: 0.50, 2: 0.65, 3: 0.80}
# gefuehl der Sprite je Satz in laeden.json
GEFUEHL = "neutral"

# id -> gesprochene Fassung mit Turbo-Tag (der Bildschirm zeigt sie ohne Tag)
SAETZE = {
    # Meer
    "sardine": "Sardines come in their thousands every summer, so nobody pays much for one. [sniff] Grill it with salt "
               "and eat it with your fingers. On this coast that is still the best supper there is.",
    "gilt_head_bream": "See the gold between the eyes? That's how you know her. [clear throat] She cracks mussels with "
                       "those teeth, so the meat is sweet, but half the harbour catches her, and I can't pay much.",
    "red_mullet": "Two whiskers to taste the sand with. [chuckle] The Romans paid silver for this fish, they say. Today "
                  "I pay you a few coins, and that is how the world goes.",
    "sea_bass": "The French call him the sea wolf. He hunts in the white water where the waves break, when it is too "
                "rough for anyone sensible. [sigh] There are plenty in the bay, so the price is small.",
    "scorpionfish": "Careful with the spines, they sting worse than a wasp. [clear throat] Ugly fish. But without him "
                    "there is no real bouillabaisse, so I pay you a fair price.",
    "cuttlefish": "She changes colour while you watch her, when she's afraid and when she's curious. [sniff] The ink "
                  "turns rice black, and the bone inside goes to the birds. A fair price for all of that.",
    "octopus": "Hm. Clever animal. [chuckle] Bastianu, at my workshop, opens jars when I'm not looking. Don't tell him "
               "I bought this one. Fair price.",
    "salmon": "A salmon, here? He must have lost his way to the north. [sniff] They say he finds the river he was born "
              "in by the smell, after years at sea. I pay fair for a fish that far from home.",
    "red_prawn": "From the deep water off the cape, where the light never reaches. [sniff] Red before it ever sees a "
                 "pan. The restaurants in Bastia fight over these, so I pay you well.",
    "spiny_lobster": "No claws, only spines and those long whips. [clear throat] Hold him close to your ear, he creaks "
                     "when he's angry. Weddings, baptisms, festas: for him I pay the best price I have.",
    # Fluss
    "brown_trout": "A trout from the cold water up high. [sniff] Look at the spots, every stream paints them a little "
                   "differently. The hills are full of streams, though, so I can't pay much.",
    "perch": "Stripes like a small tiger, and a fin that bites back if you grab him wrong. [chuckle] Where there is "
             "one, there are twenty. So, not much money.",
    "carp": "The monks kept carp in their ponds for the fasting days. [sigh] Slow fish, and he lives longer than most "
            "dogs. He tastes of mud if you cook him wrong, so the price is small.",
    "tench": "The doctor fish. The old men say the others rub against him when they are sick, because of the slime. "
             "[clear throat] I don't know if it's true. Cheap, but honest.",
    "barbel": "Four whiskers, and he reads the riverbed with them like a blind man reads a face. [sniff] Don't eat the "
              "eggs, they'll keep you in bed for two days. A fair price for a fair fish.",
    "river_crayfish": "He only lives where the water is clean. [sigh] When the crayfish leave a stream, something "
                      "upstream is wrong. I pay fair for good news like that.",
    "river_crab": "A crab that has never seen the sea. [chuckle] At night he climbs out and sits on the warm stones "
                  "like an old man. Hm. Odd neighbour. Fair price.",
    "pike": "He waits in the reeds without moving, an hour if he has to, and then he takes a duckling off the water. "
            "[clear throat] Mind the teeth, they point backwards. Fair price.",
    "eel": "Every eel in this river was born on the other side of the ocean, and one day she swims all the way back. "
           "[sigh] Nobody has ever seen where. I pay well for a traveller like that.",
    "zander": "The zander. Eyes like a cat, so he hunts at night while the others sleep. [sniff] Firm white meat, no "
              "mud in it at all. I pay you well for him.",
}

STUFE_TEXT = {1: "häufig", 2: "mittel", 3: "selten"}
WASSER = {"meer": "Meer (Boot)", "fluss": "Fluss (Rastplätze)"}
TAG = re.compile(r"\s*\[[a-z ]+\]")


def ohne_tags(t):
    return TAG.sub("", t).strip()


def seite():
    from PIL import Image
    import kochen_daten as D
    ziel = os.path.join(EDEN, "docs", "abnahme", "petru_fische")
    os.makedirs(os.path.join(ziel, "bilder"), exist_ok=True)
    fische = D.FISCHE                      # Lachs statt Little Tunny (Duc 28.10.2026) steht seit dem Kuechen-Commit dort
    fehler = sorted(set(SAETZE) ^ {f[0] for f in fische})
    if fehler:
        raise SystemExit("SAETZE passt nicht zu FISCHE: %s" % fehler)
    import json, subprocess
    idx = json.load(open(os.path.join(EDEN, "module", "eden_rise", "audio_index.json"), encoding="utf-8"))
    os.makedirs(os.path.join(ziel, "audio"), exist_ok=True)
    karten = []
    for fid, label, _kind, ort, _roh, preis, _text, _motiv in fische:
        st = D.FISCH_STUFE[fid]
        quelle = os.path.join(EDEN, "module", "eden_rise", "farm", "fische", fid + ".png")
        if os.path.isfile(quelle):
            im = Image.open(quelle).convert("RGBA")
            im.thumbnail((320, 320))
            im.save(os.path.join(ziel, "bilder", fid + ".webp"), quality=88)
        satz = SAETZE[fid]
        e = idx.get("laden.petru.fisch_%s.0" % fid)            # Aufnahme (Vertonen_EdenRise.bat --praefix laden.petru.fisch_)
        ton = ""
        if e and os.path.isfile(os.path.join(EDEN, "module", "eden_rise", "audio", e["datei"])):
            name = fid + ".mp3"                                 # klein fuer die Abnahme (die WAVs bleiben im Spiel)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(EDEN, "module", "eden_rise", "audio", e["datei"]),
                            "-q:a", "5", os.path.join(ziel, "audio", name)], check=True)
            ton = '<audio controls preload="none" src="audio/%s"></audio>' % name
        tags = " ".join(TAG.findall(satz)).strip()
        karten.append(
            '<article class="k s%d" data-wasser="%s"><img src="bilder/%s.webp" alt=""><div class="t">'
            '<h2>%s</h2><p class="m">%s · Stufe %d %s · roh %d € · Petru %d € <small>(Lola %d €)</small></p>'
            '<p class="z">%s</p>%s<p class="g">Stimme: %s · Schlüssel <code>laden.petru.fisch_%s</code></p></div></article>'
            % (st, ort, fid, html.escape(label), WASSER[ort], st, STUFE_TEXT[st], preis,
               round(preis * PETRU_ANTEIL[st]), round(preis * 0.6), html.escape(ohne_tags(satz)), ton, html.escape(tags), fid))
    doc = """<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Petrus Fisch-Sätze</title><style>
:root{--bg:#f3efe6;--card:#fffdf8;--fg:#1f2a2e;--mut:#5f6b6e;--line:#d9d1c1;--s1:#7a8f86;--s2:#2f6f8f;--s3:#a8742a}
@media (prefers-color-scheme:dark){:root{--bg:#121a1d;--card:#1a2428;--fg:#e8e4da;--mut:#9aa7a8;--line:#2c3a3f;color-scheme:dark}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,"Times New Roman",serif;padding:24px 16px 48px}
main{max-width:980px;margin:0 auto}h1{font-size:28px;margin:0 0 4px}.lead{color:var(--mut);max-width:70ch;font-family:system-ui,sans-serif;font-size:14px}
nav{display:flex;gap:8px;margin:16px 0;font-family:system-ui,sans-serif}nav button{border:1px solid var(--line);background:var(--card);color:var(--fg);padding:6px 12px;border-radius:999px;cursor:pointer}
nav button[aria-pressed=true]{background:var(--fg);color:var(--bg)}
.grid{display:grid;gap:14px}.k{display:grid;grid-template-columns:120px 1fr;gap:16px;background:var(--card);border:1px solid var(--line);border-left:5px solid var(--s1);border-radius:8px;padding:14px}
.k.s2{border-left-color:var(--s2)}.k.s3{border-left-color:var(--s3)}.k img{width:120px;height:90px;object-fit:contain}
.t{min-width:0}h2{margin:0;font-size:19px}.m,.g{font-family:system-ui,sans-serif;font-size:13px;color:var(--mut);margin:2px 0 8px}
.z{font-size:18px;margin:0 0 6px}.z::before{content:"\\201C"}.z::after{content:"\\201D"}code{font-size:12px}
.k[hidden]{display:none}audio{width:100%%;max-width:420px;height:34px;margin:2px 0 6px}@media (max-width:560px){.k{grid-template-columns:1fr}}
</style></head><body><main>
<h1>Petrus Fisch-Sätze</h1>
<p class="lead">20 Zeilen, je eine pro Fischart. Petru sagt sie beim <b>ersten Verkauf dieser Art an ihn</b>; danach steht der Satz als
seine Notiz im Journal (vorher: „Ask Petru about it.“). Aufbau: was der Fisch ist · was ihn besonders macht · warum er so viel zahlt
(Stufe 1 wenig, 2 fair, 3 gut). Petru zahlt 50 / 65 / 80 %% je Stufe (+5 %% je Vertrauensstufe), Lola immer 60 %%. Abgenommen und vertont (28.10.).</p>
<nav><button data-f="alle" aria-pressed="true">Alle</button><button data-f="meer" aria-pressed="false">Meer</button><button data-f="fluss" aria-pressed="false">Fluss</button></nav>
<div class="grid">%s</div></main>
<script>document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{document.querySelectorAll("nav button").forEach(x=>x.setAttribute("aria-pressed",x===b));
document.querySelectorAll(".k").forEach(k=>k.hidden=b.dataset.f!=="alle"&&k.dataset.wasser!==b.dataset.f)});</script>
</body></html>""" % "".join(karten)
    open(os.path.join(ziel, "index.html"), "w", encoding="utf-8").write(doc)
    print("ok", len(karten), "Saetze ->", ziel)


if __name__ == "__main__":
    seite()

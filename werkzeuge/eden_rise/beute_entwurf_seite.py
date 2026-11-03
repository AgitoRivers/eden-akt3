# -*- coding: utf-8 -*-
"""Abnahmeseite Beute (docs/abnahme/beute_tabellen, Port 8397): Reiter Tabellen je Gegnerart + Zuordnung je Gegner und
je Gegenstand. Entwurfsdaten der Beute-Diskussion 28.10.2026 (ARTEN, SIGNATUR) - Quelle fuer den spaeteren Einbau."""
import html, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
MOD = r"X:\AI\Eden\module\eden_rise"
ZIEL = r"X:\AI\Eden\docs\abnahme\beute_tabellen"
B = os.path.join(ZIEL, "bilder")
if os.path.isdir(B):
    for f in os.listdir(B):
        os.remove(os.path.join(B, f))          # generated copies of module images, rebuilt below
os.makedirs(B, exist_ok=True)
items = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))["items"]
kd = json.load(open(os.path.join(MOD, "kaempfe.json"), encoding="utf-8"))
mats = kd["werkstatt"]["materialien"]
zut = json.load(open(os.path.join(MOD, "kuechen.json"), encoding="utf-8"))["zutaten"]
enemies = kd["enemies"]
DROPS = kd["chips"]["drops"]

STUFEN = [("gewoehnlich", "gewöhnlich", "55 %"), ("gut", "gut", "30 %"), ("selten", "selten", "12 %"),
          ("meisterlich", "meisterlich", "3 %")]
SONDER = {"_wert_g": "Wertsache des Ortes (gewöhnlich)", "_wert_gut": "Wertsache des Ortes (gut)",
          "_wert_s": "Wertsache des Ortes (selten)", "_unikat": "Unikat des Ortes (einmal)",
          "_modul1": "Modul Stufe 1 (zufällige Familie)", "_modul2": "Modul Stufe 2 (zufällige Familie)", "_modul3": "Modul Stufe 3 (zufällige Familie)"}
DOPPELT = {"plaster", "cooling_spray", "bandage", "verbandskasten", "grenade_fire", "grenade_water", "grenade_shock",
           "grenade_flash", "smoke_pot", "antidote"}                       # 5: im Kampf nuetzlich -> doppelt so oft
KUECHE = set(zut)                                                         # 3: geht in den Kuechenvorrat, nicht in die Tasche

ARTEN = [
    ("mensch", "Menschen", "Piraten, Schmuggler, Agenten, der Big Man, Wolff, Riscossore. Verbandszeug, Granaten, "
     "Schmuggelware, Schmuck. Dazu Geld (Punkt 3).", {
        "gewoehnlich": ["plaster", "cooling_spray", "toastie", "cannoli", "_wert_g"],
        "gut": ["_modul1", "bandage", "verbandskasten", "grenade_fire", "grenade_water", "grenade_shock", "grenade_flash",
                "smoke_pot", "whetstone", "kupfer", "steel_plate", "cigars", "cuban_rum", "_wert_gut"],
        "selten": ["_modul2", "grenade_concussion", "grenade_shrapnel", "lockpicks", "_wert_s"],
        "meisterlich": ["_modul3", "_unikat"]}),
    ("tier", "Tiere", "Ratten, Hunde, Keiler, Wölfe, Schlangen, Raubkatzen. Keine Edelsteine: Fleisch und Funde für die "
     "Küche, Gift für Gegengift. Das Halsband-Modul bleibt fester Drop.", {
        "gewoehnlich": ["eggs", "wildkraeuter", "feigen", "pretty_shell"],
        "gut": ["_modul1", "pork", "antidote", "myrtle", "seeglas"],
        "selten": ["_modul2", "truffle"],
        "meisterlich": ["_modul3", "_unikat"]}),
    ("flieger", "Flieger", "Möwen, Kevins Tauben, Kevin, Fledermäuse. Elster-Prinzip: Sie stehlen Essen und alles, was "
     "glänzt – deshalb die Stufe-1-Steine.", {
        "gewoehnlich": ["ocean_popcorn", "toastie", "seegras_chips", "pretty_shell"],
        "gut": ["_modul1", "jade", "topas", "aquamarin", "amethyst", "silberring", "shell_anklet"],
        "selten": ["_modul2", "pink_pearl", "goldkette"],
        "meisterlich": ["_modul3", "_unikat"]}),
    ("maschine", "Maschinen", "Unit-01, später mehr in Akt 3. Technik zum Ausschlachten.", {
        "gewoehnlich": ["duct_tape", "uhrenbatterie"],
        "gut": ["_modul1", "kupfer", "steel_plate", "relais", "antennenkabel"],
        "selten": ["_modul2", "ersatzzellen"],
        "meisterlich": ["_modul3", "netzknoten"]}),
]
SIGNATUR = [  # (Ort, Gegner, Item oder None, Text, fest) - Duc 28.10.2026: alle ja
    ("Hafen", "Seagull on the Aft Deck", "lolas_kekse", "Sie hat Lola die Kekse geklaut – zurückbringen gibt eine kleine Szene.", False),
    ("Hafen", "Rat in the Workshop", "duct_tape", "Lebt in Rosis Werkstatt und hat sich am Klebeband vergriffen.", False),
    ("Hafen / Grotte", "Pirate with a Torch", "smoke_pot", "Wer mit Feuer kämpft, hat Rauch dabei.", False),
    ("Kloster", "Alpha Boar at the Bridge", "truffle", "Ein Schwein mit den richtigen Prioritäten.", False),
    ("Kloster", "Ape (Ambush in the Camp)", "feigen", "Hat das Lager geplündert.", False),
    ("Kloster", "The Black Lion", "steel_plate", "Eine Panzerplatte aus Alons Labor, von Schulter oder Flanke. Fester Drop.", True),
    ("Berge", "A Man in Black", "grenade_shock", "Er wirft im Kampf eine Schockgranate – und hat noch eine.", False),
    ("Berge", "Two on the Ridge", "grenade_flash", "Die beiden blenden mit einer Blendgranate.", False),
    ("Berge", "Lights on the Ridge (Umweg)", "grenade_water", "Wassergranate, dann der Taser des Partners: Kurzschluss.",
     False),
    ("Berge", "Old Grey", None, "<b>Old Grey's Collar Tag</b> (neu, fest): Rosi baut die Marke zum Modul <b>Calm Mind</b> um "
     "(Familie Parade, Stufe 2: Parade-Fenster +15 %).", True),
    ("Grotte", "Smuggler (Cards on a Crate)", "cuban_rum", "Schmuggelware aus der Kiste, auf der er spielt.", False),
    ("Grotte", "Kevin's Pigeons", "ocean_popcorn", "Kevins Bande klaut Essen.", False),
    ("Grotte", "Kevin", "kevins_rache", "Seine geklauten Kekse – er ist nur mit Essen zu bezirzen.", False),
    ("Grotte", "Unit-01 (Red Eye)", None, "<b>Unit-01 Steel Plate</b> (neu): rot lackierte Panzerplatte, zählt bei Rosi wie "
     "eine normale Steel Plate.", False),
]


def info(iid):
    if iid in SONDER:
        return SONDER[iid], None, None
    if iid in mats:
        lab, preis = mats[iid], (items.get(iid) or {}).get("preis")
    elif iid in items:
        lab, preis = items[iid].get("label") or iid, items[iid].get("preis")
    elif iid in zut:
        lab, preis = zut[iid]["label"], zut[iid].get("preis")
    else:
        raise KeyError(iid)
    bild = None
    src = os.path.join(MOD, "items", iid + ".webp")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(B, iid + ".webp"))
        bild = "bilder/%s.webp" % iid
    return lab, preis, bild


def zelle(iid):
    lab, preis, bild = info(iid)
    img = '<img src="%s" alt="">' % bild if bild else '<span class="ph">✦</span>'
    p = '<span class="p">%s €</span>' % preis if preis else ""
    marke = ('<span class="mk x2" title="doppelt so oft">×2</span>' if iid in DOPPELT else "") + \
            ('<span class="mk ku" title="geht in die Küche, nicht in die Tasche">Küche</span>' if iid in KUECHE else "")
    cls = " sonder" if iid in SONDER else ""
    return '<li class="it%s">%s<span class="n">%s</span>%s%s</li>' % (cls, img, html.escape(lab), p, marke)


def gegnerliste(cls):
    out = []
    for gid, g in enemies.items():
        if g.get("cls") == cls:
            d = DROPS.get(gid)
            dtxt = (" · Modul %s %s" % (d[0], d[1])) if isinstance(d, list) else (" · fest: eins aus" if d else "")
            out.append("%s <small>(%s%s)</small>" % (html.escape(g["name"]), g["tier"], dtxt))
    return ", ".join(out)


teile = []
for cls, titel, txt, tab in ARTEN:
    reihen = "".join('<div class="st st-%s"><div class="sl"><b>%s</b><span>%s</span></div><ul>%s</ul></div>'
                     % (k, name, ch, "".join(zelle(i) for i in tab[k])) for k, name, ch in STUFEN)
    teile.append('<section id="%s"><h2>%s</h2><p class="m">%s</p>%s<details><summary>Gegner dieser Art</summary>'
                 '<p class="g">%s</p></details></section>' % (cls, titel, txt, reihen, gegnerliste(cls)))
sig = "".join('<div class="st st-%s"><div class="sl"><b>%s</b><span>%s · %s</span></div><ul>%s<li class="txt">%s</li></ul></div>'
              % ("meisterlich" if fest else "gewoehnlich", html.escape(w), o, "fester Drop" if fest else "statt gewöhnlich",
                 zelle(i) if i else "", t) for o, w, i, t, fest in SIGNATUR)
teile.append('<section id="signatur"><h2>Signatur-Drops</h2><p class="m">Benannte Gegner ersetzen ihre gewöhnliche Stufe '
             'durch ein festes Stück; Löwe und Old Grey geben ihres immer (zusätzlich zum Halsband-Modul). Bewusst ohne: '
             'das Bärenjunge (ein Junges plündert man nicht), der Big Man mit seinen Agenten in der Bergerie, Riscossore, Vampirin, Sirene (eigener fester Drop), '
             'Wolff (Képi kommt aus der Story).</p>%s</section>' % sig)
monster = ", ".join(html.escape(g["name"]) for g in enemies.values() if g.get("cls") == "monster")

# ---------------------------------------------------------------- Reiter 2: Zuordnung je Gegner + je Gegenstand
SIG_ZIEL = [("enc", ["akt1_moewe"]), ("enc", ["akt1_ratte"]), ("typ", ["fackelpirat"]), ("typ", ["keiler_kloster"]),
            ("enc", ["kloster_7_affe"]), ("typ", ["loewe_schwarz"]), ("typ", ["agent"]), ("typ", ["agent_fuehrer"]), ("typ", ["agent_nass"]), ("typ", ["old_grey"]),
            ("typ", ["schmuggler"]), ("typ", ["tauben"]), ("typ", ["kevin"]), ("typ", ["unit01"])]
ORTE = [("akt1_", "Hafen"), ("hafen_", "Hafen"), ("kloster_", "Kloster"), ("berge_", "Berge"), ("gr_", "Grotte"),
        ("fn_", "Grotte · Flut-Nacht"), ("kv_", "Kevins Dächer"), ("a2_", "Akt 2"), ("maxwell_", "Training")]
ARTNAME = {"mensch": "Menschen", "tier": "Tiere", "flieger": "Flieger", "maschine": "Maschinen", "monster": "–"}
OHNE = {"maxwell": "– (Training)", "baer_junges": "– (Junges, man plündert es nicht)"}
EXTRA_FEST = {"sirene": "Sapphire (Event nach dem Gespräch)"}
erw = json.load(open(os.path.join(MOD, "erweiterungen.json"), encoding="utf-8"))["erweiterungen"]
erw = erw.values() if isinstance(erw, dict) else erw
CHIP = {(c["familie"], c["stufe"]): c["label"] for c in erw}
enc = kd["encounters"]


def enc_typ(e):
    g = e.get("enemies") or e.get("gegner") or e.get("enemy")
    return g if isinstance(g, str) else [x if isinstance(x, str) else (x.get("id") or x.get("typ")) for x in g][0]


def ort(bid):
    return next((o for p, o in ORTE if bid.startswith(p)), "Test")


def mini(iid):
    if not iid:
        return ""
    lab, _, bild = info(iid)
    return ('<img class="mi" src="%s" alt="">' % bild if bild else "") + html.escape(lab)


zeilen = []
for gid, g in enemies.items():
    orte = sorted({ort(b) for b, e in enc.items() if enc_typ(e) == gid} - {"Test"})
    sigs = []
    for (o, w, i, t, fest), (art, ziele) in zip(SIGNATUR, SIG_ZIEL):
        if art == "typ" and gid in ziele:
            sigs.append((mini(i) or t.split("</b>")[0].replace("<b>", "")) + (' <span class="mk x2">immer</span>' if fest else ""))
        elif art == "enc" and enc_typ(enc[ziele[0]]) == gid:
            sigs.append(mini(i) + ' <small>(nur „%s“)</small>' % html.escape(enc[ziele[0]].get("title", "")))
    d = DROPS.get(gid)
    if isinstance(d, list):
        fest_txt = "Modul %s <small>(%s %s)</small>" % (html.escape(CHIP.get((d[0], d[1]), d[0])), d[0], d[1])
    elif d:
        fest_txt = "eins aus: Modul St. 2 · 120 € · Stufe-1-Material"
    else:
        fest_txt = ""
    if gid in EXTRA_FEST:
        fest_txt = (fest_txt + " · " if fest_txt else "") + EXTRA_FEST[gid]
    tabelle = OHNE.get(gid) or ARTNAME.get(g.get("cls"), "?")
    zeilen.append((orte[0] if orte else "zz", '<tr><td><b>%s</b><br><small>%s · %s</small></td><td>%s</td><td>%s</td><td>%s</td>'
                   '<td>%s</td></tr>' % (html.escape(g["name"]), g.get("cls"), g["tier"], ", ".join(orte) or "–",
                                         tabelle, "<br>".join(sigs) or '<span class="leer">–</span>',
                                         fest_txt or '<span class="leer">–</span>')))
ORDNUNG = ["Hafen", "Training", "Kloster", "Berge", "Grotte", "Kevins Dächer", "Grotte · Flut-Nacht", "Akt 2", "zz"]
zeilen.sort(key=lambda x: ORDNUNG.index(x[0]) if x[0] in ORDNUNG else 99)
gegner_tab = ('<section><h2>Je Gegner</h2><p class="m">Welche Tabelle gilt, welcher Signatur-Drop, welcher feste Drop. '
              'Sortiert nach dem ersten Ort.</p><div class="scroll"><table class="gt"><tr><th>Gegner</th><th>Orte</th>'
              '<th>Tabelle</th><th>Signatur</th><th>Fester Drop</th></tr>%s</table></div></section>'
              % "".join(z for _, z in zeilen))

quellen = {}
for cls, titel, txt, tab in ARTEN:
    for k, name, ch in STUFEN:
        for i in tab[k]:
            if i not in SONDER:
                quellen.setdefault(i, []).append('<span class="q st-%s">%s · %s</span>' % (k, titel, name))
for o, w, i, t, fest in SIGNATUR:
    if i:
        quellen.setdefault(i, []).append('<span class="q sig">Signatur: %s</span>' % html.escape(w))
for m in DROPS["vampirin"]["eins_aus"][2][1]:
    quellen.setdefault(m, []).append('<span class="q sig">Vampirin (eins aus)</span>')
quellen.setdefault("saphir", []).append('<span class="q sig">Sirene (Event)</span>')
item_zeilen = []
for i, qs in quellen.items():
    lab, preis, bild = info(i)
    laden = ", ".join((items.get(i) or {}).get("wo") or [])
    item_zeilen.append((lab.lower(), '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                        % (mini(i), "%s €" % preis if preis else "–", " ".join(qs), laden or '<span class="leer">–</span>')))
item_tab = ('<section><h2>Je Gegenstand</h2><p class="m">Wo jedes Stück schon vergeben ist: Tabellen, Signatur, feste '
            'Drops – und in welchem Laden man es außerdem kaufen kann.</p><div class="scroll"><table class="gt"><tr>'
            '<th>Gegenstand</th><th>Preis</th><th>Kommt aus</th><th>Laden</th></tr>%s</table></div></section>'
            % "".join(z for _, z in sorted(item_zeilen)))

seite = """<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Beutetabellen je Gegnerart</title><style>
:root{--bg:#10141b;--k:#171c25;--l:#2a3242;--t:#ece6d8;--d:#9aa3b5;--a:#e2b86b;
--g1:#8d939e;--g2:#6fb27a;--g3:#5b9be0;--g4:#d39b3a}
body{margin:0;background:var(--bg);color:var(--t);font:15px/1.5 system-ui,sans-serif;padding:28px 20px}
main{max-width:1150px;margin:0 auto;display:grid;gap:18px}h1{margin:0;color:var(--a)}
.lead{color:var(--d);max-width:75ch;margin:0}section{background:var(--k);border:1px solid var(--l);border-radius:12px;padding:16px 18px}
h2{margin:0 0 2px}.m{color:var(--d);margin:0 0 12px;max-width:90ch}
.st{display:grid;grid-template-columns:150px 1fr;gap:12px;padding:8px 0;border-top:1px solid var(--l)}
.sl{display:flex;flex-direction:column;border-left:4px solid var(--c);padding-left:10px}.sl span{color:var(--d);font-size:13px}
.st-gewoehnlich{--c:var(--g1)}.st-gut{--c:var(--g2)}.st-selten{--c:var(--g3)}.st-meisterlich{--c:var(--g4)}
ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.it{display:flex;align-items:center;gap:8px;background:#0d1117;border:1px solid var(--l);border-radius:8px;padding:4px 10px 4px 4px}
.it img{width:40px;height:40px;object-fit:contain;border-radius:6px;background:#1b2130}.ph{width:40px;height:40px;display:grid;place-items:center;color:var(--c)}
.it.sonder{border-style:dashed}.n{font-size:14px}.p{color:var(--d);font-size:12px;font-variant-numeric:tabular-nums}
.mk{font-size:11px;padding:1px 6px;border-radius:10px;font-weight:600}.x2{background:#3b2f14;color:var(--a)}.ku{background:#173322;color:#8fd6a0}
.txt{color:var(--d);max-width:70ch}
details{margin-top:10px;color:var(--d)}summary{cursor:pointer}.g{font-size:13px}
.regeln{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.regeln div{background:var(--k);border:1px solid var(--l);border-radius:12px;padding:12px 14px}.regeln h3{margin:0 0 4px;font-size:15px;color:var(--a)}
table{border-collapse:collapse;font-variant-numeric:tabular-nums}td,th{padding:3px 10px;border-bottom:1px solid var(--l);text-align:left}
.tabs{display:flex;gap:8px;border-bottom:1px solid var(--l)}.tabs button{background:none;border:0;border-bottom:3px solid transparent;
color:var(--d);font:600 15px system-ui,sans-serif;padding:8px 14px;cursor:pointer}.tabs button.an{color:var(--a);border-color:var(--a)}
.reiter{display:grid;gap:18px}.reiter[hidden]{display:none}.scroll{overflow-x:auto}
.gt{width:100%}.gt td{vertical-align:top;padding:7px 10px}.gt th{color:var(--d);font-weight:600;font-size:13px}
.gt small{color:var(--d)}.mi{width:26px;height:26px;object-fit:contain;vertical-align:middle;margin-right:6px;border-radius:4px;background:#1b2130}
.leer{color:var(--l)}.q{display:inline-block;font-size:12px;padding:1px 8px;margin:2px 4px 2px 0;border-radius:10px;border:1px solid var(--c,#555);color:var(--t)}
.q.sig{--c:#c06bd3}
</style></head><body><main>
<h1>Beutetabellen je Gegnerart</h1>
<nav class="tabs"><button data-t="tabellen" class="an">Tabellen</button><button data-t="gegner">Zuordnung Gegner &amp; Gegenstände</button></nav>
<div class="reiter" id="r-tabellen">
<p class="lead">Entwurf zu Punkt 1, Runde 2 nach Ducs Antworten. Jeder Kampf gibt genau <b>ein</b> Stück: erst die Stufe
würfeln, dann ein Stück aus der Liste. <span class="mk x2">×2</span> = doppelt so oft (im Kampf nützlich).
<span class="mk ku">Küche</span> = geht in den Küchenvorrat, nicht in die Tasche. Preise = heutige Ladenpreise.</p>
<div class="regeln">
<div><h3>Können (1a–1c)</h3>Vorteil: ein Wurf mehr, das beste zählt, höchstens drei. Zählt nur: <b>perfekte Paraden
oder perfektes Ausweichen</b> und <b>Sieg ohne Treffer</b>. Das Spiel sagt es nirgends.</div>
<div><h3>Chancen</h3><table><tr><th></th><th>selten+</th><th>meisterl.</th></tr>
<tr><td>1 Wurf</td><td>15 %</td><td>3 %</td></tr><tr><td>2 Würfe</td><td>28 %</td><td>6 %</td></tr>
<tr><td>3 Würfe</td><td>39 %</td><td>9 %</td></tr></table></div>
<div><h3>Stufe-2-Material</h3>Kommt in <b>keiner</b> Tabelle vor – nur von einzigartigen Gegnern oder aus Missionen.
Heute: der Saphir der Sirene. Akt 1 hat keins. Wo die anderen herkommen, ist offen.</div>
<div><h3>Bleibt fest dazu</h3>Halsband-Module der Tiere und Agenten, Riscossore-Modul, Vampirin (eins aus).
<b>Monster</b> (""" + monster + """) haben nur ihren festen Drop.</div>
</div>
""" + "".join(teile) + """
</div>
<div class="reiter" id="r-gegner" hidden>""" + gegner_tab + item_tab + """</div>
<script>
function zeige(t){document.querySelectorAll('.reiter').forEach(r=>r.hidden=r.id!=='r-'+t);
document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('an',b.dataset.t===t));}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{zeige(b.dataset.t);history.replaceState(null,'','#'+b.dataset.t);});
if(location.hash==='#gegner')zeige('gegner');
</script>
</main></body></html>"""
open(os.path.join(ZIEL, "index.html"), "w", encoding="utf-8").write(seite)
print("ok", len(os.listdir(B)), "Bilder")

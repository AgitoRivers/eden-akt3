# -*- coding: utf-8 -*-
r"""Nachtlauf 19.10.2026: Sprites fuer Mr. Maximum, Yamamoto-san und Jana Maihoff in die ComfyUI-Warteschlange.

    volllauf_maximum_yamamoto_jana.py          Probelauf: frischt nichts auf, zeigt Plan und Abgleich
    volllauf_maximum_yamamoto_jana.py --los    frischt die Steckbriefe aus Prompt Studio auf und stellt die Laeufe ein

Nutzt den Code des Char Creators direkt (kein Server noetig); Prompt Studio (8301) und ComfyUI (8189) muessen laufen.
1. Kostueme wie in Prompt Studio (sp_kost): Yamamoto + Party, Jana + Kink.
2. Outfits/Optik aus den Kostuem-Presets holen (aus_ps_laden) und die Dreiwege-Basis setzen.
3. Laeufe (Ducs Auftrag): beide Maenner SFW mit allen Kostuemen; Jana SFW Deck/Bikini/Party Dress,
   voll Kitty/Kink. ersetzen=True: alte Testbilder wandern nach output\_expressions_papierkorb.
ComfyUI arbeitet die Warteschlange danach allein ab; dieses Skript endet sofort.
"""
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"X:\AI\CharCreator")
LOS = "--los" in sys.argv
sys.argv = ["creator.py", "--no-browser"]
import creator as c  # noqa: E402

LAEUFE = [
    ("7ecccb65ef0f", ["Steward", "Training", "Party"], [(None, True)]),
    ("a0ac9a8be128", ["Hawaii", "Badeanzug", "Leder", "Party"], [(None, True)]),
    ("16f8e9cf3e9b", ["Deck", "Bikini", "Party Dress", "Kitty", "Kink"],
     [(["Deck", "Bikini", "Party Dress"], True), (["Kitty", "Kink"], False)]),
]

presets_ps = c.ps("/api/state")["presets"]
gesamt = 0
for fid, kost, laeufe in LAEUFE:
    f = c.fig_laden(fid)
    name = f["name_wunsch"]
    fehlt = [k for k in kost if k not in (c.ps_kostuem_presets(f) or {})]
    if fehlt:
        print("%s: Kostuem-Preset fehlt in Prompt Studio: %s - uebersprungen" % (name, fehlt))
        continue
    if not LOS:
        print("%s: Kostueme %s -> %s" % (name, f["kostueme"], kost))
        continue
    f["kostueme"] = list(kost)
    r = c.aus_ps_laden(f)
    st = c.ps("/api/state")
    optik = {t["name"].lower() for t in st["cfg"]["tags"] if t.get("cat") in c.OPTIK_KAT}
    for k in kost:
        f.setdefault("ps_basis", {})[k] = c._stand_cc(f, k, optik)
    c.fig_speichern(f)
    f = c.fig_laden(fid)
    abw = [a for a in c.abgleich(f) if a["unterschiede"]]
    if abw:
        print("%s: NICHT abgeglichen %s - uebersprungen" % (name, [(a["kost"], a["unterschiede"]) for a in abw]))
        continue
    for nur, sfw in laeufe:
        n = c.volllauf(f, nur, True, [], sfw=sfw)
        f["station"] = 4
        c.fig_speichern(f)
        f = c.fig_laden(fid)
        gesamt += n
        print("%s: %s %s -> %d Bilder in der Warteschlange" % (name, "SFW" if sfw else "VOLL", nur or kost, n))
print(("Gesamt %d Bilder eingestellt." % gesamt) if LOS else "PROBELAUF - nichts eingestellt")

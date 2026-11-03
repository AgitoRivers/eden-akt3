# -*- coding: utf-8 -*-
r"""Musik-Teil der gemeinsamen Vorhoerseite (20.10.2026): offene Song-Takes aus ComfyUI zum Auswaehlen.

Liest die Take-Datensaetze der Musikwerkstatt (ComfyUI_Video_v30 ... output\eden_music\records, Status "drafts") und
zeigt je Song alle Takes mit Player und Haekchen (mehrere moeglich - ein Musik-Slot spielt als Playlist). Daneben,
zugeklappt, was von diesem Song schon im Spiel ist (module\eden_rise\musik\bibliothek.json).
Die Seite verschiebt und schreibt nichts; die Uebernahme ins Spiel ist ein eigener Schritt nach Ducs Auswahl.

    python musik_auswahl.py     -> baut module\eden_rise\sfx\vorhoeren.html neu (SFX + Musik), erzeugt nichts
"""
import json, os, re, sys, urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
MUSIK_OUT = r"X:\AI\ComfyUI_Video_v30\ComfyUI\output\eden_music"
BIBLIOTHEK = os.path.join(EDEN, "module", "eden_rise", "musik", "bibliothek.json")

# Gruppen nach Titelanfang - Reihenfolge = Reihenfolge auf der Seite
GRUPPEN = [("kampf", "Kampf"), ("szenen", "Szenen"), ("events", "Events"), ("kabine", "Kabine"),
           ("figuren", "Figuren-Abende"), ("insel", "Insel / Cuban"), ("finale", "Finale")]


def gruppe(titel):
    t = titel.lower()
    if t.startswith("kampf"):
        return "kampf"
    if t.startswith("event"):
        return "events"
    if t.startswith("kabine"):
        return "kabine"
    if t.startswith(("lola", "alva -", "holm", "casanova")):
        return "figuren"
    if t.startswith("finale"):
        return "finale"
    if "cuban" in t or t.startswith(("cala d", "alvas bar", "la festa", "calvi")):
        return "insel"
    return "szenen"


def datei_url(pfad):
    return "file:///" + urllib.parse.quote(pfad.replace("\\", "/"), safe="/:")


def takes():
    """Offene Takes je Song: {titel: {"zeile": CSV-Zeile, "takes": [record, ...]}}"""
    ordner = os.path.join(MUSIK_OUT, "records")
    songs = {}
    if not os.path.isdir(ordner):
        return songs
    for name in os.listdir(ordner):
        if not name.endswith(".json"):
            continue
        try:
            r = json.load(open(os.path.join(ordner, name), encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if r.get("status") != "drafts" or not os.path.exists(os.path.join(MUSIK_OUT, r.get("audio", ""))):
            continue
        s = songs.setdefault(r["title"], {"zeile": r.get("row", 999), "takes": []})
        s["zeile"] = min(s["zeile"], r.get("row", 999))
        s["takes"].append(r)
    for s in songs.values():
        s["takes"].sort(key=lambda r: r.get("number", 0))
    return songs


def im_spiel():
    """{titel: [track, ...]} - schon freigegebene Tracks (zum Vergleich)."""
    if not os.path.exists(BIBLIOTHEK):
        return {}
    out = {}
    for t in json.load(open(BIBLIOTHEK, encoding="utf-8"))["tracks"]:
        out.setdefault(t["title"], []).append(t)
    return out


def abschnitt(esc):
    """(nav, html, anzahl_takes) fuer den Musik-Bereich der Vorhoerseite."""
    songs, spiel = takes(), im_spiel()
    reihe = sorted(songs.items(), key=lambda kv: (kv[1]["zeile"], kv[0]))
    nav, teile, mnr = [], [], 0
    for gid, gname in GRUPPEN:
        liste = [(t, s) for t, s in reihe if gruppe(t) == gid]
        if not liste:
            continue
        nav.append('<a href="#m_g_%s">%s <span>%d</span></a>' % (gid, gname, len(liste)))
        teile.append('<h2 class="g" id="m_g_%s">%s</h2>' % (gid, gname))
        for titel, s in liste:
            mnr += 1
            slug = re.sub(r"[^a-z0-9]+", "_", titel.lower()).strip("_")
            zeilen = "".join(
                '<label class="var"><input type="checkbox" class="wahl" data-n="%03d" data-v="%s">'
                '<b>Take %03d</b><audio controls preload="none" src="%s"></audio>'
                '<span class="konzept">%s</span></label>'
                % (r["number"], esc(r["id"]), r["number"], datei_url(os.path.join(MUSIK_OUT, r["audio"])),
                   "%d:%02d" % divmod(round(r.get("actual_seconds") or 0), 60))
                for r in s["takes"])
            alt = spiel.get(titel, [])
            vergleich = ('<details class="spiel"><summary>Schon im Spiel: %d Track%s (Slot %s)</summary>%s</details>'
                         % (len(alt), "" if len(alt) == 1 else "s", esc(alt[0]["slot"]), "".join(
                             '<div class="var"><b>%s</b><audio controls preload="none" src="%s"></audio></div>'
                             % (esc(os.path.basename(t["file"])), datei_url(os.path.join(os.path.dirname(BIBLIOTHEK), t["file"])))
                             for t in alt))) if alt else '<p class="leer">Noch nichts davon im Spiel.</p>'
            teile.append(
                '<section id="m_%s" data-mnr="%d" data-mehrfach="1" data-art="Take" data-titel="%s">'
                '<div class="kopf"><h3><span class="nr">M%d</span>%s <span class="st"></span><small>%d Takes</small></h3>'
                '<button class="alle" onclick="alle(this)">▶ alle %d nacheinander</button></div>%s%s'
                '<input class="notiz" placeholder="Notiz (z. B. „Bass zu laut“) – optional"></section>'
                % (slug, mnr, esc(titel), mnr, esc(titel), len(s["takes"]), len(s["takes"]), zeilen, vergleich))
    return "".join(nav), "".join(teile), sum(len(s["takes"]) for s in songs.values())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, HIER)
    import sfx_erzeugen as se
    sfx = json.load(open(os.path.join(se.MOD, "sfx.json"), encoding="utf-8"))["sfx"]
    index = json.load(open(se.INDEX, encoding="utf-8")) if os.path.exists(se.INDEX) else {}
    se.vorhoerseite(sfx, index)
    songs = takes()
    print("Vorhoerseite neu:", os.path.join(se.ORDNER, "vorhoeren.html"), "-", len(songs), "Songs,",
          sum(len(s["takes"]) for s in songs.values()), "offene Takes")


if __name__ == "__main__":
    main()

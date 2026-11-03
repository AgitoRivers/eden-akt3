#!/usr/bin/env python
"""Misst das Gesicht in jedem Sprite und schreibt den Kreis-Ausschnitt nach module/<id>/gesichter.json (Duc 31.10.2026).

Vorher galt fuer alle Figuren derselbe feste Zuschnitt, und Posen und Bildgroessen unterscheiden sich stark: Ligeia
zeigte im Kreis gar kein Gesicht, Wolff den ganzen Koerper, Charly nur Mund und Kinn. Der Client nimmt je Sprite den
hier gemessenen Ausschnitt; Sprites ohne Treffer (Rueckansicht) schaetzen den Kopf aus der Silhouette, sonst gilt der
Mittelwert der Figur. Ein eigener Ausschnitt aus Menue > Portrait crops geht weiter vor.

Eintrag je Sprite: [cx, cy, zoom, r] wie im Client ausschnittStil: Mitte im Bild (0..1), zoom = Bildbreite in
Kreisdurchmessern, r = Hoehe/Breite.

Aufruf (System-Python, dort liegen insightface und onnxruntime):
  python werkzeuge/gesichter_messen.py                 alle Figuren
  python werkzeuge/gesichter_messen.py --nur wolff,bibi  nur diese, der Rest der Datei bleibt
  python werkzeuge/gesichter_messen.py --neu           nur neue und geaenderte Sprites (laeuft bei Start-Eden.bat)
"""
import argparse
import json
import os
import statistics as S
import sys
import time

import numpy as np
from PIL import Image

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WURZEL)
from kern import buehne  # noqa: E402

KOPF_ANTEIL = 0.50      # Gesichtshoehe als Anteil des Kreisdurchmessers
HOEHER = 0.05           # Kreis-Mitte etwas ueber der Gesichtsmitte, damit Haare und Kinn beide Platz haben
MIN_TREFFER = 0.45      # Sicherheit des Detektors
ALPHA_MIN = 0.02        # so viel Bild muss durchsichtig sein, damit die Silhouette etwas sagt


def detektor():
    import onnxruntime
    from insightface.app import FaceAnalysis
    wege = [w for w in ("CUDAExecutionProvider", "CPUExecutionProvider") if w in onnxruntime.get_available_providers()]
    app = FaceAnalysis(name="buffalo_l", allowed_modules=["detection"], providers=wege)
    app.prepare(ctx_id=0 if "CUDAExecutionProvider" in wege else -1, det_size=(640, 640), det_thresh=MIN_TREFFER)
    return app


def gesicht(app, rgb):
    """Bestes Gesicht -> (Mitte x, Mitte y, Hoehe) in Bildpixeln, sonst None. Groesse zaehlt mit, damit ein Gesicht auf
    einem Foto im Hintergrund nicht gegen das der Figur gewinnt."""
    treffer = app.get(rgb[:, :, ::-1].copy())
    if not treffer:
        return None
    t = max(treffer, key=lambda f: (f.bbox[3] - f.bbox[1]) * float(f.det_score))
    x0, y0, x1, y1 = t.bbox
    return float(x0 + x1) / 2, float(y0 + y1) / 2, float(y1 - y0)


def silhouette(alpha, kopf_h):
    """Rueckansicht ohne Gesicht: Kopf = oberstes Stueck der Silhouette, Groesse aus den Gesichtern der Figur."""
    maske = alpha > 128
    zeilen = np.where(maske.any(axis=1))[0]
    if not len(zeilen):
        return None
    y0 = int(zeilen[0])
    band = maske[y0: y0 + int(kopf_h)]
    spalten = np.where(band.any(axis=0))[0]
    if not len(spalten):
        return None
    return float(spalten[0] + spalten[-1]) / 2, y0 + kopf_h * 0.6, kopf_h


def ausschnitt(fx, fy, fh, w, h):
    """Kreis um das Gesicht, ganz innerhalb des Bildes: Rand des Bildes darf im Kreis nicht als Kante sichtbar sein."""
    d = min(fh / KOPF_ANTEIL, w, h)
    u = min(max(fx, d / 2), w - d / 2)
    v = min(max(fy - HOEHER * d, d / 2), h - d / 2)
    return [round(u / w, 4), round(v / h, 4), round(w / d, 3), round(h / w, 4)]


def bild_laden(pfad):
    with Image.open(pfad) as im:
        rgba = np.asarray(im.convert("RGBA"))
    alpha = rgba[:, :, 3]
    # auf Grau legen, der Detektor kennt keine Transparenz
    a = alpha[:, :, None].astype(np.float32) / 255
    rgb = (rgba[:, :, :3].astype(np.float32) * a + 128 * (1 - a)).astype(np.uint8)
    return rgb, alpha


def sprite_dateien(cfg, modul, pid):
    """{"set1/joy-1.png": Pfad} aller Sprites der Figur"""
    ordner = buehne.figur_ordner(cfg, modul, pid)
    return {"%s/%s" % (si["ordner"] or "_", d): os.path.join(ordner, si["ordner"], d)
            for si in buehne.sets(cfg, modul, pid).values() for ds in si["dateien"].values() for d in ds}


def offen(dateien, alt):
    """Sprites ohne Messung oder seit der letzten Messung geaendert. Alle, wenn die Figur noch gar nicht gemessen ist."""
    if not alt:
        return set(dateien)
    bekannt = set(alt["sprites"]) | set(alt["ohne"])
    return {k for k, p in dateien.items() if k not in bekannt or os.path.getmtime(p) > alt["stand"]}


def figur_messen(app, cfg, modul, pid, alt=None):
    """-> {"std": Eintrag, "sprites": {"set1/joy-1.png": Eintrag}, "ohne": [Sprites ohne Gesicht], "stand": Zeit} oder
    None. Mit alt werden nur die offenen Sprites gemessen."""
    stand = int(time.time())
    alle = sprite_dateien(cfg, modul, pid)
    if not alle:
        return None
    zu_messen = offen(alle, alt)
    gemessen, ohne = {}, []
    for schluessel in sorted(zu_messen):
        rgb, alpha = bild_laden(alle[schluessel])
        h, w = rgb.shape[:2]
        f = gesicht(app, rgb)
        if f:
            gemessen[schluessel] = (f, w, h, None)
        else:
            ohne.append(schluessel)
            gemessen[schluessel] = (None, w, h, alpha if (alpha < 128).mean() > ALPHA_MIN else None)
    hoehen = [g[0][2] / g[2] for g in gemessen.values() if g[0]]     # Gesichtshoehe relativ zur Bildhoehe
    if not hoehen and not alt:
        print("  KEIN Gesicht bei %s" % pid, flush=True)
    kopf = S.median(hoehen) if hoehen else KOPF_ANTEIL / (alt["std"][2] * alt["std"][3]) if alt else 0.14
    # Bekannte Sprites bleiben; was es nicht mehr gibt oder neu gemessen wurde, faellt aus dem alten Stand
    sprites = {k: w for k, w in (alt or {}).get("sprites", {}).items() if k in alle and k not in zu_messen}
    ohne += [k for k in (alt or {}).get("ohne", []) if k in alle and k not in zu_messen]
    for k, (f, w, h, alpha) in gemessen.items():
        if not f and alpha is not None:
            f = silhouette(alpha, kopf * h)
        if f:
            sprites[k] = ausschnitt(f[0], f[1], f[2], w, h)
    if not sprites:
        return None
    std = [round(S.median(e[i] for e in sprites.values()), 4) for i in range(4)]
    return {"std": std, "sprites": sprites, "ohne": sorted(ohne), "stand": stand}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nur", default="", help="Figuren-IDs, mit Komma getrennt")
    ap.add_argument("--neu", action="store_true", help="nur neue und geaenderte Sprites")
    ap.add_argument("--aus", default="", help="anderer Zielpfad, zum Probieren")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    cfg = json.load(open(os.path.join(WURZEL, "eden-config.json"), encoding="utf-8"))
    modul = json.load(open(os.path.join(WURZEL, "module", "eden_rise", "modul.json"), encoding="utf-8"))
    ziel = args.aus or os.path.join(WURZEL, "module", modul["id"], "gesichter.json")
    alt = {}
    if os.path.isfile(ziel):
        with open(ziel, encoding="utf-8") as f:
            alt = json.load(f)
    nur = [x for x in args.nur.split(",") if x]
    if args.neu:
        nur = [p for p in modul["personen"] if offen(sprite_dateien(cfg, modul, p), alt.get(p))]
        if not nur:
            return                  # der Normalfall beim Spielstart: Detektor gar nicht erst laden
    app = detektor()
    figuren = dict(alt) if nur else {}
    for pid in (nur or list(modul["personen"])):
        t = time.time()
        e = figur_messen(app, cfg, modul, pid, alt.get(pid) if args.neu else None)
        if e:
            figuren[pid] = e
            print("%-11s %4d Sprites, %3d ohne Gesicht, %.0fs" % (pid, len(e["sprites"]), len(e["ohne"]), time.time() - t), flush=True)
    with open(ziel + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        json.dump(figuren, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        f.write("\n")
    os.replace(ziel + ".tmp", ziel)
    print("geschrieben:", ziel, len(figuren), "Figuren")


if __name__ == "__main__":
    main()

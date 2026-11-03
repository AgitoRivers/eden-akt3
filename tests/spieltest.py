# -*- coding: utf-8 -*-
r"""Play test: nine fictional review profiles, several seeds, technical and peer-group reports.

  python tests\spieltest.py                  9 review profiles x 3 seeds, technical + peer_group reports
  python tests\spieltest.py --klassisch      original 6 technical player types
  python tests\spieltest.py --profile        list the nine profile ids
  python tests\spieltest.py --seeds 5        more seeds, better numbers
  python tests\spieltest.py --typen chaos,schwach --seeds 1
  python tests\spieltest.py --auswerten      evaluate the last raw runs again (after changing a limit)

The gate (tests/lauf_test.py) stays the quick check after every core change; this one is for milestones. It plays up to the
built end of the calendar, so it grows with the game without changes. Details: docs/wiki/systeme/spieltest.md.
Exit 1 on a crash, a dead end or a run that does not reach the end.
"""
import argparse, concurrent.futures, json, os, shutil, subprocess, sys, tempfile, time

HIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HIER)
sys.path.insert(0, HIER)
import spieltest_auswertung as A  # noqa: E402
import spieltest_peer as P
from spieltest_profile import PROFILE, VERSION

ZIEL = os.path.join(HIER, "spieltest_ergebnis")
TYPEN = ["sammler", "romantiker", "kaempfer", "sparer", "schwach", "chaos"]
ZEITLIMIT = 1800


def ein_lauf(typ, seed, ordner, nr=""):
    pfad = os.path.join(ordner, "%s_%d%s.json" % (typ, seed, nr))
    r = subprocess.run([sys.executable, os.path.join(HIER, "spieltest_bot.py"), typ, str(seed), pfad], cwd=BASE,
                       env=dict(os.environ, PYTHONUTF8="1", PYTHONHASHSEED="0"), capture_output=True, encoding="utf-8",
                       errors="replace", timeout=ZEITLIMIT)
    if not os.path.exists(pfad):                 # the bot itself broke, not the game: this must never read as a clean run
        raise RuntimeError("%s/%d: kein Ergebnis\n%s" % (typ, seed, (r.stdout + r.stderr)[-1500:]))
    print("  " + (r.stdout.strip().splitlines() or ["%s/%s: Ergebnis geschrieben" % (typ, seed)])[-1], flush=True)
    if r.returncode:
        raise RuntimeError("%s/%d: Bot beendet mit Fehler %d\n%s" % (typ, seed, r.returncode, r.stderr[-1500:]))
    return json.load(open(pfad, encoding="utf-8"))


def git(*args):
    return subprocess.run(["git", *args], cwd=BASE, capture_output=True, encoding="utf-8", errors="replace").stdout.strip()


def main():
    global ZIEL
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--typen", help="Kommagetrennte Profil-IDs oder klassische Spielertypen")
    ap.add_argument("--klassisch", action="store_true", help="Die bisherigen sechs technischen Spielertypen")
    ap.add_argument("--profile", action="store_true", help="Die neun Review-Profile auflisten")
    ap.add_argument("--auswerten", action="store_true")
    ap.add_argument("--ziel", default=ZIEL, help="Eigener Ergebnisordner, auch für parallele Sitzungen")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) // 2))
    a = ap.parse_args()
    ZIEL = os.path.abspath(a.ziel)
    if a.profile:
        for pid, p in PROFILE.items():
            print("%-8s %s · %s" % (pid, p["name"], p["medium"]))
        return 0
    if a.seeds < 1 or a.jobs < 1:
        ap.error("--seeds und --jobs müssen mindestens 1 sein")
    if a.klassisch and a.typen:
        ap.error("--klassisch und --typen nicht gemeinsam verwenden")
    typen = a.typen.split(",") if a.typen is not None else TYPEN if a.klassisch else list(PROFILE)
    typen = [t.strip() for t in typen]
    if not typen or any(t not in set(TYPEN) | set(PROFILE) for t in typen) or len(set(typen)) != len(typen):
        ap.error("Unbekannte, leere oder doppelte Typen. Profile: " + ", ".join(PROFILE) + "; klassisch: " + ", ".join(TYPEN))
    os.makedirs(os.path.join(ZIEL, "verlauf"), exist_ok=True)
    roh_datei = os.path.join(ZIEL, "roh.json")
    t0 = time.time()
    if a.auswerten:
        roh = json.load(open(roh_datei, encoding="utf-8"))
    else:
        arbeit = [(t, s) for t in typen for s in range(1, a.seeds + 1)]
        print("Spieltest: %d Läufe, %d parallel" % (len(arbeit), a.jobs), flush=True)
        ordner = tempfile.mkdtemp(prefix="eden_spieltest_roh_")
        try:
            with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
                laeufe = list(ex.map(lambda x: ein_lauf(x[0], x[1], ordner), arbeit))
                # the same run twice: if it ends differently, findings can't be reproduced
                nochmal = ein_lauf(typen[-1], 1, ordner, "_wieder")
        finally:
            shutil.rmtree(ordner, ignore_errors=True)
        erstes = next(r for r in laeufe if r["typ"] == typen[-1] and r["seed"] == 1)
        roh = {"laeufe": laeufe, "wieder": {"typ": typen[-1], "seed": 1, "gleich": erstes["fingerabdruck"] == nochmal["fingerabdruck"]},
               "dauer_s": round(time.time() - t0), "zeit": time.strftime("%d.%m.%Y %H:%M"),
               "commit": git("rev-parse", "--short", "HEAD"), "dirty": bool(git("status", "--porcelain", "--", "kern", "eden.py", "module"))}
        roh["profil_version"] = VERSION
        json.dump(roh, open(roh_datei, "w", encoding="utf-8"), ensure_ascii=False)
    L = roh["laeufe"]
    tage = json.load(open(os.path.join(A.MOD, "modul.json"), encoding="utf-8"))["zeitraster"]["tage"]
    bereiche = A.auswerten(L, tage, roh.get("wieder"))
    alt_datei = os.path.join(ZIEL, "letzter.json")
    alt = json.load(open(alt_datei, encoding="utf-8")) if os.path.exists(alt_datei) and not a.auswerten else None
    A.vergleichen(bereiche, alt)
    meta = {"zeit": roh["zeit"], "laeufe": len(L), "typen": len({r["typ"] for r in L}), "seeds": len({r["seed"] for r in L}), "tage": tage,
            "commit": roh["commit"], "dirty": roh["dirty"], "dauer": "%d min Rechenzeit" % round(roh["dauer_s"] / 60)}
    if alt and not a.auswerten:
        shutil.copy(alt_datei, os.path.join(ZIEL, "verlauf", "%s_%s.json" % (alt["meta"]["zeit"].replace(":", "").replace(" ", "_"), alt["meta"]["commit"])))
    deutsch_voll = sorted({k for r in L for k in r["deutsch"]})
    json.dump({"meta": meta, "bereiche": bereiche, "deutsch_voll": deutsch_voll}, open(alt_datei, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bericht = os.path.join(ZIEL, "bericht.html")
    open(bericht, "w", encoding="utf-8").write(A.seite(meta, bereiche))
    peer = P.auswerten(roh)
    json.dump(peer, open(os.path.join(ZIEL, "peer_group.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(os.path.join(ZIEL, "peer_group.md"), "w", encoding="utf-8").write(P.markdown(peer))
    open(os.path.join(ZIEL, "peer_group.html"), "w", encoding="utf-8").write(P.seite(peer))
    for b in bereiche:
        n = sum(1 for x in b["befunde"] if x["stufe"] in ("rot", "gelb"))
        print("  %-5s %-28s %d offen" % (A.FARBE[b["ampel"]], b["titel"], n))
    print("Bericht:", bericht)
    print("Review-Peer-Group:", os.path.join(ZIEL, "peer_group.html"))
    fest = sum(len(r["abstuerze"]) + len(r["sackgassen"]) + (r["ende"]["status"] != "ende") for r in L)
    return 1 if fest else 0


if __name__ == "__main__":
    sys.exit(main())

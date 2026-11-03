# -*- coding: utf-8 -*-
r"""Ketten-Simulation (26.10.2026): schafft ein echter Spielstand eine Kette von Kaempfen hintereinander?

Der Bot aus tests\lauf_test.py spielt bis zum Morgen von Tag N (echtes Level, Inventar, Chips, Mistral). Dann laeuft
dieser Duc die Kette in der echten Engine (kern\kampf.py): LP bleiben zwischen den Kaempfen (Rast per --rast
der Engine), Erfahrung und Level wachsen unterwegs. Parade-Koennen in drei Stufen, Rast = volle LP vor einem Kampf.
Pflicht vor jeder neuen Gegnerkette (Lehre 26.10.2026: das Kloster war fuer Level-2-Spieler unschaffbar).

    python werkzeuge\kampf_sim_kette.py                         Kloster, Tag 3, 200 Laeufe je Stufe
    python werkzeuge\kampf_sim_kette.py --tag 8 --n 300
    python werkzeuge\kampf_sim_kette.py --rast kloster_3_hund,kloster_7_affe
    python werkzeuge\kampf_sim_kette.py --kette hafen_ratten,hafen_hunde,hafen_keiler

Ziel (Duc 26.10.2026): mittlere Parade >= 60 %, schwache >= 30 %, der Boss ist die Huerde.
"""
import copy, json, os, random, statistics, sys, tempfile

if os.environ.get("PYTHONHASHSEED") != "0":                 # der lauf_test-Bot braucht einen festen Hash-Seed
    import subprocess
    sys.exit(subprocess.call([sys.executable] + sys.argv, env=dict(os.environ, PYTHONHASHSEED="0")))
EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
sys.path.insert(0, os.path.join(EDEN, "tests"))
sys.stdout.reconfigure(encoding="utf-8")
import eden  # noqa: E402
from kern import kampf, llm, stimme  # noqa: E402


def arg(name, std):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else std


KLOSTER = ["kloster_1_ratte", "kloster_1_schlange", "kloster_2_keiler", "kloster_3_hund", "kloster_5_affe",
           "kloster_6_hunde", "kloster_6b_wildschwein_affe", "kloster_7_affe", "kloster_8_loewe"]
KETTE = arg("--kette", ",".join(KLOSTER)).split(",")
RAST = set(x for x in arg("--rast", "").split(",") if x)
TAG, N = int(arg("--tag", "3")), int(arg("--n", "200"))
# Parade-Koennen: Faktor auf die Trefferquote aus der Fenstergroesse (mittel: etwa jede vierte Parade verfehlt)
KOENNEN = (("gut", 2.2), ("mittel", 1.5), ("schwach", 1.0))


def sandbox():
    llm.bereit = lambda: True
    llm.chat = lambda *a, **k: ("She nods.", 0.0)
    llm.json_chat = lambda *a, **k: (None, 0.0)
    stimme.chatterbox = lambda *a, **k: None
    ordner = tempfile.mkdtemp(prefix="eden_sim_")
    echt = json.load(open(eden.CFG_PFAD, encoding="utf-8-sig"))
    eden.CFG_PFAD = os.path.join(ordner, "eden-config.json")
    eden.STAENDE = os.path.join(ordner, "spielstaende")
    os.makedirs(eden.STAENDE)
    json.dump(dict(echt, modul="eden_rise", aktiv=None), open(eden.CFG_PFAD, "w", encoding="utf-8"))


def vorspulen(tag):
    import lauf_test as L
    stimme.chatterbox = lambda *a, **k: None
    prot = {"schritte": [], "erledigt": {}}
    z = eden.aktion("neu", {"modus": "entspannt"})
    while z["status"] != "ende" and not (z["tag"] >= tag and z["status"] == "wahl"):
        a = L.schritt(z, prot)
        if a is None:
            break
        if a[0] != "_tagesarbeit":
            try:
                eden.aktion(*a)
            except ValueError:
                pass
        z = eden.aktiv()
    return z


def parade(k, rng, faktor):
    if k["parade"].get("nur_ausweichen"):
        return "ausweichen" if rng.random() < min(0.9, 0.55 * faktor) else "verfehlt"
    fe = k["parade"]["fenster"]
    p_perf = min(0.6, fe["perf"] / 400 * faktor)
    p_gut = min(0.92 - p_perf, max(0, (fe["gut"] - fe["perf"]) / 300 * faktor))
    r = rng.random()
    return "perfekt" if r < p_perf else "gut" if r < p_perf + p_gut else "verfehlt"


def waehlen(z, modul, rng):
    """Einfacher, vernuenftiger Spieler: heilt bei wenig LP, sucht in Runde 1 die Schwachstelle, nutzt Spezialangriffe."""
    k = z["kampf"]
    sp = k["spieler"]
    items = [x for x in kampf.gegenstaende(z, modul) if not x.get("gesperrt")]
    if sp["lp"] < sp["lp_max"] * 0.35 and items:
        return "gegenstand", items[0]["id"]
    if sp["lp"] < sp["lp_max"] * 0.3 and kampf.pruefen(z, modul, "verteidigen") is None and rng.random() < 0.5:
        return "verteidigen", None
    fs = [f for f in kampf.skills_view(z, k) if not f["gesperrt"]]
    if k["runde"] == 1 and any(f["id"] == "schwachstelle" for f in fs):
        return "faehigkeit", "schwachstelle"
    spezial = [f for f in fs if f.get("art") == "spezial"]
    if spezial:
        return "faehigkeit", max(spezial, key=lambda f: (f.get("schaden") or 0, f["kosten"]))["id"]
    return "angriff", None


def kampf_lauf(z, modul, defs, bid, rng, faktor):
    kampf.starten(z, defs, bid, rng=rng)
    for _ in range(200):
        k = z["kampf"]
        if k.get("ergebnis"):
            break
        if k["phase"] == "parade":
            kampf.parade_aufloesen(z, modul, parade(k, rng, faktor), rng=rng)
            continue
        if kampf.must_skip(k["spieler"]):
            kampf.zug(z, modul, "aussetzen", rng=rng)
            continue
        b, ziel = waehlen(z, modul, rng)
        stehend = [i for i, g in enumerate(k.get("gegner") or []) if not g.get("aus")]   # Gruppe: den Schwaechsten zuerst
        gi = min(stehend, key=lambda i: k["gegner"][i]["lp"]) if len(stehend) > 1 else None
        try:
            kampf.zug(z, modul, b, ziel, rng=rng, **({"gegner": gi} if gi is not None else {}))
        except ValueError:
            kampf.zug(z, modul, "angriff", rng=rng)
    art = (z["kampf"].get("ergebnis") or {}).get("art")
    kampf.schliessen(z)
    return art


def kette(z0, modul, defs, seed, faktor):
    rng = random.Random(seed)
    z = copy.deepcopy(z0)
    z["status"], z["kampf"] = "wahl", None
    for bid in KETTE:
        if bid in RAST:
            kampf.lp_auffuellen(z)
        if kampf_lauf(z, modul, defs, bid, rng, faktor) not in ("ko", "aufgabe", "entkommen"):
            return False, bid, kampf.progress(z)["level"]
    return True, None, kampf.progress(z)["level"]


def main():
    sandbox()
    z0 = vorspulen(TAG)
    modul, defs = eden.modul_laden(), kampf.daten(eden.moddir("eden_rise"))
    c = kampf.progress(z0)
    print("Duc an Tag %d: Level %d, %d LP, Spezial %s, Chips %s" % (z0["tag"], c["level"], kampf.max_lp(c["level"]),
          kampf.known(z0), kampf.chip_pool(z0)["pool"]))
    print("Kette: %s%s" % (" > ".join(b.replace("kloster_", "") for b in KETTE), " · Rast vor " + ", ".join(sorted(RAST)) if RAST else " · ohne Rast"))
    for name, f in KOENNEN:
        er = [kette(z0, modul, defs, 1000 + i, f) for i in range(N)]
        stopp = {}
        for e in er:
            if not e[0]:
                stopp[e[1]] = stopp.get(e[1], 0) + 1
        print("  Parade %-7s ganze Kette %3d %%  Level am Ende %.1f  scheitert an: %s" % (
            name, round(100 * sum(e[0] for e in er) / N), statistics.mean(e[2] for e in er),
            ", ".join("%s %d" % (k, v) for k, v in sorted(stopp.items(), key=lambda x: -x[1])[:3]) or "–"))


if __name__ == "__main__":
    main()

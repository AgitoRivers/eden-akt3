# -*- coding: utf-8 -*-
r"""Kloster-Pruefung (Duc 29.10.2026, Rezensionen/Spieltest): liegt es an den Gegnern oder an der Spielweise?

Echter Stand per Gate-Bot (tests\lauf_test.py) am Morgen von Tag 4..7, dann die Kloster-Hauptkette in der echten Engine
(kern\kampf.py) mit den Rastplaetzen, wie sie im Kapitel liegen (Bachufer, Huette, Kueche, Lager, Schluchtfeuer).
Drei Spielweisen:
  bot        wie der Spieltest-Bot: Heil-Item unter 40 % LP, sonst hoechster Spezialangriff, wenn die Ausdauer reicht,
             sonst Angriff. Kein Verteidigen, keine Schwachstelle, kein Einschuechtern, keine Granaten, keine Rast.
  bot_rast   derselbe Bot, rastet aber an jedem Rastplatz (volle LP).
  gut        gute Spielerin, rastet: Schwachstelle in Runde 1, Einschuechtern ab 55 %, Verteidigen gegen einen
             angekuendigten Spezialangriff, der weh tut, Granaten, Heilen unter 40 %, Spezialangriffe.
Parade-Koennen wie werkzeuge\kampf_sim_kette.py (gut 2.2 / mittel 1.5 = "Normal" / schwach 1.0).

    python werkzeuge\kampf_sim_kloster.py              Tage 4-7, 150 Laeufe je Zelle
    python werkzeuge\kampf_sim_kloster.py --n 300 --tage 4
"""
import collections, copy, os, random, sys

if os.environ.get("PYTHONHASHSEED") != "0":
    import subprocess
    sys.exit(subprocess.call([sys.executable] + sys.argv, env=dict(os.environ, PYTHONHASHSEED="0")))
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
ARGS = list(sys.argv)
sys.argv = [sys.argv[0]]
import kampf_sim_kette as S  # noqa: E402
from kern import kampf  # noqa: E402
import eden  # noqa: E402


def arg(name, std):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else std


N = int(arg("--n", "150"))
TAGE = [int(t) for t in arg("--tage", "4,5,6,7").split(",")]
# Hauptweg wie im Kapitel (ereignisse_kloster.py): "R" = Rastplatz. Ein Rast+Kampf-Frame (Huette, Lager): erst der Kampf.
KETTE = ["kloster_1_ratte", "R", "kloster_2_keiler", "kloster_3_hund", "R", "R", "kloster_5_affe", "kloster_6_hunde",
         "kloster_7_affe", "R", "R", "kloster_8_loewe"]
KAEMPFE = [x for x in KETTE if x != "R"]
SIEG = ("ko", "aufgabe", "entkommen")


def items(z, modul):
    return [x for x in kampf.gegenstaende(z, modul) if not x.get("gesperrt")]


def heil(xs):
    return [x for x in xs if not x["id"].startswith("grenade")]


def bot(z, modul, rng):
    k = z["kampf"]
    sp = k["spieler"]
    xs = heil(items(z, modul))
    if sp["lp"] < sp["lp_max"] * 0.4 and xs:
        return "gegenstand", xs[0]["id"]
    fs = [f for f in kampf.skills_view(z, k) if not f["gesperrt"] and f.get("art") == "spezial"]
    if fs:
        return "faehigkeit", max(fs, key=lambda f: (f.get("stufe") or 0, f["kosten"]))["id"]
    return "angriff", None


GUT = {"schwachstelle": True, "einschuechtern": True, "verteidigen": True}   # Bausteine der guten Spielerin


def gut(z, modul, rng):
    k = z["kampf"]
    stehend = [x for x in k["gegner"] if not x.get("aus")]                  # Gruppe (29.10.2026): nur wer noch steht
    sp, g = k["spieler"], min(stehend, key=lambda x: x["lp"])
    alle = items(z, modul)
    xs = heil(alle)
    if sp["lp"] < sp["lp_max"] * 0.4 and xs:
        return "gegenstand", xs[0]["id"]
    fs = {f["id"]: f for f in kampf.skills_view(z, k) if not f["gesperrt"]}
    if GUT["schwachstelle"] and "schwachstelle" in fs and not g["schwaeche_bekannt"]:
        return "faehigkeit", "schwachstelle"
    flaeche = [f for f in fs.values() if f.get("flaeche")]                # Rudel: erst die Flaeche (Mistral, Lame)
    if len(stehend) > 1 and flaeche:
        return "faehigkeit", max(flaeche, key=lambda f: f["kosten"])["id"]
    droht = [x for x in stehend if x["absicht"] and x["absicht"].startswith("s") and kampf.hurts(kampf._intent(x))]
    if GUT["verteidigen"] and droht and kampf.pruefen(z, modul, "verteidigen") is None:
        antwort = [f for f in fs.values() if f.get("art") == "spezial" and k["specials"][f["id"]].get("answer")]
        if antwort:
            return "faehigkeit", antwort[0]["id"]
        return "verteidigen", None                 # nur gegen den angekuendigten STARKEN Spezialangriff
    gran = [x for x in alle if x["id"].startswith("grenade")]
    if gran and g["lp"] > g["lp_max"] * 0.4:
        return "gegenstand", gran[0]["id"]
    e = fs.get("einschuechtern")
    if GUT["einschuechtern"] and e and len(stehend) == 1 and (e.get("chance") or 0) >= 55 and not any(x.get("befehl") == "faehigkeit" and x.get("ziel") == "einschuechtern"
                                                         for x in k["log"]):
        return "faehigkeit", "einschuechtern"      # einmal je Kampf
    spez = [f for f in fs.values() if f.get("art") == "spezial" and not k["specials"][f["id"]].get("answer")]
    if spez:
        return "faehigkeit", max(spez, key=lambda f: (f.get("stufe") or 0, f["kosten"]))["id"]
    return "angriff", None


def kampf_lauf(z, modul, defs, bid, rng, faktor, wahl):
    kampf.starten(z, defs, bid, rng=rng)
    for _ in range(200):
        k = z["kampf"]
        if k.get("ergebnis"):
            break
        if k["phase"] == "parade":
            kampf.parade_aufloesen(z, modul, S.parade(k, rng, faktor), rng=rng)
            continue
        if kampf.must_skip(k["spieler"]):
            kampf.zug(z, modul, "aussetzen", rng=rng)
            continue
        b, ziel = wahl(z, modul, rng)
        stehend = [i for i, g in enumerate(k.get("gegner") or []) if not g.get("aus")]   # Gruppe: den Schwaechsten zuerst
        gi = min(stehend, key=lambda i: k["gegner"][i]["lp"]) if len(stehend) > 1 else None
        try:
            kampf.zug(z, modul, b, ziel, rng=rng, **({"gegner": gi} if gi is not None else {}))
        except ValueError:
            kampf.zug(z, modul, "angriff", rng=rng)
    art = (z["kampf"].get("ergebnis") or {}).get("art")
    kampf.schliessen(z)
    return art


def kette(z0, modul, defs, seed, faktor, wahl, rast):
    """-> (geschafft, Kampf, an dem es scheiterte, {kampf: gewonnen?})"""
    rng = random.Random(seed)
    z = copy.deepcopy(z0)
    z["status"], z["kampf"] = "wahl", None
    kampf.lp_auffuellen(z)                         # ins Kapitel mit vollen LP
    ergebnis = {}
    for x in KETTE:
        if x == "R":
            if rast:
                kampf.lp_auffuellen(z)
            continue
        ok = kampf_lauf(z, modul, defs, x, rng, faktor, wahl) in SIEG
        ergebnis[x] = ok
        if not ok:
            return False, x, ergebnis
    return True, None, ergebnis


def anlaeufe(z0, modul, defs, seed, faktor, wahl, rast, max_versuche=3):
    """Schnellreise (29.10.2026): nach einer Niederlage wacht Duc mit vollen LP auf dem Schiff auf und reist beim
    naechsten Besuch zum letzten erreichten Rastplatz. -> Anzahl Anlaeufe bis zum Ende der Kette, oder None."""
    rng = random.Random(seed)
    z = copy.deepcopy(z0)
    z["status"], z["kampf"] = "wahl", None
    ab = 0                                        # Index in KETTE, an dem der naechste Anlauf beginnt
    for versuch in range(1, max_versuche + 1):
        kampf.lp_auffuellen(z)
        ok = True
        for i in range(ab, len(KETTE)):
            x = KETTE[i]
            if x == "R":
                ab = i                            # entdeckt: der naechste Anlauf darf hierher reisen
                if rast:
                    kampf.lp_auffuellen(z)
                continue
            if kampf_lauf(z, modul, defs, x, rng, faktor, wahl) not in SIEG:
                ok = False
                break
        if ok:
            return versuch
    return None


SPIELWEISEN = (("bot", bot, False), ("bot_rast", bot, True), ("gut", gut, True))


def main():
    S.sandbox()
    modul, defs = eden.modul_laden(), kampf.daten(eden.moddir("eden_rise"))
    for tag in TAGE:
        z0 = S.vorspulen(tag)
        c = kampf.progress(z0)
        inv = collections.Counter(i for i in z0.get("inventar", []) if i)
        print("\nTag %d: Level %d, %d LP, Waffe %s, Spezial %s, Inventar %s" % (
            tag, c["level"], kampf.max_lp(c["level"]), kampf.aktive_waffe(z0, defs), kampf.known(z0), dict(inv)))
        print("  %-9s %-8s %6s   %s" % ("Spielweise", "Parade", "Kette", "Sieg je Kampf (wer ihn erreicht) · scheitert an"))
        for name, wahl, rast in SPIELWEISEN:
            for kname, f in S.KOENNEN:
                er = [kette(z0, modul, defs, 2000 + i, f, wahl, rast) for i in range(N)]
                erreicht, gewonnen, stopp = collections.Counter(), collections.Counter(), collections.Counter()
                for ok, wo, e in er:
                    for b, w in e.items():
                        erreicht[b] += 1
                        gewonnen[b] += w
                    if not ok:
                        stopp[wo] += 1
                je = " ".join("%s %d" % (b.split("_", 2)[-1][:6], round(100 * gewonnen[b] / erreicht[b])) if erreicht[b]
                              else "%s –" % b.split("_", 2)[-1][:6] for b in KAEMPFE)
                an = [anlaeufe(z0, modul, defs, 3000 + i, f, wahl, rast) for i in range(N)]
                kum = [round(100 * sum(1 for a in an if a and a <= n) / N) for n in (1, 2, 3)]
                print("  %-9s %-8s %5d %%   %s · %s" % (name, kname, round(100 * sum(e[0] for e in er) / N), je,
                      ", ".join("%s %d" % (k.replace("kloster_", ""), v) for k, v in stopp.most_common(3)) or "–"))
                print("  %-9s %-8s          mit Schnellreise geschafft nach 1 / 2 / 3 Anlaeufen: %d / %d / %d %%" % (
                    "", "", kum[0], kum[1], kum[2]))


if __name__ == "__main__":
    main()

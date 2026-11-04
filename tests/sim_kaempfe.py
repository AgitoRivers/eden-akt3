# -*- coding: utf-8 -*-
"""Sweep ueber alle Kampf-Begegnungen (Balancing-Bericht, Cloud-Sitzung 04.11.2026). Kein Gate, nichts wird eingebaut.

    PYTHONHASHSEED=0 python tests/sim_kaempfe.py [laeufe] [--nur tk_]

Je Begegnung aus kaempfe.json plus den Begegnungen der Taktik-Karte (kern/taktik.kampf_defs) spielt ein Bot den echten
Kampf aus kern/kampf.py: ueber Ducs Level (Begegnungs-Level -1, gleich, +1; bei "duc" die Level 3, 6, 9), jede Waffe
(sword, bat, knife, spear, gun), ohne Faehigkeiten und mit einem Pfad (alle Spezialangriffe bis zum Level), und zwei
Paraden-Profile (einfach 35/40/25, geuebt 55/35/10 fuer perfekt/gut/verfehlt). Keine Gegenstaende, keine Chips, Startjacke Terra Scura (jacket_earth).
"entkommen" (der Gegner zieht sich zurueck) zaehlt weder als Sieg noch als Niederlage.
Ausgabe: Siegquote, Niederlagenquote, Runden, LP-Verlust je Begegnung, dazu Ausreisser."""
import copy, json, os, random, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
from kern import kampf, taktik, zustand  # noqa: E402

M = os.path.join(EDEN, "module", "eden_rise")
MODUL = json.load(open(os.path.join(M, "modul.json"), encoding="utf-8"))
WAFFEN = ("sword", "bat", "knife", "spear", "gun")
PFADE = ("K", "M", "W", "L", "H")
PARADE = {"einfach": (.35, .75), "geuebt": (.55, .90)}


class Wurf:
    """Wuerfel aus einem eigenen Random, damit jeder Lauf reproduzierbar ist."""
    def __init__(self, r):
        self.r = r

    def random(self):
        return self.r.random()

    def randint(self, a, b):
        return self.r.randint(a, b)

    def uniform(self, a, b):
        return self.r.uniform(a, b)

    def choice(self, s):
        return self.r.choice(s)


def defs_alle():
    z = {"flags": [], "werte": {}}
    return taktik.kampf_defs(z, M)


def pfad_skills(defs, pfad, level):
    return [sid for sid, s in defs["specials"].items() if s["path"] == pfad and s["tier"] <= level]


def neuer_zustand(defs, level, waffe, skills):
    z = zustand.neu(MODUL)
    zustand.persona_setzen(z, MODUL, copy.deepcopy(MODUL["personas"][0]))
    z["inventar"] = []
    kampf.test_setup(z, defs, level=level, skills=skills, weapon=waffe, armor="jacket_earth")
    return z


def bot_zug(z, k):
    g = kampf.ziel_gegner(k)
    skills = {s["id"]: s for s in kampf.skills_view(z, k)}
    frei = lambda sid: sid in skills and not skills[sid].get("gesperrt")      # noqa: E731
    if g["def"].get("untouchable"):
        return ("faehigkeit", "reden") if frei("reden") else ("verteidigen", None)
    if g["def"].get("weakness") == "charm" and frei("reden"):
        return "faehigkeit", "reden"
    spez = [s for s in skills.values() if s.get("art") == "spezial" and not s.get("gesperrt") and not s.get("hinweis")]
    if spez:
        return "faehigkeit", max(spez, key=lambda s: s.get("stufe", 0))["id"]
    if g["def"].get("weakness") == "courage" and frei("einschuechtern"):
        return "faehigkeit", "einschuechtern"
    return "angriff", None


def ein_kampf(defs, bid, level, waffe, skills, profil, r):
    z = neuer_zustand(defs, level, waffe, skills)
    w = Wurf(r)
    kampf.starten(z, defs, bid, rng=w)
    lp0 = z["kampf"]["spieler"]["lp_max"]
    p_perf, p_gut = PARADE[profil]
    for _ in range(300):
        k = z["kampf"]
        if k.get("ergebnis"):
            art = k["ergebnis"].get("art") if isinstance(k["ergebnis"], dict) else k["ergebnis"]
            return art, k["runde"], 1 - max(0, k["spieler"]["lp"]) / max(1, lp0)
        if k["phase"] == "parade":
            x = r.random()
            erg = "perfekt" if x < p_perf else "gut" if x < p_gut else "verfehlt"
            p = k["parade"] or {}
            if p.get("nur_ausweichen") or p.get("modus") == "ring":
                erg = "ausweichen" if erg != "verfehlt" and p.get("modus") == "ring" else "verfehlt"
            kampf.parade_aufloesen(z, MODUL, erg, rng=w)
            continue
        if kampf.must_skip(k["spieler"]):
            kampf.zug(z, MODUL, "aussetzen", rng=w)
            continue
        befehl, ziel = bot_zug(z, k)
        try:
            kampf.zug(z, MODUL, befehl, ziel, rng=w)
        except ValueError:
            kampf.zug(z, MODUL, "angriff", None, rng=w)
    return "abbruch", 300, 1.0


def level_fuer(enc):
    lv = enc.get("level")
    if lv == "duc":
        return [(d, max(1, min(kampf.LEVEL_MAX, d + enc.get("level_plus", 0)))) for d in (3, 6, 9)]
    lv = int(lv)
    return [(max(1, min(10, lv + d)), lv) for d in (-1, 0, 1)]


def messen(laeufe, nur=None):
    defs = defs_alle()
    aus = {}
    for bid, enc in sorted(defs["encounters"].items()):
        if enc.get("test") or (nur and not bid.startswith(nur)):
            continue
        zeilen = []
        for duc_lv, enc_lv in level_fuer(enc):
            for pfad in (None,) + PFADE:
                skills = pfad_skills(defs, pfad, duc_lv) if pfad else []
                if pfad and not skills:
                    continue
                for waffe in WAFFEN:
                    for profil in PARADE:
                        sieg = runden = verlust = nieder = fehler = 0
                        for i in range(laeufe):
                            r = random.Random(hash((bid, duc_lv, pfad, waffe, profil, i)) & 0xffffffff)
                            try:
                                art, rd, v = ein_kampf(defs, bid, duc_lv, waffe, skills, profil, r)
                            except Exception as ex:                       # noqa: BLE001 - Fehler sind ein Befund
                                art, rd, v = "fehler:%s" % type(ex).__name__, 0, 1.0
                            sieg += art in ("ko", "aufgabe")
                            nieder += art == "niederlage"
                            fehler += art.startswith("fehler") or art == "abbruch"
                            runden += rd
                            verlust += v
                        zeilen.append({"duc": duc_lv, "gegner": enc_lv, "pfad": pfad or "-", "waffe": waffe, "profil": profil,
                                       "sieg": sieg / laeufe, "niederlage": nieder / laeufe, "fehler": fehler, "runden": runden / laeufe, "verlust": verlust / laeufe})
        aus[bid] = {"gegner": enc.get("enemies") or [enc.get("enemy")], "zeilen": zeilen}
        print(bid, flush=True, file=sys.stderr)
    return aus


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 6
    nur = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None
    erg = messen(n, nur)
    json.dump(erg, sys.stdout, ensure_ascii=False)

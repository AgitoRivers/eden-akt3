# -*- coding: utf-8 -*-
"""Crew-Moral als Wochenstimmung (27.10.2026, Duc: Variante C).

Skala -5..+5, Start 0, fuenf Stufen (Buzzing/Good/Calm/Tense/Mutinous). Regeln und Texte stehen im Modul
(modul["moral"], Builder basis_eden_rise.py); fehlt der Block, gilt die alte Moral (einfache Werte, kein Verfall).

  Momente (Events, Bordrat, Missionen, Anhoerung, Ermittlung) zaehlen doppelt - in beide Richtungen.
  Alltag (Kochen, Snacks, Gesten, Szenen-Reaktion "crew up", Bordregeln) gibt +1, aber nur bis "alltag_bis" (+2).
  Genau (Gegenstaende zum Benutzen, Strommangel, die vier Tiefpunkte unten) zaehlt, wie es dasteht.
  Jede Nacht sinkt die Moral um 1, solange sie ueber 0 liegt.

Tiefpunkte im Code (keine JSON-Handarbeit): dritter Weg im Bordrat Erfolg +2 / Fehlschlag -2, gebrochenes Versprechen
-2, Patzer (natuerliche 1) vor der Crew -1, Crew-Mission endgueltig verpatzt -1.

Wirkpunkte: Wuerfel (+1 bei Buzzing, -1 ab "tense_ab"), Ton der Zufalls-Events, Fruehstueckszeile, ein Satz im
Szenen-Prompt, Bordrat (dritter Weg mit Vorteil / SG +2), Grundgefuehl der Crew-Sprites, Megans Geduld in der
Anhoerung, Geschenke der Crew beim Fruehstueck (Buzzing).

Folgen setzen die Art mit "moral_art": "alltag" | "genau" (ohne = Moment).
"""
import random

from . import rollen

KEY = "moral"


def cfg(modul):
    return modul.get("moral") or {}


def aktiv(modul):
    return bool(cfg(modul).get("stufen"))


def wert(z):
    return z["werte"].get(KEY, 0)


def stufe(z, modul):
    """-> Stufen-ID ("buzzing", "good", "calm", "tense", "mutinous") oder None ohne Moral-Block."""
    if not aktiv(modul):
        return None
    w = wert(z)
    for s in cfg(modul)["stufen"]:                    # absteigend nach "ab"
        if w >= s["ab"]:
            return s["id"]
    return cfg(modul)["stufen"][-1]["id"]


def _stufe_def(z, modul):
    sid = stufe(z, modul)
    return next((s for s in cfg(modul)["stufen"] if s["id"] == sid), {}) if sid else {}


def ansicht(z, modul):
    """Wort + Gesicht fuer die Leiste (die Zahl steht nur im Tooltip)."""
    s = _stufe_def(z, modul)
    return {"stufe": s.get("id"), "wort": s.get("wort"), "gesicht": s.get("gesicht")} if s else None


def delta(z, modul, f):
    """Wirksame Aenderung einer Moral-Folge {"wert": "moral", "delta": n, "moral_art": ...}."""
    d = int(f.get("delta", 0))
    if not aktiv(modul):
        return max(-2, min(2, d))
    c, art = cfg(modul), f.get("moral_art", "moment")
    if art == "genau":
        return d
    if art == "alltag":
        if d <= 0:
            return max(-1, d)
        return max(0, min(1, c.get("alltag_bis", 2) - wert(z)))
    return max(-2, min(2, d)) * c.get("faktor", 2)


def folge(d, art=None):
    f = {"wert": KEY, "delta": d}
    if art:
        f["moral_art"] = art
    return f


def als(folgen, art):
    """Kopie der Folgen, in der jede Moral-Folge die Art bekommt (z. B. Bordregeln und Snacks = Alltag)."""
    return [dict(f, moral_art=art) if f.get("wert") == KEY and "moral_art" not in f else f for f in folgen or []]


# ------------------------------------------------------------------ Crew
def crew(modul):
    return rollen.liste(modul, "crew") + [p for p in rollen.liste(modul, "isst_mit") if p not in rollen.liste(modul, "crew")]


def crew_dabei(modul, pids):
    c = crew(modul)
    return [p for p in pids or [] if p in c]


def _vorname(modul, pid):
    return (modul["personen"].get(pid) or {}).get("name", pid).split()[0]


# ------------------------------------------------------------------ Wuerfel
def wuerfel_bonus(z, modul, pids):
    """[(label, wert)] fuer eine Probe mit Crew dabei: +1 bei Buzzing, -1 ab der Stufe "tense_ab"."""
    da = crew_dabei(modul, pids)
    if not aktiv(modul) or not da:
        return []
    c, w = cfg(modul), wert(z)
    if stufe(z, modul) == "buzzing":
        beste = max(da, key=lambda p: (z["werte"].get("vertrauen." + p, 0), -da.index(p)))
        return [(c["wuerfel"]["plus"] % _vorname(modul, beste), 1)]
    if w <= c.get("tense_ab", -2):
        return [(c["wuerfel"]["minus"], -1)]
    return []


def nach_probe(z, modul, probe, pids):
    """Patzer vor der Crew: -1 (genau). -> Folgen fuer folgen_anwenden."""
    if aktiv(modul) and probe and probe.get("ergebnis") == "patzer" and crew_dabei(modul, pids):
        return [folge(-1, "genau")]
    return []


# ------------------------------------------------------------------ Events
def ton_gewicht(z, modul, ton):
    return (cfg(modul).get("toene", {}).get(stufe(z, modul)) or {}).get(ton, 1.0) if aktiv(modul) else 1.0


def gewichtet(z, modul, rng, kand, faktor=None):
    """Zufalls-Event nach Ton und Stimmung ziehen (ohne Moral-Block: gleichverteilt wie bisher).
    faktor: Gewicht je Event obendrauf (Flirts der Frauen, um die Duc sich kuemmert)."""
    if not aktiv(modul) and not faktor:
        return rng.choice(kand)
    g = [(ton_gewicht(z, modul, ev.get("ton")) if aktiv(modul) else 1) * (faktor(ev) if faktor else 1) for ev in kand]
    x = rng.random() * sum(g)
    for ev, w in zip(kand, g):
        x -= w
        if x <= 0:
            return ev
    return kand[-1]


def dritter_weg(z, modul):
    """Bordrat: {"vorteil": bool, "sg": Aufschlag}."""
    if not aktiv(modul):
        return {"vorteil": False, "sg": 0}
    s = stufe(z, modul)
    return {"vorteil": s == "buzzing", "sg": 2 if s in ("tense", "mutinous") else 0}


# ------------------------------------------------------------------ Morgen
def morgen(z, modul):
    """Nach dem Tageswechsel: Verfall ueber Nacht, Fruehstueckszeile, vielleicht ein Geschenk. -> Zeilen."""
    from . import handel, zustand
    kater = handel.kater(z, modul)                     # Gras-Kuchen vom Vortag (gilt auch ohne Moral)
    if not aktiv(modul):
        return kater
    c, zeilen = cfg(modul), list(kater)
    if wert(z) > 0:
        zeilen += zustand.folgen_anwenden(z, modul, [folge(-1, "genau")])
    a = ansicht(z, modul)
    texte = c.get("fruehstueck", {}).get(a["stufe"]) or []
    if texte:
        zeilen.append("%s %s · %s" % (a["gesicht"], a["wort"], texte[z["tag"] % len(texte)]))
    zeilen += geschenk(z, modul)
    if not any(str(x).startswith("🎁") for x in zeilen):
        zeilen += freundes_geschenk(z, modul)
    return zeilen


def freundes_geschenk(z, modul):
    """Unabhaengig von der Moral: eine Figur ab "ab_vertrauen" steckt Duc mit "chance" etwas zu (modul
    ["morgen_geschenke"]: Lolas Space Cake ab 4, Energy Bar ab 3, ein Snack mit Tipp ab 2). Pause je Eintrag und je
    Figur; der erste Treffer in der Liste gewinnt."""
    from . import vorlieben, zustand
    mg = modul.get("morgen_geschenke") or {}
    zuletzt = z.get("morgen_geschenk_tag") or {}
    for g in mg.get("liste") or []:
        pid = g["von"]
        p = modul["personen"].get(pid)
        schluessel = g.get("item") or "sortiment:" + g.get("sortiment", "")
        if not p or z["tag"] >= p.get("von_bord_ab_tag", 99):
            continue
        if z["werte"].get("vertrauen." + pid, 0) < g.get("ab_vertrauen", 3):
            continue
        if z["tag"] - zuletzt.get(pid, -99) < mg.get("pause_person", 2) or z["tag"] - zuletzt.get(schluessel, -99) < g.get("pause", 2):
            continue
        rng = random.Random("%s-%d-morgen-geschenk-%s" % (z["id"], z["tag"], schluessel))
        if rng.random() >= g.get("chance", 0.35):
            continue
        item, fuer = (g["item"], None) if g.get("item") else _aus_sortiment(z, modul, pid, g.get("sortiment"), rng)
        if item not in modul.get("items", {}) or item in z.get("inventar", []) or not _platz(z, modul):
            continue                                     # schon in der Tasche oder kein Platz: naechster Eintrag
        z.setdefault("morgen_geschenk_tag", {}).update({pid: z["tag"], schluessel: z["tag"]})
        name = vorlieben._name(modul, fuer) if fuer else ""
        text = g["texte"][z["tag"] % len(g["texte"])].format(von=_vorname(modul, pid), snack=modul["items"][item]["label"],
                                                              fuer=name)
        zeilen = ["🎁 " + text] + zustand.folgen_anwenden(z, modul, [{"item": item}])
        if fuer:
            zeilen += vorlieben.aus_folge(z, modul, {"vorliebe": {"figur": fuer, "item": item, "reaktion": "mag",
                                                                  "text": "%s told you: %s loves these." % (_vorname(modul, pid), name)}})
        return zeilen
    return []


def _platz(z, modul):
    from . import zustand
    return zustand.belegt(z, modul) < zustand.inventar_plaetze(z, modul)


def _aus_sortiment(z, modul, pid, art, rng):
    """(item, fuer): ein Gegenstand der Art aus dem Laden von pid (ohne Vertrauens-Sperre) und wer ihn liebt -
    bevorzugt eine Vorliebe, die Duc noch nicht kennt. (None, None), wenn es nichts gibt."""
    from . import vorlieben
    kand = [(iid, f) for iid, it in sorted(modul.get("items", {}).items())
            if it.get("art") == art and pid in (it.get("wo") or []) and not it.get("ab") and iid not in z.get("inventar", [])
            for f, w in sorted((it.get("geschenk") or {}).items()) if w >= 2 and f != pid and f in modul["personen"]]
    if not kand:
        return None, None
    neu = [k for k in kand if not vorlieben.bekannt(z, k[1], k[0])] or kand
    return rng.choice(neu)


def geschenk(z, modul):
    """Buzzing: mit "geschenk_chance" ein Kampf-Verbrauchsgegenstand von der Crew (hoechstens einer am Tag)."""
    from . import zustand
    c = cfg(modul)
    if stufe(z, modul) != "buzzing" or z.get("moral_geschenk_tag") == z["tag"]:
        return []
    rng = random.Random("%s-%d-moral-geschenk" % (z["id"], z["tag"]))
    if rng.random() >= c.get("geschenk_chance", 0.7):
        return []
    weg = set(z.get("moral_geschenke") or [])
    tabelle = [g for g in c.get("geschenke", []) if g["item"] in modul.get("items", {})
               and g["von"] in modul["personen"] and z["tag"] < modul["personen"][g["von"]].get("von_bord_ab_tag", 99)]
    if not tabelle:
        return []
    tabelle = [g for g in tabelle if g["item"] not in z.get("inventar", [])]      # schon in der Tasche: geht sonst verloren
    if not tabelle or not _platz(z, modul):
        return []
    frisch = [g for g in tabelle if g["item"] not in weg] or tabelle
    g = rng.choice(frisch)
    z["moral_geschenk_tag"] = z["tag"]
    z.setdefault("moral_geschenke", []).append(g["item"])
    zeilen = ["🎁 " + g["text"] % _vorname(modul, g["von"])]
    return zeilen + zustand.folgen_anwenden(z, modul, [{"item": g["item"]}])


# ------------------------------------------------------------------ Szene, Sprites, Anhoerung, Abschluss
def szene_hinweis(z, modul):
    """Ein Satz Crew-Stimmung fuer den Szenen-Prompt (nur fuer Crew-Figuren) - oder None."""
    return cfg(modul).get("prompt", {}).get(stufe(z, modul)) if aktiv(modul) else None


def grund_gefuehl(z, modul, pid, standard="neutral"):
    """Gefuehl eines Crew-Sprites, bevor sie etwas sagt: freudig bei Buzzing, genervt ab Tense."""
    if not aktiv(modul) or pid not in crew(modul):
        return standard
    return cfg(modul).get("gefuehl", {}).get(stufe(z, modul), standard)


def geduld(z, modul):
    """Megans Geduld in der Anhoerung: (+1/-1, Grund) oder None."""
    s = stufe(z, modul)
    if s == "buzzing":
        return 1, cfg(modul)["anhoerung"]["plus"]
    if s in ("tense", "mutinous"):
        return -1, cfg(modul)["anhoerung"]["minus"]
    return None


def alte_skala(z, modul, standard=3):
    """Fuer die Abschluss-Rechnung, die mit der alten Skala 0..5 zaehlt: 3 + Moral/2."""
    if not aktiv(modul):
        return z["werte"].get(KEY, standard)
    return int(3 + wert(z) / 2)


def meuterei(z, modul):
    """Schiffsverlust bei Brand: alte Regel Moral <= 1, neu ab Mutinous."""
    if not aktiv(modul):
        return z["werte"].get(KEY, 3) <= 1
    return stufe(z, modul) == "mutinous"

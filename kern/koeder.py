# -*- coding: utf-8 -*-
"""Koeder bei Petru (Duc 30.10.2026): dauerhaft, drei Stufen, je Stufe zwei Looks mit gleicher Wirkung.

  * Gebaut wird bei Petru (Reiter "Baits"): Geld + Rohstoffe (Cork, Timber, Iron und die Moewenfeder), alles oder nichts.
    Der Koeder wird nicht verbraucht. Sein Look (1 von 2) steht beim Bauen fest und laesst sich jederzeit umschalten.
  * Es gilt der BESTE gebaute Koeder. Seine Wirkung steckt in kern/angeln.py auswerfen: breitere goldene Zone, Gewicht der
    selteneren Fischstufen, kuerzere Wartezeit bis zum Biss. Sein Look ersetzt den gezeichneten Schwimmer im Minispiel.
  * Stand: z["kueche"]["koeder"] = {koeder_id: look_id}. Daten: kuechen.json "koeder" (kochen_daten.py KOEDER).
  * Spielstaende ohne Koeder bekommen keinen neuen Schluessel; ohne Koeder aendert sich am Angeln nichts.
  * Ohne gebauten Koeder liegt der Standard-Schwimmer im Wasser (Duc 03.11.2026): Flaschenkorken mit Moewenfeder, ohne Bonus."""
from . import abbau, kuechen

NEUTRAL = {"zone": 0.0, "selten": {"2": 0, "3": 0}, "warten": 1.0}
STANDARD = {"id": "bottle_cork", "label": "Bottle Cork", "stufe": 0, "look": "koeder_0_4"}   # Duc 03.11.2026, ersetzt den CSS-Schwimmer


def _d(modul):
    return kuechen.daten(modul).get("koeder") or {}


def besitz(z):
    """{koeder_id: look_id} - nur lesen."""
    return dict((z.get("kueche") or {}).get("koeder") or {})


def aktiv(z, modul):
    """Der beste gebaute Koeder -> (id, Daten, look) oder None."""
    d, b = _d(modul), besitz(z)
    best = max((k for k in b if k in d), key=lambda k: d[k]["stufe"], default=None)
    return (best, d[best], b[best]) if best else None


def wirkung(z, modul):
    a = aktiv(z, modul)
    return {"zone": a[1]["zone"], "selten": a[1]["selten"], "warten": a[1]["warten"]} if a else NEUTRAL


def bild(look):
    return "/farm/koeder/%s.png" % look


def aktiv_ansicht(z, modul):
    """Fuer das Angel-Minispiel: welcher Schwimmer liegt im Wasser? -> {id, label, stufe, bild}; ohne Koeder der STANDARD."""
    a = aktiv(z, modul)
    if not a:
        return {"id": STANDARD["id"], "label": STANDARD["label"], "stufe": 0, "bild": bild(STANDARD["look"])}
    return {"id": a[0], "label": a[1]["label"], "stufe": a[1]["stufe"], "bild": bild(a[2])}


def _wirkung_text(k):
    t = ["Golden band +%d %%" % round(k["zone"] * 100)]
    if any(k["selten"].values()):
        t.append("Better fish bite more often")
    if k["warten"] < 1:
        t.append("Bites come %d %% sooner" % round((1 - k["warten"]) * 100))
    return t


def ansicht(z, modul):
    """Reiter "Baits" in Petrus Werkstatt -> Liste nach Stufe, oder None solange die Werkstatt zu ist."""
    d = _d(modul)
    if not d or not abbau.petru_offen(z, modul):
        return None
    roh, b = kuechen.rohstoffe(z), besitz(z)
    best = (aktiv(z, modul) or (None,))[0]
    out = []
    for kid, k in sorted(d.items(), key=lambda x: x[1]["stufe"]):
        rs = [{"id": r, "label": kuechen.daten(modul)["rohstoffe"][r]["label"], "n": n, "hast": roh.get(r, 0)}
              for r, n in k["rohstoffe"].items()]
        out.append({"id": kid, "label": k["label"], "stufe": k["stufe"], "text": k["text"], "geld": k["geld"], "rohstoffe": rs,
                    "gebaut": kid in b, "look": b.get(kid), "aktiv": kid == best, "wirkung": _wirkung_text(k),
                    "looks": [dict(lk, bild=bild(lk["id"])) for lk in k["looks"]],
                    "geht": kid not in b and z["konto"] >= k["geld"] and all(r["hast"] >= r["n"] for r in rs)})
    return out


def _koeder(z, modul):
    if not abbau.petru_offen(z, modul):
        raise ValueError("Petru's workshop isn't open yet.")
    return _d(modul)


def _look(k, look):
    ids = [lk["id"] for lk in k["looks"]]
    if look is None:
        return ids[0]
    if look not in ids:
        raise ValueError("That look doesn't belong to this bait.")
    return look


def bauen(z, modul, kid, look=None):
    """Einen Koeder bei Petru bauen: Geld und Rohstoffe, alles oder nichts. -> (Zeilen, Zeilen-Gruppe fuer Petrus Satz)"""
    d = _koeder(z, modul)
    k = d.get(kid)
    if not k:
        raise ValueError("That bait doesn't exist.")
    if kid in besitz(z):
        raise ValueError("You already have that one.")
    look = _look(k, look)
    if z["konto"] < k["geld"]:
        raise ValueError("You don't have enough money.")
    kuechen.rohstoffe_nehmen(z, k["rohstoffe"])        # wirft bei zu wenig Material, bevor Geld abgeht
    if k["geld"]:
        z["konto"] -= k["geld"]
        z.setdefault("buchungen", []).append({"text": "Petru: %s" % k["label"], "betrag": -k["geld"], "tag": z["tag"]})
    kuechen.kueche(z).setdefault("koeder", {})[kid] = look
    return (["%s: Petru ties it up and hands it over. It stays yours, no matter how many fish it fools." % k["label"]],
            "kalt_kauf" if abbau.petru_kalt(z) else "kauf_koeder_%d" % k["stufe"])


def look_waehlen(z, modul, kid, look):
    """Den Look eines gebauten Koeders umschalten (jederzeit, kostenlos). -> Zeilen"""
    d = _koeder(z, modul)
    k = d.get(kid)
    if not k or kid not in besitz(z):
        raise ValueError("You haven't built that bait yet.")
    kuechen.kueche(z)["koeder"][kid] = _look(k, look)
    return []

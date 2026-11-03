# -*- coding: utf-8 -*-
"""Bibis Tierstation "Mochi's" (Duc 31.10.2026, Wiki systeme/tierstation.md). Pokemon und Monster Hunter, aber ohne Fangen:

  * Spur (eine Phase): Das Halsband macht das Tier verrueckt. Duc kaempft es muede und wirft Rosis Schlafgranate, Bibi gibt zwei je Spur (Duc 01.11.2026).
    Unter 10 % LP wirkt sie immer, darueber immer seltener (kern/kampf.schlaf_chance). Schlaegt er das fast besiegte Tier weiter, ist es weg.
  * Lieblingsfutter aus der Speisekammer: als Koeder (es frisst erst, eine Runde Vorsprung) und beim Aufpaeppeln (einen Tag schneller).
  * Gesund: Es bleibt bei Bibi, ohne Halsband. Duc kann es besuchen, es findet morgens etwas, es kann als Begleiter mit. Im Epilog kommen alle frei (Duc 01.11.2026).
  * Begleiter: genau einer, nur auf Expeditionen. Nutzt den Beistand aus kern/kampf.py. Bindung 1-3 ueber gemeinsame Kaempfe.
  * Field Book: je Tier vier Seiten-Zeilen, Mochi hat eine eigene Seite ohne Spur.

Keine Pflege-Pflicht: Nichts verfaellt, kein Tier stirbt. Stand: z["mochis"] (erst beim ersten Besuch), Spielstaende ohne Station bleiben unberuehrt."""
import random

from . import expedition, handel, handy, kuechen, regeln, zustand


FANG_SET = {"bibi": "Mochis", "danzel": "danzel_B"}


def _d(modul):
    return modul.get("mochis") or {}


def _s(z):
    return z.setdefault("mochis", {"tiere": {}, "begleiter": None, "halsbaender": 0, "versuch": {}, "koeder": None, "fund_tag": {}})


def _lesen(z):
    return z.get("mochis") or {}


def offen(z, modul):
    l = (modul.get("laeden") or {}).get("mochis")
    return bool(l and _d(modul) and handel.laden_offen(z, l))


def bild(z, modul):
    """Hintergrund der Station: das Anfangsbild, ab ausbau_ab geretteten Tieren der Ausbau (Duc 01.11.2026)."""
    d = _d(modul)
    return d["bild_voll"] if len(_lesen(z).get("tiere") or {}) >= d["ausbau_ab"] else d["bild_anfang"]


def beweis_stand(z):
    """Was die Kommission an Halsbaendern vorfindet: "keiner", "fraglich" (Siegel gebrochen) oder "sicher" (in Elsas Safe). Fuer die Anklage in Akt 3."""
    if "mo_ark_beweis" not in z["flags"]:
        return "keiner"
    return "sicher" if "mo_beweis_bei_elsa" in z["flags"] else "fraglich"


def _wieder_da(z, modul, t, x):
    """Ab WIEDER_TAGE nach dem ersten Fang hoert Bibi von einem zweiten Tier derselben Art. Mehr gibt es nicht, und manche bleiben allein (Duc 01.11.2026)."""
    return not t.get("allein") and x.get("anzahl", 1) < 2 and z["tag"] >= x.get("zuletzt", x["seit"]) + _d(modul)["wieder_tage"]


def _fakten(t, x):
    """Fakten im Field Book und was noch fehlt: Der zweite kommt mit dem zweiten Tier, bei Einzelgaengern mit dem ersten Besuch."""
    zweiter = x.get("anzahl", 1) >= 2 or (t.get("allein") and x.get("besuche", 0) > 0)
    return [t["fakt"]] + ([t["fakt2"]] if zweiter else []), None if zweiter else "besuch" if t.get("allein") else "zweites"


def _spur_da(z, t):
    return regeln.gilt({"flag_seit": ["rt_ende_tag", t["ab"]]}, z) and (not t.get("wenn") or regeln.gilt(t["wenn"], z))


def _stufe(d, kaempfe):
    return 3 if kaempfe >= d["stufe_ab"]["3"] else 2 if kaempfe >= d["stufe_ab"]["2"] else 1


def _futter_key(z, t):
    """Der billigste Vorrat, den dieses Tier liebt -> Vorrats-Schluessel oder None."""
    v = (z.get("kueche") or {}).get("vorrat") or {}
    treffer = [k for k in sorted(v, key=lambda k: kuechen.zerlegen(k)[1]) if kuechen.zerlegen(k)[0] in t["futter"] and v[k] > 0]
    return treffer[0] if treffer else None


def _futter_label(modul, key):
    return kuechen.daten(modul)["zutaten"][kuechen.zerlegen(key)[0]]["label"]


def _futter_bekannt(z, tid):
    s = _lesen(z)
    return tid in (s.get("versuch") or {}) or tid in (s.get("tiere") or {})


def _status(z, tid, t):
    """nicht_da / spur / pflege / heilt / bleibt"""
    s = _lesen(z)
    x = (s.get("tiere") or {}).get(tid)
    if not x:
        return "spur" if _spur_da(z, t) else "nicht_da"
    if x.get("gesund_ab") is None:
        return "pflege"
    return "bleibt" if z["tag"] >= x["gesund_ab"] else "heilt"


def _selfie(tid, t):
    """Bibis Selfie zum Tier als Mini-Szene (Duc 02.11.2026): Bild A, dann B, je mit Polaroid-Titel; text = ihre Nachricht, log = Field-Book-Notiz."""
    titel = t.get("selfie_titel") or ["", ""]
    return {"bilder": [{"bild": "/selfie/bibi_fang_%s_%s.webp" % (tid, teil), "titel": titel[i]} for i, teil in enumerate("ab")],
            "text": t["selfie"], "log": t.get("log", "")}


def _duc_karte(z, modul):
    """Ducs Seite (Duc 02.11.2026): ab Begehren 4 ein Umriss wie ein Mensch, nie kommentiert; mit dem Gestaendnis (bibi_seite) die ganze Seite."""
    s = _d(modul).get("duc_seite")
    if not s or z["werte"].get("begehren.bibi", 0) < 4:
        return None
    karte = {"id": "duc", "bild": s["sprite"], "anzahl": 1}
    if "bibi_seite" not in z["flags"]:
        return dict(karte, status="nicht_da", name="?", art="")
    return dict(karte, status="duc", name=s["name"], gestrichen=s["gestrichen"], art=s["art"], seiten=s["seiten"])


def ansicht(z, modul):
    """Reiter Field Book -> Dict oder None, solange die Station zu ist. Nur lesen."""
    if not offen(z, modul):
        return None
    d, s = _d(modul), _lesen(z)
    karten = []
    for tid, t in d["tiere"].items():
        st, x = _status(z, tid, t), (s.get("tiere") or {}).get(tid) or {}
        # Halsband nur im Kampf-Sprite: Wer an der Station lebt, zeigt sich ohne (<Sprite>Frei, Duc 01.11.2026)
        karte = {"id": tid, "status": st, "name": t["name"] if x else t["vorher"], "art": t["art"], "bild": "/kampfbild/%s%s/idle.webp" % (t["sprite"], "Frei" if x else "")}
        if st == "nicht_da":
            karte.update(name="?", art="Bibi has heard nothing yet.")
            karten.append(karte)
            continue
        seiten = [t["gewicht"]] if x or tid in (s.get("versuch") or {}) else []
        if x:                                              # Eintrag im Field Book und im Codex: Fakten nach Zahl der Faenge
            fakten, fehlt = _fakten(t, x)
            karte.update(anzahl=x.get("anzahl", 1), fakten=fakten, fakt_fehlt=fehlt, szene=t["szene"], seit=x["seit"])
            if t.get("selfie"):
                karte["selfie"] = _selfie(tid, t)
        if x:
            seiten.append(t["narbe"])
        if x.get("gefuettert"):
            seiten.append(t["gefunden"])
        karte["seiten"] = seiten
        if _futter_bekannt(z, tid):
            karte["futter"] = [kuechen.daten(modul)["zutaten"][f]["label"] for f in t["futter"]]
        key = _futter_key(z, t)
        if st == "spur":
            heute = (s.get("versuch") or {}).get(tid) == z["tag"]
            karte["spur"] = {"heute_schon": heute, "geht": not heute and z["status"] == "wahl"}
            if key and _futter_bekannt(z, tid):
                karte["spur"]["koeder"] = _futter_label(modul, key)
        if st == "pflege":
            karte["fuettern"] = {"lieb": _futter_label(modul, key) if key else None, "geld": d["futter_geld"], "geht_geld": z["konto"] >= d["futter_geld"]}
        if st == "heilt":
            karte["gesund_in"] = x["gesund_ab"] - z["tag"]
        if st == "bleibt":
            k = x.get("kaempfe", 0)
            karte.update(stufe=_stufe(d, k), kaempfe=k, begleiter=s.get("begleiter") == tid)
            if _wieder_da(z, modul, t, x):
                heute = (s.get("versuch") or {}).get(tid) == z["tag"]
                karte["wieder"] = {"heute_schon": heute, "geht": not heute and z["status"] == "wahl"}
                if key and not heute:
                    karte["wieder"]["koeder"] = _futter_label(modul, key)
        karten.append(karte)
    for sid, m in d["seiten"].items():                     # Seiten ohne Spur: Mochi, Old Grey, der Black Beast
        zeile = next((t for flag, t in m["zeilen"].items() if flag in z["flags"]), None)
        if zeile:
            sprite = m["sprite_frei"] if any(f in z["flags"] for f in m.get("frei", [])) else m["sprite"]
            karten.append({"id": sid, "status": "mochi", "name": m["name"], "art": m["art"], "bild": "/kampfbild/%s/idle.webp" % sprite, "seiten": [m["gewicht"], zeile]})
    duc = _duc_karte(z, modul)
    if duc:
        karten.append(duc)
    return {"karten": karten, "gerettet": len(s.get("tiere") or {}), "gesamt": len(d["tiere"]), "funde": len(_fund_offen(z, modul)),
            "halsbaender": s.get("halsbaender", 0), "begleiter": d["tiere"][s["begleiter"]]["name"] if s.get("begleiter") else None}


# ------------------------------------------------------------------ Spur
def spur_start(z, modul, tid, mit_koeder):
    """Spur aufnehmen -> erster Frame der Ortskette. Der Aufrufer prueft Status und Phase, die Kette kostet die Phase."""
    d = _d(modul)
    t = d["tiere"].get(tid)
    if not offen(z, modul) or not t:
        raise ValueError("There's no trail like that.")
    status, s = _status(z, tid, t), _s(z)
    frame = "mo_%s_spur" % tid
    if status == "bleibt" and _wieder_da(z, modul, t, s["tiere"][tid]):
        frame = "mo_%s_wieder" % tid
    elif status != "spur":
        raise ValueError("There's no trail to follow right now.")
    if s["versuch"].get(tid) == z["tag"]:
        raise ValueError("That trail has gone cold today. Try again tomorrow.")
    s["koeder"] = None
    if mit_koeder:
        key = _futter_key(z, t)
        if not key:
            raise ValueError("You don't have anything it likes.")
        kuechen.vorrat_nehmen(z, key)
        s["koeder"] = tid
        z["meldungen"].append({"titel": "Mochi's", "kurz": "You bring %s along." % _futter_label(modul, key), "folgen": []})
    s["versuch"][tid] = z["tag"]
    if "mo_fang_heute" in z["flags"]:                      # sagt der Kette nach dem Kampf, ob es geklappt hat
        z["flags"].remove("mo_fang_heute")
    return frame


def _tier_von_kampf(modul, bid):
    tid = (bid or "")[len("mochis_"):] if (bid or "").startswith("mochis_") else None
    return tid if tid in _d(modul).get("tiere", {}) else None


def kampf_vorbereiten(z, modul):
    """Direkt nach kampf.starten: Schlafgranaten und Koeder in einer Rettung, sonst der Begleiter auf einer Expedition."""
    k, d = z["kampf"], _d(modul)
    if not d:
        return
    if _tier_von_kampf(modul, k.get("definition")):
        z.setdefault("inventar", []).extend([d["granate"]] * d["granaten"])   # bewusst an der Taschen-Grenze vorbei: Sie gehen nach dem Kampf zurueck
        if (z.get("mochis") or {}).get("koeder"):
            for g in k["gegner"]:
                g["states"]["skip"] = g["states"].get("skip", 0) + d["koeder_runden"]
            z["mochis"]["koeder"] = None
        return
    tid = (z.get("mochis") or {}).get("begleiter")
    if tid and expedition.aktiv(z) and not k["def"].get("beistand") and not k["def"].get("training"):
        x, a = z["mochis"]["tiere"][tid], d["tiere"][tid]["aktion"]
        stufe = _stufe(d, x.get("kaempfe", 0))
        k["def"]["beistand"] = {1: [a, None, None], 2: [a, None], 3: [a]}[stufe]
        k["mochi_begleiter"] = tid


def kampf_ende(z, modul, k, ergebnis):
    """Beim Schliessen des Kampfs: gerettetes Tier eintragen, Bindung des Begleiters zaehlen. -> Meldungs-Zeilen"""
    d = _d(modul)
    tid = _tier_von_kampf(modul, k.get("definition"))
    if tid and z.get("inventar"):                          # was nicht geworfen wurde, geht zurueck an Bibi
        z["inventar"] = [x for x in z["inventar"] if x != d["granate"]]
    if tid and ergebnis == "aufgabe" and tid in _s(z)["tiere"]:
        return _nochmal_gefangen(z, modul, tid)
    if tid and ergebnis == "aufgabe":
        s = _s(z)
        s["tiere"][tid] = {"seit": z["tag"], "gesund_ab": None, "gefuettert": False, "kaempfe": 0, "anzahl": 1, "zuletzt": z["tag"]}
        if "mo_fang_heute" not in z["flags"]:
            z["flags"].append("mo_fang_heute")
        z["mochis_brief"] = {"tier": tid}                  # Bibis Overlay (brief_ansicht), geht mit mochis_brief_zu weg
        z["flags"] += [f for f in ("mo_tier_da", "mo_tier_" + tid) if f not in z["flags"]]   # der Epilog fragt danach (mo_frei_*)
        zeilen = _halsband(z, modul, s, d["tiere"][tid]) + zustand.folgen_anwenden(z, modul, [{"vertrauen": ["bibi", 2]}, {"wert": "ruf", "delta": 1}], frei=False)
        if len(s["tiere"]) == len(d["tiere"]) and "mo_buch_voll" not in z["flags"]:
            z["flags"].append("mo_buch_voll")
            zeilen.append("Bibi turns the last page of the field book. She doesn't say anything. She makes you a coffee and she remembers the sugar.")
            zeilen += zustand.folgen_anwenden(z, modul, [{"vertrauen": ["bibi", 6]}], frei=False)
        return zeilen
    begleiter = k.get("mochi_begleiter")
    if begleiter and ergebnis in ("ko", "aufgabe", "entkommen") and begleiter in (z.get("mochis") or {}).get("tiere", {}):
        x = z["mochis"]["tiere"][begleiter]
        vorher = _stufe(d, x.get("kaempfe", 0))
        x["kaempfe"] = x.get("kaempfe", 0) + 1
        if _stufe(d, x["kaempfe"]) > vorher:
            return ["%s moves closer to you now, and helps you more often." % d["tiere"][begleiter]["name"]]
    return []


def _nochmal_gefangen(z, modul, tid):
    """Das zweite Tier derselben Art: Bibi schreibt "hat Gesellschaft" mit dem zweiten Fun Fact (Duc 01.11.2026)."""
    d, s = _d(modul), z["mochis"]
    t, x = d["tiere"][tid], s["tiere"][tid]
    x["anzahl"], x["zuletzt"] = x.get("anzahl", 1) + 1, z["tag"]
    if "mo_fang_heute" not in z["flags"]:
        z["flags"].append("mo_fang_heute")
    f = handy.faden_von(z, "bibi")
    f["tag"], f["phase"], f["gelesen"], f["chips"] = z["tag"], z["phase"], False, []
    f["verlauf"] += [handy._zeile(z, "bibi", text) for text in t["zweit"]]
    return _halsband(z, modul, s, t) + ["📱 Message from Bibi about %s." % t["name"]] + zustand.folgen_anwenden(z, modul, [{"wert": "ruf", "delta": 1}], frei=False)


def brief_ansicht(z, modul, sprite_fn):
    """Overlay nach dem ersten Fang: Tierbild, grosser Name, Bibis vertonte Zeilen."""
    b = z.get("mochis_brief")
    t = _d(modul)["tiere"].get((b or {}).get("tier"))
    if not t:
        return None
    return {"tier": b["tier"], "name": t["name"], "art": t["art"], "bild": "/kampfbild/%sFrei/idle.webp" % t["sprite"],
            "selfie": _selfie(b["tier"], t) if t.get("selfie") else None,
            "zeilen": [{"id": "mochis.%s.%d" % (b["tier"], i), "wer": wer, "name": handel.anzeigename(modul, wer), "text": text,
                        "sprite": sprite_fn(wer, FANG_SET.get(wer), gefuehl, "mochis.%s.%d" % (b["tier"], i))}
                       for i, (wer, text, gefuehl) in enumerate(t["zeilen"])]}


def alle_zeilen(modul):
    """Fuer die Vertonung: (Schluessel, Figur, Text) aller Overlay-Zeilen."""
    return [("mochis.%s.%d" % (tid, i), z_[0], z_[1]) for tid, t in _d(modul).get("tiere", {}).items() for i, z_ in enumerate(t["zeilen"])]


def zeile(modul, zid):
    """mochis.<tier>.<n> -> (Figur, Text) oder (None, None)."""
    _, tid, i = (zid.split(".") + ["", ""])[:3]
    liste = (_d(modul).get("tiere", {}).get(tid) or {}).get("zeilen") or []
    return tuple(liste[int(i)][:2]) if i.isdigit() and int(i) < len(liste) else (None, None)


def _halsband(z, modul, s, t):
    if not t["halsband"]:
        return []
    s["halsbaender"] += 1
    zeilen = ["Bibi cuts off the collar and drops it into a box. That's %d." % s["halsbaender"]]
    if s["halsbaender"] >= _d(modul)["halsband_ziel"] and "mo_halsband_3" not in z["flags"]:
        z["flags"].append("mo_halsband_3")
    return zeilen


# ------------------------------------------------------------------ Aufpaeppeln und Tor
def fuettern(z, modul, tid, art):
    """art = "lieb" (Vorrat, schneller) oder "einfach" (Bibis Futter fuer Geld). Kostet keine Phase."""
    d = _d(modul)
    t = d["tiere"].get(tid)
    if not t or _status(z, tid, t) != "pflege":
        raise ValueError("It doesn't need that right now.")
    x = z["mochis"]["tiere"][tid]
    if art == "lieb":
        key = _futter_key(z, t)
        if not key:
            raise ValueError("You don't have anything it likes.")
        label = _futter_label(modul, key)
        kuechen.vorrat_nehmen(z, key)
        x["gesund_ab"] = z["tag"] + d["tage_futter"]
        zeile = "%s eats all of the %s and looks at you for more." % (t["name"], label.lower())
    else:
        if z["konto"] < d["futter_geld"]:
            raise ValueError("You don't have enough money.")
        z["konto"] -= d["futter_geld"]
        z.setdefault("buchungen", []).append({"text": "Mochi's: feed", "betrag": -d["futter_geld"], "tag": z["tag"]})
        x["gesund_ab"] = z["tag"] + d["tage_einfach"]
        zeile = "%s eats, slowly, with one eye on you. It will take a little longer." % t["name"]
    x["gefuettert"] = True
    return [zeile]


def besuchen(z, modul, tid):
    """Ein Tier im Gehege besuchen (Duc 01.11.2026): kostet nichts. Einmal am Tag zaehlt es fuer die Bindung, der erste Besuch auch fuer Bibi und den Ruf.
    Freigelassen werden alle erst im Epilog (text_frei), bis dahin bleiben sie bei Bibi."""
    d = _d(modul)
    t = d["tiere"].get(tid)
    if not t or _status(z, tid, t) != "bleibt":
        raise ValueError("You can't visit that one yet.")
    x = z["mochis"]["tiere"][tid]
    zeilen = [t["besuch"][x.get("besuche", 0) % len(t["besuch"])]]
    if not x.get("besuche"):
        zeilen += zustand.folgen_anwenden(z, modul, [{"vertrauen": ["bibi", 2]}, {"wert": "ruf", "delta": 1}], frei=False)
    if x.get("besuch_tag") != z["tag"]:
        vorher = _stufe(d, x.get("kaempfe", 0))
        x["besuch_tag"], x["kaempfe"] = z["tag"], x.get("kaempfe", 0) + 1
        if _stufe(d, x["kaempfe"]) > vorher:
            zeilen.append("%s comes straight to the gate now when it hears you." % t["name"])
    if t.get("allein") and not x.get("besuche"):
        zeilen.append("Bibi adds a new note to your Field Book.")
    x["besuche"] = x.get("besuche", 0) + 1
    return zeilen


def begleiter_setzen(z, modul, tid):
    """Einen Begleiter waehlen, oder denselben noch einmal = wieder zu Hause lassen."""
    d = _d(modul)
    t = d["tiere"].get(tid)
    if not t or _status(z, tid, t) != "bleibt":
        raise ValueError("That animal can't come with you.")
    s = z["mochis"]
    s["begleiter"] = None if s.get("begleiter") == tid else tid
    return ["%s comes with you on the next trip." % t["name"]] if s["begleiter"] else ["%s stays at the pen for now." % t["name"]]


def _fund_offen(z, modul):
    s = _lesen(z)
    return [tid for tid, x in (s.get("tiere") or {}).items()
            if _status(z, tid, _d(modul)["tiere"][tid]) == "bleibt" and (s.get("fund_tag") or {}).get(tid) != z["tag"] and s.get("begleiter") != tid]


def einsammeln(z, modul):
    """Was die Tiere heute gefunden haben (einmal am Tag, keine Phase). Der Begleiter sucht nicht, er ist bei Duc."""
    d, zeilen = _d(modul), []
    offene = _fund_offen(z, modul)
    if not offene:
        raise ValueError("Nobody has found anything today.")
    s = z["mochis"]
    for tid in offene:
        t = d["tiere"][tid]
        for n in range(s["tiere"][tid].get("anzahl", 1)):   # das zweite Tier im Gehege sucht mit (Duc 01.11.2026)
            art, was = random.Random("%s-%s-%s-fund%s" % (z.get("id"), z["tag"], tid, n or "")).choice(t["fund"])   # reproducible (gate)
            if art == "r":
                kuechen.rohstoff_add(z, was)
                label = kuechen.daten(modul)["rohstoffe"][was]["label"]
            else:
                kuechen.vorrat_add(z, was, 2)
                label = kuechen.daten(modul)["zutaten"][was]["label"]
            zeilen.append("%s brings you: %s." % (t["name"], label))
        s["fund_tag"][tid] = z["tag"]
    return zeilen

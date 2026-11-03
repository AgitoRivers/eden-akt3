# -*- coding: utf-8 -*-
"""Ermittlung in der Hauptstory (Phase B3, 17.10.2026) - Fakten-Codex, Ermittlungs-Aktionen, Kette.

Die Wahrheit steht in story.json (vertraulich). Hier entscheidet der Code, was Duc wann erfahren kann:
  - Jeder Fakt hat Wege (art, Ort, Person, Tage, Phasen, Bedingung, braucht, Kosten). Ein Weg ist in einer Szene
    moeglich, wenn Ort/Person passen, der Tag im Fenster liegt, die Bedingung gilt und alles Gebrauchte bekannt ist.
  - Aktionen: befragen, untersuchen, sichern, anordnen, abgleichen, tausch (in Szenen); handy und abgleichen auch
    ausserhalb. erinnerung und freiwillig kommen von selbst, sobald ihre Bedingung gilt.
  - Codex: nur, was Duc kennt - sachlich, nach Uhrzeit sortiert (nie nach Bedeutung), mit Quelle und Zuverlaessigkeit.
    Widersprueche ("Das passt zeitlich nicht") markieren niemanden. Tratsch (Lola/Alva) zeigt nur, wo man suchen
    sollte, und ist nie Beweis.
  - Kette: drei Fragen (Handlung, Person, Folge), in allen Faellen gleich. Belegt, wenn ein Beweis-Satz komplett ist.
  - Angst der Verantwortlichen steigt nur, wenn sie von der Ermittlung etwas mitbekommt (B4 nutzt sie).
Ausgaben nennen nie den Fall oder die Verantwortliche - nur Fakten, die Duc selbst gefunden hat."""
import os, re

from . import chronik, regeln, rollen, zustand

ICON = {"befragen": "💬", "untersuchen": "🔍", "sichern": "📌", "anordnen": "📣", "abgleichen": "🧩", "handy": "📱",
        "tausch": "🤝", "erinnerung": "💭", "freiwillig": "🗣"}
VERB = {"befragen": "Question", "untersuchen": "Examine", "sichern": "Secure", "anordnen": "Order",
        "abgleichen": "Cross-check", "handy": "Ask", "tausch": "Trade"}
# reliability of a fact as the player reads it (26.10.2026: English, like all game text)
ZUV_DE = {"gesichert": "secured", "belastbar": "solid", "beobachtet": "seen yourself", "aussage": "only a statement",
          "geruecht": "rumour"}
IN_SZENE = ("befragen", "untersuchen", "sichern", "anordnen", "abgleichen", "tausch", "handy")
AUSSERHALB = ("abgleichen", "handy")
ANGST_MAX = 5


# ------------------------------------------------------------------ Grundlagen
def aktiv(z):
    return str(z.get("wahrheit", "")).startswith("fall_") and _story(z) is not None


def _story(z):
    from . import hauptstory
    moddir = (z.get("plan") or {}).get("_moddir") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", z.get("modul", ""))
    return hauptstory.story(moddir) if hauptstory.aktiv(moddir) else None    # auch nach Tagesende/Ende (kein Plan)


def fall(z):
    st = _story(z)
    if not st or not str(z.get("wahrheit", "")).startswith("fall_"):
        return None
    nr = int(z["wahrheit"].split("_")[1])
    return next((f for f in st["faelle"] if f["nr"] == nr), None)


def fakten(z):
    """{id: fakt} - Fakten des gezogenen Falls plus die zweite Wahrheit."""
    st, f = _story(z), fall(z)
    if not f:
        return {}
    out = {x["id"]: x for x in f["fakten"]}
    for x in st["zweite_wahrheit"]["fakten"]:
        out.setdefault(x["id"], x)
    return out


def stand(z):
    e = z.setdefault("ermittlung", {})
    e.setdefault("bekannt", {})          # fid -> {"tag", "phase", "weg"}
    e.setdefault("genutzt", [])          # Weg-IDs
    e.setdefault("angst", 0)
    e.setdefault("tipps", [])            # gehoerte Tratsch-IDs
    e.setdefault("widersprueche", [])    # erkannte Widerspruchs-IDs
    e.setdefault("geklaert", [])         # nachgefragte Widersprueche
    e.setdefault("schweigt", {})         # pid -> Tag (nach Beschuldigung)
    e.setdefault("gegen", {})            # Gegenhandlungs-ID -> {"tag", "phase"} (B4, nie angezeigt)
    e.setdefault("vorwuerfe", [])        # [{"pid", "tag", "oeffentlich", "belegt", "korrigiert"}] (B4)
    e.setdefault("gestaendnis", None)    # Tag des Gestaendnisses (B4)
    e.setdefault("megan_haltung", 0)
    return e


def kennt(z, fid):
    return fid in (z.get("ermittlung") or {}).get("bekannt", {})


def kennt_gesichert(z):
    F = fakten(z)
    return sum(1 for fid in (z.get("ermittlung") or {}).get("bekannt", {}) if F.get(fid, {}).get("zuverlaessigkeit") == "gesichert")


def glieder_status(z):
    f = fall(z)
    if not f:
        return []
    e = z.get("ermittlung") or {}
    bek = set(e.get("bekannt", {}))
    ersetzt = (f.get("gestaendnis") or {}).get("ersetzt_glied") if e.get("gestaendnis") else None
    return [{"id": g["id"], "frage": g["frage"],
             "belegt": g["id"] == ersetzt or any(set(s) <= bek for s in g["beweis_saetze"])} for g in f["glieder"]]


def kette_bekannt(z):
    g = glieder_status(z)
    return bool(g) and all(x["belegt"] for x in g)


def angst(z):
    return (z.get("ermittlung") or {}).get("angst", 0)


# ------------------------------------------------------------------ Moeglichkeiten
def _weg_ok(z, w, kontext, fid=None):
    e = stand(z)
    if w["id"] in e["genutzt"] or w["id"] in blockiert(z):
        return False
    if fid and not spur_offen(z, fid):
        return False
    a, b = w["tage"]
    if not a <= z["tag"] <= b:
        return False
    if w.get("phasen") and not regeln.phase_passt(z["phase"], w["phasen"]):
        return False
    if w.get("braucht") and not all(x in e["bekannt"] for x in w["braucht"]):
        return False
    if w.get("bedingung") and not regeln.gilt(w["bedingung"], z, kontext):
        return False
    return True


def moeglich(z, modul, sz=None):
    """Aktionen, die jetzt gehen. In einer Szene: am Ort / mit Anwesenden; sonst nur Abgleichen und Handy."""
    F = fakten(z)
    if not F:
        return []
    if not sz and "anhoerung_gehalten" in z["flags"]:
        return []                                      # nach der Anhoerung (Tag 7) keine Ermittlung mehr ausserhalb
    e = stand(z)
    figuren = (sz or {}).get("figuren") or []
    ort = ((sz or {}).get("def") or {}).get("ort")
    kontext = {"anwesend": figuren, "phase": z["phase"]}
    erlaubt = IN_SZENE if sz else AUSSERHALB
    kontakte = set(z.get("bekannt") or modul["personen"]) - set((modul.get("kabine") or {}).get("kein_handy") or [])
    tipp_ziele = {t["zeigt_auf"] for t in (fall(z) or {}).get("tipps", []) if t["id"] in e["tipps"]}
    out, gesehen = [], set()
    for fid, f in F.items():
        if fid in e["bekannt"]:
            continue
        for w in f["wege"]:
            art = w["art"]
            p = w.get("person")
            phase_weg = bool((w.get("kosten") or {}).get("phase")) and art in ("untersuchen", "befragen", "sichern")
            if not sz and phase_weg:
                # Zwischen den Szenen: hingehen und nachsehen bzw. die Person aufsuchen - kostet die ganze Phase
                if not _weg_ok(z, w, kontext, fid) or (p and not _erreichbar(z, modul, p)):
                    continue
                schl = (w["gruppe"], art, p, w.get("ort"))
                if schl not in gesehen:
                    gesehen.add(schl)
                    out.append({"weg": w["id"], "art": art, "icon": ICON.get(art, "🔎"), "verb": VERB.get(art, art),
                                "text": w["text"], "person": p, "ort": w.get("ort"),
                                "kosten": _kosten_text(w.get("kosten"), modul), "tipp": w["id"] in tipp_ziele})
                continue
            if art not in erlaubt or not _weg_ok(z, w, kontext, fid):
                continue
            if art in ("befragen", "tausch", "anordnen") and p and p not in figuren:
                continue
            if art in ("befragen", "tausch") and p and e["schweigt"].get(p) == z["tag"]:
                continue
            if art in ("untersuchen", "sichern") and w.get("ort") and w["ort"] != ort:
                continue
            if art == "handy" and p and p not in kontakte:
                continue
            if art == "handy" and p and p in figuren:
                continue                               # wer da ist, wird gefragt, nicht angerufen
            if w.get("intim") and (sz or {}).get("intim_aktiv") != p:
                continue
            # dieselbe Handlung (Gruppe) nur einmal anbieten - sie liefert alle Fakten der Gruppe auf einmal
            schl = (w["gruppe"], art, p, w.get("ort"))
            if schl in gesehen:
                continue
            sperre = _vertrauen_fehlt(z, modul, f, w)
            if sperre and e.setdefault("abgewiesen", {}).get(w["id"]) == z["tag"]:
                continue                               # heute schon abgewiesen - morgen wieder fragen
            gesehen.add(schl)
            out.append({"weg": w["id"], "art": art, "icon": ICON.get(art, "🔎"), "verb": VERB.get(art, art),
                        "text": w["text"], "person": p, "ort": w.get("ort"),
                        "kosten": _kosten_text(dict(w.get("kosten") or {}, phase=1) if kostet_aktion(w, sz)
                                               else w.get("kosten"), modul), "tipp": w["id"] in tipp_ziele,
                        "sperre": sperre})
    out += _sonder_wege(z, modul, sz, kontext, kontakte)
    out.sort(key=lambda x: (list(ICON).index(x["art"]) if x["art"] in ICON else 9, x["text"]))
    return out


def _erreichbar(z, modul, pid):
    """Kann Duc die Person jetzt aufsuchen? (an Bord bzw. im Dorf, nicht abgereist)"""
    from . import buehne
    return pid in (z.get("bekannt") or modul["personen"]) and buehne.wo_ist(z, modul, pid) is not None


def kostet_aktion(w, sz=None):
    """Modell B: hingehen/aufsuchen (kosten.phase) und - Variante B, 25.10.2026 - jede Handy-Frage ausserhalb einer
    Szene kosten 1 Aktion. Abgleichen bleibt gratis (Nachdenken)."""
    return bool((w.get("kosten") or {}).get("phase")) or (not sz and w["art"] == "handy")


def _kosten_text(k, modul):
    if not k:
        return ""
    teile = []
    if k.get("phase"):
        teile.append("costs 1 action")                 # Modell B: eine von zwei Aktionen der freien Phase
    if k.get("vertrauen"):
        p = modul["personen"].get(k["vertrauen"][0], {})
        teile.append("costs trust with %s" % (p.get("kurz") or p.get("name", "?").split()[0]))
    if k.get("rueckhalt"):
        teile.append("costs the crew's backing")
    if k.get("ruf"):
        teile.append("costs reputation")
    if k.get("flag"):
        teile.append("you'll owe a favour")
    return ", ".join(teile)


def _weg_finden(z, wid):
    for fid, f in fakten(z).items():
        for w in f["wege"]:
            if w["id"] == wid:
                return fid, f, w
    return None, None, None


# ------------------------------------------------------------------ Ausfuehren
def _lernen(z, fid, wid, notiz=None):
    e = stand(z)
    if fid in e["bekannt"]:
        return False
    e["bekannt"][fid] = {"tag": z["tag"], "phase": z["phase"], "weg": wid}
    if notiz:
        e["bekannt"][fid]["notiz"] = notiz
    return True


def ausfuehren(z, modul, wid, sz=None):
    """-> (gelernte Fakten [codex], Antwort-Hinweis fuers Sprachmodell oder "", Folgen-Zeilen, phase_vorbei).
    Die ganze Gruppe des Weges zaehlt als genutzt (eine Handlung)."""
    m = {x["weg"]: x for x in moeglich(z, modul, sz)}
    if wid not in m:
        raise ValueError("Das geht gerade nicht.")
    if ":" in wid:                                     # Route zur zweiten Wahrheit oder Warnzeichen (B4)
        return _sonder_ausfuehren(z, modul, wid, sz)
    if m[wid].get("sperre"):                           # zu wenig Vertrauen: sie weicht aus, der Weg bleibt offen (B4)
        return _ausweichen(z, modul, m[wid], sz)
    e = stand(z)
    fid0, f0, w0 = _weg_finden(z, wid)
    F = fakten(z)
    gelernt = []
    # alle noch unbekannten Fakten derselben Handlung (Gruppe + Art + Person/Ort), deren Weg jetzt offen ist
    kontext = {"anwesend": (sz or {}).get("figuren") or [], "phase": z["phase"]}
    for fid, f in F.items():
        for w in f["wege"]:
            if (w["gruppe"], w["art"], w.get("person"), w.get("ort")) == (w0["gruppe"], w0["art"], w0.get("person"),
                                                                          w0.get("ort")):
                if fid not in e["bekannt"] and _weg_ok(z, w, kontext, fid):
                    _lernen(z, fid, w["id"])
                    gelernt.append(f)
                e["genutzt"].append(w["id"])
    zeilen = kosten_anwenden(z, modul, w0.get("kosten"))
    if w0.get("setzt") and w0["setzt"] not in z["flags"]:
        z["flags"].append(w0["setzt"])                 # z. B. Ausloeser einer Gegenhandlung (story W setzt)
    _angst_pruefen(z, modul, w0, sz)
    zeilen += widersprueche_pruefen(z)
    p = w0.get("person")
    name = (modul["personen"].get(p, {}).get("kurz") or modul["personen"].get(p, {}).get("name", "").split(" ")[0]) if p else ""
    codex = [f["codex"] for f in gelernt]
    if w0["art"] in ("befragen", "tausch", "anordnen") and p:
        hinweis = ("[Investigation - this reply] Duc asks %s about it. In this reply %s tells him exactly this, in her own "
                   "words and in character - no more, nothing invented beyond it: %s\n\n" % (name, name, " / ".join(
                       f["inhalt"] for f in gelernt)))
    elif gelernt:
        hinweis = ("[Investigation - this reply] Duc checks it himself and finds: %s. React to this in character if you "
                   "are present; do not add facts.\n\n" % " / ".join(f["codex"] for f in gelernt))
    else:
        hinweis = ""
    chronik.eintragen(z, modul, "ermittlung", "Duc investigated: %s" % w0["text"], wer=[p] if p else [], wichtig=1)
    return codex, hinweis, zeilen, kostet_aktion(w0, sz)


def kosten_anwenden(z, modul, k):
    if not k:
        return []
    folgen = []
    if k.get("vertrauen"):
        folgen.append({"wert": "vertrauen." + k["vertrauen"][0], "delta": max(-2, k["vertrauen"][1])})
    if k.get("rueckhalt"):
        folgen.append({"wert": "moral", "delta": k["rueckhalt"]})       # Rueckhalt der Crew = Moral
    if k.get("ruf"):
        folgen.append({"wert": "ruf", "delta": k["ruf"]})
    if k.get("flag"):
        folgen.append({"flag": k["flag"]})
    return zustand.folgen_anwenden(z, modul, folgen)


def _angst_pruefen(z, modul, w, sz):
    """Steigt nur, wenn die Verantwortliche es mitbekommt: sie wird befragt oder ist dabei (auffaellige Wege)."""
    f = fall(z)
    v = (f or {}).get("verantwortlich")
    if not v or w.get("auffaellig") is False:
        return
    dabei = v in ((sz or {}).get("figuren") or [])
    if w.get("person") == v or dabei:
        e = stand(z)
        e["angst"] = min(ANGST_MAX, e["angst"] + 1)


def automatisch(z, modul, sz=None):
    """Erinnerungen und freiwillige Mitteilungen, sobald ihre Bedingung gilt. -> Zeilen fuer das Log."""
    F = fakten(z)
    if not F:
        return []
    e = stand(z)
    figuren = (sz or {}).get("figuren") or []
    kontext = {"anwesend": figuren, "phase": z["phase"]}
    zeilen = pflicht_beweise(z, sz)
    for fid, f in F.items():
        if fid in e["bekannt"]:
            continue
        for w in f["wege"]:
            if w["art"] == "erinnerung" and _weg_ok(z, w, kontext, fid):
                _lernen(z, fid, w["id"])
                e["genutzt"].append(w["id"])
                zeilen.append("💭 You remember: " + f["codex"])
                break
            if w["art"] == "freiwillig" and w.get("person") in figuren and _weg_ok(z, w, kontext, fid):
                _lernen(z, fid, w["id"])
                e["genutzt"].append(w["id"])
                p = modul["personen"][w["person"]]
                zeilen.append("🗣 %s tells you without being asked: %s" % (p.get("kurz") or p["name"].split()[0], f["codex"]))
                break
    zeilen += widersprueche_pruefen(z)
    zeilen += tratsch(z, modul, sz)
    zeilen += flags_verarbeiten(z, modul)
    zeilen += belegt_melden(z)
    return zeilen


def pflicht_beweise(z, sz=None):
    """Garantierte Kernbeweise (Duc 28.10.2026): What kommt mit Rosis Whiteboard (Tag 4), Why mit Megans Mappe (Tag 5).
    Laeuft die Szene, liefert sie; wurde sie verpasst, kommt es am naechsten Tag nach. Nichts, solange das Glied schon
    belegt ist. Gegenhandlungen sperren diese Wege nicht (es sind Kopien bzw. Rosis eigene Messung). -> Zeilen"""
    e = stand(z)
    szene_id = ((sz or {}).get("def") or {}).get("id")
    belegt = {g["id"] for g in glieder_status(z) if g["belegt"]}
    zeilen = []
    for fid, f in fakten(z).items():
        for w in f["wege"]:
            if w["art"] != "pflicht" or fid in e["bekannt"] or w["id"] in e["genutzt"] or w.get("glied") in belegt:
                continue
            a, b = w["tage"]
            if not a <= z["tag"] <= b or (z["tag"] == a and szene_id != w.get("szene")):
                continue
            _lernen(z, fid, w["id"])
            e["genutzt"].append(w["id"])
            zeilen.append("📌 %s: %s" % (w["text"], f["codex"]))
    return zeilen


def belegt_melden(z):
    """Eine Frage des Falls springt auf Proven -> einmal eine Zeile (der Client spielt Ton + Aufleuchten im Codex)."""
    e = stand(z)
    gemeldet = e.setdefault("belegt_gemeldet", [])
    zeilen = []
    for g in glieder_status(z):
        if g["belegt"] and g["id"] not in gemeldet:
            gemeldet.append(g["id"])
            zeilen.append("✔ The case: “%s” – proven." % g["frage"])
    return zeilen


# Fall-Tafel (Duc 28.10.2026): je offener Frage nur die ART dessen, was fehlt - nie Namen, Orte, Uhrzeiten.
TAFEL_STAPEL = {"systems": ("Nothing on the ship's systems yet.", "One more piece from the ship's systems."),
                "papers": ("Nothing on paper yet – a log or a file.", "One more piece on paper – a log or a file."),
                "people": ("Somebody saw something. You haven't heard it yet.",
                           "Someone still has to tell you a piece of it."),
                "own": ("You still have to put two things together yourself.",
                        "One more thing to put together yourself.")}


def _stapel(modul, f):
    from .anhoerung import karte_einordnen          # dieselbe Einordnung wie die Zettel in der Anhoerung
    return karte_einordnen(modul, f)[0]


TAFEL_KURZ = {"handlung": "What", "person": "Who", "folge": "Why"}


def tafel_kurz(z, modul):
    """Fuer das Ermittlungsfeld in der Szene (Duc 29.10.2026): je offene Frage eine Zeile, was noch fehlt (nur die Art)."""
    return ["%s · %s" % (TAFEL_KURZ.get(g["id"], g["id"]), " ".join(g["fehlt"]))
            for g in tafel(z, modul) if g["stand"] != "proven" and g["fehlt"]]


def tafel(z, modul):
    """-> [{id, frage, stand: open|partly|proven, x, y, fehlt: [Saetze]}] fuer Codex und Anhoerung."""
    f, F = fall(z), fakten(z)
    if not f:
        return []
    bek = set(stand(z)["bekannt"])
    status = {g["id"]: g["belegt"] for g in glieder_status(z)}
    out = []
    for g in f["glieder"]:
        if status.get(g["id"]):
            out.append({"id": g["id"], "frage": g["frage"], "stand": "proven", "x": 1, "y": 1, "fehlt": []})
            continue
        satz = max(g["beweis_saetze"], key=lambda s: (len(set(s) & bek) / len(s), -len(s)))
        x = len(set(satz) & bek)
        fehlt, saetze = [], []
        for fid in satz:
            if fid not in bek and fid in F:
                st = _stapel(modul, F[fid])
                if st not in fehlt:
                    fehlt.append(st)
        for st in fehlt[:2]:
            saetze.append(TAFEL_STAPEL[st][0 if x == 0 else 1])
        out.append({"id": g["id"], "frage": g["frage"], "stand": "partly" if x else "open", "x": x, "y": len(satz),
                    "fehlt": saetze})
    return out


def tratsch(z, modul, sz):
    """Lola an Bord, Alva an Land: ab ihrem Vertrauen ein Hinweis, WO man nachsehen koennte - nie Beweis."""
    f = fall(z)
    if not f or not sz:
        return []
    e = stand(z)
    zeilen = []
    for t in f.get("tipps", []):
        if t["id"] in e["tipps"] or t["wer"] not in sz.get("figuren", []) or z["tag"] < t.get("ab_tag", 1):
            continue
        if t.get("nach") and t["nach"] not in stand(z)["gegen"]:
            continue                                   # Tratsch ueber eine Gegenhandlung erst, wenn es sie gab
        if z["werte"].get("vertrauen." + t["wer"], 0) < t.get("ab_vertrauen", 0):
            continue
        e["tipps"].append(t["id"])
        p = modul["personen"][t["wer"]]
        zeilen.append("💬 %s (rumour): %s" % (p.get("kurz") or p["name"].split()[0], t["text"]))
        break                                          # hoechstens ein Tratsch pro Szene
    return zeilen


def widersprueche_pruefen(z):
    """Erkannte Widersprueche: Aussage und Gegenbeleg bekannt, ab Tag. Markiert niemanden."""
    f = fall(z)
    if not f:
        return []
    e = stand(z)
    zeilen = []
    for ws in f.get("widersprueche", []):
        if ws["id"] in e["widersprueche"] or z["tag"] < ws.get("tag_ab", 1):
            continue
        if kennt(z, ws["aussage"]) and all(kennt(z, g) for g in ws["gegen"]) and all(kennt(z, b) for b in ws["braucht"]):
            e["widersprueche"].append(ws["id"])
            zeilen.append("⏱ The times don't add up: " + ws["codex"])
    return zeilen


def widerspruch_aktionen(z, modul, sz):
    """In einer Szene: erkannte, ungeklaerte Widersprueche, deren Urheberin anwesend ist."""
    f = fall(z)
    if not f or not sz:
        return []
    e, F = stand(z), fakten(z)
    out = []
    for ws in f.get("widersprueche", []):
        if ws["id"] not in e["widersprueche"] or ws["id"] in e["geklaert"]:
            continue
        p = F.get(ws["aussage"], {}).get("person")
        if p and p in sz.get("figuren", []) and e["schweigt"].get(p) != z["tag"]:
            n = modul["personen"][p].get("kurz") or modul["personen"][p]["name"].split()[0]
            out.append({"id": ws["id"], "person": p, "name": n, "codex": ws["codex"]})
    return out


def widerspruch_klaeren(z, modul, wsid, beschuldigen, sz):
    """Nachfragen: neue, ueberpruefbare Angabe. Beschuldigen: Widerstand (Vertrauen -2, sie schweigt heute)."""
    f, e, F = fall(z), stand(z), fakten(z)
    ws = next((x for x in (f or {}).get("widersprueche", []) if x["id"] == wsid), None)
    if not ws or ws["id"] in e["geklaert"]:
        raise ValueError("Dazu gibt es gerade nichts nachzufragen.")
    p = F.get(ws["aussage"], {}).get("person")
    n = modul["personen"][p].get("kurz") or modul["personen"][p]["name"].split()[0]
    if beschuldigen:
        e["schweigt"][p] = z["tag"]
        zeilen = zustand.folgen_anwenden(z, modul, [{"wert": "vertrauen." + p, "delta": -2}])
        _angst_pruefen(z, modul, {"person": p}, sz)
        hinweis = ("[Investigation - this reply] Duc accuses %s outright, without proof. She closes up: she is hurt or "
                   "angry, denies it and refuses to say anything more about it today.\n\n" % n)
        return [], hinweis, zeilen
    e["geklaert"].append(ws["id"])
    neu = F.get(ws["nachfragen"])
    gelernt = []
    if neu and _lernen(z, neu["id"], "nachfragen:" + ws["id"]):
        gelernt.append(neu["codex"])
    _angst_pruefen(z, modul, {"person": p}, sz)
    hinweis = ("[Investigation - this reply] Duc points out, without accusing her, that her account does not fit the "
               "times. %s answers with a new, checkable detail - exactly this, in character: %s\n\n"
               % (n, neu["inhalt"] if neu else "she cannot explain it yet"))
    return gelernt, hinweis, widersprueche_pruefen(z)


# ------------------------------------------------------------------ Wissen der Figuren
def wissen_fuer(z, pid):
    """Was eine Figur im Prompt 'weiss': nur Fakten, die sie kennt UND die Duc schon herausgefunden hat, plus
    harmlose Rahmen-Fakten (r_). Geheimnisse bleiben so beim Code, nicht beim Sprachmodell."""
    F = fakten(z)
    e = (z.get("ermittlung") or {}).get("bekannt", {})
    out = []
    for fid, f in F.items():
        if pid not in f.get("wissende", []) and f.get("person") != pid:
            continue
        if fid in e or (fid.startswith("r_") and f.get("wahr", True)):
            out.append(f["inhalt"])
    return out[:12]


# ------------------------------------------------------------------ Codex-Ansicht
def ansicht(z, modul, sz=None):
    if not fakten(z):
        return None
    e, F = stand(z), fakten(z)
    eintraege = []
    for fid, info in e["bekannt"].items():
        f = F.get(fid)
        if not f:
            continue
        zeit = f.get("zeit_pms") and ("%s (power management display)" % f["zeit_pms"].split(" ")[1]) or \
            (f["zeit"].split(" ")[1] if not f["zeit"].startswith("T-") else "before the voyage")
        tag = f["zeit"].split(" ")[0]
        eintraege.append({"id": fid, "text": f["codex"], "zeit": zeit, "tag": tag, "sort": _sort(f["zeit"]),
                          "zuv": ZUV_DE.get(f["zuverlaessigkeit"], f["zuverlaessigkeit"]),
                          "beweis": f["zuverlaessigkeit"] in ("gesichert", "belastbar", "beobachtet"),
                          "gefunden": "Day %d" % info["tag"]})
    eintraege.sort(key=lambda x: x["sort"])
    for x in eintraege:
        x.pop("sort")
    f = fall(z)
    ws = [w["codex"] for w in (f or {}).get("widersprueche", []) if w["id"] in e["widersprueche"]]
    tipps = [t["text"] for t in (f or {}).get("tipps", []) if t["id"] in e["tipps"]]
    return {"fragen": glieder_status(z), "tafel": tafel(z, modul), "kette": kette_bekannt(z), "eintraege": eintraege, "widersprueche": ws,
            "geruechte": tipps, "aussen": moeglich(z, modul, None) if not sz else []}


def _sort(t):
    m = re.match(r"^T(-?\d+) (\d\d):(\d\d)$", t)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (99, 0, 0)


# ====================================================================== B4: Gegenwehr, Konfrontation, Megan, Technik
# (18.10.2026) Regeln aus story.json: hoechstens eine Gegenhandlung pro Tag, jede mit Spur und Umweg; Angst steigt nur,
# wenn die Person etwas mitbekommt; Anklage nur mit belegter Kette; Megans Haltung aus Ducs Handeln (kein Zufall);
# Brand nur, wenn sichtbare Warnzeichen ignoriert und das Modul nicht abgetrennt wurde. Nichts davon wird angezeigt,
# ausser dem, was Duc selbst sieht (Spur, Warnzeichen, Reaktionen).


def _gh_liste(z):
    return (fall(z) or {}).get("gegenhandlungen", [])


def _sichtbar_tag(gh):
    m = re.match(r"T(\d+)", gh.get("sichtbar_ab") or "")
    return int(m.group(1)) if m else gh["tag"]


def blockiert(z):
    """Weg-IDs, die eine geschehene Gegenhandlung versperrt hat (es gibt immer einen Umweg)."""
    e = z.get("ermittlung") or {}
    out = set()
    for gh in _gh_liste(z):
        if gh["id"] in e.get("gegen", {}):
            out.update(gh.get("blockiert") or [])
    return out


def spur_offen(z, fid):
    """Die Spur einer Gegenhandlung gibt es erst, wenn sie geschehen ist - und ab ihrem Sichtbar-Tag."""
    e = z.get("ermittlung") or {}
    for gh in _gh_liste(z):
        if gh.get("spur") == fid:
            return gh["id"] in e.get("gegen", {}) and z["tag"] >= _sichtbar_tag(gh)
    return True


def _name(modul, pid):
    p = modul["personen"].get(pid, {})
    return p.get("kurz") or p.get("name", "?").split(" ")[0]


def phase_ende(z, modul):
    """Am Ende jeder Phase (plan.naechste_phase): Gegenhandlung, Warnzeichen, Brand-Pruefung, Nachtende, Megan.
    -> Zeilen fuer eine Meldung (nur Sichtbares)."""
    if not aktiv(z) or not z.get("persona"):
        return []
    e = stand(z)
    zeilen = []
    if not any(x["tag"] == z["tag"] for x in e["gegen"].values()):
        for gh in _gh_liste(z):
            if gh["id"] in e["gegen"] or gh["tag"] != z["tag"] or gh.get("phase", "nacht") != z["phase"]:
                continue
            if regeln.gilt(gh.get("ausloeser"), z):
                e["gegen"][gh["id"]] = {"tag": z["tag"], "phase": z["phase"]}
                break                                          # hoechstens eine pro Tag
    zeilen += _warnzeichen(z)
    _brand_pruefen(z)
    zeilen += _nachtende(z, modul)
    megan_haltung(z)
    return zeilen


def etwas_anders(z):
    """Frueh am Morgen nach einer naechtlichen Gegenhandlung: Ort, an dem sich etwas veraendert hat (oder None)."""
    if not aktiv(z):
        return None
    e, F = stand(z), fakten(z)
    for gh in _gh_liste(z):
        x = e["gegen"].get(gh["id"])
        if not x or x["tag"] != z["tag"] - 1 or _sichtbar_tag(gh) > z["tag"]:
            continue
        w = next((w for w in (F.get(gh["spur"]) or {}).get("wege", []) if w["art"] in ("untersuchen", "sichern")
                  and w.get("ort")), None)
        if w:
            return {"ort": w["ort"]}
    return None


# ------------------------------------------------------------------ Technik: Warnzeichen und Brand
WARN = {4: "⚠ Rosi meldet: Das Umrichtergehäuse ist warm, obwohl der Antrieb steht. Sie misst zweimal.",
        5: "⚠ Im Technikraum riecht es nach heißem Kunststoff. Die Messwerte am Umrichter steigen, dieselbe Warnung "
           "kommt immer wieder."}


def _warnzeichen(z):
    """Sichtbare Warnzeichen am Ende von Tag 4 und 5 (Nacht) - nie verdeckt, nie zufaellig.
    Akt-Stories (story "akt", seit 24.10.2026): keine - der Umrichter ist im Cold Open schon explodiert."""
    if (_story(z) or {}).get("akt"):
        return []
    if z["phase"] != "nacht" or z["tag"] not in WARN or "warnung_%d" % z["tag"] in z["flags"]:
        return []
    z["flags"].append("warnung_%d" % z["tag"])
    return [WARN[z["tag"]]]


def _brand_pruefen(z):
    """Tag 6 nach dem technischen Weg: Brand nur, wenn das Modul nicht abgetrennt und die Warnzeichen ignoriert wurden."""
    if z["tag"] != 6 or z["phase"] not in ("tag", "dinner", "abend") or "brand_geprueft" in z["flags"]:
        return
    if not any(f in z["flags"] for f in ("weg_reparatur", "weg_schlepp", "weg_isolation")):
        return
    z["flags"].append("brand_geprueft")
    if "weg_isolation" not in z["flags"] and "warnzeichen_beachtet" not in z["flags"]:
        z["flags"].append("brand")


# ------------------------------------------------------------------ Nachtende (Tag 3): eine Nachricht mit Fakten
def _nachtende(z, modul):
    f = fall(z)
    if not f or z["tag"] != 3 or z["phase"] != "nacht" or "nachtende" in z["flags"]:
        return []
    z["flags"].append("nachtende")
    ne = f.get("nachtende") or {}
    neu = [fid for fid in ne.get("fakten", []) if fid in fakten(z) and not kennt(z, fid)]
    pid = ne.get("absender")
    if not neu or pid not in modul["personen"]:
        return []
    from . import handy
    F = fakten(z)
    for fid in neu:
        _lernen(z, fid, "nachtende")
    faden = handy.faden_von(z, pid)
    faden["tag"], faden["phase"], faden["gelesen"] = z["tag"], z["phase"], False
    faden["verlauf"].append(handy._zeile(z, pid, "Can't sleep. That night keeps going round in my head - there's "
                                                 "something you should know. Wrote it down for you, check your notes."))
    chronik.eintragen(z, modul, "ermittlung", "%s told Duc something about the night by text." % _name(modul, pid),
                      wer=[pid], dabei=[], wichtig=1, ort="handy")
    return ["📱 %s texts you in the middle of the night: %s" % (_name(modul, pid), F[fid]["codex"]) for fid in neu]


# ------------------------------------------------------------------ Megans Haltung (zweite Wahrheit)
def megan_haltung(z):
    st = _story(z)
    if not st:
        return 0
    m = st["zweite_wahrheit"]["megan_haltung"]
    e = stand(z)
    h = m.get("start", 0)
    for flag, d, _ in m.get("plus", []) + m.get("minus", []):
        if flag == "vertrauen_megan_3":
            ok = z["werte"].get("vertrauen.megan", 0) >= 3
        elif flag == "anschuldigung_ohne_beleg":
            ok = any(v["oeffentlich"] and not v["belegt"] and not v.get("korrigiert") for v in e["vorwuerfe"])
        else:
            ok = flag in z["flags"]
        if ok:
            h += d
    e["megan_haltung"] = h
    return h


# ------------------------------------------------------------------ Sonderwege: Routen zur zweiten Wahrheit, Warnzeichen
def _routen(z):
    st = _story(z)
    return st["zweite_wahrheit"].get("routen", {}) if st else {}


ROUTE_FOLGE = {"route_rosi": "Rosi schreibt dem Hersteller. Die Antwort kann ein paar Tage dauern.",
               "route_elsa": "Elsa fordert die Unterlagen an. Das dauert ein paar Tage.",
               "route_megan": "Megan hört zu. Lange. Dann sagt sie, sie melde sich.",
               "route_spaet": "Die Nachprüfung läuft. Vor der Endfassung sollte etwas zurückkommen."}


def _sonder_wege(z, modul, sz, kontext, kontakte):
    out = []
    figuren = (sz or {}).get("figuren") or []
    for rid, r in _routen(z).items():
        w = r["eroeffnen"]
        if r["setzt"] in z["flags"] or (r.get("nur_wenn") and stand(z)["megan_haltung"] < 0):
            continue
        a, b = w["tage"]
        if not a <= z["tag"] <= b or (w.get("braucht") and not all(kennt(z, x) for x in w["braucht"])):
            continue
        if w.get("bedingung") and not regeln.gilt(w["bedingung"], z, kontext):
            continue
        p, art = w.get("person"), w["art"]
        kosten = dict(w.get("kosten") or {})
        if art == "befragen":
            if sz and p not in figuren:
                continue
            if not sz:
                if not _erreichbar(z, modul, p):
                    continue
                kosten["phase"] = 1                            # die Person aufsuchen kostet die Phase
        elif art == "handy" and p and (p not in kontakte or p in figuren):
            continue
        out.append({"weg": "route:" + rid, "art": art, "icon": ICON.get(art, "🔎"), "verb": VERB.get(art, art),
                    "text": w["text"], "person": p, "ort": w.get("ort"), "kosten": _kosten_text(kosten, modul),
                    "tipp": False})
    ort = ((sz or {}).get("def") or {}).get("ort")
    if sz and ort in ("power_room", "generator_room", "workshop") and 4 <= z["tag"] <= 6 and \
            "warnung_4" in z["flags"] and "warnzeichen_beachtet" not in z["flags"]:
        out.append({"weg": "tech:warnzeichen", "art": "untersuchen", "icon": ICON["untersuchen"], "verb": "Untersuchen",
                    "text": "Die Warnzeichen am Umrichter ernst nehmen: messen, protokollieren, überwachen lassen",
                    "person": None, "ort": ort, "kosten": "", "tipp": False})
    return out


def _sonder_ausfuehren(z, modul, wid, sz):
    art, rid = wid.split(":", 1)
    if art == "tech":
        z["flags"].append("warnzeichen_beachtet")
        chronik.eintragen(z, modul, "ermittlung", "Duc had the warning signs at the inverter measured and logged; "
                                                 "it is now watched around the clock.", wer=[], wichtig=1)
        return (["Warnzeichen protokolliert – der Umrichter wird ab jetzt rund um die Uhr überwacht."],
                "[Investigation - this reply] Duc takes the warning signs at the inverter seriously: heat, smell, "
                "rising readings. He has them measured and logged and sets a watch on it. React in character.\n\n",
                [], False)
    r = _routen(z)[rid]
    w = r["eroeffnen"]
    z["flags"].append(r["setzt"])
    kosten = dict(w.get("kosten") or {})
    if w["art"] == "befragen" and not sz:
        kosten["phase"] = 1
    zeilen = kosten_anwenden(z, modul, kosten)
    p = w.get("person")
    chronik.eintragen(z, modul, "ermittlung", "Duc investigated: %s" % w["text"], wer=[p] if p else [], wichtig=1)
    megan_haltung(z)
    hinweis = ("[Investigation - this reply] Duc asks %s for this: %s. %s agrees to try; it will take a few days. "
               "Do not invent any result.\n\n" % (_name(modul, p), w["text"], _name(modul, p))) if p else ""
    return [ROUTE_FOLGE.get(rid, "Angestoßen.")], hinweis, zeilen, bool(kosten.get("phase"))


# ------------------------------------------------------------------ Konfrontation, Vorwurf, Korrektur, Gestaendnis
KONFRONT_AB = 4


def _vorwurf(z, pid):
    return next((v for v in stand(z)["vorwuerfe"] if v["pid"] == pid), None)


def konfrontation_aktionen(z, modul, sz):
    """Ab Tag 4 in einer Szene: jede anwesende Verdaechtige gleich (die Liste verraet nichts). Dazu Korrekturen."""
    if not sz or not aktiv(z) or z["tag"] < KONFRONT_AB:
        return []
    if str((sz.get("def") or {}).get("id", "")).startswith("anhoerung"):
        return []                                      # in der Anhoerung klagt Duc ueber den Wahlmoment an (anhoerung.py)
    st, e = _story(z), stand(z)
    figuren = sz.get("figuren") or []
    out = []
    for p in st.get("verdaechtige", []):
        if p in figuren and not _vorwurf(z, p) and e["schweigt"].get(p) != z["tag"] and not e["gestaendnis"]:
            andere = [x for x in figuren if x != p]
            out.append({"id": "konfront:" + p, "person": p, "name": _name(modul, p), "oeffentlich": bool(andere),
                        "text": ("In front of everyone: confront %s with your suspicion" if andere else
                                 "In private: confront %s with your suspicion") % _name(modul, p)})
    if len(figuren) >= 2:
        for v in e["vorwuerfe"]:
            if v["oeffentlich"] and not v["belegt"] and not v.get("korrigiert"):
                out.append({"id": "korrektur:" + v["pid"], "person": v["pid"], "name": _name(modul, v["pid"]),
                            "oeffentlich": True,
                            "text": "Take it back in front of everyone: the accusation against %s wasn't backed up" % _name(modul, v["pid"])})
    return out


def konfrontieren(z, modul, aid, sz):
    """-> (zeilen, hinweis). Gestaendnis nur mit belegter Kette; sonst bestreitet jede Person gleich (verraet nichts)."""
    if aid not in [a["id"] for a in konfrontation_aktionen(z, modul, sz)]:
        raise ValueError("Das geht gerade nicht.")
    art, pid = aid.split(":", 1)
    e, f = stand(z), fall(z)
    n = _name(modul, pid)
    if art == "korrektur":
        v = _vorwurf(z, pid)
        v["korrigiert"] = z["tag"]
        zeilen = zustand.folgen_anwenden(z, modul, [{"wert": "vertrauen." + pid, "delta": 1}, {"wert": "moral", "delta": 1}])
        chronik.eintragen(z, modul, "moment", "In front of everyone, Duc took back his accusation against %s: it was "
                                             "not proven." % n, wer=[pid] + sz["figuren"], wichtig=2)
        megan_haltung(z)
        return ["You take back the accusation against %s in front of everyone." % n] + zeilen, (
            "[This reply] In front of everyone, Duc openly takes back his accusation against %s - it was not proven. "
            "React in character: relief, hurt, or a cautious thaw.\n\n" % n)
    oeff = len([x for x in sz["figuren"] if x != pid]) > 0
    belegt = kette_bekannt(z) and f.get("verantwortlich") == pid
    e["vorwuerfe"].append({"pid": pid, "tag": z["tag"], "oeffentlich": oeff, "belegt": belegt})
    chronik.eintragen(z, modul, "moment", "Duc %s confronted %s with his suspicion about the night of the failure." % (
        "publicly" if oeff else "privately", n), wer=[pid] + (sz["figuren"] if oeff else []), wichtig=2)
    if belegt and (f.get("gestaendnis") or {}).get("moeglich"):
        return _gestehen(z, modul, pid, "konfrontation")
    if pid == f.get("verantwortlich"):
        e["angst"] = min(ANGST_MAX, e["angst"] + 1)
    e["schweigt"][pid] = z["tag"]
    folgen = [{"wert": "vertrauen." + pid, "delta": -2 if oeff else -1}]
    if oeff:
        folgen.append({"wert": "moral", "delta": -1})
    zeilen = zustand.folgen_anwenden(z, modul, folgen)
    megan_haltung(z)
    return (["%s bestreitet es. Ohne lückenlose Belege bleibt es deine Vermutung." % n] + zeilen,
            "[This reply] Duc confronts %s %s with his suspicion that she caused the failure. %s denies it - hurt, "
            "angry or cold, in character - and does not want to talk about it any more today. Nothing is confirmed.\n\n"
            % (n, "in front of everyone" if oeff else "in private", n))


def _gestehen(z, modul, pid, wie):
    e, f = stand(z), fall(z)
    g = f.get("gestaendnis") or {}
    e["gestaendnis"] = z["tag"]
    if "gestaendnis" not in z["flags"]:
        z["flags"].append("gestaendnis")
    for v in e["vorwuerfe"]:
        if v["pid"] == pid:
            v["belegt"] = True
    n = _name(modul, pid)
    chronik.eintragen(z, modul, "moment", "%s admitted to Duc what she did on the night of the failure." % n,
                      wer=[pid], wichtig=3, dauer=3)
    satz = (g.get("kernsatz") or {}).get("en", "")
    kern = f.get("kern", "")
    return (["🗣 %s stops denying and tells you what happened that night." % n,
             "The question “Who?” is answered now."],
            "[This reply - the turning point] %s stops denying. %s She admits, in her own words and in character, what "
            "she did that night and why - close to this sentence: \"%s\". No excuses invented beyond that, no new "
            "facts.\n\n" % (n, "Duc has laid out the proven chain." if wie == "konfrontation" else
                            "She asked Duc for this private talk herself.", satz))


def freiwillig_gestehen(z, modul, sz):
    """Freiwilliges Gestaendnis (fall.gestaendnis.freiwillig), wenn die Person in der Szene ist. -> (zeilen, pid, hinweis)"""
    f, e = fall(z), stand(z)
    if not f or not sz or e["gestaendnis"] or not f.get("verantwortlich"):
        return None
    pid = f["verantwortlich"]
    if pid not in (sz.get("figuren") or []) or sz.get("wahlmoment_offen"):
        return None
    for fr in (f.get("gestaendnis") or {}).get("freiwillig", []):
        if z["tag"] >= fr.get("ab_tag", 1) and regeln.gilt(fr.get("bedingung"), z, {"anwesend": sz["figuren"]}):
            zeilen, hinweis = _gestehen(z, modul, pid, "freiwillig")
            return zeilen, pid, hinweis
    return None


# ------------------------------------------------------------------ Story-Flags, die etwas ausloesen
def flags_verarbeiten(z, modul=None):
    """Einmalige Folgen von Story-Entscheidungen (der_satz, bericht, Holms Abschied). -> Zeilen"""
    e = stand(z)
    fertig = e.setdefault("verarbeitet", [])
    zeilen = []
    if modul and "holm_evakuiert" in z["flags"] and "holm_abschied" not in fertig:
        fertig.append("holm_abschied")
        vt = z["werte"].get("vertrauen.holm", 0)
        if vt >= 2 and "holm_compass" in modul.get("items", {}):     # Grundlagen: Kompass ab Holms Vertrauen 2
            zeilen += zustand.folgen_anwenden(z, modul, [{"item": "holm_compass"}])
            zeilen.append("Holm presses her brass compass into your hand.")
        if vt >= 3:                                    # ... ab 3 stellt sie sich bei der Uebergabe vor Duc
            alt = z["werte"].get("rueckhalt", 50)
            z["werte"]["rueckhalt"] = min(100, alt + 10)
            zeilen.append("Holm stands in front of you at the handover – crew backing +%d" % (z["werte"]["rueckhalt"] - alt))
    if "satz_mitteilen" in z["flags"] and "satz_mitteilen" not in fertig:
        fertig.append("satz_mitteilen")
        if (fall(z) or {}).get("verantwortlich"):
            e["angst"] = min(ANGST_MAX, e["angst"] + 1)          # oeffentliche Andeutung
    for fl in ("bericht_vollstaendig", "bericht_vorlaeufig"):
        if fl in z["flags"] and "unterscheidung" not in fertig:
            fertig.append("unterscheidung")
            if kennt(z, "z_03") or kennt(z, "z_01"):
                z["flags"].append("unterscheidung_bestanden")
    megan_haltung(z)
    return zeilen


# ------------------------------------------------------------------ Besetzung fallabhaengiger Szenen (B4)
def besetzung(z, modul, platzhalter, sid):
    """$fall3: die Hauptperson des Falls plus zwei weitere aus dem Kreis, gemischt (die Liste verraet nichts).
    $fall1: nur die Hauptperson (Fall ohne Verantwortliche: wen Duc zuletzt beschuldigt hat, sonst der Ersatz).
    Kreis, Ersatz und Besetzung ohne Fall: modul["ermittlung"] (rollen.py)."""
    import random
    e = modul.get("ermittlung") or {}
    f = fall(z)
    if not f:
        return list(e.get("verdacht_ohne_fall") or [])[:3 if platzhalter == "$fall3" else 1]
    haupt = f.get("verantwortlich")
    if not haupt:
        v = [x["pid"] for x in stand(z)["vorwuerfe"]]
        haupt = v[-1] if v else e.get("ersatz")
    if sid == "widerspruch" and f.get("widersprueche"):
        haupt = fakten(z).get(f["widersprueche"][0]["aussage"], {}).get("person") or haupt
    if platzhalter == "$fall1":
        return [haupt]
    rng = random.Random("%s-%s-besetzung" % (z.get("id"), sid))
    andere = [p for p in e.get("verdacht") or [] if p != haupt]
    rng.shuffle(andere)
    out = [haupt] + andere[:2]
    rng.shuffle(out)
    return out


# ------------------------------------------------------------------ Vertrauen als Schluessel (B4, 18.10.2026)
# Wer etwas Wahres weiss, sagt es erst, wenn er Duc genug vertraut. Luegen und Ausfluechte gibt es immer.
# So greifen Ermittlung und Beziehungen ineinander: Zeit mit jemandem verbringen oeffnet Aussagen.
# Schwellen je Person: modul["ermittlung"]["schwelle"] (z. B. Behoerde und Fachmann 0), sonst 2.
SCHWELLE_STANDARD = 2


def schwelle(modul, pid):
    return ((modul.get("ermittlung") or {}).get("schwelle") or {}).get(pid, SCHWELLE_STANDARD)


def _vertrauen_fehlt(z, modul, f, w):
    p = w.get("person")
    if not p or w["art"] not in ("befragen", "handy") or f.get("wahr") is False:     # ein Tausch ist ein Handel
        return ""
    if f.get("zuverlaessigkeit") == "aussage" and p == (fall(z) or {}).get("verantwortlich"):
        return ""                                      # was die Hauptperson ueber sich selbst sagt, sagt sie ohnehin
    wert = z["werte"].get("vertrauen." + p, 0)
    wert = rollen.haendler_vertrauen(z, modul, p, wert)
    if wert >= schwelle(modul, p):
        return ""
    return "%s doesn't trust you enough yet (needs %d)" % (_name(modul, p), schwelle(modul, p))


def _ausweichen(z, modul, a, sz):
    p = a["person"]
    stand(z).setdefault("abgewiesen", {})[a["weg"]] = z["tag"]
    n = _name(modul, p)
    chronik.eintragen(z, modul, "ermittlung", "Duc asked %s about the night; she did not want to talk about it yet." % n,
                      wer=[p], wichtig=1)
    hinweis = ("[Investigation - this reply] Duc asks %s about the night of the failure. %s does not trust him enough "
               "yet to tell him: she deflects, changes the subject or says she has to think about it - in character, "
               "without revealing anything.\n\n" % (n, n)) if a["art"] != "handy" else ""
    return [], hinweis, ["%s weicht aus. Vielleicht später – wenn sie dir mehr vertraut." % n], False

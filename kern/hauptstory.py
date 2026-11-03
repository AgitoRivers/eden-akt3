# -*- coding: utf-8 -*-
"""Spielleiter der Hauptstory (Phase B2, 17.10.2026) - fuer Module mit story.json (eden_rise).

Statt eines Szenen-Vorrats (showrunner.py) gibt der Wochenbogen der Story jeden Tag vor:
  - Phasen mit Story-Szenen laufen als FOLGE: alle spielbaren Szenen der Phase nacheinander (plan.py "folge").
    Szenen mit Bedingung (z. B. Brand) werden erst beim Erreichen geprueft; optionale Naehe-Szenen nur, wenn es eine
    vertraute Person gibt.
  - Phasen ohne Story-Szene sind frei: 2-3 Optionen "Zeit mit ..." an ihrem Ort (Wahl-Phase) bzw. eine (Pflicht),
    dazu wie immer die Kabine.
  - Tag 1 beginnt am Abend (Party); Phasen davor fehlen im Plan und werden uebersprungen.
Wie eine Szene aussieht (Text fuer Duc, Ort, wer da ist, Entscheidungen) steht in buehne.json (story_buehne.py);
die vertrauliche Regie-Notiz (story kern) geht nur ans Sprachmodell. Fall-Inhalte kommen erst in B3/B4 dazu.
Der Fall selbst wird von zustand.neu gezogen (wahrheit = fall_1..fall_5) und hier nie ausgegeben."""
import copy, json, os, random, re

from . import regeln, rollen, showrunner

_CACHE = {}
NAEHE_AB = 2          # "eine vertraute Person": Vertrauen mindestens 2
FREI_ANZAHL = 3


def _laden(pfad):
    st = os.path.getmtime(pfad)
    if _CACHE.get(pfad, (None,))[0] != st:
        _CACHE[pfad] = (st, json.load(open(pfad, encoding="utf-8")))
    return _CACHE[pfad][1]


def aktiv(moddir):
    return os.path.exists(os.path.join(moddir, "story.json"))


def story(moddir):
    return _laden(os.path.join(moddir, "story.json"))


def buehne(moddir):
    return _laden(os.path.join(moddir, "buehne.json"))


def regie(kern):
    """Regie-Notiz fuer das Sprachmodell: Verweise auf Datenfelder (fall.x, z_04 ...) raus."""
    t = re.sub(r"\s*\((?:[^()]*\bfall[._][^()]*|[a-z]_\d+[^()]*)\)", "", kern)
    return re.sub(r"\s{2,}", " ", t).strip()


def frauen(modul):
    return [p for p, x in modul["personen"].items() if x.get("romanzierbar")]


def partner(z, modul):
    """Die vertrauteste Frau (fuer Naehe-Szenen) oder None."""
    kand = [p for p in frauen(modul) if z["werte"].get("vertrauen." + p, 0) >= NAEHE_AB]
    if not kand:
        return None
    return max(kand, key=lambda p: (showrunner.nahe(z, p), z["werte"].get("begehren." + p, 0)))


def szene_bauen(z, modul, x, b):
    from . import ermittlung
    anwesend, will = [], dict(b.get("will") or {})
    besetzt = []
    for p in b.get("anwesend", []):
        if p.startswith("$fall"):                      # fallabhaengige Besetzung (B4), ohne Reihenfolge-Hinweis
            for q in ermittlung.besetzung(z, modul, p, x["id"]):
                if q not in anwesend and q in modul["personen"]:
                    anwesend.append(q)
                    besetzt.append(q)
            continue
        if p == "$naehe":
            q = partner(z, modul)
            if q:
                anwesend.append(q)
                if "*" in will:
                    will[q] = will.pop("*")
        elif p in modul["personen"]:
            anwesend.append(p)
    for q in besetzt:
        will.setdefault(q, will.get("*", "Get through this in your own way."))
    will.pop("*", None)
    ort = b.get("ort") or x.get("ort") or "crew_mess"
    if ort == "$spur":
        ort = (ermittlung.etwas_anders(z) or {}).get("ort") or "crew_mess"
    s = {"id": x["id"], "titel": x["titel"], "ort": ort, "anwesend": anwesend,
         "zeit": b.get("zeit", ""), "ausgangslage": b["ausgangslage"], "frage": b.get("frage", ""),
         "figuren": {p: {"will": w} for p, w in will.items() if p in anwesend},
         "ausgaenge": [], "max_zuege": b.get("max_zuege", 8), "regie": regie(x.get("kern", "")),
         "storylet": None, "improvisiert": True, "immer": copy.deepcopy(b.get("immer", [])), "hauptstory": True}
    if b.get("bild"):
        s["bild"] = b["bild"]                          # eigenes Szenenbild statt Raum-Hintergrund (z. B. Hubschrauber)
    if b.get("stimmung"):
        s["stimmung"] = copy.deepcopy(b["stimmung"])   # Stimmungsrahmen fuer den Richter (29.10.2026, kern/szene.richter)
    from . import abschluss
    dyn = abschluss.szenenbild(z, x["id"])             # vom Verlauf abhaengig (Auslaufen, Rauch im Technikraum)
    if dyn:
        s["bild"] = dyn
    if b.get("wahl"):
        s["wahlmoment"] = copy.deepcopy(b["wahl"])
        if s["wahlmoment"].pop("optionen_aus", None) == "anklage":        # Anhoerung Akt 1: Anwesende + niemand
            from . import anhoerung
            s["wahlmoment"]["optionen"] = anhoerung.anklage_optionen(z, modul, anwesend)
    if x.get("bedingung"):
        s["bedingung"] = x["bedingung"]
    if x["id"] in ("anhoerung_rolle", "anhoerung_urteil"):   # seit 26.10.2026 in der spielbaren Anhoerung entschieden
        s["bedingung"] = {"alle": [s["bedingung"], {"nicht": {"flag": "verhandlung_urteil"}}]} if s.get("bedingung") \
            else {"nicht": {"flag": "verhandlung_urteil"}}
    if x.get("exklusiv"):
        s["exklusiv"] = True
    return showrunner.figuren_fuellen(z, modul, {}, s)


def spielbar(z, modul, x, b):
    """Gehoert die Story-Szene in den Plan? (Buehnenfassung vorhanden, Naehe nur mit vertrauter Person)"""
    if not b:
        return False                                   # z. B. reine Ermittlungs-Aktion (B3) oder Gegenhandlungs-Folge (B4)
    if x.get("art") == "naehe" and not partner(z, modul):
        return False
    if x["id"] == "etwas_anders":                      # nur nach einer naechtlichen Gegenhandlung mit sichtbarer Spur
        from . import ermittlung
        return bool(ermittlung.etwas_anders(z))
    return True


def frei_phase(z, modul, ph, rng, bu, anzahl, heute=None):
    """Freie Phase: Zeit mit einer Person an ihrem Ort (Frauen zuerst, wer lange nicht dran war, dazu die Nebenfiguren
    aus rollen "freie_zeit_extra").
    Spieltest 29.10.2026 (318 Antworten bis Tag 15): Maxwell 4, Totò 2, Petru 0 gegen Chiara 57. Seitdem gehoert bei zwei
    oder mehr Karten in etwa jeder zweiten Phase die letzte der besten Nebenfigur (wer am laengsten nicht dran war),
    sonst und auf allen anderen Karten bleiben die Romanzen (bei nur einer Karte immer)."""
    kand = []
    for pid in dict.fromkeys(frauen(modul) + rollen.liste(modul, "freie_zeit_extra")):   # Lola ist beides: nur einmal
        if pid not in modul["personen"] or pid not in (z.get("bekannt") or modul["personen"]):
            continue
        pp = modul["personen"][pid]
        if (pp.get("von_bord_ab_tag") and z["tag"] >= pp["von_bord_ab_tag"]) or pp.get("weg_flag") in z.get("flags", []):
            continue                                    # Holm ab Tag 3 (evakuiert)
        ab = pp.get("ablauf") or {}
        ort = ab.get(ph, ab.get(regeln.phase_wie(ph), ab.get("*")))
        if ort not in modul["raeume"]:
            continue
        status, _ = regeln.zugang(modul["raeume"][ort], z, {"anwesend": [pid], "phase": ph})
        if status != "offen":
            continue
        gewicht = showrunner.tage_seit(z, pid) + rng.random() + (0.5 if pid in frauen(modul) else 0)
        gewicht += 3 if pp.get("frei_immer") else 0     # Ligeia: nur nachts da - dann immer eine Karte (29.10.2026)
        gewicht -= 3 * (heute or {}).get(pid, 0)        # heute schon angeboten: andere zuerst
        kand.append((gewicht, pid, ort))
    kand.sort(reverse=True)
    romanze = [k for k in kand if k[1] in frauen(modul)]
    neben = [k for k in kand if k[1] not in frauen(modul)]
    wurf = rng.random()
    immer = any(modul["personen"][k[1]].get("frei_immer") for k in neben)
    if anzahl >= 2 and neben and (wurf < 0.5 or immer):   # etwa jede zweite Phase: eine Karte fuer die Nebenfigur
        wahl = romanze[:anzahl - 1] + neben[:1]
    else:                                             # sonst wie bisher nur die Romanzen (Lola und Alva gehoeren dazu)
        wahl = romanze[:anzahl]
    wahl += [k for k in kand if k not in wahl][:anzahl - len(wahl)]          # zu wenige: auffuellen
    kand = sorted(wahl, reverse=True)
    out = []
    for nr, (_, pid, ort) in enumerate(kand[:anzahl]):
        if heute is not None:
            heute[pid] = heute.get(pid, 0) + 1
        p = modul["personen"][pid]
        n = p.get("kurz") or p["name"].split()[0]
        ortname = re.sub(r"\s*\([^)]*\)", "", modul["raeume"][ort]["label"]).strip()
        # Eigennamen ("Alva's bar") ohne "the" und gross, sonst "the sun deck" (Spieltest 28.10.2026: "the alva's bar")
        ortname = ortname if "'s " in ortname.split(" ", 1)[0] + " " else "the " + ortname[0].lower() + ortname[1:]
        vorlage = bu["frei"][ph]
        n_satz = n[0].upper() + n[1:]                  # "the Siren" am Satzanfang (29.10.2026)
        if isinstance(vorlage, list):                  # mehrere Fassungen: die Karten einer Phase nie gleich
            vorlage = vorlage[(nr + z["tag"]) % len(vorlage)]
        s = {"id": "frei_%s_t%d_%s" % (pid, z["tag"], ph), "titel": "Time with %s" % n, "ort": ort, "anwesend": [pid],
             "zeit": "", "ausgangslage": vorlage.format(name=n_satz, ort=ortname),
             "frage": "What does Duc do with this time?", "figuren": {pid: {"will": "Spend some time with Duc in %s "
                                                                              "own way." % ("his" if p.get("pronomen") == "er"
                                                                                            else "her")}},
             "ausgaenge": [], "max_zuege": 8, "storylet": None, "improvisiert": True, "frei": True}
        out.append(showrunner.figuren_fuellen(z, modul, {}, s))
    return out


def plan_bauen(z, modul, moddir):
    st, bu = story(moddir), buehne(moddir)
    tag = z["tag"]
    d = st["wochenbogen"].get(str(tag)) or {"titel": "", "phasen": {}}
    rng = random.Random("%s-%d-haupt" % (z["id"], tag))
    wetter, ende = showrunner.tagesende(z, {"sturm_tag": st.get("sturm_tag", 3)}, rng)
    # Strom gibt es seit 30.10.2026 nicht mehr (vorher seit 26.10. verborgen): keine Strom-Regeln, keine Katastrophen-Uhr
    ende = [r for r in ende if "strom" not in str(r) and r.get("uhr") != "katastrophe"]
    p = {"_showrunner": "hauptstory (kern/hauptstory.py)", "_hauptstory": True, "_moddir": moddir, "tag": tag,
         "wetter": wetter, "wetter_text": "", "spannung": d.get("titel", ""),
         "spannung_spieler": "Day %d: %s" % (tag, d.get("titel", "")), "tagesende": ende, "phasen": {}}
    zr = modul["zeitraster"]
    story_phasen = [ph for ph in zr["phasen"] if d["phasen"].get(ph)]
    erste = story_phasen[0] if tag == 1 and story_phasen else zr["phasen"][0]      # Tag 1 beginnt am Abend
    heute = {}
    from . import ereignisse
    for ph in zr["phasen"][zr["phasen"].index(erste):]:
        defs = list(d["phasen"].get(ph, []))
        if ph == "fruehstueck" and tag >= 3 and not ereignisse.gesperrt_durch_story(dict(z, tag=tag), modul, ph) and not any(x["id"] == "etwas_anders" for x in defs):
            defs.insert(0, {"id": "etwas_anders", "titel": "Etwas ist anders", "art": "fix", "kern": "",
                            "uebergang": True})
        spiel = [x for x in defs if spielbar(z, modul, x, bu["szenen"].get(x["id"]))]
        szenen = [szene_bauen(z, modul, x, bu["szenen"].get(x["id"])) for x in spiel]
        if szenen and all(x.get("uebergang") for x in spiel) and ph in zr["wahl"] + zr["pflicht"]:
            # Modell B (24.10.2026): nur kurze Uebergaenge -> sie laufen als Vorspiel, danach ist die Phase frei
            anzahl = 1 if ph in zr["pflicht"] else FREI_ANZAHL
            frei = frei_phase(z, modul, ph, rng, bu, anzahl, heute)
            p["phasen"][ph] = {"szenen": szenen + frei, "vorspiel": [s["id"] for s in szenen], "frei": True}
        elif szenen:
            p["phasen"][ph] = {"szenen": szenen, "folge": True,
                               "fix": any(s.get("exklusiv") for s in szenen) or None}
        elif d.get("nur_story"):                       # Tag 1 (Antibes, Ueberfahrt, Party): keine freie Zeit -
            continue                                   # Phase fehlt im Plan, laeuft als "leer" (Prolog-Events davor)
        else:
            anzahl = 1 if ph in zr["pflicht"] else FREI_ANZAHL
            p["phasen"][ph] = {"szenen": frei_phase(z, modul, ph, rng, bu, anzahl, heute), "frei": True}
    p["erste_phase"] = erste
    return p

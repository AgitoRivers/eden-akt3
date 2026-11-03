# -*- coding: utf-8 -*-
"""Gesten, Zeit zusammen, Intim-Bereich (16.10.2026) - die Dating-Sim-Steuerung neben dem Textfeld.

Regeln im Code, das Modell erzaehlt:
  - Eine Geste ist Ducs Zug (kostet einen Zug der Sanduhr). Probe auf ein Attribut; Lieblingsgesten +2.
  - klein: gelingt -> +4 Punkte (nur bis Stufe 3, wie Gespraeche). gross: gelingt -> Erlebnis (+1 Stufe = 8 Punkte),
    hoechstens eine grosse Geste je Frau und Tag. Misslingt eine grosse Geste ab Tag 2: -4 Vertrauen, Chronik.
  - Dieselbe Geste zweimal in einer Szene bei derselben Frau wirkt nicht mehr (abgenutzt).
  - Schwellen (Stufen) und Privatsphaere sperren Gesten sichtbar - mit Grund.
  - Momente (Kuss, Gestaendnis, Versprechen ...) landen in der Chronik; wer dabei ist, weiss es.
  - Einladung angenommen -> Verabredung: der Spielleiter garantiert die naechste Abend-Szene mit ihr. Den Ort waehlt
    Duc in der Karte im Handy (17.10.2026, eden.verabredung_ort); ihr Lieblingsort bringt einen kleinen Bonus.
  - Zeit zusammen: SIE schlaegt in ihrer Art etwas vor (Modell), eingeordnet in eine feste Kategorie; die Wirkung
    am Szenenende haengt im Code an der Kategorie (Arbeit / Entspannung / Abenteuer / Romantik).
  - Intim: Akte und Stellungen aus Ducs ST-Weltbuechern, gestaffelt nach Begehren; ihre Vorlieben (mag / nein)."""
import json, os, random, re

from . import chronik, figurenrahmen, llm, rollen, zustand

KATEGORIEN = ["arbeit", "entspannung", "abenteuer", "romantik"]
KAT_DE = {"arbeit": "Arbeit", "entspannung": "Entspannung", "abenteuer": "Abenteuer", "romantik": "Romantik"}
LIEBLING_BONUS = 2
KLEIN_PUNKTE = 4
PATZER_PUNKTE = -4
PRIVAT_AB = 4
WELTBUECHER = ("main_Sexual position lore book_world_info.json", "main_Sex Acts_world_info.json")
_BUCH = {}


def gesten(modul):
    return {g["id"]: g for g in modul.get("gesten", [])}


def frauen_da(modul, sz):
    out = [p for p in sz.get("figuren", []) if modul["personen"].get(p, {}).get("romanzierbar")]
    nacht = sz.get("intim_aktiv")                # Jana, Megan: nicht romanzierbar, aber ihr Intim-Abend (27.10.2026)
    if nacht and nacht in sz.get("figuren", []) and nacht not in out:
        out.append(nacht)
    return out


def privat(modul, sz, pid):
    andere = [p for p in sz.get("figuren", []) if p not in (pid, "erzaehler")]
    stufe = max(modul["raeume"].get(sz["def"]["ort"], {}).get("privat", 1), sz.get("privat_stufe", 0))   # gewaehlter Ort (kern/orte.py)
    return not andere and not sz.get("intim_gesperrt") and stufe >= PRIVAT_AB


def liebling(modul, pid, gid):
    return gid in (modul.get("lieblingsgesten") or {}).get(pid, [])


def kurz(modul, pid):
    p = modul["personen"][pid]
    return p.get("kurz") or p["name"].split()[0]


def chance(z, modul, attr, sg, bonus):
    from . import charms
    w = z["persona"]["attribute"].get(attr, 0) + charms.attribut(z, attr) + bonus
    return max(5, min(95, round((21 - (sg - w)) * 5)))


def gesperrt(z, modul, sz, g, pid):
    """-> Grund (deutsch) oder None."""
    for achse, min_stufe in (g.get("schwelle") or {}).items():
        if z["werte"].get("%s.%s" % (achse, pid), 0) < min_stufe:
            return "%s %d+" % ("Trust" if achse == "vertrauen" else "Desire", min_stufe)
    if g.get("verabredung") and any(v["tag"] == date_tag(z) for v in z.get("verabredungen") or []):
        return "you already have a date that evening"
    if g.get("privat") and not privat(modul, sz, pid):
        return "only when you are alone together, in a private room"
    if g["bereich"] in ("intim",) and rollen.vergeben(z, modul, pid):
        return rollen.vergeben(z, modul, pid)
    if g["id"] == "privat_gehen":
        if [p for p in sz.get("figuren", []) if p not in (pid, "erzaehler")]:
            return "only when you are alone together"
        if privat(modul, sz, pid):
            return "you are already somewhere private"
    if g["art"] == "gross" and z.setdefault("grosse_geste", {}).get(pid) == z["tag"]:
        return "you already had a big moment with her today"
    if g["id"] == "kuessen" and any(e.get("moment") == "kiss" and pid in e["wer"] for e in chronik.liste(z)):
        return None                                      # nach dem ersten Kuss: kein grosser Moment mehr, s. ausfuehren
    return None


# ------------------------------------------------------------------ Ansicht
def ansicht(z, modul, sz):
    if not sz or sz.get("wahlmoment_offen"):
        return None
    frauen = frauen_da(modul, sz)
    if not frauen:
        return None
    G = gesten(modul)
    genutzt = set(sz.get("gesten_genutzt", []))
    liste = []
    for g in G.values():
        je = {}
        for pid in frauen:
            bonus = LIEBLING_BONUS if liebling(modul, pid, g["id"]) else 0
            je[pid] = {"gesperrt": gesperrt(z, modul, sz, g, pid), "liebling": bool(bonus),
                       "abgenutzt": "%s:%s" % (g["id"], pid) in genutzt,
                       "chance": chance(z, modul, g["attribut"], g["sg"], bonus)}
            if g["id"] == "privat_gehen":
                from . import orte
                je[pid]["orte"] = [dict(o, chance=chance(z, modul, g["attribut"], g["sg"], bonus + sum(b for _, b in orte.bonus(z, modul, sz, pid, o["id"]))))
                                   for o in orte.wahl(z, modul, sz, pid)]
        liste.append({"id": g["id"], "bereich": g["bereich"], "label": g["label"], "gross": g["art"] == "gross",
                      "attribut": g["attribut"], "je": je})
    intim = None
    if sz.get("intim_aktiv") in frauen or any(privat(modul, sz, p) and z["werte"].get("begehren." + p, 0) >= 3
                                              for p in frauen):
        intim = intim_liste(z, modul, sz, frauen)
    angebot = sz.get("zeit_angebot")
    return {"frauen": [{"id": p, "name": kurz(modul, p)} for p in frauen], "liste": liste,
            "zeit": {p: {"liebling": liebling(modul, p, "zeit"), "frei": "zeit:%s" % p not in genutzt} for p in frauen},
            "zeit_angebot": {"an": angebot["pid"], "text": angebot["text"], "kategorie": KAT_DE[angebot["kategorie"]]}
            if angebot and not angebot.get("beantwortet") else None,
            "intim": intim, "intim_aktiv": sz.get("intim_aktiv")}


def intim_liste(z, modul, sz, frauen):
    buch = weltbuch(z)
    out = []
    stufen = modul.get("intim_stufen") or {}
    for pid in frauen:
        if not privat(modul, sz, pid):
            continue
        b = z["werte"].get("begehren." + pid, 0)
        if sz.get("intim_aktiv") == pid:
            b = max(b, 3)                        # ihr Abend: mindestens Stufe 3 (auch ohne Begehren-Achse)
        vorl = (modul.get("intim_vorlieben") or {}).get(pid, {})
        frei = [t for s, tags in stufen.items() if b >= int(s) for t in tags]
        if sz.get("intim_aktiv") == pid and b >= 5:
            frei += sorted(t for t in buch if t.startswith("Position:"))
        for t in frei:
            if t not in buch:
                continue
            out.append({"an": pid, "tag": t, "name": t.split(": ", 1)[1],
                        "gruppe": "Stellung" if t.startswith("Position:") else "Akt",
                        "mag": t in vorl.get("mag", []), "nein": t in vorl.get("nein", [])})
    return out


# ------------------------------------------------------------------ Ausfuehren
def ausfuehren(z, modul, gid, pid, probe_fn, zug_fn, ort=None):
    """Geste spielen. probe_fn(att, sg, extra_boni) -> Probe; zug_fn(text, probe, hinweis) -> vorbei.
    -> (vorbei, zeilen)."""
    sz = z["szene"]
    G = gesten(modul)
    if gid not in G or pid not in frauen_da(modul, sz):
        raise ValueError("Diese Geste geht gerade nicht.")
    g = G[gid]
    grund = gesperrt(z, modul, sz, g, pid)
    if grund:
        raise ValueError("%s: %s." % (g["label"], grund))
    name = kurz(modul, pid)
    schluessel = "%s:%s" % (gid, pid)
    abgenutzt = schluessel in sz.setdefault("gesten_genutzt", [])
    sz["gesten_genutzt"].append(schluessel)
    extra = [("Mag sie", LIEBLING_BONUS)] if liebling(modul, pid, gid) else []
    if gid == "privat_gehen":
        from . import orte
        moeglich = [o["id"] for o in orte.wahl(z, modul, sz, pid)]
        ort = ort or (orte.STANDARD if orte.STANDARD in moeglich else (moeglich or [None])[0])
        if ort not in moeglich:
            raise ValueError("You can't go there right now.")
        extra += orte.bonus(z, modul, sz, pid, ort)
    vorteil_item = next((i for i in g.get("vorteil_items", []) if i in z["inventar"]), None)
    if vorteil_item:
        extra.append((modul["items"][vorteil_item]["label"], 2))
    p = probe_fn(g["attribut"], g["sg"], extra)
    ok = p["ergebnis"] in ("erfolg", "kritisch")
    gross = g["art"] == "gross"
    if gid == "kuessen" and any(e.get("moment") == "kiss" and pid in e["wer"] for e in chronik.liste(z)):
        gross = False                                      # erster Kuss = grosser Moment, danach eine Zaertlichkeit
    zeilen = ["Gesture: %s – %s" % (g["label"], "it lands" if ok else "it doesn't land")]
    if abgenutzt:
        zeilen.append("no effect any more – you already tried that")
    elif ok:
        if gross:
            z.setdefault("grosse_geste", {})[pid] = z["tag"]
            zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "%s.%s" % (a, pid), "delta": 1} for a in g["achse"]], frei=False, quelle="szenen")
        else:
            for a in g["achse"]:
                zeilen += zustand.punkte_add(z, modul, "%s.%s" % (a, pid), KLEIN_PUNKTE, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
        moment = g.get("moment")
        if gid == "entschuldigen" and any(e.get("moment") == "fight" and pid in e["wer"] and chronik.gueltig(z, e)
                                          for e in chronik.liste(z)):
            moment = "apology"
        if moment and moment in chronik.MOMENTE:
            satz, wichtig, dauer = chronik.MOMENTE[moment]
            chronik.eintragen(z, modul, "moment", satz.format(n=name), wer=[pid], wichtig=wichtig, dauer=dauer,
                              moment=moment)
        if g.get("verabredung"):
            verabreden(z, modul, pid)
            zeilen.append(("📅 Date with %s tonight" % name if z["phase"] in ("fruehstueck", "tag", "nachmittag", "dinner")
                           else "📅 Date with %s tomorrow evening" % name) + " – pick the place on the map")
        if g.get("intim_aktiv"):
            sz["intim_aktiv"] = pid
    elif gross and z["tag"] > 1:
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, PATZER_PUNKTE)
        chronik.eintragen(z, modul, "moment", "%s turned Duc down when he tried: %s" % (name, g["label"].lower()),
                          wer=[pid], wichtig=2, dauer=1, moment="rebuff")
    if gid == "privat_gehen":
        if ok and not abgenutzt:
            from . import orte, szene
            raum_wechseln(z, modul, sz, ort, "You and %s slip away to %s." % (name, orte.label(modul, ort)))
            sz["privat_stufe"] = orte.PRIVAT_STUFE
            zeilen += orte.ankommen(z, modul, sz, pid, ort, lambda p, t, g: szene.zeile_einfuegen(z, modul, sz, p, t, g))
        elif not ok:
            from . import figurenrahmen, szene
            satz = figurenrahmen.absage_text(z, modul, pid, "privat")
            if satz:                                       # feste Absage: das Modell weicht ein Nein sonst auf (LLM-Vergleich 02.11.)
                szene.zeile_einfuegen(z, modul, sz, pid, satz, "neutral")
                sz.setdefault("regie_nein", {})[pid] = 2
                return False, zeilen
    vorbei = zug_fn(g["handlung"].format(n=name), p, "")
    return vorbei, zeilen


PRIVAT_RAUM = "duc_cabin"


def raum_wechseln(z, modul, sz, ort, satz):
    """Die Szene geht an einem anderen Ort weiter (Go somewhere private): Ort, Bild, eine Zeile im Log."""
    from . import buehne
    sz["def"]["ort"] = ort
    sz["bild"] = buehne.szenenbild(modul, dict(sz["def"], bild=None), z["phase"])
    sz["log"].append({"art": "ereignis", "text": satz})


def date_tag(z):
    """An welchem Abend eine Einladung gerade gelten wuerde: heute vor dem Abend, sonst morgen."""
    return z["tag"] if z["phase"] in ("fruehstueck", "tag", "nachmittag", "dinner") else z["tag"] + 1


def verabreden(z, modul, pid):
    z.setdefault("verabredungen", []).append({"pid": pid, "tag": date_tag(z), "phase": "abend"})


# ------------------------------------------------------------------ Zeit zusammen
ZEIT_SYS = ("You write one short line for a character in a story game. She proposes, in her own voice and manner, ONE "
            "concrete thing she and Duc could do together right now. Then you classify it.")
# Live-Spieltest 31.10.2026: Der Vorschlag kannte die Szene nicht und lief mit Temperatur 0. Nach einem intimen Moment
# kam wortgleich "You're late, Officer ... recalibrate the sensors". Jetzt: letzte Zeilen, eigene Vorschlaege, etwas Zufall.
ZEIT_SAMPLER = {"temperature": 0.9}
ZEIT_ZEILEN = 6                 # so viele letzte Zeilen der Szene
ZEIT_GEDAECHTNIS = 5            # so viele ihrer letzten Vorschlaege, ueber Szenen hinweg


def szene_bisher(sz):
    """Die letzten Zeilen der laufenden Szene als Text fuer den Prompt."""
    zeilen = []
    for e in sz.get("log", []):
        text = (e.get("gezeigt") or e.get("text") or "").strip()
        if text and e.get("art") in ("start", "duc", "figur"):
            wer = "Duc" if e["art"] == "duc" else e.get("name") or "Scene"
            zeilen.append("- %s: %s" % (wer, text[:400]))
    return "\n".join(zeilen[-ZEIT_ZEILEN:])


def zeit_vorschlag(z, modul, pid, figur_prompt):
    """SIE schlaegt etwas vor - passend zu Ort, Zeit, ihr und dem, was gerade war. -> Eintrag fuer das Szenen-Log (ihre Zeile)."""
    sz = z["szene"]
    if pid not in frauen_da(modul, sz):
        raise ValueError("Sie ist nicht in dieser Szene.")
    if "zeit:%s" % pid in sz.setdefault("gesten_genutzt", []):
        raise ValueError("Ihr habt in dieser Szene schon etwas zusammen gemacht.")
    sz["gesten_genutzt"].append("zeit:%s" % pid)
    raum = modul["raeume"][sz["def"]["ort"]]["label"]
    gram = ('root ::= "{" ws "\\"line\\":" ws s "," ws "\\"category\\":" ws k ws "}"\n'
            's ::= "\\"" [^"\\n]+ "\\""\n'
            'k ::= ' + " | ".join('"\\"%s\\""' % k for k in KATEGORIEN) + '\nws ::= [ \\t\\n]*')
    nah = sz.get("intim_zuletzt") == pid
    if figurenrahmen.gilt(modul, pid):              # Vorschlag und Kategorie aus den Daten, das Modell entscheidet nichts
        text, kat = figurenrahmen.vorschlag(z, modul, pid, nah)
        sz["zeit_angebot"] = {"pid": pid, "text": text, "kategorie": kat}
        return text, kat
    frueher = z.setdefault("zeit_vorschlaege", {}).setdefault(pid, [])
    kontext = ""
    bisher = szene_bisher(sz)
    if bisher:
        kontext += ("\n\nThe scene so far (latest last):\n%s\nHer line must follow from this. She does not ignore what "
                    "was just said or done." % bisher)
    if nah:
        kontext += ("\n\nThey have just been intimate and the moment is still in the air. She does not act as if nothing "
                    "happened and does not change the subject to work or chores. She proposes what comes next from this "
                    "moment.")
    if frueher:
        kontext += ("\n\nProposals she made lately. Do not repeat them, their activity or their opening words:\n%s"
                    % "\n".join("- " + f for f in frueher))
    user = ("%s\n\nRight now: %s, %s, day %d. Duc wants to spend some time with %s.%s\nWrite %s's line: she proposes one "
            "concrete activity for the two of them that fits this place, this time of day and who she is (work on "
            "something together, relax, explore, or something romantic). Spoken words in \"double quotes\" are not "
            "allowed inside the JSON string - use single quotes. One or two sentences.\ncategory: arbeit = work or "
            "repairs together, entspannung = relaxing, coffee, games, abenteuer = exploring, swimming, diving, "
            "romantik = romantic.\nJSON: {\"line\": \"...\", \"category\": \"...\"}" % (
                figur_prompt, raum, sz["def"].get("zeit", z["phase"]), z["tag"], kurz(modul, pid), kontext, kurz(modul, pid)))
    d, _ = llm.json_chat(ZEIT_SYS, user, gram, max_tokens=120, sampler=ZEIT_SAMPLER)
    d = d or {}
    text = (d.get("line") or "").strip()
    if text:
        frueher[:] = (frueher + [text[:160]])[-ZEIT_GEDAECHTNIS:]
    else:
        text = "'Stay a while. Right here, with me.'" if nah else "'Come on. Let's get some air, you and me.'"
    kat = "romantik" if nah else d.get("category") if d.get("category") in KATEGORIEN else "entspannung"
    sz["zeit_angebot"] = {"pid": pid, "text": text, "kategorie": kat}
    return text, kat


def zeit_antwort(z, modul, ja, zug_fn):
    sz = z["szene"]
    a = sz.get("zeit_angebot")
    if not a or a.get("beantwortet"):
        raise ValueError("Es liegt gerade kein Vorschlag vor.")
    a["beantwortet"] = True
    name = kurz(modul, a["pid"])
    if ja:
        sz["zeit_aktiv"] = {"pid": a["pid"], "kategorie": a["kategorie"], "text": a["text"]}
        hinweis = ("[Now] They are doing this together, as %s proposed: %s Play the activity itself - concrete, in "
                   "the moment.\n\n" % (name, a["text"]))
        return zug_fn('He grins. "Let\'s do it."', None, hinweis)
    return zug_fn('He shakes his head. "Not now - another time."', None, "")


def zeit_auswerten(z, modul, sz):
    """Am Szenenende: Wirkung der gemeinsamen Zeit nach Kategorie (im Code)."""
    a = sz.get("zeit_aktiv")
    if not a:
        return []
    pid, kat, name = a["pid"], a["kategorie"], kurz(modul, a["pid"])
    zeilen = ["Zeit zusammen mit %s: %s" % (name, KAT_DE[kat])]
    if kat == "romantik":
        if z.setdefault("romantik_tag", {}).get(pid) != z["tag"]:
            z["romantik_tag"][pid] = z["tag"]
            zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "begehren." + pid, "delta": 1}], frei=False, quelle="szenen")
        else:
            zeilen += zustand.punkte_add(z, modul, "begehren." + pid, KLEIN_PUNKTE, deckel=zustand.GESPRAECH_DECKEL, quelle="szenen")
    else:
        zeilen += zustand.punkte_add(z, modul, "vertrauen." + pid, 6, quelle="szenen")
        if kat == "arbeit":
            technik = rollen.person(modul, pid, "technik") or sz["def"]["ort"] in ("power_room", "generator_room", "workshop")
            zeilen += zustand.folgen_anwenden(z, modul, [{"uhr": "reparatur", "delta": 1}] if technik   # sonst Moral
                                              else [{"wert": "moral", "delta": 1, "moral_art": "alltag"}])  # (bis 30.10. Strom)
        elif kat == "entspannung":
            zeilen += zustand.folgen_anwenden(z, modul, [{"wert": "energie", "delta": 1},
                                                         {"wert": "moral", "delta": 1, "moral_art": "alltag"}])
        elif kat == "abenteuer" and random.Random("%s-%d-%s" % (z["id"], z["tag"], pid)).random() < 0.4:
            fund = {"geld": 50, "text": "Found while exploring"}      # bis 30.10.2026 auch Diesel
            zeilen += zustand.folgen_anwenden(z, modul, [fund])
    chronik.eintragen(z, modul, "zeit", "Duc and %s spent time together (%s): %s" % (name, kat, a["text"][:140]),
                      wer=[pid], wichtig=2 if kat == "romantik" else 1)
    return zeilen


# ------------------------------------------------------------------ Intim (ST-Weltbuecher)
def weltbuch(z):
    """{"Position: Cowgirl": content, ...} aus Ducs ST-Weltbuechern (Pfad aus der Engine-Konfiguration)."""
    if _BUCH:
        return _BUCH
    try:
        cfg = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "eden-config.json"),
                             encoding="utf-8"))
        for f in WELTBUECHER:
            d = json.load(open(os.path.join(cfg["st_daten"], "worlds", f), encoding="utf-8"))
            for e in d.get("entries", {}).values():
                if e.get("comment") and e.get("content"):
                    _BUCH[e["comment"]] = e["content"]
    except Exception:
        pass
    return _BUCH


def makros(text, name, rng):
    text = re.sub(r"\{\{random:\s*([^}]*)\}\}", lambda m: rng.choice([x.strip() for x in m.group(1).split(",") if x.strip()]
                                                                     or [""]), text)
    return text.replace("{{char}}", name).replace("{{user}}", "Duc")


def naehe_kennung(modul, tag):
    """Welcher Chronik-Eintrag zu einer intimen Aktion gehoert. "slept together" gilt erst bei Stellungen und Anal."""
    if tag.startswith("Position:") or tag == "Act: Anal":
        return "intimate"
    return "naehe" if tag in (modul.get("intim_stufen") or {}).get("3", []) else "naehe_weit"


def intim(z, modul, tag, pid, zug_fn):
    sz = z["szene"]
    frei = {(x["an"], x["tag"]): x for x in (intim_liste(z, modul, sz, frauen_da(modul, sz)) or [])}
    name = kurz(modul, pid)
    if tag == "__sie__":
        if not privat(modul, sz, pid):
            raise ValueError("Nur unter vier Augen in einem privaten Raum.")
        sz["intim_zuletzt"] = pid
        chronik.naehe_eintragen(z, modul, pid, "naehe")
        return zug_fn("He lets %s take the lead." % name, None,
                      "[She leads] %s decides what happens next and takes the lead - she picks what she likes most, "
                      "within her limit.\n\n" % name)
    x = frei.get((pid, tag))
    if not x:
        raise ValueError("Das ist gerade nicht freigeschaltet.")
    anweisung = makros(weltbuch(z)[tag], name, random.Random())
    if x["nein"]:
        hinweis = ("[She does not want this] %s does not want '%s'. She refuses in character, without killing the mood, "
                   "and steers to something she likes instead.\n\n" % (name, x["name"]))
    else:
        sz["intim_zuletzt"] = pid
        chronik.naehe_eintragen(z, modul, pid, naehe_kennung(modul, tag))
        hinweis = ("[Scene direction] %s\n%s\n\n" % (anweisung, "She loves this and is eager." if x["mag"]
                                                    else "She goes along with it if it feels right to her."))
    verb = "suggests" if x["gruppe"] == "Stellung" else "wants"
    return zug_fn("He %s: %s." % (verb, x["name"].lower()), None, hinweis)

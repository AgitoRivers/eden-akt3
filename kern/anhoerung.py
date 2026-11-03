# -*- coding: utf-8 -*-
"""Die Anhoerung am Ende von Akt 1 (Scheibe 3, Nacht 24.10.2026) - Logik ohne eigene Oberflaeche.

Duc 22.10.: Megan urteilt an Bord. Ablauf Anklage -> zwei Zeugen -> Einspruch mit Beweis -> Wahrheit -> Ducs eigene
Rolle -> Plaedoyer -> Urteil. Alle fuenf Team-Verbesserungen:
  (1) jeder logisch passende Beweis zaehlt; Megans Geduld (3 Adern) bestraft nur Raten
  (2) Zeugen haben eigene Loyalitaet und koennen luegen, um jemanden zu schuetzen
  (3) Plaedoyer Gnade erbitten / Schuld teilen / Strafe fordern; der Code prueft, ob Erbarmen moeglich ist
      (richtige Person, volle Kette, Motiv bekannt, Duc ehrlich ueber die eigene Rolle, Geduld nicht aufgebraucht)
  (4) Entschuldigung an zu Unrecht Verdaechtigte (danach ueber die bestehende Korrektur, ermittlung.konfrontieren)
  (5) die Anhoerung findet immer statt, auch mit leeren Haenden - dann urteilt Megan selbst

Gespielt wird sie mit den vorhandenen Mitteln: drei Story-Szenen am Tag 7 mit je einem Wahlmoment
(anhoerung = Anklage, anhoerung_rolle, anhoerung_urteil = Plaedoyer). Die Optionen tragen "anhoerung": {...};
szene.waehlen ruft dann waehlen() hier auf. Zeugen und Einsprueche wertet der Code aus dem aus, was Duc belegt hat
(Duc erhebt einen Einspruch genau dann, wenn er den passenden Beweis kennt - kein Raten, keine Ader).
Ergebnis in ermittlung.stand(z)["anhoerung"] und ["urteil"]; das Ende von Akt 1 liest es (kern/abschluss.py).

Urteile: erbarmen · aufgeklaert · unbelegt (richtige Person ohne Kette) · falsch (Unschuldige angeklagt) ·
offen (kein Name) · entlastet (Fall ohne Verantwortliche: "niemand allein" mit Kette)."""
import json, os, random

from . import charms, ermittlung, moral

ADERN = 3
NIEMAND = "niemand"


def _name(modul, pid):
    p = modul["personen"].get(pid, {})
    return p.get("kurz") or p.get("name", pid).split(" ")[0]


def _daten(z):
    return (ermittlung._story(z) or {}).get("anhoerung") or {}


def stand(z):
    return ermittlung.stand(z).setdefault("anhoerung", {})


# ------------------------------------------------------------------ Bausteine
def belegt(z):
    """Volle Kette - ein Gestaendnis ersetzt ein Glied (ermittlung.glieder_status). Nach der spielbaren Verhandlung
    (Variante B) zaehlt, was Duc vor Megan durchgebracht hat: jede Runde mit Beweis oder gelungenem Bluff."""
    r = stand(z).get("runden")
    if r:
        return all(x in ("beweis", "bluff", "gestaendnis") for x in r.values())
    return ermittlung.kette_bekannt(z)


def ohne_bluff(z):
    """Erbarmen braucht echte Beweise - ein Bluff traegt das Urteil, aber keine Gnade."""
    return "bluff" not in (stand(z).get("runden") or {}).values()


def motiv_bekannt(z, pid):
    """Duc weiss, warum: Gestaendnis oder so viel Vertrauen, dass sie es ihm erzaehlt hat (Vertrauen 3)."""
    return bool(ermittlung.stand(z).get("gestaendnis")) or z["werte"].get("vertrauen." + pid, 0) >= 3


def _falsch_offen(z, ausser=None):
    v = (ermittlung.fall(z) or {}).get("verantwortlich")
    return [x["pid"] for x in ermittlung.stand(z)["vorwuerfe"]
            if x["oeffentlich"] and x["pid"] != v and not x.get("korrigiert") and x["pid"] != ausser]


def an_bord(z, modul, pid):
    """Ist die Person am Tag der Anhoerung an Bord? (Holm wird an Tag 2 evakuiert: von_bord_ab_tag / weg_flag)"""
    p = modul["personen"].get(pid) or {}
    if p.get("von_bord_ab_tag") and z["tag"] >= p["von_bord_ab_tag"]:
        return False
    return not (p.get("weg_flag") and p["weg_flag"] in z.get("flags", []))


def zeugen(z, modul, angeklagt):
    """Zwei Zeugen, vorher erspielt: wer Duc etwas Bekanntes ueber die Nacht gesagt hat, die vertrautesten zuerst.
    Dazu, wenn es sie gibt, eine Person, die zur Angeklagten haelt (Loyalitaet) - sie besteht darauf auszusagen."""
    F, bek = ermittlung.fakten(z), ermittlung.stand(z)["bekannt"]
    loyal = (_daten(z).get("loyal") or {}).get(angeklagt or "", [])
    sprecher = {}
    for fid in bek:
        f = F.get(fid) or {}
        p = f.get("quelle")
        if fid.startswith("z_"):
            continue                                   # Hinweise auf Akt 3 sind keine Zeugenaussagen
        if f.get("art") in ("aussage", "beobachtung") and p in modul["personen"] and p not in (angeklagt, "megan"):
            sprecher.setdefault(p, []).append(fid)
    liste = sorted(sprecher, key=lambda p: (-z["werte"].get("vertrauen." + p, 0), p))
    wahl = [p for p in loyal if p in modul["personen"] and p != angeklagt][:1]
    wahl += [p for p in liste if p not in wahl][:2 - len(wahl)]
    v = (ermittlung.fall(z) or {}).get("verantwortlich")
    out = []
    for p in wahl:
        luegt = p in loyal and angeklagt == v and z["werte"].get("vertrauen." + p, 0) < 3
        out.append({"pid": p, "fakten": sprecher.get(p, []), "loyal": p in loyal, "luegt": luegt,
                    # Einspruch mit Beweis: das Glied "person" ist belegt -> das Alibi faellt
                    "entlarvt": luegt and any(g["id"] == "person" and g["belegt"]
                                              for g in ermittlung.glieder_status(z))})
    return out


def adern(z, angeklagt, modul=None):
    """Megans Geduld: 3 Adern, nur Raten kostet. Raten = Anklage ohne belegte Kette, offene oeffentliche falsche
    Vorwuerfe aus der Woche, Megans Haltung im Minus (sie hat Duc schon beim Raten erlebt)."""
    a, gruende = ADERN, []
    if "tag0_megan_herzlich" in z["flags"]:            # Tag 0 (E-019): Megan erinnert sich an Antibes
        a += 1
        gruende.append("Megan erinnert sich an Antibes")
    elif "tag0_megan_frech" in z["flags"]:
        a -= 1
        gruende.append("Megan erinnert sich an Antibes")
    if ermittlung.megan_haltung(z) < 0:
        a -= 1
        gruende.append("Megan traut Duc nach dieser Woche wenig zu")
    g = moral.geduld(z, modul) if modul else None                       # Crew-Stimmung (27.10.2026): Buzzing +1, ab Tense -1
    if g:
        a += g[0]
        gruende.append(g[1])
    if _falsch_offen(z, ausser=angeklagt):
        a -= 1
        gruende.append("offene öffentliche Vorwürfe ohne Beleg")
    if angeklagt and not belegt(z):
        a -= 1
        gruende.append("Anklage ohne lückenlose Kette")
    return max(0, a), gruende


ANTIBES = {"tag0_megan_herzlich": "You were kind in Antibes, Duc. I remember. Don't make me regret it.",
           "tag0_megan_frech": "You yelled your way in here in Antibes. Let's see you talk your way out.",
           "tag0_megan_flirt": "And I will be harder on you than on anyone. You know why.",
           "tag0_megan_foermlich": "You were always the professional one. Prove it."}


def antibes_satz(z):
    """Megans Satz zu Beginn der Anhoerung - je nach Chip an Tag 0 (verborgen bis hier)."""
    return next((s for f, s in ANTIBES.items() if f in z["flags"]), "")


def erbarmen_moeglich(z):
    """(3) Erbarmen nur bei richtiger Person, voller Kette, bekanntem Motiv, Ehrlichkeit ueber Ducs Rolle, Geduld > 0."""
    a = stand(z)
    v = (ermittlung.fall(z) or {}).get("verantwortlich")
    fehlt = []
    if not v or a.get("angeklagt") != v:
        fehlt.append("richtige Person")
    if not belegt(z):
        fehlt.append("volle Kette")
    elif not ohne_bluff(z):
        fehlt.append("Beweise statt Bluff")
    if v and not motiv_bekannt(z, v):
        fehlt.append("Motiv")
    if not a.get("rolle_ehrlich"):
        fehlt.append("Ducs Ehrlichkeit")
    if a.get("adern", ADERN) <= 0:
        fehlt.append("Megans Geduld")
    return not fehlt, fehlt


def urteil(z, plaedoyer):
    a = stand(z)
    pid = a.get("angeklagt")
    v = (ermittlung.fall(z) or {}).get("verantwortlich")
    if pid is None:
        return "offen"
    if pid == NIEMAND:
        return "entlastet" if v is None and belegt(z) else "offen"
    if pid != v:
        return "falsch"
    if not belegt(z) or a.get("adern", ADERN) <= 0:
        return "unbelegt"
    if plaedoyer in ("gnade", "teilen") and erbarmen_moeglich(z)[0]:
        return "erbarmen"
    return "aufgeklaert"


FOLGEN = {
    "erbarmen": [{"flag": "urteil_erbarmen"}, {"wert": "vertrauen.megan", "delta": 1}, {"wert": "moral", "delta": 1}],
    "aufgeklaert": [{"flag": "urteil_aufgeklaert"}],
    "unbelegt": [{"flag": "urteil_unbelegt"}, {"flag": "praemie_gestrichen"}, {"wert": "moral", "delta": -1}],
    "falsch": [{"flag": "urteil_falsch"}, {"flag": "praemie_gestrichen"}, {"wert": "moral", "delta": -1}],
    "offen": [{"flag": "urteil_offen"}, {"flag": "praemie_gestrichen"}, {"flag": "kuendigung_angedroht"},
              {"wert": "moral", "delta": -1}],
    "entlastet": [{"flag": "urteil_entlastet"}, {"wert": "vertrauen.megan", "delta": 1}, {"wert": "moral", "delta": 1}],
}

URTEIL_EN = {
    "erbarmen": "Megan is silent for a long time. Then she puts the pen down and shows mercy: %(n)s stays aboard. "
                "Everyone sees, for one moment, that the boss has a heart.",
    "aufgeklaert": "Megan accepts the proof and passes judgement as she announced: %(n)s is put on probation and loses "
                   "the season bonus. Fair - not easy.",
    "unbelegt": "Megan does not convict on a hunch. Without a complete chain she decides herself: the crew's bonus "
                "is cancelled, and the question stays open.",
    "falsch": "Megan does not believe the accusation against %(n)s - there is nothing that holds. She decides "
              "herself: the bonus is cancelled. %(n)s was accused in front of everyone and waits for an apology.",
    "offen": "Duc has no name. Megan decides herself: the bonus is cancelled and she writes a few names on her list "
             "- if this happens again, people will be fired.",
    "entlastet": "Duc shows that nobody alone caused it - a chain of small things. Megan checks every link and accepts "
                 "it. Whoever was blamed is cleared.",
    "gefeuert": "Megan accepts the proof, and Duc asks for the full penalty: %(n)s is dismissed and leaves the boat "
                "today.",
}


# ------------------------------------------------------------------ Optionen der Anklage (kern/hauptstory.szene_bauen)
def anklage_optionen(z, modul, anwesend):
    """Die anwesenden Verdaechtigen (Reihenfolge der Besetzung, gemischt) plus "niemand allein" - hoechstens 4."""
    kreis = set((ermittlung._story(z) or {}).get("verdaechtige", [])) | set((modul.get("ermittlung") or {}).get("verdacht", []))
    verdacht = [p for p in anwesend if p in kreis][:3]
    out = [{"text": "%s." % _name(modul, p), "handlung": "He names %s before Megan as the one who caused it."
            % _name(modul, p), "folgen": [], "anhoerung": {"schritt": "anklage", "pid": p}} for p in verdacht]
    out.append({"text": "Nobody alone – or no name I can prove.", "handlung": "He says he cannot name one person: "
                "either it was a chain of small failures, or he has no proof against anyone.", "folgen": [],
                "anhoerung": {"schritt": "anklage", "pid": NIEMAND}})
    return out


# ------------------------------------------------------------------ Schritte (aus szene.waehlen)
def anklagen(z, modul, pid):
    """Schritt 1: Anklage (pid, "niemand" oder None) -> Zeugen, Einsprueche, Adern. -> (folgen, hinweis, zeilen)"""
    a = stand(z)
    e, f = ermittlung.stand(z), ermittlung.fall(z) or {}
    v = f.get("verantwortlich")
    a.clear()
    a["angeklagt"] = pid
    zeilen, folgen = [], []
    a["adern"], gruende = adern(z, pid if pid != NIEMAND else None, modul)    # vor dem neuen Vorwurf: er zaehlt nicht doppelt
    if pid and pid != NIEMAND:
        bel = belegt(z) and pid == v
        alt = next((x for x in e["vorwuerfe"] if x["pid"] == pid), None)
        if alt:
            alt.update(oeffentlich=True, belegt=alt.get("belegt") or bel)
        else:
            e["vorwuerfe"].append({"pid": pid, "tag": z["tag"], "oeffentlich": True, "belegt": bel})
    a["zeugen"] = zeugen(z, modul, pid if pid != NIEMAND else None)
    ermittlung.megan_haltung(z)
    wer = "niemanden allein" if pid == NIEMAND else (_name(modul, pid) if pid else "niemanden")
    zeilen.append("⚖ Anklage: %s · Megans Geduld %s" % (wer, "●" * a["adern"] + "○" * (ADERN - a["adern"])))
    for g in gruende:
        zeilen.append("   – %s" % g)
    teile = []
    for w in a["zeugen"]:
        n = _name(modul, w["pid"])
        if w["luegt"] and w["entlarvt"]:
            zeilen.append("⚖ Zeugin/Zeuge %s gibt ein Alibi – dein Einspruch mit Beweis entlarvt es." % n)
            teile.append("%s gives %s an alibi out of loyalty; Duc objects with proof and the alibi collapses - %s "
                         "admits she lied to protect her." % (n, _name(modul, pid), n))
        elif w["luegt"]:
            zeilen.append("⚖ Zeugin/Zeuge %s gibt ein Alibi. Du hast nichts, was es widerlegt." % n)
            teile.append("%s gives %s an alibi out of loyalty. Duc has nothing to refute it; it stands for now."
                         % (n, _name(modul, pid)))
        elif w["loyal"] and pid != v:
            zeilen.append("⚖ Zeugin/Zeuge %s gibt %s ein Alibi – und es hält." % (n, _name(modul, pid)))
            teile.append("%s gives %s an alibi out of loyalty - and it is true." % (n, _name(modul, pid)))
        elif w["loyal"]:
            zeilen.append("⚖ Zeugin/Zeuge %s hält zu %s, lügt für sie aber nicht – nicht vor dir." % (n, _name(modul, pid)))
            teile.append("%s is loyal to %s but trusts Duc too much to lie for her; she says only what is true."
                         % (n, _name(modul, pid)))
        else:
            zeilen.append("⚖ Zeugin/Zeuge %s sagt aus, was sie/er dir schon erzählt hat." % n)
            teile.append("%s testifies truthfully, only what she or he already told Duc - nothing new." % n)
    if not a["zeugen"]:
        zeilen.append("⚖ Niemand tritt als Zeuge auf. Megan notiert es.")
        teile.append("Nobody comes forward as a witness; Megan notes it.")
    satz = antibes_satz(z)
    hinweis = (("[The hearing - this reply] Megan opens with exactly this sentence to Duc: \"%s\" " % satz) if satz else "") + \
              ("[The hearing - this reply] Duc names %s as the cause before Megan. Witnesses: %s Megan's patience: "
               "%d of 3. Play the witnesses exactly like this, invent no new facts, no verdict yet.\n\n"
               % ("nobody alone - a chain of small failures" if pid == NIEMAND else
                  (_name(modul, pid) if pid else "no one - he has no name"), " ".join(teile), a["adern"]))
    return folgen, hinweis, zeilen


def rolle(z, modul, ehrlich):
    """Schritt Ducs eigene Rolle: ehrlich oder verschweigen (zaehlt fuer das Erbarmen)."""
    a = stand(z)
    a["rolle_ehrlich"] = bool(ehrlich)
    g = (ermittlung.fall(z) or {}).get("gestaendnis") or {}
    eigen = g.get("duc_eigene_rolle") or g.get("holm_rolle") or ""
    zeilen = ["⚖ Du legst deine eigene Rolle offen." if ehrlich else "⚖ Über deine eigene Rolle schweigst du."]
    hinweis = ("[The hearing - this reply] %s %s Megan registers it without comment.\n\n" % (
        "Duc tells Megan honestly what he himself did and did not do that night as First Officer." if ehrlich else
        "Duc says nothing about his own part in that night.",
        ("(Background for the model, do not quote: %s)" % eigen) if eigen and ehrlich else ""))
    return [{"flag": "rolle_ehrlich" if ehrlich else "rolle_verschwiegen"}], hinweis, zeilen


def plaedoyer(z, modul, art):
    """Schritt Plaedoyer + Urteil. art: gnade / teilen / strafe."""
    a = stand(z)
    a["plaedoyer"] = art
    u = urteil(z, art)
    a["urteil"] = u
    ermittlung.stand(z)["urteil"] = u
    v = (ermittlung.fall(z) or {}).get("verantwortlich")
    pid = a.get("angeklagt")
    folgen = list(FOLGEN[u])
    for k in ("folge", "verrat", "praemie", "strafe_unschuldig"):
        a.pop(k, None)
    if art == "teilen":                                # (2) Schuld teilen kostet immer (Duc 26.10.2026)
        folgen += [{"flag": "schuld_geteilt"}, {"wert": "vertrauen.megan", "delta": -1}, {"wert": "moral", "delta": 1}]
    if u == "erbarmen" and v:
        folgen.append({"wert": "vertrauen." + v, "delta": 2})
    if u == "aufgeklaert" and v:
        if art == "strafe":                            # Duc 26.10.2026: volle Strafe = Feuern (verlaesst das Schiff)
            a["folge"] = "gefeuert"
            folgen += [{"flag": "gefeuert"}, {"flag": "gefeuert_" + v}, {"flag": "strafe_gefordert"},
                       {"wert": "vertrauen." + v, "delta": -2}]
            if ermittlung.stand(z).get("gestaendnis"):   # (4) sie hatte Duc unter der Woche gestanden: Verrat
                a["verrat"] = True
                folgen += [{"wert": "vertrauen." + v, "delta": -1}, {"flag": "verrat_" + v}]
        else:
            folgen.append({"flag": "bewaehrung_" + v})
    if u in ("aufgeklaert", "erbarmen") and v:         # (6) Megans Praemie fuer eine bewiesene Kette
        a["praemie"] = PRAEMIE if ohne_bluff(z) else PRAEMIE // 2
        folgen.append({"geld": a["praemie"], "text": "Megan's bonus for the hearing"})
    if u == "falsch" and pid and pid not in (None, NIEMAND):
        folgen.append({"wert": "vertrauen." + pid, "delta": -1 if art == "gnade" else -2})   # (1) Gnade mildert
        if art == "strafe":                            # (1) eine Unschuldige feuern lassen wollen
            a["strafe_unschuldig"] = True
            folgen += [{"wert": "moral", "delta": -1}, {"flag": "strafe_gegen_unschuldige"}]
    moeglich, fehlt = erbarmen_moeglich(z)
    n = _name(modul, pid) if pid and pid != NIEMAND else (_name(modul, v) if v else "")
    zeilen = ["⚖ Urteil: " + URTEIL_DE[a.get("folge") or u] % {"n": n}]
    if art in ("gnade", "teilen") and u == "aufgeklaert" and fehlt:
        zeilen.append("   Erbarmen war nicht möglich – es fehlte: %s" % ", ".join(fehlt))
    hinweis = ("[The hearing - this reply, the verdict] Duc's plea: %s. Megan hesitates once at the engine report "
               "(\"A PX-480 doesn't just burn.\") and then rules: %s Play Megan's verdict exactly like this, in "
               "character; do not change it.\n\n" % (PLAEDOYER_EN[art], URTEIL_EN[a.get("folge") or u] % {"n": n}))
    return folgen, hinweis, zeilen


PRAEMIE = 500                                         # Euro; ein Job bringt 60-200 (missionen.json), halb mit Bluff
PLAEDOYER_EN = {"gnade": "he asks for mercy", "teilen": "he offers to share the blame",
                "strafe": "he demands the full penalty"}
URTEIL_DE = {
    "erbarmen": "Erbarmen – %(n)s bleibt an Bord.",
    "aufgeklaert": "Aufgeklärt – %(n)s kommt auf Bewährung und verliert die Saisonprämie.",
    "unbelegt": "Ohne lückenlose Kette urteilt Megan selbst: Prämie gestrichen, die Frage bleibt offen.",
    "falsch": "Megan glaubt die Anklage gegen %(n)s nicht. Prämie gestrichen – %(n)s wartet auf eine Entschuldigung.",
    "offen": "Kein Name – Megan urteilt selbst: Prämie gestrichen, Kündigungen angedroht.",
    "entlastet": "Niemand allein – Megan nimmt die Kette an. Wer beschuldigt war, ist entlastet.",
    "gefeuert": "Gefeuert – %(n)s verlässt heute das Schiff.",
}


def waehlen(z, modul, schritt):
    """Hook aus szene.waehlen: schritt = Option["anhoerung"]. -> (folgen, hinweis, zeilen)"""
    art = schritt.get("schritt")
    if art == "anklage":
        return anklagen(z, modul, schritt.get("pid"))
    if art == "rolle":
        return rolle(z, modul, schritt.get("ehrlich"))
    if art == "plaedoyer":
        return plaedoyer(z, modul, schritt.get("art"))
    raise ValueError("Unbekannter Schritt der Anhörung: %r" % art)


# ------------------------------------------------------------------ Spielbare Verhandlung (Variante B, 25.10.2026)
# Duc 25.10.: "Am Ende des Tages sind wir bei der Anhoerung ein Point-and-Click-Adventure." Drei Runden, eine je
# Kettenglied (Ace Attorney): eine Aussage, Press (nachhaken), Present (eine Faktenkarte legen), Bluff (Charme oder
# List), Joker (Gegenstand mit "anhoerung_ader"), Aufgeben. Eine Karte stimmt, wenn sie zu einem Beweissatz des Glieds
# gehoert, dessen uebrige Fakten Duc ebenfalls kennt. Falsche Karte -1 Ader, misslungener Bluff -2. Bei 0 Adern
# urteilt Megan selbst. Ergebnis in stand(z)["runden"]; danach laufen Rolle, Plaedoyer und Urteil wie bisher.
# Status "verhandlung" (eden.py), Oberflaeche client/plugins/eden-hearing. Spieltext englisch (STIL.md).
RUNDEN = ("handlung", "person", "folge")
RUNDE_TITEL = {"handlung": "What happened that night?", "person": "Who did it – and did they know?",
               "folge": "Did exactly that kill the drive?"}
BLUFF_SG = 14
WERTE = {"charm": "Charm", "cunning": "Cunning"}
ART_EN = {"dokument": "a document", "messung": "a measurement", "ereignis": "something the logs recorded",
          "beobachtung": "something you saw yourself", "gegenstand": "a physical object", "nachricht": "a message",
          "aussage": "a statement from someone who was there", "abgeleitet": "a conclusion you can back up"}
# Duc 25.10.: "viel zu unuebersichtlich" -> vier Stapel statt einer Kartenwand; Personen mit Portraet, technische
# Quellen mit einem von 8 Icons (gebuendelt aus den 20 SYSTEMQUELLEN in story_basis.py).
STAPEL = ("people", "systems", "papers", "own")
STAPEL_EN = {"people": "People", "systems": "Ship systems", "papers": "Papers & logs", "own": "Your own findings"}
QUELLE_ICON = {
    "pms": "monitoring", "lm3": "monitoring", "unit01_zaehler": "monitoring", "heckverteiler": "monitoring",
    "servicegeraet_alt": "monitoring", "buero_pc": "computer", "drucker": "computer", "kamera": "kamera",
    "plotter": "navigation", "maschinenbuch": "logbuch", "holm_logbuch": "logbuch", "bordhandbuch": "logbuch",
    "notizbuch": "logbuch", "wettbuch": "logbuch", "reservierungsbuch": "logbuch", "dokumentenmappe": "unterlagen",
    "herstellerunterlagen": "unterlagen", "eden_hq": "unterlagen", "aushang": "unterlagen", "telefon": "telefon"}
ICON_STAPEL = {"monitoring": "systems", "computer": "systems", "kamera": "systems", "navigation": "systems",
               "logbuch": "papers", "unterlagen": "papers", "telefon": "papers"}
ICON_EN = {"monitoring": "Monitoring", "computer": "Office PC", "kamera": "Camera", "navigation": "Navigation",
           "logbuch": "Logbook", "unterlagen": "Files", "telefon": "Phone", "lupe": "You"}
ZUV_RANG = {"gesichert": 0, "belastbar": 1, "beobachtet": 2, "aussage": 3}
# Duc 25.10.: "Wenn wir in What sind, sollen nur Hinweise zu What angezeigt werden." Thema einer Karte: die Runden,
# in deren Beweissaetzen sie steht; Fakten ohne Beweissatz (Ablenkungen) nach ihrer Art (Faustregel, bis die
# Falldaten ein eigenes Themenfeld haben). Der Client zeigt je Runde nur ihr Thema, mit Schalter "show all notes".
THEMA_ART = {"messung": "handlung", "ereignis": "handlung", "gegenstand": "handlung", "aussage": "person",
             "beobachtung": "person", "nachricht": "person", "dokument": "folge", "abgeleitet": "folge"}
THEMA_EN = {"handlung": "Tell me about the state of the system that night.",
            "person": "Tell me who was where, and when – and who knew what.",
            "folge": "Tell me why nothing stopped it."}


def themen(z, fid, f):
    gl = [g["id"] for g in (ermittlung.fall(z) or {}).get("glieder", [])
          if any(fid in s for s in g["beweis_saetze"])]
    return gl or [f.get("thema") or THEMA_ART.get(f.get("art"), "person")]      # "thema" aus den Falldaten geht vor


def karte_einordnen(modul, f):
    """-> (stapel, icon oder None, pid oder None, Quellen-Name)."""
    q = f.get("quelle") or ""
    if q == "duc" or f.get("art") == "abgeleitet":
        return "own", "lupe", None, ICON_EN["lupe"]
    if q in modul["personen"]:
        return "people", None, q, _name(modul, q)
    icon = QUELLE_ICON.get(q, "unterlagen")
    return ICON_STAPEL[icon], icon, None, ICON_EN[icon]


ZEILEN = {
    # Megans Saetze in Kategorien, je mit Varianten (Duc 25.10.: "vertont, mit Varianzen"). Vertont unter vh.<kat>.<n>
    # (werkzeuge/eden_rise/vertonen_eden_rise.py); keine Namen im Text, damit jede Aufnahme fuer alle Faelle passt.
    # Der Werftbericht ist die Grundlage der Anhoerung (Duc 27.10.2026): Megan legt ihn vor Punkt 1 auf den Tisch.
    # Die Werft will "Verschleiss" - dann prueft niemand ihre eigene Wartung; deshalb rudert sie spaeter zurueck.
    "bericht": ["The yard opened up my drive on Monday and sent me this. Their report. It's what goes to the owner and "
                "to the insurers – unless someone in this room shows me it's wrong. They say wear and tear. How… "
                "convenient, for them.",
                "This came from the yard this morning. Twelve pages, one conclusion: wear and tear. An old module that "
                "simply gave up. If it stands, that's what the owner reads. I studied shipbuilding, First Officer. I "
                "know a tidy report when I see one.",
                "Before we start – this. The yard's report on my drive, and the basis of today. Whatever you can't "
                "disprove goes into the file exactly as written. And the yard, naturally, would very much like this to "
                "be wear and tear."],
    "einleitung_handlung": ["Point one: what happened to the drive that night. I'll read you what the yard wrote. Two "
                            "lines are true, one is not. Show me the note that proves which.",
                            "Let's begin with the machine. Three lines from the report – two true, one wrong. Your "
                            "notes will tell you which.",
                            "Point one. Here's the yard's version of that night. Most of it holds. One line doesn't. "
                            "Find it."],
    "werft_nachgebessert": ["Revised. Funny how that works.",
                            "A second version, sent within the hour. The yard can be very quick when it wants to be.",
                            "They've corrected themselves. Not by much. Let's see if this one holds."],
    "einleitung_person": ["Point two: who did it. The accused will answer for themselves. Two lines are true. One is a "
                          "lie.",
                          "Now – who. Let's hear it from the person you've named. One of these lines doesn't match what "
                          "you found. Show me.",
                          "So. You've named someone. Let them speak. Two truths and a lie, First Officer – you know the "
                          "game."],
    "einleitung_niemand": ["Point two. You say nobody alone did this. Then show me there was no single hand on that "
                           "switch.",
                           "Nobody? Bold. Systems don't change themselves, First Officer. Prove me wrong."],
    "einleitung_folge": ["Point three: why. Did exactly that kill my drive? Two of these lines hold. Show me the one "
                         "that doesn't.",
                         "Last point. Even if all that is true – why did it break? One line here is wrong.",
                         "And now the part the insurers care about. Why did it fail? Two lines are fine. One isn't."],
    "richtig": ["Hm. That I can check. So that line doesn't hold – noted.",
                "Good. You've done your homework, First Officer.",
                "…Fine. That holds up. Go on.",
                "Noted. I don't enjoy being proven wrong. I enjoy it even less when it's the yard."],
    "satz_haelt": ["That line holds, First Officer. Nobody here disputes it. Find the one that's wrong.",
                   "No. That one is true, and you know it. Don't waste my time.",
                   "You're attacking the one line nobody doubts. Are you even listening?"],
    "falsche_karte": ["That note is about something else entirely. It doesn't touch what was said.",
                      "And what exactly is that supposed to prove? Nothing. Try again.",
                      "Paper, First Officer. That's all that is. It has nothing to do with this line."],
    # Ablehnung mit Grund (Duc 28.10.2026): statt der Pauschale sagt Megan, WARUM die Notiz nicht greift
    "anderer_punkt": ["That note belongs to another point, First Officer. Not this one.",
                      "Wrong point. Keep that one for later."],
    "nur_aussage": ["That's what someone says. It doesn't touch this line.",
                    "One person's word, and not even about this. Next."],
    "andere_behauptung": ["Right point. But that's not what this line claims.",
                          "That belongs here – just not to this line. Read it again."],
    "luecke": ["That's a start – but on its own it proves nothing. What else backs it up?",
               "Interesting. Not enough, though. What else do you have?",
               "Half a proof is no proof. Keep digging."],
    "anderswo": ["That points somewhere else, First Officer. Not at the person you've named.",
                 "Then you've accused the wrong person. That evidence points elsewhere."],
    "bluff_ja": ["…Noted.", "…Hm. Very well. I'll accept that – for now.", "Confident. I'll give you that one."],
    "bluff_nein": ["Bluffing at my hearing. Bold, First Officer. Stupid, but bold.",
                   "Do you think I was born yesterday? Sit up straight.",
                   "I've eaten men like you for breakfast in board meetings. Try the truth."],
    "aufgeben": ["Then we'll leave that open. It won't count in your favour.",
                 "Nothing to show? Then this point stays open. Noted."],
    "gestaendnis": ["There's a confession on record for this. I've read it. Next.",
                    "I've seen the confession. We don't need to go through it again."],
    "joker": ["…Fine. Carry on.", "Hm. Thank you. Where were we?"],
    "geduld_weg": ["Enough. I've heard enough. I'll decide this myself.",
                   "Stop. My patience has run out, First Officer. I'll decide without you."],
    "ende": ["Thank you, First Officer. Sit down. I'll hear one more thing from you before I decide.",
             "That's all I need from the evidence. Sit. One more thing, and then I decide."],
    "plaedoyers_auf": ["Before you name anyone, First Officer, I want to hear from each of them. Briefly.",
                       "Everyone who could have done this will speak now. Listen carefully, Duc."],
    "anklage_auf": ["Now. Arrange your evidence, First Officer – and name the one who did it.",
                    "You've heard them all. Sort your notes, then give me a name.",
                    "Take your time with your notes. Then accuse someone – and be sure."],
    "punkt_handlung": ["Point one stands. Something happened to that drive, and it wasn't wear and tear.",
                       "Noted for the record: the yard's report is wrong. Point one is proven."],
    "punkt_person": ["Point two stands. We know whose hand it was.",
                     "For the record: that statement was false. Point two is proven."],
    "punkt_folge": ["Point three stands. That is what killed my drive.",
                    "And that closes the chain. Point three is proven."],
    "punkt_offen": ["That point stays open. I'm writing it down, First Officer – against you.",
                    "Unproven. Let's move on – I won't forget it."],
    "ruhe": ["Quiet, please.", "That's enough. Quiet.", "Settle down, everyone."],
    "nachgebessert": ["Then let's hear it again. Properly, this time.", "A new version. Let's see if this one holds."],
    "halb": ["Half of it holds. I'll count it – barely.", "You got that far. I'll give you half – no more."],
    "warum": ["Why? I want to hear it from you. All of it.", "Tell me why. Not to him – to me."],
    "rolle_frage": ["Before I decide: what was your part in all this, First Officer? Where were you that night?",
                    "One more question, and it's for you, Duc. What did you do that night – and what didn't you do?"],
    "rolle_ehrlich": ["…Thank you for not making me drag it out of you.", "Honest. That counts for something with me."],
    "rolle_schweigen": ["Nothing to say about yourself. Noted.", "Silence. I'll remember that, First Officer."],
    "plaedoyer_frage": ["Last word, First Officer. What do you ask of me?",
                        "Then tell me what you want. Mercy? Or the full weight of it?"],
    "urteil_erbarmen": ["I've decided. You stay aboard. No probation, no note in your file. Don't make me regret it."],
    "urteil_aufgeklaert": ["The proof holds. You're on probation for the rest of the season, and your bonus is gone. "
                           "That's fair. Not easy – fair."],
    "urteil_gefeuert": ["The proof holds, and the First Officer asks for the full penalty. So be it. You leave this "
                        "boat today."],
    "urteil_unbelegt": ["Without a complete chain I won't convict anyone. The crew's bonus is cancelled. The question "
                        "stays open."],
    "urteil_falsch": ["I don't believe it. Nothing you showed me holds against that person. The bonus is cancelled – "
                      "and you owe someone an apology."],
    "urteil_offen": ["No name. Then I decide myself: the bonus is cancelled, and I'm writing names on a list. If this "
                     "happens again, people go."],
    "urteil_entlastet": ["Nobody alone. A chain of small things. I checked every link, and it holds. Whoever was "
                         "blamed is cleared."],
    "praemie_voll": ["You did proper work this week, First Officer. There's a bonus in your account. You earned it."],
    "praemie_halb": ["Not all of that was proof. Half a bonus – that's what half-proof buys you."],
    "schluss": ["This hearing is closed. Back to work, all of you.",
                "That's it. The hearing is closed. Go – the boat won't run itself."],
    "zeuge_anruf": ["One more voice before we go on. We have a witness on the line.",
                    "Someone asked to be heard. They can't be here – so they're joining us by video."],
    "kette_auf": ["Let's put it together. We know what happened. We know who. One question is left: why.",
                  "Two links, First Officer. Give me the third, and the chain holds."],
    "kette_luecke": ["Let's see what we have. Not everything holds. Maybe this will.",
                     "There are gaps in this chain, First Officer. Let's see if you can close the last one."],
    "kette_zu": ["What, who, why. The chain holds.",
                 "Three links. It holds. That I can take to the board."],
    "kette_zu_teil": ["That link holds. Whatever else is missing – that one, I believe.",
                      "The why, at least, is clear now. The rest stays on your account."],
    "kette_riss": ["And there the chain breaks. I can't take that to anyone.",
                   "Without the why, the rest is a story, First Officer. Just a story."],
    "ungeduld": ["Tick tock, First Officer.", "I don't have all day. Decide.",
                 "Well? The crew is waiting. So am I.", "Somewhere in that pile is your answer. Find it.",
                 "Any time this century, Duc."],
}
UNVERTONT = {"person_zeuge": ("{w}", "{p} was with me that night. The whole time. I'd swear to it.")}

# ------------------------------------------------------------------ Momente (Uebergaenge mit Pause und Wucht)
# Log-Eintraege mit diesen Arten spielt der Client als eigenen Moment ab (Vollbild-Karte bzw. Sprechblase, Stimme,
# Effekt); "warte" heisst: weiter erst auf Klick. Duc hat keine Stimme - "Objection!" ist Schriftzug + Effekt.
OBJECTION = ["OBJECTION!", "HOLD IT!", "TAKE THAT!"]
PUBLIKUM = {  # ein Satz aus dem Saal nach einem Treffer, vertont unter vh.publikum.<pid>.<n>
    "lola": ["Oh, mate.", "Did everyone hear that? I heard that."],
    "toto": ["Madonna!", "Two to one on the Comandante – I said it!"],
    "maxwell": ["Eish! Number One!", "Mr. Maximum felt that one, brother."],
    "jana": ["Jessas…", "Na geh – he really did it."],
    "siri": ["Oh my god.", "Okay. Okay, wow."],
    "lea": ["Oh!", "That was proper clever."],
    "sophia": ["Well played, darling.", "Ten euros says Megan didn't see that coming."],
    "rosi": ["Ha. That one's yours, Officer.", "Told you the logs don't lie."],
    "chiara": ["…Seven. Maybe eight.", "Well. That was something."],
}
REAKTION = {  # die Angeklagte, wenn Duc ihren Namen sagt - gleiche Zeile, ob schuldig oder nicht
    "chiara": ("Me? I – Duc, you can't be serious. After everything?", "surprise"),
    "lea": ("What? No – no, I didn't, I swear I didn't!", "fear"),
    "sophia": ("Darling. You're making a scene. In front of everyone.", "disapproval"),
    "rosi": ("Me?! I'm the one who kept this boat alive! You've got some nerve, Officer.", "anger"),
    "yasin": ("Bro. Seriously? On camera? Unbelievable.", "annoyance"),
}
PLAEDOYER = {  # Verteidigung vor der Aussage (Unschuldige; die Verantwortliche bekommt ihr Plaedoyer aus den Falldaten)
    "chiara": ["Six seasons on this boat. I know every cabin, every guest, every crack in the paint.",
               "If you think I would risk all of that – then you don't know me at all."],
    "lea": ["I was on deck most of the night. I don't even know how the drive works – Rosi always says don't touch "
            "anything.", "Please. Ask anyone. I would never…"],
    "sophia": ["I've spent four seasons making this crew look better than it is. That's my job.",
               "Accusing me won't fix your engine, Duc. But go on. I'm listening."],
    "rosi": ["That drive is my life. I talk to those machines more than I talk to people.",
             "If I'd broken it, I'd have fixed it by morning. Think about that."],
    "yasin": ["I'm a guest, bro. I film things. I don't press buttons on boats.",
              "You want a villain for your report? Find someone else."],
}


# Punkt 2 und 3 (Duc 26.10.2026: "mehr Immersion, den User durch die Anhoerung fuehren"). Alle Saetze ohne Fall-
# Aufloesung: sie passen zu jedem Fall, in dem die Person verdaechtig ist. Vertont unter vh.<tabelle>.<pid>[.<n>].
RAUNEN = {  # der Saal, wenn Duc einen Namen nennt
    "lola": "Oh, here we go.", "toto": "Mamma mia. In front of everyone.", "maxwell": "Eish. That's heavy, brother.",
    "jana": "Oh dear. Oh dear, oh dear.", "siri": "Wait. What?", "lea": "No way…",
    "sophia": "Well. That's one way to start a lunch.", "rosi": "Here it comes.", "chiara": "…Careful, Duc.",
}
NERVOES = {  # die Angeklagte stockt, wenn Duc bei ihrer falschen Zeile nachhakt (Ace-Hinweis ohne Text)
    "chiara": ["That's… yes. That's what I said.", "Why are you looking at me like that?"],
    "lea": ["I – I mean, yes. I think so. Yes.", "Can we… can we move on?"],
    "sophia": ["Must we dwell on that, darling?", "I've answered that. Haven't I?"],
    "rosi": ["…Look. I said what I said.", "Don't twist my words, Officer."],
    "yasin": ["Bro, that's… that's just how it was, okay?", "Why's everyone staring? Stop staring."],
}
KONTER = {  # die Angeklagte, wenn Duc danebenliegt
    "chiara": ["Is that really all you've got, Duc?", "You're grasping. Everyone can see it."],
    "lea": ["That… doesn't have anything to do with me.", "See? I told you. I didn't do anything."],
    "sophia": ["Paper. How very thorough of you, darling.", "Is that meant to impress me?"],
    "rosi": ["Ha! Wrong engine, Officer.", "You want to try that again? Slowly?"],
    "yasin": ["Bro. That's nothing.", "Clip that. He's got nothing."],
}
ZUSAMMENBRUCH = {  # nach OBJECTION! in Punkt 2 - nur, wenn die Angeklagte es wirklich war
    "chiara": ["That's – no. That's not how it…", "…I never wanted any of this to happen. Not to the boat. Not to you."],
    "lea": ["No, no, no – wait, please –", "I'm sorry. I'm so sorry. I didn't think it would… I didn't think."],
    "sophia": ["…Oh.", "Well. It seems I underestimated you, Duc. I won't do that again."],
    "rosi": ["That's… you don't understand, I –", "…Fine. Fine! I'll own it. But I never meant to hurt the boat."],
    "yasin": ["Okay – okay, turn it off. Turn the camera off.", "…This wasn't supposed to go like this, bro."],
}
AUFATMEN = {  # Unschuldige, wenn der Beweis woanders hinzeigt
    "chiara": "…Thank you. I think.", "lea": "Oh, thank god.", "sophia": "There. Was that so hard?",
    "rosi": "Told you. Told you!", "yasin": "Finally. Someone with a brain.",
}
ZEUGE = {  # wer zur Angeklagten haelt und fuer sie luegt (story.json anhoerung.loyal)
    "sophia": "I was with them that night, darling. The whole time. I'd swear to it.",
    "lea": "They were with me! The whole night. I swear.",
    "holm": "I'll vouch for that. I was there. All night.",
    "lola": "Hold on – I was with them that night, mate. All of it.",
    "siri": "Um – I was with them. The whole night. Like, the whole time.",
}
BLICK = {  # die Ueberfuehrte, wenn sich die Kette schliesst
    "chiara": "…Six seasons. And this is how it ends.", "lea": "I'll tell her everything. I promise.",
    "sophia": "You'd have been wasted on spreadsheets, you know.", "rosi": "…Look after her engines. Someone has to.",
    "yasin": "Delete the footage. Please.",
}
# Tratsch (Duc 26.10.2026: "Lass die Crew wirklich zwischen jeder Phase tratschen, 2-3 Leute"). Zeilen, deren
# Sprecher angeklagt oder nicht an Bord ist, fallen weg; bleiben weniger als zwei, entfaellt der Tratsch.
TRATSCH_HANDLUNG = [("lola", "So it wasn't just an old part giving up."),
                    ("toto", "Madonna. Somebody did something. On our boat."),
                    ("maxwell", "Mr. Maximum does not like this, brother.")]
TRATSCH_ANKLAGE = {
    "chiara": [("lola", "Chiara? Never. She loves this boat more than any of us."),
               ("toto", "Six seasons, Lola. Love makes people do stupid things."),
               ("sophia", "Hush, both of you. Let her speak.")],
    "lea": [("sophia", "Lea? Lea can't even work the coffee machine."),
            ("rosi", "That's exactly what worries me."),
            ("siri", "Oh my god, she's shaking. Poor thing.")],
    "sophia": [("lea", "Sophia? No. She's the one who keeps us all together."),
               ("toto", "Ten years in this business, she's never broken a nail. Or a rule."),
               ("lola", "Never seen her rattled. Look at her. Not even now.")],
    "rosi": [("lola", "Rosi? She'd sleep in the engine room if they let her."),
             ("maxwell", "The machine lady, brother? No way."),
             ("chiara", "People who know a machine that well also know how to break it.")],
    "yasin": [("siri", "Yasin? He films his breakfast. When would he find the time?"),
              ("rosi", "He was down in my engine room twice. Asking questions."),
              ("toto", "A guest. On trial. Now I've seen everything.")],
    "niemand": [("lola", "Nobody? He's saying nobody did it?"),
                ("rosi", "Machines don't break themselves."),
                ("sophia", "Or maybe everybody did a little. That's worse.")],
}
TRATSCH_BRUCH = {  # nach dem Zusammenbruch der Ueberfuehrten
    "chiara": [("lola", "I'd never have thought it. Not Chiara."), ("toto", "Did you see it coming? Honestly?"),
               ("lea", "No. She always said rules are rules.")],
    "lea": [("siri", "Lea? Little Lea?"), ("sophia", "I should have seen it. I'm with her every day."),
            ("maxwell", "Even the small ones carry heavy things, brother.")],
    "sophia": [("lea", "Sophia… I don't understand."), ("lola", "The perfect one. Huh. Who'd have guessed."),
               ("rosi", "I'd have guessed. Nobody's that perfect.")],
    "rosi": [("maxwell", "The machine lady broke the machine?"), ("lola", "She'd never hurt that drive on purpose. Never."),
             ("chiara", "Then why did she lie about it?")],
    "yasin": [("siri", "Called it. I totally called it."), ("toto", "You called nothing, you bet on Sophia."),
              ("lola", "Either way. A guest. Unbelievable.")],
}
TRATSCH_URTEIL = {  # nach Megans Urteil
    "erbarmen": [("lola", "Mercy. From Megan. Somebody write that down."), ("toto", "The boss has a heart. Who knew?"),
                 ("maxwell", "Respect, brother. Real respect.")],
    "aufgeklaert": [("rosi", "Probation. Fair, I suppose."), ("lola", "Fair, but it'll be a long season."),
                    ("toto", "Bonus gone. My betting board weeps.")],
    "gefeuert": [("lola", "Gone. Just like that."), ("rosi", "He asked for the full penalty. He got it."),
                 ("maxwell", "Hard day for this crew, brother.")],
    "unbelegt": [("toto", "So… nobody?"), ("rosi", "Nobody, and no bonus. Great."), ("lola", "We'll never know now.")],
    "falsch": [("lola", "That was wrong. Everyone could see it."), ("sophia", "Someone owes an apology. A big one."),
               ("toto", "Awkward dinner tonight.")],
    "falsch_strafe": [("lola", "He wanted them gone. In front of everyone. For nothing."),
                      ("rosi", "Remember that. All of you. Remember that."),
                      ("toto", "Cold, Comandante. Very cold.")],
    "offen": [("rosi", "No name. She's writing a list now."), ("siri", "A list? Of us?"),
              ("lola", "Keep your head down, love.")],
    "entlastet": [("lea", "So it was nobody? Really nobody?"), ("maxwell", "Many small hands, brother. Many small mistakes."),
                  ("lola", "Better than one person carrying it.")],
}
URTEIL_REAKTION = {  # die Angeklagte auf das Urteil: erbarmen / aufgeklaert / gefeuert (schuldig) und falsch (unschuldig)
    "chiara": {"erbarmen": "…Thank you. I won't forget this. Either of you.", "aufgeklaert": "Probation. Okay. I'll earn it back.",
               "gefeuert": "…I'll pack my things. Don't watch me go.", "falsch": "I'll be waiting for that apology, Duc."},
    "lea": {"erbarmen": "Really? Oh – thank you, thank you.", "aufgeklaert": "I understand. I'll do better. I promise.",
            "gefeuert": "I… okay. Okay. I'll go.", "falsch": "Why would you say that about me?"},
    "sophia": {"erbarmen": "How very gracious. I won't waste it.", "aufgeklaert": "A blemish. I'll survive it.",
               "gefeuert": "Well. I always did look good leaving.", "falsch": "I'll remember this, darling. All of it."},
    "rosi": {"erbarmen": "…Thanks, boss. I'll look after her.", "aufgeklaert": "Fine. I'll take it. The engine comes first.",
             "gefeuert": "Who's going to keep her running now? You?", "falsch": "Think about it. Then come and say sorry."},
    "yasin": {"erbarmen": "Respect. Seriously. Respect.", "aufgeklaert": "Okay. That's… fair, I guess.",
              "gefeuert": "Fine. Cancel me. See if I care.", "falsch": "Unbelievable. I'm posting about this."},
}
URTEIL_VERRAT = {  # gefeuert, nachdem sie Duc unter der Woche gestanden hatte
    "chiara": "I told you everything. I trusted you. And this is what you do with it.",
    "lea": "I told you the truth… because you asked. I thought you were different.",
    "sophia": "I confided in you, darling. I won't make that mistake twice.",
    "rosi": "I came to you myself. Myself! Remember that, Officer.",
    "yasin": "I told you off camera, bro. Off camera.",
}
URTEIL_KURZ_EN = {"erbarmen": "Mercy – %(n)s stays aboard.",
                  "aufgeklaert": "Solved – %(n)s is on probation and loses the season bonus.",
                  "gefeuert": "Dismissed – %(n)s leaves the boat today.",
                  "unbelegt": "Unproven – the crew's bonus is cancelled, the question stays open.",
                  "falsch": "Wrong person – the bonus is cancelled, and %(n)s waits for an apology.",
                  "offen": "No name – the bonus is cancelled, and Megan threatens dismissals.",
                  "entlastet": "Nobody alone – whoever was blamed is cleared."}
URTEIL_GEFUEHL = {"erbarmen": "caring", "aufgeklaert": "neutral", "gefeuert": "disapproval", "unbelegt": "disappointment",
                  "falsch": "anger", "offen": "annoyance", "entlastet": "relief"}
REAKTION_GEFUEHL = {"erbarmen": "gratitude", "aufgeklaert": "sadness", "gefeuert": "grief", "falsch": "anger"}
GEWONNEN = ("beweis", "gestaendnis", "bluff")


def _tratsch(z, modul, v, zeilen, schl):
    """2-3 Crewleute reden durcheinander, dann Megan: Ruhe. zeilen = [(sprecher, satz)], schl = Vertonungs-Schluessel."""
    pid = v.get("angeklagt")
    da = [(i, p, s) for i, (p, s) in enumerate(zeilen) if p in modul["personen"] and p != pid and an_bord(z, modul, p)]
    if len(da) < 2:
        return False
    gruppe = [p for _, p, _ in da]
    for n, (i, p, s) in enumerate(da):
        _moment(v, "tratsch", s, wer=p, key="%s.%d" % (schl, i), gruppe=gruppe, gefuehl="surprise" if n == 0 else None)
    k = _wahl(v, len(ZEILEN["ruhe"]))
    _moment(v, "ruhe", ZEILEN["ruhe"][k], key="vh.ruhe.%d" % k, gefuehl="annoyance")
    return True


def _moment(v, art, text, wer="megan", key=None, gefuehl=None, warte=False, effekt=None, sub=None, **extra):
    e = dict(extra, wer=wer, text=text, art=art, moment=True)
    for k, x in (("key", key), ("gefuehl", gefuehl), ("effekt", effekt), ("sub", sub)):
        if x:
            e[k] = x
    if warte:
        e["warte"] = True
    v["log"].append(e)


def _wahl(v, n):
    return random.Random(len(v["log"]) * 13 + v["runde"] * 5 + v.get("adern", 0)).randrange(n)


def _treffer(z, modul, v, r):
    """Nach einem bewiesenen Punkt: OBJECTION!, Megans Satz, eine Stimme aus dem Saal, Punkt-Abschluss."""
    _moment(v, "objection", OBJECTION[_wahl(v, len(OBJECTION))], wer="duc", effekt="anhoerung_einspruch")
    pid = v.get("angeklagt")
    if r == "person" and pid in ZUSAMMENBRUCH:         # der Hoehepunkt des Duells: die Aussage faellt in sich zusammen
        for i, s in enumerate(ZUSAMMENBRUCH[pid]):
            _moment(v, "zusammenbruch", s, wer=pid, key="vh.zusammenbruch.%s.%d" % (pid, i),
                    gefuehl="surprise" if i == 0 else "remorse", effekt="blackout" if i == 0 else None)
    if r == "folge":
        _kette(v, "zu" if all(v["runden"].get(x) in GEWONNEN for x in RUNDEN) else "zu_teil")
    else:
        _zeile(v, "richtig", modul)
    getratscht = False
    if r == "person" and pid in TRATSCH_BRUCH:          # "Ich haette nie gedacht ..." statt eines einzelnen Rufs
        getratscht = _tratsch(z, modul, v, TRATSCH_BRUCH[pid], "vh.tratsch.bruch." + pid)
    saal = [p for p in PUBLIKUM if p != pid and p in modul["personen"]]
    if saal and not getratscht:
        p = saal[_wahl(v, len(saal))]
        n = _wahl(v, len(PUBLIKUM[p]))
        _moment(v, "publikum", PUBLIKUM[p][n], wer=p, key="vh.publikum.%s.%d" % (p, n), gefuehl="surprise")
    if r == "folge":
        _blick(v, z)
    n = _wahl(v, len(ZEILEN["punkt_" + r]))
    _moment(v, "punkt", ZEILEN["punkt_" + r][n], key="vh.punkt_%s.%d" % (r, n), gefuehl="approval", warte=True,
            effekt="mission_erfolg")
    if r == "handlung":                                  # der Saal verdaut, was gerade herauskam
        eigen = _aussagen_daten(z).get("tratsch")
        nr = (ermittlung.fall(z) or {}).get("nr")
        _tratsch(z, modul, v, [tuple(x) for x in eigen] if eigen else TRATSCH_HANDLUNG,
                 "vh.f%s.tratsch" % nr if eigen else "vh.tratsch.handlung")


def _kette(v, art):
    """Das Kettenbrett: What / Who / Why als angeheftete Zettel, Megan liest vor (auf, luecke, zu, zu_teil, riss)."""
    kat = "kette_" + art
    n = _wahl(v, len(ZEILEN[kat]))
    _moment(v, "kette", ZEILEN[kat][n], key="vh.%s.%d" % (kat, n), zustand=art,
            kette=[v["runden"].get(x) for x in RUNDEN], warte=art in ("auf", "luecke"),
            sub="Hear the last statement" if art in ("auf", "luecke") else None,
            gefuehl={"riss": "disappointment", "zu": "approval", "zu_teil": "approval"}.get(art),
            effekt={"zu": "hinweis_gefunden", "zu_teil": "hinweis_gefunden", "riss": "mission_fehlschlag"}.get(art))


def _gestaendnis_rede(z, modul, v):
    """Duc 26.10.: "Die Person erklaert nicht, warum sie das gemacht hat." Nach der Kette erzaehlt die Ueberfuehrte
    ihr Motiv (Falldaten "gestaendnis") - nur, wenn sie wirklich angeklagt und Punkt 2 gewonnen ist."""
    pid = v.get("angeklagt")
    rede = _aussagen_daten(z).get("gestaendnis")
    if not rede or pid != (ermittlung.fall(z) or {}).get("verantwortlich") or v["runden"].get("person") not in GEWONNEN:
        return
    nr = (ermittlung.fall(z) or {}).get("nr")
    k = _wahl(v, len(ZEILEN["warum"]))
    _moment(v, "warum", ZEILEN["warum"][k], key="vh.warum.%d" % k, gefuehl="curiosity")
    for i, (s, gef) in enumerate(rede):
        _moment(v, "gestaendnis", s, wer=pid, key="vh.f%s.gestaendnis.%d" % (nr, i), gefuehl=gef,
                warte=i == len(rede) - 1)


def _blick(v, z=None):
    pid = v.get("angeklagt")
    if z is not None and _aussagen_daten(z).get("gestaendnis"):
        return                                         # das Gestaendnis sagt mehr als ein letzter Blick
    if pid in BLICK and v["runden"].get("person") in GEWONNEN:
        _moment(v, "blick", BLICK[pid], wer=pid, key="vh.blick." + pid, gefuehl="sadness")


def _offen(z, modul, v, r):
    n = _wahl(v, len(ZEILEN["punkt_offen"]))
    _moment(v, "punkt", ZEILEN["punkt_offen"][n], key="vh.punkt_offen.%d" % n, gefuehl="disappointment", warte=True,
            effekt="mission_fehlschlag")


def _plaedoyers(z, modul, v):
    """Alle Verdaechtigen verteidigen sich, bevor Duc jemanden anklagt (Duc 26.10.2026). Die Verantwortliche spricht
    ihr Plaedoyer aus den Falldaten, die anderen ihr allgemeines - gleich stark, damit man nichts ablesen kann."""
    _zeile(v, "plaedoyers_auf", modul)
    v_ok = (ermittlung.fall(z) or {}).get("verantwortlich")
    daten = (_aussagen_daten(z).get("runden") or {}).get("person") or {}
    nr = (ermittlung.fall(z) or {}).get("nr")
    reihe = _verdaechtige(z, modul)
    for pid in reihe:
        if pid == v_ok and daten.get("plaedoyer"):
            zeilen = [(s, "vh.f%s.plaedoyer.%d" % (nr, i)) for i, s in enumerate(daten["plaedoyer"])]
        else:
            zeilen = [(s, "vh.plaedoyer.%s.%d" % (pid, i)) for i, s in enumerate(PLAEDOYER.get(pid, []))]
        for i, (s, key) in enumerate(zeilen):
            _moment(v, "plaedoyer", s, wer=pid, key=key, gefuehl="pride" if i == 0 else "sadness", gruppe=reihe)


def _titel(v, r, z=None, modul=None):
    nr = RUNDEN.index(r) + 1
    tipp = tafel_tipp(z, modul, r) if z else None
    _moment(v, "titel", RUNDE_TITEL[r], sub="Point %d of 3" % nr, warte=nr > 1, effekt="phase_wechsel",
            **({"tipp": tipp} if tipp else {}))


def tafel_tipp(z, modul, r):
    """Derselbe Satz wie auf der Fall-Tafel im Codex (Duc 28.10.2026): was fuer diesen Punkt noch fehlt, nur die Art."""
    g = next((x for x in ermittlung.tafel(z, modul) if x["id"] == r), None)
    if not g:
        return None
    if g["stand"] == "proven":
        return "Your notes cover this point."
    teil = "%d of %d pieces. " % (g["x"], g["y"]) if g["stand"] == "partly" else ""
    return teil + " ".join(g["fehlt"])
GEDANKE_ZWEIFEL = "Something about that doesn't sit right."
# Megans Gesicht je Kategorie (Duc 25.10.: "Wenn wir was Falsches sagen, muss Megan angry sein")
GEFUEHL = {"satz_haelt": "anger", "falsche_karte": "anger", "bluff_nein": "anger", "geduld_weg": "anger",
           "anderer_punkt": "annoyance", "nur_aussage": "disapproval", "andere_behauptung": "annoyance",
           "warum_nicht": "disapproval",
           "richtig": "approval", "bluff_ja": "surprise", "luecke": "curiosity", "anderswo": "confusion",
           "aufgeben": "disappointment", "ungeduld": "annoyance", "joker": "gratitude"}

# Allgemeine Aussagen fuer Faelle ohne eigene Daten (anhoerung_aussagen.json) - eine Zeile je Runde ist falsch und
# wird von jedem Fakt widerlegt, der zu einem Beweissatz der Runde gehoert (widerlegt None).
ALLGEMEIN = {
    "handlung": ("megan", [("The yard's first report says wear and tear: an old module that simply gave up.",
                            "A PX-480 doesn't just burn, First Officer. Our engineers will want more than a feeling.",
                            True)]),
    "person": ("{p}", [("I didn't do anything to that system.",
                        "Ask anyone. I wasn't even near it – and I don't know why you'd think I was.", True),
                       ("I would never put this crew at risk.", "This boat is my home too.", False)]),
    "unschuldig": ("{p}", [("I was in my cabin before two and I stayed there.", "Check the corridor, ask anyone.", False),
                           ("I didn't touch the bridge or the drive.", "Why would I? It's not my job.", False),
                           ("Ask anyone who saw me that night.", "I have nothing to hide.", False)]),
    "niemand": ("megan", [("Systems don't change themselves. Somebody pressed a button.",
                           "Show me otherwise, First Officer.", True)]),
    "folge": ("megan", [("Even so – a drive like that has breakers and alarms for exactly this. Something else "
                         "killed it.", "Then show me why none of the safeguards stopped it.", True)]),
}
_DATEN = {}


def _aussagen_daten(z):
    """module/<modul>/anhoerung_aussagen.json (Builder werkzeuge/eden_rise/anhoerung_aussagen.py), je Fall."""
    moddir = (z.get("plan") or {}).get("_moddir") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", z.get("modul", ""))
    pfad = os.path.join(moddir, "anhoerung_aussagen.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return {}
    if _DATEN.get(pfad, (None,))[0] != mt:
        _DATEN[pfad] = (mt, json.load(open(pfad, encoding="utf-8")))
    nr = str((ermittlung.fall(z) or {}).get("nr", ""))
    return (_DATEN[pfad][1].get("faelle") or {}).get(nr) or {}


def klartext(z):
    return _aussagen_daten(z).get("klartext") or {}


def _aussage_bauen(z, modul, v, r, stufe=0):
    """Aussage der Runde -> v["aussage"] = {sprecher, saetze: [{text, press, falsch, widerlegt}], gepresst: []}.
    stufe 1 = die nachgebesserte Aussage (Falldaten runden.<r>.nachbessern)."""
    daten = (_aussagen_daten(z).get("runden") or {}).get(r)
    if daten and stufe:
        nb = daten.get("nachbessern") or {}
        daten = dict(daten, saetze=nb.get("saetze") or [], sprecher=nb.get("sprecher") or daten["sprecher"])
    pid = v.get("angeklagt")
    v_ok = (ermittlung.fall(z) or {}).get("verantwortlich")
    if r == "person" and pid == NIEMAND:
        daten, art = None, "niemand"
    elif r == "person" and pid != v_ok:
        daten, art = None, "unschuldig"                # Unschuldige sagen die Wahrheit - kein Satz ist falsch
    elif r == "person" and daten and daten.get("sprecher") != pid:
        daten, art = None, "person"
    else:
        art = r
    nr = (ermittlung.fall(z) or {}).get("nr")
    rk = r + (".n" if stufe else "")
    if daten:
        sprecher, saetze = daten["sprecher"], [dict(s) for s in daten["saetze"]]
        for i, s in enumerate(saetze):
            s.update(key="vh.f%s.%s.%d.t" % (nr, rk, i), pkey="vh.f%s.%s.%d.p" % (nr, rk, i))
    else:
        sprecher, roh = ALLGEMEIN[art]
        wer = pid if sprecher == "{p}" else "megan"
        saetze = [{"text": t, "press": p, "falsch": f, "widerlegt": None, "key": "vh.allg.%s.%d.t.%s" % (art, i, wer),
                   "pkey": "vh.allg.%s.%d.p.%s" % (art, i, wer)} for i, (t, p, f) in enumerate(roh)]
        if art == "niemand":
            saetze[0]["falsch"] = v_ok is None         # nur wenn es wirklich niemand allein war, ist Megans Satz falsch
    sprecher = sprecher.replace("{p}", pid or "megan")
    v["aussage"] = {"sprecher": sprecher if sprecher in modul["personen"] else "megan", "saetze": saetze, "gepresst": [],
                    "fall": bool(daten), "stufe": stufe}


def _verdaechtige(z, modul):
    kreis = list((ermittlung._story(z) or {}).get("verdaechtige", [])) + \
        [p for p in (modul.get("ermittlung") or {}).get("verdacht", []) if p not in (ermittlung._story(z) or {}).get(
            "verdaechtige", [])]
    bekannt = z.get("bekannt") or modul["personen"]
    return [p for p in kreis if p in modul["personen"] and p in bekannt]


def _karte_passt(z, glied, fid):
    """-> 'ja' (Beweissatz komplett bekannt), 'luecke' (Karte gehoert dazu, aber ein Rest fehlt) oder 'nein'."""
    f = ermittlung.fall(z) or {}
    g = next((x for x in f.get("glieder", []) if x["id"] == glied), None)
    if not g:
        return "nein"
    bek = set(ermittlung.stand(z)["bekannt"])
    saetze = [set(s) for s in g["beweis_saetze"] if fid in s]
    if any(s <= bek for s in saetze):
        return "ja"
    return "luecke" if saetze else "nein"


def _zeile(v, schl, modul, **kw):
    if schl in ZEILEN:
        n = random.Random(len(v["log"]) * 31 + v["runde"] * 7 + v.get("adern", 0)).randrange(len(ZEILEN[schl]))
        wer, text, key = "megan", ZEILEN[schl][n], "vh.%s.%d" % (schl, n)
    else:
        (wer, text), key = UNVERTONT[schl], None
    p, w = v.get("angeklagt"), kw.get("w")
    wer = wer.format(p=p or "megan", w=w or "megan")
    if wer in (NIEMAND, None):
        wer = "megan"
    text = text.format(p=_name(modul, p) if p and p != NIEMAND else "them", w=_name(modul, w) if w else "",
                       s=kw.get("s", ""))
    e = {"wer": wer, "text": text, "art": schl}
    if key:
        e["key"] = key
    if kw.get("satz") is not None:
        e.update(satz=kw["satz"], r=v["runde"])        # Spalte im Client (Antwort/Rueckmeldung zu dieser Zeile)
    v["log"].append(e)


def verhandlung_beginnen(z, modul):
    """Startet die Verhandlung (aus eden.szene_starten, wenn die Szene 'anhoerung' beginnt)."""
    a = stand(z)
    a.clear()
    start, gruende = adern(z, None, modul)
    v = {"runde": 0, "schritt": "aussage", "adern": start, "max": max(start, ADERN), "gruende": gruende,
         "angeklagt": None, "log": [], "joker": [], "antibes": antibes_satz(z), "fertig": False,
         "runden": {}, "zeuge": None}
    z["verhandlung"] = v
    _moment(v, "titel", "The Hearing", sub="Megan McAllister presiding · Day 7 · the whole crew is watching",
            warte=True, effekt="klemmbrett_schritte")
    if v["antibes"]:
        flag = next((f for f in ANTIBES if f in z["flags"]), "")
        v["log"].append({"wer": "megan", "text": v["antibes"], "art": "antibes", "key": "vh.antibes." + flag})
    k = _wahl(v, len(ZEILEN["bericht"]))               # der Werftbericht, Grundlage der Anhoerung (27.10.2026)
    _moment(v, "bericht", ZEILEN["bericht"][k], key="vh.bericht.%d" % k, gefuehl="disapproval", warte=True,
            effekt="klemmbrett_schritte")
    _titel(v, "handlung", z, modul)
    _zeile(v, "einleitung_handlung", modul)
    _aussage_bauen(z, modul, v, "handlung")
    return v


def _runde(v):
    return RUNDEN[v["runde"]] if v["runde"] < len(RUNDEN) else None


def _naechste(z, modul, v):
    v["runde"] += 1
    v["schritt"] = "aussage"
    v["aussage"] = None
    if v["adern"] <= 0:
        for r in RUNDEN:
            v["runden"].setdefault(r, "verloren")
        _zeile(v, "geduld_weg", modul)
        v["log"][-1].update(moment=True, effekt="blackout", warte=True)
        _abschluss(z, modul, v, fertig=False)
        return _urteil_sprechen(z, modul, v, None)     # Megan urteilt ohne Rolle und Plaedoyer
    r = _runde(v)
    if r is None:
        folge = v["runden"].get("folge")
        if folge in ("gestaendnis", "bluff"):          # bewiesen hat das Kettenbrett schon _treffer gezeigt
            _kette(v, "zu" if all(v["runden"].get(x) in GEWONNEN for x in RUNDEN) else "zu_teil")
            _blick(v, z)
        elif folge not in GEWONNEN:
            _kette(v, "riss")
        _gestaendnis_rede(z, modul, v)
        _zeile(v, "ende", modul)
        v["log"][-1].update(moment=True)
        _moment(v, "titel", "The Verdict", sub="Your own part · your plea · Megan's decision", warte=True,
                effekt="anhoerung_wende")
        _abschluss(z, modul, v, fertig=False)
        v["schritt"] = "rolle"
        _zeile(v, "rolle_frage", modul)
        return
    _titel(v, r, z, modul)
    if r == "person":
        v["schritt"] = "anklage"
        _plaedoyers(z, modul, v)
        _zeile(v, "anklage_auf", modul)
        return
    if r == "folge":
        _kette(v, "auf" if all(v["runden"].get(x) in GEWONNEN for x in RUNDEN[:2]) else "luecke")
    _zeile(v, "einleitung_" + r, modul)
    _aussage_bauen(z, modul, v, r)
    _gestaendnis_pruefen(z, modul, v)


def _gestaendnis_pruefen(z, modul, v):
    """Ein Gestaendnis ersetzt sein Glied (wie ermittlung.glieder_status) - die Runde ist dann sofort gewonnen."""
    e, f = ermittlung.stand(z), ermittlung.fall(z) or {}
    ersetzt = (f.get("gestaendnis") or {}).get("ersetzt_glied") if e.get("gestaendnis") else None
    r = _runde(v)
    if r and r == ersetzt and (r != "person" or v["angeklagt"] == f.get("verantwortlich")):
        v["runden"][r] = "gestaendnis"
        _zeile(v, "gestaendnis", modul)
        _naechste(z, modul, v)


def verhandlung_anklage(z, modul, pid):
    v = z["verhandlung"]
    if v["fertig"] or _runde(v) != "person" or v["schritt"] != "anklage":
        raise ValueError("Jetzt wird niemand angeklagt.")
    if pid != NIEMAND and pid not in _verdaechtige(z, modul):
        raise ValueError("Unbekannte Person.")
    v["angeklagt"] = pid
    v["schritt"] = "aussage"
    saal = [p for p in RAUNEN if p != pid and p in modul["personen"]]
    if pid not in TRATSCH_ANKLAGE and saal:             # Spotlight: der Saal dreht sich um (sonst tratscht er gleich)
        p = saal[_wahl(v, len(saal))]
        _moment(v, "publikum", RAUNEN[p], wer=p, key="vh.raunen." + p, gefuehl="surprise")
    if pid in REAKTION:
        text, gef = REAKTION[pid]
        _moment(v, "reaktion", text, wer=pid, key="vh.reaktion.%s" % pid, gefuehl=gef)
    if pid in TRATSCH_ANKLAGE:
        _tratsch(z, modul, v, TRATSCH_ANKLAGE[pid], "vh.tratsch.anklage." + pid)
    if pid == NIEMAND:
        _moment(v, "titel", "Nobody alone", sub="Point 2 of 3 · Megan puts the case to you", warte=True,
                knopf="Hear the statement", effekt="phase_wechsel")
    else:
        _moment(v, "titel", "Testimony of %s" % _name(modul, pid), sub="Point 2 of 3 · the accused answers for "
                "themselves", warte=True, knopf="Hear the statement", effekt="phase_wechsel")
    _zeile(v, "einleitung_niemand" if pid == NIEMAND else "einleitung_person", modul)
    _aussage_bauen(z, modul, v, "person")
    if pid != NIEMAND:
        zg = next((w for w in zeugen(z, modul, pid) if w["luegt"]), None)
        if zg:
            v["zeuge"] = zg["pid"]
            anruf = not an_bord(z, modul, zg["pid"])  # nicht an Bord: per Videoanruf auf Megans Tablet
            v["zeuge_anruf"] = anruf
            if anruf:
                _zeile(v, "zeuge_anruf", modul)
            if zg["pid"] in ZEUGE:                     # steht auf und redet dazwischen
                _moment(v, "zeuge", ZEUGE[zg["pid"]], wer=zg["pid"], key="vh.zeuge." + zg["pid"], gefuehl="caring",
                        anruf=anruf)
            else:
                _zeile(v, "person_zeuge", modul, w=zg["pid"])
    _gestaendnis_pruefen(z, modul, v)


def _satz(v, satz):
    saetze = (v.get("aussage") or {}).get("saetze") or []
    if satz is None and len(saetze) == 1:
        satz = 0
    if satz is None or not 0 <= int(satz) < len(saetze):
        raise ValueError("Wähle zuerst die Zeile, die du anzweifelst.")
    return int(satz), saetze[int(satz)]


def verhandlung_press(z, modul, satz=None):
    """Nachhaken zu einer Zeile: kostenlos, beliebig oft. Bei der falschen Zeile stutzt Duc, und der Stapel mit dem
    passenden Zettel leuchtet auf."""
    v = z["verhandlung"]
    r = _runde(v)
    if v["fertig"] or not r or v["schritt"] != "aussage":
        raise ValueError("Hier gibt es nichts nachzuhaken.")
    i, s = _satz(v, satz)
    a = v["aussage"]
    if i not in a["gepresst"]:
        a["gepresst"].append(i)
    v["log"].append({"wer": a["sprecher"], "text": s["press"], "art": "press", "satz": i, "r": v["runde"],
                     "key": s.get("pkey")})
    if not s["falsch"]:
        bek = ermittlung.stand(z)["bekannt"]
        fid = next((f for f in s.get("stuetzt") or [] if f in bek), None)
        if fid:                                        # Ausschlussverfahren (Duc 25.10.): wahre Zeile sichtbar abhaken
            F = ermittlung.fakten(z)
            v["log"].append({"wer": "duc", "text": klartext(z).get(fid) or (F.get(fid) or {}).get("codex", fid),
                             "art": "bestaetigt", "satz": i, "r": v["runde"]})
    pid = v.get("angeklagt")
    if s["falsch"] and r == "person" and a["sprecher"] == pid and pid in NERVOES:
        n = _wahl(v, len(NERVOES[pid]))
        v["log"].append({"wer": pid, "text": NERVOES[pid][n], "art": "nervoes", "satz": i, "r": v["runde"],
                         "key": "vh.nervoes.%s.%d" % (pid, n), "gefuehl": "nervousness"})
    if s["falsch"]:
        v["log"].append({"wer": "duc", "text": s.get("gedanke") or GEDANKE_ZWEIFEL, "art": "gedanke", "satz": i,
                         "r": v["runde"]})
        fid = _beste_karte(z, r, s)
        if fid:
            v.setdefault("tipp_stapel", {})[r] = karte_einordnen(modul, ermittlung.fakten(z).get(fid) or {})[0]


def _beste_karte(z, r, s):
    """Fakt-ID fuer den Stapel-Hinweis (verlaesst den Server nicht): bekannte widerlegende Karte, sonst Beweissatz."""
    bek = ermittlung.stand(z)["bekannt"]
    kandidaten = s.get("widerlegt") or []
    for fid in kandidaten:
        if fid in bek and _karte_passt(z, r, fid) == "ja":
            return fid
    for fid in kandidaten:
        if fid in bek:
            return fid
    return _tipp(z, r)[1]


def _tipp(z, glied):
    """Erster Beweissatz, von dem Duc schon etwas kennt (sonst der erste). -> (Art auf Englisch, Fakt-ID)."""
    f = ermittlung.fall(z) or {}
    g = next((x for x in f.get("glieder", []) if x["id"] == glied), None)
    if not g:
        return "", None
    F, bek = ermittlung.fakten(z), set(ermittlung.stand(z)["bekannt"])
    saetze = sorted(g["beweis_saetze"], key=lambda s: -len(set(s) & bek))
    for fid in saetze[0]:
        x = F.get(fid) or {}
        if x.get("zuverlaessigkeit") in ("gesichert", "belastbar"):
            return ART_EN.get(x.get("art"), ""), fid
    fid = saetze[0][0]
    return ART_EN.get((F.get(fid) or {}).get("art"), ""), fid


def verhandlung_present(z, modul, fid, satz=None):
    """Zeile anzweifeln + Zettel legen. Richtig: die Zeile ist die falsche UND der Zettel widerlegt sie UND Duc kennt
    den Rest des Beweissatzes. Teilbeweis ('luecke') kostet nichts, Megan fragt nach. Sonst -1 Ader."""
    v = z["verhandlung"]
    r = _runde(v)
    if v["fertig"] or not r or v["schritt"] != "aussage":
        raise ValueError("Jetzt kannst du nichts vorlegen.")
    if fid not in ermittlung.stand(z)["bekannt"]:
        raise ValueError("Diesen Fakt kennst du nicht.")
    i, s = _satz(v, satz)
    F = ermittlung.fakten(z)
    v["log"].append({"wer": "duc", "text": klartext(z).get(fid) or (F.get(fid) or {}).get("codex", fid), "art": "karte",
                     "satz": i, "r": v["runde"]})
    passt = _karte_passt(z, r, fid)
    v_ok = (ermittlung.fall(z) or {}).get("verantwortlich")
    if r == "person" and v["angeklagt"] != (v_ok or NIEMAND):
        if passt == "ja":                              # stimmt, beweist aber jemand anderen (kein Raten, keine Ader)
            v["runden"][r] = "verloren"
            _zeile(v, "anderswo", modul)
            pid = v["angeklagt"]
            if pid in AUFATMEN:
                _moment(v, "aufatmen", AUFATMEN[pid], wer=pid, key="vh.aufatmen." + pid, gefuehl="relief")
            return _naechste(z, modul, v)
        v["adern"] -= 1
        _zeile(v, "falsche_karte", modul, s=s["text"], satz=i)
        _konter(v, r)
    elif not s["falsch"]:
        v["adern"] -= 1
        _zeile(v, "satz_haelt", modul, satz=i)
        _konter(v, r)
    elif _beruehrt(s, fid, passt):
        if passt == "ja":
            if _nachbessern(z, modul, v, r):
                return
            v["runden"][r] = "beweis"
            _treffer(z, modul, v, r)
            return _naechste(z, modul, v)
        _zeile(v, "luecke", modul, satz=i)
        return
    else:
        v["adern"] -= 1
        _ablehnen(z, modul, v, r, s, i, fid)
        _konter(v, r)
    if v["adern"] <= 0:
        v["runden"][r] = "verloren"
        return _naechste(z, modul, v)


def _beruehrt(s, fid, passt):
    """Luise/Duc 28.10.2026: Eine Notiz zaehlt gegen eine falsche Zeile, wenn sie zum Beweissatz des Punkts gehoert UND
    die Behauptung dieser Zeile beruehrt (Falldaten: widerlegt + beruehrt). Allgemeine Zeilen ohne Liste: jede Notiz
    aus einem Beweissatz des Punkts."""
    if not s.get("widerlegt") and not s.get("beruehrt"):
        return passt != "nein"
    return passt != "nein" and fid in set(s.get("widerlegt") or []) | set(s.get("beruehrt") or [])


def _ablehnen(z, modul, v, r, s, i, fid):
    """Ablehnung mit Grund: eigener Satz aus den Falldaten (warum_nicht) oder eine von drei Kategorien."""
    eigen = (s.get("warum_nicht") or {}).get(fid)
    if eigen:
        e = {"wer": "megan", "text": eigen, "art": "warum_nicht", "satz": i, "r": v["runde"]}
        if s.get("key"):
            e["key"] = s["key"][:-2] + ".wn." + fid          # vh.f1.person.0.t -> vh.f1.person.0.wn.<fid>
        v["log"].append(e)
        return
    F = ermittlung.fakten(z)
    f = F.get(fid) or {}
    im_punkt = any(fid in satz for g in (ermittlung.fall(z) or {}).get("glieder", []) if g["id"] == r
                   for satz in g["beweis_saetze"])
    if not im_punkt and r not in themen(z, fid, f):
        kat = "anderer_punkt"
    elif f.get("zuverlaessigkeit") == "aussage":
        kat = "nur_aussage"
    elif im_punkt:
        kat = "andere_behauptung"
    else:
        kat = "falsche_karte"
    _zeile(v, kat, modul, s=s["text"], satz=i)


def _nachbessern(z, modul, v, r):
    """Erster Treffer in einem Punkt mit nachgebesserter Aussage: OBJECTION!, der Zeuge rudert zurueck, neue Aussage.
    -> True, wenn nachgebessert wurde (der Punkt ist dann noch offen)."""
    a = v.get("aussage") or {}
    daten = (_aussagen_daten(z).get("runden") or {}).get(r) or {}
    nb = daten.get("nachbessern")
    if not nb or not a.get("fall") or a.get("stufe"):
        return False
    nr = (ermittlung.fall(z) or {}).get("nr")
    sp = a["sprecher"]
    _moment(v, "objection", OBJECTION[_wahl(v, len(OBJECTION))], wer="duc", effekt="anhoerung_einspruch")
    _moment(v, "nachbessern", nb["auftakt"], wer=sp, key="vh.f%s.%s.n.auftakt" % (nr, r), gefuehl=nb.get("gefuehl"))
    if sp != "megan":
        k = _wahl(v, len(ZEILEN["nachgebessert"]))
        _moment(v, "ruhe", ZEILEN["nachgebessert"][k], key="vh.nachgebessert.%d" % k, gefuehl="disapproval")
    else:                                              # Megan liest die korrigierte Fassung der Werft - mit Spitze
        k = _wahl(v, len(ZEILEN["werft_nachgebessert"]))
        _moment(v, "ruhe", ZEILEN["werft_nachgebessert"][k], key="vh.werft_nachgebessert.%d" % k,
                gefuehl="annoyance")
    _moment(v, "titel", "Revised testimony", sub="Point %d of 3 · one more lie to catch" % (RUNDEN.index(r) + 1),
            warte=True, knopf="Hear the new version", effekt="anhoerung_wende")
    _aussage_bauen(z, modul, v, r, stufe=1)
    return True


def _konter(v, r):
    """Die Angeklagte stichelt, wenn Duc danebenliegt (nur in ihrer eigenen Aussage)."""
    pid = v.get("angeklagt")
    if r == "person" and pid in KONTER and (v.get("aussage") or {}).get("sprecher") == pid and v["adern"] > 0:
        n = _wahl(v, len(KONTER[pid]))
        v["log"].append({"wer": pid, "text": KONTER[pid][n], "art": "konter", "key": "vh.konter.%s.%d" % (pid, n),
                         "gefuehl": "pride"})


def verhandlung_bluff(z, modul):
    from . import wuerfel
    v = z["verhandlung"]
    r = _runde(v)
    if v["fertig"] or not r or v["schritt"] != "aussage":
        raise ValueError("Jetzt gibt es nichts zu bluffen.")
    att = max(WERTE, key=lambda a: z["persona"]["attribute"].get(a, 0) + charms.attribut(z, a))
    bonus = z["persona"]["attribute"].get(att, 0) + charms.attribut(z, att)        # Jacken-Charm (28.10.2026)
    p = wuerfel.probe(att, BLUFF_SG, [(WERTE[att], bonus)])
    v["log"].append({"wer": "duc", "text": "You bluff (%s %d+%d = %d against %d)." % (
        WERTE[att], p["wurf"], bonus, p["summe"], BLUFF_SG), "art": "bluff"})
    if p["ergebnis"] in ("erfolg", "kritisch"):
        v["runden"][r] = "bluff"
        _zeile(v, "bluff_ja", modul)
    else:
        v["runden"][r] = "bluff" if (v.get("aussage") or {}).get("stufe") else "verloren"   # halb bewiesen
        v["adern"] -= 2
        _zeile(v, "bluff_nein", modul)
    _naechste(z, modul, v)
    return p


def verhandlung_aufgeben(z, modul):
    v = z["verhandlung"]
    r = _runde(v)
    if v["fertig"] or not r or v["schritt"] != "aussage":
        raise ValueError("Jetzt gibt es nichts aufzugeben.")
    if (v.get("aussage") or {}).get("stufe"):          # die erste Luege ist schon entlarvt: halb bewiesen
        v["runden"][r] = "bluff"
        _zeile(v, "halb", modul)
        return _naechste(z, modul, v)
    v["runden"][r] = "verloren"
    _zeile(v, "aufgeben", modul)
    if r != "folge":
        _offen(z, modul, v, r)
    _naechste(z, modul, v)


def joker_items(z, modul):
    return [i for i in dict.fromkeys(z.get("inventar", [])) if (modul["items"].get(i) or {}).get("anhoerung_ader")]


def verhandlung_joker(z, modul, iid):
    v = z["verhandlung"]
    if v["fertig"] or iid not in joker_items(z, modul):
        raise ValueError("Diesen Joker hast du nicht.")
    z["inventar"].remove(iid)
    n = modul["items"][iid]["anhoerung_ader"]
    v["adern"] = min(v["max"] + 1, v["adern"] + n)
    v["joker"].append(iid)
    v["log"].append({"wer": "duc", "text": modul["items"][iid].get("label", iid), "art": "joker"})
    _zeile(v, "joker", modul)


def verhandlung_rolle(z, modul, ehrlich):
    """Duc 26.10. (Variante A): Ducs eigene Rolle wird in der Anhoerung gewaehlt, nicht mehr in einer eigenen Szene."""
    from . import zustand
    v = z["verhandlung"]
    if v["fertig"] or v["schritt"] != "rolle":
        raise ValueError("Jetzt fragt Megan nicht nach deiner Rolle.")
    folgen, _, zeilen = rolle(z, modul, ehrlich)
    v.setdefault("urteil_zeilen", []).extend(zeilen + zustand.folgen_anwenden(z, modul, folgen))
    v["log"].append({"wer": "duc", "art": "rolle", "text": "You tell Megan everything – including what you did wrong."
                     if ehrlich else "You keep your own part to yourself."})
    _zeile(v, "rolle_ehrlich" if ehrlich else "rolle_schweigen", modul)
    v["schritt"] = "plaedoyer"
    _zeile(v, "plaedoyer_frage", modul)


def verhandlung_plaedoyer(z, modul, art):
    v = z["verhandlung"]
    if v["fertig"] or v["schritt"] != "plaedoyer" or art not in PLAEDOYER_EN:
        raise ValueError("Jetzt gibt es kein Plaedoyer.")
    v["log"].append({"wer": "duc", "art": "plaedoyer_wahl", "text": PLAEDOYER_KARTE[art][0]})
    _urteil_sprechen(z, modul, v, art)


PLAEDOYER_KARTE = {"gnade": ("Ask for mercy", "Let them stay aboard."),
                   "teilen": ("Share the blame", "Carry part of it yourself."),
                   "strafe": ("Demand the full penalty", "If the proof holds, they leave the boat today.")}


def _urteil_sprechen(z, modul, v, art):
    """Megan entscheidet (Stille-Beat), spricht das Urteil, die Angeklagte reagiert, die Crew tratscht, Schluss."""
    from . import zustand
    a = stand(z)
    if art:
        folgen, _, zeilen = plaedoyer(z, modul, art)
    else:
        u = urteil(z, None)
        a["urteil"] = ermittlung.stand(z)["urteil"] = u
        folgen, zeilen = list(FOLGEN[u]), ["⚖ Urteil: " + URTEIL_DE[u] % {"n": _name(modul, a.get("angeklagt"))
                                                                         if a.get("angeklagt") not in (None, NIEMAND) else ""}]
    folgen.append({"flag": "verhandlung_urteil"})      # die Szenen anhoerung_rolle/_urteil entfallen (hauptstory)
    v.setdefault("urteil_zeilen", []).extend(zeilen + zustand.folgen_anwenden(z, modul, folgen))
    fam = a.get("folge") or a["urteil"]
    v["urteil"] = fam
    pid0 = a.get("angeklagt")
    v["urteil_text"] = URTEIL_KURZ_EN[fam] % {"n": _name(modul, pid0) if pid0 not in (None, NIEMAND) else "nobody"} + (
        " Megan's bonus: +%d €." % a["praemie"] if a.get("praemie") else "") + (
        " You offered to share the blame." if a.get("plaedoyer") == "teilen" else "")
    v["schritt"] = "urteil"
    _moment(v, "titel", "Megan decides …", sub="The salon is silent", effekt="klemmbrett_schritte")
    _moment(v, "urteil", ZEILEN["urteil_" + fam][0], key="vh.urteil_%s.0" % fam, gefuehl=URTEIL_GEFUEHL.get(fam),
            warte=True, effekt="anhoerung_hammer",           # Hammer, danach der Ausgangs-Klang (26.10.2026)
            effekt2="mission_erfolg" if fam in ("erbarmen", "aufgeklaert", "entlastet") else "mission_fehlschlag")
    pid = a.get("angeklagt")
    if a.get("verrat") and pid in URTEIL_VERRAT:
        _moment(v, "urteil_reaktion", URTEIL_VERRAT[pid], wer=pid, key="vh.urteil_verrat." + pid, gefuehl="anger")
    elif pid in URTEIL_REAKTION and fam in URTEIL_REAKTION[pid]:
        _moment(v, "urteil_reaktion", URTEIL_REAKTION[pid][fam], wer=pid, key="vh.urteil_reaktion.%s.%s" % (pid, fam),
                gefuehl=REAKTION_GEFUEHL.get(fam))
    tr = "falsch_strafe" if a.get("strafe_unschuldig") else fam
    if tr in TRATSCH_URTEIL:
        _tratsch(z, modul, v, TRATSCH_URTEIL[tr], "vh.tratsch.urteil." + tr)
    if a.get("praemie"):
        kat = "praemie_voll" if a["praemie"] >= PRAEMIE else "praemie_halb"
        _moment(v, "punkt", ZEILEN[kat][0], key="vh.%s.0" % kat, gefuehl="approval", warte=True, effekt="geld_ein")
    _zeile(v, "schluss", modul)
    v["log"][-1].update(moment=True)
    _moment(v, "titel", "The hearing is closed", sub="Day 7 · the salon empties", warte=True, effekt="phase_wechsel")
    v["fertig"] = True


def _abschluss(z, modul, v, fertig=True):
    """Beweisaufnahme vorbei: Ergebnis wie bei anklagen() festhalten (Vorwurf, Zeugen, Adern). Seit 26.10. folgen
    Rolle, Plaedoyer und Urteil noch in der Anhoerung (fertig=False)."""
    if fertig:
        v["fertig"] = True
        v["schritt"] = "fertig"
    a = stand(z)
    pid = v["angeklagt"]
    a.update(angeklagt=pid, adern=max(0, v["adern"]), runden=dict(v["runden"]), gespielt=True,
             zeugen=zeugen(z, modul, pid if pid not in (None, NIEMAND) else None))
    if pid and pid != NIEMAND:
        e = ermittlung.stand(z)
        bel = belegt(z) and pid == (ermittlung.fall(z) or {}).get("verantwortlich")
        alt = next((x for x in e["vorwuerfe"] if x["pid"] == pid), None)
        if alt:
            alt.update(oeffentlich=True, belegt=alt.get("belegt") or bel)
        else:
            e["vorwuerfe"].append({"pid": pid, "tag": z["tag"], "oeffentlich": True, "belegt": bel})
    ermittlung.megan_haltung(z)


def verhandlung_hinweis(z, modul):
    """Erzaehlauftrag fuer die Szene nach der Verhandlung (Megan schliesst ab, kein Urteil)."""
    v = z.get("verhandlung") or {}
    pid = v.get("angeklagt")
    wer = "nobody alone" if pid == NIEMAND else (_name(modul, pid) if pid else "no one")
    gewonnen = sum(1 for x in v.get("runden", {}).values() if x in ("beweis", "bluff", "gestaendnis"))
    u = stand(z).get("folge") or stand(z).get("urteil")
    if u in URTEIL_EN:
        return ("[The hearing is over - this reply] Duc named %s and carried %d of 3 points. Megan has already passed "
                "her verdict: %s The crew leaves the salon; one or two quiet sentences, no new verdict.\n\n"
                % (wer, gewonnen, URTEIL_EN[u] % {"n": _name(modul, pid) if pid and pid != NIEMAND else "nobody"}))
    return ("[The hearing - this reply] The questioning is over. Duc named %s. He carried %d of 3 points before Megan; "
            "her patience is at %d. Megan closes the questioning in one or two sentences, in character. No verdict "
            "yet - she will hear Duc once more.\n\n" % (wer, gewonnen, max(0, v.get("adern", 0))))


def _erbarmen_liste(z):
    """Was Megan fuer Gnade braucht - offen gezeigt, damit die Wahl fair ist (ohne 'richtige Person': die zeigt Punkt 2)."""
    fehlt = erbarmen_moeglich(z)[1]
    return [{"text": "Real proof for all three points", "ok": not {"volle Kette", "Beweise statt Bluff"} & set(fehlt)},
            {"text": "You know why it happened", "ok": "Motiv" not in fehlt},
            {"text": "You were honest about your own part", "ok": "Ducs Ehrlichkeit" not in fehlt},
            {"text": "Megan still has patience left", "ok": "Megans Geduld" not in fehlt}]


def verhandlung_ansicht(z, modul, sprite):
    """Fuer den Client: Runde, Aussagen, Karten, Knoepfe. sprite(pid, gefuehl) -> URL."""
    v = z.get("verhandlung")
    if not v:
        return None
    F, bek = ermittlung.fakten(z), ermittlung.stand(z)["bekannt"]
    klar = klartext(z)
    karten = []
    for i, fid in enumerate(bek):
        f = F.get(fid)
        if not f:
            continue
        st, icon, quelle, wer = karte_einordnen(modul, f)
        karten.append({"id": fid, "text": f.get("codex", fid), "klar": klar.get(fid), "art": f.get("art", ""),
                       "runden": themen(z, fid, f),
                       "zuv": f.get("zuverlaessigkeit", ""), "stapel": st, "icon": icon, "wer": wer,
                       "portrait": sprite(quelle, "neutral") if quelle else None, "_rang": (ZUV_RANG.get(
                           f.get("zuverlaessigkeit"), 9), -i)})
    karten.sort(key=lambda k: k.pop("_rang"))
    stapel = [{"id": s, "titel": STAPEL_EN[s], "anzahl": sum(1 for k in karten if k["stapel"] == s)} for s in STAPEL]
    r = _runde(v)
    pid = v.get("angeklagt")
    figuren = ["megan"] + ([pid] if pid and pid != NIEMAND else [])
    letzter = next((e["wer"] for e in reversed(v["log"]) if e["wer"] not in ("duc",)), "megan")
    gef = GEFUEHL
    letzte_art = next((e["art"] for e in reversed(v["log"]) if e["wer"] == "megan"), "")
    return {
        "runde": v["runde"], "runden": [{"id": x, "titel": RUNDE_TITEL[x], "ergebnis": v["runden"].get(x)} for x in RUNDEN],
        "titel": RUNDE_TITEL.get(r, ""), "schritt": v["schritt"], "adern": max(0, v["adern"]), "max": v["max"],
        "log": [dict(e, n=i, sprite=sprite(e["wer"], e.get("gefuehl") or "neutral")
                     if e["wer"] == "duc" or e.get("moment") and e["wer"] in modul["personen"] else None,
                     **({"gruppe_bilder": [{"id": p, "name": _name(modul, p), "sprite": sprite(p, "neutral")}
                                           for p in e["gruppe"]]} if e.get("gruppe") else {}))
                for i, e in enumerate(v["log"])][-24:], "karten": karten, "stapel": stapel, "tipp_stapel": (v.get("tipp_stapel") or {}).get(r),
        "aussage": {"sprecher": (v.get("aussage") or {}).get("sprecher"), "name": _name(modul, (v.get("aussage") or {}).get(
            "sprecher") or "megan"), "saetze": [{"text": s["text"], "key": s.get("key"), "gepresst": i in v["aussage"]["gepresst"]}
                                                for i, s in enumerate(v["aussage"]["saetze"])]} if v.get("aussage") else None,
        "angeklagt": pid, "fertig": v["fertig"],
        # Gefuehrte erste Zeile (Duc 29.10.2026): nur Punkt 1, erste Aussage - welche Zeile der Client als Beispiel fuehrt
        "fuehrung": next((i for i, s in enumerate((v.get("aussage") or {}).get("saetze") or []) if s.get("falsch")), None)
        if v["runde"] == 0 and v["schritt"] == "aussage" and not v["fertig"] and not (v.get("aussage") or {}).get("stufe")
        else None,
        "verdaechtige": [{"id": p, "name": _name(modul, p), "sprite": sprite(p, "neutral")}
                         for p in _verdaechtige(z, modul)] + [{"id": NIEMAND, "name": "Nobody alone", "sprite": None}]
        if v["schritt"] == "anklage" else [],
        "figuren": [{"id": p, "name": _name(modul, p), "spricht": p == letzter,
                     "sprite": sprite(p, gef.get(letzte_art, "neutral") if p == "megan" else
                                      next((e.get("gefuehl") or "neutral" for e in reversed(v["log"]) if e["wer"] == p),
                                           "neutral"))} for p in figuren],
        "zeuge": {"id": v["zeuge"], "name": _name(modul, v["zeuge"]), "anruf": bool(v.get("zeuge_anruf")),
                  "sprite": sprite(v["zeuge"], "neutral")} if v.get("zeuge") else None,
        "joker": [{"id": i, "label": modul["items"][i].get("label", i), "plus": modul["items"][i]["anhoerung_ader"]}
                  for i in joker_items(z, modul)],
        "bluff": {"wert": WERTE[max(WERTE, key=lambda a: z["persona"]["attribute"].get(a, 0) + charms.attribut(z, a))],
                  "bonus": max(z["persona"]["attribute"].get(a, 0) + charms.attribut(z, a) for a in WERTE), "sg": BLUFF_SG},
        "namen": {p: _name(modul, p) for p in set(figuren) | {e["wer"] for e in v["log"]} | ({v["zeuge"]} if v.get("zeuge")
                  else set()) if p in modul["personen"]},
        "ungeduld": [{"key": "vh.ungeduld.%d" % n, "text": s} for n, s in enumerate(ZEILEN["ungeduld"])],
        "megan_ungeduld": sprite("megan", GEFUEHL["ungeduld"]),
        "duc_sprite": sprite("duc", "neutral"),            # Duc from the front, as in the Character menu (jacket + weapon, 29.10.2026)
        "plaedoyer": [{"id": k, "titel": t, "text": x} for k, (t, x) in PLAEDOYER_KARTE.items()]
        if v["schritt"] == "plaedoyer" else [],
        "erbarmen": _erbarmen_liste(z) if v["schritt"] == "plaedoyer" else [],
        "urteil_text": v.get("urteil_text") if v["fertig"] else None,
        "stufe": (v.get("aussage") or {}).get("stufe", 0),
        "bilanz": {"gefunden": len([f for f in bek if f in F]), "gesamt": len(F),
                   "besser": v.get("urteil") not in (None, "erbarmen", "entlastet")} if v["fertig"] else None,
        "rolle_ehrlich": stand(z).get("rolle_ehrlich") if v["fertig"] and "rolle_ehrlich" in stand(z) else None,
    }


# ------------------------------------------------------------------ Vertonung (/api/zeile, vertonen_eden_rise.py)
def _aussagen_alle(moddir):
    try:
        return json.load(open(os.path.join(moddir, "anhoerung_aussagen.json"), encoding="utf-8")).get("faelle") or {}
    except OSError:
        return {}


def alle_zeilen(modul, moddir):
    """-> [(schluessel, sprecher, text)] - alles, was in der Anhoerung gesprochen wird."""
    out = [("vh.%s.%d" % (k, n), "megan", s) for k, liste in ZEILEN.items() for n, s in enumerate(liste)]
    out += [("vh.antibes." + f, "megan", s) for f, s in ANTIBES.items()]
    out += [("vh.publikum.%s.%d" % (p, n), p, s) for p, liste in PUBLIKUM.items() for n, s in enumerate(liste)]
    out += [("vh.reaktion." + p, p, s) for p, (s, _) in REAKTION.items()]
    out += [("vh.plaedoyer.%s.%d" % (p, n), p, s) for p, liste in PLAEDOYER.items() for n, s in enumerate(liste)]
    for name, tab in (("nervoes", NERVOES), ("konter", KONTER), ("zusammenbruch", ZUSAMMENBRUCH)):
        out += [("vh.%s.%s.%d" % (name, p, n), p, s) for p, liste in tab.items() for n, s in enumerate(liste)]
    for name, tab in (("raunen", RAUNEN), ("aufatmen", AUFATMEN), ("zeuge", ZEUGE), ("blick", BLICK)):
        out += [("vh.%s.%s" % (name, p), p, s) for p, s in tab.items()]
    out += [("vh.tratsch.handlung.%d" % i, p, s) for i, (p, s) in enumerate(TRATSCH_HANDLUNG)]
    for name, tab in (("anklage", TRATSCH_ANKLAGE), ("bruch", TRATSCH_BRUCH), ("urteil", TRATSCH_URTEIL)):
        out += [("vh.tratsch.%s.%s.%d" % (name, k, i), p, s) for k, liste in tab.items() for i, (p, s) in enumerate(liste)]
    out += [("vh.urteil_reaktion.%s.%s" % (p, f), p, s) for p, d in URTEIL_REAKTION.items() for f, s in d.items()]
    out += [("vh.urteil_verrat." + p, p, s) for p, s in URTEIL_VERRAT.items()]
    for nr, fall in _aussagen_alle(moddir).items():
        pl = ((fall.get("runden") or {}).get("person") or {})
        out += [("vh.f%s.tratsch.%d" % (nr, i), p, s) for i, (p, s) in enumerate(fall.get("tratsch") or [])]
        out += [("vh.f%s.gestaendnis.%d" % (nr, i), pl.get("sprecher"), s) for i, (s, _) in enumerate(fall.get("gestaendnis") or [])]
        out += [("vh.f%s.plaedoyer.%d" % (nr, i), pl.get("sprecher"), s) for i, s in enumerate(pl.get("plaedoyer") or [])]
        for r, a in (fall.get("runden") or {}).items():
            for i, s in enumerate(a["saetze"]):
                out += [("vh.f%s.%s.%d.t" % (nr, r, i), a["sprecher"], s["text"]),
                        ("vh.f%s.%s.%d.p" % (nr, r, i), a["sprecher"], s["press"])]
                out += [("vh.f%s.%s.%d.wn.%s" % (nr, r, i, fid), "megan", w) for fid, w in (s.get("warum_nicht") or {}).items()]
            nb = a.get("nachbessern")
            if nb:
                sp = nb.get("sprecher") or a["sprecher"]
                out.append(("vh.f%s.%s.n.auftakt" % (nr, r), sp, nb["auftakt"]))
                for i, s in enumerate(nb.get("saetze") or []):
                    out += [("vh.f%s.%s.n.%d.t" % (nr, r, i), sp, s["text"]), ("vh.f%s.%s.n.%d.p" % (nr, r, i), sp, s["press"])]
                    out += [("vh.f%s.%s.n.%d.wn.%s" % (nr, r, i, fid), "megan", w)
                            for fid, w in (s.get("warum_nicht") or {}).items()]
    verdacht = list(dict.fromkeys(((modul.get("ermittlung") or {}).get("verdacht") or []) + ["chiara", "lea", "sophia",
                                                                                              "rosi", "yasin"]))
    for art, (sprecher, roh) in ALLGEMEIN.items():
        for wer in ([p for p in verdacht if p in modul["personen"]] if sprecher == "{p}" else ["megan"]):
            for i, (tx, pr, _) in enumerate(roh):
                out += [("vh.allg.%s.%d.t.%s" % (art, i, wer), wer, tx), ("vh.allg.%s.%d.p.%s" % (art, i, wer), wer, pr)]
    return out


def zeile(zid, modul, moddir):
    """Schluessel vh.* -> (sprecher, text) oder (None, None) - nur bekannte Saetze, nie freier Text."""
    for k, wer, text in alle_zeilen(modul, moddir):
        if k == zid:
            return wer, text
    return None, None

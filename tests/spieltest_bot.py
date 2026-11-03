# -*- coding: utf-8 -*-
r"""Play-test bot: nine review profiles or six classical types, up to the built calendar end.
Profile event choices use visible text heuristics; other mechanics still use engine state (hybrid knowledge).
No language model, no voice, no network, throw-away folder - like the gate.

The gate (tests/lauf_test.py) stays the fixed regression check. This bot is the broad one: it enters places, fishes, gathers,
farms, answers the phone, investigates and fights like the type it plays. Run it through tests/spieltest.py.

  python tests\spieltest_bot.py sammler 1 out.json     one run, writes the raw measurements

Output holds ids and numbers only, never story text: the state contains case solutions (spoilers).
"""
import collections, hashlib, json, os, random, re, shutil, struct, sys, tempfile, traceback

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402  (stubs, fixed hash seed)
from spieltest_profile import PROFILE, VERSION
from spieltest_verhalten import antwort_werten, geste_waehlen, date_signale

E = L.eden
MAX_SCHRITTE = 60000


def trainiert(z):
    """Heute schon trainiert? Jede weitere Runde gibt keine Erfahrung (kern/tutorial.aufgabe_vergeben); ein Mensch liest
    das und hoert auf (Main Chat 03.11.2026: Tandi trainierte 40-mal ohne Erfahrung)."""
    return (z.get("training_kampf") or {}).get("aufgabe_tag") == z.get("tag")
PHASE_MAX = 400          # steps in one phase before the bot leaves on purpose (a loop in the bot, not yet a bug)
ABLEHNUNGEN_MAX = 25     # refused actions in a row without progress: the game offers nothing that works

# parade = chance of perfect / perfect or good; hand = skill in the minigames; schwierig = fight style
TYPEN = {
    "sammler": {"parade": (.55, .90), "hand": .8, "stil": "klug", "modus": "ironman"},
    "romantiker": {"parade": (.35, .75), "hand": .5, "stil": "einfach", "modus": "entspannt"},
    "kaempfer": {"parade": (.55, .90), "hand": .7, "stil": "klug", "modus": "ironman"},
    "sparer": {"parade": (.35, .75), "hand": .6, "stil": "einfach", "modus": "ironman"},
    "schwach": {"parade": (.15, .45), "hand": .25, "stil": "einfach", "modus": "ironman"},
    "chaos": {"parade": (.33, .66), "hand": .5, "stil": "zufall", "modus": "ironman"},
}
# Finten (Duc 03.11.2026): eine Finte senkt die Paradechance (perfekt, perfekt-oder-gut). Unbekannt = Art noch nie
# pariert (nicht im Bestiarium), bekannt = Rhythmus gelernt. Geschaetzt, nicht gemessen.
FINTE_FAKTOR = {False: (0.5, 0.75), True: (0.85, 0.95)}
SEKUNDEN = {"entscheidung": 6, "kampf_auftakt": 30, "kampf_zug": 8, "parade": 4, "szene": 240, "laden": 30, "wurf": 20, "schlag": 3,
            "wette": 60, "handy": 20}
WOERTER_LESEN, WOERTER_HOEREN = 200, 150
# one strong word or umlaut is enough; weak words also exist in English ("the hat", "die"), so two of them are needed
DE_STARK = re.compile(r"[äöüßÄÖÜ]|\b(und|nicht|eine|ich|für|noch|auch|wird|dich|dir|keine|kein|heute|nach|oder|aber|schon|direkt|"
                      r"offen|Ursache|Abfahrt|Protokoll|Stufe|Nachricht|fertig|erledigt|gefunden)\b")
DE_SCHWACH = re.compile(r"\b(der|die|das|ist|mit|auf|du|wir|hat|zu|im|den|dem|des|morgen|Tag|Uhr|von)\b")
NAMEN_OK = re.compile(r"Totò|Cala d'Orsu|Jessas|Na geh|Grüß|Fröhlich|Bà Tư|Chloé|Mattè|Santu|Citadelle|Spitzhacke|Corsica|Café|Crème|"
                      r"Crêpe|Brûlée|Pâté|Tag Eden")
NICHT_SICHTBAR = ("plan_fehler", "chronik", "/ausschnitte", "/profil", "persona_optionen")
STUFEN = (0, 12, 36, 60, 80, 100)


class Abbruch(Exception):
    """The run cannot go on: a crash or a dead end, already written to the measurements."""


def _worte(t):
    return len((t or "").split())


def _wav(datei):
    p = os.path.join(E.moddir("eden_rise"), "audio", datei)
    try:
        with open(p, "rb") as fh:
            kopf = fh.read(44)
        rate = struct.unpack("<I", kopf[24:28])[0]
        kanaele = struct.unpack("<H", kopf[22:24])[0]
        bits = struct.unpack("<H", kopf[34:36])[0]
        return (os.path.getsize(p) - 44) / float(rate * kanaele * bits / 8)
    except (OSError, struct.error, ZeroDivisionError):
        return None


class Lauf:
    def __init__(self, typ, seed):
        self.profil_id = typ if typ in PROFILE else None
        self.profil = PROFILE.get(typ)
        self.typ = self.profil["basis"] if self.profil else typ
        self.seed = seed
        self.t = dict(TYPEN[self.typ])
        if self.profil:
            self.t.update({k: self.profil[k] for k in ("parade", "hand", "stil", "modus")})
        self.rng = random.Random("%s:%d" % (typ, seed))
        self.modul = None
        self.mod = None
        self.m = {"typ": typ, "seed": seed, "aktionen": collections.Counter(), "angebot_abgelehnt": collections.Counter(),
                  "probe_abgelehnt": collections.Counter(), "abstuerze": [], "sackgassen": [], "lange_phasen": [], "erste": {},
                  "events": {}, "event_wahl": collections.Counter(), "kaempfe": [], "szenen": collections.Counter(),
                  "items": {}, "tage": [], "belohnungen": [], "orte": collections.Counter(), "befehle": collections.Counter(),
                  "deutsch": collections.Counter(), "ohne_bild": collections.Counter(), "bild_fehlt": collections.Counter(),
                  "sekunden": collections.Counter(), "laeden": collections.Counter(), "hilfe": [], "ausgaben": collections.Counter(),
                  "einnahmen": collections.Counter()}
        if self.profil:
            self.m.update(profil_version=VERSION, basis_typ=self.typ, kampfgruppe=(
                "schwach" if self.profil_id == "noor" else "stark" if self.t["stil"] == "klug" else "normal"))
        self.m["peer"] = {"version": VERSION, "signale": collections.Counter(), "belege": [], "wahl_folgen": {},
                          "entscheidungen": [], "antworten_erfolgreich": collections.Counter()}
        self.m["testmodus"] = {"dialog": "platzhalter", "wissen": "hybrid",
            "eventwahl": "sichtbare Texte und Sperren" if self.profil else "interne Folgen",
            "hinweis": "Andere Routinen nutzen Engine-Zustände; kein vollständiger Test ohne Vorwissen."}
        self.schritte = self.ablehnungen = 0
        self.tag = None
        self.heute = None
        self.phase_schritte = collections.Counter()
        self.erledigt = set()
        self.gesehen = set()
        self.kampf = None
        self.zwang = False
        self.besuche = collections.Counter()
        self.gewaehlt = collections.Counter()
        self.niederlagen = collections.Counter()
        self.stand_vorher = None
        self.buchungen = 0
        self.audio = {}

    # ------------------------------------------------------------ engine calls, every one measured
    def tu(self, name, daten=None, angebot=True):
        """One action. angebot=False: the bot tries it without checking first, a refusal is no finding."""
        daten = daten or {}
        self.schritte += 1
        if name == "geste" and daten.get("id") == "einladen":
            self.m["peer"]["signale"]["einladungen_versucht"] += 1
        z0 = E.aktiv()
        vorher = {k: v for k, v in (z0 or {}).get("werte", {}).items() if k.startswith(("vertrauen.", "begehren."))}
        try:
            E.aktion(name, daten)
        except ValueError as ex:
            self.m["angebot_abgelehnt" if angebot else "probe_abgelehnt"]["%s: %s" % (name, re.sub(r"\d+", "N", str(ex))[:70])] += 1
            self.ablehnungen += 1
            if self.ablehnungen > ABLEHNUNGEN_MAX:
                self._sackgasse(z0, "keine Aktion wird mehr angenommen (zuletzt %s)" % name)
            return False
        except Abbruch:
            raise
        except Exception as ex:
            self._absturz(z0, name, ex)
        self.ablehnungen = 0
        self.m["aktionen"][name] += 1
        self._peer_beobachten(z0, E.aktiv(), name, vorher, daten)
        tag = (z0 or {}).get("tag", 0)
        self.m["erste"].setdefault(name, tag)
        self.beobachten(name, daten)
        return True

    def _peer_beobachten(self, vorher, nachher, aktion, werte, daten):
        """Only successful engine actions, bounded id-only evidence, no generated dialogue."""
        vorher, nachher = vorher or {}, nachher or {}
        peer = self.m["peer"]
        if aktion == "event_wahl":
            peer["signale"]["antworten_angenommen"] += 1
            eid = (vorher.get("event") or {}).get("id")
            peer["antworten_erfolgreich"]["%s:%s" % (eid, daten["index"])] += 1
        peer["signale"].update(date_signale(vorher, nachher, aktion, daten))
        for k, v in nachher.get("werte", {}).items():
            if k in werte and isinstance(v, (int, float)) and v != werte[k]:
                peer["signale"]["vertrauen_aenderungen" if k.startswith("vertrauen.") else "begehren_aenderungen"] += 1
        if aktion in ("wahl", "event_wahl", "waehlen", "geste", "intim", "kampf_schliessen", "geben", "skill_lernen", "chip_einsetzen"):
            ev = vorher.get("event") or {}
            sz = (vorher.get("szene") or {}).get("def") or {}
            if len(peer["belege"]) < 250:
                peer["belege"].append({"tag": vorher.get("tag"), "phase": vorher.get("phase"), "aktion": aktion,
                                       "event": ev.get("id"), "szene": sz.get("id"),
                                       "index": daten.get("index"), "geste": daten.get("id") if aktion == "geste" else None})

    def _ort_fehler(self, ex):
        rahmen = [f for f in traceback.extract_tb(ex.__traceback__) if "tests" not in f.filename]
        f = rahmen[-1] if rahmen else traceback.extract_tb(ex.__traceback__)[-1]
        return "%s:%d" % (os.path.basename(f.filename), f.lineno)

    def _absturz(self, z, name, ex, art="Aktion"):
        self.m["abstuerze"].append({"tag": (z or {}).get("tag"), "phase": (z or {}).get("phase"), "status": (z or {}).get("status"),
                                    "aktion": name, "art": art, "fehler": type(ex).__name__, "text": str(ex)[:120],
                                    "wo": self._ort_fehler(ex)})
        raise Abbruch()

    def _sackgasse(self, z, text):
        self.m["sackgassen"].append({"tag": (z or {}).get("tag"), "phase": (z or {}).get("phase"), "status": (z or {}).get("status"),
                                     "event": ((z or {}).get("event") or {}).get("id"), "text": text})
        raise Abbruch()

    # ------------------------------------------------------------ what happened after an action
    def beobachten(self, name, daten):
        z = E.aktiv()
        try:
            v = E.ansicht(z)                   # the display (GET /api/stand) has to work in every state
        except Exception as ex:
            self._absturz(z, name, ex, "Anzeige")
        self._letzte_ansicht = v
        ev = z.get("event")
        if ev and ev.get("id") and (not self.stand_vorher or self.stand_vorher != ev["id"]):
            self._event_oeffnet(z, ev["id"])
        self.stand_vorher = (ev or {}).get("id")
        sz = z.get("szene") if z.get("status") == "szene" else None
        if sz:
            sid = (sz.get("def") or {}).get("id") or "?"
            if (z["tag"], z["phase"], sid) not in self.erledigt:
                self.erledigt.add((z["tag"], z["phase"], sid))
                self.m["szenen"][sid] += 1
                self.m["sekunden"]["szenen"] += SEKUNDEN["szene"]
                self.heute["szenen"] += 1 if self.heute else 0
        self._kampf_beobachten(z, name)
        self._belohnungen(z)
        for i in z.get("inventar") or []:
            self.m["items"].setdefault(i, z["tag"])
        if self.tag != z["tag"]:
            self._tag_wechsel(z, v)
        if self.heute is not None and z.get("buchungen"):
            for b in z["buchungen"][self.buchungen:]:
                art = re.sub(r"[\d€.,]+", "", b["text"].split(":")[0]).strip()[:24]
                self.m["einnahmen" if b["betrag"] > 0 else "ausgaben"][art] += abs(b["betrag"])
            self.buchungen = len(z["buchungen"])
        schl = (z.get("status"), (ev or {}).get("id"), (sz or {}).get("def", {}).get("id") if sz else None)
        if schl not in self.gesehen:
            self.gesehen.add(schl)
            self._anzeige_pruefen(v)
        if z["status"] != "ende":
            pk = "%d-%s" % (z["tag"], z["phase"])
            self.phase_schritte[pk] += 1
            grenze = PHASE_MAX * (5 if z.get("taktik") else 1)   # eine Welle mit allen Runden, Kaempfen und Neustarts braucht viel mehr Schritte (Spieltest 02.11.2026)
            if self.phase_schritte[pk] == grenze:
                self.m["lange_phasen"].append({"tag": z["tag"], "phase": z["phase"], "status": z["status"],
                                               "event": (ev or {}).get("id")})
                self.zwang = True
            elif self.phase_schritte[pk] > 2 * grenze:
                self._sackgasse(z, "Phase endet nicht (%d Schritte)" % self.phase_schritte[pk])
            elif self.phase_schritte[pk] < grenze:
                self.zwang = False

    def _event_oeffnet(self, z, eid):
        self.m["events"].setdefault(eid, z["tag"])
        if self.heute:
            self.heute["events"] += 1
        roh = self.index.get(eid) or {}
        peer = self.m["peer"]
        if eid not in peer["wahl_folgen"]:
            opts = roh.get("optionen") or []
            signaturen = {json.dumps({k: o.get(k) for k in ("folgen", "probe", "bei_erfolg", "bei_fehlschlag", "energie")},
                                    sort_keys=True, default=str) for o in opts}
            peer["wahl_folgen"][eid] = {"optionen": len(opts), "folgenvarianten": len(signaturen),
                "romance": any("vertrauen" in f or "begehren" in f or "szene_intim" in f or "szene_gespraech" in f
                               for o in opts for f in self._folgen(o)),
                "kampf": any("kampf" in f for o in opts for f in self._folgen(o))}
            if any("szene_intim" in f for o in opts for f in self._folgen(o)):
                peer["signale"]["intim_angebote_events"] += 1
        s = _worte(roh.get("lage")) / WOERTER_LESEN * 60
        for n, zl in enumerate(roh.get("zeilen") or []):
            a = self.audio.get("%s#z%d" % (eid, n))
            d = _wav(a["datei"]) if a else None
            s += d if d else _worte(zl.get("text")) / WOERTER_HOEREN * 60
        s += SEKUNDEN["entscheidung"] + sum(_worte(o.get("text")) for o in roh.get("optionen") or []) / WOERTER_LESEN * 60
        self.m["sekunden"]["events"] += s
        if self.heute:
            self.heute["sekunden"] += s
        if self.heute and roh.get("personen", {}).get("favour"):
            self.m["erste"].setdefault("favour", z["tag"])

    def _kampf_beobachten(self, z, name):
        k = z.get("kampf")
        if z.get("status") == "kampf" and k and not self.kampf:
            sp = k["spieler"]
            self.kampf = {"id": k.get("definition") or "?", "tag": z["tag"], "level": E.kampf.progress(z)["level"],
                          "lp_start": sp.get("lp"), "lp_max": sp.get("lp_max"), "zuege": 0, "paraden": 0, "befehle": collections.Counter(),
                          "waffe": (sp.get("weapon") or {}).get("id") or E.kampf.equipment(z).get("weapon"),
                          "ruestung": E.kampf.equipment(z).get("armor"), "gegner": len(k.get("gegner") or [])}
        if self.kampf and k and k.get("ergebnis") and "art" not in self.kampf:
            sp = k["spieler"]
            self.kampf.update(art=k["ergebnis"].get("art"), lp_ende=sp.get("lp"))
        if self.kampf and name == "kampf_schliessen":
            d = self.kampf
            d["befehle"] = dict(d["befehle"])
            self.m["kaempfe"].append(d)
            s = SEKUNDEN["kampf_auftakt"] + d["zuege"] * SEKUNDEN["kampf_zug"] + d["paraden"] * SEKUNDEN["parade"]
            self.m["sekunden"]["kaempfe"] += s
            if self.heute:
                self.heute["kaempfe"] += 1
                self.heute["sekunden"] += s
            self.kampf = None

    def _belohnungen(self, z):
        """Anything a player would feel as a reward, once. Phase resolution, so the gap between rewards can be measured."""
        schl = "%d-%s" % (z["tag"], z["phase"])
        neu = []
        c = E.kampf.progress(z)
        stand = {"level": c["level"], "waffen": len(E.kampf.besitz(z, E.kampf.daten(self.mod))["weapons"]),
                 "fische": len(((z.get("kueche") or {}).get("fischbuch") or {})),
                 "auftraege": len(z.get("auftraege_fertig") or []), "charms": len((z.get("charms") or {}).get("besitz") or []),
                 "chips": len(E.kampf.chip_pool(z)["pool"]), "selfies": len(z.get("selfie_bilder") or {}),
                 "stufen": sum(sum(1 for s in STUFEN[1:] if v >= s) for k, v in (z.get("punkte") or {}).items()
                               if k.startswith(("vertrauen.", "begehren.")))}
        alt = getattr(self, "_bel", None)
        if alt:
            neu = [k for k in stand if stand[k] > alt[k]]
        self._bel = stand
        konto = z.get("konto", 0)
        if getattr(self, "_konto", None) is not None and konto - self._konto >= 150:
            neu.append("geld")
        self._konto = konto
        items = set(z.get("inventar") or [])
        alt_i = getattr(self, "_inv", None)
        if alt_i is not None and items - alt_i:
            neu.append("item")
        self._inv = items
        for art in neu:
            self.m["belohnungen"].append([z["tag"], z["phase"], art])
            if self.heute:
                self.heute["belohnungen"] += 1

    def _tag_wechsel(self, z, v):
        if self.heute:
            self.m["tage"].append(self.heute)
        self.tag = z["tag"]
        zz = (v or {}).get("z") or {}
        offen = sum(1 for j in zz.get("journal") or [] if j.get("status") == "aktiv")
        verspr = len(zz.get("versprechen") or [])
        fa = sum(1 for k in zz.get("favours") or [] if not k.get("foto"))
        c = E.kampf.progress(z)
        self.heute = {"tag": z["tag"], "konto": z.get("konto", 0), "level": c["level"], "flags": len(z.get("flags") or []),
                      "events": 0, "kaempfe": 0, "szenen": 0, "belohnungen": 0, "sekunden": 0.0, "offene_ziele": offen + verspr + fa,
                      "auftraege_offen": offen, "versprechen": verspr, "favours_offen": fa, "energie": z["werte"].get("energie"),
                      "moral": z["werte"].get("moral"), "rueckhalt": z["werte"].get("rueckhalt"),
                      "bindung": sum(x for k, x in z["werte"].items() if k.startswith(("vertrauen.", "begehren.")))}
        z2 = E.aktiv()                         # save and reload must not change anything
        E.sichern(z2)
        if json.dumps(z2, sort_keys=True, default=str) != json.dumps(E.aktiv(), sort_keys=True, default=str):
            self.m.setdefault("speicher_abweichung", []).append(z["tag"])

    def _anzeige_pruefen(self, v):
        for pfad, s in _texte(v):
            if any(n in pfad for n in NICHT_SICHTBAR):
                continue
            if len(s) > 5 and " " in s and not s.startswith(("/", "http")) and _deutsch(s):
                self.m["deutsch"][(pfad.split("/")[-1] or pfad)[:24] + " | " + _maske(s)[:70]] += 1
            if s.startswith("/bg/") and not E.buehne.hintergrund_datei(E.cfg(), s[4:].split("?")[0]):
                self.m["bild_fehlt"][s[4:]] += 1
        for pfad in _ohne_bild(v):
            self.m["ohne_bild"][pfad] += 1

    # ------------------------------------------------------------ the run
    def spielen(self):
        ordner = tempfile.mkdtemp(prefix="eden_spieltest_")
        try:
            L.vorbereiten("eden_rise", ordner, self.seed)
            random.seed(self.seed)
            self.modul = E.modul_laden()
            self.mod = E.moddir("eden_rise")
            self.index = E.ereignisse.daten(self.mod)["_index"]
            self.kdefs = E.kampf.daten(self.mod)
            pf = os.path.join(self.mod, "audio_index.json")
            self.audio = json.load(open(pf, encoding="utf-8")) if os.path.exists(pf) else {}
            self.tu("neu", {"modus": self.t["modus"]})
            while True:
                z = E.aktiv()
                if z["status"] == "ende":
                    break
                if self.schritte > MAX_SCHRITTE:
                    self._sackgasse(z, "Durchlauf endet nicht (%d Schritte)" % self.schritte)
                self.schritt(z)
            self._abschluss(E.aktiv())
        except Abbruch:
            self._abschluss(E.aktiv(), abgebrochen=True)
        finally:
            shutil.rmtree(ordner, ignore_errors=True)
        return self.m

    def _abschluss(self, z, abgebrochen=False):
        if self.heute:
            self.m["tage"].append(self.heute)
        v = E.ansicht(z)["z"] if not abgebrochen else {}
        zustand = json.dumps(z, sort_keys=True, default=str)
        self.m.update(schritte=self.schritte, abgebrochen=abgebrochen, ende={"tag": z["tag"], "phase": z["phase"], "status": z["status"]},
                      fingerabdruck=hashlib.sha1(zustand.encode("utf-8")).hexdigest()[:16], konto=z.get("konto", 0),
                      level=E.kampf.progress(z)["level"], flags=z.get("flags") or [], abschluss=bool(z.get("abschluss")),
                      auftraege_fertig=z.get("auftraege_fertig") or [],
                      auftraege=[{"id": j["id"], "status": j["status"]} for j in v.get("journal") or []],
                      favours=[x["id"] for x in z.get("favours") or []], fischbuch=list(((z.get("kueche") or {}).get("fischbuch") or {})),
                      bekannt=z.get("bekannt") or [], fall=(z.get("ermittlung") or {}).get("fall"),
                      ausgang=_ausgang(z.get("abschluss")), buchungen=len(z.get("buchungen") or []),
                      werte={k: x for k, x in z["werte"].items() if k.startswith(("vertrauen.", "begehren."))})

    def schritt(self, z):
        st = z["status"]
        if z.get("tisch"):                     # the table scene plays on top of everything, the client closes it
            self.tu("tisch_fertig")
        elif st == "persona_wahl":
            self.tu("persona", {"index": 0})
        elif st == "prolog":
            self.tu("prolog")
        elif st in ("warte_auf_plan", "plan_fehler"):
            self.tu("plan_laden")
        elif st == "kabine":
            self.kabine(z)
        elif st == "kampf":
            self.kampfzug(z)
        elif st == "verhandlung":
            self.verhandlung(z)
        elif st == "taktik":                     # Belagerung: der Bot spielt die Karte wie ein Mensch (Duc 02.11.2026)
            self.taktik(z)
        elif st == "sturm":
            self.sturm(z)
        elif st == "ereignis":
            self.ereignis(z)
        elif st == "szene":
            self.szene(z)
        elif st == "wahl":
            self.wahl(z)
        elif st == "angeln":
            self.angeln(z)
        elif st == "abbau":
            self.abbau(z)
        elif st == "schiessen":
            self.schiessen(z)
        else:
            self._sackgasse(z, "unbekannter Status " + st)

    # ------------------------------------------------------------ siege map (Duc 02.11.2026: end to end through act 2)
    def taktik(self, z):
        """One step on the tactics map, through the same actions as the client: scenes, placing, moves, attacks (Duc and
        Maxwell fight for real in the combat screen), rescues, the morning repairs. After three lost tries of a wave the bot
        takes the test shortcut, and that is recorded as help, never as a clean win."""
        t, D = z["taktik"], E.taktik.daten(self.mod)
        tk = self.m.setdefault("taktik", {"wellen": {}, "neustarts": 0, "hilfe": [], "kaempfe": 0, "flicken": 0, "rettungen": 0, "wahlen": []})
        ph = t["phase"]
        if t.get("briefing"):
            return self.tu("taktik", {"was": "szene"})
        if ph == "szene":
            sz = (t.get("szene") or [{}])[0]
            if sz.get("art") == "wahl":
                i = self.rng.randrange(len(sz["optionen"]))
                tk["wahlen"].append(sz["optionen"][i].get("flag"))
                return self.tu("taktik", {"was": "szene_wahl", "i": i})
            return self.tu("taktik", {"was": "szene"})
        if ph == "aufstellen":
            return self.tu("taktik", {"was": "start"})
        if ph == "bestand":
            v = E.belagerung.ansicht(z, D, self.modul, t.get("flicken"))
            for x in v["offen"]:
                if x["geht"]:
                    tk["flicken"] += 1
                    return self.tu("taktik", {"was": "flicken", "id": x["id"]}, angebot=False)
                if x["crew_geht"]:
                    tk["flicken"] += 1
                    return self.tu("taktik", {"was": "flicken_crew", "id": x["id"]}, angebot=False)
            return self.tu("taktik", {"was": "schliessen"})
        if ph == "white_neu":
            return self.tu("taktik", {"was": "white"})
        if ph == "gewonnen":
            tk["wellen"][str(t["welle"])] = tk["wellen"].get(str(t["welle"]), 0) + 1
            return self.tu("taktik", {"was": "schliessen"})
        if ph == "verloren":
            schl = "%d-%d" % (z["tag"], t["welle"])
            n = tk.setdefault("verloren", {}).get(schl, 0) + 1
            tk["verloren"][schl] = n
            grund = "kirche" if t["kirche"] <= 0 else "duc"           # warum: die Kirche faellt oder Duc
            tk.setdefault("grund", {})["%s %s" % (schl, grund)] = tk.setdefault("grund", {}).get("%s %s" % (schl, grund), 0) + 1
            if n <= 3:
                tk["neustarts"] += 1
                return self.tu("taktik", {"was": "neustart"})
            tk["hilfe"].append({"tag": z["tag"], "welle": t["welle"], "runde": t["runde"], "kirche": t["kirche"]})
            E.taktik.BOT_ERLAUBT = True
            return self.tu("taktik", {"was": "bot_sieg"})
        if ph != "spieler":
            self._sackgasse(z, "Taktik-Phase " + ph)
        versuch = self.__dict__.setdefault("_tk_versuch", {})
        for e in E.taktik.lebend(t, "blau"):
            if e["fest"] or e["fertig"] or e.get("ko"):
                continue
            k = (z["tag"], t["welle"], t["runde"], e["id"])
            versuch[k] = versuch.get(k, 0) + 1
            if versuch[k] > 3:                   # the game refused this unit three times: it waits, so the bot can never loop
                if versuch[k] == 4:
                    self.tu("taktik", {"was": "warten", "id": e["id"]}, angebot=False)
                continue
            return self._taktik_trupp(z, D, t, e, tk)
        return self.tu("taktik", {"was": "runde"})

    def _taktik_trupp(self, z, D, t, e, tk):
        """A plain but sensible player: get people out of houses about to go, hide when nearly dead, otherwise hit the best
        target in reach, preferring whoever is at the church door; nothing in reach, walk towards the nearest enemy."""
        felder = E.taktik.erreichbar(D, t, e)
        tuer = D["kirche"]["tueren"][0]
        if e["id"] not in E.taktik.SPIELER:
            for h in D["haeuser"]:
                s_ = (t.get("haeuser") or {}).get(h["id"]) or {}
                if s_.get("status") == "brennt" and s_.get("lunte", 9) <= 3:
                    nah = [f for f in felder if abs(f[0] - h["x"]) + abs(f[1] - h["y"]) <= 1]
                    if nah:
                        if tuple(nah[0]) != (e["x"], e["y"]):
                            self.tu("taktik", {"was": "bewegen", "id": e["id"], "x": nah[0][0], "y": nah[0][1]}, angebot=False)
                        tk["rettungen"] += 1
                        return self.tu("taktik", {"was": "retten", "id": e["id"], "haus": h["id"]}, angebot=False)
        weiss = [g for g in E.taktik.lebend(t, "weiss") if e["id"] == "duc" and E.taktik.white_frei(t)]
        feinde = E.taktik.lebend(t, "schwarz") + weiss
        if e["id"] != "duc":
            feinde = [g for g in feinde if not g.get("boss")]
        if not feinde:
            return self.tu("taktik", {"was": "warten", "id": e["id"]})
        schwach = (E.kampf.lp(z) / max(1, E.kampf.lp_max_duc(z)) < .3) if e["id"] == "duc" else e["lp"] / max(1, e["lp_max"]) < .25
        if schwach and not weiss:
            f = min(felder, key=lambda f: (abs(f[0] - tuer[0]) + abs(f[1] - tuer[1]), f))
            if tuple(f) != (e["x"], e["y"]):
                self.tu("taktik", {"was": "bewegen", "id": e["id"], "x": f[0], "y": f[1]}, angebot=False)
            return self.tu("taktik", {"was": "warten", "id": e["id"]}, angebot=False)

        def wert(g):
            w = 500 if g.get("boss") else 0
            w += 30 if abs(g["x"] - tuer[0]) + abs(g["y"] - tuer[1]) <= 6 else 0
            w += 25 if E.taktik.staerke(e, g) > 1 else 0
            return w - (abs(g["x"] - e["x"]) + abs(g["y"] - e["y"]))
        beste = None
        for g in sorted(feinde, key=wert, reverse=True):
            for f in felder:
                d = abs(f[0] - g["x"]) + abs(f[1] - g["y"])
                if d == 0 or d > e["reichweite"]:
                    continue
                x, y = e["x"], e["y"]
                e["x"], e["y"] = f
                kann = g in E.taktik.ziele(t, e, D)
                e["x"], e["y"] = x, y
                if kann:
                    beste = (g, f)
                    break
            if beste:
                break
        if beste:
            g, f = beste
            if tuple(f) != (e["x"], e["y"]):
                self.tu("taktik", {"was": "bewegen", "id": e["id"], "x": f[0], "y": f[1]}, angebot=False)
                if E.aktiv()["status"] != "taktik" or E.aktiv()["taktik"]["phase"] != "spieler":
                    return
            if e["id"] in E.taktik.SPIELER:
                tk["kaempfe"] += 1
            return self.tu("taktik", {"was": "angreifen", "id": e["id"], "ziel": g["id"]}, angebot=False)
        # nothing in reach: go for the enemy closest to the church, like a player who defends it (spieltest 02.11.2026: the bot
        # used to chase agents up north while the church fell)
        ziel = min(feinde, key=lambda g: (0 if g.get("boss") and weiss else 1, abs(g["x"] - tuer[0]) + abs(g["y"] - tuer[1]), g["id"]))
        wege = E.taktik._dijkstra(D, t, e, (ziel["x"], ziel["y"]))
        f = min(felder, key=lambda f: (wege.get(tuple(f), 999), tuple(f)))
        if tuple(f) != (e["x"], e["y"]):
            self.tu("taktik", {"was": "bewegen", "id": e["id"], "x": f[0], "y": f[1]}, angebot=False)
        if E.aktiv()["status"] == "taktik" and E.aktiv()["taktik"]["phase"] == "spieler" and not e.get("fertig"):
            self.tu("taktik", {"was": "warten", "id": e["id"]}, angebot=False)

    # ------------------------------------------------------------ events and places
    def _folgen(self, o):
        return list(o.get("folgen") or []) + list(o.get("bei_erfolg") or [])

    def _wertung(self, z, eid, i, o):
        if self.profil:
            return antwort_werten(self.profil, o, getattr(self, "_sichtbarer_kontext", ""),
                                  self.gewaehlt["%s:%d" % (eid, i)])[0]
        typ, wert = self.typ, 0.0
        for f in self._folgen(o):
            if typ == "romantiker":
                wert += (f.get("vertrauen") or [0, 0])[1] + 1.5 * (f.get("begehren") or [0, 0])[1]
                wert += 20 if "szene_intim" in f else 8 if "szene_gespraech" in f else 0
                wert -= 3 if "kampf" in f else 0
            elif typ == "kaempfer":
                wert += 6 if "kampf" in f else 0
                wert += 2 if "item" in f or "chip" in f else 0
                wert -= 3 if "ort_ende" in f else 0
            elif typ == "sammler":
                wert += 2 if "item" in f or "chip" in f or "charm" in f else 0
                wert += 1 if "kampf" in f else 0
                wert -= 1 if "ort_ende" in f else 0
            elif typ == "sparer":
                wert += float(f.get("geld") or 0) / 50
                wert += 2 if "item" in f else 0
                wert -= 2 if "kampf" in f else 0
            elif typ == "schwach":
                wert -= 2 if "kampf" in f else 0
            ziel = f.get("weiter")
            if isinstance(ziel, str):
                wert -= 5 * self.besuche[ziel]
                if typ in ("sammler", "kaempfer") and not self.besuche[ziel]:
                    wert += 3
            if self.zwang:
                wert += 50 if "ort_ende" in f else -5 if "weiter" in f else 0
        if typ == "sammler":
            wert += 3 if not self.gewaehlt["%s:%d" % (eid, i)] else 0
        if typ == "sparer":
            wert -= o.get("energie", 0)
        if typ == "schwach":
            wert -= 4 if o.get("probe") else 0
            wert -= o.get("energie", 0)
        if typ == "romantiker" and o.get("art") == "auflegen":
            wert -= 4
        if typ == "sammler" or typ == "kaempfer":
            wert += self.rng.random()          # different seeds take different branches
        return wert

    def ereignis(self, z):
        ev = z["event"]
        if ev.get("ergebnis"):
            self.tu("event_schliessen")
            return
        roh = self.index[ev["id"]]
        if z.get("rast_anruf"):                # somebody calls at the rest site: harvesting waits for the answer
            antworten = z["rast_anruf"].get("antworten") or [0]
            self.tu("rast_antwort", {"index": self.rng.randrange(len(antworten))})
            return
        if ev["id"] != getattr(self, "_letztes_ev", None):
            self.besuche[ev["id"]] += 1
            self._letztes_ev = ev["id"]
        if roh.get("art") == "ort" and roh.get("rast") and self.rastplatz(z):
            return
        if roh.get("art") == "ort" and self.typ != "chaos":   # am Eingang zum weitesten Wegpunkt, wie ein Mensch bei "skips N fights"
            r = E.wegpunkte.ziele(z, self.index) or {}           # (Interaction 02.11.2026: sonst jede Rueckkehr zu Fuss ab dem Start)
            if r.get("von") == "eingang" and r.get("ziele") and \
                    self.tu("ort_reisen", {"id": max(r["ziele"], key=lambda w: w["schritte"])["id"]}, angebot=True):
                return
        if roh.get("art") == "ort" and self.typ in ("chaos", "sammler") and self.rng.random() < .08:
            ziele = (E.wegpunkte.ziele(z, self.index) or {}).get("ziele") or []
            if ziele and self.tu("ort_reisen", {"id": self.rng.choice(ziele)["id"]}, angebot=True):
                return
            if self.tu("ort_zurueck", {}, angebot=False):
                return
        opts = roh["optionen"]
        if not opts:
            self._sackgasse(z, "Event ohne Antwort: " + ev["id"])
        energie = z["werte"].get("energie", 0)
        frei = [i for i, o in enumerate(opts) if o.get("energie", 0) <= energie]
        if not frei and not self.profil:
            self.m["hilfe"].append({"tag": z["tag"], "art": "keine Antwort bezahlbar", "event": ev["id"]})
            frei = [0]
        if self.profil:
            sichtbar = (E.ansicht(z).get("z") or {}).get("ereignis") or {}
            vopts = sichtbar.get("optionen") or []
            frei = [n for n, v in enumerate(vopts) if not v.get("gesperrt")]
            if not frei:
                self._sackgasse(z, "Keine sichtbare freie Antwort; keine versteckte Ersatzwahl")
            self._sichtbarer_kontext = " ".join([sichtbar.get("lage") or ""] +
                [zl.get("text") or "" for zl in sichtbar.get("zeilen", [])])
            i, gruende = self.event_entscheidung(z, ev["id"], vopts, frei)
            if len(self.m["peer"]["entscheidungen"]) < 2000:
                self.m["peer"]["entscheidungen"].append({"tag": z["tag"], "phase": z["phase"],
                    "event": ev["id"], "index": i, "grund": gruende, "wissen": "sichtbare_optionen"})
        else:
            i = self.rng.choice(frei) if self.typ == "chaos" and not self.zwang else \
                max(frei, key=lambda n: (self._wertung(z, ev["id"], n, opts[n]), -n))
        o = opts[i]
        daten = {"index": i}
        if o.get("art") == "ort_waehlen":
            orte = E.ereignisse.ort_auswahl(z, self.modul, E.ereignisse._intim_pid(o))
            if orte:
                daten["ort"] = orte[0]["id"]
        # Chase them off (Duc 02.11.2026): wer nicht kaempfen will, nimmt den Knopf, wo die Karte ihn anbietet (Main Chat 03.11.)
        if roh.get("art") == "ort" and self.typ in ("romantiker", "sparer", "schwach") \
                and z.get("ort_frame") not in z.get("ort_besiegt", []) \
                and E.expedition.wahl_info(z, E.kampf.daten(self.mod), o, lambda *a: None).get("verjagbar"):
            daten["verjagen"] = True
        self.gewaehlt["%s:%d" % (ev["id"], i)] += 1
        self.m["event_wahl"]["%s:%d" % (ev["id"], i)] += 1
        self.tu("event_wahl", daten)

    def event_entscheidung(self, z, eid, optionen, frei):
        scored = {n: antwort_werten(self.profil, optionen[n], self._sichtbarer_kontext,
                                   self.gewaehlt["%s:%d" % (eid, n)]) for n in frei}
        i = max(frei, key=lambda n: (scored[n][0], self.rng.random()))
        return i, scored[i][1]

    def rastplatz(self, z):
        """At a rest site: rest when hurt, then one harvest per kind (needs the right tool, or it stays locked)."""
        frame = z.get("ort_frame")
        if not frame:
            return False
        c = E.kampf.progress(z)
        schl = (z["tag"], z["phase"], frame)
        if E.kampf.lp(z) < .6 * E.kampf.max_lp(c["level"]) and frame not in (z.get("ort_rasten") or []) \
                and schl + ("rast",) not in self.erledigt:
            self.erledigt.add(schl + ("rast",))
            if self.tu("ort_rasten"):
                return True
        if self.typ not in ("sammler", "sparer", "kaempfer", "chaos"):
            return False
        for q in E.abbau.quellen_ansicht(z, self.modul, frame):
            art = q["art"]
            if q.get("voll") or q.get("fehlt") or not q.get("rest") or schl + (art,) in self.erledigt:
                continue
            self.erledigt.add(schl + (art,))
            if art == "wasser":
                ok = self.tu("angeln_start", {"ort": q["platz"]}, angebot=False)
            else:
                ok = self.tu("abbau_start", {"art": art}, angebot=False)
            if ok:
                return True
        return False

    def angeln(self, z):
        s = z["angeln"]
        if s.get("aktiv"):
            self.m["sekunden"]["minispiele"] += SEKUNDEN["wurf"]
            ok = self.rng.random() < self.t["hand"]
            self.tu("angeln_ergebnis", {"gefangen": ok, "fehler": 0 if self.rng.random() < self.t["hand"] else 2,
                                        "grund": "" if ok else self.rng.choice(("biss", "riss"))})
        elif s["wurf"] < min(s.get("wuerfe", 4), 4) and not s.get("schluss"):
            if not self.tu("angeln_wurf", angebot=False):
                self.tu("angeln_ende")
        else:
            self.tu("angeln_ende")

    def abbau(self, z):
        s = z["abbau"]
        if s.get("bau"):                          # Flicken in der Belagerung (kern/belagerung.py): fertig oder zu viele Fehlschlaege
            if s["geschafft"] or s["fehl"] > 12:
                self.tu("abbau_ende")
                return
        elif s["nr"] >= len(s["knoten"]) or s["nr"] >= 3 or s["fehl"] > 12:
            self.tu("abbau_ende")
            return
        self.m["sekunden"]["minispiele"] += SEKUNDEN["schlag"]
        h = self.rng.random()
        self.tu("abbau_schlag", {"ergebnis": "perfekt" if h < self.t["hand"] / 2 else "gut" if h < self.t["hand"] else "daneben"})

    def schiessen(self, z):
        s = z["schiessen"]
        if s.get("letztes") is None or (not s["letztes"]["sieg"] and s["versuche"] < 3):
            a = E.schiessen.ansicht(z)
            self.m["sekunden"]["minispiele"] += SEKUNDEN["wette"]
            plus = 1 if self.rng.random() < self.t["hand"] else -1
            self.tu("schiessen_ergebnis", {"runden": [{"du": max(0, b + plus), "bot": b} for b in a["bot"]]})
        else:
            self.tu("schiessen_ende")

    # ------------------------------------------------------------ free phases
    def wahl(self, z):
        tag = z["tag"]
        if ("arbeit", tag) not in self.erledigt:
            self.erledigt.add(("arbeit", tag))
            self.tagesarbeit(z)
            return
        schl = ("pflege", tag, z["phase"])
        if schl not in self.erledigt:
            self.erledigt.add(schl)
            self.pflege(z)
            return
        z = E.aktiv()
        if z["status"] != "wahl":
            return
        if self.extras(z):
            return
        if E.plan.aktionen(z):                 # one of two actions is gone: no scene or trip fits any more
            if self.typ == "kaempfer" and ("training2", tag, z["phase"]) not in self.erledigt:
                self.erledigt.add(("training2", tag, z["phase"]))
                if E.tutorial.training_verfuegbar(z) and not trainiert(z) and self.tu("training_kampf", angebot=False):
                    return
            self.tu("phase_beenden")
            return
        orte = E.auftraege.orte_frei(z, self.mod)
        optionen = list(z.get("optionen") or [])
        if not orte and not optionen:
            self.tu("phase_beenden")
            return
        art, wert = self.wahl_treffen(z, optionen, orte)
        if art == "ort":
            self.m["orte"][wert] += 1
            self.erledigt.add(("ort", tag, wert))
            self.besuche.clear()
            self.tu("ort_betreten", {"id": wert})
        elif art == "beenden":
            self.tu("phase_beenden")
        else:
            self.tu("wahl", {"id": wert})

    def wahl_treffen(self, z, optionen, orte):
        tag, typ = z["tag"], self.typ
        neu_ort = [o["id"] for o in orte if ("ort", tag, o["id"]) not in self.erledigt]
        if self.profil:
            # Each profile really chooses a route, rather than rewording a shared run.
            if neu_ort and (not optionen or self.rng.random() < self.profil["ort"]):
                frisch = [o for o in neu_ort if not self.m["orte"][o]]
                return "ort", self.rng.choice(frisch or neu_ort)
            if optionen:
                dates = [s for s in optionen if s.startswith("date_")]
                if dates and self.profil["vertrauen"] + self.profil["begehren"] >= 2:
                    return "szene", self.rng.choice(dates)
                frisch = [s for s in optionen if not self.m["szenen"][s]]
                return "szene", self.rng.choice(frisch or optionen)
        if typ == "chaos":
            alles = [("szene", s) for s in optionen] + [("ort", o) for o in neu_ort] + [("beenden", None)]
            return self.rng.choice(alles)
        if typ in ("kaempfer", "sammler") and neu_ort:
            frisch = [o for o in neu_ort if not self.m["orte"][o]]
            return "ort", (frisch or neu_ort)[0]
        if typ == "sparer" and neu_ort and tag % 2:
            return "ort", neu_ort[0]
        if not optionen:
            return ("ort", neu_ort[0]) if neu_ort else ("beenden", None)
        if typ == "romantiker":
            ziel = self.partner(z)
            for s in optionen:
                if s.startswith("date_"):
                    return "szene", s
            for s in optionen:
                try:
                    wer = E.plan.anwesende(z, E.plan.szene_nach_id(z, s), self.modul)
                except (KeyError, ValueError, TypeError):
                    wer = []
                if ziel in wer:
                    return "szene", s
        if typ == "sammler":
            frisch = [s for s in optionen if not self.m["szenen"][s]]
            if frisch:
                return "szene", frisch[0]
        return "szene", optionen[0]

    def partner(self, z):
        frauen = E.hauptstory.frauen(self.modul)
        return max(frauen, key=lambda p: z["werte"].get("vertrauen." + p, 0) + z["werte"].get("begehren." + p, 0)) if frauen else None

    def extras(self, z):
        """What costs no time: the phone, a fishing trip at the boat, Holm's bet, the cabin, training (one action)."""
        tag, typ = z["tag"], self.typ
        erst = lambda k: (k, tag) not in self.erledigt and (self.erledigt.add((k, tag)) or True)      # noqa: E731
        if typ in ("sammler", "romantiker", "chaos") and z.get("handy") and erst("handy"):
            self.handy(z)
            return True
        if typ in ("sammler", "sparer") and tag % 2 == 0 and erst("angeln"):
            for o in E.angeln.orte(z, self.modul):
                if o.get("rest") and self.tu("angeln_start", {"ort": o["id"]}, angebot=False):
                    return True
        if typ in ("sammler", "kaempfer", "chaos") and E.schiessen.offen(z) and erst("wette"):
            if self.tu("schiessen_start", angebot=False):
                return True
        if typ == "sammler" and tag % 3 == 0 and erst("kabine"):
            return self.tu("kabine", angebot=False)
        if typ == "chaos" and self.rng.random() < .05 and erst("kabine"):
            return self.tu("kabine", angebot=False)
        if typ in ("sammler", "chaos") and z["persona"] and erst("ermitteln") and E.ermittlung.aktiv(z):
            wege = [w for w in E.ermittlung.moeglich(z, self.modul) if not w.get("sperre")]
            if wege:
                return self.tu("ermitteln", {"weg": wege[0]["weg"]}, angebot=True)
        if typ in ("kaempfer", "sammler") and E.tutorial.training_verfuegbar(z) and not trainiert(z) and not E.plan.aktionen(z) \
                and (typ == "kaempfer" or tag % 4 == 0) and erst("training"):
            return self.tu("training_kampf", angebot=False)
        return False

    def handy(self, z):
        modul = self.modul
        ungelesen = [i for i, f in enumerate(z["handy"]) if not f.get("gelesen")]
        if ungelesen:
            self.tu("handy_gelesen", {"indizes": ungelesen})
        for i, f in enumerate(E.aktiv().get("handy", [])):
            pid = f["von"]
            if E.handy.rest(E.aktiv(), pid, modul) > 0 and not E.handy.gesperrt(E.aktiv(), modul, pid):
                self.m["sekunden"]["handy"] += SEKUNDEN["handy"]
                if self.typ == "sammler" and ("chips", z["tag"]) not in self.erledigt:
                    self.erledigt.add(("chips", z["tag"]))
                    self.tu("handy_chips", {"index": i}, angebot=False)
                vertraut = E.aktiv()["werte"].get("vertrauen." + pid, 0) >= E.handy.daten(modul)["flirt_min_trust"]
                ton = ("flirty" if vertraut else "warm") if self.typ == "romantiker" else self.rng.choice(["warm", "funny", "neutral", "pushy"])
                self.tu("handy_antwort", {"index": i, "text": "Thinking of the crew today.", "ton": ton}, angebot=False)
                if self.typ != "chaos":
                    break

    def kabine(self, z):
        if self.typ == "sammler" and ("anruf", z["tag"]) not in self.erledigt:
            self.erledigt.add(("anruf", z["tag"]))
            kontakte = E.kabine.kontakte(z, self.modul)
            if kontakte and z["tag"] % 6 == 0:
                self.tu("kabine_anruf", {"an": sorted(kontakte)[0]}, angebot=False)
                return
        self.tu("kabine_zurueck")

    def pflege(self, z):
        """Spend points, change gear, hand pieces to Rosi: what players do between the fights."""
        defs = self.kdefs
        c = E.kampf.progress(z)
        attr = ("strength", "courage", "perception", "charm", "cunning", "empathy")
        if self.typ == "romantiker":
            attr = ("charm", "empathy", "perception", "courage", "cunning", "strength")
        if self.typ == "chaos":
            attr = tuple(self.rng.sample(attr, len(attr)))
        if self.profil:
            attr = tuple(self.profil["attribute"])
        versuche = 0
        while c["attributpunkte"] > 0 and versuche < 8:
            self.tu("attribut_steigern", {"id": attr[versuche % len(attr)]}, angebot=False)
            versuche += 1
            c = E.kampf.progress(E.aktiv())
        z = E.aktiv()
        if self.typ in ("sammler", "kaempfer", "chaos", "sparer"):
            for _ in range(4):
                if E.kampf.free_points(z) <= 0:
                    break
                sp = sorted(defs["specials"].items(), key=lambda kv: (kv[1]["tier"], kv[0]))
                if self.profil:
                    # Stable per profile + seed; explores different legal builds.
                    self.rng.shuffle(sp)
                    sp.sort(key=lambda kv: kv[1]["tier"])
                neu = next((sid for sid, s in sp if sid not in E.kampf.known(z) and not E.kampf.learn_reason(z, defs, sid)), None)
                if not neu or not self.tu("skill_lernen", {"id": neu}, angebot=False):
                    break
                z = E.aktiv()
            own = E.kampf.besitz(z, defs)
            for slot, table in (("weapon", "weapons"), ("armor", "armors")):
                if not own[table]:
                    continue
                teil = (self.rng.choice(list(own[table])) if self.typ in ("sammler", "chaos")
                        else max(own[table], key=lambda i: defs[table][i].get("dmg", defs[table][i].get("schutz", 0))))
                if E.kampf.equipment(z).get(slot) != teil:
                    self.tu("ausruesten", {"platz": slot, "id": teil}, angebot=False)
            z = E.aktiv()
            w = E.kampf.werkstatt_ansicht(z, defs)
            if w and w["offen"] and not w["auftrag"]:
                for st in w["waffen"] + w["ruestungen"]:
                    if st["kosten"] and not st["fehlt"]:
                        self.tu("werkstatt_abgeben", {"platz": st["slot"], "id": st["id"]}, angebot=True)
                        break
            z = E.aktiv()
            ch = E.kampf.chip_ansicht(z, defs)
            # wie die Oberflaeche (slotKnopf): erst wenn Rosi die Chips kennt, und nur Chips der passenden Gruppe (02.11.2026:
            # vorher 50-mal "Werkstatt noch zu" und "passt nicht" im Live-Lauf, ein Bot-Fehler)
            frei = [x for x in (ch.get("pool") or []) if not x.get("ort")] if ch.get("nutzbar") else []
            for st in ch.get("stuecke") or []:
                passt = [x for x in frei if x["gruppe"] == st["gruppe"] and (not x.get("nur_waffe") or x["nur_waffe"] == st["id"])]
                if passt and len(st["belegt"]) < st["plaetze"]:
                    self.tu("chip_einsetzen", {"platz": st["slot"], "id": st["id"], "familie": passt[0]["familie"]}, angebot=False)
                    break

    def tagesarbeit(self, z):
        modul, h, typ = self.modul, E.handel, self.typ
        self.m["sekunden"]["laeden"] += SEKUNDEN["laden"]
        h.init(z, modul)
        laeden = sorted(modul.get("laeden") or {})
        kauf = 0
        wunsch = {"sammler": 3, "kaempfer": 2, "romantiker": 2, "sparer": 1, "schwach": 1, "chaos": 3}[typ]
        z = E.aktiv()
        waren = []
        for k in laeden:
            if modul["laeden"][k].get("farm") or modul["laeden"][k].get("werkzeug_laden"):
                continue
            for w in h.sortiment(z, modul, k) or []:
                waren.append((k, w))
                self.m["laeden"][k] = max(self.m["laeden"][k], 1)
        self.rng.shuffle(waren)
        waren.sort(key=lambda kw: self._kaufwert(z, kw[1]), reverse=True)
        reserve = {"sparer": 400, "schwach": 200}.get(typ, 80)
        # Volle Tasche (Interaction 02.11.2026: Kaempfer-Typen hatten 15-17 volle Tage und nie verkauft): wie ein Mensch erst
        # die groessere Tasche, wenn das Geld reicht, dann verkaufen, was dem Typ am wenigsten wert ist, bis wieder Platz ist
        voll = lambda z: E.zustand.belegt(z, modul) >= .75 * E.zustand.inventar_plaetze(z, modul)
        naechste = (h.tasche_ansicht(z, modul) or {}).get("naechste")
        if voll(z) and naechste and not naechste["fehlt"] and z["konto"] >= naechste["geld"] + reserve:
            self.tu("tasche_kaufen", {}, angebot=False)
        for _ in range(10):
            z = E.aktiv()
            ank = h.ankauf(z, modul) if voll(z) else []
            if not ank or not self.tu("verkaufen", dict(art=(w := min(ank, key=lambda x: (self._kaufwert(z, x), x["preis"])))["art"], id=w["id"]), angebot=False):
                break
        z = E.aktiv()
        if not h.platz_frei(z, modul):         # a player sees the full bag and stops: count the day, don't hammer the shop
            self.m["tasche_voll_tage"] = self.m.get("tasche_voll_tage", 0) + 1
            waren = []
        for k, w in waren:
            if kauf >= wunsch or self._kaufwert(z, w) <= 0:
                break
            z = E.aktiv()
            if w["preis"] + reserve <= z["konto"] and not w.get("im_inventar"):
                if not E.zustand.platz_fuer(z, modul, w["id"]):     # the bag filled up while shopping: a player sees it and stops
                    continue
                if self.tu("kaufen", {"laden": k, "id": w["id"]}, angebot=False):
                    kauf += 1
        z = E.aktiv()
        if typ in ("sparer", "sammler", "chaos") and "toto" in (modul.get("laeden") or {}):
            ank = h.ankauf(z, modul)
            if ank:
                self.tu("verkaufen", {"art": ank[0]["art"], "id": ank[0]["id"]}, angebot=False)
        z = E.aktiv()
        if typ in ("sammler", "kaempfer", "chaos"):
            for k in ("alva", "petru"):
                if k in laeden and self.rng.random() < .3:
                    self.tu("laden_besuch", {"laden": k}, angebot=False)
                    if E.aktiv()["status"] == "kampf":
                        return
        self.kochen(E.aktiv())
        self.farm(E.aktiv())
        self.werkzeuge(E.aktiv())
        z = E.aktiv()
        if typ == "sammler" and z["konto"] > 700:
            self.tu("tasche_kaufen", {}, angebot=False)
        z = E.aktiv()
        if typ == "sammler":
            nutzbar = next((i for i in z["inventar"] if modul["items"].get(i, {}).get("art") == "verbrauch"), None)
            if nutzbar:
                self.tu("benutzen", {"id": nutzbar}, angebot=False)

    def _kaufwert(self, z, w):
        typ, it = self.typ, self.modul["items"].get(w["id"], {})
        art = it.get("art")
        if typ == "chaos":
            return self.rng.random()
        if typ == "sammler":
            return 1 + (0 if w["id"] in self.m["items"] else 3)
        if typ == "kaempfer":
            return 5 if it.get("kampf") else 2 if art in ("attribut", "gluecksbringer") else 0
        if typ == "romantiker":
            ziel = self.partner(z)
            return 5 * (it.get("geschenk") or {}).get(ziel, 0) if art == "geschenk" and not w.get("intim") else 0
        if typ == "sparer":
            return 3 if art in ("werkzeug", "gluecksbringer") else 0
        return 1 if art == "snack" else 0

    def kochen(self, z):
        modul, h, typ = self.modul, E.handel, self.typ
        if typ == "schwach" and z["tag"] % 3:
            return
        vorrat = E.kuechen.vorrat_ansicht(z, modul)
        rolle = {}
        for x in vorrat:
            rolle.setdefault(x["rolle"], x["key"])
        if len(rolle) == 3 and h.essen_frei(z, modul):
            if self.tu("kochen_baukasten", {"basis": rolle["basis"], "haupt": rolle["haupt"], "akzent": rolle["akzent"], "fuer": "crew"}, angebot=False):
                return
        gerichte = h.gerichte(z, modul)
        if gerichte and typ != "sparer":
            self.tu("kochen", {"id": gerichte[z["tag"] % len(gerichte)]["id"], "fuer": "crew"}, angebot=False)

    def farm(self, z):
        if (self.typ not in ("sammler", "sparer", "chaos") and self.profil_id != "noor") or not E.kuechen.nonna_offen(z, self.modul):
            return
        modul = self.modul
        a = E.farm.ansicht(z, modul)
        if not a:
            return
        n = E.kuechen.nonna_ansicht(z, modul)
        if n and n.get("waren") and z["konto"] > 200:
            w = self.rng.choice(n["waren"])
            self.tu("nonna_kaufen", {"id": w["id"], "n": 1}, angebot=False)
        if a["pflanzen"] and z["konto"] > 150:
            self.tu("garten_pflanzen", {"beet": 0, "pflanze": self.rng.choice(a["pflanzen"])["id"]}, angebot=False)
        for s in a["staelle"]:
            if not s["gekauft"] and s["naechste"] and s["naechste"]["geht"]:
                self.tu("stall_kaufen", {"art": s["art"]}, angebot=True)
                break
            if s["gekauft"] and s["naechste"] and s["naechste"]["geht"]:
                self.tu("stall_ausbauen", {"art": s["art"]}, angebot=True)
                break
            if s["gekauft"] and len(s["tiere"]) < s["plaetze"] and z["konto"] > s["baby_preis"] + 100:
                self.tu("tier_kaufen", {"art": s["art"]}, angebot=False)
                break
            reif = [t for t in s["tiere"] if t["schlachtbar"]]
            if reif and self.typ != "sammler":
                self.tu("tier_schlachten", {"art": s["art"], "id": reif[0]["id"]}, angebot=True)
                break
        self.tu("nonna_verlassen", {}, angebot=False)
        if E.aktiv().get("kueche", {}).get("fred") is not None:
            self.tu("fred_gehoert", {}, angebot=False)

    def werkzeuge(self, z):
        modul = self.modul
        if self.typ not in ("sammler", "sparer", "chaos", "kaempfer") or not E.abbau.petru_offen(z, modul):
            return
        for x in E.abbau.werkzeug_ansicht(z, modul) or []:
            n = x.get("naechste")
            if n and n.get("geht") and z["konto"] > n["geld"] + 60:
                self.tu("petru_kaufen", {"werkzeug": x["id"]}, angebot=True)
                z = E.aktiv()
        for f in E.abbau.fisch_ansicht(z, modul) or []:
            if self.typ in ("sparer", "sammler") and f.get("n", 1) > 0:
                self.tu("petru_fisch", {"fisch": f.get("id"), "alle": False}, angebot=False)
                break
        for k in E.koeder.ansicht(E.aktiv(), modul) or []:
            if k.get("geht"):
                self.tu("petru_koeder", {"koeder": k["id"]}, angebot=True)
                break

    # ------------------------------------------------------------ scenes
    def szene(self, z):
        sz = z["szene"]
        modul = self.modul
        if sz.get("wahlmoment_offen"):
            anzahl = max(1, len((E.szene.wahlmoment_ansicht(z, sz, modul) or {}).get("optionen") or [0]))
            i = self.rng.randrange(anzahl) if self.typ in ("sammler", "chaos") else 0
            self.tu("waehlen", {"index": i})
            return
        schl = "%d-%s-%s" % (z["tag"], z["phase"], (sz.get("def") or {}).get("id"))
        anruf = (sz.get("def") or {}).get("anruf")
        da = [p for p in sz.get("figuren", []) if p in modul["personen"]]
        if self.typ != "schwach" and schl + ":geben" not in self.erledigt:
            self.erledigt.add(schl + ":geben")
            gabe = next((i for i in z["inventar"] if modul["items"].get(i, {}).get("art") in ("geschenk", "snack")), None)
            if gabe and da and not anruf:
                ziel = self.partner(z) if self.partner(z) in da else da[0]
                if not (modul["items"][gabe].get("nur_fuer") and modul["items"][gabe]["nur_fuer"] != ziel):
                    self.tu("geben", {"id": gabe, "an": ziel}, angebot=False)
                    return
        if not anruf and schl + ":geste" not in self.erledigt:
            self.erledigt.add(schl + ":geste")
            gesten = (E.gesten.ansicht(z, modul, sz) or {}).get("liste", [])
            if self.profil:
                geplant = {d["pid"] for d in z.get("verabredungen", []) if d.get("tag", 0) >= z["tag"]}
                wahl = geste_waehlen(self.profil, gesten, self.rng, verabredet=geplant)
                if wahl and self.tu("geste", wahl):
                    return
                gesten = []
            for e in gesten:
                frei = [p for p, x in e["je"].items() if not x["gesperrt"] and not x["abgenutzt"]]
                if frei:
                    self.tu("geste", {"id": e["id"], "an": frei[0]})
                    return
        if self.profil_id in ("naomi", "lenny") and not anruf and schl + ":intim" not in self.erledigt:
            self.erledigt.add(schl + ":intim")
            frei = (E.gesten.ansicht(z, modul, sz) or {}).get("intim") or []
            self.m["peer"]["signale"]["intim_optionen_sichtbar"] += len(frei)
            # Preferred/neutral unlocked suggestions only. Generated consent responses remain untested.
            erlaubt = [x for x in frei if not x.get("nein")]
            if erlaubt:
                x = self.rng.choice(erlaubt)
                if self.tu("intim", {"an": x["an"], "tag": x["tag"]}, angebot=True):
                    return
        if (self.typ == "romantiker" or self.profil_id == "lenny") and not anruf:
            g = E.gesten.ansicht(z, modul, sz) or {}
            if g.get("zeit_angebot"):
                self.tu("zeit_antwort", {"ja": True})
                return
            frei = [p for p, x in (g.get("zeit") or {}).items() if x["frei"]]
            if frei and schl + ":zeit" not in self.erledigt:
                self.erledigt.add(schl + ":zeit")
                self.tu("zeit", {"an": frei[0]}, angebot=False)
                return
        if self.typ in ("sammler", "chaos") and E.ermittlung.aktiv(z) and schl + ":erm" not in self.erledigt:
            self.erledigt.add(schl + ":erm")
            wege = [w for w in E.ermittlung.moeglich(z, modul, sz) if not w.get("sperre")]
            if wege:
                self.tu("ermitteln", {"weg": wege[0]["weg"]})
                return
            wid = E.ermittlung.widerspruch_aktionen(z, modul, sz)
            if wid:
                self.tu("widerspruch", {"id": wid[0]["id"], "beschuldigen": False}, angebot=False)
                return
            kon = E.ermittlung.konfrontation_aktionen(z, modul, sz)
            if kon and z["tag"] >= 4:
                self.tu("konfrontieren", {"id": kon[0]["id"]}, angebot=False)
                return
        if self.typ == "sammler" and ("vorschlaege", z["tag"]) not in self.erledigt:
            self.erledigt.add(("vorschlaege", z["tag"]))
            self.tu("vorschlaege", {}, angebot=False)
            return
        if sum(1 for e in sz.get("log", []) if e.get("art") == "duc") < 2:
            self.tu("zug", {"text": "I listen and help where I can."})
            return
        self.tu("ende")

    # ------------------------------------------------------------ fights
    def kampfzug(self, z):
        k = z["kampf"]
        if k["phase"] == "ende":
            erg = (k.get("ergebnis") or {}).get("art")
            if erg == "niederlage" and E.expedition.aktiv(z):
                beute = E.expedition.beute(z, self.modul, self.kdefs)
                if beute and not (E.expedition.aktiv(z) or {}).get("behalten"):
                    if self.tu("expedition_behalten", {"id": beute[0]["id"]}, angebot=False):
                        return
            if erg == "niederlage" and k["def"].get("neustart_bei_niederlage"):
                self.niederlagen[k.get("definition")] += 1
            self.tu("kampf_schliessen")
            return
        if k["phase"] == "parade":
            self.kampf["paraden"] += 1 if self.kampf else 0
            per, gut = self.t["parade"]
            if self.niederlagen[k.get("definition")] >= 5:   # a wall this type cannot pass: note it, then help him through
                if self.niederlagen[k.get("definition")] == 5:
                    self.m["hilfe"].append({"tag": z["tag"], "phase": z["phase"],
                        "art": "Kampf nach 5 Niederlagen mit Hilfe", "kampf": k.get("definition"),
                        "eingriff": "Parade künstlich auf perfekt gesetzt", "niederlagen_vorher": 5,
                        "parade_vorher": list(self.t["parade"]), "parade_nachher": [1, 1]})
                    self.niederlagen[k.get("definition")] += 1
                if self.kampf is not None:
                    self.kampf["hilfe_aktiv"] = True
                per, gut = 1, 1
            p = k.get("parade") or {}
            if p.get("finte") and (per, gut) != (1, 1):          # Finten (03.11.2026): Annahme, bis echte Spieler gemessen sind
                typ = (k["gegner"][p.get("gegner", 0)] or {}).get("typ")
                bekannt = typ in (z.get("bestiarium") or {})        # wer die Art schon pariert hat, kennt den Rhythmus
                per, gut = per * FINTE_FAKTOR[bekannt][0], gut * FINTE_FAKTOR[bekannt][1]
                if self.kampf is not None:
                    self.kampf["finten"] = self.kampf.get("finten", 0) + 1
            r = self.rng.random()
            wahl = "perfekt" if r < per else "gut" if r < gut else "verfehlt"
            if p.get("nur_ausweichen") or p.get("modus") == "ring":
                wahl = "ausweichen" if wahl != "verfehlt" and p.get("modus") == "ring" else "verfehlt"
            self.tu("kampf_parade", {"ergebnis": wahl, "revision": k["revision"]})
            return
        if k["phase"] != "spieler_wahl" or E.kampf.must_skip(k["spieler"]):
            self._zug("aussetzen", None, k)
            return
        if self.kampf:
            self.kampf["zuege"] += 1
        befehl, ziel = self.zug_waehlen(z, k)
        self.m["befehle"][befehl if befehl != "faehigkeit" else "f:" + str(ziel)] += 1
        if self.kampf:
            self.kampf["befehle"][befehl] += 1
        if not self._zug(befehl, ziel, k, angebot=False):
            k2 = E.aktiv().get("kampf")
            if k2:
                self._zug("angriff", None, k2)

    def _zug(self, befehl, ziel, k, angebot=True):
        return self.tu("kampf_zug", {"befehl": befehl, "ziel": ziel, "revision": k["revision"]}, angebot=angebot)

    def zug_waehlen(self, z, k):
        modul = self.modul
        lebend = E.kampf.lebend(k)
        if not lebend:
            return "angriff", None
        g = lebend[0]
        sp = k["spieler"]
        skills = {s["id"]: s for s in E.kampf.skills_view(z, k)}
        frei = lambda sid: sid in skills and not skills[sid]["gesperrt"]        # noqa: E731
        items = [x for x in E.kampf.gegenstaende(z, modul) if not x["gesperrt"]]
        if self.t["stil"] == "zufall":
            wurf = self.rng.random()
            if wurf < .15:
                return "verteidigen", None
            if wurf < .25 and items:
                return "gegenstand", self.rng.choice(items)["id"]
            los = [s for s in skills.values() if not s["gesperrt"]]
            if wurf < .55 and los:
                return "faehigkeit", self.rng.choice(los)["id"]
            if wurf < .60:
                return "fliehen", None
            return "angriff", None
        if g["def"].get("untouchable"):
            return ("faehigkeit", "reden") if frei("reden") else ("verteidigen", None)
        if self.t["stil"] == "einfach":
            heil = [x for x in items if x.get("heilen")] if self.typ != "sparer" else []
            if sp["lp"] < .3 * sp["lp_max"] and heil:
                return "gegenstand", heil[0]["id"]
            return "angriff", None
        if sp["lp"] < .35 * sp["lp_max"]:
            heil = [x for x in items if x.get("heilen")]
            if heil:
                return "gegenstand", max(heil, key=lambda x: x["heilen"])["id"]
        if g["def"].get("boss") and k["runde"] <= 2:
            gr = [x for x in items if (modul["items"][x["id"]].get("kampf") or {}).get("granate")]
            if gr:
                return "gegenstand", gr[0]["id"]
        if g["def"].get("weakness") == "charm" and frei("reden"):
            return "faehigkeit", "reden"
        if not g.get("schwaeche_bekannt") and k["runde"] <= 1 and frei("schwachstelle"):
            return "faehigkeit", "schwachstelle"
        spez = [s for s in skills.values() if s["art"] == "spezial" and not s["gesperrt"] and not s.get("hinweis")]
        if spez:
            return "faehigkeit", max(spez, key=lambda s: s["stufe"])["id"]
        if g["def"].get("weakness") == "courage" and frei("einschuechtern"):
            return "faehigkeit", "einschuechtern"
        return "angriff", None

    # ------------------------------------------------------------ hearing and storm: gate moves, some types vary them
    def verhandlung(self, z):
        v = z["verhandlung"]
        a = L.schritt(z, {"erledigt": {}, "schritte": []})
        if self.typ in ("schwach", "chaos") and not v["fertig"] and a[1].get("was") == "present" and self.rng.random() < .5:
            a = ("verhandlung", {"was": "aufgeben"})
        if self.typ == "chaos" and not v["fertig"] and a[1].get("was") == "anklage":
            pids = E.anhoerung._verdaechtige(z, self.modul)
            a = ("verhandlung", {"was": "anklage", "pid": self.rng.choice(pids)})
        if self.typ == "chaos" and not v["fertig"] and a[1].get("was") == "plaedoyer":
            a = ("verhandlung", {"was": "plaedoyer", "art": self.rng.choice(("gnade", "haerte"))})
        self.tu(*a, angebot=a[1].get("art") != "haerte")

    def sturm(self, z):
        a = L.schritt(z, {"erledigt": {}, "schritte": []})
        if a[1].get("was") == "einteilen" and self.typ in ("chaos", "sammler"):
            posten = list(a[1]["posten"].keys())
            crew = list(a[1]["posten"].values())
            self.rng.shuffle(crew)
            a = (a[0], {"was": "einteilen", "posten": dict(zip(posten, crew))})
        if a[1].get("was") == "sprint" and self.typ == "schwach":
            a = (a[0], {"was": "sprint", "rennen": False})
        self.tu(*a)


def _maske(s):
    return re.sub(r"\s+", " ", s).strip()


def _deutsch(s):
    s = NAMEN_OK.sub("", s)
    return bool(DE_STARK.search(s)) or len(set(DE_SCHWACH.findall(s))) >= 2


def _ausgang(a):
    if not isinstance(a, dict):
        return None
    return {k: x for k, x in a.items() if isinstance(x, (int, float, bool))} or None


def _texte(x, pfad=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from _texte(v, pfad + "/" + str(k))
    elif isinstance(x, list):
        for v in x:
            yield from _texte(v, pfad + "[]")
    elif isinstance(x, str):
        yield pfad, x


def _ohne_bild(x, pfad=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ("bild", "hintergrund", "avatar") and v is None:
                yield pfad + "/" + k
            else:
                yield from _ohne_bild(v, pfad + "/" + str(k))
    elif isinstance(x, list):
        for v in x:
            yield from _ohne_bild(v, pfad + "[]")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    typ, seed, ziel = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    m = Lauf(typ, seed).spielen()
    json.dump(m, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, default=lambda o: dict(o) if isinstance(o, collections.Counter) else str(o))
    print("%s %d: %d Schritte, Tag %s/%s, Abstuerze %d, Sackgassen %d" % (
        typ, seed, m["schritte"], m["ende"]["tag"], m["ende"]["status"], len(m["abstuerze"]), len(m["sackgassen"])))


if __name__ == "__main__":
    main()

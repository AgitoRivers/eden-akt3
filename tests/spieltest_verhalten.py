"""Engine-free decision helpers. Consume only labels/options exposed to the player.

These are transparent heuristics, not a semantic player LLM or a complete UI agent.
Unrecognised wording is explored through seeded ties instead of hidden reward values.
"""
import re

VERSION = 2

FLIRT = re.compile(r"come (?:and |on |up |to |see|get)|on my way|be right|report to|challenge accepted|"
                   r"competition|you look|beautiful|gorgeous|midnight|kiss|join you|can't wait|"
                   r"your name|my name|your place|take.*lead|winning|she wins|for both|didn't blink|dare|date|together", re.I)
DISTANZ = re.compile(r"cool off|goodnight|get some sleep|not (?:today|tonight|now)|"
                     r"hang up|leave her|walk away|ignore|leaves it on read|another time", re.I)
HILFE = re.compile(r"help|listen|together|comfort|ask|stay|thank|honest|decides|her choice", re.I)
ERKUNDEN = re.compile(r"look|search|explore|check|examine|investigate|read|climb", re.I)
KAMPF = re.compile(r"fight|attack|charge|hold.*ground|drives.*off|goes for", re.I)
GELD = re.compile(r"pays|sell|money|cheap|save|earn", re.I)


def sichtbare_option(o):
    """Never pass raw consequences, success branches, hidden affinity or flags to a chooser."""
    return {k: o.get(k) for k in ("text", "art", "energie", "gesperrt")}


def antwort_werten(p, option, kontext="", wiederholt=0):
    o = sichtbare_option(option)
    if o.get("gesperrt"):
        return float("-inf"), ["sichtbar gesperrt"]
    text = o.get("text") or ""
    reasons, score = [], -3.0 * wiederholt
    romance = p["vertrauen"] + p["begehren"] >= 2
    invitation = bool(FLIRT.search(kontext))
    if romance and FLIRT.search(text):
        score += 3 + p["begehren"]
        reasons.append("passender Flirt im sichtbaren Antworttext")
    if romance and (DISTANZ.search(text) or o.get("art") == "auflegen") and invitation:
        score -= 6
        reasons.append("weist eine sichtbare Einladung ab")
    if HILFE.search(text):
        score += p["vertrauen"]
        reasons.append("Zuhören, Fürsorge oder gemeinsames Handeln")
    if ERKUNDEN.search(text):
        score += 3 * p["ort"]
        reasons.append("erkundende Handlung")
    if KAMPF.search(text):
        score += 5 * (p["ort"] - .5)
        reasons.append("Kampfbereitschaft des Profils")
    if p["basis"] == "sparer" and GELD.search(text):
        score += 3
        reasons.append("sichtbarer wirtschaftlicher Anreiz")
    return score, reasons or ["keine sichere Textzuordnung; erkundende Auswahl"]


def geste_waehlen(p, gesten, rng, ziel=None, verabredet=()):
    """Choose a legal, unused visible gesture; invitations no longer lose to first-list compliments."""
    romance = p["vertrauen"] + p["begehren"] >= 2
    rang = ({"einladen": 12, "fragen": 7, "necken": 6, "hand": 5, "kompliment": 4}
            if romance else {"fragen": 7, "necken": 5, "kompliment": 4})
    if p["intim"] >= 8:
        rang.update(necken=9, kuessen=8)
    candidates = []
    for g in gesten:
        for pid, info in g.get("je", {}).items():
            if g["id"] == "einladen" and verabredet:
                continue
            if not info.get("gesperrt") and not info.get("abgenutzt"):
                # Input contains public eligibility only, not hidden character preferences.
                candidates.append((rang.get(g["id"], 1) + (1 if pid == ziel else 0), rng.random(), g["id"], pid))
    if not candidates:
        return None
    _, _, gid, pid = max(candidates)
    return dict(id=gid, an=pid)


def termine(z):
    return {(d.get("pid"), d.get("tag"), d.get("phase")) for d in z.get("verabredungen", [])}


def date_signale(vorher, nachher, aktion, daten):
    """Attempts, scheduled dates and actual scenes are different evidence."""
    out = {}
    if aktion == "geste" and daten.get("id") == "einladen":
        out["einladungen_angenommen_engine"] = 1
    neu = termine(nachher) - termine(vorher)
    if neu:
        out["dates_vereinbart"] = len(neu)
    a = vorher.get("szene") or {}
    b = nachher.get("szene") or {}
    sid = (b.get("def") or {}).get("id") or ""
    if nachher.get("status") == "szene" and sid.startswith("date_") and (
            vorher.get("status") != "szene" or (a.get("def") or {}).get("id") != sid or
            (vorher.get("tag"), vorher.get("phase")) != (nachher.get("tag"), nachher.get("phase"))):
        out["dates_begonnen"] = 1
    return out

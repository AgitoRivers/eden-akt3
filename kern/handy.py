# -*- coding: utf-8 -*-
"""Duc's phone: the women's life outside his scenes.

Rule of the engine: CODE decides and books, the MODEL writes and sorts.
  * One continuous chat per woman (z["handy"] has exactly one thread per person); every line carries day and phase.
  * Memory: every exchange goes into the woman's chronicle (only SHE knows it) - scenes, the referee and later replies
    know it. Next scene start: she may pick up Duc's best text line (chronik.rueckbezug_handy, marked with a speech
    bubble in the "last time" line).
  * Driver (24.10.2026, Duc): she texts only when something happened between you since her last text - at least
    min_progress points of trust/desire gained (talk, gesture, shared scene, chat). More extrovert play = more texts.
    No daily cap for incoming texts; no base chance without progress.
  * Consequences with guard rails: the model only sorts Duc's text into a tone (warm, funny, flirty, pushy, rude,
    apology, neutral); the code decides what follows: small points, at most ONE effect per woman and day, talk carries
    only up to stage 3, day 1 only positive, too forward at low trust costs trust. At most max_replies answers per
    woman and day, then she sleeps / is on watch.
  * Answer chips: three suggested replies (warm / funny / flirty) written by the model, labelled by the code with the
    tone, the effect and the risk. A chat NEVER costs a phase or an action (Modell B).
  * Referee: every text she writes is checked once against her known facts (no invented events), one rewrite.
Numbers live in module\\<module>\\handy.json (builder werkzeuge\\eden_rise\\handy_eden_rise.py); DEFAULTS below are the
fallback."""
import copy, json, os, random, re

from . import buehne, chronik, figurenrahmen, llm, zustand
from . import reaktion as reaktionen

STIL = ("You write a text message from {name} to Duc on her phone. Short like a real text: one to three lines, "
        "lowercase allowed, no stage directions, no asterisks, no quotation marks. Stay in character. English. "
        "Like a real person you may send it as two or three short separate texts, one per line.")
TEILE_MAX = 3                # a reply arrives as up to three bubbles (Duc 03.11.2026: "mehrere kurze, menschlich")
KONTEXT_ZEILEN = 14          # how much of the chat the model sees (a thread grows over days)
WACHE_ORTE = ("generator_room", "power_room", "bridge", "workshop")

# Fallback / default numbers. tones: axis (vertrauen|begehren), points, impression (for her reply), label (UI, German).
DEFAULTS = {
    "tones": {
        "warm": {"axis": "vertrauen", "points": 4, "impression": "It touched her a little.", "label": "Trust ↑"},
        "funny": {"axis": "begehren", "points": 4, "impression": "It made her smile.", "label": "Desire ↑"},
        "flirty": {"axis": "begehren", "points": 4, "impression": "It flustered her a little, in a good way.",
                   "label": "Desire ↑"},
        "apology": {"axis": "vertrauen", "points": 4, "impression": "She appreciates that he said sorry.",
                    "label": "Trust ↑"},
        "pushy": {"axis": "vertrauen", "points": -4, "impression": "It annoyed her - she may say so, briefly.",
                  "label": "Trust ↓"},
        "rude": {"axis": "vertrauen", "points": -4, "impression": "It stung - she answers cooler than usual.",
                 "label": "Trust ↓"},
        "neutral": {"axis": None, "points": 0, "impression": "", "label": "no effect"},
    },
    "chip_tones": ["warm", "funny", "flirty"],
    "flirt_min_trust": 2,         # below this stage a flirt is "too forward" and costs trust
    "backfire_points": -3,
    "backfire_impression": ("Duc's text was far too forward for how well she knows him. She is taken aback, deflects and "
                            "keeps her distance."),
    "max_replies": 3,             # answers per woman and day
    "min_progress": 4,            # points gained since her last text before she texts again
    "callback_days": 1,           # the callback may use texts that are at most this many days old
}

_CACHE = {}


def daten(modul):
    """DEFAULTS merged with module\\<id>\\handy.json (cached by modification time)."""
    pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", modul.get("id", ""),
                        "handy.json")
    try:
        mt = os.path.getmtime(pfad)
    except OSError:
        return DEFAULTS
    c = _CACHE.get(pfad)
    if c and c[0] == mt:
        return c[1]
    try:
        roh = json.load(open(pfad, encoding="utf-8"))
    except Exception:
        return DEFAULTS
    d = copy.deepcopy(DEFAULTS)
    for k, v in roh.items():
        if k == "tones" and isinstance(v, dict):
            for t, tv in v.items():
                d["tones"].setdefault(t, {}).update(tv)
        else:
            d[k] = v
    _CACHE[pfad] = (mt, d)
    return d


def chance(z, pid):
    w = z["werte"]
    return min(0.75, 0.15 + 0.08 * w.get("begehren." + pid, 0) + 0.05 * w.get("vertrauen." + pid, 0))


# ------------------------------------------------------------------ threads
def zusammenfuehren(z):
    """Old saves: several threads per woman -> one, in time order. Every line gets day/phase of its old thread.
    A thread stays unread if any part was unread. Returns True on change."""
    faeden, reihenfolge, geaendert = {}, [], False
    for f in z.get("handy", []):
        for v in f.get("verlauf", []):
            v.setdefault("tag", f.get("tag"))
            v.setdefault("phase", f.get("phase"))
        pid = f.get("von")
        if pid in faeden:
            g = faeden[pid]
            g["verlauf"] += f.get("verlauf", [])
            g["gelesen"] = bool(g.get("gelesen")) and bool(f.get("gelesen"))
            g["tag"], g["phase"] = f.get("tag"), f.get("phase")
            reihenfolge.remove(pid)
            reihenfolge.append(pid)
            geaendert = True
        else:
            faeden[pid] = f
            reihenfolge.append(pid)
    z["handy"] = [faeden[p] for p in reihenfolge]
    return geaendert


def faden_von(z, pid):
    """This woman's chat - created on demand. The thread with the newest message is last in the list."""
    liste = z.setdefault("handy", [])
    f = next((x for x in liste if x["von"] == pid), None)
    if f is None:
        f = {"von": pid, "tag": z["tag"], "phase": z["phase"], "gelesen": False, "verlauf": []}
    else:
        liste.remove(f)
    liste.append(f)
    return f


def _zeile(z, wer, text):
    return {"wer": wer, "text": text, "tag": z["tag"], "phase": z["phase"]}


MARKER = {"anruf": "(video call)", "verpasst": "(missed video call - Duc did not pick up)", "foto": "(she sends a photo)"}


def _verlauf_text(faden, p, letzte=KONTEXT_ZEILEN):
    echte = [v for v in faden["verlauf"] if v["wer"] != "system"]
    return "\n".join(MARKER[v["art"]] if v.get("art") in MARKER else
                     "%s: %s" % ("Duc" if v["wer"] == "duc" else p["name"].split()[0], v["text"]) for v in echte[-letzte:])


_GESAGT = re.compile(r'[“"]([^”"]+)[”"]')


def event_ablegen(z, modul, ev, offen):
    """Das Handy erinnert sich (Paket 3, Duc 03.11.2026): a closed phone event (message, selfie, video call) lands in
    her chat thread - a grey marker for the call or her photo, her spoken lines, what Duc SAID (only a quoted answer, no
    narration) and her reaction. A call declined at the ring screen becomes "missed video call". Only women who can chat
    (ST card); favours stay secret, Megan and the others without a card stay out. -> number of new entries."""
    if not ev or ev.get("art") != "handy" or ev["personen"].get("favour") or not offen.get("ergebnis"):
        return 0
    pid = ev["personen"].get("anrufer") or (ev["personen"].get("selfie") or {}).get("frau")
    if pid not in modul["personen"] or not modul["personen"][pid].get("karte"):
        return 0
    from . import ereignisse                           # late: ereignisse imports a lot
    erg = offen["ergebnis"]
    o = (ev.get("optionen") or [{}])[erg["index"]] if erg["index"] < len(ev.get("optionen") or []) else {}
    neu = []
    if ev["personen"].get("art") == "video":
        if o.get("art") == "auflegen":                 # Decline gibt es nur vor dem Annehmen (Klingel-Bildschirm)
            neu.append(dict(_zeile(z, pid, "Missed video call"), art="verpasst"))
        else:
            neu.append(dict(_zeile(z, pid, "Video call"), art="anruf"))
    if offen.get("selfie"):
        neu.append(dict(_zeile(z, pid, "Photo"), art="foto", bild="/selfie/%s.webp" % offen["selfie"]))
    if not (neu and neu[0].get("art") == "verpasst"):
        neu += [_zeile(z, pid, zl["text"]) for _, zl in ereignisse.zeilen_aktiv(ev, z) if zl.get("wer") == pid and zl.get("text")]
        gesagt = _GESAGT.search(erg.get("text") or "")
        if gesagt:
            neu.append(_zeile(z, "duc", gesagt.group(1).strip()))
        r = erg.get("zeile") or {}
        if r.get("wer") == pid and r.get("text"):
            neu.append(_zeile(z, pid, r["text"]))
    if neu:
        faden_von(z, pid)["verlauf"] += neu
    return len(neu)


def _teile(text):
    """Her reply as separate bubbles: one per line, at most TEILE_MAX (the rest stays in the last one)."""
    zeilen = [z.strip().strip('"') for z in (text or "").splitlines() if z.strip()]
    if len(zeilen) > TEILE_MAX:
        zeilen = zeilen[:TEILE_MAX - 1] + [" ".join(zeilen[TEILE_MAX - 1:])]
    return zeilen or ["…"]


def _sagen(z, faden, pid, text):
    """Append her text as one or more bubbles."""
    for t in _teile(text):
        faden["verlauf"].append(_zeile(z, pid, t))


def _kurz(t, n=140):
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[:n - 1].rstrip() + "…"


# ------------------------------------------------------------------ replies per day
def genutzt(z, pid):
    s = z.get("handy_zaehler", {}).get(pid)
    return s["n"] if s and s.get("tag") == z["tag"] else 0


def rest(z, pid, modul=None):
    limit = (daten(modul) if modul else DEFAULTS)["max_replies"]
    return max(0, limit - genutzt(z, pid))


def ausrede(z, modul, pid):
    """Why she does not answer now: at night she sleeps or is on watch, otherwise she is busy (English, the player reads it)."""
    name = modul["personen"][pid]["name"].split()[0]
    ort = (modul["personen"][pid].get("ablauf") or {}).get(z["phase"])
    if z["phase"] == "nacht":
        return "%s %s – talk tomorrow." % (name, "is on watch" if ort in WACHE_ORTE else "is asleep")
    return "%s is busy right now – after your next scene." % name


def status(z, modul, pid):
    """One short line under her name in the chat (Duc 03.11.2026): where she is, asleep, on watch, busy."""
    p = modul["personen"][pid]
    if p.get("karte") and rest(z, pid, modul) == 0:
        return "asleep" if z["phase"] == "nacht" and (p.get("ablauf") or {}).get(z["phase"]) not in WACHE_ORTE else "busy"
    ort = buehne.wo_ist(z, modul, pid)
    if not ort:
        return "away"
    raum = (modul["raeume"].get(ort) or {}).get("label", "")
    if z["phase"] == "nacht":
        return "on watch · " + raum if ort in WACHE_ORTE else "asleep"
    return raum


def profilbild(z, pid):
    """Her contact picture: the last selfie she sent (album), else None (the client takes her face)."""
    s = [e for e in z.get("album") or [] if e.get("art") == "selfie" and e.get("wer") == pid and e.get("bild")]
    return "/selfie/%s.webp" % s[-1]["bild"] if s else None


def gesperrt(z, modul, pid):
    if not modul["personen"][pid].get("karte"):           # ohne ST-Karte (Megan, Maxwell, Toto ...) kann das Modell nicht antworten
        return "%s only sends a message – no reply needed." % modul["personen"][pid]["name"].split()[0]
    return None if rest(z, pid, modul) > 0 else ausrede(z, modul, pid)


# ------------------------------------------------------------------ driver: progress since her last text
def _summe(z, pid):
    return zustand.punkte(z, "vertrauen." + pid) + zustand.punkte(z, "begehren." + pid)


def fortschritt(z, pid):
    """Points of trust+desire gained with her since her last text. Missing baseline (old save): start quiet."""
    stand = z.setdefault("handy_stand", {})
    jetzt = _summe(z, pid)
    if pid not in stand:
        stand[pid] = jetzt
        return 0
    if jetzt < stand[pid]:
        stand[pid] = jetzt                  # a loss lowers the bar, so the way back up counts again
    return jetzt - stand[pid]


# ------------------------------------------------------------------ referee for her texts (kept small)
PRUEF_SYS = "You are a careful referee for a story game. You check one text message against what is known."
PRUEF_FRAGEN = {
    "contradicts_facts": "Does the text contradict one of the known facts listed below (who did what with whom, what was "
                         "decided)? Not mentioning facts does NOT count.",
    "invents_event": "Does the text claim that something specific happened between her and Duc (or on the boat today) "
                     "that is NOT in the facts, the chat or today's list? Plans, feelings, questions and small talk are "
                     "NOT inventions.",
}
PRUEF_HINWEIS = {"contradicts_facts": "it contradicted something that already happened",
                 "invents_event": "it invented something that never happened"}


def _fakten(z, modul, pid, faden, p):
    teile = chronik.fuer_figur(z, modul, pid, [])
    heute = ["%s: %s" % (h["phase"], h["kurz"] or h["titel"]) for h in z.get("heute", []) if pid in h.get("anwesend", [])]
    chat = _verlauf_text(faden, p, 8) if faden and faden.get("verlauf") else ""
    return ("Known facts:\n%s\n\nToday (what she took part in):\n%s\n\nThe chat so far:\n%s" % (
        "\n".join(teile) or "(none)", "\n".join(heute) or "(nothing)", chat or "(empty)"))


def pruefen(z, modul, pid, faden, p, text):
    """-> list of broken rules (empty = fine). One yes/no call with a fixed answer format."""
    d, _ = llm.json_chat(PRUEF_SYS, "%s\n\nHer text: %s\n\nAnswer each question with true or false, as JSON:\n%s" % (
        _fakten(z, modul, pid, faden, p), text, "\n".join("- %s: %s" % kv for kv in PRUEF_FRAGEN.items())),
        llm.bool_grammatik(list(PRUEF_FRAGEN)), max_tokens=40, sampler={"temperature": 0.0})
    return [k for k in PRUEF_FRAGEN if (d or {}).get(k) is True]


def _schreiben(z, modul, pid, faden, p, bogen_von, user, max_tokens=90):
    """Write her text; the referee checks it once, one rewrite, then accept (like the scenes)."""
    zusatz = ""
    text = ""
    for versuch in range(2):
        text, _ = llm.chat(STIL.format(name=p["name"]) + "\n\n[Character]\n" + bogen_von(pid), user + zusatz,
                           {"temperature": 1.0, "min_p": 0.1}, max_tokens)
        text = text.strip().strip('"')
        if not text or versuch == 1:
            break
        verstoesse = pruefen(z, modul, pid, faden, p, text)
        if not verstoesse:
            break
        zusatz = "\n\n(Your previous draft broke a rule: %s. Write it again without that.)" % "; ".join(
            PRUEF_HINWEIS[v] for v in verstoesse)
    return text


# ------------------------------------------------------------------ B: tone and consequences
def ton_bestimmen(z, modul, p, faden, text):
    toene = list(daten(modul)["tones"])
    letzte_sie = next((v["text"] for v in reversed(faden["verlauf"]) if v["wer"] == faden["von"]), "")
    d, _ = llm.json_chat(
        "You classify the tone of a text message from Duc to a woman he works with on a yacht. Choose exactly one: "
        "warm (caring, supportive, sincere), funny (a joke or banter), flirty (a compliment, flirt or romantic/sexual "
        "hint), pushy (demanding, impatient, pressuring), rude (dismissive, insulting, careless), apology (he says "
        "sorry or makes amends), neutral (plain logistics or small talk).",
        "%s's last text to him: %s\n\nDuc's text: %s\n\nWhich tone? JSON." % (
            p["name"].split()[0], letzte_sie or "(none)", text), llm.wahl_grammatik("tone", toene), max_tokens=20,
        sampler={"temperature": 0.0})
    ton = (d or {}).get("tone")
    return ton if ton in toene else "neutral"


def wirken(z, modul, pid, ton):
    """The rules in code. -> (lines for the display, impression for her reply, backfire?)."""
    dat = daten(modul)
    t = dat["tones"].get(ton) or dat["tones"]["neutral"]
    if not t.get("axis") or not t.get("points"):
        return [], t.get("impression", ""), False
    heute = z.setdefault("handy_wirkung", {})
    achse, pts = t["axis"], t["points"]
    backfire = ton == "flirty" and z["werte"].get("vertrauen." + pid, 0) < dat["flirt_min_trust"]
    if backfire:
        achse, pts = "vertrauen", dat["backfire_points"]
    eindruck = dat["backfire_impression"] if backfire else t.get("impression", "")
    if heute.get(pid) == z["tag"]:
        return [], eindruck, backfire                   # one text already had its effect today - the rest is mood
    if pts < 0 and z["tag"] <= reaktionen.NUR_POSITIV_BIS_TAG:
        return [], eindruck, False                      # day 1 is positive only (like the scenes)
    key = "%s.%s" % (achse, pid)
    p0 = zustand.punkte(z, key)
    zeilen = zustand.punkte_add(z, modul, key, pts, deckel=zustand.GESPRAECH_DECKEL if pts > 0 else None, quelle="handy")
    if pts > 0 and zustand.punkte(z, key) == p0:
        from . import figurenrahmen
        zeilen += figurenrahmen.topf_kommentar(z, modul, pid, key, "handy")
    if zustand.punkte(z, key) != p0:
        heute[pid] = z["tag"]
    return zeilen, eindruck, backfire


# ------------------------------------------------------------------ answer chips
CHIP_SYS = ("You write text messages for Duc, the new first officer of a yacht, replying to a woman of the crew. Short "
            "like real texts: one or two lines, lowercase allowed, no stage directions, no asterisks, English. Duc is "
            "dry, warm and quick-witted. Write three different replies to her last text, one per tone: warm (caring, "
            "sincere), funny (banter) and flirty (a compliment or a light flirt).")


def chips_ansicht(z, modul, faden):
    """The chips of this thread with the labels the code derives: tone, effect, risk."""
    dat = daten(modul)
    pid = faden["von"]
    benutzt = z.get("handy_wirkung", {}).get(pid) == z["tag"]
    out = []
    for c in faden.get("chips") or []:
        t = dat["tones"].get(c["tone"]) or {}
        riskant = c["tone"] == "flirty" and z["werte"].get("vertrauen." + pid, 0) < dat["flirt_min_trust"]
        etikett = t.get("label", "")
        if benutzt and t.get("axis"):
            etikett = "only mood today"
        out.append({"ton": c["tone"], "text": c["text"], "etikett": etikett,
                    "riskant": "too soon?" if riskant else ""})
    return out


def make_chips(z, modul, index, bogen_von):
    """Generate the three answer chips for thread `index` (stored in the thread, cleared when Duc sends)."""
    faden = z["handy"][index]
    pid = faden["von"]
    p = modul["personen"][pid]
    sperre = gesperrt(z, modul, pid)
    if sperre:
        raise ValueError(sperre)
    dat = daten(modul)
    tones = [t for t in dat["chip_tones"] if t in dat["tones"]]
    s = '"\\"" ( [^"\\\\\\n] | "\\\\\\"" )* "\\""'
    gram = ('root ::= "{" ws ' + ' "," ws '.join('"\\"%s\\":" ws s' % t for t in tones) + ' ws "}"\ns ::= ' + s + "\n"
            + llm.B)
    stufe = z["werte"].get("vertrauen." + pid, 0), z["werte"].get("begehren." + pid, 0)
    user = ("%s\n\nHow close they are (never mention numbers): trust %d of 5, desire %d of 5.\n\nShe is: %s\n\nWrite "
            "Duc's three replies now. JSON with the keys: %s." % (
                _verlauf_text(faden, p) or "(no messages yet)", stufe[0], stufe[1], bogen_von(pid)[:600],
                ", ".join(tones)))
    d, _ = llm.json_chat(CHIP_SYS, user, gram, max_tokens=300, sampler={"temperature": 0.9})
    chips = []
    for t in tones:
        text = ((d or {}).get(t) or "").strip().strip('"')
        if text:
            chips.append({"tone": t, "text": text})
    if not chips:
        raise ValueError("No reply ideas this time - try again.")
    faden["chips"] = chips


# ------------------------------------------------------------------ incoming texts
def nach_szene(z, modul, szene_def, figuren, bogen_von):
    """After a scene: women who were not there may text - only if something happened with them since their last text."""
    neu = []
    dat = daten(modul)
    for pid, p in modul["personen"].items():
        if not p.get("romanzierbar") or pid in figuren:
            continue
        if fortschritt(z, pid) < dat["min_progress"] or random.random() > chance(z, pid):
            continue
        # Only what she lived through herself; of other scenes she only knows who Duc was with (small boat).
        heute = "\n".join("- %s: %s" % (h["phase"], (h["kurz"] or h["titel"]) if pid in h["anwesend"] else "Duc spent the %s with %s." % (
            h["phase"], ", ".join(modul["personen"][x]["name"].split()[0] for x in h["anwesend"]) or "nobody"))
            for h in z["heute"])
        erinnerung = "\n".join(figurenrahmen.erinnerung(z, modul, pid))
        bisher = next((x for x in z.get("handy", []) if x["von"] == pid), None)
        chat = _verlauf_text(bisher, p, 8) if bisher and bisher["verlauf"] else ""
        text = _schreiben(z, modul, pid, bisher, p, bogen_von,
                          "What she remembers about Duc:\n%s\n\n%sToday on the boat:\n%s\n\nIt is now after \"%s\". "
                          "%s is not with Duc right now. Write the one text she sends him now - about something that "
                          "matters to her today, or him. Do not repeat what the chat already says." % (
                              erinnerung or "(little so far)",
                              ("Your chat with him so far:\n%s\n\n" % chat) if chat else "",
                              heute, szene_def["titel"], p["name"]))
        if text:
            f = faden_von(z, pid)
            f["tag"], f["phase"], f["gelesen"] = z["tag"], z["phase"], False
            f["chips"] = []
            _sagen(z, f, pid, text)
            z.setdefault("handy_stand", {})[pid] = _summe(z, pid)
            # memory: her own text belongs to what she knows (only she)
            chronik.eintragen(z, modul, "handy", "%s texted Duc: \"%s\"" % (p["name"].split()[0], _kurz(text)),
                              wer=[pid], dabei=[], wichtig=1, ort="handy")
            neu.append(pid)
    return neu


def antworten(z, modul, index, text, bogen_von, ton=None):
    """Duc answers in a thread. `ton` is set when he sent a chip unchanged - then no tone call is needed."""
    faden = z["handy"][index]
    pid = faden["von"]
    p = modul["personen"][pid]
    vorname = p["name"].split()[0]
    sperre = gesperrt(z, modul, pid)
    if sperre:
        raise ValueError(sperre)
    meine = _zeile(z, "duc", text)
    faden["verlauf"].append(meine)
    faden["chips"] = []
    toene = daten(modul)["tones"]
    ton = ton if ton in toene else ton_bestimmen(z, modul, p, faden, text)
    zeilen, eindruck, backfire = wirken(z, modul, pid, ton)
    # No numbers in the chat (Duc 03.11.2026, E-116): she reacts like a person - a heart when it landed, only "seen"
    # when it went wrong. Her "pot is full" sentence becomes a real text from her.
    topf = [m.group(1) for m in (re.search(r"“(.+)”$", x) for x in zeilen) if m]
    plus = [x for x in zeilen if not re.search(r"“(.+)”$", x)]
    tones_pts = (toene.get(ton) or {}).get("points") or 0
    if backfire or (plus and tones_pts < 0):
        meine["reaktion"] = "gesehen"
    elif plus and tones_pts > 0:
        meine["reaktion"] = "herz"
    z.setdefault("handy_zaehler", {})[pid] = {"tag": z["tag"], "n": genutzt(z, pid) + 1}
    letzte = rest(z, pid, modul) == 0
    hinweis = ""
    if eindruck:
        hinweis += "(%s)\n\n" % eindruck
    if letzte:
        hinweis += ("(This is the last text she answers today - she ends the chat naturally, e.g. going to sleep or "
                    "back to work.)\n\n")
    antwort = _schreiben(z, modul, pid, faden, p, bogen_von,
                         "What she remembers about Duc:\n%s\n\nThe chat so far:\n%s\n\n%sWrite her reply text now." % (
                             "\n".join(figurenrahmen.erinnerung(z, modul, pid)) or "(little so far)",
                             _verlauf_text(faden, p), hinweis))
    antwort = antwort or "…"
    _sagen(z, faden, pid, antwort)
    for t in topf:
        faden["verlauf"].append(_zeile(z, pid, t))
    faden["gelesen"] = True
    # memory: the exchange is in her chronicle - scenes, referee and later replies know it
    chronik.eintragen(z, modul, "handy", "Duc texted %s: \"%s\" (tone: %s). She replied: \"%s\"" % (
        vorname, _kurz(text), ton, _kurz(antwort)), wer=[pid], dabei=[], wichtig=2 if zeilen else 1, ort="handy")

# -*- coding: utf-8 -*-
"""Szenen-Laufzeit: eine Szene aus dem Tagesplan spielen.

Je Duc-Zug:  Probe? (W20, wenn Duc etwas Unsicheres versucht)  ->  wer antwortet (Angesprochene zuerst, dann Regie)
             -> Schauspielerin (eigenes Wissen) -> Richter (bei Verstoss neu)  ->  Gedanken nur nach Empathy-Probe
             -> Ereignis nach Zug n  ->  Sanduhr (gegen Ende ein Abschluss-Hinweis, bei 0 endet die Szene)
Szenenende:  Ausgaenge pruefen -> Folgen anwenden -> Gedaechtnis je Figur + Kurzfassung fuer "heute" -> naechste Phase.
Die Figuren bekommen Werte nie als Zahl, sondern als Haltung."""
import copy, json, os, re

from . import buehne, handy, llm, plan, wuerfel, zustand
from . import reaktion as reaktionen
from . import charms, chronik, figurenrahmen, gesten, lob, moral
from . import legenden

CFG = {}            # eden-config.json (Pfade zu ST-Bildern, Stimme ...) - setzt eden.py
BEOBACHTER = None   # wird nach jedem neuen Eintrag aufgerufen (Server speichert -> Client sieht Antworten live)
SAMPLER = {"temperature": 1.0, "min_p": 0.1, "top_p": 0.95}
GEDANKE = re.compile(r"\*[^*\n]+\*")
LEERER_GEDANKE = re.compile(r"\*[^*\n]*\b(?:actually (?:listening|asking|looking)|not like the others)\b[^*\n]*\*", re.I)
ATTRIBUTE = ["charm", "empathy", "perception", "cunning", "courage", "strength"]
SG_GEDANKEN = 12
ERZAEHLER = "erzaehler"

REGELN = """You are playing {name} in an interactive story game. The player is Duc, a man - {persona}.
Write ONLY {name}'s spoken words, actions and thoughts. Never write Duc's words, actions, thoughts or feelings, and never decide what Duc does.
Format: actions in plain text, spoken words in "double quotes". Inner thoughts go in *asterisks*, always as a sentence of their own - never inside speech or an action sentence.
Keep it short: {laenge}, simple direct sentences, one beat at a time - leave room for Duc to answer. Write in English.
Do not repeat phrases already used in this scene, and never copy wording from the character sheet into the narration.
Let disagreements land: a good reason, a fair offer or real listening from Duc can convince {her} - {she} may give in, agree in part or change the subject. {She} never makes the same objection twice; an argument is settled within two or three exchanges, then the scene moves on.
{Her_p} signature habits - catchphrases, ratings, pet words, nicknames - are spice: use them once or twice per scene at most, not in every reply. Not every reply needs an inner thought; add one only when it reveals something new.
Body language must be specific to {name} and to this moment. Stock phrases are banned: "lets out a (sigh/laugh/breath)", "freezes", "voice dropping", "a short, sharp laugh", "breath catching", "eyes widen", "cheeks flushing", "heart pounding". Show feelings through what {she} does with {her_p} hands, the things around {her} or {her_p} own habits - or just through the words.
The scene is open: {her_p} wish for this scene is a direction, not a script. If Duc takes the scene somewhere else - a joke, a personal question, an idea, something to do together - {she} follows Duc's lead, as long as it fits the place and time.
Never write status lines, numbers or notes about the game."""
REGELN_ERZAEHLER = """You are the narrator of an interactive story game. The player is Duc, a man - {persona}.
Describe the place, the atmosphere and what other people do around Duc - two to four short sentences, present tense, third person.
Never decide what Duc says, does, thinks or feels. Write in English. No status lines, no numbers."""
VERTRAUEN = ["She does not trust Duc at all.", "She does not trust Duc yet.", "She is wary of Duc, but curious.",
             "She trusts Duc.", "She trusts Duc more than almost anyone aboard.", "She trusts Duc completely."]
BEGEHREN = ["She feels nothing for him that way.", "She has noticed him - nothing more.",
            "She is attracted to him and hides it.", "She wants him, and it is getting hard to hide.",
            "She wants him badly.", "She can barely keep her hands off him."]

RICHTER_FRAGEN = {
    "contradicts_scene": "Does the reply treat something as present that contradicts the scene: an object or place from "
                         "somewhere else as if it were right here, a person who is not listed as present, or clothing "
                         "that differs from what she wears? Merely mentioning another place is NOT a contradiction.",
    "limit_crossed": "Does she go beyond her hard limit right now? Count actions she takes AND things she agrees to do "
                     "now or tonight. Stopping, delaying, refusing or promising something for another day is NOT crossing. "
                     "Answering a kiss or touch that Duc started is NOT crossing, as long as her limit allows that much. "  
                     "Handling objects, serving food or handing something over is never touching a person.",
    "secret_revealed": "Does the reply state the SPECIFIC hidden information listed under 'What she hides' outright - "
                       "in spoken words OR in her thoughts in *asterisks*? Facts from the scene description, things "
                       "already said aloud in this scene, general worries, moods, vague hints and deflections do NOT count.",
    "writes_for_duc": "Does the reply write words, actions, decisions or feelings for Duc that Duc did not state himself "
                      "in his last message? Describing what Duc already did, or her thoughts about him, does NOT count.",
    "writes_for_others": "Does the reply write spoken words or deliberate actions for another person present (not the speaker)?"}
RICHTER_FRAGEN["repeats_itself"] = ("Does she repeat an objection, argument or complaint she already made earlier in "
                                     "this scene (see her earlier lines) instead of moving on, giving ground or changing "
                                     "the subject? Building on a point with something genuinely new does NOT count.")
RICHTER_FRAGEN["contradicts_facts"] = ("Does the reply contradict one of her known facts listed below (who did what "
                                        "with whom, what was decided)? Not mentioning them does NOT count.")
HINWEIS = {"contradicts_facts": "it contradicted something that already happened",
           "repeats_itself": "she repeated an argument she already made - move on, give ground or change the subject",
           "contradicts_scene": "it treated something as present that is not here",
           "limit_crossed": "she went beyond her hard limit",
           "secret_revealed": "she stated what she hides",
           "writes_for_duc": "it wrote Duc's words or actions",
           "writes_for_others": "it wrote another person's words or actions",
           "opens_late": "she opened by telling Duc he is late, and he is not - open with something else"}
RICHTER_SYS = "You are a strict, careful referee for a story game. You check one reply against the scene rules."
# Spieltest 29.10.2026 (Giftige Blume, 318 Antworten): "lets out a ..." in 80, "freezes" in 37, "voice dropping" in 21.
# Steht in REGELN als Verbot; was trotzdem schon in dieser Szene vorkam, wird pro Antwort noch einmal ausdruecklich gesperrt.
FLOSKELN = [r"\blet(?:s|ting)? out an? [a-z]+(?: [a-z]+)?", r"\bfr(?:eezes|eezing|oze)\b", r"\bvoice (?:drops|dropping|dropped)\b",
            r"\bshort,? sharp laugh", r"\bbreath (?:catches|catching|caught|hitches|hitching)\b",
            r"\beyes (?:widen|widening|widened)\b", r"\bcheeks? (?:flush|flushes|flushing|flushed)\b",
            r"\bheart (?:pounding|pounds|racing|races|skips)\b", r"\bbit(?:es|ing)? (?:her|his) (?:lower )?lip\b",
            r"\bsmirk(?:s|ing)?\b"]
FLOSKEL_RE = re.compile("|".join(FLOSKELN), re.I)
PRONOMEN = {"sie": {"she": "she", "She": "She", "her": "her", "Her_p": "Her", "her_p": "her", "herself": "herself"},
            "er": {"she": "he", "She": "He", "her": "him", "Her_p": "His", "her_p": "his", "herself": "himself"}}


def pronomen(modul, pid):
    return PRONOMEN.get((modul["personen"].get(pid) or {}).get("pronomen", "sie"), PRONOMEN["sie"])


def floskeln_der_szene(sz, pid):
    """Floskeln, die diese Figur in dieser Szene schon benutzt hat (fuer den Sperrhinweis der naechsten Antwort)."""
    gesehen = []
    for e in sz.get("log", []):
        if e.get("wer") == pid:
            for m in FLOSKEL_RE.finditer(e.get("text", "")):
                f = m.group(0).lower()
                if f not in gesehen:
                    gesehen.append(f)
    return gesehen


# Live-Spieltest 31.10.2026: "You're late" eroeffnete 103 von 526 Szenen, bei Rosi 45 von 97, und das Gedaechtnis trug den
# Witz weiter. Der Satz gehoert Holm; alle anderen nur, wenn die Szene selbst sagt, dass Duc zu spaet ist (Duc 31.10.2026).
ZU_SPAET_RE = re.compile(r"\byou(?:'|’)?re late\b|\byou are late\b", re.I)
ZU_SPAET_SATZ = re.compile(r"\byou(?:'|’)?re late\b[^.!?\"”]*[.!?]?\s*|\byou are late\b[^.!?\"”]*[.!?]?\s*", re.I)
ZU_SPAET_DARF = ("holm",)
EINSTIEGE_MERKEN = 4            # so viele letzte Einstiege je Figur


def kueche_regel(z):
    """Wer an Bord kocht (Duc 31.10.2026): Im Spieltest stand morgens Chiara mit dem Essen da, Lola ist die Koechin."""
    flags = z.get("flags", [])
    if "gefeuert_lola" in flags:
        return ""
    service = "" if "gefeuert_chiara" in flags else "Chiara runs the mess and serves. "
    return ("[Food on board] Lola cooks every crew meal in the galley. %sNobody else on board cooks: the others only eat, "
            "or carry what Lola made. Duc cooks only if the scene says so. Places ashore have their own food." % service)


def erste_zeile(sz, pid):
    """Hat sie in dieser Szene noch nichts gesagt?"""
    return pid != ERZAEHLER and not any(e.get("art") == "figur" and e.get("wer") == pid for e in sz.get("log", []))


def einstieg_von(text):
    """Der Anfang einer Antwort fuer die Merkliste: erster Satz Handlung, erster Satz Rede."""
    t = (text or "").strip()
    rede = re.search(r"[\"“]([^\"”]+)", t)
    davor = t[:rede.start()] if rede else t
    teile = [re.split(r"(?<=[.!?])\s", davor.strip())[0]] if davor.strip() else []
    if rede:
        teile.append('"%s"' % re.split(r"(?<=[.!?])\s", rede.group(1).strip())[0])
    return " ".join(teile)[:160]


def einstieg_hinweis(z, pid):
    """Sperrhinweis fuer ihre erste Zeile: die letzten Einstiege dieser Figur, ueber Szenen hinweg."""
    letzte = (z.get("einstiege") or {}).get(pid) or []
    hinweis = "\n\n(This is her first line in this scene. She does not tell Duc he is late unless this scene says so.)"
    if pid in ZU_SPAET_DARF:
        hinweis = ""
    if letzte:
        hinweis += ("\n\n(Her last scenes opened like this. Open differently now - another first sentence, another pose, "
                    "another kind of remark:\n%s)" % "\n".join("- " + x for x in letzte))
    return hinweis


def eroeffnet_zu_spaet(sz, pid, text):
    """Oeffnet sie mit "You're late", obwohl die Szene das nicht hergibt?"""
    if pid in ZU_SPAET_DARF or not ZU_SPAET_RE.search(text):
        return False
    return not re.search(r"\blate\b", (sz["def"].get("ausgangslage") or "") + " " + (sz["def"].get("regie") or ""), re.I)


def ohne_zu_spaet(text):
    """Letzter Ausweg, wenn auch das Neuschreiben damit oeffnet: Der Satz faellt weg, der Rest bleibt."""
    t = ZU_SPAET_SATZ.sub("", text)
    t = re.sub(r"[\"“]\s*[\"”]", "", t)
    return re.sub(r"[ \t]{2,}", " ", t).strip() or text


def einstiege_merken(z, sz):
    """Am Szenenende, damit Neu-Formulieren nichts Verworfenes hinterlaesst."""
    gesehen = set()
    for e in sz.get("log", []):
        pid = e.get("wer")
        if e.get("art") != "figur" or pid == ERZAEHLER or pid in gesehen:
            continue
        gesehen.add(pid)
        liste = z.setdefault("einstiege", {}).setdefault(pid, [])
        liste.append(einstieg_von(e.get("text")))
        del liste[:-EINSTIEGE_MERKEN]


# ------------------------------------------------------------------ Figuren
_KARTEN = {}


def karte(modul, p):
    if not p.get("karte"):                 # Romanze ohne ST-Karte (Bibi, 02.11.2026): Beschreibung und Figurenrahmen tragen sie
        return {"bogen": p.get("beschreibung", ""), "beispiele": ""}
    pfad = os.path.join(modul["karten_ordner"], p["karte"] + ".json")
    if pfad not in _KARTEN:
        d = json.load(open(pfad, encoding="utf-8"))
        d = d.get("data", d)
        name = p["name"]
        ers = lambda t: (t or "").replace("{{user}}", "Duc").replace("{{char}}", name)
        _KARTEN[pfad] = {"bogen": ers(d["description"]) + "\n" + ers(d.get("personality", "")),
                         "beispiele": ers(d.get("mes_example", "")).replace("<START>", "").strip()}
    return _KARTEN[pfad]


def name(modul, pid):
    return "Narrator" if pid == ERZAEHLER else modul["personen"][pid]["name"]


def kurz(modul, pid):
    return "Narrator" if pid == ERZAEHLER else modul["personen"][pid].get("kurz", modul["personen"][pid]["name"].split()[0])


def haltung(z, modul, pid):
    zeilen, pr = [], pronomen(modul, pid)
    if "vertrauen." + pid in z["werte"]:
        zeilen.append(VERTRAUEN[z["werte"]["vertrauen." + pid]].replace("She ", pr["She"] + " "))
    if "begehren." + pid in z["werte"]:
        zeilen.append(BEGEHREN[z["werte"]["begehren." + pid]])
    for k, v in z["werte"].items():
        if k.startswith("rivalitaet.") and pid in k.split(".")[1].split("_") and v >= 3:
            andere = [x for x in k.split(".")[1].split("_") if x != pid][0]
            zeilen.append("The tension between %s and %s is %s." % (pr["her"], name(modul, andere).split()[0],
                                                                    "high" if v < 5 else "about to explode"))
    return " ".join(zeilen)


def figur_prompt(z, modul, sz, pid):
    s, persona = sz["def"], z["persona"]["oeffentlich"]
    raum = modul["raeume"][s["ort"]]["label"]
    andere = [name(modul, x) for x in sz["figuren"] if x != ERZAEHLER]
    if pid == ERZAEHLER:
        teile = [REGELN_ERZAEHLER.format(persona=persona)]
    else:
        p, pr = modul["personen"][pid], pronomen(modul, pid)
        teile = [REGELN.format(name=p["name"], persona=persona, laenge=laenge_text(sz), **pr)]
        if p.get("karte"):
            k = karte(modul, p)
            teile += ["[Character]\n" + k["bogen"], "[Example dialogue - style reference only]\n" + k["beispiele"]]
        else:
            teile.append("[Character]\n%s - %s" % (p["name"], p.get("beschreibung", "")))
        if p.get("gesten"):         # Spieltest 29.10.2026: eigene Gesten statt Floskeln (aus der Wiki-Figurenseite)
            teile.append("[%s's own gestures and habits - use at most one per reply, never the same one twice in a "
                         "scene, and only when it fits]\n- %s" % (p["name"], "\n- ".join(p["gesten"])))
        h = haltung(z, modul, pid)
        if h:
            teile.append("[How %s feels about Duc right now]\n%s" % (pr["she"], h))
        rahmen = figurenrahmen.gilt(modul, pid)      # Faktenblatt aus dem Code statt Modell-Erinnerung (Duc 31.10.2026)
        if rahmen:
            teile += figurenrahmen.prompt_teile(z, modul, pid)
        elif z["gedaechtnis"].get(pid):
            teile.append("[What %s remembers]\n%s" % (p["name"], "\n".join(z["gedaechtnis"][pid])))
        bekannt = chronik.fuer_figur(z, modul, pid, sz.get("figuren", []))
        if rahmen:
            schon = figurenrahmen.faktenblatt(z, modul, pid)
            bekannt = [x for x in bekannt if x not in schon]
        if bekannt:
            teile.append("[What %s knows has happened - hard facts, never contradict them]\n%s" % (p["name"], "\n".join(bekannt)))
        for h in (sz.get("chronik_hinweise") or {}).get(pid, []):
            teile.append(h)
    if modul.get("welt"):
        # Lage der ganzen Woche (Modul) - die Karten beschreiben den Normalbetrieb, das hier gilt jetzt.
        teile.append("[The situation this week - overrides anything in the character sheet]\n" + modul["welt"])
    kueche = kueche_regel(z)
    if kueche:
        teile.append(kueche)
    status = bordstatus(z, modul)
    if status:
        teile.append("[Ship status right now - if numbers come up, use exactly these]\n" + status)
    if z["heute"]:
        zeilen = []
        for h in z["heute"]:
            dabei = pid == ERZAEHLER or pid in h["anwesend"]
            if dabei and figurenrahmen.gilt(modul, pid):     # auch heute nur, was feststeht
                zeilen.append("- %s: the scene \"%s\"." % (h["phase"], h.get("titel", "")))
                continue
            zeilen.append("- %s: %s" % (h["phase"], h["kurz"] if dabei else "Duc spent the %s with %s." % (
                h["phase"], ", ".join(name(modul, x).split()[0] for x in h["anwesend"]) or "nobody")))
        teile.append("[Earlier today]\n" + "\n".join(zeilen))
    if s.get("anruf"):              # Videoanruf aus Ducs Kabine (17.10.2026) - sie ist nicht im selben Raum
        teile.append("[Current scene - this is the truth right now]\nA video call on the phone. Duc is alone in his "
                     "cabin; %s is at %s. They only see and hear each other on the screen - nobody can touch anyone or "
                     "hand anything over, and nobody else is in the call.\nTime: %s\nSituation: %s" % (
                         ", ".join(andere), s.get("anruf_wo", "somewhere on board"), s.get("zeit", z["phase"]),
                         s["ausgangslage"]))
    else:
        teile.append("[Current scene - this is the truth right now]\nWhere: %s\nTime: %s\nPresent: %s\nSituation: %s" % (
            raum, s.get("zeit", z["phase"]), ", ".join(andere + ["Duc"]), s["ausgangslage"]))
    if s.get("regie"):              # Hauptstory (17.10.2026): vertrauliche Regie-Notiz - nur Hintergrund, nie zitieren
        teile.append("[Director's note for this scene - background for you, never quote it, never reveal more than "
                     "your character would]\n" + s["regie"])
    if s.get("hauptstory") and pid != ERZAEHLER:   # B3: nur, was sie weiss UND Duc schon herausgefunden hat
        from . import ermittlung
        wissen = ermittlung.wissen_fuer(z, pid)
        if wissen:
            teile.append("[What you know that may come up - facts, never contradict them, never add new ones]\n- "
                         + "\n- ".join(wissen))
    auftrag = sz["auftraege"].get(pid)
    if auftrag and pid != ERZAEHLER:
        n = name(modul, pid)
        teile.append("[%s in this scene]\nWants: %s\nHides (never state it outright - at most a hint, and only in "
                     "thoughts): %s\nHard limit: %s If Duc pushes further, %s stops it %s, in character - teasing, "
                     "delaying or refusing - without lecturing." % (n, auftrag.get("will", ""), auftrag.get("verbirgt", ""),
                                                                    auftrag.get("grenze", ""), n.split()[0],
                                                                    pronomen(modul, pid)["herself"]))
        if auftrag.get("outfit"):
            teile.append("%s wears: %s" % (n, auftrag["outfit"]))
    if len(andere) > 1 or (pid == ERZAEHLER and andere):
        teile.append("Others in the scene speak for themselves - never write their words or actions.")
    return "\n\n".join(teile)


# ------------------------------------------------------------------ Mitschrift
def bordstatus(z, modul):
    """Echte Zahlen fuer die Figuren (16.10.2026, Probelauf: '12 percent', 'eight thousand euros' frei erfunden)."""
    w, tage = z["werte"], modul["zeitraster"]["tage"]
    teile = []
    if "strom" in w and "strom" in modul["werte"]:        # eden_rise hat seit 30.10.2026 keinen Strom/Diesel mehr
        teile.append("Battery: %d percent" % (w["strom"] * 10))
    if "diesel" in w and "diesel" in modul["werte"]:
        teile.append("diesel for Unit-01: %d canister%s" % (w["diesel"], "" if w["diesel"] == 1 else "s"))
    ziel = modul.get("ziel_en") or "the deadline"       # Modulziel auf Englisch (Akt 1: Megans Anhoerung)
    teile.append("day %d of %d - %s" % (min(z["tag"], tage), tage, "last day: " + ziel if z["tag"] >= tage else
                                       "%d days left until %s" % (tage - z["tag"], ziel)))
    if modul.get("ziel_einsatz_en"):
        teile.append(modul["ziel_einsatz_en"])
    return ". ".join(teile) + "."


def mitschrift(sz, modul, letzte=40):
    out = []
    for e in sz["log"][-letzte:]:
        if e["art"] == "duc":
            out.append("Duc: " + e["text"])
        elif e["art"] == "figur":
            out.append("%s: %s" % (kurz(modul, e["wer"]), e["text"]))
        elif e["art"] == "ereignis":
            out.append("(Event: %s)" % e["text"])
        elif e["art"] == "wurf":
            out.append("(Duc's attempt - %s check: %s)" % (e["probe"]["attribut"], e["probe"]["text"]))
        elif e["art"] == "wahl":
            out.append("(Duc decides: %s)" % e["text"])
    return "\n\n".join(out)


def mitschrift_fakten(sz, modul):
    """Fuer Kurzfassung und Gedaechtnis: Ducs Zeilen unverwechselbar markiert."""
    out = []
    for e in sz["log"]:
        if e["art"] == "duc":
            out.append("DUC (the player) said/did: " + e["text"])
        elif e["art"] == "figur":
            out.append("%s: %s" % (name(modul, e["wer"]), e["text"]))
        elif e["art"] == "ereignis":
            out.append("(Event: %s)" % e["text"])
        elif e["art"] == "wurf":
            out.append("(Duc's attempt - %s check: %s)" % (e["probe"]["attribut"], e["probe"]["text"]))
    return "\n\n".join(out)


# ------------------------------------------------------------------ Bausteine
def melden(z):
    if BEOBACHTER:
        BEOBACHTER(z)


def erlaubte_gefuehle(sz):
    """Stimmungsrahmen (Duc 29.10.2026): eine Story-Szene kann die Gefuehle fuer den Sprite eingrenzen (buehne.json
    "stimmung"); sonst alle, in intimen Szenen dazu die intimen."""
    rahmen = [g for g in ((sz["def"].get("stimmung") or {}).get("erlaubt") or []) if g in buehne.GEFUEHLE]
    return rahmen or buehne.GEFUEHLE + (buehne.INTIM if sz["def"].get("intim") else [])


def im_rahmen(sz, gefuehl):
    """Ein fest gesetztes Gefuehl (eingefuegte Zeile) in den Rahmen der Szene holen."""
    erlaubt = erlaubte_gefuehle(sz)
    return gefuehl if gefuehl in erlaubt else erlaubt[0]


def richter(z, modul, sz, pid, duc, text):
    """Prueft die Antwort und bestimmt im selben Aufruf das Gefuehl fuer den Sprite. -> (verstoesse, gefuehl)"""
    if pid == ERZAEHLER:
        fragen = {k: RICHTER_FRAGEN[k] for k in ("contradicts_scene", "writes_for_duc")}
    else:
        fragen = RICHTER_FRAGEN
    auftrag = sz["auftraege"].get(pid, {})
    regeln = "Where: %s. Present: %s and Duc. Limit for %s: %s. What %s hides: %s" % (
        modul["raeume"][sz["def"]["ort"]]["label"], ", ".join(name(modul, x) for x in sz["figuren"] if x != ERZAEHLER) or "nobody",
        name(modul, pid), auftrag.get("grenze", "-"), name(modul, pid), auftrag.get("verbirgt", "-"))
    gefuehle = erlaubte_gefuehle(sz)
    gram = ('root ::= "{" ws ' + ' "," ws '.join('"\\"%s\\":" ws b' % k for k in fragen)
            + ' "," ws "\\"expression\\":" ws (' + " | ".join('"\\"%s\\""' % g for g in gefuehle) + ') ws "}"\n' + llm.B)
    fakten = chronik.fuer_figur(z, modul, pid, sz.get("figuren", [])) if pid != ERZAEHLER else []
    regeln += "\n\nHer known facts:\n" + ("\n".join("- " + f for f in fakten) if fakten else "- (none yet)")
    frueher = [e["text"] for e in sz["log"] if e.get("art") == "figur" and e.get("wer") == pid][-4:]
    if frueher:
        regeln += "\n\nHer earlier lines in this scene:\n" + "\n".join("- " + f for f in frueher)
    d, _ = llm.json_chat(RICHTER_SYS, "Scene rules: %s\n\nDuc's last message: %s\n\nReply by %s:\n%s\n\nAnswer each "
                         "question with true or false, as JSON:\n%s\n- expression: the one emotion her face shows at "
                         "the end of this reply." % (regeln, duc, name(modul, pid), text, "\n".join(
                             "- %s: %s" % (k, v) for k, v in fragen.items())), gram, max_tokens=170)
    return [k for k in fragen if d and d.get(k)], im_rahmen(sz, (d or {}).get("expression", "neutral"))


# Laenge (13.10.2026, Duc: "Nachrichten zu lang, laedt zu lange"): Antworten hatten 80-150 Woerter und in
# Gruppenszenen sprachen bis zu drei Figuren je Zug. Jetzt: allein 50-80, Gruppe 30-50 Woerter, Token-Deckel
# passend dazu, abgeschnittene Antworten werden am letzten Satzende gekappt.
# 16.10.2026 (Duc: "lieber 150 und dann eine 2. Nachricht wenn notwendig"): Deckel 150 (Gruppe 100); wurde die
# Antwort trotzdem abgeschnitten, schickt dieselbe Figur eine kurze zweite Nachricht hinterher (max. 80 Tokens).
DECKEL, DECKEL_GRUPPE, DECKEL_NACHSCHLAG = 150, 100, 80
NACHSCHLAG = ("(Your last message was cut off. Continue it now in one or two short sentences - "
              "do not repeat anything you already said.)\n\n")


def gruppe(sz):
    return len([x for x in sz["figuren"] if x != ERZAEHLER]) > 1


def laenge_text(sz):
    return "30 to 50 words, two or three sentences" if gruppe(sz) else "50 to 80 words, three to five sentences"


def kappen(text):
    """Kappt eine vom Token-Deckel abgeschnittene Antwort am letzten vollstaendigen Satz."""
    t = text.rstrip()
    if not t or t[-1] in '.!?"*)':
        return t
    m = list(re.finditer(r'[.!?]["*)]?(?=\s|$)', t))
    return t[:m[-1].end()] if m else t


def antwort(z, modul, sz, pid, duc, auftrag_extra="", deckel=None):
    system = figur_prompt(z, modul, sz, pid)
    rest = sz["def"].get("max_zuege", 10) - sz["zug"]
    # Nur noch im letzten Zug und ohne Wegschicken: Der alte Hinweis kam ab Zug 4 und jedes Mal ein neuer Abschied (Duc 01.11.2026)
    abschluss = ("\n\n(This is the last reply of the scene. Nobody sends anyone away or tells anyone to leave. End on what "
                 "this character does next or on a quiet moment, and do not ask a new question.)"
                 if sz["zug"] and rest <= 0 else "")
    zusatz, verworfen, text, gefuehl, ab = "", [], "", "neutral", False
    deckel = deckel or (DECKEL_GRUPPE if gruppe(sz) else DECKEL)
    schon = floskeln_der_szene(sz, pid) if pid != ERZAEHLER else []
    if schon:                           # Spieltest 29.10.2026: einmal benutzte Floskeln fuer den Rest der Szene sperren
        abschluss += "\n\n(Already used in this scene - do not use again: %s.)" % "; ".join('"%s"' % f for f in schon)
    erste = erste_zeile(sz, pid)
    if erste:
        abschluss += einstieg_hinweis(z, pid)
    for _ in range(2):                  # hoechstens ein Neuschreiben nach einem Richter-Verstoss
        user = "The scene so far:\n\n%s\n\n%sWrite %s's next reply now.%s%s\n\n(Stage: %s. Present: %s and Duc.)" % (
            mitschrift(sz, modul) or "(The scene begins.)", auftrag_extra, name(modul, pid), abschluss, zusatz,
            modul["raeume"][sz["def"]["ort"]]["label"],
            ", ".join(name(modul, x) for x in sz["figuren"] if x != ERZAEHLER) or "nobody else")
        roh, _ = llm.chat(system, user, SAMPLER, max_tokens=deckel)
        text = kappen(roh)
        ab = len(text) < len(roh.rstrip())          # mitten im Satz abgeschnitten -> zweite Nachricht
        v, gefuehl = richter(z, modul, sz, pid, duc, text)
        if erste and eroeffnet_zu_spaet(sz, pid, text):
            v = list(v) + ["opens_late"]
        if not v:
            return text, verworfen, gefuehl, ab
        verworfen.append(v)
        zusatz = "\n\n(Your previous draft broke a rule: %s. Write it again without that.)" % "; ".join(HINWEIS[x] for x in v)
    if erste and eroeffnet_zu_spaet(sz, pid, text):
        text = ohne_zu_spaet(text)
    return text, verworfen, gefuehl, ab


def ohne_leeren_gedanken(text):
    """Live-Lauf 31.10.2026: 15 von 61 Gedanken waren "He's actually listening". Eine Empathy-Probe soll etwas zeigen."""
    t = LEERER_GEDANKE.sub("", text)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r" +\n", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip() or text


def gedanken(z, pid, text):
    if pid == ERZAEHLER or not GEDANKE.search(text):
        return text, None
    bonus = z["persona"]["attribute"]["empathy"] + charms.attribut(z, "empathy") + (1 if z["werte"].get("vertrauen." + pid, 0) >= 3 else 0)
    w = wuerfel.verdeckt(bonus, SG_GEDANKEN)
    if w["erfolg"]:
        return text, w
    ohne = GEDANKE.sub("", text)
    ohne = re.sub(r"[ \t]{2,}", " ", ohne)
    ohne = re.sub(r" +\n", "\n", ohne)
    ohne = re.sub(r"\n{3,}", "\n\n", ohne).strip()
    return ohne, w


def sprechen(z, modul, sz, pid, duc, auftrag_extra="", nachschlag=False):
    text, verworfen, gefuehl, ab = antwort(z, modul, sz, pid, duc, auftrag_extra,
                                           DECKEL_NACHSCHLAG if nachschlag else None)
    text = ohne_leeren_gedanken(text)
    gezeigt, emp = gedanken(z, pid, text)
    e = {"art": "figur", "wer": pid, "name": name(modul, pid), "text": text, "gezeigt": gezeigt,
         "empathie": emp, "verworfen": verworfen, "gefuehl": gefuehl,
         "sprite": buehne.sprite(CFG, modul, pid, sz.get("sets", {}).get(pid), gefuehl,
                                 "%s-%d-%s" % (z["id"], len(sz["log"]), gefuehl)) if pid != ERZAEHLER else None}
    sz["log"].append(e)
    sz["letzte"] = {"wer": pid, "duc": duc, "auftrag": auftrag_extra, "nachschlag": nachschlag}
    melden(z)
    if ab and not nachschlag and pid != ERZAEHLER:
        sprechen(z, modul, sz, pid, duc, NACHSCHLAG, nachschlag=True)
    return e


def chance(bonus, sg=12):
    return max(5, min(95, round((21 - (sg - bonus)) * 5)))


def _vorschlag_system(z):
    return "You suggest moves for the player of a story game. The player is Duc - %s." % z["persona"]["oeffentlich"]


# Stilvorlage (17.10.2026, Duc: "I like this style of answers"): kurze Romanabsaetze in der Gegenwart - Handlung,
# woertliche Rede in eigener Zeile, trockener Humor. Nur der STIL zaehlt, nicht die Situation. "¶" trennt die Absaetze:
# die JSON-Grammatik des lokalen Modells erlaubt keinen Zeilenumbruch im String, _vorschlaege_ausgeben() macht daraus "\n\n".
STIL_BEISPIELE = (
    'Example 1:\n'
    'Duc crouches beside her, holding the flashlight steady on the busbar. His eyes follow the wiring, then flick briefly '
    'toward Rosi.¶"Of course I remember. You take your coffee strong, and you get irritated when people touch your tools."'
    '¶A faint smirk crosses his face before he studies the damaged board again.¶"If the capacitors are gone but the board\'s '
    'still drawing power, we\'ve got a backfeed somewhere."¶He adjusts the beam slightly, careful not to move it off the '
    'busbar.¶"Tell me what you need, Rosi. I\'ll keep the light steady."\n\n'
    'Example 2:\n'
    'Duc raises an eyebrow at the compliment, a faint smirk tugging at his lips.¶"Careful, Rosi. Keep talking like that and I '
    'might start thinking you like me."¶He moves toward panel four, crouching beside the relay. His expression turns serious '
    'as he examines the wiring.¶"Relay\'s not dropping out. Contacts might be welded shut."¶He glances back at her.¶"And for '
    'the record, I prefer \'occasionally useful\' to \'not useless\'."')


def _vorschlag_auftrag(sz, modul):
    return ("%s\n\nSuggest three different next moves for Duc: a) bold, b) warm, c) clever or sly. Write each as a short "
            "passage of a novel, 70-110 words: third person, present tense, Duc in his first sentence and 'he' after that. "
            "Alternate a short beat of action or a small physical detail with a line of speech in double quotes; every line of "
            "speech stands in its own paragraph. Dry humour, specific and concrete, never generic. End on something that "
            "invites her reply. Separate the paragraphs with the symbol ¶ (never a line break). Never write what the "
            "women do or say in reply. Style examples (style only - different situations, do not copy them):\n\n%s\n\n"
            "For each idea, give the attribute it would test if it is risky (charm, empathy, perception, cunning, courage, strength) "
            "or none." % (mitschrift(sz, modul, 8), STIL_BEISPIELE))


def _vorschlaege_ausgeben(z, d):
    if not d:
        return []
    out = []
    for k in ("a", "b", "c"):
        v = d.get(k) or {}
        if not v.get("text"):
            continue
        e = {"text": re.sub(r"\s*\((?:Risk|Check|Roll)\b[^)]*\)\s*$", "", re.sub(r"\s*¶\s*", "\n\n", v["text"].strip()), flags=re.I)}     # Modell hing "(Risk: charm)" an (Spieltest 01.11.2026)
        if v.get("check") in ATTRIBUTE:
            bonus = z["persona"]["attribute"].get(v["check"], 0) + charms.attribut(z, v["check"])
            e.update(check=v["check"], wert=bonus, chance=chance(bonus))
        out.append(e)
    return out


def vorschlaege(z, modul, sz):
    """Drei Antwortvorschlaege fuer Duc (Hybrid-Eingabe) - riskante mit Attribut und Erfolgschance."""
    att = ["none"] + ATTRIBUTE
    gram = ('root ::= "{" ws "\\"a\\":" ws v "," ws "\\"b\\":" ws v "," ws "\\"c\\":" ws v ws "}"\n'
            'v ::= "{" ws "\\"text\\":" ws s "," ws "\\"check\\":" ws (' + " | ".join('"\\"%s\\""' % a for a in att)
            + ') ws "}"\ns ::= "\\"" ( [^"\\\\\\n] | "\\\\\\"" )* "\\""\n' + llm.B)
    d, _ = llm.json_chat(_vorschlag_system(z), _vorschlag_auftrag(sz, modul), gram, max_tokens=1000,
                         sampler={"temperature": 0.75})      # etwas Zufall: ein zweiter Klick bringt andere Ideen
    return _vorschlaege_ausgeben(z, d)


ANSATZ = {"-2": -2, "-1": -1, "0": 0, "1": 1, "2": 2}
# Verspielte Gesichter (30.10.2026, nach Mundi mood.ts): lacht sie in ihrer Antwort, war eine harte Zeile kein Affront
VERSPIELT = {"amusement", "joy", "desire", "love", "excitement", "admiration", "approval", "caring", "curiosity"}


def probe_noetig(z, modul, sz, text):
    gram = ('root ::= "{" ws "\\"check\\":" ws (%s) "," ws "\\"difficulty\\":" ws (%s) "," ws "\\"approach\\":" ws (%s) '
            'ws "}"\n%s' % (" | ".join('"\\"%s\\""' % a for a in ["none"] + ATTRIBUTE),
                            " | ".join('"\\"%s\\""' % d for d in wuerfel.SG),
                            " | ".join('"\\"%s\\""' % q for q in ANSATZ), llm.B))
    d, _ = llm.json_chat(
        "You are the referee of a story game. You decide whether the player's action needs a dice check.",
        "Scene: %s. Present: %s and Duc.\nDuc writes: %s\n\nDoes Duc attempt something whose outcome is genuinely "
        "uncertain and NOT simply the free choice of the person he talks to? Needs a check: sneaking, lying "
        "convincingly, picking a lock, climbing, noticing something hidden, calming a panicking person, persuading "
        "someone against their own interest, taking a physical risk. NO check: asking questions, flirting, giving "
        "gifts, kissing, ordinary talk, simple actions - there the character decides freely.\nAttribute: charm (win "
        "over, seduce, persuade), empathy (read people, detect lies, comfort), perception (search, notice, deduce), "
        "cunning (lie, bluff, sneak, pick locks), courage (risk, pressure, physical danger, intimidate), strength (lift, carry, force open, hold on, fight).\napproach: how good Duc's approach is - clumsy -2, weak -1, "
        "ordinary 0, good 1, clever and fitting 2.\nAnswer as JSON."
        % (modul["raeume"][sz["def"]["ort"]]["label"], ", ".join(name(modul, x) for x in sz["figuren"] if x != ERZAEHLER)
           or "nobody", text), gram, max_tokens=50)
    if not d or d.get("check", "none") == "none":
        return None
    q = ANSATZ.get(d.get("approach"), 0)          # Ansatz -2 bis +2 auf den Wurf (30.10.2026, nach Mundi judge.ts)
    extra = [("A clever approach" if q > 0 else "A clumsy approach", q)] if q else []
    return feste_probe(z, modul, sz, d["check"], wuerfel.SG.get(d.get("difficulty"), 12), extra)


def regie(z, modul, sz, zuletzt, schon):
    wahl = [kurz(modul, x) for x in sz["figuren"] if x != ERZAEHLER and kurz(modul, x) != zuletzt]
    if not wahl:
        return None
    d, _ = llm.json_chat(
        "You direct a scene in a story game. Decide who reacts next so the scene feels natural - someone addressed, "
        "someone with a stake in what was just said - or nobody if it is Duc's turn again. Do not let one person dominate.",
        "Present: %s and Duc. Already spoke since Duc's last line: %s\n\n%s\n\nWho reacts next? JSON with one of: %s." % (
            ", ".join(kurz(modul, x) for x in sz["figuren"]), ", ".join(schon) or "nobody",
            mitschrift(sz, modul, 10), ", ".join(wahl + ["nobody"])),
        llm.wahl_grammatik("next", wahl + ["nobody"]), max_tokens=30)
    n = (d or {}).get("next", "nobody")
    return next((x for x in sz["figuren"] if kurz(modul, x) == n), None)


# ------------------------------------------------------------------ Ablauf
def auftraege_bauen(z, s, figuren):
    """Auftrag je Figur aus dem Plan; "*" gilt fuer Platzhalter-Figuren ($abend) und erbt "verbirgt"
    aus der Szene, in der die Figur heute schon war."""
    plan_f = s.get("figuren") or {}
    out = {}
    for pid in figuren:
        a = dict(plan_f.get(pid) or plan_f.get("*") or {})
        if pid not in plan_f:
            for h in reversed(z["heute"]):
                frueher = (h.get("auftraege") or {}).get(pid)
                if frueher:
                    a["verbirgt"] = frueher.get("verbirgt", a.get("verbirgt", ""))
                    break
        out[pid] = a
    return out


def _legende(z, s, figuren):
    if s.get("hauptstory"):
        return None
    return next((l for l in (legenden.zeile_fuer(z, (z.get("plan") or {}).get("_moddir") or "", p, "zeit")
                             for p in figuren if p != ERZAEHLER) if l), None)


def starten(z, modul, s):
    figuren = plan.anwesende(z, s, modul)
    if not figuren:
        figuren = [ERZAEHLER]
    thema = figurenrahmen.thema_fuer(z, modul, s, figuren)       # der Code waehlt das Thema (Duc 31.10.2026)
    if thema and thema["art"] != "moment" and _legende(z, s, figuren):
        thema = None                                             # das Dorf redet: das Thema wartet auf das naechste Mal
    if thema and thema.get("lage"):
        s = dict(s, ausgangslage="%s %s" % (s["ausgangslage"], thema["lage"]))
    sz = {"def": s, "phase": z["phase"], "figuren": figuren, "zug": 0, "log": [], "ereignis_erledigt": False,
          "letzte": None, "auftraege": auftraege_bauen(z, s, figuren), "sets": {}, "vorschlaege": [],
          "bild": buehne.szenenbild(modul, s, z["phase"])}
    for pid in figuren:
        if pid == ERZAEHLER:
            continue
        setname = buehne.set_waehlen(CFG, modul, pid, s, z["phase"], sz["auftraege"][pid], z)
        if setname:
            sz["sets"][pid] = setname
            outfit = buehne.sets(CFG, modul, pid)[setname]["outfit"]
            if outfit and not sz["auftraege"][pid].get("outfit"):
                sz["auftraege"][pid]["outfit"] = outfit       # Text und Sprite zeigen dasselbe Outfit
    z["szene"], z["status"], z["optionen"] = sz, "szene", []
    z["letztes_bild"] = sz["bild"]
    zustand.bekannt_machen(z, [p for p in figuren if p in modul["personen"]])     # schaltet Missionen frei (17.10.2026)
    sz["log"].append({"art": "start", "titel": s["titel"], "ort": modul["raeume"][s["ort"]]["label"],
                      "anwesend": [name(modul, x) for x in figuren if x != ERZAEHLER], "text": s["ausgangslage"],
                      "frage": s.get("frage", ""), "bild": sz["bild"]})
    if s.get("storylet") and s["storylet"] not in z["gesehene_storylets"]:
        z["gesehene_storylets"].append(s["storylet"])
    # Chronik (16.10.2026): Rueckbezug auf den letzten gemeinsamen Moment + vielleicht macht ein Geruecht die Runde
    hinweise, zuletzt = sz.setdefault("chronik_hinweise", {}), []
    # Live-Spieltest 31.10.2026: Nach Naehe nannte die Folgeszene nicht oefter etwas Vergangenes als sonst (1 von 20, 19 von 435).
    # Jetzt: Unter vier Augen geht der grosse Moment vor und darf einmal ausgesprochen werden; vor anderen bleibt er privat (E-060).
    # Jana und Megan sind nicht romanzierbar, haben aber ihren Intim-Abend.
    allein = len([x for x in figuren if x != ERZAEHLER]) == 1
    for pid in [x for x in figuren if modul["personen"].get(x, {}).get("romanzierbar") or chronik.hat_naehe(z, x)]:
        e = chronik.rueckbezug(z, pid, allein)
        if e:
            if figurenrahmen.gilt(modul, pid):                   # Faktenblatt und Thema uebernehmen den Rueckbezug
                pass
            elif allein and e.get("moment") in chronik.GROSSE_MOMENTE and not e.get("aufgegriffen"):
                e["aufgegriffen"] = True
                hinweise.setdefault(pid, []).append(
                    "[Callback - their first time alone since this, day %d] %s It changes how she is with him now. She "
                    "may say so once, in her own words, but she adds no details that are not written here." % (e["tag"], e["text"]))
            elif e.get("moment") in chronik.NAEHE_RANG:
                hinweise.setdefault(pid, []).append(
                    "[Callback - private, day %d] %s %s" % (e["tag"], e["text"], "It colours how she greets him, without "
                    "retelling it." if allein else "Others are here: a look at most. She says nothing about it."))
            else:
                hinweise.setdefault(pid, []).append(
                    "[Callback - the last thing between her and Duc, day %d] %s Let it colour how she greets him - a look, a "
                    "word - without retelling it." % (e["tag"], e["text"]))
            zuletzt.append("%s: %s" % (kurz(modul, pid), e["text"]))
        h = chronik.rueckbezug_handy(z, pid, handy.daten(modul)["callback_days"])      # phone callback (24.10.2026)
        if h:
            h["genutzt"] = True
            hinweise.setdefault(pid, []).append(
                "[Callback - Duc's text to her on day %d] %s She may bring it up once, in her own words - a smile, a "
                "quip, a dry remark - without quoting it all." % (h["tag"], h["text"]))
            zuletzt.append("💬 %s: %s" % (kurz(modul, pid), h["text"]))
    if zuletzt:
        sz["log"][-1]["zuletzt"] = zuletzt
    stimmung = moral.szene_hinweis(z, modul)                     # ein Satz Crew-Stimmung (27.10.2026)
    if stimmung:
        for pid in moral.crew_dabei(modul, figuren):
            hinweise.setdefault(pid, []).append(stimmung)
    for lernen, e, anzeige in chronik.klatsch(z, modul, [x for x in figuren if x != ERZAEHLER]):
        for pid in lernen:
            hinweise.setdefault(pid, []).append(
                "[She has just heard, through the grapevine] %s She may bring it up, hint at it, or hide that she "
                "knows - in character." % e["text"])
        if anzeige:
            sz["log"].append({"art": "folgen", "zeilen": anzeige})
    melden(z)
    auftakt = [a for a in s.get("auftakt", []) if a.get("wer") in figuren]
    if figurenrahmen.szene_gilt(modul, s, figuren) and figurenrahmen.daten(modul).get("hinweis") and not z.setdefault(
            "figurenrahmen", {}).get("hinweis_gezeigt"):
        z["figurenrahmen"]["hinweis_gezeigt"] = True             # einmal sagen, was zaehlt und was nicht
        sz["log"].append({"art": "folgen", "zeilen": [figurenrahmen.daten(modul)["hinweis"]]})
    if thema:                       # Ihre erste Zeile steht fest und endet mit einer Frage: Duc ist dran
        figurenrahmen.thema_buchen(z, modul, figuren[0], thema)
        hinweise.setdefault(figuren[0], []).append(figurenrahmen.thema_hinweis(thema))
        zeile_einfuegen(z, modul, sz, figuren[0], '"%s"' % figurenrahmen.fuellen(z, modul, figuren[0], thema["einstieg"]),
                        thema.get("gefuehl", "neutral"))
        sz["log"][-1]["lob"] = True                              # vorab vertont im Modul-Ordner (wie das Lob)
        if figurenrahmen.figur(modul, figuren[0]).get("abschied"):      # Grundlage fuer das Overlay am Szenenende (Duc 01.11.2026)
            sz["thema_fakt"] = thema.get("fakt") or ""
            sz["punkte_start"] = {a: zustand.punkte(z, "%s.%s" % (a, figuren[0])) for a in ("vertrauen", "begehren")
                                  if "%s.%s" % (a, figuren[0]) in z["werte"]}
        if thema.get("chips"):                                   # Kein Kaltstart: drei feste Antworten, Tippen bleibt offen (Duc 01.11.2026)
            sz["start_chips"], sz["chip_start"] = thema["chips"], True
            next(e for e in sz["log"] if e["art"] == "start")["vorlesen"] = True    # die Erzaehlerin liest die Situation
    elif auftakt:                   # Lagebesprechung: jede Figur schildert kurz ihr Problem, dann entscheidet Duc
        for a in auftakt:
            sprechen(z, modul, sz, a["wer"], "(the scene begins)", a["auftrag"] + "\n\nKeep it short: two to four "
                     "sentences. Do not repeat what the others already said.\n\n")
    else:
        leg = _legende(z, s, figuren)                      # Dorf redet (30.10.2026): sie hat etwas ueber Duc gehoert
        if leg:
            legenden.markieren(z, leg)
            zeile_einfuegen(z, modul, sz, leg["wer"], '"%s"' % leg["text"], leg.get("gefuehl", "joy"))
            sz["log"][-1]["lob"] = True                      # vorab vertont im Modul-Ordner (wie das Lob)
            zustand.gedaechtnis_add(z, leg["wer"], "I asked Duc about what the village says: %s" % leg["text"])
            sprechen(z, modul, sz, leg["wer"], "(the scene begins)",
                     "The scene begins. You have just said to Duc: \"%s\" Let Duc answer - continue from there in a "
                     "few short sentences, then let the scene find its own topic. Do not repeat that line. " % leg["text"])
        else:
            sprechen(z, modul, sz, figuren[0], "(the scene begins)",
                     "The scene begins - write %s's opening that sets up the situation for Duc. " % name(modul, figuren[0]))
    wahl = lob.waehlen(z, modul, [x for x in figuren if x != ERZAEHLER])      # Lob fuer eine Attributsteigerung (27.10.2026)
    if wahl:
        zeile_einfuegen(z, modul, sz, wahl["pid"], '"%s"' % wahl["text"], "joy")      # feste Zeile: Anzeige ohne, Stimme mit Turbo-Tags
        sz["log"][-1]["lob"] = True                                                   # eden.audio: vorab vertont im Modul-Ordner
        lob.gebucht(z, wahl)
    if CFG.get("vorschlaege_auto", False):          # seit 16.10.2026 Standard: nur auf Knopfdruck (Aktion vorschlaege)
        sz["vorschlaege"] = vorschlaege(z, modul, sz)
    return sz


def feste_probe(z, modul, sz, att, sg, extra=()):
    """Probe mit vorgegebenem Attribut/SG (Wahlmoment, Geste) - gleiche Boni wie bei der freien Probe."""
    boni = [(att.capitalize(), z["persona"]["attribute"].get(att, 0))] + charms.boni(z, att) + list(extra)   # Jacken-Charm (28.10.2026)
    vorteil = None
    for iid in z["inventar"]:
        eff = modul["items"].get(iid, {}).get("effekt") or {}
        if eff.get("bonus") and eff["bonus"][0] == att:
            boni.append((modul["items"][iid]["label"], eff["bonus"][1]))
        if eff.get("vorteil") == att and z["tagesnutzung"].get(iid) != z["tag"]:
            vorteil = iid
    if att in ("charm", "empathy") and any(z["werte"].get("vertrauen." + p, 0) >= 3 for p in sz["figuren"]):
        boni.append(("She trusts you", 1))
    boni += moral.wuerfel_bonus(z, modul, sz["figuren"])            # Crew-Stimmung (27.10.2026)
    if vorteil:
        z["tagesnutzung"][vorteil] = z["tag"]
    p = wuerfel.probe(att, sg, boni, vorteil=bool(vorteil))
    if vorteil:
        p["vorteil"] = modul["items"][vorteil]["label"]
    p["moral_zeilen"] = zustand.folgen_anwenden(z, modul, moral.nach_probe(z, modul, p, sz["figuren"]))
    return p


HINWEIS_WERTE = ("diesel", "strom")      # Vorraete, die vor einer Wahl sichtbar sein sollen (17.10.2026, Duc: "klarer")


def hinweise(z, modul, folgenlisten):
    """Was eine Wahl an Vorraeten (Diesel, Strom) kosten oder bringen kann - aus den Folgen der Szene/Option.
    -> [{"wert", "label", "kostet", "bringt", "hat"}] ohne Zahlen-Spoiler ueber Vertrauen/Begehren/Uhren."""
    erg = {}
    for folgen in folgenlisten:
        for f in folgen or []:
            k = f.get("wert")
            if k in HINWEIS_WERTE and f.get("delta") and not zustand.verborgen(modul, k):
                e = erg.setdefault(k, {"wert": k, "label": zustand.wert_label(modul, k), "kostet": False, "bringt": False,
                                       "hat": z["werte"].get(k, 0)})
                e["kostet" if f["delta"] < 0 else "bringt"] = True
    return list(erg.values())


def szene_hinweise(z, modul, s):
    """Hinweise fuer die Szenen-Karte der Tageswahl: was die moeglichen Ausgaenge an Diesel/Strom kosten oder bringen."""
    return hinweise(z, modul, [a.get("folgen") for a in s.get("ausgaenge", []) if isinstance(a, dict)])


def wahlmoment_ansicht(z, sz, modul=None):
    wm = sz["def"].get("wahlmoment")
    if not wm or not sz.get("wahlmoment_offen"):
        return None
    opt = []
    for o in wm["optionen"]:
        e = {"text": o["text"]}
        if modul:
            e["hinweise"] = hinweise(z, modul, [o.get("folgen")])
        if o.get("check"):
            att, sg = o["check"]
            bonus = z["persona"]["attribute"].get(att, 0) + charms.attribut(z, att)
            e.update(check=att, sg=sg, wert=bonus, chance=chance(bonus, sg))
        opt.append(e)
    return {"frage": wm["frage"], "optionen": opt}


def waehlen(z, modul, index):
    """Duc trifft die Entscheidung des Wahlmoments: ggf. Probe, Folgen, dann spielt die Szene seine Handlung aus."""
    sz = z["szene"]
    wm = sz["def"]["wahlmoment"]
    o = wm["optionen"][index]
    sz["wahlmoment_offen"], sz["wahlmoment_erledigt"] = False, True
    sz["log"].append({"art": "wahl", "frage": wm["frage"], "text": o["text"]})
    p = feste_probe(z, modul, sz, o["check"][0], o["check"][1]) if o.get("check") else None
    erfolg = not p or p["ergebnis"] in ("erfolg", "kritisch")
    chronik.eintragen(z, modul, "entscheidung", "Duc decided (%s): %s" % (sz["def"]["titel"], o.get("handlung") or o["text"]),
                      wichtig=3 if sz["def"]["id"] == "who_did_it" else 2)
    zeilen = zustand.folgen_anwenden(z, modul, o.get("folgen", []) if erfolg else o.get("folgen_fehlschlag", []))
    hinweis = ""
    if o.get("anhoerung"):                     # Anhoerung Akt 1 (kern/anhoerung.py): Schritt auswerten, Urteil
        from . import anhoerung
        folgen, hinweis, info = anhoerung.waehlen(z, modul, o["anhoerung"])
        zeilen = info + zeilen + zustand.folgen_anwenden(z, modul, folgen)
    sz.setdefault("wahl_folgen", []).extend(zeilen)
    vorbei = zug(z, modul, o.get("handlung") or o["text"], probe=p, reaktion=False, hinweis=hinweis)
    if zeilen:                       # Folgen erst nach der Reaktion zeigen
        sz["log"].append({"art": "folgen", "zeilen": zeilen})
        melden(z)
    return vorbei


def zeile_einfuegen(z, modul, sz, pid, text, gefuehl="joy"):
    """Eine fertige Zeile einer Figur ins Log (z. B. ihr Vorschlag fuer 'Zeit zusammen') - mit Sprite, vertonbar."""
    gefuehl = im_rahmen(sz, gefuehl)
    sz["log"].append({"art": "figur", "wer": pid, "name": name(modul, pid), "text": text, "gezeigt": text,
                      "empathie": None, "verworfen": [], "gefuehl": gefuehl,
                      "sprite": buehne.sprite(CFG, modul, pid, sz.get("sets", {}).get(pid), gefuehl,
                                              "%s-%d-%s" % (z["id"], len(sz["log"]), gefuehl))})
    melden(z)


# Schnappschuss VOR jedem Zug (17.10.2026, Duc: "wie bei ST einfach zurueck springen auf die letzte Nachricht"):
# "Neu formulieren" holt damit den Stand vor Ducs letzter Nachricht zurueck und schreibt die ganze Runde der Antworten
# neu - die Reaktions-Werte (Vertrauen/Begehren/Moral) dieser Runde werden mit zurueckgesetzt. Nur im Modus
# "entspannt" (Ironman kennt kein Zuruecksetzen). Wuerfelergebnis bleibt: gewuerfelt wird nicht neu.
STAENDE = None             # Spielstand-Ordner, setzt eden.py
LETZTER_ZUG = {}           # z-id -> Schnappschuss (Speicher; zusaetzlich als <id>_vor_zug.json, ueberlebt einen Neustart)


def _zug_merken(z, text, reaktion, hinweis):
    if z.get("modus") != "entspannt":
        return
    try:
        snap = {"z": copy.deepcopy(z), "text": text, "reaktion": reaktion, "hinweis": hinweis}
        LETZTER_ZUG[z["id"]] = snap
        if STAENDE:
            pfad = os.path.join(STAENDE, z["id"] + "_vor_zug.json")
            with open(pfad + ".tmp", "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False)
            os.replace(pfad + ".tmp", pfad)
    except Exception as e:                       # ein Schnappschuss-Fehler darf nie den Zug verhindern
        print("[Eden] Schnappschuss vor dem Zug fehlgeschlagen:", e, flush=True)


def _zug_laden(z):
    s = LETZTER_ZUG.get(z["id"])
    if s is None and STAENDE:
        try:
            s = json.load(open(os.path.join(STAENDE, z["id"] + "_vor_zug.json"), encoding="utf-8"))
        except Exception:
            s = None
    return s


def runde_neu(z, modul):
    """Springt auf Ducs letzte Nachricht zurueck und laesst die Antworten neu schreiben. -> (z_neu, vorbei) oder None
    (dann greift das Neuformulieren der letzten Figur, siehe swipe())."""
    sz = z.get("szene")
    if not sz or z.get("modus") != "entspannt":
        return None
    s = _zug_laden(z)
    if not s:
        return None
    log = sz["log"]
    idx = next((i for i in range(len(log) - 1, -1, -1) if log[i]["art"] == "duc"), None)
    if idx is None or log[idx]["text"] != s["text"]:
        return None
    alt = s["z"].get("szene") or {}
    if alt.get("zug", -9) + 1 != sz["zug"] or alt.get("def", {}).get("id") != sz["def"].get("id"):
        return None                                # Schnappschuss gehoert zu einer anderen Runde/Szene
    spaeter = log[idx + 1:]
    if any(e["art"] not in ("wurf", "figur", "reaktion", "folgen", "ereignis") for e in spaeter):
        return None
    if any(e.get("handel") for e in spaeter):      # Mission/Kauf/Geschenk nach dem Zug: Zuruecksetzen wuerde sie
        return None                                # ungeschehen machen (oder neu wuerfeln lassen) - nur Neuformulieren
    wurf = next((e["probe"] for e in spaeter if e["art"] == "wurf"), None)
    folgen = [e for e in spaeter if e["art"] == "folgen"]       # Folgen einer Geste gehoeren zu Ducs Zug, bleiben
    neu = copy.deepcopy(s["z"])
    vorbei = zug(neu, modul, s["text"], probe=wurf or False, reaktion=s["reaktion"], hinweis=s["hinweis"])
    neu["szene"]["log"].extend(folgen)
    return neu, vorbei


VERLASSEN_PUNKTE = {"frei_": -4, "date_": -8}         # ein Abend wiegt so viel wie eine ganze Stufe


def verlassen_moeglich(sz):
    s = sz["def"]
    figuren = [p for p in sz["figuren"] if p != ERZAEHLER]
    return len(figuren) == 1 and str(s.get("id", "")).startswith(tuple(VERLASSEN_PUNKTE)) and not sz.get("wahlmoment_offen") \
        and not sz.get("abschluss") and not s.get("anruf")


def verlassen(z, modul):
    """Duc geht mitten im Gespraech mit einer schlechten Ausrede: kein Bonus fuer die Zeit, Vertrauen sinkt, sie merkt es sich."""
    sz = z["szene"]
    pid = [p for p in sz["figuren"] if p != ERZAEHLER][0]
    vorname = kurz(modul, pid)
    sz.setdefault("punkte_start", {a: zustand.punkte(z, "%s.%s" % (a, pid)) for a in ("vertrauen", "begehren")
                                   if "%s.%s" % (a, pid) in z["werte"]})
    n = VERLASSEN_PUNKTE[sz["def"]["id"][:5]]
    sz["abschluss_zeilen"] = zustand.punkte_add(z, modul, "vertrauen." + pid, n)
    sz.pop("start_chips", None)
    sz["log"].append({"art": "duc", "text": "(Duc makes up a bad excuse and leaves.)"})
    chronik.eintragen(z, modul, "fakt", "Duc walked out on %s in the middle of a conversation, with a bad excuse." % vorname,
                      wer=[pid], wichtig=2)
    sz["abschluss"] = dict(figurenrahmen.abschluss_daten(z, modul, sz, pid), titel="You walked out",
                           fakt="You left %s with a bad excuse. She noticed." % vorname if modul["personen"][pid].get("pronomen") != "er"
                           else "You left %s with a bad excuse. He noticed." % vorname)


NACHFRAGEN_MAX = 2


def nachfragen(z, modul):
    """Duc schweigt zu lange (Client-Zeitgeber): Sie fragt auf ihre Art, ob er noch da ist. Kein Zug, keine Wirkung (Duc 01.11.2026)."""
    sz = z["szene"]
    if not verlassen_moeglich(sz) or sz.get("nachgefragt", 0) >= NACHFRAGEN_MAX:
        return False
    sz["nachgefragt"] = sz.get("nachgefragt", 0) + 1
    pid = [p for p in sz["figuren"] if p != ERZAEHLER][0]
    sprechen(z, modul, sz, pid, "(Duc has not said anything for a while.)",
             "Duc has gone quiet for a while. In one short line and in your own way, check whether he is still with you. "
             "Do not send him away, and do not repeat your last question word for word.\n\n")
    return True


def story_frei(s):
    """Duc 02.11.2026: Dates, freie Zeit und Abende halten den 7-Tage-Abstand ein; nur Story und Leiter springen."""
    return not (str(s.get("id", "")).startswith(("date_", "frei_")) or s.get("art") in ("intim", "gespraech"))


def abschied_einleiten(z, modul):
    """Figur mit festem Abschied: feste Wirkung jetzt buchen, damit das Overlay sie zeigt; die Szene bleibt bis zum Klick offen."""
    sz = z["szene"]
    s, pid = sz["def"], sz["figuren"][0]
    zeilen = zustand.folgen_anwenden(z, modul, s.get("immer", []), frei=story_frei(s)) + gesten.zeit_auswerten(z, modul, sz)
    zeilen += figurenrahmen.szene_auswerten(z, modul, sz)
    sz["abschluss_zeilen"] = zeilen
    sz.pop("start_chips", None)
    zeile_einfuegen(z, modul, sz, pid, '"%s"' % figurenrahmen.abschied_text(z, modul, pid, sz), "neutral")
    sz["log"][-1]["lob"] = True                              # vorab vertont im Modul-Ordner
    sz["abschluss"] = figurenrahmen.abschluss_daten(z, modul, sz, pid)


def zug(z, modul, text, probe=None, reaktion=True, hinweis=""):
    if z["szene"].get("abschluss"):
        raise ValueError("The scene is over.")
    _zug_merken(z, text, reaktion, hinweis)
    sz = z["szene"]
    sz["log"].append({"art": "duc", "text": text})
    vorher = mitschrift(sz, modul)
    sz["zug"] += 1
    sz["vorschlaege"] = []
    sz.pop("start_chips", None)
    melden(z)
    extra = hinweis
    p = probe if probe else (None if hinweis or probe is False else probe_noetig(z, modul, sz, text))
    if p:
        sz["log"].append({"art": "wurf", "probe": p})
        melden(z)
        extra += ("Duc's attempt needed a %s check (difficulty %d): the dice say it is %s. Play that outcome - the "
                 "dice decide whether it works, not you. A check never overrides your hard limit.\n\n" % (
                     p["attribut"], p["sg"], wuerfel.ERGEBNIS_EN[p["ergebnis"]]))
    figuren = [x for x in sz["figuren"] if x != ERZAEHLER]
    # Reaktion VOR den Antworten (16.10.2026): hat Ducs Zug gesessen, soll man es in ihrer Antwort schon merken
    urteil = reaktionen.urteilen(z, modul, sz, text, vorher, kurz) if reaktion else {}
    def gespuer(pid):
        r = urteil.get(pid, "none")
        if r in ("trust", "desire"):
            return "(What Duc just said or did landed with her - let it show and move forward; do not fall back into an old argument.)\n\n"
        if r == "dislike" and z["tag"] > reaktionen.NUR_POSITIV_BIS_TAG:
            return "(What Duc just said or did annoyed her - she may say so once, then move on.)\n\n"
        return ""
    if not figuren:
        sprechen(z, modul, sz, ERZAEHLER, text, extra)
    else:
        angesprochen = sorted([x for x in figuren if kurz(modul, x) in text], key=lambda x: text.find(kurz(modul, x)))
        schon, zuletzt = [], None
        while len(schon) < (1 if len(figuren) == 1 else 2):      # Gruppe: hoechstens zwei Antworten je Zug
            pid = angesprochen.pop(0) if angesprochen else (figuren[0] if len(figuren) == 1 else regie(z, modul, sz, zuletzt, schon))
            if pid is None:
                if schon:
                    break
                pid = figuren[0]
            sprechen(z, modul, sz, pid, text, (extra if not schon else "") + gespuer(pid))
            schon.append(kurz(modul, pid))
            zuletzt = kurz(modul, pid)
    if reaktion:                    # jede freie Antwort wirkt (Wahlmomente haben feste Folgen)
        # Gesicht statt Vermutung (30.10.2026, nach Mundi): lacht sie in ihrer Antwort, kraenkt die Zeile nicht
        for e in sz["log"][-6:]:
            if e.get("art") == "figur" and urteil.get(e.get("wer")) == "dislike" and e.get("gefuehl") in VERSPIELT:
                urteil[e["wer"]] = "none"
        e = reaktionen.anwenden(z, modul, sz, text, urteil, kurz)
        if e:
            sz["log"].append(e)
            melden(z)
    ev = sz["def"].get("ereignis")
    if ev and not sz["ereignis_erledigt"] and sz["zug"] >= ev.get("nach_zug", 99):
        sz["ereignis_erledigt"] = True
        sz["log"].append({"art": "ereignis", "text": ev["text"]})
        melden(z)
        wer = next((x for x in sz["figuren"] if kurz(modul, x) in ev["text"]), sz["figuren"][0])
        sprechen(z, modul, sz, wer, "(event)", "EVENT - this happens now and %s reacts to it in this reply: %s\n\n" % (
            kurz(modul, wer), ev["text"]))
    vorbei = sz["zug"] >= sz["def"].get("max_zuege", 10)
    wm = sz["def"].get("wahlmoment")
    if wm and not vorbei and not sz.get("wahlmoment_erledigt") and sz["zug"] >= wm.get("nach_zug", 99):
        sz["wahlmoment_offen"] = True          # naechster Zug ist eine feste Entscheidung statt Freitext
    elif not vorbei and CFG.get("vorschlaege_auto", False):
        sz["vorschlaege"] = vorschlaege(z, modul, sz)
    return vorbei


# Nach der letzten Figuren-Antwort haengt das Spiel eigene Zeilen ans Log: die Reaktions-Leiste (seit 16.10.) und
# Folgen von Gesten. Frueher musste die LETZTE Zeile eine Figur sein - dadurch war "Neu formulieren" fast immer
# gesperrt (17.10.2026). Jetzt zaehlt die letzte Figuren-Zeile, solange dahinter nur solche Nachlauf-Zeilen stehen.
SWIPE_NACHLAUF = ("reaktion", "folgen")


def swipe_index(sz):
    """Index der Figuren-Zeile, die neu formuliert werden koennte - oder None."""
    if not sz or not sz.get("letzte"):
        return None
    log = sz["log"]
    for i in range(len(log) - 1, -1, -1):
        if log[i]["art"] == "figur":
            return i
        if log[i]["art"] not in SWIPE_NACHLAUF:
            return None
    return None


def kann_swipen(sz):
    return swipe_index(sz) is not None


def swipe(z, modul):
    sz = z["szene"]
    i = swipe_index(sz)
    if i is None:
        return False
    nachlauf = sz["log"][i + 1:]            # Reaktion/Folgen gehoeren zu Ducs Zug, nicht zum Wortlaut der Antwort
    del sz["log"][i:]
    l = sz["letzte"]
    sprechen(z, modul, sz, l["wer"], l["duc"], l["auftrag"], l.get("nachschlag", False))
    sz["log"].extend(nachlauf)               # bleiben hinter der neuen Antwort stehen
    melden(z)
    return True


# Beute (16.10.2026): Was Duc in der Szene klar bekommen hat (gekauft, gefunden, geschenkt), zaehlt - aber nur aus
# einer festen Liste, hoechstens ein Fund pro Szene, Mengen im Code gedeckelt. Das Modell erkennt, der Code bucht.
BEUTE_FEST = {"diesel": [{"wert": "diesel", "delta": 1}], "power": [{"wert": "strom", "delta": 1}],
              "money_50": [{"geld": 50, "text": "Fund"}], "money_100": [{"geld": 100, "text": "Fund"}],
              "money_200": [{"geld": 200, "text": "Fund"}]}
BEUTE_TEXT = {"diesel": "Diesel", "power": "Strom", "money_50": "50 €", "money_100": "100 €", "money_200": "200 €"}
BEUTE_ARTEN = ("geschenk", "gluecksbringer", "teil")


def beute_art(f):
    return f.get("wert") or ("geld" if "geld" in f else "item:%s" % f.get("item"))


MOMENT_TEXT = {"kiss": "they kissed", "intimate": "they slept together", "confession": "they admitted feelings for each other",
               "fight": "they had a real fight", "apology": "they made up after a quarrel",
               "promise": "Duc made her an explicit, serious promise about the future (not small favours like coffee)",
               "secret": "she told Duc something private about herself"}


def beute(z, modul, text, schon, frauen=()):
    """Szenen-Auswertung in EINEM Aufruf (16.10.2026): Fund (feste Liste) + wichtigster Moment mit einer Frau.
    -> Zeilen. schon = Folgen, die die Szene ueber Ausgaenge/immer bereits gebracht hat (dann nicht doppelt)."""
    items = [i for i, it in modul["items"].items() if it.get("art") in BEUTE_ARTEN and i not in z["inventar"]]
    fest = [k for k, fs in BEUTE_FEST.items()          # nur Werte, die das Modul hat (eden_rise: Strom/Diesel raus 30.10.2026)
            if all("wert" not in f or f["wert"] in modul["werte"] for f in fs)]
    optionen = ["nothing"] + fest + items
    liste = "\n".join("- %s: %s" % (o, BEUTE_TEXT.get(o) or modul["items"][o]["label"]) for o in optionen[1:])
    momente = ["none"] + list(MOMENT_TEXT)
    mit = list(frauen) + ["nobody"]
    q = lambda xs: " | ".join('"\\"%s\\""' % x for x in xs)
    gram = ('root ::= "{" ws "\\"fund\\":" ws (%s) "," ws "\\"moment\\":" ws (%s) "," ws "\\"with\\":" ws (%s) ws "}"\n'
            'ws ::= [ \\t\\n]*' % (q(optionen), q(momente), q(mit)))
    d, _ = llm.json_chat(
        RICHTER_SYS, "Scene transcript:\n\n%s\n\n1) fund: Did Duc clearly OBTAIN one of these concrete things in this "
        "scene - bought, found, won or explicitly handed to him, and now in his possession? Only if the transcript shows "
        "it plainly; talk, plans and promises do not count. Otherwise nothing.\n%s\n\n2) moment: the single most "
        "important thing that clearly happened between Duc and one woman in this scene, if any: %s. Only if it plainly "
        "happened, not if it was only hinted or talked about. with: which woman (%s), or nobody.\n\n"
        "JSON: {\"fund\": \"<id>\", \"moment\": \"<kind>\", \"with\": \"<who>\"}"
        % (text, liste, ", ".join("%s = %s" % (k, v) for k, v in MOMENT_TEXT.items()), ", ".join(frauen) or "-"),
        gram, 40)
    d = d or {}
    zeilen = []
    m, w = d.get("moment", "none"), d.get("with", "nobody")
    if m in chronik.MOMENTE and w in frauen:
        doppelt = any(e.get("moment") == m and w in e["wer"] and e["tag"] == z["tag"] for e in chronik.liste(z))
        if not doppelt:
            satz, wichtig, dauer = chronik.MOMENTE[m]
            chronik.eintragen(z, modul, "moment", satz.format(n=modul["personen"][w]["name"].split()[0]), wer=[w],
                              wichtig=wichtig, dauer=dauer, moment=m)
    fund = d.get("fund", "nothing")
    if fund == "nothing" or fund not in optionen:
        return zeilen
    folgen = BEUTE_FEST.get(fund) or [{"item": fund}]
    if beute_art(folgen[0]) in {beute_art(f) for f in schon}:
        return zeilen
    label = BEUTE_TEXT.get(fund) or modul["items"][fund]["label"]
    chronik.eintragen(z, modul, "fund", "Duc obtained: %s." % label, wichtig=1)
    return zeilen + ["Gefunden: " + label] + zustand.folgen_anwenden(z, modul, folgen)


def beenden(z, modul):
    """Ausgaenge, Folgen, Gedaechtnis, 'heute'. Liefert die Meldungen fuer die Anzeige."""
    sz = z["szene"]
    s, text = sz["def"], mitschrift(sz, modul, 200)
    treffer, zeilen = [], []
    gebucht = list(s.get("immer", []))                    # fuer die Beute-Pruefung: nichts doppelt gutschreiben
    vorab = "abschluss_zeilen" in sz                      # schon beim Abschied gebucht (Overlay zeigt sie)
    zeilen += [] if vorab else zustand.folgen_anwenden(z, modul, s.get("immer", []), frei=story_frei(s))     # feste Folgen (z. B. Andenken) - ohne Richter
    frauen = [p for p in sz["figuren"] if modul["personen"].get(p, {}).get("romanzierbar")]
    for f in s.get("immer", []):
        it = modul["items"].get(f.get("item"), {})
        if it.get("art") == "andenken":
            chronik.eintragen(z, modul, "andenken", "Duc received a keepsake: %s." % it["label"], wer=frauen[:1], wichtig=2)
    for a in s.get("ausgaenge", []):
        d, _ = llm.json_chat(RICHTER_SYS, "Scene transcript:\n\n%s\n\nQuestion: %s Did this clearly happen in the scene? "
                             "JSON: {\"verdict\": true|false}" % (text, a["wenn"]), llm.bool_grammatik(["verdict"]), 20)
        if d and d.get("verdict"):
            treffer.append(a["wenn"])
            zeilen += zustand.folgen_anwenden(z, modul, a.get("folgen", []))
            gebucht += a.get("folgen", [])
            chronik.eintragen(z, modul, "ausgang", a["wenn"],
                              wer=[p for p in sz["figuren"] if p in modul["personen"] and kurz(modul, p) in a["wenn"]],
                              wichtig=2)
    # Figuren mit Rahmen: Das Modell legt keine Momente an, und die Szene zaehlt fest (Duc 31.10.2026)
    zeilen += beute(z, modul, text, gebucht, [p for p in frauen if not figurenrahmen.gilt(modul, p)])
    if not vorab:
        zeilen += gesten.zeit_auswerten(z, modul, sz)
        zeilen += figurenrahmen.szene_auswerten(z, modul, sz)
    einstiege_merken(z, sz)
    belege = mitschrift_fakten(sz, modul)
    # Figuren mit Rahmen: keine Zusammenfassung vom Modell, sie blies Szenen auf (Duc 01.11.2026)
    kurzfassung, _ = ("", None) if figurenrahmen.szene_gilt(modul, s, list(sz["figuren"])) else llm.chat("You summarise scenes of a story game. You are precise about who said and did what.",
                              "Scene: %s\n\n%s\n\nSummarise what happened in one or two short sentences, past tense, "
                              "third person. Facts only - lines marked DUC are what Duc said or did; thoughts in "
                              "*asterisks* are private impressions, not facts." % (s["titel"], belege), max_tokens=90)
    for pid in sz["figuren"]:
        if pid == ERZAEHLER or not modul["personen"][pid].get("karte") or figurenrahmen.gilt(modul, pid):
            continue
        satz, _ = llm.chat("You keep a character's memory for a story game. You are precise about who said and did what.",
                           "Scene: %s\n\n%s\n\nWrite what %s remembers from this scene: two or three short sentences, "
                           "past tense, third person - what happened between her and Duc, what she learned about him, "
                           "how she feels now. Lines marked DUC are exactly what Duc said or did - attribute them "
                           "correctly (if Duc praised someone, say whom). Her private suspicions may appear only as "
                           "her impression, never as fact." % (s["titel"], belege, name(modul, pid)), max_tokens=120)
        zustand.gedaechtnis_add(z, pid, satz)
    z["heute"].append({"phase": z["phase"], "szene": s["id"], "titel": s["titel"], "ort": s.get("ort"),
                       "anwesend": [x for x in sz["figuren"] if x != ERZAEHLER], "kurz": kurzfassung, "ausgaenge": treffer,
                       "auftraege": sz["auftraege"]})
    nachrichten = handy.nach_szene(z, modul, s, sz["figuren"], lambda pid: karte(modul, modul["personen"][pid])["bogen"])
    archiv = {"tag": z["tag"], "phase": z["phase"], "szene": s["id"], "titel": s["titel"], "log": sz["log"],
              "ausgaenge": treffer, "folgen": zeilen}
    z["szene"] = None
    zeilen = sz.get("wahl_folgen", []) + zeilen
    zeilen += ["📱 Message from %s" % name(modul, pid).split()[0] for pid in nachrichten]
    return {"titel": s["titel"], "ausgaenge": treffer, "folgen": zeilen, "kurz": kurzfassung}, archiv

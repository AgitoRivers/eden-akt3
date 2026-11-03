# -*- coding: utf-8 -*-
r"""Karten fuer Lola Brennan, Megan McAllister und Marit Holm (17.10.2026) aus lola.txt / megan.txt / holm.txt.

    karten_lola_megan_holm.py          Probelauf: prueft die Quellen, schreibt nichts

Einspielen kommt spaeter (wenn die Sprites und damit die Portraits stehen): wie bei Rosi und Siri ueber den
Char Creator (Steckbrief, Char-Builder-JSON in cards\Eden Yacht, ST-PNG mit Portrait als Avatar).
Pruefregeln wie karten_rosi_siri.py; die Begruessungs-Slots rechnet das Skript selbst nach
creator.begruessungs_slots (je Kostuem eine, dazu Zweitszenen), damit der Probelauf den Char Creator nicht laedt.
"""
import io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.argv = [sys.argv[0]]
from karten_einspielen import quelle, FELDER  # noqa: E402

# Kostueme wie in den Prompt-Studio-Presets Yacht_Lola / Yacht_Megan / Yacht_Holm (sp_kost)
FIG = {"lola": ("Lola Brennan", ["Galley", "Off Duty", "nude"]),
       "megan": ("Megan McAllister", ["Boardroom", "Inspection"]),
       "holm": ("Marit Holm", ["Bridge", "Night Watch"])}


def slots(kost):
    k = list(kost)
    kleider = [x for x in k if x.lower() != "nude"]
    return k + (kleider[:2] if len(k) <= 3 else kleider[:1])


def pruefen(q, kost):
    fehler = []
    for lang in ("en", "de"):
        for f in FELDER + ["depth_prompt"]:
            if not q[lang].get(f):
                fehler.append("%s.%s fehlt" % (lang, f))
        if q[lang].get("mes_example", "").count("<START>") != 6:
            fehler.append("%s: nicht genau 6 Beispielbloecke" % lang)
        alle = [q[lang]["first_mes"]] + q[lang]["alternate_greetings"]
        soll = slots(kost)
        if len(alle) != len(soll):
            fehler.append("%s: %d Begruessungen, Slots %d" % (lang, len(alle), len(soll)))
        for i, (g, k) in enumerate(zip(alle, soll)):
            if not g.startswith("+++ "):
                fehler.append("%s #%d ohne +++ Kopf" % (lang, i + 1))
            m = re.search(r"<!--set:([^>]+?)-->", g)
            if not m or m.group(1) != k:
                fehler.append("%s #%d: Set %s, erwartet %s" % (lang, i + 1, m and m.group(1), k))
        for marke in (("[Knows]", "[Heat]", "[Rules]") if lang == "en" else ("[Weiß]", "[Hitze]", "[Regeln]")):
            if marke not in q[lang]["depth_prompt"]:
                fehler.append("%s: %s fehlt" % (lang, marke))
        if "{{user}} is male" not in q[lang]["description"] and "{{user}} ist männlich" not in q[lang]["description"]:
            fehler.append("%s: Zeile '{{user}} is male' fehlt" % lang)
    t = json.dumps(q, ensure_ascii=False)
    if re.search(r"[“”„]", t):
        fehler.append("typografische Anfuehrungszeichen")
    if re.search(r"\bDuc\b", t):
        fehler.append("'Duc' statt {{user}}")
    if re.search(r"high heels|\bin heels\b|stiletto|pumps\b|Absatzschuh|Stöckel|High Heels", t, re.I):
        fehler.append("Heels erwaehnt")
    return fehler


gesamt = 0
for key, (name, kost) in FIG.items():
    q = quelle(key)
    f = pruefen(q, kost)
    gesamt += len(f)
    woerter = {l: sum(len(str(v).split()) for k, v in q[l].items() if k != "alternate_greetings")
               + sum(len(g.split()) for g in q[l]["alternate_greetings"]) for l in ("en", "de")}
    print("%-17s Kostueme %-28s Begruessungen %d | Woerter EN %d / DE %d | %s"
          % (name, ", ".join(kost), 1 + len(q["en"]["alternate_greetings"]), woerter["en"], woerter["de"],
             "OK" if not f else "FEHLER"))
    for x in f:
        print("   - " + x)
print("PROBELAUF - nichts geschrieben" + ("" if not gesamt else " (%d Fehler)" % gesamt))

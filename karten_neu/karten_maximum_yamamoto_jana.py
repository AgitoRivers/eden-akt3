# -*- coding: utf-8 -*-
r"""Karten fuer Mr. Maximum, Yamamoto-san und Jana Maihoff (19.10.2026) aus maximum.txt / yamamoto.txt / jana.txt.

    karten_maximum_yamamoto_jana.py          Probelauf: prueft die Quellen, schreibt nichts

Pruefregeln wie karten_lola_megan_holm.py. Unterschied: Mr. Maximum und Yamamoto-san sind Freunde, keine
Romanze; ihr depth-Block traegt [Bond]/[Bindung] statt [Heat]/[Hitze]. Jana ist NPC wie Lola (mit [Heat]).
Einspielen spaeter ueber den Char Creator (cc_figuren_maximum_yamamoto_jana.py), PNG erst mit den Portraits.
"""
import io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.argv = [sys.argv[0]]
from karten_einspielen import quelle, FELDER  # noqa: E402

# Kostueme wie in den Prompt-Studio-Presets Yacht_Maximum / Yacht_Yamamoto / Yacht_Jana (sp_kost)
FIG = {"maximum": ("Maxwell Ndlovu", ["Steward", "Training", "Party"], False),
       "yamamoto": ("Yamamoto-san", ["Hawaii", "Badeanzug", "Leder", "Party"], False),
       "jana": ("Jana Maihoff", ["Deck", "Bikini", "Party Dress", "Kitty", "Kink"], True)}


def slots(kost):
    k = list(kost)
    kleider = [x for x in k if x.lower() != "nude"]
    return k + (kleider[:2] if len(k) <= 3 else kleider[:1])


def pruefen(q, kost, romanze):
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
        if lang == "en":
            marken = ("[Knows]", "[Heat]" if romanze else "[Bond]", "[Rules]")
        else:
            marken = ("[Weiß]", "[Hitze]" if romanze else "[Bindung]", "[Regeln]")
        for marke in marken:
            if marke not in q[lang]["depth_prompt"]:
                fehler.append("%s: %s fehlt" % (lang, marke))
        if "{{user}} is male" not in q[lang]["description"] and "{{user}} ist männlich" not in q[lang]["description"]:
            fehler.append("%s: Zeile '{{user}} is male' fehlt" % lang)
    # EN und DE: gleiche Titel und Sets in gleicher Reihenfolge
    kopf = lambda lang: [g.split("\n", 1)[0] for g in [q[lang]["first_mes"]] + q[lang]["alternate_greetings"]]
    if kopf("en") != kopf("de"):
        fehler.append("Titel/Sets EN und DE verschieden")
    t = json.dumps(q, ensure_ascii=False)
    if re.search(r"[“”„]", t):
        fehler.append("typografische Anfuehrungszeichen")
    if re.search(r"\bDuc\b", t):
        fehler.append("'Duc' statt {{user}}")
    if re.search(r"high heels|\bin heels\b|\bheels\b|stiletto|pumps\b|Absatzschuh|Stöckel|High Heels", t, re.I):
        fehler.append("Heels erwaehnt")
    return fehler


gesamt = 0
for key, (name, kost, romanze) in FIG.items():
    q = quelle(key)
    f = pruefen(q, kost, romanze)
    gesamt += len(f)
    woerter = {l: sum(len(str(v).split()) for k, v in q[l].items() if k != "alternate_greetings")
               + sum(len(g.split()) for g in q[l]["alternate_greetings"]) for l in ("en", "de")}
    print("%-15s Kostueme %-34s Begruessungen %d | Woerter EN %d / DE %d | %s"
          % (name, ", ".join(kost), 1 + len(q["en"]["alternate_greetings"]), woerter["en"], woerter["de"],
             "OK" if not f else "FEHLER"))
    for x in f:
        print("   - " + x)
print("PROBELAUF - nichts geschrieben" + ("" if not gesamt else " (%d Fehler)" % gesamt))

# -*- coding: utf-8 -*-
r"""Karten fuer Rosi Scuderi und Siri Lindvik (13.10.2026) aus rosi.txt / siri.txt.

    karten_rosi_siri.py          Probelauf: prueft die Quellen, schreibt nichts
    karten_rosi_siri.py --los    schreibt ueber den Char Creator: Steckbrief-Karte (EN + DE-Zwilling),
                                 Char-Builder-JSON (cards\Eden Yacht) und ST-PNG mit Portrait als Avatar.
Neue Figuren haben noch keine PNG - deshalb nicht karten_einspielen.py, sondern Char-Creator-Weg
(karte_schreiben + st_export), wie Station 5/8 es tun wuerden."""
import io, json, os, re, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\CharCreator")
NUR = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--nur=")]       # z. B. --nur=siri
sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a == "--los"]
LOS = "--los" in sys.argv
from karten_einspielen import quelle, FELDER  # noqa: E402
sys.argv = ["creator.py", "--no-browser"]
import creator as c  # noqa: E402

FIG = {"rosi": "dd0b5c481386", "siri": "d10fa39ae605"}
ROSI_ETO = {
    "rolle": "ETO (Electro-Technical Officer) der M/Y Eden Rise, dritte Saison: Solardach, Batterien, E-Antrieb, Diesel-Notstromaggregat 'Unit-01'",
    "hintergrund": "Eigentlich Rosaria. Aufgewachsen in der Vespa-Werkstatt ihres Vaters Salvo in Catania, mit acht zerlegte sie ihren ersten Vergaser. Vor vier Jahren ging die Werkstatt an die Bank. Sie fährt zur See, weil es dort das beste Geld gibt, und spart jede Saison für den Rückkauf. Auf der solarbetriebenen Eden Rise hält sie Solardach, Batterien und E-Antrieb am Leben; das einzige laute Ding an Bord, das Diesel-Notstromaggregat, ist ihr Liebling 'Unit-01'. Liest Manga in der Koje.",
}


def pruefen(name, q, kost):
    fehler = []
    for lang in ("en", "de"):
        for f in FELDER + ["depth_prompt"]:
            if not q[lang].get(f):
                fehler.append("%s.%s fehlt" % (lang, f))
        if q[lang].get("mes_example", "").count("<START>") != 6:
            fehler.append("%s: nicht genau 6 Beispielbloecke" % lang)
        alle = [q[lang]["first_mes"]] + q[lang]["alternate_greetings"]
        if len(alle) != len(c.begruessungs_slots({"kostueme": kost})):
            fehler.append("%s: %d Begruessungen, Slots %d" % (lang, len(alle), len(c.begruessungs_slots({"kostueme": kost}))))
        for i, (g, (k, _)) in enumerate(zip(alle, c.begruessungs_slots({"kostueme": kost}))):
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
    if re.search(r"[\u201c\u201d\u201e]", t):
        fehler.append("typografische Anfuehrungszeichen")
    if re.search(r"\bDuc\b", t):
        fehler.append("'Duc' statt {{user}}")
    if re.search(r"high heels|\bin heels\b|stiletto|pumps\b|Absatzschuh|Stöckel|High Heels", t, re.I):   # Ferse ("on her heels") ist erlaubt
        fehler.append("Heels erwaehnt")
    return fehler


for name, fid in FIG.items():
    if NUR and name not in NUR:
        continue
    f = c.fig_laden(fid)
    q = quelle(name)
    tags = {k.split(":", 1)[0]: k.split(":", 1)[1] for k in q["tags"] if ":" in k}
    fehler = pruefen(name, q, f["kostueme"])
    woerter = len(q["en"]["first_mes"].split())
    print("== %s (%s): %d Begruessungen EN/%d DE, Tags %s, Erstbegruessung %d Woerter -> %s" % (
        c.karten_name(f), fid, 1 + len(q["en"]["alternate_greetings"]), 1 + len(q["de"]["alternate_greetings"]),
        {k: tags.get(k) for k in ("type", "friction", "who", "tone")}, woerter, "OK" if not fehler else fehler))
    if fehler or not LOS:
        continue
    karte = {"tags": {k: tags[k] for k in ("type", "friction", "who", "tone")},
             "befunde": [], "punkte": None, "erzeugt": time.strftime("%Y-%m-%d %H:%M:%S"), "gespeichert": False}
    for lang in ("en", "de"):
        karte[lang] = {k: (list(q[lang][k]) if k == "alternate_greetings" else q[lang][k])
                       for k in FELDER + ["alternate_greetings", "depth_prompt"]}
    f["karte"] = karte
    if name == "rosi":
        for p in [f["profil"]] + list(f.get("profile") or []):
            p.update(ROSI_ETO)
    f["station"] = max(f.get("station", 1), 5)
    c.karte_schreiben(f)
    pfad = c.st_export(f)
    f["station"] = 8
    c.fig_speichern(f)
    d = c.dc.load_json(f["karte_datei"], {}, "x")["data"]
    try:
        punkte = c.cg().bewerte(d)["punkte"]
    except Exception as e:
        punkte = "nicht bewertbar (%s)" % e
    print("   geschrieben: %s | PNG %s | Bewertung %s" % (f["karte_datei"], pfad, punkte))
    for x in c.pruefliste(f):
        print("   %s %s %s" % ("OK" if x["ok"] else "--", x["punkt"], x["detail"][:80]))

# -*- coding: utf-8 -*-
r"""Neue Yacht-Karten (13.10.2026) aus chiara.txt / sophia.txt / lea.txt einspielen.

    karten_einspielen.py          Probelauf: prueft die Quelldateien, zeigt Umfang, schreibt nichts
    karten_einspielen.py --los    sichert nach X:\AI\_Sicherung_Karten_20261013 und schreibt:
        - ST-Karten-PNG (ueber DucCommon, Bilddaten unberuehrt, Geschwisterfelder wie "chat" bleiben)
        - Char-Builder-Spiegel  cards\Eden Yacht\<Name>.json  (= Inhalt der PNG)
        - Char-Creator-Steckbrief: karte {en, de, tags} und das deutsche Kurzprofil

Quellformat: Abschnitte "=== en.description" usw.; "=== en.alt" / "=== de.alt" beliebig oft (je eine
alternative Begruessung); "=== tags" kommagetrennt.
"""
import json, os, re, shutil, sys, time

sys.path.insert(0, r"X:\AI\DucCommon")
import duc_common as dc  # noqa: E402

LOS = "--los" in sys.argv
HIER = os.path.dirname(os.path.abspath(__file__))
SICHER = r"X:\AI\_Sicherung_Karten_20261013"
ST = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\characters"
RG = r"X:\AI\RoleplayGen\cards\Eden Yacht"
CC = r"X:\AI\CharCreator\figuren"
FIG = {"chiara": ("Chiara Sonnberg", "20f1d084569e"), "sophia": ("Sophia Moore", "b5b20a86c027"),
       "lea": ("Lea Moore", "e96294f2348c")}
FELDER = ["description", "personality", "scenario", "first_mes", "mes_example"]

# Deutsches Kurzprofil fuer den Char Creator (dessen Station 1/2 und spaetere Neuerzeugung lesen es).
PROFIL = {
    "chiara": {
        "pitch": "Laute, warme Chefstewardess aus einer Hamburger Kapitänsfamilie, die heimlich für ihr eigenes Kommando lernt.",
        "name": "Chiara Sonnberg", "alter": "29", "rolle": "Chefstewardess der M/Y Eden, sechste Saison",
        "herkunft": "Hamburg-Blankenese, Familie von Kapitänen",
        "aussehen": "platinblond, sehr langes glattes Haar im hohen Pferdeschwanz, graublaue Augen, roter Lippenstift, Sommersprossen auf den Schultern",
        "hintergrund": "Opa Hinrich fuhr Containerschiffe, Bruder Jonas ging auf die Seefahrtschule, das Mädchen sollte Gastgeberin werden. Opa hinterließ ihr Marinejacke und Messingsextant.",
        "wunde": "Für die Familie war sie immer die Gastgeberin, nie die Kapitänin.",
        "widerspruch": "Der lauteste Mensch an Bord, nachts allein auf der Brücke ganz still.",
        "will": "Eigenes Kommando; jemand, der mehr in ihr sieht als die Lustige.",
        "zu_user": "Gleichrangig, Rivalität Deck gegen Innendienst; er kann Astronavigation, was nervt.",
        "stimme": "laut, warm, schnell, bewertet alles bis zehn, Hamburger Direktheit",
        "friction": "Er könnte ihr beibringen, woran sie gescheitert ist, aber fragen hieße zugeben.",
        "geheimnis": "Im April durch die Yachtmaster-Theorie gefallen, lernt nachts auf der Brückennock.",
        "eigenheit": "Verrät ihre eigenen Überraschungspartys, umarmt Leute mitten im Satz.",
        "ensemble": "Sophia: beste Freundin und Rivalin (Strichliste). Lea: ihr Küken, mit ihr am strengsten.",
        "outfit_med": "Uniform", "outfit_top": "Harbor Night",
        "nude_szene": "Außendusche auf der Badeplattform nach verlorener Wette, Kabinendusche kaputt.",
        "tag_type": "fiery", "tag_friction": "secret", "tag_who": "colleague", "tag_tone": "playful"},
    "sophia": {
        "pitch": "Charismatische Concierge aus Cornwall, die jeden Tisch der Riviera bekommt und nachts heimlich Krimis schreibt.",
        "name": "Sophia Moore", "alter": "28", "rolle": "Concierge und Guest Relations der M/Y Eden, vierte Saison",
        "herkunft": "Falmouth, Cornwall; zwei Jahre Zweitbesetzung im West End",
        "aussehen": "langes gestuftes honigblondes Haar, hellblaugraue Augen, roter Mund, Lächeln, das Ärger verspricht",
        "hintergrund": "Chaotische Künstlermutter; ab vierzehn hat sie Lea großgezogen und alle um den Finger gewickelt. Büchlein der Gefallen.",
        "wunde": "Alle lieben sie, keiner kennt sie.",
        "widerspruch": "Sieht sofort, was jeder braucht, und sorgt dafür, dass niemand fragt, was sie braucht.",
        "will": "Ihr eigener Name auf einem Buchrücken; jemand, den sie nicht erst gewinnen muss.",
        "zu_user": "Ihr Charme ist an ihm abgeglitten; seitdem wettet sie mit ihm.",
        "stimme": "tief, warm, britisches Understatement, 'Darling', ein Satz dann Stille",
        "friction": "Charme ist ihr einziges Werkzeug, und bei ihm wirkt es nicht ganz.",
        "geheimnis": "Schreibt Krimis als M. J. Penrose (14 Absagen); hat letzten Winter Chiaras Job abgelehnt, ohne es ihr zu sagen.",
        "eigenheit": "Schreibt mitten im Gespräch ins Lederbüchlein und sagt nie, was.",
        "ensemble": "Chiara: beste Freundin und Rivalin. Lea: kleine Schwester, hat ihr den Job besorgt.",
        "outfit_med": "Concierge", "outfit_top": "Crew Party",
        "nude_szene": "Nacktschwimmen im Morgengrauen von der Badeleiter, eine Gewohnheit aus Falmouth.",
        "tag_type": "tease", "tag_friction": "testing", "tag_who": "colleague", "tag_tone": "playful"},
    "lea": {
        "pitch": "Naive, begeisterte Decksfrau aus Cornwall, für die alles neu ist und die heimlich Opas Wrack sucht.",
        "name": "Lea Moore", "alter": "23", "rolle": "Decksfrau und Guide für Wassersport und Ausflüge, erste Saison",
        "herkunft": "Falmouth, Cornwall; Opa Jack war Fischer",
        "aussehen": "sehr langes gestuftes hellaschbraunes Haar, meist geflochten und nass, graugrüne Augen, Sommersprossen",
        "hintergrund": "Sophia hat sie ab neun großgezogen. Opa erzählte von der Margot, 1924 vor dem Esterel gesunken; er starb letzten Winter.",
        "wunde": "Angst, eines Tages abgestumpft zu sein wie die alte Crew.",
        "widerspruch": "Der begeistertste Mensch an Bord, mit der größten Angst, dass sie nichts mehr begeistert.",
        "will": "Opas Wrack; ernst genommen werden, ohne sich zu ändern.",
        "zu_user": "Ihr Chef im Deck-Team; der einzige Offizier, der sich ihre Zeichnungen angesehen hat.",
        "stimme": "schnell, hell, ernsthaft, Meerestier-Fakten, Cornwall-Singsang",
        "friction": "Er ist ihr Chef, und sie will mehr sein als das aufgeregte neue Mädchen.",
        "geheimnis": "Taucht allein nach dem Wrack (gegen die Regeln); hat sich heimlich für eine Azoren-Expedition beworben.",
        "eigenheit": "Hält die Luft an, wenn sie etwas umhaut; salutiert, wenn sie nervös ist.",
        "ensemble": "Sophia: große Schwester. Chiara: ihr Vorbild, deren Sprüche sie leicht falsch zitiert.",
        "outfit_med": "Deck", "outfit_top": "Crew Party",
        "nude_szene": "Heimlicher Nachttauchgang, schält sich auf der Badeplattform aus dem Neopren und wird erwischt.",
        "tag_type": "curious", "tag_friction": "role-conflict", "tag_who": "employee", "tag_tone": "wholesome"},
}


def quelle(name):
    abschnitte, aktuell = [], None
    for zeile in open(os.path.join(HIER, name + ".txt"), encoding="utf-8").read().split("\n"):
        m = re.match(r"^=== (\S+)\s*$", zeile)
        if m:
            aktuell = [m.group(1), []]
            abschnitte.append(aktuell)
        elif aktuell is not None:
            aktuell[1].append(zeile)
    q = {"en": {"alternate_greetings": []}, "de": {"alternate_greetings": []}, "tags": []}
    for key, zeilen in abschnitte:
        text = "\n".join(zeilen).strip("\n").rstrip()
        if key == "tags":
            q["tags"] = [t.strip() for t in text.split(",") if t.strip()]
            continue
        lang, feld = key.split(".", 1)
        if feld == "alt":
            q[lang]["alternate_greetings"].append(text)
        elif feld == "depth":
            q[lang]["depth_prompt"] = text
        else:
            q[lang][feld] = text
    return q


def pruefen(name, q):
    fehler = []
    for lang in ("en", "de"):
        for f in FELDER + ["depth_prompt"]:
            if not q[lang].get(f):
                fehler.append("%s.%s fehlt" % (lang, f))
        n_en, n_de = len(q["en"]["alternate_greetings"]), len(q["de"]["alternate_greetings"])
        if n_en != n_de:
            fehler.append("Begruessungen EN %d / DE %d" % (n_en, n_de))
        for g in [q[lang].get("first_mes", "")] + q[lang]["alternate_greetings"]:
            if not g.startswith("+++ "):
                fehler.append("%s: Begruessung ohne +++ Kopfzeile: %s" % (lang, g[:40]))
        if q[lang].get("mes_example", "").count("<START>") != 6:
            fehler.append("%s.mes_example: nicht genau 6 Bloecke" % lang)
    # Set-Marker muessen zu den Kostuemen passen
    kost = json.load(open(os.path.join(CC, FIG[name][1] + ".json"), encoding="utf-8"))["kostueme"]
    for lang in ("en", "de"):
        for g in [q[lang]["first_mes"]] + q[lang]["alternate_greetings"]:
            for s in re.findall(r"<!--set:([^>]+?)-->", g):
                if s not in kost:
                    fehler.append("%s: Set %s gibt es nicht (%s)" % (lang, s, kost))
    # EN und DE muessen dieselben Sets in derselben Reihenfolge haben
    sets = lambda lang: [re.findall(r"<!--set:([^>]+?)-->", g) for g in [q[lang]["first_mes"]] + q[lang]["alternate_greetings"]]
    if sets("en") != sets("de"):
        fehler.append("Set-Reihenfolge EN/DE unterschiedlich")
    if re.search(r"[\u201c\u201d\u201e]", json.dumps(q, ensure_ascii=False)):
        fehler.append("typografische Anfuehrungszeichen gefunden")
    return fehler


def sichern(p):
    if LOS and os.path.exists(p):
        rel = os.path.splitdrive(p)[1].lstrip("\\/")
        ziel = os.path.join(SICHER, rel)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        if not os.path.exists(ziel):
            shutil.copy2(p, ziel)


def zwilling(q, lang, welt):
    t = {f: q[lang][f] for f in FELDER}
    t["alternate_greetings"] = list(q[lang]["alternate_greetings"])
    t["character_book"] = None
    t["depth_prompt"] = q[lang]["depth_prompt"]
    t["tags"] = list(q["tags"])
    t["world"] = welt
    return t


def einspielen(name, q):
    st_name, fid = FIG[name]
    png = os.path.join(ST, st_name + ".png")
    roh = dc.karte_roh_lesen(png)
    d = roh["data"]
    for f in FELDER:
        d[f] = q["en"][f]
    d["alternate_greetings"] = list(q["en"]["alternate_greetings"])
    d["tags"] = list(q["tags"])
    ext = d.setdefault("extensions", {})
    alt_dp = ext.get("depth_prompt") or {}
    ext["depth_prompt"] = {"prompt": q["en"]["depth_prompt"], "depth": alt_dp.get("depth", 2), "role": alt_dp.get("role", "system")}
    ext["world"] = "Eden Yacht"
    ext["lang_aktiv"] = "en"
    ext["lang_twin"] = {"en": zwilling(q, "en", "Eden Yacht"), "de": zwilling(q, "de", "Eden Yacht (DE)")}
    if not LOS:
        return
    sichern(png)
    dc.karte_schreiben(png, roh, d)
    # Char-Builder-Spiegel: Inhalt der PNG (spec, spec_version, data), Format der bisherigen Datei
    rg = os.path.join(RG, st_name + ".json")
    sichern(rg)
    nach = dc.karte_roh_lesen(png)
    with open(rg, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"spec": nach.get("spec", "chara_card_v2"), "spec_version": nach.get("spec_version", "2.0"),
                   "data": nach["data"]}, fh, ensure_ascii=False, indent=1)
    # Char Creator
    cp = os.path.join(CC, fid + ".json")
    sichern(cp)
    f = json.load(open(cp, encoding="utf-8"))
    karte = dict(f.get("karte") or {})
    for lang in ("en", "de"):
        karte[lang] = {k: (q[lang][k] if k != "alternate_greetings" else list(q[lang][k]))
                       for k in FELDER + ["alternate_greetings", "depth_prompt"]}
    karte["tags"] = list(q["tags"])
    karte["gespeichert"] = True
    karte["erzeugt"] = time.strftime("%Y-%m-%d %H:%M:%S")
    karte["befunde"] = []
    f["karte"] = karte
    f["profil"] = dict(f.get("profil") or {}, **PROFIL[name])
    f["geaendert"] = time.strftime("%Y-%m-%d %H:%M:%S")
    roh_cc = open(cp, "rb").read(4096)
    nl = "\r\n" if b"\r\n" in roh_cc else "\n"
    with open(cp, "w", encoding="utf-8", newline=nl) as fh:
        json.dump(f, fh, ensure_ascii=False, indent=1)


def main():
    alle_ok = True
    for name in FIG:
        q = quelle(name)
        fehler = pruefen(name, q)
        woerter = sum(len(" ".join([q["en"][f] for f in FELDER] + q["en"]["alternate_greetings"] + [q["en"]["depth_prompt"]]).split()) for _ in [0])
        print("%-7s Begruessungen %d | EN-Woerter %d | Tags %s" % (name, 1 + len(q["en"]["alternate_greetings"]), woerter, q["tags"]))
        for x in fehler:
            print("   FEHLER:", x)
        alle_ok &= not fehler
        if not fehler:
            einspielen(name, q)
    print("geschrieben, Sicherung in " + SICHER if LOS and alle_ok else ("PROBELAUF" if not LOS else "abgebrochen"))


if __name__ == "__main__":
    main()

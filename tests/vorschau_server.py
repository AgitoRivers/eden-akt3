# -*- coding: utf-8 -*-
r"""Vorschau-Server zum Ansehen der Oberflaeche (18.10.2026): die echte Engine auf eigenem Port (Standard 8328), mit
Wegwerf-Spielstaenden und Wegwerf-Konfiguration, ohne Sprachmodell (feste Antworten). Fasst weder spielstaende\ noch
eden-config.json an. Zum Pruefen von Client-Aenderungen, nicht zum Spielen.

  python tests\vorschau_server.py [--port 8328] [--modul eden_rise]
  python tests\vorschau_server.py --tag 3 --inventar multitool,used_battery --konto 900
      spielt per Bot (tests\lauf_test.py, ohne Missionen) bis zum Morgen von Tag 3 vor und legt Gegenstaende ins Inventar
  --tag 2 --frei --flags kloster_angenommen   bis zur ersten freien Mittagsphase, Flags setzen (Macchia-Karte ansehen)
  --vorliebe rosi:feigen:mag,rosi:arancini:mag:gelesen   entdeckte Vorlieben vorbereiten (Meldung/Profil ansehen)
  --tag 5 --sturm vorbereitung   direkt in die Sturm-Vorbereitung (oder: nacht, nach der Bot-Einteilung) (27.10.2026)
  --tag 2 --frei --fische zander:2,sardine:3   Fisch im Vorrat und im Journal (Petrus Reiter "Sell Fish", 28.10.2026)
  --tag 2 --frei --rohstoffe cork:4,feather:5,iron:3,timber:3 --konto 300   Material fuer Petrus Koeder (Reiter "Baits", 30.10.2026)
  --tag 2 --frei --attributpunkte 3   freie Attributpunkte (Lob der Crew bei Wert 3/4/5 ansehen, 27.10.2026)
  --kampf mochis_geier --kampf-level 6 --mochis geier:1   Tierstation: wie oft schon gefangen (kein Eintrag = erster Fang: Overlay, 1 = zweiter: Handy)
  --kampf akt1_fackelpirat --kampf-level 9 --skills K3,K5,M3,M5 --waffe sword --ruestung jacket_fire
      Testschalter (Kampf, 24.10.2026): Level, Skills und Ausruestung direkt setzen - nur hier, nie im echten Spiel
"""
import json, os, shutil, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
if ("--tag" in sys.argv or "--anhoerung" in sys.argv) and os.environ.get("PYTHONHASHSEED") != "0":    # Bot aus lauf_test braucht festen Hash-Seed
    import subprocess
    sys.exit(subprocess.call([sys.executable] + sys.argv, env=dict(os.environ, PYTHONHASHSEED="0")))
sys.path.insert(0, os.path.dirname(HIER))
sys.path.insert(0, HIER)
import eden  # noqa: E402
from kern import kampf, llm, stimme  # noqa: E402


def arg(name, std):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else std


llm.bereit = lambda: True
llm.chat = lambda system, user, sampler=None, max_tokens=300, grammar=None: ("She nods and says nothing.", 0.0)
llm.json_chat = lambda system, user, grammar, max_tokens=120, sampler=None: (None, 0.0)
_chatterbox_echt = stimme.chatterbox


def _nur_vorhandene(name, text, ordner, ganz=False):
    """Play finished recordings only, never create new ones (Chatterbox stays out of the preview)."""
    import urllib.request as ur
    alt = ur.urlopen
    ur.urlopen = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("Vorschau: keine neue Aufnahme"))
    try:
        return _chatterbox_echt(name, text, ordner, ganz)
    except Exception:
        return None
    finally:
        ur.urlopen = alt


# 25.10.2026: always play the finished recordings (tutorial, events, hearing); never create new ones
stimme.chatterbox = _nur_vorhandene

ordner = tempfile.mkdtemp(prefix="eden_vorschau_")
echt = json.load(open(eden.CFG_PFAD, encoding="utf-8-sig"))
eden.CFG_PFAD = os.path.join(ordner, "eden-config.json")
eden.STAENDE = os.path.join(ordner, "spielstaende")
os.makedirs(eden.STAENDE)
json.dump(dict(echt, modul=arg("--modul", "eden_rise"), aktiv=None), open(eden.CFG_PFAD, "w", encoding="utf-8"))
eden.PORT = int(arg("--port", "8328"))


def mochis_setzen(z):
    """Tierstation: --mochis geier:2,hund:1 = so oft schon gefangen, zum Pruefen von Overlay, Handy und Field Book (01.11.2026)."""
    if "--mochis" in sys.argv:
        tiere = z.setdefault("mochis", {"tiere": {}, "begleiter": None, "halsbaender": 0, "versuch": {}, "koeder": None, "fund_tag": {}})["tiere"]
        for paar in arg("--mochis", "").split(","):
            tiere[paar.split(":")[0]] = {"seit": 1, "gesund_ab": 1, "gefuettert": True, "kaempfe": 0, "anzahl": int(paar.split(":")[1]), "zuletzt": -10}


def vorspulen(tag):
    """Bot aus lauf_test bis zum Morgen von <tag>, ohne Tagesarbeit (Missionen bleiben offen)."""
    import lauf_test as L
    stimme.chatterbox = _nur_vorhandene                # wie bei --anhoerung: lauf_test schaltet die Stimmen beim Import ab
    protokoll = {"schritte": [], "erledigt": {}}
    z = eden.aktion("neu", {"modus": "entspannt"})
    frei = "--frei" in sys.argv                        # Ortskapitel (26.10.2026): bis zur ersten freien Mittagsphase
    sturm = arg("--sturm", None)                           # Sturm an Tag 5 (27.10.2026): --tag 5 --sturm vorbereitung|nacht
    bis_event = arg("--bis-event", None)                   # Direkt vor ein Event (01.11.2026): --tag 20 --bis-event bl_kriegsrat
    while z["status"] != "ende" and not (bis_event and z["status"] == "ereignis" and (z.get("event") or {}).get("id") == bis_event) and not (sturm and z["status"] == "sturm" and eden.sturm.aktiv(z)["teil"] == sturm) and not (
            not sturm and not bis_event and z["tag"] >= tag and z["status"] == "wahl" and (
            not frei or z["phase"] in ("tag", "nachmittag") and not eden.plan.aktionen(z))):
        a = L.schritt(z, protokoll)
        if a is None:
            break
        if a[0] != "_tagesarbeit":
            try:
                eden.aktion(*a)
            except ValueError:
                pass
        z = eden.aktiv()
    for teil in [i for i in arg("--inventar", "").split(",") if i]:      # Stapeln (28.10.2026): plaster:4 = vier Stueck
        iid, _, n = teil.partition(":")
        if n or iid not in z["inventar"]:
            z["inventar"] += [iid] * int(n or 1)
    if "--energie" in sys.argv:                        # Jobkarte ohne Energie ansehen (29.10.2026): --energie 0
        z["werte"]["energie"] = int(arg("--energie", "0"))
    if "--album" in sys.argv:                          # Album ansehen (31.10.2026): ein paar Blaetter von Rosi und Lea
        z["album"] = [{"art": "szene", "wer": "rosi", "tag": 3, "titel": "Nothing's Broken", "stufe": 1},
                      {"art": "selfie", "wer": "rosi", "tag": 5, "titel": "Grease", "bild": "rosi_generatorraum_1", "stufe": 3},
                      {"art": "szene", "wer": "rosi", "tag": 9, "titel": "Nobody Lost", "stufe": 2},
                      {"art": "szene", "wer": "lea", "tag": 4, "titel": "Stay Together", "stufe": 1}]
    if "--konto" in sys.argv:
        z["konto"] = int(arg("--konto", "0"))
    if "--rast" in sys.argv:                           # Angelplatz am Bach ansehen (27.10.2026): --rast kl_bachufer
        z.setdefault("rast_gefunden", []).extend(r for r in arg("--rast", "").split(",") if r)
    if "--attributpunkte" in sys.argv:                 # Lob ansehen (27.10.2026): freie Attributpunkte, z. B. --attributpunkte 3
        kampf.progress(z)["attributpunkte"] = int(arg("--attributpunkte", "0"))
    z["flags"] += [f for f in arg("--flags", "").split(",") if f and f not in z["flags"]]   # z. B. kloster_angenommen
    for paar in [x for x in arg("--flagtag", "").split(",") if x]:   # datierte Flags, z. B. --flagtag rt_ende_tag:10 (Danzels Laden)
        z.setdefault("flag_tag", {})[paar.split(":")[0]] = int(paar.split(":")[1])
    mochis_setzen(z)
    if "--event" in sys.argv:                          # Szene direkt ansehen (31.10.2026): --event rm_r4
        eden.ereignisse.ort_oeffnen(z, eden.modul_laden(), eden.moddir(z["modul"]), arg("--event", ""))
        z["event"]["weiter"], z["event"]["status_vorher"], z["status"] = "wahl", z["status"], "ereignis"
        ev = eden.ereignisse.daten(eden.moddir(z["modul"]))["_index"][arg("--event", "")]
        if ev["personen"].get("selfie"):               # wie ereignisse._setzen: das Foto gehoert zum Selfie-Event (03.11.2026)
            z["event"]["selfie"] = eden.ereignisse.selfie_bild(z, ev["personen"]["selfie"])
            eden.ereignisse.album.merken(z, ev, z["event"]["selfie"])
    if "--an-land" in sys.argv:                        # Laeden im Dorf offen, als waere Duc heute an Land gewesen
        z.setdefault("heute", []).append({"ort": "alvas_bar", "phase": "tag", "titel": "Alva's Bar", "kurz": "", "folgen": [], "art": "besuch", "id": "vorschau", "tag": z["tag"], "anwesend": []})
    if "--ort-weg" in sys.argv:                        # Ortskapitel testen (26.10.2026): direkt an einem Frame starten,
        from kern import expedition                    # z. B. --ort-weg kl_start,kl_bruecke,kl_huette (letzter = offen;
        weg = [x for x in arg("--ort-weg", "").split(",") if x]          # die davor gelten als besiegt)
        modul = eden.modul_laden()
        z["ort_aktiv"] = arg("--ort", "macchia")
        expedition.starten(z, "kloster")
        for eid in weg:
            eden.ort_frame(z, modul, eid)
        z["ort_besiegt"] = weg[:-1]
    if "--werkzeug" in sys.argv:                       # Abbauen testen (28.10.2026): z. B. --werkzeug axe:1,pickaxe:3
        for teil in [x for x in arg("--werkzeug", "").split(",") if x]:
            wid, _, st = teil.partition(":")
            eden.kuechen.kueche(z).setdefault("werkzeug", {})[wid] = int(st or 1)
    if "--rohstoffe" in sys.argv:                      # Koeder bauen (30.10.2026): z. B. --rohstoffe cork:4,feather:5,iron:3,timber:3
        for teil in [x for x in arg("--rohstoffe", "").split(",") if x]:
            rid, _, n = teil.partition(":")
            eden.kuechen.rohstoff_add(z, rid, int(n or 1))
    if "--fische" in sys.argv:                         # Petru kauft Fisch (28.10.2026): z. B. --fische zander:2,sardine:3 (Vorrat + Journal)
        modul = eden.modul_laden()
        for teil in [x for x in arg("--fische", "").split(",") if x]:
            fid, _, n = teil.partition(":")
            eden.kuechen.fang(z, modul, fid, int(n or 1))
            eden.kuechen.kueche(z).setdefault("fischbuch", {})[fid] = {"n": int(n or 1), "bester": 2}
    if "--chips" in sys.argv:                                           # Upgrade-Fenster ansehen (25.10.2026): Werkstatt offen, Chips und Ausruestung
        defs = kampf.daten(eden.moddir(z["modul"]))
        z["flags"].append("werkstatt_offen")
        for sl, i in (("weapon", "bat"), ("weapon", "spear"), ("weapon", "gun"), ("armor", "jacket_water")):
            kampf.freischalten(z, defs, sl, i)
        for f, st in (("wucht", 2), ("praezision", 1), ("technik", 3), ("zustand_blutend", 1), ("element_feuer", 2), ("schutz", 2),
                      ("parade", 1), ("abwehr_brennend", 3), ("auftritt", 1)):
            kampf.chip_finden(z, defs, f, st)
        kampf.werkstatt(z)["stufen"]["weapon:bat"] = 1
        kampf.chip_einsetzen(z, defs, "weapon", "bat", "wucht")
        kampf.chip_einsetzen(z, defs, "armor", "jacket_earth", "schutz")
    for jid in [i for i in arg("--erfolg", "").split(",") if i]:      # z. B. Vorgaenger einer Kette als geschafft
        z["jobs_erledigt"].append(jid)
        z.setdefault("jobs_erfolg", []).append(jid)
    if "--angebot" in sys.argv:                                         # Tagesangebot festlegen (Wege einer Gruppe dazu)
        jobs = eden.showrunner.vorrat(eden.moddir())["jobs"]
        ids = []
        for jid in arg("--angebot", "").split(","):
            g = next((j.get("gruppe") for j in jobs if j["id"] == jid), None)
            ids += [j["id"] for j in jobs if j["id"] == jid or (g and j.get("gruppe") == g)]
        z["jobs_tag"] = {"tag": z["tag"], "ids": list(dict.fromkeys(ids))}
    for eintrag in [i for i in arg("--vorliebe", "").split(",") if i]:   # figur:item:mag|mag_nicht[:gelesen]
        teile = eintrag.split(":")
        e = eden.vorlieben.entdecken(z, eden.modul_laden(), teile[0], teile[1], teile[2] if len(teile) > 2 else "mag", "geschenk")
        if e and "gelesen" in teile:
            e["gelesen"] = e["gemeldet"] = True
    for fid in [i for i in arg("--favour-journal", "").split(",") if i]:  # Favours (29.10.2026): Journal fuellen, z. B.
        z.setdefault("favours", []).append({"id": fid, "weg": "Preview", "ausgang": "ok"})   # fv_lola_1,fv_lola_dank
    if arg("--favour", None):                          # eine Bitte offen im Handy, z. B. --favour fv_lola_1
        d = eden.ereignisse.daten(eden.moddir())
        z["status"] = "ereignis"
        eden.ereignisse._setzen(z, eden.ereignisse.stand(z), d["_index"][arg("--favour", None)])
    eden.sichern(z)
    import copy
    eden.TEST_START = copy.deepcopy(z)                 # Knopf "Restart day (test)" springt an den Anfang dieses Tages zurueck
    print("[Vorschau] vorgespult: Tag %d, %s, Konto %s, Inventar %s" % (z["tag"], z["status"], z.get("konto"), z["inventar"]))


# Startstand je Begegnung (Duc 29.10.2026): so steht Duc im echten Spiel an dieser Stelle (Gate-Bot, Seed 7) - sonst
# kaempft die Vorschau mit dem nackten Neustart (Schrubber, ohne Mistral) und taeuscht. --kampf-level/--skills/--waffe
# ueberschreiben wie bisher. lektion 2 = Maxwells erste Lektion vorbei, Mistral beigebracht (kern/tutorial.py LEHRT).
STARTSTAND = {
    "hafen_ratten": {"level": 1, "flags": ["waffe_bat"], "lektion": 2},
    "hafen_hunde": {"level": 1, "flags": ["waffe_bat"], "lektion": 2},
    "hafen_keiler": {"level": 2, "flags": ["waffe_bat"], "lektion": 2},   # Ratten + Hunde bringen den Aufstieg
}


def startstand(z, bid):
    s = STARTSTAND.get(bid)
    if not s:
        return
    z["flags"] += [f for f in s.get("flags", []) if f not in z["flags"]]
    if s.get("lektion"):
        eden.tutorial.stand(z)["lektion"] = max(eden.tutorial.stand(z)["lektion"], s["lektion"])
        eden.tutorial.stand(z)                         # bringt Mistral bei
    c = kampf.progress(z)
    if s.get("level", 1) > c["level"]:
        c["attributpunkte"] += (s["level"] - c["level"]) * kampf.ATTR_POINTS_PER_LEVEL
        c["level"], c["xp"] = s["level"], 0
    kampf.lp_auffuellen(z)
    print("[Vorschau] Startstand %s: Level %d, Waffe %s, Spezial %s" % (
        bid, c["level"], kampf.aktive_waffe(z, kampf.daten(eden.moddir(z["modul"]))), kampf.known(z)))


def kampf_testen(bid):
    """--kampf <begegnung>: neuer Durchlauf, Persona gewaehlt, direkt im Kampf (Etappe 3, 19.10.2026)."""
    z = eden.aktion("neu", {"modus": "entspannt"})
    z = eden.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = eden.aktion("prolog", {})
    for iid in [i for i in arg("--inventar", "multitool,verbandskasten").split(",") if i]:
        if iid not in z["inventar"]:
            z["inventar"].append(iid)
    startstand(z, bid)
    if any(a in sys.argv for a in ("--kampf-level", "--skills", "--waffe", "--ruestung")):   # test switch (24.10.2026)
        defs = kampf.daten(eden.moddir(z["modul"]))
        kampf.test_setup(z, defs, level=int(arg("--kampf-level", "1")) if "--kampf-level" in sys.argv else None,
                         skills=kampf.by_code(defs, arg("--skills", "").split(",")) if "--skills" in sys.argv else None,
                         weapon=arg("--waffe", None), armor=arg("--ruestung", None))
    if "--lektion" in sys.argv:                        # Maxwell-Lektion vorgeben (26.10.2026); ab 2 ist Mistral beigebracht
        eden.tutorial.stand(z)["lektion"] = int(arg("--lektion", "1"))
        eden.tutorial.stand(z)
    mochis_setzen(z)
    z["flags"] += [f for f in arg("--flags", "").split(",") if f and f not in z["flags"]]
    for paar in [x for x in arg("--flagtag", "").split(",") if x]:
        z.setdefault("flag_tag", {})[paar.split(":")[0]] = int(paar.split(":")[1])
    eden.kampf_starten(z, eden.modul_laden(), bid)
    defs = kampf.daten(eden.moddir(z["modul"]))
    k = z["kampf"]
    if (k["spieler"].get("weapon") or {}).get("id") == defs.get("fallback_weapon") and not k["def"].get("weapon"):
        k["vorschau_hinweis"] = ("Preview: Duc owns no weapon here and fights with the fallback scrubber. "
                                 "In the real game he holds his weapon by now - add --waffe or a start state.")
    eden.sichern(z)
    print("[Vorschau] Kampf %s gestartet, Inventar %s%s" % (bid, z["inventar"],
                                                            " - ACHTUNG Fallback-Schrubber" if k.get("vorschau_hinweis") else ""))


def realistische_fakten(z):
    """--realistisch (25.10.2026): Fakten, die man ohne Umweg findet - in einer festen Story-Szene, in der die Person
    anwesend ist bzw. die am Ort spielt (Fragen, Untersuchen, Sichern - auch die, die 1 Aktion kosten), dazu
    Erinnerungen ohne Bedingung. Keine Handy-Fragen: so viel hat ein aufmerksamer Spieler am Tag 7."""
    st = eden.ermittlung._story(z) or {}
    bu = json.load(open(os.path.join(eden.moddir(), "buehne.json"), encoding="utf-8"))["szenen"]
    szenen = []
    for t, d in st.get("wochenbogen", {}).items():
        for ph, xs in d["phasen"].items():
            for x in xs:
                b = bu.get(x["id"], {})
                szenen.append((int(t), ph, x.get("ort") or b.get("ort"),
                               {p for p in (x.get("personen") or b.get("anwesend") or []) if not p.startswith("$")}))
    out = []
    for fid, f in eden.ermittlung.fakten(z).items():
        for w in f["wege"]:
            a, b = w["tage"]
            if w["art"] == "erinnerung" and not w.get("bedingung"):
                out.append(fid)
                break
            if w["art"] in ("befragen", "untersuchen", "sichern") and any(
                    a <= t <= b and (not w.get("phasen") or ph in w["phasen"])
                    and ((w.get("person") and w["person"] in pers) or (not w.get("person") and w.get("ort") == ort))
                    for t, ph, ort, pers in szenen):
                out.append(fid)
                break
    return out


def anhoerung_testen():
    """--anhoerung: per Bot bis zur Verhandlung an Tag 7 (Variante B, 25.10.2026); --alles-wissen legt alle Fakten auf
    die Hand (viele Karten zum Ansehen); --fall N erzwingt einen Fall."""
    import lauf_test as L
    stimme.chatterbox = _nur_vorhandene                # lauf_test schaltet die Stimmen beim Import ab - hier wieder an
    protokoll = {"schritte": [], "erledigt": {}}
    z = eden.aktion("neu", {"modus": "entspannt"})
    if "--fall" in sys.argv:                           # bestimmten Fall erzwingen (z. B. 1 = Fall mit eigenen Aussagen)
        z["wahrheit"] = "fall_%s" % arg("--fall", "1")
        eden.sichern(z)
    while z["status"] not in ("ende", "verhandlung"):
        a = L.schritt(z, protokoll)
        if a is None:
            break
        if a[0] != "_tagesarbeit":
            try:
                eden.aktion(*a)
            except ValueError:
                pass
        z = eden.aktiv()
    if "--alles-wissen" in sys.argv:
        for fid in eden.ermittlung.fakten(z):
            eden.ermittlung._lernen(z, fid, "vorschau")
    elif "--realistisch" in sys.argv:                  # was ein aufmerksamer Spieler in den Story-Szenen findet
        for fid in realistische_fakten(z):
            eden.ermittlung._lernen(z, fid, "vorschau")
    eden.sichern(z)
    import copy
    eden.TEST_START = copy.deepcopy(z)                 # Knopf "Restart" in der Anhoerung springt hierher zurueck
    print("[Vorschau] Anhoerung: Tag %d, %s" % (z["tag"], z["status"]))


def taktik_testen():
    """--taktik: neuer Durchlauf, direkt auf der Taktik-Karte der Belagerung (Duc 31.10.2026). --flags kl_loewe_frei fuer Mochi."""
    z = eden.aktion("neu", {"modus": "entspannt"})
    z = eden.aktion("persona", {"index": 0})
    if z["status"] == "prolog":
        z = eden.aktion("prolog", {})
    z["flags"] += [f for f in arg("--flags", "waffe_bat").split(",") if f and f not in z["flags"]]
    kampf.test_setup(z, kampf.daten(eden.moddir(z["modul"])), level=int(arg("--kampf-level", "12")))     # so stark wie um Tag 21 (geschaetzt)
    td = eden.taktik.daten(eden.moddir(z["modul"]))
    for q in list(td["hilfe"].items()) + list(td["reserve"].items()):        # alle Hilfstruppen und Trupps verdient
        z["werte"]["vertrauen." + q[1].get("pid", q[0])] = 5
    z["flags"].append("rt_ausgang_alle")
    if arg("--taktik-art", "") in ("bericht", "flicken"):   # Der Morgen danach (Duc 01.11.2026): mit Schaeden zum Anschauen
        z["tag"] = 22
        eden.belagerung.stand(z).update(kaputt=["South", "West"], fertig=2, tag=21, einheiten={}, reserve=[], aufstellung={},
                                        t={"kirche": 1, "kirche_max": 3, "yacht": 2, "hilfe": ["holm"], "hilfe_genutzt": {}, "gesehen": [], "duo_gesehen": [], "rueckspruenge": 2, "haeuser": {"bar": {"status": "verloren"}}})
        eden.kuechen.rohstoff_add(z, "timber", 9)
        eden.kuechen.rohstoff_add(z, "slate", 3)
    eden.taktik.beginnen(z, eden.moddir(z["modul"]), art=arg("--taktik-art", None))   # manoever, echt, bericht oder flicken: wie im Kalender
    if arg("--taktik-welle", ""):                     # direkt in eine spaetere Welle, zum Pruefen
        nr, t = int(arg("--taktik-welle", "")), z["taktik"]
        t["welle_vorher"] = nr - 1
        eden.taktik._posten_anpassen(t, td)
        eden.taktik.briefing_setzen(z, td)
    if "--maxwell-kampf" in sys.argv:                 # direkt in Maxwells echten Kampf (Duc 01.11.2026): --maxwell-kampf agent|brute|roboter|hund|pirat|drohne
        md, t = eden.moddir(z["modul"]), z["taktik"]
        eden.taktik.start_schlacht(z, md)
        while t["phase"] == "szene":
            eden.taktik.szene_weiter(z, md)
        mx = eden.taktik._e(t, "maxwell")
        feind = eden.taktik._einheit("vorschau", arg("--maxwell-kampf", "agent"), "schwarz", td["feinde"][arg("--maxwell-kampf", "agent")], mx["x"] + 1, mx["y"])
        t["einheiten"].append(feind)
        kampf_id = eden.taktik.angreifen(z, md, "maxwell", feind["id"])["kampf"]
        kampf.starten(z, eden.taktik.kampf_defs(z, md), kampf_id, rueckkehr={"status": "taktik"}, held=eden.taktik.held_start(z, md))
        z["status"] = "kampf"
    eden.sichern(z)
    print("[Vorschau] Taktik-Karte, Status", z["status"])


if "--anhoerung" in sys.argv:
    anhoerung_testen()
elif "--taktik" in sys.argv:
    taktik_testen()
elif "--tag" in sys.argv:
    vorspulen(int(arg("--tag", "3")))
elif "--kampf" in sys.argv:
    kampf_testen(arg("--kampf", "hafen_dieb_test"))
if "--no-browser" not in sys.argv:
    sys.argv.append("--no-browser")
try:
    eden.main()
finally:
    shutil.rmtree(ordner, ignore_errors=True)

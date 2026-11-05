# -*- coding: utf-8 -*-
"""
Eden - Spiel-Engine fuer das Eden-RPG (Port 8308). Engine-Kern seit 12.10.2026.

Die Engine ist der Server, die Oberflaeche haengt nur dran (client\\index.html = Textclient; spaeter VN-Client).
Regeln und Spielstand leben hier im Code, das Sprachmodell (Giftige Blume in KoboldCpp, Port 5010) spielt nur.
Tagesplaene kommen vom Showrunner: module\\<modul>\\plaene\\tag<N>.json (zurzeit Claude im Chat, spaeter API).

  Ablauf:  Persona waehlen -> Plan laden (pruefen) -> je Phase eine Szene (Pflicht) oder Auswahl (Wahl)
           -> Szene spielen (Probe, Regie, Richter, Empathy-Gedanken, Ereignis, Sanduhr) -> Szenenende
           (Ausgaenge, Folgen, Gedaechtnis) -> naechste Phase -> Tagesende (Uhren) -> naechster Plan
  Speichern: nach jedem Zug (spielstaende\\<id>.json); Modus "entspannt" erlaubt Szene neu starten.

Start: Start-Eden.bat   (ComfyUI-Python, keine Installation)
"""
import base64, copy, json, os, random, re, sys, threading, time, traceback, unicodedata, urllib.parse, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from kern import buehne, handy, hauptstory, llm, plan, regeln, stimme, szene, zustand  # noqa: E402
from kern import handel, showrunner, chronik, gesten, wuerfel, kabine, ermittlung, abschluss, ereignisse, vorlieben, rollen
from kern import kampf  # noqa: E402
from kern import tutorial  # noqa: E402
from kern import anhoerung  # noqa: E402
from kern import akt3, aufbau, belagerung, kommission, meta, post, taktik  # noqa: E402
from kern import album  # noqa: E402
from kern import sturm  # noqa: E402
from kern import expedition  # noqa: E402
from kern import wegpunkte  # noqa: E402
from kern import taschendieb  # noqa: E402
from kern import moral  # noqa: E402
from kern import legenden  # noqa: E402
from kern import lob  # noqa: E402
from kern import figurenrahmen  # noqa: E402
from kern import tisch  # noqa: E402
from kern import abbau, angeln, farm, koeder, kuechen, mochis, schiessen, schneider  # noqa: E402
from kern import auftraege  # noqa: E402
from kern import wuerfel_anzeige, musik, sfx

PORT = 8308
CFG_PFAD = os.path.join(BASE, "eden-config.json")
STAENDE = os.path.join(BASE, "spielstaende")
TEST_START = None          # Spielstand-Kopie, auf die der Vorschau-Server mit "test_neustart" zurueckspringt (nie im Spiel)
PROFIL = os.path.join(BASE, "profil")          # Ducs Profilbild (17.10.2026) - persoenlich, nicht im Git
LOCK = threading.Lock()


_DATEI_CACHE = {}       # Pfad -> (mtime, Inhalt): /api/stand wird waehrend jeder Aktion sekuendlich abgefragt


def _json_gecacht(pfad, encoding="utf-8"):
    st = os.path.getmtime(pfad)
    alt = _DATEI_CACHE.get(pfad)
    if not alt or alt[0] != st:
        alt = _DATEI_CACHE[pfad] = (st, json.load(open(pfad, encoding=encoding)))
    return alt[1]


def cfg():
    # Kopie: Aufrufer veraendern die Konfiguration vor cfg_setzen
    return copy.deepcopy(_json_gecacht(CFG_PFAD, "utf-8-sig"))


def cfg_setzen(**kw):
    c = cfg()
    c.update(kw)
    json.dump(c, open(CFG_PFAD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def moddir(mid=None):
    return os.path.join(BASE, "module", mid or cfg()["modul"])


def modul_laden(mid=None):
    """Gemeinsames, nur lesend genutztes Objekt (wie showrunner.vorrat) - neu geladen, sobald die Datei sich aendert."""
    modul = _json_gecacht(os.path.join(moddir(mid), "modul.json"))
    rollen.anmelden(modul)                  # Wert-Aliase fuer regeln.gilt (Draht = Vertrauen des Haendlers)
    return modul


def aktiv():
    rid = cfg().get("aktiv")
    if rid and os.path.exists(os.path.join(STAENDE, rid + ".json")):
        z = zustand.laden(STAENDE, rid)
        modul = modul_laden(z.get("modul"))
        rollen.romanze_abgleichen(z, modul)
        meta.flags_setzen(z, STAENDE)          # Akt 3: gesehene Enden aus anderen Durchlaeufen (geheimes Ende ★)
        if zustand.angleichen(z, modul):       # alter Spielstand -> ans aktuelle Modul anpassen, einmal sichern
            handel.init(z, modul)
            zustand.speichern(STAENDE, z)
        return z
    return None


def sichern(z):
    zustand.speichern(STAENDE, z)


# ------------------------------------------------------------------ Ablauf
def weiter(z, modul, r):
    """r = Ergebnis von plan.phase_beginnen/naechste_phase."""
    nachrichten = lob.handy_faellig(z, modul)          # Lob einer Figur aufs Handy, wenn kein Treffen sie ausgespielt hat (27.10.2026)
    if nachrichten:
        z["meldungen"].append({"titel": "New message", "folgen": nachrichten, "kurz": ""})
    while True:
        if (r.startswith("szene:") or r == "wahl") and event_ziehen(z, modul, r):
            return                                    # erst das Ereignis, danach geht die Phase weiter (B5)
        if (r == "wahl" or r.startswith("szene:frei_")) and ereignisse.gesperrt_durch_story(z, modul, z["phase"]):
            r = plan.naechste_phase(z, modul)         # Belagerung: keine freie Zeit, keine Vespa-Gespraeche mitten im Krieg (Duc 01.11.2026)
            continue
        if r.startswith("szene:"):
            szene_starten(z, modul, plan.szene_nach_id(z, r[6:]))
            return
        if r == "wahl":
            return
        if r == "leer":                               # Phase ohne spielbare Szene (Hauptstory) -> weiter
            if event_ziehen(z, modul, r):             # Tag 0: Prolog-Begegnungen in einer Phase ohne Szene
                return
            r = plan.naechste_phase(z, modul)
            continue
        if r == "tagesende":
            zeilen = plan.tagesende(z, modul)
            zeilen += werkstatt_morgen(z, modul)       # Rosis fertiges Stueck + ihre Nachricht (25.10.2026)
            zeilen += farm.tagesbeginn(z, modul)       # Ernte, Eier/Trueffel/Milch, Geburten bei Nonna (27.10.2026)
            zeilen += handel.tagesende(z, modul)      # Honorar, Hehlerei, Schmuggel (16.10.2026)
            zeilen += ereignisse.tagesende(z, modul, moddir(z["modul"]))    # Bordregeln, Versprechen (B5)
            zeilen += legenden.tagesende(z, modul, moddir(z["modul"]), zustand.folgen_anwenden)   # Dorf redet (30.10.)
            zeilen += aufbau.tag_vorbei(z)              # Akt 3: Piraten bauen nachts, was Duc geliefert hat (04.11.2026)
            zeilen += akt3.morgen(z)                    # Akt 3: Kevin auf dem Dach, Dank heiler Haeuser, die Legion
            zeilen += post.morgen(z)                    # Akt 3: Mina bringt aus Bastia, was Duc bestellt hat (kern/post.py)
            auftraege.tagesbeginn(z, moddir(z["modul"]))   # seit wann ein Ort offen ist (Erinnerung, 02.11.2026)
            if z["status"] != "ende":
                zeilen += moral.morgen(z, modul)          # Crew-Stimmung: Verfall, Fruehstueck, Geschenk (27.10.2026)
            z["meldungen"].append({"titel": "Day %d is over" % (z["tag"] - 1), "folgen": zeilen, "kurz": "", "tag_ende": True})
            if z["status"] == "ende":
                z["abschluss"] = abschluss.berechnen(z, modul)      # Hauptstory: Ende aus den Entscheidungen (B4)
                if (z["abschluss"] or {}).get("akt") == 3 and z["abschluss"].get("ende"):
                    meta.ende_merken(STAENDE, z["abschluss"]["ende"])   # fuer das geheime Ende ★ im naechsten Durchlauf
                return
            if not plan.plan_laden(z, modul, moddir(z["modul"])):
                return
            r = plan.phase_beginnen(z)


def werkstatt_morgen(z, modul):
    """Rosi hat ueber Nacht ein Stueck fertig: Stufe setzen, feste Nachricht in ihren Handy-Faden. -> Zeilen."""
    defs = kampf.daten(moddir(z["modul"]))
    fertig = kampf.werkstatt_morgen(z, defs) if defs else None
    if not fertig:
        return []
    if fertig["text"] and "rosi" in modul["personen"]:
        f = handy.faden_von(z, "rosi")
        f["tag"], f["phase"], f["gelesen"], f["chips"] = z["tag"], z["phase"], False, []
        f["verlauf"].append(handy._zeile(z, "rosi", fertig["text"]))
    name = defs["weapons" if fertig["slot"] == "weapon" else "armors"][fertig["id"]]["label"]
    return ["📱 Message from Rosi: %s is ready (level %d)." % (name, fertig["stufe"])]


def farm_aktion(z, modul, name, daten):
    """Aktionen im Farm-Fenster bei Nonna (27.10.2026, E-079). Keine Phase, keine Aktion. -> Zeilen fuer eine Meldung (meist leer)."""
    if name == "garten_pflanzen":
        farm.garten_pflanzen(z, modul, int(daten.get("beet", -1)), daten.get("pflanze") or "")
    elif name == "stall_kaufen":
        farm.stall_kaufen(z, modul, daten.get("art") or "")
    elif name == "stall_ausbauen":
        farm.stall_ausbauen(z, modul, daten.get("art") or "")
    elif name == "tier_kaufen":
        farm.tier_kaufen(z, modul, daten.get("art") or "")
    elif name == "tier_benennen":
        farm.tier_benennen(z, modul, daten.get("art") or "", int(daten.get("id", -1)), daten.get("name"))
    elif name == "tier_schlachten":
        return farm.tier_schlachten(z, modul, daten.get("art") or "", int(daten.get("id", -1)))
    elif name == "nonna_kaufen":
        kuechen.nonna_kaufen(z, modul, daten.get("id") or "", daten.get("n") or 1)
    elif name == "nonna_verlassen":                   # Frederico bringt den Einkauf rueber (fester Satz fred.<n>, vertont)
        i = kuechen.nonna_verlassen(z, modul)
        if i is not None:
            kuechen.kueche(z)["fred"] = i
        los_beim_besuch(z, modul, "nonna")            # Akt 3: der Garten mit Nonna und Isabelle
    elif name == "baustelle_liefern":                # Akt 3: Baustoffe fuer die naechste Stufe (kern/aufbau.py)
        aufbau.liefern(z, daten.get("haus") or "")
    elif name == "post_bestellen":                   # Akt 3: Minas Fahrt nach Bastia, Wahl aus drei, keine Phase (kern/post.py)
        post.bestellen(z, daten.get("wahl") or "")
    elif name == "fred_gehoert":
        (z.get("kueche") or {}).pop("fred", None)
    return []


def kuechen_ansicht(z, modul):
    """Vorrat, Tagesbonus, Nonnas Laden und das Farm-Fenster fuer den Client (nur lesen)."""
    d = kuechen.daten(modul)
    mid = z["modul"]
    vorrat = kuechen.vorrat_ansicht(z, modul)
    for x in vorrat:
        x["bild"] = item_bild(mid, x["id"], z)
    n = kuechen.nonna_ansicht(z, modul)
    if n:
        for w in n["waren"]:
            w["bild"] = item_bild(mid, w["id"], z)
    fred = (z.get("kueche") or {}).get("fred")
    saetze = d.get("frederico") or []
    return {"vorrat": vorrat, "bonus": kuechen.bonus_ansicht(z, modul), "nonna": n, "farm": farm.ansicht(z, modul),
            "baustellen": aufbau.ansicht(z),
            "post": post.ansicht(z),
            "fred": {"id": "fred.%d" % fred, "text": saetze[fred]["text"]} if fred is not None and fred < len(saetze) else None,
            "essen_frei": handel.essen_frei(z, modul)}


def ort_frame(z, modul, eid):
    """Ortskapitel (26.10.2026): naechsten Frame der Kette oeffnen. Die Phase gehoert dem Ort, danach geht es zur Wahl."""
    ereignisse.ort_oeffnen(z, modul, moddir(z["modul"]), eid)
    weg = z.setdefault("ort_weg", [])                  # Mini-Karte im Expeditions-Bildschirm: was Duc schon gesehen hat
    if not weg or weg[-1] != eid:
        weg.append(eid)
    if (ereignisse.daten(moddir(z["modul"]))["_index"][eid]).get("sperre"):
        z["ort_sperre"] = len(weg) - 1                 # nach einer Entscheidung: hinter diesen Frame fuehrt kein Rueckweg
        z["ort_sperre_frame"] = eid                    # ... und keine Schnellreise davor (kern/wegpunkte.py, 29.10.2026)
    z["ort_frame"] = eid                               # Rast-Prinzip: welcher Frame gerade offen ist
    gefunden = z.setdefault("rast_gefunden", [])       # Fund-Einblendung beim ersten Erreichen eines Rastplatzes
    z["rast_fund_neu"] = eid not in gefunden
    if eid not in gefunden:
        gefunden.append(eid)
    z["event"]["weiter"], z["event"]["status_vorher"] = "wahl", "wahl"
    z["status"] = "ereignis"


def _rast_pruefen(z, modul):
    """Abbauen und Angeln unterwegs (28.10.2026): nur an einem offenen Rastplatz-Frame, vor einer Wahl, ohne laufenden Anruf."""
    offen = z.get("event") or {}
    roh = (ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {}).get(offen.get("id")) or {}
    if z["status"] != "ereignis" or not z.get("ort_aktiv") or roh.get("art") != "ort" or not roh.get("rast") or offen.get("ergebnis"):
        raise ValueError("Das geht nur an einem Rastplatz, vor einer Wahl.")
    if z.get("rast_anruf"):
        raise ValueError("Erst den Anruf beenden.")


def los_beim_besuch(z, modul, wo):
    """Akt 3: ein Festa-Los beim Besuch der Person, ohne Phase und ohne Ausflug (kern/akt3.los_besuch)."""
    eid = akt3.los_besuch(z, moddir(z["modul"]), wo) or akt3.szene_besuch(z, wo)
    if eid:
        ereignisse.ort_oeffnen(z, modul, moddir(z["modul"]), eid)
        z["event"]["weiter"], z["event"]["status_vorher"] = "wahl", "wahl"
        z["status"] = "ereignis"


def ort_aufraeumen(z):
    for k in ("ort_aktiv", "ort_ende", "ev_weiter", "ort_weg", "ort_frame", "ort_besiegt", "ort_rasten", "rast_anruf",
              "ort_sperre", "ort_start", "ort_sperre_frame"):
        z.pop(k, None)


def ort_beenden(z, modul):
    """Kette zu Ende (oder verloren): der Ausflug hat die ganze Phase gekostet."""
    ort_aufraeumen(z)
    z["status"] = "wahl"
    weiter(z, modul, plan.naechste_phase(z, modul))


def event_ziehen(z, modul, r):
    """Beim ersten Beginn einer Phase (Hauptstory): vielleicht ein Ereignis. True = Spiel wartet auf die Antwort."""
    if not (z.get("plan") or {}).get("_hauptstory"):
        return False
    e = ereignisse.stand(z)
    schl = "%d-%s" % (z["tag"], z["phase"])
    if e.get("phase_gezogen") == schl:
        return False
    e["phase_gezogen"] = schl
    if not ereignisse.ziehen(z, modul, moddir(z["modul"])):
        return False
    z["event"]["weiter"] = r
    z["event"]["status_vorher"] = z["status"]
    z["status"] = "ereignis"
    return True


def event_szene(z, modul, ev, sdef):
    """Ein Ereignis fuehrt in eine Szene (Abend mit Lola/Alva, Gespraech): frei gespielt, ersetzt die freie Phase."""
    pid = sdef.get("pid") or sdef.get("wer")
    if pid in ("wahl", None):
        pid = hauptstory.partner(z, modul) or rollen.rolle(modul, "partner_standard")
    anwesend = [p for p in hauptstory.frauen(modul) if not rollen.ist(modul, "nicht_in_crew_szene", p)][:3] \
        if pid == "crew" else [pid]
    ort = sdef.get("ort") or "duc_cabin"
    s = {"id": "ev_%s_t%d" % (ev["id"], z["tag"]), "titel": ev["titel"], "ort": ort, "anwesend": anwesend,
         "zeit": "", "ausgangslage": sdef.get("hinweis") or ev["titel"], "frage": "What happens now?",
         "figuren": {p: {"will": sdef.get("hinweis", "")} for p in anwesend}, "ausgaenge": [],
         "max_zuege": sdef.get("max_zuege", 8), "storylet": None, "improvisiert": True, "frei": True,
         "regie": sdef.get("hinweis", "")}
    if sdef.get("set") and pid in modul["personen"]:
        s["auftraege"] = {pid: {"set": sdef["set"]}}
    if sdef.get("art") == "intim" and pid in s["figuren"]:
        # Intim-Abend (Lola, Alva, Casanova): nicht die Nebenfiguren-Grenze "hoechstens Handschlag" (18.10.2026)
        s["figuren"][pid]["grenze"] = ("Adult, consensual intimacy is what both of them came for tonight. She leads as "
                                       "described, checks in with him in her own way, and either of them can stop at any time.")
    s = showrunner.figuren_fuellen(z, modul, {}, s)
    szene_starten(z, modul, s)
    if sdef.get("art") == "intim" and z.get("szene"):
        z["szene"]["intim_aktiv"] = pid


def phase_ueberspringbar(z):
    """Nur freie Karten duerfen verfallen, Story-Entscheidungen nie (Duc 01.11.2026)."""
    return all(str(o).startswith(("frei_", "date_")) for o in z.get("optionen") or [])


def szene_starten(z, modul, s):
    if z["modus"] == "entspannt":
        snap = copy.deepcopy(z)
        snap["_szene_id"] = s["id"]
        if s.get("anruf"):                  # Anruf aus der Kabine steht in keinem Plan - Definition mitsichern
            snap["_szene_def"] = s
        json.dump(snap, open(os.path.join(STAENDE, z["id"] + "_vor_szene.json"), "w", encoding="utf-8"), ensure_ascii=False)
    szene.starten(z, modul, s)
    if s.get("id") == "anhoerung" and ermittlung.aktiv(z) and z.get("szene"):
        # Variante B (25.10.2026): Die Anklage wird als Verhandlung gespielt statt als Auswahlmoment der Szene
        z["szene"]["wahlmoment_offen"], z["szene"]["wahlmoment_erledigt"] = False, True
        anhoerung.verhandlung_beginnen(z, modul)
        z["status"] = "verhandlung"
    if s.get("id") in sturm.SZENEN and z.get("szene") and sturm.beginnen(z, modul, moddir(z["modul"]), s["id"]):
        z["status"] = "sturm"                          # Sturm an Tag 5 im Stil der Anhoerung (27.10.2026), kern/sturm.py
    if s.get("id") == "lagerfeuer" and z.get("szene"):
        sturm.lagerfeuer_hinweise(z, modul, moddir(z["modul"]))      # die Crew spricht die Sturmnacht einmal an


def archivieren(z, archiv):
    ordner = os.path.join(STAENDE, z["id"])
    os.makedirs(ordner, exist_ok=True)
    datei = "tag%d_%s_%s.json" % (archiv["tag"], archiv["phase"], archiv["szene"])
    json.dump(archiv, open(os.path.join(ordner, datei), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def aktion(name, daten):
    modul = modul_laden()
    szene.CFG.clear()
    szene.CFG.update(cfg())
    zustand.STUFEN_ABSTAND = cfg().get("stufen_abstand", zustand.STUFEN_ABSTAND)   # 0 zum Testen der spaeten Szenen (Duc 31.10.2026)
    z = aktiv()
    if name == "neu":
        z = zustand.neu(modul, daten.get("modus", "ironman"))
        rollen.romanze_abgleichen(z, modul)
        handel.init(z, modul)
        cfg_setzen(aktiv=z["id"])
    elif z is None:
        raise ValueError("Kein Durchlauf aktiv - erst 'Neuer Durchlauf'.")
    elif name == "test_neustart":                     # nur Vorschau-Server (TEST_START gesetzt): zurueck zum Teststart
        if not TEST_START:
            raise ValueError("Neustart gibt es nur in der Testversion.")
        z.clear()
        z.update(copy.deepcopy(TEST_START))
    elif name == "persona":
        if z["status"] != "persona_wahl":
            raise ValueError("Persona ist schon gewaehlt.")
        p = daten.get("eigene") or modul["personas"][int(daten["index"])]
        zustand.persona_setzen(z, modul, p)
        if modul.get("prolog"):                 # erst die Lage erklaeren (Prolog), dann der erste Morgen
            z["status"] = "prolog"
        elif plan.plan_laden(z, modul, moddir(z["modul"])):
            weiter(z, modul, plan.phase_beginnen(z))
    elif name == "prolog":
        if z["status"] != "prolog":
            raise ValueError("Der Prolog ist schon vorbei.")
        if plan.plan_laden(z, modul, moddir(z["modul"])):
            weiter(z, modul, plan.phase_beginnen(z))
    elif name == "plan_laden":
        if z["status"] not in ("warte_auf_plan", "plan_fehler"):
            raise ValueError("Es wird gerade kein Plan erwartet.")
        if plan.plan_laden(z, modul, moddir(z["modul"])):
            weiter(z, modul, plan.phase_beginnen(z))
    elif name == "wahl":
        if z["status"] != "wahl" or daten["id"] not in z["optionen"]:
            raise ValueError("Diese Szene steht gerade nicht zur Wahl.")
        # Modell B: eine Szene braucht die ganze Phase (beide Aktionen). Ein zugesagtes Date geht auch nach einer Aktion.
        if plan.aktionen(z) and not daten["id"].startswith("date_"):
            raise ValueError("Für eine Szene brauchst du die ganze Phase – du hast schon eine Aktion verbraucht.")
        szene_starten(z, modul, plan.szene_nach_id(z, daten["id"]))   # Versetzt? Das prueft das Phasenende (showrunner)
    elif name == "ort_betreten":                      # Ortskapitel (26.10.2026): ein Ort statt einer Szene
        if z["status"] != "wahl" or daten.get("id") not in [o["id"] for o in auftraege.orte_frei(z, moddir(z["modul"]))]:
            raise ValueError("Dieser Ort steht gerade nicht offen.")
        if plan.aktionen(z):
            raise ValueError("Für einen Ausflug brauchst du die ganze Phase – du hast schon eine Aktion verbraucht.")
        ort_aufraeumen(z)
        z["ort_aktiv"] = daten["id"]
        z.setdefault("ort_zuletzt", {})[daten["id"]] = z["tag"]   # Erinnerung der Auftraggeberin (Bedingung ort_ruhe, 02.11.2026)
        z["ort_start"] = auftraege.start(z, moddir(z["modul"]), daten["id"])   # der Wegpunkt am Eingang (Schnellreise, 29.10.2026)
        ort_frame(z, modul, z["ort_start"])
    elif name == "kabine":                            # Kabine statt Szene (17.10.2026, nur mit modul["kabine"])
        kabine.betreten(z, modul, (showrunner.vorrat(moddir(z["modul"])) or {}).get("fixplan"))
    elif name == "kabine_zurueck":
        kabine.zurueck(z)
    elif name == "phase_beenden":                     # Modell B: freie Phase vorzeitig beenden (Rest-Aktion verfaellt)
        if z["status"] not in ("wahl", "kabine") or not phase_ueberspringbar(z):
            raise ValueError("Gerade ist keine freie Phase.")
        z["kabine"] = None
        weiter(z, modul, plan.naechste_phase(z, modul))
    elif name == "truhe":
        kabine.truhe(z, modul, daten.get("id") or "", daten.get("richtung") or "", int(daten.get("n") or 1))
    elif name == "kabine_ausruhen":
        titel, kurz, zeilen = kabine.ausruhen(z, modul)
        z["meldungen"].append({"titel": "🛏 " + titel, "kurz": kurz, "folgen": zeilen})
    elif name == "kabine_anruf":
        s = kabine.anruf_szene(z, modul, daten.get("an") or "", cfg())
        z["kabine"] = None
        szene_starten(z, modul, s)
    elif name == "zug":
        if z["status"] != "szene":
            raise ValueError("Gerade laeuft keine Szene.")
        text = (daten.get("text") or "").strip()
        if not text:
            raise ValueError("Leere Eingabe.")
        vorbei = szene.zug(z, modul, text)
        if not vorbei:
            from kern import orte
            orte.vorschlag(z, modul)                      # manchmal schlaegt sie ihren Ort vor (Duc 02.11.2026)
        sichern(z)
        if vorbei:
            szene_beenden(z, modul)
    elif name == "waehlen":
        if z["status"] != "szene" or not z["szene"].get("wahlmoment_offen"):
            raise ValueError("Gerade steht keine Entscheidung an.")
        vorbei = szene.waehlen(z, modul, int(daten["index"]))
        sichern(z)
        if vorbei:
            szene_beenden(z, modul)
    elif name == "ende":
        if z["status"] != "szene":
            raise ValueError("Gerade laeuft keine Szene.")
        szene_beenden(z, modul)
    elif name == "start_chip":                        # feste Antwort zum Szenenstart (Figurenrahmen, Duc 01.11.2026)
        sz = z.get("szene")
        chips = (sz or {}).get("start_chips") if z["status"] == "szene" else None
        if not chips:
            raise ValueError("Not possible right now.")
        chip = chips[int(daten["index"])]
        sz["chip_achse"] = chip["achse"]
        zeilen = figurenrahmen.chip_buchen(z, modul, sz["figuren"][0], chip)
        vorbei = szene.zug(z, modul, '"%s"' % chip["text"], probe=False, reaktion=False)
        if zeilen and z.get("szene"):
            z["szene"]["log"].append({"art": "folgen", "zeilen": zeilen})
        sichern(z)
        if vorbei:
            szene_beenden(z, modul)
    elif name == "nachfragen":                        # sie fragt, ob er noch da ist (Duc 01.11.2026)
        if z["status"] == "szene" and z.get("szene"):
            szene.nachfragen(z, modul)
            sichern(z)
    elif name == "verlassen":                         # Knopf an der Uhr, nach der Rueckfrage (Duc 01.11.2026)
        if z["status"] != "szene" or not z.get("szene") or not szene.verlassen_moeglich(z["szene"]):
            raise ValueError("Not possible right now.")
        szene.verlassen(z, modul)
        sichern(z)
    elif name == "schweigen":                         # Knopf an der Uhr: Duc sagt nichts, sie redet weiter; zaehlt als Zug (Duc 01.11.2026)
        if z["status"] != "szene" or not z.get("szene") or z["szene"].get("wahlmoment_offen"):
            raise ValueError("Not possible right now.")
        vorbei = szene.zug(z, modul, "(Duc says nothing and waits.)", probe=False, reaktion=False)
        sichern(z)
        if vorbei:
            szene_beenden(z, modul)
    elif name in ("geste", "zeit", "zeit_antwort", "intim"):     # Dating-Sim-Steuerung (16.10.2026)
        sz = z.get("szene")
        if z["status"] != "szene" or not sz or sz.get("wahlmoment_offen"):
            raise ValueError("Not possible right now.")
        if sz["def"].get("anruf"):
            raise ValueError("Im Anruf geht das nicht.")
        zug_fn = lambda text, probe, hinweis: szene.zug(z, modul, text, probe=probe if probe else False,
                                                        reaktion=False, hinweis=hinweis)
        vorbei, zeilen = False, []
        if name == "geste":
            vorbei, zeilen = gesten.ausfuehren(z, modul, daten["id"], daten["an"],
                                               lambda att, sg, extra: szene.feste_probe(z, modul, sz, att, sg, extra), zug_fn,
                                               ort=daten.get("ort"))
        elif name == "zeit":
            text, kat = gesten.zeit_vorschlag(z, modul, daten["an"], szene.figur_prompt(z, modul, sz, daten["an"]))
            szene.zeile_einfuegen(z, modul, sz, daten["an"], text, "joy")
        elif name == "zeit_antwort":
            vorbei = gesten.zeit_antwort(z, modul, bool(daten.get("ja")), zug_fn)
        else:
            vorbei = gesten.intim(z, modul, daten["tag"], daten["an"], zug_fn)
        if zeilen and z.get("szene"):
            z["szene"]["log"].append({"art": "folgen", "zeilen": zeilen})
        sichern(z)
        if vorbei:
            szene_beenden(z, modul)
    elif name in ("ermitteln", "widerspruch", "konfrontieren"):    # Hauptstory-Ermittlung (B3/B4, 17./18.10.2026)
        sz = z.get("szene") if z["status"] == "szene" else None
        if sz and sz.get("wahlmoment_offen"):
            raise ValueError("Erst die Entscheidung.")
        if name == "ermitteln":
            gelernt, hinweis, zeilen, phase_vorbei = ermittlung.ausfuehren(z, modul, daten.get("weg") or "", sz)
            _, _, w = ermittlung._weg_finden(z, daten.get("weg") or "")
            text = "(%s)" % (w or {}).get("text", "")
        elif name == "konfrontieren":
            if not sz:
                raise ValueError("Konfrontieren geht nur im Gespräch.")
            zeilen, hinweis = ermittlung.konfrontieren(z, modul, daten.get("id") or "", sz)
            gelernt, phase_vorbei = [], False
            ziel = (daten.get("id") or "").split(":", 1)[-1]
            text = "(Du nimmst den Vorwurf vor allen zurück.)" if (daten.get("id") or "").startswith("korrektur:") \
                else "(Du sagst %s auf den Kopf zu, was du vermutest.)" % szene.kurz(modul, ziel)
        else:
            if not sz:
                raise ValueError("Nachfragen geht nur im Gespräch.")
            gelernt, hinweis, zeilen = ermittlung.widerspruch_klaeren(z, modul, daten.get("id") or "",
                                                                      bool(daten.get("beschuldigen")), sz)
            phase_vorbei = False
            text = "(Das passt zeitlich nicht – du sprichst sie darauf an.)" if not daten.get("beschuldigen") else \
                "(Du wirfst ihr direkt vor, dass sie lügt.)"
        neu = ["🔎 " + g for g in gelernt] + zeilen
        if sz:
            vorbei = szene.zug(z, modul, text, probe=False, reaktion=False, hinweis=hinweis)
            if neu and z.get("szene"):
                z["szene"]["log"].append({"art": "ermittlung", "zeilen": neu, "handel": True})
            sichern(z)
            if vorbei or phase_vorbei:
                szene_beenden(z, modul)
        else:
            z["meldungen"].append({"titel": "Ermittlung", "kurz": text.strip("()"), "folgen": neu or ["Nichts Neues."]})
            if phase_vorbei and z["status"] in ("wahl", "kabine"):
                if not plan.aktion_verbrauchen(z):     # Modell B: 1 Aktion; nach der zweiten ist die Phase vorbei
                    z["kabine"] = None
                    weiter(z, modul, plan.naechste_phase(z, modul))
    elif name in ("event_wahl", "event_schliessen"):  # Ereignis-Bildschirme (B5, 18.10.2026)
        offen = z.get("event")
        if z["status"] != "ereignis" or not offen:
            raise ValueError("Gerade wartet kein Ereignis.")
        if name == "event_wahl":
            z.pop("ev_verjagen", None)
            if daten.get("verjagen"):                  # Chase them off (Duc 02.11.2026): only where the map offers it
                roh = (ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {}).get(offen["id"]) or {}
                opts = roh.get("optionen", [])
                i = int(daten["index"])
                info = expedition.wahl_info(z, kampf.daten(moddir(z["modul"])) or {}, opts[i], kampf_bild) if i < len(opts) else {}
                if not info.get("verjagbar") or z.get("ort_frame") in z.get("ort_besiegt", []):
                    raise ValueError("You can't chase this off.")
                z["ev_verjagen"] = True
            ereignisse.waehlen(z, modul, moddir(z["modul"]), int(daten["index"]),
                               lambda att, sg, extra: szene.feste_probe(z, modul, {"figuren": []}, att, sg, extra),
                               ort=daten.get("ort"))
        # Zweiter Takt ohne eigene Antwort (Romanzen-Leiter): kein Zwischenbildschirm, sonst reisst die Szene ab
        if name == "event_schliessen" or (z.get("ev_direkt") and not offen["ergebnis"].get("zeile")):
            if not offen.get("ergebnis"):
                raise ValueError("Erst antworten.")
            ev_taktik = z.get("ev_taktik")
            ev_kampf_id = z.get("ev_kampf") or ev_taktik
            if ev_kampf_id and not ev_taktik and z.get("ort_aktiv") and z.get("ort_frame") in z.get("ort_besiegt", []):
                z.pop("ev_kampf", None)                # Rast-Prinzip (26.10.2026): besiegt bleibt besiegt bis zur Rast
                ev_kampf_id = None
                z["meldungen"].append({"titel": "🌿 Quiet", "kurz": "The path is quiet. You beat what waited here.", "folgen": []})
            if z.pop("ev_verjagen", None) and ev_kampf_id and not ev_taktik and z.get("ort_aktiv"):
                z.pop("ev_kampf", None)                # Chase them off (Duc 02.11.2026): won without a fight
                z["meldungen"].append({"titel": "🏃 Chased off", "kurz": "",
                                       "folgen": kampf.verjagen(z, kampf.daten(moddir(z["modul"])), ev_kampf_id)})
                if z.get("ort_frame") and z["ort_frame"] not in z.setdefault("ort_besiegt", []):
                    z["ort_besiegt"].append(z["ort_frame"])     # quiet until the next rest, like a won fight
                ev_kampf_id = None
            z["event"] = None
            handy.event_ablegen(z, modul, (ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {}).get(offen["id"]), offen)   # Das Handy erinnert sich (Paket 3)
            z["status"] = offen.get("status_vorher") or "wahl"
            r = offen.get("weiter") or "wahl"
            fertig = auftraege.pruefen(z, modul, moddir(z["modul"]))
            if fertig:
                z["meldungen"].append({"titel": "📜 Auftrag", "kurz": "", "folgen": fertig})
            im_ort = z.get("ort_aktiv") and not ev_kampf_id     # Ortskapitel: mit Kampf geht es erst danach weiter
            nxt = ereignisse.weiter_ziel(z) if im_ort else None
            direkt = ereignisse.direkt_ziel(z)
            if nxt:
                ort_frame(z, modul, nxt)
            elif im_ort:
                ort_beenden(z, modul)
            elif direkt:                               # zweiter Takt einer Szene (Romanzen-Leiter, 31.10.2026)
                ereignisse.ort_oeffnen(z, modul, moddir(z["modul"]), direkt)
                z["event"]["weiter"], z["event"]["status_vorher"] = r, z["status"]
                z["status"] = "ereignis"
            elif not ev_kampf_id and ereignisse.pflicht_ziehen(z, modul, moddir(z["modul"]), nur_prolog=True):
                z["event"]["weiter"], z["event"]["status_vorher"] = r, z["status"]   # mit Kampf: erst der Kampf
                z["status"] = "ereignis"              # Tag 0: naechste Begegnung im Hangar direkt anschliessen
            elif not ev_kampf_id and not offen.get("szene") and (z.get("plan") or {}).get("_hauptstory") \
                    and ereignisse.ziehen(z, modul, moddir(z["modul"])):
                z["event"]["weiter"], z["event"]["status_vorher"] = r, z["status"]   # naechste Stufe derselben Phase
                z["status"] = "ereignis"              # (Bordrat -> Zufall -> Handy, 25.10.2026)
            elif r == "leer":
                weiter(z, modul, plan.naechste_phase(z, modul))
            elif not offen.get("szene") and not z.get("schiessen_folgt") and (r == "wahl" or r.startswith("szene:frei_")) \
                    and ereignisse.gesperrt_durch_story(z, modul, z["phase"]):   # Holms Wette: nach der Intro-Szene startet das Spiel
                if ev_taktik:                          # Die Karte oeffnet unten, sie verbraucht die Phase
                    z["status"] = "wahl"
                else:
                    weiter(z, modul, plan.naechste_phase(z, modul))
            elif offen.get("szene") and (r == "wahl" or r.startswith("szene:frei_")):
                # Abend/Gespraech ersetzt die freie Phase - auch eine geplante freie Szene, nie eine Story-Szene
                # (27.10.2026: vorher lief nach "Lets her in" die geplante freie Szene statt des Abends)
                ev = ereignisse.daten(moddir(z["modul"]))["_index"][offen["id"]]
                event_szene(z, modul, ev, offen["szene"])
            elif r.startswith("szene:"):
                szene_starten(z, modul, plan.szene_nach_id(z, r[6:]))
            else:
                z["status"] = "wahl"
            if z.pop("ev_taktik", None) and z["status"] == "wahl":
                taktik.beginnen(z, moddir(z["modul"]), art=ev_taktik)
            if z.pop("ev_kampf", None) and z["status"] == "wahl":
                kampf_starten(z, modul, ev_kampf_id)
    elif name in ("chip_einsetzen", "chip_entfernen"):         # Erweiterungen in der Kabine (keine Aktion)
        defs = kampf.daten(moddir(z["modul"]))
        if not defs or (z["status"] not in ("kabine", "wahl") and not kampf.progress(z).get("test")):
            raise ValueError("Das geht nur bei Rosi in der Werkstatt.")
        if name == "chip_einsetzen":
            kampf.chip_einsetzen(z, defs, daten.get("platz") or "", daten.get("id") or "", daten.get("familie") or "")
        else:
            kampf.chip_entfernen(z, daten.get("platz") or "", daten.get("id") or "", daten.get("familie") or "")
    elif name == "werkstatt_abgeben":                 # Rosis Werkstatt (25.10.2026): in der Kabine, keine Aktion
        defs = kampf.daten(moddir(z["modul"]))
        if not defs or z["status"] not in ("kabine", "wahl"):
            raise ValueError("Das geht nur bei Rosi in der Werkstatt.")
        kampf.abgeben(z, defs, daten.get("platz") or "", daten.get("id") or "")
    elif name == "tasche_kaufen":                     # Tasche bei Rosi (Duc 29.10.2026): nur Geld, sofort fertig
        if z["status"] not in ("kabine", "wahl"):
            raise ValueError("Das geht nur bei Rosi in der Werkstatt.")
        titel, kurz, zeilen = handel.tasche_kaufen(z, modul)
        z["meldungen"].append({"titel": "🎒 " + titel, "kurz": kurz, "folgen": zeilen})
    elif name == "laden_besuch":                      # Alvas Bar / Petrus Werkstatt betreten: vielleicht die Riccis (29.10.2026)
        bid = taschendieb.ausloesen(z, daten.get("laden") or "")
        if bid:
            kampf_starten(z, modul, bid)
        else:
            los_beim_besuch(z, modul, daten.get("laden") or "")   # Akt 3: Petrus Tafel, Alvas Getraenk
    elif name == "ort_reisen":                        # Schnellreise im Ortskapitel (Duc 29.10.2026, kern/wegpunkte.py)
        idx = (ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {})
        r = wegpunkte.ziele(z, idx)
        ziel = next((w for w in (r or {}).get("ziele", []) if w["id"] == daten.get("id")), None)
        if not ziel:
            raise ValueError("Dorthin kannst du von hier nicht reisen.")
        if not expedition.aktiv(z) and wegpunkte.expedition_von(idx, z.get("ort_start")):
            expedition.starten(z, wegpunkte.expedition_von(idx, z["ort_start"]), modul)   # wie der erste Schritt zu Fuss
        z["ort_weg"], z["ort_sperre"] = [], 0          # neue Spur ab dem Ziel: kein "Go back" hinter einen Sprung
        ort_frame(z, modul, ziel["id"])
        z["meldungen"].append({"titel": "🚩 " + ziel["titel"], "kurz": "You follow your old trail markers.", "folgen": []})
    elif name in ("ort_rasten", "ort_zurueck", "rast_antwort"):   # Rast und Rueckweg im Ortskapitel (26.10.2026)
        offen = z.get("event") or {}
        roh = ((ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {}).get(offen.get("id")) or {})
        if name == "rast_antwort":
            z["meldungen"].append({"titel": "📞 Call", "kurz": "", "folgen": expedition.rast_antwort(z, modul, int(daten.get("index", 0)))})
        elif z["status"] != "ereignis" or not z.get("ort_aktiv") or roh.get("art") != "ort" or offen.get("ergebnis"):
            raise ValueError("Das geht nur unterwegs, vor einer Wahl.")
        elif name == "ort_rasten":
            if not roh.get("rast"):
                raise ValueError("Hier ist kein Rastplatz.")
            z["meldungen"].append({"titel": "🔥 Rest", "kurz": "", "folgen": expedition.rasten(z, moddir(z["modul"]))})
        else:
            weg = z.get("ort_weg") or []
            if len(weg) < 2 or len(weg) - 1 <= z.get("ort_sperre", 0):
                raise ValueError("Weiter zurück geht es nicht.")
            weg.pop()
            ort_frame(z, modul, weg[-1])
    elif name == "attribut_steigern":                # Level-up (26.10.2026): einen Attributpunkt verteilen
        kampf.attribut_steigern(z, daten.get("id") or "")
    elif name in ("ausruesten", "skill_lernen"):     # equipment tab and level-up choice (stage 4b, 24.10.2026)
        defs = kampf.daten(moddir(z["modul"]))
        if not defs:
            raise ValueError("Dieses Modul hat keine Kaempfe.")
        if name == "ausruesten":
            if z.get("kampf") and not z["kampf"].get("ergebnis"):
                raise ValueError("Mitten im Kampf kannst du nicht umziehen.")
            if z["status"] not in ("kabine", "wahl") and not kampf.progress(z).get("test"):
                raise ValueError("Umziehen kannst du bei Rosi in der Werkstatt.")
            kampf.ausruesten(z, defs, daten.get("platz") or "", daten.get("id"))
        else:
            kampf.lernen(z, defs, daten.get("id") or "")
    elif name == "expedition_behalten":               # Niederlage auf einer Expedition: das eine Stueck, das Duc behaelt
        k = z.get("kampf") or {}
        if z["status"] != "kampf" or (k.get("ergebnis") or {}).get("art") != "niederlage" or not expedition.aktiv(z):
            raise ValueError("Gerade ist nichts zu behalten.")
        expedition.behalten(z, modul, kampf.daten(moddir(z["modul"])), daten.get("id") or None)
    elif name == "kampf_nochmal":                     # Try again (Duc 03.11.2026): einmal derselbe Kampf, sonst die Niederlage
        k = z.get("kampf") or {}
        if z["status"] != "kampf" or not (k.get("ergebnis") or {}).get("nochmal"):
            raise ValueError("There is no second try here.")
        if daten.get("annehmen"):
            kampf.niederlage_annehmen(z, modul)
            taschendieb.nach_kampf(z, modul)
            angeln.moewe_nach_kampf(z, modul)
        else:
            kampf.nochmal(z, kampf.daten(moddir(z["modul"])))
            mochis.kampf_vorbereiten(z, modul)
            tutorial.schritt(z)
    elif name in ("kampf_zug", "kampf_parade", "kampf_schliessen"):     # Kampf (Etappe 3, 19.10.2026)
        if z["status"] != "kampf" or not z.get("kampf"):
            raise ValueError("Gerade laeuft kein Kampf.")
        rev = daten.get("revision")
        if name == "kampf_zug":
            kampf.zug(z, modul, daten.get("befehl") or "", daten.get("ziel"), rev, gegner=daten.get("gegner"))   # Zielwahl (29.10.2026)
            taschendieb.nach_kampf(z, modul)           # Riccis (29.10.2026): klauen oder zurueckgeben, sobald es entschieden ist
            angeln.moewe_nach_kampf(z, modul)          # Moewe beim Angeln (29.10.2026): Fisch zurueck oder weg
            kampf.entdeckungen(z, kampf.daten(moddir(z["modul"])))     # Codex: was Duc gerade herausgefunden hat
            kampf.chip_drop_anwenden(z, kampf.daten(moddir(z["modul"])))     # Halsband-Chip des besiegten Gegners
            tutorial.schritt(z)                        # Maxwell-Tutorial: naechster Schritt (24.10.2026)
        elif name == "kampf_parade":
            kampf.parade_aufloesen(z, modul, daten.get("ergebnis") or "", rev)
            taschendieb.nach_kampf(z, modul)
            angeln.moewe_nach_kampf(z, modul)
            kampf.entdeckungen(z, kampf.daten(moddir(z["modul"])))
            kampf.chip_drop_anwenden(z, kampf.daten(moddir(z["modul"])))
            tutorial.schritt(z)
        else:
            kampf.niederlage_annehmen(z, modul)        # Try again offen gelassen: Weiter heisst Niederlage annehmen
            taschendieb.nach_kampf(z, modul)           # (beide rechnen nur einmal ab)
            angeln.moewe_nach_kampf(z, modul)
            k = z["kampf"]
            rueck = kampf.schliessen(z) or {}
            ergebnis = (k.get("ergebnis") or {}).get("art")
            gescheitert = ergebnis == "niederlage" and k["def"].get("expedition_niederlage") and expedition.aktiv(z)
            if gescheitert:                            # Expedition (26.10.2026): Schwarzblende, zurueck aufs Schiff
                (k.get("ergebnis") or {}).setdefault("zeilen", []).extend(
                    expedition.scheitern(z, modul, kampf.daten(moddir(z["modul"]))))
            if k.get("definition") in tutorial.BEGEGNUNGEN:
                tutorial.kampf_vorbei(z)
                if "tutorial_maxwell" not in z["flags"]:
                    z["flags"].append("tutorial_maxwell")
            if k.get("definition") == "maxwell_training":
                (k.get("ergebnis") or {}).setdefault("zeilen", []).extend(tutorial.training_ende(z, modul, ergebnis, k))
            z["meldungen"].append({"titel": "⚔ " + (k["def"].get("titel") or "Kampf"),
                                   "kurz": (k.get("ergebnis") or {}).get("text", ""),
                                   "folgen": (k.get("ergebnis") or {}).get("zeilen", [])})
            z["status"] = rueck.get("status") or "wahl"
            if z["status"] == "kampf":
                z["status"] = "wahl"
            if z["status"] == "taktik":                # Taktik-Karte (Duc 31.10.2026): Duc kommt aus dem echten Kampf zurueck
                taktik.kampf_ende(z, moddir(z["modul"]), ergebnis)
            z["kampf_tag"] = z["tag"]                  # Rosis "Read It" kommt nach einem Kampf
            mo_zeilen = mochis.kampf_ende(z, modul, k, ergebnis)   # Tierstation (31.10.2026): Rettung, Bindung des Begleiters
            if mo_zeilen:
                z["meldungen"].append({"titel": "Mochi's", "kurz": "", "folgen": mo_zeilen})
            chronik.eintragen(z, modul, "moment", "Duc fought: %s (%s)." % (k["def"].get("titel") or "a fight", ergebnis),
                              wer=[], dabei=[], wichtig=1)
            if k.get("definition") == "maxwell_training" and z["status"] == "wahl" and not plan.aktion_verbrauchen(z):
                weiter(z, modul, plan.naechste_phase(z, modul))     # Training kostet 1 Aktion (Modell B)
            elif gescheitert and z["status"] == "wahl":
                ort_aufraeumen(z)                      # die Ortskette bricht ab
                weiter(z, modul, plan.naechste_phase(z, modul))     # eine Phase verloren
            elif ergebnis == "niederlage" and k["def"].get("neustart_bei_niederlage"):
                kampf.lp_auffuellen(z)                 # Hafenkampf (E-041): die Welle beginnt neu, gewinnen muss man
                hilfe = k["def"].get("hilfe_event")    # einmalig nach der ersten Niederlage: Hinweis und Ausruestung (Duc 30.10.2026)
                if hilfe and k["def"].get("hilfe_flag") not in z["flags"]:
                    z["ev_kampf"] = k["definition"]    # die Welle startet neu, sobald das Event geschlossen wird
                    ort_frame(z, modul, hilfe)
                else:
                    kampf_starten(z, modul, k["definition"])
            elif z.get("ort_aktiv") and z["status"] == "wahl":
                if ergebnis in ("ko", "aufgabe", "entkommen") and z.get("ort_frame"):
                    besiegt = z.setdefault("ort_besiegt", [])       # bis zur naechsten Rast ruhig (26.10.2026)
                    if z["ort_frame"] not in besiegt:
                        besiegt.append(z["ort_frame"])
                nxt = ereignisse.weiter_ziel(z) if ergebnis in ("ko", "aufgabe", "entkommen") else None
                if nxt:                                # Ortskapitel (26.10.2026): nach dem Sieg der naechste Frame,
                    ort_frame(z, modul, nxt)           # nach einer Flucht ist der Ausflug vorbei
                else:
                    ort_beenden(z, modul)
            elif z["status"] == "wahl" and ereignisse.pflicht_ziehen(z, modul, moddir(z["modul"]), nur_prolog=True):
                z["event"]["weiter"], z["event"]["status_vorher"] = "wahl", "wahl"
                z["status"] = "ereignis"              # Kette (Hafenkampf): naechstes Glied nach dem Kampf
    elif name == "kommission":                        # Akt 3: Kommission als Verhandlung (kern/kommission.py, Plugin client/plugins/eden-commission, blind gebaut, lokal pruefen)
        d = kommission.daten(moddir(z["modul"]))
        if z["status"] != "kommission" or not z.get("kommission") or not d:
            raise ValueError("Gerade tagt keine Kommission.")
        was = daten.get("was") or ""
        if was == "press":
            kommission.press(z, d, daten.get("satz", 0))
        elif was == "vorlegen":
            kommission.vorlegen(z, d, daten.get("satz", 0), daten.get("karte") or "")
        elif was == "nichts":
            kommission.nichts(z, d)
        elif was == "plaedoyer":
            kommission.plaedoyer(z, d, daten.get("art") or "")
        elif was == "schliessen" and z["kommission"]["fertig"]:
            z["status"] = "wahl"
            weiter(z, modul, plan.naechste_phase(z, modul))
    elif name == "verhandlung":                       # spielbare Anhoerung (Variante B, 25.10.2026), kern/anhoerung.py
        if z["status"] != "verhandlung" or not z.get("verhandlung"):
            raise ValueError("Gerade laeuft keine Anhörung.")
        was = daten.get("was") or ""
        if was == "anklage":
            anhoerung.verhandlung_anklage(z, modul, daten.get("pid") or "")
        elif was == "press":
            anhoerung.verhandlung_press(z, modul, daten.get("satz"))
        elif was == "present":
            anhoerung.verhandlung_present(z, modul, daten.get("fid") or "", daten.get("satz"))
        elif was == "bluff":
            anhoerung.verhandlung_bluff(z, modul)
        elif was == "aufgeben":
            anhoerung.verhandlung_aufgeben(z, modul)
        elif was == "joker":
            anhoerung.verhandlung_joker(z, modul, daten.get("id") or "")
        elif was == "rolle":                          # Rolle, Plaedoyer, Urteil in der Anhoerung (Duc 26.10.2026)
            anhoerung.verhandlung_rolle(z, modul, bool(daten.get("ehrlich")))
        elif was == "plaedoyer":
            anhoerung.verhandlung_plaedoyer(z, modul, daten.get("art") or "")
        elif was == "schliessen":
            if not z["verhandlung"]["fertig"]:
                raise ValueError("The hearing is still going.")
            z["status"] = "szene"
            chronik.eintragen(z, modul, "entscheidung", "Duc argued the case before Megan: %s." % ", ".join(
                "%s %s" % (ANH_PUNKT.get(k, k), ANH_ERG.get(x, x)) for k, x in z["verhandlung"]["runden"].items()),
                wichtig=3)
            if szene.zug(z, modul, "(The questioning is over.)", probe=False, reaktion=False,
                         hinweis=anhoerung.verhandlung_hinweis(z, modul)):
                szene_beenden(z, modul)
        else:
            raise ValueError("Unbekannter Schritt der Anhörung.")
    elif name == "taktik":                            # Taktik-Karte der Belagerung (Duc 31.10.2026), kern/taktik.py
        if z["status"] != "taktik" or not taktik.aktiv(z):
            raise ValueError("Gerade laeuft keine Taktik-Karte.")
        was, md = daten.get("was") or "", moddir(z["modul"])
        kampf_id = None
        if was == "aufstellen":
            taktik.aufstellen(z, md, daten.get("id"), int(daten.get("x")), int(daten.get("y")))
        elif was == "macht":
            taktik.macht_einsetzen(z, md, daten.get("id"))
        elif was == "rueck":
            taktik.rueckspringen(z)
        elif was == "bank":
            taktik.auf_bank(z, md, daten.get("id"))
        elif was == "retten":
            taktik.retten(z, md, daten.get("id"), daten.get("haus"))
        elif was == "loeschen":
            taktik.loeschen(z, md, daten.get("id"), daten.get("haus"))
        elif was == "hilfe_wahl":
            taktik.hilfe_waehlen(z, md, daten.get("id"))
        elif was == "hilfe":
            taktik.hilfe_einsetzen(z, md, daten.get("id"), daten.get("ziel"))
        elif was == "start":
            taktik.start_schlacht(z, md)
        elif was == "szene":
            taktik.szene_weiter(z, md)
        elif was == "szene_alle":
            taktik.szene_ueberspringen(z, md)
        elif was == "szene_wahl":
            taktik.szene_waehlen(z, md, int(daten.get("i", 0)))
        elif was == "bewegen":
            taktik.bewegen(z, md, daten.get("id"), int(daten.get("x")), int(daten.get("y")))
        elif was == "zurueck":
            taktik.zuruecknehmen(z, daten.get("id"))
        elif was == "warten":
            taktik.warten(z, daten.get("id"))
        elif was == "angreifen":
            kampf_id = taktik.angreifen(z, md, daten.get("id"), daten.get("ziel")).get("kampf")
        elif was == "white":
            kampf_id = taktik.white_neu(z).get("kampf")
        elif was == "runde":
            taktik.runde_beenden(z, md)
        elif was == "neustart":
            taktik.neustart_welle(z, md)
        elif was == "flicken":                         # Der Morgen danach (Duc 01.11.2026): ins Ring-Minispiel oder Petrus Trupp
            belagerung.starten(z, taktik.daten(md), daten.get("id"))
        elif was == "flicken_crew":
            z["taktik"]["meldung"] = belagerung.crew(z, taktik.daten(md), daten.get("id"))
        elif was == "schliessen" or was == "bot_sieg":
            taktik.beenden(z, was == "bot_sieg", md)
            if z["plan"]:                              # aus dem Kalender: Die Schlacht hat die Phase verbraucht
                weiter(z, modul, plan.naechste_phase(z, modul))
        else:
            raise ValueError("Unbekannter Schritt auf der Taktik-Karte.")
        if kampf_id:
            kampf.starten(z, taktik.kampf_defs(z, md), kampf_id, rueckkehr={"status": "taktik"}, held=taktik.held_start(z, md))
            taktik.doppel_im_kampf(z)
            z["status"] = "kampf"
    elif name == "sturm":                             # Sturm an Tag 5 (27.10.2026): einteilen, hinrennen, schliessen
        if z["status"] != "sturm" or not sturm.aktiv(z):
            raise ValueError("Gerade tobt kein Sturm.")
        was = daten.get("was") or ""
        if was == "einteilen":
            sturm.einteilen(z, modul, moddir(z["modul"]), daten.get("posten") or {})
        elif was == "sprint":
            sturm.sprint(z, modul, moddir(z["modul"]), bool(daten.get("rennen")))
        elif was == "schliessen":
            sturm.schliessen(z)
            z["status"] = "szene"
            szene_beenden(z, modul)
        else:
            raise ValueError("Unbekannter Schritt im Sturm.")
    elif name == "training_kampf":                    # Training mit Maxwell (24.10.2026), auch ueber die Boxhandschuhe in der Kabine
        if z["status"] not in ("wahl", "kabine") or not tutorial.training_verfuegbar(z):
            raise ValueError("Training gibt es in freier Zeit, nach Maxwells erster Lektion.")
        if z["status"] == "kabine":
            kabine.zurueck(z)
        kampf_starten(z, modul, "maxwell_training")
        tutorial.aufgabe_vergeben(z)                  # Aufgabe des Tages (Duc 02.11.2026)
    elif name == "vorschlaege":                       # drei Antwortideen auf Knopfdruck (16.10.2026)
        sz = z.get("szene")
        if z["status"] != "szene" or not sz or sz.get("wahlmoment_offen"):
            raise ValueError("Gerade gibt es nichts vorzuschlagen.")
        sz["vorschlaege"] = szene.vorschlaege(z, modul, sz)
    elif name == "swipe":
        # Wie bei SillyTavern (17.10.2026): zurueck auf Ducs letzte Nachricht, die ganze Runde neu schreiben. Ohne
        # Schnappschuss (Ironman, nach Neustart ohne Datei) wird nur die letzte Antwort der Figur neu formuliert.
        neu = szene.runde_neu(z, modul)
        if neu is not None:
            z, vorbei = neu
            sichern(z)
            if vorbei:
                szene_beenden(z, modul)
        elif not szene.swipe(z, modul):
            raise ValueError("Nur die letzte Antwort einer Figur kann neu formuliert werden.")
    elif name == "kochen":                            # Ducs Kueche (18.10.2026): ein Gericht in Lolas Kombuese
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        handel.init(z, modul)
        geg = json.load(open(os.path.join(moddir(z["modul"]), "gegenstaende.json"), encoding="utf-8"))
        titel, zeilen = handel.kochen_aktion(z, modul, geg.get("kochen") or {}, daten.get("id") or "",
                                             daten.get("fuer") or "crew")
        if z["status"] == "szene" and z.get("szene"):
            z["szene"]["log"].append({"art": "folgen", "zeilen": [titel] + zeilen, "handel": True})
        z["meldungen"].append({"titel": "🍳 " + titel, "kurz": "", "folgen": zeilen})
    elif name == "kochen_baukasten":                  # Kuechenkreis (27.10.2026, E-079): 1 Haupt + 1 Akzent + 1 Basis aus dem Vorrat
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        handel.init(z, modul)
        geg = json.load(open(os.path.join(moddir(z["modul"]), "gegenstaende.json"), encoding="utf-8"))
        fuer = daten.get("fuer") or "crew"
        titel, zeilen = kuechen.kochen_baukasten(z, modul, geg.get("kochen") or {}, daten.get("basis") or "", daten.get("haupt") or "",
                                                 daten.get("akzent") or "", fuer, handel.crew_an_bord(z, modul) if fuer == "crew" else [fuer])
        if z["status"] == "szene" and z.get("szene"):
            z["szene"]["log"].append({"art": "folgen", "zeilen": [titel] + zeilen, "handel": True})
        z["meldungen"].append({"titel": "🍳 " + titel, "kurz": "", "folgen": zeilen})
        los_beim_besuch(z, modul, "kochen")           # Akt 3: Ba Tus Topf, Lolas Menue
    elif name in ("garten_pflanzen", "stall_kaufen", "stall_ausbauen", "tier_kaufen", "tier_benennen", "tier_schlachten", "nonna_kaufen",
                  "nonna_verlassen", "fred_gehoert"):  # Farm bei Nonna (27.10.2026): keine Aktion, keine Phase
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        zeilen = farm_aktion(z, modul, name, daten)
        if zeilen:
            z["meldungen"].append({"titel": "🌿 Nonna's farm", "kurz": "", "folgen": zeilen})
    elif name == "angeln_start":                      # Angeln (27./28.10.2026): am Boot oder an einem Rastplatz mit Wasser, kein Zeitpreis
        if z["status"] == "ereignis":
            _rast_pruefen(z, modul)
        angeln.starten(z, modul, daten.get("ort") or "", z.get("ort_frame"))
    elif name == "angeln_wurf":
        angeln.auswerfen(z, modul)
    elif name == "angeln_ergebnis":
        angeln.ergebnis(z, modul, bool(daten.get("gefangen")), int(daten.get("fehler") or 0), bool(daten.get("leicht")),
                        daten.get("grund") or "")
        bid = angeln.moewe_offen(z)
        if bid:                                       # Moewe (Duc 29.10.2026): sie schnappt den Fisch, gleich wird gekaempft
            bild = z["angeln"].get("bild")
            kampf_starten(z, modul, bid)
            if bild:
                z["kampf"]["def"]["bild"] = bild      # gekaempft wird, wo geangelt wird
    elif name == "angeln_ende":
        zeilen = angeln.ende(z, modul)
        if zeilen:
            z["meldungen"].append({"titel": "🎣 Fishing", "kurz": "", "folgen": zeilen})
        los_beim_besuch(z, modul, "angeln")           # Akt 3: The Catch mit Buenaventuras Maennern
    elif name == "schiessen_start":                   # Holms Wette um Gemelli (30.10.2026), Plugin eden-schiessen, kein Zeitpreis
        eid = schiessen.starten(z)                    # neuer Gegner: erst die Szene, danach startet der Client erneut
        if eid:
            ereignisse.ort_oeffnen(z, modul, moddir(z["modul"]), eid)
            z["event"]["weiter"], z["event"]["status_vorher"] = "wahl", "wahl"
            z["status"] = "ereignis"
    elif name == "schiessen_ergebnis":
        schiessen.ergebnis(z, daten.get("runden"), bool(daten.get("leicht")), modul)
    elif name == "schiessen_ende":
        eid = schiessen.ende(z)                       # Wolff geschlagen: Holm gibt die Waffe aus der Hand
        if eid:
            ereignisse.ort_oeffnen(z, modul, moddir(z["modul"]), eid)
            z["event"]["weiter"], z["event"]["status_vorher"] = "wahl", "wahl"
            z["status"] = "ereignis"
    elif name == "abbau_start":                       # Abbauen an Rastplaetzen (28.10.2026): Axt/Spitzhacke, Ring-Minispiel im Client
        _rast_pruefen(z, modul)
        abbau.starten(z, modul, z.get("ort_frame"), daten.get("art") or "")
    elif name == "abbau_schlag" and (z.get("abbau") or {}).get("bau"):
        belagerung.schlag(z, taktik.daten(moddir(z["modul"])), daten.get("ergebnis") or "")
    elif name == "abbau_ende" and (z.get("abbau") or {}).get("bau"):
        z["taktik"]["meldung"] = belagerung.ende(z)
    elif name == "abbau_schlag":
        abbau.schlag(z, modul, daten.get("ergebnis") or "")
    elif name == "abbau_ende":
        zeilen = abbau.ende(z, modul)
        if zeilen:
            z["meldungen"].append({"titel": "🪓 Gathering" if "tree" in zeilen[0] else "⛏ Gathering", "kurz": "", "folgen": zeilen})
    elif name == "schneider_bringen":                 # Danzels Auftraege (30.10.2026): Material abgeben, keine Phase
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        z["meldungen"].append({"titel": "Le Th\u00e9\u00e2tre Rouge", "kurz": "", "folgen": schneider.bringen(z, modul, daten.get("id") or "")})
    elif name == "mochis_spur":                       # Bibis Tierstation (31.10.2026): eine Spur ist ein Ausflug und kostet die Phase
        if z["status"] != "wahl":
            raise ValueError("You can't follow a trail right now.")
        if plan.aktionen(z):
            raise ValueError("A trail needs the whole phase, and you've already used an action.")
        erster = mochis.spur_start(z, modul, daten.get("id") or "", bool(daten.get("koeder")))
        ort_aufraeumen(z)
        z["ort_aktiv"] = z["ort_start"] = erster
        ort_frame(z, modul, erster)
    elif name == "mochis_brief_zu":                   # Bibis Overlay gelesen
        z.pop("mochis_brief", None)
    elif name in ("mochis_fuettern", "mochis_besuch", "mochis_begleiter", "mochis_einsammeln"):   # keine Aktion, keine Phase
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        if name == "mochis_fuettern":
            zeilen = mochis.fuettern(z, modul, daten.get("id") or "", daten.get("art") or "")
        elif name == "mochis_besuch":
            zeilen = mochis.besuchen(z, modul, daten.get("id") or "")
        elif name == "mochis_begleiter":
            zeilen = mochis.begleiter_setzen(z, modul, daten.get("id") or "")
        else:
            zeilen = mochis.einsammeln(z, modul)
        z["meldungen"].append({"titel": "Mochi's", "kurz": "", "folgen": zeilen})
    elif name == "petru_kaufen":                      # Petrus Werkstatt (28.10.2026): naechste Werkzeugstufe
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        zeilen, gruppe = abbau.werkzeug_kaufen(z, modul, daten.get("werkzeug") or "")
        z["petru_zeile"] = gruppe
        z["meldungen"].append({"titel": "🔨 Petru's Workshop", "kurz": "", "folgen": zeilen})
    elif name == "petru_fisch":                       # Petru kauft Fisch (28.10.2026): erster Verkauf je Art = sein Satz
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        zeilen, gruppe = abbau.fisch_verkaufen(z, modul, daten.get("fisch") or "", bool(daten.get("alle")))
        z["petru_zeile"] = gruppe or "gruss"
        z["meldungen"].append({"titel": "🐟 Petru's Workshop", "kurz": "", "folgen": zeilen})
    elif name == "petru_koeder":                      # Koeder bauen (30.10.2026): Geld + Rohstoffe, Look 1 von 2
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        zeilen, gruppe = koeder.bauen(z, modul, daten.get("koeder") or "", daten.get("look") or None)
        z["petru_zeile"] = gruppe
        z["meldungen"].append({"titel": "🎣 Petru's Workshop", "kurz": "", "folgen": zeilen})
    elif name == "petru_koeder_look":                 # Look eines gebauten Koeders umschalten (jederzeit, kostenlos)
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        koeder.look_waehlen(z, modul, daten.get("koeder") or "", daten.get("look") or "")
    elif name in ("kaufen", "verkaufen", "benutzen", "job"):
        if not z.get("persona") or z["status"] in ("prolog", "ende", "persona_wahl"):
            raise ValueError("Not possible right now.")
        handel.init(z, modul)
        if name == "kaufen":
            titel, zeilen = modul["laeden"][daten["laden"]]["name"], handel.kaufen(z, modul, daten["laden"], daten["id"])
            k = modul["items"][daten["id"]].get("kommentar")
            if k:                                     # Teile: die Ladenfigur sagt etwas dazu (fester, vertonter Satz)
                z["laden_kommentar"] = {"laden": daten["laden"], "id": "teil." + daten["id"], "wer": k["wer"],
                                        "text": k["text"], "gefuehl": k.get("gefuehl", "neutral"),
                                        "nr": len(z.get("buchungen", []))}
            h = rollen.rolle(modul, "haendler")
            if h and daten["laden"] == h and not k:      # Haendler: Satz je Kategorie, bei Geschenken mit Hinweis (26.10.2026)
                r = handel.kauf_reaktion(z, modul, h, daten["id"])
                if r:
                    z["laden_kommentar"] = {"laden": h, "id": r["id"], "wer": h, "text": r["text"], "gefuehl": r["gefuehl"],
                                            "nr": len(z.get("buchungen", []))}
            if h and daten["laden"] == h:
                chronik.eintragen(z, modul, "handel", "Duc bought %s from %s." % (modul["items"][daten["id"]]["label"],
                                  ascii_name(modul, h)), wer=[h], dabei=[], wichtig=1)
            kurz = ""
        elif name == "verkaufen":
            h = rollen.rolle(modul, "haendler")
            titel, zeilen, kurz = "%s buys" % handel.anzeigename(modul, h), \
                handel.verkaufen(z, modul, daten["art"], daten["id"]), ""
        elif name == "benutzen":
            titel, zeilen, kurz = "Used", handel.benutzen(z, modul, daten["id"]), ""
        else:
            V = showrunner.vorrat(moddir(z["modul"]))
            job = next((j for j in V["jobs"] if j["id"] == daten["id"]), {})
            r = handel.job_machen(z, modul, V, daten["id"])
            p = r["probe"]                          # None: Abgabe oder bezahlter/sicherer Weg ohne Wurf
            titel, kurz = "Mission · " + (p["text"] if p else "done"), r["text"]
            zeilen = (["D20 %s + %d = %d vs DC %d" % (p["wurf"], sum(b for _, b in p["boni"]), p["summe"], p["sg"])]
                      if p else []) + r["zeilen"]
            # Ergebnis-Popup (17.10.2026) statt Meldung: Figur mit passender Mimik + ihr fester Kommentar
            z["job_ergebnis"] = {"nr": len(z["jobs_erledigt"]), "id": daten["id"], "titel": job.get("titel", ""),
                                 "pid": r["pid"], "ok": r["ok"], "gruppe": r["gruppe"], "kommentar": r["kommentar"],
                                 "text": kurz, "probe": p, "folgen": r["zeilen"], "weg_gruppe": job.get("gruppe")}
        if z["status"] == "szene" and z.get("szene"):
            z["szene"]["log"].append({"art": "folgen", "zeilen": [titel] + ([kurz] if kurz else []) + zeilen, "handel": True})
        if name != "job":
            z["meldungen"].append({"titel": titel, "kurz": kurz, "folgen": zeilen})
    elif name == "geben":
        if z["status"] != "szene" or not z.get("szene"):
            raise ValueError("You can only give a gift in a scene she is part of.")
        pid, sz = daten["an"], z["szene"]
        if pid not in sz["figuren"] or pid not in modul["personen"]:
            raise ValueError("That person isn't in this scene.")
        handel.init(z, modul)
        label = modul["items"][daten["id"]]["label"]
        if not modul["personen"][pid].get("romanzierbar"):      # Nebenfigur: kommentiert, kleine Wirkung je Rolle
            zeilen, auftrag = handel.schenken_npc(z, modul, daten["id"], pid)
            abgelehnt = any("bribe" in x or "Bestechung" in x for x in zeilen)     # Meldung seit 28.10. englisch
            chronik.eintragen(z, modul, "geschenk", ("Duc tried to give %s an expensive gift (%s); she treated it as a bribe."
                                                    if abgelehnt else "Duc gave %s a gift: %s.") % (szene.kurz(modul, pid), label),
                              wer=[pid], wichtig=2 if abgelehnt else 1)
            sz["log"].append({"art": "ereignis", "text": "You give %s: %s" % (szene.kurz(modul, pid), label)})
            szene.melden(z)
            szene.sprechen(z, modul, sz, pid, "(he gives a gift: %s)" % label,
                           "EVENT - Duc gives %s a gift right now: %s. %s React to it in this reply, in character.\n\n"
                           % (szene.kurz(modul, pid), label, auftrag))
            sz["log"].append({"art": "folgen", "zeilen": zeilen, "handel": True})
            sichern(z)
            return z
        zeilen, wertung = handel.schenken(z, modul, daten["id"], pid)
        chronik.eintragen(z, modul, "geschenk", "Duc gave %s a gift: %s%s." % (
            szene.kurz(modul, pid), label, "" if wertung in (1, 2) else " - it did not go down well"), wer=[pid], wichtig=2)
        sz["log"].append({"art": "ereignis", "text": "You give %s a gift: %s" % (szene.kurz(modul, pid), label)})
        szene.melden(z)
        szene.sprechen(z, modul, sz, pid, "(he gives her a gift: %s)" % label,
                       "EVENT - Duc gives %s a gift right now: %s. %s React to it in this reply, in character.\n\n" % (
                           szene.kurz(modul, pid), label, handel.GESCHENK_AUFTRAG[wertung if isinstance(wertung, str)
                                                                                  else max(-1, min(2, wertung))]))
        sz["log"].append({"art": "folgen", "zeilen": zeilen, "handel": True})
    elif name == "tisch_fertig":                     # Tischszene (27.10.2026) zu Ende oder uebersprungen: keine Aktion, keine Phase
        tisch.fertig(z)
    elif name == "vorliebe_gemeldet":                # Lavendel-Meldung lief - beim Neuladen nicht wiederholen
        vorlieben.melden(z, set(daten.get("schluessel") or []))
    elif name == "vorliebe_gelesen":                 # Detail im Figurenprofil angezeigt - "Neu" verschwindet
        vorlieben.lesen(z, daten.get("figur") or "", daten.get("item") or "")
    elif name == "handy_antwort":
        text = (daten.get("text") or "").strip()
        if not text:
            raise ValueError("Leere Nachricht.")
        handy.antworten(z, modul, int(daten["index"]), text,
                        lambda pid: szene.karte(modul, modul["personen"][pid])["bogen"], ton=daten.get("ton"))
    elif name == "handy_chips":                       # three answer chips for one chat (24.10.2026) - costs no phase or action
        handy.make_chips(z, modul, int(daten["index"]),
                         lambda pid: szene.karte(modul, modul["personen"][pid])["bogen"])
    elif name == "handy_gelesen":
        for i in daten.get("indizes", []):
            if 0 <= i < len(z.get("handy", [])):
                z["handy"][i]["gelesen"] = True
    elif name == "verabredung_ort":                   # Ort einer Verabredung waehlen (17.10.2026, Karte im Handy)
        verabredung_ort(z, modul, int(daten["index"]), daten.get("ort") or "")
    elif name == "szene_neu":
        if z["modus"] != "entspannt":
            raise ValueError("Im Ironman-Modus gibt es kein Zuruecksetzen.")
        snap_pfad = os.path.join(STAENDE, z["id"] + "_vor_szene.json")
        snap = json.load(open(snap_pfad, encoding="utf-8"))
        sid = snap.pop("_szene_id")
        sdef = snap.pop("_szene_def", None)
        z = snap
        szene.starten(z, modul, sdef or plan.szene_nach_id(z, sid))
    else:
        raise ValueError("Unbekannte Aktion " + name)
    if z.get("persona") and z["status"] not in ("prolog", "persona_wahl"):
        handel.jobs_angebot(z, modul, showrunner.vorrat(moddir(z["modul"])))   # Tagesangebot festschreiben
    # Kennengelernt ohne eigene Szene (z. B. Petru beim ersten Landgang, Story-Flag <id>_kennengelernt) zaehlt als bekannt
    zustand.bekannt_machen(z, [f[:-len("_kennengelernt")] for f in z.get("flags", []) if f.endswith("_kennengelernt")
                               and f[:-len("_kennengelernt")] in modul["personen"]])
    sz_t = z.get("szene") if z["status"] == "szene" else None
    if sz_t and rollen.rolle(modul, "dorfohr") in (sz_t.get("figuren") or []):
        vorlieben.tratsch(z, modul, "szene")          # das Dorfohr verraet einmal am Tag eine Vorliebe (ab Vertrauen 2)
    if ermittlung.aktiv(z) and z.get("persona"):      # Erinnerungen, freiwillige Mitteilungen, Tratsch, Widersprueche
        sz = z.get("szene") if z["status"] == "szene" else None
        neu = ermittlung.automatisch(z, modul, sz)
        if neu and sz:
            sz["log"].append({"art": "ermittlung", "zeilen": neu})
        elif neu:
            z["meldungen"].append({"titel": "Ermittlung", "kurz": "", "folgen": neu})
        gest = ermittlung.freiwillig_gestehen(z, modul, sz) if sz and name in ("zug", "geste", "zeit_antwort") else None
        if gest:                                       # sie bittet selbst um das Gespraech (B4)
            zeilen, pid, hinweis = gest
            sz["log"].append({"art": "ermittlung", "zeilen": zeilen})
            szene.sprechen(z, modul, sz, pid, "(she asks Duc for a word in private)", hinweis)
    sichern(z)
    return z


def szene_beenden(z, modul):
    sz = z.get("szene") or {}
    if sz.get("def", {}).get("hauptstory") and sz["def"].get("wahlmoment") and not sz.get("wahlmoment_erledigt"):
        sz["wahlmoment_offen"] = True                  # Story-Entscheidungen (Bericht, Weg ...) nie ueberspringen
        return
    if figurenrahmen.abschied_faellig(modul, sz):      # erst der Abschied und das Overlay, der Klick beendet die Szene (Duc 01.11.2026)
        szene.abschied_einleiten(z, modul)
        return
    meldung, archiv = szene.beenden(z, modul)
    archivieren(z, archiv)
    if sz.get("abschluss"):                            # das Overlay hat schon alles gezeigt; offen ist nur noch das Handy
        meldung["kurz"], meldung["folgen"] = "", [x for x in meldung["folgen"] if x.startswith("📱")]
        meldung["still"] = not meldung["folgen"]
    z["meldungen"].append(meldung)
    if sz.get("def", {}).get("aktion") and plan.aktion_verbrauchen(z, sz["def"]["aktion"]):
        weiter(z, modul, plan.phase_beginnen(z))      # Modell B: Anruf kostet 1 Aktion, die Phase geht weiter
        return
    weiter(z, modul, plan.naechste_phase(z, modul))


# ------------------------------------------------------------------ Kampf (Etappe 3, 19.10.2026)
def kampf_starten(z, modul, bid):
    """Kampf als Unterbrechung wie ein Ereignis: Status "kampf", danach zurueck in den vorherigen Status."""
    defs = kampf.daten(moddir(z["modul"]))
    if not defs:
        raise ValueError("Dieses Modul hat keine Kaempfe.")
    kampf.starten(z, defs, bid, rueckkehr={"status": z["status"]})
    mochis.kampf_vorbereiten(z, modul)                # Tierstation (31.10.2026): Schlafgranaten und Koeder, Begleiter auf Expeditionen
    z["status"] = "kampf"
    tutorial.schritt(z)                               # Maxwell-Tutorial: erster Schritt beim Kampfbeginn


def kampf_profil(z):
    """Equipment/skill tab (24.10.2026): level, gear, skill tree - None if the module has no fights."""
    defs = kampf.daten(moddir(z["modul"]))
    return kampf.profil(z, defs) if defs else None


def kampf_bild(sprite, pose):
    """URL eines Kampfbilds oder None, wenn die Datei (noch) fehlt - der Client nimmt dann eine Ersatzpose."""
    if not re.fullmatch(r"[A-Za-z0-9_]+", sprite or "") or not re.fullmatch(r"[a-z_]+", pose):
        return None
    datei = os.path.join(moddir(), "kampf", sprite, pose + ".webp")
    return "/kampfbild/%s/%s.webp?v=%d" % (sprite, pose, int(os.path.getmtime(datei))) if os.path.isfile(datei) else None


# Gefuehle ohne eigenes Duc-Bild (seine Saetze sind SFW, Duc 03.11.2026) -> naechstes vorhandenes
DUC_GEFUEHL_ERSATZ = {"excitement": "joy_2", "desire": "love", "sultry": "pride", "teasing": "amusement", "pleasure": "joy",
                      "submissive": "embarrassment", "worshipful": "admiration"}


DUC_HANDY_GEFUEHL = {"frech": "amusement", "wholesome": "joy", "witzig": "amusement", "ernst": "caring"}


def duc_bild(z, gefuehl=None):
    """Duc von vorne wie im Character-Menue (Jacke = Look, gehaltene Waffe) fuer Ansichten ausserhalb des Kampfs -
    Anhoerung, Sturm (29.10.2026). Mit Gefuehl: seine Gefuehls-Pose in der getragenen Jacke, ohne Waffe, mit
    Sonnenbrille (charakter\\gefuehle\\Duc<Look>\\<gefuehl>.webp, Duc 03.11.2026). URL oder None, wenn das Bild fehlt."""
    defs = kampf.daten(moddir(z["modul"]))
    if not defs:
        return None
    name = kampf.duc_portrait(z, defs)
    if gefuehl:
        look = re.match(r"Duc(Erde|Wasser|Feuer|Luft|Cyber)", name)
        for g in (gefuehl, DUC_GEFUEHL_ERSATZ.get(gefuehl), gefuehl.split("_")[0], "neutral"):
            datei = look and g and os.path.join(moddir(z["modul"]), "charakter", "gefuehle", look.group(0), g + ".webp")
            if datei and os.path.isfile(datei):
                return "/charakterbild/gefuehle/%s/%s?v=%d" % (look.group(0), g, int(os.path.getmtime(datei)))
    datei = os.path.join(moddir(z["modul"]), "charakter", name + ".webp")
    return "/charakterbild/%s?v=%d" % (name, int(os.path.getmtime(datei))) if os.path.isfile(datei) else None


# ------------------------------------------------------------------ Ansicht fuer den Client
# Erklaerung der Vorraete fuer die Schiff-Leiste und das Schiff-Fenster (17.10.2026, Duc: "wofuer ist der Diesel?").
# Nur Spielregeln, keine Handlung - Zahlen stammen aus Modul und Code (szenen.json takt, handel.py, gesten.py).
VORRAT_INFO = {
    "moral": "The crew's mood (0–5). It rises with shared successes and downtime "
             "(time together · relaxing).",
    "ruf": "What the village of Cala d'Orsu thinks of the crew (0–5). Good deeds in the village raise it; fencing that gets found "
           "out, smuggling and scandals lower it.",
    "rueckhalt": "How much the crew backs your decisions (0–100). The crew council, promises kept or broken and the ship's "
                 "rules move it. It counts for the crew at the end.",
    "energie": "Your energy for the day (0–3). Every way that needs a roll when someone asks you for a favour costs 1. Each "
               "day brings 2 more, and an espresso or a relaxed hour with the crew gives +1.",
}


def ansicht(z, debug=False):
    modul = modul_laden()
    titel = "/bg/" + modul["titelbild"] if modul.get("titelbild") else None
    v = {"kobold": llm.bereit(), "modul": modul["titel"], "untertitel": modul.get("untertitel", ""), "titelbild": titel, "z": None,
         "profil": profil_ansicht(z), "ausschnitte": ausschnitte(modul["id"])}
    v["musik"] = musik.hint(BASE, modul["id"], z)
    gesehen = meta.lesen(STAENDE).get("enden", [])   # LATE_GAME.md Punkt 7: Enden ueber alle Durchlaeufe, Stern sichtbar
    v["enden"] = {"gesehen": len(gesehen), "gesamt": len(akt3.ENDEN), "stern": "stern" in gesehen}
    v["musik_titel"] = musik.hint(BASE, modul["id"], None)
    kp = kampf_profil(z) if z else None                  # einmal je Ansicht (28.10.2026: war zweimal, ~110 ms an Tag 12)
    if kp and kp.get("werkstatt"):
        kp["werkstatt"]["tasche"] = handel.tasche_ansicht(z, modul)               # Tasche bei Rosi (29.10.2026)
    v["sfx"] = {"katalog": sfx.katalog(BASE, modul["id"]), "hinweis": sfx.hint(BASE, modul["id"], z),
                "ambience": sfx.ambience(BASE, modul["id"], z, modul),          # Hintergrund-Schleife (27.10.2026)
                "waffen": len((kp or {}).get("waffen") or []),                  # neue Waffe -> Ton im Client
                "still": bool(z and ereignisse.gesperrt_durch_story(z, modul, z["phase"]))}   # Belagerung: keine Bossa beim Phasenwechsel
    if z is None:
        return v
    werte = []
    for pid, p in modul["personen"].items():
        if p.get("romanzierbar"):
            werte.append({"id": pid, "name": p["name"], "vertrauen": z["werte"].get("vertrauen." + pid, 0),
                          "begehren": z["werte"].get("begehren." + pid, 0),
                          "v_anteil": round(zustand.anteil(z, "vertrauen." + pid), 2),
                          "b_anteil": round(zustand.anteil(z, "begehren." + pid), 2),
                          # Punkte (0-100) fuer die Zahl an der Wert-Pille im Gespraech (UX-Paket 03.11.2026)
                          "v_punkte": z.get("punkte", {}).get("vertrauen." + pid), "b_punkte": z.get("punkte", {}).get("begehren." + pid),
                          "avatar": buehne.sprite(cfg(), modul, pid, p.get("set_standard"), "neutral", pid),
                          "gedaechtnis": z["gedaechtnis"].get(pid, [])[-3:] if debug else []})
    riv = [{"label": zustand.wert_label(modul, k), "wert": w} for k, w in z["werte"].items() if k.startswith("rivalitaet.")]
    profile = figuren_profile(z, modul)
    sonst = [{"key": k, "label": zustand.wert_label(modul, k), "wert": w, "max": zustand.bereich(modul, k)[1],
              "min": zustand.bereich(modul, k)[0], "info": VORRAT_INFO.get(k, "")}
             for k, w in z["werte"].items() if "." not in k and k in modul["werte"] and not zustand.verborgen(modul, k)]
    for s in sonst:                                   # Crew-Stimmung: Wort + Gesicht, Zahl nur im Tooltip (27.10.2026)
        if s["key"] == moral.KEY and moral.aktiv(modul):
            s.update(moral.ansicht(z, modul), info=moral.cfg(modul).get("info", s["info"]))
        elif s["key"] == "ruf":                    # Ruf als Wort (30.10.2026, Dorf redet): Zahl nur im Tooltip
            s.update(wort=legenden.ruf_wort(s["wert"]), gesicht="★")
    optionen = []
    if z["status"] == "wahl":
        for sid in z["optionen"]:
            s = plan.szene_nach_id(z, sid)
            wer = plan.anwesende(z, s, modul)
            sprites = []
            for pid in wer:
                setname = buehne.set_waehlen(cfg(), modul, pid, s, z["phase"], (s.get("figuren") or {}).get(pid), z)
                sp = buehne.sprite(cfg(), modul, pid, setname, moral.grund_gefuehl(z, modul, pid), pid) if setname else None
                if sp:
                    sprites.append(sp)
            optionen.append({"id": sid, "titel": s["titel"], "ort": modul["raeume"][s["ort"]]["label"],
                             "mit": [modul["personen"][x]["name"] for x in wer], "text": s["ausgangslage"],
                             "bild": buehne.szenenbild(modul, s, z["phase"]), "sprites": sprites,
                             "hinweise": szene.szene_hinweise(z, modul, s),
                             # Tageswahl (UX-Paket 03.11.2026): wo Duc mit der Person steht und ob heute etwas Neues ansteht
                             "personen": [{"id": pid, "name": modul["personen"][pid]["name"],
                                           "vertrauen": z["werte"]["vertrauen." + pid],
                                           "begehren": z["werte"].get("begehren." + pid),
                                           "neu": ereignisse.heute_neu(z, modul, moddir(z["modul"]), pid)}
                                          for pid in wer if "vertrauen." + pid in z["werte"]]})
    sz = None
    if z.get("szene"):
        s = z["szene"]
        log = []
        for e in s["log"]:
            e = dict(e)
            if e["art"] == "figur" and not debug:
                e["text"] = e["gezeigt"]
                e.pop("verworfen", None)
            log.append(e)
        # Buehne: Hintergrund + je Figur der zuletzt gezeigte Sprite (vor dem ersten Satz: neutral)
        auf_buehne, letzter = [], next((e["wer"] for e in reversed(s["log"]) if e["art"] == "figur"), None)
        for pid in s["figuren"]:
            if pid == szene.ERZAEHLER:
                continue
            sp = next((e.get("sprite") for e in reversed(s["log"]) if e["art"] == "figur" and e["wer"] == pid and e.get("sprite")), None)
            sp = sp or buehne.sprite(cfg(), modul, pid, s.get("sets", {}).get(pid), moral.grund_gefuehl(z, modul, pid), pid)
            auf_buehne.append({"id": pid, "name": modul["personen"][pid]["name"], "sprite": sp, "spricht": pid == letzter,
                               "set": s.get("sets", {}).get(pid),
                               # Punkte fuer die Wert-Pille (UX-Paket 03.11.2026), auch fuer Figuren ohne Romanze (Jana, Megan ...)
                               "v_punkte": z.get("punkte", {}).get("vertrauen." + pid), "b_punkte": z.get("punkte", {}).get("begehren." + pid)})
        anruf = bool(s["def"].get("anruf"))
        sz = {"titel": s["def"]["titel"], "zug": s["zug"], "max": s["def"].get("max_zuege", 10), "log": log,
              "kann_swipen": szene.kann_swipen(s), "anruf": anruf,
              "bild": s.get("bild"), "buehne": auf_buehne, "vorschlaege": s.get("vorschlaege", []), "start_chips": [c["text"] for c in s.get("start_chips", [])], "abschluss": s.get("abschluss"), "verlassen": szene.verlassen_moeglich(s),
              "wahlmoment": szene.wahlmoment_ansicht(z, s, modul), "gesten": None if anruf else gesten.ansicht(z, modul, s),
              "ermittlung": {"aktionen": ermittlung.moeglich(z, modul, s),
                             "widersprueche": ermittlung.widerspruch_aktionen(z, modul, s),
                             "konfrontation": ermittlung.konfrontation_aktionen(z, modul, s),
                             "fehlt": ermittlung.tafel_kurz(z, modul)} if ermittlung.aktiv(z) else None}
    v["z"] = {
        "id": z["id"], "status": z["status"], "tag": z["tag"], "tage": modul.get("probefahrt_tage") or modul["zeitraster"]["tage"],
        "phase": z["phase"], "phasen": modul["zeitraster"]["phasen"], "modus": z["modus"],
        "persona": z["persona"], "persona_optionen": modul["personas"] if z["status"] == "persona_wahl" else [],
        "prolog": modul.get("prolog", []) if z["status"] == "prolog" else [], "ziel": modul.get("ziel", ""),
        "chronik": chronik.ansicht(z, modul),
        "album": album.ansicht(z, modul),
        "handel": handel_bilder(handel.ansicht(z, modul, showrunner.vorrat(moddir(z["modul"])),
                                 [p for p in ((z.get("szene") or {}).get("figuren") or []) if p in modul["personen"]]),
                                z["modul"], z) if z.get("persona") else None,
        "werte": werte, "rivalitaet": riv, "sonst": sonst, "profile": profile,
        "vorlieben": vorlieben.ansicht(z, modul, lambda iid: item_bild(z["modul"], iid)),
        "uhren": [{"label": u["label"], "stand": z["uhren"][k], "segmente": u["segmente"]}
                  for k, u in modul["uhren"].items() if not u.get("verdeckt")],
        "inventar": [modul["items"][i]["label"] for i in z["inventar"]], "codex": z["codex"],
        "bestiarium": kampf.bestiarium(z, kampf.daten(moddir(z["modul"]))) if z.get("bestiarium") else [],
        "heute": [{"phase": h["phase"], "titel": h["titel"]} for h in z["heute"]],
        "optionen": optionen, "szene": sz, "plan_fehler": z["plan_fehler"], "meldungen": z["meldungen"][-3:], "meldung_nr": len(z["meldungen"]), "phase_skip": phase_ueberspringbar(z),
        "spannung": (z["plan"] or {}).get("spannung_spieler", ""),
        "handy": [{"von": f["von"], "name": modul["personen"][f["von"]]["name"], "tag": f["tag"], "phase": f["phase"],
                   "gelesen": f["gelesen"], "verlauf": f["verlauf"], "rest": handy.rest(z, f["von"], modul),
                   "gesperrt": handy.gesperrt(z, modul, f["von"]), "chips": handy.chips_ansicht(z, modul, f),
                   "status": handy.status(z, modul, f["von"]), "profilbild": handy.profilbild(z, f["von"])}
                  for f in z.get("handy", [])],
        "stimmen": {pid: bool(stimme_von(modul, pid)[0]) for pid in list(modul["personen"]) + [szene.ERZAEHLER]},
        "hintergrund": (z.get("szene") or {}).get("bild") or z.get("letztes_bild") or titel,
        "karte": karte(z, modul),
        "job_ergebnis": job_ergebnis_ansicht(z, modul),
        "ermittlung": ermittlung.ansicht(z, modul, z.get("szene") if z["status"] == "szene" else None)
        if ermittlung.aktiv(z) else None,
        "kalender": [{"tag": h["tag"], "phase": h["phase"], "titel": h["titel"], "kurz": h["kurz"]}
                     for h in z["verlauf"][-10:]] + [{"tag": z["tag"], "phase": h["phase"], "titel": h["titel"],
                                                      "kurz": h["kurz"]} for h in z["heute"]]
                    + [{"tag": v["tag"], "phase": v["phase"], "titel": "📅 Date with " + v["name"], "geplant": True,
                        "kurz": v["ort_name"] or "No place yet: choose one on the phone map"} for v in verabredungen_ansicht(z, modul)],
        "arbeitet": LOCK.locked(),
        "abschluss": z.get("abschluss") if z["status"] == "ende" else None,
        "ereignis": ereignisse.ansicht(z, modul, moddir(z["modul"]), cfg(), lambda pid, setname, gef, salz:
                                       event_sprite(modul, z, pid, setname, gef, salz), event_bild)
        if z.get("event") else None,
        "versprechen": ereignisse.offene_versprechen(z),
        "kampf": kampf.ansicht(z, modul, kampf_bild) if z.get("kampf") else None,
        "kampf_profil": kp,
        "bordregeln": [((ereignisse.daten(moddir(z["modul"])) or {}).get("bordregeln") or {}).get(r, {}).get("label", r)
                       for r in (z.get("ev") or {}).get("bordregeln", [])],
    }
    if z["status"] == "kampf" and z.get("kampf") and z["kampf"]["def"].get("bild"):
        v["z"]["hintergrund"] = "/bg/" + z["kampf"]["def"]["bild"]
    elif z["status"] == "ereignis" and (v["z"].get("ereignis") or {}).get("bild"):
        # 26.10.2026: the layer behind the event screen showed the last scene (e.g. the engine room) and flashed
        # through on every change of screen - now it shows the event's own picture
        v["z"]["hintergrund"] = v["z"]["ereignis"]["bild"]
    if kabine.aktiv(modul) and z["status"] == "wahl" and not kabine.gesperrt(
            z, (showrunner.vorrat(moddir(z["modul"])) or {}).get("fixplan")):
        v["z"]["kabine_karte"] = {"bild": buehne.hintergrund(modul, kabine.ort(modul, z), z["phase"]),
                                  # Kabinen-Kreis (27.10.2026): Hinweispunkt, wenn ein neues Andenken in der Vitrine liegt
                                  "andenken": sum(1 for iid, it in modul["items"].items()
                                                  if it.get("vitrine") and iid in z["inventar"])}
    if z["status"] in ("wahl", "kabine"):            # Modell B: Aktionen der freien Phase (●●)
        v["z"]["aktionen"] = {"genutzt": plan.aktionen(z), "max": plan.AKTIONEN_PRO_PHASE}
    if z["status"] in ("wahl", "kabine") and tutorial.training_verfuegbar(z) and kampf.daten(moddir(z["modul"])):
        v["z"]["training_kampf"] = z.get("training_kampf") or {"siege": 0, "niederlagen": 0}
    v["z"]["tutorial"] = tutorial.ansicht(z)
    ev_v = v["z"].get("ereignis")
    if ev_v and ev_v.get("art") == "ort" and z.get("event"):          # Expeditions-Bildschirm (Plugin eden-expedition)
        roh = (ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {}).get(z["event"]["id"]) or {}
        kdefs = kampf.daten(moddir(z["modul"])) or {}
        for o_v, o in zip(ev_v.get("optionen", []), roh.get("optionen", [])):
            o_v["exp"] = expedition.wahl_info(z, kdefs, o, kampf_bild)
        idx = (ereignisse.daten(moddir(z["modul"])) or {}).get("_index", {})
        v["z"]["ort_weg"] = [{"id": i, "titel": (idx.get(i) or {}).get("titel", ""), "rast": bool((idx.get(i) or {}).get("rast")),
                              "geruht": i in z.get("ort_rasten", [])} for i in z.get("ort_weg", [])]
        ev_v["rast"] = bool(roh.get("rast"))               # Rastplatz (26.10.2026)
        if roh.get("rast") and roh.get("fund") and z.get("rast_fund_neu"):
            ev_v["fund"] = roh["fund"]                     # erzaehlte Fund-Karte, nur beim ersten Mal
        ev_v["ruhig"] = z.get("ort_frame") in z.get("ort_besiegt", [])
        ev_v["zurueck"] = (idx.get((z.get("ort_weg") or [None, None])[-2]) or {}).get("titel") if len(z.get("ort_weg", [])) - 1 > z.get("ort_sperre", 0) else None
        reise = wegpunkte.ziele(z, idx)
        if reise:                                          # Schnellreise (29.10.2026): Wegpunkt am Eingang / am Rastplatz
            for w in reise["ziele"]:
                w["bild"] = "/bg/eden_rise_%s.png" % w["bild"] if w.get("bild") else None
        ev_v["reisen"] = reise
    if z.get("rast_anruf"):
        a = dict(z["rast_anruf"])
        a["name"] = (modul["personen"].get(a["pid"]) or {}).get("name", a["pid"])
        a["sprite"] = event_sprite(modul, z, a["pid"], None, a.get("gefuehl", "joy"), a["id"])
        v["z"]["rast_anruf"] = a
    if z.get("tisch"):                                # Tischszene (27.10.2026): Beats mit Sprite je Figurenzeile, Plugin eden-tisch
        v["z"]["tisch"] = tisch.ansicht(z, modul, lambda pid, gef: event_sprite(modul, z, pid, None, gef, "tisch.%s.%s" % (pid, gef)))
    if kuechen.daten(modul) and (kuechen.nonna_offen(z, modul) or z.get("kueche")):      # Kuechenkreis (27.10.2026, E-079)
        v["z"]["kueche"] = kuechen_ansicht(z, modul)
    if kuechen.daten(modul) and z["status"] == "wahl":                     # Angelplaetze als Karten neben Szenen und Orten
        v["z"]["angel_orte"] = angeln.orte(z, modul)
    if z["status"] == "wahl" and schiessen.offen(z):                       # runder Knopf neben Cabin (Plugin eden-schiessen)
        v["z"]["holm_wette"] = True
        v["z"]["holm_wette_folgt"] = bool(z.get("schiessen_folgt"))        # Szene mit dem neuen Gegner vorbei: Spiel startet
    if z.get("schiessen"):                                                 # laufende Wette
        a = v["z"]["schiessen"] = schiessen.ansicht(z)
        p = modul["personen"][a["gegner"]["pid"]]
        a["gegner"].update(name=p.get("kurz") or p["name"].split()[0], avatare={m: event_sprite(modul, z, a["gegner"]["pid"], p.get("set_standard"), g, a["gegner"]["pid"])
                                                                                  for m, g in schiessen.AVATAR_GEFUEHLE.items()})
        a["texte"] = [zl["text"] for zl in ereignisse.daten(moddir(z["modul"]))["_index"][a["worte"]]["zeilen"]]
        v["z"]["hintergrund"] = v["z"]["schiessen"]["bild"]
    if z.get("angeln"):                                                    # laufende Angel-Sitzung (Plugin eden-angeln)
        v["z"]["angeln"] = angeln.ansicht(z, modul)
        v["z"]["hintergrund"] = v["z"]["angeln"]["bild"]
    if ev_v and ev_v.get("rast") and kuechen.daten(modul):                 # Quellen am Rastplatz (28.10.2026, Plugin eden-abbau)
        ev_v["quellen"] = abbau.quellen_ansicht(z, modul, z.get("ort_frame"))
    if z.get("abbau"):                                                     # laufende Abbau-Sitzung vor dem Bild des Rastplatzes
        if z["abbau"].get("bau"):
            v["z"]["abbau"] = belagerung.bau_ansicht(z, taktik.daten(moddir(z["modul"])), modul)
        else:
            v["z"]["abbau"] = abbau.ansicht(z, modul)
            v["z"]["abbau"]["bild"] = (v["z"].get("ereignis") or {}).get("bild")
        v["z"]["hintergrund"] = v["z"]["abbau"]["bild"] or v["z"].get("hintergrund")
    if mochis.offen(z, modul):                                             # Bibis Tierstation (31.10.2026)
        v["z"]["mochis"] = mochis.ansicht(z, modul)
    if z.get("mochis_brief"):                                              # Overlay nach dem ersten Fang (01.11.2026)
        v["z"]["mochis_brief"] = mochis.brief_ansicht(z, modul, lambda wer, s, gef, key: event_sprite(modul, z, wer, s, gef, key))
    if schneider.offen(z, modul):                                          # Danzels Auftraege (30.10.2026)
        v["z"]["schneider"] = schneider.ansicht(z, modul)
    if kuechen.daten(modul) and abbau.petru_offen(z, modul):               # Petrus Werkstatt: Werkzeuge
        v["z"]["werkzeuge"] = abbau.werkzeug_ansicht(z, modul)
        v["z"]["petru_fische"] = abbau.fisch_ansicht(z, modul)              # Reiter "Sell Fish" ab dem ersten Fang
        v["z"]["petru_koeder"] = koeder.ansicht(z, modul)                   # Reiter "Baits" (30.10.2026)
        v["z"]["petru_zeile"] = z.get("petru_zeile")
    if z["status"] == "wahl":                         # Ortskapitel (26.10.2026): Orte als Karten neben den Szenen
        v["z"]["orte"] = auftraege.orte_frei(z, moddir(z["modul"]))
    v["z"]["journal"] = auftraege.journal(z, modul, moddir(z["modul"]),
                                          lambda pid: event_sprite(modul, z, pid, None, "neutral", "journal"))
    v["z"]["favours"] = ereignisse.favour_journal(z, modul, moddir(z["modul"]),        # Favours im Journal (29.10.2026)
                                                  lambda name: "/favourfoto/%s.webp" % name)
    if expedition.aktiv(z):
        v["z"]["expedition"] = expedition.ansicht(z, modul, kampf.daten(moddir(z["modul"])) or {})
    v["test_neustart"] = TEST_START is not None
    if z["status"] == "verhandlung":
        sets = (z.get("szene") or {}).get("sets", {})

        def vh_sprite(pid, gef):
            if pid == "duc":                           # Duc: seine Gefuehls-Pose in der getragenen Jacke (03.11.2026)
                return duc_bild(z, gef)
            vorhanden = buehne.sets(cfg(), modul, pid)
            wunsch = sets.get(pid) or modul["personen"][pid].get("set_standard")
            s = wunsch if wunsch in vorhanden else next(iter(vorhanden), None)     # Standard-Set fehlt (z. B. umbenannt)
            return buehne.sprite(cfg(), modul, pid, s, gef, pid + gef) if s else None
        v["z"]["verhandlung"] = anhoerung.verhandlung_ansicht(z, modul, vh_sprite)
    if z["status"] == "kommission":                   # Akt 3: Kommission als Verhandlung (kern/kommission.py)
        v["z"]["kommission"] = kommission.ansicht(z, kommission.daten(moddir(z["modul"])) or {})
    if z["status"] == "sturm":
        sets = (z.get("szene") or {}).get("sets", {})

        def st_sprite(pid, gef):
            if pid == "duc":                           # Duc: seine Gefuehls-Pose in der getragenen Jacke (03.11.2026)
                return duc_bild(z, gef)
            if pid not in modul["personen"]:
                return None
            vorhanden = buehne.sets(cfg(), modul, pid)
            wunsch = sets.get(pid) or modul["personen"][pid].get("set_standard")
            s = wunsch if wunsch in vorhanden else next(iter(vorhanden), None)
            return buehne.sprite(cfg(), modul, pid, s, gef, pid + gef) if s else None
        v["z"]["sturm"] = sturm.ansicht(z, modul, moddir(z["modul"]), st_sprite)
    if z.get("status") == "taktik" and taktik.aktiv(z):
        v["z"]["taktik"] = taktik.ansicht(z, moddir(z["modul"]), modul)
        for k in v["z"]["taktik"]["karten"]:           # Bild oben auf der Trupp-Karte; Duc nimmt sein Charakterbild
            k["sprite"] = duc_bild(z) if k["id"] == "duc" else event_sprite(modul, z, k["id"], k.get("set"), "neutral", "taktik") if k["id"] in modul["personen"] else None
        for k in v["z"]["taktik"]["hilfe"]:
            k["sprite"] = event_sprite(modul, z, k["pid"], k.get("set"), "neutral", "taktik")
        sz = v["z"]["taktik"]["szene"]
        if sz and sz.get("wer") == "Duc":              # Duc spricht: seine Gefuehls-Pose (03.11.2026)
            sz["sprite"] = duc_bild(z, sz.get("gefuehl") or "neutral")
        elif sz and sz.get("pid") in modul["personen"]:  # Wer spricht, steht gross im Bild (Duc 02.11.2026)
            sz["sprite"] = event_sprite(modul, z, sz["pid"], sz.get("set"), sz.get("gefuehl") or "neutral", "taktik")
    ev = v["z"].get("ereignis")
    if ev and ev["art"] == "handy":                    # Videoanruf: Duc klein im Bild, mit Sonnenbrille (Duc 03.11.2026)
        ev["duc_bild"] = duc_bild(z, DUC_HANDY_GEFUEHL.get(ev.get("ton"), "neutral"))
    v["z"]["ziel_kurz"] = modul.get("ziel_kurz", "")
    v["z"]["ziele"] = modul.get("ziele") or []      # Ziele je Akt [{bis_tag, kurz, text}] fuer die Kopfzeile (28.10.2026)
    if z["status"] == "kabine" and kabine.aktiv(modul):
        v["z"]["kabine"] = kabine.ansicht(z, modul, cfg(), lambda iid: item_bild(z["modul"], iid, z))
    return v


# Wege-Labels der Karte (Englisch seit 28.10.2026, STIL.md); der Name WEG_DE bleibt fuer bestehende Aufrufe
# Anhoerung im Chronik-Satz (sichtbar ueber "found out"), statt interner Schluessel (28.10.2026)
ANH_PUNKT = {"handlung": "what happened", "person": "who did it", "motiv": "why"}
ANH_ERG = {"bewiesen": "proven", "bluff": "bluffed", "verloren": "lost"}

WEG_DE = {"persona": "only as First Officer", "vertrauen": "%s trusts you (%d+)", "begleitung": "%s takes you along",
          "item": "with %s", "tag_ab": "from day %d", "flag": "after an event", "nur_phase": "only %s",
          "wert": "%s %d+"}


def weg_text(modul, w):
    teile = []
    for k, v in w.items():
        if k == "wurf":
            teile.append("%s roll DC %d" % (v[0].capitalize(), v[1]))
        elif k == "vertrauen":
            teile.append(WEG_DE[k] % (modul["personen"][v[0]]["name"].split()[0], v[1]))
        elif k == "begleitung":
            teile.append(WEG_DE[k] % modul["personen"][v]["name"].split()[0])
        elif k == "item":
            teile.append(WEG_DE[k] % modul["items"][v]["label"])
        elif k == "wert":
            teile.append(WEG_DE[k] % (zustand.wert_label(modul, v[0]), v[2]))
        elif k in WEG_DE:
            teile.append(WEG_DE[k] % v if "%" in WEG_DE[k] else WEG_DE[k])
    return " + ".join(teile)


def raum_name(r):
    """'Alva's bar (ashore)' -> 'Alva's bar' (Klammern sind Hinweise fuer das Modell, nicht fuer die Karte)."""
    return re.sub(r"\s*\([^)]*\)", "", r["label"]).strip()


def date_zugang(modul, z, rid, v):
    """Zugang fuer eine Verabredung: sie ist dabei (Begleitung zaehlt), abends. -> (status, weg)."""
    return regeln.zugang(modul["raeume"][rid], z, {"anwesend": [v["pid"]], "phase": v["phase"]})


def verabredungen_ansicht(z, modul):
    out = []
    for i, v in enumerate(z.get("verabredungen") or []):
        p = modul["personen"][v["pid"]]
        wann = ("heute " if v["tag"] == z["tag"] else "morgen " if v["tag"] == z["tag"] + 1 else "Tag %d " % v["tag"]) + \
            {"abend": "Abend", "nacht": "Nacht"}.get(v["phase"], v["phase"])
        ort = v.get("ort")
        out.append({"index": i, "pid": v["pid"], "name": p["name"].split()[0], "wann": wann, "tag": v["tag"],
                    "phase": v["phase"], "ort": ort, "ort_name": raum_name(modul["raeume"][ort]) if ort else None,
                    "versucht": v.get("versucht", []), "letzter_wurf": v.get("letzter_wurf"),
                    "lieblingsort": bool(ort and ort in (p.get("lieblingsorte") or []))})
    return out


def karte(z, modul):
    """Wohin? (17.10.2026) - jeder Raum mit Bild, Ruhe (privat 1-5), wer sich jetzt dort aufhaelt, wessen Lieblingsort
    er ist, Zugang in Klartext und - fuer jede offene Verabredung - ob sie dort stattfinden kann."""
    phase, offen = z["phase"], verabredungen_ansicht(z, modul)
    out = []
    for rid, r in modul["raeume"].items():
        if r.get("versteckt"):                       # Zimmer und Orte fuer Zweisamkeit: nur ueber kern/orte.py
            continue
        status, _ = regeln.zugang(r, z)
        hier, lieb = [], []
        for pid, p in modul["personen"].items():
            if buehne.wo_ist(z, modul, pid) == rid:
                k = p.get("kurz") or ""
                hier.append(k if k and not k.startswith("the ") else p["name"].split()[0] if p.get("romanzierbar") else p["name"])
            if rid in (p.get("lieblingsorte") or []):
                lieb.append(p["name"].split()[0])
        dates = {}
        for v in offen:
            st, weg = date_zugang(modul, z, rid, (z.get("verabredungen") or [])[v["index"]])
            if rid in v["versucht"]:
                st = "versucht"
            dates[v["index"]] = {"status": st, "wurf": weg["wurf"] if st == "wurf" else None}
        wege = [weg_text(modul, w) for w in r.get("zugang", [])]
        out.append({"id": rid, "name": raum_name(r), "bereich": r.get("bereich", ""), "status": status,
                    "wege": [w for w in wege if w], "privat": r.get("privat", 1),
                    "bild": "/bg/" + mochis.bild(z, modul) if rid == "mochis" else buehne.hintergrund(modul, rid, phase), "hier": hier, "lieblingsort_von": lieb,
                    "dates": dates})
    return {"raeume": out, "bereiche": modul.get("bereiche") or {}, "verabredungen": offen}


def verabredung_ort(z, modul, index, rid):
    """Duc legt den Ort einer Verabredung fest (17.10.2026). Raeume mit Probe: einmal wuerfeln - gelingt es, steht
    der Ort; misslingt es, ist dieser Raum fuer dieses Date zu (ohne weitere Strafe), ein anderer geht noch."""
    vs = z.get("verabredungen") or []
    if not 0 <= index < len(vs):
        raise ValueError("Diese Verabredung gibt es nicht mehr.")
    if rid not in modul["raeume"]:
        raise ValueError("Unbekannter Ort.")
    v, name = vs[index], modul["personen"][vs[index]["pid"]]["name"].split()[0]
    raum = raum_name(modul["raeume"][rid])
    if rid in v.get("versucht", []):
        raise ValueError("Da kommst du für dieses Date nicht rein – such einen anderen Ort.")
    status, weg = date_zugang(modul, z, rid, v)
    if status == "gesperrt":
        raise ValueError("%s ist für euch gerade nicht zugänglich." % raum)
    if status == "wurf" and v.get("ort") != rid:
        att, sg = weg["wurf"]
        p = wuerfel.probe(att, sg, [(att.capitalize(), z["persona"]["attribute"].get(att, 0))])
        ok = p["ergebnis"] in ("erfolg", "kritisch")
        v["letzter_wurf"] = {"ort": raum, "text": "%s-Probe: %d + %d = %d gegen SG %d – %s" % (
            att.capitalize(), p["wurf"], p["summe"] - p["wurf"], p["summe"], sg, p["text"]), "ok": ok}
        if not ok:
            v.setdefault("versucht", []).append(rid)
            return
    elif (v.get("letzter_wurf") or {}).get("ort") != raum:
        v.pop("letzter_wurf", None)          # alter Fehlwurf an einem anderen Ort ist erledigt
    v["ort"] = rid
    lieb = rid in (modul["personen"][v["pid"]].get("lieblingsorte") or [])
    z["meldungen"].append({"titel": "📅 %s · %s" % (name, raum), "kurz": "You meet %s." % (
        "tonight" if v["tag"] == z["tag"] else "tomorrow evening") + (" It is one of her favourite places." if lieb else ""),
        "folgen": []})


ERZAEHLER_STIMME = "Juno"      # Standard-Erzaehlerstimme (Katalog, englisch, ruhig) - in Einstellungen > Stimmen aenderbar


def stimme_von(modul, pid):
    """(Katalogname, Quelle) der Chatterbox-Stimme einer Figur: eigene Wahl in den Einstellungen > Karte
    (extensions.stimme.en, wie VoicePick in ST) > Modul (personen.<id>.stimme) > keine."""
    eigen = (cfg().get("stimmen") or {}).get(modul["id"], {})
    if pid in eigen:
        return (eigen[pid] or None), "eigene"
    if pid == szene.ERZAEHLER:            # Erzaehler: Modul-Vorgabe oder Standard, in den Einstellungen aenderbar
        return (modul.get("erzaehler_stimme") or ERZAEHLER_STIMME), "standard"
    p = modul["personen"].get(pid, {})
    if p.get("karte"):
        try:
            d = json.load(open(os.path.join(modul["karten_ordner"], p["karte"] + ".json"), encoding="utf-8"))
            name = ((d.get("data", d).get("extensions") or {}).get("stimme") or {}).get("en")
            if name:
                return name, "karte"
        except Exception:
            pass
    if p.get("stimme"):
        return p["stimme"], "modul"
    return stimme_von(modul, szene.ERZAEHLER)[0], "erzaehler"     # ohne eigene Stimme liest der Erzaehler


def audio(index):
    """wav fuer einen Eintrag der laufenden Szene - Chatterbox. Seit 16.10.2026 der ganze gezeigte Text
    (Rede, Handlung, sichtbare Gedanken) in der Stimme der Figur; Erzaehler-Eintraege in der Erzaehlerstimme."""
    z, modul = aktiv(), modul_laden()
    e = z["szene"]["log"][index]
    if e["art"] == "start" and e.get("vorlesen"):      # live, danach aus dem Speicher (Duc 01.11.2026)
        name, _ = stimme_von(modul, szene.ERZAEHLER)
        text = stimme.vorlesen(e["text"])
        return stimme.chatterbox(name, text, os.path.join(STAENDE, z["id"], "audio"), ganz=True) if name and text else None
    if e["art"] != "figur":
        return None
    name, _ = stimme_von(modul, e["wer"])
    text = stimme.vorlesen(e["gezeigt"])
    ordner = os.path.join(moddir(z["modul"]), "audio") if e.get("lob") else os.path.join(STAENDE, z["id"], "audio")   # Lob: vorab vertont
    return stimme.chatterbox(name, text, ordner, ganz=True) if name and text else None


def item_bild(mid, iid, z=None):
    """URL des Gegenstandsbilds (werkzeuge/item_bilder.py) oder None - mit Zeitstempel gegen alte Browser-Caches.
    Mit z: ein Selfie-Andenken zeigt das Selfie, das Duc bekommen hat (Raum + Nacktheitsgrad, kern/ereignisse.py)."""
    s = ((z or {}).get("selfie_bilder") or {}).get(iid)
    if s and os.path.isfile(os.path.join(moddir(mid), "selfies", s + ".webp")):
        return "/selfie/%s.webp" % s
    pfad = os.path.join(moddir(mid), "items", iid + ".webp")
    return "/itembild/%s?v=%d" % (iid, int(os.path.getmtime(pfad))) if os.path.isfile(pfad) else None


def ascii_name(modul, pid):
    """Kurzname ohne Akzente fuer englische Chronik-Saetze (Totò -> Toto)."""
    n = handel.anzeigename(modul, pid)
    return "".join(c for c in unicodedata.normalize("NFKD", n) if not unicodedata.combining(c))


def handel_bilder(h, mid, z=None):
    if not h:
        return h
    hid = h.get("haendler")
    if z is not None and hid:               # Haendler-Buehne (16.10.2026, Haendler aus rollen)
        modul = modul_laden(mid)
        hl = handel.haendler_laden(modul)
        t = handel.haendler_auftritt(z, modul)
        sets = buehne.sets(cfg(), modul, hid)
        setname = next(iter(sets), None)
        leg = legenden_gruss(z, mid, hid, "__haendler")              # Dorf redet (30.10.2026): Legende statt Gruss
        if leg:
            t["gruss"] = {"id": leg["id"], "text": leg["text"], "gefuehl": leg["gefuehl"]}
        for stimmung, zeile in t.items():
            zeile["sprite"] = buehne.sprite(cfg(), modul, hid, setname, zeile.get("gefuehl") or "neutral",
                                            zeile["id"]) if setname else None
        bg = hl.get("hintergrund")
        t["bild"] = "/bg/" + bg if bg and buehne.hintergrund_datei(cfg(), bg) else None
        t["stimme"] = bool(stimme_von(modul, hid)[0])
        h["haendler_buehne"] = t
    if z is not None:                       # Buehnen der anderen Laeden (eden_rise, 18.10.2026): wie beim Haendler
        modul = modul_laden(mid)
        h["buehnen"] = {lid: laden_auftritt(z, modul, mid, lid) for lid in h["laeden"] if lid != hid}
    for l in h["laeden"].values():
        for w in l["waren"] or []:
            w["bild"] = item_bild(mid, w["id"])
    for w in h["ankauf"]:
        w["bild"] = item_bild(mid, w["id"])      # Items und Yacht-Waren (champagne, tender_prop ...)
    for w in h["inventar_info"]:
        if "bild" not in w:                  # Ernte unterwegs (Stapeln 28.10.2026) bringt ihr Bild schon mit
            w["bild"] = item_bild(mid, w["id"], z)
    for w in h.get("tasche") or []:
        w["bild"] = item_bild(mid, w["id"])
    k = (z or {}).get("laden_kommentar")
    if k and k.get("nr") == len(z.get("buchungen", [])):     # nur direkt nach dem Kauf, danach wieder der Gruss
        modul = modul_laden(mid)
        L = laden_zeilen(mid).get(k["laden"]) or {}
        if k["laden"] == hid:                # Haendler: eigene Sprite-Auswahl wie beim Gruss
            sets = buehne.sets(cfg(), modul, hid)
            setname = next(iter(sets), None)
            spr = buehne.sprite(cfg(), modul, hid, setname, k["gefuehl"], k["id"]) if setname else None
        else:
            spr = event_sprite(modul, z, k["wer"], L.get("set"), k["gefuehl"], k["id"])
        h["kommentar"] = dict(k, name=handel.anzeigename(modul, k["wer"]), stimme=bool(stimme_von(modul, k["wer"])[0]),
                              sprite=spr)
    if z is not None:
        for j in h["jobs"]:                     # Missionen mit Gesicht und Buehne (17.10.2026)
            j.update(missions_buehne(modul, z, j["von"], "neutral", j["id"]))
            j["angebot"] = handel.job_angebot_zeile(z, modul, j["von"], j["id"])
            j["braucht_bild"] = item_bild(mid, j["braucht"]) if j.get("braucht") else None
            j["werkzeug_bild"] = item_bild(mid, j["werkzeug_da"]) if j.get("werkzeug_da") else None
            if j["angebot"]:
                j["angebot"]["sprite"] = missions_buehne(modul, z, j["von"], j["angebot"]["gefuehl"], j["id"])["sprite"]
            j["stimme"] = bool(stimme_von(modul, j["von"])[0])
            j["frau"] = bool(modul["personen"][j["von"]].get("romanzierbar"))
    return h


def job_ergebnis_ansicht(z, modul):
    e = z.get("job_ergebnis")
    if not e or e["pid"] not in modul["personen"]:
        return None
    e = dict(e)
    k = e.get("kommentar") or {}
    e.update(missions_buehne(modul, z, e["pid"], k.get("gefuehl") or ("joy" if e["ok"] else "disappointment"), e["id"]))
    p = modul["personen"][e["pid"]]
    e["name"] = p["name"]
    e["stimme"] = bool(stimme_von(modul, e["pid"])[0])
    return e


def figuren_profile(z, modul):
    """Figurenprofile (Vorlieben, 18.10.2026): alle bekannten Personen mit Vertrauen - Bild im Lieblingsraum."""
    c = cfg()
    bekannt = set(z.get("bekannt") or modul["personen"])
    out = []
    for pid, p in modul["personen"].items():
        if "vertrauen." + pid not in z["werte"] or pid not in bekannt:
            continue
        orte = p.get("lieblingsorte") or []
        ab = p.get("ablauf") or {}
        ort = next((o for o in orte if o in modul["raeume"]), None) or next(
            (o for o in [ab.get("*")] + list(ab.values()) if o in modul["raeume"]), None)
        setname = buehne.set_waehlen(c, modul, pid, {"ort": ort}, "tag", None)
        out.append({"id": pid, "name": p["name"], "kurz": handel.anzeigename(modul, pid),
                    "frau": bool(p.get("romanzierbar")), "pronomen": p.get("pronomen", "sie"),
                    "vertrauen": z["werte"].get("vertrauen." + pid, 0),
                    "begehren": z["werte"].get("begehren." + pid) if p.get("romanzierbar") else None,
                    "sprite": buehne.sprite(c, modul, pid, setname, "joy", pid + "-profil") if setname else None,
                    "avatar": buehne.sprite(c, modul, pid, setname, "neutral", pid) if setname else None,
                    "ort": raum_name(modul["raeume"][ort]) if ort else "",
                    "lieblingsort": bool(orte), "bild": buehne.hintergrund(modul, ort, "tag") if ort else
                    ("/bg/" + p["hintergrund"] if p.get("hintergrund") else None)})   # ohne Raum: eigener Hintergrund (29.10.)
    return out


def laden_zeilen(mid=None):
    pfad = os.path.join(moddir(mid), "laeden.json")
    return json.load(open(pfad, encoding="utf-8"))["laeden"] if os.path.exists(pfad) else {}


def laden_auftritt(z, modul, mid, lid):
    """Je Stimmung ein Satz der Ladenfigur (Gruss nach Vertrauen), mit Sprite und Hintergrund."""
    L = laden_zeilen(mid).get(lid)
    l = modul["laeden"][lid]
    if not L or not l.get("wer"):
        return None
    wer = l["wer"]
    vt = z["werte"].get("vertrauen." + wer, 0)
    stufen = L.get("gruss_stufen") or {}
    gruss = next((g for g, (a, b) in stufen.items() if a <= vt <= b), next(iter(stufen), None))
    kalt = lid == "petru" and abbau.petru_kalt(z)            # nach Weg B: dunkler Laden (29.10.2026)
    if kalt and L["zeilen"].get("kalt_gruss"):
        gruss = "kalt_gruss"
    allein = lid == "danzel" and "rt_ausgang_getrennt" in z.get("flags", [])   # Trio zerbrochen (E-112): knapp und ernst
    if allein and L["zeilen"].get("gruss_allein"):
        gruss = "gruss_allein"
    rng = random.Random("%s-%d-%s-%d-%s" % (z["id"], z["tag"], z["phase"], len(z.get("buchungen", [])), lid))
    out = {"wer": wer, "name": handel.anzeigename(modul, wer), "text": (kalt and L.get("text_kalt")) or (allein and L.get("text_allein")) or l.get("text", "")}
    for stimmung in ["gruss"] + [g for g in L["zeilen"] if not g.startswith("gruss")]:
        gruppe = gruss if stimmung == "gruss" else stimmung
        liste = L["zeilen"].get(gruppe) or []
        if not liste:
            continue
        i = rng.randrange(len(liste))
        gef = (L.get("gefuehl") or {}).get(gruppe) or (L.get("gefuehl") or {}).get(stimmung, "neutral")
        out[stimmung] = {"id": "laden.%s.%s.%d" % (lid, gruppe, i), "text": liste[i],
                         "sprite": event_sprite(modul, z, wer, L.get("set"), gef, "%s%d" % (gruppe, i))}
    leg = None if kalt or allein else legenden_gruss(z, mid, wer, lid)       # Dorf redet (30.10.2026): Legende statt Gruss
    if leg:
        out["gruss"] = {"id": leg["id"], "text": leg["text"],
                        "sprite": event_sprite(modul, z, wer, L.get("set"), leg["gefuehl"], "leg" + leg["id"])}
    bg = mochis.bild(z, modul) if l.get("mochis") else L.get("hintergrund")
    out["bild"] = "/bg/" + bg if bg and buehne.hintergrund_datei(cfg(), bg) else None
    out["stimme"] = bool(stimme_von(modul, wer)[0])
    return out


def legenden_gruss(z, mid, wer, lid):
    """Legenden-Zeile als Begruessung im Laden (Dorf redet, 30.10.2026). Bleibt fuer diesen Besuch (Tag + Phase)
    dieselbe, auch wenn die Ansicht neu gebaut wird; danach ist sie gehoert. -> {id, text, gefuehl} oder None."""
    besuch = z.setdefault("legenden_laden", {})
    jetzt = [z["tag"], z.get("phase")]
    alt = besuch.get(lid)
    if alt and alt[:2] == jetzt:
        l = legenden.daten(moddir(mid))["zeilen"].get(alt[2])
        return {"id": "leg." + alt[2], "text": l["text"], "gefuehl": l.get("gefuehl", "joy")} if l else None
    l = legenden.zeile_fuer(z, moddir(mid), wer, "laden")
    if not l:
        return None
    legenden.markieren(z, l)
    besuch[lid] = jetzt + [l["id"]]
    return {"id": "leg." + l["id"], "text": l["text"], "gefuehl": l.get("gefuehl", "joy")}


def event_sprite(modul, z, pid, setname, gefuehl, salz):
    c = cfg()
    vorhanden = buehne.sets(c, modul, pid)
    if not vorhanden:
        return None
    if setname and setname not in vorhanden:         # "Flamenco Noche" -> "alva_flamenco_noche", "Nude" -> "nude"
        norm = lambda x: x.lower().replace(" ", "_").replace("'", "")
        setname = next((v for v in vorhanden if norm(v) in (norm(setname), "%s_%s" % (pid, norm(setname)))), None)
    if setname not in vorhanden:
        setname = buehne.set_waehlen(c, modul, pid, {"ort": buehne.wo_ist(z, modul, pid)}, z["phase"], None, z)
    return buehne.sprite(c, modul, pid, setname, gefuehl, salz)


def event_bild(ort, fern):
    """Hintergrund eines Ereignisses: Raum (bzw. Ducs aktueller Ort) oder der Ort eines Anrufers."""
    z, modul = aktiv(), modul_laden()
    if fern:
        datei = {"megan_office": "eden_hq_megan_office", "eden_lobby": "eden_hq_lobby",
                 "krankenhaus": "eden_patient_room"}.get(ort or "")
        if not datei and z and ort in modul["raeume"]:          # Videoanruf von Bord: ihr Raum im Bild (Duc 03.11.2026)
            return buehne.hintergrund(modul, ort, z["phase"])
        if not datei:
            return z.get("letztes_bild") if z else None         # Anruf ohne Bild: Duc bleibt, wo er ist
        nacht = z and z["phase"] in ("abend", "nacht") and ort != "eden_lobby"
        return "/bg/%s%s.png" % (datei, "_night" if nacht else "")
    if not ort:
        return z.get("letztes_bild") if z else None
    return buehne.hintergrund(modul, ort, z["phase"]) if ort in modul["raeume"] else None


def missions_buehne(modul, z, pid, gefuehl, salz=""):
    """Wo die Figur gerade ist (Tagesablauf) -> Hintergrund + Sprite im passenden Outfit und Gefuehl."""
    ort = buehne.wo_ist(z, modul, pid)
    c = cfg()
    setname = buehne.set_waehlen(c, modul, pid, {"ort": ort}, z["phase"], None, z)
    p = modul["personen"].get(pid) or {}
    heim = next((o for o in (p.get("lieblingsorte") or []) if o in modul["raeume"]), None)   # nicht im Raum (29.10.):
    bild = buehne.hintergrund(modul, ort or heim, z["phase"]) if ort or heim else \
        ("/bg/" + p["hintergrund"] if p.get("hintergrund") else None)                  # Lieblingsraum, sonst eigener Hintergrund
    return {"sprite": buehne.sprite(c, modul, pid, setname, gefuehl, salz) if setname else None,
            "bild": bild,
            "ort_name": raum_name(modul["raeume"][ort]) if ort else ""}


def event_zeile(schl):
    """'<event>#z3' / '<event>#o1' -> (Figur, Satz) - nur Saetze aus ereignisse.json."""
    d = ereignisse.daten(moddir())
    eid, _, teil = schl.partition("#")
    ev = (d or {}).get("_index", {}).get(eid)
    # Erzaehlerin liest den Lagetext der Ortsbilder (Duc 02.11.2026): gleicher Text wie in vertonen_eden_rise.saetze(),
    # sonst findet stimme.chatterbox die Aufnahme nicht; Lagen mit {Platzhalter} sind nicht vertont
    if ev and teil == "l" and ev.get("art") == "ort" and ev.get("lage") and "{" not in ev["lage"]:
        return szene.ERZAEHLER, ev["lage"].replace("*", "")
    if not ev or len(teil) < 2 or not teil[1:].isdigit():
        return None, None
    i = int(teil[1:])
    if teil[0] == "z" and i < len(ev["zeilen"]):
        return ev["zeilen"][i]["wer"], ev["zeilen"][i]["text"]
    if teil[0] == "o" and i < len(ev["optionen"]) and ev["optionen"][i].get("zeile"):
        return ev["optionen"][i]["zeile"]["wer"], ev["optionen"][i]["zeile"]["text"]
    if teil[0] == "f" and i < len(ev["optionen"]) and ev["optionen"][i].get("zeile_fehlschlag"):   # Favours (29.10.2026)
        return ev["optionen"][i]["zeile_fehlschlag"]["wer"], ev["optionen"][i]["zeile_fehlschlag"]["text"]
    return None, None


def stimmen_ansicht():
    modul = modul_laden()
    personen = []
    for pid, p in modul["personen"].items():
        name, quelle = stimme_von(modul, pid)
        personen.append({"id": pid, "name": p["name"], "stimme": name or "", "quelle": quelle,
                         "romanzierbar": bool(p.get("romanzierbar"))})
    name, quelle = stimme_von(modul, szene.ERZAEHLER)
    personen.append({"id": szene.ERZAEHLER, "name": "Erzähler", "stimme": name or "", "quelle": quelle, "romanzierbar": False})
    kat = [{"name": s["name"], "herkunft": s.get("herkunft", ""), "alter": s.get("alter", ""),
            "lage": s.get("lage", ""), "typ": s.get("typ") or [], "farbe": s.get("farbe") or []} for s in stimme.katalog()]
    return {"personen": personen, "katalog": kat, "chatterbox": stimme.chatterbox_bereit()}


# ------------------------------------------------------------------ Ausschnitte der Figuren-Kreise (17.10.2026)
# Duc legt je Figur fest, welcher Teil des Sprites im Kreis steht. Gespeichert wird kein Bild, nur Mittelpunkt
# (cx, cy, 0..1 im Sprite), Zoom (Kreisdurchmesser = Spritebreite / zoom) und Seitenverhaeltnis r = Hoehe/Breite -
# so gilt der Ausschnitt fuer jedes Gefuehl und jedes Outfit der Figur. Ablage in eden-config.json je Modul.
def ausschnitte(mid=None):
    return ((cfg().get("ausschnitte") or {}).get(mid or modul_laden()["id"])) or {}


def ausschnitte_ansicht():
    modul = modul_laden()
    out = []
    for pid, p in modul["personen"].items():
        vorhanden = buehne.sets(cfg(), modul, pid)
        if not vorhanden:
            continue
        std = p.get("set_standard") if p.get("set_standard") in vorhanden else next(iter(vorhanden))
        andere = [s for s in vorhanden if s != std]
        beispiele = [buehne.sprite(cfg(), modul, pid, std, "joy", pid)] + \
                    [buehne.sprite(cfg(), modul, pid, s, g, pid) for s, g in zip(andere, ("neutral", "surprise", "amusement"))]
        out.append({"id": pid, "name": p["name"], "romanzierbar": bool(p.get("romanzierbar")),
                    "sprite": buehne.sprite(cfg(), modul, pid, std, "neutral", pid),
                    "beispiele": [b for b in beispiele if b][:4]})
    out.sort(key=lambda x: (not x["romanzierbar"], x["name"]))
    return {"figuren": out, "ausschnitte": ausschnitte(modul["id"])}


def ausschnitt_setzen(daten):
    modul = modul_laden()
    pid = daten.get("id") or ""
    if pid not in modul["personen"]:
        raise ValueError("Unbekannte Figur.")
    alle = cfg().get("ausschnitte") or {}
    m = dict(alle.get(modul["id"]) or {})
    if daten.get("loeschen"):
        m.pop(pid, None)
    else:
        c = daten.get("crop") or {}
        try:
            m[pid] = {k: round(float(c[k]), 4) for k in ("cx", "cy", "zoom", "r")}
        except (KeyError, TypeError, ValueError):
            raise ValueError("Ausschnitt unvollstaendig.")
    alle[modul["id"]] = m
    cfg_setzen(ausschnitte=alle)
    return ausschnitte_ansicht()


# ------------------------------------------------------------------ Profilbild (17.10.2026)
# Duc: eigenes Gesicht als Kreis neben seinen Texten. Ziel "duc" gilt in allen Durchlaeufen, "persona_<id>" nur fuer
# diese Rolle (hat Vorrang). Zugeschnitten wird im Browser (Duc legt den Kreis selbst fest); hier liegen das fertige
# 512er-Quadrat, das Original (Upload) bzw. der Verweis auf den ST-Avatar und die Zuschnitt-Werte zum Nachjustieren.
PROFIL_ZIEL = re.compile(r"duc|persona_[a-z0-9_]+")
PROFIL_DATEI = re.compile(r"(duc|persona_[a-z0-9_]+)(_original)?\.(png|jpg|webp)")
BILD_ENDUNG = (".png", ".jpg", ".jpeg", ".webp")
DATA_URL = re.compile(r"data:image/(png|jpeg|webp);base64,(.+)", re.S)


def profil_index():
    try:
        return json.load(open(os.path.join(PROFIL, "profil.json"), encoding="utf-8"))
    except Exception:
        return {}


def st_avatare():
    """Ducs Persona-Avatare aus SillyTavern (User Avatars), neueste zuerst."""
    ordner = os.path.join(cfg()["st_daten"], "User Avatars")
    try:
        namen = [n for n in os.listdir(ordner) if n.lower().endswith(BILD_ENDUNG)]
    except OSError:
        return ordner, []
    return ordner, sorted(namen, key=lambda n: os.path.getmtime(os.path.join(ordner, n)), reverse=True)


def profil_ansicht(z=None):
    idx, out = profil_index(), {"bilder": {}, "info": {}}
    for ziel, info in idx.items():
        pfad = os.path.join(PROFIL, ziel + ".png")
        if not os.path.isfile(pfad):
            continue
        out["bilder"][ziel] = "/profil/%s.png?v=%d" % (ziel, int(os.path.getmtime(pfad)))
        q = info.get("quelle", "")
        original = ("/stavatar/" + urllib.parse.quote(q[3:])) if q.startswith("st:") else \
            ("/profil/%s?v=%d" % (info["original"], int(os.path.getmtime(os.path.join(PROFIL, info["original"]))))
             if info.get("original") and os.path.isfile(os.path.join(PROFIL, info["original"])) else None)
        out["info"][ziel] = {"quelle": q, "crop": info.get("crop"), "original": original}
    pid = ((z or {}).get("persona") or {}).get("id")
    out["persona"] = pid
    out["aktiv"] = out["bilder"].get("persona_%s" % pid) if pid else None
    out["aktiv"] = out["aktiv"] or out["bilder"].get("duc")
    return out


def profil_setzen(daten):
    ziel = daten.get("ziel") or ""
    if not PROFIL_ZIEL.fullmatch(ziel):
        raise ValueError("Unbekanntes Ziel fuer das Profilbild.")
    os.makedirs(PROFIL, exist_ok=True)
    idx = profil_index()
    alt = idx.get(ziel) or {}
    if daten.get("loeschen"):
        for datei in (ziel + ".png", alt.get("original")):
            if datei and os.path.isfile(os.path.join(PROFIL, datei)):
                os.remove(os.path.join(PROFIL, datei))
        idx.pop(ziel, None)
    else:
        m = DATA_URL.fullmatch(daten.get("bild") or "")
        if not m or m.group(1) != "png":
            raise ValueError("Zuschnitt fehlt.")
        quelle = daten.get("quelle") or ""
        if quelle.startswith("st:"):
            if quelle[3:] not in st_avatare()[1]:
                raise ValueError("Diesen SillyTavern-Avatar gibt es nicht.")
        elif quelle != "upload":
            raise ValueError("Unbekannte Bildquelle.")
        open(os.path.join(PROFIL, ziel + ".png"), "wb").write(base64.b64decode(m.group(2)))
        neu = {"quelle": quelle, "crop": daten.get("crop"), "zeit": time.strftime("%Y-%m-%d %H:%M")}
        o = DATA_URL.fullmatch(daten.get("original") or "")
        if o and quelle == "upload":                  # neues Original hochgeladen
            if alt.get("original") and os.path.isfile(os.path.join(PROFIL, alt["original"])):
                os.remove(os.path.join(PROFIL, alt["original"]))
            neu["original"] = "%s_original.%s" % (ziel, {"jpeg": "jpg"}.get(o.group(1), o.group(1)))
            open(os.path.join(PROFIL, neu["original"]), "wb").write(base64.b64decode(o.group(2)))
        elif quelle == "upload" and alt.get("quelle") == "upload" and alt.get("original"):
            neu["original"] = alt["original"]         # nur neu zugeschnitten
        elif alt.get("original") and os.path.isfile(os.path.join(PROFIL, alt["original"])):
            os.remove(os.path.join(PROFIL, alt["original"]))  # jetzt ST-Avatar - altes Upload-Original weg
        idx[ziel] = neu
    json.dump(idx, open(os.path.join(PROFIL, "profil.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return profil_ansicht(aktiv())


# ------------------------------------------------------------------ Bild-Cache (28.10.2026, Spieltest: 22 MB beim Start)
# Hintergruende und Sprites liegen als PNG mit 1,5-2 MB vor. Beim ersten Abruf entsteht eine WebP-Kopie (gleiche
# Optik, ~10-20 % der Groesse) in spielstaende/_webp; die Originale - auch die Sprites in SillyTavern - bleiben unberuehrt.
WEBP_AB = 150 * 1024            # kleinere Bilder lohnen den Umweg nicht
_webp_sperre = threading.Lock()


def webp_kopie(pfad):
    """-> Pfad einer WebP-Kopie oder None (zu klein, kein Pillow, Fehler). Schluessel: Pfad, Groesse, Aenderungszeit."""
    try:
        st = os.stat(pfad)
        if st.st_size < WEBP_AB:
            return None
        import hashlib
        schluessel = hashlib.sha1(("%s|%d|%d" % (os.path.abspath(pfad), st.st_size, st.st_mtime_ns)).encode()).hexdigest()
        ziel = os.path.join(STAENDE, "_webp", schluessel + ".webp")
        if os.path.isfile(ziel):
            return ziel
        from PIL import Image
        with _webp_sperre:
            if not os.path.isfile(ziel):
                os.makedirs(os.path.dirname(ziel), exist_ok=True)
                with Image.open(pfad) as bild:
                    alpha = bild.mode in ("RGBA", "LA") or (bild.mode == "P" and "transparency" in bild.info)
                    bild = bild.convert("RGBA" if alpha else "RGB")
                    tmp = ziel + ".tmp"
                    bild.save(tmp, "WEBP", quality=85, alpha_quality=90, method=4)
                os.replace(tmp, ziel)
        return ziel
    except Exception:
        return None


# ------------------------------------------------------------------ HTTP
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def senden(self, code, daten, typ="application/json"):
        roh = daten if isinstance(daten, bytes) else json.dumps(daten, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", typ + "; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(roh)

    def do_GET(self):
        pfad = self.path.split("?")[0]
        debug = "debug=1" in self.path
        if pfad in ("/", "/index.html"):
            return self.senden(200, open(os.path.join(BASE, "client", "index.html"), "rb").read(), "text/html")
        if pfad == "/api/stand":
            return self.senden(200, ansicht(aktiv(), debug))
        teile = [urllib.parse.unquote(t) for t in pfad.split("/")[1:]]
        try:
            if teile[:2] == ["plugins", "eden-music"] and len(teile) == 3:
                name = teile[2]
                if name in ("eden-music.js", "eden-music.css"):
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-music", name),
                                      "text/javascript" if name.endswith(".js") else "text/css", cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if pfad == "/wiki/kampf":
                return self.datei(os.path.join(BASE, "client", "wiki", "kampf.html"), "text/html", cache=False)
            if pfad == "/musik/credits":
                return self.datei(os.path.join(BASE, "module", "eden_rise", "musik", "CREDITS.html"),
                                  "text/html", cache=False)
            if teile[:2] == ["musik", "audio"] and len(teile) == 3:
                path = musik.audio_path(BASE, modul_laden()["id"], teile[2])
                if path:
                    return self.musik_datei(path)
                return self.senden(404, {"fehler": "Musik nicht gefunden"})
            # Sound-Effekte (18.10.2026): nur das feste Plugin und Dateien aus module/<modul>/sfx/ (kern/sfx.py prueft).
            if teile[:2] == ["plugins", "eden-sfx"] and len(teile) == 3:
                if teile[2] == "eden-sfx.js":
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-sfx", "eden-sfx.js"),
                                      "text/javascript", cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[0] == "sfx" and len(teile) == 2:
                path = sfx.audio_path(BASE, modul_laden()["id"], teile[1])
                if path:
                    return self.datei(str(path), "audio/mpeg")
                return self.senden(404, {"fehler": "Sound nicht gefunden"})
            if teile[:2] == ["plugins", "eden-dice"]:
                # Public plugin files only; reject traversal and serve known file types.
                from pathlib import Path
                wurzel = Path(BASE, "client", "plugins", "eden-dice").resolve()
                ziel = wurzel.joinpath(*teile[2:]).resolve()
                mime = {".js": "text/javascript", ".css": "text/css", ".webp": "image/webp"}
                if ziel.is_relative_to(wurzel) and ziel.is_file() and ziel.suffix in mime:
                    return self.datei(str(ziel), mime[ziel.suffix], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[0] == "farm" and len(teile) == 3 and teile[1] in ("tiere", "fische", "abbau", "koeder") and re.fullmatch(r"[a-z0-9_]+\.png", teile[2]):
                datei = os.path.join(moddir(), "farm", teile[1], teile[2])        # Tier-, Fisch- und Abbau-Sprites (27./28.10.2026)
                if os.path.isfile(datei):
                    return self.datei(datei, "image/png")
                return self.senden(404, {"fehler": "Bild fehlt noch"})
            if teile[:2] == ["plugins", "eden-ui"] and len(teile) == 3:         # Gemeinsame UI-Bausteine und Icons (30.10.2026)
                mime = {"eden-ui.js": "text/javascript", "eden-ui.css": "text/css", "icons.svg": "image/svg+xml"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-ui", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-bewegung"] and len(teile) == 3:   # Mikro-Interaktionen (ui_stil.md 2b, 02.11.2026)
                mime = {"eden-bewegung.js": "text/javascript", "eden-bewegung.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-bewegung", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-angeln"] and len(teile) == 3:     # Angel-Minispiel (27.10.2026)
                mime = {"eden-angeln.js": "text/javascript", "eden-angeln.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-angeln", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-abbau"] and len(teile) == 3:      # Abbauen an Rastplaetzen + Petrus Werkzeuge (28.10.2026)
                mime = {"eden-abbau.js": "text/javascript", "eden-abbau.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-abbau", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-mochis"] and len(teile) == 3:  # Bibis Tierstation (31.10.2026)
                mime = {"eden-mochis.js": "text/javascript", "eden-mochis.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-mochis", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-schneider"] and len(teile) == 3:  # Danzels Auftraege (30.10.2026)
                mime = {"eden-schneider.js": "text/javascript", "eden-schneider.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-schneider", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-schiessen"] and len(teile) == 3:  # Holms Wette (30.10.2026)
                mime = {"eden-schiessen.js": "text/javascript", "eden-schiessen.css": "text/css",
                        **{n + ".webp": "image/webp" for n in ("flasche", "flasche2", "flasche3", "ton", "drohne", "moewe", "granate")}}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-schiessen", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-farm"] and len(teile) == 3:       # Farm-Fenster und Baukasten (27.10.2026)
                mime = {"eden-farm.js": "text/javascript", "eden-farm.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-farm", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[0] == "sprite" and len(teile) == 4:
                datei = buehne.sprite_datei(cfg(), modul_laden(), teile[1], teile[2], teile[3])
                if datei:
                    return self.datei(datei, "image/png")
            if teile[:2] == ["plugins", "eden-skills"]:
                from pathlib import Path
                wurzel = Path(BASE, "client", "plugins", "eden-skills").resolve()
                if teile[2:3] == ["preview"]:
                    relative = "/".join(teile[3:])
                    manifest = wurzel / "preview-files.json"
                    allowed = json.loads(manifest.read_text(encoding="utf-8")) if manifest.is_file() else []
                    preview_root = Path(BASE, "docs", "effekt-auswahl", "status-labor").resolve()
                    preview_file = preview_root.joinpath(*teile[3:]).resolve()
                    preview_mime = {".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".webp": "image/webp", ".json": "application/json", ".ogg": "audio/ogg"}
                    if relative in allowed and preview_file.is_relative_to(preview_root) and preview_file.is_file() and preview_file.suffix in preview_mime:
                        # Bilder und Klaenge cachen (Duc 01.11.2026): jede Zwischensequenz lud sonst 32 MB neu, 4 bis 14 s schwarzer Schirm
                        return self.datei(str(preview_file), preview_mime[preview_file.suffix], cache=preview_file.suffix in (".png", ".webp", ".ogg", ".mp3"))
                    return self.senden(404, {"fehler": "Vorschau-Datei nicht gefunden"})
                ziel = wurzel.joinpath(*teile[2:]).resolve()
                mime = {".js": "text/javascript", ".css": "text/css", ".png": "image/png"}
                if ziel.is_relative_to(wurzel) and ziel.is_file() and ziel.suffix in mime:
                    return self.datei(str(ziel), mime[ziel.suffix], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-expedition"] and len(teile) == 3:  # Expeditions-Bildschirm (26.10.2026)
                mime = {"eden-expedition.js": "text/javascript", "eden-expedition.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-expedition", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-tisch"] and len(teile) == 3:      # Tischszenen, Lieblingsgericht (27.10.2026)
                mime = {"eden-tisch.js": "text/javascript", "eden-tisch.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-tisch", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-tactics"] and len(teile) == 3:    # Taktik-Karte (Duc 31.10.2026)
                mime = {"eden-tactics.js": "text/javascript", "eden-tactics.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-tactics", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[0] == "taktikbild" and len(teile) == 2 and re.fullmatch(r"[A-Za-z0-9_]+\.webp", teile[1]):
                return self.datei(os.path.join(moddir(), "taktik", teile[1]), "image/webp", cache=True)
            if teile[:2] == ["plugins", "eden-storm"] and len(teile) == 3:      # Sturm an Tag 5 (27.10.2026)
                mime = {"eden-storm.js": "text/javascript", "eden-storm.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-storm", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-menu"] and len(teile) == 3:       # Pause-Menue (25.10.2026)
                mime = {"eden-menu.js": "text/javascript", "eden-menu.css": "text/css"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-menu", teile[2]), mime[teile[2]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-hearing"] and len(teile) == 3:    # Anhoerung (Variante B, 25.10.2026)
                mime = {"eden-hearing.js": "text/javascript", "eden-hearing.css": "text/css", "tisch.jpg": "image/jpeg"}
                if teile[2] in mime:
                    return self.datei(os.path.join(BASE, "client", "plugins", "eden-hearing", teile[2]), mime[teile[2]],
                                      cache=teile[2].endswith(".jpg"))
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[:3] == ["plugins", "eden-combat", "fx"] and len(teile) == 4 \
                    and re.fullmatch(r"[a-z_]+\.(webp|json)", teile[3]):       # Granaten-Bildfolgen (27.10.2026, granaten_fx.py)
                datei = os.path.join(BASE, "client", "plugins", "eden-combat", "fx", teile[3])
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp" if teile[3].endswith(".webp") else "application/json")
                return self.senden(404, {"fehler": "Effekt-Datei nicht gefunden"})
            if teile[:2] == ["plugins", "eden-combat"] and len(teile) == 3:     # Kampfbildschirm (Etappe 3)
                mime = {".js": "text/javascript", ".css": "text/css", ".html": "text/html"}    # .html: Spezialangriff-Zwischensequenz (26.10.2026)
                if teile[2] in ("eden-combat.js", "eden-combat.css", "eden-combat-effects.js", "eden-combat-fx.html", "eden-qte.js"):
                    datei = os.path.join(BASE, "client", "plugins", "eden-combat", teile[2])
                    if os.path.isfile(datei):
                        return self.datei(datei, mime[os.path.splitext(datei)[1]], cache=False)
                return self.senden(404, {"fehler": "Plugin-Datei nicht gefunden"})
            if teile[0] == "kampfbild" and len(teile) == 3 and re.fullmatch(r"[A-Za-z0-9_]+", teile[1]) \
                    and re.fullmatch(r"[a-z_]+\.webp", teile[2]):
                datei = os.path.join(moddir(), "kampf", teile[1], teile[2])
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp")
            if teile[0] == "favourfoto" and len(teile) == 2 and re.fullmatch(r"[a-z0-9_]+\.webp", teile[1]):
                datei = os.path.join(moddir(), "favours", teile[1])       # Favour-Dank mit Foto (29.10.2026)
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp")
            if teile[0] == "selfie" and len(teile) == 2 and re.fullmatch(r"[a-z]+_[a-z]+_[1-3]\.webp|bibi_fang_[a-z]+_[ab]\.webp", teile[1]):   # + Bibis Tier-Selfies A/B (02.11.2026)
                datei = os.path.join(moddir(), "selfies", teile[1])       # Selfie-Events (26.10.2026)
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp")
            if teile[0] == "chipbild" and re.fullmatch(r"[a-z0-9_-]+\.png", teile[-1]) and len(teile) in (2, 3) \
                    and (len(teile) == 2 or teile[1] == "kat"):
                datei = os.path.join(moddir(), "chips", *teile[1:])
                if os.path.isfile(datei):
                    return self.datei(datei, "image/png")
            if teile[0] == "charakterbild" and len(teile) == 2 and re.fullmatch(r"(Duc|Bg)[A-Za-z]+", teile[1]):
                datei = os.path.join(moddir(), "charakter", teile[1] + ".webp")      # Character-Fenster (werkzeuge\charakter_bild.py)
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp")
            if teile[0] == "charakterbild" and len(teile) == 4 and teile[1] == "gefuehle" \
                    and re.fullmatch(r"Duc[A-Za-z]+", teile[2]) and re.fullmatch(r"[a-z0-9_]+", teile[3]):
                datei = os.path.join(moddir(), "charakter", "gefuehle", teile[2], teile[3] + ".webp")   # Ducs Gefuehle (03.11.2026)
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp")
            if teile[0] == "itembild" and len(teile) == 2 and re.fullmatch(r"[a-z0-9_]+", teile[1]):
                datei = os.path.join(moddir(), "items", teile[1] + ".webp")
                if os.path.isfile(datei):
                    return self.datei(datei, "image/webp")
            if teile[0] == "bg" and len(teile) == 2:
                datei = buehne.hintergrund_datei(cfg(), teile[1])
                if datei:
                    return self.datei(datei, "image/" + ("jpeg" if datei.lower().endswith((".jpg", ".jpeg")) else "png"))
            if pfad == "/api/kuechen_vorschau":          # Baukasten (27.10.2026): was kommt heraus? Nur lesen, bucht nichts
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                try:
                    za, mo = aktiv(), modul_laden()
                    fuer = (q.get("fuer") or ["crew"])[0]
                    return self.senden(200, kuechen.vorschau(za, mo, (q.get("basis") or [""])[0], (q.get("haupt") or [""])[0],
                                                             (q.get("akzent") or [""])[0],
                                                             handel.crew_an_bord(za, mo) if fuer == "crew" else [fuer]))
                except (ValueError, KeyError) as e:
                    return self.senden(400, {"fehler": str(e) or "Unbekannte Zutat."})
            if pfad == "/api/audio":
                i = int(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)["i"][0])
                datei = audio(i)
                if datei:
                    return self.datei(datei, "audio/wav" if datei.endswith(".wav") else "audio/mpeg", cache=False)
                return self.senden(204, b"", "text/plain")
            if pfad == "/api/zeile":
                # Feste Haendler-Saetze vertonen (Toto) - nur bekannte Saetze, nie freier Text aus der URL
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                zid = (q.get("id") or [""])[0]
                ordner = os.path.join(moddir(), "audio_zeilen")
                hid = rollen.rolle(modul_laden(), "haendler")
                if zid.startswith("laden.") and zid.split(".")[1] != hid:       # Laden-Saetze (vorab vertont)
                    _, lid, gruppe, i = (zid.split(".") + ["", "", ""])[:4]
                    liste = ((laden_zeilen().get(lid) or {}).get("zeilen") or {}).get(gruppe) or []
                    pid = (laden_zeilen().get(lid) or {}).get("wer")
                    text = liste[int(i)] if i.isdigit() and int(i) < len(liste) else None
                    name = stimme_von(modul_laden(), pid)[0] if pid and text else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("teil."):        # Kommentar der Ladenfigur beim Kauf eines Teils (vorab vertont)
                    k = (modul_laden()["items"].get(zid[5:]) or {}).get("kommentar") or {}
                    pid, text = k.get("wer"), k.get("text")
                    name = stimme_von(modul_laden(), pid)[0] if pid and text else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("ev."):          # Ereignis-Zeilen (B5): vorab vertont in <modul>\audio
                    pid, text = event_zeile(zid[3:])
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("vh."):          # Anhoerung (25.10.2026): Megan, Aussagen - vorab vertont
                    pid, text = anhoerung.zeile(zid, modul_laden(), moddir())
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("st."):          # Sturm an Tag 5 (27.10.2026): vorab vertont
                    pid, text = sturm.zeile(zid, moddir())
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("fred."):        # Frederico bringt den Einkauf rueber (27.10.2026): feste Saetze, vorab vertont
                    pid, text = kuechen.zeile(modul_laden(), zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("tisch."):       # Tischszenen (27.10.2026): erster Bissen und Erinnerungen, vorab vertont
                    pid, text = tisch.zeile(modul_laden(), zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("tut."):         # Maxwells Tutorial-Saetze (24.10.2026): vorab vertont
                    pid, text = tutorial.zeile(zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("mochis."):      # Bibis Overlay nach dem ersten Fang (01.11.2026): vorab vertont
                    pid, text = mochis.zeile(modul_laden(), zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("rast."):        # Rast-Anrufe (26.10.2026): rast.<pid>.<stufe>.<n>, vorab vertont
                    _, pid, stufe, i = (zid.split(".") + ["", "", ""])[:4]
                    liste = (expedition.rast_texte(moddir()).get(pid) or {}).get(stufe) or []
                    text = liste[int(i)]["text"] if i.isdigit() and int(i) < len(liste) else None
                    name = stimme_von(modul_laden(), pid)[0] if text else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("leg."):         # Dorf redet (30.10.2026): Legenden-Zeilen, vorab vertont
                    pid, text = legenden.zeile(moddir(), zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("tk."):          # Taktik-Karte (Duc 02.11.2026): Szenen, Briefings, Appell, vorab vertont
                    pid, text = taktik.zeile(moddir(), zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("kampf."):       # feste Kampf-Saetze: Hinweise, Sprueche, Taunts beim Zoegern (03.11.2026)
                    wer, text = kampf.zeile(kampf.daten(moddir()) or {}, zid)
                    name = wer[7:] if wer and wer.startswith("stimme:") else stimme_von(modul_laden(), wer)[0] if wer else None
                    ordner = os.path.join(moddir(), "audio")
                elif zid.startswith("job."):         # Missions-Kommentare: vorab vertont in <modul>\audio
                    pid, text = handel.job_zeile(modul_laden(), zid)
                    name = stimme_von(modul_laden(), pid)[0] if pid else None
                    ordner = os.path.join(moddir(), "audio")
                else:                                # feste Saetze des Haendlers (vorab vertont in <modul>/audio, wie alle)
                    text = handel.haendler_zeile(modul_laden(), zid)
                    name = stimme_von(modul_laden(), hid)[0] if hid else None
                    ordner = os.path.join(moddir(), "audio")
                datei = stimme.chatterbox(name, text, ordner, ganz=True) if text and name else None
                if datei:
                    return self.datei(datei, "audio/wav")
                return self.senden(204, b"", "text/plain")
            if pfad == "/api/stimmen":
                return self.senden(200, stimmen_ansicht())
            if pfad == "/api/ausschnitte":
                return self.senden(200, ausschnitte_ansicht())
            if pfad == "/api/gesichter":        # Kreis-Ausschnitte je Sprite, werkzeuge/gesichter_messen.py
                datei = os.path.join(moddir(), "gesichter.json")
                return self.datei(datei, "application/json", cache=False) if os.path.isfile(datei) else self.senden(200, {})
            if pfad == "/api/st_avatare":
                return self.senden(200, [{"name": n, "url": "/stavatar/" + urllib.parse.quote(n)} for n in st_avatare()[1]])
            if teile[0] == "stavatar" and len(teile) == 2:
                ordner, namen = st_avatare()
                if teile[1] in namen:           # nur Dateien aus der Liste, kein freier Pfad
                    endung = teile[1].lower().rsplit(".", 1)[-1]
                    return self.datei(os.path.join(ordner, teile[1]), "image/" + {"jpg": "jpeg"}.get(endung, endung))
            if teile[0] == "profil" and len(teile) == 2 and PROFIL_DATEI.fullmatch(teile[1]):
                datei = os.path.join(PROFIL, teile[1])
                if os.path.isfile(datei):
                    endung = teile[1].rsplit(".", 1)[-1]
                    return self.datei(datei, "image/" + {"jpg": "jpeg"}.get(endung, endung))
            if pfad == "/api/stimme_probe":
                name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)["name"][0]
                datei = stimme.chatterbox(name, stimme.PROBE, os.path.join(STAENDE, "_proben"), ganz=True)
                if datei:
                    return self.datei(datei, "audio/wav")
                return self.senden(404, {"fehler": "Stimme nicht im Katalog"})
        except Exception as e:
            traceback.print_exc()
            return self.senden(500, {"fehler": str(e)})
        self.senden(404, {"fehler": "nicht gefunden"})

    def datei(self, pfad, typ, cache=True):
        # Grosse PNG/JPEG (Hintergruende, Sprites) als WebP ausliefern, wenn der Browser es kann (28.10.2026, Tempo)
        if typ in ("image/png", "image/jpeg") and "image/webp" in (self.headers.get("Accept") or ""):
            klein = webp_kopie(pfad)
            if klein:
                pfad, typ = klein, "image/webp"
        roh = open(pfad, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", typ)
        if typ == "image/webp":
            self.send_header("Vary", "Accept")
        # Audio nie cachen (16.10.2026): /api/audio?i=N meint in jeder Szene etwas anderes
        self.send_header("Cache-Control", "max-age=86400" if cache else "no-store")
        self.send_header("Content-Length", str(len(roh)))
        self.end_headers()
        self.wfile.write(roh)

    def musik_datei(self, path):
        size = path.stat().st_size
        start, end = 0, size - 1
        requested = self.headers.get("Range")
        if requested:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested)
            if not match or not any(match.groups()):
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            first, last = match.groups()
            if first:
                start, end = int(first), min(int(last), end) if last else end
            else:
                start = max(0, size - int(last))
            if start >= size or end < start:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
        self.send_response(206 if requested else 200)
        self.send_header("Content-Type", "audio/flac" if path.suffix == ".flac" else "audio/mpeg")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Cache-Control", "private, max-age=86400")
        if requested:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with path.open("rb") as stream:
            stream.seek(start)
            remaining = end - start + 1
            try:
                while remaining:
                    block = stream.read(min(65536, remaining))
                    if not block:
                        break
                    self.wfile.write(block)
                    remaining -= len(block)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def do_POST(self):
        pfad = self.path.split("?")[0]
        if not pfad.startswith("/api/"):
            return self.senden(404, {"fehler": "nicht gefunden"})
        laenge = int(self.headers.get("Content-Length") or 0)
        daten = json.loads(self.rfile.read(laenge) or b"{}")
        if pfad == "/api/stimme_setzen":
            # Einstellungen > Stimmen: Zuordnung je Modul und Figur in eden-config.json ("" = stumm, None = Karte)
            mid = modul_laden()["id"]
            alle = cfg().get("stimmen") or {}
            m = dict(alle.get(mid) or {})
            if daten.get("name") is None:
                m.pop(daten["id"], None)
            else:
                m[daten["id"]] = daten["name"]
            alle[mid] = m
            cfg_setzen(stimmen=alle)
            return self.senden(200, stimmen_ansicht())
        if pfad in ("/api/profil", "/api/ausschnitt"):
            try:
                return self.senden(200, (profil_setzen if pfad == "/api/profil" else ausschnitt_setzen)(daten))
            except Exception as e:
                traceback.print_exc()
                return self.senden(400, {"fehler": str(e)})
        if not LOCK.acquire(timeout=1):
            return self.senden(409, {"fehler": "Die Engine arbeitet noch am letzten Zug."})
        try:
            if not llm.bereit() and pfad[5:] in ("zug", "wahl", "waehlen", "persona", "prolog", "plan_laden", "ende", "swipe", "geben",
                                                 "szene_neu", "handy_antwort", "handy_chips", "vorschlaege", "geste", "zeit",
                                                 "zeit_antwort", "intim", "kabine_ausruhen",
                                                 "kabine_anruf", "ermitteln", "widerspruch", "konfrontieren", "event_schliessen"):
                raise ValueError("Das Spielmodell (KoboldCpp, Port 5010) laeuft nicht - Start-Eden.bat startet es.")
            t0 = time.time()
            vorher = aktiv()
            with wuerfel_anzeige.sammeln(pfad[5:], daten, vorher,
                                       moddir(vorher["modul"] if vorher else None)) as wuerfe:
                z = aktion(pfad[5:], daten)
            print("[Eden] %-10s %.1f s" % (pfad[5:], time.time() - t0), flush=True)
            antwort = ansicht(z, "debug=1" in self.path)
            if wuerfe["rolls"]:
                antwort["wuerfel_anzeige"] = wuerfe
            self.senden(200, antwort)
        except Exception as e:
            traceback.print_exc()
            self.senden(400, {"fehler": str(e)})
        finally:
            LOCK.release()


def main():
    if not os.path.exists(CFG_PFAD):
        json.dump({"modul": "eden_rise", "aktiv": None}, open(CFG_PFAD, "w", encoding="utf-8"), indent=1)
    szene.BEOBACHTER = sichern          # jede neue Antwort sofort speichern -> Client zeigt sie live
    szene.STAENDE = STAENDE             # Schnappschuss vor jedem Zug fuer "Neu formulieren" (zurueck auf die letzte Nachricht)
    szene.CFG.update(cfg())
    zustand.STUFEN_ABSTAND = cfg().get("stufen_abstand", zustand.STUFEN_ABSTAND)   # 0 zum Testen der spaeten Szenen (Duc 31.10.2026)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("[Eden] Engine laeuft: http://127.0.0.1:%d   (Modell: %s)" % (PORT, "bereit" if llm.bereit() else "NICHT erreichbar"))
    if "--no-browser" not in sys.argv:
        webbrowser.open("http://127.0.0.1:%d" % PORT)
    srv.serve_forever()


if __name__ == "__main__":
    main()

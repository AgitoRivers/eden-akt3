# -*- coding: utf-8 -*-
"""Events fuer das Modul eden_rise (17.10.2026) - Bausteine, Kataloge, Pruefung, Bau.

Vier Ereignisarten (Entwurf: Y:\\AI\\mission-control\\entwuerfe\\eden-ereignisarten.html, Regeln: eden-grundlagen.html):
  bordrat  nachts zwischen den Tagen: eine Person stellt das Problem vor, zwei vertreten Positionen (links/rechts),
           unter jeder ihre Kachel; dazu dritter Weg / Versprechen / Bordregel. Wirkt auf Rueckhalt.
  handy    Videoanruf oder Nachricht, auf die Duc reagieren muss.
  gag1     eine Person tut etwas, das andere trifft (Buehne, Betroffene mit +/-/?).
  gagv     zwei Personen gegeneinander, Zuschauer in der Mitte (Versus).
Dazu abend: die Vertrauens-Abende mit Lola und Alva (fuehren in eine Intim-Szene, gespielt vom Modell).
Ducs Staerken (17.10.2026, Persona ESG-Berater: Koepfchen, Kueche, Charme, Handwerk):
  duell    Versus wie gagv, nur steht Duc selbst auf einer Seite (personen.gegner), die Crew schaut zu und stimmt ab.
           personen.staerke = kueche/handwerk/koepfchen/charme; Proben duerfen den Persona-Vorteil tragen (P(..., vorteil)).
  auftritt Duc vor Publikum (Karaoke, Gitarre, Geschichten): personen.publikum, optional personen.partner.

Grundsatz: Kein Event beruehrt die Faelle der Hauptstory. Gags sind nie Spuren. Keine Technik rund um Antrieb,
Steuerung, Kurs, Ladeleitungen oder Partynacht-Zeitleisten.

Texte: titel/lage/Antworten deutsch (Oberflaeche), zeilen englisch (Spielsprache, werden vorab vertont).
Folgen (Liste von dicts, eine Wirkung je dict) - die Engine setzt sie in Phase B um:
  {"vertrauen": [id, punkte]}  {"begehren": [id, punkte]}   Punkte wie in den Grundlagen (+-4 klein, +-6/8 Erlebnis)
  {"wert": name, "delta": n}   moral/ruf/strom/diesel/energie  {"rueckhalt": n}  {"geld": n}  {"item": id}
  {"bordregel": id}  {"versprechen": {...}}  {"gag": id}  {"nachklang": id}  {"klatsch": {...}}  {"moment": {...}}
  {"flag": name}  {"uhr": [name, delta]}  {"kontrollrisiko": n}  {"szene_intim": {...}}
  {"szene_gespraech": {...}}  freies Gespraech, vom Modell gespielt (Duc erzaehlt in eigenen Worten, keine Probe)
  {"partner_waehlen": [ids]}  Duc waehlt eine Person aus der Liste (Duett, Begleitung)
"""
import collections, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))    # werkzeuge\eden_rise -> Eden
ZIEL = os.path.join(EDEN, "module", "eden_rise", "ereignisse.json")

FRAUEN = ["chiara", "sophia", "lea", "rosi", "siri"]
# vogel = Katrin Vogel, Personalberaterin in Koeln (Ducs Geheimnis, nur am Telefon, ohne Bild; Stimme "Lydia")
NEBEN = ["toto", "yasin", "holm", "elsa", "alva", "petru", "casanova", "lola", "megan", "vogel", "maxwell", "jana", "yamamoto",
         "nonna", "isabelle", "frederico",          # Kloster San Martinu: nur in den Frames der Macchia (art "ort")
         "laetitia", "adrien", "wolff", "ghjuvan", "dumenica",   # Ortskapitel Berge (27.10.2026): nur in den Frames
         "gennaro", "matteu", "chloe", "riscossore",        # Strand-Grotte, Akt 2 Woche 2 (27.10.2026): nur in den Frames
         "sirene",                                          # Flut-Nacht in der Grotte (28.10.2026)
         "danzel", "bibi", "charly", "mrwhite",            # Red Trio (30.10.2026): nur in den Frames
         "pascal", "mina", "batu", "sandru", "anghjulu", "minicu",
         "alon",
         "bonaventure"]                                     # Akt 3 (04.11.2026): Buenaventura nach dem Schwur. Cliffhanger Akt 2 (02.11.2026): Keynote auf der Buehne    # Dorf-Figuren (30.10.2026, ereignisse_dorf.py)
# Ortskapitel (26.10.2026): Frames haben art "ort", eigene Hintergruende eden_rise_<bild>.png (oder einen Raum) und werden
# nie gezogen - sie laufen nur als Kette ab dem Ort (auftraege.json). Folgen: weiter, spur_uhr, expedition, chip, kampf.
ORT_BILDER = ["macchia_three_ways", "charcoal_road", "charcoal_hut", "bone_gorge", "antenna_ridge",  # Red Trio (30.10.2026)
              "macchia_path", "macchia_creek_bridge", "shepherd_hut_ruin", "monastery_gate", "monastery_kitchen",
              "forest_edge_cliffs", "ravine_fork", "hidden_rock_niche", "monks_camp_abandoned", "lion_den_cave",
              "lion_den_cave_b", "monastery_garden_dusk", "creek_rest", "ravine_fire",
              "hafen_kai_chaos", "hafen_bar_tuer", "piazza_treppe", "hafen_abend",
              "piazza_treppe_tidy", "mayors_office",          # Casanovas Buero nach dem Hafentag (29.10.2026)
              # Ortskapitel Berge (27.10.2026); die Wunschbilder ersetzen die Platzhalter, sobald sie abgenommen sind
              "chestnut_switchbacks", "genoese_tower_camp", "mountain_lake", "foggy_ridge", "bergerie_interior",
              "bergerie_dusk_exterior", "berge_rotes_licht", "macchia_path_b", "charcoal_clearing", "tower_cliff",
              "high_pasture", "goat_path", "summer_hut_fire", "bear_thicket", "bear_den", "mazzera_hut",
              "ridge_night_lights", "abandoned_mountain_hut", "panther_lair", "rope_bridge_gorge",
              # Strand-Grotte und Kevins Daecher (Akt 2 Woche 2, 27.10.2026); Wunschbilder bei Character Design bestellt
              "strand_lagerfeuer", "grotto_steps", "drowned_beach", "smugglers_tunnel", "crate_hall", "underground_pool",
              "torch_gallery", "gennaro_cell", "flooded_gallery", "air_pocket", "collapsed_passage", "treasure_camp",
              "village_rooftops", "bell_tower_nest", "underground_pool_tide"]
NUR_ORT = {"nonna", "isabelle", "frederico", "laetitia", "adrien", "wolff", "ghjuvan", "dumenica", "gennaro", "matteu",
           "chloe", "riscossore", "mrwhite"}        # die Sirene (Ligeia) hat seit 29.10.2026 ihren Raum siren_pool
OHNE_BILD = {"vogel"}
STAERKEN = ["kueche", "handwerk", "koepfchen", "charme"]
VORTEILE = ["kueche", "handwerk"]        # Persona-Vorteile, die eine Probe tragen kann (handel.persona_vorteil)
PERSONEN = FRAUEN + NEBEN
ATTRIBUTE = ["charm", "empathy", "perception", "cunning", "courage", "strength"]
WERTE = ["moral", "ruf", "energie"]      # Strom/Diesel raus seit 30.10.2026
UHREN = ["reparatur", "rettung", "siri_marke", "yasin_video"]
PHASEN = ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"]
GEFUEHLE = ["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire",
            "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
            "joy", "love", "nervousness", "neutral", "optimism", "pride", "realization", "relief", "remorse",
            "sadness", "surprise"]
RAEUME = ["batu_shop", "av_market", "church", "mochis", "crew_mess", "crew_corridor", "galley", "duc_cabin", "bridge", "main_salon", "aft_deck", "sun_deck",
          "solar_deck", "foredeck", "swim_platform", "tender_garage", "power_room", "generator_room", "workshop",
          "vip_cabin", "village_harbour", "alvas_bar", "petru_workshop", "village_piazza", "hangar_antibes",
          "siren_pool",
          "alon_keynote"]                  # Alons Keynote im Cliffhanger Akt 2 (02.11.2026), nur als Szenenbild                    # Ligeias Teich (29.10.2026): nachts nach der Flut-Nacht
# Hintergruende fuer Anrufe (Ort des Anrufers) - liegen im ST-Hintergrundordner
FERNORTE = {"megan_office": ("eden_hq_megan_office.png", "eden_hq_megan_office_night.png"),
            "eden_lobby": ("eden_hq_lobby.png", "eden_hq_lobby.png"),
            "krankenhaus": ("eden_patient_room.png", "eden_patient_room_night.png"),
            "rathaus": ("eden_rise_mayors_office.png", "eden_rise_mayors_office.png")}
# Handy: "bild" = wo Duc gerade ist (Raum, darf "ort_duc" sein = aktueller Raum), personen.anrufer_ort = Hintergrund im Handy
ORT_DUC = "ort_duc"
ORT_STIMME = "nur_stimme"           # Anruf ohne Video (Anruferin ohne Bild): Handy zeigt nur Name und Wellenform
# Running Gags setzen beim Weiterzaehlen Flags "gag_<id>_<stufe>" (Bedingungen fuer Folge-Events)
# Outfit-Sets je Person (ST-Sets bzw. Prompt-Studio-Kostueme fuer die neuen Figuren); lola_bikini = Aloha, lola_denim = Shore Leave
SETS = {
    "chiara": ["Uniform", "Service", "Swim", "Harbor Night", "Bridge Night", "Cabin Night", "Dress Whites", "Nude"],
    "sophia": ["Concierge", "Shore Leave", "Swim", "Crew Party", "Writing Night", "Book Reading", "Nude"],
    "lea": ["Deck", "Dive", "Off Duty", "Crew Party", "Expedition", "Leopard Bikini", "Nude"],
    "rosi": ["Engine Room", "Off Duty", "Swim", "Crew Party", "Vespa Sunday", "Festa", "Nude"],
    "siri": ["Sea Siren", "Riviera Swim", "Morning Ritual", "Saint-Tropez '69", "Silver Night", "Dad's Sweater", "Nude"],
    "lola": ["Galley", "Off Duty", "lola_bikini", "lola_denim", "Nude"], "megan": ["Boardroom", "Inspection"], "holm": ["Bridge", "holm_bikini", "holm_shirt"],
    "alva": ["alva_standard", "alva_flamenco_noche", "alva_festa", "alva_morgen", "alva_bikini"],   # Ordnernamen aus _name.txt (24.10.)
    "toto": ["Standard"], "yasin": ["Standard"], "elsa": ["Standard", "elsa_combat"], "petru": ["Standard"],
    "casanova": ["Standard", "alva_flamenco_rojo"],      # zweites Set = ihr Flamenco-Kleid (Name aus dem ST-Ordner)
    "vogel": [],
    "maxwell": ["maximum_steward_a", "maximum_training_b", "maximum_party_b", "maximum_steelmop"],   # ST-Ordner "Maxwell Ndlovu" (24.10.)
    "jana": ["jana_deck_a", "jana_bikini_a", "pencil_shortsleeves_red", "jana_kitty_b", "eisc_bib_lounge_pink"],
    "yamamoto": ["yamamoto_hawaii_b", "yamamoto_badeanzug_b", "yamamoto_party_b", "yamamoto_leder_a"],
    "nonna": ["nonna_standard"], "isabelle": ["isabelle_standard"], "frederico": ["frederico_standard"],
    "laetitia": ["laetitia_standard"], "adrien": ["adrien_standard"], "wolff": ["wolff_standard"],
    "ghjuvan": ["ghjuvan_standard"], "dumenica": ["dumenica_standard"],
    "gennaro": ["gennaro_standard"], "matteu": ["matteu_standard"], "chloe": ["chloe_standard"],
    "riscossore": ["riscossore_standard"], "bonaventure": ["bonaventure_standard"], "sirene": ["sirene_standard"],
    "danzel": ["danzel_B"], "bibi": ["bibi_A", "Mochis"], "charly": ["charly_A"], "mrwhite": ["mrwhite_A"],
    "minicu": ["minicu_standard"], "alon": ["alon_standard"], "pascal": ["pascal_standard"], "mina": ["mina_standard"], "batu": ["batu_standard"],
    "sandru": ["sandru_av", "sandru_frei"], "anghjulu": ["anghjulu_standard"],
}
TOENE = ["witzig", "wholesome", "frech", "ernst"]
TON_ZIEL = {"witzig": .35, "wholesome": .25, "frech": .20, "ernst": .15}
# Woerter, die ein Event in die Naehe der Faelle bringen wuerden (Pruefung, nicht abschliessend)
VERBOTEN = ["inverter", "wechselrichter", "breaker", "sicherung", "autopilot", "course", "kurs ", "detour", "logbook",
            "logbuch", "protokoll", "timeline", "02:10", "margot", "publisher", "verlag", "exam", "pruefung", "prüfung",
            "yachtmaster", "recall", "report", "bericht", "serial", "serien", "blackout", "drive", "antrieb",
            "load limit", "adapter", "charger", "ladekabel", "service lock", "who did", "schuld", "culprit", "alibi",
            "group photo", "gruppenfoto", "party night", "partynacht"]

# ------------------------------------------------------------------ Kataloge
BORDREGELN = {
    "kein_gras_an_bord": {"label": "No weed on board", "taeglich": [{"vertrauen": ["lola", -2]}],
                          "wirkt": "Lola a little annoyed every evening; no inspection risk with Elsa over the weed"},
    "gras_nur_nach_dienst": {"label": "Weed only off duty, never on deck", "taeglich": [],
                             "wirkt": "Lola's evening event stays possible; Holm/Chiara events with weed on deck "
                                      "drop out"},
    "drei_minuten_dusche": {"label": "Three-minute showers", "taeglich": [{"vertrauen": ["rosi", 2]}],
                            "wirkt": "Rosi +2 trust every evening: her batteries can breathe"},   # vorher Strom +1 (bis 30.10.2026)
    "essen_geteilt": {"label": "Food is shared, not hoarded", "taeglich": [{"wert": "moral", "delta": 1}],
                      "wirkt": "Crew Mood +1 every evening, two fewer goods in Totò's locker"},
    "kamera_aus_22": {"label": "Cameras off after 10 pm", "taeglich": [{"vertrauen": ["siri", 2]}],
                      "wirkt": "Siri +2 trust in the evening; Yasin's content missions only during the day"},
    "kombuese_ordnung": {"label": "Galley order", "taeglich": [{"vertrauen": ["chiara", 2]}],
                         "wirkt": "Chiara +2; Lola's galley gags happen less often"},
    "gaestebereich": {"label": "The guest area stays the guest area", "taeglich": [{"geld": -50}],
                      "wirkt": "−50 € every evening, Megan's pressure events are milder"},
    "kein_alkohol_deck": {"label": "No alcohol on deck", "taeglich": [{"rueckhalt": 1}],
                          "wirkt": "Backing +1 every evening; Alva's bar deliveries to the boat drop out"},
    "nachtruhe": {"label": "Lights out at midnight", "taeglich": [{"wert": "energie", "delta": 1}],
                  "wirkt": "Energy +1 in the morning; fewer phone events at night"},
}
GAGS = {
    "kevin": {"label": "Kevin the seagull", "stufen": 4},
    "rosi_vs_unit01": {"label": "Rosi versus Unit-01", "stufen": 4},
    "ocean_glitter": {"label": "Ocean Glitter", "stufen": 3},
    "chiara_klopft": {"label": "Chiara always knocks now", "stufen": 3},
    "kalte_dusche": {"label": "The cold shower", "stufen": 3},
    "casanova_kapelle": {"label": "Casanova's brass band", "stufen": 3},
    "toto_cousin": {"label": "Totò's cousin from Bastia", "stufen": 3},
    "megan_lacht": {"label": "Megan laughs (and hates it)", "stufen": 3},
    "yamamoto_kamera": {"label": "Yamamoto's bird photography", "stufen": 7},
    "maxwell_training": {"label": "Jana's training with Maxwell", "stufen": 3},
}
GAG_NAMEN = set(GAGS)

# Neue Gegenstaende, die Events als Belohnung vergeben (Details in der Gegenstandsliste)
NEUE_ITEMS = {}


def item(iid, label, art, **kw):
    NEUE_ITEMS[iid] = dict(label=label, art=art, **kw)
    return {"item": iid}


# ------------------------------------------------------------------ Bausteine
def Z(wer, text, gefuehl="neutral"):
    return {"wer": wer, "text": text, "gefuehl": gefuehl}


def P(attr, sg, vorteil=None):
    p = {"attribut": attr, "sg": sg}
    if vorteil:
        p["vorteil"] = vorteil              # Persona-Vorteil ("kueche"/"handwerk"): zwei Wuerfel, der bessere zaehlt
    return p


def O(text, folgen=None, probe=None, erfolg=None, fehlschlag=None, von=None, zeile=None, art=None):
    o = {"text": text, "folgen": folgen or []}
    if probe:
        o.update(probe=probe, bei_erfolg=erfolg or [], bei_fehlschlag=fehlschlag or [])
    if von:
        o["von"] = von
    if zeile:
        o["zeile"] = zeile
    if art:
        o["art"] = art                      # "dritter_weg", "versprechen", "bordregel", "auflegen"
    return o


V = lambda pid, n: {"vertrauen": [pid, n]}
B = lambda pid, n: {"begehren": [pid, n]}
W = lambda wert, d: {"wert": wert, "delta": d}
R = lambda n: {"rueckhalt": n}
G = lambda n: {"geld": n}
I = lambda iid: {"item": iid}
REG = lambda rid: {"bordregel": rid}
GAG = lambda gid: {"gag": gid}
NK = lambda pid: {"nachklang": pid}
EN = lambda d=-1: {"wert": "energie", "delta": d}
F = lambda name: {"flag": name}
U = lambda uhr, d: {"uhr": [uhr, d]}
KR = lambda n: {"kontrollrisiko": n}


def VER(an, text, frist_tage, gehalten_wenn):
    return {"versprechen": {"an": an, "text": text, "frist_tage": frist_tage, "gehalten_wenn": gehalten_wenn}}


def KL(ueber, erzaehlt_von, was):
    return {"klatsch": {"ueber": ueber, "von": erzaehlt_von, "was": was}}


def MO(moment, wer, zeugen=()):
    return {"moment": {"art": moment, "wer": list(wer), "zeugen": list(zeugen)}}


def GESPRAECH(wer, ort, hinweis, max_zuege=6):
    """Freies Gespraech, vom Modell gespielt: wer = Person-ID oder "crew"."""
    return {"szene_gespraech": {"wer": wer, "ort": ort, "hinweis": hinweis, "max_zuege": max_zuege}}


def PARTNER(*ids):
    return {"partner_waehlen": list(ids)}


def INTIM(pid, ort, set_, fuehrung, hinweis):
    return {"szene_intim": {"pid": pid, "ort": ort, "set": set_, "fuehrung": fuehrung, "hinweis": hinweis}}


AKT3_AB = 24                                # Akt 3 beginnt am Tag nach der Belagerung (E-114: Tag 21-23), Ende Tag 35 (fix-akt2)
AKT3 = [AKT3_AB, 35]                        # zweites Fenster (wann.akt2) fuer Szenen, die auch in Akt 3 kommen duerfen


def WANN(tage=(1, 7), phasen=None, orte=None, anwesend=None, bed=None, an_land=None, wetter=None, pflicht=False,
         prolog=False, holt_leute=False):
    w = {"tage": list(tage)}
    if holt_leute:
        w["holt_leute"] = True              # Pflichtszene stellt ihre Figuren selbst, egal wo sie laut Tagesablauf sind
    if prolog:
        w["prolog"] = True                  # Tag 0 (Hangar Antibes): Tag 1, auch ohne Szene, Begegnungen direkt hintereinander
    if pflicht:
        w["pflicht"] = True                 # kommt garantiert zu Beginn der Phase (Megans Sprachnachrichten, 24.10.)
    if phasen:
        w["phasen"] = phasen
    if orte:
        w["orte"] = orte
    if anwesend:
        w["anwesend"] = anwesend
    if bed:
        w["bedingung"] = bed
    if an_land is not None:
        w["an_land"] = an_land
    if wetter:
        w["wetter"] = wetter
    return w


def E(id, art, ton, titel, wann, bild, personen, lage, zeilen, optionen, sets=None, gag=None, knistern=False,
      nachklang_text=None):
    e = {"id": id, "art": art, "ton": ton, "titel": titel, "wann": wann, "bild": bild, "personen": personen,
         "sets": sets or {}, "lage": lage, "zeilen": zeilen, "optionen": optionen}
    if gag:
        e["gag"] = gag
    if knistern:
        e["knistern"] = True
    if nachklang_text:
        e["nachklang_text"] = nachklang_text
    return e


# ------------------------------------------------------------------ Pruefung
def beteiligte(e):
    p = e["personen"]
    ids = []
    for k in ("sprecher", "links", "rechts", "handelnd", "anrufer", "bei_dir", "pid", "gegner", "partner"):
        if p.get(k):
            ids.append(p[k])
    ids += [b["id"] for b in p.get("betroffen", [])] + list(p.get("zuschauer", [])) + list(p.get("publikum", []))
    return ids


def p_fern(e):
    """Handelnde Person ist nicht an Bord (z. B. Megan per Drohne/Lautsprecher)."""
    return bool(e["personen"].get("fern"))


def folgen_alle(e):
    for o in e["optionen"]:
        for f in o["folgen"] + o.get("bei_erfolg", []) + o.get("bei_fehlschlag", []):
            yield o, f


def pruefe_ort(e, ids):
    """Frames eines Ortskapitels: Bild, Optionen (1-4), Sprecher, Ziele der Kette."""
    k, f = e["id"], []
    if e["bild"] not in ORT_BILDER and e["bild"] not in RAEUME:
        f.append("%s: Ort-Bild %s" % (k, e["bild"]))
    if not 1 <= len(e["optionen"]) <= 4:
        f.append("%s: %d Optionen" % (k, len(e["optionen"])))
    for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]:
        if z["wer"] not in PERSONEN or z["gefuehl"] not in GEFUEHLE or '"' in z["text"]:
            f.append("%s: Zeile %s/%s" % (k, z["wer"], z["gefuehl"]))
    for pid, s in e["sets"].items():
        if s not in SETS.get(pid, []):
            f.append("%s: set %s/%s" % (k, pid, s))
    for o, fo in folgen_alle(e):
        if "weiter" in fo:
            ziele = [fo["weiter"]] if isinstance(fo["weiter"], str) else [x["id"] for x in fo["weiter"]]
            f += ["%s: weiter zu unbekanntem Frame %s" % (k, x) for x in ziele if x not in ids]
        if "item" in fo and fo["item"] not in NEUE_ITEMS and fo["item"] not in ALTE_ITEMS:
            f.append("%s: item %s unbekannt" % (k, fo["item"]))
    return f


def pruefe(events):
    fehler, warn = [], []
    ids = collections.Counter(e["id"] for e in events)
    fehler += ["doppelte id %s" % i for i, n in ids.items() if n > 1]
    for e in events:
        k = e["id"]
        if e["art"] not in ("bordrat", "handy", "gag1", "gagv", "abend", "duell", "auftritt", "ort"):
            fehler.append("%s: art %s" % (k, e["art"]))
        ort = e["art"] == "ort"
        handy_selfie = e["art"] == "handy" and (e["personen"].get("selfie") or e["personen"].get("nachschlag")
                                            or e["personen"].get("charm")    # Charm-Uebergabe (28.10.2026)
                                            or e["personen"].get("favour"))  # Favours (29.10.2026)
        if any(pid in NUR_ORT for pid in beteiligte(e) + [z["wer"] for z in e["zeilen"]]) and not ort and not handy_selfie and not k.startswith(("hb_", "g1_zg_", "bl_", "a3_")):   # hb_: Holms Wette, Gaeste an Bord; g1_zg_: Nonna kommt in Ba Tus Laden; bl_: Wolff bei der Belagerung
            fehler.append("%s: Kloster-Figuren nur in Ort-Frames" % k)
        if ort:
            fehler += pruefe_ort(e, ids)
            continue
        if e["ton"] not in TOENE:
            fehler.append("%s: ton %s" % (k, e["ton"]))
        w = e["wann"]
        # Kalender (E-114): Akt 1 = Tag 1-7, Akt 2 = Tag 8-23 (Belagerung 21-23), Akt 3 = Tag AKT3_AB-35. Tag 7 ist die Anhoerung
        # (keine Zufalls-Events), die Festa-Events liegen am Ende von Akt 3.
        if not (1 <= w["tage"][0] <= w["tage"][1] <= (23 if k.startswith("bl_") else 35)) or w["tage"][0] <= 7 < w["tage"][1]:   # bl_: Die Belagerung geht bis Tag 23 (E-114)
            fehler.append("%s: tage %s (Akt 1 = Tag 1-7, Fenster nie über eine Aktgrenze)" % (k, w["tage"]))
        if w["tage"][1] == 7 and not w.get("pflicht"):
            fehler.append("%s: Tag 7 ist die Anhörung - keine Zufalls-Events" % k)
        # Pflicht mit Datums-Flag (Ligeia 30.10.2026): Fenster ueber mehrere Tage, ausgeloest erst durch flag_seit;
        # Erinnerungen (02.11.2026) ebenso, je Tag hoechstens eine (kern/ereignisse.py)
        if w.get("pflicht") and ((w["tage"][0] != w["tage"][1] and not w.get("leiter") and not w.get("erinnerung") and "flag_seit" not in json.dumps(w.get("bedingung") or w.get("bed") or {}))
                                 or len(w.get("phasen", [])) != 1):
            fehler.append("%s: Pflicht-Events brauchen genau einen Tag und eine Phase" % k)
        for ph in w.get("phasen", []):
            if ph not in PHASEN:
                fehler.append("%s: phase %s" % (k, ph))
        for o in w.get("orte", []):
            if o not in RAEUME:
                fehler.append("%s: ort %s" % (k, o))
        if e["bild"] not in RAEUME and e["bild"] not in FERNORTE and not (e["art"] == "handy" and e["bild"] == ORT_DUC):
            fehler.append("%s: bild %s" % (k, e["bild"]))
        ao = e["personen"].get("anrufer_ort")
        if e["art"] == "handy" and ao not in RAEUME and ao not in FERNORTE and ao != ORT_STIMME:
            fehler.append("%s: anrufer_ort %s" % (k, ao))
        if e["art"] == "handy" and (e["personen"].get("anrufer") in OHNE_BILD) != (ao == ORT_STIMME):
            fehler.append("%s: Anruferin ohne Bild nur mit anrufer_ort %s (und umgekehrt)" % (k, ORT_STIMME))
        if e["art"] != "handy" and any(pid in OHNE_BILD for pid in beteiligte(e)):
            fehler.append("%s: Person ohne Bild nur am Telefon" % k)
        for pid in beteiligte(e) + list(w.get("anwesend", [])):
            if pid not in PERSONEN:
                fehler.append("%s: person %s" % (k, pid))
        # Tageszaehlung seit 18.10.2026 (story.json auf phase-b): Tag 1 = Party, nur abend+nacht, beide exklusiv ->
        # Events fruehestens ab Tag 2. Holm ist persoenlich nur am Fruehstueck von Tag 2 vor ihrem Abschied da.
        if w["tage"][0] < 2 and not w.get("prolog"):
            fehler.append("%s: Tag 1 ist die Party (exklusiv) - Events erst ab Tag 2" % k)
        if "holm" in beteiligte(e) and e["art"] != "handy" and not w.get("prolog") and not k.startswith(("hb_", "bl_", "a3_")) and not (   # hb_, bl_, a3_: Holm ist zurueck (Woche 3, Akt 3)
                w["tage"] == [2, 2] and w.get("phasen") == ["fruehstueck"] and "holm_evakuiert" in json.dumps(w.get("bedingung", {}))):
            fehler.append("%s: Holm an Bord nur Tag 2 Fruehstueck mit Bedingung nicht holm_evakuiert" % k)
        if "megan" in beteiligte(e) and e["art"] != "handy" and e["bild"] not in FERNORTE and not p_fern(e) and not k.startswith(("bl_", "a3_")) and \
                not w.get("prolog") and \
                "megan_besuch" not in json.dumps(w.get("bedingung", {})):
            fehler.append("%s: Megan an Bord nur mit Bedingung megan_besuch" % k)
        for pid, s in e["sets"].items():
            if s not in SETS.get(pid, []):
                fehler.append("%s: set %s/%s" % (k, pid, s))
        p = e["personen"]
        if e["art"] == "bordrat" and not all(p.get(x) for x in ("sprecher", "links", "rechts")):
            fehler.append("%s: bordrat braucht sprecher/links/rechts" % k)
        if e["art"] == "gag1" and (not p.get("handelnd") or not p.get("betroffen")) and not k.startswith(("hb_", "bl_", "a3_")) and not e.get("solo"):
            fehler.append("%s: gag1 braucht handelnd + betroffen" % k)
        if e["art"] == "gagv" and not (p.get("links") and p.get("rechts")):
            fehler.append("%s: gagv braucht links/rechts" % k)
        if e["art"] == "handy" and not p.get("anrufer"):
            fehler.append("%s: handy braucht anrufer" % k)
        if e["art"] == "duell" and (not p.get("gegner") or p.get("staerke") not in STAERKEN):
            fehler.append("%s: duell braucht gegner + staerke (%s)" % (k, "/".join(STAERKEN)))
        if e["art"] == "auftritt" and (not (p.get("publikum") or p.get("partner")) or p.get("staerke") not in STAERKEN + ["herz"]):
            fehler.append("%s: auftritt braucht publikum/partner + staerke" % k)
        if not 2 <= len(e["optionen"]) <= 4 and e["art"] != "abend" and not k.startswith(("hb_", "bl_")):
            fehler.append("%s: %d Optionen" % (k, len(e["optionen"])))
        if not e["zeilen"]:
            fehler.append("%s: keine Zeilen" % k)
        for z in e["zeilen"] + [o["zeile"] for o in e["optionen"] if o.get("zeile")]:
            if z["wer"] not in PERSONEN:
                fehler.append("%s: zeile von %s" % (k, z["wer"]))
            if z["gefuehl"] not in GEFUEHLE:
                fehler.append("%s: gefuehl %s" % (k, z["gefuehl"]))
            if '"' in z["text"]:
                fehler.append("%s: doppeltes Anfuehrungszeichen in Zeile" % k)
        for o in e["optionen"]:
            if o.get("probe") and o["probe"]["attribut"] not in ATTRIBUTE:
                fehler.append("%s: attribut %s" % (k, o["probe"]["attribut"]))
            if o.get("probe") and o["probe"].get("vorteil") not in [None] + VORTEILE:
                fehler.append("%s: vorteil %s" % (k, o["probe"]["vorteil"]))
            if o.get("probe", {}).get("vorteil") and o["probe"]["sg"] < 12:
                warn.append("%s: Probe mit Vorteil unter SG 12 ist fast sicher" % k)
        for o, f in folgen_alle(e):
            typ = next(iter(f))
            val = f[typ]
            if len(f) > 1 and typ != "wert":
                fehler.append("%s: Folge mit mehreren Wirkungen %s" % (k, f))
            if typ in ("vertrauen", "begehren"):
                if val[0] not in PERSONEN:
                    fehler.append("%s: %s fuer %s" % (k, typ, val[0]))
                if typ == "begehren" and val[0] not in FRAUEN + ["lola", "alva", "bibi"]:
                    fehler.append("%s: Begehren nur fuer Frauen/Lola/Alva (%s)" % (k, val[0]))
                if abs(val[1]) > 16:
                    fehler.append("%s: %s %d zu gross" % (k, typ, val[1]))
            elif typ == "wert" and f["wert"] not in WERTE:
                fehler.append("%s: wert %s" % (k, f["wert"]))
            elif typ == "bordregel" and val not in BORDREGELN:
                fehler.append("%s: bordregel %s" % (k, val))
            elif typ == "gag" and val not in GAG_NAMEN:
                fehler.append("%s: gag %s" % (k, val))
            elif typ == "uhr" and val[0] not in UHREN:
                fehler.append("%s: uhr %s" % (k, val[0]))
            elif typ == "item" and val not in NEUE_ITEMS and val not in ALTE_ITEMS:
                fehler.append("%s: item %s unbekannt" % (k, val))
            elif typ == "partner_waehlen" and any(p_ not in PERSONEN for p_ in val):
                fehler.append("%s: partner %s" % (k, val))
            elif typ == "szene_gespraech" and val["wer"] not in PERSONEN + ["crew", "wahl"]:   # wahl = aus partner_waehlen
                fehler.append("%s: gespraech mit %s" % (k, val["wer"]))
        if e.get("gag") and e["gag"] not in GAG_NAMEN:
            fehler.append("%s: gag %s" % (k, e["gag"]))
        roh = json.dumps(e, ensure_ascii=False).lower().replace("of course", "")
        for wort in VERBOTEN:
            if re.search(r"(?<![a-zäöüß])" + re.escape(wort), roh):
                warn.append("%s: Wort '%s' (Fallnaehe pruefen)" % (k, wort))
    return fehler, warn


ALTE_ITEMS = set()


def alte_items():
    try:                                    # Grundgeruest-Gegenstaende (bis 18.10.2026 aus dem Modul Gestrandet gelesen)
        m = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
        ALTE_ITEMS.update(k for k, v in m["items"].items() if v.get("art") != "beweis")
    except Exception:
        pass
    try:                                    # Gegenstandspool von eden_rise (gegenstaende_eden_rise.py)
        g = json.load(open(os.path.join(EDEN, "module", "eden_rise", "gegenstaende.json"), encoding="utf-8"))
        ALTE_ITEMS.update(i["id"] for i in g["items"])
    except Exception:
        pass


def statistik(events):
    c = collections.Counter
    print("je Art:", dict(c(e["art"] for e in events)))
    t = c(e["ton"] for e in events if e["art"] not in ("abend", "ort"))
    n = sum(t.values())
    print("Ton:", {k: "%d (%d %%, Ziel %d %%)" % (t[k], round(100 * t[k] / n), round(100 * TON_ZIEL[k])) for k in TOENE})
    print("Knistern:", sum(1 for e in events if e.get("knistern")))
    vor = c()
    for e in events:
        for pid in set(beteiligte(e)):
            vor[pid] += 1
    print("Auftritte:", dict(sorted(vor.items(), key=lambda x: -x[1])))
    print("fehlend:", [p for p in PERSONEN if not vor[p]])
    mit_item = sum(1 for e in events if any("item" in f for _, f in folgen_alle(e)))
    print("Events mit Gegenstand: %d von %d" % (mit_item, len(events)))
    sets = c()
    for e in events:
        for pid, s in e["sets"].items():
            sets["%s/%s" % (pid, s)] += 1
    print("genutzte Outfits: %d von %d" % (len(sets), sum(len(v) for v in SETS.values())))
    print("ungenutzt:", sorted("%s/%s" % (p, s) for p, v in SETS.items() for s in v if "%s/%s" % (p, s) not in sets))
    zeilen = sum(len(e["zeilen"]) + sum(1 for o in e["optionen"] if o.get("zeile")) for e in events)
    print("vertonte Zeilen:", zeilen)


def bauen():
    sys.path.insert(0, HIER)
    alte_items()
    import ereignisse_bordrat, ereignisse_handy, ereignisse_gag1, ereignisse_gagv, ereignisse_abende, ereignisse_staerken
    import ereignisse_verrueckt, ereignisse_akt1, ereignisse_tag0, ereignisse_yamamoto, ereignisse_hafen, ereignisse_herkunft
    import ereignisse_wiki, ereignisse_flirt, ereignisse_kloster, ereignisse_selfies, ereignisse_funken, ereignisse_berge
    import ereignisse_akt2, ereignisse_grotte, ereignisse_charms, ereignisse_favours, ereignisse_ligeia
    import ereignisse_bibi, ereignisse_cliffhanger
    import ereignisse_legenden, ereignisse_red_trio, ereignisse_holm, ereignisse_dorf, ereignisse_schneider, ereignisse_romanzen, ereignisse_outfit_quest, ereignisse_belagerung, ereignisse_belagerung_nacht, ereignisse_mochis
    import ereignisse_erinnerung                  # Erinnerungen der Auftraggeberinnen (02.11.2026)
    import ereignisse_akt3_woche4                 # Akt 3, Woche 4 (04.11.2026, Drehbuch akt3)
    import ereignisse_akt3_lose                   # Akt 3, Zeugen und Festa-Lose (Paket C)
    events = (ereignisse_bordrat.EVENTS + ereignisse_handy.EVENTS + ereignisse_gag1.EVENTS + ereignisse_gagv.EVENTS
              + ereignisse_abende.EVENTS + ereignisse_staerken.EVENTS + ereignisse_verrueckt.EVENTS
              + ereignisse_akt1.EVENTS + ereignisse_yamamoto.EVENTS + ereignisse_tag0.EVENTS + ereignisse_hafen.EVENTS
              + ereignisse_herkunft.EVENTS + ereignisse_wiki.EVENTS
              + ereignisse_flirt.EVENTS + ereignisse_kloster.EVENTS + ereignisse_selfies.EVENTS
              + ereignisse_funken.EVENTS + ereignisse_berge.EVENTS
              + ereignisse_akt2.EVENTS + ereignisse_grotte.EVENTS + ereignisse_charms.EVENTS
              + ereignisse_favours.EVENTS + ereignisse_ligeia.EVENTS + ereignisse_legenden.EVENTS + ereignisse_red_trio.EVENTS + ereignisse_holm.EVENTS
              + ereignisse_dorf.EVENTS + ereignisse_schneider.EVENTS + ereignisse_romanzen.EVENTS + ereignisse_bibi.EVENTS + ereignisse_cliffhanger.EVENTS + ereignisse_outfit_quest.EVENTS + ereignisse_belagerung.EVENTS + ereignisse_belagerung_nacht.EVENTS + ereignisse_mochis.EVENTS
              + ereignisse_erinnerung.EVENTS + ereignisse_akt3_woche4.EVENTS + ereignisse_akt3_lose.EVENTS)
    # Die Event-Dateien importieren dieses Modul unter seinem Namen - ihre Gegenstaende landen dort, nicht in __main__
    NEUE_ITEMS.update(sys.modules["ereignisse_basis"].NEUE_ITEMS)
    import ereignisse_fenster                    # Akt 2 (29.10.2026): zeitlose Events bis Tag 21 offen, "nachlauf"
    fenster_fehlt = ereignisse_fenster.anwenden(events)
    ereignisse_romanzen.zusatz(events)           # alte Flirts reagieren auf die erste Nacht (Duc 31.10.2026)
    # Festa und Ehrenbuerger gehoeren ans Ende von Akt 3 (E-100). An Tag 21 ist die Belagerung, darum warten sie auf ein Flag.
    for e in events:
        if e["id"] in ("br_ehrenbuerger", "ab_casanova_flamenco", "gv_rotes_kleid"):
            alt = e["wann"].get("bedingung")
            e["wann"]["bedingung"] = {"alle": [{"flag": "akt3_festa"}] + ([alt] if alt else [])}
    fehler, warn = pruefe(events)
    fehler += ["Fenster: unbekanntes Event %s" % i for i in fenster_fehlt]
    statistik(events)
    for w in warn:
        print("WARNUNG", w)
    if fehler:
        for f in fehler:
            print("FEHLER", f)
        sys.exit(1)
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\ereignisse_*.py - dort aendern, dann ereignisse_basis.py laufen lassen.",
               "bordregeln": BORDREGELN, "gags": GAGS, "neue_items": NEUE_ITEMS, "events": events},
              open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", ZIEL, "-", len(events), "Events")
    print("Favours: %d gesprochene Zeilen -> stimme_tags.json" % ereignisse_favours.tags_schreiben())
    print("Schneider: %d gesprochene Zeilen -> stimme_tags.json" % ereignisse_schneider.tags_schreiben())
    print("Akt 3 Woche 4: %d gesprochene Zeilen -> stimme_tags.json" % sys.modules["ereignisse_akt3_woche4"].tags_schreiben())
    print("Akt 3 Lose: %d gesprochene Zeilen -> stimme_tags.json" % sys.modules["ereignisse_akt3_lose"].tags_schreiben())
    print("Outfit-Quest: %d gesprochene Zeilen -> stimme_tags.json" % ereignisse_outfit_quest.tags_schreiben())
    print("Legenden: %d Zeilen -> legenden.json, %d gesprochene -> stimme_tags.json" % ereignisse_legenden.schreiben(os.path.dirname(ZIEL)))
    print("Dorf: %d gesprochene Zeilen -> stimme_tags.json" % ereignisse_dorf.tags_schreiben())
    print("Erinnerungen: %d gesprochene Zeilen -> stimme_tags.json" % ereignisse_erinnerung.tags_schreiben())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    bauen()

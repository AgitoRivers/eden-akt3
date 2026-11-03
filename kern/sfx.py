"""Sound-Effekte (18.10.2026): Katalog der gewaehlten Varianten und Story-Ausloeser. Verbraucht keinen Spielzufall.

Quelle: module/<modul>/sfx.json (Builder werkzeuge/eden_rise/sfx_eden_rise.py), Dateien in module/<modul>/sfx/.
Je Effekt spielt die von Duc gewaehlte Variante (`wahl`); ist noch keine gewaehlt, wechselt der Client zwischen allen.
Oberflaeche, Wuerfel, Geld, Vertrauen usw. erkennt der Client selbst (client/plugins/eden-sfx); der Server meldet nur,
was er allein weiss: welche Szene, welches Event oder welcher Kampf gerade laeuft (`hint`).
"""
import json
import re
from functools import lru_cache
from pathlib import Path

DATEI = re.compile(r"[a-z0-9_]+_[1-9][0-9]?\.mp3")


@lru_cache(maxsize=8)
def _laden(pfad, stand):
    return json.loads(Path(pfad).read_text(encoding="utf-8"))


def daten(base, module):
    pfad = Path(base) / "module" / module / "sfx.json"
    if not pfad.is_file():
        return {"sfx": [], "ausloeser": {}}
    return _laden(str(pfad), pfad.stat().st_mtime_ns)


def _ordner(base, module):
    return (Path(base) / "module" / module / "sfx").resolve()


def katalog(base, module):
    """{effekt: [url, ...]} - nur Dateien, die es gibt; mit Wahl die gewaehlte(n), der Client wechselt zufaellig."""
    ordner, out = _ordner(base, module), {}
    for s in daten(base, module)["sfx"]:
        w = s.get("wahl")                       # Zahl, Liste (Abwechslung) oder None (noch offen: alle)
        nummern = w if isinstance(w, list) else [w] if w else range(1, s["varianten"] + 1)
        urls = ["/sfx/%s_%d.mp3" % (s["id"], n) for n in nummern if (ordner / ("%s_%d.mp3" % (s["id"], n))).is_file()]
        if urls:
            out[s["id"]] = urls
    return out


def audio_path(base, module, name):
    if not DATEI.fullmatch(name):
        return None
    ordner = _ordner(base, module)
    pfad = (ordner / name).resolve()
    if pfad.parent != ordner or not pfad.is_file():
        return None
    return pfad


def hint(base, module, state):
    """Effekt fuer die laufende Szene / das Event / den Kampf: {key, id, nach} oder None.
    key ist je Auftritt eindeutig; die Kampf-Instanz erlaubt erneutes Spielen nach einer Niederlage."""
    if not state:
        return None
    status = state.get("status")
    if status == "szene":
        sid = ((state.get("szene") or {}).get("def") or {}).get("id", "")
        feld = "szenen"
        key = "|".join(str(state.get(k, "")) for k in ("id", "tag", "phase")) + "|s|" + sid
    elif status == "ereignis":
        sid = (state.get("event") or {}).get("id", "")
        feld = "ereignisse"
        key = "|".join(str(state.get(k, "")) for k in ("id", "tag", "phase")) + "|e|" + sid
    elif status == "kampf":
        kampf = state.get("kampf") or {}
        sid = kampf.get("definition", "")
        feld = "kaempfe"
        key = "|".join(str(state.get(k, "")) for k in ("id", "tag", "phase")) + "|k|" + sid + "|" + str(kampf.get("id", ""))
    else:
        return None
    if not sid:
        return None
    ausloeser = daten(base, module).get("ausloeser", {})
    effekt = None
    if feld == "kaempfe":                            # Gegnertyp zuerst (29.10.2026): trifft auch den seltenen Gegner
        typ = (((state.get("kampf") or {}).get("gegner") or [{}])[0] or {}).get("typ")
        effekt = next((e for e, a in ausloeser.items() if typ and typ in a.get("gegner", [])), None)
    effekt = effekt or next((e for e, a in ausloeser.items() if sid in a.get(feld, [])), None)
    nach = next((e for e, a in ausloeser.items() if sid in a.get("nach_szene", [])), None) if feld == "szenen" else None
    if not effekt and not nach:
        return None
    return {"key": key, "id": effekt, "nach": nach}


# ------------------------------------------------------------------ Ambience (Duc 27.10.2026, Pixabay-Auswahl)
# Eine leise Hintergrund-Schleife je Lage; der Client blendet zwischen ihnen ueber. Effekte mit schleife=True im Katalog.
AMB_DECK = ("aft_deck", "sun_deck", "solar_deck", "foredeck", "swim_platform", "bridge")
AMB_HAFEN = ("village_harbour", "village_piazza", "calvi_harbour", "alvas_terrace", "hangar_antibes")
AMB_ORT = {"macchia": "amb_macchia", "rathaus": "amb_hafen", "hafen": "amb_hafen", "bootsschuppen": "amb_hafen",
           "berge": "amb_macchia", "hochweide": "amb_macchia", "seehuette": "amb_macchia",   # Berge (27.10.2026)
           "grotte": "amb_grotte", "grotte_flut": "amb_grotte_flut"}                       # Grotte (29.10.2026)
AMB_BILD = {"village_rooftops": "amb_daecher", "bell_tower_nest": "amb_daecher"}   # Kevins Daecher: Frames ohne Ort
HOEHLE = ("amb_grotte", "amb_grotte_flut")          # nach einem Sieg bleibt die Hoehle - keine Voegel unter Tage


def ambience(base, module, state, modul=None):
    """-> Effekt-ID der Schleife fuer die aktuelle Lage oder None (Stille)."""
    if not state:
        return None
    status, phase = state.get("status"), state.get("phase")
    nacht = phase in ("abend", "nacht")
    wahl = None
    if status == "kampf":
        return None
    if status == "ereignis":
        from . import ereignisse
        ev = (ereignisse.daten(str(Path(base) / "module" / module)) or {}).get("_index", {}).get(
            (state.get("event") or {}).get("id"), {})
        if ev.get("art") == "ort" and state.get("ort_aktiv"):
            if ev.get("rast"):
                wahl = "rast_feuer"
            elif state.get("ort_frame") in (state.get("ort_besiegt") or []) and \
                    AMB_ORT.get(state["ort_aktiv"]) not in HOEHLE:
                wahl = "ruhig_voegel"
            else:
                wahl = AMB_ORT.get(state["ort_aktiv"])
        else:
            ort = ev.get("bild")
            eid = ev.get("id", "")
            if eid.startswith(("bl_morgen", "bl_flicken")):   # Belagerung: der Morgen danach riecht nach Rauch (Duc 01.11.2026)
                return "feuer_loop" if katalog(base, module).get("feuer_loop") else None
            if eid.startswith("bl_") and ort == "generator_room":   # Rosi: Unit-01 summt hinter der Tuer
                return "amb_maschine" if katalog(base, module).get("amb_maschine") else None
            wahl = AMB_BILD.get(ort) or ("amb_bar" if ort == "alvas_bar" else "amb_hafen" if ort in AMB_HAFEN else (
                "amb_nacht" if nacht else "amb_deck"))
    elif status == "szene":
        s = (state.get("szene") or {}).get("def") or {}
        ort = s.get("ort", "")
        if s.get("id") == "explosion":
            wahl = "feuer_loop"
        elif ort == "alvas_bar":
            wahl = "amb_bar"
        elif ort in AMB_HAFEN:
            wahl = "amb_hafen"
        elif nacht:
            wahl = "amb_nacht"
        elif ort in AMB_DECK:
            wahl = "amb_deck"
    elif status == "taktik":                           # Karte der Belagerung, Morgenliste und Flicken
        t = state.get("taktik") or {}                  # Beim Manoever stirbt niemand, da bleibt es beim Hafen
        wahl = "feuer_loop" if t.get("phase") == "bestand" else "amb_hafen" if t.get("art") == "manoever" else "amb_taktik"
    elif status == "sturm":                            # Sturm an Tag 5: Wind und Wellen unter den Krisen-Effekten
        wahl = "amb_nacht" if nacht else "amb_deck"
    elif status in ("wahl", "kabine"):
        wahl = "amb_nacht" if nacht else "amb_deck"
    return wahl if wahl and katalog(base, module).get(wahl) else None

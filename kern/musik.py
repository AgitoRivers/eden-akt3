"""Local curated background music; selection never consumes game randomness."""
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

from . import ereignisse


@lru_cache(maxsize=8)
def _library(path, modified):
    return json.loads(Path(path).read_text(encoding="utf-8"))["tracks"]


def tracks(base, module):
    if module != "eden_rise":
        return []
    root = Path(base) / "module" / module / "musik"
    original, selected = root / "bibliothek.json", root / "auswahl.json"
    records = _library(str(original), original.stat().st_mtime_ns) if original.is_file() else []
    if selected.is_file():
        approved = _library(str(selected), selected.stat().st_mtime_ns)
        replaced = {track["slot"] for track in approved}
        records = [track for track in records if track["slot"] not in replaced] + approved
    return records


def audio_path(base, module, track_id):
    if not re.fullmatch(r"[0-9a-f]{32}", track_id):
        return None
    root = (Path(base) / "module" / module / "musik").resolve()
    record = next((t for t in tracks(base, module) if t["id"] == track_id), None)
    if not record:
        return None
    path = (root / record["file"]).resolve()
    if path.parent != root / "audio" or path.suffix not in (".flac", ".mp3") or not path.is_file():
        return None
    return path


def _playlist(base, module, slot):
    return [{"id": t["id"], "title": t["title"], "url": "/musik/audio/" + t["id"], "gain": t["gain"], "loop": False}
            for t in sorted((t for t in tracks(base, module) if t["slot"] == slot and audio_path(base, module, t["id"])),
                            key=lambda t: t["id"])]


# Bordmusik nach Tageszeit (Duc 27.10.2026): Phasenwahl, Anrufe und Orte ohne eigene Regel sind nicht mehr still
BORD = {"fruehstueck": "crew_alltag", "tag": "deck_tag", "nachmittag": "deck_tag", "dinner": "crew_messe",
        "abend": "nachts_vor_anker", "nacht": "nachts_vor_anker"}


def hint(base, module, state):
    extra = None                                       # zweiter Slot, dessen Titel mit in die Playlist kommen
    result = {"slot": None, "track": None, "playlist": [], "stille": True, "uebergang_ms": 1800}
    if module != "eden_rise":
        return result
    if not state or state.get("status") in ("persona_wahl", "prolog"):
        slot, context = "hauptthema", "title"
    else:
        status, phase = state.get("status"), state.get("phase")
        scene = (state.get("szene") or {}).get("def") or {}
        sid, location = scene.get("id", ""), scene.get("ort", "")
        if status == "szene" and sid in ("blackout", "explosion", "brand"):
            result["uebergang_ms"] = 0
            return result
        if status == "kampf":
            fight = state.get("kampf") or {}
            definition = fight.get("def") or {}
            enemy = ((fight.get("gegner") or [{}])[0].get("def") or {})
            outcome = (fight.get("ergebnis") or {}).get("art")
            if outcome:
                slot = "kampf_sieg" if outcome in ("ko", "aufgabe") else "kampf_niederlage"
                result.update(einmalig=True, uebergang_ms=0)
            elif definition.get("boss") or (enemy.get("boss") and not str(definition.get("enemy")).startswith("tk_")) or definition.get("enemy") == "tk_white":
                slot = "kampf_boss"
            elif definition.get("musik"):              # Begegnung bestimmt selbst (Red Trio: ernster Pfad)
                slot = definition["musik"]
            elif definition.get("enemy") in ("moewe", "ratte", "affe"):
                slot = "kampf_komisch"
            elif definition.get("enemy") in ("keiler", "keiler_kloster", "hund_wild", "hund_alpha", "hunde_paar",
                                             "ratte_alpha", "schlange", "loewe_schwarz", "wildschwein_affe",
                                             "bache", "wolf", "wolf_alpha", "baer_junges",
                                             "panzer_mufflon", "ark_hyaene", "ark_hyaene_alpha"):
                slot = "kampf_tiere"                   # Tier-Gegner (Duc 27.10.2026): Trommeln statt Surf Rock
            elif definition.get("enemy") in ("pirat", "fackelpirat", "agent", "agent_fuehrer", "agent_nass",
                                             "hirtendrohne", "rt_danzel", "tk_robot", "tk_robot_schwer", "tk_schuetze",
                                             "tk_gunner", "tk_brawler", "tk_bonaventure", "brute_solo", "tk_kobra", "tk_skorpion"):
                slot = "kampf_gefaehrlich"
            else:
                slot = "kampf_normal"
            context = str(fight.get("id", "")) + "|" + str(outcome or "fight")
        elif status == "verhandlung":                  # Anhoerung (Duc 26.10.2026): Bogen statt Stille
            hearing = state.get("verhandlung") or {}
            step = hearing.get("schritt")
            confession = _playlist(base, module, "anhoerung_gestaendnis")
            if confession:                             # spielt der Client nur, solange das Gestaendnis laeuft (Duc 27.10.2026)
                result["gestaendnis"] = {"slot": "anhoerung_gestaendnis", "stille": False, "playlist": confession,
                                         "uebergang_ms": 1800}
            if hearing.get("fertig") or step == "urteil":
                slot = "event_wholesome" if hearing.get("urteil") in ("erbarmen", "entlastet") else "event_ernst"
            elif step in ("rolle", "plaedoyer"):
                result["uebergang_ms"] = 2500          # Stille fuer Gestaendnis, Rolle und Plaedoyer
                return result
            elif (hearing.get("aussage") or {}).get("stufe"):
                slot = "kampf_gefaehrlich"             # nachgebesserte Aussage: in die Ecke gedraengt
            else:
                slot = "mysterium"
            context = str(state.get("id", "")) + "|hearing|" + slot
        elif status == "taktik":                       # Karte der Belagerung: laeuft beim Nachdenken durch, die Morgenliste bleibt wie ihr Event
            slot = "event_ernst" if (state.get("taktik") or {}).get("phase") == "bestand" else "taktik_karte"
            context = str(state.get("id", "")) + "|taktik|" + slot
        elif status == "sturm":                        # Sturm an Tag 5 (27.10.2026): Sturm-Track, am Morgen warm oder ernst
            storm = (state.get("sturm") or {}).get("laufend") or {}
            stage = (storm.get("bilanz") or {}).get("stufe")
            slot = "sturm" if not stage else ("event_wholesome" if stage == "gut" else "event_ernst")
            context = str(state.get("id", "")) + "|storm|" + str(storm.get("teil", "")) + "|" + slot
        elif status == "ende":
            slot, context = "calvi_tisch", "ending"
        elif status in ("wahl", "kabine"):
            slot = "kabine" if status == "kabine" else BORD.get(phase)
            if not slot:
                return result
            context = "|".join(str(state.get(k, "")) for k in ("id", "tag", "phase")) + "|" + status
        elif status == "ereignis":
            data = ereignisse.daten(str(Path(base) / "module" / module)) or {}
            event_id = (state.get("event") or {}).get("id", "")
            event = data.get("_index", {}).get(event_id, {})
            special = {"hy_lea_plankton": "leuchtendes_meer", "ab_casanova_flamenco": "casanova_flamenco",
                       "ab_lola_klopft": "lola_abend", "ab_lola_handy": "lola_abend",
                       "ab_alva_barabend": "alva_abend", "ab_alva_handy": "alva_abend"}
            if event.get("art") == "ort" and event_id[:3] in ("kl_", "hk_", "bg_"):   # Missions-Frames: Expedition je Ort
                special[event_id] = "expedition_hafen" if event_id.startswith("hk_") else "expedition_macchia"
            if event_id.startswith(("bl_nacht_", "bl_na_")):   # Belagerung nachts: keine Bossa, Naehe nur in der Intim-Szene (Duc 01.11.2026)
                still = event_id.startswith("bl_nacht_") or event_id.endswith("_still")
                special[event_id] = "nachts_vor_anker" if still else "sophia_naehe" if event_id.startswith("bl_na_sophia") else "naehe"
            if event.get("musik") == "stille":         # Frame verlangt Stille (Mr. White)
                return result
            slot = special.get(event_id) or event.get("musik") or {"witzig": "event_witzig", "ernst": "event_ernst",
                    "frech": "event_frech", "wholesome": "event_wholesome"}.get(event.get("ton"))
            if not slot:
                return result
            context = str(state.get("id", "")) + "|event|" + event_id
        elif status == "szene":
            explicit = {"auftakt_party": "charter_nacht", "erste_ermittlung": "mysterium",
                        "widerspruch": "mysterium", "etwas_anders": "mysterium", "wendung": "mysterium",
                        "megan_kommt": "megan_bericht", "megan_inspektion": "megan_bericht",
                        "bericht": "megan_bericht", "endfassung": "megan_bericht",
                        "anhoerung": "megan_bericht", "anhoerung_rolle": "megan_bericht",
                        "anhoerung_urteil": "megan_bericht", "sturmvorbereitung": "sturm", "sturmnacht": "sturm",
                        "festa": "festa", "schlussbild": "calvi_tisch",
                        "wache_mit_holm": "holm_wache", "reparaturschritt": "rosi_technik",
                        "cliffhanger": "mysterium"}
            if sid == "naehe" and scene.get("anwesend") == ["sophia"]:
                slot = "sophia_naehe"
            elif sid in ("naehe", "letzte_naehe"):
                slot = "naehe"
            elif sid in explicit:
                slot = explicit[sid]
            elif sid == "nach_dem_urteil":             # wie das Anhoerungsende, dazu "Bittersweet"
                gut = {"urteil_erbarmen", "urteil_entlastet"} & set(state.get("flags") or [])
                slot, extra = ("event_wholesome" if gut else "event_ernst"), "nach_urteil"
            elif sid == "holm_abschied":
                return result
            elif scene.get("anruf"):                   # Stimme duckt die Bordmusik automatisch
                slot = BORD.get(phase)
            elif location == "calvi_harbour":
                slot = "calvi_tisch"
            elif location == "village_piazza":
                slot = "dorf_gassen"
            elif location == "alvas_bar":
                slot = "alvas_bar"
            elif sid == "landgang" or location in ("village_harbour", "alvas_terrace"):
                slot = "hafen_tag"
            elif scene.get("frei") and "rosi" in scene.get("anwesend", []) and location in ("power_room", "generator_room", "workshop"):
                slot = "rosi_technik"
            elif scene.get("frei") and location in ("crew_mess", "galley"):
                slot = "crew_messe"
            elif scene.get("frei") and phase == "nacht":
                slot = "nachts_vor_anker"
            elif phase == "fruehstueck":
                slot = "crew_alltag"
            elif location in ("aft_deck", "sun_deck", "solar_deck", "foredeck", "swim_platform") and phase != "nacht":
                slot = "deck_tag"
            else:
                slot = BORD.get(phase)                 # Hauptsalon, Werkstatt, Tender-Garage ... und nachts
            if not slot:
                return result
            context = "|".join(str(state.get(k, "")) for k in ("id", "tag", "phase")) + "|" + sid
        else:
            return result
    candidates = sorted((t for t in tracks(base, module) if t["slot"] in (slot, extra) and audio_path(base, module, t["id"])),
                        key=lambda t: t["id"])
    if not candidates:
        return result
    if slot == "hauptthema":
        selected = max(candidates, key=lambda t: t["created"])
    else:
        index = int.from_bytes(hashlib.sha256(context.encode()).digest()[:8], "big") % len(candidates)
        selected = candidates[index]
    playlist = _playlist(base, module, slot) + (_playlist(base, module, extra) if extra else [])
    return dict(result, slot=slot, stille=False, playlist=playlist,
                track={"id": selected["id"], "title": selected["title"],
                       "url": "/musik/audio/" + selected["id"], "gain": selected["gain"], "loop": False})

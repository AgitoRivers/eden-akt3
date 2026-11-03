# -*- coding: utf-8 -*-
r"""Nachzug 29.10.2026 (Duc „9 nachziehen“, Spieltest-Bot): Bilder fuer Items ohne items\<id>.webp und die Zuordnung
der Profil-/Missions-Hintergruende fuer Figuren ohne Raum an Bord - alles auf einer Abnahmeseite.

    python werkzeuge\item_nachzug_bilder.py              fehlende Item-Bilder rendern + Abnahmeseite
    python werkzeuge\item_nachzug_bilder.py gps_track    nur diese neu
    python werkzeuge\item_nachzug_bilder.py --seite      nur die Seite
    python werkzeuge\item_nachzug_bilder.py --einbauen   abgenommene PNGs -> module\eden_rise\items\<id>.webp

Gleicher Look wie item_bilder.py (Produktfoto auf Leinen, Krea2 Port 8189). Motive positiv formuliert, glatte Flaechen."""
import json, os, random, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HIER)
sys.path.insert(0, HIER)
import item_bilder as IB  # noqa: E402

ORDNER = os.path.join(EDEN, "docs", "abnahme", "item_nachzug")
SPEC = os.path.join(EDEN, "docs", "abnahme", "item_nachzug.json")
ST_BG = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\backgrounds"

MOTIV = {
    "serial_mismatch": "a small brushed steel engine plate with an engraved serial number lying on an open ship's logbook "
                       "with neat handwritten columns, one entry circled in red pencil",
    "power_log": "a long curled paper printout strip from a ship's power monitor showing a calm line graph with one sharp "
                 "tall spike, a red pencil mark next to the spike",
    "gps_track": "a rugged marine tablet showing a nautical chart of a rocky coastline with a glowing blue route line that "
                 "suddenly bends away in a wide loop towards red cliffs",
    "paris_call": "a black smartphone lying face up, its glowing screen showing an incoming call over a photo of the "
                  "Eiffel Tower at night",
    "breaker_note": "a single ship's electrical circuit breaker with a short strip of beige masking tape on it, marked with "
                    "quick pen strokes",
    "burnt_cable": "a white phone charging cable, partly charred and melted near the plug, the plug blackened, coiled loosely",
    "dumenica_amulet": "a small silver pendant shaped like an open human hand with five fingers, palm facing the viewer, "
                       "smooth polished silver, hanging from a simple black cord",
    "legion_kepi": "a French Foreign Legion kepi seen from the side: tall cylindrical cap covered in bright white fabric, "
                   "a black leather visor and a slightly frayed band, standing upright",
    "laetitia_scarf": "a faded red woollen scarf, a little damp, loosely folded, a few dry pine needles caught in it",
    "av_radio": "a black military field radio with a short rubber antenna, a smooth matte casing and a small plain white "
                "logo plate on the front",
    "ir_controller": "a grey handheld remote control with a small dark infrared lamp at the top and one large round dial, "
                     "smooth plastic casing",
    "ghjuvan_knife": "an old folding shepherd's knife with a smooth polished horn handle and a half open steel blade",
    "foreign_part": "a small black electronic module with a smooth casing, a tiny plain white logo and a short flat ribbon "
                    "cable",
    "gennaro_drawing": "a child's crayon drawing on white paper of a smiling man with a big moustache in a little red boat on "
                       "blue waves under a yellow sun",
    "collar_crate": "a heavy grey plastic transport crate with its lid closed and latched, a small plain white logo and a "
                    "stencilled code on the side",
    "ghjacumu_medal": "a small round tin saint's medal on a short chewed green string",
    "bastien_ring": "a delicate silver ring with one tiny blue stone sitting in an open small dark blue velvet box",
    "treasure_notes": "a clear waterproof document folder holding old photographs of a wooden schooner and a nautical map "
                      "of a bay with one red circle drawn on it",
    "lea_chart_page": "a single page torn from an old nautical chart book, soft pencil lines of a bay, one small pencil cross "
                      "and a faded date in the margin",
}
# Figuren ohne Raum an Bord -> vorhandener Hintergrund fuer Profil und Missionen (nur Zuordnung, kein neues Bild)
HINTERGRUND = {
    "megan": "eden_hq_megan_office.png", "nonna": "eden_rise_monastery_kitchen.png",
    "isabelle": "eden_rise_monastery_garden_dusk.png", "frederico": "eden_rise_monastery_gate.png",
    "laetitia": "eden_rise_mountain_lake.png", "adrien": "eden_rise_abandoned_mountain_hut.png",
    "wolff": "eden_rise_genoese_tower_camp.png", "ghjuvan": "eden_rise_bergerie_interior.png",
    "dumenica": "eden_rise_mazzera_hut.png", "gennaro": "eden_rise_gennaro_cell.png",
    "matteu": "eden_rise_grotto_steps.png", "chloe": "eden_rise_treasure_camp.png",
    "riscossore": "eden_rise_smugglers_tunnel.png", "sirene": "eden_rise_underground_pool_tide.png",
}


def seite():
    modul = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
    items = [{"id": iid, "titel": "Item · %s" % modul["items"].get(iid, {}).get("label", iid),
              "bild": os.path.join(ORDNER, iid + ".png"), "soll": MOTIV[iid]} for iid in MOTIV]
    items += [{"id": "bg_" + pid, "titel": "Hintergrund · %s" % modul["personen"][pid]["name"],
               "bild": os.path.join(ST_BG, bg), "soll": "Profil und Missionen: %s (vorhandenes Bild)" % bg}
              for pid, bg in HINTERGRUND.items()]
    spec = {"id": "item_nachzug", "titel": "Nachzug fehlender Bilder – Abnahme",
            "hinweis": "19 neue Item-Bilder und 14 Hintergründe für Figuren ohne Raum an Bord (vorhandene Bilder, nur "
                       "zugeordnet). OK / Neu + Notiz.", "items": items}
    json.dump(spec, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, os.path.join(HIER, "abnahme_seite.py"), SPEC], check=True)


def einbauen():
    ziel = os.path.join(EDEN, "module", "eden_rise", "items")
    for iid in MOTIV:
        IB.thumbnail(ORDNER, ziel, iid)
    print("eingebaut:", len(MOTIV))


def main():
    if "--seite" in sys.argv:
        return seite()
    if "--einbauen" in sys.argv:
        return einbauen()
    os.makedirs(ORDNER, exist_ok=True)
    wahl = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziele = wahl or [i for i in MOTIV if not os.path.exists(os.path.join(ORDNER, i + ".png"))]
    bg = IB.HINTERGRUENDE[IB.HINTERGRUND]
    auftraege = {i: IB.post("/prompt", {"prompt": IB.graph(IB.STIL.format(motiv=MOTIV[i], hintergrund=bg), ORDNER, i,
                                                           random.randint(1, 2 ** 31), nsfw=True)})["prompt_id"]
                 for i in ziele}
    offen = IB.warten(auftraege, lambda n: print("fertig", n, flush=True))
    if offen:
        print("nicht fertig:", ", ".join(offen))
    seite()


if __name__ == "__main__":
    main()

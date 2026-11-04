# -*- coding: utf-8 -*-
"""Kaempfe Akt 3 (04.11.2026, Drehbuch docs/wiki/welt/drehbuch_akt3.md 5.23, 5.24, F-10). Eingebunden von kaempfe_eden_rise.py.

  a3_scrap_drohne / a3_scrap_paar   The Scrap Field: liegengebliebene Maschinen in der Macchia (Stahl, Klasse maschine)
  a3_villa_keller                   zwei Agenten und ein Roboter im Weinkeller der Villa (Gruppe)
  a3_alon                           Endkampf auf der Terrasse: Alon im Exoskelett, Luft, toedlich, Boss
Bilder: Platzhalter aus vorhandenen Hintergruenden, gewuenscht in docs/uebergabe/akt3_bestellungen.md (scrap_field,
villa_cellar, villa_terrace). Alons Sprite: Platzhalter AgentAlpha, bis "AlonExo" bei Character Design da ist."""


def SP(label, icon, bonus=0, effect=None, dodge_only=False, finte=None):
    s = {"label": label, "icon": icon, "bonus": bonus, "effect": effect, "dodge_only": dodge_only}
    if finte:
        s["finte"] = dict(finte)
    return s


def OUT(text, flag=None):
    return {"text": text, "folgen": [{"flag": flag}] if flag else []}


ZOEGERN_LANG = {"art": "zoegern", "bei": 0.75, "halt": 650}
TAEUSCHUNG = {"art": "taeuschung", "bei": 0.8, "zurueck": 0.55}

ENEMIES = {
    "alon_exo": {
        "name": "Alon Varenne", "sprite": "AgentAlpha", "cls": "mensch", "element": "luft", "tier": "toedlich",
        "attack": {"label": "Servo Strike", "icon": "🦾", "finte": dict(TAEUSCHUNG)},
        "specials": {"w1": SP("Reads Your Move", "🧠", bonus=2, effect="geschwaecht"),
                     "s1": SP("Full Power", "🦾💥", bonus=11, finte=ZOEGERN_LANG)},
        "weakness": None, "parade": "sprite", "boss": True, "parade_ziel": 65,
        "immune": {"charm": "“I wrote the book on charm, Duc. Literally. It's on Amazon.”",
                   "courage": "“Fear? I have a ten-year plan. Fear isn't in it.”"},
        "taunt": {"gruppe": "maschine", "sfx": "kampf_unit01"}},
}


def _b(titel, ziel, bild, gegner, level, ko, aufgabe, entkommen, niederlage, flucht=True, gruppe=None, lp=None, flags=None):
    """flags: {ausgang: flag} - z. B. der Endkampf setzt a3_alon_besiegt oder a3_alon_niederlage."""
    fl = flags or {}
    b = {"title": titel, "goal": ziel, "image": bild, "enemy": gegner, "level": level, "flee_allowed": flucht,
         "expedition_niederlage": True,
         "outcomes": {"ko": OUT(ko, fl.get("ko")), "aufgabe": OUT(aufgabe, fl.get("aufgabe")), "entkommen": OUT(entkommen, fl.get("entkommen")),
                      "flucht": OUT("You back away.", fl.get("flucht")), "niederlage": OUT(niederlage, fl.get("niederlage"))}}
    if gruppe:
        b.update(enemies=gruppe, lp_faktoren=lp)
    return b


ENCOUNTERS = {
    "a3_scrap_drohne": _b("Something Still Moves", "Get past the drone", "eden_rise_antenna_ridge.png", "hirtendrohne", 6,
                          "The drone drops into the grass and goes dark. Rosi would want the steel.",
                          "The drone hums, turns, and flies back towards the villa.", "The drone is gone over the ridge.",
                          "A pulse knocks you flat. When you wake up, the drone is gone."),
    "a3_scrap_paar": _b("Two Left Behind", "Take the steel", "eden_rise_antenna_ridge.png", "hirtendrohne", 7,
                        "Both drones lie still between the rocks. Good steel, all of it.",
                        "The drones lift off together and disappear.", "They're gone.",
                        "The drones circle above you until you stop moving.",
                        gruppe=["hirtendrohne", "hirtendrohne"], lp=[0.7, 0.7]),
    "a3_villa_keller": _b("The Wine Cellar", "Get to the server", "eden_rise_crate_hall.png", "agent_fuehrer", 8,
                          "The two agents are asleep between the barrels. The robot sits down like a tired dog.",
                          "They raise their hands. One of them says: “We just work here.”", "They run up the stairs.",
                          "A white flash between the barrels. You wake up outside the cellar door.",
                          flags={"ko": "a3_keller_frei", "aufgabe": "a3_keller_frei"},
                          gruppe=["agent_fuehrer", "agent", "hirtendrohne"], lp=[0.8, 0.6, 0.6]),
    "a3_alon": _b("Name Your Price", "Stop Alon Varenne", "eden_rise_village_rooftops.png", "alon_exo", 10,
                  "The exoskeleton locks up. Alon sits down on the terrace, breathing hard. For once he says nothing.",
                  "Alon raises one metal hand. “Fine. Fine. You win this one.”", "Alon steps back into the villa and locks the glass door.",
                  "Alon stands over you. “Go home, Duc. The commission is tomorrow. I'll be watching.”", flucht=False,
                  flags={"ko": "a3_alon_besiegt", "aufgabe": "a3_alon_besiegt", "entkommen": "a3_alon_entkommen",
                         "niederlage": "a3_alon_niederlage"}),
}

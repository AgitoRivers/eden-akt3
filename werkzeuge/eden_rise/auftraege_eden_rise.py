# -*- coding: utf-8 -*-
"""Auftraege und Orte von Eden Rise (E-074, 26.10.2026) -> module\\eden_rise\\auftraege.json (kern/auftraege.py).

Auftraege sind die grossen Missionen neben den Schnelljobs: Annahme, Schritte, Abschluss mit Uebergabe, mindestens eine
graue Entscheidung (E-073). Ihr Stand steht nur in Flags, die Frames des Orts (ereignisse_kloster.py) setzen sie.
Orte erscheinen in der freien Phase als Karte neben den Szenen und kosten die ganze Phase.

Laufen lassen NACH ereignisse_basis.py (prueft die Start-Frames gegen ereignisse.json)."""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
ZIEL = os.path.join(EDEN, "module", "eden_rise", "auftraege.json")

# Red Trio (Duc 30.10.2026, ereignisse_red_trio.py): startet nur, wenn die Platte geholt ist, Fenster bis Ende Tag 14
_RT = [{"flag": "kloster_fertig"}, {"flag": "grotte_fertig"}, {"flag": "kl_nische_geleert"}, {"nicht": {"tag_ab": 15}},
       {"nicht": {"flag": "red_trio_fertig"}}]
_RT_PFADE = ["rt_danzel_fertig", "rt_bibi_fertig", "rt_charly_fertig"]
_RT_START = [{"wenn": {"alle": _RT + [{"flag": "rt_tisch_fertig"}]}, "id": "rt_white",
              "text": "The man in white is coming for Danzel, Bibi and Charly, up in Nonna Fiora's garden at San Martinu. Takes the whole phase."},
             {"wenn": {"alle": _RT + [{"flag": p} for p in _RT_PFADE]}, "id": "rt_ankunft",
              "text": "You found Danzel, Bibi and Charly. Now they have to get to Nonna Fiora's table at San Martinu. Takes the whole phase."}]
for _m in range(7):                     # welche Pfade schon erledigt sind -> passende Gabelung
    _RT_START.append({"wenn": {"alle": _RT + [{"flag": "rt_getrennt"}]
                               + [{"flag": p} if _m & (1 << i) else {"nicht": {"flag": p}} for i, p in enumerate(_RT_PFADE)]},
                      "id": "rt_gabelung_" + "".join("0" if _m & (1 << i) else "1" for i in range(3)),
                      "text": "The men in black suits scattered Danzel, Bibi and Charly across the macchia. Find them. Takes the whole phase."})
_RT_START += [{"wenn": {"alle": _RT + [{"flag": "rt_1_sieg"}]}, "id": "rt_lager",
               "text": "The three people in red you beat on the path are still out there, and they want that steel plate. Takes the whole phase."}, {"wenn": {"alle": _RT}, "id": "rt_auftritt"}]

ORTE = {
    # Hafenkampf -> "the day after tomorrow, come to my office" (Duc 26.10.2026): ab Tag 4, bis der Auftrag angenommen ist
    "rathaus": {
        "label": "Madame Casanova's Office", "bild": "piazza_treppe", "phasen": ["tag", "nachmittag"],
        "text": "Madame Casanova asked you to come by once the harbour was cleaned up. Takes the whole phase.",
        "wenn": {"alle": [{"flag": "kloster_faden"}, {"tag_ab": 4}, {"nicht": {"flag": "kloster_angenommen"}}]},
        "start": [{"id": "kl_casanova_auftrag"}]},
    "macchia": {
        "label": "The Macchia", "bild": "macchia_path", "phasen": ["tag", "nachmittag"],
        "text": "Up the mountain path towards San Martinu. Takes the whole phase.",
        "wenn": {"flag": "kloster_angenommen"},
        "start": _RT_START + [{"wenn": {"flag": "kloster_fertig"}, "id": "kl_wieder"}, {"id": "kl_start"}]},
    # Ortskapitel Berge (Duc 27.10.2026): ab Tag 9, nach dem Kloster - Petru bittet am Bootsschuppen (ereignisse_berge.py)
    "bootsschuppen": {
        "label": "Petru's Boathouse", "bild": "corsican_fisherman_workshop.png", "phasen": ["tag", "nachmittag"],
        "text": "The light is on in Petru's boathouse. It's never on at this hour. Takes the whole phase.",
        "wenn": {"alle": [{"flag": "kloster_fertig"}, {"tag_ab": 9}, {"nicht": {"flag": "berge_angenommen"}}]},
        "start": [{"id": "bg_petru_auftrag"}]},
    "berge": {
        "label": "The Mountains", "bild": "chestnut_switchbacks", "phasen": ["tag", "nachmittag"],
        "text": "Up through the chestnut woods towards the Genoese tower. Takes the whole phase.",
        "wenn": {"flag": "berge_angenommen"},
        "start": [{"wenn": {"flag": "berge_fertig"}, "id": "bg_wieder"},
                  {"wenn": {"flag": "bg_wolff_niederlage"}, "id": "bg_wolff_verloren"},
                  {"wenn": {"flag": "bg_bergerie_erreicht"}, "id": "bg_bergerie_zurueck",
                   "text": "Back up to the bergerie, where Laetitia and her soldier Adrien are waiting. Takes the whole phase."},
                  {"wenn": {"flag": "bg_turm_erreicht"}, "id": "bg_turm_zurueck",
                   "text": "Back up to the Genoese tower, where Wolff and the Legion are looking for Laetitia. Takes the whole phase."},
                  {"id": "bg_start"}]},
    "hochweide": {
        "label": "Ghjuvan's Pasture", "bild": "high_pasture", "phasen": ["tag", "nachmittag"],
        "text": "Ghjuvan, the last shepherd, and the bear that takes his sheep. Takes the whole phase.",
        "wenn": {"alle": [{"flag": "bg_ghjuvan_getroffen"},
                          {"nicht": {"alle": [{"flag": "bg_u1_junge_gesehen"}, {"flag": "bg_baer_getoetet"}]}},
                          {"nicht": {"flag": "bg_u1_verkauft_gesehen"}},
                          {"nicht": {"alle": [{"flag": "bg_u1_fertig"}, {"flag": "bg_baer_frei"},
                                              {"nicht": {"flag": "bg_ghjuvan_tot"}}]}}]},
        "start": [{"wenn": {"flag": "bg_ghjuvan_tot"}, "id": "bg_u1_wieder_leer"},
                  {"wenn": {"flag": "bg_baer_getoetet"}, "id": "bg_u1_wieder_tot"},
                  {"id": "bg_u1_start"}]},
    "seehuette": {
        "label": "The Hut by the Lake", "bild": "mazzera_hut", "phasen": ["tag", "nachmittag"],
        "text": "Old Dumenica's hut. She wants the black beast from her dream dead. Takes the whole phase.",
        "wenn": {"alle": [{"flag": "bg_dumenica_getroffen"}, {"nicht": {"flag": "bg_u2_fertig"}}]},
        "start": [{"id": "bg_u2_start"}]},
    # Akt 2 Woche 2 (Duc 27.10.2026, ereignisse_grotte.py): Toto gesteht an Tag 11, Kevin klaut an Tag 12
    "grotte": {
        "label": "The Smugglers' Grotto", "bild": "grotto_steps", "phasen": ["tag", "nachmittag"],
        "text": "Low tide under Punta d'Orsu. Totò has the boat ready. Takes the whole phase.",
        "wenn": {"flag": "grotte_offen"},
        "start": [{"wenn": {"flag": "grotte_fertig"}, "id": "gr_wieder"}, {"id": "gr_start"}]},
    # Flut-Nacht (Duc 28.10.2026): abends bei Flut, die Sirene; danach Sammel-Lauf (ereignisse_grotte.py FLUT)
    "grotte_flut": {
        "label": "The Grotto at High Tide", "bild": "grotto_steps", "phasen": ["abend"],
        "text": "Night, high tide, and something humming under the rock. No Totò this time. Takes the whole evening.",
        "wenn": {"alle": [{"flag": "grotte_fertig"}, {"nicht": {"tag_ab": 22}}]},
        "start": [{"id": "fn_start"}]},
    "kevin": {
        "label": "Kevin's Rooftops", "bild": "village_rooftops", "phasen": ["tag", "nachmittag"],
        "text": "A gull, a bell tower and page forty of Lea's chart book. Takes the whole phase.",
        "wenn": {"alle": [{"flag": "kevin_jagd"}, {"nicht": {"flag": "kevin_fertig"}}, {"nicht": {"tag_ab": 15}}]},
        "start": [{"id": "kv_start"}]},
}

AUFTRAEGE = {
    "red_trio": {
        "titel": "The Red Trio", "von": "danzel", "ort": "macchia", "neben": True, "bis_tag": 15,
        "text": "Three people in red want back the steel plate you found in the rock niche above San Martinu. They attack on sight, and they are not very good at it.",
        "angenommen": "rt_gestartet", "fertig": "red_trio_fertig",
        "schritte": [
            {"text": "Get through the two women in red from the bushes.", "erledigt": {"flag": "rt_1_sieg"},
             "rueckblick": "You beat the first of them on the path above San Martinu, and they ran."},
            {"text": "Get through all three on the bridge.", "erledigt": {"flag": "rt_3_sieg"},
             "rueckblick": "You beat Danzel, Bibi and Charly on the bridge. Then men in black suits scattered them across the macchia."},
            {"text": "Find Danzel on the charcoal road.", "erledigt": {"flag": "rt_danzel_fertig"},
             "rueckblick": "You are finding Danzel, Bibi and Charly one by one, after the men in black suits scattered them."},
            {"text": "Find Bibi in the gorge.", "erledigt": {"flag": "rt_bibi_fertig"},
             "rueckblick": "You are finding Danzel, Bibi and Charly one by one, after the men in black suits scattered them."},
            {"text": "Find Charly on the ridge.", "erledigt": {"flag": "rt_charly_fertig"},
             "rueckblick": "You are finding Danzel, Bibi and Charly one by one, after the men in black suits scattered them."},
            {"text": "Get them all to Nonna Fiora's table at San Martinu.", "erledigt": {"flag": "rt_tisch_fertig"},
             "rueckblick": "Danzel, Bibi and Charly sat down at Nonna Fiora's long table at San Martinu."},
            {"text": "Hold Nonna Fiora's garden when Mr. White comes.", "wenn": {"flag": "rt_tisch_fertig"}, "erledigt": {"flag": "red_trio_fertig"}}],
        "grau": [
            {"text": "What you told Danzel", "wahl": {"rt_notiz_gesteht": "You told Danzel to tell Bibi himself.",
                                                      "rt_notiz_kuendigung": "You told Danzel nobody has to know."}},
            {"text": "What you told Bibi about the lion", "wahl": {"rt_notiz_wahrheit": "You told Bibi what you did to her black lion, Mochi.",
                                                                  "rt_notiz_futter": "You said nothing and helped Bibi look for Mochi."}},
            {"text": "What you told Charly", "wahl": {"rt_notiz_mutter": "You told her to go home.",
                                                      "rt_notiz_spiel": "You told her to show Danzel and Bibi the little game she made about them."}}],
        "belohnung": "Incendio (jacket)", "romanze": False},
    "kloster": {
        "titel": "The Silence of San Martinu", "von": "casanova", "ort": "macchia",
        "text": "No herbs, no cheese, no letters from the monastery for three weeks. Madame Casanova thinks the animals "
                "in the harbour came from up there.",
        "angenommen": "kloster_angenommen", "fertig": "kloster_fertig",
        "schritte": [
            {"text": "Climb through the macchia to the monastery of San Martinu.", "erledigt": {"flag": "kl_tor_offen"},
             "rueckblick": "You reached the gate of San Martinu and met Nonna Fiora."},
            {"text": "Find the brothers and Frederico, the boy who ran after them.",
             "erledigt": {"eine": [{"flag": "kloster_frederico_lebt"}, {"flag": "kloster_frederico_tot"}]},
             "rueckblick": "You found out what happened to the brothers and to Frederico, the boy who ran after them."},
            {"text": "Report back to Madame Casanova at the harbour.", "erledigt": {"flag": "kloster_fertig"}}],
        "grau": [
            {"text": "Trail or treasure at the fork",
             "wahl": {"kl_faehrte": "You followed the blood trail and the child's sandal.", "kl_schatz": "You climbed to the shining niche in the rock first."}},
            {"text": "The lion",
             "wahl": {"kl_loewe_erloest": "You ended his suffering.",
                      "kl_loewe_frei": "You cut the chip out of his neck and let him go."}}],
        "belohnung": "Le Large (boar spear)", "romanze": False},
    "berge": {
        "titel": "The Mountain and the Daughter", "von": "petru", "ort": "berge",
        "text": "Laetitia went up to the summer huts twelve days ago and didn't come back. In the village they say she "
                "was seen with a soldier. Petru, who never asks anyone for anything, asked you.",
        "angenommen": "berge_angenommen", "fertig": "berge_fertig",
        "schritte": [
            {"text": "Climb to the Genoese tower and get past the Legion.", "erledigt": {"flag": "bg_turm_erreicht"},
             "rueckblick": "You got past the Legion and its officer, Wolff, at the Genoese tower."},
            {"text": "Find Laetitia beyond the foggy ridge.", "erledigt": {"flag": "bg_bergerie_erreicht"},
             "rueckblick": "You found Petru's daughter Laetitia at the bergerie, with her soldier Adrien. Wolff wants him."},
            {"text": "Decide what happens to Adrien, Laetitia's soldier.",
             "erledigt": {"eine": [{"flag": "bg_weg_a"}, {"flag": "bg_weg_b"}, {"flag": "bg_weg_c"},
                                   {"flag": "bg_wolff_niederlage"}]},
             "rueckblick": "It is settled what happens to Adrien. Petru is still waiting for news of his daughter."},
            {"text": "Tell Petru what happened to Laetitia, at his boathouse.", "erledigt": {"flag": "berge_fertig"}}],
        "grau": [
            {"text": "Wolff's three questions",
             "wahl": {"bg_wolff_wahr_1": "You told Wolff about the soldier.", "bg_wolff_luege_1": "You told Wolff nothing."}},
            {"text": "Three ways down",
             "wahl": {"bg_weg_a": "You handed Adrien over to Wolff.", "bg_weg_b": "You got Adrien and Laetitia out by sea.",
                      "bg_weg_c": "You showed Wolff Adrien's pictures."}}],
        "belohnung": "Money and a képi, or a friend at the bergerie", "romanze": False},
    "old_grey": {
        "titel": "Old Grey", "von": "ghjuvan", "ort": "hochweide", "neben": True,     # Journal: Neben-Auftrag (29.10.2026)
        "text": "Ghjuvan loses a sheep every night to a bear. There are no bears on Corsica. Ten more sheep and he has to "
                "sell five generations of pasture to the men in black.",
        "angenommen": "bg_u1_angenommen", "fertig": "bg_u1_fertig",
        "schritte": [{"text": "Follow the goat path to the bear.", "erledigt": {"flag": "bg_u1_fertig"}}],
        "grau": [{"text": "The mother bear",
                  "wahl": {"bg_baer_getoetet": "You killed Old Grey for Ghjuvan.",
                           "bg_baer_frei": "You cut the chip out of Old Grey's neck and let her live."}}],
        "belohnung": "Topaz for Le Large, Ghjuvan's knife", "romanze": False},
    "mazzera": {
        "titel": "The Mazzera's Dream", "von": "dumenica", "ort": "seehuette", "neben": True,
        "text": "Old Dumenica hunts in her dreams, and last night the beast had Laetitia's face. Kill it while you are "
                "awake, she says, and the dream breaks.",
        "angenommen": "bg_u2_angenommen", "fertig": "bg_u2_fertig",
        "schritte": [{"text": "Follow the lights on the ridge to the black beast.", "erledigt": {"flag": "bg_u2_fertig"}}],
        "grau": [{"text": "Awake or dreaming",
                  "wahl": {"bg_panther_erloest": "You killed the black beast, awake, as Dumenica asked.",
                           "bg_panther_gehetzt": "You sent the black beast at the agents who controlled it."}}],
        "belohnung": "Dumenica's amulet (advantage on Perception)", "romanze": False},
    "grotte": {
        "titel": "The Smugglers' Grotto", "von": "toto", "ort": "grotte",
        "text": "Totò's cousin Gennaro went into the grotto under Punta d'Orsu on Thursday to fetch a crate for the "
                "wrong people. Three hours, he said. It's Monday.",
        "angenommen": "grotte_offen", "fertig": "grotte_fertig",
        "schritte": [
            {"text": "Go down into the grotto at low tide.", "erledigt": {"flag": "gr_gennaro_gefunden"},
             "rueckblick": "You went down at low tide and found Totò's cousin Gennaro."},
            {"text": "Answer the cry for help from the drowned beach.", "optional": True, "wenn": {"flag": "gr_1_ratten"},
             "erledigt": {"eine": [{"flag": "gr_bastien_befreit"}, {"flag": "gr_bastien_zurueckgelassen"}, {"flag": "gr_bastien_tot"}]}},
            {"text": "Hear out the diver who is down here for his own reasons.", "optional": True,
             "wenn": {"eine": [{"flag": "gr_4_schmuggler"}, {"flag": "gr_leise"}]},
             "erledigt": {"eine": [{"flag": "gr_matteu_wahrheit"}, {"flag": "gr_matteu_belogen"}, {"flag": "gr_matteu_tot"}]}},
            {"text": "Get Gennaro past the man who comes with the tide.",
             "erledigt": {"eine": [{"flag": "gr_kiste_abgegeben"}, {"flag": "gr_kiste_genommen"}]},
             "rueckblick": "You dealt with the man who comes with the tide. The water is rising, and Totò is waiting at the boat."},
            {"text": "Back to Totò before the water reaches the third step.", "erledigt": {"flag": "grotte_fertig"}}],
        "grau": [
            {"text": "Twenty minutes",
             "wahl": {"gr_bastien_befreit": "You freed Bastien from the rubble and came too late for Gennaro.",
                      "gr_bastien_zurueckgelassen": "You went for Gennaro and left Bastien under the rubble, to the tide."}},
            {"text": "What Matteu can't see",
             "wahl": {"gr_matteu_wahrheit": "You told Matteu someone locked him in.", "gr_matteu_belogen": "You told Matteu he drowned and it was quick."}},
            {"text": "The crate",
             "wahl": {"gr_kiste_abgegeben": "You paid Gennaro's debt with the crate of collars.",
                      "gr_kiste_genommen": "You kept the crate of collars as proof."}}],
        "belohnung": "Sussurro (combat knife)", "romanze": False},
    "kevin": {
        "titel": "Page Forty", "von": "lea", "ort": "kevin", "neben": True, "bis_tag": 15,
        "text": "Kevin the gull has stolen page forty of Lea's grandfather's chart book - the bay, the cross, 1924. "
                "He has carried it up to the bell tower.",
        "angenommen": "kevin_jagd", "fertig": "kevin_fertig",
        "schritte": [
            {"text": "Climb out onto the rooftops and chase Kevin.", "erledigt": {"flag": "kv_tauben"},
             "rueckblick": "You chased Kevin the gull over the village rooftops."},
            {"text": "Get up the bell tower to his nest.", "erledigt": {"flag": "kv_kevin"},
             "rueckblick": "You reached Kevin's nest in the bell tower. Lea is waiting for page forty."},
            {"text": "Give page forty back to Lea.", "erledigt": {"flag": "kevin_fertig"}}],
        "grau": [
            {"text": "Kevin's treasure",
             "wahl": {"kevin_stift": "You kept Megan's pen for yourself.", "kevin_fair": "You put everything back in the nest."}}],
        "belohnung": "Lea's trust, and her grandfather's page", "romanze": False},
    "grotte_flut": {
        "titel": "High Tide", "von": "toto", "ort": "grotte_flut", "neben": True, "bis_tag": 22,
        "text": "Since the grotto you hear it at night, when the tide is in: something humming under the rock. "
                "Totò won't row you out. You would have to go yourself.",
        "angenommen": "grotte_fertig", "fertig": "sirene_fertig",
        "schritte": [
            {"text": "Row out to the grotto at high tide, alone.", "erledigt": {"flag": "fn_1_ratten"},
             "rueckblick": "You rowed out to the grotto alone at high tide, towards the humming under the rock."},
            {"text": "Go down to the black pool.", "erledigt": {"eine": [{"flag": "fn_geredet"}, {"flag": "fn_gegangen"}]},
             "rueckblick": "You went down to the black pool and met what was humming there."},
            {"text": "Listen to the voice in the black pool.", "erledigt": {"flag": "sirene_fertig"}}],
        "grau": [
            {"text": "The humming",
             "wahl": {"fn_geredet": "You put the weapon away and talked to the woman with the fish tail.", "fn_gegangen": "You backed away, for tonight."}}],
        "belohnung": "", "romanze": False},
}


# Akt 3 (04.11.2026): Karten der Woche 4 (Lend a Hand, Alva, Siri, Nonnas Kiste) aus ereignisse_akt3_woche4.py
sys.path.insert(0, HIER)
import ereignisse_akt3_woche4  # noqa: E402
ORTE.update(ereignisse_akt3_woche4.ORTE)
import ereignisse_akt3_lose  # noqa: E402
ORTE.update(ereignisse_akt3_lose.ORTE)
import ereignisse_akt3_woche5  # noqa: E402
ORTE.update(ereignisse_akt3_woche5.ORTE)
import ereignisse_akt3_romanzen  # noqa: E402
ORTE.update(ereignisse_akt3_romanzen.ORTE)


def pruefe():
    ev = json.load(open(os.path.join(EDEN, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
    idx = {e["id"]: e for e in ev["events"]}
    personen = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))["personen"]
    f = []
    for oid, o in ORTE.items():
        for s in o["start"]:
            if idx.get(s["id"], {}).get("art") != "ort":
                f.append("Ort %s: Start-Frame %s fehlt oder ist kein Ort-Frame" % (oid, s["id"]))
    for aid, a in AUFTRAEGE.items():
        if a["ort"] not in ORTE:
            f.append("%s: Ort %s" % (aid, a["ort"]))
        if a["von"] not in personen:
            f.append("%s: Auftraggeberin %s" % (aid, a["von"]))
        if not a.get("grau"):
            f.append("%s: keine graue Entscheidung (E-073: mindestens eine je Auftrag)" % aid)
        gesetzt = {fo["flag"] for e in ev["events"] for o in e["optionen"]
                   for fo in o["folgen"] + o.get("bei_erfolg", []) + o.get("bei_fehlschlag", []) if "flag" in fo} | {fo["flag_datiert"] for e in ev["events"] for o in e["optionen"] for fo in o["folgen"] if "flag_datiert" in fo}
        for fl in [a["angenommen"], a["fertig"]] + [x for g in a.get("grau", []) for x in g["wahl"]]:
            if fl not in gesetzt:
                f.append("%s: Flag %s wird von keinem Event gesetzt" % (aid, fl))
    return f


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fehler = pruefe()
    for x in fehler:
        print("FEHLER", x)
    if fehler:
        sys.exit(1)
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\auftraege_eden_rise.py - dort aendern.",
               "orte": ORTE, "auftraege": AUFTRAEGE}, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", ZIEL, "-", len(AUFTRAEGE), "Auftraege,", len(ORTE), "Orte")


if __name__ == "__main__":
    main()

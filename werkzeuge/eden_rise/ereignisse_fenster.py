# -*- coding: utf-8 -*-
r"""Event-Fenster fuer Akt 2 (Duc 29.10.2026, Brain Trust Punkt 1+3): Fast alle Events endeten an Tag 6 (WANN((2, 6), ...)
aus Akt-1-Zeiten); ab Tag 7 fand die Engine keinen einzigen Kandidaten mehr - keine Selfies, Abende, Funken, Flirts oder
Bordraete in Akt 2. Hier werden die zeitlosen Events auf Tag 21 geoeffnet, ohne die Event-Dateien selbst anzufassen.

Auswahl (werkzeuge\eden_rise\event_fenster_pruefen.py, Topf "zeitlos", dann von Hand geschaerft): nur breite Fenster, die
an Tag 6 enden (Start <= 4) oder [2, 5]. Bewusst gesetzte Story-Tage (z. B. [3, 4] Megan, [5, 5] Hubschrauber, Festa,
Yamamoto-/Lola-Ketten) bleiben in Akt 1, ebenso alles mit Holm im Krankenhaus, Totos Cousin Gennaro (verschwindet in Akt 2
in der Grotte), Megans Besuch an Bord, Strom/Diesel und dem Vorabend der Anhoerung.

Das Akt-1-Fenster bleibt unveraendert (Tag 7 = Anhoerung ohne Zufalls-Events, Regel in ereignisse_basis.pruefe); dazu
kommt ein zweites Fenster wann.akt2 = [8, 21], das kern/ereignisse.passt mitprueft. Jedes Event kommt weiter nur einmal je
Durchlauf (gesehen). Geoeffnete Events tragen "nachlauf": True: die Engine gibt in Akt 2 neuen Akt-2-Events Vorrang und
zieht dort ruhiger (Duc: 2-4 Events am Tag).
Selfies, Abende und Funken (Duc 30.10.2026): laufen bis Tag 35, sonst steigen in Akt 3 die Stufen ohne Belohnung. Die ersten
Abende von Lola und Jana sind mit offen, weil ihre Wiederholungen an den Flags dieser Abende haengen.
Akt 3 (04.11.2026, Drehbuch docs/wiki/welt/drehbuch_akt3.md): Gags bis Tag 31 (Texte auf Alon, Holm, Festa, Minicu,
Megan, "tomorrow" geprueft), mit Maxwell bis Tag 29, Handy-Events ungeprueft bis Tag 21. Ist die Yacht schwer beschaedigt
(tk_yacht_weg), sperrt kern/ereignisse.passt die Gags an Bord bis zur Reparatur (a3_yacht_repariert).
Eingebunden in ereignisse_basis.bauen() - nach dem Sammeln aller Events."""

AKT2 = [8, 31]          # Akt 3 (Duc, CLAUDE.md): freie Gags laufen bis Tag 31, ab Tag 32 gagfrei (Drehbuch Akt 3)
AKT2_ALT = [8, 21]      # Handy-Events (hy_): nicht geprueft (Handy-Dateien sind fuer diese Sitzung tabu), bleiben in Akt 2
MIT_MAXWELL = [8, 29]   # Maxwell fliegt Tag 30 bis 32 nach Durban (Drehbuch Akt 3, 5.14)
BIS_ENDE = [8, 35]

OEFFNEN = [
    "ab_alva_barabend", "ab_alva_handy", "ab_jana_handy", "ab_jana_nacht", "ab_lola_handy", "ab_lola_klopft",
    "fk_rosi_schicht", "sf_megan_5_hubschrauber", "sf_rosi_5_werkstatt", "ak_chiara_brueckennock", "ak_chiara_herkunft",
    "auf_karaoke", "bk_rosi_tafel", "bk_siri_goldene_stunde", "bk_siri_stuhl", "bk_sophia_arm", "bk_sophia_buechlein",
    "br_fish_pie", "br_handtuecher", "br_jana_tender", "br_nacktbaden", "br_netze_flicken", "br_petrus_boot",
    "br_rosi_ueberstunden", "br_siri_umzug", "br_siris_geburtstag", "br_toto_stand", "br_trinkgeld",
    "du_harpune_chiara", "du_koch_alva", "du_poetry_sophia", "du_tiere_lea", "fk_chiara_frage", "fk_lea_schulter",
    "fk_siri_foto", "fk_sophia_wette", "fl_alva_eis", "fl_alva_schritt", "fl_alva_tuer", "fl_chiara_kragen",
    "fl_chiara_tee", "fl_chiara_zehn", "fl_elsa_strafzettel", "fl_jana_knoten", "fl_lea_fakt", "fl_lea_neopren",
    "fl_lea_salut", "fl_lea_seite41", "fl_lola_bao", "fl_lola_haengematte", "fl_lola_mehl", "fl_lola_sonnencreme",
    "fl_rosi_bandana", "fl_rosi_schicksal", "fl_rosi_vespa", "fl_siri_blick", "fl_siri_date", "fl_siri_schulter",
    "fl_sophia_blick", "fl_sophia_ungeprobt", "g1_chiara_pause", "g1_elsa_schwimmwesten", "g1_fiona_muetze",
    "g1_katerfruehstueck", "g1_lola_delfin", "g1_lola_strandkueche", "g1_petru_fisch", "g1_petru_oktopus",
    "g1_siri_pullover", "g1_siri_tanz", "g1_sophia_zweitbesetzung", "g1_toto_pizza", "g1_unit01_klonk",
    "g1_unit01_staendchen", "gv_arancini_duell", "gv_armdruecken", "gv_aussenborder", "gv_chiara_italienisch",
    "gv_einkaufsliste", "gv_elsa_roman", "gv_gute_kabine", "gv_kevin_auktion", "gv_musik_nachts", "gv_ocean_glitter",
    "gv_oktopus", "gv_quiz", "gv_seestueck", "gv_siri_yasin", "gv_toto_elsa", "gv_tuersteher", "gv_versoehnung",
    "hy_alva_sevilla", "hy_alva_tafel", "hy_chiara_jonas", "hy_elsa_segler", "hy_elsa_vorwarnung", "hy_lea_plankton",
    "hy_lola_koster", "hy_lola_tresen", "hy_lola_ziege", "hy_megan_wrong_chat", "hy_rosi_foto", "hy_siri_caption",
    "hy_siri_ungeschminkt", "hy_sophia_0213", "hy_sophia_kaffee", "hy_toto_spind", "mt_zehn", "mx_chiara_lacht",
    "mx_jana_bewundert", "sf_bibi_3_station", "sf_bibi_4_station", "sf_bibi_5_station", "sf_alva_3_bar", "sf_alva_3_tresen", "sf_alva_3_zimmer", "sf_alva_4_bar", "sf_alva_4_tresen",
    "sf_alva_4_zimmer", "sf_alva_5_bar", "sf_alva_5_tresen", "sf_alva_5_zimmer", "sf_chiara_3_bruecke",
    "sf_chiara_3_kabine", "sf_chiara_3_nock", "sf_chiara_4_bruecke", "sf_chiara_4_kabine", "sf_chiara_4_nock",
    "sf_chiara_5_bruecke", "sf_chiara_5_kabine", "sf_chiara_5_nock", "sf_elsa_3_posten", "sf_elsa_3_verhoerzelle",
    "sf_elsa_4_posten", "sf_elsa_4_verhoerzelle", "sf_elsa_5_posten", "sf_elsa_5_verhoerzelle",
    "sf_isabelle_3_apotheke", "sf_isabelle_3_lavendelbad", "sf_isabelle_4_lavendelbad", "sf_isabelle_4_zelle",
    "sf_isabelle_5_lavendelbad", "sf_isabelle_5_zelle", "sf_jana_3_dusche", "sf_jana_3_koje", "sf_jana_3_shibari",
    "sf_jana_4_koje", "sf_jana_4_shibari", "sf_jana_5_dusche", "sf_jana_5_shibari", "sf_lea_3_beach",
    "sf_lea_3_garage", "sf_lea_3_plankton", "sf_lea_4_garage", "sf_lea_4_plankton", "sf_lea_5_beach",
    "sf_lea_5_garage", "sf_lea_5_plankton", "sf_lola_3_koje", "sf_lola_3_kombuese", "sf_lola_3_sahne",
    "sf_lola_4_koje", "sf_lola_4_kombuese", "sf_lola_4_sahne", "sf_lola_5_koje", "sf_lola_5_kombuese",
    "sf_lola_5_sahne", "sf_megan_3_buero", "sf_megan_3_hubschrauber", "sf_megan_4_buero", "sf_megan_4_hubschrauber",
    "sf_megan_5_buero", "sf_rosi_3_generatorraum", "sf_rosi_3_strand", "sf_rosi_3_werkstatt",
    "sf_rosi_4_generatorraum", "sf_rosi_4_strand", "sf_rosi_4_werkstatt", "sf_rosi_5_generatorraum",
    "sf_rosi_5_strand", "sf_siri_3_dessous", "sf_siri_3_vip", "sf_siri_3_vordeck", "sf_siri_4_dessous",
    "sf_siri_4_vip", "sf_siri_4_vordeck", "sf_siri_5_dessous", "sf_siri_5_vip", "sf_siri_5_vordeck",
    "sf_sophia_3_achterdeck", "sf_sophia_3_koje", "sf_sophia_3_noir", "sf_sophia_4_achterdeck", "sf_sophia_4_koje",
    "sf_sophia_4_noir", "sf_sophia_5_achterdeck", "sf_sophia_5_koje", "sf_sophia_5_noir", "sfn_bibi_3", "sfn_bibi_4", "sfn_bibi_5", "sfn_alva_3", "sfn_alva_4",
    "sfn_alva_5", "sfn_chiara_3", "sfn_chiara_4", "sfn_chiara_5", "sfn_elsa_3", "sfn_elsa_4", "sfn_elsa_5",
    "sfn_isabelle_3", "sfn_isabelle_4", "sfn_isabelle_5", "sfn_jana_3", "sfn_jana_4", "sfn_jana_5", "sfn_lea_3",
    "sfn_lea_4", "sfn_lea_5", "sfn_lola_3", "sfn_lola_4", "sfn_lola_5", "sfn_megan_3", "sfn_megan_4", "sfn_megan_5",
    "sfn_rosi_3", "sfn_rosi_4", "sfn_rosi_5", "sfn_siri_3", "sfn_siri_4", "sfn_siri_5", "sfn_sophia_3",
    "sfn_sophia_4", "sfn_sophia_5", "yk_erwischt", "yk_herkunft", "yk_jana_merkt",
]


def anwenden(events):
    """Zweites Fenster Akt 2 setzen und als Nachlauf markieren. -> Liste unbekannter IDs (Pruefung)."""
    index = {e["id"]: e for e in events}
    fehlt = [i for i in OEFFNEN if i not in index]
    for i in OEFFNEN:
        e = index.get(i)
        if e:
            lang = i.startswith(("sf_", "sfn_")) or e["art"] == "abend"
            if lang:
                fenster = BIS_ENDE
            elif i.startswith("hy_"):
                fenster = AKT2_ALT
            elif "maxwell" in str(e).lower():
                fenster = MIT_MAXWELL
            else:
                fenster = AKT2
            e["wann"]["akt2"] = list(fenster)
            e["nachlauf"] = True
    return fehlt

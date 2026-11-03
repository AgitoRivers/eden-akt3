# -*- coding: utf-8 -*-
"""Event ranking (Duc 25.10.2026): every event scored 1-5 on the agreed criteria, weighted, with a verdict.

Criteria and weights: Bindung 30 % · Spielwirkung 25 % · Humor 20 % (only for funny events; otherwise the other
weights are scaled up) · Frische 15 % · Sehnsucht 10 %. Kanon is a gate: violations are listed as fixes, not scored.
Verdict: behalten · schärfen · umbauen · streichen. Notes are deliberately spoiler-light (Duc wants to be surprised).

    python werkzeuge\\englisch\\event_ranking.py   -> docs/brain_trust/EVENT_RANKING.md
"""
import json, os

# id: (Bindung, Wirkung, Humor or None, Frische, Sehnsucht, Urteil, Notiz)
S = {
    # ---------------------------------------------------------------- Tag 0 und Hafen (Kette, geskriptet)
    "t0_limousine": (4, 3, 4, 5, 4, "behalten", "starker Auftakt, jede Figur in einer Zeile erkennbar"),
    "t0_megan": (5, 5, None, 5, 5, "behalten", "verborgene Wirkung bis zur Anhörung"),
    "t0_holm": (5, 4, None, 5, 4, "behalten", "Knoten-Probe zeigt Holm sofort"),
    "t0_chiara": (5, 4, None, 4, 5, "behalten", "„gefragt werden“ als Romanzen-Kern früh angelegt"),
    "t0_rosi": (5, 4, 4, 5, 4, "behalten", "Kompetenz-Test als Flirt"),
    "t0_maxwell": (4, 3, 5, 5, 3, "behalten", "Flugangst-Gag sitzt"),
    "t0_toto": (4, 4, 4, 4, 3, "behalten", "legt eine Spur, ohne zu verraten"),
    "t0_lola": (5, 4, None, 4, 4, "behalten", "Kochen als Duc-Stärke"),
    "t0_wahl": (2, 4, None, 4, 3, "behalten", "Wahl ist Struktur, kein Inhalt"),
    "t0_wahl2_*": (4, 3, None, 4, 4, "behalten", "zweite Begegnung je Wahl, vier Fassungen"),
    "t0_lea": (4, 4, None, 4, 5, "behalten", "Staunen-Sehnsucht in Reinform"),
    "t0_sophia": (4, 3, None, 4, 3, "behalten", "solide, eher leise"),
    "t0_jana": (4, 3, 4, 4, 3, "behalten", "Katze als Geheimnis gut gesetzt"),
    "t0_siri": (4, 3, None, 4, 4, "behalten", "Kamera-Konflikt sofort klar"),
    "t0_yamamoto": (4, 3, 4, 4, 3, "behalten", "Verbeugungs-Chip ist ein schöner Moment"),
    "t0_abschied_*": (4, 4, None, 4, 4, "behalten", "vier Fassungen je Megan-Chip"),
    "hk_hilfe": (2, 3, None, 4, 4, "behalten", "Übergang in den Kampf"),
    "hk_rosi_*": (5, 4, None, 5, 5, "behalten", "Waffen-Übergabe als Achievement-Moment"),
    "hk_elsa": (4, 3, 4, 4, 3, "behalten", "Elsa in einer Zeile da"),
    "hk_alva": (4, 3, None, 4, 4, "behalten", "Romanzen-Anker im Chaos"),
    "hk_petru": (5, 3, None, 4, 4, "behalten", "leise, wirkt lange nach"),
    "hk_ziege": (3, 4, 4, 5, 4, "behalten", "öffnet den Kloster-Faden"),
    "yk_herkunft": (5, 4, None, 5, 5, "behalten", "Ducs eigene Geschichte, Respekt-Moment"),
    "ak_chiara_herkunft": (5, 4, None, 5, 5, "behalten", "verbindet zwei Herkünfte"),
    "mx_tutorial": (3, 4, 4, 4, 4, "behalten", "Lektion mit Figur statt Menütext"),

    # ---------------------------------------------------------------- Bordrat (Duc entscheidet für die Crew)
    "br_lolas_notvorrat": (4, 5, 4, 4, 4, "behalten", "erste echte Kommando-Entscheidung, Bordregel"),
    "br_drei_minuten": (3, 4, None, 3, 3, "behalten", "Mangel spürbar, Siri-Moment"),
    "br_gaestekabinen": (3, 4, None, 3, 3, "behalten", "Megan-Druck greifbar"),
    "br_yasins_angebot": (3, 5, None, 4, 3, "behalten", "Bordregel + Video-Uhr"),
    "br_festa_auftritt": (3, 3, 4, 4, 3, "behalten", "Festa-Vorbereitung mit Humor"),
    "br_nachtwache": (4, 3, None, 3, 3, "behalten", "Rosi- und Lea-Facetten"),
    "br_petrus_boot": (3, 3, None, 3, 4, "behalten", "Dorf-Anbindung"),
    "br_elsas_kontrolle": (3, 5, None, 4, 3, "behalten", "Schmuggel-Faden mit Folgen"),
    "br_dorfkinder": (4, 3, None, 4, 4, "behalten", "Zugehörigkeit zum Dorf"),
    "br_siris_geburtstag": (5, 4, None, 4, 5, "behalten", "Siri ohne Kamera, starker Moment"),
    "br_crew_kasse": (3, 4, 3, 4, 2, "behalten", "moralischer Graubereich"),
    "br_lola_krank": (3, 3, 4, 3, 3, "behalten", "Rosi-kocht-Gag"),
    "br_kevin_nest": (2, 3, 4, 3, 2, "behalten", "Kevin-Running-Gag"),
    "br_singen_ohne_strom": (4, 3, None, 3, 4, "behalten", "Zugehörigkeit, Siri-Bogen"),
    "br_ein_tisch": (4, 4, None, 3, 4, "behalten", "Crew wird Familie"),
    "br_megan_kommt": (3, 3, 4, 4, 3, "behalten", "Vorbote des Besuchs"),
    "br_nacktbaden": (3, 3, 4, 4, 3, "behalten", "Elsa-Faden mit Humor"),
    "br_rosi_ueberstunden": (5, 4, None, 4, 4, "behalten", "Rosi verletzlich, Versprechen"),
    "br_netze_flicken": (4, 3, None, 4, 4, "behalten", "Petrus Haltung zu Geld"),
    "br_siri_umzug": (4, 4, None, 4, 4, "behalten", "Siris Ablösung sichtbar"),
    "br_trinkgeld": (4, 4, None, 4, 3, "behalten", "Yasins Grauton, Lea schützen"),
    "br_ehrenbuerger": (3, 3, 4, 4, 4, "behalten", "jetzt an Tag 21"),
    "br_investoren_dinner": (3, 4, None, 4, 3, "behalten", "Megan an Bord, Crew am Tisch"),
    "br_abschiedsfest": (4, 3, None, 3, 5, "behalten", "Vorabend der Anhörung"),
    "br_lola_flach": (4, 4, None, 4, 4, "behalten", "Kochen als Stärke, dritter Weg"),

    # ---------------------------------------------------------------- Handy
    "hy_lola_tresen": (3, 3, 4, 3, 3, "behalten", "Lola + Alva in einem Bild"),
    "hy_sophia_0213": (5, 4, None, 3, 5, "behalten", "Sophias Text über Duc"),
    "hy_holm_krankenhaus": (5, 4, None, 4, 4, "behalten", "Holm nach dem Abschied"),
    "hy_holm_nacht": (5, 3, None, 4, 4, "behalten", "Holms Wunde, Item"),
    "hy_megan_mitternacht": (5, 4, None, 4, 4, "behalten", "Megans weiche Seite"),
    "hy_megan_feuern": (3, 4, 4, 4, 3, "behalten", "Mut-Probe mit Witz"),
    "hy_elsa_vorwarnung": (4, 5, None, 4, 3, "behalten", "Elsa beugt eine Regel fürs Dorf"),
    "hy_elsa_segler": (3, 3, None, 3, 4, "behalten", "Wirksamkeit"),
    "hy_casanova_rede": (3, 2, 4, 3, 2, "behalten", "reiner Lacher"),
    "hy_cousin_falsch": (3, 3, 4, 4, 2, "behalten", "Gennaro-Spur"),
    "hy_lola_ziege": (3, 3, 5, 5, 3, "behalten", "Fiona ist ein Highlight"),
    "hy_rosi_foto": (4, 3, 4, 3, 4, "behalten", "Rosis Verlegenheit trägt"),
    "hy_lea_plankton": (5, 3, None, 4, 5, "behalten", "Staunen, schönster Lea-Moment"),
    "hy_siri_ungeschminkt": (5, 3, None, 4, 5, "behalten", "Siri echt"),
    "hy_megan_rundgang": (3, 3, 4, 4, 3, "behalten", "Seekrank durch Bildschirme"),
    "hy_alva_diesel_tanz": (3, 4, 4, 4, 3, "behalten", "Tausch statt Kauf"),
    "hy_sophia_kaffee": (4, 3, None, 4, 4, "behalten", "Sophia sieht Chiara"),
    "hy_lola_koster": (3, 3, 4, 3, 3, "behalten", "doppelt mit „The Taster“"),
    "hy_eden_hotline": (2, 3, 4, 4, 2, "behalten", "Megan-Humor"),
    "hy_holm_letzter_anruf": (5, 4, None, 4, 5, "behalten", "Übergabe des Bootes"),
    "hy_megan_maske": (3, 3, 5, 5, 3, "behalten", "bester Megan-Gag"),
    "hy_toto_spind": (2, 2, 4, 3, 2, "behalten", "Kevin-Pointe"),
    "hy_megan_dinner": (3, 2, 4, 4, 3, "behalten", "Megan will dazugehören"),

    # ---------------------------------------------------------------- Gags mit einer Figur
    "g1_pfannkuchen": (3, 3, 4, 4, 3, "behalten", "Lola-Herz"),
    "g1_drohne": (2, 3, 4, 4, 2, "behalten", "Kescher-Pointe"),
    "g1_reissverschluss": (4, 3, 4, 3, 4, "behalten", "Rosi-Romanze mit Witz"),
    "g1_unit01_klonk": (3, 2, 5, 4, 3, "behalten", "Unit-01-Kette"),
    "g1_unit01_staendchen": (5, 2, 4, 5, 4, "behalten", "Rosis Nonna, Maschinen-Liebe"),
    "g1_kevin_butter": (2, 2, 4, 4, 2, "behalten", "Kevins Ursprung"),
    "g1_blaskapelle": (3, 2, 5, 4, 3, "behalten", "Casanova pur"),
    "g1_fiona_muetze": (2, 2, 4, 3, 2, "behalten", "Fiona-Kette"),
    "g1_siri_tanz": (5, 3, None, 4, 5, "behalten", "Siri lacht ohne Kamera"),
    "g1_chiara_inspektion": (4, 3, 4, 4, 4, "behalten", "Gedicht-Item"),
    "g1_qualle": (2, 2, 4, 3, 2, "behalten", "Slapstick"),
    "g1_toto_pizza": (3, 3, 4, 3, 3, "behalten", "Neapel-Stolz"),
    "g1_yasin_geste": (4, 5, None, 4, 4, "behalten", "Wendepunkt für Siri"),
    "g1_elsa_schwimmwesten": (3, 3, 4, 3, 3, "behalten", "Elsa-Faden"),
    "g1_petru_fisch": (4, 3, 4, 4, 4, "behalten", "Petru lehrt"),
    "g1_chiara_tender": (5, 4, None, 4, 4, "behalten", "Chiaras Kränkung sichtbar"),
    "g1_holm_kaffee": (5, 4, None, 4, 4, "behalten", "Holms Rat, Saat Blinddarm"),
    "g1_kalte_dusche": (2, 3, 4, 3, 2, "behalten", "Strom sparen spürbar"),
    "g1_chiara_pause": (4, 3, None, 3, 4, "behalten", "Chiara lässt los"),
    "g1_siri_pullover": (4, 3, None, 4, 4, "behalten", "stilles Zeichen"),
    "g1_sophia_liest_vor": (3, 3, 4, 4, 3, "behalten", "jetzt mit Lola, Geheimnis bleibt"),
    "g1_helikopter": (3, 2, 5, 4, 3, "behalten", "Megans Auftritt"),
    "g1_megan_schach": (4, 4, 4, 4, 4, "behalten", "Megan auf Augenhöhe"),
    "g1_cousin_schlauchboot": (3, 4, 4, 4, 3, "behalten", "Gennaro-Spur"),
    "g1_katerfruehstueck": (3, 3, 4, 3, 3, "behalten", "Lola nach der Party"),
    "rosi_werkstatt_offen": (4, 4, None, 4, 4, "behalten", "Tag 8, Werkstatt wieder offen"),
    "casanova_saufeder": (4, 4, None, 5, 4, "behalten", "Waffen-Übergabe"),
    "g1_casanova_nebel": (3, 2, 5, 5, 3, "behalten", "Casanova-Höhepunkt"),
    "g1_petru_oktopus": (4, 2, 4, 4, 3, "behalten", "Petru hat einen Freund"),

    # ---------------------------------------------------------------- Gags mit zwei Figuren (Duc entscheidet)
    "gv_ocean_glitter": (3, 3, None, 3, 3, "behalten", "Ordnung gegen Chaos"),
    "gv_strip_poker": (3, 4, None, 4, 3, "behalten", "geschärft: Sophias Bühnenblick, Alvas Rose"),
    "gv_kevin_auktion": (2, 3, 4, 3, 2, "behalten", "Kevin-Kette"),
    "gv_wer_fuehrt": (4, 4, None, 3, 4, "behalten", "Kommando-Frage"),
    "gv_siri_yasin": (5, 4, None, 4, 5, "behalten", "Siris erstes Nein"),
    "gv_arancini_duell": (3, 3, 4, 3, 3, "behalten", "Dorf schaut zu"),
    "gv_megan_sophia": (3, 3, 4, 4, 3, "behalten", "zwei Strateginnen"),
    "gv_toto_elsa": (3, 3, 4, 3, 3, "behalten", "Zenigata gegen Lupin"),
    "gv_festa_kleid": (4, 3, None, 4, 4, "behalten", "Chiara wird gesehen"),
    "gv_casanova_chiara": (3, 3, 4, 3, 3, "behalten", "Gangway-Duell"),
    "gv_armdruecken": (3, 3, 4, 3, 3, "behalten", "Rosi lässt sich nicht gewinnen"),
    "gv_aussenborder": (4, 3, None, 4, 4, "behalten", "Wissenschaft und Hammer"),
    "gv_oktopus": (4, 3, None, 4, 4, "behalten", "Siri weiß etwas"),
    "gv_tarot": (3, 3, None, 3, 3, "behalten", "Sophia rot"),
    "gv_casanova_alva": (3, 3, 4, 3, 3, "behalten", "Fehde berührt"),
    "gv_megan_chiara": (4, 4, None, 4, 4, "behalten", "Duc stellt sich vor Chiara"),
    "gv_keks": (4, 2, 5, 4, 3, "behalten", "Megan lacht"),
    "gv_wahrheit_pflicht": (3, 3, None, 3, 3, "behalten", "Flirt-Spiel"),
    "gv_versoehnung": (4, 3, None, 3, 4, "behalten", "Versöhnung als Lohn"),
    "gv_elsa_alva": (3, 3, 4, 3, 3, "behalten", "Diesel-Witz"),
    "gv_festa_outfits": (3, 3, None, 3, 3, "behalten", "Rosis Kleid"),
    "gv_quiz": (3, 3, 4, 4, 3, "behalten", "Totò schummelt"),
    "gv_elsa_kiste": (3, 3, 5, 4, 3, "behalten", "miauende Kartoffeln"),

    # ---------------------------------------------------------------- Abende, Duelle, Auftritte
    "ab_lola_klopft": (5, 4, None, 3, 5, "behalten", "Lolas Romanzen-Sprosse"),
    "ab_lola_handy": (3, 3, None, 2, 3, "behalten", "Wiederholung, bewusst"),
    "ab_alva_barabend": (4, 4, None, 3, 4, "behalten", "Alvas Romanzen-Stufe"),
    "ab_alva_handy": (3, 3, None, 2, 3, "behalten", "Wiederholung, bewusst"),
    "ab_casanova_flamenco": (4, 3, None, 4, 4, "behalten", "Casanova ohne Amt"),
    "du_koch_lola": (4, 4, 4, 3, 4, "behalten", "Kochen als Stärke"),
    "du_koch_alva": (4, 4, 4, 4, 4, "behalten", "Fusion, Herkunft"),
    "du_koch_toto": (3, 4, 4, 3, 3, "behalten", "Neapel gegen Saigon"),
    "du_reparatur_rosi": (4, 4, 4, 3, 4, "behalten", "jetzt ab Tag 8"),
    "du_harpune_chiara": (4, 4, None, 4, 4, "behalten", "Chiara-Duell"),
    "du_tiere_lea": (4, 3, None, 4, 5, "behalten", "Staunen, Petru"),
    "du_poetry_sophia": (5, 4, None, 5, 4, "behalten", "Sophia hört etwas anderes"),
    "auf_karaoke": (3, 3, 4, 3, 4, "behalten", "Dorf und Crew zusammen"),
    "auf_gitarre": (5, 3, None, 4, 5, "behalten", "Siris Vater"),
    "auf_herkunft": (5, 4, None, 4, 5, "behalten", "jetzt mit Ducs Kanon"),

    # ---------------------------------------------------------------- Akt-1-Bausteine, Megan, Training, Yamamoto
    "mg_tag*": (4, 3, 4, 5, 3, "behalten", "Serie mit Steigerung bis zur Anhörung"),
    "mx_jana_bewundert": (4, 3, None, 4, 3, "behalten", "Jana traut sich"),
    "mx_chiara_lacht": (3, 3, 4, 4, 3, "behalten", "Niederlage mit Würde"),
    "ak_lola_vorkoster": (5, 4, None, 4, 5, "behalten", "Lob-Mechanik"),
    "ak_lola_service": (5, 4, None, 5, 5, "behalten", "Lolas Wunde, stärkstes Lola-Event"),
    "ak_chiara_sternzettel": (4, 3, None, 4, 4, "behalten", "Geheimnis angedeutet"),
    "ak_chiara_brueckennock": (5, 4, None, 4, 5, "behalten", "Chiara lässt dich hinein"),
    "yk_vogel": (3, 2, 4, 4, 2, "behalten", "Running Gag startet"),
    "yk_schatten": (3, 2, 4, 3, 2, "behalten", "Maxwell-Schatten"),
    "yk_falle": (3, 2, 5, 4, 3, "behalten", "Handtuch-Puppe"),
    "yk_jana_merkt": (4, 3, 4, 4, 4, "behalten", "Jana wird mutig"),
    "yk_erwischt": (3, 3, 4, 3, 3, "behalten", "Auflösung des Gags"),
    "yk_liste": (5, 3, None, 5, 5, "behalten", "rührendes Ende der Kette"),
    "mt_erste": (3, 3, 4, 4, 3, "behalten", "Training startet"),
    "mt_nicht_aufhoeren": (4, 3, None, 4, 5, "behalten", "Wachstum"),
    "mt_zehn": (5, 3, None, 4, 5, "behalten", "Janas Sieg, Maxwells „Allergie“"),

    # ---------------------------------------------------------------- Neu aus dem Wiki (25.10.2026, ersetzen 28 schwache Plätze)
    "hy_chiara_jonas": (5, 3, None, 5, 5, "neu", "Chiaras Familie, Gefragt-werden-Mechanik"),
    "hy_alva_sevilla": (4, 3, None, 5, 4, "neu", "Alvas Mutter und der Traum von Sevilla"),
    "hy_alva_tafel": (3, 4, None, 5, 3, "neu", "Tratsch-Tipp deckt jetzt echte Vorlieben auf"),
    "hy_megan_anime": (4, 3, 5, 5, 4, "neu", "Megans Geheimnis, Gag mit Herz"),
    "hy_siri_caption": (5, 5, None, 5, 4, "neu", "Siris Vater trifft Ducs ESG-Beruf"),
    "hy_megan_foto": (4, 3, None, 5, 4, "neu", "Megans Werdegang, Faden zu Chiara"),
    "hy_casanova_konfetti": (3, 4, 5, 5, 3, "neu", "Festa-Einladung mit Slapstick"),
    "br_satellit_sonntag": (4, 4, None, 5, 4, "neu", "Heimweh von Lola und Jana, echter Mangel"),
    "br_jana_tender": (4, 4, None, 5, 4, "neu", "Janas Traum, Totò stolz"),
    "br_holm_paket": (5, 3, None, 5, 5, "neu", "Holm aus der Ferne, Siris Mut"),
    "br_fish_pie": (5, 4, None, 5, 4, "neu", "Petrus Trauer, Bordregel wandert mit"),
    "br_toto_stand": (4, 4, None, 5, 4, "neu", "Totòs Wunsch, Bordregel wandert mit"),
    "br_handtuecher": (3, 4, 4, 5, 3, "neu", "Jana als Fan, Siri vergisst Namen"),
    "g1_alva_tim_tams": (3, 3, 4, 5, 3, "neu", "Lolas Heimat über Alvas Vorrat"),
    "g1_lea_nachttauchen": (4, 3, None, 5, 5, "neu", "Leas Leichtsinn, Elsas Sorge"),
    "g1_sophia_zweitbesetzung": (5, 3, None, 5, 5, "neu", "Sophias Vergangenheit, leiser Moment"),
    "g1_petru_netze": (5, 3, None, 5, 4, "neu", "stärkster Petru-Moment"),
    "g1_lola_strandkueche": (5, 3, None, 5, 5, "neu", "Lolas Traum angelegt, ohne das Ende vorwegzunehmen"),
    "g1_lola_delfin": (3, 3, 5, 5, 3, "neu", "Gerald"),
    "yk_hana": (4, 2, 4, 5, 4, "neu", "Kette läuft weiter, Yamamotos Tochter"),
    "gv_elsa_roman": (4, 3, 5, 5, 3, "neu", "Elsas Gap Moe"),
    "gv_unit01_bild": (4, 3, 4, 5, 4, "neu", "Ursprung von Leas Zeichnung, speist Peace Cake"),
    "gv_rotes_kleid": (4, 3, 5, 5, 3, "neu", "Festa, Jana kopiert Chiara"),
    "gv_holm_baer": (3, 3, 5, 5, 3, "neu", "Holm-Legende als Wette"),
    "gv_chiara_italienisch": (3, 3, 5, 5, 3, "neu", "Chiaras schlechtes Italienisch"),
    "gv_tuersteher": (3, 3, 5, 5, 2, "neu", "Maxwells Vergangenheit"),
    "gv_kaffee_rosi": (4, 3, 4, 5, 4, "neu", "Siri und Rosi nach dem ersten Tag"),
    "gv_seestueck": (5, 3, None, 5, 5, "neu", "die Schwestern und ihre Mutter"),

    # ---------------------------------------------------------------- Flirt und NSFW (25.10.2026, Anteil frech auf 25 %)
    "fl_lea_neopren": (4, 3, 4, 5, 4, "neu", "Lea, Flirt mit Knistern"),
    "fl_lea_seite41": (5, 3, None, 5, 5, "neu", "Lea zeigt mehr, als sie wollte"),
    "fl_lea_fakt": (4, 3, 4, 5, 4, "neu", "Flirt per Handy, Leas Ton"),
    "fl_lea_salut": (4, 2, 4, 5, 3, "neu", "Leas Tick als Flirt"),
    "fl_rosi_pfand": (5, 4, 4, 5, 4, "neu", "Pfand-Wette, Rosis Leiter"),
    "fl_rosi_bandana": (4, 3, 4, 5, 4, "neu", "Rosi kommt zu nah"),
    "fl_rosi_vespa": (5, 3, None, 5, 5, "neu", "Rosis Vater, erste Fahrt"),
    "fl_rosi_schicksal": (4, 3, 5, 5, 4, "neu", "Anime-Pathos als Beinahe-Kuss"),
    "fl_lola_mehl": (4, 3, 4, 5, 4, "neu", "Lola nachts in der Kombüse"),
    "fl_lola_haengematte": (4, 3, None, 5, 5, "neu", "Lola lädt ein"),
    "fl_lola_bao": (5, 4, 4, 5, 4, "neu", "Kochen als Flirt, Ducs Stärke"),
    "fl_lola_sonnencreme": (3, 3, 4, 4, 3, "neu", "Fanservice mit Lolas Stimme"),
    "fl_siri_blick": (4, 4, None, 5, 4, "neu", "Siri vor der Trennung, nur ein Blick"),
    "fl_siri_date": (5, 3, None, 5, 5, "neu", "Siri fragt selbst"),
    "fl_siri_schulter": (5, 3, None, 4, 5, "neu", "stiller Moment nach der Trennung"),
    "fl_megan_palstek": (5, 4, None, 5, 4, "neu", "versteckte Romanze, Hangar-Knoten"),
    "fl_megan_privat": (4, 3, 4, 5, 4, "neu", "Megans private Nummer"),
    "fl_alva_eis": (4, 3, None, 4, 4, "neu", "Alva an der Bar"),
    "fl_alva_tuer": (4, 3, None, 4, 4, "neu", "Alva lockt"),
    "fl_alva_schritt": (4, 3, None, 5, 4, "neu", "ein Schritt Flamenco"),
    "fl_chiara_zehn": (5, 3, 4, 5, 5, "neu", "Chiaras Skala, die Zehn bleibt aufgespart"),
    "fl_chiara_kragen": (4, 2, 4, 5, 3, "neu", "Chiara richtet den Kragen"),
    "fl_chiara_tee": (4, 3, None, 5, 4, "neu", "zwei Tassen auf der Brücke"),
    "fl_sophia_blick": (5, 3, 4, 5, 4, "neu", "Wette als Flirt"),
    "fl_sophia_ungeprobt": (5, 3, None, 5, 5, "neu", "Sophias Show rutscht"),
    "fl_jana_knoten": (3, 2, 5, 5, 3, "neu", "Jana-Gag mit Knistern"),
    "fl_elsa_strafzettel": (4, 3, 5, 5, 3, "neu", "Elsa flirtet dienstlich"),
    "ab_jana_nacht": (4, 3, None, 5, 4, "neu", "One-Night-Stand aus dem Wiki"),
    "ab_jana_handy": (3, 3, None, 3, 3, "neu", "Wiederholung, bewusst"),
    "ab_megan_nacht": (5, 4, None, 5, 5, "neu", "versteckte Romanze, eine Nacht"),
}

GEW = {"bindung": 0.30, "wirkung": 0.25, "humor": 0.20, "frische": 0.15, "sehnsucht": 0.10}


def punkte(b, w, h, f, s):
    if h is None:
        rest = 1 - GEW["humor"]
        return (b * GEW["bindung"] + w * GEW["wirkung"] + f * GEW["frische"] + s * GEW["sehnsucht"]) / rest
    return b * GEW["bindung"] + w * GEW["wirkung"] + h * GEW["humor"] + f * GEW["frische"] + s * GEW["sehnsucht"]


def main():
    hier = os.path.dirname(os.path.abspath(__file__))
    eden = os.path.dirname(os.path.dirname(hier))
    d = json.load(open(os.path.join(eden, "module", "eden_rise", "ereignisse.json"), encoding="utf-8"))
    titel = {e["id"]: e["titel"] for e in d["events"]}
    ton = {e["id"]: e["ton"] for e in d["events"]}
    fehlt = [e for e in titel if e not in S and not any(k.endswith("*") and e.startswith(k[:-1]) for k in S)]
    zeilen = []
    for k, (b, w, h, f, s, urteil, notiz) in S.items():
        t = titel.get(k) or titel.get(next((e for e in titel if e.startswith(k[:-1])), ""), k)
        zeilen.append((punkte(b, w, h, f, s), k, t, b, w, h, f, s, urteil, notiz))
    zeilen.sort(key=lambda x: -x[0])
    out = ["# Event-Ranking Akt 1", "",
           "Stand 25.10.2026 · Kriterien mit Duc vereinbart: Bindung 30 % · Spielwirkung 25 % · Humor 20 % (nur bei "
           "witzigen Events, sonst anteilig verteilt) · Frische 15 % · Sehnsucht 10 %. Kanon ist Pflicht und wird "
           "repariert, nicht bewertet. Notizen bewusst spoilerarm.", "",
           "Urteil **neu** = am 25.10. aus dem Wiki gebaut, Werte sind eine erste Einschätzung vor dem Spieltest.", "",
           "| # | Event | Titel | Punkte | B | W | H | F | S | Urteil | Notiz |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for n, (p, k, t, b, w, h, f, s, u, notiz) in enumerate(zeilen, 1):
        out.append("| %d | `%s` | %s | **%.2f** | %d | %d | %s | %d | %d | %s | %s |"
                   % (n, k, t, p, b, w, "–" if h is None else h, f, s, u, notiz))
    zaehl = {}
    for z in zeilen:
        zaehl[z[8]] = zaehl.get(z[8], 0) + 1
    out += ["", "**Urteile:** " + " · ".join("%s %d" % (u, n) for u, n in sorted(zaehl.items(), key=lambda x: -x[1]))]
    witzig = [z for z in zeilen if z[5] is not None]
    out += ["", "## Humor", "", "Die zehn stärksten Lacher (Humor-Wert, dann Gesamt):", ""]
    for z in sorted(witzig, key=lambda x: (-x[5], -x[0]))[:10]:
        out.append("- `%s` %s (Humor %d)" % (z[1], z[2], z[5]))
    if fehlt:
        out += ["", "Nicht bewertet: " + ", ".join(fehlt)]
    ziel = os.path.join(eden, "docs", "brain_trust", "EVENT_RANKING.md")
    open(ziel, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("geschrieben:", ziel, len(zeilen), "Einträge; nicht bewertet:", fehlt)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
r"""Ducs Pixabay-SFX-Auswahl (27.10.2026) herunterladen und spielfertig machen.

    python werkzeuge\eden_rise\sfx_pixabay.py

Laedt die gewaehlten Dateien vom Pixabay-CDN (Pixabay Content License) nach docs\abnahme\sfx_pixabay\roh, baut
Kombinationen (z. B. Luefter + Explosion), schneidet lange Einzeltoene mit Ausblende, gleicht die Lautheit an und legt
die Ergebnisse als <id>_<n>.mp3 nach docs\abnahme\sfx_pixabay\fertig - dort hoerbar, bevor sie ins Spiel kommen.
Quellen stehen in fertig\QUELLEN.md. Einzeltoene -18 LUFS, Klick -20, Hintergrund-Schleifen -30 (unter Sprache)."""
import json, os, shutil, subprocess, sys, urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASIS = os.path.join(EDEN, "docs", "abnahme", "sfx_pixabay")
ROH, FERTIG = os.path.join(BASIS, "roh"), os.path.join(BASIS, "fertig")
SFX = os.path.join(EDEN, "module", "eden_rise", "sfx")
CDN = "https://cdn.pixabay.com/audio/"

# Quelle: Kurzname -> (CDN-Pfad nach /audio/, Pixabay-Seite)
Q = {
    "schwung": ("2024/02/06/audio_f018c74fc7.mp3", "film-special-effects-swing-whoosh-weapon-1-189819"),
    "treffer": ("2024/02/20/audio_6d4de9d80e.mp3", "film-special-effects-power-punch-192118"),
    "parade": ("2025/08/23/audio_3bbe5ce786.mp3", "film-special-effects-armor-impact-from-sword-393843"),
    "parade_perfekt": ("2024/09/18/audio_52ea34712d.mp3", "film-special-effects-sword-clash-241729"),
    "ausweichen": ("2023/08/06/audio_766a043a34.mp3", "film-special-effects-whoosh-cinematic-161021"),
    "sieg": ("2026/07/29/audio_6b3b29cb40.mp3", "musical-victory-bell-success-fanfare-576275"),
    "boden": ("2025/05/30/audio_0d4c9a071d.mp3", "film-special-effects-ground-impact-352053"),
    "posaune": ("2026/07/29/audio_70aed19c30.mp3", "musical-sad-trombone-fail-wah-576277"),
    "level": ("2026/07/29/audio_39ac04e5b8.mp3", "musical-triumphant-achievement-bell-hit-576273"),
    "vibration": ("2025/07/09/audio_d92fb979d9.mp3", "film-special-effects-phone-vibrating-372478"),
    "notification": ("2026/09/13/audio_ac8f16f713.mp3", "film-special-effects-notification-message-22-602606"),
    "energie": ("2024/07/30/audio_5c095edf22.mp3", "film-special-effects-cinematic-electricity-explosive-stinger-energy-burst-2-228345"),
    "luefter": ("2024/10/05/audio_95e5e698d2.mp3", "technology-old-fan-with-start-sound-247598"),
    "feuer": ("2025/09/16/audio_5847bf199b.mp3", "film-special-effects-fire-sounds-405444"),
    "alarm": ("2022/03/21/audio_7b23a10981.mp3", "film-special-effects-severe-warning-alarm-98704"),
    "schritte": ("2021/10/06/audio_408a28445f.mp3", "chase-running-9109"),
    "lagerfeuer": ("2024/11/25/audio_42e28dc867.mp3", "nature-campfirefireplace-crackling-268525"),
    "fund": ("2026/05/24/audio_9059ade3f3.mp3", "film-special-effects-item-pickup-3-540193"),
    "uhr": ("2022/03/15/audio_790971df2d.mp3", "film-special-effects-clock-ticking-83775"),
    "notify": ("2022/03/15/audio_943153e3c2.mp3", "film-special-effects-effect-notify-84408"),
    "erfolg": ("2021/08/04/audio_0625c1539c.mp3", "film-special-effects-success-1-6297"),
    "item": ("2022/03/10/audio_49a54d836e.mp3", "film-special-effects-item-pick-up-38258"),
    "deep_hit": ("2023/11/10/audio_db57d3d032.mp3", "film-special-effects-deep-hit-175726"),
    "ratsche": ("2022/03/18/audio_4e7779d130.mp3", "film-special-effects-ratchet-socket-wrench-tool-95253"),
    "accepter": ("2025/08/25/audio_0793fa95ea.mp3", "film-special-effects-accepter-2-394924"),
    "heil6": ("2025/07/22/audio_ef222bf7dd.mp3", "film-special-effects-healing-magic-6-378666"),
    "heil4": ("2025/07/22/audio_cdfce7cdba.mp3", "film-special-effects-healing-magic-4-378668"),
    "wellen": ("2021/08/09/audio_fc1bc78a66.mp3", "nature-waves-6907"),
    "knarzen": ("2022/03/10/audio_e89ecec2cc.mp3", "household-wood-creaking-30692"),
    "strand": ("2025/09/13/audio_1854362bf0.mp3", "nature-beach-02-404144"),
    "wald": ("2022/02/07/audio_06d4a5f29d.mp3", "nature-morning-forest-ambiance-17045"),
    "klopfen": ("2022/03/25/audio_a465b4f9c8.mp3", "household-wood-door-knock-106669"),
    "tada": ("2024/01/02/audio_836d05877e.mp3", "musical-tada-military-2-183973"),
    "trommel": ("2022/03/10/audio_9255759fab.mp3", "musical-failure-drum-sound-effect-1-46093"),
    "piano_hit": ("2026/07/14/audio_8f98537420.mp3", "musical-cinematic-piano-hit-567216"),
    "riser": ("2024/09/20/audio_3912589570.mp3", "film-special-effects-cinematic-riser-impact-242635"),
    "moewen": ("2022/03/10/audio_0056b838a6.mp3", "nature-urban-seagulls-30068"),
    "bar": ("2021/08/04/audio_415d5e6d6e.mp3", "people-talking-people-6368"),
    "seite": ("2025/05/05/audio_ca4220361e.mp3", "film-special-effects-turn-a-page-336933"),
    "voegel": ("2022/03/15/audio_442b144fc5.mp3", "nature-birds-chirping-75156"),
    "rhodes_tape": ("2026/07/29/audio_b32c23c169.mp3", "musical-warm-rhodes-lofi-tape-stop-576271"),
    "rhodes_chord": ("2026/07/29/audio_3d97ca84bb.mp3", "musical-nostalgic-rhodes-chill-chord-576270"),
    "glimmer": ("2026/07/29/audio_4c737e8fea.mp3", "musical-twinkling-glimmer-sparkle-pop-576278"),
    # Donner fuer den Sturm (Duc 27.10.2026, Abnahme docs/abnahme/donner: Nr. 1 und 2)
    "donner1": ("2024/02/20/audio_8667d9c4b2.mp3", "nature-loud-thunder-192165"),
    "donner2": ("2022/10/30/audio_65a2d39d7c.mp3", "nature-thunder-strike-124463"),
    # Granaten (Duc 28.10.2026, Abnahme docs/abnahme/granaten_klang: je ein Favorit)
    "gr_feuer": ("2021/08/04/audio_187390c215.mp3", "film-special-effects-hq-explosion-6288"),
    "gr_wasser": ("2025/08/07/audio_3e49146fc1.mp3", "film-special-effects-underwater-explosion-386175"),
    "gr_schock": ("2024/07/30/audio_f717577007.mp3", "film-special-effects-cinematic-electricity-explosive-stinger-energy-burst-1-228344"),
    "gr_flash": ("2026/05/30/audio_89f760f671.mp3", "film-special-effects-stun-grenade-flashbang-543949"),
    "gr_pfeifen": ("2022/03/15/audio_e66e87b927.mp3", "film-special-effects-high-pitched-ringing-88473"),
    "gr_erschuetterung": ("2021/08/04/audio_4a73b07cbb.mp3", "film-special-effects-explosion-5981"),
    "gr_knall": ("2022/03/10/audio_ca2325b43c.mp3", "film-special-effects-grenade-37637"),
    "gr_splitter": ("2024/12/19/audio_245757a313.mp3", "film-special-effects-debris-on-metal-hq-275769"),
    # Vorhoer-Abnahme 29.10.2026 (docs/abnahme/vorhoeren_auswahl_20261029.md): Duc nannte diese Seiten
    "heli_hover": ("2026/09/05/audio_ffba3ea0f9.mp3", "film-special-effects-helicopter-hovering-598081"),
    "angel_rute": ("2025/09/28/audio_7eb51a95b9.mp3", "film-special-effects-fishing-rod-whoosh-411640"),
    "angel_eimer": ("2023/03/11/audio_c178823ea4.mp3", "film-special-effects-your-plastic-bucket-is-full-of-water-142159"),
    "angel_seil": ("2024/04/02/audio_3c7113f22e.mp3", "film-special-effects-rope-tighten-knot-3-199789"),
    "angel_snap": ("2022/03/19/audio_d81b9947f3.mp3", "film-special-effects-snap-96332"),
    "abbau_axt": ("2025/12/11/audio_e30ae3bd4a.mp3", "giant-axe-strike-hitting-solid-wood-3-450247"),
    "abbau_baum": ("2025/11/04/audio_0dca7da2f3.mp3", "nature-falling-tree-ai-generated-431321"),
    "abbau_hacke": ("2024/11/19/audio_98ba777c64.mp3", "film-special-effects-hit-rock-02-266304"),
    "abbau_bruch": ("2024/03/05/audio_b858bdb82f.mp3", "film-special-effects-small-rock-break-194553"),
    "abbau_daneben": ("2024/11/19/audio_344dc5d699.mp3", "film-special-effects-hit-rock-01-266301"),
    # Ratten-Rudel: Duc "suche etwas bei Pixabay" - vier Kandidaten zur Wahl
    "ratten_rats": ("2022/03/15/audio_6ab47c1eee.mp3", "nature-rats-90692"),
    "ratten_ratty": ("2022/03/15/audio_f0c3b3be74.mp3", "film-special-effects-ratty-squeaks-74824"),
    "ratten_hd": ("2026/07/19/audio_a3c9bcd3f4.mp3", "film-special-effects-rat-squeaking-sound-effecthd-570216"),
    "ratten_trippeln": ("2022/03/24/audio_f41edc72a5.mp3", "film-special-effects-small-animal-scurrying-through-leaves-100670"),
    # Grotten-Mission (Duc 29.10.2026: "fehlen SFX?"): je vier Kandidaten fuer die drei Hintergrund-Schleifen
    "grotte_tropfen": ("2026/10/22/audio_0446248e84.mp3", "film-special-effects-cave-water-dripping-625149"),
    "grotte_droplets": ("2026/02/10/audio_a02ffddc37.mp3", "nature-droplets-in-a-cave-482871"),
    "grotte_stalaktit": ("2024/11/09/audio_9381dac23b.mp3", "nature-sound-of-dripping-water-from-stalactites-in-a-cave-hd-262342"),
    "grotte_echo": ("2024/08/08/audio_977e17b6ae.mp3", "film-special-effects-waterdrops-cave-echo-sounds-230896"),
    "flut_seacave": ("2022/03/12/audio_7ecd447213.mp3", "film-special-effects-sea-cave-51806"),
    "flut_seacave2": ("2022/03/13/audio_d4f0d90a9d.mp3", "film-special-effects-sea-cave-2-53782"),
    "flut_wasser": ("2025/05/17/audio_d89146f264.mp3", "nature-water-in-cave-hq-343057"),
    "flut_hoehle": ("2025/09/10/audio_1ee37fe900.mp3", "nature-cave-with-water-dripping-402696"),
    "dach_wind": ("2025/12/12/audio_bac2e25736.mp3", "city-house-terrace-wind-ambience-soundque-field-recording-445579"),
    "dach_tauben": ("2024/05/01/audio_cc919293c4.mp3", "nature-pigeons-doves-atmosphere-sound-effect-205750"),
    "dach_taube2": ("2025/09/14/audio_2fb131a530.mp3", "nature-pigeon-ambience-404244"),
    "dach_dorf": ("2022/02/07/audio_2d042007e5.mp3", "city-morning-village-ambience-16903"),
    # Handy aus einem Guss (Duc 03.11.2026, Abnahme docs/abnahme/handy_klang.json), fast alles von Universfield
    "hy_empfang": ("2026/03/01/audio_4182fd0ce7.mp3", "technology-new-notification-040-493469"),
    "hy_herz": ("2025/05/29/audio_8d79877e56.mp3", "film-special-effects-positive-notification-351299"),
    "hy_marimba": ("2026/02/20/audio_8fe2df5ef7.mp3", "musical-marimba-ringtone-487903"),
    "hy_verbinden": ("2024/05/19/audio_48ac856676.mp3", "film-special-effects-new-notification-07-210334"),
    "hy_ende": ("2025/03/22/audio_e9436dc119.mp3", "film-special-effects-end-call-sfx-317327"),
    "hy_verpasst": ("2024/08/02/audio_3a4d7c617d.mp3", "film-special-effects-notification-beep-229154"),
    # Kampf lesen (Duc 03.11.2026, Auswahl der Review-Sitzung, Runden 1-4, X:/AI/Eden_Review/ux_benchmark/sounds*.html)
    "gong": ("2024/02/13/audio_4d8b9ef2f4.mp3", "film-special-effects-celestial-gong-191122"),
    "klirren_2": ("2025/08/23/audio_8d367ce755.mp3", "film-special-effects-sword-clashhit-393837"),
    "klirren_3": ("2024/10/27/audio_c331d77d7e.mp3", "film-special-effects-sword-deflection-the-ballad-of-the-blades-255962"),
    "finte_whoosh": ("2022/08/24/audio_9377ecf42b.mp3", "film-special-effects-slow-whoosh-118247"),
    "finte_swoosh": ("2026/07/14/audio_860fc06b4e.mp3", "film-special-effects-slow-swoosh-567191"),
    "konter_kette": ("2024/01/11/audio_f5a8065509.mp3", "film-special-effects-sword-slash-and-swing-185432"),
    "harfe": ("2026/06/04/audio_b49cc002a1.mp3", "technology-cheerful-traditional-harp-positive-ui-alert-540977"),
    "leier": ("2025/11/03/audio_b0aee4e859.mp3", "musical-ancient-lyre-sound-short-arpeggio-sound-effect-430628"),
}

# Ziel-SFX: id -> Liste von Varianten; jede Variante = (Art, Teile, max. Sekunden)
#   "einzeln": ein Ton · "folge": Teile hintereinander · "loop": Hintergrund-Schleife (leise)
#   "nacht": Strand-Basis + ab und an leises Knarzen · "hafen": Moewen + Wellen im Hintergrund
ZIELE = {
    "kampf_schwung": [("einzeln", ["schwung"], 2)],
    "kampf_treffer": [("einzeln", ["treffer"], 2)],
    "kampf_parade": [("einzeln", ["parade"], 2)],
    "kampf_parade_perfekt": [("einzeln", ["parade_perfekt"], 2)],
    "kampf_ausweichen": [("einzeln", ["ausweichen"], 2.5)],
    "kampf_sieg": [("einzeln", ["sieg"], 6)],
    "kampf_niederlage": [("folge", ["boden", "posaune"], 7)],
    "level_up": [("einzeln", ["level"], 5)],
    "anruf_klingeln": [("einzeln", ["hy_marimba"], 4)],   # vorher Vibration; Duc 03.11.2026: Marimba, auf 4 s
    "handy_empfang": [("ui", ["hy_empfang"], 1.2)],        # ihre Blase im offenen Chat, leise
    "handy_herz": [("ui", ["hy_herz"], 1.2)],
    "anruf_verbinden": [("ui", ["hy_verbinden"], 1.8)],
    "anruf_ende": [("einzeln", ["hy_ende"], 2)],           # Duc: auf 2 s
    "anruf_verpasst": [("einzeln", ["hy_verpasst"], 2.1)],
    "notification": [("einzeln", ["notification"], 2)],
    "explosion": [("folge", ["luefter", "energie"], 9)],
    "feuer_loop": [("loop", ["feuer"], 0)],
    "alarm": [("einzeln", ["alarm"], 6)],
    "schritte_kies": [("einzeln", ["schritte"], 5)],
    "rast_feuer": [("loop", ["lagerfeuer"], 0)],
    "fund": [("einzeln", ["fund"], 2)],
    "spur_uhr": [("einzeln", ["uhr"], 4)],
    "auftrag_feder": [("einzeln", ["notify"], 2)],
    "auftrag_siegel": [("einzeln", ["erfolg"], 3)],
    "neue_waffe": [("einzeln", ["item"], 3)],
    "chip_einrasten": [("einzeln", ["deep_hit"], 2.5)],
    "werkstatt_fertig": [("folge", ["ratsche", "accepter"], 4)],
    "heilung": [("einzeln", ["heil6"], 4)],
    "status": [("einzeln", ["heil4"], 2.5)],
    "amb_deck": [("loop", ["wellen"], 0)],
    "amb_nacht": [("nacht", ["strand", "knarzen"], 0)],
    "amb_macchia": [("loop", ["wald"], 0)],
    "bordrat": [("einzeln", ["klopfen"], 3)],
    "versprechen": [("einzeln", ["tada"], 3)],
    "versprechen_gebrochen": [("einzeln", ["trommel"], 3)],
    "anhoerung_hammer": [("einzeln", ["piano_hit"], 4)],
    "skill_gemeistert": [("einzeln", ["piano_hit"], 4)],                 # Level-up: Pfad gemeistert (Duc 28.10.: derselbe Piano-Hit)
    "anhoerung_einspruch": [("einzeln", ["riser"], 4)],
    "amb_hafen": [("hafen", ["moewen", "wellen"], 0)],
    "amb_bar": [("loop", ["bar"], 0)],
    "menue_tab": [("einzeln", ["seite"], 1.5)],
    "ruhig_voegel": [("loop", ["voegel"], 0)],
    "tag_ende": [("einzeln", ["rhodes_tape"], 13), ("einzeln", ["rhodes_chord"], 11), ("einzeln", ["glimmer"], 6)],
    "donner": [("einzeln", ["donner1"], 5), ("einzeln", ["donner2"], 7)],
    "kampf_granate_feuer": [("knall", ["gr_feuer"], 3)],
    "kampf_granate_wasser": [("knall", ["gr_wasser"], 3)],
    "kampf_granate_schock": [("knall", ["gr_schock"], 3)],
    "kampf_granate_flash": [("knall", ["gr_flash"], 3.5)],
    "kampf_granate_pfeifen": [("pfeifen", ["gr_pfeifen"], 1)],          # Duc 28.10.: nur 1 s piepen (vorher 4, dann 2)
    "kampf_granate_erschuetterung": [("knall", ["gr_erschuetterung"], 3)],
    "kampf_granate_splitter": [("schicht", ["gr_knall", "gr_splitter"], 3.5)],   # Duc: vorher ein Explosionsknall
    # Vorhoer-Abnahme 29.10.2026: Pixabay statt ElevenLabs. Die Datei liegt als naechste Variante neben den
    # ElevenLabs-Varianten (NUMMER_AB), der Katalog waehlt sie (sfx_eden_rise.py, PIXABAY_29_10).
    "hubschrauber_start": [("einzeln", ["heli_hover"], 8)],
    "angeln_wurf": [("knall", ["angel_rute"], 2)],
    "angeln_fehl": [("einzeln", ["angel_eimer"], 3)],
    "angeln_riss": [("folge", ["angel_seil", "angel_snap"], 3)],     # Duc: erst das Seil, danach der Riss
    "abbau_axt": [("knall", ["abbau_axt"], 2)],
    "abbau_baum_faellt": [("einzeln", ["abbau_baum"], 6)],
    "abbau_hacke": [("knall", ["abbau_hacke"], 1.5)],
    "abbau_stein_bricht": [("knall", ["abbau_bruch"], 3)],
    "abbau_daneben": [("knall", ["abbau_daneben"], 1.5)],
    "rudel_ratten": [("einzeln", ["ratten_rats"], 4), ("einzeln", ["ratten_ratty"], 4),
                     ("einzeln", ["ratten_hd"], 4), ("einzeln", ["ratten_trippeln"], 4)],
    # Grotten-Mission (29.10.2026): Hintergrund-Schleifen, je vier Kandidaten zur Wahl (kern/sfx.py ambience)
    "amb_grotte": [("loop", [t], 0) for t in ("grotte_tropfen", "grotte_droplets", "grotte_stalaktit", "grotte_echo")],
    "amb_grotte_flut": [("loop", [t], 0) for t in ("flut_seacave", "flut_seacave2", "flut_wasser", "flut_hoehle")],
    "amb_daecher": [("loop", [t], 0) for t in ("dach_wind", "dach_tauben", "dach_taube2", "dach_dorf")],
    # Kampf lesen (Duc 03.11.2026): Warnung vor der Taeuschung (nur der erste Gong-Schlag), Kettenklaenge 2 und 3,
    # Finte reihum, Konter nach voller Kette; W20-Erfolg/-Fehlschlag ueberall (Harfe/Leier, Leier auf 1,5 s mit Ausblende)
    "kampf_warnung": [("einzeln", ["gong"], 1.3)],
    "kampf_kette_2": [("einzeln", ["klirren_2"], 1.2)],
    "kampf_kette_3": [("einzeln", ["klirren_3"], 1.4)],
    "kampf_finte": [("einzeln", ["finte_whoosh"], 1.2), ("einzeln", ["finte_swoosh"], 1.2)],
    "kampf_konter_kette": [("einzeln", ["konter_kette"], 1.5)],
    "wuerfel_erfolg": [("einzeln", ["harfe"], 2.0)],
    "wuerfel_fehlschlag": [("einzeln", ["leier"], 1.5)],
}
# Erste Variantennummer je Ziel (Standard 1): neben vorhandene ElevenLabs-Varianten legen, nichts ueberschreiben
NUMMER_AB = {"hubschrauber_start": 5, "angeln_wurf": 5, "angeln_fehl": 5, "angeln_riss": 5, "abbau_axt": 4,
             "abbau_baum_faellt": 3, "abbau_hacke": 4, "abbau_stein_bricht": 3, "abbau_daneben": 3, "rudel_ratten": 5,
             "wuerfel_erfolg": 5, "wuerfel_fehlschlag": 5}
LUFS = {"loop": -30, "nacht": -30, "hafen": -30, "pfeifen": -27, "ui": -22}   # ui: leise Handy-Toene, wie ein Einzelton


def ff(*a):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *a], check=True)


def laden(nur=None):
    os.makedirs(ROH, exist_ok=True)
    for k, (pfad, _) in Q.items():
        if nur is not None and k not in nur:
            continue
        ziel = os.path.join(ROH, k + ".mp3")
        if not os.path.exists(ziel):
            req = urllib.request.Request(CDN + pfad, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://pixabay.com/"})
            with urllib.request.urlopen(req, timeout=60) as r:
                open(ziel, "wb").write(r.read())


def norm(ein, aus, lufs, tp=-1.5):
    ff("-i", ein, "-af", "loudnorm=I=%s:TP=%s:LRA=11" % (lufs, tp), "-ar", "44100", "-ac", "2", "-b:a", "160k", aus)


def bauen(sid, n, art, teile, sek):
    roh = [os.path.join(ROH, t + ".mp3") for t in teile]
    tmp = os.path.join(FERTIG, "_tmp_%s.wav" % sid)
    aus = os.path.join(FERTIG, "%s_%d.mp3" % (sid, n))
    if art in ("einzeln", "ui"):
        ff("-i", roh[0], "-af", "atrim=0:%s,afade=t=out:st=%s:d=0.4" % (sek, max(0, sek - 0.4)), tmp)
    elif art == "folge":
        ff("-i", roh[0], "-i", roh[1], "-filter_complex",
           "[0:a][1:a]acrossfade=d=0.15:c1=tri:c2=tri,atrim=0:%s,afade=t=out:st=%s:d=0.5[o]" % (sek, sek - 0.5),
           "-map", "[o]", tmp)
    elif art == "loop":
        ff("-i", roh[0], "-af", "afade=t=in:d=1", tmp)
    elif art == "nacht":                                # Strand als Basis, Knarzen nur dreimal kurz und leise
        ff("-i", roh[0], "-i", roh[1], "-filter_complex",
           "[1:a]volume=0.25,asplit=3[k1][k2][k3];"
           "[k1]atrim=4:7,asetpts=PTS-STARTPTS,afade=t=in:d=0.5,afade=t=out:st=2.4:d=0.6,adelay=25000|25000[a];"
           "[k2]atrim=21:23.5,asetpts=PTS-STARTPTS,afade=t=in:d=0.5,afade=t=out:st=1.9:d=0.6,adelay=78000|78000[b];"
           "[k3]atrim=40:43,asetpts=PTS-STARTPTS,afade=t=in:d=0.5,afade=t=out:st=2.4:d=0.6,adelay=126000|126000[c];"
           "[0:a][a][b][c]amix=inputs=4:duration=first:normalize=0[o]", "-map", "[o]", tmp)
    elif art == "hafen":                                # Moewen vorn, Wellen leise dahinter
        ff("-i", roh[0], "-i", roh[1], "-filter_complex",
           "[1:a]volume=0.35[w];[0:a][w]amix=inputs=2:duration=first:normalize=0[o]", "-map", "[o]", tmp)
    elif art == "knall":                                # Einschlag: Stille vorn weg, damit der Knall genau mit dem Bild kommt
        ff("-i", roh[0], "-af", "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0,"
           "atrim=0:%s,afade=t=out:st=%s:d=0.5" % (sek, sek - 0.5), tmp)
    elif art == "pfeifen":                              # Ohrenpfeifen leise unter der Weissblende: weich rein, lang raus
        ff("-i", roh[0], "-af", "atrim=0:%s,afade=t=in:d=0.3,afade=t=out:st=%s:d=%s" % (sek, sek - min(1.8, sek / 2), min(1.8, sek / 2)), tmp)
    elif art == "schicht":                              # Knall vorn, zweiter Teil 0,25 s spaeter darueber
        ff("-i", roh[0], "-i", roh[1], "-filter_complex",
           "[0:a]silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0[a];"
           "[1:a]adelay=250|250[b];[a][b]amix=inputs=2:duration=longest:normalize=0,"
           "atrim=0:%s,afade=t=out:st=%s:d=0.6[o]" % (sek, sek - 0.6), "-map", "[o]", tmp)
    norm(tmp, aus, LUFS.get(art, -18))
    os.remove(tmp)
    return aus


def klick():
    """Jetziger Klick (gewaehlte Varianten) ohne Vorlauf: Stille am Anfang weg."""
    d = json.load(open(os.path.join(EDEN, "module", "eden_rise", "sfx.json"), encoding="utf-8"))
    s = next(x for x in d["sfx"] if x["id"] == "ui_klick")
    w = s.get("wahl")
    nummern = w if isinstance(w, list) else [w] if w else range(1, s["varianten"] + 1)
    for n in nummern:
        ein = os.path.join(SFX, "ui_klick_%d.mp3" % n)
        if os.path.exists(ein):
            ff("-i", ein, "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0", "-b:a", "160k",
               os.path.join(FERTIG, "ui_klick_%d.mp3" % n))
    return list(nummern)


def nur_diese(ids):
    """--nur a,b (03.11.2026): nur diese SFX laden, bauen und direkt nach module\\eden_rise\\sfx legen; der Rest bleibt."""
    unbekannt = [i for i in ids if i not in ZIELE]
    if unbekannt:
        raise SystemExit("unbekannt: %s" % unbekannt)
    laden({t for i in ids for _, ts, _ in ZIELE[i] for t in ts})
    os.makedirs(FERTIG, exist_ok=True)
    for sid in ids:
        for n, (art, teile, sek) in enumerate(ZIELE[sid], NUMMER_AB.get(sid, 1)):
            aus = bauen(sid, n, art, teile, sek)
            shutil.copy(aus, os.path.join(SFX, os.path.basename(aus)))
            print(os.path.basename(aus), "->", SFX)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--nur" in sys.argv:
        return nur_diese(sys.argv[sys.argv.index("--nur") + 1].split(","))
    laden()
    if os.path.isdir(FERTIG):
        shutil.rmtree(FERTIG)
    os.makedirs(FERTIG)
    for sid, varianten in ZIELE.items():
        for n, (art, teile, sek) in enumerate(varianten, NUMMER_AB.get(sid, 1)):
            bauen(sid, n, art, teile, sek)
    k = klick()
    with open(os.path.join(FERTIG, "QUELLEN.md"), "w", encoding="utf-8") as f:
        f.write("# SFX-Quellen (Pixabay Content License)\n\n| SFX | Quelle(n) |\n|---|---|\n")
        for sid, varianten in ZIELE.items():
            teile = sorted({t for _, ts, _ in varianten for t in ts})
            f.write("| %s | %s |\n" % (sid, ", ".join("https://pixabay.com/sound-effects/%s/" % Q[t][1] for t in teile)))
    print("fertig: %d SFX, Klick-Varianten %s -> %s" % (len(ZIELE), k, FERTIG))


if __name__ == "__main__":
    main()

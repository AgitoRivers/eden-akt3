# -*- coding: utf-8 -*-
r"""Baut module\eden_rise\modul.json - die neue Hauptstory "Eden Rise - Gestrandet" (Phase B1, 17.10.2026).

Grundlage ist basis_eden_rise.py (frueher das Modul Gestrandet: Raeume, Kabine, Gesten, Laden-Grundgeruest, Personen mit ST-Sets); hier
kommt nur dazu bzw. wird ersetzt, was die neue Story braucht:
- 7 Tage (Party = Tag 1, Morgen danach mit Holms Abflug = Tag 2, dann fuenf Krisentage) - Ablauf steht in
  story.json (wochenbogen), den Tagesplan baut kern\hauptstory.py daraus, kein Szenen-Vorrat (szenen.json).
- Der Fall wird beim Start gezogen: wahrheit.vorrat hat fuenf neutrale Eintraege fall_1..fall_5 (Fall 6 am 27.10.2026 gestrichen) (nie Inhalt hier).
- Neue Personen: Lola Brennan (Koechin, an Bord), Megan McAllister (Fleet Director, Telefon + einmal an Bord),
  Holm mit eigenen ST-Sets. Alle sind von Anfang an bekannt bis auf das Dorf.
- Persona: kommt aus basis_eden_rise.PERSONA_BERATER (ESG-Berater, Ducs Vorgabe: nie "Tueftler"); fehlt sie
  dort noch, gilt der hier hinterlegte Stand derselben Vorgabe.
Nicht in B1 (folgt in B3-B5 bzw. nach dem Fork): Fakten-Codex, Ermittlung, Gegenhandlungen, Event-Bildschirme,
Laeden/Essen aus eden_rise\gegenstaende.json + laeden.json, Vertrauen fuer alle Nebenfiguren.

    python modul_eden_rise.py      schreibt module\eden_rise\modul.json
"""
import copy, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import basis_eden_rise as G     # noqa: E402  (Grundgeruest: Welt, Raeume, Personen - schreibt nichts)

EDEN = os.path.dirname(os.path.dirname(HIER))    # werkzeuge\eden_rise -> Eden
ZIEL = os.path.join(EDEN, "module", "eden_rise", "modul.json")
FRAUEN = ["chiara", "sophia", "lea", "rosi", "siri"]
SCHIFF = ["crew_mess", "crew_corridor", "galley", "duc_cabin", "vip_cabin", "main_salon", "bridge", "aft_deck",
          "sun_deck", "solar_deck", "foredeck", "swim_platform", "tender_garage", "power_room", "generator_room",
          "workshop"]

MODUL = copy.deepcopy(G.MODUL)
MODUL.update({
    "_hinweis": "Neue Hauptstory Eden Rise (Phase B, 17.10.2026). Gebaut aus werkzeuge\\eden_rise\\modul_eden_rise.py auf Basis "
                "von basis_eden_rise.py - dort aendern, nicht hier. Ablauf: story.json + kern\\hauptstory.py.",
    "id": "eden_rise",
    "titel": "Eden Rise – Stranded",
    "untertitel": "The last charter night. Then the days that change everything.",
    "hauptstory": "story.json",
    # Modell B (24.10.2026): "tag" = Mittag, dazu der Nachmittag - mehr freie Zeit in Akt 1
    "sperre": {"tag": 21, "phase": "nachmittag", "praefix": "bl_", "bis": 23},   # Ab dem Angriff nur noch Szenen der Belagerung
    "zeitraster": {"tage": 23, "phasen": ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"],
                   # Die Hauptstory legt je Phase fest, was gespielt wird; freie Phasen sind eine Wahl
                   "pflicht": ["fruehstueck", "nacht"], "wahl": ["tag", "nachmittag", "dinner", "abend"]},
    "start_flags": [],
    "start_inventar": [],
    "ziel": "In seven days Megan holds a hearing on board: find out who caused the failure.",
    "ziel_kurz": "Megan's hearing",                  # Countdown oben (Akt 1, 24.10.2026)
    "ziel_en": "Megan's hearing on board",    # fuer den Bordstatus der Figuren (kern/szene.py)
    "ziel_einsatz_en": "Without a culprit at the hearing, Megan fires the whole crew",
    "storylets": {},          # die alten Boegen von Gestrandet gelten hier nicht
    "ereignisse": {},         # Events kommen aus eden_rise\ereignisse.json (B5)
    "fixpunkte": [],
})
MODUL.pop("arc", None)
MODUL.pop("enden", None)

MODUL["welt"] = (
    "M/Y Eden Rise, a 62-metre solar-powered superyacht owned by the Eden Group: a hardtop of solar panels, battery "
    "banks, a silent electric drive, and one diesel emergency generator the ETO calls Unit-01. The charter season is "
    "over; the last guests are influencer Siri Lindvik and her boyfriend Yasin Benali. After a farewell party the "
    "yacht was to sail overnight into the bay of Cala d'Orsu for a sunrise photo stop - Megan's \"Eden Bay "
    "Weekend\" - and then on to the shipyard in Calvi for the winter. In the early morning after the party the electric "
    "drive failed. She drifted into the bay of Cala d'Orsu, a fishing village of three hundred people on the west coast "
    "of Corsica, and lies at anchor out in the bay - the fishing harbour is far too shallow for her, so there is no "
    "shore power and no fuel dock; the shore is a tender ride away. The hotel side runs on the batteries in island "
    "mode: anchor light and alarm, bilge pumps, the cold rooms, the watermaker, the toilets; the emergency radio has its "
    "own supply. Captain Marit Holm was flown out with appendicitis the morning after; Duc, the First Officer, has "
    "command. Megan McAllister, Fleet Director of the Eden Group, has given them seven days: then she holds a hearing on "
    "board and judges who caused the failure - without a culprit she fires the whole crew. Nobody aboard knows yet "
    "what caused the failure.")

MODUL["ziele"] = [      # Countdown je Akt in der Kopfzeile (28.10.2026): erstes Ziel mit bis_tag >= heute
    {"bis_tag": 7, "kurz": "Megan's hearing",
     "text": "On day 7 Megan holds a hearing on board. Find out who caused the failure - without a culprit she "
             "fires the whole crew."},
    {"bis_tag": 14, "kurz": "End of week two",
     "text": "The second week in the bay. Keep the crew together - the island has more to show you."},
]

MODUL["prolog"] = [
    "The last charter of the season is over. Tonight the Eden Rise sails for the bay of Cala d'Orsu - the Eden "
    "Bay Weekend, a sunrise for the cameras. Then the shipyard in Calvi, and the winter.",
    "Tonight there is one more party on the aft deck: the crew, the last two guests, a captain who pretends her "
    "stomach is fine, and a cook who swears the sea will glow tonight.",
    "You are the new First Officer, one day aboard. Nobody expects anything of you tonight.",
    "Enjoy the light.",
]

# ------------------------------------------------------------------ Spielfigur (Vorgabe Duc, 17.10.2026)
PERSONA_STAND = {
    "id": "berater", "rolle": "first_officer",
    "titel": "The ESG consultant on sabbatical",
    "oeffentlich": "the new First Officer, aboard since Antibes",
    "vorgeschichte": "A sustainability consultant from Frankfurt on a sabbatical: one season at sea as First Officer, "
                     "Yachtmaster for years. Years of client meetings taught him to win a room; he is good with his "
                     "hands and a serious cook, European and Southeast Asian. He thinks in plans, plan B and plan C.",
    "geheimnis": "A management position at European level is waiting for his answer by the end of this week. It means "
                 "pressure, an office, no sea. Everyone aboard thinks he is staying at sea.",
    "attribute": {"charm": 3, "empathy": 2, "perception": 3, "cunning": 2, "courage": 2, "strength": 2},
    "vorteile": ["handwerk", "kueche", "koepfchen", "charme"],
    "vorteil": "Craft and cooking: advantage on repairs and in the galley.",
    "schwaeche": "Plans for everything: when something goes off-plan he wants to solve it alone.",
    "start_items": [],
}
persona = copy.deepcopy(getattr(G, "PERSONA_BERATER", None) or PERSONA_STAND)
persona["start_items"] = []                    # Holms Kompass gibt es erst beim Abschied (Tag 2)
MODUL["personas"] = [persona]

# ------------------------------------------------------------------ Fall-Ziehung (neutral, intern als Zahl)
MODUL["wahrheit"] = {"fest": None, "vorrat": {"fall_%d" % n: {"nr": n, "enthuellung_ab_tag": 4} for n in range(1, 6)},
                     "_hinweis": "Inhalt der Faelle nur in story.json (vertraulich). Hier nur die Ziehung."}

# ------------------------------------------------------------------ Raeume (neue Hintergruende 17./18.10.2026)
RA = MODUL["raeume"]
for _r, _nacht in {"galley": "yacht_galley_night.png", "crew_mess": "yacht_crew_mess_night.png",
                   "main_salon": "yacht_main_salon_night.png", "aft_deck": "yacht_aft_deck_night.png",
                   "swim_platform": "yacht_swim_platform_night.png"}.items():
    RA[_r]["bild"]["nacht"] = _nacht
# Alvas Bar frontal (Alva steht links vor dem Tresen): Tag hell, Abend/Nacht die Nachtfassung
RA["alvas_bar"]["bild"] = {"tag": "corsican_village_bar_day.png", "abend": "corsican_village_bar.png",
                           "nacht": "corsican_village_bar.png"}
RA["alvas_terrace"] = G.R("Alva's terrace on the harbour (long table, ashore)", "corsican_village_long_table.png",
                          privat=2)
# Akt 1 (24.10.2026): die Yacht kommt nicht nach Calvi - Zugang erst, wenn ein spaeteres Ende ihn braucht
RA["calvi_harbour"] = G.R("Harbour of Calvi (shipyard quay)", "calvi_harbour.png", privat=1, zugang=[{"tag_ab": 22}])
# Tag 0 (24.10.2026): Hintergrund der Begegnungen im Hangar von Antibes - nie begehbar
RA["hangar_antibes"] = G.R("Shipyard hangar, Antibes", "eden_rise_hangar_antibes.png", privat=1, zugang=[{"tag_ab": 99}])
RA["alvas_terrace"]["bereich"] = RA["calvi_harbour"]["bereich"] = RA["hangar_antibes"]["bereich"] = "land"
# Rosi's workshop burned in the explosion (E-049); it reopens with the event rosi_werkstatt_offen on day 8 (E-065).
RA["workshop"]["zugang"] = [{"flag": "werkstatt_offen", "vertrauen": ["rosi", 1]},
                            {"flag": "werkstatt_offen", "begleitung": "rosi"}]
RA["workshop"]["bild"] = {"tag": "eden_rise_workshop.png"}     # die wiederaufgebaute Werkstatt (Duc 25.10., Variante 3)
# Ligeias Teich unter der Strand-Grotte (Duc 29.10.2026): offen nach der Flut-Nacht; sie ist nur nachts da (ablauf)
RA["siren_pool"] = G.R("The pool under the beach grotto (high tide)", "eden_rise_siren_pool.png", privat=3,
                       zugang=[{"flag": "sirene_fertig"}])
RA["siren_pool"]["bereich"] = "land"

# ------------------------------------------------------------------ Personen
P = MODUL["personen"]
P["holm"].update({
    "st_ordner": "Marit Holm", "stimme": "Warrior Woman", "set_standard": "Bridge",
    # Duc 02.11.2026: Bridge bis zum Abtransport, holm_shirt (Bluse, Look M) ab der Rueckkehr, holm_bikini nur ueber Events
    "set_frei": [{"flag": "holm_zurueck", "set": "holm_shirt"}],
    "beschreibung": "the captain, 56, Norwegian, thirty years at sea, dry, fair, impossible to fool; she has had "
                    "stomach pains all day and waves them away; she does not yet take her new First Officer quite "
                    "seriously",
    "ablauf": {"*": "bridge"}, "von_bord_ab_tag": 3, "weg_flag": "holm_evakuiert"})   # Tag 2 bis zum Abflug
# Madame Casanova (18.10.2026): Flamenco-Kleid bei Festa und Feierlichkeiten (Piazza); das Set heisst im ST-Ordner
# "alva_flamenco_rojo". Fuer ihren Flamenco-Abend gibt ihr die Intim-Szene eine eigene Grenze (eden.event_szene).
P["casanova"].update({"set_standard": "casanova_standard",
                      "set_regeln": [{"ort": "village_piazza", "set": "alva_flamenco_rojo"}]})
# 24.10.2026 (Duc): Alva's ST folder now has alva_standard, alva_flamenco_noche (set2), alva_festa (set3, public
# flamenco stage dress), alva_morgen (set4, silk kimono) and alva_bikini (set5). Festa on the piazza, nights in black;
# kimono and bikini are for events (morning after, beach).
P["alva"].update({"set_standard": "alva_standard", "ablauf": {"*": "alvas_bar", "dinner": "alvas_terrace"},
                  "set_regeln": [{"ort": "village_piazza", "set": "alva_festa"},
                                 {"phase": "nacht", "set": "alva_flamenco_noche"},
                                 # Outfits (Duc 29.10.2026): Kimono zum Fruehstueck in der Bar, Bikini am Wasser
                                 {"phase": "fruehstueck", "set": "alva_morgen"},
                                 {"ort": "swim_platform", "set": "alva_bikini"}]})
P["lola"] = {
    "name": "Lola Brennan", "kurz": "Lola", "romanzierbar": False, "st_ordner": "Lola Brennan", "stimme": "Lola Brennan",
    # 23.10.2026 (Duc): new sets lola_bikini ("Aloha", by the water + Festa) and lola_denim ("Shore Leave", ashore).
    # First matching rule wins: Festa first, then evening/night Off Duty, then the places by day.
    "set_standard": "Galley", "set_regeln": [{"ort": "village_piazza", "set": "lola_bikini"},
                                             {"phase": "abend", "set": "Off Duty"}, {"phase": "nacht", "set": "Off Duty"},
                                             {"ort": "swim_platform", "set": "lola_bikini"},
                                             {"ort": "village_harbour", "set": "lola_denim"},
                                             {"ort": "alvas_bar", "set": "lola_denim"},
                                             {"ort": "alvas_terrace", "set": "lola_denim"}],
    "beschreibung": "the yacht's cook, 24, a backpacker from Byron Bay, Australia, who signed on in Antibes because the "
                    "old chef quit and she was 'literally standing right there'; scatterbrained, warm, without malice, "
                    "often a little drunk or a little high and mostly happy; loses her phone three times a day; in the "
                    "galley she is focused, fast and wildly creative and never cooks the same dish twice; strong Aussie "
                    "slang ('mate', 'heaps', 'reckon', 'no worries'), starts sentences and forgets the end; calls Duc "
                    "'Captain' because 'it suits your face'; loves gossip because people are 'just so interesting', so "
                    "whatever she hears, the whole boat knows by dinner; Toto sells her 'herbs', she is Rosi's partner "
                    "in crime at night, Chiara despairs of her hygiene",
    "ablauf": {"*": "galley", "abend": "crew_mess", "nacht": "galley"}}
P["megan"] = {
    "name": "Megan McAllister", "kurz": "Megan", "romanzierbar": False, "st_ordner": "Megan McAllister",
    "stimme": "Sera", "set_standard": "Boardroom",
    # Outfits (Duc 29.10.2026): die Ordner heissen megan_boardroom/megan_inspection - ohne Alias fiel alles auf das erste
    # Set (Boardroom), das Inspektions-Outfit an Bord war nie zu sehen. Abends an Land Monaco, tags am Wasser Off Duty.
    "set_alias": {"Boardroom": "megan_boardroom", "Inspection": "megan_inspection"},
    "set_regeln": [{"ort": "swim_platform", "phase": "tag", "set": "megan_offduty_deck"},
                   {"ort": "sun_deck", "phase": "tag", "set": "megan_offduty_deck"},
                   {"ort": "village_piazza", "set": "megan_monaco_evening"},
                   {"ort": "alvas_terrace", "phase": "dinner", "set": "megan_monaco_evening"}]
                  + [{"ort": r, "set": "Inspection"} for r in SCHIFF],
    "beschreibung": "Fleet Director of the Eden Group, 38, from Edinburgh, responsible for all of the group's yachts; "
                    "cunning, strict, ruthlessly competent; plays the anime villain - dramatic pauses, a slow smile, a "
                    "short wicked laugh, theatrical threats - but is actually funny, a little mad and very sharp; bored "
                    "by people who agree with her, rewards cleverness even against her; precise and cold, a Scottish "
                    "edge when angry ('aye', 'wee', 'dinnae'); says 'First Officer' like a warning; loves metaphors "
                    "about chess, sharks and fire",
    "ablauf": {"*": None}}                                     # nur Telefon/Video, einmal an Bord (Hauptstory)
# ------------------------------------------------------------------ Brain-Trust-Figuren (Nacht 24.10.2026)
# Umbau-Liste vor Akt 1 (docs/wiki/START.md): Lola romanzierbar (Karte vorhanden), Maxwell, Jana und
# Yamamoto als Personen. Alva bekommt Begehren (Events vergeben es) und ist seit 24.10. mit eigener Karte romanzierbar. Sprites: Yamamoto liegt im ST-Ordner; Maxwell und Jana sind noch unsortiert.
P["lola"].update({
    "romanzierbar": True, "karte": "Lola Brennan", "schaetzt": ["charm", "empathy"],
    "lieblingsorte": ["galley", "aft_deck"],
    "beschreibung": P["lola"]["beschreibung"].replace("calls Duc 'Captain' because 'it suits your face'",
                                                      "calls Duc 'Boss'")
                    + "; once she worked in a star restaurant in Sydney where the head chef shouted every night and told "
                      "her she would never be more than a line cook - she walked out that night and drifted the other "
                      "way, barefoot, no recipes, free; under stress 'Yes, Chef!' still slips out and she laughs it off; "
                      "dreams of a little beach kitchen with no head chef; wants to hear that she is good",
})
MODUL["lieblingsgesten"]["lola"] = ["kompliment", "geheimnis", "zeit"]
MODUL["intim_vorlieben"]["lola"] = {"mag": ["Position: Bent Over Desk", "Position: Spooning", "Position: Cowgirl",
                                            "Act: Caressing"], "nein": []}
# 24.10.2026: Alva hat jetzt eine Karte (RoleplayGen "Alva Santoni", nur Akt-1-Wissen) -> romanzierbar (Paar 7).
P["alva"].update({"romanzierbar": True, "karte": "Alva Santoni", "schaetzt": ["empathy", "perception"],
                  "lieblingsorte": ["alvas_bar", "alvas_terrace"]})
MODUL["lieblingsgesten"]["alva"] = ["fragen", "zeit", "kompliment"]
MODUL["intim_vorlieben"]["bibi"] = {"mag": ["Act: Caressing", "Position: Spooning"], "nein": []}
MODUL["lieblingsgesten"]["bibi"] = ["fragen", "zeit", "necken"]       # wirkt erst, wenn sie romanzierbar wird (Duc 02.11.2026)
MODUL["intim_vorlieben"]["alva"] = {"mag": ["Act: Kissing", "Act: Massage", "Position: Spooning", "Act: Caressing"],
                                    "nein": ["Act: Spanking", "Act: Hair Pulling"]}
P["toto"]["beschreibung"] = P["toto"]["beschreibung"].replace(
    "the bosun, 47, from Naples;", "the bosun, 47, from Naples, of African descent;")
P["maxwell"] = {
    "name": "Maxwell 'Mr. Maximum' Ndlovu", "kurz": "Maxwell", "romanzierbar": False, "pronomen": "er",
    "st_ordner": "Maxwell Ndlovu", "set_standard": "maximum_steward_a",       # Sets 24.10. (vorher nur in modul.json)
    "set_regeln": [{"phase": "fruehstueck", "set": "maximum_training_b"}, {"ort": "aft_deck", "set": "maximum_training_b"},
                   {"phase": "abend", "set": "maximum_party_b"}],
    "beschreibung": "steward under Chiara and the yacht's personal trainer, 35, from Umlazi near Durban, raised by his "
                    "grandmother Gogo; two metres of muscle and the big brother of the boat; talks about himself in the "
                    "third person ('Mr. Maximum does not skip leg day'), one joke per sentence and one push-up per joke, "
                    "poses like Might Guy; calls Duc 'Number One'; trains the crew every morning at half past six on "
                    "the aft deck and never lets anyone stop at 'I can't'; secretly cries at romantic films and calls it "
                    "an allergy; terrified of anything that flies; never says a bad word about the crew",
    "ablauf": {"fruehstueck": "aft_deck", "tag": "main_salon", "dinner": "crew_mess", "abend": "crew_mess",
               "nacht": "crew_corridor"}}
P["jana"] = {
    "name": "Jana Maihoff", "kurz": "Jana", "romanzierbar": False, "karte": "Jana Maihoff",
    "set_standard": "jana_deck_a",                                             # Sets 24.10. (vorher nur in modul.json)
    "set_regeln": [{"ort": "swim_platform", "set": "jana_bikini_a"}, {"phase": "abend", "set": "pencil_shortsleeves_red", "nur_date": True},
                   {"phase": "nacht", "set": "eisc_bib_lounge_pink"}],
    "beschreibung": "deckhand in her first season under Toto, 21, from Favoriten in Vienna, the quiet middle child; on her "
                    "own she is shy and says sorry to doors, in a group she joins every tease a second too late and a "
                    "step too far and always gets caught; Viennese English ('Na geh!', 'Jessas!'); calls Duc 'Sir'; best "
                    "friend of Lea, Lola is kind to her; smuggled a white cat called Strudel aboard in Antibes and hides "
                    "him in the tender garage; is learning knots from Toto - the one thing she wants to be good at on "
                    "her own",
    "ablauf": {"fruehstueck": "aft_deck", "tag": "tender_garage", "dinner": "crew_mess", "abend": "crew_mess",
               "nacht": "crew_corridor"}}
P["yamamoto"] = {
    "name": "Yamamoto-san", "kurz": "Yamamoto", "romanzierbar": False, "pronomen": "er", "st_ordner": "Yamamoto-san",
    "set_standard": "yamamoto_hawaii_b",
    "set_regeln": [{"phase": "nacht", "set": "yamamoto_leder_a"}, {"ort": "swim_platform", "set": "yamamoto_badeanzug_b"},
                   {"phase": "abend", "set": "yamamoto_party_b"}, {"ort": "village_piazza", "set": "yamamoto_party_b"}],
    "beschreibung": "guest in the owner's suite, 52, a banker from Tokyo, son of a fisherman from the Noto peninsula; thirty "
                    "years of overtime and not one holiday until his heart gave him a warning and his daughter Hana booked "
                    "him the yacht; nobody knows his first name; sober the most polite man on the Riviera - bows, says "
                    "'So sorry', tips like a king - but his thoughts show on his face; one glass and he sings karaoke "
                    "with his shirt open; his 'bird photography' always ends with Maxwell's shadow; has a secret list of "
                    "forbidden things to do once in his life; calls Duc 'Officer-san' and Jana his kitsune; never touches "
                    "anyone without being asked",
    "ablauf": {"fruehstueck": "aft_deck", "tag": "sun_deck", "dinner": "main_salon", "abend": "main_salon",
               "nacht": "aft_deck"}}
# Lob fuer Attributsteigerungen (Duc 27.10.2026): auch die Nicht-Romanzen-Figuren an Bord schaetzen zwei Attribute und
# kommentieren Meilensteine (kern/lob.py). Ohne Begehren wirkt `schaetzt` bei ihnen nur auf die Kommentare. Holm sagt nichts.
for _pid, _att in {"megan": ["charm", "strength"], "maxwell": ["strength", "courage"], "jana": ["strength", "charm"],
                   "toto": ["cunning", "strength"], "yasin": ["charm", "cunning"],
                   "yamamoto": ["perception", "courage"]}.items():
    P[_pid]["schaetzt"] = _att
# Kloster San Martinu (Ortskapitel, 26.10.2026): nur in den Frames der Macchia, kein Tagesablauf an Bord; bekannt erst,
# wenn Duc sie dort trifft. Sprites in module\eden_rise\figuren (docs/wiki/figuren/kloster.md).
P["nonna"] = {
    "name": "Nonna Fiora", "kurz": "Nonna", "romanzierbar": False, "st_ordner": "Nonna Fiora",
    "set_standard": "nonna_standard",
    "beschreibung": "runs the monastery of San Martinu with its farm and pharmacy, around 60, silver hair pinned up loosely, "
                    "a rust-red linen blouse and a wooden spoon in her hand; firm and warm, threatens with the spoon and "
                    "only half means it ('Stand still, or I'll cook you!'); nobody leaves her kitchen hungry"}
P["isabelle"] = {
    "name": "Isabelle", "kurz": "Isabelle", "romanzierbar": False, "st_ordner": "Isabelle",
    "set_standard": "isabelle_standard",
    "beschreibung": "a young novice at San Martinu who works in the pharmacy; eager, a little clumsy with her herbs and "
                    "always apologising for the last small explosion; ankle-length habit"}
P["frederico"] = {
    "name": "Frederico", "kurz": "Frederico", "romanzierbar": False, "pronomen": "er", "st_ordner": "Frederico",
    "set_standard": "frederico_standard",
    "beschreibung": "a twelve-year-old orphan who lives at San Martinu and carves everyone who lives there an animal out of "
                    "wood; brave in the way of a boy who wants to do something important just once"}
# Ortskapitel Berge (27.10.2026): nur in den Frames der Berge, Stimmen per ElevenLabs Voice Design in der Muttersprache
# (werkzeuge/eden_rise/stimmen_design.py), Sprites in module/eden_rise/figuren (Wolff, Ghjuvan, Dumenica bestellt).
P["laetitia"] = {
    "name": "Laetitia Albertini", "kurz": "Laetitia", "romanzierbar": False, "st_ordner": "Laetitia Albertini",
    "set_standard": "laetitia_standard", "stimme": "Laetitia Albertini",
    "beschreibung": "Petru's daughter, 24, a faded red bandana round her neck; always wanted to leave the village and "
                    "never told her father she loves him; hides the wounded deserter Adrien in a bergerie and would "
                    "shoot anyone who comes for him; sharp, proud, warm only underneath"}
P["adrien"] = {
    "name": "Adrien Morel", "kurz": "Adrien", "romanzierbar": False, "pronomen": "er", "st_ordner": "Adrien Morel",
    "set_standard": "adrien_standard", "stimme": "Adrien Morel IN",
    "beschreibung": "caporal of the Foreign Legion, 28, a handsome Indian man, deserted after his unit was secretly lent to guard "
                    "an estate in the mountains where he photographed animals in cages; wounded, soft-spoken, tries to "
                    "stay calm and jokes when it hurts"}
P["wolff"] = {
    "name": "Kaspar Wolff", "kurz": "Wolff", "romanzierbar": False, "pronomen": "er", "st_ordner": "Kaspar Wolff",
    "set_standard": "wolff_standard", "stimme": "Kaspar Wolff",
    "beschreibung": "sergent of the Foreign Legion, late forties, German from the Vosges; strict, correct, quotes the "
                    "service regulations, writes everything in a notebook with a pencil he sharpens with a knife; "
                    "melts for goats; patient - waiting is the half of his job he is best at"}
P["ghjuvan"] = {
    "name": "Ghjuvan Santucci", "kurz": "Ghjuvan", "romanzierbar": False, "pronomen": "er",
    "st_ordner": "Ghjuvan Santucci", "set_standard": "ghjuvan_standard", "stimme": "Ghjuvan Santucci",
    "beschreibung": "the last shepherd on the mountain, late fifties, widower; five generations on the same pasture, a "
                    "bank letter folded to pieces, forty sheep and a bear that takes one every night; A.V. Estates "
                    "wants to buy his land; counts his sheep three times, desperate and proud"}
P["dumenica"] = {
    "name": "Dumenica", "kurz": "Dumenica", "romanzierbar": False, "st_ordner": "Dumenica",
    "set_standard": "dumenica_standard", "stimme": "Dumenica",
    "beschreibung": "an old mazzera by the mountain lake, late seventies, in black; in Corsican belief she hunts in her "
                    "dreams and the animal she kills wears the face of someone who will die; dreamed her own son's face "
                    "twenty years ago and lost him; the village avoids her; calls Duc 'my son'"}
# Strand-Grotte (Akt 2 Woche 2, 27.10.2026, ereignisse_grotte.py): nur in den Frames, Stimmen per ElevenLabs Voice
# Design in der Muttersprache (stimmen_design.py --ziel stimmen_grotte), Sprites bei Character Design bestellt.
# Red Trio (30.10.2026, ereignisse_red_trio.py): nur in den Frames, Dorf-NPCs erst nach der Quest
P["danzel"] = {
    "name": "Danzel", "kurz": "Danzel", "romanzierbar": False, "pronomen": "er", "st_ordner": "Danzel",
    "set_standard": "danzel_B", "stimme": "Danzel",
    "beschreibung": "30, Japanese-French, a failed fashion designer from Paris who drew armour plates for Alon's lab and "
                    "didn't know they would go on animals; theatrical when frightened, calm only when he sews"}
P["bibi"] = {
    "name": "Bibi", "kurz": "Bibi", "romanzierbar": False, "pronomen": "sie", "st_ordner": "Bibi",
    "set_standard": "bibi_A", "stimme": "Bibi", "set_frei": [{"flag": "mochis_offen", "set": "Mochis"}],   # sie bleibt und leitet die Station (Duc 01.11.2026)
    "ablauf": {"*": "mochis", "nacht": None},                  # Time with: erst wenn der Raum offen ist (mochis_offen, Duc 02.11.2026)
    # Romanze erst mit allen drei Flags, kern/rollen.romanze_abgleichen (Duc 02.11.2026, Wiki figuren/bibi.md)
    "romanze_flags": ["kl_loewe_frei", "rt_ausgang_alle", "rt_bibi_bleibt"],
    "lieblingsorte": ["mochis"], "schaetzt": ["empathy", "courage"],
    "gesten": ["talks faster than she thinks and has to go back for the start of the sentence", "gives everything a name, including the bucket", "laughs too loud when she is afraid", "writes things on the back of a feed bill and loses it"],
    "set_regeln": [{"ort": "duc_cabin", "set": "Mochis"}],
    "beschreibung": "25, German-French animal keeper from Alon's Ark division, raised a lion for two years; laughs too "
                    "loud when she is afraid"}
P["charly"] = {
    "name": "Charly de Ravenel", "kurz": "Charly", "romanzierbar": False, "pronomen": "sie", "st_ordner": "Charly",
    "set_standard": "charly_A", "stimme": "Charly",
    "beschreibung": "26, French, daughter of an arms dynasty, wrote the collar code and knew what it was for; rates "
                    "everything out of ten instead of saying what she feels"}
P["mrwhite"] = {
    "name": "Mr. White", "kurz": "Mr. White", "romanzierbar": False, "pronomen": "er", "st_ordner": "MrWhite",
    "set_standard": "mrwhite_A", "stimme": "MrWhite",
    "beschreibung": "Alon's chief of agents, silver-haired, Scandinavian, fifties, white suit, courteous and cold"}
# Nur fuer seine Bilder in Szenen (Taktik-Karte, Duc 02.11.2026): Figurensatz aus figuren/Captain Bonaventure, noch ohne Stimme
P["bonaventure"] = {
    "name": "Captain Buenaventura", "kurz": "Buenaventura", "romanzierbar": False, "pronomen": "er", "st_ordner": "Captain Bonaventure",
    "set_standard": "bonaventure_standard",
    "beschreibung": "a pirate captain with a flag, an anthem and debts, the king of no island; robs ships but does not burn grandmothers"}
P["minicu"] = {
    "name": "Minicu", "kurz": "Minicu", "romanzierbar": False, "pronomen": "er", "st_ordner": "Minicu",
    "set_standard": "minicu_standard", "stimme": "Minicu",
    "beschreibung": "a gentle, slow giant, a Corsican dock worker of 34, very big and soft, with long shaggy hair and a full beard. He carries the crates in the harbour and trusts Pascal completely"}
P["alon"] = {"name": "Alon Varenne", "kurz": "Alon", "romanzierbar": False, "pronomen": "er", "st_ordner": "Alon", "set_standard": "alon_standard", "stimme": "Alon Varenne", "beschreibung": "a Canadian tech billionaire in his fifties with French roots, owner of A.V. Estates; a smooth, friendly keynote voice, talks about people like software and laughs at his own jokes"}     # Cliffhanger Akt 2 (Duc 02.11.2026)

P["gennaro"] = {
    "name": "Gennaro Esposito", "kurz": "Gennaro", "romanzierbar": False, "pronomen": "er", "st_ordner": "Gennaro Esposito",
    "set_standard": "gennaro_standard", "stimme": "Gennaro Esposito",
    "beschreibung": "Toto's cousin from Bastia, early forties, a charming, nervous talker with a gold tooth and a "
                    "seven-year-old daughter; owes money to the wrong people and runs crates at night for whoever "
                    "pays; always one bad idea away from the next one, and knows it"}
P["matteu"] = {
    "name": "Matteu Pinelli", "kurz": "Matteu", "romanzierbar": False, "pronomen": "er", "st_ordner": "Matteu Pinelli",
    "set_standard": "matteu_standard", "stimme": "Matteu Pinelli",
    "beschreibung": "a fisherman's son from the village, 19, shy and stubborn; dives in the grotto for the smugglers "
                    "because they promised to tell him where his older brother Ghjacumu drowned last year; wants only "
                    "to bring him home to their mother"}
P["chloe"] = {
    "name": "Chloé Marchal", "kurz": "Chloé", "romanzierbar": False, "st_ordner": "Chloe Marchal",
    "set_standard": "chloe_standard", "stimme": "Chloe Marchal",
    "beschreibung": "a treasure hunter from Marseille, 30, quick and bright and in over her head; searches the grotto "
                    "with her partner Bastien for the strongbox of a schooner that sank in 1924; their expedition is "
                    "paid for by A.V. Estates, and she tells herself that doesn't matter"}
P["riscossore"] = {
    "name": "U Riscossore", "kurz": "the Collector", "romanzierbar": False, "pronomen": "er",
    "st_ordner": "U Riscossore", "set_standard": "riscossore_standard", "stimme": "U Riscossore",
    "beschreibung": "the debt collector of the Bastia smugglers, in his sixties, a linen suit gone yellow at the "
                    "cuffs; very calm, very polite, never in a hurry; peels an orange while he talks business; "
                    "nobody in the village says his real name"}
# Dorf-Figuren (Duc 30.10.2026, docs/wiki/welt/dorf_figuren.md, E-089/E-093): nur oeffentliches Wissen, ihre Geheimnisse
# stehen im Wiki und nie hier. Noch ohne Szenen, nicht in bekannt_start; Sprites bei Character Design bestellt.
P["pascal"] = {
    "name": "Pascal Leca", "kurz": "Pascal", "romanzierbar": False, "pronomen": "er", "st_ordner": "Pascal Leca",
    "set_standard": "pascal_standard", "stimme": "Pascal Leca",
    "beschreibung": "deputy mayor of Cala d'Orsu, 52, lives above the town hall and eats standing up; knows everybody's "
                    "name and always uses it; quiet, kind, tired, laughs at himself; solves problems before anyone asks "
                    "('Leave it with me.'); the only person who claps at the mayor's speeches"}
P["mina"] = {
    "name": "Mina Orsoni", "kurz": "Mina", "romanzierbar": False, "pronomen": "sie", "st_ordner": "Mina Orsoni",
    "set_standard": "mina_standard", "stimme": "Mina Orsoni",
    "beschreibung": "24, delivers the post and parcels on an old Vespa, to the village, to Bastia and every week up to the "
                    "monastery; cheeky, fast, always a bit out of breath; knows what is in every letter and says 'I don't "
                    "read them. I just know.'; gets speeding tickets from Elsa, who has known her since she was small"}
P["batu"] = {
    "name": "Bà Tư", "kurz": "Bà Tư", "romanzierbar": False, "pronomen": "sie", "st_ordner": "Ba Tu",
    "set_standard": "batu_standard", "stimme": "Ba Tu",
    "beschreibung": "in her mid-seventies, born in Saigon, Catholic, runs the small Asian shop behind the harbour; always "
                    "cooks far too much and brings it to people's homes; counts every cent; bossy, dry and warm; tells "
                    "people they are too thin ('Eat.'); calls Duc 'con' (child)"}
P["sandru"] = {
    "name": "Sandru Amrani", "kurz": "Sandru", "romanzierbar": False, "pronomen": "er", "st_ordner": "Sandru Amrani",
    "set_standard": "sandru_av", "stimme": "Sandru Amrani",
    "beschreibung": "30, son of Moroccan farm workers, grew up in the village, manages the new A.V. Market in the old shop house opposite Alva's bar; "
                    "wears black leg braces that hum quietly because of an illness in his legs; polite, quick, tries too "
                    "hard, laughs before he speaks; his name tag says ALEX but the village calls him Sandru"}
P["anghjulu"] = {
    "name": "Don Anghjulu", "kurz": "Don Anghjulu", "romanzierbar": False, "pronomen": "er", "st_ordner": "Don Anghjulu",
    "set_standard": "anghjulu_standard", "stimme": "Don Anghjulu",
    "beschreibung": "the village priest, around sixty, a sun-browned Portuguese who came fourteen years ago and stayed, "
                    "round, red-nosed and usually a little drunk; warm, lazy, big laugh, "
                    "plays cards and loses gracefully ('God sees everything. Cut the cards.'); at war with Kevin the gull "
                    "over the bell tower; much kinder and sharper than he looks when it counts"}
# Flut-Nacht (Duc 28.10.2026): die Sirene im schwarzen Teich, besiegt nur durch Reden. Seit 29.10. ist sie Ligeia aus
# der Odyssee (docs/wiki/figuren/ligeia.md), Stimme aetherisch mit neapolitanischem Akzent (stimmen_design.py ligeia_it 3)
P["sirene"] = {
    "name": "The Siren", "kurz": "the Siren", "romanzierbar": False, "pronomen": "sie", "st_ordner": "The Siren",
    "set_standard": "sirene_standard", "stimme": "Ligeia",
    "beschreibung": "a sea spirit in the black pool of the smugglers' grotto, wet honey-blonde hair like weed, a long "
                    "emerald fish tail, only rises at high tide; ancient, with a soft Neapolitan lilt, calls every man 'sailor' and swears by 'Gods'; sang the "
                    "crew of an old sailing ship to sleep a hundred years ago and watches over the wreck; old, lonely, "
                    "amused, dangerous. Never names herself, never speaks of sisters, Homer or sirens"}
# Beschreibungen nach der Figuren-Runde (22./23.10.2026, docs/wiki/START.md) - nur oeffentliches Wissen, keine
# Fall-Aufloesungen und keine Geheimnisse, die die Figur nicht von sich aus zeigt.
P["holm"]["beschreibung"] = (
    "the captain, 52, from Alesund in Norway, eleven seasons on the Eden Rise, a legend of the fleet; dry, fair, "
    "impossible to fool, never loud and never says anything twice; wears her father's brass compass and drinks her "
    "coffee cold; calls her new First Officer 'Frankfurt' and does not yet take him quite seriously; the crew is her "
    "family and she pretends that annoys her; she has had stomach pains all day and waves them away; says 'Takk'")
P["elsa"]["beschreibung"] = (
    "lieutenant of the maritime gendarmerie, 29, born in Cala d'Orsu into a big loud fishing family - father Ange, "
    "mother Marie-Jo with the vegetable stall at the harbour who calls her on duty to ask when she will marry, three "
    "big brothers and a Nonna who cooks for fourteen every Sunday; has run the small coast-guard post for five years "
    "with two men, a fast patrol boat and an antenna that has waited eleven months for a form; dry humour, sharp eyes, "
    "never breaks a rule but bends one for the village; chases Toto like Zenigata chases Lupin ('TOTOOO!'); money is an "
    "insult, figs are fine; secretly reads romance novels and cries at Disney films - anyone who tells gets a ticket")
P["alva"]["beschreibung"] = (
    "owner of the only bar in Cala d'Orsu, 35; her Corsican father Ghjuvan ran the bar for forty years, her mother was "
    "Andalusian and her grandmother danced flamenco in Seville; at 22 Alva wanted to go to Seville to dance, then her "
    "father had a stroke and she came home and stayed; he died three years ago and the old jukebox in the corner has "
    "been silent since; knows everything that happens in the village, sells diesel under the counter, flirts with "
    "everyone and means it with nobody ('Everybody's welcome. Nobody's mine.'); calls people 'o figliolu' now and then; "
    "has not spoken to the mayor for two years")
P["petru"]["beschreibung"] = (
    "old fisherman in his seventies with his own boat workshop at the harbour; his wife Marie died five years ago and "
    "since then he mends nets that are not broken; says almost nothing - his 'Hm.' has ten meanings - and repairs "
    "everything for everyone without taking money, only fish and company; a radio on the workbench always plays "
    "Corsican football; his daughter Laetitia always wanted to leave and he never told her he needs her; knows every "
    "legend of the coast - his grandfather rowed out in 1924 when the village saved the crew of the Margot; 'The sea "
    "doesn't hurry.'")
P["casanova"]["beschreibung"] = (
    "mayor of Cala d'Orsu, 40, daughter of the old mayor; a whirlwind with anime-style humour - dramatic poses, "
    "exaggerated gasps, fist pumps, a confetti cannon and sudden speeches; organises every village feast like the "
    "Olympics and treats it like a season finale ('THIS. IS. THE. FESTA!'); the villa on the hill was her parents' house "
    "until her father had to sell it; loud because she carries a guilt she never mentions; has not spoken to Alva for "
    "two years; wants the stranded superyacht as the big attraction of the festa")
# Vertrauen auch fuer Nebenfiguren (Design 17.10.2026: Skala 0-5 fuer alle; Story-Wege haengen z. B. an Toto/Lola).
# Toto zaehlt zusaetzlich ueber seinen "Draht" (regeln.py, intern = sein Vertrauen). Begehren: fuenf Frauen + Lola + Alva.
NPC_START = {"lola": 2, "toto": 1, "holm": 1, "alva": 1, "yasin": 0, "megan": 0, "elsa": 0, "petru": 0, "casanova": 0,
             "maxwell": 1, "jana": 0, "yamamoto": 1, "nonna": 0, "isabelle": 0,
             "laetitia": 0, "adrien": 0, "wolff": 0, "ghjuvan": 0, "dumenica": 0,
             "gennaro": 0, "matteu": 0, "chloe": 0, "riscossore": 0, "danzel": 0, "bibi": 0, "charly": 0, "mrwhite": 0,
             "pascal": 0, "mina": 0, "batu": 0, "sandru": 0, "anghjulu": 0, "minicu": 0,      # Dorf-Figuren (30.10.2026)
             "sirene": 1}                 # Ligeia (29.10.2026): sichtbar, sobald man sie in der Flut-Nacht trifft
MODUL["werte"]["vertrauen"]["je"] = FRAUEN + list(NPC_START)
MODUL["werte"]["vertrauen"]["start"].update(NPC_START)
MODUL["werte"]["begehren"]["je"] = FRAUEN + ["lola", "alva"]
MODUL["werte"]["draht"]["label"] = "Trust Totò"            # Englisch seit 28.10.2026
# Strom und Diesel sind seit 30.10.2026 keine Werte mehr (Duc: "Strom brauchen wir nicht mehr", E-082); vorher seit
# 26.10. nur noch verborgen. Die Katastrophen-Uhr war ein Rest aus Gestrandet ohne Wirkung.
MODUL["uhren"].pop("katastrophe", None)
# Rueckhalt der Crew (Grundlagen 17.10.2026): 0-100, Bordrat, Versprechen, Uebergabe - die Events setzen ihn (B5)
MODUL["werte"]["rueckhalt"] = {"label": "Crew Backing", "bereich": [0, 100], "start": 50}

# Crew-Moral als Wochenstimmung (Duc 27.10.2026, Variante C; Regeln in kern\moral.py, Wiki systeme\interaktion.md):
# -5..+5, Start 0; Momente doppelt, Alltag nur bis +2, nachts -1 ueber 0; Wirkpunkte 1, 2, 4, 5, 8, 11, 13, 15.
MODUL["werte"]["moral"] = {"label": "Crew Mood", "bereich": [-5, 5], "start": 0}
MODUL["moral"] = {
    "stufen": [{"id": "buzzing", "ab": 4, "wort": "Buzzing", "gesicht": "😄"},
               {"id": "good", "ab": 1, "wort": "Good", "gesicht": "🙂"},
               {"id": "calm", "ab": 0, "wort": "Calm", "gesicht": "😐"},
               {"id": "tense", "ab": -3, "wort": "Tense", "gesicht": "😟"},
               {"id": "mutinous", "ab": -5, "wort": "Mutinous", "gesicht": "😠"}],
    "faktor": 2, "alltag_bis": 2, "tense_ab": -2, "geschenk_chance": 0.7,
    "info": "How the crew feels about the week, from Mutinous to Buzzing. Big moments - events, the night council, "
            "missions, the hearing - move it twice as far, in both directions. Cooking, snacks and time together lift "
            "it, but only up to Good. Every night it slips one step back towards Calm. Buzzing: the crew backs you on "
            "the dice and leaves you things at breakfast. Tense: they sulk, and the dice feel it.",
    "wuerfel": {"plus": "%s's got your back", "minus": "The crew is sulking"},
    "toene": {"buzzing": {"witzig": 1.5, "wholesome": 1.5, "frech": 1.2, "ernst": 0.6},
              "good": {"witzig": 1.2, "wholesome": 1.2, "ernst": 0.8},
              "tense": {"witzig": 0.8, "wholesome": 0.7, "ernst": 1.5},
              "mutinous": {"witzig": 0.6, "wholesome": 0.5, "ernst": 2.0}},
    "fruehstueck": {
        "buzzing": ["The galley is loud this morning. Lola sings along to the radio, badly, and nobody asks her to stop.",
                    "Someone has drawn a smiley face in the steam on the mess window. Nobody admits to it. Everybody "
                    "smiles at it anyway."],
        "good": ["Breakfast goes easy. Small jokes, refilled cups, the odd laugh from the galley.",
                 "Rosi steals a slice of toast off Lea's plate. Lea lets her. It's that kind of morning."],
        "calm": ["Breakfast is quiet. People eat, nod at each other and go to work.",
                 "The coffee machine hisses. Someone reads the weather out loud. That's about it."],
        "tense": ["Nobody talks much over breakfast. Cups go down on the table a little too hard.",
                  "Chiara hands out the day's jobs. Nobody argues. Nobody says thank you either."],
        "mutinous": ["Half the crew eat standing up, so they can leave sooner. The other half don't come at all.",
                     "There's a note taped to the mess door: WHO IS ACTUALLY IN CHARGE HERE? Nobody takes it down."]},
    "prompt": {
        "buzzing": "[Crew mood: buzzing] The crew is in high spirits this week and on Duc's side. Let it show in small "
                   "ways - warmth, teasing, a quick yes.",
        "good": "[Crew mood: good] The crew is in decent spirits. Small jokes come easily.",
        "tense": "[Crew mood: tense] The crew is on edge and a little fed up with Duc's calls. Let it show in small "
                 "ways - shorter answers, a sigh, a pointed remark - without making a scene of it.",
        "mutinous": "[Crew mood: close to mutiny] The crew has lost patience with Duc. She is openly short with him and "
                    "may question his decisions, but she still does her job."},
    "gefuehl": {"buzzing": "joy", "tense": "annoyance", "mutinous": "annoyance"},
    "anhoerung": {"plus": "The crew stands behind Duc", "minus": "The crew is fed up with Duc"},
    # Geschenke beim Fruehstueck (nur Buzzing): es zaehlt, was es im Modul schon gibt. Seit 27.10.2026 stehen alle
    # Kampf-Verbrauchsgegenstaende im Modul; das Megafon gibt es bei Megan im Eden-Shop statt von Sophia (Duc).
    "geschenke": [
        {"item": "plaster", "von": "chiara", "text": "%s leaves a box of plasters next to your coffee. \"You keep bleeding on my deck.\""},
        {"item": "bandage", "von": "chiara", "text": "%s drops a roll of gauze into your jacket pocket and doesn't explain."},
        {"item": "verbandskasten", "von": "chiara", "text": "%s sets an old canvas first aid pouch by your plate. \"Mine, from before. You need it more.\""},
        {"item": "espresso_single", "von": "lola", "text": "%s slides an espresso across the table. \"Drink it before it judges you.\""},
        {"item": "espresso", "von": "lola", "text": "%s hands you a double, already sugared. She knows how you take it by now."},
        {"item": "americano", "von": "lola", "text": "%s fills a tall mug and pushes it your way. \"For the long day. Don't thank me.\""},
        {"item": "mate", "von": "lea", "text": "%s passes you a gourd of mate, straw first. \"Share it next time.\""},
        {"item": "green_tea", "von": "sophia", "text": "%s leaves a glass of green tea by your plate. \"You look like you need calm more than coffee.\""},
        {"item": "duct_tape", "von": "rosi", "text": "%s tosses you a roll of duct tape across the mess. \"Fixes everything. Probably you too.\""},
        {"item": "whetstone", "von": "rosi", "text": "%s puts a grey whetstone in front of you. \"Your blade is a disgrace. Fix it.\""},
        {"item": "dog_food", "von": "lea", "text": "%s hands you a tin of dog food, completely serious. \"For the island strays. Trust me.\""},
    ],
}
# Freundes-Geschenke beim Fruehstueck (Duc 27.10.2026): unabhaengig von der Moral, ab einem Vertrauen, mit Chance und
# Pause in Tagen (je Eintrag), dazu "pause_person": eine Figur schenkt hoechstens jeden zweiten Morgen etwas. Hat die
# Crew an dem Morgen schon etwas geschenkt, kommt nichts dazu (ein Geschenk je Fruehstueck). Reihenfolge = Vorrang.
# "sortiment": ein Snack aus ihrer Kombuese (Art snack, "wo" sie, ohne Vertrauens-Sperre) mit Tipp, wer ihn liebt -
# zuerst fuer Figuren, deren Vorliebe Duc noch nicht kennt; die Vorliebe gilt danach als entdeckt.
# Platzhalter: {von} Schenkende, {snack} Name des Gegenstands, {fuer} wer ihn liebt.
MODUL["morgen_geschenke"] = {"pause_person": 2, "liste": [
    {"von": "lola", "item": "space_cake", "ab_vertrauen": 4, "chance": 0.20, "pause": 3, "texte": [
        "{von} leans in and closes your hand around a little foil parcel. \"Universe Edition. One slice, Boss, not "
        "three. And not where Chiara can see.\"",
        "{von} tucks a wrapped slice of cake under your napkin and gives you a slow wink. \"For a rough day. "
        "You'll know when.\""]},
    {"von": "lola", "item": "energieriegel", "ab_vertrauen": 3, "chance": 0.35, "pause": 2, "texte": [
        "{von} slides something wrapped in baking paper next to your cup. \"Oat and honey. For later, Boss. "
        "Don't tell the others, they'll want one too.\"",
        "{von} presses a little paper parcel into your hand on her way past. \"Made too many. Well. "
        "Made exactly one too many.\" She winks and keeps walking.",
        "{von} puts an energy bar on your plate, string still on it. \"You skipped lunch yesterday, I saw. "
        "Don't argue, just eat it. Mostly the honey.\""]},
    {"von": "lola", "sortiment": "snack", "ab_vertrauen": 2, "chance": 0.35, "pause": 2, "texte": [
        "{von} drops a paper bag next to your plate. \"{snack}. Not for you, Boss. Well, a bit for you. "
        "Mostly for {fuer}. {fuer} goes soft for these.\"",
        "{von} pushes a plate of {snack} your way. \"Leftovers. Take them to {fuer}, mate. Trust me on "
        "this one.\"",
        "\"{snack},\" {von} says, and tucks a box under your arm. \"{fuer}'s favourite. Don't tell anyone I "
        "told you.\""]},
]}
# Gras-Kuchen (Space Cake, Brownie "Captain's Calm"; Duc 27.10.2026): wer einen isst (Inventar oder Kampf), hat am
# naechsten Morgen einmal Energie -1. Je Tagesende findet Ferrandi einen Kuchen im Inventar mit "risiko" (in der
# Kabinen-Truhe mal kabine.schmuggel_faktor): beschlagnahmt, Ruf "ruf".
MODUL["gras"] = {"risiko": 0.10, "ruf": -1,
                 "kater": "😵 Your head is still floating somewhere above the mast. Lola's cake, probably.",
                 "fund": "⚠ Lieutenant Ferrandi does a spot check on deck and finds %s. She bags it without a word.",
                 "fund_truhe": "⚠ Lieutenant Ferrandi searches your cabin and finds %s in the chest. She bags it, "
                               "and gives you a long look."}
MODUL["bekannt_start"] =["chiara", "sophia", "lea", "rosi", "siri", "toto", "yasin", "holm", "lola", "megan",
                         "maxwell", "jana", "yamamoto"]
# Pascal erzaehlt Ducs Taten weiter: das erste Verblassen des Rufs faellt aus (Duc 30.10.2026, docs/wiki/systeme/dorf_redet.md)
MODUL["ruf_schutz"] = {"bekannt": "pascal", "flag": "ruf_schutz_verbraucht",
                       "text": "The village was about to forget you. Pascal told them about the boar again."}
MODUL["kabine"] = dict(copy.deepcopy(G.MODUL["kabine"]), kein_handy=[],       # Story: auch Petru ist per Telefon erreichbar
                       anruf_orte={"holm": "a hospital bed in Ajaccio", "megan": "her office at the Eden Group"})


# ------------------------------------------------------------------ Gegenstaende und Laeden (18.10.2026)
# Quelle: module\eden_rise\gegenstaende.json (werkzeuge\eden_rise\gegenstaende_eden_rise.py) und laeden.json - hier nur in das
# Format der Engine (kern\handel.py) uebersetzt. Geschmack: Grundhaltung je Kategorie (+ mag, 0 neutral, - mag nicht),
# dazu "liebt" (2), "hasst" (-1) und Einzigartiges (nur diese Person). Fundorte (quelle) werden zu Laeden:
# toto, alva, lola, eden -> megan (Eden-Shop per Videoanruf); "alva3" heisst: bei Alva ab ihrem Vertrauen 3.
MODDIR = os.path.dirname(ZIEL)
GEG = json.load(open(os.path.join(MODDIR, "gegenstaende.json"), encoding="utf-8"))
LAD = json.load(open(os.path.join(MODDIR, "laeden.json"), encoding="utf-8"))["laeden"]
NEUE_ITEMS = json.load(open(os.path.join(MODDIR, "ereignisse.json"), encoding="utf-8")).get("neue_items", {})
LADEN_VON = {"toto": "toto", "alva": "alva", "lola": "lola", "eden": "megan", "rosi": "rosi", "isabelle": "isabelle"}
WERT = {"+": 1, "0": 0, "-": -1}
ART_TEXT = {"gluecksbringer": "Once a day, advantage on %s.", "attribut": "+1 %s while you carry it."}   # Englisch (28.10.2026)
ATTR_DE = {"charm": "Charm", "empathy": "Empathy", "perception": "Perception", "cunning": "Cunning",
           "courage": "Courage", "strength": "Strength"}
SCHMUGGEL_EXTRA = {"limoncello_kiste": {"benutzen": [{"geld": 240, "text": "Limoncello an Alva"}]},
                   "taschen": {"geschenk": {"yasin": 2, "casanova": 2, "*": 0}}}


def _wirkung(w):
    out = []
    if "wert" in w:
        out.append({"wert": w["wert"][0], "delta": w["wert"][1]})
    if "uhr" in w:
        out.append({"uhr": w["uhr"][0], "delta": w["uhr"][1]})
    if "flag" in w:
        out.append({"flag": w["flag"]})
    return out


def item_umsetzen(it, alt):
    art = it["art"]
    neu = {"label": it["label"], "art": art, "text": it.get("text") or "", "preis": it.get("preis")}
    wo, ab = [], {}
    for q in it.get("quelle") or []:
        basis, stufe = q.rstrip("0123456789"), q[len(q.rstrip("0123456789")):]
        if basis in LADEN_VON:
            wo.append(LADEN_VON[basis])
            if stufe:
                ab[LADEN_VON[basis]] = int(stufe)
    if wo and it.get("preis"):
        neu["wo"] = sorted(set(wo))
        if ab:
            neu["ab"] = ab
    w = it.get("wirkung") or {}
    if art in ("geschenk", "einzigartig", "snack"):
        g = {}
        for pid, h in GEG["haltung"].items():
            g[pid] = 0 if art == "snack" else WERT.get(h.get(it.get("kat") or "", "0"), 0)
        for pid in it.get("liebt") or []:
            g[pid] = 2
        for pid in it.get("hasst") or []:
            g[pid] = -1
        if art == "einzigartig":
            g = {pid: (2 if pid == it["einzigartig"] else 0) for pid in g}
            neu["nur_fuer"] = it["einzigartig"]
        neu["geschenk"] = g
        neu["kat"] = it.get("kat")            # Kategorie: Haendler-Reaktion und Hinweise (26.10.2026)
        neu["art"] = "snack" if art == "snack" else "geschenk"
        if art == "snack":
            neu["benutzen"] = [{"wert": "energie", "delta": 1}]
            neu["text"] = neu["text"] or "From Lola's galley. Eat it yourself: energy +1."
            if w.get("gras"):                     # Gras-Kuchen (Duc 27.10.2026): Kater + Kontrolle (kern/handel.py)
                neu["gras"] = True
    elif art in ("gluecksbringer", "attribut"):
        neu["effekt"] = {"vorteil": w["vorteil"]} if art == "gluecksbringer" else {"bonus": w["bonus"]}
        att = w.get("vorteil") or w.get("bonus", [""])[0]
        neu["text"] = neu["text"] or ART_TEXT[art] % ATTR_DE.get(att, att)
    elif art == "ressource":
        neu["wirkung"] = _wirkung(w)
        neu["art"] = "verbrauch"
        if w.get("punkte_frauen"):                 # z. B. die Rose der Buergermeisterin: Punkte bei allen Frauen beim Benutzen
            wert, n = w["punkte_frauen"]
            neu["benutzen"] = [{"punkte": "%s.%s" % (wert, p), "n": n} for p in FRAUEN]
    elif art == "schmuggel":
        neu.update({k: v for k, v in (alt or {}).items() if k in ("benutzen", "geschenk", "text")})
        neu.update(SCHMUGGEL_EXTRA.get(it["id"], {}))
        neu.setdefault("benutzen", [])
        neu["text"] = neu["text"] or w.get("benutzen", "")
    elif art == "schluessel":
        neu["ort"] = w.get("ort")
    elif art == "kampf":                          # Kampfgegenstand (19.10.2026): wirkt nur in kern\kampf.py
        neu["kampf"] = w
    if it.get("kampf"):                           # 27.10.2026: auch andere Arten wirken im Kampf (Doppio)
        neu["kampf"] = it["kampf"]
    elif art == "gericht":
        neu["kochen"] = w
        # Lieblings-/Ekelgericht (Fix 18.10.2026): ging beim Umsetzen verloren, Kochen kannte nur "normal"
        neu["geschenk"] = dict({pid: 2 for pid in it.get("liebt") or []}, **{pid: -1 for pid in it.get("hasst") or []})
    if it.get("intim"):
        neu["intim"] = it["intim"]
    if it.get("kommentar"):                       # Teile: Satz der Ladenfigur beim Kauf (vertont)
        neu["kommentar"] = it["kommentar"]
    return neu


ITEMS = {k: v for k, v in copy.deepcopy(G.MODUL["items"]).items() if not v.get("wo")}   # alte Ladenware von Gestrandet nicht
for _it in GEG["items"]:
    ITEMS[_it["id"]] = item_umsetzen(_it, ITEMS.get(_it["id"]))
for _iid, _it in NEUE_ITEMS.items():
    if _iid not in ITEMS:
        ITEMS[_iid] = dict(_it, preis=_it.get("preis"))
        if _it.get("wirkung"):
            ITEMS[_iid]["wirkung"] = [{"wert": f["wert"], "delta": f.get("delta", 1)} if "wert" in f else
                                      {"wert": "vertrauen." + f["vertrauen"][0], "delta": 1} for f in _it["wirkung"]]
# Ligeias Geschmack (29.10.2026, docs/wiki/figuren/ligeia.md): Worte und Dinge vom Land; Lampen, Stahl, Gefangenes nicht
LIGEIA_GESCHMACK = {"gedichtband": 2, "ducs_gedicht": 2, "alvas_rose": 2, "macchia_strauss": 2,
                    "pink_pearl": 1, "pretty_shell": 1, "seeglas": 1, "ukulele": 1, "canistrelli": 1,
                    "dive_torch": -1, "lichterkette": -1, "schweizer_messer": -1, "goldfisch": -1}
for _iid, _it in ITEMS.items():
    if _it.get("geschenk") is not None and _it.get("art") == "geschenk" and not _it.get("nur_fuer"):
        _it["geschenk"]["sirene"] = LIGEIA_GESCHMACK.get(_iid, -1 if _it.get("kat") == "intim" else 0)
# Strom/Diesel-Ware (E-076 ruhte sie seit 26.10.2026; seit 30.10. gibt es die Werte nicht mehr): bleibt nur als Eintrag
# fuer alte Spielstaende, handel.sortiment bietet sie nie an, die Wirkung ist leer.
for _iid in ("diesel_canister", "used_battery", "panel_cleaner"):
    ITEMS[_iid]["pausiert"] = "entfernt"
    ITEMS[_iid].pop("wirkung", None)
# Keepsake Box (26.10.2026, Duc): Vitrine in der Kabine. In der Vitrine stehen nur Andenken, die ein Event wirklich vergibt
# (Altlasten von Gestrandet nicht). Echo = vertonte Zeile der Gebenden aus diesem Event, abgespielt ueber /api/zeile ev.<key>.
ECHO = {"muschelkrone": "br_ehrenbuerger#z1", "rosis_foto": "hy_rosi_foto#o1", "holms_foto": "hy_holm_nacht#z1",
        "drohnen_propeller": "g1_drohne#o1", "siris_haarband": "g1_siri_tanz#z0", "siris_karte": "br_siris_geburtstag#o0",
        }
_EV = json.load(open(os.path.join(MODDIR, "ereignisse.json"), encoding="utf-8"))["events"]
# Selfie-Events (27.10.2026): Echo = ihre Antwort auf das Kompliment (erste Reihe je Frau und Stufe; alle Reihen teilen die Zeile)
for _e in _EV:
    if (_e["personen"].get("selfie") or {}).get("stufe"):
        _iid = "%s_selfie_%d" % (_e["personen"]["selfie"]["frau"], _e["personen"]["selfie"]["stufe"])
        ECHO.setdefault(_iid, "%s#o1" % _e["id"])
        # Das Andenken traegt den Namen des Fotos, das Duc gesehen hat (31.10.2026)
        ITEMS[_iid].setdefault("titel_je_bild", {})[_e["personen"]["selfie"]["bild"]] = _e["titel"]
_ZEILEN = {}
for _e in _EV:
    _ZEILEN.update({"%s#z%d" % (_e["id"], _n): _z for _n, _z in enumerate(_e["zeilen"])})
    _ZEILEN.update({"%s#o%d" % (_e["id"], _k): _o["zeile"] for _k, _o in enumerate(_e["optionen"]) if _o.get("zeile")})
_VERGEBEN = json.dumps(_EV, ensure_ascii=False)
for _iid, _it in ITEMS.items():
    if _it.get("art") == "andenken" and '"item": "%s"' % _iid in _VERGEBEN:
        _it["vitrine"] = True
        # Beschreibung: der leere Katalog-Eintrag verdeckte den Text aus neue_items; der Epilog-Hinweis ist Technik, kein Gedanke
        _it["text"] = _it["text"] or (NEUE_ITEMS.get(_iid, {}).get("text") or "").replace(" Visible in the epilogue.", "")
for _iid, _key in ECHO.items():
    assert ITEMS[_iid].get("vitrine") and _key in _ZEILEN, "Echo %s -> %s fehlt" % (_iid, _key)
    ITEMS[_iid]["echo"] = {"key": "ev." + _key, "wer": _ZEILEN[_key]["wer"], "text": _ZEILEN[_key]["text"]}
# Stapeln (Duc 28.10.2026, Wiki items.md "Stapeln"): Consumables und Materials stapeln nach Beute-Stufe - gewoehnlich 5,
# gut 3, selten/meisterlich 1. Alles mit Geschichte (Geschenke, Wertsachen, Charms, Schmuggel, Unikate) bleibt einzeln.
# Feld "stapel" nur, wenn > 1 (kern/zustand.stapel, Standard 1).
STAPEL_GEWOEHNLICH = ["plaster", "cooling_spray", "duct_tape", "espresso_single", "americano", "mate", "green_tea", "dog_food",
                      "espresso", "energieriegel"] + [_i for _i, _x in ITEMS.items() if _x.get("art") == "snack"]
STAPEL_GUT = ["bandage", "verbandskasten", "smoke_pot", "whetstone_blue", "whetstone", "whetstone_red", "spikes", "match_ammo",
              "grenade_fire", "grenade_water", "grenade_shock", "grenade_flash", "steel_plate", "jade", "topas", "aquamarin",
              "amethyst", "kupfer", "kuehlakkus"] + [_i for _i, _x in ITEMS.items() if _x.get("art") == "gericht"]
for _n, _ids in ((5, STAPEL_GEWOEHNLICH), (3, STAPEL_GUT)):
    for _iid in _ids:
        assert _iid in ITEMS, "Stapel: %s fehlt" % _iid
        ITEMS[_iid]["stapel"] = _n
MODUL["items"] = ITEMS

# Lore-Texte (Duc 29.10.2026, docs/wiki/STIL.md "Item-Beschreibungen"): text = Lore aus werkzeuge/englisch/item_lore.py,
# die Wirkung (Saetze mit Bonus, Heilung, Kampf, Preis-Folgen) wandert nach wirkung_text und steht im Client als eigene Zeile.
WIRKUNG_SATZ = re.compile(r"In a fight|Once a day|advantage|[+−-]\d|heals|Use it|Quick:|^For (sabres|knives|the|blunt)|upgrade|"
                          r"Trust|Reputation|€|Phone features|Desire|Eat it yourself|supplies last|a day at most|"
                          r"Useless|On a wet|damage", re.I)


def lore_einsetzen(items):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "englisch"))
    from item_lore import LORE, NAMEN
    for iid, name in NAMEN.items():                       # neue Namen (29.10.2026)
        if iid in items:
            items[iid]["label"] = name
    for iid, (_, lore) in LORE.items():
        it = items.get(iid)
        if not it:
            continue
        muster = re.compile(r"Once a day|\+\d") if it.get("effekt") else WIRKUNG_SATZ    # Getragenes: nur der Bonus-Satz
        eff = " ".join(s for s in re.split(r"(?<=[.!?])\s+", it.get("text") or "") if muster.search(s))
        if not eff and it.get("effekt"):                 # Attribut/Gluecksbringer ohne Satz: aus dem Effekt
            e = it["effekt"]
            att = e.get("vorteil") or (e.get("bonus") or [""])[0]
            eff = ART_TEXT["gluecksbringer" if "vorteil" in e else "attribut"] % ATTR_DE.get(att, att)
        if not eff and it.get("art") == "snack":
            eff = "Eat it yourself: energy +1."
        if eff:
            it["wirkung_text"] = eff
        it["text"] = lore


lore_einsetzen(MODUL["items"])
MODUL["laeden"] = {
    "toto": dict(G.MODUL["laeden"]["toto"]),
    "alva": dict({k: v for k, v in LAD["alva"].items() if k != "zeilen"}, sortiment=10),
    "lola": dict({k: v for k, v in LAD["lola"].items() if k != "zeilen"}, sortiment=6),
    "megan": {k: v for k, v in LAD["megan"].items() if k != "zeilen"},
    "rosi": {k: v for k, v in LAD["rosi"].items() if k != "zeilen"},       # Werkstatt; seit 27.10.2026 mit Waffenpflege
    # Naturmedizin aus der Klosterapotheke (Duc 27.10.2026): bestellt wie bei Megan, erst wenn Duc Isabelle kennt
    "isabelle": dict({k: v for k, v in LAD["isabelle"].items() if k != "zeilen"}, erst_bekannt=True),
    # Nonnas Farm (Duc 27.10.2026, E-079): Garten, drei Staelle, Tagesvorrat - kein Warenladen, Fenster im Plugin eden-farm
    # (kern/farm.py, kern/kuechen.py, Daten in kuechen.json). Oeffnet ab Tag 4 (kuechen.json nonna.ab_tag).
    "nonna": {"name": "Nonna's Farm", "wer": "nonna", "nur_an_land": False, "farm": True, "ab_tag": 4,
              "hintergrund": "eden_rise_monastery_garden_dusk.png", "set": "nonna_standard",
              "text": "Beds, sheds and a very opinionated goat. Nonna sells what she can spare, and Frederico runs it down to the harbour."},
    # Petrus Werkstatt (Duc 28.10.2026): freier Laden ab Tag 2, Axt und Spitzhacke in 3 Stufen (kern/abbau.py, Fenster im Plugin
    # eden-abbau); Koeder, Upgrades und Fischverkauf folgen. Zeilen in laeden.json (kochen_eden_rise.py).
    "petru": {"name": "Petru's Workshop", "wer": "petru", "nur_an_land": False, "werkzeug_laden": True, "ab_tag": 2,
              "hintergrund": "corsican_fisherman_workshop.png", "set": "Standard",
              "text": "Nets, a blue boat on trestles and a radio that only plays Corsican football. Petru sells tools now, because someone has to pay for the diesel."},
    # Danzels Laden (Duc 30.10.2026, Piazza): ab dem 3. Tag nach dem Quest-Ende, in beiden Ausgaengen (E-112). Alle Kleidung zieht
    # dann hierher, bis dahin (und ohne Laden) bleibt sie bei den alten Haendlern. Zeilen in laeden.json (kochen_eden_rise.py).
    "danzel": {"name": "Le Th\u00e9\u00e2tre Rouge", "wer": "danzel", "nur_an_land": True, "handel_punkte": True,
               "hintergrund": "eden_rise_theatre_rouge.png", "set": "danzel_B",
               "bedingung": {"alle": [{"flag_seit": ["rt_ende_tag", 3]}]},
               "uebernimmt": ["wool_socks", "wollmuetze", "silk_kimono", "stockings", "lingerie", "flamenco_dessous"],
               "text": "The old room on the piazza with the good window. One red curtain, one mannequin, and a man who measures you with his eyes before he says hello."},
}
# Ba Tus Laden (Duc 30.10.2026): oeffnet mit ihrer ersten Szene. Zeilen in laeden.json (kochen_eden_rise.py). Ware unten: Asia-Laden mit Vorrats-Zutaten.
MODUL["laeden"]["batu"] = {"name": "B\u00e0 T\u01b0's Shop", "wer": "batu", "nur_an_land": True, "hintergrund": "eden_rise_batu_shop.png",
                           "set": "batu_standard", "bedingung": {"flag": "batu_laden"},
                           "text": "Too many shelves for the room, a wall of amber bottles and a small Virgin Mary with a fresh flower. "
                                   "The pot at the back is always on."}
MODUL["items"]["fish_sauce"].update(preis=12, wo=["batu"], art="zutat", zutat="fish_sauce",
                                    wirkung_text="For cooking, as the flavour: nobody dislikes the dish, whatever is in it.")
# Asia-Ware (Duc 30.10.2026 Items-Sitzung): gehen in den Vorrat, Rollen in kochen_daten.py; Reis und Sojasauce einen Euro unter Nonna
for _i, _label, _preis, _text, _wirkung in (
    ("tofu", "Tofu", 8, "White, firm and pressed this morning at the back of the shop. It tastes of almost nothing until you teach it. "
                        "B\u00e0 T\u01b0 says the same about young men.", "For cooking, as the main. Counts as vegetables."),
    ("rice_paper", "Rice Paper", 5, "Thin round sheets, dry as old letters. One second in warm water and they bend to anything. Tear one, "
                                    "and you will hear how her mother did it.", "For cooking, as the base."),
    ("rice", "Rice", 3, "Long-grain rice from the same cousin in Marseille. Still nobody knows which cousin. She washes it three times and "
                        "thinks less of you if you wash it twice.", "For cooking, as the base."),
    ("sojasauce", "Soy Sauce", 5, "Dark, salty and cheaper here than at the farm. She keeps it on the bottom shelf. The fish sauce gets the top.",
     "For cooking, as the flavour: sell prices go up for a day."),
):
    assert _i not in MODUL["items"], "Ba Tu: Item %s gibt es schon" % _i
    MODUL["items"][_i] = {"label": _label, "art": "zutat", "zutat": _i, "preis": _preis, "wo": ["batu"], "text": _text, "wirkung_text": _wirkung}
# Die Schale aus dem Topf (Duc 31.10.2026): keine Moral, aber Energie; zaehlt als Essen des Tages, einmal am Tag
MODUL["items"]["pho_bowl"] = {"label": "Bowl from the Pot", "art": "verbrauch", "preis": 8, "wo": ["batu"], "essen": True, "wirkung": [{"wert": "energie", "delta": 1}],
                              "text": "Pho from the pot at the back, the one that is never off the fire. She counts every cent, then gives you too much. "
                                      "You eat it here, standing, while she watches.",
                              "wirkung_text": "Energy +1. Counts as your meal of the day. Once a day."}
MODUL["laeden"]["batu"]["tageslimit"] = {"pho_bowl": "batu_schale_tag"}
# Zitronengras (Duc 31.10.2026): einmal kaufen, dann waechst es in Nonnas Garten
MODUL["items"]["lemongrass_cutting"] = {"label": "Lemongrass Cuttings", "art": "zutat", "preis": 25, "wo": ["batu"], "einmalig": True, "wirkung": [{"flag": "zitronengras_da"}],
                                        "text": "Three stalks in damp brown paper, from the pots behind her shop. They want sun, water and a better bed than "
                                                "she has. She knows who has one.",
                                        "wirkung_text": "Unlocks Lemongrass in Nonna's garden."}
MODUL["items"]["green_tea"].update(preis=9, wo=sorted(set((MODUL["items"]["green_tea"].get("wo") or []) + ["batu"])))
for _i in MODUL["laeden"]["danzel"]["uebernimmt"]:
    MODUL["items"][_i]["wo"] = sorted(set(MODUL["items"][_i]["wo"] + ["danzel"]))
# Bibis Tierstation (Duc 31.10.2026, systeme/tierstation.md): kein Warenladen, Fenster im Plugin eden-mochis (kern/mochis.py)
import mochis_daten as _mo  # noqa: E402
MODUL["laeden"]["mochis"] = {"name": "Mochi's", "wer": "bibi", "nur_an_land": True, "mochis": True, "hintergrund": "eden_rise_mochis_station_voll.png", "set": "bibi_A",
                             "bedingung": {"alle": [{"flag": "mochis_offen"}, {"flag_seit": ["rt_ende_tag", 1]}]},
                             "text": "An old shepherds' estate on the terraces above the bay, with a barn that has half a roof, a very neat sign and a long row of bowls. Bibi keeps a field book here, and she is the only one who can read it."}
MODUL["mochis"] = {"tiere": _mo.TIERE, "seiten": _mo.SEITEN, "granate": _mo.GRANATE, "granaten": _mo.GRANATEN, "futter_geld": _mo.FUTTER_GELD, "tage_futter": _mo.TAGE_FUTTER,
                   "tage_einfach": _mo.TAGE_EINFACH, "koeder_runden": _mo.KOEDER_RUNDEN, "stufe_ab": {str(k): v for k, v in _mo.STUFE_AB.items()},
                   "halsband_ziel": _mo.HALSBAND_ZIEL, "ausbau_ab": _mo.AUSBAU_AB, "bild_anfang": _mo.BILD_ANFANG, "bild_voll": _mo.BILD_VOLL, "wieder_tage": _mo.WIEDER_TAGE,
                   "duc_seite": _mo.DUC_SEITE}
# Danzels Auftraege (Duc 30.10.2026, systeme/schneider.md): Material zu kaufen, die Auftraege selbst, Chiaras Outfit (Pilot)
MODUL["laeden"]["danzel"]["schneider"] = True
_OFFEN = MODUL["laeden"]["danzel"]["bedingung"]["alle"]
_GHJUVAN = {"alle": [{"flag": "bg_ghjuvan_getroffen"}, {"nicht": {"flag": "bg_ghjuvan_tot"}}]}
MODUL["items"]["cloth_bolt"] = {"label": "Bolt of Cloth", "art": "rohstoff", "rohstoff": "cloth", "preis": 15, "wo": ["toto"], "wenn": {"alle": _OFFEN},
                                "text": "Plain linen that fell off a ferry, according to the man selling it. Danzel doesn't ask which ferry."}
MODUL["items"]["corsican_wool"] = {"label": "Corsican Wool", "art": "rohstoff", "rohstoff": "wool", "preis": 15, "wo": ["danzel"], "wenn": _GHJUVAN,
                                   "text": "Sheared on the high pasture and carried down in a sack. It keeps out everything except the smell of sheep."}
MODUL["items"]["import_wool"] = {"label": "Import Wool", "art": "rohstoff", "rohstoff": "wool", "preis": 40, "wo": ["toto"], "wenn": {"alle": _OFFEN + [{"nicht": _GHJUVAN}]},
                                 "text": "Good Scottish wool at a very bad price. Nobody on this island sells any cheaper now."}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ereignisse_schneider as _sn  # noqa: E402
MODUL["schneider"] = _sn.DATEN
for _p, _f in _sn.SET_FREI.items():
    MODUL["personen"][_p]["set_frei"] = _f
MODUL["personen"]["maxwell"]["set_frei"] = [{"flag": "steel_mop", "set": "maximum_steelmop"}]   # Rosis Uebergabe, Tag 19 (Duc 01.11.2026)
# Geld (18.10.2026, Messung tests\geld_messung.py): mehr zum Start, damit der erste Ladenbesuch kein Frust ist;
# weniger Gage, weil am Wochenende sonst ueber 1.500 EUR ungenutzt bleiben
# Duc 28./29.10.2026 (beute.md 3a, Brain Trust): Gage halbiert auf 125 EUR - Megans Probezeit (mg_tag2); Geld kommt jetzt auch
# von menschlichen Gegnern (kaempfe.json geld_drop) und aus Wertsachen. Ziel: Kaeufer hat an Tag 14 300-800 EUR (geld_messung.py).
MODUL["geld"] = dict(MODUL["geld"], start=400, honorar=125, honorar_text="Eden Group fee (probation rate)")
# Tasche 8 / 12 / 16 (Duc 29.10.2026, beute.md 5): je Akt ein Upgrade bei Rosi, nur gegen Geld, sofort fertig
MODUL["tasche"] = {
    "start": 8, "flag": "werkstatt_offen", "text_zu": "The workshop is still wrecked after the explosion.",
    "stufen": [
        {"plaetze": 12, "geld": 400, "ab_tag": 8, "label": "Rosi's Diving Bag",
         "text": "Cut from an old dive suit and a tender cover, stitched twice where it matters. It smells of neoprene and holds four more things than it should.",
         "text_frueh": "Rosi wants to cut it from the old dive gear. Ask her again next week.",
         "satz": "Neoprene, double seams, a pocket for your phone. If it tears, you were carrying a boar."},
        {"plaetze": 16, "geld": 800, "ab_tag": 24, "label": "Rosi's Expedition Pack",
         "text": "A frame pack built around a tender's spare hull rib. Rosi signed the inside flap, in case anyone forgets whose work it is.",
         "text_frueh": "Rosi has the frame on her bench, but she won't finish it before the siege is over.",
         "satz": "Sixteen slots, a frame that won't bend, and my name inside. Bring it back full, Maestro."},
    ],
}
# Schnelljobs (Handy-Reiter Jobs) abgeschaltet (Duc 29.10.2026): die Favours ersetzen sie (kern\handel.jobs_aktiv).
# missionen.json und der Job-Code bleiben, damit sich das umkehren laesst - hier auf True setzen und neu bauen.
MODUL["schnelljobs"] = False
# Laden-Regeln (18.10.2026 aus kern\handel.py in die Daten verschoben, Werte unveraendert; Schema in kern\rollen.py)
MODUL["laeden"]["toto"].update(wechselnd=True, immer=["espresso"], sonderangebot=True)
# Feste Ware (kern\handel.sortiment, "fest"): die zwoelf einzigartigen Geschenke, frueher Lohn der Schnelljob-Ketten
# (Duc 29.10.2026, Schnelljobs abgeschaltet). Immer im Angebot, ausserhalb der Rotation, ab Totòs Vertrauen 3 (quelle toto3).
MODUL["laeden"]["toto"]["fest"] = ["chiara_tasse", "rosi_schild", "sophia_fueller", "lea_tauchcomputer", "siri_ratgeber",
                                   "lola_vegemite", "alva_kastagnetten", "toto_gennaro", "yasin_goldbrille",
                                   "elsa_strafzettelblock", "petru_tabak", "casanova_kanone"]
MODUL["laeden"]["toto"].update(name="Totò's Locker",               # English place name (26.10.2026, STIL.md)
                               text="A locked locker in the store room. Totò has everything, almost. The better you know him, the better the price.")
MODUL["laeden"]["alva"].update(wechselnd=True, immer=["espresso"], handel_punkte=True,
                               rabatt_je_stufe=[0.04, 1])     # Diesel unter der Theke entfaellt seit 30.10.2026
MODUL["laeden"]["lola"].update(wechselnd=True, immer=[], essen=True, zweites_essen_ab=3)   # ab Lolas Vertrauen 3 zwei Essen
MODUL["laeden"]["megan"].update(rabatt_ab_vertrauen=[3, 0.85],                   # Eden-Shop zeigt immer alles
                                ab_tag=8)                                          # oeffnet erst in Akt 2 (Duc 27.10.2026)

# Feste Saetze des Haendlers (seit 26.10.2026 in haendler_toto.py: 6 Vertrauensstufen x 8 Gruesse, Reaktionen je Kategorie,
# wahre Geschenk-Hinweise; Sprite-Gefuehle je Satz).
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from haendler_toto import TOTO_ZEILEN, TOTO_GEFUEHL, FALLBACK_GEFUEHL  # noqa: E402
MODUL["laeden"]["toto"].update(hintergrund="eden_rise_toto_spind.png", haendler_zeilen=TOTO_ZEILEN,
                               haendler_gefuehl=TOTO_GEFUEHL)


# Duc 02.11.2026: je Figur und Quelle ein Topf (Vertrauen, Begehren), Summe ueber 100, unsichtbar. Startwerte von Character Design.
# Duc 02.11.2026 (Brain-Trust-Runde Orte): Risiko 0-3 je Tageszeit, eigener Ort je Frau ab Vertrauen 4, gemeinsame Orte.
# Neue Orte (tenderboot, alvas_hinterzimmer, mochis_bucht, kuehlraum, genueser_turm) kommen erst mit ihrem Bild in die Raeume.
MODUL["orte"] = {
    "risiko": {"duc_cabin": {"*": 0}, "solar_deck": {"*": 1}, "tender_garage": {"*": 1}, "workshop": {"*": 1},
               "generator_room": {"*": 2}, "sun_deck": {"*": 3, "abend": 2, "nacht": 2}, "swim_platform": {"*": 3, "nacht": 2},
               "foredeck": {"*": 3, "nacht": 2}, "petru_workshop": {"*": 3}, "galley": {"*": 3, "nacht": 2}, "vip_cabin": {"*": 3},
               "bridge": {"*": 3, "nacht": 1}, "aft_deck": {"*": 3, "nacht": 1}, "alvas_bar": {"*": 3, "nacht": 1},
               "tenderboot": {"*": 1}, "alvas_hinterzimmer": {"*": 2}, "mochis_bucht": {"*": 2}, "kuehlraum": {"*": 3},
               "genueser_turm": {"*": 3}, "crew_kabine_1": {"*": 3}, "crew_kabine_2": {"*": 2}, "crew_kabine_3": {"*": 1},
               "spare_cabin": {"*": 0}, "bibi_haeuschen": {"*": 1}, "megan_kabine": {"*": 1}, "crew_dusche": {"*": 0},
               "yacht_toilette": {"*": 0}},
    "eigen": {"chiara": {"ort": "bridge", "phasen": ["abend", "nacht"]}, "rosi": {"ort": "generator_room"},
              "lea": {"ort": "tenderboot"}, "siri": {"ort": "solar_deck"}, "lola": {"ort": "aft_deck", "phasen": ["abend", "nacht"]},
              "sophia": {"ort": "alvas_bar", "phasen": ["nacht"]}, "alva": {"ort": "alvas_hinterzimmer"},
              "bibi": {"ort": "mochis_bucht", "phasen": ["abend", "nacht"]}},
    "gemeinsam": ["duc_cabin", "solar_deck", "tender_garage", "workshop", "generator_room", "sun_deck", "swim_platform",
                  "foredeck", "galley", "petru_workshop", "kuehlraum", "genueser_turm", "crew_dusche", "yacht_toilette",
                  {"ort": "vip_cabin", "nur": ["siri"], "flag": "siri_frei"}],
    # Ihr Zimmer (welt/wohnen.md): Risiko kommt von der Mitbewohnerin. Erste passende Zeile gilt (Spare Cabin nach gv_gute_kabine).
    "zimmer": {"sophia": [{"ort": "spare_cabin", "flag": "kabine_sophia"}, {"ort": "crew_kabine_1"}], "lea": [{"ort": "crew_kabine_1"}],
               "lola": [{"ort": "spare_cabin", "flag": "kabine_lola"}, {"ort": "crew_kabine_2"}], "jana": [{"ort": "crew_kabine_2"}],
               "chiara": [{"ort": "crew_kabine_3"}], "rosi": [{"ort": "crew_kabine_3"}], "alva": [{"ort": "alvas_hinterzimmer"}],
               "bibi": [{"ort": "bibi_haeuschen", "flag": "mochis_offen"}], "siri": [{"ort": "vip_cabin", "flag": "siri_frei"}],
               "megan": [{"ort": "megan_kabine", "flag": "megan_zurueck"}]}}

MODUL["toepfe"] = {
    "rosi": {"szenen": (50, 45), "handy": (10, 15), "geschenke": (10, 10), "events": (45, 45)},
    "chiara": {"szenen": (40, 40), "handy": (20, 25), "geschenke": (20, 15), "events": (40, 40)},
    "lola": {"szenen": (40, 40), "handy": (25, 25), "geschenke": (25, 25), "events": (30, 30)},
    "sophia": {"szenen": (40, 40), "handy": (15, 20), "geschenke": (15, 15), "events": (45, 45)},
    "lea": {"szenen": (45, 40), "handy": (15, 20), "geschenke": (15, 15), "events": (40, 40)},
    "siri": {"szenen": (50, 50), "handy": (20, 20), "geschenke": (5, 10), "events": (40, 40)},
    "alva": {"szenen": (45, 40), "handy": (10, 20), "geschenke": (25, 20), "events": (35, 35)},
    "bibi": {"szenen": (45, 45), "handy": (10, 15), "geschenke": (20, 10), "events": (50, 50)},
    "jana": {"szenen": (40, 0), "handy": (20, 0), "geschenke": (20, 0), "events": (40, 0)},
    "megan": {"szenen": (45, 0), "handy": (30, 0), "geschenke": (5, 0), "events": (40, 0)},
    "sirene": {"szenen": (50, 0), "handy": (0, 0), "geschenke": (35, 0), "events": (35, 0)}}

# ------------------------------------------------------------------ Rollen und Sonderregeln (18.10.2026)
# Bis hierhin standen diese Figuren fest im Kern; jetzt liest der Kern sie aus den Daten (kern\rollen.py).
MODUL["rollen"] = {
    "haendler": "toto", "dorfohr": "alva", "tratsch": ["alva", "toto"],
    "crew": ["chiara", "sophia", "lea", "rosi"], "nicht_crew": ["toto"], "nicht_in_crew_szene": ["siri"],
    # Spieltest 29.10.2026: auch Holm, Maxwell, Totò, Petru und Jana bekommen freie Zeit (hauptstory.frei_phase)
    "freie_zeit_extra": ["lola", "alva", "holm", "maxwell", "toto", "petru", "jana", "sirene", "bibi"], "isst_mit": ["lola"],
    "partner_standard": "chiara",
    "nur_anruf": {"vogel": "Katrin Vogel"},   # Anruferin ohne Bild und Personeneintrag (Personalberaterin, Koeln)
}
P["holm"].update(immer_erreichbar=True, keine_nebenfigur=True)
# Eigene Gesten statt Floskeln (Spieltest 29.10.2026: "lets out a ..." in 80 von 318 Antworten). Aus den Wiki-Seiten
# docs/wiki/figuren/<id>.md (Stimme, Fakten); kern/szene.figur_prompt gibt sie dem Modell, hoechstens eine pro Antwort.
GESTEN = {
    "chiara": ["rates something out loud on a scale of ten", "hugs someone in the middle of a sentence",
               "hands somebody a job the moment she feels unsure", "orders in proud, slightly wrong Italian"],
    "lola": ["talks with her hands and her wooden spoon", "starts a sentence and loses the end of it",
             "laughs at her own joke before anyone else does", "pads around barefoot, tasting something off a spoon"],
    "rosi": ["talks to a machine instead of about herself", "shouts an attack name at the torque wrench",
             "wipes oily hands on her trousers", "flares up for ten seconds, then is calm again"],
    "siri": ["apologises to a piece of furniture", "slips into her bright camera voice, then drops back into her real one",
             "laughs at herself before anyone else can", "asks a question nobody would ask Siri Sea"],
    "alva": ["polishes a glass that is already clean", "rests a hand on the old jukebox that has been silent since Papa died",
             "listens longer than she talks, then says the one line that lands", "slides a drink across the bar unasked"],
    "sophia": ["writes something in her small brown leather notebook and never says what",
               "lets a sentence sit in silence", "offers a bet when she's cornered", "straightens someone's collar"],
    "megan": ["pauses like a villain before the last word", "moves a chess piece in her head - and says so",
              "names the price of a favour", "never raises her voice; it gets quieter instead"],
    "lea": ["salutes when she's nervous", "sketches a fish on whatever paper is near",
            "drops a sea fact nobody asked for", "gets faster when she's nervous and her facts go wrong"],
    "holm": ["drinks her coffee black and cold and says nothing", "checks something off on a clipboard",
             "says 'Takk' and nothing else", "says the important thing exactly once"],
    "maxwell": ["talks about himself in the third person", "does a push-up to punctuate a joke",
                "strikes a heroic pose", "goes quiet and gentle when it's serious"],
    "toto": ["eats something while he talks", "talks with his hands, gold chain swinging", "offers odds on anything",
             "jingles the keys of his locked locker"],
    "petru": ["mends a net that isn't torn", "says 'Hm.' and lets it mean something",
              "nods once - that is praise", "turns the radio a little louder instead of answering"],
    "jana": ["says sorry to a door", "tightens her ponytail", "ties a knot without looking", "borrows one of Chiara's lines "
             "and gets it slightly wrong"],
    "yasin": ["films everything on his phone", "checks his expensive watch", "calls something 'content'",
              "says one honest sentence and covers it with a grin"],
    "yamamoto": ["bows a little too deeply", "says 'So sorry' when nothing happened", "leaves the joke unsaid",
                 "holds his glass very carefully, as if it might change him"],
    "elsa": ["writes it down as if dictating a report", "asks for facts, not opinions",
             "taps her pen on her notebook", "breaks her calm only to shout for Totò"],
}
GESTEN["sirene"] = ["rests her arms on the edge of the pool like a girl on a windowsill",
                     "hums when she doesn't want to answer", "lets the water rise to her chin when she's hurt",
                     "trails her fingers through the water and watches the rings"]
for _pid, _g in GESTEN.items():
    P[_pid]["gesten"] = _g
# Ligeia als NPC (29.10.2026): nachts am Teich, Geschenke zaehlen auf ihr Vertrauen (handel.schenken_npc)
P["sirene"].update({
    "ablauf": {"abend": "siren_pool", "nacht": "siren_pool"}, "keine_nebenfigur": True, "frei_immer": True,
    "geschenk_reaktion": [None, "She turns it over in the moonlight as if nobody has given her anything in a very long "
                                "time. She reacts in character: teasing if it bores her, very quiet if it touches her. "
                                "She stays in the water."]})
P["megan"].update(immer_erreichbar=True,
                  ruft_nicht_an_wenn={"alle": [{"flag": "megan_besuch"}, {"nicht": {"flag": "megan_abgereist"}}]})
P["siri"]["vergeben"] = {"bis_flag": "siri_frei", "grund": "she is still with Yasin"}
P["rosi"]["technik"] = True
# Rosis ST-Sets heissen seit 23.10. anders (rosi_claude_biker ...); Events und set_standard nennen die alten Namen
# (Duc 25.10.2026: Zuordnung an einer Stelle statt 51 Ersetzungen, aufgeloest in kern/buehne.SetListe)
P["rosi"]["set_alias"] = {"Engine Room": "rosi_claude_biker", "Off Duty": "rosi_lounge_set", "Swim": "rosi_swim",
                          "Crew Party": "rosi_crew_party"}
P["elsa"]["set_frei"] = [{"flag": "elsa_kampfuniform", "set": "elsa_combat"}]     # von ihrem Angebot an Tag 20 bis zum Ende der Belagerung
P["elsa"]["bestechung"] = {"ab": 50, "regie": "Duc offers her something valuable: %s. That looks like a bribe to a "
                                              "gendarme. She refuses it - sharp or drily amused - hands it back and "
                                              "makes a note of it."}
for _pid, _r in {
    "toto": ["draht", "Toto takes it, appraises it like a fence - weight, value, who would buy it - and is touched "
                      "anyway, though he would never say so directly."],
    "alva": ["ruf", "Alva takes it with a knowing grin and a teasing remark; by tomorrow the whole village will know."],
    "petru": ["ruf", "Petru turns it over in his hands, says almost nothing, and nods once. For him that is a lot."],
    "casanova": ["ruf", "The mayor reacts as if she had been given a national honour - gasps, poses, a little speech."],
    "yasin": [None, "Yasin takes it, films it immediately and turns the moment into content about himself."],
    "elsa": [None, "Elsa accepts the small gift with a dry remark and puts it away, a little amused."],
}.items():
    P[_pid]["geschenk_reaktion"] = _r
MODUL["migration"] = {"ersetzt": {"paoli": "elsa"}, "umbenannt": [["LULU", "ALVA"], ["Lulu", "Alva"], ["lulu", "alva"]]}
MODUL["ermittlung"] = {
    "verdacht": ["chiara", "sophia", "rosi", "lea", "yasin"], "verdacht_ohne_fall": ["chiara", "sophia", "rosi"], "ersatz": "rosi",
    # Wer etwas Wahres weiss, sagt es ab dieser Vertrauensstufe (sonst 2): Behoerde und Fachmann sofort, Gaeste ab 1
    "schwelle": {"holm": 1, "lola": 1, "toto": 1, "elsa": 0, "petru": 0, "megan": 1, "casanova": 1, "yasin": 1,
                 "alva": 1},
}


# Figuren ohne Raum an Bord (29.10.2026, Spieltest „9 nachziehen“): vorhandener Hintergrund fuer Profil und Missionen
# (eden.py nimmt ihn, wenn die Figur gerade in keinem Raum ist). Abnahme docs/abnahme/item_nachzug.html.
HINTERGRUND = {
    "megan": "eden_hq_megan_office.png", "nonna": "eden_rise_monastery_kitchen.png",
    "isabelle": "eden_rise_monastery_garden_dusk.png", "frederico": "eden_rise_monastery_gate.png",
    "laetitia": "eden_rise_mountain_lake.png", "adrien": "eden_rise_abandoned_mountain_hut.png",
    "wolff": "eden_rise_genoese_tower_camp.png", "ghjuvan": "eden_rise_bergerie_interior.png",
    "dumenica": "eden_rise_mazzera_hut.png", "gennaro": "eden_rise_gennaro_cell.png",
    "matteu": "eden_rise_grotto_steps.png", "chloe": "eden_rise_treasure_camp.png",
    "riscossore": "eden_rise_smugglers_tunnel.png", "sirene": "eden_rise_underground_pool_tide.png",
}


def main():
    for _pid, _bg in HINTERGRUND.items():
        if _pid in MODUL["personen"]:
            MODUL["personen"][_pid]["hintergrund"] = _bg
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    MODUL["laeden"]["toto"]["fest"] = MODUL["laeden"]["toto"]["fest"] + ["cloth_bolt", "import_wool"]   # Stoff immer im Angebot (Danzels Auftraege)
    json.dump(MODUL, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben: %s | %d Personen, %d Raeume, Persona %s" % (ZIEL, len(MODUL["personen"]), len(MODUL["raeume"]),
                                                                   MODUL["personas"][0]["id"]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

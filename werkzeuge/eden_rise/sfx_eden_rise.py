# -*- coding: utf-8 -*-
r"""Sound-Effekte fuer eden_rise (18.10.2026) - Katalog als Daten. Zweite Runde (18.10.): die 30 wichtigsten, je 4 Varianten. Alle Effekte sind EINMALIG (keine Schleife), vorab erzeugt und als Datei gespeichert (nie live).

Je Effekt: id, wofuer (deutsch, fuer die Uebersicht), prompt (englisch, fuer ElevenLabs), dauer (Sekunden, 0.5-30),
varianten (wie viele Dateien - das Spiel wechselt spaeter zwischen ihnen), gruppe (ui / effekt), einfluss
(prompt_influence 0-1: hoeher = naeher am Text, weniger Zufall), wahl (von Duc gewaehlte Variante, None = offen).

Dritte Runde (18.10.): Duc hat 18 Varianten gewaehlt (wahl), 12 Effekte haben neue Prompts und werden neu erzeugt.

    python sfx_eden_rise.py        -> module\eden_rise\sfx.json
Erzeugen: Sfx_EdenRise.bat (werkzeuge\eden_rise\sfx_erzeugen.py) - ueberspringt Vorhandenes.
"""
import json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
ZIEL = os.path.join(EDEN, "module", "eden_rise", "sfx.json")

STIL = ("clean, high quality game sound effect, no music, no voices, dry, short tail")
# Fuenfte Runde (18.10.): Duc fand die Toene zu kurz -> doppelte Laufzeit und ausklingen lassen statt "short tail".
STIL_LANG = ("clean, high quality game sound effect, no music, no voices, natural full ringing tail that fades out")


def S(id, wofuer, prompt, dauer, gruppe="effekt", varianten=4, einfluss=0.5, wahl=None, lang=False, konzepte=None,
      stil=None, mehrfach=False):
    """konzepte = [(Name, Prompt), ...]: jede Variante bekommt ihren eigenen Prompt (mehr Vielfalt als Zufall allein).
    stil ersetzt den Standard-Zusatz - noetig, wenn ein Effekt Musik (Jingle) oder eine Stimme (Mhmm) braucht.
    mehrfach: Duc darf mehrere Varianten waehlen (wahl = Liste), das Spiel wechselt zwischen ihnen (Abwechslung)."""
    stil = ", " + (stil or (STIL_LANG if lang else STIL))
    s = {"id": id, "wofuer": wofuer, "prompt": prompt + stil, "dauer": dauer, "mehrfach": mehrfach,
         "varianten": varianten, "gruppe": gruppe, "einfluss": einfluss, "schleife": False, "wahl": wahl}
    if konzepte:
        s["varianten"] = len(konzepte)
        # (Name, Prompt) oder (Name, Prompt, Dauer) - eine eigene Dauer gilt nur fuer diese Variante
        s["konzepte"] = [dict({"name": k[0], "prompt": k[1] + stil}, **({"dauer": k[2]} if len(k) > 2 else {}))
                         for k in konzepte]
    return s


# Siebte Runde (18.10.): ui_klick - Natur/Retro (Runde 6) verworfen; Duc will modern und satt: tiefer runder Koerper
# plus klarer kurzer Anschlag, eine Variante je Konzept.
KLICK = ("single very short modern user interface click, rich and full-bodied, deep rounded low end with a crisp clean "
         "attack, tight and punchy, satisfying, no ringing")
_KLICK_IDEEN = {
    "Premium-App": "a premium smartphone app button tap, soft deep thump layered with a tiny crisp tick, " + KLICK,
    "Haptik": "a haptic touchscreen keyboard tap, muted low thud with a polished click on top, " + KLICK,
    "Auto-Knopf": "a premium car infotainment button press, solid damped click, expensive and precise, " + KLICK,
}
# Achte Runde (19.10.): Duc mochte 1 Premium-App, 2 Haptik, 6 Auto-Knopf -> je 4 Varianten. Verworfen: Mech. Taste,
# Juicy Pop, Glas-Touch, Konsole, Synth-Tap.
# Neunte Runde (19.10.): Auto-Knopf 3 und 4 sind nah dran -> beide behalten (Variante 1/2), dazu 4 neue Wuerfe mit
# demselben Prompt und je 2 Nuancen (tiefer/weicher, knackiger/kuerzer). Premium-App und Haptik raus.
_AUTO = _KLICK_IDEEN["Auto-Knopf"]
_AUTO_TIEF = ("a premium car infotainment button press, solid damped click with a slightly deeper and softer body, "
              "expensive and precise, " + KLICK)
_AUTO_KNACKIG = ("a premium car infotainment button press, solid damped click, slightly crisper and tighter, very "
                 "short, expensive and precise, " + KLICK)
KLICK_KONZEPTE = ([("Auto-Knopf 3 (behalten)", _AUTO), ("Auto-Knopf 4 (behalten)", _AUTO)]
                  + [("Auto-Knopf neu %d" % n, _AUTO) for n in range(1, 5)]
                  + [("Auto · tiefer %d" % n, _AUTO_TIEF) for n in (1, 2)]
                  + [("Auto · knackiger %d" % n, _AUTO_KNACKIG) for n in (1, 2)])


SFX = [
    # ---------------------------------------------------------------- Oberflaeche
    S("ui_meldung", "Allgemeine Meldung (Toast oben in der Mitte)",
      "soft elegant user interface notification chime, two gentle glassy notes, warm and premium, luxury yacht app",
      1.2, "ui", einfluss=0.6, wahl=3),
    S("handy_nachricht", "Neue Nachricht im Handy",
      "smartphone vibrating on a wooden table, a pleasant warm low buzz in two short smooth pulses, soft and rounded, "
      "no ping, no beep", 1.2, "ui", einfluss=0.6, wahl=4),
    S("vorliebe_entdeckt", "Lavendel-Meldung: Vorliebe entdeckt",
      "gentle pleasant discovery chime, soft warm bells rising slowly, mellow and harmonious, calm and tender, "
      "no harsh high frequencies, visual novel affection sound", 1.8, "ui", einfluss=0.6, wahl=3),
    S("ui_klick", "Auswahl bestätigen (Antwort, Knopf, Ort)",
      "single deep satisfying user interface click, full-bodied and solid, soft thock like a premium mechanical "
      "keyboard key, warm low end, no ringing", 0.5, "ui", einfluss=0.75, konzepte=KLICK_KONZEPTE,
      wahl=2),
    # Vierte Runde (18.10.): plus/minus als Spiegelpaar - gleiche Instrumente, gleiche Laenge, nur die Richtung kehrt um.
    S("vertrauen_plus", "Vertrauen steigt",
      "rich full-bodied two-note affection chime, a warm low note rising to a higher note a major third above, "
      "felt piano and soft marimba layered with a gentle warm bloom, heart-warming like a relationship level up "
      "in Persona or Stardew Valley, round and satisfying", 3.0, "ui", einfluss=0.7, lang=True, wahl=4),
    S("vertrauen_minus", "Vertrauen sinkt",
      "rich full-bodied sad two-note chime in a minor key, a higher note falling to a lower note, the lower note "
      "sits inside a dark minor chord, felt piano and soft marimba, muted, melancholic and wistful, clearly minor "
      "and sorrowful, no major chord, no bright or happy tones, like losing affection in Persona, round and soft, "
      "not harsh", 3.0, "ui", einfluss=0.8, lang=True, wahl=2),
    S("geld_ein", "Geld erhalten (Lohn, Verkauf)",
      "a few gold coins dropping into a leather pouch with a soft bright jingle, satisfying reward", 1.5, "ui", wahl=3),
    S("geld_aus", "Geld ausgeben (Kauf)",
      "paper banknotes counted quickly then a small cash drawer closing with a short bell, a purchase being completed",
      1.5, "ui", wahl=4),
    S("item_erhalten", "Gegenstand erhalten",
      "satisfying two-note item pickup sound, a soft round pop then a bright higher chime, crisp and rewarding, "
      "small sparkle, video game item acquired", 1.2, "ui", einfluss=0.7, wahl=1),
    S("mission_neu", "Neue Mission angenommen",
      "short intriguing notification, a soft low pluck followed by a rising glassy shimmer, quest accepted", 1.6,
      "ui", einfluss=0.6, wahl=2),
    S("mission_erfolg", "Mission geschafft",
      "short satisfying quest complete jingle, warm bright bell notes resolving upwards, rewarding but understated",
      2.0, "ui", einfluss=0.6, wahl=1),
    # Spiegel zu mission_erfolg (Variante 1): gleiche warme Glocken, aber abwaerts und gedaempft.
    S("mission_fehlschlag", "Mission fehlgeschlagen",
      "short quest failed jingle, warm muted bell notes falling downwards and settling low on a soft minor chord, "
      "full and heavy, disappointing but understated, the mirror image of a quest complete jingle, like a failed "
      "quest in The Witcher 3 or Zelda", 4.0, "ui", einfluss=0.6, lang=True, wahl=3),
    S("tag_beginnt", "Neuer Tag beginnt (Morgen auf der Yacht)",
      "calm harmonious morning at sea, a soft warm ship's bell ringing twice in tune, gentle waves lapping, "
      "peaceful and melodic, no seagull screeches", 3.0, "ui", einfluss=0.6, wahl=3),
    # ---------------------------------------------------------------- Wuerfel (wie BG3)
    S("wuerfel_rollen", "Würfel rollt (jede Probe)",
      "a single heavy twenty-sided resin die thrown onto a wooden table, rolling and tumbling, then settling", 1.8,
      gruppe="wuerfel", wahl=3),
    # Erfolg/Fehlschlag als Spiegelpaar (wie Baldur's Gate 3): gleicher Wuerfel-Aufschlag, gleiche Glocken, gleiche
    # Laenge - Erfolg steigt in Dur, Fehlschlag faellt in Moll.
    S("wuerfel_erfolg", "Probe gelungen (normaler Erfolg)",
      "a heavy resin die landing on a wooden table with a solid deep knock, then a rich resonant success chime, two "
      "warm bell notes rising a major fifth, full-bodied with a soft shimmer, satisfying like a skill check "
      "success in Baldur's Gate 3", 3.2, einfluss=0.7, gruppe="wuerfel", lang=True, wahl=4),
    S("wuerfel_fehlschlag", "Probe misslungen (normaler Fehlschlag)",
      "a heavy resin die landing on a wooden table with a solid deep knock, then a rich resonant failure tone, two "
      "low bell notes falling a minor third, full-bodied but muted and heavy, like a skill check failure in "
      "Baldur's Gate 3", 3.2, einfluss=0.7, gruppe="wuerfel", lang=True, wahl=3),
    S("wuerfel_kritisch", "Kritischer Erfolg (natürliche 20, Sonnenanker)",
      "triumphant short magical success stinger, bright shimmering sparkle and a warm brass hit, tabletop RPG "
      "critical success", 2.0, gruppe="wuerfel", wahl=1),
    S("wuerfel_patzer", "Patzer (natürliche 1, gebrochener Anker in Flammen)",
      "a heavy die lands with a deep thud and a dark low brass hit, then something bursts into flames with a deep "
      "fiery whoosh, roaring crackling fire and sizzling embers, a low ominous boom underneath, weighty and "
      "dramatic, the dark mirror of a critical success stinger, critical fumble", 5.0, einfluss=0.6,
      gruppe="wuerfel", lang=True, wahl=1),
    # ---------------------------------------------------------------- Laeden und Story
    S("lola_brutzeln", "Lolas Kombüse: beim Kauf brutzelt es",
      "food sizzling loudly as it hits a hot oiled frying pan in a small galley kitchen, then a spatula scrape", 2.0,
      wahl=1),
    S("hubschrauber_holm", "Rettungshubschrauber holt Holm (Tag 2)",
      "rescue helicopter approaching over the open sea and hovering above a yacht, rotor wash and wind, urgent but "
      "calm, distant", 6.0, wahl=3),
    S("hubschrauber_megan", "Megans Hubschrauber landet auf dem Sonnendeck (Tag 5)",
      "sleek corporate helicopter landing on a yacht helipad, rotors spinning down, powerful and imposing, then the "
      "turbine winding down", 6.0, wahl=4),
    S("blackout", "Blackout: Strom fällt aus",
      "electrical hum of a ship suddenly cutting out, heavy relay clunk, lights powering down with a falling whine, "
      "then silence", 3.0, wahl=1),
    S("strom_zurueck", "Strom kommt zurück",
      "a ship's diesel generator trying to start, the engine sputtering and stalling twice, then catching and "
      "running steadily, electrical hum rising, lights clicking back on", 6.0, wahl=3),
    S("sturm_nacht", "Sturmnacht: Donner und Wind über der Yacht",
      "night storm at sea, a rolling thunderclap, howling wind, rain hammering on a ship deck, hull creaking", 6.0,
      wahl=4),
    S("ankerkette", "Ankerkette rasselt (Anker lichten, Ankerwache)",
      "heavy anchor chain rattling and clanking through a metal hawsepipe on a yacht, winch motor whining", 4.0,
      wahl=4),
    S("tuer_klopfen", "Jemand klopft an Ducs Kabinentür (Nachtbesuch)",
      "three soft knocks on a solid wooden cabin door, quiet and hesitant, small room, a faint ship hum", 1.5, wahl=2),
    S("glaeser_anstossen", "Gläser klingen (Dinner, Festa, Toast)",
      "four crystal wine glasses clinking together in a festive toast, many bright clear glass clinks close to the "
      "microphone, rich full glassy ringing resonance that lingers, cheers at a dinner table", 4.0, einfluss=0.7,
      lang=True, wahl=1),
    S("sektkorken", "Sektkorken knallt",
      "champagne bottle cork popping loudly with a fizzy hiss, then wine pouring into glasses, party mood", 2.0,
      wahl=4),
    S("tender_motor", "Beiboot (Tender) startet und fährt ab",
      "small outboard boat engine starting with a sputter, then revving and pulling away across water", 4.0, wahl=3),
    S("wasser_platsch", "Platschen ins Wasser (Drohne, Sprung, Plattform)",
      "an object splashing into the sea off a yacht swim platform, a big splash and bubbles, waves lapping", 2.0,
      wahl=3),
    S("funk_rauschen", "Funk knackt (Bordfunk, Küstenwache)",
      "marine VHF radio squelch click followed by static crackle and a brief radio beep, tinny and realistic, no "
      "speech", 2.0, wahl=3),
    # ---------------------------------------------------------------- Weitere Anlaesse (19.10.): haeufige Momente ohne Ton
    # Zweite Runde (19.10.): Duc wollte Jingle statt Whoosh, kein Auspacken, mehr Kauen mit "mhmm", neue Event-Stinger.
    S("geschenk", "Geschenk überreicht",
      "very gentle heartwarming gift given sound, a soft quiet harp glissando drifting up into a tender muted bell "
      "chime and a faint warm glow, delicate and soothing, affectionate, like giving a gift in a cozy dating sim, "
      "soft and round", 2.5, "mehr", einfluss=0.7, lang=True, wahl=4),
    S("kochen", "Duc kocht selbst",
      "home cooking in a small galley kitchen, quick knife chopping on a wooden board, then ingredients hitting a hot "
      "pan with a big appetizing sizzle, rich and full", 3.0, "mehr", wahl=1),
    S("item_benutzen", "Snack essen / Gegenstand benutzen",
      "an adult man quietly enjoying a tasty snack, first a soft bite and calm satisfied chewing, then at the very "
      "end a quiet low male closed-mouth hum 'mmhmm' of enjoyment, all at a gentle low volume, deep masculine voice, "
      "cozy", 2.5,
      "mehr", einfluss=0.75, wahl=1,
      stil="clean, high quality game sound effect, no music, no words, only chewing and a short low male hum, short tail"),
    S("hinweis_gefunden", "Hinweis gefunden (neuer Codex-Eintrag)",
      "intriguing clue discovered stinger, a deep soft piano note with a mysterious rising shimmer and a subtle low "
      "string swell, like finding evidence in Ace Attorney or a detective game, rich and full", 2.5, "mehr",
      einfluss=0.6, lang=True, wahl=3),
    S("nicht_moeglich", "Geht nicht (zu wenig Geld/Energie, Aktion abgelehnt)",
      "soft modern denied user interface sound, two short low muted taps falling in pitch, gentle not harsh, like a "
      "locked option in a modern game menu, rich and round", 0.8, "mehr", einfluss=0.7, wahl=2),
    S("begehren_plus", "Begehren steigt",
      "sensual warm two-note chime rising, soft breathy pad with a low velvety bass and a subtle heartbeat, intimate "
      "and romantic, like a romance meter rising in a dating sim, rich and full-bodied", 3.0, "mehr", einfluss=0.7,
      lang=True, wahl=4),
    # ---------------------------------------------------------------- Tag 0 (25.10.): Hangar in Antibes, je Event ein Ton
    # Tonliste aus docs/wiki/welt/drehbuch_tag0.md; Hallen-Atmo steckt in der Limousine, die Palette im Hubschrauber-Ueberflug.
    S("limousine_ankunft", "Tag 0: Limousine rollt in die Halle, Tür fällt ins Schloss",
      "large open shipyard hangar by the sea at dawn, distant seagulls and harbour water, a heavy luxury car rolls in "
      "slowly over concrete and stops, engine idles off, a solid heavy car door shuts with a deep satisfying thud",
      6.0),
    S("klemmbrett_schritte", "Tag 0: Megan kommt mit Klemmbrett (Schritte auf Beton)",
      "confident footsteps of a woman in boots approaching on a bare concrete hangar floor with light echo, she stops, "
      "a pen clicks and a clipboard clip snaps shut", 3.0),
    S("kaffee_schluerfen", "Tag 0: Holm schlürft kalten Kaffee",
      "one slow unimpressed sip of coffee from a metal mug, a short slurp, then the mug set down on a steel railing "
      "with a dull clink, outdoors by a harbour", 2.5),
    S("schraubenschluessel_klong", "Tag 0: Rosi unterm Heck (Generator, Schraubenschlüssel)",
      "a small diesel generator humming steadily in a big hangar, then a heavy steel wrench drops onto concrete with a "
      "loud ringing clang that echoes through the hall", 4.0),
    S("hubschrauber_ueberflug", "Tag 0: Palette ab, Hubschrauber donnert übers Hallendach (Maxwell)",
      "a heavy wooden pallet set down hard on a concrete floor with a deep thud, then a helicopter roars low over a "
      "metal hangar roof, the roof rattles, the rotor sound passes overhead and fades away", 6.0),
    S("katze_miau", "Tag 0: Die Kiste miaut (Jana)",
      "a small kitten meowing softly from inside a closed cardboard box, muffled, two short curious meows and a faint "
      "scratching on cardboard, quiet hangar room tone", 2.5),
    S("kamera_ausloeser", "Tag 0: Kamera klickt (Yamamoto, Yasin)",
      "a mechanical film camera shutter click and the film advance lever wound once, crisp and close, then a second "
      "quick shutter click", 1.5),
    S("hubschrauber_start", "Tag 0: Megans Hubschrauber hebt ab (Abschied)",
      "a corporate helicopter on a concrete apron starting its turbine, rotors spinning up, lifting off and flying "
      "away over the harbour, rotor sound fading into the distance with seagulls", 7.0),
    # ---------------------------------------------------------------- Hafenkampf (25.10.)
    S("rudel_ratten", "Hafenkampf: Welle 1 – Ratten-Rudel",
      "a swarm of rats rushing over wet cobblestones at a harbour, many tiny claws scratching and skittering, "
      "excited squeaking, a fish crate tipping over, close and chaotic", 4.0),
    S("rudel_hunde", "Hafenkampf: Welle 2 – Hunde-Rudel",
      "a pack of three feral dogs at a harbour, aggressive barking and low growling, paws running on stone, one dog "
      "snarling close to the microphone, tense and threatening", 4.0),
    S("keiler_ansturm", "Hafenkampf: Welle 3 – Keiler",
      "a huge wild boar coming down a narrow stone alley, heavy snorting and grunting, hooves pounding on cobblestones, "
      "a wooden barrel knocked over, powerful and menacing", 4.5),
    S("ziege_halsband", "Hafenkampf: Ziege mit blinkendem Halsband",
      "a goat bleating twice on a quiet harbour quay, a small electronic device on its collar beeping softly three "
      "times, light hooves on stone, slightly comical", 3.0),
    # ---------------------------------------------------------------- Anhoerung Tag 7 (26.10.)
    # eigene Toene statt geliehener Wuerfel-/Missionsklaenge (Ace-Attorney-Gefuehl); kern/anhoerung.py ruft sie auf
    S("anhoerung_hammer", "Anhörung: Megan spricht das Urteil (Holzhammer)",
      "a single heavy wooden gavel striking a hardwood sound block in a quiet wood-panelled salon, firm and final, "
      "deep resonant knock", 1.5, lang=True, einfluss=0.7),
    S("anhoerung_einspruch", "Anhörung: OBJECTION! (Duc legt eine Notiz vor)",
      "dramatic courtroom game stinger, a sharp orchestral hit with a punchy brass stab and a timpani boom, sudden "
      "and confident, like Ace Attorney objection", 1.5, einfluss=0.7,
      stil="clean, high quality game stinger, instrumental only, no voices, short tail"),
    S("anhoerung_slam", "Anhörung: Notizzettel knallt auf den Tisch",
      "a flat hand slamming a sheet of paper down hard on a wooden table, sharp paper slap and a dull wooden thud, "
      "close", 0.8, einfluss=0.7),
]

# Auslöser für Story-/Ort-Effekte (Einbau 18.10.): der Server meldet den Effekt, sobald diese Szene bzw. dieses Event
# beginnt (kern/sfx.py); "nach_szene" spielt, wenn die genannte Szene endet. Oberflaeche, Wuerfel, Geld, Vertrauen,
# Missionen usw. erkennt der Client selbst am Zustand (client/plugins/eden-sfx) - die stehen hier nicht.
# "kaempfe" spielt, wenn diese Begegnung beginnt (auch beim Neustart nach einer Niederlage).
# Szenen-IDs nur als Namen aus der Story nachgeschlagen (Spoilerregel: keine Inhalte).
# ------------------------------------------------------------------ Pixabay-Auswahl (Duc 27.10.2026)
# Fertige Dateien von pixabay.com (Pixabay Content License), geschnitten/kombiniert/angeglichen mit sfx_pixabay.py
# (Quellen: docs/abnahme/sfx_pixabay/fertig/QUELLEN.md). schleife=True: Hintergrund-Schleife (Ambience-Spur im Client).
def PX(id, wofuer, varianten=1, schleife=False, gruppe="effekt"):
    s = S(id, wofuer, "pixabay", 30 if schleife else 3, gruppe, varianten=varianten, wahl=list(range(1, varianten + 1)),
          mehrfach=True, stil="pixabay")
    s.update(prompt="pixabay", schleife=schleife, quelle="pixabay")
    return s


SFX += [
    PX("ereignis_jingle", "Ein Event beginnt: Studio Jingle (Duc 02.11.2026, statt Anime-Rock)"),
    PX("szene_vorhang", "Vorhang am Gespraechsende: Logo transition, Pixabay ejah_mu (K5, 02.11.2026)"),
    PX("szene_bruecke", "Zwischenkarte vor einem Event: Swoosh 03, Pixabay Universfield (K11, 02.11.2026)"),
    PX("tag_karte", "Tageskarte: Acoustic Guitar Logo, Pixabay Muzaproduct (K1, 02.11.2026)"),
    PX("kampf_schwung", "Kampf: Schlaeger ausholen"), PX("kampf_treffer", "Kampf: Treffer"),
    PX("kampf_parade", "Kampf: Parade (Block)"), PX("kampf_parade_perfekt", "Kampf: perfekte Parade"),
    PX("kampf_ausweichen", "Kampf: Ausweichen / daneben"), PX("kampf_sieg", "Kampf: Sieg"),
    PX("kampf_niederlage", "Kampf: Niederlage (Aufprall + Posaune)"), PX("level_up", "Level-Aufstieg / Punkt verteilt"),
    PX("anruf_klingeln", "Anruf klingelt (Handy-Event, Rast-Anruf); Marimba von Universfield, 4 s (Duc 03.11.2026)"),
    PX("notification", "Handy-Benachrichtigung, wenn das Handy zu ist", gruppe="ui"),
    PX("handy_senden", "Handy: Duc schickt eine Nachricht ab (lokal erzeugt mit werkzeuge/handy_senden_klang.py; Duc 03.11.2026: bleibt)", varianten=2, gruppe="ui"),
    # Handy aus einem Guss (Duc 03.11.2026, docs/abnahme/handy_klang.json): leise Toene -22 LUFS
    PX("handy_empfang", "Handy: ihre Blase kommt an, waehrend der Chat offen ist (statt notification je Blase)", gruppe="ui"),
    PX("handy_herz", "Handy: ihr Herz an Ducs Nachricht", gruppe="ui"),
    PX("anruf_verbinden", "Videoanruf: Duc nimmt an", gruppe="ui"),
    PX("anruf_ende", "Videoanruf: das Gespraech endet (2 s)", gruppe="ui"),
    PX("anruf_verpasst", "Videoanruf abgelehnt: verpasster Anruf", gruppe="ui"),
    PX("explosion", "Explosion Nacht 1 (Luefter + Knall)"), PX("alarm", "Schiffsalarm"),
    PX("feuer_loop", "Feuer (Schleife)", schleife=True), PX("schritte_kies", "Expedition: naechster Ort"),
    PX("rast_feuer", "Lagerfeuer am Rastplatz (Schleife)", schleife=True), PX("fund", "Fund-Karte"),
    PX("spur_uhr", "Spur-Uhr verliert ein Segment"), PX("auftrag_feder", "Auftrag angenommen / Schritt erledigt"),
    PX("auftrag_siegel", "Auftrag abgeschlossen"), PX("neue_waffe", "Neue Waffe"),
    PX("chip_einrasten", "Werkstatt: Chip rastet ein"), PX("werkstatt_fertig", "Werkstatt: Stueck fertig"),
    PX("heilung", "Heilung"), PX("status", "Statuseffekt"),
    PX("amb_deck", "Ambience Deck / Wasser am Rumpf", schleife=True),
    PX("amb_nacht", "Ambience Nacht vor Anker", schleife=True), PX("amb_macchia", "Ambience Macchia", schleife=True),
    PX("bordrat", "Bordrat beginnt"), PX("versprechen", "Versprechen gegeben / gehalten"),
    PX("versprechen_gebrochen", "Versprechen gebrochen"), PX("amb_hafen", "Ambience Hafen", schleife=True),
    PX("amb_bar", "Ambience Bar", schleife=True), PX("menue_tab", "Menue: Reiter wechseln", gruppe="ui"),
    PX("ruhig_voegel", "Ruhiger Ort (Schleife)", schleife=True), PX("tag_ende", "Tagesende", varianten=3),
    # Phasenuebergaenge (27.10.): je Tageszeit eine eigene Erkennungsmelodie statt der Bass-Jingles, Quelle sfx_phasen.py.
    # phase_wechsel = Sci-Fi-Reveal der Anhoerung (effekt in kern/anhoerung.py) und Ersatz fuer unbekannte Phasen.
    PX("phase_fruehstueck", "Wechsel zu Fruehstueck (Gitarre)", varianten=3), PX("phase_tag", "Wechsel zu Tag (Bossa/Latin)", varianten=5),
    PX("phase_nachmittag", "Wechsel zu Nachmittag (Rhodes)", varianten=4), PX("phase_dinner", "Wechsel zu Dinner (Jazz-Akkorde)", varianten=5),
    PX("phase_abend", "Wechsel zu Abend (Lo-Fi)", varianten=3), PX("phase_nacht", "Wechsel zu Nacht (Lo-Fi)", varianten=4),
    PX("phase_wechsel", "Anhoerung: naechste Phase (Sci-Fi-Reveal)"), PX("anhoerung_wende", "Anhoerung: Wende / Enthuellung"),
    PX("donner", "Donnerschlag (Sturm an Tag 5: Blitz jeder Krise, ab und an zwischendurch)", varianten=2),
    # Granaten (Duc 28.10.2026, Abnahme docs/abnahme/granaten_klang): client/plugins/eden-combat spielt sie beim Wurf/Einschlag
    PX("kampf_granate_wurf", "Kampf: Granate - Splint ziehen + Wurf (ElevenLabs)"),
    PX("kampf_granate_feuer", "Kampf: Feuergranate schlaegt ein"), PX("kampf_granate_wasser", "Kampf: Wassergranate schlaegt ein"),
    PX("kampf_granate_schock", "Kampf: Schockgranate schlaegt ein"), PX("kampf_granate_flash", "Kampf: Blendgranate - Knall"),
    PX("kampf_granate_pfeifen", "Kampf: Blendgranate - Ohrenpfeifen unter der Weissblende"),
    PX("kampf_granate_erschuetterung", "Kampf: Erschuetterungsgranate schlaegt ein"),
    PX("kampf_granate_splitter", "Kampf: Splittergranate - Knall + Metallsplitter"),
    # Level-up-Zeremonie (Duc 28.10.2026, Abnahme docs/abnahme/meister_moment): vierter Skill eines Pfads sitzt
    PX("skill_gemeistert", "Level-up: Pfad gemeistert (Cinematic Piano Hit)"),
]
# Anhoerung: Duc nahm statt der ElevenLabs-Varianten 1-4 je eine Pixabay-Datei - sie liegt als Variante 5 daneben
for _s in SFX:
    if _s["id"] in ("anhoerung_hammer", "anhoerung_einspruch"):
        _s.update(varianten=5, wahl=5, quelle="pixabay")

# Nonnas Farm (Duc 27.10.2026, E-079): Klick auf ein Tier spielt seinen Laut (client/plugins/eden-farm), Baby klingt hoeher. Der Client ruft
# EdenSfx.play("tier_<laut>") bzw. "tier_<laut>_baby"; kein Ausloeser in der Engine. Mehrfach: das Spiel wechselt zwischen den Varianten.
SFX += [
    S("tier_cluck", "Farm: Huhn gluckst (Klick auf das Tier)",
      "a Livorno hen clucking contentedly in a farm shed, three soft clucks and a short scratch in straw, quiet barn room tone", 2.5, mehrfach=True),
    S("tier_cluck_baby", "Farm: Kueken piepst",
      "a baby chick peeping, three tiny high peeps and soft rustling in straw, quiet barn", 2.0, mehrfach=True),
    S("tier_grunt", "Farm: Schwein grunzt",
      "a black pig grunting twice in a wooden sty, deep snuffling and a contented snort, straw rustling", 2.5, mehrfach=True),
    S("tier_grunt_baby", "Farm: Ferkel quiekt",
      "a piglet squealing softly, two short high squeals and a snuffle, straw rustling, quiet barn", 2.0, mehrfach=True),
    S("tier_moo", "Farm: Kuh muht",
      "a big white cow mooing once deeply in a barn, a cow bell clinking faintly, hay rustling", 3.0, mehrfach=True),
    S("tier_moo_baby", "Farm: Kalb blökt",
      "a calf bleating, two short high moos, soft hooves in straw, quiet barn", 2.0, mehrfach=True),
]
# Angeln (Duc 27.10.2026): Client-Plugin eden-angeln ruft EdenSfx.play("angeln_<anlass>"); kein Ausloeser in der Engine.
SFX += [
    S("angeln_wurf", "Angeln: Auswerfen",
      "a fishing rod cast, a quick whoosh of line through the air, the reel ticking, then a small lure plopping into calm sea water", 2.0, mehrfach=True),
    S("angeln_biss", "Angeln: Biss (Pose taucht ab)",
      "a fishing float suddenly pulled under the water, a short sharp plop and a little splash, the line going taut", 1.0, mehrfach=True),
    S("angeln_treffer", "Angeln: Treffer im Drill (Rolle zieht an)",
      "a fishing reel cranked hard for a moment, a tight ratchet clicking and the line hissing through the water", 1.0, mehrfach=True),
    S("angeln_fehl", "Angeln: Fehlklick im Drill",
      "a fishing line going slack with a soft wet slap on the water and a loose reel rattle", 0.8, mehrfach=True),
    S("angeln_fang", "Angeln: Fisch ist gelandet",
      "a fish lifted out of the water with a lively splash and dripping water, then flapping on a wooden deck", 2.0, mehrfach=True),
    S("angeln_riss", "Angeln: Leine reisst",
      "a taut fishing line snapping with a sharp twang, the reel spinning free, a small splash in the distance", 1.5, mehrfach=True),
]
# Abbauen an Rastplaetzen (Duc 28.10.2026: "schoener satter Holzschlag oder Steinschlag, mit Baumfaellt oder Stein bricht ab bei
# Erfolg"): Client-Plugin eden-abbau ruft EdenSfx.play("abbau_<anlass>").
SFX += [
    S("abbau_axt", "Abbau: Axthieb in den Stamm", "", 1.2, mehrfach=True, konzepte=[
        ("tief", "a heavy steel axe biting deep into a solid oak trunk, one deep satisfying thunk with a crisp woody crack, wood chips scattering"),
        ("knackig", "a sharp axe chopping hard into dense hardwood, a full round chock with a bright splintering crack, a chip landing in leaves"),
        ("schwer", "a big felling axe striking a thick living tree, a heavy resonant thud through the trunk, bark and splinters flying")]),
    S("abbau_baum_faellt", "Abbau: Baum knackt und faellt", "", 4.0, mehrfach=True, lang=True, konzepte=[
        ("krachen", "a tree trunk creaking and cracking as it gives way, then a tall tree crashing down through branches onto the forest floor with a heavy thud and rustling leaves"),
        ("aechzen", "wood fibres groaning and snapping in a cut tree, a long creak, then the whole tree falling and hitting the ground with a deep boom and settling leaves")]),
    # Korkeiche (Duc 30.10.2026): der Baum faellt nicht, nur die Rinde
    S("abbau_rinde_faellt", "Abbau: Korkrinde loest sich und faellt herunter", "", 2.0, mehrfach=True, wahl=2, konzepte=[
        ("platte", "a large thick slab of dry cork bark tearing away from a tree trunk with a soft creak, then dropping to the dry ground with a light hollow thud"),
        ("reissen", "dry bark peeling off a tree with a long fibrous rip, then light hollow pieces of cork tumbling and clattering softly on the earth"),
        ("hohl", "a curved piece of cork bark coming loose with a woody pop and landing on dry leaves, a soft papery hollow knock, very light and airy")]),
    S("abbau_hacke", "Abbau: Spitzhacke auf Stein", "", 1.0, mehrfach=True, konzepte=[
        ("klirren", "a steel pickaxe striking hard granite rock, a sharp ringing clank with a gritty crunch and small stones skittering"),
        ("dumpf", "a heavy pickaxe biting into a large boulder, a solid stony thock with a short metallic ring and grit falling"),
        ("funken", "a pickaxe point hitting flint-hard rock, a bright chink and a crunchy crack, little pebbles bouncing away")]),
    S("abbau_stein_bricht", "Abbau: Fels bricht auseinander", "", 2.5, mehrfach=True, lang=True, konzepte=[
        ("spalten", "a large rock splitting apart with a deep crack, heavy chunks of stone tumbling and rolling onto gravel, a little dust"),
        ("bersten", "a boulder bursting in two with a loud stony crunch, the halves thudding onto the ground, small stones rattling after")]),
    S("abbau_daneben", "Abbau: Schlag geht daneben (streift)", "an axe glancing off hard bark with a dull scrape and a quick whoosh of air",
      0.8, varianten=2, mehrfach=True),
]

# Abnahme 29.10.2026 (Ducs Vorhoer-Auswahl, docs/abnahme/vorhoeren_auswahl_20261029.md): je eine Variante.
# Offen bleiben 41/42/105/108/110-115 - die sollen von Pixabay kommen.
WAHL_29_10 = {
    "limousine_ankunft": 1, "klemmbrett_schritte": 4, "kaffee_schluerfen": 3, "schraubenschluessel_klong": 3,
    "hubschrauber_ueberflug": 2, "katze_miau": 2, "kamera_ausloeser": 2, "rudel_hunde": 4, "keiler_ansturm": 4,
    "ziege_halsband": 4, "anhoerung_slam": 4, "tier_cluck": 1, "tier_cluck_baby": 4, "tier_grunt": 1,
    "tier_grunt_baby": 4, "tier_moo": 4, "tier_moo_baby": 1, "angeln_biss": 4, "angeln_treffer": 4, "angeln_fang": 1,
}
for _s in SFX:
    if _s["id"] in WAHL_29_10:
        _s["wahl"] = WAHL_29_10[_s["id"]]
assert set(WAHL_29_10) <= {_s["id"] for _s in SFX}, "WAHL_29_10: unbekannte ID"

# Pixabay statt ElevenLabs (Abnahme 29.10., Duc nannte die Seiten; Quellen in sfx_pixabay.py, Download mit seinem OK):
# die Datei liegt als naechste Variante neben den ElevenLabs-Varianten und wird gewaehlt. quelle="pixabay": nie neu erzeugen.
# rudel_ratten: vier Pixabay-Kandidaten (5-8), Duc 29.10.: Variante 7 ("Rat Squeaking HD").
PIXABAY_29_10 = {"hubschrauber_start": 5, "angeln_wurf": 5, "angeln_fehl": 5, "angeln_riss": 5, "abbau_axt": 4,
                 "abbau_baum_faellt": 3, "abbau_hacke": 4, "abbau_stein_bricht": 3, "abbau_daneben": 3}
for _s in SFX:
    if _s["id"] in PIXABAY_29_10:
        _s.update(varianten=PIXABAY_29_10[_s["id"]], wahl=PIXABAY_29_10[_s["id"]], quelle="pixabay")
    elif _s["id"] == "rudel_ratten":
        _s.update(varianten=8, wahl=7, quelle="pixabay", mehrfach=True)
    elif _s["id"] in ("wuerfel_erfolg", "wuerfel_fehlschlag"):   # Duc 03.11.2026: Harfe / Leier ueberall, eine Stimme
        _s.update(varianten=5, wahl=5, quelle="pixabay")

# Kampf lesen (Duc 03.11.2026): Warnung vor der Taeuschung, Kettenklaenge 2/3, Finte reihum, Konter nach voller Kette
SFX += [PX("kampf_warnung", "Kampf: Taeuschung angekuendigt (erster Gong-Schlag)"),
        PX("kampf_kette_2", "Kampf: zweiter Treffer einer Kette pariert"),
        PX("kampf_kette_3", "Kampf: dritter Treffer einer Kette pariert"),
        PX("kampf_finte", "Kampf: der Gegner zuckt (Taeuschung), zwei Varianten reihum", varianten=2),
        PX("kampf_konter_kette", "Kampf: Konter nach voller Kette")]
# Ducs eigener Klang (03.11.2026, S:/VR/Gallery/Downloads/Sounds/Sucess Parry.mp3): positiver Ausklang nach der perfekten
# Parade. Vorn Stille weg, 2,5 s mit 0,8 s Ausblende, -18 LUFS (ffmpeg, Befehl in docs/wiki/systeme/kampf.md)
_ERFOLG = PX("kampf_parade_erfolg", "Kampf: Ausklang der perfekten Parade (Ducs Klang 'Sucess Parry')")
_ERFOLG.update(quelle="eigen")
SFX.append(_ERFOLG)

# ------------------------------------------------------------------ Grotten-Mission (Duc 29.10.2026: "fehlen SFX?")
# Hintergrund: drei Pixabay-Schleifen mit je vier Kandidaten (noch offen, kern/sfx.py ambience). Momente in den Frames und
# Kampf-Auftakte je Gegnertyp: ElevenLabs. Ausloeser unten (ereignisse = Frame-IDs, gegner = Gegnertyp im Kampf).
_GROTTE_AMB = [PX("amb_grotte", "Grotte: Tropfen und Echo (Schleife)", varianten=4, schleife=True),
               PX("amb_grotte_flut", "Flut-Nacht: Wasser in der Grotte (Schleife)", varianten=4, schleife=True),
               PX("amb_daecher", "Kevins Daecher: Wind, Tauben, Dorf (Schleife)", varianten=4, schleife=True)]
for _s in _GROTTE_AMB:
    _s["wahl"] = None                                        # Duc waehlt auf der Vorhoerseite
SFX += _GROTTE_AMB

# Holms Wette (Duc 30.10.2026): Quellen und Schnitt in sfx_schiessen.py, Abnahme docs/abnahme/schiessen_klang.json
SFX += [PX("gun_shot", "Schiesswette: Schuss"), PX("gun_reload", "Schiesswette: Nachladen"),
        PX("schiessen_flasche", "Schiesswette: Flasche zerspringt"), PX("schiessen_ton", "Schiesswette: Tontaube zerspringt"),
        PX("schiessen_drohne", "Schiesswette: Drohne faellt aus"), PX("schiessen_moewe", "Schiesswette: Moewe getroffen"),
        PX("schiessen_blend", "Schiesswette: Blendgranate")]
# Belagerung (Duc 01.11.2026): Quellen und Schnitt in sfx_belagerung.py, Abnahme docs/abnahme/sfx_belagerung.html. Karte: eden-tactics.js
SFX += [PX("tk_taser", "Karte: Chiaras Taser"), PX("tk_flinte", "Karte: Alvas Flinte"), PX("tk_klinge", "Karte: Klinge"),
        PX("tk_granate", "Karte: Bibis Granate (kurz)"), PX("tk_drohne", "Karte: Drohne fliegt an"), PX("tk_roboter", "Karte: Roboter stampft"),
        PX("tk_ko", "Karte: Figur faellt"), PX("tk_stahlplatte", "Karte: Danzels Stahlplatte"), PX("tk_schritte", "Karte: Trupp zieht"),
        PX("tk_zugwechsel", "Karte: Zug beginnt"), PX("tk_cutin", "Karte: grosse Tat"), PX("tk_holzbruch", "Karte: Barrikade bricht"),
        PX("tk_kirche", "Karte: Kirche getroffen"), PX("tk_haus_weg", "Karte: Haus verloren"), PX("tk_yacht_sinkt", "Karte: Yacht sinkt"),
        PX("tk_gitter", "Karte: Pascal oeffnet das Tor"), PX("tk_loewe", "Karte: Mochi"), PX("tk_rauch", "Karte: Rauch auf dem Platz"),
        PX("tk_jubel", "Karte: Welle gehalten"), PX("tk_glocke", "Belagerung: Kirchenglocke"), PX("tk_hammer", "Flicken: Hammerschlag"), PX("tk_maxwell_schlag", "Maxwell trifft mit dem Steel Mop"),
        PX("tk_bretter", "Flicken: Stelle fertig"), PX("tk_bucht", "Belagerung: die Bucht bewegt sich"),
        PX("tk_unit_werkstatt", "Manoever: Unit-01 rollt aus der Werkstatt"), PX("tk_unit_wasser", "Welle 2: Roboter auf dem Wasser"),
        PX("amb_maschine", "Maschinenraum: Unit-01 summt (Schleife)", schleife=True),
        PX("tk_yacht_riss", "Karte: Roboter reisst die Yacht auf"), PX("tk_drohne_ab", "Karte: Drohne faellt"), PX("tk_haus_feuer", "Karte: Haus faengt Feuer"), PX("tk_haus_schreie", "Karte: Leute schreien im Haus"),
        PX("tk_liste", "Morgen: Holm geht die Liste durch"), PX("tk_megan_weg", "Kriegsrat: Megans Bild bricht ab"),
        PX("amb_taktik", "Karte: Krieg in der Ferne (Schleife)", schleife=True),
        # Drehbuch Finale (Duc 02.11.2026, Pixabay-Wahl finale_auswahl.html), geschnitten in sfx_belagerung.py
        PX("tk_ligeia", "Welle 4: Ligeia singt"), PX("tk_minicu_fall", "Welle 6: der eine Schlag gegen Minicu, Fall und Koerper"),
        PX("tk_applaus", "Tag 21: das Dorf klatscht nach Casanovas Rede"), PX("tk_kevin", "Welle 6: Kevin fliegt vom Tor"),
        PX("tk_rudern", "Welle 4: das Dorf rudert hinaus (1924)"), PX("tk_papier", "Abend Tag 22: Casanova verbrennt das Papier im Ofen"),
        PX("tk_kreide", "Bericht: Alvas Kreidetafel"), PX("tk_drucker", "Tag 15: die Kriegstafel kommt aus dem Drucker")]
_WORTLOS = "clean, high quality game sound effect, no music, no words, wordless voice only, short tail"
SFX += [
    S("flut_steigt", "Grotte: die Flut drueckt herein (Boss-Halle, Flut-Nacht, Ebbe-Uhr)",
      "sea water surging into a rocky sea cave, a deep rushing swell filling the chamber, water slapping against stone "
      "walls, hollow cave echo, ominous and rising", 4.0, einfluss=0.6, lang=True),
    S("fackel_an", "Grotte: Fackeln fauchen auf (Fackelgalerie)",
      "a pitch torch igniting in a damp stone cave, a sharp whoosh of flame catching, crackling fire, hollow echo", 2.0),
    S("gitter", "Grotte: Eisengitter ruettelt und gibt nach",
      "an old rusted iron grate rattling hard, then the bars bending and a bolt snapping loose with a metallic clang, "
      "dripping water, cave echo", 2.5),
    S("steinschlag", "Grotte: Steine rutschen im eingestuerzten Gang",
      "loose rocks and gravel sliding and tumbling down inside a cave passage, stones clattering and thudding, dust "
      "settling, hollow echo", 3.0),
    S("tauchen", "Grotte: Sprung ins Wasser, dann dumpf unter Wasser",
      "a person jumping feet first into deep cold water in a cave, a big splash, then muffled underwater sound with "
      "bubbles rising", 3.0),
    S("kiste_auf", "Grotte: schwere Schmugglerkiste wird geoeffnet",
      "a heavy old wooden smugglers' crate being pried open, an iron chain rattling off, the lid creaking up on rusty "
      "hinges, cave echo", 2.5),
    S("glocke", "Kevins Daecher: grosse Glocke im Glockenturm",
      "one huge bronze church bell struck once very close inside a bell tower, a deep booming strike with a long "
      "ringing hum, pigeons startled", 5.0, lang=True),
    S("tauben_auf", "Kevins Daecher: Taubenschwarm flattert auf",
      "a flock of pigeons suddenly taking off from a terracotta roof, loud flapping wings, a few startled coos, open "
      "air above a village", 2.5),
    S("kampf_fledermaeuse", "Kampf-Auftakt: Fledermaus-Schwarm",
      "a swarm of bats bursting out of a dark cave, dozens of leathery wings flapping, high shrill squeaks and "
      "screeches, echoing", 3.0),
    S("kampf_viper", "Kampf-Auftakt: Schwarze Viper",
      "a large venomous snake rearing up on stone, a long menacing hiss, scales sliding over rock, quiet cave", 2.5),
    S("kampf_sirene", "Kampf-Auftakt: die Sirene",
      "an eerie glassy siren tone rising over still water, a haunting wordless sustained female hum drenched in cave "
      "reverb, beautiful and dangerous", 4.0, einfluss=0.6, stil=_WORTLOS),
    S("kampf_riscossore", "Kampf-Auftakt: U Riscossore (Boss)",
      "heavy boss entrance stinger, slow heavy boot steps on wet stone, a deep cinematic low drum hit and a dark brass "
      "swell, menacing", 4.0, einfluss=0.6, lang=True),
    S("kampf_unit01", "Kampf-Auftakt: Unit-01 (Red Eye)",
      "an old industrial machine powering up hostile, whirring servo motors, a rising electric warning hum and three "
      "sharp red alert beeps, clanking metal", 3.0),
    S("kampf_pale_lady", "Kampf-Auftakt: The Pale Lady (selten)",
      "a cold gust of wind through a stone tunnel, rustling silk, candle flames guttering, a soft eerie wordless female "
      "laugh fading into reverb, chilling", 3.5, einfluss=0.6, stil=_WORTLOS),
]

_schlaf = PX("kampf_granate_schlaf", "Kampf: Schlafgranate - blaue Wolke (lokal erzeugt, werkzeuge/eden_rise/schlaf_klang.py)")
_schlaf.update(prompt="lokal", quelle="lokal")
SFX.append(_schlaf)

AUSLOESER = {
    "explosion": {"szenen": ["explosion"]},          # Pixabay 27.10.: Luefter + Knall
    # Hafenkampf (25.10.)
    "rudel_ratten": {"kaempfe": ["hafen_ratten"]},
    "rudel_hunde": {"kaempfe": ["hafen_hunde", "rt_4b_hyaenen"]},
    "keiler_ansturm": {"kaempfe": ["hafen_keiler", "rt_4a_mufflon"]},
    "ziege_halsband": {"ereignisse": ["hk_ziege"]},
    "hubschrauber_holm": {"szenen": ["holm_abschied"]},
    "hubschrauber_megan": {"szenen": ["megan_kommt"], "ereignisse": ["g1_helikopter"]},
    "blackout": {"szenen": ["blackout"]},
    "strom_zurueck": {"nach_szene": ["blackout"]},
    "sturm_nacht": {"szenen": ["sturmnacht"]},
    "funk_rauschen": {"szenen": ["sturmvorbereitung"], "ereignisse": ["rt_mast_2", "bl_belagerung", "bl_funk", "bl_funk_rosi", "bl_funk_rosi_charly",
                                                                     "bl_funk_sophia", "bl_funk_nichts"]},
    "donner": {"szenen": ["leises_telefonat"]},       # Sturm zieht auf (Duc 27.10.: Donner ab und an in den Szenen)
    "ankerkette": {"ereignisse": ["br_nachtwache"]},
    "anruf_klingeln": {"ereignisse": ["rt_charly"]},
    "versprechen_gebrochen": {"ereignisse": ["rt_t_bruch"]},
    "anhoerung_wende": {"ereignisse": ["rt_white"]},
    "tier_grunt_baby": {"ereignisse": ["rt_bibi_frischlinge_1", "rt_bibi_frischlinge_2", "rt_bibi_frischlinge_3"]},
    "tuer_klopfen": {"ereignisse": ["ab_lola_klopft", "bl_tueren"] + ["bl_na_%s%s%s" % (w, a, b) for w in ("chiara", "rosi", "lola") for a in ("", "_wieder") for b in ("", "_still")]},   # nur wo es eine Tuer gibt
    "sektkorken": {"szenen": ["auftakt_party"]},
    "tender_motor": {"szenen": ["landgang", "landgang_2"], "ereignisse": ["g1_chiara_tender", "gv_aussenborder", "bl_welle_3"]},
    "wasser_platsch": {"ereignisse": ["g1_chiara_pause"]},
    # Tag 0 (25.10.)
    "limousine_ankunft": {"ereignisse": ["t0_limousine"]},
    "klemmbrett_schritte": {"ereignisse": ["t0_megan"]},
    "kaffee_schluerfen": {"ereignisse": ["t0_holm"]},
    "schraubenschluessel_klong": {"ereignisse": ["t0_rosi"]},
    "hubschrauber_ueberflug": {"ereignisse": ["t0_maxwell"]},
    "katze_miau": {"ereignisse": ["t0_jana"]},
    "kamera_ausloeser": {"ereignisse": ["t0_yamamoto", "t0_siri"]},
    "hubschrauber_start": {"ereignisse": ["t0_abschied_herzlich", "t0_abschied_frech", "t0_abschied_flirt",
                                          "t0_abschied_foermlich"]},
    # Grotten-Mission (29.10.2026). "gegner": Gegnertyp im Kampf (auch der seltene Gegner einer Begegnung)
    "flut_steigt": {"ereignisse": ["gr_boss", "gr_boss_spaet", "gr_boss_matteu", "gr_boss_matteu_spaet", "fn_start"]},
    "fackel_an": {"ereignisse": ["gr_fackel"]},
    "gitter": {"ereignisse": ["gr_u1_gitter"]},
    "steinschlag": {"ereignisse": ["gr_u2_start", "gr_rueckweg_bastien"]},
    "tauchen": {"ereignisse": ["gr_u1_start"]},
    "kiste_auf": {"ereignisse": ["gr_wahl"]},
    "glocke": {"ereignisse": ["kv_glocke", "rt_weg_danzel", "rt_weg_bibi", "rt_weg_bibi_buch", "rt_weg_charly"]},
    "tauben_auf": {"ereignisse": ["kv_start"]},
    "kampf_fledermaeuse": {"gegner": ["fledermaeuse"]},
    "kampf_viper": {"gegner": ["schlange", "schlange_alpha"]},
    "kampf_sirene": {"gegner": ["sirene"]},
    "kampf_riscossore": {"gegner": ["riscossore"]},
    "kampf_unit01": {"gegner": ["unit01", "hirtendrohne"]},
    "kampf_pale_lady": {"gegner": ["vampirin"]},
    "tk_unit_werkstatt": {"ereignisse": ["bl_manoever"]},
    "tk_unit_wasser": {"ereignisse": ["bl_welle_2"]},
    "tk_bucht": {"ereignisse": ["bl_welle_5"]},
    "tk_liste": {"ereignisse": ["bl_morgen_22", "bl_morgen_23"]},
    # Drehbuch "Hold the Line" (Duc 02.11.2026). Im Bericht laeutet die Glocke erst bei Casanovas Satz (index.html ZEILEN_TON), vorher ist es still.
    "tk_glocke": {"ereignisse": ["bl_kirche", "bl_kirche_don"]},
    "tk_hammer": {"ereignisse": ["bl_aufbau_heil", "bl_aufbau_asche"]},
    "glaeser_anstossen": {"ereignisse": ["bl_bar", "bl_bar_runde"]},
    "schritte_kies": {"ereignisse": ["bl_wache_wolff_bericht", "bl_wache_elsa_bericht", "bl_wache_yamamoto_bericht"]},
    "tk_drucker": {"ereignisse": ["bl_tafel"]},
    "tk_kreide": {"ereignisse": ["bl_bericht"]},
}


def pruefen_ausloeser():
    """Jede ID muss es geben: Events, Szenen und Kaempfe (nur IDs, kein Inhalt)."""
    mod = os.path.dirname(ZIEL)
    events = {e["id"] for e in json.load(open(os.path.join(mod, "ereignisse.json"), encoding="utf-8"))["events"]}
    _k = json.load(open(os.path.join(mod, "kaempfe.json"), encoding="utf-8"))
    kaempfe, gegner = set(_k["encounters"]), set(_k["enemies"])
    szenen = set()
    story = os.path.join(mod, "story.json")
    if os.path.exists(story):
        for d in json.load(open(story, encoding="utf-8"))["wochenbogen"].values():
            for liste in (d.get("phasen") or {}).values():
                szenen.update(x["id"] for x in liste)
    ids = {s["id"] for s in SFX}
    fehler = []
    for sid, a in AUSLOESER.items():
        if sid not in ids:
            fehler.append("unbekannter Effekt: " + sid)
        fehler += ["%s: Event %s fehlt" % (sid, e) for e in a.get("ereignisse", []) if e not in events]
        fehler += ["%s: Kampf %s fehlt" % (sid, k) for k in a.get("kaempfe", []) if k not in kaempfe]
        fehler += ["%s: Gegner %s fehlt" % (sid, g) for g in a.get("gegner", []) if g not in gegner]
        fehler += ["%s: Szene %s fehlt" % (sid, s) for s in a.get("szenen", []) + a.get("nach_szene", [])
                   if szenen and s not in szenen]
    return fehler


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ids = [s["id"] for s in SFX]
    assert len(ids) == len(set(ids)), "doppelte id"
    for s in SFX:
        assert 0.5 <= s["dauer"] <= 30 and 0 <= s["einfluss"] <= 1, s["id"]
        for p in [s["prompt"]] + [k["prompt"] for k in s.get("konzepte", [])]:
            assert len(p) <= 450, "%s: Prompt %d Zeichen, ElevenLabs erlaubt 450" % (s["id"], len(p))
        w = s["wahl"]
        assert w is None or (isinstance(w, list) and s["mehrfach"] and w) or isinstance(w, int), s["id"]
        assert all(1 <= n <= s["varianten"] for n in (w if isinstance(w, list) else [w] if w else [])), s["id"]
    fehler = pruefen_ausloeser()
    if fehler:
        sys.exit("Auslöser fehlerhaft:\n  " + "\n  ".join(fehler))
    json.dump({"_hinweis": "Gebaut aus werkzeuge\\eden_rise\\sfx_eden_rise.py - dort aendern.", "sfx": SFX,
               "ausloeser": AUSLOESER}, open(ZIEL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    offen = [s for s in SFX if s["wahl"] is None]
    print("geschrieben:", ZIEL, "-", len(SFX), "Effekte,", len(SFX) - len(offen), "gewaehlt,", len(offen), "offen:",
          ",".join(s["id"] for s in offen))


if __name__ == "__main__":
    main()

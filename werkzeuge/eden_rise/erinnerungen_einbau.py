# -*- coding: utf-8 -*-
r"""Erinnerungen fuer Spieler, die die Szene davor vergessen haben (Duc 31.10.2026, STIL.md "Verstaendlich bleiben"): Paket 1 der
Missions-Pruefung. Schreibt die Builder und stimme_tags.json einmalig um und bleibt als Beleg liegen.

    erinnerungen_einbau.py <Eden-Ordner>
"""
import json, os, re, sys

B = sys.argv[1]
W = "werkzeuge/eden_rise/"


def patch(pfad, paare):
    p = os.path.join(B, pfad)
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    s = s.replace("\r\n", "\n")
    for a, b in paare:
        assert s.count(a) >= 1, (pfad, a)
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))


T = " Takes the whole phase."
patch(W + "auftraege_eden_rise.py", [
    # Ortskarte je Lage
    ('_RT_START = [{"wenn": {"alle": _RT + [{"flag": "rt_tisch_fertig"}]}, "id": "rt_white"},\n',
     '_RT_START = [{"wenn": {"alle": _RT + [{"flag": "rt_tisch_fertig"}]}, "id": "rt_white",\n'
     '              "text": "The man in white is coming for Danzel, Bibi and Charly, up in Nonna Fiora\'s garden at San Martinu.' + T + '"},\n'),
    ('{"wenn": {"alle": _RT + [{"flag": p} for p in _RT_PFADE]}, "id": "rt_ankunft"}]',
     '{"wenn": {"alle": _RT + [{"flag": p} for p in _RT_PFADE]}, "id": "rt_ankunft",\n'
     '              "text": "You found Danzel, Bibi and Charly. Now they have to get to Nonna Fiora\'s table at San Martinu.' + T + '"}]'),
    ('"id": "rt_gabelung_" + "".join("0" if _m & (1 << i) else "1" for i in range(3))})',
     '"id": "rt_gabelung_" + "".join("0" if _m & (1 << i) else "1" for i in range(3)),\n'
     '                      "text": "The men in black suits scattered Danzel, Bibi and Charly across the macchia. Find them.' + T + '"})'),
    ('{"wenn": {"alle": _RT + [{"flag": "rt_1_sieg"}]}, "id": "rt_lager"}',
     '{"wenn": {"alle": _RT + [{"flag": "rt_1_sieg"}]}, "id": "rt_lager",\n'
     '               "text": "The three people in red you beat on the path are still out there, and they want that steel plate.' + T + '"}'),
    ('{"wenn": {"flag": "bg_bergerie_erreicht"}, "id": "bg_bergerie_zurueck"}',
     '{"wenn": {"flag": "bg_bergerie_erreicht"}, "id": "bg_bergerie_zurueck",\n'
     '                   "text": "Back up to the bergerie, where Laetitia and her soldier Adrien are waiting.' + T + '"}'),
    ('{"wenn": {"flag": "bg_turm_erreicht"}, "id": "bg_turm_zurueck"}',
     '{"wenn": {"flag": "bg_turm_erreicht"}, "id": "bg_turm_zurueck",\n'
     '                   "text": "Back up to the Genoese tower, where Wolff and the Legion are looking for Laetitia.' + T + '"}'),
    ('"text": "The last shepherd on the mountain. Takes the whole phase."', '"text": "Ghjuvan, the last shepherd, and the bear that takes his sheep. Takes the whole phase."'),
    ('"text": "An old woman, a candle in the window, a dream. Takes the whole phase."', '"text": "Old Dumenica\'s hut. She wants the black beast from her dream dead. Takes the whole phase."'),
    # Journal: Text
    ('"Three people in red want a steel plate back. They attack', '"Three people in red want back the steel plate you found in the rock niche above San Martinu. They attack'),
    ('{"text": "Get through the two in the bushes.", "erledigt": {"flag": "rt_1_sieg"}}',
     '{"text": "Get through the two in the bushes.", "erledigt": {"flag": "rt_1_sieg"},\n'
     '             "rueckblick": "You beat the first of them on the path above San Martinu, and they ran."}'),
    ('{"text": "Get through all three on the bridge.", "erledigt": {"flag": "rt_3_sieg"}}',
     '{"text": "Get through all three on the bridge.", "erledigt": {"flag": "rt_3_sieg"},\n'
     '             "rueckblick": "You beat Danzel, Bibi and Charly on the bridge. Then men in black suits scattered them across the macchia."}'),
    ('{"text": "Find Danzel on the charcoal road.", "erledigt": {"flag": "rt_danzel_fertig"}}',
     '{"text": "Find Danzel on the charcoal road.", "erledigt": {"flag": "rt_danzel_fertig"},\n'
     '             "rueckblick": "You are finding Danzel, Bibi and Charly one by one, after the men in black suits scattered them."}'),
    ('{"text": "Find Bibi in the gorge.", "erledigt": {"flag": "rt_bibi_fertig"}}',
     '{"text": "Find Bibi in the gorge.", "erledigt": {"flag": "rt_bibi_fertig"},\n'
     '             "rueckblick": "You are finding Danzel, Bibi and Charly one by one, after the men in black suits scattered them."}'),
    ('{"text": "Find Charly on the ridge.", "erledigt": {"flag": "rt_charly_fertig"}}',
     '{"text": "Find Charly on the ridge.", "erledigt": {"flag": "rt_charly_fertig"},\n'
     '             "rueckblick": "You are finding Danzel, Bibi and Charly one by one, after the men in black suits scattered them."}'),
    ('{"text": "Get them all to Nonna\'s table.", "erledigt": {"flag": "rt_tisch_fertig"}}',
     '{"text": "Get them all to Nonna Fiora\'s table at San Martinu.", "erledigt": {"flag": "rt_tisch_fertig"},\n'
     '             "rueckblick": "Danzel, Bibi and Charly sat down at Nonna Fiora\'s long table at San Martinu."}'),
    ('{"text": "Hold the garden.", "erledigt": {"flag": "red_trio_fertig"}}',
     '{"text": "Hold Nonna Fiora\'s garden when Mr. White comes.", "wenn": {"flag": "rt_tisch_fertig"}, "erledigt": {"flag": "red_trio_fertig"}}'),
    ('"You told him to tell her himself."', '"You told Danzel to tell Bibi himself."'),
    ('"You told him nobody has to know."', '"You told Danzel nobody has to know."'),
    ('{"text": "Climb through the macchia to the monastery of San Martinu.", "erledigt": {"flag": "kl_tor_offen"}}',
     '{"text": "Climb through the macchia to the monastery of San Martinu.", "erledigt": {"flag": "kl_tor_offen"},\n'
     '             "rueckblick": "You reached the gate of San Martinu and met Nonna Fiora."}'),
    ('{"text": "Find the brothers and Frederico.",\n             "erledigt": {"eine": [{"flag": "kloster_frederico_lebt"}, {"flag": "kloster_frederico_tot"}]}}',
     '{"text": "Find the brothers and Frederico, the boy who ran after them.",\n             "erledigt": {"eine": [{"flag": "kloster_frederico_lebt"}, {"flag": "kloster_frederico_tot"}]},\n'
     '             "rueckblick": "You found out what happened to the brothers and to Frederico, the boy who ran after them."}'),
    ('{"text": "Climb to the Genoese tower and get past the Legion.", "erledigt": {"flag": "bg_turm_erreicht"}}',
     '{"text": "Climb to the Genoese tower and get past the Legion.", "erledigt": {"flag": "bg_turm_erreicht"},\n'
     '             "rueckblick": "You got past the Legion and its officer, Wolff, at the Genoese tower."}'),
    ('{"text": "Find Laetitia beyond the foggy ridge.", "erledigt": {"flag": "bg_bergerie_erreicht"}}',
     '{"text": "Find Laetitia beyond the foggy ridge.", "erledigt": {"flag": "bg_bergerie_erreicht"},\n'
     '             "rueckblick": "You found Petru\'s daughter Laetitia at the bergerie, with her soldier Adrien. Wolff wants him."}'),
    ('{"text": "Decide what happens to Adrien.",\n             "erledigt": {"eine": [{"flag": "bg_weg_a"}, {"flag": "bg_weg_b"}, {"flag": "bg_weg_c"},\n                                   {"flag": "bg_wolff_niederlage"}]}}',
     '{"text": "Decide what happens to Adrien, Laetitia\'s soldier.",\n             "erledigt": {"eine": [{"flag": "bg_weg_a"}, {"flag": "bg_weg_b"}, {"flag": "bg_weg_c"},\n                                   {"flag": "bg_wolff_niederlage"}]},\n'
     '             "rueckblick": "It is settled what happens to Adrien. Petru is still waiting for news of his daughter."}'),
    ('"You told him about the soldier."', '"You told Wolff about the soldier."'),
    ('"You told him nothing."', '"You told Wolff nothing."'),
    ('"You showed Wolff the pictures."', '"You showed Wolff Adrien\'s pictures."'),
    ('"You killed her for Ghjuvan."', '"You killed Old Grey for Ghjuvan."'),
    ('{"text": "Go down into the grotto at low tide.", "erledigt": {"flag": "gr_gennaro_gefunden"}}',
     '{"text": "Go down into the grotto at low tide.", "erledigt": {"flag": "gr_gennaro_gefunden"},\n'
     '             "rueckblick": "You went down at low tide and found Totò\'s cousin Gennaro."}'),
    ('{"text": "Get Gennaro past the man who comes with the tide.",\n             "erledigt": {"eine": [{"flag": "gr_kiste_abgegeben"}, {"flag": "gr_kiste_genommen"}]}}',
     '{"text": "Get Gennaro past the man who comes with the tide.",\n             "erledigt": {"eine": [{"flag": "gr_kiste_abgegeben"}, {"flag": "gr_kiste_genommen"}]},\n'
     '             "rueckblick": "You dealt with the man who comes with the tide. The water is rising, and Totò is waiting at the boat."}'),
    ('"You told him the truth."', '"You told Matteu the truth."'),
    ('"You told him it was quick."', '"You told Matteu it was quick."'),
    ('{"text": "Climb out onto the rooftops and chase Kevin.", "erledigt": {"flag": "kv_tauben"}}',
     '{"text": "Climb out onto the rooftops and chase Kevin.", "erledigt": {"flag": "kv_tauben"},\n'
     '             "rueckblick": "You chased Kevin the gull over the village rooftops."}'),
    ('{"text": "Get up the bell tower to his nest.", "erledigt": {"flag": "kv_kevin"}}',
     '{"text": "Get up the bell tower to his nest.", "erledigt": {"flag": "kv_kevin"},\n'
     '             "rueckblick": "You reached Kevin\'s nest in the bell tower. Lea is waiting for page forty."}'),
    ('{"text": "Row out to the grotto at high tide, alone.", "erledigt": {"flag": "fn_1_ratten"}}',
     '{"text": "Row out to the grotto at high tide, alone.", "erledigt": {"flag": "fn_1_ratten"},\n'
     '             "rueckblick": "You rowed out to the grotto alone at high tide, towards the humming under the rock."}'),
    ('{"text": "Go down to the black pool.", "erledigt": {"eine": [{"flag": "fn_geredet"}, {"flag": "fn_gegangen"}]}}',
     '{"text": "Go down to the black pool.", "erledigt": {"eine": [{"flag": "fn_geredet"}, {"flag": "fn_gegangen"}]},\n'
     '             "rueckblick": "You went down to the black pool and met what was humming there."}'),
])
patch(W + "missionen_eden_rise.py", [
    ("“Remember the relay? I have a little crate", "“Comandante, the relay for Alva's compressor? You owe me a little something, remember. I have a little crate"),
    ("It has to be bound in linen, says", "Elsa's tickets have to be bound in linen, says"),
    ("Three hundred and twelve sheets, one spine", "Elsa's tickets, three hundred and twelve sheets, one spine"),
    ("on the night of the failure", "on the night of the fire on board"),
    ("since the failure", "since the fire on board"),
    ("Since the failure", "Since the fire on board"),
])
patch(W + "ereignisse_red_trio.py", [
    ('"Three trails leave the clearing. Each one has footprints on it, running, and none of them lead towards the "\n              "shepherd\'s hut. These three don\'t know the macchia at all."',
     '"This is where the men in black suits scattered Danzel, Bibi and Charly. “Shepherd\'s hut, tonight,” Danzel shouted. Three "\n              "trails leave the clearing, each with footprints on it, running, and none of them lead towards the hut. These three "\n              "don\'t know the macchia at all."'),
    ('"Takes the charcoal road, into the burnt forest."', '"Takes the charcoal road, into the burnt forest, after Danzel."'),
    ('"Takes the gorge."', '"Takes the gorge, after Bibi."'),
    ('"Climbs to the ridge with the mast."', '"Climbs to the ridge with the mast, after Charly."'),
    ('"A hundred and ninety kilos, the last time I weighed him.', '"Mochi, my lion, was a hundred and ninety kilos, the last time I weighed him.'),
    ("Next to the bowl, pressed deep", "Next to the bowl she keeps filling for her lion Mochi, pressed deep"),
    ("I don't have any white linen. I don't work in white. I have never in my life", "White linen. “Lovely stitching.” That's what the man in white said to me in Nonna's garden. I have never in my life"),
])
patch(W + "ereignisse_dorf.py", [("So. Did they read them?", "So, Yacht. All those letters I gave you for the brothers. Did they read them?")])
patch(W + "ereignisse_holm.py", [
    ('“Is that the gun? The bear, a kilometre, right in the eye?”', '“Is that the gun from the old story? The bear, a kilometre, right in the eye?”'),
    ('Your dead friend from the "\n          "bergerie thinks he knows.', 'Adrien up at the bergerie, your "\n          "dead deserter, thinks he knows.'),
])
T_ = os.path.join(B, "module/eden_rise/stimme_tags.json")
d = json.load(open(T_, encoding="utf-8"))
for z in d["zeilen"]:
    for k in ("text", "gesprochen"):
        t = z.get(k) or ""
        t = t.replace("A hundred and ninety kilos, the last time", "Mochi, my lion, was a hundred and ninety kilos, the last time")
        t = t.replace("Your dead friend from the bergerie thinks he knows.", "Adrien up at the bergerie, your dead deserter, thinks he knows.")
        t = re.sub(r"I don't have any white linen\. (\[[a-z ]+\] )?I don't work in white\. (\[[a-z ]+\] )?I have never",
                   lambda m: "White linen. “Lovely stitching.” " + (m.group(1) or "") + (m.group(2) or "") + "That's what the man in white said to me in Nonna's garden. I have never", t)
        if k in z:
            z[k] = t
json.dump(d, open(T_, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ Engine und Oberflaeche
patch("kern/auftraege.py", [
    ('''    return [{"id": oid, "label": o["label"], "text": o["text"], "bild":''', '''    return [{"id": oid, "label": o["label"], "text": ort_text(z, o), "bild":'''),
    ('''def start(z, moddir, oid):
''', '''def ort_text(z, o):
    """Die Karte beschreibt die Lage: Der aktuelle Startpunkt darf einen eigenen Text haben (Duc 31.10.2026, der Spieler vergisst)."""
    s = next((s for s in o["start"] if regeln.gilt(s.get("wenn"), z)), None)
    return (s or {}).get("text") or o["text"]


def start(z, moddir, oid):
'''),
    ('''        naechster = next((s["text"] for s in schritte if not s["erledigt"] and not s["optional"]), None)
''', '''        naechster = next((s["text"] for s in schritte if not s["erledigt"] and not s["optional"]), None)
        rueckblick = next((s["rueckblick"] for s in reversed(a["schritte"]) if s.get("rueckblick") and regeln.gilt(s["erledigt"], z)), None)
'''),
    ('''"schritte": schritte, "grau": grau, "belohnung": a.get("belohnung", ""),
''', '''"schritte": schritte, "grau": grau, "belohnung": a.get("belohnung", ""),
                    "rueckblick": rueckblick if st == "aktiv" else None,      # "Last time": der Spieler vergisst (31.10.2026)
'''),
])
patch("kern/handel.py", [
    ('''def kette(z, V, j):
''', '''def zuletzt(z, V, j):
    """Ergebnis der Mission davor, fuer die Karte: Der Spieler hat sie vermutlich vergessen (Duc 31.10.2026)."""
    davor = next((x for x in V["jobs"] if x["id"] == j.get("nach")), None)
    return davor.get("erfolg") if davor and davor["id"] in z.get("jobs_erfolg", []) else None


def kette(z, V, j):
'''),
    ('''energie=1 if mit_probe else 0, kette=kette(z, V, j),
''', '''energie=1 if mit_probe else 0, kette=kette(z, V, j), zuletzt=zuletzt(z, V, j),
'''),
])
p = os.path.join(B, "client/index.html")
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
s = s.replace("\r\n", "\n")
a = """.mkette .strich{width:14px;height:1px;background:var(--linie-n)}
"""
assert s.count(a) == 1
s = s.replace(a, a + """.mzuletzt{font-size:var(--t-klein);color:var(--perle-dim)}.mzuletzt b{color:var(--perle-leise);font-weight:600}
""")
a = """    ${mKette(j)}<h3 class="mtitel">${esc(j.titel)}</h3><p>${esc(j.text)}</p>
"""
assert s.count(a) == 1
s = s.replace(a, """    ${mKette(j)}${j.zuletzt ? `<p class="mzuletzt"><b>Last time:</b> ${esc(j.zuletzt)}</p>` : ""}<h3 class="mtitel">${esc(j.titel)}</h3><p>${esc(j.text)}</p>
""")
s, n = re.subn(r"eden-menu\.js\?v=(\d+)", lambda m: "eden-menu.js?v=%d" % (int(m.group(1)) + 1), s)
assert n >= 1
open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))
patch("client/plugins/eden-menu/eden-menu.js", [(
    """      <p>${esc(a.text)}</p>
      <ul class="em-schritte">""",
    """      <p>${esc(a.text)}</p>
      ${a.rueckblick ? `<div class="em-grau"><small>Last time</small><p>${esc(a.rueckblick)}</p></div>` : ""}
      <ul class="em-schritte">""")])
print("ok", B)

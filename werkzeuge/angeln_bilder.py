# -*- coding: utf-8 -*-
r"""Angel-Bilder zur Auswahl (Duc 28.10.2026): je Gewaesser 10 Kandidaten-Orte, aus denen Duc 3 waehlt, und 4 Koeder-Varianten
je Koeder-Stufe.

    python werkzeuge\angeln_bilder.py              fehlende Kandidaten erzeugen + Abnahme-Spec schreiben
    python werkzeuge\angeln_bilder.py orte | koeder   nur diese Art
    python werkzeuge\angeln_bilder.py --spec       nur docs\abnahme\angeln_bilder.json schreiben

Orte: gleiche Bildaufteilung fuer alle (Duc: "damit links auch wirklich das Wasser ist") - die linken zwei Drittel offenes, ruhiges
Wasser, rechts das Ufer oder Deck, auf dem Duc sitzt. Breitformat 1664x928 wie hintergrund_bild.py, Ablage
ST\backgrounds\_varianten\eden_rise_angeln_<meer|fluss>_NN.png. Koeder: freigestellte Sprites wie kochen_bilder.py,
module\eden_rise\farm\koeder\_kandidaten\koeder_<stufe>_<n>.png."""
import json, os, random, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import hintergrund_bild as HB  # noqa: E402
import kochen_bilder as K  # noqa: E402

IB = K.IB
VAR = os.path.join(HB.ST_BG, "_varianten")
KOEDER_ZIEL = os.path.join(K.MOD, "farm", "koeder", "_kandidaten")
SPEC = os.path.join(K.EDEN, "docs", "abnahme", "angeln_bilder.json")

# Positiv formuliert (Krea CFG 1: Verneinungen wirken nicht, "angler"/"no fishing rod" holte Menschen und Ruten erst ins Bild)
AUFTEILUNG = ("Composition: the left two thirds of the frame are open calm water with a gently rippled clear surface reaching "
              "into the distance, wide and uninterrupted; the right third is the {ufer} in the foreground, deserted, bare and "
              "quiet. Seen from a seated eye level slightly above the water, wide angle, photorealistic, natural colours, "
              "a peaceful empty scene")
ORTE = {
    "meer": [
        ("Badeplattform am Nachmittag", "the teak swim platform at the stern of a luxury superyacht",
         "Wide photograph from the swim platform of a superyacht anchored off a Mediterranean coast in the afternoon, turquoise clear sea"),
        ("Achterdeck zur goldenen Stunde", "polished teak aft deck with a chrome railing of a superyacht",
         "Wide photograph from the aft deck of a superyacht at golden hour, warm low sun over a calm deep blue Mediterranean"),
        ("Granitbucht auf Korsika", "smooth flat red granite rocks of the shore",
         "Wide photograph of a quiet cove on the Corsican coast with red granite cliffs in the distance, clear green-blue water"),
        ("Hafenmole am Abend", "old stone breakwater of a small fishing harbour with an iron bollard",
         "Wide photograph from the stone mole of a small Corsican fishing harbour in the warm evening, a lighthouse far in the distance"),
        ("Bug im Morgendunst", "teak foredeck of a superyacht with a coiled anchor line",
         "Wide photograph from the bow of a superyacht at dawn, soft morning haze over a glassy pale-blue sea"),
        ("Badeplattform bei Nacht", "teak swim platform of a superyacht lit by warm deck lights",
         "Wide photograph from a superyacht swim platform at night, the underwater lights glow turquoise in the sea, a full moon"),
        ("Holzsteg eines Strandclubs", "weathered wooden jetty of a beach club with a rope railing",
         "Wide photograph from the end of a wooden jetty at a Mediterranean beach club in the late afternoon, sandy shallows"),
        ("Felsküste bei Sonnenuntergang", "flat warm limestone rocks of the shore",
         "Wide photograph from a rocky Mediterranean shore at sunset, the sea glowing orange and violet, a calm horizon"),
        ("Aus dem Beiboot", "grey rubber tube and wooden seat of a yacht tender",
         "Wide photograph from a small yacht tender drifting in a sheltered bay, deep blue water, green maquis hills far away"),
        ("Leuchtturmfelsen", "rough grey rocks below an old white lighthouse",
         "Wide photograph from the rocks below an old Mediterranean lighthouse in clear midday light, deep cobalt sea"),
    ],
    "fluss": [
        ("Bach unter der Steineiche", "mossy bank under an old holm oak with a small stone fire ring",
         "Wide photograph of a quiet pool in a clear creek in the Corsican maquis in warm afternoon light, yellow broom on the far bank"),
        ("Bergsee", "smooth granite boulders of the shore",
         "Wide photograph of a clear mountain lake in Corsica surrounded by granite peaks, deep green water, a few pines"),
        ("Fluss an der Steinbrücke", "grassy bank beside an old arched stone bridge",
         "Wide photograph of a slow Tuscan river at an old Roman stone arch bridge, cypresses on the far bank, soft evening light"),
        ("Alte Wassermühle", "worn stone wall of an old water mill with a wooden wheel",
         "Wide photograph of a calm mill pond behind an old Tuscan stone water mill, willows on the far bank, morning light"),
        ("Seesteg im Morgennebel", "short wooden jetty with a rope coiled on the planks",
         "Wide photograph of a still lake at dawn with soft mist on the water, reeds and alder trees along the far shore"),
        ("Gumpe am Wasserfall", "mossy rounded rocks beside a small waterfall",
         "Wide photograph of a clear emerald pool below a small forest waterfall, ferns and old chestnut trees around it"),
        ("Pappelfluss am Kiesufer", "pale gravel bank of the river",
         "Wide photograph of a wide slow river at golden hour, tall poplars along the far bank, warm light on the water"),
        ("Schlucht mit Smaragdbecken", "smooth pale granite slabs of the gorge",
         "Wide photograph of a deep emerald river pool in a granite gorge in Corsica, pine trees high on the rocks, bright noon"),
        ("Klosterteich", "old stone edge of a monastery fish pond with a stone bench",
         "Wide photograph of a calm old stone fish pond in a monastery garden, cypresses and a bell tower far behind, dusk"),
        ("Lagune mit Flamingos", "sandy bank with salt grass",
         "Wide photograph of a calm coastal lagoon in Corsica in the evening, a few pink flamingos far away on the water, low hills"),
    ],
}
KOEDER = {   # Stufe: (Name, Bauart, [4 Farbvarianten])
    # Stufe 0 (Duc 03.11.2026): Standard-Schwimmer ohne Bonus, solange bei Petru nichts gebaut ist - ersetzt den CSS-Schwimmer
    0: ("Bottle Cork", "a plain wine bottle cork used as a home-made fishing float, a seagull feather pushed upright into its top, "
        "a thin clear fishing line tied around its middle with a small silver hook hanging below",
        ["natural light brown cork with a clean white gull feather", "natural cork with one painted red ring and a soft grey gull feather",
         "a mushroom-shaped champagne cork with a white and grey gull feather", "dark weathered cork wrapped with blue twine and a white gull feather"]),
    1: ("Cork Float", "a classic round cork fishing float with a short wooden stick through it, a simple hook and a small worm bait below",
        ["painted red on top and white below", "painted yellow on top and black below", "painted orange on top and natural cork below",
         "painted green on top and white below"]),
    2: ("Balsa Float", "a slim professional hand-painted balsa wood fishing float with a long fine antenna tip, glossy varnish",
        ["with a bright fluorescent orange tip and a black body", "with a fluorescent yellow tip and a dark green body",
         "with a fluorescent red tip and a cream white body", "with a fluorescent pink tip and a deep blue body"]),
    3: ("Wooden Lure", "a handcrafted wooden fishing lure shaped like a small fish with a clear diving lip and two small silver treble hooks, glossy lacquer",
        ["painted like a silver sardine with a blue back", "painted like a golden perch with dark stripes",
         "painted like a red mullet with a pink belly", "painted like a green-gold trout with a white belly"]),
}
# Duc 28.10. (Abnahme): jeder Koeder vollstaendig im Bild, nichts angeschnitten, mit Rand - klein im Bild, alles sichtbar
KOEDER_STIL = ("Studio product photograph of {motiv}, {farbe}, seen from the side, small in the centre of the frame, every part of it "
               "fully visible from end to end with a wide empty margin on all sides, {grund}, photorealistic, sharp detail, no text")
KOEDER_RAND = 0.08                # transparenter Rand je Seite (Anteil der groesseren Kante), nach dem Freistellen


def ort_jobs(nur):
    for art, liste in ORTE.items():
        if nur and art not in nur and "orte" not in nur:
            continue
        for k, (_, ufer, szene) in enumerate(liste, 1):
            yield "eden_rise_angeln_%s_%02d" % (art, k), szene + ". " + AUFTEILUNG.format(ufer=ufer)


def koeder_jobs():
    for stufe, (_, motiv, farben) in KOEDER.items():
        for n, farbe in enumerate(farben, 1):
            yield "koeder_%d_%d" % (stufe, n), KOEDER_STIL.format(motiv=motiv, farbe=farbe, grund=K.GRUND)


def rand_dazu(pfad):
    """Freigestelltes Sprite liegt eng auf dem Motiv - fuer die Koeder ein transparenter Rand ringsum (Duc 28.10.)."""
    from PIL import Image
    im = Image.open(pfad).convert("RGBA")
    r = int(max(im.size) * KOEDER_RAND)
    neu = Image.new("RGBA", (im.width + 2 * r, im.height + 2 * r), (0, 0, 0, 0))
    neu.paste(im, (r, r))
    neu.save(pfad, "PNG", optimize=True)


def erzeugen(arten):
    os.makedirs(VAR, exist_ok=True)
    os.makedirs(KOEDER_ZIEL, exist_ok=True)
    gross = os.path.join(K.MOD, "farm", "_gross")
    lauf = {}
    if "orte" in arten:
        for name, prompt in ort_jobs(None):
            if not os.path.exists(os.path.join(VAR, name + ".png")):
                g = IB.graph(prompt, VAR, name, random.randint(1, 2 ** 31), True)
                g["6"]["inputs"].update({"width": 1664, "height": 928})
                lauf[name] = (IB.post("/prompt", {"prompt": g})["prompt_id"], prompt, "ort", 1)
    if "koeder" in arten:
        for name, prompt in koeder_jobs():
            if not os.path.exists(os.path.join(KOEDER_ZIEL, name + ".png")):
                g = K.graph_mit_freistellung(prompt, gross, name, random.randint(1, 2 ** 31))
                lauf[name] = (IB.post("/prompt", {"prompt": g})["prompt_id"], prompt, "koeder", 1)
    print("eingereiht: %d" % len(lauf), flush=True)
    t0 = time.time()
    while lauf and time.time() - t0 < 60 * 45:
        time.sleep(3)
        for name, (pid, prompt, typ, versuch) in list(lauf.items()):
            h = IB.get("/history/" + pid)
            if not (pid in h and h[pid].get("status", {}).get("completed")):
                continue
            if typ == "koeder":
                ok = K.sprite_fertig(gross, name, os.path.join(KOEDER_ZIEL, name + ".png"), letzter=versuch >= K.VERSUCHE)
                if not ok and versuch < K.VERSUCHE:
                    g = K.graph_mit_freistellung(prompt, gross, name, random.randint(1, 2 ** 31))
                    lauf[name] = (IB.post("/prompt", {"prompt": g})["prompt_id"], prompt, typ, versuch + 1)
                    continue
                rand_dazu(os.path.join(KOEDER_ZIEL, name + ".png"))
            print("fertig: %s" % name, flush=True)
            lauf.pop(name)
    print("offen: %s" % (", ".join(lauf) or "nichts"))


def spec():
    items = []
    for art, liste in ORTE.items():
        for k, (titel, _, _) in enumerate(liste, 1):
            items.append({"id": "%s_%02d" % (art, k), "titel": "%s %d · %s" % ("Meer" if art == "meer" else "Fluss/See", k, titel),
                          "bild": os.path.join(VAR, "eden_rise_angeln_%s_%02d.png" % (art, k)),
                          "soll": "Links offenes Wasser für den Köder, rechts Ufer/Deck. 3 je Gewässer mit OK markieren."})
    for stufe, (name, _, farben) in KOEDER.items():
        for n, farbe in enumerate(farben, 1):
            items.append({"id": "koeder_%d_%d" % (stufe, n), "titel": "Köder Stufe %d · %s · Variante %d" % (stufe, name, n),
                          "bild": os.path.join(KOEDER_ZIEL, "koeder_%d_%d.png" % (stufe, n)),
                          "soll": "Eine Variante je Stufe mit OK markieren (%s)." % farbe})
    json.dump({"id": "angeln_bilder", "titel": "Angeln – Orte und Köder zur Auswahl",
               "hinweis": "Je Gewässer (Meer, Fluss/See) 3 Orte mit OK markieren, je Köder-Stufe 1 Variante. Notizen für Änderungswünsche.",
               "items": items}, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: %s (%d Bilder)" % (SPEC, len(items)))


def uebernehmen():
    """Gewaehlte Kandidaten als Angel-Hintergrund der Plaetze kopieren (kochen_daten.QUELLEN angel_bild ->
    ST\\backgrounds\\eden_rise_angeln_<platz>.png, die Engine liest nur die oberste Ebene)."""
    import shutil
    sys.path.insert(0, os.path.join(HIER, "eden_rise"))
    import kochen_daten as D
    for pid, q in D.QUELLEN.items():
        if q.get("wasser"):
            quelle = os.path.join(VAR, "eden_rise_angeln_%s.png" % q["angel_bild"])
            ziel = os.path.join(HB.ST_BG, "eden_rise_angeln_%s.png" % pid)
            if os.path.isfile(quelle):
                shutil.copyfile(quelle, ziel)
                print("%-12s <- %s" % (pid, q["angel_bild"]))
            else:
                print("FEHLT %s: %s" % (pid, quelle))
    # Wechselbilder (Duc 28.10.: alle 20 nutzen) - jeder Angelgang zieht eines davon (kochen_daten.ANGEL_BILDER)
    for liste in D.ANGEL_BILDER.values():
        for datei in liste:
            quelle = os.path.join(VAR, datei)
            if os.path.isfile(quelle):
                shutil.copyfile(quelle, os.path.join(HB.ST_BG, datei))
            else:
                print("FEHLT %s" % quelle)
    print("Wechselbilder: %d" % sum(len(x) for x in D.ANGEL_BILDER.values()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "uebernehmen" in sys.argv:
        uebernehmen()
        sys.exit()
    arten = {a for a in sys.argv[1:] if a in ("orte", "koeder")} or {"orte", "koeder"}
    if "--spec" not in sys.argv:
        IB.get("/system_stats")
        erzeugen(arten)
    spec()

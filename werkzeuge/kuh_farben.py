# -*- coding: utf-8 -*-
r"""Kuh-Farben zum Vergleich (Duc 28.10.2026: "schwarze Kuehe, auch braune und schwarz-weiss fleckige zum Vergleich").

    python werkzeuge\kuh_farben.py            fehlende Kandidaten erzeugen + Abnahme-Spec schreiben
    python werkzeuge\kuh_farben.py --spec     nur die Spec docs\abnahme\kuehe_farben.json schreiben

Je Farbe die 5 Varianten wie im Stall (baby, adult_m, adult_f, old_m, old_f), freigestellt wie in kochen_bilder.py, nach
module\eden_rise\farm\_kandidaten\cow_<farbe>_<variante>.png. Die Spiel-Sprites (farm\tiere\cow_*.png) bleiben unberuehrt;
die Abnahme-Seite legt die heutige weisse Chianina daneben."""
import json, os, random, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import kochen_bilder as K  # noqa: E402

ZIEL = os.path.join(K.MOD, "farm", "_kandidaten")
SPEC = os.path.join(K.EDEN, "docs", "abnahme", "kuehe_farben.json")
FARBEN = {  # farbe: (Titel, Rasse, Fell)
    "schwarz": ("Schwarz – Pisana (Toskana, Pisa)", "Pisana",
                "a solid very dark chestnut coat that looks almost black, short smooth hair, short curved horns, dark muzzle"),
    "braun": ("Braun – Bruna (Italian Brown)", "Italian Brown",
              "a solid warm grey-brown coat, short smooth hair, a pale ring around the dark muzzle, short curved horns"),
    "fleckig": ("Schwarz-weiß gefleckt – Frisona (Holstein)", "Holstein Friesian",
                "a black and white coat in a few large clearly separated patches, short smooth hair, pink-white muzzle"),
}
WER = {"baby": "a small newborn {rasse} calf with a smooth rounded hornless head, leggy with large soft ears",   # ohne Hoerner: Geschlecht noch offen
       "adult_m": "a male {rasse} bull with a massive muscular neck and broad chest, no udder",
       "adult_f": "a female {rasse} dairy cow with a slim body and a visible udder",
       "old_m": "an old male {rasse} bull with a massive neck and a weathered look, no udder",
       "old_f": "an old female {rasse} dairy cow with a visible udder and a weathered look"}
VARIANTE = {"baby": "Baby", "adult_m": "Bulle", "adult_f": "Kuh", "old_m": "alter Bulle", "old_f": "alte Kuh"}


def jobs():
    for farbe, (_, rasse, fell) in FARBEN.items():
        for v, wer in WER.items():
            motiv = wer.format(rasse=rasse) + ", " + fell
            yield "cow_%s_%s" % (farbe, v), K.TIER_STIL.format(motiv=motiv, grund=K.GRUND)


def erzeugen():
    offen = {n: p for n, p in jobs() if not os.path.exists(os.path.join(ZIEL, n + ".png"))}
    if not offen:
        return print("Alle Kandidaten sind da.")
    gross = os.path.join(K.MOD, "farm", "_gross")
    os.makedirs(gross, exist_ok=True)

    def einreihen(name, prompt):
        g = K.graph_mit_freistellung(prompt, gross, name, random.randint(1, 2 ** 31))
        return K.IB.post("/prompt", {"prompt": g})["prompt_id"]

    lauf = {n: (einreihen(n, p), p, 1) for n, p in offen.items()}
    print("eingereiht: %d" % len(lauf), flush=True)
    t0 = time.time()
    while lauf and time.time() - t0 < 60 * 30:
        time.sleep(2)
        for name, (pid, prompt, versuch) in list(lauf.items()):
            h = K.IB.get("/history/" + pid)
            if pid in h and h[pid].get("status", {}).get("completed"):
                ok = K.sprite_fertig(gross, name, os.path.join(ZIEL, name + ".png"), letzter=versuch >= K.VERSUCHE)
                if not ok and versuch < K.VERSUCHE:
                    lauf[name] = (einreihen(name, prompt), prompt, versuch + 1)
                    continue
                print("fertig: %s" % name, flush=True)
                lauf.pop(name)
    print("offen: %s" % (", ".join(lauf) or "nichts"))


def spec():
    # Seit 28.10. (Duc: "ich nehme die schwarzen Kuehe"): oben die Spiel-Sprites (Pisana) mit der alten Chianina daneben
    items = [{"id": "cow_%s" % v, "titel": "Im Spiel: Pisana · %s" % VARIANTE[v],
              "bild": os.path.join(K.MOD, "farm", "tiere", "cow_%s.png" % v),
              "soll": "Finale Kuh im Stall (schwarze Pisana). Rechts die frühere weiße Chianina.",
              "vergleich": os.path.join(ZIEL, "cow_weiss_%s.png" % v), "vergleich_titel": "Vorher: Chianina"} for v in WER]
    return json.dump({"id": "kuehe_final", "titel": "Kühe – final im Stall (Pisana)",
                      "hinweis": "Die fünf Stall-Sprites der Kuh, wie sie jetzt im Spiel sind. Rechts die frühere weiße Chianina.",
                      "items": items}, open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def spec_kandidaten():
    items = []
    for farbe, (titel, _, _) in FARBEN.items():
        for v in WER:
            items.append({"id": "cow_%s_%s" % (farbe, v), "titel": "%s · %s" % (titel, VARIANTE[v]),
                          "bild": os.path.join(ZIEL, "cow_%s_%s.png" % (farbe, v)),
                          "soll": "Kandidat für die Kuh im Stall. Rechts die heutige Chianina in derselben Variante.",
                          "vergleich": os.path.join(K.MOD, "farm", "tiere", "cow_%s.png" % v), "vergleich_titel": "Jetzt: Chianina"})
    json.dump({"id": "kuehe_farben", "titel": "Kühe – Farben im Vergleich",
               "hinweis": "Welche Farbe soll die Kuh im Stall haben? OK bei der Farbe, die bleiben soll, Neu mit Notiz bei allem, was "
                          "anders werden soll. Rechts jeweils die heutige weiße Chianina.", "items": items},
              open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: %s (%d Bilder)" % (SPEC, len(items)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--spec" not in sys.argv:
        erzeugen()
    spec()

# -*- coding: utf-8 -*-
"""Freie Szenen nach dem Spieltest vom 29.10.2026 (Giftige Blume, 318 Antworten): "Time with ..." auch fuer Maxwell,
Totò, Petru und Jana, ohne die Romanzen zu verdraengen; Floskel-Bremse, eigene Gesten und Pronomen im Szenen-Prompt.

  python tests\\test_freie_zeit.py
"""
import collections, random, sys, tempfile, os

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import lauf_test as L  # noqa: E402

E = L.eden
PH = ["fruehstueck", "tag", "nachmittag", "dinner", "abend", "nacht"]


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    L.vorbereiten("eden_rise", tempfile.mkdtemp(prefix="eden_frei_"))
    from kern import hauptstory as H, szene as S
    z = E.aktion("neu", {"modus": "ironman"})
    modul = E.modul_laden()
    bu = H.buehne(E.moddir(z["modul"]))
    z["bekannt"], z["verlauf"] = list(modul["personen"]), []
    z["werte"]["ruf"] = 2                                   # Petrus Werkstatt offen
    rng, gew, zaehler, holm_spaet = random.Random(3), random.Random(5), collections.Counter(), 0
    for tag in range(1, 16):
        z["tag"], z["heute"], heute = tag, [], {}
        for ph in PH:
            z["phase"] = ph
            karten = H.frei_phase(z, modul, ph, rng, bu, 3, heute)
            wer = [s["anwesend"][0] for s in karten]
            zaehler.update(wer)
            holm_spaet += tag >= 3 and "holm" in wer
            if wer:
                z["heute"].append({"anwesend": [gew.choice(wer)], "phase": ph, "kurz": ""})
                for s in karten:
                    if modul["personen"][s["anwesend"][0]].get("pronomen") == "er":
                        pruefen("his own way" in s["figuren"][s["anwesend"][0]]["will"], "Wunsch mit 'his' (%s)" % s["titel"])
        z["verlauf"] += [dict(h, tag=tag) for h in z["heute"]]
    gesamt = sum(zaehler.values())
    romanze = sum(n for p, n in zaehler.items() if p in H.frauen(modul))
    print("angeboten:", dict(zaehler.most_common()))
    for p in ("maxwell", "toto", "petru", "jana"):
        pruefen(zaehler[p] >= 8, "%s bekommt freie Zeit (%d Karten)" % (p, zaehler[p]))
    pruefen(romanze >= 0.75 * gesamt, "Romanzen behalten den Vorrang (%d von %d)" % (romanze, gesamt))
    pruefen(holm_spaet == 0, "Holm ab Tag 3 nicht mehr (evakuiert)")

    # Prompt: Pronomen, Gesten, Floskel-Sperre
    z["tag"], z["phase"] = 4, "abend"
    z["persona"] = z.get("persona") or {"oeffentlich": "the new First Officer"}
    s = H.frei_phase(z, modul, "abend", random.Random(1), bu, 1, {})[0]
    s.update({"anwesend": ["petru"], "ort": "petru_workshop", "figuren": {"petru": {"will": "Spend some time."}}})
    sz = {"def": s, "figuren": ["petru"], "auftraege": {"petru": {"will": "x", "verbirgt": "y", "grenze": "z"}},
          "log": [{"wer": "petru", "text": "He lets out a long sigh and freezes."}], "zug": 1}
    pr = S.figur_prompt(z, modul, sz, "petru")
    pruefen("{she}" not in pr and "{Her_p}" not in pr and "he follows Duc's lead" in pr, "Regeln mit Pronomen 'he'")
    pruefen("mends a net that isn't torn" in pr, "Petrus eigene Gesten im Prompt")
    pruefen("stops it himself" in pr, "Grenze mit 'himself'")
    pruefen("Stock phrases are banned" in pr, "Floskel-Verbot in den Regeln")
    pruefen(S.floskeln_der_szene(sz, "petru") == ["lets out a long sigh", "freezes"], "benutzte Floskeln erkannt")
    pr_f = S.figur_prompt(z, modul, dict(sz, figuren=["chiara"], auftraege={}), "chiara")
    pruefen("she follows Duc's lead" in pr_f and "rates something out loud" in pr_f, "Chiara: 'she' und eigene Gesten")
    print("OK")


if __name__ == "__main__":
    main()

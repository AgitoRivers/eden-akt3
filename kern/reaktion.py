# -*- coding: utf-8 -*-
"""Reaktionen auf jede Antwort von Duc (16.10.2026, Duc: "jede Antwort hat bereits Einfluss auf Moral, Sympathie usw.,
erstmal nur positiv, damit der Spieler versteht, wie die Mechanik laeuft").

Nach jedem freien Zug urteilt das Sprachmodell knapp, wie jede anwesende Frau das Gesagte aufnimmt (vertraut /
angetan / missfaellt / egal) und ob die Crew-Moral steigt. Die Regeln stehen hier im Code:
  - eine Zustimmung = +1/2 Punkt (Rest wird gemerkt) - so zeigt jede Antwort eine Wirkung, ohne die Werte aufzublasen;
  - am ersten Tag zaehlt die erste Zustimmung je Wert und Szene voll (+1), damit der Spieler die Zahl sofort steigen sieht;
  - am ersten Tag gibt es nur Positives, und jede Antwort bewirkt etwas (notfalls bei der angesprochenen Frau);
  - ab Tag 2 kann eine Antwort auch missfallen (-1/2).
Wahlmomente haben eigene, feste Folgen - dort urteilt dieses Modul nicht."""
from . import figurenrahmen, llm, rollen, zustand

STUFEN = ["none", "trust", "desire", "dislike"]
CREW_STUFEN = ["none", "up", "down"]
NUR_POSITIV_BIS_TAG = 1
# Gespraeche tragen Sympathie bis 3, darueber nur Erlebnisse (Bogen-Szenen, Wahlmomente, Ausgaenge) - sonst stuenden
# nach einer Woche alle Frauen auf 5/5 und das Herz-Ende waere Zufall (Trockenlauf 16.10.2026).
DECKEL = {"vertrauen": 3, "begehren": 3, "moral": 4}

SYSTEM = """You judge, for a story game, how the women present react to what Duc just said or did. Judge only Duc's latest message, in the context of the scene. Be fair and quick.
For each woman pick one:
- "trust": she respects it, agrees, feels heard, taken seriously or cared for, or it shows competence she values.
- "desire": a compliment, charm, flirt or a moment of closeness lands with her.
- "dislike": it is rude, dismissive, unfair or goes against what she wants.
- "none": it does not concern her or leaves her cold.
"crew": "up" if Duc leads well - clear, calm, fair, encouraging - "down" if he spreads panic or chaos, else "none"."""


def grammatik(frauen, crew):
    felder = ['"\\"%s\\":" ws r' % f for f in frauen] + (['"\\"crew\\":" ws c'] if crew else [])
    r = " | ".join('"\\"%s\\""' % s for s in STUFEN)
    c = " | ".join('"\\"%s\\""' % s for s in CREW_STUFEN)
    return ('root ::= "{" ws ' + ' "," ws '.join(felder) + ' ws "}"\nr ::= ' + r + "\nc ::= " + c +
            '\nws ::= [ \\t\\n]*')


def _frauen(modul, sz):
    """Wer auf getippten Text reagiert. Figuren mit Rahmen nicht: bei ihnen zaehlt nur Zeit und Geste (Duc 31.10.2026)."""
    return [p for p in sz["figuren"] if modul["personen"].get(p, {}).get("romanzierbar") and not figurenrahmen.gilt(modul, p)]


def urteilen(z, modul, sz, text, mitschrift, kurz):
    frauen = _frauen(modul, sz)
    crew = len([p for p in sz["figuren"] if rollen.ist(modul, "crew", p)]) >= 2
    if not frauen and not crew:
        return {}
    wuensche = "\n".join("- %s wants: %s" % (kurz(modul, p), (sz["auftraege"].get(p) or {}).get("will", ""))
                         for p in frauen)
    user = ("The scene so far:\n\n%s\n\nWhat the women want in this scene:\n%s\n\nDuc's latest message:\n%s\n\n"
            "Answer with one word per woman%s." % (mitschrift, wuensche, text, " and for the crew" if crew else ""))
    try:
        u, _ = llm.json_chat(SYSTEM, user, grammatik(frauen, crew), max_tokens=60)
    except Exception:
        u = None
    return u or {}


def anwenden(z, modul, sz, text, urteil, kurz):
    """Urteil -> Werte (halbe Punkte) + Anzeige-Zeilen. Liefert Log-Eintrag oder None."""
    frauen = _frauen(modul, sz)
    nur_positiv = z["tag"] <= NUR_POSITIV_BIS_TAG
    wirkung = []                                       # (wert, richtung, anzeige)
    for p in frauen:
        r = urteil.get(p, "none")
        if r == "dislike" and nur_positiv:
            r = "none"
        name = kurz(modul, p)
        if r == "trust":
            wirkung.append(("vertrauen." + p, 1, "%s likes that" % name))
        elif r == "desire":
            wirkung.append(("begehren." + p, 1, "%s is charmed" % name))
        elif r == "dislike":
            wirkung.append(("vertrauen." + p, -1, "%s doesn't like that" % name))
    c = urteil.get("crew", "none")
    if c == "up":
        wirkung.append(("moral", 1, "The crew takes heart"))
    elif c == "down" and not nur_positiv:
        wirkung.append(("moral", -1, "The crew gets restless"))
    if nur_positiv and not wirkung and frauen:         # Tag 1: jede Antwort bewirkt etwas
        p = next((x for x in frauen if kurz(modul, x) in text), frauen[0])
        wirkung.append(("vertrauen." + p, 1, "%s likes that" % kurz(modul, p)))
    if not wirkung:
        return None
    rest = z.setdefault("neigung", {})
    voll = sz.setdefault("reaktion_voll", [])
    zeilen, werte = [], []
    for wert, richtung, anzeige in wirkung:
        zeilen.append({"text": anzeige, "ton": "gut" if richtung > 0 else "schlecht"})
        if zustand.ist_achse(wert):                    # Punkte-Skala: +2 je Zustimmung (Tag 1: erste je Szene +8), bis 36
            erst = richtung > 0 and z["tag"] == 1 and wert not in voll
            if erst:
                voll.append(wert)
            werte += zustand.punkte_add(z, modul, wert, (8 if erst else 2) * richtung,
                                        deckel=zustand.GESPRAECH_DECKEL if richtung > 0 else None, quelle="szenen")
            continue
        if richtung > 0 and z["werte"].get(wert, 0) >= DECKEL.get(wert.split(".")[0], 5):
            continue                                   # Reaktion sichtbar, Wert steigt nur noch durch Erlebnisse
        if richtung > 0 and z["tag"] == 1 and wert not in voll:
            schritt = 1.0
            voll.append(wert)
        else:
            schritt = 0.5 * richtung
        neu = rest.get(wert, 0.0) + schritt
        ganz = int(neu)                                # Richtung Null runden: nur volle Punkte zaehlen
        rest[wert] = round(neu - ganz, 2)
        if ganz:
            werte += zustand.folgen_anwenden(z, modul, [{"wert": wert, "delta": ganz, "moral_art": "alltag"}
                                                        if wert == "moral" else {"wert": wert, "delta": ganz}])
    return {"art": "reaktion", "zeilen": zeilen, "werte": werte}

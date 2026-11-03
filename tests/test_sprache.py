# -*- coding: utf-8 -*-
r"""Sprach-Pruefer (28.10.2026, Duc: "alles, was der Spieler sieht, ist Englisch"): spielt per Bot wie
tests/spieltest_akt1.py durch und sammelt jeden Text der Spieleransicht (GET /api/stand), der nach Deutsch aussieht.
Exit 1, wenn etwas gefunden wird. Ausgabe: Fundstelle (Feldname) + Textanfang, haeufigste zuerst.

  python tests\test_sprache.py              Seed 1 (dauert einige Minuten)
  python tests\test_sprache.py --seeds 1 2  mehrere Seeds

Erlaubte Eigennamen mit Umlaut stehen in spieltest_akt1.NAMEN_OK. Die Pruefung ist grob (Umlaute und haeufige
deutsche Woerter); ein Treffer heisst "ansehen", nicht zwingend "falsch".
"""
import argparse, collections, os, re, sys, types

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import spieltest_akt1 as S  # noqa: E402  (setzt PYTHONHASHSEED=0 ueber lauf_test)

# Felder, die der Spieler im normalen Spiel nicht sieht (Debug), und englische Treffer der groben Pruefung
NICHT_SICHTBAR = ("plan_fehler",)
FEHLALARM = re.compile(r"Or die\b|\bim (saving|going|not|the bar|still)\b|\bdie\b.*\b(would|will)\b|"
                       r"\bwould die\b|\bI would die\b|\bthe girl will die\b|\bheard it die\b|holds the hat|\b(a|the|little|wool|his|her|my|your) hat\b", re.I)      # englisch "hat" = Hut


class _AlleZaehler(collections.Counter):
    """spieltest_akt1 gibt nur die 40 haeufigsten Funde zurueck - hier alle."""
    def most_common(self, n=None):
        return super().most_common()


S.collections = types.SimpleNamespace(**{k: getattr(collections, k) for k in dir(collections) if not k.startswith("_")})
S.collections.Counter = _AlleZaehler
# schaerfer als spieltest_akt1.DE: auch deutsche Woerter ohne Umlaut ("Nachricht von", "Stufe")
_DE = __import__("re").compile(S.DE.pattern[:-3] + r"|von|nach|oder|aber|schon|Stufe|Nachricht|fertig|"
                                r"erledigt|geschafft|bekommt|gefunden)\b")


class _DeOhneFehlalarm:
    """Prueft den ganzen Text ohne die englischen Fehlalarme - der Befund zeigt nur die ersten 90 Zeichen, ein "hat"
    weiter hinten (Chiaras Legende, 30.10.2026) liess sich dort nicht mehr als Fehlalarm erkennen."""
    pattern = _DE.pattern

    def search(self, t):
        return _DE.search(FEHLALARM.sub(" ", t))


S.DE = _DeOhneFehlalarm()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[1])
    ap.add_argument("--max", type=int, default=60, help="hoechstens so viele Funde ausgeben")
    a = ap.parse_args()
    funde = {}
    for seed in a.seeds:
        r = S.lauf(seed)
        for text, n in r["befund"]["deutsch"]:
            feld, _, inhalt = text.partition(" | ")
            if feld.startswith(NICHT_SICHTBAR) or FEHLALARM.search(inhalt):
                continue
            funde[text] = funde.get(text, 0) + n
        if r["befund"]["fehler"]:
            print("Seed %d: Absturz %s" % (seed, r["befund"]["fehler"]))
    if not funde:
        print("Sprache: keine deutschen Texte in der Spieleransicht gefunden.")
        return 0
    print("Sprache: %d deutsche Texte in der Spieleransicht (Feld | Textanfang, Anzahl Anzeigen):" % len(funde))
    for text, n in sorted(funde.items(), key=lambda x: -x[1])[:a.max]:
        print("%6d  %s" % (n, text))
    return 1


if __name__ == "__main__":
    sys.exit(main())

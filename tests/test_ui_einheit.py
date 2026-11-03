# -*- coding: utf-8 -*-
"""Waechter der Oberflaeche (Duc 30.10.2026, docs/wiki/systeme/ui_stil.md): Einzelloesungen duerfen nur weniger werden.

Zaehlt in client/ die Emoji und Symbolzeichen sowie die verschiedenen Schriftgroessen, Radien und Hexfarben. Keine Zahl darf
ueber den Stand in tests/ui_einheit_stand.json steigen. Wird eine kleiner, schreibt --speichern den neuen, strengeren Stand;
hoeher geht nur mit --erhoehen und einem Grund von Duc.

  python tests\\test_ui_einheit.py [--speichern] [--erhoehen]
"""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT = os.path.join(EDEN, "client")
STAND = os.path.join(EDEN, "tests", "ui_einheit_stand.json")
SYMBOL = re.compile("[\u23e9-\u23fa☀-➿⬀-⯿\U0001f000-\U0001faff]")
sys.path.insert(0, os.path.join(EDEN, "werkzeuge"))
from ui_icons import ICONS  # noqa: E402


def dateien():
    for wurzel, ordner, namen in os.walk(CLIENT):
        ordner[:] = [o for o in ordner if o not in ("wiki", "node_modules")]
        for n in namen:
            if n.endswith((".js", ".css", ".html")) and n != "index_text.html":
                yield os.path.join(wurzel, n)


def ohne_tabelle(t):
    """Die Tabelle EMOJI in eden-ui.js ist die eine erlaubte Stelle: sie uebersetzt Servertexte in Icons."""
    return re.sub(r"const EMOJI = \{.*?\};", "", t, flags=re.S)


def zaehlen():
    text = "\n".join(ohne_tabelle(open(p, encoding="utf-8").read()) for p in dateien())
    return {"symbole": len(SYMBOL.findall(text)),
            # feste Werte statt Tokens; der font-Kurzwert zaehlt mit
            "schriftgroessen": len(set(re.findall(r"font-size:\s*([\d.]+px)", text) + re.findall(r"\bfont:\s*(?:italic\s+)?(?:\d{3}\s+)?([\d.]+px)", text))),
            "radien": len(set(re.findall(r"border-radius:\s*([\d.]+px)", text))),
            # feste Abstaende ueber 3 px in padding, margin, gap (grosse Layoutwerte bleiben erlaubt, zaehlen aber mit)
            "abstaende": len({v for d in re.findall(r"\b(?:padding|margin)(?:-[a-z]+)?\s*:([^;}\"'`]+)|\bgap\s*:([^;}\"'`]+)", text)
                              for v in re.findall(r"(?<![\w.\-])(\d+(?:\.\d+)?)px", d[0] + d[1]) if float(v) > 3}),
            "hexfarben": len({h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", text)})}


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    jetzt = zaehlen()
    alt = json.load(open(STAND, encoding="utf-8")) if os.path.exists(STAND) else {}
    zu_hoch = {k: (jetzt[k], alt[k]) for k in jetzt if k in alt and jetzt[k] > alt[k]}
    if "--speichern" in sys.argv:
        if zu_hoch and "--erhoehen" not in sys.argv:
            raise SystemExit("Hoeher als der Stand, nicht gespeichert: %s" % zu_hoch)
        with open(STAND, "w", encoding="utf-8", newline="\n") as f:
            json.dump(jetzt, f, indent=1)
            f.write("\n")
        print("Stand gespeichert:", jetzt)
        return
    if not alt:
        raise SystemExit("Noch kein Stand: python tests\\test_ui_einheit.py --speichern")
    pruefen(not zu_hoch, "keine neuen Einzelloesungen %s (Stand %s). Zu hoch: %s. Regeln: docs/wiki/systeme/ui_stil.md" % (jetzt, alt, zu_hoch))
    sprite = open(os.path.join(CLIENT, "plugins", "eden-ui", "icons.svg"), encoding="utf-8").read()
    pruefen(all('id="%s"' % k in sprite for k in ICONS), "jedes Wort aus dem Icon-Woerterbuch steht im Sprite")
    pruefen(len(set(ICONS.values())) == len(ICONS), "ein Begriff, ein Icon: kein Icon doppelt vergeben")
    # Icon-Namen sind IDs im Dokument: heisst ein Icon wie ein Element, findet $("name") das Icon (Duc 01.11.2026: Figuren am linken Rand)
    seiten_ids = set(re.findall(r'\bid="([A-Za-z][\w-]*)"', open(os.path.join(CLIENT, "index.html"), encoding="utf-8").read()))
    pruefen(not seiten_ids & set(ICONS), "kein Icon heisst wie ein Element der Seite: %s" % sorted(seiten_ids & set(ICONS)))
    benutzt = {n for p in dateien() for n in re.findall(r'(?:uiIc|EdenUI\.icon)\("([a-z0-9-]+)"', open(p, encoding="utf-8").read())} - {"name"}   # "name" = Beispiel im Kopfkommentar
    pruefen(benutzt <= set(ICONS), "jedes benutzte Icon steht im Woerterbuch: %s" % sorted(benutzt - set(ICONS)))
    ui = ohne_tabelle(open(os.path.join(CLIENT, "plugins", "eden-ui", "eden-ui.js"), encoding="utf-8").read()) + \
        open(os.path.join(CLIENT, "plugins", "eden-ui", "eden-ui.css"), encoding="utf-8").read()
    pruefen(not SYMBOL.search(ui), "die gemeinsamen Bausteine nutzen keine Emoji")
    genutzt = set(re.findall(r'"(mood-[a-z]+|power|diesel|reputation|energy)"', open(os.path.join(CLIENT, "index.html"), encoding="utf-8").read()))
    pruefen(genutzt <= set(ICONS), "die Kopfzeile nutzt nur Icons aus dem Woerterbuch")
    alles = "\n".join(open(p, encoding="utf-8").read() for p in dateien())
    pruefen(not re.search(r"--([a-z0-9-]+):\s*var\(--\1\)", alles), "keine Variable verweist auf sich selbst (--x:var(--x) macht sie ungueltig)")
    tokens = set(re.findall(r"(--[a-z0-9-]+):", open(os.path.join(CLIENT, "plugins", "eden-ui", "eden-ui.css"), encoding="utf-8").read().split("}")[0]))
    plugins = [p for p in dateien() if not p.endswith(("eden-ui.css", "index.html"))]
    doppelt = {t for p in plugins for t in re.findall(r"(--[a-z0-9-]+):", open(p, encoding="utf-8").read()) if t in tokens}
    pruefen(not doppelt, "kein Plugin ueberschreibt gemeinsame Tokens: %s" % doppelt)
    fremd = set(re.findall(r"""uiIc\([^()]*?,\s*["']([a-z ]+)["']\)""", alles)) - {"klein", "imtext", "imtext leer"}
    pruefen(not fremd, "Icon-Groessen nur klein oder imtext (keine Klassen, die woanders schon etwas bedeuten): %s" % fremd)
    index = open(os.path.join(CLIENT, "index.html"), encoding="utf-8").read()
    pruefen("<symbol" not in index and 'href="#i-' not in index, "index.html hat keine eigenen Icon-Symbole mehr")
    pruefen("--perle:" not in index and "--akz:" not in index and not re.search(r"^\.(glas|knopf|name|zahl)\{", index, re.M), "Tokens und Grundbausteine stehen nur in eden-ui.css")
    moral = re.findall(r'"id": "([a-z]+)", "ab"', open(os.path.join(EDEN, "werkzeuge", "eden_rise", "modul_eden_rise.py"), encoding="utf-8").read())
    pruefen(moral and all("mood-" + m in ICONS for m in moral), "jede Stimmungsstufe hat ihr Gesicht")


if __name__ == "__main__":
    main()

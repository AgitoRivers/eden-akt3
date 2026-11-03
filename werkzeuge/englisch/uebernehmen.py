# -*- coding: utf-8 -*-
r"""Writes an approved English package back into the builder sources (25.10.2026).

Finds every old text as a string literal in the given source files (via the Python AST, so implicitly concatenated
literals spread over several lines count as one) and replaces that span with the new text, wrapped to the line width.
A literal is only replaced when every key that uses it maps to the same new text; everything else is reported and
done by hand.

    python werkzeuge\englisch\uebernehmen.py docs\abnahme\englisch_pilot_tag0_hafen.json  file.py [file.py ...] [--schreiben]
Without --schreiben it only reports (dry run).
"""
import ast, json, os, sys
from collections import defaultdict

BREITE = 120


def literal(text, col):
    """New text as one or more adjacent double-quoted literals, starting at column col."""
    platz = max(40, BREITE - col - 2)
    teile, rest = [], text
    while len(json.dumps(rest, ensure_ascii=False)) > platz:
        cut = rest.rfind(" ", 0, platz - 2)
        if cut <= 0:
            break
        teile.append(rest[:cut + 1])
        rest = rest[cut + 1:]
    teile.append(rest)
    return ("\n" + " " * col).join(json.dumps(t, ensure_ascii=False) for t in teile)


def zeichen(zeile, byte_offset):
    return len(zeile.encode("utf-8")[:byte_offset].decode("utf-8"))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    schreiben = "--schreiben" in sys.argv
    spec = json.load(open(args[0], encoding="utf-8"))
    alt_neu = defaultdict(set)
    keys_je_alt = defaultdict(list)
    for g in spec["gruppen"]:
        for it in g["items"]:
            if it["alt"] and it["alt"] != it["neu"]:
                alt_neu[it["alt"]].add(it["neu"])
                keys_je_alt[it["alt"]].append(it["key"])
    konflikt = {a: n for a, n in alt_neu.items() if len(n) > 1}
    gefunden = set()
    for pfad in args[1:]:
        src = open(pfad, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in src else "\n"
        zeilen = src.replace("\r\n", "\n").split("\n")
        offs = [0]
        for z in zeilen:
            offs.append(offs[-1] + len(z) + 1)
        text = "\n".join(zeilen)
        ersatz = []
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in alt_neu \
                    and node.value not in konflikt:
                ca = zeichen(zeilen[node.lineno - 1], node.col_offset)      # AST offsets are UTF-8 bytes
                a = offs[node.lineno - 1] + ca
                b = offs[node.end_lineno - 1] + zeichen(zeilen[node.end_lineno - 1], node.end_col_offset)
                ersatz.append((a, b, literal(next(iter(alt_neu[node.value])), ca)))
                gefunden.add(node.value)
        for a, b, neu in sorted(ersatz, reverse=True):
            text = text[:a] + neu + text[b:]
        print("%s: %d Stellen" % (os.path.basename(pfad), len(ersatz)))
        if schreiben and ersatz:
            ast.parse(text)                               # still valid Python?
            open(pfad, "w", encoding="utf-8", newline="").write(text.replace("\n", nl))
    offen = [(a, keys_je_alt[a]) for a in alt_neu if a not in gefunden]
    print("\nKonflikte (gleicher alter Text, verschiedene neue): %d" % len(konflikt))
    for a, n in konflikt.items():
        print("  %r -> %s  (%s)" % (a, sorted(n), ", ".join(keys_je_alt[a])))
    print("Nicht als Literal gefunden (von Hand): %d" % len(offen))
    for a, ks in offen:
        print("  %s: %r" % (", ".join(ks), a[:90]))


if __name__ == "__main__":
    main()

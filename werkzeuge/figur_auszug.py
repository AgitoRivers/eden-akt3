# -*- coding: utf-8 -*-
"""Figure excerpt for Brain Trust rounds: collects everything about one or more characters from all sources into
one compact Markdown file per character (read-only, runs locally, costs no Claude tokens).

    python werkzeuge\\figur_auszug.py alva casanova toto maxwell
    python werkzeuge\\figur_auszug.py --alle

Output: docs/brain_trust/auszuege/<id>.md
Case links from story.json go only into the last section VERDECKT (never quote in chat). VERDECKT sections of
dossiers are not read.
"""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(EDEN, "module", "eden_rise")
OUT = os.path.join(EDEN, "docs", "brain_trust", "auszuege")
WORLD = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds\Eden Yacht.json"
PS_PRESETS = r"X:\AI\PromptStudio\presets.json"
PS_SETS = r"X:\AI\PromptStudio\set_presets.json"
BASIS = os.path.join(EDEN, "werkzeuge", "eden_rise", "basis_eden_rise.py")

# id -> (names/aliases used in texts, card text file in karten_neu, Prompt Studio preset)
FIGURES = {
    "chiara": (["Chiara"], "chiara.txt", "Yacht_Chiara"),
    "sophia": (["Sophia"], "sophia.txt", "Yacht_Sophia"),
    "lea": (["Lea"], "lea.txt", "Yacht_Lea"),
    "rosi": (["Rosi", "Rosaria"], "rosi.txt", "Yacht_Rosi"),
    "siri": (["Siri"], "siri.txt", "Yacht_Siri"),
    "lola": (["Lola"], "lola.txt", "Yacht_Lola"),
    "jana": (["Jana"], "jana.txt", "Yacht_Jana"),
    "megan": (["Megan"], "megan.txt", "Yacht_Megan"),
    "holm": (["Holm", "Marit"], "holm.txt", "Yacht_Holm"),
    "alva": (["Alva", "Lulu"], None, "Yacht_Alva"),
    "casanova": (["Casanova"], None, "Yacht_Casanova"),
    "toto": (["Totò", "Toto"], None, "Yacht_Toto"),
    "maxwell": (["Maxwell", "Maximum"], "maximum.txt", "Yacht_Maximum"),
    "yamamoto": (["Yamamoto"], "yamamoto.txt", "Yacht_Yamamoto"),
    "petru": (["Petru"], None, "Yacht_Petru"),
    "elsa": (["Elsa"], None, "Yacht_Elsa"),
    "yasin": (["Yasin"], None, "Yacht_Yasin"),
}
PS_FIELDS = ["base_prompt", "sprite_prompt", "fashion_prompt", "loras", "ref_image", "st_set", "sv_sets"]


def load(path):
    try:
        return json.load(open(path, encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None


def cut(text, n):
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= n else text[:n - 1] + "…"


def matcher(names):
    return re.compile(r"(?<![A-Za-zÀ-ÿ])(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-zÀ-ÿ])")


def mentions(obj, fid, rx):
    raw = json.dumps(obj, ensure_ascii=False)
    return ('"%s"' % fid) in raw or bool(rx.search(raw))


def section_module(fid):
    mod = load(os.path.join(MOD, "modul.json")) or {}
    p = (mod.get("personen") or {}).get(fid)
    if not p:
        return ["_Kein Eintrag in modul.json (nicht in der Engine)._"]
    return ["```json", json.dumps(p, ensure_ascii=False, indent=1), "```"]


def section_card(card):
    if not card:
        return ["_Keine Karte in karten_neu._"]
    path = os.path.join(EDEN, "karten_neu", card)
    if not os.path.exists(path):
        return ["_Karte %s fehlt._" % card]
    text = open(path, encoding="utf-8").read()
    # English part only (German mirror would double the size)
    for marker in ("\n=== DE", "\n# DE", "\n--- DE", "\nDEUTSCH"):
        if marker in text:
            text = text.split(marker)[0]
    return ["```", text.strip(), "```"]


def section_world(rx):
    w = load(WORLD)
    if not w:
        return ["_Weltbuch nicht lesbar._"]
    out = []
    for nr, e in w["entries"].items():
        blob = " ".join(str(e.get(k, "")) for k in ("comment", "key", "content"))
        if rx.search(blob):
            off = " (aus)" if str(e.get("disable")).lower() == "true" else ""
            out.append("- **LB %s %s%s:** %s" % (nr, cut(e.get("comment", ""), 60), off, cut(e.get("content", ""), 500)))
    return out or ["_Keine Einträge._"]


def section_events(fid, rx):
    d = load(os.path.join(MOD, "ereignisse.json")) or {}
    out = ["| id | Art | Tage/Phase | Rolle | Titel – Lage |", "|---|---|---|---|---|"]
    for e in d.get("events", []):
        if not mentions(e, fid, rx):
            continue
        rolle = [k for k, v in e.get("personen", {}).items()
                 if v == fid or (isinstance(v, list) and (fid in v or any(isinstance(x, dict) and x.get("id") == fid
                                                                         for x in v)))]
        w = e.get("wann", {})
        out.append("| %s | %s | T%s %s | %s | %s – %s |" % (
            e["id"], e["art"], "–".join(map(str, w.get("tage", []))), "/".join(w.get("phasen", [])),
            ",".join(rolle) or "erwähnt", cut(e.get("titel", ""), 40), cut(e.get("lage", ""), 160).replace("|", "/")))
    return out if len(out) > 2 else ["_Keine Events._"]


def section_missions(fid, rx):
    d = load(os.path.join(MOD, "missionen.json")) or {}
    out = []
    for m in d.get("missionen", []):
        if m.get("von") == fid or mentions(m, fid, rx):
            out.append("- **%s** (von %s, T%s, %s SG %s): %s – %s" % (
                m["id"], m.get("von"), "–".join(map(str, m.get("tage", []))), m.get("attribut"), m.get("sg"),
                cut(m.get("titel", ""), 60), cut(m.get("text", ""), 200)))
    return out or ["_Keine Missionen._"]


def section_items(fid, rx):
    d = load(os.path.join(MOD, "gegenstaende.json")) or {}
    out = []
    for it in d.get("items", []):
        tags = []
        for k in ("quelle", "liebt", "hasst"):
            if fid in (it.get(k) or []):
                tags.append(k)
        if it.get("einzigartig") == fid:
            tags.append("unikat")
        if not tags and rx.search(json.dumps(it, ensure_ascii=False)):
            tags.append("erwähnt")
        if tags:
            out.append("- %s **%s** (%s, %s): %s" % ("/".join(tags), it.get("label"), it.get("id"), it.get("art"),
                                                     cut(it.get("text", ""), 120)))
    for key in ("haltung", "kochen", "essen"):
        block = d.get(key)
        if isinstance(block, dict) and fid in block:
            out.append("- %s: %s" % (key, cut(json.dumps(block[fid], ensure_ascii=False), 300)))
    return out or ["_Keine Gegenstände._"]


def section_ps(preset):
    p = (load(PS_PRESETS) or {}).get(preset)
    if not p:
        return ["_Kein Preset %s._" % preset]
    out = ["- **%s:** %s" % (k, cut(json.dumps(p.get(k), ensure_ascii=False), 400)) for k in PS_FIELDS if p.get(k)]
    sets = load(PS_SETS) or {}
    names = sorted(k for k in (sets if isinstance(sets, dict) else {}) if k.startswith(preset + "|"))
    if names:
        out.append("- **Kostüm-Presets:** " + ", ".join(n.split("|", 1)[1] for n in names))
    return out


def section_voice(fid):
    cfg = load(os.path.join(EDEN, "eden-config.json")) or {}
    v = ((cfg.get("stimmen") or {}).get("eden_rise") or {}).get(fid)
    return ["- Stimme (eden-config): %s" % (v or "—")]


def section_basis(fid, rx):
    if not os.path.exists(BASIS):
        return ["_basis_eden_rise.py fehlt._"]
    out = []
    for n, line in enumerate(open(BASIS, encoding="utf-8"), 1):
        if ('"%s"' % fid) in line or rx.search(line):
            out.append("- basis:%d `%s`" % (n, cut(line, 200).replace("`", "'")))
    return out[:60] or ["_Keine Zeilen._"]


def section_docs(fid, rx):
    out = []
    roots = [os.path.join(EDEN, "docs"), os.path.join(EDEN, "docs", "brain_trust")]
    for root in roots:
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name)
            if not name.endswith(".md") or not os.path.isfile(path):
                continue
            rel = os.path.relpath(path, EDEN)
            for n, line in enumerate(open(path, encoding="utf-8"), 1):
                if line.startswith("## VERDECKT"):
                    break                              # never read hidden case sections
                if rx.search(line):
                    out.append("- %s:%d %s" % (rel, n, cut(line, 220)))
    return out[:120] or ["_Keine Erwähnungen._"]


def section_cases(fid, rx):
    """Main-story case links (never quote in chat). Facts where the figure knows, is the source or a way runs over her."""
    story = load(os.path.join(MOD, "story.json"))
    if not story:
        return ["_story.json nicht lesbar._"]
    out = []
    for fall in story.get("faelle", []):
        rows = []
        if fall.get("verantwortlich") == fid:
            rows.append("  - **verantwortlich in diesem Fall**: %s" % cut(fall.get("kern", ""), 300))
        for f in fall.get("fakten", []):
            if f["id"][:2] in ("r_", "h_") and not f["id"].startswith("h_"):
                continue                               # shared frame facts appear in every case
            roles = []
            if f.get("quelle") == fid:
                roles.append("Quelle")
            if fid in f.get("wissende", []):
                roles.append("weiß")
            if f.get("person") == fid:
                roles.append("betrifft")
            if any(w.get("person") == fid for w in f.get("wege", [])):
                roles.append("Weg")
            if not roles and rx.search(f.get("inhalt", "")):
                roles.append("erwähnt")
            if roles:
                rows.append("  - %s [%s, %s%s]: %s" % (f["id"], "/".join(roles), f.get("zuverlaessigkeit"),
                                                      "" if f.get("wahr", True) else ", UNWAHR", cut(f.get("inhalt", ""), 220)))
        for t in fall.get("tipps", []):
            if t.get("wer") == fid:
                rows.append("  - Tratsch-Tipp %s (ab V%s): %s" % (t["id"], t.get("ab_vertrauen"), cut(t.get("text", ""), 160)))
        if (fall.get("nachtende") or {}).get("absender") == fid:
            rows.append("  - schickt die Nachricht kurz vor Morgen (Tag 3)")
        if rows:
            out.append("- **Fall %s**" % fall.get("nr"))
            out += rows
    for f in (story.get("zweite_wahrheit") or {}).get("fakten", []):
        if f.get("quelle") == fid or fid in f.get("wissende", []) or any(w.get("person") == fid for w in f.get("wege", [])):
            out.append("- Zweite Wahrheit %s: %s" % (f["id"], cut(f.get("inhalt", ""), 200)))
    return out or ["_Keine Fall-Bezüge._"]


def excerpt(fid):
    names, card, preset = FIGURES[fid]
    rx = matcher(names)
    parts = [("Engine (modul.json)", section_module(fid)), ("Karte (EN)", section_card(card)),
             ("Weltbuch", section_world(rx)), ("Events", section_events(fid, rx)),
             ("Missionen", section_missions(fid, rx)), ("Gegenstände / Essen", section_items(fid, rx)),
             ("Prompt Studio", section_ps(preset)), ("Stimme", section_voice(fid)),
             ("Builder basis_eden_rise.py", section_basis(fid, rx)), ("Docs (ohne VERDECKT)", section_docs(fid, rx)),
             ("VERDECKT – Fall-Bezüge (nie im Chat zitieren)", section_cases(fid, rx))]
    lines = ["# Auszug: %s" % " / ".join(names),
             "",
             "Automatisch erzeugt von werkzeuge/figur_auszug.py. Fall-Bezüge stehen nur im letzten Abschnitt VERDECKT "
             "(Duc liest diese Dateien nicht; im Chat nie Inhalte daraus nennen).", ""]
    for title, body in parts:
        lines += ["## " + title, ""] + body + [""]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "%s.md" % fid)
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return path, len(lines), os.path.getsize(path)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ids = list(FIGURES) if "--alle" in sys.argv else [a for a in sys.argv[1:] if not a.startswith("--")]
    unknown = [i for i in ids if i not in FIGURES]
    if not ids or unknown:
        sys.exit("Figuren: %s%s" % (", ".join(FIGURES), ("  (unbekannt: %s)" % ", ".join(unknown)) if unknown else ""))
    for fid in ids:
        path, n, size = excerpt(fid)
        print("%-10s %4d Zeilen  %5.1f KB  %s" % (fid, n, size / 1024, os.path.relpath(path, EDEN)))


if __name__ == "__main__":
    main()

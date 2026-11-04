# -*- coding: utf-8 -*-
"""Textpruefung Akt 1 und 2 (Cloud-Sitzung 04.11.2026): sucht Rueckbezuege ohne Erinnerung und seltene Woerter/Redewendungen.

    pip install wordfreq
    python tests/audit_text.py > kandidaten.json

Nur ein Werkzeug fuer den Bericht docs/uebergabe/audit_text.md, aendert nichts. Ausgelassen (Spoiler und Sperre):
Kennungen vh., fv_, rt_t_, Handy-Ketten (hy_), Selfies (sf_, sfn_), module/eden_rise/story.json, handy.json, rast_anrufe.json.
Braucht das Paket wordfreq (Zipf-Haeufigkeit, 3.0 = etwa einmal je Million Woerter)."""
import json, os, re, sys

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(EDEN, "module", "eden_rise")
AUSLASSEN_ID = ("vh.", "fv_", "rt_t_", "hy_", "sf_", "sfn_")
AUSLASSEN_DATEI = {"story.json", "handy.json", "rast_anrufe.json", "stimme_tags.json", "audio_index.json", "sfx.json",
                   "gesichter.json", "wuerfel_anzeige.json"}

RUECK = re.compile(r"\b(that night|that day|that evening|that morning|the other night|the other day|last night|last time|"
                   r"the bet|the relay|the race|the deal|the promise|the thing with|you promised|like before|like last time|"
                   r"remember (?:when|that|the)|back then|that time|the storm|the hearing|the dive|the wreck|the list|"
                   r"the note|the page|the photo|the board|the bandage|the key|again\b|as I said|as you said|you said)", re.I)
IDIOM = ["piece of cake", "break a leg", "under the weather", "call it a day", "beat around the bush", "spill the beans",
         "in the same boat", "hit the sack", "once in a blue moon", "cut corners", "bite the bullet", "ball is in your court",
         "arm and a leg", "pull your leg", "pulling your leg", "off the hook", "over the moon", "by the book", "on thin ice",
         "cold feet", "break the ice", "hang in there", "keep tabs", "last straw", "up to scratch", "sit tight", "touch base",
         "play it by ear", "get the hang", "rain check", "no-brainer", "shoot the breeze", "drop the ball", "toe the line",
         "make do", "on the fence", "call the shots", "cut to the chase", "the whole nine yards", "go the extra mile",
         "a dime a dozen", "hit the nail", "let the cat out", "kill two birds", "bark up the wrong", "under wraps",
         "in hot water", "out of the blue", "rings a bell", "on the same page", "small potatoes", "the elephant in the room",
         "throw in the towel", "jump the gun", "bent out of shape", "tip of the iceberg", "red herring", "steal the show",
         "full of beans", "fair and square", "cheap shot", "low-hanging", "for the record", "on the house", "not my cup of tea",
         "bottom line", "keep your hair on", "at the end of the day", "draw the line", "rule of thumb", "take a rain check",
         "a tall order", "flat out", "no dice", "down to earth", "neck of the woods", "sleep on it", "pull through",
         "the real deal", "go figure", "beats me", "cut it out", "knock it off", "hold your horses", "mind you",
         "spot on", "fair enough", "bob's your uncle", "chuffed", "gobsmacked", "knackered", "cheeky"]


def texte():
    for fn in sorted(os.listdir(MOD)):
        if not fn.endswith(".json") or fn in AUSLASSEN_DATEI:
            continue
        try:
            d = json.load(open(os.path.join(MOD, fn), encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        if fn == "ereignisse.json":
            for e in d["events"]:
                if e["id"].startswith(AUSLASSEN_ID):
                    continue
                if e.get("lage"):
                    yield fn, e["id"], "lage", e["lage"]
                for i, z in enumerate(e.get("zeilen") or []):
                    yield fn, e["id"], "z%d:%s" % (i, z.get("person") or z.get("wer") or ""), z.get("text") or ""
                for i, o in enumerate(e.get("optionen") or []):
                    yield fn, e["id"], "o%d" % i, o.get("text") or ""
                    for j, f in enumerate(o.get("folgen") or []):
                        if isinstance(f, dict) and isinstance(f.get("text"), str):
                            yield fn, e["id"], "o%d.f%d" % (i, j), f["text"]
                    if isinstance(o.get("zeile"), dict):
                        yield fn, e["id"], "o%d.zeile:%s" % (i, o["zeile"].get("person", "")), o["zeile"].get("text", "")
            continue
        yield from _rekursiv(fn, d, fn)


def _rekursiv(fn, d, pfad):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(k, str) and k.startswith(AUSLASSEN_ID):
                continue
            yield from _rekursiv(fn, v, "%s.%s" % (pfad, k))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from _rekursiv(fn, v, "%s[%d]" % (pfad, i))
    elif isinstance(d, str) and " " in d and re.search(r"[a-z]{3,} [a-z]{2,}", d) and not re.search(r"[äöüß]", d):
        if any(x in pfad for x in AUSLASSEN_ID):
            return
        yield fn, pfad.split(".")[1] if "." in pfad else pfad, pfad, d


def main():
    from wordfreq import zipf_frequency
    aus = {"rueck": [], "idiom": [], "selten": []}
    for fn, eid, feld, t in texte():
        t2 = re.sub(r"\[[a-z ]+\]", "", t)
        for m in RUECK.finditer(t2):
            aus["rueck"].append([fn, eid, feld, m.group(0), t2])
        low = t2.lower()
        for i in IDIOM:
            if i in low:
                aus["idiom"].append([fn, eid, feld, i, t2])
        for w in set(re.findall(r"\b[a-z][a-z'-]{3,}\b", t2)):
            w2 = w.strip("'-")
            if w2 and zipf_frequency(w2, "en") < 2.6:
                aus["selten"].append([fn, eid, feld, w2, round(zipf_frequency(w2, "en"), 2), t2])
    json.dump(aus, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()

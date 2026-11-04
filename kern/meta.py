# -*- coding: utf-8 -*-
"""Was ueber Spielstaende hinweg gilt (Akt 3, 04.11.2026): gesehene Enden, fuer das geheime Ende ★ (enden.md: "Ende 1 schon
gesehen"). Datei spielstaende/_meta.json, nicht im Git. Beim Laden eines Spielstands kommen die Eintraege als Flags
meta_ende_<id> dazu (eden.aktiv), nach jedem Ende wird es hier vermerkt (eden.weiter, Tagesende)."""
import json, os

DATEI = "_meta.json"


def lesen(ordner):
    try:
        return json.load(open(os.path.join(ordner, DATEI), encoding="utf-8"))
    except (OSError, ValueError):
        return {"enden": []}


def ende_merken(ordner, eid):
    m = lesen(ordner)
    if eid and eid not in m.setdefault("enden", []):
        m["enden"].append(eid)
        os.makedirs(ordner, exist_ok=True)
        json.dump(m, open(os.path.join(ordner, DATEI), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return m


def flags_setzen(z, ordner):
    """meta_ende_<id> fuer jedes gesehene Ende in den Spielstand. -> True, wenn etwas dazukam."""
    neu = ["meta_ende_" + e for e in lesen(ordner).get("enden", []) if "meta_ende_" + e not in z.setdefault("flags", [])]
    z["flags"] += neu
    return bool(neu)

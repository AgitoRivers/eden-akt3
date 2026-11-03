# -*- coding: utf-8 -*-
"""Request-local presentation notices. No changes to rolls, rules, saves or hidden checks."""
import contextlib
import contextvars
import copy
import json
import os
import secrets

_AKTUELL = contextvars.ContextVar("eden_wuerfel_anzeige", default=None)
AKTIONEN = frozenset(("zug", "waehlen", "geste", "job", "event_wahl", "kochen", "verabredung_ort", "kampf_zug",
                      "kampf_parade"))


def einstellungen(moddir):
    """Optional sidecar, intentionally not a generated story/module file."""
    try:
        with open(os.path.join(moddir, "wuerfel_anzeige.json"), encoding="utf-8") as stream:
            daten = json.load(stream)
        return daten if isinstance(daten, dict) else {}
    except (OSError, ValueError):
        return {}


def _modus(aktion, daten, z, cfg):
    gross = cfg.get("gross") or {}
    if aktion == "event_wahl":
        return "gross" if (z.get("event") or {}).get("id") in gross.get("ereignisse", []) else "kompakt"
    if aktion == "job":
        return "gross" if daten.get("id") in gross.get("missionen", []) else "kompakt"
    sz = (z.get("szene") or {}).get("def") or {}
    return "gross" if sz.get("id") in gross.get("szenen", []) else "kompakt"


@contextlib.contextmanager
def sammeln(aktion, daten, z, moddir):
    """Collect only during a successful player's POST; GETs never contain replay notices."""
    z = z or {}
    cfg = einstellungen(moddir)
    ein = aktion in AKTIONEN and cfg.get("aktiv", True) is not False
    paket = {"version": 1, "run_id": z.get("id", ""), "rolls": [],
             "policy": {"kritisch_gross": cfg.get("kritisch_gross", True) is not False,
                        "effekte": cfg.get("effekte", True) is not False}}
    sammler = {"paket": paket, "modus": _modus(aktion, daten, z, cfg),
               "titel": ((z.get("szene") or {}).get("def") or {}).get("titel") or "Würfelprobe",
               "kennung": secrets.token_hex(12)} if ein else None
    token = _AKTUELL.set(sammler)
    try:
        yield paket
    finally:
        _AKTUELL.reset(token)


def merken(probe):
    sammler = _AKTUELL.get()
    if sammler is None:
        return
    paket = sammler["paket"]
    paket["rolls"].append({"id": "%s:%d" % (sammler["kennung"], len(paket["rolls"])),
                            "probe": copy.deepcopy(probe), "modus": sammler["modus"],
                            "titel": sammler["titel"]})

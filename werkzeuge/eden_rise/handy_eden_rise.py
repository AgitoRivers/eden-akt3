# -*- coding: utf-8 -*-
r"""Phone data for module eden_rise (24.10.2026): the tone table of the phone chat and its guard rails.
Rules live in kern\handy.py, numbers here. The builder writes the engine defaults (kern.handy.DEFAULTS) plus OVERRIDES
below into module\eden_rise\handy.json. Never edit the json by hand: change OVERRIDES here and run the builder.

  tones[id]       axis (vertrauen|begehren|null), points, impression (for her reply, English), label (UI, German)
  chip_tones      tones of the three answer chips, in order
  flirt_min_trust below this trust stage a flirt is "too forward" (costs backfire_points trust)
  max_replies     answers per woman and day
  min_progress    points of trust+desire gained since her last text before she texts again (driver)
  callback_days   the next scene start may pick up Duc's text lines of this many days

    python handy_eden_rise.py   -> module\eden_rise\handy.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, EDEN)
from kern import handy  # noqa: E402

# Module specifics on top of the engine defaults (none yet - the defaults are the Eden Rise numbers).
OVERRIDES = {}


def build():
    data = json.loads(json.dumps(handy.DEFAULTS))
    for k, v in OVERRIDES.items():
        if isinstance(v, dict) and isinstance(data.get(k), dict):
            data[k].update(v)
        else:
            data[k] = v
    return data


if __name__ == "__main__":
    out = os.path.join(EDEN, "module", "eden_rise", "handy.json")
    with open(out + ".tmp", "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    os.replace(out + ".tmp", out)
    print("written:", out, "| tones:", ", ".join(build()["tones"]))

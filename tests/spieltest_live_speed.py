"""Conservative, auditable reuse of exactly identical deterministic structured checks."""
import hashlib
import json


def check_key(system, user, args, kwargs, origin, model="Giftige-Blume-31B-v2-Q4_K_M"):
    if origin != "engine":
        return None
    grammar = kwargs.get("grammar", args[2] if len(args) > 2 else None)
    sampler = kwargs.get("sampler", args[0] if args else None)
    if not grammar:
        return None
    # An omitted sampler is explicitly temperature=0 in kern.llm.chat. Unknown sampler
    # settings and stochastic actor outputs must always reach the actual model.
    if sampler is not None and (not isinstance(sampler, dict) or sampler.get("temperature") != 0):
        return None
    try:
        payload = json.dumps(dict(model=model, system=system, user=user, args=args, kwargs=kwargs), sort_keys=True)
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_check(path, key):
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        # Only valid structured answers; malformed/empty responses are never reused.
        if not isinstance(json.loads(d["text"]), (dict, list)):
            return None
        return d["text"] if d.get("key") == key else None
    except (OSError, ValueError, KeyError, TypeError):
        return None

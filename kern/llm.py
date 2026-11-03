# -*- coding: utf-8 -*-
"""Anbindung an das lokale Spielmodell (KoboldCpp, OpenAI-kompatibel) - eine Rolle pro Aufruf:
Schauspielerin, Regie, Richter, Probe, Gedaechtnis. Alle laufen auf demselben Modell (Giftige Blume)."""
import json, re, time, urllib.request

URL = "http://127.0.0.1:5010"
DENKEN = re.compile(r"(?s)<\|channel>thought.*?<channel\|>|<think>.*?</think>")
B = 'b ::= "true" | "false"\nws ::= [ \\t\\n]*'
STOP = ["\nDuc:", "\nDuc said", "<|im_end|>", "<end_of_turn>"]


def bereit():
    try:
        urllib.request.urlopen(URL + "/api/v1/model", timeout=2).read()
        return True
    except Exception:
        return False


def chat(system, user, sampler=None, max_tokens=300, grammar=None):
    body = dict(sampler or {"temperature": 0.0}, model="kobold", max_tokens=max_tokens, stop=STOP,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    if grammar:
        body["grammar"] = grammar
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        res = json.loads(r.read())
    return DENKEN.sub("", res["choices"][0]["message"]["content"] or "").strip(), time.time() - t0


def json_chat(system, user, grammar, max_tokens=120, sampler=None):
    roh, sek = chat(system, user, sampler=sampler, max_tokens=max_tokens, grammar=grammar)
    try:
        return json.loads(roh), sek
    except Exception:
        return None, sek


def wahl_grammatik(feld, optionen):
    """{"feld": "<eine der Optionen>"}"""
    return 'root ::= "{" ws "\\"%s\\":" ws (%s) ws "}"\n%s' % (
        feld, " | ".join('"\\"%s\\""' % o for o in optionen), B)


def bool_grammatik(schluessel):
    return ('root ::= "{" ws ' + ' "," ws '.join('"\\"%s\\":" ws b' % k for k in schluessel) + ' ws "}"\n' + B)

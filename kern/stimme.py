# -*- coding: utf-8 -*-
"""Sprachausgabe (ElevenLabs) - nur die gesprochenen Worte in "Anfuehrungszeichen", nie Gedanken oder Erzaehltext.
Schluessel kommt aus dem Voice Studio (voice-studio.json), Stimmen-IDs aus dem Modul (personen.<id>.stimme_id).
Jede Zeile wird einmal erzeugt und im Spielstand-Ordner zwischengespeichert (kostet Zeichen nur beim ersten Mal)."""
import hashlib, json, os, re, urllib.request

REDE = re.compile(r'"([^"]{2,})"')
API = "https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128"


# Handy-Chat mit Emojis (Duc 27.10.2026): die Stimme liest sie nie - weg vor jeder Vertonung (Hash bleibt fuer Zeilen ohne Emoji gleich)
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u20E3]+")


def ohne_emoji(text):
    return re.sub(r"[ \t]{2,}", " ", EMOJI.sub("", text or "")).strip()


def rede(text):
    teile = [t.strip() for t in REDE.findall(text or "") if re.search(r"[A-Za-z]", t)]
    return " ... ".join(teile)


def vorlesen(text):
    """Ganzer gezeigter Text zum Vorlesen (16.10.2026, Duc: alles vertonen, nicht nur die Rede): Markup weg,
    Absaetze werden kurze Pausen. Gedanken stehen nur drin, wenn die Empathie-Probe sie sichtbar gemacht hat."""
    t = re.sub(r'[*"“”„_~]', "", ohne_emoji(text))
    t = re.sub(r"\s*\n+\s*", " ... ", t)
    t = re.sub(r"\s{2,}", " ", t).strip().lstrip(". ")
    return t if re.search(r"[A-Za-z]", t) else ""


# ------------------------------------------------------------------ Chatterbox (lokal, Standard seit 13.10.2026)
# Dieselben Stimmen wie in SillyTavern: Katalog X:\AI\Chatterbox\stimmen.json, Dateien in Chatterbox\voices.
# Englisch -> Datei "dateien.ENG". Chatterbox laeuft auf Port 8004 (OpenAI-kompatibel /v1/audio/speech).
KATALOG = r"X:\AI\Chatterbox\stimmen.json"
CHATTERBOX = "http://127.0.0.1:8004"
PROBE = "Hi. This is how I sound on board the Eden Rise. Is that alright with you?"


# Turbo-Tags (Duc 26.10.2026): jede vertonte Zeile hat mindestens einen Tag ([chuckle], [sigh] ...). Die gesprochene Fassung steht in
# module\eden_rise\stimme_tags.json (wer, text = Klartext wie im Spiel, gesprochen = mit Tags); der Spieltext bleibt ohne Tags.
TAGS_DATEI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "module", "eden_rise", "stimme_tags.json")
# stimme_fest.json (01.11.2026): nach der Hoerpruefung neu aufgenommene Zeilen. Geht vor, weil die Builder stimme_tags.json bei jedem Bau neu schreiben
# und sonst wieder die alte, fehlerhafte Aufnahme spielt.
FEST_DATEI = os.path.join(os.path.dirname(TAGS_DATEI), "stimme_fest.json")
TAG_MUSTER = re.compile(r"\s*\[(?:laugh|chuckle|sigh|gasp|cough|clear throat|sniff|groan|shush)\]")
_tags = {"stand": None, "karte": {}}


def getaggt(text):
    """Gesprochene Fassung einer festen Zeile (mit Tags); ohne Eintrag bleibt der Text, wie er ist."""
    try:
        stand = os.path.getmtime(TAGS_DATEI)
    except OSError:
        return text
    if _tags["stand"] != stand:
        try:
            d = json.load(open(TAGS_DATEI, encoding="utf-8"))
            _tags["karte"] = {z["text"]: z["gesprochen"] for z in d.get("zeilen", [])}
            if os.path.exists(FEST_DATEI):
                _tags["karte"].update(json.load(open(FEST_DATEI, encoding="utf-8"))["zeilen"])
        except (OSError, ValueError):
            _tags["karte"] = {}
        _tags["stand"] = stand
    return _tags["karte"].get(text, text)


def ohne_tags(text):
    """Anzeigetext: Turbo-Tags entfernen (sie gehoeren nur in die Stimme)."""
    return TAG_MUSTER.sub("", text or "").strip()


def katalog():
    """Aktive Katalogstimmen mit englischer Datei (voices) oder Referenzdatei (reference_audio, z. B. Cora, Dae,
    Young Adventurer), alphabetisch - dieselbe Auswahl wie in SillyTavern. Chatterbox sucht in beiden Ordnern."""
    try:
        d = json.load(open(KATALOG, encoding="utf-8"))
    except Exception:
        return []
    aus = [s for s in d.get("stimmen", []) if s.get("status") == "aktiv" and datei(s)]
    return sorted(aus, key=lambda s: s["name"].lower())


def datei(s):
    d = s.get("dateien") or {}
    return d.get("ENG") or d.get("REF")


def chatterbox_bereit():
    try:
        urllib.request.urlopen(CHATTERBOX + "/api/model-info", timeout=2).read()
        return True
    except Exception:
        return False


# Fremdwoerter, die Chatterbox auf Englisch falsch liest: nur die Stimme bekommt die Lautschrift, im Spiel steht das echte Wort
# (Bibis deutsche Kosenamen, Hoerprobe docs/abnahme/bibi_kosenamen_2, Duc 02.11.2026)
AUSSPRACHE = {"Hase": "Haaseh", "Bärchen": "Bear-shen"}


def aussprechen(text):
    for wort, laut in AUSSPRACHE.items():
        text = re.sub(r"\b%s\b" % re.escape(wort), laut, text)
    return text


def chatterbox(name, text, ordner, ganz=False):
    """wav fuer die gesprochenen Worte (ganz=True: ganzer Text, fuer die Probe). None ohne Stimme/Rede."""
    s = next((x for x in katalog() if x["name"] == name), None)
    gesagt = aussprechen(ohne_emoji(getaggt(text) if ganz else rede(text)))
    if not s or not gesagt:
        return None
    wav = datei(s)
    os.makedirs(ordner, exist_ok=True)
    pfad = os.path.join(ordner, hashlib.md5(("cb|" + wav + "|" + gesagt).encode()).hexdigest() + ".wav")
    if os.path.exists(pfad):
        return pfad
    body = {"model": "chatterbox", "input": gesagt, "voice": wav, "response_format": "wav", "language": "en"}
    req = urllib.request.Request(CHATTERBOX + "/v1/audio/speech", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        roh = r.read()
    with open(pfad + ".tmp", "wb") as fh:
        fh.write(roh)
    os.replace(pfad + ".tmp", pfad)
    return pfad


# ------------------------------------------------------------------ ElevenLabs (alt, bleibt als Reserve)
def erzeugen(cfg, stimme_id, text, ordner):
    gesagt = ohne_emoji(rede(text))
    if not gesagt or not stimme_id:
        return None
    os.makedirs(ordner, exist_ok=True)
    modell = cfg.get("stimme_modell", "eleven_flash_v2_5")
    pfad = os.path.join(ordner, hashlib.md5((stimme_id + modell + gesagt).encode()).hexdigest() + ".mp3")
    if os.path.exists(pfad):
        return pfad
    key = json.load(open(cfg["elevenlabs_config"], encoding="utf-8"))["api_key"].strip()
    body = {"text": gesagt, "model_id": modell, "language_code": "en",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True}}
    req = urllib.request.Request(API % stimme_id, data=json.dumps(body).encode(),
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        roh = r.read()
    with open(pfad + ".tmp", "wb") as fh:
        fh.write(roh)
    os.replace(pfad + ".tmp", pfad)
    return pfad

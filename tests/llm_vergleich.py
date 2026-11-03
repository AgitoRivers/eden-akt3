# -*- coding: utf-8 -*-
"""Modellvergleich fuer die freien Szenen (Duc 02.11.2026): Sind die Macken Eigenheiten von Giftige Blume oder allgemein?
Versteht ein Modell die geplante Tipp-Mechanik? Prompts kommen aus kern/szene.py und kern/figurenrahmen.py, feste Seeds, ohne Spiel.
Startet KoboldCpp selbst auf einem eigenen Port und beendet nur diesen Prozess. Ergebnis je Modell als JSON, ein Abbruch kann weiterlaufen.

  python tests\\llm_vergleich.py --trocken               Prompts ohne Modell pruefen
  python tests\\llm_vergleich.py --modelle blume,pe      laufen lassen
"""
import argparse, json, os, random, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(HERE)
sys.path.insert(0, EDEN)
os.environ.setdefault("PYTHONUTF8", "1")
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
from kern import figurenrahmen as R, llm, szene, zustand  # noqa: E402

KOBOLD = r"X:\AI\Kobold"
EXE = os.path.join(KOBOLD, "koboldcpp-1.117.1.exe")
PORT = 5021
MODELLE = {"blume": "Giftige-Blume-31B-v2-Q4_K_M.gguf", "meromero": "G4-MeroMero-26B-A4B-Q5_K_M.gguf",
           "pe": "Dans-PersonalityEngine-V1.3.0-24b.Q6_K.gguf", "magmell12": "MN-12B-Mag-Mell-R1.Q8_0.gguf",
           "magmell21": "Mag-Mell-R1-21B.Q8_0.gguf", "dolphin": "Dolphin-Mistral-24B-Venice-Q5_K_M.gguf",
           "gemstrike": "GemStrike-31B-Q4_K_M.gguf", "meromero2": "G4-MeroMero-v2-31B-Q4_K_M.gguf",
           "cydonia": "Cydonia-24B-v4zg-Q6_K.gguf", "magnum": "MS3.2-24B-Magnum-Diamond-Q6_K.gguf"}
SEEDS = (11, 22, 33)
FIGUREN = ("rosi", "chiara", "bibi", "sirene", "megan", "alva")
SZENARIEN = ["kaltstart", "anschluss", "nein", "grenzen", "erfindung"]
ORT = {"rosi": "tender_garage", "chiara": "crew_mess", "bibi": "aft_deck", "sirene": "swim_platform", "megan": "duc_cabin", "alva": "aft_deck"}
ABSAGE = '"No." She moves back, out of his reach. "Not that. Not now."'
ABSAGE_ANRUF = '"No." She looks at him through the screen and does not smile. "Not that. Not now."'
ZWEITE_ABSAGE = '"I said no, {anrede}. I meant it."'          # nur falls "absage.nachhaken" fehlt
NEIN_VORGABE = "[Just now] Duc tried something and she said no. She said no and does not come back to it. She stays in the scene, she does not soften, and she does not send him away."

# Erkennung: (Text, tut er es wirklich?, Art). Entwurf der Frage, die Mechanik E-116 ist noch nicht gebaut.
FAELLE = [
    ("I kiss her", True, "kiss"), ("I kiss you.", True, "kiss"), ("*leans in and kisses her*", True, "kiss"), ("*kisses you*", True, "kiss"),
    ("He pulls her close and kisses her.", True, "kiss"), ("*cups her face and kisses her deeply*", True, "kiss"),
    ("I lean over and kiss you on the cheek.", True, "kiss"), ("Enough talking. I kiss you.", True, "kiss"), ("i kis you", True, "kiss"),
    ("\"You talk too much.\" *I pull you in and press my lips to yours*", True, "kiss"), ("I take your hand and kiss it.", True, "kiss"),
    ("I'd never kiss you", False, "kiss"), ("did Lola kiss you?", False, "kiss"), ("Can I kiss you?", False, "kiss"), ("I want to kiss you.", False, "kiss"),
    ("I almost kissed you last night.", False, "kiss"), ("Don't kiss me.", False, "kiss"), ("I kissed you yesterday and you said nothing.", False, "kiss"),
    ("Lola kissed me at the party.", False, "kiss"), ("Kissing is overrated.", False, "kiss"), ("If I kissed you now, what would you do?", False, "kiss"),
    ("You should kiss Yasin.", False, "kiss"), ("I'm not going to kiss you.", False, "kiss"), ("*thinks about kissing her, but stays where he is*", False, "kiss"),
    ("He doesn't kiss her.", False, "kiss"), ("Kiss my ass, Rosi.", False, "kiss"), ("I dreamed that I kissed you.", False, "kiss"),
    ("*touches her arm*", True, "touch"), ("I put my hand on your shoulder.", True, "touch"), ("I grab your hand.", True, "touch"),
    ("I'd never touch you without asking.", False, "touch"), ("Don't touch my tools, you said.", False, "touch"), ("Who touched the radio?", False, "touch"),
    ("*hugs her*", True, "hug"), ("I pull you into a hug.", True, "hug"), ("Do you want a hug?", False, "hug"), ("Chiara hugged me this morning.", False, "hug"),
    ("I take off her shirt.", True, "undress"), ("*starts to unbutton her blouse*", True, "undress"), ("Lola took off her shirt at the party.", False, "undress"), ("Should I take off my shirt?", False, "undress"),
    # Runde 3 (Interaction Mechanic): Hand, Umarmen, Ausziehen, Beruehren, "somewhere private"
    ("*takes her hand*", True, "hand"), ("I hold your hand.", True, "hand"), ("Can I hold your hand?", False, "hand"), ("I held Lola's hand once.", False, "hand"),
    ("*wraps his arms around her*", True, "hug"), ("I'd hug you, but you'd bite me.", False, "hug"),
    ("*pulls her top over her head*", True, "undress"), ("*slides the strap off her shoulder*", True, "undress"), ("Take off your jacket, it's hot in here.", False, "undress"),
    ("*brushes a strand of hair from her face*", True, "touch"), ("*runs his fingers along her thigh*", True, "touch"), ("Your hair looks soft.", False, "touch"),
    ("Let's go somewhere private.", True, "privat"), ("*takes her hand and leads her to his cabin*", True, "privat"), ("Come with me. Somewhere quieter, just us.", True, "privat"),
    ("Lola and Yasin went somewhere private.", False, "privat"), ("I don't want to go anywhere private with you.", False, "privat"), ("Is there anywhere private on this boat?", False, "privat"),
]
HANDLUNG = {"kiss": "kiss her", "touch": "touch her", "hug": "hug her", "undress": "undress her", "hand": "take or hold her hand",
            "privat": "invite or lead her to go somewhere private with him"}
PRUEF_SYS = "You are the referee of a story game. You decide whether the player's character really does a physical action right now."
PRUEF_USER = ("Scene: Duc is alone with Rosi in the tender garage.\nRosi's last line: \"That's my father's workshop in Catania. Did your father teach you anything?\"\n"
              "Duc writes: %s\n\nDoes Duc himself really %s now, in this message? Answer false if he only talks about it, asks for it, refuses it, "
              "imagines it, jokes about it, or speaks about other people or another time.\nAnswer as JSON: {\"does_it\": true} or {\"does_it\": false}.")

DREHBUCH = {
    "anschluss": lambda pid: [None, "Go on."],
    "nein": lambda pid: ["Okay. Sorry.", "So, what is everybody doing tomorrow?", "Come on, you liked it. Admit it."],
    "grenzen": lambda pid: (["Give me your hand.", "Bring me a coffee, will you?"] if pid == "megan"
                            else ["Can I kiss you?", "Let's walk down to the beach later, just us."]),
    "erfindung": lambda pid: ["What do you remember about the first time we talked?", "Tell me about something we did together that you liked."],
    # Runde 3: None = feste Zeile statt Modell; "CHIP" = erste Antwort-Chip des neuen Themas
    "nein_echt": lambda pid: ["Okay. Sorry.", "So, what is everybody doing tomorrow?", "Come on, you liked it. Admit it."],
    "nein_fest": lambda pid: ["Okay. Sorry.", "So, what is everybody doing tomorrow?", ("Come on, you liked it. Admit it.", "ZWEITE"), "Alright. What now?"],
    "nein_thema": lambda pid: [("Okay. Sorry.", "THEMA"), "CHIP", ("Come on, you liked it. Admit it.", "ZWEITE"), "Alright. What now?"],
}
NEIN_ARTEN = ("nein", "nein_echt", "nein_fest", "nein_thema")


LOG = []                            # alle Modellaufrufe des laufenden Abschnitts
ZAEHLER = [0, 0]                    # Seed, laufende Nummer


def chat(system, user, sampler=None, max_tokens=300, grammar=None):
    """Wie llm.chat, dazu fester Seed und Messwerte."""
    ZAEHLER[1] += 1
    body = dict(sampler or {"temperature": 0.0}, model="kobold", max_tokens=max_tokens, stop=llm.STOP, seed=ZAEHLER[0] * 1000 + ZAEHLER[1],
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    if grammar:
        body["grammar"] = grammar
    req = urllib.request.Request(llm.URL + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        res = json.loads(r.read())
    sek = time.time() - t0
    wahl, nutz = res["choices"][0], res.get("usage") or {}
    roh = wahl["message"]["content"] or ""
    LOG.append({"rolle": "pruefer" if grammar else "figur", "sek": round(sek, 2), "grund": wahl.get("finish_reason"), "ein": nutz.get("prompt_tokens"),
                "aus": nutz.get("completion_tokens"), "denken": bool(llm.DENKEN.search(roh)), "roh": roh if not grammar else None})
    return llm.DENKEN.sub("", roh).strip(), sek


def stub(system, user, sampler=None, max_tokens=300, grammar=None):
    ZAEHLER[1] += 1
    LOG.append({"rolle": "pruefer" if grammar else "figur", "sek": 0, "grund": "stop", "ein": len(system) // 4, "aus": 1, "denken": False, "roh": "x", "system": system, "user": user})
    if grammar:
        return '{"contradicts_scene":false}', 0
    return '"Stub reply."', 0


def spiel(pid, modul, seed, thema_nr):
    random.seed(seed)
    z = zustand.neu(modul, "entspannt")
    zustand.persona_setzen(z, modul, modul["personen_wahl"] if modul.get("personen_wahl") else modul["personas"][0])
    z["tag"], z["phase"], z["status"], z["heute"] = 9, "abend", "wahl", []
    z["werte"]["vertrauen." + pid] = 3
    if pid not in ("megan", "sirene", "bibi", "jana"):
        z["werte"]["begehren." + pid] = 2
    z.setdefault("flags", [])
    for f in ("mochis_offen", "%s_kennengelernt" % pid):
        if f not in z["flags"]:
            z["flags"].append(f)
    st = R.stand(z, pid)
    frei = [t for t in R.figur(modul, pid).get("themen", []) if R.bedingung(z, pid, t.get("wenn"))]
    st["gesehen"] = [t["id"] for t in frei[:thema_nr]]
    return z


def szene_def(pid, modul, frei=True):
    p = modul["personen"][pid]
    n = p.get("kurz") or p["name"].split()[0]
    s = {"id": ("frei_%s_t9_abend" if frei else "kalt_%s_t9_abend") % pid, "titel": "Time with %s" % n, "ort": ORT[pid], "anwesend": [pid], "zeit": "",
         "ausgangslage": "%s and Duc have a quiet moment in the evening." % n, "frage": "What does Duc do with this time?",
         "figuren": {pid: {"will": "Spend some time with Duc in her own way."}}, "ausgaenge": [], "max_zuege": 8, "storylet": None, "improvisiert": True, "frei": True}
    if pid == "megan":
        s.update(anruf=True, anruf_wo="her office in Monaco", ausgangslage="Duc video-calls Megan from his cabin. She picks up; she is at her office in Monaco. They can only see and hear each other on the phone.")
    return s


def zug_spielen(z, modul, sz, pid, duc, extra=""):
    sz["log"].append({"art": "duc", "text": duc})
    sz["zug"] += 1
    n = len(LOG)
    text, verworfen, gefuehl, ab = szene.antwort(z, modul, sz, pid, duc, extra)
    szene.zeile_einfuegen(z, modul, sz, pid, text, gefuehl)
    return {"duc": duc, "text": text, "verworfen": verworfen, "gefuehl": gefuehl, "abgeschnitten": ab, "laeufe": LOG[n:]}


def szenario(name, pid, modul, seed, nr):
    ZAEHLER[0], ZAEHLER[1] = seed + FIGUREN.index(pid) * 100, 0
    z = spiel(pid, modul, seed, nr)
    del LOG[:]
    if name == "kaltstart":
        sz = szene.starten(z, modul, szene_def(pid, modul, frei=False))
        zeile = [e for e in sz["log"] if e.get("art") == "figur"]
        return {"erste": None, "thema": None, "system": None, "zuege": [{"duc": None, "text": zeile[0]["text"] if zeile else "", "verworfen": zeile[0]["verworfen"] if zeile else [],
                                                                          "gefuehl": zeile[0]["gefuehl"] if zeile else None, "abgeschnitten": False, "laeufe": list(LOG)}]}
    sz = szene.starten(z, modul, szene_def(pid, modul))
    del LOG[:]
    erste = next((e["text"] for e in sz["log"] if e.get("art") == "figur"), None)
    pid_thema = [i for i in R.stand(z, pid)["gesehen"]][-1:] or [None]
    wer = pid
    chips = sz.get("start_chips") or []
    zuege = []
    absage, neues = None, None
    if name in NEIN_ARTEN:
        duc = "Tell me you want me, Megan." if pid == "megan" else "*leans in and kisses her*"
        sz["log"].append({"art": "duc", "text": duc})
        sz["zug"] += 1
        if name == "nein":
            absage = ABSAGE_ANRUF if pid == "megan" else ABSAGE
        else:                                            # echte Absage nach Vertrauensstufe (figurenrahmen.json "absage")
            stufe = z["werte"].get("vertrauen." + pid, 0)
            absage = '"%s"' % R.fuellen(z, modul, pid, R.figur(modul, pid)["absage"]["vertrauen_" + R._bereich(stufe)])
        szene.zeile_einfuegen(z, modul, sz, pid, absage, "neutral")
        sz.setdefault("chronik_hinweise", {}).setdefault(pid, []).append(NEIN_VORGABE)
        st = R.stand(z, pid)
        frei = [x for x in R.figur(modul, pid).get("themen", []) if R.bedingung(z, pid, x.get("wenn")) and x["id"] not in st["gesehen"]]
        neues = frei[0] if frei else None
    for d in DREHBUCH[name](wer):
        fest = None
        if isinstance(d, tuple):
            d, fest = d
        if d == "CHIP":
            d = (neues or {}).get("chips", [{"text": "Tell me more about that."}])[0]["text"]
        d = d or (chips[0]["text"] if chips else "Tell me more about that.")
        if fest:                                         # der Code antwortet, nicht das Modell
            zweite = R.figur(modul, pid)["absage"].get("nachhaken") or ZWEITE_ABSAGE.strip('"')
            text = '"%s"' % R.fuellen(z, modul, pid, neues["einstieg"]) if fest == "THEMA" and neues else '"%s"' % R.fuellen(z, modul, pid, zweite)
            sz["log"].append({"art": "duc", "text": d})
            sz["zug"] += 1
            szene.zeile_einfuegen(z, modul, sz, pid, text, "neutral")
            zuege.append({"duc": d, "text": text, "fest": True, "verworfen": [], "gefuehl": "neutral", "abgeschnitten": False, "laeufe": []})
            continue
        zuege.append(zug_spielen(z, modul, sz, pid, d))
    return {"erste": erste, "thema": pid_thema[0], "absage": absage, "system": szene.figur_prompt(z, modul, sz, pid), "zuege": zuege}


def erkennung(ohne_grammatik=False):
    out = []
    gram = llm.bool_grammatik(["does_it"])
    for text, soll, art in FAELLE:
        ZAEHLER[0], ZAEHLER[1] = 7, 0
        t0 = time.time()
        roh, _ = llm.chat(PRUEF_SYS, PRUEF_USER % (text, HANDLUNG[art]), max_tokens=24, grammar=None if ohne_grammatik else gram)
        try:
            ist = json.loads(re.search(r"\{.*?\}", roh, re.S).group(0))["does_it"]
            lesbar = isinstance(ist, bool)
        except Exception:
            ist, lesbar = None, False
        out.append({"text": text, "soll": soll, "ist": ist, "lesbar": lesbar, "roh": roh[:120], "sek": round(time.time() - t0, 2)})
    return out


def vram():
    r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
    return [int(x) for x in r.stdout.strip().split(",")]


def kobold_start(datei, log):
    pfad = os.path.join(KOBOLD, datei)
    if not os.path.exists(pfad):
        raise SystemExit("Modell fehlt: " + pfad)
    frei = vram()
    print("VRAM vorher", frei, flush=True)
    p = subprocess.Popen([EXE, "--model", pfad, "--usecuda", "normal", "0", "mmq", "--gpulayers", "999", "--contextsize", "16384", "--flashattention", "--batchsize", "1024",
                          "--jinja", "--port", str(PORT), "--quiet", "--skiplauncher"], cwd=KOBOLD, stdout=log, stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < 420:
        if p.poll() is not None:
            raise SystemExit("KoboldCpp beendet, Code %s" % p.returncode)
        if llm.bereit():
            return p, {"vram_vorher": frei[0], "vram_danach": vram()[0], "gesamt": frei[1], "laden_sek": round(time.time() - t0)}
        time.sleep(3)
    p.kill()
    raise SystemExit("KoboldCpp nicht bereit nach 7 Minuten")


def kobold_stopp(p):
    subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
    p.wait(timeout=60)
    time.sleep(5)


def fertig_laden(pfad):
    try:
        return json.load(open(pfad, encoding="utf-8"))
    except Exception:
        return {"erkennung": None, "erkennung_frei": None, "szenen": {}}


def speichern(pfad, d):
    with open(pfad + ".tmp", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(pfad + ".tmp", pfad)


def modell_lauf(name, modul, aus, stopp_datei):
    pfad = os.path.join(aus, name + ".json")
    d = fertig_laden(pfad)
    with open(os.path.join(aus, name + "_kobold.log"), "ab") as log:
        p, info = kobold_start(MODELLE[name], log)
    try:
        d.update(info, datei=MODELLE[name], vram_spitze=info["vram_danach"])
        print(name, info, flush=True)
        # Gleicher Seed, gleiche Antwort? Sonst waeren die Modelle nicht vergleichbar.
        ZAEHLER[0], ZAEHLER[1] = 5, 0
        a = chat("You write one short sentence.", "Describe the sea.", {"temperature": 1.0, "min_p": 0.1, "top_p": 0.95}, 40)[0]
        ZAEHLER[0], ZAEHLER[1] = 5, 0
        b = chat("You write one short sentence.", "Describe the sea.", {"temperature": 1.0, "min_p": 0.1, "top_p": 0.95}, 40)[0]
        d["seed_stabil"] = a == b
        if not d.get("erkennung"):
            d["erkennung"] = erkennung()
            d["erkennung_frei"] = erkennung(ohne_grammatik=True)
            speichern(pfad, d)
        for pid in FIGUREN:
            for nr, seed in enumerate(SEEDS):
                for sz_name in SZENARIEN:
                    k = "%s|%s|%d" % (pid, sz_name, seed)
                    if k in d["szenen"]:
                        continue
                    if os.path.exists(stopp_datei):
                        print("Stopp-Datei gefunden", flush=True)
                        return False
                    t0 = time.time()
                    d["szenen"][k] = szenario(sz_name, pid, modul, seed, nr)
                    d["vram_spitze"] = max(d["vram_spitze"], vram()[0])
                    speichern(pfad, d)
                    print(k, round(time.time() - t0), "s", flush=True)
        d["fertig"] = True
        speichern(pfad, d)
        return True
    finally:
        kobold_stopp(p)


def trocken(modul):
    llm.chat = stub
    for pid in FIGUREN:
        for sz_name in SZENARIEN:
            e = szenario(sz_name, pid, modul, SEEDS[1], 1)
            print(pid, sz_name, "| erste:", (e["erste"] or "-")[:70], "| Thema:", e["thema"], "| Zuege:", [z["duc"] for z in e["zuege"]], "| System-Zeichen:", len(e["system"] or ""))
        if e.get("absage"):
            print("   Absage:", e["absage"], "| feste Zeilen:", [z["text"][:60] for z in e["zuege"] if z.get("fest")])
    print("Faelle:", len(FAELLE), "echt:", sum(1 for f in FAELLE if f[1]))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--modelle", default="blume")
    a.add_argument("--aus", default=os.path.join(EDEN, "docs", "abnahme", "llm_vergleich"))
    a.add_argument("--trocken", action="store_true")
    a.add_argument("--szenarien", help="Komma-Liste, Standard: die fuenf aus Runde 1")
    o = a.parse_args()
    modul = json.load(open(os.path.join(EDEN, "module", "eden_rise", "modul.json"), encoding="utf-8"))
    modul.setdefault("id", "eden_rise")
    szene.CFG.update(json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8")))
    if o.szenarien:
        SZENARIEN[:] = o.szenarien.split(",")
    if o.trocken:
        return trocken(modul)
    os.makedirs(o.aus, exist_ok=True)
    llm.URL = "http://127.0.0.1:%d" % PORT
    llm.chat = chat
    stopp = os.path.join(o.aus, "STOPP")
    for name in o.modelle.split(","):
        if not modell_lauf(name, modul, o.aus, stopp):
            break
    print("Ende", flush=True)


if __name__ == "__main__":
    main()

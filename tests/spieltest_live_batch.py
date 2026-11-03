"""Serial live-test coordinator, started explicitly after the scheduled GPU switch."""
import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
BASE = HIER.parent
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(BASE))
import spieltest_peer as P
import spieltest_rezension as R
import spieltest_auswertung as A
from spieltest_reviewstruktur import sprechtext


def write(path, data):
    path = Path(path)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    temp.replace(path)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def run(root, profil, pilot=False):
    target = root / (("pilot-" if pilot else "lauf-") + profil)
    result = target / "ergebnis.json"
    if result.exists():
        return json.loads(result.read_text(encoding="utf-8"))
    adoption = root / "uebernommener-lauf.json"
    if adoption.exists():
        running = json.loads(adoption.read_text(encoding="utf-8"))
        if running["profil"] == profil and not pilot:
            pid = int(running["pid"])
            write(root / "batch-status.json", dict(phase="spieltest", profil=profil, pid=pid, zeit=now(), uebernommen=True))
            while not result.exists():
                query = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                    "(Get-CimInstance Win32_Process -Filter 'ProcessId=%d').CommandLine" % pid],
                    capture_output=True, text=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                if "spieltest_live.py" not in query.stdout or str(target) not in query.stdout:
                    raise RuntimeError("Übernommener Lauf %s beendet, aber kein Ergebnis vorhanden" % profil)
                time.sleep(15)
            return json.loads(result.read_text(encoding="utf-8"))
    target.mkdir(parents=True, exist_ok=True)
    args = [sys.executable, str(HIER / "spieltest_live.py"), "--profil", profil, "--ziel", str(target)]
    if pilot:
        args += ["--bis-tag", "2", "--max-calls", "100"]
    if (target / "checkpoint.pickle").exists():
        args += ["--resume"]
    with (target / "prozess.out.log").open("a", encoding="utf-8") as out, (target / "prozess.err.log").open("a", encoding="utf-8") as err:
        proc = subprocess.Popen(args, cwd=BASE, env=dict(os.environ, PYTHONHASHSEED="0", PYTHONUTF8="1"), stdout=out, stderr=err)
        write(root / "batch-status.json", dict(phase="pilot" if pilot else "spieltest", profil=profil, pid=proc.pid, zeit=now()))
        code = proc.wait()
    if code or not result.exists():
        raise RuntimeError("%s: Prozessfehler %s; Details in %s" % (profil, code, target))
    return json.loads(result.read_text(encoding="utf-8"))


def live_sources(root, profil):
    path = root / ("lauf-" + profil) / "dialoge.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    scenes = {}
    for row in rows:
        snap = row.get("nachher") or row.get("vorher")
        if row.get("aktion") == "ende":
            snap = row.get("vorher") or snap
        if not snap or not any(x.get("art") == "figur" and x.get("text") for x in snap.get("log", [])):
            continue
        scenes[(snap["tag"], snap["phase"], snap["titel"])] = (row, snap)
    scenes = list(scenes.values())
    picked = scenes if len(scenes) <= 8 else [scenes[i * (len(scenes)-1)//7] for i in range(8)]
    return [dict(id=row["id"], art="dialogtranskript", tag=snap["tag"], phase=snap["phase"], titel=snap["titel"],
                 aktion=row["aktion"], angenommen=row["angenommen"],
                 log=[dict(wer=x.get("wer"), art=x.get("art"), text=(x.get("text") or "")[:500]) for x in snap["log"][-8:]])
            for row, snap in picked]


def belagerung_quellen(roh, profil, index):
    """Die Belagerung ist gescriptet (keine Modell-Dialoge) und kam nur als ein Kalenderpunkt (bl_welle_6) in die
    Stichprobe; Minicus Szene und das Akt-2-Ende fehlten (02.11.2026). Je Lauf eine eigene Quelle: Taktik-Ergebnis und
    alle erreichten bl_-Szenen in Reihenfolge, Welle 6, Bericht und Cliffhanger mit ihren ersten Zeilen."""
    out = []
    for r in roh["laeufe"]:
        if r["typ"] != profil:
            continue
        bl = [e for e in (r.get("events") or {}) if e.startswith("bl_") and e in index]
        if not bl and not r.get("taktik"):
            continue
        wahl = {k.rsplit(":", 1)[0]: int(k.rsplit(":", 1)[1]) for k in (r.get("event_wahl") or {})}
        szenen = []
        for eid in bl:                                     # knapp: Blume hat 16k Kontext, die Rezension braucht 4k davon
            ev = index[eid]
            s = dict(id=eid, tag=r["events"][eid], titel=ev.get("titel", ""))
            i = wahl.get(eid)
            if i is not None and 0 <= i < len(ev.get("optionen") or []) and len(ev["optionen"]) > 1:
                s["wahl"] = (ev["optionen"][i].get("text") or "")[:100]
            if eid.startswith(("bl_welle_6", "bl_bericht", "bl_cliff_")):
                s["lage"] = (ev.get("lage") or "")[:200]
                s["dialog"] = [dict(wer=z.get("wer"), text=(z.get("text") or "")[:140]) for z in (ev.get("zeilen") or [])[:2]]
            szenen.append(s)
        out.append(dict(id="belagerung:%s/%s" % (r["typ"], r["seed"]),
                        art="Belagerung Tag 21-23 und Ende von Akt 2: erreichte Szenen in Reihenfolge und Ergebnis der "
                            "Taktik-Karte; Offline-Messung, keine menschliche Erfahrung",
                        taktik=r.get("taktik"), ende=r.get("ende"), szenen=szenen))
    return out


def reviews(root, out, roh, prefix="Eden-Rise-Live"):
    from kern import llm
    events = json.loads((BASE / "module/eden_rise/ereignisse.json").read_text(encoding="utf-8"))["events"]
    packets = R.pakete(roh, events, limit=4)
    system = R.SYSTEM
    start = system.index("Das Spiel wurde offline")
    end = system.index("Unterscheide Messbefund")
    system = system[:start] + ("Es gibt echte lokale Modellgespräche, gekennzeichnet als dialogtranskript, und Live-Messungen. "
        "Beurteile nur diese sichtbaren Gesprächsverläufe und die gelieferten Quellen. Die Spielmechanik wurde teilweise durch "
        "Engine-Routinen bedient. Bilder, Stimme, Browsersteuerung und menschliches Erleben wurden nicht geprüft. "
        "Die Transkripte sind Stichproben, keine vollständige Lektüre des ganzen Spiels. "
        "Hat ein Profil die Belagerung erreicht, beschreibt eine Quelle belagerung:... sie vom Anfang bis zum Ende von Akt 2.\n") + system[end:]
    index = {e["id"]: e for e in events}
    results = []
    evidence = []
    for packet in packets["pakete"]:
        pid = packet["id"]
        prior = root / ("review-" + pid + ".json")
        packet["quellen"] += live_sources(root, pid) + belagerung_quellen(roh, pid, index)
        for q in packet["quellen"]:
            if q["id"].startswith("lauf:"):
                q["art"] = "Live-Messung aus isoliertem Spielstand, keine menschliche Erfahrung"
        packet["grenze"] = "Echte protokollierte LLM-Dialoge plus verfasste Eventdefinitionen; Textstichprobe ohne visuelle Prüfung."
        packet["laufstand"]["hinweis"] += " Live-Modell verwendet; kein menschlicher Spieltest."
        evidence.append(packet)
        if prior.exists():
            result = json.loads(prior.read_text(encoding="utf-8"))
            R.validieren(result, packet)
        else:
            error = ""
            for attempt in range(2):
                text, seconds = llm.chat(system, json.dumps(packet, ensure_ascii=False) + error, max_tokens=4000)
                (root / ("review-%s-%d-roh.txt" % (pid, attempt))).write_text(text, encoding="utf-8")
                try:
                    candidate = text[text.index("{"):text.rindex("}")+1]
                    result = R.validieren(json.loads(candidate), packet)
                    write(prior, result)
                    break
                except (ValueError, KeyError, TypeError) as ex:
                    error = "\nPrevious format invalid: %s. Return complete corrected JSON with exact fields and only given source IDs." % ex
            else:
                raise RuntimeError("Reviewformat für %s nach zwei Versuchen ungültig" % pid)
        results.append(dict(id=pid, name=packet["profil"]["name"], review=result))
        # Keep every validated review deliverable even if the fixed deadline interrupts a later one.
        write(out / (prefix + "-Rezensionen.json"), dict(zeit=now(), status="Zwischenstand", reviews=results))
        write(out / (prefix + "-Beleganhang.json"), dict(zeit=now(), pakete=evidence))
        (out / (prefix + "-Rezensionen-Vorlesen.txt")).write_text(sprechtext(results), encoding="utf-8")
        write(root / "batch-status.json", dict(phase="rezension", profil=pid, fertig=len(results), zeit=now()))
    write(out / (prefix + "-Rezensionen.json"), dict(zeit=now(), reviews=results))
    write(out / (prefix + "-Beleganhang.json"), dict(zeit=now(), pakete=evidence))
    (out / (prefix + "-Rezensionen-Vorlesen.txt")).write_text(sprechtext(results), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ziel", type=Path, required=True)
    ap.add_argument("--outputs", type=Path, required=True)
    a = ap.parse_args()
    root, out = a.ziel.resolve(), a.outputs.resolve()
    root.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    try:
        # An already-running first pilot is explicitly allowed; never launch a duplicate.
        first = root / "pilot-naomi"
        if (first / "status.json").exists() and not (first / "ergebnis.json").exists():
            deadline = time.monotonic() + 1800
            while not (first / "ergebnis.json").exists():
                if (first / "fehler.json").exists() or time.monotonic() > deadline:
                    raise RuntimeError("Erster Pilot fehlgeschlagen oder Zeitlimit überschritten")
                time.sleep(3)
        pilots = [run(root, pid, True) for pid in ("naomi", "tandi")]
        for p in pilots:
            live = p.get("live", {})
            if live.get("spieleraufrufe", 0) < 1 or live.get("modellaufrufe", 0) <= live.get("spieleraufrufe", 0) or live.get("transkripte", 0) < 1:
                raise RuntimeError("Pilot belegt keine echten Spieler- und Engine-Modellantworten")
            logs = [json.loads(l) for l in (root / ("pilot-" + p["typ"]) / "dialoge.jsonl").read_text(encoding="utf-8").splitlines()]
            if not any(r.get("spielertext") for r in logs):
                raise RuntimeError("Pilot ohne echte freie Spieleräußerung")
            if not any(x.get("art") == "figur" and x.get("text") for r in logs for snap in (r.get("vorher"),r.get("nachher"))
                       if snap for x in snap.get("log", [])):
                raise RuntimeError("Pilot ohne sichtbare Figurenantwort")
        write(root / "pilot-abnahme.json", dict(zeit=now(), echt_llm=True,
            hinweis="Kurze echte Dialog-/Entscheidungspiloten; Date- und Langzeitprüfungen im vollständigen Durchlauf noch offen.",
            profile=[dict(profil=p["typ"], live=p["live"], ende=p["ende"]) for p in pilots]))
        runs = []
        for pid in ("naomi", "mia", "lenny", "tandi", "noor", "alex", "deniz", "mateo", "avery"):
            result = run(root, pid)
            if result["ende"]["status"] != "ende":
                raise RuntimeError("%s erreicht das Ende nicht" % pid)
            runs.append(result)
            write(root / "abgeschlossene-laeufe.json", runs)
            if pid == "lenny" and not (root / "prioritaet-fertig.json").exists():
                priority = dict(laeufe=[r for r in runs if r["typ"] in ("mia", "lenny")],
                                commit="siehe quellenstand-start.json", dirty=True, zeit=now(), profil_version=2)
                reviews(root, out, priority, prefix="Eden-Rise-Live-Prioritaet")
                write(root / "prioritaet-fertig.json", dict(zeit=now(), profile=["mia", "lenny"],
                    vorlesetext=str(out / "Eden-Rise-Live-Prioritaet-Rezensionen-Vorlesen.txt")))
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=BASE, capture_output=True, text=True).stdout.strip()
        roh = dict(laeufe=runs, commit=commit, dirty=True, zeit=now(), profil_version=2)
        write(root / "roh.json", roh)
        peer = P.auswerten(roh)
        # Preserve honest technical criteria, but correct the offline-only presentation header.
        peer["hinweis"] = "Echte lokale LLM-Dialoge, neun simulierte Profile; mechanische Routinen teilweise mit Engine-Zuständen. Keine visuelle oder menschliche Spielprüfung."
        (out / "Eden-Rise-Live-Spieltest.html").write_text(P.seite(peer).replace(P.HINWEIS, peer["hinweis"]), encoding="utf-8")
        write(out / "Eden-Rise-Live-Spieltest.json", peer)
        reviews(root, out, roh)
        write(root / "batch-status.json", dict(phase="abgeschlossen", zeit=now(), profile=len(runs), outputs=str(out)))
    except Exception as ex:
        write(root / "batch-status.json", dict(phase="fehler", zeit=now(), fehler=type(ex).__name__, text=str(ex)))
        raise


if __name__ == "__main__":
    main()

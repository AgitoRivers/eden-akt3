# -*- coding: utf-8 -*-
r"""Vertont alle festen Saetze des Moduls eden_rise vorab mit Chatterbox (17.10.2026):
Event-Zeilen (ereignisse.json), Laden-Saetze (laeden.json) und die Saetze des Haendlers (modul.json, rollen.haendler).

    Vertonen_EdenRise.bat                 alles, was noch fehlt (bereits erzeugte Zeilen werden uebersprungen)
    Vertonen_EdenRise.bat --nur 3         Probelauf mit 3 Zeilen
    Vertonen_EdenRise.bat --wer lola      nur eine Figur
    Vertonen_EdenRise.bat --schluessel t0_holm#o3,hk_rosi_v#z0   nur diese Zeilen (z. B. zum Probehoeren)
    Vertonen_EdenRise.bat --praefix lob.  nur Schluessel mit diesem Anfang
    Vertonen_EdenRise.bat --liste         nur auflisten, nichts erzeugen
    Vertonen_EdenRise.bat --fehlende-auslassen   Figuren ohne zugeordnete Stimme ueberspringen statt abzubrechen
    Vertonen_EdenRise.bat --aufraeumen   vorher alte Aufnahmen geaenderter/geloeschter Saetze in den Papierkorb (25.10.2026)

Stimme je Figur: eden-config.json -> stimmen.eden_rise.<id>. Ablage module\eden_rise\audio\<hash>.wav - derselbe
Schluessel wie stimme.chatterbox (Stimmdatei + Text), geaenderte Saetze werden also beim naechsten Lauf neu erzeugt.
Index fuer die Engine: module\eden_rise\audio_index.json (Schluessel -> Datei, Figur, Stimme, Text).
Langlaeufer: per .bat im eigenen Fenster starten, nicht aus einer Sitzung. Braucht Chatterbox auf Port 8004."""
import json, os, sys, time

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # werkzeuge\eden_rise -> Eden
sys.path.insert(0, EDEN)
from kern import stimme  # noqa: E402

MOD = os.path.join(EDEN, "module", "eden_rise")
ORDNER = os.path.join(MOD, "audio")
INDEX = os.path.join(MOD, "audio_index.json")


def arg(name, std=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else std


def index_aendern(neu=None, weg=(), gueltig=None):
    """Aendert den Index unter einer Sperre: lesen, nur die eigenen Eintraege einarbeiten, atomar schreiben. So verlieren
    parallele Laeufe keine Eintraege mehr (30.10.2026 passiert: drei Laeufe, die Holm-Zeilen waren weg). gueltig: alle
    Schluessel ausserhalb dieser Menge fallen weg (voller Lauf). -> der neue Index."""
    sperre = INDEX + ".lock"
    while True:
        try:
            os.close(os.open(sperre, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(sperre) > 60:      # abgestuerzter Lauf
                    os.remove(sperre)
            except OSError:
                pass
            time.sleep(0.05)
    try:
        index = json.load(open(INDEX, encoding="utf-8")) if os.path.exists(INDEX) else {}
        index.update(neu or {})
        for k in weg:
            index.pop(k, None)
        if gueltig is not None:
            for k in [k for k in index if k not in gueltig]:
                del index[k]
        tmp = "%s.%d.tmp" % (INDEX, os.getpid())
        json.dump(index, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for versuch in range(50):                                    # Windows: ein Leser kann die Datei kurz sperren
            try:
                os.replace(tmp, INDEX)
                break
            except PermissionError:
                if versuch == 49:
                    raise
                time.sleep(0.1)
        return index
    finally:
        os.remove(sperre)


def papierkorb(pfade):
    """Moves files to the Windows recycle bin (never deletes for good)."""
    import ctypes
    from ctypes import wintypes

    class SHFILEOPSTRUCTW(ctypes.Structure):
        _fields_ = [("hwnd", wintypes.HWND), ("wFunc", wintypes.UINT), ("pFrom", wintypes.LPCWSTR),
                    ("pTo", wintypes.LPCWSTR), ("fFlags", ctypes.c_ushort), ("fAnyOperationsAborted", wintypes.BOOL),
                    ("hNameMappings", ctypes.c_void_p), ("lpszProgressTitle", wintypes.LPCWSTR)]
    if not pfade:
        return 0
    op = SHFILEOPSTRUCTW(None, 3, "\0".join(pfade) + "\0\0", None, 0x0040 | 0x0010 | 0x0004 | 0x0400, False, None, None)
    return ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))      # FO_DELETE, ALLOWUNDO, NOCONFIRMATION, SILENT, NOERRORUI


def aufraeumen(alle, stimmen):
    """Recordings whose sentence changed or no longer exists go to the recycle bin; their index entries are dropped,
    so the normal run records the new wording. Files that are not in the index are never touched."""
    index = json.load(open(INDEX, encoding="utf-8")) if os.path.exists(INDEX) else {}
    jetzt = {k: (stimmen.get(w), text) for k, w, text in alle}
    gueltig = {k for k, e in index.items() if k in jetzt and (e.get("stimme"), e.get("text")) == jetzt[k]}
    behalten = {index[k]["datei"] for k in gueltig}
    weg = [k for k in index if k not in gueltig]
    dateien = sorted({index[k]["datei"] for k in weg} - behalten)
    pfade = [os.path.join(ORDNER, d) for d in dateien if os.path.isfile(os.path.join(ORDNER, d))]
    fehler = papierkorb(pfade)
    index_aendern(weg=weg)
    print("Aufraeumen: %d alte Aufnahmen in den Papierkorb, %d Index-Eintraege entfernt%s"
          % (len(pfade), len(weg), "" if not fehler else " (Papierkorb meldet Fehler %d)" % fehler), flush=True)


def saetze():
    """[(schluessel, figur, text)] in fester Reihenfolge."""
    out = []
    ev = json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]
    for e in ev:
        for n, z in enumerate(e["zeilen"]):
            out.append(("%s#z%d" % (e["id"], n), z["wer"], z["text"]))
        for k, o in enumerate(e["optionen"]):
            if o.get("zeile"):
                out.append(("%s#o%d" % (e["id"], k), o["zeile"]["wer"], o["zeile"]["text"]))
            if o.get("zeile_fehlschlag"):                       # Favours (29.10.2026): Pointe beim Fehlschlag
                out.append(("%s#f%d" % (e["id"], k), o["zeile_fehlschlag"]["wer"], o["zeile_fehlschlag"]["text"]))
        # Erzaehlerin liest den Lagetext der Ortsbilder (Duc 02.11.2026): <id>#l, Stimme stimmen.eden_rise.erzaehler.
        # Wiedergabe: eden.event_zeile (Teil l) + client evSprich; tests/test_erzaehlerin.py haelt beide Texte gleich
        if e.get("art") == "ort" and e.get("lage") and "{" not in e["lage"]:
            out.append(("%s#l" % e["id"], "erzaehler", e["lage"].replace("*", "")))
    laeden = json.load(open(os.path.join(MOD, "laeden.json"), encoding="utf-8"))["laeden"]
    for lid, l in laeden.items():
        for gruppe, liste in (l.get("zeilen") or {}).items():
            for i, s in enumerate(liste):
                out.append(("laden.%s.%s.%d" % (lid, gruppe, i), l["wer"], s))
    modul = json.load(open(os.path.join(MOD, "modul.json"), encoding="utf-8"))
    hid = (modul.get("rollen") or {}).get("haendler")
    for gruppe, liste in (modul["laeden"].get(hid, {}).get("haendler_zeilen") or {}).items():
        for i, s in enumerate(liste):
            out.append(("laden.%s.%s.%d" % (hid, gruppe, i), hid, s))
    # Missionsausbau 18.10.2026: Kommentare der Auftraggeber (job.*) und der Ladenfiguren beim Teilekauf (teil.*)
    for pid, gruppen in (modul.get("job_zeilen") or {}).items():
        for gruppe, liste in gruppen.items():
            for i, (_, s) in enumerate(liste):
                out.append(("job.%s.%s.%d" % (pid, gruppe, i), pid, s))
    for iid, it in modul["items"].items():
        if it.get("kommentar"):
            out.append(("teil." + iid, it["kommentar"]["wer"], it["kommentar"]["text"]))
    from kern import tutorial                            # Maxwells Kampf-Tutorial (24.10.2026)
    for sid, s in tutorial.SCHRITTE.items():
        out.append(("tut." + sid, "maxwell", s["en"]))
    kampfdatei = os.path.join(MOD, "kaempfe.json")       # Hinweise unberuehrbarer Gegner (Sirene, 29.10.2026): kampf.<gegner>.<n>
    if os.path.exists(kampfdatei):
        for gid, g in (json.load(open(kampfdatei, encoding="utf-8")).get("enemies") or {}).items():
            for i, h in enumerate(g.get("untouchable_hinweise") or []):
                out.append(("kampf.%s.%d" % (gid, i), h["wer"], h["text"]))
            for art, liste in (g.get("sprueche") or {}).items():     # Sprueche im Kampf (Riccis, 29.10.2026)
                for i, h in enumerate(liste):
                    out.append(("kampf.%s.%s.%d" % (gid, art, i), h["wer"], h["text"]))
        for bid, b in (json.load(open(kampfdatei, encoding="utf-8")).get("encounters") or {}).items():
            for art, liste in (b.get("sprueche") or {}).items():     # Gruppen reden als eine (Mehrgegner, 29.10.2026)
                for i, h in enumerate(liste):
                    out.append(("kampf.%s.%s.%d" % (b.get("sprueche_id", bid), art, i), h["wer"], h["text"]))
    if os.path.exists(kampfdatei):                       # Taunts beim Zoegern (03.11.2026): generische Stimmen je Gruppe
        for gid, g in (json.load(open(kampfdatei, encoding="utf-8")).get("taunts") or {}).items():
            for z in g.get("zeilen") or []:
                out.append((z["id"], "stimme:" + g["stimme"], z["text"]))
    from kern import anhoerung                           # Anhoerung (25.10.2026): Megans Saetze + Aussagen je Fall
    out += anhoerung.alle_zeilen(modul, MOD)
    from kern import sturm                               # Sturm an Tag 5 (27.10.2026): st.*
    out += sturm.alle_zeilen(MOD)
    from kern import expedition                          # Rast-Anrufe im Ortskapitel (26.10.2026)
    for pid, stufen in expedition.rast_texte(MOD).items():
        for stufe, liste in stufen.items():
            for i, a in enumerate(liste):
                out.append(("rast.%s.%s.%d" % (pid, stufe, i), pid, a["text"]))
    lobdatei = os.path.join(MOD, "lob.json")             # Lob fuer Attributsteigerungen (27.10.2026): lob.<pid>.<attribut>.<wert>
    if os.path.exists(lobdatei):
        for pid, atts in (json.load(open(lobdatei, encoding="utf-8")).get("zeilen") or {}).items():
            for att, stufen in sorted(atts.items()):
                for wert, text in sorted(stufen.items()):
                    out.append(("lob.%s.%s.%s" % (pid, att, wert), pid, text))
    tischdatei = os.path.join(MOD, "tisch.json")         # Tischszenen (27.10.2026): tisch.<pid>.0 = erster Bissen, .1/.2 = Erinnerungen
    if os.path.exists(tischdatei):
        for pid, s in (json.load(open(tischdatei, encoding="utf-8")).get("szenen") or {}).items():
            out.append(("tisch.%s.0" % pid, pid, s["bissen"]["text"]))
            for i, e in enumerate(s["erinnerung"], 1):
                out.append(("tisch.%s.%d" % (pid, i), pid, e["text"]))
    from kern import mochis                              # Bibis Overlay nach dem ersten Fang (01.11.2026): mochis.<tier>.<n>
    out += mochis.alle_zeilen(modul)
    from kern import legenden                            # Dorf redet (30.10.2026): leg.<id>
    out += legenden.alle_zeilen(MOD)
    from kern import taktik                              # Taktik-Karte (02.11.2026): Szenen, Briefings, Appell: tk.*
    out += taktik.alle_zeilen(MOD)
    from kern import figurenrahmen                       # feste erste Zeilen der freien Szenen (31.10.2026): rahmen.<pid>.<id>[.<anrede>]
    out += figurenrahmen.alle_zeilen(MOD)
    kuechendatei = os.path.join(MOD, "kuechen.json")     # Fredericos Saetze beim Verlassen von Nonnas Laden (27.10.2026): fred.<n>
    if os.path.exists(kuechendatei):
        for i, s in enumerate(json.load(open(kuechendatei, encoding="utf-8")).get("frederico") or []):
            out.append(("fred.%d" % i, "frederico", s["text"]))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cfg = json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8-sig"))
    stimmen = (cfg.get("stimmen") or {}).get("eden_rise") or {}
    katalog = {s["name"] for s in stimme.katalog()}
    alle = saetze()
    if "--aufraeumen" in sys.argv:
        aufraeumen(alle, stimmen)                      # always against the full list, never a filtered one
    if arg("--ohne"):                                  # Sprecher auslassen, z. B. --ohne sophia (Stimme wird noch gewechselt)
        weg = set(arg("--ohne").split(","))
        alle = [s for s in alle if s[1] not in weg]
    if arg("--wer"):
        alle = [s for s in alle if s[1] == arg("--wer")]
    if arg("--praefix"):                               # only keys starting with this, e.g. --praefix lob. (Lob, 27.10.2026)
        alle = [s for s in alle if s[0].startswith(arg("--praefix"))]
    if arg("--schluessel"):                            # only these keys (comma-separated), e.g. a listening test
        nur = set(arg("--schluessel").split(","))
        alle = [s for s in alle if s[0] in nur]
    for w in {w for _, w, _ in alle if w.startswith("stimme:")}:     # Katalogstimme direkt (Taunt-Gruppen, 03.11.2026)
        stimmen[w] = w[7:]
    ohne = sorted({w for _, w, _ in alle if stimmen.get(w) not in katalog})
    if ohne and "--fehlende-auslassen" in sys.argv:
        print("Ohne Stimme, uebersprungen: %s (eden-config.json stimmen.eden_rise zuordnen)" % ", ".join(ohne))
        alle = [s for s in alle if s[1] not in ohne]
        ohne = []
    if ohne:
        sys.exit("Ohne Stimme im Katalog: %s - erst in eden-config.json (stimmen.eden_rise) zuordnen." % ", ".join(ohne))
    if "--liste" in sys.argv:
        je = {}
        for _, w, _ in alle:
            je[w] = je.get(w, 0) + 1
        print(len(alle), "Saetze:", ", ".join("%s %d (%s)" % (w, n, stimmen[w]) for w, n in sorted(je.items(), key=lambda x: -x[1])))
        return
    if not stimme.chatterbox_bereit():
        sys.exit("Chatterbox laeuft nicht (Port 8004) - Start-Chatterbox-TURBO-FAST.bat starten, dann nochmal.")
    if arg("--nur"):
        alle = alle[:int(arg("--nur"))]
    t0, neu, fehler = time.time(), 0, []
    frisch = {}
    for n, (key, wer, text) in enumerate(alle, 1):
        name = stimmen[wer]
        try:
            vorher = time.time()
            pfad = stimme.chatterbox(name, text, ORDNER, ganz=True)
            if time.time() - vorher > 0.5:
                neu += 1
            frisch[key] = {"datei": os.path.basename(pfad), "wer": wer, "stimme": name, "text": text}
        except Exception as e:
            fehler.append((key, str(e)))
        if n % 10 == 0 or n == len(alle):
            dauer = time.time() - t0
            rest = dauer / max(1, neu) * (len(alle) - n) if neu else 0
            print("%4d/%d  neu %d  Fehler %d  noch ca. %d min" % (n, len(alle), neu, len(fehler), rest / 60), flush=True)
            index_aendern(frisch)
            frisch = {}
    # voller Lauf: Eintraege geloeschter/umbenannter Saetze entfernen. Jeder Filter macht daraus einen Teillauf - sonst wirft
    # z. B. --schluessel den ganzen Rest aus dem Index (26.10.2026 passiert, Index aus dem Cache neu aufgebaut)
    if not any(arg(f) for f in ("--nur", "--wer", "--schluessel", "--ohne", "--praefix")):
        gueltig = {k for k, _, _ in alle}
        vorher = index_aendern(frisch)
        index_aendern(gueltig=gueltig)
        weg = [k for k in vorher if k not in gueltig]
        if weg:
            print("aus dem Index entfernt (Satz gibt es nicht mehr): %d" % len(weg))
    else:
        index_aendern(frisch)
    print("fertig: %d Saetze, davon %d neu erzeugt, %d Fehler. Index: %s" % (len(alle), neu, len(fehler), INDEX))
    for key, f in fehler[:20]:
        print("  FEHLER", key, f)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import effekte                                    # Hall je Figur (Sirene, 28.10.2026) - vor der Lautheit
    effekte.lauf()
    import lautheit_angleichen                        # neue Aufnahmen gleich laut machen (-20 LUFS, 26.10.2026)
    lautheit_angleichen.lauf()


if __name__ == "__main__":
    main()

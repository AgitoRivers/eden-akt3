"""Deadline finalizer: review completed profiles, identify unfinished runs honestly."""
import argparse
import datetime
import json
from pathlib import Path
import spieltest_peer as P
from spieltest_live_batch import reviews, write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ziel", type=Path, required=True)
    ap.add_argument("--outputs", type=Path, required=True)
    a = ap.parse_args()
    root, out = a.ziel, a.outputs
    out.mkdir(parents=True, exist_ok=True)
    runs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(root.glob("lauf-*/ergebnis.json"))]
    complete = [r for r in runs if r.get("ende", {}).get("status") == "ende"]
    missing = [pid for pid in P.PROFILE if pid not in {r["typ"] for r in complete}]
    summary = dict(zeit=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        grund="Feste Nutzerfrist 31.10.2026 06:00 Europe/Berlin; Spielphase um 05:15 beendet für Berichte.",
        abgeschlossen=[r["typ"] for r in complete], nicht_vollstaendig=missing,
        hinweis="Unfertige Profile sind keine bestandenen Durchläufe. Ihre Zwischenstände und Dialoge bleiben im Arbeitsordner erhalten.")
    write(out / "Eden-Rise-Live-Friststatus.json", summary)
    if not complete:
        (out / "Eden-Rise-Live-Fristbericht.md").write_text(
            "# Eden Rise – Fristbericht\n\nKein vollständiger Profil-Durchlauf bis zum Berichtsfenster. "
            "Die tatsächlichen Zwischenstände bleiben erhalten; es werden keine vollständigen Rezensionen erfunden.\n", encoding="utf-8")
        return
    roh = dict(laeufe=complete, commit="siehe Quellenstand", dirty=True, zeit=summary["zeit"], profil_version=2)
    peer = P.auswerten(roh)
    peer["hinweis"] = "Echte lokale LLM-Dialoge; mechanische Routinen teilweise mit Engine-Zuständen. Keine visuelle oder menschliche Spielprüfung."
    if missing:
        peer["hinweis"] += " Fristbedingt nicht alle Profile vollständig."
    (out / "Eden-Rise-Live-Spieltest.html").write_text(P.seite(peer).replace(P.HINWEIS, peer["hinweis"]), encoding="utf-8")
    write(out / "Eden-Rise-Live-Spieltest.json", peer)
    reviews(root, out, roh)
    text = "# Eden Rise – Abschluss mit fester Frist\n\nAbgeschlossen: %s.\n\nNicht vollständig: %s.\n\n%s\n" % (
        ", ".join(summary["abgeschlossen"]), ", ".join(missing) or "keine", summary["hinweis"])
    (out / "Eden-Rise-Live-Fristbericht.md").write_text(text, encoding="utf-8")
    write(root / "fristberichte-fertig.json", summary)


if __name__ == "__main__":
    main()

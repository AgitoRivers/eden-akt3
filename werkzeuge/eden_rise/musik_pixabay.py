# -*- coding: utf-8 -*-
r"""Ducs Pixabay-Musikauswahl (27.10.2026) in die Musikbibliothek uebernehmen.

    python werkzeuge\eden_rise\musik_pixabay.py

Laedt jede Auswahl unveraendert nach module\eden_rise\musik\audio\px_<id>.mp3, misst die Lautheit
(Wiedergabe-Gain auf -20 LUFS wie die uebrigen Titel), traegt sie in auswahl.json ein und ergaenzt
CREDITS.md/.html. Bereits eingetragene Titel werden uebersprungen; RAUS nimmt Titel aus der Rotation
(die Dateien bleiben liegen)."""
import datetime, hashlib, html, json, os, re, subprocess, urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MUSIK = os.path.join(EDEN, "module", "eden_rise", "musik")
CDN = "https://cdn.pixabay.com/audio/"
LIZENZ, LIZENZ_URL = "Pixabay Content License", "https://pixabay.com/service/license-summary/"
ZIEL_LUFS = -20.0

# slot: [(Pixabay-ID, Titel, Kuenstler, KI-erzeugt, CDN-Pfad, Seite)]
AUSWAHL = {
    "taktik_karte": [(444879, "Echoes of the Battlefield", "DesiFreeMusic", 1, "2025/11/30/audio_55b66a1053.mp3", "/music/world-echoes-of-the-battlefield-cinematic-percussion-ambience-444879/")],   # Duc 01.11.2026
    "kampf_normal": [(350111, "Upbeat Surf Rock Adventure", "Tunetank", 0, "2025/06/13/audio_727a11399f.mp3", "/music/modern-country-upbeat-surf-rock-adventure-350111/"),
                     (179146, "Kings Of The Surf", "EugeneMyers", 0, "2023/12/01/audio_0c48de74a5.mp3", "/music/rock-kings-of-the-surf-uplifting-summer-sport-rock-179146/"),
                     (350069, "Energetic Surf Rock Music", "Tunetank", 0, "2025/06/13/audio_2cf63e96ea.mp3", "/music/rock-energetic-surf-rock-music-350069/"),
                     (622862, "Retro Funky Groove", "BombinSound", 0, "2026/10/19/audio_c007eea2e9.mp3", "/music/funk-retro-funky-groove-lightwight-funk-622862/")],
    "kampf_tiere": [(493732, "Tribal Drums Epic Action", "Stereo_Color", 0, "2026/03/01/audio_054bc6b0f2.mp3", "/music/percussion-tribal-drums-epic-action-493732/"),
                    (263580, "Pop Thrash with Flamenco Flair", "NickPanek", 1, "2024/11/12/audio_09977b785d.mp3", "/music/folk-energetic-pop-thrash-with-flamenco-flair-263580/"),
                    (490668, "The Drums Music Tribal Percussion", "Alec_Koff", 0, "2026/02/25/audio_8c6887b9a0.mp3", "/music/percussion-the-drums-music-tribal-percussion-tribal-drums-music-490668/")],
    "kampf_komisch": [(311786, "Comedy Fight Music", "DesiFreeMusic", 1, "2025/03/10/audio_a6d88723fc.mp3", "/music/comedy-comedy-fight-music-funny-action-scene-311786/")],
    "kampf_gefaehrlich": [(331490, "Pirate Music", "AudioDollar", 0, "2025/04/23/audio_57cdc86804.mp3", "/music/main-title-pirate-music-pirate-331490/"),
                          (252511, "80s Surf Thrash", "NickPanek", 1, "2024/10/18/audio_391a555a17.mp3", "/music/action-80s-style-surf-thrash-instrumental-252511/")],
    "kampf_boss": [(159171, "To The Death", "Junipersona", 0, "2023/07/22/audio_d5b9d9e43c.mp3", "/music/video-games-to-the-death-159171/")],
    "kampf_sieg": [(527249, "Cinematic Awards Fanfare 8", "pietiX", 1, "2026/04/30/audio_ed43e1334e.mp3", "/sound-effects/musical-cinematic-awards-fanfare-8-527249/")],
    "event_ernst": [(587403, "Noir Jazz Detective Midnight", "alex-morgan", 1, "2026/08/17/audio_b53f504354.mp3", "/music/crime-scene-noir-jazz-detective-midnight-mystery-587403/")],
    "event_witzig": [(350138, "Quirky Eccentric Jazz Theme", "Tunetank", 0, "2025/06/13/audio_88c33eb9fd.mp3", "/music/comedy-quirky-eccentric-jazz-theme-350138/"),
                     (164955, "Upbeat Quirky Background Jazz", "Music_For_Videos", 0, "2023/09/03/audio_3efc7c974a.mp3", "/music/traditional-jazz-upbeat-quirky-background-jazz-164955/"),
                     (164240, "Elevator (Bossa)", "Music_For_Videos", 0, "2023/08/29/audio_cbfe5a2f0d.mp3", "/music/bossa-nova-elevator-164240/")],
    "event_wholesome": [(610897, "Chill Rhodes Lo-Fi", "YuraSoop", 0, "2026/09/27/audio_02ebd9f1c0.mp3", "/music/lofi-chill-rhodes-lo-fi-610897/"),
                        (573876, "Bossa Nova Cafe Morning Breeze", "alex-morgan", 1, "2026/07/25/audio_1f62e58a9a.mp3", "/music/bossa-nova-bossa-nova-cafe-morning-breeze-573876/"),
                        (568179, "Smooth Jazz Midnight Club", "alex-morgan", 1, "2026/07/15/audio_9b3acacc88.mp3", "/music/modern-jazz-smooth-jazz-midnight-club-568179/")],
    "event_frech": [(348267, "Jazz Cafe Music", "Tunetank", 0, "2025/06/13/audio_696ab52c39.mp3", "/music/traditional-jazz-jazz-cafe-music-348267/"),
                    (525829, "Sneaky Jazz", "Sonican", 0, "2026/05/07/audio_cf8a1eadfb.mp3", "/music/smooth-jazz-sneaky-jazz-525829/")],
    "expedition_macchia": [(390508, "Mediterranean Islands", "geoffharvey", 0, "2025/08/16/audio_103090b804.mp3", "/music/acoustic-group-mediterranean-islands-390508/")],
    "anhoerung_gestaendnis": [(512251, "Reflective Piano", "AtlasAudio", 0, "2026/04/01/audio_7be5255395.mp3", "/music/solo-piano-reflective-piano-512251/"),
                              (589281, "Meditative Reflective Piano Quiet Mind", "echoes_of_lumen", 0, "2026/08/20/audio_d82c9df7d9.mp3", "/music/small-drama-meditative-reflective-piano-quiet-mind-589281/"),
                              (533422, "Sad LoFi", "prettyjohn1", 0, "2026/05/23/audio_9c985e2f64.mp3", "/music/beats-sad-lofi-533422/")],
    "nach_urteil": [(524997, "Bittersweet", "leberch", 0, "2026/05/07/audio_c9346b9b4f.mp3", "/music/modern-classical-bittersweet-524997/")],
    "expedition_hafen": [(489898, "Sunlit Streets – Mediterranean Travel Cinematic", "Świat_Rafika", 1, "2026/02/23/audio_b6b031ae59.mp3", "/music/pop-sunlit-streets-mediterranean-travel-cinematic-489898/")],
}
RAUS = {("kampf_komisch", "Fluffing a Duck"), ("event_witzig", "Marty Gots a Plan")}


def lautheit(datei):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", datei, "-af", "loudnorm=I=-20:TP=-2:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr).group(0))


def dauer(datei):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", datei],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    pfad = os.path.join(MUSIK, "auswahl.json")
    daten = json.load(open(pfad, encoding="utf-8"))
    vorher = len(daten["tracks"])
    daten["tracks"] = [t for t in daten["tracks"] if (t["slot"], t["title"]) not in RAUS]
    print("raus:", vorher - len(daten["tracks"]))
    bekannt = {t["source"] for t in daten["tracks"]}
    neu = []
    for slot, liste in AUSWAHL.items():
        for pid, titel, kuenstler, ki, cdn, seite in liste:
            quelle = "https://pixabay.com" + seite
            if quelle in bekannt:
                continue
            name = "px_%d.mp3" % pid
            datei = os.path.join(MUSIK, "audio", name)
            if not os.path.isfile(datei):
                req = urllib.request.Request(CDN + cdn, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req) as r, open(datei, "wb") as f:
                    f.write(r.read())
            roh = open(datei, "rb").read()
            laut = lautheit(datei)
            gain = round(min(1.0, 10 ** ((ZIEL_LUFS - float(laut["input_i"])) / 20)), 5)
            t = {"id": hashlib.md5(("pixabay:%d" % pid).encode()).hexdigest(), "title": titel, "artist": kuenstler + " (Pixabay)",
                 "isrc": "", "file": "audio/" + name, "seconds": dauer(datei), "gain": gain, "source": quelle,
                 "download_url": CDN + cdn, "license": LIZENZ, "license_url": LIZENZ_URL,
                 "sha256": hashlib.sha256(roh).hexdigest(), "bytes": len(roh), "loudness": laut,
                 "modifications": "Original MP3 unchanged; playback gain and scene transitions only.",
                 "ai_generated": bool(ki), "created": datetime.datetime.now(datetime.timezone.utc).isoformat(), "slot": slot}
            daten["tracks"].append(t)
            neu.append(t)
            print(slot, pid, titel, "gain", gain)
    daten["replace_slots"] = sorted({t["slot"] for t in daten["tracks"]})
    open(pfad, "w", encoding="utf-8").write(json.dumps(daten, ensure_ascii=False, indent=2) + "\n")

    md = os.path.join(MUSIK, "CREDITS.md")
    text = open(md, encoding="utf-8").read().rstrip("\n")
    for t in neu:
        ki = "\nKI-erzeugt (laut Pixabay)." if t["ai_generated"] else ""
        text += "\n\n## %s — %s\nQuelle: %s\nLizenz: %s — %s%s\nSHA256: %s" % (
            t["title"], t["artist"], t["source"], LIZENZ, LIZENZ_URL, ki, t["sha256"])
    open(md, "w", encoding="utf-8").write(text + "\n")
    hp = os.path.join(MUSIK, "CREDITS.html")
    seite = open(hp, encoding="utf-8").read()
    e = html.escape
    li = "".join('<li><b>%s</b> — %s%s. <a href="%s">Quelle</a> · <a href="%s">%s</a></li>' % (
        e(t["title"]), e(t["artist"]), " (KI-erzeugt)" if t["ai_generated"] else "", e(t["source"]), LIZENZ_URL, LIZENZ) for t in neu)
    open(hp, "w", encoding="utf-8").write(seite.replace("</ul></html>", li + "</ul></html>"))
    print("neu:", len(neu))


if __name__ == "__main__":
    main()

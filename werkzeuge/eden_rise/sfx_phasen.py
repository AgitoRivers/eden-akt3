# -*- coding: utf-8 -*-
r"""Phasenuebergaenge (Ducs Pixabay-Auswahl, 27.10.2026) herunterladen, kuerzen, ausblenden, angleichen.

    python werkzeuge\eden_rise\sfx_phasen.py

Ergebnis: docs\abnahme\sfx_pixabay\phasen_fertig\<slot>_<n>.mp3 (-18 LUFS) zum Probehoeren, bevor etwas ins Spiel kommt.
Pro Eintrag: (Pixabay-ID, CDN-Pfad, Seite, Schnitt in s oder None = ganz, Ausblende in s)."""
import os, subprocess, urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASIS = os.path.join(EDEN, "docs", "abnahme", "sfx_pixabay")
ROH, FERTIG = os.path.join(BASIS, "roh"), os.path.join(BASIS, "phasen_fertig")
CDN = "https://cdn.pixabay.com/audio/"

SLOTS = {
    "fruehstueck": [(13084, "2021/12/29/audio_9d00914116.mp3", "musical-acoustic-guitar-logo-13084", None, 0.3),
                    (335243, "2025/05/01/audio_2e90f68351.mp3", "musical-short-guitar-logo-335243", None, 0.5),
                    (156367, "2023/07/01/audio_1a97400328.mp3", "musical-acoustic-guitar-ident-156367", None, 0.5)],
    "tag": [(335043, "2025/04/30/audio_96a6295a15.mp3", "musical-calor-samba-outro-335043", None, 0.3),
            (360733, "2025/06/16/audio_d054d43778.mp3", "../../music/bossa-nova-call-me-bossa-loop-1-intro-360733", None, 0.5),
            (335041, "2025/04/30/audio_a89e1a7d09.mp3", "../../music/bossa-nova-calor-samba-loop-1-intro-335041", 6, 1.5),
            (616153, "2026/10/06/audio_b3d80e3dfe.mp3", "musical-caliente-merengue-6-seconds-616153", None, 0.5),
            (533703, "2026/05/13/audio_b40cef87cc.mp3", "musical-bossa-1-533703", 6, 1.5)],
    "nachmittag": [(263704, "2024/11/13/audio_1103ca3ee2.mp3", "musical-rhodes-85-263704", None, 0.5),
                   (576270, "2026/07/29/audio_3d97ca84bb.mp3", "musical-nostalgic-rhodes-chill-chord-576270", 6, 2.0),
                   (555916, "2026/07/01/audio_ef85d0ae62.mp3", "musical-rhodes-loop-90bpm-fm-arp-555916", 5, 2.0),
                   (449404, "2025/12/15/audio_a60164a101.mp3", "musical-old-school-hip-hop-logo-449404", None, 0.5)],
    "dinner": [(227426, "2024/07/27/audio_2e326def40.mp3", "musical-loop-jazz-piano-chords-amin-146bpm-227426", None, 1.5),
               (221272, "2024/07/01/audio_9e05f98283.mp3", "musical-sample-smooth-melody-chords-amin-146bpm-221272", None, 0.5),
               (555914, "2026/07/01/audio_7b46048b41.mp3", "musical-rhodes-loop-90bpm-cm-chords-555914", 6, 1.5),
               (610532, "2026/09/26/audio_84c4666991.mp3", "musical-short-jazz-melody-with-drums-610532", 6, 1.5),
               (151764, "2023/05/30/audio_91bebb7ff6.mp3", "musical-soft-cinematic-piano-outro-151764", None, 0.5)],
    "abend": [(575063, "2026/07/27/audio_3db56617e5.mp3", "musical-dreamy-lo-fi-groove-loop-01-575063", 5, 2.0),
              (472611, "2026/01/24/audio_ee3342f5ce.mp3", "laidback-lofi-9-sec-edit-472611", 6, 2.0),
              (340565, "2025/05/12/audio_d5736df263.mp3", "musical-lofi-music-night-groove-340565", None, 1.2)],
    "nacht": [(618240, "2026/10/09/audio_61cdc65d45.mp3", "musical-short-vinyl-lofi-transition-618240", None, 1.2),
              (575064, "2026/07/27/audio_e9afc28cc6.mp3", "musical-dreamy-lo-fi-groove-loop-02-575064", 5, 2.0),
              (575065, "2026/07/27/audio_8e865e40dd.mp3", "musical-dreamy-lo-fi-groove-loop-03-575065", 5, 2.0),
              (340565, "2025/05/12/audio_d5736df263.mp3", "musical-lofi-music-night-groove-340565", None, 1.2)],
    "anhoerung_phase": [(227277, "2024/07/26/audio_5752f044eb.mp3", "film-special-effects-sci-fi-intro-logo-reveal-3-227277", None, 0.3)],
    "anhoerung_wende": [(227274, "2024/07/26/audio_9d9081e630.mp3", "film-special-effects-sci-fi-intro-logo-reveal-6-227274", None, 0.3)],
}


def ff(*a):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *a], check=True)


def dauer(datei):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", datei],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    os.makedirs(ROH, exist_ok=True)
    os.makedirs(FERTIG, exist_ok=True)
    quellen = ["# Phasenuebergaenge - Quellen (Pixabay Content License)", ""]
    for slot, liste in SLOTS.items():
        for n, (pid, pfad, seite, schnitt, aus) in enumerate(liste, 1):
            roh = os.path.join(ROH, "px_%d.mp3" % pid)
            if not os.path.isfile(roh):
                req = urllib.request.Request(CDN + pfad, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req) as r, open(roh, "wb") as f:
                    f.write(r.read())
            ende = min(schnitt or 99, dauer(roh))
            tmp = os.path.join(FERTIG, "_tmp.wav")
            # Stille am Anfang weg, kuerzen, ausblenden; danach Lautheit wie die anderen Einzeltoene.
            ff("-i", roh, "-af", "silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:%.2f,afade=t=out:st=%.2f:d=%.2f"
               % (ende, max(0, ende - aus), aus), tmp)
            aus_datei = os.path.join(FERTIG, "%s_%d.mp3" % (slot, n))
            ff("-i", tmp, "-af", "loudnorm=I=-18:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2", "-b:a", "160k", aus_datei)
            os.remove(tmp)
            quellen.append("- `%s_%d.mp3` <- https://pixabay.com/sound-effects/%s/ (%s)"
                           % (slot, n, seite, "ganz" if not schnitt else "auf %d s, %.1f s Ausblende" % (schnitt, aus)))
            print(slot, n, pid, "%.1f s" % dauer(aus_datei))
    open(os.path.join(FERTIG, "QUELLEN.md"), "w", encoding="utf-8").write("\n".join(quellen) + "\n")


if __name__ == "__main__":
    main()

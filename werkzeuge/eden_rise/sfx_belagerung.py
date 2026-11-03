# -*- coding: utf-8 -*-
r"""Toene der Belagerung (Duc 01.11.2026, Abnahme docs/abnahme/sfx_belagerung.html). Pixabay Content License.

    python werkzeuge\eden_rise\sfx_belagerung.py

Laedt die Wahl nach docs\abnahme\sfx_pixabay\roh, schneidet sie auf den Moment im Spiel und legt sie als <id>_1.mp3 nach
module\eden_rise\sfx. Schnittstellen sind gemessen (Huellkurve), der Hammer ist ein einzelner Schlag aus einer Folge.
Zeile: id -> (Quelle, Pixabay-Seite, Start, Laenge, Ausblende, LUFS). Quelle: CDN-Pfad oder eine vorhandene Datei im sfx-Ordner.
Einzeltoene -18 LUFS wie ueberall, Schritte leiser, damit sie unter den Treffern liegen, Schleifen -30."""
import os, subprocess, urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROH = os.path.join(EDEN, "docs", "abnahme", "sfx_pixabay", "roh")
SFX = os.path.join(EDEN, "module", "eden_rise", "sfx")
CDN = "https://cdn.pixabay.com/download/audio/"

T = {
    "tk_taser": ("2024/05/16/audio_b2f747af90.mp3", "film-special-effects-electric-shock-short-circuit-1-204989", 0.75, 1.0, 0.3, -18),
    "tk_flinte": ("2025/05/30/audio_87b126642c.mp3", "film-special-effects-shotgun-blast-352038", 0.28, 1.6, 0.5, -18),
    "tk_klinge": ("2025/07/05/audio_ec4d591a44.mp3", "film-special-effects-katana-370403", 0.18, 0.7, 0.15, -18),
    "tk_drohne": ("2026/06/04/audio_d4f0490ffe.mp3", "film-special-effects-drone-quadcopter-fast-fly-by-sound-546575", 2.6, 2.8, 0.8, -20),
    "tk_roboter": ("2024/03/08/audio_e88143d576.mp3", "film-special-effects-robot-heavy-mechanical-footsteps-194039", 0.0, 1.55, 0.25, -19),
    "tk_ko": ("2025/01/03/audio_2baf08c268.mp3", "film-special-effects-drum-huge-cinematic-tom-hit-283585", 0.0, 1.4, 0.4, -18),
    "tk_stahlplatte": ("2022/03/25/audio_c9e27a7264.mp3", "film-special-effects-heavy-cloth-rustle-106346", 0.0, 1.6, 0.3, -20),
    "tk_schritte": ("2022/03/24/audio_b31c4f3225.mp3", "film-special-effects-footsteps-boots-101657", 0.0, 1.05, 0.2, -26),
    "tk_zugwechsel": ("2023/09/30/audio_2bbb7a3c06.mp3", "film-special-effects-whoosh-drum-hits-169007", 0.1, 1.5, 0.5, -19),
    "tk_cutin": ("anhoerung_wende_1.mp3", None, 0.0, 1.8, 0.5, -18),
    "tk_holzbruch": ("2022/03/10/audio_93312656c3.mp3", "household-wood-break-40011", 1.42, 1.9, 0.3, -18),
    "tk_kirche": ("2023/10/18/audio_9d2e3ceb0f.mp3", "film-special-effects-door-slam-172171", 0.0, 1.1, 0.3, -18),
    "tk_haus_weg": ("2025/08/05/audio_eec51c73eb.mp3", "film-special-effects-building-collapse-384812", 2.4, 3.0, 0.8, -18),
    "tk_yacht_sinkt": ("2022/03/10/audio_5333e50327.mp3", "film-special-effects-wreck-bg-33420", 36.0, 8.0, 2.0, -18),
    "tk_loewe": ("2025/11/28/audio_a83280ddfa.mp3", "nature-powerful-lion-roar-sound-effect-high-quality-sfx-444190", 0.0, 2.6, 0.5, -16),
    "tk_rauch": ("2022/03/18/audio_30de469656.mp3", "film-special-effects-gas-grenade-95255", 0.0, 3.0, 1.0, -20),
    "tk_jubel": ("2021/08/09/audio_865e392ddd.mp3", "people-crowdyayapplause25ppllong-6948", 0.3, 5.0, 1.5, -20),
    "tk_hammer": ("2022/03/19/audio_1712057a76.mp3", "household-hammering-nail-96677", 0.32, 0.42, 0.1, -18),
    "tk_bretter": ("2026/01/18/audio_621998353e.mp3", "boards-fall-1-468371", 0.32, 1.55, 0.3, -18),
    "tk_bucht": ("2025/01/22/audio_ae267fbe88.mp3", "film-special-effects-cinematic-low-hit-291095", 0.0, 2.0, 0.6, -18),
    "tk_granate": ("kampf_granate_flash_1.mp3", None, 0.0, 1.5, 0.5, -18),
    "tk_glocke": ("glocke_1.mp3", None, 0.0, None, 0, None),
    "tk_gitter": ("gitter_1.mp3", None, 0.0, None, 0, None),
    "tk_unit_werkstatt": ("kampf_unit01_2.mp3", None, 0.0, None, 0, None),
    "tk_unit_wasser": ("kampf_unit01_3.mp3", None, 0.0, None, 0, None),
    "tk_yacht_riss": ("2025/05/30/audio_8865fd3bde.mp3", "film-special-effects-iron-smash-with-debris-351841", 0.05, 2.55, 0.5, -18),
    "tk_drohne_ab": ("2026/09/19/audio_43495cb9e0.mp3", "film-special-effects-metal-crack-606770", 0.0, None, 0, -18),
    "tk_haus_feuer": ("2021/08/04/audio_f4d9d2a2b3.mp3", "film-special-effects-short-fireball-woosh-6146", 0.0, None, 0, -18),
    "tk_haus_schreie": ("2022/03/14/audio_d29f9b4e6f.mp3", "people-029586-crowd-in-panic-66480", 0.4, 4.5, 1.5, -24),
    "tk_liste": ("2026/08/13/audio_1127255689.mp3", "film-special-effects-foley-paper-handling-amp-page-turning-sfx-584919", 2.7, 3.1, 0.3, -22),
    "tk_megan_weg": ("2025/07/24/audio_80472f5d2c.mp3", "film-special-effects-digital-glitch-noise-hd-379465", 0.0, None, 0, -20),
    "amb_maschine": ("2022/03/09/audio_6bcc8fa5b7.mp3", "film-special-effects-mysterion-low-ship-humming-25686", 0.0, None, 0, -30),
    # Drehbuch Finale (Duc 02.11.2026, Abnahme docs/abnahme/sfx_pixabay/finale_auswahl.html)
    "tk_ligeia": ("2022/03/09/audio_c654b01b43.mp3", "musical-dream-vocal-pad-25888", 0.0, 10.0, 3.0, -20),
    "tk_applaus": ("2022/03/26/audio_fe7418532b.mp3", "people-small-crowd-clapping-2-106993", 0.53, 6.0, 2.0, -20),
    "tk_kevin": ("2021/08/04/audio_0833f830cc.mp3", "nature-birds-taking-off-fly-6277", 0.0, None, 0, -18),
    "tk_rudern": ("2022/01/18/audio_49f3a76a9a.mp3", "nature-paddle-boat-on-waterwav-14861", 2.0, 7.0, 1.5, -22),
    "tk_papier": ("2023/12/05/audio_517f50359d.mp3", "film-special-effects-firewood-burning-sound-179862", 3.0, 6.0, 2.0, -22),
    "tk_kreide": ("2022/03/15/audio_8dbfd3128f.mp3", "film-special-effects-writing-on-black-board-3-86723", 0.0, 2.8, 0.4, -20),
    "tk_drucker": ("2022/03/26/audio_b38645002f.mp3", "technology-printer-106935", 0.0, 4.5, 0.8, -20),
}


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def roh_datei(sid, quelle):
    if quelle.endswith(".mp3") and "/" not in quelle:
        return os.path.join(SFX, quelle)
    pfad = os.path.join(ROH, "tk_" + quelle.rsplit("_", 1)[1])
    if not os.path.exists(pfad):
        req = urllib.request.Request(CDN + quelle, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://pixabay.com/"})
        with urllib.request.urlopen(req, timeout=60) as r, open(pfad, "wb") as f:
            f.write(r.read())
    return pfad


def maxwell_schlag():
    """Maxwells Treffer (Duc 02.11.2026, Abnahme docs/abnahme/sfx_maxwell.html): Stahl obenauf, darunter nur der tiefe Teil des Heavy Metal Crush."""
    stahl = roh_datei("tk_maxwell_schlag", "2025/12/20/audio_eef1deb265.mp3")     # hammer-steel-impact-454390
    tief = roh_datei("tk_maxwell_schlag", "2025/05/30/audio_336eebf829.mp3")      # film-special-effects-heavy-metal-crush-351840
    ff("-i", stahl, "-i", tief, "-filter_complex",
       "[0:a]aresample=44100,aformat=channel_layouts=stereo,atrim=start=0.05:end=1.0,asetpts=PTS-STARTPTS,afade=t=in:d=0.005[a];"
       "[1:a]aresample=44100,aformat=channel_layouts=stereo,atrim=start=0.29:end=1.0,asetpts=PTS-STARTPTS,lowpass=f=240,afade=t=in:d=0.005,afade=t=out:st=0.4:d=0.31[b];"
       "[a][b]amix=inputs=2:duration=longest:normalize=0,afade=t=out:st=0.65:d=0.3[o]",
       "-map", "[o]", os.path.join(ROH, "_maxwell.wav"))
    ff("-i", os.path.join(ROH, "_maxwell.wav"), "-af", "loudnorm=I=-16:TP=-1.0:LRA=11", "-ar", "44100", "-ac", "2", "-b:a", "160k", os.path.join(SFX, "tk_maxwell_schlag_1.mp3"))
    os.remove(os.path.join(ROH, "_maxwell.wav"))


def minicu_fall():
    """Der eine Schlag gegen Minicu (Duc 02.11.2026): erst Heavy Object Falling (291096), direkt danach Body Fall (259680), dann Stille."""
    schwer = roh_datei("tk_minicu_fall", "2025/01/22/audio_97c83e0986.mp3")      # film-special-effects-heavy-object-falling-291096
    koerper = roh_datei("tk_minicu_fall", "2024/11/04/audio_5fd41bb140.mp3")     # film-special-effects-body-fall-259680
    ff("-i", schwer, "-i", koerper, "-filter_complex",
       "[0:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=end=1.15,asetpts=PTS-STARTPTS,afade=t=out:st=1.0:d=0.15[a];"
       "[1:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=end=0.6,asetpts=PTS-STARTPTS[b];"
       "[a][b]concat=n=2:v=0:a=1[o]", "-map", "[o]", os.path.join(ROH, "_minicu.wav"))     # loudnorm in einem Schritt liefert bei so kurzen Toenen nichts
    ff("-i", os.path.join(ROH, "_minicu.wav"), "-af", "loudnorm=I=-16:TP=-1.0:LRA=11", "-ar", "44100", "-ac", "2", "-b:a", "160k", os.path.join(SFX, "tk_minicu_fall_1.mp3"))
    os.remove(os.path.join(ROH, "_minicu.wav"))


def schleife_krieg():
    """Hintergrund der Karte: die lauten 40 Sekunden in der Mitte, das Ende blendet in den Anfang, damit die Schleife keine Naht hat."""
    ein = roh_datei("amb_taktik", "2025/10/09/audio_b02ed6a9c3.mp3")          # film-special-effects-war-scene-distant-gunshots-414168
    ff("-i", ein, "-filter_complex", "[0:a]asplit=2[x][y];[x]atrim=6:46,asetpts=PTS-STARTPTS,afade=t=in:d=3[a];[y]atrim=46:49,asetpts=PTS-STARTPTS,afade=t=out:d=3[b];"
       "[a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-30:TP=-1.5:LRA=11[o]", "-map", "[o]", "-ar", "44100", "-ac", "2", "-b:a", "160k", os.path.join(SFX, "amb_taktik_1.mp3"))


def bauen(sid, quelle, seite, start, sek, aus, lufs):
    ziel = os.path.join(SFX, sid + "_1.mp3")
    ein = roh_datei(sid, quelle)
    if lufs is None:                                    # dieselbe Datei, nur mit fester Variante
        ff("-i", ein, "-c", "copy", ziel)
        return
    f = "atrim=start=%.2f" % start + (":end=%.2f" % (start + sek) if sek else "") + ",asetpts=PTS-STARTPTS"
    if start:
        f += ",afade=t=in:d=0.01"
    if sek:
        f += ",afade=t=out:st=%.2f:d=%.2f" % (sek - aus, aus)
    ff("-i", ein, "-af", f + ",loudnorm=I=%d:TP=-1.5:LRA=11" % lufs, "-ar", "44100", "-ac", "2", "-b:a", "160k", ziel)


if __name__ == "__main__":
    os.makedirs(ROH, exist_ok=True)
    for sid, z in T.items():
        bauen(sid, *z)
        print("fertig:", sid)
    schleife_krieg()
    maxwell_schlag()
    minicu_fall()

# -*- coding: utf-8 -*-
r"""Klaenge fuer Holms Wette (Duc 30.10.2026): alles von Pixabay (Pixabay Content License).

    python werkzeuge\eden_rise\sfx_schiessen.py                 Vorschlaege laden, schneiden, angleichen, nach module\eden_rise\sfx
    python werkzeuge\eden_rise\sfx_schiessen.py flasche=2 ...   andere Kandidaten waehlen (Nummer wie in docs\abnahme\schiessen_klang.json)
    python werkzeuge\eden_rise\sfx_schiessen.py --spec          nur die Abnahme-Seite schreiben

Stille am Anfang faellt weg, damit der Klang mit dem Treffer kommt. Treffer sind kurz (hoechstens 1,4 s mit Ausblende), Moewe 1,8 s,
Blendgranate 2 s (Duc: das Pfeifen nur 2 Sekunden), alles -18 LUFS wie die uebrigen Einzeltoene. Abgenommen 30.10.2026: die jeweils ersten; Schuss und Nachladen in Runde 2 (schiessen_klang_r2.json),
Nachladen auf Ducs Wunsch etwas lauter und mit mehr Bass."""
import json, os, shutil, subprocess, sys, tempfile, urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SFX = os.path.join(EDEN, "module", "eden_rise", "sfx")
SPEC = os.path.join(EDEN, "docs", "abnahme", "schiessen_klang.json")
CDN = "https://cdn.pixabay.com/download/audio/"
K = {  # Ziel: (Titel, Sekunden, [(Name, CDN-Pfad, Pixabay-Seite)]) - der erste ist der Vorschlag
    "gun_shot": ("Schuss", 1.1, [
        ("Shotgun Firing (4) · freesound_community", "2021/08/09/audio_42c2ce9d86.mp3", "film-special-effects-shotgun-firing-4-6746")]),
    "gun_reload": ("Nachladen", 2.0, [
        ("Rifle-or-shotgun-reload · freesound_community", "2021/08/09/audio_91cfcc96c2.mp3", "film-special-effects-rifle-or-shotgun-reload-6787")]),
    "schiessen_flasche": ("Flasche zerspringt", 1.4, [
        ("Glass Bottle Smash · Universfield", "2024/12/17/audio_0a00729be9.mp3", "film-special-effects-glass-bottle-smash-277554"),
        ("Glass Bottle Smash · Universfield", "2024/02/19/audio_e1ff566468.mp3", "film-special-effects-glass-bottle-smash-191998"),
        ("Bottle Shatter · Universfield", "2024/08/02/audio_f31fd2d3e8.mp3", "film-special-effects-bottle-shatter-229205"),
        ("Glass break 3 · EAGLAXLE", "2026/05/07/audio_4ba150229c.mp3", "film-special-effects-glass-break-3-530786")]),
    "schiessen_ton": ("Tontaube zerspringt", 1.2, [
        ("Plate Break 1 · freesound_community", "2022/03/10/audio_72c13eae35.mp3", "household-plate-break-1-36468"),
        ("Break the ceramic tiles · spinopel", "2025/09/28/audio_e2af439c0f.mp3", "film-special-effects-break-the-ceramic-tiles-411504")]),
    "schiessen_drohne": ("Drohne fällt aus", 1.4, [
        ("Metal Crack Electrical Circuit Brake · Tutmozis", "2026/09/19/audio_fc60af0994.mp3", "film-special-effects-metal-crack-electrical-circuit-brake-606771"),
        ("Electronic element burn spark 1 · FxProSound", "2024/10/08/audio_d2090a2c23.mp3", "film-special-effects-electronic-element-burn-spark-1-248606"),
        ("Electric Shock Short Circuit 4 · floraphonic", "2024/04/28/audio_a550796a9e.mp3", "film-special-effects-electric-shock-short-circuit-4-204986")]),
    "schiessen_moewe": ("Möwe getroffen", 1.8, [
        ("Seagulls Squawking 3 FX · SOUND_GARAGE", "2025/09/08/audio_12ef7e66a8.mp3", "nature-seagulls-squawking-3-fx-401400"),
        ("Seagulls Squawking 4 FX · SOUND_GARAGE", "2025/09/08/audio_357f1fb7fb.mp3", "nature-seagulls-squawking-4-fx-401398"),
        ("Seagull Calls · DRAGON-STUDIO", "2025/05/10/audio_9cb830e075.mp3", "nature-seagull-calls-339723")]),
    "schiessen_blend": ("Blendgranate", 2.0, [
        ("Stun Grenade Flashbang (schon im Kampf)", "2026/05/30/audio_89f760f671.mp3", "film-special-effects-stun-grenade-flashbang-543949")]),
}
EXTRA = {"gun_reload": ("bass=g=7:f=130,acompressor=threshold=-26dB:ratio=6:attack=2:release=80:makeup=10,alimiter=limit=0.9,", -15)}     # kurze Klicks: erst verdichten, sonst deckeln die Spitzen die Lautheit
START = "silenceremove=start_periods=1:start_threshold=-50dB,"


def ffmpeg(*a):
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def fertig(quelle, ziel, sek, extra=("", -18)):
    ffmpeg("-i", quelle, "-af", START + "atrim=end=%.2f,afade=t=out:st=%.2f:d=0.25,%sloudnorm=I=%d:TP=-1.5:LRA=11" % (sek, sek - 0.25, extra[0], extra[1]),
           "-ar", "44100", "-ac", "2", "-b:a", "160k", ziel)


def spec():
    gruppen = [{"id": z, "titel": t, "soll": "Kurz und knackig, sonst übertönt es den nächsten Schuss. Der erste ist mein Vorschlag und schon im Spiel.",
                "max": 1, "kandidaten": [{"titel": n, "cdn": p.replace("/download", ""), "seite": s} for n, p, s in kand]}
               for z, (t, _, kand) in K.items()]
    json.dump({"id": "schiessen_klang", "titel": "Holms Wette – Klänge", "gruppen": gruppen,
               "hinweis": "Je Ziel einen Favoriten wählen. Pixabay Content License. Schuss und Nachladen kommen aus dem freigegebenen Soundlabor."},
              open(SPEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Spec: " + SPEC)


def main():
    if "--spec" in sys.argv:
        spec()
        return
    wahl = dict(a.split("=") for a in sys.argv[1:])
    with tempfile.TemporaryDirectory() as tmp:
        for ziel, (_, sek, kand) in K.items():
            kurz = ziel.split("_")[-1]
            n = int(wahl.get(kurz, 1))
            roh = os.path.join(tmp, ziel + ".mp3")
            req = urllib.request.Request(CDN + kand[n - 1][1], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as r, open(roh, "wb") as f:
                shutil.copyfileobj(r, f)
            fertig(roh, os.path.join(SFX, ziel + "_1.mp3"), sek, EXTRA.get(ziel, ("", -18)))
            print("fertig: %s (%s)" % (ziel, kand[n - 1][0]))
    spec()


if __name__ == "__main__":
    main()

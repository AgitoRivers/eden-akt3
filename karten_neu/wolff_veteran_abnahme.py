# -*- coding: utf-8 -*-
r"""Abnahme-Spec fuer den vollen Satz Wolff "Der Veteran": docs\abnahme\wolff_veteran_satz.json, daneben jeweils die alte Pose."""
import glob, json, os

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_wolff_veteran_satz"
FIG = r"X:\AI\Eden\module\eden_rise\figuren\Kaspar Wolff"
KAMPF = r"X:\AI\Eden\module\eden_rise\kampf\Wolff"
HINWEISE = {"surprise": "Die Beine sind überkreuzt, das steht so in der Pose-Karte.", "annoyance": "Die Beine sind überkreuzt, das steht so in der Pose-Karte.",
            "disgust": "Ein Fuß ist angehoben, das kann schwebend wirken.", "caring": "Ein Fuß ist angehoben.", "curiosity": "Leicht von oben, der Kopf wirkt dadurch groß.",
            "flee": "Wird beim Einbau gespiegelt, damit er nach rechts wegläuft.", "love_2": "Neu: Der alte Satz hatte diese Pose nicht."}
items = []
for art, ordner, alt, end in (("dialog", "Dialog", FIG, ".png"), ("kampf", "Kampf", KAMPF, ".webp")):
    for p in sorted(glob.glob(os.path.join(W, art, "*.png"))):
        pose = os.path.basename(p)[:-4]
        name = pose.replace("_2", "")
        it = {"id": "%s_%s" % (art, pose), "titel": "%s · %s" % (ordner, name), "bild": p, "soll": HINWEISE.get(pose, "Gesicht, Rüstung und Schwert wie deine Wahl."),
              "vergleich": os.path.join(alt, name + end), "vergleich_titel": "Alter Wolff"}
        items.append(it)
spec = {"id": "wolff_veteran_satz_v1", "titel": "Sergent Kaspar Wolff: voller Satz", "items": items,
        "hinweis": "22 Dialog-Posen und 13 Kampf-Posen auf Basis von Dialog 3 und Kampf 3. Mein Vorschlag: alles übernehmen. Nur was nicht passt, auf „Neu“ setzen. Ins Spiel kommt der Satz erst nach deinem Urteil."}
with open(r"X:\AI\Eden\docs\abnahme\wolff_veteran_satz.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print(len(items))

# -*- coding: utf-8 -*-
r"""Abnahme-Spec fuer den vollen Satz Mr. Maximum mit Steel Mop: docs\abnahme\maximum_steelmop_satz.json, daneben das alte Bild."""
import glob, json, os

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_maximum_steelmop_satz"
ALT_D = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Maximum\Steward\Sorted"
ALT_K = r"X:\AI\Eden\module\eden_rise\kampf\MaxwellMaximum"
HINWEISE = {
    "kampf_idle": "Grundpose, deine Wahl: der Würfel auf der Schulter.",
    "kampf_flee": "Der Borstenring sitzt auf einem Stummel seitlich am Würfel statt ums Rohr. Wird beim Einbau gespiegelt.",
    "kampf_hurt": "Am Würfel ist eine kleine dunkle Stelle zu sehen, der Kranz liegt um die ganze Fläche.",
    "kampf_heavy_attack": "Vorn ragt ein kurzer Stummel aus dem Würfel.",
    "kampf_enraged": "Am Würfel ist eine kleine dunkle Stelle zu sehen.",
    "kampf_attack": "Der Kranz liegt um die ganze Fläche des Würfels, nicht nur ums Rohr. Das gilt auch für guard, windup, heavy_windup, weakened und victory.",
    "kampf_defeated": "Ohne Waffe, wie vorher bestellt nichts in den Händen.",
    "kampf_surrender": "Ohne Waffe.",
    "dialog_caring_2": "Er kniet, das steht so in der Pose-Karte.",
    "dialog_gratitude_2": "Er kniet, das steht so in der Pose-Karte.",
    "dialog_relief": "Er kniet, das steht so in der Pose-Karte.",
    "dialog_grief_2": "Er sitzt zusammengekauert, das steht so in der Pose-Karte.",
    "dialog_remorse_2": "Er sitzt zusammengesunken, das steht so in der Pose-Karte.",
    "dialog_joy_2": "Luftsprung, nur für echte Freude.",
    "dialog_optimism_2": "Eine Hand reicht fast bis zum Bildrand.",
    "dialog_neutral": "Dein gewähltes Bild.",
}
items = []
for art, ordner, alt, end in (("dialog", "Dialog", ALT_D, ".png"), ("kampf", "Kampf", ALT_K, ".webp")):
    for p in sorted(glob.glob(os.path.join(W, art, "*.png"))):
        pose = os.path.basename(p)[:-4]
        i = "%s_%s" % (art, pose)
        v = os.path.join(alt, pose.replace("_2", "-1").replace("_3", "-2") + end)
        it = {"id": i, "titel": "%s · %s" % (ordner, pose), "bild": p, "soll": HINWEISE.get(i, "Wie deine Wahl.")}
        if os.path.isfile(v):
            it.update(vergleich=v, vergleich_titel="Bisher")
        items.append(it)
spec = {"id": "maximum_steelmop_satz_v1", "titel": "Mr. Maximum: voller Satz mit Steel Mop", "items": items,
        "hinweis": "44 Dialog-Posen ohne Waffe und 13 Kampf-Posen. Mein Vorschlag: den Dialog übernehmen und im Kampf nur flee und heavy_attack neu machen, dort stört der Stummel am Würfel am meisten. Nur was nicht passt, auf „Neu“ setzen. Es wird ein eigener Satz, die alten bleiben."}
with open(r"X:\AI\Eden\docs\abnahme\maximum_steelmop_satz.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print(len(items))

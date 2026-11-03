# -*- coding: utf-8 -*-
r"""Abnahme-Spec fuer die vollen Saetze PirateBrawler und PirateGunner: docs\abnahme\piraten_neu_satz.json."""
import glob, json, os

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_piraten_neu_satz"
HINWEISE = {"brawler_idle": "Deine Wahl.", "gunner_idle": "Deine Wahl.",
            "brawler_guard": "Beide Hände am Griff, die Klinge steht senkrecht vor dem Gesicht, wie bei Wolffs guard.",
            "gunner_guard": "Der Mantel schwingt als Deckung nach vorn, der Unterarm ist oben, die Pistole bleibt an der Brust.",
            "gunner_attack": "Fertig ohne Mündungsfeuer, das kommt im Kampf als Effekt.", "gunner_heavy_attack": "Beide Hände an der Pistole, ohne Mündungsfeuer.",
            "brawler_flee": "Wird beim Einbau gespiegelt, damit er nach rechts wegläuft.", "gunner_flee": "Wird beim Einbau gespiegelt, damit er nach rechts wegläuft.",
            "gunner_windup": "Der Daumen spannt den Hahn, das sieht man nur bei genauem Hinsehen.",
            "brawler_defeated": "Ohne Waffe.", "gunner_defeated": "Ohne Waffe.", "brawler_surrender": "Ohne Waffe.", "gunner_surrender": "Ohne Waffe."}
items = []
for art, titel in (("brawler", "Brawler"), ("gunner", "Gunner")):
    for p in sorted(glob.glob(os.path.join(W, art, "*.png"))):
        pose = os.path.basename(p)[:-4]
        i = "%s_%s" % (art, pose)
        items.append({"id": i, "titel": "%s · %s" % (titel, pose), "bild": p, "soll": HINWEISE.get(i, "Wie deine Wahl.")})
spec = {"id": "piraten_neu_satz_v1", "titel": "Zwei neue Piraten: volle Sätze", "items": items,
        "hinweis": "Je 13 Kampf-Posen auf Basis von Brawler 1 und Gunner 1. Mein Vorschlag: alles übernehmen. Nur was nicht passt, auf „Neu“ setzen. Ins Spiel kommen die Sätze erst nach deinem Urteil, Pirate und PirateAlpha bleiben."}
with open(r"X:\AI\Eden\docs\abnahme\piraten_neu_satz.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print(len(items))
